# app_bookstore.py — SCU Bookstore Intelligence Platform
## OMIS-105: Introduction to DBMS · Santa Clara University

---

## What Is This App?

This is not a teaching tool. It is a **real application**.

Every chart, every alert, every number on screen is computed live from a
relational database using SQL — the same way production analytics platforms
at companies like Amazon, Spotify, and Netflix work. The database is DuckDB,
running entirely in a single file on your laptop, with no server, no cloud,
and no configuration.

The goal is to show you what becomes possible when you combine five
well-designed tables with the full power of SQL. By the end of this tour
you will understand why relational databases are the backbone of virtually
every serious application in the world.

---

## How to Run It

```bash
# One-time setup
pip install duckdb streamlit pandas matplotlib
python seed.py          # loads the database

# Launch
streamlit run app_bookstore.py
```

> **To reset all data** after adding records: `python seed.py` — it wipes
> and rebuilds from scratch.

---

## The Database Behind the App

Five tables. 13 students. 24 books. 8 courses. 60+ purchases.

```
students  ──< purchases >── books
                 │
              courses
                 │
          course_books >── books
```

Three of the 13 students have **never made a purchase** — they are registered
but inactive. Four of the 24 books have **never been sold** — they sit in
the catalog earning nothing. These are not accidents; they are deliberate
design choices that allow the app to demonstrate one of SQL's most powerful
patterns: the **LEFT JOIN anti-join**.

---

## The Six Sections

---

### 🏠 Section 1 — Executive Dashboard

The first thing a bookstore manager sees when they open the app.

**Six KPI metrics** across the top of the page give an instant snapshot:
total revenue, how many students are active buyers vs registered-but-inactive,
how many books are selling vs sitting unsold, total purchases, average order
value, and the top-earning department.

**Business Alerts** are the most instructive part of this section. Two alert
boxes appear — one red, one amber — automatically flagging problems that
would require hours of manual spreadsheet work to find:

The red alert identifies students who have accounts but have never bought
anything. The query behind it is a single LEFT JOIN anti-join:

```sql
SELECT s.name, s.major, s.year, s.gpa
FROM   students s
LEFT   JOIN purchases p ON s.student_id = p.student_id
WHERE  p.purchase_id IS NULL;  -- ← the anti-join condition
```

This says: *"Give me every student. If they have no matching purchase row,
their purchase columns will be NULL. Keep only those NULL rows."*
Three students appear: Maria Santos, Kevin Osei, and Priya Nair.
In a real business, this triggers a targeted promotion or follow-up email.

The amber alert does the same for books — four titles in the catalog that
have never appeared in a purchase: AI: A Modern Approach, The Art of War,
Python for Data Analysis, and Operating System Concepts. Their combined
catalog value is over $460. Dead stock is a real business problem, and SQL
finds it in milliseconds.

**Smart Insights** are three automatically generated sentences at the bottom
of the dashboard — facts extracted from SQL queries and formatted as
business-readable text. Who is the top customer? How much more do they spend
than average? What fraction of revenue comes from Fall semester? These
insights update automatically as data changes.

---

### 👥 Section 2 — Student Intelligence

A deep look at buying behaviour across the student population.

The **Spending Leaderboard** ranks every buyer from highest to lowest total
spend using a window function:

```sql
SELECT ROW_NUMBER() OVER (ORDER BY SUM(p.total_amount) DESC) AS rank,
       s.name, s.major,
       COUNT(*)                     AS purchases,
       ROUND(SUM(p.total_amount),2) AS total_spent
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.name, s.major, s.year
ORDER  BY total_spent DESC;
```

The `ROW_NUMBER() OVER` clause assigns rank 1 to the highest spender,
rank 2 to the next, and so on — without any application code, purely in SQL.
The horizontal bar chart is colour-coded by major so patterns emerge visually:
CS students cluster near the top.

The **Inactive Accounts** table highlights the three never-purchased students
with a prominent red alert. The LEFT JOIN anti-join pattern is shown on demand
with a "View SQL" expander and an explanation of exactly what `WHERE p.purchase_id IS NULL`
means.

