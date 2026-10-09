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

# Setup: Load This Week's Data

Run this once (from the `week07-query-performance` folder):

```sql
CREATE OR REPLACE TABLE customers   AS SELECT * FROM read_csv('data/customers.csv');
CREATE OR REPLACE TABLE orders      AS SELECT * FROM read_csv('data/orders.csv');
CREATE OR REPLACE TABLE order_items AS SELECT * FROM read_csv('data/order_items.csv');
CREATE OR REPLACE TABLE products    AS SELECT * FROM read_csv('data/products.csv');
CREATE OR REPLACE TABLE categories  AS SELECT * FROM read_csv('data/categories.csv');
```

---

# Session 1: How Queries Execute

---

# The Query Processing Pipeline

```
SQL Query
    ↓
Parser (syntax check)
    ↓
Binder (do the tables and columns exist?)
    ↓
Optimizer (find a good execution plan)
    ↓
Execution Engine (run the plan)
    ↓
Results
```

---

# Query Optimizer's Job

Given a SQL query, the optimizer:
1. Considers different **execution plans** (join order, join method, ...)
2. Estimates the **cost** of each plan
3. Chooses the cheapest plan it finds

Costs are based on: estimated number of rows, disk I/O, memory, CPU work.
The estimates can be wrong — the plan is a good guess, not a guarantee.

---

# Full Table Scan

Without an index, the database reads **every row** and keeps the matches:

```sql
SELECT * FROM products WHERE price > 100;   -- 28 of 64 products match
```

It must check all 64 rows to find the 28 matches.
For 10 million rows, a row-by-row scan takes much longer.

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

Using the prices from the table above:

```
                     [79]
                   /      \
          [12.99, 29]      [349]
          /    |    \      /    \
      [5.99] [12.99] [29, 49.99] [79] [349, 899]
         ↓      ↓      ↓    ↓     ↓    ↓    ↓
      row 7  row 4  row 2 row 6 row 3 row 5 row 1
```

- A **balanced tree**: every lookup takes the same few steps
- Search time grows like log(n), not n: about 20 steps for 1 million rows,
  instead of checking all 1 million
- In PostgreSQL and MySQL, great for: `=`, ranges (`>`, `BETWEEN`), and sorting

DuckDB uses a different tree, the **ART** (Adaptive Radix Tree), and uses it mainly for `=` lookups.

---

# Creating Indexes in DuckDB

```sql
-- Index on a single column
CREATE INDEX idx_products_price ON products(price);

-- Index on category_id for frequent filtering
CREATE INDEX idx_products_category ON products(category_id);

-- Composite index (multiple columns)
CREATE INDEX idx_orders_cust_date
ON orders(customer_id, order_date);

-- Unique index (also enforces uniqueness)
CREATE UNIQUE INDEX idx_customers_email ON customers(email);
```

A `PRIMARY KEY` or `UNIQUE` constraint creates an index automatically.

The unique index now rejects duplicates:

```sql
INSERT INTO customers (customer_id, email) VALUES (99, 'alice.smith@email.com');
-- Constraint Error: Duplicate key "email: alice.smith@email.com"
-- violates unique constraint.
```

---

# When Indexes Help (in Row-Based Databases)

In PostgreSQL, MySQL, Oracle, and SQL Server:

| Query Pattern | Index Type | Example |
|--------------|-----------|---------|
| WHERE col = value | Single column | `WHERE email = 'alice.smith@email.com'` |
| WHERE col > value | Single column | `WHERE price > 400` |
| WHERE a = x AND b > y | Composite | `WHERE customer_id = 5 AND order_date > DATE '2024-06-01'` |
| ORDER BY col | Single column | `ORDER BY price DESC LIMIT 10` |
| JOIN ON col | Single column | `ON o.customer_id = c.customer_id` |

---

# When Indexes Help in DuckDB

DuckDB uses an index **only** when a filter matches **very few rows**
(by default, at most 2,048 rows or 0.1% of the table).

Tested on a 5-million-row table with an index on `cust`:

| Query | Index used? |
|-------|-------------|
| `WHERE cust = 42` (about 50 rows) | ✅ Yes |
| `WHERE cust > 99990` (few rows) | ✅ Yes |
| `WHERE cust BETWEEN 10 AND 20` | ❌ No — scan |
| `WHERE cust IN (1, 2, 3)` | ❌ No — scan |
| `ORDER BY cust DESC LIMIT 10` | ❌ No — uses a fast "top N" sort |

