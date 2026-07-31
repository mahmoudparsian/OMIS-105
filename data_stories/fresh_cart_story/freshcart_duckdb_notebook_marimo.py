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
    # 🛒 FreshCart Analytics — DuckDB Notebook
    ---
    **Business Context:** 

            FreshCart is a mid-sized omnichannel 
            grocer operating in the USA, Canada, 
            India, and Germany. 

    **Notebook:**

            This notebook explores customer behavior, 
            product performance, and revenue trends 
            using **DuckDB** as our analytical engine.

    **KPIs:** 

    * Revenue, 
    * Average Order Value (AOV), 
    * Units Per Order (UPO), 
    * Customer Lifetime Value (LTV)

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⚙️ Setup: Import Libraries and Helper Functions
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import sys, os

    # Add notebook directory to path so we can import helpers
    sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')) if os.path.dirname(os.path.abspath('__file__')) else '.')

    from freshcart_helpers import show, plot_bar, plot_line, plot_pie, plot_hbar, plot_grouped_bar, plot_scatter

    # Create an in-memory DuckDB connection
    con = duckdb.connect(database=':memory:')
    print("✓ DuckDB connected | Helper functions loaded")
    return (con, plot_bar, plot_grouped_bar, plot_hbar, plot_line, plot_pie, plot_scatter, show)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📐 Schema Creation

    Create the three core tables: 

    * **customers**, 
    * **products**, 
    * **orders**. 

    Each order is a single line-item capturing product, quantity, price, and channel.
    """)
    return


@app.cell
def _(con):
    # ─── Create Tables ─────────────────────────────────────────────────────────
    con.execute("""
        CREATE TABLE customers ( customer_id INTEGER PRIMARY KEY, full_name VARCHAR(80) NOT NULL, email VARCHAR(120) NOT NULL, country VARCHAR(30) NOT NULL, join_date DATE NOT NULL, loyalty_tier VARCHAR(10) DEFAULT 'NONE' );
        CREATE TABLE products ( product_id INTEGER PRIMARY KEY, product_name VARCHAR(80) NOT NULL, category VARCHAR(40) NOT NULL, base_price DECIMAL(8,2) NOT NULL );
        CREATE TABLE orders (
            order_id    INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
            product_id  INTEGER NOT NULL REFERENCES products(product_id),
            order_date  DATE NOT NULL,
            channel     VARCHAR(10) NOT NULL,
            quantity    INTEGER NOT NULL,
            price_each  DECIMAL(8,2) NOT NULL
        );
    """)
    print("✓ Tables created: customers, products, orders")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📥 Load Sample Data
    We populate the tables with realistic data: **25 customers**, **15 products**, and **60 orders** across 2024–2025.
    """)
    return


@app.cell
def _(con):
    # ─── Insert Customers (25 rows) ────────────────────────────────────────────
    con.execute("""
        INSERT INTO customers
        VALUES
            (1, 'Emma Smith', 'emma.smith1@example.com', 'INDIA', '2024-09-07', 'NONE'),
            (2, 'Emma Weber', 'emma.weber2@example.com', 'USA', '2025-03-08', 'NONE'),
            (3, 'Liam Davis', 'liam.davis3@example.com', 'CANADA', '2025-06-01', 'SILVER'),
            (4, 'Raj Davis', 'raj.davis4@example.com', 'GERMANY', '2024-08-13', 'NONE'),
            (5, 'Isabella Smith', 'isabella.smith5@example.com', 'CANADA', '2025-03-08', 'NONE'),
            (6, 'Olivia Davis', 'olivia.davis6@example.com', 'INDIA', '2024-04-14', 'NONE'),
            (7, 'Emma Sharma', 'emma.sharma7@example.com', 'INDIA', '2024-09-27', 'GOLD'),
            (8, 'Lea Weber', 'lea.weber8@example.com', 'USA', '2025-01-22', 'NONE'),
            (9, 'Lucas Becker', 'lucas.becker9@example.com', 'INDIA', '2024-07-15', 'SILVER'),
            (10, 'Noah Wilson', 'noah.wilson10@example.com', 'INDIA', '2024-03-22', 'GOLD'),
            (11, 'Emma Patel', 'emma.patel11@example.com', 'INDIA', '2025-04-09', 'SILVER'),
            (12, 'Arjun Miller', 'arjun.miller12@example.com', 'INDIA', '2024-12-29', 'NONE'),
            (13, 'Sophie Martin', 'sophie.martin13@example.com', 'CANADA', '2024-05-18', 'GOLD'),
            (14, 'James Brown', 'james.brown14@example.com', 'USA', '2024-01-10', 'PLATINUM'),
            (15, 'Priya Gupta', 'priya.gupta15@example.com', 'INDIA', '2024-11-03', 'SILVER'),
            (16, 'Hans Mueller', 'hans.mueller16@example.com', 'GERMANY', '2024-06-22', 'NONE'),
            (17, 'Maria Garcia', 'maria.garcia17@example.com', 'USA', '2025-02-14', 'GOLD'),
            (18, 'Akira Tanaka', 'akira.tanaka18@example.com', 'INDIA', '2024-10-30', 'NONE'),
            (19, 'Charlotte Lee', 'charlotte.lee19@example.com', 'CANADA', '2025-01-05', 'SILVER'),
            (20, 'Felix Schmidt', 'felix.schmidt20@example.com', 'GERMANY', '2024-09-12', 'NONE'),
            (21, 'Ananya Reddy', 'ananya.reddy21@example.com', 'INDIA', '2025-05-20', 'GOLD'),
            (22, 'Oliver Chen', 'oliver.chen22@example.com', 'USA', '2024-04-03', 'PLATINUM'),
            (23, 'Sara Khan', 'sara.khan23@example.com', 'INDIA', '2025-07-11', 'NONE'),
            (24, 'Thomas Dubois', 'thomas.dubois24@example.com', 'CANADA', '2024-08-25', 'SILVER'),
            (25, 'Meera Joshi', 'meera.joshi25@example.com', 'INDIA', '2025-06-15', 'GOLD');
    """)
    print("✓ 25 customers inserted")
    return


