---
title: OMIS 105 - Week 9 (Flagship Expanded)
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
## Week 9: Project & Integration (Build a Real System)

---

# Agenda

- Why projects matter
- What you are building
- Project structure
- Step-by-step guide
- Example project
- Common mistakes
- Grading expectations

---

# Recap

- You learned:
  - SQL (SELECT, WHERE, JOIN, GROUP BY)
  - Design (normalization)
  - Performance (indexing)
  - Reliability (transactions)

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

---

# Project Requirements

Minimum:

- 3 tables
- Primary keys
- Foreign keys
- 10+ rows per table
- 5 meaningful queries

---

# Required Queries

1. Basic SELECT  
2. WHERE filter  
3. JOIN query  
4. GROUP BY  
5. Analytical (insight)

---

# Choose a Domain

Pick something simple:

- E-commerce
- Bookstore
- Food delivery
- Movie database

👉 Keep it manageable

---

# Example: E-commerce

Tables:

- customers
- orders
- products

---

# Example Schema

Customers(id, name)  
Orders(id, customer_id, product_id, amount)  
Products(id, name, price)

---

# Step 1: Design Tables

Ask:

👉 “What are the main entities?”

👉 “How are they connected?”

---

# Step 2: Define Keys

- Primary keys (id)
- Foreign keys (relationships)

---

# Step 3: Insert Data

- At least 10 rows per table
- Make it realistic

---

# Step 4: Write Queries

Start simple:

```sql
SELECT * FROM customers;
```

Then build complexity

---

# Step 5: Analytical Queries

Examples:

👉 “Who is the top customer?”  
👉 “What product generates most revenue?”  
👉 “Total sales per product?”

---

# Example Query

```sql
SELECT c.name, SUM(o.amount) AS total
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.name
ORDER BY total DESC;
```

---

# Insight Matters

Don’t just run queries.

👉 Explain what they mean

Example:
“Customer Alice generated the highest revenue”

---

# Deliverables

You will submit:

- SQL file
- Query results
- 1-page explanation

---

# Grading Criteria (Suggested)

- Correct schema (30%)
- Correct queries (30%)
- Insights (20%)
- Clarity (20%)

---

# Common Mistakes

- Too many tables ❌  
- Too few relationships ❌  
- Weak queries ❌  
- No clear insights ❌  

---

# Keep It Simple

Start with:

👉 3 tables → make them correct  

Then expand if needed

---

# In-Class Exercise

Ask:

👉 “What tables would you create for a food delivery app?”

Guide students to:
- users
- orders
- restaurants

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
- Apply everything learned
- Focus on clarity and correctness

---

# What’s Next?

Week 10:
- Review
- Big picture
- Real-world context

---

# Final Thought

This is where you prove your skills.

👉 Build something meaningful.

---

# Let’s Build 🚀
