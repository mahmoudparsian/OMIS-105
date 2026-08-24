import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    from plot_helpers import (
        bar_chart, pie_chart, line_chart, histogram, scatter_plot, heatmap, PALETTE
    )

    return (
        PALETTE,
        bar_chart,
        heatmap,
        histogram,
        line_chart,
        pie_chart,
        plt,
        scatter_plot,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Bookstore Analytics — A DuckDB + Marimo Practice Database

    This notebook is a **companion to `bookstore_analytics.ipynb`**, rebuilt
    as a reactive Marimo notebook. It uses the same bookstore data, but
    every cell runs live: change a query, and every cell that depends on
    it re-runs automatically.

    We will practice **27 SQL queries** across three levels:

    | Level | Count | You will practice |
    |---|---|---|
    | Basic | 5 | `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT` |
    | Intermediate | 15 | `JOIN`, `LEFT JOIN` (anti-joins), date functions, subqueries |
    | Advanced | 7 | `WITH` (CTEs), window functions (`LAG`, `NTILE`, running totals) |

    Each query follows the same four steps: **(1) the question we're
    answering, (2) the SQL concept it teaches, (3) the SQL query itself,
    and (4) the result — with a chart when a picture helps.**

    > Charts are drawn by helper functions in `plot_helpers.py`, so the
    > notebook cells can stay focused on SQL.

    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## About This Dataset

    A small online bookstore tracks three things: the **books** it
    sells, the **customers** who buy from it, and the **orders** they
    place. This is one of the most common patterns in business data —
    almost every store, app, or subscription service has some version of
    "things for sale," "people who buy," and "the purchases themselves."

    | Table | What it holds | Key columns |
    |---|---|---|
    | `books` | One row per book title | `book_id`, `title`, `author`, `genre`, `published_year`, `price`, `stock` |
    | `customers` | One row per customer | `customer_id`, `name`, `email`, `phone`, `city`, `country` |
    | `orders` | One row per order | `order_id`, `customer_id`, `book_id`, `order_date`, `quantity`, `total_amount` |

    **How the tables connect:**

    - `orders.book_id` &rarr; `books.book_id`
    - `orders.customer_id` &rarr; `customers.customer_id`

    `orders` is called a **fact table** — it records events (a purchase)
    and links out to the "who" and "what" of that event. `books` and
    `customers` are **dimension tables** — they describe the things
    involved. You will see this fact/dimension pattern in almost every
    real business database.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Step 1 — Load the Data and Remove Duplicates

    Real data is messy. The CSV files in `data/` contain a small number
    of **exact duplicate rows** — the same record, repeated. This can
    happen from a double file upload, a retry after a network error, or
    a copy-paste mistake. Before we analyze anything, we load each CSV
    raw (duplicates and all), count the rows, then use
    `SELECT DISTINCT` to keep only one copy of each unique row.

    This mirrors what `build_bookstore_db.py` does when it builds
    `bookstore.duckdb` — here we do it live, inside the notebook, so you
    can see every step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Table: `books`
    """)
    return


@app.cell
def _(mo):
    books_raw = mo.sql(
        f"""
        CREATE OR REPLACE TABLE books_raw AS
        SELECT * FROM read_csv_auto('data/books.csv', header=true);
        """
    )
    return


@app.cell
def _(books_raw, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS rows_loaded_with_duplicates FROM books_raw;
        """
    )
    return


@app.cell
def _(books_raw, mo):
    books = mo.sql(
        f"""
        CREATE OR REPLACE TABLE books AS
        SELECT DISTINCT * FROM books_raw;
        """
    )
    return


@app.cell
def _(books, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS rows_after_dedup FROM books;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Table: `customers`
    """)
    return


@app.cell
def _(mo):
    customers_raw = mo.sql(
        f"""
        CREATE OR REPLACE TABLE customers_raw AS
        SELECT * FROM read_csv_auto('data/customers.csv', header=true);
        """
    )
    return


@app.cell
def _(customers_raw, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS rows_loaded_with_duplicates FROM customers_raw;
        """
    )
    return


@app.cell
def _(customers_raw, mo):
    customers = mo.sql(
        f"""
        CREATE OR REPLACE TABLE customers AS
        SELECT DISTINCT * FROM customers_raw;
        """
    )
    return


@app.cell
def _(customers, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS rows_after_dedup FROM customers;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Table: `orders`
    """)
    return


@app.cell
def _(mo):
    orders_raw = mo.sql(
        f"""
        CREATE OR REPLACE TABLE orders_raw AS
        SELECT * FROM read_csv_auto('data/orders.csv', header=true);
        """
    )
    return


@app.cell
def _(mo, orders_raw):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS rows_loaded_with_duplicates FROM orders_raw;
        """
    )
    return


