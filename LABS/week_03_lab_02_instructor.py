import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 04: SQL Aggregation
    ## Lab 5 — `WHERE`, `GROUP BY`, and `HAVING` (Coffee Shop) · Instructor

    Work with a single **coffee_orders** table (3 stores, one week of
    orders). Practice the three clauses that control aggregation:

    - `WHERE` — filters **rows** *before* grouping
    - `GROUP BY` — collapses rows into one row per group
    - `HAVING` — filters **groups** *after* grouping (can use `COUNT`, `SUM`, `AVG`, ...)

    Run the setup cells first, then each question. Answers are filled in.

    Same template as the v2 labs: Q5 (predict — `WHERE` changes what
    `HAVING` sees), Q7 (debug — aggregate in `WHERE`), Q10 (explain —
    `WHERE price > 5` vs `HAVING AVG(price) > 5`), Q12 (bonus).
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

    Expected: Downtown 7, Campus 6, Airport 3.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q1 = mo.sql(
        f"""
        SELECT store, COUNT(*) AS num_orders
        FROM coffee_orders
        GROUP BY store
        ORDER BY num_orders DESC;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. What is the total revenue of each store? Revenue of one order = `qty * price`. Show `store` and `revenue`, highest first.

    Expected: Campus 51.50, Downtown 48.25, Airport 22.00.

    **Talking point:** Downtown has the *most orders* (Q1) but Campus
    has the *most revenue* — "busiest" and "biggest earner" are
    different questions with different `GROUP BY` answers.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q2 = mo.sql(
        f"""
        SELECT store, SUM(qty * price) AS revenue
        FROM coffee_orders
        GROUP BY store
        ORDER BY revenue DESC;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. `WHERE` before grouping: count only the **Large** orders at each store. Show `store` and `large_orders`, most first (ties: alphabetical by store).

    Expected: Campus 3, Airport 2, Downtown 2.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q3 = mo.sql(
        f"""
        SELECT store, COUNT(*) AS large_orders
        FROM coffee_orders
        WHERE size = 'Large'
        GROUP BY store
        ORDER BY large_orders DESC, store;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. `HAVING` after grouping: show only stores with **more than 5** orders (`store`, `num_orders`).

    Expected: Campus 6, Downtown 7 (Airport, with 3, is filtered out).
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q4 = mo.sql(
        f"""
        SELECT store, COUNT(*) AS num_orders
        FROM coffee_orders
        GROUP BY store
        HAVING COUNT(*) > 5
        ORDER BY store;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Counting only **Card** payments, which drinks sold **at least 5 cups** in total (`SUM(qty)`)? Show `drink` and `cups`, most first.

    🔮 **Predict first:** Over *all* payments, Latte and Cold Brew each
    sold 8 cups and Espresso sold 7. Which of the three will still
    appear once we count Card payments only?

    **Answer:** Cold Brew 8, Latte 5. Espresso disappears — it sold 7
    cups overall, but 3 of them were paid in cash, leaving only 4 Card
    cups. Latte drops from 8 to 5 but just survives.

    **Talking point:** `WHERE` runs first and *changes the numbers*
    that `HAVING` later tests. The `HAVING` threshold is the same; the
    groups it sees are smaller.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q5 = mo.sql(
        f"""
        -- Predict: Cold Brew and Latte stay; Espresso drops out (only 4 Card cups)
        SELECT drink, SUM(qty) AS cups
        FROM coffee_orders
        WHERE payment = 'Card'
        GROUP BY drink
        HAVING SUM(qty) >= 5
        ORDER BY cups DESC;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. For each drink ordered **at least 4 times**, show `drink`, `num_orders`, and the average price `avg_price` rounded to 2 decimals. Most expensive first.

    Expected: Latte 6 / 5.42, Cold Brew 4 / 5.00, Espresso 4 / 3.13
    (Mocha, with 3 orders, is filtered out).
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q6 = mo.sql(
        f"""
        SELECT drink,
               COUNT(*)             AS num_orders,
               ROUND(AVG(price), 2) AS avg_price
        FROM coffee_orders
        GROUP BY drink
        HAVING COUNT(*) >= 4
        ORDER BY avg_price DESC;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. 🐞 Debug it

    Goal: stores with more than 5 orders (same as Q4). Broken query:

    ```sql
    SELECT store, COUNT(*) AS num_orders
    FROM coffee_orders
    WHERE COUNT(*) > 5
    GROUP BY store;
    ```

    DuckDB: `Binder Error: WHERE clause cannot contain aggregates!`

    **The bug:** `WHERE` runs *before* `GROUP BY`. At that moment there
    are no groups yet, so there is nothing to count — `COUNT(*)` has no
    meaning in `WHERE`.

    **The fix:** move the condition to `HAVING`, which runs after the
    groups are formed.

    **Talking point for class:** unlike the silent bugs in earlier labs,
    this one *does* raise an error — good. Use it to anchor the
    processing order on the board:
    `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q7 = mo.sql(
        f"""
        -- WHERE runs before groups exist, so aggregates belong in HAVING
        SELECT store, COUNT(*) AS num_orders
        FROM coffee_orders
        GROUP BY store
        HAVING COUNT(*) > 5;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. Group by two columns: count orders for every `store` + `size` combination. Sort by store, then size.

    Expected: 8 rows — Airport (Large 2, Small 1), Campus (Large 3,
    Medium 2, Small 1), Downtown (Large 2, Medium 3, Small 2). Airport
    has no Medium row because it sold no Medium drinks.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q8 = mo.sql(
        f"""
        SELECT store, size, COUNT(*) AS num_orders
        FROM coffee_orders
        GROUP BY store, size
        ORDER BY store, size;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. All three together: at the **Downtown** store only, which drinks earned **more than $10** in revenue? Show `drink` and `revenue`, highest first.

    Expected: Latte 21.25, Espresso 12.00, Mocha 10.50 (Cold Brew,
    4.50, is filtered out).

    **Talking point:** `WHERE store = 'Downtown'` is a condition on a
    *row* (each order has a store) → `WHERE`. `revenue > 10` is a
    condition on a *group total* → `HAVING`.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q9 = mo.sql(
        f"""
        SELECT drink, SUM(qty * price) AS revenue
        FROM coffee_orders
        WHERE store = 'Downtown'
        GROUP BY drink
        HAVING SUM(qty * price) > 10
        ORDER BY revenue DESC;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. Run both queries below and compare them.

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

    Results: **A** → Airport 2, Campus 2, Downtown 3. **B** → Airport 3
    only (average prices: Airport 5.33, Campus 4.75, Downtown 4.50).

    ✍️ **Explain it (sample answer):** "Query A throws away every
    *order* priced $5 or less and then counts the expensive orders at
    each store; Query B keeps all orders, and then throws away every
    *store* whose average price is $5 or less."
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q10 = mo.sql(
        f"""
        -- A: WHERE removes cheap ORDERS, then counts what's left per store
        -- B: HAVING removes whole STORES whose average price is <= 5
        SELECT store, COUNT(*) AS num_orders
        FROM coffee_orders
        WHERE price > 5
        GROUP BY store
        ORDER BY store;
        """
    )
    return

@app.cell
def _(coffee_orders, mo):
    q10b = mo.sql(
        f"""
        SELECT store, COUNT(*) AS num_orders
        FROM coffee_orders
        GROUP BY store
        HAVING AVG(price) > 5
        ORDER BY store;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. For each day, show `order_date`, the number of orders `num_orders`, the cheapest price `cheapest`, and the most expensive price `priciest`. Sort by date.

    Expected: 5 rows (Sep 28 – Oct 2). Oct 2 is the busiest day with 4
    orders; Sep 29 has the highest price of the week (6.50).
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q11 = mo.sql(
        f"""
        SELECT order_date,
               COUNT(*)   AS num_orders,
               MIN(price) AS cheapest,
               MAX(price) AS priciest
        FROM coffee_orders
        GROUP BY order_date
        ORDER BY order_date;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional)

    Counting **Card** payments only, show each store's number of
    different drinks sold (`drinks_sold`) and its Card revenue
    (`card_revenue`). Keep only stores whose Card revenue is **more than
    $25**. Highest revenue first.

    Expected: Downtown 4 / 40.50, Campus 3 / 34.50 (Airport, 22.00, is
    filtered out).

    Combines `WHERE`, `COUNT(DISTINCT ...)`, `SUM` of an expression,
    `HAVING`, and `ORDER BY` in one query.
    """)
    return

@app.cell
def _(coffee_orders, mo):
    q12 = mo.sql(
        f"""
        SELECT store,
               COUNT(DISTINCT drink) AS drinks_sold,
               SUM(qty * price)      AS card_revenue
        FROM coffee_orders
        WHERE payment = 'Card'
        GROUP BY store
        HAVING SUM(qty * price) > 25
        ORDER BY card_revenue DESC;
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


    2. One thing about WHERE / GROUP BY / HAVING that is still fuzzy or confusing:


    """
    return (exit_ticket,)

if __name__ == "__main__":
    app.run()
