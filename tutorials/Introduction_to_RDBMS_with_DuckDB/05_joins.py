import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="05 - Joins")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 05 · Joins

    Notebook **5 of 12** · estimated time: **15 minutes**.

    This is the single most important skill in relational databases.
    Everything in notebook 02 about splitting data across linked
    tables only pays off once you can put it back together — that's a
    **join**.

    Objectives:

    - `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN` — what
      each keeps and drops
    - `CROSS JOIN` and why an accidental one is a common bug
    - **Self-joins**, for hierarchical data like `employees.manager_id`
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
    ## The shape of a join

    ```sql
    SELECT ...
    FROM table_a
    JOIN table_b ON table_a.some_id = table_b.some_id
    ```

    `ON` tells the database which rows from each table "belong
    together" — almost always a foreign key on one side matching a
    primary key on the other. Four flavors, illustrated with
    `customers` (30 rows, one — #24 — has never ordered) and `orders`
    (80 rows, all tied to *some* customer):

    | Join type | Keeps |
    |---|---|
    | `INNER JOIN` | Only rows where a match exists on **both** sides |
    | `LEFT JOIN` | **Every** row from the left table, matched data from the right where it exists, else `NULL` |
    | `RIGHT JOIN` | Mirror image of `LEFT JOIN` — every row from the right table |
    | `FULL OUTER JOIN` | Every row from **both** tables, matched where possible |

    ## `INNER JOIN`

    Every order, with the customer's name attached. Customer #24
    (who has no orders) simply won't appear — `INNER JOIN` drops
    anything without a match on both sides.
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT o.order_id, c.first_name, c.last_name, o.order_date, o.ship_city
        FROM orders o
        INNER JOIN customers c ON o.customer_id = c.customer_id
        ORDER BY o.order_id
        LIMIT 8
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two things to notice: `o` and `c` are **table aliases** — short
    names that save typing and, more importantly, disambiguate
    columns that exist in both tables (both have `customer_id`, for
    instance). And `JOIN` alone means `INNER JOIN` — DuckDB (like
    every SQL engine) defaults to inner when you don't say otherwise.

    ## `LEFT JOIN` — finding what's *missing*

    The most common real use of `LEFT JOIN` isn't fetching more
    columns — it's finding rows on the left that have **no** match on
    the right, via `WHERE right_table.key IS NULL`. Which customers
    have never placed an order?
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT c.customer_id, c.first_name, c.last_name
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.order_id IS NULL
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read this carefully: `LEFT JOIN` first keeps *every* customer,
    filling in `NULL` for `orders` columns when there's no matching
    order. The `WHERE o.order_id IS NULL` filter then keeps *only*
    the rows where that fill-in happened — i.e., customers with zero
    orders. Swap it for `INNER JOIN` and re-run: that customer
    disappears entirely, because `INNER JOIN` never produces the
    `NULL`-filled row in the first place.

    ## `RIGHT JOIN` and `FULL OUTER JOIN`

    `RIGHT JOIN` is just `LEFT JOIN` with the tables swapped — DuckDB
    supports it, but most people just rewrite the `FROM`/`JOIN` order
    and use `LEFT JOIN` everywhere for consistency. `FULL OUTER JOIN`
    keeps unmatched rows from **both** sides at once — useful for
    "show me everything, matched or not," e.g. auditing which
    employees have handled orders and which orders (in a hypothetical
    messier dataset) might reference a missing employee:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT e.employee_id, e.first_name, e.title, count(o.order_id) AS orders_handled
        FROM employees e
        FULL OUTER JOIN orders o ON e.employee_id = o.employee_id
        GROUP BY e.employee_id, e.first_name, e.title
        ORDER BY orders_handled DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    (Don't worry about `GROUP BY` / `count()` yet — that's next
    notebook. Focus on the join: managers and the VP show `0`,
    because `FULL OUTER JOIN` kept them even though they never
    appear in `orders`.)

    ## `CROSS JOIN` — every combination, and why it's usually a bug

    `CROSS JOIN` pairs **every** row on the left with **every** row on
    the right — no `ON` condition at all. 30 customers × 15 products
    would be 450 rows, most of them meaningless. It has legitimate
    uses (generating combinations, like every possible size × color),
    but its far more common appearance is **by accident**: forget the
    `ON` clause, or separate two tables with a comma instead of a
    proper join, and you silently get a cartesian product — a result
    set that's technically valid SQL but practically garbage.
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT p.category, s.size
        FROM (SELECT DISTINCT category FROM products) p
        CROSS JOIN (SELECT unnest(['Small', 'Medium', 'Large']) AS size) s
        ORDER BY p.category, s.size
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's a legitimate use — every category paired with every size,
    e.g. to build a product-variant matrix. **Rule of thumb:** if a
    query's row count is way bigger than you expected, check for a
    missing or wrong `ON` clause before anything else.

    ## Self-joins — a table joined to itself

    `employees.manager_id` points back at `employees.employee_id`
    (notebook 02). To show each employee **next to their manager's
    name**, join the table to itself using two different aliases:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT
            staff.first_name || ' ' || staff.last_name AS employee_name,
            staff.title,
            mgr.first_name || ' ' || mgr.last_name AS manager_name
        FROM employees staff
        LEFT JOIN employees mgr ON staff.manager_id = mgr.employee_id
        ORDER BY staff.employee_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `staff` and `mgr` are the *same table*, `employees` — but the two
    aliases let SQL treat them as independent for the purposes of this
    query. `LEFT JOIN` (not `INNER`) matters here too: the VP has no
    manager, and an `INNER JOIN` would silently drop her from the
    results. `||` concatenates strings in DuckDB (and standard SQL).

    ## Exercises
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **5.1** (`INNER JOIN`) — List `order_id`, customer full name, and `order_date` for every order shipped to `'Seattle'`. (9 rows.)
    """)
    return


@app.cell
def _(mo):
    ex1 = mo.ui.text_area(placeholder="SELECT ...", label="5.1", full_width=True, rows=5)
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
            "💡 5.1 solution": mo.md(
                "```sql\n"
                "SELECT o.order_id, c.first_name || ' ' || c.last_name AS customer_name, o.order_date\n"
                "FROM orders o\n"
                "INNER JOIN customers c ON o.customer_id = c.customer_id\n"
                "WHERE o.ship_city = 'Seattle'\n"
                "ORDER BY o.order_date\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **5.2** (`LEFT JOIN`) — Which employees have **never** been assigned to an order? Show `employee_id`, `first_name`, `title`. (Hint: this should return the VP and the two Sales Managers — the Sales Reps are the ones assigned to orders.)
    """)
    return


