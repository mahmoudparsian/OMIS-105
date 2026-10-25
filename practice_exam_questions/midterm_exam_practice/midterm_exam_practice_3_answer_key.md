# OMIS 105 — Midterm Exam Practice Version 3 Answer Key (Weeks 1–5)

Instructor-only. Pair with `midterm_exam_practice_3.md`.

Database: Employees & Departments
(`github/weekly_lectures/week05-sql-joins/joins_with_emps_depts/`).
Every answer below was checked by running it against
`emps_depts_db.duckdb`.

Week 5 coverage follows the 2026-10-08 decision: JOINs, LEFT JOIN +
IS NULL, and COALESCE only — no window functions, CTEs, set
operations, or views.

---

## Part 1 — Multiple Choice (30 pts, 2 pts each)

| # | Answer | Topic | Why |
|---|--------|-------|-----|
| 1 | B | Week 1 — primary key | A primary key is unique and never `NULL`. It says nothing about value ranges (A), related rows (C), or storage order (D). |
| 2 | C | Week 1 — ORDER BY / LIMIT | `ORDER BY salary DESC` sorts highest first; `LIMIT` must come after `ORDER BY`. A sorts lowest first; B has the clauses in the wrong order; D is not valid SQL. Result: Rafa, Jane, Bob. |
| 3 | B | Week 1 — LIKE | `'%a'` means "ends with a lowercase a": Rafa, Diana. A lists every name with an a anywhere; Alice and Jane do not *end* in a. `LIKE` is case-sensitive. |
| 4 | B | Week 1 — DISTINCT | The distinct values are 10, 20, and `NULL`. `DISTINCT` treats `NULL` as one value, so it is its own row. |
| 5 | C | Week 2 — foreign key | Department 50 does not exist in `departments`, so the foreign key rejects it. 30 and 40 exist. `NULL` is allowed (the FK only checks non-`NULL` values). |
| 6 | B | Week 2 — GROUP BY / HAVING | A test on an aggregate must go in `HAVING`, after `GROUP BY`. A puts an aggregate in `WHERE` (invalid); C never groups; D has the clauses in the wrong order. Result: one row — dept 20, 160,000. (Dept 10 = 140,000; `NULL` group = 150,000, not *above* 150,000.) |
| 7 | A | Week 3 — NULL | `dept_id = NULL` is never true (it is `NULL`, "unknown"), so no rows match and `COUNT(*)` is 0. The correct test is `dept_id IS NULL`, which returns 2. |
| 8 | C | Week 3 — CASE | `CASE` stops at the first true `WHEN`. High: Rafa 82,000, Jane 80,000. Medium: Bob 78,000, Charlie 75,000, Diana 70,000 (`>=` includes 70,000). Low: Alice. |
| 9 | B | Week 3 — string functions | `SUBSTRING('Marketing', 1, 3)` = `'Mar'`; `UPPER` gives `'MAR'`. |
| 10 | C | Week 4 — COUNT variants | `COUNT(*)` counts rows (6); `COUNT(dept_id)` skips `NULL`s (4); `COUNT(DISTINCT dept_id)` counts different non-`NULL` values (10, 20 → 2). |
| 11 | A | Week 4 — INNER JOIN | Only matched rows: Alice, Bob, Rafa, Charlie. Diana and Jane (no department) and Sales and Finance (no employees) drop out. |
| 12 | D | Week 4 — Cartesian product | No join condition → every employee paired with every department: 6 × 4 = 24. |
| 13 | B | Week 5 — LEFT JOIN direction | The table whose rows must all be kept goes on the **left** of a `LEFT JOIN`. A keeps all employees (not departments); C drops Sales and Finance; D keeps all employees. (`employees RIGHT JOIN departments` would also be correct.) |
| 14 | B | Week 5 — COUNT(*) trap | Sales has one row after the `LEFT JOIN` (with `NULL` employee columns), and `COUNT(*)` counts rows, so it shows 1. `COUNT(e.emp_id)` would show 0. |
| 15 | C | Week 5 — FULL OUTER JOIN | 4 matched rows + 2 employees with no department + 2 departments with no employees = 8. |

---

## Part 2 — Written Questions (70 pts)

### S1 (10 pts) — Primary key vs. foreign key

**Expected points:**
- `departments.dept_id` is the **primary key** of `departments`: it
  uniquely identifies each department, and it can never be `NULL` or
  repeated.
- `employees.dept_id` is a **foreign key**: it points to
  `departments.dept_id` and links each employee to a department. Any
  value in it must already exist in `departments` (so `50` would be
  rejected).
- A foreign key only checks **non-`NULL`** values. `NULL` means "no
  department yet", which is allowed unless the column is also
  `NOT NULL`. That is why Diana and Jane can have `NULL`.

**Grading:** 3 pts PK, 4 pts FK and the link between the tables, 3
pts for the `NULL` explanation. Give partial credit for correct
general definitions without the schema example.

### S2 (10 pts) — Predict the LEFT JOIN result

| emp_name | dept_name |
|----------|-----------|
| Alice    | Engineering |
| Bob      | Marketing |
| Rafa     | Marketing |
| Charlie  | Engineering |
| Diana    | NULL |
| Jane     | NULL |

