# DuckDB Normalization Functions Guide <br> (1NF, 2NF, 3NF)

This guide shows the most useful DuckDB functions and clauses for turning
unnormalized data into First, Second, and Third Normal Form. Each section
has a small table, the SQL that fixes it, and the result.

The step-by-step explanations are in the guides:
[`1nf_guide.md`](1nf_guide.md), [`2nf_guide.md`](2nf_guide.md), and
[`3nf_guide.md`](3nf_guide.md).

| Normal form | Problem | DuckDB tools |
| :--- | :--- | :--- |
| **1NF** | a list in one cell | `string_split()` + `unnest()` |
| **1NF** | repeating columns (`phone_1`, `phone_2`) | `UNPIVOT` (or `UNION ALL`) |
| **2NF, 3NF** | a fact stored many times | `GROUP BY … HAVING COUNT(DISTINCT …) > 1` to check, then `CREATE TABLE … AS SELECT DISTINCT` to split |
| **all** | "did we lose anything?" | `JOIN` the new tables, then `EXCEPT` the old one |

---

## 1. First Normal Form (1NF): <br> Lists in a Cell and Repeating Groups

**Core rules:** one value per cell (no lists), no repeating groups of columns,
and a primary key.

### 1a. A list in one cell

#### Sample input: unnormalized orders

```sql
CREATE OR REPLACE TABLE raw_orders (
    order_id      INT,
    customer_name VARCHAR,
    items_ordered VARCHAR      -- a comma-separated list: not atomic
);

INSERT INTO raw_orders VALUES
(101, 'Alice Smith', 'Laptop,Mouse,Keyboard'),
(102, 'Bob Jones',   'Monitor,HDMI Cable');
```

#### Functions used: `string_split()` and `unnest()`

* `string_split(text, separator)` turns delimited text into a DuckDB `LIST`.
* `unnest(list)` turns a `LIST` into separate rows, one row per item.

(More detail: [`duckdb_string_split_example.md`](duckdb_string_split_example.md).)

#### 1NF query

```sql
-- Split each list into one row per item
CREATE OR REPLACE TABLE orders_1nf AS
SELECT
    order_id,
    customer_name,
    unnest(string_split(items_ordered, ',')) AS item_name
FROM raw_orders;

SELECT * FROM orders_1nf;
```

**Before:**

| order_id | customer_name | items_ordered |
| :--- | :--- | :--- |
| 101 | Alice Smith | Laptop,Mouse,Keyboard |
| 102 | Bob Jones | Monitor,HDMI Cable |

**After (1NF):** primary key (`order_id`, `item_name`)

| order_id | customer_name | item_name |
| :--- | :--- | :--- |
| 101 | Alice Smith | Laptop |
| 101 | Alice Smith | Mouse |
| 101 | Alice Smith | Keyboard |
| 102 | Bob Jones | Monitor |
| 102 | Bob Jones | HDMI Cable |

2 rows became 5. Notice that `customer_name` is now repeated — 1NF allows
that, and **2NF/3NF** fix it later.

### 1b. Repeating columns

#### Sample input

```sql
CREATE OR REPLACE TABLE raw_contacts (
    customer_id INT,
    phone_1     VARCHAR,
    phone_2     VARCHAR,
    phone_3     VARCHAR    -- phone_1, phone_2, phone_3: a repeating group
);

INSERT INTO raw_contacts VALUES
(1, '555-0101', '555-0102', NULL),
(2, '555-0201', NULL,       NULL);
```

#### Clause used: `UNPIVOT`

* `UNPIVOT` turns columns into rows. `NAME` is the new column that holds the
  old column's name; `VALUE` is the new column that holds its value.
  `UNPIVOT` skips `NULL` values for you.

#### 1NF query

```sql
CREATE OR REPLACE TABLE customer_phones AS
SELECT customer_id, phone
FROM (
    UNPIVOT raw_contacts
    ON phone_1, phone_2, phone_3
    INTO NAME phone_slot VALUE phone
);

SELECT * FROM customer_phones ORDER BY customer_id, phone;
```

**After (1NF):** primary key (`customer_id`, `phone`)

| customer_id | phone |
| :--- | :--- |
| 1 | 555-0101 |
| 1 | 555-0102 |
| 2 | 555-0201 |

The three `NULL` cells are gone, and a customer can now have any number of phones.
(`UNION ALL`, one `SELECT` per phone column, does the same in any database —
see [`1nf_guide.md`](1nf_guide.md).)

---

## 2. Second Normal Form (2NF): Eliminating Partial Dependencies

**Core rule:** the table is in 1NF, and every non-key column depends on the
**entire** primary key (no partial dependencies on a composite key).

### Sample input: a 1NF table with a partial dependency

The primary key is (`order_id`, `item_id`): `item_id` is the line number
inside an order. `item_name` needs both columns (line 1 of order 101 is a
Laptop; line 1 of order 102 is a Monitor). But `customer_phone` depends
**only** on `order_id` — a partial dependency.

