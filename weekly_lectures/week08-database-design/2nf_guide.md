# Understanding Second Normal Form (2NF) <br> in SQL & DuckDB

Your tables are in **First Normal Form (1NF)**: every cell holds one value, there are
no repeating groups, and every table has a primary key
(see [`1nf_guide.md`](1nf_guide.md)). The next step is **Second Normal Form (2NF)**.

---

## 1. What is Second Normal Form (2NF)?

A table is in **Second Normal Form (2NF)** when:

1. **It is already in 1NF**, and
2. **no non-key column depends on only *part* of a composite primary key.**
   (A column that does is called a **partial dependency**.)

> 💡 **Important rule to remember:** <br>
> If the primary key is **a single column**, a 1NF table is **automatically in 2NF**. <br>
> 2NF problems happen **only** when the primary key is **composite** (made of two or more columns).

---

## 2. Functional Dependencies and Partial Dependencies

A **functional dependency** **A → B** means: *"If I know A, I know B."*
For example, `student_id → student_name`: one student ID always has one name.

With a composite key, a non-key column can depend on the key in two ways:

* **Full dependency (good):** `(student_id, course_id) → grade`.
  You need **both** the student and the course to know the grade.
* **Partial dependency (bad):** `(student_id, course_id) → student_name`.
  You only need `student_id` to know the name. `course_id` does not matter.

---

## 3. Example 1: Student Enrollments

### ❌ Before 2NF (has partial dependencies)

A table of student enrollments, with course details in every row:

* **Primary key:** composite key (`student_id`, `course_id`)

**Table: `enrollments_bad`**

| student_id | course_id | student_name | course_name | professor_name | grade |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 101 | CS101 | Alice | Intro to CS | Dr. Smith | A |
| 101 | MATH201 | Alice | Calculus | Dr. Jones | B |
| 102 | CS101 | Bob | Intro to CS | Dr. Smith | A |

(Here each course has one professor.)

> ❌ **Why is this NOT in 2NF?** <br>
> * `student_name` depends **only** on `student_id` — part of the key. <br>
> * `course_name` and `professor_name` depend **only** on `course_id` — part of the key. <br>
> * Only `grade` depends on **both** `student_id` and `course_id`.

**Problems this causes (anomalies):**

1. **Redundancy:** if 500 students take `CS101`, "Intro to CS" and "Dr. Smith" are stored 500 times.
2. **Update anomaly:** if CS101 gets a new professor, you must update **every** CS101 row.
   Miss one, and CS101 has two professors.
3. **Insert anomaly:** you cannot add a new course until a student enrolls in it —
   `student_id` is part of the key, and a key cannot be `NULL`.
4. **Delete anomaly:** if Bob drops CS101 and Alice drops it too, the fact
   "CS101 is Intro to CS, taught by Dr. Smith" disappears.

---

### ✅ After 2NF (split into three tables)

Split the table so that every non-key column depends on the **whole** key of its table.
Rule of thumb: **move each partial dependency to the table where that part is the key.**

#### 1. `students` (key: `student_id`)

| student_id | student_name |
| :--- | :--- |
| 101 | Alice |
| 102 | Bob |

#### 2. `courses` (key: `course_id`)

| course_id | course_name | professor_name |
| :--- | :--- | :--- |
| CS101 | Intro to CS | Dr. Smith |
| MATH201 | Calculus | Dr. Jones |

#### 3. `enrollments` (composite key: `student_id`, `course_id`)

| student_id | course_id | grade |
| :--- | :--- | :--- |
| 101 | CS101 | A |
| 101 | MATH201 | B |
| 102 | CS101 | A |

`students` and `courses` have single-column keys, so they are in 2NF automatically.
In `enrollments`, the only non-key column, `grade`, depends on the whole key.

---

### 🦆 DuckDB Code: Converting to 2NF

```sql
-- Step 1: Set up the non-2NF table
CREATE OR REPLACE TABLE enrollments_bad (
    student_id     INT,
    course_id      VARCHAR,
    student_name   VARCHAR,
    course_name    VARCHAR,
    professor_name VARCHAR,
    grade          VARCHAR
);

INSERT INTO enrollments_bad VALUES
(101, 'CS101',   'Alice', 'Intro to CS', 'Dr. Smith', 'A'),
(101, 'MATH201', 'Alice', 'Calculus',    'Dr. Jones', 'B'),
(102, 'CS101',   'Bob',   'Intro to CS', 'Dr. Smith', 'A');

-- Step 2: Check a dependency with SQL.
-- Does student_id → student_name hold? Look for a student with 2+ names.
SELECT student_id, COUNT(DISTINCT student_name) AS names
FROM enrollments_bad
GROUP BY student_id
HAVING COUNT(DISTINCT student_name) > 1;
-- 0 rows → no student has two names in this data

-- Step 3: Build the 2NF tables. DISTINCT keeps one copy of each repeated fact.
CREATE OR REPLACE TABLE students AS
SELECT DISTINCT student_id, student_name
FROM enrollments_bad;                          -- 2 rows

CREATE OR REPLACE TABLE courses AS
SELECT DISTINCT course_id, course_name, professor_name
FROM enrollments_bad;                          -- 2 rows

CREATE OR REPLACE TABLE enrollments AS
SELECT student_id, course_id, grade
FROM enrollments_bad;                          -- 3 rows

-- Step 4: JOIN the tables back together. We get the same 3 rows: nothing was lost.
SELECT
    s.student_name,
    c.course_name,
    c.professor_name,
    e.grade
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses  c ON e.course_id  = c.course_id
ORDER BY s.student_name, c.course_name;
```