**Explanation (expected):** `LEFT JOIN` keeps every row of the left
table (`employees`). Diana and Jane have no matching department, so
the right-side columns (`dept_name`) are filled with `NULL`.

**Grading:** 6 pts for the table (1 pt per row; must be 6 rows in
`emp_id` order), 4 pts for the explanation. Deduct 3 pts if Diana and
Jane are missing (that is an INNER JOIN result). Deduct 2 pts if
Sales or Finance appear (they are not on the kept side).

### I1 (15 pts)

```sql
SELECT d.dept_name,
       COUNT(*)                AS num_employees,
       ROUND(AVG(e.salary), 2) AS avg_salary
FROM employees AS e
INNER JOIN departments AS d
    ON e.dept_id = d.dept_id
GROUP BY d.dept_name
ORDER BY avg_salary DESC;
```

**Result:**

| dept_name | num_employees | avg_salary |
|-----------|--------------:|-----------:|
| Marketing   | 2 | 80000.00 |
| Engineering | 2 | 70000.00 |

**Grading:** 4 pts `INNER JOIN` with the correct `ON`, 3 pts
`GROUP BY d.dept_name`, 3 pts `COUNT` and `AVG` with aliases, 2 pts
`ORDER BY ... DESC`, 3 pts correct result. Accept `COUNT(e.emp_id)`
and no `ROUND`. A `LEFT JOIN` from `departments` that also lists
Sales and Finance does **not** meet "at least one employee": deduct
3 pts unless they filter them out (e.g. `HAVING COUNT(e.emp_id) > 0`).

### I2 (15 pts)

```sql
SELECT d.dept_name,
       COUNT(e.emp_id)            AS num_employees,
       COALESCE(SUM(e.salary), 0) AS total_salary
FROM departments AS d
LEFT JOIN employees AS e
    ON d.dept_id = e.dept_id
GROUP BY d.dept_name
ORDER BY num_employees DESC, d.dept_name;
```

**Result:**

| dept_name | num_employees | total_salary |
|-----------|--------------:|-------------:|
| Engineering | 2 | 140000 |
| Marketing   | 2 | 160000 |
| Finance     | 0 | 0 |
| Sales       | 0 | 0 |

**Grading:** 5 pts `departments LEFT JOIN employees` (or
`employees RIGHT JOIN departments`), 3 pts `COUNT(e.emp_id)` — not
`COUNT(*)`, which gives 1 for Sales and Finance, 3 pts `COALESCE(...,
0)` on the sum, 2 pts `GROUP BY`, 2 pts both sort keys. Deduct 5 pts
for an `INNER JOIN` (Sales and Finance disappear).

### A1 (10 pts) — Finding the gaps

(a)

```sql
SELECT d.dept_id, d.dept_name
FROM departments AS d
LEFT JOIN employees AS e
    ON d.dept_id = e.dept_id
WHERE e.emp_id IS NULL;
```

(b)

```sql
SELECT e.emp_name
FROM departments AS d
RIGHT JOIN employees AS e
    ON d.dept_id = e.dept_id
WHERE d.dept_id IS NULL;
```

(c) (a) returns 30 Sales and 40 Finance. (b) returns Diana and Jane.

**Grading:** 4 pts (a): outer join with the correct table kept, and
`IS NULL` on the **other** table's column. 4 pts (b): must be a
`RIGHT JOIN` with `employees` on the right, and `IS NULL` on a
`departments` column. 2 pts (c). Give partial credit (2 of 4) for (b)
written as `SELECT emp_name FROM employees WHERE dept_id IS NULL`:
it gives the right answer here, but it is not a join, and it would
miss an employee whose `dept_id` points to a department that does not
exist. Deduct 2 pts for `= NULL` instead of `IS NULL`.

### A2 (10 pts) — WHERE can undo a LEFT JOIN

(a)

```sql
SELECT d.dept_name, COUNT(e.emp_id) AS num_high_earners
FROM departments AS d
LEFT JOIN employees AS e
    ON d.dept_id = e.dept_id
   AND e.salary >= 75000
GROUP BY d.dept_name
ORDER BY d.dept_name;
```

**Result:** Engineering 1 (Charlie), Finance 0, Marketing 2 (Bob,
Rafa), Sales 0.

(b) **Sales and Finance are missing.** After the `LEFT JOIN`, their
rows have `e.salary = NULL`. `NULL >= 75000` is not true, so `WHERE`
removes those rows *after* the join, and the query behaves like an
`INNER JOIN`. The classmate gets only Engineering 1 and Marketing 2.
Putting the test in the `ON` clause filters employees *before* the
match, so every department is still kept.

**Grading:** (a) 5 pts — 2 pts `departments LEFT JOIN employees`, 2
pts salary test in `ON`, 1 pt `COUNT(e.emp_id)`. (b) 5 pts — 2 pts
naming Sales and Finance, 3 pts explaining that `WHERE` runs after the
join and drops the `NULL` rows. Accept other correct versions of (a),
e.g. `SUM(CASE WHEN e.salary >= 75000 THEN 1 ELSE 0 END)` with a plain
`LEFT JOIN`.

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
