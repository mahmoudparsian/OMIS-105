# app_level3.py — Level 3: Analytics & Power
## OMIS-105: Introduction to DBMS · Santa Clara University

---

## What Is This App?

Level 3 is the most powerful app in the series — and the first one that lets
you **change the database**. You can insert new students and purchases, and
those records immediately appear in queries.

The app also introduces the most advanced SQL features:
- **Window functions** — computations that look across multiple rows at once
- **Subqueries** — queries nested inside other queries
- **Indexes** — data structures that make lookups dramatically faster

---

## How to Run It

```bash
streamlit run app_level3.py
```

> **Note:** This app opens the database in **write mode** (not read-only).
> Run `python seed.py` to reset the database to its original state at any time.

---

## The Three Pages

---

### 📈 Page 1 — Analytics Dashboard

Six analyses, each demonstrating a different advanced SQL technique.
Pick one from the dropdown. Every analysis shows a data table, the SQL that
ran, a plain-English explanation, and a **matplotlib chart** visualising the result.

---

#### Analysis 1 · Running Total of Revenue by Date

Shows daily bookstore revenue alongside a cumulative running total.

```sql
SELECT purchase_date,
       SUM(total_amount)                        AS daily_revenue,
       SUM(SUM(total_amount))
           OVER (ORDER BY purchase_date)        AS running_total
FROM   purchases
GROUP  BY purchase_date
ORDER  BY purchase_date;
```

**What to notice:** The `OVER (ORDER BY ...)` clause is what makes this a
window function. Without it, `SUM(SUM(...))` would just be the grand total.
With it, the outer SUM "looks back" over all previous dates and accumulates.

**Chart:** Dual-axis — purple bars show daily revenue, green line shows the
cumulative running total growing over time.

---

#### Analysis 2 · Rank Students by Total Spend

Ranks every student by how much they spent, using three different ranking
functions. Switch between them and watch how ties are handled.

| Function | Behaviour with ties |
|---|---|
| `ROW_NUMBER()` | Always unique — 1, 2, 3, 4 … |
| `RANK()` | Ties get the same rank, then gaps — 1, 2, 2, 4 … |
| `DENSE_RANK()` | Ties get the same rank, no gaps — 1, 2, 2, 3 … |

**Chart:** Horizontal bar chart, sorted by spend, each bar colored by the
student's major. Dollar labels appear on the end of every bar.

```sql
SELECT ROW_NUMBER() OVER (ORDER BY total_spent DESC) AS rank,
       name, major, total_spent
FROM (
    SELECT s.name, s.major, SUM(p.total_amount) AS total_spent
    FROM   purchases p
    JOIN   students s ON p.student_id = s.student_id
    GROUP  BY s.name, s.major
) ranked;
```

---

#### Analysis 3 · Books Ranked Within Category

Uses `PARTITION BY` to restart the rank counter for each book category.
This is one of the most common real-world uses of window functions.

```sql
SELECT b.category, b.title, COUNT(*) AS times_purchased,
       RANK() OVER (
           PARTITION BY b.category
           ORDER BY COUNT(*) DESC
       ) AS rank_in_category
FROM   purchases p
JOIN   books b ON p.book_id = b.book_id
GROUP  BY b.category, b.title;
```

**Key insight:** `PARTITION BY` is to window functions what `GROUP BY` is to
aggregates — it defines the boundary of the window. The rank resets to 1
at the start of each category.

**Chart:** Three side-by-side panels (one per category). Each panel shows
purchase counts as horizontal bars, with books ordered by rank within their category.

---

#### Analysis 4 · Each Student vs Their Major's Average Spend

Shows every student's total spend *and* the average spend for their major
in the same row — without a separate join or subquery.

```sql
SELECT s.name, s.major,
       ROUND(SUM(p.total_amount), 2)                AS student_total,
       ROUND(AVG(SUM(p.total_amount))
             OVER (PARTITION BY s.major), 2)        AS major_avg,
       ROUND(SUM(p.total_amount)
             - AVG(SUM(p.total_amount))
               OVER (PARTITION BY s.major), 2)      AS vs_major_avg
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.name, s.major;
```

`vs_major_avg` is positive (green) for students who spent more than their
peers, negative (red) for those who spent less.

**Chart:** Bar chart per student — green bars are above their major's average,
red bars below. A dashed orange line marks each major's average, restarting
at the boundary between majors.

---

#### Analysis 5 · Students Who Spent Above the Overall Average (Subquery)

Uses a **scalar subquery** in the `HAVING` clause — the inner query computes
one number (the average), and the outer query compares each student to it.

```sql
SELECT s.name, s.major, ROUND(SUM(p.total_amount), 2) AS total_spent
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.name, s.major
HAVING SUM(p.total_amount) > (
    SELECT AVG(student_total)
    FROM (
        SELECT SUM(total_amount) AS student_total
        FROM   purchases
        GROUP  BY student_id
    )
);
```

**What a scalar subquery is:** A subquery that returns exactly one row and
one column — a single value. The outer query treats it like a number literal.
The inner query runs first; the result is plugged into the outer query.

**Chart:** All 10 students shown as bars. Purple = above the overall average,
dark grey = below. A yellow dashed line marks the average so the threshold is
immediately visible.

---

#### Analysis 6 · Books Above Their Category Average (Correlated Subquery)

Uses a **correlated subquery** — the inner query references a column from
the outer query, so it runs once per row.

```sql
SELECT b.title, b.category, b.price,
       (SELECT AVG(price) FROM books b2 WHERE b2.category = b.category) AS category_avg
FROM   books b
WHERE  b.price > (
    SELECT AVG(price) FROM books b2 WHERE b2.category = b.category
);
```

