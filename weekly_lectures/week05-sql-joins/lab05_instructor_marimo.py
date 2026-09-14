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
    # Lab 5: Window Functions, CTEs, Set Operations, Views — INSTRUCTOR SOLUTIONS

    ## OMIS 105 — Database Management Systems
    **Week 5 | Answer Key**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Connect to DuckDB and load `categories`, `products`, `customers`,
    `orders`, `order_items`, `reviews`, `suppliers`, and
    `product_suppliers` from `./data/`.
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
    con.execute(
        "CREATE OR REPLACE TABLE reviews AS SELECT * FROM read_csv_auto('./data/reviews.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE suppliers AS SELECT * FROM read_csv_auto('./data/suppliers.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE product_suppliers AS SELECT * FROM read_csv_auto('./data/product_suppliers.csv')"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Window Functions (25 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** (5 pts) Rank all products by price within each category. Show
    the top 2 per category.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT * FROM (
            SELECT product_name, category_id, price,
                   RANK() OVER (PARTITION BY category_id ORDER BY price DESC) AS rank_in_cat
            FROM products
        ) ranked
        WHERE rank_in_cat <= 2
        ORDER BY category_id, rank_in_cat
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** (5 pts) Running cumulative total over time, plus each order's
    percentage of the grand total.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT order_id, order_date, total_amount,
               ROUND(SUM(total_amount) OVER (ORDER BY order_date), 2) AS cumulative_total,
               ROUND(total_amount / SUM(total_amount) OVER () * 100, 2) AS pct_of_total
        FROM orders
        WHERE status != 'cancelled'
        ORDER BY order_date
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** (5 pts) LAG: each order alongside the previous order's
    total_amount for the same customer, and the difference.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT customer_id, order_id, order_date, total_amount,
               LAG(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_amount,
               ROUND(total_amount - LAG(total_amount) OVER (
                   PARTITION BY customer_id ORDER BY order_date
               ), 2) AS diff
        FROM orders
        ORDER BY customer_id, order_date
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** (5 pts) NTILE(5): divide customers into 5 spending tiers.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        WITH cust_spend AS (
            SELECT c.customer_id, c.first_name, c.last_name,
                   ROUND(SUM(o.total_amount), 2) AS total_spent
            FROM customers c
            INNER JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name
        )
        SELECT first_name, last_name, total_spent,
               NTILE(5) OVER (ORDER BY total_spent) AS spending_tier
        FROM cust_spend
        ORDER BY total_spent DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** (5 pts) Each product's price vs. its category: average, min,
    max, and PERCENT_RANK.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT product_name, category_id, price,
               ROUND(AVG(price) OVER (PARTITION BY category_id), 2) AS cat_avg,
               MIN(price) OVER (PARTITION BY category_id) AS cat_min,
               MAX(price) OVER (PARTITION BY category_id) AS cat_max,
               ROUND(PERCENT_RANK() OVER (PARTITION BY category_id ORDER BY price) * 100, 1)
                   AS percentile
        FROM products
        ORDER BY category_id, price
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: CTEs (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6.** (5 pts) Top 5 customers by total spending, with their most
    recent order date and order count.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        WITH top_spenders AS (
            SELECT customer_id,
                   COUNT(*) AS num_orders,
                   ROUND(SUM(total_amount), 2) AS total_spent,
                   MAX(order_date) AS last_order
            FROM orders
            GROUP BY customer_id
            ORDER BY total_spent DESC
            LIMIT 5
        )
        SELECT c.first_name, c.last_name,
               ts.num_orders, ts.total_spent, ts.last_order
        FROM customers c
        INNER JOIN top_spenders ts ON c.customer_id = ts.customer_id
        ORDER BY ts.total_spent DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** (5 pts) Multi-CTE report: each category's revenue, the
    overall total, and each category's percentage of total.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        WITH cat_revenue AS (
            SELECT cat.category_name,
                   ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            JOIN categories cat ON p.category_id = cat.category_id
            GROUP BY cat.category_name
        ),
        total AS (
            SELECT SUM(revenue) AS grand_total FROM cat_revenue
        )
        SELECT cr.category_name, cr.revenue,
               ROUND(cr.revenue / t.grand_total * 100, 1) AS pct_of_total
        FROM cat_revenue cr, total t
        ORDER BY cr.revenue DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8.** (5 pts) "Customer Lifetime Value" report: first/last order
    date, number of orders, total spent, average order value.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        WITH clv AS (
            SELECT customer_id,
                   MIN(order_date) AS first_order,
                   MAX(order_date) AS last_order,
                   COUNT(*) AS num_orders,
                   ROUND(SUM(total_amount), 2) AS total_spent,
                   ROUND(AVG(total_amount), 2) AS avg_order_value
            FROM orders
            WHERE status != 'cancelled'
            GROUP BY customer_id
        )
        SELECT c.first_name, c.last_name,
               l.first_order, l.last_order, l.num_orders,
               l.total_spent, l.avg_order_value
        FROM customers c
        INNER JOIN clv l ON c.customer_id = l.customer_id
        ORDER BY l.total_spent DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Set Operations (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9.** (5 pts) EXCEPT: customers who placed orders but never wrote a
    review.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT DISTINCT customer_id FROM orders
        EXCEPT
        SELECT DISTINCT customer_id FROM reviews
        ORDER BY customer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** (5 pts) INTERSECT: products that appear in both order_items
    and reviews.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT DISTINCT product_id FROM order_items
        INTERSECT
        SELECT DISTINCT product_id FROM reviews
        ORDER BY product_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: Views (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q11.** (8 pts) `product_performance` view: name, category, price,
    total units sold, total revenue, average review rating, number of
    reviews. Uses LEFT JOINs so all products are included.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE OR REPLACE VIEW product_performance AS
        SELECT p.product_name,
               cat.category_name,
               p.price,
               COALESCE(SUM(oi.quantity), 0) AS total_units_sold,
               COALESCE(ROUND(SUM(oi.quantity * oi.unit_price), 2), 0) AS total_revenue,
               ROUND(AVG(r.rating), 1) AS avg_rating,
               COUNT(DISTINCT r.review_id) AS num_reviews
        FROM products p
        INNER JOIN categories cat ON p.category_id = cat.category_id
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        LEFT JOIN reviews r ON p.product_id = r.product_id
        GROUP BY p.product_id, p.product_name, cat.category_name, p.price
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        "SELECT * FROM product_performance ORDER BY total_revenue DESC LIMIT 10"
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** (7 pts) `monthly_dashboard` view: year, month, order count,
    unique customers, revenue, average order value, month-over-month
    change.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE OR REPLACE VIEW monthly_dashboard AS
        WITH monthly AS (
            SELECT EXTRACT(YEAR FROM order_date) AS yr,
                   EXTRACT(MONTH FROM order_date) AS mo,
                   COUNT(*) AS order_count,
                   COUNT(DISTINCT customer_id) AS unique_customers,
                   ROUND(SUM(total_amount), 2) AS revenue,
                   ROUND(AVG(total_amount), 2) AS avg_order_value
            FROM orders
            WHERE status != 'cancelled'
            GROUP BY yr, mo
        )
        SELECT yr, mo, order_count, unique_customers, revenue, avg_order_value,
               ROUND(revenue - LAG(revenue) OVER (ORDER BY yr, mo), 2) AS mom_change
        FROM monthly
        """
    )
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM monthly_dashboard ORDER BY yr, mo").fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Comprehensive Analysis (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q13.** (10 pts) RFM Analysis: recency, frequency, monetary, each
    scored 1–4 with NTILE, plus a "Champion" / "At Risk" / "Average"
    segment.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        WITH rfm AS (
            SELECT customer_id,
                   DATEDIFF('day', MAX(order_date), CURRENT_DATE) AS recency,
                   COUNT(*) AS frequency,
                   ROUND(SUM(total_amount), 2) AS monetary
            FROM orders
            WHERE status != 'cancelled'
            GROUP BY customer_id
        ),
        scored AS (
            SELECT customer_id, recency, frequency, monetary,
                   NTILE(4) OVER (ORDER BY recency DESC) AS r_score,
                   NTILE(4) OVER (ORDER BY frequency) AS f_score,
                   NTILE(4) OVER (ORDER BY monetary) AS m_score
            FROM rfm
        )
        SELECT c.first_name, c.last_name,
               s.recency, s.frequency, s.monetary,
               s.r_score, s.f_score, s.m_score,
               CASE
                   WHEN s.r_score >= 3 AND s.f_score >= 3 AND s.m_score >= 3 THEN 'Champion'
                   WHEN s.r_score = 1 THEN 'At Risk'
                   ELSE 'Average'
               END AS segment
        FROM scored s
        INNER JOIN customers c ON s.customer_id = c.customer_id
        ORDER BY s.monetary DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Grading Rubric

    | Part | Points |
    |------|--------|
    | Part 1: Window Functions | 25 |
    | Part 2: CTEs | 15 |
    | Part 3: Set Operations | 10 |
    | Part 4: Views | 15 |
    | Part 5: Comprehensive | 10 |
    | **Total** | **75** |
    """)
    return


if __name__ == "__main__":
    app.run()
