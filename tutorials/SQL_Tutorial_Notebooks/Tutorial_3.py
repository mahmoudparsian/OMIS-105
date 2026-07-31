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
    # DuckDB SQL Tutorial — From Zero to Intermediate+
    ## A Comprehensive, Hands-On Guide with 40+ Worked Examples

    **Author**: Dr. Mahmoud Parsian — Santa Clara University

    **Course**: OMIS 105 — Database Management Systems
        
    **Tool**: DuckDB (in-process analytical database)
        
    **Format**: Jupyter Notebook

    ---

    ### What You Will Learn

    This tutorial walks you through **every major SQL feature** supported by DuckDB, progressing from the absolute basics to intermediate-plus analytical queries.

    Every example follows a **three-part pattern**:

    1. **Natural-language question** — the business question we want to answer
    2. **SQL query** — the DuckDB code that answers it
    3. **Result table** — the output, displayed as rows and columns

    ### Prerequisites

    - Python 3.8+ with `duckdb` installed (`pip install duckdb`)
    - Basic familiarity with running Jupyter notebooks

    ### How to Use This Notebook

    Run each cell **in order** — later cells depend on the table created at the beginning. Read the natural-language question first, predict what the SQL should look like, then run the cell to check your answer.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Table of Contents

    ### Part I — Foundations (Basic)
    1. Setting Up DuckDB
    2. Creating a Table & Inserting Data
    3. SELECT — Retrieve All Rows
    4. SELECT Specific Columns
    5. WHERE — Filter Rows
    6. Comparison Operators in WHERE
    7. AND / OR — Compound Filters
    8. ORDER BY — Sorting
    9. LIMIT & OFFSET — Pagination
    10. DISTINCT — Unique Values
    11. IN Operator
    12. BETWEEN Operator
    13. LIKE & ILIKE — Pattern Matching
    14. IS NULL / IS NOT NULL
    15. Column Aliases (AS)

    ### Part II — Aggregation & Grouping (Intermediate)
    16. COUNT, SUM, AVG, MIN, MAX
    17. GROUP BY — Summarize by Category
    18. GROUP BY Multiple Columns
    19. HAVING — Filter Groups
    20. WHERE vs HAVING

    ### Part III — Functions & Expressions (Intermediate)
    21. String Functions
    22. Mathematical Functions
    23. Date & Time Functions
    24. CASE Expressions
    25. COALESCE & NULLIF
    26. Type Casting (CAST / ::)

    ### Part IV — Joins & Subqueries (Intermediate)
    27. Creating a Second Table (departments)
    28. INNER JOIN
    29. LEFT JOIN
    30. RIGHT JOIN & FULL OUTER JOIN
    31. Self-Join
    32. Subqueries in WHERE
    33. Subqueries in FROM (Derived Tables)
    34. Correlated Subqueries

    ### Part V — Advanced SQL (Intermediate+)
    35. Common Table Expressions (CTEs)
    36. Multiple / Chained CTEs
    37. Views — Virtual Tables
    38. Set Operations: UNION, INTERSECT, EXCEPT
    39. Window Functions — ROW_NUMBER
    40. Window Functions — RANK & DENSE_RANK
    41. Window Functions — LAG & LEAD
    42. Window Functions — Running Totals & Moving Averages
    43. Window Functions — NTILE & Percentiles
    44. Window Functions — PERCENT_RANK & CUME_DIST
    45. QUALIFY — Filter Window Results
    46. PIVOT — Rows to Columns
    47. Advanced Analytical Query: Full Employee Report

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART I — FOUNDATIONS (Basic)
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Setting Up DuckDB

    DuckDB is an **in-process** analytical database — no server required.
    It runs entirely inside your Python process, just like SQLite but optimized for analytics.

    **Key advantages**:
    - Zero configuration — no install, no server, no passwords
    - Blazing fast on analytical (OLAP) workloads
    - Full SQL support including window functions, CTEs, and PIVOT
    - Seamless Python integration via the `duckdb` module

    We start by importing DuckDB and creating an **in-memory** database connection.
    """)
    return


@app.cell
def _():
    import duckdb

    # Create an in-memory database connection
    con = duckdb.connect(database=':memory:')
    print("DuckDB connection established successfully!")
    print(f"DuckDB version: {duckdb.__version__}")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Creating a Table & Inserting Data

    ### Natural-Language Query
    > *"Create an employees table with 10 employees, storing their ID, name, department, salary, hire date, city, age, and performance rating."*

    We use `CREATE TABLE` to define the schema and `INSERT INTO` to populate it with 10 rows. This single table will be the foundation for every query in this tutorial.
    """)
    return


@app.cell
def _(con):
    # Create the employees table with appropriate data types and constraints
    con.execute("""
        CREATE TABLE employees (
            id         INTEGER PRIMARY KEY,
            name       VARCHAR NOT NULL,
            department VARCHAR NOT NULL,
            salary     DECIMAL(10,2) NOT NULL,
            hire_date  DATE NOT NULL,
            city       VARCHAR,
            age        INTEGER,
            rating     DECIMAL(3,1)
        );
    """)

    # Insert 10 rows of realistic employee data
    con.execute("""
        INSERT INTO employees
        VALUES
            (1, 'Alice Johnson', 'Engineering', 95000.00, '2019-03-15', 'San Jose', 32, 4.5),
            (2, 'Bob Smith', 'Marketing', 72000.00, '2020-07-01', 'San Francisco', 28, 3.8),
            (3, 'Carol Williams', 'Engineering', 105000.00,'2018-01-10', 'San Jose', 35, 4.9),
            (4, 'David Brown', 'Sales', 68000.00, '2021-06-20', 'Los Angeles', 26, 3.2),
            (5, 'Eva Martinez', 'Marketing', 78000.00, '2019-11-05', 'San Francisco', 30, 4.1),
            (6, 'Frank Lee', 'Engineering', 112000.00,'2017-08-22', 'San Jose', 38, 4.7),
            (7, 'Grace Kim', 'Sales', 71000.00, '2022-02-14', 'Los Angeles', 24, 3.5),
            (8, 'Henry Chen', 'Engineering', 98000.00, '2020-04-30', 'Seattle', 33, 4.3),
            (9, 'Iris Patel', 'HR', 82000.00, '2019-09-12', 'Seattle', 29, 4.0),
            (10, 'Jack Wilson', 'HR', 75000.00, '2023-01-08', NULL, 27, NULL);
    """)

    print("Table 'employees' created with 10 rows.")
    print("Columns: id, name, department, salary, hire_date, city, age, rating")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. SELECT — Retrieve All Rows

    ### Natural-Language Query
    > *"Show me all employees and all their information."*

    ### SQL Concept
    `SELECT *` retrieves every column from the table. The `*` is a wildcard meaning "all columns." While convenient for exploration, in production code you should list columns explicitly.
    """)
    return


@app.cell
def _(con):
    # NL: Show me all employees and all their information.
    # SQL: SELECT * FROM employees

    _result = con.execute("""
        SELECT *
        FROM employees
        ORDER BY id;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell
