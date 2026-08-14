# 💾 CRUD of Employees Data — Persistent Database

**OMIS-105 · Week 3 — SQL Basics**

The ten-employee CRUD story, with two features the others do not have: it writes to a
**persistent database file**, and it makes a **backup table** before changing
anything.

---

## Run it

```bash
pip install -r requirements.txt
marimo edit CRUD_10_emps_persistent_marimo.py
```

| File | Role |
|---|---|
| `CRUD_10_emps_persistent_marimo.py` | The notebook |
| `helpers/crud_display.py` | Display helpers |
| `data/employees.csv` | 10 employees |
| `employees_crud.duckdb` | **The persistent database** — survives between runs |
| `requirements.txt` | Dependencies |

---

## What it covers

| Cell | Step |
|---|---|
| 1 | Project setup |
| 2 | Create the CSV data file |
| 3 | Connect to DuckDB, create the `employees` table |
| 4 | Quick validation checks |
| C1 | **Create a backup table** |
| C2 | Insert one new employee |
| C3 | Insert multiple new employees |
| … | Update and delete operations |

---

## The two things that make this one different

**It persists.** The database is a real file, so data is still there when you come
back. Run the notebook, close everything, reopen it — the rows survive. Compare that
with `CRUD_100_10_rows/`, which starts empty every time.

That difference is the whole subject of `duckdb_magic_notebooks/` (Week 1), and it is
what Week 8's durability section makes rigorous.

**It takes a backup first (C1).** Before any destructive operation, the notebook
copies the table:

```sql
CREATE TABLE employees_backup AS SELECT * FROM employees;
```

This is a real professional habit, and it is cheap to teach here. It also gives
students a way to recover from a `DELETE` with no `WHERE` clause — which somebody
will do.

> ⚠️ Because the database persists, **re-running the notebook may not start from a
> clean slate.** If results look strange on a second run, delete
> `employees_crud.duckdb` and start over.

---

## Choosing among the CRUD stories

They all teach the same four operations. The differences:

| Story | Rows | What makes it different |
|---|---|---|
| `CRUD_100_10_rows/` | 10 | The plainest version. **Start here.** |
| `CRUD_100_10_rows_drill/` | 10 | **4 examples per operation** — most repetition |
| `CRUD_100_10_rows_with_images/` | 10 | Adds employee photos to result tables |
| `CRUD_9_emps_intro/` | 9 | Longest conceptual intro — "what is DuckDB", "what is CRUD" |
| `CRUD_10_emps_staging/` | 10 | Helper-module variant |
| `CRUD_10_emps_persistent/` | 10 | Uses a **persistent** database and a backup table |
| `emps_single_table/` | **1,100** | Real-size table; adds a "did the changes stick?" check |

> **Note:** several of these folders were renamed in 2026 to say what they actually
> contain. They were previously `CRUD_100_emps`, `CRUD_101_emps`, `CRUD_102_emps` and
> `CRUD_100_10_rows_with_images_openai` — names whose numbers were not row counts, or
> that promised an AI integration which does not exist.

**Assign one.** They are variations on a theme, and doing several is repetition
without new material.
