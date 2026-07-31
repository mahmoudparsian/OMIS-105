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
    # Week 10: Synthesis & Review — Demo Notebook
    ## OMIS 105: Database Management Systems

    This notebook is a comprehensive review of all SQL concepts covered in this course, using the full ShopSmart e-commerce dataset.
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect()
    for t, f in [('categories','./data/categories.csv'),
                 ('products','./data/products.csv'),
                 ('customers','./data/customers.csv'),
                 ('orders','./data/orders.csv'),
                 ('order_items','./data/order_items.csv'),
                 ('reviews','./data/reviews.csv'),
                 ('suppliers','./data/suppliers.csv'),
                 ('product_suppliers','./data/product_suppliers.csv'),
                 ('shipping','./data/shipping.csv')]:
        con.sql(f"CREATE OR REPLACE TABLE {t} AS SELECT * FROM read_csv_auto('{f}')")
        print(f"Loaded {t}: {con.sql(f'SELECT COUNT(*) FROM {t}').fetchone()[0]} rows")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Review: Basic Queries (Week 1 & 3)
    """)
    return


@app.cell
def _(con):
    # Filtering, sorting, limiting
    con.sql("""
        SELECT
            product_name,
            category_id,
            price,
            stock_quantity
        FROM products
        WHERE price BETWEEN 20
        AND 100
        AND stock_quantity > 0
        ORDER BY price DESC
        LIMIT 10;
    """).show()
    return


@app.cell
def _(con):
    # String functions + CASE
    con.sql("""
        SELECT
            product_name,
            UPPER(SUBSTRING(product_name, 1, 1)) AS initial,
            price,
            CASE WHEN price < 25 THEN 'Budget' WHEN price < 100 THEN 'Mid-Range' ELSE 'Premium' END AS tier
        FROM products
        ORDER BY price;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Review: GROUP BY and Aggregation (Week 3)
    """)
    return


@app.cell
def _(con):
    # Category statistics with conditional aggregation
    con.sql("""
        SELECT
            cat.category_name,
            COUNT(*) AS num_products,
            ROUND(AVG(p.price), 2) AS avg_price,
            MIN(p.price) AS min_price,
            MAX(p.price) AS max_price,
            SUM(CASE WHEN p.stock_quantity = 0 THEN 1 ELSE 0 END) AS out_of_stock
        FROM products p
        JOIN categories cat ON p.category_id = cat.category_id
        GROUP BY cat.category_name
        HAVING COUNT(*) >= 5
        ORDER BY avg_price DESC;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Review: JOINs (Week 4)
    """)
    return


@app.cell
def _(con):
    # Multi-table JOIN: Full order details
    con.sql("""
        SELECT
            c.first_name || ' ' || c.last_name AS customer,
            o.order_id,
            o.order_date,
            o.status,
            p.product_name,
            cat.category_name,
            oi.quantity,
            oi.unit_price,
            ROUND(oi.quantity * oi.unit_price, 2) AS line_total
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        JOIN categories cat ON p.category_id = cat.category_id
        WHERE o.status = 'completed'
        ORDER BY o.order_date DESC
        LIMIT 15;
    """).show()
    return


@app.cell
def _(con):
    # LEFT JOIN: Products never ordered
    con.sql("""
        SELECT
            p.product_name,
            cat.category_name,
            p.price
        FROM products p
        JOIN categories cat ON p.category_id = cat.category_id
        LEFT
        JOIN order_items oi ON p.product_id = oi.product_id
        WHERE oi.item_id IS NULL
        ORDER BY p.price DESC;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Review: Window Functions and CTEs (Week 5)
    """)
    return


@app.cell
def _(con):
    # Top 2 products per category by revenue
    con.sql("""
        WITH product_revenue AS (
        SELECT
            p.product_id,
            p.product_name,
            p.category_id,
            COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS revenue,
            ROW_NUMBER() OVER ( PARTITION BY p.category_id
        ORDER BY SUM(oi.quantity * oi.unit_price) DESC ) AS rank_in_cat
        FROM products p
        LEFT
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, p.category_id )
        SELECT
            cat.category_name,
            pr.product_name,
            ROUND(pr.revenue, 2) AS revenue,
            pr.rank_in_cat
        FROM product_revenue pr
        JOIN categories cat ON pr.category_id = cat.category_id
        WHERE pr.rank_in_cat <= 2
        ORDER BY cat.category_name, pr.rank_in_cat;
    """).show()
    return


@app.cell
def _(con):
    # Monthly revenue trend with LAG
    con.sql("""
        WITH monthly AS (
        SELECT
            DATE_TRUNC('month', order_date) AS month,
            ROUND(SUM(total_amount), 2) AS revenue,
            COUNT(*) AS orders
        FROM orders
        WHERE status != 'cancelled'
        GROUP BY month )
        SELECT
            month,
            revenue,
            orders,
            LAG(revenue) OVER (
        ORDER BY month) AS prev_month, ROUND(revenue - COALESCE(LAG(revenue) OVER (
        ORDER BY month), revenue), 2) AS change
        FROM monthly
        ORDER BY month;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Review: Views (Week 5)
    """)
    return


@app.cell
def _(con):
    # Create a comprehensive customer view
    con.sql("""
        CREATE
        OR REPLACE VIEW customer_360 AS
        WITH order_stats AS (
        SELECT
            customer_id,
            COUNT(*) AS num_orders,
            ROUND(SUM(total_amount), 2) AS total_spent,
            ROUND(AVG(total_amount), 2) AS avg_order,
            MIN(order_date) AS first_order,
            MAX(order_date) AS last_order
        FROM orders
        WHERE status != 'cancelled'
        GROUP BY customer_id ), review_stats AS (
        SELECT
            customer_id,
            COUNT(*) AS num_reviews,
            ROUND(AVG(rating), 1) AS avg_rating
        FROM reviews
        GROUP BY customer_id )
        SELECT
            c.first_name || ' ' || c.last_name AS name,
            c.email,
            c.city,
            c.state,
            COALESCE(os.num_orders, 0) AS orders,
            COALESCE(os.total_spent, 0) AS spent,
            COALESCE(os.avg_order, 0) AS avg_order,
            os.first_order,
            os.last_order,
            COALESCE(rs.num_reviews, 0) AS reviews,
            rs.avg_rating,
            CASE WHEN os.total_spent >= 1000 THEN 'VIP' WHEN os.total_spent >= 500 THEN 'Regular' WHEN os.total_spent > 0 THEN 'Occasional' ELSE 'Inactive' END AS segment
        FROM customers c
        LEFT
        JOIN order_stats os ON c.customer_id = os.customer_id
        LEFT
        JOIN review_stats rs ON c.customer_id = rs.customer_id;
    """)

    con.sql("""
        SELECT *
        FROM customer_360
        ORDER BY spent DESC
        LIMIT 10;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Review: Normalization Check (Week 6)
    """)
    return


@app.cell
def _(con):
    # Verify our schema is normalized — check for redundancy
    # If joining back to denormalized form shows repetition, normalization is working
    con.sql("""
        SELECT
            'categories' AS tbl,
            COUNT(*) AS rows,
            COUNT(DISTINCT category_id) AS unique_keys
        FROM categories
        UNION ALL
        SELECT
            'products',
            COUNT(*),
            COUNT(DISTINCT product_id)
        FROM products
        UNION ALL
        SELECT
            'customers',
            COUNT(*),
            COUNT(DISTINCT customer_id)
        FROM customers
        UNION ALL
        SELECT
            'orders',
            COUNT(*),
            COUNT(DISTINCT order_id)
        FROM orders
        UNION ALL
        SELECT
            'order_items',
            COUNT(*),
            COUNT(DISTINCT item_id)
        FROM order_items;
    """).show()
    print("rows = unique_keys for each table -> no duplicate PKs -> entity integrity holds!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Review: Performance (Week 7)
    """)
    return


