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

    **DuckDB** is a fast, lightweight, *in-process* SQL database engine — meaning it runs entirely inside your Python program with no separate server needed.

    Key advantages:
    - ✅ Zero configuration — no server to install or start
    - ✅ Full SQL support (SELECT, INSERT, UPDATE, DELETE, GROUP BY, …)
    - ✅ Reads CSV files directly
    - ✅ Integrates seamlessly with pandas DataFrames

    ---

    ## What is CRUD?

    | Letter | Operation | SQL Statement | What it does |
    |--------|-----------|---------------|--------------|
    | **C** | **Create** | `INSERT INTO` | Adds new rows to a table |
    | **R** | **Read**   | `SELECT`      | Retrieves / queries rows |
    | **U** | **Update** | `UPDATE … SET`| Modifies existing rows |
    | **D** | **Delete** | `DELETE FROM` | Removes rows from a table |

    ---

    ## Two helper functions used in every cell

    | Function | Use for | What it does |
    |----------|---------|--------------|
    | `run(con, sql, title)` | **SELECT** | Prints formatted SQL → runs it → shows result table |
    | `execute_sql(con, sql)` | **INSERT / UPDATE / DELETE** | Prints formatted SQL → executes it (no rows returned) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📦 Setup

    `crud_helpers.py` (same folder) holds all display, tabulation, and plotting code — **you don't need to read or touch it**.  
    A fresh DuckDB in-memory connection is created here, so the notebook is always safe to **Restart & Run All**.

    > `sys.path.insert(...)` tells Python where to find `crud_helpers.py` — it adds this notebook's own folder to Python's search path so the import works no matter where Jupyter was launched from.
    """)
    return


@app.cell
def _():
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))

    import duckdb
    from crud_helpers import run, query, execute_sql, section, \
        plot_hbar, plot_vbar, plot_pie, plot_salary_range

    con = duckdb.connect()   # fresh in-memory database every run
    print("✅ DuckDB", duckdb.__version__, "ready.")
    return (con, execute_sql, plot_hbar, plot_pie, plot_salary_range, plot_vbar, query, run, section)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🗂️ Create Tables

    ### Method A — `employees` via INSERT

    | Column | Type | Description |
    |--------|------|-------------|
    | `emp_id` | INTEGER | Unique employee number |
    | `emp_name` | VARCHAR | First name |
    | `department` | VARCHAR | SALES / BUSINESS / AI |
    | `salary` | INTEGER | Annual salary in USD |
    | `gender` | VARCHAR | MALE / FEMALE |
    """)
    return


@app.cell
def _(con, run, section):
    section("""
        CREATE employees TABLE via INSERT;
    """)

    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)
    con.execute("""
        CREATE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR,
            department VARCHAR,
            salary     INTEGER,
            gender     VARCHAR,
            image_url  VARCHAR
        );
    """)
    con.execute("""
        INSERT INTO employees
        VALUES
            (100, 'Alex', 'SALES', 120000, 'MALE', 'https://ui-avatars.com/api/?name=Alex&size=40&background=4C72B0&color=fff&bold=true'),
            (200, 'Jeff', 'SALES', 140000, 'MALE', 'https://ui-avatars.com/api/?name=Jeff&size=40&background=55A868&color=fff&bold=true'),
            (300, 'Rafa', 'BUSINESS', 150000, 'MALE', 'https://ui-avatars.com/api/?name=Rafa&size=40&background=C44E52&color=fff&bold=true'),
            (400, 'Susan', 'SALES', 150000, 'FMALE', 'https://ui-avatars.com/api/?name=Susan&size=40&background=8172B2&color=fff&bold=true'),
            (500, 'Jen', 'BUSINESS', 160000, 'FEMALE', 'https://ui-avatars.com/api/?name=Jen&size=40&background=E58606&color=fff&bold=true'),
            (600, 'Barb', 'BUSINESS', 180000, 'FEMALE', 'https://ui-avatars.com/api/?name=Barb&size=40&background=937860&color=fff&bold=true'),
            (700, 'Dara', 'AI', 190000, 'MALE', 'https://ui-avatars.com/api/?name=Dara&size=40&background=DA8BC3&color=fff&bold=true'),
            (800, 'Venus', 'AI', 200000, 'FEMALE', 'https://ui-avatars.com/api/?name=Venus&size=40&background=CCB974&color=fff&bold=true'),
            (900, 'Margie', 'SALES', 140000, 'FEMALE', 'https://ui-avatars.com/api/?name=Margie&size=40&background=64B5CD&color=fff&bold=true'),
            (910, 'Betty', 'SALES', 170000, 'FEMALE', 'https://ui-avatars.com/api/?name=Betty&size=40&background=4878CF&color=fff&bold=true');
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
    ### Method B — `employees_backup` loaded from CSV

    DuckDB reads CSV files directly with `read_csv_auto()` — no schema needed.  
    This backup holds the same 10 rows and is never modified.
    """)
    return


