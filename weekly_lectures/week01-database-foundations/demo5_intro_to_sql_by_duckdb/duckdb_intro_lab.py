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
    <div style="background:linear-gradient(135deg,#0f1117 0%,#1a1d2e 100%);border-radius:16px;padding:40px 48px;margin-bottom:24px;border:2px solid #FFD700;box-shadow:0 8px 32px rgba(255,215,0,0.15);">
      <div style="font-size:3.5em;margin-bottom:8px;">&#x1F986;</div>
      <h1 style="font-family:Segoe UI,sans-serif;font-size:2.4em;font-weight:900;background:linear-gradient(135deg,#FFD700,#FFA500);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:0 0 8px 0;">Introduction to DuckDB &amp; SQL</h1>
      <h2 style="color:#c3c8e8;font-size:1.2em;font-weight:400;margin:0 0 20px 0;">DBMS 101 - Day 1 Hands-On Lab</h2>
      <p style="color:#8892b0;font-size:0.95em;margin:0;">By the end of this notebook you will have written real SQL queries on five datasets, produced publication-quality charts, and understood the full SELECT &rarr; GROUP BY &rarr; visualize pipeline.</p>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 0 - Install & Import Everything

    Run this cell first. It sets up DuckDB and all visualization libraries.
    """)
    return


@app.cell
def _():
    # Uncomment to install:
    # !pip install duckdb pandas matplotlib

    import duckdb
    import pandas as pd

    # Everything else — table display, charts — lives in plots.py
    from plots import (
        run, show_table,
        plot_revenue_by_category,
        plot_monthly_trend,
        plot_customer_tiers,
        plot_employee_analytics,
        plot_movie_dashboard,
        plot_customer_leaderboard,
    )

    print(f'DuckDB {duckdb.__version__} | Pandas {pd.__version__} | Ready!')
    return (
        duckdb,
        plot_customer_leaderboard,
        plot_customer_tiers,
        plot_employee_analytics,
        plot_monthly_trend,
        plot_movie_dashboard,
        plot_revenue_by_category,
        run,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 1 - Create Sample Datasets

    We build **5 interconnected tables** that simulate a real e-commerce company. Data is inserted via Python tuples — clean, no SQL escaping issues!

    | Table | Description | Rows |
    |---|---|---|
    | `customers` | Customer profiles with tier & country | 12 |
    | `products` | Product catalog with categories & margins | 20 |
    | `orders` | Purchase transactions linking customers & products | 50 |
    | `employees` | Staff records with salaries & ratings | 20 |
    | `movies` | Film database for bonus queries | 15 |
    """)
    return


