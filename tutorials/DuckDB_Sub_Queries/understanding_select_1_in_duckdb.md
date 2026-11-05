# Beginner's Guide: Understanding `SELECT 1` in DuckDB

When reading or writing SQL subqueries, especially with `EXISTS` or `NOT EXISTS`, you will often encounter `SELECT 1`. This guide explains what it means, how DuckDB handles it, and why it is commonly used.

---

## Sample Schema & Data

All examples in this guide use the following `departments` and `employees` dataset.

### DDL & Data Setup

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

### Table Contents

**`departments`**

| department_id | department_name | location | budget |
| :--- | :--- | :--- | :--- |
| 101 | Engineering | New York | 500000.00 |
| 102 | Marketing | San Francisco | 200000.00 |
| 103 | Sales | Chicago | 300000.00 |
| 104 | HR | New York | 150000.00 |
| 105 | Research | Austin | 400000.00 |

**`employees`**

| employee_id | name | department_id | salary | hire_date |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Alice | 101 | 95000.00 | 2021-03-15 |
| 2 | Bob | 101 | 120000.00 | 2019-06-01 |
| 3 | Charlie | 102 | 70000.00 | 2022-01-10 |
| 4 | Diana | 102 | 65000.00 | 2023-04-18 |
| 5 | Evan | 103 | 85000.00 | 2020-11-05 |
| 6 | Fiona | 103 | 90000.00 | 2018-08-22 |
| 7 | George | 101 | 110000.00 | 2020-02-14 |
| 8 | Hannah | 104 | 60000.00 | 2021-09-30 |

---

## 1. What does `SELECT 1` mean?

By itself, `SELECT 1` simply evaluates the integer constant `1`:

```sql
SELECT 1;
```

**Result:**

| 1 | 
| :--- | 
| 1 | 

If you run it against a table, it returns the number `1` once for **every row** present in that table:

```sql
SELECT 1 FROM employees;
```

**Result (8 rows returned because there are 8 employees):**

| 1 | 
| :--- | 
| 1 | 
| 1 | 
| 1 | 
| 1 | 
| 1 | 
| 1 | 
| 1 | 
| 1 | 

---

## 2. Why use `SELECT 1` in `EXISTS` subqueries?

The primary use case for `SELECT 1` is inside an `EXISTS (...)` or `NOT EXISTS (...)` subquery.

### Example: Find departments that have at least one employee

```sql
SELECT department_name 
FROM departments d
WHERE EXISTS (
    SELECT 1 
    FROM employees e 
    WHERE e.department_id = d.department_id
);
```

### Output:

| department_name |
| :--- |
| Engineering |
| Marketing |
| Sales |
| HR |

*(Note: 'Research' department ID 105 is excluded because no employees belong to it).*

### How DuckDB processes this query:

1. **`EXISTS` only checks for presence:** It asks a simple true/false question: *"Does the subquery return at least 1 row?"*
2. **Values don't matter:** `EXISTS` does not read or return the column values inside the subquery. It only cares whether a row was found.
3. **`SELECT 1` acts as a placeholder flag:** It tells DuckDB, *"If a matching row is found, return `1` so `EXISTS` evaluates to TRUE."*

---

## 3. Does `SELECT 1` perform better than `SELECT *`?

### Short Answer: No, they behave identically.

In modern SQL engines like DuckDB, the query optimizer optimizes `EXISTS` subqueries automatically.

All of the following queries produce the **exact same execution plan** in DuckDB:

```sql
-- Option A: Common convention
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.department_id = d.department_id)

-- Option B: Selecting all columns
WHERE EXISTS (SELECT * FROM employees e WHERE e.department_id = d.department_id)

-- Option C: Selecting specific column
WHERE EXISTS (SELECT department_id FROM employees e WHERE e.department_id = d.department_id)
```

DuckDB does **not** retrieve or load full column data for `SELECT *` inside an `EXISTS` check.

---

## 4. Key Takeaways for Beginners

* **`EXISTS` looks for rows, not values.** Whether you select `1`, `*`, or `'pizza'`, the logical result is the same.
* **`SELECT 1` is a visual signpost.** Developers use it to signal: *"I am checking for row existence, not selecting actual table data."*
* **DuckDB optimizes it for you.** You don't need to worry about performance differences between `SELECT 1` and `SELECT *` in existence checks.