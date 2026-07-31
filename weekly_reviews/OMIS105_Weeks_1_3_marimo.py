import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from plot_helpers import plot_bar, plot_hbar, plot_pie, plot_grouped_bar

    return plot_bar, plot_grouped_bar, plot_hbar, plot_pie


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=":memory:")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — SQL Fundamentals (Weeks 1–3)

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### What This Notebook Covers

    | Week | Topics | Lectures |
    |------|--------|----------|
    | 1 | SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, data types | Lectures 1–2 |
    | 2 | Multi-table design, PRIMARY KEY, FOREIGN KEY, JOINs | Lectures 3–4 |
    | 3 | GROUP BY, HAVING, aggregate functions, plots, subqueries | Lectures 5–6 |

    ### Our Dataset

    We use a single CSV file: **`orders_data.csv`** — 20 orders from a small retail business.
    It contains customer info, product info, and order details all in one flat file.
    Over the course of this notebook, we'll see why that's a problem and how to fix it.

    ### How to Use

    Run each cell in order. Read the markdown — it explains the *why* behind every query.
    In Marimo, SQL cells run directly against DuckDB — no Python wrappers needed!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Setup — Load the CSV into DuckDB
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE orders AS
            SELECT * FROM read_csv_auto('orders_data.csv');
        """
    )
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT 'orders_data.csv loaded!' AS status,
               COUNT(*) AS total_rows
        FROM orders;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # WEEK 1 — Querying a Single Table

    ---

    ## 1.1 — SELECT * (See Everything)

    The simplest SQL query: "show me all the data."
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
    ## 1.2 — SELECT Specific Columns

    You rarely need *all* columns. Pick just the ones you care about:
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT order_id,
                   customer_name,
                   product_name,
                   unit_price,
                   quantity
            FROM   orders
            ORDER BY order_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1.3 — Computed Columns

    SQL can do math. Let's compute the **total** for each order:
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT order_id,
                   customer_name,
                   product_name,
                   unit_price,
                   quantity,
                   ROUND(unit_price * quantity, 2) AS order_total
            FROM   orders
            ORDER BY order_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1.4 — WHERE (Filter Rows)

    > *Business question: "Show me only the Electronics orders."*

    `WHERE` keeps only the rows that match a condition.
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT order_id, customer_name, product_name, unit_price
            FROM   orders
            WHERE  category = 'Electronics'
            ORDER BY order_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### WHERE with comparison operators

    Orders where the total exceeds $100.

    **Note:** `WHERE` runs BEFORE `SELECT`, so we cannot use
    the alias `order_total` here — we must repeat the expression.
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT order_id,
                   customer_name,
                   product_name,
                   unit_price * quantity AS order_total
            FROM   orders
            WHERE  unit_price * quantity > 100
            ORDER BY order_total DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### Why `unit_price * quantity` instead of `order_total`?

    You might wonder: we defined `order_total` in the SELECT — why can't we use it in WHERE?

    The answer is **SQL's execution order**. SQL does NOT process your query top-to-bottom.
    It follows this order:

    ```
    1. FROM       ← pick the table
    2. WHERE      ← filter rows         (aliases do NOT exist yet!)
    3. GROUP BY   ← group rows
    4. HAVING     ← filter groups
    5. SELECT     ← compute columns      (aliases are created HERE)
    6. ORDER BY   ← sort results          (aliases ARE available here)
    7. LIMIT      ← return top N
    ```

    Since WHERE (step 2) runs **before** SELECT (step 5), the alias `order_total` does not exist yet.
    That's why we must repeat the expression: `WHERE unit_price * quantity > 100`.

    Notice that ORDER BY (step 6) runs **after** SELECT — so `ORDER BY order_total DESC` works fine.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### WHERE with AND / OR
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        -- -------------------------------------
        -- Gold customers who bought Electronics
        -- -------------------------------------
            SELECT order_id, customer_name, product_name, unit_price
            FROM   orders
            WHERE  customer_tier = 'Gold'
              AND  category = 'Electronics'
            ORDER BY order_id
        """
    )
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        -- Orders from San Jose OR Santa Clara
        SELECT order_id, customer_name, customer_city, product_name
        FROM   orders
        WHERE  customer_city = 'San Jose'
           OR  customer_city = 'Santa Clara'
        ORDER BY customer_city, order_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### WHERE with IN (cleaner than multiple ORs)
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        -- Same as above, but cleaner
        SELECT order_id, customer_name, customer_city, product_name
        FROM   orders
        WHERE  customer_city IN ('San Jose', 'Santa Clara')
        ORDER BY customer_city, order_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### WHERE with BETWEEN
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        -- Orders placed in February 2025
        SELECT order_id, customer_name, product_name, order_date
        FROM   orders
        WHERE  order_date BETWEEN '2025-02-01' AND '2025-02-28'
        ORDER BY order_date
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### WHERE with LIKE (pattern matching)
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        -- Products that start with 'L'
        SELECT DISTINCT product_name
        FROM   orders
        WHERE  product_name LIKE 'L%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1.5 — ORDER BY (Sort Results)

    > *Business question: "What are our most expensive orders?"*
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT order_id,
               customer_name,
               product_name,
               unit_price * quantity AS order_total
        FROM   orders
        ORDER BY order_total DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Sorting by multiple columns
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        -- Sort by city (A-Z), then by order_total (highest first)
        SELECT order_id,
               customer_name,
               customer_city,
               unit_price * quantity AS order_total
        FROM   orders
        ORDER BY customer_city ASC, order_total DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1.6 — LIMIT (Top N)

    > *Business question: "Show me only the top 5 highest-value orders."*
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT order_id,
               customer_name,
               product_name,
               unit_price * quantity AS order_total
        FROM   orders
        ORDER BY order_total DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1.7 — DISTINCT (Unique Values)

    > *Business question: "What cities do our customers come from?"*
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT DISTINCT customer_city
        FROM   orders
        ORDER BY customer_city
        """
    )
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        -- How many unique customers do we have?
        SELECT DISTINCT customer_name, customer_city, customer_tier
        FROM   orders
        ORDER BY customer_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1.8 — COUNT (How Many?)

    > *Business question: "How many orders do we have? How many unique customers?"*
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT COUNT(*)                      AS total_orders,
               COUNT(DISTINCT customer_name) AS unique_customers,
               COUNT(DISTINCT product_name)  AS unique_products,
               COUNT(DISTINCT category)      AS unique_categories
        FROM   orders
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ### Week 1 Summary

    | Keyword | Purpose | Example |
    |---------|---------|---------|
    | `SELECT` | Choose columns | `SELECT name, price FROM ...` |
    | `WHERE` | Filter rows | `WHERE price > 100` |
    | `AND / OR` | Combine conditions | `WHERE city = 'X' AND tier = 'Gold'` |
    | `IN` | Match a list | `WHERE city IN ('A', 'B')` |
    | `BETWEEN` | Range filter | `WHERE date BETWEEN '...' AND '...'` |
    | `LIKE` | Pattern match | `WHERE name LIKE 'L%'` |
    | `ORDER BY` | Sort results | `ORDER BY price DESC` |
    | `LIMIT` | Top N rows | `LIMIT 5` |
    | `DISTINCT` | Unique values | `SELECT DISTINCT city` |
    | `COUNT` | Count rows | `COUNT(*)`, `COUNT(DISTINCT ...)` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # WEEK 2 — Relational Design & JOINs

    ---

    ## 2.1 — The Problem: Redundancy in Our Data

    Look carefully at our CSV. Alice appears in **4 rows**. Every time, her city
    ("San Jose") and tier ("Gold") are repeated. What's wrong with that?
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        -- Alice's data is repeated in every row
        SELECT order_id, customer_name, customer_city, customer_tier
        FROM   orders
        WHERE  customer_name = 'Alice'
        ORDER BY order_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### The Three Problems of a Flat Table

    1. **Redundancy** — Alice's city and tier are stored 4 times instead of once
    2. **Update anomaly** — If Alice moves to "Palo Alto", we must update 4 rows. Miss one? Inconsistent data.
    3. **Deletion anomaly** — If we delete all of David's orders, we lose the fact that David exists at all

    ### The Solution: Split Into Multiple Tables

    We separate our data into three tables, each storing **one kind of thing**:

    - **customers** — one row per customer (name, city, tier)
    - **products** — one row per product (name, category, price)
    - **orders** — one row per order (who bought what, when, how many)

    The tables are connected by **IDs** (foreign keys).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 2.2 — Creating the Normalized Tables

    ### Customers Table
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE customers (
            customer_id   INTEGER PRIMARY KEY,
            customer_name VARCHAR NOT NULL,
            city          VARCHAR NOT NULL,
            tier          VARCHAR NOT NULL
        )
        """
    )
    return


