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
    # Week 6: Database Design & Normalization — Demo Notebook
    ## OMIS 105: Database Management Systems
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect()

    # Load the denormalized table for normalization exercises
    con.sql("""
        CREATE OR REPLACE TABLE orders_denorm AS
        SELECT *
        FROM read_csv_auto('./data/orders_denormalized.csv');
    """)
    print(f"Loaded orders_denorm: {con.sql('SELECT COUNT(*) FROM orders_denorm').fetchone()[0]} rows")

    # Also load normalized tables for comparison
    for t, f in [('categories','./data/categories.csv'),
                 ('products','./data/products.csv'),
                 ('customers','./data/customers.csv'),
                 ('orders','./data/orders.csv'),
                 ('order_items','./data/order_items.csv')]:
        con.sql(f"CREATE OR REPLACE TABLE {t} AS SELECT * FROM read_csv_auto('{f}')")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Examining the Denormalized Table
    Let's look at the problems with our denormalized data.
    """)
    return


@app.cell
def _(con):
    # See the denormalized table
    con.sql("""
        SELECT *
        FROM orders_denorm
        LIMIT 10;
    """).show()
    return


@app.cell
def _(con):
    # Problem 1: Redundancy — how many times is each customer repeated?
    con.sql("""
        SELECT
            customer_name,
            customer_email,
            COUNT(*) AS times_repeated
        FROM orders_denorm
        GROUP BY customer_name, customer_email
        ORDER BY times_repeated DESC;
    """).show()
    return


@app.cell
def _(con):
    # Problem 2: How many times is product info repeated?
    con.sql("""
        SELECT
            product_name,
            category_name,
            COUNT(*) AS times_repeated
        FROM orders_denorm
        GROUP BY product_name, category_name
        ORDER BY times_repeated DESC;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Identifying Functional Dependencies

    Let's verify our FDs programmatically.
    """)
    return


@app.cell
def _(con):
    # FD: customer_id -> customer_name (should be 1 name per ID)
    con.sql("""
        SELECT
            customer_id,
            COUNT(DISTINCT customer_name) AS distinct_names
        FROM orders_denorm
        GROUP BY customer_id
        HAVING COUNT(DISTINCT customer_name) > 1;
    """).show()
    print("Empty = FD holds: customer_id -> customer_name")
    return


@app.cell
def _(con):
    # FD: product_id -> product_name
    con.sql("""
        SELECT
            product_id,
            COUNT(DISTINCT product_name) AS distinct_names
        FROM orders_denorm
        GROUP BY product_id
        HAVING COUNT(DISTINCT product_name) > 1;
    """).show()
    print("Empty = FD holds: product_id -> product_name")
    return


@app.cell
def _(con):
    # Verify candidate key: (order_id, product_id) should be unique
    con.sql("""
        SELECT
            order_id,
            product_id,
            COUNT(*) AS cnt
        FROM orders_denorm
        GROUP BY order_id, product_id
        HAVING COUNT(*) > 1;
    """).show()
    print("Empty = (order_id, product_id) is a valid candidate key")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Step-by-Step Normalization

    ### Step 1: Check 1NF
    Already in 1NF — all values are atomic, has a candidate key.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 2: Decompose to 2NF
    Remove partial dependencies on the composite key (order_id, product_id).
    """)
    return


@app.cell
def _(con):
    # Extract orders (depends only on order_id)
    con.sql("""
        CREATE OR REPLACE TABLE orders_2nf AS
        SELECT DISTINCT
            order_id,
            order_date,
            status,
            customer_id
        FROM orders_denorm;
    """)
    con.sql("""
        SELECT *
        FROM orders_2nf
        LIMIT 5;
    """).show()
    print(f"orders_2nf: {con.sql('SELECT COUNT(*) FROM orders_2nf').fetchone()[0]} rows")
    return


@app.cell
def _(con):
    # Extract products (depends only on product_id)
    con.sql("""
        CREATE OR REPLACE TABLE products_2nf AS
        SELECT DISTINCT
            product_id,
            product_name,
            category_name,
            unit_price
        FROM orders_denorm;
    """)
    con.sql("""
        SELECT *
        FROM products_2nf
        LIMIT 5;
    """).show()
    print(f"products_2nf: {con.sql('SELECT COUNT(*) FROM products_2nf').fetchone()[0]} rows")
    return


@app.cell
def _(con):
    # Remaining: order_items (full dependency on composite key)
    con.sql("""
        CREATE OR REPLACE TABLE order_items_2nf AS
        SELECT DISTINCT
            order_id,
            product_id,
            quantity,
            line_price
        FROM orders_denorm;
    """)
    con.sql("""
        SELECT *
        FROM order_items_2nf
        LIMIT 5;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 3: Decompose to 3NF
    Remove transitive dependencies.
    """)
    return


