# OMIS 105 — Lecture Notes: Weeks 4–6

**Course:** OMIS 105 — Introduction to Database Management Systems  
**Author:** Dr. Mahmoud Parsian  
**Quarter:** Fall 2026  
**Guest Instructor:** Claude  

---

## Prerequisites (Weeks 1–3)

Students are expected to know: SELECT, FROM, WHERE (AND/OR/IN/BETWEEN/LIKE), ORDER BY, LIMIT, DISTINCT, COUNT/SUM/AVG/MIN/MAX, basic GROUP BY and HAVING, basic INNER JOIN and LEFT JOIN, PRIMARY KEY, FOREIGN KEY, and simple subqueries.

Weeks 4–6 build on these foundations. We do not repeat them.

---

## Our New Dataset: A Tech Company

We use a fresh dataset modeled on a mid-size tech company with 30 employees across 5 departments. This gives us enough variety for window functions, advanced joins, and normalization exercises.

### Tables

| Table | Rows | Purpose |
|-------|------|---------|
| departments | 5 | Department info with budget and location |
| employees | 30 | Employee info with salary, hire_date, manager_id |
| projects | 8 | Company projects with budget and status |
| assignments | 25 | Which employee works on which project (many-to-many) |

### Key Data Design Choices

- **manager_id** in employees points back to the same table → enables SELF JOIN
- Some employees have **no department** (NULL dept_id) → enables FULL OUTER JOIN scenarios
- Some departments have **no employees** → enables anti-join patterns
- **Salary variety** across departments → rich window function examples
- **hire_date spread** (2018–2025) → time-based analytics
- **projects** with different statuses → CASE expression scenarios
- **assignments** bridge table → many-to-many relationship for normalization discussion

---
---

# Week 4 — Advanced Aggregation (Lectures 7–8)

## Lecture 7 (2 hours): Window Functions — Analytics Without Collapsing Rows

### Opening Discussion (15 min)

I'd start with a problem that GROUP BY cannot solve cleanly:

> "Show every employee's name, salary, AND their department's average salary — all in one row."

With GROUP BY, you'd need a subquery or a self-join because GROUP BY collapses rows. Ask students to try it — they'll struggle. Then reveal window functions as the elegant solution.

### Core Concept: What Is a Window Function?

A window function computes a value across a set of rows (the "window") related to the current row, **without collapsing rows into groups**. This is the key difference from GROUP BY.

```
GROUP BY:    30 rows → 5 rows (one per department)
Window Fn:   30 rows → 30 rows (each with a department-level calculation)
```

### The OVER() Clause

Every window function uses `OVER()` to define its window:

```sql
AVG(salary) OVER (PARTITION BY dept_id)
```

- `PARTITION BY dept_id` = "compute separately for each department"
- Without PARTITION BY = "compute across ALL rows"

### Topics to Cover

**1. Aggregate Window Functions**

Using familiar functions (AVG, SUM, COUNT, MIN, MAX) but with OVER():

```sql
SELECT emp_name, department, salary,
       AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg,
       salary - AVG(salary) OVER (PARTITION BY dept_id) AS diff_from_avg
FROM employees
```

This answers: "How does each employee compare to their department average?" — a question managers ask constantly.

**2. Ranking Functions: ROW_NUMBER, RANK, DENSE_RANK**

Business context: "Rank employees by salary within each department."

| Function | Ties | Gaps | Example for salaries 100, 90, 90, 80 |
|----------|------|------|--------------------------------------|
| ROW_NUMBER() | Breaks ties arbitrarily | No gaps | 1, 2, 3, 4 |
| RANK() | Same rank for ties | Gaps after ties | 1, 2, 2, 4 |
| DENSE_RANK() | Same rank for ties | No gaps | 1, 2, 2, 3 |

Live demo all three on the same query so students can see the difference side-by-side.

**3. LAG and LEAD — Looking at Neighboring Rows**

Business context: "For each employee (sorted by hire date), show who was hired before and after them."

```sql
LAG(emp_name) OVER (ORDER BY hire_date)   -- previous row
LEAD(emp_name) OVER (ORDER BY hire_date)  -- next row
```

Also useful for: "What's the salary difference between consecutive hires?"

**4. Running Totals — ROWS BETWEEN**

Business context: "Show a running total of salaries ordered by hire date."

