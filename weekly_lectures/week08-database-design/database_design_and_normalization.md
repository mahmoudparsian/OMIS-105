---
title: OMIS 105 - Week 8 (Database Design & Normalization)
author: Dr. Mahmoud Parsian
marp: true
theme: default
paginate: true
class: lead
footer: "OMIS 105 – Week 8: Database Design & Normalization"
style: |
  section {
    justify-content: flex-start;
  }
---

# OMIS 105  
## Week 8: Database Design & Normalization

### 1. What is DATABASE DESIGN?

### 2. What is DATABASE NORMALIZATION?

---

## Database Design & Normalization

	**DATABASE DESIGN** is the process of planning 
	and structuring how data is stored, organized, 
	and connected in a database. 

	**DATABASE NORMALIZATION** is a key part of 
	that design process — it breaks down large, 
	messy tables into smaller, well-organized tables 
	to reduce duplicate data and prevent errors.

---

# This Week's Goals

1. Understand functional dependencies
2. Identify and fix anomalies
3. Apply normal forms: 1NF, 2NF, 3NF
4. Normalize real data (ShopSmart) with SQL
5. Know when to denormalize

---

# Agenda

**Session 1 — Ideas**
- Why database design matters
- Bad vs. good table design, and anomalies
- Functional dependencies
- 1NF, 2NF, 3NF

**Session 2 — Practice**
- Normalizing ShopSmart step by step, in SQL
- Denormalization: when to break the rules
- Design patterns and hands-on design

---

# Recap

- JOINs connect tables through keys  

👉 Today: How do we decide **which tables** to create in the first place?

---

# Session 1: Why Design Matters

---

# Why Design Matters

Bad design leads to:

- Data duplication ❌  
- Inconsistent data ❌  
- Errors when adding, changing, or deleting data ❌  

Good design leads to:

- Clean data ✅  
- Easy updates ✅  
- Reliable queries ✅  

---

# Bad Table Example

| order_id | customer_name | customer_email | product | price |
|----------|--------------|----------------|---------|-------|
| 1        | Alice        | alice@mail.com | Laptop  | 1000  |
| 2        | Alice        | alice@mail.com | Phone   | 800   |
| 3        | Bob          | bob@mail.com   | Laptop  | 1000  |

One table stores **three different things**: customers, products, and orders.

---

# Problem #1: Duplication (Redundancy)

- Alice's name and email appear in **every** order she places
- The Laptop's price appears in **every** order that contains it

👉 Wasted space — and every copy is a chance for a mistake

---

# Problem #2: Update Anomaly

Alice changes her email:

- We must update **every** row with her name ❌  
- Miss one row → two different emails for one person ❌  

An **anomaly** is an error caused by the table design, not by the user.

---

# Problem #3: Insert and Delete Anomalies

- **Insert:** we cannot add a new customer until they place an order ❌  
- **Delete:** if we delete Bob's only order, we lose Bob's email too ❌  

---

# The Four Problems, in One Table

| Problem | What goes wrong |
|---------|-----------------|
| **Redundancy** | The same fact is stored many times |
| **Update anomaly** | Changing one fact needs many updates |
| **Insertion anomaly** | We cannot add a fact without some unrelated fact |
| **Deletion anomaly** | Deleting one fact loses an unrelated fact |

Normalization removes these problems step by step.

---

# What is Normalization?

**Normalization** is a step-by-step process for splitting tables so that:

👉 each fact is stored **once**  
👉 each table describes **one thing** (customers, products, orders, ...)  

Result: less redundancy, fewer anomalies, more consistent data.

---

# Functional Dependency (FD)

**A → B** means: "If I know A, I know B."  
(A *determines* B.)

Examples:

- `customer_id → customer_name` (one ID, one name)
- `product_id → price` (one product, one price)
- `customer_name → customer_id`? ❌ No — two customers can have the same name

An FD is a **rule about the business**, not just about today's data.
The data can show that an FD is broken, but it cannot prove that it always holds.

The normal forms are rules about these dependencies.

---

# Types of FDs

| Type | Notation | Example |
|------|----------|---------|
| Full FD | Y depends on the **whole** key | `(order_id, product_id) → quantity` |
| Partial FD | **Part** of the key → Y | `order_id → order_date`, when the key is `(order_id, product_id)` |
| Transitive FD | Key → non-key → Z | `product_id → category_id → category_name` |

