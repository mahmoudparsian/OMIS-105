import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from plot_helpers import (
        plot_bar,
        plot_before_after,
        plot_group_map,
        plot_hbar,
        plot_heatmap,
        plot_pie,
        plot_range,
        plot_stacked_bars,
        plot_threshold_bars,
    )

    return (
        plot_bar,
        plot_before_after,
        plot_group_map,
        plot_hbar,
        plot_heatmap,
        plot_pie,
        plot_range,
        plot_stacked_bars,
        plot_threshold_bars,
    )


@app.cell
def _(mo):
    import duckdb

    # Open the database built from db_schema_and_records.sql
    # (see how_to_create_duckdb_database.txt).
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
    # OMIS 105 — Learning `GROUP BY` with Employees & Departments

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### Why `GROUP BY` matters

    A manager rarely asks about **one** employee. They ask about
    **groups**:

    - *How many people work in each department?*
    - *What is the average salary for each job title?*
    - *Which departments spend the most on payroll?*

    Every one of these questions is a `GROUP BY` query. It is one of
    the most useful tools in SQL — and this notebook is your guide
    to it, step by step.

    ### About This Database

    A small company keeps 2 tables:

    | Table | Rows | Columns | Links to |
    |-------|-----:|---------|----------|
    | `departments` | 5 | dept_id, dept_name | — |
    | `employees`   | 13 | emp_id, emp_name, job_title, salary, dept_id | `employees.dept_id` → `departments.dept_id` |

    ```
    departments ──< employees
    (one department has many employees)
    ```

    The data is small on purpose, so you can check every answer by
    eye. Two things to watch for:

    - Two columns are good for grouping: **`dept_id`** (3 values are
      used) and **`job_title`** (4 values).
    - **Finance (40)** and **IT (50)** have **no employees**. We find
      them at the end.

    ### The Plan

    | Part | Queries | Focus |
    |------|---------|-------|
    | 1. Meet the data | B1–B4 | Look at the tables; stats for the whole table |
    | 2. `GROUP BY` | G1–G8 | From basic to advanced: one column, two columns, `WHERE`, `HAVING`, pivot |
    | 3. Joins + `GROUP BY` | J1–J4 | Show department **names**, not numbers |
    | 4. Finding the gap | X1 | Which departments have no employees? |

    Many queries are followed by a chart. The plotting code lives in
    `plot_helpers.py`, so you can focus on the SQL. Colors stay the
    same everywhere: **dept 10 is always blue**, **Engineer is always
    blue**, and so on.

    Many queries also use **`GROUP_CONCAT`**. It lists the rows inside
    each group, so you can **see** what the aggregate function is
    working on.

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

    Before you group anything, look at the raw rows. You cannot judge
    a summary if you have never seen the details.

    ## B1 — The `departments` table

    One row per department. `dept_id` is the **primary key**: no two
    departments share it. You should see **5 rows**.
    """)
    return


@app.cell
def _(con, departments, mo):
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
    ## B2 — The `employees` table

    One row per employee. `dept_id` is a **foreign key**: it says
    which department the employee works in. You should see
    **13 rows**.

    Look at the `dept_id` and `job_title` columns. The same values
    repeat again and again. **Repeating values are what we group on.**
    """)
    return


