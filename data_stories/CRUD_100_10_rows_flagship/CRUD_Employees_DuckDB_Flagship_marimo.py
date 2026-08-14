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
    # CRUD of Employees Data using Jupyter + DuckDB

    ## Flagship Notebook

    This notebook teaches **CRUD operations** using:

    - Jupyter Notebook
    - DuckDB
    - SQL
    - Employee data with avatar image URLs

    CRUD means:

    | Letter | Operation | SQL Concept |
    |---|---|---|
    | C | Create | `CREATE TABLE`, `INSERT` |
    | R | Read | `SELECT` |
    | U | Update | `UPDATE` |
    | D | Delete | `DELETE` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Notebook Design

    Each section includes:

    1. What we are doing
    2. SQL solution in clean multi-line format
    3. Result set displayed as a table with row numbers
    4. Rendered avatar images when `image_url` is present
    5. Meaningful plot when useful

    All display and plotting helper functions are stored outside this notebook in:

    ```text
    helper_functions.py
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 1 — Setup

    ### What we are doing

    We import DuckDB and helper functions.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import duckdb
    import pandas as pd

    from helper_functions import (
        show_note,
        pretty_sql,
        show_df,
        show_df_with_images,
        run_query,
        run_query_with_images,
        run_statement,
        plot_bar,
        plot_pie
    )

    BASE_DIR = Path(".")
    DATA_DIR = BASE_DIR / "data"
    return (BASE_DIR, DATA_DIR, duckdb, plot_bar, plot_pie, run_query, run_query_with_images, run_statement, show_note)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Create a Connection to DuckDB
    """)
    return


@app.cell
def _(duckdb, show_note):
    # Create a Connection to DuckDB
    con = duckdb.connect("employees_crud.duckdb")

    print("con=", con)
    show_note("✅ DuckDB environment ready.")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 2 — Verify Data Files

    ### What we are doing

    We verify that the CSV files exist.
    """)
    return


@app.cell
def _(BASE_DIR, DATA_DIR):
    print("Current folder:", BASE_DIR.resolve())
    print("Data folder:", DATA_DIR.resolve())
    print("employees.csv exists:", (DATA_DIR / "employees.csv").exists())
    print("employees_backup.csv exists:", (DATA_DIR / "employees_backup.csv").exists())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 1 — Create Tables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 3 — Make Notebook Re-runnable

    ### What we are doing

    We drop existing tables so this notebook can run repeatedly.
    """)
    return


@app.cell
def _(con, run_statement):
    _sql = """
        DROP TABLE IF EXISTS employees;
        DROP TABLE IF EXISTS employees_backup;
        DROP TABLE IF EXISTS employees_from_csv;
        DROP TABLE IF EXISTS department_salary_summary;
    """

    run_statement(
        con,
        _sql,
        "Existing tables removed if they existed."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 4 — Create employees Table

    ### What we are doing

    We create the main employees table.
    """)
    return


@app.cell
def _(con, run_statement):
    _sql = """
        CREATE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR,
            department VARCHAR,
            salary     INTEGER,
            gender     VARCHAR,
            image_url  VARCHAR
        );
    """

    run_statement(
        con,
        _sql,
        "employees table created."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 5 — Insert Exact Employee Records

    ### What we are doing

    We insert the exact 10 employee records.
    """)
    return


@app.cell
def _(con, run_statement):
    _sql = """
        INSERT INTO employees
        VALUES
            ( 100, 'Alex', 'SALES', 120000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Alex' ),
            ( 200, 'Jeff', 'SALES', 140000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Jeff' ),
            ( 300, 'Rafa', 'BUSINESS', 150000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Rafa' ),
            ( 400, 'Susan', 'SALES', 150000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Susan' ),
            ( 500, 'Jen', 'BUSINESS', 160000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Jen' ),
            ( 600, 'Barb', 'BUSINESS', 180000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Barb' ),
            ( 700, 'Dara', 'AI', 190000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Dara' ),
            ( 800, 'Venus', 'AI', 200000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Venus' ),
            ( 900, 'Margie', 'SALES', 140000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Margie' ),
            ( 910, 'Betty', 'SALES', 170000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Betty' );
    """

    run_statement(
        con,
        _sql,
        "10 employee records inserted."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 6 — Read employees with Raw URLs and Rendered Images

    ### What we are doing

    We first display exactly what is stored in DuckDB. Then we render the avatar images.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    _sql = '''
    SELECT
        emp_id,
        emp_name,
        department,
        salary,
        gender,
        image_url
    FROM employees
    ORDER BY emp_id;
    '''

    run_query_with_images(
        con,
        _sql,
        image_column="image_url",
        title="employees table"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 7 — Create employees_backup from CSV

    ### What we are doing

    We create `employees_backup` by reading a CSV file.
    """)
    return


@app.cell
def _(con, run_statement):
    _sql = """
        CREATE TABLE employees_backup AS
        SELECT *
        FROM read_csv_auto('data/employees_backup.csv');
    """

    run_statement(
        con,
        _sql,
        "employees_backup created from CSV."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 8 — Display employees_backup with Images
    """)
    return


@app.cell
def _(con, run_query_with_images):
    _sql = '''
    SELECT
        emp_id,
        emp_name,
        department,
        salary,
        gender,
        image_url
    FROM employees_backup
    ORDER BY emp_id;
    '''

    run_query_with_images(
        con,
        _sql,
        image_column="image_url",
        title="employees_backup table"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 9 — Create employees_from_csv
    """)
    return


@app.cell
def _(con, run_statement):
    _sql = """
        CREATE TABLE employees_from_csv AS
        SELECT *
        FROM read_csv_auto('data/employees.csv');
    """

    run_statement(
        con,
        _sql,
        "employees_from_csv created from CSV."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 10 — Compare Table Counts
    """)
    return


@app.cell
def _(con, run_query):
    _sql = """
        SELECT
            'employees' AS table_name,
            COUNT(*) AS row_count
        FROM employees
        UNION ALL
        SELECT
            'employees_backup' AS table_name,
            COUNT(*) AS row_count
        FROM employees_backup
        UNION ALL
        SELECT
            'employees_from_csv' AS table_name,
            COUNT(*) AS row_count
        FROM employees_from_csv;
    """

    run_query(
        con,
        _sql,
        "row counts"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 2 — Create Operations

    Create means adding new data or creating new database objects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C1 — Create a New Employee

    ### What we are doing

    Add Omar to the AI department.

    ### Before
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            ORDER BY emp_id;
        """,
        image_column="image_url",
        title="Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        """
            INSERT INTO employees
            VALUES ( 920, 'Omar', 'AI', 175000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Omar' );
        """,
        "Omar inserted."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_id = 920;
        """,
        image_column="image_url",
        title="After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C2 — Create Another Employee

    ### What we are doing

    Add Nina to the BUSINESS department.

    ### Before
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            ORDER BY emp_id;
        """,
        image_column="image_url",
        title="Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        """
            INSERT INTO employees
            VALUES ( 930, 'Nina', 'BUSINESS', 155000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Nina' );
        """,
        "Nina inserted."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_id = 930;
        """,
        image_column="image_url",
        title="After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C3 — Create by Copying from Backup

    ### What we are doing

    Copy Alex from backup using a new employee id.

    ### Before
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_name LIKE 'Alex%';
        """,
        image_column="image_url",
        title="Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        """
            INSERT INTO employees
            SELECT
                940,
                emp_name || '_COPY',
                department,
                salary,
                gender,
                image_url
            FROM employees_backup
            WHERE emp_id = 100;
        """,
        "Copied employee inserted."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_id = 940;
        """,
        image_column="image_url",
        title="After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C4 — Create a Summary Table

    ### What we are doing

    Create a department salary summary table.

    ### Before
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT *
            FROM employees
            ORDER BY emp_id;
        """,
        "Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        """
            CREATE TABLE department_salary_summary AS
            SELECT
                department,
                COUNT(*) AS employee_count,
                SUM(salary) AS total_salary,
                ROUND(AVG(salary), 2) AS avg_salary
            FROM employees
            GROUP BY department;
        """,
        "Summary table created."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT *
            FROM department_salary_summary
            ORDER BY department;
        """,
        "After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 3 — Read Operations

    Read means retrieving data using `SELECT`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## R1 — Read All Employees

    ### What we are doing

    Show all employees.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            ORDER BY emp_id;
        """,
        image_column="image_url",
        title="R1 — Read All Employees"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## R2 — Read Selected Columns

    ### What we are doing

    Show employee name, department, and salary.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        '''SELECT
        emp_name,
        department,
        salary
    FROM employees
    ORDER BY emp_name;''',
        "R2 — Read Selected Columns"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## R3 — Read with WHERE

    ### What we are doing

    Show AI employees.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        '''SELECT
        emp_id,
        emp_name,
        department,
        salary,
        gender,
        image_url
    FROM employees
    WHERE department = 'AI'
    ORDER BY salary DESC;''',
        image_column="image_url",
        title="R3 — Read with WHERE"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## R4 — Read with ORDER BY and LIMIT

    ### What we are doing

    Show top 5 highest-paid employees.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        '''SELECT
        emp_name,
        department,
        salary,
        image_url
    FROM employees
    ORDER BY salary DESC
    LIMIT 5;''',
        image_column="image_url",
        title="R4 — Read with ORDER BY and LIMIT"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## R5 — Read with GROUP BY

    ### What we are doing

    Show employee count per department.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT
                department,
                COUNT(*) AS employee_count
            FROM employees
            GROUP BY department
            ORDER BY employee_count DESC;
        """,
        "R5 — Read with GROUP BY"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 4 — Update Operations

    Update means changing existing rows. Always use `WHERE` when updating specific rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## U1 — Update One Salary

    ### What we are doing

    Give Alex a salary raise to 130000.

    ### Before
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_name = 'Alex';
        """,
        image_column="image_url",
        title="Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        '''UPDATE employees
    SET salary = 130000
    WHERE emp_name = 'Alex';''',
        "Alex salary updated."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_name = 'Alex';
        """,
        image_column="image_url",
        title="After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## U2 — Update One Department

    ### What we are doing

    Move Jeff from SALES to AI.

    ### Before
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_name = 'Jeff';
        """,
        image_column="image_url",
        title="Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        '''UPDATE employees
    SET department = 'AI'
    WHERE emp_name = 'Jeff';''',
        "Jeff department updated."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_name = 'Jeff';
        """,
        image_column="image_url",
        title="After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## U3 — Update Multiple Rows

    ### What we are doing

    Give BUSINESS employees a 5000 salary increase.

    ### Before
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        '''SELECT
        emp_id,
        emp_name,
        department,
        salary,
        gender,
        image_url
    FROM employees
    WHERE department = 'BUSINESS'
    ORDER BY emp_name;''',
        image_column="image_url",
        title="Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        '''UPDATE employees
    SET salary = salary + 5000
    WHERE department = 'BUSINESS';''',
        "BUSINESS salaries updated."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        '''SELECT
        emp_id,
        emp_name,
        department,
        salary,
        gender,
        image_url
    FROM employees
    WHERE department = 'BUSINESS'
    ORDER BY emp_name;''',
        image_column="image_url",
        title="After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## U4 — Update Image URL

    ### What we are doing

    Update Betty's avatar seed.

    ### Before
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        '''SELECT
        emp_id,
        emp_name,
        image_url
    FROM employees
    WHERE emp_name = 'Betty';''',
        image_column="image_url",
        title="Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        '''UPDATE employees
    SET image_url = 'https://api.dicebear.com/7.x/adventurer/svg?seed=BettyUpdated'
    WHERE emp_name = 'Betty';''',
        "Betty image URL updated."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        '''SELECT
        emp_id,
        emp_name,
        image_url
    FROM employees
    WHERE emp_name = 'Betty';''',
        image_column="image_url",
        title="After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 5 — Delete Operations

    Delete means removing rows from a table. Always use `WHERE` when deleting specific rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## D1 — Delete Copied Employee

    ### What we are doing

    Delete Alex_COPY.

    ### Before
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_id = 940;
        """,
        image_column="image_url",
        title="Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        """
            DELETE
            FROM employees
            WHERE emp_id = 940;
        """,
        "Copied employee deleted."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_id = 940;
        """,
        image_column="image_url",
        title="After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## D2 — Delete Temporary Employee

    ### What we are doing

    Delete Omar.

    ### Before
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_name = 'Omar';
        """,
        image_column="image_url",
        title="Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        """
            DELETE
            FROM employees
            WHERE emp_name = 'Omar';
        """,
        "Omar deleted."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_name = 'Omar';
        """,
        image_column="image_url",
        title="After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## D3 — Delete by Condition

    ### What we are doing

    Delete employees with salary less than 70000.

    ### Before
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE salary < 70000;
        """,
        image_column="image_url",
        title="Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        """
            DELETE
            FROM employees
            WHERE salary < 70000;
        """,
        "Low-salary rows deleted if any."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE salary < 70000;
        """,
        image_column="image_url",
        title="After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## D4 — Delete from Summary Table

    ### What we are doing

    Delete summary rows with employee_count less than 2.

    ### Before
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT *
            FROM department_salary_summary
            ORDER BY department;
        """,
        "Before"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Transformation
    """)
    return


@app.cell
def _(con, run_statement):
    run_statement(
        con,
        """
            DELETE
            FROM department_salary_summary
            WHERE employee_count < 2;
        """,
        "Low-count summary rows deleted."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT *
            FROM department_salary_summary
            ORDER BY department;
        """,
        "After"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 6 — 10 Basic Queries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B1

    ### What we are doing

    Show all employees.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            ORDER BY emp_id;
        """,
        image_column="image_url",
        title="B1 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B2

    ### What we are doing

    Show employee names only.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        '''SELECT
        emp_name
    FROM employees
    ORDER BY emp_name;''',
        "B2 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B3

    ### What we are doing

    Show SALES employees.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE department = 'SALES'
            ORDER BY emp_name;
        """,
        image_column="image_url",
        title="B3 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B4

    ### What we are doing

    Show female employees.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE gender = 'FEMALE'
            ORDER BY emp_name;
        """,
        image_column="image_url",
        title="B4 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B5

    ### What we are doing

    Show male employees.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE gender = 'MALE'
            ORDER BY emp_name;
        """,
        image_column="image_url",
        title="B5 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B6

    ### What we are doing

    Show salaries greater than 150000.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE salary > 150000
            ORDER BY salary DESC;
        """,
        image_column="image_url",
        title="B6 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B7

    ### What we are doing

    Show top 3 salaries.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        '''SELECT
        emp_name,
        salary,
        image_url
    FROM employees
    ORDER BY salary DESC
    LIMIT 3;''',
        image_column="image_url",
        title="B7 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B8

    ### What we are doing

    Show AI employees ordered by salary.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        '''SELECT
        emp_name,
        department,
        salary,
        image_url
    FROM employees
    WHERE department = 'AI'
    ORDER BY salary DESC;''',
        image_column="image_url",
        title="B8 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B9

    ### What we are doing

    Show names starting with B.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            WHERE emp_name LIKE 'B%'
            ORDER BY emp_name;
        """,
        image_column="image_url",
        title="B9 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B10

    ### What we are doing

    Show first 5 employees by emp_id.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    run_query_with_images(
        con,
        """
            SELECT *
            FROM employees
            ORDER BY emp_id
            LIMIT 5;
        """,
        image_column="image_url",
        title="B10 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 7 — 10 GROUP BY, HAVING, LIMIT Queries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## G1

    ### What we are doing

    Count employees per department.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT
                department,
                COUNT(*) AS employee_count
            FROM employees
            GROUP BY department
            ORDER BY employee_count DESC;
        """,
        "G1 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## G2

    ### What we are doing

    Average salary per department.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT
                department,
                ROUND(AVG(salary), 2) AS avg_salary
            FROM employees
            GROUP BY department
            ORDER BY avg_salary DESC;
        """,
        "G2 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## G3

    ### What we are doing

    Total salary per department.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT
                department,
                SUM(salary) AS total_salary
            FROM employees
            GROUP BY department
            ORDER BY total_salary DESC;
        """,
        "G3 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## G4

    ### What we are doing

    Highest salary per department.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT
                department,
                MAX(salary) AS highest_salary
            FROM employees
            GROUP BY department
            ORDER BY highest_salary DESC;
        """,
        "G4 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## G5

    ### What we are doing

    Lowest salary per department.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT
                department,
                MIN(salary) AS lowest_salary
            FROM employees
            GROUP BY department
            ORDER BY lowest_salary;
        """,
        "G5 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## G6

    ### What we are doing

    Count employees by gender.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT
                gender,
                COUNT(*) AS employee_count
            FROM employees
            GROUP BY gender
            ORDER BY employee_count DESC;
        """,
        "G6 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## G7

    ### What we are doing

    Departments with average salary greater than 150000.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT
                department,
                ROUND(AVG(salary), 2) AS avg_salary
            FROM employees
            GROUP BY department
            HAVING AVG(salary) > 150000
            ORDER BY avg_salary DESC;
        """,
        "G7 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## G8

    ### What we are doing

    Departments with at least 2 employees.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT
                department,
                COUNT(*) AS employee_count
            FROM employees
            GROUP BY department
            HAVING COUNT(*) >= 2
            ORDER BY employee_count DESC;
        """,
        "G8 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## G9

    ### What we are doing

    Top 2 departments by total salary.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT
                department,
                SUM(salary) AS total_salary
            FROM employees
            GROUP BY department
            ORDER BY total_salary DESC
            LIMIT 2;
        """,
        "G9 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## G10

    ### What we are doing

    Gender counts inside each department.
    """)
    return


@app.cell
def _(con, run_query):
    run_query(
        con,
        """
            SELECT
                department,
                gender,
                COUNT(*) AS employee_count
            FROM employees
            GROUP BY department, gender
            ORDER BY department, gender;
        """,
        "G10 result"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 8 — Solid Queries with Meaningful Plots
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## P1 — Percentage Male/Female Employees

    ### What we are doing

    Calculate percentage of employees by gender.
    """)
    return


@app.cell
def _(con, plot_pie, run_query):
    _df = run_query(
        con,
        """
            SELECT
                gender,
                COUNT(*) AS employee_count,
                ROUND( 100.0 * COUNT(*) / (
            SELECT COUNT(*)
            FROM employees), 2 ) AS percentage
            FROM employees
            GROUP BY gender
            ORDER BY gender;
        """,
        "P1 — Percentage Male/Female Employees result"
    )

    plot_pie(_df, labels_col='gender', values_col='percentage', title='Percentage of Employees by Gender')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## P2 — Percentage per Department

    ### What we are doing

    Calculate percentage of employees by department.
    """)
    return


@app.cell
def _(con, plot_bar, run_query):
    _df = run_query(
        con,
        """
            SELECT
                department,
                COUNT(*) AS employee_count,
                ROUND( 100.0 * COUNT(*) / (
            SELECT COUNT(*)
            FROM employees), 2 ) AS percentage
            FROM employees
            GROUP BY department
            ORDER BY percentage DESC;
        """,
        "P2 — Percentage per Department result"
    )

    plot_bar(_df, x='department', y='percentage', title='Percentage of Employees per Department', ylabel='Percentage')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## P3 — Highest Salaries

    ### What we are doing

    Show the highest salaries.
    """)
    return


@app.cell
def _(con, plot_bar, run_query):
    _df = run_query(
        con,
        '''SELECT
        emp_name,
        department,
        salary
    FROM employees
    ORDER BY salary DESC
    LIMIT 5;''',
        "P3 — Highest Salaries result"
    )

    plot_bar(_df, x='emp_name', y='salary', title='Top 5 Highest Salaries', ylabel='Salary')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## P4 — Lowest Salaries

    ### What we are doing

    Show the lowest salaries.
    """)
    return


@app.cell
def _(con, plot_bar, run_query):
    _df = run_query(
        con,
        '''SELECT
        emp_name,
        department,
        salary
    FROM employees
    ORDER BY salary ASC
    LIMIT 5;''',
        "P4 — Lowest Salaries result"
    )

    plot_bar(_df, x='emp_name', y='salary', title='Bottom 5 Lowest Salaries', ylabel='Salary')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## P5 — Highest Salary per Department

    ### What we are doing

    Show highest salary per department.
    """)
    return


@app.cell
def _(con, plot_bar, run_query):
    _df = run_query(
        con,
        """
            SELECT
                department,
                MAX(salary) AS highest_salary
            FROM employees
            GROUP BY department
            ORDER BY highest_salary DESC;
        """,
        "P5 — Highest Salary per Department result"
    )

    plot_bar(_df, x='department', y='highest_salary', title='Highest Salary per Department', ylabel='Highest Salary')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## P6 — Lowest Salary per Department

    ### What we are doing

    Show lowest salary per department.
    """)
    return


@app.cell
def _(con, plot_bar, run_query):
    _df = run_query(
        con,
        """
            SELECT
                department,
                MIN(salary) AS lowest_salary
            FROM employees
            GROUP BY department
            ORDER BY lowest_salary ASC;
        """,
        "P6 — Lowest Salary per Department result"
    )

    plot_bar(_df, x='department', y='lowest_salary', title='Lowest Salary per Department', ylabel='Lowest Salary')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 9 — Final State of employees Table

    ### What we are doing

    We display the final state after all CRUD operations.
    """)
    return


@app.cell
def _(con, run_query_with_images):
    _sql = """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """

    run_query_with_images(
        con,
        _sql,
        image_column="image_url",
        title="Final employees table"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Summary

    In this notebook, we learned:

    ## Create
    - `CREATE TABLE`
    - `INSERT INTO`
    - `CREATE TABLE AS SELECT`

    ## Read
    - `SELECT`
    - `WHERE`
    - `ORDER BY`
    - `LIMIT`
    - `GROUP BY`
    - `HAVING`

    ## Update
    - `UPDATE`
    - `SET`
    - `WHERE`

    ## Delete
    - `DELETE FROM`
    - `WHERE`

    We also learned how to:
    - create DuckDB tables from CSV files
    - display result sets cleanly
    - render avatar images from URL columns
    - create meaningful plots from SQL result sets
    """)
    return


if __name__ == "__main__":
    app.run()
