# CLAUDE.md — Weekly Reviews

## Purpose

Cumulative review materials for **OMIS 105 — Introduction to
Database Management Systems**, Fall 2026. Each review notebook
consolidates three weeks of SQL topics into a single
comprehensive Marimo notebook with lecture notes.

**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Tech stack:** Python · DuckDB · Marimo
**Audience:** Senior business students with zero prior SQL exposure.

## Files in This Folder

### Weeks 1–3 Materials

- `orders_data.csv` — 20-row retail orders dataset (6 customers,
  6 products, 3 categories)
- `plot_helpers.py` — Matplotlib plotting functions (plot_bar,
  plot_hbar, plot_pie, plot_grouped_bar). Students import these;
  they never need to read the plotting code.
- `weeks_1_3_notebook.py` — Comprehensive Marimo notebook:
  SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, normalization
  (flat CSV → 3 tables), JOINs (INNER, LEFT), GROUP BY,
  HAVING, subqueries, plus plots.
- `weeks_1_3_lecture_notes.md` — Lecture-by-lecture teaching
  plan (6 lectures × 2 hours), discussion points, homework.

### Weeks 4–6 Materials

- `company_data.csv` — 30-row tech company dataset (30 employees,
  5 departments, with manager_id for self-joins, NULL dept_ids
  for FULL OUTER JOIN scenarios)
- `weeks_4_6_notebook.py` — Comprehensive Marimo notebook:
  window functions, ranking, LAG/LEAD, running totals, CASE,
  CTEs, FULL OUTER JOIN, CROSS JOIN, SELF JOIN, UNION/INTERSECT/
  EXCEPT, anti-joins, normalization (1NF/2NF/3NF), constraints,
  views, UPDATE/DELETE.
- `weeks_4_6_lecture_notes.md` — Lecture notes for Weeks 4–6
  with discussion guides.

### Template

- `marimo_template.py` — Marimo notebook template for creating
  new review notebooks.

## Data Design Principles

- **Small but rich:** 10–30 rows per table. Enough for meaningful
  queries, small enough for students to see the full picture.
- **Intentional imperfections:** NULL dept_ids (unassigned
  employees), empty departments (Legal has 0 employees),
  manager_id self-references — all designed to teach specific
  JOIN behaviors.
- **Business relevance:** Retail orders (Weeks 1–3) and tech
  company (Weeks 4–6) — scenarios business students recognize.

## Marimo Conventions

- All notebooks use in-memory DuckDB
  (`duckdb.connect(database=':memory:')`)
- SQL cells use `_df = mo.sql(f"""...""")` with bare `return`
- Markdown cells use `mo.md("""...""")` with `hide_code=True`
- Use `CREATE OR REPLACE TABLE` for re-runnability
- No Python comments (`#`) inside SQL cells — use `--` so
  Marimo renders them as native SQL cells

## Teaching Philosophy

1. **Business first, syntax second.** Every concept starts with
   a business question.
2. **Live coding, not slides.** Most class time in Marimo.
3. **Errors are learning.** Let students see and debug errors.
4. **Spiral, don't stack.** Each week revisits previous concepts
   in new contexts.
5. **Keep schemas small.** 2–3 tables, 10–30 rows. Clarity
   beats complexity.
