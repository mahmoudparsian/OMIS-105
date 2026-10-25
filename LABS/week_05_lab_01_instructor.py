import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 05 · Lab 1A · Instructor

    Joining tables, using DuckDB SQL cells.

    Run the setup cells first, then each question. Answers are filled in.
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
    Join employees + departments  (2-table join)
    """)
    return

@app.cell
def _(departments, employees, mo):
    q1 = mo.sql(
        f"""
        SELECT e.name, 
               d.dept_name
        FROM employees e
        JOIN departments d ON e.dept_id=d.dept_id
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q2
    Show employee and region name
    """)
    return

@app.cell
def _(employees, mo, regions):
    q2 = mo.sql(
        f"""
        SELECT e.name,
               r.region_name
        FROM employees e
        JOIN regions r ON e.region=r.region
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q3
    Count employees per department name 
    """)
    return

@app.cell
def _(departments, employees, mo, regions):
    q3 = mo.sql(
        f"""
        SELECT d.dept_name, 
               r.region_name, 
               COUNT(*)
        FROM employees e
        JOIN departments d ON e.dept_id=d.dept_id
        JOIN regions r ON e.region=r.region
        GROUP BY d.dept_name, r.region_name
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q4
    Average salary per department name
    """)
    return

@app.cell
def _(departments, employees, mo):
    q4 = mo.sql(
        f"""
        SELECT d.dept_name, 
               AVG(salary)
        FROM employees e
        JOIN departments d ON e.dept_id=d.dept_id
        GROUP BY d.dept_name
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q5
    Total salary per region_name
    """)
    return

@app.cell
def _(employees, mo, regions):
    q5 = mo.sql(
        f"""
        SELECT r.region_name, SUM(salary)
        FROM employees e
        JOIN regions r ON e.region=r.region
        GROUP BY r.region_name
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q6
    Show highest paid employee per department
    """)
    return

@app.cell
def _(departments, employees, mo):
    q6 = mo.sql(
        f"""
        SELECT d.dept_name, 
               MAX(salary)
        FROM employees e
        JOIN departments d ON e.dept_id=d.dept_id
        GROUP BY d.dept_name
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q7
    Show department names with avg salary > 80000
    """)
    return

@app.cell
def _(departments, employees, mo):
    q7 = mo.sql(
        f"""
        SELECT d.dept_name, 
               AVG(salary)
        FROM employees e
        JOIN departments d ON e.dept_id=d.dept_id
        GROUP BY d.dept_name
        HAVING AVG(salary) > 80000
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q8
    Sort department names by total salary
    """)
    return

@app.cell
def _(departments, employees, mo):
    q8 = mo.sql(
        f"""
        SELECT d.dept_name, 
               SUM(salary) AS total_salary
        FROM employees e
        JOIN departments d ON e.dept_id=d.dept_id
        GROUP BY d.dept_name
        ORDER BY total DESC
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q9
    Top 3 salaries with full info
    """)
    return

@app.cell
def _(departments, employees, mo):
    q9 = mo.sql(
        f"""
        SELECT e.name, d.dept_name, e.salary
        FROM employees e
        JOIN departments d ON e.dept_id=d.dept_id
        ORDER BY salary DESC
        LIMIT 3
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q10
    Show department name + region name combinations with counts
    """)
    return

@app.cell
def _(departments, employees, mo, regions):
    q10 = mo.sql(
        f"""
        SELECT d.dept_name, 
               r.region_name, 
               COUNT(*) AS combinations_count
        FROM employees e
        JOIN departments d ON e.dept_id=d.dept_id
        JOIN regions r ON e.region=r.region
        GROUP BY d.dept_name, r.region_name
        """
    )
    return

if __name__ == "__main__":
    app.run()
