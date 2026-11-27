---
title: OMIS 105 - Week 10 (Transactions & ACID)
author: Dr. Mahmoud Parsian
marp: true
theme: default
paginate: true
class: lead
style: |
  section {
    justify-content: flex-start;
    padding-top: 50px;
    padding-bottom: 50px;
  }
  table {
    font-size: 0.7em;
  }
  pre {
    white-space: pre-wrap;
  }
  blockquote {
    border-left: 6px solid #2a7ae2;
    background: #eef5ff;
    padding: 0.3em 0.8em;
    color: #222;
  }
---

# OMIS 105: Week 10
## Transactions & ACID <br> Keeping Data Correct and Reliable — in DuckDB

---

# Agenda

**Part 1 — Transactions and ACID** (a tiny bank, and a library)

- What a transaction is, and why we need one
- `BEGIN`, `COMMIT`, `ROLLBACK` — and auto-commit
- What happens when a statement fails
- ACID: **A**tomicity, **C**onsistency, **I**solation, **D**urability
- Rules DuckDB enforces: `PRIMARY KEY`, `NOT NULL`, `CHECK`, `REFERENCES`

**Part 2 — Transactions in a Store, and Many Users** (ShopSmart)

- Orders and returns as transactions
- Four concurrency problems — and how DuckDB handles two users at once

---

# The Notebooks for This Week

Run them from inside `weekly_lectures/week10-transactions-acid/`:

| Notebook | What it shows |
|---|---|
| `transactions_demo_1.py` | Part 1 on the `accounts` table: auto-commit, `COMMIT`, `ROLLBACK`, a failed statement, `transfer()`, no `SAVEPOINT`, durability with a file |
| `transactions_demo_2.py` | Part 2 on ShopSmart: one order = one transaction, `place_order()`, `process_return()`, and four two-user experiments |

> ✅ Every output on these slides was produced by **DuckDB 2.0** — nothing was typed by hand.

---

# How to Read the DuckDB Sessions

Most examples are **DuckDB sessions**. Open a terminal and start DuckDB:

```text
$ duckdb               -- in memory (gone when you quit)
$ duckdb bank.duckdb   -- a database file (kept on disk)
```

- `D ` is DuckDB's prompt: the rest of the line is **what you type**
- the lines below it are **DuckDB's answer**: a result table, or an error
- a statement that changes data (`UPDATE`, `BEGIN`, …) answers **nothing** when it works
- `A> ` and `B> ` (Part 2): **two users** on the **same** database at the same time
- long lines are wrapped to fit the slide (the extra lines are indented)

---

# Recap

- **Week 9:** ranking functions — `ROW_NUMBER`, `RANK`, `DENSE_RANK`
- **Weeks 3–9:** **reading** data with `SELECT`
- **Week 3:** **changing** data with `INSERT`, `UPDATE`, `DELETE` — one statement at a time

👉 **Today:** changing data **safely** — several statements as **one unit**, so the
data stays **correct and reliable**, even when things go wrong

---

# Part 1 — Transactions and ACID

---

# What Is a Transaction?

A **transaction** is a group of SQL statements that the database treats as
**one unit**.

Either:

- **all** of them take effect ✅
- or **none** of them do ❌

There is no "half done".

> 💡 **Key idea:** a transaction is **all or nothing**.

---

# Transactions Are Everywhere

Many everyday actions are **several** changes that must happen **together**:

| Action | The changes | If only half happens … |
|---|---|---|
| ATM withdrawal | lower the balance · record the withdrawal | money is gone, or cash comes out for free |
| Online checkout | create the order · add its items · lower the stock | an order with no items, or stock that is wrong |
| Airline seat | mark the seat taken · create the ticket | two people get the same seat |
| Library loan | create the loan · lower the copies available | a loan for a book the library does not have |

A **transaction** makes the database do **all** of the changes, or **none**.

---

# The Classic Example: A Bank Transfer

* Alice has `$500`
* Bob has `$200`

**Move `$100` from Alice to Bob:**

```
Step 1: Subtract $100 from Alice   ($500 → $400)
Step 2: Add $100 to Bob            ($200 → $300)
```

What if the system crashes **after Step 1 but before Step 2**?

- Alice lost `$100` ❌
- Bob never received it ❌
- `$100` has disappeared — the data is now **wrong**

👉 Both steps must happen — or neither.

---

# Our Table: `accounts`, with Rules

```sql
CREATE OR REPLACE TABLE accounts (
    id      INTEGER PRIMARY KEY,                           -- unique, never NULL
    owner   VARCHAR NOT NULL,                              -- must have a value
    balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0)   -- never negative
);

INSERT INTO accounts VALUES
(1, 'Alice', 500.00),
(2, 'Bob',   200.00);
```

- `NOT NULL`: the column must always have a value
- `CHECK (condition)`: every row must make the condition true
- `DECIMAL(10, 2)`: exact money values, with 2 digits after the point

---

# The `accounts` Table in DuckDB

Every example in Part 1 starts here. Alice + Bob = **`$700`** — a transfer must **never** change the total.

<!-- duckdb-session: bank -->
```text
D SELECT * FROM accounts;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     1 │ Alice   │        500.00 │
│     2 │ Bob     │        200.00 │
└───────┴─────────┴───────────────┘
D SELECT SUM(balance) AS total_money FROM accounts;
┌───────────────┐
│  total_money  │
│ decimal(38,2) │
├───────────────┤
│        700.00 │
└───────────────┘
```

---

# The Three Commands

```sql
BEGIN;      -- start a transaction
COMMIT;     -- save all changes since BEGIN
ROLLBACK;   -- undo all changes since BEGIN
```

| Command | After it … |
|---|---|
| `BEGIN` | your changes are **temporary**: only you can see them |
| `COMMIT` | your changes are **permanent**, and everyone can see them |
| `ROLLBACK` | your changes are **gone**, as if you had never made them |

---

# Auto-Commit: No `BEGIN`, No Undo

Without `BEGIN`, each statement is its **own** transaction, saved **at once** (**auto-commit**):

<!-- duckdb-session: bank -->
```text
D UPDATE accounts SET balance = balance - 100 WHERE id = 1;
D ROLLBACK;
TransactionContext Error: cannot rollback - no transaction is active
D SELECT * FROM accounts;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     1 │ Alice   │        400.00 │
│     2 │ Bob     │        200.00 │
└───────┴─────────┴───────────────┘
```

* The `UPDATE` was saved the moment it ran (Alice `$400`); `ROLLBACK` has nothing to undo.
* 👉 To be able to undo, start with `BEGIN`.

---

# One Statement Is Already All or Nothing

Even **without** `BEGIN`, a **single** statement never stops halfway.
Take `$300` from **everyone**: Alice could pay (`500 → 200`), Bob could not (`200 → −100`):

<!-- duckdb-session: bank -->
```text
D UPDATE accounts SET balance = balance - 300;
Constraint Error: CHECK constraint failed on table "accounts"
  with expression CHECK((balance >= 0))
D SELECT * FROM accounts;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     1 │ Alice   │        500.00 │
│     2 │ Bob     │        200.00 │
└───────┴─────────┴───────────────┘
```

