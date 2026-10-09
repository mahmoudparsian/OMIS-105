---
title: OMIS 105 - Week 3 (SELECT, WHERE, ORDER BY)
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
## Week 3: SQL Core (SELECT, WHERE, ORDER BY)

---

# Agenda

- SELECT basics
- Filtering with WHERE
- Sorting with ORDER BY
- Multiple conditions (AND, OR)
- LIMIT and computed columns
- Thinking in questions
- Hands-on practice

---

# Recap

- Tables store data
- Keys connect data

👉 Today: How to **ask questions with SQL**

---

# SQL Mindset (Important)

SQL is a **declarative** language.

You describe **what** you want.
The database decides **how** to get it.

👉 SQL = asking questions of your data

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

👉 Ask only for the columns you need

---

# WHERE (Filtering)

```sql
SELECT * FROM sales
WHERE price > 700;
```

👉 Keeps only the rows that match the condition

---

# Comparison Operators

| Operator | Meaning |
| :--- | :--- |
| `=` | equal to |
| `<>` or `!=` | not equal to |
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal to |
| `<=` | less than or equal to |

---

# Example Conditions

```sql
SELECT * FROM sales WHERE price = 1000;     -- Laptop
SELECT * FROM sales WHERE quantity >= 2;    -- Phone, Tablet
SELECT * FROM sales WHERE product <> 'Phone'; -- Laptop, Tablet
```

---

# Text Conditions

```sql
SELECT * FROM sales
WHERE product = 'Laptop';
```

⚠️ Text values need **single** quotes: `'Laptop'`
(numbers do not)

---

# Multiple Conditions (AND)

```sql
SELECT * FROM sales
WHERE price > 700 AND quantity >= 2;
```

👉 BOTH conditions must be true (result: Phone)

---

# OR Condition

```sql
SELECT * FROM sales
WHERE product = 'Laptop' OR product = 'Phone';
```

👉 At least ONE condition must be true (result: Laptop, Phone)

Shorter form: `WHERE product IN ('Laptop', 'Phone')`

---

# ORDER BY (Sorting)

```sql
SELECT * FROM sales
ORDER BY price ASC;
```

👉 Lowest first. `ASC` (ascending) is the default, so it can be left out.

---

# DESC (Descending)

```sql
SELECT * FROM sales
ORDER BY price DESC;
```

👉 Highest first

---

# Real Question

👉 “Which product has the highest price?”

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

👉 The top 3 rows

⚠️ Without `ORDER BY`, `LIMIT` returns *any* 3 rows.
The order is not guaranteed.

---

# Computed Columns

```sql
SELECT product, price * quantity AS revenue
FROM sales;
```

👉 SQL can calculate new values. `AS` gives the new column a name.

| product | revenue |
|---|---|
| Laptop | 1000 |
| Phone | 1600 |
| Tablet | 1500 |

---

# Business Questions

- Which products are expensive? → `WHERE`
- Which products sell the most units? → `ORDER BY quantity DESC`
- What is the revenue for each row? → `price * quantity`

---

# In-Class Exercise

Write a query for each question:

👉 “Find products with a price greater than 700.”

👉 “Find the 2 most expensive products.”

👉 “Find the product with the highest revenue.”

---

# Common Mistakes

- Forgetting quotes around text: `WHERE product = Laptop` ❌
- Using double quotes for text: `"Laptop"` means a *column name* ❌
- Mixing up `AND` and `OR`
- Using `LIMIT` without `ORDER BY`

---

# Mental Model

SELECT → which columns to show  
FROM → which table  
WHERE → which rows to keep  
ORDER BY → how to sort  
LIMIT → how many rows to return  

---

# Hands-On Lab

- SELECT all
- SELECT columns
- WHERE conditions
- ORDER BY
- Combine everything

---

# Summary

- SQL = asking questions of data
- SELECT chooses columns
- WHERE filters rows
- ORDER BY sorts data
- LIMIT gives top results

---

# What’s Next?

Next lecture (`slides_02`):
- String, math, and date functions
- CASE expressions
- GROUP BY and HAVING

---

# Final Thought

The more questions you ask, the better you get.

👉 Practice leads to mastery

---

# Let’s Practice 🚀

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
