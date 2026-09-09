# Sample Lab

A preview of what an in-class lab looks like in this course — a
self-contained Marimo notebook, not tied to any specific week.

| File | Description |
|------|-------------|
| [`sample_lab_student.py`](./sample_lab_student.py) | The lab students receive — setup is done for you; each question has an empty `con.execute(...)` cell to fill in |
| [`sample_lab_student_solution.py`](./sample_lab_student_solution.py) | A worked solution, provided for reference |
| `data/products.csv` | The dataset the lab queries |
| `data/expensive_products.csv` | A small reference file used by one of the questions |

## What it covers

**Lab 1: Getting Started with DuckDB and SQL Basics** — 16 questions
across 5 parts: exploration, filtering and sorting, aggregation,
computed columns, and a bonus challenge. Concepts: `SELECT`, `WHERE`,
`ORDER BY`, `LIMIT`, `LIKE`, `DISTINCT`, `COUNT`/`SUM`/`AVG`/`MIN`/`MAX`,
and `CASE` expressions.

## Running it

```bash
cd sample_lab
MPLBACKEND=Agg python3 sample_lab_student.py
```

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
