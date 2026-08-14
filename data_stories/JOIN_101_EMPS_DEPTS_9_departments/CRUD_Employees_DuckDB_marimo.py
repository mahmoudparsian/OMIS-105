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
    # 🦆 CRUD Operations with DuckDB — Employee Data

    > **Course:** OMIS 105 · Data Stories  
    > **Topic:** Create · Read · Update · Delete  
    > **Database:** DuckDB in-process SQL engine  
    > **Data:** 10 Employee Records  

    ---

    ## What is DuckDB?

    **DuckDB** is a fast, lightweight, *in-process* SQL database engine — meaning it runs entirely inside your Python program with no separate server needed. Think of it as SQLite but optimised for analytical queries.

    Key advantages:
    - ✅ Zero configuration — no server to install or start
    - ✅ Full SQL support (SELECT, INSERT, UPDATE, DELETE, GROUP BY, …)
    - ✅ Reads CSV files directly
    - ✅ Integrates seamlessly with pandas DataFrames
    - ✅ Blazing fast on analytical workloads

    ---

    ## What is CRUD?

    **CRUD** is an acronym for the four fundamental database operations:

    | Letter | Operation | SQL Statement | What it does |
    |--------|-----------|---------------|--------------|
    | **C** | **Create** | `INSERT INTO` | Adds new rows to a table |
    | **R** | **Read**   | `SELECT`      | Retrieves / queries rows |
    | **U** | **Update** | `UPDATE … SET`| Modifies existing rows |
    | **D** | **Delete** | `DELETE FROM` | Removes rows from a table |

    Every database-driven application in the world — Instagram, banking apps, hospital records — is built on these four operations.

    ---

    ## Notebook Structure

    1. **Setup** — imports, helpers, DuckDB connection  
    2. **Table Creation** — INSERT rows & load from CSV  
    3. **CREATE (C)** — 4 INSERT examples  
    4. **READ (R)** — 4 SELECT examples + 10 basic queries + 10 GROUP BY queries  
    5. **UPDATE (U)** — 4 UPDATE examples  
    6. **DELETE (D)** — 4 DELETE examples  
    7. **Analytics & Plots** — salary, gender, department insights  
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📦 Cell 1 — Setup: Imports & Helper Functions

    We import our helper module `crud_helpers.py` which lives in the same folder.  
    It contains all display, tabulation, and plotting code — **you don't need to touch it**.  
    We also create a fresh in-memory DuckDB connection each time the notebook runs.
    """)
    return


@app.cell
def _():
    # ── Imports ──────────────────────────────────────────────────────────
    import sys, os

    # The following line tells Python where to find our 
    # helper file crud_helpers.py — it adds the notebook's 
    # own folder to Python's search path so that import crud_helpers 
    # works no matter where Jupyter was launched from.
    sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))

    import duckdb
    import pandas as pd
    from crud_helpers import run, query, show_table, print_sql, section, \
        plot_hbar, plot_vbar, plot_pie, plot_salary_range
    return (duckdb, plot_hbar, plot_pie, plot_salary_range, plot_vbar, print_sql, query, run, section)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Connect to DuckDB
    """)
    return