@app.cell
def _(customers, mo):
    _df = mo.sql(
        f"""
        INSERT INTO customers VALUES
            (1, 'Alice', 'San Jose',      'Gold'),
            (2, 'Bob',   'Santa Clara',   'Silver'),
            (3, 'Carol', 'San Jose',      'Gold'),
            (4, 'David', 'San Francisco', 'Bronze'),
            (5, 'Eva',   'Santa Clara',   'Silver'),
            (6, 'Frank', 'San Jose',      'Gold')
        """
    )
    return


@app.cell
def _(customers, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM customers ORDER BY customer_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Products Table
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE products (
            product_id   INTEGER PRIMARY KEY,
            product_name VARCHAR NOT NULL,
            category     VARCHAR NOT NULL,
            unit_price   DECIMAL(10,2) NOT NULL
        )
        """
    )
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        INSERT INTO products VALUES
            (1, 'Laptop',    'Electronics',  999.99),
            (2, 'Mouse',     'Electronics',   29.99),
            (3, 'Notebook',  'Office',        12.99),
            (4, 'Pen Set',   'Office',         8.99),
            (5, 'Backpack',  'Accessories',   49.99),
            (6, 'USB Cable', 'Electronics',    9.99)
        """
    )
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        SELECT * FROM products ORDER BY product_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### A Smarter Way: Create Products Directly from the CSV

    The cell above typed out each product by hand. That works for 6 rows,
    but what if we had 600 products? We already have the data in the `orders` table
    (loaded from the CSV). We can extract the unique products directly:

    **Method 1 — `CREATE TABLE ... AS SELECT` (CTAS)**

    This creates a new table and fills it in one step:
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE products2 AS
        SELECT ROW_NUMBER() OVER (ORDER BY product_name) AS product_id,
               product_name,
               category,
               unit_price
        FROM   orders
        GROUP BY product_name, category, unit_price
        ORDER BY product_name
        """
    )
    return


@app.cell
def _(mo, products2):
    _df = mo.sql(
        f"""
        SELECT * FROM products2 ORDER BY product_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Method 2 — `INSERT INTO ... SELECT` (into an existing table)**

    If the table already exists (with its own schema), you can populate it from a query:
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE products3 (
            product_id   INTEGER PRIMARY KEY,
            product_name VARCHAR NOT NULL,
            category     VARCHAR NOT NULL,
            unit_price   DECIMAL(10,2) NOT NULL
        )
        """
    )
    return


@app.cell
def _(mo, orders, products3):
    _df = mo.sql(
        f"""
        INSERT INTO products3
        SELECT ROW_NUMBER() OVER (ORDER BY product_name) AS product_id,
               product_name,
               category,
               unit_price
        FROM   orders
        GROUP BY product_name, category, unit_price
        ORDER BY product_name
        """
    )
    return


@app.cell
def _(mo, products3):
    _df = mo.sql(
        f"""
        SELECT * FROM products3 ORDER BY product_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### Three Ways to Populate a Table — Summary

    | Method | When to Use It |
    |--------|---------------|
    | `INSERT INTO ... VALUES (...)` | Small, hand-typed data (good for teaching) |
    | `CREATE TABLE ... AS SELECT` | Create + populate in one step from existing data |
    | `INSERT INTO ... SELECT` | Populate an existing table from a query |

    In practice, you'll use the second and third methods most often — real data
    comes from files, other tables, or queries, not from typing values by hand.

    > **Note:** We'll continue using the original `products` table (created above)
    > for the rest of this notebook. The `products2` and `products3` tables were
    > just to demonstrate these techniques.
    """)
    return


@app.cell
def _(mo, products2):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS products2
        """
    )
    return


