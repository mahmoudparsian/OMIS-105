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
    # Transactions in Action — A DuckDB Banking Tutorial

    **What you'll learn:**

    1. What a transaction is and why it matters
    2. `BEGIN TRANSACTION`, `COMMIT`, and `ROLLBACK`
    3. How transactions keep your data consistent (the classic bank-transfer example)
    4. What happens when things go wrong mid-transaction
    5. Autocommit vs. explicit transactions
    6. Savepoints — partial rollbacks inside a transaction

    ---

    ## Prerequisites

    You only need **Python 3** and the **duckdb** package. Let's install it and get started.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Table of Contents:


    1. **What a transaction is** — ACID properties explained simply
    2. **Schema setup** — two customers (Alice & Bob) with checking/savings accounts and a `CHECK (balance >= 0)` constraint
    3. **Autocommit** — how single statements commit automatically
    4. **BEGIN + COMMIT** — a step-by-step transfer from Alice's checking to savings
    5. **ROLLBACK** — Bob starts a transfer then changes his mind
    6. **Automatic rollback on error** — Alice tries to overdraw, the CHECK constraint saves the day
    7. **Reusable transfer function** — a production-style Python function with proper error handling
    8. **Consistency check** — verifying total money in the system never changes from internal transfers
    9. **Syntax cheat sheet** — all the equivalent forms (`BEGIN` vs `START TRANSACTION`, etc.)
    10. **Common mistakes** — forgetting to commit, nesting BEGINs
    11. **Multi-transfer scenario** — payday processing as one atomic batch
    12. **Summary** with the golden rule


    ### To run this notebook:

    ```
    To run it, just open it in Jupyter and 
    make sure you have `duckdb` installed 
    (`pip install duckdb`). 

    Every cell runs top-to-bottom with no 
    external dependencies.
    ```
    """)
    return


@app.cell
def _():
    # Install duckdb if you don't have it yet
    return


@app.cell
def _():
    import duckdb
    print(f"DuckDB version: {duckdb.__version__}")
    return (duckdb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1 — What Is a Transaction?

    ```
    A **transaction** is a group of SQL 
    statements that are treated as a single, 
    indivisible unit of work.
    ```

    ### Transfer money($)
    ```   
    Think of it like this: when you transfer money 
    from your checking account to your savings account, 
    **two things** must happen:
    ```

    1. Subtract the amount from checking.
    2. Add the amount to savings.

    > If only step 1 happens (the system crashes before step 2), <br>
    > your money has vanished! A transaction guarantees that     <br>
    > **either both steps happen, or neither does**.

    This is the **A** in the famous **ACID** properties:

    | Property      | Meaning |
    |:--------------|:--------|
    | **A**tomicity  | All-or-nothing — every statement in the transaction succeeds, or they all get rolled back |
    | **C**onsistency| The database moves from one valid state to another |
    | **I**solation  | Concurrent transactions don't interfere with each other |
    | **D**urability | Once committed, the data survives crashes |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2 — Set Up the Banking Schema

    We'll create a tiny bank with:
    - A `customers` table
    - An `accounts` table (each customer can have multiple accounts)
    - A `transactions_log` table to record every transfer

    We use an **in-memory** DuckDB database so nothing is written to disk.
    """)
    return


@app.cell
def _(duckdb):
    # Create a fresh in-memory database
    con = duckdb.connect()

    # --- Schema ---
    con.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name        VARCHAR NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE accounts (
            account_id   INTEGER PRIMARY KEY,
            customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
            account_type VARCHAR NOT NULL,
            /* 'checking' or 'savings' */          balance DECIMAL(12, 2) NOT NULL,
            CHECK        (balance >= 0) /* no negative balances! */
        );
    """)

    con.execute("""
        CREATE TABLE transactions_log (
            txn_id       INTEGER PRIMARY KEY,
            from_account INTEGER REFERENCES accounts(account_id),
            to_account   INTEGER REFERENCES accounts(account_id),
            amount       DECIMAL(12, 2) NOT NULL,
            description  VARCHAR,
            created_at   TIMESTAMP DEFAULT current_timestamp
        );
    """)

    # --- Seed data ---
    con.execute("""
        INSERT INTO customers
        VALUES
            (1, 'Alice'),
            (2, 'Bob');
    """)

    con.execute("""
        INSERT INTO accounts
        VALUES
            (101, 1, 'checking', 1000.00),
            (102, 1, 'savings', 5000.00),
            (201, 2, 'checking', 2500.00),
            (202, 2, 'savings', 8000.00);
    """)

    print("Schema created and seed data loaded!")
    con.sql("""
        SELECT *
        FROM accounts;
    """).show()
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `CHECK (balance >= 0)`
    ```
    Notice the `CHECK (balance >= 0)` constraint 
    on the `accounts` table — it prevents any account 
    from going negative. 

    This will be important later when we see how 
    transactions handle errors.
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3 — Autocommit Mode (The Default)

    * By default, DuckDB runs in **autocommit** mode. 
    * Every single SQL statement is its own mini-transaction — <br>
    it's automatically committed the moment it finishes.

    ## Transaction in Action:
        
    Let's see this in action: we'll give Bob a <br>
    $100 bonus and confirm it sticks immediately.
    """)
    return