@app.cell
def _(duckdb):
    # ── DuckDB in-memory connection (fresh every run) ─────────────────────
    con = duckdb.connect()   # ':memory:' is the default

    print("✅ DuckDB", duckdb.__version__, "ready. Connection opened.")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🗂️ Cell 2 — Create Tables

    ### Method A — `employees` table via INSERT statements

    We first **drop** the table if it already exists (so the notebook is safe to re-run),  
    then **create** it and **insert** 10 employee rows.

    **Schema:**

    | Column | Type | Description |
    |--------|------|-------------|
    | `emp_id` | INTEGER | Unique employee number |
    | `emp_name` | VARCHAR | Employee first name |
    | `department` | VARCHAR | Department (SALES / BUSINESS / AI) |
    | `salary` | INTEGER | Annual salary in USD |
    | `gender` | VARCHAR | MALE / FEMALE |
    """)
    return


@app.cell
def _(con, run):
    # ── Drop & recreate employees (idempotent) ────────────────────────────
    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)

    con.execute("""
        CREATE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR,
            department VARCHAR,
            salary     INTEGER,
            gender     VARCHAR
        );
    """)

    con.execute("""
        INSERT INTO employees
        VALUES
            (100, 'Alex', 'SALES', 120000, 'MALE'),
            (200, 'Jeff', 'SALES', 140000, 'MALE'),
            (300, 'Rafa', 'BUSINESS', 150000, 'MALE'),
            (400, 'Susan', 'SALES', 150000, 'FMALE'),
            (500, 'Jen', 'BUSINESS', 160000, 'FEMALE'),
            (600, 'Barb', 'BUSINESS', 180000, 'FEMALE'),
            (700, 'Dara', 'AI', 190000, 'MALE'),
            (800, 'Venus', 'AI', 200000, 'FEMALE'),
            (900, 'Margie', 'SALES', 140000, 'FEMALE'),
            (910, 'Betty', 'SALES', 170000, 'FEMALE');
    """)

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """,
        title="employees — initial 10 rows")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Method B — `employees_backup` table loaded from CSV

    DuckDB can read CSV files directly using `read_csv_auto()`.  
    This is identical data — we keep it as a backup / reference table.
    """)
    return


@app.cell
def _(con, run):
    # ── employees_backup from CSV ─────────────────────────────────────────
    CSV_PATH = "data/employees.csv"

    con.execute("""
        DROP TABLE IF EXISTS employees_backup;
    """)
    con.execute(f"""
    CREATE TABLE employees_backup AS
        SELECT * FROM read_csv_auto('{CSV_PATH}')
    """)

    run(con, """
        SELECT *
        FROM employees_backup
        ORDER BY employee_id;
    """,
        title="employees_backup — loaded from CSV")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ C — CREATE (INSERT)

    ## What is INSERT?

    The `INSERT INTO` statement **adds one or more new rows** to a table.

    **Syntax:**
    ```sql
    INSERT INTO table_name (col1, col2, ...)
    VALUES (val1, val2, ...);
    ```

    > 💡 After each INSERT we show the full table so you can see what changed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-1 · Insert a single new employee
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("C-1 · Insert a single new employee")

    # ── Before ────────────────────────────────────────────────────────────
    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE INSERT")

    # ── SQL ───────────────────────────────────────────────────────────────
    sql_c1 = """
        INSERT INTO employees (emp_id, emp_name, department, salary, gender)
        VALUES (920, 'Carlos', 'AI', 210000, 'MALE');
    """
    print_sql(sql_c1)
    con.execute(sql_c1)

    # ── After ─────────────────────────────────────────────────────────────
    run(con, "SELECT * FROM employees ORDER BY emp_id", title="AFTER INSERT — Carlos added")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-2 · Insert multiple employees in one statement
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("C-2 · Insert multiple employees in one statement")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE INSERT")

    sql_c2 = """
        INSERT INTO employees (emp_id, emp_name, department, salary, gender)
        VALUES
            (930, 'Diana', 'BUSINESS', 155000, 'FEMALE'),
            (940, 'Ethan', 'AI', 195000, 'MALE');
    """
    print_sql(sql_c2)
    con.execute(sql_c2)

    run(con, "SELECT * FROM employees ORDER BY emp_id",
        title="AFTER INSERT — Diana & Ethan added")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-3 · Insert using a SELECT (copy rows from backup)
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("C-3 · Insert using SELECT — copy a row from backup")

    # We insert emp_id=950 by sourcing data from the backup table
    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE INSERT")

    sql_c3 = """
        INSERT INTO employees
        SELECT
            950 AS emp_id,
            'Fiona' AS emp_name,
            job_title AS department,
            salary + 5000 AS salary,
            'FEMALE' AS gender
        FROM employees_backup
        WHERE employee_id = 1;
    """
    print_sql(sql_c3)
    con.execute(sql_c3)

    run(con, "SELECT * FROM employees ORDER BY emp_id",
        title="AFTER INSERT — Fiona added (derived from backup row 700)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-4 · Insert with a DEFAULT-like pattern (NULL for optional fields)

    Sometimes you don't have all the information yet.  
    You can insert `NULL` as a placeholder for missing values.
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("C-4 · Insert with NULL placeholder")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE INSERT")

    sql_c4 = """
        INSERT INTO employees (emp_id, emp_name, department, salary, gender)
        VALUES (960, 'George', 'SALES', NULL, 'MALE');
    """
    print_sql(sql_c4)
    con.execute(sql_c4)

    run(con, "SELECT * FROM employees ORDER BY emp_id",
        title="AFTER INSERT — George added with NULL salary")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 🔄 Reset to original 10 rows before READ / UPDATE / DELETE

    The cells below rely on having exactly the original 10 employees.  
    We restore the table now.
    """)
    return


