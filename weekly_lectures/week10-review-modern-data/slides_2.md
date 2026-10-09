---
marp: true
theme: default
paginate: true
header: "OMIS 105 – Database Management Systems"
footer: "Week 10: Synthesis & Review"
---

# OMIS 105: Database Management Systems
## Week 10 — Synthesis & Review
### Bringing It All Together

---

# This Week's Agenda

**Session 1**: Capstone Presentations + Modern Database Trends + Modern Data in SQL
**Session 2**: Comprehensive Review + Exam Preparation

---

# Session 1: Beyond Relational — Modern Trends

---

# The Database Landscape in 2026

The relational model is still dominant, but the landscape has expanded:

- NoSQL databases
- NewSQL databases
- Cloud-native databases
- Data lakes and lakehouses
- Vector databases (for AI/ML)

---

# NoSQL: Not Only SQL

| Type | Examples | Best For |
|------|---------|---------|
| Document | MongoDB, CouchDB | Flexible schemas, JSON data |
| Key-Value | Redis, DynamoDB | Caching, session storage |
| Wide-Column | Cassandra, HBase | Time-series, IoT, very large scale |
| Graph | Neo4j, Amazon Neptune | Social networks, recommendations |

---

# When Relational vs. NoSQL?

| Choose Relational When | Choose NoSQL When |
|----------------------|------------------|
| Data has clear structure | Schema changes frequently |
| Complex queries needed | Simple key-based lookups |
| ACID is critical | Eventual consistency is OK |
| Joins are common | Data is denormalized |
| Moderate scale (one server is enough) | Massive horizontal scale (many servers) |

Many systems use **both**. And the line is blurring: PostgreSQL and DuckDB
can store and query JSON documents too (see "Modern Data in SQL").

---

# NewSQL: Best of Both Worlds

Databases that combine:
- SQL interface and relational model
- NoSQL-like horizontal scalability
- Full ACID compliance

Examples: CockroachDB, Google Spanner, TiDB

---

# Cloud Databases

| Service | Provider | Type |
|---------|----------|------|
| Amazon RDS | AWS | Managed relational (MySQL, PostgreSQL) |
| Amazon Aurora | AWS | Cloud-native relational |
| Azure SQL | Microsoft | Managed SQL Server |
| Google Cloud SQL | Google | Managed relational |
| Google BigQuery | Google | Serverless analytics (columnar) |
| Snowflake | Snowflake | Cloud data warehouse |

---

# DuckDB's Place in the Ecosystem

DuckDB is an **analytical (OLAP)** database:

| OLTP (Transactional) | OLAP (Analytical) |
|----------------------|-------------------|
| PostgreSQL, MySQL | DuckDB, BigQuery |
| Many small transactions | Few complex queries |
| Row-oriented storage | Column-oriented storage |
| Current state of data | Historical analysis |
| Online store checkout | Monthly sales report |

DuckDB runs **inside** your program (like a library), with no server to install.
That is why we could use it on a laptop in a Marimo notebook.

---

# Data Lakes and Lakehouses

**Data Lake**: Store raw data in any format (Parquet, CSV, JSON)
**Lakehouse**: Data lake + database-like query capabilities

```sql
-- DuckDB can query Parquet files directly (no CREATE TABLE needed)!
SELECT product_category, SUM(amount) AS revenue
FROM read_parquet('sales_2024.parquet')
WHERE region = 'West'
GROUP BY product_category;
```

**Parquet** is a compressed, column-oriented file format — the standard
file type of data lakes. (A runnable example is on the ETL slide.)

---

# Vector Databases (The AI Connection)

Store and search **vector embeddings** for AI/ML:
- Similarity search ("find similar products")
- Recommendation engines
- Semantic text search

Examples: Pinecone, Weaviate, Milvus, pgvector

---

# The DBA Role

A **Database Administrator (DBA)** manages:

| Responsibility | Description |
|---------------|-------------|
| Schema design | Create and maintain table structures |
| Performance | Monitor queries, add indexes, tune configs |
| Security | Manage users, roles, permissions |
| Backup/Recovery | Regular backups, disaster recovery plans |
| Capacity planning | Predict growth, scale infrastructure |
| Migration | Upgrade versions, move between platforms |

