# Introduction to Column Definitions <br> in DuckDB

When you create a table in SQL, you define 
**columns**. Each column has a **data type** 
(what kind of data it holds) and optional 
**constraints** (rules the data must follow).

In this tutorial, we will build a simple 
**Bookstore Database** to learn the most 
common SQL column definitions using DuckDB.

---

## 1. Core Concepts Covered

| Concept / Keyword | Type | Description |
| :--- | :--- | :--- |
| **Data Types** | Category | Defines the type of data stored: `INTEGER` (whole numbers), `VARCHAR` (text), `DECIMAL` (numbers with decimals), `DATE` (dates), and `BOOLEAN` (true/false). |
| **`PRIMARY KEY`** | Constraint | Uniquely identifies each row in a table. |
| **`SEQUENCE`** | Property | Automatically assigns sequential numbers (1, 2, 3...) to new rows. |
| **`NOT NULL`** | Constraint | Ensures a column cannot be left empty. |
| **`UNIQUE`** | Constraint | Prevents duplicate values in a column. |
| **`CHECK`** | Constraint | Enforces specific rules on column values (e.g., price must be greater than zero). |
| **`DEFAULT`** | Property | Automatically fills in a default value if none is provided. |
| **`FOREIGN KEY`** | Constraint | Links rows in one table to matching rows in another table. |

---

## 2. Creating the Tables (DDL)

Let's build three related tables: `authors`, `books`, and `orders`.

###  1. Authors Table
```sql
CREATE SEQUENCE author_id_seq START 1;

-- Demonstrates: PRIMARY KEY, SEQUENCE, 
--               NOT NULL, UNIQUE, DEFAULT
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY 
       DEFAULT nextval('author_id_seq'),
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE, -- No two authors can have the same email
    country VARCHAR DEFAULT 'Unknown' -- Defaults to 'Unknown' if not given
);
```

### 2. Books Table
```sql
-- Demonstrates: Foreign Keys, CHECK constraints, 
--               DECIMAL types
CREATE SEQUENCE book_id_seq START 1;

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY        
      DEFAULT nextval('book_id_seq'),
    title VARCHAR NOT NULL,
    author_id INTEGER NOT NULL,
    price DECIMAL(6, 2) NOT NULL CHECK (price > 0), -- Price must be positive
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0), -- Stock cannot be negative
    published_date DATE,
    
    -- Foreign Key link: connects book_id to the author who wrote it
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);
```

### 3. Orders Table
```sql
-- Demonstrates: BOOLEAN values, DEFAULT timestamps, 
--               multi-table Foreign Keys

CREATE SEQUENCE order_id_seq START 1;

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY 
       DEFAULT nextval('order_id_seq'),
    book_id INTEGER NOT NULL REFERENCES books(book_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    is_shipped BOOLEAN DEFAULT FALSE,
    order_date DATE DEFAULT CURRENT_DATE
);
```

---

## 3. Adding Sample Data

Now let's insert some data into our tables.

```sql
-- Insert Authors
INSERT INTO authors (first_name, last_name, email, country) 
VALUES 
  ('J.K.', 'Rowling', 'jk@example.com', 'United Kingdom'),
  ('George', 'Orwell', 'george@example.com', 'United Kingdom'),
  ('J.R.R.', 'Tolkien', 'jr@example.com', 'South Africa');

-- Insert Books
INSERT INTO books (title, author_id, price, stock_quantity, published_date) 
VALUES 
  ('Harry Potter and the Sorcerer''s Stone', 1, 19.99, 50, '1997-06-26'),
  ('1984', 2, 12.50, 30, '1949-06-08'),
  ('The Hobbit', 3, 14.95, 20, '1937-09-21');

-- Insert Orders
INSERT INTO orders (book_id, quantity) 
VALUES 
    (1, 2), -- Buying 2 copies of Harry Potter
    (2, 1); -- Buying 1 copy of 1984
```

---

