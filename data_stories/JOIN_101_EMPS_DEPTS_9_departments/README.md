# 🔗 JOIN 101 — Employees & Departments (9 departments)

**OMIS-105 · Week 5 — SQL Joins**

Employees and departments joined every way SQL allows. This is **the larger of the two** —
9 departments and 25 employees.

---

## Run it

```bash
marimo edit JOIN_101_EMPS_DEPTS_marimo.py
```

| File | Role |
|---|---|
| `JOIN_101_EMPS_DEPTS_marimo.py` | The joins notebook |
| `notebook_utils.py` | Display helpers |
| `CRUD_Employees_DuckDB_marimo.py` | A **second, unrelated notebook** — CRUD, not joins (see `CRUD_100_10_rows/`) |
| `crud_helpers.py` | Helpers for that CRUD notebook |
| `data/employees.csv` | 25 employees |
| `data/departments.csv` | 9 departments |

---

## What it covers

| Join | Keeps |
|---|---|
| **INNER JOIN** | Only employees who have a department **and** departments that have employees |
| **LEFT JOIN** | Every employee, whether or not they have a department |
| **RIGHT JOIN** | Every department, whether or not it has employees |

The data is shaped so the three joins really do differ:

- **Some employees have no department** — those are the rows only `LEFT JOIN` keeps.
- **Some departments have no employees** — those are the rows only `RIGHT JOIN` keeps.
- **`INNER JOIN` drops both**, so it returns the fewest rows.

**Run all three and compare the row counts.** That single comparison explains what
each join does faster than any definition.

---

## ⚠️ Before you assign this

**There are three overlapping joins stories.** Pick one:

| Story | Depts | Emps | Notes |
|---|---|---|---|
| `FK_JOINS/` | 4 | 8 | **Best choice.** Purpose-built, with PK/FK material and companion reading |
| `JOIN_101_EMPS_DEPTS_5_departments/` | 5 | 12 | Smaller |
| `JOIN_101_EMPS_DEPTS_9_departments/` | 9 | 25 | Larger |

**The folder layout is untidy.** Both `JOIN_101` folders hold several copies of the
same data:

- `data/` — what the notebook reads
- `data2/`, a `.backup/` directory, and a `files.zip` — older copies
- the 5-department folder also has loose CSVs at the top level
- this folder additionally contains an **unrelated CRUD notebook**

**The copies do not agree on row counts.** Before you quote a number to a class,
check which path the notebook actually loads.

> This folder used to be called `JOIN_101_EMPS_DEPTS_10_departments`. It was renamed
> because `data/` holds **9** departments, not 10.
