import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # OMIS 105 — Course Review: Weeks 1 to 10 in One Notebook

    **OMIS 105 — Introduction to Database Management Systems** · December 3, the last class before the final exam

    One database, **ShopSmart** (an online store), and one section per week. Every
    query answers a business question, written above it in one sentence. Every number
    in the text comes from running the query.

    | Week | Topic | Section below |
    |---|---|---|
    | 1 | Database foundations | 1 |
    | 2 | Relational modeling: keys and relationships | 2 |
    | 3 | SQL basics: `SELECT`, `WHERE`, `ORDER BY`, `NULL`, CRUD, `ENUM`, sequences | 3 |
    | 4 | Aggregation: `GROUP BY`, `HAVING` | 4 |
    | 5 | Joins: `INNER JOIN`, `LEFT JOIN` | 5 |
    | 6 | Joins II: 3+ tables, `RIGHT JOIN`, self-join | 6 |
    | 7 | Subqueries and CTEs | 7 |
    | 8 | Database design: 1NF, 2NF, 3NF | 8 |
    | 9 | Ranking functions | 9 |
    | 10 | Transactions and ACID | 10 |

    **Revenue** in this notebook always means `quantity × unit_price` from
    `order_items` (what was sold).

    ---

    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import duckdb
    import matplotlib.pyplot as plt
    import pandas as pd

    DATA_DIR = Path(__file__).parent / "data"
    con = duckdb.connect()  # an in-memory database

    # Week 2: create every table WITH its keys, then load the CSV data.
    # Parents first (categories, customers, suppliers), then the tables that reference them.
    con.execute("""
        CREATE TABLE categories (
            category_id   INTEGER PRIMARY KEY,
            category_name VARCHAR NOT NULL,
            description   VARCHAR
        )
    """)
    con.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name  VARCHAR NOT NULL,
            last_name   VARCHAR NOT NULL,
            email       VARCHAR,
            city        VARCHAR,
            state       VARCHAR,
            join_date   DATE
        )
    """)
    con.execute("""
        CREATE TABLE suppliers (
            supplier_id   INTEGER PRIMARY KEY,
            supplier_name VARCHAR NOT NULL,
            email         VARCHAR,
            city          VARCHAR,
            state         VARCHAR,
            partner_since DATE
        )
    """)
    con.execute("""
        CREATE TABLE products (
            product_id     INTEGER PRIMARY KEY,
            product_name   VARCHAR NOT NULL,
            category_id    INTEGER REFERENCES categories(category_id),
            price          DECIMAL(10, 2) NOT NULL CHECK (price > 0),
            stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0)
        )
    """)
    con.execute("""
        CREATE TABLE orders (
            order_id     INTEGER PRIMARY KEY,
            customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
            order_date   DATE NOT NULL,
            status       VARCHAR NOT NULL,
            total_amount DECIMAL(10, 2)
        )
    """)
    con.execute("""
        CREATE TABLE order_items (
            item_id    INTEGER PRIMARY KEY,
            order_id   INTEGER NOT NULL REFERENCES orders(order_id),
            product_id INTEGER NOT NULL REFERENCES products(product_id),
            quantity   INTEGER NOT NULL CHECK (quantity > 0),
            unit_price DECIMAL(10, 2) NOT NULL
        )
    """)
    con.execute("""
        CREATE TABLE shipping (
            shipping_id   INTEGER PRIMARY KEY,
            order_id      INTEGER NOT NULL REFERENCES orders(order_id),
            carrier       VARCHAR NOT NULL,
            ship_date     DATE NOT NULL,
            delivery_date DATE,                    -- NULL = not delivered yet
            shipping_cost DECIMAL(10, 2)
        )
    """)
    con.execute("""
        CREATE TABLE reviews (
            review_id   INTEGER PRIMARY KEY,
            product_id  INTEGER NOT NULL REFERENCES products(product_id),
            customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
            rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
            review_text VARCHAR,
            review_date DATE
        )
    """)
    con.execute("""
        CREATE TABLE product_suppliers (
            product_id  INTEGER REFERENCES products(product_id),
            supplier_id INTEGER REFERENCES suppliers(supplier_id),
            cost_price  DECIMAL(10, 2),
            PRIMARY KEY (product_id, supplier_id)  -- a composite key
        )
    """)
    for _table in ["categories", "customers", "suppliers", "products", "orders",
                   "order_items", "shipping", "reviews", "product_suppliers"]:
        con.execute(f"INSERT INTO {_table} SELECT * FROM read_csv('{DATA_DIR}/{_table}.csv')")

    def sql(query, params=None):
        """Run a query and return the result as a table."""
        return con.execute(query, params or []).fetchdf()

    def run(statements):
        """Run statements one by one; return a transcript (✅ / ❌ with DuckDB's answer)."""
        rows = []
        for statement in statements:
            try:
                result = con.execute(statement).fetchall()
                word = statement.split()[0].upper()
                if word in ("UPDATE", "INSERT", "DELETE"):
                    answer = f"{result[0][0]} row(s) changed"
                elif word == "SELECT":
                    answer = " | ".join(", ".join(str(v) for v in row) for row in result)
                else:
                    answer = "OK"
                rows.append(("✅", " ".join(statement.split()), answer))
            except Exception as e:
                rows.append(("❌", " ".join(statement.split()), str(e).splitlines()[0]))
        return pd.DataFrame(rows, columns=["", "statement", "DuckDB says"])

    return con, pd, plt, run, sql


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 1: A first look at the database

    A **database** is a set of **tables**; a table has **rows** and **columns**.

    **Which tables does ShopSmart have, and how many rows does each one hold?**
    """)
    return


@app.cell
def _(con, pd):
    _rows = []
    for (_name,) in con.execute("SHOW TABLES").fetchall():
        _rows.append((_name, con.execute(f"SELECT COUNT(*) FROM {_name}").fetchall()[0][0]))
    pd.DataFrame(_rows, columns=["table_name", "num_rows"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What are the columns of `customers`, and what type is each one?** (`DESCRIBE`)
    """)
    return


