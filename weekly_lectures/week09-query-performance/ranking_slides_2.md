---
title: OMIS 105 - Week 9 (Ranking Functions — DENSE_RANK and Ranking Results)
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

# OMIS 105: Week 9
## Ranking Functions — Session 2 <br> `DENSE_RANK` and Ranking Results

---

# Agenda

- Recap: `ROW_NUMBER` and `RANK`
- `DENSE_RANK()` — ties share a rank, **no gaps**
- All three functions side by side
- Ranking `GROUP BY` results with a CTE
- Best seller per category — `ROW_NUMBER` vs. `RANK`
- "Second-highest" questions
- 15 minutes on indexes
- Hands-on: Lab 5

---

# Recap from Session 1

| Function | Ties | Example |
|---|---|---|
| `ROW_NUMBER()` | different numbers (needs a tie-breaker) | 1, 2, 3, 4 |
| `RANK()` | same rank, then a **gap** | 1, 2, 2, 4 |

Today: the third function, `DENSE_RANK()` — 1, 2, 2, **3**.

---

# Our Data: A Small Café Chain ☕

```
shops ──< orders >── items
```

| Table | Rows | Columns |
|---|---|---|
| `shops` | 4 | `shop_id`, `shop_name`, `city` |
| `items` | 11 | `item_id`, `item_name`, `category`, `price` |
| `orders` | 18 | `order_id`, `shop_id`, `item_id`, `qty`, `order_date` |

---

# `items` (11 rows)

| item_id | item_name | category | price |
|---:|---|---|---:|
| 101 | Latte | Coffee | 5.50 |
| 102 | Cappuccino | Coffee | 5.50 |
| 103 | Espresso | Coffee | 3.50 |
| 104 | Mocha | Coffee | 6.00 |
| 201 | Croissant | Bakery | 4.00 |
| 202 | Muffin | Bakery | 4.00 |
| 203 | Bagel | Bakery | 3.00 |
| 204 | Scone | Bakery | 3.50 |
| 301 | Matcha | Tea | 6.00 |
| 302 | Chai | Tea | 4.50 |
| 303 | Green Tea | Tea | 3.00 |

Price ties: 6.00 (Mocha, Matcha), 5.50, 4.00, 3.50, 3.00.

---

# All Three, Side by Side

```sql
SELECT item_name, price,
       ROW_NUMBER() OVER (ORDER BY price DESC, item_name) AS row_num,
       RANK()       OVER (ORDER BY price DESC)            AS rnk,
       DENSE_RANK() OVER (ORDER BY price DESC)            AS dense_rnk
FROM items
ORDER BY row_num;
```

---

# All Three — Result

| item_name | price | row_num | rnk | dense_rnk |
|---|---:|---:|---:|---:|
| Matcha | 6.00 | 1 | 1 | 1 |
| Mocha | 6.00 | 2 | 1 | 1 |
| Cappuccino | 5.50 | 3 | 3 | 2 |
| Latte | 5.50 | 4 | 3 | 2 |
| Chai | 4.50 | 5 | 5 | 3 |
| Croissant | 4.00 | 6 | 6 | 4 |
| Muffin | 4.00 | 7 | 6 | 4 |
| Espresso | 3.50 | 8 | 8 | 5 |
| Scone | 3.50 | 9 | 8 | 5 |
| Bagel | 3.00 | 10 | 10 | 6 |
| Green Tea | 3.00 | 11 | 10 | 6 |

---

# Reading the Three Columns

- `row_num` — always **1, 2, 3, …** (ties broken by `item_name`)
- `rnk` — ties share a rank, then a **gap** (1, 1, **3**)
- `dense_rnk` — ties share a rank, **no gap** (1, 1, **2**)

👉 `dense_rnk` counts **price levels**: there are 6 different prices,
so it ends at 6.

---

# Ranking `GROUP BY` Results with a CTE

Rank the shops by revenue (`qty × price`):

```sql
WITH shop_revenue AS (
    SELECT s.shop_name,
           SUM(o.qty * i.price) AS revenue
    FROM orders AS o
    JOIN items  AS i ON i.item_id = o.item_id
    JOIN shops  AS s ON s.shop_id = o.shop_id
    GROUP BY s.shop_name
)
SELECT shop_name, revenue,
       RANK()       OVER (ORDER BY revenue DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY revenue DESC) AS dense_rnk
FROM shop_revenue
ORDER BY revenue DESC, shop_name;
```

---

# Shop Ranking — Result

| shop_name | revenue | rnk | dense_rnk |
|---|---:|---:|---:|
| Campus | 57.00 | 1 | 1 |
| Downtown | 44.00 | 2 | 2 |
| Harbor | 44.00 | 2 | 2 |
| Airport | 40.00 | 4 | 3 |

- Downtown and Harbor tie at 44.00
- Airport is **4th** by `RANK` (three shops earned more) but **3rd**
  by `DENSE_RANK` (two revenue levels are above it)

---

# Units Sold per Item

```sql
SELECT i.category, i.item_name,
       SUM(o.qty) AS units_sold
FROM items AS i
JOIN orders AS o ON o.item_id = i.item_id
GROUP BY i.category, i.item_name
ORDER BY i.category, units_sold DESC, i.item_name;
```

---

# Units Sold — Result

