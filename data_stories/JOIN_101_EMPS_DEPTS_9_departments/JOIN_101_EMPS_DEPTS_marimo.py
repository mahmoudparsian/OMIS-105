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
    # 🗂️ JOIN 101 — Employees & Departments
    ### A Complete Introduction to SQL JOIN Operations with DuckDB
    ---
    > **Course:** OMIS 105 · Data Stories  
    > **Topic:** Relational Joins — INNER, LEFT, RIGHT  
    > **Tools:** Python · DuckDB · Pandas · Matplotlib  

    ---
    ## 📚 What You Will Learn

    By the end of this notebook you will be able to:

    1. **Explain** what a JOIN is and *why* it exists
    2. **Distinguish** between INNER, LEFT, and RIGHT JOINs
    3. **Write** SQL queries that combine two tables using a shared key
    4. **Interpret** NULL values that appear after LEFT / RIGHT JOINs
    5. **Visualise** join results with meaningful charts

    ---
    ## 📂 Our Two Tables

    | Table | File | What it contains |
    |-------|------|-----------------|
    | `employees` | `data/employees.csv` | 25 employees — some assigned to departments not in the departments table |
    | `departments` | `data/departments.csv` | 9 departments — two have *no* employees assigned |

    This deliberate mismatch makes LEFT / RIGHT joins interesting and educational!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ⚙️ Section 0 — Setup

    We import libraries, load our helper utilities, and connect to DuckDB.

    > **DuckDB** is an in-process SQL database engine — think of it like SQLite but
    > optimised for analytical queries. It runs entirely inside this notebook;
    > no server required.
    """)
    return


@app.cell
def _():
    # ── Standard library imports ──────────────────────────────────────────────
    import sys, os
    import duckdb
    import pandas as pd

    # ── Add the notebook folder to the path so we can import notebook_utils ───
    sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))

    # ── Import all display / plotting helpers ─────────────────────────────────
    # (All plotting and table-display code lives in notebook_utils.py)
    # (This keeps the notebook clean and focused on SQL!)
    from notebook_utils import (
        show_df, bar_chart, pie_chart, grouped_bar,
        scatter_chart, salary_hist, draw_join_venn, match_summary_bar
    )

    print('✅ Libraries loaded successfully!')

    return (bar_chart, draw_join_venn, duckdb, grouped_bar, match_summary_bar, os, pd, pie_chart, salary_hist, scatter_chart, show_df)


@app.cell
def _(duckdb, os):
    # ── Connect to DuckDB (in-memory) ─────────────────────────────────────────
    con = duckdb.connect()          # in-memory database

    # Base path — adjust if you move the notebook
    BASE = os.path.dirname(os.path.abspath('__file__'))
    EMP_CSV  = os.path.join(BASE, 'data', 'employees.csv')
    DEPT_CSV = os.path.join(BASE, 'data', 'departments.csv')

    print(f'📁 Employees  : {EMP_CSV}')
    print(f'📁 Departments: {DEPT_CSV}')

    return (DEPT_CSV, EMP_CSV, con)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🏗️ Section 1 — Create Tables

    We create two persistent in-memory tables from our CSV files.
    The `DROP TABLE IF EXISTS` lines make this notebook **idempotent** —
    you can run it from top to bottom as many times as you like.
    """)
    return


