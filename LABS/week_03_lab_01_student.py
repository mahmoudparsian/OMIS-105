import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 03: Primary Keys & CRUD
    ## Lab 1 — Primary Keys and CRUD on `employees` · Student

    Work with a single **employees** table. Learn what a **primary key
    (PK)** is and practice the four **CRUD** operations — **C**reate
    (`INSERT`), **R**ead (`SELECT`), **U**pdate (`UPDATE`), **D**elete
    (`DELETE`) — plus a quick `GROUP BY` review. Run the setup cells
    first, then write your SQL in each question cell (replace
    `-- YOUR SQL HERE`).

    **Note:** every question cell starts with `reset_employees()`, which
    rebuilds the table with the original 6 rows. That way each question
    starts fresh, and you can re-run a cell as many times as you like.
    Leave that line in place.

    Same pattern as before: a prediction, a bug, an explain-it, and an
    optional bonus.
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
def _(mo, reset_employees):
    reset_employees()
    q1 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. Which column is a good primary key? Compare the total row count with the number of **distinct** values in `emp_id`, `emp_name`, `country`, and `department`.

    Hint: `COUNT(*)` counts rows; `COUNT(DISTINCT col)` counts different
    values in a column. A PK column must have one distinct value per
    row.

    ✍️ Some columns other than `emp_id` may look unique in these 6 rows.
    Would you still trust them as a PK? Why or why not?
    """)
    return

@app.cell
def _(mo, reset_employees):
    reset_employees()
    q2 = mo.sql(
        f"""
        -- Would you trust emp_name as a PK? Why or why not?
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. Try to insert a 7th employee who reuses `emp_id = 3`: `(3, 'Zara Ahmed', 70000, 'Egypt', 'Sales')`.

    🔮 **Predict first:** what will DuckDB do? Will the table end up
    with 7 rows, 6 rows, or will Chidi Okafor's row be replaced?

    (If the cell turns red, read the message carefully — that may be
    exactly what's supposed to happen.)
    """)
    return

@app.cell
def _(mo, reset_employees):
    reset_employees()
    q3 = mo.sql(
        f"""
        -- Predict: ___
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. Create: add a new employee `(7, 'Grace Kim', 77000, 'South Korea', 'Sales')`, then show the whole table to confirm.

    Hint: you can put two statements in one cell — the `INSERT`, then a
    `SELECT`. The cell displays the result of the last one.
    """)
    return

@app.cell
def _(mo, reset_employees):
    reset_employees()
    q4 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Read one row by primary key: show the employee with `emp_id = 3`.
    """)
    return

@app.cell
def _(mo, reset_employees):
    reset_employees()
    q5 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. Read with a filter: show the name and salary of every employee earning more than 70000.
    """)
    return

@app.cell
def _(mo, reset_employees):
    reset_employees()
    q6 = mo.sql(
        f"""
        -- YOUR SQL HERE
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
def _(mo, reset_employees):
    reset_employees()
    q7 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. 🐞 Debug it

    A classmate wanted to give Elin Karlsson (`emp_id = 5`) a raise to
    95000. They wrote this, and it ran with **no error**:

    ```sql
    UPDATE employees
    SET salary = 95000;

    SELECT * FROM employees ORDER BY emp_id;
    ```

    Run it and look at **every** row, not just Elin's. What went wrong?
    Fix it so that only Elin's salary changes.
    """)
    return

@app.cell
def _(mo, reset_employees):
    reset_employees()
    q8 = mo.sql(
        f"""
        -- What went wrong? (one sentence)
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Delete: remove the employee with `emp_id = 1`, then show the remaining rows to confirm the row is gone.
    """)
    return

@app.cell
def _(mo, reset_employees):
    reset_employees()
    q9 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. GROUP BY: show the number of employees in each department.
    """)
    return

@app.cell
def _(mo, reset_employees):
    reset_employees()
    q10 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. Show the highest salary in each department, but only for departments with more than one employee.

    ✍️ **Explain it:** in one sentence, why do we need `HAVING` here
    instead of putting `COUNT(*) > 1` in a `WHERE` clause?
    """)
    return

@app.cell
def _(mo, reset_employees):
    reset_employees()
    q11 = mo.sql(
        f"""
        -- Explanation:
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional — only if you finish early)

    Give every **Engineering** employee a 10% raise using a single
    `UPDATE`, then show the total salary per department.

    Combines `UPDATE` (with a non-PK `WHERE`), arithmetic, and
    `GROUP BY` + `SUM` — things you've used separately today, not yet
    together.
    """)
    return

@app.cell
def _(mo, reset_employees):
    reset_employees()
    q12 = mo.sql(
        f"""
        -- YOUR SQL HERE (bonus)
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## ✅ Exit Ticket — before you submit
    """)
    return

@app.cell
def _():
    exit_ticket = """
    1. One thing that clicked for you today:


    2. One thing about primary keys or CRUD that is still fuzzy or confusing:


    """
    return (exit_ticket,)

if __name__ == "__main__":
    app.run()