@app.cell
def _(con):
    # This UPDATE is auto-committed — no BEGIN/COMMIT needed
    con.execute("""
        UPDATE accounts
        SET balance = balance + 100
        WHERE account_id = 201;
    """)

    print("Bob's checking after $100 bonus:")
    con.sql("""
        SELECT *
        FROM accounts
        WHERE customer_id = 2;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Bob's checking balance went from `$2,500` to `$2,600`. <br>
    Since we didn't use `BEGIN`, DuckDB auto-committed     <br>
    the change right away.

    **Autocommit** is fine for single statements, but what <br>
    if we need **multiple statements to succeed or fail    <br>
    together**? That's where explicit transactions come in.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4 — Your First Explicit Transaction: BEGIN + COMMIT

    Let's transfer $200 from Alice's checking (101) to Alice's savings (102).

    The pattern is:

    ```sql
    BEGIN TRANSACTION;          -- open the transaction
       ... do work ...
    COMMIT;                     -- make it permanent
    ```
    """)
    return


@app.cell
def _(con):
    print("=== BEFORE transfer ===")
    con.sql("""
        SELECT *
        FROM accounts
        WHERE customer_id = 1;
    """).show()

    # --- Explicit transaction ---
    con.execute("""
        BEGIN TRANSACTION;
    """)

    # Step 1: Debit Alice's checking
    con.execute("""
        UPDATE accounts
        SET balance = balance - 200
        WHERE account_id = 101;
    """)

    # Step 2: Credit Alice's savings
    con.execute("""
        UPDATE accounts
        SET balance = balance + 200
        WHERE account_id = 102;
    """)

    # Step 3: Log the transfer
    con.execute("""
        INSERT INTO transactions_log
        VALUES (1, 101, 102, 200.00, 'Alice: checking -> savings', current_timestamp);
    """)

    # Make it permanent!
    con.execute("COMMIT;")

    print("=== AFTER transfer ===")
    con.sql("SELECT * FROM accounts WHERE customer_id = 1").show()
    print("=== Transaction Log ===")
    con.sql("""
        SELECT *
        FROM transactions_log;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What happened:**

    - Alice's checking went from `$1,000` → `$800`
    - Alice's savings went from `$5,000` → `$5,200`
    - The total money in Alice's accounts stayed the same ($6,000) — that's consistency!
    - A log entry was recorded
    - All three statements were bundled into one atomic unit. 
    - If any one had failed, **none** of them would have taken effect.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5 — ROLLBACK: Undoing a Transaction

    Sometimes you start a transaction and then    <br>
    realize you don't want to go through with it. <br>
    `ROLLBACK` discards all changes made since `BEGIN`.

    #### ***Let's say Bob accidentally starts a transfer he did NOT mean to make.***
    """)
    return


