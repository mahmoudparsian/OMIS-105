---
title: LIMIT N vs RANK() in SQL
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
    font-size: 22px;
  }
  code {
    font-size: 23px;
  }
---

# LIMIT N vs RANK() in SQL

## A clear DuckDB example

---

# Learning Goal

By the end of this lesson, you should clearly understand:

- `LIMIT N` returns only **N rows from the final result**
- `LIMIT N` applies to the **whole result set**
- `RANK()` assigns rankings to rows
- `RANK()` can rank within groups using `PARTITION BY`
- `RANK()` is much more powerful for **Top-N per group**

---

# Simple Rule

## Use `LIMIT N`

When you want only the first N rows from the final result.

## Use `RANK()`

When you want to rank rows, especially within categories or groups.

---

# Example Table: `sales`

We will use this 10-row table.

| sale_id | country | product | category | revenue |
|---:|---|---|---|---:|
| 1 | USA | Laptop | Electronics | 5000 |
| 2 | USA | Phone | Electronics | 4200 |
| 3 | USA | Mouse | Accessories | 800 |
| 4 | Canada | Laptop | Electronics | 3000 |
| 5 | Canada | Phone | Electronics | 2800 |
| 6 | Canada | Keyboard | Accessories | 900 |
| 7 | UK | Laptop | Electronics | 3500 |
| 8 | UK | Tablet | Electronics | 2500 |
| 9 | UK | Mouse | Accessories | 700 |
| 10 | Germany | Phone | Electronics | 3200 |

---

# Create the Table in DuckDB

```sql
CREATE TABLE sales (
    sale_id INTEGER,
    country VARCHAR,
    product VARCHAR,
    category VARCHAR,
    revenue INTEGER
);
```

---

# Insert the Data

```sql
INSERT INTO sales VALUES
(1,  'USA',     'Laptop',   'Electronics', 5000),
(2,  'USA',     'Phone',    'Electronics', 4200),
(3,  'USA',     'Mouse',    'Accessories', 800),
(4,  'Canada',  'Laptop',   'Electronics', 3000),
(5,  'Canada',  'Phone',    'Electronics', 2800),
(6,  'Canada',  'Keyboard', 'Accessories', 900),
(7,  'UK',      'Laptop',   'Electronics', 3500),
(8,  'UK',      'Tablet',   'Electronics', 2500),
(9,  'UK',      'Mouse',    'Accessories', 700),
(10, 'Germany', 'Phone',    'Electronics', 3200);
```

---

# First Question

> What are the top 3 sales rows overall?

This is a whole-table question.

Use:

```sql
ORDER BY revenue DESC
LIMIT 3
```

---

# LIMIT N Example

```sql
SELECT
    sale_id,
    country,
    product,
    revenue
FROM sales
ORDER BY revenue DESC
LIMIT 3;
```

---

# LIMIT N Output

| sale_id | country | product | revenue |
|---:|---|---|---:|
| 1 | USA | Laptop | 5000 |
| 2 | USA | Phone | 4200 |
| 7 | UK | Laptop | 3500 |

---

# What Did LIMIT Do?

`LIMIT 3` returned only the first 3 rows from the final sorted result.

Important:

👉 It did **not** return top 3 per country  
👉 It returned top 3 overall

---

# LIMIT Applies to the Whole Result Set

This query:

```sql
SELECT *
FROM sales
ORDER BY revenue DESC
LIMIT 3;
```

means:

1. Sort all rows by revenue
2. Keep only 3 rows total

---

# LIMIT Does NOT Understand Groups

Suppose the question is:

> Show the top 2 products in each country.

Can `LIMIT 2` solve this?

No.

`LIMIT 2` gives only 2 rows total.

---

# Wrong Attempt for Top 2 Per Country

```sql
SELECT
    country,
    product,
    revenue
FROM sales
ORDER BY country, revenue DESC
LIMIT 2;
```

---

# Why Is This Wrong?

Because `LIMIT 2` limits the entire final result.

It does not reset for each country.

