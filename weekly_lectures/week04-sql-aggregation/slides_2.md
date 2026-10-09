---
marp: true
theme: default
paginate: true
header: "OMIS 105 – Database Management Systems"
footer: "Week 4: Aggregation and JOINs"
---

# OMIS 105: Database Management Systems
## Week 4 — Aggregation and JOINs
### JOINs and Multi-Table Queries

---

# This Week's Goals

1. Understand the main JOIN types (INNER, LEFT, RIGHT, FULL, CROSS)
2. Write multi-table queries with proper JOIN syntax
3. Combine JOINs with GROUP BY, HAVING, and subqueries
4. Build real-world business reports

---

# Why JOINs?

Our data lives in separate tables:
- `customers` — who the buyers are
- `orders` — one row per order (who, when, status)
- `order_items` — the products in each order
- `products` — what we sell
- `categories` — product groups

**JOINs** let us combine these tables in a single query.

---

# Setup: Load This Week's Data

Run this once (from the `week04-sql-aggregation` folder):

```sql
CREATE OR REPLACE TABLE customers   AS SELECT * FROM read_csv('data/customers.csv');
CREATE OR REPLACE TABLE orders      AS SELECT * FROM read_csv('data/orders.csv');
CREATE OR REPLACE TABLE order_items AS SELECT * FROM read_csv('data/order_items.csv');
CREATE OR REPLACE TABLE products    AS SELECT * FROM read_csv('data/products.csv');
CREATE OR REPLACE TABLE categories  AS SELECT * FROM read_csv('data/categories.csv');
```

| Table | Rows | Key columns |
| :--- | :--- | :--- |
| customers | 40 | `customer_id` |
| orders | 200 | `order_id`, `customer_id` |
| order_items | 607 | `item_id`, `order_id`, `product_id` |
| products | 64 | `product_id`, `category_id` |
| categories | 8 | `category_id` |

Note: `products` has a `category_id`, not a category name.
To show the name, join to `categories`.

---

# A Note About This Practice Data

In this practice dataset, `orders.total_amount` was generated
separately from `order_items`. The two **do not agree**
(for order 1: `total_amount` = 56.51, but its items add up to 1033.73).

In these slides:
- **Customer** reports use `orders.total_amount`
- **Product / category** reports use `order_items.quantity * unit_price`

Do not compare totals from the two sources. In a real database,
they should match — a good thing to check!

---

# Session 1: JOIN Fundamentals

---

# The Old Way (Implicit Join)

```sql
SELECT c.first_name, o.order_id, o.total_amount
FROM customers c, orders o
WHERE c.customer_id = o.customer_id;
```

This is still valid SQL, but it is an **older style** and easy to get wrong:
forget the `WHERE`, and you get every customer paired with every order
(a *Cartesian product*: 40 × 200 = 8,000 rows).

---

# The Modern Way: INNER JOIN

```sql
SELECT c.first_name, o.order_id, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

Clear and readable: the join condition sits next to the table it joins.
**Use this syntax.** (`JOIN` alone means `INNER JOIN`.)

---

# INNER JOIN — How It Works

```
customers              orders
┌────┬───────┐         ┌──────────┬─────────────┬───────┐
│ id │ name  │         │ order_id │ customer_id │ total │
├────┼───────┤         ├──────────┼─────────────┼───────┤
│ 1  │ Alice │         │ 101      │ 1           │ 150   │
│ 2  │ Bob   │         │ 102      │ 2           │  75   │
│ 3  │ Carol │         │ 103      │ 1           │ 200   │
└────┴───────┘         └──────────┴─────────────┴───────┘

ON customers.id = orders.customer_id

Result:  Alice | 101 | 150
         Bob   | 102 |  75
         Alice | 103 | 200

Alice appears twice (two orders).
Carol is excluded (no matching orders).
```

(A small example table — not our CSV data.)

---

# INNER JOIN — Only Matching Rows

Key rule: **INNER JOIN returns only rows that have a match in BOTH tables.**

- Customer with no orders? Excluded.
- Order with no valid customer? Excluded.

---

# Table Aliases

```sql
-- Full table names (verbose)
SELECT customers.first_name, orders.order_id
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id;

-- With aliases (preferred)
SELECT c.first_name, o.order_id
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

Aliases make queries shorter and more readable.

---

# LEFT JOIN (LEFT OUTER JOIN)

Returns **all rows from the left table** (the one after `FROM`) + matching rows from the right.
If a left row has no match, the right-table columns are `NULL`.

```sql
SELECT c.first_name, c.last_name, o.order_id, o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.last_name;
```

In our data, every customer has at least one order, so LEFT JOIN and
INNER JOIN give the same rows. To see the difference, add a customer
who has not ordered yet:

```sql
INSERT INTO customers
VALUES (41, 'Dana', 'Lee', 'dana.lee@email.com', 'Denver', 'CO', DATE '2025-01-15');
```

Now Dana appears once, with `NULL` for `order_id` and `total_amount`.

---

# LEFT JOIN — Visual

Same small example as before:

```
customers LEFT JOIN orders

name  │ order_id │ total
──────┼──────────┼──────
Alice │ 101      │ 150     ✓ match
Bob   │ 102      │  75     ✓ match
Alice │ 103      │ 200     ✓ match
Carol │ NULL     │ NULL    ✓ kept, even with no match!
```

**Use case**: Find customers who have NOT placed orders.

---

# Finding Non-Matches with LEFT JOIN

```sql
-- Customers with no orders
SELECT c.first_name, c.last_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

With Dana added, this returns: **Dana Lee**.

This pattern is also **safer** than `NOT IN (subquery)`: if the subquery
returns a `NULL`, `NOT IN` returns no rows at all.

---

# RIGHT JOIN (RIGHT OUTER JOIN)

Returns all rows from the **right table** + matching from left.

```sql
SELECT c.first_name, o.order_id, o.total_amount
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;
```

Rarely used — you can always rewrite it as a LEFT JOIN by swapping the table order:
`FROM orders o LEFT JOIN customers c ON ...`

---

# FULL OUTER JOIN

Returns **all rows from both tables**, matching where possible.

```sql
SELECT c.first_name, o.order_id
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;
```

- Customers without orders → order columns are NULL
- Orders without valid customers → customer columns are NULL

In our data, every order has a valid customer.

---

# JOIN Types — Summary

| JOIN Type | Returns |
|-----------|---------|
| INNER JOIN | Only matching rows from both tables |
| LEFT JOIN | All from left + matching from right |
| RIGHT JOIN | All from right + matching from left |
| FULL OUTER JOIN | All from both, NULLs where no match |
| CROSS JOIN | Every combination (Cartesian product) |

---

# CROSS JOIN

Every row from table A paired with every row from table B.

```sql
-- All possible product-category combinations
SELECT c.category_name, p.product_name
FROM categories c
CROSS JOIN products p
LIMIT 20;
```

Use sparingly! 8 categories × 64 products = 512 rows (before `LIMIT`).
A CROSS JOIN has **no** `ON` clause.

---

# Session 2: Multi-Table Queries

---

# Joining 3+ Tables

```sql
-- Customer orders with product details
SELECT c.first_name, c.last_name,
       o.order_id, o.order_date,
       p.product_name, oi.quantity, oi.unit_price
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_date DESC
LIMIT 15;
```

---

# Join Chain Visualization

```
customers ──┐
             ├── orders ──┐
             │             ├── order_items ──┐
             │             │                 ├── products
             │             │                 │
        (customer_id)  (order_id)       (product_id)
```

Each JOIN connects a foreign key to the primary key it points to:
`orders.customer_id → customers.customer_id`, and so on.

---

# Adding Categories

```sql
SELECT cat.category_name,
       p.product_name,
       oi.quantity,
       oi.unit_price,
       oi.quantity * oi.unit_price AS line_total
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
ORDER BY line_total DESC
LIMIT 10;
```

---

# JOINs + GROUP BY

```sql
-- Total spent per customer (includes all order statuses)
SELECT c.first_name, c.last_name,
       COUNT(DISTINCT o.order_id) AS num_orders,
       ROUND(SUM(o.total_amount), 2) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 10;
```

We group by `customer_id` too, because two customers could share a name.

---

# Revenue by Category

```sql
SELECT cat.category_name,
       COUNT(DISTINCT oi.order_id) AS orders_containing,
       SUM(oi.quantity) AS units_sold,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY revenue DESC;
```

---

# JOINs + HAVING

```sql
-- Customers who spent more than $500 total
SELECT c.first_name, c.last_name,
       ROUND(SUM(o.total_amount), 2) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING SUM(o.total_amount) > 500
ORDER BY total_spent DESC;
```

---

# Self JOIN

A table joined with itself — useful for comparing rows.

```sql
-- Find products in the same category, priced similarly
SELECT p1.product_name AS product_a,
       p2.product_name AS product_b,
       p1.category_id,
       ROUND(ABS(p1.price - p2.price), 2) AS price_diff
FROM products p1
INNER JOIN products p2
    ON p1.category_id = p2.category_id
    AND p1.product_id < p2.product_id
