# Mastering DuckDB Subqueries & Joins: A 2-Table Tutorial

Welcome to Part 2 of the DuckDB tutorial series! In this guide, we will step up from a single table to working with **two related tables**. 

You will learn how to:

1. Combine tables using **INNER JOIN**.
2. Filter data using subqueries across multiple tables (**IN**, **EXISTS**, **Scalar**).
3. Simplify multi-table queries using **Common Table Expressions (`WITH` clause)**.

---

## 1. Setting Up the Sample Schema & Data

We will create two tables:
* `departments`: Contains information about company departments and their location.
* `employees`: Contains employee details, linked to `departments` via `dept_id`.

```sql
-- Create departments table
CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name VARCHAR,
    location VARCHAR
);

-- Create employees table
CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    name VARCHAR,
    salary INTEGER,
    age INTEGER,
    dept_id INTEGER
);

-- Insert sample departments
INSERT INTO departments VALUES
(101, 'Engineering', 'Austin'),
(102, 'Marketing',   'New York'),
(103, 'Sales',       'Chicago'),
(104, 'HR',          'Austin');

-- Insert sample employees
INSERT INTO employees VALUES
(1, 'Alice',   95000, 34, 101),
(2, 'Bob',     70000, 28, 101),
(3, 'Charlie', 82000, 45, 102),
(4, 'Diana',   60000, 29, 103),
(5, 'Evan',    55000, 23, 102),
(6, 'Fiona',   90000, 38, 101);
```

### Quick Visual of Our Data

**`departments`**

| dept_id | dept_name   | location |
| :---    | :---        | :---     |
| 101     | Engineering | Austin   |
| 102     | Marketing   | New York |
| 103     | Sales       | Chicago  |
| 104     | HR          | Austin   |

**`employees`**

| emp_id | name    | salary | age | dept_id |
| :---   | :---    | :---   | :---| :---    |
| 1      | Alice   | 95000  | 34  | 101     |
| 2      | Bob     | 70000  | 28  | 101     |
| 3      | Charlie | 82000  | 45  | 102     |
| 4      | Diana   | 60000  | 29  | 103     |
| 5      | Evan    | 55000  | 23  | 102     |
| 6      | Fiona   | 90000  | 38  | 101     |

---

## 2. Refresh: The Standard INNER JOIN

An `INNER JOIN` merges matching records from both tables based on a shared column (`dept_id`).

### Query: List all employees with their department name and location
```sql
SELECT 
    e.name, 
    e.salary, 
    d.dept_name, 
    d.location
FROM employees e
INNER JOIN departments d 
    ON e.dept_id = d.dept_id;
```

**Result:**

| name    | salary | dept_name   | location |
| :---    | :---   | :---        | :---     |
| Alice   | 95000  | Engineering | Austin   |
| Bob     | 70000  | Engineering | Austin   |
| Charlie | 82000  | Marketing   | New York |
| Diana   | 60000  | Sales       | Chicago  |
| Evan    | 55000  | Marketing   | New York |
| Fiona   | 90000  | Engineering | Austin   |

---

## 3. Subqueries with 2 Tables

Subqueries allow you to filter or aggregate data from one table to use as a condition for another table.

---

### Scenario A: List Subquery (`WHERE ... IN`)
**Goal:** Find all employees who work in departments located in **Austin**.

Instead of joining first, we can ask DuckDB to find the department IDs for Austin, then match employees to those IDs.

```sql
SELECT name, salary, dept_id
FROM employees
WHERE dept_id IN (
    SELECT dept_id 
    FROM departments 
    WHERE location = 'Austin'
);
```

**Step-by-Step Execution:**

1. Inner Query runs first: `SELECT dept_id FROM departments WHERE location = 'Austin'` → Returns `(101, 104)`.

2. Outer Query runs: Finds employees where `dept_id` is either `101` or `104`.

**Result:**

| name  | salary | dept_id |
| :---  | :---   | :---    |
| Alice | 95000  | 101     |
| Bob   | 70000  | 101     |
| Fiona | 90000  | 101     |

---

