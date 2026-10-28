# Week 7 — Subqueries: A Query Inside a Query

📦 **[Download Week 7 as a ZIP](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week07-subqueries.zip)** — this week's lectures and review, in one file. No git needed.

A **subquery** is a `SELECT` written inside another SQL statement. It
lets you answer a question in two steps: first find a value or a list,
then use it. For example: "Which products cost more than the average
price?"

## The Data: A Tiny Online Store 🛒

Only three tables, small enough to check every answer by eye:

```
customers ──< orders >── products
```

| Table | Rows | Worth knowing |
|---|---|---|
| `customers` | 8 | George Brown and Hana Sato never ordered |
| `products` | 8 | Blender and Standing Desk were never ordered |
| `orders` | 14 | Order 12 is a guest order: `customer_id` is `NULL` |

That one `NULL` sets up the most important trap of the week:
`NOT IN` returns **zero rows** when its list contains a `NULL`.

## Session 1 — The Basics

- [`slides_1.md`](slides_1.md) — slide deck
- [`demo1.py`](demo1.py) — Marimo notebook, from the most basic step up:
  1. A two-step question solved by hand, then with one subquery
  2. **Scalar subqueries** (one value) in `WHERE` and in `SELECT`
  3. **List subqueries** with `IN` and `NOT IN`
  4. Nested subqueries, with a slider that runs them **inside-out**
  5. The `NOT IN` + `NULL` trap, with a switch that adds or removes
     the `NULL`
  6. Two real DuckDB errors: an aggregate in `WHERE`, and a scalar
     subquery that returns too many rows

## Session 2 — Going Further

- [`slides_2.md`](slides_2.md) — slide deck
- [`demo2.py`](demo2.py) — Marimo notebook: `EXISTS` and `NOT EXISTS`,
  subqueries in `FROM` (derived tables), **correlated** subqueries
  (with a picker that shows how one row is decided), subquery vs. JOIN,
  and CTEs (`WITH`)

## Lab and Quiz

- [`lab07_student.md`](lab07_student.md) — **the week's lab**: 10
  questions, 30 points, from basic to advanced, with the expected row
  count for each one
- [`lab07_student_marimo.py`](lab07_student_marimo.py) — the same lab as a Marimo
  notebook: the data is loaded for you; replace each placeholder query
- [`lab07_instructor_marimo.py`](lab07_instructor_marimo.py) — the notebook with answers,
  real results, and a short explanation for each question
- [`quiz.md`](quiz.md) — 10 multiple-choice questions

## Files in This Folder

| File | What It Is |
|------|-----------|
| `slides_1.md`, `slides_2.md` | Marp slide decks — one per session |
| `demo1.py`, `demo2.py` | Live-demo Marimo notebooks — one per session |
| `lab07_student.md` | The lab, with blanks to fill in |
| `lab07_student_marimo.py`, `lab07_instructor_marimo.py` | The lab as Marimo notebooks — without and with answers |
| `quiz.md` | Short quiz |
| `data/` | `customers.csv`, `products.csv`, `orders.csv` |

Run the notebooks from inside this folder:

```bash
cd weekly_lectures/week07-subqueries
marimo edit demo1.py
```

## Before You Start

You should be comfortable with `GROUP BY` (Week 4) and joins
(Weeks 5–6). The "find what is missing" questions from Week 6
(`LEFT JOIN ... WHERE ... IS NULL`) come back this week, answered a
second way with `NOT EXISTS`.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
