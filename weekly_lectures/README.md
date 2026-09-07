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
| 6 | [`week06-database-design/`](week06-database-design/) | Database design & normalization |
| 7 | [`week07-query-performance/`](week07-query-performance/) | Indexing & query performance |
| 8 | [`week08-transactions-acid/`](week08-transactions-acid/) | Transactions & ACID |
| 9 | [`week09-project-integration/`](week09-project-integration/) | Project & integration — build a real system |
| 10 | [`week10-review-modern-data/`](week10-review-modern-data/) | Review, synthesis & real-world perspective |

## What Is in a Week Folder

Weeks 2–8 share a common layout:

| File | What It Is |
|------|-----------|
| `slides_1.md`, `slides_2.md` | Marp slide decks — one per class session |
| `demo1.py`, `demo2.py` | Live-demo Marimo notebooks — one per session |
| `labNN_student.md` | **The week's lab**, with blanks for students to fill in |
| `labNN_instructor.md` | The same lab with answers and teaching commentary |
| `quiz.md` | Short quiz questions for the week |
| `data/` | CSV files the demos and lab read |
| `lab.md`, `notes.md`, `solution.sql` | Brief scratch notes — see the caveat below |

Three folders differ:

- **Week 1** predates the naming convention. Its decks are
  `Lecture_Slides_01.md` / `Lecture_Slides_02.md`, and its demos are six
  numbered *folders* (`demo1_sql_with_qstudio/` through
  `demo6_intro_to_sql_by_presidents/`) rather than two `.py` files,
  because day one covers tool setup — qStudio, DuckDB, and first
  notebooks — as well as SQL. It also holds `sql_notebooks/` (the
  day-one welcome notebooks) and `Sample_Lab_Student.py` with its
  solution.
- **Week 2** has a third demo, `demo3.py`.
- **Weeks 9 and 10** have no `demo*.py`. They use full Marimo notebooks
  instead — `week09_notebook_marimo.py` and
  `week09_project_template_marimo.py` for the capstone project, and
  `week10_notebook_marimo.py`, `week10_review_marimo.py`, and
  `week10_capstone_review.md` for the final review.

### A caveat on `lab.md`, `notes.md`, and `solution.sql`

These three are **short scratch stubs**, typically 4–8 lines: a rough lab
outline, a couple of "students usually get confused here" reminders, and a
few sample SQL statements. They are not the graded materials.

The real lab for each week is `labNN_student.md` (with
`labNN_instructor.md` as the answer key).

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

**Labs** are Markdown. Hand out `labNN_student.md`; keep
`labNN_instructor.md` for yourself.

## Tech Stack

- **Database:** DuckDB (in-memory, embedded — no server setup)
- **Notebooks:** Marimo (reactive Python notebooks)
- **Slides:** Marp (Markdown → PDF)
- **Language:** Python 3 + SQL

Every notebook in this folder runs SQL through `con.execute()` against an
in-memory DuckDB connection.

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