@app.cell
def _(duckdb):
    con = duckdb.connect()

    # ── CUSTOMERS ────────────────────────────────────────────────────────────────
    con.execute("""
    CREATE OR REPLACE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name        VARCHAR,
        email       VARCHAR,
        city        VARCHAR,
        country     VARCHAR,
        age         INTEGER,
        signup_year INTEGER,
        tier        VARCHAR
    )
    """)

    customers = [
        (1,  "Alice Chen",      "alice@email.com",    "San Francisco", "USA",     29, 2019, "Gold"),
        (2,  "Bob Martin",      "bob@email.com",      "New York",      "USA",     35, 2018, "Platinum"),
        (3,  "Carlos Rivera",   "carlos@email.com",   "Mexico City",   "Mexico",  28, 2020, "Silver"),
        (4,  "Diana Prince",    "diana@email.com",    "London",        "UK",      31, 2017, "Platinum"),
        (5,  "Emma Schmidt",    "emma@email.com",     "Berlin",        "Germany", 26, 2021, "Bronze"),
        (6,  "Faisal Al-Amin",  "faisal@email.com",   "Dubai",         "UAE",     38, 2019, "Gold"),
        (7,  "Grace Okafor",    "grace@email.com",    "Lagos",         "Nigeria", 24, 2022, "Bronze"),
        (8,  "Hiroshi Tanaka",  "hiroshi@email.com",  "Tokyo",         "Japan",   42, 2016, "Platinum"),
        (9,  "Isabelle Dupont", "isabelle@email.com", "Paris",         "France",  33, 2020, "Silver"),
        (10, "James O'Brien",   "james@email.com",    "Dublin",        "Ireland", 27, 2021, "Bronze"),
        (11, "Kavya Sharma",    "kavya@email.com",    "Mumbai",        "India",   30, 2019, "Silver"),
        (12, "Luca Ferrari",    "luca@email.com",     "Milan",         "Italy",   45, 2015, "Gold"),
    ]
    con.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?,?)", customers)

    # ── PRODUCTS ─────────────────────────────────────────────────────────────────
    con.execute("""
    CREATE OR REPLACE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name       VARCHAR,
        category   VARCHAR,
        brand      VARCHAR,
        price      DECIMAL(10,2),
        cost       DECIMAL(10,2),
        stock      INTEGER
    )
    """)

    products = [
        (1,  "ProBook Laptop 15",      "Electronics",  "TechCo",     1299.99,  720.00,  45),
        (2,  "Wireless Earbuds X3",    "Electronics",  "SoundWave",   149.99,   42.00, 210),
        (3,  "Smart Watch Series 7",   "Electronics",  "TimeTech",    399.99,  180.00,  88),
        (4,  "Mechanical Keyboard",    "Electronics",  "TypePro",     129.99,   55.00, 120),
        (5,  "USB-C Hub 7-Port",       "Electronics",  "ConnectAll",   59.99,   18.00, 340),
        (6,  "Running Shoes Ultra",    "Footwear",     "SpeedFoot",   189.99,   72.00,  95),
        (7,  "Hiking Boots Trek",      "Footwear",     "TrailBoss",   249.99,  110.00,  60),
        (8,  "Yoga Mat Premium",       "Fitness",      "ZenLife",      49.99,   14.00, 175),
        (9,  "Dumbbell Set 20kg",      "Fitness",      "IronPump",    199.99,   88.00,  40),
        (10, "Protein Powder Vanilla", "Nutrition",    "MuscleMax",    54.99,   22.00, 260),
        (11, "Vitamin D3 Capsules",    "Nutrition",    "VitaPlus",     19.99,    5.50, 500),
        (12, "Office Chair Ergo",      "Furniture",    "WorkComfort", 449.99,  210.00,  28),
        (13, "Standing Desk 140cm",    "Furniture",    "WorkComfort", 699.99,  320.00,  15),
        (14, "Bookshelf 5-Tier",       "Furniture",    "HomeStyle",   179.99,   78.00,  55),
        (15, "Coffee Maker Pro",       "Kitchen",      "BrewMaster",  129.99,   52.00,  90),
        (16, "Air Fryer XL 5L",        "Kitchen",      "CrispKing",   149.99,   58.00,  72),
        (17, "Blender 1200W",          "Kitchen",      "BlendTech",    89.99,   34.00, 110),
        (18, "Fantasy Novel: Ember",   "Books",        "PageTurn",     24.99,    8.00, 200),
        (19, "SQL for Beginners",      "Books",        "TechRead",     39.99,   12.00, 350),
        (20, "Watercolor Set 48",      "Art and Craft","ColorBurst",   44.99,   16.00, 130),
    ]
    con.executemany("INSERT INTO products VALUES (?,?,?,?,?,?,?)", products)

    # ── ORDERS ───────────────────────────────────────────────────────────────────
    con.execute("""
    CREATE OR REPLACE TABLE orders (
        order_id    INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id  INTEGER,
        quantity    INTEGER,
        order_date  DATE,
        status      VARCHAR
    )
    """)

    orders = [
        (1,  2,  1,  1, "2024-01-05", "Delivered"), (2,  4,  3,  1, "2024-01-08", "Delivered"),
        (3,  8,  1,  2, "2024-01-12", "Delivered"), (4,  1,  2,  1, "2024-01-15", "Delivered"),
        (5,  6,  12, 1, "2024-01-18", "Delivered"), (6,  3,  10, 2, "2024-01-22", "Delivered"),
        (7,  11, 8,  3, "2024-01-25", "Delivered"), (8,  5,  19, 1, "2024-02-01", "Delivered"),
        (9,  12, 15, 1, "2024-02-04", "Delivered"), (10, 4,  13, 1, "2024-02-07", "Delivered"),
        (11, 2,  4,  1, "2024-02-11", "Delivered"), (12, 8,  3,  1, "2024-02-14", "Delivered"),
        (13, 1,  9,  1, "2024-02-18", "Delivered"), (14, 6,  5,  3, "2024-02-21", "Delivered"),
        (15, 9,  18, 2, "2024-02-25", "Delivered"), (16, 3,  11, 4, "2024-03-01", "Delivered"),
        (17, 7,  8,  1, "2024-03-03", "Delivered"), (18, 10, 6,  1, "2024-03-07", "Delivered"),
        (19, 12, 16, 1, "2024-03-10", "Delivered"), (20, 2,  1,  1, "2024-03-14", "Delivered"),
        (21, 4,  2,  2, "2024-03-17", "Delivered"), (22, 8,  5,  2, "2024-03-20", "Delivered"),
        (23, 11, 10, 3, "2024-03-24", "Delivered"), (24, 1,  17, 1, "2024-03-27", "Delivered"),
        (25, 6,  12, 1, "2024-04-01", "Delivered"), (26, 9,  3,  1, "2024-04-04", "Delivered"),
        (27, 5,  9,  1, "2024-04-08", "Delivered"), (28, 3,  7,  1, "2024-04-11", "Delivered"),
        (29, 12, 4,  2, "2024-04-15", "Delivered"), (30, 7,  19, 2, "2024-04-18", "Delivered"),
        (31, 10, 20, 1, "2024-04-22", "Delivered"), (32, 2,  15, 1, "2024-04-25", "Delivered"),
        (33, 4,  1,  1, "2024-05-01", "Delivered"), (34, 8,  6,  1, "2024-05-04", "Delivered"),
        (35, 1,  3,  1, "2024-05-08", "Delivered"), (36, 11, 14, 1, "2024-05-11", "Delivered"),
        (37, 6,  2,  3, "2024-05-15", "Shipped"),   (38, 9,  10, 2, "2024-05-18", "Shipped"),
        (39, 3,  16, 1, "2024-05-22", "Processing"),(40, 12, 13, 1, "2024-05-25", "Processing"),
        (41, 5,  1,  1, "2024-06-01", "Processing"),(42, 7,  12, 1, "2024-06-04", "Pending"),
        (43, 10, 3,  1, "2024-06-07", "Pending"),   (44, 2,  7,  1, "2024-06-10", "Pending"),
        (45, 4,  18, 3, "2024-06-13", "Pending"),   (46, 8,  11, 6, "2024-06-16", "Pending"),
        (47, 1,  5,  4, "2024-06-19", "Pending"),   (48, 11, 17, 2, "2024-06-22", "Pending"),
        (49, 6,  9,  1, "2024-06-25", "Pending"),   (50, 9,  20, 2, "2024-06-28", "Pending"),
    ]
    con.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", orders)

    # ── EMPLOYEES ────────────────────────────────────────────────────────────────
    con.execute("""
    CREATE OR REPLACE TABLE employees (
        employee_id INTEGER PRIMARY KEY,
        name        VARCHAR,
        department  VARCHAR,
        role        VARCHAR,
        salary      DECIMAL(10,2),
        years_exp   INTEGER,
        rating      DECIMAL(3,1),
        hire_year   INTEGER
    )
    """)

    employees = [
        (1,  "Ava Thompson",   "Engineering",  "Senior Engineer",    125000, 8,  4.8, 2016),
        (2,  "Ben Liu",        "Engineering",  "Junior Engineer",     72000, 2,  3.9, 2022),
        (3,  "Clara Santos",   "Engineering",  "Lead Engineer",      148000, 12, 4.9, 2012),
        (4,  "Derek Johnson",  "Engineering",  "Junior Engineer",     68000, 1,  3.7, 2023),
        (5,  "Ella Park",      "Data Science", "Data Scientist",     115000, 6,  4.7, 2018),
        (6,  "Frank Nguyen",   "Data Science", "Senior Scientist",   138000, 9,  4.6, 2015),
        (7,  "Gloria Reyes",   "Data Science", "ML Engineer",        128000, 7,  4.5, 2017),
        (8,  "Hassan Ali",     "Marketing",    "Marketing Manager",   98000, 10, 4.4, 2014),
        (9,  "Iris Weber",     "Marketing",    "Content Specialist",  65000, 3,  4.0, 2021),
        (10, "Jake Brown",     "Marketing",    "SEO Analyst",         72000, 4,  3.8, 2020),
        (11, "Kim Nakamura",   "Sales",        "Account Executive",   95000, 7,  4.7, 2017),
        (12, "Leo Patel",      "Sales",        "Sales Manager",      110000, 11, 4.8, 2013),
        (13, "Mia Costa",      "Sales",        "Sales Rep",           62000, 2,  3.6, 2022),
        (14, "Noah Wilson",    "HR",           "HR Manager",          88000, 9,  4.3, 2015),
        (15, "Olivia Taylor",  "HR",           "Recruiter",           61000, 2,  4.1, 2022),
        (16, "Paulo Ferreira", "Finance",      "CFO",                195000, 18, 4.9, 2006),
        (17, "Quinn Murphy",   "Finance",      "Financial Analyst",   85000, 5,  4.2, 2019),
        (18, "Rachel Green",   "Finance",      "Accountant",          76000, 6,  4.3, 2018),
        (19, "Sam Goldstein",  "Engineering",  "DevOps Engineer",    108000, 6,  4.4, 2018),
        (20, "Tina Brooks",    "Data Science", "Data Analyst",        89000, 4,  4.2, 2020),
    ]
    con.executemany("INSERT INTO employees VALUES (?,?,?,?,?,?,?,?)", employees)

    # ── MOVIES ───────────────────────────────────────────────────────────────────
    con.execute("""
    CREATE OR REPLACE TABLE movies (
        movie_id     INTEGER PRIMARY KEY,
        title        VARCHAR,
        genre        VARCHAR,
        year         INTEGER,
        director     VARCHAR,
        rating       DECIMAL(3,1),
        box_office_m DECIMAL(8,1),
        runtime_min  INTEGER
    )
    """)

    movies = [
        (1,  "Galactic Frontier",    "Sci-Fi",   2023, "A. Rodriguez", 8.4, 412.5, 148),
        (2,  "The Last Kingdom",     "Drama",    2022, "M. Okonkwo",   7.9, 198.3, 134),
        (3,  "Pixel Perfect",        "Comedy",   2023, "S. Tanaka",    7.2,  89.4, 102),
        (4,  "Crimson Tide Rising",  "Thriller", 2021, "P. Novak",     8.1, 267.8, 121),
        (5,  "Into the Abyss",       "Sci-Fi",   2022, "L. Park",      7.6, 183.2, 155),
        (6,  "A Chefs Journey",      "Drama",    2023, "C. Beaumont",  8.3, 142.6, 112),
        (7,  "Hack the Planet",      "Sci-Fi",   2021, "A. Rodriguez", 7.8, 221.0, 139),
        (8,  "Laughing All the Way", "Comedy",   2022, "J. Williams",  6.9,  67.3,  98),
        (9,  "Midnight Stalker",     "Thriller", 2023, "P. Novak",     8.6, 334.7, 128),
        (10, "Ocean Deep",           "Drama",    2021, "M. Okonkwo",   7.4, 156.9, 118),
        (11, "Stellar Bloom",        "Sci-Fi",   2023, "L. Park",      8.0, 289.4, 142),
        (12, "Perfect Timing",       "Comedy",   2023, "J. Williams",  7.5,  95.1, 105),
        (13, "Shadow Protocol",      "Thriller", 2022, "C. Beaumont",  7.7, 198.8, 116),
        (14, "The Long Walk Home",   "Drama",    2022, "S. Tanaka",    8.2, 172.4, 127),
        (15, "Neon Dystopia",        "Sci-Fi",   2021, "A. Rodriguez", 7.3, 162.1, 134),
    ]
    con.executemany("INSERT INTO movies VALUES (?,?,?,?,?,?,?,?)", movies)

    print("5 tables created successfully!")
    print("  customers (12)  products (20)  orders (50)  employees (20)  movies (15)")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 2 - Explore Tables with SELECT

    Let's start simple and look at what's in our tables.
    """)
    return


@app.cell
def _(con, run):
    run("""
    SELECT * FROM customers ORDER BY customer_id
    """, title="All Customers", con=con)
    return


@app.cell
def _(con, run):
    run("""
    SELECT product_id, name, category, brand, price, stock
    FROM products
    ORDER BY category, price DESC
    """, title="Product Catalog sorted by category & price", con=con)
    return


@app.cell
def _(con, run):
    run("""
    SELECT name, category, price,
           ROUND((price - cost) / price * 100, 1) AS margin_pct
    FROM products
    WHERE price >= 150
    ORDER BY price DESC
    """, title="Premium Products (price >= $150) with Profit Margin", con=con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 3 - GROUP BY: Sales Analysis

    `GROUP BY` computes statistics *per group*. This is where data analysis gets powerful.
    """)
    return


