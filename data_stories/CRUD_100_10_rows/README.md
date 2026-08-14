# ✏️ CRUD on 10 Employees

**OMIS-105 · Week 3 — SQL Basics**

The plainest CRUD story in the folder. One table, ten rows, and the four operations
every database supports: **C**reate, **R**ead, **U**pdate, **D**elete.

**If you are choosing between the six CRUD stories, start with this one.**

---

## Run it

```bash
marimo edit CRUD_Employees_DuckDB_marimo.py    # interactive
marimo run  CRUD_Employees_DuckDB_marimo.py    # read-only
```

| File | Role |
|---|---|
| `CRUD_Employees_DuckDB_marimo.py` | The notebook |
| `crud_helpers.py` | Display helpers, kept out of the notebook |
| `data/employees.csv` | 10 employees |

---

## What CRUD means

| Letter | Operation | SQL | What it does |
|---|---|---|---|
| **C** | Create | `INSERT INTO` | Add new rows |
| **R** | Read | `SELECT` | Look at rows without changing them |
| **U** | Update | `UPDATE … SET … WHERE` | Change existing rows |
| **D** | Delete | `DELETE FROM … WHERE` | Remove rows |

Those four cover essentially everything an application does to a database:

- Posting a photo is a **Create**.
- Loading your feed is a **Read**.
- Editing your profile is an **Update**.
- Removing a comment is a **Delete**.

Every app you have ever used is doing these behind a nicer interface.

---

## Ten rows, on purpose

The table is small enough to print in full **before and after every statement**.
That matters more than it sounds:

- With all ten rows on screen, you can check that an `UPDATE` changed **the row you
  meant** — and nothing else.
- That habit (look at the table, confirm the change) is impossible at ten thousand
  rows.
- Which is exactly why it is worth building now, while it is still easy.

---

## ⚠️ The one thing to be careful about

`UPDATE` and `DELETE` take a `WHERE` clause. **If you leave it off, the statement
applies to every row in the table, and no error is raised.**

```sql
DELETE FROM employees WHERE emp_id = 3;   -- deletes one row
DELETE FROM employees;                    -- deletes ALL of them. No warning.
```

This is the most expensive beginner mistake in SQL. Making it here, on ten rows you
can regenerate in a second, is a much better place to learn it.

---

## Choosing among the CRUD stories

They all teach the same four operations. The differences:

| Story | Rows | What makes it different |
|---|---|---|
| **`CRUD_100_10_rows/`** ← this one | 10 | The plainest version. **Start here.** |
| `CRUD_100_10_rows_drill/` | 10 | Same content using `%%dql` cell magic |
| `CRUD_100_10_rows_with_images/` | 10 | Adds employee photos to result tables |
| `CRUD_9_emps_intro/` | 9 | Longest conceptual intro — "what is DuckDB", "what is CRUD" |
| `CRUD_10_emps_staging/` | 10 | Helper-module variant |
| `CRUD_10_emps_persistent/` | 10 | Uses a **persistent** database and a backup table |
| `emps_single_table/` | **1,100** | Real-size table; adds a "did the changes stick?" check |

> **Note:** five of these folders were renamed in 2026 to say what they actually
> contain. They were previously `CRUD_100_emps`, `CRUD_101_emps`, `CRUD_102_emps`,
> `CRUD_100_10_rows_with_images_openai` and `CRUD_100_10_rows_with_dql` — names whose
> numbers were not row counts, that promised an AI integration which does not exist,
> or that named a feature the notebook no longer uses.

**Assign one.** They are variations on a theme, and doing several is repetition
without new material.

---

## Teaching notes

- Print the table before and after each statement — the notebook already does, and it
  is the thing that makes CRUD click.
- Ask what `UPDATE employees SET salary = 100000` does before running it. Then run it
  on a copy.
- Natural next step: `PRIMARY_KEY/` (Week 2) if they have not seen it, or
  `emps_single_table/` for the same operations on a table too big to eyeball.
