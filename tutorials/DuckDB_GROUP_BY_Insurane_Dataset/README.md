# Mastering SQL GROUP BY with DuckDB — Insurance Dataset

A 20-cell Marimo notebook that teaches SQL `GROUP BY` end to end —
from a single-column count all the way to `ROLLUP` and window
functions — using a real 1,800-row health insurance dataset. Every
query renders as a styled table and a matching dark-themed chart.

## Files

| File | What it is |
|---|---|
| `insurance_group_by.py` | The Marimo notebook (all 20 lessons) |
| `insurance.csv` | The dataset — 1,800 rows |
| `plots_util.py` | Shared plotting + table-styling helpers (don't edit — just import) |

**Dataset columns:**

| Column | Type | Description |
|---|---|---|
| `age` | integer | Age of the insured |
| `gender` | string | `male` / `female` |
| `bmi` | float | Body Mass Index |
| `num_children` | integer | Number of dependents |
| `smoker` | string | `yes` / `no` |
| `region` | string | US region (`northeast`, `northwest`, `southeast`, `southwest`) |
| `charges` | float | Insurance charges billed ($) |

## Requirements

```bash
pip install duckdb marimo pandas matplotlib
```

## How to Run

Open a terminal in this folder (all three files must stay together)
and run:

```bash
marimo edit insurance_group_by.py
```

This opens the notebook in your browser. Run the cells top to bottom —
each one builds on the last.

## What's Inside

| # | Cell | What It Teaches |
|---|------|-----------------|
| — | Setup | Loads `insurance.csv` into a DuckDB table and applies the dark chart theme |
| 1 | Basic Statistics | Summary stats for the whole table — no `GROUP BY` yet, for comparison |
| 2 | GROUP BY One Column | Policy count and avg charge by `gender` |
| 3 | GROUP BY One Column | Avg/min/max charges by `smoker` status |
| 4 | GROUP BY One Column | Policies and total charges by `region` |
| 5 | GROUP BY One Column | Avg vs. median charges by `num_children` |
| 6 | GROUP BY with CASE | Bucket `age` into life-stage groups, then group by the bucket |
| 7 | GROUP BY Two Columns | `region` × `gender` |
| 8 | GROUP BY Two Columns | `smoker` × `gender` — is the smoking penalty the same for both? |
| 9 | GROUP BY Two Columns | `region` × `smoker` |
| 10 | GROUP BY Two Columns | `age_group` × `smoker` — does the smoking penalty grow with age? |
| 11 | GROUP BY + HAVING | Keep only groups whose average charge exceeds $14,000 |
| 12 | GROUP BY Two Columns | WHO BMI category × `smoker` |
| 13 | GROUP BY Two Columns | `num_children` × `smoker` |
| 14 | GROUP BY + ORDER BY + LIMIT | Top 5 most expensive region/smoker/gender combinations |
| 15 | GROUP BY + COUNT DISTINCT | Unique ages per region |
| 16 | GROUP BY Two Columns | `region` × `num_children` |
| 17 | Multiple Aggregates | Full per-region financial snapshot: count, sum, mean, median, stddev, min, max |
| 18 | GROUP BY ROLLUP | Automatic subtotal and grand-total rows |
| 19 | GROUP BY + Window Function | `RANK() OVER (PARTITION BY ...)` on top of a grouped CTE |
| 20 | Grand Finale | Three grouping columns, six aggregates, `HAVING`, and `RANK()` combined in one query |

## Key Takeaways

- `GROUP BY` collapses many rows into one row per unique group value.
- Every column in `SELECT` must be in `GROUP BY` or inside an aggregate function.
- `HAVING` filters groups *after* aggregation — `WHERE` filters rows *before*.
- `ROLLUP` adds automatic subtotal / grand-total rows.
- Window functions (`RANK`, `ROW_NUMBER`) operate on top of grouped results.
