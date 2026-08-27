import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 🔗 Marimo 102: Joining Tables with SQL

    * **Course:** OMIS 105 — Introduction to Database Management Systems
    * **Instructor:** Dr. Mahmoud Parsian
    * **Before this notebook:** finish `marimo_101_duckdb_sql.py` first —
      this one assumes you're comfortable with cells, reactivity, and
      basic `SELECT` / `WHERE` / `GROUP BY`.

    ## What You'll Learn

    Real databases spread data across **multiple tables** instead of one
    giant spreadsheet. Today you'll learn `JOIN` — the SQL command that
    stitches tables back together — using our campus bookstore.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Why Split Data Into Multiple Tables?

    Imagine one giant table with a row per order, repeating the
    customer's name and email on every single row. If a customer's
    email changes, you'd have to update it in dozens of places — messy
    and error-prone.

    Instead, relational databases keep **one fact in one place**:

    - a `customers` table (one row per customer)
    - a `products` table (one row per product)
    - an `orders` table that just points to them, using **id** columns

    `JOIN` is how we bring those pieces back together when we need to
    *read* the full picture.
    """)
    return


@app.cell
def _():
    # Python cell — create an in-memory DuckDB connection
    import duckdb

    con = duckdb.connect(database=":memory:")
    print("DuckDB version:", duckdb.__version__)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1. Build Three Small Tables

    * `customers` — 5 people
    * `products` — 6 items
    * `orders` — who bought what (this table only stores **id numbers**,
      not names)
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE customers (
            customer_id   INTEGER,
            customer_name VARCHAR,
            email         VARCHAR
        );
        """
    )
    return


@app.cell
def _(customers, mo):
    _df = mo.sql(
        f"""
        INSERT INTO customers (customer_id, customer_name, email) VALUES
            (1, 'Alice',   'alice@scu.edu'),
            (2, 'Bob',     'bob@scu.edu'),
            (3, 'Carol',   'carol@scu.edu'),
            (4, 'David',   'david@scu.edu'),
            (5, 'Diana',   'diana@scu.edu');
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE products (
            product_id   INTEGER,
            product_name VARCHAR,
            price        DECIMAL(6,2)
        );
        """
    )
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        INSERT INTO products (product_id, product_name, price) VALUES
            (1, 'Spiral Notebook', 4.50),
            (2, 'Gel Pen (4-pack)', 6.25),
            (3, 'Laptop Stand',    29.99),
            (4, 'Wireless Mouse',  19.99),
            (5, 'SCU Hoodie',      45.00),
            (6, 'SCU Cap',         18.00);
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE orders (
            order_id    INTEGER,
            customer_id INTEGER,
            product_id  INTEGER,
            quantity    INTEGER,
            order_date  DATE
        );
        """
    )
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        -- Note: customer_id 5 (Diana) has no orders yet — on purpose!
        INSERT INTO orders (order_id, customer_id, product_id, quantity, order_date) VALUES
            (1, 1, 1, 2, '2026-01-10'),
            (2, 1, 4, 1, '2026-01-10'),
            (3, 2, 3, 1, '2026-01-12'),
            (4, 2, 5, 1, '2026-01-15'),
            (5, 3, 2, 3, '2026-01-18'),
            (6, 3, 6, 2, '2026-01-18'),
            (7, 4, 1, 5, '2026-01-20'),
            (8, 1, 6, 1, '2026-01-25');
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 2. The Problem With One Table Alone

    Let's look at `orders` by itself.
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   orders
        ORDER BY order_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    See the problem? We only get **numbers**. Who is `customer_id` 1?
    What's `product_id` 3? To answer that, we need to **join** `orders`
    to `customers` and `products`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3. `INNER JOIN`: Orders + Customers

    `JOIN ... ON` tells DuckDB: *"match rows where these two columns are
    equal."* Here, we match each order's `customer_id` to the
    customer's own `customer_id`.
    """)
    return


@app.cell
def _(customers, mo, orders):
    _df = mo.sql(
        f"""
        SELECT o.order_id,
               c.customer_name,
               o.product_id,
               o.quantity,
               o.order_date
        FROM   orders o
        JOIN   customers c ON o.customer_id = c.customer_id
        ORDER BY o.order_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Read it out loud: *"From orders, joined to customers where the
    customer ids match, give me the order id, customer name, product id,
    quantity, and date."*

    Notice we gave each table a short **alias** (`o` for orders, `c` for
    customers) so DuckDB knows which table each column comes from.

    ---
    ## 4. Join All Three Tables

    Let's add `products` too, so we can see product names *and* compute
    each order's dollar total.
    """)
    return


