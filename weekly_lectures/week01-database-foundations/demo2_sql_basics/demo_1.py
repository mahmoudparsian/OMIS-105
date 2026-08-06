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
    # 📊 DuckDB Complete Tutorial
    # (10-Row Dataset)

    Each section includes:
    1. What we are doing
    2. SQL query
    3. Result
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup
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
        CREATE OR REPLACE TABLE sales (
            order_id INTEGER,
            country VARCHAR,
            product VARCHAR,
            quantity INTEGER,
            price INTEGER
        )
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        DESC sales
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        INSERT INTO sales VALUES
        (1,'USA','Laptop',1,1000),
        (2,'USA','Phone',2,800),
        (3,'USA','Tablet',1,500),
        (4,'Canada','Laptop',1,1000),
        (5,'Canada','Phone',1,800),
        (6,'Canada','Mouse',3,50),
        (7,'UK','Laptop',2,1000),
        (8,'UK','Mouse',5,50),
        (9,'Germany','Phone',1,800),
        (10,'Germany','Tablet',2,500)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Show all data
    ### What: display all rows
    """)
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT * FROM sales
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Select columns
    ### What: show product and price
    """)
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT product, price FROM sales
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. WHERE
    ### What: filter USA rows
    """)
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM sales 
        WHERE country = 'USA'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. ORDER BY
    ### What: sort by price descending
    """)
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM sales 
        ORDER BY price DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. LIMIT
    ### What: top 3 rows
    """)
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM sales 
        ORDER BY price DESC 
        LIMIT 3
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Computed column
    ### What: revenue
    """)
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT *, 
               quantity*price AS revenue 
        FROM sales
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. GROUP BY
    ### What: revenue per country
    """)
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT country, 
               SUM(quantity*price) AS total_revenue
        FROM sales
        GROUP BY country
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. HAVING
    ### What: countries with revenue > 2000
    """)
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT country, 
               SUM(quantity*price) AS total_revenue
        FROM sales
        GROUP BY country
        HAVING SUM(quantity*price) > 2000
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. RANK
    ### What: rank by revenue
    """)
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT country, 
               product, 
               quantity*price AS revenue,
        RANK() OVER (ORDER BY quantity*price DESC) AS rnk
        FROM sales
        """
    )
    return


if __name__ == "__main__":
    app.run()
