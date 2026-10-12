# OMIS 105 — Database Management Systems
## Midterm Exam — Practice Version 3 (Weeks 1–5)

**Instructor:** Dr. Parsian

**Coverage:**

* Week 1 (Database Foundations: SELECT, WHERE, ORDER BY, LIMIT, LIKE, DISTINCT)
* Week 2 (Relational Modeling: keys, GROUP BY, HAVING)
* Week 3 (SQL Basics: NULL, CASE, string functions)
* Week 4 (Aggregation and INNER JOIN)
* Week 5 (JOINs: LEFT, RIGHT, FULL OUTER, CROSS, IS NULL, COALESCE)

**Total Points:**

* 100
	* Part 1: 30 pts
	* Part 2: 70 pts

---

## Reference Schema and Data — Employees & Departments

All questions use this small company database. It has only two
tables, and **all of the data is shown below**, so you can work out
every answer by hand.

```sql
CREATE TABLE departments (
    dept_id   INT PRIMARY KEY,
    dept_name VARCHAR(50)
);

CREATE TABLE employees (
    emp_id   INT PRIMARY KEY,
    emp_name VARCHAR(50),
    salary   INT,
    dept_id  INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
```

**`departments`** (4 rows)

| dept_id | dept_name   |
|--------:|-------------|
| 10      | Engineering |
| 20      | Marketing   |
| 30      | Sales       |
| 40      | Finance     |

**`employees`** (6 rows)

| emp_id | emp_name | salary | dept_id |
|-------:|----------|-------:|--------:|
| 1      | Alice    | 65000  | 10      |
| 2      | Bob      | 78000  | 20      |
| 3      | Rafa     | 82000  | 20      |
| 4      | Charlie  | 75000  | 10      |
| 5      | Diana    | 70000  | NULL    |
| 6      | Jane     | 80000  | NULL    |

Keep this page visible while you answer both parts of the exam.

**To practice:** this database is in the course repository at
`weekly_lectures/week05-sql-joins/joins_with_emps_depts/emps_depts_db.duckdb`.
Try to answer each question by hand first, then check yourself
with DuckDB.

---

# Part 1 — Multiple Choice (30 points, 2 pts each)

Circle/select the single best answer for each question.

### 1. (Week 1) `dept_id` is the **primary key** of `departments`. What does this guarantee?

A) Every `dept_id` value is greater than zero

B) Every row has a `dept_id`, and no two rows have the same `dept_id`

C) Every department has at least one employee

D) The rows are always stored in `dept_id` order

### 2. (Week 1) Which query returns the **3 highest-paid** employees, highest first?

A) `SELECT * FROM employees ORDER BY salary LIMIT 3;`

B) `SELECT * FROM employees LIMIT 3 ORDER BY salary DESC;`

C) `SELECT * FROM employees ORDER BY salary DESC LIMIT 3;`

D) `SELECT * FROM employees WHERE salary DESC LIMIT 3;`

### 3. (Week 1) What does this query return?

```sql
SELECT emp_name
FROM employees
WHERE emp_name LIKE '%a';
```

A) Alice, Rafa, Diana, Jane

B) Rafa, Diana

C) Alice

D) No rows

### 4. (Week 1) How many rows does this query return?

```sql
SELECT DISTINCT dept_id
FROM employees;
```

A) 2

B) 3

C) 4

D) 6

### 5. (Week 2) Because of the **foreign key** on `employees.dept_id`, which `INSERT` is **rejected**? (Column order: `emp_id, emp_name, salary, dept_id`.)

A) `INSERT INTO employees VALUES (7, 'Omar', 72000, 30);`

B) `INSERT INTO employees VALUES (7, 'Omar', 72000, NULL);`

C) `INSERT INTO employees VALUES (7, 'Omar', 72000, 50);`

D) `INSERT INTO employees VALUES (7, 'Omar', 72000, 40);`

### 6. (Week 2) A manager asks: "Which `dept_id` groups have a **total** salary above 150,000?" Which query is correct?

A)

```sql
SELECT dept_id, SUM(salary) AS total_salary
FROM employees
WHERE SUM(salary) > 150000
GROUP BY dept_id;
```

B)

```sql
SELECT dept_id, SUM(salary) AS total_salary
FROM employees
GROUP BY dept_id
HAVING SUM(salary) > 150000;
```

C)

```sql
SELECT dept_id, salary
FROM employees
WHERE salary > 150000;
```

D)

```sql
SELECT dept_id, SUM(salary) AS total_salary
FROM employees
HAVING SUM(salary) > 150000
GROUP BY dept_id;
```

### 7. (Week 3) What does this query return?

```sql
SELECT COUNT(*)
FROM employees
WHERE dept_id = NULL;
```

A) 0

B) 2

C) 6

D) An error

### 8. (Week 3) How many employees are labeled `'Medium'` by this query?

```sql
SELECT emp_name,
       CASE
           WHEN salary >= 80000 THEN 'High'
           WHEN salary >= 70000 THEN 'Medium'
           ELSE 'Low'
       END AS salary_band
FROM employees;
```

