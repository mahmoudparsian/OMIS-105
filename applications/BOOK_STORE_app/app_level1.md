# app_level1.py — Level 1: Explore & Query
## OMIS-105: Introduction to DBMS · Santa Clara University

---

## What Is This App?

This is a **read-only data explorer** for the University Bookstore database.
You cannot add, change, or delete any data — your only job is to *look* at what's there.

Think of it like a window into a database. You control what you see through dropdowns
and sliders, and the app shows you the exact SQL query it used to fetch your answer.

---

## The Story

Santa Clara University's bookstore sells textbooks, reference books, and novels to
students each semester. The database tracks:

- **Who** is buying (students — their major, year, GPA)
- **What** they are buying (books — title, author, price, category)
- **Why** they are buying it (courses — department, semester, instructor)
- **When and how much** they paid (purchases — date, quantity, total amount)
- **Which books belong to which course** (course_books — required or optional)

All of this lives in five tables in a single file called `bookstore.duckdb`.

---

## How to Run It

```bash
pip install streamlit duckdb pandas
streamlit run app_level1.py
```

A browser tab will open automatically.

---

## The Three Pages

### 🏠 Page 1 — Home

The home page gives you the big picture:

- How many rows are in each table?
- What do the first few rows of each table look like?
- What are the headline numbers? (top-spending department, most-bought book, total revenue)

Nothing to configure here — just read and explore.

---

### 🔍 Page 2 — Table Explorer

Pick any table and browse its data.

**Controls:**
- **Table** — choose from students, courses, books, course_books, or purchases
- **Columns to show** — leave empty to see all columns, or pick specific ones
- **Row limit** — slider from 0 to the table's actual row count, step 1
  - Set to any number to cap the result with `LIMIT N`
  - Set to **0** to remove the `LIMIT` clause entirely and return all rows

**What to notice:**
Every time you change a control, the SQL panel on the right updates instantly.
For example, if you pick the `books` table, show only `title` and `price`,
and set the limit to 5, the SQL becomes:

```sql
SELECT title, price
FROM   books
LIMIT  5;
```

Set the limit to 0 and the `LIMIT` clause disappears completely:

```sql
SELECT title, price
FROM   books;
```

The panel also explains in plain English whether a limit is applied and how
many rows were omitted.

**Below the results** you will find the Column Reference — a list of every column
in the table, its data type, and whether it can be NULL.

---

### 🛠️ Page 3 — Query Builder

This page has six query templates. Each one focuses on a different SQL concept.
Pick a template from the dropdown and use the controls to shape the query.

---

#### Template 1 · Books by Category

**What it teaches:** `WHERE` with a string comparison, `ORDER BY`

You pick a category (Textbook, Reference, or Novel) and a sort column.
The app filters the books table to just that category and sorts the result.

```sql
SELECT title, author, price, publisher
FROM   books
WHERE  category = 'Textbook'
ORDER BY price DESC;
```

**Try this:** Switch between Textbook and Reference. Notice that textbooks
are significantly more expensive — which sets up a discussion for Level 2.

---

#### Template 2 · Students by Major

**What it teaches:** `WHERE` with a string comparison, `ORDER BY` on multiple columns

Pick a major and a sort column to see all students in that program.

```sql
SELECT name, email, year, gpa
FROM   students
WHERE  major = 'Computer Science'
ORDER BY gpa DESC;
```

**Try this:** Sort by `year ASC` to see freshmen first, then `gpa DESC` to
see the highest achievers. Notice how the same data looks completely different
depending on how you sort it.

---

#### Template 3 · Top N Most Expensive Books

**What it teaches:** `ORDER BY ... DESC`, `LIMIT`

Use a slider to choose how many books to show. Optionally filter by category.

```sql
SELECT title, author, category, price
FROM   books
ORDER BY price DESC
LIMIT  5;
```

**Key insight:** `LIMIT` applies *after* sorting. That's why you get the true
top-5 most expensive — not just the first 5 rows stored in the table.

---

#### Template 4 · Books in a Price Range

**What it teaches:** `BETWEEN ... AND ...`

Drag the price range slider to set a minimum and maximum price.

```sql
SELECT title, author, category, price
FROM   books
WHERE  price BETWEEN 20 AND 100
ORDER BY price ASC;
```

**Key insight:** `BETWEEN` is inclusive — both endpoints are included in the results.
It is exactly equivalent to `WHERE price >= 20 AND price <= 100`.

---

#### Template 5 · Students with GPA Above a Threshold

**What it teaches:** Numeric comparison operators (`>=`, `>`, `<`, `<=`)

Slide the GPA threshold and watch the result set grow or shrink.

```sql
SELECT name, major, year, gpa
FROM   students
WHERE  gpa >= 3.5
ORDER BY gpa DESC;
```

**Key insight:** Numbers in SQL do not use quotes. Only string values (like
a major name or a category) need single quotes around them.

---

#### Template 6 · Purchases in a Date Range

**What it teaches:** `BETWEEN` on a `DATE` column

Pick a start and end date to see all purchases in that window.

```sql
SELECT purchase_id, student_id, book_id,
       purchase_date, quantity, total_amount
FROM   purchases
WHERE  purchase_date BETWEEN '2025-08-26' AND '2025-12-31'
ORDER BY purchase_date ASC;
```

**Key insight:** Date literals are written as strings in `'YYYY-MM-DD'` format.
DuckDB compares them chronologically when the column type is `DATE`.

**Try this:** Set the range to Fall 2025 (`2025-08-26` → `2025-12-31`), note
the total. Then switch to Spring 2026 (`2026-01-01` → `2026-06-30`).
Which semester had higher revenue? Does that match the Home page?

---

## SQL Concepts Covered in Level 1

| Concept | What It Does | Example |
|---------|--------------|---------|
| `SELECT` | Choose which columns to return | `SELECT title, price` |
| `FROM` | Choose which table to query | `FROM books` |
| `WHERE` | Filter rows by a condition | `WHERE category = 'Textbook'` |
| `ORDER BY` | Sort the results | `ORDER BY price DESC` |
| `LIMIT` | Cap the number of rows returned | `LIMIT 10` |
| `BETWEEN` | Filter a range (inclusive) | `WHERE price BETWEEN 20 AND 100` |
| `>=`, `<=`, etc. | Numeric / date comparisons | `WHERE gpa >= 3.5` |

---

## What Level 1 Does NOT Do

- No joins — every query touches exactly one table
- No aggregation — no SUM, COUNT, AVG, or GROUP BY
- No data entry — you cannot INSERT, UPDATE, or DELETE anything
- No free-text SQL — all queries are built through controls

Those come in Level 2 and Level 3.

---

## What to Explore on Your Own

1. Which category has the fewest books?
2. Are there any students with a GPA below 3.2?
3. What is the cheapest book in the Textbook category?
4. How many purchases happened in January 2026?
5. Which column in `purchases` can be NULL, and why does that make sense?

---

*OMIS-105 · Santa Clara University · Leavey School of Business · Level 1 of 3*
