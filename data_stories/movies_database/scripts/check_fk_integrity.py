#!/usr/bin/env python3
"""Check foreign-key integrity, since DuckDB enforces FKs at insert time."""
import os, sqlite3
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "duckdb_sql"))
con = sqlite3.connect(":memory:")
for f in sorted(os.listdir(OUT_DIR)):
    if f.endswith(".sql") and f != "validate.sql":
        con.executescript(open(os.path.join(OUT_DIR, f), encoding="utf-8").read())

# (child table, child col, parent table, parent col)
fks = [
    ("movie_cast", "movie_id", "movie", "movie_id"),
    ("movie_cast", "person_id", "person", "person_id"),
    ("movie_cast", "gender_id", "gender", "gender_id"),
    ("movie_company", "movie_id", "movie", "movie_id"),
    ("movie_company", "company_id", "production_company", "company_id"),
    ("movie_crew", "movie_id", "movie", "movie_id"),
    ("movie_crew", "person_id", "person", "person_id"),
    ("movie_crew", "department_id", "department", "department_id"),
    ("movie_genres", "movie_id", "movie", "movie_id"),
    ("movie_genres", "genre_id", "genre", "genre_id"),
    ("movie_keywords", "movie_id", "movie", "movie_id"),
    ("movie_keywords", "keyword_id", "keyword", "keyword_id"),
    ("movie_languages", "movie_id", "movie", "movie_id"),
    ("movie_languages", "language_id", "language", "language_id"),
    ("movie_languages", "language_role_id", "language_role", "role_id"),
    ("production_country", "movie_id", "movie", "movie_id"),
    ("production_country", "country_id", "country", "country_id"),
]
problems = 0
for ct, cc, pt, pc in fks:
    q = (f"SELECT COUNT(*) FROM {ct} c WHERE c.{cc} IS NOT NULL "
         f"AND NOT EXISTS (SELECT 1 FROM {pt} p WHERE p.{pc} = c.{cc})")
    n = con.execute(q).fetchone()[0]
    flag = "" if n == 0 else "  <-- ORPHANS"
    if n: problems += 1
    print(f"  {ct}.{cc} -> {pt}.{pc:14s}: {n:>6,d} orphans{flag}")
print("\nFK integrity:", "CLEAN" if problems == 0 else f"{problems} relationship(s) with orphans")
