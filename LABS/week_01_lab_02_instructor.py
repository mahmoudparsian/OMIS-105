import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 01 · Lab 02 · Instructor

    Basic `SELECT` queries on an **employees** table, using DuckDB SQL cells.

    Run the setup cell first, then each question cell. Answers are filled in.
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    employees = mo.sql(
        f"""
        CREATE OR REPLACE TABLE employees AS
        SELECT * FROM (
            VALUES
            (1,'Alice','Sales','West',70000),
            (2,'Bob','Sales','West',90000),
            (3,'Carol','Sales','East',72000),
            (4,'David','IT','West',95000),
            (5,'Emma','IT','East',98000),
            (6,'Frank','IT','East',115000),
            (7,'Grace','HR','West',65000),
            (8,'Henry','HR','East',85000),
            (9,'Ivy','Finance','West',78000),
            (10,'Jack','Finance','East',105000),
            (11,'Karen','Finance','East',80000),
            (12,'Leo','Marketing','West',68000)
        ) AS t(id, name, department, region, salary);
        """
    )
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        DESC employees;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q1 — Show all rows
    """)
    return


@app.cell
def _(employees, mo):
    q1 = mo.sql(
        f"""
        SELECT *
        FROM employees;
        """
    )
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        SELECT id, name, department, region, salary
        FROM employees;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q2 — Show name and salary
    """)
    return


@app.cell
def _(employees, mo):
    q2 = mo.sql(
        f"""
        SELECT name, salary
        FROM employees;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q3 — Sales employees
    """)
    return


@app.cell
def _(employees, mo):
    q3 = mo.sql(
        f"""
        SELECT *
        FROM employees
        WHERE department = 'Sales';
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q4 — Salary above 90000
    """)
    return


@app.cell
def _(employees, mo):
    q4 = mo.sql(
        f"""
        SELECT id, name, department, region, salary
        FROM employees
        WHERE salary > 90000;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM duckdb_keywords() 
        WHERE keyword_name = 'name';
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q5 — East region
    """)
    return


@app.cell
def _(employees, mo):
    q5 = mo.sql(
        f"""
        SELECT *
        FROM employees
        WHERE region = 'East';
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q6 — Sort by salary (highest first)
    """)
    return


@app.cell
def _(employees, mo):
    q6 = mo.sql(
        f"""
        SELECT *
        FROM employees
        ORDER BY salary DESC;
        """
    )
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        -- find employees — Sort by salary (lowewst first)
        SELECT *
        FROM employees
        ORDER BY salary;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q7 — Top 3 salaries
    """)
    return


@app.cell
def _(employees, mo):
    q7 = mo.sql(
        f"""
        SELECT *
        FROM employees
        ORDER BY salary DESC
        LIMIT 3;
        """
    )
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        -- bottom 3 salaries
        -- comment line 2
        SELECT *
        FROM employees
        ORDER BY salary 
        LIMIT 3;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q8 — IT employees, sorted by salary
    """)
    return


@app.cell
def _(employees, mo):
    q8 = mo.sql(
        f"""
        SELECT *
        FROM employees
        WHERE department = 'IT'
        ORDER BY salary DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q9 — Salary between 70000 and 90000
    """)
    return


@app.cell
def _(employees, mo):
    q9 = mo.sql(
        f"""
        SELECT *
        FROM employees
        WHERE salary BETWEEN 70000 AND 90000;
        """
    )
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        -- without using BETWEEN
        SELECT *
        FROM employees
        WHERE (salary >= 70000) AND 
              (salary <= 90000);
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q10 — Name starts with A
    """)
    return


@app.cell
def _(employees, mo):
    q10 = mo.sql(
        f"""
        SELECT *
        FROM employees
        WHERE name LIKE 'A%';
        """
    )
    return


if __name__ == "__main__":
    app.run()
