import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 9 - Project Starter
    ## Build your own database
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Create Tables
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE customers (
            id   INT,
            name VARCHAR
        );
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Insert Data
    """)
    return


@app.cell
def _(con):
    # Insert your data here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Write Queries
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM customers;
        """
    ).fetchdf()
    return


if __name__ == "__main__":
    app.run()
