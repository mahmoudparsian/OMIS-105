# DuckDB ENUM Type Example

An `ENUM` (Enumeration) is a custom data 
type that restricts column values to a 
specific set of allowed text options.

---

## 1. Create the ENUM Type and Table

First, define the `ENUM` type with the valid 
choices, then use it in a table definition.


```sql
-- Step 1: Create a custom ENUM type for order statuses
CREATE TYPE order_status AS 
  ENUM ('pending', 'shipped', 'delivered', 'cancelled');

-- Step 2: Create a sequence
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

Insert rows using values defined in the 
`order_status` ENUM.

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

## 3. Triggering a Constraint Error

If you try to insert a value that is **not** 
part of the `ENUM` list, DuckDB rejects it and 
throws an error.

```sql
-- Attempt to insert an invalid status value ('processing')
INSERT INTO customer_orders (customer_name, status) 
VALUES ('Diana Prince', 'processing');
```

### DuckDB Error Output

> `Conversion Error: Could not convert string 'processing' to ENUM type 'order_status'`

---

## Key Benefits of ENUMs for Students

1. **Data Integrity**: Stops spelling errors (e.g., `'shiped'` vs `'shipped'`).
2. **Storage Efficiency**: DuckDB optimizes memory and disk storage by storing small integer keys under the hood while allowing you to query readable text strings.