@app.cell
def _(con):
    # ── Restore original 10 rows ──────────────────────────────────────────
    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)
    con.execute("""
        CREATE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR,
            department VARCHAR,
            salary     INTEGER,
            gender     VARCHAR
        );
    """)
    con.execute("""
        INSERT INTO employees
        VALUES
            (100, 'Alex', 'SALES', 120000, 'MALE'),
            (200, 'Jeff', 'SALES', 140000, 'MALE'),
            (300, 'Rafa', 'BUSINESS', 150000, 'MALE'),
            (400, 'Susan', 'SALES', 150000, 'FMALE'),
            (500, 'Jen', 'BUSINESS', 160000, 'FEMALE'),
            (600, 'Barb', 'BUSINESS', 180000, 'FEMALE'),
            (700, 'Dara', 'AI', 190000, 'MALE'),
            (800, 'Venus', 'AI', 200000, 'FEMALE'),
            (900, 'Margie', 'SALES', 140000, 'FEMALE'),
            (910, 'Betty', 'SALES', 170000, 'FEMALE');
    """)
    print("✅ employees table restored to original 10 rows.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 📖 R — READ (SELECT)

    ## What is SELECT?

    `SELECT` is the most-used SQL statement. It **retrieves rows** from one or more tables.

    **Basic syntax:**
    ```sql
    SELECT column1, column2
    FROM   table_name
    WHERE  condition
    ORDER BY column1
    LIMIT  n;
    ```

    | Clause | Purpose |
    |--------|---------|
    | `SELECT` | Choose which columns to return |
    | `FROM` | Name the table(s) to read from |
    | `WHERE` | Filter rows by a condition |
    | `ORDER BY` | Sort the results |
    | `LIMIT` | Return only the first N rows |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-1 · Select all columns and all rows
    """)
    return


@app.cell
def _(con, run, section):
    section("R-1 · Select ALL columns and ALL rows")
    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """,
        title="All Employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-2 · Select specific columns
    """)
    return


@app.cell
def _(con, run, section):
    section("R-2 · Select specific columns")
    run(con,
        """
            SELECT
                emp_id,
                emp_name,
                salary
            FROM employees
            ORDER BY salary DESC;
        """,
        title="Employee Names & Salaries (highest first)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-3 · Filter with WHERE
    """)
    return


@app.cell
def _(con, run, section):
    section("R-3 · Filter with WHERE — SALES department only")
    run(con,
        """
            SELECT *
            FROM employees
            WHERE department = 'SALES'
            ORDER BY emp_id;
        """,
        title="SALES Department Employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-4 · Filter with WHERE + LIMIT
    """)
    return


@app.cell
def _(con, run, section):
    section("R-4 · Top-3 highest-paid employees")
    run(con,
        """
            SELECT
                emp_id,
                emp_name,
                department,
                salary
            FROM employees
            ORDER BY salary DESC
            LIMIT 3;
        """,
        title="Top-3 Earners")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📚 10 Basic SELECT Queries

    These queries use only `SELECT`, `FROM`, `WHERE`, `ORDER BY`, and `LIMIT` —  
    the building blocks every SQL developer uses every day.
    """)
    return


