# OMIS 105 — Database Management Systems
## Midterm Exam — Practice Version 2 (Material Covered So Far)

**Instructor:** Dr. Parsian

**Coverage:** 

* Week 1 (Database Foundations; `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `BETWEEN`, `LIKE`, `IN`)
* Week 2 (Aggregate Functions, `GROUP BY`, `HAVING`)
* Week 3 (Primary Keys, CRUD: `INSERT` / `SELECT` / `UPDATE` / `DELETE`, `NULL` handling)

**Total Points:** <br>

* 100
	* Part 1: 30 pts
	* Part 2: 70 pts

---

## Reference Schema — Food Delivery Orders

All questions use the following single table from a local **food delivery** startup:

```sql
CREATE TABLE orders (
    order_id      INTEGER PRIMARY KEY,
    customer_name VARCHAR NOT NULL,
    city          VARCHAR,
    restaurant    VARCHAR NOT NULL,
    cuisine       VARCHAR,
    order_total   DECIMAL(8,2) CHECK (order_total > 0),
    tip           DECIMAL(6,2),
    order_date    DATE,
    status        VARCHAR CHECK (status IN ('placed','delivered','cancelled'))
);
```

`tip` is `NULL` when no tip has been recorded for the order.

### Sample Data (10 rows)

| order_id | customer_name | city        | restaurant  | cuisine    | order_total | tip    | order_date | status    |
|---------:|---------------|-------------|-------------|------------|------------:|-------:|------------|-----------|
| 1        | Ana           | San Jose    | Taco Loco   | Mexican    | 24.50       | 4.00   | 2026-09-01 | delivered |
| 2        | Ben           | Santa Clara | Pho King    | Vietnamese | 18.00       | `NULL` | 2026-09-01 | delivered |
| 3        | Cara          | San Jose    | Pizza Roma  | Italian    | 42.00       | 6.00   | 2026-09-02 | delivered |
| 4        | Dev           | Sunnyvale   | Taco Loco   | Mexican    | 15.75       | `NULL` | 2026-09-02 | cancelled |
| 5        | Eli           | Santa Clara | Pizza Roma  | Italian    | 36.50       | 5.00   | 2026-09-03 | delivered |
| 6        | Fay           | San Jose    | Curry House | Indian     | 28.00       | `NULL` | 2026-09-03 | placed    |
| 7        | Gus           | Sunnyvale   | Pho King    | Vietnamese | 22.00       | 3.00   | 2026-09-04 | delivered |
| 8        | Hana          | Santa Clara | Curry House | Indian     | 31.25       | 4.50   | 2026-09-04 | delivered |
| 9        | Ian           | San Jose    | Pizza Roma  | Italian    | 55.00       | 8.00   | 2026-09-05 | delivered |
| 10       | Jo            | Sunnyvale   | Taco Loco   | Mexican    | 12.50       | `NULL` | 2026-09-05 | placed    |

Unless a question says otherwise, assume the table contains **exactly these 10 rows** before each question.
Keep the schema and data visible while answering both parts of the exam.

---

# Part 1 — Multiple Choice (30 points, 2 pts each)

Circle/select the single best answer for each question.

### 1. (Week 1) The startup currently keeps its orders in a shared spreadsheet. Two managers often edit it at the same time, the same city is typed as both `"San Jose"` and `"San Jos"`, and someone once typed `"free"` into the order-total column. What is the main advantage of moving this data into a DBMS?

A) A DBMS makes the data visible only as charts instead of rows

B) A DBMS enforces a schema (data types and constraints) and safely manages many users reading and writing the same data at once

C) A DBMS automatically corrects spelling mistakes in every text column

D) A DBMS stores data without any structure, so any value can go in any column

### 2. (Week 1) Which of the following is **metadata** about the `orders` table (data *about* the data), rather than data stored *in* it?

A) The value `'Taco Loco'` in row 1

B) The value `42.00` in row 3

C) The fact that `order_total` is declared as `DECIMAL(8,2)` with `CHECK (order_total > 0)`

D) The date `2026-09-05` on Ian's order

### 3. (Week 1) Why is `order_total` declared as `DECIMAL(8,2)` rather than `INTEGER`?

A) `INTEGER` cannot store negative numbers

B) `DECIMAL(8,2)` stores dollars-and-cents values like `24.50` exactly; `INTEGER` would drop the cents

C) `DECIMAL` columns are automatically indexed

D) `INTEGER` columns cannot be used with `SUM()` or `AVG()`

### 4. (Week 1) Which `INSERT` statement will DuckDB **reject**?

A) `INSERT INTO orders VALUES (11,'Kim','San Jose','Taco Loco','Mexican',20.00,NULL,'2026-09-06','delivered');`

B) `INSERT INTO orders VALUES (12,'Lee','San Jose','Taco Loco',NULL,20.00,2.00,'2026-09-06','delivered');`

C) `INSERT INTO orders VALUES (13,'Max',NULL,'Taco Loco','Mexican',20.00,2.00,'2026-09-06','delivered');`

D) `INSERT INTO orders VALUES (14,'Ned','San Jose','Taco Loco','Mexican',20.00,2.00,'2026-09-06','refunded');`

### 5. (Week 3) Which column is the best choice for the **primary key** of `orders`?

A) `customer_name`, because every name in the sample data is different

B) `order_id`, because each order gets its own unique, non-NULL identifier that never needs to repeat

C) `restaurant`, because every order has a restaurant

D) `order_date`, because every order happens on some date

### 6. (Week 3) What happens when you run the following statement against the 10-row table?

```sql
INSERT INTO orders VALUES
  (3, 'Zoe', 'San Jose', 'Taco Loco', 'Mexican', 20.00, 2.00, '2026-09-06', 'delivered');
```

A) The table now has 11 rows, two of which have `order_id = 3`

B) Cara's order (row 3) is replaced by Zoe's order

C) DuckDB raises a primary-key (duplicate key) error, and the table still has the original 10 rows

D) DuckDB silently changes Zoe's `order_id` to 11

### 7. (Week 3) A teammate wants to mark **only order 6** as delivered, and runs:

```sql
UPDATE orders
SET status = 'delivered';
```

What actually happens?

A) Only order 6 is changed, because it is the first `'placed'` order

B) Only the two `'placed'` orders (6 and 10) are changed

C) All 10 rows now have `status = 'delivered'`

D) DuckDB refuses to run an `UPDATE` without a `WHERE` clause

### 8. (Week 3) Management wants to **remove all cancelled orders** but keep the `orders` table and all its other rows. Which statement does this?

A) `DROP TABLE orders;`

B) `DELETE FROM orders WHERE status = 'cancelled';`

C) `DELETE FROM orders;`

D) `UPDATE orders SET status = NULL WHERE status = 'cancelled';`

### 9. (Week 1) How many rows does this query return?

```sql
SELECT *
FROM orders
WHERE order_total BETWEEN 22.00 AND 31.25;
```

A) 2

B) 3

C) 4

D) 5

### 10. (Week 3) What does this query return?

```sql
SELECT COUNT(*), COUNT(tip)
FROM orders;

```

A) `10, 10`

B) `10, 6`

C) `6, 6`

D) `10, 4`

### 11. (Week 3) How many rows does this query return? (Think carefully about `NULL`.)

```sql
SELECT *
FROM orders
WHERE tip > 3 OR tip <= 3;
```

A) 10 — every number is either greater than 3 or not

B) 6

C) 5

D) 4

### 12. (Week 1) Which query returns the **three largest** orders by `order_total`?

A)

```sql
SELECT * FROM orders
ORDER BY order_total
LIMIT 3;
```

B)

```sql
SELECT * FROM orders
ORDER BY order_total DESC
LIMIT 3;
```

C)

```sql
SELECT * FROM orders
LIMIT 3
ORDER BY order_total DESC;
```

D)

```sql
SELECT * FROM orders
WHERE order_total = MAX(order_total)
LIMIT 3;
```

### 13. (Week 2) What is the result of this query?

```sql
SELECT restaurant, COUNT(*) AS num_orders
FROM orders
WHERE status = 'delivered'
GROUP BY restaurant
HAVING COUNT(*) >= 2;
```

A) Pizza Roma (3) only

B) Pho King (2) and Pizza Roma (3)

C) Taco Loco (1), Pho King (2), Pizza Roma (3), Curry House (1)

D) Taco Loco (3), Pho King (2), Pizza Roma (3), Curry House (2)

### 14. (Week 2) Which of these queries produces an **error**?

A) `SELECT city, COUNT(*) FROM orders GROUP BY city;`

B) `SELECT city, restaurant, COUNT(*) FROM orders GROUP BY city;`

C) `SELECT city, restaurant, COUNT(*) FROM orders GROUP BY city, restaurant;`

D) `SELECT COUNT(DISTINCT city) FROM orders;`

### 15. (Week 2) Which is the correct **logical execution order** of the clauses in a `SELECT` statement?

A) `SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT`

B) `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`

C) `FROM → GROUP BY → WHERE → SELECT → HAVING → LIMIT → ORDER BY`

D) `WHERE → FROM → SELECT → GROUP BY → HAVING → ORDER BY → LIMIT`

---

# Part 2 — Written Questions (70 points)

Show your reasoning. For SQL questions, write a single query unless told otherwise; minor syntax slips are fine as long as the logic is correct.

## Simple (10 points each — 20 points total)

**S1.** What is a **primary key**? State the **two rules** a primary key column enforces. Then explain why `customer_name` would be a poor primary key for `orders`, *even though* every name in the 10-row sample happens to be unique.

**S2.** Explain what `NULL` means in the `tip` column. Then answer:
(a) Why does `WHERE tip = NULL` return no rows, and what should you write instead?
(b) Using the sample data, explain why `COUNT(*)` and `COUNT(tip)` give different answers.

## Intermediate (15 points each — 30 points total)

**I1.** Write a SQL query that returns the `customer_name`, `restaurant`, and `order_total` of every **delivered** order from **San Jose or Santa Clara** whose `order_total` is **at least $25**, sorted from largest to smallest `order_total`.
Then state how many rows your query returns on the sample data.

**I2.** Write the **three CRUD statements** below, in order, against the 10-row table:

a. **Create:** add order `11` for customer `'Kim'` in `'Sunnyvale'` from `'Pizza Roma'` (`'Italian'`), total `$47.00`, no tip recorded yet, dated `2026-09-06`, with status `'placed'`.

b. **Update:** order `6` has just been delivered and Fay left a `$5.00` tip — change **both** its `status` and its `tip` in a single statement.

c. **Delete:** remove every cancelled order.

d. After all three statements run, how many rows are in `orders`? How many have `status = 'placed'`?

## Advanced (10 points each — 20 points total)

**A1.** Management wants a **cuisine performance report** that only counts **delivered** orders. For each cuisine, return `cuisine`, `num_orders` (number of delivered orders), `total_revenue` (sum of `order_total`), and `avg_order` (average `order_total`). Only include cuisines with **at least 2** delivered orders, and sort by `total_revenue` from highest to lowest.
Then write out the **result table** your query produces on the sample data.

**A2.** A classmate wants to see the **average tip per city**, but only for cities where the average tip is **above $4.00**. They wrote:

```sql
SELECT city, restaurant, AVG(tip) AS avg_tip
FROM orders
WHERE AVG(tip) > 4
GROUP BY city
ORDER BY avg_tip DESC;
```

`(a)` Identify the **two** mistakes in this query and explain why each one is an error.

`(b)` Write the corrected query.

`(c)` Write out the result of your corrected query on the sample data.

`(d)` `AVG()` ignores `NULL` tips. If the `NULL` tips were instead treated as `$0.00`, which city would **drop out** of the result, and why?

---

*End of Exam*
