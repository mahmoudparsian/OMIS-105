import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from plot_helpers import plot_bar, plot_hbar, plot_pie

    return plot_bar, plot_hbar, plot_pie


@app.cell
def _():
    import duckdb

    # This notebook queries the DuckDB database built by create_duckdb.sh.
    # Run that script first (from the duckdb/ folder):
    #     ./create_duckdb.sh
    con = duckdb.connect("employee.duckdb")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Employee Database (DuckDB Edition)

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### About This Database

    This is a DuckDB version of the classic MySQL "employee" sample
    database (`mysql/dataset_small`). It has 6 tables:

    | Table | What it holds |
    |-------|----------------|
    | `employee` | 1 row per person: name, birth date, gender, hire date |
    | `department` | 1 row per department: code + name |
    | `dept_emp` | which department each employee works in, and when |
    | `dept_manager` | which employee manages each department, and when |
    | `title` | job titles held by each employee over time |
    | `salary` | salary history for each employee |

    To make the practice queries more realistic, this DuckDB version also adds:

    - **3 employees with no department** (`emp_no` 20001–20003) — new
      hires who haven't been assigned yet.
    - **3 departments with no employees** (`dept_no` d010–d012) — new
      departments that are still being staffed.

    ### 14 Practice Queries

    | Level | Count | Focus |
    |-------|-------|-------|
    | Simple | 4 | SELECT, WHERE, ORDER BY, LIMIT, DISTINCT |
    | Intermediate | 5 | JOIN, GROUP BY, LEFT JOIN + IS NULL |
    | Intermediate+ | 5 | Window functions, CTEs, HAVING, multi-step joins |

    ### How to Use

    Run each cell in order. Read the markdown — it explains the *why*
    behind every query. In Marimo, SQL cells run directly against DuckDB
    — no Python wrappers needed!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Setup — Confirm the Database Loaded
    """)
    return


@app.cell
def _(con, department, dept_emp, dept_manager, employee, mo, salary, title):
    _df = mo.sql(
        f"""
        SELECT 'department'   AS table_name, COUNT(*) AS row_count FROM department
        UNION ALL SELECT 'employee',      COUNT(*) FROM employee
        UNION ALL SELECT 'dept_emp',      COUNT(*) FROM dept_emp
        UNION ALL SELECT 'dept_manager',  COUNT(*) FROM dept_manager
        UNION ALL SELECT 'title',         COUNT(*) FROM title
        UNION ALL SELECT 'salary',        COUNT(*) FROM salary
        ORDER BY table_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # SIMPLE QUERIES

    ---

    ## S1 — SELECT, ORDER BY

    > *"Show me every department, alphabetically."*
    """)
    return


@app.cell
def _(con, department, mo):
    _df = mo.sql(
        f"""
        SELECT dept_no, 
               dept_name
        FROM   department
        ORDER BY dept_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S2 — WHERE + LIKE

    > *"Find every employee whose last name starts with 'A'."*

    `LIKE 'A%'` matches any string that starts with the letter `A`.
    """)
    return


@app.cell
def _(con, employee, mo):
    _df = mo.sql(
        f"""
        SELECT emp_no, first_name, last_name, hire_date
        FROM   employee
        WHERE  last_name LIKE 'A%'
        ORDER BY last_name, first_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S3 — ORDER BY + LIMIT

    > *"Who are the 10 most recently hired employees?"*
    """)
    return


@app.cell
def _(con, employee, mo):
    _df = mo.sql(
        f"""
        SELECT emp_no, first_name, last_name, hire_date
        FROM   employee
        ORDER BY hire_date DESC
        LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S4 — DISTINCT

    > *"What job titles exist at this company?"*

    `DISTINCT` removes duplicate rows — each title appears once, no
    matter how many employees have held it.
    """)
    return


@app.cell
def _(con, mo, title):
    _df = mo.sql(
        f"""
        SELECT DISTINCT title
        FROM   title
        ORDER BY title;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # INTERMEDIATE QUERIES

    ---

    ## I1 — JOIN + GROUP BY

    > *"How many people currently work in each department?"*

    `dept_emp.to_date = '9999-01-01'` marks the employee's *current*
    department assignment (an open-ended interval that hasn't closed yet).
    """)
    return


@app.cell
def _(con, department, dept_emp, mo):
    df_dept_headcount = mo.sql(
        f"""
        SELECT d.dept_name,
               COUNT(*) AS num_employees
        FROM   dept_emp de
        JOIN   department d ON de.dept_no = d.dept_no
        WHERE  de.to_date = DATE '9999-01-01'
        GROUP BY d.dept_name
        ORDER BY num_employees DESC;
        """,
        engine=con
    )
    return (df_dept_headcount,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Headcount by Department
    """)
    return


