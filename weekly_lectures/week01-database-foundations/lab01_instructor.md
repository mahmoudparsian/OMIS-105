# Lab 1: Getting Started with DuckDB and SQL Basics — INSTRUCTOR SOLUTIONS

## OMIS 105 — Database Management Systems
**Week 1 | Answer Key**

---

## Setup

```python
import duckdb
con = duckdb.connect()
con.sql("CREATE TABLE products AS SELECT * FROM read_csv_auto('products.csv')")
```

---

## Part 1: Exploration (10 points)

**Q1.** (2 pts) Display the first 10 rows of the products table.

```sql
SELECT * FROM products LIMIT 10;
```

**Q2.** (2 pts) How many products are in the table?

```sql
SELECT COUNT(*) AS total_products FROM products;
```
> **Answer**: 64 products

**Q3.** (3 pts) Distinct categories sorted alphabetically.

```sql
SELECT DISTINCT category
FROM products
ORDER BY category;
```
> **Answer**: 8 categories — Beauty, Books, Clothing, Electronics, Food & Grocery, Home & Kitchen, Sports, Toys

**Q4.** (3 pts) Describe products.

```sql
DESCRIBE products;
```
> **Answer**: 5 columns — product_id, product_name, category, price, stock_quantity

---

## Part 2: Filtering and Sorting (20 points)

**Q5.** (3 pts) All "Books" products.

```sql
SELECT product_name, price
FROM products
WHERE category = 'Books';
```

**Q6.** (3 pts) Products priced $10–$50.

```sql
SELECT product_name, category, price
FROM products
WHERE price BETWEEN 10 AND 50
ORDER BY price ASC;
```

**Q7.** (3 pts) Products containing "Pro".

```sql
SELECT product_name, category
FROM products
WHERE product_name LIKE '%Pro%';
```
> **Expected matches**: Laptop Pro 15, Blender Pro (and any others)

**Q8.** (4 pts) Electronics or Sports with price > $50.

```sql
SELECT product_name, category, price
FROM products
WHERE category IN ('Electronics', 'Sports')
  AND price > 50
ORDER BY price DESC;
```

**Q9.** (3 pts) Top 5 most expensive products.

```sql
SELECT product_name, category, price
FROM products
ORDER BY price DESC
LIMIT 5;
```

**Q10.** (4 pts) Products with zero stock.

```sql
SELECT product_name, category
FROM products
WHERE stock_quantity = 0;
```

---

## Part 3: Aggregation (15 points)

**Q11.** (5 pts) Average price of all products.

```sql
SELECT ROUND(AVG(price), 2) AS avg_price
FROM products;
```

**Q12.** (5 pts) Total inventory value.

```sql
SELECT ROUND(SUM(price * stock_quantity), 2) AS total_inventory_value
FROM products;
```

**Q13.** (5 pts) Electronics category statistics.

```sql
SELECT
    COUNT(*)             AS num_products,
    ROUND(AVG(price), 2) AS avg_price,
    MIN(price)           AS min_price,
    MAX(price)           AS max_price
FROM products
WHERE category = 'Electronics';
```

---

## Part 4: Computed Columns (10 points)

**Q14.** (5 pts) Price with tax.

```sql
SELECT product_name,
       price,
       ROUND(price * 1.0925, 2) AS price_with_tax
FROM products
ORDER BY price_with_tax DESC
LIMIT 10;
```

**Q15.** (5 pts) Stock status using CASE.

```sql
SELECT product_name,
       stock_quantity,
       CASE
           WHEN stock_quantity = 0 THEN 'Out of Stock'
           WHEN stock_quantity BETWEEN 1 AND 20 THEN 'Low Stock'
           ELSE 'In Stock'
       END AS stock_status
FROM products
ORDER BY stock_quantity;
```
> **Grading note**: Accept any reasonable threshold boundaries. The CASE syntax is what matters.

---

## Part 5: Challenge (5 bonus points)

**Q16.** Percentage of products per category.

```sql
SELECT category,
       COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM products), 1) AS percentage
FROM products
GROUP BY category
ORDER BY percentage DESC;
```
> **Note**: Students haven't formally learned GROUP BY yet (that's Week 3), but some may figure it out. Give full credit for any working solution. Also accept solutions using a manual total (64).

---

## Grading Rubric

| Part | Points |
|------|--------|
| Part 1: Exploration | 10 |
| Part 2: Filtering & Sorting | 20 |
| Part 3: Aggregation | 15 |
| Part 4: Computed Columns | 10 |
| **Subtotal** | **55** |
| Part 5: Challenge (bonus) | 5 |
| **Maximum** | **60** |

**Grading notes**:
- Deduct 1 point for missing ORDER BY when specified in the question
- Accept minor syntax variations (single vs double quotes, etc.)
- Give partial credit for queries that show correct logic but have small syntax errors

