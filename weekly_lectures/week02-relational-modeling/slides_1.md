---
title: OMIS 105 - Week 2 (Flagship Expanded)
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
## Week 2: Relational Modeling & Data Thinking

---

# Agenda

- Recap Week 1
- Tables, rows, columns
- Primary keys & foreign keys
- Relationships
- ER thinking
- Hands-on examples

---

# Recap (Quick)

- Database = organized data
- SQL = asking questions

👉 Today: HOW data is structured

---

# Why Structure Matters

Bad structure:
- Duplicate data
- Errors
- Hard queries

Good structure:
- Clean
- Flexible
- Scalable

---

# Table Basics

| id | name | age |
|----|------|-----|

- Row = one record
- Column = attribute

---

# Example: Students Table

| id | name  | major |
|----|-------|-------|
| 1  | Alice | CS    |
| 2  | Bob   | MIS   |

---

# Primary Key

- Uniquely identifies a row
- No duplicates
- Cannot be NULL

Example:
👉 student_id

---

# Why Primary Key?

Without it:
- Duplicate rows
- No reliable identification

---

# Foreign Key

- Connects tables
- References another table

Example:
orders.customer_id → customers.id

---

# Example: Customers + Orders

Customers:

| id | name |
|----|------|
| 1  | Alice |

Orders:

| id | customer_id | amount |
|----|-------------|--------|
| 1  | 1           | 1000   |

---

# Relationships

## One-to-Many (1 → many)
Customer → Orders

## Many-to-Many
Students ↔ Courses

---

# Visual Thinking (Important)

Draw on board:

Customers → Orders

👉 Helps students *see* the relationship

---

# Bad Design Example

| order_id | customer_name | product |
|----------|--------------|---------|
| 1        | Alice        | Laptop  |
| 2        | Alice        | Phone   |

Problems:
- Duplicate data
- Hard updates

---

# Good Design

Customers table  
Orders table  

👉 Link via customer_id

---

# Thinking Shift

From:
❌ “store everything in one table”

To:
✅ “split data logically”

---

# ER Diagram (Concept)

- Entities = tables
- Relationships = connections

Example:
Customer — places → Order

---

# Simple ER Example

Customer (id, name)  
Order (id, customer_id)

---

# SQL Preview (JOIN)

```sql
SELECT c.name, o.amount
FROM customers c
JOIN orders o
ON c.id = o.customer_id;
```

👉 This is WHY relationships matter

---

# In-Class Exercise

Ask:

👉 “How would you store:
students + courses?”

Guide to:
- students table
- courses table
- enrollment table

---

# Common Mistakes

- No primary key
- Using names instead of IDs
- One big table design

---

# Mental Model

Tables = entities  
Keys = connections  

👉 Database = connected system

---

# Hands-On Lab

- Create 2 tables
- Add primary keys
- Add foreign key
- Try simple JOIN

---

# Summary

- Structure matters more than syntax
- Keys define relationships
- Good design prevents problems

---

# What’s Next?

Week 3:
- SQL querying in depth

---

# Final Thought

Good databases are designed, not just written.

👉 Think before you build.

---

# Let’s Practice 🚀
