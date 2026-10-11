---
marp: true
theme: default
paginate: true
header: "OMIS 105 – Database Management Systems"
footer: "Week 5: SQL Mastery — Part 3 (Advanced)"
---

# OMIS 105: Database Management Systems
## Week 5 — SQL Mastery (Part 3)
### Window Functions, CTEs, Set Ops, and Views

> **Note:** This lecture is a preview. Its topics are **not included in the midterm exam**.

---

# This Week's Goals

1. Window functions (OVER, PARTITION BY, ORDER BY)
2. Common Table Expressions (CTEs) with WITH
3. Set operations (UNION, INTERSECT, EXCEPT)
4. Creating and using Views
5. Building analytical dashboards in SQL

---

# Setup: Load This Week's Data

Run this once (from the `week05-sql-joins` folder):

```sql
CREATE OR REPLACE TABLE customers  AS SELECT * FROM read_csv('data/customers.csv');
CREATE OR REPLACE TABLE orders     AS SELECT * FROM read_csv('data/orders.csv');
CREATE OR REPLACE TABLE reviews    AS SELECT * FROM read_csv('data/reviews.csv');
CREATE OR REPLACE TABLE categories AS SELECT * FROM read_csv('data/categories.csv');

-- products.csv has only category_id; add the category name as "category"
CREATE OR REPLACE TABLE products AS
    SELECT p.*, c.category_name AS category
    FROM read_csv('data/products.csv') AS p
    JOIN categories AS c USING (category_id);
```

---

# Session 1: Window Functions

---

# What Are Window Functions?

Regular aggregation collapses rows:
```sql
SELECT category, AVG(price) FROM products GROUP BY category;
-- One row per category
```

Window functions compute across a set of related rows **without collapsing** them:
```sql
SELECT product_name, category, price,
       AVG(price) OVER (PARTITION BY category) AS cat_avg
FROM products;
-- Every row is kept, with its category's average next to it
```

---

# Window Function Syntax

```sql
function_name(...) OVER (
    [PARTITION BY column(s)]    -- groups (like GROUP BY, but keeps rows)
    [ORDER BY column(s)]        -- ordering within each partition
    [ROWS/RANGE frame]          -- which rows to include
)
```

All three parts are optional. `OVER ()` with nothing inside means
"the whole result is one window".

---

# ROW_NUMBER — Numbering Rows

```sql
SELECT product_name, category, price,
       ROW_NUMBER() OVER (ORDER BY price DESC) AS overall_rank,
       ROW_NUMBER() OVER (
           PARTITION BY category ORDER BY price DESC
       ) AS rank_in_category
FROM products;
```

Gives a sequential number: 1, 2, 3, ... Every row gets a **different**
number, even when two prices tie (the tie is broken arbitrarily).

---

# RANK and DENSE_RANK

```sql
SELECT product_name, price,
       RANK()       OVER (ORDER BY price DESC) AS rank,
       DENSE_RANK() OVER (ORDER BY price DESC) AS dense_rank
FROM products
LIMIT 10;
```

How they handle **ties** (a small example — no two products in our data share a price, so you will not see ties there):

| Price | ROW_NUMBER | RANK | DENSE_RANK |
|-------|------------|------|------------|
| 500 | 1 | 1 | 1 |
| 500 | 2 | 1 | 1 |
| 450 | 3 | 3 | 2 |

← RANK skips 2 after a tie; DENSE_RANK does not skip

---

# Top-N Per Group

```sql
-- Top 3 most expensive products per category
SELECT * FROM (
    SELECT product_name, category, price,
           ROW_NUMBER() OVER (
               PARTITION BY category ORDER BY price DESC
           ) AS rn
    FROM products
) ranked
WHERE rn <= 3
ORDER BY category, rn;
```

Very common pattern in interviews and reports!

The window function must go in a subquery (or CTE), because
`WHERE` runs before window functions are computed.
(DuckDB also offers a shortcut: `QUALIFY rn <= 3`.)

---

# Running Aggregates

