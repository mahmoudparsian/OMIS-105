---
marp: true
theme: default
paginate: true
header: "OMIS 105 – Database Management Systems"
footer: "Week 4: SQL Mastery — Part 2 (JOINs)"
---

# OMIS 105: Database Management Systems
## Week 4 — SQL Mastery (Part 2)
### JOINs and Multi-Table Queries

---

# This Week's Goals

1. Understand all JOIN types
2. Write multi-table queries with proper JOIN syntax
3. Combine JOINs with GROUP BY, HAVING, and subqueries
4. Build real-world business reports

---

# Why JOINs?

Our data lives in separate tables:
- `customers` — who the buyers are
- `orders` — what they bought
- `products` — what we sell
- `order_items` — links orders to products

**JOINs** let us combine these tables in a single query.

---

# Session 1: JOIN Fundamentals

---

# The Old Way (Implicit Join)

```sql
SELECT c.first_name, o.order_id, o.total_amount
FROM customers c, orders o
WHERE c.customer_id = o.customer_id;
```

This works but is **outdated** and error-prone (forget WHERE → Cartesian product!).

---

# The Modern Way: INNER JOIN

```sql
SELECT c.first_name, o.order_id, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

Explicit, readable, and safe. **Always use this syntax.**

---

# INNER JOIN — How It Works

```
customers                   orders
┌────┬───────┐             ┌────┬─────┬───────┐
│ id │ name  │             │ id │c_id │ total │
├────┼───────┤             ├────┼─────┼───────┤
│ 1  │ Alice │──matches──▶ │ 1  │  1  │  150  │
│ 2  │ Bob   │──matches──▶ │ 2  │  2  │   75  │
│ 3  │ Carol │  (no match) │ 3  │  1  │  200  │
└────┴───────┘             └────┴─────┴───────┘

Result: Alice+Order1, Bob+Order2, Alice+Order3
Carol is excluded (no matching orders)
```

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

Returns **all rows from the left table** + matching rows from right.
Non-matching rows get NULL for right-table columns.

```sql
SELECT c.first_name, c.last_name, o.order_id, o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.last_name;
```

Carol (no orders) appears with NULLs for order columns.

---

# LEFT JOIN — Visual

```
customers (LEFT)            orders (RIGHT)
┌────┬───────┐             ┌────┬─────┐
│ 1  │ Alice │──match────▶ │ 1  │  1  │  ✓
│ 2  │ Bob   │──match────▶ │ 2  │  2  │  ✓
│ 3  │ Carol │──no match─▶ │    │NULL │  ✓ (included!)
└────┴───────┘             └────┴─────┘
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

This is more efficient than `NOT IN` subqueries!

---

# RIGHT JOIN (RIGHT OUTER JOIN)

Returns all rows from the **right table** + matching from left.

```sql
SELECT c.first_name, o.order_id, o.total_amount
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;
```

Rarely used — you can always rewrite as LEFT JOIN by swapping table order.

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

Use sparingly! 40 customers × 64 products = 2,560 rows.

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

Each JOIN connects via a foreign key → primary key relationship.

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
-- Total revenue per customer
SELECT c.first_name, c.last_name,
       COUNT(DISTINCT o.order_id) AS num_orders,
       ROUND(SUM(o.total_amount), 2) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 10;
```

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
       p1.category,
       ABS(p1.price - p2.price) AS price_diff
FROM products p1
INNER JOIN products p2
    ON p1.category = p2.category
    AND p1.product_id < p2.product_id
WHERE ABS(p1.price - p2.price) < 10
ORDER BY price_diff;
```

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
       p.category,
       SUM(oi.quantity) AS total_units_sold,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;
```

---

# Customer Segmentation

```sql
SELECT
    CASE
        WHEN SUM(o.total_amount) >= 1000 THEN 'VIP'
        WHEN SUM(o.total_amount) >= 500 THEN 'Regular'
        WHEN SUM(o.total_amount) >= 100 THEN 'Occasional'
        ELSE 'New'
    END AS segment,
    COUNT(*) AS num_customers,
    ROUND(AVG(SUM(o.total_amount)) OVER(), 2) AS overall_avg
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;
```

---

# Products Never Ordered

```sql
SELECT p.product_name, p.category, p.price
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.item_id IS NULL
ORDER BY p.price DESC;
```

---

# JOIN Performance Tips

1. Always join on **indexed/primary key** columns
2. **Filter early** with WHERE before joining large tables
3. Use **INNER JOIN** unless you need unmatched rows
4. Avoid unnecessary CROSS JOINs
5. Use EXPLAIN to see the query plan (Week 7)

---

# Common JOIN Mistakes

| Mistake | Result |
|---------|--------|
| Forgetting ON clause | Cartesian product (huge result) |
| Wrong join column | Incorrect matches |
| Using INNER when you need LEFT | Missing rows |
| Duplicate column names | Ambiguous references |
| Not using table aliases | Verbose, hard to read |

---

# JOIN Decision Guide

```
Do you need ALL rows from one table?
├── YES → LEFT JOIN (keep all from left table)
└── NO → Do you need only matches?
    ├── YES → INNER JOIN
    └── NO → FULL OUTER JOIN (keep all from both)
```

---

# Business Report: Full Example

```sql
-- Executive summary: revenue by category and month
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

**Week 5: SQL Mastery — Part 3 (Advanced)**
- Window functions (OVER, PARTITION BY)
- Common Table Expressions (CTEs)
- Set operations (UNION, INTERSECT, EXCEPT)
- Views

---

# Questions?

Thank you!

