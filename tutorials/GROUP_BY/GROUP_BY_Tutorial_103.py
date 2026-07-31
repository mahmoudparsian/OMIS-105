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
    # SQL GROUP BY & HAVING in DuckDB
    ## A Comprehensive, Hands-On Tutorial — From Basic to Intermediate+

    **Author**: Dr. Mahmoud Parsian — Santa Clara University
    **Course**: OMIS 105 — Database Management Systems
    **Focus**: GROUP BY, Aggregate Functions, and HAVING
    **Tool**: DuckDB (in-process analytical database)
    **Format**: Jupyter Notebook

    ---

    ### Why GROUP BY Matters

    GROUP BY is the SQL engine behind **every dashboard, report, and KPI** in business:

    - *"What is the average salary per department?"* → GROUP BY department
    - *"Which month had the highest revenue?"* → GROUP BY month
    - *"How many customers are in each city?"* → GROUP BY city

    Without GROUP BY, SQL can only show individual rows. **With** GROUP BY, SQL becomes an analytical powerhouse that summarizes millions of rows into actionable insights.

    ### Tutorial Structure

    Every example follows a three-part pattern:
    1. **Natural-Language (NL) Question** — the business question
    2. **SQL Query** — the DuckDB code that answers it
    3. **Result Table** — the output displayed as rows and columns

    ### Prerequisites
    - Python 3.8+ with `duckdb` installed (`pip install duckdb`)
    - Basic SQL knowledge (SELECT, WHERE, ORDER BY)

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Table of Contents

    ### Part I — Setup & Foundations
    1. Setting Up DuckDB
    2. Creating the `departments` Table (5 departments)
    3. Creating the `employees` Table (20 employees)
    4. Exploring the Data
    5. Aggregate Functions WITHOUT GROUP BY (whole-table summaries)

    ### Part II — GROUP BY Basics
    6. GROUP BY — Concept & How It Works
    7. GROUP BY Single Column — Count per Department
    8. GROUP BY with SUM — Total Salary per Department
    9. GROUP BY with AVG — Average Salary per Department
    10. GROUP BY with MIN and MAX
    11. GROUP BY with Multiple Aggregates
    12. The Golden Rule: SELECT + GROUP BY Compatibility

    ### Part III — GROUP BY with Multiple Columns
    13. GROUP BY Two Columns — Department + City
    14. GROUP BY Two Columns — Department + Gender
    15. GROUP BY with ORDER BY — Sorting Grouped Results
    16. GROUP BY with ROUND — Clean Numeric Output

    ### Part IV — HAVING Clause
    17. HAVING — Concept & Why WHERE Is Not Enough
    18. HAVING with COUNT — Departments with 4+ Employees
    19. HAVING with AVG — Departments with High Average Salary
    20. HAVING with SUM — Departments with Large Payroll
    21. HAVING with Multiple Conditions
    22. WHERE + GROUP BY + HAVING — The Complete Pipeline
    23. WHERE vs HAVING — Side-by-Side Comparison

    ### Part V — Intermediate GROUP BY
    24. GROUP BY with JOIN — Aggregation Across Tables
    25. GROUP BY with CASE — Custom Categories
    26. GROUP BY with Date Parts — Grouping by Year/Quarter
    27. GROUP BY with COALESCE — Handling NULLs in Groups
    28. GROUP BY with HAVING + ORDER BY + LIMIT — Top-N Analysis

    ### Part VI — Advanced GROUP BY (Intermediate+)
    29. GROUP BY with Subquery — Compare Groups to Overall
    30. GROUP BY with CTE — Multi-Level Aggregation
    31. GROUP BY ROLLUP — Subtotals and Grand Totals
    32. GROUP BY CUBE — All Possible Grouping Combinations
    33. GROUP BY GROUPING SETS — Custom Grouping Combinations
    34. GROUP BY with Window Functions — Aggregate + Detail
    35. Grand Finale — Complete Department Analytics Report

    ### Appendix
    - GROUP BY Cheat Sheet & Common Mistakes

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART I — Setup & Foundations
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Setting Up DuckDB
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=':memory:')
    print("DuckDB connection established!")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Creating the `departments` Table (5 Departments)
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE TABLE departments (
            dept_id   INTEGER PRIMARY KEY,
            dept_name VARCHAR NOT NULL,
            location  VARCHAR NOT NULL,
            budget    DECIMAL(12,2) NOT NULL
        );
    """)

    con.execute("""
        INSERT INTO departments
        VALUES
            (101, 'Engineering', 'San Jose', 500000.00),
            (102, 'Marketing', 'San Francisco', 200000.00),
            (103, 'Sales', 'Los Angeles', 300000.00),
            (104, 'HR', 'San Jose', 150000.00),
            (105, 'Finance', 'New York', 250000.00);
    """)

    con.execute("""
        SELECT *
        FROM departments
        ORDER BY dept_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Creating the `employees` Table (20 Employees)

    Our employees table includes deliberate variety for GROUP BY exercises:
    - **5 departments** with uneven distribution (Engineering has the most)
    - **Multiple cities** within departments
    - **Gender** column for multi-column grouping
    - **Salary range** from $52K to $115K for meaningful aggregation
    - **Hire dates** across 2018–2024 for date-based grouping
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE TABLE employees (
            emp_id    INTEGER PRIMARY KEY,
            emp_name  VARCHAR NOT NULL,
            dept_id   INTEGER REFERENCES departments(dept_id),
            salary    DECIMAL(10,2) NOT NULL,
            hire_date DATE NOT NULL,
            city      VARCHAR,
            gender    VARCHAR(1)
        );
    """)

    con.execute("""
        INSERT INTO employees
        VALUES
            /* Engineering (dept 101): 6 employees */ (1, 'Alice Johnson', 101, 95000.00, '2019-03-15', 'San Jose', 'F'),
            (2, 'Bob Smith', 101, 88000.00, '2020-07-01', 'San Jose', 'M'),
            (3, 'Carol Williams', 101, 105000.00, '2018-01-10', 'Santa Clara', 'F'),
            (4, 'David Brown', 101, 92000.00, '2021-06-20', 'San Jose', 'M'),
            (5, 'Eva Martinez', 101, 78000.00, '2022-04-05', 'Santa Clara', 'F'),
            (6, 'Frank Lee', 101, 115000.00, '2018-08-22', 'Sunnyvale', 'M'),
            /* Marketing (dept 102): 4 employees */ (7, 'Grace Kim', 102, 72000.00, '2020-11-15', 'San Francisco', 'F'),
            (8, 'Henry Chen', 102, 68000.00, '2021-09-01', 'San Francisco', 'M'),
            (9, 'Iris Patel', 102, 75000.00, '2019-05-20', 'Oakland', 'F'),
            (10, 'Jack Wilson', 102, 71000.00, '2023-01-08', 'San Francisco', 'M'),
            /* Sales (dept 103): 4 employees */ (11, 'Karen Davis', 103, 82000.00, '2019-02-14', 'Los Angeles', 'F'),
            (12, 'Leo Garcia', 103, 67000.00, '2022-08-30', 'Pasadena', 'M'),
            (13, 'Mia Robinson', 103, 73000.00, '2020-12-01', 'Los Angeles', 'F'),
            (14, 'Noah Thompson', 103, 69000.00, '2023-06-15', 'Los Angeles', 'M'),
            /* HR (dept 104): 3 employees */ (15, 'Olivia White', 104, 65000.00, '2021-01-10', 'San Jose', 'F'),
            (16, 'Paul Harris', 104, 62000.00, '2022-02-20', 'San Jose', 'M'),
            (17, 'Quinn Adams', 104, 58000.00, '2024-03-05', 'San Jose', 'F'),
            /* Finance (dept 105): 3 employees */ (18, 'Rachel Clark', 105, 85000.00, '2019-11-01', 'New York', 'F'),
            (19, 'Sam Turner', 105, 78000.00, '2020-12-15', 'New York', 'M'),
            (20, 'Tina Baker', 105, 52000.00, '2024-01-20', 'New York', 'F');
    """)

    print("employees table created: 20 rows across 5 departments")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Exploring the Data

    ### NL Query
    > *"Show me all 20 employees."*
    """)
    return


