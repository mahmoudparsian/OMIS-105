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
    # CRUD Operations on Employee Data with DuckDB

    **Course:** OMIS 105 — Data Stories  
    **Focus:** INSERT, UPDATE, DELETE — the write side of SQL  
    **Tool:** DuckDB (in-process SQL engine)  

    So far we have used `SELECT` to *read* data. In this notebook we learn
    how to *change* data — adding new rows, modifying existing values, and
    removing rows we no longer need.

    | Operation | SQL Keyword | What It Does |
    |-----------|-------------|-----------------------------------|
    | **C**reate | `INSERT` | Add new rows to a table |
    | **R**ead | `SELECT` | Query / retrieve rows (review) |
    | **U**pdate | `UPDATE` | Change values in existing rows |
    | **D**elete | `DELETE` | Remove rows from a table |

    For every operation we follow a **three-step pattern**:
    1. **BEFORE** — show the relevant data before the change  
    2. **TRANSFORM** — execute the INSERT / UPDATE / DELETE  
    3. **AFTER** — show the same data again to confirm the change  
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 — Environment Setup
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Load libraries, connect to DuckDB, and import our display utilities.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import sys, os

    sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))

    from utils import show, show_query
    from utils import plot_bar, plot_pie, plot_grouped_bar

    con = duckdb.connect(database=':memory:')
    print('DuckDB connected!')
    return (con, plot_bar, plot_pie, show, show_query)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 — Load the Employees Table
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We load the same CSV we used in the exploration notebook.
    This gives us a fresh copy to practise write operations on.
    """)
    return


@app.cell
def _(con, show):
    con.execute("""
        CREATE TABLE employees AS
        SELECT *
        FROM read_csv_auto('data/employees.csv');
    """)

    _df = con.execute("""
        SELECT COUNT(*) AS total_rows
        FROM employees;
    """).fetchdf()
    show(_df, title='Starting Row Count')
    return


@app.cell
def _(con, show):
    # Quick look at the table structure
    _df = con.execute("""
        DESCRIBE employees;
    """).fetchdf()
    show(_df, title='Table Schema')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3 — INSERT: Adding New Rows

    The `INSERT INTO` statement adds one or more new rows to a table.  
    **Syntax:**
    ```sql
    INSERT INTO table_name (col1, col2, ...)
    VALUES (val1, val2, ...)
    ```
    You can also insert multiple rows at once, or insert from a subquery.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### I1: Insert a Single New Employee

    We are hiring **Alice Zhang**, a new data scientist in the AI department.
    Let's add her to the table.

    **What will happen:** A new row appears in the `employees` table with
    `emp_id = 2101`. The total row count goes from 1,100 to 1,101.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BEFORE — check the current highest emp_id and total count
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            MAX(emp_id) AS max_id,
            COUNT(*) AS total_rows
        FROM employees;
    """
    show_query(con, _sql, title='Before Insert — Current Max ID & Count')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — insert Alice Zhang
    """)
    return


@app.cell
def _(con):
    con.execute("""
        INSERT INTO employees (emp_id, emp_name, department, salary, gender, degree, hire_date, country, image_url, age)
        VALUES (2101, 'Alice Zhang', 'AI', 155000, 'FEMALE', 'MS', '2015-06-15', 'CHINA', 'https://api.dicebear.com/7.x/avataaars/svg?seed=alicezhang', 29);
    """)
    print('INSERT executed — 1 row added.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — verify Alice is now in the table
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT *
        FROM employees
        WHERE emp_id = 2101;
    """
    show_query(con, _sql, title='After Insert — Alice Zhang')
    return


@app.cell
def _(con, show_query):
    # Confirm the count went up by 1
    _sql = """
        SELECT
            MAX(emp_id) AS max_id,
            COUNT(*) AS total_rows
        FROM employees;
    """
    show_query(con, _sql, title='After Insert — Updated Count')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### I2: Insert Multiple Employees at Once

    We just hired three people for the new Berlin marketing office.
    SQL lets us insert several rows in a single `VALUES` clause,
    separated by commas.

    **What will happen:** Three new rows are added. The count
    increases from 1,101 to 1,104.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BEFORE — current count and any employees with emp_id > 2100
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            country
        FROM employees
        WHERE emp_id > 2100
        ORDER BY emp_id;
    """
    show_query(con, _sql, title='Before Multi-Insert — IDs > 2100')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — insert three new hires
    """)
    return