@app.cell
def _(con, employees, mo):
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
    ## B3 — Statistics for the whole company

    An **aggregate function** turns many rows into **one** value:

    | Function | Returns |
    |----------|---------|
    | `COUNT(*)` | the number of rows |
    | `COUNT(DISTINCT col)` | the number of different values |
    | `SUM(col)` | the total |
    | `AVG(col)` | the average (mean) |
    | `MIN(col)` / `MAX(col)` | the smallest / largest value |

    There is no `GROUP BY` here, so the **whole table is one big
    group** → the answer is **1 row**. Expect 13 employees, a payroll
    of 1,400,000, and an average of about 107,692.
    """)
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*)                  AS employees,
            COUNT(DISTINCT dept_id)   AS departments_used,
            COUNT(DISTINCT job_title) AS job_titles,
            SUM(salary)               AS total_payroll,
            ROUND(AVG(salary), 2)     AS avg_salary,
            MIN(salary)               AS min_salary,
            MAX(salary)               AS max_salary
        FROM employees;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## B4 — Sort by `dept_id`: spot the groups with your eyes

    Sorting is **not** grouping — we still get all 13 rows. But when
    rows with the same `dept_id` sit next to each other, the groups
    jump out: 7 rows for dept 10, 4 for dept 20, 2 for dept 30.

    `GROUP BY` does exactly this, and then goes one step further: it
    **collapses each group into a single row**.
    """)
    return


@app.cell
def _(con, employees, mo):
    df_sorted = mo.sql(
        f"""
        SELECT
            dept_id,
            emp_name,
            job_title,
            salary
        FROM employees
        ORDER BY dept_id, salary DESC, emp_name;
        """,
        engine=con
    )
    return (df_sorted,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### The big idea, as a picture

    On the left: the 13 rows from B4. On the right: the 3 groups that
    `GROUP BY dept_id` makes. Each line shows which group a row
    falls into. **Many rows go in, one row per group comes out.**
    """)
    return


@app.cell
def _(df_sorted, plot_group_map):
    plot_group_map(df_sorted, item="emp_name", group="dept_id",
                   value="salary", group_prefix="dept_id = ",
                   title="What GROUP BY dept_id does",
                   subtitle="13 employee rows collapse into 3 department rows")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 2 — `GROUP BY`, Step by Step

    ### How `GROUP BY` works: split → apply → combine

    Take dept 20 (Marketing) as an example:

    ```
    1. SPLIT    put rows with the same dept_id in one pile
                dept 20 pile:  Barbara 170000 | Charlie 70000 | Dara 80000 | Jeff 80000

    2. APPLY    run each aggregate function on the pile
                COUNT(*)    = 4
                SUM(salary) = 170000 + 70000 + 80000 + 80000 = 400000
                AVG(salary) = 400000 / 4 = 100000

    3. COMBINE  write one result row per pile
                dept_id = 20 | employees = 4 | total = 400000 | avg = 100000
    ```

    ### The golden rule of `GROUP BY`

    > Every column in `SELECT` must be **either** in the `GROUP BY`
    > **or** inside an aggregate function.

    Why? After grouping, there is only **one row** per department.
    A department has one `dept_id`, but it has many `emp_name`s — SQL
    cannot fit 4 names into 1 cell… **unless** you ask it to join
    them into one string. That is what `GROUP_CONCAT` does.

    ### `GROUP_CONCAT` — see inside each group

    `GROUP_CONCAT(emp_name, ', ')` is an aggregate function that
    glues every value in the group into one text string. We use it
    as an **x-ray**: it shows exactly which rows each group holds.

    ```sql
    GROUP_CONCAT(emp_name, ', ' ORDER BY emp_name)   -- sorted list
    ```

    `GROUP_CONCAT` comes from MySQL and SQLite. The SQL standard name
    is `STRING_AGG`. DuckDB accepts both.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## G1 — Headcount per department  *(basic)*

    The simplest `GROUP BY`: one column, one count.
    `GROUP BY dept_id` → **3 rows**, one per `dept_id` that has
    employees. The `members` column shows who is in each group, so
    you can check the count yourself.
    """)
    return


