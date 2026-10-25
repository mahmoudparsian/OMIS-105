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
    mo.md("""
    # OMIS 105 — Midterm Exam Practice 3: Answer Key (Weeks 1–5)

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Instructor:** Dr. Mahmoud Parsian

    **Instructor only — do not publish.** Pair with
    `midterm_exam_practice_3.md` and `midterm_exam_practice_3_answer_key.md`
    (grading rubric).

    ---

    Under each question: the answer, why it is right, and — where it
    helps — the SQL that proves it, run on the exam data. Wrong
    options that are not valid SQL are described, not run.

    Week 5 coverage follows the 2026-10-08 decision: JOINs, LEFT JOIN
    + `IS NULL`, and `COALESCE` only.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: B**
    >
    > A primary key is **unique** and **never `NULL`**. It says nothing about value ranges (A), related rows (C), or storage order (D).
    """)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: C**
    >
    > `ORDER BY salary DESC` sorts highest first, and `LIMIT` must come after `ORDER BY`. A sorts lowest first; B has the clauses in the wrong order (syntax error); D is not valid SQL.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM employees
        ORDER BY salary DESC
        LIMIT 3;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: B**
    >
    > `'%a'` means "ends with a lowercase a": Rafa and Diana. A lists every name with an a anywhere; Alice and Jane do not *end* in a. `LIKE` is case-sensitive.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name
        FROM employees
        WHERE emp_name LIKE '%a';
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: B**
    >
    > The distinct values are 10, 20, and `NULL`. `DISTINCT` treats `NULL` as one value, so it gets its own row → 3 rows.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT DISTINCT dept_id
        FROM employees;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: C**
    >
    > Department 50 does not exist in `departments`, so the foreign key rejects it. 30 and 40 exist. `NULL` is allowed: a foreign key only checks non-`NULL` values. The cell below tries all four inside a transaction and rolls each one back.
    """)
    return


@app.cell
def _(con, mo):
    _lines = []
    for _value in ["30", "NULL", "50", "40"]:
        _sql = f"INSERT INTO employees VALUES (7, 'Omar', 72000, {_value})"
        con.execute("BEGIN TRANSACTION")
        try:
            con.execute(_sql)
            _lines.append(f"| `{_value}` | accepted |")
        except Exception as _err:
            _lines.append(f"| `{_value}` | **rejected** — {type(_err).__name__} |")
        finally:
            con.execute("ROLLBACK")
    mo.md("| dept_id | Result |\n|---|---|\n" + "\n".join(_lines))
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: B**
    >
    > A test on an aggregate must go in `HAVING`, after `GROUP BY`. A puts an aggregate in `WHERE` (error); C never groups; D has the clauses in the wrong order (syntax error). Result: only dept 20 (160,000). Dept 10 = 140,000; the `NULL` group = 150,000, which is not *above* 150,000.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT dept_id, SUM(salary) AS total_salary
        FROM employees
        GROUP BY dept_id
        HAVING SUM(salary) > 150000;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: A**
    >
    > `dept_id = NULL` is never true — it is `NULL` ("unknown") — so no rows match and `COUNT(*)` is 0. The correct test is `IS NULL`, which finds 2. Both are run below.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            (SELECT COUNT(*) FROM employees WHERE dept_id = NULL)  AS equals_null,
            (SELECT COUNT(*) FROM employees WHERE dept_id IS NULL) AS is_null;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: C**
    >
    > `CASE` stops at the first true `WHEN`. High: Rafa, Jane. Medium: Bob 78,000, Charlie 75,000, Diana 70,000 (`>=` includes 70,000). Low: Alice.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT emp_name, salary,
               CASE
                   WHEN salary >= 80000 THEN 'High'
                   WHEN salary >= 70000 THEN 'Medium'
                   ELSE 'Low'
               END AS salary_band
        FROM employees
        ORDER BY salary DESC;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: B**
    >
    > `SUBSTRING('Marketing', 1, 3)` = `'Mar'`, and `UPPER` gives `'MAR'`.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT UPPER(SUBSTRING(dept_name, 1, 3)) AS code
        FROM departments
        WHERE dept_id = 20;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: C**
    >
    > `COUNT(*)` counts rows (6). `COUNT(dept_id)` skips `NULL`s (4). `COUNT(DISTINCT dept_id)` counts different non-`NULL` values: 10 and 20 → 2.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*), COUNT(dept_id), COUNT(DISTINCT dept_id)
        FROM employees;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: A**
    >
    > Only matched rows: Alice, Bob, Rafa, Charlie. Diana and Jane (no department) and Sales and Finance (no employees) drop out.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT e.emp_name, d.dept_name
        FROM employees AS e
        INNER JOIN departments AS d
            ON e.dept_id = d.dept_id;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: D**
    >
    > No join condition, so every employee is paired with every department: 6 × 4 = 24 rows. This is a `CROSS JOIN`.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT e.emp_name, d.dept_name
        FROM employees AS e, departments AS d;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: B**
    >
    > The table whose rows must **all** be kept goes on the left of a `LEFT JOIN`. A and D keep all employees, not all departments; C drops Sales and Finance. (`employees RIGHT JOIN departments` would also be correct.)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT d.dept_name, e.emp_name
        FROM departments AS d
        LEFT JOIN employees AS e ON d.dept_id = e.dept_id;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: B**
    >
    > After the `LEFT JOIN`, Sales has **one row** (with `NULL` employee columns), and `COUNT(*)` counts rows, so it shows 1. The second query fixes it with `COUNT(e.emp_id)`, which skips `NULL`s and shows 0.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT d.dept_name,
               COUNT(*)        AS count_star,
               COUNT(e.emp_id) AS count_emp_id
        FROM departments AS d
        LEFT JOIN employees AS e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
        ORDER BY d.dept_name;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: C**
    >
    > 4 matched rows + 2 employees with no department + 2 departments with no employees = 8.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT e.emp_name, d.dept_name
        FROM employees AS e
        FULL OUTER JOIN departments AS d
            ON e.dept_id = d.dept_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 2 — Written Questions (70 points)

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
    > **Answer: model answer**
    >
    > - `departments.dept_id` is the **primary key** of `departments`. It
    >   identifies each department; it can never be `NULL` or repeated.
    > - `employees.dept_id` is a **foreign key**. It points to
    >   `departments.dept_id` and links each employee to a department.
    >   Any value in it must already exist in `departments`.
    > - A foreign key only checks **non-`NULL`** values. `NULL` means "no
    >   department yet", which is allowed unless the column is also
    >   `NOT NULL`. That is why Diana and Jane can have `NULL`.
    >
    > **Grading:** 3 pts PK, 4 pts FK and the link, 3 pts the `NULL`
    > explanation.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: the 6 rows below**
    >
    > `LEFT JOIN` keeps every row of the left table (`employees`). Diana
    > and Jane have no matching department, so `dept_name` is `NULL`.
    > Sales and Finance do not appear: they are on the right side.
    >
    > **Grading:** 6 pts table (1 per row), 4 pts explanation. −3 if
    > Diana and Jane are missing (an INNER JOIN result).
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT e.emp_name, d.dept_name
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: Marketing 2 / 80,000 and Engineering 2 / 70,000**
    >
    > `INNER JOIN` keeps only departments that have employees, then
    > `GROUP BY` the name. Accept `COUNT(e.emp_id)` and no `ROUND`.
    >
    > **Grading:** 4 pts join, 3 pts `GROUP BY`, 3 pts aggregates with
    > aliases, 2 pts `ORDER BY ... DESC`, 3 pts correct result.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT d.dept_name,
               COUNT(*)                AS num_employees,
               ROUND(AVG(e.salary), 2) AS avg_salary
        FROM employees AS e
        INNER JOIN departments AS d
            ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY avg_salary DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **I2.** Write a query that lists **every** department (all 4) with
    its number of employees (`num_employees`) and its total salary
    (`total_salary`). Departments with no employees must show **0** in
    both columns — not `NULL`, and not 1. Sort by `num_employees`
    (highest first), then by department name.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: 4 rows; Sales and Finance show 0 and 0**
    >
    > `departments LEFT JOIN employees` keeps all 4 departments.
    > `COUNT(e.emp_id)` gives 0, not 1. `COALESCE(SUM(...), 0)` turns
    > the `NULL` sum into 0.
    >
    > **Grading:** 5 pts LEFT JOIN (or `employees RIGHT JOIN
    > departments`), 3 pts `COUNT(e.emp_id)`, 3 pts `COALESCE`, 2 pts
    > `GROUP BY`, 2 pts both sort keys. −5 for an INNER JOIN.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT d.dept_name,
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Common mistake — `COUNT(*)` and no `COALESCE`.** Sales and
    Finance show 1 employee and a `NULL` total:
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT d.dept_name,
               COUNT(*)      AS num_employees,
               SUM(e.salary) AS total_salary
        FROM departments AS d
        LEFT JOIN employees AS e
            ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
        ORDER BY num_employees DESC, d.dept_name;
        """,
        engine=con
    )
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: (a) Sales, Finance — (b) Diana, Jane**
    >
    > The pattern: outer join, then keep the rows where the **other**
    > table's key `IS NULL`.
    >
    > **Grading:** 4 pts (a), 4 pts (b) — must be a `RIGHT JOIN` with
    > `employees` on the right — 2 pts (c). Give 2 of 4 for (b) written as
    > `WHERE dept_id IS NULL` with no join: right here, but not a join,
    > and it would miss a `dept_id` that points to a department that does
    > not exist. −2 for `= NULL`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **(a)**
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT d.dept_id, d.dept_name
        FROM departments AS d
        LEFT JOIN employees AS e
            ON d.dept_id = e.dept_id
        WHERE e.emp_id IS NULL;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **(b)**
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT e.emp_name
        FROM departments AS d
        RIGHT JOIN employees AS e
            ON d.dept_id = e.dept_id
        WHERE d.dept_id IS NULL;
        """,
        engine=con
    )
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Answer: (a) salary test in `ON` — (b) Sales and Finance are missing**
    >
    > After the `LEFT JOIN`, Sales and Finance have `e.salary = NULL`.
    > `NULL >= 75000` is not true, so `WHERE` removes those rows *after*
    > the join, and the query acts like an `INNER JOIN`. In the `ON`
    > clause, the test filters employees *before* the match, so every
    > department is kept.
    >
    > **Grading:** (a) 5 pts — 2 LEFT JOIN, 2 test in `ON`, 1
    > `COUNT(e.emp_id)`. (b) 5 pts — 2 naming Sales and Finance, 3 the
    > reason. Accept `SUM(CASE WHEN e.salary >= 75000 THEN 1 ELSE 0 END)`
    > with a plain `LEFT JOIN`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **(a) Correct — 4 rows:**
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT d.dept_name, COUNT(e.emp_id) AS num_high_earners
        FROM departments AS d
        LEFT JOIN employees AS e
            ON d.dept_id = e.dept_id
           AND e.salary >= 75000
        GROUP BY d.dept_name
        ORDER BY d.dept_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **(b) The classmate's query — only 2 rows:**
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT d.dept_name, COUNT(e.emp_id) AS num_high_earners
        FROM departments AS d
        LEFT JOIN employees AS e ON d.dept_id = e.dept_id
        WHERE e.salary >= 75000
        GROUP BY d.dept_name
        ORDER BY d.dept_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Grading Summary

    | Section | Points |
    |---------|-------:|
    | Part 1: Multiple Choice (15 × 2 pts) | 30 |
    | S1, S2 | 20 |
    | I1, I2 | 30 |
    | A1, A2 | 20 |
    | **Total** | **100** |
    """)
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