@app.cell
def _(mo, products3):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS products3
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Sales Table (the normalized orders)
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE sales (
            sale_id     INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(customer_id),
            product_id  INTEGER REFERENCES products(product_id),
            quantity    INTEGER NOT NULL,
            sale_date   DATE NOT NULL
        )
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        INSERT INTO sales VALUES
            (1,  1, 1, 1, '2025-01-10'),
            (2,  1, 2, 2, '2025-01-10'),
            (3,  2, 3, 5, '2025-01-15'),
            (4,  2, 4, 3, '2025-01-15'),
            (5,  3, 1, 1, '2025-02-01'),
            (6,  3, 5, 1, '2025-02-01'),
            (7,  4, 2, 1, '2025-02-05'),
            (8,  4, 6, 4, '2025-02-05'),
            (9,  5, 1, 1, '2025-02-10'),
            (10, 5, 3, 3, '2025-02-10'),
            (11, 6, 4, 10,'2025-02-15'),
            (12, 6, 6, 5, '2025-02-15'),
            (13, 1, 5, 2, '2025-03-01'),
            (14, 1, 3, 4, '2025-03-01'),
            (15, 2, 1, 1, '2025-03-05'),
            (16, 4, 5, 2, '2025-03-10'),
            (17, 5, 2, 2, '2025-03-15'),
            (18, 6, 1, 1, '2025-03-20'),
            (19, 3, 4, 6, '2025-03-25'),
            (20, 4, 3, 2, '2025-03-28')
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT * FROM sales ORDER BY sale_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### A Smarter Way: Create Sales Directly from the CSV

    Just like with products, we typed 20 rows by hand above. In practice,
    we'd extract the sales data from the flat `orders` table and use the
    `customers` and `products` tables to look up the correct IDs.

    **Method 1 — `CREATE TABLE ... AS SELECT` (CTAS)**

    We JOIN the `orders` table back to `customers` and `products` to
    translate names into IDs:
    """)
    return


@app.cell
def _(customers, mo, orders, products):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE sales2 AS
        SELECT o.order_id    AS sale_id,
               c.customer_id,
               p.product_id,
               o.quantity,
               o.order_date  AS sale_date
        FROM   orders o
        JOIN   customers c ON o.customer_name = c.customer_name
        JOIN   products  p ON o.product_name  = p.product_name
        ORDER BY o.order_id
        """
    )
    return