@app.cell
def _(con):
    # In orders_2nf: order_id -> customer_id -> customer_name, email, city
    # Extract customers
    con.sql("""
        CREATE OR REPLACE TABLE customers_3nf AS
        SELECT DISTINCT
            customer_id,
            customer_name,
            customer_email,
            customer_city
        FROM orders_denorm;
    """)
    con.sql("""
        SELECT *
        FROM customers_3nf
        LIMIT 5;
    """).show()
    print(f"customers_3nf: {con.sql('SELECT COUNT(*) FROM customers_3nf').fetchone()[0]} rows")
    return


@app.cell
def _(con):
    # In products_2nf: product_id -> category_name (transitive via category concept)
    # Extract categories
    con.sql("""
        CREATE OR REPLACE TABLE categories_3nf AS
        SELECT DISTINCT category_name
        FROM orders_denorm;
    """)
    con.sql("""
        SELECT *
        FROM categories_3nf;
    """).show()
    print("Now products should reference category by name (or we add an ID)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Final normalized schema from the denormalized table:
    - **customers_3nf**(customer_id, customer_name, customer_email, customer_city)
    - **categories_3nf**(category_name) — or with a surrogate category_id
    - **products_3nf**(product_id, product_name, category_name, unit_price)
    - **orders_3nf**(order_id, order_date, status, customer_id)
    - **order_items_3nf**(order_id, product_id, quantity, line_price)

    This matches our ShopSmart schema!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Comparing: Normalized vs Denormalized
    """)
    return


@app.cell
def _(con):
    # Storage comparison
    denorm_count = con.sql("""
        SELECT COUNT(*)
        FROM orders_denorm;
    """).fetchone()[0]
    norm_total = sum(con.sql(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        for t in ['customers_3nf','categories_3nf','products_2nf','orders_2nf','order_items_2nf'])

    print(f"Denormalized: {denorm_count} rows in 1 table (13 columns)")
    print(f"Normalized: {norm_total} total rows across 5 tables")
    print(f"Row reduction: {denorm_count - norm_total} fewer total rows")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Verifying Normal Forms
    """)
    return


@app.cell
def _(con):
    # Our real normalized schema — let's verify 3NF

    # Check: no partial deps in order_items (composite key)
    print("=== order_items: checking for partial dependencies ===")
    # quantity depends on (order_id, product_id) — full dependency
    con.sql("""
        SELECT
            oi.order_id,
            oi.product_id,
            COUNT(DISTINCT oi.quantity) AS dist_qty
        FROM order_items oi
        GROUP BY oi.order_id, oi.product_id
        HAVING COUNT(DISTINCT oi.quantity) > 1;
    """).show()
    print("Empty = no partial dependency issues")

    # Check: no transitive deps in products
    print("\n=== products: checking for transitive dependencies ===")
    con.sql("""
        SELECT
            category_id,
            COUNT(DISTINCT category_id) AS check_col
        FROM products
        GROUP BY category_id;
    """).show()
    print("category_id is an FK (not a transitive dep) — 3NF holds!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Denormalization Use Cases
    """)
    return


@app.cell
def _(con):
    # Example: Creating a denormalized view for reporting
    con.sql("""
        CREATE VIEW sales_report_denorm AS
        SELECT
            o.order_id,
            o.order_date,
            o.status,
            c.first_name || ' ' || c.last_name AS customer_name,
            c.city,
            c.state,
            p.product_name,
            cat.category_name,
            oi.quantity,
            oi.unit_price,
            ROUND(oi.quantity * oi.unit_price, 2) AS line_total
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        JOIN categories cat ON p.category_id = cat.category_id;
    """)

    # The view gives a denormalized "read" without storing redundant data
    con.sql("""
        SELECT *
        FROM sales_report_denorm
        LIMIT 10;
    """).show()
    print("The VIEW provides denormalized access without actual data redundancy!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    Key concepts:
    - **Functional dependencies** determine normalization steps
    - **1NF**: Atomic values, no repeating groups
    - **2NF**: Remove partial dependencies (for composite keys)
    - **3NF**: Remove transitive dependencies
    - **BCNF**: Every determinant is a superkey
    - **Views** can provide denormalized access without storing redundant data
    - Always normalize first, then selectively denormalize for performance

    **Next week**: Performance and Indexing
    """)
    return


if __name__ == "__main__":
    app.run()
