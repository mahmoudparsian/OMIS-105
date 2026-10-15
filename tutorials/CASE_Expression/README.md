# SQL's `CASE` Expression — Step by Step

* A beginner-friendly tutorial on SQL's `CASE` expression, in DuckDB.
* It assumes you have **never seen** `CASE` before.
* It moves in three levels: **Basic → Basic+ → Intermediate**.
* All examples use one tiny online-store database (2 tables, 19 rows),
so you can check every result by eye.

## Files

| File | What it is | How to use it |
|------|------------|---------------|
| [`case_expression_tutorial_01.md`](case_expression_tutorial_01.md) | The written tutorial: every query, with its real DuckDB result shown below it | Read it on GitHub, or follow along in the DuckDB shell |
| [`case_expression_tutorial_02.md`](case_expression_tutorial_02.md) | The written tutorial: every query, with its real DuckDB result shown below it | Read it on GitHub, or follow along in the DuckDB shell |
| [`case_expression_tutorial_03.md`](case_expression_tutorial_03.md) | The written tutorial: every query, with its real DuckDB result shown below it | Read it on GitHub, or follow along in the DuckDB shell |
| [`case_expression_notebook.py`](case_expression_notebook.py) | The same lessons as a Marimo notebook — run and change every query yourself | `marimo edit case_expression_notebook.py` |

The two files use the **same lesson IDs** (B1, P3, I2, ...), so you can
read a lesson in one and run it in the other.

## What You Will Learn

| Part | Level | Lessons |
|------|-------|---------|
| 1 | Basic | **B1** your first `CASE` (two outcomes) · **B2** more than two outcomes · **B3** the first match wins · **B4** what happens without `ELSE` · **B5** the short ("simple") `CASE` form |
| 2 | Basic+ | **P1** the wrong-order trap · **P2** `AND` / `IN` / `BETWEEN` inside `WHEN` · **P3** `CASE` and `NULL` · **P4** `CASE` that returns numbers · **P5** `CASE` in `ORDER BY` · **P6** the "same type" rule (with the real error) |
| 3 | Intermediate | **I1** `GROUP BY` a `CASE` · **I2** conditional counting with `SUM(CASE ...)` · **I3** conditional sums with a `JOIN` · **I4** customer segments from totals · **I5** safe division · **I6** `CASE` inside `UPDATE` |

Both files end with a list of common mistakes, a cheat sheet, and
5 practice exercises with solutions.

## The Sample Data

```
products (product_id, product_name, category, price, stock)   -- 8 rows
orders   (order_id, customer, product_id, quantity, status, order_date)   -- 11 rows

orders.product_id → products.product_id
```

* `stock` has one `0` (sold out) and one `NULL` (unknown), on purpose.
* `status` is one of `shipped`, `pending`, `cancelled`, `returned`.

The tables are built inside the tutorial and the notebook (in-memory
DuckDB). There is no CSV or database file to download.

## Best-Fit Week

**Week 3 — SQL Basics** (`CASE`, computed columns). Part 3 also uses
`GROUP BY` (Week 2), `JOIN` (Weeks 4–5), and one short CTE
(Weeks 7 and 9), so it is good review later in the quarter, too.

## How to Run the Notebook

```bash
cd tutorials/CASE_Expression
marimo edit case_expression_notebook.py
```

Requirements: `duckdb`, `pandas`, and `marimo`
(see `software_installation/` if you have not installed them yet).

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
