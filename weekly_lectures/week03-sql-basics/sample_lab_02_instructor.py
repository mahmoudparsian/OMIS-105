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
    # Lab 3: SQL Functions, GROUP BY, and Subqueries — INSTRUCTOR SOLUTIONS

    ## OMIS 105 — Database Management Systems
    **Week 3 | Answer Key**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Connect to DuckDB and load `products`, `customers`, `categories`, and
    `orders` from `./data/`.

    > **Note**: the `.md` answer key groups several queries by a `category`
    column on `products`, but `data/products.csv` only has `category_id`
    (the normalized schema from Week 2) — there is no `category` text
    column to group by. Q8, Q9, Q12, Q14, and Q15 below join `products` to
    `categories` (the same comma-join style Week 2 Q6 already used) and
    group by `category_name` instead.
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
        "CREATE OR REPLACE TABLE products AS SELECT * FROM read_csv_auto('./data/products.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv_auto('./data/customers.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE categories AS SELECT * FROM read_csv_auto('./data/categories.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE orders AS SELECT * FROM read_csv_auto('./data/orders.csv')"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: String Functions (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** (3 pts) Each customer's full name in uppercase, plus email
    length. Sort by email length descending.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT UPPER(CONCAT(first_name, ' ', last_name)) AS full_name_upper,
               email,
               LENGTH(email) AS email_length
        FROM customers
        ORDER BY email_length DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** (3 pts) Products whose name contains "Set" or "Kit"
    (case-insensitive).
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT product_name, category_id
        FROM products
        WHERE product_name ILIKE '%set%'
           OR product_name ILIKE '%kit%'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** (4 pts) An `email_domain` column extracting the part after `@`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT first_name, email,
               SPLIT_PART(email, '@', 2) AS email_domain
        FROM customers
        ORDER BY email_domain
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Also accept: `SUBSTRING(email FROM POSITION('@' IN email) + 1)`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Date Functions (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** (5 pts) Orders placed in each month of 2024. Sort by month.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT EXTRACT(YEAR FROM order_date) AS yr,
               EXTRACT(MONTH FROM order_date) AS mo,
               COUNT(*) AS order_count
        FROM orders
        WHERE EXTRACT(YEAR FROM order_date) = 2024
        GROUP BY yr, mo
        ORDER BY mo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** (5 pts) Days each customer has been a member (join_date to
    today). Sort by most senior first.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT first_name, join_date,
               DATEDIFF('day', join_date, CURRENT_DATE) AS days_as_member
        FROM customers
        ORDER BY days_as_member DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Also accept: `CURRENT_DATE - join_date`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: CASE Expressions (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6.** (5 pts) Classify each product into a price tier (Economy /
    Standard / Premium / Luxury), then count products per tier.
    """)
    return


@app.cell
def _(con):
    # Individual products
    con.execute(
        """
        SELECT product_name, price,
            CASE
                WHEN price < 15 THEN 'Economy'
                WHEN price < 50 THEN 'Standard'
                WHEN price < 150 THEN 'Premium'
                ELSE 'Luxury'
            END AS price_tier
        FROM products
        ORDER BY price
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    # Count per tier
    con.execute(
        """
        SELECT
            CASE
                WHEN price < 15 THEN 'Economy'
                WHEN price < 50 THEN 'Standard'
                WHEN price < 150 THEN 'Premium'
                ELSE 'Luxury'
            END AS price_tier,
            COUNT(*) AS cnt
        FROM products
        GROUP BY price_tier
        ORDER BY cnt DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** (5 pts) An `order_size` classification based on `total_amount`
    (Small / Medium / Large / Extra Large), with count, total revenue, and
    average value per size.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT
            CASE
                WHEN total_amount < 50 THEN 'Small'
                WHEN total_amount < 200 THEN 'Medium'
                WHEN total_amount < 500 THEN 'Large'
                ELSE 'Extra Large'
            END AS order_size,
            COUNT(*) AS cnt,
            ROUND(SUM(total_amount), 2) AS total_revenue,
            ROUND(AVG(total_amount), 2) AS avg_value
        FROM orders
        GROUP BY order_size
        ORDER BY avg_value
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: GROUP BY and HAVING (20 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8.** (5 pts) Per category: number of products, average price, total
    stock value. Sort by total stock value descending.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT c.category_name AS category,
               COUNT(*) AS num_products,
               ROUND(AVG(p.price), 2) AS avg_price,
               ROUND(SUM(p.price * p.stock_quantity), 2) AS total_stock_value
        FROM products p, categories c
        WHERE p.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY total_stock_value DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9.** (5 pts) Categories with more than 5 products with stock above 100.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT c.category_name AS category, COUNT(*) AS cnt
        FROM products p, categories c
        WHERE p.category_id = c.category_id
          AND p.stock_quantity > 100
        GROUP BY c.category_name
        HAVING COUNT(*) > 5
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** (5 pts) Number of orders per customer; only customers with 3
    or more orders.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT customer_id, COUNT(*) AS order_count
        FROM orders
        GROUP BY customer_id
        HAVING COUNT(*) >= 3
        ORDER BY order_count DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q11.** (5 pts) Average order value per month in 2024; only months
    above $200.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT EXTRACT(MONTH FROM order_date) AS mo,
               ROUND(AVG(total_amount), 2) AS avg_order_value
        FROM orders
        WHERE EXTRACT(YEAR FROM order_date) = 2024
        GROUP BY mo
        HAVING AVG(total_amount) > 200
        ORDER BY mo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Subqueries (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** (5 pts) Products priced higher than the average price in
    their own category (correlated subquery).
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT p.product_name, c.category_name AS category, p.price
        FROM products p, categories c
        WHERE p.category_id = c.category_id
          AND p.price > (
              SELECT AVG(p2.price)
              FROM products p2
              WHERE p2.category_id = p.category_id
          )
        ORDER BY c.category_name, p.price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q13.** (5 pts) The top-spending customer (highest total across all
    orders).
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT c.first_name, c.last_name,
               ROUND(SUM(o.total_amount), 2) AS total_spent
        FROM customers c, orders o
        WHERE c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY total_spent DESC
        LIMIT 1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q14.** (5 pts) Categories where every product has stock_quantity > 0
    (no out-of-stock products).
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT c.category_name AS category
        FROM products p, categories c
        WHERE p.category_id = c.category_id
        GROUP BY c.category_name
        HAVING MIN(p.stock_quantity) > 0
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > This works because if MIN(stock) > 0, no product in that category has 0 stock.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 6: Comprehensive Query (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q15.** (10 pts) "Product Dashboard": per category — number of
    products, average/min/max price, in-stock vs out-of-stock counts, and
    whether the category average is above or below the overall average.
    Sort by average price descending.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT c.category_name AS category,
               COUNT(*) AS num_products,
               ROUND(AVG(p.price), 2) AS avg_price,
               MIN(p.price) AS cheapest,
               MAX(p.price) AS most_expensive,
               COUNT(CASE WHEN p.stock_quantity > 0 THEN 1 END) AS in_stock,
               COUNT(CASE WHEN p.stock_quantity = 0 THEN 1 END) AS out_of_stock,
               CASE
                   WHEN AVG(p.price) > (SELECT AVG(price) FROM products) THEN 'Above'
                   ELSE 'Below'
               END AS vs_overall_avg
        FROM products p, categories c
        WHERE p.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY avg_price DESC
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
    | Part 1: String Functions | 10 |
    | Part 2: Date Functions | 10 |
    | Part 3: CASE Expressions | 10 |
    | Part 4: GROUP BY/HAVING | 20 |
    | Part 5: Subqueries | 15 |
    | Part 6: Comprehensive | 10 |
    | **Total** | **75** |
    """)
    return


if __name__ == "__main__":
    app.run()
