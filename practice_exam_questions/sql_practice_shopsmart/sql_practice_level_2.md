# ShopSmart SQL Practice — Level 2 (Weeks 9-10)

	Views, multi-table business reports,
	sub-queries and set operations, window
	functions, and final-review style
	analytics — on the ShopSmart database.

	All queries and results in this file were
	validated with DuckDB v1.5.5.


## 1. Setup

Build the database first (see [`README.md`](./README.md)):

```bash
duckdb shopsmart.duckdb < create_shopsmart_db.sql
duckdb shopsmart.duckdb
```

Tables: `categories`, `customers`, `suppliers`, `products`, `orders`,
`order_items`, `product_suppliers`, `reviews`, `shipping`
(the full schema is in [`create_shopsmart_db.sql`](./create_shopsmart_db.sql)).


## 2. Definitions Used in This File

* **Revenue** = `SUM(quantity * unit_price)` from `order_items`, counting only
  orders whose `status` is **not** `'cancelled'`.
* `orders.total_amount` is a separate field stored on each order. In this
  dataset it does **not** equal the sum of the order's line items (see Q43),
  so questions say which one they use.
* The last order in the data is on **2025-02-04**; questions about "days
  since" measure from that date (instead of `CURRENT_DATE`) so the answers
  never change.
* Q1 and Q3 create the views `order_summary` and `product_catalog`, which
  later questions use — run the questions in order.
* Long outputs are truncated to 10 rows by the DuckDB CLI (`.maxrows 10`);
  the total row count is shown at the bottom of each result.


## 3. SQL Practice Queries


## Part A — Views (Week 9)


### Q1. Create a view `order_summary` with one row per order

The view joins `orders`, `customers`, and `order_items`. A view stores the
**query**, not the data, so it always reflects the current tables.

```sql
CREATE OR REPLACE VIEW order_summary AS
SELECT o.order_id,
       o.customer_id,
       c.first_name || ' ' || c.last_name   AS customer_name,
       c.state,
       o.order_date,
       o.status,
       COUNT(oi.item_id)                    AS num_items,
       SUM(oi.quantity)                     AS units,
       SUM(oi.quantity * oi.unit_price)     AS items_total,
       o.total_amount
FROM orders o
JOIN customers   c  ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
GROUP BY o.order_id, o.customer_id, c.first_name, c.last_name, c.state,
         o.order_date, o.status, o.total_amount;

SELECT *
FROM order_summary
ORDER BY order_id
LIMIT 5;
```

**Result:**

```text
CREATE OR REPLACE VIEW order_summary AS
SELECT o.order_id,
       o.customer_id,
       c.first_name || ' ' || c.last_name   AS customer_name,
       c.state,
       o.order_date,
       o.status,
       COUNT(oi.item_id)                    AS num_items,
       SUM(oi.quantity)                     AS units,
       SUM(oi.quantity * oi.unit_price)     AS items_total,
       o.total_amount
FROM orders o
JOIN customers   c  ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
GROUP BY o.order_id, o.customer_id, c.first_name, c.last_name, c.state,
         o.order_date, o.status, o.total_amount;

SELECT *
FROM order_summary
ORDER BY order_id
LIMIT 5;
┌──────────┬─────────────┬───────────────┬─────────┬────────────┬────────────┬───────────┬────────┬───────────────┬───────────────┐
│ order_id │ customer_id │ customer_name │  state  │ order_date │   status   │ num_items │ units  │  items_total  │ total_amount  │
│  int32   │    int32    │    varchar    │ varchar │    date    │  varchar   │   int64   │ int128 │ decimal(38,2) │ decimal(10,2) │
├──────────┼─────────────┼───────────────┼─────────┼────────────┼────────────┼───────────┼────────┼───────────────┼───────────────┤
│        1 │           5 │ Eva Garcia    │ MA      │ 2024-12-28 │ processing │         5 │     14 │       1033.73 │         56.51 │
│        2 │           5 │ Eva Garcia    │ MA      │ 2024-01-17 │ cancelled  │         5 │      9 │        711.48 │        271.04 │
│        3 │          33 │ Gina Turner   │ CO      │ 2024-05-01 │ completed  │         5 │     13 │        998.35 │        538.49 │
│        4 │          14 │ Noah Harris   │ OR      │ 2024-10-03 │ completed  │         4 │     10 │        418.00 │        581.45 │
│        5 │          37 │ Kira Evans    │ CO      │ 2024-10-22 │ completed  │         1 │      4 │        427.04 │        201.97 │
└──────────┴─────────────┴───────────────┴─────────┴────────────┴────────────┴───────────┴────────┴───────────────┴───────────────┘
```

### Q2. Use `order_summary` to find the 5 states with the highest revenue

```sql
SELECT state,
       COUNT(*)         AS num_orders,
       SUM(items_total) AS revenue
FROM order_summary
WHERE status <> 'cancelled'
GROUP BY state
ORDER BY revenue DESC
LIMIT 5;
```

**Result:**

```text
┌─────────┬────────────┬───────────────┐
│  state  │ num_orders │    revenue    │
│ varchar │   int64    │ decimal(38,2) │
├─────────┼────────────┼───────────────┤
│ MA      │         43 │      35162.73 │
│ CA      │         28 │      24917.15 │
│ CO      │         29 │      19082.11 │
│ OR      │         25 │      15405.33 │
│ TX      │         11 │       9543.31 │
└─────────┴────────────┴───────────────┘
```

### Q3. Create a view `product_catalog` with category, supplier count, cheapest cost, and average rating

Each piece is pre-aggregated in its own sub-query, so joining them does not
multiply rows.

```sql
CREATE OR REPLACE VIEW product_catalog AS
SELECT p.product_id,
       p.product_name,
       c.category_name,
       p.price,
       p.stock_quantity,
       COALESCE(s.num_suppliers, 0) AS num_suppliers,
       s.min_cost_price,
       r.num_reviews,
       r.avg_rating
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN (SELECT product_id,
                  COUNT(*)        AS num_suppliers,
                  MIN(cost_price) AS min_cost_price
           FROM product_suppliers
           GROUP BY product_id) s ON p.product_id = s.product_id
LEFT JOIN (SELECT product_id,
                  COUNT(*)              AS num_reviews,
                  ROUND(AVG(rating), 2) AS avg_rating
           FROM reviews
           GROUP BY product_id) r ON p.product_id = r.product_id;

SELECT product_name, category_name, price, num_suppliers,
       min_cost_price, num_reviews, avg_rating
FROM product_catalog
ORDER BY product_id
LIMIT 5;
```

**Result:**

```text
CREATE OR REPLACE VIEW product_catalog AS
SELECT p.product_id,
       p.product_name,
       c.category_name,
       p.price,
       p.stock_quantity,
       COALESCE(s.num_suppliers, 0) AS num_suppliers,
       s.min_cost_price,
       r.num_reviews,
       r.avg_rating
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN (SELECT product_id,
                  COUNT(*)        AS num_suppliers,
                  MIN(cost_price) AS min_cost_price
           FROM product_suppliers
           GROUP BY product_id) s ON p.product_id = s.product_id
LEFT JOIN (SELECT product_id,
                  COUNT(*)              AS num_reviews,
                  ROUND(AVG(rating), 2) AS avg_rating
           FROM reviews
           GROUP BY product_id) r ON p.product_id = r.product_id;

SELECT product_name, category_name, price, num_suppliers,
       min_cost_price, num_reviews, avg_rating
FROM product_catalog
ORDER BY product_id
LIMIT 5;
┌──────────────────┬───────────────┬───────────────┬───────────────┬────────────────┬─────────────┬────────────┐
│   product_name   │ category_name │     price     │ num_suppliers │ min_cost_price │ num_reviews │ avg_rating │
│     varchar      │    varchar    │ decimal(10,2) │     int64     │ decimal(10,2)  │    int64    │   double   │
├──────────────────┼───────────────┼───────────────┼───────────────┼────────────────┼─────────────┼────────────┤
│ Smartphone X12   │ Electronics   │        321.52 │             2 │         159.10 │           3 │       3.67 │
│ Laptop Pro 15    │ Electronics   │        372.07 │             2 │         218.91 │           3 │       3.33 │
│ Wireless Earbuds │ Electronics   │        115.49 │             2 │          51.33 │        NULL │       NULL │
│ USB-C Hub        │ Electronics   │         55.74 │             2 │          29.40 │           1 │        5.0 │
│ Tablet Air       │ Electronics   │        446.63 │             1 │         182.82 │           2 │        5.0 │
└──────────────────┴───────────────┴───────────────┴───────────────┴────────────────┴─────────────┴────────────┘
```

### Q4. Low-stock report: products with fewer than 20 units in stock (using the view)

```sql
SELECT product_name,
       category_name,
       stock_quantity,
       num_suppliers
FROM product_catalog
WHERE stock_quantity < 20
ORDER BY stock_quantity, product_name;
```

**Result:**

```text
┌───────────────────┬───────────────┬────────────────┬───────────────┐
│   product_name    │ category_name │ stock_quantity │ num_suppliers │
│      varchar      │    varchar    │     int32      │     int64     │
├───────────────────┼───────────────┼────────────────┼───────────────┤
│ SQL Cookbook      │ Books         │              3 │             2 │
│ Smartphone X12    │ Electronics   │             12 │             2 │
│ Bluetooth Speaker │ Electronics   │             16 │             1 │
│ Stuffed Bear      │ Toys          │             16 │             1 │
└───────────────────┴───────────────┴────────────────┴───────────────┘
```

