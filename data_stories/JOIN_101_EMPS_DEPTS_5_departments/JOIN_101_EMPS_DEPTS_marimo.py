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
    ### A Hands-On Introduction to SQL JOINs with DuckDB
    ---
    > **Course:** OMIS 105 · Data Stories  
    > **Topic:** Relational Joins — INNER JOIN · LEFT JOIN · RIGHT JOIN  
    > **Tools:** Python · DuckDB · Pandas · Matplotlib  

    ---
    ## 📚 What You Will Learn

    By the end of this notebook you will be able to:

    1. **Explain** what a JOIN is and *why* it is needed
    2. **Distinguish** between INNER, LEFT, and RIGHT JOINs
    3. **Write** SQL that combines two tables using a shared key (`dept_id`)
    4. **Interpret** NULL values that appear after LEFT / RIGHT JOINs
    5. **Visualise** join results with meaningful charts

    ---
    ## 📂 Our Two Tables

    ### `employees` (12 rows)
    | Column | Type | Description |
    |--------|------|-------------|
    | `emp_id` | integer | Unique employee ID |
    | `emp_name` | text | Employee first name |
    | `dept_id` | integer | Department the employee belongs to |
    | `salary` | integer | Annual salary in USD |
    | `gender` | text | MALE / FEMALE |

    ### `departments` (5 rows)
    | Column | Type | Description |
    |--------|------|-------------|
    | `dept_id` | integer | Unique department ID |
    | `dept_name` | text | Department name |
    | `dept_location` | text | City, State |
    | `budget` | integer | Annual budget in USD |

    ---
    ## ⚠️ Intentional Mismatches (this is what makes JOINs interesting!)

    | Situation | Who | Effect |
    |-----------|-----|--------|
    | Employees with **unknown** `dept_id` | Mary (80), Barbara (90) | Dropped by INNER JOIN; NULLs in LEFT JOIN |
    | Departments with **no employees** | MARKETING (40), HARDWARE (50) | Dropped by INNER JOIN; NULLs in RIGHT JOIN |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ⚙️ Section 0 — Setup

    Run this cell first every time. It imports libraries, loads the helper
    utilities, and opens a DuckDB connection.

    > **DuckDB** is a fast, in-process SQL engine that runs entirely inside
    > this notebook — no server or installation needed beyond `pip install duckdb`.
    """)
    return


@app.cell
def _():
    import sys, os
    import duckdb
    import pandas as pd

    # Add notebook folder to path so Python can find notebook_utils.py
    sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))

    # Import all display and plotting helpers
    # (No plotting code will appear anywhere else in this notebook)
    from notebook_utils import (
        show_df, bar_chart, pie_chart, grouped_bar,
        scatter_chart, draw_join_venn, match_summary_bar
    )

    print('✅ Libraries loaded!')

    return (bar_chart, draw_join_venn, duckdb, grouped_bar, match_summary_bar, os, pd, pie_chart, scatter_chart, show_df)


@app.cell
def _(duckdb, os):
    # Open an in-memory DuckDB connection
    con = duckdb.connect()

    # Point to the data files
    # Adjust BASE if you move the notebook to a different folder
    BASE     = os.path.dirname(os.path.abspath('__file__'))
    EMP_CSV  = os.path.join(BASE, 'data2', 'employees.csv')
    DEPT_CSV = os.path.join(BASE, 'data2', 'departments.csv')

    print('📁 employees  :', EMP_CSV)
    print('📁 departments:', DEPT_CSV)

    return (DEPT_CSV, EMP_CSV, con)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🏗️ Section 1 — Create Tables

    `DROP TABLE IF EXISTS` ensures this notebook is **idempotent** —
    you can run every cell from top to bottom as many times as you like
    without errors.
    """)
    return


