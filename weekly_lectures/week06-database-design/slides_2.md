---
marp: true
theme: default
paginate: true
header: "OMIS 105 – Database Management Systems"
footer: "Week 6: Normalization & Design"
---

# OMIS 105: Database Management Systems
## Week 6 — Database Design & Normalization
### Functional Dependencies, 1NF through BCNF

---

# This Week's Goals

1. Understand functional dependencies
2. Identify and fix anomalies
3. Apply normal forms: 1NF, 2NF, 3NF, BCNF
4. Know when to denormalize
5. Practice normalizing real data

---

# Why Normalization?

Poor database design causes:
- **Redundancy** — same data stored multiple times
- **Update anomaly** — changing one fact requires multiple updates
- **Insertion anomaly** — can't add data without unrelated data
- **Deletion anomaly** — deleting data loses unrelated facts

Normalization removes these problems step by step.

---

# Session 1: Functional Dependencies & Normal Forms

---

# Functional Dependency (FD)

**X → Y** means: "If you know X, you can determine Y."

Example in `products`:
- `product_id → product_name` (knowing the ID determines the name)
- `product_id → price` (knowing the ID determines the price)
- `product_name → price`? **Not guaranteed** — two products could share a name

An FD is a **rule about the business**, not just about today's data.
The data can show that an FD is broken, but it cannot prove that it always holds.

---

# Types of FDs

| Type | Notation | Example |
|------|----------|---------|
| Full FD | Y depends on the **whole** key | `(order_id, product_id) → quantity` |
| Partial FD | Part of key → Y | In `order_items(order_id, product_id, quantity, order_date)`, `order_id → order_date` depends on only part of the key `(order_id, product_id)` |
| Transitive FD | Key → non-key → Z | `product_id → category_id → category_name` |

---

# Finding FDs

Ask: "If I know the value of X, is Y uniquely determined?"

```
orders_denormalized:
  order_id → order_date, status, customer_id
  customer_id → customer_name, customer_email, customer_city
  product_id → product_name, category_name, unit_price
  (order_id, product_id) → quantity
```

(Our CSV also has a `line_price` column, but it is always equal to
`unit_price` — it is **not** quantity × price. So it is a copy of
`unit_price` and depends on `product_id` alone. We drop it.)

---

# The Denormalized Disaster

Consider our `orders_denormalized` table (`data/orders_denormalized.csv`,
100 rows; some columns hidden):

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

# First Normal Form (1NF)

A table is in 1NF if:
1. All columns contain **atomic** (indivisible) values
2. Each column has a **single data type**
3. Each row is **unique** (has a primary key)
4. No **repeating groups**

(Textbooks state 1NF in slightly different ways; rules 1 and 4 are the core.)

---

# 1NF Violations

| order_id | products | quantities |
|----------|----------|------------|
| 1 | Laptop, Mouse | 1, 2 |
| 2 | Keyboard | 1 |

**Problem**: `products` and `quantities` contain multiple values.

**Fix**: One row per product:

| order_id | product | quantity |
|----------|---------|----------|
| 1 | Laptop | 1 |
| 1 | Mouse | 2 |
| 2 | Keyboard | 1 |

---

# Another 1NF Violation

| customer_id | name | phone1 | phone2 | phone3 |
|------------|------|--------|--------|--------|
| 1 | Alice | 555-1234 | 555-5678 | NULL |

**Problem**: Repeating group (phone1, phone2, phone3).

**Fix**: Separate phone table:

| customer_id | phone |
|------------|-------|
| 1 | 555-1234 |
| 1 | 555-5678 |

---

# Second Normal Form (2NF)

A table is in 2NF if:
1. It is in 1NF
2. **No partial dependencies** — every non-key column depends on the **entire** primary key

Only relevant when the PK is **composite** (multiple columns).

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

# Fixing 2NF

Split into three tables:

**orders**: (order_id, order_date)
**products**: (product_id, product_name)
**order_items**: (order_id, product_id, quantity)

Now every non-key attribute depends on the full PK of its table.

---

# Third Normal Form (3NF)

A table is in 3NF if:
1. It is in 2NF
2. **No transitive dependencies** — non-key columns do not depend on other non-key columns