@app.cell
def _(con, run, section):
    section("Basic Q-1 · All female employees")
    run(con,
        """
            SELECT *
            FROM employees
            WHERE gender = 'FEMALE'
            ORDER BY emp_id;
        """,
        title="Female Employees")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-2 · Employees earning more than $150,000")
    run(con,
        """
            SELECT
                emp_name,
                department,
                salary
            FROM employees
            WHERE salary > 150000
            ORDER BY salary DESC;
        """,
        title="Salary > $150,000")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-3 · AI department employees")
    run(con,
        """
            SELECT *
            FROM employees
            WHERE department = 'AI'
            ORDER BY salary DESC;
        """,
        title="AI Department")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-4 · Employees sorted alphabetically by name")
    run(con,
        """
            SELECT
                emp_id,
                emp_name,
                department
            FROM employees
            ORDER BY emp_name ASC;
        """,
        title="Alphabetical by Name")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-5 · Bottom 3 earners")
    run(con,
        """
            SELECT
                emp_id,
                emp_name,
                salary
            FROM employees
            ORDER BY salary ASC
            LIMIT 3;
        """,
        title="Bottom-3 Earners")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-6 · BUSINESS female employees")
    run(con,
        """
            SELECT *
            FROM employees
            WHERE department = 'BUSINESS'
            AND gender = 'FEMALE'
            ORDER BY salary DESC;
        """,
        title="Business + Female")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-7 · Salary between $140,000 and $170,000")
    run(con,
        """
            SELECT
                emp_name,
                department,
                salary
            FROM employees
            WHERE salary BETWEEN 140000
            AND 170000
            ORDER BY salary;
        """,
        title="Salary $140K–$170K")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-8 · SALES or AI employees (OR condition)")
    run(con,
        """
            SELECT *
            FROM employees
            WHERE department IN ('SALES', 'AI')
            ORDER BY department, salary DESC;
        """,
        title="SALES or AI Department")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-9 · emp_id greater than 500, first 4 rows")
    run(con,
        """
            SELECT *
            FROM employees
            WHERE emp_id > 500
            ORDER BY emp_id
            LIMIT 4;
        """,
        title="emp_id > 500, top 4")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-10 · Employees whose name starts with a vowel")
    run(con,
        """
            SELECT
                emp_id,
                emp_name,
                department
            FROM employees
            WHERE emp_name LIKE 'A%'
            OR emp_name LIKE 'E%'
            OR emp_name LIKE 'I%'
            OR emp_name LIKE 'O%'
            OR emp_name LIKE 'U%'
            ORDER BY emp_name;
        """,
        title="Names Starting with a Vowel")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 10 GROUP BY Queries

    ### What is GROUP BY?

    `GROUP BY` **aggregates rows** that share the same value in one or more columns.  
    It is always used with **aggregate functions** such as:

    | Function | Meaning |
    |----------|---------|
    | `COUNT(*)` | Number of rows |
    | `SUM(col)` | Total value |
    | `AVG(col)` | Average value |
    | `MIN(col)` | Smallest value |
    | `MAX(col)` | Largest value |

    **`HAVING`** filters the *grouped* results (like WHERE but for aggregates).
    """)
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-1 · Employee count per department")
    run(con,
        """
            SELECT
                department,
                COUNT(*) AS num_employees
            FROM employees
            GROUP BY department
            ORDER BY num_employees DESC;
        """,
        title="Headcount by Department")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-2 · Average salary per department")
    run(con,
        """
            SELECT
                department,
                ROUND(AVG(salary), 0) AS avg_salary
            FROM employees
            GROUP BY department
            ORDER BY avg_salary DESC;
        """,
        title="Average Salary by Department")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-3 · Min and Max salary per department")
    run(con,
        """
            SELECT
                department,
                MIN(salary) AS min_salary,
                MAX(salary) AS max_salary
            FROM employees
            GROUP BY department
            ORDER BY department;
        """,
        title="Salary Range by Department")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-4 · Count by gender")
    run(con,
        """
            SELECT
                gender,
                COUNT(*) AS num_employees
            FROM employees
            GROUP BY gender
            ORDER BY num_employees DESC;
        """,
        title="Headcount by Gender")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-5 · Total payroll per department")
    run(con,
        """
            SELECT
                department,
                SUM(salary) AS total_payroll
            FROM employees
            GROUP BY department
            ORDER BY total_payroll DESC;
        """,
        title="Total Payroll by Department")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-6 · HAVING — departments with more than 2 employees")
    run(con,
        """
            SELECT
                department,
                COUNT(*) AS num_employees
            FROM employees
            GROUP BY department
            HAVING COUNT(*) > 2
            ORDER BY num_employees DESC;
        """,
        title="Departments with > 2 Employees")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-7 · HAVING — departments with avg salary > $160,000")
    run(con,
        """
            SELECT
                department,
                ROUND(AVG(salary), 0) AS avg_salary
            FROM employees
            GROUP BY department
            HAVING AVG(salary) > 160000
            ORDER BY avg_salary DESC;
        """,
        title="Departments: Avg Salary > $160K")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-8 · Gender count per department")
    run(con,
        """
            SELECT
                department,
                gender,
                COUNT(*) AS num_employees
            FROM employees
            GROUP BY department, gender
            ORDER BY department, gender;
        """,
        title="Gender Distribution per Department")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-9 · Top department by total payroll — LIMIT 1")
    run(con,
        """
            SELECT
                department,
                SUM(salary) AS total_payroll
            FROM employees
            GROUP BY department
            ORDER BY total_payroll DESC
            LIMIT 1;
        """,
        title="Highest-Payroll Department")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-10 · Salary statistics — overall summary")
    run(con,
        """
            SELECT
                COUNT(*) AS total_employees,
                MIN(salary) AS min_salary,
                MAX(salary) AS max_salary,
                ROUND(AVG(salary), 0) AS avg_salary,
                SUM(salary) AS total_payroll
            FROM employees;
        """,
        title="Overall Salary Statistics")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✏️ U — UPDATE

    ## What is UPDATE?

    `UPDATE` **modifies existing rows** in a table.

    **Syntax:**
    ```sql
    UPDATE table_name
    SET    column1 = new_value1,
           column2 = new_value2
    WHERE  condition;
    ```

    > ⚠️ **Always include a WHERE clause** unless you intend to update every single row.
    > Omitting WHERE will modify ALL rows!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-1 · Fix a typo — correct Susan's gender from FMALE to FEMALE
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("U-1 · Fix typo: Susan's gender FMALE → FEMALE")

    run(con,
        """
            SELECT *
            FROM employees
            WHERE emp_id = 400;
        """,
        title="BEFORE UPDATE — Susan")

    sql_u1 = """
    UPDATE employees
    SET    gender = 'FEMALE'
    WHERE  emp_id = 400
    """
    print_sql(sql_u1)
    con.execute(sql_u1)

    run(con,
        "SELECT * FROM employees WHERE emp_id = 400",
        title="AFTER UPDATE — Susan's gender corrected")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-2 · Give all SALES employees a 10% raise
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("U-2 · 10% raise for all SALES employees")

    run(con,
        """
            SELECT *
            FROM employees
            WHERE department = 'SALES'
            ORDER BY emp_id;
        """,
        title="BEFORE UPDATE — SALES employees")

    sql_u2 = """
        UPDATE employees
        SET salary = ROUND(salary * 1.10, 0)
        WHERE department = 'SALES';
    """
    print_sql(sql_u2)
    con.execute(sql_u2)

    run(con,
        "SELECT * FROM employees WHERE department = 'SALES' ORDER BY emp_id",
        title="AFTER UPDATE — SALES salaries +10%")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-3 · Transfer Dara from AI to BUSINESS
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("U-3 · Transfer Dara (700) from AI → BUSINESS")

    run(con,
        """
            SELECT *
            FROM employees
            WHERE emp_id = 700;
        """,
        title="BEFORE UPDATE — Dara")

    sql_u3 = """
    UPDATE employees
    SET    department = 'BUSINESS'
    WHERE  emp_id = 700
    """
    print_sql(sql_u3)
    con.execute(sql_u3)

    run(con,
        "SELECT * FROM employees WHERE emp_id = 700",
        title="AFTER UPDATE — Dara now in BUSINESS")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-4 · Cap salaries above $180,000 at exactly $180,000
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("U-4 · Cap all salaries above $180K to exactly $180K")

    run(con,
        """
            SELECT *
            FROM employees
            ORDER BY salary DESC;
        """,
        title="BEFORE UPDATE")

    sql_u4 = """
    UPDATE employees
    SET    salary = 180000
    WHERE  salary > 180000
    """
    print_sql(sql_u4)
    con.execute(sql_u4)

    run(con,
        "SELECT * FROM employees ORDER BY salary DESC",
        title="AFTER UPDATE — salaries capped at $180K")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 🔄 Restore again before DELETE examples
    """)
    return