@app.cell
def _(con):
    # ─── Insert Products (15 rows) ─────────────────────────────────────────────
    con.execute("""
        INSERT INTO products
        VALUES
            (1, 'Whole Milk 1L', 'Dairy', 3.49),
            (2, 'Free-Range Eggs (12)', 'Dairy', 4.99),
            (3, 'Sourdough Bread', 'Bakery', 3.99),
            (4, 'Almond Butter 340g', 'Pantry', 8.99),
            (5, 'Organic Bananas (1kg)', 'Produce', 1.99),
            (6, 'Greek Yogurt 500g', 'Dairy', 5.49),
            (7, 'Cold Brew Coffee 1L', 'Beverages', 6.49),
            (8, 'Sparkling Water 1L', 'Beverages', 1.29),
            (9, 'Trail Mix 300g', 'Snacks', 4.49),
            (10, 'Dark Chocolate 85% 100g', 'Snacks', 2.99),
            (11, 'Avocado (each)', 'Produce', 2.49),
            (12, 'Chicken Breast 500g', 'Meat', 7.99),
            (13, 'Pasta Penne 500g', 'Pantry', 2.29),
            (14, 'Orange Juice 1L', 'Beverages', 3.79),
            (15, 'Granola Bar (6-pack)', 'Snacks', 3.99);
    """)
    print("✓ 15 products inserted")
    return


