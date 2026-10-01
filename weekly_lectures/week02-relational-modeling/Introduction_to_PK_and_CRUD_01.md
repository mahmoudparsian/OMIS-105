# Introduction to Primary Keys and CRUD

## Our Example Table: `employees`

We will use one simple table for this whole lesson.

| Column | Meaning |
|--------|---------|
| emp_id | A unique number for each employee |
| emp_name | The employee's full name |
| salary | The employee's yearly salary |
| country | The country where the employee works |
| department | The department the employee works in |

Here are 6 sample rows:

| emp_id | emp_name | salary | country | department |
|--------|----------|--------|---------|------------|
| 1 | Alice Chen | 75000 | USA | Sales |
| 2 | Bruno Silva | 68000 | Brazil | Marketing |
| 3 | Chidi Okafor | 82000 | Nigeria | Engineering |
| 4 | Diya Patel | 71000 | India | Engineering |
| 5 | Elin Karlsson | 90000 | Sweden | Sales |
| 6 | Farid Haidari | 64000 | UAE | Marketing |

The SQL to build this table:

```sql
CREATE OR REPLACE TABLE employees (
    emp_id      INTEGER PRIMARY KEY,
    emp_name    VARCHAR,
    salary      INTEGER,
    country     VARCHAR,
    department  VARCHAR
);

INSERT INTO employees VALUES
    (1, 'Alice Chen',    75000, 'USA',     'Sales'),
    (2, 'Bruno Silva',   68000, 'Brazil',  'Marketing'),
    (3, 'Chidi Okafor',  82000, 'Nigeria', 'Engineering'),
    (4, 'Diya Patel',    71000, 'India',   'Engineering'),
    (5, 'Elin Karlsson', 90000, 'Sweden',  'Sales'),
    (6, 'Farid Haidari', 64000, 'UAE',     'Marketing');
```

---

## Part 1: Primary Key (PK)

### What is a Primary Key?

A **primary key (PK)** is a column (or set of columns) that gives each
row a unique identity.

A good primary key must follow two rules:

1. **Unique** — no two rows can have the same value.
2. **Not null** — every row must have a value. A primary key can never
   be empty.

### Why do we need a PK?

Look at our table. Could two employees share the same name? Yes — two
people could both be named "Alice Chen." Could two employees have the
same salary? Yes. Same country? Same department? Yes to both.

But `emp_id` is different. Each employee gets their own number, and no
one else uses it. That is what makes `emp_id` a good primary key for
this table — it is the one column we can always trust to point to
exactly one row.

### Picking a Primary Key: a Simple Test

Ask yourself: "If I only know this value, can I find exactly one row?"

| Column | Could two rows share this value? | Good PK? |
|--------|-----------------------------------|----------|
| emp_id | No | Yes |
| emp_name | Yes (name collisions happen) | No |
| salary | Yes | No |
| country | Yes | No |
| department | Yes | No |

This is why real tables almost always add an ID column (like `emp_id`)
instead of relying on a "natural" column like name.

### Try It Yourself

Using the 6 rows above, answer:

1. If you only knew `department = 'Engineering'`, could you tell which
   *one* employee that is? Why or why not?
2. Why can `emp_id` never be `NULL`?
3. What would happen if we tried to insert a 7th employee with
   `emp_id = 3`?

---

## Part 2: CRUD, One Operation at a Time

**CRUD** stands for the four basic things we do to data:

- **C**reate — add new data
- **R**ead — look up existing data
- **U**pdate — change existing data
- **D**elete — remove existing data

We will learn each one separately, using our `employees` table.

---

### C — Create (`INSERT`)

`INSERT` adds a brand-new row to the table.

```sql
INSERT INTO employees VALUES
    (7, 'Grace Kim', 77000, 'South Korea', 'Sales');
```

What happens:
- A new row is added for `emp_id = 7`.
- The other 6 rows do not change.

