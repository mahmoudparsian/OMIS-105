import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — SQL's `CASE` Expression, Step by Step

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    This notebook assumes you have **never seen** a `CASE` expression.
    We start very small and add one idea at a time.

    | Part | Level | Lessons |
    |------|-------|---------|
    | 1 | Basic | B1–B5: `WHEN` / `THEN` / `ELSE` / `END`, more outcomes, first match wins, missing `ELSE`, the short form |
    | 2 | Basic+ | P1–P6: the wrong-order trap, richer conditions, `NULL`, numbers, `ORDER BY`, the "same type" rule |
    | 3 | Intermediate | I1–I6: `GROUP BY`, conditional counts and sums, `JOIN`, customer segments, safe division, `UPDATE` |

    The companion file `case_expression_tutorial.md` has the same
    lessons with the same IDs, so you can read one and run the other.

    **Tip:** after each query runs, change a number or a condition and
    watch the result change. That is the fastest way to learn.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 0. The Sample Data

    A tiny online store keeps 2 tables:

    | Table | Rows | Columns |
    |-------|-----:|---------|
    | `products` | 8 | `product_id`, `product_name`, `category`, `price`, `stock` |
    | `orders` | 11 | `order_id`, `customer`, `product_id`, `quantity`, `status`, `order_date` |

    `orders.product_id` points to `products.product_id`
    (one product can appear in many orders).

    The cell below opens an **in-memory** DuckDB database and builds
    both tables. Nothing is saved to disk.
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=":memory:")

    con.execute("""
    CREATE OR REPLACE TABLE products (
        product_id   INTEGER PRIMARY KEY,
        product_name VARCHAR,
        category     VARCHAR,
        price        DECIMAL(8, 2),
        stock        INTEGER          -- NULL means "we don't know"
    )
    """)

    con.execute("""
    INSERT INTO products VALUES
        (1, 'Laptop',     'Electronics', 1200.00,    5),
        (2, 'Mouse',      'Electronics',   25.00,  150),
        (3, 'Desk Chair', 'Furniture',    180.00,    0),
        (4, 'Notebook',   'Office',         3.00,  500),
        (5, 'Monitor',    'Electronics',  300.00,   12),
        (6, 'Bookshelf',  'Furniture',     95.00,    8),
        (7, 'Pen Pack',   'Office',         6.00, NULL),
        (8, 'Headphones', 'Electronics',   80.00,   40)
    """)

    con.execute("""
    CREATE OR REPLACE TABLE orders (
        order_id   INTEGER PRIMARY KEY,
        customer   VARCHAR,
        product_id INTEGER,
        quantity   INTEGER,
        status     VARCHAR,           -- shipped, pending, cancelled, returned
        order_date DATE
    )
    """)

    con.execute("""
    INSERT INTO orders VALUES
        (101, 'Alice', 1,  1, 'shipped',   DATE '2026-01-05'),
        (102, 'Bob',   2,  3, 'pending',   DATE '2026-01-07'),
        (103, 'Alice', 4, 10, 'shipped',   DATE '2026-02-02'),
        (104, 'Carol', 3,  2, 'cancelled', DATE '2026-02-10'),
        (105, 'Dan',   5,  2, 'shipped',   DATE '2026-02-15'),
        (106, 'Bob',   8,  1, 'returned',  DATE '2026-03-01'),
        (107, 'Carol', 6,  1, 'shipped',   DATE '2026-03-03'),
        (108, 'Dan',   7,  5, 'shipped',   DATE '2026-03-20'),
        (109, 'Alice', 2,  2, 'cancelled', DATE '2026-03-22'),
        (110, 'Eve',   1,  1, 'shipped',   DATE '2026-03-28'),
        (111, 'Eve',   2,  4, 'pending',   DATE '2026-04-02')
    """)
    return (con,)


