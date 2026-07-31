
# FreshCart Analytics – Data Story, Schema, Sample Data, and Queries

## Data Story (Business Requirement)

FreshCart is a mid-sized **omnichannel grocer** operating in the USA, Canada, India, and Germany. Customers shop both online and in-store,
and frequently mix **weekly staples** (milk, bread, eggs) with **impulse items** (snacks, specialty beverages). Leadership wants to
understand **which products drive repeat purchases**, how **seasonality** changes basket composition, and which **customer segments**
respond best to promotions. Marketing runs country-specific campaigns, while the pricing team experiments with price points by category.
The core KPIs are revenue, average order value (AOV), units per order (UPO), and customer lifetime value (LTV) — with a special focus on
identifying **high-value customers** and **fast-moving products**.

To enable these insights, FreshCart will maintain a lean analytical schema with **Customers**, **Products**, and **Orders**.
Each order is a single line-item (to keep the model compact), capturing the **product purchased, quantity, price at time of purchase,
and channel** (“online” or “store”). The team needs simple, accurate answers to questions like: *Which products are trending by month?*
*Which countries have the highest AOV?* *Who are our top 10 customers this quarter?* As the business grows, we can extend to multi-line
orders, inventory, and promotions; but for phase one, these three tables are enough to power the first set of dashboards.

---

## MySQL Schema
```sql

CREATE DATABASE IF NOT EXISTS freshcart;
USE freshcart;

CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  full_name   VARCHAR(80) NOT NULL,
  email       VARCHAR(120) UNIQUE NOT NULL,
  country     VARCHAR(30) NOT NULL,
  join_date   DATE NOT NULL,
  loyalty_tier ENUM('NONE','SILVER','GOLD','PLATINUM') DEFAULT 'NONE'
);

CREATE TABLE products (
  product_id  INT PRIMARY KEY,
  product_name VARCHAR(80) NOT NULL,
  category     VARCHAR(40) NOT NULL,
  base_price   DECIMAL(8,2) NOT NULL
);

CREATE TABLE orders (
  order_id    INT PRIMARY KEY,
  customer_id INT NOT NULL,
  product_id  INT NOT NULL,
  order_date  DATE NOT NULL,
  channel     ENUM('online','store') NOT NULL,
  quantity    INT NOT NULL CHECK (quantity > 0),
  price_each  DECIMAL(8,2) NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (product_id)  REFERENCES products(product_id)
);

```

