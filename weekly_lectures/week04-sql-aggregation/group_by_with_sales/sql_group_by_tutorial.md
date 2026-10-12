# Learning SQL's `GROUP BY` in DuckDB: <br> A Beginner's Guide

1. Welcome to your first step in mastering data aggregation! 

2. When learning SQL, `GROUP BY` is one of the 
most powerful tools in your toolkit. It allows 
you to take individual rows of data and collapse 
them into summary groups (like finding totals,
averages, or counts per category).

3. In this tutorial, we will use **DuckDB**, an incredible high-performance SQL database that you can easily run locally.

---

## 1. Our Setup: The Schema and 10 Rows of Data

Imagine you run a small local coffee shop. You keep track of every transaction in a table called `sales`. 

Here is the SQL to create your table and insert 10 rows of dummy data. You can copy and paste this directly into your DuckDB terminal or client:

**Step-1: Create the table**:

```sql
CREATE TABLE sales (
    id INTEGER,
    item VARCHAR,
    category VARCHAR,
    price DECIMAL(5,2),
    quantity INTEGER
);
```

**Step-2: Insert exactly 10 rows of data**:

```sql
INSERT INTO sales VALUES 
(1, 'Latte', 'Beverage', 4.50, 2),
(2, 'Croissant', 'Bakery', 3.00, 1),
(3, 'Cappuccino', 'Beverage', 4.00, 3),
(4, 'Muffin', 'Bakery', 2.50, 4),
(5, 'Espresso', 'Beverage', 2.50, 1),
(6, 'Croissant', 'Bakery', 3.00, 2),
(7, 'Latte', 'Beverage', 4.50, 1),
(8, 'Bagel', 'Bakery', 3.50, 3),
(9, 'Tea', 'Beverage', 3.00, 2),
(10, 'Muffin', 'Bakery', 2.50, 1);
```

### What does our data look like?
If you run `SELECT * FROM sales;`, you will see 10 individual transaction rows representing what items were sold, their category, price, and how many were bought.

```sql
duckdb ▸ SELECT * FROM sales;
┌───────┬────────────┬──────────┬──────────────┬──────────┐
│  id   │    item    │ category │    price     │ quantity │
│ int32 │  varchar   │ varchar  │ decimal(5,2) │  int32   │
├───────┼────────────┼──────────┼──────────────┼──────────┤
│     1 │ Latte      │ Beverage │         4.50 │        2 │
│     2 │ Croissant  │ Bakery   │         3.00 │        1 │
│     3 │ Cappuccino │ Beverage │         4.00 │        3 │
│     4 │ Muffin     │ Bakery   │         2.50 │        4 │
│     5 │ Espresso   │ Beverage │         2.50 │        1 │
│     6 │ Croissant  │ Bakery   │         3.00 │        2 │
│     7 │ Latte      │ Beverage │         4.50 │        1 │
│     8 │ Bagel      │ Bakery   │         3.50 │        3 │
│     9 │ Tea        │ Beverage │         3.00 │        2 │
│    10 │ Muffin     │ Bakery   │         2.50 │        1 │
└───────┴────────────┴──────────┴──────────────┴──────────┘
  10 rows                                       5 columns
```


## 2. The Core Concept: Basic `GROUP BY`

**Goal:** You want to know: *How many total items 
did we sell for each category?*

Instead of looking at 10 separate rows, we want 
to group the items by their `category` and sum up 
their `quantity`.

```sql
SELECT 
    category, 
    SUM(quantity) AS total_quantity_sold
FROM 
    sales
GROUP BY 
    category;
```

```
┌──────────┬─────────────────────┐
│ category │ total_quantity_sold │
│ varchar  │       int128        │
├──────────┼─────────────────────┤
│ Beverage │                   9 │
│ Bakery   │                  11 │
└──────────┴─────────────────────┘
```

* What values are added to create `total_quantity_sold`?

```sql
SELECT 
    category, 
    SUM(quantity) AS total_quantity_sold,
    GROUP_CONCAT(quantity) as grouped
FROM 
    sales
GROUP BY 
    category;
```

```
┌──────────┬─────────────────────┬───────────┐
│ category │ total_quantity_sold │  grouped  │
│ varchar  │       int128        │  varchar  │
├──────────┼─────────────────────┼───────────┤
│ Bakery   │                  11 │ 1,4,2,3,1 │  <- 11 = 1+4+2+3+1
│ Beverage │                   9 │ 2,3,1,1,2 │  <-  9 = 2+3+1+1+2
└──────────┴─────────────────────┴───────────┘
```

