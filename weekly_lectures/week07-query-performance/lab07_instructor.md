# Lab 7: Performance & Indexing — INSTRUCTOR SOLUTIONS

## OMIS 105 — Database Management Systems
**Week 7 | Answer Key**

---

## Part 1: Understanding Query Plans (15 points)

**Q1.** (5 pts) Students should identify: SEQ_SCAN (sequential scan) on products, FILTER (price > 100), and PROJECTION (selecting product_name, price). DuckDB uses columnar scanning and filters in the scan operator.

**Q2.** (5 pts) DuckDB typically uses a HASH_JOIN for equi-joins. Students should identify: scan of both tables, the hash join on customer_id, and the filter on total_amount.

**Q3.** (5 pts) Additional operations: HASH_GROUP_BY or UNGROUPED_AGGREGATE. Students should see the scan, then the grouping/aggregation operator.

---

## Part 2: Creating and Using Indexes (15 points)

**Q4.** (5 pts)
```sql
CREATE INDEX idx_orders_status ON orders(status);
EXPLAIN SELECT * FROM orders WHERE status = 'completed';
```
> DuckDB is an analytical database and may not always use indexes the same way OLTP databases do. Students should note this. The plan may or may not show index usage — the learning point is understanding *when* indexes help.

**Q5.** (5 pts)
```sql
CREATE INDEX idx_orders_cust_date ON orders(customer_id, order_date);

EXPLAIN
SELECT * FROM orders
WHERE customer_id = 5
  AND order_date >= '2024-01-01'
ORDER BY order_date;
```

**Q6.** (5 pts)
```sql
SELECT * FROM duckdb_indexes();
DROP INDEX idx_orders_status;
```

---

## Part 3: Query Optimization (25 points)

**Q7.** (7 pts) Problems and fixes:
1. `SELECT *` — should select only needed columns
2. LEFT JOINs — since WHERE filters on products (p.category_id = 1), LEFT JOINs are effectively INNER JOINs. Use INNER JOIN explicitly.
3. Start from the most filtered table

```sql
SELECT c.first_name, c.last_name,
       o.order_id, o.order_date,
       p.product_name, oi.quantity
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
INNER JOIN orders o ON oi.order_id = o.order_id
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE p.category_id = 1
ORDER BY o.order_date DESC;
```

**Q8.** (6 pts)
```sql
SELECT * FROM orders
WHERE order_date >= '2024-06-01'
  AND order_date < '2024-07-01';
```
> This allows an index on order_date to be used directly instead of computing EXTRACT on every row.

**Q9.** (6 pts)
```sql
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.customer_id
      AND o.total_amount > 500
);
```
> EXISTS stops scanning after finding the first match, while IN must build the complete list. For large subquery result sets, EXISTS is typically faster.

**Q10.** (6 pts)
```sql
-- Index recommendations:
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Query rewrite using CTE for clarity:
WITH order_summary AS (
    SELECT customer_id,
           COUNT(*) AS total_orders,
           ROUND(SUM(total_amount), 2) AS total_spent,
           ROUND(AVG(total_amount), 2) AS avg_order
    FROM orders
    GROUP BY customer_id
)
SELECT c.first_name, c.last_name, c.email,
       COALESCE(os.total_orders, 0) AS total_orders,
       COALESCE(os.total_spent, 0) AS total_spent,
       COALESCE(os.avg_order, 0) AS avg_order
FROM customers c
LEFT JOIN order_summary os ON c.customer_id = os.customer_id
ORDER BY total_spent DESC;
```
> Pre-aggregating in a CTE reduces the join size. Index on orders(customer_id) speeds the GROUP BY.

---

## Part 4: Performance Measurement (10 points)

**Q11.** (5 pts)
```python
def time_query(con, sql, runs=5):
    times = []
    for _ in range(runs):
        start = time.time()
        con.sql(sql).fetchall()
        times.append((time.time() - start) * 1000)
    avg = sum(times) / len(times)
    print(f"  Avg: {avg:.2f}ms over {runs} runs")
    return avg

# Query A: Subquery approach
print("Query A (subquery):")
qa = """
    SELECT c.first_name, c.last_name, SUM(o.total_amount) AS spent
    FROM customers c JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
    HAVING SUM(o.total_amount) > (
        SELECT AVG(total_per_cust) FROM (
            SELECT SUM(total_amount) AS total_per_cust
            FROM orders GROUP BY customer_id
        )
    )
"""
time_query(con, qa)

# Query B: CTE approach
print("Query B (CTE):")
qb = """
    WITH cust_totals AS (
        SELECT customer_id, SUM(total_amount) AS spent
        FROM orders GROUP BY customer_id
    )
    SELECT c.first_name, c.last_name, ct.spent
    FROM customers c JOIN cust_totals ct ON c.customer_id = ct.customer_id
    WHERE ct.spent > (SELECT AVG(spent) FROM cust_totals)
"""
time_query(con, qb)
```

**Q12.** (5 pts) Students should create a larger table and re-run:
```python
con.sql("""
    CREATE TABLE orders_big AS
    SELECT * FROM orders
    UNION ALL SELECT * FROM orders
    UNION ALL SELECT * FROM orders
    -- ... repeat 10 times
""")
# Then re-run timing comparisons
```
> With larger data, the CTE approach typically maintains or improves relative performance because the subquery is only computed once.

---

## Part 5: Index Design Challenge (10 points)

**Q13.** (10 pts) Recommended indexes:

| Query | Recommended Index | Reasoning |
|-------|------------------|-----------|
| 1 | `orders(customer_id, status)` | Composite covers both filter columns |
| 2 | `products(category_id, price DESC)` | Covers filter + sort |
| 3 | `order_items(order_id)` | Direct lookup by FK |
| 4 | `reviews(product_id, review_date DESC)` | Covers filter + sort |
| 5 | `orders(order_date)` | Range scan on date |

Notes:
- Query 1 and 5 both involve orders — could consider a single composite but the use cases are different enough to warrant separate indexes.
- order_items(order_id) may already be fast if order_id is part of the PK.
- Trade-off: 5 indexes will slow INSERT/UPDATE on these tables. If write volume is high, prioritize the most frequent queries.

---

## Grading Rubric

| Part | Points |
|------|--------|
| Part 1: Query Plans | 15 |
| Part 2: Indexes | 15 |
| Part 3: Optimization | 25 |
| Part 4: Measurement | 10 |
| Part 5: Index Design | 10 |
| **Total** | **75** |