## Sample Data (INSERTS)
```sql
INSERT INTO customers(customer_id, full_name, email, country, join_date, loyalty_tier) VALUES
(1, 'Emma Smith', 'emma.smith1@example.com', 'INDIA', '2024-09-07', 'NONE'),
(2, 'Emma Weber', 'emma.weber2@example.com', 'USA', '2025-03-08', 'NONE'),
(3, 'Liam Davis', 'liam.davis3@example.com', 'CANADA', '2025-06-01', 'SILVER'),
(4, 'Raj Davis', 'raj.davis4@example.com', 'GERMANY', '2024-08-13', 'NONE'),
(5, 'Isabella Smith', 'isabella.smith5@example.com', 'CANADA', '2025-03-08', 'NONE'),
(6, 'Olivia Davis', 'olivia.davis6@example.com', 'INDIA', '2024-04-14', 'NONE'),
(7, 'Emma Sharma', 'emma.sharma7@example.com', 'INDIA', '2024-09-27', 'GOLD'),
(8, 'Lea Weber', 'lea.weber8@example.com', 'USA', '2025-01-22', 'NONE'),
(9, 'Lucas Becker', 'lucas.becker9@example.com', 'INDIA', '2024-07-15', 'SILVER'),
(10, 'Noah Wilson', 'noah.wilson10@example.com', 'INDIA', '2024-03-22', 'GOLD'),
(11, 'Emma Patel', 'emma.patel11@example.com', 'INDIA', '2025-04-09', 'SILVER'),
(12, 'Arjun Miller', 'arjun.miller12@example.com', 'INDIA', '2024-12-29', 'NONE');
```
```sql
INSERT INTO products(product_id, product_name, category, base_price) VALUES
(1, 'Whole Milk 1L', 'Dairy', 3.49),
(2, 'Free-Range Eggs (12)', 'Dairy', 4.99),
(3, 'Sourdough Bread', 'Bakery', 3.99),
(4, 'Almond Butter 340g', 'Pantry', 8.99),
(5, 'Organic Bananas (1kg)', 'Produce', 1.99),
(6, 'Greek Yogurt 500g', 'Dairy', 5.49),
(7, 'Cold Brew Coffee 1L', 'Beverages', 6.49),
(8, 'Sparkling Water 1L', 'Beverages', 1.29),
(9, 'Trail Mix 300g', 'Snacks', 4.49),
(10, 'Dark Chocolate 85% 100g', 'Snacks', 2.99);
```
```sql
INSERT INTO orders(order_id, customer_id, product_id, order_date, channel, quantity, price_each) VALUES
(1, 5, 2, '2025-06-30', 'online', 2, 5.12),
(2, 3, 8, '2025-10-17', 'online', 2, 1.23),
(3, 11, 6, '2024-02-02', 'store', 1, 5.19),
(4, 7, 5, '2025-08-03', 'store', 1, 1.87),
(5, 4, 8, '2025-10-20', 'store', 2, 1.39),
(6, 3, 5, '2025-07-28', 'store', 1, 1.89),
(7, 12, 10, '2025-02-12', 'store', 2, 3.23),
(8, 4, 3, '2024-02-18', 'online', 2, 3.98),
(9, 3, 3, '2024-03-06', 'store', 3, 3.93),
(10, 7, 10, '2025-07-20', 'online', 2, 3.01),
(11, 11, 2, '2024-09-30', 'store', 3, 5.37),
(12, 2, 5, '2024-01-04', 'store', 2, 1.85),
(13, 9, 3, '2025-10-02', 'store', 2, 4.32),
(14, 11, 9, '2025-01-17', 'online', 2, 4.22),
(15, 9, 9, '2025-05-15', 'online', 1, 4.58),
(16, 2, 6, '2024-09-03', 'online', 1, 5.20),
(17, 2, 8, '2025-06-29', 'online', 1, 1.41),
(18, 3, 8, '2025-06-24', 'store', 2, 1.20),
(19, 4, 9, '2025-12-31', 'store', 3, 4.66),
(20, 7, 6, '2025-04-07', 'online', 2, 5.93),
(21, 4, 4, '2025-08-25', 'online', 1, 8.70),
(22, 10, 4, '2025-10-08', 'online', 1, 8.22),
(23, 4, 2, '2024-03-13', 'online', 1, 5.35),
(24, 5, 8, '2025-08-07', 'store', 1, 1.30),
(25, 4, 8, '2024-04-09', 'store', 2, 1.21);
```

---

# Query Library (60)
## Basic Queries (20)

**1. List all customers**

```sql
SELECT * FROM customers;
```

**2. List all products**

```sql
SELECT * FROM products;
```

**3. List the first 5 orders**

```sql
SELECT * FROM orders ORDER BY order_id LIMIT 5;
```

**4. Show customer names and countries**

```sql
SELECT full_name, country FROM customers;
```

**5. Show product names and categories**

```sql
SELECT product_name, category FROM products;
```

**6. Find all customers in USA**

```sql
SELECT * FROM customers WHERE country='USA';
```

**7. Find products in the Snacks category**

```sql
SELECT * FROM products WHERE category='Snacks';
```

**8. Find orders placed in 2025**

```sql
SELECT * FROM orders WHERE YEAR(order_date)=2025;
```

**9. Sort products by base_price descending**

```sql
SELECT * FROM products ORDER BY base_price DESC;
```

**10. Show distinct countries we operate in**

```sql
SELECT DISTINCT country FROM customers;
```

**11. Find customers who joined in 2024**

```sql
SELECT * FROM customers WHERE YEAR(join_date)=2024;
```

**12. Find orders from the online channel**

