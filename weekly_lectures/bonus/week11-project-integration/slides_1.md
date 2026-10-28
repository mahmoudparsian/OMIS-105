---
title: OMIS 105 - Week 9 (Project & Integration)
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
## Week 9: Project & Integration (Build a Real System)

---

# Agenda

- Why projects matter
- What you are building
- Project requirements
- Step-by-step guide
- Example project
- Common mistakes
- Grading expectations

---

# Recap

- You learned:
  - SQL (SELECT, WHERE, JOIN, GROUP BY, CTEs, window functions)
  - Design (normalization)
  - Performance (indexing)
  - Reliability (transactions and constraints)

👉 Today: Put EVERYTHING together

---

# Why This Project Matters

This is where you move from:

❌ “I learned SQL”  
to  
✅ “I can build a database system”

---

# What You Will Build

A **mini database system**:

- Schema (tables)
- Relationships (keys)
- Data (realistic)
- Queries (analysis)
- A transaction (reliability)

---

# Project Requirements

Minimum (full details: `lab09_student.md`, the capstone specification):

- **5 tables**, in 3NF
- Primary keys and foreign keys
- At least one **many-to-many** relationship (with a junction table)
- **20+ rows** per main table
- **10** meaningful queries
- 2 views and 3 indexes
- 1 transaction demo

---

# Required Queries (10 in total)

| Category | How many |
|----------|----------|
| Basic SELECT (WHERE, ORDER BY) | 2 |
| JOINs (including a 3+ table JOIN) | 3 |
| GROUP BY (with HAVING or CASE) | 2 |
| Window functions or CTEs | 2 |
| Transaction (with error handling) | 1 |

---

# Choose a Domain

Pick something you understand:

- E-commerce
- Bookstore
- Food delivery
- Movie database
- Fitness gym

👉 Keep it manageable

---

# Example: E-commerce

Tables (this is our ShopSmart data):

- customers
- categories
- products
- orders
- order_items

---

# Example Schema

customers(**customer_id**, first_name, last_name, email)  
categories(**category_id**, category_name)  
products(**product_id**, product_name, category_id → categories, price)  
orders(**order_id**, customer_id → customers, order_date, status)  
order_items(**item_id**, order_id → orders, product_id → products, quantity, unit_price)

👉 `order_items` is the **junction table**: one order has many products,
and one product appears in many orders (many-to-many).

---

# Step 1: Design Tables

Ask:

👉 “What are the main entities (things)?”

👉 “How are they connected?” (one-to-many? many-to-many?)

---

# Step 2: Define Keys

- Primary keys (one per table)
- Foreign keys (one for each relationship)
- A junction table for each many-to-many relationship

---

# Step 3: Insert Data

- At least **20 rows** per main table
- Make it realistic (real-sounding names, valid dates)
- Include some edge cases (a customer with no orders, a NULL where allowed)

---

# Step 4: Write Queries

Start simple:

```sql
SELECT * FROM customers LIMIT 10;
```

Then build complexity: filters, JOINs, GROUP BY, CTEs, window functions.

---

# Step 5: Analytical Queries

Examples:

👉 “Who is the top customer?”  
👉 “Which product generates the most revenue?”  
👉 “What are the total sales per product?”

---

# Example Query

👉 “Who are the top 3 customers by revenue?”

```sql
SELECT c.customer_id, c.first_name, c.last_name,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total DESC
LIMIT 3;
```

On the Week 9 data: Derek Mitchell (7,429.85), Eva Garcia (7,117.39), Aria Baker (6,108.70)

---

# Insight Matters

Don’t just run queries.

👉 Explain what they mean

Example:
“Derek Mitchell is our top customer, with $7,429.85 in purchases.”

---

# Deliverables

You will submit (details in `lab09_student.md`):

- Your **Marimo notebook** (.py) with all SQL code and outputs
- Your **CSV data files** (if you used any)
- Your **ER diagram** (an image, or inside the notebook)
- A **5–8 minute presentation** in Week 10

---

# Grading Weights

| Deliverable | Weight |
|-------------|--------|
| ER diagram | 15% |
| Normalized schema (DDL) | 15% |
| Sample data | 10% |
| 10 SQL queries | 25% |
| Transaction demo | 10% |
| Views and indexes | 10% |
| Presentation / write-up | 15% |

---

# Common Mistakes

- Too many tables — more than you can finish ❌  
- Too few relationships (no many-to-many) ❌  
- Weak queries (only `SELECT *`) ❌  
- No clear insights ❌  

---

# Keep It Simple

Start with:

👉 your 3 core tables → make them correct  

Then grow to the required **5 tables** (at least one junction table).

Better to do 5 tables well than 15 badly.

---

# In-Class Exercise

👉 “What tables would you create for a food delivery app?”

Hints:
- customers
- restaurants
- menu_items (each belongs to one restaurant)
- orders
- order_items (junction: orders ↔ menu_items)

---

# Mental Model

Database project =

👉 Design + Data + Queries + Insight

---

# Hands-On Time

- Start your project
- Define tables
- Insert sample data

---

# Summary

- This is your capstone
- Apply everything you learned
- Focus on clarity and correctness

---

# What’s Next?

Week 10:
- Project presentations
- Review and the big picture
- Modern data: JSON, PIVOT, LIST, UNNEST

---

# Final Thought

This is where you prove your skills.

👉 Build something meaningful.

---

# Let’s Build 🚀

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
