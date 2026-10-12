import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SQL JOIN Operations in DuckDB
    ## A Comprehensive, Hands-On Tutorial — From Basic to Intermediate+

    **Author**: Dr. Mahmoud Parsian — Santa Clara University
    **Course**: OMIS 105 — Database Management Systems
    **Focus**: JOIN Operations — the most important SQL skill
    **Tool**: DuckDB (in-process analytical database)
    **Format**: Jupyter Notebook

    ---

    ### Why JOINs Are the Most Important SQL Skill

    Real-world databases store data across **multiple tables** to avoid redundancy (normalization).
    To answer any meaningful business question, you must **combine** data from these related tables.
    That is what **JOIN** does.

    A 2024 Stack Overflow survey found that SQL JOIN proficiency is the **#1 technical differentiator**
    between junior and senior data analysts.

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

    ### Part I — Setup & Data Exploration
    1. Setting Up DuckDB
    2. Creating the `departments` Table (5 departments, 2 with no employees)
    3. Creating the `employees` Table (20 employees, some unassigned)
    4. Exploring the Departments Data
    5. Exploring the Employees Data
    6. Understanding the Data Design for JOINs

    ### Part II — Basic JOINs
    7. INNER JOIN — Concept & Visualization
    8. INNER JOIN — Basic Example
    9. INNER JOIN — With Additional Columns
    10. INNER JOIN — With WHERE Filter
    11. INNER JOIN — With ORDER BY
    12. INNER JOIN — With Aggregation (COUNT, AVG)
    13. INNER JOIN — What Gets Excluded?

    ### Part III — LEFT JOIN (LEFT OUTER JOIN)
    14. LEFT JOIN — Concept & Visualization
    15. LEFT JOIN — Basic Example
    16. LEFT JOIN — Finding Unassigned Employees (NULL detection)
    17. LEFT JOIN — COALESCE for Clean Output
    18. LEFT JOIN — With Aggregation
    19. LEFT JOIN — Counting Employees per Department (Including Empty Departments)

    ### Part IV — RIGHT JOIN (RIGHT OUTER JOIN)
    20. RIGHT JOIN — Concept & Visualization
    21. RIGHT JOIN — Basic Example
    22. RIGHT JOIN — Finding Empty Departments
    23. RIGHT JOIN — Equivalence to LEFT JOIN (Reversed)

    ### Part V — FULL OUTER JOIN
    24. FULL OUTER JOIN — Concept & Visualization
    25. FULL OUTER JOIN — Basic Example
    26. FULL OUTER JOIN — Finding ALL Mismatches
    27. FULL OUTER JOIN — Complete Data Audit

    ### Part VI — CROSS JOIN
    28. CROSS JOIN — Concept & Visualization
    29. CROSS JOIN — Cartesian Product
    30. CROSS JOIN — Practical Use Case (Combinations)

    ### Part VII — Self-JOIN
    31. Self-JOIN — Concept
    32. Self-JOIN — Employees in the Same Department
    33. Self-JOIN — Salary Comparisons Within Departments
    34. Self-JOIN — Manager-Employee Relationships

    ### Part VIII — Multi-Table JOINs (Intermediate)
    35. Creating a Third Table: `projects`
    36. Three-Table JOIN — Employees + Departments + Projects
    37. Three-Table JOIN — With Aggregation
    38. LEFT JOIN Chain — Finding Gaps Across Three Tables

    ### Part IX — JOINs with Subqueries & CTEs (Intermediate+)
    39. JOIN with Subquery — Top Earner per Department
    40. JOIN with CTE — Department Statistics Report
    41. JOIN with Multiple CTEs — Comprehensive Analysis
    42. JOIN with Window Functions — Rank Within Department

    ### Part X — Advanced JOIN Patterns (Intermediate+)
    43. Anti-JOIN — Employees NOT in Any Department (Using LEFT JOIN + IS NULL)
    44. Anti-JOIN — Departments with NO Employees
    45. Semi-JOIN — Departments That HAVE Employees (Using EXISTS)
    46. Non-Equi JOIN — Salary Range Matching
    47. NATURAL JOIN — Automatic Column Matching
    48. JOIN with USING Clause
    49. LATERAL JOIN — Correlated Subquery as a JOIN
    50. Grand Finale — Complete HR Analytics Report

    ### Appendix
    - JOIN Type Summary & Cheat Sheet

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART I — Setup & Data Exploration
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Setting Up DuckDB

    DuckDB is an **in-process** analytical database — no server needed.
    We create an in-memory connection that lives as long as this notebook session.
    """)
    return


@app.cell
def _():
    import duckdb

    # Create an in-memory database connection
    con = duckdb.connect(database=':memory:')
    print("DuckDB connection established!")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Creating the `departments` Table

    We create **5 departments**, but intentionally leave **2 departments with no employees assigned**.
    This is critical for demonstrating LEFT JOIN and RIGHT JOIN behavior.

    | dept_id | dept_name | location | budget |
    |---------|-----------|----------|--------|
    | 101 | Engineering | San Jose | 500000 |
    | 102 | Marketing | San Francisco | 200000 |
    | 103 | Sales | Los Angeles | 300000 |
    | 104 | **Research** | **Boston** | **450000** |
    | 105 | **Legal** | **New York** | **180000** |

    > **Key design**: Departments 104 (Research) and 105 (Legal) will have **zero employees** — no employee has `dept_id = 104` or `dept_id = 105`. This lets us demonstrate how different JOINs handle unmatched rows.
    """)
    return


@app.cell
def _(con):
    # Create departments table: 5 departments (2 will have NO employees)
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
            (104, 'Research', 'Boston', 450000.00),
            (105, 'Legal', 'New York', 180000.00);
    """)

    print("departments table created: 5 rows")
    print("  Departments WITH employees: Engineering (101), Marketing (102), Sales (103)")
    print("  Departments with NO employees: Research (104), Legal (105)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Creating the `employees` Table

    We create **20 employees** with deliberate variation:

    - **14 employees** have valid `dept_id` (101, 102, or 103)
    - **3 employees** have `dept_id = NULL` (never assigned to a department)
    - **3 employees** have `dept_id = 999` (references a department that doesn't exist)

    This design ensures we see meaningful differences between INNER, LEFT, RIGHT, and FULL OUTER JOINs.

    | Category | Count | dept_id | JOIN behavior |
    |----------|-------|---------|---------------|
    | Valid department | 14 | 101, 102, 103 | Appear in all JOINs |
    | NULL department | 3 | NULL | Excluded from INNER JOIN; appear in LEFT JOIN |
    | Invalid department | 3 | 999 | Excluded from INNER JOIN; appear in LEFT JOIN |
    """)
    return


