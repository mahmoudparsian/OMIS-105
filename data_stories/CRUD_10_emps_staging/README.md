# 🗂️ CRUD of Employees Data — Staging Table Variant

**OMIS-105 · Week 3 — SQL Basics**

A ten-employee CRUD story whose distinguishing feature is that it **loads into a
staging table first**, then moves data into the real table.

---

## Run it

```bash
marimo edit CRUD_10_emps_staging_marimo.py
```

| File | Role |
|---|---|
| `CRUD_10_emps_staging_marimo.py` | The notebook |
| `emp_utils.py` | Display and utility helpers |
| `data/employees.csv` | 10 employees |
| `helpers/` | (empty) |

---

## The staging-table idea

Rather than loading the CSV straight into `employees`, the notebook loads it into a
**staging table**, checks it, and only then populates the real one.

That is how production data pipelines actually work, and the reason is worth stating:

- The staging table has **no constraints**, so a bad file loads without exploding
- You can then *inspect* what arrived — row counts, nulls, duplicates
- Only clean rows move into the real table, which *does* have constraints

The alternative — loading directly into a constrained table — means a single bad row
aborts the whole load and you learn nothing about what was wrong with the file.

**This is the same reasoning behind Week 2's `PRIMARY_KEY/` story**, seen from the
other side: there, a table without a key let bad data in. Here, a table without
constraints is deliberately used as a safe landing zone.

---

## Two notes on this folder

- **It was renamed.** It used to be `CRUD_101_emps`, where the `101` was not a row
  count. The table holds **10 employees**.
- **`helpers/` is empty.** The actual helper code is `emp_utils.py` in the folder root.

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
