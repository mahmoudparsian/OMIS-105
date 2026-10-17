import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from plot_helpers import matchmaker_html, plot_before_after

    return matchmaker_html, plot_before_after


@app.cell
def _():
    import duckdb

    # Two tiny tables, built in memory. Re-running is safe
    # because of CREATE OR REPLACE.
    con = duckdb.connect(database=":memory:")

    con.execute("""
        CREATE OR REPLACE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name        VARCHAR,
            city        VARCHAR
        )
    """)
    con.execute("""
        INSERT INTO customers VALUES
            (101, 'Maya Chen',   'San Jose'),
            (102, 'Omar Haddad', 'Santa Clara'),
            (103, 'Sofia Rossi', 'Palo Alto'),
            (104, 'Leo Kim',     'Cupertino'),
            (105, 'Priya Patel', 'Sunnyvale')
    """)

    con.execute("""
        CREATE OR REPLACE TABLE orders (
            order_id    INTEGER PRIMARY KEY,
            customer_id INTEGER,
            item        VARCHAR,
            price       DECIMAL(5, 2)
        )
    """)
    con.execute("""
        INSERT INTO orders VALUES
            (1, 103, 'Latte',            5.50),
            (2, 101, 'Croissant',        4.25),
            (3, 105, 'Iced Mocha',       6.00),
            (4, 103, 'Blueberry Muffin', 3.75),
            (5, 102, 'Espresso',         3.50),
            (6, 101, 'Chai Latte',       5.25)
    """)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 🪄 Your First JOIN — The Magic of `INNER JOIN`

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### The Story: Bronco Brew ☕

    **Bronco Brew** is a small coffee shop near campus. It keeps
    its data in **2 tables**:

    | Table | Rows | What it knows |
    |-------|-----:|---------------|
    | `customers` | 5 | **who** each customer is: name and city |
    | `orders`    | 6 | **what** was sold: item and price |

    The manager wants to send a thank-you card to every customer
    who placed an order. She asks one simple question:

    > **"Who bought what — and where do they live?"**

    Here is the problem: **neither table can answer this alone.**

    - `orders` knows *what* was sold, but not *who* bought it.
    - `customers` knows *who* people are, but not *what* they bought.

    Today you will learn one SQL "spell" that combines the two
    tables into one answer: **`INNER JOIN`**.

    ### The Plan

    | Part | Queries | What happens |
    |------|---------|--------------|
    | 1. Meet the data | Q1–Q2 | Look at each table. Find the shared column. |
    | 2. The problem | Q3 | Try to answer the question by hand. It is slow! |
    | 3. The magic spell | Q4 | One `INNER JOIN` answers everything. |
    | 4. How the magic works | — | Watch the matching, one order at a time. |
    | 5. Anatomy of the spell | Q5 | Every word of the query, explained. |
    | 6. Put the magic to work | Q6–Q9 | Answer real business questions. |
    | 7. The one rule | Q10 | `INNER JOIN` keeps only rows that match. |
    | 8. Common mistakes | — | Three real errors, and how to fix them. |
    | 9. Cheat sheet & practice | — | A template and 5 exercises with solutions. |

    The tables are tiny on purpose: you can check every answer by eye.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 1 — Meet the Data

    ### Q1. The `customers` table — *who* our customers are
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT customer_id,
               name,
               city
        FROM customers
        ORDER BY customer_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    5 customers. Each one has a unique **`customer_id`** — a number
    that never repeats. No two customers share an ID.

    ### Q2. The `orders` table — *what* was sold
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT order_id,
               customer_id,
               item,
               price
        FROM orders
        ORDER BY order_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    6 orders. Look closely: **there are no names here!** An order only
    says `customer_id = 103`. Who is 103? This table does not know.

    ### 🔑 The shared column

    Both tables have a column called **`customer_id`**. This is the
    "bridge" between them:

    ```
       customers                         orders
    ┌─────────────┬─────────────┐     ┌──────────┬─────────────┬───────────┐
    │ customer_id │ name        │     │ order_id │ customer_id │ item      │
    ├─────────────┼─────────────┤     ├──────────┼─────────────┼───────────┤
    │     103     │ Sofia Rossi │ ◄───┤    1     │     103     │ Latte     │
    └─────────────┴─────────────┘     └──────────┴─────────────┴───────────┘
                     same number = same person
    ```

    - In `customers`, `customer_id` is the **primary key** — it is
      unique, one per customer.
    - In `orders`, `customer_id` is a **foreign key** — it *points to*
      a row in another table.

    Storing a small number in `orders` (instead of copying the name
    and city into every order) keeps the data clean: if Sofia moves,
    we change her city in **one** place.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 2 — The Problem: Detective Work by Hand 🔍

    Let's answer the manager's question without a join.
    Order 1 is a Latte for `customer_id = 103`. Who is that?
    We must look it up in the other table:

    ### Q3. Look up one customer by hand
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT name, city
        FROM customers
        WHERE customer_id = 103;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    It worked: Sofia Rossi from Palo Alto bought the Latte. 🎉

    But wait…

    - That was **1** order. We have **6**, so we need 6 lookups.
    - A real coffee chain has **6 million** orders. One query per order?
      Copy and paste every answer into a spreadsheet? No way. 😩

    We need a way to tell the database:

    > *"For **every** order, find the customer with the **same**
    > `customer_id`, and put the two rows **side by side**."*

    That sentence **is** an `INNER JOIN`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 3 — The Magic Spell 🪄

    ### Q4. One query. Every answer.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT orders.order_id,
               orders.customer_id,
               orders.item,
               orders.price,
               customers.name,
               customers.city
        FROM orders
        INNER JOIN customers
            ON orders.customer_id = customers.customer_id
        ORDER BY orders.order_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Look at that!** ✨ Every order now has a **name** and a **city**
    next to it. Six lookups, done in one query.

    - `orders.item` means "the `item` column from `orders`". Writing
      the table name first tells everyone where each column comes from.
    - `customers.name` and `customers.city` were **borrowed** from
      the other table — glued on the right of each order.
    - In every row, the order's `customer_id` belongs to the person
      next to it. That is exactly what we asked for:
      `ON orders.customer_id = customers.customer_id`.

    ### Before ➜ After

    Flip the switch to see the same 6 orders, before and after the join.
    """)
    return


@app.cell
def _(mo):
    spell = mo.ui.switch(label="🪄 Cast the INNER JOIN spell")
    spell
    return (spell,)


@app.cell(hide_code=True)
def _(con, mo, spell):
    if spell.value:
        _sql = """
            SELECT o.order_id, o.item, o.price, c.name, c.city
            FROM orders o
            INNER JOIN customers c
                ON o.customer_id = c.customer_id
            ORDER BY o.order_id
        """
        _title = "✨ **AFTER** — every order has a real person and a city!"
    else:
        _sql = """
            SELECT order_id, item, price, customer_id
            FROM orders
            ORDER BY order_id
        """
        _title = "❓ **BEFORE** — who are 103, 101, 105…? Nobody knows."
    mo.vstack([mo.md(_title), con.execute(_sql).fetchdf()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 4 — How Does the Magic Work? 🔬

    It is not really magic. The database follows simple steps,
    **for every row in `orders`**:

    1. **Take** one order and read its `customer_id`.
    2. **Compare** that number with the `customer_id` of every customer.
    3. **Glue** the order to the customer whose number matches.

    Pick an order below and watch the matching happen.
    """)
    return


