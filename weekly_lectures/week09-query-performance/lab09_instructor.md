# Lab 9: Ranking Functions — `ROW_NUMBER`, `RANK`, `DENSE_RANK`

## OMIS 105 — Database Management Systems
**Week 9 | Answer Key | 10 questions × 3 points = 30 points**

Every query and result below was run against the CSVs in `data/` (DuckDB 1.5.5 and 2.0 give the same output).

---

## Part 1: `ROW_NUMBER` (9 points)

**Q1. Number the products.** *Expected: 10 rows.*

```sql
SELECT product_name, price,
       ROW_NUMBER() OVER (ORDER BY price DESC, product_id) AS rn
FROM products
ORDER BY rn
LIMIT 10;
```

| product_name | price | rn |
|---|---|---|
| Tablet Air | 446.63 | 1 |
| Laptop Pro 15 | 372.07 | 2 |
| Smartphone X12 | 321.52 | 3 |
| Bluetooth Speaker | 297.29 | 4 |
| Green Tea Box | 149.61 | 5 |
| Building Blocks | 148.48 | 6 |
| Shower Curtain | 147.86 | 7 |
| Cargo Shorts | 146.10 | 8 |
| Cotton T-Shirt | 143.80 | 9 |
| Science Set | 137.40 | 10 |

---

**Q2. Restart for each category.** *Expected: 64 rows; exactly 8 rows have `rn = 1`.*

```sql
SELECT c.category_name, p.product_name, p.price,
       ROW_NUMBER() OVER (PARTITION BY c.category_name
                          ORDER BY p.price DESC, p.product_id) AS rn
FROM products AS p
JOIN categories AS c ON c.category_id = p.category_id
ORDER BY c.category_name, rn;
```

| category_name | product_name | price | rn |
|---|---|---|---|
| Beauty | Face Moisturizer | 132.07 | 1 |
| Beauty | Eye Serum | 113.02 | 2 |
| Beauty | Shampoo Natural | 98.21 | 3 |
| Beauty | Nail Kit | 67.12 | 4 |
| Beauty | Lip Balm Set | 62.37 | 5 |
| Beauty | Hand Cream | 43.41 | 6 |
| Beauty | Body Lotion | 43.10 | 7 |
| Beauty | Sunscreen SPF50 | 35.83 | 8 |
| Books | SQL Cookbook | 122.37 | 1 |
| Books | Data Science Handbook | 115.03 | 2 |
| … 54 more rows |  |  |  |

---

**Q3. The most expensive product in each category.** *Expected: 8 rows.*

```sql
SELECT category_name, product_name, price
FROM (
    SELECT c.category_name, p.product_name, p.price,
           ROW_NUMBER() OVER (PARTITION BY c.category_name
                              ORDER BY p.price DESC, p.product_id) AS rn
    FROM products AS p
    JOIN categories AS c ON c.category_id = p.category_id
) AS ranked
WHERE rn = 1
ORDER BY category_name;
```

| category_name | product_name | price |
|---|---|---|
| Beauty | Face Moisturizer | 132.07 |
| Books | SQL Cookbook | 122.37 |
| Clothing | Cargo Shorts | 146.10 |
| Electronics | Tablet Air | 446.63 |
| Food & Grocery | Green Tea Box | 149.61 |
| Home & Kitchen | Shower Curtain | 147.86 |
| Sports | Resistance Bands | 110.72 |
| Toys | Building Blocks | 148.48 |

---

## Part 2: Ties — `RANK` and `DENSE_RANK` (12 points)

**Q4. All three, side by side.** *Expected: 10 rows.*

