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
    # 🦆 DuckDB SQL 101 — A Jupyter Notebook Tutorial

    Welcome! In this hands-on tutorial you will learn **basic-to-intermediate SQL** using
    [DuckDB](https://duckdb.org/), a fast, in-process analytical database.

    First Jupyter/Notebook/DuckDB 101:

    ```
    Use the following table, and create 20 
    employee records with 4 departments:

       SALES, MARKETING, IT, SOFTWARE
    ```

    ```sql
    CREATE TABLE employees (
        employee_id INT PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        department VARCHAR(50),
        salary DECIMAL(10, 2),
        hire_date DATE
    );
    ```

    ```
    The focus is basic SQL operations using DuckDB. 

    For each cell of notebook: 

       1. tell what is the NL query, 

       2. what is the solution in sql/duckdb, 

       3. the results as a table of rows and columns
          (as a very nice formatted table). 
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # What we'll cover:

    1. Installing & connecting to DuckDB
    2. Creating a table & inserting data
    3. `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`
    4. Aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`)
    5. `GROUP BY` and the **`HAVING`** clause
    6. `DISTINCT`, `BETWEEN`, `IN`, `LIKE`
    7. `CASE` expressions & computed columns
    8. Subqueries & common patterns

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 — Setup: Install & Import DuckDB

    **Natural-language query:** *Install the DuckDB library and import it.*
    """)
    return


@app.cell
def _():
    # Install DuckDB (run once)
    # !pip install duckdb

    import duckdb

    # Create an in-memory database connection
    con = duckdb.connect(database=':memory:')
    print(f'DuckDB version: {duckdb.__version__}')
    print('Connected to in-memory database ✓')
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 — Create the `employees` Table

    **NL query:** *Create a table to store employee records with id, name, department, salary, and hire date.*
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE TABLE employees (
            employee_id INT PRIMARY KEY,
            first_name  VARCHAR(50),
            last_name   VARCHAR(50),
            department  VARCHAR(50),
            salary      DECIMAL(10, 2),
            hire_date   DATE
        );
    """)
    print('Table employees created ✓')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 — Insert 20 Employee Records

    **NL query:** *Populate the table with 20 employees across 4 departments: SALES, MARKETING, IT, SOFTWARE.*
    """)
    return


@app.cell
def _(con):
    con.execute("""
        INSERT INTO employees
        VALUES
            (1, 'Alice', 'Johnson', 'SALES', 72000.00, '2020-03-15'),
            (2, 'Bob', 'Smith', 'MARKETING', 65000.00, '2019-07-22'),
            (3, 'Carol', 'Williams', 'IT', 88000.00, '2018-01-10'),
            (4, 'David', 'Brown', 'SOFTWARE', 95000.00, '2021-06-01'),
            (5, 'Eve', 'Davis', 'SALES', 68000.00, '2022-02-14'),
            (6, 'Frank', 'Miller', 'MARKETING', 71000.00, '2020-09-30'),
            (7, 'Grace', 'Wilson', 'IT', 92000.00, '2017-11-05'),
            (8, 'Henry', 'Moore', 'SOFTWARE', 105000.00, '2019-04-18'),
            (9, 'Irene', 'Taylor', 'SALES', 74000.00, '2021-08-25'),
            (10, 'Jack', 'Anderson', 'MARKETING', 62000.00, '2023-01-09'),
            (11, 'Karen', 'Thomas', 'IT', 85000.00, '2020-05-20'),
            (12, 'Leo', 'Jackson', 'SOFTWARE', 98000.00, '2018-12-03'),
            (13, 'Mona', 'White', 'SALES', 69500.00, '2022-07-11'),
            (14, 'Nathan', 'Harris', 'MARKETING', 67000.00, '2021-03-27'),
            (15, 'Olivia', 'Martin', 'IT', 91000.00, '2019-10-14'),
            (16, 'Paul', 'Garcia', 'SOFTWARE', 102000.00, '2020-01-06'),
            (17, 'Quinn', 'Martinez', 'SALES', 73000.00, '2023-04-02'),
            (18, 'Rachel', 'Robinson', 'MARKETING', 70000.00, '2022-11-19'),
            (19, 'Steve', 'Clark', 'IT', 87000.00, '2021-09-08'),
            (20, 'Tina', 'Lewis', 'SOFTWARE', 99000.00, '2020-08-12');
    """)
    print('20 rows inserted ✓')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Helper — Pretty-Print Query Results

    We define a small helper so every query result renders as a **nicely formatted HTML table**.
    """)
    return


