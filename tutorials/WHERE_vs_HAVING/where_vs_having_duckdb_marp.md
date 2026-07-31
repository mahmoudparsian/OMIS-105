---
title: WHERE vs HAVING in SQL
author: OMIS 105 - Database Management Systems
marp: true
theme: default
paginate: true
class: lead
style: |
  section {
    justify-content: flex-start;
  }
  table {
    font-size: 24px;
  }
  code {
    font-size: 24px;
  }
---

# WHERE vs HAVING in SQL

## A clear DuckDB example

---

# Learning Goal

By the end of this lesson, you should clearly understand:

- `WHERE` filters **rows**
- `HAVING` filters **groups**
- `WHERE` happens **before** `GROUP BY`
- `HAVING` happens **after** `GROUP BY`

---

# Simple Rule

## Use `WHERE`
When you want to filter individual rows.

## Use `HAVING`
When you want to filter grouped or aggregated results.

---

# Example Table: `sales`

We will use this 10-row table.

| order_id | country | product | quantity | price |
|---:|---|---|---:|---:|
| 1 | USA | Laptop | 1 | 1000 |
| 2 | USA | Phone | 2 | 800 |
| 3 | USA | Tablet | 1 | 500 |
| 4 | Canada | Laptop | 1 | 1000 |
| 5 | Canada | Phone | 1 | 800 |
| 6 | Canada | Mouse | 3 | 50 |
| 7 | UK | Laptop | 2 | 1000 |
| 8 | UK | Mouse | 5 | 50 |
| 9 | Germany | Phone | 1 | 800 |
| 10 | Germany | Tablet | 2 | 500 |

---

# Create the Table in DuckDB

```sql
CREATE TABLE sales (
    order_id INTEGER,
    country VARCHAR,
    product VARCHAR,
    quantity INTEGER,
    price INTEGER
);
```

---

# Insert the Data

```sql
INSERT INTO sales VALUES
(1, 'USA',     'Laptop', 1, 1000),
(2, 'USA',     'Phone',  2, 800),
(3, 'USA',     'Tablet', 1, 500),
(4, 'Canada',  'Laptop', 1, 1000),
(5, 'Canada',  'Phone',  1, 800),
(6, 'Canada',  'Mouse',  3, 50),
(7, 'UK',      'Laptop', 2, 1000),
(8, 'UK',      'Mouse',  5, 50),
(9, 'Germany', 'Phone',  1, 800),
(10,'Germany', 'Tablet', 2, 500);
```

---

# First: Add Revenue

Revenue for each row:

```sql
quantity * price
```

Example:

| product | quantity | price | revenue |
|---|---:|---:|---:|
| Laptop | 1 | 1000 | 1000 |
| Phone | 2 | 800 | 1600 |

---

# Query: Show Row-Level Revenue

```sql
SELECT
    order_id,
    country,
    product,
    quantity,
    price,
    quantity * price AS revenue
FROM sales;
```

---

# Output

| order_id | country | product | quantity | price | revenue |
|---:|---|---|---:|---:|---:|
| 1 | USA | Laptop | 1 | 1000 | 1000 |
| 2 | USA | Phone | 2 | 800 | 1600 |
| 3 | USA | Tablet | 1 | 500 | 500 |
| 4 | Canada | Laptop | 1 | 1000 | 1000 |
| 5 | Canada | Phone | 1 | 800 | 800 |
| 6 | Canada | Mouse | 3 | 50 | 150 |
| 7 | UK | Laptop | 2 | 1000 | 2000 |
| 8 | UK | Mouse | 5 | 50 | 250 |
| 9 | Germany | Phone | 1 | 800 | 800 |
| 10 | Germany | Tablet | 2 | 500 | 1000 |

---

# WHERE Filters Rows

Question:

> Show only orders from the USA.

This is a row-level question.

Use `WHERE`.

---

# WHERE Example

```sql
SELECT *
FROM sales
WHERE country = 'USA';
```

---

# WHERE Output

| order_id | country | product | quantity | price |
|---:|---|---|---:|---:|
| 1 | USA | Laptop | 1 | 1000 |
| 2 | USA | Phone | 2 | 800 |
| 3 | USA | Tablet | 1 | 500 |

---

# Another WHERE Example

Question:

> Show only rows where price is greater than 700.

```sql
SELECT *
FROM sales
WHERE price > 700;
```

---

# WHERE Happens Before Grouping

Important:

```sql
WHERE price > 700
```

means:

> First remove all rows where price is not greater than 700.

Then SQL continues.

---

# GROUP BY Creates Groups

Question:

> What is total revenue by country?

```sql
SELECT
    country,
    SUM(quantity * price) AS total_revenue
FROM sales
GROUP BY country;
```

---

# GROUP BY Output

| country | total_revenue |
|---|---:|
| USA | 3100 |
| Canada | 1950 |
| UK | 2250 |
| Germany | 1800 |

---

# HAVING Filters Groups

Question:

> Show only countries where total revenue is greater than 2000.