Partial FDs break **2NF**. Transitive FDs break **3NF**.

---

# First Normal Form (1NF)

A table is in 1NF if:
1. Each cell holds **one** value (atomic) — no lists
2. There are no **repeating groups** (`phone1`, `phone2`, ...)
3. Each row is **unique** (there is a primary key)

Also: each column has one name and a **single data type**.
(Textbooks state 1NF in slightly different ways; rules 1 and 2 are the core.)

---

# 1NF Violation: A List in a Cell

| order_id | products | quantities |
|----------|----------|------------|
| 1 | Laptop, Mouse | 1, 2 |
| 2 | Keyboard | 1 |

**Problem**: `products` and `quantities` contain multiple values.

**Fix**: One row per product (key: `order_id` + `product`):

| order_id | product | quantity |
|----------|---------|----------|
| 1 | Laptop | 1 |
| 1 | Mouse | 2 |
| 2 | Keyboard | 1 |

---

# 1NF Violation: Repeating Columns

| customer_id | name | phone1 | phone2 | phone3 |
|------------|------|--------|--------|--------|
| 1 | Alice | 555-1234 | 555-5678 | NULL |

**Problem**: Repeating group (phone1, phone2, phone3).

**Fix**: One row per phone:

| customer_id | name  |phone |
|------------|-------|------|
| 1 | Alice | 555-1234 |
| 1 | Alice | 555-5678 |

---

# Second Normal Form (2NF)

A table is in 2NF if:
1. It is in 1NF
2. **No partial dependencies** — every non-key column depends on the **entire** primary key

Only relevant when the PK is **composite** (two or more columns).
A 1NF table with a one-column key is **automatically** in 2NF.

---

# 2NF Violation Example

Table: `order_items_bad`
PK: (order_id, product_id)

| order_id | product_id | quantity | order_date | product_name |
|----------|-----------|----------|-----------|-------------|
| 1 | 5 | 2 | 2024-01-15 | Tablet Air |

- `order_date` depends only on `order_id` → **partial dependency**
- `product_name` depends only on `product_id` → **partial dependency**
- `quantity` depends on (order_id, product_id) → **full dependency** ✓

---

# Intuition for 2NF

Ask:
👉 “Does this column depend on the **whole** key, or only part of it?”

If only part → move it to the table where that part is the key.

---

# Fixing 2NF

Split into three tables:

**orders**: (order_id, order_date)
**products**: (product_id, product_name)
**order_items**: (order_id, product_id, quantity)

Now every non-key column depends on the full PK of its table.

---

# Third Normal Form (3NF)

A table is in 3NF if:
1. It is in 2NF
2. **No transitive dependencies** — non-key columns do not depend on other non-key columns

---

# 3NF Violation Example

| product_id | product_name | category_id | category_name |
|-----------|-------------|------------|--------------|
| 1 | Smartphone X12 | 1 | Electronics |
| 2 | Laptop Pro 15 | 1 | Electronics |

- `product_id → category_id` ✓
- `category_id → category_name` (transitive!) ✗

`category_name` depends on the key only **through** `category_id`,
a column that is **not** the key.

---

# Intuition for 3NF

Ask:
👉 “Does this column depend on **another non-key column**?”

If yes → move it to a table where that column is the key.

A popular summary of 1NF–3NF: every non-key column must depend on
**the key, the whole key, and nothing but the key.**

---

# Fixing 3NF

Split:

**products**: (product_id, product_name, category_id)
**categories**: (category_id, category_name)

Now no non-key column depends on another non-key column.

---

# Normal Form Summary

| NF | Requirement | Eliminates |
|----|-------------|-----------|
| 1NF | Atomic values, no repeating groups, a key | Multi-valued attributes |
| 2NF | No partial dependencies | Partial key deps (composite PKs) |
| 3NF | No transitive dependencies | Non-key → non-key deps |

---

# Putting It Together: A Small Example

Starting table:

| order_id | customer_name | customer_email | product | price |

Step 1: Find the "things" (entities): **customers**, **products**, **orders**

