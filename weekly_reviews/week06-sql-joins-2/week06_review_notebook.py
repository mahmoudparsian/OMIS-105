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
    # OMIS 105 — Week 6 Review: Joins II — Joins in Practice

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    Week 5 showed every join type. This week is **practice**: choosing the right
    join, predicting how many rows it returns, and avoiding the three mistakes that
    quietly give wrong answers — a filter in the wrong place, `COUNT(*)` after a
    `LEFT JOIN`, and one `INNER JOIN` in a chain of `LEFT JOIN`s.

    We use the same tech company as Weeks 4–5, so all the energy goes into the joins.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | Same tables, different answers | `INNER`, `LEFT`, `RIGHT`, `FULL OUTER JOIN` row counts |
    | `RIGHT` = `LEFT` turned around | `RIGHT JOIN`, `LEFT JOIN` |
    | Find what is missing | `LEFT JOIN ... WHERE ... IS NULL`, `COALESCE` |
    | The `ON` vs. `WHERE` trap | filters on the optional table |
    | Counting with joins | `COUNT(*)` vs. `COUNT(column)`, `SUM` + `COALESCE` |
    | Chains of joins | 3–4 tables, `LEFT JOIN` all the way |
    | Self-joins at work | employee vs. manager, direct reports |

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
    ---
    ## 6.1 — Same Tables, Four Different Answers

    Before you trust a join, ask: **which rows did it keep?** The company data has
    gaps on both sides:

    - 3 employees (Zack, Amy, Ben) have **no department** (`dept_id` is `NULL`)
    - 1 department (Legal) has **no employees**

    So each join type returns a different number of rows. Predict all four before
    you run the cell. (The query stacks four counts with `UNION ALL` from Week 5.)
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT 'INNER JOIN' AS join_type, COUNT(*) AS row_count
        FROM employees e INNER JOIN departments d ON e.dept_id = d.dept_id
        UNION ALL
        SELECT 'LEFT JOIN', COUNT(*)
        FROM employees e LEFT JOIN departments d ON e.dept_id = d.dept_id
        UNION ALL
        SELECT 'RIGHT JOIN', COUNT(*)
        FROM employees e RIGHT JOIN departments d ON e.dept_id = d.dept_id
        UNION ALL
        SELECT 'FULL OUTER JOIN', COUNT(*)
        FROM employees e FULL OUTER JOIN departments d ON e.dept_id = d.dept_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - **27** = employees with a department
    - **30** = + the 3 employees with no department (`LEFT` keeps every employee)
    - **28** = + Legal (`RIGHT` keeps every department)
    - **31** = + both gaps (`FULL OUTER`)

    ### Which rows did `LEFT JOIN` add?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.emp_name, e.dept_id, d.dept_name
        FROM employees e
        LEFT JOIN departments d ON e.dept_id = d.dept_id
        WHERE d.dept_id IS NULL
        ORDER BY e.emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Which row did `RIGHT JOIN` add?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.emp_name, d.dept_id, d.dept_name
        FROM employees e
        RIGHT JOIN departments d ON e.dept_id = d.dept_id
        WHERE e.emp_id IS NULL
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6.2 — `RIGHT JOIN` Is `LEFT JOIN` Turned Around

    `employees RIGHT JOIN departments` keeps every department. So does
    `departments LEFT JOIN employees`. Most analysts write only `LEFT JOIN`:
    **start from the table you want to keep.**
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT d.dept_name, e.emp_name
        FROM departments d
        LEFT JOIN employees e ON e.dept_id = d.dept_id
        WHERE e.emp_id IS NULL
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6.3 — Finding What Is Missing

    The anti-join recipe: `LEFT JOIN` the table where a partner *should* be, then
    keep rows where the partner's **key** is `NULL`.

    > *"Which employees are not on any project?"* — the staffing manager wants to
    > know who is free.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.emp_id, e.emp_name, e.dept_id
        FROM employees e
        LEFT JOIN assignments a ON e.emp_id = a.emp_id
        WHERE a.assignment_id IS NULL
        ORDER BY e.emp_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **11 employees.** Three of them (Zack, Amy, Ben) also have no department — a
    double gap worth flagging to HR.

    ### `COALESCE` — a friendly label instead of `NULL`

    > *"List everyone hired since 2022, with their department."*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.emp_name,
               COALESCE(d.dept_name, '(no department)') AS department
        FROM employees e
        LEFT JOIN departments d ON e.dept_id = d.dept_id
        WHERE e.hire_date >= DATE '2022-01-01'
        ORDER BY e.hire_date
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6.4 — The `ON` vs. `WHERE` Trap

    > *"Show **every** department, with the people it hired since 2022."*

    ### Wrong: the hire-date filter is in `WHERE`
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT d.dept_name, e.emp_name, e.hire_date
        FROM departments d
        LEFT JOIN employees e ON e.dept_id = d.dept_id
        WHERE e.hire_date >= DATE '2022-01-01'
        ORDER BY d.dept_id, e.hire_date
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Only **4 departments** appear — HR and Legal vanished. `WHERE` runs **after** the
    join; for HR and Legal the employee columns are `NULL` or too old, so `WHERE`
    throws those rows away. The `LEFT JOIN` silently became an `INNER JOIN`.

    ### Right: the filter goes in `ON`
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT d.dept_name, e.emp_name, e.hire_date
        FROM departments d
        LEFT JOIN employees e
            ON e.dept_id = d.dept_id
           AND e.hire_date >= DATE '2022-01-01'
        ORDER BY d.dept_id, e.hire_date
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All **6** departments are kept. HR and Legal show `NULL`: they hired nobody since 2022.

    | Filter on… | Put it in… |
    |---|---|
    | the table you **keep** (left) | `WHERE` |
    | the **optional** table (right) | `ON ... AND ...` |

    ---
    ## 6.5 — Counting with `LEFT JOIN`

    > *"Headcount per department — including departments with nobody."*

    ### `COUNT(*)` gives Legal a headcount of 1 ❌
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT d.dept_name, COUNT(*) AS headcount
        FROM departments d
        LEFT JOIN employees e ON e.dept_id = d.dept_id
        GROUP BY d.dept_id, d.dept_name
        ORDER BY d.dept_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After the `LEFT JOIN`, Legal still has **one row** (with `NULL` employee
    columns). `COUNT(*)` counts rows.

    ### `COUNT(e.emp_id)` counts real employees ✅ — and watch `SUM`
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT d.dept_name,
               COUNT(e.emp_id)            AS headcount,
               SUM(e.salary)              AS payroll_raw,
               COALESCE(SUM(e.salary), 0) AS payroll
        FROM departments d
        LEFT JOIN employees e ON e.dept_id = d.dept_id
        GROUP BY d.dept_id, d.dept_name
        ORDER BY d.dept_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - `COUNT(e.emp_id)` → **0** for Legal (it skips `NULL`)
    - `SUM(e.salary)` → **`NULL`** for Legal (there is nothing to add)
    - `COALESCE(SUM(e.salary), 0)` → **0**, which is what a report should say

    ---
    ## 6.6 — Chains of Joins

    `employees → assignments → projects`. Every employee, with their projects:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.emp_name,
               COALESCE(p.project_name, '(no project)') AS project
        FROM employees e
        LEFT JOIN assignments a ON e.emp_id = a.emp_id
        LEFT JOIN projects    p ON a.project_id = p.project_id
        ORDER BY e.emp_id, p.project_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **36 rows**: 25 assignments + 11 employees with no project (shown as
    `(no project)`).

    ### One `INNER JOIN` in the chain drops people

    Compare the row counts. Changing only the **last** join to `INNER JOIN` loses
    every employee without a project:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT COUNT(*) AS row_count, COUNT(DISTINCT e.emp_id) AS employees
        FROM employees e
        LEFT  JOIN assignments a ON e.emp_id = a.emp_id
        INNER JOIN projects    p ON a.project_id = p.project_id
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT COUNT(*) AS row_count, COUNT(DISTINCT e.emp_id) AS employees
        FROM employees e
        LEFT JOIN assignments a ON e.emp_id = a.emp_id
        LEFT JOIN projects    p ON a.project_id = p.project_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    19 employees instead of 30. For the unassigned employees, `a.project_id` is
    `NULL`, so the final `INNER JOIN` finds no project and drops the row.

    **Rule:** once a row can have `NULL`s, keep using `LEFT JOIN` for the tables
    after it.

    ### A business report across 3 tables

    > *"For each department: how many projects are its people on, and how many
    > hours a week?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT d.dept_name,
               COUNT(DISTINCT a.project_id)         AS projects,
               COALESCE(SUM(a.hours_per_week), 0)   AS weekly_hours
        FROM departments d
        LEFT JOIN employees   e ON e.dept_id   = d.dept_id
        LEFT JOIN assignments a ON a.emp_id    = e.emp_id
        GROUP BY d.dept_id, d.dept_name
        ORDER BY weekly_hours DESC, d.dept_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6.7 — Self-Joins at Work

    `manager_id` points to another row of `employees`. Use the table twice, with
    two aliases: `e` (employee) and `m` (manager).

    > *"Does anyone earn more than their own manager?"* — a classic HR audit.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.emp_name AS employee, e.salary,
               m.emp_name AS manager, m.salary AS manager_salary
        FROM employees e
        INNER JOIN employees m ON e.manager_id = m.emp_id
        WHERE e.salary > m.salary
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Exactly one: **Mia** (130,000) earns more than her manager **Leo** (125,000).
    A real finding — an analyst would flag it, not fix it.

    ### Who manages the most people?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.emp_name AS manager,
               COUNT(e.emp_id) AS direct_reports
        FROM employees m
        LEFT JOIN employees e ON e.manager_id = m.emp_id
        GROUP BY m.emp_id, m.emp_name
        HAVING COUNT(e.emp_id) > 0
        ORDER BY direct_reports DESC, manager
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `HAVING COUNT(e.emp_id) > 0` keeps only people who manage someone.

    ---
    ## 6.8 — A Real Error: Ambiguous Column

    `employees` and `departments` both have a `dept_id` column. Name it without a
    table alias and DuckDB refuses:
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _bad = """SELECT emp_name, dept_id, dept_name
    FROM employees e
    INNER JOIN departments d ON e.dept_id = d.dept_id"""
    try:
        con.execute(_bad).fetchdf()
        _msg = "No error?!"
    except Exception as _e:
        _msg = str(_e)
    mo.md(f"""
    ```sql
    {_bad}
    ```

    **DuckDB says:**

    ```
    {_msg}
    ```

    **Fix:** say which one you mean — `e.dept_id` or `d.dept_id`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Week 6 Summary

    | Question | Join |
    |---|---|
    | Rows that match on both sides | `INNER JOIN` |
    | Keep every row of one table | `LEFT JOIN` (start from that table) |
    | Who / what has **no** partner? | `LEFT JOIN ... WHERE right_key IS NULL` |
    | Count per group, **including zero** | `LEFT JOIN` + `COUNT(right_key)` |
    | Total per group, zero not `NULL` | `COALESCE(SUM(...), 0)` |
    | Filter the optional table | condition in `ON` |
    | Compare rows of the same table | self-join with two aliases |

    ---
    ## Looking Ahead

    Several questions this week needed **two steps** — "the average", then "who is
    above it". Week 7 answers them in one query, with **subqueries**.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return



if __name__ == "__main__":
    app.run()