@app.cell
def _(con):
    # Create employees table: 20 employees with varied dept_id assignments
    con.execute("""
        CREATE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR NOT NULL,
            dept_id    INTEGER,
            salary     DECIMAL(10,2) NOT NULL,
            hire_date  DATE NOT NULL,
            city       VARCHAR,
            manager_id INTEGER
        );
    """)

    con.execute("""
        INSERT INTO employees
        VALUES
            /* Engineering (dept_id = 101): 6 employees */ (1, 'Alice Johnson', 101, 95000.00, '2019-03-15', 'San Jose', NULL),
            (2, 'Bob Smith', 101, 88000.00, '2020-07-01', 'San Jose', 1),
            (3, 'Carol Williams', 101, 105000.00, '2018-01-10', 'San Jose', 1),
            (4, 'David Brown', 101, 92000.00, '2021-06-20', 'Santa Clara', 1),
            (5, 'Eva Martinez', 101, 78000.00, '2022-04-05', 'San Jose', 3),
            (6, 'Frank Lee', 101, 112000.00, '2017-08-22', 'Sunnyvale', NULL),
            /* Marketing (dept_id = 102): 4 employees */ (7, 'Grace Kim', 102, 72000.00, '2020-11-15', 'San Francisco', NULL),
            (8, 'Henry Chen', 102, 68000.00, '2021-09-01', 'San Francisco', 7),
            (9, 'Iris Patel', 102, 75000.00, '2019-05-20', 'Oakland', 7),
            (10, 'Jack Wilson', 102, 71000.00, '2023-01-08', 'San Francisco', 7),
            /* Sales (dept_id = 103): 4 employees */ (11, 'Karen Davis', 103, 82000.00, '2019-02-14', 'Los Angeles', NULL),
            (12, 'Leo Garcia', 103, 67000.00, '2022-08-30', 'Los Angeles', 11),
            (13, 'Mia Robinson', 103, 73000.00, '2020-12-01', 'Pasadena', 11),
            (14, 'Noah Thompson', 103, 69000.00, '2023-06-15', 'Los Angeles', 11),
            /* NULL dept_id: 3 employees (unassigned — no department) */ (15, 'Olivia White', NULL, 60000.00, '2024-01-10', 'Remote', NULL),
            (16, 'Paul Harris', NULL, 55000.00, '2024-02-20', 'Remote', NULL),
            (17, 'Quinn Adams', NULL, 58000.00, '2024-03-05', NULL, NULL),
            /* Invalid dept_id (999): 3 employees (dept 999 doesn't exist in departments table) */ (18, 'Rachel Clark', 999, 63000.00, '2023-11-01', 'Chicago', NULL),
            (19, 'Sam Turner', 999, 61000.00, '2023-12-15', 'Chicago', NULL),
            (20, 'Tina Baker', 999, 59000.00, '2024-01-20', 'Detroit', NULL);
    """)

    print("employees table created: 20 rows")
    print("  dept_id = 101 (Engineering): 6 employees")
    print("  dept_id = 102 (Marketing):   4 employees")
    print("  dept_id = 103 (Sales):       4 employees")
    print("  dept_id = NULL (unassigned):  3 employees")
    print("  dept_id = 999 (invalid):     3 employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Exploring the Departments Data

    ### NL Query
    > *"Show me all departments with their details."*
    """)
    return


@app.cell
def _(con):
    # NL: Show me all departments with their details.
    # SQL: SELECT * FROM departments ORDER BY dept_id

    con.execute("""
        SELECT *
        FROM departments
        ORDER BY dept_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Exploring the Employees Data

    ### NL Query
    > *"Show me all 20 employees, sorted by emp_id."*
    """)
    return


@app.cell
def _(con):
    # NL: Show me all 20 employees.
    # SQL: SELECT * FROM employees ORDER BY emp_id

    con.execute("""
        SELECT
            emp_id,
            emp_name,
            dept_id,
            salary,
            hire_date,
            city
        FROM employees
        ORDER BY emp_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Understanding the Data Design for JOINs

    Before writing any JOIN, let's visualize what our data looks like and what each JOIN type will produce:

    ```
        employees table                      departments table
        ┌─────────────────────┐              ┌──────────────────┐
        │ emp_id  dept_id     │              │ dept_id dept_name │
        │ ────── ────────     │              │ ─────── ──────── │
        │  1      101    ─────│──────────────│▶ 101   Engineering│
        │  2      101    ─────│──────────────│▶ 101   Engineering│
        │  3      101    ─────│──────────────│▶ 101   Engineering│
        │  4      101    ─────│──────────────│▶ 101   Engineering│
        │  5      101    ─────│──────────────│▶ 101   Engineering│
        │  6      101    ─────│──────────────│▶ 101   Engineering│
        │  7      102    ─────│──────────────│▶ 102   Marketing  │
        │  8      102    ─────│──────────────│▶ 102   Marketing  │
        │  9      102    ─────│──────────────│▶ 102   Marketing  │
        │ 10      102    ─────│──────────────│▶ 102   Marketing  │
        │ 11      103    ─────│──────────────│▶ 103   Sales      │
        │ 12      103    ─────│──────────────│▶ 103   Sales      │
        │ 13      103    ─────│──────────────│▶ 103   Sales      │
        │ 14      103    ─────│──────────────│▶ 103   Sales      │
        │ 15      NULL   ─ ✗  │  No match    │  104   Research   │◀─ No employee
        │ 16      NULL   ─ ✗  │  No match    │  105   Legal      │◀─ No employee
        │ 17      NULL   ─ ✗  │  No match    └──────────────────┘
        │ 18      999    ─ ✗  │  No match (999 not in departments)
        │ 19      999    ─ ✗  │  No match
        │ 20      999    ─ ✗  │  No match
        └─────────────────────┘
    ```

    ### Expected Results by JOIN Type:

    | JOIN Type | Matched (14) | Unmatched Employees (6) | Empty Departments (2) | Total Rows |
    |-----------|:---:|:---:|:---:|:---:|
    | **INNER JOIN** | ✅ 14 | ❌ excluded | ❌ excluded | **14** |
    | **LEFT JOIN** | ✅ 14 | ✅ 6 (dept cols = NULL) | ❌ excluded | **20** |
    | **RIGHT JOIN** | ✅ 14 | ❌ excluded | ✅ 2 (emp cols = NULL) | **16** |
    | **FULL OUTER JOIN** | ✅ 14 | ✅ 6 | ✅ 2 | **22** |
    | **CROSS JOIN** | — | — | — | **20 × 5 = 100** |

    Let's verify these predictions with actual queries!

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART II — Basic JOINs: INNER JOIN
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. INNER JOIN — Concept & Visualization

    An **INNER JOIN** returns only the rows where the join condition matches in **BOTH** tables.
    Any row from either table that has no match is **excluded**.

    ```
        employees                     departments
        ┌──────────┐                  ┌──────────────┐
        │ matched  │─────── ✅ ──────│  matched     │
        │ matched  │─────── ✅ ──────│  matched     │
        │ NULL/999 │─────── ❌       │              │
        │ NULL/999 │─────── ❌       │  Research    │──── ❌ (no match)
        └──────────┘                  │  Legal       │──── ❌ (no match)
                                      └──────────────┘
    ```

    ### Syntax
    ```sql
    SELECT columns
    FROM table_A
    INNER JOIN table_B
        ON table_A.key = table_B.key
    ```

    **Key rule**: INNER JOIN is the **most restrictive** join — it shows only the intersection.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. INNER JOIN — Basic Example

    ### NL Query
    > *"Show each employee alongside their department name. Only include employees who belong to a valid department."*

    ### What to expect
    - 14 rows (the 14 employees with valid dept_id: 101, 102, 103)
    - 6 employees excluded (3 with NULL, 3 with 999)
    - 2 departments excluded (Research 104, Legal 105)
    """)
    return


@app.cell
def _(con):
    # NL: Show each employee alongside their department name.
    # SQL: SELECT ... FROM employees INNER JOIN departments ON ...

    con.execute("""
        SELECT
            e.emp_id,
            e.emp_name,
            e.dept_id,
            d.dept_name
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY e.emp_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. INNER JOIN — With Additional Columns

    ### NL Query
    > *"Show each employee's name, salary, their department name, location, and budget."*

    ### SQL Concept
    You can select columns from **both** tables. Use table aliases (`e`, `d`) to avoid ambiguity when column names appear in multiple tables (like `dept_id`).
    """)
    return


@app.cell
def _(con):
    # NL: Show employee name, salary, department name, location, and budget.
    # SQL: SELECT e.emp_name, e.salary, d.dept_name, d.location, d.budget

    con.execute("""
        SELECT
            e.emp_name,
            e.salary,
            d.dept_name,
            d.location,
            d.budget
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name, e.salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. INNER JOIN — With WHERE Filter

    ### NL Query
    > *"Show employees in the Engineering department who earn more than $90,000."*

    ### SQL Concept
    `WHERE` filters rows **after** the JOIN. The JOIN combines the tables first, then WHERE removes rows that don't meet the condition.

    **Execution order**: `FROM` → `JOIN` → `WHERE` → `SELECT` → `ORDER BY`
    """)
    return


@app.cell
def _(con):
    # NL: Engineering employees earning more than $90,000.
    # SQL: ... INNER JOIN ... WHERE d.dept_name = 'Engineering' AND e.salary > 90000

    con.execute("""
        SELECT
            e.emp_name,
            d.dept_name,
            e.salary
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE d.dept_name = 'Engineering'
        AND e.salary > 90000
        ORDER BY e.salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11. INNER JOIN — With ORDER BY

    ### NL Query
    > *"Show all matched employees, sorted first by department name, then by hire date (newest first)."*

    ### SQL Concept
    You can ORDER BY columns from **either** table in the JOIN. Multi-column sorting uses commas: the first column is the primary sort, the second breaks ties.
    """)
    return


@app.cell
def _(con):
    # NL: All matched employees sorted by department, then by hire date (newest first).
    # SQL: ... INNER JOIN ... ORDER BY d.dept_name, e.hire_date DESC

    con.execute("""
        SELECT
            e.emp_name,
            d.dept_name,
            e.hire_date,
            e.salary
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name ASC, e.hire_date DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12. INNER JOIN — With Aggregation (COUNT, AVG)

    ### NL Query
    > *"For each department, how many employees does it have and what is the average salary?"*

    ### SQL Concept
    You can combine INNER JOIN with GROUP BY and aggregate functions. The JOIN combines tables, then GROUP BY collapses rows into groups, and aggregates compute summary values.
    """)
    return


@app.cell
def _(con):
    # NL: Employee count and average salary per department.
    # SQL: ... INNER JOIN ... GROUP BY d.dept_name

    con.execute("""
        SELECT
            d.dept_name,
            d.location,
            COUNT(*) AS emp_count,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary,
            SUM(e.salary) AS total_salary
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name, d.location
        ORDER BY emp_count DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13. INNER JOIN — What Gets Excluded?

    ### NL Query
    > *"Which employees are NOT included in the INNER JOIN result? Which departments are missing?"*

    ### SQL Concept
    This is crucial to understand: INNER JOIN silently drops unmatched rows from **both sides**.
    Let's see exactly who gets left out.
    """)
    return


@app.cell
def _(con):
    # NL: Which employees are excluded from INNER JOIN?
    # SQL: Find employees whose dept_id is NOT in the departments table

    print("=== Employees EXCLUDED from INNER JOIN ===")
    print("(dept_id is NULL or not in departments table)")
    print()
    excluded = con.execute("""
        SELECT
            emp_id,
            emp_name,
            dept_id,
            CASE WHEN dept_id IS NULL THEN 'No department assigned (NULL)' ELSE 'dept_id ' || CAST(dept_id AS VARCHAR) || ' does not exist' END AS reason_excluded
        FROM employees
        WHERE dept_id IS NULL
        OR dept_id NOT IN (
        SELECT dept_id
        FROM departments)
        ORDER BY emp_id;
    """).fetchdf()
    print(excluded.to_string(index=False))

    print()
    print("=== Departments EXCLUDED from INNER JOIN ===")
    print("(no employee has this dept_id)")
    print()
    excluded_depts = con.execute("""
        SELECT
            d.dept_id,
            d.dept_name,
            d.location,
            'Zero employees assigned' AS reason_excluded
        FROM departments d
        WHERE d.dept_id NOT IN (
        SELECT DISTINCT dept_id
        FROM employees
        WHERE dept_id IS NOT NULL )
        ORDER BY d.dept_id;
    """).fetchdf()
    print(excluded_depts.to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART III — LEFT JOIN (LEFT OUTER JOIN)
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14. LEFT JOIN — Concept & Visualization

    A **LEFT JOIN** returns **ALL rows from the left table** (employees), plus matching rows from the right table (departments). If there's no match, the right-side columns are filled with **NULL**.

    ```
        employees (LEFT)              departments (RIGHT)
        ┌──────────────┐              ┌──────────────┐
        │ Alice   101  │─── ✅ ──────│ Engineering  │
        │ Bob     101  │─── ✅ ──────│ Engineering  │
        │ ...     ...  │─── ✅ ──────│ ...          │
        │ Olivia  NULL │─── ✅ ──────│ NULL, NULL   │  ← kept, dept = NULL
        │ Rachel  999  │─── ✅ ──────│ NULL, NULL   │  ← kept, dept = NULL
        └──────────────┘              │ Research 104 │  ← ❌ excluded
                                      │ Legal    105 │  ← ❌ excluded
                                      └──────────────┘
    ```

    ### Syntax
    ```sql
    SELECT columns
    FROM left_table
    LEFT JOIN right_table
        ON left_table.key = right_table.key
    ```

    **Key rule**: LEFT JOIN **never drops rows from the left table**. It guarantees every left-side row appears in the result.

    ### When to use LEFT JOIN
    - Find records with no match ("orphaned" records)
    - Include all items even if related data is missing
    - Count items per category, including categories with zero items
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 15. LEFT JOIN — Basic Example

    ### NL Query
    > *"Show ALL employees with their department name. Include employees who have no valid department."*

    ### What to expect
    - **20 rows** (all employees preserved)
    - 14 rows with department info filled in
    - 6 rows with NULL for dept_name, location (3 NULL dept_id + 3 invalid dept_id 999)
    """)
    return


