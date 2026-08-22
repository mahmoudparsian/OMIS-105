# Lab 7: Performance & Indexing

## OMIS 105 — Database Management Systems
**Week 7 | Estimated time: 75–90 minutes**

---

## Setup

```python
import duckdb, time
con = duckdb.connect()
for t, f in [('categories','categories.csv'),('products','products.csv'),
             ('customers','customers.csv'),('orders','orders.csv'),
             ('order_items','order_items.csv'),('reviews','reviews.csv'),
             ('shipping','shipping.csv'),('suppliers','suppliers.csv'),
             ('product_suppliers','product_suppliers.csv')]:
    con.sql(f"CREATE TABLE {t} AS SELECT * FROM read_csv_auto('{f}')")
```

---

## Part 1: Understanding Query Plans (15 points)

**Q1.** Run `EXPLAIN` on the following query and describe what you see. What operations does DuckDB use?

```sql
EXPLAIN
SELECT product_name, price FROM products WHERE price > 100;
```

**Q2.** Run `EXPLAIN` on a JOIN query. Identify the join algorithm DuckDB chooses.

```sql
EXPLAIN
SELECT c.first_name, o.order_id, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > 300;
```

**Q3.** Run `EXPLAIN` on a query with GROUP BY. What additional operations appear?

```sql
EXPLAIN
SELECT category_id, COUNT(*), AVG(price)
FROM products
GROUP BY category_id;
```

---

## Part 2: Creating and Using Indexes (15 points)

**Q4.** Create an index on `orders(status)`. Then run EXPLAIN on a query filtering by status. Does the plan change?

```sql
-- Create index, then EXPLAIN
```

**Q5.** Create a composite index on `orders(customer_id, order_date)`. Write a query that would benefit from this index and run EXPLAIN.

```sql
-- Your index + query + EXPLAIN
```

**Q6.** List all indexes you have created using `SELECT * FROM duckdb_indexes()`. Then drop one of them.

```sql
-- Your queries here
```

---

## Part 3: Query Optimization (25 points)

**Q7.** The following query is inefficient. Identify the problems and rewrite it for better performance. Explain each change.

```sql
SELECT *
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE p.category_id = 1
ORDER BY o.order_date DESC;
```

**Q8.** Rewrite this query to avoid using a function on an indexed column:

```sql
SELECT * FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2024
  AND EXTRACT(MONTH FROM order_date) = 6;
```

**Q9.** Rewrite this query using EXISTS instead of IN. Explain why EXISTS can be faster.

```sql
SELECT * FROM customers
WHERE customer_id IN (
    SELECT customer_id FROM orders
    WHERE total_amount > 500
);
```

**Q10.** This query runs slowly on large tables. Optimize it.

```sql
SELECT c.first_name, c.last_name, c.email,
       COUNT(o.order_id) AS total_orders,
       SUM(o.total_amount) AS total_spent,
       AVG(o.total_amount) AS avg_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
ORDER BY total_spent DESC;
```

Suggest what indexes would help and any query rewrites.

---

## Part 4: Performance Measurement (10 points)

**Q11.** Write a Python function that times a query and returns the execution time in milliseconds. Use it to compare the performance of two equivalent queries:

Query A (subquery): Find customers whose total spending exceeds the average customer spending.
Query B (CTE): Same result, different approach.

```python
# Your timing function and two queries
```

**Q12.** Generate a larger dataset by duplicating the orders table 10 times. Re-run your comparison from Q11 on the larger dataset. Does the relative performance change?

```python
# Your code here
```

---

## Part 5: Index Design Challenge (10 points)

**Q13.** You are told that the ShopSmart application runs these 5 queries most frequently:

1. `SELECT * FROM orders WHERE customer_id = ? AND status = 'completed'`
2. `SELECT * FROM products WHERE category_id = ? ORDER BY price DESC`
3. `SELECT * FROM order_items WHERE order_id = ?`
4. `SELECT * FROM reviews WHERE product_id = ? ORDER BY review_date DESC`
5. `SELECT * FROM orders WHERE order_date BETWEEN ? AND ?`

Design an index strategy: which indexes would you create? For each, explain your reasoning. Are there any indexes you would NOT create, and why?

---

## Submission

- Submit notebook with all queries, EXPLAIN outputs, timing results, and written analysis
- **Total: 75 points**

