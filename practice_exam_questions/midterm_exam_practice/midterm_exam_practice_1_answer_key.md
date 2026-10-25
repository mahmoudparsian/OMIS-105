# OMIS 105 — Midterm Exam Practice Version Answer Key (Weeks 1–5)

Instructor-only. Pair with `midterm_exam_practice_1.md`.

---

## Part 1 — Multiple Choice (30 pts, 2 pts each)

| # | Answer | Topic | Why |
|---|--------|-------|-----|
| 1 | B | Week 1 — DBMS | A DBMS mediates between apps and stored data (storage, retrieval, schema enforcement, security). |
| 2 | C | Week 1 — data types | `DECIMAL(p,s)` stores exact fixed-point values; `DECIMAL(10,2)` is right for a dollar-and-cents salary and avoids float rounding error. |
| 3 | D | Week 1 — constraints | `CHECK (salary > 0)` enforces a domain rule; `NOT NULL`/`UNIQUE`/`DEFAULT` don't restrict to positive values. |
| 4 | B | Week 2 — FK | FK enforces referential integrity: every `assignments.employee_id` must exist in `employees.employee_id`. |
| 5 | B | Week 2 — M:M relationships | Many-to-many relationships require a junction/bridge table; a single FK column can't represent it. |
| 6 | B | Week 2 — composite keys | Two or more columns together forming the PK is a composite key. |
| 7 | B | Week 3 — WHERE vs HAVING | Aggregate conditions (`AVG(salary) > 80000`) must go in `HAVING`, evaluated after `GROUP BY`. A is invalid (aggregate in WHERE); C has the clauses in the wrong order; D never aggregates by department. |
| 8 | B | Week 3 — NULL handling | `NULL` can only be tested with `IS NULL` / `IS NOT NULL`, never `=` or `<>`. |
| 9 | B | Week 3 — scalar subquery | A subquery in `WHERE` computes the average first, then filters row by row; A is invalid SQL (aggregate in WHERE without GROUP BY), C groups incorrectly, D doesn't filter by employee. |
| 10 | C | Week 3 — execution order | Logical order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. |
| 11 | B | Week 4 — LEFT JOIN | `LEFT JOIN` keeps all rows from `employees` (the left table) even without a matching assignment. |
| 12 | B | Week 4 — Cartesian product | No `ON`/`WHERE` join condition means every row of `employees` pairs with every row of `assignments`. |
| 13 | A | Week 4 — multi-table JOIN | Correct join keys throughout: `a.employee_id = e.employee_id`, `a.project_id = p.project_id`. B joins on the wrong column (`a.project_id` to `e.employee_id`); C is missing an `ON` clause entirely; D joins on mismatched columns (`a.employee_id = p.project_id`). |
| 14 | B | Week 5 — window functions | `RANK() OVER (PARTITION BY ... ORDER BY ...)` ranks every row within each partition without collapsing rows — unlike `GROUP BY`. |
| 15 | C | Week 5 — set operations | `EXCEPT` returns rows in the first query not present in the second: Project Phoenix staff minus Project Atlas staff. |

---

## Part 2 — Written Questions (70 pts)

### S1 (10 pts) — Primary key vs. foreign key
**Expected points:**
- `employees.employee_id` is the **primary key** of `employees`: it uniquely identifies each employee row and cannot be NULL or duplicated.
- `assignments.employee_id` is a **foreign key**: it points back to `employees.employee_id`, linking each assignment to the employee who is staffed on that project, and enforcing that an assignment can't reference an employee that doesn't exist.
- Grading: 5 pts correct PK description, 5 pts correct FK description/relationship. Partial credit for a correct general definition without the schema example.

### S2 (10 pts) — WHERE vs. HAVING
**Expected points:**
- `WHERE` filters individual rows **before** grouping/aggregation; it cannot reference aggregate functions.
- `HAVING` filters **groups** after `GROUP BY`/aggregation has been computed; it can reference aggregate functions like `SUM`, `AVG`, `COUNT`.
- Example WHERE: `SELECT * FROM employees WHERE salary > 80000;`
- Example HAVING: `SELECT department, AVG(salary) FROM employees GROUP BY department HAVING AVG(salary) > 80000;`
- Grading: 4 pts WHERE explanation, 4 pts HAVING explanation, 2 pts for two correct/valid examples (accept reasonable variants).

