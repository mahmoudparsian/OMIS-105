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
  }
  table {
    font-size: 0.7em;
  }
---

# OMIS 105: Week 10
## Transactions & ACID <br> Keeping Data Correct and Reliable

---

# Agenda

**Part 1 — Transactions and ACID** (a tiny bank: Alice and Bob)
- What a transaction is, and why we need one
- `BEGIN`, `COMMIT`, `ROLLBACK` — and auto-commit
- ACID: Atomicity, Consistency, Isolation, Durability
- Rules the database enforces: `PRIMARY KEY`, `NOT NULL`, `CHECK`, `REFERENCES`

**Part 2 — Transactions in a Store, and Many Users** (ShopSmart)
- Orders and returns as transactions
- Concurrency problems and isolation levels
- How DuckDB handles two users at once

---

# The Notebooks for This Week

Run them from inside `weekly_lectures/week10-transactions-acid/`:

| Notebook | What it shows |
|---|---|
| `transactions_demo_1.py` | Part 1 on the `accounts` table: auto-commit, `COMMIT`, `ROLLBACK`, a failed statement, `transfer()`, no `SAVEPOINT`, durability with a file |
| `transactions_demo_2.py` | Part 2 on ShopSmart: one order = one transaction, `place_order()`, `process_return()`, and four two-user experiments |

Every result on these slides comes from running the SQL in DuckDB 2.0.

---

# Recap

- Week 9: ranking functions — `ROW_NUMBER`, `RANK`, `DENSE_RANK`
- Weeks 3–9: **reading** data with `SELECT`

👉 Today: **changing** data safely — so it stays **correct and reliable**

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

---

# The Classic Example: A Bank Transfer

Move $100 from Alice to Bob:

```
Step 1: Subtract $100 from Alice   ($500 → $400)
Step 2: Add $100 to Bob            ($200 → $300)
```

What if the system crashes **after Step 1 but before Step 2**?

- Alice lost $100 ❌
- Bob never received it ❌
- $100 has disappeared — the data is now **wrong**

👉 Both steps must happen — or neither.

---

# Our Table: `accounts`, with Rules

```sql
CREATE OR REPLACE TABLE accounts (
    id      INTEGER PRIMARY KEY,                           -- unique, never NULL
    owner   VARCHAR NOT NULL,                              -- must have a value
    balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0)   -- never negative
);

INSERT INTO accounts VALUES (1, 'Alice', 500.00), (2, 'Bob', 200.00);
```

- `NOT NULL`: the column must always have a value
- `CHECK (condition)`: every row must make the condition true

Alice $500 + Bob $200 = **$700**. A transfer must never change the total.

---

# The Three Commands

```sql
BEGIN;      -- start a transaction  (also: BEGIN TRANSACTION)
COMMIT;     -- save all changes since BEGIN
ROLLBACK;   -- undo all changes since BEGIN
```

**Auto-commit:** without `BEGIN`, each statement is its **own** transaction and is
saved immediately. Then there is nothing to undo:

```sql
UPDATE accounts SET balance = balance - 100 WHERE id = 1;   -- saved at once
ROLLBACK;
-- TransactionContext Error: cannot rollback - no transaction is active
```

---

# A Transfer as a Transaction

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;   -- Alice: 500 → 400
UPDATE accounts SET balance = balance + 100 WHERE id = 2;   -- Bob:   200 → 300

COMMIT;
```

Both changes are saved **together**. Total money: still $700.

---

# Change Your Mind: `ROLLBACK`

Starting again from Alice $500, Bob $200:

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
SELECT balance FROM accounts WHERE id = 1;   -- 400 (you see your own change)
ROLLBACK;
SELECT balance FROM accounts WHERE id = 1;   -- 500 (undone)
```

👉 `ROLLBACK` undoes **everything** since `BEGIN`.

---

# What If a Statement Fails?

Alice has $500. Try to move **$600** to Bob:

```sql
BEGIN;
UPDATE accounts SET balance = balance + 600 WHERE id = 2;   -- Bob: OK so far
UPDATE accounts SET balance = balance - 600 WHERE id = 1;   -- Alice: -100!
-- Constraint Error: CHECK constraint failed on table "accounts"
-- with expression CHECK((balance >= 0))
SELECT * FROM accounts;
-- TransactionContext Error: Current transaction is aborted (please ROLLBACK)
ROLLBACK;
```

