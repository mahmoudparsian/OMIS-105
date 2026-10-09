# Understanding `NULL` in DuckDB

1. In **DuckDB** (and standard SQL), `NULL` means a value that is **unknown, missing, or not applicable**.
2. `NULL` is **not** the same as zero (`0`), an empty string (`''`), or `FALSE`. It is a marker that says *"no value here."*

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

We insert four rows that show different `NULL` cases:

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
You cannot use the comparison operators `=`, `!=`, or `<>` to check for `NULL`. You must use `IS NULL` or `IS NOT NULL`.

```sql
-- Select employees with no bonus assigned
SELECT name FROM employees WHERE bonus IS NULL;
-- Output: Bob

-- Comparing with = NULL gives NULL (unknown), and WHERE keeps only TRUE rows
SELECT name FROM employees WHERE bonus = NULL;
-- Output: (No rows returned)
```

---

### B. Three-Valued Logic
SQL logic has **three** values: `TRUE`, `FALSE`, and `NULL` (unknown).
A comparison with `NULL` gives `NULL`, not `TRUE` or `FALSE`.
Think of it as: *"Is 100 bigger than an unknown number? We don't know."*

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

### C. A Common Trap: `NULL` in `WHERE`

Which employees are **not** in Marketing?

```sql
SELECT name FROM employees WHERE department <> 'Marketing';
-- Output: Alice, Diana
```

Charlie is missing! Charlie's department is `NULL`, so
`NULL <> 'Marketing'` is `NULL` (unknown), and
`WHERE` drops the row. To include Charlie:

```sql
SELECT name FROM employees
WHERE department <> 'Marketing' OR department IS NULL;
-- Output: Alice, Charlie, Diana
```

---

### D. Arithmetic Operations
Any arithmetic (`+`, `-`, `*`, `/`) with `NULL` gives `NULL`. Note the difference between Bob (`NULL` bonus) and Diana (`0.00` bonus).

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

### E. Aggregate Functions Ignore `NULL`
Functions like `AVG()`, `SUM()`, and `COUNT(column)` skip `NULL` values. Only `COUNT(*)` counts every row.

```sql
SELECT 
    COUNT(*) AS total_rows,
    COUNT(bonus) AS non_null_bonuses,
    AVG(bonus) AS average_bonus
FROM employees;
```

| total_rows | non_null_bonuses | average_bonus |
| :--- | :--- | :--- |
| `4` | `3` | `250.0` |

> **Note on `AVG`:** The sum of the bonuses (500 + 250 + 0 = 750) is divided by **3** (the number of non-`NULL` values), not by 4. The result is `250.0`.
>
> If a missing bonus should count as zero, write `AVG(COALESCE(bonus, 0))`. That gives 750 / 4 = `187.5`.

---

### F. Replacing `NULL` with `COALESCE`
`COALESCE(a, b, ...)` returns the first value that is not `NULL`. Use it to replace `NULL` with a default value.

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

### G. `NULL` and Sorting

In DuckDB, `NULL` values are sorted **last** by default,
for both `ASC` and `DESC`:

```sql
SELECT name, bonus FROM employees ORDER BY bonus;
-- Diana 0.00, Charlie 250.00, Alice 500.00, Bob NULL
```

You can choose with `NULLS FIRST` or `NULLS LAST`:
`ORDER BY bonus NULLS FIRST`.

---

## Summary

- **`NULL` means unknown or missing**, not zero or an empty string.
- Use **`IS NULL`** and **`IS NOT NULL`**, never `= NULL`.
- Comparisons with `NULL` give `NULL`, so `WHERE` drops those rows.
- Arithmetic with `NULL` gives **`NULL`**.
- Aggregates (`AVG`, `SUM`, `COUNT(col)`) **skip `NULL`** values; `COUNT(*)` does not.
- Use **`COALESCE()`** to replace `NULL` with a default value.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
