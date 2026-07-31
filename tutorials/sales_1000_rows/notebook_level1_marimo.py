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
    # 📊 Flagship Notebook: Retail Sales (OMIS 105)

    This notebook walks through Weeks 1–6 using a single dataset.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Load Data
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd

    df = pd.read_csv('sales_1000.csv')

    con = duckdb.connect()
    con.register('sales_raw', df)

    df.head()
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Explore Data (Week 1–2)
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *
        FROM sales_raw
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Basic SQL (Week 3)
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            product,
            price
        FROM sales_raw;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *
        FROM sales_raw
        WHERE country = 'USA';
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Aggregation (Week 4)
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            product,
            COUNT(*) AS total_orders
        FROM sales_raw
        GROUP BY product
        ORDER BY total_orders DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5: Data Cleaning
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            product,
            CAST(REPLACE(price,'$','') AS INTEGER) AS clean_price
        FROM sales_raw
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6: Revenue Calculation
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            product,
            SUM(CAST(REPLACE(price,'$','') AS INTEGER)) AS revenue
        FROM sales_raw
        GROUP BY product
        ORDER BY revenue DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 7: Normalization (Week 6)
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE customers AS
        SELECT DISTINCT
            ROW_NUMBER() OVER () AS customer_id,
            customer_name
        FROM sales_raw
        WHERE customer_name IS NOT NULL
        AND customer_name != '';
    """)
    con.execute("""
        SELECT *
        FROM customers
        LIMIT 5;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Summary
    - Explored messy data
    - Wrote SQL queries
    - Created insights
    - Started designing databases
    """)
    return


if __name__ == "__main__":
    app.run()