Alice's row was **not** changed either: one bad row stops the **whole** statement.

👉 A transaction extends this to **several** statements.

---

# The Same for a Multi-Row `INSERT`

Two new accounts in **one** `INSERT`; Dave's balance breaks the `CHECK`:

<!-- duckdb-session: bank -->
```text
D INSERT INTO accounts VALUES (3, 'Carol', 50.00), (4, 'Dave', -5.00);
Constraint Error: CHECK constraint failed on table "accounts"
  with expression CHECK((balance >= 0))
D SELECT * FROM accounts;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     1 │ Alice   │        500.00 │
│     2 │ Bob     │        200.00 │
└───────┴─────────┴───────────────┘
```

Carol's row is **not** saved either — the `INSERT` is all or nothing.

---

# A Transfer as a Transaction

<!-- duckdb-session: bank -->
```text
D BEGIN;
D UPDATE accounts SET balance = balance - 100 WHERE id = 1;
D UPDATE accounts SET balance = balance + 100 WHERE id = 2;
D SELECT * FROM accounts;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     1 │ Alice   │        400.00 │
│     2 │ Bob     │        300.00 │
└───────┴─────────┴───────────────┘
```

Inside the transaction, both changes are done — but **not saved yet**.

---

# A Transfer as a Transaction (cont.)

<!-- duckdb-session: continue -->
```text
D COMMIT;
D SELECT SUM(balance) AS total_money FROM accounts;
┌───────────────┐
│  total_money  │
│ decimal(38,2) │
├───────────────┤
│        700.00 │
└───────────────┘
```

`COMMIT` saves both changes **together**: Alice `$400`, Bob `$300`. Total money: still **`$700`** ✅

---

# Change Your Mind: `ROLLBACK`

<!-- duckdb-session: bank -->
```text
D BEGIN;
D UPDATE accounts SET balance = balance - 100 WHERE id = 1;
D SELECT * FROM accounts WHERE id = 1;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     1 │ Alice   │        400.00 │
└───────┴─────────┴───────────────┘
D ROLLBACK;
D SELECT * FROM accounts WHERE id = 1;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     1 │ Alice   │        500.00 │
└───────┴─────────┴───────────────┘
```

You **see your own change** (`$400`) — and `ROLLBACK` undoes it.

---

# Mistakes with the Commands

DuckDB answers with an **error** when a command does not fit the moment:

<!-- duckdb-session: bank -->
```text
D BEGIN;
D BEGIN;
TransactionContext Error: cannot start a transaction within a transaction
D ROLLBACK;
D COMMIT;
TransactionContext Error: cannot commit - no transaction is active
D ROLLBACK;
TransactionContext Error: cannot rollback - no transaction is active
```

* There is **no** transaction inside a transaction: the 2nd `BEGIN` fails (the 1st one is still active).
* `COMMIT` and `ROLLBACK` need an **active** transaction.

---

# Other Spellings DuckDB Accepts

All of these work in DuckDB — pick one style and stay with it:

| Meaning | You can write |
|---|---|
| start a transaction | `BEGIN;` · `BEGIN TRANSACTION;` · `START TRANSACTION;` |
| save the work | `COMMIT;` · `COMMIT TRANSACTION;` · `END;` |
| undo the work | `ROLLBACK;` · `ROLLBACK TRANSACTION;` · `ABORT;` |
| read, but never write | `BEGIN TRANSACTION READ ONLY;` |

A write inside a `READ ONLY` transaction is refused:

<!-- duckdb-session: bank -->
```text
D BEGIN TRANSACTION READ ONLY;
D UPDATE accounts SET balance = 0 WHERE id = 1;
TransactionContext Error: Cannot write to database ""memory"" - transaction is
  launched in read-only mode
D ROLLBACK;
```

---

# What If a Statement Fails?

Alice has **`$500`**. Try to move **`$600`** to Bob — Bob first, then Alice:

<!-- duckdb-session: bank -->
```text
D BEGIN;
D UPDATE accounts SET balance = balance + 600 WHERE id = 2;
D UPDATE accounts SET balance = balance - 600 WHERE id = 1;
Constraint Error: CHECK constraint failed on table "accounts"
  with expression CHECK((balance >= 0))
D SELECT * FROM accounts;
TransactionContext Error: Current transaction is aborted (please ROLLBACK)
```

After an error, DuckDB marks the transaction as **aborted**: it refuses every
statement until you type `ROLLBACK`.

---

# What If a Statement Fails? (cont.)

<!-- duckdb-session: continue -->
```text
D ROLLBACK;
D SELECT * FROM accounts;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     1 │ Alice   │        500.00 │
│     2 │ Bob     │        200.00 │
└───────┴─────────┴───────────────┘
```

Bob's `+600` was **not** saved: Alice `$500`, Bob `$200`. The failed transfer changed **nothing**.

---

# A Common Mistake: `COMMIT` After an Error

Same failed transfer, but the program types `COMMIT` instead of `ROLLBACK`:

<!-- duckdb-session: bank -->
```text
D BEGIN;
D UPDATE accounts SET balance = balance + 600 WHERE id = 2;
D UPDATE accounts SET balance = balance - 600 WHERE id = 1;
Constraint Error: CHECK constraint failed on table "accounts"
  with expression CHECK((balance >= 0))
D COMMIT;
D SELECT * FROM accounts;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     1 │ Alice   │        500.00 │
│     2 │ Bob     │        200.00 │
└───────┴─────────┴───────────────┘
```

`COMMIT` answers **nothing**, yet Bob still has `$200`: it saved **nothing**. 👉 Write `ROLLBACK`.

---

# A Quiet Danger: An `UPDATE` That Matches No Row

Add `RETURNING *` to see which rows a statement changed:

<!-- duckdb-session: bank -->
```text
D UPDATE accounts SET balance = balance + 100 WHERE id = 99 RETURNING *;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
└───────┴─────────┴───────────────┘
              0 rows
D UPDATE accounts SET balance = balance + 100 WHERE id = 2 RETURNING *;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     2 │ Bob     │        300.00 │
└───────┴─────────┴───────────────┘
```

No account 99: **0 rows, no error**. So a safe transfer **checks** that both accounts exist.

---

# One More Example: Borrowing a Library Book

A loan = **two** changes together: add a row to `loans`, and lower `copies_available` by 1.

```sql
CREATE OR REPLACE TABLE books (
    book_id          INTEGER PRIMARY KEY,
    title            VARCHAR NOT NULL,
    copies_available INTEGER NOT NULL CHECK (copies_available >= 0)
);
CREATE OR REPLACE TABLE loans (
    loan_id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(book_id),
    student VARCHAR NOT NULL
);
INSERT INTO books VALUES
(1, 'Learning SQL',     1),     -- only ONE copy left
(2, 'DuckDB in Action', 3);
```

---

# Maria Borrows the Last Copy ✅

