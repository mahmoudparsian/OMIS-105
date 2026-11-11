import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=":memory:")

    # The bakery's spreadsheet, exactly as the owner keeps it today
    con.execute(
        """
        CREATE OR REPLACE TABLE catering_sheet AS
        SELECT * FROM (VALUES
            (1001, DATE '2026-11-02', 'Ana Lopez',  'ana@scu.edu',  '408-555-0101, 408-555-0102',
             'Croissant',  12,  3.50, 'Coffee Box',    2, 18.00, NULL,         NULL, NULL),
            (1002, DATE '2026-11-03', 'Ben Okafor', 'ben@scu.edu',  '408-555-0201',
             'Bagel',      10,  2.75, 'Muffin',        6,  3.25, 'Coffee Box',    1, 18.00),
            (1003, DATE '2026-11-03', 'Ana Lopez',  'ana@scu.edu',  '408-555-0101, 408-555-0102',
             'Muffin',     12,  3.25, NULL,         NULL,  NULL, NULL,         NULL, NULL),
            (1004, DATE '2026-11-05', 'Chen Wei',   'chen@scu.edu', '408-555-0301, 650-555-0302',
             'Croissant',  24,  3.50, 'Bagel',        12,  2.75, 'Coffee Box',    3, 18.00),
            (1005, DATE '2026-11-06', 'Dana Patel', 'dana@scu.edu', '408-555-0401',
             'Fruit Tray',  2, 24.00, 'Coffee Box',    1, 18.00, NULL,         NULL, NULL),
            (1006, DATE '2026-11-07', 'Ben Okafor', 'ben@scu.edu',  '408-555-0201',
             'Croissant',   6,  3.50, NULL,         NULL,  NULL, NULL,         NULL, NULL)
        ) AS t(order_id, order_date, customer_name, customer_email, customer_phones,
               item_1, qty_1, price_1,
               item_2, qty_2, price_2,
               item_3, qty_3, price_3)
        """
    )
    return (con,)


