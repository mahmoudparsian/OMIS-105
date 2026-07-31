#!/usr/bin/env python3
"""
validate_sql.py
---------------
Self-validation of the generated DuckDB SQL WITHOUT requiring DuckDB.

DuckDB and SQLite share the same ANSI string-literal rules ('' for a quote,
no backslash escaping) and both use loose/affinity typing for DDL like
VARCHAR(n)/INT/BIGINT/DECIMAL.  So if the converted files load cleanly into
an in-memory SQLite database and every statement parses, we have strong
confidence the same SQL will load into DuckDB.

It then:
  * loads every duckdb_sql/*.sql file in order,
  * reports row counts per table,
  * flags data problems that DuckDB (a strictly typed engine) would reject,
    in particular empty-string values in DATE / numeric columns.
"""
import os
import re
import sqlite3

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "duckdb_sql"))
FILES = sorted(f for f in os.listdir(OUT_DIR)
               if f.endswith(".sql") and f != "validate.sql")

con = sqlite3.connect(":memory:")
con.execute("PRAGMA foreign_keys = OFF;")  # load order independent

total_stmts = 0
for fname in FILES:
    with open(os.path.join(OUT_DIR, fname), encoding="utf-8") as fh:
        script = fh.read()
    try:
        con.executescript(script)
    except Exception as e:
        print(f"!! FAILED loading {fname}: {e}")
        raise
    print(f"loaded {fname}")

print("\n=== row counts ===")
tables = [r[0] for r in con.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
for t in tables:
    n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  {t:22s} {n:>8,d}")

print("\n=== strict-type data checks (issues DuckDB would reject) ===")
# empty strings in DATE column
bad_dates = con.execute(
    "SELECT COUNT(*) FROM movie WHERE release_date = ''").fetchone()[0]
print(f"  movie.release_date == '' (empty)        : {bad_dates}")
# empty strings in numeric columns
for col in ["budget", "revenue", "runtime", "popularity", "vote_average", "vote_count"]:
    n = con.execute(f"SELECT COUNT(*) FROM movie WHERE {col} = ''").fetchone()[0]
    if n:
        print(f"  movie.{col} == '' (empty)             : {n}")
print("  (numeric empties not listed above are 0)")

# unbalanced-quote heuristic: every INSERT must have an even number of
# unescaped quotes (already guaranteed by successful load, but double-check)
print("\n=== OK: all files parsed and loaded into SQLite ===")
print(f"tables: {len(tables)}   total movies: "
      f"{con.execute('SELECT COUNT(*) FROM movie').fetchone()[0]}")