```sql
SELECT product_name, category, price,
       SUM(price) OVER (
           PARTITION BY category ORDER BY price
       ) AS running_total,
       ROUND(AVG(price) OVER (
           PARTITION BY category ORDER BY price
           ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
       ), 2) AS moving_avg
FROM products
ORDER BY category, price;
```

- `running_total`: adds up prices from the cheapest product to the current one
- `moving_avg`: averages the previous, current, and next row (3 rows)

---

# LAG and LEAD

Look at previous/next row values:

```sql
SELECT order_id, order_date, total_amount,
       LAG(total_amount)  OVER (ORDER BY order_date, order_id) AS prev_amount,
       LEAD(total_amount) OVER (ORDER BY order_date, order_id) AS next_amount,
       ROUND(total_amount
             - LAG(total_amount) OVER (ORDER BY order_date, order_id), 2)
           AS change_from_prev
FROM orders
ORDER BY order_date, order_id
LIMIT 15;
```

The first row has no previous row, so `LAG` returns `NULL`.
We add `order_id` to `ORDER BY` because some days have two orders —
this makes the order of rows exact.

---

# NTILE — Percentile Buckets

```sql
-- Divide products into 4 price quartiles
SELECT product_name, price,
       NTILE(4) OVER (ORDER BY price) AS quartile
FROM products
ORDER BY price;
```

Quartile 1 = cheapest 25%, Quartile 4 = most expensive 25%.
(64 products ÷ 4 = 16 products per quartile.)

---

# Aggregate Window Functions

All regular aggregates work as window functions:

```sql
SELECT product_name, category, price,
       ROUND(AVG(price) OVER (PARTITION BY category), 2) AS cat_avg,
       MIN(price) OVER (PARTITION BY category) AS cat_min,
       MAX(price) OVER (PARTITION BY category) AS cat_max,
       COUNT(*)   OVER (PARTITION BY category) AS cat_count,
       ROUND(price - AVG(price) OVER (PARTITION BY category), 2) AS diff_from_avg
FROM products
ORDER BY category, price DESC;
```

---

# Percent of Total

```sql
SELECT product_name, category, price,
       ROUND(price / SUM(price) OVER () * 100, 2) AS pct_of_total,
       ROUND(price / SUM(price) OVER (PARTITION BY category) * 100, 2)
           AS pct_within_category
FROM products
ORDER BY category, price DESC;
```

`SUM(price) OVER ()` is the total of **all** rows;
`OVER (PARTITION BY category)` is the total of that row's category.

---

# Cumulative Distribution

```sql
SELECT product_name, price,
       ROUND(CUME_DIST() OVER (ORDER BY price), 3)    AS cumulative_pct,
       ROUND(PERCENT_RANK() OVER (ORDER BY price), 3) AS pct_rank
FROM products
ORDER BY price;
```

- `CUME_DIST`: share of rows with a price **≤** this one (0 to 1; the cheapest is 1/64 ≈ 0.016)
- `PERCENT_RANK`: (rank − 1) / (rows − 1) — the cheapest is 0, the most expensive is 1

---

# Session 2: CTEs, Set Operations, and Views

---

# Common Table Expressions (WITH)

A CTE (Common Table Expression) is a named, temporary result
that exists only while this one query runs:

```sql
WITH customer_totals AS (
    SELECT customer_id,
           COUNT(*) AS num_orders,
           ROUND(SUM(total_amount), 2) AS total_spent
    FROM orders
    GROUP BY customer_id
)
SELECT c.first_name, c.last_name,
       ct.num_orders, ct.total_spent
FROM customers c
INNER JOIN customer_totals ct ON c.customer_id = ct.customer_id
ORDER BY ct.total_spent DESC;
```

---

# Why CTEs?

- **Readability**: Name each logical step
- **Reuse**: Refer to the same CTE more than once in the query
- **Decompose**: Break a complex query into small parts
- **Replace**: A subquery in `FROM` becomes a named step

---

# Multiple CTEs