@app.cell
def _(mo):
    ex2 = mo.ui.text_area(placeholder="SELECT ...", label="5.2", full_width=True, rows=5)
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
            "💡 5.2 solution": mo.md(
                "```sql\n"
                "SELECT e.employee_id, e.first_name, e.title\n"
                "FROM employees e\n"
                "LEFT JOIN orders o ON e.employee_id = o.employee_id\n"
                "WHERE o.order_id IS NULL\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **5.3** (self-join) — For every `order_items` row where `quantity >= 4`, show the product name and the quantity. Then, separately: using the self-join pattern above, list each Sales Rep alongside their manager's `title` (not just name).
    """)
    return


@app.cell
def _(mo):
    ex3 = mo.ui.text_area(placeholder="SELECT ...", label="5.3", full_width=True, rows=6)
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
            "💡 5.3 solution": mo.md(
                "```sql\n"
                "-- part 1\n"
                "SELECT p.product_name, oi.quantity\n"
                "FROM order_items oi\n"
                "JOIN products p ON oi.product_id = p.product_id\n"
                "WHERE oi.quantity >= 4;\n\n"
                "-- part 2\n"
                "SELECT staff.first_name, staff.title AS my_title, mgr.title AS manager_title\n"
                "FROM employees staff\n"
                "JOIN employees mgr ON staff.manager_id = mgr.employee_id\n"
                "WHERE staff.title = 'Sales Rep'\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - `INNER JOIN` keeps only matches; `LEFT`/`RIGHT`/`FULL OUTER`
      keep unmatched rows from one or both sides, filled with `NULL`.
    - `LEFT JOIN ... WHERE right.key IS NULL` is the standard "find
      what's missing" pattern.
    - `CROSS JOIN` (or a missing `ON`) produces every combination —
      watch for unexpectedly huge result sets.
    - A **self-join** is the same table under two aliases — the tool
      for hierarchical/relational data within one table.

    ➡️ **Next:** `06_aggregation_group_by.py` — summarizing joined
    data with `COUNT`, `SUM`, `AVG`, and `GROUP BY`.
    """)
    return


if __name__ == "__main__":
    app.run()
