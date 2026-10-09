---
title: OMIS 105 - Week 6 (Database Design & Normalization)
author: Dr. Mahmoud Parsian
marp: true
theme: default
paginate: true
class: lead
style: |
  section {
    justify-content: flex-start;
  }
---

# OMIS 105  
## Week 6: Database Design & Normalization

---

# Agenda

- Why database design matters
- Bad vs. good table design
- Functional dependencies (the intuition)
- Normalization: 1NF, 2NF, 3NF
- Step-by-step normalization
- Hands-on design

---

# Recap

- JOINs connect tables through keys  

👉 Today: How do we decide **which tables** to create in the first place?

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

# What is Normalization?

**Normalization** is a step-by-step process for splitting tables so that:

👉 each fact is stored **once**  
👉 each table describes **one thing** (customers, products, orders, ...)  

Result: less redundancy, fewer anomalies, more consistent data.

---

# Functional Dependency (Simple View)

**A → B** means: "If I know A, I know B."  
(A *determines* B.)

Examples:
- `customer_id → customer_name` (one ID, one name)
- `product_id → price` (one product, one price)
- `customer_name → customer_id`? ❌ No — two customers can have the same name

The normal forms are rules about these dependencies.

---

# First Normal Form (1NF)

Rules:
- Each cell holds **one** value (atomic) — no lists
- No repeating groups (like `phone1`, `phone2`, `phone3`)
- Each row can be identified by a key

❌ Bad:
| order_id | products |
|----|----------|
| 1  | Laptop, Phone |

✅ Good:
| order_id | product |
|----|---------|
| 1  | Laptop |
| 1  | Phone |

---

# Second Normal Form (2NF)

Goal:
👉 Remove **partial dependencies**

It only matters when the key has **two or more columns** (a composite key).

Example: `order_items(order_id, product_id, quantity, product_name)`
- Key = `(order_id, product_id)`
- `quantity` depends on the **whole** key ✅ (how many of *this* product in *this* order)
- `product_name` depends only on `product_id` — **part** of the key ❌

Fix: move `product_name` to a `products` table.

---

# Intuition for 2NF

Ask:
👉 “Does this column depend on the **whole** key, or only part of it?”

If only part → move it to the table where that part is the key.

---

# Third Normal Form (3NF)

Goal:
👉 Remove **transitive dependencies** (A → B → C)

Example: `orders(order_id, customer_id, customer_name, customer_city)`

- `order_id → customer_id` ✅
- `customer_id → customer_name, customer_city` ❌

`customer_name` depends on the key only **through** `customer_id`,
a column that is **not** the key.

Fix: move `customer_name` and `customer_city` to a `customers` table.

---

# Intuition for 3NF

Ask:
👉 “Does this column depend on **another non-key column**?”

If yes → split it into its own table.

A popular summary of 1NF–3NF: every non-key column must depend on
**the key, the whole key, and nothing but the key.**

---

# Step-by-Step Normalization

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

---

# Why This Matters

Normalization ensures:

- No duplicate facts  
- Clear relationships  
- Reliable updates (change Alice's email in **one** row)  

---

# Real-World Thinking

Ask:

👉 “What **thing** does this column describe?”

👉 “Does it belong in another table?”

---

# In-Class Exercise

You get one messy table (all data in one place).

Your job:
- Find the duplicated data and the anomalies
- List the functional dependencies
- Split it into tables, each with a primary key
- Connect the tables with foreign keys

---

# Common Mistakes

- Keeping everything in one big table ❌  
- Linking tables by names instead of IDs ❌ (names can repeat and change)  
- Splitting too much: a table for every column ❌  

---

# Mental Model

Tables = things (entities)  
Columns = facts about those things (attributes)  
Primary keys = identity  
Foreign keys = relationships  

👉 Design first, then query

---

# Hands-On Lab

- Identify bad design  
- Normalize into 3–4 tables  
- Define primary keys  
- Define foreign keys  

---

# Summary

- Bad design causes duplication and anomalies  
- Functional dependencies tell us where each column belongs  
- 1NF: one value per cell  
- 2NF: depend on the whole key  
- 3NF: depend on nothing but the key  

👉 Design is as important as SQL

---

# What’s Next?

Week 7: Query performance
- Window functions (ROW_NUMBER, RANK)
- CTEs
- EXPLAIN and indexes

---

# Final Thought

Good databases are designed carefully.

👉 Think before you build.

---

# Let’s Design 🚀

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
