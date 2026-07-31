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

    # DuckDB + JupySQL (In-Memory Database)

    This notebook demonstrates:

    - DuckDB
    - JupySQL magic
    - In-memory database

    The database exists only while the notebook session is active.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create employees table
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE employees (
            emp_id     INTEGER,
            emp_name   VARCHAR,
            department VARCHAR,
            salary     INTEGER
        );
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Insert 7 rows
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        INSERT INTO employees
        VALUES
            (100, 'Alex', 'SALES', 120000),
            (200, 'Jeff', 'SALES', 140000),
            (300, 'Rafa', 'BUSINESS', 150000),
            (400, 'Susan', 'SALES', 150000),
            (500, 'Jen', 'BUSINESS', 160000),
            (600, 'Barb', 'BUSINESS', 180000),
            (700, 'Dara', 'AI', 190000);
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Read all rows
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM employees
        ORDER BY emp_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## GROUP BY example
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT
            department,
            COUNT(*) AS employee_count,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
        """
    )
    return


if __name__ == "__main__":
    app.run()