@app.cell
def _(con, run, section):
    section("""
        CREATE employees_backup
        FROM CSV;
    """)

    con.execute("""
        DROP TABLE IF EXISTS employees_backup;
    """)
    con.execute("""
        CREATE TABLE employees_backup AS
        SELECT *
        FROM read_csv_auto('data/employees.csv');
    """)

    run(con, """
        SELECT *
        FROM employees_backup
        ORDER BY emp_id;
    """,
        title="employees_backup — loaded from CSV")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ C — CREATE (INSERT)

    ## What is INSERT?

    Adds one or more new rows to a table.

    ```sql
    INSERT INTO table_name (col1, col2, ...)
    VALUES (val1, val2, ...);
    ```

    Each example: **BEFORE** → SQL → **AFTER**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-1 · Insert a single new employee
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("C-1 · Insert a single new employee")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE INSERT")

    execute_sql(con, """
        INSERT INTO employees (emp_id, emp_name, department, salary, gender, image_url)
        VALUES (920, 'Carlos', 'AI', 210000, 'MALE', 'https://ui-avatars.com/api/?name=Carlos&size=40&background=2ecc71&color=fff&bold=true');
    """)

    run(con, "SELECT * FROM employees ORDER BY emp_id", title="AFTER INSERT — Carlos added")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-2 · Insert multiple employees in one statement
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("C-2 · Insert multiple employees in one statement")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE INSERT")

    execute_sql(con, """
        INSERT INTO employees (emp_id, emp_name, department, salary, gender, image_url)
        VALUES
            (930, 'Diana', 'BUSINESS', 155000, 'FEMALE', 'https://ui-avatars.com/api/?name=Diana&size=40&background=e74c3c&color=fff&bold=true'),
            (940, 'Ethan', 'AI', 195000, 'MALE', 'https://ui-avatars.com/api/?name=Ethan&size=40&background=3498db&color=fff&bold=true');
    """)

    run(con, "SELECT * FROM employees ORDER BY emp_id", title="AFTER INSERT — Diana & Ethan added")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-3 · INSERT … SELECT — derive a new row from the backup table
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("C-3 · INSERT … SELECT — derive a row from backup")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE INSERT")

    execute_sql(con, """
        INSERT INTO employees
        SELECT
            950 AS emp_id,
            'Fiona' AS emp_name,
            department,
            salary + 5000 AS salary,
            'FEMALE' AS gender,
            'https://ui-avatars.com/api/?name=Fiona&size=40&background=9b59b6&color=fff&bold=true' AS image_url
        FROM employees_backup
        WHERE emp_id = 700;
    """)

    run(con, "SELECT * FROM employees ORDER BY emp_id", title="AFTER INSERT — Fiona added")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C-4 · Insert with NULL (placeholder for unknown data)
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("C-4 · Insert with NULL salary placeholder")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE INSERT")

    execute_sql(con, """
        INSERT INTO employees (emp_id, emp_name, department, salary, gender, image_url)
        VALUES (960, 'George', 'SALES', NULL, 'MALE', 'https://ui-avatars.com/api/?name=George&size=40&background=1abc9c&color=fff&bold=true');
    """)

    run(con, "SELECT * FROM employees ORDER BY emp_id", title="AFTER INSERT — George added (NULL salary)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🔄 Restore to original 10 rows
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
            gender     VARCHAR,
            image_url  VARCHAR
        );
    """)
    con.execute("""
        INSERT INTO employees
        VALUES
            (100, 'Alex', 'SALES', 120000, 'MALE', 'https://ui-avatars.com/api/?name=Alex&size=40&background=4C72B0&color=fff&bold=true'),
            (200, 'Jeff', 'SALES', 140000, 'MALE', 'https://ui-avatars.com/api/?name=Jeff&size=40&background=55A868&color=fff&bold=true'),
            (300, 'Rafa', 'BUSINESS', 150000, 'MALE', 'https://ui-avatars.com/api/?name=Rafa&size=40&background=C44E52&color=fff&bold=true'),
            (400, 'Susan', 'SALES', 150000, 'FMALE', 'https://ui-avatars.com/api/?name=Susan&size=40&background=8172B2&color=fff&bold=true'),
            (500, 'Jen', 'BUSINESS', 160000, 'FEMALE', 'https://ui-avatars.com/api/?name=Jen&size=40&background=E58606&color=fff&bold=true'),
            (600, 'Barb', 'BUSINESS', 180000, 'FEMALE', 'https://ui-avatars.com/api/?name=Barb&size=40&background=937860&color=fff&bold=true'),
            (700, 'Dara', 'AI', 190000, 'MALE', 'https://ui-avatars.com/api/?name=Dara&size=40&background=DA8BC3&color=fff&bold=true'),
            (800, 'Venus', 'AI', 200000, 'FEMALE', 'https://ui-avatars.com/api/?name=Venus&size=40&background=CCB974&color=fff&bold=true'),
            (900, 'Margie', 'SALES', 140000, 'FEMALE', 'https://ui-avatars.com/api/?name=Margie&size=40&background=64B5CD&color=fff&bold=true'),
            (910, 'Betty', 'SALES', 170000, 'FEMALE', 'https://ui-avatars.com/api/?name=Betty&size=40&background=4878CF&color=fff&bold=true');
    """)
    print("✅ employees restored to original 10 rows.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 📖 R — READ (SELECT)

    ## What is SELECT?

    Retrieves rows from a table. The most-used SQL statement.

    ```sql
    SELECT column1, column2
    FROM   table_name
    WHERE  condition
    ORDER BY column1
    LIMIT  n;
    ```
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
    """, title="All Employees")
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
    run(con, """
    SELECT emp_id,
           emp_name,
           salary
    FROM   employees
    ORDER BY salary DESC
    """, title="Employee Names & Salaries (highest first)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-3 · Filter rows with WHERE
    """)
    return


@app.cell
def _(con, run, section):
    section("R-3 · WHERE — SALES department only")
    run(con, """
        SELECT *
        FROM employees
        WHERE department = 'SALES'
        ORDER BY emp_id;
    """, title="SALES Department Employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-4 · Top-3 highest-paid employees
    """)
    return