> **Why the check in Step 2 matters:** a dependency is a **business rule**
> ("each student has one name"). The data cannot prove the rule, but it **can**
> show that it is broken. If Step 2 returned a row, `SELECT DISTINCT` in Step 3
> would give that student two rows in `students`, and `student_id` would no
> longer be a key.

---

## 4. Example 2: E-Commerce Order Items

### ❌ Before 2NF (has partial dependencies)

Each row is one product in one order.

* **Primary key:** composite key (`order_id`, `product_id`)

**Table: `order_items_bad`**

| order_id | product_id | product_name | unit_price | quantity | store_location |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 5001 | P10 | Wireless Mouse | 25.00 | 2 | NY Warehouse |
| 5001 | P20 | Mechanical Keyboard | 80.00 | 1 | NY Warehouse |
| 5002 | P10 | Wireless Mouse | 25.00 | 5 | CA Warehouse |

> ❌ **Why is this NOT in 2NF?** <br>
> * `product_name` and `unit_price` depend **only** on `product_id` (not on `order_id`). <br>
> * `store_location` depends **only** on `order_id` (not on `product_id`). <br>
> * Only `quantity` depends on **both** `order_id` and `product_id`.

---

### ✅ After 2NF

#### 1. `orders` (key: `order_id`)

| order_id | store_location |
| :--- | :--- |
| 5001 | NY Warehouse |
| 5002 | CA Warehouse |

#### 2. `products` (key: `product_id`)

| product_id | product_name | unit_price |
| :--- | :--- | :--- |
| P10 | Wireless Mouse | 25.00 |
| P20 | Mechanical Keyboard | 80.00 |

#### 3. `order_items` (composite key: `order_id`, `product_id`)

| order_id | product_id | quantity |
| :--- | :--- | :--- |
| 5001 | P10 | 2 |
| 5001 | P20 | 1 |
| 5002 | P10 | 5 |

> **A real-world note:** here we assume a product's price never changes. Real
> stores often **also** keep the price in `order_items`, because prices change
> and an old order must remember the price the customer paid. Then the column
> means "price **at the time of the order**", which depends on the whole key.

---

### 🦆 DuckDB Code: Normalizing Order Items

```sql
-- Create the non-2NF table
CREATE OR REPLACE TABLE order_items_bad (
    order_id       INT,
    product_id     VARCHAR,
    product_name   VARCHAR,
    unit_price     DECIMAL(10,2),
    quantity       INT,
    store_location VARCHAR
);

INSERT INTO order_items_bad VALUES
(5001, 'P10', 'Wireless Mouse',      25.00, 2, 'NY Warehouse'),
(5001, 'P20', 'Mechanical Keyboard', 80.00, 1, 'NY Warehouse'),
(5002, 'P10', 'Wireless Mouse',      25.00, 5, 'CA Warehouse');

-- Split into 2NF tables
CREATE OR REPLACE TABLE orders AS
SELECT DISTINCT order_id, store_location
FROM order_items_bad;                          -- 2 rows

CREATE OR REPLACE TABLE products AS
SELECT DISTINCT product_id, product_name, unit_price
FROM order_items_bad;                          -- 2 rows

CREATE OR REPLACE TABLE order_items AS
SELECT order_id, product_id, quantity
FROM order_items_bad;                          -- 3 rows

-- The 2NF tables still answer business questions: revenue per order
SELECT oi.order_id, SUM(oi.quantity * p.unit_price) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY oi.order_id
ORDER BY oi.order_id;
-- 5001 → 130.00, 5002 → 125.00
```

---

## 5. Summary Checklist for 2NF

```
             ┌───────────────────────────────┐
             │     Is the table in 1NF?      │──► NO ──► Fix 1NF first
             └───────────────┬───────────────┘
                             │ YES
                             ▼
             ┌───────────────────────────────┐
             │ Is the primary key a single   │──► YES ──► ✅ The table is in 2NF
             │ column?                       │
             └───────────────┬───────────────┘
                             │ NO (it is composite)
                             ▼
             ┌───────────────────────────────┐
             │ Does any non-key column       │──► NO ───► ✅ The table is in 2NF
             │ depend on only PART of it?    │
             └───────────────┬───────────────┘
                             │ YES
                             ▼
              ❌ Not in 2NF: move those columns
                 to a table where that part is the key
```

Ask yourself three questions:

1. **Is the table in 1NF?** If not, fix 1NF first.
2. **Is the primary key composite (two or more columns)?** If it is a single column, the table is already in 2NF.
3. **Does every non-key column depend on the WHOLE key?** If a column needs only *part* of the key,
   move it to a separate table where that part is the key.

**Next:** Third Normal Form (3NF) removes columns that depend on **another non-key column**
(for example, `product_id → category_id → category_name`). See this week's slides.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
