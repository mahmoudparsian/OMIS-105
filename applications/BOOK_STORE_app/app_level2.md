# app_level2.py — Level 2: Relationships & Joins
## OMIS-105: Introduction to DBMS · Santa Clara University

---

## What Is This App?

This is still a **read-only** app — you cannot add or change data. But now your
queries span *multiple tables* at once. Level 2 is where the real power of a
relational database becomes visible.

In Level 1, every query touched one table and results contained raw IDs like
`student_id = 3`. In Level 2 you will link tables together so those IDs become
names, departments, and book titles — and you will aggregate thousands of rows
into meaningful summaries.

---

## The Big Idea: Why JOINs Exist

Imagine you want to know: *"Which department spent the most at the bookstore?"*

The `purchases` table has `total_amount` — but no department name.
The `courses` table has `department` — but no dollar amounts.
Neither table alone can answer the question.

A `JOIN` connects the two tables on their shared key (`course_id`) and lets you
treat the combined result as a single virtual table. Then `GROUP BY` collapses
the rows into one row per department, and `SUM` adds up the revenue.

```sql
SELECT c.department,
       SUM(p.total_amount) AS revenue
FROM   purchases p
JOIN   courses c ON p.course_id = c.course_id
GROUP  BY c.department
ORDER  BY revenue DESC;
```

This single query answers a question that was impossible in Level 1.

---

## How to Run It

```bash
streamlit run app_level2.py
```

(Requires `bookstore.duckdb` in the same folder. Run `seed.py` first if needed.)

---

## The Three Pages

### 🏠 Page 1 — Home

The home page shows what becomes possible once you can join tables:

- **Top department by revenue** — requires linking `purchases` to `courses`
- **Most purchased book** — requires linking `purchases` to `books`
- **Average spend per student** — requires `GROUP BY` on `student_id`
- **Full revenue-by-department table** — sorted, with purchase counts
- **Spend by student** — every student's total with their major
- **Required vs Optional revenue comparison** — a join on *two* columns simultaneously

Every table on this page has a "Show SQL" expander — click it to see the query.

---

### 🔗 Page 2 — Join Explorer

Pick a table pair and a join type, and see the results side by side.

**Available table pairs:**
- `purchases ↔ students` — who made each purchase?
- `purchases ↔ books` — what was bought?
- `purchases ↔ courses` — which course drove each purchase?
- `books ↔ course_books` — is each book assigned to a course?
- `courses ↔ course_books` — what books does each course use?

**Join types:**
- `INNER JOIN` — keep only rows that have a match in *both* tables
- `LEFT JOIN` — keep all rows from the left table; fill with NULL where there is no match

**Row limit:**
- Slider from 0 to the actual result count of the current join, step 1
- Set to **0** to remove `LIMIT` entirely and see every row the join produces
- The maximum updates automatically when you switch between INNER and LEFT JOIN —
  because the two join types can return different numbers of rows

#### The Key Difference — INNER vs LEFT

```sql
-- INNER JOIN: only purchases tied to a course
SELECT p.purchase_id, p.total_amount, c.course_name
FROM   purchases p
INNER JOIN courses c ON p.course_id = c.course_id;

-- LEFT JOIN: all purchases, NULL course for unlinked ones
SELECT p.purchase_id, p.total_amount, c.course_name
FROM   purchases p
LEFT JOIN courses c ON p.course_id = c.course_id;
```

For the `purchases ↔ courses` pair, LEFT JOIN returns more rows than INNER JOIN.
That is because some purchases have a NULL `course_id` (a student bought a book
out of personal interest). INNER JOIN silently drops those rows; LEFT JOIN keeps
them with NULL in the course columns.

The side-by-side comparison at the bottom of the page makes this difference
concrete — you can see the row counts change and see which rows carry NULLs.

---

### 📊 Page 3 — Aggregation Builder

Build a `GROUP BY` query from scratch using controls. Six templates are available:

| Template | Groups by | Aggregates |
|---|---|---|
| Revenue by department | `department` | `total_amount` |
| Spend by student | `student name` | `total_amount` |
| Purchases per book | `book title` | `quantity` |
| Avg price by category | `category` | `price` |
| Books per course | `course name` | `book count` |
| Spend by major | `major` | `total_amount` |

**Controls:**
- **Aggregate function** — SUM, COUNT, AVG, MAX, or MIN
- **Sort direction** — highest first or lowest first
- **HAVING filter** — optionally filter groups by the aggregate result

---

## Key Concepts

### INNER JOIN

Keeps only rows where the `ON` condition finds a match in both tables.

```sql
SELECT s.name, p.total_amount
FROM   purchases p
INNER JOIN students s ON p.student_id = s.student_id;
```

If a student has never made a purchase, they do not appear in the result.
If a purchase has a student_id that doesn't exist in students, it is dropped.

### LEFT JOIN

Keeps every row from the left table. If there is no match on the right,
all right-side columns are NULL.

```sql
SELECT b.title, p.purchase_date
FROM   books b
LEFT JOIN purchases p ON b.book_id = p.book_id;
```

Books that were never purchased still appear — with NULL in `purchase_date`.
Useful for finding items with no activity ("which books have never been sold?").

### GROUP BY

Collapses rows that share the same value into a single summary row.

```sql
SELECT major, COUNT(*) AS num_students
FROM   students
GROUP  BY major;
```

Without `GROUP BY`, aggregate functions like `COUNT(*)` collapse the entire
table into one row. With `GROUP BY`, you get one row per group.

### Aggregate Functions

| Function | Returns |
|---|---|
| `COUNT(*)` | Number of rows in the group |
| `SUM(col)` | Total of all values |
| `AVG(col)` | Mean of all values |
| `MAX(col)` | Largest value |
| `MIN(col)` | Smallest value |

### HAVING

Filters groups *after* aggregation. It is the equivalent of `WHERE` for
aggregated results.

```sql
-- Find majors where students collectively spent more than $1,000
SELECT s.major, SUM(p.total_amount) AS total
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.major
HAVING SUM(p.total_amount) > 1000;
```

**Rule of thumb:** Use `WHERE` to filter individual rows before grouping.
Use `HAVING` to filter groups after aggregation. You cannot use `WHERE` on
an aggregate result — the aggregation hasn't happened yet at that stage.

---

## SQL Concepts Covered in Level 2

| Concept | What It Does | Example |
|---|---|---|
| `JOIN` | Link two tables on a shared key | `JOIN courses c ON p.course_id = c.course_id` |
| `INNER JOIN` | Keep only matching rows | drops NULLs and unmatched rows |
| `LEFT JOIN` | Keep all left rows | fills unmatched right side with NULL |
| `GROUP BY` | Group rows into buckets | `GROUP BY department` |
| `SUM` | Add up a column | `SUM(total_amount)` |
| `COUNT` | Count rows in a group | `COUNT(*)` |
| `AVG` | Compute the mean | `AVG(price)` |
| `MAX` / `MIN` | Largest / smallest value | `MAX(gpa)` |
| `HAVING` | Filter after aggregation | `HAVING SUM(...) > 500` |

---

## What to Explore on Your Own

1. Which student spent the most money in Fall 2025? (Hint: join purchases → courses to filter by semester, then join to students.)
2. How many books does each course have listed — required and optional combined?
3. Are there any books in the catalog that have never been purchased? (Hint: LEFT JOIN books to purchases and look for NULLs.)
4. Which major has the highest *average* spend per purchase — not total, but average?
5. Use HAVING to find all departments where the number of purchases is greater than 10.

---

## What Level 2 Does NOT Do

- No data entry — still read-only
- No window functions or subqueries — those come in Level 3
- No free-text SQL — all queries are built through controls and templates

---

*OMIS-105 · Santa Clara University · Leavey School of Business · Level 2 of 3*
