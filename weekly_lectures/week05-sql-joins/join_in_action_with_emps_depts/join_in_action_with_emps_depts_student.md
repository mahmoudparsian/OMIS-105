# Join in Action <br> with Employees and Departments <br> (Student Version)

This document is a hands-on guide to grouping, `CASE` expressions,
and joins in SQL. It uses two small tables: `departments` and
`employees`. Each of the 20 questions works like this:

1. **Question** — a business question in plain English.
2. **Your SQL** — you write the query that answers the question.
3. **Result** — click **Show result** to see the real output from
   DuckDB, and compare it with yours.

After most results, a short **How it works** note explains the key idea.

**How to work:** First, run the `CREATE TABLE` and `INSERT` statements
in the next section to build the two tables. Then, for each question,
write your query and run it in DuckDB. Click **Show result** only after
you have your own answer. If your output matches — same rows, same
columns, same order — your query is correct.

The tables are small on purpose. You can check every result by hand,
and that is the best way to understand what each query does.

For the relational-algebra symbol of each join (⋈ ⟕ ⟖ ⟗ ×), see
[`join_symbols.md`](../join_symbols.md).

---

## Table of Contents

1. [DuckDB Database Creation](#duckdb-database-creation)
2. [The Data at a Glance](#the-data-at-a-glance)
3. [Part 1 — GROUP BY Queries](#part-1--group-by-queries) (Q1–Q4)
4. [Part 2 — CASE Expressions](#part-2--case-expressions) (Q5–Q6)
5. [Part 3 — INNER JOIN](#part-3--inner-join) (Q7–Q10)
6. [Part 4 — LEFT JOIN](#part-4--left-join) (Q11–Q12)
7. [Part 5 — RIGHT JOIN](#part-5--right-join) (Q13–Q14)
8. [Part 6 — Finding Unmatched Rows](#part-6--finding-unmatched-rows) (Q15–Q16)
9. [Part 7 — FULL OUTER JOIN](#part-7--full-outer-join) (Q17–Q18)
10. [Part 8 — A Common Trap: ON vs. WHERE in a LEFT JOIN](#part-8--a-common-trap-on-vs-where-in-a-left-join) (Q19–Q20)
11. [Part 9 — Practice Exercises](#part-9--practice-exercises) (6 exercises with answers)
12. [Summary](#summary)

---

# DuckDB Database Creation

```sql
CREATE TABLE departments (
   dept_id INT PRIMARY KEY,
   dept_name VARCHAR,
   dept_location ENUM('USA', 'CANADA', 'CHINA')
);

DESC departments;
┌───────────────────────────────────────────────────────┐
│                      departments                      │
│                                                       │
│ dept_id       integer                        not null │
│ dept_name     varchar                                 │
│ dept_location enum('usa', 'canada', 'china')          │
└───────────────────────────────────────────────────────┘

INSERT INTO departments (dept_id, dept_name, dept_location)
VALUES
    (2, 'SALES', 'USA'),
    (3, 'BUSINESS', 'CANADA'),
    (4, 'AI', 'USA'),
    (5, 'QA', 'CHINA');

SELECT * FROM departments;
┌─────────┬───────────┬────────────────────────────────┐
│ dept_id │ dept_name │         dept_location          │
│  int32  │  varchar  │ enum('usa', 'canada', 'china') │
├─────────┼───────────┼────────────────────────────────┤
│       2 │ SALES     │ USA                            │
│       3 │ BUSINESS  │ CANADA                         │
│       4 │ AI        │ USA                            │
│       5 │ QA        │ CHINA                          │
└─────────┴───────────┴────────────────────────────────┘



CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR,
    gender ENUM('MALE', 'FEMALE'),
    salary INT,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

INSERT INTO employees(emp_id, emp_name, gender, salary, dept_id) VALUES
         (10, 'Alex', 'MALE', 67000, 2),
         (11, 'Jane', 'FEMALE', 87000, 2),
         (12, 'Barb', 'FEMALE', 68000, 3),
         (13, 'Max', 'MALE', 98000, 3),
         (14, 'Coco', 'FEMALE', 74000, 3),
         (15, 'Dara', 'MALE', 88000, NULL),
         (16, 'David', 'MALE', 66000, NULL);

SELECT * FROM EMPLOYEES;
┌────────┬──────────┬────────────────────────┬────────┬─────────┐
│ emp_id │ emp_name │         gender         │ salary │ dept_id │
│ int32  │ varchar  │ enum('male', 'female') │ int32  │  int32  │
├────────┼──────────┼────────────────────────┼────────┼─────────┤
│     10 │ Alex     │ MALE                   │  67000 │       2 │
│     11 │ Jane     │ FEMALE                 │  87000 │       2 │
│     12 │ Barb     │ FEMALE                 │  68000 │       3 │
│     13 │ Max      │ MALE                   │  98000 │       3 │
│     14 │ Coco     │ FEMALE                 │  74000 │       3 │
│     15 │ Dara     │ MALE                   │  88000 │    NULL │
│     16 │ David    │ MALE                   │  66000 │    NULL │
└────────┴──────────┴────────────────────────┴────────┴─────────┘
```

---

# The Data at a Glance

The two tables are linked by `dept_id`. In `departments`, `dept_id` is
the **primary key** (each department has one unique ID). In `employees`,
`dept_id` is a **foreign key** (it points to a row in `departments`).

The data has two "gaps" on purpose. These gaps are what make the
different joins give different answers:

```text
   departments                     employees
   ───────────                     ─────────
   2  SALES     (USA)     <────    Alex, Jane
   3  BUSINESS  (CANADA)  <────    Barb, Max, Coco
   4  AI        (USA)              (nobody)
   5  QA        (CHINA)            (nobody)
   (no department)        <────    Dara, David    (dept_id is NULL)
```

| Gap | Rows | Why it matters |
|-----|------|----------------|
| Departments with no employees | AI, QA | `INNER JOIN` drops them. `LEFT JOIN` from `departments` keeps them. |
| Employees with no department | Dara, David | `INNER JOIN` drops them. `LEFT JOIN` from `employees` keeps them. |

Keep this picture in mind. For every join below, ask yourself:
*"Which of the four special rows will appear in the result?"*

---

# Part 1 — GROUP BY Queries

`GROUP BY` puts rows with the same value into one group. Then an
**aggregate function** (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) returns one
value for each group. The result has **one row per group**.

### Q1. Headcount and payroll for each department

**Question:** How many employees work in each department, and what is
the total salary cost (payroll) of each department? Show the department
ID, the number of employees, and the total payroll. Include employees
who are not assigned to any department. Sort the result by department ID.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌─────────┬───────────────┬───────────────┐
│ dept_id │ num_employees │ total_payroll │
│  int32  │     int64     │    int128     │
├─────────┼───────────────┼───────────────┤
│       2 │             2 │        154000 │
│       3 │             3 │        240000 │
│    NULL │             2 │        154000 │
└─────────┴───────────────┴───────────────┘
```

**How it works:** The grouping key is `dept_id`. There are three distinct
values: `2`, `3`, and `NULL`. So there are three groups and three result
rows. `GROUP BY` puts all `NULL` values into **one** group. This is how
Dara and David show up together in the last row. This query reads only
the `employees` table, so it shows department IDs, not names. We will add
names with a join in Part 3.

</details>

---

### Q2. Salary statistics by gender

**Question:** For each gender, how many employees are there, and what are
the average, lowest, and highest salaries? Round the average salary to
two decimal places.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌────────────────────────┬───────────────┬────────────┬────────────┬────────────┐
│         gender         │ num_employees │ avg_salary │ min_salary │ max_salary │
│ enum('male', 'female') │     int64     │   double   │   int32    │   int32    │
├────────────────────────┼───────────────┼────────────┼────────────┼────────────┤
│ MALE                   │             4 │    79750.0 │      66000 │      98000 │
│ FEMALE                 │             3 │   76333.33 │      68000 │      87000 │
└────────────────────────┴───────────────┴────────────┴────────────┴────────────┘
```

**How it works:** Every employee belongs to exactly one gender group, so
all seven employees are counted (4 + 3 = 7). One `GROUP BY` can feed many
aggregate functions at the same time. `ROUND(AVG(salary), 2)` keeps two
decimal places. Note that `gender` is an `ENUM`, so `ORDER BY gender`
sorts by the order in the type definition (`'MALE'`, then `'FEMALE'`),
not alphabetically.

</details>

---

### Q3. Grouping by two keys: department and gender

**Question:** For employees who are assigned to a department, how many
men and how many women work in each department, and what is their
average salary? Show one row for each combination of department ID and
gender.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌─────────┬────────────────────────┬───────────────┬────────────┐
│ dept_id │         gender         │ num_employees │ avg_salary │
│  int32  │ enum('male', 'female') │     int64     │   double   │
├─────────┼────────────────────────┼───────────────┼────────────┤
│       2 │ MALE                   │             1 │    67000.0 │
│       2 │ FEMALE                 │             1 │    87000.0 │
│       3 │ MALE                   │             1 │    98000.0 │
│       3 │ FEMALE                 │             2 │    71000.0 │
└─────────┴────────────────────────┴───────────────┴────────────┘
```

**How it works:** With two grouping keys, each group is a unique
**pair** of values `(dept_id, gender)`. Department 2 has one man and one
woman, so it produces two rows. The `WHERE` clause runs **before**
grouping, so Dara and David are removed before any group is formed.

</details>

---

### Q4. Filtering groups with HAVING

**Question:** Which departments pay an average salary greater than
78,000? Ignore employees who have no department. Show the department ID,
the number of employees, and the average salary.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌─────────┬───────────────┬────────────┐
│ dept_id │ num_employees │ avg_salary │
│  int32  │     int64     │   double   │
├─────────┼───────────────┼────────────┤
│       3 │             3 │    80000.0 │
└─────────┴───────────────┴────────────┘
```

**How it works:** `WHERE` filters **rows** before grouping. `HAVING`
filters **groups** after grouping. Department 2 has an average of
77,000, so `HAVING` removes it. Department 3 has an average of 80,000,
so it stays. You cannot write `WHERE AVG(salary) > 78000`, because the
average does not exist yet when `WHERE` runs.

</details>

---

# Part 2 — CASE Expressions

A `CASE` expression is SQL's version of *if / then / else*. It checks
conditions from top to bottom and returns the value of the **first**
condition that is true.

### Q5. Classifying employees into salary bands

**Question:** Classify every employee into a salary band. An employee who
earns 85,000 or more is **High**. An employee who earns 70,000 or more
(but less than 85,000) is **Medium**. Everyone else is **Low**. Show the
employee's name, salary, and salary band, from highest to lowest salary.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌──────────┬────────┬─────────────┐
│ emp_name │ salary │ salary_band │
│ varchar  │ int32  │   varchar   │
├──────────┼────────┼─────────────┤
│ Max      │  98000 │ High        │
│ Dara     │  88000 │ High        │
│ Jane     │  87000 │ High        │
│ Coco     │  74000 │ Medium      │
│ Barb     │  68000 │ Low         │
│ Alex     │  67000 │ Low         │
│ David    │  66000 │ Low         │
└──────────┴────────┴─────────────┘
```

**How it works:** The order of the `WHEN` lines matters. Max earns
98,000, which is also `>= 70000`. But the first true condition wins, so
Max is **High**, not **Medium**. Because of this, the second `WHEN` does
not need to say `AND salary < 85000`. The `ELSE` branch catches every
other row. Without `ELSE`, those rows would get `NULL`.

</details>

---

### Q6. Counting men and women per department (CASE inside an aggregate)

**Question:** For each department ID, how many employees are there in
total, how many are women, and how many are men? Show all three counts
side by side in one row per department. Include employees with no
department.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌─────────┬─────────────────┬──────────────┬────────────┐
│ dept_id │ total_employees │ female_count │ male_count │
│  int32  │      int64      │    int128    │   int128   │
├─────────┼─────────────────┼──────────────┼────────────┤
│       2 │               2 │            1 │          1 │
│       3 │               3 │            2 │          1 │
│    NULL │               2 │            0 │          2 │
└─────────┴─────────────────┴──────────────┴────────────┘
```

**How it works:** This pattern is called **conditional aggregation**.
For each row, the `CASE` returns `1` if the condition is true and `0`
if it is false. `SUM` then adds up the 1s, which counts the matching
rows. Compare this with Q3: Q3 gives one row per *(department, gender)*
pair, while Q6 turns the genders into **columns**. Managers often find
this side-by-side layout easier to read.

</details>

---

# Part 3 — INNER JOIN

An `INNER JOIN` combines rows from two tables when the join condition is
true. It returns **only matching rows**. A row with no partner in the
other table is dropped.

From the data picture: AI and QA have no employees, and Dara and David
have no department. **None of these four rows can appear in an
`INNER JOIN` result.**

### Q7. Employees with their department name and location

**Question:** List every employee who belongs to a department, together
with the name and location of that department. Show the employee ID,
employee name, salary, department name, and department location. Sort by
employee ID.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌────────┬──────────┬────────┬───────────┬────────────────────────────────┐
│ emp_id │ emp_name │ salary │ dept_name │         dept_location          │
│ int32  │ varchar  │ int32  │  varchar  │ enum('usa', 'canada', 'china') │
├────────┼──────────┼────────┼───────────┼────────────────────────────────┤
│     10 │ Alex     │  67000 │ SALES     │ USA                            │
│     11 │ Jane     │  87000 │ SALES     │ USA                            │
│     12 │ Barb     │  68000 │ BUSINESS  │ CANADA                         │
│     13 │ Max      │  98000 │ BUSINESS  │ CANADA                         │
│     14 │ Coco     │  74000 │ BUSINESS  │ CANADA                         │
└────────┴──────────┴────────┴───────────┴────────────────────────────────┘
```

**How it works:** `e` and `d` are **table aliases** (short names). They
make the query shorter, and they tell SQL which table each column comes
from. The `employees` table has 7 rows, but the result has only 5.
Dara and David have `dept_id = NULL`, and `NULL = 2` is never true, so
they have no match. AI and QA are also missing, because no employee
points to them.

</details>

---

### Q8. Employees who work in the USA

**Question:** Which employees work in a department located in the USA?
Show the employee name, gender, salary, department name, and location.
Sort by salary, from highest to lowest.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌──────────┬────────────────────────┬────────┬───────────┬────────────────────────────────┐
│ emp_name │         gender         │ salary │ dept_name │         dept_location          │
│ varchar  │ enum('male', 'female') │ int32  │  varchar  │ enum('usa', 'canada', 'china') │
├──────────┼────────────────────────┼────────┼───────────┼────────────────────────────────┤
│ Jane     │ FEMALE                 │  87000 │ SALES     │ USA                            │
│ Alex     │ MALE                   │  67000 │ SALES     │ USA                            │
└──────────┴────────────────────────┴────────┴───────────┴────────────────────────────────┘
```

**How it works:** The join runs first, and then `WHERE` keeps only the
USA rows. We could not answer this question from `employees` alone,
because `employees` does not store a location. That is the main reason
to join: **the answer needs columns from both tables.** There are two
USA departments (SALES and AI), but only SALES appears, because AI has
no employees.

</details>

---

### Q9. Headcount and salary statistics by department name

**Question:** For each department that has employees, show the
department name, the number of employees, the average salary, and the
total payroll. Sort by total payroll, from highest to lowest.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌───────────┬───────────────┬────────────┬───────────────┐
│ dept_name │ num_employees │ avg_salary │ total_payroll │
│  varchar  │     int64     │   double   │    int128     │
├───────────┼───────────────┼────────────┼───────────────┤
│ BUSINESS  │             3 │    80000.0 │        240000 │
│ SALES     │             2 │    77000.0 │        154000 │
└───────────┴───────────────┴────────────┴───────────────┘
```

**How it works:** This query combines a join with `GROUP BY`. SQL first
joins the two tables, then groups the joined rows by department name.
Compare this with Q1: the numbers for departments 2 and 3 are the same,
but now we see real names instead of IDs. AI and QA are missing, because
an `INNER JOIN` only keeps matching rows. If we want *every* department,
even the empty ones, we need a `LEFT JOIN` (see Q12).

</details>

---

### Q10. High earners and where they work

**Question:** Which employees earn more than 70,000, and in which
department and country do they work? Show the employee name, salary,
department name, and location, from highest to lowest salary.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌──────────┬────────┬───────────┬────────────────────────────────┐
│ emp_name │ salary │ dept_name │         dept_location          │
│ varchar  │ int32  │  varchar  │ enum('usa', 'canada', 'china') │
├──────────┼────────┼───────────┼────────────────────────────────┤
│ Max      │  98000 │ BUSINESS  │ CANADA                         │
│ Jane     │  87000 │ SALES     │ USA                            │
│ Coco     │  74000 │ BUSINESS  │ CANADA                         │
└──────────┴────────┴───────────┴────────────────────────────────┘
```

**How it works:** Dara earns 88,000, which is more than 70,000, but Dara
is **not** in the result. Dara has no department, so the `INNER JOIN`
removed that row before `WHERE` was applied. This is a classic surprise:
an `INNER JOIN` can quietly drop rows you care about. If the question
were "all employees earning more than 70,000", we would need a
`LEFT JOIN`.

</details>

---

# Part 4 — LEFT JOIN

A `LEFT JOIN` returns **every row from the left table** (the table
written before `LEFT JOIN`). When a left row has a match, the columns
from the right table are filled in. When it has no match, those columns
are `NULL`.

### Q11. All employees, with their department if they have one

**Question:** List **all** employees, including employees who are not
assigned to any department. For each employee, show the employee ID,
name, salary, and department name. If an employee has no department,
the department name should be empty (`NULL`). Sort by employee ID.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌────────┬──────────┬────────┬───────────┐
│ emp_id │ emp_name │ salary │ dept_name │
│ int32  │ varchar  │ int32  │  varchar  │
├────────┼──────────┼────────┼───────────┤
│     10 │ Alex     │  67000 │ SALES     │
│     11 │ Jane     │  87000 │ SALES     │
│     12 │ Barb     │  68000 │ BUSINESS  │
│     13 │ Max      │  98000 │ BUSINESS  │
│     14 │ Coco     │  74000 │ BUSINESS  │
│     15 │ Dara     │  88000 │ NULL      │
│     16 │ David    │  66000 │ NULL      │
└────────┴──────────┴────────┴───────────┘
```

**How it works:** `employees` is the left table, so all 7 employees are
kept. Compare this with Q7, which returned only 5 rows. Dara and David
now appear, with `NULL` as the department name, because there is no
matching department. In a report, you could show a friendly label
instead with `COALESCE(d.dept_name, 'Not Assigned')`.

</details>

---

### Q12. Every department with its headcount and payroll

**Question:** Show **every** department, including departments that have
no employees. For each department, show the department ID, department
name, number of employees, and total payroll. A department with no
employees should show 0 employees and a payroll of 0. Sort by department
ID.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌─────────┬───────────┬───────────────┬───────────────┐
│ dept_id │ dept_name │ num_employees │ total_payroll │
│  int32  │  varchar  │     int64     │    int128     │
├─────────┼───────────┼───────────────┼───────────────┤
│       2 │ SALES     │             2 │        154000 │
│       3 │ BUSINESS  │             3 │        240000 │
│       4 │ AI        │             0 │             0 │
│       5 │ QA        │             0 │             0 │
└─────────┴───────────┴───────────────┴───────────────┘
```

**How it works:** Now `departments` is the left table, so all 4
departments are kept, including AI and QA. Two details are important:

1. **Use `COUNT(e.emp_id)`, not `COUNT(*)`.** For AI, the `LEFT JOIN`
   creates one row where every employee column is `NULL`. `COUNT(*)`
   counts that row and returns 1, which is wrong. `COUNT(e.emp_id)`
   skips `NULL` values and correctly returns 0.
2. **Use `COALESCE` for the sum.** `SUM` of only `NULL` values is
   `NULL`, not 0. `COALESCE(SUM(e.salary), 0)` replaces that `NULL`
   with 0.

Compare this with Q9: the `INNER JOIN` version showed 2 departments;
this `LEFT JOIN` version shows all 4.

</details>

---

# Part 5 — RIGHT JOIN

A `RIGHT JOIN` is the mirror image of a `LEFT JOIN`. It returns **every
row from the right table** (the table written after `RIGHT JOIN`), and
fills in `NULL` where the left table has no match.

In fact, `A RIGHT JOIN B` gives the same rows as `B LEFT JOIN A`. Most
SQL developers prefer `LEFT JOIN` because it is easier to read from left
to right. Still, you must be able to read a `RIGHT JOIN`, because you
will see it in other people's code.

### Q13. Every department and the names of its employees

**Question:** List every department together with the names of the
employees who work there. Departments with no employees must still
appear, with an empty (`NULL`) employee name. Show the department ID,
department name, location, and employee name. Sort by department ID and
then by employee name.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌─────────┬───────────┬────────────────────────────────┬──────────┐
│ dept_id │ dept_name │         dept_location          │ emp_name │
│  int32  │  varchar  │ enum('usa', 'canada', 'china') │ varchar  │
├─────────┼───────────┼────────────────────────────────┼──────────┤
│       2 │ SALES     │ USA                            │ Alex     │
│       2 │ SALES     │ USA                            │ Jane     │
│       3 │ BUSINESS  │ CANADA                         │ Barb     │
│       3 │ BUSINESS  │ CANADA                         │ Coco     │
│       3 │ BUSINESS  │ CANADA                         │ Max      │
│       4 │ AI        │ USA                            │ NULL     │
│       5 │ QA        │ CHINA                          │ NULL     │
└─────────┴───────────┴────────────────────────────────┴──────────┘
```

**How it works:** `departments` is the right table, so every department
is kept. SALES appears twice and BUSINESS three times (once per
employee). AI and QA appear once each, with `NULL` for the employee
name. Dara and David do **not** appear: they are in the left table and
have no matching department, and a `RIGHT JOIN` does not keep unmatched
left rows. This query gives the same result as
`FROM departments AS d LEFT JOIN employees AS e`.

</details>

---

### Q14. All employees and their department details (RIGHT JOIN version)

**Question:** List **all** employees, including those with no
department. For each employee, show the employee name, gender, salary,
department name, and department location. Write the query with a
`RIGHT JOIN`. Sort by employee ID.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌──────────┬────────────────────────┬────────┬───────────┬────────────────────────────────┐
│ emp_name │         gender         │ salary │ dept_name │         dept_location          │
│ varchar  │ enum('male', 'female') │ int32  │  varchar  │ enum('usa', 'canada', 'china') │
├──────────┼────────────────────────┼────────┼───────────┼────────────────────────────────┤
│ Alex     │ MALE                   │  67000 │ SALES     │ USA                            │
│ Jane     │ FEMALE                 │  87000 │ SALES     │ USA                            │
│ Barb     │ FEMALE                 │  68000 │ BUSINESS  │ CANADA                         │
│ Max      │ MALE                   │  98000 │ BUSINESS  │ CANADA                         │
│ Coco     │ FEMALE                 │  74000 │ BUSINESS  │ CANADA                         │
│ Dara     │ MALE                   │  88000 │ NULL      │ NULL                           │
│ David    │ MALE                   │  66000 │ NULL      │ NULL                           │
└──────────┴────────────────────────┴────────┴───────────┴────────────────────────────────┘
```

**How it works:** Here the tables are swapped: `departments` is on the
left and `employees` is on the right. A `RIGHT JOIN` keeps every
employee, so all 7 rows appear, and Dara and David have `NULL`
department details. This is exactly the same set of employees as Q11
(`employees LEFT JOIN departments`). **The rule: whichever table you
want to keep completely, put it on the "kept" side of the join.**

</details>

---

# Part 6 — Finding Unmatched Rows

Some of the most useful business questions are about what is
**missing**: departments with no staff, customers with no orders,
products that never sold. In SQL, all of these questions use the same
pattern: **LEFT JOIN + IS NULL**. This part uses it in both directions.

### Q15. Find the departments that have no employees

**Question:** Which departments currently have **no employees at all**?
Management wants to review these departments, either to hire staff or
to close them. Show the department ID, department name, and location.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌─────────┬───────────┬────────────────────────────────┐
│ dept_id │ dept_name │         dept_location          │
│  int32  │  varchar  │ enum('usa', 'canada', 'china') │
├─────────┼───────────┼────────────────────────────────┤
│       4 │ AI        │ USA                            │
│       5 │ QA        │ CHINA                          │
└─────────┴───────────┴────────────────────────────────┘
```

**How it works:** This is the **LEFT JOIN + IS NULL** pattern, one of the
most useful patterns in SQL. It works in two steps:

1. The `LEFT JOIN` keeps every department. A department with no
   employees gets one row where all employee columns are `NULL`
   (see Q12 and Q13).
2. `WHERE e.emp_id IS NULL` keeps only those rows — the departments that
   found no match.

We test `e.emp_id` because it is the primary key of `employees`, so it
is never `NULL` in a real employee row. If it is `NULL` here, we know
the row came from a department with no match. Also note: we must write
`IS NULL`, not `= NULL`. In SQL, `= NULL` is never true.

</details>

---

### Q16. Find the employees who have no department

**Question:** Which employees are **not assigned to any department**?
HR wants to assign each of them to a team. Show the employee ID, name,
gender, and salary.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌────────┬──────────┬────────────────────────┬────────┐
│ emp_id │ emp_name │         gender         │ salary │
│ int32  │ varchar  │ enum('male', 'female') │ int32  │
├────────┼──────────┼────────────────────────┼────────┤
│     15 │ Dara     │ MALE                   │  88000 │
│     16 │ David    │ MALE                   │  66000 │
└────────┴──────────┴────────────────────────┴────────┘
```

**How it works:** This is the same pattern as Q15, but in the **other
direction**. Now `employees` is the left table, so every employee is
kept, and we test the primary key of the **right** table
(`d.dept_id IS NULL`). Only Dara and David have no matching department.

Q15 and Q16 sound alike, but they answer different questions:

| Question | Left table (keep all) | Test for `NULL` | Answer |
|----------|----------------------|-----------------|--------|
| Departments with no employees (Q15) | `departments` | `e.emp_id` | AI, QA |
| Employees with no department (Q16) | `employees` | `d.dept_id` | Dara, David |

**Could we skip the join?** For this data, yes:
`SELECT emp_name FROM employees WHERE dept_id IS NULL` gives the same
two names. That works only because the `FOREIGN KEY` makes sure that
every non-`NULL` `dept_id` points to a real department. Without a
foreign key, an employee could have `dept_id = 9`, a department that
does not exist. The simple query would miss that employee, but the
`LEFT JOIN` version would catch it, because `9` finds no match either.

</details>

---

# Part 7 — FULL OUTER JOIN

A `FULL OUTER JOIN` keeps **every row from both tables**. Matching rows
are combined, as in an `INNER JOIN`. A row with no partner is still
kept, and the columns from the other table are `NULL`. You can think of
it as a `LEFT JOIN` and a `RIGHT JOIN` at the same time.

### Q17. Every employee and every department in one list

**Question:** Produce one complete list that shows **every employee and
every department**. Employees who have a department should appear next
to it. Departments with no employees and employees with no department
must also appear. Show the department ID, department name, employee ID,
and employee name. Sort by department ID, then by employee ID.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌─────────┬───────────┬────────┬──────────┐
│ dept_id │ dept_name │ emp_id │ emp_name │
│  int32  │  varchar  │ int32  │ varchar  │
├─────────┼───────────┼────────┼──────────┤
│       2 │ SALES     │     10 │ Alex     │
│       2 │ SALES     │     11 │ Jane     │
│       3 │ BUSINESS  │     12 │ Barb     │
│       3 │ BUSINESS  │     13 │ Max      │
│       3 │ BUSINESS  │     14 │ Coco     │
│       4 │ AI        │   NULL │ NULL     │
│       5 │ QA        │   NULL │ NULL     │
│    NULL │ NULL      │     15 │ Dara     │
│    NULL │ NULL      │     16 │ David    │
└─────────┴───────────┴────────┴──────────┘
```

**How it works:** The result has 9 rows. That is 5 matched rows (the
same as the `INNER JOIN` in Q7), plus 2 departments with no employees
(AI, QA), plus 2 employees with no department (Dara, David). This is
the only join in this document that keeps **all four** special rows.
Notice that `d.dept_id` is `NULL` for Dara and David. `ORDER BY` puts
`NULL` values last, so they appear at the bottom.

</details>

---

### Q18. A data-quality check: all unmatched rows on both sides

**Question:** As a data-quality check, list every row that has **no
partner** in the other table — both departments with no employees and
employees with no department — in a single result. Add a column that
explains the problem for each row.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌───────────┬──────────┬─────────────────────────────┐
│ dept_name │ emp_name │            issue            │
│  varchar  │ varchar  │           varchar           │
├───────────┼──────────┼─────────────────────────────┤
│ AI        │ NULL     │ Department has no employees │
│ QA        │ NULL     │ Department has no employees │
│ NULL      │ Dara     │ Employee has no department  │
│ NULL      │ David    │ Employee has no department  │
└───────────┴──────────┴─────────────────────────────┘
```

**How it works:** This query combines Q15 and Q16 into one. The
`FULL OUTER JOIN` keeps everything (as in Q17). Then `WHERE` keeps only
the rows where **one side is missing**: `e.emp_id IS NULL` finds empty
departments, and `d.dept_id IS NULL` finds unassigned employees. The
`CASE` expression (from Part 2) labels each row, so the report is easy
to read. A query like this is useful whenever you need to audit how
well two tables fit together.

</details>

---

# Part 8 — A Common Trap: ON vs. WHERE in a LEFT JOIN

With an `INNER JOIN`, a filter gives the same result in `ON` or in
`WHERE`. With a `LEFT JOIN`, it does **not**. A filter on the right
table in the wrong place can silently turn your `LEFT JOIN` into an
`INNER JOIN`. The next two queries try to answer the **same question**.
The first one is wrong; the second one is right.

**Question (for Q19 and Q20):** List **every** department, and for each
department show its employees who earn **more than 70,000**. A
department with no such employees must still appear, with an empty
(`NULL`) employee name and salary. Sort by department ID, then by
employee name.

### Q19. The wrong way: the filter is in WHERE

**Question:** Answer the question above by putting the salary filter in
the `WHERE` clause.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌─────────┬───────────┬──────────┬────────┐
│ dept_id │ dept_name │ emp_name │ salary │
│  int32  │  varchar  │ varchar  │ int32  │
├─────────┼───────────┼──────────┼────────┤
│       2 │ SALES     │ Jane     │  87000 │
│       3 │ BUSINESS  │ Coco     │  74000 │
│       3 │ BUSINESS  │ Max      │  98000 │
└─────────┴───────────┴──────────┴────────┘
```

**How it works (and why it is wrong):** AI and QA are **missing**, but
the question said to list every department. Here is what happened, step
by step:

1. The `LEFT JOIN` runs first. It keeps AI and QA, with
   `e.salary = NULL`.
2. Then `WHERE e.salary > 70000` runs. For AI and QA, this becomes
   `NULL > 70000`, which is **not true**. So `WHERE` removes them.

The result is the same as an `INNER JOIN`. The `LEFT JOIN` did its job,
but `WHERE` undid it.

</details>

---

### Q20. The right way: the filter is in ON

**Question:** Answer the same question by moving the salary filter into
the `ON` clause of the `LEFT JOIN`.

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌─────────┬───────────┬──────────┬────────┐
│ dept_id │ dept_name │ emp_name │ salary │
│  int32  │  varchar  │ varchar  │ int32  │
├─────────┼───────────┼──────────┼────────┤
│       2 │ SALES     │ Jane     │  87000 │
│       3 │ BUSINESS  │ Coco     │  74000 │
│       3 │ BUSINESS  │ Max      │  98000 │
│       4 │ AI        │ NULL     │   NULL │
│       5 │ QA        │ NULL     │   NULL │
└─────────┴───────────┴──────────┴────────┘
```

**How it works:** Now all 4 departments appear. The `ON` clause decides
**which employees count as a match**. An employee matches a department
only if the IDs are equal *and* the salary is above 70,000. Alex
(67,000) and Barb (68,000) do not match, so they are not shown. But
because this is a `LEFT JOIN`, a department with no match is still kept,
with `NULL` for the employee columns. That is why AI and QA appear.

**The rule to remember:**

| Where you put a filter on the **right** table | What it means | Effect on a `LEFT JOIN` |
|------|------|------|
| In `ON` | "Which right rows count as a match?" | All left rows are kept |
| In `WHERE` | "Which final rows do I keep?" | Unmatched left rows are removed |

A filter on the **left** table (for example, `d.dept_location = 'USA'`)
belongs in `WHERE`. A filter on the **right** table belongs in `ON`,
unless you really want to drop the unmatched rows. The `IS NULL` test in
Q15 and Q16 is the one exception: there, removing the matched rows in
`WHERE` is exactly the goal.

</details>

---

# Part 9 — Practice Exercises

Each exercise uses only ideas from this document. Write your query
first, run it in DuckDB, and check the number of rows. Then click
**Show result** to compare.

### Exercise 1

For each department **location**, how many employees earn more than
70,000? Show only locations that have at least one such employee.
*(Expected: 2 rows.)*

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌────────────────────────────────┬──────────────────┐
│         dept_location          │ num_high_earners │
│ enum('usa', 'canada', 'china') │      int64       │
├────────────────────────────────┼──────────────────┤
│ USA                            │                1 │
│ CANADA                         │                2 │
└────────────────────────────────┴──────────────────┘
```

`INNER JOIN` brings in the location, `WHERE` keeps the high earners, and
`GROUP BY` counts them per location. See Q8 and Q9.

</details>

### Exercise 2

List **all** employees with their department name. If an employee has
no department, show the text `Not Assigned` instead of `NULL`. Sort by
employee ID. *(Expected: 7 rows.)*

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌────────┬──────────┬──────────────┐
│ emp_id │ emp_name │  dept_name   │
│ int32  │ varchar  │   varchar    │
├────────┼──────────┼──────────────┤
│     10 │ Alex     │ SALES        │
│     11 │ Jane     │ SALES        │
│     12 │ Barb     │ BUSINESS     │
│     13 │ Max      │ BUSINESS     │
│     14 │ Coco     │ BUSINESS     │
│     15 │ Dara     │ Not Assigned │
│     16 │ David    │ Not Assigned │
└────────┴──────────┴──────────────┘
```

This is Q11 with a friendlier label. `COALESCE` returns its first
argument that is not `NULL`.

</details>

### Exercise 3

How many employees work in each location: USA, CANADA, and CHINA? Every
location must appear, even one with no employees. *(Expected: 3 rows.)*

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌────────────────────────────────┬───────────────┐
│         dept_location          │ num_employees │
│ enum('usa', 'canada', 'china') │     int64     │
├────────────────────────────────┼───────────────┤
│ USA                            │             2 │
│ CANADA                         │             3 │
│ CHINA                          │             0 │
└────────────────────────────────┴───────────────┘
```

To keep every location, start from `departments` and use a `LEFT JOIN`.
`COUNT(e.emp_id)` gives 0 for CHINA, where `COUNT(*)` would wrongly give
1. See Q12. (The locations are sorted in `ENUM` order, as in Q2.)

</details>

### Exercise 4

Which department has the **highest total payroll**? Show its name and
total payroll. *(Expected: 1 row.)*

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌───────────┬───────────────┐
│ dept_name │ total_payroll │
│  varchar  │    int128     │
├───────────┼───────────────┤
│ BUSINESS  │        240000 │
└───────────┴───────────────┘
```

Group by department, sort the totals from highest to lowest, and keep
the first row with `LIMIT 1`. See Q9.

</details>

### Exercise 5

Rewrite **Q12** (every department with its headcount and payroll) using
a `RIGHT JOIN` instead of a `LEFT JOIN`. Your result must be identical
to Q12. *(Expected: 4 rows.)*

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌─────────┬───────────┬───────────────┬───────────────┐
│ dept_id │ dept_name │ num_employees │ total_payroll │
│  int32  │  varchar  │     int64     │    int128     │
├─────────┼───────────┼───────────────┼───────────────┤
│       2 │ SALES     │             2 │        154000 │
│       3 │ BUSINESS  │             3 │        240000 │
│       4 │ AI        │             0 │             0 │
│       5 │ QA        │             0 │             0 │
└─────────┴───────────┴───────────────┴───────────────┘
```

Swap the two tables and change `LEFT` to `RIGHT`. `departments` is
still the table that is kept completely. See Part 5.

</details>

### Exercise 6 (challenge)

Which departments have **no employee earning more than 90,000**? This
includes departments with no employees at all. Show the department name
and location. *(Expected: 3 rows.)*

<details>
<summary><b>Show result</b></summary>

**Result:**

```text
┌───────────┬────────────────────────────────┐
│ dept_name │         dept_location          │
│  varchar  │ enum('usa', 'canada', 'china') │
├───────────┼────────────────────────────────┤
│ AI        │ USA                            │
│ QA        │ CHINA                          │
│ SALES     │ USA                            │
└───────────┴────────────────────────────────┘
```

This combines Part 6 and Part 8. The salary filter goes in `ON`, so
only employees earning more than 90,000 count as a match. Then
`WHERE e.emp_id IS NULL` keeps the departments that found no match.
SALES has employees, but none of them earns more than 90,000, so it is
in the answer. Only BUSINESS (Max, 98,000) is excluded.

</details>

---

# Summary

### Which special rows does each query keep?

The symbols come from relational algebra; see
[`join_symbols.md`](../join_symbols.md) for the full list.

| Query | Join | Symbol | AI, QA (departments with no employees) | Dara, David (employees with no department) | Rows |
|-------|------|:---:|:---:|:---:|:---:|
| Q7  | `employees INNER JOIN departments` | ⋈ | ✗ | ✗ | 5 |
| Q11 | `employees LEFT JOIN departments`  | ⟕ | ✗ | ✓ | 7 |
| Q13 | `employees RIGHT JOIN departments` | ⟖ | ✓ | ✗ | 7 |
| Q14 | `departments RIGHT JOIN employees` | ⟖ | ✗ | ✓ | 7 |
| Q17 | `employees FULL OUTER JOIN departments` | ⟗ | ✓ | ✓ | 9 |
| Q15 | `departments LEFT JOIN employees` + `WHERE e.emp_id IS NULL` | ⟕ | ✓ (only these) | ✗ | 2 |
| Q16 | `employees LEFT JOIN departments` + `WHERE d.dept_id IS NULL` | ⟕ | ✗ | ✓ (only these) | 2 |
| Q18 | `FULL OUTER JOIN` + `WHERE` either key `IS NULL` | ⟗ | ✓ (only these) | ✓ (only these) | 4 |

### Key takeaways

1. `GROUP BY` returns **one row per group**. All `NULL` keys form one
   group.
2. `WHERE` filters rows **before** grouping. `HAVING` filters groups
   **after** grouping.
3. `CASE` returns the value of the **first** true condition. Put the most
   specific condition first.
4. `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` counts rows that meet a
   condition, and turns categories into columns.
5. `INNER JOIN` keeps **only matching rows** from both tables. It can
   silently drop rows.
6. `LEFT JOIN` keeps **every row from the left table**. `RIGHT JOIN`
   keeps **every row from the right table**. `A RIGHT JOIN B` equals
   `B LEFT JOIN A`.
7. `FULL OUTER JOIN` keeps **every row from both tables**.
8. After an outer join, count with `COUNT(column)`, not `COUNT(*)`, and
   wrap sums in `COALESCE(..., 0)`.
9. To find rows with **no match**, use `LEFT JOIN` + `WHERE <right key> IS NULL`.
10. In a `LEFT JOIN`, put a filter on the right table in **`ON`**, not
    in `WHERE` — otherwise the unmatched rows disappear.

### See also

- [`join_symbols.md`](../join_symbols.md) — the relational-algebra
  symbol for each join type (⋈ ⟕ ⟖ ⟗ ×).
- [`SQL_Joins_in_Action_with_DuckDB.md`](../SQL_Joins_in_Action_with_DuckDB.md)
  — all five join types, including `CROSS JOIN`, with more examples.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
