# Lab 3: SQL Functions, GROUP BY, and Subqueries

## OMIS 105 — Database Management Systems
**Week 3 | Estimated time: 75–90 minutes**

---

## Setup

```python
import duckdb
con = duckdb.connect()
for t, f in [('products','products.csv'),('customers','customers.csv'),
             ('categories','categories.csv'),('orders','orders.csv')]:
    con.sql(f"CREATE TABLE {t} AS SELECT * FROM read_csv_auto('{f}')")
```

---

## Part 1: String Functions (10 points)

**Q1.** Display each customer's full name (first + last) in uppercase, along with the length of their email address. Sort by email length descending.

```sql
-- Your query here
```

**Q2.** Find all products whose name contains "Set" or "Kit" (case-insensitive). Show product_name and category.

```sql
-- Your query here
```

**Q3.** Create a column `email_domain` that extracts just the domain from each customer's email (the part after @). Show first_name, email, and email_domain.

*Hint: Look up SPLIT_PART or use SUBSTRING with POSITION.*

```sql
-- Your query here
```

---

## Part 2: Date Functions (10 points)

**Q4.** How many orders were placed in each month of 2024? Show year, month, and count. Sort by month.

```sql
-- Your query here
```

**Q5.** For each customer, calculate how many days they have been a member (from `join_date` to today). Show first_name, join_date, and days_as_member. Sort by most senior first.

```sql
-- Your query here
```

---

## Part 3: CASE Expressions (10 points)

**Q6.** Classify each product into a price tier:
- Under $15 → "Economy"
- $15 to $49.99 → "Standard"
- $50 to $149.99 → "Premium"
- $150 and above → "Luxury"

Show product_name, price, and price_tier. Count how many products fall into each tier.

```sql
-- Query 1: Show each product with its tier

-- Query 2: Count per tier
```

**Q7.** Create an `order_size` classification based on total_amount:
- Under $50 → "Small"
- $50 to $199.99 → "Medium"
- $200 to $499.99 → "Large"
- $500+ → "Extra Large"

Show the count, total revenue, and average order value for each size category.

```sql
-- Your query here
```

---

## Part 4: GROUP BY and HAVING (20 points)

**Q8.** For each category, compute: number of products, average price, total stock value (sum of price × stock_quantity). Sort by total stock value descending.

```sql
-- Your query here
```

**Q9.** Which categories have more than 5 products with stock above 100? Show category and count.

```sql
-- Your query here
```

**Q10.** Find the number of orders per customer. Show customer_id and order_count. Only include customers with 3 or more orders.

```sql
-- Your query here
```

**Q11.** What is the average order value per month in 2024? Only show months with average order value above $200.

```sql
-- Your query here
```

---

## Part 5: Subqueries (15 points)

**Q12.** List all products that are priced higher than the average price in their own category.

*Hint: Use a correlated subquery.*

```sql
-- Your query here
```

**Q13.** Find the top-spending customer (highest total across all orders). Show their name and total spent.

```sql
-- Your query here
```

**Q14.** Find all categories where every product has stock_quantity > 0 (i.e., no out-of-stock products).

```sql
-- Your query here
```

---

## Part 6: Comprehensive Query (10 points)

**Q15.** Create a "Product Dashboard" query that shows for each category:
- Category name
- Number of products
- Average price (rounded to 2 decimals)
- Cheapest and most expensive product prices
- Count of in-stock vs out-of-stock items
- Whether the category average is above or below the overall average ("Above" / "Below")

Sort by average price descending.

```sql
-- Your query here
```

---

## Submission

- Submit notebook with all queries and outputs
- **Total: 75 points**

