import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 07: Subqueries
    ## Lab 1 — Scalar Subqueries, IN & NOT IN · Instructor

    Work with a tiny **online store** (customers, products, orders) — the same data as this week's demos. Run the setup cells first, then each question. Answers are filled in.

    Remember:

    - George Brown and Hana Sato never ordered
    - Blender and Standing Desk were never ordered
    - Order 12 is a guest order: its `customer_id` is `NULL`

    Rule for students: **every answer uses a subquery** — no number typed by hand. See `week07_lab_01_design_notes.md`.
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    customers = mo.sql(
        f"""
        CREATE OR REPLACE TABLE customers AS
        SELECT * FROM (
          VALUES
            (1, 'Alice Wong', 'Santa Clara'),
            (2, 'Bob Smith', 'San Jose'),
            (3, 'Carmen Diaz', 'Sunnyvale'),
            (4, 'David Kim', 'Santa Clara'),
            (5, 'Elena Rossi', 'San Jose'),
            (6, 'Farah Ali', 'Cupertino'),
            (7, 'George Brown', 'Sunnyvale'),
            (8, 'Hana Sato', 'Cupertino')
        ) AS t(customer_id, customer_name, city);
        """
    )
    return (customers,)


@app.cell
def _(mo):
    products = mo.sql(
        f"""
        CREATE OR REPLACE TABLE products AS
        SELECT * FROM (
          VALUES
            (101, 'Laptop', 'Electronics', 1200),
            (102, 'Headphones', 'Electronics', 150),
            (103, 'Phone Case', 'Electronics', 25),
            (104, 'Desk Chair', 'Furniture', 300),
            (105, 'Bookshelf', 'Furniture', 180),
            (106, 'Coffee Mug', 'Kitchen', 12),
            (107, 'Blender', 'Kitchen', 90),
            (108, 'Standing Desk', 'Furniture', 650)
        ) AS t(product_id, product_name, category, price);
        """
    )
    return (products,)


