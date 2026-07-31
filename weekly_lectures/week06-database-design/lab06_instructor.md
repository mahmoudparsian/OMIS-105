# Lab 6: Database Design & Normalization — INSTRUCTOR SOLUTIONS

## OMIS 105 — Database Management Systems
**Week 6 | Answer Key**

---

## Part 1: Functional Dependencies (15 points)

**Q1.** (5 pts) FDs in orders_denormalized:
```
order_id → order_date, status, customer_id
customer_id → customer_name, customer_email, customer_city
product_id → product_name, category_name, unit_price
(order_id, product_id) → quantity, line_price
```

Verification queries:
```sql
-- Verify: customer_id -> customer_name
SELECT customer_id, COUNT(DISTINCT customer_name) AS dist
FROM orders_denorm GROUP BY customer_id HAVING COUNT(DISTINCT customer_name) > 1;

-- Verify: product_id -> product_name
SELECT product_id, COUNT(DISTINCT product_name) AS dist
FROM orders_denorm GROUP BY product_id HAVING COUNT(DISTINCT product_name) > 1;

-- Verify: order_id -> order_date
SELECT order_id, COUNT(DISTINCT order_date) AS dist
FROM orders_denorm GROUP BY order_id HAVING COUNT(DISTINCT order_date) > 1;
```

**Q2.** (5 pts) Candidate key: (order_id, product_id)
```sql
SELECT order_id, product_id, COUNT(*) AS cnt
FROM orders_denorm
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;
-- Empty result proves uniqueness
```

**Q3.** (5 pts)
- Full: (order_id, product_id) → quantity, line_price
- Partial: order_id → order_date, status, customer_id (depends on part of key)
- Partial: product_id → product_name, category_name, unit_price (depends on part of key)
- Transitive: order_id → customer_id → customer_name, customer_email, customer_city

---

## Part 2: Identifying Anomalies (10 points)

**Q4.** (5 pts)
```sql
SELECT customer_id, customer_name, customer_email,
       COUNT(*) AS times_repeated
FROM orders_denorm
GROUP BY customer_id, customer_name, customer_email
ORDER BY times_repeated DESC;
```

**Q5.** (5 pts)
- **Update anomaly**: If customer "Alice Smith" changes email, must update every row where she appears (could be 10+ rows). Missing one creates inconsistency.
- **Insertion anomaly**: Cannot add a new customer who hasn't placed an order because order_id is part of the key.
- **Deletion anomaly**: If we delete the only order for customer "Bob Johnson," we lose all his customer information (name, email, city).

---

## Part 3: Normalization (25 points)

**Q6.** (10 pts) 2NF decomposition:
```sql
-- Remove partial dependencies on composite key
CREATE TABLE orders_2nf AS
SELECT DISTINCT order_id, order_date, status, customer_id,
       customer_name, customer_email, customer_city
FROM orders_denorm;

CREATE TABLE products_2nf AS
SELECT DISTINCT product_id, product_name, category_name, unit_price
FROM orders_denorm;

CREATE TABLE order_items_2nf AS
SELECT DISTINCT order_id, product_id, quantity, line_price
FROM orders_denorm;

-- Verify
SELECT 'orders_2nf' AS tbl, COUNT(*) AS cnt FROM orders_2nf
UNION ALL SELECT 'products_2nf', COUNT(*) FROM products_2nf
UNION ALL SELECT 'order_items_2nf', COUNT(*) FROM order_items_2nf;
```

**Q7.** (10 pts) 3NF decomposition:
```sql
-- Remove transitive: customer_id -> customer_name, email, city
CREATE TABLE customers_3nf AS
SELECT DISTINCT customer_id, customer_name, customer_email, customer_city
FROM orders_denorm;

CREATE TABLE orders_3nf AS
SELECT DISTINCT order_id, order_date, status, customer_id
FROM orders_denorm;

-- Remove transitive: product_id -> category_name
CREATE TABLE categories_3nf AS
SELECT DISTINCT category_name FROM orders_denorm;

CREATE TABLE products_3nf AS
SELECT DISTINCT product_id, product_name, category_name, unit_price
FROM orders_denorm;

-- order_items stays the same
CREATE TABLE order_items_3nf AS
SELECT DISTINCT order_id, product_id, quantity, line_price
FROM orders_denorm;
```

**Q8.** (5 pts) Yes, the 3NF schema is also in BCNF because in each table, the only determinants are the primary keys (or candidate keys), and each is a superkey.

---

## Part 4: Design Challenge (15 points)

**Q9.** (10 pts) FDs:
```
loan_id → loan_date, return_date, member_id, book_id, branch_id
member_id → member_name, member_email, member_phone
book_id → book_title, isbn, author_name, author_nationality
author_name → author_nationality (transitive through book)
branch_id → branch_name, branch_city
```

3NF decomposition:
```sql
CREATE TABLE members (
    member_id INTEGER PRIMARY KEY,
    member_name VARCHAR, member_email VARCHAR, member_phone VARCHAR
);
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY,
    author_name VARCHAR, author_nationality VARCHAR
);
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    book_title VARCHAR, isbn VARCHAR UNIQUE,
    author_id INTEGER REFERENCES authors
);
CREATE TABLE branches (
    branch_id INTEGER PRIMARY KEY,
    branch_name VARCHAR, branch_city VARCHAR
);
CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY,
    loan_date DATE, return_date DATE,
    member_id INTEGER REFERENCES members,
    book_id INTEGER REFERENCES books,
    branch_id INTEGER REFERENCES branches
);
```

**Q10.** (5 pts) ER diagram should show:
- 5 entities with their PKs and attributes
- authors → books (1:M)
- members → loans (1:M)
- books → loans (1:M)
- branches → loans (1:M)

---

## Part 5: Denormalization Discussion (10 points)

**Q11.** (5 pts)
```sql
CREATE VIEW orders_denorm_view AS
SELECT o.order_id, o.order_date, o.status,
       c.customer_id, c.first_name || ' ' || c.last_name AS customer_name,
       c.email AS customer_email, c.city AS customer_city,
       p.product_id, p.product_name, cat.category_name, oi.unit_price,
       oi.quantity, ROUND(oi.quantity * oi.unit_price, 2) AS line_price
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id;
```

**Q12.** (5 pts) Two scenarios:
1. **E-commerce product listing page**: Store category_name directly in products table. Saves a JOIN on every page load. Trade-off: must update product rows when category names change.
2. **Analytics data warehouse**: Store pre-aggregated daily revenue totals. Trade-off: faster dashboard queries but daily ETL job needed, slightly stale data.

---

## Grading Rubric

| Part | Points |
|------|--------|
| Part 1: Functional Dependencies | 15 |
| Part 2: Identifying Anomalies | 10 |
| Part 3: Normalization | 25 |
| Part 4: Design Challenge | 15 |
| Part 5: Denormalization | 10 |
| **Total** | **75** |

