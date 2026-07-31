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
    # Week 5: SQL Mastery Part 3 — Window Functions, CTEs, Views
    ## OMIS 105: Database Management Systems
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect(database=":memory:")
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE categories AS
            SELECT * FROM read_csv_auto('./data/categories.csv')
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE products AS
            SELECT * FROM read_csv_auto('./data/products.csv')
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE customers AS
            SELECT * FROM read_csv_auto('./data/customers.csv')
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE orders AS
            SELECT * FROM read_csv_auto('./data/orders.csv')
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE order_items AS
            SELECT * FROM read_csv_auto('./data/order_items.csv')
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE reviews AS
            SELECT * FROM read_csv_auto('./data/reviews.csv')
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE suppliers AS
            SELECT * FROM read_csv_auto('./data/suppliers.csv')
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE product_suppliers AS
            SELECT * FROM read_csv_auto('./data/product_suppliers.csv')
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Window Functions — Basics

    Window functions compute values across rows **without collapsing** them.
    """)
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        SELECT
                    product_name,
                    category_id,
                    price,
                    ROUND(AVG(price) OVER (PARTITION BY category_id), 2) AS cat_avg,
                    ROUND(price - AVG(price) OVER (PARTITION BY category_id), 2) AS diff_from_avg
                FROM products
                ORDER BY category_id, price DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. ROW_NUMBER, RANK, DENSE_RANK
    """)
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        SELECT
                    product_name,
                    price,
                    ROW_NUMBER() OVER (
                ORDER BY price DESC) AS row_num, RANK() OVER (
                ORDER BY price DESC) AS RANK, DENSE_RANK() OVER (
                ORDER BY price DESC) AS DENSE_RANK
                FROM products
                LIMIT 15
        """
    )
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        SELECT *
                FROM (
                SELECT
                    product_name,
                    category_id,
                    price,
                    ROW_NUMBER() OVER ( PARTITION BY category_id
                ORDER BY price DESC ) AS rn
                FROM products ) ranked
                WHERE rn <= 3
                ORDER BY category_id, rn
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. LAG and LEAD
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT
                    order_id,
                    order_date,
                    total_amount,
                    LAG(total_amount) OVER (
                ORDER BY order_date) AS prev_amount, LEAD(total_amount) OVER (
                ORDER BY order_date) AS next_amount, ROUND(total_amount - LAG(total_amount) OVER (
                ORDER BY order_date), 2) AS change_from_prev
                FROM orders
                ORDER BY order_date
                LIMIT 15
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. NTILE — Percentile Buckets
    """)
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        SELECT
                    product_name,
                    price,
                    NTILE(4) OVER (
                ORDER BY price) AS price_quartile
                FROM products
                ORDER BY price
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Running Totals and Moving Averages
    """)
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT
                    order_date,
                    total_amount,
                    SUM(total_amount) OVER (
                ORDER BY order_date) AS cumulative_revenue, ROUND(AVG(total_amount) OVER (
                ORDER BY order_date ROWS BETWEEN 4 PRECEDING
                AND CURRENT ROW ), 2) AS moving_avg_5
                FROM orders
                WHERE status != 'cancelled'
                ORDER BY order_date
                LIMIT 20
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Percent of Total
    """)
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        SELECT
                    product_name,
                    category_id,
                    price,
                    ROUND(price / SUM(price) OVER () * 100, 2) AS pct_of_total,
                    ROUND(price / SUM(price) OVER (PARTITION BY category_id) * 100, 2) AS pct_within_category
                FROM products
                ORDER BY category_id, price DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Common Table Expressions (CTEs)
    """)
    return


@app.cell
def _(mo, customer_totals, customers, orders):
    _df = mo.sql(
        f"""
        WITH customer_totals AS (
                SELECT
                    customer_id,
                    COUNT(*) AS num_orders,
                    ROUND(SUM(total_amount), 2) AS total_spent
                FROM orders
                WHERE status != 'cancelled'
                GROUP BY customer_id )
                SELECT
                    c.first_name,
                    c.last_name,
                    ct.num_orders,
                    ct.total_spent
                FROM customers c
                INNER
                JOIN customer_totals ct ON c.customer_id = ct.customer_id
                ORDER BY ct.total_spent DESC
                LIMIT 10
        """
    )
    return


@app.cell
def _(mo, order_stats, orders, segmented):
    _df = mo.sql(
        f"""
        WITH order_stats AS (
                SELECT
                    customer_id,
                    COUNT(*) AS num_orders,
                    SUM(total_amount) AS total_spent
                FROM orders
                GROUP BY customer_id ), segmented AS (
                SELECT
                    customer_id,
                    total_spent,
                    CASE WHEN total_spent >= 1000 THEN 'VIP' WHEN total_spent >= 500 THEN 'Regular' ELSE 'Occasional' END AS segment
                FROM order_stats )
                SELECT
                    s.segment,
                    COUNT(*) AS num_customers,
                    ROUND(AVG(s.total_spent), 2) AS avg_spent
                FROM segmented s
                GROUP BY s.segment
                ORDER BY avg_spent DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Set Operations
    """)
    return


@app.cell
def _(mo, customers):
    _df = mo.sql(
        f"""
        SELECT
                    first_name,
                    last_name,
                    'CA' AS source
                FROM customers
                WHERE state = 'CA'
                UNION
                SELECT
                    first_name,
                    last_name,
                    'NY' AS source
                FROM customers
                WHERE state = 'NY'
                ORDER BY source, last_name
        """
    )
    return


@app.cell
def _(mo, orders, reviews):
    _df = mo.sql(
        f"""
        SELECT DISTINCT customer_id
                FROM orders
                EXCEPT
                SELECT DISTINCT customer_id
                FROM reviews
                ORDER BY customer_id
        """
    )
    return


@app.cell
def _(mo, orders, reviews):
    _df = mo.sql(
        f"""
        SELECT DISTINCT customer_id
                FROM orders
                INTERSECT
                SELECT DISTINCT customer_id
                FROM reviews
                ORDER BY customer_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Views
    """)
    return


@app.cell
def _(mo, categories, products):
    _df = mo.sql(
        f"""
        CREATE VIEW product_summary AS
                SELECT
                    p.product_name,
                    cat.category_name,
                    p.price,
                    p.stock_quantity,
                    CASE WHEN p.stock_quantity = 0 THEN 'Out of Stock' WHEN p.stock_quantity < 20 THEN 'Low Stock' ELSE 'In Stock' END AS availability
                FROM products p
                INNER
                JOIN categories cat ON p.category_id = cat.category_id
        """
    )
    return


@app.cell
def _(mo, product_summary):
    _df = mo.sql(
        f"""
        SELECT *
                FROM product_summary
                WHERE availability = 'Low Stock'
        """
    )
    return


@app.cell
def _(mo, customers, order_stats, orders):
    _df = mo.sql(
        f"""
        CREATE VIEW customer_dashboard AS
                WITH order_stats AS (
                SELECT
                    customer_id,
                    COUNT(*) AS total_orders,
                    ROUND(SUM(total_amount), 2) AS total_spent,
                    MAX(order_date) AS last_order
                FROM orders
                WHERE status != 'cancelled'
                GROUP BY customer_id )
                SELECT
                    c.first_name,
                    c.last_name,
                    c.email,
                    c.state,
                    COALESCE(os.total_orders, 0) AS total_orders,
                    COALESCE(os.total_spent, 0) AS total_spent,
                    os.last_order,
                    CASE WHEN os.total_spent >= 1000 THEN 'VIP' WHEN os.total_spent >= 500 THEN 'Regular' WHEN os.total_spent IS NOT NULL THEN 'Occasional' ELSE 'Inactive' END AS segment
                FROM customers c
                LEFT
                JOIN order_stats os ON c.customer_id = os.customer_id
        """
    )
    return


@app.cell
def _(mo, customer_dashboard):
    _df = mo.sql(
        f"""
        SELECT *
                FROM customer_dashboard
                ORDER BY total_spent DESC
                LIMIT 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Analytical Dashboard: Revenue Trends
    """)
    return


@app.cell
def _(mo, monthly, orders):
    _df = mo.sql(
        f"""
        WITH monthly AS (
                SELECT
                    DATE_TRUNC('month', order_date) AS month,
                    SUM(total_amount) AS revenue,
                    COUNT(*) AS num_orders
                FROM orders
                WHERE status != 'cancelled'
                GROUP BY month )
                SELECT
                    month,
                    revenue,
                    num_orders,
                    LAG(revenue) OVER (
                ORDER BY month) AS prev_month_rev, ROUND(revenue - LAG(revenue) OVER (
                ORDER BY month), 2) AS mom_change, ROUND((revenue / LAG(revenue) OVER (
                ORDER BY month) - 1) * 100, 1) AS pct_change
                FROM monthly
                ORDER BY month
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    Week 5 covered:
    - **Window functions**: ROW_NUMBER, RANK, LAG, LEAD, NTILE, running totals
    - **CTEs**: Named temporary result sets for readable queries
    - **Set operations**: UNION, INTERSECT, EXCEPT
    - **Views**: Saved queries as virtual tables
    - **Analytical patterns**: Revenue trends, RFM, customer segmentation

    **This concludes our SQL Mastery series!** (Weeks 3–5)

    **Next week**: Database Design and Normalization
    """)
    return


if __name__ == "__main__":
    app.run()
