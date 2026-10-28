# Week 9 Review — Window Functions & Query Performance

📦 **[Download Week 9 as a ZIP](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week09-query-performance.zip)** — this week's lectures and review, in one file. No git needed.

Rank and compare rows without collapsing them, then look at what the database actually does with your query.

## Run It

```bash
cd weekly_reviews/week09-query-performance
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

`ROW_NUMBER`, `RANK`, `PARTITION BY`, `AVG() OVER`, `EXPLAIN`, `CREATE INDEX`, sargable predicates, CTEs

## Dataset

CloudMetrics SaaS — created inline in SQL. `plans`, `customers`, `payments`, `support_tickets`. No CSV needed.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
