---
title: OMIS 105 - Week 7 (Indexing & Query Performance)
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
## Week 7: Indexing & Query Performance

---

# Agenda

- Why performance matters
- How a database finds rows
- What is an index?
- When to use indexes (and when not to)
- Trade-offs
- How DuckDB is different
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
- Queries can become slow ❌  
- Many users wait at the same time ❌  

👉 Performance becomes critical

---

# What Happens Behind the Scenes?

When you run:

```sql
SELECT * FROM orders WHERE customer_id = 42;
```

Without help, the database must:
👉 Read **every** row and check the condition

This is called a:

👉 **Full table scan** (or *sequential scan*)

---

# Full Table Scan

| order_id | customer_id | amount |
|----|-----|-------|
| 1  | 17  | 120.00 |
| 2  | 42  | 75.50  |
| 3  | 8   | 300.00 |
| ...| ... | ...   |

👉 The database checks the rows **one by one**

1,000 rows: instant. 1 billion rows: much slower.

---

# What is an Index?

An **index** is an extra data structure that helps the database
**find rows quickly**, without reading the whole table.

Analogy:
📖 The index at the back of a book → go straight to the right page

---

# With an Index

Instead of scanning every row:

👉 The database looks up the value in the index  
👉 The index points to the matching rows  
👉 Only those rows are read

---

# Create an Index

```sql
CREATE INDEX idx_orders_customer
ON orders(customer_id);
```

- `idx_orders_customer` is the index **name** (your choice)
- `orders(customer_id)` = the table and the column to index

A `PRIMARY KEY` or `UNIQUE` column gets an index **automatically**.

---

# Query with an Index

```sql
SELECT * FROM orders
WHERE customer_id = 42;
```

The query does **not** change.  
The database decides **by itself** whether to use the index.

👉 Can be much faster on large tables

---

# When to Use an Index

- Columns you **search** by often (`WHERE customer_id = ...`)
- Searches that return **few rows** (one customer, one email)
- Columns used to **JOIN** tables (in row-based databases)

---

# When NOT to Use an Index

- Very small tables (a scan is already fast)
- Tables with very frequent inserts and updates
- Columns with few different values (e.g., `status` with 4 values,
  or TRUE/FALSE) — each value matches too many rows

---

# Trade-Offs

Indexes are NOT free:

| Benefit | Cost |
|--------|------|
| Faster lookups (`WHERE`) | Slower `INSERT`, `UPDATE`, `DELETE` |
| Faster searches for a few rows | More storage / memory |

Every time a row changes, **every index** on that table must be updated too.

---

# Important Insight

👉 An index = faster **reading**  
👉 But a cost for **writing**  

---

# Real-World Thinking

Ask:

👉 “Will this query run **often**?”

👉 “Is this table **large**?”

👉 “Does the query return **few** rows?”

Three "yes" answers → an index is worth trying.

---

# Example Scenario

An online store:

- millions of orders  
- the website shows *"My Orders"* for one customer, thousands of times per minute  

👉 An index on `orders(customer_id)` = huge win

---

# How DuckDB Is Different

DuckDB is built for **analytics** (summarizing many rows), not for
looking up one row at a time. It is fast **without** indexes because it:

- stores data **by column** — reads only the columns you ask for
- keeps the **min/max** of each block of rows, and skips blocks that cannot match
- uses **all** CPU cores at once

DuckDB uses an index only when a filter matches **very few rows**
(for example, `WHERE customer_id = 42`). For most queries, it scans.

---

# Try It: An Index in DuckDB

```sql
-- A table with 10 million rows
CREATE OR REPLACE TABLE big_orders AS
SELECT range AS order_id,
       (random() * 100000)::INTEGER AS customer_id,
       round(random() * 1000, 2) AS amount
FROM range(10000000);

.timer on
SELECT COUNT(*) FROM big_orders WHERE customer_id = 4242;   -- no index
CREATE INDEX idx_big_cust ON big_orders(customer_id);       -- build index
SELECT COUNT(*) FROM big_orders WHERE customer_id = 4242;   -- with index
```

On a laptop: about **2 ms** without the index, about **1 ms** with it,
and about **1 second** to build the index.

(`.timer on` works in the DuckDB command-line tool, not inside a notebook.)

---

# Why You Won't See a Big Difference in Class

In class:
- small datasets (our `orders` table has 200 rows)  
- DuckDB scans very quickly

👉 The index effect is almost invisible

In large row-based systems (PostgreSQL, MySQL, Oracle) that serve many users:
👉 Indexes can turn seconds into milliseconds

---

# Advanced Idea (Light)

Indexes are stored as **trees**, so a lookup takes a few steps
instead of reading every row.

- Most databases (PostgreSQL, MySQL, Oracle): **B-tree** indexes
- DuckDB: **ART** (Adaptive Radix Tree) indexes

👉 Not needed in depth — just awareness

---

# In-Class Exercise

Which column would you index? Why?

- *"Show all orders for customer 42"* → `customer_id`?
- *"Show all orders with status 'completed'"* → `status`?
- *"Find the customer with this email"* → `email`?

Hint: think about how many rows each search returns.

---

# Common Mistakes

- Indexing every column ❌ (slows every write)  
- Indexing columns with only a few values ❌  
- Expecting a big speed-up on small data ❌  
- Expecting the index to help every query ❌  

---

# Mental Model

Without an index:
👉 read everything, keep what matches  

With an index:
👉 look up the value, jump to the matching rows  

---

# Hands-On Lab Idea

- Create a large table (like `big_orders`)
- Time a query that looks up one customer
- Add an index
- Time the query again — and time how long the index took to build

Discuss: was it worth it?

---

# Summary

- Performance matters at scale  
- An index speeds up searches that return **few** rows  
- Indexes cost time on writes and extra space  
- DuckDB is fast even without indexes (columnar storage)  
- Think before indexing  

---

# What’s Next?

Week 8:
- Transactions (`BEGIN`, `COMMIT`, `ROLLBACK`)
- ACID properties
- Constraints (`CHECK`, `NOT NULL`)

---

# Final Thought

Correct SQL is not enough.

👉 Efficient SQL matters.

---

# Let’s Optimize 🚀

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
