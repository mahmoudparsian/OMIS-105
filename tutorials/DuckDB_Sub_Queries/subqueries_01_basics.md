# SQL Subqueries in DuckDB: A Step-by-Step Lesson Plan

Teaching subqueries effectively comes down to breaking the **"query inside a query"** concept into digestible steps using visual, relatable data. Because **DuckDB** is fast and requires zero setup, students can run live queries immediately using its native `VALUES` clause.

---

## 1. The Analogy: "Solve for X"

Before writing code, walk students through a real-world scenario.

* **Problem:** Find all employees who earn more than the company average.
* **Hurdle:** You cannot filter employees directly because you don't know the average salary yet.
* **Human Process:**
  1. **Calculate** the average salary (e.g., $82,000).
  2. **Filter** the employee list for anyone making > $82,000.

> **The Golden Rule:** A subquery is simply Step 1. SQL executes the inner query first, replaces it with the resulting value, and hands it off to the outer query.

---

## 2. Interactive Setup

Run this script to create a lightweight mock dataset in DuckDB:

```sql
CREATE TABLE employees AS 
SELECT * FROM (VALUES 
    ('Alice', 'Sales', 80000),
    ('Bob', 'Sales', 50000),
    ('Charlie', 'Eng', 120000),
    ('David', 'Eng', 90000),
    ('Eva', 'HR', 70000)
) AS t(name, department, salary);
```

---

## 3. Core Progression

### Level 1: Scalar Subqueries (Returns exactly 1 value)

Start here. Scalar subqueries map directly to the "Solve for X" mental model.

**Goal:** Find employees earning more than the company average.

1. **Inner Query (Step 1):** Calculate the average salary.
   ```sql
   SELECT AVG(salary) FROM employees;
   -- Output: 82000
   ```

2. **Outer Query (Step 2):** Embed the inner query using parentheses.
   ```sql
   SELECT name, salary 
   FROM employees 
   WHERE salary > (
       SELECT AVG(salary) 
       FROM employees
   );
   ```

> 💡 **Teaching Tip:** Highlight how DuckDB evaluates `(SELECT AVG(salary) FROM employees)` first, substitutes `82000`, and executes `WHERE salary > 82000`.

---

### Level 2: Multi-Row Subqueries (Returns a list)

When a subquery produces multiple values in a single column, use set comparison operators like `IN`.

**Goal:** Find all employees working in departments that have at least one employee earning over $100,000.

1. **Inner Query (Step 1):** List high-paying departments.
   ```sql
   SELECT department 
   FROM employees 
   WHERE salary > 100000;
   -- Output: ['Eng']
   ```

2. **Outer Query (Step 2):** Match department names against that list using `IN`.
   ```sql
   SELECT name, department 
   FROM employees 
   WHERE department IN (
       SELECT department 
       FROM employees 
       WHERE salary > 100000
   );
   ```

---

### Level 3: Subqueries in `FROM` (Derived Tables)

Treat subqueries as temporary in-memory tables that can be queried directly.

**Goal:** Find the highest average salary among all departments.

* **The Challenge:** SQL does not allow nested aggregate functions like `MAX(AVG(salary))`.
* **The Solution:** Calculate department averages first, then extract the maximum from that result set.

```sql
SELECT MAX(avg_sal) AS top_dept_avg
FROM (
    SELECT department, AVG(salary) AS avg_sal 
    FROM employees 
    GROUP BY department
) AS dept_averages;
```

> 💡 **DuckDB Note:** While DuckDB allows omitting aliases for derived tables, teaching students to explicitly name them (e.g., `AS dept_averages`) is a standard best practice across SQL dialects.

---

## 4. Common Pitfalls & Error Recognition

| Pitfall | Common Cause | Resolution |
| :--- | :--- | :--- |
| **Missing Parentheses** | Forgetting `()` around the inner query. | Always enclose subqueries inside parentheses. |
| **Cardinality Mismatch** | Using single-value operators (`>`, `=`, `<`) with subqueries returning multiple rows or columns. | Use `IN`, `ANY`, or `ALL` for multi-row queries, or restrict inner query output. |
| **Missing Table Aliases** | Querying a derived table without giving it a name. | Assign an explicit alias using `AS <name>` in the `FROM` clause. |

> 🛠 **Instructor Tip:** Trigger intentional errors live (e.g., `WHERE salary > (SELECT salary FROM employees)`) to show DuckDB's exact error messaging. Recognizing error logs builds student debugging confidence early on.