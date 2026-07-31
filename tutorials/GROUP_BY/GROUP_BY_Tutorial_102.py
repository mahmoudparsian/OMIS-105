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
    # DuckDB Tutorial: `GROUP BY` Operation

    ## Focus: SQL Aggregation in DuckDB

    This notebook teaches the major features of the SQL `GROUP BY` operation using DuckDB.

    We use one simple table:

    ```sql
    employees
    ```

    with 12 rows.

    Each lesson follows this pattern:

    1. **Natural language query**
    2. **SQL / DuckDB solution**
    3. **Result as a table**

    The tutorial progresses from:

    - Basic
    - Intermediate
    - Intermediate+
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 1 — Setup DuckDB

    ### Natural Language Query

    Create a DuckDB connection so we can run SQL queries inside this notebook.

    ### SQL / DuckDB Solution

    We import DuckDB and create an in-memory database connection.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd

    con = duckdb.connect()
    print("DuckDB connection created successfully.")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 2 — Create the `employees` Table

    ### Natural Language Query

    Create a simple employee table for practicing `GROUP BY`.

    ### SQL / DuckDB Solution

    The table has:

    - `employee_id`
    - `employee_name`
    - `department`
    - `job_title`
    - `region`
    - `gender`
    - `salary`
    - `bonus`
    """)
    return


@app.cell
def _(con):
    _sql = """
        CREATE OR REPLACE TABLE employees ( 
             employee_id INTEGER, 
             employee_name VARCHAR, 
             department VARCHAR, 
             job_title VARCHAR, 
             region VARCHAR, 
             gender VARCHAR, 
             salary INTEGER, 
             bonus INTEGER 
        );
    """

    print(_sql)
    con.execute(_sql)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 3 — Insert 12 Rows

    ### Natural Language Query

    Insert 12 employees into the table.

    ### SQL / DuckDB Solution

    The data is small enough to inspect manually, but rich enough to teach aggregation.
    """)
    return


