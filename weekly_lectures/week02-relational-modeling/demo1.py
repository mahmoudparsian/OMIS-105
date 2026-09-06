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
    return (con,)


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE customers (
            id   INTEGER,
            name VARCHAR
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        INSERT INTO customers VALUES (1, 'Alice'), (2, 'Bob')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO orders VALUES (1, 1, 100), (2, 1, 200), (3, 2, 150)
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM customers
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM orders
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.name, o.amount
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        """
    ).fetchdf()
    return


if __name__ == "__main__":
    app.run()
