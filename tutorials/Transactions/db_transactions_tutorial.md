---
marp: true
theme: default
paginate: true
backgroundColor: #0a0f1e
color: #e8f0fe
style: |
  /* ── Base ─────────────────────────────────────────────── */
  section {
    font-family: 'Segoe UI', 'Inter', Helvetica, sans-serif;
    background: #0a0f1e;
    color: #e8f0fe;
    padding: 48px 56px 36px;
    font-size: 18px;
    line-height: 1.6;
  }

  /* ── Headings ──────────────────────────────────────────── */
  h1 {
    font-size: 2.0em;
    color: #60a5fa;
    border-bottom: 3px solid #1e3a8a;
    padding-bottom: 12px;
    margin-bottom: 20px;
    letter-spacing: -0.02em;
  }
  h2 {
    font-size: 1.45em;
    color: #93c5fd;
    margin-bottom: 14px;
    border-left: 4px solid #3b82f6;
    padding-left: 12px;
  }
  h3 {
    font-size: 1.15em;
    color: #bfdbfe;
    margin-bottom: 10px;
  }

  /* ── Code blocks ───────────────────────────────────────── */
  pre {
    background: #0d1f3c;
    border: 1px solid #1e3a8a;
    border-left: 4px solid #3b82f6;
    border-radius: 8px;
    padding: 16px 20px;
    font-size: 0.82em;
    line-height: 1.55;
    margin: 12px 0;
    overflow: hidden;
  }
  code {
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
    color: #7dd3fc;
    background: #0d1f3c;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.88em;
  }
  pre code {
    background: transparent;
    padding: 0;
    color: #e2e8f0;
  }

  /* ── Tables ────────────────────────────────────────────── */
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 14px 0;
    font-size: 0.85em;
  }
  th {
    background: #0d1b40;
    color: #93c5fd;
    padding: 9px 14px;
    text-align: left;
    border-bottom: 2px solid #1e3a8a;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-size: 0.82em;
  }
  td {
    padding: 8px 14px;
    border-bottom: 1px solid #1e2d55;
    color: #cbd5e1;
  }
  tr:nth-child(even) td { background: #0f1f3d; }
  tr:nth-child(odd)  td { background: #0a1528; }

  /* ── Blockquotes / callouts ────────────────────────────── */
  blockquote {
    border-left: 4px solid #f59e0b;
    background: #1a1500;
    border-radius: 0 8px 8px 0;
    padding: 12px 18px;
    margin: 14px 0;
    color: #fde68a;
    font-style: normal;
  }
  blockquote strong { color: #fbbf24; }

  /* ── Lists ─────────────────────────────────────────────── */
  ul, ol { margin: 10px 0 10px 20px; }
  li { margin-bottom: 5px; }
  li::marker { color: #3b82f6; }

  /* ── Highlight / accent boxes ──────────────────────────── */
  .success {
    background: #052e16; border-left: 4px solid #22c55e;
    padding: 10px 16px; border-radius: 0 6px 6px 0;
    color: #86efac; margin: 10px 0;
  }
  .danger {
    background: #1c0a0a; border-left: 4px solid #ef4444;
    padding: 10px 16px; border-radius: 0 6px 6px 0;
    color: #fca5a5; margin: 10px 0;
  }

  /* ── Page number ───────────────────────────────────────── */
  section::after {
    color: #334155; font-size: 0.72em;
  }

  /* ── Title slide overrides ─────────────────────────────── */
  section.title {
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    text-align: center;
  }
  section.title h1 {
    font-size: 2.6em; border: none;
    background: linear-gradient(135deg, #60a5fa, #a78bfa, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 16px;
  }
  section.title h2 { border: none; font-size: 1.2em; color: #94a3b8; }

  /* ── Section divider slides ────────────────────────────── */
  section.divider {
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    text-align: center; background: #060d1f;
  }
  section.divider h1 { font-size: 2.4em; border: none; color: #60a5fa; }
  section.divider p  { color: #64748b; font-size: 1.1em; }

  /* ── Two-column layout ─────────────────────────────────── */
  .cols { display: flex; gap: 24px; }
  .col  { flex: 1; }

  /* ── Badge / pill ──────────────────────────────────────── */
  .badge {
    display: inline-block; padding: 3px 10px;
    border-radius: 999px; font-size: 0.75em;
    font-weight: 700; letter-spacing: 0.05em;
  }
  .badge-blue  { background: #1e3a8a; color: #93c5fd; }
  .badge-green { background: #14532d; color: #86efac; }
  .badge-red   { background: #450a0a; color: #fca5a5; }
  .badge-amber { background: #451a03; color: #fde68a; }
---

<!-- _class: title -->

# 🗄️ Database Transactions
## A Complete Beginner's Guide
### From Zero to Confident · MySQL Edition

<br>

**Introductory Database Course**
*Concepts · Examples · Live MySQL Demos*

---

# 📋 What We'll Cover Today

<div class="cols">
<div class="col">

**Part 1 — The Problem**
- Why do we need transactions?
- What goes wrong without them?

**Part 2 — Core Concepts**
- What IS a transaction?
- The ACID properties
- Transaction lifecycle

**Part 3 — MySQL Commands**
- `START TRANSACTION`
- `COMMIT`
- `ROLLBACK`
- `SAVEPOINT`

</div>
<div class="col">

**Part 4 — Real Demos**
- Bank transfer scenario
- Shopping cart scenario
- Error handling & recovery

**Part 5 — Isolation Levels**
- Read phenomena
- The 4 isolation levels

**Part 6 — Best Practices**
- Common mistakes
- Production guidelines
- Quick-reference cheat sheet

</div>
</div>

> **No prior knowledge assumed.** We start from absolute zero.

---

<!-- _class: divider -->

# Part 1
## The Problem — Why Do We Need Transactions?

---

# 🏦 Meet the Problem: A Bank Transfer

Imagine you transfer **$500** from your Checking account to your Savings account.

Behind the scenes, the database must do **two things**:

```sql
-- Step 1: subtract $500 from Checking
UPDATE accounts SET balance = balance - 500 WHERE account_id = 'CHK-001';

-- Step 2: add $500 to Savings
UPDATE accounts SET balance = balance + 500 WHERE account_id = 'SAV-001';
```

### Looks simple — but what if the computer crashes between Step 1 and Step 2?

<br>

<div class="cols">
<div class="col">

✅ **What should happen:**
- Checking: –$500
- Savings: +$500
- Money is conserved

</div>
<div class="col">

<div class="danger">
❌ <strong>What could go wrong:</strong><br>
Checking: –$500  (done!)<br>
Savings: no change  (crash!)<br>
<strong>$500 just vanished!</strong>
</div>

</div>
</div>

---

# ⚡ Real-World Disasters Without Transactions

| Scenario | Without Transactions | Consequence |
|---|---|---|
| Bank transfer | Money subtracted but not added | **$500 disappears** |
| E-commerce order | Payment charged, inventory not reduced | **Overselling items** |
| Hospital records | Medication prescribed, allergy not checked | **Patient safety risk** |
| Flight booking | Seat reserved, payment fails | **Seat lost, money kept** |
| Payroll run | Some employees paid, server crashes | **Partial payroll** |

<br>

> **The core problem:** Real-world actions often require **multiple database changes** that must ALL succeed or ALL fail together. The database has no way to guarantee this without transactions.

---

# 🧩 The Root Cause: Partial Updates

```
Timeline without transactions:
─────────────────────────────────────────────────────────────

T=1  ➜  UPDATE accounts SET balance = balance - 500 ...   ✅ Done
T=2  ➜  [CRASH / Power failure / Network error]           💥 BOOM
T=3  ➜  UPDATE accounts SET balance = balance + 500 ...   ❌ Never runs

State of database: INCONSISTENT
  · Checking account: $500 short  ← this ran
  · Savings account: unchanged   ← this never ran
```

<br>

### This is the "Partial Update" problem.

Transactions were invented specifically to solve it. A transaction guarantees:

**"Either ALL of these changes are saved, or NONE of them are."**

---

<!-- _class: divider -->

# Part 2
## Core Concepts — What IS a Transaction?

---

# 📦 What Is a Database Transaction?

A **transaction** is a **group of SQL statements** that are treated as a **single unit of work**.

Think of it like a sealed envelope:
- You put multiple changes inside
- You **seal it** (commit) → all changes are saved permanently
- Or you **shred it** (rollback) → all changes are discarded

```
┌─────────────────────────────────────────────┐
│            TRANSACTION ENVELOPE             │
│                                             │
│  📝 UPDATE accounts SET balance = bal - 500 │
│  📝 UPDATE accounts SET balance = bal + 500 │
│  📝 INSERT INTO audit_log VALUES (...)      │
│                                             │
│  SEAL (COMMIT) → all 3 saved permanently   │
│  SHRED (ROLLBACK) → all 3 discarded        │
└─────────────────────────────────────────────┘
```

> A transaction is **all-or-nothing**. There is no "half-done."

---

# 🔬 The ACID Properties

Every proper database transaction must satisfy **4 properties**, called **ACID**:

| Letter | Property | Plain English |
|---|---|---|
| **A** | **Atomicity** | All changes happen, or none happen |
| **C** | **Consistency** | Database goes from one valid state to another |
| **I** | **Isolation** | Concurrent transactions don't interfere |
| **D** | **Durability** | Once committed, data survives crashes |

<br>

These aren't just nice-to-haves — they are the **guarantees** MySQL makes to you when you use transactions correctly.

Let's look at each one carefully.

---

# ⚛️ A — Atomicity

**"All or nothing."**

The word "atom" comes from Greek meaning "indivisible." A transaction is indivisible — you cannot commit only half of it.

```
ATOMIC TRANSACTION (bank transfer):

  BEGIN  →  [subtract $500]  →  [add $500]  →  COMMIT
              ✅ Both happen                    ✅ Saved

  BEGIN  →  [subtract $500]  →  [CRASH]     →  AUTO-ROLLBACK
              ✅ Ran once          💥             ↩️ Undone automatically

Result: database goes back to its state BEFORE the transaction started.
$500 is safe. No money vanished.
```

<br>

> **MySQL guarantees:** If your application crashes mid-transaction, MySQL automatically rolls back the incomplete transaction when it restarts.

---

# 🔗 C — Consistency

**"The database must always be in a valid state."**

You define valid states through **constraints** — rules the database enforces.

```sql
-- These constraints define "valid state" for a bank:
ALTER TABLE accounts ADD CONSTRAINT chk_balance CHECK (balance >= 0);
ALTER TABLE accounts ADD CONSTRAINT fk_customer
    FOREIGN KEY (customer_id) REFERENCES customers(id);
```

A transaction that would **violate a constraint is automatically rejected**:

```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 99999;  -- Would make balance negative!
-- MySQL: ERROR 3819 (HY000): Check constraint 'chk_balance' is violated.
-- Transaction is rolled back. Database stays consistent.
ROLLBACK;
```

> **Consistency** = Transactions can only bring the database from one rule-following state to another rule-following state.

---

# 🔒 I — Isolation

**"Concurrent transactions don't see each other's unfinished work."**

Imagine 1,000 users hitting the database at the same time. Isolation ensures they don't interfere.

```
Timeline with TWO concurrent transactions:

  Alice's Transaction          Bob's Transaction
  ──────────────────           ─────────────────
  START TRANSACTION            START TRANSACTION
  READ balance → $1000
                               READ balance → $1000  ← sees original!
  UPDATE balance = 500
                               UPDATE balance = 800  ← based on $1000!
  COMMIT                       COMMIT
         ↑ Who wins? What does Bob see?
```

This is the **isolation problem** — solved by **Isolation Levels** (covered in Part 5).

> MySQL's default isolation level (`REPEATABLE READ`) prevents most of these anomalies automatically.

---

# 💾 D — Durability

**"Once committed, data is permanent — even if the server crashes 1 second later."**

MySQL achieves durability through the **Write-Ahead Log (WAL)** / **InnoDB Redo Log**:

```
How MySQL guarantees durability:

1. You run COMMIT
2. MySQL writes the transaction to the REDO LOG on disk  ✅
3. MySQL confirms "committed" to your application       ✅
4. MySQL applies changes to the data files (async)

Even if power fails between steps 3 and 4:
→ On restart, MySQL reads the redo log
→ Replays committed transactions
→ Your data is there. Guaranteed.
```

<br>

> **Key setting:** `innodb_flush_log_at_trx_commit = 1` (the default) ensures full durability. Never set it to 0 in production.

---

# 🔄 The Transaction Lifecycle

```
                    ┌─────────────────────────────────┐
                    │                                  │
          ┌─────────▼──────────┐              ┌────────▼────────┐
          │                    │              │                  │
  START ─►│    ACTIVE          │──────────── ►│   COMMITTED      │
          │  (running SQL)     │  COMMIT      │  (permanent)     │
          │                    │              │                  │
          └─────────┬──────────┘              └──────────────────┘
                    │
                    │ ROLLBACK  (or crash, or error)
                    │
          ┌─────────▼──────────┐
          │                    │
          │    ROLLED BACK     │
          │   (all undone)     │
          │                    │
          └────────────────────┘
```

> **Remember:** Until you `COMMIT`, **no other user can see your changes** (under default isolation). You're working in your own private workspace.

---

<!-- _class: divider -->

# Part 3
## MySQL Transaction Commands

---

# 🛠️ Setting Up Our Demo Database

Before the demos, let's create our practice database. Run this once:

```sql
-- ── Create and select our demo database ──────────────────────────────
CREATE DATABASE IF NOT EXISTS txn_demo;
USE txn_demo;

-- ── Accounts table (bank scenario) ───────────────────────────────────
CREATE TABLE IF NOT EXISTS accounts (
    account_id   VARCHAR(20)  PRIMARY KEY,
    owner_name   VARCHAR(100) NOT NULL,
    balance      DECIMAL(12,2) NOT NULL,
    CONSTRAINT chk_balance CHECK (balance >= 0)   -- no negative balances!
);

-- ── Orders table (shopping scenario) ─────────────────────────────────
CREATE TABLE IF NOT EXISTS orders (
    order_id     INT AUTO_INCREMENT PRIMARY KEY,
    customer     VARCHAR(100) NOT NULL,
    product      VARCHAR(100) NOT NULL,
    quantity     INT          NOT NULL,
    total_price  DECIMAL(10,2) NOT NULL,
    status       ENUM('pending','confirmed','cancelled') DEFAULT 'pending'
);

-- ── Inventory table ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS inventory (
    product_id   INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    stock        INT          NOT NULL CHECK (stock >= 0)
);

-- ── Audit log (tracks all transactions) ──────────────────────────────
CREATE TABLE IF NOT EXISTS audit_log (
    log_id       INT AUTO_INCREMENT PRIMARY KEY,
    action       VARCHAR(255) NOT NULL,
    performed_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);
```

---

# 🌱 Seed Data — Populate the Tables

```sql
-- ── Clear existing data (fresh start) ────────────────────────────────
TRUNCATE TABLE audit_log;
TRUNCATE TABLE orders;
DELETE FROM accounts;
DELETE FROM inventory;

-- ── Insert sample accounts ────────────────────────────────────────────
INSERT INTO accounts VALUES
    ('CHK-001', 'Alice Johnson',  1000.00),
    ('SAV-001', 'Alice Johnson',   500.00),
    ('CHK-002', 'Bob Martinez',   2500.00),
    ('SAV-002', 'Bob Martinez',    750.00),
    ('CHK-003', 'Carol White',    3000.00);

-- ── Insert sample inventory ───────────────────────────────────────────
INSERT INTO inventory (product_name, stock) VALUES
    ('Laptop Pro 15',   10),
    ('Wireless Mouse',  50),
    ('USB-C Hub',       25),
    ('Mechanical Keyboard', 15);

-- ── Verify setup ──────────────────────────────────────────────────────
SELECT 'accounts'  AS tbl, COUNT(*) AS rows FROM accounts
UNION ALL
SELECT 'inventory' AS tbl, COUNT(*) AS rows FROM inventory;
```

**Expected output:**

| tbl | rows |
|---|---|
| accounts | 5 |
| inventory | 4 |

---

# 📝 Command 1: `START TRANSACTION`

`START TRANSACTION` opens a new transaction. Everything after this point is **temporary** until you COMMIT or ROLLBACK.

```sql
-- Syntax options (all equivalent):
START TRANSACTION;
BEGIN;
BEGIN WORK;
```

```sql
-- ── Demo: See how changes are "invisible" to others until committed ───

-- Open a transaction
START TRANSACTION;

-- Make a change
UPDATE accounts SET balance = 9999.00 WHERE account_id = 'CHK-001';

-- Check: YOU can see the change
SELECT account_id, owner_name, balance FROM accounts WHERE account_id = 'CHK-001';
-- Result: balance = 9999.00  ← you see it

-- But another user session would still see: balance = 1000.00
-- (Under REPEATABLE READ isolation — covered in Part 5)

-- We haven't committed yet — let's roll it back
ROLLBACK;

-- Verify it's back to original
SELECT account_id, owner_name, balance FROM accounts WHERE account_id = 'CHK-001';
-- Result: balance = 1000.00  ← rollback worked!
```

> **Key insight:** `START TRANSACTION` creates your private workspace. Nothing is real until `COMMIT`.

---

# ✅ Command 2: `COMMIT`

`COMMIT` **permanently saves** all changes made since `START TRANSACTION`.

After a COMMIT:
- Changes are **visible to all users**
- Changes **survive server crashes** (durability)
- You **cannot undo** them with ROLLBACK

```sql
-- ── Demo: A successful bank transfer ─────────────────────────────────

-- Check starting balances
SELECT account_id, owner_name, balance FROM accounts
WHERE account_id IN ('CHK-001', 'SAV-001');

START TRANSACTION;

    -- Step 1: Deduct from Checking
    UPDATE accounts SET balance = balance - 200.00
    WHERE account_id = 'CHK-001';

    -- Step 2: Add to Savings
    UPDATE accounts SET balance = balance + 200.00
    WHERE account_id = 'SAV-001';

    -- Step 3: Log the action
    INSERT INTO audit_log (action)
    VALUES ('Transfer $200 from CHK-001 to SAV-001');

COMMIT;  -- ← All 3 changes are now PERMANENT

-- Verify the transfer happened
SELECT account_id, owner_name, balance FROM accounts
WHERE account_id IN ('CHK-001', 'SAV-001');
```

**Expected result after COMMIT:**

| account_id | owner_name | balance |
|---|---|---|
| CHK-001 | Alice Johnson | 800.00 |
| SAV-001 | Alice Johnson | 700.00 |

---

# ↩️ Command 3: `ROLLBACK`

`ROLLBACK` **discards all changes** made since `START TRANSACTION`. The database returns to the state it was in before the transaction started.

```sql
-- ── Demo: A failed transfer — money protected by ROLLBACK ─────────────

-- Starting balances (Alice: CHK=$800, SAV=$700 from previous demo)
SELECT account_id, balance FROM accounts WHERE account_id IN ('CHK-001', 'SAV-001');

START TRANSACTION;

    -- Deduct $5000 from Checking (Alice only has $800!)
    UPDATE accounts SET balance = balance - 5000.00
    WHERE account_id = 'CHK-001';

    -- Let's check the (invalid) balance mid-transaction
    SELECT account_id, balance FROM accounts WHERE account_id = 'CHK-001';
    -- Shows: -4200.00  ← negative! This violates our CHECK constraint

    -- We detect the problem and abort
    ROLLBACK;  -- ← discard everything

-- Verify Alice's balance is safe
SELECT account_id, balance FROM accounts WHERE account_id IN ('CHK-001', 'SAV-001');
-- Shows: CHK=800.00, SAV=700.00  ← unchanged. Money is safe!
```

> **ROLLBACK is your safety net.** Whenever something goes wrong mid-transaction, `ROLLBACK` restores the database to a clean state.

---

# 🔖 Command 4: `SAVEPOINT`

A **SAVEPOINT** is a named checkpoint *inside* a transaction.  
You can roll back to a savepoint without undoing the entire transaction.

Think of it like **save checkpoints in a video game** — you can rewind to a checkpoint without starting the whole game over.

```sql
-- Syntax:
SAVEPOINT  savepoint_name;       -- create a checkpoint
ROLLBACK TO SAVEPOINT name;      -- undo back to checkpoint
RELEASE SAVEPOINT name;          -- delete the checkpoint (optional cleanup)
```

```sql
-- ── Demo: Multi-step order with a savepoint ────────────────────────────

START TRANSACTION;

    -- Step 1: Create the order
    INSERT INTO orders (customer, product, quantity, total_price)
    VALUES ('Bob Martinez', 'Laptop Pro 15', 1, 1299.00);

    SAVEPOINT order_created;  -- ← CHECKPOINT: order is in

    -- Step 2: Reduce inventory
    UPDATE inventory SET stock = stock - 1
    WHERE product_name = 'Laptop Pro 15';

    SAVEPOINT inventory_updated;  -- ← CHECKPOINT: inventory done

    -- Step 3: Charge the customer's account
    UPDATE accounts SET balance = balance - 1299.00
    WHERE account_id = 'CHK-002';  -- Bob's checking

    -- Oops — Bob only has $2500, charge is $1299. OK!
    -- But what if we had an error at this step?
    -- We can roll back to 'inventory_updated' to undo just the charge
    -- without losing the order and inventory updates.

COMMIT;  -- Everything worked fine — commit all steps
```

---

# 🎮 Savepoint Demo — Rolling Back to a Checkpoint

```sql
-- ── Demo: ROLLBACK TO SAVEPOINT in action ────────────────────────────

-- Reset: Make sure Bob has $2500
UPDATE accounts SET balance = 2500.00 WHERE account_id = 'CHK-002';

START TRANSACTION;

    INSERT INTO orders (customer, product, quantity, total_price)
    VALUES ('Bob Martinez', 'USB-C Hub', 2, 59.98);

    SAVEPOINT after_order;   -- checkpoint 1

    UPDATE inventory SET stock = stock - 2
    WHERE product_name = 'USB-C Hub';

    SAVEPOINT after_inventory;   -- checkpoint 2

    -- Simulate: payment processor returns an error
    -- We want to undo the payment attempt but KEEP the order + inventory
    -- (maybe we'll retry the payment)

    ROLLBACK TO SAVEPOINT after_inventory;
    -- ↑ This undoes everything AFTER after_inventory
    -- Order and inventory change are still pending!

    -- Now retry payment (this time succeeds)
    UPDATE accounts SET balance = balance - 59.98
    WHERE account_id = 'CHK-002';

COMMIT;   -- Save order + inventory + payment

-- Verify
SELECT order_id, customer, product, quantity FROM orders WHERE customer = 'Bob Martinez';
SELECT product_name, stock FROM inventory WHERE product_name = 'USB-C Hub';
SELECT account_id, balance FROM accounts WHERE account_id = 'CHK-002';
```

---

# ⚙️ Auto-Commit Mode

MySQL has a special setting called **`autocommit`**.  
When `autocommit = ON` (the default), every single SQL statement is its own mini-transaction — committed automatically.

```sql
-- Check current autocommit setting
SHOW VARIABLES LIKE 'autocommit';
-- Result: Value = ON   (this is MySQL's default)

-- With autocommit ON:
UPDATE accounts SET balance = 999.00 WHERE account_id = 'CHK-001';
-- ↑ This is INSTANTLY committed. There is NO way to ROLLBACK this!
```

```sql
-- ── How START TRANSACTION interacts with autocommit ────────────────────

-- START TRANSACTION temporarily suspends autocommit
-- until you COMMIT or ROLLBACK

START TRANSACTION;
-- autocommit is now paused for this session

UPDATE accounts SET balance = 100.00 WHERE account_id = 'CHK-001';
-- NOT committed yet!

ROLLBACK;
-- Changes discarded. autocommit resumes.
```

> **Best practice for students:** Always use `START TRANSACTION` ... `COMMIT` explicitly. Never rely on autocommit for multi-step operations. It's a trap!

---

<!-- _class: divider -->

# Part 4
## Real Demos — Putting It All Together

---

# 🏦 Demo 1: Complete Bank Transfer System

A realistic, production-style bank transfer with full error handling.

```sql
-- ── Reset Alice's accounts to known state ─────────────────────────────
UPDATE accounts SET balance = 1000.00 WHERE account_id = 'CHK-001';
UPDATE accounts SET balance =  500.00 WHERE account_id = 'SAV-001';

-- ── See starting state ────────────────────────────────────────────────
SELECT account_id, owner_name, balance FROM accounts
WHERE owner_name = 'Alice Johnson';
```

| account_id | owner_name | balance |
|---|---|---|
| CHK-001 | Alice Johnson | 1000.00 |
| SAV-001 | Alice Johnson | 500.00 |

```sql
-- ── Perform a $300 transfer ───────────────────────────────────────────
START TRANSACTION;

    UPDATE accounts SET balance = balance - 300.00 WHERE account_id = 'CHK-001';
    UPDATE accounts SET balance = balance + 300.00 WHERE account_id = 'SAV-001';
    INSERT INTO audit_log (action) VALUES ('Alice: Transfer $300 CHK→SAV');

COMMIT;

-- ── Verify ────────────────────────────────────────────────────────────
SELECT account_id, owner_name, balance FROM accounts WHERE owner_name = 'Alice Johnson';
SELECT action, performed_at FROM audit_log ORDER BY log_id DESC LIMIT 1;
```

---

# 🏦 Demo 1 Continued: Catching an Overdraft

```sql
-- ── Attempt to overdraft — $5000 from an account with $700 ────────────

-- Alice's checking now has $700 (after the transfer)
SELECT balance FROM accounts WHERE account_id = 'CHK-001';   -- 700.00

START TRANSACTION;

    -- Try to withdraw more than available
    UPDATE accounts SET balance = balance - 5000.00
    WHERE account_id = 'CHK-001';

    -- CHECK: what does the balance look like now (mid-transaction)?
    SELECT account_id, balance FROM accounts WHERE account_id = 'CHK-001';
    -- Shows: -4300.00  ← invalid! Our CHECK constraint blocks the commit

    -- In a real application, you would check this with a SELECT first:
    -- SELECT balance INTO @bal FROM accounts WHERE account_id = 'CHK-001' FOR UPDATE;
    -- IF @bal < 5000 THEN ROLLBACK; END IF;

    -- For now, manually abort:
ROLLBACK;

-- Confirm Alice's money is still safe
SELECT account_id, balance FROM accounts WHERE account_id = 'CHK-001';
-- Result: 700.00  ← protected!

-- The audit log has NO entry for this failed transfer
SELECT COUNT(*) AS failed_log_entries FROM audit_log WHERE action LIKE '%5000%';
-- Result: 0  ← correct, nothing was logged for the failed attempt
```

> **This is the power of atomicity:** Even though the UPDATE ran, the ROLLBACK undid it completely — as if it never happened.

---

# 🛒 Demo 2: E-Commerce Order Processing

A complete checkout flow: place order → reduce inventory → charge customer.

```sql
-- ── Reset inventory to known state ────────────────────────────────────
UPDATE inventory SET stock = 10 WHERE product_name = 'Laptop Pro 15';
UPDATE inventory SET stock = 50 WHERE product_name = 'Wireless Mouse';
UPDATE accounts SET balance = 2500.00 WHERE account_id = 'CHK-002';

-- ── Carol wants to buy 2 Wireless Mice ($29.99 each) ──────────────────
START TRANSACTION;

    -- 1. Check if Carol has enough money (best practice: lock the row)
    SELECT balance FROM accounts WHERE account_id = 'CHK-003' FOR UPDATE;
    -- Result: 3000.00  ← Carol has plenty

    -- 2. Check inventory (lock to prevent overselling)
    SELECT stock FROM inventory WHERE product_name = 'Wireless Mouse' FOR UPDATE;
    -- Result: 50  ← enough in stock

    -- 3. Create the order
    INSERT INTO orders (customer, product, quantity, total_price, status)
    VALUES ('Carol White', 'Wireless Mouse', 2, 59.98, 'confirmed');

    -- 4. Reduce inventory
    UPDATE inventory SET stock = stock - 2
    WHERE product_name = 'Wireless Mouse';

    -- 5. Charge Carol
    UPDATE accounts SET balance = balance - 59.98
    WHERE account_id = 'CHK-003';

    -- 6. Log the sale
    INSERT INTO audit_log (action)
    VALUES ('Carol purchased 2x Wireless Mouse for $59.98');

COMMIT;

-- ── Verify everything ─────────────────────────────────────────────────
SELECT o.customer, o.product, o.quantity, o.total_price, o.status FROM orders o
WHERE o.customer = 'Carol White' ORDER BY o.order_id DESC LIMIT 1;

SELECT product_name, stock FROM inventory WHERE product_name = 'Wireless Mouse';

SELECT account_id, balance FROM accounts WHERE account_id = 'CHK-003';
```

---

# 🛒 Demo 2 Continued: Out-of-Stock Scenario

```sql
-- ── What happens when inventory runs out? ────────────────────────────

-- Let's set stock of Laptop Pro 15 to just 1
UPDATE inventory SET stock = 1 WHERE product_name = 'Laptop Pro 15';

-- Bob tries to buy 3 Laptops (only 1 in stock!)
START TRANSACTION;

    -- Check inventory
    SELECT stock INTO @current_stock FROM inventory
    WHERE product_name = 'Laptop Pro 15' FOR UPDATE;
    -- @current_stock = 1

    -- Simulate the check an application would perform:
    -- IF @current_stock < 3 THEN ... ROLLBACK ... END IF;

    -- Attempt the update anyway (stock would go negative)
    UPDATE inventory SET stock = stock - 3
    WHERE product_name = 'Laptop Pro 15';
    -- This VIOLATES stock >= 0 constraint!
    -- MySQL: ERROR 3819: Check constraint violated

    -- Because of the error, we MUST rollback
ROLLBACK;

-- Verify: stock is still 1 (unchanged)
SELECT product_name, stock FROM inventory WHERE product_name = 'Laptop Pro 15';
-- Result: 1  ← inventory protected

-- No order was created
SELECT COUNT(*) AS laptop_orders FROM orders WHERE product = 'Laptop Pro 15';
-- Result: 0
```

> **Consistency in action:** The CHECK constraint (`stock >= 0`) prevented an invalid state. The transaction was rolled back, leaving everything clean.

---

# 🔖 Demo 3: Savepoints in a Multi-Step Workflow

A payroll scenario showing how savepoints enable partial rollbacks.

```sql
-- ── Monthly payroll for 3 employees ───────────────────────────────────

-- Ensure CHK-001 (Alice) and CHK-002 (Bob) exist with enough balance
-- We use the company account CHK-003 (Carol) as the "payroll fund"
UPDATE accounts SET balance = 10000.00 WHERE account_id = 'CHK-003';
UPDATE accounts SET balance = 500.00   WHERE account_id = 'CHK-001';
UPDATE accounts SET balance = 750.00   WHERE account_id = 'CHK-002';

START TRANSACTION;

    -- Pay Employee 1: Alice — $2,000 bonus
    UPDATE accounts SET balance = balance + 2000.00 WHERE account_id = 'CHK-001';
    UPDATE accounts SET balance = balance - 2000.00 WHERE account_id = 'CHK-003';
    INSERT INTO audit_log (action) VALUES ('Payroll: Alice +$2000');
    SAVEPOINT alice_paid;

    -- Pay Employee 2: Bob — $1,500 bonus
    UPDATE accounts SET balance = balance + 1500.00 WHERE account_id = 'CHK-002';
    UPDATE accounts SET balance = balance - 1500.00 WHERE account_id = 'CHK-003';
    INSERT INTO audit_log (action) VALUES ('Payroll: Bob +$1500');
    SAVEPOINT bob_paid;

    -- Pay Employee 3: New employee — but we discover their account is wrong!
    -- Simulate: account 'CHK-999' doesn't exist → payment fails
    -- We rollback to bob_paid, keeping Alice and Bob's payments
    ROLLBACK TO SAVEPOINT bob_paid;
    INSERT INTO audit_log (action) VALUES ('Payroll: Employee 3 payment FAILED - bad account');

COMMIT;  -- Alice and Bob are paid; Employee 3 is deferred

-- Verify
SELECT account_id, owner_name, balance FROM accounts
WHERE account_id IN ('CHK-001','CHK-002','CHK-003');
SELECT action FROM audit_log ORDER BY log_id DESC LIMIT 3;
```

---

<!-- _class: divider -->

# Part 5
## Isolation Levels
### What happens when multiple users hit the database simultaneously?

---

# 🔀 The Concurrency Problem

In the real world, **hundreds of users** read and write the database simultaneously.

```
Time →    T1         T2         T3         T4
─────────────────────────────────────────────────────
Alice:  [READ $1000]           [WRITE $800]  [COMMIT]
Bob:               [READ ???]
                      ↑
                What does Bob see?
                $1000 (old)?  $800 (new)?  
                Something in between?
```

The answer depends on the **Isolation Level** — a setting that controls how much one transaction can "see" of other transactions' work.

**Three bad things that can happen without proper isolation:**

| Problem | Description |
|---|---|
| **Dirty Read** | You read data another transaction hasn't committed yet |
| **Non-Repeatable Read** | You read the same row twice and get different values |
| **Phantom Read** | New rows appear in your result set between two reads |

---

# 👻 Isolation Problem 1: Dirty Read

A **dirty read** happens when you read data that another transaction has changed **but not yet committed**. If that transaction rolls back, you've read data that never officially existed!

```
Session A (Alice)               Session B (Bob)
────────────────────────────    ────────────────────────────
START TRANSACTION;

UPDATE accounts
  SET balance = 9999.00
  WHERE account_id = 'CHK-001';
                                START TRANSACTION;
                                SELECT balance FROM accounts
                                WHERE account_id = 'CHK-001';
                                -- Dirty read: sees 9999.00! 👻
                                -- But Alice hasn't committed yet!
ROLLBACK;
-- Alice's change is undone.
-- Balance is back to 1000.00.
                                -- Bob made a decision based on
                                -- data that never officially existed!
```

> **MySQL's default (`REPEATABLE READ`) PREVENTS dirty reads.** You would need to set isolation to `READ UNCOMMITTED` to allow them — almost never appropriate.

---

# 🔁 Isolation Problem 2: Non-Repeatable Read

You read a row, another transaction changes it, you read it again — different value!

```
Session A                       Session B
────────────────────────────    ────────────────────────────
START TRANSACTION;

SELECT balance FROM accounts
WHERE account_id = 'CHK-001';
-- Result: 1000.00

                                START TRANSACTION;
                                UPDATE accounts
                                  SET balance = 500.00
                                  WHERE account_id = 'CHK-001';
                                COMMIT;

SELECT balance FROM accounts
WHERE account_id = 'CHK-001';
-- Result: 500.00  ← DIFFERENT!
-- Same transaction, same query, different result!
COMMIT;
```

> **Non-repeatable reads are prevented by `REPEATABLE READ` and `SERIALIZABLE`** isolation levels. Under MySQL's default, the second read still returns 1000.00.

---

# 👥 The 4 Isolation Levels

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | Performance |
|---|---|---|---|---|
| `READ UNCOMMITTED` | ✅ Possible | ✅ Possible | ✅ Possible | 🚀 Fastest |
| `READ COMMITTED` | ❌ Prevented | ✅ Possible | ✅ Possible | 🔵 Fast |
| `REPEATABLE READ` | ❌ Prevented | ❌ Prevented | ⚠️ Partial | 🟡 Moderate |
| `SERIALIZABLE` | ❌ Prevented | ❌ Prevented | ❌ Prevented | 🐢 Slowest |

<br>

**MySQL's default is `REPEATABLE READ`** — a good balance of safety and performance.

```sql
-- Check current isolation level
SELECT @@transaction_isolation;

-- Set isolation level for current session
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;   -- back to default
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Set for a single transaction
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;
-- ... your queries here
COMMIT;
```

---

# 🔐 `FOR UPDATE` — Explicit Row Locking

Sometimes you need to **lock a row** while you're deciding what to do with it.  
`SELECT ... FOR UPDATE` locks the row so no one else can change it until you commit.

```sql
-- ── Scenario: Two cashiers both try to sell the last laptop ───────────

-- Cashier 1 (Session A)          Cashier 2 (Session B)
-- ────────────────────────       ────────────────────────
START TRANSACTION;

-- Lock the inventory row
SELECT stock FROM inventory
WHERE product_name = 'Laptop Pro 15'
FOR UPDATE;
-- stock = 1  ← LOCKED. Session B must wait.

                                   START TRANSACTION;
                                   SELECT stock FROM inventory
                                   WHERE product_name = 'Laptop Pro 15'
                                   FOR UPDATE;
                                   -- SESSION B IS NOW WAITING...

UPDATE inventory SET stock = 0
WHERE product_name = 'Laptop Pro 15';

COMMIT;  -- lock released
                                   -- Session B now gets lock
                                   -- Sees stock = 0
                                   -- Can check and handle "out of stock"
```

> **Use `FOR UPDATE`** whenever you read a value and then update it in the same transaction. This prevents the "lost update" problem.

---

<!-- _class: divider -->

# Part 6
## Best Practices & Common Mistakes

---

# ⚠️ Common Mistake 1: Forgetting to COMMIT

```sql
-- ❌ WRONG: Starting a transaction but never committing
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 'CHK-001';
-- Developer closes the connection or session times out
-- → MySQL automatically ROLLBACKs. Change is LOST.

-- ✅ RIGHT: Always explicitly COMMIT or ROLLBACK
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 'CHK-001';
UPDATE accounts SET balance = balance + 100 WHERE account_id = 'SAV-001';
COMMIT;   -- ← ALWAYS remember this line!
```

---

# ⚠️ Common Mistake 2: Transactions That Are Too Long

```sql
-- ❌ WRONG: Doing slow things inside a transaction
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 'CHK-001';

-- 😱 Sending an email takes 5 seconds...
-- During those 5 seconds, locks are HELD.
-- Other users cannot update CHK-001!
-- [send email]

COMMIT;

-- ✅ RIGHT: Do all your data work first, THEN commit, THEN do slow things
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 'CHK-001';
COMMIT;
-- Now OUTSIDE the transaction:
-- [send email — no locks held]
```

> **Rule:** Keep transactions as **short as possible**. Every second a transaction is open, it holds locks that block other users.

---

# ⚠️ Common Mistake 3: DDL Inside Transactions

```sql
-- ❌ PROBLEM: DDL statements cause implicit COMMIT in MySQL
START TRANSACTION;
UPDATE accounts SET balance = 9999 WHERE account_id = 'CHK-001';

-- DDL statement: causes an automatic COMMIT!
ALTER TABLE accounts ADD COLUMN phone VARCHAR(20);
-- ↑ This committed the UPDATE above — even without an explicit COMMIT!

ROLLBACK;  -- ← Too late! The UPDATE is already committed.

-- ✅ RULE: Never mix DDL (CREATE, ALTER, DROP) with DML (INSERT, UPDATE, DELETE)
--          in the same transaction in MySQL.
```

**Statements that cause implicit COMMIT in MySQL:**

```
CREATE TABLE    DROP TABLE     ALTER TABLE
CREATE INDEX    DROP INDEX     TRUNCATE TABLE
CREATE DATABASE DROP DATABASE  RENAME TABLE
```

---

# ⚠️ Common Mistake 4: Ignoring Deadlocks

A **deadlock** happens when two transactions each wait for the other to release a lock.

```
Session A                       Session B
────────────────────────────    ────────────────────────────
START TRANSACTION;              START TRANSACTION;
UPDATE accounts                 UPDATE accounts
  SET balance = balance - 100     SET balance = balance - 50
  WHERE account_id = 'CHK-001';   WHERE account_id = 'CHK-002';
-- Locks CHK-001                -- Locks CHK-002

UPDATE accounts                 UPDATE accounts
  SET balance = balance + 100     SET balance = balance + 50
  WHERE account_id = 'CHK-002';   WHERE account_id = 'CHK-001';
-- Needs CHK-002 → WAITING     -- Needs CHK-001 → WAITING
```

**MySQL detects this and kills one transaction automatically:**

```sql
-- MySQL error: ERROR 1213 (40001): Deadlock found when trying to get lock;
-- try restarting transaction

-- ✅ Solution: Always access tables/rows in the SAME ORDER in all transactions
-- If A always updates CHK-001 then CHK-002, and B does the same order → no deadlock
```

---

# ✅ Best Practices Checklist

```sql
-- ✅ 1. Always use explicit transactions for multi-step operations
START TRANSACTION;
  -- ... your changes ...
COMMIT;

-- ✅ 2. Check data BEFORE modifying (use SELECT ... FOR UPDATE)
SELECT balance FROM accounts WHERE account_id = 'CHK-001' FOR UPDATE;
-- verify the value, THEN update

-- ✅ 3. Use savepoints for complex multi-step workflows
SAVEPOINT before_risky_step;
-- ... attempt risky operation ...
-- If fails: ROLLBACK TO SAVEPOINT before_risky_step;
-- If succeeds: continue normally

-- ✅ 4. Keep transactions SHORT — commit as soon as possible

-- ✅ 5. Never mix DDL with DML in the same transaction

-- ✅ 6. Always access tables in the same order to avoid deadlocks

-- ✅ 7. Use ROLLBACK in error handling (application code)
-- Example in Python:
--   try:
--       cursor.execute("START TRANSACTION")
--       cursor.execute("UPDATE ...")
--       cursor.execute("UPDATE ...")
--       cursor.execute("COMMIT")
--   except Exception:
--       cursor.execute("ROLLBACK")
```

---

# 🔍 Useful Diagnostic Commands

```sql
-- ── Check your current isolation level ───────────────────────────────
SELECT @@transaction_isolation;

-- ── Check if autocommit is on ─────────────────────────────────────────
SHOW VARIABLES LIKE 'autocommit';

-- ── See what transactions are currently running ───────────────────────
SELECT * FROM information_schema.INNODB_TRX;

-- ── See what locks are being held ────────────────────────────────────
SELECT * FROM performance_schema.data_locks;

-- ── See processes currently running (and waiting) ────────────────────
SHOW PROCESSLIST;

-- ── Check the InnoDB status (includes recent deadlock info) ───────────
SHOW ENGINE INNODB STATUS;

-- ── See the last auto-increment value inserted ───────────────────────
SELECT LAST_INSERT_ID();
```

> **Tip for debugging:** If your application seems "stuck" or a query is running forever, check `SHOW PROCESSLIST` first. It often reveals a transaction holding a lock that another query is waiting for.

---

# 📋 Quick Reference — Transaction Cheat Sheet

| Command | What it does |
|---|---|
| `START TRANSACTION` | Opens a new transaction (pauses autocommit) |
| `BEGIN` | Same as `START TRANSACTION` |
| `COMMIT` | Saves all changes permanently |
| `ROLLBACK` | Discards all changes since `START TRANSACTION` |
| `SAVEPOINT name` | Creates a named checkpoint inside a transaction |
| `ROLLBACK TO SAVEPOINT name` | Undoes back to the checkpoint |
| `RELEASE SAVEPOINT name` | Removes a savepoint (frees memory) |
| `SET autocommit = 0` | Disables autocommit for the session |
| `SELECT ... FOR UPDATE` | Reads and locks rows for update |
| `SELECT ... LOCK IN SHARE MODE` | Reads and locks rows for shared reading |

<br>

**Isolation Level Quick Pick:**

| Situation | Recommended Level |
|---|---|
| Financial / banking | `SERIALIZABLE` or `REPEATABLE READ` + `FOR UPDATE` |
| General web app | `READ COMMITTED` (good balance) |
| Analytics / reporting | `READ COMMITTED` or `READ UNCOMMITTED` |
| Strict consistency required | `SERIALIZABLE` |

---

# 🎓 Complete Transaction Template

Use this as your **starting template** for any multi-step database operation:

```sql
-- ══════════════════════════════════════════════════════════════
--  TRANSACTION TEMPLATE — Copy and adapt for your use case
-- ══════════════════════════════════════════════════════════════

START TRANSACTION;

    -- ── Step 1: Read + lock any rows you will modify ─────────────
    SELECT column FROM table WHERE condition FOR UPDATE;

    -- ── Step 2: Validate the data (check constraints yourself) ───
    -- If invalid: ROLLBACK; (and exit)

    -- ── Step 3: Make your changes ────────────────────────────────
    UPDATE table SET column = new_value WHERE condition;
    INSERT INTO other_table (...) VALUES (...);
    -- etc.

    -- ── (Optional) Savepoint before a risky step ─────────────────
    SAVEPOINT before_risky;
    -- ... attempt risky operation ...
    -- If fails: ROLLBACK TO SAVEPOINT before_risky;

    -- ── Step 4: Log the action ────────────────────────────────────
    INSERT INTO audit_log (action) VALUES ('description of what happened');

COMMIT;   -- ← Save everything permanently
-- ══════════════════════════════════════════════════════════════
```

---

# 🧪 Practice Exercises

Try these on your own using the `txn_demo` database:

**Exercise 1 — Basic Transfer**
> Transfer $150 from Bob's Checking (`CHK-002`) to Carol's Checking (`CHK-003`). Log the transfer in `audit_log`. Verify both balances changed correctly.

**Exercise 2 — Failed Transfer**
> Attempt to transfer $10,000 from Alice's Checking (`CHK-001`) — more than she has. Use a transaction to ensure the database remains unchanged. Verify the balance is still the original amount.

**Exercise 3 — Savepoint Practice**
> Start a transaction that:
> 1. Places an order for 5 Wireless Mice → `SAVEPOINT`
> 2. Reduces inventory by 5 → `SAVEPOINT`
> 3. Charges the account — but then **simulate a payment failure**
> 4. Roll back to the second savepoint (keep inventory and order)
> 5. Commit the partial result

**Exercise 4 — Deadlock Simulation**
> In two separate MySQL sessions, create a deadlock scenario with the accounts table. Observe MySQL's error message and identify which transaction was killed.

**Exercise 5 — Isolation Level Exploration**
> Set Session A to `READ UNCOMMITTED`. In Session B, start a transaction and update a balance but DON'T commit. In Session A, read that balance — what do you see? Now commit in Session B and read again. Explain what you observed.

---

<!-- _class: divider -->

# 🎉 You Now Know Database Transactions!

---

# 🏁 Summary — What You Learned Today

<div class="cols">
<div class="col">

**The Problem**
- Partial updates are dangerous
- Multi-step operations must be atomic

**ACID Properties**
- **A**tomicity — all or nothing
- **C**onsistency — valid states only
- **I**solation — concurrent safety
- **D**urability — survives crashes

**MySQL Commands**
- `START TRANSACTION` — open
- `COMMIT` — save permanently
- `ROLLBACK` — discard all
- `SAVEPOINT` — checkpoint inside

</div>
<div class="col">

**Key Patterns**
- Always use `FOR UPDATE` when read → write
- Keep transactions SHORT
- Never mix DDL with DML
- Access tables in consistent order

**Isolation Levels**
- READ UNCOMMITTED — fastest, least safe
- READ COMMITTED — good default for apps
- REPEATABLE READ — MySQL's default
- SERIALIZABLE — strictest, slowest

**Diagnostic Tools**
- `SHOW PROCESSLIST`
- `INFORMATION_SCHEMA.INNODB_TRX`
- `SHOW ENGINE INNODB STATUS`

</div>
</div>

<br>

> **Golden Rule:** Every multi-step database operation should be wrapped in a transaction. No exceptions.

---

# 📚 Further Reading

| Topic | Where to Learn |
|---|---|
| MySQL Transaction Documentation | `dev.mysql.com/doc/refman/8.0/en/commit.html` |
| InnoDB Locking | `dev.mysql.com/doc/refman/8.0/en/innodb-locking.html` |
| Isolation Levels Deep Dive | `dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html` |
| Deadlock Detection | `dev.mysql.com/doc/refman/8.0/en/innodb-deadlock-detection.html` |
| Designing for Concurrency | *"Database Internals"* by Alex Petrov |
| ACID in Depth | *"Designing Data-Intensive Applications"* by Martin Kleppmann |

<br>

**Next topics to explore after this tutorial:**
- **Stored Procedures** with transaction logic
- **Two-Phase Commit** (distributed transactions)
- **Optimistic vs Pessimistic locking** strategies
- **Connection pooling** and transaction management in applications
- **MySQL 8.0 Atomic DDL** — DDL that participates in transactions

---

<!-- _class: title -->

# Thank You! 🎓

### Database Transactions — From Zero to Confident

<br>

*You can now write safe, reliable MySQL code that handles*
*real-world concurrent access and failure scenarios.*

<br>

**Remember the Golden Rule:**
> *"Every multi-step operation belongs in a transaction."*
