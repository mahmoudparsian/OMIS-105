# Second Normal Form (2NF) — Examples

A table is in **Second Normal Form (2NF)** when:

1. **It is in 1NF** (one value per cell, no repeating groups, a primary key), and
2. **every non-key column depends on the *whole* primary key**, not on just part of it.

A column that depends on only part of the key is a **partial dependency**.
Partial dependencies can happen **only** when the key is **composite**
(two or more columns). A 1NF table with a one-column key is always in 2NF.

This page shows four small examples. The full explanation, and the DuckDB code
for checking a dependency and splitting a table, is in [`2nf_guide.md`](2nf_guide.md).

**The 2NF question, for every non-key column:**
👉 *"Do I need the **whole** key to know this value, or only **part** of it?"*

---

## Example 1: Employees on Projects

### ❌ Before: not in 2NF

A company records how many hours each employee works on each project:

* **Primary key:** (`emp_id`, `project_id`)

| `emp_id` | `project_id` | `emp_name` | `project_name` | `budget` | `hours` |
|---|---|---|---|---|---|
| E1 | P10 | Ana | Website | 50000 | 12 |
| E1 | P20 | Ana | Mobile App | 80000 | 30 |
| E2 | P10 | Ben | Website | 50000 | 25 |
| E3 | P20 | Cara | Mobile App | 80000 | 8 |

**The dependencies:**

* `emp_id → emp_name` — **partial** (only part of the key)
* `project_id → project_name, budget` — **partial** (only part of the key)
* `(emp_id, project_id) → hours` — **full**: hours belong to one employee
  on one project

**Why it breaks 2NF:** "Website" and its budget are stored once for every
employee on the project. If the Website budget changes, every Website row
must change.

### ✅ After: in 2NF

**Table 1: `employees`** — primary key `emp_id`

| `emp_id` | `emp_name` |
|---|---|
| E1 | Ana |
| E2 | Ben |
| E3 | Cara |

**Table 2: `projects`** — primary key `project_id`

| `project_id` | `project_name` | `budget` |
|---|---|---|
| P10 | Website | 50000 |
| P20 | Mobile App | 80000 |

**Table 3: `assignments`** — primary key (`emp_id`, `project_id`);
both columns are foreign keys

| `emp_id` | `project_id` | `hours` |
|---|---|---|
| E1 | P10 | 12 |
| E1 | P20 | 30 |
| E2 | P10 | 25 |
| E3 | P20 | 8 |

### 🦆 Check it with DuckDB

```sql
CREATE OR REPLACE TABLE work_bad (
    emp_id       VARCHAR,
    project_id   VARCHAR,
    emp_name     VARCHAR,
    project_name VARCHAR,
    budget       INT,
    hours        INT
);

INSERT INTO work_bad VALUES
('E1', 'P10', 'Ana',  'Website',    50000, 12),
('E1', 'P20', 'Ana',  'Mobile App', 80000, 30),
('E2', 'P10', 'Ben',  'Website',    50000, 25),
('E3', 'P20', 'Cara', 'Mobile App', 80000,  8);

-- How many times is each project's budget stored?
SELECT project_id, COUNT(*) AS copies_of_budget
FROM work_bad
GROUP BY project_id
ORDER BY project_id;
-- P10 → 2, P20 → 2

-- The 2NF tables
CREATE OR REPLACE TABLE employees AS
SELECT DISTINCT emp_id, emp_name FROM work_bad;                    -- 3 rows

CREATE OR REPLACE TABLE projects AS
SELECT DISTINCT project_id, project_name, budget FROM work_bad;    -- 2 rows

CREATE OR REPLACE TABLE assignments AS
SELECT emp_id, project_id, hours FROM work_bad;                    -- 4 rows

-- Total hours per project, from the 2NF tables
SELECT p.project_name, SUM(a.hours) AS total_hours
FROM assignments a
JOIN projects p ON a.project_id = p.project_id
GROUP BY p.project_name
ORDER BY p.project_name;
-- Mobile App → 38, Website → 37
```

---

## Example 2: Store Inventory

### ❌ Before: not in 2NF

A chain of stores records how many units of each product each store has:

* **Primary key:** (`store_id`, `product_id`)

| `store_id` | `product_id` | `store_city` | `product_name` | `units_in_stock` |
|---|---|---|---|---|
| S1 | 101 | San Jose | Water Bottle | 40 |
| S1 | 102 | San Jose | Backpack | 15 |
| S2 | 101 | Oakland | Water Bottle | 22 |
| S2 | 103 | Oakland | Notebook | 60 |

