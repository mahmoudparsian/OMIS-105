# Comprehensive DuckDB Table and <br> Column Definitions Guide

* This guide provides a step-by-step tutorial 
on defining tables, column types, and constraints 
in **DuckDB**, progressing from **Basic** to 
**Intermediate** and **Advanced** concepts. 

* It also includes examples of reading external 
  CSV files and triggering constraint violation 
  errors.

---

## Level 1: Basic Column Definitions & Constraints

At the foundational level, table creation involves selecting core data types (`INTEGER`, `VARCHAR`, `DECIMAL`, `DATE`, `BOOLEAN`) and basic rules like `PRIMARY KEY`, `NOT NULL`, and `DEFAULT`.

### Step 1.1: Simple Schema (`students` & `courses`)

```sql
-- 1. Create a sequence (a number counter)
CREATE SEQUENCE student_id_seq START 1;

-- 2. Create the students table.
--    student_id is an auto-increment column:
--    the sequence fills it in with 1, 2, 3, ...
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY DEFAULT nextval('student_id_seq'),
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    is_active BOOLEAN DEFAULT TRUE
);

-- 3. Create the courses table (a text primary key, no sequence needed)
CREATE TABLE courses (
    course_code VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR NOT NULL,
    credits INTEGER DEFAULT 3 CHECK (credits > 0)
);
```

### Step 1.2: Insert Valid Rows

We do **not** give `student_id`, `enrollment_date`,
or `is_active`. DuckDB fills them in from their
`DEFAULT` values.

```sql
-- Insert into students
INSERT INTO students (first_name, last_name, email)
VALUES 
    ('Alice', 'Smith', 'alice@example.edu'),
    ('Bob', 'Jones', 'bob@example.edu');

-- Insert into courses
INSERT INTO courses (course_code, course_name, credits)
VALUES 
    ('CS101', 'Introduction to Computer Science', 4),
    ('DATA201', 'Data Wrangling with SQL', 3);
```

### Step 1.3: Viewing Results

```sql
SELECT * FROM students;
```

| student_id | first_name | last_name | email | enrollment_date | is_active |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `1` | Alice | Smith | `alice@example.edu` | `2026-10-07` | `true` |
| `2` | Bob | Jones | `bob@example.edu` | `2026-10-07` | `true` |

```sql
SELECT * FROM courses;
```

| course_code | course_name | credits |
| :--- | :--- | :--- |
| `CS101` | Introduction to Computer Science | `4` |
| `DATA201` | Data Wrangling with SQL | `3` |

### Step 1.4: Constraint Violation Examples (Basic)

#### Error 1: NOT NULL Violation
```sql
-- Missing required 'last_name'
INSERT INTO students (first_name, email)
VALUES ('Charlie', 'charlie@example.edu');
```
> **DuckDB Error:** `Constraint Error: NOT NULL constraint failed: students.last_name`

#### Error 2: UNIQUE Violation
```sql
-- Attempting to use Alice's existing email
INSERT INTO students (first_name, last_name, email)
VALUES ('Eve', 'Smith', 'alice@example.edu');
```
> **DuckDB Error:** `Constraint Error: Duplicate key "email: alice@example.edu" violates unique constraint.`

---

## Level 2: Intermediate Schema & CSV File Ingestion

Intermediate definitions introduce **Foreign Keys** to connect tables, custom **ENUM** types, and reading directly from **CSV files**.

### Step 2.1: Custom ENUM Types & Foreign Key Relationships

```sql
-- 1. Define custom ENUM types
CREATE TYPE grade_letter AS ENUM ('A', 'B', 'C', 'D', 'F', 'P', 'NP');

-- 2. Create a sequence
CREATE SEQUENCE enrollment_id_seq START 1;

-- 3. Create Enrollments junction table
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY DEFAULT nextval('enrollment_id_seq'),
    student_id INTEGER NOT NULL,
    course_code VARCHAR(10) NOT NULL,
    final_grade grade_letter,
    score DECIMAL(5,2) CHECK (score >= 0.00 AND score <= 100.00),
    
    -- Defining Foreign Keys
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
);
```

### Step 2.2: Insert Valid Rows

```sql
INSERT INTO enrollments (student_id, course_code, final_grade, score)
VALUES 
    (1, 'CS101', 'A', 94.50),
    (1, 'DATA201', 'B', 88.00),
    (2, 'CS101', 'C', 76.25);
```