<!-- duckdb-session: library -->
```text
D BEGIN;
D INSERT INTO loans VALUES (1, 1, 'Maria');
D UPDATE books SET copies_available = copies_available - 1 WHERE book_id = 1;
D COMMIT;
D SELECT l.student, b.title, b.copies_available
    FROM loans l JOIN books b USING (book_id);
┌─────────┬──────────────┬──────────────────┐
│ student │    title     │ copies_available │
│ varchar │   varchar    │      int32       │
├─────────┼──────────────┼──────────────────┤
│ Maria   │ Learning SQL │                0 │
└─────────┴──────────────┴──────────────────┘
```

The loan and the lower count are saved **together**: book 1 now has **0** copies.

---

# Kevin Tries to Borrow It Too ❌

<!-- duckdb-session: library_after_maria -->
```text
D BEGIN;
D INSERT INTO loans VALUES (2, 1, 'Kevin');
D UPDATE books SET copies_available = copies_available - 1 WHERE book_id = 1;
Constraint Error: CHECK constraint failed on table "books"
  with expression CHECK((copies_available >= 0))
D ROLLBACK;
D SELECT * FROM loans;
┌─────────┬─────────┬─────────┐
│ loan_id │ book_id │ student │
│  int32  │  int32  │ varchar │
├─────────┼─────────┼─────────┤
│       1 │       1 │ Maria   │
└─────────┴─────────┴─────────┘
```

Kevin's `INSERT` worked, then the `UPDATE` broke the `CHECK` (`0 → −1`). `ROLLBACK` undid **both**:
`loans` has **only Maria's** row. Without a transaction, Kevin would have a loan for a book the library does not have.

---

# `REFERENCES`: Loans Must Point to Real Books

`loans.book_id REFERENCES books(book_id)` — a **foreign key**. DuckDB checks it in
**both** directions:

<!-- duckdb-session: library_after_maria -->
```text
D INSERT INTO loans VALUES (2, 9, 'Kevin');
Constraint Error: Violates foreign key constraint because key "book_id: 9" does
  not exist in the referenced table
D DELETE FROM books WHERE book_id = 1;
Constraint Error: Violates foreign key constraint because key "book_id: 1" is
  still referenced by a foreign key in a different table. If this is an unexpected
  constraint violation, please refer to our foreign key limitations in the
  documentation
```

* No loan for a book that does not exist (book 9).
* No deleting a book that is still on loan (Maria has book 1).

---

# Even `CREATE TABLE` Can Be Rolled Back

In DuckDB, changes to **tables themselves** (`CREATE`, `DROP`, `ALTER`) are part of
the transaction, too:

<!-- duckdb-session: bank -->
```text
D BEGIN;
D CREATE TABLE audit_log (msg VARCHAR);
D SHOW TABLES;
┌───────────┐
│   name    │
│  varchar  │
├───────────┤
│ accounts  │
│ audit_log │
└───────────┘
```

Inside the transaction, the new table `audit_log` exists.

---

# Even `CREATE TABLE` Can Be Rolled Back (cont.)

<!-- duckdb-session: continue -->
```text
D ROLLBACK;
D SHOW TABLES;
┌──────────┐
│   name   │
│ varchar  │
├──────────┤
│ accounts │
└──────────┘
```

`ROLLBACK` removed the new table `audit_log`: as if it had never been created.

---

# The Life of a Transaction

```
 auto-commit ──BEGIN──▶ ACTIVE ──COMMIT──▶ saved ✅ (back to auto-commit)
 (each statement           │
  saved at once)           ├──ROLLBACK──▶ undone ↩️ (back to auto-commit)
                           │
                           └──a statement fails──▶ ABORTED
                                                     │  every next statement:
                                                     │  "Current transaction is aborted (please ROLLBACK)"
                                                     └──ROLLBACK (or COMMIT)──▶ undone ↩️
```

| You type | In auto-commit | In an active transaction | In an aborted transaction |
|---|---|---|---|
| `BEGIN` | starts a transaction | ❌ cannot start a transaction within a transaction | ❌ refused |
| `UPDATE …` | saved at once | visible to you only, until `COMMIT` | ❌ refused |
| `COMMIT` | ❌ no transaction is active | saves everything | saves **nothing** |
| `ROLLBACK` | ❌ no transaction is active | undoes everything | undoes everything |

---

# ACID: Four Guarantees

| Property | Meaning | In the bank | In the library |
|---|---|---|---|
| **A**tomicity | All or nothing | Never subtract from Alice without adding to Bob | No loan without lowering the count |
| **C**onsistency | Every rule holds before and after | `CHECK (balance >= 0)` | `CHECK (copies_available >= 0)` |
| **I**solation | Transactions at the same time don't interfere | Two withdrawals at once: none is "lost" | Two students, one copy: only one gets it |
| **D**urability | After `COMMIT`, the change survives a crash | The transfer is still there after a power failure | Maria's loan is still there tomorrow |

---

# Atomicity (All or Nothing)

- A transaction cannot be divided
- If **any** statement fails, **all** its changes are undone
- No "half-done" transactions

**Examples you have seen:**
- one `UPDATE` on two rows: Bob's row failed, so Alice's row was not changed
- the `$600` transfer: Bob's `+600` was undone because Alice's `−600` failed
- Kevin's loan row was undone because the copy count could not go below 0
- `CREATE TABLE audit_log` was undone by `ROLLBACK`

---

# Consistency (Valid Data)

- Every rule you **declare** holds before and after each transaction
- Rules: `PRIMARY KEY`, `NOT NULL`, `CHECK`, `UNIQUE`, `REFERENCES` (foreign key)
- A statement that would break a rule is **rejected**

<!-- duckdb-session: bank -->
```text
D INSERT INTO accounts VALUES (3, NULL, 50.00);
Constraint Error: NOT NULL constraint failed: accounts."owner"
D INSERT INTO accounts VALUES (1, 'Carol', 50.00);
Constraint Error: Duplicate key "id: 1" violates primary key constraint.
D UPDATE accounts SET balance = -1 WHERE id = 2;
Constraint Error: CHECK constraint failed on table "accounts"
  with expression CHECK((balance >= 0))
```

* DuckDB checks only the rules you **declare**.
* A rule that lives only in your head (or in your app) is **not** checked.

---

# DuckDB: See the Rules of a Table

DuckDB lists every declared rule in the table function `duckdb_constraints()`:

<!-- duckdb-session: bank -->
```text
D SELECT constraint_type, expression, constraint_column_names
    FROM duckdb_constraints() WHERE table_name = 'accounts'
    ORDER BY constraint_index;
┌─────────────────┬────────────────┬─────────────────────────┐
│ constraint_type │   expression   │ constraint_column_names │
│     varchar     │    varchar     │        varchar[]        │
├─────────────────┼────────────────┼─────────────────────────┤
│ PRIMARY KEY     │ NULL           │ [id]                    │
│ NOT NULL        │ NULL           │ [owner]                 │
│ CHECK           │ (balance >= 0) │ [balance]               │
│ NOT NULL        │ NULL           │ [balance]               │
│ NOT NULL        │ NULL           │ [id]                    │
└─────────────────┴────────────────┴─────────────────────────┘
```

