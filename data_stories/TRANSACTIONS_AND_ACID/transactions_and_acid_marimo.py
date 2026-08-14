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
    # 🏦 Transactions & ACID
    ### A Hands-On Tutorial with DuckDB — Week 8

    ---

    ## What You Will Learn

    | Topic | Description |
    |---|---|
    | **The problem** | Why two `UPDATE`s that must both happen are dangerous |
    | **`BEGIN` / `COMMIT`** | Grouping statements into one all-or-nothing unit |
    | **`ROLLBACK`** | Undoing everything since `BEGIN` |
    | **A — Atomicity** | All of it happens, or none of it does |
    | **C — Consistency** | The database refuses to end up in an invalid state |
    | **I — Isolation** | Nobody sees your half-finished work |
    | **D — Durability** | Once committed, it survives — uncommitted work does not |

    ---

    ## Why this matters — the bank transfer

    Alice sends Bob \$100. In SQL that is two statements:

    ```sql
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;  -- Alice
    UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;  -- Bob
    ```

    Now ask the uncomfortable question: **what if the power fails between them?**

    ```
    ┌──────────────────────────────────────────────────┐
    │  UPDATE 1 runs   →  Alice loses $100             │
    │  💥 CRASH                                         │
    │  UPDATE 2 never runs  →  Bob never receives it   │
    └──────────────────────────────────────────────────┘
                       $100 has ceased to exist
    ```

    No error was raised. No syntax was wrong. The money is simply gone, and the
    bank's books no longer balance.

    A **transaction** is the tool that makes this impossible.

    ---

    ## A note on how to read this notebook

    Your instructor's teaching notes say:

    > *Common issue: Students memorize ACID but don't understand it.*

    So this notebook does not define the four properties and move on. Each one gets
    a demonstration you can run, where the database visibly refuses to do the wrong
    thing. **Watch what happens, then read the label.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 0 · Setup
    """)
    return


@app.cell
def _():
    import os
    import sys

    import duckdb
    import pandas as pd

    sys.path.insert(0, os.path.dirname(os.path.abspath("__file__")))
    from acid_plot_util import (
        display_table,
        plot_acid_summary,
        plot_isolation,
        plot_transfer_states,
        show_balances,
    )

    # A real file (not :memory:) because Section 8 needs to close the connection,
    # reopen it, and prove that committed data survived. The file is deleted first
    # so the notebook is idempotent.
    DB_PATH = "bank.duckdb"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    con = duckdb.connect(DB_PATH)
    print("✅  DuckDB connected  |  version:", duckdb.__version__)
    print(f"    database file: {DB_PATH}")
    return (
        DB_PATH,
        con,
        display_table,
        duckdb,
        pd,
        plot_acid_summary,
        plot_isolation,
        plot_transfer_states,
        show_balances,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1 · The accounts table

    Straight from the Week 8 lab: create an `accounts` table and insert balances.

    One design choice matters for later — the `CHECK (balance >= 0)` constraint.
    It is a rule the database will enforce on **every** write, forever. We will use
    it in Section 5 to prove the **C** in ACID.
    """)
    return


