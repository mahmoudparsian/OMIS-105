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
    # 🦆 CRUD 101 — Employee Data with DuckDB

    **Course:** OMIS 105
    **Topic:** Create · Read · Update · Delete using SQL & DuckDB

    ---

    ### What you will learn
    | Operation | SQL Command | Meaning |
    |-----------|-------------|---------|
    | **C**reate | `INSERT INTO` | Add new rows to a table |
    | **R**ead | `SELECT ... FROM` | Query / retrieve data |
    | **U**pdate | `UPDATE ... SET` | Modify existing rows |
    | **D**elete | `DELETE FROM` | Remove rows from a table |

    > **DuckDB** is an in-process SQL database — no server needed.
    > Think of it as *SQLite* but turbocharged for analytics.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    #  CELL 1 — SETUP
    """)
    return


@app.cell
def _():
    # ════════════════════════════════════════════════════════════════
    #  CELL 1 — SETUP
    #  Import libraries, connect to DuckDB, load our helper utilities.
    #  Run this cell FIRST every time you open the notebook.
    # ════════════════════════════════════════════════════════════════
    import sys, os
    import duckdb
    import pandas as pd

    # ── Make sure emp_utils.py is importable ──────────────────────
    NOTEBOOK_DIR = os.path.dirname(os.path.abspath('__file__'))
    if NOTEBOOK_DIR not in sys.path:
        sys.path.insert(0, NOTEBOOK_DIR)

    from emp_utils import (
        show, section, note, definition, sql_box,
        show_before_after, show_avatars,
        plot_bar, plot_pie, plot_hist, plot_scatter,
        plot_grouped_bar, plot_box, plot_line
    )

    print('✅ Helper utilities loaded.')


    # ── Paths ──────────────────────────────────────────────────────
    BASE_DIR = os.path.dirname(os.path.abspath('__file__'))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    CSV_PATH = os.path.join(DATA_DIR, 'employees.csv')
    DB_PATH  = os.path.join(DATA_DIR, 'employees.duckdb')

    print('✅ BASE_DIR:', BASE_DIR)
    print('✅ DATA_DIR:', DATA_DIR)
    print('✅ CSV_PATH:', CSV_PATH)
    print('✅ DB_PATH: ', DB_PATH)
    return (
        CSV_PATH,
        DB_PATH,
        definition,
        duckdb,
        note,
        plot_bar,
        plot_grouped_bar,
        plot_hist,
        plot_line,
        plot_pie,
        plot_scatter,
        section,
        show,
        show_avatars,
        sql_box,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Create the DuckDB database
    """)
    return


@app.cell
def _(DB_PATH, duckdb):
    # ── Open (or create) the DuckDB database ──────────────────────
    con = duckdb.connect(DB_PATH)
    print('✅ DuckDB connected:', DB_PATH)
    print('✅ Helper utilities loaded.')
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🏗️ PART 0 — Build the Database (Idempotent)
    This section runs safely **every time** — it drops and re-creates the table so the notebook is bullet-proof.
    """)
    return


@app.cell
def _(definition, section):
    # ════════════════════════════════════════════════════════════════
    #  CELL 2 — CREATE TABLE FROM CSV
    #  We drop the table if it already exists, then recreate it
    #  by reading the CSV file. This makes the notebook idempotent
    #  (safe to re-run from top to bottom).
    # ════════════════════════════════════════════════════════════════
    section('PART 0 — Create the employees Table from CSV', '🏗️')

    definition('DDL (Data Definition Language)',
               'SQL statements that define the structure of a database '
               '— CREATE TABLE, DROP TABLE, ALTER TABLE.')

    definition('Idempotent',
               'Running the same operation multiple times produces the '
               'same result. Our notebook is idempotent: safe to re-run '
               'from scratch at any time.')
    return


@app.cell
def _(CSV_PATH, con, note, show, sql_box):
    _sql = '''
    -- Step 1: Remove the table if it already exists
    DROP TABLE IF EXISTS employees;

    -- Step 2: Create the table by reading the CSV file directly.
    --         DuckDB automatically infers column types.
    CREATE TABLE employees AS
        SELECT * FROM read_csv_auto('{csv}');
    '''.format(csv=CSV_PATH.replace('\\', '/'))

    print("SQL to create employees table:\n", _sql)

    sql_box(_sql)

    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)
    con.execute(f"CREATE TABLE employees AS SELECT * FROM read_csv_auto('{CSV_PATH.replace(chr(92), '/')}')")
    note(f'Table created successfully from {CSV_PATH}')

    # Verify
    show(con.execute("""
        SELECT *
        FROM employees;
    """), title='employees — All 10 Rows')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ➕ PART 1 — CREATE (INSERT)

    > **CREATE** means adding new rows to an existing table using `INSERT INTO`.

    We'll practise **4 different INSERT patterns**.
    """)
    return