@app.cell
def _(con, run):
    revenue_df = run("""
    SELECT
        p.category,
        COUNT(DISTINCT o.order_id)            AS total_orders,
        SUM(o.quantity)                       AS units_sold,
        ROUND(SUM(o.quantity * p.price), 2)   AS total_revenue,
        ROUND(AVG(p.price), 2)               AS avg_product_price
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_revenue DESC
    """, title="Revenue by Product Category", con=con)
    return (revenue_df,)


@app.cell
def _(plot_revenue_by_category, revenue_df):
    plot_revenue_by_category(revenue_df)
    return


@app.cell
def _(con, run):
    monthly_df = run("""
    SELECT
        strftime(o.order_date, '%Y-%m')           AS month,
        COUNT(DISTINCT o.order_id)                 AS num_orders,
        ROUND(SUM(o.quantity * p.price), 2)        AS revenue,
        ROUND(AVG(o.quantity * p.price), 2)        AS avg_order_value
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    GROUP BY strftime(o.order_date, '%Y-%m')
    ORDER BY month
    """, title="Monthly Revenue Trend (Jan-Jun 2024)", con=con)
    return (monthly_df,)


@app.cell
def _(monthly_df, plot_monthly_trend):
    plot_monthly_trend(monthly_df)
    return


@app.cell
def _(con, run):
    tier_df = run("""
    SELECT
        c.tier,
        COUNT(DISTINCT c.customer_id)             AS customer_count,
        COUNT(o.order_id)                          AS total_orders,
        ROUND(SUM(o.quantity * p.price), 2)        AS total_spent,
        ROUND(AVG(o.quantity * p.price), 2)        AS avg_order_value,
        ROUND(SUM(o.quantity * p.price) /
              COUNT(DISTINCT c.customer_id), 2)    AS revenue_per_customer
    FROM customers c
    LEFT JOIN orders   o ON c.customer_id = o.customer_id
    LEFT JOIN products p ON o.product_id  = p.product_id
    GROUP BY c.tier
    HAVING COUNT(o.order_id) > 0
    ORDER BY revenue_per_customer DESC
    """, title="Customer Tier Analysis — HAVING removes tiers with 0 orders", con=con)
    return (tier_df,)


