import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb

    # Build the exam database in memory, from the schema and data
    # printed in the exam. Nothing is read from disk, so this
    # notebook works from any folder. Re-run this cell to reset.
    con = duckdb.connect(database=":memory:")
    con.execute("""
    CREATE OR REPLACE TABLE departments (
        dept_id   INT PRIMARY KEY,
        dept_name VARCHAR(50)
    );
    INSERT INTO departments VALUES
        (10, 'Engineering'),
        (20, 'Marketing'),
        (30, 'Sales'),
        (40, 'Finance');

    CREATE OR REPLACE TABLE employees (
        emp_id   INT PRIMARY KEY,
        emp_name VARCHAR(50),
        salary   INT,
        dept_id  INT,
        FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
    );
    INSERT INTO employees (emp_id, emp_name, salary, dept_id) VALUES
        (1, 'Alice',   65000, 10),
        (2, 'Bob',     78000, 20),
        (3, 'Rafa',    82000, 20),
        (4, 'Charlie', 75000, 10),
        (5, 'Diana',   70000, NULL),
        (6, 'Jane',    80000, NULL);
    """)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    def check(df, rows, columns):
        """Compare a result with the expected row count and column names."""
        got_cols = [c.lower() for c in df.columns]
        if got_cols == ["todo"]:
            return mo.callout(mo.md("Not answered yet."), kind="neutral")
        problems = []
        if len(df) != rows:
            problems.append(f"expected **{rows}** rows, got **{len(df)}**")
        if got_cols != [c.lower() for c in columns]:
            problems.append(
                f"expected columns `{', '.join(columns)}`, "
                f"got `{', '.join(df.columns)}`"
            )
        if problems:
            return mo.callout(mo.md("Not yet: " + "; ".join(problems) + "."),
                              kind="warn")
        return mo.callout(
            mo.md(f"Row count and columns match ({rows} rows). "
                  "Now check the values make sense."),
            kind="success")

    return (check,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Midterm Exam Practice 3 (Weeks 1–5)

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Instructor:** Dr. Mahmoud Parsian
    **Database:** Employees & Departments (built in memory by this notebook)

    ---

    This notebook has the same questions as
    `midterm_exam_practice_3.md`, with an empty SQL cell under each one.

    ### How to practice

    1. **Answer each question by hand first**, on paper, the way you
       will on the real exam. The midterm is closed book, with no
       computer.
    2. **Then check yourself** in the SQL cell under the question:
       replace `SELECT 'not answered yet' AS todo;` with a query and
       run it.
    3. For multiple-choice questions, you can run the options one by
       one and compare the results.
    4. Under some written questions, a box tells you whether your row
       count and column names are right. Green means the *shape* is
       right — still look at the values.

    **About `INSERT`:** question 5 asks which `INSERT` is rejected.
    If you try them, an `INSERT` that works **adds a row** and changes
    later answers. Re-run the `duckdb` setup cell at the top to reset
    the data.

    | Part | Questions | Points |
    |------|-----------|-------:|
    | 1. Multiple choice | 1–15 | 30 |
    | 2. Written — Simple | S1–S2 | 20 |
    | 2. Written — Intermediate | I1–I2 | 30 |
    | 2. Written — Advanced | A1–A2 | 20 |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # The Data

    These are the two tables from the exam. Every question uses them.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM departments ORDER BY dept_id;
        """,
        engine=con
    )
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM employees ORDER BY emp_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 1 — Multiple Choice (30 points, 2 pts each)

    Choose the single best answer for each question.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1. (Week 1) `dept_id` is the **primary key** of `departments`. What does this guarantee?

    A) Every `dept_id` value is greater than zero

    B) Every row has a `dept_id`, and no two rows have the same `dept_id`

    C) Every department has at least one employee

    D) The rows are always stored in `dept_id` order
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 1: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2. (Week 1) Which query returns the **3 highest-paid** employees, highest first?

    A) `SELECT * FROM employees ORDER BY salary LIMIT 3;`

    B) `SELECT * FROM employees LIMIT 3 ORDER BY salary DESC;`

    C) `SELECT * FROM employees ORDER BY salary DESC LIMIT 3;`

    D) `SELECT * FROM employees WHERE salary DESC LIMIT 3;`
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 2: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3. (Week 1) What does this query return?

    ```sql
    SELECT emp_name
    FROM employees
    WHERE emp_name LIKE '%a';
    ```

    A) Alice, Rafa, Diana, Jane

    B) Rafa, Diana

    C) Alice

    D) No rows
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 3: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 4. (Week 1) How many rows does this query return?

    ```sql
    SELECT DISTINCT dept_id
    FROM employees;
    ```

    A) 2

    B) 3

    C) 4

    D) 6
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 4: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 5. (Week 2) Because of the **foreign key** on `employees.dept_id`, which `INSERT` is **rejected**? (Column order: `emp_id, emp_name, salary, dept_id`.)

    A) `INSERT INTO employees VALUES (7, 'Omar', 72000, 30);`

    B) `INSERT INTO employees VALUES (7, 'Omar', 72000, NULL);`

    C) `INSERT INTO employees VALUES (7, 'Omar', 72000, 50);`

    D) `INSERT INTO employees VALUES (7, 'Omar', 72000, 40);`
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 5: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 6. (Week 2) A manager asks: "Which `dept_id` groups have a **total** salary above 150,000?" Which query is correct?

    A)

    ```sql
    SELECT dept_id, SUM(salary) AS total_salary
    FROM employees
    WHERE SUM(salary) > 150000
    GROUP BY dept_id;
    ```

    B)

    ```sql
    SELECT dept_id, SUM(salary) AS total_salary
    FROM employees
    GROUP BY dept_id
    HAVING SUM(salary) > 150000;
    ```

    C)

    ```sql
    SELECT dept_id, salary
    FROM employees
    WHERE salary > 150000;
    ```

    D)

    ```sql
    SELECT dept_id, SUM(salary) AS total_salary
    FROM employees
    HAVING SUM(salary) > 150000
    GROUP BY dept_id;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 6: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 7. (Week 3) What does this query return?

    ```sql
    SELECT COUNT(*)
    FROM employees
    WHERE dept_id = NULL;
    ```

    A) 0

    B) 2

    C) 6

    D) An error
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 7: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 8. (Week 3) How many employees are labeled `'Medium'` by this query?

    ```sql
    SELECT emp_name,
           CASE
               WHEN salary >= 80000 THEN 'High'
               WHEN salary >= 70000 THEN 'Medium'
               ELSE 'Low'
           END AS salary_band
    FROM employees;
    ```

    A) 1

    B) 2

    C) 3

    D) 4
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 8: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 9. (Week 3) What does this query return?

    ```sql
    SELECT UPPER(SUBSTRING(dept_name, 1, 3)) AS code
    FROM departments
    WHERE dept_id = 20;
    ```

    A) `Mar`

    B) `MAR`

    C) `MARKETING`

    D) `ING`
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 9: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 10. (Week 4) What does this query return?

    ```sql
    SELECT COUNT(*), COUNT(dept_id), COUNT(DISTINCT dept_id)
    FROM employees;
    ```

    A) 6, 6, 4

    B) 6, 4, 3

    C) 6, 4, 2

    D) 4, 4, 2
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 10: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 11. (Week 4) How many rows does this query return?

    ```sql
    SELECT e.emp_name, d.dept_name
    FROM employees AS e
    INNER JOIN departments AS d
        ON e.dept_id = d.dept_id;
    ```

    A) 4

    B) 6

    C) 8

    D) 24
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 11: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 12. (Week 4) How many rows does this query return, and why?

    ```sql
    SELECT e.emp_name, d.dept_name
    FROM employees AS e, departments AS d;
    ```

    A) 4 — it is an INNER JOIN on `dept_id`

    B) 6 — one row per employee

    C) 10 — 6 employees plus 4 departments

    D) 24 — there is no join condition, so every employee is paired with every department (a CROSS JOIN)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 12: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 13. (Week 5) A manager wants a list of **every department**, including departments with no employees. Which query is correct?

    A)

    ```sql
    SELECT d.dept_name, e.emp_name
    FROM employees AS e
    LEFT JOIN departments AS d ON e.dept_id = d.dept_id;
    ```

    B)

    ```sql
    SELECT d.dept_name, e.emp_name
    FROM departments AS d
    LEFT JOIN employees AS e ON d.dept_id = e.dept_id;
    ```

    C)

    ```sql
    SELECT d.dept_name, e.emp_name
    FROM departments AS d
    INNER JOIN employees AS e ON d.dept_id = e.dept_id;
    ```

    D)

    ```sql
    SELECT d.dept_name, e.emp_name
    FROM departments AS d
    RIGHT JOIN employees AS e ON d.dept_id = e.dept_id;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 13: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 14. (Week 5) In the result of this query, what number is shown for **Sales**?

    ```sql
    SELECT d.dept_name, COUNT(*) AS num_employees
    FROM departments AS d
    LEFT JOIN employees AS e ON d.dept_id = e.dept_id
    GROUP BY d.dept_name;
    ```

    A) 0

    B) 1

    C) `NULL`

    D) Sales does not appear in the result
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 14: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 15. (Week 5) How many rows does this query return?

    ```sql
    SELECT e.emp_name, d.dept_name
    FROM employees AS e
    FULL OUTER JOIN departments AS d
        ON e.dept_id = d.dept_id;
    ```

    A) 4

    B) 6

    C) 8

    D) 10
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Question 15: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 2 — Written Questions (70 points)

    Write your answer on paper first. For SQL questions, use the
    column names given below each question, in that order.

    ## Simple (10 points each)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **S1.** In two or three sentences, explain the difference between a
    **primary key** and a **foreign key**. Use `departments.dept_id` and
    `employees.dept_id` as your example. Then explain why Diana's
    `dept_id` can be `NULL` even though `employees.dept_id` is a foreign
    key.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    *S1 is a written answer — no SQL needed.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **S2.** Write the **full result** (every row and column) of this
    query. Then explain in one sentence why some rows have `NULL` in
    `dept_name`.

    ```sql
    SELECT e.emp_name, d.dept_name
    FROM employees AS e
    LEFT JOIN departments AS d
        ON e.dept_id = d.dept_id
    ORDER BY e.emp_id;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- S2: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Intermediate (15 points each)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **I1.** Write a query that shows, for each **department name** that
    has at least one employee: the department name, the number of
    employees (`num_employees`), and the average salary (`avg_salary`).
    Sort from highest to lowest average salary. Then write the result
    your query returns.

    **Columns:** `dept_name`, `num_employees`, `avg_salary`
    """)
    return


