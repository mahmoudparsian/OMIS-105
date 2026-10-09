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
- Based on mathematics: set theory and logic
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

(Careful: later, "cardinality" also describes **relationships** — 1:1, 1:M, M:M.)

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

**Best practice**: Use surrogate keys (like `customer_id`) as primary keys,
and keep natural keys (like `email`) as `UNIQUE` columns.

---

# Candidate Keys

A **candidate key** is any column (or combination) that *could* serve as a PK.

In our `customers` table:
- `customer_id` → candidate key (chosen as PK)
- `email` → candidate key (unique per customer)

The one you choose becomes the **primary key**; the others are called
**alternate keys**. Declare them `UNIQUE` so the database still enforces them.

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

(Our ShopSmart CSV gives `order_items` its own surrogate key, `item_id`, instead — both designs are common.)

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

A foreign key column **can** be `NULL` (an order with no customer).
Add `NOT NULL` if every order must have a customer:
`customer_id INTEGER NOT NULL REFERENCES customers(customer_id)`

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
2. Cannot DELETE a customer who still has orders
3. Cannot UPDATE a `customer_id` in `customers` while orders refer to it

```sql
-- FAILS: customer 999 doesn't exist
INSERT INTO orders (order_id, customer_id, order_date, total_amount)
VALUES (100, 999, DATE '2024-01-01', 50.00);
-- Constraint Error: Violates foreign key constraint because key
-- "customer_id: 999" does not exist in the referenced table
```

Some databases (PostgreSQL, MySQL) can **cascade** a delete to the child rows
(`ON DELETE CASCADE`). DuckDB does not support cascading: delete the orders first.

DuckDB limitation: while orders refer to a customer, you also cannot change
that customer's `UNIQUE` columns (like `email`). Ordinary columns (like `city`)
can be updated normally.

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

**Example**: Each customer has at most one loyalty profile.

```sql
CREATE TABLE loyalty_profiles (
    profile_id  INTEGER PRIMARY KEY,
    customer_id INTEGER UNIQUE REFERENCES customers(customer_id),
    points      INTEGER DEFAULT 0,
    tier        VARCHAR DEFAULT 'Bronze'
);
```

The `UNIQUE` constraint on the FK means a customer can appear **at most once**
in `loyalty_profiles` — so each customer has zero or one profile.
(A second profile for the same customer fails: `Duplicate key "customer_id: 1"
violates unique constraint.`)

---

# Many-to-Many (M:M)

A product can have **many** suppliers.
A supplier can supply **many** products.

**Cannot be represented directly** — a single FK column can hold only one value.
It needs a **junction table** (also called a bridge or associative table).

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
products (1) ──< product_suppliers >── (1) suppliers
```

The M:M becomes **two 1:M** relationships. The junction table can also store
facts about the pair itself — here, the `cost_price` each supplier charges.

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

We will use **Crow's Foot** notation — the most widely used style in industry.

---

# Crow's Foot Symbols

Each end of a line has two marks. The mark **next to the table** is the
maximum (one or many); the other is the minimum (zero or one):

```
──||   Exactly one        (min 1, max 1)
──o|   Zero or one        (min 0, max 1)
──|<   One or many        (min 1, max many)
──o<   Zero or many       (min 0, max many)
```

Example: `customers ||──o< orders` — each order has exactly one customer;
a customer has zero or many orders.

---

# ShopSmart ER Diagram (Simplified)

```
┌──────────────┐                    ┌──────────────┐
│ categories   │                    │ customers    │
│──────────────│                    │──────────────│
│PK category_id│                    │PK customer_id│
│ category_name│                    │ first_name   │
│ description  │                    │ last_name    │
└──────┬───────┘                    │ email        │
       │ 1                          └──────┬───────┘
       │                                   │ 1
       │ M                                 │ M
┌──────┴───────┐                    ┌──────┴───────┐
│ products     │                    │ orders       │
│──────────────│                    │──────────────│
│PK product_id │                    │PK order_id   │
│ product_name │                    │FK customer_id│
│FK category_id│                    │ order_date   │
│ price        │                    │ status       │
│ stock_qty    │                    │ total_amount │
└──────┬───────┘                    └──────┬───────┘
       │ 1                                 │ 1
       │          ┌──────────────┐         │
       └─────── M │ order_items  │ M ──────┘
                  │──────────────│
                  │PK item_id    │
                  │FK order_id   │
                  │FK product_id │
                  │ quantity     │
                  │ unit_price   │
                  └──────────────┘