👉 A `PRIMARY KEY` column is also `NOT NULL` — DuckDB adds that rule for you.

---

# Isolation (No Interference)

Many users work at the same time:

👉 Each transaction behaves **as if it were alone**.

- Your **uncommitted** changes are visible to **you only**
- Others see them only **after** your `COMMIT`

**Example:** two people withdraw from the same account at the same moment — the
database must not "lose" one of the withdrawals.

Part 2 shows four concurrency problems, and what DuckDB does about each — with
**two users** on one database.

---

# Durability (Permanent)

After `COMMIT`, the change is saved **permanently** — even if the program crashes
or the power fails.

**How DuckDB does it: the write-ahead log (WAL)**

```
1. Write the changes to a log file on disk:
   bank.duckdb.wal
2. Only then report "COMMIT succeeded"
3. Later, at a CHECKPOINT, copy the changes
   into bank.duckdb and empty the log
-- After a crash, DuckDB replays the log on restart:
-- committed changes are kept, uncommitted ones are dropped
```

DuckDB checkpoints **automatically** (when the log reaches `16.0 MiB`, and when
the database is closed). You can also type `CHECKPOINT;` yourself.

---

# Durability Needs a File

```text
$ duckdb               -- in memory: lost when you quit
$ duckdb bank.duckdb   -- a file: committed changes are kept
```

In Python:

```python
con = duckdb.connect('bank.duckdb')   # a database file → durable
con = duckdb.connect()                # in memory → lost when the program ends
```

> 💡 An in-memory DuckDB still gives you **A**, **C** and **I** — but not **D**.

---

# Durability in DuckDB: Committed vs. Not

<!-- duckdb-session: none -->
```text
$ duckdb bank.duckdb
D CREATE TABLE accounts (id INTEGER, owner VARCHAR, balance DECIMAL(10, 2));
D INSERT INTO accounts VALUES (1, 'Alice', 500.00), (2, 'Bob', 200.00);
D BEGIN;
D UPDATE accounts SET balance = balance - 100 WHERE id = 1;
D COMMIT;
D BEGIN;
D UPDATE accounts SET balance = balance + 100 WHERE id = 2;
D .quit
```

Alice's `−100` was **committed**. Bob's `+100` was **not** — the program ended first.

---

# Durability in DuckDB: Committed vs. Not (cont.)

Start DuckDB again on the same file:

<!-- duckdb-session: continue -->
```text
$ duckdb bank.duckdb
D SELECT * FROM accounts;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     1 │ Alice   │        400.00 │
│     2 │ Bob     │        200.00 │
└───────┴─────────┴───────────────┘
```

* Alice's `−100` was **committed** → kept ✅
* Bob's `+100` was **never committed** → gone ❌ (`.quit` with an open transaction = `ROLLBACK`)

`transactions_demo_1.py`, Section 10, runs the same test.

---

# The Write-Ahead Log, Seen in DuckDB

`glob()` lists files on disk. Watch the `.wal` file appear — and disappear:

<!-- duckdb-session: none -->
```text
$ duckdb bank.duckdb
D CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance DECIMAL(10, 2));
D INSERT INTO accounts VALUES (1, 500.00);
D SELECT file FROM glob('bank.duckdb*');
┌─────────────────┐
│      file       │
│     varchar     │
├─────────────────┤
│ bank.duckdb     │
│ bank.duckdb.wal │
└─────────────────┘
```

The committed `INSERT` sits in the log, `bank.duckdb.wal`, for now.

---

# The Write-Ahead Log, Seen in DuckDB (cont.)

<!-- duckdb-session: continue -->
```text
D CHECKPOINT;
┌─────────┐
│ Success │
│ boolean │
└─────────┘
  0 rows
D SELECT file FROM glob('bank.duckdb*');
┌─────────────┐
│    file     │
│   varchar   │
├─────────────┤
│ bank.duckdb │
└─────────────┘
```

The **checkpoint** copied the changes into `bank.duckdb` and removed the log.
DuckDB also checkpoints by itself when the log reaches `16.0 MiB`.

---

# A Safe Transfer in Python

```python
def transfer(con, from_id, to_id, amount):
    try:
        con.execute("BEGIN")
        found = con.execute("SELECT COUNT(*) FROM accounts WHERE id IN (?, ?)",
                            [from_id, to_id]).fetchall()[0][0]
        if found != 2:
            raise ValueError("an account does not exist")
        con.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", [amount, from_id])
        con.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", [amount, to_id])
        con.execute("COMMIT")
        return True                     # the money moved
    except Exception:
        con.execute("ROLLBACK")
        return False                    # nothing changed
```

- `?` = a **parameter**: Python fills in the value safely
- `try` / `except`: on **any** error, `ROLLBACK` — the data is never left half-done

---

# A Safe Transfer in Python: Tests

Starting from Alice `$500`, Bob `$200`:

```python
print(transfer(con, 1, 2, 100))    # Alice → Bob, $100
print(transfer(con, 1, 2, 1000))   # Alice has only $400 now: CHECK fails
print(transfer(con, 1, 99, 100))   # account 99 does not exist
print(con.execute("SELECT id, owner, balance FROM accounts ORDER BY id").fetchall())
```

Output:

```text
True
False
False
[(1, 'Alice', Decimal('400.00')), (2, 'Bob', Decimal('300.00'))]
```

Only the first transfer moved money. The other two changed **nothing**.

---

# Undo Part of a Transaction? Not in DuckDB

Some databases can undo **part** of a transaction with a `SAVEPOINT`.
**DuckDB has no `SAVEPOINT`:**

<!-- duckdb-session: bank -->
```text
D BEGIN;
D INSERT INTO accounts VALUES (3, 'Dave', 300.00);
D SAVEPOINT after_dave;
Parser Error: syntax error at or near "after_dave"

LINE 1: SAVEPOINT after_dave;
                  ^^^^^^^^^^
D ROLLBACK;
```

In DuckDB, a transaction is undone **as a whole** — or not at all.

---

# The DuckDB Way: Two Transactions

Put the part you want to keep in its **own** transaction — Dave is kept, Eve is not:

<!-- duckdb-session: bank -->
```text
D BEGIN;
D INSERT INTO accounts VALUES (3, 'Dave', 300.00);
D COMMIT;
D BEGIN;
D INSERT INTO accounts VALUES (4, 'Eve', 400.00);
D ROLLBACK;
D SELECT * FROM accounts;
┌───────┬─────────┬───────────────┐
│  id   │  owner  │    balance    │
│ int32 │ varchar │ decimal(10,2) │
├───────┼─────────┼───────────────┤
│     1 │ Alice   │        500.00 │
│     2 │ Bob     │        200.00 │
│     3 │ Dave    │        300.00 │
└───────┴─────────┴───────────────┘
```

---

# Part 2 — Transactions in a Store, and Many Users

---

# Setup: ShopSmart with Rules

`read_csv` alone creates tables **without** rules. Here we create the tables with
keys and `CHECK` rules first, then load the CSV data (run from the
`week10-transactions-acid` folder):