@app.cell
def _(con, mo):
    i1 = mo.sql(
        f"""
        -- I1: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (i1,)


@app.cell(hide_code=True)
def _(check, i1):
    check(i1, rows=2, columns=["dept_name", "num_employees", "avg_salary"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **I2.** Write a query that lists **every** department (all 4) with
    its number of employees (`num_employees`) and its total salary
    (`total_salary`). Departments with no employees must show **0** in
    both columns — not `NULL`, and not 1. Sort by `num_employees`
    (highest first), then by department name.

    **Columns:** `dept_name`, `num_employees`, `total_salary`
    """)
    return


@app.cell
def _(con, mo):
    i2 = mo.sql(
        f"""
        -- I2: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (i2,)


@app.cell(hide_code=True)
def _(check, i2):
    check(i2, rows=4, columns=["dept_name", "num_employees", "total_salary"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Advanced (10 points each)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **A1.** Finding the gaps.

    (a) Write a query that returns the `dept_id` and `dept_name` of
    every department that has **no employees**. Use a JOIN.

    (b) Write a query that returns the `emp_name` of every employee who
    has **no department**. Use a **RIGHT JOIN**.

    (c) Write the result of each query.

    **Columns:** (a) `dept_id`, `dept_name` — (b) `emp_name`
    """)
    return