@app.cell
def _(con, employees, mo):
    df_dept_headcount = mo.sql(
        f"""
        SELECT
            dept_id,
            COUNT(*)                                     AS employees,
            GROUP_CONCAT(emp_name, ', ' ORDER BY emp_name) AS members,
            LIST(emp_name)
        FROM employees
        GROUP BY dept_id
        ORDER BY dept_id;
        """,
        engine=con
    )
    return (df_dept_headcount,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The donut shows each department's **share** of the company.
    More than half of all employees (7 of 13) work in dept 10.
    """)
    return


@app.cell
def _(df_dept_headcount, plot_pie):
    plot_pie(df_dept_headcount, labels="dept_id", values="employees",
             label_prefix="dept ", center_text="13\nemployees",
             title="G1 · Employees per department",
             subtitle="COUNT(*) ... GROUP BY dept_id")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Common mistake: breaking the golden rule

    What if we ask for `emp_name` **without** an aggregate?

    ```sql
    SELECT dept_id, emp_name, COUNT(*)
    FROM employees
    GROUP BY dept_id;
    ```

    Dept 20 has 4 names, but the result has only 1 row for dept 20.
    Which name should SQL show? It cannot choose, so it stops with an
    error. The cell below runs this query and shows you the real
    error message. **Learn to recognize it** — you will see it often.
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    try:
        con.execute("""
            SELECT dept_id, emp_name, COUNT(*)
            FROM employees
            GROUP BY dept_id
        """)
        _out = mo.callout(mo.md("The query ran (unexpected)."), kind="warn")
    except Exception as err:
        _out = mo.callout(
            mo.md(
                f"**DuckDB refused the query:**\n\n`{err}`\n\n"
                "**The fix:** put `emp_name` inside an aggregate, such as "
                "`GROUP_CONCAT(emp_name, ', ')`, or add it to the "
                "`GROUP BY`."
            ),
            kind="danger",
        )
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## G2 — Headcount per job title  *(basic)*

    Same idea, a different column. `GROUP BY job_title` → **4 rows**.
    We sort by the count, biggest first, and break ties by name.
    """)
    return


@app.cell
def _(con, employees, mo):
    df_job_headcount = mo.sql(
        f"""
        SELECT
            job_title,
            COUNT(*)                                     AS employees,
            GROUP_CONCAT(emp_name, ', ' ORDER BY emp_name) AS members
        FROM employees
        GROUP BY job_title
        ORDER BY employees DESC, job_title;
        """,
        engine=con
    )
    return (df_job_headcount,)


@app.cell
def _(df_job_headcount, plot_pie):
    plot_pie(df_job_headcount, labels="job_title", values="employees",
             center_text="4\njob titles",
             title="G2 · Employees per job title",
             subtitle="COUNT(*) ... GROUP BY job_title")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## G3 — Salary statistics per department  *(basic → intermediate)*

    One `GROUP BY` can feed **many** aggregate functions at once.
    Each one is computed over the **same** group of rows.

    The `salaries` column lists every salary in the group, from low
    to high. Check it: the first value is the `MIN`, the last is the
    `MAX`.
    """)
    return


@app.cell
def _(con, employees, mo):
    df_dept_salary = mo.sql(
        f"""
        SELECT
            dept_id,
            COUNT(*)                                   AS employees,
            SUM(salary)                                AS total_payroll,
            ROUND(AVG(salary), 2)                      AS avg_salary,
            MIN(salary)                                AS min_salary,
            MAX(salary)                                AS max_salary,
            GROUP_CONCAT(salary, ', ' ORDER BY salary) AS salaries
        FROM employees
        GROUP BY dept_id
        ORDER BY dept_id;
        """,
        engine=con
    )
    return (df_dept_salary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The **range chart** shows three aggregates in one picture: the
    line runs from `MIN` to `MAX`, and the diamond marks the `AVG`.
    Dept 30 has the highest average (130K) but only 2 people — one
    of them a VP. **Small groups can swing an average a lot.**
    """)
    return


