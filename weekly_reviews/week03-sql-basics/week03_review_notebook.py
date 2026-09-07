import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from plot_helpers import plot_bar, plot_hbar, plot_pie, plot_grouped_bar

    return plot_bar, plot_grouped_bar, plot_hbar, plot_pie


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
    # OMIS 105 — Week 3 Review: Aggregation, Grouping & Subqueries

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    Managers rarely want a list of rows — they want a *number*. This week
    collapses many rows into one answer per group, charts the result, and
    then asks questions that need a query inside a query.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | Summarize groups | `GROUP BY`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` |
    | Filter groups | `HAVING` (and how it differs from `WHERE`) |
    | Group by date | `STRFTIME` for monthly reporting |
    | Chart the answer | `plot_bar`, `plot_hbar`, `plot_pie`, `plot_grouped_bar` |
    | Query inside a query | Scalar subqueries, subqueries in `WHERE` |

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
    mo.md(r"""
    ---
    ## Setup — Rebuild the Normalized Tables

    Week 2 split the flat CSV into three tables: `customers`, `products`, and
    `sales`. This week's queries all run against those tables, so we rebuild
    them here in one step. If you want the full explanation of *why* we split
    them, revisit the Week 2 review notebook.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE customers (
            customer_id   INTEGER PRIMARY KEY,
            customer_name VARCHAR NOT NULL,
            city          VARCHAR NOT NULL,
            tier          VARCHAR NOT NULL
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO customers VALUES
            (1, 'Alice', 'San Jose',      'Gold'),
            (2, 'Bob',   'Santa Clara',   'Silver'),
            (3, 'Carol', 'San Jose',      'Gold'),
            (4, 'David', 'San Francisco', 'Bronze'),
            (5, 'Eva',   'Santa Clara',   'Silver'),
            (6, 'Frank', 'San Jose',      'Gold')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE products (
            product_id   INTEGER PRIMARY KEY,
            product_name VARCHAR NOT NULL,
            category     VARCHAR NOT NULL,
            unit_price   DECIMAL(10,2) NOT NULL
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO products VALUES
            (1, 'Laptop',    'Electronics',  999.99),
            (2, 'Mouse',     'Electronics',   29.99),
            (3, 'Notebook',  'Office',        12.99),
            (4, 'Pen Set',   'Office',         8.99),
            (5, 'Backpack',  'Accessories',   49.99),
            (6, 'USB Cable', 'Electronics',    9.99)
        """
    )
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        -- Add Grace — safe to re-run (skips if she already exists)
        INSERT INTO customers
        SELECT 7, 'Grace', 'Palo Alto', 'Gold'
        WHERE NOT EXISTS (SELECT 1 FROM customers WHERE customer_id = 7)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3.1 — GROUP BY & Aggregate Functions

    `GROUP BY` collapses many rows into **one row per group**.
    Aggregate functions tell SQL *how* to collapse them.

    | Function | What It Computes |
    |----------|-----------------|
    | `COUNT(*)` | Number of rows in each group |
    | `SUM(col)` | Total of a numeric column |
    | `AVG(col)` | Average value |
    | `MIN(col)` | Smallest value |
    | `MAX(col)` | Largest value |
    | `ROUND(val, n)` | Round to n decimal places |

    > *"How many orders and how much revenue per product category?"*
    """)
    return


@app.cell
def _(con):
    df_cat = con.execute(
        f"""
        SELECT p.category,
               COUNT(*)                                AS num_orders,
               SUM(s.quantity)                         AS units_sold,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS revenue
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC
        """
    ).fetchdf()
    df_cat
    return (df_cat,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Revenue by Category
    """)
    return


@app.cell
def _(df_cat, plot_bar):
    plot_bar(df_cat, x='category', y='revenue',
             title='Revenue by Product Category', ylabel='Revenue', dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"Revenue per customer — who are our biggest spenders?"*
    """)
    return


@app.cell
def _(con):
    df_cust = con.execute(
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
    ).fetchdf()
    df_cust
    return (df_cust,)


@app.cell
def _(df_cust, plot_hbar):
    plot_hbar(df_cust, x='total_spent', y='customer_name',
              title='Total Spending by Customer', xlabel='Amount Spent', dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3.2 — GROUP BY Multiple Columns

    > *"Revenue by city and customer tier?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.city,
               c.tier,
               COUNT(*)                                AS num_orders,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS revenue
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.city, c.tier
        ORDER BY c.city, revenue DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"How many units of each product were sold?"*
    """)
    return


@app.cell
def _(con):
    df_prod = con.execute(
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
    ).fetchdf()
    df_prod
    return (df_prod,)


@app.cell
def _(df_prod, plot_hbar):
    plot_hbar(df_prod, x='revenue', y='product_name',
              title='Revenue by Product', xlabel='Revenue', dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3.3 — GROUP BY with Dates

    > *"What is the monthly revenue trend?"*

    We use `STRFTIME` to extract the month from the date:
    """)
    return


@app.cell
def _(con):
    df_monthly = con.execute(
        f"""
        SELECT STRFTIME(s.sale_date, '%Y-%m')           AS month,
               COUNT(*)                                  AS num_orders,
               ROUND(SUM(p.unit_price * s.quantity), 2)  AS revenue
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        GROUP BY month
        ORDER BY month
        """
    ).fetchdf()
    df_monthly
    return (df_monthly,)


@app.cell
def _(df_monthly, plot_bar):
    plot_bar(df_monthly, x='month', y='revenue',
             title='Monthly Revenue Trend', ylabel='Revenue', dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"What share of revenue comes from each category?"*
    """)
    return


@app.cell
def _(df_cat, plot_pie):
    plot_pie(df_cat, labels='category', values='revenue',
             title='Revenue Share by Category')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3.4 — HAVING (Filter Groups)

    `WHERE` filters **individual rows** (before grouping).
    `HAVING` filters **groups** (after grouping).

    > *"Which products generated more than $100 in total revenue?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT p.product_name,
               SUM(s.quantity)                         AS units_sold,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS revenue
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        GROUP BY p.product_name
        HAVING SUM(p.unit_price * s.quantity) > 100
        ORDER BY revenue DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"Which customers placed more than 3 orders?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.customer_name,
               COUNT(*) AS num_orders
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        GROUP BY c.customer_name
        HAVING COUNT(*) > 3
        ORDER BY num_orders DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Combining WHERE + GROUP BY + HAVING

    > *"Among Electronics orders only, which customers spent more than $500?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.customer_name,
               COUNT(*)                                AS electronics_orders,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS electronics_spent
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        WHERE  p.category = 'Electronics'
        GROUP BY c.customer_name
        HAVING SUM(p.unit_price * s.quantity) > 500
        ORDER BY electronics_spent DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### SQL Execution Order

    This is the order SQL **actually processes** your query:

    ```
    1. FROM / JOIN     → pick the tables and combine them
    2. WHERE           → filter individual rows
    3. GROUP BY        → collapse rows into groups
    4. HAVING          → filter the groups
    5. SELECT          → choose which columns to show
    6. ORDER BY        → sort the final result
    7. LIMIT           → return only the first N rows
    ```

    This explains why `WHERE` can't use `AVG(salary)` — aggregation hasn't happened yet at step 2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3.5 — Subqueries: A Query Inside a Query

    Sometimes a business question requires **two steps**:
    1. Compute a value (like an average)
    2. Use that value to filter

    A subquery lets you do both in one SQL statement.

    > *"Which orders have a total above the average order total?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- First, what IS the average order total?
        SELECT ROUND(AVG(p.unit_price * s.quantity), 2) AS avg_order_total
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Now use that as a subquery in WHERE
        SELECT s.sale_id,
               c.customer_name,
               p.product_name,
               ROUND(p.unit_price * s.quantity, 2) AS order_total
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        WHERE  p.unit_price * s.quantity > (
                   SELECT AVG(p2.unit_price * s2.quantity)
                   FROM   sales s2
                   JOIN   products p2 ON s2.product_id = p2.product_id
               )
        ORDER BY order_total DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"Which customer spent the most overall?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.customer_name,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS total_spent
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.customer_name
        ORDER BY total_spent DESC
        LIMIT 1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"Show each customer's spending alongside the company average"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.customer_name,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS customer_total,
               (SELECT ROUND(AVG(sub.total), 2)
                FROM (SELECT SUM(p2.unit_price * s2.quantity) AS total
                      FROM   sales s2
                      JOIN   products p2 ON s2.product_id = p2.product_id
                      GROUP BY s2.customer_id) sub
               ) AS avg_customer_total
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.customer_name
        ORDER BY customer_total DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > *"Which customers spend MORE than the average customer?"*
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.customer_name,
               ROUND(SUM(p.unit_price * s.quantity), 2) AS total_spent
        FROM   sales s
        JOIN   customers c ON s.customer_id = c.customer_id
        JOIN   products  p ON s.product_id  = p.product_id
        GROUP BY c.customer_name
        HAVING SUM(p.unit_price * s.quantity) > (
                   SELECT AVG(sub.total)
                   FROM (SELECT SUM(p2.unit_price * s2.quantity) AS total
                         FROM   sales s2
                         JOIN   products p2 ON s2.product_id = p2.product_id
                         GROUP BY s2.customer_id) sub
               )
        ORDER BY total_spent DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3.6 — One More Visualization

    > *"Show min and max order totals per category side by side."*
    """)
    return


@app.cell
def _(con):
    df_range = con.execute(
        f"""
        SELECT p.category,
               ROUND(MIN(p.unit_price * s.quantity), 2) AS min_order,
               ROUND(MAX(p.unit_price * s.quantity), 2) AS max_order
        FROM   sales s
        JOIN   products p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY p.category
        """
    ).fetchdf()
    df_range
    return (df_range,)


@app.cell
def _(df_range, plot_grouped_bar):
    plot_grouped_bar(df_range, x='category', y_cols=['min_order', 'max_order'],
                     title='Order Value Range by Category',
                     ylabel='Order Total', dollar=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 3 Summary

    | Concept | What It Solves |
    |---------|---------------|
    | `GROUP BY` | One row per group instead of one row per order |
    | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` | *How* to collapse each group |
    | `HAVING` | Filter the groups **after** aggregating |
    | `WHERE` vs `HAVING` | `WHERE` filters rows, `HAVING` filters groups |
    | `STRFTIME` | Turn a date into a month label for trend reporting |
    | Subquery | Use one query's answer inside another query |

    ### The Journey So Far

    ```
     orders_data.csv          →   customers + products + sales
     (flat, redundant)            (normalized, clean)
           ↓                                ↓
     Week 1: query it as-is        Week 2: design & JOIN
                                            ↓
                                   Week 3: aggregate, plot, compare
    ```

    ### Looking Ahead

    Weeks 4–6 move to a new dataset — a 30-person tech company — and to analytics
    that *keep* every row instead of collapsing it: window functions.
    """)
    return


if __name__ == "__main__":
    app.run()