**The dependencies:**

* `store_id → store_city` — **partial**
* `product_id → product_name` — **partial**
* `(store_id, product_id) → units_in_stock` — **full**: the stock count is for
  one product in one store

### ✅ After: in 2NF

**`stores`**(`store_id`, `store_city`) ·
**`products`**(`product_id`, `product_name`) ·
**`inventory`**(`store_id`, `product_id`, `units_in_stock`)

| `store_id` | `store_city` |
|---|---|
| S1 | San Jose |
| S2 | Oakland |

| `product_id` | `product_name` |
|---|---|
| 101 | Water Bottle |
| 102 | Backpack |
| 103 | Notebook |

| `store_id` | `product_id` | `units_in_stock` |
|---|---|---|
| S1 | 101 | 40 |
| S1 | 102 | 15 |
| S2 | 101 | 22 |
| S2 | 103 | 60 |

**A new benefit:** we can now add a product that no store carries yet
(insert it into `products`). Before the split, we could not: the key
needs a `store_id`, and a key cannot be `NULL`.

---

## Example 3: Only One Side Is Partial (Course Sections)

Sometimes only **one** part of the key causes the problem.

### ❌ Before: not in 2NF

A university lists which instructor teaches each course in each term:

* **Primary key:** (`course_id`, `term`)

| `course_id` | `term` | `course_title` | `credits` | `instructor` |
|---|---|---|---|---|
| OMIS105 | Fall 2026 | Intro to DBMS | 4 | Dr. Lee |
| OMIS105 | Winter 2027 | Intro to DBMS | 4 | Dr. Kim |
| OMIS30 | Fall 2026 | Intro to Programming | 4 | Dr. Diaz |

**The dependencies:**

* `course_id → course_title, credits` — **partial**
* `(course_id, term) → instructor` — **full**: the instructor can change
  from term to term
* Nothing depends on `term` alone.

### ✅ After: in 2NF — two tables, not three

**Table 1: `courses`** — primary key `course_id`

| `course_id` | `course_title` | `credits` |
|---|---|---|
| OMIS105 | Intro to DBMS | 4 |
| OMIS30 | Intro to Programming | 4 |

**Table 2: `sections`** — primary key (`course_id`, `term`)

| `course_id` | `term` | `instructor` |
|---|---|---|
| OMIS105 | Fall 2026 | Dr. Lee |
| OMIS105 | Winter 2027 | Dr. Kim |
| OMIS30 | Fall 2026 | Dr. Diaz |

We do **not** need a `terms` table: no column depends on `term` alone.
Split only where a partial dependency exists.

---

## Example 4: Is It in 2NF? (Three Quick Cases)

### Case A: a composite key, and every column needs the whole key

**`exam_scores`** — primary key (`student_id`, `exam_id`)

| `student_id` | `exam_id` | `score` |
|---|---|---|
| 101 | MID | 88 |
| 101 | FINAL | 92 |
| 102 | MID | 75 |

✅ **In 2NF.** The only non-key column, `score`, needs both the student
and the exam.

### Case B: a one-column key

**`orders`** — primary key `order_id`

| `order_id` | `customer_id` | `customer_name` | `order_date` |
|---|---|---|---|
| 1 | C1 | Alice | 2026-11-02 |
| 2 | C1 | Alice | 2026-11-05 |
| 3 | C2 | Bob | 2026-11-05 |

✅ **In 2NF** — the key has one column, so no column can depend on "part" of it.
But Alice's name is still repeated! That is a **3NF** problem:
`order_id → customer_id → customer_name`. See [`3nf_guide.md`](3nf_guide.md).

### Case C: a composite key with a partial dependency

**`order_lines`** — primary key (`order_id`, `line_no`)

| `order_id` | `line_no` | `order_date` | `product` | `quantity` |
|---|---|---|---|---|
| 1 | 1 | 2026-11-02 | Pen | 3 |
| 1 | 2 | 2026-11-02 | Paper | 1 |
| 2 | 1 | 2026-11-05 | Pen | 10 |

❌ **Not in 2NF.** `order_date` depends on `order_id` alone.
Fix: move `order_date` to an `orders`(`order_id`, `order_date`) table.

---

## Quick Self-Check

For each table you design, ask:

1. Is it in 1NF? → if not, fix 1NF first ([`1nf_guide.md`](1nf_guide.md)).
2. Is the primary key composite? → if it has one column, the table is in 2NF.
3. For each non-key column: does it need the **whole** key? → if it needs only
   part, move it to a table where that part is the key.