In short: every non-key column depends on **the key, the whole key, and nothing but the key.**

---

# 3NF Violation Example

| product_id | product_name | category_id | category_name |
|-----------|-------------|------------|--------------|
| 1 | Smartphone X12 | 1 | Electronics |
| 2 | Laptop Pro 15 | 1 | Electronics |

- `product_id → category_id` ✓
- `category_id → category_name` (transitive!) ✗

`category_name` depends on `category_id`, not directly on `product_id`.

---

# Fixing 3NF

Split:

**products**: (product_id, product_name, category_id)
**categories**: (category_id, category_name)

Now no non-key column transitively depends on another non-key column.

---

# Boyce-Codd Normal Form (BCNF)

A table is in BCNF if:
- For every FD X → Y, X is a **superkey**

A **superkey** is any set of columns that uniquely identifies a row
(a key, or a key plus extra columns).

BCNF is stricter than 3NF. A table in 3NF can fail BCNF only when it has
two or more **overlapping candidate keys** — this is rare in practice.

---

# BCNF Example

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

# Fixing BCNF

**professor_subjects**: (professor, subject)
**student_professors**: (student, professor)

Now every determinant is a superkey in its table.

Trade-off: the rule *"a student has one professor per subject"* can no longer
be checked inside a single table. BCNF sometimes costs a dependency.

---

# Session 2: Normalization in Practice

---

# Normal Form Summary

| NF | Requirement | Eliminates |
|----|-------------|-----------|
| 1NF | Atomic values, no repeating groups | Multi-valued attributes |
| 2NF | No partial dependencies | Partial key deps (composite PKs) |
| 3NF | No transitive dependencies | Non-key → non-key deps |
| BCNF | Every determinant is a superkey | Remaining FD-based anomalies |

---

# Normalization Step by Step

1. List all attributes
2. Identify the candidate key(s)
3. List all functional dependencies
4. Check 1NF → fix if needed
5. Check 2NF → decompose partial deps
6. Check 3NF → decompose transitive deps
7. Check BCNF → decompose if needed

---

# Hands-On: Normalizing ShopSmart

Starting table: `orders_denormalized`

```
order_id, order_date, status,
customer_id, customer_name, customer_email, customer_city,
product_id, product_name, category_name, unit_price,
quantity, line_price
```

Load it (from the `week06-database-design` folder):

```sql
CREATE OR REPLACE TABLE orders_denormalized AS
SELECT * FROM read_csv('data/orders_denormalized.csv');
```

Let's normalize this step by step.

---

# Step 1: Identify FDs

```
order_id → order_date, status, customer_id
customer_id → customer_name, customer_email, customer_city
product_id → product_name, category_name, unit_price
(order_id, product_id) → quantity
```

Candidate key: (order_id, product_id)

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
HAVING COUNT(DISTINCT customer_id) > 1;
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
- **order_items**(order_id, product_id, quantity, unit_price)

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
- **order_items**(order_id, product_id, quantity, unit_price)

**This is our ShopSmart schema!** The real CSV files differ only slightly:
`customers` splits the name into `first_name`/`last_name` and adds `state`
and `join_date`; `order_items` has its own `item_id` key.

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
SELECT order_id, product_id, quantity, unit_price
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

**Real example:** our `orders.total_amount` is a stored total like this.
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
            → Normalization (1NF → 2NF → 3NF → BCNF)
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

Each table is in 3NF (and BCNF).

Two deliberate exceptions:
- `order_items.unit_price` copies `products.price` — on purpose, to record
  the price **at the time of the order** (prices change later).
- `orders.total_amount` is a stored (denormalized) total.

---

# Summary

- **Functional dependencies** (X → Y) drive normalization
- **1NF**: Atomic values, no repeating groups
- **2NF**: No partial dependencies on composite keys
- **3NF**: No transitive dependencies
- **BCNF**: Every determinant is a superkey
- **Denormalization**: Controlled redundancy for performance
- Always **normalize first**, then selectively denormalize

---

# What Is Next?

**Week 7: Query Performance**
- Window functions (ROW_NUMBER, RANK)
- CTEs
- EXPLAIN and query plans
- Indexes

---

# Questions?

Thank you!

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
