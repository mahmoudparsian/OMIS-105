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
    # 🔑 Primary Keys in Relational Databases
    ### A Hands-On Tutorial with DuckDB

    ---

    ## What You Will Learn

    By the end of this notebook you will understand:

    | Topic | Description |
    |---|---|
    | **Primary Key (PK)** | What it is, why it matters |
    | **Without a PK** | How duplicate rows sneak in |
    | **Enforcing a PK** | Using DuckDB to prevent duplicates |
    | **CRUD operations** | Create, Read, Update, Delete — with live examples |
    | **Analytics** | Aggregation queries with visualisations |

    ---

    ## Key Vocabulary

    **DuckDB** – An in-process analytical SQL database. Think of it as SQLite but built for analytics.  
    **Relational database** – Data stored in tables (rows + columns) that can be related to each other.  
    **Primary Key (PK)** – A column (or combination of columns) that **uniquely identifies every row** in a table. No two rows may share the same PK value, and PK values may never be NULL.  
    **CRUD** – The four fundamental database operations: **C**reate, **R**ead, **U**pdate, **D**elete.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 0 · Setup

    Import libraries, load utility functions, and connect to our in-memory DuckDB database.

    > **Note:** Running this cell again is safe — it simply re-creates the connection.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Install required Libraries 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Import libraries
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import sys, os

    # Make plot_util available regardless of working directory
    sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))
    from plot_util import (
        display_table,
        plot_bar,
        plot_gender_pie,
        plot_salary_range,
        plot_dept_bar,
    )

    # Path to our CSV (relative to this notebook)
    CSV_PATH = 'data/employees.csv'

    # Connect to an in-memory DuckDB instance
    # (re-running this cell drops and recreates a fresh connection)
    con = duckdb.connect(database=':memory:')
    print('✅ DuckDB connected  |  version:', duckdb.__version__)
    return (CSV_PATH, con, display_table, plot_bar, plot_dept_bar, plot_gender_pie, plot_salary_range)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1 · The Problem with No Primary Key

    Before we enforce a primary key, let's see what happens without one.

    ### 1.1  Create a table **without** a primary key
    """)
    return


@app.cell
def _(con):
    # Drop table if it exists so this cell is idempotent
    con.execute("""
        DROP TABLE IF EXISTS employees_no_pk;
    """)

    _sql = """
        CREATE TABLE employees_no_pk (
            emp_id     INTEGER,
            emp_name   VARCHAR,
            department VARCHAR,
            salary     INTEGER,
            gender     VARCHAR
        );
    """
    con.execute(_sql)
    print('Table employees_no_pk created (no primary key).')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2  Load employees from CSV
    """)
    return


@app.cell
def _(CSV_PATH, con, display_table):
    _sql = """
        INSERT INTO employees_no_pk
        SELECT *
        FROM read_csv_auto(?);
    """
    con.execute(_sql, [CSV_PATH])

    _df = con.execute("""
        SELECT *
        FROM employees_no_pk;
    """).df()
    display_table(_df, 'employees_no_pk  —  initial load')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.3  Duplicate insert — the danger zone!

    Without a primary key the database has **no guard** against identical rows.  
    Watch what happens when we accidentally insert `emp_id = 100` twice.
    """)
    return


@app.cell
def _(con, display_table):
    # First, remove any previous duplicate so re-runs stay clean
    con.execute("""
        DELETE
        FROM employees_no_pk
        WHERE emp_id = 100
        AND emp_name = 'Alex';
    """)
    # Insert the original row once more to have a clean baseline
    con.execute("""
        INSERT INTO employees_no_pk
        VALUES (100, 'Alex', 'SALES', 120000, 'MALE');
    """)

    # ---- Now intentionally insert Alex again ----
    _sql = """
        INSERT INTO employees_no_pk
        VALUES (100, 'Alex', 'SALES', 120000, 'MALE');
    """
    con.execute(_sql)
    print('⚠️  Inserted emp_id=100 (Alex) a second time — no error raised!')

    _df = con.execute("""
        SELECT *
        FROM employees_no_pk
        ORDER BY emp_id;
    """).df()
    display_table(_df, '👀  employees_no_pk after duplicate insert — spot the problem!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Observation:** Employee 100 (Alex) now appears **twice**.  <br>
    * Any report totalling salaries would overcount him.           
    * Any JOIN on `emp_id` would produce phantom rows.             
    * This is exactly why we need a **Primary Key**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2 · Enforcing the Primary Key

    A **Primary Key constraint** tells DuckDB:

    - The `emp_id` column must be **unique** across all rows.
    - The `emp_id` column can **never be NULL**.
    - Any attempt to insert a duplicate `emp_id` will raise an **error** immediately.

    ### 2.1  Create the `employees` table **with** a primary key
    """)
    return


