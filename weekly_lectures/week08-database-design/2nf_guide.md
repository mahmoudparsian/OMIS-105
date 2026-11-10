# Understanding Second Normal Form (2NF) <br> in SQL & DuckDB

Now that your tables are in **First Normal Form (1NF)** (all values are atomic, and there is a primary key), it is time to move to **Second Normal Form (2NF)**.

---

## 1. What is Second Normal Form (2NF)?

A table is in **Second Normal Form (2NF)** if and only if:

1. **It is already in 1NF.**
2. **No non-key column depends on only *part* of a composite primary key.** (This rule is called eliminating **Partial Dependencies**).

> 💡 **Important Rule to Remember:**  
> If a table's primary key consists of **only a single column**, the table is **automatically in 2NF** (provided it is in 1NF)!  
> 2NF issues *only* happen when you have a **Composite Primary Key** (a key made up of 2 or more columns).

---

## 2. What is a Partial Dependency?

A **Partial Dependency** occurs when a column depends on *only one part* of a composite primary key rather than the *entire* key.

* **Full Dependency (Good):** `(student_id, course_id)` $\rightarrow$ `grade`. You need both student and course to know the grade.
* **Partial Dependency (Bad):** `(student_id, course_id)` $\rightarrow$ `student_name`. You only need `student_id` to know the student's name; `course_id` is completely irrelevant!

---

## 3. Example 1: Student Enrollment System

### ❌ Before 2NF (Contains Partial Dependencies)

Consider a table tracking student course enrollments and professor details:

* **Primary Key:** Composite Key (`student_id`, `course_id`)

**Table: `enrollments_bad`**

| student_id | course_id | student_name | course_name | professor_name | grade |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 101 | CS101 | Alice | Intro to CS | Dr. Smith | A |
| 101 | MATH201 | Alice | Calculus | Dr. Jones | B |
| 102 | CS101 | Bob | Intro to CS | Dr. Smith | A |

> ❌ **Why is this NOT in 2NF?**
> * `student_name` depends **only** on `student_id` (part of the composite key).
> * `course_name` and `professor_name` depend **only** on `course_id` (part of the composite key).
> * Only `grade` depends on **both** `student_id` and `course_id`.

**Problems caused by this structure:**

1. **Redundancy:** If 500 students take `CS101`, "Intro to CS" and "Dr. Smith" are repeated 500 times.

2. **Update Anomaly:** If Dr. Smith changes names, you must update multiple rows.

---

### ✅ After 2NF (Splitting into Normalized Tables)

We break the single table into **three distinct tables** so every non-key column depends on its table's full primary key.

#### 1. `students` Table (Key: `student_id`)
| student_id | student_name |
| :--- | :--- |
| 101 | Alice |
| 102 | Bob |

#### 2. `courses` Table (Key: `course_id`)
| course_id | course_name | professor_name |
| :--- | :--- | :--- |
| CS101 | Intro to CS | Dr. Smith |
| MATH201 | Calculus | Dr. Jones |

#### 3. `enrollments` Table (Composite Key: `student_id`, `course_id`)
| student_id | course_id | grade |
| :--- | :--- | :--- |
| 101 | CS101 | A |
| 101 | MATH201 | B |
| 102 | CS101 | A |

---

### 🦆 DuckDB Code: Converting to 2NF

```sql
-- Step 1: Setup the messy non-2NF table
CREATE TABLE enrollments_bad (
    student_id INT,
    course_id VARCHAR,
    student_name VARCHAR,
    course_name VARCHAR,
    professor_name VARCHAR,
    grade VARCHAR
);

INSERT INTO enrollments_bad VALUES
(101, 'CS101', 'Alice', 'Intro to CS', 'Dr. Smith', 'A'),
(101, 'MATH201', 'Alice', 'Calculus', 'Dr. Jones', 'B'),
(102, 'CS101', 'Bob', 'Intro to CS', 'Dr. Smith', 'A');

-- Step 2: Extract normalized 2NF tables using DuckDB DISTINCT
CREATE TABLE students AS 
SELECT DISTINCT student_id, student_name 
FROM enrollments_bad;

CREATE TABLE courses AS 
SELECT DISTINCT course_id, course_name, professor_name 
FROM enrollments_bad;

CREATE TABLE enrollments AS 
SELECT student_id, course_id, grade 
FROM enrollments_bad;

-- Step 3: Query using JOIN to verify data integrity
SELECT 
    s.student_name,
    c.course_name,
    c.professor_name,
    e.grade
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id;
```

