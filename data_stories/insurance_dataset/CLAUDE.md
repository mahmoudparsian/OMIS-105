# Insurance Dataset — SQL Teaching Project

## Overview
Teaching SQL queries using a medical insurance dataset with DuckDB and Jupyter notebooks. Part of OMIS 105 at Santa Clara University.

## Dataset
- **Source:** `insurance.csv` (1,773 rows including header, 1,760 unique rows after dedup)
- **Columns:** `age`, `gender`, `bmi`, `children`, `smoker`, `region`, `charges`
- **Database:** `insurance_db.duckdb` — single table `insurance` with no duplicates

### Derived Columns (added in Notebook 2)
- `age_group` — 18-29, 30-39, 40-49, 50-64
- `bmi_category` — Underweight / Normal / Overweight / Obese (WHO thresholds)
- `charge_level` — Low / Medium / High / Very High (quartile-based)
- `cost_per_child` — charges / children (NULL if no children)

## Files

| File | Purpose |
|------|---------|
| `insurance.csv` | Raw data |
| `insurance_db.duckdb` | Clean DuckDB database (built by Notebook 1) |
| `01_build_database.ipynb` | Load CSV, find/remove duplicates, persist to DuckDB |
| `02_sql_queries_tutorial.ipynb` | 20 SQL queries across 4 difficulty tiers + concepts summary |
| `util_plot.py` | Reusable plotting functions (decoupled from notebooks) |
| `what-to-do.txt` | Original task specification |

## Notebook Structure

### Notebook 1 — Build Database
Reads CSV → identifies and displays duplicates → removes them via `ROW_NUMBER()` → persists clean table to `insurance_db.duckdb` → verifies zero duplicates.

### Notebook 2 — SQL Tutorial
Each query cell follows this pattern: explanation → SQL → result → plot (when applicable).

- **3.0** Add derived columns
- **3.1** Simple (Q1–Q5): SELECT, WHERE, ORDER BY, LIMIT, COUNT, DISTINCT
- **3.2** Simple+ (Q6–Q10): AVG, GROUP BY, HAVING, BETWEEN, ROUND
- **3.3** Intermediate (Q11–Q15): CASE, conditional aggregation, scalar subqueries, STDDEV
- **3.4** Intermediate+ (Q16–Q20): ROW_NUMBER, DENSE_RANK, PERCENT_RANK, NTILE, CTEs, running totals, JOINs
- **3.5** Key SQL concepts summary (7 concept blocks with syntax templates)

## Running
1. Run `01_build_database.ipynb` first to create `insurance_db.duckdb`
2. Then run `02_sql_queries_tutorial.ipynb`

## Dependencies
- Python 3, DuckDB, pandas, matplotlib, seaborn

## Plotting
All plot functions live in `util_plot.py`. Available: `plot_bar`, `plot_grouped_bar`, `plot_pie`, `plot_scatter`, `plot_histogram`, `plot_boxplot`, `plot_heatmap`, `plot_lollipop`, `plot_line`, `plot_multi_line`, `plot_stacked_bar`, `highlight_duplicates`.
