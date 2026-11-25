import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 10 — Transactions, Demo 2: Orders, Returns, and Two Users at Once

    **OMIS 105 — Introduction to Database Management Systems**

    Demo 1 used a tiny bank. This notebook uses the **ShopSmart** store
    (`data/products.csv`, `data/orders.csv`, `data/order_items.csv`): 64 products,
    200 orders, 607 order items.

    The tables are created **with rules** (keys, `CHECK`, `REFERENCES`) — the same
    `CREATE TABLE` statements as in `transactions_are_explained.md`, "Setup: ShopSmart
    with Rules". The database is a **file** in a temporary folder, so that Section 6
    can open it twice, as two users.

    Every section starts again from the CSV data (the function `load()`), so you can
    run the sections in any order.

    ---

    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell
def _():
    import os
    import tempfile
    from pathlib import Path

    import duckdb
    import pandas as pd

    DATA_DIR = Path(__file__).parent / "data"
    DB_FILE = os.path.join(tempfile.mkdtemp(), "shopsmart.duckdb")
    con = duckdb.connect(DB_FILE)

    def load():
        """(Re)create the three tables with their rules and load the CSV data."""
        for _t in ["refunds", "order_items", "orders", "products"]:  # children first
            con.execute(f"DROP TABLE IF EXISTS {_t}")
        con.execute("""
            CREATE TABLE products (
                product_id     INTEGER PRIMARY KEY,
                product_name   VARCHAR NOT NULL,
                category_id    INTEGER,
                price          DECIMAL(10, 2) NOT NULL CHECK (price > 0),
                stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0)
            )
        """)
        con.execute(f"INSERT INTO products SELECT * FROM read_csv('{DATA_DIR}/products.csv')")
        con.execute("""
            CREATE TABLE orders (
                order_id     INTEGER PRIMARY KEY,
                customer_id  INTEGER NOT NULL,
                order_date   DATE NOT NULL,
                status       VARCHAR NOT NULL,
                total_amount DECIMAL(10, 2) CHECK (total_amount >= 0)
            )
        """)
        con.execute(f"INSERT INTO orders SELECT * FROM read_csv('{DATA_DIR}/orders.csv')")
        con.execute("""
            CREATE TABLE order_items (
                item_id    INTEGER PRIMARY KEY,
                order_id   INTEGER NOT NULL REFERENCES orders(order_id),
                product_id INTEGER NOT NULL REFERENCES products(product_id),
                quantity   INTEGER NOT NULL CHECK (quantity > 0),
                unit_price DECIMAL(10, 2) NOT NULL
            )
        """)
        con.execute(f"INSERT INTO order_items SELECT * FROM read_csv('{DATA_DIR}/order_items.csv')")
        con.execute("""
            CREATE TABLE refunds (
                refund_id     INTEGER PRIMARY KEY,
                order_id      INTEGER NOT NULL REFERENCES orders(order_id),
                refund_date   DATE NOT NULL,
                refund_amount DECIMAL(10, 2) NOT NULL CHECK (refund_amount > 0),
                reason        VARCHAR NOT NULL
            )
        """)

    def run(steps):
        """Run (user, SQL) steps in order; return a transcript of what happened."""
        rows = []
        for who, connection, sql in steps:
            try:
                result = connection.execute(sql).fetchall()
                word = sql.split()[0].upper()
                if word in ("UPDATE", "INSERT", "DELETE"):
                    answer = f"{result[0][0]} row(s) changed"
                elif word == "SELECT":
                    answer = " | ".join(", ".join(str(v) for v in row) for row in result)
                else:
                    answer = "OK"
                rows.append((who, "✅", sql, answer))
            except Exception as e:
                rows.append((who, "❌", sql, str(e).splitlines()[0]))
        return pd.DataFrame(rows, columns=["who", "", "statement", "DuckDB says"])

    load()
    return DB_FILE, con, duckdb, load, run


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The data

    Two numbers to watch: **product 1** (Smartphone X12) has **12** in stock, and
    the newest order is **order 200** (the newest order item is item 607).
    """)
    return


@app.cell
def _(con, load):
    load()
    con.execute("""
        SELECT
            (SELECT COUNT(*) FROM products)    AS products,
            (SELECT COUNT(*) FROM orders)      AS orders,
            (SELECT COUNT(*) FROM order_items) AS order_items,
            (SELECT MAX(order_id) FROM orders) AS newest_order_id,
            (SELECT stock_quantity FROM products WHERE product_id = 1) AS product_1_stock
    """).fetchdf()
    return


@app.cell
def _(con, load):
    load()
    con.execute("""
        SELECT status, COUNT(*) AS num_orders
        FROM orders
        GROUP BY status
        ORDER BY status
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. One order = several statements = one transaction

    Customer 5 buys 2 × product 1 (price $321.52). Placing the order takes **four**
    statements. They belong together: an order without its item, or an item without
    the stock going down, would leave the data wrong.
    """)
    return


@app.cell
def _(con, load, mo, run):
    load()
    _log = run([
        ("app", con, "BEGIN"),
        ("app", con, "INSERT INTO orders VALUES (201, 5, DATE '2025-01-15', 'processing', 643.04)"),
        ("app", con, "INSERT INTO order_items VALUES (608, 201, 1, 2, 321.52)"),
        ("app", con, "UPDATE products SET stock_quantity = stock_quantity - 2 WHERE product_id = 1"),
        ("app", con, "COMMIT"),
        ("app", con, "SELECT order_id, status, total_amount FROM orders WHERE order_id = 201"),
        ("app", con, "SELECT stock_quantity FROM products WHERE product_id = 1"),
    ])
    mo.vstack([_log, mo.md("Order 201 is saved, and the stock of product 1 went from 12 to 10.")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Atomicity and consistency: when one statement fails

    **(a)** The order item names product **99**, which does not exist, so the
    `REFERENCES products(product_id)` rule rejects it. The transaction is aborted,
    so order 201 — inserted one line earlier — is **not** saved either.

    **(b)** Customer 5 wants 20 × product 1, but only 12 are in stock. The
    `CHECK (stock_quantity >= 0)` rule rejects the `UPDATE`, and the whole order is
    rolled back. The database itself protects the stock — even if the application
    forgot to check it.
    """)
    return