@app.cell
def _(df_dept_headcount, plot_bar):
    plot_bar(df_dept_headcount, x="dept_name", y="num_employees",
             title="Current Headcount by Department", ylabel="Employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I2 — Multi-table JOIN + GROUP BY + Window Function

    > *"What is the average current salary in each department?"*

    Each employee has many rows in `salary` (one per raise). We use
    `ROW_NUMBER() OVER (PARTITION BY emp_no ORDER BY from_date DESC)`
    to pick each employee's *most recent* salary row before averaging.
    """)
    return


@app.cell
def _(con, department, dept_emp, mo, salary):
    df_dept_avg_salary = mo.sql(
        f"""
        WITH current_salary AS (
            SELECT emp_no, amount,
                   ROW_NUMBER() OVER (PARTITION BY emp_no ORDER BY from_date DESC) AS rn
            FROM   salary
        )
        SELECT d.dept_name,
               ROUND(AVG(cs.amount), 0) AS avg_salary
        FROM   current_salary cs
        JOIN   dept_emp de ON cs.emp_no = de.emp_no AND de.to_date = DATE '9999-01-01'
        JOIN   department d ON de.dept_no = d.dept_no
        WHERE  cs.rn = 1
        GROUP BY d.dept_name
        ORDER BY avg_salary DESC;
        """,
        engine=con
    )
    return (df_dept_avg_salary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Average Salary by Department
    """)
    return


@app.cell
def _(df_dept_avg_salary, plot_bar):
    plot_bar(df_dept_avg_salary, x="dept_name", y="avg_salary",
             title="Average Current Salary by Department",
             ylabel="Avg Salary", dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I3 — GROUP BY (Gender Distribution)

    > *"What is the gender breakdown of all employees?"*
    """)
    return


@app.cell
def _(con, employee, mo):
    df_gender = mo.sql(
        f"""
        SELECT gender, COUNT(*) AS num_employees
        FROM   employee
        GROUP BY gender
        ORDER BY gender;
        """,
        engine=con
    )
    return (df_gender,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Gender Distribution
    """)
    return


