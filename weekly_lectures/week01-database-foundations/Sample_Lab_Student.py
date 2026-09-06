import marimo

__generated_with = "0.23.10"
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

    ## Objectives

    - Install DuckDB and connect from Python
    - Load CSV data into a DuckDB table
    - Write basic SQL queries using SELECT, WHERE, ORDER BY, LIMIT
    - Use aggregate functions (COUNT, SUM, AVG, MIN, MAX)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    This notebook already connects to DuckDB and loads
    `./data/products.csv` into a table called `products`.
    Run the two setup cells below, then answer each question
    by writing your SQL **inside the `con.execute(...)` cell**
    that follows it.
    """)
    return


@app.cell
def _():
    DATA_DIR = "./data"  # CSVs are in week01-database-foundations/data/
    return (DATA_DIR,)


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE products AS
            SELECT * FROM read_csv_auto('{DATA_DIR}/products.csv')
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
    **Q1.** Write a query to display the first 10 rows of the `products` table.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** How many products are in the table? Write a query using `COUNT(*)`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** What are the distinct categories in the products table? Sort them alphabetically.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** Use `DESCRIBE products` to show the column names and data types. How many columns are there?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
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
    **Q5.** List all products in the "Books" category. Show product_name and price.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6.** Find all products priced between $10 and $50 (inclusive). Sort by price ascending.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** Find all products whose name contains the word "Pro". Show product_name and category.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8.** List all products that are in "Electronics" or "Sports" categories AND have a price greater than $50. Sort by price descending.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9.** Find the 5 most expensive products. Show product_name, category, and price.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** Find all products with zero stock. Show product_name and category.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
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
    **Q11.** What is the average price of all products? Round to 2 decimal places.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** What is the total inventory value (sum of price × stock_quantity) across all products?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q13.** For the "Electronics" category only, find the count, average price, minimum price, and maximum price.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
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
    **Q14.** Display each product's name, price, and a new column `price_with_tax` calculated as price × 1.0925 (9.25% sales tax). Round to 2 decimal places. Show the top 10 by price_with_tax descending.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q15.** Create a column called `stock_status` that shows:

    - "Out of Stock" if stock_quantity = 0
    - "Low Stock" if stock_quantity between 1 and 20
    - "In Stock" otherwise

    *Hint: Use a CASE expression.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
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
    **Q16.** Write a single query that answers: "What percentage of products are in each category?"
    Show category, count, and percentage (rounded to 1 decimal). Sort by percentage descending.

    *Hint: You can divide COUNT by the total count.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Your query here
        """
    )
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
