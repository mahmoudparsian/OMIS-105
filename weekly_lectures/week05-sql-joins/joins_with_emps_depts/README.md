# Employees / Departments — Your First Joins

A tiny two-table DuckDB database for a first look at SQL joins:
`INNER`, `LEFT`, `RIGHT`, `FULL OUTER`, and `CROSS JOIN`, with some
aggregation first. The tables have only 4 and 6 rows, so you can
check every answer by eye.

## The Story

A small company has 4 departments and 6 employees. Most employees
belong to a department, but not everything connects:

- **2 departments have no employees:** Sales (30) and Finance (40).
- **2 employees have no department:** Diana and Jane. Their
  `dept_id` is `NULL`.

There are gaps on **both** sides. Because of these gaps, each join
type returns a different number of rows, and
`LEFT JOIN ... IS NULL` finds what is missing.

## File Structure

```
joins_with_emps_depts/
├── README.md                    # this file
├── db_schema_and_records.sql    # CREATE TABLE + INSERT (departments, employees)
├── how_to_create_database.txt   # a sample DuckDB CLI session: build the file, then look at it
├── emps_depts_db.duckdb         # the built database (committed, ready to use)
├── notebook.py                  # Marimo notebook: 21 SQL queries + 6 charts
└── plot_helpers.py              # matplotlib helpers used by notebook.py
```

## Tables

| Table | Rows | Columns | What it holds |
|-------|-----:|---------|----------------|
| `departments` | 4 | `dept_id`, `dept_name` | Engineering (10), Marketing (20), Sales (30), Finance (40) |
| `employees`   | 6 | `emp_id`, `emp_name`, `salary`, `dept_id` | Alice, Bob, Rafa, Charlie, Diana, Jane; salaries 65,000–82,000 |

```
departments (dept_id, dept_name)
     ▲
     │ employees.dept_id → departments.dept_id
     │
employees (emp_id, emp_name, salary, dept_id)
```

`employees.dept_id` is a `FOREIGN KEY`. Every non-`NULL` value must
exist in `departments`. A `NULL` is still allowed, which is why
Diana and Jane can have no department.

## Usage

**Step 1 — the database file.** `emps_depts_db.duckdb` is already
in this folder, so you can skip this step. To rebuild it from the
SQL file, delete it and run:

```bash
cd joins_with_emps_depts
rm emps_depts_db.duckdb
duckdb emps_depts_db.duckdb < db_schema_and_records.sql
```

This needs the [DuckDB CLI](https://duckdb.org/docs/installation/)
on your `PATH`. `how_to_create_database.txt` shows what the session
looks like.

**Step 2a — Notebook:**

```bash
marimo edit notebook.py
```

The notebook opens the database **read-only**: you can run any
`SELECT`, but nothing can change the data. Every query cell is a
native SQL cell, so you see only the SQL. If the `.duckdb` file is
missing, the notebook stops and tells you how to build it.

**Step 2b — DuckDB CLI or qStudio:**

```bash
duckdb -readonly emps_depts_db.duckdb    # then paste any query
```

`notebook.py` needs `marimo`, `duckdb`, `polars` (or `pandas`), and
`matplotlib`.
See the
[software installation guide](../../../software_installation/README.md).

## The 21 Notebook Queries

| Part | Queries | Focus |
|------|---------|-------|
| 1. Meet the data | V1–V2 | One `SELECT` per table |
| 2. Aggregation | A1–A4 | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`; `GROUP BY`; A3 runs the query without `HAVING` first, then with it; `COUNT(*)` vs `COUNT(column)` |
| 3. `INNER JOIN` | J1–J3 | Join; join + `WHERE`; join + `GROUP BY` |
| 4. `LEFT JOIN` | J4–J6 | Both directions; headcount per department with zeros |
| 5. `RIGHT JOIN` | J7–J8 | `A RIGHT JOIN B` = `B LEFT JOIN A`; `COALESCE` |
| 6. `FULL OUTER JOIN` | J9 | Every row from both tables |
| 7. `CROSS JOIN` | J10 | Every pair of rows (no `ON`) |
| 8. Finding the gaps | X1–X3 | Departments with no employees; employees with no department; both in one `FULL JOIN` |
| 9. Summary | S1 | Row counts of every join type, side by side |

The notebook ends with a cheat sheet and five "Try It Yourself"
exercises.

### The 6 charts

The plotting code lives in `plot_helpers.py`, so the notebook cells
stay pure SQL.

| Query | Chart | What it shows |
|-------|-------|----------------|
| A2 | pie | Employees per `dept_id`; the orange `NULL` slice shows that one third of the company has no department |
| A3 | bar + threshold line | Average salary per `dept_id`; the dashed line is the `HAVING` test, so you see which groups are kept and which are dropped |
| J6 | bar | Employees per department; Sales and Finance show as dashed "0 — none" bars, kept by the `LEFT JOIN` |
| J8 | horizontal bar | Every employee's salary, colored by department; Diana and Jane stand out as "(no department)" |
| J9 | join map | The `FULL OUTER JOIN` as a picture: a line for each match, unmatched employees and departments in orange |
| S1 | horizontal bar | Row count of each join type, side by side |

### Row counts to watch

| Join | Rows |
|------|-----:|
| `employees INNER JOIN departments` | 4 |
| `employees LEFT JOIN departments`  | 6 |
| `departments LEFT JOIN employees`  | 6 |
| `employees RIGHT JOIN departments` | 6 |
| `employees FULL OUTER JOIN departments` | 8 |
| `employees CROSS JOIN departments` | 24 |

The two `LEFT JOIN`s both return 6 rows, but **different** rows:
the first adds Diana and Jane, the second adds Sales and Finance.
`FULL OUTER JOIN` adds all four. `CROSS JOIN` is 6 × 4.

## Next Steps

When these joins feel easy, try the larger databases in this week's
folder:
[`joins_with_authors_books_orders/`](../joins_with_authors_books_orders/)
and
[`joins_with_students_and_courses/`](../joins_with_students_and_courses/).

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
