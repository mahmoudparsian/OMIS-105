import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb

    # In-memory database: nothing is written to disk, and the notebook starts
    # from a clean slate every time it runs.
    engine = duckdb.connect(":memory:")
    print("engine =", engine)
    return (engine,)


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE emps(name VARCHAR, age INT);
        """,
        engine=engine
    )
    return


@app.cell
def _(emps, engine, mo):
    _df = mo.sql(
        f"""
        INSERT INTO emps(name, age) 
        VALUES 
        ('alex', 20), 
        ('jane', 30);
        """,
        engine=engine
    )
    return


@app.cell
def _(emps, engine, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM emps;
        """,
        engine=engine
    )
    return


@app.cell
def _(emps, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM emps
        WHERE name = 'alex';
        """,
        engine=engine
    )
    return


if __name__ == "__main__":
    app.run()
