# DuckDB CASE Expression Examples

This guide demonstrates how to use `CASE` expressions in **DuckDB**, including a simple conditional query and a query that aggregates data using `GROUP BY`.

---

## 1. Setup: Schema & Sample Data

We will create a simple table named `employees` with sample data.

```sql
-- Create the employees table
CREATE TABLE employees (
    id INTEGER,
    name VARCHAR,
    department VARCHAR,
    salary DECIMAL(10, 2)
);

-- Insert sample rows
INSERT INTO employees VALUES
    (1, 'Alice', 'Engineering', 120000.00),
    (2, 'Bob', 'Engineering', 85000.00),
    (3, 'Charlie', 'Sales', 60000.00),
    (4, 'Diana', 'Sales', 95000.00),
    (5, 'Evan', 'HR', 50000.00),
    (6, 'Fiona', 'HR', 72000.00);
```

---

## 2. Simple CASE Expression Query

A `CASE` expression allows you to implement `if-then-else` logic inside a query. In this simple example, we categorize employees into salary tiers.

```sql
SELECT 
    name,
    department,
    salary,
    CASE 
        WHEN salary >= 100000 THEN 'High Tier'
        WHEN salary >= 70000 THEN 'Mid Tier'
        ELSE 'Entry Tier'
    END AS salary_tier
FROM employees;
```

### Output:

| name | department | salary | salary_tier |
| :--- | :--- | :--- | :--- |
| Alice | Engineering | 120000.00 | High Tier |
| Bob | Engineering | 85000.00 | Mid Tier |
| Charlie | Sales | 60000.00 | Entry Tier |
| Diana | Sales | 95000.00 | Mid Tier |
| Evan | HR | 50000.00 | Entry Tier |
| Fiona | HR | 72000.00 | Mid Tier |

---

## 3. CASE Expression with GROUP BY

You can use `CASE` expressions alongside `GROUP BY` in two common ways:

### Example A: Grouping BY a CASE Expression
Aggregate metrics based on dynamically defined categories (e.g., counting employees per salary tier).

```sql
SELECT 
    CASE 
        WHEN salary >= 100000 THEN 'High Tier'
        WHEN salary >= 70000 THEN 'Mid Tier'
        ELSE 'Entry Tier'
    END AS salary_tier,
    COUNT(*) AS employee_count,
    ROUND(AVG(salary), 2) AS average_salary
FROM employees
GROUP BY 
    CASE 
        WHEN salary >= 100000 THEN 'High Tier'
        WHEN salary >= 70000 THEN 'Mid Tier'
        ELSE 'Entry Tier'
    END
ORDER BY average_salary DESC;
```

#### Output:

| salary_tier | employee_count | average_salary |
| :--- | :--- | :--- |
| High Tier | 1 | 120000.00 |
| Mid Tier | 3 | 84000.00 |
| Entry Tier | 2 | 55000.00 |

---

### Example B: Conditional Aggregation (CASE inside Aggregation Function)
Use `CASE` inside functions like `SUM()` or `COUNT()` to pivot or aggregate specific subset conditions per group.

```sql
SELECT 
    department,
    COUNT(*) AS total_employees,
    COUNT(CASE WHEN salary >= 80000 THEN 1 END) AS high_earners_count,
    SUM(CASE WHEN salary < 80000 THEN salary ELSE 0 END) AS total_entry_mid_payout
FROM employees
GROUP BY department;
```

#### Output:

| department | total_employees | high_earners_count | total_entry_mid_payout |
| :--- | :--- | :--- | :--- |
| Engineering | 2 | 2 | 0.00 |
| Sales | 2 | 1 | 60000.00 |
| HR | 2 | 0 | 122000.00 |