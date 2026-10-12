# OMIS 105 — Database Management Systems
## Midterm Exam — Practice Version (Weeks 1–5)

**Instructor:** Dr. Parsian

**Coverage:** 

* Week 1 (Database Foundations) 
* Week 2 (Relational Modeling)
* Week 3 (SQL Basics, Functions, GROUP BY/HAVING)
* Week 4 (JOINs) 
* Week 5 (JOIN Deep Dive, Window Functions, CTEs, Set Operations)

**Total Points:** 

* 100 
	* Part 1: 30 pts
	* Part 2: 70 pts

---

## Reference Schema — Project Tracker

All questions referencing tables use the following **ProjectTracker** company database. Assume the following schema:

```sql
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name  VARCHAR NOT NULL,
    last_name   VARCHAR NOT NULL,
    email       VARCHAR UNIQUE NOT NULL,
    department  VARCHAR,
    salary      DECIMAL(10,2) CHECK (salary > 0),
    hire_date   DATE
);

CREATE TABLE projects (
    project_id   INTEGER PRIMARY KEY,
    project_name VARCHAR NOT NULL,
    budget       DECIMAL(12,2),
    status       VARCHAR CHECK (status IN ('planned','active','completed')),
    start_date   DATE
);

CREATE TABLE assignments (
    employee_id  INTEGER REFERENCES employees(employee_id),
    project_id   INTEGER REFERENCES projects(project_id),
    role         VARCHAR,
    hours_worked INTEGER,
    PRIMARY KEY (employee_id, project_id)
);
```

A row in `assignments` means "this employee is (or was) staffed on this project." `hours_worked` is `NULL` until the employee has logged any time on the project.

Keep this schema visible while answering both parts of the exam.

---

# Part 1 — Multiple Choice (30 points, 2 pts each)

Circle/select the single best answer for each question.

### 1. (Week 1) Which best describes what a Database Management System (DBMS) does?
A) It is a general-purpose programming language for writing web applications

B) It is software that manages the storage, retrieval, and security of data on behalf of applications, and enforces structure via a schema

C) It is a single file that stores unstructured text

D) It is a version-control system for tracking changes to source code

### 2. (Week 1) Which column type is best for `employees.salary`, so a value like `82500.50` is stored exactly, without floating-point rounding errors?

A) `INTEGER`

B) `VARCHAR`

C) `DECIMAL(10,2)`

D) `BOOLEAN`

### 3. (Week 1) Which constraint guarantees that no employee can ever be inserted with a `salary` of `0` or less?

A) `UNIQUE`

B) `NOT NULL`

C) `DEFAULT`

D) `CHECK (salary > 0)`

### 4. (Week 2) In `assignments`, `employee_id` is a **foreign key**. What does this enforce?

A) It uniquely identifies each row in `assignments`

B) It must reference an existing `employee_id` in `employees`, so an assignment can't exist for an employee who doesn't exist

C) It automatically calculates the employee's total hours worked

D) It stores a duplicate copy of the employee's name inside `assignments`

### 5. (Week 2) An employee can be staffed on many projects, and a project can have many employees. Why does the schema use a separate `assignments` table instead of adding a `project_id` column directly to `employees`?

A) Because `employees` already has too many columns

B) Because `assignments` is a junction (bridge) table needed to represent a many-to-many relationship

C) Because DuckDB does not allow foreign keys inside `employees`

D) Because `project_id` must always be a primary key

### 6. (Week 2) In `assignments`, neither `employee_id` nor `project_id` is unique by itself, but the pair `(employee_id, project_id)` is declared as the primary key. What is this called?

A) A candidate key

B) A composite (compound) primary key

C) A surrogate key

D) A natural key

### 7. (Week 3) An HR manager asks: "Which departments have an average salary above $80,000?" Which query answers this correctly?

A)

```sql
SELECT department, AVG(salary) AS avg_salary
FROM employees
WHERE AVG(salary) > 80000
GROUP BY department;
```

B)

```sql
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 80000;
```

C)

```sql
SELECT department, AVG(salary) AS avg_salary
FROM employees
HAVING AVG(salary) > 80000
GROUP BY department;
```

D)

```sql
SELECT department, salary
FROM employees
WHERE salary > 80000
GROUP BY department;
```

### 8. (Week 3) Which query correctly finds all assignments where `hours_worked` has **not yet been logged** (is missing)?

A) `SELECT * FROM assignments WHERE hours_worked = NULL;`

B) `SELECT * FROM assignments WHERE hours_worked IS NULL;`

C) `SELECT * FROM assignments WHERE hours_worked == NULL;`

D) `SELECT * FROM assignments WHERE hours_worked <> NULL;`

### 9. (Week 3) Which query correctly returns employees whose `salary` is above the **overall average salary** of all employees?

A)

```sql
SELECT first_name, last_name, salary
FROM employees
WHERE salary > AVG(salary);
```

B)

