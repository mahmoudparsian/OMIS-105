# Step-by-Step Breakdown vs. Sub-query Solutions (DuckDB)

This guide breaks down each SQL problem step-by-step using intermediate Common Table Expressions (CTEs) or staged queries, showing how to arrive at the final result iteratively before combining the logic into a compact sub-query.

---

## Setup Schema & Data

```sql
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name VARCHAR,
    location VARCHAR,
    budget NUMERIC(12, 2)
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    name VARCHAR,
    department_id INTEGER,
    salary NUMERIC(10, 2),
    hire_date DATE
);

INSERT INTO departments VALUES 
    (101, 'Engineering', 'New York', 500000.00),
    (102, 'Marketing', 'San Francisco', 200000.00),
    (103, 'Sales', 'Chicago', 300000.00),
    (104, 'HR', 'New York', 150000.00),
    (105, 'Research', 'Austin', 400000.00);

INSERT INTO employees VALUES 
    (1, 'Alice', 101, 95000.00, '2021-03-15'),
    (2, 'Bob', 101, 120000.00, '2019-06-01'),
    (3, 'Charlie', 102, 70000.00, '2022-01-10'),
    (4, 'Diana', 102, 65000.00, '2023-04-18'),
    (5, 'Evan', 103, 85000.00, '2020-11-05'),
    (6, 'Fiona', 103, 90000.00, '2018-08-22'),
    (7, 'George', 101, 110000.00, '2020-02-14'),
    (8, 'Hannah', 104, 60000.00, '2021-09-30');
```

---

## Basic Query 1: Find departments that have at least one employee

### Multi-Step Approach (Building with CTEs)

* **Step 1:** Get a unique list of department IDs that appear in the `employees` table.
* **Step 2:** Join that list back to the `departments` table to retrieve details.

```sql
WITH active_department_ids AS (
    -- Step 1: Extract distinct department IDs assigned to employees
    SELECT DISTINCT department_id 
    FROM employees
)
-- Step 2: Fetch department details matching those IDs
SELECT 
    d.department_id, 
    d.department_name, 
    d.location
FROM departments d
JOIN active_department_ids a 
    ON d.department_id = a.department_id;
```

### Combined Sub-query Approach (`EXISTS`)

```sql
SELECT 
    d.department_id, 
    d.department_name, 
    d.location 
FROM departments d
WHERE EXISTS (
    SELECT 1 
    FROM employees e 
    WHERE e.department_id = d.department_id
);
```

---

## Basic Query 2: Find departments that have NO employees assigned

### Multi-Step Approach (Building with CTEs)

* **Step 1:** Count the number of employees per department.
* **Step 2:** Join all departments with the employee counts and filter where count is 0 or null.

```sql
WITH dept_employee_counts AS (
    -- Step 1: Count employees per department ID
    SELECT 
        department_id, 
        COUNT(employee_id) AS emp_count
    FROM employees
    GROUP BY department_id
)
-- Step 2: Join departments to counts and find missing or zero-count departments
SELECT 
    d.department_id, 
    d.department_name, 
    d.location
FROM departments d
LEFT JOIN dept_employee_counts c 
    ON d.department_id = c.department_id
WHERE c.emp_count IS NULL OR c.emp_count = 0;
```

### Combined Sub-query Approach (`NOT EXISTS`)

```sql
SELECT 
    d.department_id, 
    d.department_name, 
    d.location 
FROM departments d
WHERE NOT EXISTS (
    SELECT 1 
    FROM employees e 
    WHERE e.department_id = d.department_id
);
```

---

## Basic+ Query 3: Find employees earning more than their department's average salary

### Multi-Step Approach (Building with CTEs)

* **Step 1:** Calculate the average salary for each department.
* **Step 2:** Join the employee details with the calculated averages and filter employees whose salary exceeds that average.

```sql
WITH department_averages AS (
    -- Step 1: Compute average salary per department
    SELECT 
        department_id, 
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
)
-- Step 2: Compare employee salaries against their department's average
SELECT 
    e.employee_id,
    e.name, 
    e.department_id, 
    e.salary,
    ROUND(da.avg_salary, 2) AS dept_avg_salary
FROM employees e
JOIN department_averages da 
    ON e.department_id = da.department_id
WHERE e.salary > da.avg_salary;
```

### Combined Sub-query Approach (Correlated Sub-query)

```sql
SELECT 
    e.employee_id,
    e.name, 
    e.department_id, 
    e.salary
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary) 
    FROM employees e2 
    WHERE e2.department_id = e.department_id
);
```

---

## Basic+ Query 4: Find departments in 'New York' that employ high earners (salary > 100,000)

### Multi-Step Approach (Building with CTEs)

* **Step 1:** Filter employees earning more than $100,000.
* **Step 2:** Filter departments located in 'New York'.
* **Step 3:** Find matching departments present in both filtered sets.

```sql
WITH high_earners AS (
    -- Step 1: Identify department IDs containing high earners
    SELECT DISTINCT department_id
    FROM employees
    WHERE salary > 100000.00
),
ny_departments AS (
    -- Step 2: Identify departments in New York
    SELECT department_id, department_name, budget
    FROM departments
    WHERE location = 'New York'
)
-- Step 3: Combine filtered CTE results
SELECT 
    ny.department_id, 
    ny.department_name, 
    ny.budget
FROM ny_departments ny
JOIN high_earners he 
    ON ny.department_id = he.department_id;
```

### Combined Sub-query Approach (`EXISTS` with Multi-Conditions)

```sql
SELECT 
    d.department_id, 
    d.department_name, 
    d.budget
FROM departments d
WHERE d.location = 'New York'
  AND EXISTS (
      SELECT 1 
      FROM employees e 
      WHERE e.department_id = d.department_id 
        AND e.salary > 100000.00
  );
```