@app.cell
def _(DEPT_CSV, EMP_CSV, con):
    # ── Drop tables if they already exist (so we can re-run safely) ──────────
    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)
    con.execute("""
        DROP TABLE IF EXISTS departments;
    """)

    # ── Create employees table ────────────────────────────────────────────────
    con.execute(f'''
        CREATE TABLE employees AS
        SELECT * FROM read_csv_auto('{EMP_CSV}', header=true)
    ''')

    # ── Create departments table ──────────────────────────────────────────────
    con.execute(f'''
        CREATE TABLE departments AS
        SELECT * FROM read_csv_auto('{DEPT_CSV}', header=true)
    ''')

    print('✅ Tables created!')
    print(f'   employees  : {con.execute("SELECT count(*) FROM employees").fetchone()[0]} rows')
    print(f'   departments: {con.execute("SELECT count(*) FROM departments").fetchone()[0]} rows')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 👀 Preview: employees table
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT *
        FROM employees
        LIMIT 10;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='employees — first 10 rows')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 👀 Preview: departments table
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT *
        FROM departments;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='departments — all rows')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Section 2 — 5 Basic Queries (SELECT, WHERE, LIMIT, GROUP BY)

    Before we tackle JOINs, let's warm up with single-table queries.

    | Clause | Purpose |
    |--------|---------|
    | `SELECT` | Choose which columns to return |
    | `FROM` | Which table to read from |
    | `WHERE` | Filter rows by a condition |
    | `GROUP BY` | Aggregate rows that share a value |
    | `ORDER BY` | Sort the result |
    | `LIMIT` | Return at most *n* rows |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Basic Query 1 — Top 5 highest-paid employees
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            employee_id,
            first_name,
            last_name,
            job_title,
            salary
        FROM employees
        ORDER BY salary DESC
        LIMIT 5;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Top 5 Highest-Paid Employees')
    bar_chart(_result, x='last_name', y='salary',
              title='Top 5 Highest-Paid Employees',
              xlabel='Employee', ylabel='Salary ($)',
              color='#4C72B0')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Basic Query 2 — Engineers only (WHERE + LIKE)
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            employee_id,
            first_name || ' ' || last_name AS full_name,
            job_title,
            salary,
            city
        FROM employees
        WHERE job_title LIKE '%Engineer%'
        ORDER BY salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Employees Whose Title Contains "Engineer"')
    bar_chart(_result, x='full_name', y='salary',
              title='Engineers by Salary', xlabel='Name', ylabel='Salary ($)',
              color='#55A868')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Basic Query 3 — Number of employees per department_id
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            department_id,
            COUNT(*) AS num_employees,
            AVG(salary) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY department_id
        ORDER BY num_employees DESC;
    """
    _result = con.execute(_sql).df()
    _result['avg_salary'] = _result['avg_salary'].round(0).astype(int)
    show_df(_result, title='Employee Count & Salary Stats per Department ID')
    bar_chart(_result, x='department_id', y='num_employees',
              title='Employees per Department ID',
              xlabel='Department ID', ylabel='Count',
              color='#DD8452')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Basic Query 4 — Employees hired after 2020
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            first_name || ' ' || last_name AS full_name,
            job_title,
            hire_date,
            salary
        FROM employees
        WHERE hire_date >= '2021-01-01'
        ORDER BY hire_date;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Employees Hired in 2021 or Later')
    bar_chart(_result, x='full_name', y='salary',
              title='Salary of Employees Hired 2021+',
              xlabel='Employee', ylabel='Salary ($)',
              horizontal=True, figsize=(10, 6))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Basic Query 5 — City headcount
    """)
    return


@app.cell
def _(con, pie_chart, show_df):
    _sql = """
        SELECT
            city,
            COUNT(*) AS num_employees
        FROM employees
        GROUP BY city
        ORDER BY num_employees DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Number of Employees per City')
    pie_chart(_result, labels='city', values='num_employees',
              title='Employee Distribution by City')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🔗 Section 3 — What IS a JOIN? (Concept Introduction)

    ### The Core Problem

    Our data is stored in **separate tables** to avoid repetition:

    - The `employees` table stores each person once, and refers to their department
      using a number (`department_id`).
    - The `departments` table stores the department *name*, *budget*, and *location*
      under each `department_id`.

    If we want to see an employee's **name AND their department name** in one row,
    we need to **combine** the two tables. That combination is called a **JOIN**.

    ---
    ### The Linking Key

    ```
    employees.department_id  ←──→  departments.department_id
    ```

    Both tables share `department_id`. DuckDB (and all SQL databases) use this
    shared column to know which rows "belong together".

    ---
    ### Three Types of JOIN

    | JOIN Type | Rows Returned |
    |-----------|--------------|
    | **INNER JOIN** | Only rows where `department_id` matches in **both** tables |
    | **LEFT JOIN** | All employees + matching department info (unmatched → NULL) |
    | **RIGHT JOIN** | All departments + matching employee info (unmatched → NULL) |

    ---
    ### Our Intentional Mismatches

    | Situation | department_ids | Why it matters |
    |-----------|---------------|----------------|
    | Employees with unknown departments | 99, 88 | Will appear in LEFT JOIN, disappear in INNER |
    | Departments with no employees | 80 (Legal), 90 (Customer Success) | Will appear in RIGHT JOIN, disappear in INNER |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Visual: INNER JOIN
    """)
    return