@app.cell
def _(con):
    # NL: Show ALL employees with their department name, including unassigned.
    # SQL: SELECT ... FROM employees LEFT JOIN departments ON ...

    con.execute("""
        SELECT
            e.emp_id,
            e.emp_name,
            e.dept_id,
            d.dept_name,
            d.location
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY e.emp_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 16. LEFT JOIN — Finding Unassigned Employees (NULL Detection)

    ### NL Query
    > *"Show me ONLY the employees who do not belong to any valid department."*

    ### SQL Concept
    This is the **Anti-JOIN pattern** using LEFT JOIN:
    1. LEFT JOIN keeps all employees
    2. `WHERE d.dept_id IS NULL` filters to only the ones with **no match**

    This pattern is one of the most useful in all of SQL — it finds "orphans," "gaps," and "missing" relationships.
    """)
    return


@app.cell
def _(con):
    # NL: Show ONLY employees who don't belong to any valid department.
    # SQL: LEFT JOIN ... WHERE d.dept_id IS NULL

    con.execute("""
        SELECT
            e.emp_id,
            e.emp_name,
            e.dept_id AS employee_dept_id,
            e.salary,
            CASE WHEN e.dept_id IS NULL THEN 'Never assigned a department' ELSE 'dept_id ' || CAST(e.dept_id AS VARCHAR) || ' does not exist' END AS status
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE d.dept_id IS NULL
        ORDER BY e.emp_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 17. LEFT JOIN — COALESCE for Clean Output

    ### NL Query
    > *"Show all employees with their department name. Replace missing departments with 'Unassigned'."*

    ### SQL Concept
    `COALESCE(value, default)` returns the first non-NULL argument. Combined with LEFT JOIN, it lets you provide user-friendly defaults for missing data instead of showing raw NULLs.
    """)
    return


@app.cell
def _(con):
    # NL: All employees — replace NULL department with 'Unassigned'.
    # SQL: LEFT JOIN ... COALESCE(d.dept_name, 'Unassigned')

    con.execute("""
        SELECT
            e.emp_id,
            e.emp_name,
            COALESCE(d.dept_name, 'Unassigned') AS department,
            COALESCE(d.location, 'N/A') AS location,
            e.salary
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY department, e.emp_name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 18. LEFT JOIN — With Aggregation

    ### NL Query
    > *"What is the total salary cost broken down by department status (assigned vs unassigned)?"*
    """)
    return