```sql
CREATE OR REPLACE TABLE orders_composite_1nf (
    order_id       INT,
    item_id        INT,
    item_name      VARCHAR,
    customer_phone VARCHAR     -- depends only on order_id!
);

INSERT INTO orders_composite_1nf VALUES
(101, 1, 'Laptop',  '555-1234'),
(101, 2, 'Mouse',   '555-1234'),
(102, 1, 'Monitor', '555-5678');
```

### Clauses used: `GROUP BY … HAVING` and `SELECT DISTINCT`

* `GROUP BY order_id HAVING COUNT(DISTINCT customer_phone) > 1` **checks** the
  dependency. 0 rows means no order has two phones, so
  `order_id → customer_phone` holds in this data.
* `CREATE TABLE … AS SELECT DISTINCT` builds the new table and keeps **one copy**
  of each repeated fact.

### 2NF query

```sql
-- 0. Check the dependency first: does any order have 2+ phones?
SELECT order_id, COUNT(DISTINCT customer_phone) AS phones
FROM orders_composite_1nf
GROUP BY order_id
HAVING COUNT(DISTINCT customer_phone) > 1;
-- 0 rows → order_id → customer_phone holds

-- 1. Move the partial dependency to a table keyed by order_id
CREATE OR REPLACE TABLE orders_2nf AS
SELECT DISTINCT
    order_id,
    customer_phone
FROM orders_composite_1nf;

-- 2. Keep the columns that need the whole key
CREATE OR REPLACE TABLE order_items_2nf AS
SELECT
    order_id,
    item_id,
    item_name
FROM orders_composite_1nf;
```

**`orders_2nf`** (key: `order_id`)

| order_id | customer_phone |
| :--- | :--- |
| 101 | 555-1234 |
| 102 | 555-5678 |

**`order_items_2nf`** (key: `order_id`, `item_id`; `order_id` is a foreign key)

| order_id | item_id | item_name |
| :--- | :--- | :--- |
| 101 | 1 | Laptop |
| 101 | 2 | Mouse |
| 102 | 1 | Monitor |

> **Need a new ID column?** If the "thing" you split out has no ID yet (for
> example, only a `category_name`), number the rows with
> `ROW_NUMBER() OVER (ORDER BY category_name) AS category_id`.
> (`ROW_NUMBER` is a Week 9 topic.) Avoid `hash()` for keys: it makes very
> large numbers, and two different values can, rarely, get the same hash.

---

## 3. Third Normal Form (3NF): Eliminating Transitive Dependencies

**Core rule:** the table is in 2NF, and no non-key column determines another
non-key column.

### Sample input: a 2NF table with a transitive dependency

`order_id` (the primary key) determines `store_id`. But `store_id`, a
**non-key** column, determines `store_city`. That chain,
`order_id → store_id → store_city`, is a transitive dependency.

```sql
CREATE OR REPLACE TABLE orders_transitive_2nf (
    order_id   INT,
    store_id   INT,
    store_city VARCHAR         -- depends on store_id, not directly on order_id
);

INSERT INTO orders_transitive_2nf VALUES
(101, 10, 'New York'),
(102, 20, 'Los Angeles'),
(103, 10, 'New York');         -- store 10's city is stored twice
```

### Clauses used: `GROUP BY … HAVING` and `SELECT DISTINCT`

The same two tools as 2NF: check the dependency, then split.

### 3NF query

```sql
-- 0. Check: does any store have 2+ cities?
SELECT store_id, COUNT(DISTINCT store_city) AS cities
FROM orders_transitive_2nf
GROUP BY store_id
HAVING COUNT(DISTINCT store_city) > 1;
-- 0 rows → store_id → store_city holds

-- 1. Move the store facts to their own table
CREATE OR REPLACE TABLE stores_3nf AS
SELECT DISTINCT
    store_id,
    store_city
FROM orders_transitive_2nf;

-- 2. Keep store_id in orders as a foreign key
CREATE OR REPLACE TABLE orders_3nf AS
SELECT
    order_id,
    store_id
FROM orders_transitive_2nf;

-- 3. Prove nothing was lost: rebuild the old table and compare
SELECT o.order_id, o.store_id, s.store_city
FROM orders_3nf o
JOIN stores_3nf s ON o.store_id = s.store_id
EXCEPT
SELECT * FROM orders_transitive_2nf;
-- 0 rows → the JOIN gives back exactly the original rows
```

**`stores_3nf`** (key: `store_id`)

| store_id | store_city |
| :--- | :--- |
| 10 | New York |
| 20 | Los Angeles |

**`orders_3nf`** (key: `order_id`; `store_id` is a foreign key)

| order_id | store_id |
| :--- | :--- |
| 101 | 10 |
| 102 | 20 |
| 103 | 10 |

> ⚠️ **What if the check in step 0 returns rows?** Then the data disagrees with
> itself — for example, store 10 is "New York" in one row and "Newark" in
> another. `SELECT DISTINCT` would give store 10 **two** rows, and `store_id`
> would not be a key. **Fix the data first** (find out which city is right).
> Do not hide the problem by keeping "the first row" with
> `QUALIFY ROW_NUMBER() OVER (PARTITION BY store_id …) = 1` (a Week 9
> ranking tool): that silently throws away one of the two cities.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