```sql
WITH order_counts AS (
    SELECT cu.customer_id, cu.first_name,
           COUNT(*) AS n_orders
    FROM customers AS cu
    JOIN orders AS o ON o.customer_id = cu.customer_id
    GROUP BY cu.customer_id, cu.first_name
)
SELECT customer_id, first_name, n_orders,
       ROW_NUMBER() OVER (ORDER BY n_orders DESC, customer_id) AS row_num,
       RANK()       OVER (ORDER BY n_orders DESC)              AS rnk,
       DENSE_RANK() OVER (ORDER BY n_orders DESC)              AS dense_rnk
FROM order_counts
ORDER BY row_num
LIMIT 10;
```

| customer_id | first_name | n_orders | row_num | rnk | dense_rnk |
|---|---|---|---|---|---|
| 18 | Rosa | 9 | 1 | 1 | 1 |
| 29 | Cora | 9 | 2 | 1 | 1 |
| 30 | Derek | 9 | 3 | 1 | 1 |
| 13 | Mia | 8 | 4 | 4 | 2 |
| 39 | Nora | 8 | 5 | 4 | 2 |
| 5 | Eva | 7 | 6 | 6 | 3 |
| 7 | Grace | 7 | 7 | 6 | 3 |
| 16 | Pete | 7 | 8 | 6 | 3 |
| 17 | Quinn | 7 | 9 | 6 | 3 |
| 20 | Tina | 7 | 10 | 6 | 3 |

**Note:** Rosa, Cora, Derek (9 orders): `rnk` 1, `dense_rnk` 1. Mia (8 orders): **`rnk` 4, `dense_rnk` 2** — `RANK` skips 2 and 3 after the three-way tie; `DENSE_RANK` does not.

---

**Q5. Top 4 — keeping ties.** *Expected: 5 rows.*

```sql
WITH order_counts AS (
    SELECT cu.customer_id, cu.first_name,
           COUNT(*) AS n_orders
    FROM customers AS cu
    JOIN orders AS o ON o.customer_id = cu.customer_id
    GROUP BY cu.customer_id, cu.first_name
),
ranked AS (
    SELECT *, RANK() OVER (ORDER BY n_orders DESC) AS rnk
    FROM order_counts
)
SELECT customer_id, first_name, n_orders, rnk
FROM ranked
WHERE rnk <= 4
ORDER BY rnk, customer_id;
```

| customer_id | first_name | n_orders | rnk |
|---|---|---|---|
| 18 | Rosa | 9 | 1 |
| 29 | Cora | 9 | 1 |
| 30 | Derek | 9 | 1 |
| 13 | Mia | 8 | 4 |
| 39 | Nora | 8 | 4 |

**Note:** 5 rows, because Mia and Nora tie at 8 orders and **both** get rank 4. `ROW_NUMBER() <= 4` would return exactly 4 rows and drop Nora only because of the tie-breaker.

---

**Q6. Rank the cities.** *Expected: 10 rows; the last `city_rank` is 5.*

```sql
WITH city_counts AS (
    SELECT city, COUNT(*) AS n_customers
    FROM customers
    GROUP BY city
)
SELECT city, n_customers,
       DENSE_RANK() OVER (ORDER BY n_customers DESC) AS city_rank
FROM city_counts
ORDER BY city_rank, city;
```

| city | n_customers | city_rank |
|---|---|---|
| Boston | 9 | 1 |
| Denver | 6 | 2 |
| Portland | 6 | 2 |
| Austin | 4 | 3 |
| San Jose | 4 | 3 |
| New York | 3 | 4 |
| San Francisco | 3 | 4 |
| Seattle | 3 | 4 |
| Chicago | 1 | 5 |
| Miami | 1 | 5 |

---

**Q7. The 3rd-highest value.** *Expected: 2 rows.*

```sql
WITH city_counts AS (
    SELECT city, COUNT(*) AS n_customers
    FROM customers
    GROUP BY city
),
ranked AS (
    SELECT city, n_customers,
           DENSE_RANK() OVER (ORDER BY n_customers DESC) AS city_rank
    FROM city_counts
)
SELECT city, n_customers
FROM ranked
WHERE city_rank = 3
ORDER BY city;
```

