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
    # 🦆 Correlated Subqueries and `EXISTS`
    ### When the inner query depends on the outer row

    **OMIS 105 — Introduction to Database Management Systems**

    In `subqueries_notebook_01.py`, every inner query returned **the same answer for every row**
    (for example, the company average). In this notebook, the inner query gives a
    **different answer for each row** — because it *uses a value from the outer row*.
    That is a **correlated subquery**. Then we use the same idea with **`EXISTS`**,
    which asks a yes/no question: *"is there at least one matching row?"*

    | Part | Topic | Queries |
    |---|---|---|
    | 1 | Look at the data | Q1 – Q2 |
    | 2 | Why we need a new idea | Q3 – Q4 |
    | 3 | Your first correlated subquery | Q5 |
    | 4 | X-ray: see the inner result for every row | Q6 |
    | 5 | Step through it yourself (interactive) | — |
    | 6 | Top earner in each department | Q7 |
    | 7 | Pitfall: forgetting the aliases | Q8 |
    | 8 | `EXISTS` — is there at least one? | Q9 – Q11 |
    | 9 | `NOT EXISTS` — find what is missing | Q12 |
    | 10 | The `NOT IN` + `NULL` trap | Q13 – Q15 |
    | 11 | Try it yourself (interactive) | — |
    | 12 | Exercises | E1 – E3 |

    **Before this notebook:** `subqueries_notebook_01.py` (the very basics).

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
            (1, 'Alice',  10,    60000),
            (2, 'Bob',    10,    52000),
            (3, 'Carmen', 20,   105000),
            (4, 'Daniel', 20,    98000),
            (5, 'Emma',   20,    87000),
            (6, 'Farid',  30,    64000),
            (7, 'Grace',  30,    92000),
            (8, 'Hannah', 40,    58000),
            (9, 'Ivan',   NULL,  70000)
        ) AS t(emp_id, name, dept_id, salary)
    """)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Look at the Data

    Two tables, linked by `dept_id`:

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
    **Remember two facts — they matter later:**

    - 🏢 **Legal (50) has no employees.**
    - 🆕 **Ivan is a new hire with no department yet:** his `dept_id` is `NULL`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. Why We Need a New Idea

    **Q3 — Recap from notebook 01:** who earns more than the **company** average?
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT name, dept_id, salary
        FROM employees
        WHERE salary > (
            SELECT AVG(salary)
            FROM employees
        )
        ORDER BY salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The inner query returns **one number** (76,222.22) — the same for every employee.

    Now a fairer question:

    > **Who earns more than the average of *their own* department?**

    Alice earns 60,000 — below the company average, but Sales is a low-paid department.
    Is she above the **Sales** average? We need a **different average for each department**.

    **Q4 — The department averages.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            dept_id,
            ROUND(AVG(salary), 2) AS avg_salary,
            COUNT(*)              AS employees
        FROM employees
        GROUP BY dept_id
        ORDER BY dept_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Sales (10) averages **56,000**, so Alice (60,000) *is* above her department's average.

    The last row is Ivan alone: `GROUP BY` puts all `NULL` values into one group.

    We cannot type five numbers into `WHERE`. We need an inner query that **looks at the
    current employee's department** and calculates *that* average. That is a correlated subquery.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. Your First Correlated Subquery

    **Q5 — Employees who earn more than the average of their own department.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT e.name, e.dept_id, e.salary
        FROM employees AS e
        WHERE e.salary > (
            SELECT AVG(x.salary)
            FROM employees AS x
            WHERE x.dept_id = e.dept_id     -- the link to the outer row
        )
        ORDER BY e.dept_id, e.salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🧠 How to read it

    The same table is used **twice**, so we give it two **aliases** (nicknames):

    - `e` = the **outer** query — "the employee we are checking now"
    - `x` = the **inner** query — "the employees we compare with"

    The line `WHERE x.dept_id = e.dept_id` uses `e` — a column from the **outer** query.
    That makes the inner query **correlated**: its answer depends on which employee `e` is.

    Think of it as a loop:

    ```
    for each employee e:
        inner query: average salary of employees x in e's department
        keep e if e.salary > that average
    ```

    | Employee `e` | `e.dept_id` | Inner query returns | `e.salary > ...`? |
    |---|---|---|---|
    | Alice | 10 | 56,000.00 | 60,000 > 56,000 ✅ |
    | Bob | 10 | 56,000.00 | 52,000 > 56,000 ❌ |
    | Emma | 20 | 96,666.67 | 87,000 > 96,666.67 ❌ |
    | Hannah | 40 | 58,000.00 | 58,000 > 58,000 ❌ (equal is not greater) |
    | Ivan | `NULL` | `NULL` | unknown ❌ |

    **Result: Alice, Carmen, Daniel, Grace.** Compare with Q3: Alice is **in** now, Emma is **out**.

    > Why is Ivan out? `x.dept_id = NULL` is never true, so the inner query finds **no rows**,
    > and the average of no rows is `NULL`. `70000 > NULL` is *unknown*, and `WHERE` keeps only *true*.

    > The loop is a way to **think** about it. DuckDB is smarter: it usually computes all the
    > department averages once and matches them up. The result is the same.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. X-Ray: See the Inner Result for Every Row

    A correlated subquery can also be a **column** in `SELECT`.
    This is a great way to *see* what the inner query returns for each row.

    **Q6 — Each employee, their department's average, and their department's size.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            e.name,
            e.dept_id,
            e.salary,
            (SELECT ROUND(AVG(x.salary), 2)
               FROM employees AS x
              WHERE x.dept_id = e.dept_id) AS dept_avg,
            (SELECT COUNT(*)
               FROM employees AS x
              WHERE x.dept_id = e.dept_id) AS dept_size
        FROM employees AS e
        ORDER BY e.dept_id NULLS LAST, e.salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every row gets **its own** `dept_avg`. Ivan's row shows the `NULL` effect:
    `dept_avg` is empty (`NaN`) and `dept_size` is **0** — the inner query matched nobody.

    > 💡 **Debugging tip:** when a correlated `WHERE` gives a surprising answer,
    > copy the subquery into `SELECT` like this and look at the numbers.
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _names = [
        _r[0]
        for _r in con.execute("SELECT name FROM employees ORDER BY emp_id").fetchall()
    ]
    emp_picker = mo.ui.dropdown(options=_names, value="Alice", label="Employee e")
    mo.vstack([
        mo.md(r"""
    ---
    ## 5. Step Through It Yourself 🎛️

    Pick an employee. You will see the inner query **exactly as DuckDB thinks of it for that row**
    — with `e.dept_id` replaced by the real value — and whether Q5 keeps the row.
    """),
        emp_picker,
    ])
    return (emp_picker,)


@app.cell(hide_code=True)
def _(con, emp_picker, mo):
    _name, _dept, _salary = con.execute(
        "SELECT name, dept_id, salary FROM employees WHERE name = ?",
        [emp_picker.value],
    ).fetchone()
    _avg = con.execute(
        "SELECT AVG(salary) FROM employees WHERE dept_id = ?", [_dept]
    ).fetchone()[0]
    _dept_text = "NULL" if _dept is None else str(_dept)
    _avg_text = "NULL" if _avg is None else f"{_avg:,.2f}"
    if _avg is None:
        _verdict = (
            f"❌ **{_name} is not kept.** {_salary:,} > NULL is *unknown*, "
            "and `WHERE` keeps only *true*."
        )
    elif _salary > _avg:
        _verdict = f"✅ **{_name} is kept:** {_salary:,} > {_avg_text}"
    else:
        _verdict = f"❌ **{_name} is not kept:** {_salary:,} is not greater than {_avg_text}"
    mo.md(f"""
    **Outer row:** `e.name = '{_name}'`, `e.dept_id = {_dept_text}`, `e.salary = {_salary:,}`

    **Inner query for this row:**
    ```sql
    SELECT AVG(x.salary)
    FROM employees AS x
    WHERE x.dept_id = {_dept_text}      -- was: e.dept_id
    ```
    **Inner result:** {_avg_text}

    {_verdict}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6. Top Earner in Each Department

    Swap `AVG` for `MAX`, and `>` for `=`.

    **Q7 — The highest-paid employee in each department.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT e.name, e.dept_id, e.salary
        FROM employees AS e
        WHERE e.salary = (
            SELECT MAX(x.salary)
            FROM employees AS x
            WHERE x.dept_id = e.dept_id
        )
        ORDER BY e.dept_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One row per department: Alice, Carmen, Grace, and Hannah (the only person in HR).
    Ivan is missing again — his department is `NULL`, so there is no "maximum of his department".

    > If two people tied for the top salary in a department, **both** would appear.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7. Pitfall: Forgetting the Aliases

    What if we write Q5 **without** `e` and `x`?

    **Q8 — Looks almost the same. Is it?**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT name, dept_id, salary
        FROM employees
        WHERE salary > (
            SELECT AVG(salary)
            FROM employees
            WHERE dept_id = dept_id      -- ⚠️ which dept_id is which?
        )
        ORDER BY salary DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **No error — but the wrong answer.** Carmen, Daniel, Grace, Emma: Alice is missing and Emma is back.

    **Why?** Inside the subquery, SQL looks for `dept_id` in the **nearest** table first —
    the inner `employees`. So `dept_id = dept_id` compares each inner row **with itself**.
    That is true for every row (except Ivan's `NULL`). The subquery is **not correlated** at all:
    it returns one number, the average of the 8 employees with a department (**77,000**).

    > ✅ **Rule:** in a correlated subquery, **always** give both tables an alias and
    > **always** write `alias.column`. A missing alias does not cause an error — it causes a wrong answer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8. `EXISTS` — Is There at Least One?

    `EXISTS ( subquery )` is **true** if the subquery returns **at least one row**, and **false** if it returns none.
    It does not care *what* the rows contain — only whether there are any.
    That is why people write `SELECT 1` inside: the `1` is never used.

    `EXISTS` is almost always **correlated**: "is there an employee **in this department** who…?"

    **Q9 — Departments that have at least one employee.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT d.dept_id, d.dept_name
        FROM departments AS d
        WHERE EXISTS (
            SELECT 1
            FROM employees AS e
            WHERE e.dept_id = d.dept_id
        )
        ORDER BY d.dept_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Four departments. **Legal** is missing: for Legal, the inner query finds no rows → `EXISTS` is false.

    You can add more conditions inside.

    **Q10 — Departments with at least one employee earning over 90,000.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT d.dept_name
        FROM departments AS d
        WHERE EXISTS (
            SELECT 1
            FROM employees AS e
            WHERE e.dept_id = d.dept_id
              AND e.salary > 90000
        )
        ORDER BY d.dept_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Engineering** (Carmen, Daniel) and **Marketing** (Grace).

    ### Why not just a `JOIN`?

    **Q11 — The same question with `JOIN`.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT d.dept_name
        FROM departments AS d
        JOIN employees AS e
          ON e.dept_id = d.dept_id
        WHERE e.salary > 90000
        ORDER BY d.dept_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Engineering appears twice** — once for Carmen and once for Daniel. A `JOIN` returns one row
    per *matching pair*. You would need `DISTINCT` to fix it.

    `EXISTS` never duplicates: each department is checked once and is either kept or not.

    > Use `JOIN` when you need **columns from both tables**.
    > Use `EXISTS` when you only ask **"is there a match?"**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 9. `NOT EXISTS` — Find What Is Missing

    Flip the question: keep the rows for which **no** matching row exists.
    This pattern is called an **anti-join**, and it answers many business questions:
    customers who never ordered, products never sold, courses nobody took.

    **Q12 — Departments with no employees.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT d.dept_id, d.dept_name, d.city
        FROM departments AS d
        WHERE NOT EXISTS (
            SELECT 1
            FROM employees AS e
            WHERE e.dept_id = d.dept_id
        )
        ORDER BY d.dept_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Legal** (Oakland) — exactly as expected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 10. The `NOT IN` + `NULL` Trap

    In notebook 01 you learned `NOT IN`. It *looks* like it answers the same question as Q12.

    **Q13 — Departments whose ID is not in the employees' list of department IDs.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT dept_id, dept_name
        FROM departments
        WHERE dept_id NOT IN (
            SELECT dept_id
            FROM employees
        )
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    😱 **Zero rows!** Legal has disappeared — with no error message.

    **Why?** Ivan's `dept_id` is `NULL`, so the inner list is `(10, 10, 20, 20, 20, 30, 30, 40, NULL)`.
    For Legal, `50 NOT IN (..., NULL)` means:

    ```
    50 <> 10  AND  50 <> 20  AND ...  AND  50 <> NULL
      TRUE          TRUE                   UNKNOWN
    → the whole condition is UNKNOWN → the row is not kept
    ```

    One `NULL` in the list is enough to make `NOT IN` return **nothing**.

    **Q14 — Fix 1: remove the `NULL`s from the list.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT dept_id, dept_name
        FROM departments
        WHERE dept_id NOT IN (
            SELECT dept_id
            FROM employees
            WHERE dept_id IS NOT NULL
        )
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Legal is back. **Fix 2** is simply `NOT EXISTS` (Q12) — it does not have this trap,
    because `EXISTS` only asks *"did any row match?"*, and a `NULL` never matches.

    > ✅ **Rule:** to find "rows with no match", prefer **`NOT EXISTS`**.
    > If you use `NOT IN`, make sure the list can never contain `NULL`.

    `NOT EXISTS` works in the other direction too.

    **Q15 — Employees whose department does not exist in `departments`.**
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT e.name, e.dept_id
        FROM employees AS e
        WHERE NOT EXISTS (
            SELECT 1
            FROM departments AS d
            WHERE d.dept_id = e.dept_id
        )
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Ivan** — the new hire still waiting for a department. A useful data-quality check!

    ### Which tool when?

    | Question | Good choice |
    |---|---|
    | Compare each row with **its own group** (department average, maximum…) | correlated subquery |
    | "Does at least one matching row exist?" | `EXISTS` |
    | "Is there **no** matching row?" | `NOT EXISTS` (safe with `NULL`) |
    | "Is this value in a fixed list?" | `IN` |
    | "I need columns from both tables" | `JOIN` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    salary_slider = mo.ui.slider(
        start=50000, stop=110000, step=5000, value=90000,
        label="Salary threshold", show_value=True,
    )
    mo.vstack([
        mo.md(r"""
    ---
    ## 11. Try It Yourself 🎛️

    Move the slider. Which departments have **at least one** employee earning more than the threshold
    (`EXISTS`), and which have **none** (`NOT EXISTS`)?
    """),
        salary_slider,
    ])
    return (salary_slider,)


@app.cell(hide_code=True)
def _(con, mo, salary_slider):
    _t = salary_slider.value
    _yes = con.execute(
        """
        SELECT d.dept_name
        FROM departments AS d
        WHERE EXISTS (
            SELECT 1 FROM employees AS e
            WHERE e.dept_id = d.dept_id AND e.salary > ?
        )
        ORDER BY d.dept_id
        """,
        [_t],
    ).fetchdf()
    _no = con.execute(
        """
        SELECT d.dept_name
        FROM departments AS d
        WHERE NOT EXISTS (
            SELECT 1 FROM employees AS e
            WHERE e.dept_id = d.dept_id AND e.salary > ?
        )
        ORDER BY d.dept_id
        """,
        [_t],
    ).fetchdf()
    mo.hstack(
        [
            mo.vstack([mo.md(f"**`EXISTS` — someone earns > {_t:,}**"), _yes]),
            mo.vstack([mo.md(f"**`NOT EXISTS` — nobody earns > {_t:,}**"), _no]),
        ],
        widths="equal",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    👀 **Notice:** the two lists always add up to all **5** departments. And **Legal is always on the
    `NOT EXISTS` side** — it has no employees, so "nobody earns more than X" is true for any X.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 12. Exercises

    Write each query in the empty cell below it, then open the solution to check.

    **E1.** Show the employees who earn **less** than the average of their own department.
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
    SELECT e.name, e.dept_id, e.salary
    FROM employees AS e
    WHERE e.salary < (
        SELECT AVG(x.salary)
        FROM employees AS x
        WHERE x.dept_id = e.dept_id
    )
    ORDER BY e.dept_id, e.salary;
    ```
    **3 rows:** Bob (Sales), Emma (Engineering), Farid (Marketing).
    Hannah *equals* her department's average, and Ivan's comparison is unknown — neither is kept.
    Q5 (4 rows) + E1 (3 rows) + Hannah + Ivan = all 9 employees.
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **E2.** Show the departments where **nobody** earns more than 60,000.
    *Hint:* `NOT EXISTS` with two conditions inside.
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
    SELECT d.dept_name
    FROM departments AS d
    WHERE NOT EXISTS (
        SELECT 1
        FROM employees AS e
        WHERE e.dept_id = d.dept_id
          AND e.salary > 60000
    )
    ORDER BY d.dept_id;
    ```
    **Sales, HR, Legal.** Alice earns exactly 60,000 — not *more* than 60,000 — so Sales qualifies.
    Legal qualifies because it has no employees at all. If you want only departments that *have*
    employees, add `AND EXISTS (SELECT 1 FROM employees AS e2 WHERE e2.dept_id = d.dept_id)`.
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **E3 (challenge).** Show the employees who are the **only person in their department**.
    *Hint:* "there is **no other** employee in my department" → `NOT EXISTS` with
    `x.emp_id <> e.emp_id`.
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
    SELECT e.name, e.dept_id
    FROM employees AS e
    WHERE e.dept_id IS NOT NULL
      AND NOT EXISTS (
          SELECT 1
          FROM employees AS x
          WHERE x.dept_id = e.dept_id
            AND x.emp_id <> e.emp_id
      )
    ORDER BY e.emp_id;
    ```
    **Hannah** (HR).

    Without the line `e.dept_id IS NOT NULL`, **Ivan** appears too: `x.dept_id = NULL` never matches,
    so "no other employee in my department" is true for him. That is the `NULL` lesson once more —
    always ask what happens to the `NULL` rows.
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🎓 Summary

    - A **correlated subquery** uses a column from the outer query (`WHERE x.dept_id = e.dept_id`),
      so its answer can be **different for each outer row**.
    - Read it as a loop: *for each outer row, run the inner query, then decide.*
    - **Always use aliases** (`e`, `x`) and write `alias.column`. Forgetting them gives a wrong answer, not an error (Q8).
    - **`EXISTS`** is true if the subquery returns at least one row. It never creates duplicates (Q10 vs. Q11).
    - **`NOT EXISTS`** finds rows with no match — the **anti-join** (Q12, Q15).
    - **`NOT IN` returns nothing if the list contains a `NULL`** (Q13). Prefer `NOT EXISTS`.
    - `NULL` never equals anything — not even inside a correlated subquery (Ivan).

    **What's next?**

    - `subqueries_notebook_02.py` — give subqueries a name with `WITH` (CTEs) and build multi-step queries.
    - `subqueries_04_tutorial.md` — the complete reference, with `ANY` / `ALL` and 15 more exercises.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
