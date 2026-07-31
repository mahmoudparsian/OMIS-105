# CLAUDE.md — OMIS 105 Course Materials

## Project Overview

Teaching materials for **OMIS 105 — Introduction to Database Management Systems**, a senior undergraduate business course at Santa Clara University (Leavey School of Business), Fall 2026. Instructor: Dr. Mahmoud Parsian (mparsian@scu.edu).

**Tech stack:** Python · DuckDB · Jupyter Notebook

**Audience:** Senior business students (not CS majors). Every concept must be grounded in business scenarios. SQL is taught as a "language of questions" — you have business questions, SQL is how you ask a database to answer them.

## 10-Week Course Outline

| Week | Topic |
|------|-------|
| 1 | Database Foundations |
| 2 | Relational Modeling |
| 3 | SQL Basics |
| 4 | SQL Aggregation (window functions, CASE, ROLLUP/CUBE, CTEs) |
| 5 | SQL Joins (FULL OUTER, CROSS, SELF, set operations, anti-joins) |
| 6 | Database Design (normalization 1NF/2NF/3NF, constraints, views, UPDATE/DELETE) |
| 7 | Query Performance & Indexing |
| 8 | Transactions & ACID |
| 9 | Project Integration |
| 10 | Review & Modern Data |

## Files in This Folder

### Weeks 1–3 Materials
- `orders_data.csv` — 20-row retail orders dataset (6 customers, 6 products, 3 categories)
- `plot_helpers.py` — Decoupled matplotlib plotting functions (plot_bar, plot_hbar, plot_pie, plot_grouped_bar). Students import these; they never need to read the plotting code.
- `OMIS105_Weeks_1_3.ipynb` — Comprehensive notebook: SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, normalization (flat CSV → 3 tables), JOINs (INNER, LEFT), GROUP BY, HAVING, subqueries, plus 6 plots. ~103 cells.
- `OMIS105_First_3_Weeks_Teaching_Plan.md` — Lecture-by-lecture teaching plan (6 lectures × 2 hours), discussion points, homework assignments, teaching principles.

### Weeks 4–6 Materials
- `company_data.csv` — 30-row tech company dataset (30 employees, 5 departments, with manager_id for self-joins, NULL dept_ids for FULL OUTER JOIN scenarios)
- `OMIS105_Weeks_4_6.ipynb` — Comprehensive notebook: window functions, ranking, LAG/LEAD, running totals, CASE, ROLLUP/CUBE, CTEs, FULL OUTER JOIN, CROSS JOIN, SELF JOIN, UNION/INTERSECT/EXCEPT, anti-joins, normalization (1NF/2NF/3NF with bad/good examples), constraints, views, UPDATE/DELETE. ~117 cells.
- `OMIS105_Weeks_4_6_Lecture_Notes.md` — Lecture notes for 6 lectures (7–12), discussion guides, assessment strategy.

## Data Design Principles

- **Small but rich:** 10–30 rows per table. Enough for meaningful queries, small enough for students to see the full picture.
- **Intentional imperfections:** NULL dept_ids (3 unassigned employees), empty departments (Legal has 0 employees), manager_id self-references — all designed to teach specific JOIN behaviors.
- **Business relevance:** Retail orders (weeks 1–3) and tech company (weeks 4–6) — scenarios business students recognize.

## Notebook Conventions

- All notebooks use **in-memory DuckDB** (`duckdb.connect(database=':memory:')`) — no files on disk, re-runnable from top to bottom any number of times.
- SQL is written inside `con.execute("""...""").fetchdf()` — returns a pandas DataFrame that Jupyter renders as a table.
- Python comments use `#`, not `--` (SQL comment syntax causes SyntaxError in Python code cells).
- Column aliases defined in SELECT cannot be used in WHERE (SQL execution order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY).
- Plotting is decoupled into `plot_helpers.py` — notebook cells call one-liners like `plot_bar(df, x='col', y='col', title='...')`.
- `CREATE TEMP TABLE` cannot have FOREIGN KEY references to main-schema tables in DuckDB. Use `CREATE TABLE` instead when foreign keys are needed.

## Known Issues / Fixes Applied

- **`--` comments in code cells:** SQL-style `--` comments on bare Python lines cause SyntaxError. All converted to `#`.
- **Alias in WHERE:** `WHERE order_total > 100` fails because WHERE runs before SELECT. Fixed to `WHERE unit_price * quantity > 100`. An explanation cell with the SQL execution order diagram was added.
- **TEMP TABLE + FOREIGN KEY:** `CREATE TEMP TABLE` with `REFERENCES departments(dept_id)` throws BinderException in DuckDB (cross-schema FK not supported). Fix: use `CREATE TABLE` instead.

## Teaching Philosophy

1. **Business first, syntax second.** Every concept starts with a business question.
2. **Live coding, not slides.** 90% of class time in Jupyter.
3. **Errors are learning.** Let students see and debug errors.
4. **Pair work for practice.** One types, one navigates, switch halfway.
5. **Spiral, don't stack.** Each week revisits previous concepts in new contexts.
6. **Keep schemas small.** 2–3 tables, 10–30 rows. Clarity beats complexity.

## Other OMIS 105 Materials (outside this folder)

Located in `/Users/max/mp/santa_clara_univ/OMIS_105/`:
- `data_stories/Python_and_DuckDB/` — Standalone Python+DuckDB CRUD demos (persistent and in-memory)
- `data_stories/CRUD_100_10_rows/` — CRUD notebook with 10 employees
- `data_stories/CRUD_100_10_rows_with_images/` — Same CRUD notebook with avatar image_url column added
- Software installation kit in `software_installation/`:
  - `1.Install_Python_MacBook.md` — Mac Python install guide
  - `1.Install_Python_Windows.md` — Windows Python install guide
  - `2.Setup_Software.py` — Auto-installs DuckDB, Jupyter, Pandas + verifies
  - `3.Setup_Verification.ipynb` — Final verification notebook
