import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 8: Transactions & ACID — Demo Notebook
    ## OMIS 105: Database Management Systems
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect()
    for t, f in [('categories','./data/categories.csv'),
                 ('products','./data/products.csv'),
                 ('customers','./data/customers.csv'),
                 ('orders','./data/orders.csv'),
                 ('order_items','./data/order_items.csv'),
                 ('shipping','./data/shipping.csv')]:
        con.sql(f"CREATE OR REPLACE TABLE {t} AS SELECT * FROM read_csv_auto('{f}')")
        print(f"Loaded {t}: {con.sql(f'SELECT COUNT(*) FROM {t}').fetchone()[0]} rows")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Basic Transaction: BEGIN, COMMIT, ROLLBACK
    """)
    return


@app.cell
def _(con):
    # Check current state
    con.sql("""
        SELECT
            product_name,
            stock_quantity
        FROM products
        WHERE product_id = 1;
    """).show()
    return


@app.cell
def _(con):
    # Successful transaction
    con.execute("""
        BEGIN TRANSACTION;
    """)
    con.execute("""
        UPDATE products
        SET stock_quantity = stock_quantity - 1
        WHERE product_id = 1;
    """)
    con.execute("COMMIT")

    con.sql("""
        SELECT
            product_name,
            stock_quantity
        FROM products
        WHERE product_id = 1;
    """).show()
    print("Transaction committed — stock decreased by 1")
    return


@app.cell
def _(con):
    # Transaction with ROLLBACK
    original = con.sql("""
        SELECT stock_quantity
        FROM products
        WHERE product_id = 1;
    """).fetchone()[0]
    print(f"Before: stock = {original}")

    con.execute("""
        BEGIN TRANSACTION;
    """)
    con.execute("""
        UPDATE products
        SET stock_quantity = 0
        WHERE product_id = 1;
    """)

    # Check inside transaction
    inside = con.sql("SELECT stock_quantity FROM products WHERE product_id = 1").fetchone()[0]
    print(f"Inside transaction: stock = {inside}")

    con.execute("ROLLBACK")

    after = con.sql("SELECT stock_quantity FROM products WHERE product_id = 1").fetchone()[0]
    print(f"After ROLLBACK: stock = {after}")
    print("Change was undone!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Atomicity — All or Nothing
    """)
    return


@app.cell
def _(con, product_id):
    # Simulate placing an order (multi-step transaction)
    def place_order(con, customer_id, product_id, quantity):
        try:
            con.execute("""
                BEGIN TRANSACTION;
            """)

            # Step 1: Check stock
            stock = con.sql(f"SELECT stock_quantity FROM products WHERE product_id = {product_id}").fetchone()[0]
            if stock < quantity:
                raise Exception(f"Insufficient stock: {stock} < {quantity}")

            # Step 2: Create order
            max_oid = con.sql("""
                SELECT COALESCE(MAX(order_id), 0) + 1
                FROM orders;
            """).fetchone()[0]
            price = con.sql(f"SELECT price FROM products WHERE product_id = {product_id}").fetchone()[0]
            total = round(price * quantity, 2)

            con.execute(f"INSERT INTO orders VALUES ({max_oid}, {customer_id}, CURRENT_DATE, 'processing', {total})")

            # Step 3: Create order item
            max_iid = con.sql("""
                SELECT COALESCE(MAX(item_id), 0) + 1
                FROM order_items;
            """).fetchone()[0]
            con.execute(f"INSERT INTO order_items VALUES ({max_iid}, {max_oid}, {product_id}, {quantity}, {price})")

            # Step 4: Update stock
            con.execute(f"UPDATE products SET stock_quantity = stock_quantity - {quantity} WHERE product_id = {product_id}")

            con.execute("COMMIT")
            print(f"Order {max_oid} placed successfully! Total: ${total}")
            return True

        except Exception as e:
            con.execute("ROLLBACK")
            print(f"Order FAILED and rolled back: {e}")
            return False

    # Test: successful order
    place_order(con, customer_id=1, product_id=1, quantity=1)
    return (place_order, stock)


