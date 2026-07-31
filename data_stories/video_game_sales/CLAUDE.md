# CLAUDE.md — Video Game Sales Data Story

Guidance for working in this project (OMIS 105 · Data Stories).

## Purpose

Teach SQL using a real, lightly-messy dataset. We clean a CSV of video-game
sales into a DuckDB database, then teach SQL through a graded series of queries.

## Data

`video_game_sales.csv` — ~16,600 games with sales > 100k copies, scraped from
vgchartz.com. One row = one game *release on a specific platform*.

Columns (after `snake_case` normalization):

| column | meaning |
| --- | --- |
| `rank` | overall sales ranking (surrogate id, unique per row) |
| `name` | game title |
| `platform` | console/platform (Wii, NES, PS3, …) |
| `year` | release year (nullable INTEGER; 271 missing) |
| `genre` | genre |
| `publisher` | publisher (58 missing) |
| `na_sales` | North America sales, millions |
| `eu_sales` | Europe sales, millions |
| `jp_sales` | Japan sales, millions |
| `other_sales` | rest-of-world sales, millions |
| `global_sales` | worldwide total, millions |

The four regional columns + `global_sales` are measurements at the same grain
(one game-platform), so they stay in the **single `sales` table** — no separate
table is needed. Reshape to long form with a *view* if a chart needs it.

## Files

| file | role |
| --- | --- |
| `video_game_sales.csv` | raw input |
| `01_build_database.ipynb` | Notebook 1 — clean CSV → `sales_db.duckdb` |
| `02_sql_queries.ipynb` | Notebook 2 — 20 progressive SQL teaching queries |
| `sales_db.duckdb` | generated DuckDB database, single `sales` table |
| `util_plot.py` | all matplotlib plotting helpers (decoupled from notebooks) |
| `video-games-sales-analysis-and-visualization.ipynb` | reference Kaggle notebook |
| `metadata.txt` | dataset description |
| `what-to-do.txt` | assignment spec |

## Conventions

- **Column names:** lowercase `snake_case`, no spaces (e.g. `na_sales`).
- **Duplicates:** a *true* duplicate is a row identical in every column **except**
  `rank` (which is a unique surrogate id). There is exactly one in this dataset
  (`Wii de Asobu: Metroid Prime`, Wii). Rows sharing name/platform/year but with
  *different* sales (e.g. `Madden NFL 13`) are **not** duplicates.
- **Plotting:** never put matplotlib code in a notebook cell. Add a helper to
  `util_plot.py` and call it. Pattern per query cell: explain → SQL → result table
  → plot.
- **Notebooks are re-runnable:** Notebook 1 deletes and rebuilds `sales_db.duckdb`
  from scratch each run.

## Environment

```bash
pip install duckdb pandas matplotlib jupyter
```

Run notebooks from this directory so the relative paths to the CSV and the
`.duckdb` file resolve.

## Workflow status

- [x] Notebook 1 — build & clean database (verified)
- [x] Notebook 2 — SQL teaching queries (20 queries: 3.1 simple → 3.4 windows/CTEs)