```

`order_items` is the junction table for the M:M between orders and products.

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
    category_id    INTEGER NOT NULL REFERENCES categories(category_id),
    price          DECIMAL(10,2) NOT NULL CHECK (price > 0),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0)
);
```

Create tables in order: **parents first** (`categories` before `products`).

---

# Schema (continued)

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name  VARCHAR NOT NULL,
    last_name   VARCHAR NOT NULL,
    email       VARCHAR UNIQUE NOT NULL,
    city        VARCHAR,
    state       VARCHAR(2),    -- DuckDB treats this as VARCHAR (no length check)
    join_date   DATE
);

CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date   DATE NOT NULL,
    status       VARCHAR CHECK (status IN
        ('processing','shipped','completed','cancelled')),
    total_amount DECIMAL(10,2)
);

CREATE TABLE order_items (
    item_id    INTEGER PRIMARY KEY,
    order_id   INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL
);
```

---

# Loading Data from CSV

This week's `data/` folder has three files: `categories.csv`, `customers.csv`,
and `products.csv`. (Orders arrive in Week 4.)

The tables already exist (with their keys and rules), so we **insert** into them.
DuckDB checks every PK, FK, and `CHECK` rule as the rows load.

```python
import duckdb
con = duckdb.connect()
# ... run the CREATE TABLE statements first ...

# Parents first: categories before products
for table in ['categories', 'customers', 'products']:
    con.execute(f"INSERT INTO {table} SELECT * FROM read_csv('data/{table}.csv')")
    count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"Loaded {table}: {count} rows")

# Loaded categories: 8 rows
# Loaded customers: 40 rows
# Loaded products: 64 rows
```

`CREATE TABLE ... AS SELECT * FROM read_csv(...)` also works, but makes a new
table **without** any keys or rules.

---

# Verifying Relationships

```sql
-- Do all products reference valid categories?
SELECT p.product_id, p.category_id
FROM products p
WHERE p.category_id NOT IN (
    SELECT category_id FROM categories
);
-- 0 rows: every product points to a real category
```

With a foreign key, DuckDB already guarantees this. The check is useful when
data was loaded **without** constraints (e.g., with `CREATE TABLE ... AS`).

---

# Preview: Joining Tables

```sql
-- Show each product with its category name
SELECT p.product_name, c.category_name, p.price
FROM products p, categories c
WHERE p.category_id = c.category_id
ORDER BY p.price DESC
LIMIT 5;
```

| product_name | category_name | price |
|---|---|---|
| Tablet Air | Electronics | 446.63 |
| Laptop Pro 15 | Electronics | 372.07 |
| Smartphone X12 | Electronics | 321.52 |
| Bluetooth Speaker | Electronics | 297.29 |
| Green Tea Box | Food & Grocery | 149.61 |

This is an implicit join — we will learn the proper `JOIN` syntax in Weeks 4–5!

---

# Identifying Keys in Our Data

| Table | Primary Key | Foreign Keys |
|-------|------------|-------------|
| categories | category_id | — |
| products | product_id | category_id → categories |
| customers | customer_id | — |
| orders | order_id | customer_id → customers |
| order_items | item_id | order_id → orders, product_id → products |

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
- A book can have many authors, and an author can write many books (M:M → `book_authors`)
- Members and books are also M:M: a member borrows many books over time,
  and a book is borrowed by many members
- The `loans` table resolves it: each loan links **one** member to **one** book

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
| Domain | Data types, NOT NULL, CHECK | Price must be > 0 |
| User-defined | Business rules (often CHECK) | Status must be in the allowed list |

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

**Week 3: SQL Basics**
- SELECT, WHERE, ORDER BY in depth
- Functions, CASE, and computed columns
- GROUP BY and HAVING
- Keys, CRUD, and auto-increment IDs

---

# Questions?

Thank you!

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
