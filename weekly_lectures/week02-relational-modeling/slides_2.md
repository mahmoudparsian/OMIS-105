---
marp: true
theme: default
paginate: true
header: "OMIS 105 – Database Management Systems"
footer: "Week 2: Relational Thinking"
---

# OMIS 105: Database Management Systems
## Week 2 — Relational Thinking
### Instructor: Dr. Parsian

---

# This Week's Goals

1. Understand the relational model
2. Learn about keys (primary, foreign, candidate, composite)
3. Understand table relationships (1:1, 1:M, M:M)
4. Read and draw Entity-Relationship (ER) diagrams
5. Design a multi-table schema for ShopSmart

---

# Recap: Week 1

- Databases vs. flat files
- Tables, rows, columns, schemas
- DuckDB basics
- Basic SQL: SELECT, WHERE, ORDER BY, LIMIT
- Aggregate functions

**Now**: How do we organize data across *multiple* tables?

---

# Session 1: The Relational Model

---

# The Relational Model — History

- Proposed by **Edgar F. Codd** in 1970 at IBM
- Revolutionary idea: store data in **relations** (tables)
- Based on mathematical set theory
- Still the dominant data model 50+ years later

---

# Core Terminology

| Math Term | Database Term | Meaning |
|-----------|--------------|---------|
| Relation | Table | Collection of tuples |
| Tuple | Row / Record | Single data entry |
| Attribute | Column / Field | Property of an entity |
| Domain | Data Type | Allowed values |
| Cardinality | Row count | Number of tuples |
| Degree | Column count | Number of attributes |

---

# Why Multiple Tables?

**Single-table approach** (denormalized):

| order_id | customer_name | email | product | price |
|----------|--------------|-------|---------|-------|
| 1 | Alice Smith | alice@email.com | Laptop | 899 |
| 2 | Alice Smith | alice@email.com | Mouse | 29 |
| 3 | Bob Johnson | bob@email.com | Laptop | 899 |

**Problems**: Redundancy, update anomalies, deletion anomalies

---

# Redundancy Problem

If Alice places 50 orders, her name and email are stored **50 times**.

- **Wastes storage**
- **Update anomaly**: If Alice changes her email, you must update 50 rows
- **Risk of inconsistency**: Miss one row → two different emails for Alice

---

# Deletion Anomaly

If we delete Bob's only order, we lose his customer information entirely!

**Solution**: Separate data into related tables.

---

# The Multi-Table Solution

**customers** table:
| customer_id | name | email |
|------------|------|-------|
| 1 | Alice Smith | alice@email.com |
| 2 | Bob Johnson | bob@email.com |

**orders** table:
| order_id | customer_id | product | price |
|----------|------------|---------|-------|
| 1 | 1 | Laptop | 899 |
| 2 | 1 | Mouse | 29 |
| 3 | 2 | Laptop | 899 |

---

# Keys: Connecting the Dots

---

# Primary Key (PK)

A column (or set of columns) that **uniquely identifies** each row.

