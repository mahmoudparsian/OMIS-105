# Mastering DuckDB Subqueries & CTEs: A Beginner's Guide

Welcome to the beginner-friendly guide to DuckDB subqueries and Common Table Expressions (CTEs)!

Subqueries often intimidate beginners, but they are just separate SQL queries combined together to answer a complex question.

## 1. Setup: Sample Tables & Data

Run the following SQL script in DuckDB to create our two sample tables: **`employees`** and **`departments`**.

```sql
-- Create Departments Table
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name VARCHAR,
    location VARCHAR,
    budget NUMERIC(12, 2)
);

-- Create Employees Table
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    name VARCHAR,
    department_id INTEGER,
    salary NUMERIC(10, 2),
    hire_date DATE
);

-- Insert Sample Data
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

## Scenario 1: Scalar Subquery in `WHERE` (Single Value Comparison)

### **Question:**

Which employees earn more than the overall average employee salary?

### **Step-by-Step Without Subqueries:**

1. **Find the average salary across all employees:**

   ```sql
   SELECT AVG(salary) FROM employees;
   -- Result: 86875.00
   ```

2. **Hardcode that result into a second query:**

   ```sql
   SELECT name, salary 
   FROM employees 
   WHERE salary > 86875.00;
   ```

### **Glued Together (Subquery in `WHERE`)(solution-1):**

Replace the hardcoded value with the inner query enclosed in parentheses.

```sql
SELECT name, salary 
FROM employees 
WHERE salary > (
    SELECT AVG(salary) 
    FROM employees
);
```

### **Using `WITH` (CTE)(solution-2):**

```sql
WITH overall_avg AS (
    SELECT AVG(salary) AS avg_sal 
    FROM employees
)
SELECT e.name, e.salary 
FROM employees e, overall_avg oa
WHERE e.salary > oa.avg_sal;
```

### **Using `WITH` (CTE)(solution-3):**

```sql
WITH overall_avg AS (
    SELECT AVG(salary) AS avg_sal
    FROM employees
)
SELECT name, salary
FROM employees
WHERE salary > (SELECT avg_sal FROM overall_avg);
```

## Scenario 2: Multi-Row Subquery using `IN`

### **Question:**

Which employees work in departments located in 'New York'?

### **Step-by-Step Without Subqueries:**

1. **Get department IDs located in New York:**

   ```sql
   SELECT department_id 
   FROM departments 
   WHERE location = 'New York';
   -- Result: 101, 104
   ```

2. **Use those IDs to filter employees:**

   ```sql
   SELECT name, department_id 
   FROM employees 
   WHERE department_id IN (101, 104);
   ```

### **Glued Together (Subquery with `IN`):**

```sql
SELECT name, department_id 
FROM employees 
WHERE department_id IN (
    SELECT department_id 
    FROM departments 
    WHERE location = 'New York'
);
```

### **Using `WITH` (CTE):**

```sql
WITH ny_departments AS (
    SELECT department_id 
    FROM departments 
    WHERE location = 'New York'
)
SELECT name, department_id 
FROM employees 
WHERE department_id IN (SELECT department_id 
                        FROM ny_departments);
```

## Scenario 3: Correlated Subquery with `EXISTS`

### **Question:**

Which departments have at least one employee working in them?

### **Step-by-Step Without Subqueries:**

1. **Find distinct department IDs present in the employees table:**

   ```sql
   SELECT DISTINCT department_id FROM employees;
   -- Result: 101, 102, 103, 104
   ```

2. **Fetch those department details:**

   ```sql
   SELECT department_name 
   FROM departments 
   WHERE department_id IN (101, 102, 103, 104);
   ```

### **Glued Together (Correlated Subquery with `EXISTS`):**

The inner query checks if a matching row exists in `employees` for *each* department row.

```sql
SELECT d.department_name 
FROM departments d
WHERE EXISTS (
    SELECT 1 
    FROM employees e 
    WHERE e.department_id = d.department_id
);
```

### **Using `WITH` (CTE):**

```sql
WITH active_dept_ids AS (
    SELECT DISTINCT department_id 
    FROM employees
)
SELECT d.department_name 
FROM departments d
JOIN active_dept_ids a 
  ON d.department_id = a.department_id;