```sql
SELECT * FROM orders WHERE channel='online';
```

**13. Return top 10 most recent orders**

```sql
SELECT * FROM orders ORDER BY order_date DESC LIMIT 10;
```

**14. Find products priced below $3.00**

```sql
SELECT * FROM products WHERE base_price < 3.00;
```

**15. Find orders with quantity greater than 1**

```sql
SELECT * FROM orders WHERE quantity > 1;
```

**16. Show customer emails with alias**

```sql
SELECT full_name, email AS contact FROM customers;
```

**17. Show product id, name, and rounded base price**

```sql
SELECT product_id, product_name, ROUND(base_price,2) AS price FROM products;
```

**18. Count how many products are in Beverages**

```sql
SELECT COUNT(*) FROM products WHERE category='Beverages';
```

**19. Find orders for product_id = 1**

```sql
SELECT * FROM orders WHERE product_id=1;
```

**20. Show orders sorted by customer then date**

```sql
SELECT * FROM orders ORDER BY customer_id, order_date;
```

## Basic-to-Intermediate Queries (20)

**1. Join orders to product names**

```sql
SELECT o.order_id, o.order_date, p.product_name, o.quantity, o.price_each
FROM orders o
JOIN products p ON p.product_id=o.product_id;
```

**2. Join orders to customers (who bought what)**

```sql
SELECT o.order_id, c.full_name, p.product_name, o.quantity, o.order_date
FROM orders o
JOIN customers c ON c.customer_id=o.customer_id
JOIN products  p ON p.product_id=o.product_id;
```

**3. Compute revenue per order (quantity * price_each)**

```sql
SELECT order_id, quantity*price_each AS revenue FROM orders;
```

**4. Total revenue overall**

```sql
SELECT SUM(quantity*price_each) AS total_revenue FROM orders;
```

**5. Average order value (AOV) overall**

```sql
SELECT AVG(quantity*price_each) AS aov FROM orders;
```

**6. Units per order (UPO) overall**

```sql
SELECT AVG(quantity) AS units_per_order FROM orders;
```

**7. Revenue by channel**

```sql
SELECT channel, SUM(quantity*price_each) AS revenue FROM orders GROUP BY channel;
```

**8. Revenue by country**

```sql
SELECT c.country, SUM(o.quantity*o.price_each) AS revenue
FROM orders o
JOIN customers c ON c.customer_id=o.customer_id
GROUP BY c.country;
```

**9. Revenue by product category**

```sql
SELECT p.category, SUM(o.quantity*o.price_each) AS revenue
FROM orders o
JOIN products p ON p.product_id=o.product_id
GROUP BY p.category;
```

**10. Top 5 products by revenue**

```sql
SELECT p.product_name, SUM(o.quantity*o.price_each) AS revenue
FROM orders o JOIN products p ON p.product_id=o.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 5;
```

**11. Monthly revenue (YYYY-MM)**

```sql
SELECT DATE_FORMAT(order_date,'%Y-%m') AS ym, SUM(quantity*price_each) AS revenue FROM orders GROUP BY ym ORDER BY ym;
```

**12. Customer order counts**

```sql
SELECT customer_id, COUNT(*) AS orders_count FROM orders GROUP BY customer_id ORDER BY orders_count DESC;
```

**13. Customers with more than 2 orders**

```sql
SELECT customer_id, COUNT(*) AS cnt FROM orders GROUP BY customer_id HAVING COUNT(*)>2;
```

**14. Average price_paid vs base_price per product**

```sql
SELECT p.product_id, p.product_name,
        ROUND(AVG(o.price_each),2) AS avg_paid, p.base_price
FROM products p
LEFT JOIN orders o ON o.product_id=p.product_id
GROUP BY p.product_id, p.product_name, p.base_price;
```

**15. Orders per loyalty tier**

```sql
SELECT c.loyalty_tier, COUNT(*) AS orders_cnt
FROM orders o JOIN customers c ON c.customer_id=o.customer_id
GROUP BY c.loyalty_tier
ORDER BY orders_cnt DESC;
```

