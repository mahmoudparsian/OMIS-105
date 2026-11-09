import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 07: Subqueries
    ## Lab 2 — EXISTS, Derived Tables, Correlated Subqueries & CTEs · Instructor

    Work with a tiny **online store** (customers, products, orders) — the same data as this week's demos. Run the setup cells first, then each question. Answers are filled in.

    Remember:

    - George Brown and Hana Sato never ordered
    - Blender and Standing Desk were never ordered
    - Order 12 is a guest order: its `customer_id` is `NULL`

    See `week07_lab_02_design_notes.md` for the Q11 bug (it is silent — no error).
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
    ### Q1. Products that were ordered (`EXISTS`)

    Show the `product_name` of every product that appears in **at least one** order. Use `EXISTS`. Order by `product_name`.

    🔮 **Predict:** 6 rows.
    """)
    return


@app.cell
def _(mo, orders, products):
    q1 = mo.sql(
        f"""
        -- Predict: 6 rows
        SELECT p.product_name
        FROM products p
        WHERE EXISTS (SELECT 1
                      FROM orders o
                      WHERE o.product_id = p.product_id)
        ORDER BY p.product_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. Customers who never bought Electronics (`NOT EXISTS`)

    Show the `customer_name` of customers who **never** ordered an **Electronics** product (including customers who never ordered anything). Order by `customer_name`.

    Expected: 4 rows — Carmen Diaz, Farah Ali, George Brown, Hana Sato. (The subquery may contain a JOIN.)
    """)
    return


@app.cell
def _(customers, mo, orders, products):
    q2 = mo.sql(
        f"""
        SELECT c.customer_name
        FROM customers c
        WHERE NOT EXISTS (SELECT 1
                          FROM orders o
                          INNER JOIN products p ON o.product_id = p.product_id
                          WHERE o.customer_id = c.customer_id
                            AND p.category = 'Electronics')
        ORDER BY c.customer_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. Customers with a recent order (`EXISTS` + a condition)

    Show the `customer_name` of customers with at least one order **on or after** `2026-09-15`. Order by `customer_name`.

    Expected: 2 rows — Alice Wong, Farah Ali. (The guest order on 2026-09-16 has no customer, so it matches nobody.)
    """)
    return


@app.cell
def _(customers, mo, orders):
    q3 = mo.sql(
        f"""
        SELECT c.customer_name
        FROM customers c
        WHERE EXISTS (SELECT 1
                      FROM orders o
                      WHERE o.customer_id = c.customer_id
                        AND o.order_date >= DATE '2026-09-15')
        ORDER BY c.customer_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. Most units bought by one customer (subquery in `FROM`)

    In a subquery, total the `quantity` per customer (leave out the guest order). In the outer query, show the **largest** of those totals as `max_units_by_one_customer`.

    Expected: 5 (Bob Smith: 1 + 4).
    """)
    return


@app.cell
def _(mo, orders):
    q4 = mo.sql(
        f"""
        SELECT MAX(units) AS max_units_by_one_customer
        FROM (SELECT customer_id, SUM(quantity) AS units
              FROM orders
              WHERE customer_id IS NOT NULL
              GROUP BY customer_id) AS t;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Average revenue per category (subquery in `FROM`)

    In a subquery, compute revenue (`quantity × price`) per **category**. In the outer query, show the average of those revenues, rounded to 2 decimals, as `avg_category_revenue`.

    Expected: 1449.67 — (3125 + 1140 + 84) / 3.
    """)
    return


@app.cell
def _(mo, orders, products):
    q5 = mo.sql(
        f"""
        SELECT ROUND(AVG(revenue), 2) AS avg_category_revenue
        FROM (SELECT p.category, SUM(o.quantity * p.price) AS revenue
              FROM orders o
              INNER JOIN products p ON o.product_id = p.product_id
              GROUP BY p.category) AS t;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. Each customer's first order (correlated)

    Show `customer_id`, `order_id`, and `order_date` of each customer's **first** order. Use a correlated subquery with `MIN`. Order by `customer_id`.

    Expected: 6 rows (orders 1, 3, 5, 7, 9, 11). The guest order is not included: `o2.customer_id = NULL` never matches.
    """)
    return


@app.cell
def _(mo, orders):
    q6 = mo.sql(
        f"""
        SELECT o.customer_id, o.order_id, o.order_date
        FROM orders o
        WHERE o.order_date = (SELECT MIN(o2.order_date)
                              FROM orders o2
                              WHERE o2.customer_id = o.customer_id)
        ORDER BY o.customer_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. The most expensive product in each category (correlated)

    Show `category`, `product_name`, and `price` of the most expensive product **in each category**. Order by `category`.

    ✍️ **Explain it (sample answer):** "Each product must be compared with the maximum of **its own** category, so the subquery must use the outer row's category. Without that, the subquery returns the overall maximum (1200) and only the Laptop is shown."

    Expected: 3 rows — Laptop, Standing Desk, Blender.
    """)
    return


@app.cell
def _(mo, products):
    q7 = mo.sql(
        f"""
        SELECT p.category, p.product_name, p.price
        FROM products p
        WHERE p.price = (SELECT MAX(p2.price)
                         FROM products p2
                         WHERE p2.category = p.category)
        ORDER BY p.category;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. Subquery or JOIN? Electronics buyers

    Show the `customer_name` of customers who ordered an **Electronics** product. First write it with **JOINs** (no `DISTINCT`), then with **`IN`**. Order both by `customer_name`. Why do the row counts differ?

    Expected: the JOIN version returns 6 rows (Alice and David twice — once per order); the `IN` version returns 4. Both cells are shown below.
    """)
    return


@app.cell
def _(customers, mo, orders, products):
    q8_join = mo.sql(
        f"""
        SELECT c.customer_name
        FROM customers c
        INNER JOIN orders   o ON c.customer_id = o.customer_id
        INNER JOIN products p ON o.product_id  = p.product_id
        WHERE p.category = 'Electronics'
        ORDER BY c.customer_name;
        """
    )
    return


@app.cell
def _(customers, mo, orders, products):
    q8 = mo.sql(
        f"""
        SELECT customer_name
        FROM customers
        WHERE customer_id IN (SELECT o.customer_id
                              FROM orders o
                              INNER JOIN products p ON o.product_id = p.product_id
                              WHERE p.category = 'Electronics')
        ORDER BY customer_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Customers who bought more units than average (CTE)

    Use `WITH customer_units AS (...)` to total the `quantity` per customer (leave out the guest order). Then show `customer_name` and `units` for customers above the **average** of `customer_units`. Order by `units` (highest first), then `customer_name`.

    Expected: 3 rows — Bob 5, Alice 4, Elena 4 (the average is 3.67). `customer_units` is used twice.
    """)
    return


@app.cell
def _(customers, mo, orders):
    q9 = mo.sql(
        f"""
        WITH customer_units AS (
            SELECT customer_id, SUM(quantity) AS units
            FROM orders
            WHERE customer_id IS NOT NULL
            GROUP BY customer_id
        )
        SELECT c.customer_name, cu.units
        FROM customer_units cu
        INNER JOIN customers c ON cu.customer_id = c.customer_id
        WHERE cu.units > (SELECT AVG(units) FROM customer_units)
        ORDER BY cu.units DESC, c.customer_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. The top category by revenue (CTE)

    Use `WITH category_revenue AS (...)`, then show the `category` and `revenue` of the category with the **highest** revenue.

    Expected: 1 row — Electronics, 3125.
    """)
    return


@app.cell
def _(mo, orders, products):
    q10 = mo.sql(
        f"""
        WITH category_revenue AS (
            SELECT p.category, SUM(o.quantity * p.price) AS revenue
            FROM orders o
            INNER JOIN products p ON o.product_id = p.product_id
            GROUP BY p.category
        )
        SELECT category, revenue
        FROM category_revenue
        WHERE revenue = (SELECT MAX(revenue) FROM category_revenue);
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. 🐞 Debug it



    Broken query:

    ```sql
    SELECT product_name, category, price
    FROM products
    WHERE price > (SELECT AVG(price)
                   FROM products p2
                   WHERE p2.category = category);
    ```

    **The bug:** inside the subquery, the bare word `category` means **`p2.category`** — the nearest table wins. So the condition is `p2.category = p2.category`, always true, and the subquery returns the **overall** average (325.88). No error, just a wrong answer.

    **The fix:** give the outer table an alias and use it: `WHERE p2.category = p.category`.

    Expected after the fix: 3 rows — Laptop, Standing Desk, Blender.

    **Talking point:** in a correlated subquery, always write the alias on **both** sides.
    """)
    return


@app.cell
def _(mo, products):
    q11 = mo.sql(
        f"""
        SELECT p.product_name, p.category, p.price
        FROM products p
        WHERE p.price > (SELECT AVG(p2.price)
                         FROM products p2
                         WHERE p2.category = p.category)
        ORDER BY p.category;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional — only if you finish early)

    Which customers ordered **only** Electronics products? They must have at least one order, and **no** order of a non-Electronics product. *Hint:* `EXISTS ... AND NOT EXISTS ...`.

    Expected: 1 row — David Kim (Laptop and Headphones). Without the `EXISTS` part, George and Hana would also appear — they have no non-Electronics orders because they have no orders at all.
    """)
    return


@app.cell
def _(customers, mo, orders, products):
    q12 = mo.sql(
        f"""
        SELECT c.customer_name
        FROM customers c
        WHERE EXISTS (SELECT 1 FROM orders o
                      WHERE o.customer_id = c.customer_id)
          AND NOT EXISTS (SELECT 1
                          FROM orders o
                          INNER JOIN products p ON o.product_id = p.product_id
                          WHERE o.customer_id = c.customer_id
                            AND p.category <> 'Electronics');
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


    2. One thing about EXISTS, correlated subqueries, or CTEs that is still fuzzy or confusing:


    """
    return (exit_ticket,)


if __name__ == "__main__":
    app.run()