```sql
SUM(salary) OVER (ORDER BY hire_date 
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

This is how financial reports compute cumulative figures.

### Discussion Points

- When would a business analyst use ROW_NUMBER vs RANK? (Tie-breaking matters: top-3 performers vs top-3 scores)
- How is a running total useful in finance? (Cumulative revenue, budget burn-down)
- Why doesn't GROUP BY work for "each row alongside its group average"?

---

## Lecture 8 (2 hours): CASE, ROLLUP/CUBE, and CTEs

### CASE Expressions (45 min)

**The SQL "if-then-else."** Business context: "Classify employees into salary bands."

```sql
CASE
    WHEN salary >= 150000 THEN 'Senior'
    WHEN salary >= 100000 THEN 'Mid-Level'
    ELSE 'Junior'
END AS salary_band
```

Show CASE in three positions:
1. **In SELECT** — create new computed columns (salary bands, status labels)
2. **In WHERE** — conditional filtering (less common, but useful)
3. **Inside aggregates** — conditional counting:

```sql
COUNT(CASE WHEN gender = 'Female' THEN 1 END) AS female_count
```

This is the "pivot by hand" technique — incredibly useful in business reporting.

### ROLLUP and CUBE (30 min)

Business context: "I want subtotals and a grand total in my report."

**ROLLUP** adds subtotals hierarchically:
```sql
GROUP BY ROLLUP(department, gender)
-- Gives: (dept, gender), (dept), (grand total)
```

**CUBE** adds subtotals for ALL combinations:
```sql
GROUP BY CUBE(department, gender)
-- Gives: (dept, gender), (dept), (gender), (grand total)
```

Show the difference side-by-side. ROLLUP is for hierarchical reports (region → city → store). CUBE is for cross-tabulation (every combination).

### Common Table Expressions — CTEs (45 min)

**The named subquery.** CTEs make complex queries readable by breaking them into named steps.

Business context: "Find employees who earn more than their department average."

Without CTE (nested, hard to read):
```sql
SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees e2 
                WHERE e2.dept_id = employees.dept_id)
```

With CTE (clear, step-by-step):
```sql
WITH dept_avg AS (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
)
SELECT e.emp_name, e.salary, d.avg_salary
FROM employees e
JOIN dept_avg d ON e.dept_id = d.dept_id
WHERE e.salary > d.avg_salary
```

Cover:
- Single CTE (most common)
- Multiple CTEs chained together
- CTE vs subquery — when to use which (readability, reuse)

### Discussion Points

- When have you seen "salary bands" or "tier classifications" in business? (Credit scores, customer segments, performance ratings)
- Why would a CFO want ROLLUP in a financial report? (Subtotals by region, division, grand total)
- How does a CTE improve code review and team collaboration? (Named steps = self-documenting SQL)

---
---

# Week 5 — Advanced Joins (Lectures 9–10)

## Lecture 9 (2 hours): FULL OUTER JOIN, CROSS JOIN, and SELF JOIN

### Opening Discussion (10 min)

"In weeks 1–3 you learned INNER JOIN (matching rows only) and LEFT JOIN (keep all from the left). Today we complete the picture with three more join types, each solving a specific business problem."

### FULL OUTER JOIN (40 min)

**The problem:** "Show ALL employees and ALL departments — even employees with no department and departments with no employees."

Neither LEFT JOIN nor RIGHT JOIN alone can do this. FULL OUTER JOIN keeps unmatched rows from BOTH sides.

```sql
SELECT e.emp_name, d.dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.dept_id
```

Rows with no match on either side get NULLs. This is essential for reconciliation reports: "Which records exist in System A but not System B, and vice versa?"

Show the Venn diagram: INNER = intersection, LEFT = left circle, RIGHT = right circle, FULL OUTER = entire Venn diagram.

### CROSS JOIN (30 min)

**The problem:** "Generate every possible employee-project combination."

CROSS JOIN produces the Cartesian product — every row from table A paired with every row from table B. No ON clause.

```sql
SELECT e.emp_name, p.project_name
FROM employees e
CROSS JOIN projects p
```

30 employees × 8 projects = 240 rows. Seems wasteful, but has real uses:
- Generate all possible (date, product) combinations for a sales report (so days with zero sales still appear)
- Create a grid of all (store, product) pairs for inventory planning

Warn students: CROSS JOIN on large tables creates enormous results. Always use intentionally.

### SELF JOIN (40 min)

**The problem:** "Show each employee alongside their manager's name."

The manager_id column points to another row in the SAME table. To "look up" the manager's name, we join the employees table to itself:

```sql
SELECT e.emp_name AS employee,
       m.emp_name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id
