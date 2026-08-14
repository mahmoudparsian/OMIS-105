# 📘 CRUD of Employees Data — the Long Version

**OMIS-105 · Week 3 — SQL Basics**

The most **explanatory** of the CRUD stories. Before touching a single statement it
answers "what is DuckDB?" and "what is CRUD?", then lays out a road-map of where the
notebook is going.

Choose this one when students have never met a database at all.

---

## Run it

```bash
marimo edit CRUD_Employees_DuckDB_marimo.py
```

| File | Role |
|---|---|
| `CRUD_Employees_DuckDB_marimo.py` | The notebook |
| `notebook_utils.py` | Display helpers |
| `employees.csv`, `data/employees.csv` | 9 employees (two copies of the same file) |
| `files.zip` | Archived copy of the materials |

---

## What it covers

| § | Section |
|---|---|
| — | What is DuckDB? |
| — | What is CRUD? |
| — | Notebook road-map |
| 0 | Setup & imports |
| 1 | **CREATE** — building the employees table |
| 2 | **READ** — querying the data |
| 3 | **UPDATE** — modifying existing rows |
| 4 | **DELETE** — removing rows |

---

## Two things to know before assigning it

**Nine employees, not a hundred.** This folder used to be called `CRUD_100_emps`,
which led people to expect 100 rows. It was renamed to say what it holds. Nine rows is
genuinely fine for the material.

**`employees.csv` exists twice**, at the top level and in `data/`. They are identical.
Check which path the notebook reads before editing either.

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