**Rules**:
- Must be unique — no two rows share the same PK value
- Cannot be NULL
- Should rarely change
- Every table should have one

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,  -- PK
    first_name  VARCHAR NOT NULL,
    last_name   VARCHAR NOT NULL,
    email       VARCHAR UNIQUE
);
```

---

# Natural vs. Surrogate Keys

**Natural key**: A real-world attribute
- Email address, Social Security Number, ISBN
- Meaningful but may change

**Surrogate key**: An artificial identifier
- Auto-generated integer (1, 2, 3, ...)
- No business meaning, never changes

**Best practice**: Use surrogate keys (like `customer_id`) as primary keys.

---

# Candidate Keys

A **candidate key** is any column (or combination) that *could* serve as a PK.

In our `customers` table:
- `customer_id` → candidate key (chosen as PK)
- `email` → candidate key (unique per customer)

The one you choose becomes the **primary key**; the rest remain candidate keys.

---

# Composite Key

A primary key made of **two or more columns** together.

```sql
CREATE TABLE order_items (
    order_id   INTEGER,
    product_id INTEGER,
    quantity   INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

Neither `order_id` nor `product_id` is unique alone, but **together** they uniquely identify each line item.

---

# Foreign Key (FK)

A column in one table that **references** the primary key of another table.

```sql
CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER REFERENCES customers(customer_id),
    order_date   DATE,
    total_amount DECIMAL(10,2)
);
```

`customer_id` in `orders` → Foreign Key
`customer_id` in `customers` → Primary Key

---

# Foreign Key — Visual

```
customers                    orders
┌─────────────┐             ┌──────────────────┐
│ customer_id │─────PK──────│ customer_id (FK)  │
│ first_name  │             │ order_id (PK)     │
│ last_name   │             │ order_date        │
│ email       │             │ total_amount      │
└─────────────┘             └──────────────────┘
```

The FK enforces **referential integrity**: you cannot have an order for a customer that does not exist.

---

# Referential Integrity

**Rules enforced by foreign keys**:

1. Cannot INSERT an order with a `customer_id` that does not exist in `customers`
2. Cannot DELETE a customer who has existing orders (unless cascading)
3. Cannot UPDATE a `customer_id` in `customers` if it is referenced

```sql
-- This would FAIL if customer 999 doesn't exist:
INSERT INTO orders VALUES (100, 999, '2024-01-01', 50.00);
```

---

# Relationships Between Tables

---

# Types of Relationships

| Type | Notation | Example |
|------|----------|---------|
| One-to-One | 1:1 | Customer ↔ Customer Profile |
| One-to-Many | 1:M | Customer → Orders |
| Many-to-Many | M:M | Products ↔ Suppliers |

---

# One-to-Many (1:M)

The most common relationship.

**One** customer can place **many** orders.
Each order belongs to **one** customer.

```
customers (1) ────── (M) orders
```

The FK goes in the "many" side table.

---

# One-to-One (1:1)

Each entity on both sides has exactly one counterpart.

**Example**: Each customer has exactly one loyalty profile.

```sql
CREATE TABLE loyalty_profiles (
    profile_id  INTEGER PRIMARY KEY,
    customer_id INTEGER UNIQUE REFERENCES customers(customer_id),
    points      INTEGER DEFAULT 0,
    tier        VARCHAR DEFAULT 'Bronze'
);
```

The `UNIQUE` constraint on the FK enforces 1:1.

---

# Many-to-Many (M:M)

A product can have **many** suppliers.
A supplier can supply **many** products.

**Cannot be represented directly** — needs a **junction table** (also called bridge/associative table).

---

# Junction Table Example

```sql
CREATE TABLE product_suppliers (
    product_id  INTEGER REFERENCES products(product_id),
    supplier_id INTEGER REFERENCES suppliers(supplier_id),
    cost_price  DECIMAL(10,2),
    PRIMARY KEY (product_id, supplier_id)
);
```

```
products (M) ── product_suppliers ── (M) suppliers
```

---

# Entity-Relationship (ER) Diagrams

---

# What Is an ER Diagram?

A **visual blueprint** of your database design showing:
- **Entities** (tables) — rectangles
- **Attributes** (columns) — listed inside
- **Relationships** — lines connecting entities
- **Cardinality** — symbols showing 1:1, 1:M, M:M

---

# ER Notation Styles

| Style | One | Many |
|-------|-----|------|
| Chen | 1 | M or N |
| Crow's Foot | \|\| | ──<  (fork) |
| Min-Max | (1,1) | (0,*) |

We will use **Crow's Foot** notation — the industry standard.

---

# Crow's Foot Symbols

```
──||──     Exactly one (mandatory)
──|O──     Zero or one (optional)
──<──      Many (one or more)
──<O──     Zero or many (optional many)
```

---

# ShopSmart ER Diagram (Simplified)

```
┌────────────┐         ┌────────────┐
│ categories │         │ customers  │
│────────────│         │────────────│
│ PK cat_id  │──┐      │ PK cust_id │──┐
│ cat_name   │  │      │ first_name │  │
│ description│  │      │ last_name  │  │
└────────────┘  │      │ email      │  │
                │      └────────────┘  │
           ┌────┴───┐            ┌─────┴────┐
           │products│            │  orders   │
           │────────│            │──────────│
           │PK p_id │──┐         │PK ord_id │
           │name    │  │         │FK cust_id│
           │FK cat  │  │         │date      │
           │price   │  │         │status    │
           │stock   │  │         │total     │
           └────────┘  │         └──────────┘
                       │
                  ┌────┴──────┐
                  │order_items│
                  │───────────│
                  │FK ord_id  │
                  │FK p_id    │
                  │quantity   │
                  │unit_price │
                  └───────────┘
```

---

# Session 2: Building It in DuckDB

---

# ShopSmart Schema — Full DDL

```sql
CREATE TABLE categories (
    category_id   INTEGER PRIMARY KEY,
    category_name VARCHAR NOT NULL,
    description   VARCHAR
);

CREATE TABLE products (
    product_id     INTEGER PRIMARY KEY,
    product_name   VARCHAR NOT NULL,
    category_id    INTEGER REFERENCES categories(category_id),
    price          DECIMAL(10,2) CHECK (price > 0),
    stock_quantity INTEGER DEFAULT 0
);
```

---

# Schema (continued)

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name  VARCHAR NOT NULL,
    last_name   VARCHAR NOT NULL,
    email       VARCHAR UNIQUE NOT NULL,
    city        VARCHAR,
    state       VARCHAR(2),
    join_date   DATE
);

CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER REFERENCES customers(customer_id),
    order_date   DATE NOT NULL,
    status       VARCHAR CHECK (status IN
        ('processing','shipped','completed','cancelled')),
    total_amount DECIMAL(10,2)
);
```

---

# Loading Data from CSV

```python
import duckdb
con = duckdb.connect()

# Load each CSV into a table
for table, file in [
    ('categories', 'categories.csv'),
    ('products',   'products.csv'),
    ('customers',  'customers.csv'),
    ('orders',     'orders.csv')]:
    con.sql(f"""
        CREATE TABLE {table} AS
        SELECT * FROM read_csv_auto('{file}')
    """)
    count = con.sql(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"Loaded {table}: {count} rows")
```

---

# Verifying Relationships

```sql
-- Do all orders reference valid customers?
SELECT o.order_id, o.customer_id
FROM orders o
WHERE o.customer_id NOT IN (
    SELECT customer_id FROM customers
);
-- Should return 0 rows if data integrity holds
```

---

# Preview: Joining Tables

```sql
-- Combine customer info with their orders
SELECT c.first_name, c.last_name,
       o.order_id, o.order_date, o.total_amount
FROM customers c, orders o
WHERE c.customer_id = o.customer_id
ORDER BY o.order_date DESC
LIMIT 10;
```

This is an implicit join — we will learn proper JOIN syntax in Week 3!

---

# Identifying Keys in Our Data

| Table | Primary Key | Foreign Keys |
|-------|------------|-------------|
| categories | category_id | — |
| products | product_id | category_id → categories |
| customers | customer_id | — |
| orders | order_id | customer_id → customers |

---

# Database Design Best Practices

1. **Every table gets a surrogate PK** (integer ID)
2. **Use foreign keys** to link related tables
3. **Avoid redundancy** — store each fact once
4. **Choose meaningful names** — `customer_id` not `cid`
5. **Apply constraints** — NOT NULL, CHECK, UNIQUE
6. **Document your schema** — ER diagrams!

---

# Common Design Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Repeating data | Customer name in every order | Use FK to customers table |
| No primary key | Table without a unique ID | Add surrogate key |
| Wrong relationship | M:M without junction table | Add bridge table |
| Too few tables | Everything in one giant table | Split into entities |
| Too many tables | Splitting name into own table | Keep related data together |

---

# Thinking Relationally: A Process

1. **Identify entities** — What "things" do we track?
2. **Define attributes** — What do we know about each thing?
3. **Find relationships** — How are entities related?
4. **Determine cardinality** — 1:1, 1:M, or M:M?
5. **Assign keys** — PK for each table, FK for relationships
6. **Draw the ER diagram** — Visualize the design

---

# Exercise: Design a Library Database

Entities to consider:
- Books
- Authors
- Members
- Loans

What are the relationships?
- A book can have many authors (M:M)
- A member can borrow many books (1:M with loans)
- A loan links one member to one book

---

# Library ER Diagram

```
┌──────────┐          ┌────────────┐
│ authors  │          │  members   │
│──────────│          │────────────│
│ PK a_id  │──┐       │ PK m_id   │──┐
│ name     │  │       │ name      │  │
│ bio      │  │       │ email     │  │
└──────────┘  │       └───────────┘  │
         ┌────┴────┐           ┌─────┴───┐
         │book_auth│           │  loans  │
         │─────────│           │─────────│
         │FK book  │           │PK loan_id│
         │FK auth  │           │FK m_id  │
         └────┬────┘           │FK b_id  │
         ┌────┴────┐           │due_date │
         │  books  │───────────└─────────┘
         │─────────│
         │PK b_id  │
         │ title   │
         │ isbn    │
         │ year    │
         └─────────┘
```

---

# Data Integrity Summary

| Integrity Type | Enforced By | Example |
|---------------|-------------|---------|
| Entity | Primary Key | Each product has unique ID |
| Referential | Foreign Key | Orders reference valid customers |
| Domain | Data Types, CHECK | Price must be > 0 |
| User-defined | Business rules | Status must be in allowed list |

---

# Summary

- The **relational model** organizes data into related tables
- **Primary keys** uniquely identify rows
- **Foreign keys** link tables and enforce referential integrity
- Relationships come in three types: **1:1, 1:M, M:M**
- **ER diagrams** visualize database structure
- Good design **eliminates redundancy** and **prevents anomalies**

---

# What Is Next?

**Week 3: SQL Mastery — Part 1**
- SELECT with JOINs (combining tables!)
- GROUP BY and HAVING
- More powerful queries

---

# Questions?

Thank you!

