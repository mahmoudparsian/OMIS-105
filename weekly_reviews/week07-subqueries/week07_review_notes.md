# OMIS 105 — Week 7 Review Notes: Subqueries

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week07_review_notebook.py`. Open the notebook
and teach from it; use these notes for timing, discussion prompts, and the
homework assignment.

---

## Prerequisites (Weeks 1–6)

Students know SELECT, WHERE, GROUP BY, HAVING, the aggregate functions,
and all join types, including anti-joins with `LEFT JOIN ... IS NULL`.
Subqueries appeared briefly before (Weeks 3–5). This week teaches them
formally, from the simplest kind up.

---

## Dataset: The Same Tech Company

`departments` (6), `employees` (30), `projects` (8), `assignments` (25).
What matters this week:

| Fact | Why it matters |
|---|---|
| Company average salary is 123,866.67 | 7.1 — 15 employees are above it |
| Zack, Amy, Ben have `dept_id = NULL` | 7.3 — makes `NOT IN` return **0 rows** |
| Legal has no employees | 7.3 — the answer `NOT IN` *should* find |
| 19 employees are on projects (25 assignments) | 7.7 — `IN` vs. JOIN row counts |

---

# Week 7 — Subqueries (Lectures 13–14)

## Lecture 13 (2 hours): One Value and a List

### Opening (10 min)

"Who earns more than the average?" Ask students to solve it. Most will run
`AVG` first, then type the number into a second query. Praise that — it is
exactly the two steps a subquery joins together. Then show that
`WHERE salary > AVG(salary)` is an error: `WHERE` sees one row at a time.

### Scalar Subqueries (35 min)

7.1. The inner query runs first and produces **one value**. Show it in
`WHERE` (above average, newest hire) and in `SELECT` (distance from the
average). Then the real error: `=` with a subquery that returns several
rows. Read the DuckDB message together.

### List Subqueries with IN (30 min)

7.2. One column, many rows → `IN`. Then a nested `IN` read **inside-out**:
Planning projects → their assignments → the employees' names. Have
students run the innermost query on its own first.

### The NOT IN Trap (35 min)

7.3 is the most important part of the week. Ask for "departments with no
employees" — everyone expects Legal. `NOT IN` returns **nothing**.

Show the list the subquery returns (it contains `NULL`), then explain on
the board:

```
60 NOT IN (10, 20, 30, 40, 50, NULL)
= 60<>10 AND ... AND 60<>NULL
=  true  AND ... AND unknown   →  unknown  →  row dropped
```

Two fixes: `WHERE dept_id IS NOT NULL` inside, or — preferred —
`NOT EXISTS`.

### Discussion Points

- Why is a silent wrong answer worse than an error? (Nobody checks a
  query that "worked".)
- Which columns in a real database are likely to contain `NULL`s?
  (Optional foreign keys: manager, department, referral source.)

---

## Lecture 14 (2 hours): Tables, Correlation, and CTEs

### EXISTS (20 min)

7.4. "Is there at least one?" `SELECT 1` is a custom. A subquery can
contain a JOIN.

### Subqueries in FROM (25 min)

7.5. An average **of totals** needs two levels of aggregation. Build the
totals first, then wrap them. The alias (`AS t`) is required.

### Correlated Subqueries (30 min)

7.6. The subquery uses a column from the outer row, so it runs once per
employee. Act it out: pick Mia, compute the Sales average, compare. Warn
about the silent bug: a bare `dept_id` inside the subquery means
`e2.dept_id`, which makes the test always true — write the alias on both
sides.

### Subquery or JOIN? (15 min)

7.7. Same question, 25 rows vs. 19 rows. Rule: JOIN to *show* columns from
both tables; `IN` / `EXISTS` to *check*.

### CTEs (25 min)

7.8. `WITH` names a subquery and reads top to bottom. Point out
`dept_stats` used twice. Then a chained CTE (busiest project). Connect it
back: a CTE is the subquery from 7.5, moved to the top and given a name.

### Discussion Points

- When would you choose a CTE over a nested subquery? (When a step is
  reused, or when there are more than two levels.)
- How would you check a correlated subquery by hand? (Pick one outer row
  and run the inner query for it alone.)

---

## Homework

| Homework | Key Skill Tested |
|----------|-----------------|
| 8 queries on the company data: 2 scalar subqueries (one in `SELECT`), 1 nested `IN`, 1 "has no …" question with `NOT EXISTS` plus one sentence on why `NOT IN` fails, 1 subquery in `FROM`, 2 correlated subqueries, 1 CTE used twice | Can they turn a two-step question into one query, safely? |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