@app.cell
def _(df_gender, plot_pie):
    plot_pie(df_gender, labels="gender", values="num_employees",
             title="Employees by Gender")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I4 — LEFT JOIN + IS NULL (Employees With No Department)

    > *"Which employees are not yet assigned to a department?"*

    A `LEFT JOIN` keeps every row from `employee`, even ones with no
    match in `dept_emp`. Where there's no match, `de.emp_no` comes back
    `NULL` — that's how we find the unassigned employees.
    """)
    return


@app.cell
def _(con, dept_emp, employee, mo):
    _df = mo.sql(
        f"""
        SELECT e.emp_no, e.first_name, e.last_name, e.hire_date
        FROM   employee e
        LEFT JOIN dept_emp de ON e.emp_no = de.emp_no
        WHERE  de.emp_no IS NULL
        ORDER BY e.emp_no;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I5 — LEFT JOIN + IS NULL (Departments With No Employees)

    > *"Which departments have nobody working in them yet?"*

    Same idea as I4, flipped around: `LEFT JOIN` from `department`,
    then keep only the rows where `dept_emp` had no match.
    """)
    return


@app.cell
def _(con, department, dept_emp, mo):
    _df = mo.sql(
        f"""
        SELECT d.dept_no, d.dept_name
        FROM   department d
        LEFT JOIN dept_emp de ON d.dept_no = de.dept_no
        WHERE  de.dept_no IS NULL
        ORDER BY d.dept_no;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # INTERMEDIATE+ QUERIES

    ---

    ## A1 — CTEs + Window Functions (Current Salary & Title)

    > *"Show me the top 10 highest-paid employees, with their current title."*

    Two CTEs each use `ROW_NUMBER()` to pick out one "current" row per
    employee — one for salary, one for title — then we join them together.
    """)
    return


@app.cell
def _(con, employee, mo, salary, title):
    _df = mo.sql(
        f"""
        WITH current_salary AS (
            SELECT emp_no, amount,
                   ROW_NUMBER() OVER (PARTITION BY emp_no ORDER BY from_date DESC) AS rn
            FROM   salary
        ),
        current_title AS (
            SELECT emp_no, title,
                   ROW_NUMBER() OVER (PARTITION BY emp_no ORDER BY from_date DESC) AS rn
            FROM   title
        )
        SELECT e.emp_no, e.first_name, e.last_name,
               ct.title, cs.amount AS current_salary
            FROM   employee e
            JOIN   current_salary cs ON e.emp_no = cs.emp_no AND cs.rn = 1
            JOIN   current_title  ct ON e.emp_no = ct.emp_no AND ct.rn = 1
            ORDER BY cs.amount DESC
            LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A2 — RANK() (Top Earner in Each Department)

    > *"Who is the single highest-paid employee in each department?"*

    `RANK() OVER (PARTITION BY dept_name ORDER BY amount DESC)` numbers
    employees 1, 2, 3, ... *within each department*, restarting the
    count for every new department. We keep only rank 1.
    """)
    return


@app.cell
def _(con, department, dept_emp, employee, mo, salary):
    df_top_earners = mo.sql(
        f"""
        WITH current_salary AS (
            SELECT emp_no, amount,
                   ROW_NUMBER() OVER (PARTITION BY emp_no ORDER BY from_date DESC) AS rn
            FROM   salary
        ),
        dept_salary AS (
            SELECT d.dept_name, e.first_name, e.last_name, cs.amount,
                   RANK() OVER (PARTITION BY d.dept_name ORDER BY cs.amount DESC) AS salary_rank
            FROM   current_salary cs
            JOIN   dept_emp de ON cs.emp_no = de.emp_no AND de.to_date = DATE '9999-01-01'
            JOIN   department d ON de.dept_no = d.dept_no
            JOIN   employee e ON e.emp_no = cs.emp_no
            WHERE  cs.rn = 1
        )
        SELECT dept_name, first_name, last_name, amount AS salary
            FROM   dept_salary
            WHERE  salary_rank = 1
            ORDER BY salary DESC;
        """,
        engine=con
    )
    return (df_top_earners,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Top Earner per Department
    """)
    return


