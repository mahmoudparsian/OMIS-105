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
    # OMIS 105 — SQL Intermediate (Weeks 4–6)
    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### What This Notebook Covers

    | Week | Topics | Lectures |
    |------|--------|----------|
    | 4 | Window functions, CASE, ROLLUP/CUBE, CTEs | Lectures 7–8 |
    | 5 | FULL OUTER JOIN, CROSS JOIN, SELF JOIN, Set Operations, Anti-Joins | Lectures 9–10 |
    | 6 | Normalization (1NF/2NF/3NF), Constraints, Views, UPDATE/DELETE | Lectures 11–12 |

    ### Prerequisites (Weeks 1–3)

    You should already know: SELECT, FROM, WHERE, ORDER BY, LIMIT, DISTINCT, GROUP BY, HAVING, basic INNER JOIN and LEFT JOIN, PRIMARY KEY, FOREIGN KEY, and simple subqueries.

    ### Our Dataset

    A mid-size tech company with **30 employees** across **5 departments**, plus **8 projects** and an **assignments** bridge table. Loaded from `company_data.csv`.

    ### How to Use

    Run each cell in order. The plotting helper `plot_helpers.py` from Weeks 1–3 is reused.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Setup — Build the Company Database
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=":memory:")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load and Normalize the CSV

    The CSV is a flat file with department info embedded in every employee row.
    We'll normalize it into proper tables — just like you learned in Week 2.
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE raw_data AS
            SELECT * FROM read_csv_auto('company_data.csv')
        """
    )
    return


@app.cell
def _(mo, raw_data):
    _df = mo.sql(
        f"""
        SELECT 'company_data.csv loaded!' AS status,
               COUNT(*) AS total_rows
        FROM raw_data
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE departments (
            dept_id       INTEGER PRIMARY KEY,
            dept_name     VARCHAR NOT NULL,
            dept_location VARCHAR NOT NULL,
            budget        DECIMAL(12,2) NOT NULL
        )
        """
    )
    return


@app.cell
def _(departments, mo):
    _df = mo.sql(
        f"""
        INSERT INTO departments VALUES
            (10, 'Engineering',  'San Jose',      2000000),
            (20, 'Marketing',    'San Francisco', 1200000),
            (30, 'Sales',        'Santa Clara',   1500000),
            (40, 'Finance',      'Palo Alto',     1000000),
            (50, 'HR',           'San Jose',       800000),
            (60, 'Legal',        'San Francisco',  600000)
        """
    )
    return


@app.cell
def _(departments, mo):
    _df = mo.sql(
        f"""
        -- departments: 6 rows (note: Legal has NO employees)
        SELECT * FROM departments ORDER BY dept_id
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR NOT NULL,
            gender     VARCHAR NOT NULL,
            dept_id    INTEGER,
            salary     DECIMAL(10,2) NOT NULL,
            hire_date  DATE NOT NULL,
            manager_id INTEGER
        )
        """
    )
    return


@app.cell
def _(employees, mo, raw_data):
    _df = mo.sql(
        f"""
        INSERT INTO employees
        SELECT emp_id, emp_name, gender, dept_id, salary, hire_date, manager_id
        FROM   raw_data
        ORDER BY emp_id
        """
    )
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        -- employees: 30 rows (3 have NULL dept_id — unassigned)
        SELECT * FROM employees ORDER BY emp_id LIMIT 10
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE projects (
            project_id   INTEGER PRIMARY KEY,
            project_name VARCHAR NOT NULL,
            budget       DECIMAL(12,2) NOT NULL,
            status       VARCHAR NOT NULL,
            start_date   DATE NOT NULL
        )
        """
    )
    return


@app.cell
def _(mo, projects):
    _df = mo.sql(
        f"""
        INSERT INTO projects VALUES
            (101, 'Cloud Migration',   500000, 'Active',    '2024-01-15'),
            (102, 'Mobile App v2',     300000, 'Active',    '2024-03-01'),
            (103, 'Data Warehouse',    450000, 'Active',    '2024-06-10'),
            (104, 'Brand Refresh',     200000, 'Completed', '2023-09-01'),
            (105, 'CRM Upgrade',       350000, 'Active',    '2024-04-20'),
            (106, 'Security Audit',    150000, 'Completed', '2023-11-15'),
            (107, 'AI Chatbot',        400000, 'Planning',  '2025-01-01'),
            (108, 'Office Relocation', 250000, 'Planning',  '2025-03-01')
        """
    )
    return


@app.cell
def _(mo, projects):
    _df = mo.sql(
        f"""
        -- projects: 8 rows
        SELECT * FROM projects ORDER BY project_id
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE assignments (
            assignment_id INTEGER PRIMARY KEY,
            emp_id        INTEGER,
            project_id    INTEGER,
            role          VARCHAR NOT NULL,
            hours_per_week INTEGER NOT NULL
        )
        """
    )
    return


