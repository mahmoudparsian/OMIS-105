# OMIS 105 <br>Introduction to SQL with qStudio

* **Course:** OMIS 105 — Introduction to Database Management Systems
* **Quarter:** Fall 2026
* **Author:** Dr. Mahmoud Parsian

---
# qStudio

* qStudio is a free, open-source SQL editor
* qStudio is a data analysis tool 

* Download page: `https://www.timestored.com/qstudio/download`

---

## What Is a Table?

* A database stores information in **tables** 
* A table has rows and columns.
* Each **row** is one row/record 
	* one student, one product, one transaction.
* Each **column** is one piece of information 
	* (`student_id` , `first_name`, `major`, `GPA`).

---

# A Table: `students`

|student_id | first_name | major       | gpa   |              
|-----------|------------|-------------|-------|
|`100`      | `Alex`     | `Business`  | `3.2` |              
|`300`      | `Jane`     | `AI`        | `3.4` |              
|`400`      | `Megan`    | `Business ` | `3.0` |              
|`700`      | `Janet`    | `AI`        | `3.8` |              
|`900`      | `Rafa`     | `Business ` | `3.1` |         
--- 

## What to do

Today we will: use  **SQL** (Structured Query Language)

1. Create a table, 
2. Fill/insert/populate it with data/rows/records, and 
3. Ask questions about that data using SQL

---

## Getting Started

Open **qStudio** and make sure you are connected to **DuckDB** (in-memory).
Copy each SQL block below into the query editor and press
**Cmd+Enter** (Mac) or **Ctrl+Enter** (Windows) to run it.

---

## Step 1 — Create the Table

* We define a table called **`students`** with six columns.
* Think of this as setting up the column headers in a blank spreadsheet.

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

---

## Step 2 — Insert Data

Now we fill the table with 10 student records.

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

## Now Let's Query the Data

Each query below asks a different question about our `students` table.
Read the explanation first, then run the SQL.

---

### Query 1 — See All the Data

The simplest query: 

* show every row and every column.
* The `*` means "all columns."

```sql
SELECT *
FROM  students;
```

---

### Query 2 — Choose Specific Columns

We don't always need every column.
Here we ask for just the name, major, and GPA.

```sql
SELECT first_name,
       major,
       gpa
FROM   students;
```

---

### Query 3 — Filter Rows with WHERE

`WHERE` keeps only the rows that match a condition.
Let's find all Finance majors.

```sql
SELECT first_name,
       major,
       gpa
FROM   students
WHERE  major = 'Finance';
```

---

### Query 4 — Combine Conditions with AND

`AND` means **both** conditions must be true.
Find students graduating in 2027 who also have a GPA above 3.5.

```sql
SELECT first_name,
       gpa,
       graduation_year
FROM   students
WHERE  gpa > 3.5
  AND  graduation_year = 2027;
```

---

### Query 5 — Either Condition with OR

`OR` means **at least one** condition must be true.
Find students in Finance or Marketing.

```sql
SELECT first_name,
       major,
       gpa
FROM   students
WHERE  major = 'Finance'
   OR  major = 'Marketing';
```

---

### Query 6 — Filter with IN

`IN` is a shorthand for multiple `OR` conditions on the same column.
This is the same question as Query 5, written more cleanly.

```sql
SELECT first_name,
       major,
       gpa
FROM   students
WHERE  major IN ('Finance', 'Marketing');
```

---

### Query 7 — Filter a Range with BETWEEN

`BETWEEN` checks if a value falls within a range (inclusive on both ends).
Find students with a GPA from 3.0 to 3.5.

```sql
SELECT first_name,
       major,
       gpa
FROM   students
WHERE  gpa BETWEEN 3.0 AND 3.5;
```

---

### Query 8 — Search Text with LIKE

`LIKE` searches for patterns in text.
The `%` means "anything can come after."
Find students whose name starts with the letter "A."

```sql
SELECT first_name,
       major
FROM   students
WHERE  first_name LIKE 'A%';
```

---

### Query 9 — Sort Results (Low to High)

`ORDER BY` arranges the output. The default is ascending (low to high).
Show all students sorted by GPA from lowest to highest.

```sql
SELECT first_name,
       major,
       gpa
FROM   students
ORDER BY gpa ASC;
```

---

### Query 10 — Sort Results (High to Low)

Add `DESC` to sort in descending order (high to low).
Who has the highest GPA?

```sql
SELECT first_name,
       major,
       gpa
FROM   students
ORDER BY gpa DESC;
```

---

### Query 11 — Show Only the Top Rows

`LIMIT` restricts how many rows are returned.
Show the top 3 students by GPA.

```sql
SELECT first_name,
       major,
       gpa
FROM   students
ORDER BY gpa DESC
LIMIT  3;
```

---

### Query 12 — Find Unique Values with DISTINCT

`DISTINCT` removes duplicates.
What majors do our students have?

```sql
SELECT DISTINCT major
FROM   students
ORDER BY major;
```

---

### Query 13 — Count the Rows

`COUNT(*)` tells us how many rows match.
How many students are in the table?

```sql
SELECT COUNT(*) AS total_students
FROM   students;
```

---

### Query 14 — Calculate Summary Statistics

SQL can compute averages, minimums, maximums, and totals in one query.
What is the average GPA? The highest? The lowest? The total scholarship money awarded?

```sql
SELECT COUNT(*)                   AS total_students,
       ROUND(AVG(gpa), 2)         AS average_gpa,
       MIN(gpa)                   AS lowest_gpa,
       MAX(gpa)                   AS highest_gpa,
       SUM(scholarship_amount)    AS total_scholarships
FROM   students;
```

---

### Query 15 — Group and Summarize

`GROUP BY` splits the data into groups and computes a summary for each one.
How many students are in each major, and what is the average GPA per major?

```sql
SELECT   major,
         COUNT(*)           AS num_students,
         ROUND(AVG(gpa), 2) AS avg_gpa
FROM     students
GROUP BY major
ORDER BY avg_gpa DESC;
```

---

## What You Learned Today

| Concept | SQL Keyword | What It Does |
|---------|-------------|--------------|
| Create a table | `CREATE TABLE` | Defines column names and types |
| Add data | `INSERT INTO` | Puts rows into the table |
| See everything | `SELECT *` | Returns all columns |
| Pick columns | `SELECT col1, col2` | Returns only the columns you name |
| Filter rows | `WHERE` | Keeps rows that match a condition |
| Both conditions | `AND` | Both must be true |
| Either condition | `OR` | At least one must be true |
| Match a list | `IN` | Shorthand for multiple OR conditions |
| Match a range | `BETWEEN` | Value falls within a range |
| Search text | `LIKE` | Pattern matching with `%` wildcard |
| Sort output | `ORDER BY` | Arranges rows (ASC or DESC) |
| Limit output | `LIMIT` | Restricts how many rows are shown |
| Remove duplicates | `DISTINCT` | Shows unique values only |
| Count rows | `COUNT(*)` | How many rows match |
| Summarize numbers | `AVG`, `MIN`, `MAX`, `SUM` | Compute statistics |
| Group and summarize | `GROUP BY` | Compute statistics per group |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
