# Week 5 — SQL Joins

Lecture materials for Week 5 of **OMIS 105**. This week is about
combining tables with `JOIN`.

## Start Here: Employees / Departments

**[`joins_with_emps_depts/`](joins_with_emps_depts/)** — the first
joins demo: just 4 departments and 6 employees, small enough to
check every answer by eye. Two departments have no employees, and
two employees have no department, so every join type gives a
different row count. It includes:

- [`notebook.py`](joins_with_emps_depts/notebook.py) — a Marimo
  notebook with 21 SQL queries. It opens `emps_depts_db.duckdb`
  read-only and covers aggregation, `INNER`, `LEFT`, `RIGHT`,
  `FULL OUTER`, and `CROSS` joins, then "find what is missing"

Start with that folder's [README](joins_with_emps_depts/README.md).

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

## Join Practice: Authors / Books / Orders

**[`joins_with_authors_books_orders/`](joins_with_authors_books_orders/)**
— a small online bookstore: `authors` → `books` → `orders`. Two
authors have no books, and four books were never ordered, so
`INNER JOIN`, `LEFT JOIN`, and `RIGHT JOIN` give different answers.
It includes:

- [`create_duckdb_database.sh`](joins_with_authors_books_orders/create_duckdb_database.sh)
  — builds `authors_books_orders.duckdb` from `db_schema.sql` and
  `db_records.sql`. Run it first.
- [`notebook.py`](joins_with_authors_books_orders/notebook.py) — a
  Marimo notebook with 26 queries and 5 charts. It opens the database read-only
  and goes from a little aggregation to `INNER`, `LEFT`, and `RIGHT`
  joins, then to "find what is missing"

Start with that folder's [README](joins_with_authors_books_orders/README.md).

## Join Practice: Students / Courses / Grades

**[`joins_with_students_and_courses/`](joins_with_students_and_courses/)**
— a university database: `students` ──< `grades` >── `courses`. It is
bigger than the bookstore: 500 students, 50 courses, and 8,000
grades. Five students have never taken a course, and three courses
were never taken, so `INNER JOIN`, `LEFT JOIN`, and `RIGHT JOIN` give
different answers. It includes:

- [`create_duckdb_database.sh`](joins_with_students_and_courses/create_duckdb_database.sh)
  — builds `students_courses_grades.duckdb` from `db_schema.sql` and
  `db_records.sql`. Run it first.
- [`notebook.py`](joins_with_students_and_courses/notebook.py) — a
  Marimo notebook with 16 queries and 6 charts. It opens the database
  read-only and goes from simple `SELECT`s and aggregation to
  `INNER`, `LEFT`, and `RIGHT` joins, including a GPA by department
- [`interview_practice/`](joins_with_students_and_courses/interview_practice/)
  — optional: 12 timed SQL interview questions, from warm-up to hard,
  with an automatic row-count check under each one, and answers that
  explain the common mistakes
- [`manager_questions/`](joins_with_students_and_courses/manager_questions/)
  — optional: 8 vague requests from managers (the Dean, the CFO, …).
  You define what to measure, write the query, and write the answer
  you would send, then compare with model answers and 5 charts
- [`data_quality/`](joins_with_students_and_courses/data_quality/)
  — optional, advanced: a data-quality round on a messy copy of the
  database. 14 checks for duplicates, bad spellings, `NULL`s, and
  orphan rows, with answers that show which database rules would
  have stopped each problem

Start with that folder's [README](joins_with_students_and_courses/README.md).

## Files in This Folder

| File | What It Is |
|------|-----------|
| `lecture_slides_01.md` | Marp slide deck, session 1 — JOIN deep dive |
| `lecture_slides_02.md` | Marp slide deck, session 2 — window functions, CTEs, set operations, views |
| `SQL_Joins_in_Action_with_DuckDB.md` | All five join types: symbols, math, and verified DuckDB examples |
| `join_symbols.md` | Quick reference: relational-algebra symbols for each join (⋈ ⟕ ⟖ ⟗ ×) |
| `notebook_01_join_basics.py` | Live-demo Marimo notebook, session 1 |
| `notebook_02_join_basics.py` | Live-demo Marimo notebook, session 2 |
| `sample_lab_01_student.md` | Sample lab (window functions, CTEs, set operations, views), with blanks to fill in |
| `sample_lab_01_instructor.md` | The same sample lab, with answers |
| `notebook_03_student.py` | The sample lab as a Marimo notebook |
| `notebook_03_instructor.py` | The sample lab notebook, with answers |
| `quiz.md` | Short quiz questions for the week |
| `data/` | CSV files the demos and lab read |
| `lab.md`, `notes.md`, `solution.sql` | Brief scratch notes and sample SQL |

Run the notebooks from inside this folder, so the `data/` paths work:

```bash
cd weekly_lectures/week05-sql-joins
marimo edit notebook_01_join_basics.py
```

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
