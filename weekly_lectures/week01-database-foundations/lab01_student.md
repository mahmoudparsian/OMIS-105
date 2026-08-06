# Lab 1: Getting Started with DuckDB and SQL Basics

## OMIS 105 — Database Management Systems
**Week 1 | Estimated time: 60–90 minutes**

---

## Objectives

- Install DuckDB and connect from Python
- Load CSV data into a DuckDB table
- Write basic SQL queries using SELECT, WHERE, ORDER BY, LIMIT
- Use aggregate functions (COUNT, SUM, AVG, MIN, MAX)

## Setup

1. Open a Jupyter Notebook or Python environment
2. Install DuckDB: `pip install duckdb`
3. Place `./data/products.csv` in your working directory

```python
import duckdb
con = duckdb.connect()
con.sql("""
CREATE TABLE products 
AS 
SELECT * FROM read_csv_auto('./data/products.csv')
""")
```

---

## Part 1: Exploration (10 points)

**Q1.** Write a query to display the first 10 rows of the `products` table.

```sql
-- Your query here
```

**Q2.** How many products are in the table? Write a query using `COUNT(*)`.

```sql
-- Your query here
```

**Q3.** What are the distinct categories in the products table? Sort them alphabetically.

```sql
-- Your query here
```

**Q4.** Use `DESCRIBE products` to show the column names and data types. How many columns are there?

```sql
-- Your query here
```

---

## Part 2: Filtering and Sorting (20 points)

**Q5.** List all products in the "Books" category. Show product_name and price.

```sql
-- Your query here
```

**Q6.** Find all products priced between $10 and $50 (inclusive). Sort by price ascending.

```sql
-- Your query here
```

**Q7.** Find all products whose name contains the word "Pro". Show product_name and category.

```sql
-- Your query here
```

**Q8.** List all products that are in "Electronics" or "Sports" categories AND have a price greater than $50. Sort by price descending.

```sql
-- Your query here
```

**Q9.** Find the 5 most expensive products. Show product_name, category, and price.

```sql
-- Your query here
```

**Q10.** Find all products with zero stock. Show product_name and category.

```sql
-- Your query here
```

---

## Part 3: Aggregation (15 points)

**Q11.** What is the average price of all products? Round to 2 decimal places.

```sql
-- Your query here
```

**Q12.** What is the total inventory value (sum of price × stock_quantity) across all products?

```sql
-- Your query here
```

**Q13.** For the "Electronics" category only, find the count, average price, minimum price, and maximum price.

```sql
-- Your query here
```

---

## Part 4: Computed Columns (10 points)

**Q14.** Display each product's name, price, and a new column `price_with_tax` calculated as price × 1.0925 (9.25% sales tax). Round to 2 decimal places. Show the top 10 by price_with_tax descending.

```sql
-- Your query here
```

**Q15.** Create a column called `stock_status` that shows:
- "Out of Stock" if stock_quantity = 0
- "Low Stock" if stock_quantity between 1 and 20
- "In Stock" otherwise

*Hint: Use a CASE expression.*

```sql
-- Your query here
```

---

## Part 5: Challenge (5 points — bonus)

**Q16.** Write a single query that answers: "What percentage of products are in each category?" Show category, count, and percentage (rounded to 1 decimal). Sort by percentage descending.

*Hint: You can divide COUNT by the total count.*

```sql
-- Your query here
```

---

## Submission

- Submit your completed notebook/script with all queries and their output
- Ensure all queries run without errors
- Add brief comments explaining your approach for Q15 and Q16

**Total: 60 points (+ 5 bonus)**

