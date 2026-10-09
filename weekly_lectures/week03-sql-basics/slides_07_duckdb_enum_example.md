# DuckDB ENUM Type Example

An `ENUM` (short for *enumeration*) is a data
type that allows **only** the values in a fixed
list of text options.

---

## 1. Create the ENUM Type and Table

First, define the `ENUM` type with the valid
choices. Then use it in a table definition, just
like `INTEGER` or `VARCHAR`.

```sql
-- Step 1: Create a custom ENUM type for order statuses
CREATE TYPE order_status AS 
  ENUM ('pending', 'shipped', 'delivered', 'cancelled');

-- Step 2: Create a sequence (for the auto-increment order_id)
CREATE SEQUENCE order_id_seq START 1;

-- Step 3: Create a table using the custom ENUM type
CREATE TABLE customer_orders (
    order_id INTEGER PRIMARY KEY 
        DEFAULT nextval('order_id_seq'),
    customer_name VARCHAR NOT NULL,
    status order_status DEFAULT 'pending'
);
```

---

## 2. Insert Valid Rows

Insert rows using values from the
`order_status` list. We leave out `order_id`:
the sequence fills it in.

```sql
-- Insert rows with allowed status values
INSERT INTO customer_orders (customer_name, status) 
VALUES 
    ('Alice Smith', 'pending'),
    ('Bob Jones', 'shipped'),
    ('Charlie Brown', 'delivered');
```

### Table Contents

```sql
SELECT * FROM customer_orders;
```

| order_id | customer_name | status |
| :--- | :--- | :--- |
| `1` | Alice Smith | `pending` |
| `2` | Bob Jones | `shipped` |
| `3` | Charlie Brown | `delivered` |

---

## 3. Inserting a Value That Is Not in the List

If you insert a value that is **not** in the
`ENUM` list, DuckDB rejects the row.

```sql
-- Attempt to insert an invalid status value ('processing')
INSERT INTO customer_orders (customer_name, status) 
VALUES ('Diana Prince', 'processing');
```

### DuckDB Error Output

> `Conversion Error: Could not convert string 'processing' to UINT8`

The message is not very friendly. It means:
*"`'processing'` is not in the ENUM list."*
(DuckDB stores each ENUM value as a small number,
`UINT8`, behind the scenes.)

To see the allowed values:

```sql
SELECT enum_range(NULL::order_status);
-- [pending, shipped, delivered, cancelled]
```

---

## Why Use ENUMs?

1. **Data integrity:** stops spelling mistakes, such as `'shiped'` instead of `'shipped'`.
2. **Storage efficiency:** DuckDB stores each value as a small number behind the scenes, but you still read and write normal text.
3. **The default helps too:** a new order with no status gets `'pending'` automatically.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