@app.cell
def _(mo, orders_raw):
    orders = mo.sql(
        f"""
        CREATE OR REPLACE TABLE orders AS
        SELECT DISTINCT * FROM orders_raw;
        """
    )
    return


@app.cell
def _(mo, orders):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS rows_after_dedup FROM orders;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    > **Checkpoint:** `books`, `customers`, and `orders` are now clean —
    > every remaining row is unique. All 27 queries below use these three
    > tables. If a chart or number ever looks wrong, this is the first
    > place to check.
    """)
    return


@app.cell
def _(books, customers, mo, orders):
    df_totals = mo.sql(
        f"""
        SELECT (SELECT COUNT(*) FROM books)     AS total_books,
               (SELECT COUNT(*) FROM customers) AS total_customers,
               (SELECT COUNT(*) FROM orders)    AS total_orders;
        """
    )
    return (df_totals,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Basic Queries

    Single-table queries: filtering, sorting, and simple aggregation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### B1 — Count of Books by Genre
    How many books do we carry in each genre?

    **Concept:** `GROUP BY` collects rows that share the same value into one group, so `COUNT(*)` can count books **per genre** instead of counting the whole table at once.
    """)
    return


@app.cell
def _(books, mo):
    df_b1 = mo.sql(
        f"""
        SELECT genre,
               COUNT(*) AS book_count
        FROM   books
        GROUP  BY genre
        ORDER  BY book_count DESC;
        """
    )
    return (df_b1,)


@app.cell
def _(bar_chart, df_b1, plt):
    bar_chart(df_b1, "genre", "book_count",
              "Number of Books per Genre",
              xlabel="Genre", ylabel="Books")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### B2 — Average Book Price
    What is the overall average price of books in the store?

    **Concept:** `AVG()`, `MIN()`, and `MAX()` are **aggregate functions** — each one takes many rows and collapses them into a single summary number.
    """)
    return


@app.cell
def _(books, mo):
    df_b2 = mo.sql(
        f"""
        SELECT ROUND(AVG(price), 2) AS avg_price,
               ROUND(MIN(price), 2) AS min_price,
               ROUND(MAX(price), 2) AS max_price
        FROM   books;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### B3 — Top 10 Most Recently Published Books
    Which 10 books were published most recently?

    **Concept:** `ORDER BY ... DESC` sorts rows from largest to smallest — here, newest year first. `LIMIT 10` keeps only the top 10 rows after sorting.
    """)
    return


@app.cell
def _(books, mo):
    df_b3 = mo.sql(
        f"""
        SELECT title, author, genre, published_year, price
        FROM   books
        ORDER  BY published_year DESC
        LIMIT  10;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### B4 — Customers per Country (Top 15)
    Which countries have the most customers?

    **Concept:** The same `GROUP BY` + `COUNT(*)` pattern from B1, now combined with `LIMIT` to show only the top 15 countries.
    """)
    return


@app.cell
def _(customers, mo):
    df_b4 = mo.sql(
        f"""
        SELECT country,
               COUNT(*) AS total_customers
        FROM   customers
        GROUP  BY country
        ORDER  BY total_customers DESC
        LIMIT  15;
        """
    )
    return (df_b4,)


@app.cell
def _(PALETTE, bar_chart, df_b4, plt):
    bar_chart(df_b4, "country", "total_customers",
              "Top 15 Countries by Customer Count",
              xlabel="Country", ylabel="Customers",
              color=PALETTE[1])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### B5 — Total Revenue
    What is the total revenue generated from all orders?

    **Concept:** `SUM()` adds up a column across every matching row. With no `WHERE` and no `GROUP BY`, it summarizes the **entire table** into one row.
    """)
    return


@app.cell
def _(mo, orders):
    df_b5 = mo.sql(
        f"""
        SELECT ROUND(SUM(total_amount), 2) AS total_revenue,
               COUNT(*)                    AS total_orders,
               ROUND(AVG(total_amount), 2) AS avg_order_value
        FROM   orders;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Intermediate Queries

    Now we combine tables with `JOIN`, work with dates, and meet the
    `LEFT JOIN` / `IS NULL` **anti-join** pattern for finding what's
    *missing*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I1 — Monthly Revenue Trend
    How does revenue change month over month?

    **Concept:** `STRFTIME(date, '%Y-%m')` reformats a `DATE` into text like `'2025-03'`, so `GROUP BY` can bucket orders by month instead of by exact day.
    """)
    return


@app.cell
def _(mo, orders):
    df_i1 = mo.sql(
        f"""
        SELECT STRFTIME(order_date, '%Y-%m') AS month,
               ROUND(SUM(total_amount), 2)   AS revenue,
               COUNT(*)                      AS orders
        FROM   orders
        GROUP  BY month
        ORDER  BY month;
        """
    )
    return (df_i1,)


