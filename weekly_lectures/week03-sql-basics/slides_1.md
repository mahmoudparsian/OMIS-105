---
title: OMIS 105 - Week 3 (Flagship Expanded)
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
## Week 3: SQL Core (SELECT, WHERE, ORDER BY)

---

# Agenda

- SELECT basics
- Filtering with WHERE
- Sorting with ORDER BY
- Multiple conditions
- Thinking in questions
- Hands-on practice

---

# Recap

- Tables store data
- Keys connect data

👉 Today: How to **ask questions with SQL**

---

# SQL Mindset (Important)

SQL is NOT programming.

👉 SQL = asking questions to data

---

# Example Table: sales

| id | product | price | quantity |
|----|--------|------|----------|
| 1  | Laptop | 1000 | 1        |
| 2  | Phone  | 800  | 2        |
| 3  | Tablet | 500  | 3        |

---

# SELECT (Basic)

Retrieve all data:

```sql
SELECT * FROM sales;
```

---

# SELECT Specific Columns

```sql
SELECT product, price FROM sales;
```

👉 Only what you need

---

# WHERE (Filtering)

```sql
SELECT * FROM sales
WHERE price > 700;
```

👉 Only rows that match condition

---

# Comparison Operators

- = (equal)
- > (greater than)
- < (less than)
- >=, <=

---

# Example Conditions

```sql
WHERE price = 1000
WHERE quantity >= 2
```

---

# Text Conditions

```sql
SELECT * FROM sales
WHERE product = 'Laptop';
```

⚠️ Text needs quotes

---

# Multiple Conditions (AND)

```sql
SELECT * FROM sales
WHERE price > 700 AND quantity >= 2;
```

👉 BOTH must be true

---

# OR Condition

```sql
SELECT * FROM sales
WHERE product = 'Laptop' OR product = 'Phone';
```

👉 Either condition

---

# ORDER BY (Sorting)

```sql
SELECT * FROM sales
ORDER BY price ASC;
```

---

# DESC (Descending)

```sql
SELECT * FROM sales
ORDER BY price DESC;
```

👉 Highest first

---

# Real Question

👉 “What is the most expensive product?”

```sql
SELECT * FROM sales
ORDER BY price DESC
LIMIT 1;
```

---

# LIMIT (Top N)

```sql
SELECT * FROM sales
ORDER BY price DESC
LIMIT 3;
```

👉 Top 3 results

---

# Computed Columns

```sql
SELECT product, price * quantity AS revenue
FROM sales;
```

👉 SQL can calculate

---

# Business Questions

- Which products are expensive?
- Which products sell more?
- What is total revenue per row?

---

# In-Class Exercise

Ask students:

👉 “Find products with price > 700”

👉 “Find top 2 expensive products”

---

# Common Mistakes

- Forgetting quotes for text
- Using = instead of >
- Not understanding AND vs OR

---

# Mental Model

SELECT → what to show  
WHERE → which rows  
ORDER BY → how to sort  

---

# Hands-On Lab

- SELECT all
- SELECT columns
- WHERE conditions
- ORDER BY
- Combine everything

---

# Summary

- SQL = asking questions
- WHERE filters data
- ORDER BY sorts data
- LIMIT gives top results

---

# What’s Next?

Week 4:
- Aggregation (SUM, COUNT)
- GROUP BY
- HAVING

---

# Final Thought

The more questions you ask, the better you get.

👉 Practice = mastery

---

# Let’s Practice 🚀
