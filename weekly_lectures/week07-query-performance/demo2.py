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
    # Week 7: Performance & Indexing — Demo Notebook
    ## OMIS 105: Database Management Systems
    """)
    return


@app.cell
def _():
    import duckdb, time
    con = duckdb.connect()
    for t, f in [('categories','./data/categories.csv'),
                 ('products','./data/products.csv'),
                 ('customers','./data/customers.csv'),
                 ('orders','./data/orders.csv'),
                 ('order_items','./data/order_items.csv'),
                 ('reviews','./data/reviews.csv'),
                 ('shipping','./data/shipping.csv')]:
        con.sql(f"CREATE OR REPLACE TABLE {t} AS SELECT * FROM read_csv_auto('{f}')")
        print(f"Loaded {t}: {con.sql(f'SELECT COUNT(*) FROM {t}').fetchone()[0]} rows")
    return (con, time)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Full Table Scan vs. Index Lookup
    """)
    return


@app.cell
def _(con, time):
    # Without index — full scan
    start = time.time()
    con.sql("""
        SELECT *
        FROM products
        WHERE price > 100;
    """).fetchall()
    print(f"Full scan: {(time.time()-start)*1000:.2f}ms")
    return


@app.cell
def _(con, time):
    # Create an index
    con.sql("""
        CREATE INDEX idx_products_price ON products(price);
    """)
    start2 = time.time()
    con.sql("""
        SELECT *
        FROM products
        WHERE price > 100;
    """).fetchall()
    print(f"With index: {(time.time()-start2)*1000:.2f}ms")
    print("(Small dataset — difference minimal. Impact grows with millions of rows)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. EXPLAIN — Seeing the Query Plan
    """)
    return


@app.cell
def _(con):
    # View the execution plan
    con.sql("""
        EXPLAIN
        SELECT *
        FROM products
        WHERE price > 100;
    """).show()
    return


@app.cell
def _(con):
    # Explain a JOIN query
    con.sql("""
        EXPLAIN
        SELECT
            c.first_name,
            o.order_id,
            o.total_amount
        FROM customers c
        INNER
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.total_amount > 500;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Index Types and Usage
    """)
    return


@app.cell
def _(con):
    # Single column index
    con.sql("""
        CREATE INDEX idx_orders_status ON orders(status);
    """)

    # Composite index
    con.sql("""
        CREATE INDEX idx_orders_cust_date ON orders(customer_id, order_date);
    """)

    # List all indexes
    con.sql("""
        SELECT *
        FROM duckdb_indexes();
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Query Optimization Techniques
    """)
    return


@app.cell
def _(con, time):
    # Technique 1: Select only needed columns
    start3 = time.time()
    con.sql("""
        SELECT *
        FROM orders;
    """).fetchall()
    t1 = time.time() - start3

    start4 = time.time()
    con.sql("""
        SELECT
            order_id,
            total_amount
        FROM orders;
    """).fetchall()
    t2 = time.time() - start4

    print(f"SELECT *: {t1*1000:.2f}ms")
    print(f"SELECT specific cols: {t2*1000:.2f}ms")
    return


@app.cell
def _(con):
    # Technique 2: EXISTS vs IN
    con.sql("""
        EXPLAIN
        SELECT *
        FROM customers
        WHERE customer_id IN (
        SELECT customer_id
        FROM orders);
    """).show()
    print("--- vs ---")
    con.sql("""
        EXPLAIN
        SELECT *
        FROM customers c
        WHERE EXISTS (
        SELECT 1
        FROM orders o
        WHERE o.customer_id = c.customer_id);
    """).show()
    return


@app.cell
def _(con):
    # Technique 3: Avoid functions on indexed columns
    # BAD
    con.sql("""
        EXPLAIN
        SELECT *
        FROM orders
        WHERE EXTRACT(YEAR
        FROM order_date) = 2024;
    """).show()
    print("--- vs ---")
    # GOOD
    con.sql("""
        EXPLAIN
        SELECT *
        FROM orders
        WHERE order_date >= '2024-01-01'
        AND order_date < '2025-01-01';
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. DuckDB Columnar Storage
    """)
    return


@app.cell
def _(con):
    # DuckDB reads only the columns you need (columnar advantage)
    con.sql("""
        EXPLAIN ANALYZE
        SELECT SUM(total_amount)
        FROM orders;
    """).show()
    return


@app.cell
def _(con, time):
    # Aggregation performance on larger data
    con.sql("""
        CREATE OR REPLACE TABLE orders_big AS
        SELECT *
        FROM orders
        UNION ALL
        SELECT *
        FROM orders
        UNION ALL
        SELECT *
        FROM orders
        UNION ALL
        SELECT *
        FROM orders
        UNION ALL
        SELECT *
        FROM orders;
    """)
    cnt = con.sql("""
        SELECT COUNT(*)
        FROM orders_big;
    """).fetchone()[0]
    print(f"orders_big: {cnt} rows")

    start5 = time.time()
    con.sql("""
        SELECT
            status,
            SUM(total_amount)
        FROM orders_big
        GROUP BY status;
    """).fetchall()
    print(f"Aggregation on {cnt} rows: {(time.time()-start5)*1000:.2f}ms")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Practical Optimization: Before vs After
    """)
    return


@app.cell
def _(con):
    # Complex query — before optimization
    con.sql("""
        EXPLAIN
        SELECT *
        FROM customers c
        LEFT
        JOIN orders o ON c.customer_id = o.customer_id
        LEFT
        JOIN order_items oi ON o.order_id = oi.order_id
        LEFT
        JOIN products p ON oi.product_id = p.product_id
        WHERE p.category_id = 1;
    """).show()
    return


@app.cell
def _(con):
    # After optimization: filter early, select needed columns
    con.sql("""
        EXPLAIN
        SELECT
            c.first_name,
            c.last_name,
            p.product_name,
            oi.quantity
        FROM order_items oi
        INNER
        JOIN products p ON oi.product_id = p.product_id
        AND p.category_id = 1
        INNER
        JOIN orders o ON oi.order_id = o.order_id
        INNER
        JOIN customers c ON o.customer_id = c.customer_id;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    Key takeaways:
    - **Indexes** speed up reads but slow writes (B-Tree is most common)
    - **EXPLAIN** reveals how the DBMS executes your query
    - Optimization: filter early, select only needed columns, use EXISTS over IN
    - **DuckDB** uses columnar storage for fast analytics
    - Always **measure** performance before and after changes

    **Next week**: Transactions and ACID properties
    """)
    return


if __name__ == "__main__":
    app.run()
