# Your First JOIN — The Magic of `INNER JOIN`

The **first** lesson on joins. It teaches one idea only: `INNER JOIN`.
Two tiny tables, one shared column, and one query that answers a
question no single table can answer.

## The Story

**Bronco Brew** is a small coffee shop near campus. The manager asks:
*"Who bought what — and where do they live?"*

- `orders` knows **what** was sold, but only has a `customer_id` number.
- `customers` knows **who** each person is: name and city.

Neither table can answer the question alone. `INNER JOIN` puts the
matching rows side by side, and the answer appears.

## File Structure

```
joins_for_first_time/
├── README.md         # this file
├── notebook.py       # Marimo notebook: 10 SQL queries, 1 chart, 2 interactive demos
└── plot_helpers.py   # the chart and the "matchmaker" view used by notebook.py
```

The tables are built **inside the notebook** (in memory), so there is
no database file to create first.

## Tables

| Table | Rows | Columns | What it holds |
|-------|-----:|---------|----------------|
| `customers` | 5 | `customer_id`, `name`, `city` | Maya, Omar, Sofia, Leo, Priya (IDs 101–105) |
| `orders`    | 6 | `order_id`, `customer_id`, `item`, `price` | coffee and pastries, $3.50–$6.00 |

`orders.customer_id` (foreign key) points to `customers.customer_id`
(primary key). That shared column is what we join on.

Two details are there on purpose:

- **Maya and Sofia each have 2 orders**, so each appears in 2 result rows.
- **Leo has no orders**, so he does not appear after the join. This
  teaches the one rule: `INNER JOIN` keeps only rows that match.

## What's in the Notebook

| Part | Queries | What happens |
|------|---------|--------------|
| 1. Meet the data | Q1–Q2 | Look at each table. Find the shared column. |
| 2. The problem | Q3 | Look up one customer by hand — and see why that does not scale. |
| 3. The magic spell | Q4 | One `INNER JOIN` answers everything. A **before/after switch** shows the change. |
| 4. How the magic works | — | An **interactive matchmaker**: pick an order and watch it compared with every customer. |
| 5. Anatomy of the spell | Q5 | Every part of the query, explained. Table aliases. |
| 6. Put the magic to work | Q6–Q9 | `WHERE`, `GROUP BY`, `SUM` after a join, plus a before/after chart. |
| 7. The one rule | Q10 | Where is Leo? `INNER JOIN` keeps only matches. |
| 8. Common mistakes | — | Three real DuckDB errors and their fixes. |
| 9. Cheat sheet & practice | — | A template and 5 exercises with hidden solutions. |

Every query cell is a **pure SQL cell**.

## How to Run

From this folder:

```bash
marimo edit notebook.py
```

To check that every cell runs (no browser):

```bash
MPLBACKEND=Agg python3 notebook.py
```

## After This

Next, open [`../joins_with_emps_depts/`](../joins_with_emps_depts/).

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
