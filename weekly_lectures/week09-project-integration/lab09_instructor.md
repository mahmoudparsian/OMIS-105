# Capstone Project — INSTRUCTOR GRADING GUIDE

## OMIS 105 — Database Management Systems
**Week 9 | Grading Rubric**

---

## Grading Breakdown (100 points total)

### 1. ER Diagram (15 points)

| Points | Criteria |
|--------|----------|
| 13–15 | Clear, complete diagram with all entities, attributes, PKs, FKs, correct cardinality, M:M junction table present |
| 10–12 | Mostly complete, minor errors (missing an attribute or wrong cardinality) |
| 7–9 | Major omissions (missing entities or relationships) |
| 0–6 | Incomplete, incorrect, or missing |

### 2. Normalized Schema (15 points)

| Points | Criteria |
|--------|----------|
| 13–15 | 5+ tables, proper CREATE TABLE with PK, FK, NOT NULL, CHECK, UNIQUE; documented 3NF verification |
| 10–12 | 5 tables, most constraints present, minor normalization issues |
| 7–9 | <5 tables or missing key constraints |
| 0–6 | Major issues: no PKs, no FKs, clear normalization violations |

### 3. Sample Data (10 points)

| Points | Criteria |
|--------|----------|
| 9–10 | 20+ rows per main table, realistic data, good variety, edge cases |
| 7–8 | 20 rows, mostly realistic |
| 5–6 | <20 rows or unrealistic ("test1", "aaa") |
| 0–4 | Minimal or missing data |

### 4. SQL Queries (25 points)

| Points | Criteria |
|--------|----------|
| 22–25 | 10 queries covering all categories, well-documented, complex, correct output |
| 18–21 | 10 queries, adequate coverage, minor issues |
| 14–17 | <10 queries or mostly simple (no JOINs, no window functions) |
| 0–13 | Few queries, errors, or missing categories |

**Query category minimums:**
- 2 basic SELECT with WHERE/ORDER BY (2 pts each)
- 3 JOINs including multi-table (3 pts each)
- 2 GROUP BY/HAVING/CASE (2.5 pts each)
- 2 Window functions or CTEs (3 pts each)
- 1 Transaction (see below, scored separately)

### 5. Transaction Demo (10 points)

| Points | Criteria |
|--------|----------|
| 9–10 | Multi-step (3+ SQL), try/except with ROLLBACK, success + failure demos |
| 7–8 | Transaction works, some error handling |
| 5–6 | Basic BEGIN/COMMIT only, no error handling |
| 0–4 | No transaction or non-functional |

### 6. Views and Indexes (10 points)

| Points | Criteria |
|--------|----------|
| 9–10 | 2+ views, 3+ indexes, each with clear justification |
| 7–8 | Requirements met, minimal justification |
| 5–6 | Only 1 view or 1 index |
| 0–4 | Missing or non-functional |

### 7. Presentation (15 points)

| Points | Criteria |
|--------|----------|
| 13–15 | Clear structure, within time, live demo works, good explanation of design choices |
| 10–12 | Adequate presentation, mostly within time |
| 7–9 | Disorganized, over/under time, no live demo |
| 0–6 | Confusing, incomplete, or not presented |

---

## Common Issues to Watch For

1. **Copying ShopSmart exactly** — the project should be a different domain. Deduct 10 points for using ShopSmart or trivially renaming it.
2. **No M:M relationship** — this is a key requirement. Deduct 5 points.
3. **Queries that don't run** — partial credit for correct logic with syntax errors.
4. **"Fake" data** — random strings like "asdf" should result in data point deductions.
5. **Over-scoping** — don't penalize for ambitious projects with minor incomplete areas; reward ambition.

---

## Sample Excellent Project (Reference)

**Domain**: Fitness Gym

**Tables**: members, trainers, class_types, classes, rooms, bookings, payments (7 tables)

**M:M**: members ↔ classes through bookings

**Strong queries included**:
- Class utilization rate using window functions
- Revenue by trainer using CTEs
- Member retention analysis using LAG
- Transaction: book a class (check capacity, create booking, process payment)

**This would score 90+.**

