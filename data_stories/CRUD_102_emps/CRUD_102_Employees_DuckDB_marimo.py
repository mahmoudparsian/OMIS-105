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
    # CRUD 102 with Employee Data using DuckDB

    **Goal:** Learn CRUD operations using a small, realistic employee dataset in DuckDB.

    CRUD means **Create, Read, Update, Delete**. This notebook assumes students are new to DuckDB and CRUD. Each major operation shows the data **before**, the SQL **transformation**, and the data **after**.

    All table-display and plotting functions are kept in `helpers/crud_display.py` so students can focus on SQL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 1 — Project setup

    **What are we doing?** Importing DuckDB, pandas, and helper functions.

    **Why?** DuckDB runs SQL, pandas holds results, and helper functions create clean tables and plots.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SQL Formatting Style Used in This Notebook

    In this notebook, all SQL statements are written using:

    - triple-quoted SQL strings
    - multi-line formatting
    - indentation
    - aligned SQL clauses

    This reflects how SQL is written in real-world production systems.

    Example:

    ```python
    sql = "\"\"
    SELECT
        emp_id,
        emp_name,
        salary
    FROM employees
    WHERE salary > 120000
    ORDER BY salary DESC
    "\"\"

    df = con.execute(sql).df()
    ```
    """)
    return


@app.cell
def _():
    from pathlib import Path
    import sys
    import duckdb
    import pandas as pd

    PREFERRED_PROJECT_DIR = Path("/Users/max/mp/OMIS_105/data_stories/CRUD_102_emps")
    PROJECT_DIR = PREFERRED_PROJECT_DIR if PREFERRED_PROJECT_DIR.exists() else Path.cwd()
    DATA_DIR = PROJECT_DIR / "data"
    HELPERS_DIR = PROJECT_DIR / "helpers"
    DB_PATH = PROJECT_DIR / "employees_crud.duckdb"
    CSV_PATH = DATA_DIR / "employees.csv"

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    HELPERS_DIR.mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(HELPERS_DIR))
    from crud_display import run_sql, execute_sql, display_table, plot_bar, plot_horizontal_bar, plot_pie, plot_line

    print("PROJECT_DIR:", PROJECT_DIR)
    print("DATA_DIR:", DATA_DIR)
    print("DB_PATH:", DB_PATH)
    print("CSV_PATH:", CSV_PATH)
    return (
        CSV_PATH,
        DB_PATH,
        display_table,
        duckdb,
        execute_sql,
        pd,
        plot_bar,
        plot_line,
        plot_pie,
        run_sql,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 2 — Create the CSV data file

    **What are we doing?** Creating `data/employees.csv` with 10 realistic employee records.

    **Why?** A CSV file is a common source system format. We will load this CSV into DuckDB.

    Rules satisfied: 10 records, 2 employees per country, 50% male/female, salaries 81,000–230,000, hire dates in 2015, ages 22–52.
    """)
    return