Step 2: Give each one a table and a primary key

Step 3: Link them with foreign keys

Step 4: An order can contain many products → add an **order_items** table

---

# Good Design (Final)

customers(**customer_id**, name, email)

products(**product_id**, product_name, price)

orders(**order_id**, customer_id → customers, order_date)

order_items(**order_id** → orders, **product_id** → products, quantity)

👉 Each fact is stored once. JOINs bring the data back together.
Change Alice's email in **one** row.

---

# Session 2: Normalization in Practice

---

# Normalization Step by Step

1. List all attributes
2. Identify the candidate key(s)
3. List all functional dependencies
4. Check 1NF → fix if needed
5. Check 2NF → decompose partial deps
6. Check 3NF → decompose transitive deps

At every step, ask:
👉 “What **thing** does this column describe? Does it belong in another table?”

---

# Hands-On: Normalizing ShopSmart

Starting table: `orders_denormalized` (100 rows)

```
order_id, order_date, status,
customer_id, customer_name, customer_email, customer_city,
product_id, product_name, category_name, unit_price,
quantity, line_price
```

Load it (from the `week08-database-design` folder):

```sql
CREATE OR REPLACE TABLE orders_denormalized AS
SELECT * FROM read_csv('data/orders_denormalized.csv');
```

Let's normalize this step by step.

---

# The Denormalized Disaster

Some columns of `orders_denormalized`:

| order_id | order_date | customer_id | customer_name | customer_email | product_name | category_name | quantity |
|----------|-----------|------------|--------------|----------------|-------------|---------------|----------|
| 17 | 2024-07-18 | 1 | Alice Smith | alice.smith@email.com | Nail Kit | Beauty | 4 |
| 17 | 2024-07-18 | 1 | Alice Smith | alice.smith@email.com | Running Shoes | Clothing | 2 |
| 17 | 2024-07-18 | 1 | Alice Smith | alice.smith@email.com | Bookshelf | Home & Kitchen | 2 |

**Alice's information is repeated 3 times — and the order's date too!**
(Customer Gina Turner appears in 15 rows.)

---

# Anomalies in Action

**Update anomaly**: Alice changes email → must update every row she appears in.

**Insertion anomaly**: New customer, no orders yet → can't add them (`order_id` is part of the key, and a key cannot be `NULL`).

**Deletion anomaly**: Delete Alice's only order → lose her customer info entirely.

---

# Step 1: Identify FDs

```
order_id → order_date, status, customer_id
customer_id → customer_name, customer_email, customer_city
product_id → product_name, category_name, unit_price
(order_id, product_id) → quantity
```

Candidate key: (order_id, product_id)

(The CSV also has a `line_price` column, but it is always equal to
`unit_price` — it is **not** quantity × price. So it is a copy of
`unit_price` and depends on `product_id` alone. We drop it.)

---

# Checking an FD with SQL

Does `customer_id → customer_email` hold in the data?
Look for any customer with **more than one** email:

```sql
SELECT customer_id, COUNT(DISTINCT customer_email) AS emails
FROM orders_denormalized
GROUP BY customer_id
HAVING COUNT(DISTINCT customer_email) > 1;
-- 0 rows → no violations
```

Does `customer_city → customer_id` hold? No:

```sql
SELECT customer_city, COUNT(DISTINCT customer_id) AS customers
FROM orders_denormalized
GROUP BY customer_city
HAVING COUNT(DISTINCT customer_id) > 1
ORDER BY customers DESC;
-- Boston has 5 customers, Portland 4, ...
```

---

# Step 2: Check 1NF

- All values are atomic ✓
- No repeating groups ✓
- Has a primary key (order_id, product_id) ✓

**Already in 1NF.**

---

# Step 3: Check 2NF

Partial dependencies on composite key (order_id, product_id):
- `order_id → order_date, status, customer_id` (partial)
- `product_id → product_name, category_name, unit_price` (partial)

**NOT in 2NF.** Decompose:
- **orders**(order_id, order_date, status, customer_id)
- **products**(product_id, product_name, category_name, unit_price)
- **order_items**(order_id, product_id, quantity)

`unit_price` goes to **products**: it depends on `product_id` alone.

---

# Step 4: Check 3NF