@app.cell
def _(con, load, mo, run):
    load()
    _a = run([
        ("app", con, "BEGIN"),
        ("app", con, "INSERT INTO orders VALUES (201, 5, DATE '2025-01-15', 'processing', 150.00)"),
        ("app", con, "INSERT INTO order_items VALUES (608, 201, 99, 2, 75.00)"),
        ("app", con, "ROLLBACK"),
        ("app", con, "SELECT COUNT(*) FROM orders WHERE order_id = 201"),
    ])
    _b = run([
        ("app", con, "BEGIN"),
        ("app", con, "INSERT INTO orders VALUES (201, 5, DATE '2025-01-15', 'processing', 6430.40)"),
        ("app", con, "INSERT INTO order_items VALUES (608, 201, 1, 20, 321.52)"),
        ("app", con, "UPDATE products SET stock_quantity = stock_quantity - 20 WHERE product_id = 1"),
        ("app", con, "ROLLBACK"),
        ("app", con, "SELECT COUNT(*) FROM orders WHERE order_id = 201"),
        ("app", con, "SELECT stock_quantity FROM products WHERE product_id = 1"),
    ])
    mo.vstack([mo.md("**(a)** a product that does not exist"), _a,
               mo.md("**(b)** not enough stock"), _b])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. `place_order()`: a whole order in one Python function

    `place_order(con, customer_id, items)` places one order; `items` is a list of
    `(product_id, quantity)` pairs. Inside **one** transaction it:

    1. creates the order: `order_id` = the largest `order_id` + 1,
       `order_date` = `2025-01-15` (fixed, so the results are the same every run),
       `status` = `'processing'`, `total_amount` = 0 for now;
    2. for each item: finds the product (error if it does not exist), checks
       `stock_quantity` (error if there are not enough), inserts an `order_items`
       row (`item_id` = the largest `item_id` + 1, `unit_price` = the product's
       `price`), and lowers `stock_quantity`;
    3. sets `total_amount` = the sum of `quantity × unit_price`;
    4. commits and returns the new `order_id` — or, on **any** error, rolls back
       and returns `None`.
    """)
    return


@app.cell
def _():
    ORDER_DATE = "2025-01-15"

    def place_order(con, customer_id, items):
        try:
            con.execute("BEGIN")
            order_id = con.execute("SELECT MAX(order_id) + 1 FROM orders").fetchall()[0][0]
            con.execute(
                "INSERT INTO orders VALUES (?, ?, ?, 'processing', 0)",
                [order_id, customer_id, ORDER_DATE],
            )
            total = 0
            for product_id, quantity in items:
                found = con.execute(
                    "SELECT price, stock_quantity FROM products WHERE product_id = ?", [product_id]
                ).fetchall()
                if not found:
                    raise ValueError(f"product {product_id} does not exist")
                price, stock = found[0]
                if stock < quantity:
                    raise ValueError(f"product {product_id}: wanted {quantity}, only {stock} in stock")
                item_id = con.execute("SELECT MAX(item_id) + 1 FROM order_items").fetchall()[0][0]
                con.execute(
                    "INSERT INTO order_items VALUES (?, ?, ?, ?, ?)",
                    [item_id, order_id, product_id, quantity, price],
                )
                con.execute(
                    "UPDATE products SET stock_quantity = stock_quantity - ? WHERE product_id = ?",
                    [quantity, product_id],
                )
                total += quantity * price
            con.execute("UPDATE orders SET total_amount = ? WHERE order_id = ?", [total, order_id])
            con.execute("COMMIT")
            print(f"✅ order {order_id} placed: {len(items)} item(s), total ${total}")
            return order_id
        except Exception as e:
            con.execute("ROLLBACK")
            print(f"❌ order rolled back: {str(e).splitlines()[0]}")
            return None

    return (place_order,)


@app.cell
def _(con, load, place_order):
    load()
    print("(a) a valid order:", place_order(con, 5, [(1, 1), (10, 2), (20, 1)]))
    print("(b) too many:     ", place_order(con, 6, [(1, 1), (2, 500)]))
    print("(c) no product 99:", place_order(con, 7, [(1, 1), (99, 1)]))
    con.execute("""
        SELECT
            (SELECT COUNT(*) FROM orders)      AS orders,
            (SELECT COUNT(*) FROM order_items) AS order_items,
            (SELECT stock_quantity FROM products WHERE product_id = 1) AS product_1_stock
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Only order (a) was saved: 201 orders, 610 order items (607 + 3), and product 1's
    stock went from 12 to 11. Orders (b) and (c) **also** took one of product 1 in
    their first step — and both were rolled back completely.

    ## 5. `process_return()`: a product return

    `process_return(con, order_id, reason)` handles a return. **Only a `completed`
    order can be returned.** Inside one transaction it:

    1. finds the order (error if it does not exist or its `status` is not `'completed'`);
    2. sets the order's `status` to `'cancelled'`;
    3. puts the stock back: for each `order_items` row of the order,
       `stock_quantity` + `quantity`;
    4. inserts a `refunds` row: `refund_id` = the largest `refund_id` + 1 (1 for
       the first), `refund_date` = `2025-01-20` (fixed), `refund_amount` = what the
       customer paid for the items, `SUM(quantity × unit_price)`, and the `reason`;
    5. commits and returns `True` — or rolls back and returns `False`.

    The `refunds` table (created in `load()`):

    ```sql
    CREATE TABLE refunds (
        refund_id     INTEGER PRIMARY KEY,
        order_id      INTEGER NOT NULL REFERENCES orders(order_id),
        refund_date   DATE NOT NULL,
        refund_amount DECIMAL(10, 2) NOT NULL CHECK (refund_amount > 0),
        reason        VARCHAR NOT NULL
    );
    ```
    """)
    return


@app.cell
def _():
    RETURN_DATE = "2025-01-20"

    def process_return(con, order_id, reason):
        try:
            con.execute("BEGIN")
            found = con.execute(
                "SELECT status FROM orders WHERE order_id = ?", [order_id]
            ).fetchall()
            if not found:
                raise ValueError(f"order {order_id} does not exist")
            status = found[0][0]
            if status != "completed":
                raise ValueError(f"order {order_id} is '{status}', only 'completed' orders can be returned")
            con.execute("UPDATE orders SET status = 'cancelled' WHERE order_id = ?", [order_id])
            items = con.execute(
                "SELECT product_id, quantity FROM order_items WHERE order_id = ?", [order_id]
            ).fetchall()
            for product_id, quantity in items:
                con.execute(
                    "UPDATE products SET stock_quantity = stock_quantity + ? WHERE product_id = ?",
                    [quantity, product_id],
                )
            refund_amount = con.execute(
                "SELECT SUM(quantity * unit_price) FROM order_items WHERE order_id = ?", [order_id]
            ).fetchall()[0][0]
            refund_id = con.execute("SELECT COALESCE(MAX(refund_id), 0) + 1 FROM refunds").fetchall()[0][0]
            con.execute(
                "INSERT INTO refunds VALUES (?, ?, ?, ?, ?)",
                [refund_id, order_id, RETURN_DATE, refund_amount, reason],
            )
            con.execute("COMMIT")
            print(f"✅ order {order_id} returned: {len(items)} item(s) back in stock, refund ${refund_amount}")
            return True
        except Exception as e:
            con.execute("ROLLBACK")
            print(f"❌ return rolled back: {str(e).splitlines()[0]}")
            return False

    return (process_return,)


@app.cell
def _(con, load, process_return):
    load()
    print("(a) order 3 (completed):       ", process_return(con, 3, "arrived damaged"))
    print("(b) order 3 again:             ", process_return(con, 3, "arrived damaged"))
    print("(c) order 1 (processing):      ", process_return(con, 1, "changed my mind"))
    print("(d) order 999 (does not exist):", process_return(con, 999, "wrong size"))
    con.execute("SELECT * FROM refunds").fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Only (a) was saved: order 3 is now `cancelled`, its 5 products are back in
    stock, and there is exactly **one** refund, of **$998.35**. (b) failed because order 3 is no
    longer `completed` — the same order cannot be refunded twice.

    Why not refund `orders.total_amount`? In this data set it matches the items in **none** of the
    200 orders (order 3: `total_amount` = $538.49, items = $998.35). A stored total can be wrong;
    the items are what the customer actually bought, so the refund is computed from them.

    ## 6. Isolation: two users at the same time

    Below, the same database file is opened **twice**: `A` and `B` are two users
    (two connections). DuckDB uses **snapshot isolation**: a transaction sees the
    data as it was when the transaction **started**, plus its own changes.

    The four experiments use product 1 (stock **12**, price **$321.52**) and the
    **30** `processing` orders.
    """)
    return


