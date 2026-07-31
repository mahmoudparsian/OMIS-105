---
marp: true
theme: default
paginate: true
header: "OMIS 105 – Database Management Systems"
footer: "Week 3: SQL Mastery — Part 1 (Basics)"
---

# OMIS 105: Database Management Systems
## Week 3 — SQL Mastery (Part 1)
### SELECT, Filtering, Functions, and GROUP BY

---

# This Week's Goals

1. Master the full SELECT statement
2. String, date, and math functions
3. GROUP BY and HAVING
4. Intro to simple subqueries
5. Combining everything in complex queries

---

# Recap: Weeks 1–2

- Database fundamentals, DuckDB
- Relational model, keys, relationships
- Basic SELECT, WHERE, ORDER BY, LIMIT
- Aggregate functions: COUNT, SUM, AVG, MIN, MAX

**Now**: Deeper SQL — functions, grouping, and richer queries.

---

# Session 1: Functions and Expressions

---

# SQL is a Full Language

SQL is not just SELECT/WHERE — it has:
- String manipulation functions
- Date/time functions
- Mathematical functions
- Conditional expressions (CASE)
- Type conversion (CAST)

---

# String Functions

```sql
SELECT
    UPPER('hello world')       AS upper_case,    -- HELLO WORLD
    LOWER('HELLO WORLD')       AS lower_case,    -- hello world
    LENGTH('DuckDB')           AS len,            -- 6
    TRIM('  hello  ')          AS trimmed,        -- hello
    SUBSTRING('Database', 1, 4) AS sub,           -- Data
    REPLACE('DuckDB', 'Duck', 'Goose') AS rep,    -- GooseDB
    CONCAT('Hello', ' ', 'World') AS combined     -- Hello World
;
```

---

# String Functions — Applied

```sql
-- Full name from first and last
SELECT CONCAT(first_name, ' ', last_name) AS full_name,
       UPPER(email) AS email_upper,
       LENGTH(first_name) AS name_length
FROM customers
ORDER BY name_length DESC
LIMIT 10;
```

---

# String Matching: LIKE vs ILIKE

```sql
-- LIKE is case-sensitive
SELECT * FROM products WHERE product_name LIKE '%pro%';  -- might miss 'Pro'

-- ILIKE is case-insensitive (DuckDB extension)
SELECT * FROM products WHERE product_name ILIKE '%pro%'; -- finds 'Pro' too

-- Multiple patterns
SELECT * FROM products
WHERE product_name LIKE '%Set%'
   OR product_name LIKE '%Kit%';
```

---

# Mathematical Functions

```sql
SELECT
    ROUND(3.14159, 2)     AS rounded,    -- 3.14
    CEIL(3.2)             AS ceiling,     -- 4
    FLOOR(3.8)            AS floored,     -- 3
    ABS(-42)              AS absolute,    -- 42
    POWER(2, 10)          AS two_to_ten,  -- 1024
    SQRT(144)             AS square_root, -- 12
    MOD(17, 5)            AS remainder    -- 2
;
```

---

# Math in Business Queries

```sql
-- Calculate discounted prices
SELECT product_name,
       price AS original_price,
       ROUND(price * 0.85, 2) AS discounted_15pct,
       ROUND(price * 0.90, 2) AS discounted_10pct
FROM products
WHERE category = 'Electronics'
ORDER BY price DESC;
```

---

# Date Functions

```sql
SELECT
    CURRENT_DATE                          AS today,
    CURRENT_TIMESTAMP                     AS now,
    EXTRACT(YEAR FROM DATE '2024-06-15')  AS yr,     -- 2024
    EXTRACT(MONTH FROM DATE '2024-06-15') AS mo,     -- 6
    EXTRACT(DOW FROM DATE '2024-06-15')   AS dow,    -- day of week
    DATE '2024-06-15' + INTERVAL 30 DAY   AS plus30,
    DATEDIFF('day', '2024-01-01', '2024-06-15') AS diff  -- 166
;
```

---

# Date Queries on Our Data

```sql
-- Orders from 2024
SELECT order_id, customer_id, order_date, total_amount
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2024
ORDER BY order_date
LIMIT 10;

-- Orders in the last 90 days
SELECT *
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL 90 DAY;
```

