import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # DuckDB SQL Tutorial
    ### Basic → Intermediate → Intermediate+

    This notebook teaches SQL using DuckDB with a simple 12‑row table.

    Each example includes:
    1. Natural‑language query (NLQ)
    2. DuckDB SQL solution
    3. Result table
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect()
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create Sample Table (12 rows)
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE TABLE sales ( id INTEGER, product TEXT, category TEXT, quantity INTEGER, price DOUBLE, region TEXT );
        INSERT INTO sales
        VALUES
            (1, 'Apple', 'Fruit', 10, 1.20, 'North'),
            (2, 'Banana', 'Fruit', 5, 0.80, 'South'),
            (3, 'Orange', 'Fruit', 8, 1.00, 'East'),
            (4, 'Broccoli', 'Vegetable', 4, 2.50, 'West'),
            (5, 'Carrot', 'Vegetable', 6, 1.10, 'North'),
            (6, 'Potato', 'Vegetable', 12, 0.60, 'South'),
            (7, 'Steak', 'Meat', 3, 8.00, 'East'),
            (8, 'Chicken', 'Meat', 7, 5.50, 'West'),
            (9, 'Salmon', 'Meat', 2, 10.00, 'North'),
            (10, 'Milk', 'Dairy', 9, 2.00, 'South'),
            (11, 'Cheese', 'Dairy', 4, 3.50, 'East'),
            (12, 'Yogurt', 'Dairy', 6, 1.80, 'West');
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## View Table
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *
        FROM sales;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. BASIC SQL OPERATIONS
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Show all rows where category = 'Fruit'.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *
        FROM sales
        WHERE category = 'Fruit';
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Show product and price only.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            product,
            price
        FROM sales;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Show distinct categories.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT DISTINCT category
        FROM sales;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. ORDER BY
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Sort products by price ascending.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            product,
            price
        FROM sales
        ORDER BY price ASC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Sort by quantity descending.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            product,
            quantity
        FROM sales
        ORDER BY quantity DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. FILTERING WITH WHERE
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Show items with quantity > 6.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *
        FROM sales
        WHERE quantity > 6;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Show items priced between 1.00 and 3.00.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *
        FROM sales
        WHERE price BETWEEN 1.00
        AND 3.00;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. AGGREGATIONS (SUM, AVG, MIN, MAX)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Compute total quantity sold.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT SUM(quantity) AS total_quantity
        FROM sales;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Compute average price.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT AVG(price) AS avg_price
        FROM sales;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 5. GROUP BY (with HAVING)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Show total quantity per category.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            category,
            SUM(quantity) AS total_qty
        FROM sales
        GROUP BY category;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Show categories where total quantity > 15 (HAVING).
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            category,
            SUM(quantity) AS total_qty
        FROM sales
        GROUP BY category
        HAVING SUM(quantity) > 15;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 6. JOINS
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Create region info table
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE TABLE region_info (
            region  TEXT,
            manager TEXT
        );
    """)
    con.execute("""
        INSERT INTO region_info
        VALUES
            ('North','Alice'),
            ('South','Bob'),
            ('East','Carol'),
            ('West','Dan');
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Join sales with region_info to show manager for each sale.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            s.product,
            s.region,
            r.manager
        FROM sales s
        JOIN region_info r ON s.region = r.region;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 7. WINDOW FUNCTIONS
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Rank products by price (highest first).
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            product,
            price,
            RANK() OVER (
        ORDER BY price DESC) AS price_rank
        FROM sales;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 8. CASE WHEN (Conditional Logic)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Label products as 'Cheap' (<2), 'Moderate' (2–5), 'Expensive' (>5).
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            product,
            price,
            CASE WHEN price < 2 THEN 'Cheap' WHEN price <= 5 THEN 'Moderate' ELSE 'Expensive' END AS price_band
        FROM sales;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 9. SUBQUERIES
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Show products priced above the average price.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            product,
            price
        FROM sales
        WHERE price > (
        SELECT AVG(price)
        FROM sales);
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 10. SET OPERATIONS (UNION, INTERSECT, EXCEPT)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Create small comparison table
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE TABLE compare (
            product TEXT
        );
    """)
    con.execute("""
        INSERT INTO compare
        VALUES
            ('Apple'),
            ('Steak'),
            ('Milk');
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NLQ: Products in both tables (INTERSECT).
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT product
        FROM sales
        INTERSECT
        SELECT product
        FROM compare;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Tutorial Complete
    You have learned:
    - SELECT, WHERE, ORDER BY
    - DISTINCT
    - Aggregations
    - GROUP BY + HAVING
    - JOINs
    - Window functions
    - CASE WHEN
    - Subqueries
    - Set operations
    """)
    return


if __name__ == "__main__":
    app.run()