## 4. Viewing the Data

Here is what our tables look like after inserting rows:

### `authors` Table

```sql
SELECT * 
FROM authors;
```

| author_id | first_name | last_name | email | country |
| :--- | :--- | :--- | :--- | :--- |
| `1` | J.K. | Rowling | `jk@example.com` | United Kingdom |
| `2` | George | Orwell | `george@example.com` | United Kingdom |
| `3` | J.R.R. | Tolkien | `jr@example.com` | South Africa |

### `books` Table

```sql
SELECT * 
FROM books;
```

| book_id | title | author_id | price | stock_quantity | published_date |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `1` | Harry Potter and the Sorcerer's Stone | `1` | `19.99` | `50` | `1997-06-26` |
| `2` | 1984 | `2` | `12.50` | `30` | `1949-06-08` |
| `3` | The Hobbit | `3` | `14.95` | `20` | `1937-09-21` |

### `orders` Table

```sql
SELECT * 
FROM orders;
```

| order_id | book_id | quantity | is_shipped | order_date |
| :--- | :--- | :--- | :--- | :--- |
| `1` | `1` | `2` | `false` | `2026-10-07` |
| `2` | `2` | `1` | `false` | `2026-10-07` |

---

## 5. What Happens When Rules Are Broken?

DuckDB checks your rules (constraints) every time you insert or update data. If a rule is broken, DuckDB cancels the query and shows an error message.

### Example 1: `CHECK` Constraint Error
Trying to add a book with a negative price:

```sql
INSERT INTO books (title, author_id, price) 
VALUES ('Broken Book', 1, -5.00);
```
**DuckDB Error Output:**
> `Constraint Error: CHECK constraint failed: (price > 0)`

---

### Example 2: `UNIQUE` Constraint Error
Trying to reuse an author email address:

```sql
INSERT INTO authors (first_name, last_name, email) 
VALUES ('Jane', 'Doe', 'jk@example.com');
```
**DuckDB Error Output:**
> `Constraint Error: Duplicate key "jk@example.com" violates unique constraint`

---

### Example 3: `FOREIGN KEY` Constraint Error
Trying to order a book that does not exist in the database (`book_id = 999`):

```sql
INSERT INTO orders (book_id, quantity) 
VALUES (999, 1);
```
**DuckDB Error Output:**
> `Constraint Error: Violates foreign key constraint`

* View Table 

```sql
memory D SELECT * FROM orders;
┌──────────┬───────────────┬──────────────────────────────────────────────────┬────────────┐
│ order_id │    amount     │                      status                      │ created_at │
│  int32   │ decimal(10,2) │ enum('valid', 'cancelled', 'pending', 'unknown') │    date    │
├──────────┼───────────────┼──────────────────────────────────────────────────┼────────────┤
│       10 │        234.56 │ valid                                            │ 2026-03-23 │
│       20 │        500.55 │ pending                                          │ 2026-03-29 │
└──────────┴───────────────┴──────────────────────────────────────────────────┴────────────┘
```
---

# 6. DuckDB ENUM Type Example

An `ENUM` (Enumeration) is a custom data type that restricts column values to a specific set of allowed text options.

---

### 6.0 Simple Example with ENUM

* Create a Table with an ENUM column:

```sql
memory D CREATE TABLE orders (
      order_id INT NOT NULL,
      amount DECIMAL(10, 2) NOT NULL,
      status ENUM('valid', 'cancelled', 'pending', 'unknown'),
      created_at DATE NOT NULL
);

memory D DESC orders;
┌──────────────────────────────────────────────────────────────────────┐
│                                orders                                │
│                                                                      │
│ order_id   integer                                          not null │
│ amount     decimal                                          not null │
│ status     enum('valid', 'cancelled', 'pending', 'unknown')          │
│ created_at date                                             not null │
└──────────────────────────────────────────────────────────────────────┘
```

* Populate table

