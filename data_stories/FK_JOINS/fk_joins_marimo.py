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
    # 🔗 Foreign Keys & JOINs in Relational Databases
    ### A Hands-On Tutorial with DuckDB

    ---

    ## What You Will Learn

    | Topic | Description |
    |---|---|
    | **Primary Key (PK)** | Quick recap — uniquely identifies every row |
    | **Foreign Key (FK)** | Links rows in one table to rows in another |
    | **Referential Integrity** | Why the database enforces FK rules |
    | **INNER JOIN** | Returns only rows that match in **both** tables |
    | **LEFT JOIN** | Returns **all** rows from the left table, matched or not |
    | **RIGHT JOIN** | Returns **all** rows from the right table, matched or not |

    ---

    ## The Schema We Will Use

    ```
     departments                       employees
    ┌─────────────────────────┐       ┌──────────────────────────────┐
    │ dept_id   PK  INTEGER   │◄──FK──│ emp_id    PK  INTEGER        │
    │ dept_name     VARCHAR   │       │ dept_id   FK  INTEGER (NULL) │
    │ dept_location VARCHAR   │       │ gender        VARCHAR        │
    │ budget        INTEGER   │       │ salary        INTEGER        │
    └─────────────────────────┘       └──────────────────────────────┘
    ```

    **Key design decisions:**
    - `employees.dept_id` is a **Foreign Key** pointing to `departments.dept_id`.
    - `employees.dept_id` is **nullable** — some employees have not yet been assigned to a department.
    - One department (`LEGAL`) has **no employees** — intentional, so RIGHT JOIN has something to show.
    - The FK constraint means you **cannot** insert an employee with a `dept_id` that does not exist in `departments`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 0 · Setup

    Install dependencies (safe to re-run), import libraries, and connect to DuckDB.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import sys, os

    sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))
    from fk_joins_plot_util import (
        display_table,
        plot_join_counts,
        plot_salary_by_dept,
        plot_budget_vs_headcount,
        plot_null_dept_pie,
    )

    DEPT_CSV = 'data/departments.csv'
    EMP_CSV  = 'data/employees.csv'

    # In-memory DuckDB — fresh each run, so notebook is fully idempotent
    con = duckdb.connect(database=':memory:')
    print('✅  DuckDB connected  |  version:', duckdb.__version__)
    return (DEPT_CSV, EMP_CSV, con, display_table, plot_budget_vs_headcount, plot_join_counts, plot_null_dept_pie, plot_salary_by_dept)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1 · Quick Recap — Primary Key (PK)

    A **Primary Key** uniquely identifies every row in a table.

    Rules:
    - Every value must be **unique** — no two rows share the same PK.
    - PK columns can **never be NULL**.
    - A table can have only **one** primary key (though it may span multiple columns).

    In our schema:
    - `departments.dept_id` is the PK of the departments table.
    - `employees.emp_id` is the PK of the employees table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2 · Foreign Key (FK) — The Link Between Tables

    A **Foreign Key** is a column in one table that **references the Primary Key of another table**.

    ```
      departments.dept_id  ←──── employees.dept_id
           (PK)                       (FK)
    ```

    ### What the FK constraint guarantees

    | Scenario | Without FK | With FK enforced |
    |---|---|---|
    | Insert employee with `dept_id = 99` (non-existent) | Silently accepted ❌ | Error raised ✅ |
    | Delete a dept that still has employees | Silently accepted ❌ | Error raised ✅ |

    ### NULL is allowed

    A FK column *may* be `NULL` — it simply means the row has no parent yet.  
    In our data, employees 401 and 402 have `dept_id = NULL`, meaning they have not been assigned to any department.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3 · Create Tables and Load Data

    We always create the **parent table first** (`departments`), then the **child table** (`employees`).  
    The FK cannot reference a table that does not yet exist.
    """)
    return


@app.cell
def _(DEPT_CSV, con, display_table):
    # ── Parent table first ───────────────────────────────────────────────────────
    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)    # child must be dropped first
    con.execute("""
        DROP TABLE IF EXISTS departments;
    """)

    _sql = """
        CREATE TABLE departments (
            dept_id       INTEGER PRIMARY KEY,
            dept_name     VARCHAR NOT NULL,
            dept_location VARCHAR NOT NULL,
            budget        INTEGER NOT NULL
        );
    """
    con.execute(_sql)
    con.execute("""
        INSERT INTO departments
        SELECT *
        FROM read_csv_auto(?);
    """, [DEPT_CSV])

    _df = con.execute("""
        SELECT *
        FROM departments
        ORDER BY dept_id;
    """).df()
    display_table(_df, 'departments — 4 rows (LEGAL has no employees yet)')
    return


@app.cell
def _(EMP_CSV, con, display_table):
    # ── Child table second — FK references departments ───────────────────────────
    _sql = """
        CREATE TABLE employees (
            emp_id  INTEGER PRIMARY KEY,
            dept_id INTEGER REFERENCES departments(dept_id),
            /* FK */     gender VARCHAR NOT NULL,
            salary  INTEGER NOT NULL
        );
    """
    con.execute(_sql)
    con.execute("""
        INSERT INTO employees
        SELECT *
        FROM read_csv_auto(?);
    """, [EMP_CSV])

    _df = con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id;
    """).df()
    display_table(_df, 'employees — 8 rows (401 and 402 have NULL dept_id)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 · FK Enforcement in Action

    Let's try to break referential integrity and watch DuckDB stop us.
    """)
    return


@app.cell
def _(con):
    # ── Attempt 1: insert an employee pointing to a dept that does NOT exist ──────
    print('Inserting emp_id=999 with dept_id=99 (dept 99 does not exist)...')
    try:
        con.execute("""
            INSERT INTO employees
            VALUES (999, 99, 'MALE', 50000);
        """)
        print('ERROR: DuckDB accepted an invalid FK — not good!')
    except Exception as e:
        print(f'✅  DuckDB rejected it:\n    {e}')
    return


@app.cell
def _(con):
    # ── Attempt 2: delete a department that still has employees ───────────────────
    print('Deleting dept_id=10 (SALES) which has employees 101 and 102...')
    try:
        con.execute("""
            DELETE
            FROM departments
            WHERE dept_id = 10;
        """)
        print('ERROR: DuckDB allowed orphaned employees — not good!')
    except Exception as e:
        print(f'✅  DuckDB rejected it:\n    {e}')
    return


@app.cell
def _(con, display_table):
    # ── Attempt 3: NULL dept_id IS allowed (employee not yet assigned) ────────────
    con.execute("""
        DELETE
        FROM employees
        WHERE emp_id = 501;
    """)
    print('Inserting emp_id=501 with dept_id=NULL (unassigned employee)...')
    try:
        con.execute("""
            INSERT INTO employees
            VALUES (501, NULL, 'FEMALE', 72000);
        """)
        _df = con.execute("""
            SELECT *
            FROM employees
            WHERE emp_id = 501;
        """).df()
        display_table(_df, 'NULL dept_id accepted — employee exists but is unassigned')
        con.execute("""
            DELETE
            FROM employees
            WHERE emp_id = 501;
        """)  # clean up
    except Exception as e:
        print(f'Unexpected error: {e}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 · Exploring the Data Before Joining

    Before writing any JOIN, understand the shape of your data:  
    how many employees have a department, and how many do not?
    """)
    return


