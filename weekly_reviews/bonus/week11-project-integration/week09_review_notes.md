# OMIS 105 — Week 9 Review Notes: CTEs, Subqueries & Advanced Window Functions

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week09_review_notebook.py`. Open the notebook
and teach from it; use these notes for timing, discussion prompts, and the
homework assignment.

---

## Dataset: CloudMetrics SaaS (Extended)

The same SaaS company from Weeks 7–8, plus two new tables: user activity
`events` (with a JSON `metadata` column) and quarterly `kpi_targets`.

| Table | Rows | Purpose |
|-------|------|---------|
| `plans` | 3 | Subscription tiers |
| `customers` | 10 | Companies subscribed to CloudMetrics |
| `payments` | 25 | Monthly payment records |
| `events` | 25 | User activity events, each with JSON metadata |
| `kpi_targets` | 6 | Quarterly revenue and signup targets |

**Why this dataset?** SaaS businesses live and die by metrics:
monthly recurring revenue (MRR), churn, customer lifetime value.
Window functions and aggregations are exactly how analysts at
these companies answer business questions every day.

---

## Session 1 — CTEs & Subqueries

### Learning Objectives

Students will be able to:

- Write CTEs with `WITH ... AS`
- Chain multiple CTEs
- Write subqueries in WHERE, FROM, and SELECT
- Write correlated subqueries
- Use `EXISTS` and `IN` with subqueries

### Key Concepts

**CTE (Common Table Expression):** A named temporary 
result set defined with `WITH`. Think of it as "naming 
a paragraph" in a long query. CTEs are not stored — 
they exist only during the query execution.

**Subquery:** A query nested inside another query. Can appear in:

- `WHERE` — filter rows based on another query's result
- `FROM` — use a query result as a virtual table
- `SELECT` — compute a value for each row

**Correlated subquery:** A subquery that references a column
from the outer query. It runs once per row of the outer query.

**EXISTS vs IN:**

- `EXISTS` checks whether a subquery returns any rows (true/false)
- `IN` checks whether a value is in a set of values

### Teaching Flow (2 hours)

1. **Motivating question** (10 min): "Which customers have paid
   more than the average customer?" Show that you need two
   queries — or a subquery / CTE.

2. **Basic CTE** (15 min): Calculate total revenue per customer,
   then filter to above-average customers.

3. **Chained CTEs** (15 min): Revenue per customer → plan-level
   summary → comparison. Show how each CTE builds on the last.

4. **Subquery in WHERE** (15 min): Find customers whose total
   payments exceed the overall average.

5. **Subquery in FROM** (15 min): Use a derived table to join
   aggregated data back to detail rows.

6. **Correlated subquery** (15 min): For each customer, find
   their most recent payment. The subquery references the outer
   customer_id.

7. **EXISTS and IN** (15 min): Find customers who have at least
   one failed payment (EXISTS). Find customers on the Enterprise
   plan (IN).

8. **Practice** (20 min): Students write CTEs and subqueries
   to answer business questions about the events table.

### Discussion Questions

- When would you choose a CTE over a subquery?
- Why is a correlated subquery slower than a regular subquery?
- Can you always rewrite EXISTS as IN? Are they interchangeable?

---

## Session 2 — Advanced Window Functions

### Learning Objectives

Students will be able to:

- Use `LAG()` and `LEAD()` to compare consecutive rows
- Compute running totals with `SUM() OVER (ORDER BY ...)`
- Calculate moving averages with `ROWS BETWEEN`
- Use `DENSE_RANK()`, `NTILE()`, and `FIRST_VALUE()`
- Combine CTEs with window functions

### Key Concepts

**LAG / LEAD:** Access the previous row (`LAG`) or next row
(`LEAD`) without a self-join. Essential for time-series analysis:
month-over-month growth, day-over-day change.

**Running total:** `SUM() OVER (ORDER BY date)` — the cumulative
sum up to each row. Shows how revenue accumulates over time.

**Moving average:** `AVG() OVER (ROWS BETWEEN 2 PRECEDING AND
CURRENT ROW)` — the average of the current row and the 2 before
it. Smooths out noise in time-series data.

**NTILE(n):** Divides rows into n roughly equal buckets. Useful
for quartile analysis (NTILE(4)) or decile (NTILE(10)).

**FIRST_VALUE:** Returns the first value in the window. Useful
for comparing every row to the earliest/highest/lowest.

### Teaching Flow (2 hours)

1. **LAG / LEAD** (20 min): Show each customer's payment next
   to their previous payment. Calculate the change.

2. **Running total** (15 min): Cumulative revenue over time.
   "How much total revenue have we earned by each month?"

3. **Moving average** (15 min): 3-payment moving average to
   smooth out payment fluctuations.

4. **DENSE_RANK** (10 min): Like RANK but no gaps. Compare
   RANK(1,2,2,4) vs DENSE_RANK(1,2,2,3).

5. **NTILE(4)** (15 min): Divide customers into quartiles by
   total revenue. "Which customers are in the top 25%?"

6. **FIRST_VALUE** (10 min): For each customer, show their
   first-ever payment date next to each row.

7. **CTE + Window combo** (15 min): Calculate each customer's
   percentage of total revenue using a CTE for the total and
   a window function for the per-row calculation.

8. **Practice** (20 min): Students write LAG/LEAD queries on
   events data — what did each customer do before and after
   each event?

### Discussion Questions

- What's the difference between `RANK`, `DENSE_RANK`, 
  and `ROW_NUMBER`?
- When would you use NTILE in a business context?
- Why is LAG useful for detecting churn?

---

## Homework / Review Exercises

1. Write a CTE that finds customers whose total payments are
   in the top quartile (use NTILE).

2. Use LAG() to calculate month-over-month payment change for
   each customer. Which customer had the biggest drop?

3. Write a correlated subquery that returns, for each customer,
   the date and amount of their most recent completed payment.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
