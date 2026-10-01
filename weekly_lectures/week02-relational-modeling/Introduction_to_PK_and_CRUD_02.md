# Beginner's Guide to Primary Keys and CRUD in DuckDB

Welcome to your first step into database management! In this tutorial, you will learn two fundamental concepts in relational databases:

1. **Primary Keys (PK)**

2. **CRUD Operations** (Create, Read, Update, Delete)

We will use **DuckDB**, a fast, easy-to-use, and lightweight SQL database engine designed for analytical and general database tasks.

## 1. Understanding Primary Keys (PK)

### What is a Primary Key?

A **Primary Key (PK)** is a specific column (or set of columns) in a database table designed to uniquely identify each row or record. Think of it like your student ID number or Social Security Number—no two individuals share the same ID.

### Key Rules for Primary Keys:

* **Uniqueness:** Every value in the primary key column must be completely unique. No duplicate values are allowed.

* **Non-Null:** A primary key column cannot contain `NULL` (empty or missing) values. Every row must have a valid ID.

* **Single Identity:** A table can only have one primary key constraint.

## 2. Setting Up the Database & Schema

Before performing operations, let's create a table called `students`.

### The `students` Schema Definition:

We will define our table with the following columns:

* `id`: **INTEGER** (Primary Key)

* `name`: **VARCHAR** (Text string)

* `major`: **VARCHAR**

* `age`: **INTEGER**

* `gender`: **VARCHAR**

* `country`: **VARCHAR**

### SQL Query to Create the Table:

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    major VARCHAR,
    age INTEGER,
    gender VARCHAR,
    country VARCHAR
);
```

> **Note:** In DuckDB, assigning `PRIMARY KEY` 
> to `id` ensures that DuckDB enforces uniqueness 
> and non-null constraints automatically.

## 3. What is CRUD?

**CRUD** is an acronym for the four basic operations 
you can perform on database data:

| Letter | Operation  | SQL Command Equivalent | Purpose              | 
| ------ | ---------- | ---------------------- | -------------------- | 
| **C**  | **Create** | `INSERT INTO`          | Add new data/records | 
| **R**  | **Read**   | `SELECT`               | Query/retrieve existing data | 
| **U**  | **Update** | `UPDATE`               | Modify existing data | 
| **D**  | **Delete** | `DELETE FROM`          | Remove/Delete data | 

## 4. Step-by-Step CRUD Tutorial

### Step 1: CREATE (Inserting Records)

To **Create** data in a table, we use the `INSERT INTO` command followed by the values we wish to store. Let's populate our table with **8 initial records**.

```sql
INSERT INTO students (id, name, major, age, gender, country) 
VALUES 
 (1, 'Alice Smith', 'Computer Science', 20, 'Female', 'USA'),
 (2, 'Bob Jones', 'Mathematics', 22, 'Male', 'Canada'),
 (3, 'Charlie Brown', 'Physics', 21, 'Male', 'UK'),
 (4, 'Diana Prince', 'Computer Science', 19, 'Female', 'USA'),
 (5, 'Ethan Hunt', 'Engineering', 23, 'Male', 'Australia'),
 (6, 'Fiona Gallagher', 'Biology', 20, 'Female', 'Ireland'),
 (7, 'George Clark', 'Mathematics', 22, 'Male', 'USA'),
 (8, 'Hannah Abbott', 'Chemistry', 21, 'Female', 'UK');
```

#### Detailed Breakdown:

* `INSERT INTO students (...)`: <br>
Specifies which table and columns receive data.

* `VALUES (...), (...)`: <br>
Provides the tuple dataset. Notice how each `id` is unique ($1$ through $8$).

### Step 2: READ (Retrieving Records)

To **Read** or query data from your table, we use the `SELECT` statement.

#### 2.1 Retrieve All Records

To view every row and column in the `students` table, use the asterisk (`*`) wildcard:

```sql
SELECT * 
FROM students;
```

**Output Preview:**

```
┌───────┬─────────────────┬──────────────────┬───────┬─────────┬───────────┐
│  id   │      name       │      major       │  age  │ gender  │  country  │
│ int32 │     varchar     │     varchar      │ int32 │ varchar │  varchar  │
├───────┼─────────────────┼──────────────────┼───────┼─────────┼───────────┤
│     1 │ Alice Smith     │ Computer Science │    20 │ Female  │ USA       │
│     2 │ Bob Jones       │ Mathematics      │    22 │ Male    │ Canada    │
│     3 │ Charlie Brown   │ Physics          │    21 │ Male    │ UK        │
│     4 │ Diana Prince    │ Computer Science │    19 │ Female  │ USA       │
│     5 │ Ethan Hunt      │ Engineering      │    23 │ Male    │ Australia │
│     6 │ Fiona Gallagher │ Biology          │    20 │ Female  │ Ireland   │
│     7 │ George Clark    │ Mathematics      │    22 │ Male    │ USA       │
│     8 │ Hannah Abbott   │ Chemistry        │    21 │ Female  │ UK        │
└───────┴─────────────────┴──────────────────┴───────┴─────────┴───────────┘
```


#### 2.2 Select Specific Columns

If you only need students' names and majors:

```sql
SELECT name, major 
FROM students;
```

#### 2.3 Filter Data Using the `WHERE` Clause

To retrieve specific records matching criteria 
(e.g., all students majoring in **Computer Science**):

```sql
SELECT * 
FROM students 
WHERE major = 'Computer Science';
```

#### 2.4 Combining Filters (`AND` / `OR`)

Find all students from the **USA** who are older than **20**:

```sql
SELECT name, age, country 
FROM students 
WHERE country = 'USA' AND 
      age > 20;
