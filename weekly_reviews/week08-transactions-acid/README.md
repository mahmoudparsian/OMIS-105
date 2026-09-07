# Week 8 Review — Transactions, ACID & Constraints

Make a group of changes all-or-nothing, and let the database reject bad data on its own.

## Run It

```bash
cd weekly_reviews/week08-transactions-acid
marimo edit week08_review_notebook.py
```

Run the command from inside this folder. The notebook resolves its data
directory relative to its own location, so it works from anywhere, but
Marimo is easiest to launch from here.

This notebook is self-contained: it rebuilds every table it needs. You do not have to run Week 7 first.

## Files

| File | Purpose |
|------|---------|
| `week08_review_notebook.py` | The review notebook — open this in Marimo |
| `week08_review_notes.md` | Teaching notes: timing, discussion prompts, homework |

## SQL Covered

`BEGIN TRANSACTION`, `COMMIT`, `ROLLBACK`, ACID, `CHECK`, `NOT NULL`, `PRIMARY KEY`, audit logging

## Dataset

CloudMetrics SaaS — created inline in SQL, plus `accounts`, `safe_accounts`, and `audit_log` built during the exercises.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
