---
marp: true
theme: default
paginate: true
header: "OMIS 105 – Database Management Systems"
footer: "Week 7: Performance & Indexing"
---

# OMIS 105: Database Management Systems
## Week 7 — Performance & Indexing
### How Queries Execute and How to Make Them Faster

---

# This Week's Goals

1. Understand how a DBMS executes queries
2. Learn about indexes and when to use them
3. Use EXPLAIN to analyze query plans
4. Apply query optimization techniques
5. Understand storage and I/O fundamentals

---

# Session 1: How Queries Execute

---

# The Query Processing Pipeline

```
SQL Query
    ↓
Parser (syntax check)
    ↓
Optimizer (find best execution plan)
    ↓
Execution Engine (run the plan)
    ↓
Results
```

---

# Query Optimizer's Job

Given a SQL query, the optimizer:
1. Considers multiple **execution plans**
2. Estimates the **cost** of each plan
3. Chooses the **cheapest** plan

Costs are based on: number of rows, disk I/O, memory usage, CPU operations.

---

# Full Table Scan

Without indexes, every query reads **every row**:

```sql
SELECT * FROM products WHERE price > 100;
```

Must scan all 64 rows to find matches.
For 10 million rows? Very slow.

---

# What Is an Index?

An index is a **separate data structure** that speeds up lookups.

Like a book's index:
- Without index: read every page to find "normalization"
- With index: look up "normalization → page 127"

---

# Index Analogy

```
Table (unsorted data):          Index on price:
┌────┬──────────┬───────┐      ┌───────┬────────┐
│ id │ name     │ price │      │ price │ row_id │
├────┼──────────┼───────┤      ├───────┼────────┤
│ 1  │ Laptop   │ 899   │      │ 5.99  │   7    │
│ 2  │ Mouse    │ 29    │      │ 12.99 │   4    │
│ 3  │ Keyboard │ 79    │      │ 29.00 │   2    │
│ 4  │ USB Hub  │ 12.99 │      │ 49.99 │   6    │
│ 5  │ Monitor  │ 349   │      │ 79.00 │   3    │
│ 6  │ Webcam   │ 49.99 │      │ 349   │   5    │
│ 7  │ Cable    │ 5.99  │      │ 899   │   1    │
└────┴──────────┴───────┘      └───────┴────────┘
                                (sorted by price)
```

---

# B-Tree Index (Most Common)

```
                    [349]
                   /      \
             [29, 79]    [499, 899]
            /   |    \    /    \
        [5,12] [29] [79] [349] [499,899]
```

- Balanced tree structure
- O(log n) lookups instead of O(n) scans
- Great for: equality, range queries, sorting

---

# Creating Indexes in DuckDB

```sql
-- Index on a single column
CREATE INDEX idx_products_price ON products(price);

-- Index on category for frequent filtering
CREATE INDEX idx_products_category ON products(category);

-- Composite index (multiple columns)
CREATE INDEX idx_orders_cust_date
ON orders(customer_id, order_date);

-- Unique index (also enforces uniqueness)
CREATE UNIQUE INDEX idx_customers_email ON customers(email);
```

---

# When Indexes Help

| Query Pattern | Index Type | Example |
|--------------|-----------|---------|
| WHERE col = value | Single column | `WHERE category = 'Books'` |
| WHERE col > value | Single column | `WHERE price > 100` |
| WHERE a = x AND b = y | Composite | `WHERE cust_id = 5 AND date > '2024-01'` |
| ORDER BY col | Single column | `ORDER BY price DESC` |
| JOIN ON col | Single column | `ON o.customer_id = c.customer_id` |

---

# When Indexes Do NOT Help

- **Small tables** (full scan is fast enough)
- **Low-selectivity** columns (e.g., boolean: TRUE/FALSE)
- **Expressions** not matching the index (e.g., `WHERE UPPER(name) = 'LAPTOP'`)
- **Heavy writes** (indexes slow down INSERT/UPDATE/DELETE)
- **Selecting most rows** (optimizer ignores index when >15-20% of rows match)

---

# Index Trade-offs

| Benefit | Cost |
|---------|------|
| Faster reads (SELECT) | Slower writes (INSERT/UPDATE/DELETE) |
| Faster sorts (ORDER BY) | Extra storage space |
| Faster joins | Maintenance overhead |
| Faster lookups | Must choose wisely |

---

# EXPLAIN — Seeing the Query Plan

```sql
EXPLAIN SELECT * FROM products WHERE price > 100;
```

Shows you exactly how DuckDB will execute the query:
- What scans it uses (sequential vs. index)
- Join algorithms
- Sort methods
- Estimated costs

