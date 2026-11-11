# Third Normal Form (3NF) — Examples

A table is in **Third Normal Form (3NF)** when:

1. **It is in 2NF** (in 1NF, and every non-key column depends on the whole key), and
2. **no non-key column depends on another non-key column.**

A chain like `key → X → Y`, where X and Y are both non-key columns, is a
**transitive dependency**. Y is really a fact about X, so it belongs in a table
where X is the key.

This page shows four small examples. The full explanation, and the DuckDB code
for checking a dependency and splitting a table, is in [`3nf_guide.md`](3nf_guide.md).

**The 3NF question, for every non-key column:**
👉 *"Is this a fact about the row's own key, or about **another column** in the row?"*

---

## Example 1: Products and Categories

### ❌ Before: not in 3NF

* **Primary key:** `product_id`

| `product_id` | `product_name` | `category_id` | `category_name` | `category_manager` |
|---|---|---|---|---|
| 1 | Laptop | C1 | Electronics | Rosa |
| 2 | Headphones | C1 | Electronics | Rosa |
| 3 | Desk Chair | C2 | Furniture | Omar |
| 4 | Monitor | C1 | Electronics | Rosa |

**The dependencies:**

* `product_id → product_name, category_id` — direct ✅
* `category_id → category_name, category_manager` — a **non-key** column
  determines other columns ❌
* The chain: `product_id → category_id → category_name, category_manager`

**Why it breaks 3NF:** "Electronics, Rosa" is stored once per electronic product.
If Rosa leaves, three rows must change.

### ✅ After: in 3NF

**Table 1: `categories`** — primary key `category_id`

| `category_id` | `category_name` | `category_manager` |
|---|---|---|
| C1 | Electronics | Rosa |
| C2 | Furniture | Omar |

**Table 2: `products`** — primary key `product_id`;
`category_id` is a foreign key to `categories`

| `product_id` | `product_name` | `category_id` |
|---|---|---|
| 1 | Laptop | C1 |
| 2 | Headphones | C1 |
| 3 | Desk Chair | C2 |
| 4 | Monitor | C1 |

### 🦆 Check it with DuckDB

```sql
CREATE OR REPLACE TABLE products_bad (
    product_id       INT,
    product_name     VARCHAR,
    category_id      VARCHAR,
    category_name    VARCHAR,
    category_manager VARCHAR
);

INSERT INTO products_bad VALUES
(1, 'Laptop',     'C1', 'Electronics', 'Rosa'),
(2, 'Headphones', 'C1', 'Electronics', 'Rosa'),
(3, 'Desk Chair', 'C2', 'Furniture',   'Omar'),
(4, 'Monitor',    'C1', 'Electronics', 'Rosa');

-- Does category_id → category_manager hold? (0 rows = yes, in this data)
SELECT category_id, COUNT(DISTINCT category_manager) AS managers
FROM products_bad
GROUP BY category_id
HAVING COUNT(DISTINCT category_manager) > 1;

-- The 3NF tables
CREATE OR REPLACE TABLE categories AS
SELECT DISTINCT category_id, category_name, category_manager
FROM products_bad;                                         -- 2 rows

CREATE OR REPLACE TABLE products AS
SELECT product_id, product_name, category_id
FROM products_bad;                                         -- 4 rows

-- Products per category, from the 3NF tables
SELECT c.category_name, c.category_manager, COUNT(*) AS products
FROM products p
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name, c.category_manager
ORDER BY products DESC;
-- Electronics | Rosa | 3
-- Furniture   | Omar | 1
```

---

## Example 2: Employees and Departments

### ❌ Before: not in 3NF

* **Primary key:** `emp_id`

| `emp_id` | `emp_name` | `dept_id` | `dept_name` | `dept_building` |
|---|---|---|---|---|
| 1 | Alice | 10 | Engineering | Building A |
| 2 | Bob | 20 | Marketing | Building B |
| 3 | Carlos | 10 | Engineering | Building A |
| 4 | Diana | 30 | Finance | Building C |

**The chain:** `emp_id → dept_id → dept_name, dept_building`

**The anomalies:**

* **Update:** Engineering moves to Building D → change every engineer's row.
* **Insert:** a new department, "Legal", has no employees yet → no row to put it in.
* **Delete:** Diana leaves → we forget that Finance is in Building C.

### ✅ After: in 3NF

**`departments`**(`dept_id`, `dept_name`, `dept_building`)

| `dept_id` | `dept_name` | `dept_building` |
|---|---|---|
| 10 | Engineering | Building A |
| 20 | Marketing | Building B |
| 30 | Finance | Building C |

**`employees`**(`emp_id`, `emp_name`, `dept_id` → `departments`)

