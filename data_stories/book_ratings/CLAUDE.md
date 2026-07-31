# CLAUDE.md

Guidance for Claude (and humans) working in this project.

## Project

OMIS 105 · Data Stories · **Book Ratings**. A teaching project that builds a clean
DuckDB database from raw CSVs and then uses it to teach SQL through a series of
progressively harder queries.

## Files

| File | Purpose |
|------|---------|
| `books.csv` | Raw data, ~10,000 books (one row per book) + some intentionally messy rows. |
| `ratings.csv` | Raw data, ~980k ratings, columns `book_id, user_id, rating`. |
| `books_db.duckdb` | The cleaned database produced by Notebook 1. Tables: `books`, `ratings`. |
| `01_build_database.ipynb` | **Notebook 1** — ETL: load CSVs, normalize columns, remove duplicates, verify. |
| `02_sql_queries.ipynb` | **Notebook 2** — teaches SQL against `books_db.duckdb`. (built after NB1 is verified) |
| `util_plot.py` | All matplotlib plotting helpers. Notebooks import this, not raw plotting code. |
| `what-to-do.txt` | The original assignment spec. Source of truth for requirements. |

## Data facts (verified against the real files)

- `books.csv`: 10,000 clean rows + **7 exact duplicate rows** (ids 9986–9992)
  + **7 malformed rows** that have an extra field / 24 columns instead of 23
  (ids 19986–19992).
- `ratings.csv`: well-formed, with **1,644 duplicate rows**.
- **Load behavior (DuckDB v1.5.x):** `read_csv(..., ignore_errors=true)` *salvages*
  the 7 malformed rows (truncates the extra field) rather than skipping them, so the
  raw load is **10,014** rows. `SELECT DISTINCT *` then removes the 7 exact duplicates,
  leaving `books` = **10,007** rows. The 7 salvaged dirty rows (ids 19986–19992) remain
  because they are not exact duplicates of any other row. They have altered titles/authors,
  empty image URLs, and `book_id` values that do **not** appear in `ratings` — which is
  why query 3.4 ("books not rated by anyone") returns exactly these 7 rows.
- After cleaning: `books` = **10,007** rows, `ratings` = **980,112** rows.

## Schema (after normalization)

- `books`: `id, book_id, best_book_id, work_id, books_count, isbn, isbn13, authors,
  original_publication_year, original_title, title, language_code, average_rating,
  ratings_count, work_ratings_count, work_text_reviews_count, ratings_1, ratings_2,
  ratings_3, ratings_4, ratings_5, image_url, small_image_url`
- `ratings`: `book_id, user_id, rating`
- Join key: `ratings.book_id` ↔ **`books.id`** (both range 1–10000). NOT `books.book_id`,
  which holds large Goodreads ids that do not appear in `ratings`.

## Conventions

- **Column names**: lowercase, words joined by `_`, no spaces. A `normalize_columns()`
  helper in Notebook 1 enforces this and is safe to re-run.
- **Database engine**: DuckDB, accessed from Python via `duckdb.connect("books_db.duckdb")`.
- **Duplicate detection**: `GROUP BY ALL ... HAVING COUNT(*) > 1`.
- **Deduplication**: `CREATE OR REPLACE TABLE t AS SELECT DISTINCT * FROM t`.
- **Plotting**: never inline matplotlib in a notebook cell — add/extend a function in
  `util_plot.py` and call it. Each helper returns a matplotlib `Figure`.

## Notebook cell pattern (required for teaching notebooks)

Each query should be presented as:

1. **Markdown** — clearly explain *what* we are doing and *why*.
2. **SQL** — nicely formatted query (uppercase keywords, indented clauses).
3. **Result** — displayed as a DataFrame (`con.execute(sql).df()`).
4. **Plot** — visualize via `util_plot` when it adds insight.

## Notebook 2 plan (from the spec)

- 3.0 Add derived columns if useful (e.g. rating spread, total ratings).
- 3.1 five simple queries · 3.2 five simple+ · 3.3 five intermediate.
- 3.4 one query: books not rated by anyone.
- 3.5 five intermediate+ (Top-N, window/ranking functions, `WITH` subqueries).
- Demonstrate key SQL concepts progressively.

## Workflow

1. Build/modify Notebook 1, user verifies.
2. Only then build Notebook 2.
3. Keep this file current when data facts, schema, or conventions change.

## Environment notes

- Requires `duckdb`, `pandas`, `matplotlib`. Run notebooks from this directory so the
  relative paths (`books.csv`, `ratings.csv`, `books_db.duckdb`) resolve.
