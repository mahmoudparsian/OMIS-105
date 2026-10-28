---
title: OMIS 105 - Week 7 (Subqueries — A Query Inside a Query)
author: Dr. Mahmoud Parsian
marp: true
theme: default
paginate: true
class: lead
style: |
  section {
    justify-content: flex-start;
  }
  table {
    font-size: 0.7em;
  }

---

# OMIS 105: Week 7
## Subqueries — Session 1 <br> A Query Inside a Query

---

# Agenda

- Why we need subqueries
- Our data: a tiny online store (3 tables)
- **Scalar subqueries** — return one value
- Subqueries in `SELECT`
- **List subqueries** — `IN` and `NOT IN`
- Reading nested subqueries "inside-out"
- ⚠️ The `NOT IN` + `NULL` trap
- Hands-on practice

---

# What You Already Know

- `SELECT`, `WHERE`, `ORDER BY` (Weeks 1–3)
- `GROUP BY`, `HAVING`, `AVG`, `MAX` (Week 4)
- `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN` (Weeks 5–6)

👉 Today: put **one query inside another**, so a question that
needs **two steps** can be answered in **one** query.

---

# Our Data: A Tiny Online Store 🛒

Only **3 tables**:

```
customers ──< orders >── products
```

| Table | Rows | Columns |
|---|---|---|
| `customers` | 8 | `customer_id`, `customer_name`, `city` |
| `products` | 8 | `product_id`, `product_name`, `category`, `price` |
| `orders` | 14 | `order_id`, `customer_id`, `product_id`, `quantity`, `order_date` |

---

# `customers` (8 rows)

| customer_id | customer_name | city |
|---|---|---|
| 1 | Alice Wong | Santa Clara |
| 2 | Bob Smith | San Jose |
| 3 | Carmen Diaz | Sunnyvale |
| 4 | David Kim | Santa Clara |
| 5 | Elena Rossi | San Jose |
| 6 | Farah Ali | Cupertino |
| **7** | **George Brown** | Sunnyvale |
| **8** | **Hana Sato** | Cupertino |

George and Hana have **never ordered**.

---

# `products` (8 rows)

| product_id | product_name | category | price |
|---|---|---|---|
| 101 | Laptop | Electronics | 1200 |
| 102 | Headphones | Electronics | 150 |
| 103 | Phone Case | Electronics | 25 |
| 104 | Desk Chair | Furniture | 300 |
| 105 | Bookshelf | Furniture | 180 |
| 106 | Coffee Mug | Kitchen | 12 |
| **107** | **Blender** | Kitchen | 90 |
| **108** | **Standing Desk** | Furniture | 650 |

Blender and Standing Desk were **never ordered**.

---

# `orders` (14 rows)

| order_id | customer_id | product_id | quantity | | order_id | customer_id | product_id | quantity |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 101 | 1 | | 8 | 4 | 102 | 2 |
| 2 | 1 | 103 | 2 | | 9 | 5 | 105 | 1 |
| 3 | 2 | 102 | 1 | | 10 | 5 | 103 | 3 |
| 4 | 2 | 106 | 4 | | 11 | 6 | 106 | 1 |
| 5 | 3 | 104 | 1 | | **12** | **NULL** | 102 | 1 |
| 6 | 3 | 106 | 2 | | 13 | 1 | 104 | 1 |
| 7 | 4 | 101 | 1 | | 14 | 6 | 105 | 2 |

(Also: `order_date`.) Order **12** is a **guest order** — no customer.
Remember this `NULL`. It will surprise us later.

---

# A Two-Step Question

**"Which products cost more than the average price?"**

We need **two** steps:

1. Find the average price
2. Find the products above it

Let's do it by hand first.

---

# Step 1: The Average Price

```sql
SELECT AVG(price) AS avg_price
FROM products;
```

| avg_price |
|---|
| 325.875 |

---

# Step 2: Products Above 325.875