@app.cell
def _(sql):
    sql("DESCRIBE customers")[["column_name", "column_type", "null", "key"]]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 2: Keys and relationships

    - A **primary key** identifies each row: unique, never `NULL`.
    - A **foreign key** (`REFERENCES`) links a row to a row in another table.
    - **One-to-many (1:N):** one customer → many orders (`orders.customer_id`).
    - **Many-to-many (M:N):** a product has many suppliers, and a supplier supplies
      many products. It needs a **link table**, `product_suppliers`, whose primary key
      is the pair `(product_id, supplier_id)`.

    **Which foreign keys connect the 9 tables?**
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT table_name, constraint_text
        FROM duckdb_constraints()
        WHERE constraint_type = 'FOREIGN KEY'
        ORDER BY table_name, constraint_text
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Which suppliers supply product 1, and at what cost price?** (the M:N link table)
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT product_id, supplier_id, cost_price
        FROM product_suppliers
        WHERE product_id = 1
        ORDER BY supplier_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The keys protect the data.** Each statement below breaks a key, so the database
    rejects it: a second customer 1, and an order for customer 999, who does not exist.
    """)
    return


@app.cell
def _(run):
    run([
        "INSERT INTO customers VALUES (1, 'Copy', 'Cat', NULL, NULL, NULL, NULL)",
        "INSERT INTO orders VALUES (999, 999, DATE '2025-02-01', 'processing', 10.00)",
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 3: SQL basics

    **List the 5 most expensive products: name and price, most expensive first
    (ties broken by `product_id`).**
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT product_id, product_name, price
        FROM products
        ORDER BY price DESC, product_id
        LIMIT 5
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **In which states do our customers live?** (each state once: `DISTINCT`)
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT DISTINCT state
        FROM customers
        ORDER BY state
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Which Electronics (category 1) or Sports (category 5) products cost from $100 to
    $200?** (`IN`, `BETWEEN` — both ends included)
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT product_id, product_name, category_id, price
        FROM products
        WHERE category_id IN (1, 5)
          AND price BETWEEN 100 AND 200
        ORDER BY price, product_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`NULL` = "unknown / missing".** A shipment that has not arrived yet has no
    `delivery_date`. **How many shipments are not delivered yet?**

    `= NULL` never matches anything (the comparison is itself unknown) — always write
    `IS NULL`.
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT
            COUNT(*) FILTER (WHERE delivery_date IS NULL) AS with_is_null,
            COUNT(*) FILTER (WHERE delivery_date = NULL)  AS with_equals_null,
            COUNT(*)                                      AS all_shipments
        FROM shipping
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **An `ENUM` type lists the only allowed values.** An order's status can only be one
    of four words; a typo like `'shiped'` is rejected.
    """)
    return


