import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from pathlib import Path

    import duckdb

    DATA_DIR = Path(__file__).parent / "data"
    con = duckdb.connect(database=":memory:")
    for _t in ["customers", "products", "orders"]:
        con.execute(
            f"CREATE OR REPLACE TABLE {_t} AS "
            f"SELECT * FROM read_csv('{DATA_DIR}/{_t}.csv')"
        )
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 7 — Subqueries, Session 1: A Query Inside a Query

    **OMIS 105 — Introduction to Database Management Systems**

    This notebook follows `slides_1.md`. Run the cells from top to bottom.
    The setup cell loads three small tables from `data/`:

    ```
    customers ──< orders >── products
    ```

    | Table | Rows | Columns |
    |---|---|---|
    | `customers` | 8 | `customer_id`, `customer_name`, `city` |
    | `products` | 8 | `product_id`, `product_name`, `category`, `price` |
    | `orders` | 14 | `order_id`, `customer_id`, `product_id`, `quantity`, `order_date` |

    **Remember three facts about the data:**

    - George Brown and Hana Sato have **never ordered**
    - Blender and Standing Desk were **never ordered**
    - Order 12 is a **guest order**: its `customer_id` is `NULL`

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Look at the Data
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM customers
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM products
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM orders
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. A Two-Step Question

    **"Which products cost more than the average price?"**

    ### Step 1 — find the average
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT AVG(price) AS avg_price
        FROM products
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 2 — type that number by hand 😟
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, price
        FROM products
        WHERE price > 325.875
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It works, but the number is **hard-coded**. If one price changes, the
    query is wrong.

    ### Why not `WHERE price > AVG(price)`?

    This cell runs it and shows DuckDB's real answer:
    """)
    return


@app.cell(hide_code=True)
def _(mo, con):
    _bad = """SELECT product_name, price
    FROM products
    WHERE price > AVG(price)"""
    try:
        con.execute(_bad).fetchdf()
        _msg = "No error?!"
    except Exception as _e:
        _msg = str(_e)
    mo.md(f"""
    ```sql
    {_bad}
    ```

    **DuckDB says:**

    ```
    {_msg}
    ```

    `WHERE` looks at **one row at a time**; `AVG` needs **all rows**. We need the average **first** — a subquery.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. The Subquery: Step 1 Inside Step 2 ✅

    The query in parentheses runs **first**. Its answer (325.875) is put in
    its place, then the outer query runs.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, price
        FROM products
        WHERE price > (SELECT AVG(price)
                       FROM products)
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Scalar subquery = one value

    A subquery that returns **one row and one column** can go anywhere a
    number can go. The most expensive product:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, price
        FROM products
        WHERE price = (SELECT MAX(price)
                       FROM products)
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A scalar subquery in `SELECT`
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name,
               price,
               ROUND((SELECT AVG(price) FROM products), 2)         AS avg_price,
               ROUND(price - (SELECT AVG(price) FROM products), 2) AS difference
        FROM products
        ORDER BY difference DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A real error: the subquery returns more than one row

    A scalar subquery must return **one** value. This one returns three
    Furniture prices:
    """)
    return


@app.cell(hide_code=True)
def _(mo, con):
    _bad = """SELECT product_name
    FROM products
    WHERE price = (SELECT price
                   FROM products
                   WHERE category = 'Furniture')"""
    try:
        con.execute(_bad).fetchdf()
        _msg = "No error?!"
    except Exception as _e:
        _msg = str(_e)
    mo.md(f"""
    ```sql
    {_bad}
    ```

    **DuckDB says:**

    ```
    {_msg}
    ```

    **Fix:** when the subquery returns a **list**, use `IN` instead of `=`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. Subqueries That Return a List: `IN`

    This subquery returns one column, many rows. Notice the `NULL` (the guest
    order) at the end:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT DISTINCT customer_id
        FROM orders
        ORDER BY customer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Which customers have placed an order?**
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT customer_id, customer_name
        FROM customers
        WHERE customer_id IN (SELECT customer_id
                              FROM orders)
        ORDER BY customer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. Nested Subqueries — Read Them Inside-Out

    **"Which customers bought an Electronics product?"** Move the slider to
    run the query one level at a time, from the inside out.
    """)
    return


@app.cell
def _(mo):
    step = mo.ui.slider(1, 3, value=1, label="Level:", show_value=True)
    step
    return (step,)


@app.cell
def _(con, mo, step):
    _levels = {
        1: ("Innermost: the Electronics products",
            """SELECT product_id
    FROM products
    WHERE category = 'Electronics'"""),
        2: ("Middle: customers who ordered one of them",
            """SELECT customer_id
    FROM orders
    WHERE product_id IN (
        SELECT product_id
        FROM products
        WHERE category = 'Electronics'
    )"""),
        3: ("Outer: the names of those customers",
            """SELECT customer_name
    FROM customers
    WHERE customer_id IN (
        SELECT customer_id
        FROM orders
        WHERE product_id IN (
            SELECT product_id
            FROM products
            WHERE category = 'Electronics'
        )
    )
    ORDER BY customer_name"""),
    }
    _title, _sql = _levels[step.value]
    mo.vstack([
        mo.md(f"### Level {step.value} — {_title}"),
        mo.md(f"```sql\n{_sql}\n```"),
        con.execute(_sql).fetchdf(),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At level 2, the list includes `NULL` (the guest order bought Headphones).
    `IN` simply ignores it: `NULL` never equals any `customer_id`.

    ---
    ## 6. `NOT IN` — and Its Trap ⚠️

    **Products never ordered** — works fine (`orders.product_id` has no `NULL`):
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_id, product_name
        FROM products
        WHERE product_id NOT IN (SELECT product_id
                                 FROM orders)
        ORDER BY product_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Customers who never ordered** — the same pattern returns **0 rows**!
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT customer_id, customer_name
        FROM customers
        WHERE customer_id NOT IN (SELECT customer_id
                                  FROM orders)
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it: the guest order switch

    Turn the switch **off** to leave the guest order (the `NULL`) out of the
    list. Watch George and Hana appear.
    """)
    return


