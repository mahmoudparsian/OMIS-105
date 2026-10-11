import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from plot_helpers import (
        plot_bar,
        plot_hbar,
        plot_hbar_groups,
        plot_join_map,
        plot_pie,
        plot_threshold_bars,
    )

    return (
        plot_bar,
        plot_hbar,
        plot_hbar_groups,
        plot_join_map,
        plot_pie,
        plot_threshold_bars,
    )


@app.cell
def _(mo):
    import duckdb

    # Open the database built from db_schema_and_records.sql
    # (see how_to_create_database.txt).
    # read_only=True: queries can read the tables, but nothing in
    # this notebook can change them.
    db_path = mo.notebook_dir() / "emps_depts_db.duckdb"
    if not db_path.exists():
        raise FileNotFoundError(
            f"{db_path} not found. Build it first:  "
            "duckdb emps_depts_db.duckdb < db_schema_and_records.sql"
        )
    con = duckdb.connect(database=str(db_path), read_only=True)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Employees & Departments: Learning SQL Joins

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### About This Database

    A small company keeps 2 tables:

    | Table | Rows | Columns | Links to |
    |-------|-----:|---------|----------|
    | `departments` | 4 | dept_id, dept_name | — |
    | `employees`   | 6 | emp_id, emp_name, salary, dept_id | `employees.dept_id` → `departments.dept_id` |

    `employees.dept_id` is a **foreign key**. It points to the
    **primary key** `departments.dept_id`. That shared column is
    what we join on.

    ```
    departments ──< employees
    (one department has many employees)
    ```

    The data is tiny on purpose, so you can check every answer by eye.
    It also has gaps on **both** sides:

    - **2 departments have no employees:** Sales (30) and Finance (40).
    - **2 employees have no department:** Diana and Jane (`dept_id` is `NULL`).

    These gaps are why `INNER`, `LEFT`, `RIGHT`, and `FULL` joins
    give *different* answers here. **Watch the row counts.**

    ### The Plan

    | Part | Queries | Focus |
    |------|---------|-------|
    | 1. Meet the data | V1–V2 | Look at each table |
    | 2. Aggregation | A1–A4 | COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING |
    | 3. INNER JOIN | J1–J3 | Only rows that match on both sides |
    | 4. LEFT JOIN | J4–J6 | Keep every row from the left table |
    | 5. RIGHT JOIN | J7–J8 | Keep every row from the right table |
    | 6. FULL JOIN | J9 | Keep every row from both tables |
    | 7. CROSS JOIN | J10 | Every row paired with every row |
    | 8. Finding the gaps | X1–X3 | Departments with no employees, employees with no department |
    | 9. Summary | S1 | Row counts of every join, side by side |

    Six queries (A2, A3, J6, J8, J9, S1) are followed by a chart. The
    plotting code lives in `plot_helpers.py`, so you can focus on
    the SQL.

    Every query cell is a **pure SQL cell**. The notebook opens
    `emps_depts_db.duckdb` in **read-only** mode, so you cannot break
    the data by accident.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 1 — Meet the Data

    Before you join tables, look at each one by itself.

    ## V1 — The `departments` table

    One row per department. `dept_id` is the **primary key**: no two
    departments share it. You should see **4 rows**.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM departments
        ORDER BY dept_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## V2 — The `employees` table

    One row per employee. `dept_id` says which department the
    employee works in. Look at **Diana** and **Jane**: their
    `dept_id` is `NULL` — they have not been assigned yet.
    You should see **6 rows**.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM employees
        ORDER BY emp_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 2 — Aggregation

    An **aggregate function** turns many rows into one value:
    `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. With `GROUP BY`, you get one
    value **per group** instead of one for the whole table.

    ## A1 — Company-wide salary summary

    No `GROUP BY`, so the whole table is one group → **1 row**.
    Expect 6 employees, a payroll of 450,000, and an average of 75,000.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*)              AS num_employees,
            SUM(salary)           AS total_payroll,
            ROUND(AVG(salary), 2) AS avg_salary,
            MIN(salary)           AS min_salary,
            MAX(salary)           AS max_salary
        FROM employees;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A2 — Headcount and payroll per `dept_id`

    `GROUP BY dept_id` makes one row per department id. Notice that
    `NULL` becomes **its own group**: Diana and Jane are counted
    together. We only see ids here, not names — we need a join for
    names (Part 3).
    """)
    return


@app.cell
def _(con, mo):
    df_headcount_by_id = mo.sql(
        f"""
        SELECT
            dept_id,
            COUNT(*)    AS num_employees,
            SUM(salary) AS total_salary
        FROM employees
        GROUP BY dept_id
        ORDER BY dept_id NULLS LAST;
        """,
        engine=con
    )
    return (df_headcount_by_id,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The pie shows how the 6 employees split across the 3 groups.
    The slices are equal: 2 employees each. The orange slice is the
    `NULL` group — **one third of the company has no department**.
    That is easy to miss in a table, and impossible to miss here.
    """)
    return


@app.cell
def _(df_headcount_by_id, plot_pie):
    plot_pie(df_headcount_by_id, labels="dept_id", values="num_employees",
             label_prefix="dept ", highlight="(NULL)",
             title="Employees per dept_id")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A3 — Filter groups with `HAVING`

    `WHERE` filters **rows** before grouping. `HAVING` filters
    **groups** after grouping.

    ### Step 1 — Without `HAVING`

    First, look at **every** group and its average salary.
    → **3 rows**: dept 10 (70,000), dept 20 (80,000), and the
    `NULL` group (75,000).
    """)
    return


@app.cell
def _(con, mo):
    df_avg_salary = mo.sql(
        f"""
        SELECT
            dept_id,
            COUNT(*)              AS num_employees,
            ROUND(AVG(salary), 2) AS avg_salary,
            MIN(salary)           AS min_salary,
            MAX(salary)           AS max_salary
        FROM employees
        GROUP BY dept_id
        ORDER BY avg_salary DESC;
        """,
        engine=con
    )
    return (df_avg_salary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The chart shows the Step 1 result. The red dashed line is the
    test we add in Step 2: `HAVING AVG(salary) > 72000`. Groups
    above the line will be **kept**; groups below it will be
    **dropped**.
    """)
    return


@app.cell
def _(df_avg_salary, plot_threshold_bars):
    plot_threshold_bars(df_avg_salary, labels="dept_id", values="avg_salary",
                        threshold=72000,
                        title="Average salary per dept_id — which groups pass HAVING?",
                        ylabel="average salary")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Step 2 — Add `HAVING`

    Same query, plus one line: `HAVING AVG(salary) > 72000`.
    It keeps only the groups whose average salary is above 72,000.

    Engineering (10) averages 70,000, so it is dropped →
    **2 rows**: dept 20 and the `NULL` group. Compare with Step 1.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            dept_id,
            COUNT(*)              AS num_employees,
            ROUND(AVG(salary), 2) AS avg_salary,
            MIN(salary)           AS min_salary,
            MAX(salary)           AS max_salary
        FROM employees
        GROUP BY dept_id
        HAVING AVG(salary) > 72000
        ORDER BY avg_salary DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A4 — `COUNT(*)` vs `COUNT(column)` vs `COUNT(DISTINCT column)`

    These three look alike but answer different questions:

    - `COUNT(*)` counts **rows** → 6
    - `COUNT(dept_id)` counts **non-NULL values** → 4
    - `COUNT(DISTINCT dept_id)` counts **different non-NULL values** → 2

    This difference matters a lot once we use `LEFT JOIN` (see J6).
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*)                AS all_rows,
            COUNT(dept_id)          AS with_department,
            COUNT(*) - COUNT(dept_id) AS without_department,
            COUNT(DISTINCT dept_id) AS distinct_departments
        FROM employees;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 3 — INNER JOIN

    `A INNER JOIN B ON A.key = B.key` keeps a row **only when it has
    a match on both sides**. Rows without a partner disappear.

    ## J1 — Employees with their department name

    Diana and Jane (no department) are dropped. Sales and Finance
    (no employees) are dropped. → **4 rows**.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            e.emp_id,
            e.emp_name,
            e.salary,
            d.dept_name
        FROM employees AS e
        INNER JOIN departments AS d
            ON e.dept_id = d.dept_id
        ORDER BY e.emp_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J2 — INNER JOIN plus `WHERE`

    Join first, then filter. Who earns at least 75,000 **and** has a
    department? → **3 rows**: Rafa, Bob, Charlie.
    Jane earns 80,000 but has no department, so the join already
    removed her.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            e.emp_name,
            e.salary,
            d.dept_name
        FROM employees AS e
        INNER JOIN departments AS d
            ON e.dept_id = d.dept_id
        WHERE e.salary >= 75000
        ORDER BY e.salary DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J3 — INNER JOIN plus `GROUP BY`

    Now we can group by department **name** instead of id.
    Only departments that have employees appear → **2 rows**.
    Compare with J6, which keeps every department.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            d.dept_name,
            COUNT(*)              AS num_employees,
            SUM(e.salary)         AS total_salary,
            ROUND(AVG(e.salary), 2) AS avg_salary
        FROM employees AS e
        INNER JOIN departments AS d
            ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY total_salary DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 4 — LEFT JOIN

    `A LEFT JOIN B` keeps **every row of A** (the left table).
    When a row of A has no match in B, the B columns are `NULL`.

    ## J4 — Every employee, with a department if they have one

    `employees` is on the left, so all **6** employees appear.
    Diana and Jane get `NULL` for `dept_name`.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            e.emp_id,
            e.emp_name,
            e.salary,
            d.dept_name
        FROM employees AS e
        LEFT JOIN departments AS d
            ON e.dept_id = d.dept_id
        ORDER BY e.emp_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J5 — Every department, with its employees

    Swap the order: `departments` is now on the left, so all 4
    departments appear. Engineering and Marketing show 2 rows each.
    Sales and Finance show once, with `NULL` employee columns.
    → **6 rows**, but a *different* 6 rows than J4.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            d.dept_id,
            d.dept_name,
            e.emp_name,
            e.salary
        FROM departments AS d
        LEFT JOIN employees AS e
            ON d.dept_id = e.dept_id
        ORDER BY d.dept_id, e.emp_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J6 — Headcount for **every** department (zeros included)

    A manager asks: "How many people are in each department?"
    They expect to see Sales and Finance with **0**, not missing.

    Two details make this right:

    - `COUNT(e.emp_id)`, not `COUNT(*)`. `COUNT(*)` would count the
      `NULL` row and report 1 for Sales.
    - `COALESCE(SUM(e.salary), 0)` turns a `NULL` total into 0.

    → **4 rows**.
    """)
    return


@app.cell
def _(con, mo):
    df_headcount = mo.sql(
        f"""
        SELECT
            d.dept_name,
            COUNT(e.emp_id)            AS num_employees,
            COALESCE(SUM(e.salary), 0) AS total_salary
        FROM departments AS d
        LEFT JOIN employees AS e
            ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
        ORDER BY num_employees DESC, d.dept_name;
        """,
        engine=con
    )
    return (df_headcount,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The `LEFT JOIN` keeps Sales and Finance, so they appear on the
    chart as dashed **0** bars. With an `INNER JOIN` (J3), these two
    bars would be missing — and a missing bar is easy to overlook.
    """)
    return


@app.cell
def _(df_headcount, plot_bar):
    plot_bar(df_headcount, labels="dept_name", values="num_employees",
             title="Employees per department (LEFT JOIN keeps all 4)",
             ylabel="number of employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 5 — RIGHT JOIN

    `A RIGHT JOIN B` keeps **every row of B** (the right table).
    It is a mirror of LEFT JOIN: `A RIGHT JOIN B` gives the same rows
    as `B LEFT JOIN A`. Most people write LEFT JOIN, but you must be
    able to read both.

    ## J7 — Every department, written as a RIGHT JOIN

    `departments` is on the right, so every department is kept.
    Same **6 rows** as J5.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            d.dept_id,
            d.dept_name,
            e.emp_name,
            e.salary
        FROM employees AS e
        RIGHT JOIN departments AS d
            ON e.dept_id = d.dept_id
        ORDER BY d.dept_id, e.emp_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J8 — Every employee, written as a RIGHT JOIN

    Now `employees` is on the right, so every employee is kept.
    Same **6 rows** as J4. This time `COALESCE` replaces the
    `NULL` department name with a friendly label.
    """)
    return


@app.cell
def _(con, mo):
    df_emp_salaries = mo.sql(
        f"""
        SELECT
            e.emp_id,
            e.emp_name,
            e.salary,
            COALESCE(d.dept_name, '(no department)') AS dept_name
        FROM departments AS d
        RIGHT JOIN employees AS e
            ON d.dept_id = e.dept_id
        ORDER BY e.emp_id;
        """,
        engine=con
    )
    return (df_emp_salaries,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Every employee is on the chart, colored by department. Diana and
    Jane are in orange: the `RIGHT JOIN` kept them, and `COALESCE`
    gave them a label. Jane is the second-highest earner — an
    `INNER JOIN` would have hidden her.
    """)
    return


@app.cell
def _(df_emp_salaries, plot_hbar_groups):
    plot_hbar_groups(df_emp_salaries, labels="emp_name", values="salary",
                     groups="dept_name", highlight="(no department)",
                     title="Salary of every employee, by department",
                     xlabel="salary")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 6 — FULL OUTER JOIN

    `A FULL JOIN B` keeps **every row of A and every row of B**.
    Matches are paired up. Rows without a partner still appear,
    with `NULL` on the missing side.

    ## J9 — Everyone and everything

    4 matched rows + 2 employees with no department + 2 departments
    with no employees → **8 rows**.
    """)
    return


@app.cell
def _(con, mo):
    df_full_join = mo.sql(
        f"""
        SELECT
            e.emp_id,
            e.emp_name,
            e.dept_id AS emp_dept_id,
            d.dept_id AS dept_dept_id,
            d.dept_name
        FROM employees AS e
        FULL OUTER JOIN departments AS d
            ON e.dept_id = d.dept_id
        ORDER BY d.dept_id NULLS LAST, e.emp_id NULLS LAST;
        """,
        engine=con
    )
    return (df_full_join,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The same 8 rows as a picture. Each **blue line** is one matched
    row (4 lines). Each **orange name** is a row with `NULL` on the
    other side: 2 employees on the left, 2 departments on the right.

    This one picture shows all the joins:

    - `INNER JOIN` = only the lines
    - `employees LEFT JOIN departments` = the lines + the orange employees
    - `departments LEFT JOIN employees` = the lines + the orange departments
    - `FULL OUTER JOIN` = everything
    """)
    return


@app.cell
def _(df_full_join, plot_join_map):
    plot_join_map(df_full_join, left="emp_name", right="dept_name",
                  left_title="employees", right_title="departments",
                  title="FULL OUTER JOIN: who matches whom")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 7 — CROSS JOIN

    `A CROSS JOIN B` has **no `ON` clause**. It pairs every row of A
    with every row of B. This is called the **Cartesian product**.
    Row count = rows in A × rows in B.

    ## J10 — Every employee paired with every department

    6 employees × 4 departments → **24 rows**. Useful for building
    "every combination" lists (for example, a planning grid).
    Dangerous by accident: forget the `ON` clause on two big tables
    and you get millions of rows.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            e.emp_name,
            d.dept_name
        FROM employees AS e
        CROSS JOIN departments AS d
        ORDER BY e.emp_name, d.dept_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 8 — Finding the Gaps

    A very common business question is "what is **missing**?"
    The pattern is: **outer join, then keep only the rows where the
    other side is `NULL`.**

    ## X1 — Which departments have no employees?

    `departments LEFT JOIN employees`, then keep rows where no
    employee matched (`e.emp_id IS NULL`).
    → **2 rows**: Sales and Finance.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            d.dept_id,
            d.dept_name
        FROM departments AS d
        LEFT JOIN employees AS e
            ON d.dept_id = e.dept_id
        WHERE e.emp_id IS NULL
        ORDER BY d.dept_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## X2 — Which employees have no department?

    The same pattern, other direction: `employees LEFT JOIN
    departments`, then keep rows where no department matched
    (`d.dept_id IS NULL`).
    → **2 rows**: Diana and Jane.

    Why test `d.dept_id` and not `e.dept_id`? Testing the **other**
    table's key also catches an employee whose `dept_id` points to a
    department that does not exist. (The foreign key prevents that
    here, but in real data it happens.)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            e.emp_id,
            e.emp_name,
            e.salary,
            e.dept_id
        FROM employees AS e
        LEFT JOIN departments AS d
            ON e.dept_id = d.dept_id
        WHERE d.dept_id IS NULL
        ORDER BY e.emp_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## X3 — Both kinds of gaps in one query

    A `FULL JOIN` keeps unmatched rows from **both** sides. Keep only
    the rows where one side is `NULL`, and label which kind of gap
    each row is. → **4 rows**: X1 and X2 together.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            CASE
                WHEN e.emp_id IS NULL THEN 'Department with no employees'
                ELSE 'Employee with no department'
            END AS gap_type,
            d.dept_name,
            e.emp_name
        FROM employees AS e
        FULL OUTER JOIN departments AS d
            ON e.dept_id = d.dept_id
        WHERE e.emp_id IS NULL
           OR d.dept_id IS NULL
        ORDER BY gap_type, d.dept_name, e.emp_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 9 — Summary

    ## S1 — Row counts of every join type, side by side

    Same two tables, same `ON` condition — only the join type
    changes. The row count tells the story:

    - INNER = matches only (4)
    - LEFT / RIGHT = matches + unmatched rows from one side (6)
    - FULL = matches + unmatched rows from both sides (8)
    - CROSS = every pair (24)
    """)
    return


@app.cell
def _(con, mo):
    df_join_counts = mo.sql(
        f"""
        SELECT 'INNER JOIN' AS join_type, COUNT(*) AS row_count
        FROM employees AS e INNER JOIN departments AS d ON e.dept_id = d.dept_id
        UNION ALL
        SELECT 'employees LEFT JOIN departments', COUNT(*)
        FROM employees AS e LEFT JOIN departments AS d ON e.dept_id = d.dept_id
        UNION ALL
        SELECT 'departments LEFT JOIN employees', COUNT(*)
        FROM departments AS d LEFT JOIN employees AS e ON d.dept_id = e.dept_id
        UNION ALL
        SELECT 'employees RIGHT JOIN departments', COUNT(*)
        FROM employees AS e RIGHT JOIN departments AS d ON e.dept_id = d.dept_id
        UNION ALL
        SELECT 'FULL OUTER JOIN', COUNT(*)
        FROM employees AS e FULL OUTER JOIN departments AS d ON e.dept_id = d.dept_id
        UNION ALL
        SELECT 'CROSS JOIN', COUNT(*)
        FROM employees AS e CROSS JOIN departments AS d;
        """,
        engine=con
    )
    return (df_join_counts,)


@app.cell
def _(df_join_counts, plot_hbar):
    plot_hbar(df_join_counts, labels="join_type", values="row_count",
              title="Same two tables, different joins: how many rows?",
              xlabel="number of rows")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ### Cheat Sheet

    | You want… | Write |
    |-----------|-------|
    | only rows that match on both sides | `A INNER JOIN B ON …` |
    | every row of A, matched or not | `A LEFT JOIN B ON …` |
    | every row of B, matched or not | `A RIGHT JOIN B ON …` (= `B LEFT JOIN A`) |
    | every row of A and of B | `A FULL OUTER JOIN B ON …` |
    | every pair of rows | `A CROSS JOIN B` (no `ON`) |
    | rows of A with **no** match in B | `A LEFT JOIN B ON … WHERE B.key IS NULL` |
    | count matches, 0 when none | `COUNT(B.key)`, not `COUNT(*)` |

    ### Try It Yourself

    1. List each department with its **highest-paid** employee's salary.
       Show Sales and Finance with `NULL`. (INNER or LEFT?)
    2. Rewrite X1 as a `RIGHT JOIN`. Check that you still get 2 rows.
    3. Show every employee with their department name; use
       `COALESCE` to show `'Unassigned'` when there is none.
    4. What is the average salary of employees **with** a department,
       versus **without** one? (Hint: `CASE` + `GROUP BY`.)
    5. Add `WHERE d.dept_name = 'Sales'` to J4. Why do you get
       0 rows? Move the test into the `ON` clause and compare.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
