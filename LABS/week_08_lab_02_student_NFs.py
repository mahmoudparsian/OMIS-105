import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # OMIS 105 — Week 08: Database Design & Normalization
    ## Lab 2 — 1NF and 2NF with DuckDB, step by step · Student

    Today you learn **how to normalize a table with DuckDB**, one small step at a time.

    | Part | What you do | Data |
    |---|---|---|
    | **Part 1 — Learn 1NF** | Read and run. Nothing to write. | 🥐 Bronco Bakery |
    | **Part 2 — Learn 2NF** | Read and run. Nothing to write. | 🥐 Bronco Bakery |
    | **Part 3 — Your turn** | Q1–Q11 (+ a bonus). Use the same steps on new data. | 📚 Bronco Campus Bookstore |

    **How to work:** run each cell from top to bottom. In Part 1 and Part 2, read the text, **predict** the result, then look at the output.
    In Part 3, write your SQL where you see `-- YOUR SQL HERE`. Each Part 3 question says which Part 1–2 step to copy. 🔮 = predict first · ✍️ = explain in words · 🐞 = find the bug.

    ### Words you need today

    | Word | Plain meaning |
    |---|---|
    | **primary key** | the column (or columns) that point to **exactly one row** |
    | **composite key** | a primary key made of **two or more** columns, like `(order_id, product)` |
    | **A → B** ("A decides B") | if you know A, you know B. Example: `order_id → customer` — one order has one customer. |
    | **partial dependency** | a column that is decided by only **part** of a composite key |

    ### The two rules

    - **1NF:** one value per cell · no repeating groups (`phone_1`, `phone_2`, …) · a primary key
    - **2NF:** the table is in 1NF, **and** every non-key column needs the **whole** key (no partial dependencies)
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 1 — Learn 1NF with DuckDB 🥐

    **Bronco Bakery** writes every order on one line. The `items` cell holds the whole basket:

    | order_id | order_date | customer | items |
    |---|---|---|---|
    | 101 | 2026-11-02 | Ana | Croissant x2, Muffin x1 |

    What is wrong?

    1. One cell holds a **list** (two items). → breaks *one value per cell*.
    2. Each item hides **two facts**: the product (`Croissant`) and the quantity (`2`). We cannot `SUM` a quantity that is glued to a word.

    **Goal:** one row per order **per product**, with `product` and `quantity` in their own columns:

    | order_id | order_date | customer | product | quantity |
    |---|---|---|---|---|
    | 101 | 2026-11-02 | Ana | Croissant | 2 |
    | 101 | 2026-11-02 | Ana | Muffin | 1 |

    We get there in **4 small steps**. Run the cell below to create the table.
    """)
    return


@app.cell
def _(mo):
    bakery_orders_raw = mo.sql(
        f"""
        CREATE OR REPLACE TABLE bakery_orders_raw AS
        SELECT * FROM (
          VALUES
            (101, DATE '2026-11-02', 'Ana', 'Croissant x2, Muffin x1'),
            (102, DATE '2026-11-02', 'Ben', 'Bagel x3'),
            (103, DATE '2026-11-03', 'Ana', 'Muffin x2, Bagel x1, Croissant x1'),
            (104, DATE '2026-11-04', 'Cai', 'Croissant x4')
        ) AS t(order_id, order_date, customer, items);

        SELECT * FROM bakery_orders_raw ORDER BY order_id;
        """
    )
    return (bakery_orders_raw,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1 — `STRING_SPLIT`: turn the text into a list

    `STRING_SPLIT(items, ', ')` cuts the text at every `', '` (comma **and** space) and returns a **list**.
    DuckDB shows a list in square brackets: `[Croissant x2, Muffin x1]`. Its type is `VARCHAR[]` (a list of text).

    `LEN(list)` counts the elements of the list.

    🔮 **Predict:** how many items does order 103 have? How many items in all 4 orders together?
    """)
    return


@app.cell
def _(bakery_orders_raw, mo):
    _step1 = mo.sql(
        f"""
        SELECT order_id,
               items,
               STRING_SPLIT(items, ', ')      AS item_list,
               LEN(STRING_SPLIT(items, ', ')) AS n_items
        FROM bakery_orders_raw
        ORDER BY order_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What you see:** order 103 has 3 items; together 2 + 1 + 3 + 1 = **7 items**.
    So after the split we expect **7 rows**. Always count *before* you split — then you can check your result.

    ## Step 2 — `UNNEST`: one row per list element

    `UNNEST(list)` takes a list and gives back **one row per element**. The other columns (`order_id`, `order_date`, `customer`) are **copied** into every new row.

    ```
    order 101  [Croissant x2, Muffin x1]   ──UNNEST──►   101 | Croissant x2
                                                          101 | Muffin x1
    ```

    🔮 **Predict:** 4 rows go in. How many rows come out?
    """)
    return