@app.cell
def _(mo, sales2):
    _df = mo.sql(
        f"""
        SELECT * FROM sales2 ORDER BY sale_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Notice what happened: we started with the flat `orders` table (which has names)
    and JOINed it to `customers` and `products` to look up the matching IDs.
    This is a very common real-world pattern:

    ```
    Flat CSV  ──JOIN──>  Lookup tables  ──>  Normalized fact table
    (names)              (name → ID)          (IDs only)
    ```

    **Method 2 — `INSERT INTO ... SELECT`**
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE sales3 (
            sale_id     INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(customer_id),
            product_id  INTEGER REFERENCES products(product_id),
            quantity    INTEGER NOT NULL,
            sale_date   DATE NOT NULL
        )
        """
    )
    return


@app.cell
def _(customers, mo, orders, products, sales3):
    _df = mo.sql(
        f"""
        INSERT INTO sales3
        SELECT o.order_id    AS sale_id,
               c.customer_id,
               p.product_id,
               o.quantity,
               o.order_date  AS sale_date
        FROM   orders o
        JOIN   customers c ON o.customer_name = c.customer_name
        JOIN   products  p ON o.product_name  = p.product_name
        ORDER BY o.order_id
        """
    )
    return


@app.cell
def _(mo, sales3):
    _df = mo.sql(
        f"""
        SELECT * FROM sales3 ORDER BY sale_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### The Big Picture: Normalizing a Flat File

    We just demonstrated the full real-world workflow:

    ```
      orders_data.csv         (flat, redundant)
            │
            ├──> customers     (extracted unique customers)
            ├──> products      (extracted unique products)
            └──> sales         (JOINed back to get IDs)
    ```

    | Step | What You Do | SQL Technique |
    |------|-------------|---------------|
    | 1. Load CSV | `CREATE TABLE orders AS SELECT * FROM read_csv_auto(...)` | CTAS from file |
    | 2. Extract dimensions | `SELECT DISTINCT ...` with `ROW_NUMBER()` | CTAS from query |
    | 3. Build fact table | `JOIN` flat table to dimensions to get IDs | INSERT...SELECT with JOINs |

    This is exactly how data warehouses are built — flat files come in,
    and SQL transforms them into clean, normalized tables.

    > **Note:** We'll continue using the original `sales` table for the rest
    > of this notebook.
    """)
    return


