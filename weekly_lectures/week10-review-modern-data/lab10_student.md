# Lab 10: Comprehensive Review & Practice Exam

## OMIS 105 — Database Management Systems
**Week 10 | Estimated time: 90 minutes**

---

## Setup

```python
import duckdb
con = duckdb.connect()
for t, f in [('categories','categories.csv'),('products','products.csv'),
             ('customers','customers.csv'),('orders','orders.csv'),
             ('order_items','order_items.csv'),('reviews','reviews.csv'),
             ('suppliers','suppliers.csv'),('product_suppliers','product_suppliers.csv'),
             ('shipping','shipping.csv')]:
    con.sql(f"CREATE TABLE {t} AS SELECT * FROM read_csv_auto('{f}')")
```

---

## Part 1: Conceptual Questions (20 points)

Answer these in your own words (2–3 sentences each).

**Q1.** What is the difference between a primary key and a foreign key? Give an example from ShopSmart.

**Q2.** Explain the difference between WHERE and HAVING. When would you use each?

**Q3.** What is a transitive dependency? Give an example and explain how to fix it.

**Q4.** Explain the difference between INNER JOIN and LEFT JOIN. When would you choose LEFT JOIN?

**Q5.** What does Atomicity mean in the context of ACID? Why is it important for an e-commerce system?

---

## Part 2: Schema Design (15 points)

**Q6.** Given the following requirements for a **Movie Theater** database:
- Movies have a title, genre, duration, and rating (G/PG/PG-13/R)
- Theaters have multiple screens, each with a capacity
- Showtimes link a movie to a screen at a specific date/time
- Customers can purchase tickets for specific showtimes
- Each ticket has a seat number and price

a) List all functional dependencies.
b) Write CREATE TABLE statements for all tables (minimum 5).
c) Identify all relationships and their cardinality.

```sql
-- Your CREATE TABLE statements here
```

---

## Part 3: SQL Queries on ShopSmart (30 points)

Write SQL queries for each of the following. Include comments explaining your approach.

**Q7.** Find the top 3 customers by total spending. Show their full name, number of orders, total spent, and average order value.

```sql
-- Your query here
```

**Q8.** For each category, find the product with the highest number of reviews. Show category_name, product_name, and review_count. (Use a window function.)

```sql
-- Your query here
```

**Q9.** Calculate the month-over-month revenue growth rate for 2024. Show month, revenue, previous month's revenue, and growth percentage. (Use LAG.)

```sql
-- Your query here
```

**Q10.** Find customers who have ordered products from at least 4 different categories. Show their name and the number of distinct categories.

```sql
-- Your query here
```

**Q11.** Using a CTE, create a "supplier performance" report that shows each supplier's name, number of products they supply, the average cost price, and the average retail margin (retail price - cost price).

```sql
-- Your query here
```

**Q12.** Find the average shipping time (days between order_date and delivery_date) by carrier. Only include completed orders with a delivery date. Rank carriers by speed.

```sql
-- Your query here
```

---

## Part 4: Normalization (15 points)

**Q13.** The following denormalized table tracks employee training:

```
training_log(
    employee_id, employee_name, department, dept_manager,
    course_id, course_title, instructor_name, instructor_email,
    completion_date, score, certificate_id
)
```

a) Identify all functional dependencies.
b) What is the candidate key?
c) Is this in 1NF? 2NF? 3NF? Explain.
d) Decompose into 3NF. Write CREATE TABLE statements.

---

## Part 5: Transaction Design (10 points)

**Q14.** Write a Python function `process_return(con, order_id)` that handles a product return:
1. Verify the order exists and status is 'completed'
2. Change order status to 'returned'
3. Restore stock for each item in the order
4. Calculate the refund amount
5. Handle errors with ROLLBACK

Test with both a valid and invalid order_id.

```python
# Your function here
```

---

## Part 6: Performance & Design (10 points)

**Q15.** Given that ShopSmart runs these queries thousands of times per day:

```sql
A: SELECT * FROM orders WHERE customer_id = ? AND order_date > ?
B: SELECT * FROM products WHERE category_id = ? AND price < ?
C: SELECT * FROM reviews WHERE product_id = ? ORDER BY review_date DESC LIMIT 5
```

a) What indexes would you create? Explain each choice.
b) Would you create a view for any of these? Why or why not?
c) Are there any queries where an index would NOT help? Explain.

---

## Submission

- Submit notebook with all answers, queries, and outputs
- **Total: 100 points** (this lab counts as your review/practice exam)

