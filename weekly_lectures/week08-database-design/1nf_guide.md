# Understanding First Normal Form (1NF) <br> in SQL & DuckDB

Welcome! If you already know basic SQL queries like `SELECT`, `WHERE`, and `JOIN`,
you are ready to learn **database normalization**.

* **Normalization** is the process of organizing data in a database to
	* **reduce redundancy** (the same fact stored many times), and
	* **improve data integrity** (the data stays correct and consistent).
* The very first step in this process is **First Normal Form (1NF)**.

For more small examples, see [`1nf_examples.md`](1nf_examples.md).
The next step is [`2nf_guide.md`](2nf_guide.md).

---

## 1. What is First Normal Form (1NF)?

A table is in **First Normal Form (1NF)** when it follows these three rules:

1. **One value per cell (atomic values):** every cell holds a **single** value —
   no comma-separated lists, no arrays, no "several items in one box".
2. **No repeating groups:** no set of columns that store the same kind of data,
   such as `phone_1`, `phone_2`, `phone_3`.
3. **A primary key:** every row is unique. A **primary key** (one column, or a set
   of columns) identifies each row.

Two simple housekeeping rules come with them: every column has a **unique name**,
and all values in one column have the **same data type** (for example, all dates).

---

## 2. Example 1: Eliminating Multi-Value Strings (Comma-Separated Lists)

### ❌ Before 1NF (breaks Rule 1: values are not atomic)

Here, the `courses` column holds several values, separated by commas, in one cell.

**Table: `student_courses_bad`**

| student_id | student_name | courses |
| :--- | :--- | :--- |
| 101 | Alice | SQL, Python, DuckDB |
| 102 | Bob | Java, SQL |

> **Why is this bad?** <br>
> - `WHERE courses = 'SQL'` returns **0 rows**: no cell is exactly `'SQL'`. The values are `'SQL, Python, DuckDB'` and `'Java, SQL'`. <br>
> - `WHERE courses LIKE '%SQL%'` finds both students, but it would also match a course named `MySQL`. <br>
> - How do you count how many students take each course? <br>
> - How do you join this table with a `courses` table?

---

### ✅ After 1NF (atomic values and a primary key)

To fix this, each row must describe **one student taking one course**.

**Table: `student_courses_1nf`**

| student_id | student_name | course_name |
| :--- | :--- | :--- |
| 101 | Alice | SQL |
| 101 | Alice | Python |
| 101 | Alice | DuckDB |
| 102 | Bob | Java |
| 102 | Bob | SQL |

* **Primary key:** (`student_id`, `course_name`) — a **composite** primary key
  (a key made of two or more columns).
* Notice that `student_name` is now repeated (Alice appears 3 times). That is
  allowed in 1NF, but it is a new kind of redundancy. **Second Normal Form**
  fixes it — see [`2nf_guide.md`](2nf_guide.md).

---

### 🦆 DuckDB Tip: Convert a comma-separated list to 1NF with `STRING_SPLIT` and `UNNEST`

If you ever inherit messy data like the table above, DuckDB can split it for you.
`STRING_SPLIT` turns the text into a list, and `UNNEST` turns the list into rows.

```sql
-- Create the non-1NF sample table
CREATE OR REPLACE TABLE student_courses_bad AS
SELECT 101 AS student_id, 'Alice' AS student_name, 'SQL, Python, DuckDB' AS courses
UNION ALL
SELECT 102, 'Bob', 'Java, SQL';

-- Transform it into 1NF
CREATE OR REPLACE TABLE student_courses_1nf AS
SELECT
    student_id,
    student_name,
    UNNEST(STRING_SPLIT(courses, ', ')) AS course_name
FROM student_courses_bad;

-- View the 1NF result (5 rows)
SELECT * FROM student_courses_1nf;
```

> ⚠️ Split on `', '` (comma **and** space). If you split on `','` only, the values
> after the first one keep a leading space (`' Python'`), and
> `WHERE course_name = 'Python'` will not find them. `TRIM()` also fixes this.

---

## 3. Example 2: Eliminating Repeating Groups (Numbered Columns)

### ❌ Before 1NF (breaks Rule 2: repeating groups)

Sometimes people avoid comma-separated lists by adding numbered columns instead.
That is still not 1NF.

**Table: `employee_phones_bad`**

| emp_id | emp_name | phone_1 | phone_2 | phone_3 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Carol | 555-0101 | 555-0102 | NULL |
| 2 | Dave | 555-0199 | NULL | NULL |

> **Why is this bad?** <br>
> - What if an employee has 4 phone numbers? You must change the table (add `phone_4`). <br>
> - Searches become long: `WHERE phone_1 = '...' OR phone_2 = '...' OR phone_3 = '...'`. <br>
> - Many `NULL` values add clutter.

---

### ✅ After 1NF (one row per phone number)