It gives only two rows total, not two rows per country.

---

# Output of Wrong Attempt

| country | product | revenue |
|---|---|---:|
| Canada | Laptop | 3000 |
| Canada | Phone | 2800 |

This only shows Canada because Canada comes first alphabetically.

---

# Enter RANK()

`RANK()` assigns a ranking number based on an ordering.

Example:

```sql
RANK() OVER (ORDER BY revenue DESC)
```

This ranks all rows by revenue.

---

# RANK Overall

```sql
SELECT
    country,
    product,
    revenue,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM sales;
```

---

# RANK Overall Output

| country | product | revenue | revenue_rank |
|---|---|---:|---:|
| USA | Laptop | 5000 | 1 |
| USA | Phone | 4200 | 2 |
| UK | Laptop | 3500 | 3 |
| Germany | Phone | 3200 | 4 |
| Canada | Laptop | 3000 | 5 |
| Canada | Phone | 2800 | 6 |
| UK | Tablet | 2500 | 7 |
| Canada | Keyboard | 900 | 8 |
| USA | Mouse | 800 | 9 |
| UK | Mouse | 700 | 10 |

---

# RANK vs LIMIT So Far

Both can help with top results.

But they are different:

| Feature | LIMIT N | RANK() |
|---|---|---|
| Returns rows? | Yes | No, creates rank values |
| Applies to whole result? | Yes | Can be whole result or groups |
| Can rank per group? | No | Yes |
| Good for Top-N per group? | No | Yes |

---

# Key Idea: PARTITION BY

`PARTITION BY` means:

👉 Restart the ranking inside each group.

Example:

```sql
RANK() OVER (
    PARTITION BY country
    ORDER BY revenue DESC
)
```

This ranks products separately within each country.

---

# Rank Within Each Country

```sql
SELECT
    country,
    product,
    revenue,
    RANK() OVER (
        PARTITION BY country
        ORDER BY revenue DESC
    ) AS country_rank
FROM sales
ORDER BY country, country_rank;
```

---

# Rank Within Country Output

| country | product | revenue | country_rank |
|---|---|---:|---:|
| Canada | Laptop | 3000 | 1 |
| Canada | Phone | 2800 | 2 |
| Canada | Keyboard | 900 | 3 |
| Germany | Phone | 3200 | 1 |
| UK | Laptop | 3500 | 1 |
| UK | Tablet | 2500 | 2 |
| UK | Mouse | 700 | 3 |
| USA | Laptop | 5000 | 1 |
| USA | Phone | 4200 | 2 |
| USA | Mouse | 800 | 3 |

---

# Now We Can Answer Top 2 Per Country

Question:

> Show the top 2 sales rows within each country.

We need:

1. Rank rows within each country
2. Keep only rank <= 2

---

# Top 2 Per Country with RANK

```sql
WITH ranked_sales AS (
    SELECT
        country,
        product,
        revenue,
        RANK() OVER (
            PARTITION BY country
            ORDER BY revenue DESC
        ) AS country_rank
    FROM sales
)
SELECT *
FROM ranked_sales
WHERE country_rank <= 2
ORDER BY country, country_rank;
```

---

# Top 2 Per Country Output

| country | product | revenue | country_rank |
|---|---|---:|---:|
| Canada | Laptop | 3000 | 1 |
| Canada | Phone | 2800 | 2 |
| Germany | Phone | 3200 | 1 |
| UK | Laptop | 3500 | 1 |
| UK | Tablet | 2500 | 2 |
| USA | Laptop | 5000 | 1 |
| USA | Phone | 4200 | 2 |

---

# Why This Is More Powerful Than LIMIT

`LIMIT 2` gives:

👉 2 rows total

`RANK() ... PARTITION BY country` gives:

👉 up to 2 rows per country

This is the key difference.

---

# LIMIT N Is Global

```sql
ORDER BY revenue DESC
LIMIT 2
```

returns:

| country | product | revenue |
|---|---|---:|
| USA | Laptop | 5000 |
| USA | Phone | 4200 |

