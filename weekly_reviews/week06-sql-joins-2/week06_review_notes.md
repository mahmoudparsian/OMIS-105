# OMIS 105 — Week 6 Review Notes: Joins II — Joins in Practice

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week06_review_notebook.py`. Open the notebook
and teach from it; use these notes for timing, discussion prompts, and the
homework assignment.

---

## Prerequisites (Weeks 1–5)

Students know SELECT, WHERE, ORDER BY, GROUP BY, HAVING, the aggregate
functions, and every join type from Week 5 (INNER, LEFT, RIGHT, FULL
OUTER, CROSS, SELF). This week adds no new syntax. It is **practice**:
choosing the right join, predicting its row count, and avoiding three
silent mistakes.

---

## Dataset: The Same Tech Company

The company from Weeks 4–5: `departments` (6), `employees` (30),
`projects` (8), `assignments` (25). The gaps that matter this week:

| Gap | Rows | Shows up in |
|---|---|---|
| Employees with no department (`dept_id` is `NULL`) | Zack, Amy, Ben | 6.1, 6.3 |
| Department with no employees | Legal | 6.1, 6.2, 6.4, 6.5 |
| Employees on no project | 11 | 6.3, 6.6 |
| Employee who earns more than their manager | Mia (vs. Leo) | 6.7 |

---

# Week 6 — Joins II (Lectures 11–12)

## Lecture 11 (2 hours): Which Rows Did My Join Keep?

### Opening (10 min)

Write the four join types on the board and ask students to **predict** the
row count of `employees ⋈ departments` for each one before running 6.1.
Answers: INNER 27, LEFT 30, RIGHT 28, FULL OUTER 31. Most students get
INNER right and miss the others — that is the point.

### Four Answers from the Same Tables (25 min)

Run 6.1. Then show *which* rows each join added (the two queries under
the scoreboard). Key sentence: "A join is not just a way to get columns.
It is a decision about which rows to keep."

### RIGHT = LEFT Turned Around (15 min)

6.2. `employees RIGHT JOIN departments` = `departments LEFT JOIN employees`.
Recommend the habit: "Start `FROM` the table you want to keep, then
`LEFT JOIN` everything else."

### Finding What Is Missing (30 min)

6.3. The anti-join recipe, step by step:

1. `FROM` the table you are checking
2. `LEFT JOIN` the table where a partner should be
3. `WHERE partner_key IS NULL`

Stress testing the **key** of the right table — a column that is never
`NULL` in a real row. Then `COALESCE` for readable reports.

### The ON vs. WHERE Trap (30 min)

6.4. Ask: "We want *every* department. Why did HR and Legal disappear?"
Walk through it: the `LEFT JOIN` keeps them, then `WHERE` removes them
because their employee columns are `NULL` (or too old). Moving the
condition into `ON` fixes it.

Rule on the board:

| Filter on… | Put it in… |
|---|---|
| the table you keep | `WHERE` |
| the optional table | `ON ... AND ...` |

### Discussion Points

- Your report shows 27 employees but HR says there are 30. What happened?
  (An `INNER JOIN` dropped the 3 employees with no department.)
- When is it *correct* to drop unmatched rows? (When the question is only
  about matched pairs — e.g. "employees and their department budgets".)

---

## Lecture 12 (2 hours): Joins at Work

### Counting with LEFT JOIN (35 min)

6.5. Legal shows a headcount of **1** with `COUNT(*)`. Ask students to
explain before showing the fix. Then the second surprise: `SUM(e.salary)`
is `NULL` for Legal, not 0. `COUNT` of nothing is 0; `SUM` of nothing is
"no value". `COALESCE(SUM(...), 0)` is the reporting fix.

### Chains of Joins (35 min)

6.6. Build the chain one join at a time: employees → assignments →
projects. Then change only the last join to `INNER` and compare: 30
employees become 19. Rule: once a row can have `NULL`s, keep using
`LEFT JOIN` after it.

Finish with the 3-table department report (projects and weekly hours per
department, Legal at 0).

### Self-Joins at Work (30 min)

6.7. "Does anyone earn more than their manager?" — exactly one: Mia
(130,000) vs. Leo (125,000). Discuss what an analyst does with a finding
like this (report it with context; do not "fix" the data).

Then direct reports per manager with `GROUP BY` + `HAVING`.

### A Real Error (10 min)

6.8. The ambiguous `dept_id` error. Read the message together — DuckDB
even suggests the fix.

### Discussion Points

- Why does `COUNT(*)` give 1 for an empty department? (The `LEFT JOIN`
  row with `NULL`s is still a row.)
- Where in your own work would a chain of 3–4 joins appear? (Orders →
  order items → products → suppliers.)

---

## Homework

| Homework | Key Skill Tested |
|----------|-----------------|
| 8 queries on the company data: 2 anti-joins, 1 `ON` vs. `WHERE` pair (wrong and right), 2 counts including zero (one with `COALESCE(SUM(...), 0)`), 1 three-table chain with `LEFT JOIN`s, 2 self-joins | Can they predict and control which rows a join keeps? |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