### Q5. List the views in the database and their definitions

```sql
SELECT view_name,
       LEFT(sql, 60) || '...' AS definition_start
FROM duckdb_views()
WHERE NOT internal
ORDER BY view_name;
```

**Result:**

```text
┌─────────────────┬─────────────────────────────────────────────────────────────────┐
│    view_name    │                        definition_start                         │
│     varchar     │                             varchar                             │
├─────────────────┼─────────────────────────────────────────────────────────────────┤
│ order_summary   │ CREATE VIEW order_summary AS SELECT o.order_id, o.customer_i... │
│ product_catalog │ CREATE VIEW product_catalog AS SELECT p.product_id, p.produc... │
└─────────────────┴─────────────────────────────────────────────────────────────────┘
```


## Part B — Multi-table Business Reports


### Q6. Revenue and units sold by category

```sql
SELECT c.category_name,
       SUM(oi.quantity)                 AS units_sold,
       SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN orders     o ON oi.order_id   = o.order_id
JOIN products   p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
WHERE o.status <> 'cancelled'
GROUP BY c.category_name
ORDER BY revenue DESC;
```

**Result:**

```text
┌────────────────┬────────────┬───────────────┐
│ category_name  │ units_sold │    revenue    │
│    varchar     │   int128   │ decimal(38,2) │
├────────────────┼────────────┼───────────────┤
│ Electronics    │        158 │      35556.66 │
│ Toys           │        165 │      18550.07 │
│ Books          │        150 │      13304.55 │
│ Home & Kitchen │        175 │      13018.15 │
│ Sports         │        147 │      12890.09 │
│ Clothing       │        182 │      12441.13 │
│ Food & Grocery │        185 │      12388.98 │
│ Beauty         │        160 │      12313.71 │
└────────────────┴────────────┴───────────────┘
```

### Q7. Number of orders and percentage of all orders for each status

```sql
SELECT status,
       COUNT(*) AS num_orders,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_orders
FROM orders
GROUP BY status
ORDER BY num_orders DESC;
```

**Result:**

```text
┌────────────┬────────────┬───────────────┐
│   status   │ num_orders │ pct_of_orders │
│  varchar   │   int64    │    double     │
├────────────┼────────────┼───────────────┤
│ completed  │        115 │          57.5 │
│ processing │         30 │          15.0 │
│ cancelled  │         29 │          14.5 │
│ shipped    │         26 │          13.0 │
└────────────┴────────────┴───────────────┘
```

### Q8. Monthly revenue in 2024

```sql
SELECT DATE_TRUNC('month', o.order_date)  AS month,
       COUNT(DISTINCT o.order_id)         AS num_orders,
       SUM(oi.quantity * oi.unit_price)   AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status <> 'cancelled' AND
      o.order_date >= DATE '2024-01-01' AND
      o.order_date <  DATE '2025-01-01'
GROUP BY month
ORDER BY month;
```

**Result:**

```text
┌─────────────────────┬────────────┬───────────────┐
│        month        │ num_orders │    revenue    │
│      timestamp      │   int64    │ decimal(38,2) │
├─────────────────────┼────────────┼───────────────┤
│ 2024-01-01 00:00:00 │         16 │       7030.54 │
│ 2024-02-01 00:00:00 │         13 │      11901.00 │
│ 2024-03-01 00:00:00 │         11 │       7266.20 │
│ 2024-04-01 00:00:00 │         12 │      10721.49 │
│ 2024-05-01 00:00:00 │         15 │       9271.63 │
│ 2024-06-01 00:00:00 │         19 │      18635.99 │
│ 2024-07-01 00:00:00 │         11 │      11599.31 │
│ 2024-08-01 00:00:00 │         10 │       7729.81 │
│ 2024-09-01 00:00:00 │          7 │       5209.37 │
│ 2024-10-01 00:00:00 │         19 │      11790.25 │
│ 2024-11-01 00:00:00 │         12 │       5243.49 │
│ 2024-12-01 00:00:00 │         12 │      12049.22 │
└─────────────────────┴────────────┴───────────────┘
  12 rows                                3 columns
```

### Q9. Each customer's first order, last order, and the days between them

```sql
SELECT c.customer_id,
       c.first_name || ' ' || c.last_name AS customer_name,
       MIN(o.order_date) AS first_order,
       MAX(o.order_date) AS last_order,
       DATE_DIFF('day', MIN(o.order_date), MAX(o.order_date)) AS days_between
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY days_between DESC, c.customer_id;
```

**Result:**

```text
┌─────────────┬────────────────┬─────────────┬────────────┬──────────────┐
│ customer_id │ customer_name  │ first_order │ last_order │ days_between │
│    int32    │    varchar     │    date     │    date    │    int64     │
├─────────────┼────────────────┼─────────────┼────────────┼──────────────┤
│           7 │ Grace Anderson │ 2024-01-07  │ 2025-02-02 │          392 │
│          35 │ Iris Campbell  │ 2024-01-08  │ 2025-01-31 │          389 │
│          22 │ Vic Lopez      │ 2024-01-15  │ 2025-02-04 │          386 │
│          18 │ Rosa Young     │ 2024-01-23  │ 2025-01-27 │          370 │
│           5 │ Eva Garcia     │ 2024-01-05  │ 2024-12-28 │          358 │
│           · │     ·          │     ·       │     ·      │           ·  │
│           · │     ·          │     ·       │     ·      │           ·  │
│           · │     ·          │     ·       │     ·      │           ·  │
│          10 │ Jack Wilson    │ 2024-05-16  │ 2024-10-06 │          143 │
│          40 │ Omar Stewart   │ 2024-10-18  │ 2025-01-13 │           87 │
│          21 │ Uma Wright     │ 2024-01-30  │ 2024-04-18 │           79 │
│          24 │ Xander Scott   │ 2024-02-05  │ 2024-03-26 │           50 │
│          11 │ Karen Moore    │ 2024-06-17  │ 2024-06-17 │            0 │
└─────────────┴────────────────┴─────────────┴────────────┴──────────────┘
  40 rows (10 shown)      use .last to show entire result      5 columns
```

### Q10. How many customers joined in each quarter?

```sql
SELECT YEAR(join_date)    AS join_year,
       QUARTER(join_date) AS join_quarter,
       COUNT(*)           AS new_customers
FROM customers
GROUP BY join_year, join_quarter
ORDER BY join_year, join_quarter;
```

**Result:**

```text
┌───────────┬──────────────┬───────────────┐
│ join_year │ join_quarter │ new_customers │
│   int64   │    int64     │     int64     │
├───────────┼──────────────┼───────────────┤
│      2023 │            1 │             6 │
│      2023 │            2 │             6 │
│      2023 │            3 │             6 │
│      2023 │            4 │             2 │
│      2024 │            1 │             3 │
│      2024 │            2 │             5 │
│      2024 │            3 │             8 │
│      2024 │            4 │             4 │
└───────────┴──────────────┴───────────────┘
```

### Q11. Which day of the week gets the most orders?

```sql
SELECT DAYNAME(order_date)   AS weekday,
       ISODOW(order_date)    AS day_number,
       COUNT(*)              AS num_orders
FROM orders
GROUP BY weekday, day_number
ORDER BY day_number;
```

**Result:**

```text
┌───────────┬────────────┬────────────┐
│  weekday  │ day_number │ num_orders │
│  varchar  │   int64    │   int64    │
├───────────┼────────────┼────────────┤
│ Monday    │          1 │         22 │
│ Tuesday   │          2 │         31 │
│ Wednesday │          3 │         39 │
│ Thursday  │          4 │         25 │
│ Friday    │          5 │         29 │
│ Saturday  │          6 │         24 │
│ Sunday    │          7 │         30 │
└───────────┴────────────┴────────────┘
```

### Q12. Carrier report: shipments, average and total shipping cost, and how many are still in transit

```sql
SELECT carrier,
       COUNT(*)                                     AS shipments,
       ROUND(AVG(shipping_cost), 2)                 AS avg_cost,
       SUM(shipping_cost)                           AS total_cost,
       COUNT(*) FILTER (WHERE delivery_date IS NULL) AS in_transit
FROM shipping
GROUP BY carrier
ORDER BY shipments DESC;
```

**Result:**

```text
┌─────────┬───────────┬──────────┬───────────────┬────────────┐
│ carrier │ shipments │ avg_cost │  total_cost   │ in_transit │
│ varchar │   int64   │  double  │ decimal(38,2) │   int64    │
├─────────┼───────────┼──────────┼───────────────┼────────────┤
│ USPS    │        38 │     16.3 │        619.54 │          7 │
│ DHL     │        36 │    13.46 │        484.38 │          5 │
│ FedEx   │        34 │    13.69 │        465.61 │          6 │
│ UPS     │        33 │    14.76 │        487.13 │          8 │
└─────────┴───────────┴──────────┴───────────────┴────────────┘
```

### Q13. Distribution of delivery times (days from ship date to delivery date)

```sql
SELECT DATE_DIFF('day', ship_date, delivery_date) AS days_to_deliver,
       COUNT(*)                                  AS num_shipments
FROM shipping
WHERE delivery_date IS NOT NULL
GROUP BY days_to_deliver
ORDER BY days_to_deliver;
```