@app.cell
def _(plot_customer_tiers, tier_df):
    plot_customer_tiers(tier_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 4 - Employee Analytics with GROUP BY
    """)
    return


@app.cell
def _(con, run):
    dept_df = run("""
    SELECT
        department,
        COUNT(*)                    AS headcount,
        ROUND(AVG(salary), 0)       AS avg_salary,
        MIN(salary)                 AS min_salary,
        MAX(salary)                 AS max_salary,
        ROUND(AVG(years_exp), 1)    AS avg_experience,
        ROUND(AVG(rating), 2)       AS avg_rating
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
    """, title="Department Salary & Performance Summary", con=con)
    return (dept_df,)


@app.cell
def _(con, dept_df, plot_employee_analytics):
    plot_employee_analytics(dept_df, con)
    return


@app.cell
def _(con, run):
    # HAVING demo — only departments with 3+ employees
    run("""
    SELECT department, COUNT(*) AS headcount,
           ROUND(AVG(salary), 0) AS avg_salary,
           ROUND(AVG(years_exp), 1) AS avg_experience
    FROM employees
    GROUP BY department
    HAVING COUNT(*) >= 3
    ORDER BY avg_salary DESC
    """, title="Departments with 3+ Employees — HAVING demo", con=con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 5 - Movie Database Analytics
    """)
    return