@app.cell
def _(con, place_order):
    # Test: failed order (insufficient stock)
    con.sql("""
        SELECT
            product_name,
            stock_quantity
        FROM products
        WHERE product_id = 1;
    """).show()

    # Try to buy more than available
    place_order(con, customer_id=2, product_id=1, quantity=99999)

    # Verify stock unchanged
    con.sql("SELECT product_name, stock_quantity FROM products WHERE product_id = 1").show()
    print("Stock unchanged — atomicity preserved!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Consistency — Constraints Are Enforced
    """)
    return


@app.cell
def _(con):
    # Create a table with constraints
    con.sql("""
        CREATE OR REPLACE TABLE bank_accounts (
            account_id INTEGER PRIMARY KEY,
            owner_name VARCHAR NOT NULL,
            balance    DECIMAL(10,2) CHECK (balance >= 0)
        );
    """)
    con.execute("""
        INSERT INTO bank_accounts
        VALUES (1, 'Alice', 500.00);
    """)
    con.execute("""
        INSERT INTO bank_accounts
        VALUES (2, 'Bob', 200.00);
    """)
    con.sql("""
        SELECT *
        FROM bank_accounts;
    """).show()
    return


@app.cell
def _(con):
    # Consistency: transfer that would make balance negative
    try:
        con.execute("BEGIN")
        con.execute("""
            UPDATE bank_accounts
            SET balance = balance - 600
            WHERE account_id = 1;
        """)
        con.execute("""
            UPDATE bank_accounts
            SET balance = balance + 600
            WHERE account_id = 2;
        """)
        con.execute("COMMIT")
        print("Transfer succeeded")
    except Exception as e:
        con.execute("ROLLBACK")
        print(f"Transfer REJECTED (consistency violation): {e}")

    con.sql("""
        SELECT *
        FROM bank_accounts;
    """).show()
    print("Balances unchanged — consistency preserved!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Savepoints — Partial Rollback
    """)
    return


@app.cell
def _(con):
    # ── Note: DuckDB does NOT support SAVEPOINT / partial rollback ──
    # DuckDB transactions are single-level: BEGIN, then either COMMIT or
    # ROLLBACK (all-or-nothing). There is no SAVEPOINT / ROLLBACK TO SAVEPOINT.

    # (a) Show that DuckDB rejects SAVEPOINT
    con.execute("BEGIN")
    con.execute("INSERT INTO bank_accounts VALUES (3, 'Carol', 300.00);")
    try:
        con.execute("SAVEPOINT after_carol")
    except Exception as e:
        print("⚠️  SAVEPOINT is not supported by DuckDB:")
        print("   ", e)
    con.execute("ROLLBACK")  # only a full rollback is available

    # (b) DuckDB-compatible way to get the same "keep Carol, undo Dave" result:
    #     COMMIT the part you want to keep, use a SEPARATE transaction for the
    #     part you might undo, and ROLLBACK that one.
    con.execute("BEGIN")
    con.execute("INSERT INTO bank_accounts VALUES (3, 'Carol', 300.00);")
    con.execute("COMMIT")
    print("After committing Carol:")
    con.sql("SELECT * FROM bank_accounts").show()

    con.execute("BEGIN")
    con.execute("INSERT INTO bank_accounts VALUES (4, 'Dave', 400.00);")
    con.execute("ROLLBACK")
    print("After rolling back Dave's separate transaction (Dave undone):")
    con.sql("SELECT * FROM bank_accounts").show()

    print("\nFinal state (Carol kept, Dave undone) — achieved without SAVEPOINT:")
    con.sql("SELECT * FROM bank_accounts").show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Simulating Concurrency Problems

    Since DuckDB is single-connection, we simulate to illustrate concepts.
    """)
    return


@app.cell
def _(con):
    # Simulating a Lost Update problem
    print("=== Lost Update Simulation ===")
    print()

    # Both "users" read the same stock level
    stock = con.sql("""
        SELECT stock_quantity
        FROM products
        WHERE product_id = 2;
    """).fetchone()[0]
    print(f"User A reads stock: {stock}")
    print(f"User B reads stock: {stock}")

    # User A buys 1
    new_stock_a = stock - 1
    con.execute(f"UPDATE products SET stock_quantity = {new_stock_a} WHERE product_id = 2")
    print(f"User A writes stock: {new_stock_a}")

    # User B also buys 1, but based on stale read
    new_stock_b = stock - 1  # Same starting value!
    con.execute(f"UPDATE products SET stock_quantity = {new_stock_b} WHERE product_id = 2")
    print(f"User B writes stock: {new_stock_b}")

    final = con.sql("SELECT stock_quantity FROM products WHERE product_id = 2").fetchone()[0]
    print(f"\nFinal stock: {final}")
    print(f"Expected (two items sold): {stock - 2}")
    print(f"Lost update! One sale was lost.")
    return (stock,)


@app.cell
def _(con, stock):
    # The correct approach: use atomic UPDATE
    # Reset stock
    con.execute(f"UPDATE products SET stock_quantity = {stock} WHERE product_id = 2")

    # Atomic decrements — no read-then-write race condition
    con.execute("""
        UPDATE products
        SET stock_quantity = stock_quantity - 1
        WHERE product_id = 2;
    """)
    con.execute("UPDATE products SET stock_quantity = stock_quantity - 1 WHERE product_id = 2")

    final2 = con.sql("""
        SELECT stock_quantity
        FROM products
        WHERE product_id = 2;
    """).fetchone()[0]
    print(f"Correct final stock: {final2} (expected {stock - 2})")
    print("Using atomic UPDATE avoids the lost update problem!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Error Handling Pattern
    """)
    return