**Result:**

```text
┌─────────────────┬───────────────┐
│ days_to_deliver │ num_shipments │
│      int64      │     int64     │
├─────────────────┼───────────────┤
│               2 │            20 │
│               3 │            13 │
│               4 │            23 │
│               5 │            19 │
│               6 │            15 │
│               7 │            25 │
└─────────────────┴───────────────┘
```

### Q14. Find the slowest deliveries (the maximum number of days in transit) with customer and carrier

```sql
SELECT s.order_id,
       c.first_name || ' ' || c.last_name AS customer_name,
       s.carrier,
       s.ship_date,
       s.delivery_date,
       DATE_DIFF('day', s.ship_date, s.delivery_date) AS days_to_deliver
FROM shipping s
JOIN orders    o ON s.order_id    = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE DATE_DIFF('day', s.ship_date, s.delivery_date) = (
    SELECT MAX(DATE_DIFF('day', ship_date, delivery_date))
    FROM shipping
)
ORDER BY s.carrier, s.order_id;
```

**Result:**

```text
┌──────────┬────────────────┬─────────┬────────────┬───────────────┬─────────────────┐
│ order_id │ customer_name  │ carrier │ ship_date  │ delivery_date │ days_to_deliver │
│  int32   │    varchar     │ varchar │    date    │     date      │      int64      │
├──────────┼────────────────┼─────────┼────────────┼───────────────┼─────────────────┤
│       14 │ Iris Campbell  │ DHL     │ 2024-01-10 │ 2024-01-17    │               7 │
│       32 │ Eva Garcia     │ DHL     │ 2024-01-06 │ 2024-01-13    │               7 │
│      104 │ Eva Garcia     │ DHL     │ 2024-08-02 │ 2024-08-09    │               7 │
│       20 │ Mia White      │ FedEx   │ 2024-06-01 │ 2024-06-08    │               7 │
│       60 │ Derek Mitchell │ FedEx   │ 2024-06-30 │ 2024-07-07    │               7 │
│        · │      ·         │  ·      │     ·      │     ·         │               · │
│        · │      ·         │  ·      │     ·      │     ·         │               · │
│        · │      ·         │  ·      │     ·      │     ·         │               · │
│      108 │ Alice Smith    │ USPS    │ 2024-06-30 │ 2024-07-07    │               7 │
│      148 │ Mia White      │ USPS    │ 2024-02-15 │ 2024-02-22    │               7 │
│      156 │ Mia White      │ USPS    │ 2024-06-13 │ 2024-06-20    │               7 │
│      162 │ Rosa Young     │ USPS    │ 2024-01-26 │ 2024-02-02    │               7 │
│      199 │ Quinn Hall     │ USPS    │ 2024-06-15 │ 2024-06-22    │               7 │
└──────────┴────────────────┴─────────┴────────────┴───────────────┴─────────────────┘
  25 rows (10 shown)            use .last to show entire result            6 columns
```

### Q15. Products with at least 3 reviews and an average rating below 3 (HAVING)

```sql
SELECT p.product_name,
       COUNT(*)                AS num_reviews,
       ROUND(AVG(r.rating), 2) AS avg_rating
FROM reviews r
JOIN products p ON r.product_id = p.product_id
GROUP BY p.product_name
HAVING COUNT(*) >= 3 AND AVG(r.rating) < 3
ORDER BY avg_rating, p.product_name;
```

**Result:**

```text
┌──────────────────────┬─────────────┬────────────┐
│     product_name     │ num_reviews │ avg_rating │
│       varchar        │    int64    │   double   │
├──────────────────────┼─────────────┼────────────┤
│ History of Computing │           3 │       2.67 │
└──────────────────────┴─────────────┴────────────┘
```

### Q16. Count the 1- to 5-star reviews in each category (PIVOT)

solution-1 (DuckDB `PIVOT`):

```sql
PIVOT (
    SELECT c.category_name, r.rating
    FROM reviews r
    JOIN products   p ON r.product_id  = p.product_id
    JOIN categories c ON p.category_id = c.category_id
)
ON rating IN (1, 2, 3, 4, 5)
USING COUNT(*)
GROUP BY category_name
ORDER BY category_name;
```

**Result:**

```text
┌────────────────┬───────┬───────┬───────┬───────┬───────┐
│ category_name  │   1   │   2   │   3   │   4   │   5   │
│    varchar     │ int64 │ int64 │ int64 │ int64 │ int64 │
├────────────────┼───────┼───────┼───────┼───────┼───────┤
│ Beauty         │     4 │     0 │     1 │    10 │     2 │
│ Books          │     0 │     3 │     4 │     7 │     8 │
│ Clothing       │     2 │     1 │     6 │     5 │     8 │
│ Electronics    │     2 │     0 │     1 │     3 │     9 │
│ Food & Grocery │     1 │     2 │     2 │     8 │     4 │
│ Home & Kitchen │     1 │     2 │     1 │     5 │     9 │
│ Sports         │     1 │     1 │     1 │     5 │    10 │
│ Toys           │     1 │     2 │     4 │     9 │     5 │
└────────────────┴───────┴───────┴───────┴───────┴───────┘
```

solution-2 (standard SQL with `FILTER`):

```sql
SELECT c.category_name,
       COUNT(*) FILTER (WHERE r.rating = 1) AS "1",
       COUNT(*) FILTER (WHERE r.rating = 2) AS "2",
       COUNT(*) FILTER (WHERE r.rating = 3) AS "3",
       COUNT(*) FILTER (WHERE r.rating = 4) AS "4",
       COUNT(*) FILTER (WHERE r.rating = 5) AS "5"
FROM reviews r
JOIN products   p ON r.product_id  = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY c.category_name;
```

**Result:**

```text
┌────────────────┬───────┬───────┬───────┬───────┬───────┐
│ category_name  │   1   │   2   │   3   │   4   │   5   │
│    varchar     │ int64 │ int64 │ int64 │ int64 │ int64 │
├────────────────┼───────┼───────┼───────┼───────┼───────┤
│ Beauty         │     4 │     0 │     1 │    10 │     2 │
│ Books          │     0 │     3 │     4 │     7 │     8 │
│ Clothing       │     2 │     1 │     6 │     5 │     8 │
│ Electronics    │     2 │     0 │     1 │     3 │     9 │
│ Food & Grocery │     1 │     2 │     2 │     8 │     4 │
│ Home & Kitchen │     1 │     2 │     1 │     5 │     9 │
│ Sports         │     1 │     1 │     1 │     5 │    10 │
│ Toys           │     1 │     2 │     4 │     9 │     5 │
└────────────────┴───────┴───────┴───────┴───────┴───────┘
```

### Q17. For each supplier, list how many products it supplies and the categories they belong to (STRING_AGG)

```sql
SELECT s.supplier_name,
       COUNT(*) AS num_products,
       STRING_AGG(DISTINCT c.category_name, ', ' ORDER BY c.category_name) AS categories
FROM suppliers s
JOIN product_suppliers ps ON s.supplier_id  = ps.supplier_id
JOIN products          p  ON ps.product_id  = p.product_id
JOIN categories        c  ON p.category_id  = c.category_id
GROUP BY s.supplier_name
ORDER BY num_products DESC, s.supplier_name;
```

**Result:**

```text
┌─────────────────┬──────────────┬─────────────────────────────────────────────────────────────────────────────┐
│  supplier_name  │ num_products │                                 categories                                  │
│     varchar     │    int64     │                                   varchar                                   │
├─────────────────┼──────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ GlobalTech      │           14 │ Beauty, Clothing, Electronics, Food & Grocery, Home & Kitchen, Sports, Toys │
│ QualityFirst    │           12 │ Beauty, Books, Electronics, Home & Kitchen, Sports, Toys                    │
│ BeautyCare      │            8 │ Beauty                                                                      │
│ BookHouse Ltd   │            8 │ Books                                                                       │
│ Fashion Forward │            8 │ Clothing                                                                    │
│ FreshFoods      │            8 │ Food & Grocery                                                              │
│ HomeGoods Co    │            8 │ Home & Kitchen                                                              │
│ SportZone       │            8 │ Sports                                                                      │
│ TechWorld Inc   │            8 │ Electronics                                                                 │
│ ToyLand Inc     │            8 │ Toys                                                                        │
└─────────────────┴──────────────┴─────────────────────────────────────────────────────────────────────────────┘
  10 rows                                                                                            3 columns
```

### Q18. Supply risk: products that have only one supplier

```sql
SELECT product_name,
       category_name,
       stock_quantity
FROM product_catalog
WHERE num_suppliers = 1
ORDER BY category_name, product_name;
```

**Result:**

```text
┌────────────────────┬───────────────┬────────────────┐
│    product_name    │ category_name │ stock_quantity │
│      varchar       │    varchar    │     int32      │
├────────────────────┼───────────────┼────────────────┤
│ Body Lotion        │ Beauty        │            299 │
│ Eye Serum          │ Beauty        │            275 │
│ Hand Cream         │ Beauty        │            126 │
│ Sunscreen SPF50    │ Beauty        │            255 │
│ Clean Code         │ Books         │            174 │
│    ·               │   ·           │             ·  │
│    ·               │   ·           │             ·  │
│    ·               │   ·           │             ·  │
│ Yoga Mat           │ Sports        │            186 │
│ Board Game Classic │ Toys          │            112 │
│ Puzzle 1000pc      │ Toys          │            431 │
│ RC Car             │ Toys          │             28 │
│ Stuffed Bear       │ Toys          │             16 │
└────────────────────┴───────────────┴────────────────┘
  38 rows (10 shown)                        3 columns
```