**Rule to remember:** the new `emp_id` must be unique. If you tried to
insert another row with `emp_id = 7`, the primary key rule would block
it.

**Try it:** Write an `INSERT` statement that adds yourself as employee
`emp_id = 8`, in the `Marketing` department.

---

### R — Read (`SELECT`)

`SELECT` reads data without changing anything.

```sql
-- Read everyone
SELECT * FROM employees;

-- Read just the Engineering department
SELECT emp_name, salary
FROM employees
WHERE department = 'Engineering';

-- Read one specific employee by primary key
SELECT * FROM employees
WHERE emp_id = 3;
```

Notice the last query: looking something up by its primary key is the
fastest and safest way to find exactly one row. This is the most
common use of a PK in everyday SQL.

**Try it:** Write a `SELECT` that reads all employees with a `salary`
greater than 70000.

---

### U — Update (`UPDATE`)

`UPDATE` changes values in existing rows. It does **not** add or
remove rows.

```sql
UPDATE employees
SET salary = 95000
WHERE emp_id = 5;
```

What happens:
- Elin Karlsson's (`emp_id = 5`) salary changes from 90000 to 95000.
- No other row is touched.

**Why `WHERE emp_id = ...` matters:** the primary key tells SQL
exactly which row to change. If you forget the `WHERE` clause,
`UPDATE` will change *every row* in the table — a common and
dangerous mistake.

```sql
-- DANGER: this updates ALL 6 employees, not just one!
UPDATE employees
SET salary = 95000;
```

**Try it:** Write an `UPDATE` that moves `emp_id = 2` to the
`Engineering` department.

---

### D — Delete (`DELETE`)

`DELETE` removes whole rows from the table.

```sql
DELETE FROM employees
WHERE emp_id = 6;
```

What happens:
- Farid Haidari's row (`emp_id = 6`) is removed completely.
- The other 5 rows remain untouched.

Just like `UPDATE`, forgetting the `WHERE` clause is dangerous:

```sql
-- DANGER: this deletes ALL rows in the table!
DELETE FROM employees;
```

**Try it:** Write a `DELETE` that removes the employee with
`emp_id = 1`. Then write a `SELECT` to confirm the row is gone.

---

## Part 3: GROUP BY

`GROUP BY` collects rows into groups that share the same value, so we
can calculate something for each group — like a count, a sum, or an
average.

### Example 1: Count employees per department

```sql
SELECT department, COUNT(*) AS num_employees
FROM employees
GROUP BY department;
```

This answers: "How many employees work in each department?" Each
distinct `department` value becomes one row in the result.

### Example 2: Average salary per country

```sql
SELECT country, AVG(salary) AS avg_salary
FROM employees
GROUP BY country;
```

This answers: "What is the average salary in each country?"

### Example 3: Total salary per department

```sql
SELECT department, SUM(salary) AS total_salary
FROM employees
GROUP BY department;
```

This answers: "How much does the company pay out, in total, for each
department?"

### Example 4: Highest salary per department, only for departments with more than one employee

```sql
SELECT department, MAX(salary) AS highest_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 1;
```

This answers: "What is the top salary in each department — but only
show departments that have more than one employee?" `HAVING` filters
groups *after* they are formed, while `WHERE` would filter rows
*before* grouping.

**Try it:** Write a `GROUP BY` query that shows the number of
employees in each country.

---

## Summary

| Operation | SQL Keyword | Changes row count? | Needs `WHERE emp_id = ...`? |
|-----------|-------------|---------------------|-------------------------------|
| Create | `INSERT` | Adds 1 row | No — the new PK goes in the row itself |
| Read | `SELECT` | No | Only if you want one specific row |
| Update | `UPDATE` | No (same rows) | Yes — almost always |
| Delete | `DELETE` | Removes rows | Yes — almost always |

The primary key (`emp_id`) is what makes `UPDATE` and `DELETE` safe.
Without it, we could not reliably target one single row.

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
