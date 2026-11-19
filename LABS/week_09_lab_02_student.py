import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 09 · Lab 2A · Student

    Window functions (RANK, ROW_NUMBER, partitioned aggregates) on the **employees** table, using DuckDB SQL cells.

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
    Show employees above department average using window function
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
    Add department average column to each employee
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
    Compare salary vs department average
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
    Show employees whose salary rank <=2 per department
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
    Show lowest salary per department
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
    Show second highest salary per department
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
    Rank employees within region
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
    Show top salary per region using RANK
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
    Show employees sorted with rank and row_number
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
    Explain difference between RANK and ROW_NUMBER
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
