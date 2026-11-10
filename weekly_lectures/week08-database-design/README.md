# Week 8 — Database Design & Normalization

📦 **[Download Week 8 as a ZIP](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week08-database-design.zip)** — this week's lectures and review, in one file. No git needed.

Until now, the tables were given to you. This week you decide **which
tables to create**. A bad design stores the same fact many times, and
every copy is a chance for a mistake. **Normalization** is a
step-by-step way to split a table so that each fact is stored **once**:

| Normal form | The rule, in one line |
|---|---|
| **1NF** | One value per cell, no repeating groups, and a primary key |
| **2NF** | Every non-key column depends on the **whole** key (not part of it) |
| **3NF** | Every non-key column depends on **nothing but** the key |

## The Data: ShopSmart 🛍️

The folder `data/` holds one messy table and the clean design it
becomes:

| File | Rows | What it is |
|---|---|---|
| `orders_denormalized.csv` | 100 | **Everything in one table**: order, customer, product, and category details in every row |
| `customers.csv`, `categories.csv`, `products.csv`, `orders.csv`, `order_items.csv` | 40, 8, 64, 200, 607 | The normalized ShopSmart tables |
| `suppliers.csv`, `product_suppliers.csv`, `reviews.csv` | 10, 90, 150 | More ShopSmart tables (a many-to-many example) |

In `orders_denormalized.csv`, Alice Smith's name and email are repeated
in every row of her order, and Gina Turner appears in 15 rows.

## Start Here: Step-by-Step Guides

Read these in order. Each one has small tables you can check by eye,
and DuckDB code you can copy and run.

1. [`1nf_guide.md`](1nf_guide.md) — First Normal Form: split lists
   with `STRING_SPLIT` and `UNNEST`, turn repeating columns into rows
   with `UNION ALL` or `UNPIVOT`, and check a primary key with SQL
2. [`1nf_examples.md`](1nf_examples.md) — four more 1NF examples
   (courses, phone numbers, order items, mechanics and cars)
3. [`2nf_guide.md`](2nf_guide.md) — Second Normal Form: composite keys,
   partial dependencies, the anomalies they cause, and how to split
   the table in DuckDB

## Slides

- [`01_database_design_and_normalization.md`](01_database_design_and_normalization.md) —
  the short deck: why design matters, anomalies, functional
  dependencies, and the intuition behind 1NF, 2NF, and 3NF
- [`02_database_design_and_normalization.md`](02_database_design_and_normalization.md) —
  the full deck: types of dependencies, 1NF through BCNF, normalizing
  ShopSmart step by step in SQL, and when to denormalize

## Demo Notebooks

- [`demo1.py`](demo1.py) — a first look: a tiny `raw_orders` table
  (3 rows) and the first split into `customers` and `orders`
- [`demo2.py`](demo2.py) — the full walk-through on ShopSmart: find the
  redundancy, check functional dependencies with SQL, then split the
  table into 2NF and 3NF

## Lab and Quiz

- [`lab08_student.md`](lab08_student.md) — the week's companion lab on
  `orders_denormalized`: 12 questions, 75 points (dependencies,
  anomalies, normalization, queries on the result)
- [`lab08_student_marimo.py`](lab08_student_marimo.py) — the same lab as
  a Marimo notebook
- [`lab08_instructor_marimo.py`](lab08_instructor_marimo.py) — the
  notebook with answers
- [`quiz.md`](quiz.md) — 5 short review questions

## Files in This Folder

| File | What It Is |
|------|-----------|
| `1nf_guide.md`, `1nf_examples.md`, `2nf_guide.md` | Step-by-step guides with DuckDB code |
| `01_…`, `02_database_design_and_normalization.md` | Marp slide decks |
| `demo1.py`, `demo2.py` | Live-demo Marimo notebooks |
| `lab08_student.md` | The companion lab, with blanks to fill in |
| `lab08_student_marimo.py`, `lab08_instructor_marimo.py` | The lab as Marimo notebooks — without and with answers |
| `quiz.md` | Short quiz |
| `lab.md`, `notes.md`, `solution.sql` | Short outline notes |
| `data/` | The ShopSmart CSV files |

Run the notebooks from inside this folder:

```bash
cd weekly_lectures/week08-database-design
marimo edit demo2.py
```

## Before You Start

You should be comfortable with primary and foreign keys (Week 2),
`GROUP BY` and `HAVING` (Week 4), and joins (Weeks 5–6). This week,
`GROUP BY … HAVING COUNT(…) > 1` becomes a tool for **checking a
design**, and a JOIN is how you put the split tables back together.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