---

# Database Security

Key security concepts:

```sql
-- PostgreSQL syntax
-- Create a role with specific permissions
CREATE ROLE analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst;

-- Create a user and give them the role
CREATE USER intern WITH PASSWORD 'secure_pass';
GRANT analyst TO intern;

-- Revoke access
REVOKE INSERT, UPDATE, DELETE ON orders FROM intern;
```

- **Principle of least privilege:** give each user only the access they need
- DuckDB has **no** users, roles, or `GRANT` — it runs inside one program,
  so access is controlled by who can open the database file.
  These commands matter in multi-user servers (PostgreSQL, MySQL, SQL Server).

---

# Backup and Recovery

| Strategy | Description | Trade-off |
|----------|------------|-----------|
| Full backup | Copy the entire database | Slow to take; simplest to restore |
| Incremental | Copy only the changes since the last backup | Fast to take; restore needs the full backup **plus** every incremental |
| Point-in-time | Restore a backup, then replay the WAL (log) up to a chosen moment | Can undo a mistake made at 2:15 pm |
| Replication | A live copy on a standby server | Near-instant failover — but it also copies mistakes |

A backup you have never tested restoring is not a backup.

---

# ETL: Extract, Transform, Load

Moving data between systems:

```
Source Systems → Extract → Transform → Load → Data Warehouse
 (OLTP DBs,      (Read      (Clean,       (Insert
  APIs, files)    data)      reshape)       into DW)
```

DuckDB excels at the Transform step (run from the `week10-review-modern-data` folder):
```sql
-- Extract from CSV, transform (group), load into a Parquet file
COPY (
    SELECT category_id,
           COUNT(*)             AS products,
           ROUND(AVG(price), 2) AS avg_price
    FROM read_csv('data/products.csv')
    GROUP BY category_id
) TO 'category_summary.parquet' (FORMAT PARQUET);

-- Query the new Parquet file directly
SELECT * FROM read_parquet('category_summary.parquet')
WHERE avg_price > 80;              -- 5 of the 8 categories
```

---

# Modern Data in SQL

Real data is not always neat rows and columns:

- **JSON**: app and web data with flexible fields
- **Lists**: several values in one cell (tags, items in a basket)
- **PIVOT**: turning row values into columns (a spreadsheet-style report)
- **CROSS JOIN**: every combination of two lists

DuckDB handles all of these with SQL.

---

# JSON: Querying Flexible Data

```sql
CREATE OR REPLACE TABLE events AS
SELECT * FROM (VALUES
    (1, 'Alice', '{"device": "mobile", "page": "/cart", "items": 3}'::JSON),
    (2, 'Bob',   '{"device": "laptop", "page": "/home"}'::JSON),
    (3, 'Alice', '{"device": "mobile", "page": "/checkout", "items": 2}'::JSON)
) AS t(event_id, customer, metadata);

SELECT event_id, customer,
       metadata->>'device'               AS device,
       metadata->>'page'                 AS page,
       (metadata->>'items')::INTEGER     AS items
FROM events;
```

| event_id | customer | device | page | items |
|---|---|---|---|---|
| 1 | Alice | mobile | /cart | 3 |
| 2 | Bob | laptop | /home | NULL |
| 3 | Alice | mobile | /checkout | 2 |