This is a group-level question.

Use `HAVING`.

---

# HAVING Example

```sql
SELECT
    country,
    SUM(quantity * price) AS total_revenue
FROM sales
GROUP BY country
HAVING SUM(quantity * price) > 2000;
```

---

# HAVING Output

| country | total_revenue |
|---|---:|
| USA | 3100 |
| UK | 2250 |

---

# Why Not WHERE?

This is wrong:

```sql
SELECT
    country,
    SUM(quantity * price) AS total_revenue
FROM sales
WHERE SUM(quantity * price) > 2000
GROUP BY country;
```

---

# Why Is That Wrong?

Because `WHERE` filters rows.

But:

```sql
SUM(quantity * price)
```

does not exist yet at the row-filtering stage.

Aggregation happens later.

---

# Correct Version

```sql
SELECT
    country,
    SUM(quantity * price) AS total_revenue
FROM sales
GROUP BY country
HAVING SUM(quantity * price) > 2000;
```

---

# WHERE vs HAVING Side by Side

| Clause | Filters | Used With Aggregates? | Happens |
|---|---|---|---|
| `WHERE` | individual rows | No | before `GROUP BY` |
| `HAVING` | grouped results | Yes | after `GROUP BY` |

---

# Key Execution Order

SQL is written like this:

```sql
SELECT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
```

But logically processed like this:

1. `FROM`
2. `WHERE`
3. `GROUP BY`
4. `HAVING`
5. `SELECT`
6. `ORDER BY`

---

# Example with WHERE and HAVING Together

Question:

> For only USA and UK rows, find countries with total revenue greater than 2000.

This needs both:

- `WHERE` filters rows first
- `HAVING` filters grouped results later

---

# WHERE + HAVING Query

```sql
SELECT
    country,
    SUM(quantity * price) AS total_revenue
FROM sales
WHERE country IN ('USA', 'UK')
GROUP BY country
HAVING SUM(quantity * price) > 2000;
```

---

# Step-by-Step Explanation

## Step 1: WHERE

Keep only rows where:

```sql
country IN ('USA', 'UK')
```

## Step 2: GROUP BY

Group remaining rows by country.

## Step 3: HAVING

Keep only groups where total revenue > 2000.

---

# Result

| country | total_revenue |
|---|---:|
| USA | 3100 |
| UK | 2250 |

---

# Product-Level Example

Question:

> Which products generated more than 2000 in total revenue?

Use `GROUP BY product` and `HAVING`.

---

# Product Revenue Query

```sql
SELECT
    product,
    SUM(quantity * price) AS total_revenue
FROM sales
GROUP BY product
HAVING SUM(quantity * price) > 2000
ORDER BY total_revenue DESC;
```

---

# Product Revenue Output

| product | total_revenue |
|---|---:|
| Laptop | 4000 |
| Phone | 3200 |

---

# Row-Level vs Group-Level Question

## Row-level question

> Which rows have price > 700?

Use `WHERE`.

## Group-level question

> Which products have total revenue > 2000?

Use `HAVING`.

---

# Common Beginner Mistake

Students often write:

```sql
WHERE total_revenue > 2000
```

But `total_revenue` is an aggregate result.

So use:

```sql
HAVING SUM(quantity * price) > 2000
```

---

# Another Common Mistake

This may not work reliably:

```sql
HAVING total_revenue > 2000
```

Better for beginners:

```sql
HAVING SUM(quantity * price) > 2000
```

Why?

Because the alias `total_revenue` is created in the `SELECT` step.

---

# Teaching Shortcut

Ask yourself:

## Am I filtering raw rows?

Use `WHERE`.

## Am I filtering summarized results?

Use `HAVING`.

---

# Practice Question 1

Write a query:

> Show all sales rows for products with price greater than 500.

Use `WHERE`.

---

# Practice Solution 1

```sql
SELECT *
FROM sales
WHERE price > 500;
```

---

# Practice Question 2

Write a query:

> Show countries with more than 2 total order rows.

Use `GROUP BY` and `HAVING`.

---

# Practice Solution 2

```sql
SELECT
    country,
    COUNT(*) AS number_of_orders
FROM sales
GROUP BY country
HAVING COUNT(*) > 2;
```

---

# Practice Question 3

Write a query:

> For only Laptop and Phone rows, show products with total revenue greater than 3000.

Use both `WHERE` and `HAVING`.

---

# Practice Solution 3

```sql
SELECT
    product,
    SUM(quantity * price) AS total_revenue
FROM sales
WHERE product IN ('Laptop', 'Phone')
GROUP BY product
HAVING SUM(quantity * price) > 3000;
```

---

# Final Summary

## `WHERE`

Filters rows before grouping.

Example:

```sql
WHERE price > 700
```

## `HAVING`

Filters groups after aggregation.

Example:

```sql
HAVING SUM(quantity * price) > 2000
```

---

# Final Mental Model

## WHERE = before the summary

## HAVING = after the summary

If you remember this, you will almost always choose correctly.

---

# End
