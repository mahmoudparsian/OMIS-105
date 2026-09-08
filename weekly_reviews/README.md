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

## Tech Stack

- **Database:** DuckDB (in-memory)
- **Notebooks:** Marimo (reactive Python notebooks)
- **Language:** Python 3 + SQL

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