@app.cell
def _(con):
    orders_df = con.execute(
        "SELECT order_id, customer_id, item, price FROM orders ORDER BY order_id"
    ).fetchdf()
    customers_df = con.execute(
        "SELECT customer_id, name, city FROM customers ORDER BY customer_id"
    ).fetchdf()
    return customers_df, orders_df


@app.cell
def _(mo, orders_df):
    _options = {
        f"Order {r.order_id}: {r.item} (customer_id {r.customer_id})": r.order_id
        for r in orders_df.itertuples()
    }
    order_picker = mo.ui.dropdown(
        options=_options,
        value=next(iter(_options)),
        label="Pick an order:",
    )
    order_picker
    return (order_picker,)


@app.cell(hide_code=True)
def _(customers_df, matchmaker_html, mo, order_picker, orders_df):
    _row = orders_df[orders_df["order_id"] == order_picker.value].iloc[0]
    _order = {
        "order_id": int(_row["order_id"]),
        "customer_id": int(_row["customer_id"]),
        "item": _row["item"],
        "price": float(_row["price"]),
    }
    mo.Html(matchmaker_html(_order, customers_df))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Try every order. Each one finds **exactly one** partner, because
    each `customer_id` appears only once in `customers`.

    Did you notice? **Maya** (101) and **Sofia** (103) each placed
    **2** orders, so each of them appears in **2** result rows.
    A customer is glued to *every* order that points to them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 5 — Anatomy of the Spell 📜

    ```sql
    SELECT o.order_id, o.item, o.price, c.name, c.city   -- ④ pick the columns you want
    FROM orders AS o                                     -- ① start with one table
    INNER JOIN customers AS c                            -- ② bring in a second table
        ON o.customer_id = c.customer_id                 -- ③ the matching rule
    ORDER BY o.order_id;                                 -- ⑤ sort, as usual
    ```

    | Part | Meaning |
    |------|---------|
    | ① `FROM orders AS o` | Start with the `orders` table. Give it a short nickname: `o`. |
    | ② `INNER JOIN customers AS c` | Bring in `customers`, nickname `c`. |
    | ③ `ON o.customer_id = c.customer_id` | **The matching rule.** Glue two rows together when their `customer_id` values are equal. |
    | ④ `SELECT o.item, c.name, …` | Choose columns from **either** table. `o.item` means "the `item` column from `o`". |
    | ⑤ `ORDER BY` | Everything you already know still works after a join. |

    **Nicknames (aliases).** `o` and `c` are **table aliases**. They
    save typing, and they tell everyone which table each column comes
    from. The word `AS` is optional: `FROM orders o` works too.

    **`JOIN` = `INNER JOIN`.** If you just write `JOIN`, SQL treats it
    as `INNER JOIN`. In this course we write `INNER JOIN` so the
    meaning is clear.

    ### Q5. The clean version — only the columns we need
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT o.order_id,
               o.item,
               o.price,
               c.name,
               c.city
        FROM orders AS o
        INNER JOIN customers AS c
            ON o.customer_id = c.customer_id
        ORDER BY o.order_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    This is the manager's answer: **who bought what, and where they
    live.** The thank-you cards can go out today. 💌

    ---
    # Part 6 — Put the Magic to Work 💼

    After the join, the result is just a table. So `WHERE`,
    `ORDER BY`, `GROUP BY`, `SUM`, and `COUNT` all work on it — exactly
    as you learned in earlier weeks.

    ### Q6. Who ordered what? (sorted by customer name)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT c.name,
               o.item,
               o.price
        FROM orders AS o
        INNER JOIN customers AS c
            ON o.customer_id = c.customer_id
        ORDER BY c.name, o.item;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. What did customers from Palo Alto buy?

    The **city** is in `customers`; the **items** are in `orders`.
    Only a join can filter on one and show the other.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT c.name,
               c.city,
               o.item,
               o.price
        FROM orders AS o
        INNER JOIN customers AS c
            ON o.customer_id = c.customer_id
        WHERE c.city = 'Palo Alto';
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. How much did each customer spend? 💰

    First, the `orders` table **alone**. It can add up the money,
    but it can only show ID numbers:
    """)
    return


@app.cell
def _(con, mo):
    df_spend_by_id = mo.sql(
        f"""
        SELECT customer_id,
               COUNT(*)   AS num_orders,
               SUM(price) AS total_spent
        FROM orders
        GROUP BY customer_id
        ORDER BY total_spent DESC;
        """,
        engine=con
    )
    return (df_spend_by_id,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Now the same question **with a join**. Same numbers — but now
    they belong to real people:
    """)
    return


