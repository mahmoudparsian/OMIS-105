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
    # Week 2 — Relational Modeling
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
        CREATE OR REPLACE TABLE customers (
            id   INTEGER,
            name VARCHAR
        )
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE orders (
            id          INTEGER,
            customer_id INTEGER,
            amount      INTEGER
        )
        """
    )
    return


@app.cell
def _(mo, customers):
    _df = mo.sql(
        f"""
        INSERT INTO customers VALUES (1, 'Alice'), (2, 'Bob')
        """
    )
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        INSERT INTO orders VALUES (1, 1, 100), (2, 1, 200), (3, 2, 150)
        """
    )
    return


@app.cell
def _(mo, customers):
    _df = mo.sql(
        f"""
        SELECT * FROM customers
        """
    )
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT * FROM orders
        """
    )
    return


@app.cell
def _(mo, customers, orders):
    _df = mo.sql(
        f"""
        SELECT c.name, o.amount
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        """
    )
    return


if __name__ == "__main__":
    app.run()