Move the repeating group into rows.

**Table: `employee_phones_1nf`**

| emp_id | emp_name | phone_number |
| :--- | :--- | :--- |
| 1 | Carol | 555-0101 |
| 1 | Carol | 555-0102 |
| 2 | Dave | 555-0199 |

* **Primary key:** (`emp_id`, `phone_number`)

---

### 🦆 DuckDB Tip: Turn repeating columns into rows

**Way 1 — `UNION ALL` (works in every database).** Select each phone column
in turn, and skip the empty ones:

```sql
-- Create the non-1NF table with repeating columns
CREATE OR REPLACE TABLE employee_phones_bad (
    emp_id   INT,
    emp_name VARCHAR,
    phone_1  VARCHAR,
    phone_2  VARCHAR,
    phone_3  VARCHAR
);

INSERT INTO employee_phones_bad VALUES
(1, 'Carol', '555-0101', '555-0102', NULL),
(2, 'Dave',  '555-0199', NULL,       NULL);

-- One SELECT per phone column
CREATE OR REPLACE TABLE employee_phones_1nf AS
SELECT emp_id, emp_name, phone_1 AS phone_number FROM employee_phones_bad WHERE phone_1 IS NOT NULL
UNION ALL
SELECT emp_id, emp_name, phone_2 FROM employee_phones_bad WHERE phone_2 IS NOT NULL
UNION ALL
SELECT emp_id, emp_name, phone_3 FROM employee_phones_bad WHERE phone_3 IS NOT NULL;

-- View the 1NF table (3 rows)
SELECT * FROM employee_phones_1nf ORDER BY emp_id, phone_number;
```

**Way 2 — `UNPIVOT` (a DuckDB shortcut).** It does the same thing in one step,
and it drops the `NULL` values for you:

```sql
SELECT emp_id, emp_name, phone_number
FROM (
    UNPIVOT employee_phones_bad
    ON phone_1, phone_2, phone_3
    INTO
        NAME phone_type
        VALUE phone_number
)
ORDER BY emp_id, phone_number;
-- 3 rows: the NULL phones are gone
```

---

## 4. Example 3: DuckDB List Types (`VARCHAR[]`)

DuckDB has a **list** data type (`VARCHAR[]`, `INTEGER[]`, ...). Lists are useful
for quick analysis, but a list stored inside a column breaks Rule 1, just like a
comma-separated string.

### ❌ Not 1NF: a list column

```sql
CREATE OR REPLACE TABLE orders_bad (
    order_id INT,
    customer VARCHAR,
    items    VARCHAR[]   -- a list
);

INSERT INTO orders_bad VALUES
(501, 'Eve',   ['Laptop', 'Mouse', 'Keyboard']),
(502, 'Frank', ['Monitor']);
```

**Table data:**

| order_id | customer | items |
| :--- | :--- | :--- |
| 501 | Eve | [Laptop, Mouse, Keyboard] |
| 502 | Frank | [Monitor] |

---

### ✅ 1NF: one row per item

```sql
CREATE OR REPLACE TABLE orders_1nf AS
SELECT
    order_id,
    customer,
    UNNEST(items) AS item_name
FROM orders_bad;
```

**Table data:**

| order_id | customer | item_name |
| :--- | :--- | :--- |
| 501 | Eve | Laptop |
| 501 | Eve | Mouse |
| 501 | Eve | Keyboard |
| 502 | Frank | Monitor |

* **Primary key:** (`order_id`, `item_name`)

---

## 5. Summary Checklist for 1NF

Before you move on to 2NF and 3NF, check every table:

| Rule | Question to ask | Fix |
| :--- | :--- | :--- |
| **1. One value per cell** | Is there a comma-separated list or a list (`[...]`) in any cell? | Split it into rows: `UNNEST(STRING_SPLIT(...))` or `UNNEST(list)`. |
| **2. No repeating groups** | Are there columns like `tag_1`, `tag_2`, `tag_3`? | Turn the columns into rows: `UNION ALL` or `UNPIVOT`. |
| **3. A primary key** | Can every row be identified uniquely? | Choose a key column (or columns), or add an ID column. |
| Housekeeping | Does every column have a unique name and one data type? | Rename columns; fix mixed types. |

**Check a key with SQL:** if this query returns **0 rows**, the columns you chose
are unique in the current data:

```sql
SELECT student_id, course_name, COUNT(*) AS copies
FROM student_courses_1nf
GROUP BY student_id, course_name
HAVING COUNT(*) > 1;
```
---

## 6. References

1. [First Normal Form (1NF) — GeeksforGeeks](https://www.geeksforgeeks.org/dbms/first-normal-form-1nf/)
2. [First Normal Form (1NF) — upGrad](https://www.upgrad.com/tutorials/software-engineering/dbms-tutorial/first-normal-form-1nf/)

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