@app.cell
def _(bakery_orders_raw, mo):
    _step2 = mo.sql(
        f"""
        SELECT order_id, order_date, customer,
               UNNEST(STRING_SPLIT(items, ', ')) AS item
        FROM bakery_orders_raw;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **7 rows** — the number we predicted in Step 1. ✅ Every cell now holds **one** item.

    But `item` still glues two facts together (`Croissant x2`). Let's cut it.

    ## Step 3 — `SPLIT_PART` + `CAST`: one fact per column

    `SPLIT_PART(text, separator, n)` cuts the text at the separator and returns **piece number n**:

    | Expression | Result |
    |---|---|
    | `SPLIT_PART('Croissant x2', ' x', 1)` | `Croissant` |
    | `SPLIT_PART('Croissant x2', ' x', 2)` | `2` (still text!) |

    `CAST(… AS INTEGER)` turns the text `'2'` into the **number** 2, so we can `SUM` it later.

    We build on Step 2 with a **CTE** (`WITH step2 AS (…)`, Week 7): the CTE is Step 2, the outer `SELECT` is Step 3. Step on top of step.
    """)
    return


@app.cell
def _(bakery_orders_raw, mo):
    _step3 = mo.sql(
        f"""
        WITH step2 AS (
            SELECT order_id, order_date, customer,
                   UNNEST(STRING_SPLIT(items, ', ')) AS item
            FROM bakery_orders_raw
        )
        SELECT order_id, order_date, customer,
               SPLIT_PART(item, ' x', 1)                  AS product,
               CAST(SPLIT_PART(item, ' x', 2) AS INTEGER) AS quantity
        FROM step2
        ORDER BY order_id, product;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look at the column types: `product` is `varchar`, `quantity` is `int32` (an integer). One value per cell, one fact per column. ✅

    ## Step 4 — Find the primary key, then let DuckDB guard it

    **4a. Find the key.** One `order_id` now has many rows, so `order_id` alone is **not** a key.
    Try the pair `(order_id, product)`. The test: group by the candidate key and look for groups with **more than one** row.

    > **Key test:** `GROUP BY candidate_key HAVING COUNT(*) > 1` → **0 rows** means the candidate is unique. ✅

    (We reuse Step 3's query as a CTE called `step3`.)
    """)
    return


@app.cell
def _(bakery_orders_raw, mo):
    _step4a = mo.sql(
        f"""
        WITH step2 AS (
            SELECT order_id, order_date, customer,
                   UNNEST(STRING_SPLIT(items, ', ')) AS item
            FROM bakery_orders_raw
        ),
        step3 AS (
            SELECT order_id, order_date, customer,
                   SPLIT_PART(item, ' x', 1)                  AS product,
                   CAST(SPLIT_PART(item, ' x', 2) AS INTEGER) AS quantity
            FROM step2
        )
        SELECT order_id, product, COUNT(*) AS copies
        FROM step3
        GROUP BY order_id, product
        HAVING COUNT(*) > 1;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **0 rows** → `(order_id, product)` is unique. It is our composite primary key.

    **4b. 🦆 DuckDB power: store it with a real `PRIMARY KEY`.** Write the table's columns and its key first (`CREATE TABLE`), then fill it with `INSERT INTO … SELECT` (Step 3's query).
    From now on, DuckDB **refuses** any row that would repeat a key. If we tried to add a second `(101, 'Croissant')` row, DuckDB would stop with:

    ```
    Constraint Error: Duplicate key "order_id: 101, product: Croissant" violates primary key constraint.
    ```

    A data check you write once, and DuckDB runs it forever.
    """)
    return