After an error, DuckDB marks the transaction as **aborted**. Bob's +600 is **not**
saved: Alice $500, Bob $200.

---

# A Common Mistake: `COMMIT` After an Error

Same failed transfer, but the program types `COMMIT` instead of `ROLLBACK`:

```sql
BEGIN;
UPDATE accounts SET balance = balance + 600 WHERE id = 2;
UPDATE accounts SET balance = balance - 600 WHERE id = 1;   -- CHECK error
COMMIT;                                                     -- answers "OK" ...
SELECT balance FROM accounts WHERE id = 2;                  -- ... but Bob has 200
```

An aborted transaction can **only** be rolled back. `COMMIT` saves nothing.

👉 Always check for errors. Write `ROLLBACK` to make your intent clear.

---

# ACID: Four Guarantees

| Property | Meaning | In the bank |
|---|---|---|
| **A**tomicity | All or nothing | Never subtract from Alice without adding to Bob |
| **C**onsistency | Every rule holds before and after | `CHECK (balance >= 0)`: no negative balance |
| **I**solation | Transactions at the same time don't interfere | Two withdrawals at once: none is "lost" |
| **D**urability | After `COMMIT`, the change survives a crash | The transfer is still there after a power failure |

---

# Atomicity (All or Nothing)

- A transaction cannot be divided
- If **any** statement fails, **all** its changes are undone
- No "half-done" transactions

Example: the $600 transfer above — Bob's +600 was undone because Alice's −600
failed.

---

# Consistency (Valid Data)

- Every rule you **declare** holds before and after each transaction
- Rules: `PRIMARY KEY`, `NOT NULL`, `CHECK`, `UNIQUE`, `REFERENCES` (foreign key)
- A statement that would break a rule is **rejected**

```sql
INSERT INTO accounts VALUES (3, NULL, 50.00);
-- Constraint Error: NOT NULL constraint failed: accounts."owner"
INSERT INTO accounts VALUES (1, 'Carol', 50.00);
-- Constraint Error: Duplicate key "id: 1" violates primary key constraint.
```

The database checks only the rules you **declare**. A rule that lives only in your
head (or in your app) is not checked.

---

# Isolation (No Interference)

Many users work at the same time:

👉 Each transaction behaves **as if it were alone**.

Example: two people withdraw from the same account at the same moment — the
database must not "lose" one of the withdrawals.

Part 2 shows four concurrency problems, and what DuckDB does about each.

---

# Durability (Permanent)

After `COMMIT`, the change is saved **permanently** — even if the program crashes
or the power fails.

How: **write-ahead logging (WAL)**

```
1. Write the changes and a "committed" record to a log file on disk
2. Only then report "COMMIT succeeded"
3. Later, copy the changes into the main database file
-- After a crash, the database replays the log on restart:
-- committed changes are kept, uncommitted ones are dropped
```

DuckDB's log is the `.wal` file next to your `.duckdb` file.

---

# Durability Needs a File

```python
con = duckdb.connect('bank.duckdb')   # a database file → durable
con = duckdb.connect()                # in memory → lost when the program ends
```

`transactions_demo_1.py`, Section 10, tests it with a file:
- Alice's −100 is **committed**, then the connection is closed → **kept**
- Bob's +100 is **never committed**, then the connection is closed → **gone**

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

---

# A Safe Transfer in Python (cont.)

Why count the accounts first?

An `UPDATE` whose `WHERE` matches **no row** is **not** an error — it changes
0 rows. Without the check, a transfer to account 99 would subtract $100 from Alice
and add it to **nobody**.

| Test | Returns |
|---|---|
| Alice → Bob, $100 | `True` |
| Alice → Bob, $1,000 (`CHECK` fails) | `False` |
| Alice → account 99 (does not exist) | `False` |

---

# Undo Part of a Transaction? `SAVEPOINT`

PostgreSQL, MySQL, Oracle and SQL Server can undo **part** of a transaction:

```sql
-- PostgreSQL / MySQL syntax — NOT supported in DuckDB
BEGIN;
INSERT INTO accounts VALUES (3, 'Dave', 300.00);
SAVEPOINT after_dave;
INSERT INTO accounts VALUES (4, 'Eve', 400.00);
ROLLBACK TO SAVEPOINT after_dave;     -- undo Eve, keep Dave
COMMIT;
```