@app.cell
def _(CSV_PATH, display_table, pd):
    employees_data = [
        [1001, "John Smith", "SALES", 92000, "MALE", "BA", "2015-01-12", "USA", "https://i.pravatar.cc/150?img=11", 29],
        [1002, "Emily Johnson", "IT", 128000, "FEMALE", "MS", "2015-03-08", "USA", "https://i.pravatar.cc/150?img=32", 34],
        [1003, "Liam Brown", "AI", 167000, "MALE", "BS", "2015-02-19", "CANADA", "https://i.pravatar.cc/150?img=12", 31],
        [1004, "Sophia Martin", "BUSINESS", 118000, "FEMALE", "MIS", "2015-09-22", "CANADA", "https://i.pravatar.cc/150?img=47", 38],
        [1005, "Luca Rossi", "MARKETING", 101000, "MALE", "BA", "2015-05-14", "ITALY", "https://i.pravatar.cc/150?img=15", 42],
        [1006, "Giulia Bianchi", "AI", 181000, "FEMALE", "PHD", "2015-11-03", "ITALY", "https://i.pravatar.cc/150?img=45", 36],
        [1007, "Hans Müller", "IT", 145000, "MALE", "BS", "2015-04-27", "GERMANY", "https://i.pravatar.cc/150?img=16", 45],
        [1008, "Anna Schneider", "BUSINESS", 134000, "FEMALE", "MS", "2015-08-16", "GERMANY", "https://i.pravatar.cc/150?img=44", 33],
        [1009, "Wei Zhang", "AI", 219000, "MALE", "PHD", "2015-06-30", "CHINA", "https://i.pravatar.cc/150?img=18", 40],
        [1010, "Mei Chen", "MARKETING", 97000, "FEMALE", "MIS", "2015-12-09", "CHINA", "https://i.pravatar.cc/150?img=49", 28],
    ]
    columns = ["emp_id", "emp_name", "department", "salary", "gender", "degree", "hire_date", "country", "image_url", "age"]
    employees_df = pd.DataFrame(employees_data, columns=columns)
    employees_df.to_csv(CSV_PATH, index=False)
    display_table(employees_df, title="CSV data created from Python", render_images=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 3 — Connect to DuckDB and create the employees table

    **What are we doing?** Creating a DuckDB table from the CSV.

    **Why?** Once data is in DuckDB, we can teach CRUD with SQL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Creating the `avatar` / `image_url` Column

    In this section, we create employee avatar URLs directly inside the notebook.

    This teaches students:

    - how synthetic columns are generated
    - how Python enriches datasets
    - how URLs can later be rendered in dashboards and applications

    We use the public avatar service:

    `https://randomuser.me`
    """)
    return


@app.cell
def _(pd):

    # ============================================================
    # Create image_url / avatar column
    # ============================================================

    import random

    df_employees = pd.read_csv("data/employees.csv")
    print(df_employees.head())


    # Make sure df_employees already exists

    # Example:

    # df_employees = pd.read_csv("data/employees.csv")

    male_avatars = [
        f"https://randomuser.me/api/portraits/men/{i}.jpg"
        for i in range(10, 60)
    ]

    female_avatars = [
        f"https://randomuser.me/api/portraits/women/{i}.jpg"
        for i in range(10, 60)
    ]

    avatar_urls = []

    for gender in df_employees['gender']:
        if gender == 'MALE':
            avatar_urls.append(random.choice(male_avatars))
        else:
            avatar_urls.append(random.choice(female_avatars))

    # Add image_url column

    df_employees['image_url'] = avatar_urls

    # Display results

    df_employees[['emp_name', 'gender', 'image_url']]
    return


@app.cell
def _(CSV_PATH, DB_PATH, duckdb, execute_sql, run_sql):
    con = duckdb.connect(str(DB_PATH))
    execute_sql(con, """
        DROP TABLE IF EXISTS employees;
    """, title="""
        DROP old employees TABLE IF it EXISTS;
    """)

    create_table_sql = f"""
    CREATE TABLE employees AS
    SELECT
        emp_id::INTEGER AS emp_id,
        emp_name::VARCHAR AS emp_name,
        department::VARCHAR AS department,
        salary::INTEGER AS salary,
        gender::VARCHAR AS gender,
        degree::VARCHAR AS degree,
        hire_date::DATE AS hire_date,
        country::VARCHAR AS country,
        image_url::VARCHAR AS image_url,
        age::INTEGER AS age
    FROM read_csv_auto('{CSV_PATH.as_posix()}', HEADER = TRUE);
    """
    execute_sql(con, create_table_sql, title="""
        CREATE employees TABLE
        FROM CSV;
    """)
    run_sql(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="employees table after loading CSV")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 4 — Quick validation checks

    **What are we doing?** Checking that the dataset follows the required rules.

    **Why?** Always validate source data before teaching or analyzing it.
    """)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT COUNT(*) AS number_of_employees
        FROM employees;
    """, title="Validation 1: number of employees", render_images=False)

    run_sql(con, """
        SELECT
            country,
            COUNT(*) AS employees_per_country
        FROM employees
        GROUP BY country
        ORDER BY country;
    """, title="Validation 2: two employees per country", render_images=False)

    run_sql(con, """
        SELECT
            gender,
            COUNT(*) AS gender_count
        FROM employees
        GROUP BY gender
        ORDER BY gender;
    """, title="Validation 3: gender balance", render_images=False)

    run_sql(con, """
        SELECT
            country,
            COUNT(DISTINCT degree) AS different_degrees
        FROM employees
        GROUP BY country
        ORDER BY country;
    """, title="Validation 4: at least two different degrees per country", render_images=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part A — CREATE Operations

    Create means adding new data or creating new database objects. Common SQL examples are `CREATE TABLE`, `CREATE TABLE AS SELECT`, and `INSERT INTO`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C1 — Create a backup table

    **What are we doing?** Creating `employees_backup` as a copy of `employees`.

    **Why?** A backup copy protects us before making changes.
    """)
    return