```sql
SELECT product_name, price
FROM products
WHERE price > 325.875;
```

| product_name | price |
|---|---|
| Laptop | 1200 |
| Standing Desk | 650 |

😟 It works, but we **typed the number by hand**.
If a price changes tomorrow, this query is wrong.

---

# Can We Just Write `AVG(price)` in `WHERE`?

```sql
SELECT product_name, price
FROM products
WHERE price > AVG(price);
```

```
Binder Error: WHERE clause cannot contain aggregates!
```

`WHERE` looks at **one row at a time**. `AVG` needs **all rows**.
They cannot be mixed in one step.

---

# The Answer: A Subquery ✅

Put **step 1 inside step 2**, in parentheses:

```sql
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price)
               FROM products);
```

| product_name | price |
|---|---|
| Laptop | 1200 |
| Standing Desk | 650 |

Same answer — and no number typed by hand.

---

# How It Works

```sql
SELECT product_name, price           -- outer query
FROM products
WHERE price > ( SELECT AVG(price)    -- inner query (the subquery)
                FROM products );
```

1. DuckDB runs the **inner query** first → `325.875`
2. It puts that value where the subquery was
3. It runs the **outer query**: `WHERE price > 325.875`

👉 A **subquery** is a `SELECT` inside parentheses, inside another
SQL statement.

---

# Scalar Subquery = One Value

A subquery that returns **exactly one row and one column** is a
**scalar subquery**. Use it anywhere you could type a number.

**The most expensive product:**

```sql
SELECT product_name, price
FROM products
WHERE price = (SELECT MAX(price)
               FROM products);
```

| product_name | price |
|---|---|
| Laptop | 1200 |

💡 Why not `ORDER BY price DESC LIMIT 1`? If two products tie for the
top price, `LIMIT 1` hides one. The subquery shows **both**.

---

# A Scalar Subquery in `SELECT`

Compare each product to the average:

```sql
SELECT product_name,
       price,
       ROUND((SELECT AVG(price) FROM products), 2)         AS avg_price,
       ROUND(price - (SELECT AVG(price) FROM products), 2) AS difference
FROM products
ORDER BY difference DESC;
```

---

# A Scalar Subquery in `SELECT` — Result

| product_name | price | avg_price | difference |
|---|---|---|---|
| Laptop | 1200 | 325.88 | 874.13 |
| Standing Desk | 650 | 325.88 | 324.13 |
| Desk Chair | 300 | 325.88 | -25.88 |
| Bookshelf | 180 | 325.88 | -145.88 |
| Headphones | 150 | 325.88 | -175.88 |
| Blender | 90 | 325.88 | -235.88 |
| Phone Case | 25 | 325.88 | -300.88 |
| Coffee Mug | 12 | 325.88 | -313.88 |

👉 The same value (325.88) appears on every row. Positive difference =
above average.

---

# A Real Error: Too Many Rows ⚠️

A scalar subquery must return **one** row. This one returns three
(three Furniture prices):

```sql
SELECT product_name
FROM products
WHERE price = (SELECT price
               FROM products
               WHERE category = 'Furniture');
```

```
Invalid Input Error: More than one row returned by a subquery
used as an expression - scalar subqueries can only return a single row.
```

👉 When the subquery returns **a list**, use `IN` (next slide).

---

# Subqueries That Return a List

This subquery returns **one column, many rows** — a list:

```sql
SELECT DISTINCT customer_id
FROM orders
ORDER BY customer_id;
```

| customer_id |
|---|
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
| 6 |
| NULL |

Notice the `NULL` at the end — the guest order.

---

# `IN` — "Is the Value in the List?"

**"Which customers have placed an order?"**

```sql
SELECT customer_id, customer_name
FROM customers
WHERE customer_id IN (SELECT customer_id
                      FROM orders)
ORDER BY customer_id;
```