| `emp_id` | `emp_name` | `dept_id` |
|---|---|---|
| 1 | Alice | 10 |
| 2 | Bob | 20 |
| 3 | Carlos | 10 |
| 4 | Diana | 30 |

All three anomalies are gone: one row to update, "Legal" can be added to
`departments` alone, and deleting Diana leaves Finance in place.

---

## Example 3: A Chain Without an ID Column (ZIP Codes)

A transitive dependency does not need a column named `..._id`.
Any non-key column can be the middle of the chain.

### ❌ Before: not in 3NF

* **Primary key:** `customer_id`

| `customer_id` | `customer_name` | `zip_code` | `city` | `state` |
|---|---|---|---|---|
| 1 | Alice | 95053 | Santa Clara | CA |
| 2 | Bob | 94301 | Palo Alto | CA |
| 3 | Cara | 95053 | Santa Clara | CA |

**The chain:** `customer_id → zip_code → city, state`
(in the US, a ZIP code belongs to one city and one state).

### ✅ After: in 3NF

**`zip_codes`**(`zip_code`, `city`, `state`)

| `zip_code` | `city` | `state` |
|---|---|---|
| 95053 | Santa Clara | CA |
| 94301 | Palo Alto | CA |

**`customers`**(`customer_id`, `customer_name`, `zip_code` → `zip_codes`)

| `customer_id` | `customer_name` | `zip_code` |
|---|---|---|
| 1 | Alice | 95053 |
| 2 | Bob | 94301 |
| 3 | Cara | 95053 |

> **A real-world note:** many companies keep `city` and `state` in the
> `customers` table anyway. Addresses rarely change, and one less JOIN is
> convenient. That is a deliberate **denormalization**: they know the rule and
> choose to break it. Normalize first, and break the rule only on purpose.

---

## Example 4: A Column Computed from Other Columns

### ❌ Before: not in 3NF

* **Primary key:** `line_id`

| `line_id` | `product` | `quantity` | `unit_price` | `line_total` |
|---|---|---|---|---|
| 1 | Pen | 3 | 2.00 | 6.00 |
| 2 | Paper | 1 | 9.50 | 9.50 |
| 3 | Pen | 10 | 2.00 | 20.00 |

**The dependency:** `(quantity, unit_price) → line_total`.
`line_total` depends on **other non-key columns**, not on the key.
If someone changes `quantity` and forgets `line_total`, the row contradicts itself.

### ✅ After: in 3NF — do not store it, compute it

| `line_id` | `product` | `quantity` | `unit_price` |
|---|---|---|---|
| 1 | Pen | 3 | 2.00 |
| 2 | Paper | 1 | 9.50 |
| 3 | Pen | 10 | 2.00 |

```sql
CREATE OR REPLACE TABLE order_lines (
    line_id    INT PRIMARY KEY,
    product    VARCHAR,
    quantity   INT,
    unit_price DECIMAL(10,2)
);

INSERT INTO order_lines VALUES
(1, 'Pen',   3,  2.00),
(2, 'Paper', 1,  9.50),
(3, 'Pen',   10, 2.00);

-- Compute the total when you need it. It can never be out of date.
SELECT line_id, product, quantity, unit_price,
       quantity * unit_price AS line_total
FROM order_lines
ORDER BY line_id;
-- line totals: 6.00, 9.50, 20.00
```

(A **view** — `CREATE VIEW ... AS SELECT ...` — saves this query under a name,
so everyone computes the total the same way.)

---

## Quick Self-Check

For each table you design, ask:

1. Is it in 2NF? → if not, fix 1NF and 2NF first ([`2nf_guide.md`](2nf_guide.md)).
2. For each non-key column: is it a fact about **this row's key**, or about
   **another column** in the row? → if another column, move it to a table where
   that column is the key.
3. Can the column be **computed** from other columns? → do not store it; compute
   it in a query or a view.

Every non-key column must depend on **the key, the whole key, and nothing but
the key.**

---

## Complete Example: From a Non-3NF Table to 3NF, Step by Step

This last example puts everything together: check the key, find the
transitive dependencies with SQL, split the table with keys and foreign keys,
and prove that nothing was lost. Every result below is real DuckDB output, so
you can run the code and compare.

### The story

A campus food-delivery service keeps one table of deliveries. Each row also
holds the driver's details and the restaurant's details.

### Step 1: Create the table

