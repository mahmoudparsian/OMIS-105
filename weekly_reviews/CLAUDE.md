# CLAUDE.md — Weekly Reviews

## ⚠️ This file is NOT tracked — do not `git add` it

Untracked 2026-09-08 (commit `bed359f`) along with the root `CLAUDE.md`:
no AI-assistant files on GitHub. The reader-facing parts of this file —
the self-containment rule, notebook conventions, the verification
recipe, dataset design principles, and the teaching philosophy — now
live in `weekly_reviews/README.md`. Edit the README when the guidance
matters to a human.

## Purpose

Cumulative review materials for **OMIS 105 — Introduction to
Database Management Systems**, Fall 2026. **One self-contained folder
per week**, mirroring the layout of `weekly_lectures/`.

**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Tech stack:** Python · DuckDB · Marimo
**Audience:** Senior business students with zero prior SQL exposure.

## Structure

```
weekly_reviews/
├── README.md
├── CLAUDE.md                      # This file
├── week01-database-foundations/
├── week02-relational-modeling/
├── week03-sql-basics/
├── week04-sql-aggregation/
├── week05-sql-joins/
├── week06-sql-joins-2/            # new 2026-10-27 (company data)
├── week07-subqueries/             # new 2026-10-27 (company data)
├── week08-database-design/        # was week06 (renumbered 2026-10-27)
├── week09-query-performance/      # was week07
├── week10-transactions-acid/      # was week08
└── bonus/                         # old week09/week10, contents unchanged,
                                   # folders renamed week11/week12 (2026-10-27)
    ├── week11-project-integration/
    └── week12-review-modern-data/
```

Folder names match `weekly_lectures/` exactly, so the two trees line up
side by side.

Each week folder contains:

```
weekNN-topic/
├── README.md                    # What the week covers, how to run it
├── weekNN_review_notebook.py    # The Marimo review notebook
├── weekNN_review_notes.md       # Teaching notes: timing, discussion, homework
├── data/                        # CSV for that week (Weeks 1–8 only)
└── plot_helpers.py              # Matplotlib helpers (Week 3 only)
```

**2026-09-07:** these ten folders were split out of four cumulative
notebooks (`weeks_1_3_notebook.py`, `weeks_4_6_notebook.py`,
`weeks_7_8_notebook.py`, `weeks_9_10_notebook.py`) plus their four
lecture-notes files. The originals were deleted in the same change —
they are in Git history if you need them. Every `mo.sql()` cell was
converted to `con.execute()` during that split, so **all of
`weekly_reviews/` now follows the `con.execute()` convention**.

**2026-09-07:** `marimo_template.py` was deleted. It had sat unchanged
since the initial commit and could never have run — it created `orders`,
`orders_test`, and `sales` but queried `customers` and `products`, which
it never created. Nobody had noticed, which is a fair sign nobody used
it. To start a new review notebook, copy the closest week folder
(`cp -R week09-query-performance week11-my-topic`): it is self-contained,
already runs, and carries the conventions below.

## Self-Containment Rule

This is the point of the folder-per-week layout: **a week folder must
run on its own**, with no dependency on any sibling folder. If you add
or move anything, keep this true.

- Each notebook opens its own `duckdb.connect(database=":memory:")`.
- Each notebook builds *every* table it queries. Week 3 rebuilds the
  normalized tables that Week 2 taught; Weeks 5–8 rebuild the company
  schema that Week 4 built.
- CSVs are duplicated into the week folders that need them, not shared.
- The data path is resolved from the notebook's own location:

  ```python
  from pathlib import Path
  DATA_DIR = Path(__file__).parent / "data"
  ```

  and interpolated into the SQL f-string:
  `read_csv_auto('{DATA_DIR}/orders_data.csv')`.

## Weekly Topics

