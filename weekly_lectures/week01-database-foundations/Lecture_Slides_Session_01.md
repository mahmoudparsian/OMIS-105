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

Data = raw facts

Examples:

- Name: "Alice"
- Price: 1000
- Date: 2026-01-01

---

### What is Metadata?

Metadata in database tables is "**data about data**"
—the underlying blueprint that defines how a table 
is structured, organized, and governed rather than 
the actual records stored inside it. 

```sql
-- metadata
CREATE TABLE employees (
  name  VARCHAR,
  age   int,
  salary int
);
```

```sql
-- data
INSERT INTO employees 
VALUES
('alex', 25, 78000);
```

---

# From Data to Information

Data → processed → Information

Example:

- **Raw Data**: sales transactions

- **Insight:** “Top-selling products in CA”

- **Insight:** “Top-5 Customers in NY”

- **Insight:** “Total sales of iPhone 16 in December 2025”


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

| customer | order  | price |
|----------|--------|-------|
| Alice    | Laptop | 1800  |
| Alice    | Phone  | 1200  |
| Alice    | Phone  | 1100  |
| Jane     | Laptop | 1900  |
| Jane     | Phone  | 1400  |

👉 What if name changes?

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

- Ensure consistency

- Handle multiple users

---

# Examples of DBMS

- **DuckDB**
- MySQL
- PostgreSQL
- Snowflake
- Oracle

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

- Table

- Row (record)

- Column (attribute)

---

# What is SQL?

**S**tructured **Q**uery **L**anguage

Used to:

- Create table

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
    product_id INTEGER,
    product_name VARCHAR,
    price INTEGER
);
```

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
---

# Query Data

```sql
SELECT * 
FROM products;
```

---

# Filter Data

```sql
SELECT * 
FROM products
WHERE price > 700;
```

---

# Compute Values

```sql
SELECT name, 
       price,
       price * 0.9 AS discounted_price
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
