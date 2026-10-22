import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 05 · Lab 2A · Student

    Joining tables, using DuckDB SQL cells.

    Run the setup cell first, then write your SQL in each question cell (replace `-- YOUR SQL HERE`).
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
        (1,'Alice',1,'West',70000),
        (2,'Bob',1,'West',90000),
        (3,'Carol',1,'East',72000),
        (4,'David',2,'West',95000),
        (5,'Emma',2,'East',98000),
        (6,'Frank',2,'East',115000),
        (7,'Grace',3,'West',65000),
        (8,'Henry',3,'East',85000),
        (9,'Ivy',4,'West',78000),
        (10,'Jack',4,'East',105000),
        (11,'Karen',4,'East',80000),
        (12,'Leo',5,'West',68000)
        ) AS t(id,name,dept_id,region,salary);
        """
    )
    return

@app.cell
def _(mo):
    departments = mo.sql(
        f"""
        CREATE OR REPLACE TABLE departments AS
        SELECT * FROM (
        VALUES
        (1,'Sales'),
        (2,'IT'),
        (3,'HR'),
        (4,'Finance'),
        (5,'Marketing')
        ) AS t(dept_id,dept_name);
        """
    )
    return

@app.cell
def _(mo):
    regions = mo.sql(
        f"""
        CREATE OR REPLACE TABLE regions AS
        SELECT * FROM (
        VALUES
        ('West','USA-West'),
        ('East','USA-East')
        ) AS t(region,region_name);
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q1
    Self join: pair employees in same department
    """)
    return

@app.cell
def _(mo):
    q1 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q2
    Count employees per department using self join
    """)
    return

@app.cell
def _(mo):
    q2 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q3
    Show employees earning more than coworkers (same dept)
    """)
    return

@app.cell
def _(mo):
    q3 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q4
    Show highest salary per department using self join logic
    """)
    return

@app.cell
def _(mo):
    q4 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q5
    Compare each employee with dept average (join + subquery)
    """)
    return

@app.cell
def _(mo):
    q5 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q6
    Show departments with more than 2 employees (join version)
    """)
    return

@app.cell
def _(mo):
    q6 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q7
    Show employees with same salary (self join)
    """)
    return

@app.cell
def _(mo):
    q7 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q8
    Show employee vs all others in same dept
    """)
    return

@app.cell
def _(mo):
    q8 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q9
    Show employees with salary above department avg
    """)
    return

@app.cell
def _(mo):
    q9 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q10
    Top employee per department using ranking logic (preview)
    """)
    return

@app.cell
def _(mo):
    q10 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

if __name__ == "__main__":
    app.run()