@app.cell
def _(con, run):
    genre_df = run("""
    SELECT
        genre,
        COUNT(*)                      AS num_movies,
        ROUND(AVG(rating), 2)         AS avg_rating,
        MAX(rating)                   AS best_rating,
        ROUND(AVG(box_office_m), 1)   AS avg_box_office_m,
        ROUND(SUM(box_office_m), 1)   AS total_box_office_m,
        ROUND(AVG(runtime_min), 0)    AS avg_runtime_min
    FROM movies
    GROUP BY genre
    ORDER BY total_box_office_m DESC
    """, title="Movie Genre Analysis", con=con)
    return (genre_df,)


@app.cell
def _(con, genre_df, plot_movie_dashboard):
    plot_movie_dashboard(genre_df, con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 6 - INNER JOIN: Combining Tables

    Real answers come from linking tables together.
    """)
    return


@app.cell
def _(con, run):
    run("""
    SELECT
        o.order_id,
        o.order_date,
        c.name                          AS customer,
        c.tier,
        c.country,
        p.name                          AS product,
        p.category,
        o.quantity,
        p.price,
        ROUND(o.quantity * p.price, 2)  AS line_total,
        o.status
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    INNER JOIN products  p ON o.product_id  = p.product_id
    ORDER BY o.order_date DESC
    LIMIT 20
    """, title="Full Order Report (latest 20) — 3-way INNER JOIN", con=con)
    return


@app.cell
def _(con, run):
    top_customers = run("""
    SELECT
        c.name,
        c.tier,
        c.country,
        COUNT(o.order_id)                    AS total_orders,
        ROUND(SUM(o.quantity * p.price), 2)  AS total_spent,
        ROUND(AVG(o.quantity * p.price), 2)  AS avg_order_value
    FROM customers c
    INNER JOIN orders   o ON c.customer_id = o.customer_id
    INNER JOIN products p ON o.product_id  = p.product_id
    GROUP BY c.customer_id, c.name, c.tier, c.country
    ORDER BY total_spent DESC
    """, title="Customer Leaderboard — Total Spend (JOIN + GROUP BY)", con=con)
    return (top_customers,)


@app.cell
def _(plot_customer_leaderboard, top_customers):
    plot_customer_leaderboard(top_customers)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 7 - Your Turn: Practice Challenges

    Write the SQL yourself first — then run the answer cell to check!
    """)
    return