@app.cell
def _(con):
    # ─── Insert Orders (60 rows) ───────────────────────────────────────────────
    con.execute("""
        INSERT INTO orders
        VALUES
            (1, 5, 2, '2025-06-30', 'online', 2, 5.12),
            (2, 3, 8, '2025-10-17', 'online', 2, 1.23),
            (3, 11, 6, '2024-02-02', 'store', 1, 5.19),
            (4, 7, 5, '2025-08-03', 'store', 1, 1.87),
            (5, 4, 8, '2025-10-20', 'store', 2, 1.39),
            (6, 3, 5, '2025-07-28', 'store', 1, 1.89),
            (7, 12, 10, '2025-02-12', 'store', 2, 3.23),
            (8, 4, 3, '2024-02-18', 'online', 2, 3.98),
            (9, 3, 3, '2024-03-06', 'store', 3, 3.93),
            (10, 7, 10, '2025-07-20', 'online', 2, 3.01),
            (11, 11, 2, '2024-09-30', 'store', 3, 5.37),
            (12, 2, 5, '2024-01-04', 'store', 2, 1.85),
            (13, 9, 3, '2025-10-02', 'store', 2, 4.32),
            (14, 11, 9, '2025-01-17', 'online', 2, 4.22),
            (15, 9, 9, '2025-05-15', 'online', 1, 4.58),
            (16, 2, 6, '2024-09-03', 'online', 1, 5.20),
            (17, 2, 8, '2025-06-29', 'online', 1, 1.41),
            (18, 3, 8, '2025-06-24', 'store', 2, 1.20),
            (19, 4, 9, '2025-12-31', 'store', 3, 4.66),
            (20, 7, 6, '2025-04-07', 'online', 2, 5.93),
            (21, 4, 4, '2025-08-25', 'online', 1, 8.70),
            (22, 10, 4, '2025-10-08', 'online', 1, 8.22),
            (23, 4, 2, '2024-03-13', 'online', 1, 5.35),
            (24, 5, 8, '2025-08-07', 'store', 1, 1.30),
            (25, 4, 8, '2024-04-09', 'store', 2, 1.21),
            (26, 13, 7, '2024-07-15', 'online', 2, 6.39),
            (27, 14, 1, '2024-03-20', 'store', 4, 3.49),
            (28, 14, 12, '2024-06-11', 'online', 2, 7.89),
            (29, 15, 6, '2025-01-28', 'store', 1, 5.35),
            (30, 16, 3, '2025-03-14', 'online', 1, 4.10),
            (31, 17, 11, '2025-04-22', 'store', 3, 2.49),
            (32, 17, 7, '2025-05-10', 'online', 1, 6.49),
            (33, 18, 12, '2025-02-08', 'store', 1, 7.75),
            (34, 19, 14, '2025-03-19', 'online', 2, 3.65),
            (35, 19, 1, '2025-06-02', 'store', 2, 3.39),
            (36, 20, 13, '2024-11-28', 'online', 3, 2.29),
            (37, 20, 10, '2025-01-05', 'store', 2, 2.99),
            (38, 21, 5, '2025-07-14', 'online', 4, 1.89),
            (39, 21, 11, '2025-08-20', 'store', 2, 2.39),
            (40, 22, 4, '2024-05-30', 'online', 1, 8.99),
            (41, 22, 12, '2024-08-18', 'store', 2, 7.99),
            (42, 22, 7, '2025-01-12', 'online', 1, 6.35),
            (43, 23, 15, '2025-09-05', 'store', 2, 3.85),
            (44, 23, 5, '2025-09-22', 'online', 3, 1.95),
            (45, 24, 1, '2024-10-10', 'store', 2, 3.45),
            (46, 24, 9, '2025-02-28', 'online', 1, 4.49),
            (47, 25, 6, '2025-08-30', 'store', 2, 5.29),
            (48, 25, 14, '2025-09-15', 'online', 1, 3.69),
            (49, 13, 11, '2024-09-04', 'store', 2, 2.45),
            (50, 14, 15, '2024-11-20', 'online', 3, 3.99),
            (51, 10, 7, '2025-06-18', 'online', 1, 6.29),
            (52, 6, 1, '2024-06-30', 'store', 2, 3.49),
            (53, 6, 3, '2024-08-12', 'online', 1, 4.15),
            (54, 1, 2, '2025-03-25', 'store', 2, 4.99),
            (55, 1, 9, '2025-05-08', 'online', 1, 4.35),
            (56, 8, 13, '2025-04-17', 'store', 2, 2.19),
            (57, 8, 7, '2025-07-03', 'online', 1, 6.45),
            (58, 15, 12, '2025-06-22', 'online', 1, 7.85),
            (59, 16, 11, '2025-08-09', 'store', 2, 2.55),
            (60, 18, 15, '2025-10-11', 'online', 2, 3.89);
    """)
    print("✓ 60 orders inserted")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📋 Section 1 — Basic Queries
    Simple SELECT statements, filtering, sorting, and aliasing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q1. List All Customers
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM customers
        ORDER BY customer_id;
    """).fetchdf()

    show(_df, "All Customers")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q2. List All Products
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM products
        ORDER BY product_id;
    """).fetchdf()

    show(_df, "All Products")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q3. First 10 Orders (by order_id)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM orders
        ORDER BY order_id
        LIMIT 10;
    """).fetchdf()

    show(_df, "First 10 Orders")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q4. Customer Names and Countries
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
    SELECT full_name,
           country
    FROM   customers
    ORDER BY country, full_name
    ;""").fetchdf()

    show(_df, "Customers by Country")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q5. Products and Their Categories
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
    SELECT product_name,
           category
    FROM   products
    ORDER BY category, product_name
    ;""").fetchdf()

    show(_df, "Products by Category")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q6. Customers in USA
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM customers
        WHERE country = 'USA'
        ORDER BY full_name;
    """).fetchdf()

    show(_df, "USA Customers")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q7. Products in the Snacks Category
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM products
        WHERE category = 'Snacks'
        ORDER BY product_name;
    """).fetchdf()

    show(_df, "Snacks Products")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q8. Orders Placed in 2025
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM orders
        WHERE YEAR(order_date) = 2025
        ORDER BY order_date;
    """).fetchdf()

    show(_df, "2025 Orders")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q9. Products Sorted by Price (Descending)
    """)
    return


@app.cell
def _(con, plot_hbar, show):
    _df = con.execute("""
        SELECT *
        FROM products
        ORDER BY base_price DESC;
    """).fetchdf()

    show(_df, "Products by Price (High → Low)")
    plot_hbar(_df, 'product_name', 'base_price', title="Products Ranked by Base Price ($)", xlabel="Base Price ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q10. Distinct Countries
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
    SELECT DISTINCT country
    FROM   customers
    ORDER BY country
    ;""").fetchdf()

    show(_df, "Countries We Operate In")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q11. Customers Who Joined in 2024
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM customers
        WHERE YEAR(join_date) = 2024
        ORDER BY join_date;
    """).fetchdf()

    show(_df, "Customers Joining in 2024")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q12. Online Channel Orders
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM orders
        WHERE channel = 'online'
        ORDER BY order_date;
    """).fetchdf()

    show(_df, "Online Orders")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q13. Top 10 Most Recent Orders
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM orders
        ORDER BY order_date DESC
        LIMIT 10;
    """).fetchdf()

    show(_df, "10 Most Recent Orders")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q14. Products Priced Below $3.00
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM products
        WHERE base_price < 3.00
        ORDER BY base_price;
    """).fetchdf()

    show(_df, "Budget Products (< $3)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q15. Orders with Quantity > 1
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM orders
        WHERE quantity > 1
        ORDER BY quantity DESC, order_date;
    """).fetchdf()

    show(_df, "Multi-Unit Orders")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q16. Customer Emails (with Alias)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
    SELECT full_name,
           email AS contact_email
    FROM   customers
    ORDER BY full_name
    ;""").fetchdf()

    show(_df, "Customer Contact List")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q17. Product Count Per Category
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT
            category,
            COUNT(*) AS product_count
        FROM products
        GROUP BY category
        ORDER BY product_count DESC;
    """).fetchdf()

    show(_df, "Products Per Category")
    plot_bar(_df, 'category', 'product_count', title="Number of Products Per Category", ylabel="Count")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q18. Orders Sorted by Customer then Date
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM orders
        ORDER BY customer_id, order_date;
    """).fetchdf()

    show(_df, "Orders by Customer → Date")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q19. Customers with GOLD or PLATINUM Loyalty
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM customers
        WHERE loyalty_tier IN ('GOLD', 'PLATINUM')
        ORDER BY loyalty_tier DESC, full_name;
    """).fetchdf()

    show(_df, "Premium Loyalty Customers")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q20. Orders Between $5 and $10 (price_each)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM orders
        WHERE price_each BETWEEN 5.00
        AND 10.00
        ORDER BY price_each DESC;
    """).fetchdf()

    show(_df, "Mid-to-High Price Orders")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Section 2 — Basic-to-Intermediate Queries
    JOINs, aggregations, GROUP BY, HAVING, and computed columns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q21. Join Orders to Product Names
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
    SELECT o.order_id,
           o.order_date,
           p.product_name,
           o.quantity,
           o.price_each
    FROM   orders   o
    JOIN   products p ON p.product_id = o.product_id
    ORDER BY o.order_id
    ;""").fetchdf()

    show(_df, "Orders with Product Names")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q22. Full Order Details (Customer + Product)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
    SELECT o.order_id,
           c.full_name   AS customer,
           p.product_name,
           p.category,
           o.quantity,
           o.price_each,
           o.channel,
           o.order_date
    FROM   orders    o
    JOIN   customers c ON c.customer_id = o.customer_id
    JOIN   products  p ON p.product_id  = o.product_id
    ORDER BY o.order_date DESC
    ;""").fetchdf()

    show(_df, "Complete Order Details")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q23. Revenue Per Order (quantity × price_each)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            order_id,
            quantity,
            price_each,
            ROUND(quantity * price_each, 2) AS revenue
        FROM orders
        ORDER BY revenue DESC;
    """).fetchdf()

    show(_df, "Revenue Per Order")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q24. Total Revenue Overall
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT ROUND(SUM(quantity * price_each), 2) AS total_revenue
        FROM orders;
    """).fetchdf()

    show(_df, "Total Revenue")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q25. Average Order Value (AOV) and Units Per Order (UPO)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            ROUND(AVG(quantity * price_each), 2) AS avg_order_value,
            ROUND(AVG(quantity), 2) AS avg_units_per_order
        FROM orders;
    """).fetchdf()

    show(_df, "AOV & UPO")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q26. Revenue by Channel
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT
            channel,
            ROUND(SUM(quantity * price_each), 2) AS revenue,
            COUNT(*) AS order_count
        FROM orders
        GROUP BY channel
        ORDER BY revenue DESC;
    """).fetchdf()

    show(_df, "Revenue by Channel")
    plot_bar(_df, 'channel', 'revenue', title="Revenue by Sales Channel", ylabel="Revenue ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q27. Revenue by Country
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT
            c.country,
            ROUND(SUM(o.quantity * o.price_each), 2) AS revenue,
            COUNT(*) AS order_count
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.country
        ORDER BY revenue DESC;
    """).fetchdf()

    show(_df, "Revenue by Country")
    plot_bar(_df, 'country', 'revenue', title="Revenue by Country", ylabel="Revenue ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q28. Revenue by Product Category
    """)
    return


