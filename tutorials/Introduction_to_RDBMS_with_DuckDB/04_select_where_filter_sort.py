import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="04 - SELECT, WHERE, ORDER BY")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 04 · SELECT, WHERE, Filtering & Sorting

    Notebook **4 of 12** · estimated time: **12 minutes**.

    Every notebook from here uses the same one-line setup: load the
    shared e-commerce database from `ecommerce_data.py`.

    Objectives:

    - Select and alias specific columns, filter rows with `WHERE`
    - Use `IN`, `BETWEEN`, `LIKE`, and `NULL`-aware comparisons
    - Sort with `ORDER BY`, limit with `LIMIT`, dedupe with `DISTINCT`
    - Write a **parameterized** query — safely, this time
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
    ## `SELECT` and `WHERE`

    ```sql
    SELECT product_name, unit_price      -- only these columns
    FROM products
    WHERE category = 'Electronics'       -- only rows matching this
    ```

    `SELECT *` means "all columns" — fine for exploring, but naming
    columns explicitly is better practice in real code (it's clearer,
    and doesn't silently break if someone adds a column later).
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT product_name, unit_price
        FROM products
        WHERE category = 'Electronics'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Comparison building blocks

    | Need | SQL |
    |---|---|
    | Multiple exact matches | `state IN ('CA', 'WA', 'TX')` |
    | A range (inclusive) | `unit_price BETWEEN 20 AND 50` |
    | Pattern match | `email LIKE '%@example.com'` (`%` = any chars, `_` = one char) |
    | Combine conditions | `AND`, `OR`, `NOT` — use parentheses when you mix them |
    | Missing values | `city IS NULL` / `city IS NOT NULL` (never `= NULL`) |

    That last one trips everyone up at least once: in SQL, `NULL`
    means *unknown*, and `unknown = unknown` is itself unknown — not
    true. So `WHERE city = NULL` matches **nothing**, ever. You must
    use `IS NULL`.
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT product_name, category, unit_price
        FROM products
        WHERE category IN ('Electronics', 'Stationery')
          AND unit_price BETWEEN 5 AND 50
        ORDER BY unit_price DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sorting, limiting, deduping

    - `ORDER BY column [ASC|DESC]` — sort (ASC is the default); you
      can sort by multiple columns, e.g. `ORDER BY state, city`
    - `LIMIT n` — only return the first `n` rows (after sorting)
    - `DISTINCT` — remove duplicate rows from the result

    Which states do our customers live in — no duplicates, most
    common first?
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT DISTINCT state
        FROM customers
        ORDER BY state
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Making it interactive — and doing it *safely*

    Notebook 02 flagged that pasting user input straight into an
    f-string is how SQL injection happens. Here's the fix:
    **parameterized queries** — write `?` placeholders in the SQL and
    pass the actual values as a separate list. DuckDB substitutes them
    safely, no matter what characters they contain.

    Pick a category and a minimum price:
    """)
    return


@app.cell
def _(con, mo):
    category_picker = mo.ui.dropdown(
        options=sorted(con.sql("SELECT DISTINCT category FROM products").df()["category"]),
        value="Electronics",
        label="Category",
    )
    min_price = mo.ui.slider(start=0, stop=300, step=5, value=20, label="Minimum price ($)")
    mo.hstack([category_picker, min_price])
    return category_picker, min_price


@app.cell
def _(category_picker, con, min_price):
    con.execute(
        """
        SELECT product_name, category, unit_price
        FROM products
        WHERE category = ? AND unit_price >= ?
        ORDER BY unit_price
        """,
        [category_picker.value, min_price.value],
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice: the SQL string itself never changes, no matter what you
    pick — only the two parameters passed alongside it do. That's the
    pattern to reach for any time a query needs to include a value
    that came from a user (or a UI element, or an API request).

    ## Exercises

    Use the text areas below. `con` (with all 5 tables loaded) is
    already available to each one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **4.1** — List every customer's `first_name`, `last_name`, and `city` for customers in `'CA'`, ordered by `last_name`.
    """)
    return


@app.cell
def _(mo):
    ex1 = mo.ui.text_area(placeholder="SELECT ...", label="4.1", full_width=True, rows=4)
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
            "💡 4.1 solution": mo.md(
                """```sql
                SELECT first_name, last_name, city
                FROM customers
                WHERE state = 'CA'
                ORDER BY last_name
                ```"""
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **4.2** — Find every product whose name contains the word `"Desk"` (case-sensitive is fine), showing `product_name` and `unit_price`.
    """)
    return


@app.cell
def _(mo):
    ex2 = mo.ui.text_area(placeholder="SELECT ...", label="4.2", full_width=True, rows=4)
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
            "💡 4.2 solution": mo.md(
                """```sql
                SELECT product_name, unit_price
                FROM products
                WHERE product_name LIKE '%Desk%'
                ```"""
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **4.3** — Show the 5 most expensive products currently `in_stock`, cheapest of the five first.
    """)
    return


@app.cell
def _(mo):
    ex3 = mo.ui.text_area(placeholder="SELECT ...", label="4.3", full_width=True, rows=4)
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
            "💡 4.3 solution": mo.md(
                """```sql
                SELECT product_name, unit_price
                FROM (
                    SELECT product_name, unit_price
                    FROM products
                    WHERE in_stock = TRUE
                    ORDER BY unit_price DESC
                    LIMIT 5
                )
                ORDER BY unit_price ASC
                ```

                (Or: `ORDER BY unit_price DESC LIMIT 5` and just read the
                output bottom-to-top — the subquery above is one way to
                get cheapest-of-the-top-5-first directly, but isn't
                required.)
                """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - `SELECT columns FROM table WHERE condition` is the core query
      shape you'll use constantly.
    - `IN`, `BETWEEN`, `LIKE`, `IS NULL` cover most filtering needs;
      `ORDER BY` / `LIMIT` / `DISTINCT` shape the result.
    - Parameterize (`?` + a values list) any query built from
      variable input — never paste user values into SQL text.

    ➡️ **Next:** `05_joins.py` — a single table only gets you so far;
    joins are how you combine `customers`, `orders`, `products`, and
    more into one answer.
    """)
    return


if __name__ == "__main__":
    app.run()