DuckDB answers: `Parser Error: syntax error at or near "SAVEPOINT"`

---

# The DuckDB Way: Two Transactions

Put the part you want to keep in its **own** transaction:

```sql
BEGIN;
INSERT INTO accounts VALUES (3, 'Dave', 300.00);
COMMIT;                 -- Dave is saved

BEGIN;
INSERT INTO accounts VALUES (4, 'Eve', 400.00);
ROLLBACK;               -- Eve is undone
```

Result: Dave is kept, Eve is not.

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
INSERT INTO products SELECT * FROM read_csv('data/products.csv');      -- 64 rows
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
INSERT INTO orders SELECT * FROM read_csv('data/orders.csv');          -- 200 rows
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
INSERT INTO order_items SELECT * FROM read_csv('data/order_items.csv'); -- 607 rows
```

To run the setup again, drop `order_items` first: a table that another table
references cannot be replaced.

---

# One Order = One Transaction

Customer 5 buys 2 × product 1 (Smartphone X12, $321.52; **12** in stock):

```sql
BEGIN;
INSERT INTO orders VALUES (201, 5, DATE '2025-01-15', 'processing', 643.04);
INSERT INTO order_items VALUES (608, 201, 1, 2, 321.52);
UPDATE products SET stock_quantity = stock_quantity - 2 WHERE product_id = 1;
COMMIT;
```

Order 201 is saved, and the stock goes from 12 to 10.

An order without its item, or an item without the stock going down, would leave
the data wrong — so the statements belong **together**.

---

# Atomicity: a Wrong Product

```sql
BEGIN;
INSERT INTO orders VALUES (201, 5, DATE '2025-01-15', 'processing', 150.00);
INSERT INTO order_items VALUES (608, 201, 99, 2, 75.00);
-- Constraint Error: Violates foreign key constraint because key
-- "product_id: 99" does not exist in the referenced table
ROLLBACK;
```

Order 201 is **not** saved either:
`SELECT COUNT(*) FROM orders WHERE order_id = 201` returns 0.

---

# Consistency: Not Enough Stock, Negative Price

```sql
BEGIN;
INSERT INTO orders VALUES (201, 5, DATE '2025-01-15', 'processing', 6430.40);
INSERT INTO order_items VALUES (608, 201, 1, 20, 321.52);
UPDATE products SET stock_quantity = stock_quantity - 20 WHERE product_id = 1;
-- Constraint Error: CHECK constraint failed on table "products"
-- with expression CHECK((stock_quantity >= 0))
ROLLBACK;                                   -- stock is still 12

UPDATE products SET price = -5 WHERE product_id = 1;
-- Constraint Error: CHECK constraint failed on table "products"
-- with expression CHECK((price > 0))       -- product 1 still costs 321.52
```

The database protects the stock — even if the application forgot to check it.

---

# A Return Is a Transaction, Too

A product return at ShopSmart (only a `completed` order can be returned):

1. set the order's `status` to `'cancelled'`
2. put each item's `quantity` back into `stock_quantity`
3. insert a `refunds` row (`refund_amount` = the order's `total_amount`)

All three — or none. `transactions_demo_2.py` has `place_order()` and
`process_return()` in Python, with tests that succeed and tests that roll back.

| Task | Statements in one transaction |
|---|---|
| Place an order | insert order → insert items → lower stock → set total |
| Process a return | change status → restore stock → insert refund |
| Transfer money | subtract from one account → add to another |

---

# Why Concurrency Matters

Real databases serve many users at the same time:
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
enough isolation. The values are ShopSmart's: product 1 has 12 in stock and costs
$321.52; 30 orders are `processing`.

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

Same query, different result, inside the same transaction.

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

A new row "appeared" (a phantom) between two identical queries.

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

Tip: let the database do the math in **one** statement:
`SET stock_quantity = stock_quantity - 1`.

---

# Isolation Levels (SQL Standard)

The SQL standard defines four levels, from weakest to strongest. The table shows
what each level **must** prevent (real databases often prevent more):

| Level | Dirty read | Non-repeatable read | Phantom read |
|---|---|---|---|
| READ UNCOMMITTED | possible | possible | possible |
| READ COMMITTED | prevented | possible | possible |
| REPEATABLE READ | prevented | prevented | possible |
| SERIALIZABLE | prevented | prevented | prevented |

Stronger = safer, but fewer transactions can run at the same time.
Choose the **weakest level** that gives you the **correctness you need**.

---

# Isolation Levels in Practice

- **READ UNCOMMITTED** — almost never used
- **READ COMMITTED** — the default in PostgreSQL, Oracle, SQL Server
- **REPEATABLE READ** — the default in MySQL
- **SERIALIZABLE** — transactions behave as if they ran one after another;
  for money and the last item in stock

```sql
-- PostgreSQL / MySQL / SQL Server syntax — NOT supported in DuckDB
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

