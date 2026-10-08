import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 04: SQL Aggregation
    ## Lab 5 — `WHERE`, `GROUP BY`, and `HAVING` (Coffee Shop) · Student

    Work with a single **coffee_orders** table (3 stores, one week of
    orders). Practice the three clauses that control aggregation:

    - `WHERE` — filters **rows** *before* grouping
    - `GROUP BY` — collapses rows into one row per group
    - `HAVING` — filters **groups** *after* grouping (can use `COUNT`, `SUM`, `AVG`, ...)

    Run the setup cells first, then write your SQL in each question cell
    (replace `-- YOUR SQL HERE`).

    Same pattern as before: a prediction, a bug, an explain-it, and an
    optional bonus.
    """)
    return

@app.cell
def _():
    import marimo as mo

    return (mo,)

@app.cell
def _(mo):
    coffee_orders = mo.sql(
        f"""
        CREATE OR REPLACE TABLE coffee_orders AS
        SELECT * FROM (
            VALUES
            (1,  'Downtown', 'Latte',     'Large',  2, 5.50, DATE '2026-09-28', 'Card'),
            (2,  'Downtown', 'Espresso',  'Small',  1, 3.00, DATE '2026-09-28', 'Cash'),
            (3,  'Campus',   'Latte',     'Medium', 1, 4.75, DATE '2026-09-28', 'Card'),
            (4,  'Campus',   'Cold Brew', 'Large',  3, 5.00, DATE '2026-09-29', 'Card'),
            (5,  'Airport',  'Latte',     'Large',  1, 6.50, DATE '2026-09-29', 'Card'),
            (6,  'Downtown', 'Mocha',     'Medium', 2, 5.25, DATE '2026-09-29', 'Card'),
            (7,  'Campus',   'Espresso',  'Small',  2, 3.00, DATE '2026-09-30', 'Cash'),
            (8,  'Airport',  'Cold Brew', 'Large',  2, 6.00, DATE '2026-09-30', 'Card'),
            (9,  'Downtown', 'Latte',     'Medium', 1, 4.75, DATE '2026-09-30', 'Cash'),
            (10, 'Campus',   'Mocha',     'Large',  1, 5.75, DATE '2026-10-01', 'Card'),
            (11, 'Downtown', 'Cold Brew', 'Medium', 1, 4.50, DATE '2026-10-01', 'Card'),
            (12, 'Campus',   'Latte',     'Large',  2, 5.50, DATE '2026-10-01', 'Cash'),
            (13, 'Airport',  'Espresso',  'Small',  1, 3.50, DATE '2026-10-02', 'Card'),
            (14, 'Downtown', 'Espresso',  'Small',  3, 3.00, DATE '2026-10-02', 'Card'),
            (15, 'Campus',   'Cold Brew', 'Medium', 2, 4.50, DATE '2026-10-02', 'Card'),
            (16, 'Downtown', 'Latte',     'Large',  1, 5.50, DATE '2026-10-02', 'Card')
        ) AS t(order_id, store, drink, size, qty, price, order_date, payment);
        """
    )
    return (coffee_orders,)

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q1. How many orders did each store receive? Show `store` and `num_orders`, busiest store first.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q1 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. What is the total revenue of each store? Revenue of one order = `qty * price`. Show `store` and `revenue`, highest first.

    Compare with Q1: is the busiest store also the biggest earner?
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q2 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. `WHERE` before grouping: count only the **Large** orders at each store. Show `store` and `large_orders`, most first (ties: alphabetical by store).
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q3 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. `HAVING` after grouping: show only stores with **more than 5** orders (`store`, `num_orders`).
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q4 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Counting only **Card** payments, which drinks sold **at least 5 cups** in total (`SUM(qty)`)? Show `drink` and `cups`, most first.

    🔮 **Predict first:** Over *all* payments, Latte and Cold Brew each
    sold 8 cups and Espresso sold 7 — all three pass "at least 5." Which
    of them will still appear once we count Card payments only?
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q5 = mo.sql(
        f"""
        -- Predict: ___
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. For each drink ordered **at least 4 times**, show `drink`, `num_orders`, and the average price `avg_price` rounded to 2 decimals. Most expensive first.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q6 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. 🐞 Debug it

    A classmate wanted the stores with more than 5 orders (same as Q4)
    and wrote:

    ```sql
    SELECT store, COUNT(*) AS num_orders
    FROM coffee_orders
    WHERE COUNT(*) > 5
    GROUP BY store;
    ```

    Run it — DuckDB refuses. Read the error message, then fix the query.
    Why can't `COUNT(*)` go in `WHERE`?
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q7 = mo.sql(
        f"""
        -- Why can't COUNT(*) go in WHERE? (one sentence)
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. Group by two columns: count orders for every `store` + `size` combination. Sort by store, then size.

    How many rows do you get? Why isn't it 3 stores × 3 sizes = 9?
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q8 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. All three together: at the **Downtown** store only, which drinks earned **more than $10** in revenue? Show `drink` and `revenue`, highest first.

    Hint: one condition is about a single *order*, the other is about a
    *group total*. Which goes in `WHERE`, and which in `HAVING`?
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q9 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. Run both queries below (one per cell) and compare the results.

    ```sql
    -- Query A
    SELECT store, COUNT(*) AS num_orders
    FROM coffee_orders
    WHERE price > 5
    GROUP BY store;

    -- Query B
    SELECT store, COUNT(*) AS num_orders
    FROM coffee_orders
    GROUP BY store
    HAVING AVG(price) > 5;
    ```

    ✍️ **Explain it:** in one sentence, what does each query throw away —
    and why do they give such different answers?
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q10 = mo.sql(
        f"""
        -- Explanation:
        -- Query A here
        """
    )
    return

@app.cell
def _(coffee_orders, mo):
    q10b = mo.sql(
        f"""
        -- Query B here
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. For each day, show `order_date`, the number of orders `num_orders`, the cheapest price `cheapest`, and the most expensive price `priciest`. Sort by date.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q11 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional — only if you finish early)

    Counting **Card** payments only, show each store's number of
    different drinks sold (`drinks_sold`) and its Card revenue
    (`card_revenue`). Keep only stores whose Card revenue is **more than
    $25**. Highest revenue first.

    Combines `WHERE`, `COUNT(DISTINCT ...)`, `SUM` of an expression,
    `HAVING`, and `ORDER BY` in one query.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q12 = mo.sql(
        f"""
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


    2. One thing about WHERE / GROUP BY / HAVING that is still fuzzy or confusing:


    """
    return (exit_ticket,)

if __name__ == "__main__":
    app.run()