@app.cell
def _(DEPT_CSV, EMP_CSV, con):
    # Drop and recreate both tables from CSV files
    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)
    con.execute("""
        DROP TABLE IF EXISTS departments;
    """)

    con.execute(f"""
        CREATE TABLE employees AS
        SELECT * FROM read_csv_auto('{EMP_CSV}', header=true)
    """)

    con.execute(f"""
        CREATE TABLE departments AS
        SELECT * FROM read_csv_auto('{DEPT_CSV}', header=true)
    """)

    e_count = con.execute("""
        SELECT COUNT(*)
        FROM employees;
    """).fetchone()[0]
    d_count = con.execute("""
        SELECT COUNT(*)
        FROM departments;
    """).fetchone()[0]
    print(f'✅ employees  : {e_count} rows')
    print(f'✅ departments: {d_count} rows')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 👀 Preview — employees table
    """)
    return


@app.cell
def _(con, show_df):
    _result = con.execute("""
        SELECT *
        FROM employees;
    """).df()
    show_df(_result, title='employees — all 12 rows')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 👀 Preview — departments table
    """)
    return


@app.cell
def _(con, show_df):
    _result = con.execute("""
        SELECT *
        FROM departments;
    """).df()
    show_df(_result, title='departments — all 5 rows')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Section 2 — 5 Basic Queries (Single Table)

    Before combining tables, let's warm up with queries on one table at a time.

    | Clause | What it does |
    |--------|-------------|
    | `SELECT` | Chooses which columns to return |
    | `FROM` | Names the table to read |
    | `WHERE` | Filters rows by a condition |
    | `GROUP BY` | Collapses rows that share a value into one summary row |
    | `ORDER BY` | Sorts the result |
    | `LIMIT` | Returns at most *n* rows |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Basic Query 1 — View all employees, sorted by salary (highest first)
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            dept_id,
            salary,
            gender
        FROM employees
        ORDER BY salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='All Employees Sorted by Salary (Descending)')
    bar_chart(_result, x='emp_name', y='salary',
              title='Employee Salaries (Highest → Lowest)',
              xlabel='Employee', ylabel='Salary ($)', color='#4C72B0')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Basic Query 2 — Top 5 highest-paid employees
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        ORDER BY salary DESC
        LIMIT 5;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Top 5 Highest-Paid Employees')
    bar_chart(_result, x='emp_name', y='salary',
              title='Top 5 Salaries', xlabel='Employee', ylabel='Salary ($)',
              color='#C44E52')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Basic Query 3 — Female employees only (WHERE)
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            dept_id,
            salary
        FROM employees
        WHERE gender = 'FEMALE'
        ORDER BY salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Female Employees')
    bar_chart(_result, x='emp_name', y='salary',
              title='Female Employee Salaries',
              xlabel='Employee', ylabel='Salary ($)', color='#DA8BC3')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Basic Query 4 — Headcount and average salary per dept_id (GROUP BY)
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            dept_id,
            COUNT(*) AS num_employees,
            AVG(salary) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY dept_id
        ORDER BY num_employees DESC;
    """
    _result = con.execute(_sql).df()
    _result['avg_salary'] = _result['avg_salary'].round(0).astype(int)
    show_df(_result, title='Employee Stats per dept_id')
    bar_chart(_result, x='dept_id', y='avg_salary',
              title='Average Salary per dept_id',
              xlabel='dept_id', ylabel='Avg Salary ($)', color='#55A868')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Basic Query 5 — Gender split in the company (GROUP BY + pie chart)
    """)
    return