@app.cell
def _(con):
    con.execute("""
        INSERT INTO employees (emp_id, emp_name, department, salary, gender, degree, hire_date, country, image_url, age)
        VALUES
            (2102, 'Hans Mueller', 'MARKETING', 112000, 'MALE', 'BS', '2015-09-01', 'GERMANY', 'https://api.dicebear.com/7.x/avataaars/svg?seed=hansm', 34),
            (2103, 'Petra Schneider', 'MARKETING', 118000, 'FEMALE', 'MIS', '2015-09-01', 'GERMANY', 'https://api.dicebear.com/7.x/avataaars/svg?seed=petras', 31),
            (2104, 'Marco Bianchi', 'MARKETING', 105000, 'MALE', 'BA', '2015-09-15', 'ITALY', 'https://api.dicebear.com/7.x/avataaars/svg?seed=marcob', 27);
    """)
    print('INSERT executed — 3 rows added.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — confirm all three appear
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            country
        FROM employees
        WHERE emp_id > 2100
        ORDER BY emp_id;
    """
    show_query(con, _sql, title='After Multi-Insert — New Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### I3: Insert From a Subquery (INSERT … SELECT)

    Sometimes we want to copy rows from one query result into a table.
    For example, let's create a **bonus_recipients** table and populate it
    with every employee whose salary exceeds $200,000.

    **Syntax:**
    ```sql
    INSERT INTO target_table (columns…)
    SELECT columns… FROM source_table WHERE …
    ```

    **What will happen:** A new table is created, then filled with rows
    selected from `employees`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — create the table and insert via subquery
    """)
    return


@app.cell
def _(con):
    # Step 1: Create an empty bonus_recipients table
    con.execute("""
        CREATE TABLE bonus_recipients (
            emp_id     INTEGER,
            emp_name   VARCHAR,
            department VARCHAR,
            salary     INTEGER,
            country    VARCHAR
        );
    """)

    # Step 2: Insert high earners from the employees table
    con.execute("""
        INSERT INTO bonus_recipients (emp_id, emp_name, department, salary, country)
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            country
        FROM employees
        WHERE salary > 200000;
    """)
    print('INSERT ... SELECT executed.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — see who made the bonus list
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT *
        FROM bonus_recipients
        ORDER BY salary DESC;
    """
    show_query(con, _sql, title='Bonus Recipients (Salary > $200K)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### I4: Insert With Only Some Columns Specified

    You don't always have to specify every column. If you omit columns,
    DuckDB fills them with `NULL` (or a default value if one is defined).

    **What will happen:** A new employee is inserted, but `image_url`
    will be `NULL` because we didn't supply it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — insert with missing image_url
    """)
    return