@app.cell
def _(bakery_orders_raw, mo):
    order_lines_1nf = mo.sql(
        f"""
        CREATE OR REPLACE TABLE order_lines_1nf (
            order_id   INTEGER,
            order_date DATE,
            customer   VARCHAR,
            product    VARCHAR,
            quantity   INTEGER,
            PRIMARY KEY (order_id, product)
        );

        INSERT INTO order_lines_1nf
        WITH step2 AS (
            SELECT order_id, order_date, customer,
                   UNNEST(STRING_SPLIT(items, ', ')) AS item
            FROM bakery_orders_raw
        )
        SELECT order_id, order_date, customer,
               SPLIT_PART(item, ' x', 1),
               CAST(SPLIT_PART(item, ' x', 2) AS INTEGER)
        FROM step2;

        SELECT * FROM order_lines_1nf ORDER BY order_id, product;
        """
    )
    return (order_lines_1nf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    🎉 `order_lines_1nf` is in **1NF**: one value per cell, no lists, and a primary key that DuckDB enforces.

    ## The other 1NF problem: repeating groups (`phone_1`, `phone_2`, `phone_3`)

    The bakery also keeps a contact sheet. Each customer has **up to 3** phone numbers, in 3 columns:
    """)
    return


@app.cell
def _(mo):
    customers_raw = mo.sql(
        f"""
        CREATE OR REPLACE TABLE customers_raw AS
        SELECT * FROM (
          VALUES
            ('Ana', '408-555-0101', '408-555-0102', NULL),
            ('Ben', '650-555-0201', NULL,           NULL),
            ('Cai', '408-555-0301', '669-555-0302', '650-555-0303')
        ) AS t(customer, phone_1, phone_2, phone_3);

        SELECT * FROM customers_raw ORDER BY customer;
        """
    )
    return (customers_raw,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Why is this bad? `phone_1`, `phone_2`, `phone_3` are the **same kind of fact** in three columns (a *repeating group*).

    - To find who owns `669-555-0302`, you must search **three** columns.
    - Ben wastes two `NULL` cells.
    - A 4th phone number means **changing the table**.

    **Goal:** one row per customer **per phone**: `customer_phones(customer, phone)`.

    **Way 1 — `UNION ALL` (works in every database).** One `SELECT` per column, stacked on top of each other. Skip the `NULL`s.

    🔮 **Predict:** how many rows? (Count the phone numbers that are not `NULL`.)
    """)
    return


@app.cell
def _(customers_raw, mo):
    _way1 = mo.sql(
        f"""
        SELECT customer, phone_1 AS phone FROM customers_raw WHERE phone_1 IS NOT NULL
        UNION ALL
        SELECT customer, phone_2 AS phone FROM customers_raw WHERE phone_2 IS NOT NULL
        UNION ALL
        SELECT customer, phone_3 AS phone FROM customers_raw WHERE phone_3 IS NOT NULL
        ORDER BY customer, phone;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **6 rows** (Ana 2, Ben 1, Cai 3).

    **Way 2 — 🦆 DuckDB power: `UNPIVOT`.** Same result, one step. `UNPIVOT` turns **columns into rows**:

    - `ON phone_1, phone_2, phone_3` — the columns to turn into rows
    - `NAME phone_slot` — a new column that remembers where the value came from (`phone_1`, …)
    - `VALUE phone` — a new column that holds the value
    - `NULL` values are **dropped for you**

    We keep only `customer` and `phone`, and store the result with its primary key `(customer, phone)`.
    """)
    return


@app.cell
def _(customers_raw, mo):
    customer_phones = mo.sql(
        f"""
        CREATE OR REPLACE TABLE customer_phones (
            customer VARCHAR,
            phone    VARCHAR,
            PRIMARY KEY (customer, phone)
        );

        INSERT INTO customer_phones
        SELECT customer, phone
        FROM (
            UNPIVOT customers_raw
            ON phone_1, phone_2, phone_3
            INTO NAME phone_slot VALUE phone
        );

        SELECT * FROM customer_phones ORDER BY customer, phone;
        """
    )
    return (customer_phones,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✅ 1NF recipe (keep this!)

    | Problem you see | DuckDB tool | Step |
    |---|---|---|
    | a list in one cell (`'Croissant x2, Muffin x1'`) | `STRING_SPLIT` → list, `LEN` to count, `UNNEST` → rows | 1, 2 |
    | two facts glued in one value (`'Croissant x2'`) | `SPLIT_PART`, then `CAST(… AS INTEGER)` | 3 |
    | repeating columns (`phone_1`, `phone_2`, …) | `UNPIVOT` (or `UNION ALL`) | — |
    | no primary key | key test `GROUP BY … HAVING COUNT(*) > 1` = 0 rows, then `PRIMARY KEY (…)` | 4 |

    **But wait.** Look at `order_lines_1nf` again: order 103's date and customer (`2026-11-03`, `Ana`) are stored **3 times**.
    That breaks **no** 1NF rule — every cell has one value. It is **redundancy**, and it is exactly what **2NF** fixes. → Part 2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 2 — Learn 2NF with DuckDB 🥐

    The bakery's cash register prints a sales report. It is the same 4 orders, plus each product's `category` and `unit_price`:
    """)
    return


@app.cell
def _(mo):
    bakery_sales = mo.sql(
        f"""
        CREATE OR REPLACE TABLE bakery_sales AS
        SELECT * FROM (
          VALUES
            (101, 'Croissant', DATE '2026-11-02', 'Ana', 'Pastry', 3.50, 2),
            (101, 'Muffin',    DATE '2026-11-02', 'Ana', 'Pastry', 3.00, 1),
            (102, 'Bagel',     DATE '2026-11-02', 'Ben', 'Bread',  2.50, 3),
            (103, 'Muffin',    DATE '2026-11-03', 'Ana', 'Pastry', 3.00, 2),
            (103, 'Bagel',     DATE '2026-11-03', 'Ana', 'Bread',  2.50, 1),
            (103, 'Croissant', DATE '2026-11-03', 'Ana', 'Pastry', 3.50, 1),
            (104, 'Croissant', DATE '2026-11-04', 'Cai', 'Pastry', 3.50, 4)
        ) AS t(order_id, product, order_date, customer, category, unit_price, quantity);

        SELECT * FROM bakery_sales ORDER BY order_id, product;
        """
    )
    return (bakery_sales,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This table **is** in 1NF (one value per cell, no repeating groups). Is it in 2NF? We find out in **5 steps**:

    1. Find the primary key.
    2. Test which column depends on which part of the key.
    3. See the problem with your own eyes.
    4. Split the table.
    5. Prove that nothing was lost.

    ## Step 1 — Find the primary key

    Count the rows, and count the different values of each candidate:
    """)
    return