**16. Average order value per country**

```sql
SELECT c.country, ROUND(AVG(o.quantity*o.price_each),2) AS aov
FROM orders o JOIN customers c ON c.customer_id=o.customer_id
GROUP BY c.country;
```

**17. Customers who never ordered (if any)**

```sql
SELECT c.*
FROM customers c
LEFT JOIN orders o ON o.customer_id=c.customer_id
WHERE o.order_id IS NULL;
```

**18. Products never purchased (if any)**

```sql
SELECT p.*
FROM products p
LEFT JOIN orders o ON o.product_id=p.product_id
WHERE o.order_id IS NULL;
```

**19. Top customers by revenue (top 5)**

```sql
SELECT c.customer_id, c.full_name, SUM(o.quantity*o.price_each) AS revenue
FROM orders o JOIN customers c ON c.customer_id=o.customer_id
GROUP BY c.customer_id, c.full_name
ORDER BY revenue DESC
LIMIT 5;
```

## Intermediate Queries (20)

**1. CTE: rank customers by revenue**

```sql
WITH cust_rev AS (
  SELECT c.customer_id, c.full_name, SUM(o.quantity*o.price_each) AS revenue
  FROM orders o JOIN customers c ON c.customer_id=o.customer_id
  GROUP BY c.customer_id, c.full_name
)
SELECT *, RANK() OVER(ORDER BY revenue DESC) AS rnk
FROM cust_rev;
```

**2. CTE: Top 3 products by revenue within category**

```sql
WITH prod_rev AS (
  SELECT p.category, p.product_id, p.product_name, SUM(o.quantity*o.price_each) AS revenue
  FROM orders o JOIN products p ON p.product_id=o.product_id
  GROUP BY p.category, p.product_id, p.product_name
), ranked AS (
  SELECT *, ROW_NUMBER() OVER(PARTITION BY category ORDER BY revenue DESC) AS rn
  FROM prod_rev
)
SELECT * FROM ranked WHERE rn<=3;
```

**3. Window: running monthly revenue**

```sql
SELECT DATE_FORMAT(order_date,'%Y-%m') AS ym,
        SUM(quantity*price_each) AS revenue,
        SUM(SUM(quantity*price_each)) OVER(ORDER BY DATE_FORMAT(order_date,'%Y-%m')) AS running_rev
FROM orders
GROUP BY ym
ORDER BY ym;
```

**4. Window: z-score of price paid per product**

```sql
SELECT product_id, price_each,
        (price_each - AVG(price_each) OVER(PARTITION BY product_id))
        / NULLIF(STDDEV_POP(price_each) OVER(PARTITION BY product_id),0) AS z
FROM orders;
```

**5. Percentile: p90 order value overall**

```sql
SELECT PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY quantity*price_each) AS p90_order_value FROM orders;
```

**6. Find the most recent order per customer (ROW_NUMBER)**

```sql
WITH r AS (
  SELECT o.*, ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) rn
  FROM orders o
)
SELECT * FROM r WHERE rn=1;
```

**7. Customers whose AOV is above overall average**

```sql
WITH per_cust AS (
  SELECT customer_id, AVG(quantity*price_each) AS aov
  FROM orders GROUP BY customer_id
), overall AS (
  SELECT AVG(quantity*price_each) AS global_aov FROM orders
)
SELECT c.customer_id, c.full_name, p.aov
FROM per_cust p
JOIN customers c ON c.customer_id=p.customer_id, overall
WHERE p.aov > overall.global_aov;
```

**8. Month-over-month revenue growth (%)**

```sql
WITH m AS (
  SELECT DATE_FORMAT(order_date,'%Y-%m') ym, SUM(quantity*price_each) rev
  FROM orders GROUP BY ym
),
g AS (
  SELECT ym, rev,
         LAG(rev) OVER(ORDER BY ym) AS prev_rev
  FROM m
)
SELECT ym, rev,
       ROUND(100.0*(rev - prev_rev)/NULLIF(prev_rev,0),2) AS mom_pct
FROM g;
```