@app.cell
def _(df_i1, line_chart, plt):
    line_chart(df_i1, "month", "revenue",
               "Monthly Revenue Trend",
               xlabel="Month", ylabel="Revenue ($)")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I2 — Revenue by Genre
    Which genres generate the most revenue?

    **Concept:** `orders` and `books` are separate tables. `JOIN ... ON` combines their rows using the shared `book_id`, so we can group *order* revenue by a *book* attribute (genre).
    """)
    return


@app.cell
def _(books, mo, orders):
    df_i2 = mo.sql(
        f"""
        SELECT b.genre,
               ROUND(SUM(o.total_amount), 2) AS revenue,
               SUM(o.quantity)               AS units_sold
        FROM   orders o
        JOIN   books b ON o.book_id = b.book_id
        GROUP  BY b.genre
        ORDER  BY revenue DESC;
        """
    )
    return (df_i2,)


@app.cell
def _(df_i2, pie_chart, plt):
    pie_chart(df_i2, "genre", "revenue",
              "Revenue Share by Genre")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I3 — Top 10 Best-Selling Books (by Quantity)
    Which individual titles sold the most copies?

    **Concept:** Same `JOIN` + `GROUP BY` pattern as I2, grouped by title/author instead of genre, then ranked with `ORDER BY` + `LIMIT`.
    """)
    return


@app.cell
def _(books, mo, orders):
    df_i3 = mo.sql(
        f"""
        SELECT b.title,
               b.author,
               SUM(o.quantity)               AS total_qty,
               ROUND(SUM(o.total_amount), 2) AS total_rev
        FROM   orders o
        JOIN   books b ON o.book_id = b.book_id
        GROUP  BY b.title, b.author
        ORDER  BY total_qty DESC
        LIMIT  10;
        """
    )
    return (df_i3,)


@app.cell
def _(PALETTE, bar_chart, df_i3, plt):
    bar_chart(df_i3, "title", "total_qty",
              "Top 10 Best-Selling Books by Quantity",
              xlabel="Book Title", ylabel="Units Sold",
              color=PALETTE[2], figsize=(12, 5))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I4 — Top 10 Customers by Total Spend
    Who are our highest-value customers?

    **Concept:** The same join pattern, this time linking `orders` to `customers` instead of `books`.
    """)
    return


@app.cell
def _(customers, mo, orders):
    df_i4 = mo.sql(
        f"""
        SELECT c.customer_id,
               c.name,
               c.country,
               COUNT(o.order_id)             AS order_count,
               ROUND(SUM(o.total_amount), 2) AS total_spent
        FROM   orders o
        JOIN   customers c ON o.customer_id = c.customer_id
        GROUP  BY c.customer_id, c.name, c.country
        ORDER  BY total_spent DESC
        LIMIT  10;
        """
    )
    return (df_i4,)


@app.cell
def _(PALETTE, bar_chart, df_i4, plt):
    bar_chart(df_i4, "name", "total_spent",
              "Top 10 Customers by Total Spend",
              xlabel="Customer", ylabel="Total Spent ($)",
              horizontal=True, color=PALETTE[3])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I5 — Year-over-Year Revenue
    How does annual revenue compare across years?

    **Concept:** `EXTRACT(YEAR FROM date)` pulls just the year out of a `DATE` value, so we can group by year the same way I1 grouped by month.
    """)
    return


@app.cell
def _(mo, orders):
    df_i5 = mo.sql(
        f"""
        SELECT EXTRACT(YEAR FROM order_date) AS year,
               ROUND(SUM(total_amount), 2)   AS revenue,
               COUNT(*)                      AS orders,
               ROUND(AVG(total_amount), 2)   AS avg_order
        FROM   orders
        GROUP  BY year
        ORDER  BY year;
        """
    )
    return (df_i5,)


@app.cell
def _(PALETTE, bar_chart, df_i5, plt):
    bar_chart(df_i5, "year", "revenue",
              "Annual Revenue",
              xlabel="Year", ylabel="Revenue ($)",
              color=PALETTE[4])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I6 — Orders per Day of Week
    Are there patterns in which day orders are placed?

    **Concept:** `DAYNAME()` and `DAYOFWEEK()` are date functions that read the weekday out of a `DATE` — handy for spotting weekly patterns.
    """)
    return


@app.cell
def _(mo, orders):
    df_i6 = mo.sql(
        f"""
        SELECT DAYNAME(order_date)   AS day_name,
               DAYOFWEEK(order_date) AS day_num,
               COUNT(*)              AS orders
        FROM   orders
        GROUP  BY day_name, day_num
        ORDER  BY day_num;
        """
    )
    return (df_i6,)


@app.cell
def _(PALETTE, bar_chart, df_i6, plt):
    bar_chart(df_i6, "day_name", "orders",
              "Orders by Day of Week",
              xlabel="Day", ylabel="Number of Orders",
              color=PALETTE[5])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I7 — Average Order Value by Genre
    Which genres command higher order values?

    **Concept:** Same join as I2, but `AVG()` instead of `SUM()` — this answers "how big is a typical order" rather than "how much money total."
    """)
    return