@app.cell
def _(con):
    # Drop and recreate — makes the notebook idempotent
    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)

    _sql = """
        CREATE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            /* ← PK enforced here */        emp_name VARCHAR NOT NULL,
            department VARCHAR NOT NULL,
            salary     INTEGER NOT NULL,
            gender     VARCHAR NOT NULL
        );
    """
    con.execute(_sql)
    print('✅  Table employees created WITH PRIMARY KEY on emp_id.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2  Load employees from CSV
    """)
    return


@app.cell
def _(CSV_PATH, con, display_table):
    _sql = """
        INSERT INTO employees
        SELECT *
        FROM read_csv_auto(?);
    """
    con.execute(_sql, [CSV_PATH])

    _df = con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """).df()
    display_table(_df, 'employees  —  initial load (PK enforced)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3  Prove the PK blocks duplicates
    """)
    return


@app.cell
def _(con):
    print('Attempting to insert a duplicate emp_id = 100 ...')
    try:
        con.execute("""
            INSERT INTO employees
            VALUES (100, 'Alex', 'SALES', 120000, 'MALE');
        """)
        print('ERROR: Duplicate was accepted — PK is NOT working!')
    except Exception as e:
        print(f'✅  DuckDB correctly rejected the duplicate:\n    {e}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3 · CRUD Operations

    **CRUD** stands for the four core operations every database supports:

    | Letter | Operation | SQL Statement |
    |--------|-----------|---------------|
    | **C**  | Create    | `INSERT INTO` |
    | **R**  | Read      | `SELECT`      |
    | **U**  | Update    | `UPDATE ... SET` |
    | **D**  | Delete    | `DELETE FROM` |

    We will demonstrate **3 examples of each**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### ➕ C · CREATE (INSERT)

    **INSERT** adds new rows to a table.  
    Because our table has a PK, every new `emp_id` must be unique.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### C-1  Insert a single new employee
    """)
    return


@app.cell
def _(con, display_table):
    # ── Before ───────────────────────────────────────────────────────────────────
    _df_before = con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """).df()
    display_table(_df_before, 'BEFORE  —  C-1: Insert single employee')

    # ── SQL ──────────────────────────────────────────────────────────────────────
    # Remove first in case cell is re-run
    con.execute("""
        DELETE
        FROM employees
        WHERE emp_id = 920;
    """)

    _sql = """
        INSERT INTO employees (emp_id, emp_name, department, salary, gender)
        VALUES (920, 'Carlos', 'AI', 195000, 'MALE');
    """
    print('SQL:\n', _sql)
    con.execute(_sql)

    # ── After ────────────────────────────────────────────────────────────────────
    _df_after = con.execute('SELECT * FROM employees ORDER BY emp_id').df()
    display_table(_df_after, 'AFTER  —  Carlos (920) added to AI department')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### C-2  Insert multiple employees at once
    """)
    return


@app.cell
def _(con, display_table):
    # ── Before ───────────────────────────────────────────────────────────────────
    _df_before = con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """).df()
    display_table(_df_before, 'BEFORE  —  C-2: Insert multiple employees')

    # ── SQL ──────────────────────────────────────────────────────────────────────
    con.execute("""
        DELETE
        FROM employees
        WHERE emp_id IN (930, 940);
    """)

    _sql = """
        INSERT INTO employees (emp_id, emp_name, department, salary, gender)
        VALUES
            (930, 'Diana', 'BUSINESS', 145000, 'FEMALE'),
            (940, 'Ethan', 'SALES', 135000, 'MALE');
    """
    print('SQL:\n', _sql)
    con.execute(_sql)

    # ── After ────────────────────────────────────────────────────────────────────
    _df_after = con.execute('SELECT * FROM employees ORDER BY emp_id').df()
    display_table(_df_after, 'AFTER  —  Diana (930) and Ethan (940) added')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### C-3  INSERT … SELECT — copy rows from another source
    """)
    return


