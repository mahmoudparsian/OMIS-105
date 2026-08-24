import json, textwrap

def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.split("\n")}

def code(source):
    return {"cell_type": "code", "metadata": {}, "source": source.split("\n"),
            "execution_count": None, "outputs": []}

cells = []

# ══════════════════════════════════════════════════════════════════════
# TITLE
# ══════════════════════════════════════════════════════════════════════
cells.append(md("""# Bookstore Analytics — DuckDB Portfolio Project

This notebook connects to `bookstore.duckdb` and runs **25 analytical queries** across three complexity tiers:

| Tier | Count |
|------|-------|
| Basic | 5 |
| Intermediate | 15 |
| Advanced | 5 |

Each cell includes: **what we are doing**, the **SQL query**, the **result**, and a **plot** when applicable.

> Plotting code is decoupled into `plot_helpers.py`."""))

# ══════════════════════════════════════════════════════════════════════
# SETUP
# ══════════════════════════════════════════════════════════════════════
cells.append(md("## Setup"))

cells.append(code("""import duckdb
import pandas as pd
import matplotlib.pyplot as plt
from plot_helpers import (
    bar_chart, pie_chart, line_chart, grouped_bar_chart,
    stacked_bar_chart, histogram, scatter_plot, heatmap, multi_line_chart,
    PALETTE
)
%matplotlib inline

con = duckdb.connect("bookstore.duckdb", read_only=True)

# Quick sanity check
for t in ["books", "customers", "orders"]:
    n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t:>12s}: {n:>7,} rows")"""))

# ══════════════════════════════════════════════════════════════════════
# BASIC (5)
# ══════════════════════════════════════════════════════════════════════
cells.append(md("---\n## Basic Queries"))

# B1
cells.append(md("### B1 — Count of Books by Genre\nHow many books do we carry in each genre?"))
cells.append(code("""sql = \"\"\"
SELECT genre,
       COUNT(*) AS book_count
FROM   books
GROUP  BY genre
ORDER  BY book_count DESC;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""bar_chart(df, "genre", "book_count",
          "Number of Books per Genre",
          xlabel="Genre", ylabel="Books")
plt.show()"""))

# B2
cells.append(md("### B2 — Average Book Price\nWhat is the overall average price of books in the store?"))
cells.append(code("""sql = \"\"\"
SELECT ROUND(AVG(price), 2) AS avg_price,
       ROUND(MIN(price), 2) AS min_price,
       ROUND(MAX(price), 2) AS max_price
FROM   books;
\"\"\"
df = con.execute(sql).df()
df"""))

# B3
cells.append(md("### B3 — Top 10 Most Recently Published Books\nWhich 10 books were published most recently?"))
cells.append(code("""sql = \"\"\"
SELECT title, author, genre, published_year, price
FROM   books
ORDER  BY published_year DESC
LIMIT  10;
\"\"\"
df = con.execute(sql).df()
df"""))

# B4
cells.append(md("### B4 — Customers per Country (Top 15)\nWhich countries have the most customers?"))
cells.append(code("""sql = \"\"\"
SELECT country,
       COUNT(*) AS total_customers
FROM   customers
GROUP  BY country
ORDER  BY total_customers DESC
LIMIT  15;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""bar_chart(df, "country", "total_customers",
          "Top 15 Countries by Customer Count",
          xlabel="Country", ylabel="Customers",
          color=PALETTE[1])
plt.show()"""))

# B5
cells.append(md("### B5 — Total Revenue\nWhat is the total revenue generated from all orders?"))
cells.append(code("""sql = \"\"\"
SELECT ROUND(SUM(total_amount), 2)  AS total_revenue,
       COUNT(*)                      AS total_orders,
       ROUND(AVG(total_amount), 2)  AS avg_order_value
FROM   orders;
\"\"\"
df = con.execute(sql).df()
df"""))

# ══════════════════════════════════════════════════════════════════════
# INTERMEDIATE (15)
# ══════════════════════════════════════════════════════════════════════
cells.append(md("---\n## Intermediate Queries"))

# I1
cells.append(md("### I1 — Monthly Revenue Trend\nHow does revenue change month over month?"))
cells.append(code("""sql = \"\"\"
SELECT STRFTIME(order_date, '%Y-%m') AS month,
       ROUND(SUM(total_amount), 2)   AS revenue,
       COUNT(*)                       AS orders
FROM   orders
GROUP  BY month
ORDER  BY month;
\"\"\"
df = con.execute(sql).df()
df.tail(12)"""))
cells.append(code("""line_chart(df, "month", "revenue",
           "Monthly Revenue Trend",
           xlabel="Month", ylabel="Revenue ($)")
plt.show()"""))