@app.cell
def _(df_dept_salary, plot_range):
    plot_range(df_dept_salary, labels="dept_id", low="min_salary",
               mid="avg_salary", high="max_salary", label_prefix="dept ",
               title="G3 · Salary range per department",
               subtitle="MIN (left dot), AVG (diamond), MAX (right dot)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## G4 — Payroll per job title, and its share of the total  *(intermediate)*

    Here `GROUP_CONCAT` shows **how `SUM` works**: we glue the
    salaries together with `' + '`, so the `how_sum_works` column is
    the exact sum that SQL computes.

    The share column divides each group's total by the company total.
    The company total comes from a small **subquery** in parentheses:
    `(SELECT SUM(salary) FROM employees)` = 1,400,000.
    """)
    return


@app.cell
def _(con, employees, mo):
    df_job_payroll = mo.sql(
        f"""
        SELECT
            job_title,
            COUNT(*)                                    AS employees,
            GROUP_CONCAT(salary, ' + ' ORDER BY salary) AS how_sum_works,
            SUM(salary)                                 AS total_payroll,
            ROUND(100.0 * SUM(salary)
                  / (SELECT SUM(salary) FROM employees), 1) AS pct_of_payroll
        FROM employees
        GROUP BY job_title
        ORDER BY total_payroll DESC;
        """,
        engine=con
    )
    return (df_job_payroll,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Compare this donut with G2. VPs are only **3 of 13** employees
    (23%), but they take **35%** of the payroll. Counting people and
    summing money tell two different stories.
    """)
    return


@app.cell
def _(df_job_payroll, plot_pie):
    plot_pie(df_job_payroll, labels="job_title", values="total_payroll",
             money=True, center_text="$1.4M\npayroll",
             title="G4 · Where the payroll goes, by job title",
             subtitle="SUM(salary) ... GROUP BY job_title")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## G5 — `WHERE` + `GROUP BY`: filter rows first  *(intermediate)*

    *How many employees in each department earn **at least
    100,000**?*

    `WHERE` runs **before** `GROUP BY`. It throws away rows first, and
    only the surviving rows are grouped. So the 8 employees under
    100,000 never reach a group at all → 5 rows are grouped into
    **3 rows**.

    Note: if **every** row of a department failed the `WHERE` test,
    that department would disappear from the result completely.
    """)
    return


@app.cell
def _(con, employees, mo):
    df_high_earners = mo.sql(
        f"""
        SELECT
            dept_id,
            COUNT(*)                                       AS high_earners,
            GROUP_CONCAT(emp_name, ', ' ORDER BY emp_name) AS members
        FROM employees
        WHERE salary >= 100000
        GROUP BY dept_id
        ORDER BY dept_id;
        """,
        engine=con
    )
    return (df_high_earners,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Each department gets two bars. The dashed bar is the headcount
    from G1 (all rows). The solid bar is what is left after `WHERE`.
    """)
    return


@app.cell
def _(df_dept_headcount, df_high_earners, plot_before_after):
    plot_before_after(df_dept_headcount, df_high_earners, labels="dept_id",
                      before="employees", after="high_earners",
                      label_prefix="dept ",
                      after_label="salary >= 100,000 (kept by WHERE)",
                      title="G5 · WHERE removes rows before grouping",
                      subtitle="Headcount per department: all employees vs. high earners")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## G6 — `HAVING`: filter groups after  *(intermediate)*

    *Which job titles have an **average** salary above 100,000?*

    You **cannot** write `WHERE AVG(salary) > 100000`. `WHERE` looks
    at one row at a time, and the average does not exist yet. To test
    an aggregate, use **`HAVING`**. It runs **after** `GROUP BY` and
    keeps or drops whole groups.

    **Step 1 — without `HAVING`.** First, look at all 4 groups:
    """)
    return


@app.cell
def _(con, employees, mo):
    df_job_avg = mo.sql(
        f"""
        SELECT
            job_title,
            COUNT(*)              AS employees,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY job_title
        ORDER BY avg_salary DESC;
        """,
        engine=con
    )
    return (df_job_avg,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The dashed line is the `HAVING` test. Groups whose bar is above
    the line are **kept**. Groups below it are **dropped**.
    """)
    return


