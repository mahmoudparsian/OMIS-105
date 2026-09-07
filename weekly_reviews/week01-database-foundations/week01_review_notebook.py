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
    return DATA_DIR, con


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # OMIS 105 — Week 1 Review: Querying a Single Table

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    This week is about asking a **single table** the right questions.
    One flat CSV of 20 retail orders, and the six SQL clauses that let
    you slice it any way a manager might ask for.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | See the data | `SELECT *`, specific columns, computed columns |
    | Filter rows | `WHERE`, `AND` / `OR`, `IN`, `BETWEEN`, `LIKE` |
    | Sort and trim | `ORDER BY`, `LIMIT` |
    | Summarize | `DISTINCT`, `COUNT` |

    ### How to Use

    Run the cells from top to bottom. Every database cell takes `con`, the
    DuckDB connection created in the setup cell. Read the markdown between
    queries — it explains the *why*, not just the *how*.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Setup — Load the CSV into DuckDB

    `orders_data.csv` lives in this folder's `data/` directory. DuckDB can read
    a CSV straight into a table — no import wizard, no schema definition.
    """)
    return


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE orders AS
            SELECT * FROM read_csv_auto('{DATA_DIR}/orders_data.csv');
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT 'orders_data.csv loaded!' AS status,
               COUNT(*) AS total_rows
        FROM orders;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1.1 — SELECT * (See Everything)

    The simplest SQL query: "show me all the data."
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
            FROM   orders
            ORDER BY order_id;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1.2 — SELECT Specific Columns

    You rarely need *all* columns. Pick just the ones you care about:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT order_id,
                   customer_name,
                   product_name,
                   unit_price,
                   quantity
            FROM   orders
            ORDER BY order_id;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1.3 — Computed Columns

    SQL can do math. Let's compute the **total** for each order:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT order_id,
                   customer_name,
                   product_name,
                   unit_price,
                   quantity,
                   ROUND(unit_price * quantity, 2) AS order_total
            FROM   orders
            ORDER BY order_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1.4 — WHERE (Filter Rows)

    > *Business question: "Show me only the Electronics orders."*

    `WHERE` keeps only the rows that match a condition.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT order_id, customer_name, product_name, unit_price
            FROM   orders
            WHERE  category = 'Electronics'
            ORDER BY order_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### WHERE with comparison operators

    Orders where the total exceeds $100.

    **Note:** `WHERE` runs BEFORE `SELECT`, so we cannot use
    the alias `order_total` here — we must repeat the expression.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT order_id,
                   customer_name,
                   product_name,
                   unit_price * quantity AS order_total
            FROM   orders
            WHERE  unit_price * quantity > 100
            ORDER BY order_total DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### Why `unit_price * quantity` instead of `order_total`?

    You might wonder: we defined `order_total` in the SELECT — why can't we use it in WHERE?

    The answer is **SQL's execution order**. SQL does NOT process your query top-to-bottom.
    It follows this order:

    ```
    1. FROM       ← pick the table
    2. WHERE      ← filter rows         (aliases do NOT exist yet!)
    3. GROUP BY   ← group rows
    4. HAVING     ← filter groups
    5. SELECT     ← compute columns      (aliases are created HERE)
    6. ORDER BY   ← sort results          (aliases ARE available here)
    7. LIMIT      ← return top N
    ```

    Since WHERE (step 2) runs **before** SELECT (step 5), the alias `order_total` does not exist yet.
    That's why we must repeat the expression: `WHERE unit_price * quantity > 100`.

    Notice that ORDER BY (step 6) runs **after** SELECT — so `ORDER BY order_total DESC` works fine.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### WHERE with AND / OR
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- -------------------------------------
        -- Gold customers who bought Electronics
        -- -------------------------------------
            SELECT order_id, customer_name, product_name, unit_price
            FROM   orders
            WHERE  customer_tier = 'Gold'
              AND  category = 'Electronics'
            ORDER BY order_id
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Orders from San Jose OR Santa Clara
        SELECT order_id, customer_name, customer_city, product_name
        FROM   orders
        WHERE  customer_city = 'San Jose'
           OR  customer_city = 'Santa Clara'
        ORDER BY customer_city, order_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### WHERE with IN (cleaner than multiple ORs)
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Same as above, but cleaner
        SELECT order_id, customer_name, customer_city, product_name
        FROM   orders
        WHERE  customer_city IN ('San Jose', 'Santa Clara')
        ORDER BY customer_city, order_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### WHERE with BETWEEN
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Orders placed in February 2025
        SELECT order_id, customer_name, product_name, order_date
        FROM   orders
        WHERE  order_date BETWEEN '2025-02-01' AND '2025-02-28'
        ORDER BY order_date
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### WHERE with LIKE (pattern matching)
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Products that start with 'L'
        SELECT DISTINCT product_name
        FROM   orders
        WHERE  product_name LIKE 'L%'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1.5 — ORDER BY (Sort Results)

    > *Business question: "What are our most expensive orders?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT order_id,
               customer_name,
               product_name,
               unit_price * quantity AS order_total
        FROM   orders
        ORDER BY order_total DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Sorting by multiple columns
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Sort by city (A-Z), then by order_total (highest first)
        SELECT order_id,
               customer_name,
               customer_city,
               unit_price * quantity AS order_total
        FROM   orders
        ORDER BY customer_city ASC, order_total DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1.6 — LIMIT (Top N)

    > *Business question: "Show me only the top 5 highest-value orders."*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT order_id,
               customer_name,
               product_name,
               unit_price * quantity AS order_total
        FROM   orders
        ORDER BY order_total DESC
        LIMIT 5
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1.7 — DISTINCT (Unique Values)

    > *Business question: "What cities do our customers come from?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT DISTINCT customer_city
        FROM   orders
        ORDER BY customer_city
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- How many unique customers do we have?
        SELECT DISTINCT customer_name, customer_city, customer_tier
        FROM   orders
        ORDER BY customer_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1.8 — COUNT (How Many?)

    > *Business question: "How many orders do we have? How many unique customers?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT COUNT(*)                      AS total_orders,
               COUNT(DISTINCT customer_name) AS unique_customers,
               COUNT(DISTINCT product_name)  AS unique_products,
               COUNT(DISTINCT category)      AS unique_categories
        FROM   orders
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ### Week 1 Summary

    | Keyword | Purpose | Example |
    |---------|---------|---------|
    | `SELECT` | Choose columns | `SELECT name, price FROM ...` |
    | `WHERE` | Filter rows | `WHERE price > 100` |
    | `AND / OR` | Combine conditions | `WHERE city = 'X' AND tier = 'Gold'` |
    | `IN` | Match a list | `WHERE city IN ('A', 'B')` |
    | `BETWEEN` | Range filter | `WHERE date BETWEEN '...' AND '...'` |
    | `LIKE` | Pattern match | `WHERE name LIKE 'L%'` |
    | `ORDER BY` | Sort results | `ORDER BY price DESC` |
    | `LIMIT` | Top N rows | `LIMIT 5` |
    | `DISTINCT` | Unique values | `SELECT DISTINCT city` |
    | `COUNT` | Count rows | `COUNT(*)`, `COUNT(DISTINCT ...)` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 1 Summary

    | Clause | What It Does | Business Question It Answers |
    |--------|-------------|------------------------------|
    | `SELECT` | Choose columns | "Show me name and price" |
    | `WHERE` | Filter rows | "Only Electronics orders" |
    | `AND` / `OR` | Combine conditions | "Electronics **and** over $500" |
    | `IN` | Match a list | "San Jose, Santa Clara, or Cupertino" |
    | `BETWEEN` | Match a range | "Orders in February" |
    | `LIKE` | Match a pattern | "Products starting with L" |
    | `ORDER BY` | Sort results | "Biggest orders first" |
    | `LIMIT` | Keep the top N | "Top 5 only" |
    | `DISTINCT` | Remove duplicates | "Which cities do we ship to?" |
    | `COUNT` | Count rows | "How many orders?" |

    ### Looking Ahead

    Every query this week ran against one flat table. Alice's city is repeated
    in four rows, and every product price is stored over and over. Week 2 shows
    why that is a problem and how to fix it with multiple tables and `JOIN`.
    """)
    return


if __name__ == "__main__":
    app.run()
