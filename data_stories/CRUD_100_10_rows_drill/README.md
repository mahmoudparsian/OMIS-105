# 🔁 CRUD Drill — Four Examples per Operation

**OMIS-105 · Week 3 — SQL Basics**

The same ten-employee CRUD story as `CRUD_100_10_rows/`, but with **four worked
examples of each operation** instead of one or two.

**Sixteen worked examples in total** — more practice per concept than any other CRUD
story here. Choose it when students need repetition rather than new material.

---

## Run it

```bash
marimo edit CRUD_100_10_rows_drill_marimo.py    # interactive
marimo run  CRUD_100_10_rows_drill_marimo.py    # read-only
```

| File | Role |
|---|---|
| `CRUD_100_10_rows_drill_marimo.py` | The notebook |
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

Every query lives in its own SQL cell, so what students read is plain SQL with no
Python wrapped around it.

---

## Why four examples each

One example shows a student **that** a statement works. Four show them **how it
varies**:

- Different `WHERE` conditions on the same `UPDATE`
- Filtering on text, then on numbers, then on both
- Deleting one row, then a set of rows
- Reading with and without sorting and limits

That variation is what turns "I saw it done" into "I could write it myself". On a
ten-row table it costs nothing to run all sixteen.

---

## Ten rows, on purpose

The table is small enough to print in full **before and after every statement**:

- With all ten rows on screen, you can check that a statement changed **the rows you
  meant** — and nothing else.
- That habit is impossible on a table of ten thousand rows.
- Which is exactly why it is worth building now, while it is still easy.

---

## ⚠️ The one thing to be careful about

`UPDATE` and `DELETE` take a `WHERE` clause. **If you leave it off, the statement
applies to every row in the table, and no error is raised.**

```sql
DELETE FROM employees WHERE emp_id = 300;   -- deletes one row
DELETE FROM employees;                      -- deletes ALL of them. No warning.
```

This is the most expensive beginner mistake in SQL. Making it here, on ten rows you
can regenerate in a second, is a much better place to learn it.

---

## Choosing among the CRUD stories

They all teach the same four operations. The differences:

| Story | Rows | What makes it different |
|---|---|---|
| `CRUD_100_10_rows/` | 10 | The plainest version. **Start here.** |
| **`CRUD_100_10_rows_drill/`** ← this one | 10 | **4 examples per operation** — most repetition |
| `CRUD_100_10_rows_with_images/` | 10 | Adds employee photos to result tables |
| `CRUD_100_10_rows_flagship/` | 10 | Photos, backup table, persistence, re-runnability |
| `CRUD_9_emps_intro/` | 9 | Longest conceptual intro — "what is DuckDB", "what is CRUD" |
| `CRUD_10_emps_staging/` | 10 | Staging-table variant |
| `CRUD_10_emps_persistent/` | 10 | Persistent database and backup table |
| `emps_single_table/` | 1,100 | Real-size table; adds a "did the changes stick?" check |

**Assign one.** They are variations on a theme, and doing several is repetition
without new material.

---

## Teaching notes

- **Use it for practice, not for first exposure.** Sixteen examples is a lot to sit
  through cold. Teach the four operations from `CRUD_100_10_rows/`, then come here
  when students need the reps.
- Good in-class pattern: run example 1 of each block, then have students **predict**
  what examples 2–4 will return before running them.
- Ask what `UPDATE employees SET salary = 100000` does before running it. Then run it
  on a copy.