@app.cell
def _(con):
    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)
    con.execute("""
        CREATE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR,
            department VARCHAR,
            salary     INTEGER,
            gender     VARCHAR
        );
    """)
    con.execute("""
        INSERT INTO employees
        VALUES
            (100, 'Alex', 'SALES', 120000, 'MALE'),
            (200, 'Jeff', 'SALES', 140000, 'MALE'),
            (300, 'Rafa', 'BUSINESS', 150000, 'MALE'),
            (400, 'Susan', 'SALES', 150000, 'FMALE'),
            (500, 'Jen', 'BUSINESS', 160000, 'FEMALE'),
            (600, 'Barb', 'BUSINESS', 180000, 'FEMALE'),
            (700, 'Dara', 'AI', 190000, 'MALE'),
            (800, 'Venus', 'AI', 200000, 'FEMALE'),
            (900, 'Margie', 'SALES', 140000, 'FEMALE'),
            (910, 'Betty', 'SALES', 170000, 'FEMALE');
    """)
    print("✅ employees table restored to original 10 rows.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 🗑️ D — DELETE

    ## What is DELETE?

    `DELETE FROM` **removes one or more rows** from a table.

    **Syntax:**
    ```sql
    DELETE FROM table_name
    WHERE       condition;
    ```

    > ⚠️ **Always include a WHERE clause** unless you want to erase the entire table.  
    > `DELETE FROM employees;` (no WHERE) removes every row!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-1 · Delete a single employee by ID
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("D-1 · Delete employee 100 (Alex)")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE DELETE")

    sql_d1 = """
        DELETE
        FROM employees
        WHERE emp_id = 100;
    """
    print_sql(sql_d1)
    con.execute(sql_d1)

    run(con, "SELECT * FROM employees ORDER BY emp_id",
        title="AFTER DELETE — Alex (100) removed")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-2 · Delete all employees in AI department
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("D-2 · Delete all AI department employees")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE DELETE")

    sql_d2 = """
        DELETE
        FROM employees
        WHERE department = 'AI';
    """
    print_sql(sql_d2)
    con.execute(sql_d2)

    run(con, "SELECT * FROM employees ORDER BY emp_id",
        title="AFTER DELETE — AI department removed")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-3 · Delete employees earning below $150,000
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("D-3 · Delete employees with salary < $150,000")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE DELETE")

    sql_d3 = """
        DELETE
        FROM employees
        WHERE salary < 150000;
    """
    print_sql(sql_d3)
    con.execute(sql_d3)

    run(con, "SELECT * FROM employees ORDER BY emp_id",
        title="AFTER DELETE — low earners removed")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-4 · Delete all remaining rows (TRUNCATE-style) — careful!
    """)
    return


@app.cell
def _(con, print_sql, run, section):
    section("D-4 · Delete ALL remaining rows")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE DELETE")

    sql_d4 = """
        DELETE
        FROM employees;
    """
    print_sql(sql_d4)
    con.execute(sql_d4)

    run(con, """
        SELECT *
        FROM employees;
    """,
        title="AFTER DELETE — table is empty")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 🔄 Final Restore — for Analytics & Plots
    """)
    return