@app.cell
def _(df_job_avg, plot_threshold_bars):
    plot_threshold_bars(df_job_avg, labels="job_title", values="avg_salary",
                        threshold=100000, money=True, ylabel="average salary",
                        title="G6 · HAVING keeps or drops whole groups",
                        subtitle="AVG(salary) per job title vs. the HAVING test")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Step 2 — with `HAVING`.** Add one line, and only the groups
    above the line remain → **2 rows**: VP and Salesperson.
    """)
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        SELECT
            job_title,
            COUNT(*)                                       AS employees,
            ROUND(AVG(salary), 2)                          AS avg_salary,
            GROUP_CONCAT(emp_name, ', ' ORDER BY emp_name) AS members
        FROM employees
        GROUP BY job_title
        HAVING AVG(salary) > 100000
        ORDER BY avg_salary DESC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        SELECT
            job_title,
            COUNT(*)                                       AS employees,
            ROUND(AVG(salary), 2)                          AS avg_salary,
            GROUP_CONCAT(emp_name, ', ' ORDER BY emp_name) AS members
        FROM employees
        GROUP BY job_title
        HAVING avg_salary > 100000
        ORDER BY avg_salary DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### `WHERE` vs. `HAVING` — the order SQL works in

    You **write** a query in one order, but SQL **runs** it in
    another:

    ```
      FROM employees              1. take the table
      WHERE salary >= 100000      2. filter ROWS        (G5)
      GROUP BY dept_id            3. make groups
      HAVING COUNT(*) > 1         4. filter GROUPS      (G6)
      SELECT dept_id, COUNT(*)    5. compute the output columns
      ORDER BY dept_id            6. sort the result
    ```

    | | `WHERE` | `HAVING` |
    |---|---|---|
    | Filters | rows | groups |
    | Runs | before `GROUP BY` | after `GROUP BY` |
    | Can use aggregates? | **no** | **yes** |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## G7 — `GROUP BY` two columns  *(advanced)*

    *How many of each job title work in each department?*

    `GROUP BY dept_id, job_title` makes one group for each
    **combination** of the two columns that exists in the data. The
    rows match only if **both** values match. → **7 rows**.

    Dept 10 splits into 3 groups (Engineer, Salesperson, VP).
    There is no "dept 30 + Engineer" row: no such employee exists,
    so no group is made.
    """)
    return


@app.cell
def _(con, employees, mo):
    df_dept_job = mo.sql(
        f"""
        SELECT
            dept_id,
            job_title,
            COUNT(*)                                       AS employees,
            SUM(salary)                                    AS total_payroll,
            GROUP_CONCAT(emp_name, ', ' ORDER BY emp_name) AS members
        FROM employees
        GROUP BY dept_id, job_title
        ORDER BY dept_id, job_title;
        """,
        engine=con
    )
    return (df_dept_job,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Each bar is one department (G1). Each colored piece is one row of
    G7. The pieces add up to the G1 headcount: the two-column groups
    are **smaller pieces of** the one-column groups.
    """)
    return


@app.cell
def _(df_dept_job, plot_stacked_bars):
    plot_stacked_bars(df_dept_job, x="dept_id", stack="job_title",
                      values="employees", label_prefix="dept ",
                      ylabel="employees",
                      title="G7 · Job titles inside each department",
                      subtitle="COUNT(*) ... GROUP BY dept_id, job_title")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## G8 — Conditional aggregation: a pivot table  *(advanced)*

    G7 gave us a **long** result: one row per (dept, job) pair. A
    manager often wants a **wide** one instead: one row per
    department, one **column** per job title. This is called a
    **pivot table**.

    The trick is a `CASE` expression **inside** `SUM`:

    ```sql
    SUM(CASE WHEN job_title = 'VP' THEN salary END)
    ```

    For each row, the `CASE` gives the salary if the row is a VP, and
    `NULL` otherwise. `SUM` skips `NULL`s, so it adds up **only the VP
    salaries** in that department. Repeat it once per job title.

    A `NULL` cell in the result means *"this department has no one
    with that job title"*.
    """)
    return