@app.cell
def _(con, pie_chart, show_df):
    _sql = """
        SELECT
            gender,
            COUNT(*) AS headcount
        FROM employees
        GROUP BY gender;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Gender Headcount')
    pie_chart(_result, labels='gender', values='headcount',
              title='Gender Distribution — All Employees')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🔗 Section 3 — What IS a JOIN?

    ### The Problem

    Our `employees` table stores each person's `dept_id` (a number), but it does
    **not** store the department name, location, or budget.
    That information lives in the `departments` table.

    ```
    employees                      departments
    ──────────────────────         ──────────────────────────────────
    emp_id │ emp_name │ dept_id    dept_id │ dept_name │ dept_location │ budget
    ───────┼──────────┼────────    ────────┼───────────┼───────────────┼───────
       100 │ Alex     │  10    ←──     10  │ SALES     │ Sunnyvale CA  │ 4000000
       300 │ Rafa     │  20    ←──     20  │ BUSINESS  │ Dallas TX     │ 3000000
    ```

    A **JOIN** lets us stitch the two tables together using the shared column
    `dept_id`, so we can answer questions like:

    - *What department does Alex work in?*
    - *Which employees work in the AI department?*
    - *What is the total payroll for the BUSINESS department?*

    ---
    ### The Linking Key

    ```
    employees.dept_id  ←──────→  departments.dept_id
    ```

    When `employees.dept_id = departments.dept_id`, the rows "match".

    ---
    ### Our Mismatches (intentional!)

    | employees side | departments side |
    |----------------|-----------------|
    | Mary has `dept_id = 80` | dept 80 does NOT exist in departments |
    | Barbara has `dept_id = 90` | dept 90 does NOT exist in departments |
    | *(all employees matched)* | MARKETING (40) has NO employees |
    | *(all employees matched)* | HARDWARE (50) has NO employees |

    These gaps produce different results depending on which JOIN you use.

    ---
    ### The Three JOINs

    | JOIN | Rows returned |
    |------|--------------|
    | **INNER JOIN** | Only rows where `dept_id` exists in **both** tables |
    | **LEFT JOIN** | All rows from `employees` + matching dept info (NULL if no dept found) |
    | **RIGHT JOIN** | All rows from `departments` + matching employees (NULL if no employees) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Venn diagram — INNER JOIN
    """)
    return


