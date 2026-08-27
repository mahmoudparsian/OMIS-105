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
    # 🧩 Marimo 103: Subqueries and CTEs

    * **Course:** OMIS 105 — Introduction to Database Management Systems
    * **Instructor:** Dr. Mahmoud Parsian
    * **Before this notebook:** finish `marimo_102_joins.py` first — this
      one assumes you're comfortable with `JOIN`, `GROUP BY`, and
      aggregate functions like `SUM`/`COUNT`/`AVG`.

    ## What You'll Learn

    Some business questions need an answer to *another* question first —
    for example, *"which products cost more than average?"* requires
    computing the average before you can compare anything to it. Today
    you'll learn two tools for that: **subqueries** (a query inside a
    query) and **CTEs** (a way to name and organize those inner
    queries), using the same campus-bookstore data from Marimo 102.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Why Not Just Use JOIN and GROUP BY?

    You already know `JOIN` and `GROUP BY` — they're often enough. But
    some questions need a **two-step** answer:

    1. Compute something first (an average, a count, a list of ids)
    2. Then compare each row to that computed value

    A **subquery** is a `SELECT` statement nested inside another `SELECT`
    statement to do exactly that. A **CTE** (Common Table Expression,
    written with `WITH ... AS`) does the same thing, but gives the inner
    query a name — making long queries much easier to read.
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
    ## 0. Rebuild the Tables From Marimo 102

    Same three small tables, same data: `customers` (5 rows), `products`
    (6 rows), `orders` (8 rows) — including Diana, who still has no
    orders.
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
    ## 1. A Subquery in `WHERE`

    **Question:** *"Which products cost more than the average product
    price?"*

    The inner query `(SELECT AVG(price) FROM products)` runs first and
    produces one number. The outer query then uses that number just like
    a constant.
    """)
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        SELECT product_name,
               price
        FROM   products
        WHERE  price > (SELECT AVG(price) FROM products)
        ORDER BY price DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Read it out loud: *"From products, where the price is greater than
    the average price of all products, show me the name and price."*
    DuckDB computes the average once, then compares every row to it.

    ---
    ## 2. A Subquery With `IN` / `NOT IN`

    **Question:** *"Which customers have never placed an order?"*
    """)
    return


@app.cell
def _(customers, mo, orders):
    _df = mo.sql(
        f"""
        SELECT customer_name
        FROM   customers
        WHERE  customer_id NOT IN (SELECT customer_id FROM orders);
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Diana shows up — same answer we got with `LEFT JOIN ... IS NULL` in
    Marimo 102, but asked a different way: *"give me customer ids that
    are **not** in this list of ids that have ordered."*

    ⚠️ **Caution:** `NOT IN` can misbehave if the subquery's column
    contains `NULL` values. Here `orders.customer_id` never has `NULL`s,
    so we're safe — but it's a good habit to check.

    ---
    ## 3. A Subquery in `FROM`

    A subquery can also stand in for a table. Here we first count each
    customer's orders, then filter on that count.
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   (
            SELECT customer_id,
                   COUNT(*) AS num_orders
            FROM   orders
            GROUP BY customer_id
        ) AS order_counts
        WHERE  num_orders > 1;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    That query works, but it's already a little hard to read — the
    inner `SELECT` is buried inside the outer one. This is exactly the
    problem CTEs solve.

    ---
    ## 4. CTEs: `WITH ... AS`

    A **CTE** pulls the inner query out and gives it a name, using
    `WITH name AS (...)` before the main `SELECT`. Same logic as the
    subquery above, but easier to follow — and now we can join it to
    `customers` to include everyone, even customers with zero orders.
    """)
    return


@app.cell
def _(customers, mo, orders):
    _df = mo.sql(
        f"""
        WITH order_counts AS (
            SELECT customer_id,
                   COUNT(*) AS num_orders
            FROM   orders
            GROUP BY customer_id
        )
        SELECT c.customer_name,
               COALESCE(order_counts.num_orders, 0) AS num_orders
        FROM   customers c
        LEFT JOIN order_counts ON c.customer_id = order_counts.customer_id
        ORDER BY num_orders DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Notice the shape: `WITH <name> AS ( <query> )`, then a normal
    `SELECT` that treats `order_counts` just like any other table.

    ---
    ## 5. Chaining Two CTEs

    **Question:** *"Which customers spent above the average customer's
    total spending?"* That takes three steps:

    1. Compute each customer's total spent (needs a `JOIN`)
    2. Compute the average of those totals
    3. Compare each customer's total to that average

    Each step becomes its own named CTE.
    """)
    return


