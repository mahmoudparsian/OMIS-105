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
    # 🦆 CRUD of Employee Data — DuckDB Edition

    > **Course:** OMIS 105 · Data Stories  
    > **Topic:** Create · Read · Update · Delete with DuckDB & SQL  
    > **Audience:** Beginners — no prior DuckDB or SQL experience required

    ---

    ## What is DuckDB?

    **DuckDB** is a blazing-fast, in-process analytical database — think SQLite, but optimised for data analysis.  
    It runs *inside* your Python process (no server needed) and speaks full SQL.

    ## What is CRUD?

    | Letter | SQL Keyword | Meaning |
    |--------|-------------|------------------------------------|
    | **C** | `INSERT` | **C**reate new rows of data |
    | **R** | `SELECT` | **R**ead / retrieve existing data |
    | **U** | `UPDATE` | **U**pdate / modify existing data |
    | **D** | `DELETE` | **D**elete rows from a table |

    Every application that stores data — Instagram, Gmail, your bank — runs on CRUD.

    ---

    ## Notebook Road-Map

    ```
    0. Setup & Imports
    1. CREATE  — Build the employees table (4 operations)
    2. READ    — Query & explore the data  (4+ operations)
    3. UPDATE  — Modify existing rows      (4 operations)
    4. DELETE  — Remove rows               (4 operations)
    5. Basic Queries    — 10 SELECT / WHERE / LIMIT
    6. Aggregate Queries — 10 GROUP BY / HAVING / LIMIT
    7. Intermediate Queries — 10 ranking, subqueries, CTEs
    8. Visualisations   — Plots linked to real query results
    ```

    > 🔁 **This notebook is idempotent** — you can run every cell from top to bottom as many times as you like without errors.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 0 · Setup & Imports
    """)
    return


@app.cell
def _():
    # ── 0.1  Install dependencies (silent if already installed) ──────────────────
    import subprocess, sys


    # ── 0.2  Core imports ────────────────────────────────────────────────────────
    import duckdb
    import pandas as pd
    import sys, pathlib

    # ── 0.3  Add notebook folder to path so we can import notebook_utils ─────────
    NB_DIR = pathlib.Path().resolve()            # folder this notebook lives in
    if str(NB_DIR) not in sys.path:
        sys.path.insert(0, str(NB_DIR))

    from notebook_utils import (
        show_table, show_sql, show_header, show_note,
        plot_bar, plot_horizontal_bar, plot_pie,
        plot_hist, plot_grouped_bar, plot_scatter, plot_line
    )

    # ── 0.4  Create (or reconnect to) an in-memory DuckDB database ───────────────
    con = duckdb.connect()          # pure in-memory, no file needed

    # ── 0.5  Path to the CSV data folder ─────────────────────────────────────────
    DATA_DIR = NB_DIR / "data"

    print("✅ DuckDB version:", duckdb.__version__)
    print("✅ Data folder   :", DATA_DIR)
    return (DATA_DIR, con, plot_bar, plot_grouped_bar, plot_hist, plot_horizontal_bar, plot_line, plot_pie, plot_scatter, show_header, show_note, show_sql, show_table)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1 · CREATE — Building the Employees Table

    ### What is CREATE?

    The **CREATE** operation adds *new data* to the database.  
    In SQL this means:
    - **`CREATE TABLE`** — define the table schema (columns + data types)
    - **`INSERT INTO`** — add rows of data into the table

    We will also demonstrate loading data from a **CSV file** using DuckDB's powerful `READ_CSV_AUTO()` function.

    ### Our Employee Table Schema

    | Column | Type | Description |
    |------------|---------|-------------------------------------|
    | emp_id | INTEGER | Unique employee identifier |
    | emp_name | VARCHAR | Full name of the employee |
    | department | VARCHAR | Department: SALES, IT, AI, … |
    | salary | INTEGER | Annual salary in USD |
    | gender | VARCHAR | MALE or FEMALE |
    | degree | VARCHAR | Highest degree: BA, BS, MS, MIS, PHD|
    | hire_date | DATE | Date the employee was hired |
    | country | VARCHAR | Country: USA, CANADA, CHINA |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-1 · `CREATE TABLE` — Define the Schema (drop & recreate for idempotency)
    """)
    return


