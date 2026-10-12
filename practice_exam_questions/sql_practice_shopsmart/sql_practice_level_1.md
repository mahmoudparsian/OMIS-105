# ShopSmart SQL Practice — Level 1 (Weeks 6-8)

	Database design, keys & constraints,
	normalization, query plans & indexes,
	and transactions — on the ShopSmart
	e-commerce database.

	All queries and results in this file were
	validated with DuckDB v1.5.5.


## 1. The ShopSmart Database

| Table | Rows | Primary key | Foreign keys |
|-------|-----:|-------------|--------------|
| `categories` | 8 | `category_id` | |
| `customers` | 40 | `customer_id` | |
| `suppliers` | 10 | `supplier_id` | |
| `products` | 64 | `product_id` | `category_id` → `categories` |
| `orders` | 200 | `order_id` | `customer_id` → `customers` |
| `order_items` | 607 | `item_id` | `order_id` → `orders`, `product_id` → `products` |
| `product_suppliers` | 90 | (`product_id`, `supplier_id`) | `product_id` → `products`, `supplier_id` → `suppliers` |
| `reviews` | 150 | `review_id` | `product_id` → `products`, `customer_id` → `customers` |
| `shipping` | 141 | `shipping_id` | `order_id` → `orders` (UNIQUE: one shipment per order) |
| `orders_denormalized` | 100 | none (on purpose) | none — the "before normalization" table |

The full schema (with all `CHECK`, `UNIQUE`, and `NOT NULL` constraints)
is in [`create_shopsmart_db.sql`](./create_shopsmart_db.sql).


## 2. Build the Database

From this folder, run:

```bash
duckdb shopsmart.duckdb < create_shopsmart_db.sql
```

Then open it:

```bash
duckdb shopsmart.duckdb
```

Notes:

* Run the questions **in order** in the same database: a few of them
  (Q29–Q31, Q38–Q50) create, change, or drop practice objects that later
  questions use.
* Questions that change data either use their own practice tables
  (`gift_cards`, `price_history`) or end with `ROLLBACK`, so the ShopSmart
  data stays the same. To start over at any time, re-run
  `create_shopsmart_db.sql`.
* Questions marked `-- expected error` are **supposed** to fail — the
  error message is the answer.
* Long outputs are truncated to 10 rows by the DuckDB CLI (`.maxrows 10`);
  the total row count is shown at the bottom of each result.


## 3. SQL Practice Queries


## Part A — Warm-up: JOINs Across the Schema (Week 5 refresher)


### Q1. List every product with its category name (INNER JOIN)

```sql
SELECT p.product_id,
       p.product_name,
       c.category_name,
       p.price
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
ORDER BY p.product_id;
```

**Result:**

```text
┌────────────┬──────────────────┬────────────────┬───────────────┐
│ product_id │   product_name   │ category_name  │     price     │
│   int32    │     varchar      │    varchar     │ decimal(10,2) │
├────────────┼──────────────────┼────────────────┼───────────────┤
│          1 │ Smartphone X12   │ Electronics    │        321.52 │
│          2 │ Laptop Pro 15    │ Electronics    │        372.07 │
│          3 │ Wireless Earbuds │ Electronics    │        115.49 │
│          4 │ USB-C Hub        │ Electronics    │         55.74 │
│          5 │ Tablet Air       │ Electronics    │        446.63 │
│          · │     ·            │      ·         │           ·   │
│          · │     ·            │      ·         │           ·   │
│          · │     ·            │      ·         │           ·   │
│         60 │ Trail Mix        │ Food & Grocery │        114.59 │
│         61 │ Protein Bars     │ Food & Grocery │         20.90 │
│         62 │ Olive Oil Extra  │ Food & Grocery │         28.20 │
│         63 │ Honey Jar        │ Food & Grocery │         66.21 │
│         64 │ Almond Butter    │ Food & Grocery │         60.79 │
└────────────┴──────────────────┴────────────────┴───────────────┘
  64 rows (10 shown)                                   4 columns
```

### Q2. Show each order with the customer's full name

```sql
SELECT o.order_id,
       c.first_name || ' ' || c.last_name AS customer_name,
       o.order_date,
       o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_id;
```

**Result:**

```text
┌──────────┬───────────────┬────────────┬────────────┐
│ order_id │ customer_name │ order_date │   status   │
│  int32   │    varchar    │    date    │  varchar   │
├──────────┼───────────────┼────────────┼────────────┤
│        1 │ Eva Garcia    │ 2024-12-28 │ processing │
│        2 │ Eva Garcia    │ 2024-01-17 │ cancelled  │
│        3 │ Gina Turner   │ 2024-05-01 │ completed  │
│        4 │ Noah Harris   │ 2024-10-03 │ completed  │
│        5 │ Kira Evans    │ 2024-10-22 │ completed  │
│        · │     ·         │     ·      │     ·      │
│        · │     ·         │     ·      │     ·      │
│        · │     ·         │     ·      │     ·      │
│      196 │ Karen Moore   │ 2024-06-17 │ completed  │
│      197 │ Sam Allen     │ 2024-12-05 │ completed  │
│      198 │ Joel Parker   │ 2024-01-19 │ completed  │
│      199 │ Quinn Hall    │ 2024-06-14 │ completed  │
│      200 │ Zach Adams    │ 2024-09-20 │ cancelled  │
└──────────┴───────────────┴────────────┴────────────┘
  200 rows (10 shown)                      4 columns
```

### Q3. Find the products that have never been reviewed (LEFT JOIN … IS NULL)

```sql
SELECT p.product_id,
       p.product_name
FROM products p
LEFT JOIN reviews r ON p.product_id = r.product_id
WHERE r.review_id IS NULL
ORDER BY p.product_id;
```

**Result:**

```text
┌────────────┬──────────────────┐
│ product_id │   product_name   │
│   int32    │     varchar      │
├────────────┼──────────────────┤
│          3 │ Wireless Earbuds │
│         21 │ Wool Sweater     │
│         31 │ Wall Clock       │
│         33 │ Yoga Mat         │
│         56 │ Nail Kit         │
│         59 │ Dark Chocolate   │
│         60 │ Trail Mix        │
│         61 │ Protein Bars     │
└────────────┴──────────────────┘
```

### Q4. Count the orders with and without a shipping record, by order status

```sql
SELECT o.status,
       COUNT(*)            AS num_orders,
       COUNT(s.order_id)   AS with_shipping,
       COUNT(*) - COUNT(s.order_id) AS without_shipping
FROM orders o
LEFT JOIN shipping s ON o.order_id = s.order_id
GROUP BY o.status
ORDER BY o.status;
```

**Result:**

```text
┌────────────┬────────────┬───────────────┬──────────────────┐
│   status   │ num_orders │ with_shipping │ without_shipping │
│  varchar   │   int64    │     int64     │      int64       │
├────────────┼────────────┼───────────────┼──────────────────┤
│ cancelled  │         29 │             0 │               29 │
│ completed  │        115 │           115 │                0 │
│ processing │         30 │             0 │               30 │
│ shipped    │         26 │            26 │                0 │
└────────────┴────────────┴───────────────┴──────────────────┘
```

### Q5. Find the 5 products with the most suppliers (many-to-many through a junction table)

```sql
SELECT p.product_name,
       COUNT(ps.supplier_id) AS num_suppliers
FROM products p
JOIN product_suppliers ps ON p.product_id = ps.product_id
GROUP BY p.product_name
ORDER BY num_suppliers DESC, p.product_name
LIMIT 5;
```

