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
    # Week 10 - Review Notebook
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE review (
            id       INT,
            category VARCHAR,
            value    INT
        );
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO review
        VALUES
            (1,'A',100),
            (2,'B',200),
            (3,'A',150);
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
            category,
            SUM(value)
        FROM review
        GROUP BY category;
        """
    ).fetchdf()
    return


if __name__ == "__main__":
    app.run()
