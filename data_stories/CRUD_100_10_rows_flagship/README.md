# 🚩 CRUD Flagship — Employees with Images

**OMIS-105 · Week 3 — SQL Basics**

The most thorough of the CRUD stories: ten employees, images in every result, a
backup table, and explicit re-runnability. Billed in the notebook itself as the
**"Flagship"** version.

---

## ⚠️ A note on this folder's history

This story used to be called `CRUD_100_10_rows_with_images_openai`, which was
misleading:

- **It contains no OpenAI code and makes no AI calls.**
- The only occurrence of the word anywhere in the folder was a file path inside the
  old build prompt.
- It is an ordinary CRUD-with-images notebook, so it belongs in **Week 3** — not in a
  modern-data or AI unit.

It was renamed to `CRUD_100_10_rows_flagship`, after the name the notebook already
uses for itself.

---

## Run it

```bash
marimo edit CRUD_Employees_DuckDB_Flagship_marimo.py
```

| File | Role |
|---|---|
| `CRUD_Employees_DuckDB_Flagship_marimo.py` | The notebook |
| `helper_functions.py` | Display helpers, including image rendering |
| `data/employees.csv` | 10 employees |
| `data/employees_backup.csv` | Backup copy |
| `employees_crud.duckdb` | **Persistent** database |

---

## What it covers

| Cell | Step |
|---|---|
| 1–2 | Setup, verify the data files exist |
| 3 | **Make the notebook re-runnable** |
| 4–5 | Create the `employees` table, insert exact records |
| 6 | Read with raw URLs **and** rendered images side by side |
| 7–8 | Create `employees_backup` from CSV, display it |
| 9–10 | Create `employees_from_csv`, compare table counts |
| C1–C4 | **CREATE** — new employees, copy from backup, build a summary table |
| … | READ, UPDATE, DELETE sections |

---

## The two things it does better than its siblings

**Cell 3 makes the notebook re-runnable.** Because the database is persistent, a
second run would otherwise hit duplicate-key errors or double-insert rows. Cell 3
resets state explicitly first.

That is a real engineering habit worth naming:

- **A notebook you cannot run twice is a notebook you cannot trust.**
- Every other CRUD story here dodges the problem by using an in-memory database, which
  starts empty every time.
- This one uses a real file, so it has to reset state deliberately — and shows you how.

**Cell 6 shows the URL and the image together.** Seeing `https://…/photo.jpg` in one
column and the rendered face beside it makes the point that the database stores
*text* — the picture is produced by the display layer, not the database.

---

## Choosing among the CRUD stories

| Story | Rows | What makes it different |
|---|---|---|
| `CRUD_100_10_rows/` | 10 | The plainest version. **Start here.** |
| `CRUD_100_10_rows_drill/` | 10 | Same content using `%%dql` cell magic |
| `CRUD_100_10_rows_with_images/` | 10 | Adds employee photos |
| **`CRUD_100_10_rows_flagship/`** ← this one | 10 | Photos **plus** backup table, persistence, re-runnability |
| `CRUD_9_emps_intro/` | 9 | Longest conceptual intro |
| `CRUD_10_emps_staging/` | 10 | Staging-table variant |
| `CRUD_10_emps_persistent/` | 10 | Persistent database and backup table |
| `emps_single_table/` | 1,100 | Real-size table |

> **Note:** five of these folders were renamed in 2026 to say what they actually
> contain. They were previously `CRUD_100_emps`, `CRUD_101_emps`, `CRUD_102_emps`,
> `CRUD_100_10_rows_with_images_openai` and `CRUD_100_10_rows_with_dql` — names whose
> numbers were not row counts, that promised an AI integration which does not exist,
> or that named a feature the notebook no longer uses.

**Assign one.** This is the most complete if you want a single thorough pass; use
`CRUD_100_10_rows/` if you want the simplest.