Each book is compared to the average price of *its own category*.
Without correlation, a $17 novel would be compared to the average of
all books (including $224 textbooks) and might wrongly appear cheap.

**Chart:** Three panels (Textbook / Reference / Novel). Each book is shown as
a horizontal bar — bright fill = above category average, faded = below.
A yellow dashed line marks the category average in each panel.

---

### ➕ Page 2 — Add Records

The first page in the series where you can **write** to the database.

Two tabs:

**🎓 Add a Student**
Fill in the name, email, major, year, and GPA. The app computes the next
available `student_id` automatically and shows the exact INSERT statement
it will run before you click the button.

```sql
INSERT INTO students
    (student_id, name, email, major, year, gpa)
VALUES
    (11, 'Sofia Reyes', 'sreyes@scu.edu', 'Computer Science', 2, 3.75);
```

After inserting, the full `students` table refreshes so you can see the
new row.

**🛒 Add a Purchase**
Choose a student, a book, and an optional course from dropdowns.
The app computes `total_amount` automatically as `quantity × book price`,
which demonstrates why that column exists — it locks in the price at the
time of sale.

```sql
INSERT INTO purchases
    (purchase_id, student_id, book_id, course_id,
     purchase_date, quantity, total_amount)
VALUES
    (61, 11, 3, NULL, '2026-06-05', 1, 114.95);
```

The 15 most recent purchases refresh after each insert.

> **To reset:** Run `python seed.py` from the terminal. This drops and
> recreates all tables with the original 60 purchases and 10 students.

---

### ⚡ Page 3 — Index Lab

The most hands-on page. You control indexes and measure the impact.

**Index Status panel:** shows whether each of the three useful indexes
currently exists, with CREATE and DROP buttons for each.

```sql
CREATE INDEX idx_purchases_student ON purchases(student_id);
CREATE INDEX idx_purchases_book    ON purchases(book_id);
CREATE INDEX idx_purchases_date    ON purchases(purchase_date);
```

**Timing Comparison:** pick a query, choose how many repetitions (50–1000),
and click Run. The app:
1. Drops the relevant index (if it exists)
2. Times the query N times — records the average milliseconds per call
3. Creates the index
4. Times the same query N times again
5. Reports the speedup factor

**What you will see:** On 60 rows the speedup is modest — maybe 1.5–3×.
That is expected. On a table with 1 million rows, the same index can yield
1,000× or more. The lab makes the *mechanism* visible even if the scale is small.

**EXPLAIN panel:** shows DuckDB's query execution plan side by side —
*without index* on the left, *with index* on the right. The full plan
text is rendered as a code block so you can read the complete tree. Look for:
- `SEQ_SCAN` — a full sequential scan (no index in use)
- `INDEX_SCAN` — the database is using the index for a direct lookup

The execution plan is the query optimiser's blueprint — it shows *how* the
database will retrieve data before it actually does so. The query is identical
in both panels; only the execution strategy changes.

---

## SQL Concepts Covered in Level 3

| Concept | What It Does | Example |
|---|---|---|
| `ROW_NUMBER() OVER` | Unique sequential rank | `ROW_NUMBER() OVER (ORDER BY total DESC)` |
| `RANK() OVER` | Rank with gaps for ties | `RANK() OVER (ORDER BY price DESC)` |
| `DENSE_RANK() OVER` | Rank without gaps for ties | `DENSE_RANK() OVER (ORDER BY gpa DESC)` |
| `SUM() OVER (ORDER BY)` | Running / cumulative total | `SUM(amount) OVER (ORDER BY date)` |
| `AVG() OVER (PARTITION BY)` | Group average per row | `AVG(total) OVER (PARTITION BY major)` |
| `PARTITION BY` | Restart window per group | `OVER (PARTITION BY category ORDER BY price)` |
| Scalar subquery | Single-value inner query | `HAVING total > (SELECT AVG(...) FROM ...)` |
| Correlated subquery | Inner references outer row | `WHERE price > (SELECT AVG(price) FROM ... WHERE category = b.category)` |
| `INSERT INTO` | Add a new row | `INSERT INTO students VALUES (...)` |
| `CREATE INDEX` | Build a lookup structure | `CREATE INDEX idx ON purchases(student_id)` |
| `DROP INDEX` | Remove an index | `DROP INDEX idx_purchases_student` |
| `EXPLAIN` | Show the query execution plan | `EXPLAIN SELECT ...` |

---

## What to Explore on Your Own

1. Insert yourself as a new student and then add a purchase of your favourite book in the catalog.
2. After inserting, run Analysis 2 (rank students by spend) — where do you rank?
3. In the Index Lab, create all three indexes and run EXPLAIN. Does the plan change?
4. In Analysis 4, which major has the highest average spend? Which student is furthest above their major's average?
5. In Analysis 6, are there any categories where *every* book costs above the category average? (Hint: that is mathematically impossible — why?)

---

## The Complete Three-Level Journey

| Level | Mode | Core idea |
|---|---|---|
| 1 | Read-only | One table at a time — SELECT, WHERE, ORDER BY |
| 2 | Read-only | Link tables — JOIN, GROUP BY, HAVING |
| 3 | Read + Write | Advanced analytics + modifying the database |

By the end of Level 3 you have written queries that span five tables,
computed running totals across time, ranked rows within groups, inserted
new records, and measured the performance impact of indexes — all on a
database that lives in a single file on your laptop.

---

*OMIS-105 · Santa Clara University · Leavey School of Business · Level 3 of 3*