@app.cell
def _(con, execute_sql, run_sql):
    execute_sql(con, """
        DROP TABLE IF EXISTS employees_backup;
    """, title="Prepare: remove old backup table")
    run_sql(con, """
        SELECT COUNT(*) AS employees_before_backup
        FROM employees;
    """, title="Before CREATE", render_images=False)
    execute_sql(con, """
        CREATE TABLE employees_backup AS
        SELECT *
        FROM employees;
    """, title="Transformation: CREATE TABLE AS SELECT")
    run_sql(con, """
        SELECT COUNT(*) AS backup_rows_after_create
        FROM employees_backup;
    """, title="After CREATE", render_images=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C2 — Insert one new employee

    **What are we doing?** Adding one employee to the table.

    **Why?** `INSERT INTO` creates a new row in an existing table.
    """)
    return


@app.cell
def _(con, execute_sql, run_sql):
    run_sql(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title="Before INSERT")
    execute_sql(con, """
        INSERT INTO employees
        VALUES (1011, 'Robert Wilson', 'SALES', 112000, 'MALE', 'BS', DATE '2015-10-10', 'USA', 'https://i.pravatar.cc/150?img=20', 37);
    """, title="Transformation: INSERT one employee")
    run_sql(con, """
        SELECT *
        FROM employees
        WHERE emp_id = 1011;
    """, title="After INSERT: new employee")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C3 — Insert multiple new employees

    **What are we doing?** Inserting two rows with one statement.

    **Why?** Bulk inserts are useful when adding multiple records.
    """)
    return


@app.cell
def _(con, execute_sql, run_sql):
    run_sql(con, """
        SELECT COUNT(*) AS rows_before_insert
        FROM employees;
    """, title="Before INSERT multiple", render_images=False)
    execute_sql(con, """
        INSERT INTO employees
        VALUES
            (1012, 'Claire Dubois', 'BUSINESS', 121000, 'FEMALE', 'MIS', DATE '2015-07-15', 'CANADA', 'https://i.pravatar.cc/150?img=41', 35),
            (1013, 'Marco Ferrari', 'MARKETING', 106000, 'MALE', 'BA', DATE '2015-02-05', 'ITALY', 'https://i.pravatar.cc/150?img=21', 39);
    """, title="Transformation: INSERT multiple employees")
    run_sql(con, """
        SELECT *
        FROM employees
        WHERE emp_id IN (1012, 1013)
        ORDER BY emp_id;
    """, title="After INSERT multiple")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C4 — Create a department summary table

    **What are we doing?** Creating an analytical summary table.

    **Why?** Summary tables make reporting easier.
    """)
    return


@app.cell
def _(con, execute_sql, plot_bar, run_sql):
    execute_sql(con, """
        DROP TABLE IF EXISTS department_summary;
    """, title="Prepare: remove old summary table")
    run_sql(con, """
        SELECT
            department,
            salary
        FROM employees
        ORDER BY department;
    """, title="Before summary table")
    execute_sql(con, """
        CREATE TABLE department_summary AS
        SELECT
            department,
            COUNT(*) AS num_employees,
            ROUND(AVG(salary), 2) AS avg_salary,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY department;
    """, title="Transformation: CREATE summary table")
    _df = run_sql(con, """
        SELECT *
        FROM department_summary
        ORDER BY total_salary DESC;
    """, title="After CREATE summary table", render_images=False)
    plot_bar(_df, x="department", y="total_salary", title="Total Salary by Department", ylabel="Total Salary", rotation=30)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part B — READ Operations

    Read means retrieving data using `SELECT`. Important clauses include `SELECT`, `FROM`, `WHERE`, `ORDER BY`, and `LIMIT`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## R1 — Read all employees

    **What are we doing?** Reading data using `SELECT`.

    **Why?** Read queries answer questions without changing data.
    """)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """, title='R1 — Read all employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## R2 — Read selected columns

    **What are we doing?** Reading data using `SELECT`.

    **Why?** Read queries answer questions without changing data.
    """)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            department,
            salary
        FROM employees
        ORDER BY emp_id;
    """, title='R2 — Read selected columns')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## R3 — Read high salary employees

    **What are we doing?** Reading data using `SELECT`.

    **Why?** Read queries answer questions without changing data.
    """)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            department,
            salary
        FROM employees
        WHERE salary >= 150000
        ORDER BY salary DESC;
    """, title='R3 — Read high salary employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## R4 — Read employees from one country

    **What are we doing?** Reading data using `SELECT`.

    **Why?** Read queries answer questions without changing data.
    """)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            country,
            degree,
            salary
        FROM employees
        WHERE country = 'USA'
        ORDER BY salary DESC;
    """, title='R4 — Read employees from one country')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## R5 — Read youngest employees

    **What are we doing?** Reading data using `SELECT`.

    **Why?** Read queries answer questions without changing data.
    """)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            age,
            country
        FROM employees
        ORDER BY age ASC
        LIMIT 5;
    """, title='R5 — Read youngest employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part C — UPDATE Operations

    Update means changing existing data. The pattern is:

    ```sql
    UPDATE table_name
    SET column_name = new_value
    WHERE condition;
    ```

    The `WHERE` clause is critical.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## U1 — Give one employee a salary increase

    **What are we doing?** Changing existing values.

    **Why?** Update operations keep stored data current or add derived categories.
    """)
    return


