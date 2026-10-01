import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 02 · Lab 1A · Instructor

    Grouping and aggregation with GROUP BY on the **employees** table, using DuckDB SQL cells.

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
        ) AS t(id,name,department,region,salary);
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q1
    Count employees per department
    """)
    return

@app.cell
def _(employees, mo):
    q1 = mo.sql(
        f"""
        SELECT department, COUNT(*)
        FROM employees
        GROUP BY department;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q2
    Average salary per department
    """)
    return

@app.cell
def _(employees, mo):
    q2 = mo.sql(
        f"""
        SELECT department, AVG(salary)
        FROM employees
        GROUP BY department;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q3
    Total salary per department
    """)
    return

@app.cell
def _(employees, mo):
    q3 = mo.sql(
        f"""
        SELECT department, SUM(salary)
        FROM employees
        GROUP BY department;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q4
    Count employees per region
    """)
    return

@app.cell
def _(employees, mo):
    q4 = mo.sql(
        f"""
        SELECT region, COUNT(*)
        FROM employees
        GROUP BY region;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q5
    Average salary per region
    """)
    return

@app.cell
def _(employees, mo):
    q5 = mo.sql(
        f"""
        SELECT region, AVG(salary)
        FROM employees
        GROUP BY region;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q6
    Department + region counts
    """)
    return

@app.cell
def _(employees, mo):
    q6 = mo.sql(
        f"""
        SELECT department, region, COUNT(*)
        FROM employees
        GROUP BY department, region;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q7
    Department salary sorted descending
    """)
    return

@app.cell
def _(employees, mo):
    q7 = mo.sql(
        f"""
        SELECT department, SUM(salary)
        FROM employees
        GROUP BY department
        ORDER BY SUM(salary) DESC;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q8
    Min salary per department
    """)
    return

@app.cell
def _(employees, mo):
    q8 = mo.sql(
        f"""
        SELECT department, MIN(salary)
        FROM employees
        GROUP BY department;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q9
    Max salary per department
    """)
    return

@app.cell
def _(employees, mo):
    q9 = mo.sql(
        f"""
        SELECT department, MAX(salary)
        FROM employees
        GROUP BY department;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q10
    Total salary per region
    """)
    return

@app.cell
def _(employees, mo):
    q10 = mo.sql(
        f"""
        SELECT region, SUM(salary)
        FROM employees
        GROUP BY region;
        """
    )
    return

if __name__ == "__main__":
    app.run()
