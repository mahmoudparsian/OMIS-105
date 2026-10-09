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
| **`SEQUENCE`** | Database object | A number counter. Used with `DEFAULT nextval(...)`, it gives new rows the numbers 1, 2, 3, ... (DuckDB's way to make an **auto-increment** column — see `slides_09`). |
| **`NOT NULL`** | Constraint | Ensures a column always has a value (it cannot be `NULL`). |
| **`UNIQUE`** | Constraint | Prevents duplicate values in a column. |
| **`CHECK`** | Constraint | Enforces specific rules on column values (e.g., price must be greater than zero). |
| **`DEFAULT`** | Column option | Fills in a value automatically when the `INSERT` does not provide one. |
| **`FOREIGN KEY`** | Constraint | Links rows in one table to matching rows in another table. |

---

## 2. Creating the Tables (DDL)

Let's build three related tables: `authors`, `books`, and `orders`.

###  1. Authors Table
```sql
-- Demonstrates: PRIMARY KEY, SEQUENCE (auto-increment),
--               NOT NULL, UNIQUE, DEFAULT
CREATE SEQUENCE author_id_seq START 1;

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
-- Demonstrates: FOREIGN KEY, CHECK constraints,
--               DECIMAL type
CREATE SEQUENCE book_id_seq START 1;

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY        
      DEFAULT nextval('book_id_seq'),
    title VARCHAR NOT NULL,
    author_id INTEGER NOT NULL,
    price DECIMAL(6, 2) NOT NULL CHECK (price > 0), -- Price must be positive
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0), -- Stock cannot be negative
    published_date DATE,
    
    -- Foreign Key: author_id must match an author_id in authors
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);
```

### 3. Orders Table
```sql
-- Demonstrates: BOOLEAN values, DEFAULT dates,
--               a short-form (inline) Foreign Key

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
Notice that we **never** give `author_id`,
`book_id`, or `order_id`. The sequences fill them
in for us.

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

Here is what our tables look like after inserting rows.
The ID columns were filled in by the sequences.

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

`is_shipped` and `order_date` came from their
`DEFAULT` values. (`order_date` will show the day
*you* run the query.)

---

## 5. What Happens When Rules Are Broken?

DuckDB checks your rules (constraints) every time you insert or update data. If a rule is broken, DuckDB cancels the statement, no row is saved, and you see an error message.

### Example 1: `CHECK` Constraint Error
Trying to add a book with a negative price:

```sql
INSERT INTO books (title, author_id, price) 
VALUES ('Broken Book', 1, -5.00);
```
**DuckDB Error Output:**
> `Constraint Error: CHECK constraint failed on table books with expression CHECK((price > 0))`

---

### Example 2: `UNIQUE` Constraint Error
Trying to reuse an author email address:

```sql
INSERT INTO authors (first_name, last_name, email) 
VALUES ('Jane', 'Doe', 'jk@example.com');
```
**DuckDB Error Output:**
> `Constraint Error: Duplicate key "email: jk@example.com" violates unique constraint.`

---

### Example 3: `FOREIGN KEY` Constraint Error
Trying to order a book that does not exist in the database (`book_id = 999`):

```sql
INSERT INTO orders (book_id, quantity) 
VALUES (999, 1);
```
**DuckDB Error Output:**
> `Constraint Error: Violates foreign key constraint because key "book_id: 999" does not exist in the referenced table`

---

## 6. The `ENUM` Data Type

An `ENUM` (short for *enumeration*) is a data type
that allows **only** the values in a fixed list,
for example `'pending'`, `'shipped'`, `'delivered'`.

There are two ways to use it:

* **6.1** — write the list directly in the column definition.
* **6.2** — create a **named** `ENUM` type once, then reuse it.

---

### 6.1 Simple Example: an Inline ENUM Column

We use a new table name, `simple_orders`, because
`orders` already exists from Section 2.

```sql
memory D CREATE TABLE simple_orders (
             order_id INTEGER NOT NULL,
             amount DECIMAL(10, 2) NOT NULL,
             status ENUM('valid', 'cancelled', 'pending', 'unknown'),
             created_at DATE NOT NULL
         );

memory D DESCRIBE simple_orders;
┌──────────────────────────────────────────────────────────────────────┐
│                            simple_orders                             │
│                                                                      │
│ order_id   integer                                          not null │
│ amount     decimal                                          not null │
│ status     enum('valid', 'cancelled', 'pending', 'unknown')          │
│ created_at date                                             not null │
└──────────────────────────────────────────────────────────────────────┘
```

Insert two valid rows and one invalid row:

```sql
memory D INSERT INTO simple_orders
         VALUES (10, 234.56, 'valid', '2026-03-23');

memory D INSERT INTO simple_orders
         VALUES (20, 500.55, 'pending', '2026-03-29');

memory D INSERT INTO simple_orders
         VALUES (30, 100.22, 'pendinggg', '2026-03-29');
Conversion Error:
Could not convert string 'pendinggg' to UINT8
```

The message is not very friendly. It means:
*"`'pendinggg'` is not in the ENUM list."*
(DuckDB stores each ENUM value as a small number,
`UINT8`, behind the scenes.)

Only the two valid rows were saved:

```sql
memory D SELECT * FROM simple_orders;
┌──────────┬───────────────┬──────────────────────────────────────────────────┬────────────┐
│ order_id │    amount     │                      status                      │ created_at │
│  int32   │ decimal(10,2) │ enum('valid', 'cancelled', 'pending', 'unknown') │    date    │
├──────────┼───────────────┼──────────────────────────────────────────────────┼────────────┤
│       10 │        234.56 │ valid                                            │ 2026-03-23 │
│       20 │        500.55 │ pending                                          │ 2026-03-29 │
└──────────┴───────────────┴──────────────────────────────────────────────────┴────────────┘
```

---

### 6.2 Create a Named ENUM Type, Then Use It

First, define the `ENUM` type with the valid
choices. Then use it in a table definition, just
like `INTEGER` or `VARCHAR`.

```sql
-- Step 1: Create a named ENUM type for order statuses
CREATE TYPE order_status
   AS ENUM ('pending', 'shipped', 'delivered', 'cancelled');

-- Step 2: Create a sequence for the auto-increment ID
--         (a new name: order_id_seq is already used by orders)
CREATE SEQUENCE customer_order_id_seq START 1;

-- Step 3: Create a table that uses the ENUM type
CREATE TABLE customer_orders (
    order_id INTEGER PRIMARY KEY
       DEFAULT nextval('customer_order_id_seq'),
    customer_name VARCHAR NOT NULL,
    status order_status DEFAULT 'pending'
);
```

---

### 6.3 Insert Valid Rows

Insert rows using values from the `order_status` list.

```sql
-- Insert rows with allowed status values
INSERT INTO customer_orders (customer_name, status)
VALUES
    ('Alice Smith', 'pending'),
    ('Bob Jones', 'shipped'),
    ('Charlie Brown', 'delivered');

SELECT * FROM customer_orders;
```

| order_id | customer_name | status |
| :--- | :--- | :--- |
| `1` | Alice Smith | `pending` |
| `2` | Bob Jones | `shipped` |
| `3` | Charlie Brown | `delivered` |

---

### 6.4 Inserting a Value That Is Not in the List

If you insert a value that is **not** in the
`ENUM` list, DuckDB rejects the row.

```sql
-- 'processing' is not in the order_status list
INSERT INTO customer_orders (customer_name, status)
VALUES ('Diana Prince', 'processing');
```

**DuckDB Error Output:**
> `Conversion Error: Could not convert string 'processing' to UINT8`

---

### 6.5 Why Use ENUMs?

1. **Data integrity:** stops spelling mistakes, such as `'shiped'` instead of `'shipped'`.
2. **Storage efficiency:** DuckDB stores each value as a small number behind the scenes, but you still read and write normal text.

---

## 7. Summary Checklist for Beginners

| Constraint / Option | Purpose | Example |
| :--- | :--- | :--- |
| `PRIMARY KEY` | Uniquely identifies each row | `id INTEGER PRIMARY KEY` |
| `SEQUENCE` + `DEFAULT nextval(...)` | Auto-increment: numbers new rows 1, 2, 3, ... | `id INTEGER PRIMARY KEY DEFAULT nextval('id_seq')` |
| `NOT NULL` | Requires a value (cannot be `NULL`) | `name VARCHAR NOT NULL` |
| `UNIQUE` | Stops duplicate values | `email VARCHAR UNIQUE` |
| `DEFAULT` | Fills in a value when none is given | `country VARCHAR DEFAULT 'USA'` |
| `CHECK` | Requires a condition to be true | `CHECK (age >= 18)` |
| `FOREIGN KEY` | Must match a key in another table | `FOREIGN KEY (author_id) REFERENCES authors(author_id)` |
| `ENUM` | Allows only values from a fixed list | `status ENUM('pending', 'shipped')` |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