---

# Reading EXPLAIN Output

```sql
EXPLAIN SELECT p.product_name, cat.category_name
FROM products p
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE p.price > 100;
```

Look for:
- **Seq Scan** (full table scan — potentially slow)
- **Index Scan** (using an index — fast)
- **Hash Join** vs **Nested Loop** vs **Merge Join**
- **Filter** (WHERE clause applied)

---

# Session 2: Query Optimization

---

# Optimization Strategy

```
1. Write correct query first
2. EXPLAIN to see the plan
3. Identify bottlenecks (full scans, bad joins)
4. Add indexes where beneficial
5. Rewrite query if needed
6. EXPLAIN again to verify improvement
```

---

# Optimization Tip 1: Filter Early

```sql
-- BAD: Join everything, then filter
SELECT c.first_name, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed' AND o.total_amount > 500;

-- BETTER: Optimizer usually handles this, but be explicit
-- Use indexed columns in WHERE
-- Put selective filters on indexed columns
```

---

# Optimization Tip 2: Select Only Needed Columns

```sql
-- BAD: Select everything
SELECT * FROM orders;

-- BETTER: Select only what you need
SELECT order_id, order_date, total_amount FROM orders;
```

Less data transferred, less memory used.

---

# Optimization Tip 3: Use EXISTS Instead of IN

```sql
-- Slower (for large subqueries)
SELECT * FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);

-- Faster (stops at first match)
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

---

# Optimization Tip 4: Avoid Functions on Indexed Columns

```sql
-- BAD: Index on order_date won't be used
SELECT * FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2024;

-- BETTER: Rewrite to use the column directly
SELECT * FROM orders
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';
```

---

# Optimization Tip 5: Use Appropriate JOIN Types

```sql
-- If you don't need unmatched rows, use INNER JOIN
-- LEFT JOIN is more expensive if you don't need NULLs

-- For existence checks, use EXISTS instead of LEFT JOIN + IS NULL
SELECT * FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

---

# Optimization Tip 6: LIMIT with ORDER BY

```sql
-- Without index, must sort ALL rows then take top 10
SELECT * FROM orders ORDER BY total_amount DESC LIMIT 10;

-- With index on total_amount, can stop after 10 rows
CREATE INDEX idx_orders_total ON orders(total_amount);
SELECT * FROM orders ORDER BY total_amount DESC LIMIT 10;
```

---

# DuckDB-Specific Optimizations

DuckDB uses **columnar storage**:
- Only reads columns you SELECT (not entire rows)
- Vectorized execution (processes batches of values)
- Automatic parallelism

```sql
-- DuckDB automatically parallelizes this
SELECT category, SUM(price) FROM products GROUP BY category;
```

---

# Columnar vs. Row Storage

```
Row-oriented (PostgreSQL, MySQL):
[id=1, name="Laptop", price=899] [id=2, name="Mouse", price=29] ...

Column-oriented (DuckDB):
id:    [1, 2, 3, 4, ...]
name:  ["Laptop", "Mouse", "Keyboard", ...]
price: [899, 29, 79, ...]
```

Column storage excels at analytics (aggregating one column across many rows).

---

# Monitoring Query Performance

```sql
-- DuckDB: time a query
.timer on
SELECT ... ;

-- Or in Python
import time
start = time.time()
result = con.sql("SELECT ...").fetchall()
print(f"Query took {time.time() - start:.3f}s")
```

---

# Index Maintenance

```sql
-- List indexes
SELECT * FROM duckdb_indexes();

-- Drop an index
DROP INDEX IF EXISTS idx_products_price;

-- Rebuild (after many inserts/updates)
-- DuckDB handles this automatically
```

---

# Best Practices Summary

1. **Index** columns used in WHERE, JOIN, ORDER BY
2. **Don't over-index** — each index slows writes
3. Use **EXPLAIN** to verify your optimizations
4. **Filter early**, select only needed columns
5. Avoid **functions on indexed columns** in WHERE
6. Use **EXISTS** over IN for large subqueries
7. Consider **composite indexes** for multi-column queries
8. **Profile first**, optimize second — don't guess

---

# Summary

- Queries go through: parse → optimize → execute
- **Indexes** trade write speed for read speed (B-Tree is most common)
- **EXPLAIN** reveals the query execution plan
- Optimization: filter early, select needed columns, proper JOINs
- DuckDB's columnar storage provides automatic optimizations
- Always **measure** before and after optimization

---

# What Is Next?

**Week 8: Transactions & ACID**
- ACID properties
- Concurrency control
- Isolation levels
- Data integrity under concurrent access

---

# Questions?

Thank you!