@app.cell
def _(con, employees, mo):
    df_pivot = mo.sql(
        f"""
        SELECT
            dept_id,
            SUM(CASE WHEN job_title = 'Engineer'    THEN salary END) AS Engineer,
            SUM(CASE WHEN job_title = 'Marketer'    THEN salary END) AS Marketer,
            SUM(CASE WHEN job_title = 'Salesperson' THEN salary END) AS Salesperson,
            SUM(CASE WHEN job_title = 'VP'          THEN salary END) AS VP,
            SUM(salary)                                              AS total_payroll
        FROM employees
        GROUP BY dept_id
        ORDER BY dept_id;
        """,
        engine=con
    )
    return (df_pivot,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The heatmap draws the pivot table: darker cells hold more money.
    Each row adds up to the `total_payroll` column. Notice that every
    department pays a VP, but the VP's share is very different: about
    19% of payroll in dept 10, but 69% in dept 30.
    """)
    return


@app.cell
def _(df_pivot, plot_heatmap):
    plot_heatmap(df_pivot, row_label="dept_id",
                 columns=["Engineer", "Marketer", "Salesperson", "VP"],
                 label_prefix="dept ",
                 title="G8 · Payroll by department and job title",
                 subtitle="SUM(CASE WHEN job_title = ... THEN salary END) ... GROUP BY dept_id")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **DuckDB shortcut:** `SUM(salary) FILTER (WHERE job_title = 'VP')`
    > does the same as the `CASE` version. The `CASE` version works in
    > every database, so learn it first.

    ---
    # Part 3 — Joins + `GROUP BY`

    So far our groups have **numbers** (10, 20, 30). A report needs
    **names** (Engineering, Marketing, Sales). The names live in the
    `departments` table, so we **join** the two tables on the column
    they share: `dept_id`.

    ```sql
    FROM employees AS e
    INNER JOIN departments AS d
        ON e.dept_id = d.dept_id
    ```

    `e` and `d` are **aliases** — short nicknames for the tables.
    `e.dept_id` means "the `dept_id` column of `employees`".

    ## J1 — Every employee with their department name

    `INNER JOIN` keeps only rows that match on **both** sides. Every
    employee has a valid `dept_id`, so → **13 rows**.
    """)
    return


@app.cell
def _(con, departments, employees, mo):
    _df = mo.sql(
        f"""
        SELECT
            e.emp_id,
            e.emp_name,
            e.job_title,
            e.salary,
            d.dept_name
        FROM employees AS e
        INNER JOIN departments AS d
            ON e.dept_id = d.dept_id
        ORDER BY d.dept_name, e.emp_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J2 — Join + `WHERE`: everyone in Marketing

    After the join, `dept_name` is a column like any other, so we can
    filter on it. We no longer need to remember that Marketing is
    dept 20. → **4 rows**.
    """)
    return


@app.cell
def _(con, departments, employees, mo):
    _df = mo.sql(
        f"""
        SELECT
            e.emp_name,
            e.job_title,
            e.salary,
            d.dept_name
        FROM employees AS e
        INNER JOIN departments AS d
            ON e.dept_id = d.dept_id
        WHERE d.dept_name = 'Marketing'
        ORDER BY e.salary DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J3 — Join + `GROUP BY`: average salary per department **name**

    This is G3 again, now with names. SQL joins first, then groups:
    the join (`FROM` … `JOIN`) is step 1 of the order of operations.
    → **3 rows**.
    """)
    return