```sql
WITH
  order_stats AS (
      SELECT customer_id,
             COUNT(*) AS num_orders,
             ROUND(SUM(total_amount), 2) AS total_spent
      FROM orders GROUP BY customer_id
  ),
  top_customers AS (
      SELECT customer_id FROM order_stats
      WHERE total_spent > 500
  )
SELECT c.first_name, c.last_name, os.total_spent
FROM customers c
JOIN order_stats os ON c.customer_id = os.customer_id
WHERE c.customer_id IN (SELECT customer_id FROM top_customers)
ORDER BY os.total_spent DESC;
```

Each CTE can use the CTEs defined before it (`top_customers` reads `order_stats`).

---

# CTEs vs Subqueries

```sql
-- Subquery version (harder to read)
SELECT c.first_name, sub.total
FROM customers c
INNER JOIN (
    SELECT customer_id, ROUND(SUM(total_amount), 2) AS total
    FROM orders GROUP BY customer_id
) sub ON c.customer_id = sub.customer_id;

-- CTE version (easier to read)
WITH order_totals AS (
    SELECT customer_id, ROUND(SUM(total_amount), 2) AS total
    FROM orders GROUP BY customer_id
)
SELECT c.first_name, ot.total
FROM customers c
INNER JOIN order_totals ot ON c.customer_id = ot.customer_id;
```

---

# Set Operations

Combine results of two queries:

| Operation | Returns |
|-----------|---------|
| UNION | All unique rows from both queries |
| UNION ALL | All rows (including duplicates) |
| INTERSECT | Only rows in both queries |
| EXCEPT | Rows in first query but not second |

---

# UNION Example

```sql
-- Customers from CA and NY
SELECT first_name, last_name, city, state
FROM customers WHERE state = 'CA'

UNION

SELECT first_name, last_name, city, state
FROM customers WHERE state = 'NY'

ORDER BY state, last_name;
```

- Both queries must have the same number of columns, in the same order, with compatible types.
- `ORDER BY` at the end sorts the **combined** result.
- Result: 10 customers (7 in CA, 3 in NY). This one could also be
  written as `WHERE state IN ('CA', 'NY')`; UNION is needed when the
  rows come from **different** tables or queries.

---

# INTERSECT and EXCEPT

```sql
-- Customers who ordered AND left a review
SELECT customer_id FROM orders
INTERSECT
SELECT customer_id FROM reviews;

-- Customers who ordered but NEVER left a review
SELECT DISTINCT customer_id FROM orders
EXCEPT
SELECT customer_id FROM reviews;
```

Like `UNION`, `INTERSECT` and `EXCEPT` remove duplicates.

In our data, all 40 customers have ordered **and** reviewed,
so `INTERSECT` returns 40 rows and `EXCEPT` returns **0 rows**.
Try `SELECT product_id FROM products EXCEPT SELECT product_id FROM reviews;`
— it returns the 8 products that have never been reviewed.

---

# Views — Virtual Tables

A **view** is a saved query that acts like a table.
It stores the **query**, not the data — every time you use it,
the query runs again on the current data.

```sql
CREATE VIEW product_summary AS
SELECT p.product_name, cat.category_name,
       p.price, p.stock_quantity,
       CASE WHEN p.stock_quantity = 0 THEN 'Out of Stock'
            WHEN p.stock_quantity < 20 THEN 'Low Stock'
            ELSE 'In Stock'
       END AS availability
FROM products p
INNER JOIN categories cat ON p.category_id = cat.category_id;
```

---

# Using Views

```sql
-- Now query it like a regular table
SELECT * FROM product_summary
WHERE availability = 'Low Stock'          -- 4 products in our data
ORDER BY price DESC;

-- Aggregate over the view
SELECT category_name, COUNT(*) AS cnt,
       ROUND(AVG(price), 2) AS avg_price
FROM product_summary
GROUP BY category_name;
```

---

# Why Use Views?

1. **Simplify** complex queries — write once, reuse
2. **Security** — in multi-user databases, let users see a view but not the full table
3. **Abstraction** — change underlying tables without breaking apps
4. **Consistency** — ensure everyone uses the same logic

---

# View for Customer Dashboard

