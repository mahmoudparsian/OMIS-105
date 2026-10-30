# DuckDB Subqueries & CTEs on One Table: <br> A Beginner's Guide

Welcome! If you are learning DuckDB (or standard SQL), subqueries are one of the most powerful tools to add to your toolkit.

A **subquery** is simply a query nested inside another SQL query. Think of it like solving a math problem inside parentheses first before completing the full equation.

---

## 1. Setting Up the Dataset

Let's start by creating a simple table named `employees` in DuckDB.

### Schema & Data Setup

```sql
CREATE OR REPLACE TABLE employees (
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

Quick facts you will use below:

| dept | employees | average salary |
| :--- | ---: | ---: |
| Engineering | Alice, Bob, Fiona | 93,333.33 |
| Marketing | Evan, George | 48,500.00 |
| Sales | Charlie, Diana | 55,000.00 |
| *(everyone)* | 7 people | 69,571.43 |

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
    salary > (SELECT AVG(salary) FROM employees)
ORDER BY 
    salary DESC;
```

### How DuckDB executes this:
1. First, it runs `(SELECT AVG(salary) FROM employees)` which returns `69571.43`.
2. Next, it evaluates `salary > 69571.43` for each row in `employees`.

**Result:**

| name  | dept        | salary |
| :---  | :---        | ---:   |
| Fiona | Engineering | 110000 |
| Alice | Engineering | 90000  |
| Bob   | Engineering | 80000  |

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
    )
ORDER BY 
    dept, name;
```

### How DuckDB executes this:
1. The inner query finds departments with young workers (`Engineering`, `Marketing`).
2. The outer query finds all employees who belong to either of those departments.

**Result:**

| name   | dept        | age |
| :---   | :---        | ---: |
| Alice  | Engineering | 30  |
| Bob    | Engineering | 28  |
| Fiona  | Engineering | 38  |
| Evan   | Marketing   | 24  |
| George | Marketing   | 29  |

Alice (30) and Fiona (38) are not under 30, but they are in the result. The subquery chooses **departments**; the outer query returns **everyone** in those departments.

> `DISTINCT` inside the subquery is optional. `IN` only checks whether a value is in the list, so duplicates in the list do not change the result.

---

## 4. Subqueries in the `FROM` Clause (Derived Tables)

You can also treat the output of a subquery as a temporary table and query against it.

### The Problem: Calculate department summary metrics, then find departments with an average salary greater than $60,000.

```sql
SELECT 
    dept, 
    ROUND(avg_salary, 2) AS avg_salary
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

**Result:**

| dept        | avg_salary |
| :---        | ---:       |
| Engineering | 93333.33   |

> **Why not just `WHERE AVG(salary) > 60000`?** `WHERE` runs *before* grouping, so it cannot see averages. You could use `HAVING` here instead — the derived table is useful when you want to treat the grouped result as a normal table and keep working with it.

> **Note:** Always give a subquery in the `FROM` clause an alias (like `AS dept_summary`). DuckDB lets you skip it, but many other databases require it.

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
    )
ORDER BY 
    e1.dept;
```

### How it works:
- `e1` and `e2` are two **aliases** (nicknames) for the same `employees` table: `e1` is the outer query, `e2` is the inner query.
- For every row in `e1`, the inner query calculates the average salary of *that employee's* department (`WHERE e2.dept = e1.dept`).
- Example: for Diana (Sales), the inner query averages Sales only → 55,000. Diana earns 60,000, so she is kept.

**Result:**

| name   | dept        | salary |
| :---   | :---        | ---:   |
| Fiona  | Engineering | 110000 |
| George | Marketing   | 52000  |
| Diana  | Sales       | 60000  |

Compare this with Section 2: George and Diana are **below** the company average, but **above** their own department's average.

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
    ROUND(avg_salary, 2) AS avg_salary,
    employee_count
FROM 
    dept_summary
WHERE 
    avg_salary > 60000;
```

Same result as Section 4 (Engineering, 93,333.33, now with `employee_count` = 3), but the steps read from top to bottom: first build `dept_summary`, then use it.

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
    nae.salary > da.avg_dept_salary
ORDER BY 
    nae.salary DESC;
```

**Result:**

| name  | dept        | salary | dept_avg |
| :---  | :---        | ---:   | ---:     |
| Fiona | Engineering | 110000 | 93333.33 |
| Diana | Sales       | 60000  | 55000.00 |

George is above his department average too, but he works in the UK, so the second CTE removed him.

> Notice the department averages are computed from **all** employees (including the UK). Only the final list of people is limited to North America. Where you filter changes the answer — always ask *"average of whom?"*

---

## 7. DuckDB Pro Tip: Friendly Syntax Shortcuts

DuckDB adds clean extensions to SQL syntax. For CTEs, you can skip the explicit `SELECT * FROM` in simple exploratory queries:

```sql
WITH high_earners AS (
    SELECT * FROM employees WHERE salary > 80000
)
FROM high_earners;  -- DuckDB lets you omit "SELECT *" if you want the whole table!
```

**Result:** Alice (90000) and Fiona (110000). Bob earns exactly 80000, which is not *greater than* 80000.

> This `FROM`-first shortcut works only in DuckDB. In exams and in other databases, write the full `SELECT * FROM high_earners;`.

---

## Summary Checklist

| Subquery Type | Used For | Example Operator |
| :--- | :--- | :--- |
| **Scalar Subquery** | Returns a single value (1 row, 1 col) | `>`, `<`, `=` |
| **Multi-row Subquery** | Returns a list of values (N rows, 1 col) | `IN`, `NOT IN`, `ANY`, `ALL` |
| **Derived Table** | Acts as a temporary dataset in `FROM` | Subquery aliased in `FROM` clause |
| **Correlated Subquery** | References column from outer query | `WHERE inner.col = outer.col` |
| **CTE (`WITH`)** | Organizes complex subqueries cleanly | `WITH name AS (...)` |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*