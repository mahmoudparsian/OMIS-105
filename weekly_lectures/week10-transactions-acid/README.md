# Week 10 — Transactions & ACID

📦 **[Download Week 10 as a ZIP](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week10-transactions-acid.zip)** — this week's lectures and review, in one file. No git needed.

A **transaction** is a group of SQL statements that the database treats as
**one unit**: either all of them take effect, or none of them do. Moving money
from Alice to Bob, placing an order, processing a return — each is several
statements that must happen **together**.

| Command | What it does |
|---|---|
| `BEGIN` | start a transaction |
| `COMMIT` | save every change since `BEGIN` |
| `ROLLBACK` | undo every change since `BEGIN` |

Without `BEGIN`, every statement is saved at once (**auto-commit**).

**ACID** names the four guarantees: **A**tomicity (all or nothing),
**C**onsistency (every declared rule holds), **I**solation (users at the same
time don't interfere), **D**urability (after `COMMIT`, the change survives a
crash).

## Session — December 1

1. [`transactions_are_explained.md`](transactions_are_explained.md) — the slide
   deck (94 slides). Almost every example is a **DuckDB session**: what you type
   at the `D ` prompt, and what DuckDB 2.0 answers (result tables and error
   messages, copied from real runs). **Part 1:** transactions and ACID on a
   two-row bank table (Alice $500, Bob $200) and a library: auto-commit, `BEGIN` /
   `COMMIT` / `ROLLBACK`, why one statement is already all or nothing, the
   **life of a transaction** (auto-commit → active → aborted), `UPDATE …
   RETURNING`, a `CREATE TABLE` undone by `ROLLBACK`, and durability tested with
   a database file and its write-ahead log. **Part 2:** the ShopSmart store with
   rules (`CHECK`, `REFERENCES`), an order and a return as transactions, the four
   concurrency problems, isolation levels, and the same four problems run in
   DuckDB with **two users** (`A> ` / `B> `). It ends with a **cheat sheet** and
   nine **"Check yourself"** questions (with answers) for the final exam.
2. [`transactions_demo_1.py`](transactions_demo_1.py) — Marimo notebook for
   Part 1: auto-commit, `COMMIT`, `ROLLBACK`, a failed statement that aborts the
   transaction, `COMMIT` after an error (saves nothing), `PRIMARY KEY` /
   `NOT NULL` / `CHECK`, a safe `transfer()` function, no `SAVEPOINT` in DuckDB,
   and durability tested with a database file.
3. [`transactions_demo_2.py`](transactions_demo_2.py) — Marimo notebook for
   Part 2 on ShopSmart (`data/`): one order = one transaction, a wrong product
   and too little stock (both rolled back), `place_order()`, `process_return()`
   (only `completed` orders; the refund is what the items cost, not the stored
   `total_amount`), and four experiments with **two users** on one database
   file: dirty read, non-repeatable read, phantom read, lost update.

Each notebook shows a **transcript** for every experiment: each SQL statement in
order, and what DuckDB answered (✅ or ❌ with the error message). Every section
starts again from the same data, so the sections can run in any order.

## December 3 — Course Review

The last class before the final exam reviews the whole course in one notebook:

- [`course_review_weeks_01_to_10.py`](course_review_weeks_01_to_10.py) — Weeks 1
  to 10 on the ShopSmart database (`data/`, all 9 tables, created **with** their
  keys), one section per week: first look (`SHOW TABLES`, `DESCRIBE`) → keys and
  relationships (1:N, M:N) → `SELECT` / `WHERE` / `NULL` / `ENUM` / CRUD with a
  sequence → `GROUP BY` / `HAVING` (with a chart) → `INNER` / `LEFT` joins → 3+
  tables, `RIGHT JOIN`, self-join → subqueries and a CTE (and the `NOT IN` trap) →
  1NF / 2NF / 3NF → `ROW_NUMBER` / `RANK` / `DENSE_RANK` and a **live top-N per
  category** (pick a category and N) → a transaction with `ROLLBACK`. It ends with
  a "Can you …?" checklist for the final exam.

For this week's topic on its own, see
[`../../weekly_reviews/week10-transactions-acid/`](../../weekly_reviews/week10-transactions-acid/).

## Files in This Folder

| File | What It Is |
|------|-----------|
| `transactions_are_explained.md` | Slide deck — Part 1 and Part 2, with real DuckDB sessions |
| `transactions_demo_1.py` | Part 1 notebook: the `accounts` table (bank) |
| `transactions_demo_2.py` | Part 2 notebook: ShopSmart orders, returns, two users |
| `course_review_weeks_01_to_10.py` | December 3: the whole course, Weeks 1–10, in one notebook |
| `data/` | ShopSmart CSVs: `products`, `orders`, `order_items` (used by `transactions_demo_2.py`), and `categories`, `customers`, `shipping`, `reviews`, `suppliers`, `product_suppliers` (all 9 used by the course review) |

Run the notebooks from inside this folder:

```bash
cd weekly_lectures/week10-transactions-acid
marimo edit transactions_demo_1.py
```

Every result in the slides and notebooks comes from running the SQL in DuckDB 2.0.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