def _(con):
    # Option 2 — Explicit display
    from IPython.display import display
    _result = con.execute("""
        SELECT *
        FROM employees
        ORDER BY id;
    """).fetchdf()
    display(_result)
    return (_result,)


@app.cell
def _(result):
    # Option 3 — Use tabulate for a styled text table


    from tabulate import tabulate
    def display_as_table(result):
        print(tabulate(result, headers='keys', tablefmt='grid', showindex=False))  
    return (display_as_table,)


@app.cell
def _(con, display_as_table):
    _result = con.execute("""
        SELECT *
        FROM employees
        ORDER BY id;
    """).fetchdf()
    display_as_table(_result)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. SELECT Specific Columns

    ### Natural-Language Query
    > *"Show me just the names and salaries of all employees."*

    ### SQL Concept
    Instead of `SELECT *`, list only the columns you need. This is a best practice — it reduces data transfer, makes queries self-documenting, and protects against schema changes breaking your code.
    """)
    return


@app.cell
def _(con, display_as_table):
    # NL: Show me just the names and salaries of all employees.
    # SQL: SELECT name, salary FROM employees

    _result = con.execute("""
        SELECT
            name,
            salary
        FROM employees
        ORDER BY id;
    """).fetchdf()
    #print(_result.to_string(index=False))
    display_as_table(_result)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. WHERE — Filter Rows

    ### Natural-Language Query
    > *"Which employees work in the Engineering department?"*

    ### SQL Concept
    The `WHERE` clause filters rows **before** they appear in the result. Only rows that satisfy the condition are included. Think of it as a row-level filter.
    """)
    return


@app.cell
def _(con):
    # NL: Which employees work in the Engineering department?
    # SQL: SELECT * FROM employees WHERE department = 'Engineering'

    _result = con.execute("""
        SELECT
            id,
            name,
            department,
            salary,
            city
        FROM employees
        WHERE department = 'Engineering'
        ORDER BY id;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Comparison Operators in WHERE

    ### Natural-Language Query
    > *"Which employees earn more than $80,000?"*

    ### SQL Concept
    SQL supports standard comparison operators: `=`, `!=` (or `<>`), `<`, `>`, `<=`, `>=`. These work on numbers, strings (alphabetical order), and dates (chronological order).
    """)
    return


@app.cell
def _(con):
    # NL: Which employees earn more than $80,000?
    # SQL: SELECT name, salary FROM employees WHERE salary > 80000

    _result = con.execute("""
        SELECT
            name,
            department,
            salary
        FROM employees
        WHERE salary > 80000
        ORDER BY salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. AND / OR — Compound Filters

    ### Natural-Language Query
    > *"Which employees are in Engineering AND earn more than $100,000?"*

    ### SQL Concept
    - `AND` — both conditions must be true
    - `OR` — at least one condition must be true
    - Use parentheses `()` to control evaluation order when mixing AND/OR
    """)
    return


@app.cell
def _(con):
    # NL: Which employees are in Engineering AND earn more than $100,000?
    # SQL: SELECT ... WHERE department = 'Engineering' AND salary > 100000

    _result = con.execute("""
        SELECT
            name,
            department,
            salary
        FROM employees
        WHERE department = 'Engineering'
        AND salary > 100000
        ORDER BY salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    print()

    # Bonus: OR example
    # NL: Which employees are in Sales OR Marketing?
    print("--- Employees in Sales OR Marketing ---")
    _result2 = con.execute("""
        SELECT
            name,
            department,
            salary
        FROM employees
        WHERE department = 'Sales'
        OR department = 'Marketing'
        ORDER BY department, name;
    """).fetchdf()
    print(_result2.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. ORDER BY — Sorting Results

    ### Natural-Language Query
    > *"List all employees sorted by salary from highest to lowest."*

    ### SQL Concept
    - `ORDER BY column ASC` — ascending (default, A→Z, low→high, old→new)
    - `ORDER BY column DESC` — descending (Z→A, high→low, new→old)
    - You can sort by multiple columns: `ORDER BY dept ASC, salary DESC`
    """)
    return


@app.cell
def _(con):
    # NL: List all employees sorted by salary from highest to lowest.
    # SQL: SELECT ... ORDER BY salary DESC

    _result = con.execute("""
        SELECT
            name,
            department,
            salary
        FROM employees
        ORDER BY salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. LIMIT & OFFSET — Pagination

    ### Natural-Language Query
    > *"Show me only the top 3 highest-paid employees."*

    ### SQL Concept
    - `LIMIT n` — return only the first n rows
    - `OFFSET m` — skip the first m rows before returning
    - Combined: `LIMIT 3 OFFSET 3` returns rows 4, 5, 6 — useful for pagination
    """)
    return


@app.cell
def _(con):
    # NL: Show me only the top 3 highest-paid employees.
    # SQL: SELECT ... ORDER BY salary DESC LIMIT 3

    _result = con.execute("""
        SELECT
            name,
            department,
            salary
        FROM employees
        ORDER BY salary DESC
        LIMIT 3;
    """).fetchdf()
    print(_result.to_string(index=False))
    print()

    # Bonus: Page 2 (rows 4-6)
    print("--- Page 2 (LIMIT 3 OFFSET 3) ---")
    _result2 = con.execute("""
        SELECT
            name,
            department,
            salary
        FROM employees
        ORDER BY salary DESC
        LIMIT 3
        OFFSET 3;
    """).fetchdf()
    print(_result2.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. DISTINCT — Unique Values

    ### Natural-Language Query
    > *"What are all the different departments in the company?"*

    ### SQL Concept
    `SELECT DISTINCT` removes duplicate values from the result. It applies to the entire row — if you select multiple columns, it returns unique *combinations*.
    """)
    return


@app.cell
def _(con):
    # NL: What are all the different departments in the company?
    # SQL: SELECT DISTINCT department FROM employees

    _result = con.execute("""
        SELECT DISTINCT department
        FROM employees
        ORDER BY department;
    """).fetchdf()
    print(_result.to_string(index=False))
    print()

    # Bonus: Unique department-city combinations
    print("--- Unique department + city combinations ---")
    _result2 = con.execute("""
        SELECT DISTINCT
            department,
            city
        FROM employees
        WHERE city IS NOT NULL
        ORDER BY department, city;
    """).fetchdf()
    print(_result2.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11. IN Operator

    ### Natural-Language Query
    > *"Show employees who work in Engineering, HR, or Sales."*

    ### SQL Concept
    `IN (value1, value2, ...)` is shorthand for multiple `OR` conditions. It checks if a value matches **any** item in a list. Cleaner and more readable than chaining ORs.
    """)
    return


@app.cell
def _(con):
    # NL: Show employees who work in Engineering, HR, or Sales.
    # SQL: SELECT ... WHERE department IN ('Engineering', 'HR', 'Sales')

    _result = con.execute("""
        SELECT
            name,
            department,
            salary
        FROM employees
        WHERE department IN ('Engineering', 'HR', 'Sales')
        ORDER BY department, name;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12. BETWEEN Operator

    ### Natural-Language Query
    > *"Which employees earn between $70,000 and $90,000 (inclusive)?"*

    ### SQL Concept
    `BETWEEN low AND high` is inclusive on both ends — equivalent to `value >= low AND value <= high`. Works on numbers, dates, and strings.
    """)
    return


