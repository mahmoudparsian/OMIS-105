# Lab 7: Subqueries — A Query Inside a Query

## OMIS 105 — Database Management Systems
**Week 7 | Estimated time: 75–90 minutes | 10 questions × 3 points = 30 points**

---

## Setup

Open a new Marimo notebook **inside the `week07-subqueries` folder**
(so the `data/` path works), and run this cell first:

```python
import duckdb
con = duckdb.connect(database=":memory:")
for t in ["customers", "products", "orders"]:
    con.execute(f"CREATE OR REPLACE TABLE {t} AS SELECT * FROM read_csv('data/{t}.csv')")
```

Then write each answer in its own cell:

```python
con.execute("""
    SELECT ...
""").fetchdf()
```

**The tables** (the same data as the demos):

| Table | Columns |
|---|---|
| `customers` | `customer_id`, `customer_name`, `city` |
| `products` | `product_id`, `product_name`, `category`, `price` |
| `orders` | `order_id`, `customer_id`, `product_id`, `quantity`, `order_date` |

Remember: order 12 is a guest order, so its `customer_id` is `NULL`.

**Rules for every query:**

- **Every answer must use a subquery** (or a CTE in Q10). No number
  typed by hand: `WHERE price > 325.875` gets 0 points
- List the columns you need — no `SELECT *`
- Use the `ORDER BY` given in the question
- The **expected row count** is given for each question. If your
  count is different, check your subquery on its own first.

---

## Part 1: Scalar Subqueries — One Value (9 points)

**Q1. Cheaper than average.** Show `product_name` and `price` for products that cost **less** than the average price. Order by `price`.

*Expected: 6 rows.*

```sql
-- your query here

```

---

**Q2. The cheapest product.** Show `product_name` and `price` of the product(s) with the **lowest** price. Use `MIN` in a subquery, not `ORDER BY ... LIMIT 1`.

*Expected: 1 row.*

```sql
-- your query here

```

---

**Q3. A subquery in `SELECT`.** For every product, show `product_name`, `price`, and how much more it costs than the cheapest product, as `above_cheapest`. Order by `above_cheapest` (highest first).

*Expected: 8 rows.*

```sql
-- your query here

```

---

## Part 2: List Subqueries — `IN`, `NOT IN`, `EXISTS` (12 points)

**Q4. Nested `IN`.** Show the `product_name` of every product ordered by a customer who lives in `'San Jose'`. Use two nested `IN` subqueries, no JOIN. Order by `product_name`.

*Expected: 4 rows.*

```sql
-- your query here

```

---

**Q5. `NOT IN`.** Show the `product_name` of products that were **never ordered**. Order by `product_name`. In one sentence: why is `NOT IN` safe here, but not for customers?

*Expected: 2 rows.*

```sql
-- your query here

```

---

**Q6. `NOT EXISTS`.** Show `customer_name` and `city` of customers who **never ordered**. Use `NOT EXISTS`. Order by `customer_name`.

*Expected: 2 rows.*

```sql
-- your query here

```

---

**Q7. `EXISTS`.** Show the `product_name` of products that appear in **at least one** order with a `quantity` of **3 or more**. Use `EXISTS`. Order by `product_name`.

*Expected: 2 rows.*

```sql
-- your query here

```

---

## Part 3: Going Further (9 points)

**Q8. A subquery in `FROM`.** What is the average number of orders per customer? Count orders per customer in a subquery (leave out the guest order), then average those counts in the outer query, rounded to 2 decimals, as `avg_orders_per_customer`.

*Expected: 1 row.*

```sql
-- your query here

```

---

**Q9. Correlated subquery.** Show `product_name`, `category`, and `price` of products that cost **less** than the average price **of their own category**. Order by `category`, then `product_name`.

*Expected: 5 rows.*

```sql
-- your query here

```

---

**Q10. CTE.** Use `WITH product_sales AS (...)` to total the `quantity` sold per product as `units_sold`. Then show the `product_name` and `units_sold` of the best-selling product(s).

*Expected: 1 row.*

```sql
-- your query here

```

---


---

## Grading

- 3 points per question: 2 for a correct result, 1 for using the
  required tool (subquery, `IN`, `NOT EXISTS`, `EXISTS`, CTE) cleanly
- Q5's short written answer is part of its second point


---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
