import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="13 - Window Functions")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 13 · Window Functions

    Notebook **13 of 13** · estimated time: **15 minutes**.

    Notebook 07 gave you a first taste of `OVER (...)`. This notebook
    goes further, practically: what a window function actually buys
    you over `GROUP BY`, then a progression from simple to
    intermediate real queries.

    Objectives:

    - Explain how a window function differs from `GROUP BY` (it keeps
      every row instead of collapsing them)
    - Rank rows within groups with `ROW_NUMBER`, `RANK`, and
      `DENSE_RANK` — and know when they disagree
    - Compute a running total with `SUM(...) OVER (...)`
    - Compare a row to the previous one with `LAG(...)`
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
    ## The one idea to hold onto: rows stay rows

    `GROUP BY` (notebook 06) answers "one number per group" — it
    **collapses** every row in a group down to a single output row.
    A window function answers a different question: "for *this* row,
    compute something using a set of *related* rows" — and every
    input row **survives** in the output, now carrying that extra
    computed value alongside its own columns.

    The giveaway syntax is `OVER (...)`. Here's the simplest possible
    case: compare each product's price to its own category's average
    price, without losing any product from the result:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT product_name, category, unit_price,
               round(avg(unit_price) OVER (PARTITION BY category), 2) AS category_avg_price,
               round(unit_price - avg(unit_price) OVER (PARTITION BY category), 2) AS diff_from_avg
        FROM products
        ORDER BY category, unit_price DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All 15 products are still here — `GROUP BY category` would have
    crushed this down to 3 rows, one per category, and you'd have
    lost every individual product's price in the process. `PARTITION
    BY category` tells `avg(unit_price) OVER (...)` "compute this
    average per category," but it doesn't touch how many rows come
    back. That's the whole trick of window functions: aggregate-style
    math, row-level detail.

    ## Ranking rows: `ROW_NUMBER`, `RANK`, `DENSE_RANK`

    All three number rows within a group (or across the whole result,
    if you skip `PARTITION BY`), following an `ORDER BY` you specify
    inside the `OVER (...)`. They only disagree when there's a
    **tie**. Let's rank our 30 customers by how many orders they've
    placed — several customers are tied, so the difference will be
    obvious:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT customer_id, n_orders,
               ROW_NUMBER() OVER (ORDER BY n_orders DESC) AS row_num,
               RANK()       OVER (ORDER BY n_orders DESC) AS rank,
               DENSE_RANK() OVER (ORDER BY n_orders DESC) AS dense_rank
        FROM (
            SELECT customer_id, count(*) AS n_orders
            FROM orders
            GROUP BY customer_id
        )
        ORDER BY n_orders DESC, customer_id
        LIMIT 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Four customers are tied at 5 orders each. Watch what each
    function does with that tie, then what happens on the very next
    row:

    - **`ROW_NUMBER`** hands out `1, 2, 3, 4, 5, ...` no matter what —
      ties get an arbitrary but unique number each.
    - **`RANK`** gives every tied row the *same* number (`1, 1, 1,
      1`), then **skips ahead** to `5` for the next row — because
      four rows already "used up" ranks 1 through 4.
    - **`DENSE_RANK`** also gives tied rows the same number, but
      **doesn't skip** — the next distinct value gets `2`, right
      after.

    Rule of thumb: use `ROW_NUMBER` when you need exactly one row per
    rank (e.g. "just the single top order per customer"); use `RANK`
    or `DENSE_RANK` when ties should visibly share a place, and pick
    `DENSE_RANK` specifically when gaps in the numbering would be
    confusing (e.g. showing "price tier 1, 2, 3" to a user).

    ## Running totals with `SUM(...) OVER (...)`

    Add `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` to an
    `ORDER BY` inside `OVER (...)` and a window function sums
    everything *up to and including* the current row — a running
    total. Here's cumulative revenue by month:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        WITH monthly AS (
            SELECT date_trunc('month', o.order_date) AS month,
                   sum(oi.quantity * oi.unit_price) AS revenue
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY 1
        )
        SELECT month,
               round(revenue, 2) AS revenue,
               round(
                   sum(revenue) OVER (
                       ORDER BY month
                       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                   ),
                   2
               ) AS running_total
        FROM monthly
        ORDER BY month
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each row's `running_total` is that month's revenue plus every
    month before it — the same number you'd get by hand-summing down
    the `revenue` column. No self-join, no correlated subquery,
    just one `OVER (...)` clause.

    ## Comparing a row to its neighbor with `LAG`

    `LAG(column)` reaches back to the *previous* row (by whatever
    `ORDER BY` you give it) so you can compare a row to what came
    right before it — `LEAD(column)` does the same thing but reaches
    *forward*. Let's add month-over-month change to the query above:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        WITH monthly AS (
            SELECT date_trunc('month', o.order_date) AS month,
                   sum(oi.quantity * oi.unit_price) AS revenue
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY 1
        )
        SELECT month,
               round(revenue, 2) AS revenue,
               round(revenue - LAG(revenue) OVER (ORDER BY month), 2) AS change_from_prev_month
        FROM monthly
        ORDER BY month
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first row's `change_from_prev_month` is `NULL` — there is no
    month before the first one, and `LAG` returns `NULL` rather than
    erroring when there's nothing to look back at. Every other row is
    simply "this month's revenue minus last month's," computed
    without a self-join. `LEAD` would answer the mirror-image
    question ("how much will revenue change *next* month?").

    ## Exercises
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **13.1** (simple — `ROW_NUMBER`) — For each customer, number
    their orders in chronological order (their 1st order, 2nd order,
    ...) using `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY
    order_date)`. Show `customer_id`, `order_id`, `order_date`, and
    the row number.
    """)
    return


@app.cell
def _(mo):
    ex1 = mo.ui.text_area(placeholder="SELECT ...", label="13.1", full_width=True, rows=5)
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
            "💡 13.1 solution": mo.md(
                "```sql\n"
                "SELECT customer_id, order_id, order_date,\n"
                "       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_sequence\n"
                "FROM orders\n"
                "ORDER BY customer_id, order_sequence\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **13.2** (simple — `DENSE_RANK`) — Within each category, rank
    products from most to least expensive using `DENSE_RANK`. Show
    `category`, `product_name`, `unit_price`, and the rank.
    """)
    return


@app.cell
def _(mo):
    ex2 = mo.ui.text_area(placeholder="SELECT ...", label="13.2", full_width=True, rows=5)
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
            "💡 13.2 solution": mo.md(
                "```sql\n"
                "SELECT category, product_name, unit_price,\n"
                "       DENSE_RANK() OVER (PARTITION BY category ORDER BY unit_price DESC) AS price_rank\n"
                "FROM products\n"
                "ORDER BY category, price_rank\n"
                "```\n\n"
                "No two products in the same category happen to share a\n"
                "price in this dataset, so `DENSE_RANK` and `ROW_NUMBER`\n"
                "would give identical results here — but `DENSE_RANK` is\n"
                "the right *default* choice for a ranking like this, since\n"
                "it would still make sense the moment a tie ever appeared."
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **13.3** (intermediate — running total) — For each customer,
    compute a running total of their spend over time: join `orders`
    to `order_items` to get one row per order with its total
    (`sum(quantity * unit_price)`), then add a running total **per
    customer**, ordered by `order_date`. Show `customer_id`,
    `order_date`, `order_id`, `order_total`, and `running_total`.
    """)
    return


