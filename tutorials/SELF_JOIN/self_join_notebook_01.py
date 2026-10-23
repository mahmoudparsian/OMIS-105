import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    # CELL #1 — Import Marimo
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    # CELL #2
    mo.md("""
    ## CELL #2 — One table, two roles

    * A **self join** matches rows with other rows in the same table.
    * Give the table two aliases to describe two roles: `e` for employee and `m`
    for manager.
    * There is no special `SELF JOIN` keyword.

    1. The next SQL cell creates our 10-row `employees` table from literal values.

    2. Marimo stores its result as a dataframe that DuckDB can query as a table.

    3. `employee_id` identifies a person; `manager_id` points to their manager's ID.

    4. Alice has no manager (`NULL`). Salaries are annual amounts in USD.

    Read each question, predict the answer, then run its SQL cell.
    """)
    return


@app.cell
def _(mo):
    employees = mo.sql(
        f"""
        -- CELL #3
        SELECT *
        FROM (VALUES
            (1,  'Alice', 'Leadership',  NULL, 150000),
            (2,  'Bob',   'Engineering', 1,    110000),
            (3,  'Carol', 'Sales',       1,    105000),
            (4,  'David', 'Engineering', 2,     90000),
            (5,  'Eva',   'Engineering', 2,    115000),
            (6,  'Frank', 'Sales',       3,     80000),
            (7,  'Grace', 'Sales',       3,     85000),
            (8,  'Henry', 'Engineering', 4,     70000),
            (9,  'Ivy',   'Sales',       3,     78000),
            (10, 'Jack',  'Engineering', 2,     95000)
        ) AS staff(employee_id, name, department, manager_id, salary)
        ORDER BY employee_id;
        """
    )
    return (employees,)


@app.cell
def _(mo):
    # CELL #4
    mo.md("""
    ## CELL #4 — Query 1: Who manages each employee?

    Match an employee's `manager_id` to another employee's `employee_id`.
    `e` supplies the employee name; `m` supplies the manager name.
    For example, David's manager ID is 2, which finds Bob.

    **Expected: 9 rows.** `INNER JOIN` excludes Alice because she has no manager.
    """)
    return


@app.cell
def _(employees, mo):
    query_1 = mo.sql(
        f"""
        -- CELL #5
        SELECT e.name AS employee, m.name AS manager
        FROM employees AS e
        INNER JOIN employees AS m
            ON e.manager_id = m.employee_id
        ORDER BY e.employee_id;
        """
    )
    return


@app.cell
def _(mo):
    # CELL #6
    mo.md("""
    ## CELL #6 — Query 2: Can we keep the boss too?

    Use `LEFT JOIN` to keep every employee, even if no manager matches.
    The matching rule stays the same.

    **Expected: 10 rows.** Alice appears with a `NULL` manager.
    """)
    return


@app.cell
def _(employees, mo):
    query_2 = mo.sql(
        f"""
        -- CELL #7
        SELECT e.name AS employee, m.name AS manager
        FROM employees AS e
        LEFT JOIN employees AS m
            ON e.manager_id = m.employee_id
        ORDER BY e.employee_id;
        """
    )
    return


@app.cell
def _(mo):
    # CELL #8
    mo.md("""
    ## CELL #8 — Query 3: Who earns more than their manager?

    First match each employee to their manager, then compare their salaries.
    `ON` establishes the relationship; `WHERE` filters the matched rows.

    **Expected: 1 row.** Eva earns 115,000; Bob earns 110,000. The difference is 5,000.
    """)
    return


@app.cell
def _(employees, mo):
    query_3 = mo.sql(
        f"""
        -- CELL #9
        SELECT e.name AS employee, e.salary AS employee_salary,
               m.name AS manager, m.salary AS manager_salary,
               e.salary - m.salary AS salary_difference
        FROM employees AS e
        INNER JOIN employees AS m
            ON e.manager_id = m.employee_id
        WHERE e.salary > m.salary
        ORDER BY e.employee_id;
        """
    )
    return


@app.cell
def _(mo):
    # CELL #10
    mo.md("""
    ## CELL #10 — Query 4: Which coworker pairs share a manager?

    Match two employees with the same manager.
    `a.employee_id < b.employee_id` excludes pairing someone with themselves
    and keeps each pair only once. Using `<>` would keep both orders of each pair.

    **Expected: 7 pairs.** Bob–Carol; David–Eva, David–Jack, Eva–Jack;
    Frank–Grace, Frank–Ivy, Grace–Ivy. `NULL` manager IDs do not match.
    """)
    return


@app.cell
def _(employees, mo):
    query_4 = mo.sql(
        f"""
        -- CELL #11
        SELECT a.name AS coworker_1, b.name AS coworker_2,
               a.manager_id AS shared_manager_id
        FROM employees AS a
        INNER JOIN employees AS b
            ON a.manager_id = b.manager_id
           AND a.employee_id < b.employee_id
        ORDER BY a.employee_id, b.employee_id;
        """
    )
    return


@app.cell
def _(mo):
    # CELL #12
    mo.md("""
    ## CELL #12 — Query 5: How many direct reports does everyone have?

    Treat every employee as a potential manager (`m`) and match their reports (`e`).
    `LEFT JOIN` keeps people with no reports. `COUNT(e.employee_id)` counts only
    matches; `COUNT(*)` would incorrectly count an unmatched row as 1.

    **Expected: 10 rows.** Bob has 3 reports, Carol 3, Alice 2, David 1,
    and everyone else 0. These counts include direct reports only.
    """)
    return


@app.cell
def _(employees, mo):
    query_5 = mo.sql(
        f"""
        -- CELL #13
        SELECT m.employee_id, m.name AS employee,
               COUNT(e.employee_id) AS direct_reports
        FROM employees AS m
        LEFT JOIN employees AS e
            ON e.manager_id = m.employee_id
        GROUP BY m.employee_id, m.name
        ORDER BY direct_reports DESC, m.employee_id;
        """
    )
    return


@app.cell
def _(mo):
    # CELL #14
    mo.md("""
    ## CELL #14 — Try it yourself

    Change Eva's salary to 108000 in CELL #3. Query 3 should return zero rows.

    Change Query 4 to match departments instead of managers. Keep the `<` condition.
    You should get 16 pairs: 10 in Engineering and 6 in Sales.

    **Remember:** one table, two aliases, and a condition that connects the rows.

    [DuckDB joins](https://duckdb.org/docs/lts/sql/query_syntax/from) ·
    [Marimo SQL cells](https://docs.marimo.io/guides/working_with_data/sql/)
    """)
    return


if __name__ == "__main__":
    app.run()