@app.cell
def _(con, execute_sql, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        WHERE emp_id = 1001;
    """, title="Before UPDATE")
    execute_sql(con, """
    UPDATE employees
    SET salary = salary + 5000
    WHERE emp_id = 1001;
    """, title="Transformation: increase salary by 5,000")
    run_sql(con, "SELECT emp_id, emp_name, salary FROM employees WHERE emp_id = 1001", title="After UPDATE")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## U2 — Update a department name

    **What are we doing?** Changing existing values.

    **Why?** Update operations keep stored data current or add derived categories.
    """)
    return


@app.cell
def _(con, execute_sql, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            department
        FROM employees
        WHERE department = 'AI'
        ORDER BY emp_id;
    """, title="Before UPDATE")
    execute_sql(con, """
    UPDATE employees
    SET department = 'DATA_AI'
    WHERE department = 'AI';
    """, title="Transformation: rename AI department")
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            department
        FROM employees
        WHERE department = 'DATA_AI'
        ORDER BY emp_id;
    """, title="After UPDATE")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## U3 — Update salaries for one department

    **What are we doing?** Changing existing values.

    **Why?** Update operations keep stored data current or add derived categories.
    """)
    return


@app.cell
def _(con, execute_sql, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            department,
            salary
        FROM employees
        WHERE department = 'IT'
        ORDER BY emp_id;
    """, title="Before UPDATE")
    execute_sql(con, """
        UPDATE employees
        SET salary = CAST(ROUND(salary * 1.03, 0) AS INTEGER)
        WHERE department = 'IT';
    """, title="Transformation: IT salary increase")
    run_sql(con, "SELECT emp_id, emp_name, department, salary FROM employees WHERE department = 'IT' ORDER BY emp_id", title="After UPDATE")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## U4 — Update a value using a CASE expression

    **What are we doing?** Changing existing values.

    **Why?** Update operations keep stored data current or add derived categories.
    """)
    return


@app.cell
def _(con, execute_sql, run_sql):
    execute_sql(con, """
        ALTER TABLE employees DROP COLUMN IF EXISTS salary_band;
    """, title="Prepare: remove old salary_band column")
    execute_sql(con, """
        ALTER TABLE employees ADD COLUMN salary_band VARCHAR;
    """, title="Add salary_band column")
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            salary,
            salary_band
        FROM employees
        ORDER BY emp_id;
    """, title="Before UPDATE with CASE")
    execute_sql(con, """
    UPDATE employees
    SET salary_band = CASE
        WHEN salary >= 180000 THEN 'HIGH'
        WHEN salary >= 120000 THEN 'MEDIUM'
        ELSE 'LOW'
    END;
    """, title="Transformation: assign salary bands")
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            salary,
            salary_band
        FROM employees
        ORDER BY salary DESC;
    """, title="After UPDATE with CASE")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part D — DELETE Operations

    Delete means removing data. The pattern is:

    ```sql
    DELETE FROM table_name
    WHERE condition;
    ```

    A missing `WHERE` can delete every row.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## D1 — Delete one employee by ID

    **What are we doing?** Removing rows.

    **Why?** Delete operations remove records that should no longer exist or are part of a safe practice demo.
    """)
    return


