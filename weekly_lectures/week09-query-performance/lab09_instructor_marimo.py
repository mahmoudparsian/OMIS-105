import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 9: Ranking Functions — `ROW_NUMBER`, `RANK`, `DENSE_RANK` (INSTRUCTOR SOLUTIONS)

    ## OMIS 105 — Database Management Systems
    **Week 9 | Answer Key | 10 questions × 3 points = 30 points**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Run the next cell first. It connects to DuckDB and loads `customers`, `orders`, `order_items`, `products`, `categories`, `reviews` from this folder's `data/` directory.

    **Rules for every query:**

    - **Every answer must use a ranking function** — `ROW_NUMBER`, `RANK`, or `DENSE_RANK`
    - To **filter** on a rank, compute it in a subquery or CTE first — `WHERE` cannot see it
    - With `ROW_NUMBER`, always add the tie-breaker the question gives
    - List the columns you need — no `SELECT *` — and use the `ORDER BY` given
    - The **expected row count** is given for each question. If yours is different, check your ranking first
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import duckdb

    DATA_DIR = Path(__file__).parent / "data"
    con = duckdb.connect(database=":memory:")
    for _t in ["customers", "orders", "order_items", "products", "categories", "reviews"]:
        con.execute(
            f"CREATE OR REPLACE TABLE {_t} AS "
            f"SELECT * FROM read_csv('{DATA_DIR}/{_t}.csv')"
        )
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1: `ROW_NUMBER` (9 points)

    Number rows one by one — and restart the numbering in each group.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1. Number the products.** Show `product_name`, `price`, and `rn` — a `ROW_NUMBER()` by price, **highest first**, with `product_id` as the tie-breaker. Order by `rn` and show the first 10 rows.

    *Expected: 10 rows.*
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT product_name, price,
               ROW_NUMBER() OVER (ORDER BY price DESC, product_id) AS rn
        FROM products
        ORDER BY rn
        LIMIT 10
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2. Restart for each category.** Join `products` to `categories`. Show `category_name`, `product_name`, `price`, and `rn` — a `ROW_NUMBER()` that **restarts at 1 in each category** (highest price first, tie-breaker `product_id`). Order by `category_name`, then `rn`.

    *Expected: 64 rows; exactly 8 rows have `rn = 1`.*
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT c.category_name, p.product_name, p.price,
               ROW_NUMBER() OVER (PARTITION BY c.category_name
                                  ORDER BY p.price DESC, p.product_id) AS rn
        FROM products AS p
        JOIN categories AS c ON c.category_id = p.category_id
        ORDER BY c.category_name, rn
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3. The most expensive product in each category.** Use Q2's query as a **subquery** and keep only `rn = 1`. Show `category_name`, `product_name`, and `price`. Order by `category_name`.

    *Expected: 8 rows.*
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT category_name, product_name, price
        FROM (
            SELECT c.category_name, p.product_name, p.price,
                   ROW_NUMBER() OVER (PARTITION BY c.category_name
                                      ORDER BY p.price DESC, p.product_id) AS rn
            FROM products AS p
            JOIN categories AS c ON c.category_id = p.category_id
        ) AS ranked
        WHERE rn = 1
        ORDER BY category_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2: Ties — `RANK` and `DENSE_RANK` (12 points)

    The data has real ties: three customers with 9 orders, two cities with 6 customers, two with 4.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4. All three, side by side.** In a CTE, count each customer's orders: `customer_id`, `first_name`, `n_orders` (join `customers` and `orders`). Then show those three columns plus `row_num` (`ROW_NUMBER`, tie-breaker `customer_id`), `rnk` (`RANK`), and `dense_rnk` (`DENSE_RANK`) — all ordered by `n_orders`, highest first. Order by `row_num` and show the first 10 rows.

    🔮 **Predict first:** three customers have 9 orders. What will `rnk` and `dense_rnk` be for the customer with **8** orders?

    *Expected: 10 rows.*
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH order_counts AS (
            SELECT cu.customer_id, cu.first_name,
                   COUNT(*) AS n_orders
            FROM customers AS cu
            JOIN orders AS o ON o.customer_id = cu.customer_id
            GROUP BY cu.customer_id, cu.first_name
        )
        SELECT customer_id, first_name, n_orders,
               ROW_NUMBER() OVER (ORDER BY n_orders DESC, customer_id) AS row_num,
               RANK()       OVER (ORDER BY n_orders DESC)              AS rnk,
               DENSE_RANK() OVER (ORDER BY n_orders DESC)              AS dense_rnk
        FROM order_counts
        ORDER BY row_num
        LIMIT 10
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Note:** Rosa, Cora, Derek (9 orders): `rnk` 1, `dense_rnk` 1. Mia (8 orders): **`rnk` 4, `dense_rnk` 2** — `RANK` skips 2 and 3 after the three-way tie; `DENSE_RANK` does not.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5. Top 4 — keeping ties.** Using Q4's CTE, show `customer_id`, `first_name`, `n_orders`, and `rnk` (`RANK`) for every customer with `rnk <= 4`. Order by `rnk`, then `customer_id`.

    ✍️ **Explain it:** you asked for the top **4** — why are there more than 4 rows? How many rows would `ROW_NUMBER() <= 4` return?

    *Expected: 5 rows.*
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH order_counts AS (
            SELECT cu.customer_id, cu.first_name,
                   COUNT(*) AS n_orders
            FROM customers AS cu
            JOIN orders AS o ON o.customer_id = cu.customer_id
            GROUP BY cu.customer_id, cu.first_name
        ),
        ranked AS (
            SELECT *, RANK() OVER (ORDER BY n_orders DESC) AS rnk
            FROM order_counts
        )
        SELECT customer_id, first_name, n_orders, rnk
        FROM ranked
        WHERE rnk <= 4
        ORDER BY rnk, customer_id
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Note:** 5 rows, because Mia and Nora tie at 8 orders and **both** get rank 4. `ROW_NUMBER() <= 4` would return exactly 4 rows and drop Nora only because of the tie-breaker.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6. Rank the cities.** In a CTE, count the customers in each `city` (`n_customers`). Show `city`, `n_customers`, and `city_rank` — a `DENSE_RANK` by `n_customers`, highest first. Order by `city_rank`, then `city`.

    *Expected: 10 rows; the last `city_rank` is 5.*
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH city_counts AS (
            SELECT city, COUNT(*) AS n_customers
            FROM customers
            GROUP BY city
        )
        SELECT city, n_customers,
               DENSE_RANK() OVER (ORDER BY n_customers DESC) AS city_rank
        FROM city_counts
        ORDER BY city_rank, city
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7. The 3rd-highest value.** Which city or cities have the **3rd-highest** number of customers? Rank in a CTE with `DENSE_RANK`, then keep `city_rank = 3`. Show `city` and `n_customers`. Order by `city`.

    ✍️ **Explain it:** change `DENSE_RANK` to `RANK`. How many rows do you get now, and why?

    *Expected: 2 rows.*
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH city_counts AS (
            SELECT city, COUNT(*) AS n_customers
            FROM customers
            GROUP BY city
        ),
        ranked AS (
            SELECT city, n_customers,
                   DENSE_RANK() OVER (ORDER BY n_customers DESC) AS city_rank
            FROM city_counts
        )
        SELECT city, n_customers
        FROM ranked
        WHERE city_rank = 3
        ORDER BY city
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With `RANK` instead of `DENSE_RANK`:
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH city_counts AS (
            SELECT city, COUNT(*) AS n_customers
            FROM customers
            GROUP BY city
        ),
        ranked AS (
            SELECT city, n_customers,
                   RANK() OVER (ORDER BY n_customers DESC) AS city_rank
            FROM city_counts
        )
        SELECT city, n_customers
        FROM ranked
        WHERE city_rank = 3
        ORDER BY city
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Note:** Austin and San Jose (4 customers each). With `RANK`, the ranks are 1, 2, 2, **4**, … — no city has rank 3, so the query returns **0 rows**. For "Nth-highest value" questions, use `DENSE_RANK`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 3: Ranking Results and Patterns (9 points)

    Rank a `GROUP BY` result, find the first event per group, and fix a common error.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8. Rank a `GROUP BY` result.** In a CTE, compute each category's `revenue` = `SUM(quantity * unit_price)` from `order_items` (join `products` and `categories`), rounded to 2 decimals. Show `category_name`, `revenue`, and `revenue_rank` (`DENSE_RANK`, highest revenue first). Order by `revenue_rank`, then `category_name`.

    *Expected: 8 rows.*
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH category_revenue AS (
            SELECT c.category_name,
                   ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
            FROM order_items AS oi
            JOIN products   AS p ON p.product_id  = oi.product_id
            JOIN categories AS c ON c.category_id = p.category_id
            GROUP BY c.category_name
        )
        SELECT category_name, revenue,
               DENSE_RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
        FROM category_revenue
        ORDER BY revenue_rank, category_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9. Each customer's first order.** Show each customer's **first** order: `customer_id`, `order_id`, `order_date`. Use `ROW_NUMBER()` with `PARTITION BY customer_id`, ordered by `order_date` (tie-breaker `order_id`), in a subquery; keep `rn = 1`. Order by `order_date`, then `customer_id`.

    *Expected: 40 rows.*
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT customer_id, order_id, order_date
        FROM (
            SELECT customer_id, order_id, order_date,
                   ROW_NUMBER() OVER (PARTITION BY customer_id
                                      ORDER BY order_date, order_id) AS rn
            FROM orders
        ) AS ranked
        WHERE rn = 1
        ORDER BY order_date, customer_id
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10. 🐞 Debug it.** A classmate wanted the **best-rated** products (every product tied for the highest average rating) and wrote:

    ```sql
    WITH product_ratings AS (
        SELECT p.product_name,
               ROUND(AVG(r.rating), 2) AS avg_rating
        FROM products AS p
        JOIN reviews AS r ON r.product_id = p.product_id
        GROUP BY p.product_name
    )
    SELECT product_name, avg_rating,
           DENSE_RANK() OVER (ORDER BY avg_rating DESC) AS rating_rank
    FROM product_ratings
    WHERE rating_rank = 1;
    ```

    DuckDB answers: **`WHERE clause cannot contain window functions!`** Explain in one sentence why `WHERE` cannot see `rating_rank`, then fix the query. Show `product_name` and `avg_rating`. Order by `product_name`.

    *Expected: 10 rows.*
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        WITH product_ratings AS (
            SELECT p.product_name,
                   ROUND(AVG(r.rating), 2) AS avg_rating
            FROM products AS p
            JOIN reviews AS r ON r.product_id = p.product_id
            GROUP BY p.product_name
        ),
        ranked AS (
            SELECT product_name, avg_rating,
                   DENSE_RANK() OVER (ORDER BY avg_rating DESC) AS rating_rank
            FROM product_ratings
        )
        SELECT product_name, avg_rating
        FROM ranked
        WHERE rating_rank = 1
        ORDER BY product_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Note:** `WHERE` is applied **before** window functions are computed, so `rating_rank` does not exist yet. Fix: put the `DENSE_RANK` in a second CTE (or a subquery) and filter outside it. 10 products tie at an average of 5.00.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Grading

    - 3 points per question: 2 for a correct result, 1 for using the right
      ranking function (and `PARTITION BY` / a subquery or CTE where needed)
    - The short written answers in Q5, Q7, and Q10 are part of their second point


    ---

    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
