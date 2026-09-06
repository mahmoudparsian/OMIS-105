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
    # Week 7 - Indexing & Performance
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE TABLE sales (
            id      INT,
            product VARCHAR,
            price   INT
        );
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO sales
        VALUES
            (1,'Laptop',1000),
            (2,'Phone',800),
            (3,'Tablet',500);
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM sales
        WHERE price = 800;
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE INDEX idx_price ON sales(price);
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM sales
        WHERE price = 800;
        """
    ).fetchdf()
    return


if __name__ == "__main__":
    app.run()