@app.cell
def _(con, departments, employees, mo):
    df_dept_names = mo.sql(
        f"""
        SELECT
            d.dept_name,
            COUNT(*)                                         AS employees,
            ROUND(AVG(e.salary), 2)                          AS avg_salary,
            GROUP_CONCAT(e.emp_name, ', ' ORDER BY e.emp_name) AS members
        FROM employees AS e
        INNER JOIN departments AS d
            ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY avg_salary DESC;
        """,
        engine=con
    )
    return (df_dept_names,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The dashed line is the company-wide average from B3 (107,692).
    Only Sales is above it.
    """)
    return


@app.cell
def _(df_dept_names, plot_hbar):
    plot_hbar(df_dept_names, labels="dept_name", values="avg_salary",
              money=True, xlabel="average salary",
              reference=107692.31, reference_label="company average",
              title="J3 · Average salary per department",
              subtitle="AVG(e.salary) ... JOIN departments ... GROUP BY d.dept_name")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J4 — `LEFT JOIN` + `GROUP BY`: headcount for **every** department

    J3 showed only 3 departments. Finance and IT are missing, because
    `INNER JOIN` drops a department with no matching employee.

    A **`LEFT JOIN`** keeps **every** row of the left table
    (`departments`), even with no match. For Finance and IT, the
    employee columns are filled with `NULL`. → **5 rows**.

    ### Watch out: `COUNT(*)` vs. `COUNT(e.emp_id)`

    - `COUNT(*)` counts **rows**. Finance has 1 row (full of `NULL`s),
      so `COUNT(*)` says **1** — wrong!
    - `COUNT(e.emp_id)` counts **non-`NULL` values**. Finance's
      `emp_id` is `NULL`, so it says **0** — right!

    The query shows both, so you can compare.
    """)
    return


@app.cell
def _(con, departments, employees, mo):
    df_all_depts = mo.sql(
        f"""
        SELECT
            d.dept_id,
            d.dept_name,
            COUNT(e.emp_id)                                    AS employees,
            COUNT(*)                                           AS count_star_wrong,
            COALESCE(SUM(e.salary), 0)                         AS total_payroll,
            GROUP_CONCAT(e.emp_name, ', ' ORDER BY e.emp_name) AS members
        FROM departments AS d
        LEFT JOIN employees AS e
            ON d.dept_id = e.dept_id
        GROUP BY d.dept_id, d.dept_name
        ORDER BY d.dept_id;
        """,
        engine=con
    )
    return (df_all_depts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    `COALESCE(SUM(e.salary), 0)` turns a `NULL` total into `0`.
    `GROUP_CONCAT` of no names is `NULL` (an empty cell).

    In the chart, Finance and IT show as dashed "0 — none" bars: they
    are in the result **because of** the `LEFT JOIN`.
    """)
    return


@app.cell
def _(df_all_depts, plot_bar):
    plot_bar(df_all_depts, labels="dept_name", values="employees",
             ylabel="employees",
             title="J4 · Employees in every department",
             subtitle="COUNT(e.emp_id) ... departments LEFT JOIN employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 4 — Finding the Gap

    ## X1 — Which departments have no employees?

    Start from J4's `LEFT JOIN`. A department with no employees has
    `NULL` in **every** employee column. So keep only those rows:
    `WHERE e.emp_id IS NULL`. → **2 rows**: Finance and IT.

    Use `IS NULL`, never `= NULL`. Nothing is ever *equal* to `NULL`,
    so `= NULL` always returns 0 rows.
    """)
    return


