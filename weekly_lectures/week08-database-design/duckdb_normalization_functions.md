# DuckDB Normalization Functions Guide <br> (1NF, 2NF, 3NF)

This guide demonstrates the most useful DuckDB 
functions for restructuring unnormalized data 
into First, Second, and Third Normal Forms using 
concrete table schemas and sample data.

---

## 1. First Normal Form (1NF): <br> Eliminating Repeating Groups & Arrays

**Core Rule:** All column values must be atomic (indivisible), 
and there must be no repeating groups or arrays.

### Sample Input Schema: Unnormalized Orders

```sql
CREATE TABLE raw_orders (
    order_id INT,
    customer_name VARCHAR,
    items_ordered VARCHAR -- Non-atomic comma-separated list
);

INSERT INTO raw_orders VALUES
(101, 'Alice Smith', 'Laptop,Mouse,Keyboard'),
(102, 'Bob Jones', 'Monitor,HDMI Cable');
```

### Functions Used: `string_split()` and `unnest()`

*   `string_split(string, delimiter)`: Converts a 
    delimited text string into a native DuckDB `LIST`.

*   `unnest(list)`: Explodes a `LIST` container 
    into individual, separate rows.

### 1NF Query Example

```sql
-- Combining both functions to explode the non-atomic tags into individual atomic rows
CREATE TABLE orders_1nf AS
SELECT 
    order_id,
    customer_name,
    unnest(string_split(items_ordered, ',')) AS item_name
FROM raw_orders;

-- View Output
SELECT * FROM orders_1nf;
```

### Resulting Data Row Transformation

**Before:**

| order_id | customer_name | items_ordered |
| :--- | :--- | :--- |
| 101 | Alice Smith | Laptop,Mouse,Keyboard |

**After (1NF compliant):**

| order_id | customer_name | item_name |
| :--- | :--- | :--- |
| 101 | Alice Smith | Laptop |
| 101 | Alice Smith | Mouse |
| 101 | Alice Smith | Keyboard |

---

## 2. Second Normal Form (2NF): Eliminating Partial Dependencies

**Core Rule:** The data must be in 1NF, and all non-key attributes must depend on the *entire* primary key (no partial dependencies on a composite key).

### Sample Input Schema: 1NF with Composite Key Dependency Issue
In this table, the primary key is a composite of `(order_id, item_id)`. However, `customer_phone` depends *only* on `order_id` (a partial dependency), not the item.

```sql
CREATE TABLE orders_composite_1nf (
    order_id INT,
    item_id INT,
    item_name VARCHAR,
    customer_phone VARCHAR -- Only dependent on order_id!
);

INSERT INTO orders_composite_1nf VALUES
(101, 1, 'Laptop', '555-1234'),
(101, 2, 'Mouse', '555-1234'),
(102, 1, 'Monitor', '555-5678');
```

### Functions/Clauses Used: `DISTINCT` and `hash()` / `ROW_NUMBER()`
*   `DISTINCT`: Isolates unique records to separate entities safely.
*   `hash(columns)` or `ROW_NUMBER() OVER ()`: Generates clean surrogate keys or unique IDs for the newly decoupled tables.

### 2NF Query Example
To achieve 2NF, we split the partial dependency out into a separate parent table (`orders_summary`) and leave the multi-item details in a child table (`order_items`).

```sql
-- 1. Isolate the order entity to remove partial dependency
CREATE TABLE orders_2nf AS
SELECT DISTINCT 
    order_id,
    customer_phone
FROM orders_composite_1nf;

-- 2. Isolate the items entity
CREATE TABLE order_items_2nf AS
SELECT 
    order_id,
    item_id,
    item_name
FROM orders_composite_1nf;
```

### Resulting Data Row Transformation

**`orders_2nf` Table:**

| order_id | customer_phone |
| :--- | :--- |
| 101 | 555-1234 |
| 102 | 555-5678 |


**`order_items_2nf` Table:**

| order_id | item_id | item_name |
| :--- | :--- | :--- |
| 101 | 1 | Laptop |
| 101 | 2 | Mouse |
| 102 | 1 | Monitor |

---

## 3. Third Normal Form (3NF): Eliminating Transitive Dependencies

**Core Rule:** The data must be in 2NF, and no 
non-key attribute can be transitively dependent 
on the primary key (no non-key column should 
determine another non-key column).

### Sample Input Schema: 2NF with Transitive Dependency Issue
Here, `order_id` (Primary Key) determines `store_id`. 
However, `store_id` (a non-key) determines `store_city` 
(another non-key). This is a transitive dependency 
(`order_id` -> `store_id` -> `store_city`).

```sql
CREATE TABLE orders_transitive_2nf (
    order_id INT,
    store_id INT,
    store_city VARCHAR -- Dependent on store_id, not directly order_id
);

INSERT INTO orders_transitive_2nf VALUES
(101, 10, 'New York'),
(102, 20, 'Los Angeles'),
(103, 10, 'New York'); -- Redundant tracking of store details
```

### Functions/Clauses Used: `SELECT DISTINCT` and `QUALIFY`
*   `QUALIFY`: Filters window function outputs inline. 
*   Excellent if your raw input data is messy/redundant 
    and you need to select exactly one deterministic 
    lookup row during normalization.

### 3NF Query Example
To remove the transitive dependency, we separate the 
`stores` lookup tracking from the core `orders` table.

```sql
-- 1. Deduplicate the transitive relationship using 
--    QUALIFY to guarantee 1 row per store
CREATE TABLE stores_3nf AS
SELECT 
    store_id,
    store_city
FROM orders_transitive_2nf
QUALIFY ROW_NUMBER() OVER (PARTITION BY store_id ORDER BY order_id) = 1;

-- 2. Maintain a clean foreign key 
--    relationship in the main table
CREATE TABLE orders_3nf AS
SELECT 
    order_id,
    store_id
FROM orders_transitive_2nf;
```

### Resulting Data Row Transformation

**`stores_3nf` Table:**

| store_id | store_city |
| :--- | :--- |
| 10 | New York |
| 20 | Los Angeles |

**`orders_3nf` Table:**

| order_id | store_id |
| :--- | :--- |
| 101 | 10 |
| 102 | 20 |
| 103 | 10 |