@app.cell
def _(draw_join_venn):
    draw_join_venn('inner')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🟡 Venn diagram — LEFT JOIN
    """)
    return


@app.cell
def _(draw_join_venn):
    draw_join_venn('left')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🟢 Venn diagram — RIGHT JOIN
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
    ## 🔵 Section 4 — INNER JOIN

    ### 📘 Definition

    ```
    INNER JOIN returns ONLY rows where the join key (dept_id) matches
    in BOTH the employees table AND the departments table.

    Employees with dept_id 80 or 90 → EXCLUDED (no match in departments)
    Departments 40 (MARKETING) and 50 (HARDWARE) → EXCLUDED (no employees)
    ```

    **General syntax:**
    ```sql
    SELECT  columns
    FROM    employees     AS e
    INNER JOIN departments AS d  ON e.dept_id = d.dept_id
    ```

    > 💡 `AS e` and `AS d` are **table aliases** — short nicknames.
    > Instead of writing `employees.salary` we write `e.salary`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 1 — Every matched employee with their department name
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT
            e.emp_id,
            e.emp_name,
            e.gender,
            e.salary,
            d.dept_name,
            d.dept_location
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name, e.salary DESC;
    """
    result = con.execute(_sql).df()
    show_df(result, title='INNER JOIN: All Matched Employees with Department Info')
    print(f'Rows: {len(result)}  (12 employees − 2 unmatched = 10)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 2 — Headcount and average salary per department
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            d.dept_name,
            d.dept_location,
            COUNT(e.emp_id) AS num_employees,
            ROUND(AVG(e.salary), 0) AS avg_salary
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name, d.dept_location
        ORDER BY avg_salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Headcount & Average Salary per Department (INNER JOIN)')
    bar_chart(_result, x='dept_name', y='avg_salary',
              title='Average Salary by Department (INNER JOIN)',
              xlabel='Department', ylabel='Avg Salary ($)', color='#4C72B0')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 3 — Total payroll vs. budget per department
    """)
    return


@app.cell
def _(con, grouped_bar, show_df):
    _sql = """
        SELECT
            d.dept_name,
            d.budget,
            SUM(e.salary) AS total_payroll,
            d.budget - SUM(e.salary) AS budget_remaining
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name, d.budget
        ORDER BY budget_remaining DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Budget vs Total Payroll per Department (INNER JOIN)')
    grouped_bar(_result, x='dept_name',
                y_cols=['budget', 'total_payroll'],
                title='Department Budget vs Total Payroll',
                ylabel='Amount ($)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 4 — Female employees and their department
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            e.emp_name,
            e.salary,
            d.dept_name,
            d.dept_location
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        WHERE e.gender = 'FEMALE'
        ORDER BY e.salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Female Employees with Department (INNER JOIN)')
    bar_chart(_result, x='emp_name', y='salary',
              title='Female Employee Salaries by Department',
              horizontal=True, color='#DA8BC3')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 5 — Employees earning above $150,000 with dept info
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            e.emp_name,
            e.salary,
            e.gender,
            d.dept_name,
            d.dept_location
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        WHERE e.salary > 150000
        ORDER BY e.salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='High Earners (> $150k) with Department Info')
    bar_chart(_result, x='emp_name', y='salary',
              title='Employees Earning > $150,000',
              xlabel='Employee', ylabel='Salary ($)', color='#C44E52')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 6 — Gender breakdown per department (INNER JOIN)
    """)
    return


@app.cell
def _(con, grouped_bar, show_df):
    _sql = """
        SELECT
            d.dept_name,
            e.gender,
            COUNT(*) AS headcount,
            SUM(e.salary) AS total_salary
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name, e.gender
        ORDER BY d.dept_name, e.gender;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Gender Breakdown per Department (INNER JOIN)')
    # Pivot for grouped bar
    pivot = _result.pivot(index='dept_name', columns='gender', values='headcount').fillna(0).reset_index()
    pivot.columns.name = None
    grouped_bar(pivot, x='dept_name',
                y_cols=[c for c in pivot.columns if c != 'dept_name'],
                title='Male vs Female Headcount per Department',
                ylabel='Headcount')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 7 — Salary scatter: employee vs. dept budget (INNER JOIN)
    """)
    return


@app.cell
def _(con, scatter_chart, show_df):
    _sql = """
        SELECT
            e.emp_name,
            e.salary,
            d.budget,
            d.dept_name
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Employee Salary vs. Department Budget')
    scatter_chart(_result, x='budget', y='salary',
                  title='Individual Salary vs Dept Budget',
                  color_col='dept_name', label_col='emp_name')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 8 — Highest-paid employee in each department (QUALIFY)
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            d.dept_name,
            e.emp_name,
            e.gender,
            e.salary
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id QUALIFY e.salary = MAX(e.salary) OVER (PARTITION BY d.dept_id)
        ORDER BY e.salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Highest-Paid Employee in Each Department')
    bar_chart(_result, x='dept_name', y='salary',
              title='Top Earner per Department',
              xlabel='Department', ylabel='Salary ($)', color='#8172B3')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🟡 Section 5 — LEFT JOIN

    ### 📘 Definition

    ```
    A LEFT JOIN returns ALL rows from the LEFT table (employees).

      • If a matching dept_id IS found in departments
          → department columns are filled in normally.
      • If NO matching dept_id is found
          → every department column is filled with NULL.
    ```

    **Key fact for our data:**
    ALL 12 employees appear in the result.
    Mary (dept 80) and Barbara (dept 90) will have NULL for dept_name,
    dept_location, and budget because those department IDs don't exist.

    ```sql
    SELECT  columns
    FROM    employees     AS e
    LEFT JOIN departments  AS d  ON e.dept_id = d.dept_id
    ```

    > 💡 The word **LEFT** refers to the table written on the LEFT side of the JOIN.
    > That table is always kept in full.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 9 — ALL employees, NULLs where dept is unknown (LEFT JOIN)
    """)
    return


@app.cell
def _(con, match_summary_bar, show_df):
    _sql = """
        SELECT
            e.emp_id,
            e.emp_name,
            e.dept_id,
            e.salary,
            e.gender,
            d.dept_name,
            d.dept_location
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name NULLS LAST, e.salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='LEFT JOIN: All 12 Employees (NULL = no matching department)')
    # Show matched vs unmatched
    matched   = _result['dept_name'].notna().sum()
    unmatched = _result['dept_name'].isna().sum()
    match_summary_bar(matched, unmatched,
                      title='LEFT JOIN — Employees: Matched vs Unmatched Dept')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 10 — Find employees with NO matching department

    > **Pattern:** after a LEFT JOIN, filter `WHERE d.dept_id IS NULL`
    > to isolate the rows that had no match on the right side.
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT
            e.emp_id,
            e.emp_name,
            e.dept_id AS unknown_dept_id,
            e.salary,
            e.gender
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.dept_id = d.dept_id
        WHERE d.dept_id IS NULL;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Employees Whose dept_id Has No Match in departments Table')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 11 — Avg salary per dept including unassigned (COALESCE)
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            COALESCE(d.dept_name, 'UNASSIGNED') AS department,
            COUNT(e.emp_id) AS headcount,
            ROUND(AVG(e.salary), 0) AS avg_salary
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY COALESCE(d.dept_name, 'UNASSIGNED')
        ORDER BY avg_salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Avg Salary per Department — incl. Unassigned (LEFT JOIN)')
    bar_chart(_result, x='department', y='avg_salary',
              title='Avg Salary by Dept (UNASSIGNED = no dept found)',
              horizontal=True, color='#DD8452')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 12 — Full employee roster with friendly NULLs (COALESCE)
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT
            e.emp_id,
            e.emp_name,
            e.gender,
            e.salary,
            COALESCE(d.dept_name, 'UNKNOWN') AS dept_name,
            COALESCE(d.dept_location, 'UNKNOWN') AS dept_location,
            COALESCE( CAST(d.budget AS VARCHAR), 'N/A' ) AS budget
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.dept_id = d.dept_id
        ORDER BY dept_name, e.salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Complete Employee Roster — NULLs replaced via COALESCE (LEFT JOIN)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🟢 Section 6 — RIGHT JOIN

    ### 📘 Definition

    ```
    A RIGHT JOIN returns ALL rows from the RIGHT table (departments).

      • If matching employees exist     → employee columns are filled in.
      • If NO employees match a dept    → every employee column is NULL.
    ```

    **Key fact for our data:**
    ALL 5 departments appear in the result.
    MARKETING (40) and HARDWARE (50) have no employees, so their
    emp_id, emp_name, salary, and gender columns will be NULL.
    Mary and Barbara are excluded because their dept_ids (80, 90)
    do not exist in the departments table.

    ```sql
    SELECT  columns
    FROM    employees     AS e
    RIGHT JOIN departments AS d  ON e.dept_id = d.dept_id
    ```

    > 💡 `A RIGHT JOIN B` is equivalent to `B LEFT JOIN A`.
    > The RIGHT table is always kept in full.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 13 — ALL departments, NULLs where no employees (RIGHT JOIN)
    """)
    return


@app.cell
def _(con, match_summary_bar, show_df):
    _sql = """
        SELECT
            d.dept_id,
            d.dept_name,
            d.dept_location,
            d.budget,
            e.emp_id,
            e.emp_name,
            e.salary,
            e.gender
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name, e.salary DESC NULLS LAST;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='RIGHT JOIN: All 5 Departments (NULL rows = no employees)')
    staffed   = _result['emp_id'].notna().sum()
    unstaffed = _result['emp_id'].isna().sum()
    match_summary_bar(staffed, unstaffed,
                      label_matched='Dept rows WITH employees',
                      label_unmatched='Dept rows with NO employees',
                      title='RIGHT JOIN — Staffed vs Empty Department Rows')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 14 — Departments with no employees (RIGHT JOIN + IS NULL)
    """)
    return


@app.cell
def _(con, show_df):
    _sql = """
        SELECT
            d.dept_id,
            d.dept_name,
            d.dept_location,
            d.budget
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.dept_id = d.dept_id
        WHERE e.emp_id IS NULL;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Departments That Have NO Employees Assigned')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 15 — Headcount per department including empty ones (RIGHT JOIN)
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            d.dept_name,
            d.dept_location,
            d.budget,
            COUNT(e.emp_id) AS num_employees,
            COALESCE(SUM(e.salary), 0) AS total_payroll
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name, d.dept_location, d.budget
        ORDER BY num_employees DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='All Departments: Headcount & Payroll (empty depts show 0)')
    bar_chart(_result, x='dept_name', y='num_employees',
              title='Employee Count per Department (RIGHT JOIN — 0 = no staff)',
              xlabel='Department', ylabel='Employees', color='#55A868')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Section 7 — Side-by-Side Comparison of All Three JOINs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 16 — Row counts for INNER vs LEFT vs RIGHT JOIN
    """)
    return


@app.cell
def _(bar_chart, con, pd, show_df):
    inner_n = con.execute("""
        SELECT COUNT(*)
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id;
    """).fetchone()[0]

    left_n = con.execute("""
        SELECT COUNT(*)
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id;
    """).fetchone()[0]

    right_n = con.execute("""
        SELECT COUNT(*)
        FROM employees e
        RIGHT
        JOIN departments d ON e.dept_id = d.dept_id;
    """).fetchone()[0]

    summary = pd.DataFrame({
        'join_type':        ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN'],
        'rows_returned':    [inner_n, left_n, right_n],
        'all_employees':    ['Only matched (10)', 'All 12 ✅', 'Only matched (10)'],
        'all_departments':  ['Only matched (3)', 'Only matched (3)', 'All 5 ✅'],
    })
    show_df(summary, title='Row Count Comparison: INNER vs LEFT vs RIGHT JOIN')
    bar_chart(summary, x='join_type', y='rows_returned',
              title='Rows Returned by Each JOIN Type',
              xlabel='JOIN Type', ylabel='Rows', color='#8172B3')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 17 — Avg salary by dept for all three JOIN types in one view
    """)
    return


