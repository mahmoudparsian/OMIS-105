import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 03: Primary Keys & CRUD
    ## Lab 1 — Primary Keys and CRUD on `employees` · Instructor

    Work with a single **employees** table. Learn what a **primary key
    (PK)** is and practice the four **CRUD** operations — **C**reate
    (`INSERT`), **R**ead (`SELECT`), **U**pdate (`UPDATE`), **D**elete
    (`DELETE`) — plus a quick `GROUP BY` review. Run the setup cells
    first, then each question. Answers are filled in.

    Based on `Introduction_to_PK_and_CRUD_01.md` (week 02 lecture
    folder). Same template as the v2 labs: Q3 (predict — duplicate PK),
    Q8 (debug — the missing-`WHERE` `UPDATE`), Q11 (explain — `WHERE` vs
    `HAVING`), Q12 (bonus).

    **Why every question cell calls `reset_employees()` first:**
    `INSERT`/`UPDATE`/`DELETE` change the table, and marimo can re-run
    cells in any order. Resetting at the top of each cell means every
    question starts from the same original 6 rows — so an `INSERT` cell
    can be re-run without tripping its own primary key, and results
    always match the expected answers below.
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    # The PRIMARY KEY on emp_id means DuckDB enforces two rules:
    #   1. unique   -- no two rows may share an emp_id
    #   2. not null -- every row must have an emp_id
    EMPLOYEES_SQL = """
        CREATE OR REPLACE TABLE employees (
            emp_id      INTEGER PRIMARY KEY,
            emp_name    VARCHAR,
            salary      INTEGER,
            country     VARCHAR,
            department  VARCHAR
        );

        INSERT INTO employees VALUES
            (1, 'Alice Chen',    75000, 'USA',     'Sales'),
            (2, 'Bruno Silva',   68000, 'Brazil',  'Marketing'),
            (3, 'Chidi Okafor',  82000, 'Nigeria', 'Engineering'),
            (4, 'Diya Patel',    71000, 'India',   'Engineering'),
            (5, 'Elin Karlsson', 90000, 'Sweden',  'Sales'),
            (6, 'Farid Haidari', 64000, 'UAE',     'Marketing');
    """

    def reset_employees():
        # Rebuild the table with the original 6 rows
        mo.sql(EMPLOYEES_SQL, output=False)

    reset_employees()
    return (reset_employees,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q1. Read the whole table: show every column of every employee.
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    q1 = mo.sql(
        f"""
        SELECT *
        FROM employees;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. Which column is a good primary key? Compare the total row count with the number of **distinct** values in `emp_id`, `emp_name`, `country`, and `department`.

    A column can only be a PK if its distinct count equals the row count
    (every value appears exactly once). Expected: 6 rows; `emp_id` 6,
    `emp_name` 6, `country` 6, `department` 3.

    **Talking point:** `emp_name` and `country` *also* happen to be
    unique in these 6 rows — but only by luck. A 7th "Alice Chen" or a
    second employee in the USA is perfectly possible. A PK must be unique
    for every row the table could *ever* hold, not just today's data —
    that's why real tables add an ID column like `emp_id`.
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    q2 = mo.sql(
        f"""
        SELECT COUNT(*)                   AS total_rows,
               COUNT(DISTINCT emp_id)     AS distinct_emp_id,
               COUNT(DISTINCT emp_name)   AS distinct_emp_name,
               COUNT(DISTINCT country)    AS distinct_country,
               COUNT(DISTINCT department) AS distinct_department
        FROM employees;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. Try to insert a 7th employee who reuses `emp_id = 3`: `(3, 'Zara Ahmed', 70000, 'Egypt', 'Sales')`.

    🔮 **Predict first:** DuckDB **refuses** the insert with a
    `Constraint Error: Duplicate key "emp_id: 3" violates primary key
    constraint`. The table still has 6 rows — Chidi Okafor is untouched.

    **Talking point:** this is the PK doing its job. An error here is
    *good news* — the database is protecting us from two rows that
    claim to be the same employee. (Contrast with Q8, where the
    dangerous query runs with **no** error.)

    The cell below catches the error so it displays nicely; in the
    student copy the cell simply turns red, which is the point.
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    # Predict: error -- emp_id 3 already belongs to Chidi Okafor
    try:
        q3 = mo.sql(
            f"""
            INSERT INTO employees VALUES
                (3, 'Zara Ahmed', 70000, 'Egypt', 'Sales');
            """
        )
    except Exception as e:
        q3 = mo.callout(mo.md(f"**DuckDB refused the insert:** `{e}`"), kind="danger")
    q3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. Create: add a new employee `(7, 'Grace Kim', 77000, 'South Korea', 'Sales')`, then show the whole table to confirm.

    Expected: 7 rows; the original 6 are unchanged.
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    q4 = mo.sql(
        f"""
        INSERT INTO employees VALUES
            (7, 'Grace Kim', 77000, 'South Korea', 'Sales');

        SELECT *
        FROM employees
        ORDER BY emp_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Read one row by primary key: show the employee with `emp_id = 3`.

    Expected: exactly one row — Chidi Okafor. Looking up by PK is the
    fastest and safest way to find exactly one row.
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    q5 = mo.sql(
        f"""
        SELECT *
        FROM employees
        WHERE emp_id = 3;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. Read with a filter: show the name and salary of every employee earning more than 70000.

    Expected: Alice Chen, Chidi Okafor, Diya Patel, Elin Karlsson (4
    rows).
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    q6 = mo.sql(
        f"""
        SELECT emp_name, salary
        FROM employees
        WHERE salary > 70000
        ORDER BY salary DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. Update: move `emp_id = 2` (Bruno Silva) to the `Engineering` department, then show his row to confirm.
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    q7 = mo.sql(
        f"""
        UPDATE employees
        SET department = 'Engineering'
        WHERE emp_id = 2;

        SELECT *
        FROM employees
        WHERE emp_id = 2;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. 🐞 Debug it

    Goal: give Elin Karlsson (`emp_id = 5`) a raise to 95000. Broken
    (well — *silently wrong*) query:

    ```sql
    UPDATE employees
    SET salary = 95000;
    ```

    **The bug:** no `WHERE` clause. `UPDATE` without `WHERE` changes
    **every row** — all 6 employees now earn 95000. No error, because
    it's perfectly valid SQL.

    **The fix:** `WHERE emp_id = 5` — the primary key points at exactly
    one row.

    **Talking point for class:** this is why the PK matters for
    `UPDATE`/`DELETE`, not just for `INSERT`. Habit worth drilling: run
    the `WHERE` clause as a `SELECT` first, check you get the row(s) you
    expect, *then* turn it into an `UPDATE`. (We come back to this
    disaster in week 08 with transactions and `ROLLBACK`.)
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    q8 = mo.sql(
        f"""
        -- Without WHERE, every row gets salary = 95000
        UPDATE employees
        SET salary = 95000
        WHERE emp_id = 5;

        SELECT *
        FROM employees
        ORDER BY emp_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Delete: remove the employee with `emp_id = 1`, then show the remaining rows to confirm the row is gone.

    Expected: 5 rows, `emp_id` 2–6; Alice Chen is gone.
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    q9 = mo.sql(
        f"""
        DELETE FROM employees
        WHERE emp_id = 1;

        SELECT *
        FROM employees
        ORDER BY emp_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. GROUP BY: show the number of employees in each department.

    Expected: Engineering 2, Marketing 2, Sales 2.
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    q10 = mo.sql(
        f"""
        SELECT department, COUNT(*) AS num_employees
        FROM employees
        GROUP BY department
        ORDER BY department;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. Show the highest salary in each department, but only for departments with more than one employee.

    Expected: Engineering 82000, Marketing 68000, Sales 90000 (every
    department has 2 employees, so all 3 pass).

    ✍️ **Explain it (sample answer):** "`WHERE` filters individual rows
    *before* grouping, so it can't see `COUNT(*)` — the count doesn't
    exist yet. `HAVING` filters whole groups *after* they're formed, so
    it can test `COUNT(*) > 1`."
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    q11 = mo.sql(
        f"""
        -- WHERE filters rows before grouping; HAVING filters groups after,
        -- so only HAVING can use COUNT(*)
        SELECT department, MAX(salary) AS highest_salary
        FROM employees
        GROUP BY department
        HAVING COUNT(*) > 1
        ORDER BY department;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional)

    Give every **Engineering** employee a 10% raise (one `UPDATE`), then
    show the total salary per department.

    Expected: Engineering 168300 (90200 + 78100), Marketing 132000,
    Sales 165000.

    **Talking point:** this `UPDATE` deliberately uses a non-PK
    `WHERE` (`department = 'Engineering'`) and touches 2 rows — that's
    fine *when you mean it*. The PK is for "exactly this one row"; other
    conditions are for "every row that matches."
    """)
    return


@app.cell
def _(employees, mo, reset_employees):
    reset_employees()
    q12 = mo.sql(
        f"""
        UPDATE employees
        SET salary = salary * 1.10
        WHERE department = 'Engineering';

        SELECT department, SUM(salary) AS total_salary
        FROM employees
        GROUP BY department
        ORDER BY department;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## ✅ Exit Ticket — before you submit

    (Instructor copy — read a few out loud, anonymously, next class.)
    """)
    return


@app.cell
def _():
    exit_ticket = """
    1. One thing that clicked for you today:


    2. One thing about primary keys or CRUD that is still fuzzy or confusing:


    """
    return


if __name__ == "__main__":
    app.run()
