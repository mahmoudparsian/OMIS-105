# Mastering SQL Sub-Queries with WITH (CTEs)

A beginner-friendly, 12-cell Marimo notebook that teaches Common Table
Expressions (CTEs) — the `WITH` clause — from first principles up to
ranking functions, using a single 20-row `employees` table. Every
query result renders as a styled HTML table via a small built-in
`show()` helper.

## Files

| File | What it is |
|---|---|
| `subqueries_with_duckdb.py` | The Marimo notebook (all 12 cells). Creates its own `employees` table and `show()` rendering helper — no data files needed. |

**Dataset (`employees`, 20 rows):**

| Column | Description |
|---|---|
| `emp_id` | Unique employee ID |
| `name` | Employee name |
| `department` | Department they belong to |
| `job_title` | Their role |
| `salary` | Annual salary (USD) |
| `years_exp` | Years of experience |
| `hire_year` | Year they were hired |
| `rating` | Annual performance rating (1–5) |

## Requirements

```bash
pip install duckdb marimo pandas ipython
```

## How to Run

Open a terminal in this folder and run:

```bash
marimo edit subqueries_with_duckdb.py
```

This opens the notebook in your browser. Run the cells top to bottom —
each one builds on the last.

## What's Inside

| Cell | Pattern | Key Idea |
|------|---------|----------|
| 1 | Setup | Loads DuckDB and defines the `show()` rendering helper (reused everywhere) |
| 2 | Dataset | Creates the 20-row `employees` table |
| 3 | Lesson 1 — Why `WITH`? | Compares a messy nested sub-query to the same logic named with `WITH` |
| 4 | Lesson 2 — Basic `WITH` | Filter rows inside a CTE, then filter again in the main query |
| 5 | Lesson 3 — Aggregate in CTE | Push `GROUP BY` into the CTE; the outer query just selects from it |
| 6 | Lesson 4 — Two CTEs | Chain two CTEs with a comma; the second can reference the first |
| 7 | Lesson 5 — JOIN CTE to base | Compute a summary in a CTE, then `JOIN` it back to the detail rows |
| 8 | Lesson 6 — Three CTEs | Build a step-by-step pipeline: max salary → top earners → elite filter |
| 9 | Lesson 7 — Derive + aggregate | Create a column (salary band) in a CTE, then `GROUP BY` it |
| 10 | Lesson 8 — Ranking functions | `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()` compared side by side |
| 11 | Lesson 9 — Filter by rank | The golden pattern: rank inside a CTE, then `WHERE rank = 1` outside — impossible in a single query |
| 12 | Grand Finale | Three CTEs, salary bands, department ranking, and a company-average filter, all combined |

## Key Takeaways

- **CTE** = Common Table Expression. `WITH name AS (...)` gives a
  temporary result set a nickname you can reference later in the
  same query.
- A CTE can reference any CTE defined before it — chain them with commas
  to build a query pipeline.
- Push `GROUP BY` or derived columns (`CASE`) into a CTE, then keep the
  outer query simple.
- Window functions (`RANK()`, `DENSE_RANK()`, `ROW_NUMBER()`) can't be
  used directly in `WHERE` — compute them in a CTE, then filter on the
  result in the outer query.

**Next steps:** try `WITH RECURSIVE` for hierarchical data, or explore
`NTILE()`, `PERCENT_RANK()`, and `LAG()` / `LEAD()`.
