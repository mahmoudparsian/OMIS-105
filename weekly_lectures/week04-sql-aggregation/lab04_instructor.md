# Lab 4: JOINs and Multi-Table Queries — INSTRUCTOR SOLUTIONS

## OMIS 105 — Database Management Systems
**Week 4 | Answer Key**

---

## Part 1: INNER JOIN (15 points)

**Q1.** (5 pts)
```sql
SELECT c.first_name, c.last_name, o.order_id, o.order_date, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC
LIMIT 15;
```

**Q2.** (5 pts)
```sql
SELECT p.product_name, cat.category_name, p.price
FROM products p
INNER JOIN categories cat ON p.category_id = cat.category_id
ORDER BY cat.category_name, p.price DESC;
```

**Q3.** (5 pts)
```sql
SELECT o.order_id,
       c.first_name || ' ' || c.last_name AS customer_name,
       p.product_name, oi.quantity, oi.unit_price
FROM order_items oi
INNER JOIN orders o ON oi.order_id = o.order_id
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id
LIMIT 20;
```

---

## Part 2: LEFT JOIN (15 points)

**Q4.** (5 pts)
```sql
SELECT c.first_name, c.last_name, c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

**Q5.** (5 pts)
```sql
SELECT p.product_name, p.category_id, p.price
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.item_id IS NULL
ORDER BY p.price DESC;
```

**Q6.** (5 pts)
```sql
SELECT c.first_name, c.last_name,
       COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY order_count DESC;
```
> Key: COUNT(o.order_id) returns 0 for NULLs; COUNT(*) would return 1.

---

## Part 3: JOINs with GROUP BY (20 points)

**Q7.** (5 pts)
```sql
SELECT cat.category_name,
       SUM(oi.quantity) AS total_units,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY total_revenue DESC;
```

**Q8.** (5 pts)
```sql
SELECT p.product_name,
       SUM(oi.quantity) AS total_units,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_units DESC
LIMIT 5;
```

**Q9.** (5 pts)
```sql
SELECT c.first_name || ' ' || c.last_name AS full_name,
       COUNT(DISTINCT o.order_id) AS num_orders,
       ROUND(SUM(o.total_amount), 2) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING SUM(o.total_amount) > 300
ORDER BY total_spent DESC;
```

**Q10.** (5 pts)
```sql
SELECT EXTRACT(YEAR FROM o.order_date) AS yr,
       EXTRACT(MONTH FROM o.order_date) AS mo,
       COUNT(DISTINCT o.order_id) AS num_orders,
       COUNT(DISTINCT o.customer_id) AS unique_customers,
       ROUND(SUM(o.total_amount), 2) AS total_revenue
FROM orders o
WHERE o.status != 'cancelled'
  AND EXTRACT(YEAR FROM o.order_date) = 2024
GROUP BY yr, mo
ORDER BY yr, mo;
```

---

## Part 4: Advanced JOINs (15 points)

**Q11.** (5 pts)
```sql
SELECT p1.product_name AS product_a,
       p2.product_name AS product_b,
       p1.category_id,
       ROUND(ABS(p1.price - p2.price), 2) AS price_diff
FROM products p1
INNER JOIN products p2
    ON p1.category_id = p2.category_id
    AND p1.product_id < p2.product_id
WHERE ABS(p1.price - p2.price) < 5
ORDER BY price_diff;
```

**Q12.** (5 pts)
```sql
SELECT c.first_name, c.last_name,
       co.num_orders,
       co.avg_order_value
FROM customers c
INNER JOIN (
    SELECT customer_id,
           COUNT(*) AS num_orders,
           ROUND(AVG(total_amount), 2) AS avg_order_value
    FROM orders
    GROUP BY customer_id
    HAVING COUNT(*) >= 3
) co ON c.customer_id = co.customer_id
ORDER BY co.avg_order_value DESC;
```

**Q13.** (5 pts)
```sql
SELECT segment,
       COUNT(*) AS num_customers,
       ROUND(AVG(total_spent), 2) AS avg_spending
FROM (
    SELECT c.customer_id,
           SUM(o.total_amount) AS total_spent,
           CASE
               WHEN SUM(o.total_amount) >= 1000 THEN 'VIP'
               WHEN SUM(o.total_amount) >= 500 THEN 'Regular'
               WHEN SUM(o.total_amount) >= 100 THEN 'Occasional'
               ELSE 'New'
           END AS segment
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
) seg
GROUP BY segment
ORDER BY avg_spending DESC;
```

---

## Part 5: Business Report (10 points)

**Q14.** (10 pts)
```sql
SELECT p.product_name,
       cat.category_name,
       COALESCE(SUM(oi.quantity), 0) AS total_units,
       COALESCE(ROUND(SUM(oi.quantity * oi.unit_price), 2), 0) AS total_revenue,
       COUNT(DISTINCT oi.order_id) AS distinct_orders,
       COALESCE(ROUND(AVG(oi.quantity), 1), 0) AS avg_qty_per_order
FROM products p
INNER JOIN categories cat ON p.category_id = cat.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, cat.category_name
ORDER BY total_revenue DESC;
```
> Key points: LEFT JOIN to include never-ordered products; COALESCE for 0s instead of NULLs.

---

## Grading Rubric

| Part | Points |
|------|--------|
| Part 1: INNER JOIN | 15 |
| Part 2: LEFT JOIN | 15 |
| Part 3: JOINs + GROUP BY | 20 |
| Part 4: Advanced JOINs | 15 |
| Part 5: Business Report | 10 |
| **Total** | **75** |