**Result:**

```text
┌─────────────────┬───────────────┐
│  product_name   │ num_suppliers │
│     varchar     │     int64     │
├─────────────────┼───────────────┤
│ Almond Butter   │             2 │
│ Art Kit         │             2 │
│ Blender Pro     │             2 │
│ Building Blocks │             2 │
│ Card Game       │             2 │
└─────────────────┴───────────────┘
```

### Q6. Show the line items of order 10 with product and category names (3-table join)

```sql
SELECT oi.item_id,
       p.product_name,
       c.category_name,
       oi.quantity,
       oi.unit_price,
       oi.quantity * oi.unit_price AS line_total
FROM order_items oi
JOIN products   p ON oi.product_id  = p.product_id
JOIN categories c ON p.category_id  = c.category_id
WHERE oi.order_id = 10
ORDER BY oi.item_id;
```

**Result:**

```text
┌─────────┬─────────────────┬────────────────┬──────────┬───────────────┬───────────────┐
│ item_id │  product_name   │ category_name  │ quantity │  unit_price   │  line_total   │
│  int32  │     varchar     │    varchar     │  int32   │ decimal(10,2) │ decimal(18,2) │
├─────────┼─────────────────┼────────────────┼──────────┼───────────────┼───────────────┤
│      34 │ Organic Granola │ Food & Grocery │        1 │         62.91 │         62.91 │
└─────────┴─────────────────┴────────────────┴──────────┴───────────────┴───────────────┘
```

### Q7. Find customers who live in the same city as at least one supplier

```sql
SELECT DISTINCT c.first_name, c.last_name, c.city, c.state
FROM customers c
JOIN suppliers s ON c.city = s.city AND c.state = s.state
ORDER BY c.city, c.last_name;
```

**Result:**

```text
┌────────────┬───────────┬──────────┬─────────┐
│ first_name │ last_name │   city   │  state  │
│  varchar   │  varchar  │ varchar  │ varchar │
├────────────┼───────────┼──────────┼─────────┤
│ Grace      │ Anderson  │ Austin   │ TX      │
│ Leo        │ Jackson   │ Austin   │ TX      │
│ Bob        │ Johnson   │ Austin   │ TX      │
│ Finn       │ Roberts   │ Austin   │ TX      │
│ Cora       │ Carter    │ Boston   │ MA      │
│  ·         │  ·        │   ·      │ ·       │
│  ·         │  ·        │   ·      │ ·       │
│  ·         │  ·        │   ·      │ ·       │
│ Carol      │ Lee       │ San Jose │ CA      │
│ Ivy        │ Thomas    │ San Jose │ CA      │
│ Zach       │ Adams     │ Seattle  │ WA      │
│ Blake      │ Nelson    │ Seattle  │ WA      │
│ Henry      │ Taylor    │ Seattle  │ WA      │
└────────────┴───────────┴──────────┴─────────┘
  37 rows (10 shown)                4 columns
```

### Q8. List pairs of customers who live in the same city (self-join)

`c1.customer_id < c2.customer_id` keeps each pair only once and stops a
customer from being paired with themself.

```sql
SELECT c1.city,
       c1.first_name || ' ' || c1.last_name AS customer_1,
       c2.first_name || ' ' || c2.last_name AS customer_2
FROM customers c1
JOIN customers c2
  ON c1.city = c2.city AND
     c1.customer_id < c2.customer_id
ORDER BY c1.city, customer_1, customer_2;
```

**Result:**

```text
┌──────────┬────────────────┬────────────────┐
│   city   │   customer_1   │   customer_2   │
│ varchar  │    varchar     │    varchar     │
├──────────┼────────────────┼────────────────┤
│ Austin   │ Bob Johnson    │ Finn Roberts   │
│ Austin   │ Bob Johnson    │ Grace Anderson │
│ Austin   │ Bob Johnson    │ Leo Jackson    │
│ Austin   │ Grace Anderson │ Finn Roberts   │
│ Austin   │ Grace Anderson │ Leo Jackson    │
│   ·      │     ·          │     ·          │
│   ·      │     ·          │     ·          │
│   ·      │     ·          │     ·          │
│ San Jose │ Ivy Thomas     │ Sam Allen      │
│ San Jose │ Quinn Hall     │ Sam Allen      │
│ Seattle  │ Henry Taylor   │ Blake Nelson   │
│ Seattle  │ Henry Taylor   │ Zach Adams     │
│ Seattle  │ Zach Adams     │ Blake Nelson   │
└──────────┴────────────────┴────────────────┘
  87 rows (10 shown)               3 columns
```


## Part B — Keys, Constraints & Relationships (Week 6)


### Q9. List every table and its number of columns (information_schema)

```sql
SELECT table_name,
       COUNT(*) AS num_columns
FROM information_schema.columns
WHERE table_schema = 'main'
GROUP BY table_name
ORDER BY table_name;
```

**Result:**

```text
┌─────────────────────┬─────────────┐
│     table_name      │ num_columns │
│       varchar       │    int64    │
├─────────────────────┼─────────────┤
│ categories          │           3 │
│ customers           │           7 │
│ order_items         │           5 │
│ orders              │           5 │
│ orders_denormalized │          13 │
│ product_suppliers   │           3 │
│ products            │           5 │
│ reviews             │           6 │
│ shipping            │           6 │
│ suppliers           │           6 │
└─────────────────────┴─────────────┘
  10 rows                 2 columns
```

### Q10. Show the column names and data types of the `orders` table

```sql
DESCRIBE orders;
```

**Result:**

```text
┌───────────────────────────────┐
│            orders             │
│                               │
│ order_id     integer not null │
│ customer_id  integer not null │
│ order_date   date    not null │
│ status       varchar not null │
│ total_amount decimal          │
└───────────────────────────────┘
```

### Q11. List all PRIMARY KEY and FOREIGN KEY constraints in the database

```sql
SELECT table_name,
       constraint_type,
       constraint_text
FROM duckdb_constraints()
WHERE constraint_type IN ('PRIMARY KEY', 'FOREIGN KEY')
ORDER BY table_name, constraint_type DESC, constraint_text;
```

**Result:**

```text
┌─────────────┬─────────────────┬─────────────────────────────────────────────────────────────┐
│ table_name  │ constraint_type │                       constraint_text                       │
│   varchar   │     varchar     │                           varchar                           │
├─────────────┼─────────────────┼─────────────────────────────────────────────────────────────┤
│ categories  │ PRIMARY KEY     │ PRIMARY KEY(category_id)                                    │
│ customers   │ PRIMARY KEY     │ PRIMARY KEY(customer_id)                                    │
│ order_items │ PRIMARY KEY     │ PRIMARY KEY(item_id)                                        │
│ order_items │ FOREIGN KEY     │ FOREIGN KEY (order_id) REFERENCES orders(order_id)          │
│ order_items │ FOREIGN KEY     │ FOREIGN KEY (product_id) REFERENCES products(product_id)    │
│    ·        │      ·          │                            ·                                │
│    ·        │      ·          │                            ·                                │
│    ·        │      ·          │                            ·                                │
│ reviews     │ FOREIGN KEY     │ FOREIGN KEY (customer_id) REFERENCES customers(customer_id) │
│ reviews     │ FOREIGN KEY     │ FOREIGN KEY (product_id) REFERENCES products(product_id)    │
│ shipping    │ PRIMARY KEY     │ PRIMARY KEY(shipping_id)                                    │
│ shipping    │ FOREIGN KEY     │ FOREIGN KEY (order_id) REFERENCES orders(order_id)          │
│ suppliers   │ PRIMARY KEY     │ PRIMARY KEY(supplier_id)                                    │
└─────────────┴─────────────────┴─────────────────────────────────────────────────────────────┘
  18 rows (10 shown)                use .last to show entire result                 3 columns
```