@app.cell
def _(mo):
    orders = mo.sql(
        f"""
        CREATE OR REPLACE TABLE orders AS
        SELECT * FROM (
          VALUES
            (1, 1, 101, 1, DATE '2026-09-01'),
            (2, 1, 103, 2, DATE '2026-09-03'),
            (3, 2, 102, 1, DATE '2026-09-04'),
            (4, 2, 106, 4, DATE '2026-09-05'),
            (5, 3, 104, 1, DATE '2026-09-06'),
            (6, 3, 106, 2, DATE '2026-09-08'),
            (7, 4, 101, 1, DATE '2026-09-10'),
            (8, 4, 102, 2, DATE '2026-09-11'),
            (9, 5, 105, 1, DATE '2026-09-12'),
            (10, 5, 103, 3, DATE '2026-09-14'),
            (11, 6, 106, 1, DATE '2026-09-15'),
            (12, NULL, 102, 1, DATE '2026-09-16'),
            (13, 1, 104, 1, DATE '2026-09-18'),
            (14, 6, 105, 2, DATE '2026-09-20')
        ) AS t(order_id, customer_id, product_id, quantity, order_date);
        """
    )
    return (orders,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q1. Step 1 on its own: the average quantity

    Write a query that returns the **average `quantity`** per order.

    🔮 **Predict:** 1 row, 1 column (about 1.64).
    """)
    return


@app.cell
def _(mo, orders):
    q1 = mo.sql(
        f"""
        -- Predict: 1 rows
        SELECT AVG(quantity) AS avg_quantity
        FROM orders;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. Orders above the average quantity

    Use Q1 as a subquery. Show `order_id`, `product_id`, and `quantity` for orders with a quantity **greater than** the average.

    Expected: 6 rows (orders 2, 4, 6, 8, 10, 14).
    """)
    return


@app.cell
def _(mo, orders):
    q2 = mo.sql(
        f"""
        SELECT order_id, product_id, quantity
        FROM orders
        WHERE quantity > (SELECT AVG(quantity) FROM orders);
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. The most recent order

    Show `order_id`, `customer_id`, and `order_date` of the most recent order. Use `MAX` in a subquery, not `ORDER BY ... LIMIT 1`.

    Expected: 1 row — order 14 (2026-09-20).
    """)
    return


@app.cell
def _(mo, orders):
    q3 = mo.sql(
        f"""
        SELECT order_id, customer_id, order_date
        FROM orders
        WHERE order_date = (SELECT MAX(order_date) FROM orders);
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. Price as a percent of the top price (subquery in `SELECT`)

    For every product, show `product_name`, `price`, and the price as a percent of the most expensive product's price, rounded to 1 decimal, as `pct_of_top_price`. Order by `price` (highest first). *Hint:* write `100.0 * price / (...)`.

    Expected: 8 rows — Laptop 100.0 … Coffee Mug 1.0.
    """)
    return


@app.cell
def _(mo, products):
    q4 = mo.sql(
        f"""
        SELECT product_name,
               price,
               ROUND(100.0 * price / (SELECT MAX(price) FROM products), 1) AS pct_of_top_price
        FROM products
        ORDER BY price DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Same category as the Desk Chair

    Show `product_name` and `price` of the other products in the **same category as 'Desk Chair'** (do not show the Desk Chair itself). Do **not** type the category name — find it with a subquery.

    Expected: 2 rows — Bookshelf, Standing Desk. (A scalar subquery can return text too.)
    """)
    return


@app.cell
def _(mo, products):
    q5 = mo.sql(
        f"""
        SELECT product_name, price
        FROM products
        WHERE category = (SELECT category
                          FROM products
                          WHERE product_name = 'Desk Chair')
          AND product_name <> 'Desk Chair';
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. Customers who bought a Kitchen product (nested `IN`)

    Show the `customer_name` of every customer who ordered a product in the **Kitchen** category. Use two nested `IN` subqueries — no JOIN. Order by `customer_name`.

    Expected: 3 rows — Bob Smith, Carmen Diaz, Farah Ali (all bought Coffee Mugs).
    """)
    return


@app.cell
def _(customers, mo, orders, products):
    q6 = mo.sql(
        f"""
        SELECT customer_name
        FROM customers
        WHERE customer_id IN (SELECT customer_id
                              FROM orders
                              WHERE product_id IN (SELECT product_id
                                                   FROM products
                                                   WHERE category = 'Kitchen'))
        ORDER BY customer_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. What did Alice Wong buy?

    Show the `product_name` of every product **Alice Wong** ordered. Do not type her `customer_id` — find it with a subquery. Order by `product_name`.

    Expected: 3 rows — Desk Chair, Laptop, Phone Case. (The innermost subquery returns one value, so `=` works there; the middle one returns a list, so it needs `IN`.)
    """)
    return


@app.cell
def _(customers, mo, orders, products):
    q7 = mo.sql(
        f"""
        SELECT product_name
        FROM products
        WHERE product_id IN (SELECT product_id
                             FROM orders
                             WHERE customer_id = (SELECT customer_id
                                                  FROM customers
                                                  WHERE customer_name = 'Alice Wong'))
        ORDER BY product_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. Products no San Jose customer ordered (`NOT IN`)

    Show the `product_name` of products that **no customer from San Jose** ever ordered. Order by `product_name`.

    Expected: 4 rows — Blender, Desk Chair, Laptop, Standing Desk. (`orders.product_id` has no `NULL`, so `NOT IN` is safe here.)
    """)
    return


@app.cell
def _(customers, mo, orders, products):
    q8 = mo.sql(
        f"""
        SELECT product_name
        FROM products
        WHERE product_id NOT IN (SELECT product_id
                                 FROM orders
                                 WHERE customer_id IN (SELECT customer_id
                                                       FROM customers
                                                       WHERE city = 'San Jose'))
        ORDER BY product_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Cupertino customers who never ordered

    Show the `customer_name` of customers in **Cupertino** who **never** placed an order. Use `NOT IN`.

    ✍️ **Explain it (sample answer):** "Without the filter I got 0 rows. The list from `orders` contains a `NULL` (guest order 12). `NOT IN` means 'not equal to every value', and `8 <> NULL` is unknown, so the whole test is unknown and the row is dropped. Adding `WHERE customer_id IS NOT NULL` removes the `NULL`."

    The query that returns 0 rows:

    ```sql
    SELECT customer_name
    FROM customers
    WHERE city = 'Cupertino'
      AND customer_id NOT IN (SELECT customer_id
                              FROM orders);
    ```

    Expected after the fix: 1 row — Hana Sato.
    """)
    return


@app.cell
def _(customers, mo, orders):
    q9 = mo.sql(
        f"""
        SELECT customer_name
        FROM customers
        WHERE city = 'Cupertino'
          AND customer_id NOT IN (SELECT customer_id
                                  FROM orders
                                  WHERE customer_id IS NOT NULL);
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. Customers with more than 2 orders (`IN` + `GROUP BY`)

    Show the `customer_name` of customers who placed **more than 2** orders. The subquery should use `GROUP BY` and `HAVING`.

    Expected: 1 row — Alice Wong (3 orders).
    """)
    return


@app.cell
def _(customers, mo, orders):
    q10 = mo.sql(
        f"""
        SELECT customer_name
        FROM customers
        WHERE customer_id IN (SELECT customer_id
                              FROM orders
                              GROUP BY customer_id
                              HAVING COUNT(*) > 2);
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. 🐞 Debug it



    Broken query:

    ```sql
    SELECT product_name, price
    FROM products
    WHERE price = (SELECT price
                   FROM products
                   WHERE category = 'Electronics');
    ```

    DuckDB says: `Invalid Input Error: More than one row returned by a subquery used as an expression - scalar subqueries can only return a single row.`

    **The bug:** `=` needs **one** value, but there are three Electronics prices.

    **The fix:** `IN`.

    Expected after the fix: 3 rows — Laptop, Headphones, Phone Case.

    **Talking point:** older DuckDB versions silently picked one random row here. An error is better than a wrong answer.
    """)
    return


@app.cell
def _(mo, products):
    q11 = mo.sql(
        f"""
        SELECT product_name, price
        FROM products
        WHERE price IN (SELECT price
                        FROM products
                        WHERE category = 'Electronics')
        ORDER BY price DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional — only if you finish early)

    Show the `product_name` and `price` of the **second most expensive** product. *Hint:* the largest price that is smaller than the largest price. (A subquery inside a subquery.)

    Expected: Standing Desk, 650.
    """)
    return


@app.cell
def _(mo, products):
    q12 = mo.sql(
        f"""
        SELECT product_name, price
        FROM products
        WHERE price = (SELECT MAX(price)
                       FROM products
                       WHERE price < (SELECT MAX(price) FROM products));
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## ✅ Exit Ticket — before you submit

    (Instructor copy — read a few out loud, anonymously, next class.)
    """)
    return


@app.cell
def _():
    exit_ticket = """
    1. One thing that clicked for you today:


    2. One thing about subqueries that is still fuzzy or confusing:


    """
    return (exit_ticket,)


if __name__ == "__main__":
    app.run()
