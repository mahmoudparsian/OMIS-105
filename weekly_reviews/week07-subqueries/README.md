# Week 7 Review — Subqueries

📦 **[Download Week 7 as a ZIP](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week07-subqueries.zip)** — this week's lectures and review, in one file. No git needed.

A query inside a query — from one value, to a list, to a table, to a subquery that runs once per row.

## Run It

```bash
cd weekly_reviews/week07-subqueries
marimo edit week07_review_notebook.py
```

Run the command from inside this folder. The notebook resolves its data
directory relative to its own location, so it works from anywhere, but
Marimo is easiest to launch from here.

This notebook is self-contained: it rebuilds every table it needs. You do not have to run Week 6 first.

## Files

| File | Purpose |
|------|---------|
| `week07_review_notebook.py` | The review notebook — open this in Marimo |
| `week07_review_notes.md` | Teaching notes: timing, discussion prompts, homework |
| `data/company_data.csv` | The dataset (30-person tech company) |

## SQL Covered

Scalar subqueries in `WHERE` and `SELECT`, `IN`, nested `IN`, `NOT IN` and the `NULL` trap, `NOT EXISTS`, `EXISTS`, subqueries in `FROM`, correlated subqueries, subquery vs. JOIN, CTEs (`WITH`), chained CTEs

## Dataset

`data/company_data.csv` — the same company as Weeks 4–6. Three employees have a `NULL` `dept_id`, which is exactly what makes `NOT IN` return zero rows for "departments with no employees".

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
