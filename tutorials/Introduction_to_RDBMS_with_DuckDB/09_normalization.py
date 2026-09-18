import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="09 - Normalization")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 09 · Normalization

    Notebook **9 of 12** · estimated time: **12 minutes**.

    Back in notebook 02 you were told "one giant flat table is worse
    than five linked ones" and asked to take it on faith. This
    notebook proves it, with real anomalies in real data, then walks
    through 1NF → 2NF → 3NF — the formal reasoning for *why* our
    schema is shaped the way it is.

    Objectives:

    - Build one wide, "everything in one table" version of our data
    - Identify **update**, **insert**, and **delete anomalies** in it
    - Define **1NF**, **2NF**, and **3NF**, and see our schema satisfy them
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect("ecommerce_database.duckdb", read_only=True)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exhibit A: the flattened table

    Here's what our data looks like un-split into one table — a
    `JOIN` of all four tables into a single wide result, the way
    you'd get it from a spreadsheet or a single denormalized report:
    """)
    return


@app.cell
def _(con):
    flat = con.sql(
        """
        SELECT o.order_id, o.order_date,
               c.customer_id, c.first_name, c.last_name,
               c.city AS customer_city, c.state AS customer_state,
               p.product_id, p.product_name, p.category,
               oi.quantity, oi.unit_price
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        ORDER BY o.order_id
        """
    ).df()
    flat.head(8)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look closely at rows 0–3: order #1 has four line items, so
    **Sofia Smith's name, city, and state are repeated four times**,
    and every product's name/category is repeated once for every
    order that includes it. That redundancy isn't cosmetic — it
    causes three specific, well-known classes of bug.

    ## The three anomalies

    **Update anomaly.** Sofia Smith moves from San Jose to Denver.
    In this flat table, that means updating `customer_city` on
    *every row* that mentions her — miss even one, and the table now
    disagrees with itself about where she lives. In our real schema,
    it's **one row, one `UPDATE`**, in `customers`:
    """)
    return


