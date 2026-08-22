# Lab 10: Comprehensive Review — INSTRUCTOR SOLUTIONS

## OMIS 105 — Database Management Systems
**Week 10 | Answer Key**

---

## Part 1: Conceptual Questions (20 points, 4 each)

**Q1.** A primary key uniquely identifies each row in a table (e.g., `products.product_id`). A foreign key is a column that references another table's primary key (e.g., `orders.customer_id` references `customers.customer_id`). The FK creates a link between related tables and enforces referential integrity.

**Q2.** WHERE filters individual rows before grouping; HAVING filters groups after aggregation. Use WHERE for row-level conditions (e.g., `WHERE price > 50`), use HAVING for aggregate conditions (e.g., `HAVING COUNT(*) > 5`).

**Q3.** A transitive dependency occurs when a non-key column determines another non-key column: `product_id → category_id → category_name`. Fix by extracting the transitive dependency into a separate table: create a `categories` table with `(category_id, category_name)` and keep only `category_id` in `products`.

**Q4.** INNER JOIN returns only matching rows from both tables; LEFT JOIN returns all rows from the left table plus matches from the right (NULLs for non-matches). Use LEFT JOIN when you need all records from one table regardless of matches — e.g., "show all customers, including those with no orders."

**Q5.** Atomicity means a transaction is all-or-nothing — either all operations succeed or none do. For e-commerce, this ensures that when a customer places an order, the order record, line items, and stock updates all happen together. If any step fails (e.g., item out of stock), everything rolls back.

---

## Part 2: Schema Design (15 points)

**Q6.** (15 pts)

FDs:
```
movie_id → title, genre, duration, rating
screen_id → theater_id, capacity
theater_id → theater_name, location
showtime_id → movie_id, screen_id, show_date, show_time, ticket_price
ticket_id → showtime_id, customer_id, seat_number, price
customer_id → customer_name, email, phone
```

```sql
CREATE TABLE theaters (
    theater_id INTEGER PRIMARY KEY,
    theater_name VARCHAR NOT NULL,
    location VARCHAR
);

CREATE TABLE screens (
    screen_id INTEGER PRIMARY KEY,
    theater_id INTEGER REFERENCES theaters(theater_id),
    screen_name VARCHAR,
    capacity INTEGER CHECK (capacity > 0)
);

CREATE TABLE movies (
    movie_id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    genre VARCHAR,
    duration_min INTEGER CHECK (duration_min > 0),
    rating VARCHAR CHECK (rating IN ('G','PG','PG-13','R'))
);

CREATE TABLE showtimes (
    showtime_id INTEGER PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(movie_id),
    screen_id INTEGER REFERENCES screens(screen_id),
    show_date DATE NOT NULL,
    show_time TIME NOT NULL,
    ticket_price DECIMAL(6,2) CHECK (ticket_price > 0)
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE,
    phone VARCHAR
);

CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    showtime_id INTEGER REFERENCES showtimes(showtime_id),
    customer_id INTEGER REFERENCES customers(customer_id),
    seat_number VARCHAR NOT NULL,
    price DECIMAL(6,2),
    UNIQUE (showtime_id, seat_number)
);
```

Relationships: theaters→screens (1:M), movies→showtimes (1:M), screens→showtimes (1:M), customers→tickets (1:M), showtimes→tickets (1:M). Movies↔Customers is M:M through showtimes+tickets.

---

## Part 3: SQL Queries (30 points, 5 each)

**Q7.**
```sql
SELECT c.first_name || ' ' || c.last_name AS full_name,
       COUNT(DISTINCT o.order_id) AS num_orders,
       ROUND(SUM(o.total_amount), 2) AS total_spent,
       ROUND(AVG(o.total_amount), 2) AS avg_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status != 'cancelled'
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 3;
```

**Q8.**
```sql
WITH review_counts AS (
    SELECT p.product_id, p.product_name, p.category_id,
           COUNT(r.review_id) AS review_count,
           ROW_NUMBER() OVER (PARTITION BY p.category_id ORDER BY COUNT(r.review_id) DESC) AS rn
    FROM products p
    LEFT JOIN reviews r ON p.product_id = r.product_id
    GROUP BY p.product_id, p.product_name, p.category_id
)
SELECT cat.category_name, rc.product_name, rc.review_count
FROM review_counts rc
JOIN categories cat ON rc.category_id = cat.category_id
WHERE rc.rn = 1
ORDER BY rc.review_count DESC;
```

**Q9.**
```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date) AS month,
           ROUND(SUM(total_amount), 2) AS revenue
    FROM orders
    WHERE status != 'cancelled'
      AND EXTRACT(YEAR FROM order_date) = 2024
    GROUP BY month
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
       ROUND((revenue / LAG(revenue) OVER (ORDER BY month) - 1) * 100, 1) AS growth_pct
FROM monthly
ORDER BY month;
```

**Q10.**
```sql
SELECT c.first_name || ' ' || c.last_name AS name,
       COUNT(DISTINCT p.category_id) AS distinct_categories
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(DISTINCT p.category_id) >= 4
ORDER BY distinct_categories DESC;
```

