import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 1: Getting Started with DuckDB and SQL Basics — INSTRUCTOR SOLUTIONS

    ## OMIS 105 — Database Management Systems
    **Week 1 | Answer Key**

    ## Objectives

    - Install DuckDB and connect from Python
    - Load CSV data into a DuckDB table
    - Write basic SQL queries using SELECT, WHERE, ORDER BY, LIMIT
    - Use aggregate functions (COUNT, SUM, AVG, MIN, MAX)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    This notebook connects to DuckDB and loads
    `./data/products.csv` into a table called `products`.
    """)
    return


@app.cell
def _():
    DATA_DIR = "./data"  # CSVs are in week01-database-foundations/data/
    return (DATA_DIR,)


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=":memory:")
    return (con,)


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
    ---
    ## Part 1: Exploration (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** (2 pts) Display the first 10 rows of the `products` table.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** (2 pts) How many products are in the table?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT COUNT(*) AS total_products FROM products
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Answer**: 64 products
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** (3 pts) Distinct categories sorted alphabetically.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Answer**: 8 categories — Beauty, Books, Clothing, Electronics, Food & Grocery, Home & Kitchen, Sports, Toys
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** (3 pts) Describe `products`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        DESCRIBE products
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Answer**: 5 columns — product_id, product_name, category, price, stock_quantity
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Filtering and Sorting (20 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** (3 pts) All "Books" products.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, price
        FROM products
        WHERE category = 'Books'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6.** (3 pts) Products priced $10–$50.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category, price
        FROM products
        WHERE price BETWEEN 10 AND 50
        ORDER BY price ASC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** (3 pts) Products containing "Pro".
    """)
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
    > **Expected matches**: Laptop Pro 15, Blender Pro (and any others)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8.** (4 pts) Electronics or Sports with price > $50.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category, price
        FROM products
        WHERE category IN ('Electronics', 'Sports')
          AND price > 50
        ORDER BY price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9.** (3 pts) Top 5 most expensive products.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category, price
        FROM products
        ORDER BY price DESC
        LIMIT 5
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** (4 pts) Products with zero stock.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, category
        FROM products
        WHERE stock_quantity = 0
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Aggregation (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q11.** (5 pts) Average price of all products.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT ROUND(AVG(price), 2) AS avg_price
        FROM products
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** (5 pts) Total inventory value.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT ROUND(SUM(price * stock_quantity), 2) AS total_inventory_value
        FROM products
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q13.** (5 pts) Electronics category statistics.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
            COUNT(*)             AS num_products,
            ROUND(AVG(price), 2) AS avg_price,
            MIN(price)           AS min_price,
            MAX(price)           AS max_price
        FROM products
        WHERE category = 'Electronics'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: Computed Columns (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q14.** (5 pts) Price with tax.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name,
               price,
               ROUND(price * 1.0925, 2) AS price_with_tax
        FROM products
        ORDER BY price_with_tax DESC
        LIMIT 10
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q15.** (5 pts) Stock status using CASE.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name,
               stock_quantity,
               CASE
                   WHEN stock_quantity = 0 THEN 'Out of Stock'
                   WHEN stock_quantity BETWEEN 1 AND 20 THEN 'Low Stock'
                   ELSE 'In Stock'
               END AS stock_status
        FROM products
        ORDER BY stock_quantity
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Grading note**: Accept any reasonable threshold boundaries. The CASE syntax is what matters.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Challenge (5 bonus points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q16.** Percentage of products per category.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT category,
               COUNT(*) AS count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM products), 1) AS percentage
        FROM products
        GROUP BY category
        ORDER BY percentage DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Note**: Students haven't formally learned GROUP BY yet (that's Week 3), but some
    > may figure it out. Give full credit for any working solution. Also accept
    > solutions using a manual total (64).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Grading Rubric

    | Part | Points |
    |------|--------|
    | Part 1: Exploration | 10 |
    | Part 2: Filtering & Sorting | 20 |
    | Part 3: Aggregation | 15 |
    | Part 4: Computed Columns | 10 |
    | **Subtotal** | **55** |
    | Part 5: Challenge (bonus) | 5 |
    | **Maximum** | **60** |

    **Grading notes**:

    - Deduct 1 point for missing ORDER BY when specified in the question
    - Accept minor syntax variations (single vs double quotes, etc.)
    - Give partial credit for queries that show correct logic but have small syntax errors
    """)
    return


if __name__ == "__main__":
    app.run()
