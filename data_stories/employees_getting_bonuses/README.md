# 💰 SQL Fundamentals — Employees Getting Bonuses

**OMIS-105 · Week 4 — SQL Aggregation** *(also usable in Week 3)*

A deliberately tiny story — **ten employees, one table, one notebook** — aimed at
business students who have never written SQL. Subtitled *"A Beginner's Guide for
Business Students"*, and it means it.

---

## Run it

```bash
marimo edit SQL_Fundamentals_with_DuckDB_marimo.py
```

| File | Role |
|---|---|
| `SQL_Fundamentals_with_DuckDB_marimo.py` | The notebook |
| `employees.csv` | 10 employees |

The database is **in-memory**, so nothing is written to disk and the notebook can be
re-run freely.

---

## What it covers

It starts from nothing and builds up:

- Installing DuckDB and opening a connection
- Filtering rows with `WHERE`
- Grouping with `GROUP BY`
- Filtering **groups** with `HAVING`
- A first look at ranking

**Ten rows means every result can be checked by hand.** If the notebook says three
employees earn over $70,000, a student can count them and confirm it — which is the
fastest way to build trust in a new tool.

---

## The bonus question

The framing is a business one: *who gets a bonus?* That turns an abstract `WHERE`
clause into a decision with consequences —

```sql
SELECT emp_name, salary
FROM employees
WHERE salary > 70000;        -- ...and everyone below this line does not get one
```

Why that framing helps:

- Changing `70000` changes **who gets a bonus**.
- So the query is not a maths exercise — it is a **decision with consequences**.
- For students who find SQL abstract, this is the useful reframing: **a query is a
  policy**, and someone has to defend where the line goes.

---

## When to use it

| Situation | Better choice |
|---|---|
| Students have never written SQL | **This one** |
| You want CRUD (insert/update/delete) | `CRUD_100_10_rows/` |
| You want aggregation on real volume | `super_stores_sales/` or `book_ratings/` |

It is the gentlest aggregation story here, and correspondingly the least ambitious.
Use it as a first exposure or a confidence-builder, not as the main Week 4 material.