@app.cell
def _(con):
    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)
    con.execute("""
        CREATE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR,
            department VARCHAR,
            salary     INTEGER,
            gender     VARCHAR
        );
    """)
    con.execute("""
        INSERT INTO employees
        VALUES
            (100, 'Alex', 'SALES', 120000, 'MALE'),
            (200, 'Jeff', 'SALES', 140000, 'MALE'),
            (300, 'Rafa', 'BUSINESS', 150000, 'MALE'),
            (400, 'Susan', 'SALES', 150000, 'FEMALE'),
            (500, 'Jen', 'BUSINESS', 160000, 'FEMALE'),
            (600, 'Barb', 'BUSINESS', 180000, 'FEMALE'),
            (700, 'Dara', 'AI', 190000, 'MALE'),
            (800, 'Venus', 'AI', 200000, 'FEMALE'),
            (900, 'Margie', 'SALES', 140000, 'FEMALE'),
            (910, 'Betty', 'SALES', 170000, 'FEMALE');
    """)
    print("✅ employees restored (Susan's gender corrected to FEMALE).")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 📊 Analytics & Visualisations

    Now we combine SQL aggregations with plots to gain **data insights**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 1 · Gender Distribution (% Male vs Female)
    """)
    return


@app.cell
def _(con, plot_pie, query, run, section):
    section("Analytics · Gender Distribution")

    df_gender = query(con,
        """
            SELECT
                gender,
                COUNT(*) AS count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
            FROM employees
            GROUP BY gender
            ORDER BY COUNT DESC;
        """,
        title="Gender Count & Percentage")

    plot_pie(df_gender, label_col='gender', value_col='count',
             title="Gender Distribution — All Employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 2 · Headcount per Department
    """)
    return


