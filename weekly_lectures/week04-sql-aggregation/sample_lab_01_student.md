# Lab 4: JOINs and Multi-Table Queries

## OMIS 105 — Database Management Systems
**Week 4 | Estimated time: 75–90 minutes**

---

## Setup

```python
import duckdb
con = duckdb.connect()
for t, f in [('categories','categories.csv'),('products','products.csv'),
             ('customers','customers.csv'),('orders','orders.csv'),
             ('order_items','order_items.csv')]:
    con.sql(f"CREATE TABLE {t} AS SELECT * FROM read_csv_auto('{f}')")
```

---

## Part 1: INNER JOIN (15 points)

**Q1.** Join `customers` and `orders` to display each customer's name alongside their order details (order_id, order_date, total_amount). Show the first 15 rows sorted by order_date descending.

```sql
-- Your query here
```

**Q2.** Join `products` and `categories` to show each product's name, category name, and price. Sort by category name, then price descending.

```sql
-- Your query here
```

**Q3.** Write a 3-table join: show order_id, customer name, product name, quantity, and unit_price for all order items. Sort by order_id.

```sql
-- Your query here
```

---

## Part 2: LEFT JOIN (15 points)

**Q4.** Find all customers who have **never** placed an order. Show their first_name, last_name, and email.

```sql
-- Your query here
```

**Q5.** Find all products that have **never** been ordered. Show product_name, category_id, and price.

```sql
-- Your query here
```

**Q6.** Show all customers with their order count. Customers with no orders should show 0. Sort by order_count descending.

```sql
-- Your query here
```

---

## Part 3: JOINs with GROUP BY (20 points)

**Q7.** Calculate total revenue per category. Show category_name, total units sold, and total revenue. Sort by revenue descending.

```sql
-- Your query here
```

**Q8.** Find the top 5 best-selling products by total units sold. Show product_name, total_units, and total_revenue.

```sql
-- Your query here
```

**Q9.** Calculate each customer's total spending across all orders. Show full name, number of orders, and total spent. Only include customers who spent more than $300.

```sql
-- Your query here
```

**Q10.** Create a monthly revenue report for 2024: show year, month, number of orders, unique customers, and total revenue. Exclude cancelled orders.

```sql
-- Your query here
```

---

## Part 4: Advanced JOINs (15 points)

**Q11.** Using a self-join, find pairs of products in the same category where the price difference is less than $5. Show both product names, the category, and the price difference.

```sql
-- Your query here
```

**Q12.** Write a query using a derived table (subquery in FROM) that shows each customer's name alongside their average order value. Only include customers with at least 3 orders.

```sql
-- Your query here
```

**Q13.** Create a customer segmentation report:
- "VIP": total spending >= $1000
- "Regular": $500–$999
- "Occasional": $100–$499
- "New": under $100

Show each segment, number of customers, and average spending per segment.

```sql
-- Your query here
```

---

## Part 5: Business Report (10 points)

**Q14.** Create a comprehensive "Product Performance Report" that shows:
- Product name and category name
- Total units sold
- Total revenue
- Number of distinct orders containing this product
- Average quantity per order
- Rank by total revenue (highest first)

Include ALL products (even those never ordered, showing 0s).

```sql
-- Your query here
```

---

## Submission

- Submit notebook with all queries and outputs
- **Total: 75 points**