@app.cell
def _(con):
    con.sql("SELECT customer_id, first_name, city FROM customers WHERE customer_id = 1")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insert anomaly.** Suppose the business adds a brand-new
    product that nobody has ordered yet. In the flat table, there's
    nowhere to put it — every row requires an `order_id`, so you
    *can't record that a product exists* until someone orders it.
    In our real schema, `products` is its own table: insert a new
    product any time, order-independent.

    **Delete anomaly.** Now imagine a product that has only ever
    been ordered once, and that one order gets cancelled and its row
    deleted. In the flat table, deleting that *order* row also
    deletes the only record that the *product* ever existed — you
    lose its name, category, and price along with the order. In our
    schema, deleting a row from `orders` doesn't touch `products` at
    all — they're independent, so the product's own record survives.

    All three anomalies have the same root cause: **the flat table
    is forcing unrelated facts** (a customer's address, a product's
    name, an order's date) **to live and die together** just because
    they happened to appear in the same query result. Normalization
    is the formal process of splitting them back apart correctly.

    ## Normal forms

    ### 1NF — Atomic values, no repeating groups

    A table is in **First Normal Form** if every column holds a
    single, indivisible value — no comma-separated lists, no
    repeated column groups like `product_1, product_2, product_3`.

    ❌ Not 1NF:

    | order_id | products |
    |---|---|
    | 1 | Whiteboard, Webcam, Notebook (3-pack) |

    ✅ 1NF (our actual `order_items` table): one row per
    order–product pair, not one row per order with a packed-in list.
    You already saw this — it's why `order_items` exists at all.

    ### 2NF — No partial dependency on *part of* a composite key

    Second Normal Form only becomes a question when a table has a
    **composite primary key** (notebook 02: `order_items`'s key is
    `(order_id, product_id)`). It requires that every non-key column
    depend on the *whole* key, not just part of it.

    In the flat table above, imagine `(order_id, product_id)` as the
    key. `quantity` genuinely depends on *both* — a specific product
    *within* a specific order. But `product_name` and `category`
    depend only on `product_id` — they'd be identical no matter which
    order you looked at. That's a **partial dependency**, and it
    violates 2NF. The fix is exactly what our schema does: pull
    `product_name`/`category` out into their own `products` table,
    keyed by `product_id` alone.

    ### 3NF — No transitive dependency between non-key columns

    Third Normal Form says: every non-key column must depend
    **directly** on the primary key — not on another non-key column.

    In the flat table, `order_id` is (part of) the key. But
    `customer_city` doesn't really depend on `order_id` — it depends
    on `customer_id`, which itself depends on `order_id`. That chain
    (`order_id → customer_id → customer_city`) is a **transitive
    dependency**, and it's why the same city value gets copy-pasted
    across every order that customer ever places. The fix, again,
    is our actual schema: `customers` holds `city` once, keyed by
    `customer_id`; `orders` just references `customer_id`.

    **In short: our 5-table schema isn't arbitrary — it's what you
    get when you mechanically remove every partial and transitive
    dependency from the flat version.** That's normalization.

    ## Exercise

    A colleague proposes this single table for a library system:

    | book_id (PK) | title | author_name | author_country | borrower_name | borrower_email | due_date |
    |---|---|---|---|---|---|---|

    Answer using the reasoning above.
    """)
    return


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "author_country depends on author_name, not on book_id — a transitive dependency (3NF violation)",
            "This table is already in 3NF, no changes needed",
            "title is not atomic, so it violates 1NF",
        ],
        label="9.1 — What normalization problem does this table have?",
    )
    q1
    return (q1,)


@app.cell(hide_code=True)
def _(mo, q1):
    def _check():
        correct = "author_country depends on author_name, not on book_id — a transitive dependency (3NF violation)"
        if q1.value is None:
            return mo.md("_Not answered yet._")
        icon = "✅" if q1.value == correct else "❌"
        return mo.md(f"{icon} You chose: *{q1.value}*" + ("" if q1.value == correct else f"\n\ncorrect answer: *{correct}*"))

    _check()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **9.2** — Sketch (in words, or a text cell below) how you'd split
    the library table into properly normalized tables. Think about
    what happens when the same author writes multiple books, or the
    same borrower checks out multiple books.
    """)
    return


@app.cell
def _(mo):
    ex2 = mo.ui.text_area(
        placeholder="e.g. authors(author_id PK, author_name, author_country) ...",
        label="9.2 — your design",
        full_width=True,
        rows=5,
    )
    ex2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "💡 One reasonable answer": mo.md(
                "```\n"
                "authors(author_id PK, author_name, author_country)\n"
                "books(book_id PK, title, author_id FK -> authors)\n"
                "borrowers(borrower_id PK, borrower_name, borrower_email)\n"
                "loans(loan_id PK, book_id FK -> books, borrower_id FK -> borrowers, due_date)\n"
                "```\n\n"
                "This mirrors our course schema exactly: `authors` is like\n"
                "`customers`/`employees`, `books` is like `products`,\n"
                "and `loans` is like `orders`/`order_items` — a linking\n"
                "table that can reference the same book or borrower\n"
                "many times without repeating their details."
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - A single flat table causes **update**, **insert**, and
      **delete anomalies** because it forces unrelated facts to live
      in the same row.
    - **1NF**: atomic values, no repeating groups.
    - **2NF**: every non-key column depends on the *entire* primary
      key (relevant when the key is composite).
    - **3NF**: no non-key column depends on another non-key column
      (no transitive dependencies).
    - Our 5-table e-commerce schema is a worked example of applying
      all three.

    ➡️ **Next:** `10_views_and_transactions.py` — `CREATE VIEW` for
    reusable queries, and real `BEGIN`/`COMMIT`/`ROLLBACK`
    transactions.
    """)
    return


if __name__ == "__main__":
    app.run()
