# CLAUDE.md — Top 500 Movies (DuckDB + Marimo data story)

Guidance for any AI assistant (or human) working in this folder.

## What this project is

An OMIS 105 teaching notebook that turns a scraped "Top 500 movies" CSV into a
persistent **DuckDB** database and tells a data story through **20 progressively
harder SQL queries**, each explained, displayed, and charted. The notebook is
built with **Marimo** (a reactive Python notebook) and keeps query cells in
**pure SQL**.

## Files

| File | Role |
|---|---|
| `top_500_movies_ranked.csv` | Source data — 449 movies, 26 columns. **Read-only.** |
| `top_500_movies.py` | The Marimo notebook (the deliverable). Builds the DB and runs all queries. |
| `util_plot.py` | All matplotlib plotting helpers, decoupled from the notebook. |
| `top_500_movies.duckdb` | Persistent DuckDB database, **created when the notebook runs**. |
| `web_scraping_top_500_movies.py` | The original scraper that produced the CSV (reference only). |
| `what_to_do.txt` | The original task brief. |

## How to run

```bash
pip install marimo duckdb pandas matplotlib   # polars optional (mo.sql uses it if present)
cd /path/to/Top_500_Movies
marimo edit top_500_movies.py      # interactive editor
# or
marimo run top_500_movies.py       # read-only app view
```

Run from **this folder** (the notebook resolves the CSV/DB paths via
`mo.notebook_dir()`, falling back to the current directory).

**Version note:** the SQL cells call `mo.sql(..., engine=conn)`, where `conn` is a
DuckDB connection. This requires a reasonably recent Marimo (≈0.8+). If `mo.sql`
rejects the `engine` argument, upgrade Marimo.

## Architecture / conventions

- **One concept per cell trio.** Every analytical step is three cells: a markdown
  briefing → a pure-SQL cell → a chart cell. Keep this rhythm when adding queries.
- **Pure SQL.** Query logic lives in `mo.sql(...)` cells, not in Python. The only
  Python in a query path is the build cell's `conn.execute(BUILD_SQL)` and small
  DataFrame reshapes inside *plot* cells (e.g. Q16's pivot).
- **Plotting is decoupled.** No matplotlib in the notebook — call helpers in
  `util_plot.py` (`barh_top`, `bar`, `line`, `grouped_bar`, `scatter`,
  `stacked_bar`). They accept pandas **or** polars and return a `Figure`, which
  Marimo renders when it's the cell's last expression.
- **Ordering via dataflow.** The build cell returns `conn`; every SQL cell takes
  `conn` as a parameter, so Marimo guarantees the table exists before any query
  runs. Do not rely on top-to-bottom file order — Marimo is reactive.
- **Naming.** SQL cell outputs are `q1`…`q20` (plus `schema`, `explorer`). Temp
  variables inside cells are `_`-prefixed so Marimo treats them as cell-local.

## Data model

The build SQL (in the "BUILD THE DATABASE" cell) does the full ETL in one
`CREATE OR REPLACE TABLE movies AS ...` statement with three CTEs:

1. `raw` — `read_csv_auto` of the CSV.
2. `renamed` — every column renamed to **lower_snake_case**
   (`IMDb_Votes` → `imdb_votes`, `Critic_Rating_RT` → `critic_rating_rt`, etc.).
   Note `Cast` → `"cast"` is quoted because `cast` is a SQL keyword.
3. `derived` — engineered columns, then a final `SELECT` adds the totals.

### Derived columns

| Column | Definition |
|---|---|
| `decade` | `(year / 10) * 10` |
| `era` | `CASE`: Classic (<1970) / Modern (1970–1999) / Contemporary (2000+) |
| `primary_genre` | `trim(split_part(genre, ',', 1))` |
| `num_genres` | comma count in `genre` + 1 |
| `is_english` | `language = 'en'` |
| `num_cast_members` | comma count in `cast` + 1 (0 if null) |
| `num_streaming_platforms` | comma count in `streaming_on` + 1 (0 if null) |
| `oscar_wins`, `oscar_nominations` | `regexp_extract` of `Won N Oscar` / `Nominated for N Oscar` |
| `other_wins`, `other_nominations` | `regexp_extract` of `N wins` / `N nominations` |
| `total_wins`, `total_nominations` | Oscar + other |

## The 20 queries (and the concept each teaches)

**Simple** — 1 top by Custom Score · 2 top by IMDb (multi-key sort) · 3 audience
favourites (`IS NOT NULL`) · 4 most-voted · 5 best since 2018 (range filter).

**Simple+** — 6 films per decade · 7 per language · 8 per primary genre ·
9 English vs world (`CASE` + `AVG`) · 10 avg IMDb by decade.

**Intermediate** — 11 genre tags via `UNNEST` (cross join) · 12 director
leaderboard (`HAVING`) · 13 critics-vs-audience `JOIN` of two CTEs · 14 language
stats (`HAVING`) · 15 awards by genre.

**Intermediate+** — 16 top-3 per decade (`ROW_NUMBER`) · 17 director `RANK()`
from a `WITH` pool · 18 best film per genre (`ROW_NUMBER`, `rn = 1`) ·
19 films above their decade average (`WITH` benchmark + `JOIN`) · 20 score
quartiles (`NTILE(4)`).

**Bonus** — a reactive explorer: `mo.ui.dropdown` + `mo.ui.slider` parameterise an
f-string SQL cell that re-runs automatically (the notebook-native concept).

## Gotchas

- DuckDB folds unquoted identifiers and is case-insensitive, but `cast` is a
  reserved word — always quote it as `"cast"`.
- `mo.sql` returns a **polars** DataFrame when polars is installed, otherwise
  **pandas**. `util_plot` handles both via `_as_pandas`; keep new helpers tolerant.
- The `.duckdb` file is a build artifact. Deleting it is safe — re-running the
  notebook recreates it. Don't commit it as source of truth.
- The sandbox used to author this could not install DuckDB/Marimo (no network),
  so the SQL and notebook were verified statically (compile + cell-graph) and
  against a pandas re-implementation of every query. If you change the build SQL,
  re-run the notebook locally to confirm.