@app.cell
def _(con, plot_pie, plot_vbar, query, run, section):
    section("Analytics · Headcount per Department")

    df_dept = query(con,
        """
            SELECT
                department,
                COUNT(*) AS num_employees
            FROM employees
            GROUP BY department
            ORDER BY num_employees DESC;
        """,
        title="Employees per Department")

    plot_vbar(df_dept, x_col='department', y_col='num_employees',
              title="Headcount by Department",
              ylabel="Number of Employees",
              color_col='department')

    plot_pie(df_dept, label_col='department', value_col='num_employees',
             title="Department Share (%)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 3 · Highest and Lowest Salaries (Overall)
    """)
    return


@app.cell
def _(con, plot_hbar, query, run, section):
    section("Analytics · All Salaries Ranked")

    df_sal = query(con,
        """
            SELECT
                emp_name,
                department,
                salary
            FROM employees
            ORDER BY salary DESC;
        """,
        title="All Employees Ranked by Salary")

    plot_hbar(df_sal, x_col='salary', y_col='emp_name',
              title="Individual Salaries (Highest → Lowest)",
              xlabel="Annual Salary (USD)",
              color_col='department')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 4 · Min & Max Salary per Department
    """)
    return


@app.cell
def _(con, plot_salary_range, query, run, section):
    section("Analytics · Salary Range per Department")

    df_range = query(con,
        """
            SELECT
                department,
                MIN(salary) AS min_salary,
                MAX(salary) AS max_salary
            FROM employees
            GROUP BY department
            ORDER BY department;
        """,
        title="Min & Max Salary per Department")

    plot_salary_range(df_range, dept_col='department',
                      min_col='min_salary', max_col='max_salary',
                      title="Salary Range (Min vs Max) per Department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 5 · Average Salary per Department
    """)
    return


@app.cell
def _(con, plot_vbar, query, run, section):
    section("Analytics · Average Salary per Department")

    df_avg = query(con,
        """
            SELECT
                department,
                ROUND(AVG(salary), 0) AS avg_salary
            FROM employees
            GROUP BY department
            ORDER BY avg_salary DESC;
        """,
        title="Average Salary by Department")

    plot_vbar(df_avg, x_col='department', y_col='avg_salary',
              title="Average Annual Salary by Department",
              ylabel="Average Salary (USD)",
              color_col='department')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ✅ Summary

    Congratulations! You have completed the CRUD walkthrough. Here's what you learned:

    | Operation | Statement | Examples Covered |
    |-----------|-----------|------------------|
    | **Create** | `INSERT INTO` | Single row, multi-row, INSERT-SELECT, NULL |
    | **Read** | `SELECT` | All rows, specific cols, WHERE, ORDER BY, LIMIT, GROUP BY, HAVING |
    | **Update** | `UPDATE … SET` | Fix typo, bulk raise, transfer dept, salary cap |
    | **Delete** | `DELETE FROM` | By ID, by dept, by condition, truncate all |

    You also built **analytics queries** with `GROUP BY`, `HAVING`, aggregate functions, and created **5 visualisations** using DuckDB result sets.

    > 💡 **Next steps:** Try modifying the SQL in any cell. Change the WHERE conditions, add new employees, or experiment with different salary thresholds. DuckDB is fast — every query is instant!
    """)
    return


if __name__ == "__main__":
    app.run()