@app.cell
def _(con):
    # NL: Which employees earn between $70,000 and $90,000 (inclusive)?
    # SQL: SELECT ... WHERE salary BETWEEN 70000 AND 90000

    _result = con.execute("""
        SELECT
            name,
            department,
            salary
        FROM employees
        WHERE salary BETWEEN 70000
        AND 90000
        ORDER BY salary;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13. LIKE & ILIKE — Pattern Matching

    ### Natural-Language Query
    > *"Find all employees whose name starts with a letter between A and D."*

    ### SQL Concept
    - `LIKE` — case-sensitive pattern matching
    - `ILIKE` — case-insensitive (DuckDB extension)
    - `%` matches zero or more characters
    - `_` matches exactly one character

    | Pattern | Matches |
    |---------|---------|
    | `'A%'` | Starts with A |
    | `'%son'` | Ends with "son" |
    | `'%art%'` | Contains "art" |
    | `'_ob'` | Three chars ending in "ob" |
    """)
    return


@app.cell
def _(con):
    # NL: Find all employees whose name contains 'son'.
    # SQL: SELECT ... WHERE name LIKE '%son%'

    _result = con.execute("""
        SELECT
            name,
            department
        FROM employees
        WHERE name LIKE '%son%'
        ORDER BY name;
    """).fetchdf()
    print("Names containing 'son':")
    print(_result.to_string(index=False))
    print()

    # NL: Find employees whose name starts with a vowel (case-insensitive).
    print("--- Names starting with a vowel (ILIKE) ---")
    _result2 = con.execute("""
        SELECT
            name,
            department
        FROM employees
        WHERE name ILIKE 'a%'
        OR name ILIKE 'e%'
        OR name ILIKE 'i%'
        ORDER BY name;
    """).fetchdf()
    print(_result2.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14. IS NULL / IS NOT NULL

    ### Natural-Language Query
    > *"Which employees have no city on file? Which employees have a performance rating?"*

    ### SQL Concept
    In SQL, `NULL` means "unknown" or "missing." You **cannot** test for NULL with `=` — you must use `IS NULL` or `IS NOT NULL`. This is one of the most common SQL mistakes beginners make.
    """)
    return


@app.cell
def _(con):
    # NL: Which employees have no city on file?
    # SQL: SELECT ... WHERE city IS NULL

    _result = con.execute("""
        SELECT
            name,
            department,
            city,
            rating
        FROM employees
        WHERE city IS NULL;
    """).fetchdf()
    print("Employees with NO city:")
    print(_result.to_string(index=False))
    print()

    # NL: Which employees have a performance rating?
    print("--- Employees WITH a rating ---")
    _result2 = con.execute("""
        SELECT
            name,
            rating
        FROM employees
        WHERE rating IS NOT NULL
        ORDER BY rating DESC;
    """).fetchdf()
    print(_result2.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 15. Column Aliases (AS)

    ### Natural-Language Query
    > *"Show each employee's name and their annual salary labeled as 'annual_pay', plus a computed monthly salary."*

    ### SQL Concept
    `AS` renames a column in the output. Useful for computed columns and making results more readable. DuckDB also allows aliases without `AS` (just a space), but `AS` is clearer.
    """)
    return


@app.cell
def _(con):
    # NL: Show name, annual salary as 'annual_pay', and computed monthly salary.
    # SQL: SELECT name, salary AS annual_pay, salary/12 AS monthly_pay FROM employees

    _result = con.execute("""
        SELECT
            name,
            salary AS annual_pay,
            ROUND(salary / 12, 2) AS monthly_pay
        FROM employees
        ORDER BY annual_pay DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART II — AGGREGATION & GROUPING (Intermediate)
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 16. Aggregate Functions: COUNT, SUM, AVG, MIN, MAX

    ### Natural-Language Query
    > *"How many employees do we have? What is the total payroll? What is the average, minimum, and maximum salary?"*

    ### SQL Concept
    Aggregate functions collapse multiple rows into a single summary value.

    | Function | Purpose |
    |----------|---------|
    | `COUNT(*)` | Number of rows |
    | `COUNT(col)` | Number of non-NULL values in a column |
    | `SUM(col)` | Total of all values |
    | `AVG(col)` | Arithmetic mean |
    | `MIN(col)` | Smallest value |
    | `MAX(col)` | Largest value |
    """)
    return


@app.cell
def _(con):
    # NL: How many employees? Total payroll? Average, min, max salary?
    # SQL: SELECT COUNT(*), SUM(salary), AVG(salary), MIN(salary), MAX(salary)

    _result = con.execute("""
        SELECT
            COUNT(*) AS total_employees,
            SUM(salary) AS total_payroll,
            ROUND(AVG(salary), 2) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            COUNT(rating) AS employees_with_rating,
            ROUND(AVG(rating), 2) AS avg_rating
        FROM employees;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 17. GROUP BY — Summarize by Category

    ### Natural-Language Query
    > *"What is the average salary in each department?"*

    ### SQL Concept
    `GROUP BY` partitions rows into groups based on one or more columns. Each group is then collapsed into a single row by aggregate functions. **Rule**: every column in SELECT must either be in GROUP BY or inside an aggregate function.
    """)
    return


@app.cell
def _(con):
    # NL: What is the average salary in each department?
    # SQL: SELECT department, AVG(salary) FROM employees GROUP BY department

    _result = con.execute("""
        SELECT
            department,
            COUNT(*) AS num_employees,
            ROUND(AVG(salary), 2) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 18. GROUP BY Multiple Columns

    ### Natural-Language Query
    > *"How many employees are in each department-city combination, and what is the total salary for each?"*

    ### SQL Concept
    You can GROUP BY multiple columns to get finer-grained summaries. Each unique combination of the grouped columns creates one row in the output.
    """)
    return


@app.cell
def _(con):
    # NL: How many employees per department-city combo?
    # SQL: SELECT department, city, COUNT(*), SUM(salary) GROUP BY department, city

    _result = con.execute("""
        SELECT
            department,
            city,
            COUNT(*) AS num_employees,
            SUM(salary) AS total_salary
        FROM employees
        WHERE city IS NOT NULL
        GROUP BY department, city
        ORDER BY department, city;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 19. HAVING — Filter Groups

    ### Natural-Language Query
    > *"Which departments have an average salary above $75,000?"*

    ### SQL Concept
    `HAVING` filters **groups** (after aggregation), while `WHERE` filters **rows** (before aggregation). You cannot use aggregate functions in WHERE — that's what HAVING is for.

    **Execution order**: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
    """)
    return


@app.cell
def _(con):
    # NL: Which departments have an average salary above $75,000?
    # SQL: SELECT department, AVG(salary) ... GROUP BY department HAVING AVG(salary) > 75000

    _result = con.execute("""
        SELECT
            department,
            COUNT(*) AS num_employees,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY department
        HAVING AVG(salary) > 75000
        ORDER BY avg_salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 20. WHERE vs HAVING — When to Use Which

    ### Natural-Language Query
    > *"For employees aged 30 or older, which departments have more than 1 such employee?"*

    ### SQL Concept
    This query requires **both** WHERE and HAVING:
    - `WHERE age >= 30` filters individual rows first
    - `HAVING COUNT(*) > 1` filters the resulting groups

    | Clause | Filters | When | Can Use Aggregates? |
    |--------|---------|------|---------------------|
    | WHERE | Individual rows | Before GROUP BY | No |
    | HAVING | Groups | After GROUP BY | Yes |
    """)
    return