@app.cell
def _(books, mo, orders):
    df_i7 = mo.sql(
        f"""
        SELECT b.genre,
               ROUND(AVG(o.total_amount), 2) AS avg_order_value,
               ROUND(AVG(o.quantity), 1)     AS avg_qty
        FROM   orders o
        JOIN   books b ON o.book_id = b.book_id
        GROUP  BY b.genre
        ORDER  BY avg_order_value DESC;
        """
    )
    return (df_i7,)


@app.cell
def _(PALETTE, bar_chart, df_i7, plt):
    bar_chart(df_i7, "genre", "avg_order_value",
              "Average Order Value by Genre",
              xlabel="Genre", ylabel="Avg Order Value ($)",
              color=PALETTE[6])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I8 — Books That Have Never Been Ordered
    Are there books sitting unsold in inventory?

    **Concept:** A `LEFT JOIN` keeps **every** row from the left table (`books`), even when there is no matching order. Unmatched rows show `NULL` for the order's columns — so `WHERE o.order_id IS NULL` finds books with *no match at all*. This is called an **anti-join**, and it is the standard way to answer "which X have no related Y."
    """)
    return


@app.cell
def _(books, mo, orders):
    df_i8 = mo.sql(
        f"""
        SELECT b.book_id, b.title, b.author, b.genre, b.price, b.stock
        FROM   books b
        LEFT   JOIN orders o ON b.book_id = o.book_id
        WHERE  o.order_id IS NULL
        ORDER  BY b.stock DESC;
        """
    )
    return (df_i8,)


@app.cell
def _(df_i8, df_totals, mo):
    mo.md(f"""
    **{len(df_i8)}** of **{int(df_totals['total_books'][0])}** "
        f"books have never been ordered "
        f"({len(df_i8) / df_totals['total_books'][0] * 100:.1f}% of inventory).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I9 — Customer Order Frequency Distribution
    How many orders do most customers place?

    **Concept:** A **subquery** in parentheses runs first, and its result is treated like a temporary table for the outer query. Here the inner query counts orders per customer; the outer query counts how many customers land at each order count.
    """)
    return


@app.cell
def _(mo, orders):
    df_i9 = mo.sql(
        f"""
        SELECT order_count, COUNT(*) AS num_customers
        FROM (
            SELECT customer_id, COUNT(*) AS order_count
            FROM   orders
            GROUP  BY customer_id
        )
        GROUP BY order_count
        ORDER BY order_count;
        """
    )
    return (df_i9,)


@app.cell
def _(df_i9):
    # Keep the chart readable — focus on the common, low order counts
    df_i9_chart = df_i9.head(25)
    df_i9_chart
    return (df_i9_chart,)


@app.cell
def _(PALETTE, bar_chart, df_i9_chart, plt):
    bar_chart(df_i9_chart, "order_count", "num_customers",
              "Customer Order Frequency Distribution",
              xlabel="Number of Orders", ylabel="Number of Customers",
              color=PALETTE[0])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I10 — Quarterly Revenue by Year
    Revenue broken down by quarter and year.

    **Concept:** `EXTRACT(QUARTER FROM date)` returns 1-4. Grouping by both year and quarter gives one row per quarter across the whole date range.
    """)
    return


@app.cell
def _(mo, orders):
    df_i10 = mo.sql(
        f"""
        SELECT EXTRACT(YEAR FROM order_date)    AS year,
               EXTRACT(QUARTER FROM order_date) AS quarter,
               ROUND(SUM(total_amount), 2)      AS revenue
        FROM   orders
        GROUP  BY year, quarter
        ORDER  BY year, quarter;
        """
    )
    return (df_i10,)


@app.cell
def _(df_i10):
    # Build a "2023-Q1" style label for the x-axis
    df_i10_labeled = df_i10.copy()
    df_i10_labeled["label"] = (
        df_i10_labeled["year"].astype(int).astype(str)
        + "-Q" + df_i10_labeled["quarter"].astype(int).astype(str)
    )
    df_i10_labeled
    return (df_i10_labeled,)