@app.cell
def _(con, display_table):
    # ── Before ───────────────────────────────────────────────────────────────────
    _df_before = con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """).df()
    display_table(_df_before, 'BEFORE  —  C-3: INSERT … SELECT from staging')

    # ── SQL ──────────────────────────────────────────────────────────────────────
    # Create a tiny staging table, insert from it, then clean up
    con.execute("""
        DROP TABLE IF EXISTS staging;
    """)
    con.execute("""
        CREATE TABLE staging AS
        SELECT
            950 AS emp_id,
            'Fiona' AS emp_name,
            'AI' AS department,
            210000 AS salary,
            'FEMALE' AS gender;
    """)
    con.execute("""
        DELETE
        FROM employees
        WHERE emp_id = 950;
    """)

    _sql = """
        INSERT INTO employees
        SELECT *
        FROM staging
        WHERE emp_id NOT IN (
        SELECT emp_id
        FROM employees);
    """
    print('SQL:\n', _sql)
    con.execute(_sql)
    con.execute('DROP TABLE IF EXISTS staging')

    # ── After ────────────────────────────────────────────────────────────────────
    _df_after = con.execute('SELECT * FROM employees ORDER BY emp_id').df()
    display_table(_df_after, 'AFTER  —  Fiona (950) inserted via INSERT … SELECT')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 🔍 R · READ (SELECT)

    **SELECT** retrieves rows from a table.  
    You can filter (`WHERE`), sort (`ORDER BY`), and aggregate (`GROUP BY`).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### R-1  Select all employees sorted by salary (descending)
    """)
    return


@app.cell
def _(con, display_table, plot_bar):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            gender
        FROM employees
        ORDER BY salary DESC;
    """
    print('SQL:\n', _sql)
    _df = con.execute(_sql).df()
    display_table(_df, 'R-1: All employees ordered by salary (highest first)')

    plot_bar(
        _df['emp_name'], _df['salary'],
        title='Employee Salaries (Descending)',
        xlabel='Employee', ylabel='Salary ($)',
        value_fmt='${:,.0f}'
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### R-2  Filter — read only SALES employees
    """)
    return


@app.cell
def _(con, display_table, plot_bar):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        WHERE department = 'SALES'
        ORDER BY salary DESC;
    """
    print('SQL:\n', _sql)
    _df = con.execute(_sql).df()
    display_table(_df, 'R-2: SALES employees only')

    plot_bar(
        _df['emp_name'], _df['salary'],
        title='SALES Department — Salaries',
        xlabel='Employee', ylabel='Salary ($)',
        color='#55A868',
        value_fmt='${:,.0f}'
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### R-3  Aggregate — count and average salary per department
    """)
    return


@app.cell
def _(con, display_table, plot_bar):
    _sql = """
        SELECT
            department,
            COUNT(*) AS headcount,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
    """
    print('SQL:\n', _sql)
    _df = con.execute(_sql).df()
    display_table(_df, 'R-3: Headcount and average salary per department')

    plot_bar(
        _df['department'], _df['avg_salary'],
        title='Average Salary by Department',
        xlabel='Department', ylabel='Avg Salary ($)',
        color='#8172B2',
        value_fmt='${:,.0f}'
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### ✏️ U · UPDATE

    **UPDATE** modifies existing rows.  
    Always use a `WHERE` clause — without it, *every* row gets changed!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### U-1  Give one employee a raise
    """)
    return


@app.cell
def _(con, display_table):
    # ── Before ───────────────────────────────────────────────────────────────────
    _df_before = con.execute(
        """
            SELECT
                emp_id,
                emp_name,
                salary
            FROM employees
            WHERE emp_id = 700;
        """
    ).df()
    display_table(_df_before, 'BEFORE  —  U-1: Raise for emp_id 700 (Dara)')

    # ── SQL ──────────────────────────────────────────────────────────────────────
    _sql = """
        UPDATE employees
        SET salary = 205000
        WHERE emp_id = 700;
    """
    print('SQL:\n', _sql)
    con.execute(_sql)

    # ── After ────────────────────────────────────────────────────────────────────
    _df_after = con.execute(
        "SELECT emp_id, emp_name, salary FROM employees WHERE emp_id = 700"
    ).df()
    display_table(_df_after, 'AFTER  —  Dara salary updated to $205,000')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### U-2  Transfer an employee to a new department
    """)
    return