@app.cell
def _(con):
    # NL: For employees aged 30+, which departments have more than 1 such employee?
    # SQL: WHERE age >= 30 ... GROUP BY department HAVING COUNT(*) > 1

    _result = con.execute("""
        SELECT
            department,
            COUNT(*) AS senior_count,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        WHERE age >= 30
        GROUP BY department
        HAVING COUNT(*) > 1
        ORDER BY senior_count DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART III — FUNCTIONS & EXPRESSIONS (Intermediate)
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 21. String Functions

    ### Natural-Language Query
    > *"Show each employee's name in uppercase, the length of their name, and their first name only."*

    ### SQL Concept — Common String Functions in DuckDB

    | Function | Purpose | Example |
    |----------|---------|---------|
    | `UPPER(s)` | Uppercase | `UPPER('hello')` → `'HELLO'` |
    | `LOWER(s)` | Lowercase | `LOWER('Hello')` → `'hello'` |
    | `LENGTH(s)` | Character count | `LENGTH('hello')` → `5` |
    | `SUBSTRING(s, start, len)` | Extract portion | `SUBSTRING('hello', 1, 3)` → `'hel'` |
    | `SPLIT_PART(s, delim, n)` | Split and pick | `SPLIT_PART('a-b', '-', 1)` → `'a'` |
    | `CONCAT(a, b)` | Concatenate | `CONCAT('hi', '!')` → `'hi!'` |
    | `REPLACE(s, old, new)` | Replace text | `REPLACE('hello', 'l', 'r')` → `'herro'` |
    | `TRIM(s)` | Remove whitespace | `TRIM('  hi  ')` → `'hi'` |
    """)
    return


@app.cell
def _(con):
    # NL: Show name in uppercase, name length, and first name only.
    # SQL: SELECT UPPER(name), LENGTH(name), SPLIT_PART(name, ' ', 1)

    _result = con.execute("""
        SELECT
            name,
            UPPER(name) AS upper_name,
            LENGTH(name) AS name_length,
            SPLIT_PART(name, ' ', 1) AS first_name,
            SPLIT_PART(name, ' ', 2) AS last_name
        FROM employees
        ORDER BY name_length DESC
        LIMIT 6;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 22. Mathematical Functions

    ### Natural-Language Query
    > *"Show each employee's salary rounded to the nearest thousand, their salary as a percentage of the highest salary, and the absolute difference from the average."*

    ### SQL Concept — Common Math Functions

    | Function | Purpose |
    |----------|---------|
    | `ROUND(x, d)` | Round to d decimal places |
    | `CEIL(x)` / `FLOOR(x)` | Round up / down to integer |
    | `ABS(x)` | Absolute value |
    | `POWER(x, n)` | x raised to the nth power |
    | `SQRT(x)` | Square root |
    | `MOD(x, y)` | Remainder (x % y) |
    """)
    return


@app.cell
def _(con):
    # NL: Salary rounded to nearest thousand, % of max salary, difference from avg.
    # SQL: SELECT name, ROUND(salary, -3), salary*100.0 / MAX(salary) OVER(), ...

    _result = con.execute("""
        SELECT
            name,
            salary,
            ROUND(salary, -3) AS rounded_salary,
            ROUND(salary * 100.0 / MAX(salary) OVER(), 1) AS pct_of_max,
            ROUND(ABS(salary - AVG(salary) OVER()), 2) AS diff_from_avg
        FROM employees
        ORDER BY salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 23. Date & Time Functions

    ### Natural-Language Query
    > *"How long has each employee been with the company (in years and days)? Who was hired in 2019?"*

    ### SQL Concept — Common Date Functions in DuckDB

    | Function | Purpose |
    |----------|---------|
    | `CURRENT_DATE` | Today's date |
    | `EXTRACT(part FROM date)` | Get year, month, day, etc. |
    | `DATEDIFF('unit', d1, d2)` | Difference between two dates |
    | `DATE_PART('part', date)` | Same as EXTRACT |
    | `date + INTERVAL '30 days'` | Date arithmetic |
    | `STRFTIME(fmt, date)` | Format date as string |
    """)
    return


@app.cell
def _(con):
    # NL: How long has each employee been with the company? Who was hired in 2019?
    # SQL: SELECT name, hire_date, DATEDIFF('year', hire_date, CURRENT_DATE), ...

    _result = con.execute("""
        SELECT
            name,
            hire_date,
            EXTRACT(YEAR
        FROM hire_date) AS hire_year, DATEDIFF('year', hire_date, DATE '2026-05-01') AS years_tenure, DATEDIFF('day', hire_date, DATE '2026-05-01') AS days_tenure
        FROM employees
        ORDER BY hire_date;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 24. CASE Expressions — Conditional Logic

    ### Natural-Language Query
    > *"Classify each employee's salary as 'High' (≥100K), 'Medium' (75K–99K), or 'Low' (<75K)."*

    ### SQL Concept
    `CASE` is SQL's if/else. It evaluates conditions top-to-bottom and returns the value for the first matching `WHEN`. `ELSE` handles everything that didn't match.

    ```sql
    CASE
        WHEN condition1 THEN result1
        WHEN condition2 THEN result2
        ELSE default_result
    END
    ```
    """)
    return


@app.cell
def _(con):
    # NL: Classify salary as High (>=100K), Medium (75K-99K), or Low (<75K).
    # SQL: SELECT name, salary, CASE WHEN ... END AS salary_tier

    _result = con.execute("""
        SELECT
            name,
            department,
            salary,
            CASE WHEN salary >= 100000 THEN 'High' WHEN salary >= 75000 THEN 'Medium' ELSE 'Low' END AS salary_tier,
            CASE WHEN rating >= 4.5 THEN 'Excellent' WHEN rating >= 4.0 THEN 'Good' WHEN rating >= 3.0 THEN 'Satisfactory' ELSE 'Needs Review' END AS performance_level
        FROM employees
        ORDER BY salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 25. COALESCE & NULLIF — Handling NULLs Gracefully

    ### Natural-Language Query
    > *"Show all employees, but replace any missing city with 'Unknown' and any missing rating with 0."*

    ### SQL Concept
    - `COALESCE(a, b, c)` — returns the first non-NULL argument
    - `NULLIF(a, b)` — returns NULL if a = b, otherwise returns a

    These are essential for cleaning data and providing sensible defaults.
    """)
    return