**Next:** Third Normal Form — [`3nf_guide.md`](3nf_guide.md) and
[`3nf_examples.md`](3nf_examples.md).

---

## Complete Example: From a Non-2NF Table to 2NF, Step by Step

This last example puts everything together: find the key, **prove** each
dependency with SQL, split the table, and prove that nothing was lost. Every
result below is real DuckDB output, so you can run the code and compare.

### The story

A one-day tech conference records who registered for which workshop. One
table holds everything.

### Step 1: Create the table

```sql
CREATE OR REPLACE TABLE registrations_bad (
    attendee_id    INT,
    workshop_id    VARCHAR,
    attendee_name  VARCHAR,
    company        VARCHAR,
    workshop_title VARCHAR,
    room           VARCHAR,
    fee_paid       DECIMAL(6,2)
);

INSERT INTO registrations_bad VALUES
(1, 'W1', 'Ana',  'Bay Tech',    'Intro to SQL',  'Room 101', 100.00),
(1, 'W2', 'Ana',  'Bay Tech',    'Data Viz',      'Room 205', 120.00),
(2, 'W1', 'Ben',  'Valley Bank', 'Intro to SQL',  'Room 101',  80.00),
(3, 'W1', 'Cara', 'Sun Foods',   'Intro to SQL',  'Room 101', 100.00),
(3, 'W3', 'Cara', 'Sun Foods',   'Python Basics', 'Room 101',  90.00);
```

| attendee_id | workshop_id | attendee_name | company | workshop_title | room | fee_paid |
|---|---|---|---|---|---|---|
| 1 | W1 | Ana | Bay Tech | Intro to SQL | Room 101 | 100.00 |
| 1 | W2 | Ana | Bay Tech | Data Viz | Room 205 | 120.00 |
| 2 | W1 | Ben | Valley Bank | Intro to SQL | Room 101 | 80.00 |
| 3 | W1 | Cara | Sun Foods | Intro to SQL | Room 101 | 100.00 |
| 3 | W3 | Cara | Sun Foods | Python Basics | Room 101 | 90.00 |

The table **is** in 1NF: one value per cell, no repeating columns.

### Step 2: Find the primary key

One row = one attendee in one workshop, so the key should be
(`attendee_id`, `workshop_id`). Check that no pair appears twice:

```sql
SELECT attendee_id, workshop_id, COUNT(*) AS copies
FROM registrations_bad
GROUP BY attendee_id, workshop_id
HAVING COUNT(*) > 1;            -- 0 rows ✅ the pair is unique
```

The key is **composite** (two columns), so 2NF problems are possible.

### Step 3: Test each non-key column with SQL

For each column, ask: *"Is one part of the key enough to know it?"*
The test: group by that part. If no group has two different values, the part
determines the column.

```sql
-- Does attendee_id alone determine attendee_name and company?
SELECT attendee_id,
       COUNT(DISTINCT attendee_name) AS names,
       COUNT(DISTINCT company)       AS companies
FROM registrations_bad
GROUP BY attendee_id
HAVING COUNT(DISTINCT attendee_name) > 1 OR COUNT(DISTINCT company) > 1;
-- 0 rows → YES: attendee_id → attendee_name, company   (partial ❌)

-- Does workshop_id alone determine workshop_title and room?
SELECT workshop_id,
       COUNT(DISTINCT workshop_title) AS titles,
       COUNT(DISTINCT room)           AS rooms
FROM registrations_bad
GROUP BY workshop_id
HAVING COUNT(DISTINCT workshop_title) > 1 OR COUNT(DISTINCT room) > 1;
-- 0 rows → YES: workshop_id → workshop_title, room     (partial ❌)

-- Does workshop_id alone determine fee_paid?
SELECT workshop_id, COUNT(DISTINCT fee_paid) AS fees
FROM registrations_bad
GROUP BY workshop_id
HAVING COUNT(DISTINCT fee_paid) > 1;
```

| workshop_id | fees |
|---|---|
| W1 | 2 |

**NO** — W1 has two different fees (Ben paid 80.00 with a discount). The fee
needs **both** the attendee and the workshop: `fee_paid` is a **full**
dependency ✅. It stays with the key.

> Remember: the data can show that a dependency is **broken** (the last query),
> but it cannot prove that a dependency always holds. The first two results
> agree with the business rules ("an attendee has one name and company",
> "a workshop has one title and room").

### Step 4: Plan the 2NF tables

