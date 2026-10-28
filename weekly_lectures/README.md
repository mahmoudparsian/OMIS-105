# Weekly Lectures

Lecture materials for **OMIS 105 — Introduction to Database Management
Systems**, Fall 2026 — one folder per week, ten weeks.

Each week runs **two 2-hour sessions**, so each folder carries two slide
decks and (usually) two live-demo notebooks: one pair per session.

The companion folder [`weekly_reviews/`](../weekly_reviews) uses the same
week folder names and holds cumulative review notebooks for the same
topics.

## The Ten Weeks

| Week | Folder | Topic |
|------|--------|-------|
| 1 | [`week01-database-foundations/`](week01-database-foundations/) | Database foundations — what a database is, first SQL, tooling setup |
| 2 | [`week02-relational-modeling/`](week02-relational-modeling/) | Relational modeling & data thinking |
| 3 | [`week03-sql-basics/`](week03-sql-basics/) | SQL core — `SELECT`, `WHERE`, `ORDER BY` |
| 4 | [`week04-sql-aggregation/`](week04-sql-aggregation/) | SQL analytics — aggregation, `GROUP BY`, `HAVING` |
| 5 | [`week05-sql-joins/`](week05-sql-joins/) | JOIN deep dive |
| 6 | [`week06-sql-joins-2/`](week06-sql-joins-2/) | Joins II — `INNER`, `LEFT`, `RIGHT JOIN` in practice, self-joins, 3+ tables |
| 7 | [`week07-subqueries/`](week07-subqueries/) | Subqueries — a query inside a query |
| 8 | [`week08-database-design/`](week08-database-design/) | Database design & normalization |
| 9 | [`week09-query-performance/`](week09-query-performance/) | Indexing & query performance |
| 10 | [`week10-transactions-acid/`](week10-transactions-acid/) | Transactions & ACID |

### Bonus weeks (optional)

Two weeks moved to [`bonus/`](bonus/) when Joins II and Subqueries were
added, and are now numbered 11 and 12 (folders, files, and contents).
Nothing was deleted.

| Folder | Topic |
|--------|-------|
| [`bonus/week11-project-integration/`](bonus/week11-project-integration/) | Project & integration — build a real system |
| [`bonus/week12-review-modern-data/`](bonus/week12-review-modern-data/) | Review, synthesis & real-world perspective |

## Download a Week as a ZIP

You do not need git to get the course files. Each link below
downloads one week as a single ZIP file. Inside it are two folders:

- `lectures/` — that week's folder from here
- `review/` — the matching folder from [`weekly_reviews/`](../weekly_reviews)

| Week | Download |
|------|----------|
| 1 | [`week01-database-foundations.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week01-database-foundations.zip) |
| 2 | [`week02-relational-modeling.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week02-relational-modeling.zip) |
| 3 | [`week03-sql-basics.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week03-sql-basics.zip) |
| 4 | [`week04-sql-aggregation.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week04-sql-aggregation.zip) |
| 5 | [`week05-sql-joins.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week05-sql-joins.zip) |
| 6 | [`week06-sql-joins-2.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week06-sql-joins-2.zip) |
| 7 | [`week07-subqueries.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week07-subqueries.zip) |
| 8 | [`week08-database-design.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week08-database-design.zip) |
| 9 | [`week09-query-performance.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week09-query-performance.zip) |
| 10 | [`week10-transactions-acid.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week10-transactions-acid.zip) |
| Bonus | [`bonus-week11-project-integration.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/bonus-week11-project-integration.zip) |
| Bonus | [`bonus-week12-review-modern-data.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/bonus-week12-review-modern-data.zip) |

To use a week, unzip it, open a terminal in the `lectures/` or
`review/` folder, and run `marimo edit` on a notebook.

The ZIP files are rebuilt automatically every time the course files
change. A link always gives you the newest version. If you downloaded
a week earlier, download it again to get any updates.

## What Is in a Week Folder

Weeks 2–10 share a common layout:

| File | What It Is |
|------|-----------|
| `slides_1.md`, `slides_2.md` | Marp slide decks — one per class session |
| `demo1.py`, `demo2.py` | Live-demo Marimo notebooks — one per session |
| `labNN_student.md` | **The week's lab**, with blanks for students to fill in |
| `quiz.md` | Short quiz questions for the week |
| `data/` | CSV files the demos and lab read |
| `lab.md`, `notes.md`, `solution.sql` | Brief scratch notes — see the caveat below |