@app.cell
def _(con, show_balances):
    _sql = """
        CREATE OR REPLACE TABLE accounts (
            account_id INTEGER PRIMARY KEY,
            owner      VARCHAR NOT NULL,
            balance    DECIMAL(10,2) NOT NULL CHECK (balance >= 0)
        );
    """
    print("SQL:\n", _sql)
    con.execute(_sql)

    con.execute("""
        INSERT INTO accounts VALUES
            (1, 'Alice', 500.00),
            (2, 'Bob',   300.00);
    """)

    show_balances(con, "Opening balances")
    print("Total money in the bank: 800.00  ← this number must never change on a transfer")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2 · The unsafe transfer

    First, the dangerous version — two `UPDATE`s with nothing protecting them.

    We deliberately stop between the statements to see the state the crash would
    have frozen. Notice the **total**: it is wrong. \$100 has evaporated.
    """)
    return


@app.cell
def _(con, plot_transfer_states, show_balances):
    _read = lambda: con.execute(
        "SELECT balance FROM accounts ORDER BY account_id"
    ).fetchall()

    _start = _read()
    print("Step 1 — take $100 from Alice")
    con.execute("UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;")
    _midway = _read()
    show_balances(con, "💥 Imagine the power fails RIGHT HERE")
    print(f"Total now: {float(_midway[0][0]) + float(_midway[1][0]):,.2f}  ← $100 has vanished\n")

    print("Step 2 — give $100 to Bob (this is the statement that never ran)")
    con.execute("UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;")
    _end = _read()
    show_balances(con, "Only now is the transfer complete")

    unsafe_states = [
        ("Before",
         _start[0][0], _start[1][0]),
        ("After UPDATE 1\n(crash window)",
         _midway[0][0], _midway[1][0]),
        ("After UPDATE 2",
         _end[0][0], _end[1][0]),
    ]
    plot_transfer_states(unsafe_states)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The middle bar is the problem. For a brief moment the database held a state
    that **must never be allowed to exist** — and if anything had gone wrong in
    that window, it would have been frozen there permanently.

    That window is what a transaction closes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3 · `BEGIN` … `COMMIT` — the safe transfer

    ```sql
    BEGIN TRANSACTION;
        UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
        UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
    COMMIT;
    ```

    Everything between `BEGIN` and `COMMIT` becomes **one indivisible unit**. The
    outside world sees the state before, or the state after — never the middle.

    The crash window still exists inside the transaction, but it no longer matters:
    if the power fails before `COMMIT`, the database throws the whole thing away on
    restart.
    """)
    return


@app.cell
def _(con, show_balances):
    con.execute("BEGIN TRANSACTION;")
    con.execute("UPDATE accounts SET balance = balance - 100 WHERE account_id = 2;")
    con.execute("UPDATE accounts SET balance = balance + 100 WHERE account_id = 1;")
    show_balances(con, "Inside the transaction (Bob returns the $100)")
    con.execute("COMMIT;")
    show_balances(con, "After COMMIT — now it is permanent")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 · `ROLLBACK` — the undo button

    `ROLLBACK` discards everything since `BEGIN`. This is not an error-recovery
    mechanism bolted on afterwards — it is the normal way to abandon work you have
    decided against.
    """)
    return


@app.cell
def _(con, plot_transfer_states, show_balances):
    _read = lambda: con.execute(
        "SELECT balance FROM accounts ORDER BY account_id"
    ).fetchall()

    _before = _read()
    con.execute("BEGIN TRANSACTION;")
    con.execute("UPDATE accounts SET balance = 0 WHERE account_id = 1;")
    con.execute("UPDATE accounts SET balance = 99999 WHERE account_id = 2;")
    _during = _read()
    show_balances(con, "Inside the transaction — chaos")

    con.execute("ROLLBACK;")
    _after = _read()
    show_balances(con, "After ROLLBACK — as if it never happened")

    plot_transfer_states([
        ("Before", _before[0][0], _before[1][0]),
        ("Inside txn\n(uncommitted)", _during[0][0], _during[1][0]),
        ("After ROLLBACK", _after[0][0], _after[1][0]),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ---
    # The four letters, demonstrated

    Now we take ACID one letter at a time. Each section runs code that makes the
    database *prove* the property, rather than asserting it in prose.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 · **A** is for Atomicity — all, or nothing

    Watch this sequence carefully. Inside one transaction we run:

    1. A **valid** update — take \$100 from Alice. It works.
    2. An **invalid** update — take \$99,999 from Bob, which the `CHECK` constraint
       forbids. It fails.

    The question is what happens to the *first* update. If the database were not
    atomic, Alice would be \$100 poorer for no reason.
    """)
    return


