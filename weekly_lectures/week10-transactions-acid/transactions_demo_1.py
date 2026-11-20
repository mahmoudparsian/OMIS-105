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
    # Week 10 — Transactions, Demo 1: `BEGIN`, `COMMIT`, `ROLLBACK` and ACID

    **OMIS 105 — Introduction to Database Management Systems**

    This notebook follows `transactions_are_explained.md`. It uses one small table,
    `accounts`, with two customers: **Alice has $500, Bob has $200** — $700 in total.
    A transfer moves money from one account to another, so the total must **always**
    stay $700.

    Every section starts again from the same two rows (the function `reset()`), so you
    can run the sections in any order. Each section shows a **transcript**: every SQL
    statement, in order, with what DuckDB answered (✅ success, ❌ error).

    ---

    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd

    con = duckdb.connect()  # an in-memory database (Section 9 uses a file)

    def reset():
        """Create the accounts table with its rules, and the two starting rows."""
        con.execute("""
            CREATE OR REPLACE TABLE accounts (
                id      INTEGER PRIMARY KEY,
                owner   VARCHAR NOT NULL,
                balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0)
            )
        """)
        con.execute("INSERT INTO accounts VALUES (1, 'Alice', 500.00), (2, 'Bob', 200.00)")

    def run(connection, statements):
        """Run SQL statements one by one; return a transcript of what happened."""
        rows = []
        for sql in statements:
            try:
                result = connection.execute(sql).fetchall()
                word = sql.split()[0].upper()
                if word in ("UPDATE", "INSERT", "DELETE"):
                    answer = f"{result[0][0]} row(s) changed"
                elif word in ("SELECT", "FROM"):
                    answer = " | ".join(", ".join(str(v) for v in row) for row in result)
                else:
                    answer = "OK"
                rows.append(("✅", sql, answer))
            except Exception as e:
                rows.append(("❌", sql, str(e).splitlines()[0]))
        return pd.DataFrame(rows, columns=["", "statement", "DuckDB says"])

    def balances():
        return con.execute("""
            SELECT id, owner, balance
            FROM accounts
            ORDER BY id
        """).fetchdf()

    return balances, con, duckdb, reset, run


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The data, and the rules on it

    `id` is the **primary key**, `owner` is **`NOT NULL`**, and `balance` has a
    **`CHECK (balance >= 0)`** rule: no account may ever go below $0.
    """)
    return


@app.cell
def _(balances, con, reset):
    reset()
    _total = con.execute("SELECT SUM(balance) FROM accounts").fetchall()[0][0]
    print(f"Total money in the bank: ${_total}")
    balances()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Auto-commit: without `BEGIN`, every statement is saved at once

    Without `BEGIN`, each statement is its **own** transaction and is saved
    immediately. There is nothing left to undo: `ROLLBACK` fails because no
    transaction is open.
    """)
    return


