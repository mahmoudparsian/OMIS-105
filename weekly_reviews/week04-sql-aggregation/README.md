# Week 4 Review — Advanced Aggregation & Window Functions

Analyze data without collapsing it — window functions, ranking, `CASE`, subtotals, and CTEs.

## Run It

```bash
cd weekly_reviews/week04-sql-aggregation
marimo edit week04_review_notebook.py
```

Run the command from inside this folder. The notebook resolves its data
directory relative to its own location, so it works from anywhere, but
Marimo is easiest to launch from here.

This notebook is self-contained: it rebuilds every table it needs. You do not have to run Week 3 first.

## Files

| File | Purpose |
|------|---------|
| `week04_review_notebook.py` | The review notebook — open this in Marimo |
| `week04_review_notes.md` | Teaching notes: timing, discussion prompts, homework |
| `data/company_data.csv` | The dataset (30-person tech company) |

## SQL Covered

`OVER()`, `PARTITION BY`, `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`, running totals, `CASE`, `ROLLUP`, `CUBE`, CTEs

## Dataset

`data/company_data.csv` — a 30-person tech company, split into `departments`, `employees`, `projects`, and `assignments`.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