| city | n_customers |
|---|---|
| Austin | 4 |
| San Jose | 4 |

With `RANK` instead (`= 3`): **0 rows**.

**Note:** Austin and San Jose (4 customers each). With `RANK`, the ranks are 1, 2, 2, **4**, … — no city has rank 3, so the query returns **0 rows**. For "Nth-highest value" questions, use `DENSE_RANK`.

---

## Part 3: Ranking Results and Patterns (9 points)

**Q8. Rank a `GROUP BY` result.** *Expected: 8 rows.*

```sql
WITH category_revenue AS (
    SELECT c.category_name,
           ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
    FROM order_items AS oi
    JOIN products   AS p ON p.product_id  = oi.product_id
    JOIN categories AS c ON c.category_id = p.category_id
    GROUP BY c.category_name
)
SELECT category_name, revenue,
       DENSE_RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM category_revenue
ORDER BY revenue_rank, category_name;
```

| category_name | revenue | revenue_rank |
|---|---|---|
| Electronics | 40431.29 | 1 |
| Toys | 22141.36 | 2 |
| Sports | 16237.24 | 3 |
| Books | 15754.27 | 4 |
| Food & Grocery | 15125.25 | 5 |
| Home & Kitchen | 14595.29 | 6 |
| Clothing | 13978.58 | 7 |
| Beauty | 13679.98 | 8 |

---

**Q9. Each customer's first order.** *Expected: 40 rows.*

```sql
SELECT customer_id, order_id, order_date
FROM (
    SELECT customer_id, order_id, order_date,
           ROW_NUMBER() OVER (PARTITION BY customer_id
                              ORDER BY order_date, order_id) AS rn
    FROM orders
) AS ranked
WHERE rn = 1
ORDER BY order_date, customer_id;
```

| customer_id | order_id | order_date |
|---|---|---|
| 28 | 70 | 2024-01-01 |
| 5 | 32 | 2024-01-05 |
| 34 | 37 | 2024-01-05 |
| 7 | 164 | 2024-01-07 |
| 20 | 161 | 2024-01-08 |
| 35 | 14 | 2024-01-08 |
| 13 | 123 | 2024-01-11 |
| 27 | 55 | 2024-01-13 |
| 22 | 144 | 2024-01-15 |
| 36 | 198 | 2024-01-19 |
| … 30 more rows |  |  |

---

**Q10. 🐞 Debug it.** *Expected: 10 rows.*

```sql
WITH product_ratings AS (
    SELECT p.product_name,
           ROUND(AVG(r.rating), 2) AS avg_rating
    FROM products AS p
    JOIN reviews AS r ON r.product_id = p.product_id
    GROUP BY p.product_name
),
ranked AS (
    SELECT product_name, avg_rating,
           DENSE_RANK() OVER (ORDER BY avg_rating DESC) AS rating_rank
    FROM product_ratings
)
SELECT product_name, avg_rating
FROM ranked
WHERE rating_rank = 1
ORDER BY product_name;
```

| product_name | avg_rating |
|---|---|
| Cycling Helmet | 5.00 |
| Data Science Handbook | 5.00 |
| Desk Lamp | 5.00 |
| Dumbbells Set | 5.00 |
| Jump Rope | 5.00 |
| Mechanical Keyboard | 5.00 |
| Shower Curtain | 5.00 |
| Tablet Air | 5.00 |
| Tennis Racket | 5.00 |
| USB-C Hub | 5.00 |

**Note:** `WHERE` is applied **before** window functions are computed, so `rating_rank` does not exist yet. Fix: put the `DENSE_RANK` in a second CTE (or a subquery) and filter outside it. 10 products tie at an average of 5.00.

---

## Grading

- 3 points per question: 2 for a correct result, 1 for using the right
  ranking function (and `PARTITION BY` / a subquery or CTE where needed)
- The short written answers in Q5, Q7, and Q10 are part of their second point


---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
