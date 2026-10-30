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
    # 🦆 Subqueries — The Very Basics
    ### A query inside a query, step by step, with DuckDB

    **OMIS 105 — Introduction to Database Management Systems**

    A **subquery** is a `SELECT` written **inside another SQL statement**, in parentheses.
    The inner query finds a value (or a list, or a small table). The outer query uses it.

    | Part | Topic | Queries |
    |---|---|---|
    | 1 | Look at the data | Q1 |
    | 2 | The problem: a question in two steps | Q2 – Q4 |
    | 3 | One value: `MAX` and `MIN` | Q5 |
    | 4 | A subquery in `SELECT` | Q6 |
    | 5 | A subquery that returns text | Q7 |
    | 6 | A list of values: `IN` and `NOT IN` | Q8 – Q10 |
    | 7 | A table of rows: a subquery in `FROM` | Q11 – Q13 |
    | 8 | The most common error | — |
    | 9 | Try it yourself (interactive) | — |
    | 10 | Exercises | E1 – E3 |

    Run the cells from top to bottom. After this notebook, continue with
    `subqueries_notebook_03.py` (correlated subqueries and `EXISTS`)
    and `subqueries_notebook_04.py` (subqueries with `WITH`).

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=":memory:")
    con.execute("""
        CREATE OR REPLACE TABLE employees AS
        SELECT * FROM (VALUES
            (1, 'Alice',  'Sales',        60000),
            (2, 'Bob',    'Sales',        52000),
            (3, 'Carmen', 'Engineering', 105000),
            (4, 'Daniel', 'Engineering',  98000),
            (5, 'Emma',   'Engineering',  87000),
            (6, 'Farid',  'Marketing',    64000),
            (7, 'Grace',  'Marketing',    92000),
            (8, 'Hannah', 'HR',           58000)
        ) AS t(emp_id, name, dept, salary)
    """)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Look at the Data

    One small table, `employees`, with 8 rows. That is all we need.

    | Column | Meaning |
    |---|---|
    | `emp_id` | Employee ID |
    | `name` | First name |
    | `dept` | Department: Sales, Engineering, Marketing, or HR |
    | `salary` | Annual salary (USD) |

    **Q1 — Show every employee.**
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
    ## 2. The Problem: A Question in Two Steps

    > **Question:** Which employees earn **more than the average salary**?

    You cannot answer this with one simple `WHERE`, because you do not know the average yet.
    A person would solve it in **two steps**:

    1. Calculate the average salary.
    2. Keep the employees whose salary is greater than that number.

    **Q2 — Step 1: calculate the average.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT AVG(salary) AS avg_salary
        FROM employees
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The average is **77,000**.

    **Q3 — Step 2: type that number into a second query.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT name, dept, salary
        FROM employees
        WHERE salary > 77000          -- typed by hand from Q2
        ORDER BY salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This works — but it has a problem. **77000 is typed by hand.**
    If someone gets a raise tomorrow, the average changes, and Q3 silently gives the wrong answer.

    **Q4 — The subquery version: put Step 1 inside Step 2.**

    Replace the number `77000` with the query that *calculates* it, in parentheses:
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT name, dept, salary
        FROM employees
        WHERE salary > (
            SELECT AVG(salary)      -- the inner query (subquery)
            FROM employees
        )
        ORDER BY salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Same 4 rows as Q3 — Carmen, Daniel, Grace, Emma — but now **nothing is typed by hand**.

    ### 🧠 How to read a subquery: from the inside out

    ```
    SELECT name, dept, salary
    FROM employees
    WHERE salary > ( SELECT AVG(salary) FROM employees )
                     └──────────── inner query ─────────┘
                                   returns 77000

    becomes  →  WHERE salary > 77000
    ```

    1. Read the **inner query** first. Ask: *what does it return?* Here: one number, 77000.
    2. Mentally replace the parentheses with that result.
    3. Now read the **outer query** as a normal query.

    > This is a way to **think** about a subquery. DuckDB may run it in a smarter order,
    > but the result is always the same as this picture.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. One Value: `MAX` and `MIN`

    A subquery that returns **exactly one value** (one row, one column) is called a
    **scalar subquery**. You can use it anywhere you could type a single number.

    **Q5 — Who earns the most?**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT name, dept, salary
        FROM employees
        WHERE salary = (
            SELECT MAX(salary)
            FROM employees
        )
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The inner query returns **105000**, so the outer query becomes `WHERE salary = 105000` → **Carmen**.

    > 💡 Why not `ORDER BY salary DESC LIMIT 1`? That also finds Carmen — but if **two** people
    > shared the top salary, `LIMIT 1` would show only one of them. The subquery shows **all** of them.

    ✏️ **Try it:** change `MAX` to `MIN`. You should get **Bob** (52,000).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. A Subquery in `SELECT`

    A scalar subquery can also be a **column**. The same value is repeated on every row,
    so you can compare each row with it.

    **Q6 — Show each salary next to the company average, and the difference.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            name,
            salary,
            (SELECT AVG(salary) FROM employees)          AS company_avg,
            salary - (SELECT AVG(salary) FROM employees) AS difference
        FROM employees
        ORDER BY salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A **positive** difference means *above* average (Carmen: +28,000).
    A **negative** difference means *below* average (Bob: −25,000).

    > Why not just `SELECT name, salary, AVG(salary) FROM employees`?
    > Because `AVG` would collapse the 8 rows into 1 — and DuckDB would ask for a `GROUP BY`.
    > The subquery calculates the average **separately**, so every row stays.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. A Subquery That Returns Text

    A scalar subquery does not have to return a number. It can return a name, a department, a date…

    **Q7 — Who works in the same department as Farid?**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT name, dept, salary
        FROM employees
        WHERE dept = (
            SELECT dept
            FROM employees
            WHERE name = 'Farid'
        )
        ORDER BY name
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Inside out: the inner query returns **'Marketing'** → the outer query becomes
    `WHERE dept = 'Marketing'` → **Farid and Grace**.

    We never had to look up Farid's department ourselves.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6. A List of Values: `IN` and `NOT IN`

    Sometimes the inner query returns **several rows**. Then `=` is not enough —
    a value cannot be "equal" to a whole list. Use **`IN`**, which means *"is in this list"*.

    > **Question:** Show every employee who works in a department that has **at least one person earning over 90,000**.

    **Q8 — First, run the inner query alone.** (A good habit!)
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT DISTINCT dept
        FROM employees
        WHERE salary > 90000
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two departments: **Engineering** (Carmen, Daniel) and **Marketing** (Grace). That is a **list**.

    **Q9 — Now put it inside `IN`.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT name, dept, salary
        FROM employees
        WHERE dept IN (
            SELECT dept
            FROM employees
            WHERE salary > 90000
        )
        ORDER BY dept, salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    👀 **Look at Farid.** He earns only 64,000 — but he is in the result.
    The subquery chooses **departments**; the outer query returns **everyone** in those departments.
    Always ask: *what does the inner query return — people, or departments?*

    **Q10 — `NOT IN`: everyone in the *other* departments.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT name, dept, salary
        FROM employees
        WHERE dept NOT IN (
            SELECT dept
            FROM employees
            WHERE salary > 90000
        )
        ORDER BY dept, salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    HR (Hannah) and Sales (Alice, Bob) — the 3 employees Q9 did not show. Q9 + Q10 = all 8 rows.

    > ⚠️ **Careful with `NOT IN`:** if the inner list contains a `NULL`, `NOT IN` returns **no rows at all**.
    > Our table has no `NULL`s, so we are safe here. You will see this trap in action — and its fix, `NOT EXISTS` —
    > in `subqueries_notebook_03.py` (Part 10).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7. A Table of Rows: A Subquery in `FROM`

    The inner query can also return a **whole small table**. Put it in `FROM`,
    give it a name with `AS`, and query it like any other table.
    This is called a **derived table**.

    **Q11 — First, the department averages (a normal `GROUP BY`).**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT dept, ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY dept
        ORDER BY avg_salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Four departments, four averages. Engineering is the highest: **96,666.67**.

    > **Question:** What is the **highest department average**?

    It is tempting to write `MAX(AVG(salary))` — but SQL does **not** allow one aggregate inside another:
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    try:
        con.execute("""
            SELECT MAX(AVG(salary))
            FROM employees
            GROUP BY dept
        """)
        _msg = "No error?"
    except Exception as _e:
        _msg = str(_e).splitlines()[0]
    mo.callout(
        mo.md(f"""
    ```sql
    SELECT MAX(AVG(salary)) FROM employees GROUP BY dept
    ```
    **DuckDB says:** `{_msg}`
    """),
        kind="danger",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12 — The fix: compute the averages in a subquery, then take the `MAX` of that table.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT MAX(avg_salary) AS highest_dept_avg
        FROM (
            SELECT dept, AVG(salary) AS avg_salary
            FROM employees
            GROUP BY dept
        ) AS dept_averages
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Inside out: the inner query builds a 4-row table named `dept_averages`.
    The outer query treats it like a normal table and takes its `MAX` → **96,666.67**.

    > Always give a derived table a name (`AS dept_averages`). DuckDB lets you skip it,
    > but most other databases require it.

    **Q13 — Filter the derived table: departments with an average above 70,000.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT dept, ROUND(avg_salary, 2) AS avg_salary
        FROM (
            SELECT dept, AVG(salary) AS avg_salary
            FROM employees
            GROUP BY dept
        ) AS dept_averages
        WHERE avg_salary > 70000
        ORDER BY avg_salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Engineering (96,666.67) and Marketing (78,000).

    > You could also write this one with `HAVING AVG(salary) > 70000`.
    > The derived table becomes the better tool when you need **two levels** of calculation, as in Q12.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8. The Most Common Error

    `=`, `>`, `<` need **one value** on the right side. What happens if the subquery returns **a list**?
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    try:
        con.execute("""
            SELECT name
            FROM employees
            WHERE dept = (
                SELECT dept
                FROM employees
                WHERE salary > 90000
            )
        """)
        _msg = "No error?"
    except Exception as _e:
        _msg = str(_e).splitlines()[0]
    mo.callout(
        mo.md(f"""
    ```sql
    SELECT name FROM employees
    WHERE dept = (SELECT dept FROM employees WHERE salary > 90000)
    ```
    **DuckDB says:** `{_msg}`

    **Why?** The inner query returns **two** departments (Q8). `=` cannot compare with two values.

    **Fix:** use `IN` (as in Q9) — or make the inner query return one value, e.g. with `MAX`, `MIN`, or `AVG`.
    """),
        kind="danger",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Rule of thumb — know the shape of the inner result:**

    | The inner query returns… | Name | Use it with… | Example |
    |---|---|---|---|
    | **one value** (1 row, 1 column) | scalar subquery | `=`, `>`, `<`, or as a column in `SELECT` | Q4 – Q7 |
    | **a list** (many rows, 1 column) | multi-row subquery | `IN`, `NOT IN` | Q9 – Q10 |
    | **a table** (many rows and columns) | derived table | `FROM ( ... ) AS name` | Q12 – Q13 |
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _depts = [
        _r[0]
        for _r in con.execute(
            "SELECT DISTINCT dept FROM employees ORDER BY dept"
        ).fetchall()
    ]
    dept_picker = mo.ui.dropdown(options=_depts, value="Sales", label="Department")
    mo.vstack([
        mo.md(r"""
    ---
    ## 9. Try It Yourself 🎛️

    > **Question:** Who earns more than the **average salary of the department you pick**?

    Pick a department. Watch the inner query's result and the final answer change.
    """),
        dept_picker,
    ])
    return (dept_picker,)


@app.cell(hide_code=True)
def _(con, dept_picker, mo):
    _dept = dept_picker.value
    _inner = con.execute(
        "SELECT AVG(salary) FROM employees WHERE dept = ?", [_dept]
    ).fetchone()[0]
    _result = con.execute(
        """
        SELECT name, dept, salary
        FROM employees
        WHERE salary > (
            SELECT AVG(salary)
            FROM employees
            WHERE dept = ?
        )
        ORDER BY salary DESC
        """,
        [_dept],
    ).fetchdf()
    mo.vstack([
        mo.md(f"""
    ```sql
    SELECT name, dept, salary
    FROM employees
    WHERE salary > (
        SELECT AVG(salary)
        FROM employees
        WHERE dept = '{_dept}'      -- inner query returns {_inner:,.2f}
    )
    ORDER BY salary DESC
    ```
    **{len(_result)} employee(s)** earn more than {_inner:,.2f}:
    """),
        _result,
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 10. Exercises

    Write each query in the empty cell below it, then open the solution to check.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **E1.** Show the employees who earn **less** than the company average salary. Sort by salary.
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
    SELECT name, dept, salary
    FROM employees
    WHERE salary < (
        SELECT AVG(salary)
        FROM employees
    )
    ORDER BY salary;
    ```
    **4 rows:** Bob (52,000), Hannah (58,000), Alice (60,000), Farid (64,000) — all below 77,000.
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **E2.** Show the employees who earn more than the **average salary of the Sales department**.
    *Hint:* the inner query needs its own `WHERE`.
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
    SELECT name, dept, salary
    FROM employees
    WHERE salary > (
        SELECT AVG(salary)
        FROM employees
        WHERE dept = 'Sales'
    )
    ORDER BY salary DESC;
    ```
    The Sales average is **56,000**, so **7 rows** — everyone except Bob (52,000).
    Alice is in Sales herself, and she still qualifies (60,000 > 56,000).
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **E3 (challenge).** Show everyone who works in the **same department as the lowest-paid employee**.
    *Hint:* you need a subquery **inside** a subquery. Work from the inside out:
    lowest salary → that person's department → everyone in that department.
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
    SELECT name, dept, salary
    FROM employees
    WHERE dept = (
        SELECT dept
        FROM employees
        WHERE salary = (
            SELECT MIN(salary)
            FROM employees
        )
    )
    ORDER BY salary DESC;
    ```
    Inside out: `MIN(salary)` → **52,000** → that is Bob, in **Sales** → everyone in Sales:
    **Alice and Bob**.
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🎓 Summary

    - A **subquery** is a `SELECT` inside parentheses, inside another query.
    - Read it **from the inside out**: what does the inner query return? Then read the outer query.
    - **One value** → compare with `=`, `>`, `<`, or show it as a column.
    - **A list** → use `IN` / `NOT IN`. (Watch out for `NULL` with `NOT IN`.)
    - **A table** → put it in `FROM` and give it a name with `AS`.
    - A subquery replaces a **number typed by hand**, so your answer stays right when the data changes.

    **What's next?**

    - `subqueries_notebook_03.py` — **correlated** subqueries ("the average of *this employee's* department"),
      `EXISTS`, `NOT EXISTS`, and the `NOT IN` + `NULL` trap.
    - `subqueries_notebook_04.py` — give subqueries a name with `WITH` (CTEs), step by step.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
