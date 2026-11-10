# Understanding First Normal Form (1NF) <br> in SQL & DuckDB

Welcome! If you already know basic SQL queries like `SELECT`, `WHERE`, and `JOIN`, you are ready to learn **Database Normalization**. 

* Normalization is the process of organizing data in a database to 
	* **reduce redundancy**, and 
	* **improve data integrity**. 

*  The very first step in this process is **First Normal Form (1NF)**.

---

## 1. What is First Normal Form (1NF)?

A table is in **First Normal Form (1NF)** if and only if it meets these four core rules:

1. **Atomic Values:** Every cell in a column must contain a **single, indivisible value** (no comma-separated lists, arrays, or multiple items in one cell).
2. **Unique Column Names:** Each column in a table must have a unique name.
3. **No Repeating Groups:** You should not have multiple columns storing the same type of data (e.g., `Phone1`, `Phone2`, `Phone3`).
4. **Primary Key:** Every table must have a primary key (a column or set of columns) that uniquely identifies each row.

---

## 2. Example 1: Eliminating Multi-Value Strings (Comma-Separated Lists)

### ❌ Before 1NF (Violates Rule 1: Not Atomic)
Here, the `courses` column contains multiple values separated by commas in a single cell.

**Table: `student_courses_bad`**

| student_id | student_name | courses |
| :--- | :--- | :--- |
| 101 | Alice | SQL, Python, DuckDB |
| 102 | Bob | Java, SQL |

> **Why is this bad?** <br>
> - How do you count how many students take `SQL`? <br>
> - How do you join this table with a `courses` table?
> - `WHERE courses = 'SQL'` will fail because the value is `'SQL, Python, DuckDB'`.

---

### ✅ After 1NF (Atomic Values & Primary Key)
To fix this, each row must represent **one student taking one course**.

**Table: `student_courses_1nf`**

| student_id | student_name | course_name |
| :--- | :--- | :--- |
| 101 | Alice | SQL |
| 101 | Alice | Python |
| 101 | Alice | DuckDB |
| 102 | Bob | Java |
| 102 | Bob | SQL |

* **Primary Key:** (`student_id`, `course_name`) — a composite primary key.

---

### 🦆 DuckDB Tip: How to convert non-1NF to 1NF using `STRING_SPLIT` & `UNNEST`
In DuckDB, if you ever inherit messy data like the non-1NF table above, you can unnest it easily:

```sql
-- Create non-1NF sample table
CREATE TABLE student_courses_bad AS 
SELECT 101 AS student_id, 'Alice' AS student_name, 'SQL, Python, DuckDB' AS courses
UNION ALL
SELECT 102, 'Bob', 'Java, SQL';

-- Transform into 1NF using DuckDB
CREATE TABLE student_courses_1nf AS
SELECT 
    student_id, 
    student_name, 
    UNNEST(STRING_SPLIT(courses, ', ')) AS course_name
FROM student_courses_bad;

-- View 1NF result
SELECT * FROM student_courses_1nf;
```

---

## 3. Example 2: Eliminating Repeating Groups (Numbered Columns)

### ❌ Before 1NF (Violates Rule 3: Repeating Groups)
Sometimes people try to avoid comma-separated strings by creating multiple numbered columns.

**Table: `employee_phones_bad`**

| emp_id | emp_name | phone_1 | phone_2 | phone_3 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Carol | 555-0101 | 555-0102 | NULL |
| 2 | Dave | 555-0199 | NULL | NULL |

> **Why is this bad?** <br>
> - What if an employee has 4 phone numbers? You have to alter the table schema to add `phone_4`. <br>
> - Search queries become messy: `WHERE phone_1 = '...' OR phone_2 = '...' OR phone_3 = '...'`. <br>
> - Lots of `NULL` values waste space and create unnecessary clutter.

---

### ✅ After 1NF (Normalized Rows)
Move the repeating group into its own rows.

**Table: `employee_phones_1nf`**

| emp_id | emp_name | phone_number |
| :--- | :--- | :--- |
| 1 | Carol | 555-0101 |
| 1 | Carol | 555-0102 |
| 2 | Dave | 555-0199 |

* **Primary Key:** (`emp_id`, `phone_number`)

---

### 🦆 DuckDB Tip: Unpivoting Repeating Columns into 1NF
DuckDB provides an elegant `UNPIVOT` clause to solve this:

```sql
-- Create non-1NF table with repeating columns
CREATE TABLE employee_phones_bad (
    emp_id INT,
    emp_name VARCHAR,
    phone_1 VARCHAR,
    phone_2 VARCHAR,
    phone_3 VARCHAR
);

INSERT INTO employee_phones_bad VALUES 
(1, 'Carol', '555-0101', '555-0102', NULL),
(2, 'Dave', '555-0199', NULL, NULL);

-- Unpivot into 1NF (automatically drops NULLs)
CREATE TABLE employee_phones_1nf AS
UNPIVOT employee_phones_bad
ON phone_1, phone_2, phone_3
INTO
    NAME phone_type
    VALUE phone_number;

-- View 1NF table
SELECT emp_id, emp_name, phone_number 
FROM employee_phones_1nf 
WHERE phone_number IS NOT NULL;
```

---

## 4. Example 3: Handling DuckDB Complex Types (`LIST` & `STRUCT`)

DuckDB supports native array/list data types (`VARCHAR[]`). While useful for temporary analytical queries, storing lists directly inside columns breaks traditional 1NF rules.

### ❌ Non-1NF DuckDB List Type

```sql
CREATE TABLE orders_bad (
    order_id INT,
    customer VARCHAR,
    items VARCHAR[] -- List/Array type
);

INSERT INTO orders_bad VALUES 
(501, 'Eve', ['Laptop', 'Mouse', 'Keyboard']),
(502, 'Frank', ['Monitor']);
```

**Table Data:**

| order_id | customer | items |
| :--- | :--- | :--- |
| 501 | Eve | ['Laptop', 'Mouse', 'Keyboard'] |
| 502 | Frank | ['Monitor'] |

---

### ✅ 1NF Table Structure

```sql
CREATE TABLE orders_1nf AS
SELECT 
    order_id, 
    customer, 
    UNNEST(items) AS item_name
FROM orders_bad;
```

**Table Data:**

| order_id | customer | item_name |
| :--- | :--- | :--- |
| 501 | Eve | Laptop |
| 501 | Eve | Mouse |
| 501 | Eve | Keyboard |
| 502 | Frank | Monitor |

---

## 5. Summary Checklist for 1NF

Before moving to 2NF or 3NF, check your tables against this checklist:

| Rule | Questions to Ask | Fix |
| :--- | :--- | :--- |
| **1. Atomic Values** | Are there comma-separated lists or JSON arrays in any cell? | Split items into individual rows using `UNNEST()`. |
| **2. No Repeating Groups** | Do you have columns like `tag1`, `tag2`, `tag3`? | Convert columns to rows using `UNPIVOT`. |
| **3. Unique Columns** | Does every column have a clear, unique name? | Rename duplicate column headers. |
| **4. Primary Key** | Does every row have a unique identifier? | Add an ID column or composite key. |

## 6. References

[1. First Normal Form (1NF) - www.geeksforgeeks.org](https://www.geeksforgeeks.org/dbms/first-normal-form-1nf/)

[2. First Normal Form (1NF) - www.upgrad.com](https://www.upgrad.com/tutorials/software-engineering/dbms-tutorial/first-normal-form-1nf/)