**9. Country share of total revenue**

```sql
WITH rev AS (
  SELECT c.country, SUM(o.quantity*o.price_each) AS revenue
  FROM orders o JOIN customers c ON c.customer_id=o.customer_id
  GROUP BY c.country
), tot AS (
  SELECT SUM(revenue) AS total_rev FROM rev
)
SELECT r.country, r.revenue,
       ROUND(100.0*r.revenue/t.total_rev,2) AS pct_share
FROM rev r CROSS JOIN tot t
ORDER BY pct_share DESC;
```

**10. Customers who bought from both channels**

```sql
WITH ch AS (
  SELECT customer_id, COUNT(DISTINCT channel) ch_ct
  FROM orders
  GROUP BY customer_id
)
SELECT c.customer_id, c.full_name
FROM ch JOIN customers c ON c.customer_id=ch.customer_id
WHERE ch_ct=2;
```

**11. Category with highest average price paid**

```sql
SELECT p.category, AVG(o.price_each) AS avg_paid
FROM orders o JOIN products p ON p.product_id=o.product_id
GROUP BY p.category
ORDER BY avg_paid DESC
LIMIT 1;
```

**12. Products whose avg paid price > base price**

```sql
SELECT p.product_id, p.product_name
FROM products p
JOIN (SELECT product_id, AVG(price_each) avg_paid FROM orders GROUP BY product_id) x
  ON x.product_id=p.product_id
WHERE x.avg_paid > p.base_price;
```

**13. Customers who only shop online**

```sql
SELECT c.*
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id=c.customer_id AND o.channel='store'
) AND EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id=c.customer_id AND o.channel='online'
);
```

**14. Best-selling product per country (by units)**

```sql
WITH by_cty AS (
  SELECT c.country, p.product_id, SUM(o.quantity) units
  FROM orders o JOIN customers c ON c.customer_id=o.customer_id
                JOIN products  p ON p.product_id=o.product_id
  GROUP BY c.country, p.product_id
), ranked AS (
  SELECT *, ROW_NUMBER() OVER(PARTITION BY country ORDER BY units DESC) rn
  FROM by_cty
)
SELECT r.country, r.product_id, r.units
FROM ranked r WHERE rn=1;
```

**15. Customers with no orders in 2025 (but had orders before)**

```sql
WITH hist AS (
  SELECT customer_id, MIN(order_date) first_dt, MAX(order_date) last_dt
  FROM orders GROUP BY customer_id
)
SELECT c.customer_id, c.full_name, h.last_dt
FROM hist h JOIN customers c ON c.customer_id=h.customer_id
WHERE YEAR(h.last_dt)<2025;
```

**16. Median price paid per product (PERCENTILE_CONT)**

```sql
SELECT product_id, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price_each) AS median_paid FROM orders GROUP BY product_id;
```

**17. Top 3 customers per country by revenue**

```sql
WITH cr AS (
  SELECT c.country, c.customer_id, SUM(o.quantity*o.price_each) rev
  FROM orders o JOIN customers c ON c.customer_id=o.customer_id
  GROUP BY c.country, c.customer_id
), rnk AS (
  SELECT *, ROW_NUMBER() OVER(PARTITION BY country ORDER BY rev DESC) rn
  FROM cr
)
SELECT * FROM rnk WHERE rn<=3;
```

**18. Product/category mix per channel (units)**

```sql
SELECT channel, p.category, SUM(o.quantity) units
FROM orders o JOIN products p ON p.product_id=o.product_id
GROUP BY channel, p.category
ORDER BY channel, units DESC;
```

**19. Days with zero orders in Jan 2025 (calendar CTE)**

```sql
WITH RECURSIVE d AS (
  SELECT DATE('2025-01-01') AS dt
  UNION ALL
  SELECT dt + INTERVAL 1 DAY FROM d WHERE dt < '2025-01-31'
)
SELECT d.dt
FROM d
LEFT JOIN orders o ON o.order_date=d.dt
WHERE o.order_id IS NULL;
```