---

# CASE Expressions

Conditional logic inside SQL (like if/else):

```sql
SELECT product_name, price,
    CASE
        WHEN price < 20 THEN 'Budget'
        WHEN price < 100 THEN 'Mid-Range'
        WHEN price < 300 THEN 'Premium'
        ELSE 'Luxury'
    END AS price_tier
FROM products
ORDER BY price;
```

---

# CASE with Aggregation

```sql
SELECT
    CASE
        WHEN price < 20 THEN 'Budget'
        WHEN price < 100 THEN 'Mid-Range'
        ELSE 'Premium'
    END AS price_tier,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY price_tier
ORDER BY avg_price;
```

---

# Type Conversion: CAST

```sql
-- Convert types explicitly
SELECT
    CAST(42 AS VARCHAR)            AS num_to_text,
    CAST('2024-06-15' AS DATE)     AS text_to_date,
    CAST('99.95' AS DECIMAL(10,2)) AS text_to_num,
    CAST(price AS INTEGER)         AS truncated_price
FROM products
LIMIT 5;

-- DuckDB shorthand
SELECT price::INTEGER FROM products LIMIT 5;
```

---

# COALESCE and NULLIF

```sql
-- COALESCE: return first non-NULL value
SELECT product_name,
       COALESCE(stock_quantity, 0) AS stock
FROM products;

-- NULLIF: return NULL if two values are equal
SELECT product_name,
       NULLIF(stock_quantity, 0) AS stock_or_null
FROM products;
-- Turns 0 into NULL (useful for avoiding division by zero)
```

---

# Session 2: GROUP BY and Beyond

---

# GROUP BY — The Big Idea

**Group rows** that share a value, then **aggregate** each group.

```sql
SELECT category, COUNT(*) AS num_products
FROM products
GROUP BY category;
```

Without GROUP BY: one result row for the entire table.
With GROUP BY: one result row **per group**.

---

# GROUP BY — Execution Order

```
1. FROM     → pick the table
2. WHERE    → filter individual rows
3. GROUP BY → form groups
4. HAVING   → filter groups
5. SELECT   → compute output columns
6. ORDER BY → sort results
7. LIMIT    → restrict output
```

This order matters! You cannot use aliases from SELECT in WHERE.

---

# GROUP BY — Examples

```sql
-- Products per category
SELECT category, COUNT(*) AS cnt
FROM products
GROUP BY category
ORDER BY cnt DESC;

-- Average price per category
SELECT category,
       COUNT(*) AS num_products,
       ROUND(AVG(price), 2) AS avg_price,
       MIN(price) AS cheapest,
       MAX(price) AS most_expensive
FROM products
GROUP BY category
ORDER BY avg_price DESC;
```

---

# GROUP BY with Multiple Columns

```sql
-- Orders by status and month
SELECT
    EXTRACT(YEAR FROM order_date) AS yr,
    EXTRACT(MONTH FROM order_date) AS mo,
    status,
    COUNT(*) AS order_count,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM orders
GROUP BY yr, mo, status
ORDER BY yr, mo, status;
```

---

# The GROUP BY Rule

**Every column in SELECT must be either:**
1. In the GROUP BY clause, OR
2. Inside an aggregate function

```sql
-- CORRECT
SELECT category, AVG(price) FROM products GROUP BY category;

-- WRONG — product_name is neither grouped nor aggregated
-- SELECT category, product_name, AVG(price) FROM products GROUP BY category;
```

---

# HAVING — Filter Groups

WHERE filters **rows** (before grouping).
HAVING filters **groups** (after grouping).

```sql
-- Categories with average price > $50
SELECT category,
       ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY category
HAVING AVG(price) > 50
ORDER BY avg_price DESC;
```

---

# WHERE vs. HAVING

```sql
-- WHERE: filter rows before grouping
SELECT category, AVG(price) AS avg_price
FROM products
WHERE stock_quantity > 0        -- filter rows first
GROUP BY category
HAVING AVG(price) > 30          -- then filter groups
ORDER BY avg_price DESC;
```

Use WHERE for row-level conditions.
Use HAVING for aggregate conditions.

---

# Counting with Conditions