@app.cell
def _(con):
    # NL: Show me all 20 employees.
    con.execute("""
        SELECT
            emp_id,
            emp_name,
            dept_id,
            salary,
            hire_date,
            city,
            gender
        FROM employees
        ORDER BY emp_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Aggregate Functions WITHOUT GROUP BY (Whole-Table Summaries)

    ### NL Query
    > *"What is the total number of employees, total payroll, average salary, lowest salary, and highest salary across the ENTIRE company?"*

    ### SQL Concept
    When you use aggregate functions **without** GROUP BY, SQL treats the **entire table** as one group and returns a **single row**.

    | Function | Purpose | Example |
    |----------|---------|---------|
    | `COUNT(*)` | Number of rows | 20 |
    | `COUNT(col)` | Non-NULL values in column | 20 |
    | `SUM(col)` | Total | 1,547,000 |
    | `AVG(col)` | Mean | 77,350 |
    | `MIN(col)` | Smallest | 52,000 |
    | `MAX(col)` | Largest | 115,000 |
    """)
    return


@app.cell
def _(con):
    # NL: Company-wide summary stats — no GROUP BY (whole table = one group).
    con.execute("""
        SELECT
            COUNT(*) AS total_employees,
            SUM(salary) AS total_payroll,
            ROUND(AVG(salary), 2) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            MAX(salary) - MIN(salary) AS salary_range
        FROM employees;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART II — GROUP BY Basics
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. GROUP BY — Concept & How It Works

    ### What GROUP BY Does

    GROUP BY **partitions** rows into groups based on one or more columns, then **collapses** each group into a single summary row using aggregate functions.

    ```
                               GROUP BY department
                               ─────────────────────
    Raw Rows (20)                          Grouped Result (5)
    ┌──────────────────────┐               ┌──────────────────────────────┐
    │ Alice   Engineering  │               │ Engineering   6   $95,500    │
    │ Bob     Engineering  │  ──────────▶  │ Marketing     4   $71,500    │
    │ Carol   Engineering  │               │ Sales         4   $72,750    │
    │ David   Engineering  │               │ HR            3   $61,667    │
    │ Eva     Engineering  │               │ Finance       3   $71,667    │
    │ Frank   Engineering  │               └──────────────────────────────┘
    │ Grace   Marketing    │                 dept_name   count  avg_salary
    │ Henry   Marketing    │
    │ ...     ...          │
    │ Tina    Finance      │
    └──────────────────────┘
    ```

    ### Execution Order

    ```
    1. FROM       ← read the table
    2. WHERE      ← filter individual rows (BEFORE grouping)
    3. GROUP BY   ← partition rows into groups
    4. HAVING     ← filter groups (AFTER grouping)
    5. SELECT     ← compute aggregates, choose columns
    6. ORDER BY   ← sort the result
    7. LIMIT      ← restrict output rows
    ```

    ### The Golden Rule
    Every column in SELECT must either:
    - Appear in the **GROUP BY** clause, OR
    - Be inside an **aggregate function** (COUNT, SUM, AVG, MIN, MAX)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. GROUP BY Single Column — Count per Department

    ### NL Query
    > *"How many employees are in each department?"*

    ### SQL Concept
    `GROUP BY dept_id` creates one group per unique `dept_id` value. `COUNT(*)` then counts how many rows are in each group.
    """)
    return