@app.cell
def _(con, execute_sql, run_sql):
    run_sql(con, """
        SELECT *
        FROM employees
        WHERE emp_id = 1013;
    """, title="Before DELETE")
    execute_sql(con, """
        DELETE
        FROM employees
        WHERE emp_id = 1013;
    """, title="Transformation: DELETE one employee")
    run_sql(con, "SELECT * FROM employees WHERE emp_id = 1013", title="After DELETE")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## D2 — Delete employees below a salary threshold

    **What are we doing?** Removing rows.

    **Why?** Delete operations remove records that should no longer exist or are part of a safe practice demo.
    """)
    return


@app.cell
def _(con, execute_sql, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        WHERE salary < 100000
        ORDER BY salary;
    """, title="Before DELETE")
    execute_sql(con, """
        DELETE
        FROM employees
        WHERE salary < 100000;
    """, title="Transformation: DELETE low salary records")
    run_sql(con, "SELECT emp_id, emp_name, salary FROM employees WHERE salary < 100000 ORDER BY salary", title="After DELETE")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## D3 — Delete from a temporary practice table

    **What are we doing?** Removing rows.

    **Why?** Delete operations remove records that should no longer exist or are part of a safe practice demo.
    """)
    return


@app.cell
def _(con, execute_sql, run_sql):
    execute_sql(con, """
        DROP TABLE IF EXISTS employees_delete_practice;
    """, title="Prepare practice table")
    execute_sql(con, """
        CREATE TABLE employees_delete_practice AS
        SELECT *
        FROM employees;
    """, title="""
        CREATE practice TABLE;
    """)
    run_sql(con, """
        SELECT
            country,
            COUNT(*) AS rows_before
        FROM employees_delete_practice
        GROUP BY country
        ORDER BY country;
    """, title="Before DELETE", render_images=False)
    execute_sql(con, """
        DELETE
        FROM employees_delete_practice
        WHERE country = 'CANADA';
    """, title="Transformation: DELETE Canada from practice table")
    run_sql(con, """
        SELECT
            country,
            COUNT(*) AS rows_after
        FROM employees_delete_practice
        GROUP BY country
        ORDER BY country;
    """, title="After DELETE", render_images=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## D4 — Delete all rows from a temporary table

    **What are we doing?** Removing rows.

    **Why?** Delete operations remove records that should no longer exist or are part of a safe practice demo.
    """)
    return