@app.cell
def _(bakery_sales, mo):
    _p2_step1 = mo.sql(
        f"""
        SELECT COUNT(*)                   AS total_rows,
               COUNT(DISTINCT order_id)   AS different_order_ids,
               COUNT(DISTINCT product)    AS different_products
        FROM bakery_sales;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    7 rows, but only 4 order ids and 3 products → neither column alone can point to one row.
    Use the **key test** from Part 1 on the pair:
    """)
    return


@app.cell
def _(bakery_sales, mo):
    _p2_step1b = mo.sql(
        f"""
        SELECT order_id, product, COUNT(*) AS copies
        FROM bakery_sales
        GROUP BY order_id, product
        HAVING COUNT(*) > 1;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **0 rows** → the primary key is the composite key **`(order_id, product)`**.
    2NF only matters when the key has **two or more** columns — so this table needs the 2NF check.

    ## Step 2 — The dependency test

    For every **non-key** column (`order_date`, `customer`, `category`, `unit_price`, `quantity`) we ask:
    *does it need the whole key, or only **part** of it?*

    > **Dependency test:** does `A` decide `B`?
    > `GROUP BY A HAVING COUNT(DISTINCT B) > 1`
    > → **0 rows**: every A has only one B, so **A → B** ✅
    > → **some rows**: those A's have several B's, so A does **not** decide B ❌

    **Test 1:** does `order_id` decide `customer`? (Can one order have two customers?)
    """)
    return


@app.cell
def _(bakery_sales, mo):
    _test1 = mo.sql(
        f"""
        SELECT order_id, COUNT(DISTINCT customer) AS customers
        FROM bakery_sales
        GROUP BY order_id
        HAVING COUNT(DISTINCT customer) > 1;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **0 rows** → `order_id → customer`. The customer needs only **part** of the key (`order_id`). That is a **partial dependency**. ❌ for 2NF.

    **Test 2:** does `product` decide `quantity`? (Is a croissant always bought 2 at a time?)
    """)
    return


@app.cell
def _(bakery_sales, mo):
    _test2 = mo.sql(
        f"""
        SELECT product, COUNT(DISTINCT quantity) AS quantities
        FROM bakery_sales
        GROUP BY product
        HAVING COUNT(DISTINCT quantity) > 1
        ORDER BY product;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **3 rows** → no. A croissant was bought 2, 1, and 4 at a time. `product` does **not** decide `quantity`.

    ### 🦆 DuckDB power: test **every** column at once with `COLUMNS(*)`

    Writing one test per column is slow. `COLUMNS(* EXCLUDE (order_id, product))` means *"every column except the key columns"*.
    DuckDB repeats the expression for each of them — one query, a whole scoreboard.

    The inner query counts, **for each order**, how many different values each column has.
    The outer query takes the **largest** count (`MAX`). **1 = always one value = depends on `order_id`.**
    """)
    return


