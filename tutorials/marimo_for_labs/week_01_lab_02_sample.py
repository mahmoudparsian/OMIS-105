import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Week 1 — Lab 02 (Sample)

    **Goal:** confirm that Marimo and DuckDB both work on your machine,
    and see the difference between an **in-memory** connection and a
    **persistent** (file) connection.

    Run every cell top to bottom (click ▷ on each cell, or press
    **Cmd+Enter** / **Ctrl+Enter**). If you see a table with Alice and
    Bob below, everything works.

    Full explanation of what's happening here: see
    `running_marimo_on_macbook.md` or `running_marimo_on_windows.md` in this
    same folder.
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
        """
        CREATE OR REPLACE TABLE students (
            student_id INTEGER,
            name       VARCHAR,
            gpa        DECIMAL(3,2)
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        """
        INSERT INTO students VALUES
            (1, 'Alice', 3.80),
            (2, 'Bob',   3.20)
        """
    )
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM students").fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Try It: Make This Persistent

    Right now the connection above is `:memory:` — close this notebook
    and reopen it, and the `students` table will be empty again.

    To make it persistent instead:

    1. Find the cell above that says
       `con = duckdb.connect(database=":memory:")`.
    2. Change it to:

    ```python
    con = duckdb.connect(database="week_01_lab_02_sample.duckdb")
    ```

    3. Re-run that cell, then re-run the `CREATE OR REPLACE TABLE` and
       `INSERT` cells below it (top to bottom).
    4. Close this notebook, then reopen it and run only the connection
       cell and the final `SELECT` cell — the `students` table is still
       there.

    A new file, `week_01_lab_02_sample.duckdb`, now sits in the same folder as
    this notebook. That file **is** your database.
    """)
    return


if __name__ == "__main__":
    app.run()
