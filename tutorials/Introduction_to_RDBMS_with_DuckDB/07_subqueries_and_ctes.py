import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="07 - Subqueries & CTEs")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 07 · Subqueries, CTEs & a Taste of Window Functions

    Notebook **7 of 12** · estimated time: **12 minutes**.

    Objectives:

    - Nest a query inside `WHERE` (scalar and `IN` subqueries)
    - Nest a query inside `FROM` (a derived table)
    - Rewrite nested queries readably with `WITH` (a **CTE**)
    - Get a first look at window functions (`OVER (...)`)
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
    ## Subqueries in `WHERE`

    A **subquery** is a query nested inside another query. The
    simplest case: a *scalar* subquery (one that returns exactly one
    value) used in a comparison. Which products cost more than the
    average product?
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT product_name, unit_price
        FROM products
        WHERE unit_price > (SELECT avg(unit_price) FROM products)
        ORDER BY unit_price
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The inner query `(SELECT avg(unit_price) FROM products)` runs
    first, produces one number, and the outer query compares every
    row's `unit_price` against it. You could compute the average
    yourself and hardcode it — but then the query goes stale the
    moment prices change. The subquery always reflects current data.

    A subquery can also return a **set** of values, for use with
    `IN`. Which customers have ever ordered something in the
    `'Electronics'` category?
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT customer_id, first_name, last_name
        FROM customers
        WHERE customer_id IN (
            SELECT o.customer_id
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE p.category = 'Electronics'
        )
        ORDER BY last_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Subqueries in `FROM` — derived tables

    A subquery can also stand in for a table, anywhere after `FROM`.
    First compute each order's total, *then* average those totals —
    two separate levels of aggregation that a single `GROUP BY`
    can't express directly:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT round(avg(order_total), 2) AS avg_order_value,
               round(max(order_total), 2) AS max_order_value
        FROM (
            SELECT order_id, sum(quantity * unit_price) AS order_total
            FROM order_items
            GROUP BY order_id
        )
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That inner `(SELECT order_id, sum(...) ... GROUP BY order_id)` is
    called a **derived table** — it produces per-order totals, which
    the outer query then treats as if it were a real table and
    aggregates *again*, this time across orders.

    ## `WITH` — the same idea, named and readable

    Nesting subqueries gets hard to read fast, especially several
    levels deep. A **CTE** (Common Table Expression), written with
    `WITH name AS (...)`, gives a subquery a name you can reference
    later in the query — same result, much easier to follow:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        WITH order_totals AS (
            SELECT order_id, sum(quantity * unit_price) AS order_total
            FROM order_items
            GROUP BY order_id
        )
        SELECT round(avg(order_total), 2) AS avg_order_value,
               round(max(order_total), 2) AS max_order_value
        FROM order_totals
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Identical result to the derived-table version above — `WITH` is
    purely a readability tool (DuckDB even runs them the same way
    internally, most of the time). You can chain multiple CTEs,
    each one able to reference the ones defined before it:

    ```sql
    WITH step_one AS (...),
         step_two AS (SELECT ... FROM step_one ...)
    SELECT ... FROM step_two
    ```

    This "build up the answer in labeled steps" style is how most
    real, complex SQL queries are written — you'll use it constantly
    in the capstone (notebook 12).

    ## A first taste of window functions

    A **window function** computes something *across a set of rows
    related to the current row*, without collapsing them into one
    row the way `GROUP BY` does — every input row stays in the
    output. The giveaway syntax is `OVER (...)`. `RANK()` numbers
    rows within groups defined by `PARTITION BY`:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        WITH product_revenue AS (
            SELECT p.product_id, p.product_name, p.category,
                   sum(oi.quantity * oi.unit_price) AS revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, p.category
        )
        SELECT category, product_name, revenue,
               RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rank_in_category
        FROM product_revenue
        ORDER BY category, rank_in_category
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Compare this to `GROUP BY category`: that would collapse each
    category down to one row. Here, every product keeps its own row
    — `PARTITION BY category` just tells `RANK()` to restart the
    count at 1 every time `category` changes. This is DuckDB
    (and modern SQL's) tool for "top N per group," running totals,
    and moving averages — worth knowing exists even if we don't go
    deep on it in this course.

    ## Exercises
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **7.1** (scalar subquery) — List every order whose total value (`sum(quantity * unit_price)` from `order_items`, grouped by `order_id`) is **greater than** the average order total across all orders.
    """)
    return


@app.cell
def _(mo):
    ex1 = mo.ui.text_area(placeholder="WITH ... SELECT ...", label="7.1", full_width=True, rows=7)
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
            "💡 7.1 solution": mo.md(
                "```sql\n"
                "WITH order_totals AS (\n"
                "    SELECT order_id, sum(quantity * unit_price) AS order_total\n"
                "    FROM order_items\n"
                "    GROUP BY order_id\n"
                ")\n"
                "SELECT order_id, order_total\n"
                "FROM order_totals\n"
                "WHERE order_total > (SELECT avg(order_total) FROM order_totals)\n"
                "ORDER BY order_total DESC\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **7.2** (`IN` subquery) — List every product that has **never** appeared in any `order_items` row, using `NOT IN` and a subquery (don't use a `LEFT JOIN` here — that was notebook 05; the point is to practice the subquery form).
    """)
    return


@app.cell
def _(mo):
    ex2 = mo.ui.text_area(placeholder="SELECT ...", label="7.2", full_width=True, rows=6)
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
            "💡 7.2 solution": mo.md(
                "```sql\n"
                "SELECT product_id, product_name\n"
                "FROM products\n"
                "WHERE product_id NOT IN (SELECT product_id FROM order_items)\n"
                "```\n\n"
                "In our dataset every product **has** been ordered at least\n"
                "once, so this correctly returns zero rows — that's a valid\n"
                "(if anticlimactic) result, not a bug."
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **7.3** (CTE) — Using a CTE, compute total revenue per customer, then list only customers whose total spend exceeds $500, highest spender first.
    """)
    return


@app.cell
def _(mo):
    ex3 = mo.ui.text_area(placeholder="WITH ... SELECT ...", label="7.3", full_width=True, rows=8)
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
            "💡 7.3 solution": mo.md(
                "```sql\n"
                "WITH customer_spend AS (\n"
                "    SELECT o.customer_id, sum(oi.quantity * oi.unit_price) AS total_spend\n"
                "    FROM orders o\n"
                "    JOIN order_items oi ON o.order_id = oi.order_id\n"
                "    GROUP BY o.customer_id\n"
                ")\n"
                "SELECT c.first_name, c.last_name, cs.total_spend\n"
                "FROM customer_spend cs\n"
                "JOIN customers c ON cs.customer_id = c.customer_id\n"
                "WHERE cs.total_spend > 500\n"
                "ORDER BY cs.total_spend DESC\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - A subquery is a query nested inside `WHERE` (scalar or `IN`)
      or `FROM` (a derived table).
    - `WITH name AS (...)` (a CTE) names a subquery so multi-step
      logic reads top to bottom instead of nesting inward.
    - Window functions (`... OVER (PARTITION BY ... ORDER BY ...)`)
      compute per-row values relative to a group, without collapsing
      rows the way `GROUP BY` does.

    ➡️ **Next:** `08_constraints_and_data_integrity.py` — go back to
    the constraints from notebook 03 and deliberately break them, to
    see exactly how DuckDB protects your data.
    """)
    return


if __name__ == "__main__":
    app.run()
