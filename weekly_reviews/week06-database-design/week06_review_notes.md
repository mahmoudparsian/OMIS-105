# OMIS 105 — Week 6 Review Notes: Database Design, Constraints & Views

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week06_review_notebook.py`. Open the notebook
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

## Homework

| Homework | Key Skill Tested |
|----------|-----------------|
| Design exercise: normalize a flat table to 3NF, add constraints, create a view, UPDATE/DELETE with before-and-after | Can they design and modify a database? |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