@app.cell
def _(con):
    # NL: Replace missing city with 'Unknown' and missing rating with 0.
    # SQL: SELECT name, COALESCE(city, 'Unknown'), COALESCE(rating, 0)

    _result = con.execute("""
        SELECT
            name,
            city,
            COALESCE(city, 'Unknown') AS city_clean,
            rating,
            COALESCE(rating, 0) AS rating_clean
        FROM employees
        WHERE city IS NULL
        OR rating IS NULL;
    """).fetchdf()
    print("Employees with NULL values (before and after COALESCE):")
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 26. Type Casting (CAST / ::)

    ### Natural-Language Query
    > *"Show each employee's salary as an integer (no decimals), and their hire_date as a formatted string."*

    ### SQL Concept
    - `CAST(expr AS type)` — standard SQL casting
    - `expr::type` — DuckDB shorthand (PostgreSQL-style)
    - Common types: `INTEGER`, `VARCHAR`, `DATE`, `DECIMAL(p,s)`, `BOOLEAN`
    """)
    return


@app.cell
def _(con):
    # NL: Show salary as integer and hire_date as a string.
    # SQL: SELECT name, CAST(salary AS INTEGER), hire_date::VARCHAR

    _result = con.execute("""
        SELECT
            name,
            salary,
            CAST(salary AS INTEGER) AS salary_int,
            STRFTIME(hire_date, '%B %d, %Y') AS hire_date_formatted,
            CAST(age AS VARCHAR) || ' years old' AS age_text
        FROM employees
        ORDER BY id
        LIMIT 5;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART IV — JOINS & SUBQUERIES (Intermediate)
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 27. Creating a Second Table — departments

    To demonstrate JOINs, we need a second table. This `departments` table stores department-level information that doesn't belong in the employee table (normalization!).
    """)
    return


@app.cell
def _(con):
    # Create the departments table
    con.execute("""
        CREATE TABLE departments (
            dept_name VARCHAR PRIMARY KEY,
            budget    DECIMAL(12,2),
            manager   VARCHAR,
            floor_num INTEGER
        );
    """)

    con.execute("""
        INSERT INTO departments
        VALUES
            ('Engineering', 500000.00, 'Carol Williams', 3),
            ('Marketing', 200000.00, 'Eva Martinez', 2),
            ('Sales', 180000.00, 'David Brown', 1),
            ('HR', 150000.00, 'Iris Patel', 2),
            ('Finance', 300000.00, 'Lisa Ray', 4);
    """)
    # Note: Finance has no employees — useful for demonstrating LEFT/RIGHT JOIN!

    _result = con.execute("""
        SELECT *
        FROM departments
        ORDER BY dept_name;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 28. INNER JOIN — Matching Rows Only

    ### Natural-Language Query
    > *"Show each employee with their department's budget and floor number."*

    ### SQL Concept
    `INNER JOIN` returns only rows where the join condition matches in **both** tables. Rows from either table with no match are excluded.

    ```
    employees          departments
    ┌──────────┐       ┌─────────────┐
    │ Alice     │──────▶│ Engineering │
    │ Bob       │──────▶│ Marketing   │
    │ ...       │       │ Finance     │  ← No match → excluded
    └──────────┘       └─────────────┘
    ```
    """)
    return


@app.cell
def _(con):
    # NL: Show each employee with their department's budget and floor.
    # SQL: SELECT ... FROM employees INNER JOIN departments ON ...

    _result = con.execute("""
        SELECT
            e.name,
            e.department,
            e.salary,
            d.budget AS dept_budget,
            d.floor_num
        FROM employees e
        INNER
        JOIN departments d ON e.department = d.dept_name
        ORDER BY e.department, e.name;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 29. LEFT JOIN — Keep All Left-Side Rows

    ### Natural-Language Query
    > *"Show ALL departments and their employees — even departments with no employees."*

    ### SQL Concept
    `LEFT JOIN` keeps every row from the left table. If there's no match in the right table, the right-side columns are filled with NULL. This is how you find "gaps" — e.g., departments with no employees.
    """)
    return


@app.cell
def _(con):
    # NL: Show ALL departments and their employees — even if no employees exist.
    # SQL: SELECT ... FROM departments LEFT JOIN employees ON ...

    _result = con.execute("""
        SELECT
            d.dept_name,
            d.budget,
            COALESCE(e.name, '-- No employees --') AS employee_name,
            e.salary
        FROM departments d
        LEFT
        JOIN employees e ON d.dept_name = e.department
        ORDER BY d.dept_name, e.name;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 30. RIGHT JOIN & FULL OUTER JOIN

    ### Natural-Language Query
    > *"Show all department-employee combinations, keeping ALL rows from both sides."*

    ### SQL Concept
    - `RIGHT JOIN` — keeps all rows from the **right** table (mirror of LEFT JOIN)
    - `FULL OUTER JOIN` — keeps all rows from **both** tables, filling NULLs where no match exists
    """)
    return


@app.cell
def _(con):
    # NL: Which departments have no employees? (Using RIGHT JOIN perspective)
    # SQL: SELECT ... FROM employees RIGHT JOIN departments ON ...

    _result = con.execute("""
        SELECT
            d.dept_name,
            COUNT(e.id) AS employee_count,
            COALESCE(SUM(e.salary), 0) AS total_salary
        FROM employees e
        RIGHT
        JOIN departments d ON e.department = d.dept_name
        GROUP BY d.dept_name
        ORDER BY employee_count DESC;
    """).fetchdf()
    print("RIGHT JOIN — All departments (including empty ones):")
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 31. Self-Join — Comparing Rows Within the Same Table

    ### Natural-Language Query
    > *"Find all pairs of employees who work in the same department."*

    ### SQL Concept
    A self-join joins a table to **itself**. You must use **table aliases** (e.g., `e1`, `e2`) to distinguish the two copies. Self-joins are useful for comparisons, hierarchies, and finding duplicates.
    """)
    return


@app.cell
def _(con):
    # NL: Find all pairs of employees in the same department.
    # SQL: SELECT ... FROM employees e1 JOIN employees e2 ON ... AND e1.id < e2.id

    _result = con.execute("""
        SELECT
            e1.name AS employee_1,
            e2.name AS employee_2,
            e1.department,
            ABS(e1.salary - e2.salary) AS salary_diff
        FROM employees e1
        JOIN employees e2 ON e1.department = e2.department
        AND e1.id < e2.id
        ORDER BY e1.department, salary_diff DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 32. Subqueries in WHERE

    ### Natural-Language Query
    > *"Which employees earn more than the company average?"*

    ### SQL Concept
    A **subquery** is a query inside another query. When used in WHERE, the inner query computes a value that the outer query uses as a filter. The subquery runs first, then its result is used in the comparison.
    """)
    return


