# Week 3 Review — Aggregation, Grouping & Subqueries

Collapse many rows into one number per group, chart it, and ask questions that need a query inside a query.

## Run It

```bash
cd weekly_reviews/week03-sql-basics
marimo edit week03_review_notebook.py
```

Run the command from inside this folder. The notebook resolves its data
directory relative to its own location, so it works from anywhere, but
Marimo is easiest to launch from here.

This notebook is self-contained: it rebuilds every table it needs. You do not have to run Week 2 first.

## Files

| File | Purpose |
|------|---------|
| `week03_review_notebook.py` | The review notebook — open this in Marimo |
| `week03_review_notes.md` | Teaching notes: timing, discussion prompts, homework |
| `data/orders_data.csv` | The dataset (20 retail orders) |
| `plot_helpers.py` | Matplotlib helpers — you never need to read this code |

## SQL Covered

`GROUP BY`, `HAVING`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `STRFTIME`, subqueries, charts

## Dataset

`data/orders_data.csv` — normalized into `customers`, `products`, and `sales` by the setup cells, then aggregated.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
