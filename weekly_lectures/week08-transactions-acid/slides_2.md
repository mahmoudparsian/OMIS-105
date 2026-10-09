---
marp: true
theme: default
paginate: true
header: "OMIS 105 – Database Management Systems"
footer: "Week 8: Transactions & ACID"
---

# OMIS 105: Database Management Systems
## Week 8 — Transactions & ACID
### Data Integrity Under Concurrent Access

---

# This Week's Goals

1. Understand what a transaction is
2. Master the ACID properties
3. Learn about concurrency problems
4. Explore isolation levels
5. Work with transactions in DuckDB

---

# Setup: Tables with Constraints

`read_csv` alone creates tables **without** rules. For this week, create the
tables with keys and `CHECK` rules first, then load the CSV data
(run from the `week08-transactions-acid` folder):

```sql
CREATE OR REPLACE TABLE products (
    product_id     INTEGER PRIMARY KEY,
    product_name   VARCHAR NOT NULL,
    category_id    INTEGER,
    price          DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0)
);
INSERT INTO products SELECT * FROM read_csv('data/products.csv');      -- 64 rows

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

# Setup (continued)

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

To run this setup again, drop `order_items` first: a table that others
reference cannot be replaced while the reference exists.

---

# Why Transactions?

Imagine ShopSmart processes 1,000 orders per minute:
- Two customers buying the last item in stock at the same moment
- Payment processing while inventory updates
- What if the system crashes mid-operation?

We need **guarantees** that data stays correct.

---

# Session 1: Transactions and ACID

---

# What Is a Transaction?

A **transaction** is a sequence of operations treated as a **single logical unit**.

Either **all** operations succeed, or **none** of them do.

```sql
BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

Without `BEGIN`, every statement is its own transaction and is saved
immediately (**auto-commit**). (The `accounts` table is created in `slides_1`.)

---

# The Classic Example: Bank Transfer

Transfer $100 from Alice to Bob:

```
Step 1: Read Alice's balance ($500)
Step 2: Subtract $100 from Alice ($400)
Step 3: Read Bob's balance ($200)
Step 4: Add $100 to Bob ($300)
```

What if the system crashes after Step 2 but before Step 4?
Alice lost $100, Bob never received it!

---

# Transactions Solve This

```sql
BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Alice
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- Bob
COMMIT;  -- Both changes saved atomically
```

If anything fails → `ROLLBACK` undoes everything since `BEGIN`.

---

# ACID Properties

| Property | Meaning |
|----------|---------|
| **A**tomicity | All or nothing — no partial transactions |
| **C**onsistency | Data moves from one valid state to another |
| **I**solation | Concurrent transactions don't interfere |
| **D**urability | Once committed, data survives crashes |

---

# Atomicity

- A transaction is **indivisible**
- If any statement fails, **all** changes are rolled back
- No "half-done" transactions

```sql
BEGIN;
  INSERT INTO orders VALUES (201, 5, DATE '2024-07-01', 'processing', 150.00);
  INSERT INTO order_items VALUES (608, 201, 99, 2, 75.00);
  -- Constraint Error: Violates foreign key constraint because key
  -- "product_id: 99" does not exist in the referenced table
ROLLBACK;
```

Order 201 is **not** saved either: `SELECT * FROM orders WHERE order_id = 201` returns 0 rows.

In DuckDB, after an error the transaction is **aborted**. Even if you type
`COMMIT`, nothing is saved — DuckDB rolls it back. Write `ROLLBACK` to make
your intent clear.

---

# Consistency

- Transactions take the database from one **valid state** to another
- All constraints (PK, FK, CHECK, UNIQUE) must hold after the transaction
- If a transaction would violate a constraint, it is rejected

```sql
-- This fails: the table has CHECK (price > 0)
BEGIN;
  UPDATE products SET price = -5 WHERE product_id = 1;
  -- Constraint Error: CHECK constraint failed on table products
  -- with expression CHECK((price > 0))
ROLLBACK;
-- product 1 still costs 321.52
```