@app.cell
def _(mo, sales2):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS sales2
        """
    )
    return


@app.cell
def _(mo, sales3):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS sales3
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### What Changed?

    | Before (flat CSV) | After (3 tables) |
    |-------------------|-------------------|
    | Alice's city stored 4 times | Alice's city stored **once** in customers |
    | Laptop's price stored 4 times | Laptop's price stored **once** in products |
    | 20 rows × 9 columns = 180 cells | Much less total data, zero redundancy |
    | Change Alice's city → update 4 rows | Change Alice's city → update **1 row** |

    The sales table uses `customer_id` and `product_id` as **foreign keys** — they
    point back to the customers and products tables. This is the **relational model**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 2.3 — INNER JOIN: Reconnecting the Tables

    The sales table has IDs, not names. To see names, we **JOIN** the tables back together.

    > *Business question: "Show every sale with the customer name and product name."*
    """)
    return


@app.cell
def _(customers, mo, products, sales):
    _df = mo.sql(
        f"""
        SELECT s.sale_id,
               c.customer_name,
               p.product_name,
               p.unit_price,
               s.quantity,
               ROUND(p.unit_price * s.quantity, 2) AS sale_total,
               s.sale_date
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        ORDER BY s.sale_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### How JOIN Works

    ```
    FROM   sales s                              ← start with sales
    JOIN   customers c ON s.customer_id = c.customer_id  ← match each sale to its customer
    JOIN   products  p ON s.product_id  = p.product_id   ← match each sale to its product
    ```

    The `ON` clause is the matching rule. For each sale, SQL finds the customer with
    the same `customer_id` and the product with the same `product_id`, then combines
    the columns into one row.

    ### More JOIN Examples

    > *"How much has each customer spent in total?"*
    """)
    return


@app.cell
def _(customers, mo, products, sales):
    _df = mo.sql(
        f"""
        SELECT c.customer_name,
               c.tier,
               COUNT(*)                                AS num_orders,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS total_spent
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.customer_name, c.tier
        ORDER BY total_spent DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"What is the total revenue per city?"*
    """)
    return


@app.cell
def _(customers, mo, products, sales):
    _df = mo.sql(
        f"""
        SELECT c.city,
               COUNT(*)                                AS num_orders,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS revenue
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.city
        ORDER BY revenue DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 2.4 — LEFT JOIN: Keep Everything from the Left Table

    INNER JOIN only returns rows with matches in **both** tables.
    LEFT JOIN keeps **all** rows from the left table, even if there's no match.

    To demonstrate, let's add a customer who has never placed an order:
    """)
    return


@app.cell
def _(customers, mo):
    _df = mo.sql(
        f"""
        -- Add Grace — safe to re-run (skips if she already exists)
        INSERT INTO customers
        SELECT 7, 'Grace', 'Palo Alto', 'Gold'
        WHERE NOT EXISTS (SELECT 1 FROM customers WHERE customer_id = 7)
        """
    )
    return


