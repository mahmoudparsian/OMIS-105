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
    # Week 8 - Transactions & ACID
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect()
    return (con,)


@app.cell
def _(con):
    con.execute("""
        CREATE TABLE accounts (
            id      INT,
            balance INT
        );
    """)
    return


@app.cell
def _(con):
    con.execute("""
        INSERT INTO accounts
        VALUES
            (1,1000),
            (2,500);
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *
        FROM accounts;
    """).fetchdf()
    return


@app.cell
def _(con):
    # Transaction example
    con.execute("""
        BEGIN TRANSACTION;
    """)
    con.execute("""
        UPDATE accounts
        SET balance = balance - 100
        WHERE id=1;
    """)
    con.execute("""
        UPDATE accounts
        SET balance = balance + 100
        WHERE id=2;
    """)
    con.execute('COMMIT;')
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *
        FROM accounts;
    """).fetchdf()
    return


if __name__ == "__main__":
    app.run()
