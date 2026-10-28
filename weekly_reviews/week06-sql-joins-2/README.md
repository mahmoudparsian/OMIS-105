# Week 6 Review — Joins II: Joins in Practice

📦 **[Download Week 6 as a ZIP](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week06-sql-joins-2.zip)** — this week's lectures and review, in one file. No git needed.

Choosing the right join, predicting its row count, and avoiding the mistakes that quietly give wrong answers.

## Run It

```bash
cd weekly_reviews/week06-sql-joins-2
marimo edit week06_review_notebook.py
```

Run the command from inside this folder. The notebook resolves its data
directory relative to its own location, so it works from anywhere, but
Marimo is easiest to launch from here.

This notebook is self-contained: it rebuilds every table it needs. You do not have to run Week 5 first.

## Files

| File | Purpose |
|------|---------|
| `week06_review_notebook.py` | The review notebook — open this in Marimo |
| `week06_review_notes.md` | Teaching notes: timing, discussion prompts, homework |
| `data/company_data.csv` | The dataset (30-person tech company) |

## SQL Covered

`INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN` row counts, anti-joins (`LEFT JOIN ... IS NULL`), `COALESCE`, the `ON` vs. `WHERE` trap, `COUNT(*)` vs. `COUNT(column)`, `COALESCE(SUM(...), 0)`, 3-table chains, self-joins

## Dataset

`data/company_data.csv` — the same company as Weeks 4–5. Three employees have no department, Legal has no employees, and 11 employees are on no project, so every join type returns a different row count (27 / 30 / 28 / 31).

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