@app.cell
def _(draw_join_venn):
    draw_join_venn('inner')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Visual: LEFT JOIN
    """)
    return


@app.cell
def _(draw_join_venn):
    draw_join_venn('left')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Visual: RIGHT JOIN
    """)
    return


@app.cell
def _(draw_join_venn):
    draw_join_venn('right')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🔵 Section 4 — INNER JOIN (15 Join Queries)

    ---
    ### 📘 What is an INNER JOIN?

    ```
    An INNER JOIN returns ONLY the rows where the join key matches in BOTH tables.
    If an employee's department_id does not appear in the departments table,
    that employee is LEFT OUT of the result.
    Likewise, a department with no employees is also excluded.
    ```

    **Syntax:**
    ```sql
    SELECT  ...
    FROM    employees  AS e
    INNER JOIN departments AS d  ON e.department_id = d.department_id
    ```

    > 💡 `AS e` and `AS d` are **aliases** — short nicknames for the table names.
    > Instead of writing `employees.salary` we can write `e.salary`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 1 — Employee name + department name (INNER JOIN)
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            e.job_title,
            d.department_name,
            e.salary
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.department_id = d.department_id
        ORDER BY d.department_name, e.salary DESC;
    """
    result = con.execute(_sql).df()
    show_df(result, title='All Matched Employees with Their Department Name')
    # Note: employees with dept 99 and 88 are NOT in this result
    print(f'Rows returned: {len(result)}  (25 employees - 2 unmatched = 23)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 2 — Avg salary by department name
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            d.department_name,
            COUNT(e.employee_id) AS num_employees,
            ROUND(AVG(e.salary), 0) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY avg_salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Average Salary by Department (INNER JOIN)')
    bar_chart(_result, x='department_name', y='avg_salary',
              title='Average Salary by Department',
              xlabel='Department', ylabel='Avg Salary ($)',
              color='#4C72B0')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 3 — Employees earning above dept average
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS full_name,
            e.job_title,
            d.department_name,
            e.salary,
            ROUND(AVG(e.salary) OVER (PARTITION BY d.department_id), 0) AS dept_avg
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.department_id = d.department_id
        WHERE e.salary > (
        SELECT AVG(e2.salary)
        FROM employees e2
        WHERE e2.department_id = e.department_id)
        ORDER BY d.department_name, e.salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Employees Earning Above Their Department Average')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 4 — Budget vs actual payroll per department
    """)
    return


@app.cell
def _(con, grouped_bar, show_df):
    _sql = """
        SELECT
            d.department_name,
            d.budget,
            SUM(e.salary) AS total_payroll,
            d.budget - SUM(e.salary) AS budget_remaining
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.department_id = d.department_id
        GROUP BY d.department_name, d.budget
        ORDER BY budget_remaining;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Department Budget vs Total Payroll')
    grouped_bar(_result, x='department_name',
                y_cols=['budget', 'total_payroll'],
                title='Budget vs Total Payroll by Department',
                ylabel='Amount ($)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 5 — Employees in departments located in New York
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS full_name,
            e.job_title,
            e.salary,
            d.department_name,
            d.location AS dept_location
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.department_id = d.department_id
        WHERE d.location = 'New York'
        ORDER BY e.salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Employees in New York Departments')
    bar_chart(_result, x='full_name', y='salary',
              title='NY Department Employees by Salary',
              horizontal=True, figsize=(10,5))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 6 — Salary histogram for Engineering dept
    """)
    return


