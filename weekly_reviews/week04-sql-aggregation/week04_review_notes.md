# OMIS 105 — Week 4 Review Notes: Advanced Aggregation & Window Functions

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week04_review_notebook.py`. Open the notebook
and teach from it; use these notes for timing, discussion prompts, and the
homework assignment.

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

## Homework

| Homework | Key Skill Tested |
|----------|-----------------|
| 8 queries: 3 window functions, 2 CASE, 1 ROLLUP, 2 CTEs | Can they analyze data without collapsing rows? |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