@app.cell
def _(bakery_sales, mo):
    _board_order = mo.sql(
        f"""
        SELECT MAX(COLUMNS(* EXCLUDE (order_id)))
        FROM (
            SELECT order_id,
                   COUNT(DISTINCT COLUMNS(* EXCLUDE (order_id, product)))
            FROM bakery_sales
            GROUP BY order_id
        );
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `order_date` = 1 and `customer` = 1 → both depend on **`order_id`** alone.

    The same scoreboard for the other part of the key, `product`:
    """)
    return


@app.cell
def _(bakery_sales, mo):
    _board_product = mo.sql(
        f"""
        SELECT MAX(COLUMNS(* EXCLUDE (product)))
        FROM (
            SELECT product,
                   COUNT(DISTINCT COLUMNS(* EXCLUDE (order_id, product)))
            FROM bakery_sales
            GROUP BY product
        );
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `category` = 1 and `unit_price` = 1 → both depend on **`product`** alone.

    ### Read the two scoreboards together

    | Non-key column | Decided by `order_id` alone? | Decided by `product` alone? | Kind of dependency |
    |---|---|---|---|
    | `order_date` | ✅ (1) | ❌ (3) | **partial** (`order_id`) |
    | `customer` | ✅ (1) | ❌ (2) | **partial** (`order_id`) |
    | `category` | ❌ (2) | ✅ (1) | **partial** (`product`) |
    | `unit_price` | ❌ (3) | ✅ (1) | **partial** (`product`) |
    | `quantity` | ❌ (2) | ❌ (3) | **full** — needs *this* order **and** *this* product |

    Four partial dependencies → `bakery_sales` is **not in 2NF**.

    ⚠️ **Data can prove "no", but not "yes".** A 1 in a tiny table could be luck. Always confirm with the business rule:
    "one order belongs to one customer" ✔️, "each product has one price" ✔️. Here the data and the rules agree.

    ## Step 3 — See the problem: an update anomaly

    Croissants now cost **3.75**. A busy clerk updates only **one** of the three croissant rows.
    We do it on a **copy**, so the real table stays clean:
    """)
    return


@app.cell
def _(bakery_sales, mo):
    sales_copy = mo.sql(
        f"""
        CREATE OR REPLACE TABLE sales_copy AS
        SELECT * FROM bakery_sales;

        UPDATE sales_copy
        SET unit_price = 3.75
        WHERE product = 'Croissant' AND order_id = 104;

        SELECT product,
               COUNT(*)                   AS rows_stored,
               COUNT(DISTINCT unit_price) AS different_prices,
               MIN(unit_price)            AS low_price,
               MAX(unit_price)            AS high_price
        FROM sales_copy
        GROUP BY product
        ORDER BY product;
        """
    )
    return (sales_copy,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The croissant price was stored **3 times**, so now the data **contradicts itself**: 3.50 *and* 3.75. Which one is true? Nobody knows.

    The cause is the partial dependency: `unit_price` depends on `product` only, but it is stored once **per order line**.

    ## Step 4 — Split the table

    > **2NF rule of thumb:** move each partial dependency into its **own table**, where that part of the key is the **whole** key.

    | New table | Primary key | Columns | Why |
    |---|---|---|---|
    | `orders` | `order_id` | `order_date`, `customer` | they depend on `order_id` |
    | `products` | `product` | `category`, `unit_price` | they depend on `product` |
    | `order_items` | `(order_id, product)` | `quantity` | it depends on the **whole** key |

    `SELECT DISTINCT` keeps **one** copy of each fact. The `PRIMARY KEY` makes DuckDB check that it really is one copy:
    if order 101 had two different customers, `INSERT` would fail with a *Constraint Error*.
    """)
    return


@app.cell
def _(bakery_sales, mo):
    orders = mo.sql(
        f"""
        CREATE OR REPLACE TABLE orders (
            order_id   INTEGER PRIMARY KEY,
            order_date DATE,
            customer   VARCHAR
        );

        INSERT INTO orders
        SELECT DISTINCT order_id, order_date, customer
        FROM bakery_sales;

        SELECT * FROM orders ORDER BY order_id;
        """
    )
    return (orders,)


@app.cell
def _(bakery_sales, mo):
    products = mo.sql(
        f"""
        CREATE OR REPLACE TABLE products (
            product    VARCHAR PRIMARY KEY,
            category   VARCHAR,
            unit_price DECIMAL(5, 2)
        );

        INSERT INTO products
        SELECT DISTINCT product, category, unit_price
        FROM bakery_sales;

        SELECT * FROM products ORDER BY product;
        """
    )
    return (products,)


@app.cell
def _(bakery_sales, mo):
    order_items = mo.sql(
        f"""
        CREATE OR REPLACE TABLE order_items (
            order_id INTEGER,
            product  VARCHAR,
            quantity INTEGER,
            PRIMARY KEY (order_id, product)
        );

        INSERT INTO order_items
        SELECT order_id, product, quantity
        FROM bakery_sales;

        SELECT * FROM order_items ORDER BY order_id, product;
        """
    )
    return (order_items,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    7 rows became **4 + 3 + 7** rows, but look what disappeared: Ana's order 103 date is stored **once**, the croissant price is stored **once**.
    Now a price change is **one** `UPDATE` of **one** row — the contradiction in Step 3 can't happen any more.

    Is each table in 2NF?

    - `orders` and `products` have a **one-column** key → no "part of the key" exists → 2NF automatically. ✅
    - `order_items`: its only non-key column, `quantity`, needs the **whole** key. ✅

    ## Step 5 — Prove that nothing was lost

    A good split is **lossless**: `JOIN` the tables back together and you get **exactly** the old table.

    **5a. Count** the rows after the JOIN (we expect 7):
    """)
    return