@app.cell
def _(con):
    # NL: How many employees are in each department?
    # SQL: SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id

    con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS employee_count
        FROM employees
        GROUP BY dept_id
        ORDER BY dept_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. GROUP BY with SUM — Total Salary per Department

    ### NL Query
    > *"What is the total salary cost for each department?"*
    """)
    return


@app.cell
def _(con):
    # NL: Total salary cost for each department.
    # SQL: SELECT dept_id, SUM(salary) FROM employees GROUP BY dept_id

    con.execute("""
        SELECT
            dept_id,
            SUM(salary) AS total_salary,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY dept_id
        ORDER BY total_salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. GROUP BY with AVG — Average Salary per Department

    ### NL Query
    > *"What is the average salary in each department?"*
    """)
    return


@app.cell
def _(con):
    # NL: Average salary in each department.
    # SQL: SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id

    con.execute("""
        SELECT
            dept_id,
            ROUND(AVG(salary), 2) AS avg_salary,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY dept_id
        ORDER BY avg_salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. GROUP BY with MIN and MAX

    ### NL Query
    > *"What is the lowest and highest salary in each department?"*
    """)
    return


@app.cell
def _(con):
    # NL: Lowest and highest salary in each department.
    # SQL: SELECT dept_id, MIN(salary), MAX(salary) GROUP BY dept_id

    con.execute("""
        SELECT
            dept_id,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            MAX(salary) - MIN(salary) AS salary_spread
        FROM employees
        GROUP BY dept_id
        ORDER BY salary_spread DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11. GROUP BY with Multiple Aggregates — Full Department Summary

    ### NL Query
    > *"For each department, show the employee count, total payroll, average salary, min salary, max salary, and salary range — all in one query."*
    """)
    return


@app.cell
def _(con):
    # NL: Complete summary stats per department.
    # SQL: Multiple aggregate functions in one GROUP BY

    con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            SUM(salary) AS total_payroll,
            ROUND(AVG(salary), 2) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            MAX(salary) - MIN(salary) AS salary_range
        FROM employees
        GROUP BY dept_id
        ORDER BY total_payroll DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12. The Golden Rule: SELECT + GROUP BY Compatibility

    ### The Rule
    > **Every column in SELECT must either be in GROUP BY or inside an aggregate function.**

    ### Why?
    When you GROUP BY `dept_id`, each group has **multiple** employees. SQL doesn't know which employee's name to show — it's ambiguous. Aggregate functions resolve this ambiguity by collapsing multiple values into one.

    ```sql
    -- ✅ CORRECT: dept_id is in GROUP BY, salary is aggregated
    SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id

    -- ❌ ERROR: emp_name is NOT in GROUP BY and NOT aggregated
    SELECT dept_id, emp_name, AVG(salary) FROM employees GROUP BY dept_id
    -- Which emp_name should SQL pick? Alice? Bob? Carol? → AMBIGUOUS!
    ```

    ### What Happens If You Break the Rule?

    Most databases throw an error. DuckDB will return an error like:
    ```
    Binder Error: column "emp_name" must appear in the GROUP BY clause
    or be used in an aggregate function
    ```
    """)
    return