@app.cell
def _(con, execute_sql, run_sql):
    execute_sql(con, """
        DROP TABLE IF EXISTS temp_delete_all_demo;
    """, title="Prepare temp table")
    execute_sql(con, """
        CREATE TABLE temp_delete_all_demo AS
        SELECT *
        FROM employees;
    """, title="""
        CREATE temp TABLE;
    """)
    run_sql(con, """
        SELECT COUNT(*) AS rows_before_delete_all
        FROM temp_delete_all_demo;
    """, title="Before DELETE all", render_images=False)
    execute_sql(con, """
        DELETE
        FROM temp_delete_all_demo;
    """, title="Transformation: DELETE all rows from temp table")
    run_sql(con, """
        SELECT COUNT(*) AS rows_after_delete_all
        FROM temp_delete_all_demo;
    """, title="After DELETE all", render_images=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part E — 10 Basic SELECT Queries

    These queries focus on `SELECT`, `FROM`, `WHERE`, and `LIMIT`.
    """)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT *
        FROM employees
        ORDER BY emp_id
        LIMIT 5;
    """, title='Basic 1 — First five employees')
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_name,
            department
        FROM employees
        ORDER BY emp_name
        LIMIT 10;
    """, title='Basic 2 — Names and departments')
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            country
        FROM employees
        WHERE country = 'GERMANY';
    """, title='Basic 3 — Employees in Germany')
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_name,
            age
        FROM employees
        WHERE age >= 35
        ORDER BY age DESC;
    """, title='Basic 4 — Employees age 35 or older')
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_name,
            degree,
            salary
        FROM employees
        WHERE degree = 'MS';
    """, title='Basic 5 — Employees with MS degree')
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_name,
            salary
        FROM employees
        ORDER BY salary DESC
        LIMIT 5;
    """, title='Basic 6 — Highest salaries')
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_name,
            age,
            country
        FROM employees
        ORDER BY age ASC
        LIMIT 3;
    """, title='Basic 7 — Youngest employees')
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_name,
            department,
            salary
        FROM employees
        WHERE department IN ('BUSINESS', 'MARKETING');
    """, title='Basic 8 — Business or Marketing')
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_name,
            salary
        FROM employees
        WHERE salary BETWEEN 120000
        AND 180000
        ORDER BY salary;
    """, title='Basic 9 — Salary between 120k and 180k')
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            image_url,
            country
        FROM employees
        ORDER BY emp_id
        LIMIT 8;
    """, title='Basic 10 — Render employee avatars')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part F — 10 GROUP BY / HAVING / LIMIT Queries

    `GROUP BY` creates groups. `HAVING` filters groups after aggregation. These queries include meaningful plots when appropriate.
    """)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            country,
            COUNT(*) AS num_employees
        FROM employees
        GROUP BY country
        ORDER BY country;
    """, title='Group 1 — Employees per country', render_images=False)
    plot_bar(_df, x='country', y='num_employees', title='Group 1 — Employees per country', rotation=25)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            department,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
    """, title='Group 2 — Average salary by department', render_images=False)
    plot_bar(_df, x='department', y='avg_salary', title='Group 2 — Average salary by department', rotation=25)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            country,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY country
        ORDER BY total_salary DESC;
    """, title='Group 3 — Total salary by country', render_images=False)
    plot_bar(_df, x='country', y='total_salary', title='Group 3 — Total salary by country', rotation=25)
    return


@app.cell
def _(con, plot_pie, run_sql):
    _df = run_sql(con, """
        SELECT
            gender,
            COUNT(*) AS gender_count
        FROM employees
        GROUP BY gender
        ORDER BY gender;
    """, title='Group 4 — Gender counts', render_images=False)
    plot_pie(_df, labels='gender', values='gender_count', title='Group 4 — Gender counts')
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            degree,
            ROUND(AVG(age), 2) AS avg_age
        FROM employees
        GROUP BY degree
        ORDER BY avg_age DESC;
    """, title='Group 5 — Average age by degree', render_images=False)
    plot_bar(_df, x='degree', y='avg_age', title='Group 5 — Average age by degree', rotation=25)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            department,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY department
        HAVING AVG(salary) > 130000
        ORDER BY avg_salary DESC;
    """, title='Group 6 — Departments with average salary over 130k', render_images=False)
    plot_bar(_df, x='department', y='avg_salary', title='Group 6 — Departments with average salary over 130k', rotation=25)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            country,
            COUNT(*) AS num_employees
        FROM employees
        GROUP BY country
        HAVING COUNT(*) >= 2
        ORDER BY num_employees DESC;
    """, title='Group 7 — Countries with at least 2 employees', render_images=False)
    plot_bar(_df, x='country', y='num_employees', title='Group 7 — Countries with at least 2 employees', rotation=25)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            degree,
            COUNT(*) AS degree_count
        FROM employees
        GROUP BY degree
        ORDER BY degree_count DESC, degree
        LIMIT 3;
    """, title='Group 8 — Degree counts limited to top 3', render_images=False)
    plot_bar(_df, x='degree', y='degree_count', title='Group 8 — Degree counts limited to top 3', rotation=25)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            country,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            MAX(salary) - MIN(salary) AS salary_range
        FROM employees
        GROUP BY country
        ORDER BY salary_range DESC;
    """, title='Group 9 — Salary range by country', render_images=False)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            salary_band,
            COUNT(*) AS num_employees,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY salary_band
        ORDER BY avg_salary DESC;
    """, title='Group 10 — Average salary by salary band', render_images=False)
    plot_bar(_df, x='salary_band', y='avg_salary', title='Group 10 — Average salary by salary band', rotation=25)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part G — 10 Intermediate Queries

    These queries introduce ranking, subqueries, CTEs, and window functions.
    """)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            RANK() OVER (
        ORDER BY salary DESC) AS salary_rank
        FROM employees
        ORDER BY salary_rank;
    """, title='Intermediate 1 — Rank employees by salary', render_images=True)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            RANK() OVER (PARTITION BY department
        ORDER BY salary DESC) AS dept_salary_rank
        FROM employees
        ORDER BY department, dept_salary_rank;
    """, title='Intermediate 2 — Rank salary within department', render_images=True)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        WHERE salary > (
        SELECT AVG(salary)
        FROM employees)
        ORDER BY salary DESC;
    """, title='Intermediate 3 — Employees above average salary', render_images=True)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            department,
            SUM(salary) AS dept_salary,
            ROUND(100.0 * SUM(salary) / (
        SELECT SUM(salary)
        FROM employees), 2) AS pct_of_total_salary
        FROM employees
        GROUP BY department
        ORDER BY pct_of_total_salary DESC;
    """, title='Intermediate 4 — Department salary share', render_images=False)
    plot_bar(_df, x='department', y='pct_of_total_salary', title='Intermediate 4 — Department salary share', ylabel='Percent of Total Salary', rotation=25)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        WITH ranked AS (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY country
        ORDER BY salary DESC) AS rn
        FROM employees)
        SELECT
            country,
            emp_name,
            salary
        FROM ranked
        WHERE rn = 1
        ORDER BY salary DESC;
    """, title='Intermediate 5 — Top employee per country', render_images=True)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_name,
            salary,
            ROUND(salary - AVG(salary) OVER (), 2) AS diff_from_company_avg
        FROM employees
        ORDER BY diff_from_company_avg DESC;
    """, title='Intermediate 6 — Salary difference from company average', render_images=True)
    return