@app.cell
def _(con, mo):
    df_spend_by_name = mo.sql(
        f"""
        SELECT c.name,
               COUNT(*)     AS num_orders,
               SUM(o.price) AS total_spent
        FROM orders AS o
        INNER JOIN customers AS c
            ON o.customer_id = c.customer_id
        GROUP BY c.name
        ORDER BY total_spent DESC;
        """,
        engine=con
    )
    return (df_spend_by_name,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **The chart below shows the same totals twice.** On the left,
    the `orders` table alone: grey bars labeled with numbers nobody
    can read. On the right, after the join: the same bars, now with
    real names. Same data, much more meaning.
    """)
    return


@app.cell(hide_code=True)
def _(df_spend_by_id, df_spend_by_name, plot_before_after):
    plot_before_after(
        df_spend_by_id["customer_id"],
        df_spend_by_id["total_spent"],
        df_spend_by_name["name"],
        df_spend_by_name["total_spent"],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Which city brings in the most money? 🏙️
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT c.city,
               COUNT(*)     AS num_orders,
               SUM(o.price) AS total_sales
        FROM orders AS o
        INNER JOIN customers AS c
            ON o.customer_id = c.customer_id
        GROUP BY c.city
        ORDER BY total_sales DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    San Jose wins, with $9.50 from Maya's two orders. The manager
    now knows where to put the next flyer. 📍

    ---
    # Part 7 — The One Rule to Remember ⚖️

    Look back at Q5. Count the people in it. Maya, Sofia, Priya,
    Omar… **Where is Leo Kim?** 🤔

    ### Q10. Count before and after the join
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            (SELECT COUNT(*) FROM customers) AS customers_in_table,
            (SELECT COUNT(*) FROM orders)    AS orders_in_table,
            (SELECT COUNT(*)
             FROM orders AS o
             INNER JOIN customers AS c
                 ON o.customer_id = c.customer_id) AS rows_after_join,
            (SELECT COUNT(DISTINCT c.customer_id)
             FROM orders AS o
             INNER JOIN customers AS c
                 ON o.customer_id = c.customer_id) AS customers_after_join;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    5 customers went in, but only **4** came out. Leo Kim (104) has
    **not ordered anything yet**. No order has `customer_id = 104`,
    so Leo has no partner to be glued to — and he is left out.

    > **The rule:** `INNER JOIN` keeps **only the rows that match** in
    > **both** tables. A row with no partner does not appear.

    Think of it like a dance: only people who **found a partner**
    are on the dance floor. 💃🕺

    For the manager's question, this is exactly right: thank-you
    cards go to people who **placed an order**. Leo didn't, so he
    gets no card (yet!).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 8 — Common Mistakes (and How to Fix Them) 🚧

    These are real error messages from DuckDB. When you see one in
    class, don't panic — read it. It usually tells you the fix.
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _mistakes = [
        (
            "Mistake 1 — Which `customer_id`?",
            """SELECT customer_id, name
    FROM orders AS o
    INNER JOIN customers AS c
        ON o.customer_id = c.customer_id;""",
            "Both tables have a `customer_id` column, so DuckDB does "
            "not know which one you mean. **Fix:** add the alias — "
            "`o.customer_id` or `c.customer_id`.",
        ),
        (
            "Mistake 2 — Forgetting the `ON` rule",
            """SELECT orders.item, customers.name
    FROM orders
    INNER JOIN customers;""",
            "An `INNER JOIN` needs a matching rule. Without `ON`, "
            "DuckDB does not know how to pair the rows. **Fix:** add "
            "`ON orders.customer_id = customers.customer_id`.",
        ),
        (
            "Mistake 3 — Using the full name after giving a nickname",
            """SELECT o.item, customers.name
    FROM orders AS o
    INNER JOIN customers AS c
        ON o.customer_id = c.customer_id;""",
            "Once a table has an alias, use the alias everywhere in "
            "that query. **Fix:** write `c.name`, not `customers.name`.",
        ),
    ]

    _blocks = []
    for _title, _sql, _fix in _mistakes:
        try:
            con.execute(_sql)
            _err = "(no error?)"
        except Exception as _e:
            _err = str(_e)
        _blocks.append(mo.md(
            f"### {_title}\n\n"
            f"```sql\n{_sql}\n```\n\n"
            f"**DuckDB says:**\n\n```\n{_err}\n```\n\n"
            f"{_fix}"
        ))
    mo.vstack(_blocks)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 9 — Cheat Sheet 📋

    ```sql
    SELECT a.column1, b.column2
    FROM table_a AS a
    INNER JOIN table_b AS b
        ON a.shared_column = b.shared_column
    WHERE ...        -- optional: filter
    GROUP BY ...     -- optional: summarize
    ORDER BY ...;    -- optional: sort
    ```

    | Remember | Why |
    |----------|-----|
    | Find the **shared column** first | It is the bridge: a primary key in one table, a foreign key in the other. |
    | The `ON` rule says **how rows match** | Usually `a.key = b.key`. |
    | Use **aliases** (`o`, `c`) | Shorter queries, and every column says where it comes from. |
    | Prefix shared column names | `o.customer_id`, never just `customer_id`. |
    | `INNER JOIN` keeps **only matches** | A row with no partner (like Leo) is left out. |
    | One row can match **many** rows | Maya has 2 orders, so she appears in 2 result rows. |
    | After the join, it's just a table | `WHERE`, `GROUP BY`, `SUM`, `ORDER BY` all work. |

    ---
    # Try It Yourself ✍️

    Write each query in a new cell, then open the solution to check.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Exercise 1 — Show every order's item and the city it came from.": mo.md("""
    ```sql
    SELECT o.item, c.city
    FROM orders AS o
    INNER JOIN customers AS c
        ON o.customer_id = c.customer_id;
    ```
    6 rows — one per order.
        """),
        "Exercise 2 — Which items did Maya Chen buy?": mo.md("""
    ```sql
    SELECT o.item, o.price
    FROM orders AS o
    INNER JOIN customers AS c
        ON o.customer_id = c.customer_id
    WHERE c.name = 'Maya Chen';
    ```
    2 rows: Croissant ($4.25) and Chai Latte ($5.25).
        """),
        "Exercise 3 — List every order over $5.00 with the customer's name, most expensive first.": mo.md("""
    ```sql
    SELECT c.name, o.item, o.price
    FROM orders AS o
    INNER JOIN customers AS c
        ON o.customer_id = c.customer_id
    WHERE o.price > 5.00
    ORDER BY o.price DESC;
    ```
    3 rows: Priya's Iced Mocha ($6.00), Sofia's Latte ($5.50),
    Maya's Chai Latte ($5.25).
        """),
        "Exercise 4 — How many orders came from each city?": mo.md("""
    ```sql
    SELECT c.city, COUNT(*) AS num_orders
    FROM orders AS o
    INNER JOIN customers AS c
        ON o.customer_id = c.customer_id
    GROUP BY c.city
    ORDER BY num_orders DESC;
    ```
    San Jose 2, Palo Alto 2, Sunnyvale 1, Santa Clara 1.
    Cupertino is not listed: Leo has no orders.
        """),
        "Exercise 5 (think!) — Tomorrow Leo orders a Latte. How many rows will Q5 return then?": mo.md("""
    **7 rows.** The new order has `customer_id = 104`, so it finds
    Leo as its partner, and Leo now appears in the result. You can
    test it:

    ```sql
    INSERT INTO orders VALUES (7, 104, 'Latte', 5.50);
    ```

    Then re-run Q5. (Re-run the whole notebook afterward to get the
    original 6 orders back.)
        """),
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ### 🎓 What You Learned Today

    - Real databases split data into **separate tables**, linked by a
      **shared column**.
    - `INNER JOIN … ON …` puts matching rows **side by side**, so one
      query can answer a question that no single table can.
    - It is not magic — just **take, compare, glue**, for every row.
    - `INNER JOIN` keeps **only the rows that match**.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
