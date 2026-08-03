# OMIS 105 — Intermediate SQL with qStudio

* **Course:** OMIS 105 — Introduction to Database Management Systems
* **Quarter:** Fall 2026
* **Author:** Dr. Mahmoud Parsian

---

## Before You Begin

This document builds on the introductory SQL lab.
You should already have the `students` table from that session.
If not, run the two blocks below to recreate it.

```sql
CREATE OR REPLACE TABLE students (
    student_id         INTEGER,
    first_name         VARCHAR,
    major              VARCHAR,
    gpa                DECIMAL(3,2),
    graduation_year    INTEGER,
    scholarship_amount DECIMAL(8,2)
);
```

```sql
INSERT INTO students VALUES
    (1,  'Alice', 'Finance',    3.82, 2027, 5000.00),
    (2,  'Bob',   'Marketing',  3.15, 2026,    0.00),
    (3,  'Carol', 'Finance',    3.91, 2027, 7500.00),
    (4,  'David', 'Accounting', 2.78, 2026,    0.00),
    (5,  'Emma',  'Marketing',  3.45, 2028, 3000.00),
    (6,  'Frank', 'Management', 3.60, 2027, 4000.00),
    (7,  'Grace', 'Finance',    3.25, 2028, 2500.00),
    (8,  'Henry', 'Accounting', 3.70, 2026, 5000.00),
    (9,  'Iris',  'Management', 2.95, 2028,    0.00),
    (10, 'Jack',  'Marketing',  3.55, 2027, 3500.00);
```

---

## Intermediate Queries

* These queries go beyond the basics. 
* You will learn how to 
	* rename columns, 
	* do arithmetic, 
	* filter on groups, 
	* use CASE expressions, 
	* work with NULL, 
	* combine multiple techniques, and 
	* write subqueries.

---

### Query 1 — Column Aliases with AS

* You can rename any column in the output using `AS`.
* This makes results easier to read — especially for computed values.

```sql
SELECT first_name         AS student,
       major              AS field_of_study,
       gpa                AS grade_point_avg,
       scholarship_amount AS award
FROM   students
ORDER BY student;
```

---

### Query 2 — Arithmetic in SELECT

* SQL can do math directly in a query.
* Let's calculate a projected GPA boost of 0.10 for each student
and see the result alongside the original.

```sql
SELECT first_name,
       gpa                   AS current_gpa,
       ROUND(gpa + 0.10, 2)  AS projected_gpa
FROM   students
ORDER BY projected_gpa DESC;
```

---

### Query 3 — HAVING — Filter After Grouping

* `WHERE` filters individual rows **before** grouping.
* `HAVING` filters entire groups **after** grouping.
* Show only majors where the average GPA is above 3.4.

```sql
SELECT   major,
         COUNT(*)           AS num_students,
         ROUND(AVG(gpa), 2) AS avg_gpa
FROM     students
GROUP BY major
HAVING   AVG(gpa) > 3.4
ORDER BY avg_gpa DESC;
```

---

### Query 4 — WHERE vs HAVING Together

* You can use both in the same query.
* First `WHERE` removes individual rows, then `GROUP BY` groups what's left,
* Then `HAVING` removes groups that don't qualify.
* Find majors with average scholarship above $2,000 — but only count students graduating in 2027 or later.

```sql
SELECT   major,
         COUNT(*)                       AS num_students,
         ROUND(AVG(scholarship_amount)) AS avg_scholarship
FROM     students
WHERE    graduation_year >= 2027
GROUP BY major
HAVING   AVG(scholarship_amount) > 2000
ORDER BY avg_scholarship DESC;
```

---

### Query 5 — CASE Expression — Categorize Data

`CASE` works like an if/else inside SQL.
Classify each student's GPA into a letter-grade category.

```sql
SELECT first_name,
       gpa,
       CASE
           WHEN gpa >= 3.7 THEN 'A'
           WHEN gpa >= 3.3 THEN 'B+'
           WHEN gpa >= 3.0 THEN 'B'
           ELSE                 'Below B'
       END AS letter_grade
FROM   students
ORDER BY gpa DESC;
```

---

### Query 6 — CASE Inside an Aggregate

You can combine `CASE` with `COUNT` to build a summary table.
How many students fall into each scholarship tier?

```sql
SELECT CASE
           WHEN scholarship_amount = 0                THEN 'No Award'
           WHEN scholarship_amount BETWEEN 1 AND 3999 THEN 'Partial Award'
           ELSE                                            'Full Award'
       END              AS scholarship_tier,
       COUNT(*)         AS num_students
FROM   students
GROUP BY scholarship_tier
ORDER BY num_students DESC;
```

---

### Query 7 — NOT and != — Exclude Rows

`!=` means "not equal." `NOT` negates a condition.
Find all students who are NOT in Finance.

```sql
SELECT first_name,
       major,
       gpa
FROM   students
WHERE  major != 'Finance'
ORDER BY gpa DESC;
```

---

### Query 8 — NOT IN — Exclude Multiple Values

`NOT IN` is the opposite of `IN`.
Find students who are in neither Marketing nor Management.

```sql
SELECT first_name,
       major,
       gpa
FROM   students
WHERE  major NOT IN ('Marketing', 'Management')
ORDER BY first_name;
```

---

### Query 9 — LIKE Patterns — Wildcards

`%` matches any number of characters. `_` matches exactly one character.
Find students whose name has exactly 5 letters.