@app.cell
def _(con):
    # Robust transaction template
    def safe_transaction(con, operations, description="Transaction"):
        try:
            con.execute("BEGIN")
            for op in operations:
                con.execute(op)
            con.execute("COMMIT")
            print(f"{description}: COMMITTED successfully")
            return True
        except Exception as e:
            con.execute("ROLLBACK")
            print(f"{description}: ROLLED BACK due to error: {e}")
            return False

    # Test with valid operations
    safe_transaction(con, [
        """
            UPDATE products
            SET price = price * 1.05
            WHERE category_id = 1;
        """,
    ], "5% Electronics price increase")

    # Test with invalid operation
    safe_transaction(con, [
        """
            UPDATE products
            SET price = price * 1.05
            WHERE category_id = 2;
        """,
        """
            INSERT INTO nonexistent_table
            VALUES (1, 2, 3);
        """,
    ], "Books price increase + bad insert")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Transaction in a Real Workflow: Order Processing
    """)
    return


@app.cell
def _(con):
    # Full order processing pipeline
    def process_order(con, customer_id, items):
        """
        items: list of (product_id, quantity)
        """
        try:
            con.execute("BEGIN")
            
            # 1. Create order
            oid = con.sql("""
                SELECT COALESCE(MAX(order_id),0)+1
                FROM orders;
            """).fetchone()[0]
            con.execute(f"INSERT INTO orders VALUES ({oid},{customer_id},CURRENT_DATE,'processing',0)")
            # (DuckDB has no SAVEPOINT; on any error below we ROLLBACK the whole txn)

            total = 0
            iid = con.sql("""
                SELECT COALESCE(MAX(item_id),0)
                FROM order_items;
            """).fetchone()[0]
            
            # 2. Add each item
            for product_id, qty in items:
                iid += 1
                stock = con.sql(f"SELECT stock_quantity FROM products WHERE product_id={product_id}").fetchone()
                if stock is None:
                    raise Exception(f"Product {product_id} not found")
                if stock[0] < qty:
                    raise Exception(f"Product {product_id}: need {qty}, only {stock[0]} available")
                
                price = con.sql(f"SELECT price FROM products WHERE product_id={product_id}").fetchone()[0]
                line = round(price * qty, 2)
                total += line
                
                con.execute(f"INSERT INTO order_items VALUES ({iid},{oid},{product_id},{qty},{price})")
                con.execute(f"UPDATE products SET stock_quantity=stock_quantity-{qty} WHERE product_id={product_id}")
            
            # 3. Update order total
            con.execute(f"UPDATE orders SET total_amount={round(total,2)} WHERE order_id={oid}")
            
            con.execute("COMMIT")
            print(f"Order {oid} committed: {len(items)} items, total ${total:.2f}")
            return oid
            
        except Exception as e:
            con.execute("ROLLBACK")
            print(f"Order FAILED: {e}")
            return None

    # Successful multi-item order
    process_order(con, 1, [(1, 1), (10, 2), (20, 1)])
    return (process_order, product_id, stock)


@app.cell
def _(con, process_order):
    # Failed order (one item out of stock) — everything rolls back
    process_order(con, 2, [(1, 1), (999, 1)])  # product 999 doesn't exist
    print("\nNo partial order was created — atomicity in action!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    Key concepts demonstrated:
    - **BEGIN/COMMIT/ROLLBACK**: Transaction lifecycle
    - **Atomicity**: Multi-step operations are all-or-nothing
    - **Consistency**: Constraint violations cause rollback
    - **Savepoints**: Partial rollback within a transaction
    - **Lost Update**: Why atomic UPDATE is essential
    - **Error handling**: Always ROLLBACK on exceptions
    - **Real-world pattern**: Order processing as a transaction

    **Next week**: Capstone Project — apply everything you've learned!
    """)
    return


if __name__ == "__main__":
    app.run()
