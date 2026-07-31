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
    # Week 4 - Aggregation & GROUP BY
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE sales (
            id       INTEGER,
            product  VARCHAR,
            price    INTEGER,
            quantity INTEGER
        );
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        INSERT INTO sales
        VALUES
            (1,'Laptop',1000,1),
            (2,'Phone',800,2),
            (3,'Tablet',500,3),
            (4,'Laptop',1200,1),
            (5,'Phone',900,1);
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT *
        FROM sales;
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT COUNT(*)
        FROM sales;
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT SUM(price * quantity) AS total_revenue
        FROM sales;
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT
            product,
            SUM(price * quantity) AS revenue
        FROM sales
        GROUP BY product;
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT
            product,
            SUM(price * quantity) AS revenue
        FROM sales
        GROUP BY product
        HAVING revenue > 1500;
        """
    )
    return


if __name__ == "__main__":
    app.run()
