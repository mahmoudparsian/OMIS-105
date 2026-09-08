# Weekly Reviews

Cumulative review materials for
**OMIS 105 — Introduction to Database Management Systems**.

One self-contained folder per week, mirroring the layout of
[`weekly_lectures/`](../weekly_lectures). Each folder holds a Marimo
review notebook, teaching notes, and whatever data that week needs.
Nothing is shared between folders — you can copy a single week's folder
anywhere and it still runs.

## The Ten Weeks

| Week | Folder | Topic |
|------|--------|-------|
| 1 | [`week01-database-foundations/`](week01-database-foundations/) | Querying a single table |
| 2 | [`week02-relational-modeling/`](week02-relational-modeling/) | Relational design & JOINs |
| 3 | [`week03-sql-basics/`](week03-sql-basics/) | Aggregation, grouping & subqueries |
| 4 | [`week04-sql-aggregation/`](week04-sql-aggregation/) | Advanced aggregation & window functions |
| 5 | [`week05-sql-joins/`](week05-sql-joins/) | Advanced joins & set operations |
| 6 | [`week06-database-design/`](week06-database-design/) | Database design, constraints & views |
| 7 | [`week07-query-performance/`](week07-query-performance/) | Window functions & query performance |
| 8 | [`week08-transactions-acid/`](week08-transactions-acid/) | Transactions, ACID & constraints |
| 9 | [`week09-project-integration/`](week09-project-integration/) | CTEs, subqueries & advanced window functions |
| 10 | [`week10-review-modern-data/`](week10-review-modern-data/) | Modern DuckDB — JSON, PIVOT & lists |

## What Is in Each Folder

```
weekNN-topic/
├── README.md                    # What this week covers, how to run it
├── weekNN_review_notebook.py    # The Marimo review notebook
├── weekNN_review_notes.md       # Teaching notes: timing, discussion, homework
├── data/                        # CSV for that week (Weeks 1–6 only)
└── plot_helpers.py              # Matplotlib helpers (Week 3 only)
```

## Running a Review Notebook

```bash
cd weekly_reviews/week01-database-foundations
marimo edit week01_review_notebook.py
```

Every notebook is independent. It creates its own in-memory DuckDB
connection and builds every table it needs, so you can open Week 7
without having run Weeks 1–6.

## Datasets

| Weeks | Domain | Source | Tables |
|-------|--------|--------|--------|
| 1–3 | Retail orders | `data/orders_data.csv` (20 rows, flat → normalized) | `customers`, `products`, `sales` |
| 4–6 | Tech company | `data/company_data.csv` (30 rows, flat → normalized) | `departments`, `employees`, `projects`, `assignments` |
| 7–8 | CloudMetrics SaaS | Inline SQL (no CSV) | `plans`, `customers`, `payments`, `support_tickets`, `accounts`, `audit_log` |
| 9–10 | CloudMetrics SaaS (extended) | Inline SQL (no CSV) | `plans`, `customers`, `payments`, `events` (JSON), `kpi_targets` |

The Weeks 4–6 dataset has deliberate imperfections — NULL `dept_id`s, an
empty department, a self-referencing `manager_id` — so that OUTER JOINs,
SELF JOINs, and anti-joins have something real to find.

## Starting a New Review Notebook

Copy the week folder closest to what you need and edit it — the notebooks
are self-contained, so a copy runs immediately:

```bash
cp -R week07-query-performance week11-my-topic
```

A week folder is a better starting point than a blank template: it
already has the setup cell, the `con.execute()` pattern, the title and
summary cells, and a README to edit.

## The Self-Containment Rule

This is the point of the folder-per-week layout: **a week folder must run
on its own**, with no dependency on any sibling folder. If you add or move
anything, keep this true.

- Each notebook opens its own `duckdb.connect(database=":memory:")`.
- Each notebook builds *every* table it queries. Week 3 rebuilds the
  normalized tables Week 2 taught; Weeks 5–6 rebuild the company schema
  Week 4 built.
- CSVs are duplicated into the week folders that need them, never shared.
- The data path is resolved from the notebook's own location:

  ```python
  from pathlib import Path
  DATA_DIR = Path(__file__).parent / "data"
  ```

  and interpolated into the SQL f-string:
  `read_csv_auto('{DATA_DIR}/orders_data.csv')`.

## Notebook Conventions

SQL runs through `con.execute()`, not `mo.sql()`:

```python
import duckdb
con = duckdb.connect(database=":memory:")   # this cell returns (con,)
...
con.execute("CREATE OR REPLACE TABLE ...")  # DDL/DML: no .fetchdf()
con.execute("SELECT ...").fetchdf()         # a query cell ends with .fetchdf()
```

Every cell that touches the database takes `con` as a parameter
(`def _(con):`) — that is what wires it into Marimo's reactivity graph.
Markdown cells use `mo.md("""...""")` with `hide_code=True`, tables use
`CREATE OR REPLACE TABLE` for re-runnability, and SQL comments use `--`
rather than `#`, so Marimo renders the cell as native SQL.

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

> ⚠️ Never run `marimo check --fix` against this directory — it treats
> every `.md` file as a notebook and rewrites it, READMEs and teaching
> notes included. Name the `.py` files explicitly instead, or use plain
> read-only `marimo check`. See "Working in This Repository" in the
> [root README](../README.md).

## Dataset Design Principles

- **Small but rich:** 10–30 rows per table. Enough for meaningful
  queries, small enough for students to verify by eye.
- **Intentional edge cases:** NULL `dept_id`s, an empty department, a
  self-referencing `manager_id`, failed and refunded payments,
  unresolved tickets, JSON with varying fields.
- **Business relevance:** SaaS metrics — MRR, churn, customer lifetime
  value — are exactly what analysts compute daily.

## Teaching Philosophy

1. **Business first, syntax second.** Every concept starts with a
   business question.
2. **Live coding, not slides.** Most class time is spent in Marimo.
3. **Errors are learning.** Let students see and debug real errors.
4. **Spiral, don't stack.** Each week revisits earlier concepts in new
   contexts.
5. **Keep schemas small.** 2–5 tables, 10–30 rows. Clarity beats
   complexity.

## Tech Stack

- **Database:** DuckDB (in-memory)
- **Notebooks:** Marimo (reactive Python notebooks)
- **Language:** Python 3 + SQL

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