```sql
SELECT * FROM enrollments;
```

| enrollment_id | student_id | course_code | final_grade | score |
| :--- | :--- | :--- | :--- | :--- |
| `1` | `1` | `CS101` | `A` | `94.50` |
| `2` | `1` | `DATA201` | `B` | `88.00` |
| `3` | `2` | `CS101` | `C` | `76.25` |

### Step 2.3: Reading CSV Files & Creating Tables directly

DuckDB makes loading external data easy. You can query a CSV file directly, or create a table from it.

Suppose you have a file named `professors.csv` with these contents:

```csv
prof_id,first_name,last_name,department,salary
101,Grace,Hopper,Computer Science,95000.00
102,Edgar,Codd,Database Systems,92000.00
103,Ada,Lovelace,Mathematics,98000.00
```

#### Option A: Query CSV Directly without loading into a table
```sql
SELECT * FROM read_csv_auto('professors.csv');
```

#### Option B: Create a table directly from the CSV
```sql
-- DuckDB infers data types automatically
CREATE TABLE professors AS 
SELECT * FROM read_csv_auto('professors.csv');
```

#### Option C: Create table with strict column types first, then read CSV
```sql
CREATE TABLE strict_professors (
    prof_id INTEGER PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    department VARCHAR DEFAULT 'General',
    salary DECIMAL(10,2) CHECK (salary > 0)
);

-- Populate the table from the CSV.
-- The CSV columns must be in the same order as the table columns.
INSERT INTO strict_professors
SELECT * FROM read_csv_auto('professors.csv');
```

Option C is the safest: every row is checked
against the `PRIMARY KEY`, `NOT NULL`, and `CHECK`
rules as it is loaded.

> `read_csv_auto()` and `read_csv()` do the same
> thing in current DuckDB versions. Both detect the
> column names and types for you.

```sql
SELECT * FROM strict_professors;
```

| prof_id | first_name | last_name | department | salary |
| :--- | :--- | :--- | :--- | :--- |
| `101` | Grace | Hopper | Computer Science | `95000.00` |
| `102` | Edgar | Codd | Database Systems | `92000.00` |
| `103` | Ada | Lovelace | Mathematics | `98000.00` |

### Step 2.4: Constraint Violation Examples (Intermediate)

#### Error 1: FOREIGN KEY Violation
```sql
-- Attempting to enroll student_id 999 which does not exist in 'students'
INSERT INTO enrollments (student_id, course_code, final_grade, score)
VALUES (999, 'CS101', 'A', 90.00);
```
> **DuckDB Error:** `Constraint Error: Violates foreign key constraint because key "student_id: 999" does not exist in the referenced table`

#### Error 2: ENUM Type Violation
```sql
-- 'E' is not a valid value in grade_letter ENUM ('A', 'B', 'C', 'D', 'F', 'P', 'NP')
INSERT INTO enrollments (student_id, course_code, final_grade, score)
VALUES (1, 'CS101', 'E', 80.00);
```
> **DuckDB Error:** `Conversion Error: Could not convert string 'E' to UINT8`
>
> (This means *"`'E'` is not in the ENUM list."* DuckDB stores ENUM values as small numbers, `UINT8`, behind the scenes.)

#### Error 3: CHECK Constraint Range Violation
```sql
-- Score exceeds maximum allowed (100.00)
INSERT INTO enrollments (student_id, course_code, final_grade, score)
VALUES (2, 'DATA201', 'A', 105.00);
```
> **DuckDB Error:** `Constraint Error: CHECK constraint failed on table enrollments with expression CHECK(((score >= 0.00) AND (score <= 100.00)))`

---

## Level 3: Advanced Column Definitions & Data Structures

DuckDB supports nested data types: **LIST** (an ordered list of values), **STRUCT** (a record with named fields), and **MAP** (key-value pairs). It can also generate random **UUID** keys.

### Step 3.1: Advanced Schema (`assignment_submissions`)