@app.cell
def _(con):
    print("=== BEFORE (Bob's accounts) ===")
    con.sql("""
        SELECT *
        FROM accounts
        WHERE customer_id = 2;
    """).show()

    # Start a transaction
    con.execute("""
        BEGIN TRANSACTION;
    """)

    # Oops — Bob transfers $1,000 from checking to savings
    con.execute("""
        UPDATE accounts
        SET balance = balance - 1000
        WHERE account_id = 201;
    """)
    con.execute("""
        UPDATE accounts
        SET balance = balance + 1000
        WHERE account_id = 202;
    """)

    # Let's peek at the data INSIDE the transaction (not yet committed)
    print("=== DURING transaction (uncommitted) ===")
    con.sql("SELECT * FROM accounts WHERE customer_id = 2").show()

    # Wait — Bob changed his mind!
    con.execute("ROLLBACK;")
    print(">>> ROLLBACK executed! <<<\n")

    print("=== AFTER rollback (Bob's accounts) ===")
    con.sql("SELECT * FROM accounts WHERE customer_id = 2").show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Key takeaway:** <br>
    During the transaction, the data *looked* changed. <br>
    But after `ROLLBACK`, everything snapped back to   <br>
    exactly how it was before `BEGIN`. 

    It's like the transfer never happened.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6 — Automatic Rollback on Error

    Remember our `CHECK (balance >= 0)` constraint? <br>
    Let's see what happens when a transaction violates it.

    Alice only has `$800` in checking. <br>
    What if she tries to transfer `$5,000`?
    """)
    return


@app.cell
def _(con, duckdb):
    print("=== BEFORE (Alice's accounts) ===")
    con.sql("""
        SELECT *
        FROM accounts
        WHERE customer_id = 1;
    """).show()

    try:
        con.execute("""
            BEGIN TRANSACTION;
        """)
        
        # Try to withdraw $5,000 from checking (only has $800!)
        con.execute("""
            UPDATE accounts
            SET balance = balance - 5000
            WHERE account_id = 101;
        """)
        
        # This would credit savings, but we'll never get here if the CHECK fails
        con.execute("""
            UPDATE accounts
            SET balance = balance + 5000
            WHERE account_id = 102;
        """)
        
        con.execute("COMMIT;")
        print("Transfer committed successfully.")

    except duckdb.Error as e:
        print(f"ERROR: {e}")
        # The transaction is already invalidated by the error;
        # we issue ROLLBACK to cleanly close it.
        try:
            con.execute("ROLLBACK;")
            print("Transaction rolled back.")
        except:
            pass  # already rolled back automatically

    print("\n=== AFTER failed transaction (Alice's accounts) ===")
    con.sql("SELECT * FROM accounts WHERE customer_id = 1").show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What happened:**

    * The `CHECK (balance >= 0)` constraint caught the problem. 
    * The entire transaction was rolled back 
    * Alice's balances are unchanged. 
    * This is **atomicity** in action: the debit failed, so the credit never happened either.

    > **Tip:** In DuckDB, once any statement inside a     <br>
    > transaction fails, the transaction is automatically <br>
    > marked as "aborted." <br>
    > You must issue `ROLLBACK` to clean up before you can run new statements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7 — A Realistic Transfer Function

    Let's wrap everything we've learned  <br> 
    into a reusable Python function that <br>
    performs a safe bank transfer.
    """)
    return


@app.cell
def _(amount, con):
    def transfer(con, from_acct, to_acct, amount, description=""):
        """
        Transfer money between accounts using a transaction.
        Returns True on success, False on failure.
        """
        try:
            con.execute("""
                BEGIN TRANSACTION;
            """)
            
            # 1. Check that the source account has enough funds
            result = con.execute(
                """
                    SELECT balance
                    FROM accounts
                    WHERE account_id = ?;
                """, [from_acct]
            ).fetchone()
            
            if result is None:
                raise ValueError(f"Account {from_acct} does not exist.")
            
            current_balance = result[0]
            if current_balance < amount:
                raise ValueError(
                    f"Insufficient funds: balance is ${current_balance:.2f}, "
                    f"but transfer requires ${amount:.2f}"
                )
            
            # 2. Debit the source
            con.execute(
                """
                    UPDATE accounts
                    SET balance = balance - ?
                    WHERE account_id = ?;
                """,
                [amount, from_acct]
            )
            
            # 3. Credit the destination
            con.execute(
                """
                    UPDATE accounts
                    SET balance = balance + ?
                    WHERE account_id = ?;
                """,
                [amount, to_acct]
            )
            
            # 4. Log the transfer
            con.execute("""
                INSERT INTO transactions_log
                VALUES ( (
                SELECT COALESCE(MAX(txn_id), 0) + 1
                FROM transactions_log), ?, ?, ?, ?, current_timestamp );
            """, [from_acct, to_acct, amount, description])
            
            # 5. Commit!
            con.execute("COMMIT;")
            print(f"SUCCESS: Transferred ${amount:.2f} from {from_acct} -> {to_acct}")
            return True
            
        except Exception as e:
            print(f"FAILED: {e}")
            try:
                con.execute("ROLLBACK;")
            except:
                pass
            return False
    return (transfer,)