@app.cell
def _(con, display_table):
    # ── Before ───────────────────────────────────────────────────────────────────
    _df_before = con.execute(
        """
            SELECT
                emp_id,
                emp_name,
                department
            FROM employees
            WHERE emp_id = 940;
        """
    ).df()
    display_table(_df_before, 'BEFORE  —  U-2: Transfer Ethan (940) to AI')

    # ── SQL ──────────────────────────────────────────────────────────────────────
    _sql = """
        UPDATE employees
        SET department = 'AI'
        WHERE emp_id = 940;
    """
    print('SQL:\n', _sql)
    con.execute(_sql)

    # ── After ────────────────────────────────────────────────────────────────────
    _df_after = con.execute(
        "SELECT emp_id, emp_name, department FROM employees WHERE emp_id = 940"
    ).df()
    display_table(_df_after, 'AFTER  —  Ethan transferred to AI')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### U-3  Apply a 10 % raise to all BUSINESS employees
    """)
    return


@app.cell
def _(con, display_table):
    # ── Before ───────────────────────────────────────────────────────────────────
    _df_before = con.execute(
        """
            SELECT
                emp_id,
                emp_name,
                salary
            FROM employees
            WHERE department = 'BUSINESS'
            ORDER BY emp_id;
        """
    ).df()
    display_table(_df_before, 'BEFORE  —  U-3: 10% raise for all BUSINESS employees')

    # ── SQL ──────────────────────────────────────────────────────────────────────
    _sql = """
        UPDATE employees
        SET salary = ROUND(salary * 1.10)
        WHERE department = 'BUSINESS';
    """
    print('SQL:\n', _sql)
    con.execute(_sql)

    # ── After ────────────────────────────────────────────────────────────────────
    _df_after = con.execute(
        "SELECT emp_id, emp_name, salary FROM employees WHERE department = 'BUSINESS' ORDER BY emp_id"
    ).df()
    display_table(_df_after, 'AFTER  —  10% raise applied to BUSINESS department')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 🗑️ D · DELETE

    **DELETE** permanently removes rows from a table.  
    Again, always use `WHERE` — `DELETE FROM employees` with no condition wipes the entire table!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### D-1  Delete a single employee by primary key
    """)
    return


@app.cell
def _(con, display_table):
    # Re-insert 950 (Fiona) if needed so D-1 always has something to delete
    existing = con.execute("""
        SELECT COUNT(*)
        FROM employees
        WHERE emp_id = 950;
    """).fetchone()[0]
    if existing == 0:
        con.execute("""
            INSERT INTO employees
            VALUES (950, 'Fiona', 'AI', 210000, 'FEMALE');
        """)

    # ── Before ───────────────────────────────────────────────────────────────────
    _df_before = con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """).df()
    display_table(_df_before, 'BEFORE  —  D-1: Delete Fiona (emp_id = 950)')

    # ── SQL ──────────────────────────────────────────────────────────────────────
    _sql = """
        DELETE
        FROM employees
        WHERE emp_id = 950;
    """
    print('SQL:\n', _sql)
    con.execute(_sql)

    # ── After ────────────────────────────────────────────────────────────────────
    _df_after = con.execute('SELECT * FROM employees ORDER BY emp_id').df()
    display_table(_df_after, 'AFTER  —  Fiona removed')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### D-2  Delete employees whose salary is below a threshold
    """)
    return


