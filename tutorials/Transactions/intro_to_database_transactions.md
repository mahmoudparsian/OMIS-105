---
title: Database Transactions (MySQL)
author: Max's Course
marp: true
theme: default
paginate: true

---

# Database Transactions (A → Z)
### Introductory Database Systems  
### Using MySQL

---
## 🤔 Do Both Databases Support Transactions?

Yes — both support transactions:

- DuckDB ✅  
- MySQL ✅  

Both provide:

- ACID guarantees  
- BEGIN / COMMIT / ROLLBACK  

👉 So technically, both are correct and reliable

---

## 🟢 What is DuckDB Designed For?

DuckDB is built for:

- 📊 Data analysis (OLAP)
- 📁 Working with local data (CSV, Parquet)
- 👤 Mostly single-user usage

👉 Think:

> “Analyze data quickly on one machine”

---

## 🔵 What is MySQL Designed For?

MySQL is built for:

- 🌍 Real-world applications
- 👥 Many users at the same time
- 💳 Systems like banking, shopping

👉 Think:

> “Many people using the system together”

---

## 🎯 Why We Use MySQL for Transactions

Even though DuckDB supports transactions:

👉 MySQL is better for teaching because:

- Shows multiple users interacting
- Demonstrates real-world behavior
- Helps us understand:
  - Conflicts
  - Isolation
  - System reliability

---

💡 Simple idea:
> DuckDB = analysis  
> MySQL = real-world systems

---
## ⚙️ Why We Use MySQL for Transactions

We use MySQL because it is designed for 
real transactional systems:

- ✅ Full support for ACID transactions
- ✅ Handles multiple users concurrently
- ✅ Supports COMMIT / ROLLBACK / isolation levels
- ✅ Widely used in real applications:
  - Banking systems
  - E-commerce platforms
  - Enterprise databases

👉 MySQL represents how transactions work in production systems

---

## ⚠️ Why Not DuckDB for Transactions?

DuckDB is excellent, but for a different purpose:

- ❌ Designed for analytics (OLAP), not transactions (OLTP)
- ❌ Limited focus on concurrent multi-user updates
- ❌ Not ideal for demonstrating:
  - Transaction conflicts
  - Isolation behavior
  - Real-world system failures

✅ DuckDB is perfect for: 

- Data analysis
- SQL learning
- Data warehousing

👉 But for learning transactions, MySQL is the right choice

---

## 🔐 ACID Properties (Transactions)

ACID defines the 4 guarantees that make transactions reliable:

- A — Atomicity  
  👉 All or nothing  
  If any step fails, the whole transaction is undone  
  (COMMIT vs ROLLBACK)

- C — Consistency  
  👉 Valid state always  
  Data must follow rules (constraints, no invalid values)

- I — Isolation  
  👉 No interference  
  Transactions do not see each other’s partial work

- D — Durability  
  👉 Permanent after commit  
  Once committed, data survives crashes

---
# ACID in one sentence:

💡 In one sentence:  

> ACID ensures transactions are safe, correct, and reliable

---

# 🎯 Why Transactions Matter

Imagine:

- You transfer $100 from Account A → B
- A is debited
- System crashes before B is credited ❌

👉 Result: Money disappears

Transactions prevent this.

---

# 🧠 What is a Transaction?

A transaction is a group of SQL operations that:

- Execute as one unit
- Either:
  - ✅ ALL succeed
  - ❌ ALL fail

---

# 🧱 Simple Example

```sql 
UPDATE accounts 
SET balance = balance - 100 
WHERE id = 1; 

UPDATE accounts 
SET balance = balance + 100 
WHERE id = 2; 
```
👉 These must run together or not at all

---

# 🔑 Transaction Keywords

| Command | Meaning |
|--------|--------|
| BEGIN / START TRANSACTION | Start transaction |
| COMMIT | Save changes |
| ROLLBACK | Undo changes |

---

# ⚙️ Why MySQL (Not DuckDB)?

We use MySQL because:

- ✅ Supports real transactions
- ✅ Multi-user environment
- ✅ Used in production systems

Why NOT DuckDB?

- ❌ Primarily analytical (OLAP)
- ❌ Limited transaction teaching realism
- ❌ Not designed for concurrent updates

👉 Transactions are about real-world systems

---

# 🧪 Setup Table

```sql 
CREATE TABLE accounts (     
   id INT PRIMARY KEY,     
   name VARCHAR(50),     
   balance INT );  

INSERT INTO accounts VALUES 
(1, 'Alice', 1000), 
(2, 'Bob', 1000); 
```
---

# ▶️ First Transaction Demo

```sql 
START TRANSACTION;  

UPDATE accounts 
SET balance = balance - 100 
WHERE id = 1;  

UPDATE accounts 
SET balance = balance + 100 
WHERE id = 2;  

COMMIT; 
```
---

# 🔍 What Happened?

- Alice → 900
- Bob → 1100
- Changes are permanent

---

# ❌ What if Something Goes Wrong?

```sql 
START TRANSACTION;  

UPDATE accounts 
SET balance = balance - 100 
WHERE id = 1;  -- ERROR happens here!  

ROLLBACK; 
```

👉 Alice remains 1000

---

# 🧠 Key Idea

> Until you COMMIT, nothing is permanent.

---

# 🔐 ACID Properties

Transactions follow ACID

| Property | Meaning |
|---------|--------|
| Atomicity | All or nothing |
| Consistency | Valid data |
| Isolation | No interference |
| Durability | Permanent after commit |

---

# ⚛️ Atomicity (All or Nothing)

```sql 
START TRANSACTION;  

UPDATE accounts SET balance = balance - 500 WHERE id = 1; UPDATE accounts SET balance = balance + 500 WHERE id = 2;  

ROLLBACK; 
```
👉 Nothing changes

---

# 🧮 Consistency

Database rules must hold:

- No negative balances
- Valid constraints

👉 Transactions protect integrity

---

# 🔄 Isolation (Conceptual)

Two users working at the same time:

User A:

```sql 
START TRANSACTION; 

UPDATE accounts SET balance = 0 WHERE id = 1; 
```

User B:
```sql 
SELECT * FROM accounts; 
```

👉 Should B see the change?

---

# 🔐 Isolation Levels (Intro Only)

MySQL supports:

- READ UNCOMMITTED
- READ COMMITTED
- REPEATABLE READ (default)
- SERIALIZABLE

👉 We won’t go deep, just awareness.

---

# 💾 Durability

After COMMIT:

sql COMMIT; 

👉 Even if system crashes:

- Data is safe
- Stored permanently

---

# 🧪 Full Demo Scenario

```sql 
START TRANSACTION;  
UPDATE accounts SET balance = balance - 200 WHERE id = 1; UPDATE accounts SET balance = balance + 200 WHERE id = 2;  SELECT * FROM accounts;  
-- Decide: COMMIT; -- OR ROLLBACK; 
```
---

# 🔍 Observe Behavior

Before COMMIT:

- Changes visible in session

After ROLLBACK:

- Changes disappear

---

# ⚠️ Common Mistake

Forgetting COMMIT:

```sql 
START TRANSACTION; 
UPDATE accounts SET balance = 0 WHERE id = 1; 
-- session ends 
```

👉 MySQL may rollback automatically

---

# 🧪 Hands-On Exercise

1. Start transaction  
2. Deduct 300 from Alice  
3. Do NOT commit  
4. Check balance  
5. Rollback  

👉 What happens?

---

# 🎯 Real-World Use Cases

Transactions are used in:

- Banking systems
- E-commerce checkout
- Airline bookings
- Inventory systems

---

# 🧠 Key Takeaways

- Transactions = safe execution
- COMMIT = save
- ROLLBACK = undo
- ACID = guarantees correctness

---

# 🚀 Final Thought

> Transactions turn SQL into a reliable system, not just queries.

---

# ✅ End

Next:

- Locks
- Concurrency control
- Isolation levels (deep dive)
