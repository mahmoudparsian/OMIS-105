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
    # Week 4: SQL Mastery Part 2 — JOINs and Multi-Table Queries
    ## OMIS 105: Database Management Systems
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
        f"""
        CREATE OR REPLACE TABLE categories AS
            SELECT * FROM read_csv_auto('./data/categories.csv')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE products AS
            SELECT * FROM read_csv_auto('./data/products.csv')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE customers AS
            SELECT * FROM read_csv_auto('./data/customers.csv')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE orders AS
            SELECT * FROM read_csv_auto('./data/orders.csv')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE order_items AS
            SELECT * FROM read_csv_auto('./data/order_items.csv')
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. INNER JOIN Basics
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    c.first_name,
                    c.last_name,
                    o.order_id,
                    o.order_date,
                    o.total_amount
                FROM customers c
                INNER
                JOIN orders o ON c.customer_id = o.customer_id
                ORDER BY o.order_date DESC
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    p.product_name,
                    cat.category_name,
                    p.price
                FROM products p
                INNER
                JOIN categories cat ON p.category_id = cat.category_id
                ORDER BY cat.category_name, p.price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. LEFT JOIN — Finding Non-Matches
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    c.first_name,
                    c.last_name,
                    o.order_id,
                    o.total_amount
                FROM customers c
                LEFT
                JOIN orders o ON c.customer_id = o.customer_id
                ORDER BY o.order_id IS NULL DESC, c.last_name
                LIMIT 15
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    c.first_name,
                    c.last_name,
                    c.email
                FROM customers c
                LEFT
                JOIN orders o ON c.customer_id = o.customer_id
                WHERE o.order_id IS NULL
                ORDER BY c.last_name
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    p.product_name,
                    p.category_id,
                    p.price
                FROM products p
                LEFT
                JOIN order_items oi ON p.product_id = oi.product_id
                WHERE oi.item_id IS NULL
                ORDER BY p.price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Joining Multiple Tables
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    c.first_name || ' ' || c.last_name AS customer,
                    o.order_id,
                    o.order_date,
                    o.status,
                    p.product_name,
                    oi.quantity,
                    oi.unit_price,
                    ROUND(oi.quantity * oi.unit_price, 2) AS line_total
                FROM customers c
                INNER
                JOIN orders o ON c.customer_id = o.customer_id
                INNER
                JOIN order_items oi ON o.order_id = oi.order_id
                INNER
                JOIN products p ON oi.product_id = p.product_id
                ORDER BY o.order_date DESC
                LIMIT 15
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. JOINs with GROUP BY
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    c.first_name,
                    c.last_name,
                    COUNT(DISTINCT o.order_id) AS num_orders,
                    ROUND(SUM(o.total_amount), 2) AS total_spent
                FROM customers c
                INNER
                JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id, c.first_name, c.last_name
                ORDER BY total_spent DESC
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    cat.category_name,
                    COUNT(DISTINCT oi.order_id) AS orders_with_category,
                    SUM(oi.quantity) AS units_sold,
                    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
                FROM order_items oi
                INNER
                JOIN products p ON oi.product_id = p.product_id
                INNER
                JOIN categories cat ON p.category_id = cat.category_id
                GROUP BY cat.category_name
                ORDER BY revenue DESC
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    p.product_name,
                    SUM(oi.quantity) AS total_units,
                    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
                FROM order_items oi
                INNER
                JOIN products p ON oi.product_id = p.product_id
                GROUP BY p.product_id, p.product_name
                ORDER BY total_revenue DESC
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. JOINs with HAVING
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    c.first_name,
                    c.last_name,
                    ROUND(SUM(o.total_amount), 2) AS total_spent
                FROM customers c
                INNER
                JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id, c.first_name, c.last_name
                HAVING SUM(o.total_amount) > 500
                ORDER BY total_spent DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Self JOIN
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    p1.product_name AS product_a,
                    p2.product_name AS product_b,
                    p1.category_id,
                    ROUND(ABS(p1.price - p2.price), 2) AS price_diff
                FROM products p1
                INNER
                JOIN products p2 ON p1.category_id = p2.category_id
                AND p1.product_id < p2.product_id
                WHERE ABS(p1.price - p2.price) < 10
                ORDER BY price_diff
                LIMIT 15
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Derived Tables (Subqueries in FROM)
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    c.first_name,
                    c.last_name,
                    co.total_spent,
                    co.num_orders
                FROM customers c
                INNER
                JOIN (
                SELECT
                    customer_id,
                    ROUND(SUM(total_amount), 2) AS total_spent,
                    COUNT(*) AS num_orders
                FROM orders
                GROUP BY customer_id ) co ON c.customer_id = co.customer_id
                ORDER BY co.total_spent DESC
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Business Reports
    """)
    return


@app.cell
def _(o, con):
    con.execute(
        f"""
        SELECT EXTRACT(YEAR
                FROM o.order_date) AS yr, EXTRACT(MONTH
                FROM o.order_date) AS mo, COUNT(DISTINCT o.order_id) AS num_orders, COUNT(DISTINCT o.customer_id) AS unique_customers, ROUND(SUM(o.total_amount), 2) AS revenue, ROUND(AVG(o.total_amount), 2) AS avg_order_value
                FROM orders o
                WHERE o.status != 'cancelled'
                GROUP BY yr, mo
                ORDER BY yr, mo
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    segment,
                    COUNT(*) AS num_customers,
                    ROUND(AVG(total_spent), 2) AS avg_spent
                FROM (
                SELECT
                    c.customer_id,
                    SUM(o.total_amount) AS total_spent,
                    CASE WHEN SUM(o.total_amount) >= 1000 THEN 'VIP' WHEN SUM(o.total_amount) >= 500 THEN 'Regular' WHEN SUM(o.total_amount) >= 100 THEN 'Occasional' ELSE 'New' END AS segment
                FROM customers c
                INNER
                JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id ) segmented
                GROUP BY segment
                ORDER BY avg_spent DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    Covered this week:
    - **INNER JOIN**: Only matching rows
    - **LEFT JOIN**: All from left table + matches from right
    - **RIGHT JOIN / FULL OUTER JOIN**: Less common but important
    - **Self JOIN**: Comparing rows within the same table
    - **Multi-table JOINs**: Chaining 3+ tables
    - **JOINs + GROUP BY/HAVING**: Aggregating across tables
    - **Derived tables**: Subqueries in the FROM clause

    **Next week**: Window functions, CTEs, set operations, and views!
    """)
    return


if __name__ == "__main__":
    app.run()
