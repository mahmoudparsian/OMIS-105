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
    # Week 3 — SQL Core
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
        CREATE OR REPLACE TABLE sales (
            id       INTEGER,
            product  VARCHAR,
            price    INTEGER,
            quantity INTEGER
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO sales VALUES
            (1, 'Laptop',  1000, 1),
            (2, 'Phone',    800, 2),
            (3, 'Tablet',   500, 3),
            (4, 'Laptop',  1200, 1)
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM sales
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product, price FROM sales
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM sales WHERE price > 700
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM sales WHERE price > 700 AND quantity >= 1
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM sales ORDER BY price DESC
        """
    ).fetchdf()
    return


if __name__ == "__main__":
    app.run()