@app.cell
def _(con):
    con.execute("""
        INSERT INTO employees (emp_id, emp_name, department, salary, gender, degree, hire_date, country, age)
        VALUES (2105, 'Raj Patel', 'IT', 142000, 'MALE', 'MS', '2015-07-20', 'INDIA', 35);
    """)
    print('INSERT executed — image_url left as NULL.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — notice the NULL in image_url
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary,
            image_url
        FROM employees
        WHERE emp_id = 2105;
    """
    show_query(con, _sql, title='After Insert — Raj Patel (NULL image_url)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 — UPDATE: Modifying Existing Rows

    The `UPDATE` statement changes values in rows that already exist.  
    **Syntax:**
    ```sql
    UPDATE table_name
    SET    col1 = new_value1,
           col2 = new_value2
    WHERE  condition
    ```

    > **Warning:** If you forget the `WHERE` clause, *every row* in the
    > table gets updated! Always double-check your condition.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U1: Give One Employee a Raise

    Alice Zhang (emp_id 2101) just got promoted — her salary goes
    from $155,000 to $175,000.

    **What will happen:** Only the row where `emp_id = 2101` is changed.
    The `salary` column updates from 155,000 → 175,000.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BEFORE — Alice's current record
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            degree
        FROM employees
        WHERE emp_id = 2101;
    """
    show_query(con, _sql, title='Before Update — Alice Zhang')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — update her salary
    """)
    return


@app.cell
def _(con):
    con.execute("""
        UPDATE employees
        SET salary = 175000
        WHERE emp_id = 2101;
    """)
    print('UPDATE executed — salary changed to $175,000.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — confirm the new salary
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            degree
        FROM employees
        WHERE emp_id = 2101;
    """
    show_query(con, _sql, title='After Update — Alice Zhang (New Salary)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U2: Update Multiple Columns (Department Transfer + Raise)

    Raj Patel (emp_id 2105) is transferring from IT to AI, and his salary
    is being adjusted to $160,000. We also want to fill in his missing
    `image_url`.

    **What will happen:** Three columns change in a single UPDATE statement:
    `department`, `salary`, and `image_url`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BEFORE — Raj's current record (note NULL image_url)
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            image_url
        FROM employees
        WHERE emp_id = 2105;
    """
    show_query(con, _sql, title='Before Update — Raj Patel')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — update department, salary, and image_url
    """)
    return


@app.cell
def _(con):
    con.execute("""
        UPDATE employees
        SET department = 'AI', salary = 160000, image_url = 'https://api.dicebear.com/7.x/avataaars/svg?seed=rajpatel'
        WHERE emp_id = 2105;
    """)
    print('UPDATE executed — 3 columns changed.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — verify all three changes
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            image_url
        FROM employees
        WHERE emp_id = 2105;
    """
    show_query(con, _sql, title='After Update — Raj Patel (Transferred to AI)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U3: Bulk Update — 5% Raise for All SALES Employees

    The company decided to give every employee in the SALES department
    a 5% salary increase.

    **What will happen:** All rows where `department = 'SALES'` will have
    their salary multiplied by 1.05. This affects many rows at once.

    **Key concept:** You can use arithmetic expressions in `SET`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BEFORE — average salary and a sample of SALES employees
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            ROUND(AVG(salary), 0) AS avg_salary_before,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            COUNT(*) AS sales_count
        FROM employees
        WHERE department = 'SALES';
    """
    show_query(con, _sql, title='Before Raise — SALES Summary')
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        WHERE department = 'SALES'
        ORDER BY emp_id
        LIMIT 8;
    """
    show_query(con, _sql, title='Before Raise — SALES Sample (first 8)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — apply the 5% raise
    """)
    return


@app.cell
def _(con):
    con.execute("""
        UPDATE employees
        SET salary = CAST(salary * 1.05 AS INTEGER)
        WHERE department = 'SALES';
    """)
    print('UPDATE executed — 5% raise applied to all SALES employees.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — compare the new averages and sample values
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            ROUND(AVG(salary), 0) AS avg_salary_after,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            COUNT(*) AS sales_count
        FROM employees
        WHERE department = 'SALES';
    """
    show_query(con, _sql, title='After Raise — SALES Summary (compare avg!)')
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        WHERE department = 'SALES'
        ORDER BY emp_id
        LIMIT 8;
    """
    show_query(con, _sql, title='After Raise — SALES Sample (each is 5% higher)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U4: Conditional Update Using CASE

    Instead of a flat raise, the company wants *tiered* raises:
    - Employees in the **IT** department earning **under $120K** get a **10% raise**
    - Those earning **$120K–$160K** get a **5% raise**
    - Those earning **above $160K** get a **3% raise**

    **What will happen:** Different rows in IT get different raises
    depending on their current salary. The `CASE` expression handles the logic.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BEFORE — IT salary distribution
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary,
            CASE WHEN salary < 120000 THEN 'Tier 1 (< $120K) → +10%' WHEN salary <= 160000 THEN 'Tier 2 ($120K-$160K) → +5%' ELSE 'Tier 3 (> $160K) → +3%' END AS raise_tier
        FROM employees
        WHERE department = 'IT'
        ORDER BY salary
        LIMIT 12;
    """
    show_query(con, _sql, title='Before Tiered Raise — IT Employees (with tier preview)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — apply tiered raises using CASE
    """)
    return


@app.cell
def _(con):
    con.execute("""
        UPDATE employees
        SET salary = CAST( CASE WHEN salary < 120000 THEN salary * 1.10 WHEN salary <= 160000 THEN salary * 1.05 ELSE salary * 1.03 END AS INTEGER)
        WHERE department = 'IT';
    """)
    print('UPDATE executed — tiered raises applied to IT department.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — see the adjusted salaries
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary,
            degree
        FROM employees
        WHERE department = 'IT'
        ORDER BY salary
        LIMIT 12;
    """
    show_query(con, _sql, title='After Tiered Raise — IT Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### U5: Update Using a Subquery

    Let's update every employee's salary to the **department average**
    if they are currently earning *below* their department's average.
    We only do this for the **MARKETING** department to keep it contained.

    **What will happen:** Any MARKETING employee earning below the
    department average gets bumped up to exactly the average.

    **Key concept:** The `SET` clause can contain a subquery.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BEFORE — MARKETING salaries vs. their department average
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary,
            (
        SELECT ROUND(AVG(salary), 0)
        FROM employees
        WHERE department = 'MARKETING') AS dept_avg, CASE WHEN salary < (
        SELECT AVG(salary)
        FROM employees
        WHERE department = 'MARKETING') THEN 'BELOW avg → will be raised' ELSE 'AT or ABOVE avg → no change' END AS status
        FROM employees
        WHERE department = 'MARKETING'
        ORDER BY salary
        LIMIT 12;
    """
    show_query(con, _sql, title='Before Subquery Update — MARKETING')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — raise below-average salaries to the average
    """)
    return


@app.cell
def _(con):
    con.execute("""
        UPDATE employees
        SET salary = CAST( (
        SELECT AVG(salary)
        FROM employees
        WHERE department = 'MARKETING') AS INTEGER)
        WHERE department = 'MARKETING'
        AND salary < (
        SELECT AVG(salary)
        FROM employees
        WHERE department = 'MARKETING');
    """)
    print('UPDATE executed — below-average MARKETING salaries raised.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — no one in MARKETING is below average now
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary
        FROM employees
        WHERE department = 'MARKETING'
        ORDER BY salary
        LIMIT 12;
    """
    show_query(con, _sql, title='After Subquery Update — MARKETING (lowest salaries raised)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 — DELETE: Removing Rows

    The `DELETE` statement removes rows from a table.  
    **Syntax:**
    ```sql
    DELETE FROM table_name
    WHERE condition
    ```

    > **Warning:** Omitting the `WHERE` clause deletes *every row*
    > in the table! This is permanent — there is no undo.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D1: Delete a Single Employee

    Marco Bianchi (emp_id 2104) has resigned. We need to remove his
    record from the table.

    **What will happen:** The row with `emp_id = 2104` is removed.
    The total count drops by 1.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BEFORE — verify Marco exists
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            country
        FROM employees
        WHERE emp_id = 2104;
    """
    show_query(con, _sql, title='Before Delete — Marco Bianchi')
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT COUNT(*) AS total_before
        FROM employees;
    """).fetchdf()
    show(_df, title='Row Count Before Delete')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — delete Marco's record
    """)
    return


@app.cell
def _(con):
    con.execute("""
        DELETE
        FROM employees
        WHERE emp_id = 2104;
    """)
    print('DELETE executed — 1 row removed.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — Marco is gone
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            country
        FROM employees
        WHERE emp_id = 2104;
    """
    show_query(con, _sql, title='After Delete — emp_id 2104 (should be empty)')
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT COUNT(*) AS total_after
        FROM employees;
    """).fetchdf()
    show(_df, title='Row Count After Delete (one fewer)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D2: Delete Multiple Rows — Remove Low-Earning BA Holders

    Suppose the company decides to let go all employees with a BA
    degree who earn less than $95,000 (a hypothetical scenario).

    **What will happen:** All rows matching *both* conditions are deleted.
    We'll check how many rows match before and confirm they're gone after.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BEFORE — who matches this criteria?
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT COUNT(*) AS will_be_deleted
        FROM employees
        WHERE degree = 'BA'
        AND salary < 95000;
    """
    show_query(con, _sql, title='Before Delete — Count of BA + Salary < $95K')
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            degree,
            salary,
            department
        FROM employees
        WHERE degree = 'BA'
        AND salary < 95000
        ORDER BY salary
        LIMIT 10;
    """
    show_query(con, _sql, title='Before Delete — Sample of Affected Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — delete the matching rows
    """)
    return


@app.cell
def _(con):
    con.execute("""
        DELETE
        FROM employees
        WHERE degree = 'BA'
        AND salary < 95000;
    """)
    print('DELETE executed — low-earning BA holders removed.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — confirm they're gone
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT COUNT(*) AS remaining_matches
        FROM employees
        WHERE degree = 'BA'
        AND salary < 95000;
    """
    show_query(con, _sql, title='After Delete — Should Be Zero')
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT COUNT(*) AS total_remaining
        FROM employees;
    """).fetchdf()
    show(_df, title='Total Rows Remaining')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D3: Delete Using a Subquery

    Remove employees whose salary is below the *overall company average*
    **and** who are in the CANADA office.

    **Key concept:** The `WHERE` clause uses a subquery to compute
    the company-wide average at delete time.

    **What will happen:** Only CANADA employees earning below the
    company average are removed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BEFORE — who in CANADA earns below the company average?
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary,
            (
        SELECT ROUND(AVG(salary), 0)
        FROM employees) AS company_avg
        FROM employees
        WHERE country = 'CANADA'
        AND salary < (
        SELECT AVG(salary)
        FROM employees)
        ORDER BY salary
        LIMIT 10;
    """
    show_query(con, _sql, title='Before Delete — CANADA Employees Below Company Avg')
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT COUNT(*) AS will_be_deleted
        FROM employees
        WHERE country = 'CANADA'
        AND salary < (
        SELECT AVG(salary)
        FROM employees);
    """
    show_query(con, _sql, title='Count to Be Deleted')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — delete using the subquery condition
    """)
    return


@app.cell
def _(con):
    con.execute("""
        DELETE
        FROM employees
        WHERE country = 'CANADA'
        AND salary < (
        SELECT AVG(salary)
        FROM employees);
    """)
    print('DELETE executed — below-average CANADA employees removed.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — remaining CANADA employees all earn above average
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary,
            degree
        FROM employees
        WHERE country = 'CANADA'
        ORDER BY salary
        LIMIT 10;
    """
    show_query(con, _sql, title='After Delete — Remaining CANADA Employees')
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            COUNT(*) AS canada_remaining,
            ROUND(AVG(salary), 0) AS canada_avg_now
        FROM employees
        WHERE country = 'CANADA';
    """
    show_query(con, _sql, title='CANADA Summary After Cleanup')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### D4: Delete ALL Rows From a Table

    Let's clear out the `bonus_recipients` table we created earlier.
    Omitting the `WHERE` clause removes *everything*.

    **What will happen:** The `bonus_recipients` table becomes empty
    but the table structure still exists.

    > In production databases, you'd use `TRUNCATE TABLE` instead —
    > it's faster for large tables. DuckDB supports both.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BEFORE — how many rows in bonus_recipients?
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT COUNT(*) AS row_count
        FROM bonus_recipients;
    """
    show_query(con, _sql, title='Before Delete All — bonus_recipients Count')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### TRANSFORM — delete everything
    """)
    return


@app.cell
def _(con):
    con.execute("""
        DELETE
        FROM bonus_recipients;
    """)
    print("""
        DELETE executed — ALL rows removed
        FROM bonus_recipients.;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### AFTER — table is empty but still exists
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT COUNT(*) AS row_count
        FROM bonus_recipients;
    """
    show_query(con, _sql, title='After Delete All — bonus_recipients is Empty')
    return


@app.cell
def _(con, show):
    # The table structure is still there
    _df = con.execute("""
        DESCRIBE bonus_recipients;
    """).fetchdf()
    show(_df, title='Table Schema Still Exists')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6 — Post-CRUD Checkpoint: Did Our Changes Stick?

    After all the inserts, updates, and deletes above, let's take stock
    of where our data stands now compared to the original.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT COUNT(*) AS total_employees
        FROM employees;
    """
    show_query(con, _sql, title='Final Employee Count (started at 1,100)')
    return


@app.cell
def _(con, plot_bar, show_query):
    _sql = """
        SELECT
            department,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
    """
    _df = show_query(con, _sql, title='Final Department Summary')
    plot_bar(_df, x='department', y='avg_salary',
             title='Average Salary by Department — After All CRUD Operations',
             ylabel='Average Salary ($)', currency=True)
    return


@app.cell
def _(con, plot_pie, show_query):
    _sql = """
        SELECT
            country,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY country
        ORDER BY emp_count DESC;
    """
    _df = show_query(con, _sql, title='Final Country Distribution')
    plot_pie(_df, labels='country', values='emp_count',
             title='Workforce by Country — After CRUD Operations')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7 — Key Takeaways

    | Concept | Syntax | Tip |
    |---------|--------|-----|
    | Single insert | `INSERT INTO t (cols) VALUES (vals)` | List columns explicitly for clarity |
    | Multi-row insert | `VALUES (row1), (row2), …` | More efficient than multiple statements |
    | Insert from query | `INSERT INTO t SELECT … FROM …` | Great for populating summary tables |
    | Partial insert | Omit columns → they become `NULL` | Useful when data is incomplete |
    | Single-row update | `UPDATE t SET col = val WHERE id = x` | Always use WHERE! |
    | Multi-column update | `SET col1 = v1, col2 = v2` | Change several fields at once |
    | Bulk update | `UPDATE t SET … WHERE condition` | Affects all matching rows |
    | Conditional update | `SET col = CASE … END` | Different logic per row |
    | Subquery update | `SET col = (SELECT …)` | Compute values dynamically |
    | Single delete | `DELETE FROM t WHERE id = x` | Removes exactly one row |
    | Bulk delete | `DELETE FROM t WHERE condition` | Check count before running |
    | Subquery delete | `WHERE col < (SELECT …)` | Dynamic threshold |
    | Delete all | `DELETE FROM t` (no WHERE) | Empties the table — be careful! |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8 — Cleanup
    """)
    return


@app.cell
def _(con):
    con.close()
    print('DuckDB connection closed. Notebook complete!')
    return


if __name__ == "__main__":
    app.run()
