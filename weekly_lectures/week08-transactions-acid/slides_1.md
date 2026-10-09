---
title: OMIS 105 - Week 8 (Transactions & ACID)
author: Dr. Mahmoud Parsian
marp: true
theme: default
paginate: true
class: lead
style: |
  section {
    justify-content: flex-start;
  }
---

# OMIS 105  
## Week 8: Transactions & ACID (Reliability)

---

# Agenda

- What is a transaction?
- Why transactions matter
- ACID properties (the intuition)
- Constraints: `NOT NULL` and `CHECK`
- SQL commands: `BEGIN`, `COMMIT`, `ROLLBACK`
- Failure scenarios
- Concurrency basics (light)
- Hands-on practice

---

# Recap

- Week 7: Performance & indexing  

👉 Today: Make data **correct and reliable**

---

# What is a Transaction?

A **transaction** is:

👉 A group of SQL statements that the database treats as **one unit**

Either:
- **All** of them succeed ✅  
- Or **none** of them take effect ❌  

---

# Real Example (Bank Transfer)

Transfer $100 from Alice → Bob:

1. Subtract $100 from Alice  
2. Add $100 to Bob  

👉 Both must happen — or neither

---

# Problem Without Transactions

If the system crashes after step 1:

- Alice lost $100 ❌  
- Bob never received it ❌  

👉 $100 has disappeared. The data is now **inconsistent**.

---

# ACID Properties

Transactions guarantee four properties:

- **A** → Atomicity  
- **C** → Consistency  
- **I** → Isolation  
- **D** → Durability  

---

# Atomicity (All or Nothing)

👉 Either every statement in the transaction happens, or none does

Example:
- Subtract from Alice **and** add to Bob — never only one of them

---

# Consistency (Valid State)

Before and after every transaction:

👉 The data follows **all the rules** (constraints)

Example:
- No negative balance — if the table has a `CHECK (balance >= 0)` rule
- A transaction that would break a rule is rejected

---

# Isolation (No Interference)

Many users work at the same time:

👉 Each transaction behaves **as if it were alone**

Example:
- Two people withdraw from the same account at the same moment
- The database must not "lose" one of the withdrawals

---

# Durability (Permanent)

After `COMMIT`:

👉 The change is saved **permanently**

Even if:
- the program crashes  
- the power fails  

(This needs a database **file**. An in-memory DuckDB database
disappears when the program ends.)

---

# Try It: An Accounts Table with Rules

```sql
CREATE OR REPLACE TABLE accounts (
    id      INTEGER PRIMARY KEY,
    owner   VARCHAR NOT NULL,                              -- must have a value
    balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0)   -- never negative
);

INSERT INTO accounts VALUES (1, 'Alice', 500.00), (2, 'Bob', 200.00);
```

- `NOT NULL`: the column must always have a value
- `CHECK (condition)`: every row must make the condition true

These rules are how the database enforces **consistency**.

---

# SQL Commands

```sql
BEGIN;      -- start a transaction
COMMIT;     -- save all changes since BEGIN
ROLLBACK;   -- undo all changes since BEGIN
```

Without `BEGIN`, each statement is its **own** transaction and is saved
immediately (this is called **auto-commit**).

---

# Transaction Example

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1;          -- Alice: 500 → 400

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;          -- Bob: 200 → 300

COMMIT;
```

Both changes are saved together. Total money: still $700.

---

# What if You Change Your Mind?

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Alice: 400 → 300
SELECT * FROM accounts;                                    -- you see 300 here
ROLLBACK;
SELECT * FROM accounts;                                    -- Alice is back to 400
```

👉 `ROLLBACK` undoes **everything** since `BEGIN`

---

# What if a Statement Fails?

Alice now has $400. Try to move $600:

```sql
BEGIN;
UPDATE accounts SET balance = balance + 600 WHERE id = 2;  -- Bob: OK so far
UPDATE accounts SET balance = balance - 600 WHERE id = 1;  -- Alice: -200!
-- Constraint Error: CHECK constraint failed on table accounts
-- with expression CHECK((balance >= 0))
ROLLBACK;
```

After the error, DuckDB marks the transaction as **aborted**:
any further query says *"Current transaction is aborted (please ROLLBACK)"*.

Bob's +600 is **not** saved. Atomicity protects us.

---

# Failure Scenario (Important)

👉 “What if the system crashes after the first UPDATE?”

Without a transaction:
- the first change is already saved → inconsistent data ❌  

With a transaction:
- nothing was committed → the database returns to the state before `BEGIN` ✅  

---

# Concurrency (Light Intro)

Many users at the same time can cause problems:

- **Dirty read:** reading a change that is later undone
- **Lost update:** two users change the same row, and one change is lost

👉 **Isolation** prevents these problems

---

# Isolation Levels (Concept Only)

The SQL standard defines four levels, from weakest to strongest:

- Read Uncommitted  
- Read Committed  
- Repeatable Read  
- Serializable  

Stronger = safer, but less work can happen at the same time.

DuckDB uses one level for everything: **snapshot isolation**
(each transaction sees the data as it was when it started).

👉 Just awareness (no deep dive)

---

# Real-World Thinking

Ask:

👉 “What must NEVER go wrong?”

Examples:
- money transfers  
- orders and payments  
- inventory (stock counts)  

These operations belong inside transactions.

---

# In-Class Exercise

Design a safe transaction for **placing an order**:

- create the order  
- add the order items  
- reduce the stock for each product  

Questions:
- Which statements go between `BEGIN` and `COMMIT`?
- Which constraint stops the stock from going below 0?
- What should happen if one product is out of stock?

---

# Common Mistakes

- Forgetting `COMMIT` ❌ (the changes are lost when the connection closes)  
- Running `COMMIT` after an error, and thinking the work was saved ❌
  (in DuckDB, the aborted transaction is rolled back instead)  
- Thinking every statement always succeeds ❌  
- Keeping a transaction open for a long time ❌  

---

# Mental Model

Transaction = safety layer  
ACID = the guarantees  
Constraints = the rules  

👉 Database = reliable system

---

# Hands-On Lab Idea

- Create the `accounts` table (with `CHECK`)
- Do a transfer with `BEGIN` ... `COMMIT`
- Try a transfer that breaks the `CHECK` rule
- Use `ROLLBACK` and confirm nothing changed

---

# Summary

- A transaction = all or nothing  
- ACID: Atomicity, Consistency, Isolation, Durability  
- `NOT NULL` and `CHECK` keep the data valid  
- `BEGIN` / `COMMIT` / `ROLLBACK` control transactions  

👉 Databases protect data integrity

---

# What’s Next?

Week 9: Project Integration
- CTEs and subqueries, `EXISTS`
- `LAG`, `LEAD`, `NTILE`, `FIRST_VALUE`
- Putting all the concepts together

---

# Final Thought

Fast systems are good.  
Correct systems are essential.

👉 Reliability is everything.

---

# Let’s Build Safe Systems 🚀

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
