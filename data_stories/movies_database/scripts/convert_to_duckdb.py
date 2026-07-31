#!/usr/bin/env python3
"""
convert_to_duckdb.py
--------------------
Convert the original MySQL dump files (01_*.sql .. 12_*.sql) into
DuckDB-compatible SQL files written to ../duckdb_sql/.

Transformations applied
========================
DDL (structure)
  * Drop  `DROP DATABASE` / `CREATE DATABASE` statements (DuckDB has no
    server-side databases; the database *is* the .duckdb file).
  * Remove the `movies.` schema qualifier so every object lives in the
    default `main` schema  (DROP/CREATE/INSERT/REFERENCES ... movies.X -> X).
  * Remove `AUTO_INCREMENT` (DuckDB uses sequences; every row already
    supplies an explicit id, so we simply keep the column as INTEGER).
  * Strip MySQL display widths on integer types:
        BIGINT(20) -> BIGINT      int(5) -> INTEGER
  * Drop bare `COMMIT;` lines (DuckDB autocommits).

DML (string literals inside the data)
  * MySQL backslash escapes are converted to ANSI-SQL / DuckDB form:
        \'  ->  ''     (a literal apostrophe becomes a doubled quote)
        \"  ->  "      (a literal double quote is just a double quote)
        \r  ->  (carriage return removed)
    Already-doubled quotes ('') are valid in DuckDB and pass through.

Naming
  * All table and column names in the source are already lower-case
    snake_case, so no renaming is required; the script asserts this.

The transformation is performed with a single character-level scanner so
that the DDL rewrites never touch text that lives *inside* a data string,
and the escape rewrites only ever fire *inside* a string.
"""

import os
import re
import sys

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(SRC_DIR, "duckdb_sql")

FILES = [
    "01_reference_data.sql",
    "02_keyword.sql",
    "03_person.sql",
    "04_production_company.sql",
    "05_movie.sql",
    "06_movie_cast.sql",
    "07_movie_company.sql",
    "08_movie_crew.sql",
    "09_movie_genres.sql",
    "10_movie_keywords.sql",
    "11_movie_languages.sql",
    "12_production_country.sql",
]


def convert_strings(text):
    """Char-level scan: rewrite MySQL escapes only inside single-quoted strings."""
    out = []
    i = 0
    n = len(text)
    in_str = False
    while i < n:
        c = text[i]
        if not in_str:
            out.append(c)
            if c == "'":
                in_str = True
            i += 1
            continue
        # inside a single-quoted string
        if c == "\\":
            nxt = text[i + 1] if i + 1 < n else ""
            if nxt == "'":
                out.append("''")      # literal apostrophe -> doubled quote
                i += 2
            elif nxt == '"':
                out.append('"')        # literal double quote
                i += 2
            elif nxt == "\\":
                out.append("\\")      # literal backslash
                i += 2
            elif nxt == "r":
                i += 2                 # drop carriage return
            elif nxt == "n":
                out.append("\n")      # newline stays a real newline
                i += 2
            elif nxt == "t":
                out.append("\t")
                i += 2
            elif nxt == "":
                out.append(c)
                i += 1
            else:
                out.append(nxt)        # unknown escape -> drop the backslash
                i += 2
        elif c == "'":
            out.append("'")            # terminator (or start of '' empty/escaped)
            in_str = False
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def convert_ddl(text):
    """Structural rewrites that only ever appear in DDL / statement headers."""
    # remove server-database statements
    text = re.sub(r"(?im)^\s*DROP\s+DATABASE\s+IF\s+EXISTS\s+movies\s*;\s*$\n?", "", text)
    text = re.sub(r"(?im)^\s*CREATE\s+DATABASE\s+movies\s*;\s*$\n?", "", text)
    # strip the schema qualifier in every context it is used
    text = text.replace("DROP TABLE IF EXISTS movies.", "DROP TABLE IF EXISTS ")
    text = text.replace("CREATE TABLE movies.", "CREATE TABLE ")
    text = text.replace("INSERT INTO movies.", "INSERT INTO ")
    text = text.replace("REFERENCES movies.", "REFERENCES ")
    # remove AUTO_INCREMENT
    text = re.sub(r"\s+AUTO_INCREMENT", "", text)
    # integer display widths
    text = re.sub(r"(?i)\bBIGINT\(\s*\d+\s*\)", "BIGINT", text)
    text = re.sub(r"(?i)\bINT\(\s*\d+\s*\)", "INTEGER", text)
    # drop bare COMMIT (with or without a trailing semicolon)
    text = re.sub(r"(?im)^\s*COMMIT\s*;?\s*$\n?", "", text)
    return text


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    summary = []
    for fname in FILES:
        src = os.path.join(SRC_DIR, fname)
        with open(src, "r", encoding="utf-8") as fh:
            raw = fh.read()

        # 1) structural DDL rewrites happen outside of any data string
        ddl = convert_ddl(raw)
        # 2) string-escape normalization (only fires inside quoted strings)
        out = convert_strings(ddl)

        # sanity: schema qualifier and MySQL-isms must be gone
        assert "movies." not in re.sub(r"'[^']*'", "", out), f"residual movies. in {fname}"
        assert "AUTO_INCREMENT" not in out, f"residual AUTO_INCREMENT in {fname}"
        assert not re.search(r"(?i)\bINT\(\d+\)", out), f"residual int(N) in {fname}"

        # header banner
        banner = (
            f"-- ============================================================\n"
            f"-- {fname}  ->  DuckDB-compatible\n"
            f"-- Auto-generated by scripts/convert_to_duckdb.py. Do not edit by hand.\n"
            f"-- ============================================================\n\n"
        )
        dst = os.path.join(OUT_DIR, fname)
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(banner + out)

        summary.append((fname, len(raw), len(out)))

    print(f"Converted {len(FILES)} files -> {OUT_DIR}")
    for name, a, b in summary:
        print(f"  {name:30s} {a:>9,d} -> {b:>9,d} bytes")


if __name__ == "__main__":
    main()