@app.cell
def _(customers, mo, sales):
    _df = mo.sql(
        f"""
        -- INNER JOIN: Grace does NOT appear (no matching sales)
        SELECT c.customer_name,
               COUNT(s.sale_id) AS num_orders
        FROM   customers c
        JOIN   sales s ON c.customer_id = s.customer_id
        GROUP BY c.customer_name
        ORDER BY c.customer_name
        """
    )
    return


@app.cell
def _(customers, mo, sales):
    _df = mo.sql(
        f"""
        -- LEFT JOIN: Grace DOES appear (with 0 orders)
        SELECT c.customer_name,
               COUNT(s.sale_id) AS num_orders
        FROM   customers c
        LEFT JOIN sales s ON c.customer_id = s.customer_id
        GROUP BY c.customer_name
        ORDER BY num_orders ASC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Finding "Missing" Data with LEFT JOIN + IS NULL

    > *"Which customers have NEVER placed an order?"*
    """)
    return


@app.cell
def _(customers, mo, sales):
    _df = mo.sql(
        f"""
        SELECT c.customer_name, c.city, c.tier
        FROM   customers c
        LEFT JOIN sales s ON c.customer_id = s.customer_id
        WHERE  s.sale_id IS NULL
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    This is one of the most useful patterns in SQL:
    `LEFT JOIN` + `WHERE right_table.key IS NULL` = "find everything with no match."

    ---
    ### Week 2 Summary

    | Concept | What It Solves |
    |---------|---------------|
    | Redundancy / Anomalies | Why one flat table causes problems |
    | Normalization | Split into multiple tables to eliminate redundancy |
    | PRIMARY KEY | Uniquely identifies each row |
    | FOREIGN KEY | Links one table to another |
    | INNER JOIN | Combine tables — only matching rows |
    | LEFT JOIN | Combine tables — keep all rows from the left table |
    | LEFT JOIN + IS NULL | Find rows with no match ("who hasn't ordered?") |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # WEEK 3 — Aggregation, Grouping, Plots & Subqueries

    ---

    ## 3.1 — GROUP BY & Aggregate Functions

    `GROUP BY` collapses many rows into **one row per group**.
    Aggregate functions tell SQL *how* to collapse them.

    | Function | What It Computes |
    |----------|-----------------|
    | `COUNT(*)` | Number of rows in each group |
    | `SUM(col)` | Total of a numeric column |
    | `AVG(col)` | Average value |
    | `MIN(col)` | Smallest value |
    | `MAX(col)` | Largest value |
    | `ROUND(val, n)` | Round to n decimal places |

    > *"How many orders and how much revenue per product category?"*
    """)
    return


@app.cell
def _(mo, products, sales):
    df_cat = mo.sql(
        f"""
        SELECT p.category,
               COUNT(*)                                AS num_orders,
               SUM(s.quantity)                         AS units_sold,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS revenue
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC
        """
    )
    return (df_cat,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Revenue by Category
    """)
    return


@app.cell
def _(df_cat, plot_bar):
    plot_bar(df_cat, x='category', y='revenue',
             title='Revenue by Product Category', ylabel='Revenue', dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"Revenue per customer — who are our biggest spenders?"*
    """)
    return


@app.cell
def _(customers, mo, products, sales):
    df_cust = mo.sql(
        f"""
        SELECT c.customer_name,
               c.tier,
               COUNT(*)                                AS num_orders,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS total_spent
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.customer_name, c.tier
        ORDER BY total_spent DESC
        """
    )
    return (df_cust,)