@app.cell
def _(con, plot_line, run_sql):
    _df = run_sql(con, """
        SELECT
            emp_name,
            hire_date,
            salary,
            SUM(salary) OVER (
        ORDER BY hire_date) AS running_total_salary
        FROM employees
        ORDER BY hire_date;
    """, title='Intermediate 7 — Running total salary by hire date', render_images=False)
    plot_line(_df, x='hire_date', y='running_total_salary', title='Intermediate 7 — Running total salary by hire date', ylabel='Running Total Salary')
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_name,
            department,
            salary,
            ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS dept_avg_salary
        FROM employees
        ORDER BY department, salary DESC;
    """, title='Intermediate 8 — Department average using window function', render_images=True)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        SELECT
            emp_name,
            department,
            salary,
            ROUND(salary - AVG(salary) OVER (PARTITION BY department), 2) AS diff_from_dept_avg
        FROM employees
        ORDER BY department, diff_from_dept_avg DESC;
    """, title='Intermediate 9 — Compare each employee to department average', render_images=True)
    return


@app.cell
def _(con, run_sql):
    run_sql(con, """
        WITH ranked AS (
        SELECT
            emp_name,
            degree,
            age,
            ROW_NUMBER() OVER (PARTITION BY degree
        ORDER BY age ASC) AS rn
        FROM employees)
        SELECT
            degree,
            emp_name,
            age
        FROM ranked
        WHERE rn = 1
        ORDER BY degree;
    """, title='Intermediate 10 — Youngest employee per degree', render_images=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part H — Final Dashboard-Style Analytical Queries with Plots

    These business-style queries combine SQL result sets and meaningful visualizations.
    """)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            department,
            COUNT(*) AS employees,
            SUM(salary) AS total_salary,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY total_salary DESC;
    """, title='Dashboard 1 — Salary investment by department', render_images=False)
    plot_bar(_df, x='department', y='total_salary', title='Dashboard 1 — Salary investment by department', rotation=25)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            country,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY country
        ORDER BY avg_salary DESC;
    """, title='Dashboard 2 — Average salary by country', render_images=False)
    plot_bar(_df, x='country', y='avg_salary', title='Dashboard 2 — Average salary by country', rotation=25)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            degree,
            COUNT(*) AS employees
        FROM employees
        GROUP BY degree
        ORDER BY employees DESC, degree;
    """, title='Dashboard 3 — Employee count by degree', render_images=False)
    plot_bar(_df, x='degree', y='employees', title='Dashboard 3 — Employee count by degree', rotation=25)
    return


@app.cell
def _(con, plot_bar, run_sql):
    _df = run_sql(con, """
        SELECT
            department,
            ROUND(AVG(age), 2) AS avg_age
        FROM employees
        GROUP BY department
        ORDER BY avg_age DESC;
    """, title='Dashboard 4 — Average age by department', render_images=False)
    plot_bar(_df, x='department', y='avg_age', title='Dashboard 4 — Average age by department', rotation=25)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final Cell — Close the DuckDB connection

    **What are we doing?** Closing the database connection.

    **Why?** This saves work cleanly and releases the database file.
    """)
    return


@app.cell
def _(con):
    con.close()
    print("DuckDB connection closed successfully.")
    return


if __name__ == "__main__":
    app.run()