### Q12. Show all constraints on `product_suppliers`. Why is its primary key made of two columns?

A product can have many suppliers and a supplier can supply many products,
so neither `product_id` nor `supplier_id` is unique on its own — only the
**pair** is. This is the classic junction table of a many-to-many relationship.

```sql
SELECT constraint_type,
       constraint_column_names,
       constraint_text
FROM duckdb_constraints()
WHERE table_name = 'product_suppliers'
ORDER BY constraint_type DESC;
```

**Result:**

```text
┌─────────────────┬───────────────────────────┬─────────────────────────────────────────────────────────────┐
│ constraint_type │  constraint_column_names  │                       constraint_text                       │
│     varchar     │         varchar[]         │                           varchar                           │
├─────────────────┼───────────────────────────┼─────────────────────────────────────────────────────────────┤
│ PRIMARY KEY     │ [product_id, supplier_id] │ PRIMARY KEY(product_id, supplier_id)                        │
│ NOT NULL        │ [product_id]              │ NOT NULL                                                    │
│ NOT NULL        │ [supplier_id]             │ NOT NULL                                                    │
│ FOREIGN KEY     │ [product_id]              │ FOREIGN KEY (product_id) REFERENCES products(product_id)    │
│ FOREIGN KEY     │ [supplier_id]             │ FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) │
└─────────────────┴───────────────────────────┴─────────────────────────────────────────────────────────────┘
```

### Q13. Try to insert a category whose `category_id` already exists (PRIMARY KEY)

```sql
-- expected error
INSERT INTO categories VALUES (1, 'Garden', 'Plants and tools');
```

**Result:**

```text
Constraint Error:
Duplicate key "category_id: 1" violates primary key constraint.
```

### Q14. Try to insert an order for a customer that does not exist (FOREIGN KEY)

```sql
-- expected error
INSERT INTO orders VALUES (999, 999, DATE '2025-01-15', 'processing', 50.00);
```

**Result:**

```text
Constraint Error:
Violates foreign key constraint because key "customer_id: 999" does not exist in the referenced table
```

### Q15. Try to insert a review with a rating of 6 (CHECK)

```sql
-- expected error
INSERT INTO reviews VALUES (999, 1, 1, 6, 'Amazing!', DATE '2025-01-15');
```

**Result:**

```text
Constraint Error:
CHECK constraint failed on table reviews with expression CHECK((rating BETWEEN 1 AND 5))
```

### Q16. Try to delete a customer who has orders (FOREIGN KEY protects the child rows)

```sql
-- expected error
DELETE FROM customers WHERE customer_id = 1;
```

**Result:**

```text
Constraint Error:
Violates foreign key constraint because key "customer_id: 1" is still referenced by a foreign key in a different table. If this is an unexpected constraint violation, please refer to our foreign key limitations in the documentation
```

### Q17. Use the data to confirm the cardinality of two relationships

`customers → orders` is one-to-many (a customer can have many orders);
`orders → shipping` is one-to-one (an order has at most one shipment).

```sql
SELECT 'orders per customer' AS relationship,
       MAX(n) AS max_per_parent
FROM (SELECT customer_id, COUNT(*) AS n FROM orders GROUP BY customer_id)
UNION ALL
SELECT 'shipments per order',
       MAX(n)
FROM (SELECT order_id, COUNT(*) AS n FROM shipping GROUP BY order_id);
```

**Result:**

```text
┌─────────────────────┬────────────────┐
│    relationship     │ max_per_parent │
│       varchar       │     int64      │
├─────────────────────┼────────────────┤
│ orders per customer │              9 │
│ shipments per order │              1 │
└─────────────────────┴────────────────┘
```

### Q18. Could `reviews` have a UNIQUE (customer_id, product_id) constraint? Check the data first

If any customer reviewed the same product more than once, the constraint
could not be added without first cleaning the data.

```sql
SELECT customer_id,
       product_id,
       COUNT(*) AS num_reviews
FROM reviews
GROUP BY customer_id, product_id
HAVING COUNT(*) > 1
ORDER BY customer_id, product_id;
```

**Result:**

```text
┌─────────────┬────────────┬─────────────┐
│ customer_id │ product_id │ num_reviews │
│    int32    │   int32    │    int64    │
├─────────────┼────────────┼─────────────┤
│           6 │         36 │           2 │
│           7 │         12 │           2 │
│           9 │         26 │           2 │
│          20 │         18 │           2 │
└─────────────┴────────────┴─────────────┘
```


## Part C — Normalization with `orders_denormalized` (Week 6)


### Q19. How many rows, orders, customers, and products are in `orders_denormalized`?

```sql
SELECT COUNT(*)                    AS num_rows,
       COUNT(DISTINCT order_id)    AS num_orders,
       COUNT(DISTINCT customer_id) AS num_customers,
       COUNT(DISTINCT product_id)  AS num_products
FROM orders_denormalized;
```

**Result:**

```text
┌──────────┬────────────┬───────────────┬──────────────┐
│ num_rows │ num_orders │ num_customers │ num_products │
│  int64   │   int64    │     int64     │    int64     │
├──────────┼────────────┼───────────────┼──────────────┤
│      100 │         30 │            20 │           51 │
└──────────┴────────────┴───────────────┴──────────────┘
```

### Q20. Check the functional dependency `product_id → product_name, category_name`

A dependency X → Y holds if every value of X maps to exactly one value of Y.
An empty result means no violations: the dependency holds in this data.

```sql
SELECT product_id,
       COUNT(DISTINCT product_name)  AS names,
       COUNT(DISTINCT category_name) AS categories
FROM orders_denormalized
GROUP BY product_id
HAVING COUNT(DISTINCT product_name) > 1 OR
       COUNT(DISTINCT category_name) > 1;
```

**Result:**

```text
┌────────────┬───────┬────────────┐
│ product_id │ names │ categories │
│   int32    │ int64 │   int64    │
└────────────┴───────┴────────────┘
              0 rows             
```

### Q21. Does `customer_city → customer_id` hold? Show the counterexamples

```sql
SELECT customer_city,
       COUNT(DISTINCT customer_id) AS num_customers
FROM orders_denormalized
GROUP BY customer_city
HAVING COUNT(DISTINCT customer_id) > 1
ORDER BY num_customers DESC, customer_city;
```

**Result:**

```text
┌───────────────┬───────────────┐
│ customer_city │ num_customers │
│    varchar    │     int64     │
├───────────────┼───────────────┤
│ Boston        │             5 │
│ Portland      │             4 │
│ Denver        │             2 │
│ San Francisco │             2 │
│ Seattle       │             2 │
└───────────────┴───────────────┘
```

### Q22. Show that `order_id` alone is not a key of `orders_denormalized`, but (`order_id`, `product_id`) is

```sql
SELECT COUNT(*)                                   AS num_rows,
       COUNT(DISTINCT order_id)                   AS distinct_order_id,
       COUNT(DISTINCT (order_id, product_id))     AS distinct_order_product
FROM orders_denormalized;
```

**Result:**

```text
┌──────────┬───────────────────┬────────────────────────┐
│ num_rows │ distinct_order_id │ distinct_order_product │
│  int64   │       int64       │         int64          │
├──────────┼───────────────────┼────────────────────────┤
│      100 │                30 │                    100 │
└──────────┴───────────────────┴────────────────────────┘
```