For everything else, DuckDB's columnar scan is already fast.
Indexes in DuckDB matter most for **`PRIMARY KEY` and `UNIQUE` checks**.

---

# When Indexes Do NOT Help

- **Small tables** (full scan is fast enough)
- **Low-selectivity** columns — few different values (e.g., TRUE/FALSE, or `status`)
- **Expressions** that do not match the index (e.g., `WHERE UPPER(name) = 'LAPTOP'`
  cannot use an index on `name`)
- **Heavy writes** (indexes slow down INSERT/UPDATE/DELETE)
- **Selecting many rows** — then a scan is cheaper. (A common rule of thumb in
  row-based databases is "more than about 5–20% of the rows"; DuckDB's limit is far lower.)

---

# Index Trade-offs

| Benefit | Cost |
|---------|------|
| Faster reads (SELECT) | Slower writes (INSERT/UPDATE/DELETE) |
| Faster sorts (ORDER BY) — in row-based databases | Extra storage space |
| Faster joins | Maintenance overhead |
| Faster lookups | Must choose wisely |

Measured in DuckDB: inserting 500,000 rows took **0.16 s** with an index,
and **0.01 s** without one — about 12 times slower.

---

# EXPLAIN — Seeing the Query Plan

```sql
EXPLAIN SELECT * FROM products WHERE price > 100;
```

Shows the **plan** DuckDB will use, as a tree of operators:
- How each table is read (`SEQ_SCAN`, with the filters it applies)
- How tables are joined (`HASH_JOIN`, ...)
- Sorting, grouping, and `LIMIT` steps
- The **estimated** number of rows at each step (e.g., `~12 rows`)

`EXPLAIN ANALYZE` actually **runs** the query and shows the real row counts and time.

---

# Reading EXPLAIN Output

```sql
EXPLAIN SELECT p.product_name, cat.category_name
FROM products p
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE p.price > 100;
```

DuckDB's plan (read it from the **bottom up**):

```
HASH_JOIN  (Join Type: INNER, category_id = category_id)  ~10 rows
├── SEQ_SCAN products    Filters: price>100.0             ~12 rows
└── SEQ_SCAN categories                                    ~8 rows
```

Look for:
- **SEQ_SCAN** — reads the table (DuckDB's normal, fast columnar scan)
- **Filters:** — the `WHERE` condition, applied *during* the scan
- **HASH_JOIN** — DuckDB's usual join method
- **~N rows** — an *estimate*: really 28 products cost more than 100, not ~12

Note: plain `EXPLAIN` always shows "Sequential Scan". DuckDB decides to use an
index at run time, so only `EXPLAIN ANALYZE` shows "Index Scan".

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
```sql
SELECT c.first_name, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed' AND o.total_amount > 500;
```

Written this way, it *looks* like "join everything, then filter".
But the optimizer **pushes the filter down**: it filters `orders`
**before** the join (check with `EXPLAIN`: the filter appears inside the `SEQ_SCAN` of `orders`).

Your job: write the filters you need in `WHERE`. Filters on large tables
that remove many rows help the most.

---

# Optimization Tip 2: Select Only Needed Columns

```sql
-- BAD: Select everything
SELECT * FROM orders;

-- BETTER: Select only what you need
SELECT order_id, order_date, total_amount FROM orders;
```

Less data transferred, less memory used.
In a **columnar** database like DuckDB, this matters even more:
columns you do not select are not read at all.

---

# Optimization Tip 3: EXISTS vs. IN

```sql
-- IN with a subquery
SELECT * FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);

-- EXISTS (can stop at the first match)
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

In older databases, `EXISTS` was often faster. Modern optimizers —
including DuckDB's — turn **both** into the same plan (a *semi join*).
Check with `EXPLAIN`: you will see `HASH_JOIN` with a `SEMI` join type in both.

Choose the one that is easier to read. (But remember from Week 5:
`NOT IN` behaves badly when the subquery returns `NULL`; `NOT EXISTS` does not.)

---

# Optimization Tip 4: Avoid Functions on Indexed Columns

```sql
-- BAD: the function hides the column; an index on order_date can't be used
SELECT * FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2024;

-- BETTER: compare the column directly
SELECT * FROM orders
WHERE order_date >= DATE '2024-01-01' AND order_date < DATE '2025-01-01';
```

Both return the same 182 orders. In DuckDB, the direct comparison also lets
the scan **skip whole blocks** of rows using their stored min/max dates.

---

# Optimization Tip 5: Use Appropriate JOIN Types

```sql
-- If you don't need unmatched rows, use INNER JOIN
-- (LEFT JOIN must keep extra rows, and gives the optimizer fewer choices)

-- To find rows with NO match, NOT EXISTS states the goal directly
SELECT * FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

DuckDB runs this as an **anti join** (`Join Type: ANTI`).
LEFT JOIN + `IS NULL` gives the same answer; both are fine.
In our data, every customer has orders, so this returns 0 rows.

---

# Optimization Tip 6: LIMIT with ORDER BY

```sql
SELECT * FROM orders ORDER BY total_amount DESC LIMIT 10;
```

A smart database does **not** sort all rows here. It keeps only the
**top 10 seen so far** while it reads (DuckDB's `TOP_N` operator).
Much less work than a full sort.

- In PostgreSQL/MySQL, an index on `total_amount` can make this even faster:
  read the first 10 index entries and stop.
- DuckDB does **not** use an index for `ORDER BY`; `TOP_N` is already fast.

Always use `ORDER BY` with `LIMIT` — without it, the "top 10" is random.

---

# DuckDB-Specific Optimizations

DuckDB uses **columnar storage**:
- Only reads the columns the query uses (not entire rows)
- Stores min/max values per block of rows, and **skips** blocks that cannot match
- **Vectorized** execution: processes batches of about 2,048 values at a time
- Automatic **parallelism**: uses all CPU cores

```sql
-- DuckDB automatically parallelizes this (on large tables)
SELECT category_id, SUM(price) FROM products GROUP BY category_id;
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

- **Column storage** excels at analytics: aggregating a few columns over many rows (OLAP).
- **Row storage** excels at transactions: reading or changing one whole row at a time (OLTP).

---

# Monitoring Query Performance

In the DuckDB command-line tool:

```
.timer on
SELECT COUNT(*) FROM orders;
-- Run Time (s): real 0.001 ...
```

In Python (for example, in a Marimo notebook):

```python
import time
start = time.perf_counter()
result = con.execute("SELECT COUNT(*) FROM orders").fetchall()
print(f"Query took {time.perf_counter() - start:.3f} s")
```

`EXPLAIN ANALYZE SELECT ...` also shows the time spent in each step.

Run a query a few times: the first run is often slower (data loading, caches).

---

# Index Maintenance

```sql
-- List indexes
SELECT * FROM duckdb_indexes();

-- Drop an index
DROP INDEX IF EXISTS idx_products_price;

-- Rebuild: not needed — DuckDB keeps indexes up to date automatically
```

`duckdb_indexes()` lists the indexes you created with `CREATE INDEX`.
(Indexes created by `PRIMARY KEY` and `UNIQUE` are not listed there.)

---

# Best Practices Summary

1. **Write a correct query first**
2. **Index** columns used in selective `WHERE` lookups (and, in row-based databases, in JOIN and ORDER BY)
3. **Don't over-index** — each index slows writes
4. Use **EXPLAIN / EXPLAIN ANALYZE** to see what really happens
5. Select only the columns you need
6. Avoid **functions on filtered columns** in `WHERE`
7. Consider **composite indexes** for multi-column lookups
8. **Measure first**, optimize second — don't guess

---

# Summary

- Queries go through: parse → optimize → execute
- **Indexes** trade write speed for read speed (B-tree in most databases; ART in DuckDB)
- DuckDB uses an index only for very selective lookups
- **EXPLAIN** shows the plan; **EXPLAIN ANALYZE** runs it and shows real numbers
- The optimizer already pushes filters down and rewrites `IN`/`EXISTS`
- DuckDB's columnar storage gives fast scans without indexes
- Always **measure** before and after optimization

---

# What Is Next?

**Week 8: Transactions & ACID**
- `BEGIN`, `COMMIT`, `ROLLBACK`
- ACID properties
- Constraints: `CHECK`, `NOT NULL`
- Data integrity when many users work at once

---

# Questions?

Thank you!

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