@app.cell
def _(con, salary_hist, show_df):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS full_name,
            e.salary,
            d.department_name
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.department_id = d.department_id
        WHERE d.department_name = 'Engineering'
        ORDER BY e.salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Engineering Department — Salary Details')
    salary_hist(_result, col='salary', title='Salary Distribution — Engineering Dept', bins=5)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 7 — Count employees per department location
    """)
    return


@app.cell
def _(con, pie_chart, show_df):
    _sql = """
        SELECT
            d.location,
            COUNT(e.employee_id) AS num_employees
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.department_id = d.department_id
        GROUP BY d.location
        ORDER BY num_employees DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Employees per Department Location (INNER JOIN)')
    pie_chart(_result, labels='location', values='num_employees',
              title='Employees by Department Location')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 8 — Manager name for each employee
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS employee,
            e.job_title,
            d.department_name,
            d.manager_name
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.department_id = d.department_id
        ORDER BY d.department_name, e.last_name;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Each Employee and Their Department Manager')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 9 — Salary vs. dept budget (scatter)
    """)
    return


@app.cell
def _(con, scatter_chart, show_df):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS full_name,
            e.salary,
            d.budget,
            d.department_name
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.department_id = d.department_id;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Employee Salary vs. Department Budget')
    scatter_chart(_result, x='budget', y='salary',
                  title='Individual Salary vs. Department Total Budget',
                  color_col='department_name')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 10 — Top earner in each department
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            d.department_name,
            e.first_name || ' ' || e.last_name AS top_earner,
            e.job_title,
            e.salary
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.department_id = d.department_id QUALIFY e.salary = MAX(e.salary) OVER (PARTITION BY d.department_id)
        ORDER BY e.salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Top Earner in Each Department')
    bar_chart(_result, x='department_name', y='salary',
              title='Highest Salary per Department',
              xlabel='Department', ylabel='Salary ($)',
              color='#C44E52')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🟡 Section 5 — LEFT JOIN

    ---
    ### 📘 What is a LEFT JOIN?

    ```
    A LEFT JOIN returns ALL rows from the LEFT (first) table.
    For each left-table row, it tries to find a matching row in the right table.
      • If a match IS found  → join data from the right table is included.
      • If NO match is found → the right-table columns are filled with NULL.
    ```

    **In our case:**
    - The **left** table is `employees`
    - ALL 25 employees appear in the result
    - Employees with `department_id` = 99 or 88 (not in departments) will have
      `NULL` for every department column

    **Syntax:**
    ```sql
    SELECT ...
    FROM   employees  AS e
    LEFT JOIN departments AS d  ON e.department_id = d.department_id
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 11 — ALL employees, NULLs where dept unknown (LEFT JOIN)
    """)
    return