- `->>'key'` returns the value as **text**; cast it (`::INTEGER`) to do math
- A missing key gives `NULL` (Bob's event has no `items`)

---

# JSON: Group by a JSON Field

```sql
SELECT metadata->>'device' AS device,
       COUNT(*)            AS events
FROM events
GROUP BY device
ORDER BY events DESC;
```

| device | events |
|---|---|
| mobile | 2 |
| laptop | 1 |

Once extracted, a JSON field works like any other column:
`WHERE`, `GROUP BY`, `ORDER BY`, ...

---

# LIST and UNNEST

A **LIST** holds several values in one cell:

```sql
CREATE OR REPLACE TABLE baskets AS
SELECT * FROM (VALUES
    (1, 'Alice', ['laptop', 'mouse']),
    (2, 'Bob',   ['phone']),
    (3, 'Cara',  ['laptop', 'case', 'charger'])
) AS t(order_id, customer, items);

SELECT order_id, len(items) AS n_items, items[1] AS first_item
FROM baskets;                -- list positions start at 1
```

**UNNEST** turns a list into rows (one row per value):

```sql
SELECT order_id, UNNEST(items) AS item
FROM baskets;                -- 6 rows: laptop, mouse, phone, laptop, case, charger
```

The opposite — rows into a list — is the `list()` aggregate:
`SELECT customer, list(event_id) FROM events GROUP BY customer;`

(A list in a cell breaks 1NF! It is handy for analysis, but keep your
core tables normalized.)

---

# PIVOT: Rows into Columns

```sql
CREATE OR REPLACE TABLE sales AS
SELECT * FROM (VALUES
    ('West', 'Q1', 100), ('West', 'Q2', 150), ('West', 'Q1', 20),
    ('East', 'Q1',  80), ('East', 'Q2', 120)
) AS t(region, quarter, amount);

PIVOT sales
ON quarter
USING SUM(amount)
GROUP BY region
ORDER BY region;
```

| region | Q1 | Q2 |
|---|---|---|
| East | 80 | 120 |
| West | 120 | 150 |

- `ON quarter`: each quarter value becomes a **column**
- `USING SUM(amount)`: what goes in each cell (West Q1 = 100 + 20)
- `UNPIVOT` does the opposite (columns back into rows)

---

# CROSS JOIN: Every Combination

```sql
SELECT s.size, c.color
FROM (VALUES ('S'), ('M'), ('L')) AS s(size)
CROSS JOIN (VALUES ('red'), ('blue')) AS c(color)
ORDER BY ALL;
```

3 sizes × 2 colors = **6 rows** (every size in every color).

Useful for: product variants, calendars (every store × every day),
and finding missing combinations. There is **no** `ON` clause.

---

# Session 2: Comprehensive Review

---

# Course Map

```
Week 1: Foundations (SELECT, WHERE, ORDER BY) ───┐
Week 2: Relational Model (keys, relationships) ──┤
Week 3: SQL Basics (functions, CASE, GROUP BY) ──┤
Week 4: Aggregation + first JOINs ───────────────┤
Week 5: JOINs, IS NULL, COALESCE ────────────────┤ → Week 9: Project
Week 6: Normalization (1NF → BCNF) ──────────────┤
Week 7: Performance (indexes, EXPLAIN) ──────────┤
Week 8: Transactions (ACID, constraints) ────────┘
                                   Week 10: Review + Modern Data
```

---

# Review: Database Fundamentals (Weeks 1–3)

**Key concepts**:
- Database vs. flat file
- DBMS: software layer between apps and data
- Tables, rows, columns, schemas
- Data types: INTEGER, VARCHAR, DECIMAL, DATE, BOOLEAN
- Constraints: PRIMARY KEY, NOT NULL, UNIQUE, CHECK, DEFAULT

```sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    price DECIMAL(10,2) CHECK (price > 0)
);
```

---

# Review: Relational Model (Week 2)

**Key concepts**:
- Primary Key (PK): uniquely identifies each row
- Foreign Key (FK): references another table's PK
- Candidate Key, Composite Key
- Relationships: 1:1, 1:M, M:M (junction tables)
- Referential integrity
- ER diagrams (Crow's Foot notation)

**Critical rule**: FK in the "many" side table.

---

# Review: SQL — SELECT and Functions (Week 3)

```sql
SELECT columns           -- what to show
FROM table               -- where to look
WHERE conditions         -- filter rows
GROUP BY columns         -- group rows
HAVING agg_condition     -- filter groups
ORDER BY columns         -- sort
LIMIT n OFFSET m;        -- restrict output
```

Functions: UPPER, LOWER, CONCAT, ROUND, EXTRACT, CASE, COALESCE

---

# Review: SQL — JOINs (Weeks 4–5)

| JOIN | Returns |
|------|---------|
| INNER JOIN | Only matching rows |
| LEFT JOIN | All from left + matches from right |
| RIGHT JOIN | All from right + matches from left |
| FULL OUTER JOIN | All rows from both |
| CROSS JOIN | Cartesian product |
| Self JOIN | Table joined with itself |

```sql
SELECT c.first_name, o.order_id
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- Find non-matches: LEFT JOIN + IS NULL
SELECT c.first_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

`COALESCE(x, 0)` replaces `NULL` with 0 (e.g., a customer with no orders).

---

# Review: SQL — Advanced (Week 5 preview, Weeks 7 and 9)

**Window functions**: compute across rows without collapsing
```sql
ROW_NUMBER() OVER (PARTITION BY cat ORDER BY price DESC)
LAG(value) OVER (ORDER BY date)
SUM(amount) OVER (ORDER BY date) -- running total
```

**CTEs**: named temporary result sets
```sql
WITH cte AS (SELECT ...) SELECT ... FROM cte;
```

**Set operations**: UNION, INTERSECT, EXCEPT

**Views**: saved queries acting as virtual tables

---

# Review: Normalization (Week 6)

| NF | Rule | Eliminates |
|----|------|-----------|
| 1NF | Atomic values, no repeating groups | Multi-valued cells |
| 2NF | No partial dependencies | Partial key → non-key |
| 3NF | No transitive dependencies | Non-key → non-key |
| BCNF | Every determinant is a superkey | Remaining FD-based anomalies |

**Functional dependency**: X → Y ("knowing X determines Y")

---

# Review: Performance (Week 7)

- **Indexes**: trees (B-tree in most databases, ART in DuckDB) that speed up
  searches returning **few** rows — at a cost on every write
- **EXPLAIN** shows the plan; **EXPLAIN ANALYZE** runs it and shows real numbers
- **Optimization tips**:
  - Select only the columns you need
  - Avoid functions on filtered columns in WHERE
  - Use INNER JOIN when LEFT JOIN isn't needed
  - The optimizer already pushes filters down and treats `IN`/`EXISTS` alike
- **DuckDB**: columnar storage, vectorized and parallel execution

---

# Review: Transactions (Week 8)

**ACID**: Atomicity, Consistency, Isolation, Durability

```sql
BEGIN;
  -- multiple operations
COMMIT;    -- save all changes
ROLLBACK;  -- undo all changes
```

**Isolation levels**: READ UNCOMMITTED → READ COMMITTED → REPEATABLE READ → SERIALIZABLE
(DuckDB always uses snapshot isolation; a conflicting write fails with an error)

**Concurrency problems**: dirty read, non-repeatable read, phantom read, lost update

**Constraints** (`NOT NULL`, `CHECK`, `UNIQUE`, keys) keep the data consistent.

---

# Practice Problem 1: Schema Design

Design a schema for a **pet adoption shelter**:
- Animals (id, name, species, breed, age, status)
- Adopters (id, name, email, phone, address)
- Adoptions (which animal, which adopter, when, fee)
- Veterinary records (animal, vet, date, procedure, cost)
- Vets (id, name, clinic)

Questions:
1. What are the relationships (1:1, 1:M, M:M)?
2. Where do the FKs go?
3. Which `CHECK` and `NOT NULL` rules would you add?
4. Is this in 3NF?

---

# Practice Problem 2: SQL Query

Given ShopSmart tables, write a query that shows:
- Each category's name
- Number of products
- Total revenue (from order_items)
- The best-selling product in each category
- Whether the category is "above" or "below" the overall average revenue

*Try this before looking at the solution!*

---

# Solution: Practice Problem 2

```sql
WITH cat_revenue AS (
    SELECT cat.category_id, cat.category_name,
           COUNT(DISTINCT p.product_id) AS num_products,
           SUM(oi.quantity * oi.unit_price) AS revenue
    FROM categories cat
    JOIN products p ON cat.category_id = p.category_id
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY cat.category_id, cat.category_name
),
best_sellers AS (
    SELECT p.category_id, p.product_name,
           SUM(oi.quantity) AS total_sold,
           ROW_NUMBER() OVER (
               PARTITION BY p.category_id ORDER BY SUM(oi.quantity) DESC
           ) AS rn
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.category_id, p.product_id, p.product_name
)
SELECT cr.category_name, cr.num_products,
       ROUND(cr.revenue, 2) AS revenue,
       bs.product_name AS best_seller,
       CASE WHEN cr.revenue > (SELECT AVG(revenue) FROM cat_revenue)
            THEN 'Above' ELSE 'Below' END AS vs_average
FROM cat_revenue cr
LEFT JOIN best_sellers bs
    ON cr.category_id = bs.category_id
    AND bs.rn = 1
ORDER BY cr.revenue DESC;
```

---

# Solution: Result

| category_name | num_products | revenue | best_seller | vs_average |
|---|---|---|---|---|
| Electronics | 8 | 40431.29 | Wireless Earbuds | Above |
| Toys | 8 | 22141.36 | Science Set | Above |
| Sports | 8 | 16237.24 | Cycling Helmet | Below |
| Books | 8 | 15754.27 | SQL Cookbook | Below |
| Food & Grocery | 8 | 15125.25 | Olive Oil Extra | Below |
| Home & Kitchen | 8 | 14595.29 | Bookshelf | Below |
| Clothing | 8 | 13978.58 | Denim Jeans | Below |
| Beauty | 8 | 13679.98 | Hand Cream | Below |

Only 2 categories beat the average: Electronics is so large that it pulls
the average up. (The window function can use `SUM(oi.quantity)` because
window functions run **after** `GROUP BY`.)

---

# Practice Problem 3: Normalization

Normalize this table to 3NF:

```
employee_projects(
    emp_id, emp_name, emp_department, dept_location,
    project_id, project_name, project_budget,
    hours_worked, hourly_rate
)
```

Identify all FDs, then decompose step by step.

---

# Practice Problem 4: Transactions

Write a transaction for: "An employee transfers from one department to another."

Requirements:
- Update the employee's department
- Decrease the old department's headcount
- Increase the new department's headcount
- Log the transfer in a transfer_history table
- Roll back if the new department is at capacity

Hint: which `CHECK` constraint could the database enforce for you?

---

# Exam Preparation Tips

1. **Understand concepts** — don't just memorize SQL syntax
2. **Practice writing queries** by hand — the exam is closed book, with no DuckDB
3. **Know when to use** each JOIN type
4. **Be able to normalize** a table from scratch
5. **Explain ACID** with real examples
6. **Read EXPLAIN output** — know what a full (sequential) scan and an index scan mean
7. **Draw ER diagrams** with correct notation

---

# Key SQL Patterns to Remember

```sql
-- Top-N per group
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY g ORDER BY v DESC) AS rn
    FROM t
) AS ranked
WHERE rn <= N;

-- Running total
SUM(amount) OVER (ORDER BY date)

-- Percentage of total
value / SUM(value) OVER () * 100

-- Find non-matches
SELECT * FROM a LEFT JOIN b ON ... WHERE b.id IS NULL;

-- CTE for readability
WITH step1 AS (...), step2 AS (...) SELECT ... FROM step2;

-- Replace NULL with a default
COALESCE(SUM(amount), 0)
```

---

# Thank You!

This has been a great quarter. You now have solid foundations in:
- Relational database design
- SQL querying (basic through advanced)
- Normalization theory
- Performance optimization
- Transaction management
- Modern data: JSON, lists, PIVOT

These skills are valuable in **any** career involving data.

---

# Final Reminders

- Capstone project presentations: today's session
- Final exam: in class, closed book, LockDown Browser required —
  date and time in the [SCU Final Exam Schedule](https://www.scu.edu/media/offices/registrar/2026---2027-Final-Exam-Schedule-1.pdf)
  (see `course_information/ASSIGNMENTS_and_GRADING.md`)
- Course evaluations: please fill them out!
- Keep practicing SQL — it's a lifelong skill

---

# Questions?

Thank you and good luck!

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
