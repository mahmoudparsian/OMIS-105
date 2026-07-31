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
    # 📊 OMIS 105 Flagship Notebook Level 3  
    ## Retail Sales Database: From Raw Data to Business Insights

    This notebook is designed as a **teaching notebook** for an introductory Database Management Systems course.

    It includes:

    - One practical dataset used across the course
    - Bronze → Silver → Gold pipeline
    - Explicit business rules
    - SQL practice checkpoints
    - Instructor solution cells
    - Database design and normalization preview
    - Business insight questions

    > Dataset required: `flagship_sales_1000.csv`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Learning Objectives

    By the end of this notebook, students should be able to:

    1. Load and inspect a raw dataset
    2. Identify common real-world data quality issues
    3. Write basic SQL queries using DuckDB
    4. Clean messy columns using SQL
    5. Apply business rules step by step
    6. Create analytical tables
    7. Generate business insights
    8. Understand why normalization matters
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 0 — Setup

    We will use:

    - `pandas` to load the CSV file
    - `duckdb` to run SQL
    - `matplotlib` for a simple chart
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    # Load CSV
    df = pd.read_csv("sales_1000.csv")

    # Create DuckDB connection
    con = duckdb.connect()

    # Register pandas dataframe as a DuckDB table/view
    con.register("sales_raw", df)

    df.head()
    return (con, plt)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🟫 Part 1 — Bronze Layer: Raw Data

    The Bronze layer stores the data as originally received.

    At this stage, we do **not** fix anything yet.

    We first ask:

    - What columns do we have?
    - What data quality problems exist?
    - What questions can we answer?
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *
        FROM sales_raw
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inspect the Dataset
    """)
    return


@app.cell
def _(con):
    con.execute("""
        DESCRIBE sales_raw;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check Basic Counts
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT order_id) AS distinct_order_ids,
            COUNT(DISTINCT product) AS distinct_products,
            COUNT(DISTINCT country) AS distinct_country_values
        FROM sales_raw;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data Quality Investigation

    This dataset intentionally contains realistic issues:

    - `order_id` is not unique
    - `order_date` has mixed formats
    - `customer_name` may be missing or inconsistent
    - `price` may include `$`
    - `quantity` may contain text values such as `two`
    - `discount` may be blank
    - `country` has inconsistent casing
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT DISTINCT country
    FROM sales_raw
    ORDER BY country;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT DISTINCT quantity
    FROM sales_raw
    ORDER BY quantity;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧪 Student Checkpoint 1

    Answer these using SQL:

    1. Show the first 20 rows.
    2. Count how many rows are in the dataset.
    3. List all distinct products.
    4. List all distinct status values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Instructor Solution — Checkpoint 1
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        /* 1. First 20 rows */
        SELECT *
        FROM sales_raw
        LIMIT 20;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        /* 2. Count rows */
        SELECT COUNT(*) AS total_rows
        FROM sales_raw;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        /* 3. Distinct products */
        SELECT DISTINCT product
        FROM sales_raw
        ORDER BY product;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        /* 4. Distinct statuses */
        SELECT DISTINCT status
        FROM sales_raw
        ORDER BY status;
        """
    ).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ⚪ Part 2 — Silver Layer: Cleaned Data

    The Silver layer applies cleaning and validation rules.

    We will define each rule clearly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Business Rules

    ### Rule-1: Clean customer names
    - Convert names to uppercase
    - Remove rows where customer name is missing

    ### Rule-2: Clean prices
    - Remove `$`
    - Convert price to integer

    ### Rule-3: Clean quantities
    - Convert text quantities (`one`, `two`, etc.) into numbers

    ### Rule-4: Clean countries
    - Convert country values to uppercase
    - Standardize `US`, `USA`, and `usa` into `USA`

    ### Rule-5: Clean discounts
    - Convert blank discount to `0%`
    - Remove `%`
    - Convert to numeric percent

    ### Rule-6: Keep valid order statuses
    - Keep only `shipped`, `pending`, and `delivered`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Apply Rule-1: Clean Customer Names
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE silver_step1 AS
        SELECT
            order_id,
            order_date,
            UPPER(TRIM(customer_name)) AS customer_name,
            product,
            category,
            price,
            quantity,
            discount,
            country,
            status
        FROM sales_raw
        WHERE customer_name IS NOT NULL
        AND TRIM(customer_name) != '';
    """)

    con.execute("""
        SELECT *
        FROM silver_step1
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Apply Rule-2: Clean Prices
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE silver_step2 AS
        SELECT
            order_id,
            order_date,
            customer_name,
            product,
            category,
            CAST(REPLACE(price, '$', '') AS INTEGER) AS price,
            quantity,
            discount,
            country,
            status
        FROM silver_step1;
    """)

    con.execute("""
        SELECT
            product,
            price
        FROM silver_step2
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Apply Rule-3: Clean Quantities

    We map text quantities to numbers.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE silver_step3 AS
        SELECT
            order_id,
            order_date,
            customer_name,
            product,
            category,
            price,
            CASE WHEN LOWER(quantity) = 'one' THEN 1 WHEN LOWER(quantity) = 'two' THEN 2 WHEN LOWER(quantity) = 'three' THEN 3 WHEN LOWER(quantity) = 'four' THEN 4 WHEN LOWER(quantity) = 'five' THEN 5 ELSE CAST(quantity AS INTEGER) END AS quantity,
            discount,
            country,
            status
        FROM silver_step2;
    """)

    con.execute("""
        SELECT DISTINCT quantity
        FROM silver_step3
        ORDER BY quantity;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Apply Rule-4: Clean Countries
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE silver_step4 AS
        SELECT
            order_id,
            order_date,
            customer_name,
            product,
            category,
            price,
            quantity,
            discount,
            CASE WHEN UPPER(TRIM(country)) IN ('US', 'USA') THEN 'USA' ELSE UPPER(TRIM(country)) END AS country,
            LOWER(TRIM(status)) AS status
        FROM silver_step3;
    """)

    con.execute("""
        SELECT DISTINCT country
        FROM silver_step4
        ORDER BY country;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Apply Rule-5: Clean Discounts
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE silver_step5 AS
        SELECT
            order_id,
            order_date,
            customer_name,
            product,
            category,
            price,
            quantity,
            CASE WHEN discount IS NULL
        OR TRIM(discount) = '' THEN 0 ELSE CAST(REPLACE(discount, '%', '') AS INTEGER) END AS discount_pct, country, status
        FROM silver_step4;
    """)

    con.execute("""
        SELECT
            discount_pct,
            COUNT(*) AS rows
        FROM silver_step5
        GROUP BY discount_pct
        ORDER BY discount_pct;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Apply Rule-6: Keep Valid Statuses
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE silver_sales AS
        SELECT *
        FROM silver_step5
        WHERE status IN ('shipped', 'pending', 'delivered');
    """)

    con.execute("""
        SELECT *
        FROM silver_sales
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create Derived Business Columns

    Now that the data is clean enough, we can calculate:

    - `gross_revenue = price * quantity`
    - `discount_amount = gross_revenue * discount_pct / 100`
    - `net_revenue = gross_revenue - discount_amount`
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE silver_sales_enriched AS
        SELECT
            *,
            price * quantity AS gross_revenue,
            ROUND((price * quantity) * discount_pct / 100.0, 2) AS discount_amount,
            ROUND((price * quantity) - ((price * quantity) * discount_pct / 100.0), 2) AS net_revenue
        FROM silver_sales;
    """)

    con.execute("""
        SELECT *
        FROM silver_sales_enriched
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧪 Student Checkpoint 2

    Using `silver_sales_enriched`, write SQL to answer:

    1. Show all rows where `country = 'USA'`.
    2. Show orders with `net_revenue > 1000`.
    3. Show only `customer_name`, `product`, `quantity`, and `net_revenue`.
    4. Sort orders by `net_revenue` from highest to lowest.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Instructor Solution — Checkpoint 2
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT *
        FROM silver_sales_enriched
        WHERE country = 'USA';
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT *
        FROM silver_sales_enriched
        WHERE net_revenue > 1000;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT
            customer_name,
            product,
            quantity,
            net_revenue
        FROM silver_sales_enriched;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT *
        FROM silver_sales_enriched
        ORDER BY net_revenue DESC;
        """
    ).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🟡 Part 3 — Gold Layer: Analytical Tables

    The Gold layer is designed for business questions.

    Now we create summary tables.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gold Table 1: Revenue by Product
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE gold_revenue_by_product AS
        SELECT
            product,
            category,
            COUNT(*) AS order_lines,
            SUM(quantity) AS units_sold,
            ROUND(SUM(net_revenue), 2) AS total_net_revenue
        FROM silver_sales_enriched
        GROUP BY product, category
        ORDER BY total_net_revenue DESC;
    """)

    con.execute("""
        SELECT *
        FROM gold_revenue_by_product;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gold Table 2: Revenue by Country
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE gold_revenue_by_country AS
        SELECT
            country,
            COUNT(*) AS order_lines,
            ROUND(SUM(net_revenue), 2) AS total_net_revenue
        FROM silver_sales_enriched
        GROUP BY country
        ORDER BY total_net_revenue DESC;
    """)

    con.execute("""
        SELECT *
        FROM gold_revenue_by_country;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gold Table 3: Top Customers
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE gold_top_customers AS
        SELECT
            customer_name,
            COUNT(*) AS order_lines,
            ROUND(SUM(net_revenue), 2) AS total_net_revenue
        FROM silver_sales_enriched
        GROUP BY customer_name
        ORDER BY total_net_revenue DESC;
    """)

    con.execute("""
        SELECT *
        FROM gold_top_customers
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Visualization: Revenue by Product
    """)
    return


@app.cell
def _(con, plt):
    df_product = con.execute("""
        SELECT *
        FROM gold_revenue_by_product;
    """).df()

    plt.figure(figsize=(10, 5))
    plt.bar(df_product["product"], df_product["total_net_revenue"])
    plt.title("Total Net Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Total Net Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧪 Student Checkpoint 3

    Using the Gold tables:

    1. Which product generated the highest net revenue?
    2. Which country generated the highest net revenue?
    3. Which customer generated the highest net revenue?
    4. Which product sold the most units?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Instructor Solution — Checkpoint 3
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT *
        FROM gold_revenue_by_product
        ORDER BY total_net_revenue DESC
        LIMIT 1;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT *
        FROM gold_revenue_by_country
        ORDER BY total_net_revenue DESC
        LIMIT 1;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT *
        FROM gold_top_customers
        ORDER BY total_net_revenue DESC
        LIMIT 1;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT *
        FROM gold_revenue_by_product
        ORDER BY units_sold DESC
        LIMIT 1;
        """
    ).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧱 Part 4 — Normalization Preview

    The raw table is useful for early learning, but it has design problems:

    - Customer names are repeated
    - Product information is repeated
    - Orders and products are mixed together

    A better design separates data into multiple tables.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create Dimension Tables

    We create:

    - `dim_customer`
    - `dim_product`
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE dim_customer AS
        SELECT ROW_NUMBER() OVER (
        ORDER BY customer_name) AS customer_id, customer_name
        FROM (
        SELECT DISTINCT customer_name
        FROM silver_sales_enriched );
    """)

    con.execute("""
        SELECT *
        FROM dim_customer
        LIMIT 10;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE dim_product AS
        SELECT ROW_NUMBER() OVER (
        ORDER BY product) AS product_id, product, category
        FROM (
        SELECT DISTINCT
            product,
            category
        FROM silver_sales_enriched );
    """)

    con.execute("""
        SELECT *
        FROM dim_product
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create Fact Table

    The fact table stores measurable events:

    - order line
    - quantity
    - revenue
    - links to customer and product
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE
        OR REPLACE TABLE fact_order_line AS
        SELECT
            s.order_id,
            c.customer_id,
            p.product_id,
            s.order_date,
            s.quantity,
            s.price,
            s.discount_pct,
            s.net_revenue,
            s.country,
            s.status
        FROM silver_sales_enriched s
        JOIN dim_customer c ON s.customer_name = c.customer_name
        JOIN dim_product p ON s.product = p.product
        AND s.category = p.category;
    """)

    con.execute("""
        SELECT *
        FROM fact_order_line
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Query the Normalized Model

    Now we use JOINs to answer business questions.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            p.product,
            p.category,
            ROUND(SUM(f.net_revenue), 2) AS total_net_revenue
        FROM fact_order_line f
        JOIN dim_product p ON f.product_id = p.product_id
        GROUP BY p.product, p.category
        ORDER BY total_net_revenue DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧪 Student Checkpoint 4

    Using the normalized tables:

    1. Join `fact_order_line` with `dim_customer`.
    2. Join `fact_order_line` with `dim_product`.
    3. Find revenue by product using the normalized model.
    4. Find revenue by customer using the normalized model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Instructor Solution — Checkpoint 4
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT
            f.order_id,
            c.customer_name,
            f.net_revenue
        FROM fact_order_line f
        JOIN dim_customer c ON f.customer_id = c.customer_id
        LIMIT 10;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT
            f.order_id,
            p.product,
            p.category,
            f.net_revenue
        FROM fact_order_line f
        JOIN dim_product p ON f.product_id = p.product_id
        LIMIT 10;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT
            p.product,
            ROUND(SUM(f.net_revenue), 2) AS total_net_revenue
        FROM fact_order_line f
        JOIN dim_product p ON f.product_id = p.product_id
        GROUP BY p.product
        ORDER BY total_net_revenue DESC;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT
            c.customer_name,
            ROUND(SUM(f.net_revenue), 2) AS total_net_revenue
        FROM fact_order_line f
        JOIN dim_customer c ON f.customer_id = c.customer_id
        GROUP BY c.customer_name
        ORDER BY total_net_revenue DESC;
        """
    ).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ⚙️ Part 5 — Performance Preview

    Indexes help databases find rows faster.

    For small teaching datasets, speed differences may not be obvious.  
    But the idea is important.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_fact_customer ON fact_order_line(customer_id); CREATE INDEX IF NOT EXISTS idx_fact_product ON fact_order_line(product_id);
        """
    ).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🔐 Part 6 — Transactions Preview

    Transactions protect correctness.

    Example idea:

    - Insert an order
    - Insert order line
    - Commit only when all steps succeed
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        BEGIN TRANSACTION; /* Example safe operation */ /* In a real system, we would insert into orders and order lines together. */
        COMMIT;
        """
    ).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧠 Final Business Insight Questions

    Use SQL to answer:

    1. Which product category performs best?
    2. Which country produces the most revenue?
    3. Which customer is most valuable?
    4. Which order status has the most revenue?
    5. Which products may need more marketing attention?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Instructor Solution — Final Insight Examples
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT
            category,
            ROUND(SUM(total_net_revenue), 2) AS revenue
        FROM gold_revenue_by_product
        GROUP BY category
        ORDER BY revenue DESC;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT *
        FROM gold_revenue_by_country
        ORDER BY total_net_revenue DESC;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT *
        FROM gold_top_customers
        ORDER BY total_net_revenue DESC
        LIMIT 5;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT
            status,
            ROUND(SUM(net_revenue), 2) AS revenue
        FROM silver_sales_enriched
        GROUP BY status
        ORDER BY revenue DESC;
        """
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT *
        FROM gold_revenue_by_product
        ORDER BY total_net_revenue ASC
        LIMIT 5;
        """
    ).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✅ Notebook Summary

    In this notebook, you practiced:

    - Raw data exploration
    - SQL basics
    - Data cleaning
    - Business rules
    - Aggregation
    - Visualization
    - Normalization
    - JOINs
    - Performance preview
    - Transaction preview

    This notebook connects the full OMIS 105 course into one coherent learning experience.
    """)
    return


if __name__ == "__main__":
    app.run()