@app.cell
def _(con, show_header, show_note, show_sql):
    show_header("C-1 · CREATE TABLE", "Define the employees table schema")

    _sql = """
        DROP TABLE IF EXISTS employees;
        CREATE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR NOT NULL,
            department VARCHAR NOT NULL,
            salary     INTEGER NOT NULL,
            gender     VARCHAR NOT NULL,
            degree     VARCHAR NOT NULL,
            hire_date  DATE NOT NULL,
            country    VARCHAR NOT NULL
        );
    """

    show_sql(_sql, "C-1 · SQL: Create Table")
    con.execute(_sql)
    show_note("Table 'employees' created successfully.", "success")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-2 · `INSERT INTO` — Add Rows with SQL (the manual way)
    """)
    return


@app.cell
def _(con, show_header, show_note, show_sql, show_table):
    show_header("C-2 · INSERT INTO (9 employees via SQL)",
                "The fundamental way to add rows — one INSERT statement at a time")

    _sql = """
        INSERT INTO employees
        VALUES
            /* USA (3 employees) */ (100, 'John Smith', 'SALES', 95000, 'MALE', 'BS', '2015-03-15', 'USA'),
            (101, 'Emily Johnson', 'IT', 142000, 'FEMALE', 'MS', '2015-06-01', 'USA'),
            (102, 'Michael Davis', 'AI', 198000, 'MALE', 'PHD', '2015-09-10', 'USA'),
            /* CANADA (3 employees) */ (103, 'Sophie Tremblay', 'MARKETING', 87000, 'FEMALE', 'BA', '2015-02-20', 'CANADA'),
            (104, 'Liam Bouchard', 'BUSINESS', 115000, 'MALE', 'MIS', '2015-07-14', 'CANADA'),
            (105, 'Chloe Gagnon', 'AI', 175000, 'FEMALE', 'MS', '2015-11-03', 'CANADA'),
            /* CHINA (3 employees) */ (106, 'Wei Zhang', 'IT', 155000, 'FEMALE', 'MS', '2015-04-18', 'CHINA'),
            (107, 'Hao Liu', 'AI', 210000, 'MALE', 'PHD', '2015-08-25', 'CHINA'),
            (108, 'Mei Chen', 'BUSINESS', 130000, 'FEMALE', 'MIS', '2015-01-30', 'CHINA');
    """

    show_sql(_sql, "C-2 · SQL: INSERT 9 Employees")
    con.execute(_sql)

    _df = con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """).df()
    show_note(f"Inserted {len(_df)} employees.", "success")
    show_table(_df, "employees — after INSERT")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-3 · Export to CSV — Save a Snapshot
    """)
    return


@app.cell
def _(DATA_DIR, con, show_header, show_note, show_sql):
    show_header("C-3 · COPY TO CSV", "Persist the table as a CSV file in the data/ folder")

    import os
    os.makedirs(DATA_DIR, exist_ok=True)
    _csv_path = str(DATA_DIR / "employees.csv")

    _sql = f"""
        COPY employees
        TO '{_csv_path}'
        ( HEADER, DELIMITER ',' );
    """
    show_sql(_sql, "C-3 · SQL: Export to CSV")
    con.execute(_sql)
    show_note(f"CSV written → {_csv_path}", "success")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-4 · Load from CSV — `READ_CSV_AUTO`
    """)
    return