**DuckDB** has no levels to choose from: it always uses **snapshot isolation** —
each transaction sees the data as it was when the transaction **started**, plus
its own changes.

---

# Isolation in DuckDB (Tested)

`transactions_demo_2.py` opens one database **file** twice — users A and B — and
runs the four problems:

| Problem | Result in DuckDB |
|---|---|
| Dirty read | ✅ prevented — B still sees 12 while A's 0 is uncommitted |
| Non-repeatable read | ✅ prevented — B still sees $321.52 until B's transaction ends |
| Phantom read | ✅ prevented — A's count stays 30 until A's transaction ends |
| Lost update | ✅ prevented — B's write fails: `Conflict on update!` |

When two transactions change the **same row**, DuckDB does not make one wait: the
second gets an error, must `ROLLBACK`, and tries again (the final stock is 10 —
both sales counted).

---

# Locks and Deadlocks (Other Databases)

PostgreSQL, MySQL and SQL Server use **locks**: a writer locks a row, and others
**wait**.

```
Transaction A          Transaction B
─────────────          ─────────────
LOCK row 1             LOCK row 2
REQUEST lock row 2     REQUEST lock row 1
(waits for B)          (waits for A)
           DEADLOCK! 🔒
```

The database detects the deadlock and rolls back one transaction.
Avoid it: lock rows in the same order, and keep transactions short.

DuckDB keeps **multiple versions** of changed rows (MVCC): readers never wait, and
a conflicting write fails **at once** — so classic deadlocks do not occur there.

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

DuckDB's Python API also has `con.begin()`, `con.commit()` and `con.rollback()`.

---

# Best Practices

1. Put every group of changes that must happen **together** in one transaction
2. Keep transactions **short**
3. No user input, emails or web calls **inside** a transaction
   (send the confirmation email **after** `COMMIT`)
4. Always **handle errors**: `ROLLBACK` on failure
5. Let the database do the math: `SET x = x - 1`, not "read, compute, write"
6. Declare your rules (`CHECK`, `NOT NULL`, keys) — the database enforces them

---

# ACID in DuckDB

| Property | DuckDB |
|---|---|
| Atomicity | `BEGIN` / `COMMIT` / `ROLLBACK` (no `SAVEPOINT`) |
| Consistency | `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `UNIQUE`, `NOT NULL` enforced |
| Isolation | snapshot isolation; a conflicting write fails with an error |
| Durability | with a database **file** (and its write-ahead log) |

Only **one program** at a time can open a DuckDB file for writing. DuckDB is built
for analytics, not for thousands of users writing at once.

---

# In-Class Exercise

Design a safe transaction for **placing an order** with two products:

- create the order
- add the two order items
- lower the stock of each product

Questions:
- Which statements go between `BEGIN` and `COMMIT`?
- Which rule stops the stock from going below 0?
- What should happen if the second product is out of stock?

(Compare your answer with `place_order()` in `transactions_demo_2.py`.)

---

# Common Mistakes

- Forgetting `COMMIT` ❌ — the changes are lost when the connection closes
- `COMMIT` after an error, thinking the work was saved ❌ — DuckDB saves nothing
- Thinking an `UPDATE` that matched no row is an error ❌ — it just changes 0 rows
- "Read, compute in Python, write back" ❌ — a lost update waiting to happen
- Keeping a transaction open for a long time ❌

---

# Summary

- A **transaction** = a group of statements: all or nothing
- `BEGIN` / `COMMIT` / `ROLLBACK`; without `BEGIN`, every statement is saved at once
- **ACID**: Atomicity, Consistency, Isolation, Durability
- Declared rules (`PRIMARY KEY`, `NOT NULL`, `CHECK`, `REFERENCES`) keep data valid
- Concurrency problems: dirty read, non-repeatable read, phantom, lost update
- DuckDB: snapshot isolation; a write conflict is an **error** — roll back and retry

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