@app.cell
def _(con, show_df):
    inner_df = con.execute("""
        SELECT
            d.dept_name,
            ROUND(AVG(e.salary),0) AS avg_salary_inner
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name;
    """).df()

    left_df = con.execute("""
        SELECT
            COALESCE(d.dept_name,'UNASSIGNED') AS dept_name,
            ROUND(AVG(e.salary),0) AS avg_salary_left
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY COALESCE(d.dept_name,'UNASSIGNED');
    """).df()

    right_df = con.execute("""
        SELECT
            d.dept_name,
            ROUND(AVG(e.salary),0) AS avg_salary_right
        FROM employees e
        RIGHT
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name;
    """).df()

    merged = (inner_df
        .merge(left_df,  on='dept_name', how='outer')
        .merge(right_df, on='dept_name', how='outer')
        .sort_values('dept_name')
        .reset_index(drop=True))

    show_df(merged, title='Avg Salary per Dept — INNER vs LEFT vs RIGHT (NULL = dept not in result)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🔍 Section 8 — Three More Useful JOIN Queries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 18 — Salary range per department (LEFT JOIN + GROUP BY)
    """)
    return


@app.cell
def _(con, grouped_bar, show_df):
    _sql = """
        SELECT
            COALESCE(d.dept_name, 'UNASSIGNED') AS department,
            COUNT(e.emp_id) AS headcount,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary,
            ROUND(AVG(e.salary), 0) AS avg_salary
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY COALESCE(d.dept_name, 'UNASSIGNED')
        ORDER BY avg_salary DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Salary Range per Department (LEFT JOIN)')
    grouped_bar(_result, x='department',
                y_cols=['min_salary', 'avg_salary', 'max_salary'],
                title='Min / Avg / Max Salary per Department',
                ylabel='Salary ($)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 19 — Budget utilisation: payroll as % of budget (INNER JOIN)
    """)
    return


@app.cell
def _(bar_chart, con, show_df):
    _sql = """
        SELECT
            d.dept_name,
            d.budget,
            SUM(e.salary) AS total_payroll,
            ROUND(SUM(e.salary) * 100.0 / d.budget, 1) AS payroll_pct_of_budget
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name, d.budget
        ORDER BY payroll_pct_of_budget DESC;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Payroll as % of Department Budget (INNER JOIN)')
    bar_chart(_result, x='dept_name', y='payroll_pct_of_budget',
              title='Payroll as % of Budget per Department',
              xlabel='Department', ylabel='Payroll / Budget (%)', color='#937860')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔗 Join Query 20 — Gender pay gap per department (INNER JOIN + CASE)
    """)
    return


@app.cell
def _(con, grouped_bar, show_df):
    _sql = """
        SELECT
            d.dept_name,
            ROUND(AVG(CASE WHEN e.gender = 'MALE' THEN e.salary END), 0) AS avg_male_salary,
            ROUND(AVG(CASE WHEN e.gender = 'FEMALE' THEN e.salary END), 0) AS avg_female_salary
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        HAVING AVG(CASE WHEN e.gender = 'MALE' THEN e.salary END) IS NOT NULL
        AND AVG(CASE WHEN e.gender = 'FEMALE' THEN e.salary END) IS NOT NULL
        ORDER BY d.dept_name;
    """
    _result = con.execute(_sql).df()
    show_df(_result, title='Average Male vs Female Salary per Department (INNER JOIN)')
    grouped_bar(_result, x='dept_name',
                y_cols=['avg_male_salary', 'avg_female_salary'],
                title='Male vs Female Average Salary per Department',
                ylabel='Avg Salary ($)')

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🎓 Summary & SQL Cheat Sheet

    Congratulations — you have completed **JOIN 101**!

    ---
    ### SQL Cheat Sheet

    ```sql
    -- ─────────────────────────────────────────────
    -- INNER JOIN  →  only matching rows from BOTH tables
    -- ─────────────────────────────────────────────
    SELECT e.emp_name, d.dept_name
    FROM   employees     AS e
    INNER JOIN departments AS d  ON e.dept_id = d.dept_id;

    -- ─────────────────────────────────────────────
    -- LEFT JOIN  →  ALL employees + matches from departments
    --              (NULL where no dept match found)
    -- ─────────────────────────────────────────────
    SELECT e.emp_name, d.dept_name
    FROM   employees     AS e
    LEFT JOIN departments  AS d  ON e.dept_id = d.dept_id;

    -- ─────────────────────────────────────────────
    -- RIGHT JOIN  →  ALL departments + matches from employees
    --               (NULL where no employee match found)
    -- ─────────────────────────────────────────────
    SELECT e.emp_name, d.dept_name
    FROM   employees     AS e
    RIGHT JOIN departments AS d  ON e.dept_id = d.dept_id;

    -- ─────────────────────────────────────────────
    -- Find UNMATCHED rows after a LEFT JOIN
    -- ─────────────────────────────────────────────
    SELECT e.*  FROM employees e
    LEFT JOIN departments d ON e.dept_id = d.dept_id
    WHERE d.dept_id IS NULL;

    -- ─────────────────────────────────────────────
    -- Replace NULLs with a friendly label
    -- ─────────────────────────────────────────────
    SELECT COALESCE(d.dept_name, 'UNASSIGNED') AS department
    FROM employees e
    LEFT JOIN departments d ON e.dept_id = d.dept_id;
    ```

    ---
    ### When to use which JOIN?

    | Goal | JOIN to use |
    |------|------------|
    | Only see records present in **both** tables | `INNER JOIN` |
    | Keep **every row from the left** table | `LEFT JOIN` |
    | Keep **every row from the right** table | `RIGHT JOIN` |
    | Find orphan / unmatched records | `LEFT` or `RIGHT JOIN` + `WHERE ... IS NULL` |
    | Show NULLs as readable text | `COALESCE(col, 'label')` |

    ---
    > 🚀 **Next topic:** FULL OUTER JOIN, CROSS JOIN, and self-joins!
    """)
    return


if __name__ == "__main__":
    app.run()