@app.cell
def _(df_cust, plot_hbar):
    plot_hbar(df_cust, x='total_spent', y='customer_name',
              title='Total Spending by Customer', xlabel='Amount Spent', dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3.2 — GROUP BY Multiple Columns

    > *"Revenue by city and customer tier?"*
    """)
    return


@app.cell
def _(customers, mo, products, sales):
    _df = mo.sql(
        f"""
        SELECT c.city,
               c.tier,
               COUNT(*)                                AS num_orders,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS revenue
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.city, c.tier
        ORDER BY c.city, revenue DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"How many units of each product were sold?"*
    """)
    return


@app.cell
def _(mo, products, sales):
    df_prod = mo.sql(
        f"""
        SELECT p.product_name,
               p.category,
               SUM(s.quantity) AS units_sold,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS revenue
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        GROUP BY p.product_name, p.category
        ORDER BY revenue DESC
        """
    )
    return (df_prod,)


@app.cell
def _(df_prod, plot_hbar):
    plot_hbar(df_prod, x='revenue', y='product_name',
              title='Revenue by Product', xlabel='Revenue', dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3.3 — GROUP BY with Dates

    > *"What is the monthly revenue trend?"*

    We use `STRFTIME` to extract the month from the date:
    """)
    return


@app.cell
def _(mo, products, sales):
    df_monthly = mo.sql(
        f"""
        SELECT STRFTIME(s.sale_date, '%Y-%m')           AS month,
               COUNT(*)                                  AS num_orders,
               ROUND(SUM(p.unit_price * s.quantity), 2)  AS revenue
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        GROUP BY month
        ORDER BY month
        """
    )
    return (df_monthly,)


@app.cell
def _(df_monthly, plot_bar):
    plot_bar(df_monthly, x='month', y='revenue',
             title='Monthly Revenue Trend', ylabel='Revenue', dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"What share of revenue comes from each category?"*
    """)
    return


@app.cell
def _(df_cat, plot_pie):
    plot_pie(df_cat, labels='category', values='revenue',
             title='Revenue Share by Category')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3.4 — HAVING (Filter Groups)

    `WHERE` filters **individual rows** (before grouping).
    `HAVING` filters **groups** (after grouping).

    > *"Which products generated more than $100 in total revenue?"*
    """)
    return


@app.cell
def _(mo, products, sales):
    _df = mo.sql(
        f"""
        SELECT p.product_name,
               SUM(s.quantity)                         AS units_sold,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS revenue
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        GROUP BY p.product_name
        HAVING SUM(p.unit_price * s.quantity) > 100
        ORDER BY revenue DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"Which customers placed more than 3 orders?"*
    """)
    return


@app.cell
def _(customers, mo, sales):
    _df = mo.sql(
        f"""
        SELECT c.customer_name,
               COUNT(*) AS num_orders
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        GROUP BY c.customer_name
        HAVING COUNT(*) > 3
        ORDER BY num_orders DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Combining WHERE + GROUP BY + HAVING

    > *"Among Electronics orders only, which customers spent more than $500?"*
    """)
    return


@app.cell
def _(customers, mo, products, sales):
    _df = mo.sql(
        f"""
        SELECT c.customer_name,
               COUNT(*)                                AS electronics_orders,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS electronics_spent
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        WHERE  p.category = 'Electronics'
        GROUP BY c.customer_name
        HAVING SUM(p.unit_price * s.quantity) > 500
        ORDER BY electronics_spent DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### SQL Execution Order

    This is the order SQL **actually processes** your query:

    ```
    1. FROM / JOIN     → pick the tables and combine them
    2. WHERE           → filter individual rows
    3. GROUP BY        → collapse rows into groups
    4. HAVING          → filter the groups
    5. SELECT          → choose which columns to show
    6. ORDER BY        → sort the final result
    7. LIMIT           → return only the first N rows
    ```

    This explains why `WHERE` can't use `AVG(salary)` — aggregation hasn't happened yet at step 2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3.5 — Subqueries: A Query Inside a Query

    Sometimes a business question requires **two steps**:
    1. Compute a value (like an average)
    2. Use that value to filter

    A subquery lets you do both in one SQL statement.

    > *"Which orders have a total above the average order total?"*
    """)
    return