In **orders**: `order_id → customer_id → customer_name, customer_email, customer_city`
- Transitive dependency through customer_id!

In **products**: `category_name` is repeated for every product in the category.
- Strictly, `product_id → category_name` is direct (there is no `category_id` column yet).
- But a category is its own "thing": we cannot store a category with no products,
  and renaming one means updating many rows.
- Fix: create a **categories** table with a new key, `category_id`.
  Then `product_id → category_id → category_name` would be transitive, so
  `category_name` moves to `categories`.

---

# Step 5: Fix 3NF

Final decomposition:
- **customers**(customer_id, customer_name, customer_email, customer_city)
- **categories**(category_id, category_name)
- **products**(product_id, product_name, category_id, unit_price)
- **orders**(order_id, order_date, status, customer_id)
- **order_items**(order_id, product_id, quantity)

**This is our ShopSmart schema!** The real CSV files differ only slightly:
`customers` splits the name into `first_name`/`last_name` and adds `state`
and `join_date`; `order_items` has its own `item_id` key and **also** keeps
`unit_price` — on purpose (see the final schema slide).

---

# Building the Normalized Tables in SQL

```sql
CREATE OR REPLACE TABLE n_customers AS
SELECT DISTINCT customer_id, customer_name, customer_email, customer_city
FROM orders_denormalized;                                   -- 20 rows

CREATE OR REPLACE TABLE n_categories AS
SELECT ROW_NUMBER() OVER (ORDER BY category_name) AS category_id, category_name
FROM (SELECT DISTINCT category_name FROM orders_denormalized);  -- 8 rows

CREATE OR REPLACE TABLE n_products AS
SELECT DISTINCT d.product_id, d.product_name, c.category_id, d.unit_price
FROM orders_denormalized d
JOIN n_categories c USING (category_name);                  -- 51 rows

CREATE OR REPLACE TABLE n_orders AS
SELECT DISTINCT order_id, order_date, status, customer_id
FROM orders_denormalized;                                   -- 30 rows

CREATE OR REPLACE TABLE n_order_items AS
SELECT order_id, product_id, quantity
FROM orders_denormalized;                                   -- 100 rows
```

`SELECT DISTINCT` keeps one copy of each repeated fact.
JOINing the five tables back together returns all 100 original rows —
**no information was lost**.

---

# Denormalization: When to Break the Rules

Sometimes **controlled redundancy** improves performance:

| Scenario | Strategy |
|----------|----------|
| Frequent JOINs are slow | Store computed totals |
| Read-heavy, write-light | Duplicate for speed |
| Reporting/analytics | Summary tables, or materialized views (in databases that have them, e.g. PostgreSQL) |
| Caching | Precomputed summaries |

---

# Denormalization Example

Instead of joining orders + order_items every time:

```sql
-- Add a computed column to orders
ALTER TABLE orders ADD COLUMN item_count INTEGER;
ALTER TABLE orders ADD COLUMN computed_total DECIMAL(10,2);

-- Keep it updated with application logic
-- (some databases also offer triggers; DuckDB does not)
```

Trade-off: faster reads, but risk of inconsistency.

**Real example:** ShopSmart's `orders.total_amount` is a stored total like this.
In our practice data it does **not** match the sum of the order's
`order_items` — exactly the inconsistency denormalization can cause!

---

# When NOT to Denormalize

- Small datasets (JOINs are fast enough)
- Write-heavy systems (updates become complex)
- When data integrity is critical
- When you can use views or CTEs instead

**Rule of thumb**: Normalize first, denormalize only when performance demands it.

---

# Design Methodology Summary

```
Requirements → Conceptual Design (ER Diagram)
            → Logical Design (Tables + Constraints)
            → Normalization (1NF → 2NF → 3NF)
            → Physical Design (Indexes, Performance)
            → Implementation (CREATE TABLE, Load Data)
```

---

# Common Design Patterns

| Pattern | Structure | Use Case |
|---------|-----------|----------|
| Lookup table | (id, name, description) | Categories, statuses |
| Junction table | (fk1, fk2, attrs) | M:M (many-to-many) relationships |
| Audit trail | (id, entity_id, action, timestamp) | Change tracking |
| Hierarchy | (id, parent_id, name) | Org charts, categories |
| Temporal | (id, valid_from, valid_to, value) | Price history |