@app.cell
def _(con, transfer):
    # --- Test the transfer function ---

    print("=== Test 1: Valid transfer (Bob checking -> Bob savings, $500) ===")
    transfer(con, 201, 202, 500, "Bob: checking -> savings")

    print("\n=== Test 2: Insufficient funds (Alice checking -> Bob checking, $9999) ===")
    transfer(con, 101, 201, 9999, "Alice -> Bob (too much!)")

    print("\n=== Test 3: Cross-customer transfer (Alice savings -> Bob checking, $1000) ===")
    transfer(con, 102, 201, 1000, "Alice savings -> Bob checking")

    print("\n=== Final account balances ===")
    con.sql("""
        SELECT *
        FROM accounts
        ORDER BY account_id;
    """).show()

    print("=== Full transaction log ===")
    con.sql("""
        SELECT *
        FROM transactions_log
        ORDER BY txn_id;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What happened?
    * Test 1 and Test 3 succeeded, 
    * while Test 2 was correctly rejected. 
    * The failed transfer left no trace — no partial updates, no orphaned log entries.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 8 — Verifying Consistency: The Money Never Disappears

    ```
    A good sanity check for any banking system: 
    the **total money across all accounts** should 
    only change when money enters or leaves the 
    system (like the $100 bonus we gave Bob earlier), 
    never during internal transfers.
    ```
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            SUM(balance) AS total_money_in_system,
            COUNT(*) AS number_of_accounts
        FROM accounts;
    """).show()

    # Original totals: Alice had 1000+5000=6000, Bob had 2500+8000=10500
    # Plus Bob's $100 bonus = 16,600 total
    # All transfers were internal, so the total should still be 16,600
    print("Expected total: $16,600.00")
    print("(Original $16,500 + Bob's $100 bonus)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 9 — Transaction Syntax Cheat Sheet

    DuckDB supports several equivalent ways to write transaction commands:

    | Action | SQL Syntax (all equivalent) |
    |:-------|:---------------------------|
    | Start  | `BEGIN TRANSACTION;` or `BEGIN;` or `START TRANSACTION;` |
    | Save   | `COMMIT;` or `COMMIT TRANSACTION;` |
    | Undo   | `ROLLBACK;` or `ROLLBACK TRANSACTION;` or `ABORT;` |

    Let's verify that the short forms work too:
    """)
    return


@app.cell
def _(con):
    # Short form: BEGIN ... COMMIT
    con.execute("BEGIN;")
    con.execute("""
        UPDATE accounts
        SET balance = balance + 1
        WHERE account_id = 101;
    """)
    con.execute("COMMIT;")
    print("Short form BEGIN/COMMIT works!")

    # Short form: BEGIN ... ROLLBACK
    con.execute("BEGIN;")
    con.execute("""
        UPDATE accounts
        SET balance = balance + 9999
        WHERE account_id = 101;
    """)
    con.execute("ROLLBACK;")
    print("Short form BEGIN/ROLLBACK works!")

    # Verify only the +1 stuck
    con.sql("""
        SELECT
            account_id,
            balance
        FROM accounts
        WHERE account_id = 101;
    """).show()
    print("(The $1 from COMMIT stuck; the $9,999 from ROLLBACK did not)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 10 — Common Mistakes & Tips

    ### Mistake 1: Forgetting to COMMIT

    ```
    If you `BEGIN` a transaction but never 
    `COMMIT` or `ROLLBACK`, the transaction 
    stays open. 
        
    In DuckDB's Python API, the connection 
    closing will implicitly roll back any 
    uncommitted transaction.
    ```
    """)
    return