```sql
SELECT first_name, last_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

C)

```sql
SELECT first_name, last_name, salary
FROM employees
GROUP BY salary
HAVING salary > AVG(salary);
```

D)

```sql
SELECT first_name, AVG(salary)
FROM employees;
```

### 10. (Week 3) In logical query execution order, which clause runs immediately **after** `GROUP BY` and filters the resulting groups?

A) `WHERE`

B) `SELECT`

C) `HAVING`

D) `ORDER BY`

### 11. (Week 4) HR wants a report listing **every employee**, including those not currently staffed on any project, alongside any assignment they do have. Which query is correct?

A)

```sql
SELECT e.first_name, a.project_id
FROM employees e
INNER JOIN assignments a ON e.employee_id = a.employee_id;
```

B)

```sql
SELECT e.first_name, a.project_id
FROM employees e
LEFT JOIN assignments a ON e.employee_id = a.employee_id;
```

C)

```sql
SELECT e.first_name, a.project_id
FROM employees e, assignments a;
```

D)

```sql
SELECT e.first_name, a.project_id
FROM employees e
RIGHT JOIN assignments a ON e.employee_id = a.employee_id;
```

### 12. (Week 4) What is the main risk of writing a join like this?
```sql
SELECT e.first_name, a.project_id
FROM employees e, assignments a;
```

A) It will raise a syntax error in DuckDB

B) It produces a Cartesian product — every employee paired with every assignment row — because there is no join condition

C) It automatically defaults to an INNER JOIN on `employee_id`

D) It only returns employees who are not staffed on anything

### 13. (Week 4) Which query correctly lists each employee's `first_name`, the `project_name` they're staffed on, `hours_worked`, and their `role`, by joining `assignments`, `employees`, and `projects`?

A)

```sql
SELECT e.first_name, p.project_name, a.hours_worked, a.role
FROM assignments a
INNER JOIN employees e ON a.employee_id = e.employee_id
INNER JOIN projects p ON a.project_id = p.project_id;
```

B)

```sql
SELECT e.first_name, p.project_name, a.hours_worked, a.role
FROM assignments a
INNER JOIN employees e ON a.project_id = e.employee_id
INNER JOIN projects p ON a.project_id = p.project_id;
```

C)

```sql
SELECT e.first_name, p.project_name, a.hours_worked, a.role
FROM assignments a
INNER JOIN employees e
INNER JOIN projects p ON a.project_id = p.project_id;
```

D)

```sql
SELECT e.first_name, p.project_name, a.hours_worked, a.role
FROM assignments a, employees e, projects p
WHERE a.employee_id = p.project_id;
```

### 14. (Week 5) What does the following query return?

```sql
SELECT first_name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS salary_rank
FROM employees;
```

A) One row per department showing only the single highest-paid employee

B) Every employee row, ranked by salary from highest to lowest *within their own department*, with ranking restarting for each department

C) A single number representing the total count of employees

D) The average salary for each department

### 15. (Week 5) HR wants the `employee_id`s of employees who are staffed on **"Project Phoenix"** but have **never** been staffed on **"Project Atlas."** Which set operation correctly expresses this?

A)

```sql
SELECT a.employee_id FROM assignments a
JOIN projects p ON a.project_id = p.project_id
WHERE p.project_name = 'Project Phoenix'
UNION
SELECT a.employee_id FROM assignments a
JOIN projects p ON a.project_id = p.project_id
WHERE p.project_name = 'Project Atlas';
```

B)

```sql
SELECT a.employee_id FROM assignments a
JOIN projects p ON a.project_id = p.project_id
WHERE p.project_name = 'Project Phoenix'
INTERSECT
SELECT a.employee_id FROM assignments a
JOIN projects p ON a.project_id = p.project_id
WHERE p.project_name = 'Project Atlas';
```

C)

```sql
SELECT a.employee_id FROM assignments a
JOIN projects p ON a.project_id = p.project_id
WHERE p.project_name = 'Project Phoenix'
EXCEPT
SELECT a.employee_id FROM assignments a
JOIN projects p ON a.project_id = p.project_id
WHERE p.project_name = 'Project Atlas';
```

D)

```sql
SELECT a.employee_id FROM assignments a
JOIN projects p ON a.project_id = p.project_id
WHERE p.project_name = 'Project Atlas'
EXCEPT
SELECT a.employee_id FROM assignments a
JOIN projects p ON a.project_id = p.project_id
WHERE p.project_name = 'Project Phoenix';
```

---

# Part 2 — Written Questions (70 points)

Show your reasoning. For SQL questions, write a single query unless told otherwise; minor syntax slips are fine as long as the logic is correct.

## Simple (10 points each — 20 points total)

**S1.** In two or three sentences, explain the difference between a **primary key** and a **foreign key**. Use `employees.employee_id` and `assignments.employee_id` as your example.

**S2.** Explain the difference between the `WHERE` clause and the `HAVING` clause — specifically, *when* each one filters data (before or after grouping) and *what* each one is allowed to filter (individual rows vs. aggregated groups). Give one short example query using the `employees` table for each clause.

## Intermediate (15 points each — 30 points total)

**I1.** Write a SQL query against the ProjectTracker schema that returns the `project_name`, `budget`, and `status` of every project with a `status` of `"active"` and a `budget` above `$50,000`, sorted from largest to smallest budget.

**I2.** Write a SQL query that returns each employee's `first_name`, `last_name`, and their total number of project assignments (`num_projects`) — **including employees who are not currently staffed on any project**. Sort the result so employees with the most assignments appear first. (Hint: think carefully about which JOIN type keeps employees with no matching rows.)

## Advanced (10 points each — 20 points total)

**A1.** Write a single SQL query that finds every employee who has logged **more than 100 total hours** across projects with a `status` of `"active"` (only count hours from active projects). For each qualifying employee, return `first_name`, `last_name`, `num_projects` (count of their active-project assignments), and `total_hours` (sum of `hours_worked` on those active projects). Sort by `total_hours` descending. Your query must correctly combine a `JOIN` across all three tables, a row-level filter, `GROUP BY`, and a group-level filter.

**A2.** Using a **Common Table Expression (CTE)** and a **window function**, write a query that returns the **top 2 highest-paid employees in each department** (`department`, `first_name`, `last_name`, `salary`, and their rank within the department). Briefly explain (1–2 sentences) why a plain `GROUP BY` with `MAX(salary)` would not be enough to answer this question.

---

*End of Exam*
