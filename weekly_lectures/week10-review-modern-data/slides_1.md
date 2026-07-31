---
title: OMIS 105 - Week 10 (Flagship Expanded)
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

- SQL querying
- Data modeling
- Database design
- Performance thinking
- Transactions & reliability

👉 This is a COMPLETE foundation

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

- SELECT → retrieve data  
- WHERE → filter  
- ORDER BY → sort  
- GROUP BY → aggregate  
- HAVING → filter groups  
- JOIN → connect tables  

---

# Example Full Query

```sql
SELECT c.name, SUM(o.amount) AS total
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.name
HAVING total > 1000
ORDER BY total DESC;
```

👉 Combines everything

---

# Design Review

You learned:

- Primary keys  
- Foreign keys  
- Normalization  
- Clean schema design  

---

# Design Mental Model

👉 “Where should this data live?”

👉 “Does this belong in another table?”

---

# Performance Review

- Index = faster queries  
- Trade-offs exist  
- Think about scale  

---

# Transactions Review

- BEGIN / COMMIT / ROLLBACK  
- ACID properties  
- Reliability matters  

---

# Common Mistakes (Important)

- Missing JOIN condition ❌  
- Confusing WHERE vs HAVING ❌  
- Poor schema design ❌  
- Ignoring NULL values ❌  

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
- Business intelligence  
- Backend systems  
- Data engineering  

---

# Example Roles

- Data Analyst  
- Data Engineer  
- Backend Developer  
- Business Analyst  

---

# Simple Data Architecture

Data → Database → Queries → Insights → Decisions

---

# Project Reflection

Ask yourself:

- Is my schema clean?  
- Are my queries correct?  
- Do I provide insights?  

---

# Final Tips

- Practice SQL regularly  
- Work on real datasets  
- Build small projects  
- Stay curious  

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
- Learn advanced topics  
- Explore data tools  

---

# Final Thought

You didn’t just learn SQL.

👉 You learned how to think with data.

---

# Thank You 🙌

You are now ready to use databases in the real world.
