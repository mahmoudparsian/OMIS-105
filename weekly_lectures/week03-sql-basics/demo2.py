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
    # Week 3: SQL Mastery Part 1 — Functions, GROUP BY, Subqueries
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
        CREATE OR REPLACE TABLE categories AS
            SELECT * FROM read_csv_auto('./data/categories.csv')
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. String Functions
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    UPPER('hello world') AS upper_case,
                    LOWER('HELLO') AS lower_case,
                    LENGTH('DuckDB') AS len,
                    TRIM('  hi  ') AS trimmed,
                    CONCAT('Hello', ' ', 'World') AS combined,
                    REPLACE('DuckDB', 'Duck', 'Goose') AS replaced
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT CONCAT(first_name, ' ', last_name) AS full_name,
                       LOWER(email) AS email_lower,
                       LENGTH(first_name) AS name_len
                FROM customers
                ORDER BY name_len DESC
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        DESC products
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category_id
                FROM products
                WHERE product_name ILIKE '%pro%'
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT DISTINCT category_id
                FROM products
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Mathematical Functions
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, 
                       price,
                       ROUND(price * 0.85, 2) AS price_15pct_off,
                       CEIL(price) AS price_rounded_up,
                       FLOOR(price) AS price_rounded_down
                FROM products
                WHERE category_id = 3
                ORDER BY price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Date Functions
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT CURRENT_DATE AS today,
                       EXTRACT(YEAR FROM DATE '2024-06-15') AS yr,
                       EXTRACT(MONTH FROM DATE '2024-06-15') AS mo,
                       EXTRACT(DOW FROM DATE '2024-06-15') AS day_of_week,
                       DATE '2024-06-15' + INTERVAL 30 DAY AS plus_30_days
        """
    ).fetchdf()
    return


@app.cell
def _(order_date, con):
    con.execute(
        f"""
        SELECT EXTRACT(YEAR FROM order_date) AS yr,
                       EXTRACT(MONTH FROM order_date) AS mo,
                       COUNT(*) AS order_count,
                       ROUND(SUM(total_amount), 2) AS revenue
                FROM orders
                GROUP BY yr, mo
                ORDER BY yr, mo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. CASE Expressions
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, price,
                    CASE
                        WHEN price < 20 THEN 'Budget'
                        WHEN price < 100 THEN 'Mid-Range'
                        WHEN price < 300 THEN 'Premium'
                        ELSE 'Luxury'
                    END AS price_tier
                FROM products
                ORDER BY price
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    CASE
                        WHEN price < 20 THEN 'Budget'
                        WHEN price < 100 THEN 'Mid-Range'
                        ELSE 'Premium'
                    END AS price_tier,
                    COUNT(*) AS cnt,
                    ROUND(AVG(price), 2) AS avg_price
                FROM products
                GROUP BY price_tier
                ORDER BY avg_price
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. GROUP BY Fundamentals
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT category_id, COUNT(*) AS num_products
                FROM products
                GROUP BY category_id
                ORDER BY num_products DESC
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT category_id,
                       COUNT(*) AS cnt,
                       ROUND(AVG(price), 2) AS avg_price,
                       MIN(price) AS min_price,
                       MAX(price) AS max_price,
                       SUM(stock_quantity) AS total_stock
                FROM products
                GROUP BY category_id
                ORDER BY avg_price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. HAVING — Filtering Groups
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT category_id,
                       ROUND(AVG(price), 2) AS avg_price,
                       COUNT(*) AS cnt
                FROM products
                GROUP BY category_id
                HAVING AVG(price) > 50
                ORDER BY avg_price DESC
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT category_id,
                       ROUND(AVG(price), 2) AS avg_price
                FROM products
                WHERE stock_quantity > 0          -- filter rows first
                GROUP BY category_id
                HAVING AVG(price) > 30            -- then filter groups
                ORDER BY avg_price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Conditional Aggregation
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT category_id,
                    COUNT(*) AS total,
                    COUNT(CASE WHEN stock_quantity > 0 THEN 1 END) AS in_stock,
                    COUNT(CASE WHEN stock_quantity = 0 THEN 1 END) AS out_of_stock
                FROM products
                GROUP BY category_id
                ORDER BY total DESC
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT status,
                       COUNT(*) AS cnt,
                       ROUND(SUM(total_amount), 2) AS total_revenue,
                       ROUND(AVG(total_amount), 2) AS avg_order_value
                FROM orders
                GROUP BY status
                ORDER BY total_revenue DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Subqueries
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category_id, price
                FROM products
                WHERE price > (SELECT AVG(price) FROM products)
                ORDER BY price DESC
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT first_name, last_name, email
                FROM customers
                WHERE customer_id IN (
                    SELECT DISTINCT customer_id FROM orders
                )
                ORDER BY last_name
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT first_name, last_name, email
                FROM customers
                WHERE customer_id NOT IN (
                    SELECT DISTINCT customer_id FROM orders
                )
                ORDER BY last_name
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, price,
                       ROUND(price - (SELECT AVG(price) FROM products), 2) AS diff_from_avg,
                       ROUND(price / (SELECT MAX(price) FROM products) * 100, 1) AS pct_of_max
                FROM products
                ORDER BY price DESC
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Putting It All Together
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT category_id,
                       COUNT(*) AS num_products,
                       ROUND(AVG(price), 2) AS cat_avg,
                       ROUND((SELECT AVG(price) FROM products), 2) AS overall_avg,
                       CASE
                           WHEN AVG(price) > (SELECT AVG(price) FROM products)
                           THEN 'Above Average'
                           ELSE 'Below Average'
                       END AS comparison
                FROM products
                GROUP BY category_id
                ORDER BY cat_avg DESC
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT status,
                       COUNT(*) AS cnt,
                       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 1) AS pct
                FROM orders
                GROUP BY status
                ORDER BY pct DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    Covered this week:
    - **String functions**: UPPER, LOWER, CONCAT, LENGTH, LIKE/ILIKE
    - **Math functions**: ROUND, CEIL, FLOOR, ABS, POWER
    - **Date functions**: EXTRACT, DATEDIFF, CURRENT_DATE
    - **CASE expressions**: Conditional logic in SQL
    - **GROUP BY + HAVING**: Aggregate by groups, filter groups
    - **Subqueries**: Nested queries for comparisons

    **Next week**: JOINs — combining multiple tables!
    """)
    return


if __name__ == "__main__":
    app.run()