**Q11.**
```sql
WITH supplier_data AS (
    SELECT s.supplier_name,
           COUNT(DISTINCT ps.product_id) AS num_products,
           ROUND(AVG(ps.cost_price), 2) AS avg_cost,
           ROUND(AVG(p.price - ps.cost_price), 2) AS avg_margin
    FROM suppliers s
    JOIN product_suppliers ps ON s.supplier_id = ps.supplier_id
    JOIN products p ON ps.product_id = p.product_id
    GROUP BY s.supplier_id, s.supplier_name
)
SELECT * FROM supplier_data ORDER BY avg_margin DESC;
```

**Q12.**
```sql
SELECT sh.carrier,
       COUNT(*) AS deliveries,
       ROUND(AVG(DATEDIFF('day', o.order_date, sh.delivery_date::DATE)), 1) AS avg_days,
       MIN(DATEDIFF('day', o.order_date, sh.delivery_date::DATE)) AS fastest,
       MAX(DATEDIFF('day', o.order_date, sh.delivery_date::DATE)) AS slowest,
       RANK() OVER (ORDER BY AVG(DATEDIFF('day', o.order_date, sh.delivery_date::DATE))) AS speed_rank
FROM shipping sh
JOIN orders o ON sh.order_id = o.order_id
WHERE o.status = 'completed'
  AND sh.delivery_date IS NOT NULL
  AND sh.delivery_date != ''
GROUP BY sh.carrier
ORDER BY avg_days;
```

---

## Part 4: Normalization (15 points)

**Q13.**

a) FDs:
```
employee_id → employee_name, department
department → dept_manager
course_id → course_title, instructor_name
instructor_name → instructor_email
(employee_id, course_id) → completion_date, score, certificate_id
```

b) Candidate key: (employee_id, course_id)

c) 1NF: Yes (atomic values, has a key). 2NF: No — partial deps: employee_id → employee_name, department; course_id → course_title, instructor_name. 3NF: No — transitive deps: department → dept_manager; instructor_name → instructor_email.

d) 3NF decomposition:
```sql
CREATE TABLE departments (department VARCHAR PRIMARY KEY, dept_manager VARCHAR);
CREATE TABLE employees (employee_id INTEGER PRIMARY KEY, employee_name VARCHAR, department VARCHAR REFERENCES departments);
CREATE TABLE instructors (instructor_name VARCHAR PRIMARY KEY, instructor_email VARCHAR);
CREATE TABLE courses (course_id INTEGER PRIMARY KEY, course_title VARCHAR, instructor_name VARCHAR REFERENCES instructors);
CREATE TABLE training_completions (
    employee_id INTEGER REFERENCES employees, course_id INTEGER REFERENCES courses,
    completion_date DATE, score INTEGER, certificate_id VARCHAR UNIQUE,
    PRIMARY KEY (employee_id, course_id)
);
```

---

## Part 5: Transaction Design (10 points)

**Q14.**
```python
def process_return(con, order_id):
    try:
        con.execute("BEGIN")
        row = con.sql(f"SELECT status, total_amount FROM orders WHERE order_id={order_id}").fetchone()
        if not row: raise Exception(f"Order {order_id} not found")
        if row[0] != 'completed': raise Exception(f"Order status is '{row[0]}', expected 'completed'")

        con.execute(f"UPDATE orders SET status='cancelled' WHERE order_id={order_id}")

        items = con.sql(f"SELECT product_id, quantity FROM order_items WHERE order_id={order_id}").fetchall()
        for pid, qty in items:
            con.execute(f"UPDATE products SET stock_quantity=stock_quantity+{qty} WHERE product_id={pid}")

        con.execute("COMMIT")
        print(f"Order {order_id} returned. Refund: ${row[1]}")
    except Exception as e:
        con.execute("ROLLBACK")
        print(f"Return failed: {e}")

# Test valid
process_return(con, 1)
# Test invalid
process_return(con, 99999)
```

---

## Part 6: Performance & Design (10 points)

**Q15.**

a) Indexes:
- `CREATE INDEX idx_orders_cust_date ON orders(customer_id, order_date)` — composite covers both filters in Query A
- `CREATE INDEX idx_products_cat_price ON products(category_id, price)` — composite covers Query B
- `CREATE INDEX idx_reviews_prod_date ON reviews(product_id, review_date DESC)` — covers Query C filter + sort

b) A view could wrap Query C (recent reviews per product) since it's a common UI pattern. Queries A and B are simple enough not to need views.

c) If category_id has very low cardinality (only 8 values), an index on category_id alone in Query B may not help — the optimizer may choose a full scan since each value matches ~12% of rows. The composite index with price helps because it narrows the result set further.

---

## Grading Rubric

| Part | Points |
|------|--------|
| Part 1: Conceptual | 20 |
| Part 2: Schema Design | 15 |
| Part 3: SQL Queries | 30 |
| Part 4: Normalization | 15 |
| Part 5: Transaction | 10 |
| Part 6: Performance | 10 |
| **Total** | **100** |