@app.cell
def _(con):
    from IPython.display import display, HTML

    def run(sql, title=""):
        """Execute SQL and display the result as a styled HTML table."""
        result = con.execute(sql).fetchall()
        cols   = [desc[0] for desc in con.execute(sql).description]

        css = "border-collapse:collapse;font-family:monospace;font-size:13px;margin:8px 0"
        th  = "background:#4a90d9;color:#fff;padding:6px 14px;text-align:left;border:1px solid #ddd"
        td  = "padding:6px 14px;border:1px solid #ddd"

        header = "".join(f'<th style="{th}">{c}</th>' for c in cols)
        rows = ""
        for i, row in enumerate(result):
            bg = 'style="background:#f4f8fc"' if i % 2 == 1 else ""
            cells = "".join(f'<td style="{td}">{v}</td>' for v in row)
            rows += f"<tr {bg}>{cells}</tr>\n"

        caption = f'<caption style="text-align:left;font-weight:bold;padding:4px 0">{title}</caption>' if title else ""
        html = f'<table style="{css}">{caption}<tr>{header}</tr>{rows}</table>'
        display(HTML(html))
        print(f"({len(result)} row{'s' if len(result)!=1 else ''})")

    print("Helper function run() defined ✓")
    return (run,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 — SELECT All Rows

    **NL query:** *Show me all employees and all their details.*

    **SQL concept:** `SELECT *` retrieves every column from a table.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT *
        FROM employees;
    """, 'All Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 — SELECT Specific Columns

    **NL query:** *Show only names and departments of all employees.*

    **SQL concept:** List the column names you want instead of `*`.
    """)
    return


@app.cell
def _(run):
    run('''
    SELECT first_name, last_name, department
    FROM employees;
    ''', 'Names & Departments')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6 — Filtering with WHERE

    **NL query:** *Show all employees in the IT department.*

    **SQL concept:** `WHERE` filters rows that match a condition.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT *
        FROM employees
        WHERE department = 'IT';
    """, 'IT Department Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7 — WHERE with Comparison Operators

    **NL query:** *Find employees earning more than $90,000.*

    **SQL concept:** Use `>`, `<`, `>=`, `<=`, `!=` in WHERE conditions.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT *
        FROM employees
        WHERE salary > 90000;
    """, 'Salary > $90,000')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8 — Combining Conditions: AND / OR

    **NL query:** *Find SOFTWARE engineers earning at least $100,000.*

    **SQL concept:** Combine multiple conditions with `AND` / `OR`.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT *
        FROM employees
        WHERE department = 'SOFTWARE'
        AND salary >= 100000;
    """, 'SOFTWARE with Salary ≥ $100K')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 9 — Sorting with ORDER BY

    **NL query:** *List all employees sorted by salary from highest to lowest.*

    **SQL concept:** `ORDER BY column DESC` sorts in descending order; `ASC` (default) for ascending.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT *
        FROM employees
        ORDER BY salary DESC;
    """, 'Employees Sorted by Salary (High → Low)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 10 — Limiting Results with LIMIT

    **NL query:** *Show the top 5 highest-paid employees.*

    **SQL concept:** `LIMIT n` restricts the output to the first *n* rows.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT *
        FROM employees
        ORDER BY salary DESC
        LIMIT 5;
    """, 'Top 5 Highest-Paid')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 11 — DISTINCT Values

    **NL query:** *What are the unique departments in the company?*

    **SQL concept:** `SELECT DISTINCT` removes duplicate values.
    """)
    return


