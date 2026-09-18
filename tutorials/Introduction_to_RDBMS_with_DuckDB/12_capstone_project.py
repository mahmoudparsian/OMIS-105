import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="12 - Capstone Project")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 12 · Capstone Project

    Notebook **12 of 12** · estimated time: **15 minutes**.

    You're the analyst for this small shop. Below are five real
    business questions, each requiring you to combine more than one
    idea from notebooks 1–11: joins, `GROUP BY`, subqueries/CTEs,
    and window functions. Then one final open-ended question is
    yours to design from scratch.

    There's no new material here — just you, `con`, and the full
    toolkit.
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
    ## Reference: the schema

    ```
    customers(customer_id PK, first_name, last_name, email, city, state, signup_date)
    employees(employee_id PK, first_name, last_name, title, manager_id FK -> employees)
    products(product_id PK, product_name, category, unit_price, in_stock)
    orders(order_id PK, customer_id FK, employee_id FK, order_date, ship_city)
    order_items(order_id FK, product_id FK, quantity, unit_price)  -- PK is (order_id, product_id)
    ```

    Revenue for a line item is always `quantity * unit_price` from
    `order_items`. Every question below can be answered using only
    these five tables.

    ---

    ## Question 1 — Monthly revenue trend

    Total revenue **per calendar month**, across all orders,
    chronologically. (Hint: `date_trunc('month', some_date)` rounds
    a date down to the first of its month — perfect for grouping.)
    """)
    return


@app.cell
def _(mo):
    ex1 = mo.ui.text_area(placeholder="SELECT ...", label="Q1", full_width=True, rows=6)
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
            "💡 Q1 solution": mo.md(
                "```sql\n"
                "SELECT date_trunc('month', o.order_date) AS month,\n"
                "       round(sum(oi.quantity * oi.unit_price), 2) AS revenue\n"
                "FROM orders o\n"
                "JOIN order_items oi ON o.order_id = oi.order_id\n"
                "GROUP BY month\n"
                "ORDER BY month\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2 — Top 3 customers by lifetime spend

    Show each customer's `first_name`, `last_name`, `state`, and total spend, for the **3 highest-spending customers overall**.
    """)
    return