@app.cell
def _(con):
    # EXPLAIN a complex query
    con.sql("""
        EXPLAIN
        SELECT
            cat.category_name,
            SUM(oi.quantity * oi.unit_price) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        JOIN categories cat ON p.category_id = cat.category_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status = 'completed'
        GROUP BY cat.category_name
        ORDER BY revenue DESC;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Review: Transactions (Week 8)
    """)
    return


@app.cell
def _(con):
    # Complete transaction example: process a new order
    def process_order(con, cust_id, items):
        try:
            con.execute("BEGIN")
            oid = con.sql("""
                SELECT COALESCE(MAX(order_id),0)+1
                FROM orders;
            """).fetchone()[0]
            con.execute(f"INSERT INTO orders VALUES ({oid},{cust_id},CURRENT_DATE,'processing',0)")
            
            total = 0
            iid = con.sql("""
                SELECT COALESCE(MAX(item_id),0)
                FROM order_items;
            """).fetchone()[0]
            for pid, qty in items:
                iid += 1
                row = con.sql(f"SELECT price, stock_quantity FROM products WHERE product_id={pid}").fetchone()
                if not row: raise Exception(f"Product {pid} not found")
                if row[1] < qty: raise Exception(f"Product {pid}: need {qty}, have {row[1]}")
                total += round(row[0] * qty, 2)
                con.execute(f"INSERT INTO order_items VALUES ({iid},{oid},{pid},{qty},{row[0]})")
                con.execute(f"UPDATE products SET stock_quantity=stock_quantity-{qty} WHERE product_id={pid}")
            
            con.execute(f"UPDATE orders SET total_amount={total} WHERE order_id={oid}")
            con.execute("COMMIT")
            print(f"Order {oid}: ${total:.2f} — COMMITTED")
        except Exception as e:
            con.execute("ROLLBACK")
            print(f"ROLLED BACK: {e}")

    # Success case
    process_order(con, 1, [(1, 1), (10, 2)])

    # Failure case
    process_order(con, 2, [(999, 1)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Comprehensive Final Query

    Combining every technique from the course into one analytical query.
    """)
    return


@app.cell
def _(con):
    # The Ultimate ShopSmart Analytics Query
    con.sql("""
        WITH /* CTE 1: Customer spending */ customer_spend AS (
        SELECT
            customer_id,
            SUM(total_amount) AS total_spent,
            COUNT(*) AS num_orders
        FROM orders
        WHERE status != 'cancelled'
        GROUP BY customer_id ), /* CTE 2: Category revenue */ category_rev AS (
        SELECT
            p.category_id,
            SUM(oi.quantity * oi.unit_price) AS revenue,
            SUM(oi.quantity) AS units_sold
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.category_id ), /* CTE 3: Combine */ dashboard AS (
        SELECT
            cat.category_name,
            cr.revenue,
            cr.units_sold,
            COUNT(DISTINCT p.product_id) AS num_products,
            ROUND(AVG(COALESCE(r.rating, 0)), 1) AS avg_rating,
            /* Window: percent of total revenue */ ROUND(cr.revenue / SUM(cr.revenue) OVER () * 100, 1) AS pct_of_revenue,
            /* Window: rank by revenue */ RANK() OVER (
        ORDER BY cr.revenue DESC) AS revenue_rank
        FROM categories cat
        JOIN category_rev cr ON cat.category_id = cr.category_id
        JOIN products p ON cat.category_id = p.category_id
        LEFT
        JOIN reviews r ON p.product_id = r.product_id
        GROUP BY cat.category_name, cat.category_id, cr.revenue, cr.units_sold )
        SELECT
            category_name,
            ROUND(revenue, 2) AS revenue,
            units_sold,
            num_products,
            avg_rating,
            pct_of_revenue || '%' AS market_share,
            revenue_rank,
            CASE WHEN revenue_rank <= 3 THEN 'Top Tier' WHEN revenue_rank <= 6 THEN 'Mid Tier' ELSE 'Emerging' END AS tier
        FROM dashboard
        ORDER BY revenue_rank;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Course Complete!

    Congratulations on completing OMIS 105! You now have practical skills in:

    1. **Database Design** — ER diagrams, schema creation, constraints
    2. **Relational Theory** — keys, relationships, normalization
    3. **SQL Mastery** — SELECT, JOINs, GROUP BY, window functions, CTEs, views
    4. **Performance** — indexes, EXPLAIN, query optimization
    5. **Transactions** — ACID properties, concurrency, error handling
    6. **Modern Trends** — NoSQL, cloud databases, data lakes

    These are career-ready skills used in every industry that works with data. Keep practicing!
    """)
    return


if __name__ == "__main__":
    app.run()