@app.cell
def _(con, definition, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  C-1  INSERT a single new employee
    # ════════════════════════════════════════════════════════════════
    section('C-1 · INSERT a Single Row', '➕')
    definition("""
        INSERT INTO …
        VALUES;
    """,
               'Adds one or more rows to a table. You list the columns '
               'and provide matching values in the same order.')

    note('BEFORE — current row count:')
    show(con.execute("""
        SELECT COUNT(*) AS total_rows
        FROM employees;
    """), title='Row Count BEFORE')

    _sql = """
        INSERT INTO employees
        VALUES ( 11, 'Aisha Patel', 'AI', 198000, 'FEMALE', 'PHD', '2015-10-05', 'USA', 'https://api.dicebear.com/7.x/personas/svg?seed=AishaPatel', 35 );
    """
    sql_box(_sql)
    con.execute(_sql)

    note('AFTER — row count increased by 1:')
    show(con.execute('SELECT COUNT(*) AS total_rows FROM employees'), title='Row Count AFTER')
    show(con.execute("""
        SELECT *
        FROM employees
        WHERE emp_id = 11;
    """), title='The New Row')
    return


@app.cell
def _(con, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  C-2  INSERT multiple rows in one statement
    # ════════════════════════════════════════════════════════════════
    section('C-2 · INSERT Multiple Rows at Once', '➕')
    note('BEFORE:')
    show(con.execute("""
        SELECT COUNT(*) AS total_rows
        FROM employees;
    """), title='Row Count BEFORE')

    _sql = """
        INSERT INTO employees
        VALUES
            (12, 'Carlos Rivera', 'SALES', 91000, 'MALE', 'BS', '2015-03-30', 'CANADA', 'https://api.dicebear.com/7.x/personas/svg?seed=CarlosRivera', 28),
            (13, 'Nina Volkova', 'MARKETING', 87000, 'FEMALE', 'BA', '2015-08-08', 'GERMANY', 'https://api.dicebear.com/7.x/personas/svg?seed=NinaVolkova', 31);
    """
    sql_box(_sql)
    con.execute(_sql)

    note('AFTER — 2 rows added:')
    show(con.execute('SELECT COUNT(*) AS total_rows FROM employees'), title='Row Count AFTER')
    show(con.execute("""
        SELECT *
        FROM employees
        WHERE emp_id IN (12,13);
    """), title='The 2 New Rows')
    return


@app.cell
def _(con, definition, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  C-3  INSERT specifying only certain columns (others get NULL)
    # ════════════════════════════════════════════════════════════════
    section('C-3 · INSERT with Named Columns', '➕')
    definition('Named-column INSERT',
               'You can list only the columns you want to populate. '
               'Unspecified columns receive NULL (or a default value).')

    note('BEFORE:')
    show(con.execute("""
        SELECT *
        FROM employees
        WHERE emp_id = 14;
    """), title='emp_id 14 — BEFORE (should be empty)')

    _sql = '''
    -- Only supply the essential columns; image_url and age will be NULL
    INSERT INTO employees (emp_id, emp_name, department, salary, gender, degree, hire_date, country)
    VALUES (14, 'Tariq Hassan', 'IT', 142000, 'MALE', 'MS', '2015-09-15', 'CANADA');
    '''
    sql_box(_sql)
    con.execute(_sql)

    note('AFTER — notice image_url and age are NULL:')
    show(con.execute('SELECT * FROM employees WHERE emp_id = 14'), title='The New Row (partial insert)')
    return


@app.cell
def _(con, definition, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  C-4  INSERT … SELECT (copy rows from a derived query)
    # ════════════════════════════════════════════════════════════════
    section('C-4 · INSERT … SELECT (Derived Rows)', '➕')
    definition('INSERT … SELECT',
               'You can insert the results of a SELECT query into a table. '
               'This is useful to duplicate, transform, or aggregate rows.')

    # Create a staging table first
    con.execute("""
        DROP TABLE IF EXISTS new_hires;
    """)
    con.execute("""
        CREATE TABLE new_hires AS
        SELECT
            15 AS emp_id,
            'Yuki Tanaka' AS emp_name,
            'AI' AS department,
            175000 AS salary,
            'FEMALE' AS gender,
            'MS' AS degree,
            DATE '2015-11-21' AS hire_date,
            'CHINA' AS country,
            'https://api.dicebear.com/7.x/personas/svg?seed=YukiTanaka' AS image_url,
            29 AS age;
    """)
    note('Staging table new_hires:')
    show(con.execute("""
        SELECT *
        FROM new_hires;
    """), title='Staging Table — new_hires')

    note('BEFORE — checking if emp_id 15 exists:')
    show(con.execute("""
        SELECT COUNT(*) AS cnt
        FROM employees
        WHERE emp_id = 15;
    """), title='Count BEFORE')

    _sql = '''
    -- Copy every row from new_hires into employees
    INSERT INTO employees
        SELECT * FROM new_hires;
    '''
    sql_box(_sql)
    con.execute(_sql)

    note('AFTER:')
    show(con.execute("""
        SELECT *
        FROM employees
        WHERE emp_id = 15;
    """), title='Row Inserted via SELECT')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🔍 PART 2 — READ (SELECT)

    > **READ** means querying the database to retrieve information — the most common operation in SQL.

    We'll cover **4 SELECT patterns** (basic → intermediate).
    """)
    return


@app.cell
def _(con, definition, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  R-1  SELECT all columns — the simplest read
    # ════════════════════════════════════════════════════════════════
    section('R-1 · SELECT * (All Columns)', '🔍')
    definition('SELECT *',
               'Retrieves every column from the table. The asterisk (*) '
               'is a wildcard meaning "all columns".')

    _sql = """
        SELECT *
        FROM employees
        LIMIT 5;
    """
    sql_box(_sql)
    show(con.execute(_sql), title='First 5 Employees')
    return


@app.cell
def _(con, definition, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  R-2  SELECT specific columns with WHERE filter
    # ════════════════════════════════════════════════════════════════
    section('R-2 · SELECT with WHERE Filter', '🔍')
    definition('WHERE clause',
               'Filters rows so that only those matching the condition '
               'are returned. Think of it as a sieve for your data.')

    _sql = '''
    SELECT emp_id, emp_name, department, salary, country
    FROM   employees
    WHERE  salary > 130000
    ORDER  BY salary DESC;
    '''
    sql_box(_sql)
    _result = con.execute(_sql)
    show(_result, title='Employees Earning > $130,000')
    return


@app.cell
def _(con, definition, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  R-3  SELECT with multiple conditions and computed column
    # ════════════════════════════════════════════════════════════════
    section('R-3 · SELECT with AND / OR and Computed Column', '🔍')
    definition('Computed column (alias)',
               'You can create a new column in your result set by writing '
               'an expression and giving it a name with AS.')

    _sql = """
        SELECT
            emp_name,
            department,
            salary,
            ROUND(salary * 0.15, 0) AS bonus_15pct,
            country
        FROM employees
        WHERE (department = 'AI'
        OR department = 'IT')
        AND gender = 'FEMALE'
        ORDER BY salary DESC;
    """
    sql_box(_sql)
    show(con.execute(_sql), title='Female AI / IT Employees + Bonus')
    return


@app.cell
def _(con, note, section, show, show_avatars, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  R-4  SELECT with avatars rendered
    # ════════════════════════════════════════════════════════════════
    section('R-4 · SELECT and Render Avatar Images', '🔍')
    note('We use the image_url column to display employee avatars. '
         'show_avatars() is defined in emp_utils.py.')

    _sql = '''
    SELECT emp_id, emp_name, department, salary, image_url
    FROM   employees
    ORDER  BY salary DESC
    LIMIT  10;
    '''
    sql_box(_sql)
    _result = con.execute(_sql).df()
    show(_result, title='Top-10 Earners')
    show_avatars(_result, name_col='emp_name', url_col='image_url',
                 dept_col='department', salary_col='salary')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ✏️ PART 3 — UPDATE

    > **UPDATE** modifies existing rows.
    > ⚠️ Always use a `WHERE` clause — without it you change **every** row!
    """)
    return


@app.cell
def _(con, definition, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  U-1  UPDATE a single employee's salary
    # ════════════════════════════════════════════════════════════════
    section('U-1 · UPDATE a Single Column for One Row', '✏️')
    definition("""
        UPDATE …
        SET …
        WHERE;
    """,
               'Changes the value of one or more columns in every row '
               'that matches the WHERE condition.')

    note('BEFORE:')
    show(con.execute("""
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        WHERE emp_id = 1;
    """),
         title='BEFORE — James Carter salary')

    sql = '''
    UPDATE employees
    SET    salary = 110000
    WHERE  emp_id = 1;
    '''
    sql_box(sql)
    con.execute(sql)

    note('AFTER:')
    show(con.execute("SELECT emp_id, emp_name, salary FROM employees WHERE emp_id = 1"),
         title='AFTER — James Carter salary updated')
    return


@app.cell
def _(con, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  U-2  UPDATE multiple columns at once
    # ════════════════════════════════════════════════════════════════
    section('U-2 · UPDATE Multiple Columns', '✏️')

    note('BEFORE:')
    show(con.execute("""
        SELECT
            emp_id,
            emp_name,
            department,
            degree
        FROM employees
        WHERE emp_id = 8;
    """),
         title='BEFORE — Li Mei')

    _sql = '''
    UPDATE employees
    SET    department = 'AI',
           degree     = 'MS'
    WHERE  emp_id = 8;
    '''
    sql_box(_sql)
    con.execute(_sql)

    note('AFTER:')
    show(con.execute("SELECT emp_id, emp_name, department, degree FROM employees WHERE emp_id = 8"),
         title='AFTER — Li Mei promoted to AI with MS')
    return


@app.cell
def _(con, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  U-3  UPDATE with a calculated expression (give all SALES a raise)
    # ════════════════════════════════════════════════════════════════
    section('U-3 · UPDATE with a Calculated Expression (Bulk Raise)', '✏️')

    note('BEFORE — SALES salaries:')
    show(con.execute("""
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        WHERE department='SALES';
    """),
         title='BEFORE — SALES Department')

    _sql = '''
    -- Give every SALES employee a 10% raise
    UPDATE employees
    SET    salary = ROUND(salary * 1.10, 0)
    WHERE  department = 'SALES';
    '''
    sql_box(_sql)
    con.execute(_sql)

    note('AFTER — SALES salaries (10% higher):')
    show(con.execute("SELECT emp_id, emp_name, salary FROM employees WHERE department='SALES'"),
         title='AFTER — SALES Department (+10%)')
    return


@app.cell
def _(con, definition, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  U-4  UPDATE using a CASE expression (conditional update)
    # ════════════════════════════════════════════════════════════════
    section('U-4 · UPDATE with CASE (Conditional Transformation)', '✏️')
    definition('CASE … WHEN … THEN … END',
               'A SQL if-else statement inside a query. It lets you '
               'apply different logic to different rows in a single pass.')

    note('BEFORE — degree distribution:')
    show(con.execute("""
        SELECT
            emp_id,
            emp_name,
            degree
        FROM employees
        ORDER BY emp_id
        LIMIT 10;
    """),
         title='BEFORE — Degrees')

    _sql = '''
    -- Relabel degrees: BA/BS → 'UNDERGRADUATE', MIS/MS/PHD → keep as-is
    UPDATE employees
    SET    degree = CASE
                        WHEN degree IN ('BA', 'BS') THEN 'UNDERGRADUATE'
                        ELSE degree
                    END
    WHERE  degree IN ('BA', 'BS');
    '''
    sql_box(_sql)
    con.execute(_sql)

    note('AFTER — BA and BS are now labelled UNDERGRADUATE:')
    show(con.execute("""
        SELECT
            emp_id,
            emp_name,
            degree
        FROM employees
        ORDER BY emp_id;
    """),
         title='AFTER — Updated Degree Labels')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🗑️ PART 4 — DELETE

    > **DELETE** permanently removes rows from a table.
    > ⚠️ There is no "undo" — always double-check your `WHERE` clause first!
    """)
    return


@app.cell
def _(con, definition, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  D-1  DELETE a single row by primary key
    # ════════════════════════════════════════════════════════════════
    section('D-1 · DELETE a Single Row', '🗑️')
    definition("""
        DELETE
        FROM …
        WHERE;
    """,
               'Removes every row that matches the WHERE condition. '
               'Without WHERE, the entire table is wiped!')

    note('BEFORE — row 15 (Yuki Tanaka):')
    show(con.execute("""
        SELECT *
        FROM employees
        WHERE emp_id = 15;
    """),
         title='BEFORE — emp_id 15')

    _sql = """
        DELETE
        FROM employees
        WHERE emp_id = 15;
    """
    sql_box(_sql)
    con.execute(_sql)

    note('AFTER — row 15 is gone:')
    show(con.execute('SELECT * FROM employees WHERE emp_id = 15'),
         title='AFTER — emp_id 15 (should be empty)')
    return


@app.cell
def _(con, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  D-2  DELETE rows matching a condition
    # ════════════════════════════════════════════════════════════════
    section('D-2 · DELETE Rows Matching a Condition', '🗑️')

    note('BEFORE — rows with emp_id > 13:')
    show(con.execute("""
        SELECT
            emp_id,
            emp_name
        FROM employees
        WHERE emp_id > 13
        ORDER BY emp_id;
    """),
         title='BEFORE — IDs > 13')

    _sql = '''
    -- Remove all employees added beyond the original 10
    DELETE FROM employees
    WHERE  emp_id > 13;
    '''
    sql_box(_sql)
    con.execute(_sql)

    note('AFTER:')
    show(con.execute("""
        SELECT
            emp_id,
            emp_name
        FROM employees
        ORDER BY emp_id;
    """),
         title='AFTER — Remaining Employees')
    return


@app.cell
def _(con, definition, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  D-3  DELETE using IN (a list of values)
    # ════════════════════════════════════════════════════════════════
    section('D-3 · DELETE with IN Clause', '🗑️')
    definition('IN clause',
               'Matches a column against a list of values — a compact '
               'alternative to writing many OR conditions.')

    note('BEFORE — rows 11, 12, 13:')
    show(con.execute("""
        SELECT
            emp_id,
            emp_name
        FROM employees
        WHERE emp_id IN (11,12,13);
    """),
         title='BEFORE')

    _sql = """
        DELETE
        FROM employees
        WHERE emp_id IN (11, 12, 13);
    """
    sql_box(_sql)
    con.execute(_sql)

    note('AFTER — back to the original 10 employees:')
    show(con.execute("""
        SELECT COUNT(*) AS total_rows
        FROM employees;
    """), title='Row Count AFTER')
    return


@app.cell
def _(CSV_PATH, con, definition, note, section, show, sql_box):
    # ════════════════════════════════════════════════════════════════
    #  D-4  DELETE using a sub-query (delete below-average earners in IT)
    #       Then RESTORE the table from CSV so later cells still work.
    # ════════════════════════════════════════════════════════════════
    section('D-4 · DELETE with a Sub-Query + Restore', '🗑️')
    definition('Sub-query',
               'A query nested inside another query. Here we use a '
               'sub-query to find the average IT salary, then delete '
               'IT employees who earn below that average.')

    note('BEFORE — IT department:')
    show(con.execute("""
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        WHERE department='IT';
    """),
         title='BEFORE — IT Department')

    _sql = """
        DELETE
        FROM employees
        WHERE department = 'IT'
        AND salary < (
        SELECT AVG(salary)
        FROM employees
        WHERE department = 'IT');
    """
    sql_box(_sql)
    con.execute(_sql)

    note('AFTER — only above-average IT earners remain:')
    show(con.execute("SELECT emp_id, emp_name, salary FROM employees WHERE department='IT'"),
         title='AFTER — IT Department (above average only)')

    # ── Restore the table to original 10 rows for the next sections ──
    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)
    con.execute(f"CREATE TABLE employees AS SELECT * FROM read_csv_auto('{CSV_PATH.replace(chr(92), '/')}')")
    note('✅ Table restored to the original 10 rows for the Query sections below.')
    show(con.execute("""
        SELECT COUNT(*) AS total_rows
        FROM employees;
    """), title='Restored Row Count')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 PART 5 — 10 Basic Queries (SELECT · WHERE · LIMIT)
    """)
    return


@app.cell
def _(con, plot_bar, section, show, sql_box):
    section('Q-01 · All employees ordered by salary (highest first)', '📊')
    _sql = '''
    SELECT emp_id, emp_name, department, salary, country
    FROM   employees
    ORDER  BY salary DESC;
    '''
    sql_box(_sql)
    _r = con.execute(_sql)
    show(_r, title='All Employees — Salary Ranking')
    plot_bar(con.execute(_sql).df().head(10), 'emp_name', 'salary',
             title='Employee Salaries (Highest First)',
             xlabel='Employee', ylabel='Salary ($)', horizontal=True)
    return


@app.cell
def _(con, section, show, sql_box):
    section('Q-02 · Employees from Italy or Germany', '📊')
    _sql = """
        SELECT
            emp_name,
            country,
            department,
            salary
        FROM employees
        WHERE country IN ('ITALY', 'GERMANY')
        ORDER BY country, salary DESC;
    """
    sql_box(_sql)
    show(con.execute(_sql), title='Italy & Germany Employees')
    return


@app.cell
def _(con, plot_bar, section, show, sql_box):
    section('Q-03 · Top-3 highest salaries', '📊')
    _sql = '''
    SELECT emp_name, salary, department
    FROM   employees
    ORDER  BY salary DESC
    LIMIT  3;
    '''
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Top 3 Earners')
    plot_bar(_r, 'emp_name', 'salary', title='Top-3 Earners', ylabel='Salary ($)')
    return


@app.cell
def _(con, section, show, sql_box):
    section('Q-04 · Female employees with a PHD', '📊')
    _sql = '''
    SELECT emp_name, department, salary, country
    FROM   employees
    WHERE  gender = 'FEMALE'
      AND  degree = 'PHD'
    ORDER  BY salary DESC;
    '''
    sql_box(_sql)
    show(con.execute(_sql), title='Female PHD Employees')
    return


@app.cell
def _(con, section, show, sql_box):
    section('Q-05 · Employees hired in Q1 2015 (Jan–Mar)', '📊')
    _sql = '''
    SELECT emp_name, hire_date, department, country
    FROM   employees
    WHERE  hire_date BETWEEN DATE '2015-01-01' AND DATE '2015-03-31'
    ORDER  BY hire_date;
    '''
    sql_box(_sql)
    show(con.execute(_sql), title='Q1 2015 Hires')
    return


@app.cell
def _(con, section, show, sql_box):
    section('Q-06 · Salary range — min, max, and spread', '📊')
    _sql = """
        SELECT
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            ROUND(AVG(salary), 0) AS avg_salary,
            MAX(salary)-MIN(salary) AS salary_spread
        FROM employees;
    """
    sql_box(_sql)
    show(con.execute(_sql), title='Salary Summary Statistics')
    return


@app.cell
def _(con, plot_scatter, section, show, sql_box):
    section('Q-07 · Employees with salary between $90,000 and $150,000', '📊')
    _sql = '''
    SELECT emp_name, salary, department, age
    FROM   employees
    WHERE  salary BETWEEN 90000 AND 150000
    ORDER  BY salary;
    '''
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Mid-Range Earners ($90k – $150k)')
    plot_scatter(_r, 'age', 'salary', title='Age vs Salary (Mid-Range Employees)')
    return


@app.cell
def _(con, section, show, sql_box):
    section('Q-08 · DISTINCT countries in the dataset', '📊')
    _sql = '''
    SELECT DISTINCT country
    FROM   employees
    ORDER  BY country;
    '''
    sql_box(_sql)
    show(con.execute(_sql), title='Distinct Countries')
    return


@app.cell
def _(con, section, show, show_avatars, sql_box):
    section('Q-09 · Employees older than 40 with avatars', '📊')
    _sql = '''
    SELECT emp_name, age, department, salary, image_url
    FROM   employees
    WHERE  age > 40
    ORDER  BY age DESC;
    '''
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Senior Employees (Age > 40)')
    show_avatars(_r, name_col='emp_name', url_col='image_url', dept_col='department', salary_col='salary')
    return


@app.cell
def _(con, plot_pie, section, show, sql_box):
    section('Q-10 · CASE statement — classify salary tier', '📊')
    _sql = '''
    SELECT emp_name,
           salary,
           CASE
               WHEN salary >= 180000 THEN 'Elite'
               WHEN salary >= 120000 THEN 'Senior'
               WHEN salary >= 90000  THEN 'Mid-Level'
               ELSE                       'Junior'
           END AS salary_tier
    FROM   employees
    ORDER  BY salary DESC;
    '''
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Employees with Salary Tier')

    tier_counts = _r['salary_tier'].value_counts().reset_index()
    tier_counts.columns = ['salary_tier','count']
    plot_pie(tier_counts, 'salary_tier', 'count', title='Salary Tier Distribution')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📦 PART 6 — 10 Aggregation Queries (GROUP BY · HAVING · LIMIT)
    """)
    return


@app.cell
def _(con, definition, plot_bar, section, show, sql_box):
    section('A-01 · Average salary by department', '📦')
    definition('GROUP BY',
               'Collapses rows with the same value in a column into '
               'a single summary row. Aggregate functions like AVG, '
               'COUNT, SUM, MIN, MAX are applied to each group.')
    _sql = """
        SELECT
            department,
            COUNT(*) AS headcount,
            ROUND(AVG(salary), 0) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Department Salary Summary')
    plot_bar(_r, 'department', 'avg_salary',
             title='Average Salary by Department', ylabel='Avg Salary ($)')
    return


@app.cell
def _(con, plot_pie, section, show, sql_box):
    section('A-02 · Headcount by country', '📦')
    _sql = """
        SELECT
            country,
            COUNT(*) AS headcount
        FROM employees
        GROUP BY country
        ORDER BY headcount DESC;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Headcount by Country')
    plot_pie(_r, 'country', 'headcount', title='Employee Distribution by Country')
    return


@app.cell
def _(con, plot_grouped_bar, section, show, sql_box):
    section('A-03 · Gender split per department', '📦')
    _sql = """
        SELECT
            department,
            gender,
            COUNT(*) AS cnt
        FROM employees
        GROUP BY department, gender
        ORDER BY department, gender;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Gender Split by Department')
    plot_grouped_bar(_r, 'department', 'cnt', 'gender',
                     title='Gender Split per Department', ylabel='Count')
    return


@app.cell
def _(con, definition, plot_bar, section, show, sql_box):
    section('A-04 · HAVING — departments with avg salary > $130,000', '📦')
    definition('HAVING clause',
               'Filters grouped results — like WHERE, but applied '
               'AFTER the GROUP BY. Use HAVING to filter on aggregate values.')
    _sql = """
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department
        HAVING AVG(salary) > 130000
        ORDER BY avg_salary DESC;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Departments with Avg Salary > $130k')
    plot_bar(_r, 'department', 'avg_salary',
             title='High-Paying Departments (Avg > $130k)', ylabel='Avg Salary ($)')
    return


@app.cell
def _(con, plot_bar, section, show, sql_box):
    section('A-05 · Total salary payroll by country', '📦')
    _sql = """
        SELECT
            country,
            SUM(salary) AS total_payroll,
            COUNT(*) AS headcount
        FROM employees
        GROUP BY country
        ORDER BY total_payroll DESC;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Total Payroll by Country')
    plot_bar(_r, 'country', 'total_payroll',
             title='Total Payroll by Country', ylabel='Total Payroll ($)')
    return


@app.cell
def _(con, plot_bar, section, show, sql_box):
    section('A-06 · Degree distribution across all employees', '📦')
    _sql = """
        SELECT
            degree,
            COUNT(*) AS cnt,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY degree
        ORDER BY avg_salary DESC;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Degree Distribution & Avg Salary')
    plot_bar(_r, 'degree', 'avg_salary',
             title='Avg Salary by Degree', ylabel='Avg Salary ($)')
    return


@app.cell
def _(con, plot_bar, section, show, sql_box):
    section('A-07 · Average age by department', '📦')
    _sql = """
        SELECT
            department,
            ROUND(AVG(age), 1) AS avg_age,
            MIN(age) AS youngest,
            MAX(age) AS oldest
        FROM employees
        GROUP BY department
        ORDER BY avg_age DESC;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Age Profile by Department')
    plot_bar(_r, 'department', 'avg_age',
             title='Average Age by Department', ylabel='Age (years)')
    return


@app.cell
def _(con, plot_hist, section, show, sql_box):
    section('A-08 · Salary histogram — salary buckets', '📦')
    _sql = """
        SELECT
            emp_name,
            salary
        FROM employees
        ORDER BY salary;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Salaries for Histogram')
    plot_hist(_r, 'salary', title='Salary Distribution (Histogram)',
              xlabel='Salary ($)', bins=6)
    return


@app.cell
def _(con, section, show, sql_box):
    section('A-09 · HAVING — countries with more than 1 employee', '📦')
    _sql = """
        SELECT
            country,
            COUNT(*) AS headcount
        FROM employees
        GROUP BY country
        HAVING COUNT(*) > 1
        ORDER BY headcount DESC
        LIMIT 5;
    """
    sql_box(_sql)
    show(con.execute(_sql), title='Countries with > 1 Employee')
    return


@app.cell
def _(con, plot_pie, section, show, sql_box):
    section('A-10 · Top-2 departments by total payroll', '📦')
    _sql = """
        SELECT
            department,
            SUM(salary) AS total_payroll
        FROM employees
        GROUP BY department
        ORDER BY total_payroll DESC
        LIMIT 2;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Top-2 Departments by Payroll')
    plot_pie(_r, 'department', 'total_payroll', title='Top-2 Departments — Payroll Share')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🚀 PART 7 — 10 Intermediate Queries (Ranking · Sub-queries · Window Functions · CTEs)
    """)
    return


@app.cell
def _(con, definition, plot_bar, section, show, sql_box):
    section('I-01 · RANK employees by salary (overall)', '🚀')
    definition('Window Function — RANK()',
               'Assigns a rank to each row within a defined partition/order '
               'without collapsing rows. Ties receive the same rank, '
               'and the next rank is skipped.')
    _sql = """
        SELECT
            emp_name,
            salary,
            department,
            RANK() OVER (
        ORDER BY salary DESC) AS salary_rank
        FROM employees
        ORDER BY salary_rank;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Employees Ranked by Salary')
    plot_bar(_r, 'emp_name', 'salary_rank',
             title='Salary Rank (1 = Highest)', ylabel='Rank', horizontal=False)
    return


@app.cell
def _(con, definition, section, show, sql_box):
    section('I-02 · DENSE_RANK by salary within each department', '🚀')
    definition('DENSE_RANK()',
               'Like RANK() but no gaps after ties — if two employees '
               'tie for rank 1, the next rank is 2 (not 3).')
    _sql = """
        SELECT
            emp_name,
            department,
            salary,
            DENSE_RANK() OVER ( PARTITION BY department
        ORDER BY salary DESC ) AS dept_rank
        FROM employees
        ORDER BY department, dept_rank;
    """
    sql_box(_sql)
    show(con.execute(_sql), title='Salary Rank Within Each Department')
    return


@app.cell
def _(con, definition, plot_line, section, show, sql_box):
    section('I-03 · Running total of salary (by hire_date)', '🚀')
    definition('SUM() … OVER (ORDER BY …)',
               'A cumulative (running) sum window function — each row '
               'shows the total salary accumulated up to that row.')
    _sql = """
        SELECT
            emp_name,
            hire_date,
            salary,
            SUM(salary) OVER (
        ORDER BY hire_date ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW ) AS running_total
        FROM employees
        ORDER BY hire_date;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Running Salary Total (by Hire Date)')
    plot_line(_r, 'emp_name', 'running_total',
              title='Cumulative Payroll as Employees Were Hired',
              xlabel='Employee (in hire order)', ylabel='Cumulative Salary ($)')
    return


@app.cell
def _(con, definition, plot_bar, section, show, sql_box):
    section('I-04 · Sub-query — employees earning above overall average', '🚀')
    definition('Scalar Sub-query',
               'A sub-query that returns a single value. Here we compute '
               'the overall average salary and use it in the WHERE clause.')
    _sql = """
        SELECT
            emp_name,
            salary,
            department,
            salary - (
        SELECT ROUND(AVG(salary),0)
        FROM employees) AS above_avg_by
        FROM employees
        WHERE salary > (
        SELECT AVG(salary)
        FROM employees)
        ORDER BY salary DESC;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Above-Average Earners')
    plot_bar(_r, 'emp_name', 'above_avg_by',
             title='How Much Each Employee Earns Above Average', ylabel='$ Above Average')
    return


@app.cell
def _(con, definition, section, show, sql_box):
    section('I-05 · CTE (Common Table Expression) — department stats', '🚀')
    definition('CTE — WITH clause',
               'A named temporary result set defined before the main '
               'query. CTEs make complex queries more readable by '
               'breaking them into named steps.')
    _sql = """
        WITH dept_stats AS (
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_sal,
            COUNT(*) AS headcount
        FROM employees
        GROUP BY department )
        SELECT
            e.emp_name,
            e.department,
            e.salary,
            ds.avg_sal AS dept_avg,
            e.salary - ds.avg_sal AS diff_from_avg
        FROM employees e
        JOIN dept_stats ds USING (department)
        ORDER BY e.department, e.salary DESC;
    """
    sql_box(_sql)
    show(con.execute(_sql), title='Each Employee vs Their Department Average')
    return


@app.cell
def _(con, definition, plot_bar, section, show, sql_box):
    section('I-06 · NTILE — divide employees into salary quartiles', '🚀')
    definition('NTILE(n)',
               'Divides the rows into n equally-sized buckets and '
               'assigns a bucket number. NTILE(4) creates quartiles.')
    _sql = """
        SELECT
            emp_name,
            salary,
            NTILE(4) OVER (
        ORDER BY salary) AS quartile
        FROM employees
        ORDER BY quartile, salary;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Employees by Salary Quartile')
    q_counts = _r['quartile'].value_counts().sort_index().reset_index()
    q_counts.columns = ['quartile','count']
    q_counts['quartile'] = q_counts['quartile'].astype(str)
    plot_bar(q_counts, 'quartile', 'count', title='Employees per Salary Quartile',
             xlabel='Quartile', ylabel='Count')
    return


@app.cell
def _(con, definition, section, show, sql_box):
    section('I-07 · LAG — compare each employee to the previous one (by salary)', '🚀')
    definition('LAG(col, n)',
               'Returns the value of col from the row that is n rows '
               'before the current row within the window. Useful to '
               'compute differences between consecutive rows.')
    _sql = """
        SELECT
            emp_name,
            salary,
            LAG(salary, 1) OVER (
        ORDER BY salary DESC) AS prev_salary, salary - LAG(salary, 1) OVER (
        ORDER BY salary DESC) AS gap
        FROM employees
        ORDER BY salary DESC;
    """
    sql_box(_sql)
    show(con.execute(_sql), title='Salary Gap Between Consecutive Employees')
    return


@app.cell
def _(con, definition, section, show, sql_box):
    section('I-08 · Correlated sub-query — each employee vs department max salary', '🚀')
    definition('Correlated Sub-query',
               'A sub-query that references a column from the outer query. '
               'It is re-evaluated for each row of the outer query.')
    _sql = """
        SELECT
            e.emp_name,
            e.department,
            e.salary,
            (
        SELECT MAX(salary)
        FROM employees i
        WHERE i.department = e.department) AS dept_max, CASE WHEN e.salary = (
        SELECT MAX(salary)
        FROM employees i
        WHERE i.department = e.department) THEN '⭐ Top Earner' ELSE '' END AS badge
        FROM employees e
        ORDER BY e.department, e.salary DESC;
    """
    sql_box(_sql)
    show(con.execute(_sql), title='Each Employee vs Department Maximum')
    return


@app.cell
def _(con, definition, plot_grouped_bar, section, show, sql_box):
    section('I-09 · Pivot — salary by gender across departments', '🚀')
    definition('PIVOT / conditional aggregation',
               'Rotate rows into columns. We use FILTER (WHERE …) '
               'inside aggregate functions to simulate a pivot table.')
    _sql = """
        SELECT
            department,
            ROUND(AVG(salary) FILTER (
        WHERE gender = 'MALE'), 0) AS avg_male_salary, ROUND(AVG(salary) FILTER (
        WHERE gender = 'FEMALE'), 0) AS avg_female_salary
        FROM employees
        GROUP BY department
        ORDER BY department;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Average Salary: Male vs Female by Department')

    melted = _r.melt(id_vars='department', var_name='gender', value_name='avg_salary')
    plot_grouped_bar(melted, 'department', 'avg_salary', 'gender',
                     title='Male vs Female Avg Salary by Department', ylabel='Avg Salary ($)')
    return


@app.cell
def _(con, section, show, show_avatars, sql_box):
    section('I-10 · Full profile — top earner per department with avatar', '🚀')
    _sql = """
        WITH ranked AS (
        SELECT
            *,
            RANK() OVER (PARTITION BY department
        ORDER BY salary DESC) AS rk
        FROM employees )
        SELECT
            emp_name,
            department,
            salary,
            country,
            degree,
            image_url
        FROM ranked
        WHERE rk = 1
        ORDER BY salary DESC;
    """
    sql_box(_sql)
    _r = con.execute(_sql).df()
    show(_r, title='Top Earner in Each Department')
    show_avatars(_r, name_col='emp_name', url_col='image_url',
                 dept_col='department', salary_col='salary')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ✅ Summary

    | Section | Operations Covered |
    |---------|-------------------|
    | PART 0 | DDL — `CREATE TABLE`, idempotent setup |
    | PART 1 | **C**REATE — 4 INSERT patterns |
    | PART 2 | **R**EAD — 4 SELECT patterns + avatars |
    | PART 3 | **U**PDATE — 4 UPDATE patterns incl. CASE |
    | PART 4 | **D**ELETE — 4 DELETE patterns incl. sub-query |
    | PART 5 | 10 Basic Queries — SELECT, WHERE, LIMIT |
    | PART 6 | 10 Aggregation Queries — GROUP BY, HAVING, LIMIT |
    | PART 7 | 10 Intermediate Queries — RANK, CTE, LAG, PIVOT |

    > 🦆 **DuckDB tip:** Run `con.close()` when you're done to flush all writes to disk.
    """)
    return


@app.cell
def _(DB_PATH, con):
    # ════════════════════════════════════════════════════════════════
    #  FINAL CELL — Close the connection
    # ════════════════════════════════════════════════════════════════
    con.close()
    print('✅ DuckDB connection closed. All changes saved to:', DB_PATH)
    return


if __name__ == "__main__":
    app.run()
