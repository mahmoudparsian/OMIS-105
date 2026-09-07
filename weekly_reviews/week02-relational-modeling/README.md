# Week 2 Review — Relational Design & JOINs

See why one flat table is a problem, split it into three, and put it back together with `JOIN`.

## Run It

```bash
cd weekly_reviews/week02-relational-modeling
marimo edit week02_review_notebook.py
```

Run the command from inside this folder. The notebook resolves its data
directory relative to its own location, so it works from anywhere, but
Marimo is easiest to launch from here.

This notebook is self-contained: it rebuilds every table it needs. You do not have to run Week 1 first.

## Files

| File | Purpose |
|------|---------|
| `week02_review_notebook.py` | The review notebook — open this in Marimo |
| `week02_review_notes.md` | Teaching notes: timing, discussion prompts, homework |
| `data/orders_data.csv` | The dataset (20 retail orders) |

## SQL Covered

`CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`, `INSERT INTO`, `CREATE TABLE AS SELECT`, `INNER JOIN`, `LEFT JOIN`, `IS NULL`

## Dataset

`data/orders_data.csv` — the same 20 retail orders, split in the notebook into `customers`, `products`, and `sales`.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