@app.cell
def _(mo):
    keep_guest = mo.ui.switch(value=True, label="Include the guest order (customer_id = NULL) in the list")
    keep_guest
    return (keep_guest,)


@app.cell
def _(con, keep_guest, mo):
    _inner = "SELECT customer_id FROM orders"
    if not keep_guest.value:
        _inner += " WHERE customer_id IS NOT NULL"
    _list = sorted({r[0] for r in con.execute(_inner).fetchall()}, key=lambda v: (v is None, v))
    _shown = ", ".join("NULL" if v is None else str(v) for v in _list)
    _sql = f"""SELECT customer_id, customer_name
    FROM customers
    WHERE customer_id NOT IN ({_inner})
    ORDER BY customer_id"""
    _df = con.execute(_sql).fetchdf()
    mo.vstack([
        mo.md(f"**The list:** `{_shown}`"),
        mo.md(f"```sql\n{_sql}\n```"),
        mo.md(f"### {len(_df)} rows"),
        _df,
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Why?** For George (7), `NOT IN` checks `7 <> 1 AND 7 <> 2 AND … AND
    7 <> NULL`. The last comparison is **unknown**, so the whole test is
    unknown, and `WHERE` drops the row.

    ### The fix: `WHERE customer_id IS NOT NULL` inside the subquery
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT customer_id, customer_name
        FROM customers
        WHERE customer_id NOT IN (SELECT customer_id
                                  FROM orders
                                  WHERE customer_id IS NOT NULL)
        ORDER BY customer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    | Kind | Returns | Use it with |
    |---|---|---|
    | Scalar | 1 row, 1 column | `=`, `>`, `<`, or in `SELECT` |
    | List | 1 column, many rows | `IN`, `NOT IN` |

    - The inner query runs first; read nested queries **inside-out**
    - ⚠️ `NOT IN` + one `NULL` in the list = **zero rows**

    **Next:** `demo2.py` — `EXISTS`, subqueries in `FROM`, correlated
    subqueries, and CTEs.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
