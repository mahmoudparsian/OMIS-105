import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    # cell 01
    import marimo as mo

    return (mo,)


@app.cell
def _():
    # cell 02
    import duckdb
    con = duckdb.connect(database=":memory:")
    print("con=", con)
    return (con,)


@app.cell
def _(con):
    # cell 03
    con.execute("""
    CREATE OR REPLACE TABLE orders_test 
    AS
    SELECT * FROM read_csv_auto('orders_data.csv');
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- cell 04
        CREATE OR REPLACE TABLE orders 
        AS
        SELECT * FROM read_csv_auto('orders_data.csv');
        """
    )
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        -- cell 05
        SELECT 'orders_data.csv loaded!' AS status,
               COUNT(*) AS total_rows
        FROM orders;
        """
    )
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   orders
        ORDER BY order_id;
        """
    )
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT order_id,
               customer_name,
               product_name
        FROM   orders
        ORDER BY order_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Products Table
    """)
    return


@app.cell
def _(mo, products2):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS products2
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE sales (
            sale_id     INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(customer_id),
            product_id  INTEGER REFERENCES products(product_id),
            quantity    INTEGER NOT NULL,
            sale_date   DATE NOT NULL
        )
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        INSERT INTO sales VALUES
            (1,  1, 1, 1, '2025-01-10'),
            (2,  1, 2, 2, '2025-01-10'),
            (3,  2, 3, 5, '2025-01-15'),
            (4,  2, 4, 3, '2025-01-15'),
            (5,  3, 1, 1, '2025-02-01'),
            (6,  3, 5, 1, '2025-02-01'),
            (7,  4, 2, 1, '2025-02-05'),
            (8,  4, 6, 4, '2025-02-05'),
            (9,  5, 1, 1, '2025-02-10'),
            (10, 5, 3, 3, '2025-02-10'),
            (11, 6, 4, 10,'2025-02-15'),
            (12, 6, 6, 5, '2025-02-15'),
            (13, 1, 5, 2, '2025-03-01'),
            (14, 1, 3, 4, '2025-03-01'),
            (15, 2, 1, 1, '2025-03-05'),
            (16, 4, 5, 2, '2025-03-10'),
            (17, 5, 2, 2, '2025-03-15'),
            (18, 6, 1, 1, '2025-03-20'),
            (19, 3, 4, 6, '2025-03-25'),
            (20, 4, 3, 2, '2025-03-28')
        """
    )
    return


@app.cell
def _(mo, sales):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM sales 
        ORDER BY sale_id
        """
    )
    return


@app.cell
def _(customers, mo, products, sales):
    df_cust = mo.sql(
        f"""
        SELECT c.customer_name,
               c.tier,
               COUNT(*)                                AS num_orders,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS total_spent
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.customer_name, c.tier
        ORDER BY total_spent DESC
        """
    )
    return


@app.cell
def _(mo, products, sales):
    df_prod = mo.sql(
        f"""
        SELECT p.product_name,
               p.category,
               SUM(s.quantity) AS units_sold,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS revenue
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        GROUP BY p.product_name, p.category
        ORDER BY revenue DESC
        """
    )
    return


@app.cell
def _(mo, products, sales):
    df_monthly = mo.sql(
        f"""
        SELECT STRFTIME(s.sale_date, '%Y-%m')           AS month,
               COUNT(*)                                  AS num_orders,
               ROUND(SUM(p.unit_price * s.quantity), 2)  AS revenue
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        GROUP BY month
        ORDER BY month
        """
    )
    return


if __name__ == "__main__":
    app.run()