@app.cell
def _(assignments, mo):
    _df = mo.sql(
        f"""
        INSERT INTO assignments VALUES
            (1,  1,  101, 'Lead',       20),
            (2,  2,  101, 'Developer',  30),
            (3,  3,  102, 'Lead',       25),
            (4,  4,  101, 'Developer',  35),
            (5,  5,  102, 'Developer',  30),
            (6,  6,  103, 'Developer',  40),
            (7,  7,  104, 'Lead',       15),
            (8,  8,  105, 'Analyst',    20),
            (9,  9,  104, 'Analyst',    25),
            (10, 10, 105, 'Analyst',    30),
            (11, 12, 105, 'Lead',       20),
            (12, 13, 105, 'Sales Rep',  25),
            (13, 14, 106, 'Auditor',    35),
            (14, 18, 106, 'Lead',       15),
            (15, 19, 103, 'Analyst',    20),
            (16, 20, 103, 'Analyst',    25),
            (17, 29, 101, 'Developer',  30),
            (18, 29, 102, 'Developer',  15),
            (19, 1,  107, 'Lead',       10),
            (20, 3,  107, 'Developer',  15),
            (21, 18, 103, 'Analyst',    10),
            (22, 7,  108, 'Lead',       10),
            (23, 23, 108, 'Coordinator',20),
            (24, 12, 106, 'Auditor',    10),
            (25, 30, 104, 'Analyst',    20)
        """
    )
    return


@app.cell
def _(assignments, mo):
    _df = mo.sql(
        f"""
        -- assignments: 25 rows
        SELECT * FROM assignments ORDER BY assignment_id LIMIT 10
        """
    )
    return


