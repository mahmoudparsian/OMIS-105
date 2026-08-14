# 🔁 CRUD with Four Examples per Operation

**OMIS-105 · Week 3 — SQL Basics**

The same ten-employee CRUD story as `CRUD_100_10_rows/`, but with **four worked
examples of each operation** instead of one or two. Choose it when students need
repetition rather than novelty.

---

## ⚠️ The folder name is out of date

The name says `dql`, and the notebook's own text talks about the **`%%dql` cell
magic** from the `magic-duckdb` extension. **That is no longer how it works.**

- The notebook was converted from Jupyter to **Marimo**.
- `%%dql` is an **IPython cell magic** — Marimo cannot run it.
- There are **zero `%%dql` cells** left in the file.
- Every query now runs through Marimo's native `mo.sql()`, exactly like the other
  stories here.

Three leftovers from the old version are still in the notebook and should be cleaned
up:

| Leftover | Where | Effect |
|---|---|---|
| Markdown explaining `%%dql` | §"Using magic-duckdb", §"What is magic-duckdb?" | **Misleads students** — describes syntax the notebook never uses |
| `magic_duckdb` in the install list | Setup cell | Installs a package that is never imported |
| "Load magic-duckdb" cell | After setup | **Empty** — a comment and nothing else |

None of this breaks the notebook. It runs correctly. But a student reading it will be
told about a feature they will not see.

---

## Run it

```bash
marimo edit CRUD_employees_duckdb_marimo.py    # interactive
marimo run  CRUD_employees_duckdb_marimo.py    # read-only
```

| File | Role |
|---|---|
| `CRUD_employees_duckdb_marimo.py` | The notebook |
| `display_utils.py` | Display and chart helpers |
| `data/employees.csv` | 10 employees |

---

## What it covers

| § | Section | Operations |
|---|---|---|
| 0 | Environment setup | Install packages, connect |
| 2A | **CREATE** | 4 `INSERT` examples |
| 2B | **READ** | 4 `SELECT` examples |
| 2C | **UPDATE** | 4 `UPDATE` examples |
| 2D | **DELETE** | 4 `DELETE` examples |

**Sixteen worked examples in total** — more drill per concept than any other CRUD
story here. That is now its real distinguishing feature.

---

## What it no longer offers

Before the Marimo conversion, this story existed to show an **alternative way of
writing SQL** in a notebook:

```sql
%%dql
SELECT * FROM employees WHERE salary > 60000
```

instead of wrapping each query in Python. That was a genuine reason to keep a
separate variant.

With `%%dql` gone, **the SQL here looks the same as everywhere else**. If you were
planning to use this story to show students a different notebook style, that reason
no longer applies — use it for the extra practice instead.

---

## Choosing among the CRUD stories

They all teach the same four operations. The differences:

| Story | Rows | What makes it different |
|---|---|---|
| `CRUD_100_10_rows/` | 10 | The plainest version. **Start here.** |
| **`CRUD_100_10_rows_with_dql/`** ← this one | 10 | **4 examples per operation** — most repetition |
| `CRUD_100_10_rows_with_images/` | 10 | Adds employee photos to result tables |
| `CRUD_100_10_rows_flagship/` | 10 | Photos, backup table, persistence, re-runnability |
| `CRUD_9_emps_intro/` | 9 | Longest conceptual intro — "what is DuckDB", "what is CRUD" |
| `CRUD_10_emps_staging/` | 10 | Staging-table variant |
| `CRUD_10_emps_persistent/` | 10 | Persistent database and backup table |
| `emps_single_table/` | 1,100 | Real-size table; adds a "did the changes stick?" check |

> **Note:** these folders were renamed in 2026 to say what they actually contain.
> They were previously `CRUD_100_emps`, `CRUD_101_emps`, `CRUD_102_emps` and
> `CRUD_100_10_rows_with_images_openai` — names whose numbers were not row counts and
> which promised an AI integration that does not exist.
>
> **This folder's own name is still inaccurate** and would be worth renaming too —
> something like `CRUD_100_10_rows_drill` would describe it correctly.

**Assign one.** They are variations on a theme, and doing several is repetition
without new material.
