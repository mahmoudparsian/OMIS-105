# OMIS 105 — Week 5 Review Notes: Advanced Joins & Set Operations

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week05_review_notebook.py`. Open the notebook
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

## Homework

| Homework | Key Skill Tested |
|----------|-----------------|
| 8 queries: 2 FULL OUTER JOIN, 1 CROSS JOIN, 2 SELF JOIN, 1 UNION, 2 anti-joins | Can they handle every join type and set operation? |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
