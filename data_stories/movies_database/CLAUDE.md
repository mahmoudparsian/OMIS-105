# CLAUDE.md — Movies Database (DuckDB + Marimo)

This file documents the project for future iterations. It records what was
built, how, and why, plus exactly how to rebuild and run everything.

## Goal

Convert a set of **MySQL** dump files for a movie database into a **DuckDB**
database (`movies_db.duckdb`), then build two **Marimo** notebooks of
pure-SQL example queries (basic → intermediate+), with detailed explanations
and charts.

## Source data

12 MySQL dump files (`01_…sql` … `12_…sql`) describe a TMDB-style movie
database with **17 tables** and **4,803 movies**. The central table is
`movie`; people, genres, keywords, companies, languages and countries each
have their own table and are linked to movies through bridge tables.

Schema (all names are already lower-case snake_case):

| Table | Key columns | Notes |
|---|---|---|
| `movie` | movie_id (PK) | title, budget, revenue, popularity, release_date, runtime, vote_average, vote_count, … |
| `person` | person_id (PK) | person_name |
| `genre` | genre_id (PK) | genre_name |
| `keyword` | keyword_id (PK) | keyword_name |
| `production_company` | company_id (PK) | company_name |
| `country` | country_id (PK) | country_iso_code, country_name |
| `language` | language_id (PK) | language_code, language_name |
| `language_role` | role_id (PK) | Original / Spoken |
| `gender` | gender_id (PK) | Unspecified / Female / Male |
| `department` | department_id (PK) | crew departments |
| `movie_cast` | movie_id, person_id, gender_id (FKs) | character_name, cast_order |
| `movie_crew` | movie_id, person_id, department_id (FKs) | job |
| `movie_company` | movie_id, company_id (FKs) | |
| `movie_genres` | movie_id, genre_id (FKs) | |
| `movie_keywords` | movie_id, keyword_id (FKs) | |
| `movie_languages` | movie_id, language_id, language_role_id (FKs) | |
| `production_country` | movie_id, country_id (FKs) | |

Row counts (verified): country 88, department 12, gender 3, genre 20,
keyword 9,794, language 88, language_role 2, movie 4,803, movie_cast 106,257,
movie_company 13,677, movie_crew 129,581, movie_genres 12,160,
movie_keywords 36,162, movie_languages 11,740, person 104,842,
production_company 5,047, production_country 6,436.

## Directory layout

```
movies_database/
├── mysql_sql/               # ORIGINAL MySQL dumps (unchanged)
├── duckdb_sql/              # GENERATED DuckDB-compatible SQL  + validate.sql
├── create_duckdb.sh            # builds movies_db.duckdb and validates it
├── notebook_01_basics.py        # Marimo notebook 1 (GENERATED)
├── notebook_02_intermediate.py  # Marimo notebook 2 (GENERATED)
├── plot_util.py            # all plotting code (decoupled from notebooks)
├── requirements.txt        # python deps for the notebooks
├── scripts/                # all build/validation tooling (see below)
│   ├── convert_to_duckdb.py    # MySQL → DuckDB SQL converter
│   ├── query_specs.py          # single source of truth for all 35 queries
│   ├── gen_notebooks.py        # builds the two notebooks from query_specs
│   ├── validate_sql.py         # loads generated SQL, prints row counts
│   ├── check_fk_integrity.py   # confirms no orphaned foreign keys
│   ├── test_queries.py         # runs every notebook query on the real data
│   └── test_plots.py           # renders every chart to catch plot errors
├── blog/                   # reference material (schema image, sample queries)
└── movies_db.duckdb        # BUILT database (created by create_duckdb.sh)
```

## MySQL → DuckDB conversion (`scripts/convert_to_duckdb.py`)

The converter is a character-level scanner so structural rewrites never touch
text inside data strings, and string-escape rewrites only fire inside strings.

