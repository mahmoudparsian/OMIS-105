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

Normalization systematically removes these problems.

---

# Session 1: Functional Dependencies & Normal Forms

---

# Functional Dependency (FD)

**X → Y** means: "If you know X, you can determine Y."

Example in `products`:
- `product_id → product_name` (knowing the ID determines the name)
- `product_id → price` (knowing the ID determines the price)
- `product_name → price`? **Maybe not** (two products could share a name)

---

# Types of FDs

| Type | Notation | Example |
|------|----------|---------|
| Full FD | X → Y | `product_id → product_name` |
| Partial FD | Part of key → Y | In (order_id, product_id) → quantity: `order_id → order_date` depends on only part of key |
| Transitive FD | X → Y → Z | `product_id → category_id → category_name` |

---

# Finding FDs

Ask: "If I know the value of X, is Y uniquely determined?"

```
orders_denormalized:
  order_id → order_date, status
  customer_id → customer_name, customer_email, customer_city
  product_id → product_name, category_name, unit_price
  (order_id, product_id) → quantity, line_price
```

---

# The Denormalized Disaster

Consider our `orders_denormalized` table:

| order_id | order_date | customer_id | customer_name | customer_email | product_id | product_name | category_name | quantity |
|----------|-----------|------------|--------------|----------------|-----------|-------------|---------------|----------|
| 1 | 2024-01-15 | 1 | Alice Smith | alice@email.com | 5 | Tablet Air | Electronics | 2 |
| 1 | 2024-01-15 | 1 | Alice Smith | alice@email.com | 12 | SQL Cookbook | Books | 1 |
| 2 | 2024-01-20 | 1 | Alice Smith | alice@email.com | 5 | Tablet Air | Electronics | 1 |

**Alice's info repeated 3 times!**

---

# Anomalies in Action

**Update anomaly**: Alice changes email → must update every row she appears in.

**Insertion anomaly**: New customer, no orders yet → can't add them (order_id is part of key).

**Deletion anomaly**: Delete Alice's only order → lose her customer info entirely.

---

# First Normal Form (1NF)

A table is in 1NF if:
1. All columns contain **atomic** (indivisible) values
2. Each column has a **single data type**
3. Each row is **unique** (has a primary key)
4. No **repeating groups**

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

Stricter than 3NF. Differences only arise with overlapping candidate keys.

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

`professor → subject` violates BCNF because `professor` is not a superkey.

---

# Fixing BCNF

**professor_subjects**: (professor, subject)
**student_professors**: (student, professor)

Now every determinant is a superkey in its table.

---

# Session 2: Normalization in Practice

---

# Normal Form Summary

| NF | Requirement | Eliminates |
|----|-------------|-----------|
| 1NF | Atomic values, no repeating groups | Multi-valued attributes |
| 2NF | No partial dependencies | Partial key deps (composite PKs) |
| 3NF | No transitive dependencies | Non-key → non-key deps |
| BCNF | Every determinant is a superkey | All remaining anomalies |

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

Let's normalize this step by step.

---

# Step 1: Identify FDs

```
order_id → order_date, status
customer_id → customer_name, customer_email, customer_city
product_id → product_name, category_name, unit_price
(order_id, product_id) → quantity, line_price
order_id → customer_id
```

Candidate key: (order_id, product_id)

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
- **order_items**(order_id, product_id, quantity, line_price)

---

# Step 4: Check 3NF

In **orders**: `order_id → customer_id → customer_name, customer_email, customer_city`
- Transitive dependency through customer_id!

In **products**: `product_id → category_name` through a conceptual category_id
- Transitive dependency!

---

# Step 5: Fix 3NF

Final decomposition:
- **customers**(customer_id, customer_name, customer_email, customer_city)
- **categories**(category_id, category_name)
- **products**(product_id, product_name, category_id, unit_price)
- **orders**(order_id, order_date, status, customer_id)
- **order_items**(order_id, product_id, quantity, line_price)

**This is exactly our ShopSmart schema!**

---

# Denormalization: When to Break the Rules

Sometimes **controlled redundancy** improves performance:

| Scenario | Strategy |
|----------|----------|
| Frequent JOINs are slow | Store computed totals |
| Read-heavy, write-light | Duplicate for speed |
| Reporting/analytics | Materialized views |
| Caching | Precomputed summaries |

---

# Denormalization Example

Instead of joining orders + order_items every time:

```sql
-- Add a computed column to orders
ALTER TABLE orders ADD COLUMN item_count INTEGER;
ALTER TABLE orders ADD COLUMN computed_total DECIMAL(10,2);

-- Keep it updated with triggers or application logic
```

Trade-off: faster reads, but risk of inconsistency.

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
| Junction table | (fk1, fk2, attrs) | M:M relationships |
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

Each table is in 3NF / BCNF. No redundancy. Full referential integrity.

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

**Week 7: Performance & Indexing**
- How queries execute
- Creating and using indexes
- EXPLAIN and query plans
- Query optimization techniques

---

# Questions?

Thank you!

