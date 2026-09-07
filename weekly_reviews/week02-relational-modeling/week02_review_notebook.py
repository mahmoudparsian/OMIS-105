import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from pathlib import Path

    import duckdb

    DATA_DIR = Path(__file__).parent / "data"
    con = duckdb.connect(database=":memory:")
    return DATA_DIR, con


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # OMIS 105 — Week 2 Review: Relational Design & JOINs

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    One flat table repeats the same customer and product facts over and
    over. This week we split `orders_data.csv` into three clean tables and
    then reconnect them with `JOIN`.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | Spot the problem | Redundancy, update / insert / delete anomalies |
    | Design tables | `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY` |
    | Populate tables | `INSERT INTO`, `CREATE TABLE AS SELECT` |
    | Reconnect them | `INNER JOIN`, `LEFT JOIN`, `LEFT JOIN` + `IS NULL` |

    ### How to Use

    Run the cells from top to bottom. Every database cell takes `con`, the
    DuckDB connection created in the setup cell. Read the markdown between
    queries — it explains the *why*, not just the *how*.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Setup — Load the CSV into DuckDB

    `orders_data.csv` lives in this folder's `data/` directory. DuckDB can read
    a CSV straight into a table — no import wizard, no schema definition.
    """)
    return


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE orders AS
            SELECT * FROM read_csv_auto('{DATA_DIR}/orders_data.csv');
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT 'orders_data.csv loaded!' AS status,
               COUNT(*) AS total_rows
        FROM orders;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 2.1 — The Problem: Redundancy in Our Data

    Look carefully at our CSV. Alice appears in **4 rows**. Every time, her city
    ("San Jose") and tier ("Gold") are repeated. What's wrong with that?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Alice's data is repeated in every row
        SELECT order_id, customer_name, customer_city, customer_tier
        FROM   orders
        WHERE  customer_name = 'Alice'
        ORDER BY order_id
        """
    ).fetchdf()
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM customers ORDER BY customer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Products Table
    """)
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM products ORDER BY product_id
        """
    ).fetchdf()
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM products2 ORDER BY product_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Method 2 — `INSERT INTO ... SELECT` (into an existing table)**

    If the table already exists (with its own schema), you can populate it from a query:
    """)
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM products3 ORDER BY product_id
        """
    ).fetchdf()
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
def _(con):
    con.execute(
        f"""
        DROP TABLE IF EXISTS products2
        """
    )
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM sales ORDER BY sale_id
        """
    ).fetchdf()
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM sales2 ORDER BY sale_id
        """
    ).fetchdf()
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM sales3 ORDER BY sale_id
        """
    ).fetchdf()
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
def _(con):
    con.execute(
        f"""
        DROP TABLE IF EXISTS sales2
        """
    )
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"What is the total revenue per city?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
        f"""
        -- Add Grace — safe to re-run (skips if she already exists)
        INSERT INTO customers
        SELECT 7, 'Grace', 'Palo Alto', 'Gold'
        WHERE NOT EXISTS (SELECT 1 FROM customers WHERE customer_id = 7)
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- INNER JOIN: Grace does NOT appear (no matching sales)
        SELECT c.customer_name,
               COUNT(s.sale_id) AS num_orders
        FROM   customers c
        JOIN   sales s ON c.customer_id = s.customer_id
        GROUP BY c.customer_name
        ORDER BY c.customer_name
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- LEFT JOIN: Grace DOES appear (with 0 orders)
        SELECT c.customer_name,
               COUNT(s.sale_id) AS num_orders
        FROM   customers c
        LEFT JOIN sales s ON c.customer_id = s.customer_id
        GROUP BY c.customer_name
        ORDER BY num_orders ASC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Finding "Missing" Data with LEFT JOIN + IS NULL

    > *"Which customers have NEVER placed an order?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.customer_name, c.city, c.tier
        FROM   customers c
        LEFT JOIN sales s ON c.customer_id = s.customer_id
        WHERE  s.sale_id IS NULL
        """
    ).fetchdf()
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
    mo.md(r"""
    ---
    ## Looking Ahead

    You can now design tables and put them back together. Week 3 uses those same
    three tables to answer *summary* questions — totals, averages, and rankings
    per category, customer, and month.
    """)
    return


if __name__ == "__main__":
    app.run()