@app.cell
def _(mo, products, sales):
    _df = mo.sql(
        f"""
        -- First, what IS the average order total?
        SELECT ROUND(AVG(p.unit_price * s.quantity), 2) AS avg_order_total
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        """
    )
    return


@app.cell
def _(customers, mo, products, sales):
    _df = mo.sql(
        f"""
        -- Now use that as a subquery in WHERE
        SELECT s.sale_id,
               c.customer_name,
               p.product_name,
               ROUND(p.unit_price * s.quantity, 2) AS order_total
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        WHERE  p.unit_price * s.quantity > (
                   SELECT AVG(p2.unit_price * s2.quantity)
                   FROM   sales s2
                   JOIN   products p2 ON s2.product_id = p2.product_id
               )
        ORDER BY order_total DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"Which customer spent the most overall?"*
    """)
    return


@app.cell
def _(customers, mo, products, sales):
    _df = mo.sql(
        f"""
        SELECT c.customer_name,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS total_spent
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.customer_name
        ORDER BY total_spent DESC
        LIMIT 1
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"Show each customer's spending alongside the company average"*
    """)
    return


@app.cell
def _(customers, mo, products, sales):
    _df = mo.sql(
        f"""
        SELECT c.customer_name,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS customer_total,
               (SELECT ROUND(AVG(sub.total), 2)
                FROM (SELECT SUM(p2.unit_price * s2.quantity) AS total
                      FROM   sales s2
                      JOIN   products p2 ON s2.product_id = p2.product_id
                      GROUP BY s2.customer_id) sub
               ) AS avg_customer_total
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.customer_name
        ORDER BY customer_total DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"Which customers spend MORE than the average customer?"*
    """)
    return


@app.cell
def _(customers, mo, products, sales):
    _df = mo.sql(
        f"""
        SELECT c.customer_name,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS total_spent
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.customer_name
        HAVING SUM(p.unit_price * s.quantity) > (
                   SELECT AVG(sub.total)
                   FROM (SELECT SUM(p2.unit_price * s2.quantity) AS total
                         FROM   sales s2
                         JOIN   products p2 ON s2.product_id = p2.product_id
                         GROUP BY s2.customer_id) sub
               )
        ORDER BY total_spent DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3.6 — One More Visualization

    > *"Show min and max order totals per category side by side."*
    """)
    return


@app.cell
def _(mo, products, sales):
    df_range = mo.sql(
        f"""
        SELECT p.category,
               ROUND(MIN(p.unit_price * s.quantity), 2) AS min_order,
               ROUND(MAX(p.unit_price * s.quantity), 2) AS max_order
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY p.category
        """
    )
    return (df_range,)


@app.cell
def _(df_range, plot_grouped_bar):
    plot_grouped_bar(df_range, x='category', y_cols=['min_order', 'max_order'],
                     title='Order Value Range by Category',
                     ylabel='Order Total', dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # Summary — What You Learned in 3 Weeks

    | Week | Concepts | SQL Keywords |
    |------|----------|-------------|
    | **1** | Query a single table | `SELECT`, `WHERE`, `AND/OR`, `IN`, `BETWEEN`, `LIKE`, `ORDER BY`, `LIMIT`, `DISTINCT`, `COUNT` |
    | **2** | Relational design & combining tables | `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`, `JOIN` (INNER), `LEFT JOIN`, `IS NULL` |
    | **3** | Aggregation, reporting & subqueries | `GROUP BY`, `HAVING`, `SUM`, `AVG`, `MIN`, `MAX`, subqueries |

    ### The Journey of Our Data

    ```
     orders_data.csv            →    customers + products + sales
     (flat, redundant)               (normalized, clean)
           ↓                                  ↓
     Week 1: query it as-is          Week 2: design & JOIN
                                              ↓
                                     Week 3: aggregate, plot, compare
    ```

    ### Files in This Folder

    | File | Purpose |
    |------|---------|
    | `orders_data.csv` | The raw dataset (20 orders) |
    | `plot_helpers.py` | Plotting functions (decoupled from notebook) |
    | `OMIS105_Weeks_1_3_marimo.py` | This notebook |

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
