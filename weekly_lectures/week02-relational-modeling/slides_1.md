---
title: OMIS 105 - Week 2 (Relational Modeling)
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
## Week 2: Relational Modeling & Data Thinking

---

# Agenda

- Recap of Week 1
- Tables, rows, columns
- Primary keys & foreign keys
- Relationships (one-to-many, many-to-many)
- ER thinking
- Hands-on examples

---

# Recap (Quick)

- Database = organized data
- SQL = asking questions of the data

👉 Today: HOW the data is structured

---

# Why Structure Matters

Bad structure:
- Duplicate data
- Errors and inconsistent values
- Hard-to-write queries

Good structure:
- Clean data
- Flexible (easy to add new data)
- Scalable (works for millions of rows)

---

# Table Basics

| id | name | age |
|----|------|-----|
| 1  | Alice | 21 |

- **Row** = one record (one thing: one student, one order)
- **Column** = one attribute (one fact about each thing)
- **Table** = all the records of one kind

---

# Example: Students Table

| student_id | name  | major |
|----|-------|-------|
| 1  | Alice | CS    |
| 2  | Bob   | MIS   |

Each row is one student. Each column is one fact about a student.

---

# Primary Key

- Uniquely identifies each row
- No duplicates
- Cannot be `NULL` (empty)

Example:
👉 `student_id`

Two students can have the same name — but never the same `student_id`.

---

# Why a Primary Key?

Without it:
- Duplicate rows can appear
- There is no reliable way to point to **one** row
  ("update Alice's major" — which Alice?)

---

# Foreign Key

- A column that **points to** the primary key of another table
- Connects the two tables

Example:
`orders.customer_id` → `customers.id`

Every order must belong to a customer that really exists.

---

# Example: Customers + Orders

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

Alice (id 1) has two orders. Bob has none yet.

---

# Try It: Keys in DuckDB

```sql
CREATE OR REPLACE TABLE customers (
    id   INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE OR REPLACE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),  -- foreign key
    amount      DECIMAL(10, 2)
);

INSERT INTO customers VALUES (1, 'Alice'), (2, 'Bob');
INSERT INTO orders VALUES (1, 1, 1000), (2, 1, 800);
```

(To run it again, drop `orders` first: `DROP TABLE IF EXISTS orders;`)

---

# The Keys Protect the Data

```sql
INSERT INTO customers VALUES (1, 'Carol');
-- Constraint Error: Duplicate key "id: 1" violates primary key constraint.

INSERT INTO orders VALUES (3, 999, 50);
-- Constraint Error: Violates foreign key constraint because key
-- "id: 999" does not exist in the referenced table
```

(The error names the column it looked up: `id` in `customers`.)

👉 The database refuses bad data — you don't have to check it yourself

---

# Relationships

## One-to-Many (1 → many)
One customer → many orders  
(each order belongs to **one** customer)

## Many-to-Many
Students ↔ Courses  
(a student takes many courses; a course has many students)

## One-to-One (less common)
One customer → one loyalty profile

---

# Many-to-Many Needs a Third Table

You cannot store "which students take which courses" in either table alone.

Add a **junction table**:

| student_id | course_id |
|------------|-----------|
| 1          | OMIS105   |
| 1          | OMIS30    |
| 2          | OMIS105   |

Each row = one enrollment. Two one-to-many relationships replace one many-to-many.

---

# Visual Thinking (Important)

Draw it:

Customers ──< Orders

The line connects the tables; the fork (`<`) marks the "many" side.

👉 A quick sketch helps you *see* the relationship

---

# Bad Design Example

| order_id | customer_name | product |
|----------|--------------|---------|
| 1        | Alice        | Laptop  |
| 2        | Alice        | Phone   |

Problems:
- Duplicate data (Alice stored twice)
- Hard updates (rename Alice → change many rows)
- Lost data (delete Alice's orders → Alice disappears)

---

# Good Design

customers table (id, name)  
orders table (id, customer_id, product)  

👉 Linked via `customer_id`

Alice is stored **once**. Each order just points to her.

---

# Thinking Shift

From:
❌ “store everything in one table”

To:
✅ “one table per kind of thing, linked by keys”

---

# ER Diagram (Concept)

An **Entity-Relationship (ER) diagram** is a picture of the design:

- Entities = the things (they become tables)
- Relationships = the connections (they become foreign keys)

Example:
Customer — *places* → Order

---

# Simple ER Example

```
Customer (id, name)  ──<  Order (id, customer_id, amount)
   one customer             many orders
```

The foreign key (`customer_id`) goes in the table on the **"many"** side.

---

# SQL Preview (JOIN)

```sql
SELECT c.name, o.amount
FROM customers c
JOIN orders o
  ON c.id = o.customer_id;
```

| name | amount |
|------|--------|
| Alice | 1000 |
| Alice | 800 |

👉 This is WHY relationships matter (JOINs are covered in Weeks 4–5)

---

# In-Class Exercise

👉 “How would you store students and the courses they take?”

Think about:
- a `students` table
- a `courses` table
- an `enrollments` table (the junction table)

Which columns are primary keys? Which are foreign keys?

---

# Common Mistakes

- No primary key
- Linking tables by names instead of IDs (names repeat and change)
- One big table for everything
- A many-to-many relationship without a junction table

---

# Mental Model

Tables = entities  
Keys = connections  

👉 Database = connected system

---

# Hands-On Lab

- Create 2 tables
- Add primary keys
- Add a foreign key
- Try to insert bad data — and read the error
- Try a simple JOIN

---

# Summary

- Structure matters more than syntax
- Primary keys identify rows; foreign keys link tables
- Many-to-many relationships need a junction table
- Good design prevents problems

---

# What’s Next?

Week 3:
- SELECT, WHERE, ORDER BY in depth
- Functions, CASE, and computed columns
- GROUP BY and HAVING
- Keys, CRUD, and auto-increment IDs

---

# Final Thought

Good databases are designed, not just written.

👉 Think before you build.

---

# Let’s Practice 🚀

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