```

Why LEFT JOIN? Because the CEO has no manager (manager_id IS NULL) — we still want to see them.

Additional self-join examples:
- "Find pairs of employees in the same department"
- "Find employees who earn more than their manager"

### Discussion Points

- When would an auditor need a FULL OUTER JOIN? (Reconciling two data sources)
- Why is CROSS JOIN dangerous on big tables? (Exponential row count)
- What real-world hierarchies use self-referencing? (Org charts, folder structures, category trees)

---

## Lecture 10 (2 hours): Set Operations and Anti-Joins

### Set Operations: UNION, INTERSECT, EXCEPT (60 min)

These combine the RESULTS of two queries (not the tables themselves).

**Key rule:** Both queries must have the same number of columns with compatible types.

**UNION / UNION ALL**

Business context: "Combine active and archived employee lists."

```sql
SELECT emp_name, dept FROM current_employees
UNION
SELECT emp_name, dept FROM archived_employees
```

- UNION removes duplicates
- UNION ALL keeps duplicates (faster — use when you know there are no duplicates or want to keep them)

**INTERSECT**

"Which employees appear in BOTH the bonus list and the high-performer list?"

```sql
SELECT emp_name FROM bonus_list
INTERSECT
SELECT emp_name FROM high_performers
```

**EXCEPT**

"Which employees are on the bonus list but NOT on the high-performer list?"

```sql
SELECT emp_name FROM bonus_list
EXCEPT
SELECT emp_name FROM high_performers
```

To demonstrate these, we'll create small temporary tables in the notebook.

### Anti-Joins: Finding What's Missing (30 min)

Two equivalent patterns for "find rows with no match":

**Pattern 1: LEFT JOIN + IS NULL** (reviewed from Week 2, now formalized)
```sql
SELECT e.emp_name
FROM employees e
LEFT JOIN assignments a ON e.emp_id = a.emp_id
WHERE a.assignment_id IS NULL
```

**Pattern 2: NOT EXISTS**
```sql
SELECT e.emp_name
FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM assignments a
    WHERE a.emp_id = e.emp_id
)
```

**Pattern 3: NOT IN**
```sql
SELECT emp_name
FROM employees
WHERE emp_id NOT IN (SELECT emp_id FROM assignments)
```

Show all three producing the same result. Discuss trade-offs:
- LEFT JOIN + IS NULL: most visual, easiest to understand
- NOT EXISTS: most robust (handles NULLs correctly)
- NOT IN: simplest syntax, but breaks if the subquery returns NULLs

### JOIN Summary Table (10 min)

Put all join types together in one reference:

| Join Type | What It Returns | Use Case |
|-----------|----------------|----------|
| INNER JOIN | Only matching rows | Standard lookups |
| LEFT JOIN | All left + matching right | "Keep everyone, even with no match" |
| RIGHT JOIN | All right + matching left | Same as LEFT with tables swapped |
| FULL OUTER JOIN | All from both sides | Reconciliation, data comparison |
| CROSS JOIN | Every combination | Grids, calendars, test data |
| SELF JOIN | Table joined to itself | Hierarchies, comparisons within same table |

### Discussion Points

- When would EXCEPT be useful in data quality? (Finding records in staging that didn't make it to production)
- Why is NOT IN dangerous with NULLs? (If the subquery returns a NULL, NOT IN returns no rows at all)
- What's the business case for anti-joins? (Customers who haven't ordered, employees not assigned to projects)

---
---

# Week 6 — Database Design (Lectures 11–12)

## Lecture 11 (2 hours): Normalization — 1NF, 2NF, 3NF

### Opening Discussion (15 min)

"In Week 2, we saw that a flat table causes redundancy and anomalies, and we split it into multiple tables. That was normalization by intuition. Today we formalize it — there are specific rules called Normal Forms that tell us exactly when and how to split."

### Functional Dependencies (20 min)

Before normal forms, students need to understand functional dependencies:

**emp_id → emp_name** means "knowing the emp_id uniquely determines the emp_name."

This is the foundation of normalization — it tells us which columns depend on which keys.

Examples students can relate to:
- student_id → student_name (one ID, one name)
- zip_code → city, state (one zip, one city/state)
- (order_id, product_id) → quantity (one order-product pair, one quantity)

### First Normal Form (1NF) (20 min)

**Rule:** Every cell contains a single atomic value. No repeating groups, no arrays.

Bad (violates 1NF):
```
| emp_id | emp_name | skills              |
|--------|----------|---------------------|
| 1      | Alice    | Python, SQL, Java   |
```

Good (1NF):
```
| emp_id | emp_name | skill  |
|--------|----------|--------|
| 1      | Alice    | Python |
| 1      | Alice    | SQL    |
| 1      | Alice    | Java   |
```

Or better — a separate skills table with a bridge table.

### Second Normal Form (2NF) (25 min)

**Rule:** 1NF + every non-key column depends on the ENTIRE primary key (not just part of it).

Only relevant when the primary key is composite (multiple columns).

Bad (violates 2NF):
```
Primary key: (order_id, product_id)
Columns: quantity, product_name, product_price