@app.cell
def _(con, match_summary_bar, show_df):
    _sql = """
        SELECT
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            e.department_id AS emp_dept_id,
            d.department_name,
            d.location AS dept_location
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.department_id = d.department_id
        ORDER BY d.department_name NULLS LAST, e.last_name;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='LEFT JOIN: All Employees (NULLs = no matching department)')
    # Visualise matched vs unmatched
    matched   = _result['department_name'].notna().sum()
    unmatched = _result['department_name'].isna().sum()
    match_summary_bar(matched, unmatched,
                      title='LEFT JOIN — Employees: Matched vs Unmatched Departments')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 12 — Find employees with NO matching department

    > **Key pattern:** `WHERE d.department_id IS NULL`
    > This filters to only the rows where the RIGHT table had no match.
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            e.job_title,
            e.department_id AS unknown_dept_id,
            e.salary
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.department_id = d.department_id
        WHERE d.department_id IS NULL;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Employees Whose department_id Does NOT Exist in departments Table')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 13 — Avg salary including unassigned employees
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            COALESCE(d.department_name, 'Unknown / Unassigned') AS department,
            COUNT(e.employee_id) AS num_employees,
            ROUND(AVG(e.salary),0) AS avg_salary
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.department_id = d.department_id
        GROUP BY COALESCE(d.department_name, 'Unknown / Unassigned')
        ORDER BY avg_salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Average Salary per Department (incl. Unassigned) — LEFT JOIN')
    bar_chart(_result, x='department', y='avg_salary',
              title='Avg Salary by Department (LEFT JOIN includes Unassigned)',
              horizontal=True, figsize=(10, 6))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 14 — Employee city vs department location (match check)
    """)
    return


