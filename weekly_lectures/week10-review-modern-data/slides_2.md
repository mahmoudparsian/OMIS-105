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

**Session 1**: Capstone Presentations + Modern Database Trends
**Session 2**: Comprehensive Review + Exam Preparation

---

# Session 1: Beyond Relational — Modern Trends

---

# The Database Landscape in 2025

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
| Column-Family | Cassandra, HBase | Time-series, IoT, large scale |
| Graph | Neo4j, Amazon Neptune | Social networks, recommendations |

---

# When Relational vs. NoSQL?

| Choose Relational When | Choose NoSQL When |
|----------------------|------------------|
| Data has clear structure | Schema changes frequently |
| Complex queries needed | Simple key-based lookups |
| ACID is critical | Eventual consistency is OK |
| Joins are common | Data is denormalized |
| Moderate scale | Massive horizontal scale |

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

---

# Data Lakes and Lakehouses

**Data Lake**: Store raw data in any format (Parquet, CSV, JSON)
**Lakehouse**: Data lake + database-like query capabilities

```sql
-- DuckDB can query Parquet files directly!
SELECT * FROM read_parquet('sales_2024.parquet')
WHERE region = 'West'
GROUP BY product_category;
```

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
-- Create roles with specific permissions
CREATE ROLE analyst;
GRANT SELECT ON ALL TABLES TO analyst;

-- Create users and assign roles
CREATE USER intern WITH PASSWORD 'secure_pass';
GRANT analyst TO intern;

-- Revoke access
REVOKE INSERT, UPDATE, DELETE ON orders FROM intern;
```

Not all features available in DuckDB, but critical in production systems.

---

# Backup and Recovery

| Strategy | Description | Recovery Time |
|----------|------------|---------------|
| Full backup | Copy entire database | Slow restore |
| Incremental | Only changes since last backup | Faster restore |
| Point-in-time | Restore to any moment | Using WAL logs |
| Replication | Real-time copy to standby | Near-instant failover |

---

# ETL: Extract, Transform, Load

Moving data between systems:

```
Source Systems → Extract → Transform → Load → Data Warehouse
 (OLTP DBs,      (Read      (Clean,       (Insert
  APIs, files)    data)      reshape)       into DW)
```

DuckDB excels at the Transform step:
```sql
-- Transform CSV data and export
COPY (
    SELECT category, COUNT(*), SUM(revenue)
    FROM read_csv_auto('raw_sales.csv')
    GROUP BY category
) TO 'summary.parquet' (FORMAT PARQUET);
```

---

# Session 2: Comprehensive Review

---

# Course Map

```
Week 1: Foundations ──────────────────────────────┐
Week 2: Relational Model ────────────────────────┤
Week 3: SQL Basics (Functions, GROUP BY) ────────┤
Week 4: SQL JOINs (Multi-table queries) ─────────┤
Week 5: SQL Advanced (Windows, CTEs, Views) ──────┤
Week 6: Normalization (1NF → BCNF) ──────────────┤ → Week 9: Project
Week 7: Performance (Indexes, EXPLAIN) ───────────┤
Week 8: Transactions (ACID) ──────────────────────┘
```

---

# Review: Database Fundamentals (Week 1)

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

# Review: SQL — JOINs (Week 4)

| JOIN | Returns |
|------|---------|
| INNER JOIN | Only matching rows |
| LEFT JOIN | All from left + matches from right |
| RIGHT JOIN | All from right + matches from left |
| FULL OUTER JOIN | All rows from both |
| CROSS JOIN | Cartesian product |
| Self JOIN | Table joined with itself |

```sql
SELECT c.name, o.order_id
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

---

# Review: SQL — Advanced (Week 5)

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
| BCNF | Every determinant is a superkey | Remaining anomalies |

**Functional dependency**: X → Y ("knowing X determines Y")

---

# Review: Performance (Week 7)

- **Indexes**: B-Tree structures that speed up reads
- **EXPLAIN**: shows the query execution plan
- **Optimization tips**:
  - Filter early, select only needed columns
  - Avoid functions on indexed columns in WHERE
  - Use EXISTS over IN for large subqueries
  - Use INNER JOIN when LEFT JOIN isn't needed
- **DuckDB**: columnar storage, vectorized execution

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

**Concurrency problems**: dirty read, non-repeatable read, phantom read, lost update

---

# Practice Problem 1: Schema Design

Design a schema for a **pet adoption shelter**:
- Animals (id, name, species, breed, age, status)
- Adopters (id, name, email, phone, address)
- Adoptions (which animal, which adopter, when, fee)
- Veterinary records (animal, vet, date, procedure, cost)

Questions:
1. What are the relationships?
2. Where do the FKs go?
3. Is this in 3NF?

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
    SELECT cat.category_name,
           COUNT(DISTINCT p.product_id) AS num_products,
           SUM(oi.quantity * oi.unit_price) AS revenue
    FROM categories cat
    JOIN products p ON cat.category_id = p.category_id
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY cat.category_name
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
    ON cr.category_name = (SELECT category_name FROM categories WHERE category_id = bs.category_id)
    AND bs.rn = 1
ORDER BY cr.revenue DESC;
```

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

---

# Exam Preparation Tips

1. **Understand concepts** — don't just memorize SQL syntax
2. **Practice writing queries** by hand (no DuckDB help)
3. **Know when to use** each JOIN type
4. **Be able to normalize** a table from scratch
5. **Explain ACID** with real examples
6. **Read EXPLAIN output** — know what full scan vs. index scan means
7. **Draw ER diagrams** with correct notation

---

# Key SQL Patterns to Remember

```sql
-- Top-N per group
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY g ORDER BY v DESC) AS rn
    FROM t
) WHERE rn <= N;

-- Running total
SUM(amount) OVER (ORDER BY date)

-- Percentage of total
value / SUM(value) OVER () * 100

-- Find non-matches
SELECT * FROM a LEFT JOIN b ON ... WHERE b.id IS NULL;

-- CTE for readability
WITH step1 AS (...), step2 AS (...) SELECT ... FROM step2;
```

---

# Thank You!

This has been a great quarter. You now have solid foundations in:
- Relational database design
- SQL querying (basic through advanced)
- Normalization theory
- Performance optimization
- Transaction management

These skills are valuable in **any** career involving data.

---

# Final Reminders

- Capstone project presentations: today's session
- Final exam: [date/time per syllabus]
- Course evaluations: please fill them out!
- Keep practicing SQL — it's a lifelong skill

---

# Questions?

Thank you and good luck!