```sql
CREATE OR REPLACE TABLE products (
    product_id     INTEGER PRIMARY KEY,
    product_name   VARCHAR NOT NULL,
    category_id    INTEGER,
    price          DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0)
);
INSERT INTO products SELECT * FROM read_csv('data/products.csv');
```

---

# Setup: ShopSmart with Rules (cont.)

```sql
CREATE OR REPLACE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL,
    order_date   DATE NOT NULL,
    status       VARCHAR NOT NULL,
    total_amount DECIMAL(10, 2) CHECK (total_amount >= 0)
);
INSERT INTO orders SELECT * FROM read_csv('data/orders.csv');
```

---

# Setup: ShopSmart with Rules (cont.)

```sql
CREATE OR REPLACE TABLE order_items (
    item_id    INTEGER PRIMARY KEY,
    order_id   INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL
);
INSERT INTO order_items SELECT * FROM read_csv('data/order_items.csv');
```

To run the setup again, drop `order_items` first. DuckDB will not replace a table
that another table references:

```
Catalog Error: Could not drop the table because this table is
main key table of the table "order_items"
```

---

# ShopSmart: What Is in the Tables

<!-- duckdb-session: shop -->
```text
D SELECT (SELECT COUNT(*) FROM products) AS products, (SELECT COUNT(*)
    FROM orders) AS orders, (SELECT COUNT(*) FROM order_items) AS order_items;
┌──────────┬────────┬─────────────┐
│ products │ orders │ order_items │
│  int64   │ int64  │    int64    │
├──────────┼────────┼─────────────┤
│       64 │    200 │         607 │
└──────────┴────────┴─────────────┘
D SELECT status, COUNT(*) AS orders FROM orders GROUP BY status ORDER BY status;
┌────────────┬────────┐
│   status   │ orders │
│  varchar   │ int64  │
├────────────┼────────┤
│ cancelled  │     29 │
│ completed  │    115 │
│ processing │     30 │
│ shipped    │     26 │
└────────────┴────────┘
```

---

# ShopSmart: What Is in the Tables (cont.)

<!-- duckdb-session: continue -->
```text
D SELECT product_id, product_name, price, stock_quantity FROM products
    WHERE product_id <= 2;
┌────────────┬────────────────┬───────────────┬────────────────┐
│ product_id │  product_name  │     price     │ stock_quantity │
│   int32    │    varchar     │ decimal(10,2) │     int32      │
├────────────┼────────────────┼───────────────┼────────────────┤
│          1 │ Smartphone X12 │        321.52 │             12 │
│          2 │ Laptop Pro 15  │        372.07 │            125 │
└────────────┴────────────────┴───────────────┴────────────────┘
```

We will use **product 1** (Smartphone X12: `$321.52`, **12** in stock) and the **30** `processing` orders.

---

# One Order = One Transaction

Customer 5 buys 2 × product 1 (`2 × $321.52 = $643.04`):

<!-- duckdb-session: shop -->
```text
D BEGIN;
D INSERT INTO orders VALUES (201, 5, DATE '2025-01-15', 'processing', 643.04);
D INSERT INTO order_items VALUES (608, 201, 1, 2, 321.52);
D UPDATE products SET stock_quantity = stock_quantity - 2 WHERE product_id = 1;
D COMMIT;
```

An order without its item, or an item without the stock going down, would leave
the data wrong — so the three statements belong **together**.

---

# One Order = One Transaction (cont.)

<!-- duckdb-session: continue -->
```text
D SELECT order_id, customer_id, status, total_amount FROM orders
    WHERE order_id = 201;
┌──────────┬─────────────┬────────────┬───────────────┐
│ order_id │ customer_id │   status   │ total_amount  │
│  int32   │    int32    │  varchar   │ decimal(10,2) │
├──────────┼─────────────┼────────────┼───────────────┤
│      201 │           5 │ processing │        643.04 │
└──────────┴─────────────┴────────────┴───────────────┘
D SELECT product_id, stock_quantity FROM products WHERE product_id = 1;
┌────────────┬────────────────┐
│ product_id │ stock_quantity │
│   int32    │     int32      │
├────────────┼────────────────┤
│          1 │             10 │
└────────────┴────────────────┘
```

Order 201 is saved, and the stock went from **12** to **10**.

---

# Atomicity: a Wrong Product

<!-- duckdb-session: shop -->
```text
D BEGIN;
D INSERT INTO orders VALUES (201, 5, DATE '2025-01-15', 'processing', 150.00);
D INSERT INTO order_items VALUES (608, 201, 99, 2, 75.00);
Constraint Error: Violates foreign key constraint because key "product_id: 99"
  does not exist in the referenced table
D ROLLBACK;
D SELECT COUNT(*) AS order_201 FROM orders WHERE order_id = 201;
┌───────────┐
│ order_201 │
│   int64   │
├───────────┤
│         0 │
└───────────┘
```

There is no product 99, so the item is refused — and `ROLLBACK` removes order 201, too.

---

# Consistency: Not Enough Stock

Customer 5 wants **20** smartphones; only **12** are in stock:

<!-- duckdb-session: shop -->
```text
D BEGIN;
D INSERT INTO orders VALUES (201, 5, DATE '2025-01-15', 'processing', 6430.40);
D INSERT INTO order_items VALUES (608, 201, 1, 20, 321.52);
D UPDATE products SET stock_quantity = stock_quantity - 20 WHERE product_id = 1;
Constraint Error: CHECK constraint failed on table "products"
  with expression CHECK((stock_quantity >= 0))
D ROLLBACK;
D SELECT product_id, stock_quantity FROM products WHERE product_id = 1;
┌────────────┬────────────────┐
│ product_id │ stock_quantity │
│   int32    │     int32      │
├────────────┼────────────────┤
│          1 │             12 │
└────────────┴────────────────┘
```

👉 The `CHECK` rule refuses it — even if the app forgot to check the stock.

---

# Consistency: a Negative Price

<!-- duckdb-session: shop -->
```text
D UPDATE products SET price = -5 WHERE product_id = 1;
Constraint Error: CHECK constraint failed on table "products"
  with expression CHECK((price > 0))
D SELECT product_id, price FROM products WHERE product_id = 1;
┌────────────┬───────────────┐
│ product_id │     price     │
│   int32    │ decimal(10,2) │
├────────────┼───────────────┤
│          1 │        321.52 │
└────────────┴───────────────┘
```

The `CHECK (price > 0)` rule refuses the change: product 1 still costs `$321.52`.

---

# A Return Is a Transaction, Too

A product return at ShopSmart (only a `completed` order can be returned):