@app.cell
def _(DB_FILE, duckdb, load):
    load()
    user_a = duckdb.connect(DB_FILE)
    user_b = duckdb.connect(DB_FILE)
    return user_a, user_b


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### (a) Dirty read — prevented

    A sets the stock to 0 but has **not** committed. B must not see the 0: A may
    still roll back (and does).
    """)
    return


@app.cell
def _(load, run, user_a, user_b):
    load()
    run([
        ("A", user_a, "BEGIN"),
        ("A", user_a, "UPDATE products SET stock_quantity = 0 WHERE product_id = 1"),
        ("B", user_b, "SELECT stock_quantity FROM products WHERE product_id = 1"),
        ("A", user_a, "ROLLBACK"),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### (b) Non-repeatable read — prevented

    A reads the price twice inside one transaction. In between, B changes the price
    (auto-commit: saved at once). A still sees $321.52 until A's transaction ends; after that, A sees
    the new price.
    """)
    return


@app.cell
def _(load, run, user_a, user_b):
    load()
    run([
        ("A", user_a, "BEGIN"),
        ("A", user_a, "SELECT price FROM products WHERE product_id = 1"),
        ("B", user_b, "UPDATE products SET price = 299.99 WHERE product_id = 1"),
        ("A", user_a, "SELECT price FROM products WHERE product_id = 1"),
        ("A", user_a, "COMMIT"),
        ("A", user_a, "SELECT price FROM products WHERE product_id = 1"),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### (c) Phantom read — prevented

    A counts the `processing` orders twice inside one transaction. In between, B adds
    a new `processing` order and commits. A's count stays 30 until A's transaction
    ends; then A sees 31.
    """)
    return


@app.cell
def _(load, run, user_a, user_b):
    load()
    run([
        ("A", user_a, "BEGIN"),
        ("A", user_a, "SELECT COUNT(*) FROM orders WHERE status = 'processing'"),
        ("B", user_b, "INSERT INTO orders VALUES (201, 5, DATE '2025-01-15', 'processing', 100.00)"),
        ("A", user_a, "SELECT COUNT(*) FROM orders WHERE status = 'processing'"),
        ("A", user_a, "COMMIT"),
        ("A", user_a, "SELECT COUNT(*) FROM orders WHERE status = 'processing'"),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### (d) Lost update — prevented, but B must try again

    A and B each sell **one** product 1. Both read the stock (12), and each
    application computes 12 − 1 = 11 and writes **11**. If both writes were saved,
    the stock would be 11 although **two** were sold — one sale "lost".

    DuckDB does not let that happen: B's write to the **same row** fails at once with
    `Conflict on update!`. B rolls back and tries again — this time with the safe
    form `stock_quantity = stock_quantity - 1`, which lets the database do the math.
    The final stock is 10: both sales counted.
    """)
    return


@app.cell
def _(load, run, user_a, user_b):
    load()
    run([
        ("A", user_a, "BEGIN"),
        ("B", user_b, "BEGIN"),
        ("A", user_a, "SELECT stock_quantity FROM products WHERE product_id = 1"),
        ("B", user_b, "SELECT stock_quantity FROM products WHERE product_id = 1"),
        ("A", user_a, "UPDATE products SET stock_quantity = 11 WHERE product_id = 1"),
        ("B", user_b, "UPDATE products SET stock_quantity = 11 WHERE product_id = 1"),
        ("A", user_a, "COMMIT"),
        ("B", user_b, "ROLLBACK"),
        ("B", user_b, "UPDATE products SET stock_quantity = stock_quantity - 1 WHERE product_id = 1"),
        ("A", user_a, "SELECT stock_quantity FROM products WHERE product_id = 1"),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    | Section | What you saw |
    |---|---|
    | 2 | An order is several statements — they belong in **one** transaction |
    | 3 | **Atomicity** + **consistency**: a `REFERENCES` or `CHECK` error rolls back the whole order |
    | 4 | `place_order()`: check, insert, update stock, set the total — all or nothing |
    | 5 | `process_return()`: only `completed` orders; status, stock and refund change together |
    | 6 | **Isolation** (snapshot): no dirty reads, no non-repeatable reads, no phantoms; a write conflict on the same row is an **error** — roll back and try again |

    **What belongs inside a transaction?** Every group of changes that must happen
    **together**: placing an order, a return, a money transfer, moving stock between
    warehouses.

    **December 3:** review of the whole course — Weeks 1–10.
    """)
    return


if __name__ == "__main__":
    app.run()
