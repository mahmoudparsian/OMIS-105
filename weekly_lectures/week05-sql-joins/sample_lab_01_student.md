# Lab 5: Window Functions, CTEs, Set Operations, and Views

## OMIS 105 — Database Management Systems
**Week 5 | Estimated time: 75–90 minutes**

---

## Setup

```python
import duckdb
con = duckdb.connect()
for t, f in [('categories','categories.csv'),('products','products.csv'),
             ('customers','customers.csv'),('orders','orders.csv'),
             ('order_items','order_items.csv'),('reviews','reviews.csv'),
             ('suppliers','suppliers.csv'),('product_suppliers','product_suppliers.csv')]:
    con.sql(f"CREATE TABLE {t} AS SELECT * FROM read_csv_auto('{f}')")
```

---

## Part 1: Window Functions (25 points)

**Q1.** Rank all products by price within each category. Show product_name, category_id, price, and rank_in_category. Display only the top 2 per category.

```sql
-- Your query here
```

**Q2.** For each order, show the order_id, total_amount, and the running cumulative total over time (ordered by order_date). Also show what percentage each order contributes to the grand total.

```sql
-- Your query here
```

**Q3.** Using LAG, show each order alongside the previous order's total_amount for the same customer. Compute the difference between consecutive orders.

```sql
-- Your query here
```

**Q4.** Divide all customers into 5 spending tiers using NTILE (based on total spending from orders). Show customer name, total spent, and tier.

```sql
-- Your query here
```

**Q5.** For each product, show its price compared to its category: the category average, category min, category max, and what percentile the product's price falls in within its category (use PERCENT_RANK).

```sql
-- Your query here
```

---

## Part 2: CTEs (15 points)

**Q6.** Using a CTE, find the top 5 customers by total spending, then show their most recent order date and number of orders.

```sql
-- Your query here
```

**Q7.** Using multiple CTEs, create a report that shows:
1. Each category's total revenue (from order_items)
2. The overall total revenue
3. Each category's percentage of total revenue

```sql
-- Your query here
```

**Q8.** Write a CTE-based query for a "Customer Lifetime Value" report that shows each customer's name, first order date, last order date, number of orders, total spent, and average order value.

```sql
-- Your query here
```

---

## Part 3: Set Operations (10 points)

**Q9.** Using EXCEPT, find customer_ids who have placed orders but have never written a review.

```sql
-- Your query here
```

**Q10.** Using INTERSECT, find products that appear in both order_items AND reviews.

```sql
-- Your query here
```

---

## Part 4: Views (15 points)

**Q11.** Create a view called `product_performance` that shows each product's name, category, price, total units sold, total revenue, average review rating, and number of reviews. Use LEFT JOINs so all products are included.

```sql
-- Your CREATE VIEW here
-- Then query the view
```

**Q12.** Create a view called `monthly_dashboard` that shows year, month, order count, unique customers, total revenue, average order value, and month-over-month revenue change (using LAG).

```sql
-- Your CREATE VIEW here
-- Then query the view
```

---

## Part 5: Comprehensive Analysis (10 points)

**Q13.** Combine window functions, CTEs, and JOINs to create an "RFM Analysis" (Recency, Frequency, Monetary). For each customer show: name, days since last order, number of orders, total spent, plus an R/F/M score (each 1–4 using NTILE). Determine a simple segment: "Champion" (all scores >= 3), "At Risk" (R score = 1), or "Average" (everyone else).

```sql
-- Your query here
```

---

## Submission

- Submit notebook with all queries and outputs
- **Total: 75 points**

