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
    # 🦆 CTEs: Giving Subqueries a Name with `WITH`
    ### Write a query as a list of steps, read it from top to bottom

    **OMIS 105 — Introduction to Database Management Systems**

    A **CTE** (*Common Table Expression*) is a subquery that you **write first** and **give a name**.
    The main query then uses that name like a table. CTEs do not let you ask new questions —
    they let you ask **long** questions in a way people can read.

    | Part | Topic | Queries |
    |---|---|---|
    | 1 | Look at the data | Q1 – Q2 |
    | 2 | From subquery to CTE | Q3 – Q4 |
    | 3 | Anatomy of `WITH` | — |
    | 4 | A CTE that holds one value | Q5 |
    | 5 | Two CTEs | Q6 |
    | 6 | A CTE that reads an earlier CTE | Q7 – Q8 |
    | 7 | CTE + `JOIN` | Q9 – Q10 |
    | 8 | Use the same CTE twice | Q11 |
    | 9 | Debug a pipeline one step at a time (interactive) | Q12 |
    | 10 | Rules and real error messages | — |
    | 11 | Exercises | E1 – E3 |

    **Before this notebook:** `subqueries_notebook_01.py` (subqueries) and, ideally,
    `subqueries_notebook_03.py` (correlated subqueries).
    **After it:** `subqueries_notebook_02.py` — more CTE patterns on a bigger table, plus ranking.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=":memory:")
    con.execute("""
        CREATE OR REPLACE TABLE departments AS
        SELECT * FROM (VALUES
            (10, 'Sales',       'San Francisco'),
            (20, 'Engineering', 'San Jose'),
            (30, 'Marketing',   'San Francisco'),
            (40, 'HR',          'San Jose'),
            (50, 'Legal',       'Oakland')
        ) AS t(dept_id, dept_name, city)
    """)
    con.execute("""
        CREATE OR REPLACE TABLE employees AS
        SELECT * FROM (VALUES
            (1, 'Alice',  10,  60000),
            (2, 'Bob',    10,  52000),
            (3, 'Carmen', 20, 105000),
            (4, 'Daniel', 20,  98000),
            (5, 'Emma',   20,  87000),
            (6, 'Farid',  30,  64000),
            (7, 'Grace',  30,  92000),
            (8, 'Hannah', 40,  58000)
        ) AS t(emp_id, name, dept_id, salary)
    """)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Look at the Data

    The same 8 employees as notebook 01, now linked to a `departments` table by `dept_id`.
    **Legal (50) has no employees.**

    ```
    departments (dept_id) ──< employees (dept_id)
    ```

    **Q1 — Departments.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *
        FROM departments
        ORDER BY dept_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2 — Employees.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *
        FROM employees
        ORDER BY emp_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. From Subquery to CTE

    > **Question:** Which departments have an average salary above 70,000?

    **Q3 — The subquery version you already know** (a derived table in `FROM`, from notebook 01):
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT dept_id, ROUND(avg_salary, 2) AS avg_salary
        FROM (
            SELECT dept_id, AVG(salary) AS avg_salary
            FROM employees
            GROUP BY dept_id
        ) AS dept_averages
        WHERE avg_salary > 70000
        ORDER BY avg_salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To read Q3, you start in the **middle** (the inner query), then jump **out** to the outer query.

    **Q4 — The CTE version.** Cut the inner query out, move it to the **top**, and give it a name:
    """)
    return


@app.cell
def _(con):
    con.execute("""
        WITH dept_averages AS (
            SELECT dept_id, AVG(salary) AS avg_salary
            FROM employees
            GROUP BY dept_id
        )
        SELECT dept_id, ROUND(avg_salary, 2) AS avg_salary
        FROM dept_averages
        WHERE avg_salary > 70000
        ORDER BY avg_salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Same result:** Engineering (20) at 96,666.67 and Marketing (30) at 78,000.
    Same logic, too — only the **order on the page** changed. Now you read it **from top to bottom**:

    1. *First*, build `dept_averages` (one row per department).
    2. *Then*, select from it and keep the averages above 70,000.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. Anatomy of `WITH`

    ```
    WITH dept_averages AS (            ← WITH, then a NAME, then AS (
        SELECT dept_id, AVG(salary)    ← any SELECT query
        FROM employees                    (this is the "subquery")
        GROUP BY dept_id
    )                                  ← close the parenthesis
    SELECT ...                         ← the MAIN query: uses the name
    FROM dept_averages                    like a normal table
    WHERE ...;
    ```

    With **several** CTEs, write `WITH` **once** and separate the CTEs with **commas**:

    ```
    WITH step_one AS ( ... ),          ← comma after every CTE …
         step_two AS ( ... ),
         step_three AS ( ... )         ← … except the last one
    SELECT ... FROM step_three;        ← the main query
    ```

    > 💡 Choose names that say **what is inside**: `dept_averages`, `company_avg`, `top_earners`.
    > Then the query reads almost like a sentence.

    > A CTE is **not** a saved table. It exists only while **this one statement** runs (see Part 10).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. A CTE That Holds One Value

    A CTE can be tiny — even **one row with one number**.

    **Q5 — Employees who earn more than the company average** (notebook 01, Q4 — now with a CTE):
    """)
    return


@app.cell
def _(con):
    con.execute("""
        WITH company AS (
            SELECT AVG(salary) AS company_avg
            FROM employees
        )
        SELECT
            e.name,
            e.salary,
            c.company_avg,
            e.salary - c.company_avg AS difference
        FROM employees AS e
        CROSS JOIN company AS c
        WHERE e.salary > c.company_avg
        ORDER BY e.salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Carmen, Daniel, Grace, Emma — above 77,000.

    **`CROSS JOIN`** pairs every employee with every row of `company`. That is safe here because
    `company` has exactly **one** row: each employee simply gets the average attached as a new column.
    A bonus of the CTE: we can **show** `company_avg` in the output, which the `WHERE` subquery could not.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. Two CTEs

    > **Question:** Which departments pay **below** the company average, on average?

    We need two results: the department averages **and** the company average.

    **Q6 — Two CTEs, separated by a comma.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        WITH dept_averages AS (
            SELECT dept_id, AVG(salary) AS dept_avg
            FROM employees
            GROUP BY dept_id
        ),
        company AS (
            SELECT AVG(salary) AS company_avg
            FROM employees
        )
        SELECT
            d.dept_id,
            ROUND(d.dept_avg, 2) AS dept_avg,
            c.company_avg
        FROM dept_averages AS d
        CROSS JOIN company AS c
        WHERE d.dept_avg < c.company_avg
        ORDER BY d.dept_avg
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Sales (10) at 56,000 and HR (40) at 58,000 — both below 77,000.

    Here the two CTEs are **independent**: both read from `employees`.
    Next, one CTE will read from **another**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6. A CTE That Reads an Earlier CTE

    > **Question:** Which departments have a total payroll **above the average department payroll**?

    That is **two levels** of aggregation: first `SUM` per department, then `AVG` of those sums.

    **Q7 — The second CTE reads from the first.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        WITH dept_payroll AS (                 -- step 1: total per department
            SELECT dept_id, SUM(salary) AS payroll
            FROM employees
            GROUP BY dept_id
        ),
        avg_payroll AS (                       -- step 2: average of step 1
            SELECT AVG(payroll) AS avg_payroll
            FROM dept_payroll                  -- ← reads the first CTE
        )
        SELECT p.dept_id, p.payroll, a.avg_payroll
        FROM dept_payroll AS p
        CROSS JOIN avg_payroll AS a
        WHERE p.payroll > a.avg_payroll
        ORDER BY p.payroll DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The four payrolls are 112,000 (Sales), 290,000 (Engineering), 156,000 (Marketing), and 58,000 (HR).
    Their average is **154,000**. Engineering is far above it; Marketing just makes it (156,000).

    **Q8 — For comparison: the same question without `WITH`.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT dept_id, payroll
        FROM (
            SELECT dept_id, SUM(salary) AS payroll
            FROM employees
            GROUP BY dept_id
        ) AS p
        WHERE payroll > (
            SELECT AVG(payroll)
            FROM (
                SELECT dept_id, SUM(salary) AS payroll   -- the same query, written again
                FROM employees
                GROUP BY dept_id
            ) AS p2
        )
        ORDER BY payroll DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Same answer — but the payroll query is written **twice**, and you must read from the inside out
    through three levels of parentheses. If you later change one copy and forget the other,
    you get a wrong answer.

    > ✅ **This is the main reason to use a CTE:** write each step **once**, give it a **name**,
    > and let later steps **build on** earlier ones. A CTE can use any CTE written **above** it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7. CTE + `JOIN`

    A CTE can be joined to real tables, just like any table.

    **Q9 — A department report with names and cities — including Legal.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        WITH dept_stats AS (
            SELECT
                dept_id,
                COUNT(*)    AS headcount,
                SUM(salary) AS payroll,
                AVG(salary) AS avg_salary
            FROM employees
            GROUP BY dept_id
        )
        SELECT
            d.dept_name,
            d.city,
            COALESCE(s.headcount, 0)  AS headcount,
            COALESCE(s.payroll, 0)    AS payroll,
            ROUND(s.avg_salary, 2)    AS avg_salary
        FROM departments AS d
        LEFT JOIN dept_stats AS s
               ON s.dept_id = d.dept_id
        ORDER BY d.dept_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `dept_stats` has only **4** rows — Legal has no employees, so it has no group.
    The `LEFT JOIN` from `departments` keeps **all 5** departments, and `COALESCE` turns Legal's
    missing headcount and payroll into **0**. (Its average stays empty: there is no average of nobody.)

    **Q10 — Employees above their own department's average.**

    In notebook 03 you solved this with a **correlated subquery**. Here is the CTE way:
    compute every department average **once**, then join it to the employees.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        WITH dept_averages AS (
            SELECT dept_id, AVG(salary) AS dept_avg
            FROM employees
            GROUP BY dept_id
        )
        SELECT
            e.name,
            d.dept_name,
            e.salary,
            ROUND(a.dept_avg, 2)            AS dept_avg,
            ROUND(e.salary - a.dept_avg, 2) AS above_by
        FROM employees AS e
        JOIN dept_averages AS a ON a.dept_id = e.dept_id
        JOIN departments   AS d ON d.dept_id = e.dept_id
        WHERE e.salary > a.dept_avg
        ORDER BY d.dept_id, e.salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Alice, Carmen, Daniel, Grace — the same four people as notebook 03, Q5.
    The CTE version can also **show** the department average and the gap, which helps explain the answer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8. Use the Same CTE Twice

    A CTE can be used **more than once** in the same statement.

    **Q11 — The department(s) with the most employees.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        WITH dept_stats AS (
            SELECT dept_id, COUNT(*) AS headcount, AVG(salary) AS avg_salary
            FROM employees
            GROUP BY dept_id
        )
        SELECT dept_id, headcount, ROUND(avg_salary, 2) AS avg_salary
        FROM dept_stats                         -- use #1
        WHERE headcount = (
            SELECT MAX(headcount)
            FROM dept_stats                     -- use #2
        )
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Engineering (20), with 3 employees. Notice that a CTE and a subquery work **together** here:
    the scalar subquery `(SELECT MAX(headcount) FROM dept_stats)` reads the CTE.
    If two departments tied for the most employees, both would appear.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    step_picker = mo.ui.dropdown(
        options={
            "Step 1 — dept_stats": "dept_stats",
            "Step 2 — company": "company",
            "Step 3 — compared": "compared",
        },
        value="Step 1 — dept_stats",
        label="Show the result of",
    )
    mo.vstack([
        mo.md(r"""
    ---
    ## 9. Debug a Pipeline One Step at a Time 🎛️

    **Q12** below is a three-step pipeline. When a long query gives a strange answer,
    use this professional trick: **keep the `WITH` part, and change only the last line** to
    `SELECT * FROM <one step>`. That shows you exactly what each step produces.

    Pick a step and watch the last line — and the result — change.
    """),
        step_picker,
    ])
    return (step_picker,)