@app.cell
def _(con):
    # NL: Which employees earn more than the company average?
    # SQL: SELECT ... WHERE salary > (SELECT AVG(salary) FROM employees)

    _result = con.execute("""
        SELECT
            name,
            department,
            salary,
            ROUND(salary - (
        SELECT AVG(salary)
        FROM employees), 2) AS above_avg_by
        FROM employees
        WHERE salary > (
        SELECT AVG(salary)
        FROM employees)
        ORDER BY salary DESC;
    """).fetchdf()
    print(f"Company average salary: $85,600.00")
    print(f"Employees above average:")
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 33. Subqueries in FROM (Derived Tables)

    ### Natural-Language Query
    > *"What is the average of each department's average salary?"*

    ### SQL Concept
    A subquery in `FROM` creates a temporary table (called a **derived table** or **inline view**). The outer query can then query this temporary result as if it were a regular table. This is useful for multi-level aggregation.
    """)
    return


@app.cell
def _(con):
    # NL: What is the average of each department's average salary?
    # SQL: SELECT AVG(avg_salary) FROM (SELECT department, AVG(salary) ... GROUP BY ...)

    _result = con.execute("""
        SELECT
            ROUND(AVG(dept_avg), 2) AS avg_of_dept_avgs,
            MIN(dept_avg) AS lowest_dept_avg,
            MAX(dept_avg) AS highest_dept_avg
        FROM (
        SELECT
            department,
            ROUND(AVG(salary), 2) AS dept_avg
        FROM employees
        GROUP BY department ) dept_summary;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 34. Correlated Subqueries

    ### Natural-Language Query
    > *"Show each employee alongside their department's average salary, and flag if they're above or below it."*

    ### SQL Concept
    A **correlated subquery** references a column from the outer query — it re-executes for each row of the outer query. This is powerful but can be slower than JOINs on large datasets.
    """)
    return


@app.cell
def _(con):
    # NL: Each employee vs their department's average. Above or below?
    # SQL: SELECT ..., (SELECT AVG(salary) FROM employees e2 WHERE e2.department = e1.department)

    _result = con.execute("""
        SELECT
            e1.name,
            e1.department,
            e1.salary,
            ROUND((
        SELECT AVG(e2.salary)
        FROM employees e2
        WHERE e2.department = e1.department), 2) AS dept_avg, CASE WHEN e1.salary > (
        SELECT AVG(e2.salary)
        FROM employees e2
        WHERE e2.department = e1.department) THEN 'Above' ELSE 'Below' END AS vs_dept_avg
        FROM employees e1
        ORDER BY e1.department, e1.salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return (_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART V — ADVANCED SQL (Intermediate+)
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 35. Common Table Expressions (CTEs)

    ### Natural-Language Query
    > *"Calculate the company average salary, then show each employee's salary compared to that average — all in one readable query."*

    ### SQL Concept
    A CTE (`WITH ... AS (...)`) is a **named temporary result** you define at the top of a query. It makes complex queries **readable and modular** — like assigning a variable in a programming language.

    ```sql
    WITH cte_name AS (
        SELECT ...
    )
    SELECT ... FROM cte_name ...
    ```
    """)
    return


@app.cell
def _(con):
    # NL: Calculate company avg, then compare each employee to it.
    # SQL: WITH avg_cte AS (...) SELECT ... FROM employees, avg_cte

    _result = con.execute("""
        WITH company_stats AS (
        SELECT
            ROUND(AVG(salary), 2) AS avg_salary,
            ROUND(AVG(age), 1) AS avg_age
        FROM employees )
        SELECT
            e.name,
            e.salary,
            cs.avg_salary,
            ROUND(e.salary - cs.avg_salary, 2) AS diff_from_avg,
            ROUND((e.salary / cs.avg_salary - 1) * 100, 1) AS pct_diff
        FROM employees e
        CROSS
        JOIN company_stats cs
        ORDER BY e.salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 36. Multiple / Chained CTEs

    ### Natural-Language Query
    > *"First compute each department's stats, then classify departments as 'Large' (3+ people) or 'Small', and finally show only departments where the average salary exceeds the company average."*

    ### SQL Concept
    You can chain multiple CTEs separated by commas. Each CTE can reference any CTE defined before it. This lets you build complex analyses step-by-step, keeping each step clean and readable.
    """)
    return


@app.cell
def _(con):
    # NL: Dept stats → classify by size → filter above company avg.
    # SQL: WITH dept_stats AS (...), classified AS (...) SELECT ...

    _result = con.execute("""
        WITH dept_stats AS (
        SELECT
            department,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY department ), classified AS (
        SELECT
            *,
            CASE WHEN emp_count >= 3 THEN 'Large' ELSE 'Small' END AS dept_size
        FROM dept_stats ), company_avg AS (
        SELECT ROUND(AVG(salary), 2) AS overall_avg
        FROM employees )
        SELECT
            c.department,
            c.emp_count,
            c.avg_salary,
            c.total_salary,
            c.dept_size,
            ca.overall_avg,
            CASE WHEN c.avg_salary > ca.overall_avg THEN 'Yes' ELSE 'No' END AS above_company_avg
        FROM classified c
        CROSS
        JOIN company_avg ca
        ORDER BY c.avg_salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 37. Views — Virtual Tables

    ### Natural-Language Query
    > *"Create a reusable view called 'employee_summary' that I can query like a regular table."*

    ### SQL Concept
    A `VIEW` is a **saved query** that behaves like a table. It doesn't store data — it re-runs the underlying query each time you select from it. Views simplify complex queries, enforce consistency, and can restrict access to sensitive columns.
    """)
    return


@app.cell
def _(con):
    # NL: Create a reusable employee_summary view.
    # SQL: CREATE VIEW employee_summary AS SELECT ...

    con.execute("""
        CREATE
        OR REPLACE VIEW employee_summary AS
        SELECT
            e.name,
            e.department,
            e.salary,
            COALESCE(e.rating, 0) AS rating,
            DATEDIFF('year', e.hire_date, DATE '2026-05-01') AS tenure_years,
            d.budget AS dept_budget,
            ROUND(e.salary * 100.0 / d.budget, 1) AS pct_of_budget
        FROM employees e
        LEFT
        JOIN departments d ON e.department = d.dept_name;
    """)

    # Now query the view just like a table
    _result = con.execute("""
        SELECT *
        FROM employee_summary
        ORDER BY pct_of_budget DESC
        LIMIT 6;
    """).fetchdf()
    print("Querying the employee_summary VIEW:")
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 38. Set Operations: UNION, INTERSECT, EXCEPT

    ### Natural-Language Query
    > *"Which cities appear in the employees table but NOT in a given list of office cities?"*

    ### SQL Concept
    Set operations combine results of two queries with compatible columns:

    | Operation | Returns |
    |-----------|---------|
    | `UNION` | All rows from both (no duplicates) |
    | `UNION ALL` | All rows from both (with duplicates) |
    | `INTERSECT` | Only rows in both |
    | `EXCEPT` | Rows in first but not second |
    """)
    return