A) 1

B) 2

C) 3

D) 4

### 9. (Week 3) What does this query return?

```sql
SELECT UPPER(SUBSTRING(dept_name, 1, 3)) AS code
FROM departments
WHERE dept_id = 20;
```

A) `Mar`

B) `MAR`

C) `MARKETING`

D) `ING`

### 10. (Week 4) What does this query return?

```sql
SELECT COUNT(*), COUNT(dept_id), COUNT(DISTINCT dept_id)
FROM employees;
```

A) 6, 6, 4

B) 6, 4, 3

C) 6, 4, 2

D) 4, 4, 2

### 11. (Week 4) How many rows does this query return?

```sql
SELECT e.emp_name, d.dept_name
FROM employees AS e
INNER JOIN departments AS d
    ON e.dept_id = d.dept_id;
```

A) 4

B) 6

C) 8

D) 24

### 12. (Week 4) How many rows does this query return, and why?

```sql
SELECT e.emp_name, d.dept_name
FROM employees AS e, departments AS d;
```

A) 4 — it is an INNER JOIN on `dept_id`

B) 6 — one row per employee

C) 10 — 6 employees plus 4 departments

D) 24 — there is no join condition, so every employee is paired with every department (a CROSS JOIN)

### 13. (Week 5) A manager wants a list of **every department**, including departments with no employees. Which query is correct?

A)

```sql
SELECT d.dept_name, e.emp_name
FROM employees AS e
LEFT JOIN departments AS d ON e.dept_id = d.dept_id;
```

B)

```sql
SELECT d.dept_name, e.emp_name
FROM departments AS d
LEFT JOIN employees AS e ON d.dept_id = e.dept_id;
```

C)

```sql
SELECT d.dept_name, e.emp_name
FROM departments AS d
INNER JOIN employees AS e ON d.dept_id = e.dept_id;
```

D)

```sql
SELECT d.dept_name, e.emp_name
FROM departments AS d
RIGHT JOIN employees AS e ON d.dept_id = e.dept_id;
```

### 14. (Week 5) In the result of this query, what number is shown for **Sales**?

```sql
SELECT d.dept_name, COUNT(*) AS num_employees
FROM departments AS d
LEFT JOIN employees AS e ON d.dept_id = e.dept_id
GROUP BY d.dept_name;
```

A) 0

B) 1

C) `NULL`

D) Sales does not appear in the result

### 15. (Week 5) How many rows does this query return?

```sql
SELECT e.emp_name, d.dept_name
FROM employees AS e
FULL OUTER JOIN departments AS d
    ON e.dept_id = d.dept_id;
```

A) 4

B) 6

C) 8

D) 10

---

# Part 2 — Written Questions (70 points)

Show your reasoning. For SQL questions, write a single query unless
told otherwise. Small syntax slips are fine if the logic is correct.

## Simple (10 points each — 20 points total)

**S1.** In two or three sentences, explain the difference between a
**primary key** and a **foreign key**. Use `departments.dept_id` and
`employees.dept_id` as your example. Then explain why Diana's
`dept_id` can be `NULL` even though `employees.dept_id` is a foreign
key.

**S2.** Write the **full result** (every row and column) of this
query. Then explain in one sentence why some rows have `NULL` in
`dept_name`.

```sql
SELECT e.emp_name, d.dept_name
FROM employees AS e
LEFT JOIN departments AS d
    ON e.dept_id = d.dept_id
ORDER BY e.emp_id;
```

## Intermediate (15 points each — 30 points total)

**I1.** Write a query that shows, for each **department name** that
has at least one employee: the department name, the number of
employees (`num_employees`), and the average salary (`avg_salary`).
Sort from highest to lowest average salary. Then write the result
your query returns.

**I2.** Write a query that lists **every** department (all 4) with
its number of employees (`num_employees`) and its total salary
(`total_salary`). Departments with no employees must show **0** in
both columns — not `NULL`, and not 1. Sort by `num_employees`
(highest first), then by department name.

## Advanced (10 points each — 20 points total)

**A1.** Finding the gaps.

(a) Write a query that returns the `dept_id` and `dept_name` of
every department that has **no employees**. Use a JOIN.

(b) Write a query that returns the `emp_name` of every employee who
has **no department**. Use a **RIGHT JOIN**.

(c) Write the result of each query.

**A2.** A manager asks: "For **every** department, how many
employees earn **at least 75,000**? Show 0 for departments with
none."

(a) Write the query. (Hint: think carefully about *where* the salary
test goes.)

(b) A classmate writes this query instead:

```sql
SELECT d.dept_name, COUNT(e.emp_id) AS num_high_earners
FROM departments AS d
LEFT JOIN employees AS e ON d.dept_id = e.dept_id
WHERE e.salary >= 75000
GROUP BY d.dept_name;
```

Which departments are **missing** from the classmate's result, and
why? Explain in 1–2 sentences.

---

*End of Exam*
