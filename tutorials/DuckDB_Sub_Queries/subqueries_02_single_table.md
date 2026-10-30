# Master DuckDB Subqueries & CTEs: <br> A Beginner's Guide

Welcome! If you are learning DuckDB (or standard SQL), subqueries are one of the most powerful tools to add to your toolkit. 

A **subquery** is simply a query nested inside another SQL query. Think of it like solving a math problem inside parentheses first before completing the full equation.

---

## 1. Setting Up the Dataset

Let's start by creating a simple table named `employees` in DuckDB.

### Schema & Data Setup

```sql
CREATE TABLE employees (
    name VARCHAR,
    dept VARCHAR,
    salary INT,
    age INT,
    country VARCHAR
);

INSERT INTO employees VALUES
    ('Alice',   'Engineering', 90000, 30, 'USA'),
    ('Bob',     'Engineering', 80000, 28, 'Canada'),
    ('Charlie', 'Sales',       50000, 35, 'USA'),
    ('Diana',   'Sales',       60000, 42, 'Canada'),
    ('Evan',    'Marketing',   45000, 24, 'UK'),
    ('Fiona',   'Engineering', 110000, 38, 'USA'),
    ('George',  'Marketing',   52000, 29, 'UK');
```

---

## 2. Scalar Subqueries (Returns a Single Value)

### The Problem: Find employees who earn more than the overall average salary.

To answer this, you need to answer two questions:

1. What is the average salary overall?

2. Which employees make more than that calculated number?

Instead of doing this in two manual steps, you can use a **scalar subquery** (a subquery that evaluates to a single value) directly in your `WHERE` clause.

```sql
SELECT 
    name, 
    dept, 
    salary
FROM 
    employees
WHERE 
    salary > (SELECT AVG(salary) FROM employees);
```

### How DuckDB executes this:
1. First, it runs `(SELECT AVG(salary) FROM employees)` which returns `69571.43`.
2. Next, it evaluates `salary > 69571.43` for each row in `employees`.

---

## 3. Subqueries with Lists (`IN` Operator)

### The Problem: Find employees working in departments that have at least one worker under 30 years old.

Here, the subquery returns a **list of values** rather than a single number.

```sql
SELECT 
    name, 
    dept, 
    age
FROM 
    employees
WHERE 
    dept IN (
        SELECT DISTINCT dept 
        FROM employees 
        WHERE age < 30
    );
```

### How DuckDB executes this:
1. The inner query finds departments with young workers (`Engineering`, `Marketing`).
2. The outer query finds all employees who belong to either of those departments.

---

## 4. Subqueries in the `FROM` Clause (Derived Tables)

You can also treat the output of a subquery as a temporary table and query against it.

### The Problem: Calculate department summary metrics, then find departments with an average salary greater than $60,000.

```sql
SELECT 
    dept, 
    avg_salary
FROM (
    SELECT 
        dept, 
        AVG(salary) AS avg_salary
    FROM 
        employees
    GROUP BY 
        dept
) AS dept_summary
WHERE 
    avg_salary > 60000;
```

> **Note:** Subqueries in the `FROM` clause **must** have an alias (like `AS dept_summary`).

---

## 5. Correlated Subqueries

A **correlated subquery** is a subquery that depends on values from the outer query for its evaluation.

### The Problem: Find employees who earn more than the average salary *of their specific department*.

```sql
SELECT 
    e1.name, 
    e1.dept, 
    e1.salary
FROM 
    employees e1
WHERE 
    e1.salary > (
        SELECT AVG(e2.salary)
        FROM employees e2
        WHERE e2.dept = e1.dept
    );
```

### How it works:
- For every row in `e1` ( outer query ), DuckDB calculates the average salary for that employee's department in `e2` ( inner query ).

---

## 6. Better Readability: `WITH` Subqueries (Common Table Expressions - CTEs)

As queries grow complex, nesting subqueries inside subqueries makes SQL hard to read and debug. 

The `WITH` clause allows you to write subqueries first, assign them a clean name, and reference them later. These are called **Common Table Expressions (CTEs)**.

### Example 1: Re-writing the Department Summary Query

```sql
WITH dept_summary AS (
    SELECT 
        dept, 
        AVG(salary) AS avg_salary,
        COUNT(*) AS employee_count
    FROM 
        employees
    GROUP BY 
        dept
)
SELECT 
    dept, 
    avg_salary
FROM 
    dept_summary
WHERE 
    avg_salary > 60000;
```

### Example 2: Chaining Multiple `WITH` Subqueries

You can define multiple CTEs separated by commas.

```sql
-- Goal: Find employees earning above their 
--       department average in Canada or USA
WITH dept_averages AS (
    SELECT 
        dept, 
        AVG(salary) AS avg_dept_salary
    FROM 
        employees
    GROUP BY 
        dept
),
north_america_employees AS (
    SELECT 
        name, 
        dept, 
        salary, 
        country
    FROM 
        employees
    WHERE 
        country IN ('USA', 'Canada')
)
SELECT 
    nae.name, 
    nae.dept, 
    nae.salary, 
    ROUND(da.avg_dept_salary, 2) AS dept_avg
FROM 
    north_america_employees nae
JOIN 
    dept_averages da ON nae.dept = da.dept
WHERE 
    nae.salary > da.avg_dept_salary;
```

---

## 7. DuckDB Pro Tip: Friendly Syntax Shortcuts

DuckDB adds clean extensions to SQL syntax. For CTEs, you can skip the explicit `SELECT * FROM` in simple exploratory queries:

```sql
WITH high_earners AS (
    SELECT * FROM employees WHERE salary > 80000
)
FROM high_earners;  -- DuckDB lets you omit "SELECT *" if you want the whole table!
```

---

## Summary Checklist

| Subquery Type | Used For | Example Operator |
| :--- | :--- | :--- |
| **Scalar Subquery** | Returns a single value (1 row, 1 col) | `>`, `<`, `=` |
| **Multi-row Subquery** | Returns a list of values (N rows, 1 col) | `IN`, `NOT IN`, `ANY`, `ALL` |
| **Derived Table** | Acts as a temporary dataset in `FROM` | Subquery aliased in `FROM` clause |
| **Correlated Subquery** | References column from outer query | `WHERE inner.col = outer.col` |
| **CTE (`WITH`)** | Organizes complex subqueries cleanly | `WITH name AS (...)` |