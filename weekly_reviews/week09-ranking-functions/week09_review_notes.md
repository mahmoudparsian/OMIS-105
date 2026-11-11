# OMIS 105 — Week 9 Review Notes: Ranking Functions

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week09_review_notebook.py`. Open the notebook
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

## Session 1 — ROW_NUMBER and RANK

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

## Session 2 — DENSE_RANK and Filtering on a Rank

### Learning Objectives

Students will be able to:

- Use `DENSE_RANK()` and explain how it differs from `RANK()`
- Read `ROW_NUMBER`, `RANK`, and `DENSE_RANK` side by side on tied data
- Filter on a rank by computing it in a CTE, then using `WHERE` outside
- Answer "second-highest" questions with `DENSE_RANK() ... = 2`
- Explain why `ORDER BY ... LIMIT n` (and `OFFSET`) cannot answer
  ranking questions

### Key Concepts

**Three functions, three ways to treat ties:**

- `ROW_NUMBER()` — 1, 2, 3, 4 (add a tie-breaker so the order is stable)
- `RANK()` — 1, 1, 3, 3 (ties share a rank, then a **gap**)
- `DENSE_RANK()` — 1, 1, 2, 2 (ties share a rank, **no gap**)

**Filtering on a rank:** `WHERE` runs before window functions, so it
cannot see a rank. Compute the rank in a CTE or subquery, then filter
outside it.

**`LIMIT` is not a ranking tool:** `LIMIT n` counts **rows**, a ranking
function compares **values**. With ties at the cut-off, `LIMIT` silently
drops tied rows; `OFFSET 1` skips a row, not a value; and `LIMIT` cannot
restart per group. Use it only to make a long result shorter.

### Teaching Flow (2 hours)

1. **Recap** (10 min): `ROW_NUMBER` and `RANK` from Session 1.

2. **Side by side** (20 min): Section 1.4 — rank customers by
   number of completed payments. Two customers tie at 4 and two at 3.
   Ask students to predict each column before running the cell.

3. **Second-highest** (25 min): Section 1.8 — `DENSE_RANK() = 2`
   returns Harbor Health and Acme Corp. Then change it to `RANK() = 2`:
   no rows. Ask: why?

4. **`LIMIT` vs. ranking** (10 min): Section 1.9 — ask students to
   predict `LIMIT 1` and `LIMIT 1 OFFSET 1` before running them
   (ClearView only; Falcon Logistics with 4, not a 3-payment customer).

5. **Top-N per group** (15 min): Revisit Section 1.6. Which
   function would keep ties?

6. **Practice** (40 min): Students rank plans, customers, and
   tickets, choosing the right function for each question.

### Discussion Questions

- When is `RANK` the right answer, and when is `DENSE_RANK`?
- Why does `ROW_NUMBER` need a tie-breaker?
- "Top 3 customers" returned 4 rows. Is that a bug?
- A teammate answers "top 3 customers" with `ORDER BY ... LIMIT 3`.
  When is that answer wrong, and how would you notice?

## Homework / Review Exercises

1. Write a window function that ranks support tickets by
   resolution time within each priority level.

2. Rank the plans by total completed revenue with `RANK` and
   `DENSE_RANK`. Do they differ? Why or why not?

3. Find the customers with the **second-highest** number of support
   tickets. Use a CTE and `DENSE_RANK`.

4. Answer exercise 3 again with `ORDER BY ... LIMIT 1 OFFSET 1`.
   Do you get the same answer? Explain the difference.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
