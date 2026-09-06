# SQL JOIN Operations

Two Marimo notebooks that teach SQL's `JOIN` operations (`INNER`,
`LEFT`, `RIGHT`, `FULL OUTER`, and more) against a realistic employee
dataset, with display/plot code kept out of the notebooks and in
`display_tables.py` / `plots.py`.

| Notebook | Cells | Dataset |
|---|---|---|
| [`Join_Operations_Tutorial_1_Employees.py`](Join_Operations_Tutorial_1_Employees.py) | 20 hands-on exercises | `data/employees.csv` (3,060 rows), `data/departments.csv` (7 depts — 5 active + 2 unused), `data/countries.csv` (10 countries) |
| [`Join_Operations_Tutorial_2.py`](Join_Operations_Tutorial_2.py) | Comprehensive, basic → intermediate+ | Same three tables, built up from scratch inside the notebook |

Both notebooks follow the same three-part pattern per example: a
natural-language question, the DuckDB SQL that answers it, and a
styled result table (plus a chart where meaningful).

**Dataset design notes:** `employees.dept_id` includes 10 rows set to
`"TOP-SECRET"`, a department that doesn't exist in `departments` — a
deliberate case for exploring unmatched rows in `LEFT`/`RIGHT` joins.
Country and salary distributions are intentionally unbalanced (e.g.
USA/China/India are the largest groups) so `GROUP BY` and join results
look like real-world data rather than a perfectly even toy dataset.

Run either notebook with:

```bash
pip install marimo duckdb pandas matplotlib
marimo edit Join_Operations_Tutorial_1_Employees.py
# or
marimo edit Join_Operations_Tutorial_2.py
```

Run from inside this folder so the relative `data/*.csv` paths resolve.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