@app.cell
def _(con, plot_pie, show):
    _df = con.execute("""
        SELECT
            p.category,
            ROUND(SUM(o.quantity * o.price_each), 2) AS revenue,
            SUM(o.quantity) AS total_units
        FROM orders o
        JOIN products p ON p.product_id = o.product_id
        GROUP BY p.category
        ORDER BY revenue DESC;
    """).fetchdf()

    show(_df, "Revenue by Category")
    plot_pie(_df, 'category', 'revenue', title="Revenue Share by Product Category")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q29. Top 5 Products by Revenue
    """)
    return


@app.cell
def _(con, plot_hbar, show):
    _df = con.execute("""
        SELECT
            p.product_name,
            ROUND(SUM(o.quantity * o.price_each), 2) AS revenue
        FROM orders o
        JOIN products p ON p.product_id = o.product_id
        GROUP BY p.product_name
        ORDER BY revenue DESC
        LIMIT 5;
    """).fetchdf()

    show(_df, "Top 5 Products by Revenue")
    plot_hbar(_df, 'product_name', 'revenue', title="Top 5 Revenue-Generating Products", xlabel="Revenue ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q30. Monthly Revenue (YYYY-MM)
    """)
    return


@app.cell
def _(con, plot_line, show):
    _df = con.execute("""
        SELECT
            STRFTIME(order_date, '%Y-%m') AS year_month,
            ROUND(SUM(quantity * price_each), 2) AS revenue
        FROM orders
        GROUP BY year_month
        ORDER BY year_month;
    """).fetchdf()

    show(_df, "Monthly Revenue")
    plot_line(_df, 'year_month', 'revenue', title="Monthly Revenue Trend", xlabel="Month", ylabel="Revenue ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q31. Customer Order Counts
    """)
    return


@app.cell
def _(con, plot_hbar, show):
    _df = con.execute("""
        SELECT
            c.customer_id,
            c.full_name,
            COUNT(*) AS order_count
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.full_name
        ORDER BY order_count DESC;
    """).fetchdf()

    show(_df, "Orders Per Customer")
    plot_hbar(_df.head(10), 'full_name', 'order_count', title="Top 10 Customers by Order Count", xlabel="Orders")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q32. Customers with More Than 3 Orders
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            c.customer_id,
            c.full_name,
            COUNT(*) AS order_count
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.full_name
        HAVING COUNT(*) > 3
        ORDER BY order_count DESC;
    """).fetchdf()

    show(_df, "Frequent Shoppers (> 3 orders)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q33. Average Price Paid vs Base Price Per Product
    """)
    return


@app.cell
def _(con, plot_grouped_bar, show):
    _df = con.execute("""
        SELECT
            p.product_id,
            p.product_name,
            p.base_price,
            ROUND(AVG(o.price_each), 2) AS avg_paid
        FROM products p
        LEFT
        JOIN orders o ON o.product_id = p.product_id
        GROUP BY p.product_id, p.product_name, p.base_price
        ORDER BY p.product_id;
    """).fetchdf()

    show(_df, "Base Price vs Average Price Paid")
    plot_grouped_bar(_df, 'product_name', ['base_price', 'avg_paid'],
                     title="Base Price vs Avg Paid Per Product", ylabel="Price ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q34. Orders Per Loyalty Tier
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT
            c.loyalty_tier,
            COUNT(*) AS order_count,
            ROUND(SUM(o.quantity * o.price_each), 2) AS revenue
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.loyalty_tier
        ORDER BY revenue DESC;
    """).fetchdf()

    show(_df, "Performance by Loyalty Tier")
    plot_bar(_df, 'loyalty_tier', 'revenue', title="Revenue by Loyalty Tier", ylabel="Revenue ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q35. Average Order Value Per Country
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT
            c.country,
            ROUND(AVG(o.quantity * o.price_each), 2) AS avg_order_value
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.country
        ORDER BY avg_order_value DESC;
    """).fetchdf()

    show(_df, "AOV by Country")
    plot_bar(_df, 'country', 'avg_order_value', title="Average Order Value by Country", ylabel="AOV ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q36. Customers Who Never Ordered
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT c.*
        FROM customers c
        LEFT
        JOIN orders o ON o.customer_id = c.customer_id
        WHERE o.order_id IS NULL;
    """).fetchdf()

    show(_df, "Customers with Zero Orders")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q37. Products Never Purchased
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT p.*
        FROM products p
        LEFT
        JOIN orders o ON o.product_id = p.product_id
        WHERE o.order_id IS NULL;
    """).fetchdf()

    show(_df, "Products Never Purchased")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q38. Top 5 Customers by Total Revenue
    """)
    return


