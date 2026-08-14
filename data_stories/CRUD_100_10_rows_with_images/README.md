# 🖼️ CRUD with Employee Photos

**OMIS-105 · Week 3 — SQL Basics**

The same ten-employee CRUD story as `CRUD_100_10_rows/`, with a photo for every
employee rendered inline in the result tables.

---

## Run it

```bash
marimo edit CRUD_Employees_DuckDB_marimo.py
```

Needs an **internet connection** — images are fetched at display time.

| File | Role |
|---|---|
| `CRUD_Employees_DuckDB_marimo.py` | The notebook |
| `crud_helpers.py` | Display helpers, including image rendering |
| `transform.py` | Data preparation |
| `web_images.txt` | The image URLs |
| `data/employees.csv` | 10 employees |

---

## What it covers

The notebook explains each operation from first principles before using it:

| Section | Question it answers |
|---|---|
| What is DuckDB? | Why a database at all |
| What is CRUD? | The four operations |
| Two helper functions | How the notebook prints tables and images |
| What is INSERT? | **C** — adding rows |
| What is SELECT? | **R** — reading rows |
| What is UPDATE? | **U** — changing rows |
| What is DELETE? | **D** — removing rows |

---

## Why images

The database stores a **URL as text**. It has no idea it is a picture — the rendering
happens entirely in `crud_helpers.py` when the result is displayed.

That is worth saying out loud, because it is a genuine modelling point:

- Databases store **references** to files far more often than the files themselves.
- A production system keeps the image in object storage and the **URL in a column** —
  exactly the shape used here.
- Storing the picture itself would make the database large, slow, and hard to back up.

The practical benefit is attention: an `UPDATE` is more memorable when a face moves
with it.

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