@app.cell
def _(con, run, section):
    section("R-4 · Top-3 highest-paid employees")
    run(con, """
    SELECT emp_id,
           emp_name,
           department,
           salary
    FROM   employees
    ORDER BY salary DESC
    LIMIT  3
    """, title="Top-3 Earners")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📚 10 Basic SELECT Queries
    """)
    return


@app.cell
def _(con, run, section):
    section("Basic Q-1 · All female employees")
    run(con, """
        SELECT *
        FROM employees
        WHERE gender = 'FEMALE'
        ORDER BY emp_id;
    """, title="Female Employees")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-2 · Salary > $150,000")
    run(con, """
    SELECT emp_name,
           department,
           salary
    FROM   employees
    WHERE  salary > 150000
    ORDER BY salary DESC
    """, title="Salary > $150,000")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-3 · AI department employees")
    run(con, """
        SELECT *
        FROM employees
        WHERE department = 'AI'
        ORDER BY salary DESC;
    """, title="AI Department")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-4 · All employees sorted alphabetically")
    run(con, """
    SELECT emp_id,
           emp_name,
           department
    FROM   employees
    ORDER BY emp_name ASC
    """, title="Alphabetical by Name")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-5 · Bottom-3 earners")
    run(con, """
    SELECT emp_id,
           emp_name,
           salary
    FROM   employees
    ORDER BY salary ASC
    LIMIT  3
    """, title="Bottom-3 Earners")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-6 · BUSINESS female employees")
    run(con, """
        SELECT *
        FROM employees
        WHERE department = 'BUSINESS'
        AND gender = 'FEMALE'
        ORDER BY salary DESC;
    """, title="Business + Female")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-7 · Salary BETWEEN $140K and $170K")
    run(con, """
    SELECT emp_name,
           department,
           salary
    FROM   employees
    WHERE  salary BETWEEN 140000 AND 170000
    ORDER BY salary
    """, title="Salary $140K–$170K")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-8 · SALES or AI employees (IN operator)")
    run(con, """
        SELECT *
        FROM employees
        WHERE department IN ('SALES', 'AI')
        ORDER BY department, salary DESC;
    """, title="SALES or AI Department")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-9 · emp_id > 500, first 4 rows")
    run(con, """
        SELECT *
        FROM employees
        WHERE emp_id > 500
        ORDER BY emp_id
        LIMIT 4;
    """, title="emp_id > 500, top 4")
    return


@app.cell
def _(con, run, section):
    section("Basic Q-10 · Names starting with a vowel (LIKE)")
    run(con, """
    SELECT emp_id,
           emp_name,
           department
    FROM   employees
    WHERE  emp_name LIKE 'A%'
        OR emp_name LIKE 'E%'
        OR emp_name LIKE 'I%'
        OR emp_name LIKE 'O%'
        OR emp_name LIKE 'U%'
    ORDER BY emp_name
    """, title="Names Starting with a Vowel")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 10 GROUP BY Queries

    ### What is GROUP BY?

    * Aggregates rows sharing the same column value. 
    * Always used with aggregate functions:

    `COUNT(*)`, `SUM()`, `AVG()`, `MIN()`, `MAX()`.

    `HAVING` filters *grouped* results — like `WHERE` but applied after aggregation.
    """)
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-1 · Employee count per department")
    run(con, """
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
    run(con, """
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
    run(con, """
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
    section("GROUP BY Q-4 · Headcount by gender")
    run(con, """
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
    run(con, """
        SELECT
            department,
            SUM(salary) AS total_payroll
        FROM employees
        GROUP BY department
        ORDER BY total_payroll DESC;
    """, title="Total Payroll by Department")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-6 · HAVING — departments with > 2 employees")
    run(con, """
        SELECT
            department,
            COUNT(*) AS num_employees
        FROM employees
        GROUP BY department
        HAVING COUNT(*) > 2
        ORDER BY num_employees DESC;
    """, title="Departments with > 2 Employees")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-7 · HAVING — avg salary > $160,000")
    run(con, """
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department
        HAVING AVG(salary) > 160000
        ORDER BY avg_salary DESC;
    """, title="Avg Salary > $160K")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-8 · Gender count per department")
    run(con, """
        SELECT
            department,
            gender,
            COUNT(*) AS num_employees
        FROM employees
        GROUP BY department, gender
        ORDER BY department, gender;
    """, title="Gender Distribution per Department")
    return


@app.cell
def _(con, run, section):
    section("GROUP BY Q-9 · Top department by total payroll")
    run(con, """
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
    section("GROUP BY Q-10 · Overall salary statistics")
    run(con, """
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

    Modifies existing rows in a table.

    ```sql
    UPDATE table_name
    SET    column = new_value
    WHERE  condition;
    ```

    > ⚠️ **Always include WHERE** — omitting it updates *every* row!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-1 · Fix a typo — Susan's gender `FMALE` → `FEMALE`
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("U-1 · Fix typo: Susan's gender FMALE → FEMALE")

    run(con, """
        SELECT *
        FROM employees
        WHERE emp_id = 400;
    """,
        title="BEFORE UPDATE — Susan")

    execute_sql(con, """
    UPDATE employees
    SET    gender = 'FEMALE'
    WHERE  emp_id = 400
    """)

    run(con, "SELECT * FROM employees WHERE emp_id = 400",
        title="AFTER UPDATE — Susan corrected")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-2 · 10% raise for all SALES employees
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("U-2 · 10% raise for all SALES employees")

    run(con, """
        SELECT *
        FROM employees
        WHERE department = 'SALES'
        ORDER BY emp_id;
    """,
        title="BEFORE UPDATE — SALES")

    execute_sql(con, """
        UPDATE employees
        SET salary = ROUND(salary * 1.10, 0)
        WHERE department = 'SALES';
    """)

    run(con, "SELECT * FROM employees WHERE department = 'SALES' ORDER BY emp_id",
        title="AFTER UPDATE — SALES salaries +10%")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-3 · Transfer Dara from AI to BUSINESS
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("U-3 · Transfer Dara (700) from AI → BUSINESS")

    run(con, """
        SELECT *
        FROM employees
        WHERE emp_id = 700;
    """,
        title="BEFORE UPDATE — Dara")

    execute_sql(con, """
    UPDATE employees
    SET    department = 'BUSINESS'
    WHERE  emp_id = 700
    """)

    run(con, "SELECT * FROM employees WHERE emp_id = 700",
        title="AFTER UPDATE — Dara in BUSINESS")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U-4 · Cap all salaries above $180,000
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("U-4 · Cap salaries above $180K to exactly $180K")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY salary DESC;
    """,
        title="BEFORE UPDATE")

    execute_sql(con, """
    UPDATE employees
    SET    salary = 180000
    WHERE  salary > 180000
    """)

    run(con, "SELECT * FROM employees ORDER BY salary DESC",
        title="AFTER UPDATE — salaries capped at $180K")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🔄 Restore before DELETE
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
            gender     VARCHAR,
            image_url  VARCHAR
        );
    """)
    con.execute("""
        INSERT INTO employees
        VALUES
            (100, 'Alex', 'SALES', 120000, 'MALE', 'https://ui-avatars.com/api/?name=Alex&size=40&background=4C72B0&color=fff&bold=true'),
            (200, 'Jeff', 'SALES', 140000, 'MALE', 'https://ui-avatars.com/api/?name=Jeff&size=40&background=55A868&color=fff&bold=true'),
            (300, 'Rafa', 'BUSINESS', 150000, 'MALE', 'https://ui-avatars.com/api/?name=Rafa&size=40&background=C44E52&color=fff&bold=true'),
            (400, 'Susan', 'SALES', 150000, 'FMALE', 'https://ui-avatars.com/api/?name=Susan&size=40&background=8172B2&color=fff&bold=true'),
            (500, 'Jen', 'BUSINESS', 160000, 'FEMALE', 'https://ui-avatars.com/api/?name=Jen&size=40&background=E58606&color=fff&bold=true'),
            (600, 'Barb', 'BUSINESS', 180000, 'FEMALE', 'https://ui-avatars.com/api/?name=Barb&size=40&background=937860&color=fff&bold=true'),
            (700, 'Dara', 'AI', 190000, 'MALE', 'https://ui-avatars.com/api/?name=Dara&size=40&background=DA8BC3&color=fff&bold=true'),
            (800, 'Venus', 'AI', 200000, 'FEMALE', 'https://ui-avatars.com/api/?name=Venus&size=40&background=CCB974&color=fff&bold=true'),
            (900, 'Margie', 'SALES', 140000, 'FEMALE', 'https://ui-avatars.com/api/?name=Margie&size=40&background=64B5CD&color=fff&bold=true'),
            (910, 'Betty', 'SALES', 170000, 'FEMALE', 'https://ui-avatars.com/api/?name=Betty&size=40&background=4878CF&color=fff&bold=true');
    """)
    print("✅ employees restored to original 10 rows.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 🗑️ D — DELETE

    ## What is DELETE?

    Removes rows from a table.

    ```sql
    DELETE FROM table_name
    WHERE       condition;
    ```

    > ⚠️ **Always include WHERE** — `DELETE FROM employees;` with no WHERE erases the entire table!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-1 · Delete a single employee by ID
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("D-1 · Delete employee 100 (Alex)")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE DELETE")

    execute_sql(con, """
        DELETE
        FROM employees
        WHERE emp_id = 100;
    """)

    run(con, "SELECT * FROM employees ORDER BY emp_id", title="AFTER DELETE — Alex removed")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-2 · Delete all employees in a department
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("D-2 · Delete all AI department employees")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE DELETE")

    execute_sql(con, """
        DELETE
        FROM employees
        WHERE department = 'AI';
    """)

    run(con, "SELECT * FROM employees ORDER BY emp_id", title="AFTER DELETE — AI removed")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-3 · Delete rows matching a condition
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("D-3 · Delete employees with salary < $150,000")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE DELETE")

    execute_sql(con, """
        DELETE
        FROM employees
        WHERE salary < 150000;
    """)

    run(con, "SELECT * FROM employees ORDER BY emp_id", title="AFTER DELETE — low earners removed")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D-4 · Delete ALL rows (no WHERE — use with caution!)
    """)
    return


@app.cell
def _(con, execute_sql, run, section):
    section("D-4 · Delete ALL rows — no WHERE clause")

    run(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="BEFORE DELETE")

    execute_sql(con, """
        DELETE
        FROM employees;
    """)

    run(con, """
        SELECT *
        FROM employees;
    """, title="AFTER DELETE — table is empty")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🔄 Final Restore — for Analytics
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
            gender     VARCHAR,
            image_url  VARCHAR
        );
    """)
    con.execute("""
        INSERT INTO employees
        VALUES
            (100, 'Alex', 'SALES', 120000, 'MALE', 'https://ui-avatars.com/api/?name=Alex&size=40&background=4C72B0&color=fff&bold=true'),
            (200, 'Jeff', 'SALES', 140000, 'MALE', 'https://ui-avatars.com/api/?name=Jeff&size=40&background=55A868&color=fff&bold=true'),
            (300, 'Rafa', 'BUSINESS', 150000, 'MALE', 'https://ui-avatars.com/api/?name=Rafa&size=40&background=C44E52&color=fff&bold=true'),
            (400, 'Susan', 'SALES', 150000, 'FEMALE', 'https://ui-avatars.com/api/?name=Susan&size=40&background=8172B2&color=fff&bold=true'),
            (500, 'Jen', 'BUSINESS', 160000, 'FEMALE', 'https://ui-avatars.com/api/?name=Jen&size=40&background=E58606&color=fff&bold=true'),
            (600, 'Barb', 'BUSINESS', 180000, 'FEMALE', 'https://ui-avatars.com/api/?name=Barb&size=40&background=937860&color=fff&bold=true'),
            (700, 'Dara', 'AI', 190000, 'MALE', 'https://ui-avatars.com/api/?name=Dara&size=40&background=DA8BC3&color=fff&bold=true'),
            (800, 'Venus', 'AI', 200000, 'FEMALE', 'https://ui-avatars.com/api/?name=Venus&size=40&background=CCB974&color=fff&bold=true'),
            (900, 'Margie', 'SALES', 140000, 'FEMALE', 'https://ui-avatars.com/api/?name=Margie&size=40&background=64B5CD&color=fff&bold=true'),
            (910, 'Betty', 'SALES', 170000, 'FEMALE', 'https://ui-avatars.com/api/?name=Betty&size=40&background=4878CF&color=fff&bold=true');
    """)
    print("✅ employees restored (Susan corrected to FEMALE).")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 📊 Analytics & Visualisations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 1 · Gender Distribution
    """)
    return


@app.cell
def _(con, plot_pie, query, section):
    section("Analytics · Gender Distribution")
    df_gender = query(con, """
        SELECT
            gender,
            COUNT(*) AS count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
        FROM employees
        GROUP BY gender
        ORDER BY COUNT DESC;
    """, title="Gender Count & Percentage")

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
def _(con, plot_pie, plot_vbar, query, section):
    section("Analytics · Headcount per Department")
    df_dept = query(con, """
        SELECT
            department,
            COUNT(*) AS num_employees
        FROM employees
        GROUP BY department
        ORDER BY num_employees DESC;
    """, title="Employees per Department")

    plot_vbar(df_dept, x_col='department', y_col='num_employees',
              title="Headcount by Department", ylabel="Number of Employees",
              color_col='department')

    plot_pie(df_dept, label_col='department', value_col='num_employees',
             title="Department Share (%)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 3 · All Salaries Ranked
    """)
    return


@app.cell
def _(con, plot_hbar, query, section):
    section("Analytics · All Salaries Ranked")
    df_sal = query(con, """
    SELECT emp_name,
           department,
           salary
    FROM   employees
    ORDER BY salary DESC
    """, title="All Employees Ranked by Salary")

    plot_hbar(df_sal, x_col='salary', y_col='emp_name',
              title="Individual Salaries (Highest → Lowest)",
              xlabel="Annual Salary (USD)", color_col='department')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 4 · Salary Range per Department
    """)
    return


@app.cell
def _(con, plot_salary_range, query, section):
    section("Analytics · Salary Range per Department")
    df_range = query(con, """
        SELECT
            department,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY department
        ORDER BY department;
    """, title="Min & Max Salary per Department")

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
def _(con, plot_vbar, query, section):
    section("Analytics · Average Salary per Department")
    df_avg = query(con, """
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
    """, title="Average Salary by Department")

    plot_vbar(df_avg, x_col='department', y_col='avg_salary',
              title="Average Annual Salary by Department",
              ylabel="Average Salary (USD)", color_col='department')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ✅ Summary

    | Operation | Statement | Examples Covered |
    |-----------|-----------|------------------|
    | **Create** | `INSERT INTO` | Single row, multi-row, INSERT-SELECT, NULL |
    | **Read** | `SELECT` | All rows, specific cols, WHERE, ORDER BY, LIMIT, GROUP BY, HAVING |
    | **Update** | `UPDATE … SET` | Fix typo, bulk raise, transfer dept, salary cap |
    | **Delete** | `DELETE FROM` | By ID, by dept, by condition, full wipe |

    > 💡 Modify any cell's SQL and re-run — DuckDB is instant!
    """)
    return


if __name__ == "__main__":
    app.run()