@app.cell
def _(con, departments, employees, mo):
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
    > **Another way, with `GROUP BY`:** group J4's join by department
    > and keep the groups whose count is 0:
    >
    > ```sql
    > SELECT d.dept_id, d.dept_name
    > FROM departments AS d
    > LEFT JOIN employees AS e ON d.dept_id = e.dept_id
    > GROUP BY d.dept_id, d.dept_name
    > HAVING COUNT(e.emp_id) = 0;
    > ```
    >
    > Same 2 rows. (With `COUNT(*)` it would return **0 rows** — do you
    > see why?)

    ---
    # Summary

    ### Cheat Sheet

    | You want… | Write |
    |-----------|-------|
    | one number for the whole table | `SELECT COUNT(*), AVG(salary) FROM t` |
    | one row per group | `… GROUP BY col` |
    | one row per **combination** | `… GROUP BY col1, col2` |
    | to see the rows in each group | `GROUP_CONCAT(col, ', ')` (= `STRING_AGG`) |
    | to filter **rows** before grouping | `WHERE …` |
    | to filter **groups** after grouping | `HAVING aggregate …` |
    | one column per category (pivot) | `SUM(CASE WHEN … THEN col END)` |
    | names instead of ids | `JOIN` the lookup table, then `GROUP BY` the name |
    | groups with 0 members | `LEFT JOIN` + `COUNT(right.key)`, not `COUNT(*)` |

    ### Five things to remember

    1. **The golden rule:** every `SELECT` column is in the `GROUP BY`
       or inside an aggregate.
    2. `GROUP BY` returns **one row per group** — count your groups
       before you run the query, and check the row count after.
    3. `WHERE` filters rows (before). `HAVING` filters groups (after).
    4. `COUNT(*)` counts rows; `COUNT(col)` counts non-`NULL` values.
    5. When in doubt, add `GROUP_CONCAT` and **look inside** the groups.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
        mo.md("""
        ### Try It Yourself

        Write each query first. Then open the solution and compare.
        """),
        mo.accordion({
            "1. Total payroll per job title, smallest first.": mo.md("""
            ```sql
            SELECT job_title, SUM(salary) AS total_payroll
            FROM employees
            GROUP BY job_title
            ORDER BY total_payroll;
            ```
            4 rows. Marketer (230,000) comes first.
            """),
            "2. For each department, how many different job titles does it have?": mo.md("""
            ```sql
            SELECT dept_id, COUNT(DISTINCT job_title) AS job_titles
            FROM employees
            GROUP BY dept_id
            ORDER BY dept_id;
            ```
            Dept 10 has 3, dept 20 has 2, dept 30 has 2.
            """),
            "3. Which departments have more than 2 employees? Show the names of the people.": mo.md("""
            ```sql
            SELECT dept_id,
                   COUNT(*) AS employees,
                   GROUP_CONCAT(emp_name, ', ') AS members
            FROM employees
            GROUP BY dept_id
            HAVING COUNT(*) > 2;
            ```
            2 rows: dept 10 (7) and dept 20 (4).
            """),
            "4. Among employees earning under 100,000, what is the average salary per job title?": mo.md("""
            ```sql
            SELECT job_title, ROUND(AVG(salary), 2) AS avg_salary
            FROM employees
            WHERE salary < 100000
            GROUP BY job_title;
            ```
            3 rows. VP disappears: every VP fails the `WHERE` test.
            """),
            "5. Show the highest salary in each department, by department name.": mo.md("""
            ```sql
            SELECT d.dept_name, MAX(e.salary) AS max_salary
            FROM employees AS e
            INNER JOIN departments AS d ON e.dept_id = d.dept_id
            GROUP BY d.dept_name
            ORDER BY max_salary DESC;
            ```
            Sales 180,000 · Marketing 170,000 · Engineering 140,000.
            """),
            "6. Challenge: a pivot of headcount — one row per department name, one column per job title, 0 instead of NULL.": mo.md("""
            ```sql
            SELECT d.dept_name,
                   COUNT(CASE WHEN e.job_title = 'Engineer'    THEN 1 END) AS Engineer,
                   COUNT(CASE WHEN e.job_title = 'Marketer'    THEN 1 END) AS Marketer,
                   COUNT(CASE WHEN e.job_title = 'Salesperson' THEN 1 END) AS Salesperson,
                   COUNT(CASE WHEN e.job_title = 'VP'          THEN 1 END) AS VP
            FROM departments AS d
            LEFT JOIN employees AS e ON d.dept_id = e.dept_id
            GROUP BY d.dept_id, d.dept_name
            ORDER BY d.dept_id;
            ```
            5 rows. `COUNT` never returns `NULL`, so empty cells are 0.
            Finance and IT show a row of zeros, thanks to the `LEFT JOIN`.
            """),
        }),
        mo.md("""
        ---
        *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
        """),
    ])
    return


if __name__ == "__main__":
    app.run()