Transformations:
- Drop `DROP DATABASE` / `CREATE DATABASE` (DuckDB's database *is* the file).
- Remove the `movies.` schema qualifier (objects live in the default `main`
  schema): `DROP/CREATE/INSERT/REFERENCES … movies.X → X`.
- Remove `AUTO_INCREMENT` (every row already has an explicit id).
- Strip integer display widths: `BIGINT(20) → BIGINT`, `int(5) → INTEGER`.
- Drop bare `COMMIT;` lines (with or without trailing `;`).
- Convert MySQL string escapes to ANSI/DuckDB form **inside string literals**:
  `\' → ''`, `\" → "`, `\r` removed. Already-doubled `''` (empty strings and
  standard quotes) pass through unchanged.

Column/table names were already lower-case snake_case, so no renaming was
needed (the converter asserts this).

Regenerate at any time:
```bash
python3 scripts/convert_to_duckdb.py
```

## Building the database

```bash
./create_duckdb.sh
```
Requires the DuckDB CLI (`brew install duckdb`). The script regenerates the
converted SQL (if `python3` is present), builds a fresh `movies_db.duckdb` by
loading the 12 files **in dependency order** (reference tables → movie →
bridge tables, so foreign keys resolve), then runs `duckdb_sql/validate.sql`
(table list, row counts, a 3-table join smoke test).

## Validation strategy

DuckDB and SQLite share ANSI string escaping (`''`) and loose/affinity typing,
so the build was validated **without** DuckDB installed:
- `scripts/validate_sql.py` — loads all generated SQL into in-memory SQLite;
  all 12 files parse, 17 tables, 4,803 movies; no empty DATE/numeric values.
- `scripts/check_fk_integrity.py` — confirms **0 orphaned foreign keys** across
  all 17 FK relationships (DuckDB enforces FKs at insert time, so this matters).
- `scripts/test_queries.py` — executes **all 35 notebook queries** against the
  real data (SQLite with `year()`/`floor()` shims; window funcs, CTEs, subqueries
  all run) and checks each plot's referenced columns exist. All pass.
- `scripts/test_plots.py` — renders **all 28 charts** via `plot_util` to a PNG to
  catch any plotting error. All pass.

When DuckDB itself is available, prefer `./create_duckdb.sh` for the authoritative
build + validation.

## The notebooks

Generated from `scripts/query_specs.py` by `scripts/gen_notebooks.py`:
```bash
python3 scripts/gen_notebooks.py
```

Run them (after building the DB):
```bash
pip install -r requirements.txt
marimo edit notebook_01_basics.py        # or: marimo run notebook_01_basics.py
marimo edit notebook_02_intermediate.py
```

Design:
- **Setup cell** opens a READ-ONLY DuckDB connection (`conn`) to
  `movies_db.duckdb` (path resolved relative to the notebook).
- Every query is a **pure SQL cell**: `result = mo.sql(f"""…""", engine=conn)`.
  Passing `engine=conn` makes each SQL cell depend on the connection cell, so
  marimo's reactive runtime always runs them in the correct order.
- Each query has a **markdown explanation** (what we're doing + the SQL concept),
  the **SQL**, the **result table**, and a **chart** where useful.
- **All plotting lives in `plot_util.py`** (matplotlib: `barh`, `bar`, `line`),
  keeping notebook cells SQL-only. Column access uses `df[col].to_list()`, which
  works for both polars and pandas frames, so no specific dataframe lib is forced.

### Notebook 1 — `notebook_01_basics.py` (15 queries)
- 5 simple: count; top-10 revenue; top-10 rated; counts by status; longest runtime.
- 5 simple+: `LIKE`; date `BETWEEN`; movies-per-year; aggregate summary; compound `AND`.
- 5 intermediate (joins/aggregations): top Action; movies per genre; busiest actors;
  Forrest Gump cast; top production countries.

### Notebook 2 — `notebook_02_intermediate.py` (20 queries)
- 5 simple+: top popularity; per-decade; most profitable; avg rating/yr (`HAVING`);
  rating distribution.
- 5 intermediate: top directors; top companies; rating by genre; top keywords;
  revenue by genre.
- 10 intermediate+: Top-N-per-group via `ROW_NUMBER`; top-3 per genre; `RANK` within
  year; scalar subquery (above-avg popularity); `LIMIT/OFFSET`; cumulative `SUM`
  window; genre share via `SUM() OVER ()`; actor box-office (CTE + join + agg);
  top actor per gender (chained CTEs + `RANK`); year-over-year change via `LAG`.

## DuckDB SQL notes used here
- `year(release_date)` and `EXTRACT(YEAR FROM …)` both work.
- Decade bucketing: `CAST(FLOOR(year(d)/10.0)*10 AS INTEGER)`.
- Date literals: `DATE '2005-01-01'`.
- Window functions (`ROW_NUMBER/RANK/LAG/SUM OVER`), CTEs (`WITH`), scalar
  subqueries, and `LIMIT … OFFSET` are all supported.

## Regenerate everything from scratch
```bash
python3 scripts/convert_to_duckdb.py     # MySQL → DuckDB SQL
python3 scripts/validate_sql.py          # parse + row counts (no DuckDB needed)
python3 scripts/check_fk_integrity.py    # FK integrity
python3 scripts/test_queries.py          # all 35 queries run on real data
python3 scripts/gen_notebooks.py         # build both notebooks
python3 scripts/test_plots.py            # render all charts
./create_duckdb.sh                           # authoritative build (needs duckdb CLI)
```

## Status / iteration log
- **Iteration 1 (complete):** SQL converted + validated (sqlite + FK checks),
  `create_duckdb.sh` + `validate.sql` written, both notebooks generated and their
  queries/plots verified against the real data, `plot_util.py` written.
  Outstanding: run `./create_duckdb.sh` on a machine with the DuckDB CLI to produce
  the actual `movies_db.duckdb`, then launch the notebooks.