### Q23. Demonstrate an update anomaly (inside a transaction that is rolled back)

Customer 5's email is stored in several rows. Updating only one of them
leaves the table contradicting itself.

```sql
BEGIN TRANSACTION;

UPDATE orders_denormalized
SET customer_email = 'eva.new@email.com'
WHERE customer_id = 5 AND order_id = 1 AND product_id = 60;

SELECT customer_id,
       customer_email,
       COUNT(*) AS num_rows
FROM orders_denormalized
WHERE customer_id = 5
GROUP BY customer_id, customer_email;

ROLLBACK;
```

**Result:**

```text
BEGIN TRANSACTION;

UPDATE orders_denormalized
SET customer_email = 'eva.new@email.com'
WHERE customer_id = 5 AND order_id = 1 AND product_id = 60;

SELECT customer_id,
       customer_email,
       COUNT(*) AS num_rows
FROM orders_denormalized
WHERE customer_id = 5
GROUP BY customer_id, customer_email;
┌─────────────┬──────────────────────┬──────────┐
│ customer_id │    customer_email    │ num_rows │
│    int32    │       varchar        │  int64   │
├─────────────┼──────────────────────┼──────────┤
│           5 │ eva.new@email.com    │        1 │
│           5 │ eva.garcia@email.com │        9 │
└─────────────┴──────────────────────┴──────────┘

ROLLBACK;
```

### Q24. Count how many times each category name is stored in `orders_denormalized` (redundancy)

In the normalized schema, each name is stored exactly once (in `categories`).

```sql
SELECT category_name,
       COUNT(*) AS times_stored
FROM orders_denormalized
GROUP BY category_name
ORDER BY times_stored DESC, category_name;
```

**Result:**

```text
┌────────────────┬──────────────┐
│ category_name  │ times_stored │
│    varchar     │    int64     │
├────────────────┼──────────────┤
│ Food & Grocery │           18 │
│ Sports         │           17 │
│ Beauty         │           14 │
│ Toys           │           12 │
│ Home & Kitchen │           11 │
│ Books          │           10 │
│ Clothing       │           10 │
│ Electronics    │            8 │
└────────────────┴──────────────┘
```

### Q25. Check that the customer data in `orders_denormalized` agrees with the normalized `customers` table (EXCEPT)

`EXCEPT` returns the rows of the first query that are not in the second;
an empty result means every denormalized customer row is consistent.

```sql
SELECT DISTINCT customer_id, customer_name, customer_email, customer_city
FROM orders_denormalized
EXCEPT
SELECT customer_id, first_name || ' ' || last_name, email, city
FROM customers;
```

**Result:**

```text
┌─────────────┬───────────────┬────────────────┬───────────────┐
│ customer_id │ customer_name │ customer_email │ customer_city │
│    int32    │    varchar    │    varchar     │    varchar    │
└─────────────┴───────────────┴────────────────┴───────────────┘
                             0 rows                           
```


## Part D — Query Plans, Indexes & Performance (Week 7)


### Q26. Show the query plan for a filter on `orders.status`

DuckDB reads the table with a `SEQ_SCAN` and applies the filter during the
scan. Notice that only the columns the query needs are listed under
`Projections` — DuckDB is a columnar database.

```sql
EXPLAIN
SELECT order_id, total_amount
FROM orders
WHERE status = 'cancelled';
```

**Result:**

```text
┌─────────────────────────────┐
│┌───────────────────────────┐│
││       Physical Plan       ││
│└───────────────────────────┘│
└─────────────────────────────┘
┌───────────────────────────┐
│          SEQ_SCAN         │
│    ────────────────────   │
│           Table:          │
│   shopsmart.main.orders   │
│                           │
│   Type: Sequential Scan   │
│                           │
│        Projections:       │
│          order_id         │
│        total_amount       │
│                           │
│          Filters:         │
│     status='cancelled'    │
│                           │
│          ~50 rows         │
└───────────────────────────┘
```

### Q27. Show the query plan for a primary-key lookup on `customers`

Even with a primary key (which DuckDB backs with an index), the plan for a
40-row table is still a `SEQ_SCAN`: scanning a tiny table is cheaper than
using an index. Indexes pay off on large tables and very selective filters.

```sql
EXPLAIN
SELECT *
FROM customers
WHERE customer_id = 7;
```

**Result:**

```text
┌─────────────────────────────┐
│┌───────────────────────────┐│
││       Physical Plan       ││
│└───────────────────────────┘│
└─────────────────────────────┘
┌───────────────────────────┐
│          SEQ_SCAN         │
│    ────────────────────   │
│           Table:          │
│  shopsmart.main.customers │
│                           │
│   Type: Sequential Scan   │
│                           │
│        Projections:       │
│        customer_id        │
│         first_name        │
│         last_name         │
│           email           │
│            city           │
│           state           │
│         join_date         │
│                           │
│          Filters:         │
│       customer_id=7       │
│                           │
│           ~1 row          │
└───────────────────────────┘
```

### Q28. Show the query plan for a 3-table join. Which join algorithm does DuckDB use?

```sql
EXPLAIN
SELECT c.category_name,
       SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN products   p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name;
```

**Result:**

```text
┌─────────────────────────────┐
│┌───────────────────────────┐│
││       Physical Plan       ││
│└───────────────────────────┘│
└─────────────────────────────┘
┌───────────────────────────┐
│         PROJECTION        │
│    ────────────────────   │
│__internal_decompress_strin│
│           g(#0)           │
│             #1            │
│                           │
│          ~4 rows          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│    ────────────────────   │
│         Groups: #0        │
│    Aggregates: sum(#1)    │
│                           │
│          ~4 rows          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│       category_name       │
│          quantity         │
│                           │
│         ~566 rows         │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│             #0            │
│__internal_compress_string_│
│        uhugeint(#1)       │
│                           │
│         ~566 rows         │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         HASH_JOIN         │
│    ────────────────────   │
│      Join Type: INNER     │
│                           │
│        Conditions:        ├──────────────┐
│  product_id = product_id  │              │
│                           │              │
│         ~566 rows         │              │
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│          SEQ_SCAN         ││         HASH_JOIN         │
│    ────────────────────   ││    ────────────────────   │
│           Table:          ││      Join Type: INNER     │
│ shopsmart.main.order_items││                           │
│                           ││        Conditions:        │
│   Type: Sequential Scan   ││ category_id = category_id │
│                           ││                           ├──────────────┐
│        Projections:       ││                           │              │
│         product_id        ││                           │              │
│          quantity         ││                           │              │
│                           ││                           │              │
│         ~607 rows         ││          ~56 rows         │              │
└───────────────────────────┘└─────────────┬─────────────┘              │
                             ┌─────────────┴─────────────┐┌─────────────┴─────────────┐
                             │          SEQ_SCAN         ││          SEQ_SCAN         │
                             │    ────────────────────   ││    ────────────────────   │
                             │           Table:          ││           Table:          │
                             │  shopsmart.main.products  ││ shopsmart.main.categories │
                             │                           ││                           │
                             │   Type: Sequential Scan   ││   Type: Sequential Scan   │
                             │                           ││                           │
                             │        Projections:       ││        Projections:       │
                             │         product_id        ││        category_id        │
                             │        category_id        ││       category_name       │
                             │                           ││                           │
                             │          ~64 rows         ││          ~8 rows          │
                             └───────────────────────────┘└───────────────────────────┘
```

