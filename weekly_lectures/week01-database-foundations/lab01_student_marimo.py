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
    # Lab 1: Getting Started with DuckDB and SQL Basics

    ## OMIS 105 — Database Management Systems
    **Week 1 | Estimated time: 60–90 minutes**

    ---

    ## Objectives

    - Connect to DuckDB from Python
    - Load CSV data into a DuckDB table
    - Write basic SQL queries using SELECT, WHERE, ORDER BY, LIMIT
    - Use aggregate functions (COUNT, SUM, AVG, MIN, MAX)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Make sure `./data/products.csv` is available, then run this cell to
    connect to DuckDB and load it into a `products` table.
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
        """
        CREATE OR REPLACE TABLE products AS
        SELECT * FROM read_csv_auto('./data/products.csv')
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Exploration (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** (2 pts) Write a query to display the first 10 rows of the `products` table.
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
    **Q2.** (2 pts) How many products are in the table? Use `COUNT(*)`.
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
    **Q3.** (3 pts) What are the distinct categories in the `products` table?
    Sort them alphabetically.
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
    **Q4.** (3 pts) Use `DESCRIBE products` to show the column names and data
    types. How many columns are there?
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
    ---
    ## Part 2: Filtering and Sorting (20 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** (3 pts) List all products in the "Books" category. Show
    `product_name` and `price`.
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
    **Q6.** (3 pts) Find all products priced between $10 and $50 (inclusive).
    Sort by price ascending.
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
    **Q7.** (3 pts) Find all products whose name contains the word "Pro".
    Show `product_name` and `category`.
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
    **Q8.** (4 pts) List all products that are in "Electronics" or "Sports"
    categories AND have a price greater than $50. Sort by price descending.
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
    **Q9.** (3 pts) Find the 5 most expensive products. Show `product_name`,
    `category`, and `price`.
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
    **Q10.** (4 pts) Find all products with zero stock. Show `product_name`
    and `category`.
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
    ## Part 3: Aggregation (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q11.** (5 pts) What is the average price of all products? Round to 2
    decimal places.
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
    **Q12.** (5 pts) What is the total inventory value (sum of
    price × stock_quantity) across all products?
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
    **Q13.** (5 pts) For the "Electronics" category only, find the count,
    average price, minimum price, and maximum price.
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
    ## Part 4: Computed Columns (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q14.** (5 pts) Display each product's name, price, and a new column
    `price_with_tax` calculated as price × 1.0925 (9.25% sales tax). Round to
    2 decimal places. Show the top 10 by `price_with_tax` descending.
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
    **Q15.** (5 pts) Create a column called `stock_status` that shows:
    - "Out of Stock" if stock_quantity = 0
    - "Low Stock" if stock_quantity between 1 and 20
    - "In Stock" otherwise

    *Hint: Use a `CASE` expression.*
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q15
    con.execute(
        """
        -- Your query here
        SELECT 'Q15: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Challenge (5 points — bonus)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q16.** Write a single query that answers: "What percentage of products
    are in each category?" Show `category`, `count`, and `percentage`
    (rounded to 1 decimal). Sort by percentage descending.

    *Hint: You can divide COUNT by the total count.*
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q16 (bonus)
    con.execute(
        """
        -- Your query here
        SELECT 'Q16: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Submission

    - Submit your completed notebook with all queries and their output
    - Ensure all queries run without errors
    - Add brief comments explaining your approach for Q15 and Q16

    **Total: 60 points (+ 5 bonus)**
    """)
    return


if __name__ == "__main__":
    app.run()