The database can only enforce the rules you **declare**.
Rules that live only in your head (or your app) are not checked.

---

# Isolation

- Concurrent transactions behave **as if** they ran sequentially
- One transaction's uncommitted changes are invisible to others
- Prevents interference between simultaneous operations

```
Transaction A                  Transaction B
─────────────                  ─────────────
BEGIN;                         BEGIN;
UPDATE products
SET stock_quantity = 9
WHERE product_id = 1;          SELECT stock_quantity FROM products
                               WHERE product_id = 1;
                               -- Should B see 10 or 9?
COMMIT;                        COMMIT;
```

Answer: **10**. A has not committed yet, so B must not see A's change.

---

# Durability

- Once a transaction is **committed**, it is permanent
- Survives power failures, crashes, hardware issues
- Achieved through **write-ahead logging (WAL)**

```
1. Write the changes and a "committed" record to a log file on disk
2. Only then report "COMMIT succeeded"
3. Later, copy the changes into the main database file
-- After a crash, the database replays the log on restart:
-- committed changes are kept, uncommitted ones are dropped
```

DuckDB's log is the `.wal` file next to your `.duckdb` file.

---

# Transaction Control Statements

```sql
-- Start a transaction
BEGIN TRANSACTION;   -- or just BEGIN

-- Save all changes permanently
COMMIT;

-- Undo all changes since BEGIN
ROLLBACK;

-- Create a savepoint (partial rollback target) — not in DuckDB
SAVEPOINT my_save;

-- Roll back to a savepoint (keep earlier work) — not in DuckDB
ROLLBACK TO SAVEPOINT my_save;
```

`BEGIN`, `COMMIT`, and `ROLLBACK` work everywhere.
Savepoints work in PostgreSQL, MySQL, Oracle, and SQL Server, but **not in
DuckDB** (`Parser Error: syntax error at or near "SAVEPOINT"`).

---

# Savepoints — Partial Rollback (PostgreSQL, MySQL, ...)

```sql
-- PostgreSQL / MySQL syntax — DuckDB does not support SAVEPOINT
BEGIN;
  INSERT INTO orders VALUES (201, 5, '2024-07-01', 'processing', 150.00);
  SAVEPOINT after_order;
  
  INSERT INTO order_items VALUES (608, 201, 99, 2, 75.00);
  -- Oops, wrong product
  ROLLBACK TO SAVEPOINT after_order;
  
  INSERT INTO order_items VALUES (608, 201, 10, 2, 75.00);
  -- Correct product
COMMIT;
-- Order and correct item are saved; wrong item was rolled back
```

In DuckDB, roll back the whole transaction and start again with the correct product.

---

# Session 2: Concurrency and Isolation

---

# Why Concurrency Matters

Real databases serve many users simultaneously:
- 100 customers checking out at once
- Inventory must stay accurate
- Reports must not show half-updated data

---

# Concurrency Problems

Without proper isolation, concurrent transactions can cause:

1. **Dirty Read** — reading uncommitted changes
2. **Non-Repeatable Read** — same query gives different results
3. **Phantom Read** — new rows appear between queries
4. **Lost Update** — one update overwrites another

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
-- stock is back to 10         -- B used a wrong value!
```

B read data that was **never committed**.

---

# Non-Repeatable Read

```
Transaction A                  Transaction B
─────────────                  ─────────────
BEGIN;                         BEGIN;
SELECT price FROM products
WHERE product_id = 1;
→ reads $99.99                 UPDATE products SET price = 79.99
                               WHERE product_id = 1;
                               COMMIT;
SELECT price FROM products
WHERE product_id = 1;
→ reads $79.99 (!!)
COMMIT;                        
```

Same query, different result within the same transaction.

---

# Phantom Read

```
Transaction A                  Transaction B
─────────────                  ─────────────
BEGIN;                         BEGIN;
SELECT COUNT(*) FROM orders    
WHERE status = 'processing';   
→ 31 orders                   INSERT INTO orders VALUES
                               (201, 5, '2024-07-01',
                               'processing', 100.00);
                               COMMIT;