### Q29. Create an index on `reviews(product_id)` and list the indexes in the database

`IF NOT EXISTS` lets you re-run the statement without an error.

```sql
CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);

SELECT index_name, table_name, is_unique, sql
FROM duckdb_indexes()
ORDER BY index_name;
```

**Result:**

```text
CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);

SELECT index_name, table_name, is_unique, sql
FROM duckdb_indexes()
ORDER BY index_name;
┌─────────────────────┬────────────┬───────────┬──────────────────────────────────────────────────────────┐
│     index_name      │ table_name │ is_unique │                           sql                            │
│       varchar       │  varchar   │  boolean  │                         varchar                          │
├─────────────────────┼────────────┼───────────┼──────────────────────────────────────────────────────────┤
│ idx_reviews_product │ reviews    │ false     │ CREATE INDEX idx_reviews_product ON reviews(product_id); │
└─────────────────────┴────────────┴───────────┴──────────────────────────────────────────────────────────┘
```

### Q30. Create a UNIQUE index on `suppliers(email)`, then try to insert a duplicate email

```sql
-- expected error
CREATE UNIQUE INDEX IF NOT EXISTS idx_suppliers_email ON suppliers(email);

INSERT INTO suppliers
VALUES (11, 'Copy Cat LLC', 'techworld@supply.com', 'Reno', 'NV', DATE '2025-01-01');
```

**Result:**

```text
-- expected error
CREATE UNIQUE INDEX IF NOT EXISTS idx_suppliers_email ON suppliers(email);

INSERT INTO suppliers
VALUES (11, 'Copy Cat LLC', 'techworld@supply.com', 'Reno', 'NV', DATE '2025-01-01');
Constraint Error:
Duplicate key "email: techworld@supply.com" violates unique constraint.
```

### Q31. Drop both indexes and confirm they are gone

```sql
DROP INDEX IF EXISTS idx_reviews_product;
DROP INDEX IF EXISTS idx_suppliers_email;

SELECT COUNT(*) AS num_indexes
FROM duckdb_indexes();
```

**Result:**

```text
DROP INDEX IF EXISTS idx_reviews_product;
DROP INDEX IF EXISTS idx_suppliers_email;

SELECT COUNT(*) AS num_indexes
FROM duckdb_indexes();
┌─────────────┐
│ num_indexes │
│    int64    │
├─────────────┤
│           0 │
└─────────────┘
```

### Q32. Rewrite a filter so the column is not wrapped in a function (sargable predicate)

Both queries count the orders placed in March 2024. The second compares the
raw `order_date` column to a range, which lets the database use min/max
statistics (and indexes) to skip data instead of computing a function on
every row.

solution-1 (function on the column — avoid):

```sql
SELECT COUNT(*) AS march_2024_orders
FROM orders
WHERE YEAR(order_date) = 2024 AND MONTH(order_date) = 3;
```

**Result:**

```text
┌───────────────────┐
│ march_2024_orders │
│       int64       │
├───────────────────┤
│                14 │
└───────────────────┘
```

solution-2 (range on the raw column — preferred):

```sql
SELECT COUNT(*) AS march_2024_orders
FROM orders
WHERE order_date >= DATE '2024-03-01' AND
      order_date <  DATE '2024-04-01';
```

**Result:**

```text
┌───────────────────┐
│ march_2024_orders │
│       int64       │
├───────────────────┤
│                14 │
└───────────────────┘
```

### Q33. Find the customers who reviewed an Electronics product: three equivalent queries

All three return the same customers. `EXISTS` can stop at the first match,
and the `JOIN` version needs `DISTINCT` because a customer may have several
matching reviews.

solution-1 (IN):

```sql
SELECT customer_id, first_name, last_name
FROM customers
WHERE customer_id IN (
    SELECT r.customer_id
    FROM reviews r
    JOIN products p ON r.product_id = p.product_id
    WHERE p.category_id = 1
)
ORDER BY customer_id;
```

**Result:**

```text
┌─────────────┬────────────┬───────────┐
│ customer_id │ first_name │ last_name │
│    int32    │  varchar   │  varchar  │
├─────────────┼────────────┼───────────┤
│           3 │ Carol      │ Lee       │
│           6 │ Frank      │ Martinez  │
│           9 │ Ivy        │ Thomas    │
│          12 │ Leo        │ Jackson   │
│          19 │ Sam        │ Allen     │
│           · │  ·         │   ·       │
│           · │  ·         │   ·       │
│           · │  ·         │   ·       │
│          29 │ Cora       │ Carter    │
│          31 │ Elena      │ Perez     │
│          36 │ Joel       │ Parker    │
│          37 │ Kira       │ Evans     │
│          40 │ Omar       │ Stewart   │
└─────────────┴────────────┴───────────┘
  14 rows (10 shown)         3 columns
```

solution-2 (EXISTS):

```sql
SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM reviews r
    JOIN products p ON r.product_id = p.product_id
    WHERE p.category_id = 1 AND
          r.customer_id = c.customer_id
)
ORDER BY c.customer_id;
```

**Result:**

```text
┌─────────────┬────────────┬───────────┐
│ customer_id │ first_name │ last_name │
│    int32    │  varchar   │  varchar  │
├─────────────┼────────────┼───────────┤
│           3 │ Carol      │ Lee       │
│           6 │ Frank      │ Martinez  │
│           9 │ Ivy        │ Thomas    │
│          12 │ Leo        │ Jackson   │
│          19 │ Sam        │ Allen     │
│           · │  ·         │   ·       │
│           · │  ·         │   ·       │
│           · │  ·         │   ·       │
│          29 │ Cora       │ Carter    │
│          31 │ Elena      │ Perez     │
│          36 │ Joel       │ Parker    │
│          37 │ Kira       │ Evans     │
│          40 │ Omar       │ Stewart   │
└─────────────┴────────────┴───────────┘
  14 rows (10 shown)         3 columns
```

solution-3 (JOIN + DISTINCT):

```sql
SELECT DISTINCT c.customer_id, c.first_name, c.last_name
FROM customers c
JOIN reviews  r ON r.customer_id = c.customer_id
JOIN products p ON r.product_id  = p.product_id
WHERE p.category_id = 1
ORDER BY c.customer_id;
```

**Result:**

```text
┌─────────────┬────────────┬───────────┐
│ customer_id │ first_name │ last_name │
│    int32    │  varchar   │  varchar  │
├─────────────┼────────────┼───────────┤
│           3 │ Carol      │ Lee       │
│           6 │ Frank      │ Martinez  │
│           9 │ Ivy        │ Thomas    │
│          12 │ Leo        │ Jackson   │
│          19 │ Sam        │ Allen     │
│           · │  ·         │   ·       │
│           · │  ·         │   ·       │
│           · │  ·         │   ·       │
│          29 │ Cora       │ Carter    │
│          31 │ Elena      │ Perez     │
│          36 │ Joel       │ Parker    │
│          37 │ Kira       │ Evans     │
│          40 │ Omar       │ Stewart   │
└─────────────┴────────────┴───────────┘
  14 rows (10 shown)         3 columns
```

### Q34. Aggregate before joining: units sold per category

Pre-aggregating `order_items` in a CTE means the join only has to match
64 product totals instead of 607 line items. The result is identical.

```sql
WITH units_per_product AS (
    SELECT product_id, SUM(quantity) AS units
    FROM order_items
    GROUP BY product_id
)
SELECT c.category_name,
       SUM(u.units) AS units_sold
FROM units_per_product u
JOIN products   p ON u.product_id  = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY units_sold DESC;
```

