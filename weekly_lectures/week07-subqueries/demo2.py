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
    # Week 7 — Subqueries, Session 2: Going Further

    **OMIS 105 — Introduction to Database Management Systems**

    This notebook follows `slides_2.md`. Same three tables as `demo1.py`:
    `customers` (8), `products` (8), `orders` (14).

    | Part | You will learn |
    |---|---|
    | 1 | `EXISTS` and `NOT EXISTS` |
    | 2 | Subqueries in `FROM` (derived tables) |
    | 3 | Correlated subqueries |
    | 4 | Subquery or JOIN? |
    | 5 | CTEs — `WITH` |

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. `EXISTS` — "Is There at Least One Matching Row?"

    For each customer `c`, the subquery looks for orders of **that**
    customer. `SELECT 1` is a custom: `EXISTS` only cares **whether** a row
    exists.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.customer_id, c.customer_name
        FROM customers AS c
        WHERE EXISTS (SELECT 1
                      FROM orders AS o
                      WHERE o.customer_id = c.customer_id)
        ORDER BY c.customer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `NOT EXISTS` — safe with `NULL`s ✅

    The question `NOT IN` got wrong in Session 1:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.customer_id, c.customer_name
        FROM customers AS c
        WHERE NOT EXISTS (SELECT 1
                          FROM orders AS o
                          WHERE o.customer_id = c.customer_id)
        ORDER BY c.customer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. Subqueries in `FROM` (Derived Tables)

    **"What is the average amount a customer spends?"**

    ### Step 1 — total per customer
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT o.customer_id,
               SUM(o.quantity * p.price) AS total_spent
        FROM orders AS o
        INNER JOIN products AS p
            ON o.product_id = p.product_id
        WHERE o.customer_id IS NOT NULL
        GROUP BY o.customer_id
        ORDER BY o.customer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 2 — put step 1 in `FROM`, give it a name (`AS t`), and average it
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT COUNT(*)                    AS customers,
               ROUND(AVG(total_spent), 2) AS avg_spent
        FROM (
            SELECT o.customer_id,
                   SUM(o.quantity * p.price) AS total_spent
            FROM orders AS o
            INNER JOIN products AS p
                ON o.product_id = p.product_id
            WHERE o.customer_id IS NOT NULL
            GROUP BY o.customer_id
        ) AS t
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. Correlated Subqueries — Run Once per Row

    **"Which products cost more than the average of their own category?"**

    The category averages:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT category,
               ROUND(AVG(price), 2) AS avg_price
        FROM products
        GROUP BY category
        ORDER BY category
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The correlated subquery uses `p.category` from the outer row:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT p.product_name, p.category, p.price
        FROM products AS p
        WHERE p.price > (SELECT AVG(p2.price)
                         FROM products AS p2
                         WHERE p2.category = p.category)
        ORDER BY p.category
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it: how one row is decided

    Pick a product. The cell runs the inner query **for that row only** —
    exactly what the correlated subquery does for every row.
    """)
    return


@app.cell
def _(con, mo):
    _names = [r[0] for r in con.execute(
        "SELECT product_name FROM products ORDER BY product_id"
    ).fetchall()]
    product = mo.ui.dropdown(options=_names, value="Laptop", label="Product:")
    product
    return (product,)


@app.cell
def _(con, mo, product):
    _name, _cat, _price = con.execute(
        "SELECT product_name, category, price FROM products WHERE product_name = ?",
        [product.value],
    ).fetchone()
    _avg = con.execute(
        "SELECT AVG(price) FROM products WHERE category = ?", [_cat]
    ).fetchone()[0]
    _kept = _price > _avg
    mo.md(f"""
    **Outer row:** {_name} — category **{_cat}**, price **{_price}**

    **Inner query for this row:**

    ```sql
    SELECT AVG(p2.price)
    FROM products AS p2
    WHERE p2.category = '{_cat}'      -- p.category from the outer row
    ```

    → **{_avg:.2f}**

    **Test:** {_price} > {_avg:.2f} → **{"✅ kept" if _kept else "❌ dropped"}**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Another correlated subquery: each customer's latest order
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT o.customer_id, o.order_id, o.order_date
        FROM orders AS o
        WHERE o.order_date = (SELECT MAX(o2.order_date)
                              FROM orders AS o2
                              WHERE o2.customer_id = o.customer_id)
        ORDER BY o.customer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. Subquery or JOIN?

    **"Which customers placed an order?"** A JOIN returns one row **per
    order**:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.customer_name
        FROM customers AS c
        INNER JOIN orders AS o
            ON c.customer_id = o.customer_id
        ORDER BY c.customer_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `DISTINCT` removes the duplicates:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT DISTINCT c.customer_name
        FROM customers AS c
        INNER JOIN orders AS o
            ON c.customer_id = o.customer_id
        ORDER BY c.customer_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `IN` returns one row per customer from the start:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.customer_name
        FROM customers AS c
        WHERE c.customer_id IN (SELECT customer_id
                                FROM orders)
        ORDER BY c.customer_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Rule of thumb:** need columns from **both** tables → JOIN. Only
    **checking** another table → `IN` / `EXISTS`.

    ---
    ## 5. CTEs — Give a Subquery a Name

    `WITH name AS (...)` moves the subquery to the top. Read it top to
    bottom. Here `customer_totals` is used **twice**.

    **"Which customers spent more than the average customer?"**
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        WITH customer_totals AS (
            SELECT o.customer_id,
                   SUM(o.quantity * p.price) AS total_spent
            FROM orders AS o
            INNER JOIN products AS p
                ON o.product_id = p.product_id
            WHERE o.customer_id IS NOT NULL
            GROUP BY o.customer_id
        )
        SELECT c.customer_name, ct.total_spent
        FROM customer_totals AS ct
        INNER JOIN customers AS c
            ON ct.customer_id = c.customer_id
        WHERE ct.total_spent > (SELECT AVG(total_spent)
                                FROM customer_totals)
        ORDER BY ct.total_spent DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Which Tool for Which Question?

    | Question | Tool |
    |---|---|
    | "…more than the **average**?" | scalar subquery |
    | "…customers **who** ordered X?" | `IN` (or `EXISTS`) |
    | "…**never** ordered?" | `NOT EXISTS` (or `LEFT JOIN ... IS NULL`) |
    | "…the average **of totals**?" | subquery in `FROM` |
    | "…above **their own group's** average?" | correlated subquery |
    | "…show columns from **both** tables" | JOIN |
    | long, multi-step query | CTE (`WITH`) |

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
