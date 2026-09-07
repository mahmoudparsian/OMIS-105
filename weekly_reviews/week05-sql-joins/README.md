# Week 5 Review — Advanced Joins & Set Operations

Every remaining way to combine tables, including finding the rows that match nothing.

## Run It

```bash
cd weekly_reviews/week05-sql-joins
marimo edit week05_review_notebook.py
```

Run the command from inside this folder. The notebook resolves its data
directory relative to its own location, so it works from anywhere, but
Marimo is easiest to launch from here.

This notebook is self-contained: it rebuilds every table it needs. You do not have to run Week 4 first.

## Files

| File | Purpose |
|------|---------|
| `week05_review_notebook.py` | The review notebook — open this in Marimo |
| `week05_review_notes.md` | Teaching notes: timing, discussion prompts, homework |
| `data/company_data.csv` | The dataset (30-person tech company) |

## SQL Covered

`FULL OUTER JOIN`, `COALESCE`, `CROSS JOIN`, `SELF JOIN`, `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT`, `NOT EXISTS`, `NOT IN`

## Dataset

`data/company_data.csv` — the same company. NULL `dept_id`s, an empty department, and a self-referencing `manager_id` make the joins real.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
