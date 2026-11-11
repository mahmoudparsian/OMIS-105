# Understanding Third Normal Form (3NF) <br> in SQL & DuckDB

Your tables are in **Second Normal Form (2NF)**: they are in 1NF, and every
non-key column depends on the **whole** primary key
(see [`2nf_guide.md`](2nf_guide.md)). The last step this week is
**Third Normal Form (3NF)**.

For more small examples, see [`3nf_examples.md`](3nf_examples.md).

---

## 1. What is Third Normal Form (3NF)?

A table is in **Third Normal Form (3NF)** when:

1. **It is already in 2NF**, and
2. **no non-key column depends on another non-key column.**
   (A column that does is called a **transitive dependency**.)

> 💡 **Important rule to remember:** <br>
> Every non-key column must depend on **the key, the whole key, and nothing but the key.** <br>
> * "the key" → 1NF (there is a key) <br>
> * "the whole key" → 2NF (no partial dependencies) <br>
> * "nothing but the key" → 3NF (no transitive dependencies)

2NF problems need a composite key. **3NF problems can happen with any key** —
even a one-column key like `order_id`.

---

## 2. Transitive Dependencies

A **functional dependency** **A → B** means: *"If I know A, I know B."*

A **transitive dependency** is a chain of two dependencies:

```
order_id  →  customer_id  →  customer_city
  (key)       (non-key)        (non-key)
```

* `order_id → customer_id`: each order has one customer. ✅ Fine.
* `customer_id → customer_city`: each customer lives in one city.
* So `order_id → customer_city` holds too — but only **through** `customer_id`.

`customer_city` is a fact about the **customer**, not about the order.
It belongs in a `customers` table.

> **Quick test:** cover the key with your hand. If you can still tell a column's
> value from **another non-key column**, that column has a transitive dependency.

---

## 3. Example 1: Orders with Customer Details

### ❌ Before 3NF (has transitive dependencies)

* **Primary key:** `order_id` (one column — so the table is already in 2NF)

**Table: `orders_bad`**

| order_id | order_date | customer_id | customer_name | customer_city |
| :--- | :--- | :--- | :--- | :--- |
| 1001 | 2026-11-02 | C1 | Alice | San Jose |
| 1002 | 2026-11-03 | C2 | Bob | Oakland |
| 1003 | 2026-11-05 | C1 | Alice | San Jose |
| 1004 | 2026-11-06 | C1 | Alice | San Jose |

> ❌ **Why is this NOT in 3NF?** <br>
> * `order_date` and `customer_id` depend directly on `order_id`. ✅ <br>
> * `customer_name` and `customer_city` depend on `customer_id` — a **non-key** column. <br>
> * The chain: `order_id → customer_id → customer_name, customer_city`.

**Problems this causes (anomalies):**

1. **Redundancy:** Alice's name and city are stored 3 times, once per order.
2. **Update anomaly:** if Alice moves to Palo Alto, you must update **every** one
   of her orders. Miss one, and Alice lives in two cities.
3. **Insert anomaly:** you cannot add a new customer until they place an order —
   `order_id` is the key, and a key cannot be `NULL`.
4. **Delete anomaly:** if you delete Bob's only order (1002), you lose the fact
   that Bob lives in Oakland.

---

### ✅ After 3NF (split into two tables)

Move the columns that depend on `customer_id` into a table where
`customer_id` **is** the key. Keep `customer_id` in `orders` as a **foreign key**.

#### 1. `customers` (key: `customer_id`)

| customer_id | customer_name | customer_city |
| :--- | :--- | :--- |
| C1 | Alice | San Jose |
| C2 | Bob | Oakland |

#### 2. `orders` (key: `order_id`; `customer_id` is a foreign key)

| order_id | order_date | customer_id |
| :--- | :--- | :--- |
| 1001 | 2026-11-02 | C1 |
| 1002 | 2026-11-03 | C2 |
| 1003 | 2026-11-05 | C1 |
| 1004 | 2026-11-06 | C1 |

Now Alice's city is stored **once**. If she moves, you change **one** row.

---

### 🦆 DuckDB Code: Converting to 3NF

```sql
-- Step 1: Set up the non-3NF table
CREATE OR REPLACE TABLE orders_bad (
    order_id      INT,
    order_date    DATE,
    customer_id   VARCHAR,
    customer_name VARCHAR,
    customer_city VARCHAR
);

INSERT INTO orders_bad VALUES
(1001, DATE '2026-11-02', 'C1', 'Alice', 'San Jose'),
(1002, DATE '2026-11-03', 'C2', 'Bob',   'Oakland'),
(1003, DATE '2026-11-05', 'C1', 'Alice', 'San Jose'),
(1004, DATE '2026-11-06', 'C1', 'Alice', 'San Jose');

-- Step 2: Check the dependency customer_id → customer_city.
-- Look for a customer with 2+ cities.
SELECT customer_id, COUNT(DISTINCT customer_city) AS cities
FROM orders_bad
GROUP BY customer_id
HAVING COUNT(DISTINCT customer_city) > 1;
-- 0 rows → every customer has one city in this data

-- Step 3: Build the 3NF tables. DISTINCT keeps one copy of each customer.
CREATE OR REPLACE TABLE customers AS
SELECT DISTINCT customer_id, customer_name, customer_city
FROM orders_bad;                               -- 2 rows

CREATE OR REPLACE TABLE orders AS
SELECT order_id, order_date, customer_id
FROM orders_bad;                               -- 4 rows

-- Step 4: JOIN the tables back together. We get the same 4 rows: nothing was lost.
SELECT
    o.order_id,
    o.order_date,
    c.customer_name,
    c.customer_city
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_id;
```

---

### 🦆 See the Update Anomaly Happen

