# Weekly Reviews

Cumulative review notebooks and lecture notes for
**OMIS 105 — Introduction to Database Management Systems**.

These materials consolidate multiple weeks into comprehensive
notebooks with accompanying lecture notes. Use them for review
sessions, exam preparation, or as a reference during later weeks.

## Files in This Folder

### Weeks 1–3: Database Foundations, Relational Modeling & SQL Basics

| File | Description |
|------|-------------|
| `weeks_1_3_notebook.py` | Marimo notebook: SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, normalization, JOINs, GROUP BY, HAVING, subqueries, plots |
| `weeks_1_3_lecture_notes.md` | Lecture plan (6 sessions × 2 hours) with discussion points and homework |
| `orders_data.csv` | 20-row retail orders dataset (6 customers, 6 products, 3 categories) |

### Weeks 4–6: Aggregation, Joins & Database Design

| File | Description |
|------|-------------|
| `weeks_4_6_notebook.py` | Marimo notebook: window functions, CASE, CTEs, FULL/CROSS/SELF JOINs, set operations, normalization (1NF/2NF/3NF), constraints, views |
| `weeks_4_6_lecture_notes.md` | Lecture notes (6 sessions) with discussion guides |
| `company_data.csv` | 30-row tech company dataset (30 employees, 5 departments) |

### Weeks 7–8: Window Functions, Performance, Transactions & ACID

| File | Description |
|------|-------------|
| `weeks_7_8_notebook.py` | Marimo notebook: ROW_NUMBER, RANK, PARTITION BY, EXPLAIN, indexes, sargable predicates, CTEs, BEGIN/COMMIT/ROLLBACK, CHECK/NOT NULL constraints, audit logging |
| `weeks_7_8_lecture_notes.md` | Lecture notes (4 sessions) with discussion guides |

### Weeks 9–10: CTEs, Subqueries, Advanced Windows & Modern DuckDB

| File | Description |
|------|-------------|
| `weeks_9_10_notebook.py` | Marimo notebook: chained CTEs, correlated subqueries, EXISTS/IN, LAG/LEAD, running totals, moving averages, DENSE_RANK, NTILE, FIRST_VALUE, JSON extraction, PIVOT, LIST/UNNEST, STRFTIME, CROSS JOIN |
| `weeks_9_10_lecture_notes.md` | Lecture notes (4 sessions) with discussion guides |

### Shared

| File | Description |
|------|-------------|
| `plot_helpers.py` | Matplotlib plotting functions (plot_bar, plot_hbar, plot_pie, plot_grouped_bar) |
| `marimo_template.py` | Marimo notebook template for creating new notebooks |

## Dataset Summary

| Weeks | Domain | Tables | Key Features |
|-------|--------|--------|-------------|
| 1–3 | Retail orders | orders (flat CSV → normalized) | 20 rows, 6 customers, 6 products |
| 4–6 | Tech company | employees, departments (flat CSV → normalized) | 30 employees, NULLs for OUTER JOIN, self-referencing manager_id |
| 7–10 | CloudMetrics SaaS | plans, customers, payments, support_tickets, accounts, events, kpi_targets | 10 companies, JSON metadata, 3 subscription tiers, audit logging |

## Tech Stack

- **Database:** DuckDB (in-memory)
- **Notebooks:** Marimo (reactive Python notebooks)
- **Language:** Python 3 + SQL

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