```sql
memory D INSERT INTO orders
  VALUES (10, 234.56, 'valid', '2026-03-23');

memory D INSERT INTO orders
  VALUES (20, 500.55, 'pending', '2026-03-29');

memory D INSERT INTO orders
  VALUES (30, 100.22, 'pendinggg', '2026-03-29');
Conversion Error:
Could not convert string 'pendinggg' to UINT8

LINE 3: (30, 100.22, 'pendinggg', '2026-03-29');
                     ^
```

* View Table

```sql
memory D SELECT * FROM orders;
┌──────────┬───────────────┬──────────────────────────────────────────────────┬────────────┐
│ order_id │    amount     │                      status                      │ created_at │
│  int32   │ decimal(10,2) │ enum('valid', 'cancelled', 'pending', 'unknown') │    date    │
├──────────┼───────────────┼──────────────────────────────────────────────────┼────────────┤
│       10 │        234.56 │ valid                                            │ 2026-03-23 │
│       20 │        500.55 │ pending                                          │ 2026-03-29 │
└──────────┴───────────────┴──────────────────────────────────────────────────┴────────────┘
memory D
```

---

### 6.1. Create Custom ENUM Type and Table

First, define the `ENUM` type with the valid choices, 
then use it in a table definition.

```sql
-- Step 1: Create a custom ENUM type for order statuses
CREATE TYPE order_status 
   AS ENUM ('pending', 'shipped', 'delivered', 'cancelled');

-- Step 2: Create a table using the custom ENUM type

CREATE SEQUENCE order_id_seq START 1;

CREATE TABLE customer_orders (
    order_id INTEGER PRIMARY KEY 
       DEFAULT nextval('order_id_seq'),
    customer_name VARCHAR NOT NULL,
    status order_status DEFAULT 'pending'
);
```

---

### 6.2. Insert Valid Rows

Insert rows using values defined in the `order_status` ENUM.

```sql
-- Insert rows with allowed status values
INSERT INTO customer_orders (customer_name, status) 
VALUES 
    ('Alice Smith', 'pending'),
    ('Bob Jones', 'shipped'),
    ('Charlie Brown', 'delivered');
```

### 6.3 Table Contents

```sql
SELECT * FROM customer_orders;
```

| order_id | customer_name | status |
| :--- | :--- | :--- |
| `1` | Alice Smith | `pending` |
| `2` | Bob Jones | `shipped` |
| `3` | Charlie Brown | `delivered` |

---

### 6.4 Triggering a Constraint Error

If you try to insert a value that is **not** part of the `ENUM` list, DuckDB rejects it and throws an error.

```sql
-- Attempt to insert an invalid status value ('processing')
INSERT INTO customer_orders (customer_name, status) 
VALUES ('Diana Prince', 'processing');
```

### 6.5 DuckDB Error Output

> `Conversion Error: Could not convert string 'processing' to ENUM type 'order_status'`

---

### 6.6 Key Benefits of ENUMs for Students

1. **Data Integrity**: Stops spelling errors (e.g., `'shiped'` vs `'shipped'`).
2. **Storage Efficiency**: DuckDB optimizes memory and disk storage by storing small integer keys under the hood while allowing you to query readable text strings.

---

## 7. Summary Checklist for Beginners

| Constraint / Property | Purpose | Example |
| :--- | :--- | :--- |
| `PRIMARY KEY` | Uniquely identifies each record | `id INTEGER PRIMARY KEY` |
| `NOT NULL` | Requires a value (cannot be blank) | `name VARCHAR NOT NULL` |
| `UNIQUE` | Stops duplicate values | `email VARCHAR UNIQUE` |
| `DEFAULT` | Fills in a default value if missing | `country VARCHAR DEFAULT 'USA'` |
| `CHECK` | Verifies a condition is met | `CHECK (age >= 18)` |
| `FOREIGN KEY` | Connects to a primary key in another table | `FOREIGN KEY (author_id) REFERENCES authors(author_id)` |