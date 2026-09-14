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
    # Lab 7: Performance & Indexing — INSTRUCTOR SOLUTIONS

    ## OMIS 105 — Database Management Systems
    **Week 7 | Answer Key**

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
    **Q1.** (5 pts) `EXPLAIN` on a filtered scan.

    > SEQ_SCAN (sequential scan) on `products`, FILTER (`price > 100`),
    and PROJECTION (selecting `product_name`, `price`). DuckDB uses
    columnar scanning and filters in the scan operator.
    """)
    return


@app.cell
def _(con):
    con.execute(
        "EXPLAIN SELECT product_name, price FROM products WHERE price > 100"
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** (5 pts) `EXPLAIN` on a JOIN.

    > DuckDB typically uses a HASH_JOIN for equi-joins: scan of both
    tables, the hash join on `customer_id`, and the filter on
    `total_amount`.
    """)
    return


@app.cell
def _(con):
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
    **Q3.** (5 pts) `EXPLAIN` on a GROUP BY.

    > Additional operations: HASH_GROUP_BY or UNGROUPED_AGGREGATE —
    the scan, then the grouping/aggregation operator.
    """)
    return


@app.cell
def _(con):
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
    **Q4.** (5 pts) Index on `orders(status)`, then `EXPLAIN` a query
    filtering by status.

    > DuckDB is an analytical database and may not always use indexes
    the same way OLTP databases do. The plan may or may not show index
    usage — the learning point is understanding *when* indexes help.
    """)
    return


@app.cell
def _(con):
    con.execute("CREATE INDEX idx_orders_status ON orders(status)")
    return


@app.cell
def _(con):
    con.execute(
        "EXPLAIN SELECT * FROM orders WHERE status = 'completed'"
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** (5 pts) Composite index on `orders(customer_id, order_date)`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        "CREATE INDEX idx_orders_cust_date ON orders(customer_id, order_date)"
    )
    return


@app.cell
def _(con):
    con.execute(
        """
        EXPLAIN
        SELECT * FROM orders
        WHERE customer_id = 5
          AND order_date >= '2024-01-01'
        ORDER BY order_date
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6.** (5 pts) List all indexes, then drop one.
    """)
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM duckdb_indexes()").fetchdf()
    return


@app.cell
def _(con):
    con.execute("DROP INDEX idx_orders_status")
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
    **Q7.** (7 pts) Problems and fixes:
    1. `SELECT *` — should select only needed columns.
    2. LEFT JOINs — since `WHERE p.category_id = 1` filters on
       `products`, the LEFT JOINs are effectively INNER JOINs. Use
       INNER JOIN explicitly.
    3. Start from the most filtered table (`products`).
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT c.first_name, c.last_name,
               o.order_id, o.order_date,
               p.product_name, oi.quantity
        FROM products p
        INNER JOIN order_items oi ON p.product_id = oi.product_id
        INNER JOIN orders o ON oi.order_id = o.order_id
        INNER JOIN customers c ON o.customer_id = c.customer_id
        WHERE p.category_id = 1
        ORDER BY o.order_date DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8.** (6 pts) Avoid a function on the indexed column — use a date
    range instead of `EXTRACT`.

    > This allows an index on `order_date` to be used directly instead
    of computing `EXTRACT` on every row.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT * FROM orders
        WHERE order_date >= '2024-06-01'
          AND order_date < '2024-07-01'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9.** (6 pts) Rewrite `IN` as `EXISTS`.

    > `EXISTS` stops scanning after finding the first match, while `IN`
    must build the complete list. For large subquery result sets,
    `EXISTS` is typically faster.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT * FROM customers c
        WHERE EXISTS (
            SELECT 1 FROM orders o
            WHERE o.customer_id = c.customer_id
              AND o.total_amount > 500
        )
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** (6 pts) Index recommendation plus a CTE rewrite.

    > Pre-aggregating in a CTE reduces the join size. An index on
    `orders(customer_id)` speeds up the GROUP BY.
    """)
    return


@app.cell
def _(con):
    con.execute("CREATE INDEX idx_orders_customer ON orders(customer_id)")
    return


@app.cell
def _(con):
    con.execute(
        """
        WITH order_summary AS (
            SELECT customer_id,
                   COUNT(*) AS total_orders,
                   ROUND(SUM(total_amount), 2) AS total_spent,
                   ROUND(AVG(total_amount), 2) AS avg_order
            FROM orders
            GROUP BY customer_id
        )
        SELECT c.first_name, c.last_name, c.email,
               COALESCE(os.total_orders, 0) AS total_orders,
               COALESCE(os.total_spent, 0) AS total_spent,
               COALESCE(os.avg_order, 0) AS avg_order
        FROM customers c
        LEFT JOIN order_summary os ON c.customer_id = os.customer_id
        ORDER BY total_spent DESC
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
    **Q11.** (5 pts) A timing helper, then Query A (subquery) vs. Query B
    (CTE) for "customers whose spending exceeds the average."
    """)
    return


@app.cell
def _(time):
    def time_query(con, sql, runs=5):
        times = []
        for _ in range(runs):
            start = time.time()
            con.execute(sql).fetchall()
            times.append((time.time() - start) * 1000)
        avg = sum(times) / len(times)
        print(f"  Avg: {avg:.2f}ms over {runs} runs")
        return avg

    return (time_query,)


@app.cell
def _(con, time_query):
    print("Query A (subquery):")
    qa = """
        SELECT c.first_name, c.last_name, SUM(o.total_amount) AS spent
        FROM customers c JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        HAVING SUM(o.total_amount) > (
            SELECT AVG(total_per_cust) FROM (
                SELECT SUM(total_amount) AS total_per_cust
                FROM orders GROUP BY customer_id
            )
        )
    """
    time_query(con, qa)
    return


@app.cell
def _(con, time_query):
    print("Query B (CTE):")
    qb = """
        WITH cust_totals AS (
            SELECT customer_id, SUM(total_amount) AS spent
            FROM orders GROUP BY customer_id
        )
        SELECT c.first_name, c.last_name, ct.spent
        FROM customers c JOIN cust_totals ct ON c.customer_id = ct.customer_id
        WHERE ct.spent > (SELECT AVG(spent) FROM cust_totals)
    """
    time_query(con, qb)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** (5 pts) Duplicate `orders` 10x into `orders_big`, then
    re-run the comparison.

    > With larger data, the CTE approach typically maintains or improves
    relative performance, because the subquery is only computed once.
    """)
    return


