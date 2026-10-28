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
    # Lab 7: Subqueries — A Query Inside a Query — INSTRUCTOR SOLUTIONS

    ## OMIS 105 — Database Management Systems
    **Week 7 | Answer Key | 10 questions × 3 points = 30 points**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Run the next two cells first. They connect to DuckDB and load `customers`, `products`, `orders`
    from this folder's `data/` directory — the same data as the demos.

    **Rules for every query:** give every table an alias and use it on every
    column; list the columns you need (no `SELECT *`); use the `ORDER BY` given
    in the question. The **expected row count** is given for each question —
    if yours is different, look again at your query.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import duckdb

    DATA_DIR = Path(__file__).parent / "data"
    con = duckdb.connect(database=":memory:")
    return DATA_DIR, con


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv('{DATA_DIR}/customers.csv')"
    )
    con.execute(
        f"CREATE OR REPLACE TABLE products AS SELECT * FROM read_csv('{DATA_DIR}/products.csv')"
    )
    con.execute(
        f"CREATE OR REPLACE TABLE orders AS SELECT * FROM read_csv('{DATA_DIR}/orders.csv')"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Scalar Subqueries — One Value (9 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1. Cheaper than average.** Show `product_name` and `price` for products that cost **less** than the average price. Order by `price`.

    *Expected: 6 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT product_name, price
        FROM products
        WHERE price < (SELECT AVG(price)
                       FROM products)
        ORDER BY price
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | product_name | price |
    |---|---|
    | Coffee Mug | 12 |
    | Phone Case | 25 |
    | Blender | 90 |
    | Headphones | 150 |
    | Bookshelf | 180 |
    | Desk Chair | 300 |

    **Why:** The average price is 325.875. Six products are below it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2. The cheapest product.** Show `product_name` and `price` of the product(s) with the **lowest** price. Use `MIN` in a subquery, not `ORDER BY ... LIMIT 1`.

    *Expected: 1 row.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT product_name, price
        FROM products
        WHERE price = (SELECT MIN(price)
                       FROM products)
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | product_name | price |
    |---|---|
    | Coffee Mug | 12 |

    **Why:** `MIN` in a subquery would also show a tie; `LIMIT 1` would hide it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3. A subquery in `SELECT`.** For every product, show `product_name`, `price`, and how much more it costs than the cheapest product, as `above_cheapest`. Order by `above_cheapest` (highest first).

    *Expected: 8 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT product_name,
               price,
               price - (SELECT MIN(price) FROM products) AS above_cheapest
        FROM products
        ORDER BY above_cheapest DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | product_name | price | above_cheapest |
    |---|---|---|
    | Laptop | 1200 | 1188 |
    | Standing Desk | 650 | 638 |
    | Desk Chair | 300 | 288 |
    | Bookshelf | 180 | 168 |
    | Headphones | 150 | 138 |
    | Blender | 90 | 78 |
    | Phone Case | 25 | 13 |
    | Coffee Mug | 12 | 0 |

    **Why:** The scalar subquery gives the same value (12) on every row.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: List Subqueries — `IN`, `NOT IN`, `EXISTS` (12 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4. Nested `IN`.** Show the `product_name` of every product ordered by a customer who lives in `'San Jose'`. Use two nested `IN` subqueries, no JOIN. Order by `product_name`.

    *Expected: 4 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT product_name
        FROM products
        WHERE product_id IN (
            SELECT product_id
            FROM orders
            WHERE customer_id IN (
                SELECT customer_id
                FROM customers
                WHERE city = 'San Jose'
            )
        )
        ORDER BY product_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | product_name |
    |---|
    | Bookshelf |
    | Coffee Mug |
    | Headphones |
    | Phone Case |

    **Why:** Inside-out: San Jose customers → 2, 5; their orders → 102, 106, 105, 103; names of those products.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5. `NOT IN`.** Show the `product_name` of products that were **never ordered**. Order by `product_name`. In one sentence: why is `NOT IN` safe here, but not for customers?

    *Expected: 2 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT product_name
        FROM products
        WHERE product_id NOT IN (SELECT product_id
                                 FROM orders)
        ORDER BY product_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | product_name |
    |---|
    | Blender |
    | Standing Desk |

    **Why:** `orders.product_id` has no `NULL`. `orders.customer_id` has one (order 12), and one `NULL` in a `NOT IN` list returns zero rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6. `NOT EXISTS`.** Show `customer_name` and `city` of customers who **never ordered**. Use `NOT EXISTS`. Order by `customer_name`.

    *Expected: 2 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT c.customer_name, c.city
        FROM customers AS c
        WHERE NOT EXISTS (SELECT 1
                          FROM orders AS o
                          WHERE o.customer_id = c.customer_id)
        ORDER BY c.customer_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | customer_name | city |
    |---|---|
    | George Brown | Sunnyvale |
    | Hana Sato | Cupertino |

    **Why:** `NOT EXISTS` is safe with the guest order's `NULL`. `NOT IN` without `IS NOT NULL` returns 0 rows here.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7. `EXISTS`.** Show the `product_name` of products that appear in **at least one** order with a `quantity` of **3 or more**. Use `EXISTS`. Order by `product_name`.

    *Expected: 2 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT p.product_name
        FROM products AS p
        WHERE EXISTS (SELECT 1
                      FROM orders AS o
                      WHERE o.product_id = p.product_id
                        AND o.quantity >= 3)
        ORDER BY p.product_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | product_name |
    |---|
    | Coffee Mug |
    | Phone Case |

    **Why:** Only orders 4 (Coffee Mug, 4) and 10 (Phone Case, 3) have quantity ≥ 3.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Going Further (9 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8. A subquery in `FROM`.** What is the average number of orders per customer? Count orders per customer in a subquery (leave out the guest order), then average those counts in the outer query, rounded to 2 decimals, as `avg_orders_per_customer`.

    *Expected: 1 row.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT ROUND(AVG(num_orders), 2) AS avg_orders_per_customer
        FROM (
            SELECT customer_id, COUNT(*) AS num_orders
            FROM orders
            WHERE customer_id IS NOT NULL
            GROUP BY customer_id
        ) AS t
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | avg_orders_per_customer |
    |---|
    | 2.17 |

    **Why:** Counts: Alice 3, the other five customers 2 each → 13 / 6 = 2.17. Without `WHERE customer_id IS NOT NULL`, the guest order becomes a 7th "customer" and the answer is 2.00 — wrong.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9. Correlated subquery.** Show `product_name`, `category`, and `price` of products that cost **less** than the average price **of their own category**. Order by `category`, then `product_name`.

    *Expected: 5 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT p.product_name, p.category, p.price
        FROM products AS p
        WHERE p.price < (SELECT AVG(p2.price)
                         FROM products AS p2
                         WHERE p2.category = p.category)
        ORDER BY p.category, p.product_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | product_name | category | price |
    |---|---|---|
    | Headphones | Electronics | 150 |
    | Phone Case | Electronics | 25 |
    | Bookshelf | Furniture | 180 |
    | Desk Chair | Furniture | 300 |
    | Coffee Mug | Kitchen | 12 |

    **Why:** Electronics average 458.33, Furniture 376.67, Kitchen 51. Each product is compared with its own category.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10. CTE.** Use `WITH product_sales AS (...)` to total the `quantity` sold per product as `units_sold`. Then show the `product_name` and `units_sold` of the best-selling product(s).

    *Expected: 1 row.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        WITH product_sales AS (
            SELECT product_id, SUM(quantity) AS units_sold
            FROM orders
            GROUP BY product_id
        )
        SELECT p.product_name, ps.units_sold
        FROM product_sales AS ps
        INNER JOIN products AS p
            ON ps.product_id = p.product_id
        WHERE ps.units_sold = (SELECT MAX(units_sold)
                               FROM product_sales)
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | product_name | units_sold |
    |---|---|
    | Coffee Mug | 7 |

    **Why:** Coffee Mug: 4 + 2 + 1 = 7 units. `product_sales` is used twice: in `FROM` and in the `MAX` subquery.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Grading

    - 3 points per question: 2 for a correct result, 1 for a clean query
      (and, where asked, the short written answer)
    - **Total: 30 points**

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
