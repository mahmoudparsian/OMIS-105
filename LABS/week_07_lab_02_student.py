import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 07: Subqueries
    ## Lab 2 — EXISTS, Derived Tables, Correlated Subqueries & CTEs · Student

    Work with a tiny **online store** (customers, products, orders) — the same data as this week's demos. Run the setup cells first, then write your SQL in each question cell (replace `-- YOUR SQL HERE`).

    Remember:

    - George Brown and Hana Sato never ordered
    - Blender and Standing Desk were never ordered
    - Order 12 is a guest order: its `customer_id` is `NULL`

    Today: a prediction, two explain-its, a bug to fix, and an optional bonus.
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

    🔮 **Predict first:** there are 8 products, and 2 were never ordered. How many rows?
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
    ### Q2. Customers who never bought Electronics (`NOT EXISTS`)

    Show the `customer_name` of customers who **never** ordered an **Electronics** product (including customers who never ordered anything). Order by `customer_name`.
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
    ### Q3. Customers with a recent order (`EXISTS` + a condition)

    Show the `customer_name` of customers with at least one order **on or after** `2026-09-15`. Order by `customer_name`.
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
    ### Q4. Most units bought by one customer (subquery in `FROM`)

    In a subquery, total the `quantity` per customer (leave out the guest order). In the outer query, show the **largest** of those totals as `max_units_by_one_customer`.
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
    ### Q5. Average revenue per category (subquery in `FROM`)

    In a subquery, compute revenue (`quantity × price`) per **category**. In the outer query, show the average of those revenues, rounded to 2 decimals, as `avg_category_revenue`.
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
    ### Q6. Each customer's first order (correlated)

    Show `customer_id`, `order_id`, and `order_date` of each customer's **first** order. Use a correlated subquery with `MIN`. Order by `customer_id`.
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
    ### Q7. The most expensive product in each category (correlated)

    Show `category`, `product_name`, and `price` of the most expensive product **in each category**. Order by `category`.

    ✍️ **Explain it:** why does this need a *correlated* subquery? What would you get with `WHERE price = (SELECT MAX(price) FROM products)` instead?
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
    ### Q8. Subquery or JOIN? Electronics buyers

    Show the `customer_name` of customers who ordered an **Electronics** product. First write it with **JOINs** (no `DISTINCT`), then with **`IN`**. Order both by `customer_name`. Why do the row counts differ?
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
    ### Q9. Customers who bought more units than average (CTE)

    Use `WITH customer_units AS (...)` to total the `quantity` per customer (leave out the guest order). Then show `customer_name` and `units` for customers above the **average** of `customer_units`. Order by `units` (highest first), then `customer_name`.
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
    ### Q10. The top category by revenue (CTE)

    Use `WITH category_revenue AS (...)`, then show the `category` and `revenue` of the category with the **highest** revenue.
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



    This should list products that cost more than the average **of their own category**:

    ```sql
    SELECT product_name, category, price
    FROM products
    WHERE price > (SELECT AVG(price)
                   FROM products p2
                   WHERE p2.category = category);
    ```

    It runs with **no error** and returns 2 rows. But the Blender (90) costs more than the Kitchen average (51) and is missing. Find the bug and fix it. Order by `category`.
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

    Which customers ordered **only** Electronics products? They must have at least one order, and **no** order of a non-Electronics product. *Hint:* `EXISTS ... AND NOT EXISTS ...`.
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


    2. One thing about EXISTS, correlated subqueries, or CTEs that is still fuzzy or confusing:


    """
    return (exit_ticket,)


if __name__ == "__main__":
    app.run()
