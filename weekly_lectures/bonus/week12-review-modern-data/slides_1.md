---
title: OMIS 105 - Week 10 (Review & Synthesis)
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
## Week 10: Review, Synthesis & Real-World Perspective

---

# Agenda

- Course recap (big picture)
- Key SQL concepts review
- Design principles review
- Common mistakes
- Real-world applications
- Career relevance
- Final preparation

---

# What You Have Learned

Over 10 weeks:

- SQL querying (SELECT, JOINs, GROUP BY, CTEs, window functions)
- Data modeling (keys and relationships)
- Database design (normalization)
- Performance thinking (indexes, EXPLAIN)
- Transactions & reliability (ACID, constraints)
- Modern data (JSON, lists, PIVOT)

👉 This is a solid foundation

---

# The Big Picture

From:

Raw data  

To:

👉 Structured data → Queries → Insights → Decisions

---

# Your Skillset Now

You can:

- Create tables  
- Design schemas  
- Write queries  
- Join data  
- Analyze results  

👉 This is powerful

---

# SQL Review

Core concepts:

- SELECT → choose columns  
- WHERE → filter rows  
- ORDER BY → sort  
- GROUP BY → aggregate  
- HAVING → filter groups  
- JOIN → connect tables  
- WITH (CTE) → name a step of a query  
- OVER (window function) → compute across rows without collapsing them  

---

# Example Full Query

```sql
SELECT c.customer_id, c.first_name, c.last_name,
       ROUND(SUM(o.total_amount), 2) AS total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status <> 'cancelled'
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING SUM(o.total_amount) > 1000
ORDER BY total DESC
LIMIT 5;
```

👉 Combines JOIN, WHERE, GROUP BY, HAVING, ORDER BY, and LIMIT

(Group by the key, `customer_id`, not only by the name — two customers can share a name.)

---

# Design Review

You learned:

- Primary keys (one unique ID per row)  
- Foreign keys (links between tables)  
- Normalization (1NF, 2NF, 3NF)  
- Constraints (`NOT NULL`, `CHECK`, `UNIQUE`)  

---

# Design Mental Model

👉 “Where should this data live?”

👉 “Does this belong in another table?”

---

# Performance Review

- An index speeds up searches that return **few** rows  
- Indexes slow down writes and use extra space  
- DuckDB is fast even without indexes (columnar storage)  
- Think about scale  

---

# Transactions Review

- BEGIN / COMMIT / ROLLBACK  
- ACID: Atomicity, Consistency, Isolation, Durability  
- After an error, the transaction must be rolled back  
- Reliability matters  

---

# Common Mistakes (Important)

- Missing JOIN condition ❌  
- Confusing WHERE vs HAVING ❌  
- Selecting a column that is neither grouped nor aggregated ❌  
- Using `= NULL` instead of `IS NULL` ❌  
- `COUNT(*)` after a LEFT JOIN ❌  
- Poor schema design ❌  

---

# How to Think Like a Data Professional

Instead of:

❌ “Write SQL”

Think:

✅ “What question am I answering?”

---

# Real-World Applications

SQL is used in:

- Data analytics  
- Business intelligence (dashboards and reports)  
- Backend systems (websites and apps)  
- Data engineering (moving and cleaning data)  

---

# Example Roles

- Data Analyst  
- Data Engineer  
- Backend Developer  
- Business Analyst  

---

# Simple Data Architecture

Data sources → Database → Queries → Insights → Decisions

(apps, files, APIs) → (tables) → (SQL) → (reports, dashboards) → (business actions)

---

# Project Reflection

Ask yourself:

- Is my schema clean?  
- Are my queries correct?  
- Do I provide insights?  

---

# Final Tips

- Practice SQL regularly  
- Work on real datasets (public CSV files are a great start)  
- Build small projects  
- Stay curious  

For the final exam (closed book): practice writing queries **by hand**.

---

# Confidence Boost

If you can:

- Write JOIN queries  
- Use GROUP BY  
- Design tables  

👉 You are ahead of many beginners

---

# What to Do Next

After this course:

- Practice more SQL  
- Learn advanced topics (window functions, query tuning)  
- Explore data tools (Python + pandas, BI tools, cloud databases)  

---

# Final Thought

You didn’t just learn SQL.

👉 You learned how to think with data.

---

# Thank You 🙌

You are now ready to use databases in the real world.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