@app.cell
def _(con):
    # Demonstrate the Golden Rule violation
    try:
        con.execute("""
            SELECT
                dept_id,
                emp_name,
                AVG(salary)
            FROM employees
            GROUP BY dept_id;
        """)
    except Exception as e:
        print(f"ERROR (as expected):\n{e}")

    print()
    print("FIX: Either add emp_name to GROUP BY, or use an aggregate like MIN(emp_name)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART III — GROUP BY with Multiple Columns
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13. GROUP BY Two Columns — Department + City

    ### NL Query
    > *"How many employees work in each department-city combination?"*

    ### SQL Concept
    GROUP BY with multiple columns creates groups for each **unique combination** of values. If Engineering has employees in San Jose, Santa Clara, and Sunnyvale, that's 3 separate groups (not 1).
    """)
    return


@app.cell
def _(con):
    # NL: Employee count by department + city combination.
    # SQL: GROUP BY dept_id, city

    con.execute("""
        SELECT
            dept_id,
            city,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY dept_id, city
        ORDER BY dept_id, city;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14. GROUP BY Two Columns — Department + Gender

    ### NL Query
    > *"How many male and female employees are in each department, and what is the average salary by gender within each department?"*
    """)
    return


@app.cell
def _(con):
    # NL: Employee count and avg salary by department + gender.
    # SQL: GROUP BY dept_id, gender

    con.execute("""
        SELECT
            dept_id,
            gender,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY dept_id, gender
        ORDER BY dept_id, gender;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 15. GROUP BY with ORDER BY — Sorting Grouped Results

    ### NL Query
    > *"Show departments ranked by average salary, highest to lowest."*

    ### SQL Concept
    ORDER BY applies **after** GROUP BY. You can sort by:
    - Columns in the GROUP BY
    - Aggregate function results (computed columns)
    - Column aliases
    """)
    return


@app.cell
def _(con):
    # NL: Departments ranked by average salary (highest first).
    # SQL: GROUP BY dept_id ORDER BY avg_salary DESC

    con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY dept_id
        ORDER BY avg_salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 16. GROUP BY with ROUND — Clean Numeric Output

    ### NL Query
    > *"Show salary stats per department, with all numbers rounded to whole dollars and with percentage of total payroll."*
    """)
    return


@app.cell
def _(con):
    # NL: Salary stats per department with percentages (clean numbers).
    # SQL: GROUP BY + ROUND + percentage calculation

    con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            CAST(ROUND(AVG(salary), 0) AS INTEGER) AS avg_salary,
            CAST(SUM(salary) AS INTEGER) AS total_payroll,
            ROUND(SUM(salary) * 100.0 / (
        SELECT SUM(salary)
        FROM employees), 1) AS pct_of_total
        FROM employees
        GROUP BY dept_id
        ORDER BY pct_of_total DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART IV — HAVING Clause
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 17. HAVING — Concept & Why WHERE Is Not Enough

    ### The Problem
    > *"Show only departments that have more than 3 employees."*

    You might try `WHERE COUNT(*) > 3` — but that **will not work**:

    ```sql
    -- ❌ WRONG: Cannot use aggregate in WHERE
    SELECT dept_id, COUNT(*)
    FROM employees
    WHERE COUNT(*) > 3    -- ERROR!
    GROUP BY dept_id
    ```

    ### Why WHERE Fails
    `WHERE` filters **individual rows BEFORE grouping**. At that point, groups don't exist yet, so `COUNT(*)` is meaningless.

    ### The Solution: HAVING
    `HAVING` filters **groups AFTER grouping**. It runs after GROUP BY, so aggregate functions are available.

    ```sql
    -- ✅ CORRECT: Use HAVING for aggregate conditions
    SELECT dept_id, COUNT(*)
    FROM employees
    GROUP BY dept_id
    HAVING COUNT(*) > 3   -- filters GROUPS, not rows
    ```

    ### WHERE vs HAVING Summary

    | Clause | Filters | When | Can Use Aggregates? |
    |--------|---------|------|---------------------|
    | **WHERE** | Individual rows | BEFORE GROUP BY | ❌ No |
    | **HAVING** | Groups | AFTER GROUP BY | ✅ Yes |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 18. HAVING with COUNT — Departments with 4+ Employees

    ### NL Query
    > *"Which departments have 4 or more employees?"*
    """)
    return


@app.cell
def _(con):
    # NL: Departments with 4 or more employees.
    # SQL: GROUP BY dept_id HAVING COUNT(*) >= 4

    con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY dept_id
        HAVING COUNT(*) >= 4
        ORDER BY emp_count DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 19. HAVING with AVG — Departments with High Average Salary

    ### NL Query
    > *"Which departments have an average salary above $72,000?"*
    """)
    return


@app.cell
def _(con):
    # NL: Departments with average salary above $72,000.
    # SQL: GROUP BY dept_id HAVING AVG(salary) > 72000

    con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY dept_id
        HAVING AVG(salary) > 72000
        ORDER BY avg_salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 20. HAVING with SUM — Departments with Large Payroll

    ### NL Query
    > *"Which departments have a total payroll exceeding $250,000?"*
    """)
    return


@app.cell
def _(con):
    # NL: Departments with total payroll > $250,000.
    # SQL: GROUP BY dept_id HAVING SUM(salary) > 250000

    con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            SUM(salary) AS total_payroll
        FROM employees
        GROUP BY dept_id
        HAVING SUM(salary) > 250000
        ORDER BY total_payroll DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 21. HAVING with Multiple Conditions

    ### NL Query
    > *"Which departments have at least 4 employees AND an average salary below $80,000?"*

    ### SQL Concept
    HAVING supports `AND`, `OR`, and `NOT` — just like WHERE. Each condition can use a different aggregate function.
    """)
    return