product_name depends only on product_id, NOT on order_id
→ partial dependency → violates 2NF
```

Fix: Move product_name and product_price to a separate products table.

This is exactly what we did in weeks 1–3 when we split the flat orders table.

### Third Normal Form (3NF) (25 min)

**Rule:** 2NF + no column depends on another non-key column (no transitive dependencies).

Bad (violates 3NF):
```
| emp_id | emp_name | dept_id | dept_name | dept_location |

dept_name depends on dept_id (not on emp_id directly)
→ transitive dependency: emp_id → dept_id → dept_name
```

Fix: Move dept_name and dept_location to a separate departments table.

### Normalization Hands-On Exercise (15 min)

Give students a deliberately un-normalized table and have them:
1. Identify the violations (1NF? 2NF? 3NF?)
2. Decompose into normalized tables
3. Define primary and foreign keys
4. Write the CREATE TABLE statements in their notebook

### Discussion Points

- Is more normalization always better? (No — sometimes denormalization improves read performance)
- How do you decide when to stop normalizing? (3NF is sufficient for most business applications)
- What happens if you skip normalization? (Redundancy, anomalies, data integrity issues — exactly what we saw in Week 2)

---

## Lecture 12 (2 hours): Constraints, Views, and UPDATE/DELETE

### Constraints (40 min)

"Constraints are rules enforced by the database. You've seen PRIMARY KEY and FOREIGN KEY. Let's learn the rest."

| Constraint | What It Enforces | Example |
|-----------|-----------------|---------|
| PRIMARY KEY | Unique, not null identifier | `emp_id INTEGER PRIMARY KEY` |
| FOREIGN KEY | Must reference a valid row | `REFERENCES departments(dept_id)` |
| NOT NULL | Column cannot be empty | `emp_name VARCHAR NOT NULL` |
| UNIQUE | No duplicate values | `email VARCHAR UNIQUE` |
| CHECK | Custom validation rule | `CHECK (salary > 0)` |
| DEFAULT | Value when none is provided | `status VARCHAR DEFAULT 'Active'` |

Live demo: Try to INSERT a row that violates each constraint. Show the error message. Students learn that the database itself prevents bad data — you don't need application code to check.

### Views (30 min)

**A saved query that acts like a virtual table.**

```sql
CREATE VIEW high_earners AS
SELECT emp_name, department, salary
FROM employees
WHERE salary > 150000
```

Now `SELECT * FROM high_earners` works as if it were a real table.

Use cases:
- **Simplification:** Give business users a simple view instead of a complex JOIN query
- **Security:** Show only certain columns (hide salary, show everything else)
- **Reusability:** Define a complex query once, use it many times

### UPDATE and DELETE (40 min)

Now students learn to modify data, not just query it.

**UPDATE:**
```sql
UPDATE employees
SET salary = salary * 1.10
WHERE department = 'Engineering'
```

Always show BEFORE and AFTER snapshots. Emphasize: "UPDATE without WHERE changes EVERY row — this is the most dangerous SQL mistake."

**DELETE:**
```sql
DELETE FROM employees
WHERE emp_id = 30
```

Same warning: "DELETE without WHERE empties the entire table."

Best practice: Write the WHERE clause first, test it with SELECT, then change SELECT to UPDATE/DELETE.

**MERGE (UPSERT):**
Brief introduction to the concept — "insert if new, update if existing." This is a preview for more advanced courses.

### Discussion Points

- Why would a company use views for security? (HR view hides salary; Finance view hides personal details)
- What's the safest way to run an UPDATE? (SELECT first with the same WHERE, verify the rows, then change to UPDATE)
- When would you denormalize on purpose? (Read-heavy dashboards, data warehouses, reporting tables)

---
---

# Assessment Strategy for Weeks 4–6

| Week | Homework | Key Skills Tested |
|------|----------|------------------|
| 4 | 8 queries: 3 window functions, 2 CASE, 1 ROLLUP, 2 CTEs | Can they analyze data without collapsing rows? |
| 5 | 8 queries: 2 FULL OUTER JOIN, 1 CROSS JOIN, 2 SELF JOIN, 1 UNION, 2 anti-joins | Can they handle all join types and set operations? |
| 6 | Design exercise: normalize a flat table to 3NF + write constraints + create a view + UPDATE/DELETE with before/after | Can they design and modify a database? |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