@app.cell
def _(duckdb):
    # Demonstrate: forgetting to commit
    temp_con = duckdb.connect()  # fresh connection
    temp_con.execute("""
        CREATE TABLE demo (
            x INT
        );
    """)
    temp_con.execute("""
        INSERT INTO demo
        VALUES (1);
    """)

    # Start a transaction but never commit...
    temp_con.execute("BEGIN;")
    temp_con.execute("""
        INSERT INTO demo
        VALUES (2);
    """)
    temp_con.execute("""
        INSERT INTO demo
        VALUES (3);
    """)
    # Oops — we close without committing!
    temp_con.close()

    # Reconnect and check — rows 2 and 3 are gone
    # (In-memory DB is gone entirely, but the principle holds for file-based DBs)
    print("If this were a file-based DB, rows 2 and 3 would be lost.")
    print("Lesson: Always COMMIT or ROLLBACK your transactions!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Mistake 2: Nesting BEGINs

    ```
    DuckDB does **not** support nested transactions. 

    If you call `BEGIN` while a transaction is already 
    open, you'll get an error.
    ```
    """)
    return


@app.cell
def _(con, duckdb):
    try:
        con.execute("BEGIN;")
        con.execute("BEGIN;")  # This will fail!
    except duckdb.Error as e:
        print(f"Error: {e}")
        con.execute("ROLLBACK;")  # Clean up the first transaction
        print("Lesson: You can't nest BEGIN statements in DuckDB.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Tip: Use Python's try/except Pattern

    #### The safest pattern for transactions in Python is:

    ```python
    try:
        con.execute("BEGIN TRANSACTION;")
        # ... your SQL statements ...
        con.execute("COMMIT;")
    except Exception as e:
        con.execute("ROLLBACK;")
        raise  # or handle the error
    ```

    This guarantees the transaction is always properly closed, even if something goes wrong.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 11 — Putting It All Together: A Multi-Transfer Scenario

    Let's simulate a realistic scenario: **payday processing** where multiple employees get paid.
    """)
    return


@app.cell
def _(con):
    # First, let's see current state
    print("=== Balances BEFORE payday ===")
    con.sql("""
        SELECT
            a.account_id,
            c.name,
            a.account_type,
            a.balance
        FROM accounts a
        JOIN customers c ON a.customer_id = c.customer_id
        ORDER BY a.account_id;
    """).show()

    # Payday: deposit salaries into checking accounts
    # This should be all-or-nothing — either everyone gets paid, or no one does
    payroll = [
        (101, 3000.00, "Salary deposit - Alice"),
        (201, 2800.00, "Salary deposit - Bob"),
    ]

    try:
        con.execute("""
            BEGIN TRANSACTION;
        """)
        
        for account_id, amount, desc in payroll:
            con.execute(
                """
                    UPDATE accounts
                    SET balance = balance + ?
                    WHERE account_id = ?;
                """,
                [amount, account_id]
            )
            con.execute("""
                INSERT INTO transactions_log
                VALUES ( (
                SELECT COALESCE(MAX(txn_id), 0) + 1
                FROM transactions_log), NULL, ?, ?, ?, current_timestamp );
            """, [account_id, amount, desc])
            print(f"  Processed: {desc} (${amount:.2f})")
        
        con.execute("COMMIT;")
        print("\nPayroll committed successfully!")
        
    except Exception as e:
        con.execute("ROLLBACK;")
        print(f"\nPayroll FAILED and rolled back: {e}")

    print("\n=== Balances AFTER payday ===")
    con.sql("""
        SELECT a.account_id, c.name, a.account_type, a.balance
        FROM accounts a
        JOIN customers c ON a.customer_id = c.customer_id
        ORDER BY a.account_id;
    """).show()
    return (amount,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 12 — Summary

    Here's what we covered:

    | Concept | What It Does |
    |:--------|:-------------|
    | `BEGIN TRANSACTION` | Opens a new transaction — changes are now "pending" |
    | `COMMIT` | Makes all pending changes permanent |
    | `ROLLBACK` | Discards all pending changes since `BEGIN` |
    | Autocommit | Default mode — each statement is its own transaction |
    | CHECK constraints | Database-level rules that trigger automatic rollback on violation |
    | try/except pattern | Python best practice for safe transaction handling |

    ### The Golden Rule of Transactions

    > **Every `BEGIN` must be followed by exactly one `COMMIT` or `ROLLBACK`.** No exceptions.

    > NOTE: <br>
    * Transactions are one of the most important concepts in databases. 
    * They're what makes it safe to do things like transfer money, update inventory, or process orders — anywhere you need a guarantee that multiple changes happen together or not at all.
    """)
    return


@app.cell
def _(con):
    # Final state of everything
    print("=== FINAL: All Accounts ===")
    con.sql("""
        SELECT
            a.account_id,
            c.name,
            a.account_type,
            a.balance
        FROM accounts a
        JOIN customers c ON a.customer_id = c.customer_id
        ORDER BY c.name, a.account_type;
    """).show()

    print("=== FINAL: Transaction History ===")
    con.sql("""
        SELECT *
        FROM transactions_log
        ORDER BY txn_id;
    """).show()

    print("=== Total money in the system ===")
    con.sql("""
        SELECT SUM(balance) AS total
        FROM accounts;
    """).show()

    # Clean up
    con.close()
    print("Connection closed. Tutorial complete!")
    return


if __name__ == "__main__":
    app.run()