Only 2 rows total.

---

# RANK Can Be Local to Groups

```sql
RANK() OVER (
    PARTITION BY country
    ORDER BY revenue DESC
)
```

returns rankings inside:

- Canada
- Germany
- UK
- USA

Each country gets its own ranking.

---

# Important Concept

## LIMIT answers:

> What are the top N rows overall?

## RANK answers:

> What is each row's position?

## RANK + PARTITION BY answers:

> What are the top N rows within each group?

---

# Another Example: Top Product per Country

```sql
WITH ranked_sales AS (
    SELECT
        country,
        product,
        revenue,
        RANK() OVER (
            PARTITION BY country
            ORDER BY revenue DESC
        ) AS country_rank
    FROM sales
)
SELECT *
FROM ranked_sales
WHERE country_rank = 1
ORDER BY country;
```

---

# Top Product per Country Output

| country | product | revenue | country_rank |
|---|---|---:|---:|
| Canada | Laptop | 3000 | 1 |
| Germany | Phone | 3200 | 1 |
| UK | Laptop | 3500 | 1 |
| USA | Laptop | 5000 | 1 |

---

# Can LIMIT Do This?

No.

This query:

```sql
SELECT *
FROM sales
ORDER BY revenue DESC
LIMIT 1;
```

returns only one row overall:

| country | product | revenue |
|---|---|---:|
| USA | Laptop | 5000 |

It does not return one row per country.

---

# RANK Handles Ties

If two rows have the same revenue, `RANK()` gives them the same rank.

Example:

| product | revenue | rank |
|---|---:|---:|
| Laptop | 5000 | 1 |
| Phone | 5000 | 1 |
| Tablet | 3000 | 3 |

Notice rank 2 is skipped.

---

# RANK vs DENSE_RANK vs ROW_NUMBER

| Function | Handles ties? | Skips numbers? |
|---|---|---|
| `RANK()` | Yes | Yes |
| `DENSE_RANK()` | Yes | No |
| `ROW_NUMBER()` | No | No |

---

# Example Concept

If revenues are:

| product | revenue |
|---|---:|
| A | 100 |
| B | 100 |
| C | 90 |

Then:

| product | RANK | DENSE_RANK | ROW_NUMBER |
|---|---:|---:|---:|
| A | 1 | 1 | 1 |
| B | 1 | 1 | 2 |
| C | 3 | 2 | 3 |

---

# Why This Matters

For business questions:

> “Top 2 products per country”

Should ties be included?

- Use `RANK()` if ties matter
- Use `ROW_NUMBER()` if you want exactly 2 rows per country
- Use `DENSE_RANK()` if you want ties but no skipped ranks

---

# LIMIT N Does Not Handle Ties Intelligently

```sql
ORDER BY revenue DESC
LIMIT 2
```

If there is a tie for second place, `LIMIT 2` may exclude one tied row.

So `LIMIT` is simple, but not always fair.

---

# When to Use LIMIT

Use `LIMIT` for:

- Previewing data
- Showing sample rows
- Top N overall
- Reducing output size

Example:

```sql
SELECT *
FROM sales
LIMIT 5;
```

---

# When to Use RANK

Use `RANK()` for:

- Ranking rows
- Top-N per group
- Leaderboards
- Product performance by country
- Customer ranking by spending

---

# LIMIT Example: Preview Data

```sql
SELECT *
FROM sales
LIMIT 5;
```

Good for quickly checking a table.

---

# LIMIT Example: Top 3 Overall

```sql
SELECT
    country,
    product,
    revenue
FROM sales
ORDER BY revenue DESC
LIMIT 3;
```

Good for overall leaderboard.

---

# RANK Example: Leaderboard

```sql
SELECT
    country,
    product,
    revenue,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM sales;
```

Good for showing position.

---

# RANK Example: Top 2 Per Country