@app.cell
def _(con, pie_chart, show_df):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS full_name,
            e.city AS employee_city,
            COALESCE(d.location,'—') AS dept_location,
            CASE WHEN d.location IS NULL THEN 'No Dept Found' WHEN e.city = d.location THEN '✅ Same City' ELSE '🚗 Different City' END AS city_match
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.department_id = d.department_id
        ORDER BY city_match, e.last_name;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Employee City vs Department HQ City (LEFT JOIN)')
    _summary = _result['city_match'].value_counts().reset_index()
    _summary.columns = ['city_match', 'count']
    pie_chart(_summary, labels='city_match', values='count',
              title='City Match Distribution (Employee vs Dept Location)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 15 — Total payroll by dept, including unassigned
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            COALESCE(d.department_name, 'Unknown') AS department,
            SUM(e.salary) AS total_payroll,
            COUNT(e.employee_id) AS headcount
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.department_id = d.department_id
        GROUP BY COALESCE(d.department_name, 'Unknown')
        ORDER BY total_payroll DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Total Payroll & Headcount per Department (LEFT JOIN)')
    bar_chart(_result, x='department', y='total_payroll',
              title='Total Payroll by Department (LEFT JOIN)',
              horizontal=True, figsize=(10, 6))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🟢 Section 6 — RIGHT JOIN

    ---
    ### 📘 What is a RIGHT JOIN?

    ```
    A RIGHT JOIN returns ALL rows from the RIGHT (second) table.
    For each right-table row, it tries to find matching rows in the left table.
      • If a match IS found  → left-table columns are included.
      • If NO match is found → left-table columns are filled with NULL.
    ```

    **In our case:**
    - The **right** table is `departments`
    - ALL 9 departments appear in the result
    - Departments with no employees (Legal=80, Customer Success=90)
      will have `NULL` for every employee column

    **Syntax:**
    ```sql
    SELECT ...
    FROM   employees  AS e
    RIGHT JOIN departments AS d  ON e.department_id = d.department_id
    ```

    > 💡 A RIGHT JOIN is just a mirrored LEFT JOIN.
    > `A RIGHT JOIN B` gives the same result as `B LEFT JOIN A`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 16 — ALL departments, NULLs where no employees (RIGHT JOIN)
    """)
    return


@app.cell
def _(con, match_summary_bar, show_df):
    _sql = """
        SELECT
            d.department_id,
            d.department_name,
            d.location,
            d.budget,
            e.first_name || ' ' || e.last_name AS employee_name,
            e.job_title
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.department_id = d.department_id
        ORDER BY d.department_name, e.last_name NULLS LAST;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='RIGHT JOIN: All Departments (NULLs = no employees)')
    matched_d   = _result['employee_name'].notna().sum()
    unmatched_d = _result['employee_name'].isna().sum()
    match_summary_bar(matched_d, unmatched_d,
                      label_matched='Depts With Employees',
                      label_unmatched='Depts With NO Employees',
                      title='RIGHT JOIN — Departments: Staffed vs Unstaffed')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 17 — Find departments with NO employees

    > **Key pattern:** `WHERE e.employee_id IS NULL`
    > After a RIGHT JOIN, employee columns are NULL for departments with no staff.
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT
            d.department_id,
            d.department_name,
            d.location,
            d.budget,
            d.manager_name
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.department_id = d.department_id
        WHERE e.employee_id IS NULL;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Departments That Have NO Employees Assigned')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 18 — Headcount per department (0 for empty depts)
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            d.department_name,
            d.location,
            COUNT(e.employee_id) AS num_employees
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.department_id = d.department_id
        GROUP BY d.department_name, d.location
        ORDER BY num_employees DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='All Departments with Employee Count (0 = no staff)')
    bar_chart(_result, x='department_name', y='num_employees',
              title='Employee Count per Department (RIGHT JOIN — includes empty depts)',
              xlabel='Department', ylabel='Employees',
              color='#55A868')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 19 — Budget efficiency: budget per employee
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            d.department_name,
            d.budget,
            COUNT(e.employee_id) AS num_employees,
            CASE WHEN COUNT(e.employee_id) = 0 THEN NULL ELSE ROUND(d.budget * 1.0 / COUNT(e.employee_id), 0) END AS budget_per_employee
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.department_id = d.department_id
        GROUP BY d.department_name, d.budget
        ORDER BY budget_per_employee DESC NULLS LAST;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Budget per Employee by Department (RIGHT JOIN)')
    # Filter to departments that have employees for the chart
    chart_df = _result[_result['num_employees'] > 0]
    bar_chart(chart_df, x='department_name', y='budget_per_employee',
              title='Budget Allocated per Employee (Staffed Departments)',
              horizontal=True, figsize=(10, 5))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 20 — Summarise all three joins side by side
    """)
    return


@app.cell
def _(bar_chart, con, pd, show_df):
    inner_count = con.execute("""
        SELECT COUNT(*)
        FROM employees e
        INNER
        JOIN departments d ON e.department_id = d.department_id;
    """).fetchone()[0]

    left_count = con.execute("""
        SELECT COUNT(*)
        FROM employees e
        LEFT
        JOIN departments d ON e.department_id = d.department_id;
    """).fetchone()[0]

    right_count = con.execute("""
        SELECT COUNT(*)
        FROM employees e
        RIGHT
        JOIN departments d ON e.department_id = d.department_id;
    """).fetchone()[0]

    _summary = pd.DataFrame({
        'join_type':  ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN'],
        'row_count':  [inner_count, left_count, right_count],
        'description': [
            'Only matched rows',
            'All employees (incl. unmatched)',
            'All departments (incl. empty)'
        ]
    })
    show_df(_summary, title='Row Count Comparison: INNER vs LEFT vs RIGHT JOIN')
    bar_chart(_summary, x='join_type', y='row_count',
              title='Number of Rows Returned by Each JOIN Type',
              xlabel='JOIN Type', ylabel='Row Count',
              color='#8172B3')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 21 — Complete employee roster with COALESCE (LEFT JOIN + friendly NULLs)
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            e.job_title,
            e.salary,
            COALESCE(d.department_name, 'UNASSIGNED') AS department,
            COALESCE(d.location, 'Unknown') AS dept_location,
            COALESCE(d.manager_name, 'No Manager') AS manager,
            COALESCE(CAST(d.budget AS VARCHAR), 'N/A') AS dept_budget
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.department_id = d.department_id
        ORDER BY department, e.salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Complete Employee Roster (NULL → Friendly Labels via COALESCE)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 22 — Salary range per department (LEFT JOIN + GROUP BY)
    """)
    return