@app.cell
def _(PALETTE, bar_chart, df_i10_labeled, plt):
    bar_chart(df_i10_labeled, "label", "revenue",
              "Quarterly Revenue",
              xlabel="Quarter", ylabel="Revenue ($)",
              color=PALETTE[2], figsize=(14, 5))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I11 — Price Distribution of Books
    What does the distribution of book prices look like, and what are its summary statistics?

    **Concept:** `MEDIAN()` and `STDDEV()` are aggregate functions too — median is the middle value, and standard deviation measures how spread out prices are around the average.
    """)
    return


@app.cell
def _(books, mo):
    df_i11 = mo.sql(
        f"""
        SELECT ROUND(AVG(price), 2)    AS avg_price,
               ROUND(MEDIAN(price), 2) AS median_price,
               ROUND(STDDEV(price), 2) AS stddev_price,
               MIN(price)              AS min_price,
               MAX(price)              AS max_price
        FROM   books;
        """
    )
    return


@app.cell
def _(books, mo):
    df_i11_prices = mo.sql(
        f"""
        SELECT price FROM books;
        """
    )
    return (df_i11_prices,)


@app.cell
def _(df_i11_prices, histogram, plt):
    histogram(df_i11_prices["price"], bins=25,
               title="Distribution of Book Prices",
               xlabel="Price ($)", ylabel="Number of Books")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I12 — Top 10 Authors by Revenue
    Which authors bring in the most money?

    **Concept:** `COUNT(DISTINCT column)` counts **unique** values only — a book that appears in 40 orders still counts once toward `books_in_store`.
    """)
    return


@app.cell
def _(books, mo, orders):
    df_i12 = mo.sql(
        f"""
        SELECT b.author,
               COUNT(DISTINCT b.book_id)     AS books_in_store,
               SUM(o.quantity)               AS units_sold,
               ROUND(SUM(o.total_amount), 2) AS total_revenue
        FROM   orders o
        JOIN   books b ON o.book_id = b.book_id
        GROUP  BY b.author
        ORDER  BY total_revenue DESC
        LIMIT  10;
        """
    )
    return (df_i12,)


@app.cell
def _(PALETTE, bar_chart, df_i12, plt):
    bar_chart(df_i12, "author", "total_revenue",
              "Top 10 Authors by Revenue",
              xlabel="Author", ylabel="Revenue ($)",
              horizontal=True, color=PALETTE[1], figsize=(12, 6))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I13 — November & December Sales Spike
    Do holiday months really outperform the rest?

    **Concept:** `MONTHNAME()` gives a readable month name. This query sets up a **two-axis chart** next — bars for revenue, a line for order count — so we can compare two different scales on one picture.
    """)
    return


@app.cell
def _(mo, orders):
    df_i13 = mo.sql(
        f"""
        SELECT EXTRACT(MONTH FROM order_date) AS month_num,
               MONTHNAME(order_date)          AS month_name,
               COUNT(*)                       AS orders,
               ROUND(SUM(total_amount), 2)    AS revenue
        FROM   orders
        GROUP  BY month_num, month_name
        ORDER  BY month_num;
        """
    )
    return (df_i13,)


@app.cell
def _(PALETTE, df_i13, plt):
    _fig, _ax1 = plt.subplots(figsize=(12, 5))
    _ax1.bar(df_i13["month_name"], df_i13["revenue"], color=PALETTE[0], alpha=0.7, label="Revenue")
    _ax1.set_ylabel("Revenue ($)", color=PALETTE[0])
    _ax1.set_xlabel("Month")
    _ax2 = _ax1.twinx()
    _ax2.plot(df_i13["month_name"], df_i13["orders"], color=PALETTE[3], marker="o", linewidth=2, label="Orders")
    _ax2.set_ylabel("Order Count", color=PALETTE[3])
    _ax1.set_title("Monthly Revenue & Order Count")
    _lines1, _labels1 = _ax1.get_legend_handles_labels()
    _lines2, _labels2 = _ax2.get_legend_handles_labels()
    _ax1.legend(_lines1 + _lines2, _labels1 + _labels2, loc="upper left")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I14 — Revenue by Country (Top 15)
    Which countries generate the most bookstore revenue?

    **Concept:** The same join-and-group pattern as I4, aggregated by country instead of by individual customer.
    """)
    return


@app.cell
def _(customers, mo, orders):
    df_i14 = mo.sql(
        f"""
        SELECT c.country,
               COUNT(DISTINCT c.customer_id)  AS customers,
               ROUND(SUM(o.total_amount), 2)  AS revenue
        FROM   orders o
        JOIN   customers c ON o.customer_id = c.customer_id
        GROUP  BY c.country
        ORDER  BY revenue DESC
        LIMIT  15;
        """
    )
    return (df_i14,)