```sql
CREATE VIEW customer_dashboard AS
WITH order_stats AS (
    SELECT customer_id,
           COUNT(*) AS total_orders,
           ROUND(SUM(total_amount), 2) AS total_spent,
           MAX(order_date) AS last_order_date
    FROM orders
    WHERE status != 'cancelled'
    GROUP BY customer_id
)
SELECT c.first_name, c.last_name, c.email, c.city, c.state,
       COALESCE(os.total_orders, 0) AS total_orders,
       COALESCE(os.total_spent, 0) AS total_spent,
       os.last_order_date,
       CASE
           WHEN os.total_spent >= 1000 THEN 'VIP'
           WHEN os.total_spent >= 500 THEN 'Regular'
           WHEN os.total_spent IS NOT NULL THEN 'Occasional'
           ELSE 'Inactive'
       END AS segment
FROM customers c
LEFT JOIN order_stats os ON c.customer_id = os.customer_id;
```

This view combines a CTE, a LEFT JOIN, `COALESCE`, and `CASE`.
The LEFT JOIN keeps customers with no (non-cancelled) orders;
`COALESCE` shows 0 for them, and `CASE` labels them `'Inactive'`.

---

# Analytical Query: Revenue Trends

```sql
WITH monthly_revenue AS (
    SELECT DATE_TRUNC('month', order_date) AS month,
           SUM(total_amount) AS revenue
    FROM orders
    WHERE status != 'cancelled'
    GROUP BY month
)
SELECT month,
       revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_month,
       ROUND(revenue - LAG(revenue) OVER (ORDER BY month), 2)
           AS month_over_month_change,
       ROUND((revenue / LAG(revenue) OVER (ORDER BY month) - 1) * 100, 1)
           AS pct_change
FROM monthly_revenue
ORDER BY month;
```

`DATE_TRUNC('month', order_date)` turns every date into the first day
of its month (2024-03-17 → 2024-03-01), so all orders in a month group together.

---

# Analytical Query: Customer RFM

```sql
-- Recency, Frequency, Monetary analysis
-- Recency is measured from the last date in the data (not today),
-- because our sample orders end in February 2025.
WITH rfm AS (
    SELECT customer_id,
           DATEDIFF('day', MAX(order_date),
                    (SELECT MAX(order_date) FROM orders)) AS recency,
           COUNT(*) AS frequency,
           ROUND(SUM(total_amount), 2) AS monetary
    FROM orders
    WHERE status != 'cancelled'
    GROUP BY customer_id
)
SELECT c.first_name, c.last_name,
       r.recency, r.frequency, r.monetary,
       NTILE(4) OVER (ORDER BY r.recency DESC) AS r_score,
       NTILE(4) OVER (ORDER BY r.frequency) AS f_score,
       NTILE(4) OVER (ORDER BY r.monetary) AS m_score
FROM rfm r
INNER JOIN customers c ON r.customer_id = c.customer_id
ORDER BY r.monetary DESC;
```

- **R**ecency: days since the last order (smaller is better)
- **F**requency: number of orders (bigger is better)
- **M**onetary: total spent (bigger is better)

Each score is 1–4, and **4 is best**. That is why recency is sorted
`DESC`: the customers who ordered most recently land in group 4.

---

# DROP and REPLACE Views

```sql
-- Remove a view
DROP VIEW IF EXISTS product_summary;

-- Create or replace
CREATE OR REPLACE VIEW product_summary AS
SELECT product_name, price FROM products;
```

---

# Summary

- **Window functions**: Compute across rows without collapsing
  - ROW_NUMBER, RANK, DENSE_RANK, NTILE
  - LAG, LEAD
  - Running SUM, AVG, etc.
- **CTEs** (WITH): Named, temporary results that make queries readable
- **Set operations**: UNION, INTERSECT, EXCEPT
- **Views**: Saved queries that act like tables (they store the query, not the data)

---

# End of SQL Mastery!

Over weeks 3–5 you have learned:
- Functions (string, math, date, CASE)
- GROUP BY, HAVING, subqueries
- All JOIN types
- Window functions
- CTEs and Views

You now have a comprehensive SQL toolkit!

---

# What Is Next?

**Week 6: Database Design & Normalization**
- Functional dependencies
- Normal forms (1NF, 2NF, 3NF, BCNF)
- When to denormalize

---

# Questions?

Thank you!

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
