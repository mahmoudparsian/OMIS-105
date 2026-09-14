import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 6: Database Design & Normalization — INSTRUCTOR SOLUTIONS

    ## OMIS 105 — Database Management Systems
    **Week 6 | Answer Key**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Connect to DuckDB and load `orders_denorm` (the denormalized table
    used throughout Parts 1–3), plus the already-normalized `categories`,
    `products`, `customers`, `orders`, and `order_items` (used in Part 5)
    from `./data/`.
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell
def _(con):
    con.execute(
        "CREATE OR REPLACE TABLE orders_denorm AS SELECT * FROM read_csv_auto('./data/orders_denormalized.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE categories AS SELECT * FROM read_csv_auto('./data/categories.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE products AS SELECT * FROM read_csv_auto('./data/products.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv_auto('./data/customers.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE orders AS SELECT * FROM read_csv_auto('./data/orders.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE order_items AS SELECT * FROM read_csv_auto('./data/order_items.csv')"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Functional Dependencies (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** (5 pts) Functional dependencies in `orders_denormalized`:

    ```
    order_id → order_date, status, customer_id
    customer_id → customer_name, customer_email, customer_city
    product_id → product_name, category_name, unit_price
    (order_id, product_id) → quantity, line_price
    ```

    Verify: `customer_id → customer_name`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT customer_id, COUNT(DISTINCT customer_name) AS dist
        FROM orders_denorm GROUP BY customer_id HAVING COUNT(DISTINCT customer_name) > 1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Verify: `product_id → product_name`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT product_id, COUNT(DISTINCT product_name) AS dist
        FROM orders_denorm GROUP BY product_id HAVING COUNT(DISTINCT product_name) > 1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Verify: `order_id → order_date`.

    > All three return 0 rows — each FD holds, since no key value maps
    to more than one distinct value on the right-hand side.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT order_id, COUNT(DISTINCT order_date) AS dist
        FROM orders_denorm GROUP BY order_id HAVING COUNT(DISTINCT order_date) > 1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** (5 pts) Candidate key: `(order_id, product_id)`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT order_id, product_id, COUNT(*) AS cnt
        FROM orders_denorm
        GROUP BY order_id, product_id
        HAVING COUNT(*) > 1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Empty result proves uniqueness — `(order_id, product_id)` is a
    valid candidate key.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** (5 pts) Classify each FD as full, partial, or transitive with
    respect to the candidate key `(order_id, product_id)`:

    - **Full**: `(order_id, product_id) → quantity, line_price`
    - **Partial**: `order_id → order_date, status, customer_id`
      (depends on only part of the key)
    - **Partial**: `product_id → product_name, category_name, unit_price`
      (depends on only part of the key)
    - **Transitive**: `order_id → customer_id → customer_name,
      customer_email, customer_city`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Identifying Anomalies (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** (5 pts) Redundancy: how many times each customer's
    information repeats.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT customer_id, customer_name, customer_email,
               COUNT(*) AS times_repeated
        FROM orders_denorm
        GROUP BY customer_id, customer_name, customer_email
        ORDER BY times_repeated DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** (5 pts) Anomalies in `orders_denormalized`:

    - **Update anomaly**: if customer "Alice Smith" changes her email,
      every row where she appears must be updated (could be 10+ rows).
      Missing one creates inconsistency.
    - **Insertion anomaly**: cannot add a new customer who hasn't placed
      an order, because `order_id` is part of the key.
    - **Deletion anomaly**: deleting the only order for customer "Bob
      Johnson" loses all his customer information (name, email, city).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Normalization (25 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6.** (10 pts) 2NF decomposition — remove partial dependencies on
    the composite key.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE OR REPLACE TABLE orders_2nf AS
        SELECT DISTINCT order_id, order_date, status, customer_id,
               customer_name, customer_email, customer_city
        FROM orders_denorm
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE products_2nf AS
        SELECT DISTINCT product_id, product_name, category_name, unit_price
        FROM orders_denorm
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE order_items_2nf AS
        SELECT DISTINCT order_id, product_id, quantity, line_price
        FROM orders_denorm
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT 'orders_2nf' AS tbl, COUNT(*) AS cnt FROM orders_2nf
        UNION ALL SELECT 'products_2nf', COUNT(*) FROM products_2nf
        UNION ALL SELECT 'order_items_2nf', COUNT(*) FROM order_items_2nf
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** (10 pts) 3NF decomposition — remove the transitive
    dependencies (`customer_id → customer_name/email/city` and
    `product_id → category_name`).
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE OR REPLACE TABLE customers_3nf AS
        SELECT DISTINCT customer_id, customer_name, customer_email, customer_city
        FROM orders_denorm
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE orders_3nf AS
        SELECT DISTINCT order_id, order_date, status, customer_id
        FROM orders_denorm
        """
    )
    con.execute(
        "CREATE OR REPLACE TABLE categories_3nf AS SELECT DISTINCT category_name FROM orders_denorm"
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE products_3nf AS
        SELECT DISTINCT product_id, product_name, category_name, unit_price
        FROM orders_denorm
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE order_items_3nf AS
        SELECT DISTINCT order_id, product_id, quantity, line_price
        FROM orders_denorm
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8.** (5 pts) Yes — the 3NF schema is also in BCNF, because in each
    table the only determinants are the primary (or candidate) keys, and
    each of those is a superkey.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: Design Challenge (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9.** (10 pts) Functional dependencies for `library_flat`:

    ```
    loan_id → loan_date, return_date, member_id, book_id, branch_id
    member_id → member_name, member_email, member_phone
    book_id → book_title, isbn, author_name, author_nationality
    author_name → author_nationality (transitive through book)
    branch_id → branch_name, branch_city
    ```

    3NF decomposition:
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE OR REPLACE TABLE members (
            member_id INTEGER PRIMARY KEY,
            member_name VARCHAR, member_email VARCHAR, member_phone VARCHAR
        )
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE authors (
            author_id INTEGER PRIMARY KEY,
            author_name VARCHAR, author_nationality VARCHAR
        )
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE books (
            book_id INTEGER PRIMARY KEY,
            book_title VARCHAR, isbn VARCHAR UNIQUE,
            author_id INTEGER REFERENCES authors(author_id)
        )
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE branches (
            branch_id INTEGER PRIMARY KEY,
            branch_name VARCHAR, branch_city VARCHAR
        )
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE loans (
            loan_id INTEGER PRIMARY KEY,
            loan_date DATE, return_date DATE,
            member_id INTEGER REFERENCES members(member_id),
            book_id INTEGER REFERENCES books(book_id),
            branch_id INTEGER REFERENCES branches(branch_id)
        )
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** (5 pts) The ER diagram should show:

    - 5 entities with their PKs and attributes: `members`, `authors`,
      `books`, `branches`, `loans`
    - `authors → books` (1:M)
    - `members → loans` (1:M)
    - `books → loans` (1:M)
    - `branches → loans` (1:M)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Denormalization Discussion (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q11.** (5 pts) A view that reconstructs the denormalized data from
    the normalized ShopSmart tables.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE OR REPLACE VIEW orders_denorm_view AS
        SELECT o.order_id, o.order_date, o.status,
               c.customer_id, c.first_name || ' ' || c.last_name AS customer_name,
               c.email AS customer_email, c.city AS customer_city,
               p.product_id, p.product_name, cat.category_name, oi.unit_price,
               oi.quantity, ROUND(oi.quantity * oi.unit_price, 2) AS line_price
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        JOIN categories cat ON p.category_id = cat.category_id
        """
    )
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM orders_denorm_view ORDER BY order_id LIMIT 10").fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** (5 pts) Two real-world denormalization scenarios:

    1. **E-commerce product listing page**: store `category_name`
       directly in the `products` table. Saves a JOIN on every page
       load. Trade-off: must update product rows when category names
       change.
    2. **Analytics data warehouse**: store pre-aggregated daily revenue
       totals. Trade-off: faster dashboard queries, but a daily ETL job
       is needed and the data is slightly stale.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Grading Rubric

    | Part | Points |
    |------|--------|
    | Part 1: Functional Dependencies | 15 |
    | Part 2: Identifying Anomalies | 10 |
    | Part 3: Normalization | 25 |
    | Part 4: Design Challenge | 15 |
    | Part 5: Denormalization | 10 |
    | **Total** | **75** |
    """)
    return


if __name__ == "__main__":
    app.run()