```sql
SELECT first_name,
       major
FROM   students
WHERE  first_name LIKE '_____';
```

---

### Query 10 — Multiple Aggregates per Group

You can compute several statistics in one query.
For each graduation year, show the count, GPA range, and total scholarships.

```sql
SELECT   graduation_year,
         COUNT(*)                       AS num_students,
         MIN(gpa)                       AS min_gpa,
         MAX(gpa)                       AS max_gpa,
         ROUND(MAX(gpa) - MIN(gpa), 2)  AS gpa_spread,
         SUM(scholarship_amount)        AS total_scholarships
FROM     students
GROUP BY graduation_year
ORDER BY graduation_year;
```

---

### Query 11 — Subquery in WHERE

A subquery is a query inside another query.
Find students whose GPA is above the overall average.

```sql
SELECT first_name,
       major,
       gpa
FROM   students
WHERE  gpa > (SELECT AVG(gpa) FROM students)
ORDER BY gpa DESC;
```


---

### Query 12 — Subquery — Who Has the Highest GPA?

Find the student(s) with the single highest GPA.
The inner query finds the maximum; the outer 
query finds who has it.

* **Solution-1:**

```sql
SELECT first_name,
       major,
       gpa
FROM   students
WHERE  gpa = (SELECT MAX(gpa) FROM students);
```

OR

* **Solution-2:**

```sql
WITH max_gpa_table AS (
    SELECT MAX(gpa) AS max_gpa
    FROM students
)
SELECT s.first_name,
       s.major,
       s.gpa
FROM   students s, 
       max_gpa_table m
WHERE  s.gpa = m.max_gpa;
```

OR

* **Solution-3:**

```sql
WITH max_gpa_table AS (
    SELECT MAX(gpa) AS max_gpa
    FROM students
)
SELECT first_name,
       major,
       gpa
FROM   students
WHERE  gpa = (SELECT max_gpa FROM max_gpa_table);
```

### Query 12 — Discussion

If you only need one top student:

```sql
SELECT first_name, major, gpa
FROM   students
ORDER BY gpa DESC
LIMIT 1;
```

	NOTE-1:  
		   But be careful — if two students 
		   share the highest GPA, LIMIT 1 only 
		   returns ONE of them. The subquery 
		   version returns all tied students. 
		

	NOTE-2:
		   So the subquery version is already 
		   the simplest correct approach when 
		   ties matter.
		
---

### Query 13 — Ranking with ROW_NUMBER

`ROW_NUMBER()` assigns a rank to each row based 
on an ordering. 

Rank all students by GPA from highest to lowest.

```sql
SELECT ROW_NUMBER() OVER (ORDER BY gpa DESC) AS rank,
       first_name,
       major,
       gpa
FROM   students;
```

---

### Query 14 — Ranking Within Groups with PARTITION BY

`PARTITION BY` restarts the ranking for each group.

Rank students within their own major by GPA.

```sql
SELECT major,
       first_name,
       gpa,
       ROW_NUMBER() OVER (
           PARTITION BY major
           ORDER BY gpa DESC
       ) AS rank_in_major
FROM   students
ORDER BY major, rank_in_major;
```

---

### Query 15 — Putting It All Together

Combine several techniques in one query: 

* CASE, 
* aggregation,
* HAVING, and 
* ORDER BY.

For each major, show the number of students, 
average GPA, a performance label, and total 
scholarship money — but only for majors with 
2 or more students.

* **solution-1**:

```sql
SELECT   major,
         COUNT(*)                 AS num_students,
         ROUND(AVG(gpa), 2)       AS avg_gpa,
         
         CASE
             WHEN AVG(gpa) >= 3.5 THEN 'Strong'
             WHEN AVG(gpa) >= 3.2 THEN 'Solid'
             ELSE                      'Developing'
         END                         AS performance,
         
         SUM(scholarship_amount)     AS total_scholarships
FROM     students
GROUP BY major
HAVING   COUNT(*) >= 2
ORDER BY avg_gpa DESC;
```

* **solution-2**: replace `COUNT(*)` with `num_students `

```sql
SELECT   major,
         COUNT(*)                 AS num_students,
         ROUND(AVG(gpa), 2)       AS avg_gpa,
         
         CASE
             WHEN AVG(gpa) >= 3.5 THEN 'Strong'
             WHEN AVG(gpa) >= 3.2 THEN 'Solid'
             ELSE                      'Developing'
         END                         AS performance,
         
         SUM(scholarship_amount)     AS total_scholarships
FROM     students
GROUP BY major
HAVING   num_students >= 2
ORDER BY avg_gpa DESC;
```

---

## What You Learned Today

| Concept | SQL Keyword | What It Does |
|---------|-------------|--------------|
| Rename columns | `AS` | Gives a column a display name |
| Do math | `+`, `-`, `*`, `/` in SELECT | Computes values on the fly |
| Filter groups | `HAVING` | Like WHERE, but runs after GROUP BY |
| Conditional logic | `CASE WHEN ... THEN ... END` | If/else inside SQL |
| Exclude rows | `!=`, `NOT`, `NOT IN` | Keeps rows that don't match |
| Wildcard matching | `_` in LIKE | Matches exactly one character |
| Subquery | `(SELECT ... )` inside WHERE | A query inside another query |
| Row numbering | `ROW_NUMBER() OVER (...)` | Assigns a rank to each row |
| Rank within groups | `PARTITION BY` | Restarts ranking per group |
| Combined techniques | Multiple clauses together | Real-world queries use many features at once |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