```sql
-- Count products in stock vs out of stock per category
SELECT category,
    COUNT(*) AS total,
    COUNT(CASE WHEN stock_quantity > 0 THEN 1 END) AS in_stock,
    COUNT(CASE WHEN stock_quantity = 0 THEN 1 END) AS out_of_stock
FROM products
GROUP BY category
ORDER BY total DESC;
```

---

# Introduction to Subqueries

A **subquery** is a query nested inside another query.

```sql
-- Products priced above average
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC;
```

The inner query runs first, returns a single value, then the outer query uses it.

---

# Subqueries in WHERE

```sql
-- Customers who placed at least one order
SELECT first_name, last_name, email
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id FROM orders
);

-- Customers who have NEVER ordered
SELECT first_name, last_name, email
FROM customers
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id FROM orders
);
```

---

# Scalar Subqueries

Return a **single value** — can be used in SELECT:

```sql
SELECT product_name, price,
       price - (SELECT AVG(price) FROM products) AS diff_from_avg,
       ROUND(price / (SELECT MAX(price) FROM products) * 100, 1)
           AS pct_of_max
FROM products
ORDER BY price DESC
LIMIT 10;
```

---

# Bringing It All Together

```sql
-- Category report: which categories beat the overall average?
SELECT category,
       COUNT(*) AS num_products,
       ROUND(AVG(price), 2) AS cat_avg,
       ROUND((SELECT AVG(price) FROM products), 2) AS overall_avg,
       CASE
           WHEN AVG(price) > (SELECT AVG(price) FROM products)
           THEN 'Above Average'
           ELSE 'Below Average'
       END AS comparison
FROM products
GROUP BY category
ORDER BY cat_avg DESC;
```

---

# Complete Query Template

```sql
SELECT   columns / expressions / aggregates
FROM     table
WHERE    row-level conditions
GROUP BY grouping columns
HAVING   group-level conditions
ORDER BY sort columns [ASC|DESC]
LIMIT    n OFFSET m;
```

---

# String Aggregation

```sql
-- List all product names per category
SELECT category,
       STRING_AGG(product_name, ', ') AS products
FROM products
GROUP BY category
ORDER BY category;
```

---

# ROUND, CEIL, FLOOR in Aggregates

```sql
SELECT category,
       ROUND(AVG(price), 2) AS avg_price,
       CEIL(AVG(price)) AS avg_ceil,
       FLOOR(AVG(price)) AS avg_floor,
       ROUND(STDDEV(price), 2) AS price_stddev
FROM products
GROUP BY category;
```

---

# Conditional Aggregation

```sql
-- Revenue by order status
SELECT
    status,
    COUNT(*) AS num_orders,
    ROUND(SUM(total_amount), 2) AS total,
    ROUND(AVG(total_amount), 2) AS avg_order
FROM orders
GROUP BY status
ORDER BY total DESC;
```

---

# Percentages in SQL

```sql
-- What percentage of orders are in each status?
SELECT status,
       COUNT(*) AS cnt,
       ROUND(COUNT(*) * 100.0 /
             (SELECT COUNT(*) FROM orders), 1) AS pct
FROM orders
GROUP BY status
ORDER BY pct DESC;
```

---

# Summary: SQL Functions Cheat Sheet

| Category | Functions |
|----------|----------|
| String | UPPER, LOWER, LENGTH, TRIM, CONCAT, REPLACE, SUBSTRING |
| Math | ROUND, CEIL, FLOOR, ABS, POWER, SQRT, MOD |
| Date | EXTRACT, DATEDIFF, CURRENT_DATE, + INTERVAL |
| Conditional | CASE WHEN, COALESCE, NULLIF |
| Aggregate | COUNT, SUM, AVG, MIN, MAX, STRING_AGG |

---

# Summary: GROUP BY

- Groups rows sharing a value, then aggregates each group
- Every SELECT column must be grouped or aggregated
- WHERE filters rows *before* grouping
- HAVING filters groups *after* aggregating
- Subqueries let you embed one query inside another

---

# What Is Next?

**Week 4: SQL Mastery — Part 2 (JOINs)**
- INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN
- Combining multiple tables in one query
- Complex multi-table reports

---

# Questions?

Thank you!