```sql
CREATE TABLE assignment_submissions (
    -- UUID key: a random, unique ID (not 1, 2, 3, ...)
    submission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id INTEGER NOT NULL REFERENCES students(student_id),
    course_code VARCHAR(10) NOT NULL REFERENCES courses(course_code),
    
    -- LIST column: ordered list of submission file names
    submitted_files VARCHAR[],
    
    -- STRUCT column: a nested record with fixed field names
    metadata STRUCT(
        submission_time TIMESTAMP, 
        ip_address VARCHAR, 
        file_size_mb DECIMAL(4,2)
    ),
    
    -- MAP column: flexible key-value pairs for rubric scores
    rubric_scores MAP(VARCHAR, DECIMAL(4,1))
);
```

### Step 3.2: Insert Valid Rows with Complex Types

```sql
INSERT INTO assignment_submissions (
    student_id, 
    course_code, 
    submitted_files, 
    metadata, 
    rubric_scores
)
VALUES (
    1, 
    'CS101', 
    ['main.py', 'utils.py', 'README.md'], -- LIST
    {'submission_time': TIMESTAMP '2026-10-07 14:30:00', 'ip_address': '192.168.1.50', 'file_size_mb': 2.45}, -- STRUCT
    map(['Code Quality', 'Test Cases', 'Documentation'], [9.5, 10.0, 8.5]) -- MAP
);
```

### Step 3.3: Querying Nested Data Types

```sql
SELECT 
    submission_id,
    submitted_files[1] AS primary_file,
    metadata.submission_time AS submitted_at,
    metadata.file_size_mb AS size_mb,
    rubric_scores['Code Quality'] AS code_quality_score
FROM assignment_submissions;
```

| submission_id | primary_file | submitted_at | size_mb | code_quality_score |
| :--- | :--- | :--- | :--- | :--- |
| `d8b2e1f4-...` | `main.py` | `2026-10-07 14:30:00` | `2.45` | `9.5` |

Your `submission_id` will be different: it is random.
Note that list positions in DuckDB start at **1**,
so `submitted_files[1]` is the first file.
For a MAP, `rubric_scores['Code Quality']` looks up
the value stored under that key.

---

## Quick Reference: Summary of Column Definition Properties

| Category | Keyword / Syntax | Description | Example |
| :--- | :--- | :--- | :--- |
| **Basic Types** | `INTEGER`, `VARCHAR`, `DECIMAL(p,s)`, `DATE`, `BOOLEAN` | Core standard SQL data types. | `price DECIMAL(8,2)` |
| **Identity** | `PRIMARY KEY` | Uniquely identifies rows; cannot be null. | `id INTEGER PRIMARY KEY` |
| **Identity** | `SEQUENCE` + `DEFAULT nextval()` | Auto-increment: assigns 1, 2, 3, ... to new rows. (DuckDB has no `AUTOINCREMENT` keyword.) | `CREATE SEQUENCE id_seq START 1;` then `id INTEGER PRIMARY KEY DEFAULT nextval('id_seq')` |
| **Identity** | `UUID DEFAULT gen_random_uuid()` | Assigns a random, unique ID to new rows. | `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` |
| **Integrity** | `NOT NULL` | Disallows `NULL` values. | `name VARCHAR NOT NULL` |
| **Integrity** | `UNIQUE` | Enforces distinct values across all rows. | `email VARCHAR UNIQUE` |
| **Integrity** | `CHECK (condition)` | Validates logic expression on column value. | `CHECK (age >= 18)` |
| **Integrity** | `FOREIGN KEY` | Ensures referential link to a target table. | `FOREIGN KEY (a_id) REFERENCES target(id)` |
| **Default** | `DEFAULT expression` | Sets fall-back value if none is provided. | `created_at DEFAULT CURRENT_TIMESTAMP` |
| **Advanced** | `ENUM(...)` | Restricts column to pre-defined set of values. | `CREATE TYPE status AS ENUM ('a', 'b')` |
| **Advanced** | `LIST` (`TYPE[]`) | Dynamic array of elements. | `tags VARCHAR[]` |
| **Advanced** | `STRUCT(...)` | Nested record with fixed field names. | `user STRUCT(name VARCHAR, age INT)` |
| **Advanced** | `MAP(key, value)` | Dynamic map of key-value pairs. | `attributes MAP(VARCHAR, VARCHAR)` |
| **Advanced** | `MAP(key, value)` | Flexible key-value pairs. | `scores MAP(VARCHAR, DECIMAL(4,1))` |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