### Q19. Top 10 products by margin percentage (price vs. cheapest supplier cost)

```sql
SELECT product_name,
       price,
       min_cost_price,
       price - min_cost_price                                AS margin,
       ROUND(100.0 * (price - min_cost_price) / price, 1)    AS margin_pct
FROM product_catalog
ORDER BY margin_pct DESC
LIMIT 10;
```

**Result:**

```text
┌─────────────────────┬───────────────┬────────────────┬───────────────┬────────────┐
│    product_name     │     price     │ min_cost_price │    margin     │ margin_pct │
│       varchar       │ decimal(10,2) │ decimal(10,2)  │ decimal(11,2) │   double   │
├─────────────────────┼───────────────┼────────────────┼───────────────┼────────────┤
│ Cycling Helmet      │         98.97 │          37.25 │         61.72 │       62.4 │
│ Mechanical Keyboard │        120.17 │          47.50 │         72.67 │       60.5 │
│ SQL Cookbook        │        122.37 │          48.65 │         73.72 │       60.2 │
│ The Great Novel     │         84.02 │          34.16 │         49.86 │       59.3 │
│ Tablet Air          │        446.63 │         182.82 │        263.81 │       59.1 │
│ Shampoo Natural     │         98.21 │          40.59 │         57.62 │       58.7 │
│ Resistance Bands    │        110.72 │          46.27 │         64.45 │       58.2 │
│ Desk Lamp           │        133.39 │          55.70 │         77.69 │       58.2 │
│ Running Shoes       │         19.02 │           7.96 │         11.06 │       58.1 │
│ Lip Balm Set        │         62.37 │          26.13 │         36.24 │       58.1 │
└─────────────────────┴───────────────┴────────────────┴───────────────┴────────────┘
  10 rows                                                                 5 columns
```

### Q20. The 5 products with the lowest margin percentage

```sql
SELECT product_name,
       category_name,
       price,
       min_cost_price,
       ROUND(100.0 * (price - min_cost_price) / price, 1) AS margin_pct
FROM product_catalog
ORDER BY margin_pct ASC
LIMIT 5;
```

**Result:**

```text
┌─────────────────┬────────────────┬───────────────┬────────────────┬────────────┐
│  product_name   │ category_name  │     price     │ min_cost_price │ margin_pct │
│     varchar     │    varchar     │ decimal(10,2) │ decimal(10,2)  │   double   │
├─────────────────┼────────────────┼───────────────┼────────────────┼────────────┤
│ Throw Pillow    │ Home & Kitchen │         88.72 │          61.41 │       30.8 │
│ Yoga Mat        │ Sports         │         97.17 │          66.49 │       31.6 │
│ Bookshelf       │ Home & Kitchen │         60.12 │          40.53 │       32.6 │
│ Organic Granola │ Food & Grocery │         62.91 │          41.81 │       33.5 │
│ Science Set     │ Toys           │        137.40 │          90.03 │       34.5 │
└─────────────────┴────────────────┴───────────────┴────────────────┴────────────┘
```


## Part C — Sub-queries and Set Operations


### Q21. Customers who have never had a cancelled order (NOT EXISTS)

```sql
SELECT c.customer_id,
       c.first_name,
       c.last_name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id AND
          o.status = 'cancelled'
)
ORDER BY c.customer_id;
```

**Result:**

```text
┌─────────────┬────────────┬───────────┐
│ customer_id │ first_name │ last_name │
│    int32    │  varchar   │  varchar  │
├─────────────┼────────────┼───────────┤
│           2 │ Bob        │ Johnson   │
│           3 │ Carol      │ Lee       │
│           6 │ Frank      │ Martinez  │
│          11 │ Karen      │ Moore     │
│          12 │ Leo        │ Jackson   │
│           · │  ·         │    ·      │
│           · │  ·         │    ·      │
│           · │  ·         │    ·      │
│          34 │ Hugo       │ Phillips  │
│          35 │ Iris       │ Campbell  │
│          36 │ Joel       │ Parker    │
│          37 │ Kira       │ Evans     │
│          40 │ Omar       │ Stewart   │
└─────────────┴────────────┴───────────┘
  19 rows (10 shown)         3 columns
```

### Q22. Products that have been ordered but never reviewed (EXCEPT)

```sql
SELECT p.product_id, p.product_name
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
EXCEPT
SELECT p.product_id, p.product_name
FROM reviews r
JOIN products p ON r.product_id = p.product_id
ORDER BY product_id;
```

**Result:**

```text
┌────────────┬──────────────────┐
│ product_id │   product_name   │
│   int32    │     varchar      │
├────────────┼──────────────────┤
│          3 │ Wireless Earbuds │
│         21 │ Wool Sweater     │
│         31 │ Wall Clock       │
│         33 │ Yoga Mat         │
│         56 │ Nail Kit         │
│         59 │ Dark Chocolate   │
│         60 │ Trail Mix        │
│         61 │ Protein Bars     │
└────────────┴──────────────────┘
```

### Q23. Customers who both ordered and reviewed the same product (INTERSECT)

```sql
SELECT o.customer_id, oi.product_id
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
INTERSECT
SELECT customer_id, product_id
FROM reviews
ORDER BY customer_id, product_id;
```

**Result:**

```text
┌─────────────┬────────────┐
│ customer_id │ product_id │
│    int32    │   int32    │
├─────────────┼────────────┤
│           1 │         57 │
│           5 │         19 │
│           5 │         36 │
│           6 │         17 │
│           6 │         36 │
│           · │          · │
│           · │          · │
│           · │          · │
│          35 │         47 │
│          36 │         23 │
│          36 │         64 │
│          37 │         64 │
│          38 │         24 │
└─────────────┴────────────┘
  27 rows        2 columns
  (10 shown)               
```

### Q24. "Unverified" reviews: reviews of a product the reviewer never ordered

```sql
SELECT COUNT(*) AS total_reviews,
       COUNT(*) FILTER (WHERE NOT EXISTS (
           SELECT 1
           FROM orders o
           JOIN order_items oi ON o.order_id = oi.order_id
           WHERE o.customer_id  = r.customer_id AND
                 oi.product_id  = r.product_id
       )) AS unverified_reviews
FROM reviews r;
```

**Result:**

```text
┌───────────────┬────────────────────┐
│ total_reviews │ unverified_reviews │
│     int64     │       int64        │
├───────────────┼────────────────────┤
│           150 │                122 │
└───────────────┴────────────────────┘
```

### Q25. Products priced above the average price of their own category (correlated sub-query)

```sql
SELECT p.product_name,
       c.category_name,
       p.price
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.price > (
    SELECT AVG(p2.price)
    FROM products p2
    WHERE p2.category_id = p.category_id
)
ORDER BY c.category_name, p.price DESC;
```

**Result:**

```text
┌───────────────────────┬───────────────┬───────────────┐
│     product_name      │ category_name │     price     │
│        varchar        │    varchar    │ decimal(10,2) │
├───────────────────────┼───────────────┼───────────────┤
│ Face Moisturizer      │ Beauty        │        132.07 │
│ Eye Serum             │ Beauty        │        113.02 │
│ Shampoo Natural       │ Beauty        │         98.21 │
│ SQL Cookbook          │ Books         │        122.37 │
│ Data Science Handbook │ Books         │        115.03 │
│      ·                │  ·            │           ·   │
│      ·                │  ·            │           ·   │
│      ·                │  ·            │           ·   │
│ Science Set           │ Toys          │        137.40 │
│ Card Game             │ Toys          │        121.73 │
│ RC Car                │ Toys          │        116.41 │
│ Board Game Classic    │ Toys          │        104.78 │
│ Puzzle 1000pc         │ Toys          │        104.27 │
└───────────────────────┴───────────────┴───────────────┘
  33 rows (10 shown)                          3 columns
```

### Q26. Orders whose revenue is more than twice the customer's average order revenue

```sql
WITH customer_avg AS (
    SELECT customer_id,
           AVG(items_total) AS avg_items_total
    FROM order_summary
    WHERE status <> 'cancelled'
    GROUP BY customer_id
)
SELECT s.order_id,
       s.customer_name,
       s.items_total,
       ROUND(a.avg_items_total, 2) AS customer_avg
FROM order_summary s
JOIN customer_avg a ON s.customer_id = a.customer_id
WHERE s.status <> 'cancelled' AND
      s.items_total > 2 * a.avg_items_total
ORDER BY s.items_total DESC;
```

**Result:**

```text
┌──────────┬───────────────┬───────────────┬──────────────┐
│ order_id │ customer_name │  items_total  │ customer_avg │
│  int32   │    varchar    │ decimal(38,2) │    double    │
├──────────┼───────────────┼───────────────┼──────────────┤
│      182 │ Mia White     │       1984.98 │       742.73 │
│      109 │ Aria Baker    │       1983.78 │       708.81 │
│       11 │ Cora Carter   │       1973.93 │       733.02 │
│      199 │ Quinn Hall    │       1877.48 │       599.04 │
│      108 │ Alice Smith   │       1866.46 │       705.39 │
│       ·  │     ·         │          ·    │          ·   │
│       ·  │     ·         │          ·    │          ·   │
│       ·  │     ·         │          ·    │          ·   │
│      169 │ Tina King     │       1426.52 │       704.97 │
│       21 │ Liam Edwards  │       1403.77 │       601.22 │
│      110 │ Nora Collins  │       1070.67 │       429.37 │
│       44 │ Rosa Young    │        825.59 │       313.56 │
│      139 │ Hugo Phillips │        774.00 │       356.01 │
└──────────┴───────────────┴───────────────┴──────────────┘
  16 rows (10 shown)                            4 columns
```

