# Understanding `NULL` in DuckDB

1. In **DuckDB** (and standard SQL), `NULL` represents an **unknown, missing, or inapplicable value**. 
2. `NULL` is not equal to zero, an empty string `""`, or `FALSE`—it is simply a marker for missing data.

---

## 1. Simple Schema Setup

Let's create a table called `employees` containing basic information where some data is intentionally missing.

```sql
CREATE TABLE employees (
    id INT,
    name VARCHAR,
    department VARCHAR,
    bonus DECIMAL(10, 2)
);
```

---

## 2. Sample Data Insertion

We insert four records demonstrating different `NULL` scenarios:

```sql
INSERT INTO employees VALUES
    (1, 'Alice', 'Engineering', 500.00),    -- Complete record
    (2, 'Bob', 'Marketing', NULL),           -- Bonus is missing (NULL)
    (3, 'Charlie', NULL, 250.00),            -- Department is missing (NULL)
    (4, 'Diana', 'Engineering', 0.00);      -- Bonus is explicitly zero (not NULL)
```

### Table View

| id | name | department | bonus |
| :--- | :--- | :--- | :--- |
| **1** | Alice | Engineering | `500.00` |
| **2** | Bob | Marketing | `NULL` |
| **3** | Charlie | `NULL` | `250.00` |
| **4** | Diana | Engineering | `0.00` |

---

## 3. Key Concepts & Behavior of `NULL` in DuckDB

### A. Checking for `NULL` (Use `IS NULL` / `IS NOT NULL`)
You cannot use standard equality operators (`=` or `!=`) to check for `NULL`. You must use `IS NULL` or `IS NOT NULL`.

```sql
-- Select employees with no bonus assigned
SELECT name FROM employees WHERE bonus IS NULL;
-- Output: Bob

-- Attempting equality with NULL returns NULL (which acts like FALSE in filtering)
SELECT name FROM employees WHERE bonus = NULL;
-- Output: (No rows returned)
```

---

### B. Three-Valued Logic
In DuckDB, comparisons involving `NULL` yield `NULL` (Unknown) rather than `TRUE` or `FALSE`.

```sql
SELECT 
    (NULL = NULL) AS null_equals_null,
    (NULL IS NULL) AS null_is_null,
    (100 > NULL) AS comparison_with_null;
```

| null_equals_null | null_is_null | comparison_with_null |
| :--- | :--- | :--- |
| `NULL` | `TRUE` | `NULL` |

---

### C. Arithmetic Operations
Any standard arithmetic operation on a `NULL` value results in `NULL`. Note the difference between Bob (`NULL` bonus) and Diana (`0.00` bonus).

```sql
SELECT 
    name, 
    bonus, 
    bonus + 100 AS bonus_with_raise 
FROM employees;
```

| name | bonus | bonus_with_raise |
| :--- | :--- | :--- |
| Alice | `500.00` | `600.00` |
| Bob | `NULL` | `NULL` |
| Charlie | `250.00` | `350.00` |
| Diana | `0.00` | `100.00` |

---

### D. Aggregate Functions Ignore `NULL`
Functions like `AVG()`, `SUM()`, and `COUNT(column)` automatically ignore `NULL` values.

```sql
SELECT 
    COUNT(*) AS total_rows,
    COUNT(bonus) AS non_null_bonuses,
    AVG(bonus) AS average_bonus
FROM employees;
```

| total_rows | non_null_bonuses | average_bonus |
| :--- | :--- | :--- |
| `4` | `3` | `250.00` |

> **Note on `AVG`:** The sum of bonuses ($500 + 250 + 0 = 750$) is divided by 3 (the number of non-null values), resulting in `250.00`, rather than divided by 4.

---

### E. Handling `NULL` Values (`COALESCE`)
Use the `COALESCE()` function to replace `NULL` values with a default value.

```sql
SELECT 
    name, 
    COALESCE(bonus, 0.00) AS safe_bonus 
FROM employees;
```

| name | safe_bonus |
| :--- | :--- |
| Alice | `500.00` |
| Bob | `0.00` |
| Charlie | `250.00` |
| Diana | `0.00` |

---

## Summary

- **`NULL` is unknown data**, not zero or an empty string.
- Use **`IS NULL`** and **`IS NOT NULL`** instead of `= NULL`.
- Mathematical expressions with `NULL` yield **`NULL`**.
- Aggregations (`AVG`, `SUM`, `COUNT(col)`) **ignore `NULL`** values.
- Use **`COALESCE()`** to safely map `NULL` to fallback defaults.