**Result:**

```text
┌────────────────┬────────────┐
│ category_name  │ units_sold │
│    varchar     │   int128   │
├────────────────┼────────────┤
│ Food & Grocery │        219 │
│ Toys           │        205 │
│ Clothing       │        202 │
│ Home & Kitchen │        193 │
│ Books          │        184 │
│ Sports         │        181 │
│ Electronics    │        180 │
│ Beauty         │        177 │
└────────────────┴────────────┘
```

### Q35. Use LIMIT with ORDER BY to get only what you need: the 5 most recent orders

```sql
SELECT order_id, customer_id, order_date, status
FROM orders
ORDER BY order_date DESC, order_id DESC
LIMIT 5;
```

**Result:**

```text
┌──────────┬─────────────┬────────────┬───────────┐
│ order_id │ customer_id │ order_date │  status   │
│  int32   │    int32    │    date    │  varchar  │
├──────────┼─────────────┼────────────┼───────────┤
│       56 │          22 │ 2025-02-04 │ completed │
│      127 │           8 │ 2025-02-02 │ cancelled │
│       91 │           7 │ 2025-02-02 │ completed │
│      171 │          15 │ 2025-02-01 │ shipped   │
│      140 │          35 │ 2025-01-31 │ completed │
└──────────┴─────────────┴────────────┴───────────┘
```

### Q36. Which tables use the most storage? (DuckDB metadata)

```sql
SELECT table_name,
       estimated_size AS approx_rows,
       column_count
FROM duckdb_tables()
ORDER BY estimated_size DESC;
```

**Result:**

```text
┌─────────────────────┬─────────────┬──────────────┐
│     table_name      │ approx_rows │ column_count │
│       varchar       │    int64    │    int64     │
├─────────────────────┼─────────────┼──────────────┤
│ order_items         │         607 │            5 │
│ orders              │         200 │            5 │
│ reviews             │         150 │            6 │
│ shipping            │         141 │            6 │
│ orders_denormalized │         100 │           13 │
│ product_suppliers   │          90 │            3 │
│ products            │          64 │            5 │
│ customers           │          40 │            7 │
│ suppliers           │          10 │            6 │
│ categories          │           8 │            3 │
└─────────────────────┴─────────────┴──────────────┘
  10 rows                                3 columns
```

### Q37. Avoid repeating the same sub-query: find orders above the average order total

The CTE computes the average once and the main query reuses it.

```sql
WITH stats AS (
    SELECT AVG(total_amount) AS avg_total
    FROM orders
)
SELECT o.order_id,
       o.total_amount,
       ROUND(s.avg_total, 2) AS avg_total
FROM orders o
CROSS JOIN stats s
WHERE o.total_amount > s.avg_total
ORDER BY o.total_amount DESC;
```

**Result:**

```text
┌──────────┬───────────────┬───────────┐
│ order_id │ total_amount  │ avg_total │
│  int32   │ decimal(10,2) │  double   │
├──────────┼───────────────┼───────────┤
│      190 │        799.66 │    408.59 │
│      200 │        790.61 │    408.59 │
│        8 │        787.49 │    408.59 │
│      133 │        787.24 │    408.59 │
│      159 │        784.60 │    408.59 │
│       ·  │           ·   │       ·   │
│       ·  │           ·   │       ·   │
│       ·  │           ·   │       ·   │
│      161 │        431.97 │    408.59 │
│       99 │        421.83 │    408.59 │
│      147 │        418.14 │    408.59 │
│       63 │        412.43 │    408.59 │
│       74 │        410.63 │    408.59 │
└──────────┴───────────────┴───────────┘
  100 rows (10 shown)        3 columns
```


## Part E — Transactions & ACID (Week 8)

DuckDB notes:

* Outside of `BEGIN TRANSACTION ... COMMIT/ROLLBACK`, every statement is its
  own transaction (**auto-commit**).
* When a statement inside a transaction fails, the whole transaction is
  aborted: later statements are refused until you `ROLLBACK`, and a `COMMIT`
  saves nothing.
* DuckDB does not support `SAVEPOINT`.


### Q38. Create a practice table `gift_cards` with three cards

`CREATE OR REPLACE` lets you re-run this question to reset the table.

```sql
CREATE OR REPLACE TABLE gift_cards (
    card_id     INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    balance     DECIMAL(10,2) NOT NULL CHECK (balance >= 0)
);

INSERT INTO gift_cards VALUES
    (1, 5,  100.00),
    (2, 12,  40.00),
    (3, 20,  75.00);

SELECT * FROM gift_cards ORDER BY card_id;
```

**Result:**

```text
CREATE OR REPLACE TABLE gift_cards (
    card_id     INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    balance     DECIMAL(10,2) NOT NULL CHECK (balance >= 0)
);

INSERT INTO gift_cards VALUES
    (1, 5,  100.00),
    (2, 12,  40.00),
    (3, 20,  75.00);

SELECT * FROM gift_cards ORDER BY card_id;
┌─────────┬─────────────┬───────────────┐
│ card_id │ customer_id │    balance    │
│  int32  │    int32    │ decimal(10,2) │
├─────────┼─────────────┼───────────────┤
│       1 │           5 │        100.00 │
│       2 │          12 │         40.00 │
│       3 │          20 │         75.00 │
└─────────┴─────────────┴───────────────┘
```

### Q39. Move $25 from card 1 to card 2 in one transaction and COMMIT

Both updates succeed together or not at all (**Atomicity**).

```sql
BEGIN TRANSACTION;

UPDATE gift_cards SET balance = balance - 25 WHERE card_id = 1;
UPDATE gift_cards SET balance = balance + 25 WHERE card_id = 2;

COMMIT;

SELECT * FROM gift_cards ORDER BY card_id;
```

**Result:**

```text
BEGIN TRANSACTION;

UPDATE gift_cards SET balance = balance - 25 WHERE card_id = 1;
UPDATE gift_cards SET balance = balance + 25 WHERE card_id = 2;

COMMIT;

SELECT * FROM gift_cards ORDER BY card_id;
┌─────────┬─────────────┬───────────────┐
│ card_id │ customer_id │    balance    │
│  int32  │    int32    │ decimal(10,2) │
├─────────┼─────────────┼───────────────┤
│       1 │           5 │         75.00 │
│       2 │          12 │         65.00 │
│       3 │          20 │         75.00 │
└─────────┴─────────────┴───────────────┘
```

### Q40. Give every card a 10% bonus, look at the result, then ROLLBACK

```sql
BEGIN TRANSACTION;

UPDATE gift_cards SET balance = balance * 1.10;

SELECT * FROM gift_cards ORDER BY card_id;

ROLLBACK;

SELECT * FROM gift_cards ORDER BY card_id;
```

**Result:**

```text
BEGIN TRANSACTION;

UPDATE gift_cards SET balance = balance * 1.10;

SELECT * FROM gift_cards ORDER BY card_id;
┌─────────┬─────────────┬───────────────┐
│ card_id │ customer_id │    balance    │
│  int32  │    int32    │ decimal(10,2) │
├─────────┼─────────────┼───────────────┤
│       1 │           5 │         82.50 │
│       2 │          12 │         71.50 │
│       3 │          20 │         82.50 │
└─────────┴─────────────┴───────────────┘

ROLLBACK;

SELECT * FROM gift_cards ORDER BY card_id;
┌─────────┬─────────────┬───────────────┐
│ card_id │ customer_id │    balance    │
│  int32  │    int32    │ decimal(10,2) │
├─────────┼─────────────┼───────────────┤
│       1 │           5 │         75.00 │
│       2 │          12 │         65.00 │
│       3 │          20 │         75.00 │
└─────────┴─────────────┴───────────────┘
```