### Q27. Categories in which every product has at least 50 units in stock

```sql
SELECT c.category_name,
       MIN(p.stock_quantity) AS lowest_stock
FROM categories c
JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_name
HAVING MIN(p.stock_quantity) >= 50
ORDER BY c.category_name;
```

**Result:**

```text
┌────────────────┬──────────────┐
│ category_name  │ lowest_stock │
│    varchar     │    int32     │
├────────────────┼──────────────┤
│ Beauty         │           73 │
│ Clothing       │           63 │
│ Home & Kitchen │           51 │
│ Sports         │           83 │
└────────────────┴──────────────┘
```


## Part D — Window Functions


### Q28. Top 2 products by revenue within each category (QUALIFY)

```sql
SELECT c.category_name,
       p.product_name,
       SUM(oi.quantity * oi.unit_price) AS revenue,
       RANK() OVER (PARTITION BY c.category_name
                    ORDER BY SUM(oi.quantity * oi.unit_price) DESC) AS rnk
FROM order_items oi
JOIN orders     o ON oi.order_id   = o.order_id
JOIN products   p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
WHERE o.status <> 'cancelled'
GROUP BY c.category_name, p.product_name
QUALIFY rnk <= 2
ORDER BY c.category_name, rnk;
```

**Result:**

```text
┌────────────────┬───────────────────────┬───────────────┬───────┐
│ category_name  │     product_name      │    revenue    │  rnk  │
│    varchar     │        varchar        │ decimal(38,2) │ int64 │
├────────────────┼───────────────────────┼───────────────┼───────┤
│ Beauty         │ Face Moisturizer      │       3037.61 │     1 │
│ Beauty         │ Eye Serum             │       2938.52 │     2 │
│ Books          │ SQL Cookbook          │       4160.58 │     1 │
│ Books          │ Data Science Handbook │       2185.57 │     2 │
│ Clothing       │ Cargo Shorts          │       3652.50 │     1 │
│    ·           │      ·                │          ·    │     · │
│    ·           │      ·                │          ·    │     · │
│    ·           │      ·                │          ·    │     · │
│ Home & Kitchen │ Shower Curtain        │       2513.62 │     2 │
│ Sports         │ Cycling Helmet        │       3266.01 │     1 │
│ Sports         │ Running Watch         │       3202.80 │     2 │
│ Toys           │ Science Set           │       5083.80 │     1 │
│ Toys           │ Building Blocks       │       4751.36 │     2 │
└────────────────┴───────────────────────┴───────────────┴───────┘
  16 rows (10 shown)                                   4 columns
```

### Q29. Number each of customer 5's orders and show the days since the previous order (ROW_NUMBER, LAG)

```sql
SELECT order_id,
       order_date,
       ROW_NUMBER() OVER (ORDER BY order_date, order_id) AS order_number,
       LAG(order_date) OVER (ORDER BY order_date, order_id) AS previous_order,
       DATE_DIFF('day',
                 LAG(order_date) OVER (ORDER BY order_date, order_id),
                 order_date) AS days_since_previous
FROM orders
WHERE customer_id = 5
ORDER BY order_number;
```

**Result:**

```text
┌──────────┬────────────┬──────────────┬────────────────┬─────────────────────┐
│ order_id │ order_date │ order_number │ previous_order │ days_since_previous │
│  int32   │    date    │    int64     │      date      │        int64        │
├──────────┼────────────┼──────────────┼────────────────┼─────────────────────┤
│       32 │ 2024-01-05 │            1 │ NULL           │                NULL │
│        2 │ 2024-01-17 │            2 │ 2024-01-05     │                  12 │
│      177 │ 2024-03-21 │            3 │ 2024-01-17     │                  64 │
│       35 │ 2024-05-05 │            4 │ 2024-03-21     │                  45 │
│      167 │ 2024-07-24 │            5 │ 2024-05-05     │                  80 │
│      104 │ 2024-07-31 │            6 │ 2024-07-24     │                   7 │
│        1 │ 2024-12-28 │            7 │ 2024-07-31     │                 150 │
└──────────┴────────────┴──────────────┴────────────────┴─────────────────────┘
```

### Q30. Running total of revenue by month (cumulative SUM)

```sql
SELECT month,
       revenue,
       SUM(revenue) OVER (ORDER BY month) AS running_revenue
FROM (
    SELECT DATE_TRUNC('month', order_date) AS month,
           SUM(items_total)                AS revenue
    FROM order_summary
    WHERE status <> 'cancelled'
    GROUP BY month
)
ORDER BY month;
```

**Result:**

```text
┌─────────────────────┬───────────────┬─────────────────┐
│        month        │    revenue    │ running_revenue │
│      timestamp      │ decimal(38,2) │  decimal(38,2)  │
├─────────────────────┼───────────────┼─────────────────┤
│ 2024-01-01 00:00:00 │       7030.54 │         7030.54 │
│ 2024-02-01 00:00:00 │      11901.00 │        18931.54 │
│ 2024-03-01 00:00:00 │       7266.20 │        26197.74 │
│ 2024-04-01 00:00:00 │      10721.49 │        36919.23 │
│ 2024-05-01 00:00:00 │       9271.63 │        46190.86 │
│          ·          │          ·    │            ·    │
│          ·          │          ·    │            ·    │
│          ·          │          ·    │            ·    │
│ 2024-10-01 00:00:00 │      11790.25 │       101155.59 │
│ 2024-11-01 00:00:00 │       5243.49 │       106399.08 │
│ 2024-12-01 00:00:00 │      12049.22 │       118448.30 │
│ 2025-01-01 00:00:00 │       9516.46 │       127964.76 │
│ 2025-02-01 00:00:00 │       2498.58 │       130463.34 │
└─────────────────────┴───────────────┴─────────────────┘
  14 rows (10 shown)                          3 columns
```

### Q31. 3-month moving average of monthly revenue

```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date) AS month,
           SUM(items_total)                AS revenue
    FROM order_summary
    WHERE status <> 'cancelled'
    GROUP BY month
)
SELECT month,
       revenue,
       ROUND(AVG(revenue) OVER (ORDER BY month
             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m
FROM monthly
ORDER BY month;
```

**Result:**

```text
┌─────────────────────┬───────────────┬───────────────┐
│        month        │    revenue    │ moving_avg_3m │
│      timestamp      │ decimal(38,2) │    double     │
├─────────────────────┼───────────────┼───────────────┤
│ 2024-01-01 00:00:00 │       7030.54 │       7030.54 │
│ 2024-02-01 00:00:00 │      11901.00 │       9465.77 │
│ 2024-03-01 00:00:00 │       7266.20 │       8732.58 │
│ 2024-04-01 00:00:00 │      10721.49 │        9962.9 │
│ 2024-05-01 00:00:00 │       9271.63 │       9086.44 │
│          ·          │          ·    │          ·    │
│          ·          │          ·    │          ·    │
│          ·          │          ·    │          ·    │
│ 2024-10-01 00:00:00 │      11790.25 │       8243.14 │
│ 2024-11-01 00:00:00 │       5243.49 │       7414.37 │
│ 2024-12-01 00:00:00 │      12049.22 │       9694.32 │
│ 2025-01-01 00:00:00 │       9516.46 │       8936.39 │
│ 2025-02-01 00:00:00 │       2498.58 │       8021.42 │
└─────────────────────┴───────────────┴───────────────┘
  14 rows (10 shown)                        3 columns
```

### Q32. Each customer's share of their state's revenue

```sql
SELECT state,
       customer_name,
       SUM(items_total) AS revenue,
       ROUND(100.0 * SUM(items_total)
             / SUM(SUM(items_total)) OVER (PARTITION BY state), 1) AS pct_of_state
FROM order_summary
WHERE status <> 'cancelled'
GROUP BY state, customer_name
ORDER BY state, pct_of_state DESC;
```

**Result:**

```text
┌─────────┬───────────────┬───────────────┬──────────────┐
│  state  │ customer_name │    revenue    │ pct_of_state │
│ varchar │    varchar    │ decimal(38,2) │    double    │
├─────────┼───────────────┼───────────────┼──────────────┤
│ CA      │ Sam Allen     │       5027.59 │         20.2 │
│ CA      │ Iris Campbell │       4913.00 │         19.7 │
│ CA      │ Quinn Hall    │       4193.27 │         16.8 │
│ CA      │ Carol Lee     │       3622.57 │         14.5 │
│ CA      │ David Brown   │       3583.49 │         14.4 │
│ ·       │      ·        │          ·    │           ·  │
│ ·       │      ·        │          ·    │           ·  │
│ ·       │      ·        │          ·    │           ·  │
│ TX      │ Leo Jackson   │       2299.28 │         24.1 │
│ TX      │ Finn Roberts  │       1101.48 │         11.5 │
│ WA      │ Blake Nelson  │       4062.90 │         50.2 │
│ WA      │ Zach Adams    │       3170.95 │         39.2 │
│ WA      │ Henry Taylor  │        853.73 │         10.6 │
└─────────┴───────────────┴───────────────┴──────────────┘
  40 rows (10 shown)                           4 columns
```