| customer_id | customer_name |
|---|---|
| 1 | Alice Wong |
| 2 | Bob Smith |
| 3 | Carmen Diaz |
| 4 | David Kim |
| 5 | Elena Rossi |
| 6 | Farah Ali |

---

# Nested Subqueries: Read Them Inside-Out

**"Which customers bought an Electronics product?"**

```sql
SELECT customer_name
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
    WHERE product_id IN (
        SELECT product_id
        FROM products
        WHERE category = 'Electronics'
    )
)
ORDER BY customer_name;
```

---

# Inside-Out, Step by Step

1. **Innermost:** Electronics products → `101, 102, 103`
2. **Middle:** customers who ordered 101, 102, or 103
   → `1, 2, 4, 5, NULL`
3. **Outer:** names of those customers

| customer_name |
|---|
| Alice Wong |
| Bob Smith |
| David Kim |
| Elena Rossi |

👉 Always read a nested query from the **inside out**.

---

# `NOT IN` — "Is the Value Missing from the List?"

**"Which products were never ordered?"**

```sql
SELECT product_id, product_name
FROM products
WHERE product_id NOT IN (SELECT product_id
                         FROM orders)
ORDER BY product_id;
```

| product_id | product_name |
|---|---|
| 107 | Blender |
| 108 | Standing Desk |

✅ Works as expected.

---

# The `NOT IN` Trap ⚠️

Same idea: **"Which customers never ordered?"**

```sql
SELECT customer_id, customer_name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id
                          FROM orders);
```

**Result: 0 rows.** 😱

But George and Hana never ordered! Where are they?

---

# Why `NOT IN` Returned Nothing

The list from `orders` is: `1, 2, 3, 4, 5, 6, NULL`

For George (7), SQL checks:

```
7 <> 1  AND  7 <> 2  AND ... AND  7 <> NULL
 true        true                 unknown
```

- Any comparison with `NULL` is **unknown**, not true
- `true AND unknown` = **unknown**
- `WHERE` keeps only rows that are **true** → George is dropped

👉 **One `NULL` in a `NOT IN` list → zero rows.**

---

# The Fix: Remove the `NULL`s

```sql
SELECT customer_id, customer_name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id
                          FROM orders
                          WHERE customer_id IS NOT NULL)
ORDER BY customer_id;
```

| customer_id | customer_name |
|---|---|
| 7 | George Brown |
| 8 | Hana Sato |

✅ Rule: with `NOT IN`, always add `WHERE column IS NOT NULL`
inside the subquery. (Or use `NOT EXISTS` — Session 2.)

💡 `NOT IN (SELECT product_id ...)` worked earlier because
`orders.product_id` has **no** `NULL`s. Lucky — not safe.

---

# Two Kinds of Subqueries So Far

| Kind | Returns | Use it with | Example |
|---|---|---|---|
| **Scalar** | 1 row, 1 column | `=`, `>`, `<`, or in `SELECT` | `price > (SELECT AVG(price) ...)` |
| **List** | 1 column, many rows | `IN`, `NOT IN` | `customer_id IN (SELECT customer_id ...)` |

Session 2 adds:

- **`EXISTS`** — "is there at least one matching row?"
- **Table subqueries** — a subquery in `FROM`
- **Correlated subqueries** — run once per row

---

# Summary

- A **subquery** is a `SELECT` inside parentheses
- The inner query runs first; its result is used by the outer query
- **Scalar** subquery → one value → `=`, `>`, `<`, `SELECT`
- **List** subquery → `IN` / `NOT IN`
- Read nested subqueries **inside-out**
- ⚠️ `NOT IN` + a `NULL` in the list = zero rows.
  Filter with `IS NOT NULL`.

---

# Next Session

**Subqueries — Going Further**

- `EXISTS` and `NOT EXISTS`
- Subqueries in `FROM` (derived tables)
- Correlated subqueries
- Subquery or JOIN?
- CTEs: give a subquery a name with `WITH`

---

# Questions?

Thank you!

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
