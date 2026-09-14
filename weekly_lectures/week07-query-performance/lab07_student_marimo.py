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
    # Lab 7: Performance & Indexing

    ## OMIS 105 — Database Management Systems
    **Week 7 | Estimated time: 75–90 minutes**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Connect to DuckDB and load `categories`, `products`, `customers`,
    `orders`, `order_items`, `reviews`, `shipping`, `suppliers`, and
    `product_suppliers` from `./data/`.
    """)
    return


@app.cell
def _():
    import duckdb
    import time
    con = duckdb.connect(database=":memory:")
    return con, time


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
        "CREATE OR REPLACE TABLE shipping AS SELECT * FROM read_csv_auto('./data/shipping.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE suppliers AS SELECT * FROM read_csv_auto('./data/suppliers.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE product_suppliers AS SELECT * FROM read_csv_auto('./data/product_suppliers.csv')"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Understanding Query Plans (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** Run `EXPLAIN` on the following query and describe what you
    see. What operations does DuckDB use?

    ```sql
    EXPLAIN
    SELECT product_name, price FROM products WHERE price > 100;
    ```

    *(Write your description here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: run the EXPLAIN query above
    con.execute(
        "EXPLAIN SELECT product_name, price FROM products WHERE price > 100"
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** Run `EXPLAIN` on a JOIN query. Identify the join algorithm
    DuckDB chooses.

    ```sql
    EXPLAIN
    SELECT c.first_name, o.order_id, o.total_amount
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.total_amount > 300;
    ```

    *(Write your answer here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: run the EXPLAIN query above
    con.execute(
        """
        EXPLAIN
        SELECT c.first_name, o.order_id, o.total_amount
        FROM customers c
        INNER JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.total_amount > 300
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** Run `EXPLAIN` on a query with GROUP BY. What additional
    operations appear?

    ```sql
    EXPLAIN
    SELECT category_id, COUNT(*), AVG(price)
    FROM products
    GROUP BY category_id;
    ```

    *(Write your answer here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: run the EXPLAIN query above
    con.execute(
        """
        EXPLAIN
        SELECT category_id, COUNT(*), AVG(price)
        FROM products
        GROUP BY category_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Creating and Using Indexes (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** Create an index on `orders(status)`. Then run EXPLAIN on a
    query filtering by status. Does the plan change?

    *(Write your answer here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: create the index, then EXPLAIN
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
    **Q5.** Create a composite index on `orders(customer_id, order_date)`.
    Write a query that would benefit from this index and run EXPLAIN.
    """)
    return


@app.cell
def _(con):
    # TODO: your index + query + EXPLAIN
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
    **Q6.** List all indexes you have created using
    `SELECT * FROM duckdb_indexes()`. Then drop one of them.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q6
    con.execute(
        """
        -- Your query here
        SELECT 'Q6: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Query Optimization (25 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** The following query is inefficient. Identify the problems
    and rewrite it for better performance. Explain each change.

    ```sql
    SELECT *
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN products p ON oi.product_id = p.product_id
    WHERE p.category_id = 1
    ORDER BY o.order_date DESC;
    ```

    *(Explain the problems here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your rewritten query
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
    **Q8.** Rewrite this query to avoid using a function on an indexed
    column:

    ```sql
    SELECT * FROM orders
    WHERE EXTRACT(YEAR FROM order_date) = 2024
      AND EXTRACT(MONTH FROM order_date) = 6;
    ```
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your rewritten query
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
    **Q9.** Rewrite this query using EXISTS instead of IN. Explain why
    EXISTS can be faster.

    ```sql
    SELECT * FROM customers
    WHERE customer_id IN (
        SELECT customer_id FROM orders
        WHERE total_amount > 500
    );
    ```

    *(Write your explanation here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your EXISTS rewrite
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
    **Q10.** This query runs slowly on large tables. Optimize it.

    ```sql
    SELECT c.first_name, c.last_name, c.email,
           COUNT(o.order_id) AS total_orders,
           SUM(o.total_amount) AS total_spent,
           AVG(o.total_amount) AS avg_order
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.email
    ORDER BY total_spent DESC;
    ```

    Suggest what indexes would help and any query rewrites.

    *(Write your index recommendation here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your optimized query
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
    ---
    ## Part 4: Performance Measurement (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q11.** Write a Python function that times a query and returns the
    execution time in milliseconds. Use it to compare the performance of
    two equivalent queries:

    - Query A (subquery): Find customers whose total spending exceeds
      the average customer spending.
    - Query B (CTE): Same result, different approach.
    """)
    return


@app.cell
def _(time):
    # TODO: write your timing function, e.g.:
    # def time_query(con, sql, runs=5):
    #     ...
    print("Q11: define your time_query() function here")
    return


@app.cell
def _(con):
    # TODO: time Query A (subquery approach) here
    print("Q11: time Query A here")
    return


@app.cell
def _(con):
    # TODO: time Query B (CTE approach) here
    print("Q11: time Query B here")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** Generate a larger dataset by duplicating the orders table 10
    times. Re-run your comparison from Q11 on the larger dataset. Does
    the relative performance change?

    *(Write your observations here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: build orders_big and re-run your timing comparison
    print("Q12: build orders_big and re-run your timing comparison here")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Index Design Challenge (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q13.** You are told that the ShopSmart application runs these 5
    queries most frequently:

    1. `SELECT * FROM orders WHERE customer_id = ? AND status = 'completed'`
    2. `SELECT * FROM products WHERE category_id = ? ORDER BY price DESC`
    3. `SELECT * FROM order_items WHERE order_id = ?`
    4. `SELECT * FROM reviews WHERE product_id = ? ORDER BY review_date DESC`
    5. `SELECT * FROM orders WHERE order_date BETWEEN ? AND ?`

    Design an index strategy: which indexes would you create? For each,
    explain your reasoning. Are there any indexes you would NOT create,
    and why?

    *(Write your index design here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Submission

    - Submit notebook with all queries, EXPLAIN outputs, timing results,
      and written analysis
    - **Total: 75 points**
    """)
    return


if __name__ == "__main__":
    app.run()
