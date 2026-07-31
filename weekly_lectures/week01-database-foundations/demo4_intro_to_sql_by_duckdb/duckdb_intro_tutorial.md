---
marp: true
theme: default
paginate: true
backgroundColor: #0f1117
color: #e8eaf6
style: |
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

  section {
    font-family: 'Inter', sans-serif;
    background-color: #0f1117;
    color: #e8eaf6;
    padding: 50px 60px;
  }

  h1 {
    font-size: 2.6em;
    font-weight: 900;
    background: linear-gradient(135deg, #FFD700, #FFA500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2em;
    line-height: 1.1;
  }

  h2 {
    font-size: 1.8em;
    font-weight: 700;
    color: #FFD700;
    border-bottom: 3px solid #FFD700;
    padding-bottom: 10px;
    margin-bottom: 0.6em;
  }

  h3 {
    font-size: 1.3em;
    font-weight: 600;
    color: #FFA500;
  }

  code {
    font-family: 'JetBrains Mono', monospace;
    background: #1e2130;
    color: #61dafb;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.88em;
  }

  pre {
    background: #1a1d2e;
    border-left: 5px solid #FFD700;
    border-radius: 10px;
    padding: 20px 24px;
    font-size: 0.82em;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5);
  }

  pre code {
    background: transparent;
    color: #e8eaf6;
    padding: 0;
    font-size: 1em;
  }

  .keyword { color: #FFD700; font-weight: bold; }
  .string  { color: #98c379; }
  .comment { color: #6272a4; font-style: italic; }
  .num     { color: #bd93f9; }

  ul, ol {
    margin: 0.4em 0;
    padding-left: 1.5em;
  }

  li {
    margin: 0.35em 0;
    font-size: 0.98em;
    line-height: 1.5;
  }

  strong {
    color: #FFD700;
    font-weight: 700;
  }

  em {
    color: #FFA500;
    font-style: normal;
    font-weight: 600;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85em;
    margin-top: 0.8em;
  }

  th {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: #0f1117;
    font-weight: 700;
    padding: 10px 16px;
    text-align: left;
  }

  td {
    background: #1a1d2e;
    border-bottom: 1px solid #2d3148;
    padding: 8px 16px;
    color: #e8eaf6;
  }

  tr:nth-child(even) td {
    background: #1e2130;
  }

  blockquote {
    background: #1a1d2e;
    border-left: 5px solid #FFA500;
    border-radius: 8px;
    padding: 14px 20px;
    margin: 1em 0;
    font-style: italic;
    color: #c3c8e8;
  }

  .highlight-box {
    background: linear-gradient(135deg, #1a1d2e, #1e2340);
    border: 2px solid #FFD700;
    border-radius: 12px;
    padding: 18px 24px;
    margin: 0.8em 0;
  }

  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    align-items: start;
  }

  footer {
    color: #4a4f6a;
    font-size: 0.75em;
  }

  section.title-slide {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    text-align: left;
  }

  section.title-slide h1 {
    font-size: 3.5em;
    line-height: 1.05;
  }

  .duck-icon {
    font-size: 3em;
    margin-bottom: 0.3em;
  }

  .badge {
    display: inline-block;
    background: #FFD700;
    color: #0f1117;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75em;
    font-weight: 700;
    margin: 2px;
  }

  .tag-green  { background: #50fa7b; color: #0f1117; }
  .tag-blue   { background: #61dafb; color: #0f1117; }
  .tag-purple { background: #bd93f9; color: #0f1117; }

  section.section-break {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  section.section-break h1 {
    font-size: 3em;
  }

---

<!-- _class: title-slide -->

<div class="duck-icon">🦆</div>

# Introduction to <br> Databases & SQL

## with DuckDB

**OMIS 105 — Day 1** · *Your journey into data begins here*

---

## 🗺️ What We'll Cover Today

<div class="two-col">
<div>

**Part 1 — The Big Picture**
- What is a database?
- Why not just use Excel?
- Meet DuckDB 🦆

**Part 2 — Your First SQL**
- Anatomy of a table
- SELECT — the workhorse
- Filtering with WHERE
- Sorting with ORDER BY

</div>
<div>

**Part 3 — Aggregation**
- Summarizing with GROUP BY
- COUNT, SUM, AVG, MIN, MAX

**Part 4 — Joining Tables**
- What is a JOIN?
- INNER JOIN in action

**Hands-on Lab 🧪**
- Run it yourself in Jupyter!

</div>
</div>

---

# SQL: language of data

**Hands-on Lab 🧪**
- Run it yourself in Jupyter!

> 💡 No prior experience needed. 
> 
> If you can use Google Sheets, you can learn SQL.

---

<!-- _class: section-break -->

# Part 1
## The Big Picture

---

## 🤔 What Is a Database?

A **database** is an organized collection of structured data, stored electronically, designed to be **queried and managed efficiently**.

Think of it as a **super-powered, organized filing cabinet** that can answer questions instantly — even with millions of records.

<br>

| Filing Cabinet 📂 | Database 🗄️ |
|---|---|
| Physical folders | Tables |
| Documents in a folder | Rows |
| Fields on a form | Columns |
| Finding files manually | SQL Query |
| One person at a time | Many users simultaneously |

---

## 😩 Why Not Just Use Excel or CSV?

You might be thinking: *"I already have Excel, why learn this?"*

<div class="two-col">
<div>

**Excel struggles with:**
- Files > 1 million rows
- Multiple people editing at once
- Complex relationships between data
- Repeatable, automated analysis
- Data integrity & validation
- Joining multiple datasets

</div>
<div>

**Databases excel at:**
- **Billions** of rows, no sweat
- Concurrent multi-user access
- Foreign keys & relationships
- Version-controlled queries
- Data types & constraints
- Lightning-fast JOINs

</div>
</div>

> 🔥 **Real talk:** The average company database has tens of millions of rows. Excel would crash. DuckDB handles it in seconds.

---

## 🦆 Meet DuckDB — The Database That Runs Anywhere

**DuckDB** is a modern, open-source analytical database that runs *entirely inside your Python environment* — no server, no installation headaches.

```python
import duckdb          # That's it. You're ready!
```

<br>

**Why DuckDB is perfect for learning:**

- 🚀 **Zero setup** — install with `pip install duckdb`
- 🐍 **Python-native** — works perfectly in Jupyter notebooks
- ⚡ **Blazing fast** — column-oriented storage engine
- 📁 **Reads anything** — CSV, Parquet, JSON, Excel, even Pandas DataFrames
- 🆓 **100% free** — open source, forever
- 💼 **Industry-grade SQL** — the same SQL used in real companies

---

## 🏗️ How DuckDB Fits In the Data World

```
Your Data Sources
      │
      ▼
┌─────────────────────────────────────┐
│           DuckDB Engine             │
│   ┌──────┐ ┌──────┐ ┌──────────┐    │
│   │ CSV  │ │ JSON │ │  Parquet │    │
│   └──────┘ └──────┘ └──────────┘    │
│        ↓ SQL Queries ↓              │
│   ┌─────────────────────────────┐   │
│   │   In-Memory Columnar Store  │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
      │
      ▼
 Results → Pandas DataFrame → Charts → Reports
```

DuckDB slots neatly into any Python data pipeline.

---

<!-- _class: section-break -->

# Part 2
## Your First SQL

---

## 🏛️ Anatomy of a Table

A database table looks a lot like a spreadsheet — but with **strict rules**. Every column has a **data type**, and every row is a **record**.

```sql
-- Our sample table: students
```

| student_id | name | age | major | gpa |
|---|---|---|---|---|
| 1 | Alice Chen | 20 | Computer Science | 3.9 |
| 2 | Bob Martin | 22 | Mathematics | 3.4 |
| 3 | Carol White | 21 | Computer Science | 3.7 |
| 4 | David Lee | 23 | Physics | 3.2 |
| 5 | Emma Davis | 20 | Mathematics | 3.8 |

**Column data types:** `INTEGER`, `VARCHAR`, `DECIMAL`, `DATE`, `BOOLEAN` ...

> 🔑 Every table should have a **primary key** — a unique identifier for each row. Here it's `student_id`.

---

## 📖 SELECT — The Workhorse of SQL

`SELECT` retrieves data from a table. It's the command you'll use **90% of the time**.

**Syntax:**
```sql
SELECT column1, column2, ...
FROM table_name;
```

**Examples:**

```sql
-- Get all columns (the * means "everything")
SELECT * FROM students;

-- Get only specific columns
SELECT name, gpa FROM students;

-- Add a computed column
SELECT name, gpa, gpa * 4.0 AS scaled_score FROM students;
```

> 💡 SQL is **not case-sensitive** for keywords, but by convention we write `SELECT`, `FROM`, `WHERE` in UPPERCASE for readability.

---

## 🔍 WHERE — Filtering Your Data

`WHERE` lets you ask *"give me only rows that match this condition"*.

```sql
SELECT column1, column2
FROM table_name
WHERE condition;
```

**Comparison operators:**

| Operator | Meaning | Example |
|---|---|---|
| `=` | Equal to | `major = 'Computer Science'` |
| `!=` or `<>` | Not equal | `major != 'Physics'` |
| `>`, `<` | Greater / Less | `gpa > 3.5` |
| `>=`, `<=` | Greater/Less or equal | `age <= 21` |
| `BETWEEN` | In a range | `gpa BETWEEN 3.0 AND 3.8` |
| `LIKE` | Pattern match | `name LIKE 'A%'` |
| `IN` | In a list | `major IN ('CS', 'Math')` |

---

## 🔍 WHERE — Examples 1

```sql
-- Students with GPA above 3.5
SELECT name, gpa
FROM students
WHERE gpa > 3.5;
```

```sql
-- Students in Computer Science OR Mathematics
SELECT name, major
FROM students
WHERE major IN ('Computer Science', 'Mathematics');
```

---

## 🔍 WHERE — Examples 2

```sql
-- Combine conditions with AND / OR
SELECT name, age, gpa
FROM students
WHERE age <= 21
  AND gpa >= 3.7;
```

```sql
-- Names that start with the letter 'A' or 'E'
SELECT name FROM students
WHERE name LIKE 'A%' OR name LIKE 'E%';
```

> 🎯 `%` is a wildcard — it matches any sequence of characters.

---

## 🔢 ORDER BY — Sorting Results

`ORDER BY` controls the **order** your results come back in.

```sql
SELECT column1, column2
FROM table_name
ORDER BY column1 ASC;   -- ASC = ascending (default)
                         -- DESC = descending
```

**Examples:**

```sql
-- Best students first (highest GPA)
SELECT name, major, gpa
FROM students
ORDER BY gpa DESC;
```

---

## 🔢 ORDER BY —  examples


```sql
-- Alphabetically by major, then by GPA within each major
SELECT name, major, gpa
FROM students
ORDER BY major ASC, gpa DESC;
```

```sql
-- Limit results to top 3
SELECT name, gpa
FROM students
ORDER BY gpa DESC
LIMIT 3;
```

---

## 🧩 Putting It Together — The SQL Query Structure

Every SQL query follows this structure (in this exact order!):

```sql
SELECT   what columns to show           ← Always first
FROM     which table                    ← Where the data lives
WHERE    filter conditions              ← Optional
ORDER BY how to sort                    ← Optional
LIMIT    max number of rows to return   ← Optional
```

---

## 🧩 Putting It Together: Full example:

```sql
SELECT name, major, gpa
FROM students
WHERE gpa >= 3.5
  AND major != 'Physics'
ORDER BY gpa DESC
LIMIT 5;
```

> 🧠 **Memory trick:** Think of it as answering: "Show me ___(SELECT) from ___(FROM), but only where ___(WHERE), sorted by ___(ORDER BY)."

---

<!-- _class: section-break -->

# Part 3
## Aggregation & Grouping

---

## 🔢 Aggregate Functions — Summarizing Data

Instead of seeing every row, sometimes you want **summary statistics**.

| Function | What It Does | Example |
|---|---|---|
| `COUNT(*)` | Count rows | How many students? |
| `SUM(col)` | Add up values | Total revenue? |
| `AVG(col)` | Calculate average | Average GPA? |
| `MIN(col)` | Find the minimum | Lowest price? |
| `MAX(col)` | Find the maximum | Highest salary? |

---

## 🔢 Aggregate Functions — Examples

```sql
-- How many students do we have?
SELECT COUNT(*) AS total_students 
FROM students;

-- What's the average GPA?
SELECT AVG(gpa) AS average_gpa 
FROM students;

-- What are the min and max GPAs?
SELECT MIN(gpa) AS lowest, 
       MAX(gpa) AS highest 
FROM students;
```

---

## 📊 GROUP BY — Aggregating by Category

`GROUP BY` is where the magic happens. It lets you compute aggregate statistics **for each group** in your data.

```sql
SELECT group_column, AGGREGATE(value_column)
FROM table_name
GROUP BY group_column;
```

---

## 📊 GROUP BY Example:

```sql
-- Average GPA broken down by major
SELECT
    major,
    COUNT(*) AS num_students,
    ROUND(AVG(gpa), 2) AS avg_gpa,
    MAX(gpa) AS top_gpa
FROM students
GROUP BY major
ORDER BY avg_gpa DESC;
```

---

## 📊 GROUP BY Example: sample output


| major | num_students | avg_gpa | top_gpa |
|---|---|---|---|
| Computer Science | 2 | 3.80 | 3.9 |
| Mathematics | 2 | 3.60 | 3.8 |
| Physics | 1 | 3.20 | 3.2 |

---

## 🎛️ HAVING — Filtering Groups

`WHERE` filters rows **before** grouping. `HAVING` filters **after** grouping.

```sql
SELECT major, COUNT(*) AS num_students, AVG(gpa) AS avg_gpa
FROM students
GROUP BY major
HAVING COUNT(*) >= 2;   -- Only show majors with 2+ students
```

---

## The order of clauses:

```sql
SELECT   ...
FROM     ...
WHERE    ...    ← Filters ROWS (before grouping)
GROUP BY ...
HAVING   ...    ← Filters GROUPS (after grouping)
ORDER BY ...
LIMIT    ...
```

> 💡 Think of `HAVING` as a `WHERE` clause specifically for groups.

---

<!-- _class: section-break -->

# Part 4
## Joining Tables

---

## 🔗 Why We Need Multiple Tables

In real databases, data is spread across **multiple related tables** to avoid repetition. This is called **normalization**.

**Instead of this (bad — repetitive data):**

| order_id | customer_name | customer_email | product | price |
|---|---|---|---|---|
| 1 | Alice | alice@email.com | Laptop | 999 |
| 2 | Alice | alice@email.com | Mouse | 25 |
| 3 | Bob | bob@email.com | Keyboard | 75 |

**We use two separate tables (good):**
- `customers` (customer_id, name, email)
- `orders` (order_id, customer_id, product, price)

Then we **JOIN** them together when we need combined information.

---

## 🤝 INNER JOIN — The Most Common Join

`INNER JOIN` returns rows where there is a **match in both tables**.

```sql
SELECT customers.name, orders.product, orders.price
FROM orders
INNER JOIN customers
    ON orders.customer_id = customers.customer_id;
```

---

## Visualizing the JOIN:

```
 customers table        orders table
┌────┬───────┐         ┌────┬──────┬─────────┐
│ id │ name  │         │ id │ c_id │ product │
├────┼───────┤   JOIN  ├────┼──────┼─────────┤
│  1 │ Alice │ ◄──────►│  1 │  1   │ Laptop  │
│  2 │ Bob   │ ◄──────►│  2 │  1   │ Mouse   │
│  3 │ Carol │         │  3 │  2   │ Keybd   │
└────┴───────┘         └────┴──────┴─────────┘
                        (Carol has no orders - excluded)
```

---

## 🗂️ Types of JOINs at a Glance

<br>

| JOIN Type | Returns | Use Case |
|---|---|---|
| `INNER JOIN` | Rows matching in **both** tables | Most common — only matched data |
| `LEFT JOIN` | All left rows + matched right | Keep all left, even without a match |
| `RIGHT JOIN` | All right rows + matched left | Keep all right, even without a match |
| `FULL OUTER JOIN` | All rows from both | Everything, matched or not |

---

## 🗂️ LEFT JOIN Example

```sql
-- LEFT JOIN example: 
-- All customers, even if they haven't ordered
--
SELECT customers.name, orders.product
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id;
```

> 🔑 Start with `INNER JOIN`. It covers 80% of real-world cases.

---

<!-- _class: section-break -->

# Part 5
## DuckDB in Python

---

## 🐍 DuckDB + Python — The Setup

```python
# Install (run once in terminal)
# pip install duckdb pandas matplotlib seaborn

import duckdb
import pandas as pd

# Create an in-memory database
con = duckdb.connect()

# Create a table
con.execute("""
    CREATE TABLE students (
        student_id INTEGER,
        name       VARCHAR,
        age        INTEGER,
        major      VARCHAR,
        gpa        DECIMAL(3,2)
    )
""")

# Insert data
con.execute("""
    INSERT INTO students VALUES
    (1, 'Alice Chen',   20, 'Computer Science', 3.9),
    (2, 'Bob Martin',   22, 'Mathematics',      3.4),
    (3, 'Carol White',  21, 'Computer Science', 3.7),
    (4, 'David Lee',    23, 'Physics',          3.2),
    (5, 'Emma Davis',   20, 'Mathematics',      3.8)
""")
```

---

## ⚡ Running Queries from Python

```python
# Method 1: Fetch as a list of tuples
result = con.execute("SELECT * FROM students").fetchall()

# Method 2: Fetch as a Pandas DataFrame (recommended!)
df = con.execute("""
    SELECT major,
           COUNT(*) AS num_students,
           ROUND(AVG(gpa), 2) AS avg_gpa
    FROM students
    GROUP BY major
    ORDER BY avg_gpa DESC
""").df()

print(df)
#             major  num_students  avg_gpa
# 0  Computer Science             2     3.80
# 1      Mathematics             2     3.60
# 2           Physics             1     3.20
```

---

## 🔮 The Superpower: Query CSV Files Directly!

DuckDB can query **raw CSV files** without even loading them first:

```python
import duckdb

# Query a CSV file as if it were a database table!
result = duckdb.sql("""
    SELECT department,
           COUNT(*) AS headcount,
           ROUND(AVG(salary), 0) AS avg_salary
    FROM 'employees.csv'
    GROUP BY department
    ORDER BY avg_salary DESC
""").df()
```

```python
# Even query multiple CSV files at once!
result = duckdb.sql("""
    SELECT * FROM read_csv_auto('data/*.csv')
    WHERE year = 2024
""").df()
```

> 🤯 **Mind = blown.** No need to load into memory first. DuckDB streams through the file intelligently.

---

## 🦆 DuckDB Can Also Query Pandas DataFrames!

```python
import duckdb
import pandas as pd

# Create a Pandas DataFrame
df = pd.DataFrame({
    'city':  ['NYC', 'LA', 'Chicago', 'NYC', 'LA'],
    'sales': [1200, 850, 430, 980, 720]
})

# Query it directly with SQL!
result = duckdb.sql("""
    SELECT city,
           COUNT(*) AS transactions,
           SUM(sales) AS total_sales,
           ROUND(AVG(sales), 0) AS avg_sale
    FROM df
    GROUP BY city
    ORDER BY total_sales DESC
""").df()

print(result)
```

> 🔥 This is a game-changer: use SQL on data you already have in Python — no migration needed!

---

<!-- _class: section-break -->

# 🧪 Hands-On Lab
## Time to Get Your Hands Dirty

---

## 📋 Lab Overview

Open the Jupyter Notebook: **`duckdb_intro_lab.ipynb`**

<div class="two-col">
<div>

**You'll explore 3 real-world datasets:**

🛒 **E-Commerce Orders**
- Products, customers, transactions

🎬 **Movies Database**
- Films, genres, ratings, box office

🏢 **Employee Records**
- Staff, departments, salaries

</div>
<div>

**You'll run queries that:**

✅ Filter with `WHERE`

✅ Sort with `ORDER BY`

✅ Aggregate with `GROUP BY`

✅ Visualize with `matplotlib`

✅ Join two tables with `INNER JOIN`

</div>
</div>

> 🎯 **Goal:** By the end of today, you'll write real SQL queries on real data and produce your first data visualizations!

---

## 🛠️ SQL Cheat Sheet — Keep This Handy!

```sql
-- Full query template (clauses must be in this order)
SELECT   col1, col2, AGG_FUNC(col3) AS alias     -- What to show
FROM     table_name                              -- Where data is
JOIN     other_table ON table.key = other.key    -- Combine tables
WHERE    condition1 AND condition2               -- Filter rows
GROUP BY col1, col2                              -- Group for aggregation
HAVING   AGG_FUNC(col3) > value                  -- Filter groups
ORDER BY col1 DESC, col2 ASC                     -- Sort results
LIMIT    10;                                     -- Cap row count
```

---

## Aggregate functions:

*  `COUNT(*)`
*  `SUM(col)`
*  `AVG(col)`
*  `MIN(col)`
*  `MAX(col)`
*  `ROUND(val, n)`

---

## WHERE operators: 
* `=` 
* `!=` 
*  `>`
*  `<` 
*  `>=`
*  `<=`
*  `BETWEEN`
*  `IN (...)`
*  `LIKE '%pattern%'`
*  `IS NULL`
*  `IS NOT NULL`

---

## Boolean Logic:

* `AND`
* `OR`
* `NOT`

---

## 🎓 Key Takeaways

<div class="two-col">
<div>

**🦆 DuckDB**
- Runs inside Python, zero setup
- Full SQL support
- Reads CSV, JSON, Parquet
- Queries Pandas DataFrames
- Perfect for analytics

**🏛️ Database Fundamentals**
- Tables = rows + typed columns
- Primary keys = unique identifiers
- Normalization = no repetition
- Relationships via foreign keys

</div>
<div>

**📝 SQL Essentials**
- `SELECT` — choose columns
- `FROM` — choose table
- `WHERE` — filter rows
- `ORDER BY` — sort output
- `LIMIT` — cap results
- `GROUP BY` — aggregate
- `HAVING` — filter groups
- `JOIN` — combine tables

</div>
</div>

---

## 🚀 What's Coming Next

| Week | Topic |
|---|---|
| Week 1 | ✅ **Today** — DuckDB, SELECT, WHERE, GROUP BY |
| Week 2 | Advanced JOINs, Subqueries, CTEs |
| Week 3 | Window Functions (RANK, LEAD, LAG, PARTITION BY) |
| Week 4 | Data Modeling & Schema Design |
| Week 5 | Indexing, Query Optimization, EXPLAIN |
| Week 6 | Project — Build a Real Analytical Dashboard |

> 🌟 SQL is one of the **most in-demand skills** in tech, data science, finance, and business. You're making a great investment today.

---

<!-- _class: title-slide -->

# 🦆 You're Ready.

## Open your Jupyter Notebook and run your first SQL query!

<br>

```sql
SELECT 'Hello, World of Data!' AS message;
```

<br>

**Questions?** Raise your hand — no question is too basic.

*Database Management Systems 101 · Day 1*

---

## 📚 Resources & Further Reading

**Official Documentation**
- 🦆 DuckDB Docs: `duckdb.org/docs`
- 📘 SQL Tutorial: `sqlzoo.net`
- 🎓 Mode SQL Tutorial: `mode.com/sql-tutorial`

**Practice Platforms**
- `leetcode.com` — SQL challenges
- `kaggle.com` — Real datasets + notebooks
- `sqlpractice.io` — Interactive SQL exercises

**Books**
- *Learning SQL* — Alan Beaulieu (O'Reilly)
- *SQL Cookbook* — Anthony Molinaro (O'Reilly)
- *Designing Data-Intensive Applications* — Martin Kleppmann *(for later!)*

> 💬 *"The best way to learn SQL is to write SQL. Don't just read — type it out, break it, fix it, explore it."*