@app.cell(hide_code=True)
def _(con, mo, step_picker):
    from textwrap import dedent as _dedent

    _pipeline = """\
    WITH dept_stats AS (
        SELECT dept_id, COUNT(*) AS headcount, AVG(salary) AS avg_salary
        FROM employees
        GROUP BY dept_id
    ),
    company AS (
        SELECT AVG(salary) AS company_avg
        FROM employees
    ),
    compared AS (
        SELECT
            d.dept_name,
            s.headcount,
            ROUND(s.avg_salary, 2) AS avg_salary,
            c.company_avg,
            CASE WHEN s.avg_salary > c.company_avg
                 THEN 'Above' ELSE 'Below' END AS vs_company
        FROM dept_stats AS s
        JOIN departments AS d ON d.dept_id = s.dept_id
        CROSS JOIN company AS c
    )"""
    _last = f"SELECT * FROM {step_picker.value}"
    _notes = {
        "dept_stats": "One row per department **that has employees** — 4 rows, no Legal.",
        "company": "Exactly **one** row: the company average, 77,000.",
        "compared": "Steps 1 and 2 combined, with department names and an Above/Below label.",
    }
    _pipeline = _dedent(_pipeline)
    _md = (
        "```sql\n" + _pipeline + "\n" + _last
        + ";      -- ← only this line changes\n```\n\n"
        + _notes[step_picker.value]
    )
    mo.vstack([
        mo.md(_md),
        con.execute(f"{_pipeline}\n{_last}").fetchdf(),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 10. Rules and Real Error Messages

    Each mistake below was run in DuckDB. This is what you would see:
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    con.execute("""
        WITH dept_stats AS (
            SELECT dept_id, COUNT(*) AS headcount
            FROM employees
            GROUP BY dept_id
        )
        SELECT * FROM dept_stats
    """)
    _mistakes = [
        (
            "1. Using a CTE after its statement has ended",
            "SELECT * FROM dept_stats;   -- a new statement",
            "A CTE lives only inside its own statement. "
            "To keep a result, use `CREATE TABLE ... AS` or a `VIEW`.",
        ),
        (
            "2. Using a CTE before it is defined",
            "WITH a AS (SELECT * FROM b),\n     b AS (SELECT 1 AS x)\nSELECT * FROM a;",
            "A CTE can use only the CTEs written **above** it. Put `b` first.",
        ),
        (
            "3. Writing `WITH` twice",
            "WITH a AS (SELECT 1 AS x)\nWITH b AS (SELECT 2 AS y)\nSELECT * FROM a, b;",
            "Write `WITH` once, then separate the CTEs with commas.",
        ),
        (
            "4. Forgetting the comma between CTEs",
            "WITH a AS (SELECT 1 AS x)\n     b AS (SELECT 2 AS y)\nSELECT * FROM a, b;",
            "Add a comma after `)` of every CTE except the last.",
        ),
        (
            "5. A comma after the last CTE",
            "WITH a AS (SELECT 1 AS x),\nSELECT * FROM a;",
            "No comma between the last CTE and the main `SELECT`.",
        ),
    ]
    _cards = []
    for _title, _sql, _fix in _mistakes:
        try:
            con.execute(_sql)
            _msg = "No error?"
        except Exception as _e:
            _msg = str(_e).splitlines()[0]
        _md = (
            f"**{_title}**\n\n```sql\n{_sql}\n```\n\n"
            f"**DuckDB says:** `{_msg}`\n\n**Fix:** {_fix}"
        )
        _cards.append(mo.callout(mo.md(_md), kind="danger"))
    mo.vstack(_cards)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Mistakes 1 and 2 give a **Catalog Error** ("table does not exist") — DuckDB cannot find the name.
    Mistakes 3–5 give a **Parser Error** — the query is not valid SQL. The error points to the
    word *right after* the problem.

    ### When should I use a CTE?

    | Situation | Good choice |
    |---|---|
    | A short, one-step condition (`WHERE salary > (SELECT AVG(salary) ...)`) | a plain subquery is fine |
    | Two or more steps, or nested parentheses are getting hard to read | **CTE** |
    | The same intermediate result is needed **twice** | **CTE** (write it once) |
    | You want to **show** an intermediate value (like the company average) in the output | **CTE** + `CROSS JOIN` |
    | You need the result again in **later** queries | a table or a `VIEW` — a CTE disappears |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 11. Exercises

    Write each query in the empty cell below it, then open the solution to check.

    **E1.** Rewrite notebook 01's Q4 with a CTE: show the **names** of the employees who earn more
    than the company average. Use a CTE named `company`.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        -- your query for E1 here
        SELECT 'replace me' AS hint
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "💡 Solution E1": mo.md(r"""
    ```sql
    WITH company AS (
        SELECT AVG(salary) AS company_avg
        FROM employees
    )
    SELECT e.name
    FROM employees AS e
    CROSS JOIN company AS c
    WHERE e.salary > c.company_avg
    ORDER BY e.salary DESC;
    ```
    **Carmen, Daniel, Grace, Emma.**
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **E2.** Use a CTE named `top_salary` with the **highest salary in each department**.
    Then show **every** department's name, city, and top salary — Legal included.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        -- your query for E2 here
        SELECT 'replace me' AS hint
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "💡 Solution E2": mo.md(r"""
    ```sql
    WITH top_salary AS (
        SELECT dept_id, MAX(salary) AS max_salary
        FROM employees
        GROUP BY dept_id
    )
    SELECT d.dept_name, d.city, t.max_salary
    FROM departments AS d
    LEFT JOIN top_salary AS t
           ON t.dept_id = d.dept_id
    ORDER BY d.dept_id;
    ```
    **5 rows:** Sales 60,000 · Engineering 105,000 · Marketing 92,000 · HR 58,000 · Legal (empty).
    "Legal included" is the clue for `LEFT JOIN` from `departments`. An `INNER JOIN` would give only 4 rows.
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **E3 (challenge).** Build a **three-step** pipeline:

    1. `dept_payroll` — total salary per department.
    2. `total` — the company's total payroll (one row), read **from step 1**.
    3. `shares` — each department's payroll as a **percentage** of the total, rounded to 2 decimals.

    Then show the department **names** whose share is **more than 15%**, largest first.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        -- your query for E3 here
        SELECT 'replace me' AS hint
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "💡 Solution E3": mo.md(r"""
    ```sql
    WITH dept_payroll AS (
        SELECT dept_id, SUM(salary) AS payroll
        FROM employees
        GROUP BY dept_id
    ),
    total AS (
        SELECT SUM(payroll) AS total_payroll
        FROM dept_payroll
    ),
    shares AS (
        SELECT
            p.dept_id,
            p.payroll,
            ROUND(100.0 * p.payroll / t.total_payroll, 2) AS pct
        FROM dept_payroll AS p
        CROSS JOIN total AS t
    )
    SELECT d.dept_name, s.payroll, s.pct
    FROM shares AS s
    JOIN departments AS d ON d.dept_id = s.dept_id
    WHERE s.pct > 15
    ORDER BY s.pct DESC;
    ```
    Total payroll is **616,000**. **Engineering 47.08% · Marketing 25.32% · Sales 18.18%.**
    HR (9.42%) is below 15%.

    Write `100.0` (not `100`) so the division is done with decimals.
    🔍 Stuck? Use the Part 9 trick: end with `SELECT * FROM shares` and look at the step.
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🎓 Summary

    - A **CTE** is a subquery with a **name**, written **first**: `WITH name AS ( SELECT ... )`.
    - Write `WITH` **once**; separate several CTEs with **commas**; no comma before the main `SELECT`.
    - A CTE can read any CTE written **above** it — so a query becomes a **pipeline of steps** (Q7).
    - A CTE can be joined to tables (Q9, Q10), used **twice** (Q11), or hold just **one value** (Q5).
    - CTEs make queries **easier to read and to debug** — end with `SELECT * FROM <step>` to inspect any step (Q12).
    - A CTE lives only for **one statement**. To keep a result, create a table or a view.

    **What's next?**

    - `subqueries_notebook_02.py` — nine more CTE lessons on a 20-row table, ending with
      ranking (`ROW_NUMBER`, `RANK`, `DENSE_RANK`) and "top earner per department".
    - `subqueries_04_tutorial.md` §13 — CTEs in the complete reference, including **recursive** CTEs.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
