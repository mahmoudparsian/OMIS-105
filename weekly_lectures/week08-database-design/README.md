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

A popular summary: every non-key column must depend on **the key, the
whole key, and nothing but the key.**

## Slides

- [`database_design_and_normalization.md`](database_design_and_normalization.md) —
  the week's deck. **Session 1:** why design matters, anomalies,
  functional dependencies, and 1NF, 2NF, and 3NF. **Session 2:**
  normalizing the ShopSmart table step by step in SQL, when to
  denormalize, and common design patterns. An optional appendix covers
  BCNF (not on the exams).

## Start Here: Step-by-Step Guides

Read these in order. Each guide explains one normal form; each examples
page gives you more small cases to practice on. The tables are small
enough to check by eye, and the DuckDB code can be copied and run.

| Step | Guide | More examples |
|---|---|---|
| 1NF | [`1nf_guide.md`](1nf_guide.md) — split lists with `STRING_SPLIT` and `UNNEST`, turn repeating columns into rows with `UNION ALL` or `UNPIVOT`, check a primary key with SQL | [`1nf_examples.md`](1nf_examples.md) — courses, phone numbers, order items, mechanics and cars; ends with a complete SQL walk-through (book club) |
| 2NF | [`2nf_guide.md`](2nf_guide.md) — composite keys, partial dependencies, the anomalies they cause, and how to split the table | [`2nf_examples.md`](2nf_examples.md) — employees on projects, store inventory, course sections, and three "is it in 2NF?" cases; ends with a complete SQL walk-through (conference workshops) |
| 3NF | [`3nf_guide.md`](3nf_guide.md) — transitive dependencies, an update anomaly you can watch happen, and how to split the table | [`3nf_examples.md`](3nf_examples.md) — categories, departments, ZIP codes, and a computed column; ends with a complete SQL walk-through (food deliveries) |

Two short DuckDB references go with the 1NF guide:

- [`duckdb_string_split_example.md`](duckdb_string_split_example.md) —
  `string_split` + `unnest`: one comma-separated column → many rows
- [`duckdb_normalization_functions.md`](duckdb_normalization_functions.md) —
  the DuckDB functions that help with 1NF, 2NF, and 3NF, on small tables

## Marimo Notebooks

- [`marimo_design_1nf_2nf.py`](marimo_design_1nf_2nf.py) — the main
  notebook: start from a bakery's spreadsheet, design the tables, fix
  1NF (repeating groups, lists, a primary key), check dependencies with
  SQL, see the anomalies, split into 2NF, and prove nothing was lost
- [`marimo_1nf_multi_values.py`](marimo_1nf_multi_values.py) — 1NF: a
  list of values in one cell
- [`marimo_1nf_repeating_columns.py`](marimo_1nf_repeating_columns.py) —
  1NF: repeating columns (`phone_number_1`, `2`, `3`)
- [`marimo_2nf_tutorial.py`](marimo_2nf_tutorial.py) — 2NF: removing
  partial dependencies
- [`marimo_3nf_tutorial.py`](marimo_3nf_tutorial.py) — 3NF: removing
  transitive dependencies (employees and departments)

Every notebook builds its tables in memory, so no data files are needed.
Run a notebook from inside this folder:

```bash
cd weekly_lectures/week08-database-design
marimo edit marimo_design_1nf_2nf.py
```

## The ShopSmart Example in the Slides

Session 2 of the deck normalizes `orders_denormalized` (100 rows: order,
customer, product, and category details in every row; Gina Turner
appears in 15 rows) into five tables. The file is
[`data/orders_denormalized.csv`](data/orders_denormalized.csv); run the
slides' SQL from inside this folder.

## Files in This Folder

| File | What It Is |
|------|-----------|
| `database_design_and_normalization.md` | The Marp slide deck (both sessions) |
| `1nf_guide.md`, `2nf_guide.md`, `3nf_guide.md` | Step-by-step guides with DuckDB code |
| `1nf_examples.md`, `2nf_examples.md`, `3nf_examples.md` | More small before/after examples |
| `duckdb_string_split_example.md`, `duckdb_normalization_functions.md` | Short DuckDB function references |
| `marimo_design_1nf_2nf.py` | The main Marimo notebook (design, 1NF, 2NF) |
| `marimo_1nf_*.py`, `marimo_2nf_tutorial.py`, `marimo_3nf_tutorial.py` | Short Marimo tutorials, one per normal form |
| `data/orders_denormalized.csv` | The ShopSmart table the slides normalize (100 rows) |

## Before You Start

You should be comfortable with primary and foreign keys (Week 2),
`GROUP BY` and `HAVING` (Week 4), and joins (Weeks 5–6). This week,
`GROUP BY … HAVING COUNT(…) > 1` becomes a tool for **checking a
design**, and a JOIN is how you put the split tables back together.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