@app.cell
def _(mo, raw_data):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS raw_data
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ---
    # WEEK 4 — Advanced Aggregation

    ---

    ## 4.1 — Window Functions: Analytics Without Collapsing Rows

    **The problem:** GROUP BY collapses rows — you get one row per group.
    But what if you want each employee's row AND their department average?

    **Window functions** compute a value across a set of rows ("window")
    without collapsing anything. Every original row is preserved.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Aggregate Window Functions with OVER()
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        -- Each employee + their department average + difference from average
        SELECT emp_name,
               d.dept_name,
               salary,
               ROUND(AVG(salary) OVER (PARTITION BY e.dept_id), 0) AS dept_avg,
               ROUND(salary - AVG(salary) OVER (PARTITION BY e.dept_id), 0) AS diff_from_avg
        FROM   employees e
        JOIN   departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name, salary DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice: **30 rows in, 27 rows out** (3 unassigned employees excluded by JOIN).
    Every row still has the individual employee — but now also has the department average.

    `PARTITION BY e.dept_id` means "compute AVG(salary) separately for each department."
    Without PARTITION BY, it would compute across ALL employees.
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        -- Without PARTITION BY: company-wide average on every row
        SELECT emp_name,
               salary,
               ROUND(AVG(salary) OVER (), 0) AS company_avg,
               ROUND(salary - AVG(salary) OVER (), 0) AS diff_from_company
        FROM   employees
        ORDER BY diff_from_company DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.2 — Ranking Functions: ROW_NUMBER, RANK, DENSE_RANK

    > *"Rank employees by salary within each department."*

    Three ranking functions — the difference is how they handle ties:

    | Function | Ties | Gaps | For 100, 90, 90, 80 |
    |----------|------|------|----------------------|
    | ROW_NUMBER() | Breaks arbitrarily | No | 1, 2, 3, 4 |
    | RANK() | Same rank | Yes | 1, 2, 2, 4 |
    | DENSE_RANK() | Same rank | No | 1, 2, 2, 3 |
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        -- All three ranking functions side by side
        SELECT emp_name,
               d.dept_name,
               salary,
               ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY salary DESC) AS row_num,
               RANK()       OVER (PARTITION BY e.dept_id ORDER BY salary DESC) AS rank,
               DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY salary DESC) AS dense_rank
        FROM   employees e
        JOIN   departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name, salary DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > *"Show only the top earner in each department."*
    >
    > Use ROW_NUMBER + a CTE (we'll learn CTEs fully later, but here's a preview):
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        WITH ranked AS (
            SELECT emp_name,
                   d.dept_name,
                   salary,
                   ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY salary DESC) AS rn
            FROM   employees e
            JOIN   departments d ON e.dept_id = d.dept_id
        )
        SELECT emp_name, dept_name, salary
        FROM   ranked
        WHERE  rn = 1
        ORDER BY salary DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.3 — LAG and LEAD: Looking at Neighboring Rows

    LAG looks at the **previous** row. LEAD looks at the **next** row.

    > *"For each employee (by hire date), show when the previous person was hired
    > and the gap in days between hires."*
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name,
               hire_date,
               LAG(emp_name)   OVER (ORDER BY hire_date) AS prev_hire,
               LAG(hire_date)  OVER (ORDER BY hire_date) AS prev_date,
               hire_date - LAG(hire_date) OVER (ORDER BY hire_date) AS days_gap
        FROM   employees
        ORDER BY hire_date
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > *"Within each department, show the salary difference from the next-highest earner."*
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name,
               d.dept_name,
               salary,
               LEAD(salary) OVER (PARTITION BY e.dept_id ORDER BY salary DESC) AS next_salary,
               salary - LEAD(salary) OVER (PARTITION BY e.dept_id ORDER BY salary DESC) AS gap
        FROM   employees e
        JOIN   departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name, salary DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.4 — Running Totals

    > *"Show a running total of salaries by hire date (cumulative payroll over time)."*
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name,
               hire_date,
               salary,
               SUM(salary) OVER (ORDER BY hire_date
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                   AS running_total
        FROM   employees
        ORDER BY hire_date
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > *"Running total per department."*
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name,
               d.dept_name,
               hire_date,
               salary,
               SUM(salary) OVER (PARTITION BY e.dept_id
                                 ORDER BY hire_date
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                   AS dept_running_total
        FROM   employees e
        JOIN   departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name, hire_date
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.5 — CASE Expressions: SQL's If-Then-Else

    > *"Classify each employee into a salary band."*
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name,
               salary,
               CASE
                   WHEN salary >= 150000 THEN 'Senior'
                   WHEN salary >= 120000 THEN 'Mid-Level'
                   WHEN salary >= 100000 THEN 'Junior'
                   ELSE 'Entry'
               END AS salary_band
        FROM   employees
        ORDER BY salary DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### CASE Inside Aggregates: Conditional Counting

    > *"For each department, count male and female employees."*
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        SELECT d.dept_name,
               COUNT(*) AS total,
               COUNT(CASE WHEN e.gender = 'F' THEN 1 END) AS female,
               COUNT(CASE WHEN e.gender = 'M' THEN 1 END) AS male
        FROM   employees e
        JOIN   departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY d.dept_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### CASE to Classify Projects
    """)
    return


@app.cell
def _(mo, projects):
    _df = mo.sql(
        f"""
        SELECT project_name,
               budget,
               status,
               CASE
                   WHEN budget >= 400000 THEN 'Large'
                   WHEN budget >= 200000 THEN 'Medium'
                   ELSE 'Small'
               END AS budget_tier
        FROM   projects
        ORDER BY budget DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.6 — ROLLUP and CUBE: Subtotals and Grand Totals

    **ROLLUP** adds hierarchical subtotals.
    **CUBE** adds subtotals for ALL combinations.

    > *"Show headcount per department per gender — with subtotals."*
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        -- ROLLUP: subtotals for department, then grand total
        SELECT d.dept_name,
               e.gender,
               COUNT(*)            AS headcount,
               ROUND(AVG(salary),0) AS avg_salary
        FROM   employees e
        JOIN   departments d ON e.dept_id = d.dept_id
        GROUP BY ROLLUP(d.dept_name, e.gender)
        ORDER BY d.dept_name NULLS LAST, e.gender NULLS LAST
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    NULL in dept_name = grand total. NULL in gender = department subtotal.
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        -- CUBE: subtotals for EVERY combination
        SELECT d.dept_name,
               e.gender,
               COUNT(*)            AS headcount,
               ROUND(AVG(salary),0) AS avg_salary
        FROM   employees e
        JOIN   departments d ON e.dept_id = d.dept_id
        GROUP BY CUBE(d.dept_name, e.gender)
        ORDER BY d.dept_name NULLS LAST, e.gender NULLS LAST
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    CUBE adds something ROLLUP doesn't: the gender-only subtotals
    (total across ALL departments for each gender).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.7 — Common Table Expressions (CTEs)

    A CTE is a **named subquery** that makes complex SQL readable.

    > *"Find employees who earn more than their department average."*
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        -- Without CTE — nested and hard to read
        SELECT emp_name, salary, dept_id
        FROM   employees e
        WHERE  salary > (
            SELECT AVG(salary)
            FROM   employees e2
            WHERE  e2.dept_id = e.dept_id
        )
        ORDER BY salary DESC
        """
    )
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        -- With CTE — clear, step-by-step
        WITH dept_avg AS (
            SELECT dept_id,
                   ROUND(AVG(salary), 0) AS avg_salary
            FROM   employees
            WHERE  dept_id IS NOT NULL
            GROUP BY dept_id
        )
        SELECT e.emp_name,
               d.dept_name,
               e.salary,
               da.avg_salary AS dept_avg,
               e.salary - da.avg_salary AS above_avg_by
        FROM   employees e
        JOIN   departments d  ON e.dept_id = d.dept_id
        JOIN   dept_avg    da ON e.dept_id = da.dept_id
        WHERE  e.salary > da.avg_salary
        ORDER BY above_avg_by DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Multiple CTEs Chained Together

    > *"For each department, show the top earner and how much more they earn
    > than the department average."*
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        WITH dept_avg AS (
            SELECT dept_id,
                   ROUND(AVG(salary), 0) AS avg_salary
            FROM   employees
            WHERE  dept_id IS NOT NULL
            GROUP BY dept_id
        ),
        top_earner AS (
            SELECT emp_name, dept_id, salary,
                   ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn
            FROM   employees
            WHERE  dept_id IS NOT NULL
        )
        SELECT t.emp_name,
               d.dept_name,
               t.salary,
               da.avg_salary,
               t.salary - da.avg_salary AS premium
        FROM   top_earner t
        JOIN   departments d  ON t.dept_id  = d.dept_id
        JOIN   dept_avg    da ON t.dept_id  = da.dept_id
        WHERE  t.rn = 1
        ORDER BY t.salary DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Week 4 Summary

    | Concept | What It Does | Key Syntax |
    |---------|-------------|------------|
    | Window Functions | Compute across rows without collapsing | `OVER (PARTITION BY ... ORDER BY ...)` |
    | ROW_NUMBER / RANK / DENSE_RANK | Assign rankings | Differ in tie handling |
    | LAG / LEAD | Access previous / next row | `LAG(col) OVER (ORDER BY ...)` |
    | Running Total | Cumulative sum | `SUM() OVER (ORDER BY ... ROWS ...)` |
    | CASE | If-then-else logic | `CASE WHEN ... THEN ... ELSE ... END` |
    | ROLLUP | Hierarchical subtotals | `GROUP BY ROLLUP(a, b)` |
    | CUBE | All-combination subtotals | `GROUP BY CUBE(a, b)` |
    | CTE | Named subquery for readability | `WITH name AS (SELECT ...) SELECT ...` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ---
    # WEEK 5 — Advanced Joins & Set Operations

    ---

    ## 5.1 — FULL OUTER JOIN: Keep Everything from Both Sides

    INNER JOIN: only matching rows.
    LEFT JOIN: all from left + matching right.
    **FULL OUTER JOIN: all from BOTH sides** — NULLs where no match.

    > *"Show ALL employees and ALL departments — even unassigned employees
    > and departments with no employees."*
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        SELECT e.emp_name,
               e.dept_id AS emp_dept_id,
               d.dept_id,
               d.dept_name
        FROM   employees e
        FULL OUTER JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name NULLS LAST, e.emp_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice two types of NULLs:
    - **Zack, Amy, Ben** have `dept_name = NULL` → employees with no department
    - **Legal** has `emp_name = NULL` → department with no employees

    FULL OUTER JOIN is essential for **reconciliation**: finding mismatches between two data sources.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > *"Find the mismatches: unassigned employees AND empty departments."*
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        SELECT COALESCE(e.emp_name, '(no employee)') AS employee,
               COALESCE(d.dept_name, '(no department)') AS department,
               CASE
                   WHEN e.emp_id IS NULL THEN 'Empty department'
                   WHEN d.dept_id IS NULL THEN 'Unassigned employee'
               END AS issue
        FROM   employees e
        FULL OUTER JOIN departments d ON e.dept_id = d.dept_id
        WHERE  e.emp_id IS NULL OR d.dept_id IS NULL
        ORDER BY issue
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5.2 — CROSS JOIN: Every Possible Combination

    CROSS JOIN pairs every row from table A with every row from table B.
    No ON clause — it produces the **Cartesian product**.

    > *"Generate a grid of all department-project combinations for resource planning."*
    """)
    return


@app.cell
def _(departments, mo, projects):
    _df = mo.sql(
        f"""
        -- 6 departments x 4 active projects = 24 rows
        SELECT d.dept_name,
               p.project_name,
               p.status
        FROM   departments d
        CROSS JOIN projects p
        WHERE  p.status = 'Active'
        ORDER BY d.dept_name, p.project_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Warning:** CROSS JOIN on large tables produces enormous results.
    100 rows × 100 rows = 10,000 rows. 10,000 × 10,000 = 100 million rows.
    Always use intentionally, often with a WHERE to limit the output.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5.3 — SELF JOIN: Joining a Table to Itself

    The `manager_id` column in employees points to another `emp_id` in the SAME table.
    To see the manager's name, we join employees to itself.

    > *"Show each employee and their manager's name."*
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        SELECT e.emp_name   AS employee,
               e.salary     AS emp_salary,
               m.emp_name   AS manager,
               m.salary     AS mgr_salary
        FROM   employees e
        LEFT JOIN employees m ON e.manager_id = m.emp_id
        ORDER BY e.emp_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use LEFT JOIN (not INNER) so that employees with no manager
    (manager_id IS NULL — the department heads) still appear.

    > *"Which employees earn more than their manager?"*
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        SELECT e.emp_name  AS employee,
               e.salary    AS emp_salary,
               m.emp_name  AS manager,
               m.salary    AS mgr_salary,
               e.salary - m.salary AS earns_more_by
        FROM   employees e
        JOIN   employees m ON e.manager_id = m.emp_id
        WHERE  e.salary > m.salary
        ORDER BY earns_more_by DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > *"Find pairs of employees in the same department (co-workers)."*
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        SELECT e1.emp_name AS employee_1,
               e2.emp_name AS employee_2,
               d.dept_name
        FROM   employees e1
        JOIN   employees e2 ON e1.dept_id = e2.dept_id
                           AND e1.emp_id < e2.emp_id
        JOIN   departments d ON e1.dept_id = d.dept_id
        ORDER BY d.dept_name, e1.emp_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The trick: `e1.emp_id < e2.emp_id` ensures each pair appears only once
    (Alice-Bob, not also Bob-Alice).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5.4 — Set Operations: UNION, INTERSECT, EXCEPT

    These combine the **results** of two queries (not the tables).
    Rule: both queries must return the same number of columns with compatible types.

    Let's create two helper tables to demonstrate:
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        -- Employees eligible for a bonus (salary > 120K)
        CREATE OR REPLACE TABLE bonus_eligible AS
        SELECT emp_id, emp_name FROM employees WHERE salary > 120000
        """
    )
    return


@app.cell
def _(assignments, employees, mo, projects):
    _df = mo.sql(
        f"""
        -- Employees on active projects
        CREATE OR REPLACE TABLE on_active_project AS
        SELECT DISTINCT e.emp_id, e.emp_name
        FROM   employees e
        JOIN   assignments a ON e.emp_id = a.emp_id
        JOIN   projects p    ON a.project_id = p.project_id
        WHERE  p.status = 'Active'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### UNION — Combine both lists (remove duplicates)

    > *"Employees who are bonus-eligible OR on an active project (or both)."*
    """)
    return


@app.cell
def _(bonus_eligible, mo, on_active_project):
    _df = mo.sql(
        f"""
        SELECT emp_name FROM bonus_eligible
        UNION
        SELECT emp_name FROM on_active_project
        ORDER BY emp_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### INTERSECT — Only those in BOTH lists

    > *"Employees who are bonus-eligible AND on an active project."*
    """)
    return


@app.cell
def _(bonus_eligible, mo, on_active_project):
    _df = mo.sql(
        f"""
        SELECT emp_name FROM bonus_eligible
        INTERSECT
        SELECT emp_name FROM on_active_project
        ORDER BY emp_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### EXCEPT — In the first list but NOT the second

    > *"Bonus-eligible employees who are NOT on any active project."*
    """)
    return


@app.cell
def _(bonus_eligible, mo, on_active_project):
    _df = mo.sql(
        f"""
        SELECT emp_name FROM bonus_eligible
        EXCEPT
        SELECT emp_name FROM on_active_project
        ORDER BY emp_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### UNION ALL — Keep duplicates (faster)

    Use UNION ALL when you know there are no duplicates or want to preserve them:
    """)
    return


@app.cell
def _(bonus_eligible, mo, on_active_project):
    _df = mo.sql(
        f"""
        SELECT emp_name, 'Bonus Eligible' AS source FROM bonus_eligible
        UNION ALL
        SELECT emp_name, 'Active Project' AS source FROM on_active_project
        ORDER BY emp_name, source
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5.5 — Anti-Joins: Finding What's Missing

    Three patterns that all answer: *"Which employees are NOT assigned to any project?"*

    ### Pattern 1: LEFT JOIN + IS NULL
    """)
    return


@app.cell
def _(assignments, employees, mo):
    _df = mo.sql(
        f"""
        SELECT e.emp_name, e.salary
        FROM   employees e
        LEFT JOIN assignments a ON e.emp_id = a.emp_id
        WHERE  a.assignment_id IS NULL
        ORDER BY e.emp_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Pattern 2: NOT EXISTS
    """)
    return


@app.cell
def _(assignments, employees, mo):
    _df = mo.sql(
        f"""
        SELECT e.emp_name, e.salary
        FROM   employees e
        WHERE  NOT EXISTS (
            SELECT 1
            FROM   assignments a
            WHERE  a.emp_id = e.emp_id
        )
        ORDER BY e.emp_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Pattern 3: NOT IN
    """)
    return


@app.cell
def _(assignments, employees, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name, salary
        FROM   employees
        WHERE  emp_id NOT IN (SELECT emp_id FROM assignments)
        ORDER BY emp_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All three produce the same result. Which to use?

    | Pattern | Pros | Cons |
    |---------|------|------|
    | LEFT JOIN + IS NULL | Visual, easy to understand | More verbose |
    | NOT EXISTS | Robust, handles NULLs correctly | Slightly harder to read |
    | NOT IN | Simplest syntax | **Breaks if subquery returns NULLs** |

    > **Warning:** If the subquery in NOT IN can return NULL, the entire
    > NOT IN returns no rows. Use NOT EXISTS to be safe.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > *"Which projects have NO employees assigned?"*
    """)
    return


@app.cell
def _(assignments, mo, projects):
    _df = mo.sql(
        f"""
        SELECT p.project_name, p.status
        FROM   projects p
        LEFT JOIN assignments a ON p.project_id = a.project_id
        WHERE  a.assignment_id IS NULL
        ORDER BY p.project_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Week 5 Summary — Complete JOIN Reference

    | Join Type | Returns | Use Case |
    |-----------|---------|----------|
    | INNER JOIN | Only matching rows | Standard lookups |
    | LEFT JOIN | All left + matching right | Keep everyone, NULLs for no match |
    | RIGHT JOIN | All right + matching left | Same as LEFT, tables swapped |
    | FULL OUTER JOIN | All from both sides | Reconciliation, finding mismatches |
    | CROSS JOIN | Every combination (Cartesian) | Grids, planning, test data |
    | SELF JOIN | Table joined to itself | Hierarchies, within-table comparisons |

    | Set Operation | Returns | SQL |
    |---------------|---------|-----|
    | UNION | Combined, no duplicates | `A UNION B` |
    | UNION ALL | Combined, with duplicates | `A UNION ALL B` |
    | INTERSECT | Only in both | `A INTERSECT B` |
    | EXCEPT | In A but not B | `A EXCEPT B` |

    | Anti-Join Pattern | Best When |
    |-------------------|-----------|
    | LEFT JOIN + IS NULL | You want to see columns from both tables |
    | NOT EXISTS | Safest — handles NULLs correctly |
    | NOT IN | Quick and simple, if no NULLs |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ---
    # WEEK 6 — Database Design

    ---

    ## 6.1 — Normalization: The Formal Rules

    In Week 2, we split a flat CSV into multiple tables to remove redundancy.
    That was **normalization by intuition**. Now we formalize it.

    ### Functional Dependencies

    A **functional dependency** means one column uniquely determines another:

    ```
    emp_id → emp_name        (knowing emp_id gives you exactly one emp_name)
    dept_id → dept_name      (knowing dept_id gives you exactly one dept_name)
    (emp_id, project_id) → hours_per_week   (the pair determines the hours)
    ```

    This is the foundation of normalization.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### First Normal Form (1NF)

    **Rule:** Every cell holds a single atomic value. No lists, no arrays, no repeating groups.

    Here's a table that **violates 1NF**:
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- BAD: skills column holds multiple values in one cell
        CREATE OR REPLACE TABLE bad_1nf (
            emp_id   INTEGER,
            emp_name VARCHAR,
            skills   VARCHAR
        )
        """
    )
    return


@app.cell
def _(bad_1nf, mo):
    _df = mo.sql(
        f"""
        INSERT INTO bad_1nf VALUES
            (1, 'Alice', 'Python, SQL, Java'),
            (2, 'Bob',   'SQL, Excel'),
            (3, 'Carol', 'Python, R, SQL, Tableau')
        """
    )
    return


@app.cell
def _(bad_1nf, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM bad_1nf
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Problem:** You can't easily query "find everyone who knows SQL" because
    skills are buried inside a comma-separated string.

    **Fix:** One row per skill (or better: a separate skills table with a bridge).
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- GOOD: 1NF — one skill per row
        CREATE OR REPLACE TABLE good_1nf (
            emp_id   INTEGER,
            emp_name VARCHAR,
            skill    VARCHAR
        )
        """
    )
    return


@app.cell
def _(good_1nf, mo):
    _df = mo.sql(
        f"""
        INSERT INTO good_1nf VALUES
            (1, 'Alice', 'Python'), (1, 'Alice', 'SQL'), (1, 'Alice', 'Java'),
            (2, 'Bob',   'SQL'),    (2, 'Bob',   'Excel'),
            (3, 'Carol', 'Python'), (3, 'Carol', 'R'),
            (3, 'Carol', 'SQL'),    (3, 'Carol', 'Tableau')
        """
    )
    return


@app.cell
def _(good_1nf, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM good_1nf ORDER BY emp_id, skill
        """
    )
    return


@app.cell
def _(good_1nf, mo):
    _df = mo.sql(
        f"""
        -- Now we CAN query: "Who knows SQL?"
        SELECT DISTINCT emp_name
        FROM   good_1nf
        WHERE  skill = 'SQL'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Second Normal Form (2NF)

    **Rule:** 1NF + every non-key column depends on the **entire** primary key
    (not just part of it).

    Only matters when the primary key has **multiple columns**.

    Here's a table that **violates 2NF**:
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- BAD: product_name depends only on product_id, not on (order_id, product_id)
        CREATE OR REPLACE TABLE bad_2nf (
            order_id      INTEGER,
            product_id    INTEGER,
            quantity      INTEGER,
            product_name  VARCHAR,
            product_price DECIMAL(10,2),
            PRIMARY KEY (order_id, product_id)
        )
        """
    )
    return


@app.cell
def _(bad_2nf, mo):
    _df = mo.sql(
        f"""
        INSERT INTO bad_2nf VALUES
            (1, 100, 2, 'Laptop', 999.99),
            (1, 200, 1, 'Mouse',   29.99),
            (2, 100, 1, 'Laptop', 999.99),
            (3, 200, 3, 'Mouse',   29.99)
        """
    )
    return


@app.cell
def _(bad_2nf, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM bad_2nf
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Problem:** `product_name` and `product_price` depend only on `product_id`,
    not on the full key `(order_id, product_id)`. That's a **partial dependency**.
    Result: "Laptop" and 999.99 are stored 2 times.

    **Fix:** Move product info to its own table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **GOOD: 2NF — separate tables**

    Products (stored ONCE):
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE products_2nf (
            product_id    INTEGER PRIMARY KEY,
            product_name  VARCHAR,
            product_price DECIMAL(10,2)
        )
        """
    )
    return


@app.cell
def _(mo, products_2nf):
    _df = mo.sql(
        f"""
        INSERT INTO products_2nf VALUES
            (100, 'Laptop', 999.99),
            (200, 'Mouse', 29.99)
        """
    )
    return


@app.cell
def _(mo, products_2nf):
    _df = mo.sql(
        f"""
        SELECT * FROM products_2nf
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Orders (IDs only, no redundancy):
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE orders_2nf (
            order_id   INTEGER,
            product_id INTEGER,
            quantity   INTEGER,
            PRIMARY KEY (order_id, product_id)
        )
        """
    )
    return


@app.cell
def _(mo, orders_2nf):
    _df = mo.sql(
        f"""
        INSERT INTO orders_2nf VALUES
            (1, 100, 2), (1, 200, 1), (2, 100, 1), (3, 200, 3)
        """
    )
    return


@app.cell
def _(mo, orders_2nf):
    _df = mo.sql(
        f"""
        SELECT * FROM orders_2nf
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Third Normal Form (3NF)

    **Rule:** 2NF + no non-key column depends on another non-key column
    (no **transitive dependencies**).

    Here's a table that **violates 3NF**:
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- BAD: dept_name depends on dept_id, not directly on emp_id
        CREATE OR REPLACE TABLE bad_3nf (
            emp_id    INTEGER PRIMARY KEY,
            emp_name  VARCHAR,
            dept_id   INTEGER,
            dept_name VARCHAR,
            dept_loc  VARCHAR
        )
        """
    )
    return


@app.cell
def _(bad_3nf, mo):
    _df = mo.sql(
        f"""
        INSERT INTO bad_3nf VALUES
            (1, 'Alice', 10, 'Engineering', 'San Jose'),
            (2, 'Bob',   10, 'Engineering', 'San Jose'),
            (3, 'Carol', 20, 'Marketing',   'San Francisco'),
            (4, 'David', 20, 'Marketing',   'San Francisco')
        """
    )
    return


@app.cell
def _(bad_3nf, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM bad_3nf
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Problem:** `dept_name` and `dept_loc` depend on `dept_id`, not on `emp_id`.
    That's a **transitive dependency**: `emp_id → dept_id → dept_name`.
    Result: "Engineering, San Jose" stored twice.

    **Fix:** This is exactly what our `employees` + `departments` tables already do!
    The `employees` table stores only `dept_id`, and the department details live in `departments`.

    ### Normalization Summary

    | Normal Form | Rule | Fixes |
    |-------------|------|-------|
    | **1NF** | Atomic values, no lists | Split multi-value cells into rows |
    | **2NF** | No partial dependencies | Move columns that depend on part of the key |
    | **3NF** | No transitive dependencies | Move columns that depend on non-key columns |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6.2 — Constraints: The Database Enforces Your Rules

    Constraints prevent bad data from entering the database.
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Demo table with ALL constraint types
        CREATE OR REPLACE TABLE employees_strict (
            emp_id   INTEGER PRIMARY KEY,
            emp_name VARCHAR NOT NULL,
            email    VARCHAR UNIQUE,
            dept_id  INTEGER REFERENCES departments(dept_id),
            salary   DECIMAL(10,2) CHECK (salary > 0),
            status   VARCHAR DEFAULT 'Active'
        )
        """
    )
    return


@app.cell
def _(employees_strict, mo):
    _df = mo.sql(
        f"""
        -- Good insert — all constraints satisfied
        INSERT INTO employees_strict (emp_id, emp_name, email, dept_id, salary)
        VALUES (1, 'Test User', 'test@company.com', 10, 100000)
        """
    )
    return


@app.cell
def _(employees_strict, mo):
    _df = mo.sql(
        f"""
        -- Notice: status is 'Active' even though we didn't provide it — that's the DEFAULT
        SELECT * FROM employees_strict
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's see what happens when we **violate** each constraint:
    """)
    return


@app.cell
def _(employees_strict, mo):
    # Violate NOT NULL — the database rejects the insert
    try:
        mo.sql(f"""
            INSERT INTO employees_strict (emp_id, email) VALUES (2, 'x@y.com')
        """)
    except Exception as e:
        print(f"NOT NULL violation: {e}")
    return


@app.cell
def _(employees_strict, mo):
    # Violate UNIQUE — duplicate email rejected
    try:
        mo.sql(f"""
            INSERT INTO employees_strict (emp_id, emp_name, email, salary)
            VALUES (3, 'Another', 'test@company.com', 90000)
        """)
    except Exception as e:
        print(f"UNIQUE violation: {e}")
    return


@app.cell
def _(employees_strict, mo):
    # Violate CHECK — negative salary rejected
    try:
        mo.sql(f"""
            INSERT INTO employees_strict (emp_id, emp_name, email, salary)
            VALUES (4, 'Negative', 'neg@co.com', -5000)
        """)
    except Exception as e:
        print(f"CHECK violation: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The database itself rejects bad data. You don't need application code to validate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6.3 — Views: A Saved Query That Acts Like a Table

    A view is a **virtual table** — it stores a query, not data.
    """)
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE VIEW dept_summary AS
        SELECT d.dept_name,
               COUNT(e.emp_id)         AS headcount,
               ROUND(AVG(e.salary), 0) AS avg_salary,
               MIN(e.salary)           AS min_salary,
               MAX(e.salary)           AS max_salary
        FROM   departments d
        LEFT JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
        """
    )
    return


@app.cell
def _(dept_summary, mo):
    _df = mo.sql(
        f"""
        -- Use it like a regular table
        SELECT * FROM dept_summary ORDER BY avg_salary DESC
        """
    )
    return


@app.cell
def _(departments, employees, mo):
    _df = mo.sql(
        f"""
        -- A view that hides salary info (for non-HR users)
        CREATE OR REPLACE VIEW employee_directory AS
        SELECT e.emp_name,
               e.gender,
               d.dept_name,
               e.hire_date
        FROM   employees e
        LEFT JOIN departments d ON e.dept_id = d.dept_id
        """
    )
    return


@app.cell
def _(employee_directory, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM employee_directory ORDER BY emp_name LIMIT 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Why Views?

    | Use Case | Example |
    |----------|---------|
    | **Simplification** | Complex JOIN hidden behind a simple view name |
    | **Security** | Hide salary column from non-HR users |
    | **Reusability** | Define once, query many times |
    | **Consistency** | Everyone uses the same definition |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6.4 — UPDATE and DELETE: Modifying Data

    Until now, we've only queried data. Now we change it.

    **Golden rule:** Always test your WHERE clause with SELECT first,
    then change SELECT to UPDATE or DELETE.

    ### UPDATE
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **BEFORE** — current Engineering salaries:
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name, salary
        FROM   employees
        WHERE  dept_id = 10
        ORDER BY emp_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Give Engineering a **10% raise**:
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        UPDATE employees
        SET    salary = ROUND(salary * 1.10, 2)
        WHERE  dept_id = 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **AFTER** — Engineering salaries (10% raise applied):
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name, salary
        FROM   employees
        WHERE  dept_id = 10
        ORDER BY emp_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### UPDATE with CASE — conditional updates
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        -- Tiered raises: 8% under 100K, 5% under 130K, 3% above
        UPDATE employees
        SET salary = ROUND(
            CASE
                WHEN salary < 100000  THEN salary * 1.08
                WHEN salary < 130000  THEN salary * 1.05
                ELSE salary * 1.03
            END, 2)
        WHERE dept_id = 30
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **AFTER** — Sales team salaries (tiered raises applied):
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name, salary
        FROM   employees
        WHERE  dept_id = 30
        ORDER BY salary DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### DELETE

    > **WARNING:** `DELETE` without `WHERE` deletes EVERY row in the table!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Step 1:** SELECT first to verify which rows will be affected:
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        -- These rows will be deleted
        SELECT emp_name, salary, hire_date
        FROM   employees
        WHERE  emp_name = 'Ben'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Step 2:** Now delete (same WHERE clause):
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        DELETE FROM employees
        WHERE  emp_name = 'Ben'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Remaining unassigned employees after deletion:
    """)
    return


