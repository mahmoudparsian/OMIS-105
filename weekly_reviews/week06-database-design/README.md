# Week 6 Review — Database Design, Constraints & Views

Normalize formally (1NF → 3NF), enforce the design with constraints, and change data safely.

## Run It

```bash
cd weekly_reviews/week06-database-design
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

1NF, 2NF, 3NF, functional dependencies, `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK`, `CREATE VIEW`, `UPDATE`, `DELETE`

## Dataset

`data/company_data.csv` — the same company, plus small throwaway tables built in the notebook to demonstrate each normal form.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
