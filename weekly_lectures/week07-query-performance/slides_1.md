---
title: OMIS 105 - Week 7 (Flagship Expanded)
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
## Week 7: Indexing & Query Performance

---

# Agenda

- Why performance matters
- How databases execute queries
- What is an index?
- When to use indexes
- Trade-offs
- Real-world intuition
- Hands-on ideas

---

# Recap

- Week 6: Design clean databases  
👉 Today: Make queries **fast**

---

# Why Performance Matters

Small data:
- Everything feels fast

Large data (millions of rows):
- Queries become slow ❌  
- Systems can fail ❌  

👉 Performance becomes critical

---

# What Happens Behind the Scenes?

When you run:

```sql
SELECT * FROM sales WHERE price = 800;
```

Database may:
👉 Scan EVERY row

This is called:

👉 Full Table Scan

---

# Full Table Scan (Slow)

| id | price |
|----|-------|
| 1  | 1000  |
| 2  | 800   |
| 3  | 500   |
|... | ...   |

👉 Database checks row by row

---

# What is an Index?

An index is:

👉 A data structure that speeds up lookup

Analogy:
📖 Book index → jump to page directly

---

# With Index (Fast)

Instead of scanning all rows:

👉 Database jumps directly to matching data

---

# Create Index

```sql
CREATE INDEX idx_price
ON sales(price);
```

---

# Query with Index

```sql
SELECT * FROM sales
WHERE price = 800;
```

👉 Much faster on large data

---

# When to Use Index

- Frequently searched columns  
- Columns in WHERE  
- Columns used in JOIN  

---

# When NOT to Use Index

- Very small tables  
- Columns with frequent updates  
- Columns with many duplicate values  

---

# Trade-Offs

Indexes are NOT free:

| Benefit | Cost |
|--------|------|
| Faster SELECT | Slower INSERT |
| Faster WHERE  | More storage |

---

# Important Insight

👉 Index = speed for reading  
👉 But cost for writing  

---

# Real-World Thinking

Ask:

👉 “Will this query run often?”

👉 “Is this table large?”

---

# Example Scenario

E-commerce system:

- millions of orders  
- searching by customer_id  

👉 index on customer_id = huge win

---

# Why Students Don’t See Speed Difference

In class:
- small datasets  

👉 Index effect is invisible

But in real world:
👉 HUGE impact

---

# Advanced Idea (Light)

Database uses:
- trees (B-tree)

👉 Not needed in depth, just awareness

---

# In-Class Exercise

Ask:

👉 “Which column would you index?”

Example:
- search by price?
- search by product?

---

# Common Mistakes

- Index everything ❌  
- Forget index exists ❌  
- Expect instant speed on small data ❌  

---

# Mental Model

Without index:
👉 scan everything  

With index:
👉 jump directly  

---

# Hands-On Lab Idea

- Run query  
- Add index  
- Run query again  

Discuss difference conceptually

---

# Summary

- Performance matters at scale  
- Index = faster queries  
- Trade-offs exist  
- Think before indexing  

---

# What’s Next?

Week 8:
- Transactions
- ACID properties

---

# Final Thought

Correct SQL is not enough.

👉 Efficient SQL matters.

---

# Let’s Optimize 🚀