@app.cell
def _(customers, mo, orders, products):
    _df = mo.sql(
        f"""
        WITH customer_totals AS (
            SELECT c.customer_id,
                   c.customer_name,
                   ROUND(SUM(o.quantity * p.price), 2) AS total_spent
            FROM   customers c
            JOIN   orders   o ON c.customer_id = o.customer_id
            JOIN   products p ON o.product_id  = p.product_id
            GROUP BY c.customer_id, c.customer_name
        ),
        avg_spent AS (
            SELECT AVG(total_spent) AS avg_total
            FROM   customer_totals
        )
        SELECT customer_totals.customer_name,
               customer_totals.total_spent
        FROM   customer_totals, avg_spent
        WHERE  customer_totals.total_spent > avg_spent.avg_total
        ORDER BY customer_totals.total_spent DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Read the query top to bottom, one CTE at a time:

    1. `customer_totals` — one row per customer, with what they spent
    2. `avg_spent` — a single number: the average of those totals
    3. The final `SELECT` compares each customer's total to that one
       number and keeps only the above-average spenders

    Placing `customer_totals` and `avg_spent` side by side with a comma
    pairs every row of the first with the one row of the second — since
    `avg_spent` has just one row, this simply attaches that average to
    every customer.

    ---
    ## 6. Make It Interactive

    Let's turn "above average" into an adjustable threshold: *"above
    **N ×** average spending."*
    """)
    return


@app.cell
def _(mo):
    multiplier = mo.ui.slider(
        0.5, 2.0, step=0.1, value=1.0, label="Spending threshold (× average):"
    )
    multiplier
    return (multiplier,)


@app.cell
def _(customers, mo, multiplier, orders, products):
    _df = mo.sql(
        f"""
        WITH customer_totals AS (
            SELECT c.customer_id,
                   c.customer_name,
                   ROUND(SUM(o.quantity * p.price), 2) AS total_spent
            FROM   customers c
            JOIN   orders   o ON c.customer_id = o.customer_id
            JOIN   products p ON o.product_id  = p.product_id
            GROUP BY c.customer_id, c.customer_name
        ),
        avg_spent AS (
            SELECT AVG(total_spent) AS avg_total
            FROM   customer_totals
        )
        SELECT customer_totals.customer_name,
               customer_totals.total_spent
        FROM   customer_totals, avg_spent
        WHERE  customer_totals.total_spent > avg_spent.avg_total * {multiplier.value}
        ORDER BY customer_totals.total_spent DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Drag the slider down toward `0.5` and more customers qualify; push
    it up toward `2.0` and the list shrinks — the CTEs stay exactly the
    same, only the final comparison changes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Recap: What You Just Learned

    - ✅ A **subquery** is a `SELECT` nested inside another query — it
      can appear in `WHERE`, `FROM`, or with `IN`/`NOT IN`
    - ✅ The inner query runs first; the outer query uses its result
      like a constant, a list, or a table
    - ✅ A **CTE** (`WITH name AS (...)`) names a subquery so it can be
      read top to bottom instead of nested inside itself
    - ✅ CTEs can be **chained**, each one building on the last, to break
      a hard question into simple steps
    - ✅ Subqueries and CTEs combine with everything from 101 and 102:
      `WHERE`, `JOIN`, `GROUP BY`, and UI elements

    ## Where to Go Next

    - Try changing `> (SELECT AVG(price) FROM products)` in Section 1
      to `<` and see which products come back
    - Rewrite the `NOT IN` query in Section 2 using a `LEFT JOIN ...
      WHERE ... IS NULL` instead, and compare the two approaches
    - Continue to `outline-10-weeks/sql_notebooks/` and the
      `weekly_reviews/` notebooks — CTEs and subqueries show up
      constantly in Weeks 7–10

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