These folders differ:

- **Week 1** predates the naming convention. Its decks are
  `Lecture_Slides_01.md` / `Lecture_Slides_02.md`, and its demos are six
  numbered *folders* (`demo1_sql_with_qstudio/` through
  `demo6_intro_to_sql_by_presidents/`) rather than two `.py` files,
  because day one covers tool setup — qStudio, DuckDB, and first
  notebooks — as well as SQL. It also holds `sql_notebooks/` (the
  day-one welcome notebooks) and `Sample_Lab_Student.py` with its
  solution.
- **Week 2** has a third demo, `demo3.py`.
- **Weeks 6 and 7** (Joins II and Subqueries, added 2026-10-27) have the
  usual slides, demos, lab, quiz, and `data/` (Week 6 also has
  `images/`), but no `lab.md`, `notes.md`, or `solution.sql` stubs.
- **The bonus weeks** (11 and 12; Weeks 9 and 10 before 2026-10-27) have no `demo*.py`. They use full Marimo notebooks
  instead — `week11_notebook_marimo.py`, `lab11_student_marimo.py`
  (the capstone starter template, renamed from
  `week09_project_template_marimo.py`), and `week11_project_example.py`
  (a worked example project) for the capstone, and `week12_notebook_marimo.py`, `week12_review_marimo.py`,
  and `week12_capstone_review.md` for the final review.

### Tutorial subfolders

Some weeks also have self-contained tutorial folders. Each one has
its own small DuckDB database, a notebook, and a README:

| Week | Folder | What it teaches |
|------|--------|-----------------|
| 4 | [`group_by_with_emps_depts/`](week04-sql-aggregation/group_by_with_emps_depts/) | **The `GROUP BY` tutorial:** 18 queries and 11 charts, from basic counts to `HAVING` and pivot tables |
| 5 | [`joins_with_emps_depts/`](week05-sql-joins/joins_with_emps_depts/) | First joins demo: every join type on 4 departments and 6 employees |
| 5 | [`joins_with_users_roles_cities/`](week05-sql-joins/joins_with_users_roles_cities/), [`joins_with_authors_books_orders/`](week05-sql-joins/joins_with_authors_books_orders/), [`joins_with_students_and_courses/`](week05-sql-joins/joins_with_students_and_courses/) | More join practice on larger databases |

The week folders for 4 and 5 each have a README that describes them.

### A caveat on `lab.md`, `notes.md`, and `solution.sql`

These three are **short scratch stubs**, typically 4–8 lines: a rough lab
outline, a couple of "students usually get confused here" reminders, and a
few sample SQL statements. They are not the graded materials.

The real lab for each week is `labNN_student.md`. The matching answer key
is kept by the instructor and is not published in this repository.

## How to Use These Files

**Slide decks** are [Marp](https://marp.app/) Markdown. Preview them in
VS Code with the Marp extension, or export to PDF:

```bash
marp weekly_lectures/week03-sql-basics/slides_1.md --pdf
```

**Demo notebooks** are [Marimo](https://marimo.io/). Launch one from
inside its week folder so the relative `data/` paths resolve:

```bash
cd weekly_lectures/week03-sql-basics
marimo edit demo1.py
```

**Labs** are Markdown. `labNN_student.md` is the version students work
from; answer keys are held separately by the instructor.

## Tech Stack

- **Database:** DuckDB (in-memory, embedded — no server setup)
- **Notebooks:** Marimo (reactive Python notebooks)
- **Slides:** Marp (Markdown → PDF)
- **Language:** Python 3 + SQL

The week notebooks run SQL through `con.execute()` against an in-memory
DuckDB connection. The tutorial subfolders above use native SQL cells
(`mo.sql()`) against a read-only `.duckdb` file instead, so you see
only the SQL.

## Related Folders

| Folder | What It Adds |
|--------|-------------|
| [`../weekly_reviews/`](../weekly_reviews) | Cumulative review notebook + teaching notes per week, same folder names |
| [`../outline-10-weeks/`](../outline-10-weeks) | The 10-week syllabus and tech-stack overview |
| [`../tutorials/`](../tutorials) | Standalone tutorials, each mapped to a best-fit week |
| [`../data_stories/`](../data_stories) | 36 short DuckDB + Marimo demo notebooks |
| [`../course_information/`](../course_information) | Grading, attendance, and course policies |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
