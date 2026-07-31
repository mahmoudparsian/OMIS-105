---
title: OMIS 105 - Week 1 (Flagship Expanded)
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
## Database Management Systems  
### Week 1: Foundations

---

# Agenda (Today)

- Why databases matter
- What is data?
- File systems vs DBMS
- Relational thinking (preview)
- First SQL queries
- Hands-on practice

---

# Why Should You Care?

Think about apps you use daily:

- Banking apps
- Amazon
- Netflix
- Uber

👉 All powered by databases

---

# Real-World Example

Imagine Amazon without a database:

- Orders lost ❌
- Prices inconsistent ❌
- Inventory incorrect ❌

👉 Databases prevent chaos

---

# What is Data?

Data = raw facts

Examples:
- Name: "Alice"
- Price: 1000
- Date: 2026-01-01

---

# From Data to Information

Data → processed → Information

Example:
- Raw: transactions
- Insight: “Top-selling product”

---

# What is a Database?

A structured collection of data

Key properties:
- Organized
- Persistent
- Queryable

---

# File System vs Database

## File System (Excel / CSV)
- No relationships
- Hard to maintain
- Data duplication

## Database
- Structured
- Connected data
- Efficient queries

---

# Problem: Data Duplication

| customer | order |
|----------|------|
| Alice    | Laptop |
| Alice    | Phone |

👉 What if name changes?

---

# Solution: Database Design

Separate tables:

Customers  
Orders  

👉 One change → consistent everywhere

---

# What is a DBMS?

Database Management System

Responsibilities:
- Store data
- Retrieve data
- Ensure consistency
- Handle multiple users

---

# Examples of DBMS

- MySQL
- PostgreSQL
- DuckDB

---

# Roles in Database World

- Developer → builds apps
- Analyst → queries data
- DBA → manages database

---

# Relational Model (Preview)

Data stored in tables:

| id | name | price |
|----|------|-------|

---

# Key Terms

- Table
- Row (record)
- Column (attribute)

---

# What is SQL?

Structured Query Language

Used to:
- Query data
- Insert data
- Update data

---

# First SQL Query

```sql
SELECT 1;
```

👉 SQL can act like a calculator

---

# Create a Table

```sql
CREATE TABLE products (
    id INTEGER,
    name VARCHAR,
    price INTEGER
);
```

---

# Insert Data

```sql
INSERT INTO products VALUES
(1, 'Laptop', 1000),
(2, 'Phone', 800),
(3, 'Tablet', 500);
```

---

# Query Data

```sql
SELECT * FROM products;
```

---

# Filter Data

```sql
SELECT * FROM products
WHERE price > 700;
```

---

# Compute Values

```sql
SELECT name, price * 0.9 AS discounted_price
FROM products;
```

---

# Think Like This

Instead of:

❌ “Write SQL”

Think:

✅ “What question do I want to answer?”

---

# Example Questions

- Which products are expensive?
- Which products are cheap?
- What is the average price?

---

# In-Class Exercise

Ask students:

👉 “Find all products above $800”

---

# Common Beginner Mistakes

- Forgetting quotes
- Confusing columns vs rows
- Thinking SQL = programming

---

# Mental Model

SQL = Asking questions  
Database = Organized memory

---

# Hands-On Lab (Today)

- Run SELECT 1
- Create a table
- Insert data
- Query data
- Filter results

---

# Summary

- Databases are everywhere
- SQL is essential
- Tables are simple structures
- You can already query data 🎉

---

# What’s Next?

Week 2:
- Relationships
- Keys
- Data modeling

---

# Final Thought

You are not learning syntax.

👉 You are learning how to think with data.

---

# Let’s Practice 🚀