@app.cell
def _(con, plot_hbar, show):
    _df = con.execute("""
        SELECT
            c.customer_id,
            c.full_name,
            c.country,
            ROUND(SUM(o.quantity * o.price_each), 2) AS total_revenue
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.full_name, c.country
        ORDER BY total_revenue DESC
        LIMIT 5;
    """).fetchdf()

    show(_df, "Top 5 Customers by Revenue")
    plot_hbar(_df, 'full_name', 'total_revenue', title="Top 5 Customers — Lifetime Revenue", xlabel="Revenue ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q39. Revenue by Day of Week
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT
            DAYNAME(order_date) AS day_of_week,
            ROUND(SUM(quantity * price_each), 2) AS revenue,
            COUNT(*) AS orders
        FROM orders
        GROUP BY day_of_week, DAYOFWEEK(order_date)
        ORDER BY DAYOFWEEK(order_date);
    """).fetchdf()

    show(_df, "Revenue by Day of Week")
    plot_bar(_df, 'day_of_week', 'revenue', title="Revenue by Day of Week", ylabel="Revenue ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q40. Quarter-over-Quarter Order Counts
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT
            YEAR(order_date) AS yr,
            QUARTER(order_date) AS qtr,
            COUNT(*) AS order_count,
            ROUND(SUM(quantity * price_each), 2) AS revenue
        FROM orders
        GROUP BY yr, qtr
        ORDER BY yr, qtr;
    """).fetchdf()

    _df['period'] = _df['yr'].astype(str) + '-Q' + _df['qtr'].astype(str)
    show(_df, "Quarterly Performance")
    plot_bar(_df, 'period', 'revenue', title="Quarterly Revenue", ylabel="Revenue ($)", rotate_x=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🔬 Section 3 — Intermediate Queries
    CTEs, window functions, ranking, running totals, growth rates, and percentiles.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q41. Rank Customers by Revenue (RANK window function)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        WITH cust_rev AS (
        SELECT
            c.customer_id,
            c.full_name,
            c.country,
            ROUND(SUM(o.quantity * o.price_each), 2) AS revenue
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.full_name, c.country )
        SELECT
            *,
            RANK() OVER (
        ORDER BY revenue DESC) AS revenue_rank
        FROM cust_rev
        ORDER BY revenue_rank;
    """).fetchdf()

    show(_df, "Customer Revenue Rankings")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q42. Top Product by Revenue Within Each Category
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        WITH prod_rev AS (
        SELECT
            p.category,
            p.product_name,
            ROUND(SUM(o.quantity * o.price_each), 2) AS revenue
        FROM orders o
        JOIN products p ON p.product_id = o.product_id
        GROUP BY p.category, p.product_name ), ranked AS (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY category
        ORDER BY revenue DESC) AS rn
        FROM prod_rev )
        SELECT
            category,
            product_name,
            revenue
        FROM ranked
        WHERE rn <= 2
        ORDER BY category, rn;
    """).fetchdf()

    show(_df, "Top 2 Products Per Category (by Revenue)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q43. Running Monthly Revenue (Cumulative)
    """)
    return


@app.cell
def _(con, plot_line, show):
    _df = con.execute("""
        SELECT
            STRFTIME(order_date, '%Y-%m') AS year_month,
            ROUND(SUM(quantity * price_each), 2) AS monthly_rev,
            ROUND(SUM(SUM(quantity * price_each)) OVER (
        ORDER BY STRFTIME(order_date, '%Y-%m')), 2) AS cumulative_rev
        FROM orders
        GROUP BY year_month
        ORDER BY year_month;
    """).fetchdf()

    show(_df, "Cumulative Revenue Over Time")
    plot_line(_df, 'year_month', 'cumulative_rev', title="Cumulative Revenue Growth", xlabel="Month", ylabel="Cumulative Revenue ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q44. Most Recent Order Per Customer (ROW_NUMBER)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        WITH ranked_orders AS (
        SELECT
            o.*,
            c.full_name,
            ROW_NUMBER() OVER (PARTITION BY o.customer_id
        ORDER BY o.order_date DESC, o.order_id DESC) AS rn
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id )
        SELECT
            customer_id,
            full_name,
            order_id,
            order_date,
            product_id,
            channel
        FROM ranked_orders
        WHERE rn = 1
        ORDER BY order_date DESC;
    """).fetchdf()

    show(_df, "Each Customer's Most Recent Order")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q45. Customers Whose AOV Exceeds Global Average
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        WITH per_customer AS (
        SELECT
            c.customer_id,
            c.full_name,
            ROUND(AVG(o.quantity * o.price_each), 2) AS customer_aov
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.full_name ), overall AS (
        SELECT ROUND(AVG(quantity * price_each), 2) AS global_aov
        FROM orders )
        SELECT
            p.customer_id,
            p.full_name,
            p.customer_aov,
            o.global_aov
        FROM per_customer p
        CROSS
        JOIN overall o
        WHERE p.customer_aov > o.global_aov
        ORDER BY p.customer_aov DESC;
    """).fetchdf()

    show(_df, "Above-Average AOV Customers")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q46. Month-over-Month Revenue Growth (%)
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        WITH monthly AS (
        SELECT
            STRFTIME(order_date, '%Y-%m') AS year_month,
            ROUND(SUM(quantity * price_each), 2) AS revenue
        FROM orders
        GROUP BY year_month ), with_lag AS (
        SELECT
            year_month,
            revenue,
            LAG(revenue) OVER (
        ORDER BY year_month) AS prev_revenue
        FROM monthly )
        SELECT
            year_month,
            revenue,
            prev_revenue,
            CASE WHEN prev_revenue > 0 THEN ROUND(100.0 * (revenue - prev_revenue) / prev_revenue, 1) ELSE NULL END AS mom_growth_pct
        FROM with_lag
        ORDER BY year_month;
    """).fetchdf()

    show(_df, "Month-over-Month Revenue Growth")
    df_plot = _df.dropna(subset=['mom_growth_pct'])
    plot_bar(df_plot, 'year_month', 'mom_growth_pct', title="MoM Revenue Growth (%)", ylabel="Growth %", rotate_x=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q47. Country Share of Total Revenue
    """)
    return


@app.cell
def _(con, plot_pie, show):
    _df = con.execute("""
        WITH country_rev AS (
        SELECT
            c.country,
            ROUND(SUM(o.quantity * o.price_each), 2) AS revenue
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.country ), total AS (
        SELECT SUM(revenue) AS total_rev
        FROM country_rev )
        SELECT
            cr.country,
            cr.revenue,
            ROUND(100.0 * cr.revenue / t.total_rev, 1) AS pct_share
        FROM country_rev cr
        CROSS
        JOIN total t
        ORDER BY pct_share DESC;
    """).fetchdf()

    show(_df, "Country Revenue Share")
    plot_pie(_df, 'country', 'revenue', title="Revenue Share by Country")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q48. Customers Who Shopped in Both Channels
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            c.customer_id,
            c.full_name,
            COUNT(DISTINCT o.channel) AS channels_used
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.full_name
        HAVING COUNT(DISTINCT o.channel) = 2
        ORDER BY c.full_name;
    """).fetchdf()

    show(_df, "Omnichannel Customers (Both Online & Store)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q49. Products Whose Average Paid Price Exceeds Base Price
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            p.product_id,
            p.product_name,
            p.base_price,
            ROUND(AVG(o.price_each), 2) AS avg_paid
        FROM products p
        JOIN orders o ON o.product_id = p.product_id
        GROUP BY p.product_id, p.product_name, p.base_price
        HAVING AVG(o.price_each) > p.base_price
        ORDER BY (AVG(o.price_each) - p.base_price) DESC;
    """).fetchdf()

    show(_df, "Products Selling Above Base Price")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q50. Best-Selling Product Per Country (by Units)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        WITH country_product AS (
        SELECT
            c.country,
            p.product_name,
            SUM(o.quantity) AS total_units
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        JOIN products p ON p.product_id = o.product_id
        GROUP BY c.country, p.product_name ), ranked AS (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY country
        ORDER BY total_units DESC) AS rn
        FROM country_product )
        SELECT
            country,
            product_name,
            total_units
        FROM ranked
        WHERE rn = 1
        ORDER BY total_units DESC;
    """).fetchdf()

    show(_df, "Best-Selling Product Per Country")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q51. Customers Who Only Shop Online
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            c.customer_id,
            c.full_name,
            c.country
        FROM customers c
        WHERE EXISTS (
        SELECT 1
        FROM orders o
        WHERE o.customer_id = c.customer_id
        AND o.channel = 'online' )
        AND NOT EXISTS (
        SELECT 1
        FROM orders o
        WHERE o.customer_id = c.customer_id
        AND o.channel = 'store' )
        ORDER BY c.full_name;
    """).fetchdf()

    show(_df, "Online-Only Shoppers")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q52. Median Price Paid Per Product (PERCENTILE_CONT)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            p.product_name,
            ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (
        ORDER BY o.price_each), 2) AS median_price
        FROM orders o
        JOIN products p ON p.product_id = o.product_id
        GROUP BY p.product_name
        ORDER BY median_price DESC;
    """).fetchdf()

    show(_df, "Median Price Paid Per Product")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q53. Top 3 Customers Per Country by Revenue
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        WITH cust_country_rev AS (
        SELECT
            c.country,
            c.full_name,
            ROUND(SUM(o.quantity * o.price_each), 2) AS revenue
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.country, c.full_name ), ranked AS (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY country
        ORDER BY revenue DESC) AS rn
        FROM cust_country_rev )
        SELECT
            country,
            full_name,
            revenue,
            rn AS RANK
        FROM ranked
        WHERE rn <= 3
        ORDER BY country, rn;
    """).fetchdf()

    show(_df, "Top 3 Customers Per Country")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q54. Category Mix by Channel (Units Sold)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            o.channel,
            p.category,
            SUM(o.quantity) AS total_units
        FROM orders o
        JOIN products p ON p.product_id = o.product_id
        GROUP BY o.channel, p.category
        ORDER BY o.channel, total_units DESC;
    """).fetchdf()

    show(_df, "Category Mix by Channel")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q55. Days with Zero Orders in January 2025 (Calendar CTE)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        WITH RECURSIVE calendar AS (
        SELECT DATE '2025-01-01' AS dt
        UNION ALL
        SELECT dt + INTERVAL 1 DAY
        FROM calendar
        WHERE dt < DATE '2025-01-31' )
        SELECT cal.dt AS date_with_no_orders
        FROM calendar cal
        LEFT
        JOIN orders o ON o.order_date = cal.dt
        WHERE o.order_id IS NULL
        ORDER BY cal.dt;
    """).fetchdf()

    show(_df, "Zero-Order Days in January 2025")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q56. Customer Recency (Days Since Last Order)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            c.customer_id,
            c.full_name,
            MAX(o.order_date) AS last_order_date,
            CURRENT_DATE - MAX(o.order_date) AS days_since_last_order
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.full_name
        ORDER BY days_since_last_order ASC;
    """).fetchdf()

    show(_df, "Customer Recency")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q57. Revenue Contribution: Top 20% of Customers (Pareto)
    """)
    return


@app.cell
def _(con, plot_line, show):
    _df = con.execute("""
        WITH cust_rev AS (
        SELECT
            c.customer_id,
            c.full_name,
            ROUND(SUM(o.quantity * o.price_each), 2) AS revenue
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.full_name ), with_pct AS (
        SELECT
            *,
            ROUND(100.0 * revenue / SUM(revenue) OVER (), 2) AS pct_of_total,
            ROUND(100.0 * SUM(revenue) OVER (
        ORDER BY revenue DESC) / SUM(revenue) OVER (), 2) AS cumulative_pct
        FROM cust_rev )
        SELECT *
        FROM with_pct
        ORDER BY revenue DESC;
    """).fetchdf()

    show(_df, "Pareto Analysis — Customer Revenue Contribution")
    plot_line(_df, 'full_name', 'cumulative_pct', title="Cumulative Revenue % (Pareto Curve)", xlabel="Customer", ylabel="Cumulative %")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q58. Average Basket Size by Loyalty Tier
    """)
    return