| Dependency | Kind | Table |
|---|---|---|
| `attendee_id → attendee_name, company` | partial | `attendees`(**attendee_id**, attendee_name, company) |
| `workshop_id → workshop_title, room` | partial | `workshops`(**workshop_id**, workshop_title, room) |
| `(attendee_id, workshop_id) → fee_paid` | full | `registrations`(**attendee_id, workshop_id**, fee_paid) |

### Step 5: Create the tables with keys, then fill them

This time we write the `PRIMARY KEY` and `REFERENCES` (foreign key) rules into
`CREATE TABLE`, so DuckDB **enforces** the design. Then `INSERT … SELECT
DISTINCT` copies each fact **once** from the bad table.

```sql
CREATE OR REPLACE TABLE attendees (
    attendee_id   INT PRIMARY KEY,
    attendee_name VARCHAR,
    company       VARCHAR
);
INSERT INTO attendees
SELECT DISTINCT attendee_id, attendee_name, company
FROM registrations_bad;                       -- 3 rows

CREATE OR REPLACE TABLE workshops (
    workshop_id    VARCHAR PRIMARY KEY,
    workshop_title VARCHAR,
    room           VARCHAR
);
INSERT INTO workshops
SELECT DISTINCT workshop_id, workshop_title, room
FROM registrations_bad;                       -- 3 rows

CREATE OR REPLACE TABLE registrations (
    attendee_id INT     REFERENCES attendees(attendee_id),
    workshop_id VARCHAR REFERENCES workshops(workshop_id),
    fee_paid    DECIMAL(6,2),
    PRIMARY KEY (attendee_id, workshop_id)
);
INSERT INTO registrations
SELECT attendee_id, workshop_id, fee_paid
FROM registrations_bad;                       -- 5 rows
```

> If Step 3 had been wrong — say, Ana had two different companies —
> `SELECT DISTINCT` would produce two rows for attendee 1, and the
> `PRIMARY KEY` would **reject** the `INSERT`. The key protects the design.

**`attendees`**

| attendee_id | attendee_name | company |
|---|---|---|
| 1 | Ana | Bay Tech |
| 2 | Ben | Valley Bank |
| 3 | Cara | Sun Foods |

**`workshops`**

| workshop_id | workshop_title | room |
|---|---|---|
| W1 | Intro to SQL | Room 101 |
| W2 | Data Viz | Room 205 |
| W3 | Python Basics | Room 101 |

**`registrations`**

| attendee_id | workshop_id | fee_paid |
|---|---|---|
| 1 | W1 | 100.00 |
| 1 | W2 | 120.00 |
| 2 | W1 | 80.00 |
| 3 | W1 | 100.00 |
| 3 | W3 | 90.00 |

### Step 6: Prove that nothing was lost

JOIN the three tables back together, and subtract the original table with
`EXCEPT`. If the result is empty, the JOIN rebuilt **exactly** the old rows.

```sql
SELECT r.attendee_id, r.workshop_id, a.attendee_name, a.company,
       w.workshop_title, w.room, r.fee_paid
FROM registrations r
JOIN attendees a ON r.attendee_id = a.attendee_id
JOIN workshops w ON r.workshop_id = w.workshop_id
EXCEPT
SELECT * FROM registrations_bad;
-- 0 rows ✅ (and the JOIN returns 5 rows, the same as the original)
```

### Step 7: Enjoy the benefit

"Intro to SQL" moves to Room 300. In the old table, that was 3 rows to change.
Now it is **one** row:

```sql
UPDATE workshops SET room = 'Room 300' WHERE workshop_id = 'W1';   -- 1 row

SELECT w.workshop_title, w.room,
       COUNT(*)        AS attendees,
       SUM(r.fee_paid) AS fees
FROM registrations r
JOIN workshops w ON r.workshop_id = w.workshop_id
GROUP BY w.workshop_title, w.room
ORDER BY w.workshop_title;
```

| workshop_title | room | attendees | fees |
|---|---|---|---|
| Data Viz | Room 205 | 1 | 120.00 |
| Intro to SQL | Room 300 | 3 | 280.00 |
| Python Basics | Room 101 | 1 | 90.00 |

All three Intro to SQL attendees see the new room through the JOIN.

### What we did

1. Found the key, and checked it is unique (`GROUP BY … HAVING COUNT(*) > 1`).
2. Tested every non-key column: does **part** of the key determine it?
   (`GROUP BY part … HAVING COUNT(DISTINCT column) > 1`)
3. Moved each partial dependency to a table where that part is the key.
4. Kept the full dependency (`fee_paid`) with the whole key.
5. Proved the split is lossless with `JOIN … EXCEPT`.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
