---
title: OMIS 105 - Week 7 (Subqueries — Going Further)
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
## Subqueries — Session 2 <br> Going Further

---

# Agenda

- Recap: scalar and list subqueries
- `EXISTS` and `NOT EXISTS`
- Subqueries in `FROM` (derived tables)
- **Correlated** subqueries — run once per row
- Subquery or JOIN?
- CTEs: give a subquery a name with `WITH`

Same data: `customers` (8), `products` (8), `orders` (14).
George and Hana never ordered. Order 12 has `customer_id = NULL`.

---

# Recap from Session 1

| Kind | Returns | Use it with |
|---|---|---|
| Scalar | 1 value | `=`, `>`, `<`, `SELECT` |
| List | 1 column, many rows | `IN`, `NOT IN` |

⚠️ `NOT IN` + one `NULL` in the list = **zero rows**

---

# `EXISTS` — "Is There at Least One?"

**"Which customers have placed an order?"**

```sql
SELECT c.customer_id, c.customer_name
FROM customers AS c
WHERE EXISTS (SELECT 1
              FROM orders AS o
              WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id;
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

# How `EXISTS` Works

```sql
WHERE EXISTS (SELECT 1
              FROM orders AS o
              WHERE o.customer_id = c.customer_id)
```

- For **each** customer `c`, the subquery looks for matching orders
- `EXISTS` is **true** if it finds **at least one** row
- It does not care *what* is selected — `SELECT 1` is the custom

👉 The subquery uses `c.customer_id` from the **outer** query.
That makes it a **correlated** subquery (more soon).

---

# `NOT EXISTS` — Safe with `NULL`s ✅

**"Which customers never ordered?"** (the question `NOT IN` got wrong)

```sql
SELECT c.customer_id, c.customer_name
FROM customers AS c
WHERE NOT EXISTS (SELECT 1
                  FROM orders AS o
                  WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id;
```

| customer_id | customer_name |
|---|---|
| 7 | George Brown |
| 8 | Hana Sato |

The guest order (`customer_id = NULL`) matches no customer, so it
does no harm.

👉 For "never / missing" questions, **prefer `NOT EXISTS`**.

---

# Three Ways to Find What Is Missing

"Customers who never ordered" — all give George and Hana:

```sql
-- 1. LEFT JOIN + IS NULL (Week 6)
SELECT c.customer_name FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- 2. NOT IN — only safe with IS NOT NULL inside
WHERE c.customer_id NOT IN (SELECT customer_id FROM orders
                            WHERE customer_id IS NOT NULL);

-- 3. NOT EXISTS — always safe
WHERE NOT EXISTS (SELECT 1 FROM orders o
                  WHERE o.customer_id = c.customer_id);
```

---

# Subqueries in `FROM` (Derived Tables)

A subquery can also return a **whole table**. Put it in `FROM` and
query it like any table.

**Question:** "What is the average amount **a customer** spends?"

Two steps again:

1. Total spent by **each** customer
2. Average of those totals

---

# Step 1: Total per Customer

```sql
SELECT o.customer_id,
       SUM(o.quantity * p.price) AS total_spent
FROM orders AS o
INNER JOIN products AS p
    ON o.product_id = p.product_id
WHERE o.customer_id IS NOT NULL
GROUP BY o.customer_id
ORDER BY o.customer_id;
```

| customer_id | total_spent |
|---|---|
| 1 | 1550 |
| 2 | 198 |
| 3 | 324 |
| 4 | 1500 |
| 5 | 255 |
| 6 | 372 |

---

# Step 2: Query the Result of Step 1

```sql
SELECT COUNT(*)                    AS customers,
       ROUND(AVG(total_spent), 2) AS avg_spent
FROM (
    SELECT o.customer_id,
           SUM(o.quantity * p.price) AS total_spent
    FROM orders AS o
    INNER JOIN products AS p
        ON o.product_id = p.product_id
    WHERE o.customer_id IS NOT NULL
    GROUP BY o.customer_id
) AS t;
```

| customers | avg_spent |
|---|---|
| 6 | 699.83 |

- The inner query builds a **temporary table** (6 rows)
- `AS t` gives it a name — **required** for a subquery in `FROM`
- The outer query averages it

---

# Correlated Subqueries

So far, most subqueries ran **once**. A **correlated** subquery
uses a column from the outer query, so it runs **once per outer row**.

**Question:** "Which products cost more than the average **of their
own category**?"

First, the category averages:

| category | avg_price |
|---|---|
| Electronics | 458.33 |
| Furniture | 376.67 |
| Kitchen | 51 |

---

# Correlated Subquery — Above Category Average

```sql
SELECT p.product_name, p.category, p.price
FROM products AS p
WHERE p.price > (SELECT AVG(p2.price)
                 FROM products AS p2
                 WHERE p2.category = p.category)
ORDER BY p.category;
```

| product_name | category | price |
|---|---|---|
| Laptop | Electronics | 1200 |
| Standing Desk | Furniture | 650 |
| Blender | Kitchen | 90 |

- Laptop is compared with the **Electronics** average (458.33)
- Blender (90) is compared with the **Kitchen** average (51)

👉 Compare: above the **overall** average (325.88) were only Laptop and
Standing Desk.

---

# How a Correlated Subquery Runs

```sql
WHERE p.price > (SELECT AVG(p2.price)
                 FROM products AS p2
                 WHERE p2.category = p.category)   -- ← outer column
```

| Outer row `p` | Subquery computes | Kept? |
|---|---|---|
| Laptop, Electronics, 1200 | AVG of Electronics = 458.33 | ✅ |
| Headphones, Electronics, 150 | AVG of Electronics = 458.33 | ❌ |
| Blender, Kitchen, 90 | AVG of Kitchen = 51 | ✅ |
| … | … | … |

Two aliases (`p`, `p2`) for the same table — like a self-join.

---

# Correlated: Each Customer's Latest Order

```sql
SELECT o.customer_id, o.order_id, o.order_date
FROM orders AS o
WHERE o.order_date = (SELECT MAX(o2.order_date)
                      FROM orders AS o2
                      WHERE o2.customer_id = o.customer_id)
ORDER BY o.customer_id;
```

| customer_id | order_id | order_date |
|---|---|---|
| 1 | 13 | 2026-09-18 |
| 2 | 4 | 2026-09-05 |
| 3 | 6 | 2026-09-08 |
| 4 | 8 | 2026-09-11 |
| 5 | 10 | 2026-09-14 |
| 6 | 14 | 2026-09-20 |

The guest order is not here: `o2.customer_id = NULL` never matches.

---

# Subquery or JOIN?

**"Which customers placed an order?"** with a JOIN:

```sql
SELECT c.customer_name
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
ORDER BY c.customer_name;
```

**13 rows!** Alice appears 3 times — once per order.

---

# Subquery or JOIN? (continued)

| | Rows | Note |
|---|---|---|
| `INNER JOIN` | 13 | one row **per order** |
| `SELECT DISTINCT ... INNER JOIN` | 6 | duplicates removed |
| `WHERE customer_id IN (subquery)` | 6 | one row **per customer** |

👉 Rule of thumb:

- Need columns **from both tables**? → **JOIN**
- Only **checking** another table (yes/no)? → `IN` / `EXISTS`

---

# CTEs: Give a Subquery a Name

A **CTE** (Common Table Expression) moves a subquery to the **top**
and gives it a name with `WITH`:

```sql
WITH name AS (
    SELECT ...          -- the subquery
)
SELECT ...
FROM name;              -- use it like a table
```

- Easier to read: top to bottom, not inside-out
- You can use the name **more than once**

---

# CTE Example: Big Spenders

**"Which customers spent more than the average customer?"**

```sql
WITH customer_totals AS (
    SELECT o.customer_id,
           SUM(o.quantity * p.price) AS total_spent
    FROM orders AS o
    INNER JOIN products AS p
        ON o.product_id = p.product_id
    WHERE o.customer_id IS NOT NULL
    GROUP BY o.customer_id
)
SELECT c.customer_name, ct.total_spent
FROM customer_totals AS ct
INNER JOIN customers AS c
    ON ct.customer_id = c.customer_id
WHERE ct.total_spent > (SELECT AVG(total_spent)
                        FROM customer_totals)
ORDER BY ct.total_spent DESC;
```

---

# CTE Example — Result

| customer_name | total_spent |
|---|---|
| Alice Wong | 1550 |
| David Kim | 1500 |

- `customer_totals` is used **twice**: in `FROM` and in the subquery
- The average is 699.83 (from the derived-table slide)

---

# Which Tool for Which Question? 🗺️

| Question | Tool |
|---|---|
| "…more than the **average**?" | scalar subquery |
| "…customers **who** ordered X?" | `IN` (or `EXISTS`) |
| "…**never** ordered?" | `NOT EXISTS` (or `LEFT JOIN ... IS NULL`) |
| "…the average **of totals**?" | subquery in `FROM` |
| "…above **their own group's** average?" | correlated subquery |
| "…show columns from **both** tables" | JOIN |
| long, multi-step query | CTE (`WITH`) |

---

# Summary

- `EXISTS` / `NOT EXISTS`: is there at least one matching row?
- `NOT EXISTS` is safe with `NULL`s; `NOT IN` is not
- A subquery in `FROM` needs an alias: `AS t`
- A **correlated** subquery uses an outer column and runs once per row
- JOIN to **show** columns; `IN` / `EXISTS` to **check**
- A CTE (`WITH`) names a subquery and reads top to bottom

---

# What's Next?

**Week 8: Database Design & Normalization**

- How should tables be designed in the first place?
- Keys, `FOREIGN KEY`s, and normal forms
- Rules (`NOT NULL`, `FOREIGN KEY`) that stop bad data at the door

---

# Questions?

Thank you!

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
