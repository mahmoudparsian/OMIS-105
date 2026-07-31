# Lab 2: Relational Thinking — Keys, Relationships, and Schema Design

## OMIS 105 — Database Management Systems
**Week 2 | Estimated time: 60–90 minutes**

---

## Objectives

- Identify primary keys, foreign keys, and candidate keys
- Understand and classify table relationships (1:1, 1:M, M:M)
- Create tables with proper constraints in DuckDB
- Draw an ER diagram for a given scenario

## Setup

```python
import duckdb
con = duckdb.connect()

for table, file in [('categories','categories.csv'),
                    ('products','products.csv'),
                    ('customers','customers.csv')]:
    con.sql(f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto('{file}')")
```

---

## Part 1: Key Identification (15 points)

**Q1.** For each table below, identify the primary key and explain why it qualifies:
- categories
- products
- customers

**Q2.** Which column in the `products` table is a foreign key? What table does it reference?

**Q3.** Is `email` in the `customers` table a candidate key? Write a query to prove your answer.

```sql
-- Your query here
```

**Q4.** Give an example of when you would use a composite primary key. Describe the table and its columns.

---

## Part 2: Relationship Analysis (15 points)

**Q5.** Classify each relationship and explain your reasoning:
- categories → products
- customers → orders (imagine an orders table)
- products ↔ suppliers

**Q6.** For the categories → products relationship, write a query that shows how many products belong to each category.

```sql
-- Your query here
```

**Q7.** If we add a `reviews` table where customers can review products, what type of relationship exists between:
- customers and reviews?
- products and reviews?
- customers and products (through reviews)?

---

## Part 3: Schema Creation (20 points)

**Q8.** Write CREATE TABLE statements for an `orders` table with:
- `order_id` as primary key
- `customer_id` as foreign key referencing customers
- `order_date` (DATE, not null)
- `status` (VARCHAR, must be one of: 'processing', 'shipped', 'completed', 'cancelled')
- `total_amount` (DECIMAL, must be positive)

```sql
-- Your CREATE TABLE here
```

**Q9.** Write a CREATE TABLE for an `order_items` junction table with:
- `order_id` (FK to orders)
- `product_id` (FK to products)
- `quantity` (integer, must be > 0)
- `unit_price` (decimal)
- Composite primary key of (order_id, product_id)

```sql
-- Your CREATE TABLE here
```

**Q10.** Insert 3 sample rows into your `orders` table and 5 sample rows into `order_items`. Verify with SELECT queries.

```sql
-- Your INSERT and SELECT statements here
```

---

## Part 4: Referential Integrity (10 points)

**Q11.** Try inserting an order with a `customer_id` that does not exist in the `customers` table. What happens?

```sql
-- Your query here (explain the result)
```

**Q12.** Write a query that checks if there are any products with a `category_id` that does not exist in the `categories` table.

```sql
-- Your query here
```

---

## Part 5: ER Diagram (15 points)

**Q13.** Draw an ER diagram (on paper or using text/ASCII art) for a **University Registration System** with the following entities:
- Students (student_id, name, email, major)
- Courses (course_id, title, credits, department)
- Enrollments (student_id, course_id, semester, grade)
- Instructors (instructor_id, name, department)

Include:
- Primary keys for each table
- Foreign keys showing relationships
- Cardinality labels (1:1, 1:M, or M:M)

---

## Part 6: Challenge (5 bonus points)

**Q14.** Design a schema (CREATE TABLE statements) for a simple **music streaming service** with at least 4 tables. Include at least one M:M relationship with a junction table. Draw the ER diagram.

---

## Submission

- Submit your notebook with all queries, outputs, and ER diagrams
- For diagram questions, include a photo/scan of hand-drawn diagrams or ASCII art

**Total: 75 points (+ 5 bonus)**