@app.cell
def _(con, show_balances):
    show_balances(con, "Before the doomed transaction")

    con.execute("BEGIN TRANSACTION;")
    con.execute("UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;")
    print("✅ Statement 1 succeeded — Alice charged $100 (inside the transaction)")

    try:
        con.execute("UPDATE accounts SET balance = balance - 99999 WHERE account_id = 2;")
        print("Statement 2 succeeded — unexpected!")
    except Exception as e:
        print(f"❌ Statement 2 FAILED: {type(e).__name__}")
        print(f"   {str(e).splitlines()[0][:100]}")

    print("\nWhat can we do now?")
    try:
        con.execute("SELECT * FROM accounts;")
    except Exception as e:
        print(f"   Even a SELECT fails: {str(e).splitlines()[0][:80]}")
        print("   👉 The transaction is in an ABORTED state.")

    con.execute("ROLLBACK;")
    show_balances(con, "After ROLLBACK — Alice's $100 was never taken")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **That is atomicity.** The first update genuinely succeeded, and the database
    still threw it away, because its partner failed.

    Two details worth noticing:

    - Once a statement fails, DuckDB puts the transaction into an **aborted** state.
      Every following statement — even a harmless `SELECT` — is refused until you
      `ROLLBACK`. The database is refusing to let you build on top of a broken
      transaction.
    - If you issue `COMMIT` on an aborted transaction, DuckDB accepts the command
      without error, but **nothing is written**. The net effect is the same as
      `ROLLBACK`. Do not read "COMMIT succeeded" as "my data was saved" — always
      check.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6 · **C** is for Consistency — the rules always hold

    Consistency means the database never *ends* in a state that breaks your rules.
    You declare the rules once, as constraints, and they are enforced on every
    write from then on — including writes made by code you have not written yet.

    Our table declares three:

    | Constraint | Rule |
    |---|---|
    | `PRIMARY KEY (account_id)` | No two accounts share an id |
    | `NOT NULL` on `owner` | Every account has an owner |
    | `CHECK (balance >= 0)` | **No account may go negative** |

    Let us try to break each one.
    """)
    return


@app.cell
def _(con, display_table, pd, show_balances):
    _attempts = [
        ("Overdraw Alice by $10,000",
         "UPDATE accounts SET balance = balance - 10000 WHERE account_id = 1;"),
        ("Insert a duplicate account_id",
         "INSERT INTO accounts VALUES (1, 'Impostor', 50.00);"),
        ("Insert an account with no owner",
         "INSERT INTO accounts VALUES (9, NULL, 50.00);"),
    ]

    _rows = []
    for _label, _sql in _attempts:
        try:
            con.execute(_sql)
            _rows.append((_label, "ALLOWED — constraint missing!"))
        except Exception as e:
            _rows.append((_label, f"REJECTED — {type(e).__name__}"))

    display_table(pd.DataFrame(_rows, columns=["attempt", "result"]),
                  "Three attempts to put the database into an invalid state")
    show_balances(con, "Balances are untouched")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All three were refused. Notice that **we did not write any checking code** —
    no `if balance < 0` anywhere. The rule lives in the table definition, so it
    applies to every program that ever touches this database.

    That is the difference between a rule you *hope* everyone follows and a rule
    the database *enforces*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7 · **I** is for Isolation — nobody sees your half-finished work

    Two connections to the same database. One starts a transfer but does not commit.
    What does the other one see?

    If it saw the uncommitted change, that would be a **dirty read** — and any
    report running at that moment would print a number that never officially
    existed.
    """)
    return


