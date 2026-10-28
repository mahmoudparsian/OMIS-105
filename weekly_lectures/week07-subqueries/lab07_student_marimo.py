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
    # Lab 7: Subqueries — A Query Inside a Query

    ## OMIS 105 — Database Management Systems
    **Week 7 | Estimated time: 75–90 minutes | 10 questions × 3 points = 30 points**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Run the next two cells first. They connect to DuckDB and load `customers`, `products`, `orders`
    from this folder's `data/` directory — the same data as the demos.

    **Rules for every query:** give every table an alias and use it on every
    column; list the columns you need (no `SELECT *`); use the `ORDER BY` given
    in the question. The **expected row count** is given for each question —
    if yours is different, look again at your query.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import duckdb

    DATA_DIR = Path(__file__).parent / "data"
    con = duckdb.connect(database=":memory:")
    return DATA_DIR, con


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv('{DATA_DIR}/customers.csv')"
    )
    con.execute(
        f"CREATE OR REPLACE TABLE products AS SELECT * FROM read_csv('{DATA_DIR}/products.csv')"
    )
    con.execute(
        f"CREATE OR REPLACE TABLE orders AS SELECT * FROM read_csv('{DATA_DIR}/orders.csv')"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Scalar Subqueries — One Value (9 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1. Cheaper than average.** Show `product_name` and `price` for products that cost **less** than the average price. Order by `price`.

    *Expected: 6 rows.*
    """)
    return


@app.cell
def _(con):
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
    **Q2. The cheapest product.** Show `product_name` and `price` of the product(s) with the **lowest** price. Use `MIN` in a subquery, not `ORDER BY ... LIMIT 1`.

    *Expected: 1 row.*
    """)
    return


@app.cell
def _(con):
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
    **Q3. A subquery in `SELECT`.** For every product, show `product_name`, `price`, and how much more it costs than the cheapest product, as `above_cheapest`. Order by `above_cheapest` (highest first).

    *Expected: 8 rows.*
    """)
    return


@app.cell
def _(con):
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
    ## Part 2: List Subqueries — `IN`, `NOT IN`, `EXISTS` (12 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4. Nested `IN`.** Show the `product_name` of every product ordered by a customer who lives in `'San Jose'`. Use two nested `IN` subqueries, no JOIN. Order by `product_name`.

    *Expected: 4 rows.*
    """)
    return


@app.cell
def _(con):
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
    **Q5. `NOT IN`.** Show the `product_name` of products that were **never ordered**. Order by `product_name`. In one sentence: why is `NOT IN` safe here, but not for customers?

    *Expected: 2 rows.*

    *(Write your answer here.)*
    """)
    return


@app.cell
def _(con):
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
    **Q6. `NOT EXISTS`.** Show `customer_name` and `city` of customers who **never ordered**. Use `NOT EXISTS`. Order by `customer_name`.

    *Expected: 2 rows.*
    """)
    return


@app.cell
def _(con):
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
    **Q7. `EXISTS`.** Show the `product_name` of products that appear in **at least one** order with a `quantity` of **3 or more**. Use `EXISTS`. Order by `product_name`.

    *Expected: 2 rows.*
    """)
    return


@app.cell
def _(con):
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
    ---
    ## Part 3: Going Further (9 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8. A subquery in `FROM`.** What is the average number of orders per customer? Count orders per customer in a subquery (leave out the guest order), then average those counts in the outer query, rounded to 2 decimals, as `avg_orders_per_customer`.

    *Expected: 1 row.*
    """)
    return


@app.cell
def _(con):
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
    **Q9. Correlated subquery.** Show `product_name`, `category`, and `price` of products that cost **less** than the average price **of their own category**. Order by `category`, then `product_name`.

    *Expected: 5 rows.*
    """)
    return


@app.cell
def _(con):
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
    **Q10. CTE.** Use `WITH product_sales AS (...)` to total the `quantity` sold per product as `units_sold`. Then show the `product_name` and `units_sold` of the best-selling product(s).

    *Expected: 1 row.*
    """)
    return


@app.cell
def _(con):
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
    ## Grading

    - 3 points per question: 2 for a correct result, 1 for a clean query
      (and, where asked, the short written answer)
    - **Total: 30 points**

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