SELECT COUNT(*) FROM orders    
WHERE status = 'processing';   
→ 32 orders (!!)
COMMIT;                        
```

A new row "appeared" (phantom) between two identical queries.

---

# Lost Update

```
Transaction A                  Transaction B
─────────────                  ─────────────
BEGIN;                         BEGIN;
SELECT stock_quantity          SELECT stock_quantity
FROM products                  FROM products
WHERE product_id = 1;          WHERE product_id = 1;
→ 10                           → 10
-- app computes 10 - 1 = 9     -- app computes 10 - 1 = 9
UPDATE products                UPDATE products
SET stock_quantity = 9         SET stock_quantity = 9
WHERE product_id = 1;          WHERE product_id = 1;
COMMIT;                        COMMIT;
```

Two items sold, but stock only decreased by 1!

Tip: let the database do the math in one statement:
`SET stock_quantity = stock_quantity - 1`.

---

# Isolation Levels

The SQL standard defines four isolation levels, from weakest to strongest.
The table shows what each level **must** prevent (real databases often prevent more):

| Level | Dirty Read | Non-Repeatable | Phantom |
|-------|-----------|----------------|---------|
| READ UNCOMMITTED | Possible | Possible | Possible |
| READ COMMITTED | Prevented | Possible | Possible |
| REPEATABLE READ | Prevented | Prevented | Possible |
| SERIALIZABLE | Prevented | Prevented | Prevented |

---

# READ UNCOMMITTED

- Weakest isolation — transactions can see uncommitted changes
- Almost never used in practice
- Maximum concurrency, minimum safety

```sql
-- SQL Server / MySQL syntax (not supported in DuckDB)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
```

---

# READ COMMITTED (Common Default)

- Can only see **committed** data
- Prevents dirty reads
- The default in PostgreSQL, Oracle, and SQL Server
  (MySQL's default is REPEATABLE READ)
- DuckDB has no levels to choose from: it always uses
  **snapshot isolation** (see the "Isolation in DuckDB" slide)

```sql
-- PostgreSQL / MySQL / SQL Server syntax (not supported in DuckDB)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

---

# REPEATABLE READ

- Guarantees the same query returns the same rows within a transaction
- Prevents dirty reads and non-repeatable reads
- Phantoms still possible (by the standard; PostgreSQL also prevents them)

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;   -- not in DuckDB
```

---

# SERIALIZABLE (Strongest)

- Transactions behave as if they ran one after another
- Prevents all concurrency problems
- Slowest — reduces throughput
- Used when correctness is critical (banking, inventory)

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;      -- not in DuckDB
```

---

# Isolation Level Trade-offs

```
More concurrent, faster     ←─────────────────→     More correct, slower
READ UNCOMMITTED → READ COMMITTED → REPEATABLE READ → SERIALIZABLE
```

Choose the **weakest level** that gives you the **correctness you need**.

---

# Isolation in DuckDB (Tested)

DuckDB uses **snapshot isolation**: each transaction reads the data as it was
when the transaction **started**. Tested with two connections to one DuckDB file:

| Problem | Result in DuckDB |
|---------|------------------|
| Dirty read | ✅ Prevented — B still sees 10 while A's change is uncommitted |
| Non-repeatable read | ✅ Prevented — B still sees 10 even after A commits |
| Phantom read | ✅ Prevented — A's `COUNT(*)` stays the same until A commits |
| Lost update | ✅ Prevented — B's update fails with `Conflict on update!` |

When two transactions change the **same row**, DuckDB does not make one wait:
the second one gets an error, and must `ROLLBACK` and try again.

---

# Locking Mechanisms

Many databases (PostgreSQL, MySQL, SQL Server) use **locks** to enforce isolation:

| Lock Type | Allows |
|-----------|--------|
| Shared (S) | Multiple readers, no writers |
| Exclusive (X) | One writer, no readers |
| Row-level | Lock individual rows |
| Table-level | Lock entire table |

DuckDB works differently: it keeps **multiple versions** of changed rows
(MVCC), so readers never wait for writers. Conflicting writes fail at once
instead of waiting (*optimistic* concurrency control).

---

# Deadlocks

```
Transaction A          Transaction B
─────────────          ─────────────
LOCK row 1             LOCK row 2
...                    ...
REQUEST lock row 2     REQUEST lock row 1
(waiting for B)        (waiting for A)
     ↓                      ↓
        DEADLOCK! 🔒
```

Solution: the DBMS detects the deadlock and rolls back one transaction.

(Deadlocks need transactions that **wait** for locks. DuckDB's writes do not
wait — a conflict causes an immediate error — so classic deadlocks do not occur there.)

---

# Preventing Deadlocks

In databases that use locks:

1. **Lock ordering** — always acquire locks in the same order
2. **Lock timeout** — give up after waiting too long
3. **Keep transactions short** — hold locks briefly
4. **Avoid user interaction** inside transactions

---

# Transaction Best Practices

1. **Keep transactions short** — minimize lock time
2. **Don't do I/O** inside transactions (no user prompts, no API calls)
3. **Handle errors** — always ROLLBACK on failure
4. **Use appropriate isolation** — don't over-isolate
5. **Avoid long-running** transactions in OLTP systems
6. **Test concurrent** scenarios

---

# Error Handling Pattern

```python
try:
    con.execute("BEGIN")
    con.execute("UPDATE products SET stock_quantity = stock_quantity - 2 WHERE product_id = 10")
    con.execute("INSERT INTO order_items VALUES (609, 1, 10, 2, 75.00)")
    con.execute("COMMIT")
    print("Transaction committed successfully")
except Exception as e:
    con.execute("ROLLBACK")
    print(f"Transaction rolled back: {e}")
```

DuckDB's Python API also has `con.begin()`, `con.commit()`, and `con.rollback()`.

---

# ACID in DuckDB

DuckDB provides:
- **Atomicity**: Full support — BEGIN/COMMIT/ROLLBACK (no savepoints)
- **Consistency**: PRIMARY KEY, FOREIGN KEY, CHECK, UNIQUE, NOT NULL enforced
- **Isolation**: Snapshot isolation (MVCC); conflicting writes fail with an error
- **Durability**: When using a database **file** (with a write-ahead log)

```python
# Persistent database → full durability
con = duckdb.connect('shopsmart.duckdb')

# In-memory → no durability (data lost on exit)
con = duckdb.connect()
```

Only **one program** at a time can open a DuckDB file for writing.
DuckDB is built for analytics, not for thousands of users writing at once.

---

# Real-World Transaction Scenarios

| Scenario | Transaction Scope |
|----------|------------------|
| Place an order | Insert order → insert items → update stock |
| Process return | Update order status → refund → restore stock |
| Transfer funds | Debit one account → credit another |
| Batch price update | Update prices → verify constraints |
| User registration | Create user → create profile (send the email **after** COMMIT) |

---

# Summary

- **Transactions** group operations into atomic units
- **ACID** guarantees: Atomicity, Consistency, Isolation, Durability
- Concurrency problems: dirty reads, non-repeatable reads, phantoms, lost updates
- **Isolation levels** trade concurrency for correctness
- Many databases use **locks** (deadlocks must be handled);
  DuckDB uses snapshot isolation and reports write conflicts as errors
- Keep transactions **short** and always handle **errors**

---

# What Is Next?

**Week 9: Project Integration**
- CTEs, subqueries, and `EXISTS`
- `LAG`, `LEAD`, `NTILE`, `FIRST_VALUE`
- Apply everything from Weeks 1–8 in one project

---

# Questions?

Thank you!

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