@app.cell
def _(con):
    # NL: Departments with 4+ employees AND avg salary < $80,000.
    # SQL: HAVING COUNT(*) >= 4 AND AVG(salary) < 80000

    con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary,
            SUM(salary) AS total_payroll
        FROM employees
        GROUP BY dept_id
        HAVING COUNT(*) >= 4
        AND AVG(salary) < 80000
        ORDER BY avg_salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 22. WHERE + GROUP BY + HAVING — The Complete Pipeline

    ### NL Query
    > *"Among employees hired since 2020, which departments have more than 2 such employees, and what is their average salary?"*

    ### SQL Concept
    This query uses the **full pipeline**:
    1. `WHERE hire_date >= '2020-01-01'` — filters individual rows first (only post-2020 hires)
    2. `GROUP BY dept_id` — groups the filtered rows by department
    3. `HAVING COUNT(*) > 2` — keeps only groups with more than 2 employees

    ```
    20 rows → WHERE (filter to post-2020) → 12 rows → GROUP BY → 5 groups → HAVING (>2) → ? groups
    ```
    """)
    return


@app.cell
def _(con):
    # NL: Post-2020 hires, departments with more than 2 such employees.
    # SQL: WHERE ... GROUP BY ... HAVING COUNT(*) > 2

    # First, let's see how many post-2020 hires each dept has:
    print("Step 1: All departments with post-2020 hire counts:")
    all_depts = con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS post_2020_hires,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        WHERE hire_date >= '2020-01-01'
        GROUP BY dept_id
        ORDER BY dept_id;
    """).fetchdf()
    print(all_depts.to_string(index=False))

    print()
    print("Step 2: After HAVING COUNT(*) > 2:")
    filtered = con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS post_2020_hires,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        WHERE hire_date >= '2020-01-01'
        GROUP BY dept_id
        HAVING COUNT(*) > 2
        ORDER BY post_2020_hires DESC;
    """).fetchdf()
    print(filtered.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 23. WHERE vs HAVING — Side-by-Side Comparison

    ### NL Query
    > *"Show the difference between filtering rows with WHERE vs filtering groups with HAVING."*

    ### The Key Distinction

    ```
    WHERE salary > 70000           HAVING AVG(salary) > 70000
    ─────────────────────          ──────────────────────────
    Filters INDIVIDUAL rows        Filters GROUPS
    Runs BEFORE GROUP BY           Runs AFTER GROUP BY
    Cannot use COUNT, AVG, etc.    CAN use COUNT, AVG, etc.
    "Remove rows below 70K"        "Remove groups whose AVERAGE is below 70K"
    ```
    """)
    return