@app.cell
def _(con):
    con.execute("""
    SELECT * FROM products
    """).fetchdf()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT * FROM orders
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Notice two things we will use later:

    - The Desk Chair has `stock = 0` (sold out).
    - The Pen Pack has `stock = NULL` (nobody counted it yet).

    ---

    ## What Is a `CASE` Expression?

    A `CASE` expression lets SQL **make a decision for each row**.
    You already know this idea from everyday life:

    > **If** the price is under $100, **then** call it "Cheap".
    > **Otherwise**, call it "Expensive".

    In Python you write `if ... elif ... else`.
    In SQL you write `CASE ... WHEN ... THEN ... ELSE ... END`:

    ```sql
    CASE
        WHEN <condition 1> THEN <result 1>
        WHEN <condition 2> THEN <result 2>
        ...
        ELSE <default result>
    END
    ```

    | Keyword | Meaning |
    |---------|---------|
    | `CASE`  | "I am starting a decision." |
    | `WHEN`  | "Test this condition." (a yes/no question) |
    | `THEN`  | "If the answer is yes, give back this value." |
    | `ELSE`  | "If no `WHEN` said yes, give back this value." (optional) |
    | `END`   | "The decision is finished." (required!) |

    Two important facts:

    1. `CASE` is an **expression**. It produces **one value** for each
       row — just like `price * 2` or `UPPER(product_name)` do. So it
       can go anywhere a value can go: `SELECT`, `ORDER BY`,
       `GROUP BY`, inside `SUM()`, and more.
    2. `CASE` does **not** change your table. It only changes what you
       see in the result.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    # Part 1 — Basic

    ## B1. Your first `CASE`: two outcomes

    **Question:** Label each product as `'Cheap'` (under $100) or
    `'Expensive'`.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT product_name,
           price,
           CASE
               WHEN price < 100 THEN 'Cheap'
               ELSE 'Expensive'
           END AS price_label
    FROM products
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **How to read it:** for each row, DuckDB asks "Is `price < 100`?"
    If yes, the answer is `'Cheap'`. If no, the `ELSE` gives
    `'Expensive'`.

    `AS price_label` names the new column. Without it, the header
    would be the whole `CASE ... END` text — hard to read.

    **Try it:** move the slider. The query below re-runs every time,
    and the labels change.
    """)
    return


@app.cell
def _(mo):
    cutoff = mo.ui.slider(start=0, stop=1500, step=25, value=100, label="'Cheap' means price under $", show_value=True)
    cutoff
    return (cutoff,)


@app.cell
def _(con, cutoff):
    con.execute(f"""
    SELECT product_name,
           price,
           CASE
               WHEN price < {cutoff.value} THEN 'Cheap'
               ELSE 'Expensive'
           END AS price_label
    FROM products
    ORDER BY price
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## B2. More than two outcomes

    **Question:** Put each product into a price tier:

    - under $20 → `'Budget'`
    - under $200 → `'Mid-range'`
    - everything else → `'Premium'`

    Just add more `WHEN` lines.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT product_name,
           price,
           CASE
               WHEN price < 20  THEN 'Budget'
               WHEN price < 200 THEN 'Mid-range'
               ELSE 'Premium'
           END AS price_tier
    FROM products
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## B3. How `CASE` thinks: the first match wins

    `CASE` checks the `WHEN` lines **from top to bottom**. As soon as
    one condition is true, it returns that `THEN` value and **stops**.
    The lines below are never checked for that row.

    Let's follow two rows through the query in B2:

    | Row | `price < 20`? | `price < 200`? | `ELSE` | Result |
    |-----|---------------|----------------|--------|--------|
    | Notebook (3.00) | **yes → stop** | (not checked) | (not checked) | `Budget` |
    | Monitor (300.00) | no | no | **used** | `Premium` |

    The Notebook's price is also less than 200 — but that does not
    matter. `CASE` already stopped at the first `WHEN`. This is why the
    second line did not need `price >= 20 AND price < 200`.
    Keep this rule in mind; it comes back in P1.

    ## B4. What if you forget the `ELSE`?

    `ELSE` is optional. But if no `WHEN` matches and there is no
    `ELSE`, the result is **`NULL`** (empty, "unknown").
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT product_name,
           category,
           CASE
               WHEN category = 'Electronics' THEN 'Tech'
               WHEN category = 'Furniture'   THEN 'Home'
           END AS dept_label          -- no ELSE!
    FROM products
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The two `Office` products got `NULL` (shown as `None`), because no
    `WHEN` matched them.

    **Good habit:** always write an `ELSE`, even if it is only
    `ELSE 'Other'`. Then a missing case is easy to see.

    ## B5. The short form: "simple" `CASE`

    When every `WHEN` compares **the same column** with `=`, you can
    write the column **once**, right after `CASE`:
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT product_name,
           category,
           CASE category
               WHEN 'Electronics' THEN 'Tech'
               WHEN 'Furniture'   THEN 'Home'
               ELSE 'Other'
           END AS dept_label
    FROM products
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    | Searched `CASE` (long form) | Simple `CASE` (short form) |
    |-----------------------------|----------------------------|
    | `CASE WHEN category = 'Office' THEN ...` | `CASE category WHEN 'Office' THEN ...` |
    | Any condition: `<`, `>`, `AND`, `OR`, `IN`, `LIKE`, `IS NULL`, ... | Only "equals" (`=`) on one column |
    | Works for everything | Shorter, easy to read for code → label lookups |

    **Tip:** when in doubt, use the long (searched) form. It can do
    everything the short form can do, and more.

    ---

    # Part 2 — Basic+

    ## P1. The wrong-order trap

    The first true `WHEN` wins (B3), so **order matters**. Here the
    conditions are in the wrong order — the widest range first:
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT product_name,
           price,
           CASE
               WHEN price < 200 THEN 'Mid-range'   -- too wide, checked first!
               WHEN price < 20  THEN 'Budget'      -- never reached
               ELSE 'Premium'
           END AS price_tier
    FROM products
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    There is **no error** — but the answer is **wrong**. The Notebook
    ($3) and the Pen Pack ($6) should be `'Budget'`. They are caught by
    `price < 200` first, so the `'Budget'` line is never reached.

    **Rule:** when ranges overlap, put the **narrowest** condition
    first (or write ranges that do not overlap).

    ## P2. Richer conditions: `AND`, `IN`, `BETWEEN`

    A `WHEN` can hold **any** condition you could write in a `WHERE`
    clause.

    **Question:** Give each order a short note for the warehouse team.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT order_id,
           customer,
           quantity,
           status,
           CASE
               WHEN status IN ('cancelled', 'returned')       THEN 'No action'
               WHEN status = 'pending' AND quantity >= 3      THEN 'Big order - pack today'
               WHEN status = 'pending'                        THEN 'Pack this week'
               WHEN order_date BETWEEN DATE '2026-03-01'
                                   AND DATE '2026-03-31'      THEN 'Shipped in March'
               ELSE 'Shipped earlier'
           END AS warehouse_note
    FROM orders
    ORDER BY order_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Read the `WHEN` lines as plain English:

    - `status IN ('cancelled', 'returned')` — the status is one of
      these two. (A short way to write
      `status = 'cancelled' OR status = 'returned'`.)
    - `status = 'pending' AND quantity >= 3` — **both** must be true.
    - `order_date BETWEEN ... AND ...` — the date is in March
      (both ends included).

    Line 2 comes **before** line 3. A big pending order matches both,
    and we want the more specific message (see P1).

    ## P3. `CASE` and `NULL` values

    The Pen Pack's stock is `NULL` (unknown). Let's build a stock report.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT product_name,
           stock,
           CASE
               WHEN stock IS NULL THEN 'Unknown - please count'
               WHEN stock = 0     THEN 'Sold out'
               WHEN stock < 10    THEN 'Low - reorder'
               ELSE 'In stock'
           END AS stock_status
    FROM products
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **1. Test for `NULL` with `IS NULL`, and test it first.**
    `NULL < 10` is not true and not false — it is *unknown*. A `WHEN`
    only fires when its condition is **true**, so a `NULL` row would
    skip every `WHEN` and fall into the `ELSE` (`'In stock'` — wrong!).

    **2. The short form cannot find `NULL`.**
    `CASE stock WHEN NULL THEN ...` means `stock = NULL`, which is
    never true — not even when `stock` *is* `NULL`:
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT product_name,
           stock,
           CASE stock
               WHEN NULL THEN 'Unknown'      -- this NEVER matches
               WHEN 0    THEN 'Sold out'
               ELSE 'Has a number'
           END AS wrong_check
    FROM products
    WHERE product_id IN (3, 7)
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The Pen Pack should say `'Unknown'`, but it says `'Has a number'`.
    For `NULL`, always use the long form with `IS NULL`.

    ## P4. `CASE` can return numbers, too

    **Question:** This week there is a sale: Electronics 10% off,
    Furniture 20% off, everything else no discount. Show the sale price.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT product_name,
           category,
           price,
           CASE category
               WHEN 'Electronics' THEN 0.10
               WHEN 'Furniture'   THEN 0.20
               ELSE 0.00
           END AS discount,
           ROUND(price * (1 - CASE category
                                  WHEN 'Electronics' THEN 0.10
                                  WHEN 'Furniture'   THEN 0.20
                                  ELSE 0.00
                              END), 2) AS sale_price
    FROM products
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The `CASE` inside `sale_price` gives back one number per row, and
    `price * (1 - that number)` uses it. A `CASE` can sit **inside** a
    bigger calculation — it is just a value.

    ## P5. `CASE` in `ORDER BY`: a custom sort order

    `ORDER BY status` sorts alphabetically: cancelled, pending,
    returned, shipped. The team wants **pending first** (they need
    action), then shipped, then the rest. The trick: turn each status
    into a **sort number**.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT order_id,
           customer,
           status
    FROM orders
    ORDER BY CASE status
                 WHEN 'pending' THEN 1
                 WHEN 'shipped' THEN 2
                 ELSE 3
             END,
             order_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The `CASE` is not shown in the result. It only decides the order.
    The second sort key, `order_id`, breaks ties inside each group.

    ## P6. The "same type" rule

    Every `THEN` and the `ELSE` must give back the **same kind of
    value**: all text, or all numbers, or all dates. Here we mix text
    (`'Sold out'`) with a number (`stock`). The cell below runs it and
    shows the real DuckDB error:
    """)
    return


@app.cell
def _(con, mo):
    try:
        con.execute("""
        SELECT product_name,
               CASE
                   WHEN stock = 0 THEN 'Sold out'
                   ELSE stock
               END AS stock_info
        FROM products
        """).fetchdf()
        _out = mo.callout(mo.md("No error?! (unexpected)"), kind="warn")
    except Exception as err:
        _msg = str(err).splitlines()[0]
        _out = mo.callout(mo.md(f"**DuckDB error:** `{_msg}`"), kind="danger")
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    DuckDB decided the column is a number (`INT32`), then found the
    text `'Sold out'` and could not turn it into a number.

    **Fix:** make every branch the same type. Here, turn the number into
    text with `CAST(... AS VARCHAR)`:
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT product_name,
           CASE
               WHEN stock = 0 THEN 'Sold out'
               ELSE CAST(stock AS VARCHAR)
           END AS stock_info
    FROM products
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    (The Pen Pack shows `NULL`: `stock = 0` is unknown for `NULL`, so
    the `ELSE` runs, and `CAST(NULL AS VARCHAR)` is still `NULL`.)

    ---

    # Part 3 — Intermediate

    ## I1. `GROUP BY` a `CASE`

    Because `CASE` makes a new value for each row, you can **group by**
    that value.

    **Question:** How many products are in each price tier, and what is
    their average price?
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT CASE
               WHEN price < 20  THEN 'Budget'
               WHEN price < 200 THEN 'Mid-range'
               ELSE 'Premium'
           END                  AS price_tier,
           COUNT(*)             AS num_products,
           ROUND(AVG(price), 2) AS avg_price,
           STRING_AGG(product_name, ', ' ORDER BY product_name) AS products
    FROM products
    GROUP BY price_tier
    ORDER BY avg_price
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The `products` column is an "x-ray": `STRING_AGG` lists the rows
    inside each group, so you can check the counts with your own eyes.

    **DuckDB note:** `GROUP BY price_tier` uses the alias from `SELECT`.
    DuckDB allows this. Some other databases do not — there you must
    repeat the whole `CASE` in the `GROUP BY`.

    ## I2. Conditional counting: `SUM(CASE ...)`

    This is the most useful `CASE` pattern in business reports.

    **Question:** For each customer, how many orders were shipped,
    pending, and cancelled/returned — **side by side in one row**?

    The idea: make a column that is `1` when the row matches and `0`
    when it does not. Then `SUM` adds up the 1s — that is a count!
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT customer,
           COUNT(*) AS total_orders,
           SUM(CASE WHEN status = 'shipped' THEN 1 ELSE 0 END) AS shipped,
           SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending,
           SUM(CASE WHEN status IN ('cancelled', 'returned')
                    THEN 1 ELSE 0 END)                         AS cancelled_or_returned
    FROM orders
    GROUP BY customer
    ORDER BY customer
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **X-ray:** here are Alice's rows *before* `GROUP BY`, with the
    `CASE` value for the `shipped` column. `SUM` adds the last column:
    1 + 1 + 0 = **2**.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT order_id,
           customer,
           status,
           CASE WHEN status = 'shipped' THEN 1 ELSE 0 END AS is_shipped
    FROM orders
    WHERE customer = 'Alice'
    ORDER BY order_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Same result, two other ways** (good to recognize when you read
    other people's SQL):

    - `COUNT(CASE WHEN status = 'shipped' THEN 1 END)` — no `ELSE`, so
      non-matching rows become `NULL`, and `COUNT` skips `NULL`s.
    - `COUNT(*) FILTER (WHERE status = 'shipped')` — DuckDB's `FILTER`
      clause, a shortcut for exactly this pattern.

    The cell below proves all three give the same numbers:
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT customer,
           SUM(CASE WHEN status = 'shipped' THEN 1 ELSE 0 END) AS sum_case,
           COUNT(CASE WHEN status = 'shipped' THEN 1 END)      AS count_case,
           COUNT(*) FILTER (WHERE status = 'shipped')          AS count_filter
    FROM orders
    GROUP BY customer
    ORDER BY customer
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I3. Conditional sums with a `JOIN`

    `SUM(CASE ...)` can add up **amounts**, not just 1s.

    **Question:** For each product category, how much money did we
    **earn** (shipped orders) and how much did we **lose** (cancelled
    or returned orders)? Amount = `quantity * price`.

    `orders` has the quantity; `products` has the price and category,
    so we `JOIN` them first.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT p.category,
           SUM(CASE WHEN o.status = 'shipped'
                    THEN o.quantity * p.price ELSE 0 END) AS earned,
           SUM(CASE WHEN o.status IN ('cancelled', 'returned')
                    THEN o.quantity * p.price ELSE 0 END) AS lost,
           SUM(CASE WHEN o.status = 'pending'
                    THEN o.quantity * p.price ELSE 0 END) AS waiting
    FROM orders AS o
    JOIN products AS p ON o.product_id = p.product_id
    GROUP BY p.category
    ORDER BY earned DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    One query, one row per category, three money columns.
    Without `CASE`, you would need three separate queries.

    ## I4. `CASE` on totals: customer segments

    `CASE` can also test the result of an aggregate like `SUM(...)`.

    **Question:** Put each customer into a loyalty segment based on how
    much they spent on **shipped** orders:

    - $1,000 or more → `'Gold'`
    - $500 or more → `'Silver'`
    - more than $0 → `'Bronze'`
    - $0 → `'No purchases yet'`

    A **CTE** (`WITH`) computes each customer's total once and gives it
    a name, `total_spent`. Then the outer `CASE` is short and easy to
    read. (CTEs are covered fully in Week 7 and Week 9.)
    """)
    return


