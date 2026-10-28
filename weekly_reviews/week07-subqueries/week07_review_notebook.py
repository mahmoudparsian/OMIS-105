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
    # OMIS 105 — Week 7 Review: Subqueries

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    A **subquery** is a `SELECT` inside another SQL statement. It answers a
    question that needs **two steps** in one query: first find a value or a list,
    then use it. We start from the simplest kind and move up, on the same tech
    company as Weeks 4–6.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | Scalar subqueries | `WHERE x > (SELECT AVG(...))`, subqueries in `SELECT` |
    | List subqueries | `IN`, nested `IN` |
    | The `NOT IN` + `NULL` trap | `NOT IN`, `IS NOT NULL`, `NOT EXISTS` |
    | Is there at least one? | `EXISTS` |
    | Subqueries in `FROM` | derived tables |
    | Correlated subqueries | compare each row with its own group |
    | Subquery or JOIN? | duplicates vs. one row per item |
    | CTEs | `WITH`, chained CTEs |

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
    ## 7.1 — Scalar Subqueries: One Value

    > *"Who earns more than the company average?"*

    Step 1 on its own — the average:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Step 2 needs that number. Instead of typing `123866.67` by hand, put step 1
    **inside** step 2. The inner query runs first; its one value is used by the
    outer query.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name, salary
        FROM employees
        WHERE salary > (SELECT AVG(salary) FROM employees)
        ORDER BY salary DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **15 employees.** If a salary changes tomorrow, the query is still right — a
    hand-typed number would not be.

    ### Any aggregate works: the newest hire
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name, hire_date
        FROM employees
        WHERE hire_date = (SELECT MAX(hire_date) FROM employees)
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A scalar subquery in `SELECT`

    > *"For Marketing (department 20), how far is each salary from the company
    > average?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name,
               salary,
               ROUND(salary - (SELECT AVG(salary) FROM employees), 2) AS vs_company_avg
        FROM employees
        WHERE dept_id = 20
        ORDER BY salary DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A real error: the subquery returns more than one row

    `=` needs **one** value. `GROUP BY dept_id` returns one maximum **per department**
    (6 rows, counting the no-department group), so this fails:
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _bad = """SELECT emp_name
    FROM employees
    WHERE salary = (SELECT MAX(salary) FROM employees GROUP BY dept_id)"""
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

    **Fix:** a list needs `IN`, not `=`. (Or think again: did you mean the *one* overall `MAX`?)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7.2 — List Subqueries: `IN`

    > *"Who works in a department located in San Jose?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name, dept_id
        FROM employees
        WHERE dept_id IN (SELECT dept_id
                          FROM departments
                          WHERE dept_location = 'San Jose')
        ORDER BY dept_id, emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Nested `IN` — read it inside-out

    > *"Who works on a project that is still in **Planning**?"*

    1. **Innermost:** projects in Planning → 107, 108
    2. **Middle:** employees assigned to 107 or 108
    3. **Outer:** their names
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name
        FROM employees
        WHERE emp_id IN (
            SELECT emp_id
            FROM assignments
            WHERE project_id IN (
                SELECT project_id
                FROM projects
                WHERE status = 'Planning'
            )
        )
        ORDER BY emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7.3 — The `NOT IN` + `NULL` Trap ⚠️

    > *"Which departments have no employees?"* — we know the answer is **Legal**.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT dept_id, dept_name
        FROM departments
        WHERE dept_id NOT IN (SELECT dept_id
                              FROM employees)
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **0 rows!** Look at the list the subquery returns:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT DISTINCT dept_id
        FROM employees
        ORDER BY dept_id NULLS LAST
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It contains a `NULL` (Zack, Amy, and Ben have no department). For Legal (60),
    `NOT IN` checks `60 <> 10 AND … AND 60 <> NULL`. The last comparison is
    **unknown**, so the whole test is unknown, and `WHERE` drops the row.

    **One `NULL` in a `NOT IN` list → zero rows, no error.**

    ### Fix 1: remove the `NULL`s inside the subquery
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT dept_id, dept_name
        FROM departments
        WHERE dept_id NOT IN (SELECT dept_id
                              FROM employees
                              WHERE dept_id IS NOT NULL)
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Fix 2 (preferred): `NOT EXISTS` — always safe
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT d.dept_id, d.dept_name
        FROM departments d
        WHERE NOT EXISTS (SELECT 1
                          FROM employees e
                          WHERE e.dept_id = d.dept_id)
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7.4 — `EXISTS`: Is There at Least One?

    > *"Which departments have at least one person **leading** a project?"*

    For each department `d`, the subquery looks for a matching row. `SELECT 1` is a
    custom — `EXISTS` only cares whether a row exists. A subquery may contain a JOIN.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT d.dept_name
        FROM departments d
        WHERE EXISTS (SELECT 1
                      FROM employees e
                      INNER JOIN assignments a ON a.emp_id = e.emp_id
                      WHERE e.dept_id = d.dept_id
                        AND a.role = 'Lead')
        ORDER BY d.dept_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7.5 — Subqueries in `FROM` (Derived Tables)

    > *"What is the average department payroll?"* — an average **of totals**.

    Step 1, the totals:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT dept_id, SUM(salary) AS payroll
        FROM employees
        WHERE dept_id IS NOT NULL
        GROUP BY dept_id
        ORDER BY dept_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Step 2, query the result of step 1. A subquery in `FROM` needs a name (`AS t`):
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT COUNT(*)               AS departments,
               ROUND(AVG(payroll), 2) AS avg_payroll,
               MAX(payroll)           AS max_payroll
        FROM (
            SELECT dept_id, SUM(salary) AS payroll
            FROM employees
            WHERE dept_id IS NOT NULL
            GROUP BY dept_id
        ) AS t
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7.6 — Correlated Subqueries: Each Row vs. Its Own Group

    > *"Who earns more than the average **of their own department**?"*

    The subquery uses `e.dept_id` from the **outer** row, so it runs once per
    employee. Write the alias on **both** sides (`e2.dept_id = e.dept_id`) — a bare
    `dept_id` would mean `e2.dept_id`, and the test would always be true.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.emp_name, e.dept_id, e.salary
        FROM employees e
        WHERE e.salary > (SELECT AVG(e2.salary)
                          FROM employees e2
                          WHERE e2.dept_id = e.dept_id)
        ORDER BY e.dept_id, e.salary DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **12 employees.** Notice Zack, Amy, and Ben are never in the result: for them
    `e2.dept_id = NULL` matches nothing, so the average is `NULL`.

    ### The longest-serving employee in each department
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.dept_id, e.emp_name, e.hire_date
        FROM employees e
        WHERE e.hire_date = (SELECT MIN(e2.hire_date)
                             FROM employees e2
                             WHERE e2.dept_id = e.dept_id)
        ORDER BY e.dept_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7.7 — Subquery or JOIN?

    > *"Who is assigned to at least one project?"*

    ### With a JOIN — one row **per assignment**
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.emp_name
        FROM employees e
        INNER JOIN assignments a ON a.emp_id = e.emp_id
        ORDER BY e.emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **25 rows** — Alice, Carol, Chloe… appear twice. With `IN` — one row **per employee**:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name
        FROM employees
        WHERE emp_id IN (SELECT emp_id FROM assignments)
        ORDER BY emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **19 rows.** Rule of thumb: need columns from **both** tables → JOIN. Only
    **checking** another table → `IN` / `EXISTS`.

    ---
    ## 7.8 — CTEs: Give a Subquery a Name

    `WITH name AS (...)` moves the subquery to the top. Read it top to bottom, and
    use the name more than once.

    > *"Which departments pay more than the average department?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        WITH dept_stats AS (
            SELECT dept_id,
                   COUNT(*)    AS headcount,
                   AVG(salary) AS avg_salary
            FROM employees
            WHERE dept_id IS NOT NULL
            GROUP BY dept_id
        )
        SELECT d.dept_name, ds.headcount, ROUND(ds.avg_salary, 2) AS avg_salary
        FROM dept_stats ds
        INNER JOIN departments d ON ds.dept_id = d.dept_id
        WHERE ds.avg_salary > (SELECT AVG(avg_salary) FROM dept_stats)
        ORDER BY ds.avg_salary DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `dept_stats` is used **twice**: in `FROM` and inside the scalar subquery.

    ### Chained CTEs: the busiest project

    Each CTE can use the ones before it.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        WITH project_hours AS (
            SELECT project_id, SUM(hours_per_week) AS weekly_hours
            FROM assignments
            GROUP BY project_id
        ),
        busiest AS (
            SELECT project_id, weekly_hours
            FROM project_hours
            WHERE weekly_hours = (SELECT MAX(weekly_hours) FROM project_hours)
        )
        SELECT p.project_name, p.status, b.weekly_hours
        FROM busiest b
        INNER JOIN projects p ON b.project_id = p.project_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Week 7 Summary

    | Question | Tool |
    |---|---|
    | "…more than the **average**?" | scalar subquery |
    | "…who works on X?" | `IN` (or `EXISTS`) |
    | "…has **no** …?" | `NOT EXISTS` — never a bare `NOT IN` on a column with `NULL`s |
    | "…the average **of totals**?" | subquery in `FROM` |
    | "…above **their own group's** average?" | correlated subquery |
    | show columns from both tables | JOIN |
    | long, multi-step query | CTE (`WITH`) |

    ---
    ## Looking Ahead

    Week 8 steps back from querying to **design**: how should these tables have
    been built in the first place? Normal forms, keys, and the constraints that stop
    bad data — like an employee with no department — at the door.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return



if __name__ == "__main__":
    app.run()