**Spending by Major** and **Spending by Academic Year** provide two more views.
The year analysis often surprises students: seniors spend more per purchase
than freshmen, but freshmen make a comparable number of purchases — because
they buy required textbooks for every course without yet knowing which optional
titles are worth it.

---

### 📖 Section 3 — Catalog & Inventory

The complete inventory picture — every book, what it earned, and what it didn't.

The **Full Catalog Performance** table is built with a LEFT JOIN that reaches
across all 24 books, including the ones with zero purchases:

```sql
SELECT b.title, b.category, b.price,
       COALESCE(COUNT(p.purchase_id), 0)          AS times_purchased,
       COALESCE(ROUND(SUM(p.total_amount),2), 0)  AS total_revenue,
       CASE WHEN COUNT(p.purchase_id) = 0
            THEN '🔴 Never Sold' ELSE '🟢 Active' END AS status
FROM   books b
LEFT   JOIN purchases p ON b.book_id = p.book_id
GROUP  BY b.book_id, b.title, b.category, b.price
ORDER  BY total_revenue DESC;
```

`COALESCE` converts NULL (no sales) into 0, so the table always shows a clean
number instead of an empty cell. The status column is computed entirely in SQL
using a `CASE` expression — no post-processing in Python.

The **Dead Stock Alert** table repeats the four unsold books with the dollar
value of potential unrealised revenue, prompting the question: *should these
be promoted, discounted, or dropped from the catalog?*

The **Price vs Revenue Scatter Plot** is the most visually striking chart in
the app. Each book is a bubble: x-axis is list price, y-axis is total revenue
earned, bubble size is how many times it was purchased, and colour represents
category. Books that were never sold appear as red ✕ markers. The scatter
immediately reveals that expensive textbooks that sell even a few times
generate more revenue than cheap novels that sell many times.

---

### 💰 Section 4 — Revenue Analytics

Four views of revenue, each answering a different business question.

**Cumulative Revenue** uses a window function to compute a running total of
every dollar the bookstore has ever received, date by date:

```sql
SELECT purchase_date,
       ROUND(SUM(total_amount), 2)                                    AS daily_rev,
       ROUND(SUM(SUM(total_amount)) OVER (ORDER BY purchase_date), 2) AS cumulative
FROM   purchases
GROUP  BY purchase_date
ORDER  BY purchase_date;
```

The outer `SUM(...) OVER (ORDER BY purchase_date)` accumulates as it moves
forward in time. The result is rendered as an area chart with bars for daily
revenue and a smooth rising line for the cumulative — a classic business
intelligence visualisation.

**Fall vs Spring** breaks revenue down by semester. Fall 2025 outperforms
Spring 2026 by roughly 25% — a textbook rush effect. The comparison table
also shows average order value and unique students per semester.

**Required vs Optional** uses a JOIN on two columns simultaneously to
classify every purchase:

```sql
FROM purchases p
JOIN course_books cb
     ON p.book_id = cb.book_id AND p.course_id = cb.course_id
```

The result shows that required books generate significantly more revenue per
purchase than optional ones, even though the purchase counts are similar —
because required reading tends to be expensive textbooks. The dual pie charts
make this contrast immediate.

**Per-Student vs Major Average** uses `AVG() OVER (PARTITION BY major)` to
place each student's total spend alongside their major's average in the same
query — without a subquery or self-join. Students above their major's average
appear in green; those below in red. The dashed orange lines mark each major's
average across the bar chart.

---

### ✏️ Section 5 — Manager Actions

The first section that changes the database.

**Record a Purchase** lets the manager select a student and a book from
dropdowns. The app computes `total_amount = price × quantity` automatically
and shows the exact INSERT statement it will execute before any data is written:

```sql
INSERT INTO purchases
    (purchase_id, student_id, book_id, course_id,
     purchase_date, quantity, total_amount)
VALUES (61, 3, 11, 6, '2026-06-06', 1, 79.99);
```

This demonstrates a core RDBMS design principle: `total_amount` is stored
explicitly rather than derived from the current book price. Prices change over
time. Storing the amount paid at the time of sale preserves historical truth —
a fact that becomes obvious the moment you imagine updating a price and watching
old revenue figures change.