Run this on the **bad** table. We update Alice's city, but only in one row —
the kind of mistake that is easy to make:

```sql
UPDATE orders_bad
SET customer_city = 'Palo Alto'
WHERE order_id = 1004;

-- Where does Alice live now?
SELECT DISTINCT customer_name, customer_city
FROM orders_bad
WHERE customer_id = 'C1'
ORDER BY customer_city;
-- 2 rows: Alice | Palo Alto, and Alice | San Jose  ← the data contradicts itself
```

In the 3NF design, Alice's city lives in **one** row of `customers`, so this
contradiction cannot happen:

```sql
UPDATE customers
SET customer_city = 'Palo Alto'
WHERE customer_id = 'C1';
-- 1 row changed, and all 3 of Alice's orders now show Palo Alto through the JOIN
```

---

## 4. Example 2: Students and Advisors

### ❌ Before 3NF

* **Primary key:** `student_id`

**Table: `students_bad`**

| student_id | student_name | major | advisor_id | advisor_name | advisor_office |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 101 | Alice | Finance | A1 | Dr. Patel | Lucas 210 |
| 102 | Bob | Marketing | A2 | Dr. Chen | Lucas 118 |
| 103 | Cara | Finance | A1 | Dr. Patel | Lucas 210 |
| 104 | Dan | Analytics | A1 | Dr. Patel | Lucas 210 |

> ❌ **Why is this NOT in 3NF?** <br>
> * `student_name`, `major`, and `advisor_id` are facts about the **student**. ✅ <br>
> * `advisor_name` and `advisor_office` are facts about the **advisor**: <br>
>   `student_id → advisor_id → advisor_name, advisor_office`.

---

### ✅ After 3NF

#### 1. `advisors` (key: `advisor_id`)

| advisor_id | advisor_name | advisor_office |
| :--- | :--- | :--- |
| A1 | Dr. Patel | Lucas 210 |
| A2 | Dr. Chen | Lucas 118 |

#### 2. `students` (key: `student_id`; `advisor_id` is a foreign key)

| student_id | student_name | major | advisor_id |
| :--- | :--- | :--- | :--- |
| 101 | Alice | Finance | A1 |
| 102 | Bob | Marketing | A2 |
| 103 | Cara | Finance | A1 |
| 104 | Dan | Analytics | A1 |

---

### 🦆 DuckDB Code: Normalizing Students and Advisors

```sql
CREATE OR REPLACE TABLE students_bad (
    student_id     INT,
    student_name   VARCHAR,
    major          VARCHAR,
    advisor_id     VARCHAR,
    advisor_name   VARCHAR,
    advisor_office VARCHAR
);

INSERT INTO students_bad VALUES
(101, 'Alice', 'Finance',   'A1', 'Dr. Patel', 'Lucas 210'),
(102, 'Bob',   'Marketing', 'A2', 'Dr. Chen',  'Lucas 118'),
(103, 'Cara',  'Finance',   'A1', 'Dr. Patel', 'Lucas 210'),
(104, 'Dan',   'Analytics', 'A1', 'Dr. Patel', 'Lucas 210');

-- Split into 3NF tables
CREATE OR REPLACE TABLE advisors AS
SELECT DISTINCT advisor_id, advisor_name, advisor_office
FROM students_bad;                             -- 2 rows

CREATE OR REPLACE TABLE students AS
SELECT student_id, student_name, major, advisor_id
FROM students_bad;                             -- 4 rows

-- The 3NF tables still answer business questions: how many students per advisor?
SELECT a.advisor_name, a.advisor_office, COUNT(*) AS students
FROM students s
JOIN advisors a ON s.advisor_id = a.advisor_id
GROUP BY a.advisor_name, a.advisor_office
ORDER BY students DESC;
-- Dr. Patel | Lucas 210 | 3
-- Dr. Chen  | Lucas 118 | 1
```

> **Why is `major` not a problem?** Alice and Cara are both Finance majors, so
> "Finance" appears twice. But `major` is a fact about **each student**
> (`student_id → major`), and nothing else is determined by it here.
> Repeated **values** are fine; a repeated **fact** is the problem.
> (If each major had a department and a building, those would move to a
> `majors` table.)

---

## 5. Summary Checklist for 3NF

```
             ┌───────────────────────────────┐
             │     Is the table in 2NF?      │──► NO ──► Fix 1NF / 2NF first
             └───────────────┬───────────────┘
                             │ YES
                             ▼
             ┌───────────────────────────────┐
             │ Does any non-key column       │──► NO ───► ✅ The table is in 3NF
             │ depend on ANOTHER non-key     │
             │ column?                       │
             └───────────────┬───────────────┘
                             │ YES  (key → X → Y)
                             ▼
              ❌ Not in 3NF: move Y to a new table
                 where X is the key; keep X as a
                 foreign key in the old table
```

Ask yourself three questions:

1. **Is the table in 2NF?** If not, fix 1NF and 2NF first.
2. **For each non-key column, what does it describe?** The row's own "thing"
   (the order, the student)? Or some **other** thing (the customer, the advisor)?
3. **If it describes another thing,** move it to that thing's table, and link the
   two tables with a foreign key.

| Normal form | Removes | Ask |
| :--- | :--- | :--- |
| **1NF** | lists in cells, repeating columns | "One value per cell? Is there a key?" |
| **2NF** | partial dependencies | "Does it need the **whole** key?" |
| **3NF** | transitive dependencies | "Does it depend on **nothing but** the key?" |

**Going further:** **BCNF** (Boyce-Codd Normal Form) is a slightly stricter
version of 3NF. It matters only when a table has two overlapping candidate keys,
which is rare. It is **optional** in this course (not on the exams): see the
appendix at the end of [`database_design_and_normalization.md`](database_design_and_normalization.md).

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