# I2
cells.append(md("### I2 — Revenue by Genre\nWhich genres generate the most revenue?"))
cells.append(code("""sql = \"\"\"
SELECT b.genre,
       ROUND(SUM(o.total_amount), 2) AS revenue,
       SUM(o.quantity)                AS units_sold
FROM   orders o
JOIN   books b ON o.book_id = b.book_id
GROUP  BY b.genre
ORDER  BY revenue DESC;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""pie_chart(df, "genre", "revenue",
          "Revenue Share by Genre")
plt.show()"""))

# I3
cells.append(md("### I3 — Top 10 Best-Selling Books (by Quantity)\nWhich individual titles sold the most copies?"))
cells.append(code("""sql = \"\"\"
SELECT b.title,
       b.author,
       SUM(o.quantity)                AS total_qty,
       ROUND(SUM(o.total_amount), 2) AS total_rev
FROM   orders o
JOIN   books b ON o.book_id = b.book_id
GROUP  BY b.title, b.author
ORDER  BY total_qty DESC
LIMIT  10;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""bar_chart(df, "title", "total_qty",
          "Top 10 Best-Selling Books by Quantity",
          xlabel="Book Title", ylabel="Units Sold",
          color=PALETTE[2], figsize=(12, 5))
plt.show()"""))

# I4
cells.append(md("### I4 — Top 10 Customers by Total Spend\nWho are our highest-value customers?"))
cells.append(code("""sql = \"\"\"
SELECT c.customer_id,
       c.name,
       c.country,
       COUNT(o.order_id)              AS order_count,
       ROUND(SUM(o.total_amount), 2) AS total_spent
FROM   orders o
JOIN   customers c ON o.customer_id = c.customer_id
GROUP  BY c.customer_id, c.name, c.country
ORDER  BY total_spent DESC
LIMIT  10;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""bar_chart(df, "name", "total_spent",
          "Top 10 Customers by Total Spend",
          xlabel="Customer", ylabel="Total Spent ($)",
          horizontal=True, color=PALETTE[3])
plt.show()"""))

# I5
cells.append(md("### I5 — Year-over-Year Revenue\nHow does annual revenue compare across years?"))
cells.append(code("""sql = \"\"\"
SELECT EXTRACT(YEAR FROM order_date) AS year,
       ROUND(SUM(total_amount), 2)   AS revenue,
       COUNT(*)                       AS orders,
       ROUND(AVG(total_amount), 2)   AS avg_order
FROM   orders
GROUP  BY year
ORDER  BY year;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""bar_chart(df, "year", "revenue",
          "Annual Revenue",
          xlabel="Year", ylabel="Revenue ($)",
          color=PALETTE[4])
plt.show()"""))

# I6
cells.append(md("### I6 — Orders per Day of Week\nAre there patterns in which day orders are placed?"))
cells.append(code("""sql = \"\"\"
SELECT DAYNAME(order_date)  AS day_name,
       DAYOFWEEK(order_date) AS day_num,
       COUNT(*)              AS orders
FROM   orders
GROUP  BY day_name, day_num
ORDER  BY day_num;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""bar_chart(df, "day_name", "orders",
          "Orders by Day of Week",
          xlabel="Day", ylabel="Number of Orders",
          color=PALETTE[5])
plt.show()"""))

# I7
cells.append(md("### I7 — Average Order Value by Genre\nWhich genres command higher order values?"))
cells.append(code("""sql = \"\"\"
SELECT b.genre,
       ROUND(AVG(o.total_amount), 2) AS avg_order_value,
       ROUND(AVG(o.quantity), 1)     AS avg_qty
FROM   orders o
JOIN   books b ON o.book_id = b.book_id
GROUP  BY b.genre
ORDER  BY avg_order_value DESC;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""bar_chart(df, "genre", "avg_order_value",
          "Average Order Value by Genre",
          xlabel="Genre", ylabel="Avg Order Value ($)",
          color=PALETTE[6])
plt.show()"""))