@app.cell
def _(order_items, orders, products, mo):
    _p2_step5a = mo.sql(
        f"""
        SELECT COUNT(*) AS rows_after_join
        FROM order_items oi
        INNER JOIN orders   o ON oi.order_id = o.order_id
        INNER JOIN products p ON oi.product  = p.product;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **5b. 🦆 Compare every row with `EXCEPT`.** `A EXCEPT B` returns the rows of A that are **not** in B.
    We check both directions — old minus new, and new minus old. **Both must be 0.**
    (The JOIN lists the columns in the **same order** as `bakery_sales`, so the rows can be compared.)
    """)
    return


@app.cell
def _(bakery_sales, order_items, orders, products, mo):
    _p2_step5b = mo.sql(
        f"""
        WITH rebuilt AS (
            SELECT oi.order_id, oi.product, o.order_date, o.customer,
                   p.category, p.unit_price, oi.quantity
            FROM order_items oi
            INNER JOIN orders   o ON oi.order_id = o.order_id
            INNER JOIN products p ON oi.product  = p.product
        )
        SELECT 'old minus new' AS direction,
               COUNT(*) AS missing_rows
        FROM (SELECT * FROM bakery_sales EXCEPT SELECT * FROM rebuilt)
        UNION ALL
        SELECT 'new minus old',
               COUNT(*)
        FROM (SELECT * FROM rebuilt EXCEPT SELECT * FROM bakery_sales);
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    0 and 0 → the three tables hold **exactly** the same information as `bakery_sales`, with no repeats. 🎉

    ### ✅ 2NF recipe (keep this!)

    | Step | Question | DuckDB tool |
    |---|---|---|
    | 1 | What is the primary key? | `COUNT(DISTINCT …)`, then `GROUP BY key HAVING COUNT(*) > 1` = 0 rows |
    | 2 | Which column depends on which part of the key? | `GROUP BY part HAVING COUNT(DISTINCT col) > 1` = 0 rows — or all at once with `COLUMNS(*)` |
    | 3 | What goes wrong? | update a **copy**, then count the different values |
    | 4 | Split | one table per key part: `CREATE TABLE … PRIMARY KEY` + `INSERT … SELECT DISTINCT` |
    | 5 | Nothing lost? | `JOIN` back, `COUNT(*)`, `EXCEPT` both ways = 0 |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 3 — Your turn 📚 Bronco Campus Bookstore

    The campus bookstore sells textbooks to students. You get three tables. Run the three cells below first.

    - `book_orders_raw` — one row per order, the books in **one** cell (Part A, 1NF)
    - `student_emails_raw` — up to 3 email addresses per student, in 3 columns (Part A, 1NF)
    - `bookstore_sales` — the store's sales report, already in 1NF (Part B, 2NF)
    """)
    return


@app.cell
def _(books, mo):
    book_orders_raw = mo.sql(
        f"""
        CREATE OR REPLACE TABLE book_orders_raw AS
        SELECT * FROM (
          VALUES
            (1, DATE '2026-10-05', 'Lily', 'SQL Basics x1, Data Viz x2'),
            (2, DATE '2026-10-05', 'Raj',  'Python 101 x1'),
            (3, DATE '2026-10-06', 'Sara', 'SQL Basics x2, Python 101 x1, Stats Made Easy x1'),
            (4, DATE '2026-10-07', 'Lily', 'Stats Made Easy x1'),
            (5, DATE '2026-10-08', 'Tom',  'Data Viz x1, SQL Basics x1')
        ) AS t(order_id, order_date, student, books);

        SELECT * FROM book_orders_raw ORDER BY order_id;
        """
    )
    return (book_orders_raw,)


