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
    # Lab 4: JOINs and Multi-Table Queries

    ## OMIS 105 — Database Management Systems
    **Week 4 | Estimated time: 75–90 minutes**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Connect to DuckDB and load `categories`, `products`, `customers`,
    `orders`, and `order_items` from `./data/`.
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: INNER JOIN (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** Join `customers` and `orders` to display each customer's name
    alongside their order details (order_id, order_date, total_amount).
    Show the first 15 rows sorted by order_date descending.
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
    **Q2.** Join `products` and `categories` to show each product's name,
    category name, and price. Sort by category name, then price
    descending.
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
    **Q3.** Write a 3-table join: show order_id, customer name, product
    name, quantity, and unit_price for all order items. Sort by order_id.
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
    ---
    ## Part 2: LEFT JOIN (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** Find all customers who have **never** placed an order. Show
    their first_name, last_name, and email.
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
    **Q5.** Find all products that have **never** been ordered. Show
    product_name, category_id, and price.
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
    **Q6.** Show all customers with their order count. Customers with no
    orders should show 0. Sort by order_count descending.
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
    ---
    ## Part 3: JOINs with GROUP BY (20 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** Calculate total revenue per category. Show category_name,
    total units sold, and total revenue. Sort by revenue descending.
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
    **Q8.** Find the top 5 best-selling products by total units sold.
    Show product_name, total_units, and total_revenue.
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
    **Q9.** Calculate each customer's total spending across all orders.
    Show full name, number of orders, and total spent. Only include
    customers who spent more than $300.
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
    **Q10.** Create a monthly revenue report for 2024: show year, month,
    number of orders, unique customers, and total revenue. Exclude
    cancelled orders.
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
    ## Part 4: Advanced JOINs (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q11.** Using a self-join, find pairs of products in the same
    category where the price difference is less than $5. Show both
    product names, the category, and the price difference.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q11
    con.execute(
        """
        -- Your query here
        SELECT 'Q11: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** Write a query using a derived table (subquery in FROM) that
    shows each customer's name alongside their average order value. Only
    include customers with at least 3 orders.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q12
    con.execute(
        """
        -- Your query here
        SELECT 'Q12: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q13.** Create a customer segmentation report:
    - "VIP": total spending >= $1000
    - "Regular": $500–$999
    - "Occasional": $100–$499
    - "New": under $100

    Show each segment, number of customers, and average spending per
    segment.
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
    ## Part 5: Business Report (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q14.** Create a comprehensive "Product Performance Report" that
    shows:
    - Product name and category name
    - Total units sold
    - Total revenue
    - Number of distinct orders containing this product
    - Average quantity per order
    - Rank by total revenue (highest first)

    Include ALL products (even those never ordered, showing 0s).
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q14
    con.execute(
        """
        -- Your query here
        SELECT 'Q14: replace this query' AS todo
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