@app.cell
def _(con, plot_grouped_bar, show):
    _df = con.execute("""
        SELECT
            c.loyalty_tier,
            ROUND(AVG(o.quantity), 2) AS avg_units,
            ROUND(AVG(o.quantity * o.price_each), 2) AS avg_basket_value
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.loyalty_tier
        ORDER BY avg_basket_value DESC;
    """).fetchdf()

    show(_df, "Basket Size by Loyalty Tier")
    plot_grouped_bar(_df, 'loyalty_tier', ['avg_units', 'avg_basket_value'],
                     title="Avg Units & Basket Value by Loyalty Tier", ylabel="Value")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q59. Products Purchased Together (Same Customer, Same Day)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            p1.product_name AS product_a,
            p2.product_name AS product_b,
            COUNT(*) AS co_purchase_count
        FROM orders o1
        JOIN orders o2 ON o1.customer_id = o2.customer_id
        AND o1.order_date = o2.order_date
        AND o1.product_id < o2.product_id
        JOIN products p1 ON p1.product_id = o1.product_id
        JOIN products p2 ON p2.product_id = o2.product_id
        GROUP BY p1.product_name, p2.product_name
        HAVING COUNT(*) >= 2
        ORDER BY co_purchase_count DESC;
    """).fetchdf()

    show(_df, "Frequently Co-Purchased Products (same customer, same day)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q60. Yearly Revenue Growth Rate
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        WITH yearly AS (
        SELECT
            YEAR(order_date) AS yr,
            ROUND(SUM(quantity * price_each), 2) AS revenue
        FROM orders
        GROUP BY yr )
        SELECT
            yr,
            revenue,
            LAG(revenue) OVER (
        ORDER BY yr) AS prev_year_rev, CASE WHEN LAG(revenue) OVER (
        ORDER BY yr) > 0 THEN ROUND(100.0 * (revenue - LAG(revenue) OVER (
        ORDER BY yr)) / LAG(revenue) OVER (
        ORDER BY yr), 1) ELSE NULL END AS yoy_growth_pct
        FROM yearly
        ORDER BY yr;
    """).fetchdf()

    show(_df, "Year-over-Year Revenue Growth")
    plot_bar(_df, 'yr', 'revenue', title="Annual Revenue", ylabel="Revenue ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🚀 Section 4 — Advanced Queries
    Complex analytics: cohort analysis, RFM segmentation, moving averages, and more.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q61. Customer Cohort by Join Quarter + Retention
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        WITH cohort AS (
        SELECT
            c.customer_id,
            YEAR(c.join_date) || '-Q' || QUARTER(c.join_date) AS join_cohort,
            YEAR(o.order_date) || '-Q' || QUARTER(o.order_date) AS order_quarter
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id )
        SELECT
            join_cohort,
            order_quarter,
            COUNT(DISTINCT customer_id) AS active_customers
        FROM cohort
        GROUP BY join_cohort, order_quarter
        ORDER BY join_cohort, order_quarter;
    """).fetchdf()

    show(_df, "Customer Cohort Activity")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q62. 3-Month Moving Average of Revenue
    """)
    return