@app.cell
def _(con):
    _sql = """
        INSERT INTO employees
        VALUES
            (1, 'Alice', 'Sales', 'Analyst', 'West', 'F', 70000, 5000),
            (2, 'Bob', 'Sales', 'Manager', 'West', 'M', 90000, 8000),
            (3, 'Carol', 'Sales', 'Analyst', 'East', 'F', 72000, 4000),
            (4, 'David', 'IT', 'Engineer', 'West', 'M', 95000, 7000),
            (5, 'Emma', 'IT', 'Engineer', 'East', 'F', 98000, 9000),
            (6, 'Frank', 'IT', 'Manager', 'East', 'M', 115000, 12000),
            (7, 'Grace', 'HR', 'Analyst', 'West', 'F', 65000, 3000),
            (8, 'Henry', 'HR', 'Manager', 'East', 'M', 85000, 6000),
            (9, 'Ivy', 'Finance', 'Analyst', 'West', 'F', 78000, 5000),
            (10, 'Jack', 'Finance', 'Manager', 'East', 'M', 105000, 10000),
            (11, 'Karen', 'Finance', 'Analyst', 'East', 'F', 80000, 5500),
            (12, 'Leo', 'Marketing', 'Analyst', 'West', 'M', 68000, 3500);
    """

    print(_sql)
    con.execute(_sql)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 4 — Display the Full Table

    ### Natural Language Query

    Show all rows and columns from the `employees` table.

    ### SQL / DuckDB Solution

    ```sql
    SELECT * FROM employees ORDER BY employee_id;
    ```

    ### Result
    The result is displayed as a table of rows and columns.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT *
        FROM employees
        ORDER BY employee_id;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 5 — Basic Aggregation Without `GROUP BY`

    ### Natural Language Query

    How many employees are in the company?

    ### SQL / DuckDB Solution

    ```sql
    SELECT COUNT(*) AS total_employees FROM employees;
    ```

    ### Concept
    This summarizes the entire table into one row.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT COUNT(*) AS total_employees
        FROM employees;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 6 — First `GROUP BY`: Count Employees by Department

    ### Natural Language Query

    How many employees are in each department?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        COUNT(*) AS number_of_employees
    FROM employees
    GROUP BY department
    ORDER BY department;
    ```

    ### Concept
    `GROUP BY department` creates one group for each department.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            COUNT(*) AS number_of_employees
        FROM employees
        GROUP BY department
        ORDER BY department;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 7 — Sum Salaries by Department

    ### Natural Language Query

    What is the total salary cost for each department?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        SUM(salary) AS total_salary
    FROM employees
    GROUP BY department
    ORDER BY total_salary DESC;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY department
        ORDER BY total_salary DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 8 — Average Salary by Department

    ### Natural Language Query

    What is the average salary in each department?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        ROUND(AVG(salary), 2) AS avg_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 9 — Minimum and Maximum Salary by Department

    ### Natural Language Query

    What are the lowest and highest salaries in each department?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        MIN(salary) AS min_salary,
        MAX(salary) AS max_salary
    FROM employees
    GROUP BY department
    ORDER BY department;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY department
        ORDER BY department;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 10 — Multiple Aggregations in One Query

    ### Natural Language Query

    For each department, show employee count, total salary, average salary, and total bonus.

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        COUNT(*) AS employee_count,
        SUM(salary) AS total_salary,
        ROUND(AVG(salary), 2) AS avg_salary,
        SUM(bonus) AS total_bonus
    FROM employees
    GROUP BY department
    ORDER BY total_salary DESC;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            COUNT(*) AS employee_count,
            SUM(salary) AS total_salary,
            ROUND(AVG(salary), 2) AS avg_salary,
            SUM(bonus) AS total_bonus
        FROM employees
        GROUP BY department
        ORDER BY total_salary DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 11 — Group by Job Title

    ### Natural Language Query

    How many employees do we have for each job title?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        job_title,
        COUNT(*) AS number_of_employees
    FROM employees
    GROUP BY job_title
    ORDER BY number_of_employees DESC;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            job_title,
            COUNT(*) AS number_of_employees
        FROM employees
        GROUP BY job_title
        ORDER BY number_of_employees DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 12 — Group by Region

    ### Natural Language Query

    How many employees are in each region?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        region,
        COUNT(*) AS number_of_employees
    FROM employees
    GROUP BY region
    ORDER BY region;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            region,
            COUNT(*) AS number_of_employees
        FROM employees
        GROUP BY region
        ORDER BY region;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 13 — Group by Gender

    ### Natural Language Query

    What is the average salary by gender?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        gender,
        COUNT(*) AS employee_count,
        ROUND(AVG(salary), 2) AS avg_salary
    FROM employees
    GROUP BY gender
    ORDER BY gender;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            gender,
            COUNT(*) AS employee_count,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY gender
        ORDER BY gender;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 14 — Group by Multiple Columns

    ### Natural Language Query

    How many employees are in each department and region combination?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        region,
        COUNT(*) AS employee_count
    FROM employees
    GROUP BY department, region
    ORDER BY department, region;
    ```

    ### Concept
    Each unique combination of `department` and `region` becomes a separate group.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            region,
            COUNT(*) AS employee_count
        FROM employees
        GROUP BY department, region
        ORDER BY department, region;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 15 — Total Salary by Department and Region

    ### Natural Language Query

    What is the total salary cost for each department-region combination?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        region,
        SUM(salary) AS total_salary
    FROM employees
    GROUP BY department, region
    ORDER BY department, total_salary DESC;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            region,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY department, region
        ORDER BY department, total_salary DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 16 — Aggregating a Computed Expression

    ### Natural Language Query

    What is the total compensation by department, where total compensation is salary plus bonus?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        SUM(salary + bonus) AS total_compensation
    FROM employees
    GROUP BY department
    ORDER BY total_compensation DESC;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            SUM(salary + bonus) AS total_compensation
        FROM employees
        GROUP BY department
        ORDER BY total_compensation DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 17 — `WHERE` Before `GROUP BY`

    ### Natural Language Query

    For only employees in the East region, what is the average salary by department?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        ROUND(AVG(salary), 2) AS avg_salary
    FROM employees
    WHERE region = 'East'
    GROUP BY department
    ORDER BY avg_salary DESC;
    ```

    ### Concept
    `WHERE` filters rows before grouping happens.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        WHERE region = 'East'
        GROUP BY department
        ORDER BY avg_salary DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 18 — Introduction to `HAVING`

    ### Natural Language Query

    Which departments have at least 2 employees?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        COUNT(*) AS employee_count
    FROM employees
    GROUP BY department
    HAVING COUNT(*) >= 2
    ORDER BY employee_count DESC;
    ```

    ### Concept
    `HAVING` filters groups after aggregation.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            COUNT(*) AS employee_count
        FROM employees
        GROUP BY department
        HAVING COUNT(*) >= 2
        ORDER BY employee_count DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 19 — `HAVING` with Total Salary

    ### Natural Language Query

    Which departments have total salary cost greater than 150,000?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        SUM(salary) AS total_salary
    FROM employees
    GROUP BY department
    HAVING SUM(salary) > 150000
    ORDER BY total_salary DESC;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY department
        HAVING SUM(salary) > 150000
        ORDER BY total_salary DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 20 — Using `WHERE` and `HAVING` Together

    ### Natural Language Query

    Among employees in the East region only, which departments have total salary greater than 150,000?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        SUM(salary) AS east_total_salary
    FROM employees
    WHERE region = 'East'
    GROUP BY department
    HAVING SUM(salary) > 150000
    ORDER BY east_total_salary DESC;
    ```

    ### Concept
    `WHERE` filters rows first; `HAVING` filters grouped results later.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            SUM(salary) AS east_total_salary
        FROM employees
        WHERE region = 'East'
        GROUP BY department
        HAVING SUM(salary) > 150000
        ORDER BY east_total_salary DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 21 — Ordering by an Aggregate Alias

    ### Natural Language Query

    Show departments ranked by average salary from highest to lowest.

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        ROUND(AVG(salary), 2) AS avg_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 22 — Important Rule: Non-Aggregated Columns Must Be Grouped

    ### Natural Language Query

    Why can’t we select `employee_name` while grouping only by `department`?

    ### Incorrect SQL Pattern

    ```sql
    SELECT department, employee_name, AVG(salary)
    FROM employees
    GROUP BY department;
    ```

    ### Explanation

    For each department, there are multiple employee names.

    DuckDB cannot know which employee name to show for each department group.

    ### Correct SQL / DuckDB Solution

    Remove `employee_name`, or group by it explicitly.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY department;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 23 — `COUNT(DISTINCT ...)` with `GROUP BY`

    ### Natural Language Query

    How many distinct job titles exist in each department?

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        COUNT(DISTINCT job_title) AS distinct_job_titles
    FROM employees
    GROUP BY department
    ORDER BY department;
    ```
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            COUNT(DISTINCT job_title) AS distinct_job_titles
        FROM employees
        GROUP BY department
        ORDER BY department;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 24 — Grouping by a Derived Category

    ### Natural Language Query

    Group employees into salary bands and count employees in each band.

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        CASE
            WHEN salary >= 100000 THEN 'High'
            WHEN salary >= 80000 THEN 'Medium'
            ELSE 'Low'
        END AS salary_band,
        COUNT(*) AS employee_count,
        ROUND(AVG(salary), 2) AS avg_salary
    FROM employees
    GROUP BY salary_band
    ORDER BY avg_salary DESC;
    ```

    ### Concept
    We can group by a derived expression such as a `CASE` result.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            CASE WHEN salary >= 100000 THEN 'High' WHEN salary >= 80000 THEN 'Medium' ELSE 'Low' END AS salary_band,
            COUNT(*) AS employee_count,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY salary_band
        ORDER BY avg_salary DESC;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 25 — DuckDB Convenience Feature: `GROUP BY ALL`

    ### Natural Language Query

    Show average salary by department and region using DuckDB's `GROUP BY ALL`.

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        region,
        ROUND(AVG(salary), 2) AS avg_salary
    FROM employees
    GROUP BY ALL
    ORDER BY department, region;
    ```

    ### Concept
    DuckDB supports `GROUP BY ALL`, which groups by all non-aggregated selected columns.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            region,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY ALL
        ORDER BY department, region;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 26 — Intermediate+: Subtotals with `ROLLUP`

    ### Natural Language Query

    Show total salary by department, plus a grand total.

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        SUM(salary) AS total_salary
    FROM employees
    GROUP BY ROLLUP(department)
    ORDER BY department NULLS LAST;
    ```

    ### Concept
    `ROLLUP` adds subtotal or total rows.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY ROLLUP(department)
        ORDER BY department NULLS LAST;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 27 — Intermediate+: `GROUPING SETS`

    ### Natural Language Query

    Show total salary by department and also total salary by region in one query.

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        department,
        region,
        SUM(salary) AS total_salary
    FROM employees
    GROUP BY GROUPING SETS (
        (department),
        (region)
    )
    ORDER BY department NULLS LAST, region NULLS LAST;
    ```

    ### Concept
    `GROUPING SETS` lets us request multiple grouping patterns in one query.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            department,
            region,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY GROUPING SETS ( (department), (region) )
        ORDER BY department NULLS LAST, region NULLS LAST;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 28 — `GROUP BY` vs Window Function Preview

    ### Natural Language Query

    Show each employee with their department average salary.

    ### SQL / DuckDB Solution

    ```sql
    SELECT
        employee_name,
        department,
        salary,
        ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS department_avg_salary
    FROM employees
    ORDER BY department, employee_name;
    ```

    ### Concept
    `GROUP BY` reduces rows. Window functions keep detail rows while adding group-level calculations.
    """)
    return


@app.cell
def _(con):
    _sql = """
        SELECT
            employee_name,
            department,
            salary,
            ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS department_avg_salary
        FROM employees
        ORDER BY department, employee_name;
    """
    print(_sql)
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 29 — Practice Challenge

    ### Natural Language Queries

    Write SQL for the following:

    1. Total bonus by department
    2. Average salary by job title
    3. Departments with average salary greater than 80,000
    4. Total compensation by region
    5. Salary band counts

    Try writing these before viewing the solution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 30 — Practice Challenge Solutions

    ### SQL / DuckDB Solutions

    The following cell contains sample solutions.
    """)
    return


