import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="06 - Aggregation & GROUP BY")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 06 · Aggregation & GROUP BY

    Notebook **6 of 12** · estimated time: **12 minutes**.

    Objectives:

    - Summarize a table with `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
    - Summarize **per group** with `GROUP BY`
    - Filter groups (not rows) with `HAVING`
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect("ecommerce_database.duckdb", read_only=True)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Aggregate functions

    An **aggregate function** collapses many rows into one number.
    The big five: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. Applied with no
    `GROUP BY`, they summarize the *entire* table into a single row:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT
            count(*)                          AS n_line_items,
            sum(quantity * unit_price)         AS total_revenue,
            round(avg(quantity * unit_price),2) AS avg_line_value,
            min(quantity)                      AS smallest_order_qty,
            max(quantity)                      AS largest_order_qty
        FROM order_items
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `quantity * unit_price` is computed per row *before* `sum()`
    totals it — this is "revenue per line item, then add them all
    up," the same arithmetic you'd do by hand, just at database
    speed. `count(*)` counts rows; `count(column)` counts only the
    rows where that column is not `NULL` (a subtly different, and
    occasionally important, distinction).

    ## `GROUP BY` — one row per group, instead of per table

    Add `GROUP BY` and every aggregate function computes **once per
    distinct value** of the grouping column(s), instead of once for
    the whole table. Revenue by product category:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT p.category, round(sum(oi.quantity * oi.unit_price), 2) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The rule that trips people up: **every** non-aggregated column in
    `SELECT` must also appear in `GROUP BY`. SQL can't know which
    single `product_name` to show for a group of 20 rows unless you
    either group by it too, or aggregate it (`max(product_name)`,
    `string_agg(product_name, ', ')`, etc.). DuckDB will raise a
    `Binder Error` if you forget — try removing `p.category` from the
    `GROUP BY` above (in your own scratch query) to see it.

    ## `HAVING` — filtering *groups*

    `WHERE` filters rows **before** grouping happens; `HAVING`
    filters the **groups themselves**, after aggregation — so it's
    the only place you can write a condition on an aggregate like
    `count(*) > 2`. Which customers have placed more than a given
    number of orders?
    """)
    return


@app.cell
def _(mo):
    min_orders = mo.ui.slider(start=1, stop=6, value=3, label="Minimum number of orders")
    min_orders
    return (min_orders,)


@app.cell
def _(con, min_orders):
    con.execute(
        """
        SELECT c.customer_id, c.first_name, c.last_name, count(*) AS n_orders
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        HAVING count(*) >= ?
        ORDER BY n_orders DESC
        """,
        [min_orders.value],
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The order of clauses in a query is fixed — `SELECT ... FROM ...
    WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT ...` — but
    the order they logically *execute* in is different: filter rows
    (`WHERE`) → form groups (`GROUP BY`) → filter groups (`HAVING`) →
    pick columns (`SELECT`) → sort (`ORDER BY`) → cap the count
    (`LIMIT`). Understanding that execution order is what makes it
    click why `WHERE` can't reference an aggregate but `HAVING` can.

    ## Exercises
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **6.1** — For each sales rep (`employees.title = 'Sales Rep'`), count how many orders they've handled. Show `first_name`, `last_name`, and the count, highest first.
    """)
    return


@app.cell
def _(mo):
    ex1 = mo.ui.text_area(placeholder="SELECT ...", label="6.1", full_width=True, rows=5)
    ex1
    return (ex1,)


@app.cell
def _(con, ex1, mo):
    def _run(q):
        if not q.strip():
            return mo.md("_Write a query above._")
        try:
            return con.sql(q).df()
        except Exception as e:
            return mo.callout(mo.md(f"**SQL error:** {e}"), kind="danger")

    _run(ex1.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "💡 6.1 solution": mo.md(
                "```sql\n"
                "SELECT e.first_name, e.last_name, count(*) AS n_orders\n"
                "FROM orders o\n"
                "JOIN employees e ON o.employee_id = e.employee_id\n"
                "WHERE e.title = 'Sales Rep'\n"
                "GROUP BY e.first_name, e.last_name\n"
                "ORDER BY n_orders DESC\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **6.2** — Find the average `unit_price` of products in each `category`, but only for categories with **more than 3** products.
    """)
    return


@app.cell
def _(mo):
    ex2 = mo.ui.text_area(placeholder="SELECT ...", label="6.2", full_width=True, rows=5)
    ex2
    return (ex2,)


@app.cell
def _(con, ex2, mo):
    def _run(q):
        if not q.strip():
            return mo.md("_Write a query above._")
        try:
            return con.sql(q).df()
        except Exception as e:
            return mo.callout(mo.md(f"**SQL error:** {e}"), kind="danger")

    _run(ex2.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "💡 6.2 solution": mo.md(
                "```sql\n"
                "SELECT category, round(avg(unit_price), 2) AS avg_price, count(*) AS n_products\n"
                "FROM products\n"
                "GROUP BY category\n"
                "HAVING count(*) > 3\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **6.3** — For each order (`order_id`), compute its total dollar value (`sum(quantity * unit_price)` from `order_items`). Then find the single **most valuable order**. (Hint: two ways to finish — `ORDER BY ... DESC LIMIT 1`, or wrap it in a subquery with `MAX()`. Either counts.)
    """)
    return


@app.cell
def _(mo):
    ex3 = mo.ui.text_area(placeholder="SELECT ...", label="6.3", full_width=True, rows=5)
    ex3
    return (ex3,)


@app.cell
def _(con, ex3, mo):
    def _run(q):
        if not q.strip():
            return mo.md("_Write a query above._")
        try:
            return con.sql(q).df()
        except Exception as e:
            return mo.callout(mo.md(f"**SQL error:** {e}"), kind="danger")

    _run(ex3.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "💡 6.3 solution": mo.md(
                "```sql\n"
                "SELECT order_id, sum(quantity * unit_price) AS order_total\n"
                "FROM order_items\n"
                "GROUP BY order_id\n"
                "ORDER BY order_total DESC\n"
                "LIMIT 1\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - `COUNT`/`SUM`/`AVG`/`MIN`/`MAX` collapse rows into numbers;
      with no `GROUP BY`, they summarize the whole table.
    - `GROUP BY column` computes them **per distinct value** of
      `column` instead — every non-aggregated `SELECT`ed column must
      appear in the `GROUP BY`.
    - `WHERE` filters rows before grouping; `HAVING` filters groups
      after — that's the only place an aggregate condition belongs.

    ➡️ **Next:** `07_subqueries_and_ctes.py` — nesting queries inside
    queries, and giving them readable names with `WITH`.
    """)
    return


if __name__ == "__main__":
    app.run()
