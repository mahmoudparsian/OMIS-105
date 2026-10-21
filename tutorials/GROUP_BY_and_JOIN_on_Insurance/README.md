# Mastering GROUP BY and INNER JOIN 
# Dataset: Insurance 

A 25-lesson Marimo notebook that teaches SQL `GROUP BY` end to end —
from a single-column count all the way to `ROLLUP` and window
functions — using a real 1,800-row health insurance dataset. A second,
small table, `regions`, holds the full region names. Cell 4b gives a
first look at joining the two tables, and Part 2 (Cells 21–25) teaches
`INNER JOIN` + `GROUP BY` step by step. Every query renders as a styled
table, and most have a matching dark-themed chart.

## Files

| File | What it is |
|---|---|
| `insurance_notebook.py` | The Marimo notebook (all 25 lessons, plus Cell 4b) |
| `insurance.csv` | The insurance policies — 1,800 rows |
| `regions.csv` | The sales regions — 6 rows |
| `plots_util.py` | Shared plotting + table-styling helpers (don't edit — just import) |

**`insurance.csv` columns:**

| Column | Type | Description |
|---|---|---|
| `age` | integer | Age of the insured |
| `gender` | string | `male` / `female` |
| `bmi` | float | Body Mass Index |
| `num_children` | integer | Number of dependents |
| `smoker` | string | `yes` / `no` |
| `region_id` | string | Region code (`ne`, `nw`, `se`, `sw`) — links to `regions.csv` |
| `charges` | float | Insurance charges billed ($) |

**`regions.csv` columns:**

| Column | Type | Description |
|---|---|---|
| `region_id` | string | Region code — the key that `insurance.region_id` points to |
| `region_name` | string | Full name, e.g. `South-West` |
| `region_manager` | string | The person who runs the region |
| `region_head_quarter` | string | The city where the region's office is |

**`regions.csv` data:**

| region_id | region_name | region_manager | region_head_quarter |
|---|---|---|---|
| `sw` | South-West | Adam Smith | Los Angeles |
| `nw` | North-West | Roger Grogu | Portland |
| `se` | South-East | Rafa Gomez | West Palm Beach |
| `ne` | North-East | Alex Pope | New York |
| `mw` | Mid-West | Jane Eastwood | Chicago |
| `ma` | Mid-Atlantic |Betty Woodward | Pittsburgh|


Mid-West (`mw`) and Mid-Atlantic (`ma`) have **no policies** 
in `insurance.csv`. This is on purpose: it shows that an 
`INNER JOIN` drops rows that have no match.

In Part 1, results show the short region code (`se`, `sw`, …). 
To see the full region name, a query must join `insurance` table
with `regions` table — that is what Cell 4b and Part 2 do.

## Requirements

```bash
pip install duckdb marimo pandas matplotlib
```

## How to Run

Open a terminal in this folder (all four files must stay together)
and run:

```bash
marimo edit insurance_notebook.py
```

This opens the notebook in your browser. Run the cells top to bottom —
each one builds on the last.

## What's Inside

| # | Cell | What It Teaches |
|---|------|-----------------|
| — | Setup | Loads `insurance.csv` and `regions.csv` into two DuckDB tables and applies the dark chart theme |
| | **Part 1 — GROUP BY** | |
| 1 | Basic Statistics | Summary stats for the whole table — no `GROUP BY` yet, for comparison |
| 2 | GROUP BY One Column | Policy count and avg charge by `gender` |
| 3 | GROUP BY One Column | Avg/min/max charges by `smoker` status |
| 4 | GROUP BY One Column | Policies and total charges by `region_id` |
| 4b | GROUP BY + INNER JOIN | Cell 4 again, but joined with `regions` to show `region_name` instead of the code |
| 5 | GROUP BY One Column | Avg vs. median charges by `num_children` |
| 6 | GROUP BY with CASE | Bucket `age` into life-stage groups, then group by the bucket |
| 7 | GROUP BY Two Columns | `region_id` × `gender` |
| 8 | GROUP BY Two Columns | `smoker` × `gender` — is the smoking penalty the same for both? |
| 9 | GROUP BY Two Columns | `region_id` × `smoker` |
| 10 | GROUP BY Two Columns | `age_group` × `smoker` — does the smoking penalty grow with age? |
| 11 | GROUP BY + HAVING | Keep only groups whose average charge exceeds $14,000 |
| 12 | GROUP BY Two Columns | WHO BMI category × `smoker` |
| 13 | GROUP BY Two Columns | `num_children` × `smoker` |
| 14 | GROUP BY + ORDER BY + LIMIT | Top 5 most expensive region/smoker/gender combinations |
| 15 | GROUP BY + COUNT DISTINCT | Unique ages per region |
| 16 | GROUP BY Two Columns | `region_id` × `num_children` |
| 17 | Multiple Aggregates | Full per-region financial snapshot: count, sum, mean, median, stddev, min, max |
| 18 | GROUP BY ROLLUP | Automatic subtotal and grand-total rows |
| 19 | GROUP BY + Window Function | `RANK() OVER (PARTITION BY ...)` on top of a grouped CTE |
| 20 | Grand Finale | Three grouping columns, six aggregates, `HAVING`, and `RANK()` combined in one query |
| | **Part 2 — INNER JOIN** | |
| 21 | First INNER JOIN | Look at `regions`, then attach region name and manager to each policy with `INNER JOIN ... ON` |
| 22 | INNER JOIN + GROUP BY | Policies and total charges by `region_name` — and why Mid-West disappears |
| 23 | INNER JOIN + GROUP BY Two Columns | Manager scorecard: policies, smoker share, and charges by `region_manager` × `region_head_quarter` |
| 24 | INNER JOIN + WHERE + GROUP BY + HAVING | Smoker groups (`region_name` × `gender`) with average charge above $32,000 |
| 25 | Group First, Then Join | A CTE groups `insurance` by `region_id`, then `INNER JOIN` adds the names |

## Key Takeaways

- `GROUP BY` collapses many rows into one row per unique group value.
- Every column in `SELECT` must be in `GROUP BY` or inside an aggregate function.
- `HAVING` filters groups *after* aggregation — `WHERE` filters rows *before*.
- `ROLLUP` adds automatic subtotal / grand-total rows.
- Window functions (`RANK`, `ROW_NUMBER`) operate on top of grouped results.
- `INNER JOIN ... ON` combines two tables where the key values match.
- `INNER JOIN` keeps only matching rows — a region with no policies (Mid-West) is dropped.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