### Q33. Split customers into 4 spending tiers (NTILE) and summarize each tier

```sql
WITH spend AS (
    SELECT customer_id,
           SUM(items_total) AS revenue
    FROM order_summary
    WHERE status <> 'cancelled'
    GROUP BY customer_id
),
tiers AS (
    SELECT *,
           NTILE(4) OVER (ORDER BY revenue DESC) AS tier
    FROM spend
)
SELECT tier,
       COUNT(*)     AS num_customers,
       MIN(revenue) AS min_revenue,
       MAX(revenue) AS max_revenue,
       SUM(revenue) AS tier_revenue
FROM tiers
GROUP BY tier
ORDER BY tier;
```

**Result:**

```text
┌───────┬───────────────┬───────────────┬───────────────┬───────────────┐
│ tier  │ num_customers │  min_revenue  │  max_revenue  │ tier_revenue  │
│ int64 │     int64     │ decimal(38,2) │ decimal(38,2) │ decimal(38,2) │
├───────┼───────────────┼───────────────┼───────────────┼───────────────┤
│     1 │            10 │       4193.27 │       7012.77 │      52053.32 │
│     2 │            10 │       3241.74 │       4062.90 │      36663.86 │
│     3 │            10 │       2299.28 │       3170.95 │      27688.86 │
│     4 │            10 │        619.30 │       1880.69 │      14057.30 │
└───────┴───────────────┴───────────────┴───────────────┴───────────────┘
```

### Q34. The first product each customer ever bought (ARG_MIN)

`ARG_MIN(x, y)` returns the value of `x` on the row where `y` is smallest.

```sql
SELECT o.customer_id,
       MIN(o.order_date)                                AS first_order_date,
       ARG_MIN(p.product_name, (o.order_date, oi.item_id)) AS first_product
FROM orders o
JOIN order_items oi ON o.order_id   = oi.order_id
JOIN products    p  ON oi.product_id = p.product_id
GROUP BY o.customer_id
ORDER BY o.customer_id;
```

**Result:**

```text
┌─────────────┬──────────────────┬─────────────────┐
│ customer_id │ first_order_date │  first_product  │
│    int32    │       date       │     varchar     │
├─────────────┼──────────────────┼─────────────────┤
│           1 │ 2024-02-27       │ Science Set     │
│           2 │ 2024-02-17       │ Tablet Air      │
│           3 │ 2024-06-06       │ Blender Pro     │
│           4 │ 2024-02-17       │ Nail Kit        │
│           5 │ 2024-01-05       │ Wall Clock      │
│           · │     ·            │     ·           │
│           · │     ·            │     ·           │
│           · │     ·            │     ·           │
│          36 │ 2024-01-19       │ Almond Butter   │
│          37 │ 2024-02-21       │ Design Patterns │
│          38 │ 2024-05-17       │ Bookshelf       │
│          39 │ 2024-01-21       │ Dumbbells Set   │
│          40 │ 2024-10-18       │ Lip Balm Set    │
└─────────────┴──────────────────┴─────────────────┘
  40 rows (10 shown)                     3 columns
```

### Q35. Products priced in the top 10% (QUANTILE_CONT)

```sql
WITH cutoff AS (
    SELECT QUANTILE_CONT(price, 0.9) AS p90
    FROM products
)
SELECT p.product_name,
       p.price,
       ROUND(c.p90, 2) AS p90_price
FROM products p
CROSS JOIN cutoff c
WHERE p.price >= c.p90
ORDER BY p.price DESC;
```

**Result:**

```text
┌───────────────────┬───────────────┬───────────────┐
│   product_name    │     price     │   p90_price   │
│      varchar      │ decimal(10,2) │ decimal(10,2) │
├───────────────────┼───────────────┼───────────────┤
│ Tablet Air        │        446.63 │        147.33 │
│ Laptop Pro 15     │        372.07 │        147.33 │
│ Smartphone X12    │        321.52 │        147.33 │
│ Bluetooth Speaker │        297.29 │        147.33 │
│ Green Tea Box     │        149.61 │        147.33 │
│ Building Blocks   │        148.48 │        147.33 │
│ Shower Curtain    │        147.86 │        147.33 │
└───────────────────┴───────────────┴───────────────┘
```

### Q36. The best-selling product (by units) in each month of 2024

```sql
SELECT DATE_TRUNC('month', o.order_date) AS month,
       p.product_name,
       SUM(oi.quantity) AS units
FROM orders o
JOIN order_items oi ON o.order_id   = oi.order_id
JOIN products    p  ON oi.product_id = p.product_id
WHERE o.status <> 'cancelled' AND
      YEAR(o.order_date) = 2024
GROUP BY month, p.product_name
QUALIFY ROW_NUMBER() OVER (PARTITION BY month
                           ORDER BY SUM(oi.quantity) DESC, p.product_name) = 1
ORDER BY month;
```

**Result:**

```text
┌─────────────────────┬────────────────────┬────────┐
│        month        │    product_name    │ units  │
│      timestamp      │      varchar       │ int128 │
├─────────────────────┼────────────────────┼────────┤
│ 2024-01-01 00:00:00 │ Wireless Earbuds   │      6 │
│ 2024-02-01 00:00:00 │ Wireless Earbuds   │     11 │
│ 2024-03-01 00:00:00 │ Running Shoes      │      7 │
│ 2024-04-01 00:00:00 │ Building Blocks    │     10 │
│ 2024-05-01 00:00:00 │ Clean Code         │      8 │
│ 2024-06-01 00:00:00 │ Dark Chocolate     │     12 │
│ 2024-07-01 00:00:00 │ Baseball Cap       │      9 │
│ 2024-08-01 00:00:00 │ Winter Jacket      │      6 │
│ 2024-09-01 00:00:00 │ Cutting Board      │      5 │
│ 2024-10-01 00:00:00 │ Running Watch      │      7 │
│ 2024-11-01 00:00:00 │ Board Game Classic │      6 │
│ 2024-12-01 00:00:00 │ Hand Cream         │     12 │
└─────────────────────┴────────────────────┴────────┘
  12 rows                                 3 columns
```

### Q37. Customers who placed two orders within 7 days of each other (LAG over each customer)

```sql
WITH gaps AS (
    SELECT customer_id,
           order_id,
           order_date,
           DATE_DIFF('day',
                     LAG(order_date) OVER (PARTITION BY customer_id
                                           ORDER BY order_date, order_id),
                     order_date) AS days_since_previous
    FROM orders
)
SELECT customer_id,
       order_id,
       order_date,
       days_since_previous
FROM gaps
WHERE days_since_previous <= 7
ORDER BY customer_id, order_date;
```

**Result:**

```text
┌─────────────┬──────────┬────────────┬─────────────────────┐
│ customer_id │ order_id │ order_date │ days_since_previous │
│    int32    │  int32   │    date    │        int64        │
├─────────────┼──────────┼────────────┼─────────────────────┤
│           3 │       51 │ 2024-07-02 │                   6 │
│           4 │      184 │ 2024-03-25 │                   7 │
│           5 │      104 │ 2024-07-31 │                   7 │
│           9 │      163 │ 2024-11-22 │                   0 │
│          13 │      160 │ 2024-05-31 │                   0 │
│           · │       ·  │     ·      │                   · │
│           · │       ·  │     ·      │                   · │
│           · │       ·  │     ·      │                   · │
│          30 │      105 │ 2024-07-31 │                   0 │
│          33 │      187 │ 2024-10-03 │                   5 │
│          37 │      190 │ 2024-10-27 │                   5 │
│          38 │       28 │ 2024-10-16 │                   7 │
│          39 │      188 │ 2024-01-21 │                   0 │
└─────────────┴──────────┴────────────┴─────────────────────┘
  18 rows (10 shown)                              4 columns
```


## Part E — Final Review: Integrated Analytics (Week 10)


### Q38. Customer 360: one row per customer with orders, revenue, reviews, and last order date

```sql
WITH o AS (
    SELECT customer_id,
           COUNT(*)                                      AS num_orders,
           SUM(items_total) FILTER (WHERE status <> 'cancelled') AS revenue,
           MAX(order_date)                               AS last_order
    FROM order_summary
    GROUP BY customer_id
),
r AS (
    SELECT customer_id,
           COUNT(*)              AS num_reviews,
           ROUND(AVG(rating), 2) AS avg_rating_given
    FROM reviews
    GROUP BY customer_id
)
SELECT c.customer_id,
       c.first_name || ' ' || c.last_name AS customer_name,
       o.num_orders,
       o.revenue,
       COALESCE(r.num_reviews, 0) AS num_reviews,
       r.avg_rating_given,
       o.last_order
FROM customers c
LEFT JOIN o ON c.customer_id = o.customer_id
LEFT JOIN r ON c.customer_id = r.customer_id
ORDER BY o.revenue DESC NULLS LAST;
```

**Result:**