@app.cell
def _(run):
    run('''
    SELECT DISTINCT department
    FROM employees
    ORDER BY department;
    ''', 'Unique Departments')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 12 — Filtering with BETWEEN

    **NL query:** *Find employees with salaries between $70,000 and $90,000.*

    **SQL concept:** `BETWEEN` is inclusive on both ends — shorthand for `>= AND <=`.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT *
        FROM employees
        WHERE salary BETWEEN 70000
        AND 90000
        ORDER BY salary;
    """, 'Salary Between $70K – $90K')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 13 — Filtering with IN

    **NL query:** *Show employees who are in either SALES or MARKETING.*

    **SQL concept:** `IN (...)` checks membership in a list — cleaner than multiple `OR`s.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT *
        FROM employees
        WHERE department IN ('SALES', 'MARKETING')
        ORDER BY department, last_name;
    """, 'SALES & MARKETING Staff')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 14 — Pattern Matching with LIKE

    **NL query:** *Find employees whose first name starts with the letter 'A' or 'B'.*

    **SQL concept:** `LIKE 'A%'` matches strings starting with A. `%` = any characters, `_` = one character.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT *
        FROM employees
        WHERE first_name LIKE 'A%'
        OR first_name LIKE 'B%';
    """, 'Names Starting with A or B')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 15 — Column Aliases & Expressions

    **NL query:** *Show each employee's full name, department, and their monthly salary.*

    **SQL concept:** Use `AS` to rename columns; expressions can compute new values.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT
            first_name || ' ' || last_name AS full_name,
            department,
            ROUND(salary / 12, 2) AS monthly_salary
        FROM employees;
    """, 'Full Name & Monthly Salary')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 16 — Aggregate Functions: COUNT

    **NL query:** *How many employees are there in total?*

    **SQL concept:** `COUNT(*)` counts all rows.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT COUNT(*) AS total_employees
        FROM employees;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 17 — Aggregate Functions: SUM, AVG, MIN, MAX

    **NL query:** *What are the total payroll, average salary, lowest salary, and highest salary?*

    **SQL concept:** Aggregate functions summarize a set of values into one result.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT
            SUM(salary) AS total_payroll,
            ROUND(AVG(salary),2) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees;
    """, 'Payroll Summary')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 18 — GROUP BY: Aggregate per Department

    **NL query:** *How many employees are in each department, and what is each department's average salary?*

    **SQL concept:** `GROUP BY` splits the data into groups; aggregate functions then run **per group**.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT
            department,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary),2) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY department;
    """, 'Headcount & Avg Salary by Department')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 19 — GROUP BY: Total Payroll per Department

    **NL query:** *What is the total salary expense for each department?*

    **SQL concept:** `SUM()` with `GROUP BY` gives subtotals per group.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT
            department,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY department
        ORDER BY total_salary DESC;
    """, 'Total Payroll by Department')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 20 — The HAVING Clause (Filter on Aggregates)

    **NL query:** *Which departments have an average salary above $80,000?*

    **SQL concept:** `HAVING` filters **after** grouping — use it when the condition involves an aggregate.

    > 💡 **Key rule:** `WHERE` filters individual rows *before* grouping.
    > `HAVING` filters groups *after* aggregation.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT
            department,
            ROUND(AVG(salary),2) AS avg_salary
        FROM employees
        GROUP BY department
        HAVING AVG(salary) > 80000
        ORDER BY avg_salary DESC;
    """, 'Departments with Avg Salary > $80K')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 21 — HAVING with COUNT

    **NL query:** *Show departments that have more than 4 employees.*

    **SQL concept:** You can use any aggregate in `HAVING` — here we use `COUNT(*)`.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT
            department,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY department
        HAVING COUNT(*) > 4
        ORDER BY emp_count DESC;
    """, 'Departments with > 4 Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 22 — Combining WHERE + GROUP BY + HAVING

    **NL query:** *Among employees hired after 2020, which departments have a total salary above $150,000?*

    **SQL concept:** `WHERE` filters rows first → `GROUP BY` groups them → `HAVING` filters the groups.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT
            department,
            SUM(salary) AS total_salary
        FROM employees
        WHERE hire_date > '2020-12-31'
        GROUP BY department
        HAVING SUM(salary) > 150000
        ORDER BY total_salary DESC;
    """, 'Post-2020 Hires: Depts with Total Salary > $150K')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 23 — CASE Expression (Conditional Logic)

    **NL query:** *Classify each employee's salary as 'High', 'Medium', or 'Low'.*

    **SQL concept:** `CASE WHEN ... THEN ... ELSE ... END` adds if/else logic inside SQL.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT
            first_name,
            last_name,
            salary,
            CASE WHEN salary >= 90000 THEN 'High (≥90K)' WHEN salary >= 70000 THEN 'Medium (70K-90K)' ELSE 'Low (<70K)' END AS salary_band
        FROM employees
        ORDER BY salary DESC;
    """, 'Salary Bands')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 24 — GROUP BY on a CASE Expression

    **NL query:** *How many employees fall into each salary band?*

    **SQL concept:** You can `GROUP BY` a computed expression, not just a raw column.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT
            CASE WHEN salary >= 90000 THEN 'High (≥90K)' WHEN salary >= 70000 THEN 'Medium (70K-90K)' ELSE 'Low (<70K)' END AS salary_band,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY salary_band
        ORDER BY salary_band;
    """, 'Employees per Salary Band')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 25 — Subquery: Employees Above Average Salary

    **NL query:** *List employees whose salary is above the company average.*

    **SQL concept:** A subquery in `WHERE` computes a value used for filtering.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT *
        FROM employees
        WHERE salary > (
        SELECT AVG(salary)
        FROM employees)
        ORDER BY salary DESC;
    """, 'Above-Average Earners (avg = $81,625)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 26 — Correlated Subquery: Highest Earner per Department

    **NL query:** *Who is the highest-paid employee in each department?*

    **SQL concept:** A correlated subquery references the outer table, running once per outer row.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT *
        FROM employees e
        WHERE salary = (
        SELECT MAX(salary)
        FROM employees
        WHERE department = e.department )
        ORDER BY department;
    """, 'Top Earner per Department')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 27 — Date Functions & GROUP BY Year

    **NL query:** *How many employees were hired each year?*

    **SQL concept:** DuckDB's `YEAR()` extracts the year part from a date.
    """)
    return


@app.cell
def _(run):
    run("""
        SELECT
            YEAR(hire_date) AS hire_year,
            COUNT(*) AS hires
        FROM employees
        GROUP BY hire_year
        ORDER BY hire_year;
    """, 'Hires per Year')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 28 — Cleanup

    **NL query:** *Close the database connection.*
    """)
    return