1. set the order's `status` to `'cancelled'`
2. put each item's `quantity` back into `stock_quantity`
3. insert a `refunds` row (`refund_amount` = `SUM(quantity × unit_price)` of the order's items)

All three — or none.

```sql
CREATE TABLE refunds (
    refund_id     INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    refund_date   DATE NOT NULL,
    refund_amount DECIMAL(10, 2) NOT NULL CHECK (refund_amount > 0),
    reason        VARCHAR NOT NULL
);
```

---

# Which Order Do We Return? Order 3

<!-- duckdb-session: shop -->
```text
D SELECT order_id, status, total_amount FROM orders WHERE order_id = 3;
┌──────────┬───────────┬───────────────┐
│ order_id │  status   │ total_amount  │
│  int32   │  varchar  │ decimal(10,2) │
├──────────┼───────────┼───────────────┤
│        3 │ completed │        538.49 │
└──────────┴───────────┴───────────────┘
D SELECT product_id, quantity, unit_price, quantity * unit_price AS line_total
    FROM order_items WHERE order_id = 3 ORDER BY item_id;
┌────────────┬──────────┬───────────────┬───────────────┐
│ product_id │ quantity │  unit_price   │  line_total   │
│   int32    │  int32   │ decimal(10,2) │ decimal(18,2) │
├────────────┼──────────┼───────────────┼───────────────┤
│         53 │        1 │         43.41 │         43.41 │
│         12 │        2 │         70.14 │        140.28 │
│         29 │        4 │         38.05 │        152.20 │
│         15 │        3 │        106.23 │        318.69 │
│         60 │        3 │        114.59 │        343.77 │
└────────────┴──────────┴───────────────┴───────────────┘
```

---

# Which Order Do We Return? Order 3 (cont.)

Order 3 is `completed`, so it can be returned. The refund = what the customer paid for its **5** items:

<!-- duckdb-session: continue -->
```text
D SELECT SUM(quantity * unit_price) AS refund_amount FROM order_items
    WHERE order_id = 3;
┌───────────────┐
│ refund_amount │
│ decimal(38,2) │
├───────────────┤
│        998.35 │
└───────────────┘
```

**Why not refund `orders.total_amount`?** It matches the items in **0 of 200** orders
(order 3: `$538.49` stored, `$998.35` of items). Refund what was actually bought.

---

# The Return of Order 3, in SQL

<!-- duckdb-session: shop_refunds -->
```text
D BEGIN;
D UPDATE orders SET status = 'cancelled' WHERE order_id = 3
    AND status = 'completed';
D UPDATE products SET stock_quantity = stock_quantity + i.quantity
    FROM order_items AS i WHERE i.order_id = 3
    AND products.product_id = i.product_id;
D INSERT INTO refunds SELECT 1, 3, DATE '2025-01-20', SUM(quantity * unit_price),
    'arrived damaged' FROM order_items WHERE order_id = 3;
D COMMIT;
```

Three changes — status, stock, refund — saved **together** by one `COMMIT`.

---

# The Return of Order 3, in SQL (cont.)

<!-- duckdb-session: continue -->
```text
D SELECT order_id, status FROM orders WHERE order_id = 3;
┌──────────┬───────────┐
│ order_id │  status   │
│  int32   │  varchar  │
├──────────┼───────────┤
│        3 │ cancelled │
└──────────┴───────────┘
D SELECT refund_id, order_id, refund_amount, reason FROM refunds;
┌───────────┬──────────┬───────────────┬─────────────────┐
│ refund_id │ order_id │ refund_amount │     reason      │
│   int32   │  int32   │ decimal(10,2) │     varchar     │
├───────────┼──────────┼───────────────┼─────────────────┤
│         1 │        3 │        998.35 │ arrived damaged │
└───────────┴──────────┴───────────────┴─────────────────┘
```

`transactions_demo_2.py` does the same in Python with `process_return()` — and **refuses** a second return of order 3, because its status is no longer `completed`.

---

# Which Statements Belong Together?

| Task | Statements in one transaction |
|---|---|
| Transfer money | subtract from one account → add to another |
| Borrow a book | insert loan → lower `copies_available` |
| Place an order | insert order → insert items → lower stock → set total |
| Process a return | change status → restore stock → insert refund |

> 💡 Ask: "If the program stopped **between** these two statements, would the data be wrong?"
> If yes, they belong in **one** transaction.

---

# Why Concurrency Matters

Real systems serve many users at the same time:
- 100 customers checking out at once
- the stock must stay accurate
- reports must not show half-updated data

Without **isolation**, transactions running at the same time can cause four
problems.

---

# Four Concurrency Problems

1. **Dirty read** — reading a change that is not committed yet (and may be undone)
2. **Non-repeatable read** — the same query in one transaction gives a different value
3. **Phantom read** — new rows appear between two identical queries
4. **Lost update** — two users change the same row, and one change is lost

The next four slides show each one **as it could happen** in a database without
enough isolation. Then we run the same four experiments in **DuckDB**.

---

# Dirty Read

```
Transaction A                  Transaction B
─────────────                  ─────────────
BEGIN;                         BEGIN;
UPDATE products
SET stock_quantity = 0
WHERE product_id = 1;          SELECT stock_quantity FROM products
                               WHERE product_id = 1;
                               → reads 0 (DIRTY!)
ROLLBACK;
-- stock is back to 12         -- B used a value that never existed!
```

B read data that was **never committed**.

---

# Non-Repeatable Read

```
Transaction A                  Transaction B
─────────────                  ─────────────
BEGIN;
SELECT price FROM products
WHERE product_id = 1;
→ $321.52                      UPDATE products SET price = 299.99
                               WHERE product_id = 1;
                               -- saved at once (auto-commit)
SELECT price FROM products
WHERE product_id = 1;
→ $299.99 (!!)
COMMIT;
```

Same query, different result, inside the **same** transaction.

---

# Phantom Read

```
Transaction A                  Transaction B
─────────────                  ─────────────
BEGIN;
SELECT COUNT(*) FROM orders
WHERE status = 'processing';
→ 30                           INSERT INTO orders VALUES
                               (201, 5, DATE '2025-01-15',
                               'processing', 100.00);
                               -- saved at once (auto-commit)
SELECT COUNT(*) FROM orders
WHERE status = 'processing';
→ 31 (!!)
COMMIT;
```

A new row "appeared" (a **phantom**) between two identical queries.

---

# Lost Update

```
Transaction A                  Transaction B
─────────────                  ─────────────
BEGIN;                         BEGIN;
SELECT stock_quantity          SELECT stock_quantity
FROM products                  FROM products
WHERE product_id = 1;          WHERE product_id = 1;
→ 12                           → 12
-- app computes 12 - 1 = 11    -- app computes 12 - 1 = 11
UPDATE products                UPDATE products
SET stock_quantity = 11        SET stock_quantity = 11
WHERE product_id = 1;          WHERE product_id = 1;
COMMIT;                        COMMIT;
```

Two items sold, but the stock went down by only 1!

**Tip:** let the database do the math in **one** statement:
`SET stock_quantity = stock_quantity - 1`.

---

# Isolation Levels (SQL Standard)

The SQL standard names four **isolation levels**, from weakest to strongest. The table
shows what each level **must** prevent:

| Level | Dirty read | Non-repeatable read | Phantom read |
|---|---|---|---|
| READ UNCOMMITTED | possible | possible | possible |
| READ COMMITTED | prevented | possible | possible |
| REPEATABLE READ | prevented | prevented | possible |
| SERIALIZABLE | prevented | prevented | prevented |

**SERIALIZABLE** = transactions behave as if they ran **one after another**.
Stronger = safer, but fewer transactions can run at the same time.

---

# Isolation in DuckDB: One Level, Always On

DuckDB has **no levels to choose from**:

<!-- duckdb-session: bank -->
```text
D SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
Parser Error: syntax error at or near "ISOLATION"

LINE 1: SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
                        ^^^^^^^^^
```

DuckDB always uses **snapshot isolation** (built on **MVCC** — multi-version
concurrency control):

- each transaction sees the data **as it was when the transaction started**,
  plus its **own** changes
- DuckDB keeps the old version of a changed row while others may still need it
- so **readers never wait** for writers, and writers never wait for readers

---

# Two Users in DuckDB: How We Test

A DuckDB **file** can be opened for writing by **one program** at a time — so two
terminal windows cannot both run `duckdb shop.duckdb`. Inside **one** program,
though, we can open **two connections** to the same file — two users:

```python
user_a = duckdb.connect('shop.duckdb')   # A>
user_b = duckdb.connect('shop.duckdb')   # B>
```

Each connection has its **own** transactions. The next sessions show what each user
typed (`A> ` or `B> `) and what DuckDB answered — the same experiments as
`transactions_demo_2.py`, Section 6.

---

# DuckDB Test 1: No Dirty Read ✅

<!-- duckdb-session: shop users=2 -->
```text
A> BEGIN;
A> UPDATE products SET stock_quantity = 0 WHERE product_id = 1;
A> SELECT stock_quantity FROM products WHERE product_id = 1;
┌────────────────┐
│ stock_quantity │
│     int32      │
├────────────────┤
│              0 │
└────────────────┘
B> SELECT stock_quantity FROM products WHERE product_id = 1;
┌────────────────┐
│ stock_quantity │
│     int32      │
├────────────────┤
│             12 │
└────────────────┘
A> ROLLBACK;
```

A sees its **own** uncommitted `0`; B still sees the committed **12**: no dirty read.

---

# DuckDB Test 2: No Non-Repeatable Read ✅

<!-- duckdb-session: shop users=2 -->
```text
A> BEGIN;
A> SELECT price FROM products WHERE product_id = 1;
┌───────────────┐
│     price     │
│ decimal(10,2) │
├───────────────┤
│        321.52 │
└───────────────┘
B> UPDATE products SET price = 299.99 WHERE product_id = 1;
A> SELECT price FROM products WHERE product_id = 1;
┌───────────────┐
│     price     │
│ decimal(10,2) │
├───────────────┤
│        321.52 │
└───────────────┘
```

B's change is committed at once, but A keeps its **snapshot**: still `$321.52`.

---

# DuckDB Test 2: No Non-Repeatable Read (cont.)

<!-- duckdb-session: continue -->
```text
A> COMMIT;
A> SELECT price FROM products WHERE product_id = 1;
┌───────────────┐
│     price     │
│ decimal(10,2) │
├───────────────┤
│        299.99 │
└───────────────┘
```

A's transaction has ended; a new statement sees B's committed `$299.99`.

---

# DuckDB Test 3: No Phantom Read ✅

<!-- duckdb-session: shop users=2 -->
```text
A> BEGIN;
A> SELECT COUNT(*) AS processing_orders FROM orders WHERE status = 'processing';
┌───────────────────┐
│ processing_orders │
│       int64       │
├───────────────────┤
│                30 │
└───────────────────┘
B> INSERT INTO orders VALUES (201, 5, DATE '2025-01-15', 'processing', 100.00);
A> SELECT COUNT(*) AS processing_orders FROM orders WHERE status = 'processing';
┌───────────────────┐
│ processing_orders │
│       int64       │
├───────────────────┤
│                30 │
└───────────────────┘
```

B's new order is committed, but A's count stays **30**: no phantom row.

---

# DuckDB Test 3: No Phantom Read (cont.)

<!-- duckdb-session: continue -->
```text
A> COMMIT;
A> SELECT COUNT(*) AS processing_orders FROM orders WHERE status = 'processing';
┌───────────────────┐
│ processing_orders │
│       int64       │
├───────────────────┤
│                31 │
└───────────────────┘
```

A's transaction has ended; now A sees B's new order: **31**.

---

# DuckDB Test 4: Lost Update → an Error ✅

Both users sell one smartphone the "read → compute → write" way (`12 − 1 = 11`). B, the
**second** writer, fails at once — then rolls back and **retries** with `stock_quantity - 1`:

<!-- duckdb-session: shop users=2 -->
```text
A> BEGIN;
B> BEGIN;
A> UPDATE products SET stock_quantity = 11 WHERE product_id = 1;
B> UPDATE products SET stock_quantity = 11 WHERE product_id = 1;
TransactionContext Error: Conflict on update!
A> COMMIT;
B> ROLLBACK;
B> UPDATE products SET stock_quantity = stock_quantity - 1 WHERE product_id = 1;
B> SELECT stock_quantity FROM products WHERE product_id = 1;
┌────────────────┐
│ stock_quantity │
│     int32      │
├────────────────┤
│             10 │
└────────────────┘
```

---

# Two Writers, Different Rows: Both Succeed

<!-- duckdb-session: shop users=2 -->
```text
A> BEGIN;
B> BEGIN;
A> UPDATE products SET stock_quantity = stock_quantity - 1 WHERE product_id = 1;
B> UPDATE products SET stock_quantity = stock_quantity - 1 WHERE product_id = 2;
A> COMMIT;
B> COMMIT;
A> SELECT product_id, stock_quantity FROM products WHERE product_id <= 2
     ORDER BY 1;
┌────────────┬────────────────┐
│ product_id │ stock_quantity │
│   int32    │     int32      │
├────────────┼────────────────┤
│          1 │             11 │
│          2 │            124 │
└────────────┴────────────────┘
```

A conflict happens only on the **same row**. DuckDB never makes anyone **wait**,
so transactions never get stuck waiting for each other (no **deadlocks**).

---

# Isolation in DuckDB: Summary of the Tests

| Problem | Result in DuckDB |
|---|---|
| Dirty read | ✅ prevented — B still sees 12 while A's 0 is uncommitted |
| Non-repeatable read | ✅ prevented — A still sees `$321.52` until A's transaction ends |
| Phantom read | ✅ prevented — A's count stays 30 until A's transaction ends |
| Lost update | ✅ prevented — B's write fails: `Conflict on update!` |

👉 On `Conflict on update!`: `ROLLBACK`, then **try the whole transaction again**.

---

# Transactions in Python: the Pattern

```python
try:
    con.execute("BEGIN")
    # ... several statements that belong together ...
    con.execute("COMMIT")
except Exception as e:
    con.execute("ROLLBACK")
    print(f"Transaction rolled back: {e}")
```

DuckDB's Python API also has methods for the same three commands:

```python
con.begin()      # = BEGIN
con.commit()     # = COMMIT
con.rollback()   # = ROLLBACK
```

---

# Best Practices

1. Put every group of changes that must happen **together** in one transaction
2. Keep transactions **short**
3. No user input, emails or web calls **inside** a transaction
   (send the confirmation email **after** `COMMIT`)
4. Always **handle errors**: `ROLLBACK` on failure
5. Let the database do the math: `SET x = x - 1`, not "read, compute, write"
6. Declare your rules (`CHECK`, `NOT NULL`, keys) — DuckDB enforces them
7. Check that a row exists before you change it (`RETURNING`, or count first)
8. In DuckDB, on `Conflict on update!`: `ROLLBACK`, then **try again**

---

# ACID in DuckDB

| Property | DuckDB |
|---|---|
| Atomicity | `BEGIN` / `COMMIT` / `ROLLBACK` (no `SAVEPOINT`); one statement is always all or nothing; `CREATE`/`DROP` can be rolled back |
| Consistency | `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `UNIQUE`, `NOT NULL` enforced; list them with `duckdb_constraints()` |
| Isolation | snapshot isolation (MVCC); a conflicting write fails with `Conflict on update!` |
| Durability | with a database **file**: write-ahead log (`.wal`) + `CHECKPOINT` |

Only **one program** at a time can open a DuckDB file for writing. DuckDB is built
for **analytics**, not for thousands of users writing at once.

---

# In-Class Exercise

Design a safe transaction for **placing an order** with two products:

- create the order
- add the two order items
- lower the stock of each product

**Questions:**
- Which statements go between `BEGIN` and `COMMIT`?
- Which rule stops the stock from going below 0?
- What should happen if the second product is out of stock?

(Compare your answer with `place_order()` in `transactions_demo_2.py`.)

---

# Common Mistakes

- Forgetting `COMMIT` ❌ — the changes are lost when the connection closes
- `COMMIT` after an error, thinking the work was saved ❌ — DuckDB saves nothing
- `ROLLBACK` without `BEGIN`, hoping to undo ❌ — auto-commit already saved it
- Thinking an `UPDATE` that matched no row is an error ❌ — it just changes 0 rows
- "Read, compute in Python, write back" ❌ — a lost update waiting to happen
- Keeping a transaction open for a long time ❌
- Expecting durability from `duckdb.connect()` (in memory) ❌ — use a file

---

# Cheat Sheet: Transactions in DuckDB

| I want to … | Write |
|---|---|
| group statements | `BEGIN;` … `COMMIT;` |
| undo everything since `BEGIN` | `ROLLBACK;` (or `ABORT;`) |
| only read, safely | `BEGIN TRANSACTION READ ONLY;` |
| keep part of the work (no `SAVEPOINT`) | commit that part in its **own** transaction |
| make the database reject bad data | `PRIMARY KEY`, `NOT NULL`, `CHECK (…)`, `REFERENCES …` |
| see a table's rules | `SELECT * FROM duckdb_constraints() WHERE table_name = '…';` |
| see which rows a change touched | `UPDATE … RETURNING *;` |
| change a number safely with many users | `SET x = x - 1` (one statement), never read → compute → write |
| handle `Conflict on update!` | `ROLLBACK`, then try the transaction again |
| survive a crash | a database **file** + `COMMIT` (+ `CHECKPOINT;` to empty the `.wal`) |
| in Python | `try: BEGIN … COMMIT` / `except: ROLLBACK` |

---

# Check Yourself (Final-Exam Style)

Start each question from Alice `$500`, Bob `$200` (`CHECK (balance >= 0)`).

1. Without `BEGIN`: `UPDATE accounts SET balance = balance - 100 WHERE id = 1;` then `ROLLBACK;`. What is Alice's balance, and what does `ROLLBACK` answer?
2. `BEGIN;` Bob `+600`; Alice `−600` (fails); `COMMIT;`. What is Bob's balance?
3. `UPDATE accounts SET balance = 0 WHERE id = 99;` — is it an error?
4. Library: book 1 has **0** copies. `BEGIN;` insert Kevin's loan; lower the count (fails); `ROLLBACK;`. How many rows are in `loans` for book 1 — Maria's only, or Maria's and Kevin's?
5. Without `BEGIN`: `UPDATE accounts SET balance = balance - 300;` (both rows). What are the two balances afterwards?

---

# Check Yourself (cont.)

6. Name the ACID property: (a) Bob's `+600` is undone because Alice's `−600` failed; (b) the `CHECK` stops a negative balance; (c) B still sees stock 12 while A's uncommitted 0 is pending; (d) after `COMMIT`, a power failure does not lose the transfer.
7. In DuckDB, users A and B both read stock 12, and both write `SET stock_quantity = 11`. What happens?
8. Which SQL-standard isolation level is the weakest one that prevents phantom reads? Which isolation does DuckDB use?
9. `BEGIN; CREATE TABLE audit_log (msg VARCHAR); ROLLBACK;` — does `audit_log` exist afterwards?

---

# Check Yourself: Answers

1. **`$400`**: the `UPDATE` was saved at once (auto-commit). `ROLLBACK` answers `TransactionContext Error: cannot rollback - no transaction is active`.
2. **`$200`**: the failed statement aborted the transaction; `COMMIT` of an aborted transaction saves nothing.
3. **No**: it changes 0 rows. (That is why `transfer()` counts the accounts first.)
4. **Maria's only** (1 row): `ROLLBACK` undid Kevin's loan together with the failed `UPDATE`.
5. **Still `$500` and `$200`**: Bob's row breaks the `CHECK`, so the **whole** statement fails — Alice's row is not changed either.

---

# Check Yourself: Answers (cont.)

6. (a) **A**tomicity (b) **C**onsistency (c) **I**solation (d) **D**urability.
7. A's `UPDATE` works; B's fails at once with `Conflict on update!`. A commits (stock 11); B rolls back and retries with
   `SET stock_quantity = stock_quantity - 1` → **10**: both sales counted.
8. **SERIALIZABLE** (REPEATABLE READ may still allow phantoms). DuckDB always uses **snapshot isolation**; in our tests it prevented
   dirty, non-repeatable and phantom reads, and turned a lost update into an error.
9. **No**: in DuckDB, `CREATE TABLE` is part of the transaction, so `ROLLBACK` removes it.

---

# Summary

- A **transaction** = a group of statements: **all or nothing**
- `BEGIN` / `COMMIT` / `ROLLBACK`; without `BEGIN`, every statement is saved at once
- A failed statement **aborts** the transaction: only `ROLLBACK` is left
- **ACID**: Atomicity, Consistency, Isolation, Durability
- Declared rules (`PRIMARY KEY`, `NOT NULL`, `CHECK`, `REFERENCES`) keep data valid
- Concurrency problems: dirty read, non-repeatable read, phantom, lost update
- **DuckDB:** snapshot isolation (MVCC); a write conflict is an **error** — roll back and retry;
  durability needs a **file**

👉 Fast systems are good. **Correct** systems are essential.

---

# What Is Next?

**December 3 — Course Review**
- Going over everything: `SELECT` → aggregation → joins → subqueries →
  database design → ranking functions → transactions
- Want more? The `bonus/` folder: Project Integration (CTEs, `LAG`, `LEAD`) and
  Modern Data (JSON, `PIVOT`, lists)

---

# Questions?

Thank you!

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
