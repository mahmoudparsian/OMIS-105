---
title: OMIS 105 - Week 8 (Flagship Expanded)
author: Instructor
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
- ACID properties (intuitive)
- Failure scenarios
- Concurrency basics (light)
- SQL commands (BEGIN/COMMIT/ROLLBACK)
- Hands-on thinking

---

# Recap

- Week 7: Performance & indexing  
👉 Today: Make data **correct and reliable**

---

# What is a Transaction?

A transaction is:

👉 A group of operations executed as a unit

Either:
- All succeed ✅  
- Or none happen ❌  

---

# Real Example (Bank Transfer)

Transfer $100 from A → B:

1. Deduct from A  
2. Add to B  

👉 Both must happen together

---

# Problem Without Transactions

If system crashes:

- Money deducted ❌  
- Money not added ❌  

👉 Data becomes inconsistent

---

# ACID Properties

Transactions guarantee:

- A → Atomicity  
- C → Consistency  
- I → Isolation  
- D → Durability  

---

# Atomicity (All or Nothing)

👉 Either everything happens or nothing

Example:
- Deduct + Add must both complete

---

# Consistency (Valid State)

Before and after transaction:

👉 Data follows rules

Example:
- No negative balance (if rule exists)

---

# Isolation (No Interference)

Multiple users:

👉 Transactions don’t interfere

Example:
- Two users updating same account

---

# Durability (Permanent)

After COMMIT:

👉 Data is saved permanently

Even if:
- crash occurs  
- power failure  

---

# SQL Commands

```sql
BEGIN;
COMMIT;
ROLLBACK;
```

---

# Transaction Example

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1;

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;

COMMIT;
```

---

# What if Something Fails?

If error occurs:

```sql
ROLLBACK;
```

👉 Undo everything

---

# Failure Scenario (Important)

Ask:

👉 “What if crash happens after first UPDATE?”

Without transaction:
- inconsistent data ❌  

With transaction:
- rollback restores state ✅  

---

# Concurrency (Light Intro)

Many users at same time:

Problems:
- Dirty reads  
- Lost updates  

👉 Transactions help control this

---

# Isolation Levels (Concept Only)

- Read Uncommitted  
- Read Committed  
- Repeatable Read  

👉 Just awareness (no deep dive)

---

# Real-World Thinking

Ask:

👉 “What must NEVER go wrong?”

Examples:
- money transfers  
- orders  
- inventory  

---

# In-Class Exercise

Ask:

👉 “Design a safe transaction for:
placing an order”

Steps:
- reduce inventory  
- create order  
- confirm payment  

---

# Common Mistakes

- Forgetting COMMIT ❌  
- Ignoring failures ❌  
- Thinking queries always succeed ❌  

---

# Mental Model

Transaction = safety layer  
ACID = guarantees  

👉 Database = reliable system

---

# Hands-On Lab Idea

- Create accounts table  
- Simulate transfer  
- Add failure scenario  
- Use ROLLBACK  

---

# Summary

- Transactions ensure correctness  
- ACID guarantees reliability  
- BEGIN/COMMIT/ROLLBACK control execution  

👉 Databases protect data integrity

---

# What’s Next?

Week 9:
- Project (integration of all concepts)

---

# Final Thought

Fast systems are good.  
Correct systems are essential.

👉 Reliability is everything.

---

# Let’s Build Safe Systems 🚀