---

## 4. Example 2: E-Commerce Order Items

### ❌ Before 2NF (Contains Partial Dependencies)

Here, we record item line details inside orders.

* **Primary Key:** Composite Key (`order_id`, `product_id`)

**Table: `order_items_bad`**

| order_id | product_id | product_name | unit_price | quantity | store_location |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 5001 | P10 | Wireless Mouse | 25.00 | 2 | NY Warehouse |
| 5001 | P20 | Mechanical Keyboard | 80.00 | 1 | NY Warehouse |
| 5002 | P10 | Wireless Mouse | 25.00 | 5 | CA Warehouse |

> ❌ **Why is this NOT in 2NF?**
> * `product_name` and `unit_price` depend **only** on `product_id` (not `order_id`).
> * `store_location` depends **only** on `order_id` (not `product_id`).
> * Only `quantity` depends on **both** `order_id` AND `product_id`.

---

### ✅ After 2NF

#### 1. `orders` Table (Key: `order_id`)
| order_id | store_location |
| :--- | :--- |
| 5001 | NY Warehouse |
| 5002 | CA Warehouse |

#### 2. `products` Table (Key: `product_id`)
| product_id | product_name | unit_price |
| :--- | :--- | :--- |
| P10 | Wireless Mouse | 25.00 |
| P20 | Mechanical Keyboard | 80.00 |

#### 3. `order_items` Table (Composite Key: `order_id`, `product_id`)
| order_id | product_id | quantity |
| :--- | :--- | :--- |
| 5001 | P10 | 2 |
| 5001 | P20 | 1 |
| 5002 | P10 | 5 |

---

### 🦆 DuckDB Code: Normalizing Order Items

```sql
-- Create non-2NF table
CREATE TABLE order_items_bad (
    order_id INT,
    product_id VARCHAR,
    product_name VARCHAR,
    unit_price DECIMAL(10,2),
    quantity INT,
    store_location VARCHAR
);

INSERT INTO order_items_bad VALUES
(5001, 'P10', 'Wireless Mouse', 25.00, 2, 'NY Warehouse'),
(5001, 'P20', 'Mechanical Keyboard', 80.00, 1, 'NY Warehouse'),
(5002, 'P10', 'Wireless Mouse', 25.00, 5, 'CA Warehouse');

-- Separate into 2NF tables
CREATE TABLE orders AS 
SELECT DISTINCT order_id, store_location 
FROM order_items_bad;

CREATE TABLE products AS 
SELECT DISTINCT product_id, product_name, unit_price 
FROM order_items_bad;

CREATE TABLE order_items AS 
SELECT order_id, product_id, quantity 
FROM order_items_bad;
```

---

## 5. Summary Checklist for 2NF

To check if a table is in 2NF, ask your students these three questions:

```
                  ┌──────────────────────────────┐
                  │      Is the table in 1NF?    │
                  └──────────────┬───────────────┘
                                 │ YES
                                 ▼
              ┌─────────────────────────────────────┐
              │ Is Primary Key a single column?     │───► YES ───► [ ✅ Table is in 2NF! ]
              └──────────────────┬──────────────────┘
                                 │ NO (It is Composite)
                                 ▼
    ┌─────────────────────────────────────────────────────────┐
    │ Does any attribute depend on ONLY PART of the key?     │
    └────────────────────────────┬────────────────────────────┘
                                 │
                     ┌───────────┴───────────┐
                     ▼                       ▼
                  [ YES ]                 [ NO ]
                     │                       │
                     ▼                       ▼
         ❌ Violates 2NF!            ✅ Table is in 2NF!
    (Split into multiple tables)
```

1. **Is the table in 1NF?** If not, fix 1NF first.
2. **Is the primary key composite (multiple columns)?** If the primary key is a single column, the table is automatically in 2NF!
3. **Does every non-key column depend on the FULL composite key?** If a column only needs *part* of the key, extract it into a separate table.