@app.cell
def _(PALETTE, bar_chart, df_i14, plt):
    bar_chart(df_i14, "country", "revenue",
              "Top 15 Countries by Revenue",
              xlabel="Country", ylabel="Revenue ($)",
              color=PALETTE[4], figsize=(12, 5))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### I15 — Stock vs. Sales Comparison
    Are high-stock books selling, or just sitting on shelves?

    **Concept:** `COALESCE(x, default)` replaces `NULL` with a fallback value — here, `0` units sold for books that were never ordered, instead of a missing value.
    """)
    return


@app.cell
def _(books, mo, orders):
    df_i15 = mo.sql(
        f"""
        SELECT b.book_id,
               b.title,
               b.stock,
               COALESCE(SUM(o.quantity), 0) AS total_sold
        FROM   books b
        LEFT   JOIN orders o ON b.book_id = o.book_id
        GROUP  BY b.book_id, b.title, b.stock
        ORDER  BY b.stock DESC
        LIMIT  30;
        """
    )
    return (df_i15,)


@app.cell
def _(df_i15, plt, scatter_plot):
    scatter_plot(df_i15, "stock", "total_sold",
                 "Stock Level vs. Units Sold (Top 30 by Stock)",
                 xlabel="Stock on Hand", ylabel="Total Units Sold")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Advanced Queries

    `WITH` (Common Table Expressions) and **window functions** — tools
    that let a query "look sideways" at other rows without a self-join.
    A window function does not collapse rows the way `GROUP BY` does;
    each row keeps its own identity while also seeing a calculation
    across a group of related rows (its "window").
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### A1 — Year-over-Year Revenue Growth Rate
    What is the percentage change in revenue from one year to the next?

    **Concept:** `WITH yearly AS (...)` names a subquery so the main query can reuse it. `LAG(revenue) OVER (ORDER BY year)` looks at the *previous row's* revenue — comparing each year to the one before it, without a self-join.
    """)
    return


@app.cell
def _(mo, orders):
    df_a1 = mo.sql(
        f"""
        WITH yearly AS (
            SELECT EXTRACT(YEAR FROM order_date) AS year,
                   ROUND(SUM(total_amount), 2)   AS revenue
            FROM   orders
            GROUP  BY year
        )
        SELECT year,
               revenue,
               LAG(revenue) OVER (ORDER BY year) AS prev_year_rev,
               ROUND(
                   (revenue - LAG(revenue) OVER (ORDER BY year))
                   / LAG(revenue) OVER (ORDER BY year) * 100, 1
               ) AS yoy_growth_pct
        FROM   yearly
        ORDER  BY year;
        """
    )
    return (df_a1,)


@app.cell
def _(PALETTE, df_a1, plt):
    _fig, _ax1 = plt.subplots(figsize=(10, 5))
    _ax1.bar(df_a1["year"].astype(int).astype(str), df_a1["revenue"], color=PALETTE[0], alpha=0.7, label="Revenue")
    _ax1.set_ylabel("Revenue ($)", color=PALETTE[0])
    _ax1.set_xlabel("Year")
    _ax2 = _ax1.twinx()
    _growth = df_a1.dropna(subset=["yoy_growth_pct"])
    _ax2.plot(_growth["year"].astype(int).astype(str), _growth["yoy_growth_pct"],
             color=PALETTE[3], marker="s", linewidth=2, label="YoY Growth %")
    _ax2.set_ylabel("Growth %", color=PALETTE[3])
    _ax2.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    _ax1.set_title("Annual Revenue & Year-over-Year Growth")
    _lines1, _labels1 = _ax1.get_legend_handles_labels()
    _lines2, _labels2 = _ax2.get_legend_handles_labels()
    _ax1.legend(_lines1 + _lines2, _labels1 + _labels2, loc="upper left")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### A2 — Customer RFM Segmentation (Recency, Frequency, Monetary)
    Which customers are our best (and most at-risk) based on how recently, how often, and how much they buy?

    **Concept:** Two CTEs chained together: `rfm` computes three raw metrics per customer, then `scored` ranks each metric with `NTILE(5)`, which splits customers into 5 equal-sized buckets (quintiles) — a common way to score "best to worst" on a metric.
    """)
    return


@app.cell
def _(customers, mo, orders):
    df_a2 = mo.sql(
        f"""
        WITH rfm AS (
            SELECT c.customer_id,
                   c.name,
                   DATEDIFF('day', MAX(o.order_date),
                            (SELECT MAX(order_date) FROM orders)) AS recency,
                   COUNT(o.order_id)             AS frequency,
                   ROUND(SUM(o.total_amount), 2) AS monetary
            FROM   customers c
            JOIN   orders o ON c.customer_id = o.customer_id
            GROUP  BY c.customer_id, c.name
        ),
        scored AS (
            SELECT *,
                   NTILE(5) OVER (ORDER BY recency DESC) AS r_score,
                   NTILE(5) OVER (ORDER BY frequency)     AS f_score,
                   NTILE(5) OVER (ORDER BY monetary)      AS m_score
            FROM rfm
        )
        SELECT *,
               r_score + f_score + m_score AS rfm_total,
               CASE
                   WHEN r_score + f_score + m_score >= 13 THEN 'Champions'
                   WHEN r_score + f_score + m_score >= 10 THEN 'Loyal'
                   WHEN r_score + f_score + m_score >= 7  THEN 'At Risk'
                   ELSE 'Lost'
               END AS segment
        FROM scored
        ORDER BY rfm_total DESC;
        """
    )
    return (df_a2,)


@app.cell
def _(df_a2):
    df_a2_seg = df_a2["segment"].value_counts().reset_index()
    df_a2_seg.columns = ["segment", "count"]
    df_a2_seg
    return (df_a2_seg,)


@app.cell
def _(df_a2_seg, pie_chart, plt):
    pie_chart(df_a2_seg, "segment", "count",
              "Customer RFM Segments")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### A3 — Cumulative Revenue with Running Total
    How does daily revenue build up over the year, day by day?

    **Concept:** Adding `ORDER BY` inside `OVER()` turns `SUM()` into a **running total**: each row adds itself to the sum of every row before it, in date order.
    """)
    return