@app.cell
def _(con, mo):
    a1a = mo.sql(
        f"""
        -- A1 (a): write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (a1a,)


@app.cell(hide_code=True)
def _(check, a1a):
    check(a1a, rows=2, columns=["dept_id", "dept_name"])
    return


@app.cell
def _(con, mo):
    a1b = mo.sql(
        f"""
        -- A1 (b) — use a RIGHT JOIN: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (a1b,)


@app.cell(hide_code=True)
def _(check, a1b):
    check(a1b, rows=2, columns=["emp_name"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **A2.** A manager asks: "For **every** department, how many
    employees earn **at least 75,000**? Show 0 for departments with
    none."

    (a) Write the query. (Hint: think carefully about *where* the salary
    test goes.)

    (b) A classmate writes this query instead:

    ```sql
    SELECT d.dept_name, COUNT(e.emp_id) AS num_high_earners
    FROM departments AS d
    LEFT JOIN employees AS e ON d.dept_id = e.dept_id
    WHERE e.salary >= 75000
    GROUP BY d.dept_name;
    ```

    Which departments are **missing** from the classmate's result, and
    why? Explain in 1–2 sentences.

    **Columns for (a):** `dept_name`, `num_high_earners`
    """)
    return


@app.cell
def _(con, mo):
    a2a = mo.sql(
        f"""
        -- A2 (a): write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (a2a,)


@app.cell(hide_code=True)
def _(check, a2a):
    check(a2a, rows=4, columns=["dept_name", "num_high_earners"])
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- A2 (b) — try the classmate's query: write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
