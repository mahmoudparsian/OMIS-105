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
    # Lab 10: Comprehensive Review & Practice Exam

    ## OMIS 105 — Database Management Systems
    **Week 10 | Estimated time: 90 minutes**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Connect to DuckDB and load `categories`, `products`, `customers`,
    `orders`, `order_items`, `reviews`, `suppliers`, `product_suppliers`,
    and `shipping` from `./data/`.
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
        "CREATE OR REPLACE TABLE categories AS SELECT * FROM read_csv_auto('./data/categories.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE products AS SELECT * FROM read_csv_auto('./data/products.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv_auto('./data/customers.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE orders AS SELECT * FROM read_csv_auto('./data/orders.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE order_items AS SELECT * FROM read_csv_auto('./data/order_items.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE reviews AS SELECT * FROM read_csv_auto('./data/reviews.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE suppliers AS SELECT * FROM read_csv_auto('./data/suppliers.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE product_suppliers AS SELECT * FROM read_csv_auto('./data/product_suppliers.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE shipping AS SELECT * FROM read_csv_auto('./data/shipping.csv')"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Conceptual Questions (20 points)

    Answer these in your own words (2–3 sentences each).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** What is the difference between a primary key and a foreign
    key? Give an example from ShopSmart.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** Explain the difference between WHERE and HAVING. When would
    you use each?

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** What is a transitive dependency? Give an example and explain
    how to fix it.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** Explain the difference between INNER JOIN and LEFT JOIN.
    When would you choose LEFT JOIN?

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** What does Atomicity mean in the context of ACID? Why is it
    important for an e-commerce system?

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Schema Design (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6.** Given the following requirements for a **Movie Theater**
    database:
    - Movies have a title, genre, duration, and rating (G/PG/PG-13/R)
    - Theaters have multiple screens, each with a capacity
    - Showtimes link a movie to a screen at a specific date/time
    - Customers can purchase tickets for specific showtimes
    - Each ticket has a seat number and price

    a) List all functional dependencies.
    b) Write CREATE TABLE statements for all tables (minimum 5).
    c) Identify all relationships and their cardinality.

    *(List your FDs and relationships here. Name your customer table
    something other than `customers` — that name is already taken by
    the ShopSmart table loaded above.)*
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your CREATE TABLE statements
    con.execute(
        """
        -- Your CREATE TABLE statements here
        SELECT 'Q6: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: SQL Queries on ShopSmart (30 points)

    Write SQL queries for each of the following. Include comments
    explaining your approach.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** Find the top 3 customers by total spending. Show their full
    name, number of orders, total spent, and average order value.
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
    **Q8.** For each category, find the product with the highest number
    of reviews. Show category_name, product_name, and review_count.
    (Use a window function.)
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
    **Q9.** Calculate the month-over-month revenue growth rate for 2024.
    Show month, revenue, previous month's revenue, and growth
    percentage. (Use LAG.)
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
    **Q10.** Find customers who have ordered products from at least 4
    different categories. Show their name and the number of distinct
    categories.
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
    **Q11.** Using a CTE, create a "supplier performance" report that
    shows each supplier's name, number of products they supply, the
    average cost price, and the average retail margin (retail price -
    cost price).
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
    **Q12.** Find the average shipping time (days between order_date and
    delivery_date) by carrier. Only include completed orders with a
    delivery date. Rank carriers by speed.
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
    ---
    ## Part 4: Normalization (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q13.** The following denormalized table tracks employee training:

    ```
    training_log(
        employee_id, employee_name, department, dept_manager,
        course_id, course_title, instructor_name, instructor_email,
        completion_date, score, certificate_id
    )
    ```

    a) Identify all functional dependencies.
    b) What is the candidate key?
    c) Is this in 1NF? 2NF? 3NF? Explain.
    d) Decompose into 3NF. Write CREATE TABLE statements.

    *(Write your FDs, candidate key, and normal-form analysis here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your 3NF CREATE TABLE statements
    con.execute(
        """
        -- Your CREATE TABLE statements here
        SELECT 'Q13: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Transaction Design (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q14.** Write a Python function `process_return(con, order_id)`
    that handles a product return:
    1. Verify the order exists and status is 'completed'
    2. Change order status to 'cancelled' (the `orders.status` CHECK
       constraint only allows 'processing', 'shipped', 'completed', or
       'cancelled')
    3. Restore stock for each item in the order
    4. Calculate the refund amount
    5. Handle errors with ROLLBACK

    Test with both a valid and invalid order_id.
    """)
    return


@app.cell
def _(con):
    # TODO: define process_return(con, order_id)
    print("Q14: define your process_return() function here")
    return


@app.cell
def _(con):
    # TODO: test process_return() with a valid and an invalid order_id
    print("Q14: call process_return() with your test cases here")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 6: Performance & Design (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q15.** Given that ShopSmart runs these queries thousands of times
    per day:

    ```sql
    A: SELECT * FROM orders WHERE customer_id = ? AND order_date > ?
    B: SELECT * FROM products WHERE category_id = ? AND price < ?
    C: SELECT * FROM reviews WHERE product_id = ? ORDER BY review_date DESC LIMIT 5
    ```

    a) What indexes would you create? Explain each choice.
    b) Would you create a view for any of these? Why or why not?
    c) Are there any queries where an index would NOT help? Explain.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Submission

    - Submit notebook with all answers, queries, and outputs
    - **Total: 100 points** (this lab counts as your review/practice exam)
    """)
    return


if __name__ == "__main__":
    app.run()