@app.cell
def _(con):
    # NL: Combine high-salary and high-rating employees (showing why UNION removes dups).
    # SQL: (SELECT ... WHERE salary > 95000) UNION (SELECT ... WHERE rating > 4.3)

    _result = con.execute("""
        -- High salary employees
        (SELECT name, 'High Salary' AS reason FROM employees WHERE salary > 95000)
        UNION
        -- High rating employees
        (SELECT name, 'High Rating' AS reason FROM employees WHERE rating > 4.3)
        ORDER BY name, reason
    """).fetchdf()
    print("UNION — High salary (>95K) OR high rating (>4.3):")
    print(_result.to_string(index=False))
    print()

    # INTERSECT: employees who are BOTH high salary AND high rating
    _result2 = con.execute("""
        (SELECT name FROM employees WHERE salary > 95000)
        INTERSECT
        (SELECT name FROM employees WHERE rating > 4.3)
    """).fetchdf()
    print("INTERSECT — Both high salary AND high rating:")
    print(_result2.to_string(index=False))
    print()

    # EXCEPT: high salary but NOT high rating
    result3 = con.execute("""
        (SELECT name FROM employees WHERE salary > 95000)
        EXCEPT
        (SELECT name FROM employees WHERE rating > 4.3)
    """).fetchdf()
    print("EXCEPT — High salary but NOT high rating:")
    print(result3.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 39. Window Functions — ROW_NUMBER

    ### Natural-Language Query
    > *"Assign a rank number to each employee within their department, ordered by salary (highest first)."*

    ### SQL Concept
    Window functions perform calculations **across a set of rows** related to the current row, without collapsing them into a single output row (unlike GROUP BY).

    ```sql
    FUNCTION() OVER (
        PARTITION BY column   -- defines the "window" (like GROUP BY but keeps rows)
        ORDER BY column       -- defines the order within each window
    )
    ```

    `ROW_NUMBER()` assigns sequential integers (1, 2, 3...) with no gaps and no ties.
    """)
    return


@app.cell
def _(con):
    # NL: Rank employees within their department by salary (highest first).
    # SQL: ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)

    _result = con.execute("""
        SELECT ROW_NUMBER() OVER (PARTITION BY department
        ORDER BY salary DESC) AS dept_rank, name, department, salary
        FROM employees
        ORDER BY department, dept_rank;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 40. Window Functions — RANK & DENSE_RANK

    ### Natural-Language Query
    > *"Rank all employees by salary across the entire company. Show how RANK skips numbers after ties while DENSE_RANK doesn't."*

    ### SQL Concept

    | Function | Ties | After Tie |
    |----------|------|-----------|
    | `ROW_NUMBER()` | No ties — always unique | Sequential |
    | `RANK()` | Same rank for ties | Skips numbers (1,1,3) |
    | `DENSE_RANK()` | Same rank for ties | No gaps (1,1,2) |
    """)
    return


@app.cell
def _(con):
    # NL: Compare ROW_NUMBER, RANK, and DENSE_RANK across all employees by salary.
    # SQL: ROW_NUMBER() OVER ..., RANK() OVER ..., DENSE_RANK() OVER ...

    _result = con.execute("""
        SELECT
            name,
            salary,
            ROW_NUMBER() OVER (
        ORDER BY salary DESC) AS row_num, RANK() OVER (
        ORDER BY salary DESC) AS rank_val, DENSE_RANK() OVER (
        ORDER BY salary DESC) AS dense_rank_val
        FROM employees
        ORDER BY salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 41. Window Functions — LAG & LEAD

    ### Natural-Language Query
    > *"For each employee (ordered by salary), show the salary of the person just above and just below them."*

    ### SQL Concept
    - `LAG(col, n)` — value from `n` rows **before** the current row
    - `LEAD(col, n)` — value from `n` rows **after** the current row
    - Both accept an optional default value: `LAG(col, 1, 0)` returns 0 instead of NULL

    These are essential for **time-series analysis**, **month-over-month comparisons**, and **gap detection**.
    """)
    return


@app.cell
def _(con):
    # NL: For each employee (by salary), show the salary above and below them.
    # SQL: LAG(salary) OVER (ORDER BY salary DESC), LEAD(salary) OVER (...)

    _result = con.execute("""
        SELECT
            name,
            salary,
            LAG(salary, 1) OVER (
        ORDER BY salary DESC) AS higher_salary, LEAD(salary, 1) OVER (
        ORDER BY salary DESC) AS lower_salary, salary - LEAD(salary, 1) OVER (
        ORDER BY salary DESC) AS gap_to_next
        FROM employees
        ORDER BY salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 42. Window Functions — Running Totals & Moving Averages

    ### Natural-Language Query
    > *"Show a running total of salaries as we go from oldest hire to newest, and a 3-person moving average of salary."*

    ### SQL Concept
    Window frames control which rows are included in the calculation:

    ```sql
    SUM(salary) OVER (
        ORDER BY hire_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  -- running total
    )

    AVG(salary) OVER (
        ORDER BY hire_date
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING  -- 3-row moving average
    )
    ```
    """)
    return


@app.cell
def _(con):
    # NL: Running total and 3-person moving average of salary by hire date.
    # SQL: SUM() OVER (ORDER BY hire_date ROWS ...), AVG() OVER (... ROWS ...)

    _result = con.execute("""
        SELECT
            name,
            hire_date,
            salary,
            SUM(salary) OVER (
        ORDER BY hire_date ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW ) AS running_total, ROUND(AVG(salary) OVER (
        ORDER BY hire_date ROWS BETWEEN 1 PRECEDING
        AND 1 FOLLOWING ), 2) AS moving_avg_3
        FROM employees
        ORDER BY hire_date;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 43. Window Functions — NTILE & Percentiles

    ### Natural-Language Query
    > *"Divide employees into 4 salary quartiles (top 25%, second 25%, etc.)."*

    ### SQL Concept
    `NTILE(n)` divides the result set into `n` roughly equal buckets and assigns a bucket number to each row. With `NTILE(4)`, you get quartiles; `NTILE(100)` gives percentiles.
    """)
    return


@app.cell
def _(con):
    # NL: Divide employees into 4 salary quartiles.
    # SQL: NTILE(4) OVER (ORDER BY salary DESC)

    _result = con.execute("""
        SELECT
            name,
            salary,
            NTILE(4) OVER (
        ORDER BY salary DESC) AS quartile, CASE NTILE(4) OVER (
        ORDER BY salary DESC) WHEN 1 THEN 'Top 25%' WHEN 2 THEN '25-50%' WHEN 3 THEN '50-75%' WHEN 4 THEN 'Bottom 25%' END AS quartile_label
        FROM employees
        ORDER BY salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 44. Window Functions — PERCENT_RANK & CUME_DIST

    ### Natural-Language Query
    > *"What percentile does each employee's salary fall in?"*

    ### SQL Concept
    - `PERCENT_RANK()` — relative rank as a percentage: `(rank - 1) / (total_rows - 1)`
    - `CUME_DIST()` — cumulative distribution: what fraction of rows are ≤ this value

    Both return values between 0 and 1.
    """)
    return


@app.cell
def _(con):
    # NL: What percentile does each employee's salary fall in?
    # SQL: PERCENT_RANK() OVER (ORDER BY salary), CUME_DIST() OVER (...)

    _result = con.execute("""
        SELECT
            name,
            salary,
            ROUND(PERCENT_RANK() OVER (
        ORDER BY salary) * 100, 1) AS pct_rank, ROUND(CUME_DIST() OVER (
        ORDER BY salary) * 100, 1) AS cume_dist_pct
        FROM employees
        ORDER BY salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 45. QUALIFY — Filter Window Function Results (DuckDB Extension)

    ### Natural-Language Query
    > *"Show only the highest-paid employee in each department."*

    ### SQL Concept
    `QUALIFY` is a DuckDB/Snowflake extension that filters rows **after** window functions are computed. Without QUALIFY, you'd need a subquery or CTE. It's to window functions what HAVING is to GROUP BY.

    **Execution order**: FROM → WHERE → GROUP BY → HAVING → **Window Functions** → **QUALIFY** → SELECT → ORDER BY
    """)
    return


@app.cell
def _(con):
    # NL: Show only the highest-paid employee in each department.
    # SQL: SELECT ... QUALIFY ROW_NUMBER() OVER (...) = 1

    _result = con.execute("""
        SELECT
            name,
            department,
            salary,
            rating
        FROM employees QUALIFY ROW_NUMBER() OVER (PARTITION BY department
        ORDER BY salary DESC) = 1
        ORDER BY salary DESC;
    """).fetchdf()
    print("Top earner per department (using QUALIFY):")
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 46. PIVOT — Transform Rows into Columns (DuckDB Extension)

    ### Natural-Language Query
    > *"Create a cross-tab showing the number of employees in each department-city combination, with cities as columns."*

    ### SQL Concept
    `PIVOT` rotates rows into columns — creating a **cross-tabulation** (crosstab). This is the SQL equivalent of a pivot table in Excel. DuckDB supports native PIVOT syntax, which is much cleaner than the traditional CASE-based approach.
    """)
    return


