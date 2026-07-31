---
title: OMIS 105 - Week 4 (Flagship Expanded)
author: Instructor
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

- Aggregation functions
- GROUP BY (core concept)
- HAVING vs WHERE
- Business analytics queries
- Common mistakes
- Hands-on practice

---

# Recap

- SELECT → what to show  
- WHERE → which rows  
- ORDER BY → sorting  

👉 Today: Turn data into **insight**

---

# What is Aggregation?

Combining multiple rows into a single result

Examples:
- COUNT → number of rows
- SUM → total
- AVG → average
- MIN / MAX

---

# Example Table: sales

| id | product | price | quantity |
|----|--------|------|----------|
| 1  | Laptop | 1000 | 1        |
| 2  | Phone  | 800  | 2        |
| 3  | Tablet | 500  | 3        |
| 4  | Laptop | 1200 | 1        |
| 5  | Phone  | 900  | 1        |

---

# COUNT

```sql
SELECT COUNT(*) FROM sales;
```

👉 Total number of rows

---

# SUM

```sql
SELECT SUM(price * quantity) AS total_revenue
FROM sales;
```

👉 Total revenue

---

# AVG

```sql
SELECT AVG(price) FROM sales;
```

👉 Average price

---

# GROUP BY (Core Idea)

Group rows by a column

```sql
SELECT product, SUM(price * quantity)
FROM sales
GROUP BY product;
```

---

# Why GROUP BY?

To answer:

👉 “How does each group perform?”

Examples:
- Revenue per product
- Orders per customer

---

# GROUP BY Output

| product | revenue |
|--------|---------|
| Laptop | 2200    |
| Phone  | 2500    |
| Tablet | 1500    |

---

# Important Rule

Every column in SELECT must be:
- in GROUP BY  
OR  
- aggregated  

---

# HAVING (Filtering Groups)

```sql
SELECT product, SUM(price * quantity) AS revenue
FROM sales
GROUP BY product
HAVING revenue > 2000;
```

👉 Filters aggregated results

---

# WHERE vs HAVING (Critical)

| WHERE | HAVING |
|------|--------|
| Filters rows | Filters groups |
| Before grouping | After grouping |

---

# Example Comparison

```sql
-- WHERE (row-level)
SELECT * FROM sales
WHERE price > 700;

-- HAVING (group-level)
SELECT product, SUM(price)
FROM sales
GROUP BY product
HAVING SUM(price) > 1500;
```

---

# ORDER BY with GROUP BY

```sql
SELECT product, SUM(price * quantity) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC;
```

---

# Top Performer

```sql
SELECT product, SUM(price * quantity) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 1;
```

👉 Most valuable product

---

# Business Questions

- Which product generates most revenue?
- Which product performs poorly?
- How many items sold per product?

---

# In-Class Exercise

Ask students:

👉 “Find revenue per product”

👉 “Find products with revenue > 2000”

---

# Common Mistakes

- Using WHERE instead of HAVING ❌  
- Missing GROUP BY ❌  
- Mixing aggregated and non-aggregated columns ❌  

---

# Mental Model

GROUP BY → organize data  
Aggregation → summarize data  
HAVING → filter insights  

---

# Hands-On Lab

- COUNT rows
- SUM revenue
- GROUP BY product
- HAVING conditions
- ORDER BY + LIMIT

---

# Summary

- Aggregation creates insight
- GROUP BY organizes data
- HAVING filters results

👉 This is **real analytics**

---

# What’s Next?

Week 5:
- JOIN deep dive
- multi-table analytics

---

# Final Thought

Raw data is useless without aggregation.

👉 Insight = power

---

# Let’s Analyze Data 🚀
