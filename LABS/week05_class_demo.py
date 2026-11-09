import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 05 · Demo Lab 01 · Instructor

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
        (5,'Emma',2,'East',98000)
        ) AS t(id,name,dept_id,region,salary);
        """
    )
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM employees
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
        (4,'Finance')
        ) AS t(dept_id,dept_name);
        """
    )
    return


@app.cell
def _(departments, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM departments;
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
        JOIN departments d ON e.dept_id = d.dept_id
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q3
    Count employees per department name
    """)
    return


@app.cell
def _(departments, employees, mo):
    q3 = mo.sql(
        f"""
        SELECT d.dept_name, 
               COUNT(*) AS count_per_dept
        FROM employees e
        JOIN departments d ON e.dept_id=d.dept_id
        GROUP BY d.dept_name
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
               ROUND(AVG(salary)) AS avg_salary
        FROM employees e
        JOIN departments d ON e.dept_id=d.dept_id
        GROUP BY d.dept_name
        """
    )
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q5
    Total salary per department name
    """)
    return


@app.cell
def _(departments, employees, mo):
    q5 = mo.sql(
        f"""
        SELECT d.dept_name, 
               SUM(salary) AS total_per_dept
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
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
               MAX(salary) AS higest_salary
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
               AVG(salary) AS avg_salary
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
        ORDER BY total_salary DESC
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
        SELECT e.name, 
               e.salary, 
               d.dept_name 
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
    Show department name with counts
    """)
    return


@app.cell
def _(departments, employees, mo):
    q10 = mo.sql(
        f"""
        SELECT d.dept_name, 
               COUNT(*) AS count_per_dept
        FROM employees e
        JOIN departments d ON e.dept_id=d.dept_id
        GROUP BY d.dept_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q11: find departments with no employees
    """)
    return


@app.cell
def _(departments, employees, mo):
    q11 = mo.sql(
        f"""
        SELECT d.dept_id AS d_dept_id,
               d.dept_name AS d_dept_name,
               e.dept_id AS e_dept_id
        FROM departments d
        LEFT JOIN employees e
        ON d.dept_id = e.dept_id 
        WHERE  e.dept_id IS NULL
        """
    )
    return


if __name__ == "__main__":
    app.run()
