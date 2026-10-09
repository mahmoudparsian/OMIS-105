# Primary Key & CRUD Operations in DuckDB

This guide introduces two fundamental concepts in relational databases using **DuckDB**:

1. **Primary Key (PK):** A unique identifier for every record in a table.

2. **CRUD Operations:** The four basic database operations: **C**reate, **R**ead, **U**pdate, and **D**elete.

---

## What is a Primary Key (PK)?

A **Primary Key** is a column (or combination of columns) that uniquely identifies each row in a database table.

* **Unique:** No two rows can have the same primary key value.
* **NOT NULL:** A primary key column can never contain `NULL`.
* **One per table:** A table has at most one primary key (it may use several columns together).

---

## Example Schema: `products`

We will use a simple store inventory table called `products`.
Here we choose each `product_id` ourselves.

```sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name VARCHAR,
    category VARCHAR,
    price DECIMAL(10, 2)
);
```

---

## Step-by-Step CRUD Guide

### 1. **C**reate (Insert Data)

The **Create** operation adds new rows to your table using the `INSERT INTO` statement.

```sql
-- Insert initial records
INSERT INTO products (product_id, name, category, price) VALUES
    (1, 'Laptop', 'Electronics', 999.99),
    (2, 'Wireless Mouse', 'Electronics', 25.00),
    (3, 'Desk Chair', 'Furniture', 150.00);
```

#### Primary Key Constraint in Action
If you try to insert a duplicate `product_id`, DuckDB rejects the row with a primary key error:

```sql
-- This will cause an error!
INSERT INTO products (product_id, name, category, price) 
VALUES (1, 'Smartphone', 'Electronics', 699.99);
-- Constraint Error: Duplicate key "product_id: 1" violates primary key constraint.
```

#### Tip: Let DuckDB Choose the IDs (Auto-Increment)
Choosing every ID by hand is easy to get wrong. A
**sequence** can number new rows for you
(1, 2, 3, ...). Then the `INSERT` leaves out `product_id`:

```sql
CREATE SEQUENCE product_id_seq START 1;

CREATE TABLE products_auto (
    product_id INTEGER PRIMARY KEY DEFAULT nextval('product_id_seq'),
    name VARCHAR,
    category VARCHAR,
    price DECIMAL(10, 2)
);

INSERT INTO products_auto (name, category, price)
VALUES ('Laptop', 'Electronics', 999.99);   -- product_id = 1
```

DuckDB has no `AUTO_INCREMENT` keyword; this is
how DuckDB does it. Details: `slides_09_AUTO_INCREMENT_in_DuckDB.md`.

---

### 2. **R**ead (Query Data)

The **Read** operation retrieves data from the table using the `SELECT` statement.

#### Read All Columns and Rows
```sql
SELECT * FROM products;
```

**Result:**

| product_id | name | category | price |
| :--- | :--- | :--- | :--- |
| **1** | Laptop | Electronics | `999.99` |
| **2** | Wireless Mouse | Electronics | `25.00` |
| **3** | Desk Chair | Furniture | `150.00` |

---

#### Read Specific Columns with Filtering
Find products in the `'Electronics'` category using a `WHERE` clause:

```sql
SELECT name, price 
FROM products 
WHERE category = 'Electronics';
```

**Result:**

| name | price |
| :--- | :--- |
| Laptop | `999.99` |
| Wireless Mouse | `25.00` |

---

### 3. **U**pdate (Modify Data)

The **Update** operation changes existing rows using the `UPDATE` statement. The `WHERE` clause chooses **which** rows change. Using the primary key in `WHERE` is the safest way to change exactly one row.

```sql
-- Apply a discount to the Desk Chair (product_id = 3)
UPDATE products
SET price = 129.99
WHERE product_id = 3;
```

#### Check the Updated Row
```sql
SELECT * FROM products WHERE product_id = 3;
```

**Result:**

| product_id | name | category | price |
| :--- | :--- | :--- | :--- |
| **3** | Desk Chair | Furniture | `129.99` |

---

### 4. **D**elete (Remove Data)

The **Delete** operation removes rows using the `DELETE FROM` statement. Like `UPDATE`, use the primary key in `WHERE` so you remove only the row you mean.

```sql
-- Remove Wireless Mouse (product_id = 2)
DELETE FROM products
WHERE product_id = 2;
```

#### Check the Final Table
```sql
SELECT * FROM products;
```

**Result:**

| product_id | name | category | price |
| :--- | :--- | :--- | :--- |
| **1** | Laptop | Electronics | `999.99` |
| **3** | Desk Chair | Furniture | `129.99` |

---

## CRUD Cheat Sheet

| Operation | SQL Command | Description |
| :--- | :--- | :--- |
| **C**reate | `INSERT INTO table ...` | Add new rows to a table |
| **R**ead | `SELECT ... FROM table` | Retrieve data from a table |
| **U**pdate | `UPDATE table SET ... WHERE id = x` | Modify existing rows |
| **D**elete | `DELETE FROM table WHERE id = x` | Remove rows from a table |

---

## Warning: `UPDATE` and `DELETE` Without `WHERE`

```sql
-- ⚠️ Do NOT run these. They show what can go wrong.
UPDATE products SET price = 0;   -- changes EVERY row!
DELETE FROM products;            -- removes EVERY row!
```

There is no "undo". **Safe habit:** first run a
`SELECT` with the same `WHERE` clause. Check that it
returns only the rows you want. Then run the
`UPDATE` or `DELETE`.

---

## Key Points

1. A **primary key** gives every row a unique, non-`NULL` identifier.
2. An **auto-increment** key (a `SEQUENCE` in DuckDB) lets the database choose new IDs for you.
3. **CRUD** = `INSERT` (Create), `SELECT` (Read), `UPDATE` (Update), `DELETE` (Delete).
4. Always write a **`WHERE` clause** for `UPDATE` and `DELETE`. Without it, every row is changed or removed.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
