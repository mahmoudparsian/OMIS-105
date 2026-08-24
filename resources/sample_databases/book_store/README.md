# Bookstore Sample Database

A small, realistic **online bookstore** dataset for practicing SQL with
DuckDB. It has three tables — `books`, `customers`, `orders` — and comes
with two ready-to-run notebooks that walk through 27 SQL queries, from
simple filters to window functions.

Use this database to practice everything you learn in OMIS 105: filtering,
sorting, grouping, joins, subqueries, CTEs, and window functions — all on
data that looks and behaves like a real business dataset (it even has
duplicate rows, just like real data does).

## The Schema

| Table | What it holds | Key columns |
|---|---|---|
| `books` | One row per book title | `book_id`, `title`, `author`, `genre`, `published_year`, `price`, `stock` |
| `customers` | One row per customer | `customer_id`, `name`, `email`, `phone`, `city`, `country` |
| `orders` | One row per order | `order_id`, `customer_id`, `book_id`, `order_date`, `quantity`, `total_amount` |

How the tables connect:

- `orders.book_id` → `books.book_id`
- `orders.customer_id` → `customers.customer_id`

`orders` is a **fact table** — it records events (a purchase) and points to
the "who" and "what" of that event. `books` and `customers` are
**dimension tables** — they describe the things involved. This
fact/dimension pattern shows up in almost every real business database.

## Where the Data Came From

The original idea and the 22 starter SQL questions in
[`bookstore_queries.sql`](bookstore_queries.sql) come from a public MySQL
portfolio project,
[SQL-Data-Analytics-BookStore](https://github.com/Shahimti/SQL-Data-Analytics-BookStore).
We rebuilt it for this course on top of **DuckDB** instead of MySQL, and
grew the dataset so it behaves like a real, multi-year sales history:

- **`generate_data.py`** starts from 500 books, 500 customers, and 500
  orders, then:
  - Adds 7,000 new orders spread across 2023–2025 (1,000 in 2023, 2,000
    in 2024, 4,000 in 2025), with heavier sales in November and December
    and a few "whale" customers who buy far more than everyone else —
    just like a real store's sales pattern.
  - Adds a small number of **exact duplicate rows** to each CSV (25 in
    `books.csv`, 42 in `customers.csv`, 100 in `orders.csv`) to simulate
    the messy duplicates that show up in real-world data exports.
- **`build_bookstore_db.py`** reads the `data/` folder, loads each CSV
  into DuckDB, removes the duplicate rows with `SELECT DISTINCT`, and
  prints a before/after row count for every table. Its output is saved in
  [`build_bookstore_db.log`](build_bookstore_db.log).

After cleaning, the database holds:

| Table | Rows |
|---|---|
| `books` | 503 |
| `customers` | 504 |
| `orders` | 7,500 |

## Files in This Folder

| File | Purpose |
|---|---|
| `data/` | The three source CSV files (with duplicates left in, on purpose) |
| `generate_data.py` | Script that expanded and "messed up" the original 500-row CSVs |
| `build_bookstore_db.py` | Builds `bookstore.duckdb` from `data/`, deduplicating as it goes |
| `build_bookstore_db.log` | Saved output from the last time `build_bookstore_db.py` ran |
| `bookstore.duckdb` | The finished DuckDB database file |
| `bookstore_queries.sql` | The 22 original starter questions, as plain `.sql` |
| `bookstore_analytics.ipynb` | Jupyter notebook — 27 queries, explained, with charts |
| `build_notebook.py` | Script that generated `bookstore_analytics.ipynb` (kept for reference; you don't need to run it) |
| `bookstore_analytics_marimo.py` | Marimo notebook — the same 27 queries, as a reactive notebook |
| `plot_helpers.py` | Chart-drawing functions used by both notebooks (kept separate so notebook cells stay focused on SQL) |

## How to Run It

**Option A — Marimo notebook (recommended for this course).**
It loads the CSVs and removes duplicates itself, so there is nothing to
build first.

```bash
marimo edit bookstore_analytics_marimo.py
```

**Option B — Jupyter notebook.**
This one reads the already-built `bookstore.duckdb` file, so build the
database first if you don't already have it:

```bash
python3 build_bookstore_db.py data/
jupyter notebook bookstore_analytics.ipynb
```

**Option C — Explore with SQL directly.** Open `bookstore.duckdb` in
[qStudio](https://www.timestored.com/qstudio/) or the DuckDB CLI and try
the questions in `bookstore_queries.sql`.

## What's Inside the Notebooks

Both notebooks work through the same **27 questions**, grouped by
difficulty. Each one states the business question, the SQL concept it
teaches, the query itself, and the result — with a chart when a picture
helps.

| Level | Count | You will practice |
|---|---|---|
| Basic | 5 | `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT` |
| Intermediate | 15 | `JOIN`, `LEFT JOIN` (anti-joins), date functions, subqueries |
| Advanced | 7 | `WITH` (CTEs), window functions (`LAG`, `NTILE`, running totals) |

A few examples of what you'll answer along the way: Which genres earn the
most revenue? Which books have never been ordered? Do 20% of customers
really generate 80% of revenue? How does revenue grow year over year?

## Try It Yourself

1. Pick a query in either notebook and change a column, a filter, or a
   `LIMIT` — see how the result and the chart react.
2. Write a new query that answers a question *you* have about this
   bookstore (for example: "which genre has the most expensive average
   book?").
3. Compare your SQL to the matching question in
   [`bookstore_queries.sql`](bookstore_queries.sql).

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
