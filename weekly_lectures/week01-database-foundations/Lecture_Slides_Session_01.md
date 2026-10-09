---
title: OMIS 105 - Week 1 (Database Foundations)
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
## Introduction to Database Management Systems  
## Week 1 — Foundations
## Instructor: Dr. Parsian

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

Data = raw facts, before anyone has organized or analyzed them

Examples:

- Name: "Alice"
- Price: 1000
- Date: 2026-01-01

---

### What is Metadata?

Metadata is "**data about data**": the blueprint that
describes a table — its name, its columns, and their
data types — not the records stored inside it.

```sql
-- metadata: the structure of the table
CREATE TABLE employees (
  name   VARCHAR,
  age    INTEGER,
  salary INTEGER
);
```

```sql
-- data: the actual records
INSERT INTO employees
VALUES
('Alex', 25, 78000);
```

---

# From Data to Information

Data → processed → Information

Example:

- **Raw data:** thousands of sales transactions

- **Information:** “Top-selling products in CA”

- **Information:** “Top-5 customers in NY”

- **Information:** “Total sales of iPhone 16 in December 2025”

Information helps people make **decisions**.


---

# What is a Database?

A structured collection of data

Key properties:

- Organized (stored in a known structure)

- Persistent (still there after you close the program)

- Queryable (you can ask it questions)

---

# File System vs Database

## Files (Excel / CSV)
- No relationships between files
- Hard to maintain
- Data duplication
- No rules: anyone can type anything

## Database
- Structured
- Connected data
- Efficient queries

---

# Problem: Data Duplication

| customer | product | price |
|----------|---------|-------|
| Alice    | Laptop | 1800  |
| Alice    | Phone  | 1200  |
| Alice    | Phone  | 1100  |
| Jane     | Laptop | 1900  |
| Jane     | Phone  | 1400  |

👉 What if Alice changes her name? We must update **3** rows — and miss none.

---

# Solution: Database Design

Separate tables:

* Customers  

* Orders  

👉 One change → consistent everywhere

---

# What is a DBMS?

Database Management System

**Responsibilities:**

- Store data

- Retrieve data

- Ensure consistency (enforce rules)

- Handle multiple users at the same time

- Protect data (security, backups)

---

# Examples of DBMS

- **DuckDB** (our course tool)
- MySQL
- PostgreSQL
- Oracle
- SQL Server
- Snowflake (in the cloud)

---

# Roles in Database World

- Developer → builds apps

- Analyst → queries data

- DBA → manages database

---

# Relational Model (Preview)

Data stored in tables:

**products** table:

| id  | name   | price   |
|-----|--------|---------|
| 100 | Laptop | 1200.00 |
| 200 | Monitor| 300.00  |

---

# Key Terms

- **Table:** all the records of one kind (e.g., products)

- **Row** (record): one item (one product)

- **Column** (attribute): one fact about every item (e.g., price)

---

# What is SQL?

**S**tructured **Q**uery **L**anguage

Used to:

- Create tables

- Insert data

- Query data

- Update and delete data

SQL is **declarative**: you say *what* you want, and the database decides *how* to get it.

---

# First SQL Query

```sql
SELECT 1;
SELECT 2 + 3 AS answer;     -- 5
```

👉 SQL can act like a calculator

---

# Create a Table

```sql
CREATE TABLE products (
    product_id   INTEGER,
    product_name VARCHAR,
    price        INTEGER
);
```

Each column has a **name** and a **data type** (INTEGER = whole number, VARCHAR = text).

---

# Insert Data

```sql
INSERT INTO products 
VALUES
(1, 'Laptop', 1000),
(2, 'Phone-12', 800),
(3, 'Tablet-1', 500);
```

```sql
INSERT INTO products (product_id, product_name, price)
VALUES
(11, 'Laptop-X', 1200),
(23, 'Phone-11', 700),
(35, 'Tablet-2', 500);
```

The second form lists the columns. It is safer: the values go to the named columns.

---

# Query Data

```sql
SELECT *
FROM products;
```

`*` means "all columns". This returns all 6 rows we inserted.

---

# Filter Data

```sql
SELECT *
FROM products
WHERE price > 700;
```

Returns: Laptop (1000), Phone-12 (800), Laptop-X (1200)

---

# Compute Values

```sql
SELECT product_name,
       price,
       price * 0.9 AS discounted_price
FROM products;
```

`AS` gives the new column a name. The table itself does not change.

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

Write the query:

👉 “Find all products that cost more than $800.”

(Answer: Laptop and Laptop-X)

---

# Common Beginner Mistakes

- Forgetting quotes around text: `'Laptop'`

- Confusing columns and rows

- Forgetting the `;` at the end of a statement

- Expecting SQL to work step by step like Python — you describe the result instead

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

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