@app.cell
def _(con, display_table):
    # Re-add test rows if needed
    if con.execute("""
        SELECT COUNT(*)
        FROM employees
        WHERE emp_id = 940;
    """).fetchone()[0] == 0:
        con.execute("""
            INSERT INTO employees
            VALUES (940, 'Ethan', 'AI', 135000, 'MALE');
        """)

    # ── Before ───────────────────────────────────────────────────────────────────
    _df_before = con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """).df()
    display_table(_df_before, 'BEFORE  —  D-2: Remove employees with salary < 130,000')

    # ── SQL ──────────────────────────────────────────────────────────────────────
    _sql = """
        DELETE
        FROM employees
        WHERE salary < 130000;
    """
    print('SQL:\n', _sql)
    con.execute(_sql)

    # ── After ────────────────────────────────────────────────────────────────────
    _df_after = con.execute('SELECT * FROM employees ORDER BY emp_id').df()
    display_table(_df_after, 'AFTER  —  Employees earning < $130,000 removed')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### D-3  Delete all employees in a specific department (then restore)
    """)
    return


@app.cell
def _(CSV_PATH, con, display_table):
    # Ensure at least one SALES employee exists
    for row in [(100,'Alex','SALES',120000,'MALE'),
                (200,'Jeff','SALES',140000,'MALE')]:
        if con.execute(f"SELECT COUNT(*) FROM employees WHERE emp_id = {row[0]}").fetchone()[0] == 0:
            con.execute(f"INSERT INTO employees VALUES {row}")

    # ── Before ───────────────────────────────────────────────────────────────────
    _df_before = con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """).df()
    display_table(_df_before, 'BEFORE  —  D-3: Delete all SALES employees')

    # ── SQL ──────────────────────────────────────────────────────────────────────
    _sql = """
        DELETE
        FROM employees
        WHERE department = 'SALES';
    """
    print('SQL:\n', _sql)
    con.execute(_sql)

    # ── After ────────────────────────────────────────────────────────────────────
    _df_after = con.execute('SELECT * FROM employees ORDER BY emp_id').df()
    display_table(_df_after, 'AFTER  —  All SALES rows removed')

    # ── Restore from CSV so analytics section has full data ──────────────────────
    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)
    con.execute("""
        CREATE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR NOT NULL,
            department VARCHAR NOT NULL,
            salary     INTEGER NOT NULL,
            gender     VARCHAR NOT NULL
        );
    """)
    con.execute("""
        INSERT INTO employees
        SELECT *
        FROM read_csv_auto(?);
    """, [CSV_PATH])
    print('\n✅  employees table restored from CSV for the analytics section.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 · Analytics Queries

    Now that we understand CRUD, let's mine the data for insights.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A-1  Gender distribution (% male vs female)

    > ⚠️ **Data Quality Alert — Teaching Moment**  
    > Before we run this query, notice that the raw CSV contains a **typo** in the `gender` column: one row has `'FMALE'` instead of `'FEMALE'`.  
    > We will first run the query on the **dirty data** so you can see the problem, then fix it with an `UPDATE` statement and re-run.  
    > This is a classic example of why **data cleaning** is an essential step before any analysis.
    """)
    return


@app.cell
def _(con, display_table):
    # ── Dirty data — shows FMALE as a separate gender ───────────────────────
    _sql = """
        SELECT
            gender,
            COUNT(*) AS headcount,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct
        FROM employees
        GROUP BY gender
        ORDER BY headcount DESC;
    """
    print('SQL:\n', _sql)
    df_dirty = con.execute(_sql).df()
    display_table(df_dirty, 'A-1 (dirty): Gender distribution — notice "FMALE" is a separate row!')

    print("\n👆 There are 3 gender groups instead of 2 because Susan's gender was",
          "mis-typed as 'FMALE' in the source CSV.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 🔧 Fix the Data Error

    The raw CSV has `gender = 'FMALE'` for **Susan (emp_id = 400)** — a simple typo.  
    In a real project you would fix the source file, but we can also correct it directly
    in the database using an `UPDATE` statement.

    This is also a great reminder: **always inspect your data before analysing it.**  
    A quick `GROUP BY gender` (as above) immediately surfaces the anomaly.
    """)
    return


@app.cell
def _(con, display_table):
    # ── Before ───────────────────────────────────────────────────────────────────
    _df_before = con.execute(
        """
            SELECT
                emp_id,
                emp_name,
                gender
            FROM employees
            WHERE gender = 'FMALE';
        """
    ).df()
    display_table(_df_before, 'BEFORE  —  Row(s) with the typo "FMALE"')

    # ── SQL ──────────────────────────────────────────────────────────────────────
    _sql = """
        UPDATE employees
        SET gender = 'FEMALE'
        WHERE gender = 'FMALE';
    """
    print('SQL:\n', _sql)
    con.execute(_sql)

    # ── After ────────────────────────────────────────────────────────────────────
    _df_after = con.execute(
        """
            SELECT
                emp_id,
                emp_name,
                gender
            FROM employees
            WHERE emp_id = 400;
        """
    ).df()
    display_table(_df_after, 'AFTER  —  Susan\'s gender corrected to "FEMALE"')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### ✅ A-1 (Clean)  Gender distribution after the fix
    """)
    return


