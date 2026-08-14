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
    # CRUD Operations with DuckDB & Marimo
    ## Four worked examples of each operation

    ---

    ### What is CRUD?

    **CRUD** stands for the four fundamental operations used to manage data in a database:

    | Letter | Operation | SQL Command | Description |
    |--------|-----------|-------------|-------------|
    | **C** | **Create** | `INSERT INTO` | Add new records to a table |
    | **R** | **Read**   | `SELECT`      | Retrieve / query existing records |
    | **U** | **Update** | `UPDATE`      | Modify existing records |
    | **D** | **Delete** | `DELETE`      | Remove records from a table |

    ### What is DuckDB?

    **DuckDB** is an in-process SQL database — think of it as *SQLite for analytics*.  
    It runs entirely inside your Python process (no server needed!) and is optimised for analytical queries.

    ### How SQL is written here

    Every query in this notebook lives in its own **Marimo SQL cell**, so what you read  
    is plain SQL — no Python wrapping around it.

    ### What You Will Learn

    1. How to **create** tables and insert data  
    2. How to **read** data with various query patterns  
    3. How to **update** existing records  
    4. How to **delete** records  
    5. Basic and advanced SQL queries (SELECT, WHERE, GROUP BY, HAVING)  
    6. Data visualisation with plots

    ---
    > **Tip:** This notebook is *bullet-proof* — you can run it from top to bottom  
    > as many times as you like. Every section cleans up after itself first.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 0 · Environment Setup
    Install the required packages (runs only if not already installed).
    """)
    return


@app.cell
def _():
    # ── Install packages (idempotent) ──────────────────────────
    import subprocess, importlib, sys as _sys

    required = ["duckdb", "pandas", "matplotlib"]

    for pkg in required:
        try:
            importlib.import_module(pkg)
        except ImportError:
            subprocess.check_call(
                [_sys.executable, "-m", "pip", "install",
                 pkg.replace("_", "-"), "-q"])

    print("All packages ready.")
    import duckdb
    return (duckdb,)


@app.cell
def _():
    # ── Import display / plot helpers (external module) ────────
    # These live in  display_utils.py  so the notebook stays clean.
    import sys as _sys, os
    _sys.path.insert(0, os.path.dirname(os.path.abspath("__file__")))

    from display_utils import (
        show, show_before_after, pretty_sql,
        plot_bar, plot_pie, plot_grouped_bar,
        plot_salary_range, plot_gender_salary,
        plot_horizontal_salary,
        show_with_images,
    )

    print("DuckDB ready.")
    return (plot_bar, plot_gender_salary, plot_grouped_bar, plot_horizontal_salary, plot_pie, plot_salary_range, pretty_sql, show, show_before_after, show_with_images)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART 1 · Creating Tables (the **C** in CRUD)

    ## What Does "Create" Mean?

    In database terminology, **Create** refers to two things:

    1. **Creating a table** — defining the structure (columns, data types)  
    2. **Inserting rows** — adding data into the table  

    We will create **two** tables:

    | Table | Method |
    |-------|--------|
    | `employees` | Created with `INSERT INTO` statements |
    | `employees_backup` | Created by reading a **CSV file** |

    Both tables will contain the **exact same 10 employee records**.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1a · Create the `employees` Table via INSERT Statements

    We first `DROP` the table if it already exists — this makes the notebook  
    re-runnable without errors.
    """)
    return