# I8
cells.append(md("### I8 — Books That Have Never Been Ordered\nAre there books sitting unsold in inventory?"))
cells.append(code("""sql = \"\"\"
SELECT b.book_id, b.title, b.author, b.genre, b.price, b.stock
FROM   books b
LEFT   JOIN orders o ON b.book_id = o.book_id
WHERE  o.order_id IS NULL
ORDER  BY b.stock DESC;
\"\"\"
df = con.execute(sql).df()
print(f"Books never ordered: {len(df)}")
df.head(10)"""))

# I9
cells.append(md("### I9 — Customer Order Frequency Distribution\nHow many orders do most customers place?"))
cells.append(code("""sql = \"\"\"
SELECT order_count, COUNT(*) AS num_customers
FROM (
    SELECT customer_id, COUNT(*) AS order_count
    FROM   orders
    GROUP  BY customer_id
)
GROUP BY order_count
ORDER BY order_count;
\"\"\"
df = con.execute(sql).df()
df.head(15)"""))
cells.append(code("""bar_chart(df.head(25), "order_count", "num_customers",
          "Customer Order Frequency Distribution",
          xlabel="Number of Orders", ylabel="Number of Customers",
          color=PALETTE[0])
plt.show()"""))

# I10
cells.append(md("### I10 — Quarterly Revenue by Year\nRevenue broken down by quarter and year."))
cells.append(code("""sql = \"\"\"
SELECT EXTRACT(YEAR FROM order_date)    AS year,
       EXTRACT(QUARTER FROM order_date) AS quarter,
       ROUND(SUM(total_amount), 2)      AS revenue
FROM   orders
GROUP  BY year, quarter
ORDER  BY year, quarter;
\"\"\"
df = con.execute(sql).df()
df["label"] = df["year"].astype(int).astype(str) + "-Q" + df["quarter"].astype(int).astype(str)
df"""))
cells.append(code("""bar_chart(df, "label", "revenue",
          "Quarterly Revenue",
          xlabel="Quarter", ylabel="Revenue ($)",
          color=PALETTE[2], figsize=(14, 5))
plt.show()"""))

# I11
cells.append(md("### I11 — Price Distribution of Books\nWhat does the distribution of book prices look like?"))
cells.append(code("""sql = \"\"\"
SELECT price FROM books;
\"\"\"
df = con.execute(sql).df()
df.describe()"""))
cells.append(code("""histogram(df["price"], bins=25,
           title="Distribution of Book Prices",
           xlabel="Price ($)", ylabel="Number of Books")
plt.show()"""))

# I12
cells.append(md("### I12 — Top 10 Authors by Revenue\nWhich authors bring in the most money?"))
cells.append(code("""sql = \"\"\"
SELECT b.author,
       COUNT(DISTINCT b.book_id)      AS books_in_store,
       SUM(o.quantity)                AS units_sold,
       ROUND(SUM(o.total_amount), 2) AS total_revenue
FROM   orders o
JOIN   books b ON o.book_id = b.book_id
GROUP  BY b.author
ORDER  BY total_revenue DESC
LIMIT  10;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""bar_chart(df, "author", "total_revenue",
          "Top 10 Authors by Revenue",
          xlabel="Author", ylabel="Revenue ($)",
          horizontal=True, color=PALETTE[1], figsize=(12, 6))
plt.show()"""))

# I13
cells.append(md("### I13 — November & December Sales Spike\nDo holiday months really outperform the rest?"))
cells.append(code("""sql = \"\"\"
SELECT EXTRACT(MONTH FROM order_date) AS month_num,
       MONTHNAME(order_date)          AS month_name,
       COUNT(*)                       AS orders,
       ROUND(SUM(total_amount), 2)   AS revenue
FROM   orders
GROUP  BY month_num, month_name
ORDER  BY month_num;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.bar(df["month_name"], df["revenue"], color=PALETTE[0], alpha=0.7, label="Revenue")
ax1.set_ylabel("Revenue ($)", color=PALETTE[0])
ax1.set_xlabel("Month")
ax2 = ax1.twinx()
ax2.plot(df["month_name"], df["orders"], color=PALETTE[3], marker="o", linewidth=2, label="Orders")
ax2.set_ylabel("Order Count", color=PALETTE[3])
ax1.set_title("Monthly Revenue & Order Count")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()"""))

# I14
cells.append(md("### I14 — Revenue by Country (Top 15)\nWhich countries generate the most bookstore revenue?"))
cells.append(code("""sql = \"\"\"
SELECT c.country,
       COUNT(DISTINCT c.customer_id)  AS customers,
       ROUND(SUM(o.total_amount), 2) AS revenue
FROM   orders o
JOIN   customers c ON o.customer_id = c.customer_id
GROUP  BY c.country
ORDER  BY revenue DESC
LIMIT  15;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""bar_chart(df, "country", "revenue",
          "Top 15 Countries by Revenue",
          xlabel="Country", ylabel="Revenue ($)",
          color=PALETTE[4], figsize=(12, 5))
plt.show()"""))

