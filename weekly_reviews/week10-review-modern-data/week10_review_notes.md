# OMIS 105 — Week 10 Review Notes: Modern DuckDB — JSON, PIVOT & Lists

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week10_review_notebook.py`. Open the notebook
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

## Session 1 — Course Review

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

## Session 2 — Modern DuckDB Features

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

1. Extract the `referral` field from the events JSON metadata.
   Which referral source drives the most purchase events?

2. PIVOT the events table to show each customer as a row with
   columns for each event_type, containing the count.

3. Write a CROSS JOIN query comparing actual monthly revenue
   to KPI targets. Which quarters missed their target?

4. Write one query that combines: a CTE for aggregation, a
   window function for ranking, and a HAVING clause for
   filtering. Use it to find the top-3 most active customers
   per plan.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
