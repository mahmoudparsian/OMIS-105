# Sample Lab 01: SQL Functions, GROUP BY, and Subqueries — INSTRUCTOR SOLUTIONS

## OMIS 105 — Database Management Systems
**Week 3 | Answer Key**

> **Note**: `data/products.csv` has a `category_id` column, not a
> `category` text column. Q8, Q9, Q12, Q14, and Q15 join `products` to
> `categories` and group by `category_name`. The marimo version of this
> lab is `sample_lab_02_instructor.py`.

---

## Part 1: String Functions (10 points)

**Q1.** (3 pts)
```sql
SELECT UPPER(CONCAT(first_name, ' ', last_name)) AS full_name_upper,
       email,
       LENGTH(email) AS email_length
FROM customers
ORDER BY email_length DESC;
```

**Q2.** (3 pts)
```sql
SELECT product_name, category_id
FROM products
WHERE product_name ILIKE '%set%'
   OR product_name ILIKE '%kit%';
```

**Q3.** (4 pts)
```sql
SELECT first_name, email,
       SPLIT_PART(email, '@', 2) AS email_domain
FROM customers
ORDER BY email_domain;
```
> Also accept: `SUBSTRING(email FROM POSITION('@' IN email) + 1)`

---

## Part 2: Date Functions (10 points)

**Q4.** (5 pts)
```sql
SELECT EXTRACT(YEAR FROM order_date) AS yr,
       EXTRACT(MONTH FROM order_date) AS mo,
       COUNT(*) AS order_count
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2024
GROUP BY yr, mo
ORDER BY mo;
```

**Q5.** (5 pts)
```sql
SELECT first_name, join_date,
       DATEDIFF('day', join_date, CURRENT_DATE) AS days_as_member
FROM customers
ORDER BY days_as_member DESC;
```
> Also accept: `CURRENT_DATE - join_date`

---

## Part 3: CASE Expressions (10 points)

**Q6.** (5 pts)

```sql
-- Individual products
SELECT product_name, price,
    CASE
        WHEN price < 15 THEN 'Economy'
        WHEN price < 50 THEN 'Standard'
        WHEN price < 150 THEN 'Premium'
        ELSE 'Luxury'
    END AS price_tier
FROM products
ORDER BY price;

-- Count per tier
SELECT
    CASE
        WHEN price < 15 THEN 'Economy'
        WHEN price < 50 THEN 'Standard'
        WHEN price < 150 THEN 'Premium'
        ELSE 'Luxury'
    END AS price_tier,
    COUNT(*) AS cnt
FROM products
GROUP BY price_tier
ORDER BY cnt DESC;
```

**Q7.** (5 pts)
```sql
SELECT
    CASE
        WHEN total_amount < 50 THEN 'Small'
        WHEN total_amount < 200 THEN 'Medium'
        WHEN total_amount < 500 THEN 'Large'
        ELSE 'Extra Large'
    END AS order_size,
    COUNT(*) AS cnt,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_value
FROM orders
GROUP BY order_size
ORDER BY avg_value;
```

---

## Part 4: GROUP BY and HAVING (20 points)

**Q8.** (5 pts)
```sql
SELECT c.category_name AS category,
       COUNT(*) AS num_products,
       ROUND(AVG(p.price), 2) AS avg_price,
       ROUND(SUM(p.price * p.stock_quantity), 2) AS total_stock_value
FROM products p, categories c
WHERE p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_stock_value DESC;
```

**Q9.** (5 pts)
```sql
SELECT c.category_name AS category, COUNT(*) AS cnt
FROM products p, categories c
WHERE p.category_id = c.category_id
  AND p.stock_quantity > 100
GROUP BY c.category_name
HAVING COUNT(*) > 5;
```

**Q10.** (5 pts)
```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 3
ORDER BY order_count DESC;
```

**Q11.** (5 pts)
```sql
SELECT EXTRACT(MONTH FROM order_date) AS mo,
       ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2024
GROUP BY mo
HAVING AVG(total_amount) > 200
ORDER BY mo;
```

---

## Part 5: Subqueries (15 points)

**Q12.** (5 pts)
```sql
SELECT p.product_name, c.category_name AS category, p.price
FROM products p, categories c
WHERE p.category_id = c.category_id
  AND p.price > (
      SELECT AVG(p2.price)
      FROM products p2
      WHERE p2.category_id = p.category_id
  )
ORDER BY c.category_name, p.price DESC;
```

**Q13.** (5 pts)
```sql
SELECT c.first_name, c.last_name,
       ROUND(SUM(o.total_amount), 2) AS total_spent
FROM customers c, orders o
WHERE c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 1;
```

**Q14.** (5 pts)
```sql
SELECT c.category_name AS category
FROM products p, categories c
WHERE p.category_id = c.category_id
GROUP BY c.category_name
HAVING MIN(p.stock_quantity) > 0;
```
> This works because if MIN(stock) > 0, no product in that category has 0 stock.

---

## Part 6: Comprehensive Query (10 points)

**Q15.** (10 pts)
```sql
SELECT c.category_name AS category,
       COUNT(*) AS num_products,
       ROUND(AVG(p.price), 2) AS avg_price,
       MIN(p.price) AS cheapest,
       MAX(p.price) AS most_expensive,
       COUNT(CASE WHEN p.stock_quantity > 0 THEN 1 END) AS in_stock,
       COUNT(CASE WHEN p.stock_quantity = 0 THEN 1 END) AS out_of_stock,
       CASE
           WHEN AVG(p.price) > (SELECT AVG(price) FROM products) THEN 'Above'
           ELSE 'Below'
       END AS vs_overall_avg
FROM products p, categories c
WHERE p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY avg_price DESC;
```

---

## Grading Rubric

| Part | Points |
|------|--------|
| Part 1: String Functions | 10 |
| Part 2: Date Functions | 10 |
| Part 3: CASE Expressions | 10 |
| Part 4: GROUP BY/HAVING | 20 |
| Part 5: Subqueries | 15 |
| Part 6: Comprehensive | 10 |
| **Total** | **75** |