```text
┌─────────────┬────────────────┬────────────┬───────────────┬─────────────┬──────────────────┬────────────┐
│ customer_id │ customer_name  │ num_orders │    revenue    │ num_reviews │ avg_rating_given │ last_order │
│    int32    │    varchar     │   int64    │ decimal(38,2) │    int64    │      double      │    date    │
├─────────────┼────────────────┼────────────┼───────────────┼─────────────┼──────────────────┼────────────┤
│          30 │ Derek Mitchell │          9 │       7012.77 │           2 │              4.0 │ 2024-12-28 │
│           5 │ Eva Garcia     │          7 │       6405.91 │           6 │             4.33 │ 2024-12-28 │
│          13 │ Mia White      │          8 │       5941.83 │           1 │              3.0 │ 2024-08-05 │
│          19 │ Sam Allen      │          4 │       5027.59 │           3 │             2.67 │ 2024-12-27 │
│          20 │ Tina King      │          7 │       4934.82 │           5 │              3.8 │ 2024-12-24 │
│           · │     ·          │          · │          ·    │           · │               ·  │     ·      │
│           · │     ·          │          · │          ·    │           · │               ·  │     ·      │
│           · │     ·          │          · │          ·    │           · │               ·  │     ·      │
│          15 │ Olivia Clark   │          2 │       1371.26 │           1 │              4.0 │ 2025-02-01 │
│          10 │ Jack Wilson    │          2 │       1216.24 │           1 │              4.0 │ 2024-10-06 │
│          32 │ Finn Roberts   │          2 │       1101.48 │           2 │              3.5 │ 2024-10-11 │
│           8 │ Henry Taylor   │          3 │        853.73 │           1 │              4.0 │ 2025-02-02 │
│          23 │ Wendy Hill     │          2 │        619.30 │           5 │              4.4 │ 2025-01-08 │
└─────────────┴────────────────┴────────────┴───────────────┴─────────────┴──────────────────┴────────────┘
  40 rows (10 shown)                      use .last to show entire result                       7 columns
```

### Q39. RFM segmentation: recency, frequency, and monetary value with a CASE label

```sql
WITH rfm AS (
    SELECT customer_id,
           DATE_DIFF('day', MAX(order_date), DATE '2025-02-04') AS recency_days,
           COUNT(*)                                            AS frequency,
           SUM(items_total)                                    AS monetary
    FROM order_summary
    WHERE status <> 'cancelled'
    GROUP BY customer_id
)
SELECT CASE
           WHEN recency_days <= 90 AND frequency >= 5 THEN '1-champion'
           WHEN recency_days <= 90                    THEN '2-active'
           WHEN frequency >= 5                        THEN '3-at risk (was loyal)'
           ELSE '4-inactive'
       END                       AS segment,
       COUNT(*)                  AS num_customers,
       ROUND(AVG(recency_days))  AS avg_recency_days,
       ROUND(AVG(frequency), 1)  AS avg_orders,
       ROUND(AVG(monetary), 2)   AS avg_revenue
FROM rfm
GROUP BY segment
ORDER BY segment;
```

**Result:**

```text
┌───────────────────────┬───────────────┬──────────────────┬────────────┬─────────────┐
│        segment        │ num_customers │ avg_recency_days │ avg_orders │ avg_revenue │
│        varchar        │     int64     │      double      │   double   │   double    │
├───────────────────────┼───────────────┼──────────────────┼────────────┼─────────────┤
│ 1-champion            │            13 │             45.0 │        6.0 │     4206.89 │
│ 2-active              │            13 │             31.0 │        3.3 │     2779.84 │
│ 3-at risk (was loyal) │             5 │            138.0 │        6.2 │     4227.05 │
│ 4-inactive            │             9 │            231.0 │        2.1 │     2055.62 │
└───────────────────────┴───────────────┴──────────────────┴────────────┴─────────────┘
```

### Q40. Order fulfillment funnel: status vs. shipping progress

```sql
SELECT o.status,
       COUNT(*)                                                AS num_orders,
       COUNT(s.shipping_id)                                    AS shipped,
       COUNT(s.delivery_date)                                  AS delivered,
       COUNT(s.shipping_id) - COUNT(s.delivery_date)           AS in_transit
FROM orders o
LEFT JOIN shipping s ON o.order_id = s.order_id
GROUP BY o.status
ORDER BY num_orders DESC;
```

**Result:**

```text
┌────────────┬────────────┬─────────┬───────────┬────────────┐
│   status   │ num_orders │ shipped │ delivered │ in_transit │
│  varchar   │   int64    │  int64  │   int64   │   int64    │
├────────────┼────────────┼─────────┼───────────┼────────────┤
│ completed  │        115 │     115 │       115 │          0 │
│ processing │         30 │       0 │         0 │          0 │
│ cancelled  │         29 │       0 │         0 │          0 │
│ shipped    │         26 │      26 │         0 │         26 │
└────────────┴────────────┴─────────┴───────────┴────────────┘
```

### Q41. Market-basket analysis: product pairs most often bought in the same order (self-join)

```sql
SELECT p1.product_name AS product_a,
       p2.product_name AS product_b,
       COUNT(*)        AS times_together
FROM order_items a
JOIN order_items b ON a.order_id = b.order_id AND
                      a.product_id < b.product_id
JOIN products p1 ON a.product_id = p1.product_id
JOIN products p2 ON b.product_id = p2.product_id
GROUP BY product_a, product_b
HAVING COUNT(*) >= 3
ORDER BY times_together DESC, product_a, product_b;
```

**Result:**

```text
┌───────────────────────┬─────────────────┬────────────────┐
│       product_a       │    product_b    │ times_together │
│        varchar        │     varchar     │     int64      │
├───────────────────────┼─────────────────┼────────────────┤
│ Data Science Handbook │ Cycling Helmet  │              4 │
│ Data Science Handbook │ Science Set     │              4 │
│ Design Patterns       │ Cycling Helmet  │              4 │
│ Tablet Air            │ Cycling Helmet  │              4 │
│ Bluetooth Speaker     │ Shampoo Natural │              3 │
│     ·                 │      ·          │              · │
│     ·                 │      ·          │              · │
│     ·                 │      ·          │              · │
│ Wall Clock            │ Science Set     │              3 │
│ Webcam HD             │ Bookshelf       │              3 │
│ Winter Jacket         │ Building Blocks │              3 │
│ Winter Jacket         │ Hand Cream      │              3 │
│ Yoga Mat              │ Dark Chocolate  │              3 │
└───────────────────────┴─────────────────┴────────────────┘
  20 rows (10 shown)                             3 columns
```

### Q42. Category revenue by order status with subtotals (ROLLUP)

`NULL` in `status` marks a category subtotal; the last row is the grand total.

```sql
SELECT c.category_name,
       o.status,
       SUM(oi.quantity * oi.unit_price) AS items_total
FROM order_items oi
JOIN orders     o ON oi.order_id   = o.order_id
JOIN products   p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
WHERE c.category_name IN ('Electronics', 'Books')
GROUP BY ROLLUP (c.category_name, o.status)
ORDER BY c.category_name NULLS LAST, o.status NULLS LAST;
```

**Result:**

```text
┌───────────────┬────────────┬───────────────┐
│ category_name │   status   │  items_total  │
│    varchar    │  varchar   │ decimal(38,2) │
├───────────────┼────────────┼───────────────┤
│ Books         │ cancelled  │       2449.72 │
│ Books         │ completed  │       9489.13 │
│ Books         │ processing │       2844.98 │
│ Books         │ shipped    │        970.44 │
│ Books         │ NULL       │      15754.27 │
│ Electronics   │ cancelled  │       4874.63 │
│ Electronics   │ completed  │      26020.48 │
│ Electronics   │ processing │       4947.94 │
│ Electronics   │ shipped    │       4588.24 │
│ Electronics   │ NULL       │      40431.29 │
│ NULL          │ NULL       │      56185.56 │
└───────────────┴────────────┴───────────────┘
  11 rows                          3 columns
```

### Q43. Data-quality check: compare `orders.total_amount` with the sum of each order's line items

```sql
SELECT COUNT(*)                                                       AS num_orders,
       COUNT(*) FILTER (WHERE total_amount = items_total)             AS matching,
       COUNT(*) FILTER (WHERE total_amount <> items_total)            AS not_matching,
       ROUND(AVG(items_total - total_amount), 2)                      AS avg_difference
FROM order_summary;
```

**Result:**

```text
┌────────────┬──────────┬──────────────┬────────────────┐
│ num_orders │ matching │ not_matching │ avg_difference │
│   int64    │  int64   │    int64     │     double     │
├────────────┼──────────┼──────────────┼────────────────┤
│        200 │        0 │          200 │         351.13 │
└────────────┴──────────┴──────────────┴────────────────┘
```

### Q44. Query a CSV file directly, without loading it into a table

DuckDB can run SQL straight on files (CSV, Parquet, JSON) — a core idea of
modern data tools. This compares the file with the loaded table.

```sql
SELECT 'csv file' AS source, COUNT(*) AS num_rows, SUM(total_amount) AS total
FROM 'data/orders.csv'
UNION ALL
SELECT 'orders table', COUNT(*), SUM(total_amount)
FROM orders;
```

**Result:**

```text
┌──────────────┬──────────┬──────────┐
│    source    │ num_rows │  total   │
│   varchar    │  int64   │  double  │
├──────────────┼──────────┼──────────┤
│ csv file     │      200 │ 81718.06 │
│ orders table │      200 │ 81718.06 │
└──────────────┴──────────┴──────────┘
```

### Q45. Activity feed for customer 5: orders and reviews in one timeline (UNION ALL)

