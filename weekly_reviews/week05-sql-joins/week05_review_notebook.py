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
    # OMIS 105 — Week 5 Review: Advanced Joins & Set Operations

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    `INNER JOIN` and `LEFT JOIN` cover most days. This week covers the rest:
    keeping both sides, pairing everything with everything, joining a table
    to itself, and finding the rows that match **nothing**.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | Keep both sides | `FULL OUTER JOIN`, `COALESCE` |
    | Every combination | `CROSS JOIN` |
    | A table joined to itself | `SELF JOIN` for manager and co-worker pairs |
    | Stack results | `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT` |
    | Find what is missing | `LEFT JOIN` + `IS NULL`, `NOT EXISTS`, `NOT IN` |

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
    ## 5.1 — FULL OUTER JOIN: Keep Everything from Both Sides

    INNER JOIN: only matching rows.
    LEFT JOIN: all from left + matching right.
    **FULL OUTER JOIN: all from BOTH sides** — NULLs where no match.

    > *"Show ALL employees and ALL departments — even unassigned employees
    > and departments with no employees."*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.emp_name,
               e.dept_id AS emp_dept_id,
               d.dept_id,
               d.dept_name
        FROM   employees e
        FULL OUTER JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name NULLS LAST, e.emp_name
        """
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
        f"""
        SELECT e.emp_name   AS employee,
               e.salary     AS emp_salary,
               m.emp_name   AS manager,
               m.salary     AS mgr_salary
        FROM   employees e
        LEFT JOIN employees m ON e.manager_id = m.emp_id
        ORDER BY e.emp_id
        """
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > *"Find pairs of employees in the same department (co-workers)."*
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
        f"""
        -- Employees eligible for a bonus (salary > 120K)
        CREATE OR REPLACE TABLE bonus_eligible AS
        SELECT emp_id, emp_name FROM employees WHERE salary > 120000
        """
    )
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT emp_name FROM bonus_eligible
        UNION
        SELECT emp_name FROM on_active_project
        ORDER BY emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### INTERSECT — Only those in BOTH lists

    > *"Employees who are bonus-eligible AND on an active project."*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name FROM bonus_eligible
        INTERSECT
        SELECT emp_name FROM on_active_project
        ORDER BY emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### EXCEPT — In the first list but NOT the second

    > *"Bonus-eligible employees who are NOT on any active project."*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name FROM bonus_eligible
        EXCEPT
        SELECT emp_name FROM on_active_project
        ORDER BY emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### UNION ALL — Keep duplicates (faster)

    Use UNION ALL when you know there are no duplicates or want to preserve them:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name, 'Bonus Eligible' AS source FROM bonus_eligible
        UNION ALL
        SELECT emp_name, 'Active Project' AS source FROM on_active_project
        ORDER BY emp_name, source
        """
    ).fetchdf()
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
def _(con):
    con.execute(
        f"""
        SELECT e.emp_name, e.salary
        FROM   employees e
        LEFT JOIN assignments a ON e.emp_id = a.emp_id
        WHERE  a.assignment_id IS NULL
        ORDER BY e.emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Pattern 2: NOT EXISTS
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Pattern 3: NOT IN
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name, salary
        FROM   employees
        WHERE  emp_id NOT IN (SELECT emp_id FROM assignments)
        ORDER BY emp_name
        """
    ).fetchdf()
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
def _(con):
    con.execute(
        f"""
        SELECT p.project_name, p.status
        FROM   projects p
        LEFT JOIN assignments a ON p.project_id = a.project_id
        WHERE  a.assignment_id IS NULL
        ORDER BY p.project_name
        """
    ).fetchdf()
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
    ## Looking Ahead

    You can now combine tables any way the question demands. Week 6 asks the
    prior question: how should those tables have been designed in the first place?
    """)
    return


if __name__ == "__main__":
    app.run()
