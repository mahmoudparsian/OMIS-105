# Week 9 Review — CTEs, Subqueries & Advanced Window Functions

Multi-step analysis: name intermediate results, nest queries, and use the full window-function toolkit.

## Run It

```bash
cd weekly_reviews/week09-project-integration
marimo edit week09_review_notebook.py
```

Run the command from inside this folder. The notebook resolves its data
directory relative to its own location, so it works from anywhere, but
Marimo is easiest to launch from here.

This notebook is self-contained: it rebuilds every table it needs. You do not have to run Week 8 first.

## Files

| File | Purpose |
|------|---------|
| `week09_review_notebook.py` | The review notebook — open this in Marimo |
| `week09_review_notes.md` | Teaching notes: timing, discussion prompts, homework |

## SQL Covered

`WITH ... AS`, chained CTEs, correlated subqueries, `EXISTS`, `IN`, `LAG`, `LEAD`, running totals, moving averages, `DENSE_RANK`, `NTILE`, `FIRST_VALUE`

## Dataset

CloudMetrics SaaS (extended) — created inline in SQL. `plans`, `customers`, `payments`, `events` (JSON metadata), `kpi_targets`.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
