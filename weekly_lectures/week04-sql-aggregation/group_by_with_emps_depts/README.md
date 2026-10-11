# Employees / Departments — Learning `GROUP BY`

A complete, step-by-step tutorial on `GROUP BY`, built on a small
two-table DuckDB database. It starts with whole-table statistics and
ends with pivot tables, joins, and "find what is missing". Use it as
your reference whenever you need to group data.

## The Story

A small company has 5 departments and 13 employees. Each employee
has a `job_title` and a `salary`, and belongs to one department.

- **Two good columns to group on:** `dept_id` (3 values are used:
  10, 20, 30) and `job_title` (4 values: Engineer, Marketer,
  Salesperson, VP).
- **Two departments have no employees:** Finance (40) and IT (50).
  `GROUP BY` on `employees` never sees them. A `LEFT JOIN` finds them.

## File Structure

```
group_by_with_emps_depts/
├── README.md                           # this file
├── db_schema_and_records.sql           # CREATE TABLE + INSERT (departments, employees)
├── how_to_create_duckdb_database.txt   # a sample DuckDB CLI session: build the file, then look at it
├── emps_depts_db.duckdb                # the built database (committed, ready to use)
├── notebook.py                         # Marimo notebook: 18 SQL queries + 11 charts
└── plot_helpers.py                     # matplotlib helpers used by notebook.py
```

## Tables

| Table | Rows | Columns | What it holds |
|-------|-----:|---------|----------------|
| `departments` | 5 | `dept_id`, `dept_name` | Engineering (10), Marketing (20), Sales (30), Finance (40), IT (50) |
| `employees`   | 13 | `emp_id`, `emp_name`, `job_title`, `salary`, `dept_id` | salaries 70,000–180,000 |

```
departments (dept_id, dept_name)
     ▲
     │ employees.dept_id → departments.dept_id
     │
employees (emp_id, emp_name, job_title, salary, dept_id)
```

## Usage

**Step 1 — the database file.** `emps_depts_db.duckdb` is already
in this folder, so you can skip this step. To rebuild it from the
SQL file, delete it and run:

```bash
cd group_by_with_emps_depts
rm emps_depts_db.duckdb
duckdb emps_depts_db.duckdb < db_schema_and_records.sql
```

This needs the [DuckDB CLI](https://duckdb.org/docs/installation/)
on your `PATH`. `how_to_create_duckdb_database.txt` shows what the
session looks like.

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
`matplotlib`. See the
[software installation guide](../../../software_installation/README.md).

## The 18 Notebook Queries

| Part | Queries | Focus |
|------|---------|-------|
| 1. Meet the data | B1–B4 | Both tables; `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` for the whole table; sorting to "see" the groups |
| 2. `GROUP BY` | G1–G8 | Basic → advanced (below) |
| 3. Joins + `GROUP BY` | J1–J4 | `INNER JOIN`; join + `WHERE`; join + `GROUP BY` by name; `LEFT JOIN` + `COUNT(e.emp_id)` vs. `COUNT(*)` |
| 4. Finding the gap | X1 | Departments with no employees (`LEFT JOIN … IS NULL`, and the `HAVING COUNT(…) = 0` alternative) |

The eight `GROUP BY` queries:

| Query | Level | Teaches |
|-------|-------|---------|
| G1 | basic | `COUNT(*)` per `dept_id` |
| G2 | basic | `COUNT(*)` per `job_title` |
| G3 | basic → intermediate | many aggregates over the same groups |
| G4 | intermediate | `SUM` per `job_title` and its percent of the total (a subquery) |
| G5 | intermediate | `WHERE` + `GROUP BY`: rows are filtered **before** grouping |
| G6 | intermediate | `HAVING`: groups are filtered **after** grouping (run without, then with) |
| G7 | advanced | `GROUP BY` two columns |
| G8 | advanced | conditional aggregation: a pivot table with `SUM(CASE WHEN …)` |

Most queries use **`GROUP_CONCAT`** (also known as `STRING_AGG`) to
list the rows inside each group, so you can see what `COUNT`, `SUM`,
`MIN`, and `MAX` are working on. G4 glues salaries together with
`' + '`, so the column shows the exact sum SQL computes.

The notebook also runs a broken query (a column that is neither
grouped nor aggregated) and shows DuckDB's real error message. It
ends with a cheat sheet and six "Try It Yourself" exercises with
hidden solutions.

### The 11 charts

The plotting code lives in `plot_helpers.py`, so the notebook cells
stay pure SQL. Colors follow the entity: dept 10 and Engineer are
always blue, and so on.

| Query | Chart | What it shows |
|-------|-------|----------------|
| B4 | group map | 13 employee rows, each with a line to its `dept_id` group: "many rows in, one row per group out" |
| G1 | donut | Employees per department |
| G2 | donut | Employees per job title |
| G3 | range | `MIN`, `AVG`, and `MAX` salary per department in one picture |
| G4 | donut | Share of payroll per job title; compare with G2 (VPs are 23% of people, 35% of payroll) |
| G5 | paired bars | All employees vs. those kept by `WHERE`, per department |
| G6 | bars + threshold line | Average salary per job title; the `HAVING` test keeps or drops each group |
| G7 | stacked bars | Job titles inside each department |
| G8 | heatmap | The pivot table: payroll by department × job title |
| J3 | horizontal bars | Average salary per department name, with the company average |
| J4 | bars | Employees in every department; Finance and IT show as "0 — none" |

### Row counts to watch

| Query | Rows |
|-------|-----:|
| B3 — no `GROUP BY` | 1 |
| G1 — `GROUP BY dept_id` | 3 |
| G2 — `GROUP BY job_title` | 4 |
| G6 — `HAVING AVG(salary) > 100000` | 2 |
| G7 — `GROUP BY dept_id, job_title` | 7 |
| J3 — `INNER JOIN` + `GROUP BY` | 3 |
| J4 — `LEFT JOIN` + `GROUP BY` | 5 |
| X1 — departments with no employees | 2 |

## Next Steps

In Week 5, the same kind of data comes back in
[`joins_with_emps_depts/`](../../week05-sql-joins/joins_with_emps_depts/),
which focuses on every join type.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