```

### Step 3: UPDATE (Modifying Existing Records)

The **Update** operation modifies existing records in a table.

> **CRITICAL WARNING:** Always use a `WHERE` clause when updating! If you omit the `WHERE` clause, **every single row in your table will be updated.**

#### Scenario A: Update a single student's record using the Primary Key

Let's change **Charlie Brown's** (`id = 3`) major to `Data Science`:

```sql
UPDATE students 
SET major = 'Data Science' 
WHERE id = 3;
```

#### Verification:

```sql
SELECT * 
FROM students 
WHERE id = 3;
```

#### Scenario B: Update multiple attributes at once

Let's update **Alice Smith's** (`id = 1`) age and country:

```sql
UPDATE students 
SET age = 21, country = 'Canada' 
WHERE id = 1;
```

### Step 4: DELETE (Removing Records)

The **Delete** operation removes one or more rows from a table.

> **CRITICAL WARNING:** Just like `UPDATE`, always use a `WHERE` clause with `DELETE`. Omitting `WHERE` will erase all rows in the table!

#### Scenario A: Remove a record using the Primary Key

Suppose **George Clark** (`id = 7`) graduates and leaves the dataset. We remove his record using his unique Primary Key:

```sql
DELETE FROM students 
WHERE id = 7;
```

#### Verification:

```sql
SELECT * 
FROM students;
```

*(Notice that row with `id = 7` is no longer present.)*

#### Scenario B: Remove records based on a condition

Delete all students who are from **Ireland**:

```sql
DELETE FROM students 
WHERE country = 'Ireland';
```

---

## 5. Grouping Data with `GROUP BY`

The `GROUP BY` clause groups rows that have the same 
values in specified columns into summary rows. It is 
frequently paired with aggregate functions like 

* `COUNT()` 
* `AVG()` 
* `MAX()`
* `MIN()`

Assume we are operating on our original dataset of 8 students.

### Example 1: Count the Number of Students by Country

**Goal:** Find out how many students are enrolled from each country.

```sql
SELECT country, 
       COUNT(*) AS student_count
FROM students
GROUP BY country;
```

**How it works:**
* `GROUP BY country` gathers all rows with matching country 
values into single groups.
* `COUNT(*)` counts how many students belong to each group.

---

### Example 2: Calculate the Average Age by Major

**Goal:** Find the average age of students within each major area of study.

```sql
SELECT major, 
       AVG(age) AS average_age
FROM students
GROUP BY major;
```

**How it works:**
* `GROUP BY major` categorizes students by their field of study.
* `AVG(age)` computes the mean age for students in each specific major.

---

### Example 3: Multi-Column Grouping (Gender Breakdown per Country)

**Goal:** Count how many male and female students are in each country.

```sql
SELECT country, gender, 
       COUNT(*) AS student_count
FROM students
GROUP BY country, gender
ORDER BY country;
```

**How it works:**
* `GROUP BY country, gender` creates subgroups for every unique pair of country and gender (e.g., USA-Female, USA-Male, UK-Female, UK-Male).

---

### Example 4: Filtering Grouped Results with `HAVING`

**Goal:** List only the countries that have 
**more than 1 student** enrolled.

```sql
SELECT country, 
       COUNT(*) AS total_students
FROM students
GROUP BY country
HAVING COUNT(*) > 1;
```

**How it works:**
* `WHERE` filters individual rows **before** grouping occurs.
* `HAVING` filters aggregated group results **after** grouping takes place.

---

## 6. Summary Cheat Sheet

| Operation | SQL Pattern | Example | 
| ----- | ----- | ----- | 
| **Create** | `INSERT INTO table (cols) VALUES (vals);` | `INSERT INTO students VALUES (9, 'Ian', 'Art', 20, 'Male', 'France');` | 
| **Read** | `SELECT cols FROM table WHERE condition;` | `SELECT * FROM students WHERE age >= 21;` | 
| **Update** | `UPDATE table SET col = val WHERE condition;` | `UPDATE students SET age = 22 WHERE id = 2;` | 
| **Delete** | `DELETE FROM table WHERE condition;` | `DELETE FROM students WHERE id = 5;` | 
| **Group By** | `SELECT col, AGG(col) FROM table GROUP BY col;` | `SELECT major, COUNT(*) FROM students GROUP BY major;` | 

## Next Steps & Practice Exercises

1. Try adding a 9th student with `id = 1` to see how DuckDB handles Primary Key constraint violations.

2. Practice writing a query that retrieves all female students majoring in either `Computer Science` or `Mathematics`.

3. Write a query using `GROUP BY` to find the oldest student (`MAX(age)`) in each major.