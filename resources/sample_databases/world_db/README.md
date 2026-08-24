# The World Database

**Every country. Every major city. Every language. One tiny file.**

## The Story

In the early 2000s, the team behind MySQL needed one sample database
that could teach *every* SQL idea at once — filtering, joins,
aggregation, subqueries — without inventing a fake company or a toy
dataset nobody cared about. They picked the most universal subject
there is: **the entire planet.**

The result, nicknamed simply **"world,"** ships with almost every
MySQL install on Earth and has quietly taught SQL to millions of
students for more than 20 years. It is small enough to fit in a
2 MB file, yet real enough to answer genuinely interesting
questions: *Which country is the most densely populated? Where does
a capital city lose out to a bigger rival in its own country? Which
continent has the widest life-expectancy gap?*

This folder ports that same classic dataset to **DuckDB** — no
server, no installation, no `CREATE USER`. Just `world.duckdb`, one
file, ready to query the moment you open it.

## What's Inside

| Table | Rows | What it holds |
|-------|-----:|----------------|
| `country` | 239 | Population, GNP, life expectancy, government form, independence year — one row per country |
| `city` | 4,079 | Name, district, population — every major city, linked to its country |
| `countrylanguage` | 984 | Which languages are spoken where, what share of the population speaks them, and whether they're official |

Together, these 3 tables describe **6+ billion people** across
**7 continents**, speaking **457 distinct languages** — and every
one of those numbers is something you compute yourself in the
notebooks below, not a number we're just telling you.

## Quick Facts to Get You Curious

- The world's most populous city in this dataset is **Mumbai**
  (10.5M), followed by Seoul and São Paulo.
- 239 countries share only **7** continent labels — so `GROUP BY
  continent` collapses a *lot* of detail into a handful of rows.
  That's the whole point of aggregation.
- Some countries have **no independence year** at all — they're
  still dependencies or overseas territories. Finding them is a
  one-line `WHERE ... IS NULL` query, and a good first taste of how
  much a single filter can reveal.

## Files in This Folder

```
world_db/
├── world.duckdb              # the database — open this, nothing to build
├── world_queries.ipynb       # 20 queries, Jupyter edition
├── world_queries_marimo.py   # the same 20 queries, Marimo edition
├── world_plots.py            # shared plotting helpers (matplotlib) — used by BOTH notebooks
├── world_mysql.sql           # original MySQL source this was ported from
├── world_duckdb_utf8.sql     # the DuckDB-flavored SQL that built world.duckdb
├── world_duckdb_latin1.sql   # intermediate encoding step (see "How It Was Built" below)
├── convert_to_utf8.sh        # latin1 → utf8 conversion script
└── build_duckb_from_utf8.sh  # builds world.duckdb from the utf8 SQL
```

## Two Notebooks, One Set of Questions

Both notebooks ask the **same 20 questions** — 5 basic, 10
intermediate, 5 advanced — against the same database, and draw the
same charts using the same `world_plots.py` module. Pick whichever
tool fits the moment:

- **`world_queries.ipynb`** — classic Jupyter. Each cell calls a
  `run(sql)` helper that executes the query and displays the result.
- **`world_queries_marimo.py`** — Marimo, this course's primary
  notebook tool. SQL cells run directly against DuckDB with
  `mo.sql(...)` — no Python wrapper needed, and cells re-run
  automatically whenever something they depend on changes.

### Open the Jupyter version

```bash
jupyter notebook world_queries.ipynb
```

### Open the Marimo version

```bash
marimo edit world_queries_marimo.py
```

Both notebooks connect to `world.duckdb` in **read-only** mode, so
there's no way to accidentally damage the shared file — query all
you like.

## The 20 Questions

| Level | Count | You will practice |
|-------|------:|--------------------|
| **Basic** | 5 | `SELECT`, `DISTINCT`, `WHERE`, `ORDER BY`, `LIMIT` |
| **Intermediate** | 10 | `JOIN`, `GROUP BY`, `HAVING`, subqueries, `STRING_AGG`, correlated subqueries |
| **Advanced** | 5 | CTEs (`WITH`), `RANK() OVER (PARTITION BY ...)`, `MEDIAN`, `PERCENTILE_CONT`, tuple-subquery joins |

Every query cell is preceded by a short **"What are we doing?"**
explanation — read that before you read the SQL. Most also produce a
chart, so you can *see* the answer, not just read a table of numbers.

## How It Was Built

`world.duckdb` was ported from the original MySQL `world` database
in three steps:

1. `world_mysql.sql` (the original MySQL dump) was hand-adapted into
   DuckDB-compatible SQL.
2. `convert_to_utf8.sh` ran `iconv` to fix the encoding
   (`world_duckdb_latin1.sql` → `world_duckdb_utf8.sql`) — the
   original dump has Latin-1 characters in country names.
3. `build_duckb_from_utf8.sh` loaded the UTF-8 SQL straight into a
   fresh DuckDB file:
   ```bash
   duckdb world.duckdb < world_duckdb_utf8.sql
   ```

You don't need to repeat any of this — `world.duckdb` is already
built and checked into this folder.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