@app.cell
def _(employees, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name, salary
        FROM   employees
        WHERE  dept_id IS NULL
        ORDER BY emp_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Best Practice: The SELECT-then-DELETE Pattern

    ```sql
    -- Step 1: VERIFY (run this first)
    SELECT * FROM employees WHERE <your_condition>

    -- Step 2: DELETE (only after Step 1 looks correct)
    DELETE FROM employees WHERE <your_condition>
    ```

    Same pattern works for UPDATE. This prevents accidental mass changes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ---
    # Summary — What You Learned in Weeks 4–6

    | Week | Concepts | Key Takeaway |
    |------|----------|-------------|
    | **4** | Window functions, CASE, ROLLUP/CUBE, CTEs | Analyze data without collapsing rows |
    | **5** | FULL OUTER JOIN, CROSS JOIN, SELF JOIN, Set operations, Anti-joins | Handle every type of table relationship |
    | **6** | Normalization (1NF/2NF/3NF), Constraints, Views, UPDATE/DELETE | Design, protect, and modify databases |

    ### Files in This Folder

    | File | Purpose |
    |------|---------|
    | `company_data.csv` | 30-employee tech company dataset |
    | `plot_helpers.py` | Plotting functions (reused from Weeks 1–3) |
    | `OMIS105_Weeks_4_6_marimo.py` | This notebook |
    | `OMIS105_Weeks_4_6_Lecture_Notes.md` | Detailed lecture notes and discussion guides |

    ### What's Next (Weeks 7–10)

    | Week | Topic |
    |------|-------|
    | 7 | Query Performance & Indexing |
    | 8 | Transactions & ACID |
    | 9 | Project Integration |
    | 10 | Review & Modern Data |

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