@app.cell
def _(con, mo):
    def try_sql(sql):
        # Runs a statement that may break a rule, and shows what DuckDB says
        try:
            con.execute(sql)
            return mo.callout(mo.md("✅ **DuckDB accepted it.**"), kind="success")
        except duckdb_error() as e:
            return mo.callout(
                mo.md(f"❌ **DuckDB refused it:**\n\n`{e}`"), kind="danger"
            )

    def duckdb_error():
        import duckdb

        return duckdb.Error

    return (try_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 8 — Database Design, 1NF, and 2NF

    **OMIS 105 — Introduction to Database Management Systems**

    **The story.** *Mission Bakery* sells catering orders to campus offices:
    trays of croissants, bagels, muffins, coffee boxes, and fruit. The owner
    keeps every order in **one spreadsheet**. It worked when the bakery was
    small. Now there are mistakes: two prices for the same croissant, lost
    products, and phone numbers nobody can search.

    Today we **design** a better database for the bakery, then reach it step
    by step with **First Normal Form (1NF)** and **Second Normal Form (2NF)**.

    | Part | Topic | Session |
    |---|---|---|
    | 1 | Look at the spreadsheet | 1 |
    | 2 | Design first: entities, keys, relationships | 1 |
    | 3 | 1NF, rule 2: no repeating groups | 1 |
    | 4 | 1NF, rule 1: one value per cell | 1 |
    | 5 | 1NF, rule 3: a primary key | 1 |
    | 6 | Functional dependencies, checked with SQL | 2 |
    | 7 | Anomalies: why 1NF is not enough | 2 |
    | 8 | 2NF: split the table | 2 |
    | 9 | Prove it: nothing was lost, and the anomalies are gone | 2 |

    Run the cells from top to bottom. All data is created in the notebook,
    so no files are needed. The guides [`1nf_guide.md`](1nf_guide.md) and
    [`2nf_guide.md`](2nf_guide.md) cover the same rules with other examples.

    > 🧑‍🏫 **Instructor tip:** each "Ask the class" box hides its answer.
    > Ask first, wait for answers, then open it.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1. Look at the Spreadsheet

    The table `catering_sheet` is the owner's spreadsheet: **6 orders**,
    one row per order.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM catering_sheet
        ORDER BY order_id
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- 14 columns: look at the names
        DESCRIBE catering_sheet
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🙋 Ask the class: what looks wrong in this spreadsheet? (click for answers)": mo.md(
                r"""
                1. **Numbered columns:** `item_1`, `qty_1`, `price_1`, then
                   `item_2` …, then `item_3` … What happens when an office
                   orders **4** different items?
                2. **Many empty cells:** most orders have fewer than 3 items.
                3. **Two phone numbers in one cell:** `'408-555-0101, 408-555-0102'`.
                4. **The same facts again and again:** Ana's name, email, and
                   phones are in 2 rows; the Croissant price 3.50 is typed
                   in 3 places.
                5. **No key:** nothing stops two rows for order 1001.
                """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try simple questions on the spreadsheet

    **"Which orders include a Coffee Box?"** The answer can be in any of
    three columns, so the query must check all three:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT order_id, customer_name
        FROM catering_sheet
        WHERE item_1 = 'Coffee Box'
           OR item_2 = 'Coffee Box'
           OR item_3 = 'Coffee Box'
        ORDER BY order_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4 orders. If the owner adds `item_4` next month, this query silently
    misses Coffee Boxes in the new column.

    **"Whose phone number is 408-555-0102?"**
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT customer_name
        FROM catering_sheet
        WHERE customer_phones = '408-555-0102'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **0 rows** — but the number is in the data! No cell is *exactly*
    `'408-555-0102'`; it hides inside `'408-555-0101, 408-555-0102'`.
    `LIKE '%408-555-0102%'` would find it, but that is a workaround, not a
    design.

    > 💡 **Lesson:** when the design is wrong, simple questions need
    > complicated SQL — and the SQL can still be wrong.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2. Design First: Entities, Keys, Relationships

    Before we fix the spreadsheet, decide **what the database should look
    like**. Three questions:

    **1. What are the "things" (entities) the bakery keeps facts about?**
    Look for nouns in the business:

    | Entity | Facts about it (attributes) | What identifies one? (key) |
    |---|---|---|
    | **Customer** | name, email, phone numbers | `customer_email` |
    | **Order** | date, which customer | `order_id` |
    | **Product** | name, price | `product_name` |

    **2. How are they related?**

    - One customer places **many** orders; each order has **one** customer → **one-to-many (1:M)**
    - One order contains **many** products, and one product appears in
      **many** orders → **many-to-many (M:N)**
    - One customer can have **many** phone numbers → **1:M**

    **3. Where does each fact belong?** A many-to-many relationship always
    needs a **bridge table**. "How many croissants in order 1001?" is a fact
    about one order **and** one product together, so `quantity` lives in the
    bridge table `order_items`.

    > 🧑‍🏫 Draw this on the board before showing the diagram below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
        erDiagram
            CUSTOMERS ||--o{ ORDERS : places
            CUSTOMERS ||--o{ CUSTOMER_PHONES : has
            ORDERS ||--|{ ORDER_ITEMS : contains
            PRODUCTS ||--o{ ORDER_ITEMS : "appears in"
            CUSTOMERS {
                varchar customer_email PK
                varchar customer_name
            }
            CUSTOMER_PHONES {
                varchar customer_email PK
                varchar phone PK
            }
            ORDERS {
                int order_id PK
                date order_date
                varchar customer_email FK
            }
            ORDER_ITEMS {
                int order_id PK
                varchar product_name PK
                int quantity
            }
            PRODUCTS {
                varchar product_name PK
                decimal unit_price
            }
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is **where we are heading**. Normalization is the step-by-step
    method that gets us from the messy spreadsheet to this design, and lets
    us **prove** each step with SQL.

    Today we do **1NF** and **2NF**. The last step (3NF, a separate
    `customers` table) comes at the end of the 2NF part, as a preview.

    | Normal form | The rule, in one line |
    |---|---|
    | **1NF** | One value per cell, no repeating groups, and a primary key |
    | **2NF** | 1NF, and every non-key column depends on the **whole** key |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3. 1NF, Rule 2: No Repeating Groups

    `(item_1, qty_1, price_1)`, `(item_2, qty_2, price_2)`,
    `(item_3, qty_3, price_3)` are the **same kind of data three times**.
    That is a **repeating group**.

    **Fix:** turn the columns into **rows** — one row per *order line*
    (one product in one order). We write one `SELECT` per group and stack
    them with `UNION ALL`, skipping the empty slots.

    We also declare the table with a **primary key** now. Part 5 explains
    why `(order_id, product_name)` is the right one.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE order_lines (
            order_id       INTEGER,
            order_date     DATE,
            customer_name  VARCHAR,
            customer_email VARCHAR,
            product_name   VARCHAR,
            unit_price     DECIMAL(6, 2),
            quantity       INTEGER,
            PRIMARY KEY (order_id, product_name)
        )
        """
    )
    con.execute(
        f"""
        INSERT INTO order_lines
        SELECT order_id, order_date, customer_name, customer_email, item_1, price_1, qty_1
        FROM catering_sheet WHERE item_1 IS NOT NULL
        UNION ALL
        SELECT order_id, order_date, customer_name, customer_email, item_2, price_2, qty_2
        FROM catering_sheet WHERE item_2 IS NOT NULL
        UNION ALL
        SELECT order_id, order_date, customer_name, customer_email, item_3, price_3, qty_3
        FROM catering_sheet WHERE item_3 IS NOT NULL
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM order_lines
        ORDER BY order_id, product_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **12 rows**, one per order line: 2 + 3 + 1 + 3 + 2 + 1 items. No more
    empty item slots, and a fourth item is just one more **row** — no new
    column, no change to the table.

    Now the Coffee Box question is easy:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT order_id, customer_name, quantity
        FROM order_lines
        WHERE product_name = 'Coffee Box'
        ORDER BY order_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Same 4 orders as before (1001, 1002, 1004, 1005), with **one** condition.

    > 🦆 **DuckDB shortcut:** `UNPIVOT` can also turn columns into rows.
    > `UNION ALL` works in every database, so we use it here.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4. 1NF, Rule 1: One Value per Cell

    `customer_phones` holds a **list** in one cell. We did not copy it into
    `order_lines` — on purpose.

    🙋 **Ask the class:** where do phone numbers belong? To an order? To an
    order line? **To a customer.** So they get their own table, with one
    row per phone number.

    `STRING_SPLIT` turns the text into a list, and `UNNEST` turns the list
    into rows. `DISTINCT` is needed because Ana and Ben each appear in two
    spreadsheet rows.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE customer_phones AS
        SELECT DISTINCT
            customer_email,
            UNNEST(STRING_SPLIT(customer_phones, ', ')) AS phone
        FROM catering_sheet
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM customer_phones
        ORDER BY customer_email, phone
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **6 rows**: Ana and Chen have 2 phones, Ben and Dana have 1.
    The key is `(customer_email, phone)`.

    > ⚠️ Split on `', '` (comma **and** space). Split on `','` only, and the
    > second number keeps a leading space: `' 408-555-0102'`.

    Now the phone question works with a plain `=`:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT customer_email
        FROM customer_phones
        WHERE phone = '408-555-0102'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5. 1NF, Rule 3: A Primary Key

    A **primary key** is one column, or a set of columns, whose values are
    **different in every row**. How do we choose it? We **test** candidates
    with SQL:

    ```sql
    SELECT <candidate columns>, COUNT(*) AS copies
    FROM order_lines
    GROUP BY <candidate columns>
    HAVING COUNT(*) > 1;
    ```

    **0 rows** means: no value appears twice, so the candidate is unique in
    this data. Pick a candidate below and watch the result.
    """)
    return


@app.cell
def _(mo):
    key_choice = mo.ui.dropdown(
        options={
            "order_id": "order_id",
            "product_name": "product_name",
            "order_id + customer_email": "order_id, customer_email",
            "order_id + product_name": "order_id, product_name",
        },
        value="order_id",
        label="Candidate key:",
    )
    key_choice
    return (key_choice,)


@app.cell
def _(con, key_choice, mo):
    _cols = key_choice.value
    _df = con.execute(
        f"""
        SELECT {_cols}, COUNT(*) AS copies
        FROM order_lines
        GROUP BY {_cols}
        HAVING COUNT(*) > 1
        ORDER BY {_cols}
        """
    ).fetchdf()
    _verdict = (
        mo.callout(mo.md(f"✅ **0 rows:** `({_cols})` is unique — a good key."), kind="success")
        if len(_df) == 0
        else mo.callout(
            mo.md(f"❌ **{len(_df)} values appear more than once:** `({_cols})` is **not** a key."),
            kind="danger",
        )
    )
    mo.vstack([_verdict, _df])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🙋 Ask the class: what did each candidate show? (click for answers)": mo.md(
                r"""
                | Candidate | Repeated values | Key? |
                |---|---|---|
                | `order_id` | 4 (orders 1001, 1002, 1004, 1005 have several lines) | ❌ |
                | `product_name` | 4 (Bagel, Coffee Box, Croissant, Muffin) | ❌ |
                | `order_id + customer_email` | 4 (an order has one customer, so this is no better than `order_id`) | ❌ |
                | `order_id + product_name` | 0 | ✅ |

                The key is **composite** — made of two columns:
                **`(order_id, product_name)`**. That is the `PRIMARY KEY`
                we declared in Part 3. It also makes sense: "one product in
                one order" is exactly what a row means.
                """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Because we **declared** the key, DuckDB now enforces it. Try to add
    a second Croissant line to order 1001:
    """)
    return


@app.cell
def _(try_sql):
    try_sql(
        """
        INSERT INTO order_lines VALUES
            (1001, DATE '2026-11-02', 'Ana Lopez', 'ana@scu.edu', 'Croissant', 3.50, 5)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✅ Checkpoint: we are in 1NF

    | 1NF rule | How we met it |
    |---|---|
    | One value per cell | Phone lists → `customer_phones`, one phone per row |
    | No repeating groups | `item_1/2/3` → one row per order line in `order_lines` |
    | A primary key | `(order_id, product_name)`, tested with SQL and declared |

    **End of Session 1.** In-class lab: design + 1NF.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 6. Functional Dependencies, Checked with SQL

    *Session 2 starts here. Run all cells above first.*

    `order_lines` is in 1NF, but look at it again: Ana's name is stored in
    3 rows, and the Croissant price in 3 rows. Let's count:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_name, unit_price, COUNT(*) AS times_stored
        FROM order_lines
        GROUP BY product_name, unit_price
        ORDER BY times_stored DESC, product_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The Coffee Box price (18.00) is stored **4 times**. Why? To explain it
    we need one new idea.

    ### Functional dependency: A → B

    **A → B** means: *"if I know A, I know B."* Every row with the same A
    has the same B.

    - `product_name → unit_price`: a Croissant always costs 3.50
    - `order_id → order_date, customer_name, customer_email`: an order has
      one date and one customer

    **Test it with SQL:** group by A and look for groups with **more than
    one** B. **0 rows** means the dependency holds.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- product_name -> unit_price ?
        SELECT product_name, COUNT(DISTINCT unit_price) AS different_prices
        FROM order_lines
        GROUP BY product_name
        HAVING COUNT(DISTINCT unit_price) > 1
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- order_id -> order_date, customer_name, customer_email ?
        SELECT order_id
        FROM order_lines
        GROUP BY order_id
        HAVING COUNT(DISTINCT order_date) > 1
            OR COUNT(DISTINCT customer_name) > 1
            OR COUNT(DISTINCT customer_email) > 1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both return **0 rows**: both dependencies hold.

    What about `quantity`? Does `order_id` alone decide it?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- order_id -> quantity ?
        SELECT order_id, COUNT(DISTINCT quantity) AS different_quantities
        FROM order_lines
        GROUP BY order_id
        HAVING COUNT(DISTINCT quantity) > 1
        ORDER BY order_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **4 rows: no.** Order 1002 has 3 different quantities (10, 6, 1).
    The same test with `product_name` also fails (4 rows — try it).
    `quantity` needs **both** columns: *how many Croissants in order 1001?*

    ### Full vs. partial dependency

    Our key is **`(order_id, product_name)`**. Sort every non-key column:

    | Column | Depends on | Kind |
    |---|---|---|
    | `quantity` | `order_id` **and** `product_name` | ✅ **full** — needs the whole key |
    | `order_date` | `order_id` only | ❌ **partial** — only part of the key |
    | `customer_name` | `order_id` only | ❌ partial |
    | `customer_email` | `order_id` only | ❌ partial |
    | `unit_price` | `product_name` only | ❌ partial |

    A **partial dependency** is a column that depends on **part** of a
    composite key. Every partial dependency means **repeated data** —
    and repeated data causes **anomalies**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 7. Anomalies: Why 1NF Is Not Enough

    An **anomaly** is a problem when you **change** data. We test each one
    on a **copy** of `order_lines`, so the real table stays clean.

    ### 1. Update anomaly

    The Croissant price goes up to **3.75**. A new employee updates only
    the newest order:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE order_lines_test AS
        SELECT * FROM order_lines
        """
    )
    con.execute(
        f"""
        UPDATE order_lines_test
        SET unit_price = 3.75
        WHERE product_name = 'Croissant' AND order_id = 1006
        """
    )
    con.execute(
        f"""
        -- the dependency test from Part 6
        SELECT product_name,
               COUNT(DISTINCT unit_price) AS different_prices,
               MIN(unit_price) AS low_price,
               MAX(unit_price) AS high_price
        FROM order_lines_test
        GROUP BY product_name
        HAVING COUNT(DISTINCT unit_price) > 1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now the database says a Croissant costs **both** 3.50 and 3.75. The
    price is stored 3 times, so a correct update must change 3 rows.
    Miss one, and the data **contradicts itself**.

    ### 2. Insert anomaly

    The bakery adds a new product, a **Cookie Platter** for 15.00. Nobody
    has ordered it yet. Can we store it?
    """)
    return


@app.cell
def _(try_sql):
    try_sql(
        """
        INSERT INTO order_lines VALUES
            (NULL, NULL, NULL, NULL, 'Cookie Platter', 15.00, NULL)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **No.** `order_id` is part of the primary key, and a key column can
    never be `NULL`. A product cannot exist until **someone orders it**.

    ### 3. Delete anomaly

    Dana cancels order 1005. Delete it:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE order_lines_test AS
        SELECT * FROM order_lines
        """
    )
    con.execute(
        f"""
        DELETE FROM order_lines_test
        WHERE order_id = 1005
        """
    )
    con.execute(
        f"""
        -- what do we still know about the Fruit Tray and about Dana?
        SELECT product_name, unit_price, customer_name
        FROM order_lines_test
        WHERE product_name = 'Fruit Tray'
           OR customer_name = 'Dana Patel'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **0 rows.** Order 1005 was the only Fruit Tray order and Dana's only
    order. Deleting one order also deleted **the Fruit Tray's price** and
    **Dana's name and email**. We lost facts we wanted to keep.

    | Anomaly | What went wrong | Caused by |
    |---|---|---|
    | Update | One price, two values | `product_name → unit_price` (partial) |
    | Insert | Can't add a product with no orders | `unit_price` stored only with an order |
    | Delete | Cancelling an order lost a product and a customer | facts about products and customers live in order rows |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 8. 2NF: Split the Table

    **A table is in 2NF when it is in 1NF and no non-key column depends on
    only part of the key.**

    **Recipe:** move each partial dependency into a table where **that part**
    is the whole key.

    | Part of the key | Columns that depend on it | New table |
    |---|---|---|
    | `order_id` | `order_date`, `customer_name`, `customer_email` | `orders` |
    | `product_name` | `unit_price` | `products` |
    | `(order_id, product_name)` | `quantity` | `order_items` |

    We create the tables with **keys** and **foreign keys** first, then
    fill them from `order_lines`. `DISTINCT` removes the repeated copies.

    > ℹ️ The `DROP` statements come first so the cell can run again:
    > DuckDB will not drop a table that another table's foreign key points to.
    """)
    return


@app.cell
def _(con):
    con.execute("DROP TABLE IF EXISTS order_items")
    con.execute("DROP TABLE IF EXISTS orders")
    con.execute("DROP TABLE IF EXISTS products")
    con.execute(
        f"""
        CREATE TABLE products (
            product_name VARCHAR PRIMARY KEY,
            unit_price   DECIMAL(6, 2) NOT NULL
        )
        """
    )
    con.execute(
        f"""
        CREATE TABLE orders (
            order_id       INTEGER PRIMARY KEY,
            order_date     DATE NOT NULL,
            customer_name  VARCHAR,
            customer_email VARCHAR
        )
        """
    )
    con.execute(
        f"""
        CREATE TABLE order_items (
            order_id     INTEGER REFERENCES orders (order_id),
            product_name VARCHAR REFERENCES products (product_name),
            quantity     INTEGER NOT NULL,
            PRIMARY KEY (order_id, product_name)
        )
        """
    )
    con.execute(
        f"""
        INSERT INTO products
        SELECT DISTINCT product_name, unit_price
        FROM order_lines
        """
    )
    con.execute(
        f"""
        INSERT INTO orders
        SELECT DISTINCT order_id, order_date, customer_name, customer_email
        FROM order_lines
        """
    )
    con.execute(
        f"""
        INSERT INTO order_items
        SELECT order_id, product_name, quantity
        FROM order_lines
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM products
        ORDER BY product_name
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM orders
        ORDER BY order_id
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM order_items
        ORDER BY order_id, product_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each price is now stored **once** (5 products), each order's date and
    customer **once** (6 orders), and `order_items` keeps only what needs
    the whole key: the `quantity` of 12 order lines.

    🙋 **Ask the class:** is each table in 2NF?

    - `products` and `orders` have a **single-column** key. A 1NF table
      with a single-column key is **always** in 2NF — no "part" of the key exists.
    - `order_items` has a composite key, and its only non-key column,
      `quantity`, depends on the **whole** key. ✅
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
        erDiagram
            ORDERS ||--|{ ORDER_ITEMS : contains
            PRODUCTS ||--o{ ORDER_ITEMS : "appears in"
            ORDERS {
                int order_id PK
                date order_date
                varchar customer_name
                varchar customer_email
            }
            ORDER_ITEMS {
                int order_id PK
                varchar product_name PK
                int quantity
            }
            PRODUCTS {
                varchar product_name PK
                decimal unit_price
            }
            CUSTOMER_PHONES {
                varchar customer_email PK
                varchar phone PK
            }
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 9. Prove It

    ### Nothing was lost

    Splitting a table is only safe if a **JOIN** gives the original back.
    First, count the rows:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT 'order_lines (1NF)' AS table_name, COUNT(*) AS row_count FROM order_lines
        UNION ALL
        SELECT 'orders', COUNT(*) FROM orders
        UNION ALL
        SELECT 'products', COUNT(*) FROM products
        UNION ALL
        SELECT 'order_items', COUNT(*) FROM order_items
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now join the three tables back together and compare with `order_lines`.
    `EXCEPT` returns the rows of the first query that are **not** in the
    second. We check both directions — **0 and 0** means identical.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        WITH rebuilt AS (
            SELECT o.order_id, o.order_date, o.customer_name, o.customer_email,
                   i.product_name, p.unit_price, i.quantity
            FROM order_items AS i
            JOIN orders   AS o ON i.order_id = o.order_id
            JOIN products AS p ON i.product_name = p.product_name
        )
        SELECT
            (SELECT COUNT(*) FROM (SELECT * FROM order_lines EXCEPT SELECT * FROM rebuilt)) AS missing_rows,
            (SELECT COUNT(*) FROM (SELECT * FROM rebuilt EXCEPT SELECT * FROM order_lines)) AS extra_rows
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And the tables answer business questions with a JOIN — the total of
    each order:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT o.order_id,
               o.customer_name,
               SUM(i.quantity * p.unit_price) AS order_total
        FROM orders AS o
        JOIN order_items AS i ON o.order_id = i.order_id
        JOIN products    AS p ON i.product_name = p.product_name
        GROUP BY o.order_id, o.customer_name
        ORDER BY o.order_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The anomalies are gone

    Again on **copies**, so the tables above stay as they are.

    **Update:** the Croissant price changes in **one** row:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE products_test AS
        SELECT * FROM products
        """
    )
    con.execute(
        f"""
        UPDATE products_test
        SET unit_price = 3.75
        WHERE product_name = 'Croissant'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Count = 1`: one row changed, and every order now sees the new price.

    **Insert:** the Cookie Platter needs no order:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO products_test VALUES ('Cookie Platter', 15.00)
        """
    )
    con.execute(
        f"""
        SELECT *
        FROM products_test
        ORDER BY product_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Delete:** cancelling order 1005 removes its 2 order lines, but the
    Fruit Tray stays in `products`:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE order_items_test AS
        SELECT * FROM order_items
        """
    )
    con.execute(
        f"""
        DELETE FROM order_items_test
        WHERE order_id = 1005
        """
    )
    con.execute(
        f"""
        SELECT product_name, unit_price
        FROM products
        WHERE product_name = 'Fruit Tray'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bonus: the keys protect the data

    The keys and foreign keys we declared make DuckDB refuse bad data.
    Run each cell and read the message.

    **A product that does not exist** (foreign key):
    """)
    return


@app.cell
def _(try_sql):
    try_sql(
        """
        INSERT INTO order_items VALUES (1001, 'Donut', 5)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The same product twice** (primary key):
    """)
    return


@app.cell
def _(try_sql):
    try_sql(
        """
        INSERT INTO products VALUES ('Bagel', 3.00)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **An order that still has items** (foreign key) — delete its
    `order_items` rows first:
    """)
    return


@app.cell
def _(try_sql):
    try_sql(
        """
        DELETE FROM orders WHERE order_id = 1005
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Wrap-Up

    ### Preview: one problem is left (3NF)
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT customer_name, customer_email, COUNT(*) AS times_stored
        FROM orders
        GROUP BY customer_name, customer_email
        HAVING COUNT(*) > 1
        ORDER BY customer_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ana and Ben each have 2 orders, so their names are stored twice.
    `orders` **is** in 2NF (its key is one column), but
    `customer_email → customer_name` is a dependency between two
    **non-key** columns. **3NF** moves it into a `customers` table — the
    last box of the design from Part 2. See the 3NF section of
    `02_database_design_and_normalization.md`.

    > ℹ️ **Real systems** often copy the price into `order_items` too
    > (the price *on the day of the order*), so a later price change does
    > not change old receipts. That is a deliberate design decision, not a
    > 2NF mistake: it is a *different fact* from today's price.

    ### Summary

    | Step | Question to ask | Fix | SQL tool |
    |---|---|---|---|
    | Design | What are the entities, keys, relationships? | Entity list + diagram; M:N needs a bridge table | — |
    | 1NF rule 1 | A list in a cell? | One value per row, in its own table | `UNNEST(STRING_SPLIT(...))` |
    | 1NF rule 2 | Numbered columns (`item_1`, `item_2`)? | Turn columns into rows | `UNION ALL` |
    | 1NF rule 3 | What makes each row unique? | Test and declare a primary key | `GROUP BY … HAVING COUNT(*) > 1` |
    | 2NF | Composite key: does a column need only part of it? | Move it to a table keyed by that part | `COUNT(DISTINCT …) > 1`, `SELECT DISTINCT` |
    | Check | Did the split lose anything? | Join back and compare | `JOIN`, `EXCEPT` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🎟️ Exit ticket: 3 quick questions (click for answers)": mo.md(
                r"""
                **Q1.** A table `enrollments(student_id, course_id, grade,
                course_title)` has key `(student_id, course_id)`. Which
                column breaks 2NF, and why?

                > `course_title` — it depends on `course_id` only (part of
                > the key). `grade` needs both columns, so it is fine.

                **Q2.** A table has a single-column primary key and is in
                1NF. Can it break 2NF?

                > No. 2NF problems need a composite key; a one-column key
                > has no "part".

                **Q3.** Which SQL query proves that `product_name →
                unit_price` holds in the current data?

                > `SELECT product_name FROM order_lines GROUP BY product_name
                > HAVING COUNT(DISTINCT unit_price) > 1;` — 0 rows means it
                > holds.
                """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
