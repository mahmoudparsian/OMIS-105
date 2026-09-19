# Introduction to RDBMS with DuckDB

A hands-on, ~2.5-hour course that takes you from "what is a relational
database" to writing multi-table, multi-CTE SQL with window functions
— using
[marimo](https://marimo.io) reactive notebooks and
[DuckDB](https://duckdb.org) as an embedded, in-process SQL engine. No
server to install, no account to create: everything runs locally in
Python.

You don't need prior database experience. You do need a little Python
familiarity (you should be comfortable reading a `for` loop and calling
a function) — marimo itself is taught from scratch in notebook 1.

## Contents

1. [Setup](#1-setup)
2. [How to work through this course](#2-how-to-work-through-this-course)
3. [The dataset](#3-the-dataset)
4. [Syllabus](#4-syllabus)
5. [What you'll be able to do afterward](#5-what-youll-be-able-to-do-afterward)
6. [Folder contents](#6-folder-contents)
7. [Troubleshooting](#7-troubleshooting)
8. [After the course](#8-after-the-course)
9. [For instructors extending this course](#9-for-instructors-extending-this-course)

## 1. Setup

This course was built and tested against:

```
python        3.13
marimo        0.23.10
duckdb        1.5.5
pandas        2.2.3
```

If you're setting this up somewhere new:

```bash
pip install marimo duckdb pandas
```

No other setup, accounts, or servers required — DuckDB runs entirely
inside this Python process. Before opening any notebook, build the
shared course database (a one-time step — see
[The dataset](#3-the-dataset) below):

```bash
./create_database.sh
```

This calls `build_database()` in [`ecommerce_data.py`](./ecommerce_data.py),
which creates a new file, `ecommerce_database.duckdb`, in this folder,
runs the `CREATE TABLE` statements for all five tables (with their real
`PRIMARY KEY`/`FOREIGN KEY`/`UNIQUE`/`CHECK` constraints — see
notebook 02), and loads each one with generated sample data, seeded so
the numbers below are identical every time you run it:

| Table | Row count | Primary key | Foreign key(s) |
|---|---|---|---|
| `customers` | 30 | `customer_id` | — |
| `employees` | 6 | `employee_id` | `manager_id` → `employees.employee_id` (self-referencing) |
| `products` | 15 | `product_id` | — |
| `orders` | 80 | `order_id` | `customer_id` → `customers`, `employee_id` → `employees` |
| `order_items` | 192 | (`order_id`, `product_id`) composite | `order_id` → `orders`, `product_id` → `products` |

So each of the 30 customers places a handful of the 80 orders (via
`orders.customer_id`), and each order is a bundle of 1–4 line items in
`order_items` (1–5 units of a product per line) — that's why
`order_items`, at 192 rows, is the largest table: it's where `orders`
and `products` meet. The whole file is a build artifact (gitignored,
not committed) — delete it and re-run `./create_database.sh` any time
you want to reset it to this exact state.

Then confirm it worked:

```bash
python3 -c "import duckdb; con = duckdb.connect('ecommerce_database.duckdb', read_only=True); print(con.sql('SHOW TABLES'))"
```

You should see the five tables listed (`customers`, `employees`,
`orders`, `order_items`, `products`). If either command errors, fix the
underlying issue before opening notebook 1 — see
[Troubleshooting](#7-troubleshooting) below.

## 2. How to work through this course

Each notebook is a plain `.py` file. Open one for real, interactive
editing with:

```bash
marimo edit 01_setup_and_marimo_basics.py
```

This opens it in your browser. Work through it top to bottom — run
cells, drag sliders, edit the SQL exercise boxes, expand the solution
accordions **after** you've tried each exercise yourself. Then move to
the next file in order:

```bash
marimo edit 02_relational_model_and_keys.py
# ...and so on through 13_window_functions.py
```

Every notebook (from 2 onward) connects directly to the same shared,
pre-built `ecommerce_database.duckdb` file with the plain DuckDB API —
`duckdb.connect("ecommerce_database.duckdb", read_only=True)` (see
[`ecommerce_data.py`](./ecommerce_data.py) and the [Setup](#1-setup)
step above) — you can open any single one on its own without having
run the others first, though the material builds conceptually in order
and is meant to be done in sequence the first time through. Notebooks 08
and 10 deliberately insert/update/delete data as a teaching demo, so
they open the file read-write instead; 08's inserts are all designed to
violate a constraint and never actually commit, and 10 cleans up after
itself (both before and after its demos) so the shared file is always
back to its original state once the notebook finishes running.

When you're done with a notebook, `Ctrl+C` in the terminal stops its
`marimo edit` server before you open the next one (or just leave it
running and open the next file in a second terminal — each uses its own
port automatically).

If you'd rather just *view and interact* with a notebook without being
able to edit its code cells (e.g. projecting it for a class), use `run`
instead of `edit`:

```bash
marimo run 01_setup_and_marimo_basics.py
```

This serves the app-only view: markdown, outputs, and every interactive
exercise still work, but the underlying code cells are hidden and
locked.

## 3. The dataset

All thirteen notebooks share one small, fictional e-commerce database — a
shop with customers, employees, products, orders, and order line items.
It lives in a single file, `ecommerce_database.duckdb`, built by running
`./create_database.sh` (which calls `build_database()` in
`ecommerce_data.py`, a plain Python module — not a notebook). Because
the data is generated from a fixed random seed, re-running the script
always produces byte-for-byte identical contents. The file itself isn't
checked into the repo — build it locally before opening notebook 1.
You're welcome to open `ecommerce_data.py` and read how it works;
notebook 03 walks through the same ideas by hand.

```
customers(customer_id PK, first_name, last_name, email, city, state, signup_date)
employees(employee_id PK, first_name, last_name, title, manager_id FK -> employees)
products(product_id PK, product_name, category, unit_price, in_stock)
orders(order_id PK, customer_id FK, employee_id FK, order_date, ship_city)
order_items(order_id FK, product_id FK, quantity, unit_price)   -- composite PK
```

## 4. Syllabus

| # | Notebook | Covers | ~Time |
|---|---|---|---|
| 1 | [`01_setup_and_marimo_basics.py`](./01_setup_and_marimo_basics.py) | What marimo is, reactivity, UI elements, your first DuckDB query two ways | 10 min |
| 2 | [`02_relational_model_and_keys.py`](./02_relational_model_and_keys.py) | Relations/tuples/attributes, primary/foreign/composite keys, the course schema | 12 min |
| 3 | [`03_creating_tables_and_loading_data.py`](./03_creating_tables_and_loading_data.py) | `CREATE TABLE`, constraints, `INSERT ... VALUES` / `... SELECT`, in-memory vs. persistent DBs | 12 min |
| 4 | [`04_select_where_filter_sort.py`](./04_select_where_filter_sort.py) | `SELECT`, `WHERE`, `IN`/`BETWEEN`/`LIKE`/`NULL`, `ORDER BY`, `LIMIT`, parameterized queries | 12 min |
| 5 | [`05_joins.py`](./05_joins.py) | `INNER`/`LEFT`/`RIGHT`/`FULL OUTER`/`CROSS` joins, self-joins | 15 min |
| 6 | [`06_aggregation_group_by.py`](./06_aggregation_group_by.py) | `COUNT`/`SUM`/`AVG`/`MIN`/`MAX`, `GROUP BY`, `HAVING` | 12 min |
| 7 | [`07_subqueries_and_ctes.py`](./07_subqueries_and_ctes.py) | Subqueries in `WHERE`/`FROM`, CTEs (`WITH`), a first look at window functions | 12 min |
| 8 | [`08_constraints_and_data_integrity.py`](./08_constraints_and_data_integrity.py) | Watching PK/FK/UNIQUE/CHECK/NOT NULL block bad data, live; ACID overview | 10 min |
| 9 | [`09_normalization.py`](./09_normalization.py) | Update/insert/delete anomalies, 1NF/2NF/3NF, why the schema is shaped this way | 12 min |
| 10 | [`10_views_and_transactions.py`](./10_views_and_transactions.py) | `CREATE VIEW`, `BEGIN`/`COMMIT`/`ROLLBACK`, atomicity under a real failure | 10 min |
| 11 | [`11_duckdb_superpowers.py`](./11_duckdb_superpowers.py) | Querying CSV/Parquet files and pandas DataFrames directly, `EXPLAIN`, exporting | 10 min |
| 12 | [`12_capstone_project.py`](./12_capstone_project.py) | Five guided multi-step business questions + one you design yourself | 15 min |
| 13 | [`13_window_functions.py`](./13_window_functions.py) | Bonus deep dive: `ROW_NUMBER`/`RANK`/`DENSE_RANK`, running totals, `LAG`/`LEAD` | 15 min |

**Total: ~157 minutes** including reading time — budget roughly 2.5–3
hours if you work every exercise by hand before checking each solution
(recommended) rather than skimming.

## 5. What you'll be able to do afterward

- Read and write `CREATE TABLE` statements with real constraints
  (primary/foreign keys, `NOT NULL`, `UNIQUE`, `CHECK`)
- Write `SELECT` queries combining filtering, sorting, joins,
  aggregation, subqueries, CTEs, and window functions (ranking,
  running totals, `LAG`/`LEAD`)
- Explain *why* a schema is split into multiple tables (normalization),
  not just that it is
- Use transactions to make multi-step changes safely
- Query CSV/Parquet files and pandas DataFrames directly with DuckDB —
  no separate loading step
- Build your own interactive, reactive marimo notebooks — with live SQL
  editors, dropdowns, sliders, and graded exercises — for future work

## 6. Folder contents

```
README.md                              this file
ecommerce_data.py                      shared sample database (plain Python, not a notebook)
01_setup_and_marimo_basics.py          \
02_relational_model_and_keys.py         |
...                                      > the 13 course notebooks, run in order
13_window_functions.py                 /
```

Nothing else in this folder is required reading — `ecommerce_data.py`
is worth a skim (notebook 03 walks through the same ideas by hand) but
you never need to edit it to complete the course.

## 7. Troubleshooting

**`FileNotFoundError: ecommerce_database.duckdb not found`** — you
haven't built the shared database yet, or you moved/deleted it. Run
`./create_database.sh` from this folder, then reopen the notebook.

**`marimo: command not found`** — the `marimo` package installed but
its script isn't on your `PATH`. Try `python3 -m marimo edit
01_setup_and_marimo_basics.py` instead, or reinstall with `pip install
--user marimo` and ensure your Python user-scripts directory is on
`PATH`.

**A notebook opens to a browser tab that won't load / port already in
use** — another `marimo edit`/`marimo run` process is likely still
bound to that port. Find and stop it (`Ctrl+C` in whichever terminal
started it), or pass a different port: `marimo edit
01_setup_and_marimo_basics.py --port 8890`.

**A cell shows a red error instead of a table** — for the numbered
exercises, this is often intentional (notebook 08 deliberately triggers
SQL errors to teach constraints) or just a typo in the SQL you typed
into an exercise box. Read the DuckDB error message; it's usually
specific about the exact clause and reason. For a demo cell (not an
exercise box) showing an error, something is more likely wrong with the
environment — check the [Setup](#1-setup) verification command above.

**"I edited a notebook and now it's broken"** — every notebook that
queries the shared database opens it read-only, and the notebooks that
write (03's exercise, 08, 10) do so against a private in-memory copy —
so the sample data itself can't get corrupted no matter what you run.
If a cell's *code* got accidentally changed or deleted, close without
saving and reopen `marimo edit <file>.py` — or re-fetch the original
file if you're tracking this folder in git. If you suspect
`ecommerce_database.duckdb` itself is in a bad state, just delete it
and run `./create_database.sh` again.

**Verifying a notebook is still structurally valid** after hand-editing
it outside the interactive UI:

```bash
marimo check --ignore-scripts 0*.py 1*.py
```

This should report no errors (style warnings about markdown indentation
are auto-fixable with `--fix` and harmless either way).

## 8. After the course

- Swap `ecommerce_data.py` for a generator over your own domain, and
  revisit any notebook's queries against it.
- DuckDB docs: [duckdb.org/docs](https://duckdb.org/docs)
- Marimo's built-in tutorials: run `marimo tutorial --help` in a
  terminal for a list.

## 9. For instructors extending this course

This repo was built to be easy to extend without redoing the groundwork:

- **Every notebook is independently testable.** Every notebook just calls
  `duckdb.connect("ecommerce_database.duckdb", ...)` directly — no
  custom wrapper. 08 and 10 open it read-write since they deliberately
  mutate data as a teaching demo; 10 cleans up before and after itself
  so the shared file always ends a run in its original state.
- **Validation loop used while authoring:** for any notebook file you
  add or change, run `marimo check --fix <file>.py` (auto-fixes style,
  flags structural issues), then do a headless execution smoke test —
  a failed cell raises a real Python exception, so a passing run is a
  strong signal every query and every exercise's solution actually
  works against the live data, not just "looks right":

  ```bash
  python3 -c "
  import importlib.util
  spec = importlib.util.spec_from_file_location('nb', '<file>.py')
  mod = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(mod)
  outputs, defs = mod.app.run()
  print('OK, cells ran:', len(outputs))
  "
  ```