@app.cell
def _(mo):
    student_emails_raw = mo.sql(
        f"""
        CREATE OR REPLACE TABLE student_emails_raw AS
        SELECT * FROM (
          VALUES
            ('Lily', 'lily@scu.edu', 'lily.k@gmail.com', NULL),
            ('Raj',  'raj@scu.edu',  NULL,               NULL),
            ('Sara', 'sara@scu.edu', 'sara.m@yahoo.com', 'sara.work@outlook.com'),
            ('Tom',  'tom@scu.edu',  NULL,               NULL)
        ) AS t(student, email_1, email_2, email_3);

        SELECT * FROM student_emails_raw ORDER BY student;
        """
    )
    return (student_emails_raw,)


@app.cell
def _(mo):
    bookstore_sales = mo.sql(
        f"""
        CREATE OR REPLACE TABLE bookstore_sales AS
        SELECT * FROM (
          VALUES
            (1, 'B01', DATE '2026-10-05', 'Lily', 'SQL Basics',      40, 1),
            (1, 'B02', DATE '2026-10-05', 'Lily', 'Data Viz',        35, 2),
            (2, 'B03', DATE '2026-10-05', 'Raj',  'Python 101',      45, 1),
            (3, 'B01', DATE '2026-10-06', 'Sara', 'SQL Basics',      40, 2),
            (3, 'B03', DATE '2026-10-06', 'Sara', 'Python 101',      45, 1),
            (3, 'B04', DATE '2026-10-06', 'Sara', 'Stats Made Easy', 30, 1),
            (4, 'B04', DATE '2026-10-07', 'Lily', 'Stats Made Easy', 30, 1),
            (5, 'B02', DATE '2026-10-08', 'Tom',  'Data Viz',        35, 1),
            (5, 'B01', DATE '2026-10-08', 'Tom',  'SQL Basics',      40, 1)
        ) AS t(order_id, book_code, order_date, student, title, price, quantity);

        SELECT * FROM bookstore_sales ORDER BY order_id, book_code;
        """
    )
    return (bookstore_sales,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part A — 1NF (`book_orders_raw`, `student_emails_raw`)

    ### Q1. 🔮 Look before you split (copy Part 1, Step 1)

    Show each `order_id`, the `books` cell as a list (`book_list`), and the number of books in it (`n_books`). Order by `order_id`.

    🔮 **Predict first** (write it in the comment): after the split, how many rows will there be in all?
    """)
    return


@app.cell
def _(mo):
    q1 = mo.sql(
        f"""
        -- Predict: ___ rows after the split
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q2. Split the books into rows and columns (copy Part 1, Steps 2 and 3)

    Write **one** query with a CTE that returns `order_id`, `order_date`, `student`, `title`, `quantity` — one row per order **per book**.
    `title` is text, `quantity` must be an **integer**. Order by `order_id`, `title`.

    Hint: the separator between title and quantity is `' x'` (space + x).
    """)
    return


@app.cell
def _(mo):
    q2 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q3. Store it with a primary key (copy Part 1, Step 4)

    1. Create the table `book_lines_1nf(order_id, order_date, student, title, quantity)` with `PRIMARY KEY (order_id, title)`.
    2. Fill it with `INSERT INTO book_lines_1nf` + your Q2 query (without `ORDER BY`).
    3. Show the table, ordered by `order_id`, `title`.

    ✅ **Self-check:** 9 rows. (If `INSERT` fails with a *Constraint Error*, your key is wrong.)

    ✍️ **Explain it** (in the comment at the end of your cell): `book_lines_1nf` is in 1NF. What is still stored **more than once**?
    """)
    return


@app.cell
def _(mo):
    q_book_lines_1nf = mo.sql(
        f"""
        -- YOUR SQL HERE
        -- Explain:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q4. 🔮 Repeating group → rows (copy Part 1, `UNPIVOT`)

    `student_emails_raw` has a repeating group: `email_1`, `email_2`, `email_3`.
    Create `student_emails(student, email)` with `PRIMARY KEY (student, email)`, fill it with `UNPIVOT`, and show it ordered by `student`, `email`.

    🔮 **Predict first:** how many rows?
    """)
    return


@app.cell
def _(mo):
    q_student_emails = mo.sql(
        f"""
        -- Predict: ___ rows
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part B — 2NF (`bookstore_sales`)

    ### Q5. Find the primary key (copy Part 2, Step 1)

    1. Show `total_rows`, `different_order_ids`, `different_book_codes` of `bookstore_sales`.
    2. Run the key test on `(order_id, book_code)`.

    ✍️ **Explain it:** what is the primary key, and why is neither column alone enough?
    """)
    return