# I15
cells.append(md("### I15 — Stock vs. Sales Comparison\nAre high-stock books selling, or just sitting on shelves?"))
cells.append(code("""sql = \"\"\"
SELECT b.book_id,
       b.title,
       b.stock,
       COALESCE(SUM(o.quantity), 0) AS total_sold
FROM   books b
LEFT   JOIN orders o ON b.book_id = o.book_id
GROUP  BY b.book_id, b.title, b.stock
ORDER  BY b.stock DESC
LIMIT  30;
\"\"\"
df = con.execute(sql).df()
df.head(10)"""))
cells.append(code("""scatter_plot(df, "stock", "total_sold",
             "Stock Level vs. Units Sold (Top 30 by Stock)",
             xlabel="Stock on Hand", ylabel="Total Units Sold")
plt.show()"""))

# ══════════════════════════════════════════════════════════════════════
# ADVANCED (5)
# ══════════════════════════════════════════════════════════════════════
cells.append(md("---\n## Advanced Queries"))

# A1
cells.append(md("""### A1 — Year-over-Year Revenue Growth Rate
Calculate the percentage change in revenue from one year to the next using a window function."""))
cells.append(code("""sql = \"\"\"
WITH yearly AS (
    SELECT EXTRACT(YEAR FROM order_date)  AS year,
           ROUND(SUM(total_amount), 2)    AS revenue
    FROM   orders
    GROUP  BY year
)
SELECT year,
       revenue,
       LAG(revenue) OVER (ORDER BY year)                         AS prev_year_rev,
       ROUND(
           (revenue - LAG(revenue) OVER (ORDER BY year))
           / LAG(revenue) OVER (ORDER BY year) * 100, 1
       )                                                          AS yoy_growth_pct
FROM   yearly
ORDER  BY year;
\"\"\"
df = con.execute(sql).df()
df"""))
cells.append(code("""fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(df["year"].astype(int).astype(str), df["revenue"], color=PALETTE[0], alpha=0.7, label="Revenue")
ax1.set_ylabel("Revenue ($)", color=PALETTE[0])
ax1.set_xlabel("Year")
ax2 = ax1.twinx()
growth = df.dropna(subset=["yoy_growth_pct"])
ax2.plot(growth["year"].astype(int).astype(str), growth["yoy_growth_pct"],
         color=PALETTE[3], marker="s", linewidth=2, label="YoY Growth %")
ax2.set_ylabel("Growth %", color=PALETTE[3])
ax2.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax1.set_title("Annual Revenue & Year-over-Year Growth")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
plt.tight_layout()
plt.show()"""))

# A2
cells.append(md("""### A2 — Customer RFM Segmentation (Recency, Frequency, Monetary)
Classify customers into segments using quintile-based RFM scoring."""))
cells.append(code("""sql = \"\"\"
WITH rfm AS (
    SELECT c.customer_id,
           c.name,
           DATEDIFF('day', MAX(o.order_date), (SELECT MAX(order_date) FROM orders)) AS recency,
           COUNT(o.order_id)              AS frequency,
           ROUND(SUM(o.total_amount), 2) AS monetary
    FROM   customers c
    JOIN   orders o ON c.customer_id = o.customer_id
    GROUP  BY c.customer_id, c.name
),
scored AS (
    SELECT *,
           NTILE(5) OVER (ORDER BY recency DESC)  AS r_score,
           NTILE(5) OVER (ORDER BY frequency)      AS f_score,
           NTILE(5) OVER (ORDER BY monetary)       AS m_score
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
\"\"\"
df = con.execute(sql).df()
print(f"Total customers scored: {len(df)}")
df.head(10)"""))
cells.append(code("""seg = df["segment"].value_counts().reset_index()
seg.columns = ["segment", "count"]
pie_chart(seg, "segment", "count",
          "Customer RFM Segments")
plt.show()"""))

