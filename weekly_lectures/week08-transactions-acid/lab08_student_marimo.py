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
    # Lab 8: Transactions & ACID

    ## OMIS 105 — Database Management Systems
    **Week 8 | Estimated time: 75–90 minutes**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Connect to DuckDB, load `categories`, `products`, `customers`,
    `orders`, `order_items`, and `shipping` from `./data/`, and create a
    `bank_accounts` table for the transaction exercises.
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell
def _(con):
    con.execute(
        "CREATE OR REPLACE TABLE categories AS SELECT * FROM read_csv_auto('./data/categories.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE products AS SELECT * FROM read_csv_auto('./data/products.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv_auto('./data/customers.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE orders AS SELECT * FROM read_csv_auto('./data/orders.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE order_items AS SELECT * FROM read_csv_auto('./data/order_items.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE shipping AS SELECT * FROM read_csv_auto('./data/shipping.csv')"
    )
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE OR REPLACE TABLE bank_accounts (
            account_id INTEGER PRIMARY KEY,
            owner_name VARCHAR NOT NULL,
            balance DECIMAL(10,2) CHECK (balance >= 0)
        )
        """
    )
    con.execute("INSERT INTO bank_accounts VALUES (1,'Alice',1000.00)")
    con.execute("INSERT INTO bank_accounts VALUES (2,'Bob',500.00)")
    con.execute("INSERT INTO bank_accounts VALUES (3,'Carol',750.00)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: ACID Concepts (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** In your own words, explain each ACID property (2–3 sentences
    each). Give a ShopSmart example for each.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** For each scenario, identify which ACID property is most at
    risk and explain why:

    a) Two customers simultaneously buy the last item in stock.
    b) The server crashes while processing a multi-item order — 2 of 3
       items were inserted.
    c) A price update sets price to -$5.
    d) After a successful checkout, the order disappears from the
       database.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Basic Transactions (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** Write a transaction that transfers $200 from Alice
    (account 1) to Bob (account 2). Verify the balances before and
    after.
    """)
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM bank_accounts ORDER BY account_id").fetchdf()
    return


@app.cell
def _(con):
    # TODO: replace with your BEGIN / UPDATE / UPDATE / COMMIT transaction
    print("Q3: add your transfer transaction here")
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM bank_accounts ORDER BY account_id").fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** Write a transaction that attempts to transfer $1500 from
    Carol to Alice. What happens when the CHECK constraint is violated?
    Show the balances after the attempt.

    *(Write your explanation here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your BEGIN / UPDATE / UPDATE / COMMIT (wrapped in try/except)
    print("Q4: add your transaction here (wrap it in try/except with ROLLBACK)")
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM bank_accounts ORDER BY account_id").fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** Add a new account for "Dave" with $300, then add a new
    account for "Eve" with $400, then undo only the Eve insert while
    keeping Dave.

    > Note: DuckDB does not implement `SAVEPOINT` /
    `ROLLBACK TO SAVEPOINT` — running them raises a parser error. Use
    two separate transactions instead: commit the Dave insert, then
    begin a second transaction for Eve and roll that one back.

    Verify that Dave exists but Eve does not.
    """)
    return


@app.cell
def _(con):
    # TODO: commit a transaction that inserts Dave
    print("Q5: add your Dave transaction here")
    return


@app.cell
def _(con):
    # TODO: begin a transaction that inserts Eve, then roll it back
    print("Q5: add your Eve transaction here")
    return


@app.cell
def _(con):
    con.execute(
        "SELECT * FROM bank_accounts WHERE account_id IN (4, 5)"
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Transaction Patterns (20 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6.** Write a Python function `transfer(con, from_id, to_id,
    amount)` that:
    - Begins a transaction
    - Checks that the sender has sufficient balance
    - Performs the transfer
    - Commits on success, rolls back on failure
    - Returns True/False

    Test it with: (a) a valid transfer, (b) insufficient funds, (c) a
    non-existent account.
    """)
    return


@app.cell
def _(con):
    # TODO: define transfer(con, from_id, to_id, amount)
    print("Q6: define your transfer() function here")
    return


@app.cell
def _(con):
    # TODO: test transfer() with a valid transfer, insufficient funds,
    # and a non-existent account
    print("Q6: call transfer() with your test cases here")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** Write a Python function `place_order(con, customer_id,
    items)` where `items` is a list of `(product_id, quantity)` tuples.
    The function should:
    - Begin a transaction
    - Create a new order record
    - For each item: check stock, insert order_item, decrement stock
    - If any item fails, roll back the entire order
    - Update the order total on success
    - Commit

    Test with a valid order and an order with an out-of-stock item.
    """)
    return


@app.cell
def _(con):
    # TODO: define place_order(con, customer_id, items)
    print("Q7: define your place_order() function here")
    return


@app.cell
def _(con):
    # TODO: test place_order() with a valid order and one with a missing product
    print("Q7: call place_order() with your test cases here")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: Concurrency Analysis (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8.** Consider this scenario with two transactions running
    concurrently:

    ```
    T1: BEGIN; SELECT balance FROM accounts WHERE id=1; -- reads $1000
    T2: BEGIN; SELECT balance FROM accounts WHERE id=1; -- reads $1000
    T1: UPDATE accounts SET balance=1000-200=800 WHERE id=1; COMMIT;
    T2: UPDATE accounts SET balance=1000-300=700 WHERE id=1; COMMIT;
    ```

    a) What is the final balance? What should it be?
    b) Which concurrency problem is this?
    c) How would you fix this? Show the corrected SQL.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9.** For each isolation level (READ UNCOMMITTED, READ COMMITTED,
    REPEATABLE READ, SERIALIZABLE), describe a ShopSmart scenario where
    that level would be appropriate or inappropriate.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Real-World Design (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** Design a complete transaction for a "product return"
    workflow at ShopSmart. The transaction should:
    - Update the order status to 'cancelled' (the `orders.status` CHECK
      constraint only allows 'processing', 'shipped', 'completed', or
      'cancelled')
    - Restore the product stock
    - Create a refund record (design the refund table yourself)
    - Handle errors gracefully

    Write both the CREATE TABLE for the refund table and the Python
    function for the transaction.
    """)
    return


@app.cell
def _(con):
    # TODO: CREATE TABLE for your refund table
    print("Q10: add your refund table CREATE TABLE statement here")
    return


@app.cell
def _(con):
    # TODO: define process_return(con, order_id, reason="Customer return")
    print("Q10: define your process_return() function here")
    return


@app.cell
def _(con):
    # TODO: test process_return() on a completed order
    print("Q10: call process_return() with a completed order_id here")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Submission

    - Submit notebook with all code, queries, outputs, and written
      explanations
    - **Total: 75 points**
    """)
    return


if __name__ == "__main__":
    app.run()
