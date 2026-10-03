# Week 5 — SQL Joins

Lecture materials for Week 5 of **OMIS 105**. This week is about
combining tables with `JOIN`.

## Join Practice: Users / Roles / Cities

**[`joins_with_users_roles_cities/`](joins_with_users_roles_cities/)**
— a tiny three-table database (`users`, `roles`, `cities`) built for
join practice. Some users have no role or no city, and some roles and
cities have no users, so `INNER JOIN` and `LEFT JOIN` give different
answers. It includes:

- [`notebook.py`](joins_with_users_roles_cities/notebook.py) — a
  Marimo notebook with 20 practice queries and 5 charts
- [`users_roles_cities_join_operations.md`](joins_with_users_roles_cities/users_roles_cities_join_operations.md)
  — 40 practice queries, from basic `SELECT` to "find what is
  missing", each with its expected result

Start with that folder's [README](joins_with_users_roles_cities/README.md).

## Files in This Folder

| File | What It Is |
|------|-----------|
| `slides_1.md` | Marp slide deck, session 1 — JOIN deep dive |
| `slides_2.md` | Marp slide deck, session 2 — window functions, CTEs, set operations, views |
| `demo1.py` | Live-demo Marimo notebook, session 1 |
| `demo2.py` | Live-demo Marimo notebook, session 2 |
| `lab05_student.md` | The week's lab, with blanks to fill in |
| `lab05_student_marimo.py` | The same lab as a Marimo notebook |
| `lab05_instructor_marimo.py` | The lab notebook with answers |
| `quiz.md` | Short quiz questions for the week |
| `data/` | CSV files the demos and lab read |
| `lab.md`, `notes.md`, `solution.sql` | Brief scratch notes and sample SQL |

Run the notebooks from inside this folder, so the `data/` paths work:

```bash
cd weekly_lectures/week05-sql-joins
marimo edit demo1.py
```

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
