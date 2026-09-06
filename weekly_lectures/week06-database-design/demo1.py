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
    # Week 6 - Normalization
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE TABLE raw_orders (
            order_id      INT,
            customer_name VARCHAR,
            product       VARCHAR,
            price         INT
        );
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO raw_orders
        VALUES
            (1,'Alice','Laptop',1000),
            (2,'Alice','Phone',800),
            (3,'Bob','Tablet',500);
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM raw_orders;
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE TABLE customers (
            id   INT,
            name VARCHAR
        );
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE TABLE orders (
            order_id    INT,
            customer_id INT,
            product     VARCHAR,
            price       INT
        );
        """
    )
    return


if __name__ == "__main__":
    app.run()
