# 🪄 CRUD with `%%dql` Cell Magic

**OMIS-105 · Week 3 — SQL Basics**

The same ten-employee CRUD story as `CRUD_100_10_rows/`, written with the
**`magic-duckdb`** extension so that SQL is typed directly into a cell instead of
being wrapped in Python.

---

## Run it

```bash
pip install magic-duckdb
marimo edit CRUD_employees_duckdb_marimo.py
```

| File | Role |
|---|---|
| `CRUD_employees_duckdb_marimo.py` | The notebook |
| `display_utils.py` | Display helpers |
| `data/employees.csv` | 10 employees |

---

## What the magic does

Without it, every query is a Python call:

```python
con.execute("SELECT * FROM employees WHERE salary > 60000").df()
```

With it, the cell *is* SQL:

```sql
%%dql
SELECT * FROM employees WHERE salary > 60000
```

`%%dql` is a **cell magic**: a marker on the first line that says "treat everything
below as SQL, not Python". The database, the query and the result are identical —
only the typing changes.

**Why it matters for teaching:** it removes the Python scaffolding from the screen,
so a student reading the cell sees SQL and nothing else.

**Why it might not suit you:** it is an extra dependency, and it hides how the
query actually reaches the database. If your course wants students to understand the
connection object, the plain version is the better choice.

---

## What it covers

| § | Section | Operations |
|---|---|---|
| 0 | Environment setup | Install and load the extension |
| 2A | **CREATE** | 4 `INSERT` examples |
| 2B | **READ** | 4 `SELECT` examples |
| 2C | **UPDATE** | 4 `UPDATE` examples |
| 2D | **DELETE** | 4 `DELETE` examples |

Four worked examples per operation — more repetition per concept than the other CRUD
stories, which makes this a good choice if students need the drill.

---

## Choosing among the six CRUD stories

They all teach the same four operations. The differences:

| Story | Rows | What makes it different |
|---|---|---|
| `CRUD_100_10_rows/` | 10 | The plainest version. **Start here.** |
| `CRUD_100_10_rows_with_dql/` | 10 | Same content using `%%dql` cell magic |
| `CRUD_100_10_rows_with_images/` | 10 | Adds employee photos to result tables |
| `CRUD_9_emps_intro/` | 9 | Longest conceptual intro — "what is DuckDB", "what is CRUD" |
| `CRUD_10_emps_staging/` | 10 | Helper-module variant |
| `CRUD_10_emps_persistent/` | 10 | Uses a **persistent** database and a backup table |
| `emps_single_table/` | **1,100** | Real-size table; adds a "did the changes stick?" check |

> **Note:** these folders were renamed in 2026 to say what they actually contain.
> They were previously `CRUD_100_emps`, `CRUD_101_emps`, `CRUD_102_emps` and
> `CRUD_100_10_rows_with_images_openai` — names whose numbers were not row counts and
> which promised an AI integration that does not exist.

**Assign one.** They are variations on a theme, and doing several is repetition
without new material.