---

# ShopSmart: Final Normalized Schema

```
categories ──(1:M)──▶ products
customers  ──(1:M)──▶ orders
orders     ──(1:M)──▶ order_items
products   ──(1:M)──▶ order_items
products   ──(M:M)──▶ suppliers (via product_suppliers)
products   ──(1:M)──▶ reviews
customers  ──(1:M)──▶ reviews
```

Each table is in 3NF.

Two deliberate exceptions:
- `order_items.unit_price` copies `products.price` — on purpose, to record
  the price **at the time of the order** (prices change later).
- `orders.total_amount` is a stored (denormalized) total.

---

# Mental Model

Tables = things (entities)  
Columns = facts about those things (attributes)  
Primary keys = identity  
Foreign keys = relationships  

👉 Design first, then query

---

# Common Mistakes

- Keeping everything in one big table ❌  
- Linking tables by names instead of IDs ❌ (names can repeat and change)  
- Splitting too much: a table for every column ❌  

---

# In-Class Exercise

You get one messy table (all data in one place).

Your job:
- Find the duplicated data and the anomalies
- List the functional dependencies
- Split it into tables, each with a primary key
- Connect the tables with foreign keys

---

# Hands-On Labs

**Lab 1 — design and 1NF**
- Find the 1NF problems (lists in a cell, repeating columns)
- Split them into rows with SQL
- Choose a primary key, and check it with SQL

**Lab 2 — 1NF and 2NF**
- Find the partial dependencies of a composite key
- Split the table into 2NF tables, then JOIN them back together

---

# Summary

- Bad design causes duplication and anomalies  
- **Functional dependencies** (X → Y) tell us where each column belongs  
- **1NF**: one value per cell, no repeating groups, a key  
- **2NF**: depend on the **whole** key (no partial dependencies)  
- **3NF**: depend on **nothing but** the key (no transitive dependencies)  
- **Normalize first**, then denormalize only when needed  

👉 Design is as important as SQL

---

# What’s Next?

**Week 9: Ranking Functions**
- `ROW_NUMBER`, `RANK`, `DENSE_RANK`
- Ranking within groups (`PARTITION BY`)
- Top-N and "second-highest" questions

---

# Read More

- `1nf_guide.md` and `1nf_examples.md` — First Normal Form, step by step
- `2nf_guide.md` and `2nf_examples.md` — Second Normal Form
- `3nf_guide.md` and `3nf_examples.md` — Third Normal Form
- `marimo_design_1nf_2nf.py` — design, 1NF, and 2NF in a Marimo notebook
- Optional appendix (end of this deck): BCNF, a stricter form of 3NF

---

# Final Thought

Good databases are designed carefully.

👉 Think before you build.

**Let’s design! 🚀**

---

# Optional Appendix: Going Further

**Boyce-Codd Normal Form (BCNF)**

For curious students only — **not on the exams**.
In this course, normalization stops at **3NF**.

---

# Optional: Boyce-Codd Normal Form (BCNF)

A table is in BCNF if:
- For every FD X → Y, X is a **superkey**

A **superkey** is any set of columns that uniquely identifies a row
(a key, or a key plus extra columns).

BCNF is stricter than 3NF. A table in 3NF can fail BCNF only when it has
two or more **overlapping candidate keys** — this is rare in practice.

---

# Optional: BCNF Example

| student | subject | professor |
|---------|---------|-----------|
| Alice | Math | Dr. Smith |
| Bob | Math | Dr. Smith |
| Alice | Physics | Dr. Jones |

FDs:
- (student, subject) → professor
- professor → subject (each prof teaches one subject)

Candidate keys: `(student, subject)` and `(student, professor)` — they overlap on `student`.

`professor → subject` violates BCNF because `professor` alone is not a superkey.
(The table **is** in 3NF, because `subject` is part of a candidate key.)

---

# Optional: Fixing BCNF

**professor_subjects**: (professor, subject)
**student_professors**: (student, professor)

Now every determinant is a superkey in its table.

Trade-off: the rule *"a student has one professor per subject"* can no longer
be checked inside a single table. BCNF sometimes costs a dependency.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