| Week | Review Topic | Key SQL |
|------|-------------|---------|
| 01 | Querying a single table | `SELECT`, `WHERE`, `IN`, `BETWEEN`, `LIKE`, `ORDER BY`, `LIMIT`, `DISTINCT`, `COUNT` |
| 02 | Relational design & JOINs | `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`, `INNER JOIN`, `LEFT JOIN`, `IS NULL` |
| 03 | Aggregation, grouping & subqueries | `GROUP BY`, `HAVING`, `SUM`/`AVG`/`MIN`/`MAX`, `STRFTIME`, subqueries, charts |
| 04 | Advanced aggregation | `OVER()`, `PARTITION BY`, `ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `CASE`, `ROLLUP`, `CUBE`, CTEs |
| 05 | Advanced joins & set operations | `FULL OUTER JOIN`, `CROSS JOIN`, `SELF JOIN`, `UNION`, `INTERSECT`, `EXCEPT`, anti-joins |
| 06 | Joins II — joins in practice | row counts per join type, anti-joins, `ON` vs. `WHERE`, `COUNT(col)`, `COALESCE(SUM)`, chains, self-joins |
| 07 | Subqueries | scalar, `IN`, nested `IN`, `NOT IN` + `NULL` trap, `NOT EXISTS`, `EXISTS`, derived tables, correlated, CTEs |
| 08 | Database design | 1NF/2NF/3NF, `NOT NULL`, `UNIQUE`, `CHECK`, `CREATE VIEW`, `UPDATE`, `DELETE` |
| 09 | Window functions & performance | `ROW_NUMBER`, `RANK`, `EXPLAIN`, `CREATE INDEX`, sargable predicates, CTEs |
| 10 | Transactions & ACID | `BEGIN`, `COMMIT`, `ROLLBACK`, `CHECK`, `NOT NULL`, `PRIMARY KEY`, audit logging |
| bonus (old 09) | CTEs, subqueries & advanced windows | Chained CTEs, correlated subqueries, `EXISTS`, `NTILE`, `FIRST_VALUE`, moving averages |
| bonus (old 10) | Modern DuckDB | `json_extract_string`, `PIVOT`, `LIST`, `UNNEST`, `STRFTIME`, `CROSS JOIN` |

## Datasets

| Weeks | Domain | Source | Tables |
|-------|--------|--------|--------|
| 1–3 | Retail orders | `data/orders_data.csv` (20 rows) | `customers`, `products`, `sales` |
| 4–8 | Tech company | `data/company_data.csv` (30 rows) | `departments`, `employees`, `projects`, `assignments` |
| 9–10 | CloudMetrics SaaS | Inline SQL | `plans`, `customers`, `payments`, `support_tickets`, `accounts`, `safe_accounts`, `audit_log` |
| Bonus (11–12) | CloudMetrics SaaS (extended) | Inline SQL | `plans`, `customers`, `payments`, `events` (JSON metadata), `kpi_targets` |

Design principles:
- **Small but rich:** 10–30 rows per table. Enough for meaningful
  queries, small enough for students to verify by eye.
- **Intentional edge cases:** NULL `dept_id`s, an empty department, a
  self-referencing `manager_id`, failed/refunded payments, unresolved
  tickets, JSON with varying fields.
- **Business relevance:** SaaS metrics (MRR, churn, customer lifetime
  value) are exactly what analysts compute daily.

## Marimo Conventions

- **SQL pattern: `con.execute()`, not `mo.sql()`.**

  ```python
  import duckdb
  con = duckdb.connect(database=":memory:")   # cell returns (con,)
  ...
  con.execute("CREATE OR REPLACE TABLE ...")  # DDL/DML: no .fetchdf()
  con.execute("SELECT ...").fetchdf()         # a query cell ends with .fetchdf()
  ```

  Every cell that touches the database takes `con` as a parameter
  (`def _(con):`) — that is what wires up Marimo's reactivity graph,
  since `con.execute()` does not register table names as Python
  variables the way `mo.sql()` did.
- Markdown cells: `mo.md("""...""")` with `hide_code=True`
- Use `CREATE OR REPLACE TABLE` for re-runnability
- No Python comments (`#`) inside SQL — use `--` so Marimo renders
  the cell as native SQL

## Verifying a Change

A review notebook is a runnable Python file. After editing one, run it
from its own folder (so the relative `data/` path resolves) and run it
**twice** — the second run is what catches a missing `CREATE OR REPLACE`:

```bash
cd weekly_reviews/weekNN-topic
MPLBACKEND=Agg python3 weekNN_review_notebook.py && \
MPLBACKEND=Agg python3 weekNN_review_notebook.py
```

Exit code 0 means every cell ran. Do this for any notebook you touch.
All 10 pass, twice, as of 2026-09-07.

**Before running `marimo check --fix`, read the "Marimo Tooling" section
in the root `CLAUDE.md`.** Pointed at this directory it rewrites every
`.md` file here — READMEs and notes included. Name `.py` files
explicitly instead.

## Teaching Philosophy

1. **Business first, syntax second.** Every concept starts with
   a business question.
2. **Live coding, not slides.** Most class time in Marimo.
3. **Errors are learning.** Let students see and debug errors.
4. **Spiral, don't stack.** Each week revisits previous concepts
   in new contexts.
5. **Keep schemas small.** 2–5 tables, 10–30 rows. Clarity
   beats complexity.

## Weeks 6–7 reviews (2026-10-27)

`week06_review_notebook.py` and `week07_review_notebook.py` were generated
from a script: the setup cells (company data load + normalization) are copied
**verbatim** from `week05_review_notebook.py`, so all company-data weeks build
identical tables. Every query was run in DuckDB 1.5.5 first; the markdown quotes
real numbers (27/30/28/31 join row counts, Mia > Leo, `NOT IN` → 0 rows).
If you change the week05 setup cells, the Week 6–7 numbers may change too.

## Weekly ZIP download links (2026-10-15)

Every `weekNN-*/README.md` here has a "📦 Download Week N as a ZIP"
line right under its H1, linking to
`https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/<folder>.zip`.
The ZIP bundles this folder as `review/` with the matching
`weekly_lectures/` folder as `lectures/`. Keep the line when rewriting
a README, and keep folder names in sync with `weekly_lectures/` — the
build pairs them by name. Bonus folders (`bonus/week11-*`, `bonus/week12-*`)
link to `bonus-<folder>.zip` instead. Details: root `CLAUDE.md`, "Weekly ZIP
Downloads".
