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
    # SQL Fundamentals with DuckDB
    ## A Beginner's Guide for Business Students

    **What is SQL?**  
    SQL (Structured Query Language) is the <br>
    standard language for communicating with <br> 
    databases. Think of a database as a collection <br> 
    of organized tables (like spreadsheets), and SQL <br> 
    as the language you use to ask questions about <br>
    the data in those tables.

    **What is DuckDB?**  
    DuckDB is a fast, lightweight database that <br>
    runs right inside your Python environment — <br>
    no server setup needed. 

    **DuckDB is perfect for learning SQL!**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup: Install and Import DuckDB

    First, let's install DuckDB and set up our environment.
    """)
    return


@app.cell
def _():
    # Install DuckDB (run this once)
    return


@app.cell
def _():
    import duckdb

    # Create a connection to DuckDB (in-memory database)
    con = duckdb.connect()

    print("DuckDB is ready! Version:", duckdb.__version__)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load the CSV File and Create the `employees` Table

    We'll read our CSV file and create a table called **employees**. 

    A table is like a spreadsheet with rows and columns.
    """)
    return


@app.cell
def _(con):
    # Create the employees table from our CSV file
    con.execute("""
        CREATE TABLE employees AS
        SELECT *
        FROM read_csv_auto('employees.csv');
    """)

    print("Table 'employees' created successfully!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART 1: Basic Queries (10 Queries)

    These are the building blocks of SQL. Each query teaches you one fundamental concept.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basic Query 1: SELECT All Columns — View the Entire Table

    **What are we doing?**  

    ```
    We want to see ALL the data in our employees table. 
    The `SELECT *` command means "give me everything" 
    and `FROM employees` tells the database which table 
    to look at.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT *
        FROM employees;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌────────┬──────────┬────────────┬────────┬────────────┬────────┬────────┐
    │ emp_id │ emp_name │ department │ gender │ hire_date  │ degree │ salary │
    │ int64  │ varchar  │  varchar   │varchar │  varchar   │varchar │ int64  │
    ├────────┼──────────┼────────────┼────────┼────────────┼────────┼────────┤
    │    100 │ Alex     │ BUSINESS   │ MALE   │ 02/10/2024 │ PHD    │ 220000 │
    │    200 │ Fred     │ BUSINESS   │ MALE   │ 03/11/2024 │ MIS    │ 170000 │
    │    300 │ Barb     │ BUSINESS   │ FEMALE │ 02/03/2024 │ BS     │ 200000 │
    │    400 │ Rafa     │ SPORTS     │ MALE   │ 03/11/2023 │ MS     │ 270000 │
    │    500 │ Novak    │ SPORTS     │ MALE   │ 01/11/2023 │ MS     │ 250000 │
    │    600 │ Betty    │ SPORTS     │ FEMALE │ 01/11/2023 │ MS     │ 210000 │
    │    700 │ Dara     │ SOFTWARE   │ MALE   │ 03/11/2023 │ MS     │ 220000 │
    │    800 │ David    │ SOFTWARE   │ MALE   │ 01/11/2023 │ MS     │ 200000 │
    │    900 │ Max      │ SOFTWARE   │ MALE   │ 01/11/2023 │ PHD    │ 290000 │
    │    950 │ Jenny    │ SOFTWARE   │ FEMALE │ 01/11/2023 │ MS     │ 180000 │
    ├────────┴──────────┴────────────┴────────┴────────────┴────────┴────────┤
    │ 10 rows                                                      7 columns │
    └────────────────────────────────────────────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basic Query 2: SELECT Specific Columns

    **What are we doing?**  

    ```
    Sometimes you don't need ALL columns. 
    Here we ask for just the employee name and salary. 
    This is like looking at only two columns 
    in a spreadsheet.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            salary
        FROM employees;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────┐
    │ emp_name │ salary │
    │ varchar  │ int64  │
    ├──────────┼────────┤
    │ Alex     │ 220000 │
    │ Fred     │ 170000 │
    │ Barb     │ 200000 │
    │ Rafa     │ 270000 │
    │ Novak    │ 250000 │
    │ Betty    │ 210000 │
    │ Dara     │ 220000 │
    │ David    │ 200000 │
    │ Max      │ 290000 │
    │ Jenny    │ 180000 │
    ├──────────┴────────┤
    │      10 rows      │
    └───────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basic Query 3: WHERE Clause — Filtering Rows

    **What are we doing?**  

    ```
    We want to find only employees who work 
    in the BUSINESS department. The `WHERE` 
    clause acts like a filter — it only shows 
    rows that match the condition.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT *
        FROM employees
        WHERE department = 'BUSINESS';
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌────────┬──────────┬────────────┬────────┬────────────┬────────┬────────┐
    │ emp_id │ emp_name │ department │ gender │ hire_date  │ degree │ salary │
    │ int64  │ varchar  │  varchar   │varchar │  varchar   │varchar │ int64  │
    ├────────┼──────────┼────────────┼────────┼────────────┼────────┼────────┤
    │    100 │ Alex     │ BUSINESS   │ MALE   │ 02/10/2024 │ PHD    │ 220000 │
    │    200 │ Fred     │ BUSINESS   │ MALE   │ 03/11/2024 │ MIS    │ 170000 │
    │    300 │ Barb     │ BUSINESS   │ FEMALE │ 02/03/2024 │ BS     │ 200000 │
    ├────────┴──────────┴────────────┴────────┴────────────┴────────┴────────┤
    │ 3 rows                                                       7 columns │
    └────────────────────────────────────────────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basic Query 4: WHERE with Comparison Operators — Salary Greater Than

    **What are we doing?**  
    ```
    We want to find employees who earn 
    more than $200,000. We use the `>` 
    (greater than) operator to compare numbers.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            department,
            salary
        FROM employees
        WHERE salary > 200000;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────────┬────────┐
    │ emp_name │ department │ salary │
    │ varchar  │  varchar   │ int64  │
    ├──────────┼────────────┼────────┤
    │ Alex     │ BUSINESS   │ 220000 │
    │ Rafa     │ SPORTS     │ 270000 │
    │ Novak    │ SPORTS     │ 250000 │
    │ Betty    │ SPORTS     │ 210000 │
    │ Dara     │ SOFTWARE   │ 220000 │
    │ Max      │ SOFTWARE   │ 290000 │
    ├──────────┴────────────┴────────┤
    │           6 rows               │
    └─────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basic Query 5: ORDER BY — Sorting Results

    **What are we doing?**  

    ```
    We want to see all employees sorted by 
    salary from highest to lowest. 

    `ORDER BY salary DESC` sorts in descending 
    order (biggest first). 

    Use `ASC` for ascending (smallest first — 
    this is the default).
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            salary
        FROM employees
        ORDER BY salary DESC;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────┐
    │ emp_name │ salary │
    │ varchar  │ int64  │
    ├──────────┼────────┤
    │ Max      │ 290000 │
    │ Rafa     │ 270000 │
    │ Novak    │ 250000 │
    │ Alex     │ 220000 │
    │ Dara     │ 220000 │
    │ Betty    │ 210000 │
    │ Barb     │ 200000 │
    │ David    │ 200000 │
    │ Jenny    │ 180000 │
    │ Fred     │ 170000 │
    ├──────────┴────────┤
    │      10 rows      │
    └───────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basic Query 6: LIMIT — Show Only a Few Rows

    **What are we doing?**  

    ```
    Sometimes tables have millions 
    of rows.  The `LIMIT` clause 
    lets you see just the first 
    few rows. 

    Here we get the top 3 
    highest-paid employees.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            salary
        FROM employees
        ORDER BY salary DESC
        LIMIT 3;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────┐
    │ emp_name │ salary │
    │ varchar  │ int64  │
    ├──────────┼────────┤
    │ Max      │ 290000 │
    │ Rafa     │ 270000 │
    │ Novak    │ 250000 │
    ├──────────┴────────┤
    │      3 rows       │
    └───────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basic Query 7: DISTINCT — Finding Unique Values

    **What are we doing?**  
    We want to know what departments exist in our company, without seeing duplicates. `DISTINCT` removes repeated values and shows each unique value only once.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT DISTINCT department
        FROM employees;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌────────────┐
    │ department │
    │  varchar   │
    ├────────────┤
    │ BUSINESS   │
    │ SPORTS     │
    │ SOFTWARE   │
    ├────────────┤
    │   3 rows   │
    └────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basic Query 8: COUNT — Counting Rows

    **What are we doing?**  
    We want to know: how many employees do we have in total? The `COUNT(*)` function counts all rows in the table.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT COUNT(*) AS total_employees
        FROM employees;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌─────────────────┐
    │ total_employees │
    │      int64      │
    ├─────────────────┤
    │              10 │
    ├─────────────────┤
    │     1 row       │
    └─────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basic Query 9: AND / OR — Combining Conditions

    **What are we doing?**  
    We want employees who are in the SOFTWARE department AND earn more than $200,000. The `AND` keyword means BOTH conditions must be true.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            department,
            salary
        FROM employees
        WHERE department = 'SOFTWARE'
        AND salary > 200000;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────────┬────────┐
    │ emp_name │ department │ salary │
    │ varchar  │  varchar   │ int64  │
    ├──────────┼────────────┼────────┤
    │ Dara     │ SOFTWARE   │ 220000 │
    │ Max      │ SOFTWARE   │ 290000 │
    ├──────────┴────────────┴────────┤
    │           2 rows               │
    └─────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basic Query 10: Column Aliases with AS — Renaming Output Columns

    **What are we doing?**  
    Sometimes column names aren't reader-friendly. We use `AS` to give columns nicer display names. Here we also calculate annual salary divided by 12 to show monthly pay.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name AS "Employee Name",
            salary AS "Annual Salary",
            ROUND(salary / 12, 2) AS "Monthly Salary"
        FROM employees;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌───────────────┬───────────────┬────────────────┐
    │ Employee Name │ Annual Salary │ Monthly Salary │
    │    varchar    │     int64     │     double     │
    ├───────────────┼───────────────┼────────────────┤
    │ Alex          │        220000 │       18333.33 │
    │ Fred          │        170000 │       14166.67 │
    │ Barb          │        200000 │       16666.67 │
    │ Rafa          │        270000 │       22500.00 │
    │ Novak         │        250000 │       20833.33 │
    │ Betty         │        210000 │       17500.00 │
    │ Dara          │        220000 │       18333.33 │
    │ David         │        200000 │       16666.67 │
    │ Max           │        290000 │       24166.67 │
    │ Jenny         │        180000 │       15000.00 │
    ├───────────────┴───────────────┴────────────────┤
    │ 10 rows                              3 columns │
    └────────────────────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART 2: Intermediate Queries (10 Queries)

    Now that you know the basics, let's explore more powerful SQL features like grouping, aggregation, and more advanced filtering.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intermediate Query 1: GROUP BY — Counting Employees per Department

    **What are we doing?**  
    We want to know how many employees are in each department. `GROUP BY` groups rows that share the same value, then `COUNT(*)` counts how many rows are in each group.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            department,
            COUNT(*) AS num_employees
        FROM employees
        GROUP BY department;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌────────────┬───────────────┐
    │ department │ num_employees │
    │  varchar   │    int64      │
    ├────────────┼───────────────┤
    │ BUSINESS   │             3 │
    │ SPORTS     │             3 │
    │ SOFTWARE   │             4 │
    ├────────────┴───────────────┤
    │          3 rows            │
    └────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intermediate Query 2: Aggregate Functions — AVG, MIN, MAX, SUM

    **What are we doing?**  
    We want to see salary statistics for each department: the average, minimum, maximum, and total salary. These are called "aggregate functions" because they combine (aggregate) multiple values into one.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY department;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌────────────┬────────────┬────────────┬────────────┬──────────────┐
    │ department │ avg_salary │ min_salary │ max_salary │ total_salary │
    │  varchar   │   double   │   int64    │   int64    │    int128    │
    ├────────────┼────────────┼────────────┼────────────┼──────────────┤
    │ BUSINESS   │   196667.0 │     170000 │     220000 │       590000 │
    │ SPORTS     │   243333.0 │     210000 │     270000 │       730000 │
    │ SOFTWARE   │   222500.0 │     180000 │     290000 │       890000 │
    ├────────────┴────────────┴────────────┴────────────┴──────────────┤
    │ 3 rows                                                 5 columns │
    └──────────────────────────────────────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intermediate Query 3: HAVING — Filtering Groups

    **What are we doing?**  
    We want departments where the average salary is greater than $200,000. `WHERE` filters individual rows, but `HAVING` filters groups after `GROUP BY` is applied.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department
        HAVING avg_salary > 200000;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌────────────┬────────────┐
    │ department │ avg_salary │
    │  varchar   │   double   │
    ├────────────┼────────────┤
    │ SPORTS     │   243333.0 │
    │ SOFTWARE   │   222500.0 │
    ├────────────┴────────────┤
    │         2 rows          │
    └─────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intermediate Query 4: IN Operator — Matching Multiple Values

    **What are we doing?**  
    We want employees who have either a PHD or MS degree. Instead of writing `degree = 'PHD' OR degree = 'MS'`, we can use the cleaner `IN (...)` syntax.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            degree,
            salary
        FROM employees
        WHERE degree IN ('PHD', 'MS')
        ORDER BY degree, salary DESC;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────┬────────┐
    │ emp_name │ degree │ salary │
    │ varchar  │varchar │ int64  │
    ├──────────┼────────┼────────┤
    │ Max      │ PHD    │ 290000 │
    │ Alex     │ PHD    │ 220000 │
    │ Rafa     │ MS     │ 270000 │
    │ Novak    │ MS     │ 250000 │
    │ Dara     │ MS     │ 220000 │
    │ Betty    │ MS     │ 210000 │
    │ David    │ MS     │ 200000 │
    │ Jenny    │ MS     │ 180000 │
    ├──────────┴────────┴────────┤
    │          8 rows            │
    └────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intermediate Query 5: BETWEEN — Range Filtering

    **What are we doing?**  

    ```
    We want employees whose salary is between 
    $200,000 and $250,000 (inclusive). 

    The `BETWEEN` keyword is a shortcut for 
    `salary >= 200000 AND salary <= 250000`.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            department,
            salary
        FROM employees
        WHERE salary BETWEEN 200000
        AND 250000
        ORDER BY salary;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────────┬────────┐
    │ emp_name │ department │ salary │
    │ varchar  │  varchar   │ int64  │
    ├──────────┼────────────┼────────┤
    │ Barb     │ BUSINESS   │ 200000 │
    │ David    │ SOFTWARE   │ 200000 │
    │ Betty    │ SPORTS     │ 210000 │
    │ Alex     │ BUSINESS   │ 220000 │
    │ Dara     │ SOFTWARE   │ 220000 │
    │ Novak    │ SPORTS     │ 250000 │
    ├──────────┴────────────┴────────┤
    │           6 rows               │
    └─────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intermediate Query 6: CASE WHEN — Conditional Logic (Like IF-ELSE)

    **What are we doing?**  

    ```
    We want to categorize employees into 
    salary tiers: 

       "High" (above $250K), 
       "Medium" ($200K-$250K), or 
       "Low" (below $200K). 

    `CASE WHEN` lets us write if-else 
    logic inside SQL.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            salary,
            CASE WHEN salary > 250000 THEN 'High' WHEN salary >= 200000 THEN 'Medium' ELSE 'Low' END AS salary_tier
        FROM employees
        ORDER BY salary DESC;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────┬─────────────┐
    │ emp_name │ salary │ salary_tier │
    │ varchar  │ int64  │   varchar   │
    ├──────────┼────────┼─────────────┤
    │ Max      │ 290000 │ High        │
    │ Rafa     │ 270000 │ High        │
    │ Novak    │ 250000 │ Medium      │
    │ Alex     │ 220000 │ Medium      │
    │ Dara     │ 220000 │ Medium      │
    │ Betty    │ 210000 │ Medium      │
    │ Barb     │ 200000 │ Medium      │
    │ David    │ 200000 │ Medium      │
    │ Jenny    │ 180000 │ Low         │
    │ Fred     │ 170000 │ Low         │
    ├──────────┴────────┴─────────────┤
    │ 10 rows               3 columns │
    └──────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intermediate Query 7: GROUP BY Multiple Columns — Gender Distribution per Department

    **What are we doing?**  

    ```
    We want to see how many male and female 
    employees are in each department. 

    We group by BOTH department and gender 
    to get a breakdown.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            department,
            gender,
            COUNT(*) AS num_employees
        FROM employees
        GROUP BY department, gender
        ORDER BY department, gender;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌────────────┬────────┬───────────────┐
    │ department │ gender │ num_employees │
    │  varchar   │varchar │    int64      │
    ├────────────┼────────┼───────────────┤
    │ BUSINESS   │ FEMALE │             1 │
    │ BUSINESS   │ MALE   │             2 │
    │ SOFTWARE   │ FEMALE │             1 │
    │ SOFTWARE   │ MALE   │             3 │
    │ SPORTS     │ FEMALE │             1 │
    │ SPORTS     │ MALE   │             2 │
    ├────────────┴────────┴───────────────┤
    │             6 rows                  │
    └─────────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intermediate Query 8: Subquery — Find Employees Earning Above Average

    **What are we doing?** 

    ```
    We want to find employees who earn 
    more than the company-wide average salary. 

    A subquery is a query inside another query — 
    the inner query calculates the average, and 
    the outer query uses that result as a filter.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            department,
            salary
        FROM employees
        WHERE salary > (
        SELECT AVG(salary)
        FROM employees)
        ORDER BY salary DESC;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────────┬────────┐
    │ emp_name │ department │ salary │
    │ varchar  │  varchar   │ int64  │
    ├──────────┼────────────┼────────┤
    │ Max      │ SOFTWARE   │ 290000 │
    │ Rafa     │ SPORTS     │ 270000 │
    │ Novak    │ SPORTS     │ 250000 │
    │ Alex     │ BUSINESS   │ 220000 │
    │ Dara     │ SOFTWARE   │ 220000 │
    ├──────────┴────────────┴────────┤
    │           5 rows               │
    └─────────────────────────────────┘
    ```

    *Note: The average salary is $221,000. These 5 employees earn above that.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intermediate Query 9: LIKE — Pattern Matching in Text

    **What are we doing?**  

    ```
    We want to find employees whose names 
    start with the letter 'D'. The `LIKE` 
    operator lets you search for patterns 
    in text. 
                            
    `%` means "any characters" — so `'D%'` 
    means "starts with D followed by anything."
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            department,
            salary
        FROM employees
        WHERE emp_name LIKE 'D%';
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────────┬────────┐
    │ emp_name │ department │ salary │
    │ varchar  │  varchar   │ int64  │
    ├──────────┼────────────┼────────┤
    │ Dara     │ SOFTWARE   │ 220000 │
    │ David    │ SOFTWARE   │ 200000 │
    ├──────────┴────────────┴────────┤
    │           2 rows               │
    └─────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intermediate Query 10: Window Function <br> RANK Employees by Salary Within Each Department

    **What are we doing?**  

    ```
    We want to rank employees by salary 
    within their own department. 

    A window function (`RANK() OVER(...)`) 
    performs calculations across related 
    rows without collapsing them into groups 
    like GROUP BY does.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            department,
            salary,
            RANK() OVER ( PARTITION BY department
        ORDER BY salary DESC ) AS dept_salary_rank
        FROM employees
        ORDER BY department, dept_salary_rank;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────────┬────────┬──────────────────┐
    │ emp_name │ department │ salary │ dept_salary_rank │
    │ varchar  │  varchar   │ int64  │      int64       │
    ├──────────┼────────────┼────────┼──────────────────┤
    │ Alex     │ BUSINESS   │ 220000 │                1 │
    │ Barb     │ BUSINESS   │ 200000 │                2 │
    │ Fred     │ BUSINESS   │ 170000 │                3 │
    │ Max      │ SOFTWARE   │ 290000 │                1 │
    │ Dara     │ SOFTWARE   │ 220000 │                2 │
    │ David    │ SOFTWARE   │ 200000 │                3 │
    │ Jenny    │ SOFTWARE   │ 180000 │                4 │
    │ Rafa     │ SPORTS     │ 270000 │                1 │
    │ Novak    │ SPORTS     │ 250000 │                2 │
    │ Betty    │ SPORTS     │ 210000 │                3 │
    ├──────────┴────────────┴────────┴──────────────────┤
    │ 10 rows                                 4 columns │
    └───────────────────────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART 3: Creating the `employees_with_bonuses` Table

    Now let's create a new table that adds a **bonus** column calculated based on department:

    | Department | Bonus Rate |
    |------------|------------|
    | BUSINESS   | 5% of salary |
    | SPORTS     | 7% of salary |
    | SOFTWARE   | 9% of salary |

    We'll also create a **new_salary** column = salary + bonus.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Creating the Table: employees_with_bonuses

    **What are we doing?**  

    ```
    We are creating a brand new table called 
    `employees_with_bonuses`. 

    This table will have all the original columns 
    PLUS two new ones: `bonus` (calculated using 
    CASE WHEN based on department) and `new_salary` 
    (original salary + bonus). We use `ROUND()` to 
    ensure bonus values are whole numbers.
    ```
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE TABLE employees_with_bonuses AS
        SELECT
            emp_id,
            emp_name,
            department,
            gender,
            hire_date,
            degree,
            salary,
            ROUND( CASE WHEN department = 'BUSINESS' THEN salary * 0.05 WHEN department = 'SPORTS' THEN salary * 0.07 WHEN department = 'SOFTWARE' THEN salary * 0.09 END ) AS bonus,
            salary + ROUND( CASE WHEN department = 'BUSINESS' THEN salary * 0.05 WHEN department = 'SPORTS' THEN salary * 0.07 WHEN department = 'SOFTWARE' THEN salary * 0.09 END ) AS new_salary
        FROM employees;
    """)

    print("Table 'employees_with_bonuses' created successfully!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Viewing the New Table

    **What are we doing?**  
    Let's look at our new table to verify that bonuses and new salaries were calculated correctly.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            emp_name,
            department,
            salary,
            bonus,
            new_salary
        FROM employees_with_bonuses
        ORDER BY department, emp_name;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌──────────┬────────────┬────────┬────────┬────────────┐
    │ emp_name │ department │ salary │ bonus  │ new_salary │
    │ varchar  │  varchar   │ int64  │ double │   double   │
    ├──────────┼────────────┼────────┼────────┼────────────┤
    │ Alex     │ BUSINESS   │ 220000 │  11000 │     231000 │
    │ Barb     │ BUSINESS   │ 200000 │  10000 │     210000 │
    │ Fred     │ BUSINESS   │ 170000 │   8500 │     178500 │
    │ Dara     │ SOFTWARE   │ 220000 │  19800 │     239800 │
    │ David    │ SOFTWARE   │ 200000 │  18000 │     218000 │
    │ Jenny    │ SOFTWARE   │ 180000 │  16200 │     196200 │
    │ Max      │ SOFTWARE   │ 290000 │  26100 │     316100 │
    │ Betty    │ SPORTS     │ 210000 │  14700 │     224700 │
    │ Novak    │ SPORTS     │ 250000 │  17500 │     267500 │
    │ Rafa     │ SPORTS     │ 270000 │  18900 │     288900 │
    ├──────────┴────────────┴────────┴────────┴────────────┤
    │ 10 rows                                    5 columns │
    └──────────────────────────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bonus Summary by Department

    **What are we doing?**  

    ```
    Let's summarize the bonus information by 
    department to see the total and average 
    bonuses paid out per department.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            department,
            COUNT(*) AS num_employees,
            SUM(bonus) AS total_bonus,
            ROUND(AVG(bonus), 0) AS avg_bonus,
            SUM(new_salary) AS total_new_salary
        FROM employees_with_bonuses
        GROUP BY department
        ORDER BY department;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected Output:**
    ```
    ┌────────────┬───────────────┬─────────────┬───────────┬──────────────────┐
    │ department │ num_employees │ total_bonus │ avg_bonus │ total_new_salary │
    │  varchar   │    int64      │   double    │  double   │     double       │
    ├────────────┼───────────────┼─────────────┼───────────┼──────────────────┤
    │ BUSINESS   │             3 │       29500 │      9833 │           619500 │
    │ SOFTWARE   │             4 │       80100 │     20025 │           970100 │
    │ SPORTS     │             3 │       51100 │     17033 │           781100 │
    ├────────────┴───────────────┴─────────────┴───────────┴──────────────────┤
    │ 3 rows                                                        5 columns │
    └─────────────────────────────────────────────────────────────────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary: SQL Concepts Covered

    | Concept | What It Does |
    |---------|-------------|
    | `SELECT` | Choose which columns to display |
    | `FROM` | Specify which table to query |
    | `WHERE` | Filter rows based on conditions |
    | `ORDER BY` | Sort results (ASC or DESC) |
    | `LIMIT` | Show only N rows |
    | `DISTINCT` | Remove duplicate values |
    | `COUNT, AVG, MIN, MAX, SUM` | Aggregate functions |
    | `GROUP BY` | Group rows and apply aggregates |
    | `HAVING` | Filter groups (after GROUP BY) |
    | `IN` | Match against a list of values |
    | `BETWEEN` | Filter within a range |
    | `LIKE` | Pattern matching in text |
    | `CASE WHEN` | Conditional logic (if-else) |
    | `AS` | Rename columns (aliases) |
    | `AND / OR` | Combine multiple conditions |
    | Subqueries | Queries inside queries |
    | Window Functions | Calculations across related rows |
    | `CREATE TABLE AS` | Create new tables from queries |

    ---

    **Congratulations!** You now know the fundamentals of SQL. Practice by modifying these queries — change the conditions, try different columns, and experiment!
    """)
    return


@app.cell
def _(con):
    # Close the connection when you're done
    con.close()
    print("Database connection closed. Great job!")
    return


if __name__ == "__main__":
    app.run()
