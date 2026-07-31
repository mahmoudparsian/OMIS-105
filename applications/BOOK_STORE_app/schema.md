# University Bookstore — Database Schema
## OMIS-105: Introduction to DBMS

---

## Entity Overview

| Table | Type | Description |
|-------|------|-------------|
| `students` | Core entity | Buyers — demographic and academic info |
| `courses` | Core entity | Demand drivers — department, credits, semester |
| `books` | Core entity | Inventory — title, price, category |
| `purchases` | Fact / transaction | Every sale event, linking student + book + course |
| `course_books` | Junction | Resolves M:M between courses and books |

---

## DDL — Create Statements

### students

```sql
CREATE TABLE students (
    student_id   INTEGER       PRIMARY KEY,
    name         VARCHAR(100)  NOT NULL,
    email        VARCHAR(150)  UNIQUE NOT NULL,
    major        VARCHAR(80)   NOT NULL,
    year         INTEGER       NOT NULL CHECK (year BETWEEN 1 AND 4),
    gpa          DECIMAL(3,2)  CHECK (gpa BETWEEN 0.0 AND 4.0)
);
```

**Design notes:**
- `student_id` is a surrogate key (system-generated integer).
- `email` carries a `UNIQUE` constraint — it is a natural key, but not the PK.
- `year` is constrained to 1–4 (freshman through senior).
- `gpa` is optional (NULL-able) — a new student may not have one yet.

---

### courses

```sql
CREATE TABLE courses (
    course_id    INTEGER       PRIMARY KEY,
    course_name  VARCHAR(150)  NOT NULL,
    department   VARCHAR(80)   NOT NULL,
    credits      INTEGER       NOT NULL CHECK (credits BETWEEN 1 AND 6),
    semester     VARCHAR(20)   NOT NULL,   -- e.g. 'Fall 2025'
    instructor   VARCHAR(100)
);
```

**Design notes:**
- `semester` is stored as a string for flexibility (e.g., `'Fall 2025'`, `'Spring 2026'`).
- `instructor` is nullable — a course can be listed before an instructor is assigned.
- `department` is a plain string here. In a production schema you might normalize it
  into a separate `departments` table; for teaching purposes, keeping it denormalized
  makes Level 1 queries simpler.

---

### books

```sql
CREATE TABLE books (
    book_id      INTEGER       PRIMARY KEY,
    title        VARCHAR(200)  NOT NULL,
    author       VARCHAR(150)  NOT NULL,
    isbn         VARCHAR(20)   UNIQUE NOT NULL,
    price        DECIMAL(6,2)  NOT NULL CHECK (price >= 0),
    category     VARCHAR(50)   NOT NULL,   -- 'Textbook', 'Novel', 'Reference', ...
    publisher    VARCHAR(100)
);
```

**Design notes:**
- `isbn` is a **natural key** — globally unique, assigned outside our system.
  It gets a `UNIQUE` constraint but is not the PK (we use a surrogate `book_id`).
  This is a teachable moment: surrogate vs. natural keys.
- `price` reflects the **current** catalog price. The price at time of purchase is
  captured separately in `purchases.total_amount`.
- `category` enables filtering and grouping without a join.

---

### purchases

```sql
CREATE TABLE purchases (
    purchase_id    INTEGER        PRIMARY KEY,
    student_id     INTEGER        NOT NULL REFERENCES students(student_id),
    book_id        INTEGER        NOT NULL REFERENCES books(book_id),
    course_id      INTEGER        REFERENCES courses(course_id),
    purchase_date  DATE           NOT NULL,
    quantity       INTEGER        NOT NULL DEFAULT 1 CHECK (quantity > 0),
    total_amount   DECIMAL(8,2)   NOT NULL CHECK (total_amount >= 0)
);
```

**Design notes:**
- This is the **fact table** — the transactional center of the schema. All three
  entity tables converge here via foreign keys.
- `course_id` is **nullable**: a student might buy a book without associating it
  with a specific course (general interest, gift, etc.).
- `total_amount` is stored explicitly, not derived from `books.price × quantity`.
  Prices change; this preserves the historical truth of what was paid.
- The combination of `student_id + book_id + purchase_date` is not enforced as unique —
  a student could buy the same book twice (lost copy, second edition, etc.).

---

### course_books

```sql
CREATE TABLE course_books (
    course_id   INTEGER      NOT NULL REFERENCES courses(course_id),
    book_id     INTEGER      NOT NULL REFERENCES books(book_id),
    required    BOOLEAN      NOT NULL DEFAULT TRUE,
    edition     VARCHAR(20),
    PRIMARY KEY (course_id, book_id)
);
```

**Design notes:**
- **Composite primary key** on `(course_id, book_id)` — a book appears at most once
  per course listing. This is the only table in the schema with a composite PK.
- `required` distinguishes required reading from optional/recommended titles.
  This one boolean enables a whole class of interesting queries in Level 2.
- `edition` records which edition is specified by the course, independent of the
  edition description in `books`.

---

## Relationships

```
students  ──< purchases >── books
                 │
              courses
                 │
          course_books >── books
```

| Relationship | Cardinality | Via |
|---|---|---|
| student → purchases | 1 : Many | `purchases.student_id` |
| book → purchases | 1 : Many | `purchases.book_id` |
| course → purchases | 1 : Many | `purchases.course_id` |
| course ↔ book | Many : Many | `course_books` junction |

---

## Sample Query — Each Level

**Level 1**
```sql
-- Top 5 most expensive textbooks
SELECT title, author, price
FROM books
WHERE category = 'Textbook'
ORDER BY price DESC
LIMIT 5;
```

**Level 2**
```sql
-- Total revenue per department
SELECT c.department,
       SUM(p.total_amount) AS total_revenue,
       COUNT(*)            AS num_purchases
FROM purchases p
JOIN courses c ON p.course_id = c.course_id
GROUP BY c.department
ORDER BY total_revenue DESC;
```

**Level 3**
```sql
-- Running total of revenue by month
SELECT purchase_date,
       total_amount,
       SUM(total_amount) OVER (ORDER BY purchase_date) AS running_total
FROM purchases
ORDER BY purchase_date;
```

---

## Indexes (Level 3 Discussion)

```sql
-- Without index: full scan on purchases
-- With index: seek on student_id
CREATE INDEX idx_purchases_student ON purchases(student_id);
CREATE INDEX idx_purchases_book    ON purchases(book_id);
CREATE INDEX idx_purchases_date    ON purchases(purchase_date);
```

Students time the same query before and after creating an index to see the
performance difference — a concrete, empirical demonstration of why indexes matter.

---

*OMIS-105 · Santa Clara University · Leavey School of Business*