@app.cell
def _(con):
    con.close()
    print('Connection closed. Tutorial complete! 🎉')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary of SQL Concepts Covered

    | # | Concept | Key Syntax |
    |---|---------|------------|
    | 1 | Select all columns | `SELECT *` |
    | 2 | Select specific columns | `SELECT col1, col2` |
    | 3 | Filter rows | `WHERE condition` |
    | 4 | Comparison operators | `>`, `<`, `>=`, `<=`, `!=` |
    | 5 | Logical operators | `AND`, `OR` |
    | 6 | Sorting | `ORDER BY col ASC/DESC` |
    | 7 | Limit results | `LIMIT n` |
    | 8 | Unique values | `SELECT DISTINCT` |
    | 9 | Range filter | `BETWEEN ... AND ...` |
    | 10 | Set membership | `IN (...)` |
    | 11 | Pattern matching | `LIKE '%pattern%'` |
    | 12 | Column aliases | `AS alias_name` |
    | 13 | Aggregates | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` |
    | 14 | Group aggregation | `GROUP BY` |
    | 15 | Filter groups | `HAVING` |
    | 16 | Conditional logic | `CASE WHEN ... THEN ... END` |
    | 17 | Subqueries | `WHERE col > (SELECT ...)` |
    | 18 | Correlated subqueries | Inner query references outer table |
    | 19 | Date functions | `YEAR()`, `MONTH()` |

    ---
    *Happy querying!* 🦆
    """)
    return


if __name__ == "__main__":
    app.run()
