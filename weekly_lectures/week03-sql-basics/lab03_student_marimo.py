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
    # Lab 3: SQL Functions, GROUP BY, and Subqueries

    ## OMIS 105 — Database Management Systems
    **Week 3 | Estimated time: 75–90 minutes**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Connect to DuckDB and load `products`, `customers`, `categories`, and
    `orders` from `./data/`.

    > **Note**: `products` has a `category_id` column (not a `category`
    text column) — to show a readable category name, join `products` to
    `categories` on `category_id`, the same comma-join style you used in
    Week 2 Q6.
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell
def _(con):
    con.execute(
        "CREATE OR REPLACE TABLE products AS SELECT * FROM read_csv_auto('./data/products.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv_auto('./data/customers.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE categories AS SELECT * FROM read_csv_auto('./data/categories.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE orders AS SELECT * FROM read_csv_auto('./data/orders.csv')"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: String Functions (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** Display each customer's full name (first + last) in uppercase,
    along with the length of their email address. Sort by email length
    descending.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q1
    con.execute(
        """
        -- Your query here
        SELECT 'Q1: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** Find all products whose name contains "Set" or "Kit"
    (case-insensitive). Show product_name and category.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q2
    con.execute(
        """
        -- Your query here
        SELECT 'Q2: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** Create a column `email_domain` that extracts just the domain
    from each customer's email (the part after @). Show first_name, email,
    and email_domain.

    *Hint: Look up `SPLIT_PART` or use `SUBSTRING` with `POSITION`.*
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q3
    con.execute(
        """
        -- Your query here
        SELECT 'Q3: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Date Functions (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** How many orders were placed in each month of 2024? Show year,
    month, and count. Sort by month.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q4
    con.execute(
        """
        -- Your query here
        SELECT 'Q4: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** For each customer, calculate how many days they have been a
    member (from `join_date` to today). Show first_name, join_date, and
    days_as_member. Sort by most senior first.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q5
    con.execute(
        """
        -- Your query here
        SELECT 'Q5: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: CASE Expressions (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6.** Classify each product into a price tier:
    - Under $15 → "Economy"
    - $15 to $49.99 → "Standard"
    - $50 to $149.99 → "Premium"
    - $150 and above → "Luxury"

    Show product_name, price, and price_tier. Count how many products fall
    into each tier.
    """)
    return


@app.cell
def _(con):
    # TODO: Query 1 — replace to show each product with its tier
    con.execute(
        """
        -- Your query here
        SELECT 'Q6 (part 1): replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    # TODO: Query 2 — replace to count products per tier
    con.execute(
        """
        -- Your query here
        SELECT 'Q6 (part 2): replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** Create an `order_size` classification based on total_amount:
    - Under $50 → "Small"
    - $50 to $199.99 → "Medium"
    - $200 to $499.99 → "Large"
    - $500+ → "Extra Large"

    Show the count, total revenue, and average order value for each size
    category.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q7
    con.execute(
        """
        -- Your query here
        SELECT 'Q7: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: GROUP BY and HAVING (20 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8.** For each category, compute: number of products, average price,
    total stock value (sum of price × stock_quantity). Sort by total stock
    value descending.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q8
    con.execute(
        """
        -- Your query here
        SELECT 'Q8: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9.** Which categories have more than 5 products with stock above
    100? Show category and count.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q9
    con.execute(
        """
        -- Your query here
        SELECT 'Q9: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** Find the number of orders per customer. Show customer_id and
    order_count. Only include customers with 3 or more orders.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q10
    con.execute(
        """
        -- Your query here
        SELECT 'Q10: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q11.** What is the average order value per month in 2024? Only show
    months with average order value above $200.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q11
    con.execute(
        """
        -- Your query here
        SELECT 'Q11: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Subqueries (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** List all products that are priced higher than the average
    price in their own category.

    *Hint: Use a correlated subquery.*
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q12
    con.execute(
        """
        -- Your query here
        SELECT 'Q12: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q13.** Find the top-spending customer (highest total across all
    orders). Show their name and total spent.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q13
    con.execute(
        """
        -- Your query here
        SELECT 'Q13: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q14.** Find all categories where every product has stock_quantity > 0
    (i.e., no out-of-stock products).
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q14
    con.execute(
        """
        -- Your query here
        SELECT 'Q14: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 6: Comprehensive Query (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q15.** Create a "Product Dashboard" query that shows for each
    category:
    - Category name
    - Number of products
    - Average price (rounded to 2 decimals)
    - Cheapest and most expensive product prices
    - Count of in-stock vs out-of-stock items
    - Whether the category average is above or below the overall average
      ("Above" / "Below")

    Sort by average price descending.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q15
    con.execute(
        """
        -- Your query here
        SELECT 'Q15: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Submission

    - Submit notebook with all queries and outputs
    - **Total: 75 points**
    """)
    return


if __name__ == "__main__":
    app.run()