@app.cell
def _(mo):
    ex2 = mo.ui.text_area(placeholder="SELECT ...", label="Q2", full_width=True, rows=6)
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
            "💡 Q2 solution": mo.md(
                "```sql\n"
                "SELECT c.first_name, c.last_name, c.state,\n"
                "       round(sum(oi.quantity * oi.unit_price), 2) AS total_spend\n"
                "FROM customers c\n"
                "JOIN orders o ON c.customer_id = o.customer_id\n"
                "JOIN order_items oi ON o.order_id = oi.order_id\n"
                "GROUP BY c.first_name, c.last_name, c.state\n"
                "ORDER BY total_spend DESC\n"
                "LIMIT 3\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3 — Rank sales reps by revenue generated

    For each Sales Rep, compute total revenue from orders they handled, and rank them (1 = highest revenue) using a window function. (Hint: a CTE for per-rep revenue, then `RANK() OVER (ORDER BY revenue DESC)` — same shape as notebook 07's product-ranking example.)
    """)
    return


@app.cell
def _(mo):
    ex3 = mo.ui.text_area(placeholder="WITH ... SELECT ...", label="Q3", full_width=True, rows=9)
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
            "💡 Q3 solution": mo.md(
                "```sql\n"
                "WITH rep_revenue AS (\n"
                "    SELECT e.employee_id, e.first_name, e.last_name,\n"
                "           sum(oi.quantity * oi.unit_price) AS revenue\n"
                "    FROM employees e\n"
                "    JOIN orders o ON e.employee_id = o.employee_id\n"
                "    JOIN order_items oi ON o.order_id = oi.order_id\n"
                "    WHERE e.title = 'Sales Rep'\n"
                "    GROUP BY e.employee_id, e.first_name, e.last_name\n"
                ")\n"
                "SELECT first_name, last_name, round(revenue, 2) AS revenue,\n"
                "       RANK() OVER (ORDER BY revenue DESC) AS rank\n"
                "FROM rep_revenue\n"
                "ORDER BY rank\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 4 — Customers who shop across categories

    Find customers who have bought products from **more than one** distinct `category`. Show `customer_id`, `first_name`, and how many distinct categories they've bought from, most categories first.
    """)
    return


@app.cell
def _(mo):
    ex4 = mo.ui.text_area(placeholder="SELECT ...", label="Q4", full_width=True, rows=8)
    ex4
    return (ex4,)


@app.cell
def _(con, ex4, mo):
    def _run(q):
        if not q.strip():
            return mo.md("_Write a query above._")
        try:
            return con.sql(q).df()
        except Exception as e:
            return mo.callout(mo.md(f"**SQL error:** {e}"), kind="danger")

    _run(ex4.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "💡 Q4 solution": mo.md(
                "```sql\n"
                "SELECT c.customer_id, c.first_name,\n"
                "       count(DISTINCT p.category) AS n_categories\n"
                "FROM customers c\n"
                "JOIN orders o ON c.customer_id = o.customer_id\n"
                "JOIN order_items oi ON o.order_id = oi.order_id\n"
                "JOIN products p ON oi.product_id = p.product_id\n"
                "GROUP BY c.customer_id, c.first_name\n"
                "HAVING count(DISTINCT p.category) > 1\n"
                "ORDER BY n_categories DESC\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 5 — Running total of revenue over time

    Using the monthly revenue from Question 1, add a **running (cumulative) total** column — total revenue from the start of the dataset through the end of each month. (Hint: `sum(revenue) OVER (ORDER BY month)`, applied to a CTE of monthly revenue.)
    """)
    return


@app.cell
def _(mo):
    ex5 = mo.ui.text_area(placeholder="WITH ... SELECT ...", label="Q5", full_width=True, rows=9)
    ex5
    return (ex5,)


@app.cell
def _(con, ex5, mo):
    def _run(q):
        if not q.strip():
            return mo.md("_Write a query above._")
        try:
            return con.sql(q).df()
        except Exception as e:
            return mo.callout(mo.md(f"**SQL error:** {e}"), kind="danger")

    _run(ex5.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "💡 Q5 solution": mo.md(
                "```sql\n"
                "WITH monthly AS (\n"
                "    SELECT date_trunc('month', o.order_date) AS month,\n"
                "           sum(oi.quantity * oi.unit_price) AS revenue\n"
                "    FROM orders o\n"
                "    JOIN order_items oi ON o.order_id = oi.order_id\n"
                "    GROUP BY month\n"
                ")\n"
                "SELECT month, round(revenue, 2) AS revenue,\n"
                "       round(sum(revenue) OVER (ORDER BY month), 2) AS running_total\n"
                "FROM monthly\n"
                "ORDER BY month\n"
                "```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final question — design your own

    Pose a business question of your own about this dataset, using
    at least a `JOIN`, a `GROUP BY`, and one of {subquery, CTE,
    window function}. Some starter ideas, if you want one:

    - Which `ship_city` generates the most revenue?
    - Is there a relationship between how long ago a customer signed
      up (`signup_date`) and how much they've spent?
    - Which product has the highest revenue **per unit sold**
      (`revenue / total quantity sold`), among products sold more
      than 5 times total?
    - For each employee, what's the average order value they
      handle, compared to the overall average order value?

    There's no solution key for this one — write your question in
    the first box, your SQL in the second, and check that the result
    actually answers what you asked.
    """)
    return


@app.cell
def _(mo):
    my_question = mo.ui.text_area(
        placeholder="My question: ...",
        label="Your question",
        full_width=True,
        rows=2,
    )
    my_question
    return


@app.cell
def _(mo):
    ex6 = mo.ui.text_area(placeholder="SELECT ...", label="Your query", full_width=True, rows=8)
    ex6
    return (ex6,)


@app.cell
def _(con, ex6, mo):
    def _run(q):
        if not q.strip():
            return mo.md("_Write a query above._")
        try:
            return con.sql(q).df()
        except Exception as e:
            return mo.callout(mo.md(f"**SQL error:** {e}"), kind="danger")

    _run(ex6.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Course complete

    You've gone from "what's a relational database" to writing
    multi-CTE, window-function queries against a real, constrained,
    five-table schema — and along the way, learned marimo's
    reactive model well enough to build your own interactive SQL
    tools. From here:

    - **Keep this folder.** `ecommerce_data.py` and all twelve
      notebooks are yours to reopen, tweak, and reuse as a
      reference or a template for your own datasets.
    - **Swap in your own data.** Point `read_csv_auto` /
      `read_parquet` (notebook 11) at a real file of yours, or write
      a new generator module modeled on `ecommerce_data.py`, and
      revisit any notebook's queries against it.
    - **Go deeper on DuckDB specifically:** its documentation at
      [duckdb.org/docs](https://duckdb.org/docs) covers extensions
      (spatial, full-text search, connecting to Postgres/MySQL
      directly), performance tuning, and its Python/SQL client APIs
      in more depth than a 2-hour course can.
    - **Go deeper on marimo:** `marimo tutorial --help` from your
      terminal lists several built-in interactive tutorials covering
      UI elements, layout, and reactivity in more depth.

    Nice work.
    """)
    return


if __name__ == "__main__":
    app.run()