@app.cell
def _(con, run):
    con.execute("DROP TABLE IF EXISTS status_demo")   # so the cell can run again
    con.execute("DROP TYPE IF EXISTS order_status")
    run([
        "CREATE TYPE order_status AS ENUM ('processing', 'shipped', 'completed', 'cancelled')",
        "CREATE TABLE status_demo (order_id INTEGER PRIMARY KEY, status order_status NOT NULL)",
        "INSERT INTO status_demo VALUES (1, 'shipped')",
        "INSERT INTO status_demo VALUES (2, 'shiped')",
        "SELECT order_id, status FROM status_demo",
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **CRUD with a sequence (auto-increment).** A new table `wishlist` gets its
    `wish_id` from a **sequence**: `nextval('wish_seq')` gives 1, 2, 3, … Then
    **C**reate (`INSERT`), **R**ead (`SELECT`), **U**pdate, **D**elete.
    """)
    return


@app.cell
def _(con, run):
    con.execute("DROP TABLE IF EXISTS wishlist")      # so the cell can run again
    con.execute("DROP SEQUENCE IF EXISTS wish_seq")
    run([
        "CREATE SEQUENCE wish_seq START 1",
        """CREATE TABLE wishlist (
               wish_id     INTEGER DEFAULT nextval('wish_seq') PRIMARY KEY,
               customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
               product_id  INTEGER NOT NULL REFERENCES products(product_id),
               quantity    INTEGER NOT NULL CHECK (quantity > 0))""",
        "INSERT INTO wishlist (customer_id, product_id, quantity) VALUES (5, 1, 1), (5, 10, 2), (7, 3, 1)",
        "SELECT wish_id, customer_id, product_id, quantity FROM wishlist ORDER BY wish_id",
        "UPDATE wishlist SET quantity = 3 WHERE wish_id = 2",
        "DELETE FROM wishlist WHERE customer_id = 7",
        "SELECT wish_id, customer_id, product_id, quantity FROM wishlist ORDER BY wish_id",
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 4: Aggregation

    **Summarize the product catalog in one row:** number of products, lowest, highest
    and average price, and the total number of items in stock.
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT
            COUNT(*)              AS num_products,
            MIN(price)            AS lowest_price,
            MAX(price)            AS highest_price,
            ROUND(AVG(price), 2)  AS average_price,
            CAST(SUM(stock_quantity) AS INTEGER) AS items_in_stock
        FROM products
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **How many orders are in each status?** (`GROUP BY`: one row per group)
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT status, COUNT(*) AS num_orders
        FROM orders
        GROUP BY status
        ORDER BY num_orders DESC, status
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Which products have at least 5 reviews, and what is their average rating?**
    `WHERE` filters rows **before** grouping; `HAVING` filters **groups** after.
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT product_id,
               COUNT(*)              AS num_reviews,
               ROUND(AVG(rating), 2) AS average_rating
        FROM reviews
        GROUP BY product_id
        HAVING COUNT(*) >= 5
        ORDER BY num_reviews DESC, product_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **How many orders were placed in each month of 2024?** (a Marimo chart from a
    `GROUP BY` result)
    """)
    return


@app.cell
def _(plt, sql):
    _monthly = sql("""
        SELECT MONTH(order_date) AS month, COUNT(*) AS num_orders
        FROM orders
        WHERE order_date >= DATE '2024-01-01' AND order_date < DATE '2025-01-01'
        GROUP BY month
        ORDER BY month
    """)
    _fig, _ax = plt.subplots(figsize=(8, 3))
    _ax.bar(_monthly["month"], _monthly["num_orders"], color="#4C72B0")
    _ax.set_xticks(range(1, 13))
    _ax.set_xlabel("month of 2024")
    _ax.set_ylabel("orders")
    _ax.set_title("Orders per month, 2024")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 5: Joins

    **What did order 3 contain?** For each item: product name, quantity, unit price
    and line total (`quantity × unit_price`). (`INNER JOIN`: only matching rows)
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT oi.item_id, p.product_name, oi.quantity, oi.unit_price,
               oi.quantity * oi.unit_price AS line_total
        FROM order_items AS oi
        INNER JOIN products AS p ON p.product_id = oi.product_id
        WHERE oi.order_id = 3
        ORDER BY oi.item_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Which products have never been reviewed?** `LEFT JOIN` keeps **every** product;
    a product without a review gets `NULL` in the review columns — keep only those rows.
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT p.product_id, p.product_name
        FROM products AS p
        LEFT JOIN reviews AS r ON r.product_id = p.product_id
        WHERE r.review_id IS NULL
        ORDER BY p.product_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **How many orders have no shipment yet, by order status?**
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT o.status, COUNT(*) AS orders_without_shipment
        FROM orders AS o
        LEFT JOIN shipping AS s ON s.order_id = o.order_id
        WHERE s.shipping_id IS NULL
        GROUP BY o.status
        ORDER BY o.status
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Only `cancelled` and `processing` orders lack a shipment — as expected.

    ---
    ## Week 6: Joins II

    **What is the revenue of each product category, highest first?** (3 tables:
    `order_items` → `products` → `categories`)
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT c.category_name,
               SUM(oi.quantity * oi.unit_price) AS revenue
        FROM order_items AS oi
        INNER JOIN products   AS p ON p.product_id  = oi.product_id
        INNER JOIN categories AS c ON c.category_id = p.category_id
        GROUP BY c.category_name
        ORDER BY revenue DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **How many products does each category have?** `RIGHT JOIN` keeps every row of
    the **right** table (`categories`): a category with no products would still be
    listed, with 0. (Here every category has 8.) It is the same as swapping the tables
    and writing `LEFT JOIN`.
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT c.category_id, c.category_name, COUNT(p.product_id) AS num_products
        FROM products AS p
        RIGHT JOIN categories AS c ON c.category_id = p.category_id
        GROUP BY c.category_id, c.category_name
        ORDER BY c.category_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Self-join: which pairs of customers live in Denver?** The table is joined to
    **itself** (aliases `a` and `b`); `a.customer_id < b.customer_id` lists each pair
    once and never pairs a customer with themself.
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT a.first_name || ' ' || a.last_name AS customer_1,
               b.first_name || ' ' || b.last_name AS customer_2
        FROM customers AS a
        INNER JOIN customers AS b
            ON a.city = b.city AND a.customer_id < b.customer_id
        WHERE a.city = 'Denver'
        ORDER BY a.customer_id, b.customer_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 7: Subqueries

    **Scalar subquery (one value): how many products cost more than the average
    product price?**
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT
            (SELECT ROUND(AVG(price), 2) FROM products) AS average_price,
            COUNT(*) AS products_above_average
        FROM products
        WHERE price > (SELECT AVG(price) FROM products)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`IN` (a list): which customers have written at least one 1-star review?**
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT customer_id, first_name, last_name
        FROM customers
        WHERE customer_id IN (SELECT customer_id FROM reviews WHERE rating = 1)
        ORDER BY customer_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The `NOT IN` trap.** If the list contains a `NULL`, `NOT IN` is never true: is 3
    different from an **unknown** value? Unknown. `NOT EXISTS` does not have this
    problem.
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT
            3 NOT IN (1, 2)       AS list_without_null,
            3 NOT IN (1, 2, NULL) AS list_with_null
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`EXISTS`: which customers placed at least one order in January 2025?**
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT c.customer_id, c.first_name, c.last_name
        FROM customers AS c
        WHERE EXISTS (
            SELECT 1
            FROM orders AS o
            WHERE o.customer_id = c.customer_id
              AND o.order_date >= DATE '2025-01-01'
              AND o.order_date <  DATE '2025-02-01'
        )
        ORDER BY c.customer_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Correlated subquery: which products cost more than the average price of their
    own category?** The inner query runs once for each product `p`, using `p.category_id`.
    """)
    return


@app.cell
def _(sql):
    sql("""
        SELECT p.product_id, p.product_name, p.category_id, p.price
        FROM products AS p
        WHERE p.price > (
            SELECT AVG(p2.price)
            FROM products AS p2
            WHERE p2.category_id = p.category_id
        )
        ORDER BY p.category_id, p.price DESC, p.product_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **A CTE (a named subquery): which customers have a revenue above $5,000 — the sum
    of `quantity × unit_price` over all their orders?**
    """)
    return


@app.cell
def _(sql):
    sql("""
        WITH customer_revenue AS (
            SELECT o.customer_id,
                   SUM(oi.quantity * oi.unit_price) AS revenue
            FROM orders AS o
            INNER JOIN order_items AS oi ON oi.order_id = o.order_id
            GROUP BY o.customer_id
        )
        SELECT c.customer_id, c.first_name, c.last_name, cr.revenue
        FROM customer_revenue AS cr
        INNER JOIN customers AS c ON c.customer_id = cr.customer_id
        WHERE cr.revenue > 5000
        ORDER BY cr.revenue DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 8: Database design and normalization

    **1NF: one value per cell.** Someone sends us orders with **several products in one
    cell**. `string_split()` turns the text into a list, and `unnest()` gives each list
    item its own row — now the table is in 1NF.
    """)
    return


@app.cell
def _(sql):
    sql("""
        WITH messy_orders(order_id, products) AS (
            VALUES (1001, 'Laptop, Mouse, Keyboard'),
                   (1002, 'Phone'),
                   (1003, 'Phone, Charger')
        )
        SELECT order_id,
               unnest(string_split(products, ', ')) AS product
        FROM messy_orders
        ORDER BY order_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Why not one big table?** Imagine one wide table with a row per order item and
    every fact repeated in it: the customer's city, the product's name, the category's
    name. **How often would the same facts be stored?**
    """)
    return


@app.cell
def _(sql):
    sql("""
        WITH wide AS (
            SELECT oi.order_id, oi.product_id, cu.city, p.product_name, c.category_name
            FROM order_items AS oi
            INNER JOIN orders     AS o  ON o.order_id     = oi.order_id
            INNER JOIN customers  AS cu ON cu.customer_id = o.customer_id
            INNER JOIN products   AS p  ON p.product_id   = oi.product_id
            INNER JOIN categories AS c  ON c.category_id  = p.category_id
        )
        SELECT
            COUNT(*)                                        AS rows_in_wide_table,
            COUNT(*) FILTER (WHERE city = 'Boston')         AS times_boston_is_stored,
            COUNT(*) FILTER (WHERE category_name = 'Books') AS times_books_is_stored,
            COUNT(DISTINCT category_name)                   AS different_category_names
        FROM wide
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Renaming the category "Books" would mean updating every one of those rows — and
    missing one leaves the data contradicting itself (an **update anomaly**).

    **2NF and 3NF: find the dependencies with `GROUP BY … HAVING`.** In the wide table
    the key is `(order_id, product_id)`.

    - `product_name` depends on **only part** of the key (`product_id`) → a **partial
      dependency** → 2NF moves it to `products`.
    - `category_name` depends on `category_id`, which is **not** a key → a
      **transitive dependency** → 3NF moves it to `categories`.

    **Does `product_id` determine `product_name`, and `category_id` determine
    `category_name`?** If a value of the left column ever had two different values on
    the right, the query would list it. Both return 0 rows: the dependencies hold.
    """)
    return


@app.cell
def _(sql):
    sql("""
        WITH wide AS (
            SELECT oi.order_id, oi.product_id, p.product_name, p.category_id, c.category_name
            FROM order_items AS oi
            INNER JOIN products   AS p ON p.product_id  = oi.product_id
            INNER JOIN categories AS c ON c.category_id = p.category_id
        )
        SELECT 'product_id → product_name' AS dependency, product_id AS left_value
        FROM wide GROUP BY product_id HAVING COUNT(DISTINCT product_name) > 1
        UNION ALL
        SELECT 'category_id → category_name', category_id
        FROM wide GROUP BY category_id HAVING COUNT(DISTINCT category_name) > 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ShopSmart's 9 tables are already in 3NF: each fact is stored **once**, and the
    joins of Weeks 5–6 put it back together when a question needs it.

    ---
    ## Week 9: Ranking functions

    **Rank the products by number of reviews — `ROW_NUMBER`, `RANK` and `DENSE_RANK`
    side by side (the 10 most-reviewed products; ties in `ROW_NUMBER` broken by
    `product_id`).** Watch how each function treats **ties**.
    """)
    return


@app.cell
def _(sql):
    sql("""
        WITH review_counts AS (
            SELECT product_id, COUNT(*) AS num_reviews
            FROM reviews
            GROUP BY product_id
        )
        SELECT product_id, num_reviews,
               ROW_NUMBER() OVER (ORDER BY num_reviews DESC, product_id) AS row_number,
               RANK()       OVER (ORDER BY num_reviews DESC)             AS rank,
               DENSE_RANK() OVER (ORDER BY num_reviews DESC)             AS dense_rank
        FROM review_counts
        ORDER BY num_reviews DESC, product_id
        LIMIT 10
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Top N per group, live.** Pick a category and N: the query below finds the N
    products with the most revenue **in that category** (`RANK()` with
    `PARTITION BY` inside a CTE, then `WHERE rnk <= N` outside — `WHERE` cannot see a
    rank computed in the same query). With `RANK()`, a tie can return more than N rows.
    """)
    return


@app.cell
def _(mo, sql):
    _names = sql("SELECT category_name FROM categories ORDER BY category_id")["category_name"].tolist()
    category = mo.ui.dropdown(options=_names, value="Electronics", label="Category")
    top_n = mo.ui.slider(start=1, stop=8, value=3, label="N")
    mo.hstack([category, top_n], justify="start", gap=2)
    return category, top_n


@app.cell
def _(category, sql, top_n):
    sql("""
        WITH product_revenue AS (
            SELECT c.category_name, p.product_name,
                   SUM(oi.quantity * oi.unit_price) AS revenue
            FROM order_items AS oi
            INNER JOIN products   AS p ON p.product_id  = oi.product_id
            INNER JOIN categories AS c ON c.category_id = p.category_id
            GROUP BY c.category_name, p.product_name
        ),
        ranked AS (
            SELECT *, RANK() OVER (PARTITION BY category_name ORDER BY revenue DESC) AS rnk
            FROM product_revenue
        )
        SELECT rnk, product_name, revenue
        FROM ranked
        WHERE category_name = ? AND rnk <= ?
        ORDER BY rnk, product_name
    """, [category.value, top_n.value])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 10: Transactions

    A **transaction** makes several changes **all or nothing**. Below, two orders
    lower the stock of product 1 (12 in stock) on a **copy** of the table:

    1. sell 2 → `COMMIT` → the stock is 10;
    2. sell 2 **and** 20 in one transaction → the second `UPDATE` breaks
       `CHECK (stock_quantity >= 0)` → the transaction is aborted → `ROLLBACK` →
       the stock is still 10: the first −2 of that transaction was undone too.
    """)
    return


