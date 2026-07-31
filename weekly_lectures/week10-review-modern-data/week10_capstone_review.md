# OMIS 105 — Week 10: Capstone + Final Review + Practice Exam

---

# 🎯 Week 10 Structure

## Session 1 (2 hours)
- Capstone Project (end-to-end SQL)

## Session 2 (2 hours)
- Final Review
- Practice Exam

---

# 🧪 PART 1 — CAPSTONE PROJECT

## Dataset

Assume table:

sales(order_id, customer, product, region, price)

---

## Tasks (Students)

1. Show total revenue.
2. Show revenue per customer.
3. Show top 3 customers by revenue.
4. Show revenue per region.
5. Show product revenue.
6. Show products with revenue > 1000.
7. Show top customer per region (ROW_NUMBER).
8. Rank customers globally (RANK).
9. Show customers above average spending.
10. Show revenue contribution % per customer.

---

## Instructor Sample Solutions

-- Total revenue
SELECT SUM(price) FROM sales;

-- Revenue per customer
SELECT customer, SUM(price) FROM sales GROUP BY customer;

-- Top 3 customers
SELECT customer, SUM(price) total
FROM sales
GROUP BY customer
ORDER BY total DESC
LIMIT 3;

-- Top customer per region
SELECT * FROM (
  SELECT customer, region, SUM(price) total,
         ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(price) DESC) rn
  FROM sales
  GROUP BY customer, region
) t WHERE rn=1;

-- Rank customers
SELECT customer, SUM(price),
RANK() OVER (ORDER BY SUM(price) DESC)
FROM sales GROUP BY customer;

---

# 📘 PART 2 — FINAL REVIEW

## Key Concepts Checklist

### Week 1–3
- SELECT
- WHERE
- ORDER BY
- LIMIT
- GROUP BY
- HAVING

### Week 4–5
- JOIN
- LEFT JOIN
- Multi-table JOIN

### Week 6
- Normalization
- 1NF, 2NF, 3NF

### Week 7
- ROW_NUMBER
- RANK
- PARTITION BY

### Week 8
- Transactions
- COMMIT / ROLLBACK
- ACID

---

# 🧪 PART 3 — PRACTICE EXAM

## Multiple Choice

1. WHERE vs HAVING difference?
Answer: WHERE filters rows, HAVING filters groups

2. LIMIT vs RANK?
Answer: LIMIT global, RANK supports grouping

---

## Analyze SQL

3.
SELECT department, COUNT(*) FROM employees GROUP BY department;

Answer: count per department

4.
SELECT * FROM employees ORDER BY salary DESC LIMIT 2;

Answer: top 2 salaries

---

## Write SQL

5. Top 2 employees per department.

SELECT * FROM (
SELECT *, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) rn
FROM employees) t WHERE rn<=2;

6. Employees above department average.

SELECT * FROM (
SELECT *, AVG(salary) OVER (PARTITION BY department) avg
FROM employees) t WHERE salary > avg;

---

## Transactions

7. What does ROLLBACK do?
Answer: undo all changes

---

## Normalization

8. What is 3NF?
Answer: no transitive dependency

---

# 🎯 Final Advice to Students

- Read questions carefully
- Write SQL step-by-step
- Test logic mentally before writing
- Watch for WHERE vs HAVING
- Use window functions when needed

---

# 🚀 End of Course

You now know:
- SQL querying
- Data modeling
- Analytical SQL
- Database systems concepts

