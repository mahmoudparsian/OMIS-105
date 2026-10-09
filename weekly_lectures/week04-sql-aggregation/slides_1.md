---
title: OMIS 105 - Week 4 (Aggregation, GROUP BY, HAVING)
author: Dr. Mahmoud Parsian
marp: true
theme: default
paginate: true
class: lead
style: |
  section {
    justify-content: flex-start;
  }
---

# OMIS 105  
## Week 4: SQL Analytics (Aggregation, GROUP BY, HAVING)

---

# Agenda

- Aggregate functions: COUNT, SUM, AVG, MIN, MAX
- GROUP BY (the core concept)
- HAVING vs WHERE
- Business analytics queries
- Common mistakes
- Hands-on practice

---

# Recap

- SELECT → which columns to show  
- WHERE → which rows to keep  
- ORDER BY → how to sort  
- LIMIT → how many rows  

👉 Today: Turn data into **insight**

---

# What is Aggregation?

**Aggregation** combines many rows into one summary value.

| Function | Returns |
| :--- | :--- |
| `COUNT` | how many rows (or values) |
| `SUM` | the total |
| `AVG` | the average |
| `MIN` / `MAX` | the smallest / largest value |

---

# Example Table: sales

| id | product | price | quantity |
|----|--------|------|----------|
| 1  | Laptop | 1000 | 1        |
| 2  | Phone  | 800  | 2        |
| 3  | Tablet | 500  | 3        |
| 4  | Laptop | 1200 | 1        |
| 5  | Phone  | 900  | 1        |

To follow along in DuckDB:

```sql
CREATE OR REPLACE TABLE sales AS
SELECT * FROM (VALUES
    (1, 'Laptop', 1000, 1),
    (2, 'Phone',   800, 2),
    (3, 'Tablet',  500, 3),
    (4, 'Laptop', 1200, 1),
    (5, 'Phone',   900, 1)
) AS t(id, product, price, quantity);
```

---

# COUNT

```sql
SELECT COUNT(*) FROM sales;                  -- 5
```

👉 `COUNT(*)` counts all rows

```sql
SELECT COUNT(DISTINCT product) FROM sales;   -- 3
```

👉 `COUNT(DISTINCT col)` counts the different values

`COUNT(col)` counts only the rows where `col` is **not** `NULL`.

---

# SUM

```sql
SELECT SUM(price * quantity) AS total_revenue
FROM sales;                                  -- 6200
```

👉 Total revenue: SQL multiplies each row first, then adds the results

---

# AVG, MIN, MAX

```sql
SELECT AVG(price) AS avg_price,              -- 880.0
       MIN(price) AS lowest_price,           -- 500
       MAX(price) AS highest_price           -- 1200
FROM sales;
```

👉 Several aggregates can go in one `SELECT`

Tip: use `ROUND(AVG(price), 2)` to show two decimal places.

---

# GROUP BY (Core Idea)

**Group** rows that share a value, then **aggregate** each group.

```sql
SELECT product, SUM(price * quantity) AS revenue
FROM sales
GROUP BY product;
```

👉 One result row **per product**

---

# GROUP BY Output

| product | revenue |
|--------|---------|
| Laptop | 2200    |
| Phone  | 2500    |
| Tablet | 1500    |

Laptop = 1000×1 + 1200×1 = 2200  
Phone = 800×2 + 900×1 = 2500  
Tablet = 500×3 = 1500

(The order of groups is not guaranteed. Add `ORDER BY` if order matters.)

---

# Why GROUP BY?

To answer:

👉 “How does **each** group perform?”

Examples:
- Revenue per product
- Orders per customer
- Average price per category

---

# Important Rule

Every column in `SELECT` must be:
- listed in `GROUP BY`,  
OR  
- inside an aggregate function

```sql
-- WRONG: id is neither grouped nor aggregated
SELECT product, id, SUM(quantity) FROM sales GROUP BY product;
-- Binder Error: column "id" must appear in the GROUP BY clause
-- or must be part of an aggregate function.
```

Why? Each product has several `id` values. SQL cannot show them all in one row.

---

# HAVING (Filtering Groups)

```sql
SELECT product, SUM(price * quantity) AS revenue
FROM sales
GROUP BY product
HAVING SUM(price * quantity) > 2000;
```

| product | revenue |
|--------|---------|
| Laptop | 2200    |
| Phone  | 2500    |

👉 `HAVING` keeps only the **groups** that match

(DuckDB also accepts `HAVING revenue > 2000`, using the alias.
Many other databases do not, so repeating the expression is safer.)

---

# WHERE vs HAVING (Critical)

| WHERE | HAVING |
|------|--------|
| Filters **rows** | Filters **groups** |
| Runs **before** grouping | Runs **after** grouping |
| Cannot use aggregates | Usually uses aggregates |

---

# Example Comparison

```sql
-- WHERE (row-level): rows with price > 700
SELECT * FROM sales
WHERE price > 700;                -- ids 1, 2, 4, 5

-- HAVING (group-level): products whose prices add up to more than 1500
SELECT product, SUM(price)
FROM sales
GROUP BY product
HAVING SUM(price) > 1500;         -- Laptop 2200, Phone 1700
```

---

# WHERE and HAVING Together

```sql
SELECT product, SUM(price * quantity) AS revenue
FROM sales
WHERE price >= 900                -- 1. keep only rows with price >= 900
GROUP BY product                  -- 2. group the remaining rows
HAVING SUM(price * quantity) > 1000;  -- 3. keep only big groups
```

Result: Laptop 2200 (Phone has only one row left, revenue 900)

---

# ORDER BY with GROUP BY

```sql
SELECT product, SUM(price * quantity) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC;
```

👉 `ORDER BY` runs last, so it **can** use the alias `revenue`

---

# Top Performer

```sql
SELECT product, SUM(price * quantity) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 1;                          -- Phone, 2500
```

👉 The product with the highest revenue

---

# Business Questions

- Which product generates the most revenue? → `ORDER BY revenue DESC LIMIT 1`
- Which product performs worst? → `ORDER BY revenue ASC LIMIT 1`
- How many units were sold per product? → `SUM(quantity) ... GROUP BY product`

---

# In-Class Exercise

Write a query for each question:

👉 “Find the revenue for each product.”

👉 “Find the products with revenue greater than 2000.”

👉 “Find the number of units sold for each product.”

---

# Common Mistakes

- Using `WHERE` with an aggregate: `WHERE SUM(price) > 1500` ❌ (use `HAVING`)
- Forgetting `GROUP BY` when mixing columns and aggregates ❌
- Selecting a column that is neither grouped nor aggregated ❌
- Expecting `AVG` to count `NULL` values (it skips them) ❌

---

# Mental Model

GROUP BY → organize rows into groups  
Aggregation → summarize each group  
HAVING → filter the summaries  

Order of thinking:
`FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`

---

# Hands-On Lab

- COUNT rows
- SUM revenue
- GROUP BY product
- HAVING conditions
- ORDER BY + LIMIT

---

# Summary

- Aggregate functions turn many rows into one value
- GROUP BY gives one result row per group
- WHERE filters rows; HAVING filters groups

👉 This is **real analytics**

---

# What’s Next?

Next lecture (`slides_2`):
- JOINs: combining tables
- INNER JOIN and LEFT JOIN
- JOINs + GROUP BY for business reports

---

# Final Thought

Raw data becomes useful when you summarize it.

👉 Good questions + aggregation = insight

---

# Let’s Analyze Data 🚀

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