**Register a Student** adds a new row to the `students` table. The next
available `student_id` is computed with `MAX(student_id) + 1` — no
auto-increment needed because DuckDB handles it cleanly in a single query.

**Recent Activity** shows the 25 most recent purchases via a four-table JOIN:
purchases linked to students, books, and courses in one query. This is the kind
of activity feed that appears in every real transaction system.

---

### 🔬 Section 6 — SQL Playground

The most open-ended section. Write any SELECT query. See the result.
If the result has a numeric column, chart it.

A **Schema Quick-Reference** panel lists every table and column so you never
have to guess a column name. A **10-query example library** loads pre-written
SQL into the editor with one click — covering anti-joins, window functions,
aggregations, and monthly trends.

The **SQL editor** accepts any SELECT (or WITH / EXPLAIN) statement.
Write operations are blocked for safety.

When the result has at least one text column and one numeric column, the
**chart builder** appears automatically with six chart types:

| Chart type | Best for |
|---|---|
| Bar Chart | Comparing categories side by side |
| Horizontal Bar | Ranked lists with long labels |
| Pie Chart | Parts of a whole (2–8 slices) |
| Line Chart | Trends over time |
| Area Chart | Cumulative or volume trends |
| Scatter Plot | Relationship between two numeric columns |

Column pickers let you choose which column goes on each axis. Four colour
palettes — Indigo, Emerald, Amber, and Multi-colour — match the app's design
language. Every chart renders with value labels and the same dark theme as
the rest of the platform.

**Try this sequence in the Playground:**

1. Load "Books never sold" — the anti-join query. Notice the four books.
2. Load "Revenue by department" — change chart type to Pie. See CS and EE dominate.
3. Load "Cumulative revenue by date" — switch to Area Chart. The slope tells the story.
4. Write your own: `SELECT major, COUNT(*) AS students FROM students GROUP BY major` — then try every chart type on it.
5. Try `EXPLAIN SELECT * FROM purchases WHERE student_id = 1` — read the execution plan.

---

## What Makes This App Impressive

Everything you see is produced by SQL running against a file on your laptop.
No cloud. No API calls. No data pipeline. Five tables and a query engine.

The LEFT JOIN anti-join detects inactive customers in one query. Window
functions rank and compare thousands of rows without any loop in application
code. A scatter plot with bubble sizes and colour encoding emerges from four
lines of SQL and ten lines of matplotlib. The cumulative revenue chart that
looks like it belongs in a VC pitch deck is a single window function.

This is what relational databases are for. Not storing data — *understanding* it.

---

## Key SQL Patterns Used in This App

| Pattern | Where you see it |
|---|---|
| `LEFT JOIN + WHERE IS NULL` | Inactive students, dead-stock books |
| `ROW_NUMBER() OVER (ORDER BY ...)` | Customer leaderboard |
| `SUM() OVER (ORDER BY date)` | Cumulative revenue chart |
| `AVG() OVER (PARTITION BY major)` | Per-student vs major comparison |
| `COALESCE(agg, 0)` | Catalog table — zero sales shown cleanly |
| `CASE WHEN ... END` | Status column, year labels |
| Multi-column JOIN (`ON a=a AND b=b`) | Required vs optional classification |
| `strftime(date, '%Y-%m')` | Monthly revenue grouping |
| `MAX(id) + 1` | Next available primary key for INSERT |
| `INSERT INTO ... VALUES (...)` | Manager Actions — recording purchases |

---

## The Complete Journey

| App | What it teaches |
|---|---|
| `app_level1.py` | One table at a time — SELECT, WHERE, ORDER BY |
| `app_level2.py` | Linking tables — JOIN, GROUP BY, HAVING |
| `app_level3.py` | Advanced analytics — window functions, indexes, INSERT |
| `app_bookstore.py` | Everything at once — a real application |

The bookstore app does not explain SQL clause by clause. It shows what SQL
*produces* when all the pieces come together: a dashboard a real business
could use, built on a database that fits in a single file.

---

*OMIS-105 · Santa Clara University · Leavey School of Business*
*SCU Bookstore Intelligence Platform — powered by DuckDB + Streamlit*
