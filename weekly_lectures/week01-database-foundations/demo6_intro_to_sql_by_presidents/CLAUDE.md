# CLAUDE.md

Guidance for working in this project. Read this first.

## What this project is

A self-contained teaching notebook that introduces **DuckDB** (an in-process
analytical SQL database) using a small, friendly data set: the 47 U.S.
presidencies and their political parties. It is built for **OMIS 105, Santa Clara
University**. The notebook walks from basic `SELECT` statements up through joins,
aggregations, window functions, and CTEs, with a chart for almost every query.

## Files

| File | Role |
|---|---|
| `data/presidents.csv` | Source data — one row per presidency (`sequence, last_name, first_name, term_start, term_end, party_id`). 47 rows. |
| `data/parties.csv` | Lookup table — `party_id, party_name`. 7 rows. |
| `duckdb_presidents.py` | **The main deliverable.** A Marimo notebook (not Jupyter — this was converted from an earlier `.ipynb`, which no longer exists). |
| `util_plot.py` | All plotting code, fully decoupled from the notebook. |
| `presidents_db.duckdb` | The DuckDB database file. **Generated** by running the notebook (not committed). |
| `CLAUDE.md` | This file. |

## How to run

```bash
pip install duckdb pandas matplotlib seaborn marimo
marimo edit duckdb_presidents.py
```

To verify without opening the browser UI: `python3 duckdb_presidents.py` should
run every cell top to bottom and exit 0. The notebook is **idempotent**: it
deletes and rebuilds `presidents_db.duckdb` each run, so the output is always
reproducible.

**2026-09-06:** the notebook's SQL cells were converted from `mo.sql()` to the
`con.execute()` pattern (repo-wide standard — see the root `CLAUDE.md`). An
explicit `con = duckdb.connect(database=":memory:")` cell now exists; a couple
of downstream cells that used the module-level `duckdb.sql(...)` (relying on
`mo.sql()`'s implicit default connection) were repointed to `con.sql(...)`
since they'd otherwise query an empty, disconnected database.

## Database schema (after the notebook builds it)

`parties` — loaded as-is from `parties.csv`:

- `party_id` (INTEGER), `party_name` (VARCHAR)

`presidents` — loaded from `presidents.csv` **plus derived columns** computed at
load time (notebook §2.2):

| Column | Type | Source |
|---|---|---|
| `sequence` | INT | raw |
| `last_name`, `first_name` | VARCHAR | raw |
| `full_name` | VARCHAR | derived: `first_name || ' ' || last_name` |
| `term_start`, `term_end` | DATE | raw, cast from string |
| `party_id` | INT | raw (foreign key → `parties.party_id`) |
| `term_days` | INT | derived: `term_end - term_start` (DuckDB date diff = integer days) |
| `term_years` | DOUBLE | derived: `term_days / 365.25` |
| `term_start_year`, `term_end_year` | INT | derived: `YEAR(...)` |
| `century` | VARCHAR | derived: `CASE` on `term_start_year` |

## Notebook structure

The notebook follows the assignment's required progression. Every query is
presented in four steps: (1) a plain-English explanation, (2) cleanly formatted
SQL run via `con.execute(sql).df()`, (3) the result as a DataFrame, and (4) a
chart when one helps.

- **§4.1 — 5 simple queries:** `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `COUNT`.
- **§4.2 — 5 simple+ queries:** `BETWEEN`, `LIKE`, `IN`, `CASE`, computed columns.
- **§4.3 — 5 intermediate queries:** `JOIN`, `GROUP BY`, `HAVING`, aggregates.
- **§4.4 — 5 intermediate+ queries:** Top-N, `RANK()`, `SUM() OVER`, `AVG() OVER`,
  `LAG()`, and `WITH` (CTEs).
- **§4.5 — Key concepts:** querying a pandas DataFrame directly with SQL, the
  relational/method-chaining API, and big-picture visualisations.

## Plotting conventions (`util_plot.py`)

**All** plotting lives in `util_plot.py`. The notebook never calls matplotlib
directly except `plt.show()`. Each helper takes a tidy pandas DataFrame (exactly
what `.df()` returns) and returns a `matplotlib.figure.Figure`.

- Call `util_plot.set_theme()` once near the top of the notebook (helpers also
  call it defensively).
- `PARTY_COLORS` maps each party to a recognisable brand colour (Democratic blue,
  Republican red, Whig gold, etc.). Reuse it for any new party-segmented chart.
- Available helpers: `plot_presidents_per_party`, `plot_term_length_distribution`,
  `plot_term_timeline`, `plot_avg_term_by_party`, `plot_top_n_longest`,
  `plot_cumulative_days`, `plot_presidents_per_century`, `plot_term_vs_sequence`.

When adding a chart: write a new function in `util_plot.py` (don't inline plotting
in the notebook), accept a DataFrame, return a Figure, and reuse `set_theme()`,
`PARTY_COLORS`, and `_style_axes()` for visual consistency.

## Conventions for editing

- Keep SQL readable: uppercase keywords, aligned clauses, one concept per query.
- Prefer the derived columns (`term_days`, `full_name`, `century`, …) over
  recomputing date math inline.
- Keep the notebook idempotent — never assume a pre-existing database.
- Keep plotting out of the notebook; it belongs in `util_plot.py`.