```

## Scenario 4: Subquery in `FROM` Clause (Derived Table)

### **Question:**

What is the average salary per department, and which departments have an average salary exceeding \$80,000?

### **Step-by-Step Without Subqueries:**

1. **Calculate average salaries per department:**

   ```sql
   SELECT department_id, 
          AVG(salary) AS avg_salary 
   FROM employees 
   GROUP BY department_id;
   ```

2. **Filter the aggregated results using `HAVING` (or conceptually querying the result set above):**

   ```sql
   SELECT department_id, avg_salary 
   FROM (/* table from step 1 */) 
   WHERE avg_salary > 80000;
   ```

### **Glued Together (Subquery in `FROM`):**

```sql
SELECT dept_summary.department_id, 
       dept_summary.avg_salary
FROM (
    SELECT department_id, 
           AVG(salary) AS avg_salary 
    FROM employees 
    GROUP BY department_id
) AS dept_summary
WHERE dept_summary.avg_salary > 80000;
```

### **Using `WITH` (CTE):**

```sql
WITH dept_averages AS (
    SELECT department_id, 
           AVG(salary) AS avg_salary 
    FROM employees 
    GROUP BY department_id
)
SELECT department_id, 
       avg_salary 
FROM dept_averages 
WHERE avg_salary > 80000;
```

## Scenario 5: Scalar Subquery in `SELECT` Clause

### **Question:**

List each employee's name, salary, and the difference between their salary and the overall company average salary.

### **Step-by-Step Without Subqueries:**

1. **Calculate overall average salary:**

   ```sql
   SELECT AVG(salary) 
   FROM employees;
   -- Result: 86875.00
   ```

2. **Compute difference for each employee manually:**

   ```sql
   SELECT name, 
          salary, 
          salary - 86875.00 AS diff_from_avg 
   FROM employees;
   ```

### **Glued Together (Subquery in `SELECT`):**

```sql
SELECT 
    name, 
    salary, 
    salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg 
FROM employees;
```

### **Using `WITH` (CTE):**

```sql
WITH company_stats AS (
    SELECT AVG(salary) AS avg_salary 
    FROM employees
)
SELECT 
    e.name, 
    e.salary, 
    e.salary - cs.avg_salary AS diff_from_avg
FROM employees e, company_stats cs;
```


### **Using `WITH` (CTE):**

```sql
WITH company_stats AS (
    SELECT AVG(salary) AS avg_salary
    FROM employees
)
SELECT
    name,
    salary,
    salary - (SELECT avg_salary FROM company_stats) AS diff_from_avg
FROM employees;
```


## Scenario 6: Subquery with `NOT IN` (Finding Unmatched Records)

### **Question:**

Which departments currently have **no** employees assigned to them?

### **Step-by-Step Without Subqueries:**

1. **Get all department IDs that have employees:**

   ```sql
   SELECT DISTINCT department_id 
   FROM employees 
   WHERE department_id IS NOT NULL;
   -- Result: 101, 102, 103, 104
   ```

2. **Filter departments excluding those IDs:**

   ```sql
   SELECT department_name 
   FROM departments 
   WHERE department_id NOT IN (101, 102, 103, 104);
   ```

### **Glued Together (Subquery with `NOT IN`):**

```sql
SELECT department_name 
FROM departments 
WHERE department_id NOT IN (
    SELECT DISTINCT department_id 
    FROM employees 
    WHERE department_id IS NOT NULL
);
```

### **Using `WITH` (CTE):**

```sql
WITH assigned_departments AS (
    SELECT DISTINCT department_id 
    FROM employees
)
SELECT d.department_name 
FROM departments d
LEFT JOIN assigned_departments ad 
  ON d.department_id = ad.department_id