@app.cell
def _(mo):
    ex3 = mo.ui.text_area(placeholder="WITH ... SELECT ...", label="13.3", full_width=True, rows=9)
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
            "💡 13.3 solution": mo.md(
                "```sql\n"
                "WITH customer_order_totals AS (\n"
                "    SELECT o.customer_id, o.order_date, o.order_id,\n"
                "           sum(oi.quantity * oi.unit_price) AS order_total\n"
                "    FROM orders o\n"
                "    JOIN order_items oi ON o.order_id = oi.order_id\n"
                "    GROUP BY o.customer_id, o.order_date, o.order_id\n"
                ")\n"
                "SELECT customer_id, order_date, order_id, order_total,\n"
                "       sum(order_total) OVER (\n"
                "           PARTITION BY customer_id ORDER BY order_date, order_id\n"
                "           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
                "       ) AS running_total\n"
                "FROM customer_order_totals\n"
                "ORDER BY customer_id, order_date, order_id\n"
                "```\n\n"
                "`PARTITION BY customer_id` is what makes this a *running\n"
                "total per customer* instead of one running total across\n"
                "everybody — each customer's total resets and builds up\n"
                "independently, exactly like `RANK`'s numbering resets per\n"
                "category back in the ranking example above."
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - A window function (`... OVER (...)`) computes a value across a
      set of related rows **without collapsing them** — unlike
      `GROUP BY`, every input row survives in the output.
    - `PARTITION BY` restarts the computation per group; `ORDER BY`
      inside `OVER (...)` controls ranking order, running-total
      order, and what `LAG`/`LEAD` consider "previous"/"next."
    - `ROW_NUMBER`, `RANK`, and `DENSE_RANK` only disagree on ties —
      know the difference before picking one.
    - `SUM(...) OVER (... ROWS BETWEEN UNBOUNDED PRECEDING AND
      CURRENT ROW)` gives a running total; `LAG`/`LEAD` compare a row
      to its neighbor.

    That's the last topic in this course. If you haven't already,
    revisit notebook 12's "after the course" section for where to go
    from here — swapping in your own dataset, DuckDB's docs, and
    marimo's built-in tutorials.

    🎉 Nice work.
    """)
    return


if __name__ == "__main__":
    app.run()
