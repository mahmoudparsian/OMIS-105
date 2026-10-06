# Primary Key & CRUD Operations in DuckDB

This guide introduces two fundamental concepts in relational databases using **DuckDB**:

1. **Primary Key (PK):** A unique identifier for every record in a table.

2. **CRUD Operations:** The four basic database operations: **C**reate, **R**ead, **U**pdate, and **D**elete.

---

## What is a Primary Key (PK)?

A **Primary Key** is a column (or combination of columns) that uniquely identifies each row in a database table.

* **Unique:** No two rows can have the same primary key value.
* **NOT NULL:** A primary key column can never contain `NULL`.

---

## Example Schema: `products`

We will use a simple store inventory table called `products`.

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
If you try to insert a duplicate `product_id`, DuckDB will raise a Primary Key violation error:

```sql
-- This will cause an error!
INSERT INTO products (product_id, name, category, price) 
VALUES (1, 'Smartphone', 'Electronics', 699.99);
-- Error: Constraint Error: PRIMARY KEY constraint failed
```

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

The **Update** operation modifies existing records using the `UPDATE` statement. Always use the Primary Key in the `WHERE` clause to target specific records safely.

```sql
-- Apply a discount to the Desk Chair (product_id = 3)
UPDATE products
SET price = 129.99
WHERE product_id = 3;
```

#### Check Updated State
```sql
SELECT * FROM products WHERE product_id = 3;
```

**Result:**

| product_id | name | category | price |
| :--- | :--- | :--- | :--- |
| **3** | Desk Chair | Furniture | `129.99` |

---

### 4. **D**elete (Remove Data)

The **Delete** operation removes rows using the `DELETE FROM` statement. Like `UPDATE`, target rows by their Primary Key to avoid accidentally removing unwanted data.

```sql
-- Remove Wireless Mouse (product_id = 2)
DELETE FROM products
WHERE product_id = 2;
```

#### Check Final Table State
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

## Summary Key Points

1. **Primary Keys** enforce data integrity by guaranteeing each row is uniquely addressable.
2. Always specify a **`WHERE` clause referencing the Primary Key** when executing `UPDATE` or `DELETE` queries to prevent updating or deleting the entire table by accident.