| category | item_name | units_sold |
|---|---|---:|
| Bakery | Croissant | 5 |
| Bakery | Muffin | 5 |
| Bakery | Bagel | 3 |
| Bakery | Scone | 2 |
| Coffee | Cappuccino | 6 |
| Coffee | Latte | 5 |
| Coffee | Mocha | 4 |
| Coffee | Espresso | 2 |
| Tea | Chai | 3 |
| Tea | Matcha | 3 |
| Tea | Green Tea | 2 |

Ties at the top: Croissant and Muffin (Bakery), Chai and Matcha (Tea).

---

# Best Seller per Category — `ROW_NUMBER`

```sql
WITH units AS (
    SELECT i.category, i.item_name, SUM(o.qty) AS units_sold
    FROM items AS i
    JOIN orders AS o ON o.item_id = i.item_id
    GROUP BY i.category, i.item_name
),
ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY category
                                 ORDER BY units_sold DESC, item_name) AS rn
    FROM units
)
SELECT category, item_name, units_sold
FROM ranked
WHERE rn = 1
ORDER BY category;
```

---

# Best Seller — `ROW_NUMBER` Result

| category | item_name | units_sold |
|---|---|---:|
| Bakery | Croissant | 5 |
| Coffee | Cappuccino | 6 |
| Tea | Chai | 3 |

⚠️ Exactly one row per category. Muffin and Matcha also sold the most
— they were cut only by the tie-breaker (`item_name`).

---

# Best Seller per Category — `RANK`

Change one line in the `ranked` CTE:

```sql
SELECT *, RANK() OVER (PARTITION BY category
                       ORDER BY units_sold DESC) AS rnk
...
WHERE rnk = 1
```

| category | item_name | units_sold |
|---|---|---:|
| Bakery | Croissant | 5 |
| Bakery | Muffin | 5 |
| Coffee | Cappuccino | 6 |
| Tea | Chai | 3 |
| Tea | Matcha | 3 |

👉 **5 rows**: both tied items are shown for Bakery and Tea.

---

# "What Is the Second-Highest Price?"

```sql
WITH ranked AS (
    SELECT item_name, price,
           DENSE_RANK() OVER (ORDER BY price DESC) AS price_rank
    FROM items
)
SELECT item_name, price
FROM ranked
WHERE price_rank = 2
ORDER BY item_name;
```

| item_name | price |
|---|---:|
| Cappuccino | 5.50 |
| Latte | 5.50 |

---

# Why Not `RANK` or `ROW_NUMBER`?

| Version | `= 2` returns | Why |
|---|---|---|
| `DENSE_RANK` | Cappuccino, Latte (5.50) ✅ | 5.50 is the 2nd price **level** |
| `RANK` | **no rows** ❌ | two items tie at 1, so the next rank is 3 |
| `ROW_NUMBER` (tie-breaker `item_name`) | Mocha (6.00) ❌ | the 2nd **row** is still a 6.00 item |

👉 For "Nth-highest **value**" questions, use `DENSE_RANK`.

---

# ⚠️ Again: `WHERE` Cannot See the Rank

```sql
SELECT item_name, price,
       DENSE_RANK() OVER (ORDER BY price DESC) AS price_rank
FROM items
WHERE price_rank = 2;
```

```
Binder Error: WHERE clause cannot contain window functions!
```

👉 Fix: compute the rank in a **CTE** (or subquery), then filter it
outside — as on the previous slides.

---

# Which Ranking Function?

| The question says… | Use |
|---|---|
| "exactly N per group", "first / last event" | `ROW_NUMBER` + tie-breaker |
| "top N, include ties" (competition ranking) | `RANK` |
| "Nth-highest value", "top N price levels" | `DENSE_RANK` |

All three: `FUNCTION() OVER (PARTITION BY … ORDER BY …)`.

---

# 15 Minutes on Indexes 📇

- An **index** is like the index at the back of a book: the database
  finds rows **without reading the whole table**
- `CREATE INDEX idx_orders_date ON orders (order_date);`
- Good for: columns you often search with `WHERE` or `JOIN` on
- Cost: extra storage, and slower `INSERT` / `UPDATE`

More detail: `slides_1.md` (this folder).

---

# Write Searches the Index Can Use

Both return the same answer:

```sql
SELECT COUNT(*) AS orders_2026
FROM orders
WHERE YEAR(order_date) = 2026;
```

```sql
SELECT COUNT(*) AS orders_2026
FROM orders
WHERE order_date >= DATE '2026-01-01'
  AND order_date <  DATE '2027-01-01';
```

| orders_2026 |
|---:|
| 18 |

- `YEAR(order_date) = 2026` must compute `YEAR()` for **every row** — an
  index on `order_date` cannot help
- The **range** compares `order_date` itself — an index can jump
  straight to 2026

👉 Rule: keep the column **alone** on one side of the comparison.

---

# Summary

| Pattern | SQL |
|---|---|
| no-gap ranks / price levels | `DENSE_RANK() OVER (ORDER BY col DESC)` |
| rank a `GROUP BY` result | totals in a CTE, then rank the CTE |
| filter a rank | rank in a CTE or subquery, `WHERE` outside |
| index-friendly date filter | `col >= DATE '…' AND col < DATE '…'` |

Demo notebook: `ranking_demo_2.py`

---

# Questions?

Thank you!

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
