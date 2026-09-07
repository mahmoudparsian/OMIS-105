# OMIS 105 — Week 7 Review Notes: Window Functions & Query Performance

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week07_review_notebook.py`. Open the notebook
and teach from it; use these notes for timing, discussion prompts, and the
homework assignment.

---

## Dataset: CloudMetrics SaaS

A software-as-a-service (SaaS) company that sells analytics tools to
businesses. This week uses four tables:

| Table | Rows | Purpose |
|-------|------|---------|
| `plans` | 3 | Subscription tiers: Starter (`$29.99`), Professional (`$79.99`), Enterprise (`$149.99`) |
| `customers` | 10 | Companies subscribed to CloudMetrics, across 8 industries |
| `payments` | 25 | Monthly payment records with statuses: completed, failed, refunded |
| `support_tickets` | 15 | Support requests with priority levels and categories |

**Why this dataset?** SaaS businesses live and die by metrics:
monthly recurring revenue (MRR), churn, customer lifetime value.
Window functions and aggregations are exactly how analysts at
these companies answer business questions every day.

---

## Session 1 — Window Functions

### Learning Objectives

Students will be able to:

- Use `ROW_NUMBER()` to assign sequential numbers to rows
- Use `PARTITION BY` to number/rank within groups
- Use `RANK()` and understand ties
- Compare `ROW_NUMBER` vs `RANK` behavior
- Use `AVG() OVER (PARTITION BY ...)` to compare a row to its group average
- Extract top-N per group using window functions

### Key Concepts

**What is a window function?** A function that computes a value
for each row based on a "window" of related rows — without
collapsing the result into a single row like GROUP BY does.

**The OVER clause:** Every window function needs `OVER(...)`.
Inside OVER you specify:

- `ORDER BY` — how to sort the window
- `PARTITION BY` — how to divide into groups

**ROW_NUMBER vs RANK:**

- `ROW_NUMBER()` always gives unique numbers (1, 2, 3, 4...)
- `RANK()` gives the same number to ties and skips (1, 2, 2, 4...)

### Teaching Flow (2 hours)

1. **Motivating question** (10 min): "Which customers pay the
   most? Can you rank them without losing the individual payment
   rows?" Show why GROUP BY alone can't do this.

2. **ROW_NUMBER basics** (15 min): Number all customers by
   signup date. Then PARTITION BY plan to number within each plan.

3. **RANK** (15 min): Rank customers by total payments. Show
   what happens with ties.

4. **AVG OVER PARTITION** (20 min): For each payment, show the
   plan average next to it. Calculate the difference. Ask:
   "Which customers are paying above their plan's average?"

5. **Top-N per group** (20 min): Find the top-2 paying customers
   per plan. Use a subquery wrapping ROW_NUMBER.

6. **Practice** (40 min): Students write window function queries
   on the support_tickets table — rank tickets by priority,
   number tickets per customer, compare resolution times.

### Discussion Questions

- Why can't you put a window function in WHERE?
- When would you choose RANK over ROW_NUMBER?
- How is `AVG() OVER (PARTITION BY plan_id)` different from
  `GROUP BY plan_id`?

---

## Session 2 — Query Performance

### Learning Objectives

Students will be able to:

- Use `EXPLAIN` to see how DuckDB executes a query
- Create indexes with `CREATE INDEX`
- Distinguish sargable from non-sargable predicates
- Write CTEs for readability and reuse
- Rewrite subqueries as JOINs for clarity

### Key Concepts

**EXPLAIN:** Shows the query execution plan — what steps the
database takes to answer your query. Not about memorizing the
output; about understanding that databases plan before executing.

**Indexes:** A data structure that speeds up lookups on specific
columns. Like the index at the back of a textbook.

**Sargable predicates:** Conditions the database can use an index
for. `WHERE payment_date >= '2025-03-01'` is sargable.
`WHERE YEAR(payment_date) = 2025` is NOT — the function call
prevents index usage.

**CTEs (WITH clause):** Named temporary result sets that make
complex queries readable. Think of them as "named paragraphs"
in a long SQL query.

### Teaching Flow (2 hours)

1. **Selective queries** (10 min): Why `SELECT *` is wasteful.
   Select only the columns you need.

2. **EXPLAIN** (20 min): Run EXPLAIN on a simple query, then a
   complex join. Compare the plans. Don't memorize — just see
   that the database has a strategy.

3. **Indexes** (20 min): CREATE INDEX on payment_date. Run
   EXPLAIN before and after. Show the difference.

4. **Sargable vs non-sargable** (20 min): Compare
   `WHERE payment_date BETWEEN '2025-03-01' AND '2025-03-31'`
   vs `WHERE MONTH(payment_date) = 3`. Same result, different
   performance.

5. **CTEs** (25 min): Rewrite a nested subquery as a CTE. Then
   chain two CTEs. Show how readability improves dramatically.

6. **Practice** (25 min): Students rewrite messy queries using
   CTEs, create indexes, and check EXPLAIN output.

### Discussion Questions

- Why would a database NOT use an index even when one exists?
- When is a subquery better than a CTE?
- What happens to indexes when you INSERT new rows?

---

## Homework / Review Exercises

1. Write a window function that ranks support tickets by
   resolution time within each priority level.

2. Create an index on `support_tickets(customer_id)` and
   use EXPLAIN to compare query plans before and after.

3. Write a CTE that calculates each customer's total payments,
   then use it to find customers paying above the overall average.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