@app.cell
def _(duckdb):
    duckdb.execute("DROP TABLE IF EXISTS " + "employees")
    duckdb.execute(
        "CREATE TABLE " + "employees" +
        " (emp_id INTEGER PRIMARY KEY, emp_name VARCHAR,"
        " department VARCHAR, salary INTEGER, gender VARCHAR, image_url VARCHAR)"
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        INSERT INTO employees
        VALUES
            (100, 'Alex', 'SALES', 120000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Alex'),
            (200, 'Jeff', 'SALES', 140000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Jeff'),
            (300, 'Rafa', 'BUSINESS', 150000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Rafa'),
            (400, 'Susan', 'SALES', 150000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Susan'),
            (500, 'Jen', 'BUSINESS', 160000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Jen'),
            (600, 'Barb', 'BUSINESS', 180000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Barb'),
            (700, 'Dara', 'AI', 190000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Dara'),
            (800, 'Venus', 'AI', 200000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Venus'),
            (900, 'Margie', 'SALES', 140000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Margie'),
            (910, 'Betty', 'SALES', 170000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Betty');
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Verify: Show all employees
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM employees
        ORDER BY emp_id;
        """
    )
    return


@app.cell
def _(show):
    show("SELECT * FROM employees ORDER BY emp_id",
         title="employees table — created via INSERT")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Meet the Team — Employees with Avatars

    Let's see our employees with their **profile pictures** rendered from the `image_url` column.  
    The avatars are generated by [DiceBear](https://www.dicebear.com/) — a free avatar API.
    """)
    return


@app.cell
def _(show_with_images):
    show_with_images(
        "SELECT * FROM employees ORDER BY emp_id",
        title="All Employees with Avatars"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1b · Create the `employees_backup` Table from a CSV File

    Reading data from a CSV file is one of the most common operations.  
    DuckDB can read CSV files directly with `read_csv_auto()`.
    """)
    return


@app.cell
def _(duckdb):
    duckdb.execute("DROP TABLE IF EXISTS employees_backup")
    duckdb.execute("""
        CREATE TABLE employees_backup AS
        SELECT * FROM read_csv_auto('data/employees.csv')
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Verify: Show all employees_backup
    """)
    return


@app.cell
def _(show):
    show("SELECT * FROM employees_backup ORDER BY emp_id",
         title="employees_backup table — created from CSV file")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART 2 · CRUD Operations

    We will now demonstrate **4 examples** for each CRUD operation.  
    For every operation we show:
    1. **BEFORE** — the table state before the change  
    2. **SQL** — the transformation query (pretty-printed)  
    3. **AFTER** — the table state after the change

    ---

    ## 2A · CREATE (Insert) — 4 Examples

    The SQL `INSERT INTO` statement adds new rows to a table.

    **Syntax:**
    ```sql
    INSERT INTO table_name (col1, col2, ...)
    VALUES (val1, val2, ...);
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C1 · Insert a Single Employee
    """)
    return


@app.cell
def _(show_before_after):
    show_before_after(
        sql_transform="""
            INSERT INTO employees VALUES
            (1000, 'Tom', 'AI', 195000, 'MALE',
             'https://api.dicebear.com/7.x/adventurer/svg?seed=Tom')
        """,
        transform_title="C1: Insert a single new employee (Tom)"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C2 · Insert Multiple Employees at Once
    """)
    return


@app.cell
def _(show_before_after):
    show_before_after(
        sql_transform="""
            INSERT INTO employees VALUES
            (1100, 'Grace', 'BUSINESS', 175000, 'FEMALE',
             'https://api.dicebear.com/7.x/adventurer/svg?seed=Grace'),
            (1200, 'Oscar', 'AI', 210000, 'MALE',
             'https://api.dicebear.com/7.x/adventurer/svg?seed=Oscar')
        """,
        transform_title="C2: Insert two employees at once (Grace, Oscar)"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C3 · Insert with Explicit Column Names
    """)
    return


@app.cell
def _(show_before_after):
    show_before_after(
        sql_transform="""
            INSERT INTO employees (emp_id, emp_name, department, salary, gender, image_url)
            VALUES (1300, 'Nina', 'SALES', 155000, 'FEMALE',
                    'https://api.dicebear.com/7.x/adventurer/svg?seed=Nina')
        """,
        transform_title="C3: Insert with explicit column list (Nina)"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### C4 · Insert from a SELECT (copy from backup)
    You can insert rows by selecting from another table — very useful for restoring data.
    """)
    return


@app.cell
def _(duckdb, show_before_after):
    # First, let's add a fictional employee to the backup table
    duckdb.execute("""
        INSERT INTO employees_backup VALUES
        (1400, 'Leo', 'BUSINESS', 165000, 'MALE',
         'https://api.dicebear.com/7.x/adventurer/svg?seed=Leo')
    """)

    show_before_after(
        sql_transform="""
            INSERT INTO employees
            SELECT * FROM employees_backup
            WHERE emp_id = 1400
        """,
        transform_title="C4: Insert from SELECT (copy Leo from backup)"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2B · READ (Select) — 4 Examples

    The SQL `SELECT` statement retrieves data from one or more tables.

    **Syntax:**
    ```sql
    SELECT col1, col2, ...
    FROM table_name
    WHERE condition
    ORDER BY col
    LIMIT n;
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R1 · Select All Columns
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("SELECT * FROM employees ORDER BY emp_id")
    show("SELECT * FROM employees ORDER BY emp_id",
         title="R1: All employees (SELECT *)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R2 · Select Specific Columns
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("SELECT emp_name, department, salary FROM employees ORDER BY salary DESC")
    show("SELECT emp_name, department, salary FROM employees ORDER BY salary DESC",
         title="R2: Names, departments, and salaries — sorted by salary (highest first)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R3 · Select with a WHERE Filter
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("SELECT * FROM employees WHERE department = 'AI' ORDER BY emp_id")
    show("SELECT * FROM employees WHERE department = 'AI' ORDER BY emp_id",
         title="R3: Only AI department employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AI Department — with Avatars
    """)
    return


@app.cell
def _(show_with_images):
    show_with_images(
        "SELECT emp_id, emp_name, salary, gender, image_url FROM employees WHERE department = 'AI' ORDER BY emp_id",
        title="AI Department Employees with Avatars"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R4 · Select with WHERE + LIMIT
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("SELECT * FROM employees WHERE salary >= 170000 ORDER BY salary DESC LIMIT 5")
    show("SELECT * FROM employees WHERE salary >= 170000 ORDER BY salary DESC LIMIT 5",
         title="R4: Top 5 employees earning >= $170,000")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2C · UPDATE — 4 Examples

    The SQL `UPDATE` statement modifies existing rows.

    **Syntax:**
    ```sql
    UPDATE table_name
    SET col1 = value1, col2 = value2, ...
    WHERE condition;
    ```

    > **Warning:** Without a `WHERE` clause, `UPDATE` changes **every** row!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U1 · Update a Single Employee's Salary
    """)
    return


@app.cell
def _(show_before_after):
    show_before_after(
        sql_transform="""
            UPDATE employees
            SET salary = 135000
            WHERE emp_id = 100
        """,
        transform_title="U1: Give Alex (emp_id=100) a raise to $135,000"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U2 · Update Department for an Employee
    """)
    return


@app.cell
def _(show_before_after):
    show_before_after(
        sql_transform="""
            UPDATE employees
            SET department = 'AI'
            WHERE emp_id = 300
        """,
        transform_title="U2: Transfer Rafa (emp_id=300) from BUSINESS to AI"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U3 · Update Multiple Columns at Once
    """)
    return


@app.cell
def _(show_before_after):
    show_before_after(
        sql_transform="""
            UPDATE employees
            SET salary = 180000,
                department = 'BUSINESS'
            WHERE emp_id = 900
        """,
        transform_title="U3: Update Margie — new salary $180k and move to BUSINESS"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U4 · Update All Employees in a Department (bulk update)
    """)
    return


@app.cell
def _(show_before_after):
    show_before_after(
        sql_transform="""
            UPDATE employees
            SET salary = salary + 5000
            WHERE department = 'SALES'
        """,
        transform_title="U4: Give every SALES employee a $5,000 raise"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2D · DELETE — 4 Examples

    The SQL `DELETE` statement removes rows from a table.

    **Syntax:**
    ```sql
    DELETE FROM table_name
    WHERE condition;
    ```

    > **Warning:** Without a `WHERE` clause, `DELETE` removes **all** rows!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D1 · Delete a Single Employee by ID
    """)
    return


@app.cell
def _(show_before_after):
    show_before_after(
        sql_transform="""
            DELETE FROM employees
            WHERE emp_id = 1400
        """,
        transform_title="D1: Delete Leo (emp_id=1400)"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D2 · Delete Employees by Name
    """)
    return


@app.cell
def _(show_before_after):
    show_before_after(
        sql_transform="""
            DELETE FROM employees
            WHERE emp_name = 'Nina'
        """,
        transform_title="D2: Delete Nina by name"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D3 · Delete Employees with Salary Above a Threshold
    """)
    return


@app.cell
def _(show_before_after):
    show_before_after(
        sql_transform="""
            DELETE FROM employees
            WHERE salary > 200000
        """,
        transform_title="D3: Delete employees earning more than $200,000"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D4 · Delete All Inserted Test Employees (clean-up)
    """)
    return


@app.cell
def _(show_before_after):
    show_before_after(
        sql_transform="""
            DELETE FROM employees
            WHERE emp_id >= 1000
        """,
        transform_title="D4: Delete all employees with emp_id >= 1000 (clean up test data)"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART 3 · Restore Original Data

    After all those CRUD operations, let's restore the `employees` table  
    to its original 10 rows from the backup. This makes the rest of the  
    notebook work correctly every time.
    """)
    return


@app.cell
def _(duckdb, show):
    # ── Restore employees from backup ────────────────────────────
    duckdb.execute("DROP TABLE IF EXISTS " + "employees")
    duckdb.execute("CREATE TABLE " + "employees" + " AS SELECT * FROM employees_backup WHERE emp_id <= 910")
    show("SELECT * FROM employees ORDER BY emp_id",
         title="employees table restored to original 10 rows")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART 4 · 10 Basic Queries (SELECT, WHERE, FROM, LIMIT)

    These queries demonstrate the fundamental building blocks of SQL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q1: Select all employees
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT * FROM employees ORDER BY emp_id""")
    show("""SELECT * FROM employees ORDER BY emp_id""",
         title="Q1: Select all employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q2: Select only names and salaries
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT emp_name, salary FROM employees ORDER BY emp_name""")
    show("""SELECT emp_name, salary FROM employees ORDER BY emp_name""",
         title="Q2: Select only names and salaries")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q3: Employees in the SALES department
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT * FROM employees WHERE department = 'SALES' ORDER BY emp_id""")
    show("""SELECT * FROM employees WHERE department = 'SALES' ORDER BY emp_id""",
         title="Q3: Employees in the SALES department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q4: Female employees only
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT * FROM employees WHERE gender = 'FEMALE' ORDER BY emp_name""")
    show("""SELECT * FROM employees WHERE gender = 'FEMALE' ORDER BY emp_name""",
         title="Q4: Female employees only")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q5: Employees earning more than $150,000
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT * FROM employees WHERE salary > 150000 ORDER BY salary DESC""")
    show("""SELECT * FROM employees WHERE salary > 150000 ORDER BY salary DESC""",
         title="Q5: Employees earning more than $150,000")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q6: Top 3 highest-paid employees
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT emp_name, salary FROM employees ORDER BY salary DESC LIMIT 3""")
    show("""SELECT emp_name, salary FROM employees ORDER BY salary DESC LIMIT 3""",
         title="Q6: Top 3 highest-paid employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q7: Employees NOT in SALES
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT * FROM employees WHERE department != 'SALES' ORDER BY emp_id""")
    show("""SELECT * FROM employees WHERE department != 'SALES' ORDER BY emp_id""",
         title="Q7: Employees NOT in SALES")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q8: Employees with salary between $140,000 and $170,000
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT * FROM employees WHERE salary BETWEEN 140000 AND 170000 ORDER BY salary""")
    show("""SELECT * FROM employees WHERE salary BETWEEN 140000 AND 170000 ORDER BY salary""",
         title="Q8: Employees with salary between $140,000 and $170,000")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q9: Employees whose name starts with 'B'
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT * FROM employees WHERE emp_name LIKE 'B%' ORDER BY emp_name""")
    show("""SELECT * FROM employees WHERE emp_name LIKE 'B%' ORDER BY emp_name""",
         title="Q9: Employees whose name starts with 'B'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q10: Count of all employees (LIMIT 1 — one-row result)
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT COUNT(*) AS total_employees FROM employees LIMIT 1""")
    show("""SELECT COUNT(*) AS total_employees FROM employees LIMIT 1""",
         title="Q10: Count of all employees (LIMIT 1 — one-row result)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART 5 · 10 Queries with GROUP BY, HAVING, LIMIT

    `GROUP BY` groups rows that share a value so aggregate functions  
    (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) can operate on each group.

    `HAVING` filters **groups** (like `WHERE` filters rows).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### G1: Count employees per department
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT department, COUNT(*) AS emp_count FROM employees GROUP BY department ORDER BY emp_count DESC""")
    show("""SELECT department, COUNT(*) AS emp_count FROM employees GROUP BY department ORDER BY emp_count DESC""",
         title="G1: Count employees per department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### G2: Average salary per department
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT department, ROUND(AVG(salary),0) AS avg_salary FROM employees GROUP BY department ORDER BY avg_salary DESC""")
    show("""SELECT department, ROUND(AVG(salary),0) AS avg_salary FROM employees GROUP BY department ORDER BY avg_salary DESC""",
         title="G2: Average salary per department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### G3: Total salary expense per department
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT department, SUM(salary) AS total_salary FROM employees GROUP BY department ORDER BY total_salary DESC""")
    show("""SELECT department, SUM(salary) AS total_salary FROM employees GROUP BY department ORDER BY total_salary DESC""",
         title="G3: Total salary expense per department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### G4: Min and Max salary per department
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT department, MIN(salary) AS min_salary, MAX(salary) AS max_salary FROM employees GROUP BY department ORDER BY department""")
    show("""SELECT department, MIN(salary) AS min_salary, MAX(salary) AS max_salary FROM employees GROUP BY department ORDER BY department""",
         title="G4: Min and Max salary per department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### G5: Count employees per gender
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT gender, COUNT(*) AS emp_count FROM employees GROUP BY gender""")
    show("""SELECT gender, COUNT(*) AS emp_count FROM employees GROUP BY gender""",
         title="G5: Count employees per gender")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### G6: Average salary per gender
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT gender, ROUND(AVG(salary),0) AS avg_salary FROM employees GROUP BY gender""")
    show("""SELECT gender, ROUND(AVG(salary),0) AS avg_salary FROM employees GROUP BY gender""",
         title="G6: Average salary per gender")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### G7: Departments with more than 2 employees (HAVING)
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT department, COUNT(*) AS emp_count FROM employees GROUP BY department HAVING COUNT(*) > 2 ORDER BY emp_count DESC""")
    show("""SELECT department, COUNT(*) AS emp_count FROM employees GROUP BY department HAVING COUNT(*) > 2 ORDER BY emp_count DESC""",
         title="G7: Departments with more than 2 employees (HAVING)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### G8: Departments where average salary > $160,000 (HAVING)
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT department, ROUND(AVG(salary),0) AS avg_salary FROM employees GROUP BY department HAVING AVG(salary) > 160000 ORDER BY avg_salary DESC""")
    show("""SELECT department, ROUND(AVG(salary),0) AS avg_salary FROM employees GROUP BY department HAVING AVG(salary) > 160000 ORDER BY avg_salary DESC""",
         title="G8: Departments where average salary > $160,000 (HAVING)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### G9: Top 2 departments by total salary (GROUP BY + LIMIT)
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT department, SUM(salary) AS total_salary FROM employees GROUP BY department ORDER BY total_salary DESC LIMIT 2""")
    show("""SELECT department, SUM(salary) AS total_salary FROM employees GROUP BY department ORDER BY total_salary DESC LIMIT 2""",
         title="G9: Top 2 departments by total salary (GROUP BY + LIMIT)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### G10: Gender & department breakdown
    """)
    return


@app.cell
def _(pretty_sql, show):
    pretty_sql("""SELECT department, gender, COUNT(*) AS emp_count, ROUND(AVG(salary),0) AS avg_salary FROM employees GROUP BY department, gender ORDER BY department, gender""")
    show("""SELECT department, gender, COUNT(*) AS emp_count, ROUND(AVG(salary),0) AS avg_salary FROM employees GROUP BY department, gender ORDER BY department, gender""",
         title="G10: Gender & department breakdown")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART 6 · Analytics & Visualisations

    Let's create meaningful plots from our employee data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 1 · Percentage of Male vs Female Employees
    """)
    return


@app.cell
def _(plot_pie, pretty_sql, show):
    _sql = "SELECT gender, COUNT(*) AS emp_count FROM employees GROUP BY gender"
    pretty_sql(_sql)
    _df = show(_sql, title="Gender Distribution")
    plot_pie(_df, "gender", "emp_count",
             title="Employee Gender Distribution",
             colors=["#4E79A7", "#E15759"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 2 · Percentage of Employees per Department
    """)
    return


@app.cell
def _(plot_pie, pretty_sql, show):
    _sql = "SELECT department, COUNT(*) AS emp_count FROM employees GROUP BY department ORDER BY emp_count DESC"
    pretty_sql(_sql)
    _df = show(_sql, title="Department Distribution")
    plot_pie(_df, "department", "emp_count",
             title="Employees by Department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 3 · All Employee Salaries (Highest to Lowest)
    """)
    return


@app.cell
def _(plot_horizontal_salary, pretty_sql, show):
    _sql = "SELECT emp_name, salary FROM employees ORDER BY salary DESC"
    pretty_sql(_sql)
    _df = show(_sql, title="Employee Salaries Ranked")
    plot_horizontal_salary(_df, title="All Employee Salaries (Ranked)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 4 · Salary Range by Department (Min / Avg / Max)
    """)
    return


@app.cell
def _(plot_salary_range, pretty_sql, show):
    _sql = """
    SELECT department,
           MIN(salary) AS min_salary,
           ROUND(AVG(salary),0)::INTEGER AS avg_salary,
           MAX(salary) AS max_salary
    FROM employees
    GROUP BY department
    ORDER BY department
    """
    pretty_sql(_sql)
    _df = show(_sql, title="Salary Range per Department")
    plot_salary_range(_df, title="Salary Range by Department (● min/max, ◆ avg)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 5 · Average Salary by Gender
    """)
    return


@app.cell
def _(plot_gender_salary, pretty_sql, show):
    _sql = "SELECT gender, ROUND(AVG(salary),0) AS avg_salary FROM employees GROUP BY gender"
    pretty_sql(_sql)
    _df = show(_sql, title="Average Salary by Gender")
    plot_gender_salary(_df, title="Average Salary: Male vs Female")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 6 · Total Salary Expense per Department
    """)
    return


@app.cell
def _(plot_bar, pretty_sql, show):
    _sql = "SELECT department, SUM(salary) AS total_salary FROM employees GROUP BY department ORDER BY total_salary DESC"
    pretty_sql(_sql)
    _df = show(_sql, title="Total Salary by Department")
    plot_bar(_df, "department", "total_salary",
             title="Total Salary Expense per Department",
             ylabel="Total Salary ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 7 · Average Salary by Department and Gender
    """)
    return


@app.cell
def _(plot_grouped_bar, pretty_sql, show):
    _sql = """
    SELECT department, gender,
           ROUND(AVG(salary),0) AS avg_salary
    FROM employees
    GROUP BY department, gender
    ORDER BY department, gender
    """
    pretty_sql(_sql)
    _df = show(_sql, title="Avg Salary by Department & Gender")
    plot_grouped_bar(_df, "gender", "department", "avg_salary",
                     title="Average Salary by Department & Gender",
                     ylabel="Avg Salary ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 8 · Employee Count per Department
    """)
    return


@app.cell
def _(plot_bar, pretty_sql, show):
    _sql = "SELECT department, COUNT(*) AS emp_count FROM employees GROUP BY department ORDER BY emp_count DESC"
    pretty_sql(_sql)
    _df = show(_sql, title="Headcount by Department")
    plot_bar(_df, "department", "emp_count",
             title="Number of Employees per Department",
             ylabel="Count", fmt="{:.0f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 9 · Top 5 Highest-Paid Employees with Avatars
    """)
    return


@app.cell
def _(pretty_sql, show_with_images):
    pretty_sql("SELECT * FROM employees ORDER BY salary DESC LIMIT 5")
    show_with_images(
        "SELECT emp_id, emp_name, department, salary, gender, image_url FROM employees ORDER BY salary DESC LIMIT 5",
        title="Top 5 Highest-Paid Employees"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Summary

    In this notebook you learned:

    | Topic | What You Practiced |
    |-------|-------------------|
    | **CREATE** | `INSERT INTO` — single row, multiple rows, explicit columns, from SELECT |
    | **READ**   | `SELECT *`, specific columns, `WHERE`, `LIMIT` |
    | **UPDATE** | Single column, department transfer, multi-column, bulk update |
    | **DELETE** | By ID, by name, by condition, bulk clean-up |
    | **Basic Queries** | `SELECT`, `WHERE`, `FROM`, `LIMIT`, `LIKE`, `BETWEEN`, `!=` |
    | **GROUP BY** | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `HAVING`, `LIMIT` |
    | **Plots** | Pie charts, bar charts, horizontal bars, range charts, grouped bars |

    ### Key Takeaways

    - **DuckDB** runs in-process — no server setup needed  
    - **Marimo SQL cells** let you write raw SQL with no Python wrapper  
    - Always use `DROP TABLE IF EXISTS` to make notebooks re-runnable  
    - `WHERE` filters rows; `HAVING` filters groups  
    - Keep plotting code in a separate utility file for clean notebooks

    ---
    *Notebook created for OMIS 105 — Santa Clara University*
    """)
    return


@app.cell
def _():
    # ── Done! ──────────────────────────────────────────────────
    # The in-memory DuckDB database is discarded when the kernel stops.
    print("Notebook complete!")
    return


if __name__ == "__main__":
    app.run()