WHERE ABS(p1.price - p2.price) < 10
ORDER BY price_diff;
```

`p1.product_id < p2.product_id` stops a product from matching itself,
and lists each pair only once (A–B, not also B–A).
Top result: Yoga Mat and Jump Rope, 0.10 apart.

---

# JOIN with Subqueries

```sql
-- Join with a derived table (subquery in FROM)
SELECT c.first_name, c.last_name, cust_orders.total_spent
FROM customers c
INNER JOIN (
    SELECT customer_id,
           ROUND(SUM(total_amount), 2) AS total_spent
    FROM orders
    GROUP BY customer_id
) cust_orders ON c.customer_id = cust_orders.customer_id
WHERE cust_orders.total_spent > 300
ORDER BY cust_orders.total_spent DESC;
```

---

# Monthly Revenue Report

```sql
SELECT
    EXTRACT(YEAR FROM o.order_date) AS yr,
    EXTRACT(MONTH FROM o.order_date) AS mo,
    COUNT(DISTINCT o.order_id) AS num_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    ROUND(SUM(o.total_amount), 2) AS revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM orders o
WHERE o.status != 'cancelled'
GROUP BY yr, mo
ORDER BY yr, mo;
```

---

# Best-Selling Products

```sql
SELECT p.product_name,
       cat.category_name,
       SUM(oi.quantity) AS total_units_sold,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
GROUP BY p.product_id, p.product_name, cat.category_name
ORDER BY total_revenue DESC
LIMIT 10;
```

---

# Customer Segmentation

```sql
SELECT segment,
       COUNT(*) AS num_customers,
       ROUND(AVG(total_spent), 2) AS avg_spent
FROM (
    SELECT c.customer_id,
           SUM(o.total_amount) AS total_spent,
           CASE
               WHEN SUM(o.total_amount) >= 1000 THEN 'VIP'
               WHEN SUM(o.total_amount) >= 500  THEN 'Regular'
               WHEN SUM(o.total_amount) >= 100  THEN 'Occasional'
               ELSE 'Low'
           END AS segment
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
) segmented
GROUP BY segment
ORDER BY avg_spent DESC;
```

The inner query computes each customer's segment; the outer
query groups by segment to count customers per tier. Grouping
by `customer_id` alone (skipping the subquery) would put every
customer in their own group, so `COUNT(*)` would always be 1.

Customers with no orders are not counted, because of the INNER JOIN.

---

# Products Never Ordered

```sql
-- Every product in our data has been ordered, so first add one that has not:
INSERT INTO products VALUES (65, 'Desk Lamp', 4, 29.99, 40);
```

```sql
SELECT p.product_name, cat.category_name, p.price
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE oi.item_id IS NULL
ORDER BY p.price DESC;
```

Result: **Desk Lamp**, Home & Kitchen, 29.99

---

# JOIN Performance Tips

1. Join on **key columns**: a foreign key to its primary key
2. Select only the columns and rows you need
3. Use **INNER JOIN** unless you need unmatched rows
4. Avoid unnecessary CROSS JOINs (they multiply row counts)
5. Use `EXPLAIN` to see the query plan (Week 7)

DuckDB's optimizer reorders joins and pushes `WHERE` filters
down for you, so you can focus on writing a **correct** query.

---

# Common JOIN Mistakes

| Mistake | Result |
|---------|--------|
| Forgetting ON clause | Cartesian product (huge result) |
| Wrong join column | Incorrect matches |
| Using INNER when you need LEFT | Missing rows |
| Same column name in two tables, no alias | "Ambiguous reference" error |
| Not using table aliases | Verbose, hard to read |

---

# JOIN Decision Guide

```
Do you need only the rows that match in both tables?
├── YES → INNER JOIN
└── NO → Do you need ALL rows from just one table?
    ├── YES → LEFT JOIN (put that table first, after FROM)
    └── NO  → FULL OUTER JOIN (keep all rows from both)
```

---

# Business Report: Full Example

```sql
-- Executive summary: 2024 revenue by category and month
-- (completed and shipped orders only)
SELECT cat.category_name,
       EXTRACT(MONTH FROM o.order_date) AS month,
       COUNT(DISTINCT o.order_id) AS orders,
       SUM(oi.quantity) AS units,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status IN ('completed', 'shipped')
  AND EXTRACT(YEAR FROM o.order_date) = 2024
GROUP BY cat.category_name, EXTRACT(MONTH FROM o.order_date)
ORDER BY cat.category_name, month;
```

---

# Summary

- **INNER JOIN**: Only matching rows from both tables
- **LEFT JOIN**: All from left + matches from right (NULLs for non-matches)
- **RIGHT JOIN**: Mirror of LEFT JOIN
- **FULL OUTER JOIN**: All from both tables
- **Self JOIN**: Table joined with itself
- JOIN 3+ tables by chaining ON clauses
- Combine with GROUP BY, HAVING, CASE for powerful reports

---

# What Is Next?

**Week 5: SQL Joins**
- More multi-table JOINs
- LEFT JOIN and finding missing data with `IS NULL`
- Replacing `NULL` with `COALESCE`

---

# Questions?

Thank you!

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