@app.cell
def _(con, run):
    # CHALLENGE 1
    # Which product category has the highest profit margin?
    # margin_pct = (price - cost) / price * 100

    run("""
    -- YOUR CODE HERE
    SELECT 'Replace this with your query!' AS hint
    """, title="Challenge 1 - Your Answer", con=con)
    return


@app.cell
def _(con, run):
    # Answer 1:
    run("""
    SELECT
        category,
        ROUND(AVG(price - cost), 2)              AS avg_profit_per_unit,
        ROUND(AVG((price - cost)/price*100), 1)  AS avg_margin_pct
    FROM products
    GROUP BY category
    ORDER BY avg_margin_pct DESC
    """, title="Challenge 1 ANSWER — Profit Margin by Category", con=con)
    return


@app.cell
def _(con, run):
    # CHALLENGE 2
    # List countries with MORE than 1 customer.
    # Show: country, num_customers — sorted descending.

    run("""
    -- YOUR CODE HERE
    SELECT 'Replace this with your query!' AS hint
    """, title="Challenge 2 - Your Answer", con=con)
    return


@app.cell
def _(con, run):
    # Answer 2 (uses HAVING!):
    run("""
    SELECT country, COUNT(*) AS num_customers
    FROM customers
    GROUP BY country
    HAVING COUNT(*) > 1
    ORDER BY num_customers DESC
    """, title="Challenge 2 ANSWER — Countries with Multiple Customers", con=con)
    return