@app.cell
def _(customers, mo, orders, products):
    _df = mo.sql(
        f"""
        SELECT o.order_id,
               c.customer_name,
               p.product_name,
               o.quantity,
               p.price,
               ROUND(o.quantity * p.price, 2) AS line_total
        FROM   orders o
        JOIN   customers c ON o.customer_id = c.customer_id
        JOIN   products  p ON o.product_id  = p.product_id
        ORDER BY o.order_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    That's a real, readable order history — built from three small
    tables and two `JOIN`s.

    ---
    ## 5. Business Question: Who Spent the Most?

    Join + `GROUP BY` + `SUM()` answers this in one query.
    """)
    return


@app.cell
def _(customers, mo, orders, products):
    _df = mo.sql(
        f"""
        SELECT c.customer_name,
               COUNT(*)                            AS num_orders,
               ROUND(SUM(o.quantity * p.price), 2)  AS total_spent
        FROM   orders o
        JOIN   customers c ON o.customer_id = c.customer_id
        JOIN   products  p ON o.product_id  = p.product_id
        GROUP BY c.customer_name
        ORDER BY total_spent DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 6. `INNER JOIN` vs. `LEFT JOIN`

    Remember Diana? She's in `customers` but has **no rows** in
    `orders`. An `INNER JOIN` only keeps rows that match on *both*
    sides — so Diana quietly disappears.
    """)
    return


@app.cell
def _(customers, mo, orders):
    _df = mo.sql(
        f"""
        -- INNER JOIN: customers with zero orders are dropped
        SELECT c.customer_name,
               COUNT(o.order_id) AS num_orders
        FROM   customers c
        JOIN   orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_name
        ORDER BY c.customer_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Only 4 customers — Diana is missing! If the business question is
    *"how many orders does **each** customer have, including zero?"*,
    we need `LEFT JOIN` instead: **keep every row from the left table**
    (`customers`), even when there's no match on the right.
    """)
    return


@app.cell
def _(customers, mo, orders):
    _df = mo.sql(
        f"""
        -- LEFT JOIN: every customer appears, even with zero orders
        SELECT c.customer_name,
               COUNT(o.order_id) AS num_orders
        FROM   customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_name
        ORDER BY c.customer_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Now all 5 customers show up, and Diana correctly shows `0`.
    `COUNT(o.order_id)` counts only non-`NULL` order ids, so a customer
    with no matching orders gets `0` instead of `1`.

    **Rule of thumb:** use `INNER JOIN` when you only want rows that
    exist in *both* tables; use `LEFT JOIN` when you want to keep every
    row from the first table no matter what.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 7. Make It Interactive

    Just like in Marimo 101, we can wire a dropdown into a join query.
    Pick a customer and see their full order history, joined with
    product names — live.
    """)
    return


@app.cell
def _(mo):
    customer_picker = mo.ui.dropdown(
        options=["Alice", "Bob", "Carol", "David", "Diana"],
        value="Alice",
        label="Choose a customer:",
    )
    customer_picker
    return (customer_picker,)


@app.cell
def _(customer_picker, customers, mo, orders, products):
    _df = mo.sql(
        f"""
        SELECT p.product_name,
               o.quantity,
               p.price,
               ROUND(o.quantity * p.price, 2) AS line_total
        FROM   customers c
        LEFT JOIN orders   o ON c.customer_id = o.customer_id
        LEFT JOIN products p ON o.product_id  = p.product_id
        WHERE  c.customer_name = '{customer_picker.value}'
        ORDER BY o.order_date;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Try picking **Diana** — she has no orders, so the table comes back
    empty (rather than erroring out), because we used `LEFT JOIN`
    starting from `customers`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Recap: What You Just Learned

    - ✅ Data lives in **multiple small tables** connected by id columns
    - ✅ `JOIN ... ON` matches rows across tables using those id columns
    - ✅ Table **aliases** (`o`, `c`, `p`) keep multi-table queries readable
    - ✅ `INNER JOIN` keeps only matching rows; `LEFT JOIN` keeps every
      row from the first table, filling in `NULL` where there's no match
    - ✅ `JOIN` combines with `GROUP BY`, `SUM`, and UI elements exactly
      like the single-table queries from Marimo 101

    ## Where to Go Next

    - Try changing the `LEFT JOIN`s back to `JOIN`s in the last query and
      see what happens when you pick Diana
    - Add a 6th customer and a couple of orders, then re-run the notebook
    - Continue to `marimo_103_subqueries_ctes.py`, in this same folder,
      to learn subqueries and CTEs
    - Continue to `outline-10-weeks/sql_notebooks/` and the
      `weekly_reviews/` notebooks for multi-table practice with bigger
      datasets

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
