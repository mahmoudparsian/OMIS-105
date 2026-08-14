# 🐣 My Very First DuckDB Notebook

**OMIS-105 · Week 1 — Database Foundations**

The gentlest possible start. Ten steps, one small table, no data files, nothing to
install beyond DuckDB itself. If you have never touched a database before, **start
here.**

---

## Run it

```bash
marimo edit My_Very_First_DuckDB_Notebook_marimo.py    # interactive
marimo run  My_Very_First_DuckDB_Notebook_marimo.py    # read-only
```

| File | Role |
|---|---|
| `My_Very_First_DuckDB_Notebook_marimo.py` | The notebook — 10 steps |

- The database is **in-memory** (`:memory:`), so nothing is written to disk.
- You can re-run the notebook as many times as you like.
- Close it and the data is gone — which is exactly the point of Step 10.

---

## What it covers

| Step | Topic | SQL |
|---|---|---|
| 1 | Import DuckDB and connect | — |
| 2 | Create the `students` table | `CREATE OR REPLACE TABLE` |
| 3 | Insert 10 rows | `INSERT INTO` |
| 4 | View all rows | `SELECT *` |
| 5 | Filter | `WHERE` |
| 6 | Sort | `ORDER BY` |
| 7 | Count rows | `COUNT(*)` |
| 8 | Aggregate | `AVG`, `SUM` |
| 9 | Top N | `LIMIT` |
| 10 | Close the connection | — |

---

## The data

A single `students` table with 10 rows, typed by hand in Step 3. Small enough that
you can read the whole thing and check every answer yourself — which is the reason
it is small.

---

## Where to go next

| If you want… | Go to |
|---|---|
| More on the DuckDB tool itself | `Introducing_DuckDB_by_Presidents/` |
| Practice with `SELECT` / `WHERE` | `emps_single_table/`, `CRUD_100_10_rows/` |
| To understand keys | `PRIMARY_KEY/` |

---

## Teaching notes

- Steps 1–4 are enough for a first 20-minute session. Steps 5–9 map directly onto the
  Week 3 lab, so this notebook can be revisited then as a warm-up.
- **Step 10 is worth dwelling on.** Students often assume data is saved automatically.
  Closing an in-memory connection and losing everything is a cheap, memorable way to
  introduce the idea that persistence is a choice — which Week 8 makes rigorous.