@app.cell
def _(con):
    _sql = '''
    -- 1. Total bonus by department
    SELECT department, SUM(bonus) AS total_bonus
    FROM employees
    GROUP BY department
    ORDER BY total_bonus DESC;

    -- Note:
    -- DuckDB executes one final result at a time in this notebook display pattern.
    -- Run each query separately if you want to see every output table.
    '''
    print(_sql)
    con.execute("""
        SELECT
            department,
            SUM(bonus) AS total_bonus
        FROM employees
        GROUP BY department
        ORDER BY total_bonus DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bonus Solution Queries

    Copy and run each query separately to see each output.
    """)
    return


@app.cell
def _(con):
    queries = {
        "Average salary by job title": """
            SELECT
                job_title,
                ROUND(AVG(salary), 2) AS avg_salary
            FROM employees
            GROUP BY job_title
            ORDER BY avg_salary DESC;
        """,
        "Departments with average salary > 80000": """
            SELECT
                department,
                ROUND(AVG(salary), 2) AS avg_salary
            FROM employees
            GROUP BY department
            HAVING AVG(salary) > 80000
            ORDER BY avg_salary DESC;
        """,
        "Total compensation by region": """
            SELECT
                region,
                SUM(salary + bonus) AS total_compensation
            FROM employees
            GROUP BY region
            ORDER BY total_compensation DESC;
        """,
        "Salary band counts": """
            SELECT
                CASE WHEN salary >= 100000 THEN 'High' WHEN salary >= 80000 THEN 'Medium' ELSE 'Low' END AS salary_band,
                COUNT(*) AS employee_count
            FROM employees
            GROUP BY salary_band
            ORDER BY employee_count DESC;
        """
    }

    for name, q in queries.items():
        print("\n---", name, "---")
        print(q)
        print(con.execute(q).df())
    return


if __name__ == "__main__":
    app.run()