@app.cell
def _(con, run):
    con.execute("DROP TABLE IF EXISTS stock_demo")    # so the cell can run again
    run([
        """CREATE TABLE stock_demo (
               product_id     INTEGER PRIMARY KEY,
               stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0))""",
        "INSERT INTO stock_demo SELECT product_id, stock_quantity FROM products",
        "BEGIN",
        "UPDATE stock_demo SET stock_quantity = stock_quantity - 2 WHERE product_id = 1",
        "COMMIT",
        "SELECT stock_quantity FROM stock_demo WHERE product_id = 1",
        "BEGIN",
        "UPDATE stock_demo SET stock_quantity = stock_quantity - 2 WHERE product_id = 1",
        "UPDATE stock_demo SET stock_quantity = stock_quantity - 20 WHERE product_id = 1",
        "ROLLBACK",
        "SELECT stock_quantity FROM stock_demo WHERE product_id = 1",
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    More in `transactions_demo_1.py` (ACID on a bank table) and
    `transactions_demo_2.py` (orders, returns, two users at once).

    ---
    ## Before the Final Exam: Checklist

    | Week | Can you … |
    |---|---|
    | 1 | explain what a database, a table, a row and a column are? |
    | 2 | name the primary key and the foreign keys of a table, and spot a 1:N vs. an M:N relationship? |
    | 3 | filter, sort and limit rows; handle `NULL` with `IS NULL`; write `INSERT` / `UPDATE` / `DELETE`? |
    | 4 | aggregate with `GROUP BY`, and know when to use `WHERE` vs. `HAVING`? |
    | 5 | choose `INNER JOIN` vs. `LEFT JOIN`, and find "rows without a match"? |
    | 6 | join 3+ tables, use `RIGHT JOIN`, and join a table to itself? |
    | 7 | write scalar, `IN`, `EXISTS` and correlated subqueries, and a CTE — and avoid the `NOT IN` trap? |
    | 8 | put a table into 1NF, 2NF and 3NF, and explain the update anomaly? |
    | 9 | choose between `ROW_NUMBER`, `RANK` and `DENSE_RANK`, and find the top N per group? |
    | 10 | explain ACID, and use `BEGIN` / `COMMIT` / `ROLLBACK`? |

    **Good luck on the final exam!**
    """)
    return


if __name__ == "__main__":
    app.run()