@app.cell
def _(con):
    # COMPARISON: WHERE filters rows BEFORE grouping

    # Query A: WHERE salary > 70000 → then GROUP BY
    print("Query A: WHERE salary > 70000, then GROUP BY")
    print("(Excludes low-salary individuals BEFORE counting)")
    a = con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary),2) AS avg_salary
        FROM employees
        WHERE salary > 70000
        GROUP BY dept_id
        ORDER BY dept_id;
    """).fetchdf()
    print(a.to_string(index=False))

    print()

    # Query B: GROUP BY → then HAVING AVG(salary) > 70000
    print("Query B: GROUP BY, then HAVING AVG(salary) > 70000")
    print("(Includes ALL employees in the average, then filters groups)")
    b = con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary),2) AS avg_salary
        FROM employees
        GROUP BY dept_id
        HAVING AVG(salary) > 70000
        ORDER BY dept_id;
    """).fetchdf()
    print(b.to_string(index=False))

    print()
    print("NOTE: Query A has different counts and averages because low-salary")
    print("employees were removed BEFORE grouping. Query B counts ALL employees")
    print("but only shows departments where the group average exceeds $70K.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART V — Intermediate GROUP BY
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 24. GROUP BY with JOIN — Aggregation Across Tables

    ### NL Query
    > *"Show the department NAME (not just ID), employee count, and average salary for each department."*

    ### SQL Concept
    JOIN first combines the tables, then GROUP BY aggregates. The department name comes from the `departments` table, so we need a JOIN.
    """)
    return


@app.cell
def _(con):
    # NL: Department name, employee count, avg salary (using JOIN).
    # SQL: employees JOIN departments ... GROUP BY d.dept_name

    con.execute("""
        SELECT
            d.dept_name,
            d.location,
            COUNT(*) AS emp_count,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            SUM(e.salary) AS total_payroll,
            d.budget,
            ROUND(SUM(e.salary) * 100.0 / d.budget, 1) AS budget_utilization_pct
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name, d.location, d.budget
        ORDER BY avg_salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 25. GROUP BY with CASE — Custom Categories

    ### NL Query
    > *"How many employees fall into each salary tier: 'High' (≥90K), 'Medium' (70K–89K), or 'Low' (<70K)?"*

    ### SQL Concept
    Use `CASE` inside GROUP BY to create **custom grouping categories** that don't exist as columns in the table. This is extremely powerful for ad-hoc analysis.
    """)
    return


@app.cell
def _(con):
    # NL: Employee count by salary tier (High / Medium / Low).
    # SQL: GROUP BY CASE expression

    con.execute("""
        SELECT
            CASE WHEN salary >= 90000 THEN 'High (≥90K)' WHEN salary >= 70000 THEN 'Medium (70K-89K)' ELSE 'Low (<70K)' END AS salary_tier,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary,
            MIN(salary) AS min_in_tier,
            MAX(salary) AS max_in_tier
        FROM employees
        GROUP BY salary_tier
        ORDER BY avg_salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 26. GROUP BY with Date Parts — Grouping by Year

    ### NL Query
    > *"How many employees were hired each year, and what was the average starting salary by year?"*

    ### SQL Concept
    Use `EXTRACT(YEAR FROM date)` or `DATE_PART('year', date)` to extract the year from a date column, then GROUP BY that extracted value.
    """)
    return


@app.cell
def _(con):
    # NL: Hire count and avg salary by year.
    # SQL: GROUP BY EXTRACT(YEAR FROM hire_date)

    con.execute("""
        SELECT EXTRACT(YEAR
        FROM hire_date) AS hire_year, COUNT(*) AS hires, ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY hire_year
        ORDER BY hire_year;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 27. GROUP BY with COALESCE — Handling NULLs in Groups

    ### NL Query
    > *"Group employees by city. If any employee has a NULL city, label it 'Unknown'."*

    ### SQL Concept
    If a grouping column contains NULL, all NULL rows form their own group (labeled NULL in the output). Use `COALESCE` to replace NULLs with a readable label before grouping.
    """)
    return


@app.cell
def _(con):
    # NL: Employee count by city (handling potential NULLs).
    # SQL: GROUP BY COALESCE(city, 'Unknown')

    con.execute("""
        SELECT
            COALESCE(city, 'Unknown') AS city,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY COALESCE(city, 'Unknown')
        ORDER BY emp_count DESC, city;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 28. GROUP BY + HAVING + ORDER BY + LIMIT — Top-N Analysis

    ### NL Query
    > *"What are the top 2 departments by average salary, considering only departments with at least 3 employees?"*

    ### SQL Concept
    The full pipeline: GROUP BY → HAVING → ORDER BY → LIMIT. This is the classic pattern for **"Top N by metric with a minimum threshold"** queries.
    """)
    return


@app.cell
def _(con):
    # NL: Top 2 departments by avg salary (min 3 employees).
    # SQL: GROUP BY → HAVING → ORDER BY → LIMIT

    con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary,
            SUM(salary) AS total_payroll
        FROM employees
        GROUP BY dept_id
        HAVING COUNT(*) >= 3
        ORDER BY avg_salary DESC
        LIMIT 2;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART VI — Advanced GROUP BY (Intermediate+)
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 29. GROUP BY with Subquery — Compare Each Group to Overall Average

    ### NL Query
    > *"For each department, show the average salary and whether it's above or below the company-wide average."*
    """)
    return