# A3
cells.append(md("""### A3 — Cumulative Revenue with Running Total
Show daily revenue alongside a running cumulative total using window functions."""))
cells.append(code("""sql = \"\"\"
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
\"\"\"
df = con.execute(sql).df()
print(f"Days in 2025 with orders: {len(df)}")
df.tail(10)"""))
cells.append(code("""fig, ax1 = plt.subplots(figsize=(14, 5))
ax1.fill_between(range(len(df)), df["cumulative_rev"], alpha=0.3, color=PALETTE[0])
ax1.plot(range(len(df)), df["cumulative_rev"], color=PALETTE[0], linewidth=1.5, label="Cumulative")
ax1.set_xlabel("Day of Year")
ax1.set_ylabel("Cumulative Revenue ($)")
ax1.set_title("2025 Cumulative Revenue Build-Up")
ax1.legend()
plt.tight_layout()
plt.show()"""))

# A4
cells.append(md("""### A4 — Genre Revenue Heatmap by Year and Genre
Pivot revenue data into a year x genre matrix and visualize as a heatmap."""))
cells.append(code("""sql = \"\"\"
SELECT EXTRACT(YEAR FROM o.order_date) AS year,
       b.genre,
       ROUND(SUM(o.total_amount), 2)  AS revenue
FROM   orders o
JOIN   books b ON o.book_id = b.book_id
GROUP  BY year, b.genre
ORDER  BY year, b.genre;
\"\"\"
df = con.execute(sql).df()
pivot = df.pivot(index="genre", columns="year", values="revenue").fillna(0)
pivot.columns = pivot.columns.astype(int).astype(str)
pivot"""))
cells.append(code("""heatmap(pivot,
        "Revenue Heatmap — Genre x Year",
        xlabel="Year", ylabel="Genre", fmt=",.0f",
        figsize=(10, 6))
plt.show()"""))

# A5
cells.append(md("""### A5 — Pareto Analysis: Top 20% Customers Driving Revenue
Verify the 80/20 rule — do 20% of customers generate ~80% of revenue?"""))
cells.append(code("""sql = \"\"\"
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
       ROW_NUMBER() OVER (ORDER BY revenue DESC)            AS rank
FROM   cust_rev
ORDER  BY revenue DESC;
\"\"\"
df = con.execute(sql).df()
top_20_pct = int(len(df) * 0.2)
rev_by_top20 = df.head(top_20_pct)["revenue"].sum()
total = df["revenue"].sum()
print(f"Total customers: {len(df)}")
print(f"Top 20% ({top_20_pct} customers) generate ${rev_by_top20:,.2f} "
      f"= {rev_by_top20/total*100:.1f}% of total ${total:,.2f}")
df.head(10)"""))
cells.append(code("""fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(range(len(df)), df["revenue"], color=PALETTE[0], alpha=0.5, width=1.0)
ax2 = ax.twinx()
ax2.plot(range(len(df)), df["cum_pct"], color=PALETTE[3], linewidth=2)
ax2.axhline(80, color="red", linestyle="--", linewidth=1, label="80% line")
ax2.axvline(int(len(df)*0.2), color="green", linestyle="--", linewidth=1, label="20% of customers")
ax.set_xlabel("Customers (ranked by revenue)")
ax.set_ylabel("Individual Revenue ($)")
ax2.set_ylabel("Cumulative Revenue %")
ax.set_title("Pareto Analysis — Customer Revenue Concentration")
ax2.legend(loc="center right")
plt.tight_layout()
plt.show()"""))

# ══════════════════════════════════════════════════════════════════════
# CLOSE
# ══════════════════════════════════════════════════════════════════════
cells.append(md("---\n## Cleanup"))
cells.append(code("""con.close()
print("Connection closed.")"""))

# ── Build notebook JSON ──────────────────────────────────────────────
nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0"
        }
    },
    "cells": cells
}

# Fix: split source lines properly with newlines
for cell in nb["cells"]:
    src = cell["source"]
    if isinstance(src, list) and len(src) == 1:
        # re-split single string
        cell["source"] = [line + "\n" for line in src[0].split("\n")]
        # Remove trailing \n from last line
        if cell["source"]:
            cell["source"][-1] = cell["source"][-1].rstrip("\n")
    else:
        cell["source"] = [line + "\n" for line in src]
        if cell["source"]:
            cell["source"][-1] = cell["source"][-1].rstrip("\n")

path = "/sessions/wonderful-blissful-gauss/mnt/duckdb_book_store/bookstore_analytics.ipynb"
with open(path, "w") as f:
    json.dump(nb, f, indent=1)

print(f"Notebook written to {path}")
print(f"Total cells: {len(cells)}")