WHERE ad.department_id IS NULL;
```

## Scenario 7: Correlated Subquery with Comparison Operator

### **Question:**

Which employees earn **more than the average salary of their own department**?

### **Step-by-Step Without Subqueries:**

1. **Find average salary for Department 101:**
   `AVG = 108333.33` $\rightarrow$ Filter: Bob (120000), George (110000).

2. **Find average salary for Department 102:**
   `AVG = 67500.00` $\rightarrow$ Filter: Charlie (70000).

3. **Repeat for each department and assemble results.**

### **Glued Together (Correlated Subquery in `WHERE`):**

The subquery executes dynamically for every employee row evaluated.

```sql
SELECT e.name, e.department_id, e.salary
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e.department_id
);
```

### **Using `WITH` (CTE):**

```sql
WITH dept_avg_salaries AS (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT e.name, e.department_id, e.salary
FROM employees e
JOIN dept_avg_salaries das 
  ON e.department_id = das.department_id
WHERE e.salary > das.avg_salary;
```

## Scenario 8: Subquery with Quantification (`ALL`)

### **Question:**

Which employees earn more than **all** employees in the 'Marketing' department (department ID 102)?

### **Step-by-Step Without Subqueries:**

1. **Find the maximum salary in Department 102:**

   ```sql
   SELECT MAX(salary) 
   FROM employees 
   WHERE department_id = 102;
   -- Result: 70000.00
   ```

2. **Find employees earning more than that maximum:**

   ```sql
   SELECT name, salary 
   FROM employees 
   WHERE salary > 70000.00;
   ```

### **Glued Together (Using `ALL` Subquery):**

```sql
SELECT name, salary 
FROM employees 
WHERE salary > ALL (
    SELECT salary 
    FROM employees 
    WHERE department_id = 102
);
```

### **Using `WITH` (CTE):**

```sql
WITH marketing_max_salary AS (
    SELECT MAX(salary) AS max_sal 
    FROM employees 
    WHERE department_id = 102
)
SELECT e.name, e.salary 
FROM employees e, marketing_max_salary mms
WHERE e.salary > mms.max_sal;
```

## Scenario 9: Multi-Column Subquery

### **Question:**

Find the highest-paid employee(s) in each department (match department and max salary).

### **Step-by-Step Without Subqueries:**

1. **Find the max salary per department:**

   ```sql
   SELECT department_id, MAX(salary) 
   FROM employees 
   GROUP BY department_id;
   -- (101, 120000), (102, 70000), (103, 90000), (104, 60000)
   ```

2. **Manually check for matching pairs:**

   ```sql
   SELECT name, department_id, salary 
   FROM employees 
   WHERE (department_id = 101 AND salary = 120000.00)
       OR (department_id = 102 AND salary = 70000.00)
      -- ... continue for all pairs
   ```

### **Glued Together (Multi-Column Subquery):**

```sql
SELECT name, department_id, salary 
FROM employees 
WHERE (department_id, salary) IN (
    SELECT department_id, MAX(salary) 
    FROM employees 
    GROUP BY department_id
);
```

### **Using `WITH` (CTE):**

```sql
WITH max_salaries AS (
    SELECT department_id, MAX(salary) AS max_sal 
    FROM employees 
    GROUP BY department_id
)
SELECT e.name, e.department_id, e.salary 
FROM employees e
JOIN max_salaries ms 
  ON e.department_id = ms.department_id 
 AND e.salary = ms.max_sal;
```

## Scenario 10: Chained CTEs (Multiple `WITH` Blocks)

### **Question:**

Find departments whose total employee salary payout consumes **more than 30%** of their department's budget.

### **Step-by-Step Without Subqueries:**

1. **Compute total payroll per department:**

   ```sql
   SELECT department_id, 
          SUM(salary) AS total_payroll 
   FROM employees 
   GROUP BY department_id;
   ```

2. **Calculate 30% of each department's budget:**

   ```sql
   SELECT department_id, 
          department_name, 
          (budget * 0.30) AS threshold 
   FROM departments;
   ```

3. **Compare results from Step 1 and Step 2.**

### **Glued Together (Nested Subqueries in `FROM` and `JOIN`):**

```sql
SELECT 
    d_info.department_name, 
    p_info.total_payroll, 
    d_info.threshold
FROM (
    SELECT department_id, 
           SUM(salary) AS total_payroll 
    FROM employees 
    GROUP BY department_id
) AS p_info
JOIN (
    SELECT department_id, 
           department_name, 
           (budget * 0.30) AS threshold 
    FROM departments
) AS d_info 
  ON p_info.department_id = d_info.department_id
WHERE p_info.total_payroll > d_info.threshold;
```

### **Using Chained `WITH` (Cleanest & Recommended Pattern in DuckDB):**

```sql
WITH department_payroll AS (
    -- Step 1: Aggregate salaries per department
    SELECT department_id, 
           SUM(salary) AS total_payroll 
    FROM employees 
    GROUP BY department_id
),
department_thresholds AS (
    -- Step 2: Calculate 30% threshold for each department
    SELECT department_id, 
           department_name, 
           (budget * 0.30) AS threshold 
    FROM departments
)
-- Step 3: Combine CTEs and filter
SELECT 
    dt.department_name, 
    dp.total_payroll, 
    dt.threshold
FROM department_payroll dp
JOIN department_thresholds dt 
  ON dp.department_id = dt.department_id
WHERE dp.total_payroll > dt.threshold;
```

## Scenario 11: Subquery with `ANY` / `SOME`

### **Question:**

Find employees who earn more than **at least one** employee in the 'Sales' department (department ID 103).

### **Step-by-Step Without Subqueries:**

1. **Find the minimum salary in Department 103:**

   ```sql
   SELECT MIN(salary) 
   FROM employees 
   WHERE department_id = 103;
   -- Result: 85000.00
   ```

2. **Filter employees who earn more than that minimum:**

   ```sql
   SELECT name, salary 
   FROM employees 
   WHERE salary > 85000.00;
   ```

### **Glued Together (Using `ANY` Subquery):**

```sql
SELECT name, salary 
FROM employees 
WHERE salary > ANY (
    SELECT salary 
    FROM employees 
    WHERE department_id = 103
);
```

### **Using `WITH` (CTE):**

```sql
WITH sales_min_salary AS (
    SELECT MIN(salary) AS min_sal 
    FROM employees 
    WHERE department_id = 103
)
SELECT e.name, e.salary 
FROM employees e, sales_min_salary sms
WHERE e.salary > sms.min_sal;
```

## Scenario 12: Conditional Categorization with Subquery in `CASE`

### **Question:**

Categorize each employee's salary status 
('Above Dept Avg' or 'Below or Equal Dept Avg') 
based on their department's average salary.

### **Step-by-Step Without Subqueries:**

1. **Calculate average salary for each department individually:**
   * Dept 101: 108333.33
   * Dept 102: 67500.00
   * Dept 103: 87500.00
   * Dept 104: 60000.00

2. **Apply explicit `CASE` expressions using hardcoded department averages:**

   ```sql
   SELECT name, department_id, salary,
          CASE 
              WHEN department_id = 101 AND salary > 108333.33 THEN 'Above Dept Avg'
              WHEN department_id = 102 AND salary > 67500.00  THEN 'Above Dept Avg'
              WHEN department_id = 103 AND salary > 87500.00  THEN 'Above Dept Avg'
              ELSE 'Below or Equal Dept Avg'
          END AS salary_tier
   FROM employees;
   ```

### **Glued Together (Correlated Subquery inside `CASE`):**

```sql
SELECT name, department_id, salary,
       CASE 
           WHEN salary > (
               SELECT AVG(e2.salary) 
               FROM employees e2 
               WHERE e2.department_id = employees.department_id
           ) THEN 'Above Dept Avg'
           ELSE 'Below or Equal Dept Avg'
       END AS salary_tier
FROM employees;
```

### **Using `WITH` (CTE):**

```sql
WITH dept_averages AS (
    SELECT department_id, 
           AVG(salary) AS avg_sal 
    FROM employees 
    GROUP BY department_id
)
SELECT 
    e.name, 
    e.department_id, 
    e.salary,
    CASE 
        WHEN e.salary > da.avg_sal THEN 'Above Dept Avg'
        ELSE 'Below or Equal Dept Avg'
    END AS salary_tier
FROM employees e
JOIN dept_averages da 
  ON e.department_id = da.department_id;
```

## Scenario 13: CTE with Window Functions (Top-N per Group)

### **Question:**

Find the top 2 highest-paid employees in each department.

### **Step-by-Step Without Subqueries:**

1. **Assign salary ranks to employees within each department:**

   ```sql
   SELECT name, department_id, salary,
          ROW_NUMBER() OVER (PARTITION BY department_id 
                             ORDER BY salary DESC) 
            AS rank
   FROM employees;
   ```

2. **Filter the resulting table for rows where `rank <= 2`.**

### **Glued Together (Subquery in `FROM`):**

```sql
SELECT department_id, name, salary, rank
FROM (
    SELECT name, department_id, salary,
           ROW_NUMBER() OVER (PARTITION BY department_id 
                              ORDER BY salary DESC) 
             AS rank
    FROM employees
) ranked_employees
WHERE rank <= 2;
```

### **Using `WITH` (CTE):**

```sql
WITH ranked_employees AS (
    SELECT 
        name, 
        department_id, 
        salary,
        ROW_NUMBER() OVER (PARTITION BY department_id 
                           ORDER BY salary DESC) AS rank
    FROM employees
)
SELECT department_id, name, salary, rank
FROM ranked_employees
WHERE rank <= 2;
```

## Scenario 14: Filtering Aggregates with `HAVING` Subquery

### **Question:**

Find departments whose minimum salary is greater than the average salary of the entire company.

### **Step-by-Step Without Subqueries:**

1. **Find overall company average salary:**

   ```sql
   SELECT AVG(salary) 
   FROM employees;
   -- Result: 86875.00
   ```

2. **Group employees by department and filter groups using `HAVING`:**

   ```sql
   SELECT department_id, 
          MIN(salary) AS min_salary 
   FROM employees 
   GROUP BY department_id 
   HAVING MIN(salary) > 86875.00;
   ```

### **Glued Together (Subquery inside `HAVING`):**

```sql
SELECT department_id, 
       MIN(salary) AS min_salary 
FROM employees 
GROUP BY department_id 
HAVING MIN(salary) > (
    SELECT AVG(salary) 
    FROM employees
);
```

### **Using `WITH` (CTE):**

```sql
WITH company_avg AS (
    SELECT AVG(salary) AS avg_sal 
    FROM employees
)
SELECT e.department_id, 
       MIN(e.salary) AS min_salary 
FROM employees e, company_avg ca
GROUP BY e.department_id, ca.avg_sal
HAVING MIN(e.salary) > ca.avg_sal;
```

## Scenario 15: Recursive CTE (Generating Series / Data Sequences)

### **Question:**

Generate a timeline of months for the year 2024 and calculate how many total years of tenure the company gains each month (simulated sequence generation).

### **Step-by-Step Without Subqueries:**

1. **Create an explicit list of sequential dates or numbers manually.**

2. **Join that sequence against our target tables.**

### **Glued Together (Recursive `WITH` CTE):**

DuckDB supports recursive CTEs (`WITH RECURSIVE`), which allow queries to refer to their own previous output to build iterative sequences.

```sql
WITH RECURSIVE month_series(month_num, month_date) AS (
    -- Anchor member: start at Month 1
    SELECT 1, DATE '2024-01-01'
    
    UNION ALL
    
    -- Recursive member: add 1 month until month 12
    SELECT month_num + 1, month_date + INTERVAL 1 MONTH
    FROM month_series
    WHERE month_num < 12
)
SELECT 
    month_num, 
    month_date,
    (SELECT COUNT(*) FROM employees WHERE hire_date <= month_date) AS cumulative_hires
FROM month_series;
```

## Summary Cheat Sheet

| Subquery Type | Common Location | Typical Use Case | 
| ----- | ----- | ----- | 
| **Scalar** | `SELECT`, `WHERE` | Single value calculation (e.g., global average, overall count) | 
| **Multi-Row** | `WHERE` (with `IN`, `ALL`, `ANY`) | Matching lists of values (e.g., IDs from another filtered table) | 
| **Correlated** | `WHERE`, `CASE` | Row-by-row comparative checking between outer and inner query | 
| **Derived Table** | `FROM` | Pre-aggregating data before joining or filtering | 
| **CTE (`WITH`)** | Top of query | Breaking complex queries into readable, modular steps | 
| **Recursive CTE** | Top of query (`WITH RECURSIVE`) | Generating sequences, date ranges, or hierarchical tree traversals |
