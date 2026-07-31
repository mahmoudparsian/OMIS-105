---
title: OMIS 105 - Week 6 (Flagship Expanded)
author: Instructor
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
- Bad vs good schema design
- Normalization (1NF, 2NF, 3NF)
- Functional dependencies (intuitive)
- Step-by-step normalization
- Hands-on design

---

# Recap

- JOIN connects tables  
👉 Today: How to design tables correctly

---

# Why Design Matters

Bad design leads to:

- Data duplication ❌  
- Inconsistency ❌  
- Update errors ❌  

Good design leads to:

- Clean data ✅  
- Easy updates ✅  
- Reliable queries ✅  

---

# Bad Table Example

| order_id | customer_name | product | price |
|----------|--------------|---------|-------|
| 1        | Alice        | Laptop  | 1000  |
| 2        | Alice        | Phone   | 800   |

---

# Problem #1: Duplication

- "Alice" appears multiple times  
👉 Wasteful + risky

---

# Problem #2: Update Anomaly

If Alice changes name:

- Must update many rows ❌  
- Risk inconsistency ❌  

---

# Problem #3: Insert/Delete Anomaly

- Cannot add customer without order ❌  
- Deleting order may remove customer ❌  

---

# What is Normalization?

Process of organizing data to:

👉 Reduce redundancy  
👉 Improve consistency  

---

# First Normal Form (1NF)

Rules:
- No repeating groups  
- Atomic values (no lists)

❌ Bad:
| id | products |
|----|----------|
| 1  | Laptop, Phone |

✅ Good:
| id | product |
|----|---------|
| 1  | Laptop |
| 1  | Phone |

---

# Second Normal Form (2NF)

Goal:
👉 Remove partial dependency

Applies when:
- Composite key exists

Example idea:
- Key = (order_id, product_id)
- Non-key depends only on part → BAD

---

# Intuition for 2NF

Ask:
👉 “Does this column depend on the whole key?”

If not → move it

---

# Third Normal Form (3NF)

Goal:
👉 Remove transitive dependency

Example:

| customer_id | customer_name | city |
|-------------|--------------|------|

If:
customer_id → customer_name  
customer_name → city  

👉 city should be separate

---

# Intuition for 3NF

Ask:
👉 “Does this depend on another non-key column?”

If yes → split table

---

# Step-by-Step Normalization

Starting table:

| order_id | customer_name | product | price |

Step 1:
Customers table  
Orders table  

Step 2:
Add keys

---

# Good Design (Final)

Customers:

| id | name |

Orders:

| id | customer_id | product | price |

👉 Connected via foreign key

---

# Functional Dependency (Simple View)

A → B means:
A determines B

Example:
customer_id → customer_name

---

# Why This Matters

Normalization ensures:

- No duplicate facts  
- Clear relationships  
- Reliable updates  

---

# Real-World Thinking

Ask:

👉 “Where should this data live?”

👉 “Does this belong in another table?”

---

# In-Class Exercise

Give students:

Messy table

Ask them to:
- Identify problems  
- Split into multiple tables  

---

# Common Mistakes

- Keeping everything in one table ❌  
- Using names instead of IDs ❌  
- Over-normalizing too early ❌  

---

# Mental Model

Tables = entities  
Columns = attributes  
Keys = relationships  

👉 Design first, then query

---

# Hands-On Lab

- Identify bad design  
- Normalize to 2–3 tables  
- Define primary keys  
- Define foreign keys  

---

# Summary

- Bad design causes real problems  
- Normalization organizes data  
- 1NF, 2NF, 3NF = cleaner structure  

👉 Design is as important as SQL

---

# What’s Next?

Week 7:
- Indexing
- Query performance

---

# Final Thought

Good databases are designed carefully.

👉 Think before you build.

---

# Let’s Design 🚀