@app.cell
def _(con, run):
    # CHALLENGE 3 (uses JOIN!)
    # Find the top 5 best-selling products by total units sold.
    # Show: product name, category, units_sold

    run("""
    -- YOUR CODE HERE
    SELECT 'Replace this with your query!' AS hint
    """, title="Challenge 3 - Your Answer", con=con)
    return


@app.cell
def _(con, run):
    # Answer 3:
    run("""
    SELECT
        p.name          AS product_name,
        p.category,
        SUM(o.quantity) AS units_sold
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    GROUP BY p.product_id, p.name, p.category
    ORDER BY units_sold DESC
    LIMIT 5
    """, title="Challenge 3 ANSWER — Top 5 Products by Units Sold", con=con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## SQL Quick Reference — Keep This Handy!
    """)
    return


@app.cell
def _():
    print("""
    SQL QUERY STRUCTURE (clauses must be in this exact order):

      SELECT   col1, col2, AGG(col3) AS alias   <- what to show
      FROM     table_name                        <- where data lives
      JOIN     other ON a.id = b.id              <- combine tables
      WHERE    condition AND condition           <- filter ROWS
      GROUP BY col1, col2                        <- aggregate
      HAVING   AGG(col) > value                  <- filter GROUPS
      ORDER BY col DESC                          <- sort results
      LIMIT    10;                               <- cap row count

    AGGREGATE FUNCTIONS:
      COUNT(*)   SUM(col)   AVG(col)   MIN(col)   MAX(col)   ROUND(val, 2)

    WHERE OPERATORS:
      =  !=  >  <  >=  <=
      BETWEEN x AND y
      IN ('a', 'b', 'c')
      LIKE '%pattern%'
      IS NULL   IS NOT NULL
      AND   OR   NOT

    DUCKDB SUPERPOWERS:
      FROM 'file.csv'               -- query CSV directly
      FROM read_csv_auto('*.csv')   -- glob multiple files
      FROM my_pandas_dataframe      -- query pandas DataFrames
      duckdb.sql('SELECT ...').df() -- return result as pandas
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <div style="background:linear-gradient(135deg,#0f1117,#1a1d2e);border:2px solid #FFD700;border-radius:12px;padding:28px 36px;margin-top:24px;">
      <h2 style="color:#FFD700;font-family:Segoe UI,sans-serif;margin:0 0 12px 0;">Congratulations - You Completed Day 1!</h2>
      <p style="color:#c3c8e8;">You wrote real SQL queries across five datasets, joined three tables, used GROUP BY and HAVING, and built six charts. That is a complete data analysis pipeline!</p>
      <p style="color:#8892b0;font-size:0.9em;"><strong style="color:#FFD700;">Next class:</strong> Subqueries, CTEs (WITH clauses), and Window Functions.</p>
    </div>
    """)
    return


if __name__ == "__main__":
    app.run()