@app.cell
def _(con, grouped_bar, show_df):
    _sql = """
        SELECT
            COALESCE(d.department_name, 'Unassigned') AS department,
            COUNT(e.employee_id) AS headcount,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary,
            ROUND(AVG(e.salary), 0) AS avg_salary
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.department_id = d.department_id
        GROUP BY COALESCE(d.department_name, 'Unassigned')
        ORDER BY avg_salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Salary Range per Department (LEFT JOIN)')
    grouped_bar(_result, x='department',
                y_cols=['min_salary', 'avg_salary', 'max_salary'],
                title='Salary Range (Min / Avg / Max) by Department',
                ylabel='Salary ($)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 23 — Employees per department, with dept location (RIGHT JOIN)
    """)
    return


@app.cell
def _(con, scatter_chart, show_df):
    _sql = """
        SELECT
            d.location,
            d.department_name,
            COUNT(e.employee_id) AS num_employees,
            COALESCE(SUM(e.salary), 0) AS total_payroll
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.department_id = d.department_id
        GROUP BY d.location, d.department_name
        ORDER BY d.location, total_payroll DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Departments: Location, Headcount & Payroll (RIGHT JOIN)')
    scatter_chart(_result, x='num_employees', y='total_payroll',
                  title='Dept Headcount vs Total Payroll',
                  color_col='location', label_col='department_name')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 24 — Most recent hire per department (RIGHT JOIN)
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT
            d.department_name,
            MAX(e.hire_date) AS latest_hire_date,
            COUNT(e.employee_id) AS total_employees
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY latest_hire_date DESC NULLS LAST;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Most Recent Hire Date per Department (RIGHT JOIN)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 25 — Final audit: all employees + all departments in one view
    """)
    return


@app.cell
def _(con, pd, show_df):
    # ── Show a side-by-side summary of what each JOIN keeps and drops ─────────

    left_nulls  = con.execute("""
        SELECT COUNT(*)
        FROM employees e
        LEFT
        JOIN departments d ON e.department_id = d.department_id
        WHERE d.department_id IS NULL;
    """).fetchone()[0]

    right_nulls = con.execute("""
        SELECT COUNT(*)
        FROM employees e
        RIGHT
        JOIN departments d ON e.department_id = d.department_id
        WHERE e.employee_id IS NULL;
    """).fetchone()[0]

    audit = pd.DataFrame({
        'JOIN Type':             ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN'],
        'Rows in Result':        [23, 25, 25],
        'Employees Dropped':     [2,   0,  2],
        'Departments Dropped':   [2,   2,  0],
        'NULL Rows (unmatched)': [0, left_nulls, right_nulls],
    })
    show_df(audit, title='Final Audit: What Each JOIN Includes / Excludes')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🎓 Summary & Key Takeaways

    Congratulations — you have completed JOIN 101! Here's a quick cheat sheet:

    ---
    ### JOIN Cheat Sheet

    ```sql
    -- INNER JOIN: only matched rows
    SELECT ... FROM employees e
    INNER JOIN departments d ON e.department_id = d.department_id

    -- LEFT JOIN: all employees, NULLs for unmatched departments
    SELECT ... FROM employees e
    LEFT JOIN departments d ON e.department_id = d.department_id

    -- RIGHT JOIN: all departments, NULLs for unmatched employees
    SELECT ... FROM employees e
    RIGHT JOIN departments d ON e.department_id = d.department_id
    ```

    ---
    ### When to use which JOIN?

    | You want to... | Use |
    |----------------|-----|
    | Only see records that exist in **both** tables | `INNER JOIN` |
    | Keep **all records from the left** table | `LEFT JOIN` |
    | Keep **all records from the right** table | `RIGHT JOIN` |
    | Find **unmatched** records (orphans) | `LEFT/RIGHT JOIN` + `WHERE ... IS NULL` |
    | Replace NULLs with friendly text | `COALESCE(col, 'default')` |

    ---
    > 🚀 **Next up:** FULL OUTER JOIN, CROSS JOIN, and self-joins!
    """)
    return


if __name__ == "__main__":
    app.run()