@app.cell
def _(df_top_earners, plot_hbar):
    plot_hbar(df_top_earners, x="salary", y="dept_name",
              title="Highest Salary in Each Department",
              xlabel="Salary", dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A3 — CTEs + HAVING (Above-Average Departments)

    > *"Which departments pay better than the company average?"*

    We build two CTEs — one average salary per department, one average
    salary company-wide — then compare them with a `WHERE` on the
    cross-joined result. (This is the CTE-based cousin of `HAVING`.)
    """)
    return


@app.cell
def _(con, department, dept_emp, mo, salary):
    _df = mo.sql(
        f"""
        WITH current_salary AS (
            SELECT emp_no, amount,
                   ROW_NUMBER() OVER (PARTITION BY emp_no ORDER BY from_date DESC) AS rn
            FROM   salary
        ),
        dept_avg AS (
            SELECT d.dept_name, AVG(cs.amount) AS avg_salary
            FROM   current_salary cs
            JOIN   dept_emp de ON cs.emp_no = de.emp_no AND de.to_date = DATE '9999-01-01'
            JOIN   department d ON de.dept_no = d.dept_no
            WHERE  cs.rn = 1
            GROUP BY d.dept_name
        ),
        company_avg AS (
            SELECT AVG(amount) AS company_avg_salary
            FROM   current_salary
            WHERE  rn = 1
        )
        SELECT da.dept_name,
               ROUND(da.avg_salary, 0) AS dept_avg_salary,
               ROUND(ca.company_avg_salary, 0) AS company_avg_salary
            FROM   dept_avg da, company_avg ca
            WHERE  da.avg_salary > ca.company_avg_salary
            ORDER BY dept_avg_salary DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A4 — GROUP BY + HAVING (Employees With Multiple Titles)

    > *"Which employees have been promoted (held more than one title)?"*

    `HAVING COUNT(DISTINCT title) > 1` filters out anyone who has only
    ever held a single title — `HAVING` filters *groups*, not rows.
    """)
    return


@app.cell
def _(con, employee, mo, title):
    _df = mo.sql(
        f"""
        SELECT e.emp_no, e.first_name, e.last_name,
               COUNT(DISTINCT t.title) AS num_titles_held
            FROM   employee e
            JOIN   title t ON e.emp_no = t.emp_no
            GROUP BY e.emp_no, e.first_name, e.last_name
            HAVING COUNT(DISTINCT t.title) > 1
            ORDER BY num_titles_held DESC, e.emp_no
            LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A5 — Window Functions (Salary Growth Since Hire)

    > *"Which employees have seen the biggest salary growth?"*

    Two `ROW_NUMBER()` windows over the same `salary` table — one
    ordered oldest-first (to find the *first* salary), one ordered
    newest-first (to find the *current* salary) — then we compare them.
    """)
    return


@app.cell
def _(con, employee, mo, salary):
    df_growth = mo.sql(
        f"""
        WITH ranked AS (
            SELECT emp_no, amount, from_date,
                   ROW_NUMBER() OVER (PARTITION BY emp_no ORDER BY from_date ASC)  AS rn_first,
                   ROW_NUMBER() OVER (PARTITION BY emp_no ORDER BY from_date DESC) AS rn_last
            FROM   salary
        )
        SELECT e.emp_no, e.first_name, e.last_name,
               f.amount AS first_salary,
               l.amount AS current_salary,
               l.amount - f.amount AS salary_growth,
               ROUND(100.0 * (l.amount - f.amount) / f.amount, 1) AS pct_growth
            FROM   employee e
            JOIN   ranked f ON e.emp_no = f.emp_no AND f.rn_first = 1
            JOIN   ranked l ON e.emp_no = l.emp_no AND l.rn_last = 1
            ORDER BY pct_growth DESC
            LIMIT 10;
        """,
        engine=con
    )
    return (df_growth,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Top 10 Salary Growth (% Since Hire)
    """)
    return


@app.cell
def _(df_growth, plot_hbar):
    plot_hbar(df_growth, x="pct_growth", y="last_name",
              title="Top 10 Employees by Salary Growth Since Hire",
              xlabel="Growth (%)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Summary

    In this notebook we practiced:

    - **Simple:** `SELECT`, `WHERE` + `LIKE`, `ORDER BY`, `LIMIT`, `DISTINCT`
    - **Intermediate:** `JOIN`, `GROUP BY`, `LEFT JOIN` + `IS NULL`
    - **Intermediate+:** CTEs (`WITH`), `ROW_NUMBER()`, `RANK()`, `HAVING`

    The 3 unassigned employees and 3 empty departments (added by
    `create_duckdb.sh`) gave I4 and I5 real rows to find — in the
    original dataset, every employee has a department and vice versa,
    so those `LEFT JOIN ... IS NULL` queries would otherwise return
    nothing to look at.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