@app.cell
def _(con):
    # NL: Cross-tab of department × city (employee counts).
    # SQL: PIVOT ... ON city USING COUNT(*)

    # Using traditional CASE approach (works in all SQL databases)
    _result = con.execute("""
        SELECT
            department,
            COUNT(CASE WHEN city = 'San Jose' THEN 1 END) AS San_Jose,
            COUNT(CASE WHEN city = 'San Francisco' THEN 1 END) AS San_Francisco,
            COUNT(CASE WHEN city = 'Los Angeles' THEN 1 END) AS Los_Angeles,
            COUNT(CASE WHEN city = 'Seattle' THEN 1 END) AS Seattle,
            COUNT(*) AS Total
        FROM employees
        GROUP BY department
        ORDER BY department;
    """).fetchdf()
    print("Department × City cross-tabulation:")
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 47. Advanced Analytical Query — Full Employee Report

    ### Natural-Language Query
    > *"Build a comprehensive employee report that shows: each employee's name, department, salary, their rank within the department, their salary as a percentage of the department total, whether they're above or below the department average, their tenure in years, and their salary quartile company-wide."*

    ### SQL Concept
    This query combines **everything** we've learned: JOINs, CTEs, CASE, window functions, aggregates, and string functions — into a single, powerful analytical report.
    """)
    return


@app.cell
def _(con):
    # NL: Comprehensive employee report combining all techniques.
    # SQL: CTE + JOIN + Window Functions + CASE + Aggregates

    _result = con.execute("""
        WITH dept_stats AS (
        SELECT
            department,
            COUNT(*) AS dept_size,
            ROUND(AVG(salary), 2) AS dept_avg_salary,
            SUM(salary) AS dept_total_salary
        FROM employees
        GROUP BY department )
        SELECT
            e.name,
            e.department AS dept,
            e.salary,
            ds.dept_avg_salary AS dept_avg,
            /* Rank within department */ ROW_NUMBER() OVER ( PARTITION BY e.department
        ORDER BY e.salary DESC ) AS dept_rank, /* Salary as % of department total */ ROUND(e.salary * 100.0 / ds.dept_total_salary, 1) AS pct_of_dept, /* Above or below department average */ CASE WHEN e.salary >= ds.dept_avg_salary THEN '↑ Above' ELSE '↓ Below' END AS vs_avg, /* Tenure */ DATEDIFF('year', e.hire_date, DATE '2026-05-01') AS tenure_yrs, /* Company-wide quartile */ CASE NTILE(4) OVER (
        ORDER BY e.salary DESC) WHEN 1 THEN 'Q1 (Top)' WHEN 2 THEN 'Q2' WHEN 3 THEN 'Q3' WHEN 4 THEN 'Q4 (Bottom)' END AS quartile
        FROM employees e
        JOIN dept_stats ds ON e.department = ds.department
        ORDER BY e.department, e.salary DESC;
    """).fetchdf()
    print(_result.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # SQL Quick Reference — Cheat Sheet
    ---

    ## Clause Execution Order

    ```
    1. FROM        — Which table(s)?
    2. JOIN        — Combine tables
    3. WHERE       — Filter individual rows
    4. GROUP BY    — Create groups
    5. HAVING      — Filter groups
    6. SELECT      — Choose columns
    7. Window Fns  — Compute over partitions
    8. QUALIFY     — Filter window results
    9. DISTINCT    — Remove duplicates
    10. ORDER BY   — Sort results
    11. LIMIT      — Restrict output rows
    ```

    ## Key Syntax Patterns

    | Pattern | Example |
    |---------|---------|
    | Basic select | `SELECT col FROM table WHERE condition` |
    | Aggregation | `SELECT dept, AVG(salary) FROM emp GROUP BY dept` |
    | Filtered groups | `... GROUP BY dept HAVING COUNT(*) > 2` |
    | Join | `SELECT ... FROM a JOIN b ON a.key = b.key` |
    | Subquery | `WHERE salary > (SELECT AVG(salary) FROM emp)` |
    | CTE | `WITH cte AS (SELECT ...) SELECT ... FROM cte` |
    | Window function | `ROW_NUMBER() OVER (PARTITION BY dept ORDER BY sal DESC)` |
    | Running total | `SUM(sal) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING)` |
    | Top-N per group | `QUALIFY ROW_NUMBER() OVER (...) <= N` |

    ## DuckDB-Specific Features Used in This Tutorial

    | Feature | Description |
    |---------|-------------|
    | `ILIKE` | Case-insensitive LIKE |
    | `QUALIFY` | Filter after window functions |
    | `PIVOT` | Native row-to-column transformation |
    | `::type` | PostgreSQL-style casting shorthand |
    | `STRFTIME` | Date formatting |
    | In-memory mode | `duckdb.connect(':memory:')` |

    ---

    ## What's Next?

    Now that you've mastered SQL fundamentals through intermediate+ topics, here are suggested next steps:

    1. **Practice**: Try modifying these queries — change filters, add columns, combine techniques
    2. **Normalization**: Learn to design multi-table schemas (1NF, 2NF, 3NF)
    3. **Transactions**: Understand ACID properties and BEGIN/COMMIT/ROLLBACK
    4. **Indexing**: Learn how B-Tree indexes speed up queries
    5. **Real datasets**: Load CSV/Parquet files into DuckDB and analyze them
    6. **DuckDB extensions**: Explore httpfs, spatial, and JSON extensions

    ---

    * Tutorial by Dr. Mahmoud Parsian 

    * Course: OMIS 105, Santa Clara University

    * Built with DuckDB and Jupyter Notebooks
    """)
    return


@app.cell
def _(con):
    # Clean up: close the connection
    con.close()
    print("DuckDB connection closed. Tutorial complete!")
    print(f"Total examples covered: 47 topics")
    print(f"Progression: Basic (15) → Intermediate (11) → Intermediate+ (13) → Cheat Sheet")
    return


if __name__ == "__main__":
    app.run()
