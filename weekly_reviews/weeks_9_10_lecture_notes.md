# OMIS 105 — Weeks 9 & 10 Lecture Notes

## CTEs, Subqueries, Advanced Window Functions & Modern DuckDB

**Instructor:** Dr. Mahmoud Parsian
**Quarter:** Fall 2026

---

## Dataset: CloudMetrics SaaS (Extended)

Builds on the same CloudMetrics company from Weeks 7–8, now
extended with event tracking and KPI targets:

| Table | Rows | Purpose |
|-------|------|---------|
| `plans` | 3 | Subscription tiers (Starter, Professional, Enterprise) |
| `customers` | 10 | Companies subscribed to CloudMetrics |
| `payments` | 25 | Monthly payment records |
| `events` | 25 | User activity events with JSON metadata (page visits, purchases, signups, exports, upgrades) |
| `kpi_targets` | 6 | Quarterly performance targets for key metrics |

**Why extend the dataset?** The `events` table has a JSON
`metadata` column — this is how modern applications actually
store semi-structured data. Students see that SQL can handle
JSON, not just rigid tables.

---

## Session 1 (Week 9) — CTEs & Subqueries

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

## Session 2 (Week 9) — Advanced Window Functions

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

## Session 3 (Week 10) — Course Review

### Learning Objectives

Students will be able to:

- Combine `JOIN`s, `GROUP BY`, `HAVING`, `CTEs`, 
  and window functions
  in a single analytical query
- Apply all SQL concepts learned in Weeks 1–9 to a new dataset

### Teaching Flow (2 hours)

1. **Warm-up queries** (20 min): Quick exercises on the events
   table — SELECT, WHERE, JOIN with customers.

2. **GROUP BY + HAVING review** (15 min): Event counts per
   customer, filtered by HAVING COUNT > 3.

3. **JOIN review** (15 min): LEFT JOIN to find customers with
   no events. INNER JOIN events with customers and plans.

4. **CTE review** (15 min): Multi-step aggregation — events per
   customer → compare to average → flag outliers.

5. **Window function review** (15 min): RANK customers by event
   count. `ROW_NUMBER` events per customer chronologically.

6. **Integration challenge** (30 min): One complex query that
   uses JOINs + GROUP BY + CTE + window function to answer:
   "For each plan, who is the most active customer and how
   does their activity compare to the plan average?"

7. **Q&A** (10 min): Open questions before the final session.

---

## Session 4 (Week 10) — Modern DuckDB Features

### Learning Objectives

Students will be able to:

- Extract fields from JSON columns using `json_extract_string()`
- Reshape data with `PIVOT`
- Collect values into lists with `LIST()`
- Flatten lists with `UNNEST`
- Extract day-of-week with `STRFTIME`
- Use `CROSS JOIN` to compare actuals vs targets

### Key Concepts

**JSON in SQL:** Modern databases store semi-structured data as
JSON inside regular columns. DuckDB can query JSON fields using
`json_extract_string(column, '$.field')`.

**PIVOT:** Rotates rows into columns. Instead of rows like
(customer, event_type, count), you get columns for each event
type. Like a pivot table in Excel.

**LIST():** An aggregate function that collects all values into
an array instead of counting or summing them.

**UNNEST:** The opposite of LIST — it expands an array into rows.

**CROSS JOIN:** Every row from table A paired with every row from
table B. Useful for comparing each actual value against each
target.

### Teaching Flow (2 hours)

1. **JSON extraction** (20 min): Pull `page`, `referral`, and
   `amount` from the JSON metadata column. Cast amount to a
   number for calculations.

2. **PIVOT** (20 min): Pivot event_type into columns to see
   how many page_views, purchases, etc. each customer has.

3. **LIST and UNNEST** (15 min): Collect all event types per
   customer into a list. Then UNNEST to expand back to rows.

4. **STRFTIME** (10 min): Extract day of week from event dates.
   "Which day of the week has the most activity?"

5. **CROSS JOIN** (15 min): Compare actual metrics against KPI
   targets. Every actual paired with every target to find gaps.

6. **Grand finale query** (20 min): CTE + window + JSON + HAVING
   in one query. "This is what real analytics SQL looks like."

7. **Course wrap-up** (20 min): What we learned, what's next,
   how SQL applies to their careers.

### Discussion Questions

- Where have you seen JSON data in the real world? (APIs, config
  files, NoSQL databases, log files)
- When would you use PIVOT vs GROUP BY?
- Why is DuckDB particularly good at these modern features?

---

## Homework / Review Exercises

1. Write a CTE that finds customers whose total payments are
   in the top quartile (use NTILE).

2. Use LAG() to calculate month-over-month payment change for
   each customer. Which customer had the biggest drop?

3. Extract the `referral` field from the events JSON metadata.
   Which referral source drives the most purchase events?

4. PIVOT the events table to show each customer as a row with
   columns for each event_type, containing the count.

5. Write a CROSS JOIN query comparing actual monthly revenue
   to KPI targets. Which quarters missed their target?

6. Write one query that combines: a CTE for aggregation, a
   window function for ranking, and a HAVING clause for
   filtering. Use it to find the top-3 most active customers
   per plan.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