@app.cell
def _(con):
    # NL: Total salary cost by department status (assigned vs unassigned).
    # SQL: LEFT JOIN ... GROUP BY ...

    con.execute("""
        SELECT
            COALESCE(d.dept_name, 'Unassigned') AS department,
            COUNT(*) AS emp_count,
            SUM(e.salary) AS total_salary,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            ROUND(SUM(e.salary) * 100.0 / (
        SELECT SUM(salary)
        FROM employees), 1) AS pct_of_total_payroll
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY COALESCE(d.dept_name, 'Unassigned')
        ORDER BY total_salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 19. LEFT JOIN — Counting Employees per Department (Including Empty Departments)

    ### NL Query
    > *"Show the employee count for EVERY department, including Research and Legal which have zero employees."*

    ### SQL Concept
    This is a critical difference from INNER JOIN + GROUP BY:
    - **INNER JOIN + GROUP BY**: Only shows departments that **have** employees (3 rows)
    - **LEFT JOIN + GROUP BY** (with departments on the left): Shows **all** departments (5 rows)

    Note: We flip the table order — departments on the LEFT — to keep all departments.
    """)
    return


@app.cell
def _(con):
    # NL: Employee count for EVERY department (including empty ones).
    # SQL: departments LEFT JOIN employees ... GROUP BY d.dept_name
    # NOTE: departments is now the LEFT table!

    con.execute("""
        SELECT
            d.dept_id,
            d.dept_name,
            d.location,
            COUNT(e.emp_id) AS emp_count,
            COALESCE(SUM(e.salary), 0) AS total_salary
        FROM departments d
        LEFT
        JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_id, d.dept_name, d.location
        ORDER BY emp_count DESC, d.dept_name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART IV — RIGHT JOIN (RIGHT OUTER JOIN)
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 20. RIGHT JOIN — Concept & Visualization

    A **RIGHT JOIN** returns **ALL rows from the right table** (departments), plus matching rows from the left table (employees). If there's no match, the left-side columns are filled with **NULL**.

    ```
        employees (LEFT)              departments (RIGHT)
        ┌──────────────┐              ┌──────────────┐
        │ Alice   101  │─── ✅ ──────│ Engineering  │  ← kept
        │ Bob     101  │─── ✅ ──────│ Engineering  │  ← kept
        │ ...     ...  │              │ ...          │
        │ Olivia  NULL │─── ❌       │              │
        │ Rachel  999  │─── ❌       │ Research 104 │  ← ✅ kept (emp = NULL)
        └──────────────┘              │ Legal    105 │  ← ✅ kept (emp = NULL)
                                      └──────────────┘
    ```

    ### Syntax
    ```sql
    SELECT columns
    FROM left_table
    RIGHT JOIN right_table
        ON left_table.key = right_table.key
    ```

    ### RIGHT JOIN vs LEFT JOIN
    A RIGHT JOIN is the **mirror image** of a LEFT JOIN. In practice, most SQL developers prefer LEFT JOIN and simply swap the table order. RIGHT JOIN exists for readability in some cases.

    ```
    A LEFT JOIN B   ≡   B RIGHT JOIN A
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 21. RIGHT JOIN — Basic Example

    ### NL Query
    > *"Show ALL departments with their employees. Include departments that have no employees."*

    ### What to expect
    - **16 rows**: 14 matched + 2 empty departments (Research, Legal)
    - The 6 unassigned employees (NULL/999 dept_id) are **excluded**
    """)
    return


@app.cell
def _(con):
    # NL: Show ALL departments with their employees, including empty departments.
    # SQL: SELECT ... FROM employees RIGHT JOIN departments ON ...

    con.execute("""
        SELECT
            d.dept_id,
            d.dept_name,
            d.location,
            e.emp_id,
            e.emp_name,
            e.salary
        FROM employees e
        RIGHT
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_id, e.emp_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 22. RIGHT JOIN — Finding Empty Departments

    ### NL Query
    > *"Which departments have NO employees at all?"*

    ### SQL Concept
    Same anti-join pattern as LEFT JOIN, but from the right side:
    1. RIGHT JOIN keeps all departments
    2. `WHERE e.emp_id IS NULL` filters to only departments with **no matching employees**
    """)
    return


@app.cell
def _(con):
    # NL: Which departments have NO employees?
    # SQL: RIGHT JOIN ... WHERE e.emp_id IS NULL

    con.execute("""
        SELECT
            d.dept_id,
            d.dept_name,
            d.location,
            d.budget,
            'No employees assigned' AS status
        FROM employees e
        RIGHT
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE e.emp_id IS NULL
        ORDER BY d.dept_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 23. RIGHT JOIN — Equivalence to LEFT JOIN (Reversed)

    ### NL Query
    > *"Prove that RIGHT JOIN gives the same result as LEFT JOIN with tables swapped."*

    ### SQL Concept
    These two queries produce **identical results**:
    ```sql
    -- Query A: employees RIGHT JOIN departments
    SELECT ... FROM employees e RIGHT JOIN departments d ON e.dept_id = d.dept_id

    -- Query B: departments LEFT JOIN employees (tables swapped)
    SELECT ... FROM departments d LEFT JOIN employees e ON d.dept_id = e.dept_id
    ```

    Most developers prefer LEFT JOIN because reading left-to-right is more natural.
    """)
    return