@app.cell
def _(con, plot_isolation, show_balances):
    writer = con.cursor()     # connection 1
    reader = con.cursor()     # connection 2

    _peek = lambda c: c.execute(
        "SELECT balance FROM accounts WHERE account_id = 1"
    ).fetchone()[0]

    writer.execute("BEGIN TRANSACTION;")
    writer.execute("UPDATE accounts SET balance = balance - 250 WHERE account_id = 1;")

    _writer_sees = _peek(writer)
    _reader_sees = _peek(reader)

    print(f"Writer, inside its own transaction : {_writer_sees}")
    print(f"Reader, a different connection     : {_reader_sees}   ← no dirty read")

    writer.execute("COMMIT;")
    _reader_after = _peek(reader)
    print(f"Reader, after the COMMIT           : {_reader_after}   ← now visible")

    plot_isolation(_writer_sees, _reader_sees, _reader_after)

    # put the money back so later sections start from a clean state
    con.execute("UPDATE accounts SET balance = balance + 250 WHERE account_id = 1;")
    show_balances(con, "Restored")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The reader saw the **old** value the entire time the writer was mid-transaction,
    and switched to the new value only after `COMMIT`. It never saw a partial state.

    This is why a bank can run its end-of-day report while transfers are still
    happening: every reader gets a consistent snapshot.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8 · **D** is for Durability — and the lab's question

    > **The Week 8 lab challenge: "What happens if COMMIT is not executed?"**

    Here is the answer, demonstrated rather than described.

    We will do two things and then **close the database entirely**:

    1. A transfer that we **commit**.
    2. A change that we **never commit**.

    Then we reopen the file and see which one survived.
    """)
    return


@app.cell
def _(DB_PATH, con, duckdb, show_balances):
    # 1 — committed change
    con.execute("BEGIN TRANSACTION;")
    con.execute("UPDATE accounts SET balance = balance - 50 WHERE account_id = 1;")
    con.execute("UPDATE accounts SET balance = balance + 50 WHERE account_id = 2;")
    con.execute("COMMIT;")
    print("✅ Transfer of $50 Alice → Bob was COMMITTED")

    # 2 — uncommitted change, on its own connection
    _ghost = con.cursor()
    _ghost.execute("BEGIN TRANSACTION;")
    _ghost.execute("UPDATE accounts SET balance = 999999 WHERE account_id = 2;")
    _inside = _ghost.execute(
        "SELECT balance FROM accounts WHERE account_id = 2"
    ).fetchone()[0]
    print(f"⚠️  Bob's balance inside the uncommitted transaction: {_inside}")
    print("   ...and now we close the database without committing it.\n")

    show_balances(con, "Last look before closing")
    con.close()

    # Reopen from disk — a brand new connection to the same file
    con2 = duckdb.connect(DB_PATH)
    _after = con2.execute(
        "SELECT account_id, owner, balance FROM accounts ORDER BY account_id"
    ).df()
    print("After closing and reopening the database file:")
    print(_after.to_string(index=False))
    print("\n👉 The committed $50 transfer survived.")
    print("👉 The uncommitted 999999 is gone — as if it never happened.")
    con2.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **That is the answer to the lab's challenge.**

    If `COMMIT` is not executed, the work is **discarded**. Not saved partially, not
    left pending, not recovered on the next start — discarded.

    This is deliberate and it is the safe default. A transaction that never
    committed is, by definition, a transaction nobody promised to finish. The
    database's rule is simple:

    > **No `COMMIT`, no promise. No promise, no data.**

    The mirror image is just as important: once `COMMIT` returns, the data is on
    disk and will survive a crash, a power cut, or someone tripping over the cable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 9 · All four, together
    """)
    return


@app.cell
def _(plot_acid_summary):
    acid_results = [
        ("A", "Atomicity — all or nothing", True),
        ("C", "Consistency — rules always hold", True),
        ("I", "Isolation — no dirty reads", True),
        ("D", "Durability — committed survives", True),
    ]
    plot_acid_summary(acid_results)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 10 · Summary

    | Letter | Property | What we ran | What it proved |
    |---|---|---|---|
    | **A** | Atomicity | Valid update + invalid update in one transaction | The valid one was thrown away too |
    | **C** | Consistency | Overdraft, duplicate key, missing owner | All three refused by the table's own rules |
    | **I** | Isolation | Two connections, one mid-transaction | The reader never saw uncommitted data |
    | **D** | Durability | Close and reopen the database file | Committed survived; uncommitted vanished |

    ### The commands

    | Command | Meaning |
    |---|---|
    | `BEGIN TRANSACTION;` | Start grouping statements |
    | `COMMIT;` | Make everything since `BEGIN` permanent |
    | `ROLLBACK;` | Discard everything since `BEGIN` |

    ### The sentence to remember

    > **A transaction turns several statements into one. Either all of them happen,
    > or the database behaves as though you never asked.**

    ---

    ## Exercises

    1. **Break the transfer.** Modify Section 3 so the second `UPDATE` targets a
       non-existent `account_id`. Does the money disappear? Explain the result.
    2. **The aborted state.** After a failed statement, try `COMMIT` instead of
       `ROLLBACK`. Check the balances afterwards. Was anything written? Why is
       "COMMIT succeeded" a misleading message here?
    3. **Consistency by design.** Add a `CHECK` constraint that no account may hold
       more than \$1,000,000. Test it with an `INSERT` and with an `UPDATE`.
    4. **Isolation.** In Section 7, make the *reader* also start a transaction
       before the writer commits. Does the reader see the new value after the
       writer commits, or only after the reader's own transaction ends?
    5. **Challenge.** A shop must reduce `stock` and insert a row into `orders` at
       the same time. Write it as a transaction, then describe in two sentences what
       the customer would experience if the database crashed halfway through.
    """)
    return


if __name__ == "__main__":
    app.run()