@app.cell
def _(con, plot_line, show):
    _df = con.execute("""
        WITH monthly AS (
        SELECT
            STRFTIME(order_date, '%Y-%m') AS year_month,
            ROUND(SUM(quantity * price_each), 2) AS revenue
        FROM orders
        GROUP BY year_month )
        SELECT
            year_month,
            revenue,
            ROUND(AVG(revenue) OVER (
        ORDER BY year_month ROWS BETWEEN 2 PRECEDING
        AND CURRENT ROW ), 2) AS moving_avg_3m
        FROM monthly
        ORDER BY year_month;
    """).fetchdf()

    show(_df, "3-Month Moving Average")
    plot_line(_df, 'year_month', 'moving_avg_3m', title="3-Month Moving Average Revenue", xlabel="Month", ylabel="Revenue ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q63. RFM Segmentation (Recency, Frequency, Monetary)
    """)
    return


@app.cell
def _(con, plot_scatter, show):
    _df = con.execute("""
        WITH rfm AS (
        SELECT
            c.customer_id,
            c.full_name,
            CURRENT_DATE - MAX(o.order_date) AS recency_days,
            COUNT(*) AS frequency,
            ROUND(SUM(o.quantity * o.price_each), 2) AS monetary
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.full_name ), scored AS (
        SELECT
            *,
            NTILE(3) OVER (
        ORDER BY recency_days ASC) AS r_score, NTILE(3) OVER (
        ORDER BY frequency DESC) AS f_score, NTILE(3) OVER (
        ORDER BY monetary DESC) AS m_score
        FROM rfm )
        SELECT
            customer_id,
            full_name,
            recency_days,
            frequency,
            monetary,
            r_score,
            f_score,
            m_score,
            (r_score + f_score + m_score) AS rfm_total
        FROM scored
        ORDER BY rfm_total DESC, monetary DESC;
    """).fetchdf()

    show(_df, "RFM Segmentation")
    plot_scatter(_df, 'frequency', 'monetary', title="RFM: Frequency vs Monetary Value",
                 xlabel="Order Frequency", ylabel="Total Spend ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q64. Channel Preference Shift Over Time
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            STRFTIME(order_date, '%Y-%m') AS year_month,
            channel,
            COUNT(*) AS orders,
            ROUND(SUM(quantity * price_each), 2) AS revenue
        FROM orders
        GROUP BY year_month, channel
        ORDER BY year_month, channel;
    """).fetchdf()

    show(_df, "Channel Performance Over Time")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q65. Price Elasticity Indicator (% change price vs base)
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT
            p.product_name,
            p.base_price,
            ROUND(AVG(o.price_each), 2) AS avg_actual_price,
            ROUND(100.0 * (AVG(o.price_each) - p.base_price) / p.base_price, 1) AS price_change_pct,
            SUM(o.quantity) AS total_units
        FROM orders o
        JOIN products p ON p.product_id = o.product_id
        GROUP BY p.product_name, p.base_price
        ORDER BY price_change_pct DESC;
    """).fetchdf()

    show(_df, "Price Deviation from Base Price")
    plot_bar(_df, 'product_name', 'price_change_pct',
             title="% Price Change from Base (Avg Paid vs List)", ylabel="% Change", rotate_x=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q66. Customer Lifetime Value (Simple LTV = Revenue / Tenure in Months)
    """)
    return