### Scenario B: Correlated Subquery (`WHERE EXISTS`)
**Goal:** Find departments that have at least one employee earning more than $80,000.

A **correlated subquery** refers to columns from the outer query (here, `d.dept_id`). It evaluates row-by-row for the outer table.

```sql
SELECT dept_name, location
FROM departments d
WHERE EXISTS (
    SELECT 1 
    FROM employees e
    WHERE e.dept_id = d.dept_id 
      AND e.salary > 80000
);
```

**Result:**

| dept_name   | location |
| :---        | :---     |
| Engineering | Austin   |
| Marketing   | New York |

---

### Scenario C: Scalar Subquery with JOIN
**Goal:** Find employees who earn **more than the average salary of the Engineering department**.

```sql
SELECT 
    e.name, 
    e.salary, 
    d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id
WHERE e.salary > (
    SELECT AVG(salary) 
    FROM employees 
    WHERE dept_id = 101
);
```

**Step-by-Step Execution:**

1. The subquery computes Engineering's average salary: `(95000 + 70000 + 90000) / 3 = 85000`.

2. The outer query joins `employees` and `departments` and filters for `salary > 85000`.

**Result:**

| name  | salary | dept_name   |
| :---  | :---   | :---        |
| Alice | 95000  | Engineering |
| Fiona | 90000  | Engineering |

---

## 4. Multi-Table `WITH` Subqueries (CTEs)

Common Table Expressions (CTEs) allow you to break complex multi-table logic into clean, readable modular steps.

---

### Scenario A: Aggregating First, Then Joining
**Goal:** Calculate the total payroll and employee count per department, showing only departments located in Austin or New York.

```sql
WITH dept_stats AS (
    -- Step 1: Calculate aggregates per department
    SELECT 
        dept_id,
        COUNT(*) AS total_employees,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
)
-- Step 2: Join summary stats back to department metadata
SELECT 
    d.dept_name,
    d.location,
    s.total_employees,
    ROUND(s.avg_salary, 2) AS avg_salary
FROM departments d
INNER JOIN dept_stats s 
    ON d.dept_id = s.dept_id
WHERE d.location IN ('Austin', 'New York');
```

**Result:**

| dept_name   | location | total_employees | avg_salary |
| :---        | :---     | :---            | :---       |
| Engineering | Austin   | 3               | 85000.00   |
| Marketing   | New York | 2               | 68500.00   |

---

### Scenario B: Chaining Multiple CTEs
**Goal:** Compare each employee's salary to their department's average salary using two chained `WITH` blocks.

```sql
WITH dept_averages AS (
    -- CTE 1: Compute average salary for each department
    SELECT 
        dept_id,
        AVG(salary) AS dept_avg_salary
    FROM employees
    GROUP BY dept_id
),
high_earners AS (
    -- CTE 2: Join employees with dept averages and filter above-average earners
    SELECT 
        e.name,
        e.dept_id,
        e.salary,
        da.dept_avg_salary
    FROM employees e
    INNER JOIN dept_averages da ON e.dept_id = da.dept_id
    WHERE e.salary > da.dept_avg_salary
)
-- Final Query: Join high earners with department names
SELECT 
    he.name,
    d.dept_name,
    he.salary,
    ROUND(he.dept_avg_salary, 2) AS dept_avg
FROM high_earners he
INNER JOIN departments d ON he.dept_id = d.dept_id;
```

**Result:**

| name    | dept_name   | salary | dept_avg |
| :---    | :---        | :---   | :---     |
| Alice   | Engineering | 95000  | 85000.00 |
| Charlie | Marketing   | 82000  | 68500.00 |
| Fiona   | Engineering | 90000  | 85000.00 |

---

## Cheat Sheet: When to Use Which Tool?

| Method | Best Used For |
| :--- | :--- |
| **`INNER JOIN`** | Combining columns from 2+ tables based on a key match. |
| **`WHERE ... IN (subquery)`** | Filtering table A using a list of values derived from table B. |
| **`WHERE EXISTS (subquery)`** | Checking if matching records exist in table B without returning extra columns. |
| **`WITH clause (CTE)`** | Pre-aggregating data from one table before joining it to another, or keeping long queries clean. |