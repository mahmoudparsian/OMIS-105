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

    # 📊 Flagship Notebook Level 2: Retail Sales (OMIS 105)

    This notebook demonstrates a **full data lifecycle**:

    👉 Raw → Clean → Analytics (Medallion Architecture)

    Covers Weeks 1–6 + advanced thinking
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 0: Setup
    """)
    return


@app.cell
def _():

    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv('sales_1000.csv')
    con = duckdb.connect()
    con.register('sales_raw', df)

    df.head()

    return (con, plt)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""

    ## 🟫 Bronze Layer (Raw Data)

    - Messy
    - Unstructured
    - Real-world issues
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

    ### Data Issues
    - inconsistent dates
    - messy price
    - inconsistent country
    - missing names
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""

    ## ⚪ Silver Layer (Clean Data)

    We fix:
    - price → numeric
    - quantity → numeric
    - country → uppercase
    """)
    return


@app.cell
def _(con):

    con.execute("""
        CREATE
        OR REPLACE TABLE silver_sales AS
        SELECT
            order_id,
            order_date,
            UPPER(customer_name) AS customer_name,
            product,
            category,
            CAST(REPLACE(price,'$','') AS INTEGER) AS price,
            CAST(
                CASE quantity
                    WHEN 'one'   THEN '1'
                    WHEN 'two'   THEN '2'
                    WHEN 'three' THEN '3'
                    WHEN 'four'  THEN '4'
                    WHEN 'five'  THEN '5'
                    ELSE quantity
                END AS INTEGER
            ) AS quantity,
            discount,
            UPPER(country) AS country,
            status
        FROM sales_raw
        WHERE customer_name IS NOT NULL
        AND customer_name != '';
    """)
    con.execute("""
        SELECT *
        FROM silver_sales
        LIMIT 10;
    """).df()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""

    ## 🟡 Gold Layer (Analytics)

    We generate insights
    """)
    return


@app.cell
def _(con):

    df_gold = con.execute("""
        SELECT
            product,
            SUM(price * quantity) AS revenue
        FROM silver_sales
        GROUP BY product
        ORDER BY revenue DESC;
    """).df()

    df_gold

    return (df_gold,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 📊 Revenue by Product
    """)
    return


@app.cell
def _(df_gold, plt):

    plt.figure()
    plt.bar(df_gold['product'], df_gold['revenue'])
    plt.xticks(rotation=45)
    plt.title("Revenue by Product")
    plt.show()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Top Customers
    """)
    return


@app.cell
def _(con):

    con.execute("""
        SELECT
            customer_name,
            SUM(price * quantity) AS total_spent
        FROM silver_sales
        GROUP BY customer_name
        ORDER BY total_spent DESC
        LIMIT 10;
    """).df()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""

    ## 🧱 Normalization (Week 6)

    Split into:
    - customers
    - orders
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
        FROM silver_sales;
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

    ## 🧠 Business Insights

    Ask:
    - Which product drives revenue?
    - Who are top customers?
    - Which country performs best?
    """)
    return


@app.cell
def _(con):

    con.execute("""
        SELECT
            country,
            SUM(price * quantity) AS revenue
        FROM silver_sales
        GROUP BY country
        ORDER BY revenue DESC;
    """).df()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""

    ## ✅ Final Summary

    You performed:
    - Data exploration
    - Cleaning
    - Aggregation
    - Visualization
    - Normalization

    👉 This is real-world data work
    """)
    return


if __name__ == "__main__":
    app.run()