@app.cell
def _(con):
    # NL: Dept avg salary vs company avg — above or below?
    # SQL: GROUP BY with scalar subquery comparison

    con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS dept_avg,
            (
        SELECT ROUND(AVG(salary), 2)
        FROM employees) AS company_avg, ROUND(AVG(salary) - (
        SELECT AVG(salary)
        FROM employees), 2) AS diff, CASE WHEN AVG(salary) >= (
        SELECT AVG(salary)
        FROM employees) THEN '↑ Above' ELSE '↓ Below' END AS vs_company
        FROM employees
        GROUP BY dept_id
        ORDER BY dept_avg DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 30. GROUP BY with CTE — Multi-Level Aggregation

    ### NL Query
    > *"What is the average of each department's average salary? (i.e., the 'average of averages')"*

    ### SQL Concept
    Sometimes you need to aggregate **already-aggregated** data. A CTE computes the first level (department averages), then the outer query aggregates those results.
    """)
    return


@app.cell
def _(con):
    # NL: Average of department averages (two-level aggregation).
    # SQL: WITH dept_avgs AS (...) SELECT AVG(dept_avg)

    con.execute("""
        WITH dept_avgs AS (
        SELECT
            dept_id,
            ROUND(AVG(salary), 2) AS dept_avg
        FROM employees
        GROUP BY dept_id )
        SELECT
            COUNT(*) AS num_departments,
            ROUND(AVG(dept_avg), 2) AS avg_of_dept_avgs,
            MIN(dept_avg) AS lowest_dept_avg,
            MAX(dept_avg) AS highest_dept_avg,
            MAX(dept_avg) - MIN(dept_avg) AS spread
        FROM dept_avgs;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 31. GROUP BY ROLLUP — Subtotals and Grand Totals

    ### NL Query
    > *"Show employee count and average salary by department, AND include a grand total row at the bottom."*

    ### SQL Concept
    `GROUP BY ROLLUP(col1, col2)` generates:
    - All regular groups
    - **Subtotals** for each level
    - A **grand total** row (all columns NULL)

    ROLLUP creates a **hierarchical** summary — like the totals row at the bottom of a spreadsheet.
    """)
    return


@app.cell
def _(con):
    # NL: Department stats WITH a grand total row.
    # SQL: GROUP BY ROLLUP(dept_id)

    con.execute("""
        SELECT
            COALESCE(CAST(dept_id AS VARCHAR), '** GRAND TOTAL **') AS dept_id,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary,
            SUM(salary) AS total_payroll
        FROM employees
        GROUP BY ROLLUP(dept_id)
        ORDER BY CASE WHEN dept_id IS NULL THEN 999 ELSE dept_id END;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 32. GROUP BY CUBE — All Possible Grouping Combinations

    ### NL Query
    > *"Show employee count by department AND gender, with subtotals for each department, each gender, AND a grand total."*

    ### SQL Concept
    `GROUP BY CUBE(col1, col2)` generates **every possible combination** of groupings:

    | Grouping | dept_id | gender | What it shows |
    |----------|---------|--------|---------------|
    | Both | ✅ | ✅ | Regular groups (dept + gender) |
    | dept only | ✅ | NULL | Subtotal per department |
    | gender only | NULL | ✅ | Subtotal per gender |
    | Neither | NULL | NULL | Grand total |

    For 2 columns, CUBE produces 2² = 4 types of grouping rows.
    """)
    return


@app.cell
def _(con):
    # NL: Employee count by dept + gender, with ALL subtotals.
    # SQL: GROUP BY CUBE(dept_id, gender)

    con.execute("""
        SELECT
            COALESCE(CAST(dept_id AS VARCHAR), 'ALL') AS dept,
            COALESCE(gender, 'ALL') AS gender,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY CUBE(dept_id, gender)
        ORDER BY CASE WHEN dept_id IS NULL THEN 999 ELSE dept_id END, CASE WHEN gender IS NULL THEN 'Z' ELSE gender END;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 33. GROUP BY GROUPING SETS — Custom Grouping Combinations

    ### NL Query
    > *"Show me three different summaries in one query: by department, by gender, and the grand total — but NOT the department+gender combination."*

    ### SQL Concept
    `GROUPING SETS` gives you **fine-grained control** over which combinations to include. Unlike CUBE (which generates ALL combinations), GROUPING SETS lets you pick exactly the ones you want.

    ```sql
    -- CUBE generates ALL 4 combinations
    GROUP BY CUBE(dept_id, gender)

    -- GROUPING SETS lets you pick specific ones
    GROUP BY GROUPING SETS (
        (dept_id),        -- subtotal by department
        (gender),         -- subtotal by gender
        ()                -- grand total
    )
    ```
    """)
    return


@app.cell
def _(con):
    # NL: Three summaries: by department, by gender, and grand total.
    # SQL: GROUP BY GROUPING SETS((dept_id), (gender), ())

    con.execute("""
        SELECT
            COALESCE(CAST(dept_id AS VARCHAR), '--') AS dept,
            COALESCE(gender, '--') AS gender,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary,
            SUM(salary) AS total_payroll
        FROM employees
        GROUP BY GROUPING SETS ( (dept_id), (gender), () )
        ORDER BY dept, gender;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 34. GROUP BY with Window Functions — Aggregate + Detail Together

    ### NL Query
    > *"Show each department's stats AND rank them by average salary — without losing the grouped summary."*

    ### SQL Concept
    Window functions can be applied **on top of** GROUP BY results. The GROUP BY collapses rows into department summaries, then the window function (like RANK) ranks those summaries.

    ```
    Step 1: GROUP BY → 5 department rows
    Step 2: RANK() OVER (ORDER BY avg_salary DESC) → adds rank to each row
    ```
    """)
    return


@app.cell
def _(con):
    # NL: Department stats ranked by average salary.
    # SQL: GROUP BY + RANK() OVER() on the grouped result

    con.execute("""
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 2) AS avg_salary,
            SUM(salary) AS total_payroll,
            RANK() OVER (
        ORDER BY AVG(salary) DESC) AS salary_rank, RANK() OVER (
        ORDER BY COUNT(*) DESC) AS size_rank, ROUND(SUM(salary) * 100.0 / SUM(SUM(salary)) OVER(), 1) AS pct_of_total_payroll
        FROM employees
        GROUP BY dept_id
        ORDER BY salary_rank;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 35. Grand Finale — Complete Department Analytics Report

    ### NL Query
    > *"Build a comprehensive department report combining: JOIN (department names), GROUP BY (aggregation), HAVING (filter), CASE (classification), Window Functions (ranking), CTE (multi-level), and percentage calculations — all in one query."*

    This query combines **every GROUP BY concept** from this tutorial.
    """)
    return


@app.cell
def _(con):
    # NL: Complete department analytics report combining ALL GROUP BY concepts.

    con.execute("""
        WITH dept_summary AS (
        SELECT
            e.dept_id,
            d.dept_name,
            d.location,
            d.budget,
            COUNT(*) AS emp_count,
            SUM(e.salary) AS total_payroll,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary,
            COUNT(CASE WHEN e.gender = 'F' THEN 1 END) AS female_count,
            COUNT(CASE WHEN e.gender = 'M' THEN 1 END) AS male_count
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY e.dept_id, d.dept_name, d.location, d.budget
        HAVING COUNT(*) >= 3 /* only departments with 3+ employees */ ), company_stats AS (
        SELECT
            ROUND(AVG(salary), 2) AS company_avg,
            SUM(salary) AS company_total
        FROM employees )
        SELECT
            ds.dept_name,
            ds.location,
            ds.emp_count,
            ds.avg_salary,
            cs.company_avg,
            /* vs company average */ CASE WHEN ds.avg_salary >= cs.company_avg THEN '↑ Above' ELSE '↓ Below' END AS vs_company_avg,
            /* salary tier classification */ CASE WHEN ds.avg_salary >= 90000 THEN 'Premium' WHEN ds.avg_salary >= 70000 THEN 'Standard' ELSE 'Budget' END AS dept_tier,
            /* budget utilization */ ROUND(ds.total_payroll * 100.0 / ds.budget, 1) AS budget_util_pct,
            /* share of company payroll */ ROUND(ds.total_payroll * 100.0 / cs.company_total, 1) AS payroll_share_pct,
            /* gender ratio */ ds.female_count || 'F / ' || ds.male_count || 'M' AS gender_split,
            /* rank by avg salary */ RANK() OVER (
        ORDER BY ds.avg_salary DESC) AS salary_rank
        FROM dept_summary ds
        CROSS
        JOIN company_stats cs
        ORDER BY salary_rank;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Appendix — GROUP BY Cheat Sheet & Common Mistakes
    ---

    ## GROUP BY Syntax Quick Reference

    ```sql
    -- Basic GROUP BY
    SELECT column, AGG(column2)
    FROM table
    GROUP BY column

    -- GROUP BY + HAVING
    SELECT column, AGG(column2)
    FROM table
    GROUP BY column
    HAVING AGG(column2) > threshold

    -- WHERE + GROUP BY + HAVING (full pipeline)
    SELECT column, AGG(column2)
    FROM table
    WHERE row_filter
    GROUP BY column
    HAVING group_filter
    ORDER BY sort_column
    LIMIT n

    -- GROUP BY with ROLLUP (subtotals + grand total)
    SELECT column, AGG(column2)
    FROM table
    GROUP BY ROLLUP(column)

    -- GROUP BY with CUBE (all grouping combinations)
    SELECT col1, col2, AGG(col3)
    FROM table
    GROUP BY CUBE(col1, col2)

    -- GROUP BY with GROUPING SETS (custom combos)
    SELECT col1, col2, AGG(col3)
    FROM table
    GROUP BY GROUPING SETS ((col1), (col2), ())
    ```

    ## Execution Order (Critical!)

    ```
    1. FROM / JOIN    ← identify source tables
    2. WHERE          ← filter INDIVIDUAL ROWS (before grouping)
    3. GROUP BY       ← create groups
    4. HAVING         ← filter GROUPS (after grouping)
    5. SELECT         ← compute aggregates, choose columns
    6. Window Fns     ← compute over partitions
    7. ORDER BY       ← sort results
    8. LIMIT/OFFSET   ← paginate
    ```

    ## Aggregate Functions Summary

    | Function | Purpose | NULL handling |
    |----------|---------|---------------|
    | `COUNT(*)` | Count all rows | Counts NULLs |
    | `COUNT(col)` | Count non-NULL values | Skips NULLs |
    | `SUM(col)` | Total | Skips NULLs |
    | `AVG(col)` | Mean | Skips NULLs |
    | `MIN(col)` | Smallest value | Skips NULLs |
    | `MAX(col)` | Largest value | Skips NULLs |
    | `STRING_AGG(col, ',')` | Concatenate values | Skips NULLs |

    ## WHERE vs HAVING — Decision Guide

    ```
    "Filter individual rows before grouping?"  →  WHERE
    "Filter groups after aggregation?"         →  HAVING
    "Need both?"                               →  WHERE + HAVING

    Can I use salary > 70000?
      → Yes in WHERE (row-level comparison)
      → Yes in HAVING (but unusual — better in WHERE)

    Can I use AVG(salary) > 70000?
      → NO in WHERE (aggregates not allowed)
      → Yes in HAVING ✅
    ```

    ## Common Mistakes

    | Mistake | Error | Fix |
    |---------|-------|-----|
    | Non-aggregated column in SELECT | `must appear in GROUP BY` | Add to GROUP BY or wrap in aggregate |
    | Aggregate in WHERE | `aggregate functions not allowed in WHERE` | Use HAVING instead |
    | GROUP BY with SELECT * | Ambiguous columns | List specific columns |
    | HAVING without GROUP BY | Usually an error | Add GROUP BY or use WHERE |
    | Ordering by non-selected column | May work but confusing | Include in SELECT for clarity |

    ---

    *Tutorial by Dr. Mahmoud Parsian — OMIS 105, Santa Clara University*
    *Built with DuckDB and Jupyter Notebooks*
    *Focus: GROUP BY & HAVING — the engine behind every business dashboard*
    """)
    return


@app.cell
def _(con):
    con.close()
    print("Tutorial complete!")
    print("Tables used: employees (20 rows), departments (5 rows)")
    print("Topics covered: 35 sections across 6 parts")
    print("Key concepts: GROUP BY, HAVING, WHERE vs HAVING, ROLLUP, CUBE, GROUPING SETS")
    return


if __name__ == "__main__":
    app.run()