@app.cell
def _(con, display_table, plot_null_dept_pie):
    _sql = """
        SELECT
            COUNT(*) AS total_employees,
            COUNT(dept_id) AS with_dept,
            COUNT(*) - COUNT(dept_id) AS without_dept
        FROM employees;
    """
    print('SQL:\n', _sql)
    _df = con.execute(_sql).df()
    display_table(_df, 'Employee dept assignment summary')

    row = _df.iloc[0]
    plot_null_dept_pie(int(row['with_dept']), int(row['without_dept']))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6 · JOINs — Combining Two Tables

    A **JOIN** lets you combine columns from two (or more) tables based on a matching condition.

    The general syntax is:

    ```sql
    SELECT ...
      FROM  left_table
      <JOIN TYPE>  right_table  ON  left_table.key = right_table.key
    ```

    In our case the join condition is always:

    ```sql
    ON employees.dept_id = departments.dept_id
    ```

    ### The three JOIN types we will cover

    | JOIN type | What it returns |
    |---|---|
    | `INNER JOIN` | Only rows where `dept_id` matches in **both** tables |
    | `LEFT JOIN`  | **All** employees — matched get dept info, unmatched get NULL |
    | `RIGHT JOIN` | **All** departments — matched get employee info, empty depts show up too |

    Think of it visually:

    ```
     employees          departments
    ┌────────┐         ┌────────────┐
    │  101   │◄───────►│     10     │  INNER: both sides match
    │  102   │◄───────►│     10     │
    │  201   │◄───────►│     20     │
    │  202   │◄───────►│     20     │
    │  301   │◄───────►│     30     │
    │  302   │◄───────►│     30     │
    │  401   │  NULL   │            │  LEFT only: employee has no dept
    │  402   │  NULL   │            │  LEFT only: employee has no dept
    │        │         │     40     │  RIGHT only: LEGAL has no employees
    └────────┘         └────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 6.1  INNER JOIN

    **Returns only the rows where the join condition is satisfied on both sides.**

    - Employees with `dept_id = NULL` are **excluded** (no match).
    - Department 40 (`LEGAL`) is **excluded** (no employees point to it).
    - Result: only the 6 employees who are assigned to an existing department.

    > Use INNER JOIN when you only care about rows that have a complete match on both sides.
    """)
    return


@app.cell
def _(con, display_table, plot_salary_by_dept):
    _sql = """
        SELECT
            e.emp_id,
            d.dept_name,
            d.dept_location,
            e.gender,
            e.salary
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        ORDER BY e.emp_id;
    """
    print('SQL:\n', _sql)
    df_inner = con.execute(_sql).df()
    display_table(df_inner,
        f'INNER JOIN — {len(df_inner)} rows '
        '(employees 401/402 excluded; LEGAL excluded)')

    plot_salary_by_dept(
        df_inner.groupby('dept_name', as_index=False)['salary'].mean().rename(
            columns={'salary': 'avg_salary'}),
        title='INNER JOIN — Average Salary per Department'
    )
    return (df_inner,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 6.2  LEFT JOIN

    **Returns every row from the LEFT table (`employees`), plus matching columns from the RIGHT table (`departments`) where available.**

    - Employees **with** a valid `dept_id` → dept columns filled in.
    - Employees **without** a `dept_id` (NULL) → still appear, but dept columns are `NULL`.
    - Department 40 (`LEGAL`) → still excluded because no employees reference it.

    > Use a LEFT JOIN when you need all records from the left table, regardless of whether a match exists.  
    > Classic question: *Show all employees and their department if they have one.*
    """)
    return


@app.cell
def _(con, display_table):
    _sql = """
        SELECT
            e.emp_id,
            e.dept_id AS emp_dept_id,
            d.dept_name,
            d.dept_location,
            e.gender,
            e.salary
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.dept_id = d.dept_id
        ORDER BY e.emp_id;
    """
    print('SQL:\n', _sql)
    df_left = con.execute(_sql).df()
    display_table(df_left,
        f'LEFT JOIN — {len(df_left)} rows '
        '(all 8 employees; 401/402 show NULL for dept columns)')
    return (df_left,)


@app.cell
def _(con, display_table):
    # ── Use LEFT JOIN + WHERE IS NULL to find unassigned employees ────────────────
    _sql = """
        SELECT
            e.emp_id,
            e.gender,
            e.salary,
            d.dept_name
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.dept_id = d.dept_id
        WHERE d.dept_id IS NULL
        ORDER BY e.emp_id;
    """
    print('SQL:\n', _sql)
    df_unassigned = con.execute(_sql).df()
    display_table(df_unassigned,
        'LEFT JOIN + WHERE IS NULL — employees with no department assigned')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 6.3  RIGHT JOIN

    **Returns every row from the RIGHT table (`departments`), plus matching columns from the LEFT table (`employees`) where available.**

    - Departments **with** employees → those employees appear.
    - Department 40 (`LEGAL`) → still appears, but employee columns are `NULL`.
    - Employees 401/402 (no dept) → excluded because they match no department.

    > Use a RIGHT JOIN when you need all records from the right table.  
    > Classic question: *Show all departments — even the ones with no staff.*

    > **Tip:** A RIGHT JOIN is equivalent to swapping table order and writing a LEFT JOIN.  
    > Most developers prefer LEFT JOINs for readability, but RIGHT JOIN is useful when reordering the FROM clause is awkward.
    """)
    return


@app.cell
def _(con, display_table):
    _sql = """
        SELECT
            d.dept_id,
            d.dept_name,
            d.dept_location,
            d.budget,
            e.emp_id,
            e.gender,
            e.salary
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.dept_id = d.dept_id
        ORDER BY d.dept_id, e.emp_id;
    """
    print('SQL:\n', _sql)
    df_right = con.execute(_sql).df()
    display_table(df_right,
        f'RIGHT JOIN — {len(df_right)} rows '
        '(LEGAL dept_id=40 appears with NULL employee columns)')
    return (df_right,)


@app.cell
def _(con, display_table):
    # ── RIGHT JOIN + WHERE IS NULL to find departments with NO employees ──────────
    _sql = """
        SELECT
            d.dept_id,
            d.dept_name,
            d.dept_location,
            d.budget
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.dept_id = d.dept_id
        WHERE e.emp_id IS NULL
        ORDER BY d.dept_id;
    """
    print('SQL:\n', _sql)
    df_empty_depts = con.execute(_sql).df()
    display_table(df_empty_depts,
        'RIGHT JOIN + WHERE IS NULL — departments with no employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7 · Comparing the Three JOINs Side-by-Side

    The same two tables, three different lenses:
    """)
    return


@app.cell
def _(df_inner, df_left, df_right, plot_join_counts):
    labels = ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN']
    counts = [len(df_inner), len(df_left), len(df_right)]

    for label, count in zip(labels, counts):
        print(f'  {label:<12}  →  {count} rows')

    plot_join_counts(labels, counts)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8 · Analytics Across Tables

    JOINs become powerful when combined with aggregations.  
    Here we combine data from both tables to answer real business questions.
    """)
    return


@app.cell
def _(con, display_table, plot_salary_by_dept):
    # ── Headcount, avg salary, and budget per department ─────────────────────────
    _sql = """
        SELECT
            d.dept_name,
            d.dept_location,
            d.budget,
            COUNT(e.emp_id) AS headcount,
            ROUND(AVG(e.salary), 0) AS avg_salary
        FROM departments AS d
        LEFT
        JOIN employees AS e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name, d.dept_location, d.budget
        ORDER BY headcount DESC;
    """
    print('SQL:\n', _sql)
    df_stats = con.execute(_sql).df()
    display_table(df_stats, 'Dept stats — headcount, avg salary, budget (LEGAL shows 0 headcount)')

    df_with_emp = df_stats[df_stats['headcount'] > 0].copy()
    plot_salary_by_dept(df_with_emp, title='Average Salary by Department (assigned employees only)')
    return (df_stats,)


@app.cell
def _(df_stats, plot_budget_vs_headcount):
    # ── Budget vs headcount scatter (all depts including empty LEGAL) ─────────────
    plot_budget_vs_headcount(
        df_stats,
        title='Department Budget vs Headcount'
    )
    return


@app.cell
def _(con, display_table):
    # ── Budget per assigned employee (resource efficiency) ───────────────────────
    _sql = """
        SELECT
            d.dept_name,
            d.budget,
            COUNT(e.emp_id) AS headcount,
            ROUND(d.budget * 1.0 / NULLIF(COUNT(e.emp_id),0)) AS budget_per_employee
        FROM departments AS d
        LEFT
        JOIN employees AS e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name, d.budget
        ORDER BY budget_per_employee DESC NULLS LAST;
    """
    print('SQL:\n', _sql)
    df_eff = con.execute(_sql).df()
    display_table(df_eff,
        'Budget per employee by department '
        '(LEGAL shows NULL — divide by zero avoided with NULLIF)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 9 · Summary

    | Concept | Key Takeaway |
    |---|---|
    | **Primary Key** | Uniquely identifies every row; never NULL |
    | **Foreign Key** | Links child rows to parent rows; enforces referential integrity |
    | **FK + NULL** | A NULL FK is allowed — it means not yet assigned |
    | **INNER JOIN** | Only matched rows on both sides — strictest, smallest result |
    | **LEFT JOIN** | All rows from the left table — unmatched right columns become NULL |
    | **RIGHT JOIN** | All rows from the right table — unmatched left columns become NULL |
    | **IS NULL trick** | Combine with LEFT/RIGHT JOIN to find *unmatched* rows specifically |

    ### When to use which JOIN?

    - **INNER JOIN** — Give me only records that exist in both tables.
    - **LEFT JOIN** — Give me everything from the left table; fill in right-side data where it exists.
    - **RIGHT JOIN** — Give me everything from the right table; fill in left-side data where it exists.

    > **Good habit:** Always think about NULLs *before* writing a JOIN.  
    > Ask yourself: are there rows on either side that have no match? What should happen to them?
    """)
    return


if __name__ == "__main__":
    app.run()