@app.cell
def _(con):
    # NL: Prove RIGHT JOIN = LEFT JOIN with swapped tables.

    # RIGHT JOIN version
    right_result = con.execute("""
        SELECT
            d.dept_name,
            COUNT(e.emp_id) AS emp_count
        FROM employees e
        RIGHT
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY d.dept_name;
    """).fetchdf()

    # LEFT JOIN version (tables swapped)
    left_result = con.execute("""
        SELECT
            d.dept_name,
            COUNT(e.emp_id) AS emp_count
        FROM departments d
        LEFT
        JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
        ORDER BY d.dept_name;
    """).fetchdf()

    print("RIGHT JOIN result:")
    print(right_result.to_string(index=False))
    print()
    print("LEFT JOIN (swapped) result:")
    print(left_result.to_string(index=False))
    print()
    print(f"Results identical? {right_result.equals(left_result)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART V — FULL OUTER JOIN
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 24. FULL OUTER JOIN — Concept & Visualization

    A **FULL OUTER JOIN** returns ALL rows from **BOTH** tables. Where there's a match, columns are filled in from both sides. Where there's no match, the missing side gets NULLs.

    ```
        employees (LEFT)              departments (RIGHT)
        ┌──────────────┐              ┌──────────────┐
        │ Alice   101  │─── ✅ ──────│ Engineering  │  ← both matched
        │ ...     ...  │─── ✅ ──────│ ...          │
        │ Olivia  NULL │─── ✅       │              │  ← left only (dept=NULL)
        │ Rachel  999  │─── ✅       │              │  ← left only (dept=NULL)
        └──────────────┘              │ Research 104 │  ← ✅ right only (emp=NULL)
                                      │ Legal    105 │  ← ✅ right only (emp=NULL)
                                      └──────────────┘
    ```

    ### Syntax
    ```sql
    SELECT columns
    FROM table_A
    FULL OUTER JOIN table_B
        ON table_A.key = table_B.key
    ```

    ### What to expect
    - **22 rows** total: 14 matched + 6 unmatched employees + 2 unmatched departments
    - FULL OUTER JOIN = LEFT JOIN ∪ RIGHT JOIN
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 25. FULL OUTER JOIN — Basic Example

    ### NL Query
    > *"Show every employee and every department — even if they don't match each other."*
    """)
    return


@app.cell
def _(con):
    # NL: Show every employee and every department, even unmatched.
    # SQL: SELECT ... FROM employees FULL OUTER JOIN departments ON ...

    con.execute("""
        SELECT
            e.emp_id,
            e.emp_name,
            e.dept_id AS emp_dept_id,
            d.dept_id AS dept_dept_id,
            d.dept_name,
            d.location
        FROM employees e
        FULL OUTER
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY COALESCE(e.emp_id, 999), COALESCE(d.dept_id, 999);
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 26. FULL OUTER JOIN — Finding ALL Mismatches

    ### NL Query
    > *"Show me everything that's broken: employees without departments AND departments without employees."*

    ### SQL Concept
    Filter the FULL OUTER JOIN to show ONLY the unmatched rows from either side. This is a powerful **data quality audit** technique.
    """)
    return


@app.cell
def _(con):
    # NL: Show all mismatches — employees without depts AND depts without employees.
    # SQL: FULL OUTER JOIN ... WHERE e.emp_id IS NULL OR d.dept_id IS NULL

    con.execute("""
        SELECT
            COALESCE(CAST(e.emp_id AS VARCHAR), '---') AS emp_id,
            COALESCE(e.emp_name, '---') AS emp_name,
            COALESCE(CAST(e.dept_id AS VARCHAR), 'NULL') AS emp_dept_id,
            COALESCE(CAST(d.dept_id AS VARCHAR), '---') AS dept_id,
            COALESCE(d.dept_name, '---') AS dept_name,
            CASE WHEN d.dept_id IS NULL
        AND e.dept_id IS NULL THEN 'Employee has no dept (NULL)' WHEN d.dept_id IS NULL
        AND e.dept_id IS NOT NULL THEN 'Employee has invalid dept_id' WHEN e.emp_id IS NULL THEN 'Department has no employees' END AS mismatch_type
        FROM employees e
        FULL OUTER
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE e.emp_id IS NULL
        OR d.dept_id IS NULL
        ORDER BY mismatch_type, emp_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 27. FULL OUTER JOIN — Complete Data Audit Summary

    ### NL Query
    > *"Give me a summary: how many matched, how many unmatched on each side?"*
    """)
    return


@app.cell
def _(con):
    # NL: Summary of matched vs unmatched for the entire dataset.
    # SQL: FULL OUTER JOIN with CASE-based classification

    con.execute("""
        SELECT CASE WHEN e.emp_id IS NOT NULL
        AND d.dept_id IS NOT NULL THEN 'Matched' WHEN e.emp_id IS NOT NULL
        AND d.dept_id IS NULL THEN 'Employee without department' WHEN e.emp_id IS NULL
        AND d.dept_id IS NOT NULL THEN 'Department without employees' END AS match_status, COUNT(*) AS row_count
        FROM employees e
        FULL OUTER
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY match_status
        ORDER BY row_count DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART VI — CROSS JOIN
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 28. CROSS JOIN — Concept & Visualization

    A **CROSS JOIN** produces the **Cartesian product** — every row from the left table paired with every row from the right table. No `ON` clause is needed (or allowed).

    ```
    employees (20 rows)  ×  departments (5 rows)  =  100 rows
    ```

    ### Syntax
    ```sql
    SELECT columns
    FROM table_A
    CROSS JOIN table_B
    ```

    ### When to use CROSS JOIN
    - Generating all possible combinations (e.g., every employee × every department)
    - Creating test data
    - Comparing each row against a summary (e.g., each salary vs. company average)

    ### Warning
    CROSS JOINs can produce **enormous** result sets. A 10,000-row table crossed with a 10,000-row table = **100 million rows**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 29. CROSS JOIN — Cartesian Product

    ### NL Query
    > *"Show every possible employee-department combination. How many rows does this produce?"*
    """)
    return


@app.cell
def _(con):
    # NL: Every possible employee-department combination.
    # SQL: SELECT ... FROM employees CROSS JOIN departments

    # Show count first
    count = con.execute("""
        SELECT COUNT(*) AS total_combinations
        FROM employees e
        CROSS
        JOIN departments d;
    """).fetchone()[0]
    print(f"Total combinations: {count} (20 employees × 5 departments)")
    print()

    # Show a sample (first 10)
    con.execute("""
        SELECT
            e.emp_name,
            d.dept_name,
            d.location
        FROM employees e
        CROSS
        JOIN departments d
        WHERE e.emp_id <= 3
        ORDER BY e.emp_name, d.dept_name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 30. CROSS JOIN — Practical Use Case (Compare Each Employee to Company Average)

    ### NL Query
    > *"Show each employee's salary and how far it is from the overall company average."*

    ### SQL Concept
    CROSS JOIN with a **single-row subquery** is a clean pattern: compute a summary once, then compare every row to it.
    """)
    return


@app.cell
def _(con):
    # NL: Each employee's salary vs company average.
    # SQL: CROSS JOIN with aggregated subquery

    con.execute("""
        SELECT
            e.emp_name,
            e.salary,
            stats.avg_salary,
            ROUND(e.salary - stats.avg_salary, 2) AS diff_from_avg,
            CASE WHEN e.salary >= stats.avg_salary THEN 'Above Average' ELSE 'Below Average' END AS status
        FROM employees e
        CROSS
        JOIN (
        SELECT ROUND(AVG(salary), 2) AS avg_salary
        FROM employees ) stats
        ORDER BY e.salary DESC
        LIMIT 10;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART VII — Self-JOIN
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 31. Self-JOIN — Concept

    A **self-join** joins a table to **itself**. You use table aliases (e.g., `e1`, `e2`) to treat the same table as if it were two separate tables.

    ### When to use Self-JOIN
    - **Hierarchies**: employee → manager relationships (both are in the same table)
    - **Comparisons**: find employees in the same department
    - **Pairs**: find all pairs of rows meeting some condition

    ### Syntax
    ```sql
    SELECT a.col, b.col
    FROM table_name a
    JOIN table_name b
        ON a.some_col = b.some_col
        AND a.id < b.id   -- prevents duplicates and self-matches
    ```

    The `a.id < b.id` condition is critical — it prevents:
    - An employee pairing with **themselves** (a.id = b.id)
    - Duplicate pairs in reverse order (Alice-Bob and Bob-Alice)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 32. Self-JOIN — Employees in the Same Department

    ### NL Query
    > *"Find all pairs of employees who work in the same department."*
    """)
    return


@app.cell
def _(con):
    # NL: All pairs of employees in the same department.
    # SQL: employees e1 JOIN employees e2 ON e1.dept_id = e2.dept_id AND e1.emp_id < e2.emp_id

    con.execute("""
        SELECT
            e1.emp_name AS employee_1,
            e2.emp_name AS employee_2,
            e1.dept_id
        FROM employees e1
        JOIN employees e2 ON e1.dept_id = e2.dept_id
        AND e1.emp_id < e2.emp_id
        WHERE e1.dept_id IN (102, 103)
        ORDER BY e1.dept_id, e1.emp_name, e2.emp_name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 33. Self-JOIN — Salary Comparisons Within Departments

    ### NL Query
    > *"For each pair of employees in the same department, show who earns more and by how much."*
    """)
    return


@app.cell
def _(con):
    # NL: Salary comparison between pairs in the same department.
    # SQL: Self-join with salary difference

    con.execute("""
        SELECT
            e1.emp_name AS higher_earner,
            e2.emp_name AS lower_earner,
            e1.dept_id,
            e1.salary AS salary_1,
            e2.salary AS salary_2,
            e1.salary - e2.salary AS salary_gap
        FROM employees e1
        JOIN employees e2 ON e1.dept_id = e2.dept_id
        AND e1.salary > e2.salary
        WHERE e1.dept_id = 101
        ORDER BY salary_gap DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 34. Self-JOIN — Manager-Employee Relationships

    ### NL Query
    > *"Show each employee alongside their manager's name (the manager_id column references another emp_id)."*

    ### SQL Concept
    The `manager_id` column in the employees table references another row's `emp_id`. A self-join with a LEFT JOIN (to keep employees with no manager) reveals the hierarchy.
    """)
    return


@app.cell
def _(con):
    # NL: Show each employee alongside their manager's name.
    # SQL: employees e LEFT JOIN employees m ON e.manager_id = m.emp_id

    con.execute("""
        SELECT
            e.emp_id,
            e.emp_name AS employee,
            e.manager_id,
            COALESCE(m.emp_name, '-- No Manager --') AS manager_name,
            e.dept_id
        FROM employees e
        LEFT
        JOIN employees m ON e.manager_id = m.emp_id
        WHERE e.dept_id IS NOT NULL
        AND e.dept_id != 999
        ORDER BY e.dept_id, e.emp_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART VIII — Multi-Table JOINs (Intermediate)
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 35. Creating a Third Table: `projects`

    To demonstrate multi-table JOINs, we add a `projects` table linking employees to projects. Some employees have projects; some don't. Some departments have projects; some don't.
    """)
    return


@app.cell
def _(con):
    # Create projects table
    con.execute("""
        CREATE TABLE projects (
            project_id   INTEGER PRIMARY KEY,
            project_name VARCHAR NOT NULL,
            dept_id      INTEGER,
            lead_emp_id  INTEGER,
            budget       DECIMAL(10,2),
            status       VARCHAR
        );
    """)

    con.execute("""
        INSERT INTO projects
        VALUES
            (1001, 'Cloud Migration', 101, 1, 150000.00, 'Active'),
            (1002, 'AI Platform', 101, 3, 200000.00, 'Active'),
            (1003, 'Mobile App v2', 101, 6, 120000.00, 'Completed'),
            (1004, 'Brand Refresh', 102, 7, 80000.00, 'Active'),
            (1005, 'Holiday Campaign', 102, 9, 60000.00, 'Planning'),
            (1006, 'West Coast Push', 103, 11, 90000.00, 'Active'),
            (1007, 'Research Initiative', 104, NULL, 300000.00, 'Planning'),
            (1008, 'Patent Filing', 105, NULL, 50000.00, 'Planning');
    """)

    con.execute("""
        SELECT *
        FROM projects
        ORDER BY project_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 36. Three-Table JOIN — Employees + Departments + Projects

    ### NL Query
    > *"Show each project with its department name, location, and the name of the project lead."*

    ### SQL Concept
    Chain JOINs by adding another `JOIN` clause. Each JOIN connects two tables via a condition. You can mix JOIN types in the same query.
    """)
    return


@app.cell
def _(con):
    # NL: Each project with department name and project lead name.
    # SQL: projects JOIN departments JOIN employees (three-table)

    con.execute("""
        SELECT
            p.project_name,
            p.status,
            d.dept_name,
            d.location,
            COALESCE(e.emp_name, 'Unassigned') AS project_lead,
            p.budget AS project_budget
        FROM projects p
        INNER
        JOIN departments d ON p.dept_id = d.dept_id
        LEFT
        JOIN employees e ON p.lead_emp_id = e.emp_id
        ORDER BY d.dept_name, p.project_name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 37. Three-Table JOIN — With Aggregation

    ### NL Query
    > *"For each department, show the number of active projects and the total project budget."*
    """)
    return


@app.cell
def _(con):
    # NL: Active projects and total project budget per department.
    # SQL: departments LEFT JOIN projects ... GROUP BY

    con.execute("""
        SELECT
            d.dept_name,
            COUNT(p.project_id) AS total_projects,
            COUNT(CASE WHEN p.status = 'Active' THEN 1 END) AS active_projects,
            COALESCE(SUM(p.budget), 0) AS total_project_budget,
            d.budget AS dept_budget,
            ROUND(COALESCE(SUM(p.budget), 0) * 100.0 / d.budget, 1) AS pct_budget_in_projects
        FROM departments d
        LEFT
        JOIN projects p ON d.dept_id = p.dept_id
        GROUP BY d.dept_name, d.budget
        ORDER BY total_projects DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 38. LEFT JOIN Chain — Finding Gaps Across Three Tables

    ### NL Query
    > *"Show all employees: their department (if any), and any projects they lead (if any). I want to see who has no department AND who has no project."*
    """)
    return


@app.cell
def _(con):
    # NL: All employees with dept and project info — showing gaps.
    # SQL: employees LEFT JOIN departments LEFT JOIN projects

    con.execute("""
        SELECT
            e.emp_name,
            COALESCE(d.dept_name, 'No Dept') AS department,
            COALESCE(p.project_name, 'No Project') AS project_led,
            e.salary
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        LEFT
        JOIN projects p ON e.emp_id = p.lead_emp_id
        ORDER BY CASE WHEN d.dept_name IS NULL THEN 1 ELSE 0 END, d.dept_name, e.emp_name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART IX — JOINs with Subqueries & CTEs (Intermediate+)
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 39. JOIN with Subquery — Top Earner per Department

    ### NL Query
    > *"Show the highest-paid employee in each department."*

    ### SQL Concept
    Use a subquery to find the max salary per department, then JOIN back to get the employee details.
    """)
    return


@app.cell
def _(con):
    # NL: Highest-paid employee in each department.
    # SQL: JOIN with subquery that finds MAX(salary) per dept

    con.execute("""
        SELECT
            e.emp_name,
            d.dept_name,
            e.salary
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        INNER
        JOIN (
        SELECT
            dept_id,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY dept_id ) top ON e.dept_id = top.dept_id
        AND e.salary = top.max_salary
        ORDER BY e.salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 40. JOIN with CTE — Department Statistics Report

    ### NL Query
    > *"For each employee, show their salary alongside their department's average salary, and whether they're above or below it."*

    ### SQL Concept
    A CTE computes department stats first, then we JOIN the employees to this summary.
    """)
    return


@app.cell
def _(con):
    # NL: Each employee vs their department's average salary.
    # SQL: WITH dept_stats AS (...) SELECT ... JOIN dept_stats

    con.execute("""
        WITH dept_stats AS (
        SELECT
            dept_id,
            ROUND(AVG(salary), 2) AS dept_avg,
            COUNT(*) AS dept_size
        FROM employees
        WHERE dept_id IS NOT NULL
        GROUP BY dept_id )
        SELECT
            e.emp_name,
            d.dept_name,
            e.salary,
            ds.dept_avg,
            e.salary - ds.dept_avg AS diff,
            CASE WHEN e.salary >= ds.dept_avg THEN 'Above' ELSE 'Below' END AS vs_avg
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        INNER
        JOIN dept_stats ds ON e.dept_id = ds.dept_id
        ORDER BY d.dept_name, e.salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 41. JOIN with Multiple CTEs — Comprehensive Analysis

    ### NL Query
    > *"Create a report showing each department with: employee count, average salary, total project budget, and a department health score (based on budget utilization)."*
    """)
    return


@app.cell
def _(con):
    # NL: Comprehensive department report with multiple CTEs.
    # SQL: WITH emp_stats, proj_stats ... JOIN both

    con.execute("""
        WITH emp_stats AS (
        SELECT
            dept_id,
            COUNT(*) AS emp_count,
            ROUND(AVG(salary), 0) AS avg_salary,
            SUM(salary) AS total_salary
        FROM employees
        WHERE dept_id IN (
        SELECT dept_id
        FROM departments)
        GROUP BY dept_id ), proj_stats AS (
        SELECT
            dept_id,
            COUNT(*) AS project_count,
            COUNT(CASE WHEN status = 'Active' THEN 1 END) AS active_projects,
            COALESCE(SUM(budget), 0) AS total_proj_budget
        FROM projects
        GROUP BY dept_id )
        SELECT
            d.dept_name,
            COALESCE(es.emp_count, 0) AS employees,
            COALESCE(es.avg_salary, 0) AS avg_salary,
            COALESCE(ps.project_count, 0) AS projects,
            COALESCE(ps.active_projects, 0) AS active,
            d.budget AS dept_budget,
            COALESCE(es.total_salary, 0) AS salary_cost,
            ROUND(COALESCE(es.total_salary, 0) * 100.0 / d.budget, 1) AS budget_utilization_pct
        FROM departments d
        LEFT
        JOIN emp_stats es ON d.dept_id = es.dept_id
        LEFT
        JOIN proj_stats ps ON d.dept_id = ps.dept_id
        ORDER BY budget_utilization_pct DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 42. JOIN with Window Functions — Rank Within Department

    ### NL Query
    > *"Rank each employee by salary within their department, and show their salary as a percentage of the department total."*
    """)
    return


@app.cell
def _(con):
    # NL: Rank each employee within dept + salary as % of dept total.
    # SQL: JOIN + ROW_NUMBER() OVER (PARTITION BY ...) + SUM() OVER (...)

    con.execute("""
        SELECT
            e.emp_name,
            d.dept_name,
            e.salary,
            ROW_NUMBER() OVER (PARTITION BY d.dept_name
        ORDER BY e.salary DESC) AS dept_rank, SUM(e.salary) OVER (PARTITION BY d.dept_name) AS dept_total, ROUND(e.salary * 100.0 / SUM(e.salary) OVER (PARTITION BY d.dept_name), 1) AS pct_of_dept
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name, dept_rank;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # PART X — Advanced JOIN Patterns (Intermediate+)
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 43. Anti-JOIN — Employees NOT in Any Department

    ### NL Query
    > *"Find employees who are NOT assigned to any existing department."*

    ### SQL Concept
    An **Anti-JOIN** finds rows in table A that have **no match** in table B. The pattern is:

    ```sql
    SELECT a.*
    FROM table_A a
    LEFT JOIN table_B b ON a.key = b.key
    WHERE b.key IS NULL    -- ← only the unmatched rows
    ```

    This is equivalent to `NOT EXISTS` and `NOT IN`, but often performs best.
    """)
    return


@app.cell
def _(con):
    # NL: Employees NOT in any existing department (Anti-JOIN pattern).
    # SQL: LEFT JOIN ... WHERE d.dept_id IS NULL

    con.execute("""
        SELECT
            e.emp_id,
            e.emp_name,
            e.dept_id,
            e.salary,
            e.city
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE d.dept_id IS NULL
        ORDER BY e.emp_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 44. Anti-JOIN — Departments with NO Employees

    ### NL Query
    > *"Find departments that have zero employees assigned."*
    """)
    return


@app.cell
def _(con):
    # NL: Departments with NO employees (Anti-JOIN).
    # SQL: departments LEFT JOIN employees ... WHERE e.emp_id IS NULL

    con.execute("""
        SELECT
            d.dept_id,
            d.dept_name,
            d.location,
            d.budget,
            'No employees' AS status
        FROM departments d
        LEFT
        JOIN employees e ON d.dept_id = e.dept_id
        WHERE e.emp_id IS NULL
        ORDER BY d.dept_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 45. Semi-JOIN — Departments That HAVE Employees (Using EXISTS)

    ### NL Query
    > *"Show only the departments that have at least one employee."*

    ### SQL Concept
    A **Semi-JOIN** is the opposite of an Anti-JOIN: it returns rows from table A that **have at least one match** in table B. Use `EXISTS` for this pattern — it stops searching as soon as it finds the first match (efficient!).
    """)
    return


@app.cell
def _(con):
    # NL: Departments that have at least one employee (Semi-JOIN).
    # SQL: SELECT ... FROM departments WHERE EXISTS (...)

    con.execute("""
        SELECT
            d.dept_id,
            d.dept_name,
            d.location,
            d.budget
        FROM departments d
        WHERE EXISTS (
        SELECT 1
        FROM employees e
        WHERE e.dept_id = d.dept_id )
        ORDER BY d.dept_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 46. Non-Equi JOIN — Salary Range Matching

    ### NL Query
    > *"Create salary bands and assign each employee to a band based on their salary range."*

    ### SQL Concept
    A **Non-Equi JOIN** uses inequality operators (`<`, `>`, `<=`, `>=`, `BETWEEN`) instead of `=`. This is useful for range-based matching like salary bands, tax brackets, or grading scales.
    """)
    return


@app.cell
def _(con):
    # Create a salary_bands reference table
    con.execute("""
        CREATE TABLE salary_bands (
            band_name  VARCHAR,
            min_salary DECIMAL(10,2),
            max_salary DECIMAL(10,2)
        );
    """)

    con.execute("""
        INSERT INTO salary_bands
        VALUES
            ('Junior', 0.00, 65000.00),
            ('Mid-Level', 65000.01, 85000.00),
            ('Senior', 85000.01, 105000.00),
            ('Principal', 105000.01, 999999.00);
    """)

    # NL: Assign each employee to a salary band.
    # SQL: Non-equi JOIN using BETWEEN

    con.execute("""
        SELECT
            e.emp_name,
            e.salary,
            sb.band_name,
            d.dept_name
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        JOIN salary_bands sb ON e.salary BETWEEN sb.min_salary
        AND sb.max_salary
        ORDER BY sb.min_salary DESC, e.salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 47. NATURAL JOIN — Automatic Column Matching

    ### NL Query
    > *"Join employees and departments without specifying the join column — let SQL figure it out."*

    ### SQL Concept
    `NATURAL JOIN` automatically matches columns **with the same name** in both tables. Here, both tables have `dept_id`, so DuckDB joins on that column automatically.

    ### Warning
    NATURAL JOIN is **fragile** — if someone adds a column with the same name to both tables (e.g., `name`), the join condition silently changes. **Avoid in production code**; prefer explicit `ON` clauses.
    """)
    return


@app.cell
def _(con):
    # NL: Join employees and departments automatically.
    # SQL: SELECT ... FROM employees NATURAL JOIN departments

    con.execute("""
        SELECT
            dept_id,
            emp_name,
            dept_name,
            salary
        FROM employees
        NATURAL
        JOIN departments
        ORDER BY dept_id, emp_name
        LIMIT 8;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 48. JOIN with USING Clause

    ### NL Query
    > *"Join employees and departments on dept_id using the USING shorthand."*

    ### SQL Concept
    `USING(column)` is a shorthand when the join column has the **same name** in both tables:
    - `ON e.dept_id = d.dept_id` → `USING(dept_id)`
    - The `dept_id` column appears **once** in the result (not duplicated)
    - Safer than NATURAL JOIN because you explicitly name the column
    """)
    return


@app.cell
def _(con):
    # NL: Join using USING clause.
    # SQL: SELECT ... FROM employees JOIN departments USING(dept_id)

    con.execute("""
        SELECT
            dept_id,
            emp_name,
            dept_name,
            salary,
            location
        FROM employees
        JOIN departments USING(dept_id)
        ORDER BY dept_name, salary DESC
        LIMIT 8;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 49. LATERAL JOIN — Correlated Subquery as a JOIN

    ### NL Query
    > *"For each department, show the top 2 highest-paid employees."*

    ### SQL Concept
    A `LATERAL JOIN` allows the right-side subquery to **reference columns from the left side** — like a correlated subquery but used in the FROM clause. DuckDB supports this via `LATERAL` or the comma-separated syntax with `LATERAL`.

    Alternative approach: use `QUALIFY` with window functions.
    """)
    return


@app.cell
def _(con):
    # NL: Top 2 highest-paid employees per department.
    # SQL: Using QUALIFY (DuckDB-native, cleaner than LATERAL for this case)

    con.execute("""
        SELECT
            d.dept_name,
            e.emp_name,
            e.salary,
            ROW_NUMBER() OVER (PARTITION BY d.dept_name
        ORDER BY e.salary DESC) AS RANK
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id QUALIFY ROW_NUMBER() OVER (PARTITION BY d.dept_name
        ORDER BY e.salary DESC) <= 2
        ORDER BY d.dept_name, e.salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 50. Grand Finale — Complete HR Analytics Report

    ### NL Query
    > *"Build a comprehensive report that combines ALL join techniques: show every employee with their department, their rank within the department, their manager's name, any projects they lead, their salary band, and whether they're above or below the department average. Include unassigned employees."*

    This query combines:
    - **LEFT JOIN** (keep all employees)
    - **Self-JOIN** (manager lookup)
    - **Non-Equi JOIN** (salary bands)
    - **CTE** (department stats)
    - **Window Function** (rank within department)
    - **CASE** (conditional logic)
    - **COALESCE** (NULL handling)
    """)
    return


@app.cell
def _(con):
    # NL: Complete HR Analytics report combining ALL join techniques.

    con.execute("""
        WITH dept_stats AS (
        SELECT
            dept_id,
            ROUND(AVG(salary), 2) AS dept_avg_salary,
            COUNT(*) AS dept_size
        FROM employees
        WHERE dept_id IN (
        SELECT dept_id
        FROM departments)
        GROUP BY dept_id )
        SELECT
            e.emp_id,
            e.emp_name,
            /* Department info (LEFT JOIN) */ COALESCE(d.dept_name, 'Unassigned') AS department,
            /* Salary and band (Non-Equi JOIN) */ e.salary,
            COALESCE(sb.band_name, 'Unclassified') AS salary_band,
            /* Manager (Self-JOIN) */ COALESCE(m.emp_name, 'None') AS manager,
            /* Project led (LEFT JOIN) */ COALESCE(p.project_name, 'None') AS project_led,
            /* Department rank (Window Function) */ CASE WHEN d.dept_id IS NOT NULL THEN ROW_NUMBER() OVER (PARTITION BY d.dept_name
        ORDER BY e.salary DESC) ELSE NULL END AS dept_rank, /* Above/below dept avg (CTE JOIN) */ CASE WHEN ds.dept_avg_salary IS NULL THEN 'N/A' WHEN e.salary >= ds.dept_avg_salary THEN 'Above Avg' ELSE 'Below Avg' END AS vs_dept_avg
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        LEFT
        JOIN employees m ON e.manager_id = m.emp_id
        LEFT
        JOIN projects p ON e.emp_id = p.lead_emp_id
        LEFT
        JOIN salary_bands sb ON e.salary BETWEEN sb.min_salary
        AND sb.max_salary
        LEFT
        JOIN dept_stats ds ON e.dept_id = ds.dept_id
        ORDER BY CASE WHEN d.dept_name IS NULL THEN 'ZZZZ' ELSE d.dept_name END, e.salary DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Appendix — JOIN Type Summary & Cheat Sheet
    ---

    ## Visual Summary of All JOIN Types

    ```
    Given:  employees (20 rows)    departments (5 rows)
            14 match               3 match
            6 don't match          2 don't match
    ```

    ```
    ┌────────────────────┬────────────┬───────────────┬─────────────────┬───────┐
    │ JOIN Type          │ Matched    │ Unmatched     │ Unmatched       │ Total │
    │                    │ (both)     │ (left only)   │ (right only)    │ Rows  │
    ├────────────────────┼────────────┼───────────────┼─────────────────┼───────┤
    │ INNER JOIN         │ ✅ 14      │ ❌ excluded   │ ❌ excluded     │  14   │
    │ LEFT JOIN          │ ✅ 14      │ ✅ 6 (R=NULL) │ ❌ excluded     │  20   │
    │ RIGHT JOIN         │ ✅ 14      │ ❌ excluded   │ ✅ 2 (L=NULL)   │  16   │
    │ FULL OUTER JOIN    │ ✅ 14      │ ✅ 6 (R=NULL) │ ✅ 2 (L=NULL)   │  22   │
    │ CROSS JOIN         │ Every row paired with every row              │ 100   │
    └────────────────────┴────────────┴───────────────┴─────────────────┴───────┘
    ```

    ## JOIN Syntax Quick Reference

    ```sql
    -- INNER JOIN: only matches
    SELECT * FROM A INNER JOIN B ON A.key = B.key

    -- LEFT JOIN: all from A + matches from B
    SELECT * FROM A LEFT JOIN B ON A.key = B.key

    -- RIGHT JOIN: all from B + matches from A
    SELECT * FROM A RIGHT JOIN B ON A.key = B.key

    -- FULL OUTER: all from both
    SELECT * FROM A FULL OUTER JOIN B ON A.key = B.key

    -- CROSS JOIN: cartesian product (no ON clause)
    SELECT * FROM A CROSS JOIN B

    -- SELF JOIN: table joined to itself
    SELECT * FROM A a1 JOIN A a2 ON a1.col = a2.col AND a1.id < a2.id

    -- USING shorthand (when column names match)
    SELECT * FROM A JOIN B USING(key)

    -- NATURAL JOIN (auto-match same-named columns — avoid in production)
    SELECT * FROM A NATURAL JOIN B
    ```

    ## Anti-JOIN & Semi-JOIN Patterns

    ```sql
    -- Anti-JOIN: rows in A with NO match in B
    SELECT a.* FROM A a LEFT JOIN B b ON a.key = b.key WHERE b.key IS NULL

    -- Semi-JOIN: rows in A that HAVE a match in B
    SELECT a.* FROM A a WHERE EXISTS (SELECT 1 FROM B b WHERE b.key = a.key)
    ```

    ## Common Mistakes to Avoid

    | Mistake | Problem | Fix |
    |---------|---------|-----|
    | `WHERE` on RIGHT table in LEFT JOIN | Converts to INNER JOIN | Move filter to `ON` clause |
    | Missing table alias with self-join | Ambiguous column error | Always use aliases (e1, e2) |
    | CROSS JOIN on large tables | Millions/billions of rows | Only use with small tables |
    | NATURAL JOIN in production | Fragile — breaks on schema changes | Use explicit `ON` |
    | Forgetting `a.id < b.id` in self-join | Duplicate + self-matching pairs | Always add inequality |

    ## Execution Order with JOINs

    ```
    1. FROM + JOIN    ← tables combined here
    2. ON             ← join condition applied
    3. WHERE          ← row-level filter (after join)
    4. GROUP BY       ← group rows
    5. HAVING         ← filter groups
    6. SELECT         ← choose columns
    7. Window Fns     ← compute over partitions
    8. QUALIFY        ← filter window results (DuckDB)
    9. DISTINCT       ← remove duplicates
    10. ORDER BY      ← sort
    11. LIMIT/OFFSET  ← paginate
    ```

    ---

    *Tutorial by Dr. Mahmoud Parsian — OMIS 105, Santa Clara University*
    *Built with DuckDB and Jupyter Notebooks*
    *Focus: SQL JOIN Operations — the most important SQL skill*
    """)
    return


@app.cell
def _(con):
    # Clean up
    con.close()
    print("Tutorial complete!")
    print("Tables used: employees (20 rows), departments (5 rows),")
    print("             projects (8 rows), salary_bands (4 rows)")
    print("Topics covered: 50 sections across 10 parts")
    print("JOIN types: INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF,")
    print("            NATURAL, USING, Anti-JOIN, Semi-JOIN, Non-Equi, LATERAL/QUALIFY")
    return


if __name__ == "__main__":
    app.run()