@app.cell
def _(mo, orders):
    df_a3 = mo.sql(
        f"""
        WITH daily AS (
            SELECT order_date,
                   ROUND(SUM(total_amount), 2) AS daily_rev
            FROM   orders
            WHERE  EXTRACT(YEAR FROM order_date) = 2025
            GROUP  BY order_date
        )
        SELECT order_date,
               daily_rev,
               ROUND(SUM(daily_rev) OVER (ORDER BY order_date), 2) AS cumulative_rev
        FROM   daily
        ORDER  BY order_date;
        """
    )
    return (df_a3,)


@app.cell
def _(PALETTE, df_a3, plt):
    _fig, _ax1 = plt.subplots(figsize=(14, 5))
    _ax1.fill_between(range(len(df_a3)), df_a3["cumulative_rev"], alpha=0.3, color=PALETTE[0])
    _ax1.plot(range(len(df_a3)), df_a3["cumulative_rev"], color=PALETTE[0], linewidth=1.5, label="Cumulative")
    _ax1.set_xlabel("Day of Year")
    _ax1.set_ylabel("Cumulative Revenue ($)")
    _ax1.set_title("2025 Cumulative Revenue Build-Up")
    _ax1.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### A4 — Genre Revenue Heatmap by Year and Genre
    How does each genre's revenue shift across years?

    **Concept:** SQL produces one row per year+genre combination — "long" data. `df.pivot()` reshapes it into a "wide" grid (years as columns, genres as rows) so a heatmap can color every genre x year cell at once.
    """)
    return


@app.cell
def _(books, mo, orders):
    df_a4 = mo.sql(
        f"""
        SELECT EXTRACT(YEAR FROM o.order_date) AS year,
               b.genre,
               ROUND(SUM(o.total_amount), 2)   AS revenue
        FROM   orders o
        JOIN   books b ON o.book_id = b.book_id
        GROUP  BY year, b.genre
        ORDER  BY year, b.genre;
        """
    )
    return (df_a4,)


@app.cell
def _(df_a4):
    df_a4_pivot = df_a4.pivot(index="genre", columns="year", values="revenue").fillna(0)
    df_a4_pivot.columns = df_a4_pivot.columns.astype(int).astype(str)
    df_a4_pivot
    return (df_a4_pivot,)


@app.cell
def _(df_a4_pivot, heatmap, plt):
    heatmap(df_a4_pivot, "Revenue Heatmap — Genre x Year",
            xlabel="Year", ylabel="Genre", fmt=",.0f",
            figsize=(10, 6))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### A5 — Pareto Analysis: Top 20% Customers Driving Revenue
    Do 20% of customers generate about 80% of revenue (the 80/20 rule)?

    **Concept:** `SUM(revenue) OVER ()` with **no** `ORDER BY` puts the grand total on every row. Dividing the running total (`SUM() OVER (ORDER BY ...)`) by that grand total gives each customer's cumulative share of all revenue.
    """)
    return