@app.cell
def _(balances, con, mo, reset, run):
    reset()
    _log = run(con, [
        "UPDATE accounts SET balance = balance - 100 WHERE id = 1",
        "ROLLBACK",
    ])
    mo.vstack([_log, mo.md("**After:** Alice has $400 — the update was saved at once."), balances()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. A transfer with `BEGIN` … `COMMIT`

    Move $100 from Alice to Bob. The two `UPDATE`s form **one unit**: `COMMIT`
    saves both together. The total is still $700.
    """)
    return


@app.cell
def _(balances, con, mo, reset, run):
    reset()
    _log = run(con, [
        "BEGIN",
        "UPDATE accounts SET balance = balance - 100 WHERE id = 1",
        "UPDATE accounts SET balance = balance + 100 WHERE id = 2",
        "COMMIT",
        "SELECT SUM(balance) FROM accounts",
    ])
    mo.vstack([_log, mo.md("**After:** Alice $400, Bob $300, total $700."), balances()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Change your mind: `ROLLBACK`

    Inside the transaction you **see** your own change (Alice $400). `ROLLBACK`
    undoes everything since `BEGIN`, and Alice is back to $500.
    """)
    return


@app.cell
def _(balances, con, mo, reset, run):
    reset()
    _log = run(con, [
        "BEGIN",
        "UPDATE accounts SET balance = balance - 100 WHERE id = 1",
        "SELECT balance FROM accounts WHERE id = 1",
        "ROLLBACK",
        "SELECT balance FROM accounts WHERE id = 1",
    ])
    mo.vstack([_log, mo.md("**After:** nothing changed."), balances()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Atomicity: a failed statement stops the whole transaction

    Try to move **$600** from Alice (who has only $500) to Bob. The first `UPDATE`
    (Bob +600) works; the second (Alice −600) breaks the `CHECK` rule.

    After an error, DuckDB marks the transaction as **aborted**: every further
    statement fails until you `ROLLBACK`. Bob's +600 is **not** saved — all or
    nothing.
    """)
    return


@app.cell
def _(balances, con, mo, reset, run):
    reset()
    _log = run(con, [
        "BEGIN",
        "UPDATE accounts SET balance = balance + 600 WHERE id = 2",
        "UPDATE accounts SET balance = balance - 600 WHERE id = 1",
        "SELECT * FROM accounts",
        "ROLLBACK",
    ])
    mo.vstack([_log, mo.md("**After:** Alice $500, Bob $200 — exactly as before."), balances()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. A common mistake: `COMMIT` after an error

    Same failed transfer, but this time the program types `COMMIT` instead of
    `ROLLBACK`. DuckDB answers "OK" — and saves **nothing**: an aborted transaction
    can only be rolled back. Always check for errors; don't assume your work was saved.
    """)
    return


@app.cell
def _(balances, con, mo, reset, run):
    reset()
    _log = run(con, [
        "BEGIN",
        "UPDATE accounts SET balance = balance + 600 WHERE id = 2",
        "UPDATE accounts SET balance = balance - 600 WHERE id = 1",
        "COMMIT",
    ])
    mo.vstack([_log, mo.md("**After:** Bob still has $200 — the `COMMIT` saved nothing."), balances()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Consistency: the database checks every rule you declare

    Each statement below breaks one rule, so the database rejects it. The table
    stays valid: still 2 rows, still $700.
    """)
    return


@app.cell
def _(balances, con, mo, reset, run):
    reset()
    _log = run(con, [
        "INSERT INTO accounts VALUES (3, NULL, 50.00)",                   # NOT NULL
        "INSERT INTO accounts VALUES (1, 'Carol', 50.00)",                # PRIMARY KEY
        "UPDATE accounts SET balance = balance - 1000 WHERE id = 2",      # CHECK
        "SELECT COUNT(*), SUM(balance) FROM accounts",
    ])
    mo.vstack([_log, balances()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. A safe `transfer()` function in Python

    A real application wraps the transaction in Python: `try` → `COMMIT`, and on
    **any** error → `ROLLBACK`. The function returns `True` if the money moved and
    `False` if nothing changed.

    Watch case (c): an `UPDATE` whose `WHERE` matches **no row** is **not** an error —
    it changes 0 rows. Without the check "does the account exist?", Alice would
    lose $100 and nobody would receive it. That is why the function counts the
    accounts first.
    """)
    return


@app.cell
def _(con):
    def transfer(con, from_id, to_id, amount):
        """Move `amount` dollars from account `from_id` to account `to_id`.
        Returns True if the transfer was saved, False if nothing changed."""
        try:
            con.execute("BEGIN")
            found = con.execute(
                "SELECT COUNT(*) FROM accounts WHERE id IN (?, ?)", [from_id, to_id]
            ).fetchall()[0][0]
            if found != 2:
                raise ValueError(f"account {from_id} or {to_id} does not exist")
            # the CHECK (balance >= 0) rule rejects this UPDATE if the money is not there
            con.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", [amount, from_id])
            con.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", [amount, to_id])
            con.execute("COMMIT")
            print(f"✅ moved ${amount} from account {from_id} to account {to_id}")
            return True
        except Exception as e:
            con.execute("ROLLBACK")
            print(f"❌ transfer rolled back: {str(e).splitlines()[0]}")
            return False

    return (transfer,)


@app.cell
def _(balances, reset, transfer, con):
    reset()
    print("(a) a valid transfer:          ", transfer(con, 1, 2, 100))
    print("(b) not enough money:          ", transfer(con, 1, 2, 1000))
    print("(c) account 99 does not exist: ", transfer(con, 1, 99, 100))
    balances()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Only (a) changed the data: Alice $400, Bob $300, total $700.

    ## 9. No `SAVEPOINT` in DuckDB

    PostgreSQL, MySQL, Oracle and SQL Server can undo **part** of a transaction with
    `SAVEPOINT` / `ROLLBACK TO SAVEPOINT`. DuckDB cannot (a parser error). The
    DuckDB way: put the part you want to keep in its **own** transaction and commit
    it, then use a second transaction for the part you may undo.

    Goal: add Dave ($300) and keep him, add Eve ($400) and undo her.
    """)
    return


@app.cell
def _(balances, con, mo, reset, run):
    reset()
    _log = run(con, [
        "BEGIN",
        "INSERT INTO accounts VALUES (3, 'Dave', 300.00)",
        "SAVEPOINT after_dave",
        "ROLLBACK",
        # the DuckDB way: two transactions
        "BEGIN",
        "INSERT INTO accounts VALUES (3, 'Dave', 300.00)",
        "COMMIT",
        "BEGIN",
        "INSERT INTO accounts VALUES (4, 'Eve', 400.00)",
        "ROLLBACK",
    ])
    mo.vstack([_log, mo.md("**After:** Dave is kept, Eve is not."), balances()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Durability: a committed change survives; an uncommitted one does not

    Durability needs a database **file** (an in-memory database disappears when the
    program ends). Below, a file `bank.duckdb` is created in a temporary folder:

    1. Alice's −100 is **committed**, then the connection is closed (like a program
       that ends or crashes).
    2. Bob's +100 is made **inside a transaction that never commits**, then the
       connection is closed.
    3. Opening the file again shows Alice's change kept and Bob's change gone.
    """)
    return


@app.cell
def _(duckdb):
    import os
    import tempfile

    _folder = tempfile.mkdtemp()
    _path = os.path.join(_folder, "bank.duckdb")

    _db = duckdb.connect(_path)
    _db.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner VARCHAR, balance DECIMAL(10, 2))")
    _db.execute("INSERT INTO accounts VALUES (1, 'Alice', 500.00), (2, 'Bob', 200.00)")
    _db.execute("BEGIN")
    _db.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    _db.execute("COMMIT")                                                   # 1. saved
    _db.close()

    _db = duckdb.connect(_path)
    _db.execute("BEGIN")
    _db.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")  # 2. never committed
    _db.close()

    _db = duckdb.connect(_path)                                             # 3. open again
    _after = _db.execute("SELECT id, owner, balance FROM accounts ORDER BY id").fetchdf()
    _db.close()
    _after
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Alice has $400 (committed — kept). Bob has $200 (never committed — gone).

    ## Summary

    | Section | What you saw |
    |---|---|
    | 2 | Without `BEGIN`, each statement is saved at once (auto-commit) |
    | 3–4 | `BEGIN` … `COMMIT` saves the changes together; `ROLLBACK` undoes them |
    | 5–6 | **Atomicity**: after an error the transaction is aborted — nothing is saved, even with `COMMIT` |
    | 7 | **Consistency**: `PRIMARY KEY`, `NOT NULL` and `CHECK` reject bad data |
    | 8 | In Python: `try` → `COMMIT`, `except` → `ROLLBACK`; an `UPDATE` that matches no row is not an error |
    | 9 | DuckDB has no `SAVEPOINT`: use separate transactions |
    | 10 | **Durability**: after `COMMIT` (to a file), the change survives; without it, it is lost |

    **Next:** `transactions_demo_2.py` — transactions on the ShopSmart store
    (orders, stock, returns) and **Isolation** with two users at the same time.
    """)
    return


if __name__ == "__main__":
    app.run()