@app.cell
def _(con):
    con.execute("CREATE OR REPLACE TABLE orders_big AS SELECT * FROM orders")
    for _ in range(9):
        con.execute("INSERT INTO orders_big SELECT * FROM orders")
    return


@app.cell
def _(con, time_query):
    print("Query A on orders_big (subquery):")
    qa_big = """
        SELECT c.first_name, c.last_name, SUM(o.total_amount) AS spent
        FROM customers c JOIN orders_big o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        HAVING SUM(o.total_amount) > (
            SELECT AVG(total_per_cust) FROM (
                SELECT SUM(total_amount) AS total_per_cust
                FROM orders_big GROUP BY customer_id
            )
        )
    """
    time_query(con, qa_big)
    return


@app.cell
def _(con, time_query):
    print("Query B on orders_big (CTE):")
    qb_big = """
        WITH cust_totals AS (
            SELECT customer_id, SUM(total_amount) AS spent
            FROM orders_big GROUP BY customer_id
        )
        SELECT c.first_name, c.last_name, ct.spent
        FROM customers c JOIN cust_totals ct ON c.customer_id = ct.customer_id
        WHERE ct.spent > (SELECT AVG(spent) FROM cust_totals)
    """
    time_query(con, qb_big)
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
    **Q13.** (10 pts) Recommended indexes:

    | Query | Recommended Index | Reasoning |
    |-------|------------------|-----------|
    | 1 | `orders(customer_id, status)` | Composite covers both filter columns |
    | 2 | `products(category_id, price DESC)` | Covers filter + sort |
    | 3 | `order_items(order_id)` | Direct lookup by FK |
    | 4 | `reviews(product_id, review_date DESC)` | Covers filter + sort |
    | 5 | `orders(order_date)` | Range scan on date |

    Notes:
    - Query 1 and 5 both involve `orders` — could consider a single
      composite, but the use cases are different enough to warrant
      separate indexes.
    - `order_items(order_id)` may already be fast if `order_id` is part
      of the PK.
    - Trade-off: 5 indexes will slow INSERT/UPDATE on these tables. If
      write volume is high, prioritize the most frequent queries.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Grading Rubric

    | Part | Points |
    |------|--------|
    | Part 1: Query Plans | 15 |
    | Part 2: Indexes | 15 |
    | Part 3: Optimization | 25 |
    | Part 4: Measurement | 10 |
    | Part 5: Index Design | 10 |
    | **Total** | **75** |
    """)
    return


if __name__ == "__main__":
    app.run()