### Q41. Try to move $500 from card 3 (balance $75) to card 1. What happens?

The `CHECK (balance >= 0)` constraint rejects the first update, the
transaction is aborted, and the second update is refused (**Consistency** +
**Atomicity**). After `ROLLBACK`, the balances are unchanged.

```sql
-- expected error
BEGIN TRANSACTION;

UPDATE gift_cards SET balance = balance - 500 WHERE card_id = 3;
UPDATE gift_cards SET balance = balance + 500 WHERE card_id = 1;

ROLLBACK;

SELECT * FROM gift_cards ORDER BY card_id;
```

**Result:**

```text
-- expected error
BEGIN TRANSACTION;

UPDATE gift_cards SET balance = balance - 500 WHERE card_id = 3;
Constraint Error:
CHECK constraint failed on table gift_cards with expression CHECK((balance >= 0))
UPDATE gift_cards SET balance = balance + 500 WHERE card_id = 1;
TransactionContext Error:
Current transaction is aborted (please ROLLBACK)

ROLLBACK;

SELECT * FROM gift_cards ORDER BY card_id;
┌─────────┬─────────────┬───────────────┐
│ card_id │ customer_id │    balance    │
│  int32  │    int32    │ decimal(10,2) │
├─────────┼─────────────┼───────────────┤
│       1 │           5 │         75.00 │
│       2 │          12 │         65.00 │
│       3 │          20 │         75.00 │
└─────────┴─────────────┴───────────────┘
```

### Q42. What does COMMIT do after a statement in the transaction has failed?

It saves nothing: card 2 keeps its old balance even though its update ran
before the failing statement.

```sql
-- expected error
BEGIN TRANSACTION;

UPDATE gift_cards SET balance = balance + 10 WHERE card_id = 2;
UPDATE gift_cards SET balance = balance - 999 WHERE card_id = 3;

COMMIT;

SELECT * FROM gift_cards ORDER BY card_id;
```

**Result:**

```text
-- expected error
BEGIN TRANSACTION;

UPDATE gift_cards SET balance = balance + 10 WHERE card_id = 2;
UPDATE gift_cards SET balance = balance - 999 WHERE card_id = 3;
Constraint Error:
CHECK constraint failed on table gift_cards with expression CHECK((balance >= 0))

COMMIT;

SELECT * FROM gift_cards ORDER BY card_id;
┌─────────┬─────────────┬───────────────┐
│ card_id │ customer_id │    balance    │
│  int32  │    int32    │ decimal(10,2) │
├─────────┼─────────────┼───────────────┤
│       1 │           5 │         75.00 │
│       2 │          12 │         65.00 │
│       3 │          20 │         75.00 │
└─────────┴─────────────┴───────────────┘
```

### Q43. Show auto-commit: an UPDATE outside a transaction cannot be rolled back

```sql
-- expected error
UPDATE gift_cards SET balance = balance + 5 WHERE card_id = 3;

ROLLBACK;

SELECT * FROM gift_cards ORDER BY card_id;
```

**Result:**

```text
-- expected error
UPDATE gift_cards SET balance = balance + 5 WHERE card_id = 3;

ROLLBACK;
TransactionContext Error:
cannot rollback - no transaction is active

SELECT * FROM gift_cards ORDER BY card_id;
┌─────────┬─────────────┬───────────────┐
│ card_id │ customer_id │    balance    │
│  int32  │    int32    │ decimal(10,2) │
├─────────┼─────────────┼───────────────┤
│       1 │           5 │         75.00 │
│       2 │          12 │         65.00 │
│       3 │          20 │         80.00 │
└─────────┴─────────────┴───────────────┘
```

### Q44. Show durability: the committed balances are still there in a new session

Each question in this file was validated in a separate DuckDB session, so
this result also shows that the changes committed in Q39 and Q43 were saved
to the database file (**Durability**).

```sql
SELECT card_id,
       balance
FROM gift_cards
ORDER BY card_id;
```

**Result:**

```text
┌─────────┬───────────────┐
│ card_id │    balance    │
│  int32  │ decimal(10,2) │
├─────────┼───────────────┤
│       1 │         75.00 │
│       2 │         65.00 │
│       3 │         80.00 │
└─────────┴───────────────┘
```

### Q45. A CHECK constraint protects stock levels: try to sell 1000 units of product 1

```sql
-- expected error
BEGIN TRANSACTION;

UPDATE products
SET stock_quantity = stock_quantity - 1000
WHERE product_id = 1;

ROLLBACK;

SELECT product_id, product_name, stock_quantity
FROM products
WHERE product_id = 1;
```

**Result:**

```text
-- expected error
BEGIN TRANSACTION;

UPDATE products
SET stock_quantity = stock_quantity - 1000
WHERE product_id = 1;
Constraint Error:
CHECK constraint failed on table products with expression CHECK((stock_quantity >= 0))

ROLLBACK;

SELECT product_id, product_name, stock_quantity
FROM products
WHERE product_id = 1;
┌────────────┬────────────────┬────────────────┐
│ product_id │  product_name  │ stock_quantity │
│   int32    │    varchar     │     int32      │
├────────────┼────────────────┼────────────────┤
│          1 │ Smartphone X12 │             12 │
└────────────┴────────────────┴────────────────┘
```

### Q46. Place an order as one transaction: order + items + stock update (then ROLLBACK)

A real checkout would end with `COMMIT`; we end with `ROLLBACK` so the
practice data stays unchanged. `UPDATE ... FROM` updates `products` using
values from `order_items`.

```sql
BEGIN TRANSACTION;

INSERT INTO orders VALUES (201, 5, DATE '2025-02-05', 'processing', 662.79);

INSERT INTO order_items VALUES
    (608, 201, 1, 2, 321.52),
    (609, 201, 7, 1,  19.75);

UPDATE products
SET stock_quantity = products.stock_quantity - oi.quantity
FROM order_items oi
WHERE oi.product_id = products.product_id AND
      oi.order_id = 201;

SELECT p.product_id, p.product_name, p.stock_quantity
FROM products p
WHERE p.product_id IN (1, 7)
ORDER BY p.product_id;

ROLLBACK;

SELECT COUNT(*) AS order_201_exists FROM orders WHERE order_id = 201;
```

**Result:**

```text
BEGIN TRANSACTION;

INSERT INTO orders VALUES (201, 5, DATE '2025-02-05', 'processing', 662.79);

INSERT INTO order_items VALUES
    (608, 201, 1, 2, 321.52),
    (609, 201, 7, 1,  19.75);

UPDATE products
SET stock_quantity = products.stock_quantity - oi.quantity
FROM order_items oi
WHERE oi.product_id = products.product_id AND
      oi.order_id = 201;

SELECT p.product_id, p.product_name, p.stock_quantity
FROM products p
WHERE p.product_id IN (1, 7)
ORDER BY p.product_id;
┌────────────┬────────────────┬────────────────┐
│ product_id │  product_name  │ stock_quantity │
│   int32    │    varchar     │     int32      │
├────────────┼────────────────┼────────────────┤
│          1 │ Smartphone X12 │             10 │
│          7 │ Webcam HD      │            110 │
└────────────┴────────────────┴────────────────┘

ROLLBACK;

SELECT COUNT(*) AS order_201_exists FROM orders WHERE order_id = 201;
┌──────────────────┐
│ order_201_exists │
│      int64       │
├──────────────────┤
│                0 │
└──────────────────┘
```

