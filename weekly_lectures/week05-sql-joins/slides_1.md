---
title: OMIS 105 - Week 5 (Flagship Expanded)
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
## Week 5: JOIN Deep Dive (Relational Power)

---

# Agenda

- Why JOIN exists
- INNER JOIN
- LEFT JOIN
- Multi-table JOINs
- NULL understanding
- Business queries
- Hands-on practice

---

# Recap

- Week 4: GROUP BY → insights  
👉 Today: Combine multiple tables

---

# Why JOIN?

Real data is split:

- customers
- orders
- products

👉 Need JOIN to connect

---

# Example Tables

Customers:

| id | name |
|----|------|
| 1  | Alice |
| 2  | Bob |

Orders:

| id | customer_id | amount |
|----|-------------|--------|
| 1  | 1           | 1000   |
| 2  | 1           | 800    |

---

# INNER JOIN

Only matching rows

```sql
SELECT c.name, o.amount
FROM customers c
JOIN orders o
ON c.id = o.customer_id;
```

---

# INNER JOIN Result

| name  | amount |
|-------|--------|
| Alice | 1000   |
| Alice | 800    |

👉 Bob disappears (no match)

---

# LEFT JOIN

Keep ALL rows from left table

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

👉 Bob appears with NULL

---

# What is NULL?

- Missing value
- Unknown

👉 Very important in JOINs

---

# JOIN Mental Model

INNER JOIN → intersection  
LEFT JOIN → keep left side  

---

# Multiple JOINs

Example:

customers → orders → products

```sql
SELECT c.name, p.product_name
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN products p ON o.product_id = p.id;
```

---

# Business Question

👉 “What did each customer buy?”

---

# Aggregation + JOIN

```sql
SELECT c.name, SUM(o.amount) AS total
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;
```

👉 Total spending per customer

---

# Top Customer

```sql
SELECT c.name, SUM(o.amount) AS total
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.name
ORDER BY total DESC
LIMIT 1;
```

---

# Common Mistakes

- Missing ON condition ❌  
- Wrong join key ❌  
- Confusing LEFT vs INNER ❌  
- Ignoring NULL values ❌  

---

# In-Class Exercise

Ask:

👉 “Show all customers (even without orders)”

👉 “Find total spending per customer”

---

# Visual Teaching Tip

Draw tables:

Customers → Orders  

Draw arrows → helps understanding

---

# Mental Model

Tables = nodes  
JOIN = connection  

👉 Database = network of tables

---

# Hands-On Lab

- INNER JOIN
- LEFT JOIN
- Multiple JOIN
- JOIN + GROUP BY
- Top-N query

---

# Summary

- JOIN connects data
- INNER JOIN = matching rows
- LEFT JOIN = keep all left rows
- JOIN + GROUP BY = powerful analytics

---

# What’s Next?

Week 6:
- Database design
- Normalization

---

# Final Thought

Without JOIN, databases are just isolated tables.

👉 JOIN gives databases their power.

---

# Let’s Connect Data 🚀