```sql
CREATE OR REPLACE TABLE deliveries_bad (
    delivery_id     INT,
    delivery_date   DATE,
    driver_id       VARCHAR,
    driver_name     VARCHAR,
    driver_phone    VARCHAR,
    restaurant_id   VARCHAR,
    restaurant_name VARCHAR,
    restaurant_city VARCHAR,
    amount          DECIMAL(6,2)
);

INSERT INTO deliveries_bad VALUES
(501, DATE '2026-11-02', 'D1', 'Sam',  '408-555-1111', 'R1', 'Bronco Tacos', 'Santa Clara', 18.50),
(502, DATE '2026-11-02', 'D2', 'Lina', '408-555-2222', 'R2', 'Pho House',    'San Jose',    24.00),
(503, DATE '2026-11-03', 'D1', 'Sam',  '408-555-1111', 'R2', 'Pho House',    'San Jose',    31.25),
(504, DATE '2026-11-04', 'D1', 'Sam',  '408-555-1111', 'R3', 'Slice Corner', 'Santa Clara', 22.75),
(505, DATE '2026-11-04', 'D2', 'Lina', '408-555-2222', 'R1', 'Bronco Tacos', 'Santa Clara', 12.00);
```

| delivery_id | delivery_date | driver_id | driver_name | driver_phone | restaurant_id | restaurant_name | restaurant_city | amount |
|---|---|---|---|---|---|---|---|---|
| 501 | 2026-11-02 | D1 | Sam | 408-555-1111 | R1 | Bronco Tacos | Santa Clara | 18.50 |
| 502 | 2026-11-02 | D2 | Lina | 408-555-2222 | R2 | Pho House | San Jose | 24.00 |
| 503 | 2026-11-03 | D1 | Sam | 408-555-1111 | R2 | Pho House | San Jose | 31.25 |
| 504 | 2026-11-04 | D1 | Sam | 408-555-1111 | R3 | Slice Corner | Santa Clara | 22.75 |
| 505 | 2026-11-04 | D2 | Lina | 408-555-2222 | R1 | Bronco Tacos | Santa Clara | 12.00 |

### Step 2: Check the key — and why the table is already in 2NF

```sql
SELECT delivery_id, COUNT(*) AS copies
FROM deliveries_bad
GROUP BY delivery_id
HAVING COUNT(*) > 1;            -- 0 rows ✅ delivery_id is unique
```

The key is **one column**, `delivery_id`. So no column can depend on "part" of
the key: the table is in **2NF**. But look at Sam: his name and phone appear 3
times. Something is still wrong.

### Step 3: Find the transitive dependencies with SQL

Ask about each non-key column: *"Is it a fact about the delivery, or about
**another column** in the row?"* Driver details look like facts about
`driver_id`; restaurant details look like facts about `restaurant_id`.
Test both:

```sql
-- Does driver_id determine driver_name and driver_phone?
SELECT driver_id,
       COUNT(DISTINCT driver_name)  AS names,
       COUNT(DISTINCT driver_phone) AS phones
FROM deliveries_bad
GROUP BY driver_id
HAVING COUNT(DISTINCT driver_name) > 1 OR COUNT(DISTINCT driver_phone) > 1;
-- 0 rows → YES: driver_id → driver_name, driver_phone

-- Does restaurant_id determine restaurant_name and restaurant_city?
SELECT restaurant_id,
       COUNT(DISTINCT restaurant_name) AS names,
       COUNT(DISTINCT restaurant_city) AS cities
FROM deliveries_bad
GROUP BY restaurant_id
HAVING COUNT(DISTINCT restaurant_name) > 1 OR COUNT(DISTINCT restaurant_city) > 1;
-- 0 rows → YES: restaurant_id → restaurant_name, restaurant_city
```

`driver_id` and `restaurant_id` are **non-key** columns, so we have two chains:

```
delivery_id → driver_id     → driver_name, driver_phone         ❌ transitive
delivery_id → restaurant_id → restaurant_name, restaurant_city  ❌ transitive
delivery_id → delivery_date, amount                             ✅ direct
```

How much repetition does this cause?

```sql
SELECT driver_id, driver_name, COUNT(*) AS copies
FROM deliveries_bad
GROUP BY driver_id, driver_name
ORDER BY driver_id;
```

| driver_id | driver_name | copies |
|---|---|---|
| D1 | Sam | 3 |
| D2 | Lina | 2 |

Sam's phone is stored 3 times. If he gets a new phone, 3 rows must change.

### Step 4: Plan the 3NF tables

Each chain's **middle column** becomes the key of a new table. It also stays in
`deliveries` as a **foreign key**, so the tables stay linked.

| Table | Key | Other columns |
|---|---|---|
| `drivers` | **driver_id** | driver_name, driver_phone |
| `restaurants` | **restaurant_id** | restaurant_name, restaurant_city |
| `deliveries` | **delivery_id** | delivery_date, driver_id → drivers, restaurant_id → restaurants, amount |

### Step 5: Create the tables with keys, then fill them