@app.cell
def _(con, display_table, plot_gender_pie):
    _sql = """
        SELECT
            gender,
            COUNT(*) AS headcount,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct
        FROM employees
        GROUP BY gender
        ORDER BY headcount DESC;
    """
    print('SQL:\n', _sql)
    _df = con.execute(_sql).df()
    display_table(_df, 'A-1 (clean): Gender distribution — now correctly 2 groups')

    plot_gender_pie(_df['gender'].tolist(), _df['pct'].tolist())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A-2  Employee distribution by department (%)
    """)
    return


@app.cell
def _(con, display_table, plot_dept_bar):
    _sql = """
        SELECT
            department,
            COUNT(*) AS headcount,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct
        FROM employees
        GROUP BY department
        ORDER BY pct DESC;
    """
    print('SQL:\n', _sql)
    _df = con.execute(_sql).df()
    display_table(_df, 'A-2: Employee % per department')

    plot_dept_bar(_df['department'].tolist(), _df['pct'].tolist())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A-3  Overall highest and lowest salaries
    """)
    return


@app.cell
def _(con, display_table, plot_bar):
    _sql = """
        SELECT
            'Highest' AS rank_label,
            emp_name,
            department,
            salary
        FROM employees
        WHERE salary = (
        SELECT MAX(salary)
        FROM employees)
        UNION ALL
        SELECT
            'Lowest' AS rank_label,
            emp_name,
            department,
            salary
        FROM employees
        WHERE salary = (
        SELECT MIN(salary)
        FROM employees);
    """
    print('SQL:\n', _sql)
    _df = con.execute(_sql).df()
    display_table(_df, 'A-3: Highest and lowest paid employees overall')

    plot_bar(
        _df.apply(lambda r: f"{r['emp_name']} ({r['rank_label']})", axis=1),
        _df['salary'],
        title='Highest vs Lowest Salary — Overall',
        ylabel='Salary ($)',
        color='#C44E52',
        value_fmt='${:,.0f}'
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A-4  Highest and lowest salary per department
    """)
    return


@app.cell
def _(con, display_table, plot_salary_range):
    _sql = """
        SELECT
            department,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            MAX(salary) - MIN(salary) AS salary_range
        FROM employees
        GROUP BY department
        ORDER BY department;
    """
    print('SQL:\n', _sql)
    _df = con.execute(_sql).df()
    display_table(_df, 'A-4: Min / Max salary per department')

    plot_salary_range(
        _df['department'], _df['min_salary'], _df['max_salary'],
        title='Min and Max Salary by Department',
        group_label='Department'
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 · Summary

    | Concept | Key Takeaway |
    |---|---|
    | **No Primary Key** | Duplicate rows are silently accepted — data integrity is broken |
    | **Primary Key** | Uniqueness + NOT NULL guaranteed at the database level |
    | **INSERT** | Adds rows; PK blocks duplicate `emp_id` |
    | **SELECT** | Retrieves rows; filter with `WHERE`, sort with `ORDER BY` |
    | **UPDATE** | Modifies existing rows; always use `WHERE` |
    | **DELETE** | Removes rows permanently; always use `WHERE` |

    > **Rule of thumb:** Every table should have a primary key.  
    > If the data doesn't have a natural key, add a surrogate key (e.g., `id INTEGER PRIMARY KEY`).
    """)
    return


if __name__ == "__main__":
    app.run()
