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
    con.execute(f"""
        CREATE OR REPLACE TABLE shops AS SELECT * FROM read_csv('{DATA_DIR}/cafe_shops.csv')
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE items AS
        SELECT item_id, item_name, category, CAST(price AS DECIMAL(5, 2)) AS price
        FROM read_csv('{DATA_DIR}/cafe_items.csv')
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE orders AS SELECT * FROM read_csv('{DATA_DIR}/cafe_orders.csv')
    """)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 9 — Ranking Functions, Session 2: `DENSE_RANK` and Ranking Results

    **OMIS 105 — Introduction to Database Management Systems**

    This notebook follows `ranking_slides_2.md`. Run the cells from top to bottom.
    The setup cell loads a small café chain from `data/`:

    ```
    shops ──< orders >── items
    ```

    | Table | Rows |
    |---|---:|
    | `shops` | 4 |
    | `items` | 11 |
    | `orders` | 18 |
    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The menu (`items`)
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT item_id, item_name, category, price
        FROM items
        ORDER BY item_id
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## All three functions, side by side
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT item_name, price,
               ROW_NUMBER() OVER (ORDER BY price DESC, item_name) AS row_num,
               RANK()       OVER (ORDER BY price DESC)            AS rnk,
               DENSE_RANK() OVER (ORDER BY price DESC)            AS dense_rnk
        FROM items
        ORDER BY row_num
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rank `GROUP BY` results: shops by revenue (CTE first, then rank)

    Airport is 4th by `RANK` but 3rd by `DENSE_RANK`.
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH shop_revenue AS (
            SELECT s.shop_name,
                   SUM(o.qty * i.price) AS revenue
            FROM orders AS o
            JOIN items  AS i ON i.item_id = o.item_id
            JOIN shops  AS s ON s.shop_id = o.shop_id
            GROUP BY s.shop_name
        )
        SELECT shop_name, revenue,
               RANK()       OVER (ORDER BY revenue DESC) AS rnk,
               DENSE_RANK() OVER (ORDER BY revenue DESC) AS dense_rnk
        FROM shop_revenue
        ORDER BY revenue DESC, shop_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Units sold per item
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT i.category, i.item_name,
               SUM(o.qty) AS units_sold
        FROM items AS i
        JOIN orders AS o ON o.item_id = i.item_id
        GROUP BY i.category, i.item_name
        ORDER BY i.category, units_sold DESC, i.item_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Best seller per category — `ROW_NUMBER` (exactly 1 per category)
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH units AS (
            SELECT i.category, i.item_name, SUM(o.qty) AS units_sold
            FROM items AS i
            JOIN orders AS o ON o.item_id = i.item_id
            GROUP BY i.category, i.item_name
        ),
        ranked AS (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY category
                                         ORDER BY units_sold DESC, item_name) AS rn
            FROM units
        )
        SELECT category, item_name, units_sold
        FROM ranked
        WHERE rn = 1
        ORDER BY category
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Best seller per category — `RANK` (ties kept: 5 rows)
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH units AS (
            SELECT i.category, i.item_name, SUM(o.qty) AS units_sold
            FROM items AS i
            JOIN orders AS o ON o.item_id = i.item_id
            GROUP BY i.category, i.item_name
        ),
        ranked AS (
            SELECT *, RANK() OVER (PARTITION BY category
                                   ORDER BY units_sold DESC) AS rnk
            FROM units
        )
        SELECT category, item_name, units_sold
        FROM ranked
        WHERE rnk = 1
        ORDER BY category, item_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Second-highest price — `DENSE_RANK` ✅
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH ranked AS (
            SELECT item_name, price,
                   DENSE_RANK() OVER (ORDER BY price DESC) AS price_rank
            FROM items
        )
        SELECT item_name, price
        FROM ranked
        WHERE price_rank = 2
        ORDER BY item_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Same question with `RANK` — no rows ❌
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH ranked AS (
            SELECT item_name, price,
                   RANK() OVER (ORDER BY price DESC) AS price_rank
            FROM items
        )
        SELECT item_name, price
        FROM ranked
        WHERE price_rank = 2
        ORDER BY item_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Same question with `ROW_NUMBER` — the wrong item ❌
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH ranked AS (
            SELECT item_name, price,
                   ROW_NUMBER() OVER (ORDER BY price DESC, item_name) AS price_rank
            FROM items
        )
        SELECT item_name, price
        FROM ranked
        WHERE price_rank = 2
        ORDER BY item_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⚠️ `WHERE` cannot see the rank

    This cell is **meant to fail**.
    """)
    return


@app.cell
def _(con):
    try:
        con.execute("""
        SELECT item_name, price,
               DENSE_RANK() OVER (ORDER BY price DESC) AS price_rank
        FROM items
        WHERE price_rank = 2
        """).fetchdf()
    except Exception as e:
        print("Error:", str(e).splitlines()[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Indexes: two ways to ask for 2026 orders

    Same answer — but only the **range** version lets an index on `order_date` help.
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT COUNT(*) AS orders_2026
        FROM orders
        WHERE YEAR(order_date) = 2026
    """).fetchdf()
    _df
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT COUNT(*) AS orders_2026
        FROM orders
        WHERE order_date >= DATE '2026-01-01'
          AND order_date <  DATE '2027-01-01'
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Your turn

    1. Which item has the **third-highest** price? Which function do you use?
    2. Rank the **categories** by total units sold with `DENSE_RANK`.
    3. Show the **most expensive** item in each category, keeping ties.
    """)
    return


if __name__ == "__main__":
    app.run()
