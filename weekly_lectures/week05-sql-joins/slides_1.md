---
title: OMIS 105 - Week 5 (JOIN Deep Dive)
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
## Week 5: JOIN Deep Dive (Relational Power)

---

# Agenda

- Why JOIN exists
- INNER JOIN
- LEFT JOIN
- Finding missing data with `IS NULL`
- Replacing `NULL` with `COALESCE`
- Multi-table JOINs
- Business queries
- Hands-on practice

---

# Recap

- Week 4: GROUP BY → insights  
- Week 4: first look at INNER JOIN and LEFT JOIN  

👉 Today: go deeper — combine tables **correctly**, including missing data

---

# Why JOIN?

Real data is split across tables:

- customers
- orders
- products

Each fact is stored **once**, in one table.
Keys (`customer_id`, `product_id`, ...) link the tables.

👉 A JOIN follows those links to bring the data back together

---

# Example Tables

customers:

| id | name |
|----|------|
| 1  | Alice |
| 2  | Bob |

orders:

| id | customer_id | amount |
|----|-------------|--------|
| 1  | 1           | 1000   |
| 2  | 1           | 800    |

Alice has two orders. Bob has none.

---

# Try It: Create the Example Tables

```sql
CREATE OR REPLACE TABLE customers AS
SELECT * FROM (VALUES (1, 'Alice'), (2, 'Bob')) AS t(id, name);

CREATE OR REPLACE TABLE orders AS
SELECT * FROM (VALUES (1, 1, 1000), (2, 1, 800)) AS t(id, customer_id, amount);
```

---

# INNER JOIN

Keeps only rows that have a match in **both** tables

```sql
SELECT c.name, o.amount
FROM customers c
JOIN orders o
  ON c.id = o.customer_id;
```

`JOIN` alone means `INNER JOIN`.

---

# INNER JOIN Result

| name  | amount |
|-------|--------|
| Alice | 1000   |
| Alice | 800    |

👉 Alice appears **twice** (two orders)

👉 Bob disappears (no matching order)

---

# LEFT JOIN

Keeps **all** rows from the left table (the one after `FROM`)

```sql
SELECT c.name, o.amount
FROM customers c
LEFT JOIN orders o
  ON c.id = o.customer_id;
```

---

# LEFT JOIN Result

| name  | amount |
|-------|--------|
| Alice | 1000   |
| Alice | 800    |
| Bob   | NULL   |

👉 Bob appears, with `NULL` in the order columns

---

# What is NULL?

- `NULL` = missing or unknown value
- In a LEFT JOIN, `NULL` means **"no match was found"**
- `NULL` is not 0 and not an empty string `''`
- Test for it with `IS NULL`, never `= NULL`

👉 Very important in JOINs

---

# Finding Missing Data: LEFT JOIN + IS NULL

👉 “Which customers have **never** ordered?”

```sql
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```

| name |
|------|
| Bob  |

Pattern: LEFT JOIN, then keep the rows where the right side is `NULL`.

---

# Replacing NULL: COALESCE

`COALESCE(a, b)` returns `a` if it is not `NULL`, otherwise `b`.

```sql
SELECT c.name,
       COALESCE(SUM(o.amount), 0) AS total
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;
```

| name  | total |
|-------|-------|
| Alice | 1800  |
| Bob   | 0     |

Without `COALESCE`, Bob's total would be `NULL`.

---

# Trap 1: COUNT(*) After a LEFT JOIN

```sql
SELECT c.name,
       COUNT(*)    AS wrong_count,   -- counts rows
       COUNT(o.id) AS order_count    -- counts non-NULL order ids
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;
```

| name  | wrong_count | order_count |
|-------|-------------|-------------|
| Alice | 2           | 2           |
| Bob   | 1           | 0           |

👉 Bob has one row (full of `NULL`s), but **zero** orders.
Count a column from the right table.

---

# Trap 2: WHERE Can Undo a LEFT JOIN

```sql
-- Goal: all customers, with their orders over 900
SELECT c.name, o.amount
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.amount > 900;          -- Bob is gone!
```

Bob's `amount` is `NULL`, and `NULL > 900` is not true, so `WHERE` drops him.

Fix: put the condition in `ON`:

```sql
SELECT c.name, o.amount
FROM customers c
LEFT JOIN orders o
  ON c.id = o.customer_id AND o.amount > 900;   -- Alice 1000, Bob NULL
```

---

# JOIN Mental Model

INNER JOIN → only the matches (the overlap)  
LEFT JOIN → everything on the left, plus matches from the right  

---

# Multiple JOINs

Now use this week's real data (run from the `week05-sql-joins` folder):

```sql
CREATE OR REPLACE TABLE customers   AS SELECT * FROM read_csv('data/customers.csv');
CREATE OR REPLACE TABLE orders      AS SELECT * FROM read_csv('data/orders.csv');
CREATE OR REPLACE TABLE order_items AS SELECT * FROM read_csv('data/order_items.csv');
CREATE OR REPLACE TABLE products    AS SELECT * FROM read_csv('data/products.csv');
CREATE OR REPLACE TABLE reviews     AS SELECT * FROM read_csv('data/reviews.csv');
```

(These replace the small `customers` and `orders` tables from before.)

An order can contain many products, so `order_items` sits between them:

customers → orders → order_items → products

---

# Multiple JOINs: The Query

👉 “What did each customer buy?”

```sql
SELECT c.first_name, c.last_name,
       o.order_id, p.product_name, oi.quantity
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
JOIN products p     ON oi.product_id = p.product_id
ORDER BY o.order_id
LIMIT 10;
```

Each `ON` links a foreign key to the primary key it points to.

---

# Aggregation + JOIN

```sql
SELECT c.customer_id, c.first_name, c.last_name,
       ROUND(SUM(o.total_amount), 2) AS total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name;
```

👉 Total spending per customer

Group by the **key** (`customer_id`), not only the name —
two customers can share a name.

---

# Top Customer

```sql
SELECT c.customer_id, c.first_name, c.last_name,
       ROUND(SUM(o.total_amount), 2) AS total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total DESC
LIMIT 1;
```

Result: Quinn Hall, 4050.10

---

# Real Data: Products With No Reviews

```sql
SELECT p.product_id, p.product_name
FROM products p
LEFT JOIN reviews r ON p.product_id = r.product_id
WHERE r.review_id IS NULL
ORDER BY p.product_id;
```

👉 Returns 8 products that nobody has reviewed yet.

Same pattern as "customers who never ordered":
LEFT JOIN + `IS NULL`.

---

# Common Mistakes

- Missing or wrong `ON` condition ❌ (wrong matches, or far too many rows)
- Joining on the wrong key ❌ (e.g., `o.order_id = c.customer_id`)
- Using INNER JOIN when you need LEFT JOIN ❌ (rows silently disappear)
- `COUNT(*)` after a LEFT JOIN ❌ (counts the `NULL` row)
- Filtering the right table in `WHERE` after a LEFT JOIN ❌

---

# In-Class Exercise

Write a query for each question:

👉 “Show all customers, even those without orders.”

👉 “Find the total spending per customer (show 0 for no orders).”

👉 “Which products have never been reviewed?”

---

# Tip: Draw the Tables

Before writing a JOIN, sketch it:

customers ──(customer_id)──▶ orders ──(order_id)──▶ order_items ──(product_id)──▶ products

Each arrow is one `JOIN ... ON ...`.

---

# Mental Model

Tables = nodes  
JOIN = connection (key = foreign key)  

👉 A database = a network of linked tables

---

# Hands-On Lab

- INNER JOIN
- LEFT JOIN
- LEFT JOIN + IS NULL
- COALESCE
- Multiple JOINs
- JOIN + GROUP BY
- Top-N query

---

# Summary

- JOIN connects data through keys
- INNER JOIN = only matching rows
- LEFT JOIN = all left rows; `NULL` where there is no match
- LEFT JOIN + `IS NULL` = find what is missing
- `COALESCE` replaces `NULL` with a default value
- JOIN + GROUP BY = powerful analytics

---

# What’s Next?

Week 6:
- Database design
- Normalization (1NF, 2NF, 3NF)

---

# Final Thought

Without JOINs, a database is just a set of separate tables.

👉 JOINs give databases their power.

---

# Let’s Connect Data 🚀

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