@app.cell
def _(mo):
    q5 = mo.sql(
        f"""
        -- 1. counts
        -- YOUR SQL HERE
        """
    )
    return


@app.cell
def _(mo):
    q5b = mo.sql(
        f"""
        -- 2. key test
        -- YOUR SQL HERE
        -- Explain:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q6. The dependency scoreboards (copy Part 2, Step 2)

    Write the **two** `COLUMNS(*)` scoreboards for `bookstore_sales`:

    1. one grouped by `order_id`
    2. one grouped by `book_code`

    (Remember to exclude **both** key columns inside `COUNT(DISTINCT COLUMNS(…))`.)
    """)
    return


@app.cell
def _(mo):
    q6a = mo.sql(
        f"""
        -- 1. scoreboard by order_id
        -- YOUR SQL HERE
        """
    )
    return


@app.cell
def _(mo):
    q6b = mo.sql(
        f"""
        -- 2. scoreboard by book_code
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q7. ✍️ Full or partial?

    Use your two scoreboards. For each **non-key** column, write **full** or **partial** (and which part of the key). Then answer: is `bookstore_sales` in 2NF?
    Write your answers in the text cell below.
    """)
    return


@app.cell
def _():
    q7_answer = """
    order_date :
    student    :
    title      :
    price      :
    quantity   :

    Is bookstore_sales in 2NF?
    """
    return (q7_answer,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q8. Split into three 2NF tables (copy Part 2, Step 4)

    Create each table with its `PRIMARY KEY`, fill it with `INSERT … SELECT` (use `DISTINCT` where a fact repeats), and show it:

    - `book_orders(order_id, order_date, student)` — key `order_id`
    - `books(book_code, title, price)` — key `book_code`
    - `book_order_lines(order_id, book_code, quantity)` — key `(order_id, book_code)`

    ✅ **Self-check:** 5, 4, and 9 rows.
    """)
    return


@app.cell
def _(mo):
    q_book_orders = mo.sql(
        f"""
        -- book_orders
        -- YOUR SQL HERE
        """
    )
    return


@app.cell
def _(mo):
    q_books = mo.sql(
        f"""
        -- books
        -- YOUR SQL HERE
        """
    )
    return


@app.cell
def _(mo):
    q_book_order_lines = mo.sql(
        f"""
        -- book_order_lines
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q9. Prove that nothing was lost (copy Part 2, Step 5)

    `JOIN` your three tables back together (columns in the **same order** as `bookstore_sales`) and use `EXCEPT` in **both** directions.
    Show `direction` and `missing_rows`.
    """)
    return


@app.cell
def _(mo):
    q9 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q10. 🐞 Debug it

    A classmate thought "every book has a quantity" and wrote:

    ```sql
    CREATE OR REPLACE TABLE books_v2 (
        book_code VARCHAR PRIMARY KEY,
        title     VARCHAR,
        price     INTEGER,
        quantity  INTEGER
    );

    INSERT INTO books_v2
    SELECT DISTINCT book_code, title, price, quantity
    FROM bookstore_sales;
    ```

    The `INSERT` fails: `Constraint Error: PRIMARY KEY or UNIQUE constraint violation: duplicate key …`

    1. Run **only** the `SELECT DISTINCT …` part. How many rows does it return, and which book codes appear twice?
    2. ✍️ **Explain it:** why does `quantity` not belong in `books`? (Use the words *full* or *partial*.)
    """)
    return


@app.cell
def _(mo):
    q10 = mo.sql(
        f"""
        -- YOUR SQL HERE
        -- Explain:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q11. Use your 2NF tables: sales per book

    Show each `title`, the number of copies sold (`copies`), and the money it brought in (`revenue` = quantity × price).
    Use `book_order_lines` and `books` (**not** `bookstore_sales`). Order by `revenue` (highest first), then `title`.
    """)
    return


@app.cell
def _(mo):
    q11 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🌟 Q12. Bonus (optional — only if you finish early)

    Show each `student`, their number of orders (`orders`), and how much they spent in all (`total_spent`). JOIN all three 2NF tables.
    Order by `total_spent` (highest first), then `student`.
    """)
    return


@app.cell
def _(mo):
    q12 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Exit Ticket — before you submit
    """)
    return


@app.cell
def _():
    exit_ticket = """
    1. One thing that clicked for you today:


    2. One step of the 1NF or 2NF recipe that is still fuzzy or confusing:
    """
    return (exit_ticket,)


if __name__ == "__main__":
    app.run()