```sql
SELECT order_date      AS activity_date,
       'order'         AS activity,
       'order #' || order_id || ' (' || status || ')' AS details
FROM orders
WHERE customer_id = 5
UNION ALL
SELECT r.review_date,
       'review',
       r.rating || ' stars for ' || p.product_name
FROM reviews r
JOIN products p ON r.product_id = p.product_id
WHERE r.customer_id = 5
ORDER BY activity_date, activity;
```

**Result:**

```text
┌───────────────┬──────────┬─────────────────────────────┐
│ activity_date │ activity │           details           │
│     date      │ varchar  │           varchar           │
├───────────────┼──────────┼─────────────────────────────┤
│ 2024-01-05    │ order    │ order #32 (completed)       │
│ 2024-01-17    │ order    │ order #2 (cancelled)        │
│ 2024-03-21    │ order    │ order #177 (completed)      │
│ 2024-05-05    │ order    │ order #35 (completed)       │
│ 2024-06-04    │ review   │ 4 stars for Running Watch   │
│ 2024-06-20    │ review   │ 5 stars for Card Game       │
│ 2024-07-24    │ order    │ order #167 (completed)      │
│ 2024-07-31    │ order    │ order #104 (completed)      │
│ 2024-09-23    │ review   │ 4 stars for Green Tea Box   │
│ 2024-12-28    │ order    │ order #1 (processing)       │
│ 2025-01-07    │ review   │ 4 stars for Running Shoes   │
│ 2025-03-05    │ review   │ 4 stars for Olive Oil Extra │
│ 2025-04-01    │ review   │ 5 stars for Shampoo Natural │
└───────────────┴──────────┴─────────────────────────────┘
  13 rows                                      3 columns
```

### Q46. Count orders by year and status, plus totals per year and per status (GROUPING SETS)

```sql
SELECT YEAR(order_date) AS order_year,
       status,
       COUNT(*)         AS num_orders
FROM orders
GROUP BY GROUPING SETS ((order_year, status), (order_year), (status))
ORDER BY order_year NULLS LAST, status NULLS LAST;
```

**Result:**

```text
┌────────────┬────────────┬────────────┐
│ order_year │   status   │ num_orders │
│   int64    │  varchar   │   int64    │
├────────────┼────────────┼────────────┤
│       2024 │ cancelled  │         25 │
│       2024 │ completed  │        106 │
│       2024 │ processing │         30 │
│       2024 │ shipped    │         21 │
│       2024 │ NULL       │        182 │
│       2025 │ cancelled  │          4 │
│       2025 │ completed  │          9 │
│       2025 │ shipped    │          5 │
│       2025 │ NULL       │         18 │
│       NULL │ cancelled  │         29 │
│       NULL │ completed  │        115 │
│       NULL │ processing │         30 │
│       NULL │ shipped    │         26 │
└────────────┴────────────┴────────────┘
  13 rows                    3 columns
```

### Q47. Average rating vs. units sold by category: do better-rated categories sell more?

```sql
WITH sales AS (
    SELECT p.category_id, SUM(oi.quantity) AS units_sold
    FROM order_items oi
    JOIN orders   o ON oi.order_id   = o.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status <> 'cancelled'
    GROUP BY p.category_id
),
ratings AS (
    SELECT p.category_id, ROUND(AVG(r.rating), 2) AS avg_rating
    FROM reviews r
    JOIN products p ON r.product_id = p.product_id
    GROUP BY p.category_id
)
SELECT c.category_name,
       r.avg_rating,
       s.units_sold
FROM categories c
JOIN sales   s ON c.category_id = s.category_id
JOIN ratings r ON c.category_id = r.category_id
ORDER BY r.avg_rating DESC;
```

**Result:**

```text
┌────────────────┬────────────┬────────────┐
│ category_name  │ avg_rating │ units_sold │
│    varchar     │   double   │   int128   │
├────────────────┼────────────┼────────────┤
│ Sports         │       4.22 │        147 │
│ Electronics    │       4.13 │        158 │
│ Home & Kitchen │       4.06 │        175 │
│ Books          │       3.91 │        150 │
│ Clothing       │       3.73 │        182 │
│ Toys           │       3.71 │        165 │
│ Food & Grocery │       3.71 │        185 │
│ Beauty         │       3.35 │        160 │
└────────────────┴────────────┴────────────┘
```

### Q48. Customers whose revenue is above the average customer's revenue, with how far above (%)

```sql
WITH spend AS (
    SELECT customer_id,
           customer_name,
           SUM(items_total) AS revenue
    FROM order_summary
    WHERE status <> 'cancelled'
    GROUP BY customer_id, customer_name
)
SELECT customer_name,
       revenue,
       ROUND(100.0 * (revenue / AVG(revenue) OVER () - 1), 1) AS pct_above_avg
FROM spend
QUALIFY revenue > AVG(revenue) OVER ()
ORDER BY revenue DESC;
```

**Result:**

```text
┌────────────────┬───────────────┬───────────────┐
│ customer_name  │    revenue    │ pct_above_avg │
│    varchar     │ decimal(38,2) │    double     │
├────────────────┼───────────────┼───────────────┤
│ Derek Mitchell │       7012.77 │         115.0 │
│ Eva Garcia     │       6405.91 │          96.4 │
│ Mia White      │       5941.83 │          82.2 │
│ Sam Allen      │       5027.59 │          54.1 │
│ Tina King      │       4934.82 │          51.3 │
│     ·          │          ·    │            ·  │
│     ·          │          ·    │            ·  │
│     ·          │          ·    │            ·  │
│ Carol Lee      │       3622.57 │          11.1 │
│ Bob Johnson    │       3588.97 │          10.0 │
│ David Brown    │       3583.49 │           9.9 │
│ Aria Baker     │       3544.03 │           8.7 │
│ Yara Green     │       3416.78 │           4.8 │
└────────────────┴───────────────┴───────────────┘
  19 rows (10 shown)                   3 columns
```

### Q49. Shipping cost as a percentage of order revenue, by carrier

```sql
SELECT s.carrier,
       COUNT(*)                                                 AS shipments,
       SUM(s.shipping_cost)                                     AS shipping_cost,
       SUM(os.items_total)                                      AS revenue,
       ROUND(100.0 * SUM(s.shipping_cost) / SUM(os.items_total), 2) AS cost_pct
FROM shipping s
JOIN order_summary os ON s.order_id = os.order_id
GROUP BY s.carrier
ORDER BY cost_pct;
```

**Result:**

```text
┌─────────┬───────────┬───────────────┬───────────────┬──────────┐
│ carrier │ shipments │ shipping_cost │    revenue    │ cost_pct │
│ varchar │   int64   │ decimal(38,2) │ decimal(38,2) │  double  │
├─────────┼───────────┼───────────────┼───────────────┼──────────┤
│ UPS     │        33 │        487.13 │      28987.97 │     1.68 │
│ DHL     │        36 │        484.38 │      24965.42 │     1.94 │
│ USPS    │        38 │        619.54 │      30459.30 │     2.03 │
│ FedEx   │        34 │        465.61 │      22327.40 │     2.09 │
└─────────┴───────────┴───────────────┴───────────────┴──────────┘
```

### Q50. Executive dashboard: one row of key business numbers (multiple CTEs)

```sql
WITH sales AS (
    SELECT COUNT(*)         AS num_orders,
           SUM(items_total) AS revenue,
           AVG(items_total) AS avg_order_revenue
    FROM order_summary
    WHERE status <> 'cancelled'
),
cancels AS (
    SELECT ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'cancelled') / COUNT(*), 1)
               AS cancel_rate_pct
    FROM orders
),
delivery AS (
    SELECT ROUND(AVG(DATE_DIFF('day', ship_date, delivery_date)), 1) AS avg_delivery_days
    FROM shipping
    WHERE delivery_date IS NOT NULL
),
top_category AS (
    SELECT c.category_name
    FROM order_items oi
    JOIN orders     o ON oi.order_id   = o.order_id
    JOIN products   p ON oi.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    WHERE o.status <> 'cancelled'
    GROUP BY c.category_name
    ORDER BY SUM(oi.quantity * oi.unit_price) DESC
    LIMIT 1
)
SELECT (SELECT COUNT(*) FROM customers)       AS customers,
       s.num_orders,
       s.revenue,
       ROUND(s.avg_order_revenue, 2)           AS avg_order_revenue,
       c.cancel_rate_pct,
       d.avg_delivery_days,
       (SELECT ROUND(AVG(rating), 2) FROM reviews) AS avg_rating,
       t.category_name                         AS top_category
FROM sales s, cancels c, delivery d, top_category t;
```

**Result:**

```text
┌───────────┬────────────┬───────────────┬───────────────────┬─────────────────┬───────────────────┬────────────┬──────────────┐
│ customers │ num_orders │    revenue    │ avg_order_revenue │ cancel_rate_pct │ avg_delivery_days │ avg_rating │ top_category │
│   int64   │   int64    │ decimal(38,2) │      double       │     double      │      double       │   double   │   varchar    │
├───────────┼────────────┼───────────────┼───────────────────┼─────────────────┼───────────────────┼────────────┼──────────────┤
│        40 │        171 │     130463.34 │            762.94 │            14.5 │               4.6 │       3.85 │ Electronics  │
└───────────┴────────────┴───────────────┴───────────────────┴─────────────────┴───────────────────┴────────────┴──────────────┘
```