```sql
WITH ranked_sales AS (
    SELECT
        country,
        product,
        revenue,
        RANK() OVER (
            PARTITION BY country
            ORDER BY revenue DESC
        ) AS country_rank
    FROM sales
)
SELECT *
FROM ranked_sales
WHERE country_rank <= 2;
```

Good for grouped ranking.

---

# Common Beginner Mistake

Students write:

```sql
SELECT *
FROM sales
ORDER BY country, revenue DESC
LIMIT 2;
```

thinking it means:

> top 2 per country

But it really means:

> first 2 rows after sorting the whole table

---

# Correct Mental Model

## LIMIT

Cuts the final output.

## RANK

Adds ranking information.

## RANK + PARTITION BY

Ranks separately inside each group.

---

# SQL Processing Difference

## LIMIT

Occurs at the end.

```sql
SELECT ...
FROM ...
ORDER BY ...
LIMIT ...
```

## RANK

Computed as a window function before final filtering.

Often used inside a CTE.

---

# Why Use a CTE with RANK?

Because this does not usually work:

```sql
SELECT
    country,
    product,
    revenue,
    RANK() OVER (
        PARTITION BY country
        ORDER BY revenue DESC
    ) AS country_rank
FROM sales
WHERE country_rank <= 2;
```

---

# Why Is That Wrong?

`WHERE` happens before the `SELECT` alias exists.

So `country_rank` is not available to `WHERE` yet.

---

# Correct Pattern

```sql
WITH ranked_sales AS (
    SELECT
        country,
        product,
        revenue,
        RANK() OVER (
            PARTITION BY country
            ORDER BY revenue DESC
        ) AS country_rank
    FROM sales
)
SELECT *
FROM ranked_sales
WHERE country_rank <= 2;
```

---

# Practice Question 1

Write a query:

> Show the top 3 sales rows overall by revenue.

Use `LIMIT`.

---

# Practice Solution 1

```sql
SELECT
    country,
    product,
    revenue
FROM sales
ORDER BY revenue DESC
LIMIT 3;
```

---

# Practice Question 2

Write a query:

> Rank all sales rows from highest revenue to lowest revenue.

Use `RANK()`.

---

# Practice Solution 2

```sql
SELECT
    country,
    product,
    revenue,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM sales;
```

---

# Practice Question 3

Write a query:

> Show the top product in each country.

Use `RANK()` with `PARTITION BY`.

---

# Practice Solution 3

```sql
WITH ranked_sales AS (
    SELECT
        country,
        product,
        revenue,
        RANK() OVER (
            PARTITION BY country
            ORDER BY revenue DESC
        ) AS country_rank
    FROM sales
)
SELECT *
FROM ranked_sales
WHERE country_rank = 1
ORDER BY country;
```

---

# Practice Question 4

Write a query:

> Show the top 2 products in each country.

Use `RANK()` with `PARTITION BY`.

---

# Practice Solution 4

```sql
WITH ranked_sales AS (
    SELECT
        country,
        product,
        revenue,
        RANK() OVER (
            PARTITION BY country
            ORDER BY revenue DESC
        ) AS country_rank
    FROM sales
)
SELECT *
FROM ranked_sales
WHERE country_rank <= 2
ORDER BY country, country_rank;
```

---

# Final Comparison

| Need | Best Tool |
|---|---|
| Preview first 5 rows | `LIMIT 5` |
| Top 3 rows overall | `ORDER BY ... LIMIT 3` |
| Rank all rows | `RANK()` |
| Top 2 per country | `RANK() OVER (PARTITION BY country ...)` |
| Include ties | `RANK()` or `DENSE_RANK()` |
| Exactly N rows per group | `ROW_NUMBER()` |

---

# Final Summary

## LIMIT N

- Applies to the whole final result
- Returns only N rows total
- Simple and useful
- Not enough for top-N-per-group problems

## RANK()

- Creates ranking values
- Can rank overall
- Can rank inside groups
- Solves top-N-per-group problems

---

# Final Mental Model

## LIMIT = cut the final list

## RANK = assign positions

## PARTITION BY = restart ranking for each group

---

# End