### How to read this query:
1. `SELECT category`: Choose the column you want to group or aggregate by.
2. `SUM(quantity)`: Apply an aggregate function (`SUM`, `COUNT`, `AVG`, `MAX`, `MIN`) to combine the rows within that group.
3. `FROM sales`: Look at our `sales` table.
4. `GROUP BY category`: Bundle all rows that share the exact same `category` value together before calculating the sum.

---

## 3. Filtering Before Grouping: `GROUP BY` with `WHERE`

**Goal:** You want to know total quantities sold per 
category, **but only for items that cost $3.00 or more**.

When you want to filter rows *before* any grouping or 
aggregation takes place, you use the `WHERE` clause.

```sql
SELECT 
    category, 
    SUM(quantity) AS total_quantity_sold
FROM 
    sales
WHERE 
    price >= 3.00
GROUP BY 
    category;
```

```
┌──────────┬─────────────────────┐
│ category │ total_quantity_sold │
│ varchar  │       int128        │
├──────────┼─────────────────────┤
│ Bakery   │                   6 │
│ Beverage │                   8 │
└──────────┴─────────────────────┘
```

### Key Rule for `WHERE`:
* `WHERE` evaluates rows **before** the grouping 
happens. 
* You cannot use aggregate functions like 
`SUM()` or `COUNT()` inside a `WHERE` clause.

---

## 4. Filtering After Grouping: `GROUP BY` with `HAVING`

**Goal:** You want to see categories, but **only show categories where the total quantity sold is greater than 7**.

What happens if you want to filter based on the *result* of an aggregate calculation (like a sum or a count)? That is where `HAVING` comes in. `HAVING` acts like a `WHERE` clause, but it filters **after** the `GROUP BY` has taken place.

```sql
SELECT 
    category, 
    SUM(quantity) AS total_quantity_sold
FROM 
    sales
GROUP BY 
    category;
```

```
┌──────────┬─────────────────────┐
│ category │ total_quantity_sold │
│ varchar  │       int128        │
├──────────┼─────────────────────┤
│ Bakery   │                  11 │
│ Beverage │                   9 │
└──────────┴─────────────────────┘
```

* use `GROUP_CONCAT(quantity)` & `GROUP_CONCAT(price)`

```sql
SELECT
       category,
       SUM(quantity) AS total_quantity_sold,
       GROUP_CONCAT(quantity) AS grouped_quantity, 
       GROUP_CONCAT(price) AS grouped_price
FROM
       sales
GROUP BY
       category;
┌──────────┬─────────────────────┬──────────────────┬──────────────────────────┐
│ category │ total_quantity_sold │ grouped_quantity │      grouped_price       │
│ varchar  │       int128        │     varchar      │         varchar          │
├──────────┼─────────────────────┼──────────────────┼──────────────────────────┤
│ Bakery   │                  11 │ 1,4,2,3,1        │ 3.00,2.50,3.00,3.50,2.50 │
│ Beverage │                   9 │ 2,3,1,1,2        │ 4.50,4.00,2.50,4.50,3.00 │
└──────────┴─────────────────────┴──────────────────┴──────────────────────────┘
```

* use `HAVING`

```sql
SELECT 
    category, 
    SUM(quantity) AS total_quantity_sold
FROM 
    sales
GROUP BY 
    category
HAVING 
    total_quantity_sold > 9;
```

```
┌──────────┬─────────────────────┐
│ category │ total_quantity_sold │
│ varchar  │       int128        │
├──────────┼─────────────────────┤
│ Bakery   │                  11 │
└──────────┴─────────────────────┘
```

### Key Rule for `HAVING`:
* `HAVING` evaluates the summarized groups **after** the `GROUP BY` step. 
* It allows you to filter using aggregate functions (e.g., `SUM(quantity) > 9`).

---

## Summary Cheat Sheet for DuckDB

| Clause | When does it filter/process? | Can it use aggregate functions (`SUM`, `COUNT`)? |
| :--- | :--- | :--- |
| **`WHERE`** | Before grouping (on individual rows) | ❌ No |
| **`GROUP BY`** | Groups individual rows into summary buckets | N/A |
| **`HAVING`** | After grouping (on aggregated summary rows) | ✅ Yes |
