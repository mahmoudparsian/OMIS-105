# 👥 Employees — CRUD on a Real-Size Table

**OMIS-105 · Week 3 — SQL Basics**

The same four CRUD operations as the `CRUD_*` stories, but on **1,100 employees**
instead of ten — a table too big to check by eye. That changes how you have to work,
which is the point.

---

## Run it

```bash
marimo edit employees_duckdb_marimo.py    # data exploration
marimo edit emps_CRUD_marimo.py           # the CRUD walkthrough
```

| File | Role |
|---|---|
| `emps_CRUD_marimo.py` | The CRUD notebook — 7 sections |
| `employees_duckdb_marimo.py` | Exploration of the same table |
| `generate_data.py` | Regenerates the dataset |
| `utils/` | Display helpers |
| `data/employees.csv` | **1,100 employees** |

---

## The data

One table, ten columns:

```
employees(emp_id, emp_name, department, salary, gender,
          degree, hire_date, country, image_url, age)
```

Richer than the ten-row CRUD tables — enough columns to make `WHERE` clauses
interesting and enough rows that `GROUP BY` gives a real answer.

---

## What it covers

| § | Section |
|---|---|
| 1 | Environment setup |
| 2 | Load the employees table |
| 3 | **INSERT** — adding new rows |
| 4 | **UPDATE** — modifying existing rows |
| 5 | **DELETE** — removing rows |
| 6 | **Post-CRUD checkpoint: did our changes stick?** |
| 7 | Key takeaways |

---

## Why §6 is the important one

On ten rows you verify an `UPDATE` by looking at the table. On 1,100 you cannot — so
you have to **ask a question whose answer you already know**:

```sql
-- I updated one salary. Did exactly one row change?
SELECT COUNT(*) FROM employees WHERE salary = 95000;
```

That shift is the real Week 3 skill:

- On ten rows you **look** at the result.
- On 1,100 rows you **verify it with another query**.
- Every table students meet after this course will be too big to eyeball, so the
  second habit is the one that lasts.

---

## How it compares

| Story | Rows | Use it for |
|---|---|---|
| `CRUD_100_10_rows/` | 10 | First contact with CRUD — check results by eye |
| **`emps_single_table/`** | **1,100** | The same operations when eyeballing is impossible |

A good sequence is both, in that order: learn the statements on ten rows, then learn
to *trust* them on 1,100.

---

## Teaching notes

- Have students predict the row count **before** running each `UPDATE` or `DELETE`,
  then check. A mismatch is the entire lesson.
- `generate_data.py` means you can hand different students different data, which makes
  copied answers obvious.
- The `country` and `department` columns make this usable again in Week 4 for
  `GROUP BY` practice, on data students already know.