### I1 (15 pts)
```sql
SELECT project_name, budget, status
FROM projects
WHERE status = 'active'
  AND budget > 50000
ORDER BY budget DESC;
```
**Grading:** 5 pts correct filter on `status`, 4 pts correct filter on `budget`, 3 pts correct `ORDER BY DESC`, 3 pts correct columns selected. Accept conditions in either order.

### I2 (15 pts)
```sql
SELECT e.first_name, e.last_name, COUNT(a.project_id) AS num_projects
FROM employees e
LEFT JOIN assignments a ON e.employee_id = a.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name
ORDER BY num_projects DESC;
```
**Grading:** 6 pts uses `LEFT JOIN` (not INNER — this is the key concept being tested), 4 pts correct `GROUP BY` on all non-aggregated selected columns, 3 pts `COUNT(a.project_id)` (must count the assignment-side column, not `COUNT(*)`, to correctly yield 0 rather than 1 for employees with no assignments), 2 pts correct `ORDER BY ... DESC`. Deduct 6 pts if `INNER JOIN` is used (fails the "include unstaffed employees" requirement) or if `COUNT(*)` is used with `LEFT JOIN` (yields 1 instead of 0 for non-matching employees).

### A1 (10 pts)
```sql
SELECT e.first_name, e.last_name,
       COUNT(a.project_id) AS num_projects,
       SUM(a.hours_worked) AS total_hours
FROM employees e
INNER JOIN assignments a ON e.employee_id = a.employee_id
INNER JOIN projects p ON a.project_id = p.project_id
WHERE p.status = 'active'
GROUP BY e.employee_id, e.first_name, e.last_name
HAVING SUM(a.hours_worked) > 100
ORDER BY total_hours DESC;
```
**Grading:** 2 pts joins all three tables correctly (`employees`→`assignments`→`projects`), 2 pts `WHERE p.status = 'active'` (row-level filter applied before grouping), 2 pts correct `GROUP BY`, 2 pts `HAVING SUM(a.hours_worked) > 100` (group-level filter, not WHERE), 1 pt correct `COUNT`/`SUM` aliases, 1 pt `ORDER BY total_hours DESC`. Full credit only if the WHERE/HAVING split is correct — using `HAVING` for the active-status filter or `WHERE` for the 100-hour filter should lose 2 pts, since this tests the exact WHERE-vs-HAVING distinction from Week 3/4.

### A2 (10 pts)
```sql
WITH ranked_employees AS (
    SELECT department, first_name, last_name, salary,
           ROW_NUMBER() OVER (
               PARTITION BY department ORDER BY salary DESC
           ) AS rank_in_department
    FROM employees
)
SELECT department, first_name, last_name, salary, rank_in_department
FROM ranked_employees
WHERE rank_in_department <= 2
ORDER BY department, rank_in_department;
```
**Explanation (expected):** `GROUP BY` with `MAX(salary)` collapses each department into a single row and can only return the single highest salary (and loses the employee's identity, especially if salaries tie) — it cannot return the "top 2" individual employee rows per group. A window function like `ROW_NUMBER() OVER (PARTITION BY ...)` ranks rows within each partition **without collapsing them**, so we can filter to the top N per group afterward.

**Grading:** 3 pts correct CTE structure (`WITH ... AS (...)`), 3 pts correct window function syntax (`ROW_NUMBER()`/`RANK()` with `PARTITION BY department ORDER BY salary DESC`), 2 pts correct outer filter (`rank_in_department <= 2`), 2 pts correct/clear explanation of why GROUP BY alone is insufficient. Accept `RANK()` or `DENSE_RANK()` in place of `ROW_NUMBER()` with equivalent reasoning.

---

## Suggested Grading Summary Table

| Section | Points |
|---------|--------|
| Part 1: Multiple Choice (15 × 2 pts) | 30 |
| S1 | 10 |
| S2 | 10 |
| I1 | 15 |
| I2 | 15 |
| A1 | 10 |
| A2 | 10 |
| **Total** | **100** |
