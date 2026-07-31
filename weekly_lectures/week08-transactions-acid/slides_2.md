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

# Why Transactions?

Imagine ShopSmart processes 1,000 orders per minute:
- Multiple customers buying the last item in stock
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

If anything fails → `ROLLBACK` undoes everything.

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
  INSERT INTO orders VALUES (201, 5, '2024-07-01', 'processing', 150.00);
  INSERT INTO order_items VALUES (608, 201, 99, 2, 75.00);
  -- If product 99 doesn't exist and FK is enforced → ROLLBACK both
COMMIT;
```

---

# Consistency

- Transactions take the database from one **valid state** to another
- All constraints (PK, FK, CHECK, UNIQUE) must hold after the transaction
- If a transaction would violate a constraint, it is rejected

```sql
-- This should fail: price must be > 0
BEGIN;
  UPDATE products SET price = -5 WHERE product_id = 1;
COMMIT;
-- CHECK constraint violation → transaction rejected
```

---

# Isolation

- Concurrent transactions behave **as if** they ran sequentially
- One transaction's uncommitted changes are invisible to others
- Prevents interference between simultaneous operations

```
Transaction A                  Transaction B
─────────────                  ─────────────
BEGIN;                         BEGIN;
UPDATE stock = 9               
WHERE id = 1;                  SELECT stock FROM products
                               WHERE id = 1;
                               -- Should see 10 or 9?
COMMIT;                        COMMIT;
```

---

# Durability

- Once a transaction is **committed**, it is permanent
- Survives power failures, crashes, hardware issues
- Achieved through **write-ahead logging (WAL)**

```
1. Write changes to log file (on disk)
2. Apply changes to database
3. Mark transaction as committed in log
-- Even if crash at step 2, log allows recovery
```

---

# Transaction Control Statements

```sql
-- Start a transaction
BEGIN TRANSACTION;   -- or just BEGIN

-- Save all changes permanently
COMMIT;

-- Undo all changes since BEGIN
ROLLBACK;

-- Create a savepoint (partial rollback target)
SAVEPOINT my_save;

-- Roll back to a savepoint (keep earlier work)
ROLLBACK TO SAVEPOINT my_save;
```

---

# Savepoints — Partial Rollback

```sql
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
SET stock = 0                  
WHERE id = 1;                  SELECT stock FROM products
                               WHERE id = 1;
                               → reads 0 (DIRTY!)
ROLLBACK;                      
-- stock is back to 10         -- B used wrong value!
```

B read data that was **never committed**.

---

# Non-Repeatable Read

```
Transaction A                  Transaction B
─────────────                  ─────────────
BEGIN;                         BEGIN;
SELECT price FROM products     
WHERE id = 1;                  
→ reads $99.99                 UPDATE products SET price = 79.99
                               WHERE id = 1;
                               COMMIT;
SELECT price FROM products     
WHERE id = 1;                  
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
→ 15 orders                   INSERT INTO orders VALUES
                               (201, 5, '2024-07-01',
                               'processing', 100.00);
                               COMMIT;
SELECT COUNT(*) FROM orders    
WHERE status = 'processing';   
→ 16 orders (!!)              
COMMIT;                        
```

A new row "appeared" (phantom) between two identical queries.

---

# Lost Update

```
Transaction A                  Transaction B
─────────────                  ─────────────
BEGIN;                         BEGIN;
SELECT stock FROM products     SELECT stock FROM products
WHERE id = 1;                  WHERE id = 1;
→ stock = 10                   → stock = 10

UPDATE products                
SET stock = 10 - 1 = 9         UPDATE products
WHERE id = 1;                  SET stock = 10 - 1 = 9
                               WHERE id = 1;
COMMIT;                        COMMIT;
```

Two items sold, but stock only decreased by 1!

---

# Isolation Levels

SQL defines four isolation levels, from weakest to strongest:

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
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
```

---

# READ COMMITTED (Common Default)

- Can only see **committed** data
- Prevents dirty reads
- Most databases default to this level
- **DuckDB uses this level**

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

---

# REPEATABLE READ

- Guarantees the same query returns the same rows within a transaction
- Prevents dirty reads and non-repeatable reads
- Phantoms still possible

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

---

# SERIALIZABLE (Strongest)

- Transactions behave as if they ran one after another
- Prevents all concurrency problems
- Slowest — reduces throughput
- Used when correctness is critical (banking, inventory)

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

---

# Isolation Level Trade-offs

```
More concurrent, faster     ←─────────────────→     More correct, slower
READ UNCOMMITTED → READ COMMITTED → REPEATABLE READ → SERIALIZABLE
```

Choose the **weakest level** that gives you the **correctness you need**.

---

# Locking Mechanisms

Databases use **locks** to enforce isolation:

| Lock Type | Allows |
|-----------|--------|
| Shared (S) | Multiple readers, no writers |
| Exclusive (X) | One writer, no readers |
| Row-level | Lock individual rows |
| Table-level | Lock entire table |

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

Solution: DBMS detects deadlocks and rolls back one transaction.

---

# Preventing Deadlocks

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
    con.execute("UPDATE products SET stock = stock - 1 WHERE id = 1")
    con.execute("INSERT INTO order_items VALUES (...)")
    con.execute("COMMIT")
    print("Transaction committed successfully")
except Exception as e:
    con.execute("ROLLBACK")
    print(f"Transaction rolled back: {e}")
```

---

# ACID in DuckDB

DuckDB provides:
- **Atomicity**: Full support — BEGIN/COMMIT/ROLLBACK
- **Consistency**: CHECK, UNIQUE, NOT NULL constraints enforced
- **Isolation**: Snapshot isolation (similar to REPEATABLE READ)
- **Durability**: When using persistent database files

```python
# Persistent database → full durability
con = duckdb.connect('shopmart.duckdb')

# In-memory → no durability (data lost on exit)
con = duckdb.connect()
```

---

# Real-World Transaction Scenarios

| Scenario | Transaction Scope |
|----------|------------------|
| Place an order | Insert order → insert items → update stock |
| Process return | Update order status → refund → restore stock |
| Transfer funds | Debit one account → credit another |
| Batch price update | Update prices → verify constraints |
| User registration | Create user → create profile → send email |

---

# Summary

- **Transactions** group operations into atomic units
- **ACID** guarantees: Atomicity, Consistency, Isolation, Durability
- Concurrency problems: dirty reads, non-repeatable reads, phantoms, lost updates
- **Isolation levels** trade concurrency for correctness
- **Locks** enforce isolation; deadlocks must be handled
- Keep transactions **short** and always handle **errors**

---

# What Is Next?

**Week 9: Capstone Project**
- Design and implement a complete database
- Apply everything from Weeks 1–8
- Present your work

---

# Questions?

Thank you!

