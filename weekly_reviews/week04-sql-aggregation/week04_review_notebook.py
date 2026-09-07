import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from pathlib import Path

    import duckdb

    DATA_DIR = Path(__file__).parent / "data"
    con = duckdb.connect(database=":memory:")
    return DATA_DIR, con


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # OMIS 105 — Week 4 Review: Advanced Aggregation & Window Functions

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    `GROUP BY` collapses rows. Sometimes you need each employee's own row
    **and** their department average side by side. That is what window
    functions do.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | Keep every row | `OVER()`, `PARTITION BY` |
    | Rank within groups | `ROW_NUMBER`, `RANK`, `DENSE_RANK` |
    | Look at neighbors | `LAG`, `LEAD` |
    | Accumulate | Running totals with `ROWS BETWEEN` |
    | If-then-else in SQL | `CASE`, conditional counting |
    | Subtotals | `ROLLUP`, `CUBE` |
    | Readable queries | `WITH ... AS` (CTEs), chained CTEs |

    ### How to Use

    Run the cells from top to bottom. Every database cell takes `con`, the
    DuckDB connection created in the setup cell. Read the markdown between
    queries — it explains the *why*, not just the *how*.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Setup — Build the Company Database

    `company_data.csv` lives in this folder's `data/` directory. We load it into a
    staging table, then split it into `departments`, `employees`, `projects`, and
    `assignments`.

    The data has deliberate imperfections: some employees have a `NULL` department,
    one department has no employees, and `manager_id` points back into the same
    table. Those are the cases that make JOINs interesting.
    """)
    return


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE raw_data AS
            SELECT * FROM read_csv_auto('{DATA_DIR}/company_data.csv')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT 'company_data.csv loaded!' AS status,
               COUNT(*) AS total_rows
        FROM raw_data
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        -- departments: 6 rows (note: Legal has NO employees)
        SELECT * FROM departments ORDER BY dept_id
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        INSERT INTO employees
        SELECT emp_id, emp_name, gender, dept_id, salary, hire_date, manager_id
        FROM   raw_data
        ORDER BY emp_id
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- employees: 30 rows (3 have NULL dept_id — unassigned)
        SELECT * FROM employees ORDER BY emp_id LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        -- projects: 8 rows
        SELECT * FROM projects ORDER BY project_id
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        -- assignments: 25 rows
        SELECT * FROM assignments ORDER BY assignment_id LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        DROP TABLE IF EXISTS raw_data
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
        f"""
        -- Without PARTITION BY: company-wide average on every row
        SELECT emp_name,
               salary,
               ROUND(AVG(salary) OVER (), 0) AS company_avg,
               ROUND(salary - AVG(salary) OVER (), 0) AS diff_from_company
        FROM   employees
        ORDER BY diff_from_company DESC
        """
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
        f"""
        SELECT emp_name,
               hire_date,
               LAG(emp_name)   OVER (ORDER BY hire_date) AS prev_hire,
               LAG(hire_date)  OVER (ORDER BY hire_date) AS prev_date,
               hire_date - LAG(hire_date) OVER (ORDER BY hire_date) AS days_gap
        FROM   employees
        ORDER BY hire_date
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > *"Within each department, show the salary difference from the next-highest earner."*
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > *"Running total per department."*
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### CASE Inside Aggregates: Conditional Counting

    > *"For each department, count male and female employees."*
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### CASE to Classify Projects
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    NULL in dept_name = grand total. NULL in gender = department subtotal.
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
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
    ## Looking Ahead

    Window functions answered "how does this row compare to its group?" Week 5
    answers "how do two *tables* relate?" — including the rows that match nothing.
    """)
    return


if __name__ == "__main__":
    app.run()