@app.cell
def _(con, plot_hbar, show):
    _df = con.execute("""
        WITH cust_metrics AS (
        SELECT
            c.customer_id,
            c.full_name,
            c.join_date,
            ROUND(SUM(o.quantity * o.price_each), 2) AS total_revenue,
            GREATEST( DATEDIFF('month', c.join_date, CURRENT_DATE), 1 ) AS tenure_months
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.full_name, c.join_date )
        SELECT
            customer_id,
            full_name,
            total_revenue,
            tenure_months,
            ROUND(total_revenue / tenure_months, 2) AS monthly_ltv
        FROM cust_metrics
        ORDER BY monthly_ltv DESC;
    """).fetchdf()

    show(_df, "Customer LTV (Monthly Rate)")
    plot_hbar(_df.head(10), 'full_name', 'monthly_ltv',
              title="Top 10 Customers by Monthly LTV", xlabel="Monthly LTV ($)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q67. Repeat Purchase Rate by Product
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        WITH product_buyers AS (
        SELECT
            product_id,
            customer_id,
            COUNT(*) AS purchase_count
        FROM orders
        GROUP BY product_id, customer_id )
        SELECT
            p.product_name,
            COUNT(*) AS total_buyers,
            SUM(CASE WHEN pb.purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_buyers,
            ROUND(100.0 * SUM(CASE WHEN pb.purchase_count > 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS repeat_rate_pct
        FROM product_buyers pb
        JOIN products p ON p.product_id = pb.product_id
        GROUP BY p.product_name
        ORDER BY repeat_rate_pct DESC;
    """).fetchdf()

    show(_df, "Repeat Purchase Rate by Product")
    plot_bar(_df, 'product_name', 'repeat_rate_pct',
             title="Repeat Purchase Rate (%)", ylabel="% Repeat Buyers", rotate_x=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q68. New vs Returning Customers Per Month
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        WITH first_order AS (
        SELECT
            customer_id,
            MIN(order_date) AS first_order_date
        FROM orders
        GROUP BY customer_id ), classified AS (
        SELECT
            o.order_id,
            STRFTIME(o.order_date, '%Y-%m') AS year_month,
            CASE WHEN o.order_date = f.first_order_date THEN 'New' ELSE 'Returning' END AS customer_type
        FROM orders o
        JOIN first_order f ON f.customer_id = o.customer_id )
        SELECT
            year_month,
            customer_type,
            COUNT(*) AS order_count
        FROM classified
        GROUP BY year_month, customer_type
        ORDER BY year_month, customer_type;
    """).fetchdf()

    show(_df, "New vs Returning Customer Orders by Month")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q69. Revenue Percentiles (P25, P50, P75, P90)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (
        ORDER BY quantity * price_each), 2) AS p25, ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (
        ORDER BY quantity * price_each), 2) AS p50_median, ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (
        ORDER BY quantity * price_each), 2) AS p75, ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (
        ORDER BY quantity * price_each), 2) AS p90
        FROM orders;
    """).fetchdf()

    show(_df, "Order Revenue Distribution (Percentiles)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q70. Product Category Growth: 2024 vs 2025
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        WITH by_year AS (
        SELECT
            p.category,
            YEAR(o.order_date) AS yr,
            ROUND(SUM(o.quantity * o.price_each), 2) AS revenue
        FROM orders o
        JOIN products p ON p.product_id = o.product_id
        GROUP BY p.category, yr )
        SELECT
            a.category,
            a.revenue AS rev_2024,
            b.revenue AS rev_2025,
            ROUND(100.0 * (b.revenue - a.revenue) / a.revenue, 1) AS growth_pct
        FROM by_year a
        JOIN by_year b ON a.category = b.category
        WHERE a.yr = 2024
        AND b.yr = 2025
        ORDER BY growth_pct DESC;
    """).fetchdf()

    show(_df, "Category Revenue Growth: 2024 → 2025")
    plot_bar(_df, 'category', 'growth_pct',
             title="Category Revenue Growth 2024→2025 (%)", ylabel="Growth %", rotate_x=30)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ✅ Summary

    This notebook demonstrated **70 queries** across four skill levels:

    | Section | Level | Concepts |
    |---------|-------|----------|
    | 1 | Basic | SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, aliases |
    | 2 | Basic-to-Intermediate | JOIN, GROUP BY, HAVING, aggregates, computed columns |
    | 3 | Intermediate | CTEs, Window Functions, RANK, LAG, PERCENTILE, running totals |
    | 4 | Advanced | Cohort analysis, RFM, moving averages, LTV, Pareto, co-purchases |

    **Helper module:** `freshcart_helpers.py` — provides `show()`, `plot_bar()`, `plot_line()`, `plot_pie()`, `plot_hbar()`, `plot_grouped_bar()`, `plot_scatter()`

    ---
    *Generated for OMIS 105 — FreshCart Analytics*
    """)
    return


if __name__ == "__main__":
    app.run()