@app.cell
def _(DATA_DIR, con, show_header, show_note, show_sql, show_table):
    show_header("C-4 · CREATE TABLE … AS SELECT from CSV",
                "DuckDB can read CSV directly — no pandas required")

    _csv_path = str(DATA_DIR / "employees.csv")

    _sql = f"""
        DROP TABLE IF EXISTS employees_from_csv;

        CREATE TABLE employees_from_csv AS
            SELECT *
            FROM READ_CSV_AUTO('{_csv_path}');
    """
    show_sql(_sql, "C-4 · SQL: Load CSV into a new table")
    con.execute(_sql)

    _df = con.execute("""
        SELECT *
        FROM employees_from_csv
        ORDER BY emp_id;
    """).df()
    show_note(f"Loaded {len(_df)} rows from CSV.", "success")
    show_table(_df, "employees_from_csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2 · READ — Querying the Data

    ### What is READ?

    The **READ** operation retrieves data from the database without changing it.  
    In SQL the primary keyword is **`SELECT`**.

    The anatomy of a SELECT:
    ```sql
    SELECT  <columns>         -- what columns to return
    FROM    <table>           -- which table
    WHERE   <condition>       -- optional filter
    ORDER BY <column>         -- optional sort
    LIMIT   <n>;              -- optional row cap
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-1 · Read ALL rows
    """)
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("R-1 · SELECT * — Read Every Row", "The simplest possible query")

    _sql = """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """
    show_sql(_sql, "R-1 · SQL: Select All")
    _df = con.execute(_sql).df()
    show_table(_df, "All Employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-2 · Read with WHERE Filter
    """)
    return


@app.cell
def _(con, plot_bar, show_header, show_sql, show_table):
    show_header("R-2 · SELECT with WHERE", "Filter rows to only AI department employees")

    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            country
        FROM employees
        WHERE department = 'AI'
        ORDER BY salary DESC;
    """
    show_sql(_sql, "R-2 · SQL: AI Employees Sorted by Salary")
    _df = con.execute(_sql).df()
    show_table(_df, "AI Department Employees")
    plot_bar(_df, "emp_name", "salary",
             title="AI Department — Salary Comparison",
             xlabel="Employee", ylabel="Annual Salary ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-3 · Read Specific Columns
    """)
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("R-3 · SELECT Specific Columns", "Only fetch the columns we actually need")

    _sql = """
        SELECT
            emp_name,
            country,
            salary,
            degree
        FROM employees
        ORDER BY country, salary DESC;
    """
    show_sql(_sql, "R-3 · SQL: Name / Country / Salary / Degree")
    _df = con.execute(_sql).df()
    show_table(_df, "Employees — Selected Columns")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-4 · Read with Multiple WHERE Conditions
    """)
    return


@app.cell
def _(con, plot_horizontal_bar, show_header, show_sql, show_table):
    show_header("R-4 · WHERE with AND / OR",
                "Combine conditions to narrow results precisely")

    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            gender,
            country
        FROM employees
        WHERE salary > 100000
        AND gender = 'FEMALE'
        ORDER BY salary DESC;
    """
    show_sql(_sql, "R-4 · SQL: Female Employees Earning > $100,000")
    _df = con.execute(_sql).df()
    show_table(_df, "High-Earning Female Employees")
    plot_horizontal_bar(_df, "emp_name", "salary",
                        title="Female Employees — Salary > $100K",
                        xlabel="Annual Salary ($)", ylabel="Employee")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3 · UPDATE — Modifying Existing Rows

    ### What is UPDATE?

    **UPDATE** changes the value of one or more columns in *existing* rows.  
    The anatomy:
    ```sql
    UPDATE  <table>
    SET     <column> = <new_value>
    WHERE   <condition>;      -- ⚠️ always include WHERE or you change EVERY row!
    ```

    > ⚠️ **Golden Rule:** Always include a `WHERE` clause when updating, or you'll accidentally change every single row!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-1 · Give One Employee a Raise
    """)
    return


@app.cell
def _(con, show_header, show_note, show_sql, show_table):
    show_header("U-1 · UPDATE — Single Row Salary Raise",
                "John Smith (emp_id=100) gets a 10% raise")

    # BEFORE
    _df_before = con.execute("""
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        WHERE emp_id = 100;
    """).df()
    show_note("BEFORE the update:", "warning")
    show_table(_df_before, "Before")

    _sql = """
        UPDATE employees
        SET salary = ROUND(salary * 1.10)
        WHERE emp_id = 100;
    """
    show_sql(_sql, "U-1 · SQL: 10% Raise for emp_id = 100")
    con.execute(_sql)

    # AFTER
    _df_after = con.execute("SELECT emp_id, emp_name, salary FROM employees WHERE emp_id = 100").df()
    show_note("AFTER the update:", "success")
    show_table(_df_after, "After")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-2 · Department-Wide Raise
    """)
    return


@app.cell
def _(con, show_header, show_note, show_sql, show_table):
    show_header("U-2 · UPDATE — Department-Wide Salary Adjustment",
                "The IT department gets a 5% pay bump")

    _df_before = con.execute("""
        SELECT
            emp_id,
            emp_name,
            department,
            salary
        FROM employees
        WHERE department = 'IT'
        ORDER BY emp_id;
    """).df()
    show_note("BEFORE:", "warning")
    show_table(_df_before, "IT Department — Before")

    _sql = """
        UPDATE employees
        SET salary = ROUND(salary * 1.05)
        WHERE department = 'IT';
    """
    show_sql(_sql, "U-2 · SQL: 5% Raise for IT Department")
    con.execute(_sql)

    _df_after = con.execute("""
        SELECT emp_id, emp_name, department, salary
        FROM   employees
        WHERE  department = 'IT'
        ORDER BY emp_id
    """).df()
    show_note("AFTER:", "success")
    show_table(_df_after, "IT Department — After")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-3 · Update Multiple Columns at Once
    """)
    return


@app.cell
def _(con, show_header, show_note, show_sql, show_table):
    show_header("U-3 · UPDATE Multiple Columns",
                "Sophie Tremblay moves from MARKETING to BUSINESS and gets a promotion raise")

    _df_before = con.execute("""
        SELECT *
        FROM employees
        WHERE emp_id = 103;
    """).df()
    show_note("BEFORE:", "warning")
    show_table(_df_before, "Before")

    _sql = """
        UPDATE employees
        SET department = 'BUSINESS', salary = 105000
        WHERE emp_id = 103;
    """
    show_sql(_sql, "U-3 · SQL: Promotion — Change Department + Salary")
    con.execute(_sql)

    _df_after = con.execute("SELECT * FROM employees WHERE emp_id = 103").df()
    show_note("AFTER:", "success")
    show_table(_df_after, "After")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-4 · Bulk Update with CASE WHEN
    """)
    return


@app.cell
def _(con, show_header, show_note, show_sql, show_table):
    show_header("U-4 · UPDATE with CASE WHEN",
                "Apply differentiated raises based on degree level")

    _df_before = con.execute("""
        SELECT
            emp_id,
            emp_name,
            degree,
            salary
        FROM employees
        ORDER BY emp_id;
    """).df()
    show_note("BEFORE (degree-based raise):", "warning")
    show_table(_df_before, "Before")

    _sql = """
        UPDATE employees
        SET salary = ROUND( salary * CASE degree WHEN 'PHD' THEN 1.08 WHEN 'MS' THEN 1.06 WHEN 'MIS' THEN 1.05 WHEN 'BS' THEN 1.04 WHEN 'BA' THEN 1.03 ELSE 1.00 END );
    """
    show_sql(_sql, "U-4 · SQL: Degree-Based Salary Adjustments")
    con.execute(_sql)

    _df_after = con.execute("SELECT emp_id, emp_name, degree, salary FROM employees ORDER BY emp_id").df()
    show_note("AFTER:", "success")
    show_table(_df_after, "After")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 · DELETE — Removing Rows

    ### What is DELETE?

    **DELETE** permanently removes rows from a table.  
    The anatomy:
    ```sql
    DELETE FROM <table>
    WHERE  <condition>;       -- ⚠️ omit WHERE → delete EVERYTHING!
    ```

    > ⚠️ **Golden Rule:** Always double-check your `WHERE` clause before running DELETE.  
    > A `SELECT` with the same `WHERE` first is a safe habit.

    We will add temporary rows to practice deletion without destroying our real data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-1 · Delete a Single Row
    """)
    return


@app.cell
def _(con, show_header, show_note, show_sql, show_table):
    show_header("D-1 · DELETE a Single Row",
                "Add a test employee, then delete them")

    # Add temp row first
    con.execute("""
        INSERT INTO employees
        VALUES (999, 'Temp Worker', 'SALES', 50000, 'MALE', 'BA', '2015-12-01', 'USA') ON CONFLICT (emp_id) DO NOTHING;
    """)
    _df_before = con.execute("""
        SELECT *
        FROM employees
        WHERE emp_id = 999;
    """).df()
    show_note("BEFORE — temp employee exists:", "warning")
    show_table(_df_before, "Before")

    _sql = """
        DELETE
        FROM employees
        WHERE emp_id = 999;
    """
    show_sql(_sql, "D-1 · SQL: Delete Single Employee")
    con.execute(_sql)

    _df_after = con.execute("SELECT * FROM employees WHERE emp_id = 999").df()
    show_note(f"AFTER — rows with emp_id=999: {len(_df_after)}", "success")
    show_table(_df_after, "After (should be empty)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-2 · Delete Based on a Condition
    """)
    return


@app.cell
def _(con, show_header, show_note, show_sql, show_table):
    show_header("D-2 · DELETE Based on Salary Threshold",
                "Add 2 low-salary temps, then delete all employees earning below $60,000")

    con.execute("""
        INSERT INTO employees
        VALUES
            (990, 'Intern Alice', 'SALES', 40000, 'FEMALE', 'BA', '2015-12-10', 'USA'),
            (991, 'Intern Bob', 'MARKETING',45000, 'MALE', 'BA', '2015-12-15', 'USA') ON CONFLICT (emp_id) DO NOTHING;
    """)
    _df_before = con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """).df()
    show_note("BEFORE (11 rows, 2 interns added):", "warning")
    show_table(_df_before, "Before")

    _sql = """
        DELETE
        FROM employees
        WHERE salary < 60000;
    """
    show_sql(_sql, "D-2 · SQL: Delete Employees with Salary < $60,000")
    con.execute(_sql)

    _df_after = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    show_note(f"AFTER — {len(_df_after)} rows remain.", "success")
    show_table(_df_after, "After")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-3 · Delete with Multiple Conditions
    """)
    return


@app.cell
def _(con, show_header, show_note, show_sql, show_table):
    show_header("D-3 · DELETE with AND / OR",
                """
                    DELETE ANY temp rows we added (emp_id >= 900);
                """)

    # Ensure no temp rows leak from previous cells
    con.execute("""
        DELETE
        FROM employees
        WHERE emp_id >= 900;
    """)

    # Add fresh temps to demonstrate
    con.execute("""
        INSERT INTO employees
        VALUES
            (901, 'Temp X', 'SALES', 50000, 'MALE', 'BS', '2015-12-20', 'USA'),
            (902, 'Temp Y', 'IT', 55000, 'FEMALE', 'BA', '2015-12-21', 'USA') ON CONFLICT (emp_id) DO NOTHING;
    """)
    _df_before = con.execute("""
        SELECT *
        FROM employees
        WHERE emp_id >= 900;
    """).df()
    show_note("BEFORE — temp rows:", "warning")
    show_table(_df_before, "Temp Rows")

    _sql = """
        DELETE
        FROM employees
        WHERE emp_id >= 900
        AND emp_name LIKE 'Temp%';
    """
    show_sql(_sql, "D-3 · SQL: Delete All 'Temp' Employees")
    con.execute(_sql)

    _df_after = con.execute("SELECT * FROM employees WHERE emp_id >= 900").df()
    show_note(f"AFTER — temp rows remaining: {len(_df_after)}", "success")
    show_table(_df_after, "After (should be empty)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-4 · Delete with a Subquery
    """)
    return


@app.cell
def _(con, show_header, show_note, show_sql, show_table):
    show_header("D-4 · DELETE via Subquery",
                """
                    DELETE employees whose salary IS below the company average (demo only — we restore after);
                """)

    # Snapshot before
    _df_before = con.execute("""
        SELECT
            emp_id,
            emp_name,
            salary,
            ROUND(AVG(salary) OVER (), 0) AS avg_salary
        FROM employees
        ORDER BY salary;
    """).df()
    show_note("BEFORE — all employees with company average:", "warning")
    show_table(_df_before, "Before")

    _sql = """
        DELETE
        FROM employees
        WHERE salary < (
        SELECT AVG(salary)
        FROM employees );
    """
    show_sql(_sql, "D-4 · SQL: Delete Below-Average Salary Employees")
    con.execute(_sql)

    _df_after = con.execute("""
        SELECT *
        FROM employees
        ORDER BY salary;
    """).df()
    show_note(f"AFTER — {len(_df_after)} employees remain (above average salary).", "success")
    show_table(_df_after, "After")

    # ── Restore deleted rows so the rest of the notebook works ───────────────────
    show_note("Restoring deleted rows for the rest of the notebook…", "info")
    con.execute("""
        INSERT INTO employees
        VALUES
            (100, 'John Smith', 'SALES', 95000, 'MALE', 'BS', '2015-03-15', 'USA'),
            (103, 'Sophie Tremblay', 'BUSINESS', 105000,'FEMALE', 'BA', '2015-02-20', 'CANADA'),
            (104, 'Liam Bouchard', 'BUSINESS', 115000,'MALE', 'MIS', '2015-07-14', 'CANADA') ON CONFLICT (emp_id) DO NOTHING;
    """)
    df_restored = con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """).df()
    show_note(f"Restored. Total employees: {len(df_restored)}", "success")
    show_table(df_restored, "Employees — Restored")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 · 10 Basic Queries — SELECT / WHERE / LIMIT

    These foundational queries cover the everyday use of `SELECT`, `WHERE`, and `LIMIT`.
    """)
    return


@app.cell
def _(con, plot_bar, show_header, show_sql, show_table):
    show_header("BQ-1 · All Employees Sorted by Salary (Highest First)", "ORDER BY … DESC")

    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            country
        FROM employees
        ORDER BY salary DESC;
    """
    show_sql(_sql, "BQ-1")
    _df = con.execute(_sql).df()
    show_table(_df, "Employees Sorted by Salary")
    plot_bar(_df, "emp_name", "salary",
             title="Employee Salaries — High to Low",
             xlabel="Employee", ylabel="Salary ($)")
    return


@app.cell
def _(con, plot_bar, show_header, show_sql, show_table):
    show_header("BQ-2 · Top 3 Earners", "LIMIT restricts how many rows are returned")

    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary,
            department,
            country
        FROM employees
        ORDER BY salary DESC
        LIMIT 3;
    """
    show_sql(_sql, "BQ-2")
    _df = con.execute(_sql).df()
    show_table(_df, "Top 3 Earners")
    plot_bar(_df, "emp_name", "salary",
             title="Top 3 Earners",
             xlabel="Employee", ylabel="Salary ($)")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("BQ-3 · Employees from Canada", "WHERE with a single equality condition")

    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            degree
        FROM employees
        WHERE country = 'CANADA'
        ORDER BY salary DESC;
    """
    show_sql(_sql, "BQ-3")
    _df = con.execute(_sql).df()
    show_table(_df, "Canadian Employees")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("BQ-4 · Employees with Salary Between $100K and $160K",
                "BETWEEN is inclusive on both ends")

    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary,
            department,
            country
        FROM employees
        WHERE salary BETWEEN 100000
        AND 160000
        ORDER BY salary;
    """
    show_sql(_sql, "BQ-4")
    _df = con.execute(_sql).df()
    show_table(_df, "Mid-Range Salary Employees")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("BQ-5 · Female Employees with a PhD or MS",
                "WHERE … AND … IN (…)")

    _sql = """
        SELECT
            emp_id,
            emp_name,
            gender,
            degree,
            salary,
            country
        FROM employees
        WHERE gender = 'FEMALE'
        AND degree IN ('PHD', 'MS')
        ORDER BY salary DESC;
    """
    show_sql(_sql, "BQ-5")
    _df = con.execute(_sql).df()
    show_table(_df, "Female PhD/MS Employees")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("BQ-6 · Distinct Departments", "DISTINCT removes duplicate values")

    _sql = """
        SELECT DISTINCT department
        FROM employees
        ORDER BY department;
    """
    show_sql(_sql, "BQ-6")
    _df = con.execute(_sql).df()
    show_table(_df, "Unique Departments")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("BQ-7 · Employees Hired in Q1 2015",
                "Filter by date range: January–March 2015")

    _sql = """
        SELECT
            emp_id,
            emp_name,
            hire_date,
            department
        FROM employees
        WHERE hire_date BETWEEN '2015-01-01'
        AND '2015-03-31'
        ORDER BY hire_date;
    """
    show_sql(_sql, "BQ-7")
    _df = con.execute(_sql).df()
    show_table(_df, "Q1 2015 Hires")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("BQ-8 · Computed Column — Monthly Salary",
                "Create a derived column with arithmetic in SELECT")

    _sql = """
        SELECT
            emp_name,
            salary AS annual_salary,
            ROUND(salary / 12) AS monthly_salary
        FROM employees
        ORDER BY annual_salary DESC;
    """
    show_sql(_sql, "BQ-8")
    _df = con.execute(_sql).df()
    show_table(_df, "Annual vs Monthly Salary")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("BQ-9 · Employees NOT in the AI Department",
                "Using NOT and != (not equal) operators")

    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            country
        FROM employees
        WHERE department != 'AI'
        ORDER BY department, salary DESC;
    """
    show_sql(_sql, "BQ-9")
    _df = con.execute(_sql).df()
    show_table(_df, "Non-AI Employees")
    return


@app.cell
def _(con, plot_pie, show_header, show_sql, show_table):
    show_header("BQ-10 · Country Workforce Summary Count",
                "Using COUNT(*) to tally rows per country")

    _sql = """
        SELECT
            country,
            COUNT(*) AS employee_count
        FROM employees
        GROUP BY country
        ORDER BY employee_count DESC;
    """
    show_sql(_sql, "BQ-10")
    _df = con.execute(_sql).df()
    show_table(_df, "Employees per Country")
    plot_pie(_df, "country", "employee_count",
             title="Employee Distribution by Country")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6 · 10 Aggregate Queries — GROUP BY / HAVING / LIMIT

    ### What is GROUP BY?

    `GROUP BY` collapses multiple rows into summary rows — one per unique value of the grouping column.  
    Aggregate functions like `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` operate on each group.

    `HAVING` filters *groups* (like `WHERE` but for aggregated results).
    """)
    return


@app.cell
def _(con, plot_bar, show_header, show_sql, show_table):
    show_header("AQ-1 · Average Salary by Department", "GROUP BY + AVG")

    _sql = """
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_salary,
            COUNT(*) AS headcount
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
    """
    show_sql(_sql, "AQ-1")
    _df = con.execute(_sql).df()
    show_table(_df, "Average Salary by Department")
    plot_bar(_df, "department", "avg_salary",
             title="Average Salary by Department",
             xlabel="Department", ylabel="Avg Salary ($)")
    return


@app.cell
def _(con, plot_bar, show_header, show_sql, show_table):
    show_header("AQ-2 · Total Payroll by Country", "GROUP BY + SUM")

    _sql = """
        SELECT
            country,
            SUM(salary) AS total_payroll,
            COUNT(*) AS headcount
        FROM employees
        GROUP BY country
        ORDER BY total_payroll DESC;
    """
    show_sql(_sql, "AQ-2")
    _df = con.execute(_sql).df()
    show_table(_df, "Total Payroll by Country")
    plot_bar(_df, "country", "total_payroll",
             title="Total Payroll by Country",
             xlabel="Country", ylabel="Total Payroll ($)")
    return


@app.cell
def _(con, plot_pie, show_header, show_sql, show_table):
    show_header("AQ-3 · Gender Distribution", "GROUP BY + COUNT")

    _sql = """
        SELECT
            gender,
            COUNT(*) AS count,
            ROUND(AVG(salary),0) AS avg_salary
        FROM employees
        GROUP BY gender
        ORDER BY COUNT DESC;
    """
    show_sql(_sql, "AQ-3")
    _df = con.execute(_sql).df()
    show_table(_df, "Gender Distribution")
    plot_pie(_df, "gender", "count", title="Gender Distribution")
    return


@app.cell
def _(con, plot_bar, show_header, show_sql, show_table):
    show_header("AQ-4 · Degree Distribution", "Count employees per degree")

    _sql = """
        SELECT
            degree,
            COUNT(*) AS count,
            ROUND(AVG(salary),0) AS avg_salary
        FROM employees
        GROUP BY degree
        ORDER BY avg_salary DESC;
    """
    show_sql(_sql, "AQ-4")
    _df = con.execute(_sql).df()
    show_table(_df, "Degree Distribution")
    plot_bar(_df, "degree", "avg_salary",
             title="Average Salary by Degree",
             xlabel="Degree", ylabel="Avg Salary ($)")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("AQ-5 · HAVING — Departments with Avg Salary > $130K",
                "HAVING filters groups, not individual rows")

    _sql = """
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department
        HAVING AVG(salary) > 130000
        ORDER BY avg_salary DESC;
    """
    show_sql(_sql, "AQ-5")
    _df = con.execute(_sql).df()
    show_table(_df, "High-Paying Departments (Avg > $130K)")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("AQ-6 · Min & Max Salary by Country",
                "MIN and MAX in one GROUP BY query")

    _sql = """
        SELECT
            country,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            MAX(salary) - MIN(salary) AS salary_range
        FROM employees
        GROUP BY country
        ORDER BY salary_range DESC;
    """
    show_sql(_sql, "AQ-6")
    _df = con.execute(_sql).df()
    show_table(_df, "Salary Range by Country")
    return


@app.cell
def _(con, plot_grouped_bar, show_header, show_sql, show_table):
    show_header("AQ-7 · Headcount by Department and Country",
                "GROUP BY two columns simultaneously")

    _sql = """
        SELECT
            department,
            country,
            COUNT(*) AS headcount
        FROM employees
        GROUP BY department, country
        ORDER BY department, country;
    """
    show_sql(_sql, "AQ-7")
    _df = con.execute(_sql).df()
    show_table(_df, "Headcount — Department × Country")
    plot_grouped_bar(_df, "country", "headcount", "department",
                     title="Headcount by Country and Department",
                     xlabel="Country", ylabel="Count")
    return


@app.cell
def _(con, plot_grouped_bar, show_header, show_sql, show_table):
    show_header("AQ-8 · Average Salary by Gender per Country",
                "Multi-dimensional aggregation")

    _sql = """
        SELECT
            country,
            gender,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY country, gender
        ORDER BY country, avg_salary DESC;
    """
    show_sql(_sql, "AQ-8")
    _df = con.execute(_sql).df()
    show_table(_df, "Avg Salary — Country × Gender")
    plot_grouped_bar(_df, "country", "avg_salary", "gender",
                     title="Average Salary by Country and Gender",
                     xlabel="Country", ylabel="Avg Salary ($)")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("AQ-9 · Top Earning Department (LIMIT 1)",
                "Combine GROUP BY + ORDER BY + LIMIT to find the #1 result")

    _sql = """
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC
        LIMIT 1;
    """
    show_sql(_sql, "AQ-9")
    _df = con.execute(_sql).df()
    show_table(_df, "Highest-Paying Department")
    return


@app.cell
def _(con, plot_pie, show_header, show_sql, show_table):
    show_header("AQ-10 · Degree Groups with More Than 1 Employee",
                "HAVING COUNT(*) > 1")

    _sql = """
        SELECT
            degree,
            COUNT(*) AS count
        FROM employees
        GROUP BY degree
        HAVING COUNT(*) > 1
        ORDER BY COUNT DESC;
    """
    show_sql(_sql, "AQ-10")
    _df = con.execute(_sql).df()
    show_table(_df, "Degrees with Multiple Employees")
    plot_pie(_df, "degree", "count",
             title="Most Common Degrees (>1 employee)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7 · 10 Intermediate Queries — Ranking, Subqueries, CTEs

    ### Key concepts:

    | Concept | What it does |
    |---------|-----------------------------|
    | **Window function** | Compute a value *across* a set of rows related to the current row |
    | **RANK() / ROW_NUMBER()** | Rank rows within a partition |
    | **Subquery** | A `SELECT` nested inside another `SELECT` or `WHERE` |
    | **CTE (Common Table Expression)** | A temporary named result set defined with `WITH` |
    """)
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("IQ-1 · Salary Rank (Company-Wide)",
                "RANK() assigns a rank to each employee by salary")

    _sql = """
        SELECT
            emp_name,
            department,
            salary,
            RANK() OVER (
        ORDER BY salary DESC) AS salary_rank
        FROM employees
        ORDER BY salary_rank;
    """
    show_sql(_sql, "IQ-1 · Window Function: RANK()")
    _df = con.execute(_sql).df()
    show_table(_df, "Company-Wide Salary Ranking")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("IQ-2 · Salary Rank Within Each Country",
                "PARTITION BY resets the rank for each country")

    _sql = """
        SELECT
            emp_name,
            country,
            salary,
            RANK() OVER ( PARTITION BY country
        ORDER BY salary DESC ) AS country_rank
        FROM employees
        ORDER BY country, country_rank;
    """
    show_sql(_sql, "IQ-2 · RANK with PARTITION BY country")
    _df = con.execute(_sql).df()
    show_table(_df, "Salary Rank Within Each Country")
    return


@app.cell
def _(con, plot_bar, show_header, show_sql, show_table):
    show_header("IQ-3 · Top Earner per Country (Subquery)",
                "Filter to rank = 1 using a subquery")

    _sql = """
        SELECT *
        FROM (
        SELECT
            emp_name,
            country,
            department,
            salary,
            RANK() OVER ( PARTITION BY country
        ORDER BY salary DESC ) AS rnk
        FROM employees ) ranked
        WHERE rnk = 1
        ORDER BY salary DESC;
    """
    show_sql(_sql, "IQ-3 · Subquery: Top Earner per Country")
    _df = con.execute(_sql).df()
    show_table(_df, "Top Earner per Country")
    plot_bar(_df, "country", "salary",
             title="Top Earner in Each Country",
             xlabel="Country", ylabel="Salary ($)")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("IQ-4 · Employees Above Company Average Salary (Subquery in WHERE)",
                "A scalar subquery returns a single value for comparison")

    _sql = """
        SELECT
            emp_name,
            department,
            salary,
            country
        FROM employees
        WHERE salary > (
        SELECT AVG(salary)
        FROM employees )
        ORDER BY salary DESC;
    """
    show_sql(_sql, "IQ-4 · Scalar Subquery in WHERE")
    _df = con.execute(_sql).df()
    show_table(_df, "Above-Average Earners")
    return


@app.cell
def _(con, plot_pie, show_header, show_sql, show_table):
    show_header("IQ-5 · CTE — Salary Percentile Buckets",
                """
                    WITH clause defines a reusable temp result (CTE);
                """)

    _sql = """
        WITH salary_stats AS (
        SELECT
            AVG(salary) AS avg_sal,
            PERCENTILE_CONT(0.25) WITHIN GROUP (
        ORDER BY salary) AS p25, PERCENTILE_CONT(0.75) WITHIN GROUP (
        ORDER BY salary) AS p75
        FROM employees )
        SELECT
            e.emp_name,
            e.salary,
            CASE WHEN e.salary < s.p25 THEN 'Low' WHEN e.salary BETWEEN s.p25
        AND s.p75 THEN 'Mid' ELSE 'High' END AS salary_tier
        FROM employees e
        CROSS
        JOIN salary_stats s
        ORDER BY e.salary;
    """
    show_sql(_sql, "IQ-5 · CTE: Salary Tiers")
    _df = con.execute(_sql).df()
    show_table(_df, "Employee Salary Tiers")
    tier_counts = _df["salary_tier"].value_counts().reset_index()
    tier_counts.columns = ["tier", "count"]
    plot_pie(tier_counts, "tier", "count", title="Salary Tier Distribution")
    return


@app.cell
def _(con, plot_line, show_header, show_sql, show_table):
    show_header("IQ-6 · Running Total of Salary (Cumulative)",
                "SUM() OVER with ORDER BY creates a running total")

    _sql = """
        SELECT
            emp_name,
            salary,
            SUM(salary) OVER (
        ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW ) AS running_total
        FROM employees
        ORDER BY salary;
    """
    show_sql(_sql, "IQ-6 · Running Total with Window Function")
    _df = con.execute(_sql).df()
    show_table(_df, "Running Total of Salary")
    plot_line(_df, "emp_name", "running_total",
              title="Cumulative Salary (Sorted by Salary)",
              xlabel="Employee", ylabel="Cumulative Salary ($)")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("IQ-7 · Salary vs Department Average (Difference)",
                "AVG() OVER (PARTITION BY) gives the group average in every row")

    _sql = """
        SELECT
            emp_name,
            department,
            salary,
            ROUND(AVG(salary) OVER (PARTITION BY department), 0) AS dept_avg,
            salary - ROUND(AVG(salary) OVER (PARTITION BY department), 0) AS diff_from_avg
        FROM employees
        ORDER BY department, salary DESC;
    """
    show_sql(_sql, "IQ-7 · Salary Delta from Department Average")
    _df = con.execute(_sql).df()
    show_table(_df, "Salary vs Department Average")
    return


@app.cell
def _(con, show_header, show_sql, show_table):
    show_header("IQ-8 · ROW_NUMBER — Unique Row Assignment",
                "ROW_NUMBER never ties (unlike RANK which can share a position)")

    _sql = """
        SELECT ROW_NUMBER() OVER (
        ORDER BY salary DESC) AS row_num, emp_name, salary, department
        FROM employees;
    """
    show_sql(_sql, "IQ-8 · ROW_NUMBER()")
    _df = con.execute(_sql).df()
    show_table(_df, "Employees with Unique Row Numbers")
    return


@app.cell
def _(con, plot_bar, show_header, show_sql, show_table):
    show_header("IQ-9 · Multi-Level CTE — Department Summary + Company Totals",
                "Chain two CTEs together")

    _sql = """
        WITH dept_summary AS (
        SELECT
            department,
            COUNT(*) AS headcount,
            ROUND(AVG(salary),0) AS avg_salary,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY department ), company_total AS (
        SELECT SUM(total_salary) AS grand_total
        FROM dept_summary )
        SELECT
            d.department,
            d.headcount,
            d.avg_salary,
            d.total_salary,
            ROUND(100.0 * d.total_salary / c.grand_total, 1) AS pct_of_payroll
        FROM dept_summary d
        CROSS
        JOIN company_total c
        ORDER BY d.total_salary DESC;
    """
    show_sql(_sql, "IQ-9 · Two-Level CTE")
    _df = con.execute(_sql).df()
    show_table(_df, "Department Payroll vs Company Total")
    plot_bar(_df, "department", "pct_of_payroll",
             title="Each Department's Share of Total Payroll (%)",
             xlabel="Department", ylabel="% of Payroll")
    return


@app.cell
def _(con, plot_bar, show_header, show_sql, show_table):
    show_header("IQ-10 · NTILE — Quartile Bucketing",
                "NTILE(4) splits employees into 4 salary quartiles")

    _sql = """
        SELECT
            emp_name,
            salary,
            NTILE(4) OVER (
        ORDER BY salary) AS quartile
        FROM employees
        ORDER BY quartile, salary;
    """
    show_sql(_sql, "IQ-10 · NTILE(4) Salary Quartiles")
    _df = con.execute(_sql).df()
    show_table(_df, "Employees by Salary Quartile")

    q_summary = _df.groupby("quartile")["salary"].agg(["mean","count"]).reset_index()
    q_summary.columns = ["quartile", "avg_salary", "count"]
    q_summary["quartile"] = "Q" + q_summary["quartile"].astype(str)
    plot_bar(q_summary, "quartile", "avg_salary",
             title="Average Salary per Quartile",
             xlabel="Quartile", ylabel="Avg Salary ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8 · Visualisations — Rich Plots from Query Results
    """)
    return


@app.cell
def _(con, plot_hist, show_header, show_table):
    show_header("VIZ-1 · Salary Distribution — Histogram",
                "How are salaries spread across all employees?")

    _df = con.execute("""
        SELECT salary
        FROM employees;
    """).df()
    show_table(_df, "Salaries")
    plot_hist(_df["salary"], title="Salary Distribution",
              xlabel="Annual Salary ($)", bins=6)
    return


@app.cell
def _(con, plot_horizontal_bar, show_header, show_sql, show_table):
    show_header("VIZ-2 · Average Salary by Degree — Horizontal Bar",
                "Higher education = higher pay?")

    _sql = """
        SELECT
            degree,
            ROUND(AVG(salary),0) AS avg_salary
        FROM employees
        GROUP BY degree
        ORDER BY avg_salary;
    """
    _df = con.execute(_sql).df()
    show_sql(_sql, "VIZ-2 · SQL")
    show_table(_df, "Avg Salary by Degree")
    plot_horizontal_bar(_df, "degree", "avg_salary",
                        title="Average Salary by Degree Level",
                        xlabel="Avg Salary ($)", ylabel="Degree")
    return


@app.cell
def _(con, plot_scatter, show_header, show_sql, show_table):
    show_header("VIZ-3 · Department Headcount vs Avg Salary — Scatter",
                "Bubble perspective: is a busier department better paid?")

    _sql = """
        SELECT
            department,
            COUNT(*) AS headcount,
            ROUND(AVG(salary),0) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY headcount;
    """
    _df = con.execute(_sql).df()
    show_sql(_sql, "VIZ-3 · SQL")
    show_table(_df, "Dept Headcount vs Avg Salary")
    plot_scatter(_df, "headcount", "avg_salary",
                 label_col="department",
                 title="Department: Headcount vs Average Salary")
    return


@app.cell
def _(con, plot_grouped_bar, show_header, show_sql, show_table):
    show_header("VIZ-4 · Country × Gender Breakdown — Grouped Bar",
                "How is gender distributed across countries?")

    _sql = """
        SELECT
            country,
            gender,
            COUNT(*) AS count
        FROM employees
        GROUP BY country, gender
        ORDER BY country, gender;
    """
    _df = con.execute(_sql).df()
    show_sql(_sql, "VIZ-4 · SQL")
    show_table(_df, "Gender per Country")
    plot_grouped_bar(_df, "country", "count", "gender",
                     title="Gender Distribution by Country",
                     xlabel="Country", ylabel="Headcount")
    return


@app.cell
def _(con, plot_bar, show_header, show_sql, show_table):
    show_header("VIZ-5 · Hire Month Distribution — Bar",
                "Which months saw the most hiring in 2015?")

    _sql = """
        SELECT
            STRFTIME(hire_date, '%b') AS month_name,
            MONTH(hire_date) AS month_num,
            COUNT(*) AS hires
        FROM employees
        GROUP BY month_name, month_num
        ORDER BY month_num;
    """
    show_sql(_sql, "VIZ-5 · SQL")
    _df = con.execute(_sql).df()
    show_table(_df, "Hires by Month")
    plot_bar(_df, "month_name", "hires",
             title="New Hires by Month (2015)",
             xlabel="Month", ylabel="Number of Hires")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🎓 Summary

    Congratulations! You have completed the **CRUD of Employee Data** notebook.

    | Section | What You Learned |
    |---------|------------------|
    | **C — Create** | `CREATE TABLE`, `INSERT INTO`, `COPY TO`, `READ_CSV_AUTO` |
    | **R — Read** | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`, `BETWEEN`, `IN` |
    | **U — Update** | `UPDATE … SET … WHERE`, multi-column updates, `CASE WHEN` |
    | **D — Delete** | `DELETE … WHERE`, subquery deletion, restore pattern |
    | **Basic Queries** | Filtering, sorting, derived columns, counting |
    | **Aggregate Queries** | `GROUP BY`, `HAVING`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` |
    | **Intermediate Queries** | `RANK()`, `ROW_NUMBER()`, `NTILE()`, CTEs, subqueries, running totals |
    | **Visualisations** | Bar, pie, histogram, scatter, grouped bar, line charts |

    ---
    *Built with 🦆 DuckDB · 🐼 pandas · 📊 matplotlib*
    """)
    return


if __name__ == "__main__":
    app.run()
