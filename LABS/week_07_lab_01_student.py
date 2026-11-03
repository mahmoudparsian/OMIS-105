import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 07: Subqueries
    ## Lab 1 — Scalar Subqueries, IN & NOT IN · Student

    Work with a tiny **online store** (customers, products, orders) — the same data as this week's demos. Run the setup cells first, then write your SQL in each question cell (replace `-- YOUR SQL HERE`).

    Remember:

    - George Brown and Hana Sato never ordered
    - Blender and Standing Desk were never ordered
    - Order 12 is a guest order: its `customer_id` is `NULL`

    **Rule: every answer must use a subquery.** Typing a number by hand (like `WHERE quantity > 1.64`) gets no credit.

    Today: a prediction, an explain-it, a bug to fix, and an optional bonus.
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

    🔮 **Predict first:** how many rows and columns will it return? (This is what makes it usable as a *scalar* subquery.)
    """)
    return


@app.cell
def _(mo):
    q1 = mo.sql(
        """
        -- Predict: ___ rows
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. Orders above the average quantity

    Use Q1 as a subquery. Show `order_id`, `product_id`, and `quantity` for orders with a quantity **greater than** the average.
    """)
    return


@app.cell
def _(mo):
    q2 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. The most recent order

    Show `order_id`, `customer_id`, and `order_date` of the most recent order. Use `MAX` in a subquery, not `ORDER BY ... LIMIT 1`.
    """)
    return


@app.cell
def _(mo):
    q3 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. Price as a percent of the top price (subquery in `SELECT`)

    For every product, show `product_name`, `price`, and the price as a percent of the most expensive product's price, rounded to 1 decimal, as `pct_of_top_price`. Order by `price` (highest first). *Hint:* write `100.0 * price / (...)`.
    """)
    return


@app.cell
def _(mo):
    q4 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Same category as the Desk Chair

    Show `product_name` and `price` of the other products in the **same category as 'Desk Chair'** (do not show the Desk Chair itself). Do **not** type the category name — find it with a subquery.
    """)
    return


@app.cell
def _(mo):
    q5 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. Customers who bought a Kitchen product (nested `IN`)

    Show the `customer_name` of every customer who ordered a product in the **Kitchen** category. Use two nested `IN` subqueries — no JOIN. Order by `customer_name`.
    """)
    return


@app.cell
def _(mo):
    q6 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. What did Alice Wong buy?

    Show the `product_name` of every product **Alice Wong** ordered. Do not type her `customer_id` — find it with a subquery. Order by `product_name`.
    """)
    return


@app.cell
def _(mo):
    q7 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. Products no San Jose customer ordered (`NOT IN`)

    Show the `product_name` of products that **no customer from San Jose** ever ordered. Order by `product_name`.
    """)
    return


@app.cell
def _(mo):
    q8 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Cupertino customers who never ordered

    Show the `customer_name` of customers in **Cupertino** who **never** placed an order. Use `NOT IN`.

    ✍️ **Explain it:** try it first *without* filtering `NULL`s inside the subquery. How many rows do you get? Why? Then fix it.
    """)
    return


@app.cell
def _(mo):
    q9 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. Customers with more than 2 orders (`IN` + `GROUP BY`)

    Show the `customer_name` of customers who placed **more than 2** orders. The subquery should use `GROUP BY` and `HAVING`.
    """)
    return


@app.cell
def _(mo):
    q10 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. 🐞 Debug it



    A classmate wants every product with the same price as an Electronics product:

    ```sql
    SELECT product_name, price
    FROM products
    WHERE price = (SELECT price
                   FROM products
                   WHERE category = 'Electronics');
    ```

    DuckDB stops with an error. Read the error message, then fix the query. Order by `price` (highest first).
    """)
    return


@app.cell
def _(mo):
    q11 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional — only if you finish early)

    Show the `product_name` and `price` of the **second most expensive** product. *Hint:* the largest price that is smaller than the largest price. (A subquery inside a subquery.)
    """)
    return


@app.cell
def _(mo):
    q12 = mo.sql(
        """
        -- YOUR SQL HERE (bonus)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## ✅ Exit Ticket — before you submit
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