Create the "parent" tables (`drivers`, `restaurants`) first: the foreign keys in
`deliveries` must point to tables that already exist.

```sql
CREATE OR REPLACE TABLE drivers (
    driver_id    VARCHAR PRIMARY KEY,
    driver_name  VARCHAR,
    driver_phone VARCHAR
);
INSERT INTO drivers
SELECT DISTINCT driver_id, driver_name, driver_phone
FROM deliveries_bad;                          -- 2 rows

CREATE OR REPLACE TABLE restaurants (
    restaurant_id   VARCHAR PRIMARY KEY,
    restaurant_name VARCHAR,
    restaurant_city VARCHAR
);
INSERT INTO restaurants
SELECT DISTINCT restaurant_id, restaurant_name, restaurant_city
FROM deliveries_bad;                          -- 3 rows

CREATE OR REPLACE TABLE deliveries (
    delivery_id   INT PRIMARY KEY,
    delivery_date DATE,
    driver_id     VARCHAR REFERENCES drivers(driver_id),
    restaurant_id VARCHAR REFERENCES restaurants(restaurant_id),
    amount        DECIMAL(6,2)
);
INSERT INTO deliveries
SELECT delivery_id, delivery_date, driver_id, restaurant_id, amount
FROM deliveries_bad;                          -- 5 rows
```

**`drivers`**

| driver_id | driver_name | driver_phone |
|---|---|---|
| D1 | Sam | 408-555-1111 |
| D2 | Lina | 408-555-2222 |

**`restaurants`**

| restaurant_id | restaurant_name | restaurant_city |
|---|---|---|
| R1 | Bronco Tacos | Santa Clara |
| R2 | Pho House | San Jose |
| R3 | Slice Corner | Santa Clara |

**`deliveries`**

| delivery_id | delivery_date | driver_id | restaurant_id | amount |
|---|---|---|---|---|
| 501 | 2026-11-02 | D1 | R1 | 18.50 |
| 502 | 2026-11-02 | D2 | R2 | 24.00 |
| 503 | 2026-11-03 | D1 | R2 | 31.25 |
| 504 | 2026-11-04 | D1 | R3 | 22.75 |
| 505 | 2026-11-04 | D2 | R1 | 12.00 |

### Step 6: Prove that nothing was lost

JOIN the three tables back together, and subtract the original with `EXCEPT`.
An empty result means the JOIN rebuilt **exactly** the old rows.

```sql
SELECT d.delivery_id, d.delivery_date,
       d.driver_id, dr.driver_name, dr.driver_phone,
       d.restaurant_id, r.restaurant_name, r.restaurant_city,
       d.amount
FROM deliveries d
JOIN drivers     dr ON d.driver_id     = dr.driver_id
JOIN restaurants r  ON d.restaurant_id = r.restaurant_id
EXCEPT
SELECT * FROM deliveries_bad;
-- 0 rows ✅
```

### Step 7: Enjoy the benefits

**One fact, one row.** Sam gets a new phone — one `UPDATE`, one row:

```sql
UPDATE drivers SET driver_phone = '408-555-9999' WHERE driver_id = 'D1';   -- 1 row

SELECT dr.driver_name, dr.driver_phone,
       COUNT(*)      AS deliveries,
       SUM(d.amount) AS total_amount
FROM deliveries d
JOIN drivers dr ON d.driver_id = dr.driver_id
GROUP BY dr.driver_name, dr.driver_phone
ORDER BY dr.driver_name;
```

| driver_name | driver_phone | deliveries | total_amount |
|---|---|---|---|
| Lina | 408-555-2222 | 2 | 36.00 |
| Sam | 408-555-9999 | 3 | 72.50 |

All 3 of Sam's deliveries show the new phone through the JOIN.

**The foreign key guards the data.** A delivery by a driver who does not exist
is refused:

```sql
INSERT INTO deliveries VALUES (506, DATE '2026-11-05', 'D9', 'R1', 15.00);
```

```
Constraint Error: Violates foreign key constraint because key "driver_id: D9"
does not exist in the referenced table
```

In the old table, nothing would stop a row with a made-up driver.

### What we did

1. Checked the key (`delivery_id`, unique) — one column, so already 2NF.
2. Asked of every non-key column: a fact about the **key**, or about **another
   column**? Tested each guess with `GROUP BY … HAVING COUNT(DISTINCT …) > 1`.
3. Found two chains: `delivery_id → driver_id → …` and
   `delivery_id → restaurant_id → …`.
4. Gave each middle column (`driver_id`, `restaurant_id`) its own table, and
   kept it in `deliveries` as a foreign key.
5. Proved the split is lossless with `JOIN … EXCEPT`.

Every non-key column now depends on **the key, the whole key, and nothing but
the key.**

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