@app.cell
def _(con):
    con.execute("""
    WITH spending AS (
        SELECT o.customer,
               SUM(CASE WHEN o.status = 'shipped'
                        THEN o.quantity * p.price ELSE 0 END) AS total_spent
        FROM orders AS o
        JOIN products AS p ON o.product_id = p.product_id
        GROUP BY o.customer
    )
    SELECT customer,
           total_spent,
           CASE
               WHEN total_spent >= 1000 THEN 'Gold'
               WHEN total_spent >= 500  THEN 'Silver'
               WHEN total_spent > 0     THEN 'Bronze'
               ELSE 'No purchases yet'
           END AS segment
    FROM spending
    ORDER BY total_spent DESC
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Bob has two orders, but one is pending and one was returned — so
    his shipped total is $0. Without the `ELSE`, his segment would be
    `NULL`.

    ## I5. Safe division: avoid dividing by zero

    **Question:** For each customer, what percent of their ordered
    **units** were cancelled or returned?

    A percent is `part / total`. If `total` were 0, the division would
    fail or give a meaningless value. A `CASE` can guard against it:
    "if the total is 0, give `NULL`; otherwise divide."
    """)
    return


@app.cell
def _(con):
    con.execute("""
    WITH units AS (
        SELECT customer,
               SUM(quantity) AS total_units,
               SUM(CASE WHEN status IN ('cancelled', 'returned')
                        THEN quantity ELSE 0 END) AS bad_units
        FROM orders
        GROUP BY customer
    )
    SELECT customer,
           total_units,
           bad_units,
           CASE
               WHEN total_units = 0 THEN NULL
               ELSE ROUND(100.0 * bad_units / total_units, 1)
           END AS pct_bad
    FROM units
    ORDER BY pct_bad DESC, customer
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    In our data no customer has 0 units, so the guard never fires — but
    in real data it will, someday. The `CASE` makes the query safe
    **before** that day comes.

    ## I6. `CASE` in `UPDATE`: change many rows in one statement

    Until now, `CASE` only changed what we **see**. Inside an
    `UPDATE`, it changes the **stored data**.

    **Question:** Next month prices change: Electronics +5%, Office
    +10%, Furniture stays the same.

    To keep our original `products` table safe, we first make a copy
    (`new_prices`) and update the copy.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE new_prices AS
    SELECT product_id, product_name, category,
           price AS old_price,
           price AS new_price
    FROM products
    """)

    con.execute("""
    UPDATE new_prices
    SET new_price = CASE category
                        WHEN 'Electronics' THEN ROUND(new_price * 1.05, 2)
                        WHEN 'Office'      THEN ROUND(new_price * 1.10, 2)
                        ELSE new_price            -- keep the same price
                    END
    """)

    con.execute("""
    SELECT * FROM new_prices ORDER BY category, product_id
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    One `UPDATE` changed three categories in three different ways.

    **Why `ELSE new_price` matters here:** without it, Furniture would
    get `NULL` (see B4) — and the update would **erase** those prices.
    In an `UPDATE`, a missing `ELSE` can destroy data.

    ---

    ## Common Mistakes

    | Mistake | What happens | Fix |
    |---------|--------------|-----|
    | Forgetting `END` | Syntax error | Every `CASE` needs its own `END` |
    | No `ELSE` | Unmatched rows get `NULL` (B4) — in an `UPDATE`, data is erased (I6) | Always write an `ELSE` |
    | Wide condition first | No error, but wrong labels (P1) | Narrowest condition first |
    | `CASE col WHEN NULL` | Never matches (P3) | Use `WHEN col IS NULL` (long form) |
    | `NULL` not tested first | `NULL` rows fall into `ELSE` (P3) | Put `WHEN col IS NULL` at the top |
    | Mixing text and numbers | `Conversion Error` (P6) | Same type in every branch (`CAST`) |
    | No `AS` alias | Ugly column name | `END AS my_label` |

    ## Cheat Sheet

    ```sql
    -- Searched CASE (long form): any condition
    CASE
        WHEN price < 20  THEN 'Budget'
        WHEN price < 200 THEN 'Mid-range'
        ELSE 'Premium'
    END AS price_tier

    -- Simple CASE (short form): one column, "equals" only
    CASE status
        WHEN 'pending' THEN 1
        WHEN 'shipped' THEN 2
        ELSE 3
    END

    -- Where CASE can go
    SELECT   CASE ... END AS label             -- a new column
    ORDER BY CASE ... END                      -- a custom sort order
    GROUP BY label                             -- buckets (DuckDB allows the alias)
    SUM(CASE WHEN ... THEN 1 ELSE 0 END)       -- conditional count
    SUM(CASE WHEN ... THEN amount ELSE 0 END)  -- conditional sum
    UPDATE t SET col = CASE ... END            -- different change per row
    ```

    **Rules to remember**

    1. `WHEN` lines are checked top to bottom. The **first** true one wins.
    2. No match and no `ELSE` → `NULL`.
    3. Every branch must return the **same type**.
    4. Test `NULL` with `IS NULL`, and put that test first.

    ---

    ## Practice Exercises

    Write your answer in the empty cell below, then open the solution
    to check it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "1. Label each order by quantity: 1 → 'Single', 2 to 4 → 'Few', 5 or more → 'Bulk'.": mo.md("""
        ```sql
        SELECT order_id,
               quantity,
               CASE
                   WHEN quantity = 1 THEN 'Single'
                   WHEN quantity <= 4 THEN 'Few'
                   ELSE 'Bulk'
               END AS size_label
        FROM orders
        ORDER BY order_id;
        ```
        11 rows. Orders 103 (10 units) and 108 (5 units) are `Bulk`.
        """),
        "2. For each category, count products under $100 and products $100 or more, in one row per category.": mo.md("""
        ```sql
        SELECT category,
               SUM(CASE WHEN price < 100  THEN 1 ELSE 0 END) AS under_100,
               SUM(CASE WHEN price >= 100 THEN 1 ELSE 0 END) AS from_100_up
        FROM products
        GROUP BY category
        ORDER BY category;
        ```
        Electronics 2 / 2, Furniture 1 / 1, Office 2 / 0.
        """),
        "3. List all products with sold-out items first, then unknown stock, then everything else. Inside each group, sort by name.": mo.md("""
        ```sql
        SELECT product_name, stock
        FROM products
        ORDER BY CASE
                     WHEN stock = 0     THEN 1
                     WHEN stock IS NULL THEN 2
                     ELSE 3
                 END,
                 product_name;
        ```
        Desk Chair, then Pen Pack, then Bookshelf, Headphones, Laptop, ...
        """),
        "4. Add a column is_final: 'Yes' if the order is shipped, cancelled, or returned; 'No' if it is pending.": mo.md("""
        ```sql
        SELECT order_id,
               status,
               CASE
                   WHEN status IN ('shipped', 'cancelled', 'returned') THEN 'Yes'
                   ELSE 'No'
               END AS is_final
        FROM orders
        ORDER BY order_id;
        ```
        Only orders 102 and 111 are `No`.
        """),
        "5. For each month of 2026, show the number of orders and the number of shipped orders. (Hint: MONTH(order_date).)": mo.md("""
        ```sql
        SELECT MONTH(order_date) AS order_month,
               COUNT(*) AS orders,
               SUM(CASE WHEN status = 'shipped' THEN 1 ELSE 0 END) AS shipped
        FROM orders
        GROUP BY order_month
        ORDER BY order_month;
        ```
        4 rows: month 1 → 2 / 1, month 2 → 3 / 2, month 3 → 5 / 3, month 4 → 1 / 0.
        """),
    })
    return


@app.cell
def _(con):
    con.execute("""
    -- Your answer here. Replace this query with your own.
    SELECT 'Write your query here' AS hint
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    ## Summary

    - `CASE` is SQL's **if-then-else**. It gives back **one value per row**.
    - Write it as `CASE WHEN ... THEN ... ELSE ... END AS name`.
    - The **first** true `WHEN` wins, so order matters.
    - Without `ELSE`, unmatched rows become `NULL`.
    - Use the long form for ranges and `NULL` checks; the short form
      for simple "equals" lookups.
    - `CASE` works in `SELECT`, `ORDER BY`, `GROUP BY`, inside `SUM`
      and `COUNT`, and in `UPDATE`.
    - `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` is the classic way to
      count several things side by side in one report.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
