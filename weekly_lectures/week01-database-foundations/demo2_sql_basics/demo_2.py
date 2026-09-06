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
    # Week 1: Foundations — DuckDB Demo Notebook
    ## OMIS 105: Database Management Systems

    In this notebook we will:
    1. Install and connect to DuckDB
    2. Load CSV data into tables
    3. Explore table structure
    4. Write basic SQL queries
    5. Use filtering, sorting, and aggregate functions
    """)
    return


@app.cell
def _():
    DATA_DIR = '../data'  # CSVs are in week01-database-foundations/data/
    return (DATA_DIR,)

@app.cell
def _():
    import duckdb
    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Hello DuckDB
    Let's verify DuckDB works with a simple query.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT 'Hello, DuckDB!' AS greeting, 42 AS answer
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Loading CSV Data
    We load our ShopSmart `products.csv` file into a DuckDB table.
    """)
    return


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"""
        SELECT * FROM read_csv_auto('{DATA_DIR}/products.csv') LIMIT 5
        """
    ).fetchdf()
    return


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE products AS
            SELECT * FROM read_csv_auto('{DATA_DIR}/products.csv')
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Exploring Table Structure
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SHOW TABLES
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        DESCRIBE products
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT COUNT(*) AS total_products FROM products
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SUMMARIZE products
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Basic SELECT Queries
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM products LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, price, stock_quantity
                FROM products
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name,
                       price,
                       ROUND(price * 1.0875, 2) AS price_with_tax,
                       stock_quantity * price AS inventory_value
                FROM products
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Filtering with WHERE
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, price
                FROM products
                WHERE category = 'Electronics'
                ORDER BY price DESC
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category, price
                FROM products
                WHERE price < 20
                ORDER BY price
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category, price
                FROM products
                WHERE (category = 'Books' OR category = 'Toys')
                  AND price < 30
                ORDER BY category, price
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category, price
                FROM products
                WHERE category IN ('Electronics', 'Sports', 'Beauty')
                ORDER BY category, price DESC
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category, price
                FROM products
                WHERE price BETWEEN 25 AND 75
                ORDER BY price
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category
                FROM products
                WHERE product_name LIKE '%Pro%'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Sorting with ORDER BY
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, price
                FROM products
                ORDER BY price
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category, price
                FROM products
                ORDER BY price DESC
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category, price
                FROM products
                ORDER BY category ASC, price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. DISTINCT Values
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT DISTINCT category
                FROM products
                ORDER BY category
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT COUNT(DISTINCT category) AS num_categories FROM products
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Aggregate Functions
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    COUNT(*)                  AS total_products,
                    ROUND(AVG(price), 2)      AS avg_price,
                    MIN(price)                AS cheapest,
                    MAX(price)                AS most_expensive,
                    SUM(stock_quantity)       AS total_inventory
                FROM products
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                    COUNT(*)             AS count,
                    ROUND(AVG(price), 2) AS avg_price,
                    MAX(price)           AS max_price
                FROM products
                WHERE category = 'Electronics'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Exporting Results
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        COPY (
            SELECT product_name, category, price
            FROM products
            WHERE price > 100
            ORDER BY price DESC
        ) TO 'expensive_products.csv' (HEADER, DELIMITER ',')
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Working with a Persistent Database
    """)
    return


@app.cell
def _(duckdb, DATA_DIR):
    # Save to a file-based database
    con2 = duckdb.connect('shopmart.duckdb')

    con2.sql(f"""
        CREATE TABLE IF NOT EXISTS products AS
        SELECT * FROM read_csv_auto('{DATA_DIR}/products.csv')
    """)

    con2.sql("SELECT COUNT(*) AS rows FROM products").show()
    con2.close()
    print("Database saved to shopmart.duckdb")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    In this notebook we learned:
    - How to connect to DuckDB in Python
    - Loading CSV data with `read_csv_auto()`
    - Basic SQL: `SELECT`, `FROM`, `WHERE`, `ORDER BY`, `LIMIT`
    - Operators: `=`, `<`, `>`, `LIKE`, `IN`, `BETWEEN`
    - Aggregate functions: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
    - Exporting results and persistent databases

    **Next week**: Relational Thinking — keys, relationships, and multiple tables!
    """)
    return


if __name__ == "__main__":
    app.run()
