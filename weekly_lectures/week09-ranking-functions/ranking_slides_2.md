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
- ⚠️ Why `LIMIT` / `OFFSET` cannot answer them
- Hands-on: Lab 5

---

# Recap from Session 1

| Function | Ties | Example |
|---|---|---|
| `ROW_NUMBER()` | different numbers (needs a tie-breaker) | 1, 2, 3, 4 |
| `RANK()` | same rank, then a **gap** | 1, 2, 2, 4 |

⚠️ `ORDER BY … LIMIT n` counts **rows**: it cuts tied rows and cannot
work per group.

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

# And `LIMIT 1 OFFSET 1`?

"Skip the first row, take the next one":

```sql
SELECT item_name, price
FROM items
ORDER BY price DESC
LIMIT 1 OFFSET 1;
```

| item_name | price |
|---|---:|
| Matcha | 6.00 |

❌ `OFFSET 1` skips one **row**, not one **price**. The 2nd row is still a
6.00 item — the same mistake as `ROW_NUMBER`.

---

# "But `DISTINCT` Fixes It!" — Only Half

```sql
SELECT DISTINCT price
FROM items
ORDER BY price DESC
LIMIT 1 OFFSET 1;
```

| price |
|---:|
| 5.50 |

- ✅ The right **value**, 5.50
- ❌ But **which items** cost 5.50? You need a second query
- ❌ And the second-highest price **in each category**? `LIMIT` cannot
  restart per group

👉 `DENSE_RANK` answers all three in one query.

---

# "Top 3 Prices" — `LIMIT 3` vs. `DENSE_RANK`

`LIMIT 3` gives 3 **rows**: Mocha 6.00, Matcha 6.00, Latte 5.50 — and
Cappuccino (also 5.50) is cut.

```sql
WITH ranked AS (
    SELECT item_name, price,
           DENSE_RANK() OVER (ORDER BY price DESC) AS price_rank
    FROM items
)
SELECT item_name, price, price_rank
FROM ranked
WHERE price_rank <= 3
ORDER BY price_rank, item_name;
```

| item_name | price | price_rank |
|---|---:|---:|
| Matcha | 6.00 | 1 |
| Mocha | 6.00 | 1 |
| Cappuccino | 5.50 | 2 |
| Latte | 5.50 | 2 |
| Chai | 4.50 | 3 |

✅ The 3 highest **prices** — 5 items.

---

# "Top 2 Shops by Revenue" — `LIMIT 2`

Using the `shop_revenue` CTE from before:

```sql
SELECT shop_name, revenue
FROM shop_revenue
ORDER BY revenue DESC
LIMIT 2;
```

| shop_name | revenue |
|---|---:|
| Campus | 57.00 |
| Downtown | 44.00 |

❌ **Harbor also earned 44.00** — tied with Downtown for 2nd, but cut.
With `RANK() … WHERE rnk <= 2` you get Campus, Downtown **and** Harbor.

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
| "just show me the first few rows" (no ranking question) | `ORDER BY … LIMIT n` |

All three: `FUNCTION() OVER (PARTITION BY … ORDER BY …)`.

---

# Summary

| Pattern | SQL |
|---|---|
| no-gap ranks / price levels | `DENSE_RANK() OVER (ORDER BY col DESC)` |
| rank a `GROUP BY` result | totals in a CTE, then rank the CTE |
| filter a rank | rank in a CTE or subquery, `WHERE` outside |
| ⚠️ `LIMIT` / `OFFSET` | count **rows**: they cut ties and ignore groups — never for ranking |

Demo notebook: `ranking_demo_2.py`

---

# Questions?

Thank you!

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