@app.cell
def _(mo, orders):
    df_a5 = mo.sql(
        f"""
        WITH cust_rev AS (
            SELECT customer_id,
                   ROUND(SUM(total_amount), 2) AS revenue
            FROM   orders
            GROUP  BY customer_id
        )
        SELECT customer_id,
               revenue,
               ROUND(SUM(revenue) OVER (ORDER BY revenue DESC), 2) AS cum_revenue,
               ROUND(SUM(revenue) OVER (), 2)                      AS grand_total,
               ROUND(SUM(revenue) OVER (ORDER BY revenue DESC)
                     / SUM(revenue) OVER () * 100, 2)              AS cum_pct,
               ROW_NUMBER() OVER (ORDER BY revenue DESC)           AS rank
        FROM   cust_rev
        ORDER  BY revenue DESC;
        """
    )
    return (df_a5,)


@app.cell
def _(df_a5, mo):
    _top_20_pct = int(len(df_a5) * 0.2)
    _rev_by_top20 = df_a5.head(_top_20_pct)["revenue"].sum()
    _grand_total = df_a5["revenue"].sum()
    mo.md(
        f"**Top 20%** of customers ({_top_20_pct} people) generate "
        rf"**\${_rev_by_top20:,.2f}** = "
        f"**{_rev_by_top20 / _grand_total * 100:.1f}%** of the grand total "
        rf"(\${_grand_total:,.2f})."
    )
    return


@app.cell
def _(PALETTE, df_a5, plt):
    _fig, _ax = plt.subplots(figsize=(12, 5))
    _ax.bar(range(len(df_a5)), df_a5["revenue"], color=PALETTE[0], alpha=0.5, width=1.0)
    _ax2 = _ax.twinx()
    _ax2.plot(range(len(df_a5)), df_a5["cum_pct"], color=PALETTE[3], linewidth=2)
    _ax2.axhline(80, color="red", linestyle="--", linewidth=1, label="80% line")
    _ax2.axvline(int(len(df_a5) * 0.2), color="green", linestyle="--", linewidth=1, label="20% of customers")
    _ax.set_xlabel("Customers (ranked by revenue)")
    _ax.set_ylabel("Individual Revenue ($)")
    _ax2.set_ylabel("Cumulative Revenue %")
    _ax.set_title("Pareto Analysis — Customer Revenue Concentration")
    _ax2.legend(loc="center right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### A6 — Customers Who Have Never Purchased Any Books
    Which customers are prospects for a re-engagement campaign?

    **Concept:** The anti-join pattern from I8, applied to `customers` instead of `books`: `LEFT JOIN` + `WHERE order_id IS NULL` finds customers with zero matching orders.
    """)
    return


@app.cell
def _(customers, mo, orders):
    df_a6 = mo.sql(
        f"""
        SELECT c.customer_id,
               c.name,
               c.email,
               c.city,
               c.country
        FROM   customers c
        LEFT   JOIN orders o ON c.customer_id = o.customer_id
        WHERE  o.order_id IS NULL
        ORDER  BY c.customer_id;
        """
    )
    return (df_a6,)


@app.cell
def _(df_a6, df_totals, mo):
    mo.md(f"""
    **{len(df_a6)}** of **{int(df_totals['total_customers'][0])}** "
        f"customers have never placed an order — "
        f"potential targets for a re-engagement campaign.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### A7 — Books That No One Has Ordered
    Which titles might need promotion, a discount, or removal from inventory?

    **Concept:** The same anti-join pattern once more, this time sorted by price so the most expensive unsold titles surface first.
    """)
    return


@app.cell
def _(books, mo, orders):
    df_a7 = mo.sql(
        f"""
        SELECT b.book_id,
               b.title,
               b.author,
               b.genre,
               b.published_year,
               b.price,
               b.stock
        FROM   books b
        LEFT   JOIN orders o ON b.book_id = o.book_id
        WHERE  o.order_id IS NULL
        ORDER  BY b.price DESC;
        """
    )
    return (df_a7,)


@app.cell
def _(df_a7, df_totals, mo):
    mo.md(f"""
    **{len(df_a7)}** of **{int(df_totals['total_books'][0])}** "
        f"books have zero sales — candidates for a discount, a "
        f"promotion, or dropping from inventory.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Next Steps

    You have now practiced the full range of SQL you need for OMIS 105:
    filtering and sorting, aggregation, joins (including anti-joins),
    subqueries, CTEs, and window functions.

    Try this:

    1. Pick one query above and change a column, a filter, or a `LIMIT`
       — see how the result and the chart react.
    2. Write a brand-new query that answers a question *you* have about
       this bookstore (e.g., "which genre has the most expensive average
       book?").
    3. Compare your answer to `bookstore_queries.sql` and
       `bookstore_analytics.ipynb` — the same 27 questions, written as
       plain SQL and as a Jupyter notebook.

    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
