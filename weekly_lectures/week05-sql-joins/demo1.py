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
    # Week 5 - JOIN Deep Dive
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE customers (
            id   INTEGER,
            name VARCHAR
        );
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE orders (
            id          INTEGER,
            customer_id INTEGER,
            product     VARCHAR,
            amount      INTEGER
        );
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        INSERT INTO customers
        VALUES
            (1,'Alice'),
            (2,'Bob'),
            (3,'Charlie');
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        INSERT INTO orders
        VALUES
            (1,1,'Laptop',1000),
            (2,1,'Phone',800),
            (3,2,'Tablet',500);
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM customers;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM orders;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT
            c.name,
            o.product,
            o.amount
        FROM customers c
        JOIN orders o ON c.id = o.customer_id;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT
            c.name,
            o.product
        FROM customers c
        LEFT
        JOIN orders o ON c.id = o.customer_id;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT
            c.name,
            SUM(o.amount) AS total
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        GROUP BY c.name
        ORDER BY total DESC;
        """
    )
    return


if __name__ == "__main__":
    app.run()
