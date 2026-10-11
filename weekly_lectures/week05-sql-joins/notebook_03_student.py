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
    # Lab 5: Window Functions, CTEs, Set Operations, and Views

    ## OMIS 105 — Database Management Systems
    **Week 5 | Estimated time: 75–90 minutes**

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
    **Q1.** Rank all products by price within each category. Show
    product_name, category_id, price, and rank_in_category. Display only
    the top 2 per category.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q1
    con.execute(
        """
        -- Your query here
        SELECT 'Q1: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** For each order, show the order_id, total_amount, and the
    running cumulative total over time (ordered by order_date). Also show
    what percentage each order contributes to the grand total.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q2
    con.execute(
        """
        -- Your query here
        SELECT 'Q2: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** Using LAG, show each order alongside the previous order's
    total_amount for the same customer. Compute the difference between
    consecutive orders.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q3
    con.execute(
        """
        -- Your query here
        SELECT 'Q3: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** Divide all customers into 5 spending tiers using NTILE
    (based on total spending from orders). Show customer name, total
    spent, and tier.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q4
    con.execute(
        """
        -- Your query here
        SELECT 'Q4: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** For each product, show its price compared to its category:
    the category average, category min, category max, and what
    percentile the product's price falls in within its category (use
    PERCENT_RANK).
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q5
    con.execute(
        """
        -- Your query here
        SELECT 'Q5: replace this query' AS todo
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
    **Q6.** Using a CTE, find the top 5 customers by total spending, then
    show their most recent order date and number of orders.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q6
    con.execute(
        """
        -- Your query here
        SELECT 'Q6: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** Using multiple CTEs, create a report that shows:
    1. Each category's total revenue (from order_items)
    2. The overall total revenue
    3. Each category's percentage of total revenue
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q7
    con.execute(
        """
        -- Your query here
        SELECT 'Q7: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8.** Write a CTE-based query for a "Customer Lifetime Value"
    report that shows each customer's name, first order date, last order
    date, number of orders, total spent, and average order value.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q8
    con.execute(
        """
        -- Your query here
        SELECT 'Q8: replace this query' AS todo
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
    **Q9.** Using EXCEPT, find customer_ids who have placed orders but
    have never written a review.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q9
    con.execute(
        """
        -- Your query here
        SELECT 'Q9: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** Using INTERSECT, find products that appear in both
    order_items AND reviews.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q10
    con.execute(
        """
        -- Your query here
        SELECT 'Q10: replace this query' AS todo
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
    **Q11.** Create a view called `product_performance` that shows each
    product's name, category, price, total units sold, total revenue,
    average review rating, and number of reviews. Use LEFT JOINs so all
    products are included.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q11 (CREATE VIEW)
    con.execute(
        """
        -- Your CREATE VIEW here
        SELECT 'Q11: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** Create a view called `monthly_dashboard` that shows year,
    month, order count, unique customers, total revenue, average order
    value, and month-over-month revenue change (using LAG).
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q12 (CREATE VIEW)
    con.execute(
        """
        -- Your CREATE VIEW here
        SELECT 'Q12: replace this query' AS todo
        """
    ).fetchdf()
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
    **Q13.** Combine window functions, CTEs, and JOINs to create an "RFM
    Analysis" (Recency, Frequency, Monetary). For each customer show:
    name, days since last order, number of orders, total spent, plus an
    R/F/M score (each 1–4 using NTILE). Determine a simple segment:
    "Champion" (all scores >= 3), "At Risk" (R score = 1), or "Average"
    (everyone else).
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q13
    con.execute(
        """
        -- Your query here
        SELECT 'Q13: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Submission

    - Submit notebook with all queries and outputs
    - **Total: 75 points**
    """)
    return


if __name__ == "__main__":
    app.run()
