# Mastering ENUMs in DuckDB

Now that you have the basics of SQL in DuckDB down (like `CREATE TABLE`, `INSERT`, and `SELECT`), let’s look at a powerful feature for maintaining clean and efficient data: **ENUM types**.

## What is an ENUM?

An **ENUM** (short for "enumeration") is a custom data type that consists of a static, ordered list of allowed text values.

Think of it as a **drop-down menu** for your database column. Instead of allowing *any* string to be entered into a column, an ENUM restricts inputs strictly to a predefined set of options.

## Why Use ENUMs?

1. **Data Integrity:** Prevents typos or invalid entries (e.g., prevents saving `'Pendng'` or `'in-progress'` when you expect `'PENDING'`).

2. **Storage Efficiency:** DuckDB stores ENUM values internally as integers, which saves disk space and speeds up queries compared to storing repeated text strings.

3. **Ordering:** DuckDB remembers the order in which you defined your ENUM values, making comparisons like `status < 'COMPLETED'` possible.

---

## Option 1: Creating an ENUM Data Type First (Recommended)

Before using an ENUM in a table, you can create it as a reusable data type using the `CREATE TYPE` statement.

### Step 1: Define the ENUM Type

```sql
-- Create an ENUM type for order statuses
CREATE TYPE order_status AS ENUM ('PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED');
```

### Step 2: Create a Table using the Type

```sql
-- Create a simple orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_name VARCHAR,
    status order_status,
    total_amount DECIMAL(10, 2)
);
```

---

## Option 2: Using Inline ENUMs (Without Creating a Type)

If you don't want to define a standalone type (for example, if the ENUM is only used once in your entire schema), you can define the ENUM **inline** directly inside the `CREATE TABLE` statement.

### Inline ENUM Example:

```sql
-- Define the ENUM directly inside the column definition
CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    issue_description VARCHAR,
    priority ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')
);
```

### Inserting and Validating Inline ENUMs:

Inline ENUMs behave identically to explicit ENUM types regarding validation and ordering:

```sql
-- Valid inserts
INSERT INTO tickets VALUES
    (1, 'Password reset', 'LOW'),
    (2, 'Database outage', 'CRITICAL');

-- INVALID insert - This will cause an error!
INSERT INTO tickets VALUES
    (3, 'Feature request', 'URGENT');
```

**DuckDB Output:**
> `Conversion Error: Could not convert string 'URGENT' to 'ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')'`

---

## Step 3: Querying with ENUMs

Whether you created a named type or used an inline ENUM, querying works the same way.

### 1. Basic Filtering

Filtering works just like string columns:

```sql
SELECT * 
FROM tickets 
WHERE priority = 'CRITICAL';
```

| ticket_id | issue_description | priority |
| :--- | :--- | :--- |
| 2 | Database outage | CRITICAL |

### 2. Leveraging ENUM Ordering

Because DuckDB preserves the order of ENUM elements defined in the schema:

* `'LOW'` (0)
* `'MEDIUM'` (1)
* `'HIGH'` (2)
* `'CRITICAL'` (3)

You can use logical comparison operators (`<`, `>`, `<=`, `>=`):

```sql
-- Find all high-priority or critical tickets
SELECT * 
FROM tickets 
WHERE priority >= 'HIGH';
```

| ticket_id | issue_description | priority |
| :--- | :--- | :--- |
| 2 | Database outage | CRITICAL |

---

## Summary Checklist

* **Named ENUM:** Use `CREATE TYPE type_name AS ENUM (...)` when you want to reuse the ENUM across multiple tables.
* **Inline ENUM:** Use `column_name ENUM(...)` inside `CREATE TABLE` for single-use columns without creating a separate type.
* **Validate:** DuckDB automatically rejects values not in the defined list.
* **Compare:** ENUMs respect the positional order in which their values were defined.