### Q47. One bad line item cancels the whole order

The second item has `quantity = 0`, which violates `CHECK (quantity > 0)`.
Because the order and its items are in one transaction, the order row is
not saved either.

```sql
-- expected error
BEGIN TRANSACTION;

INSERT INTO orders VALUES (202, 7, DATE '2025-02-05', 'processing', 19.75);

INSERT INTO order_items VALUES
    (610, 202, 7, 1, 19.75),
    (611, 202, 9, 0, 25.00);

COMMIT;

SELECT COUNT(*) AS order_202_exists FROM orders WHERE order_id = 202;
```

**Result:**

```text
-- expected error
BEGIN TRANSACTION;

INSERT INTO orders VALUES (202, 7, DATE '2025-02-05', 'processing', 19.75);

INSERT INTO order_items VALUES
    (610, 202, 7, 1, 19.75),
    (611, 202, 9, 0, 25.00);
Constraint Error:
CHECK constraint failed on table order_items with expression CHECK((quantity > 0))

COMMIT;

SELECT COUNT(*) AS order_202_exists FROM orders WHERE order_id = 202;
┌──────────────────┐
│ order_202_exists │
│      int64       │
├──────────────────┤
│                0 │
└──────────────────┘
```

### Q48. Cancel an order and return its items to stock in one transaction (then ROLLBACK)

```sql
BEGIN TRANSACTION;

UPDATE orders SET status = 'cancelled' WHERE order_id = 10;

UPDATE products
SET stock_quantity = products.stock_quantity + oi.quantity
FROM order_items oi
WHERE oi.product_id = products.product_id AND
      oi.order_id = 10;

SELECT o.order_id, o.status, p.product_name, p.stock_quantity
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products    p  ON oi.product_id = p.product_id
WHERE o.order_id = 10
ORDER BY p.product_name;

ROLLBACK;

SELECT order_id, status FROM orders WHERE order_id = 10;
```

**Result:**

```text
BEGIN TRANSACTION;

UPDATE orders SET status = 'cancelled' WHERE order_id = 10;

UPDATE products
SET stock_quantity = products.stock_quantity + oi.quantity
FROM order_items oi
WHERE oi.product_id = products.product_id AND
      oi.order_id = 10;

SELECT o.order_id, o.status, p.product_name, p.stock_quantity
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products    p  ON oi.product_id = p.product_id
WHERE o.order_id = 10
ORDER BY p.product_name;
┌──────────┬───────────┬─────────────────┬────────────────┐
│ order_id │  status   │  product_name   │ stock_quantity │
│  int32   │  varchar  │     varchar     │     int32      │
├──────────┼───────────┼─────────────────┼────────────────┤
│       10 │ cancelled │ Organic Granola │            113 │
└──────────┴───────────┴─────────────────┴────────────────┘

ROLLBACK;

SELECT order_id, status FROM orders WHERE order_id = 10;
┌──────────┬───────────┐
│ order_id │  status   │
│  int32   │  varchar  │
├──────────┼───────────┤
│       10 │ completed │
└──────────┴───────────┘
```

### Q49. Raise Toys prices by 5% and record each change in a `price_history` table, as one unit

Both changes belong together: a price change without its history row (or
the reverse) would leave the data inconsistent. We `ROLLBACK` at the end
to keep the practice data unchanged.

```sql
CREATE OR REPLACE TABLE price_history (
    product_id INTEGER,
    old_price  DECIMAL(10,2),
    new_price  DECIMAL(10,2),
    changed_on DATE
);

BEGIN TRANSACTION;

INSERT INTO price_history
SELECT product_id, price, ROUND(price * 1.05, 2), DATE '2025-02-05'
FROM products
WHERE category_id = 6;

UPDATE products
SET price = ROUND(price * 1.05, 2)
WHERE category_id = 6;

SELECT h.product_id, p.product_name, h.old_price, h.new_price, p.price AS current_price
FROM price_history h
JOIN products p ON h.product_id = p.product_id
ORDER BY h.product_id;

ROLLBACK;

SELECT COUNT(*) AS history_rows FROM price_history;
```

**Result:**

```text
CREATE OR REPLACE TABLE price_history (
    product_id INTEGER,
    old_price  DECIMAL(10,2),
    new_price  DECIMAL(10,2),
    changed_on DATE
);

BEGIN TRANSACTION;

INSERT INTO price_history
SELECT product_id, price, ROUND(price * 1.05, 2), DATE '2025-02-05'
FROM products
WHERE category_id = 6;

UPDATE products
SET price = ROUND(price * 1.05, 2)
WHERE category_id = 6;

SELECT h.product_id, p.product_name, h.old_price, h.new_price, p.price AS current_price
FROM price_history h
JOIN products p ON h.product_id = p.product_id
ORDER BY h.product_id;
┌────────────┬────────────────────┬───────────────┬───────────────┬───────────────┐
│ product_id │    product_name    │   old_price   │   new_price   │ current_price │
│   int32    │      varchar       │ decimal(10,2) │ decimal(10,2) │ decimal(10,2) │
├────────────┼────────────────────┼───────────────┼───────────────┼───────────────┤
│         41 │ Building Blocks    │        148.48 │        155.90 │        155.90 │
│         42 │ Board Game Classic │        104.78 │        110.02 │        110.02 │
│         43 │ Puzzle 1000pc      │        104.27 │        109.48 │        109.48 │
│         44 │ RC Car             │        116.41 │        122.23 │        122.23 │
│         45 │ Stuffed Bear       │         38.21 │         40.12 │         40.12 │
│         46 │ Card Game          │        121.73 │        127.82 │        127.82 │
│         47 │ Art Kit            │         43.82 │         46.01 │         46.01 │
│         48 │ Science Set        │        137.40 │        144.27 │        144.27 │
└────────────┴────────────────────┴───────────────┴───────────────┴───────────────┘

ROLLBACK;

SELECT COUNT(*) AS history_rows FROM price_history;
┌──────────────┐
│ history_rows │
│    int64     │
├──────────────┤
│            0 │
└──────────────┘
```

### Q50. Clean up the practice tables and confirm the ShopSmart data is unchanged

```sql
DROP TABLE IF EXISTS gift_cards;
DROP TABLE IF EXISTS price_history;

SELECT (SELECT COUNT(*) FROM orders)      AS orders,
       (SELECT COUNT(*) FROM order_items) AS order_items,
       (SELECT SUM(stock_quantity) FROM products) AS total_stock,
       (SELECT SUM(price) FROM products)  AS sum_of_prices;
```

**Result:**

```text
DROP TABLE IF EXISTS gift_cards;
DROP TABLE IF EXISTS price_history;

SELECT (SELECT COUNT(*) FROM orders)      AS orders,
       (SELECT COUNT(*) FROM order_items) AS order_items,
       (SELECT SUM(stock_quantity) FROM products) AS total_stock,
       (SELECT SUM(price) FROM products)  AS sum_of_prices;
┌────────┬─────────────┬─────────────┬───────────────┐
│ orders │ order_items │ total_stock │ sum_of_prices │
│ int64  │    int64    │   int128    │ decimal(38,2) │
├────────┼─────────────┼─────────────┼───────────────┤
│    200 │         607 │       13037 │       6289.34 │
└────────┴─────────────┴─────────────┴───────────────┘
```
