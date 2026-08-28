# SQL Tutorial Notebooks

Three self-contained Marimo notebooks that teach SQL with DuckDB, from
a first tour of `SELECT` through joins, CTEs, and window functions.
Every table is built in-notebook with `CREATE TABLE`/`INSERT` — no
external CSV files are needed. Each SQL example follows the same
three-part pattern: a natural-language question, the DuckDB SQL that
answers it, and a rendered result table.

Pick the notebook that matches how much ground you want to cover:

| Notebook | Scope | Table(s) |
|---|---|---|
| `sql_tutorial_01_quick_tour.py` | Quick tour (10 short sections) — SELECT, WHERE, ORDER BY, aggregates, GROUP BY/HAVING, a JOIN, an intro window function, CASE, a subquery, and set operations | 12-row `sales` table |
| `sql_tutorial_02_fundamentals.py` | Deep single-table fundamentals (28 lessons) — every SELECT/WHERE/ORDER BY/LIMIT variant, DISTINCT, BETWEEN, IN, LIKE, aliases, aggregates, GROUP BY/HAVING, CASE, subqueries, a correlated subquery, and date functions | `employees` table |
| `sql_tutorial_03_comprehensive.py` | Comprehensive master guide (47 lessons) — everything above, plus a second table with every join type, self-joins, CTEs (including chained CTEs), views, set operations, the full window-function suite (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`/`LEAD`, running totals, `NTILE`, `PERCENT_RANK`/`CUME_DIST`), `QUALIFY`, and `PIVOT` | `employees` + `departments` tables |

Suggested order: `01` for a fast overview, `02` to go deep on
single-table fundamentals, then `03` as the capstone that adds joins,
CTEs, views, and window functions.

## Requirements

```bash
pip install marimo duckdb pandas
```

## How to run

```bash
marimo edit sql_tutorial_01_quick_tour.py
# or
marimo edit sql_tutorial_02_fundamentals.py
# or
marimo edit sql_tutorial_03_comprehensive.py
```

Run cells in order — later cells depend on tables created earlier in
the same notebook.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
