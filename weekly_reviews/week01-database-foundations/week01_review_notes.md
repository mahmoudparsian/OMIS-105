# OMIS 105 — Week 1 Review Notes: Querying a Single Table

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week01_review_notebook.py`. Open the notebook
and teach from it; use these notes for timing, discussion prompts, and the
homework assignment.

---

## My Teaching Philosophy for This Course

These students are business seniors, not CS majors. They will manage people who build databases, write requirements that become schemas, and make decisions based on queried data. Every concept must be grounded in a business scenario they recognize. No abstract theory without a concrete "here's why you'd care about this at work" moment.

I would teach SQL as a *language of questions* — you have business questions, SQL is how you ask a database to answer them. DuckDB running inside Jupyter means zero infrastructure friction: no servers, no configuration files, no passwords, no cloud consoles. Students open a notebook and they're immediately writing SQL against data.

The three weeks build as follows: Week 1 creates confidence ("I can do this"), Week 2 creates competence ("I understand how data is structured"), Week 3 creates capability ("I can answer real business questions with SQL").

---

## Week 1: Foundations — Why Databases Matter to You

### Lecture 1 (2 hours): The World Runs on Databases

**Goal:** Students leave understanding *why* databases exist, *what problem they solve*, and have DuckDB running on their laptops.

**Hour 1 — Motivation & Big Picture (no laptops yet)**

I would open with a question, not a lecture: "How many of you have used a spreadsheet?" Every hand goes up. "How many have had a spreadsheet break — wrong formula, someone deleted a row, two people editing at once?" Most hands stay up. That's the hook.

From there I'd walk through three real business scenarios:

*Scenario 1 — The Retail Chain.* You manage 200 stores. Each store has thousands of products, daily transactions, employee schedules, and supplier contracts. Could you run this in Excel? Technically yes — but you'd have hundreds of spreadsheets, no way to connect them, no way to ensure consistency, and no way for 50 managers to work simultaneously without stepping on each other. This is why databases exist.

*Scenario 2 — The Registration System.* Right here at SCU, when you enrolled in this class, a database checked prerequisites, seat availability, time conflicts, and your student record — all in milliseconds. Imagine doing that with spreadsheets.

*Scenario 3 — The Coffee Shop.* Even a small business has customers, orders, products, inventory, and suppliers. The moment you want to answer "which product sold the most last month?" across all of that, you need structured data and a language to query it.

I'd then introduce the key vocabulary — *database*, *table*, *row*, *column*, *schema*, *query* — but always by analogy to things they already know: a table is like a well-organized spreadsheet tab, a row is one record, a column is one attribute, a schema is the structure you define up front so the data stays clean.

I would also briefly cover *why DuckDB*: it runs inside Python with no server setup, it speaks standard SQL, it's fast enough for real analytical work, and companies like MotherDuck and various data teams actually use it in production. They're learning a real tool, not a toy.

**Hour 2 — Software Setup & First Query (laptops open)**

This is where we use the software installation kit: `Install_Python_Mac.md` or `Install_Python_Windows.md`, then `2.Setup_Software.py`, then `3.Setup_Verification.ipynb`. I'd budget a full 30–40 minutes for this because there are always a few students with PATH issues, Windows Store Python, or permission errors. I'd have a TA circulate.

Once everyone has Jupyter running, we open `My_Very_First_DuckDB_Notebook.ipynb` together. I'd live-code alongside them, explaining each cell:

- `import duckdb` — we're loading the database engine
- `con = duckdb.connect(database=':memory:')` — we're creating a database that lives in memory
- `CREATE TABLE students (...)` — we're defining the structure
- `INSERT INTO students VALUES (...)` — we're adding data
- `SELECT * FROM students` — "show me everything"

The magic moment is when they run that first `SELECT *` and see a table appear. That's the "I can do this" moment. I'd let them experiment: "Change the WHERE clause. Try `ORDER BY gpa DESC`. What happens if you type `LIMIT 3`?"

**Homework 1:** Modify the notebook — add 5 more students to the table, write 3 queries of your own (one with WHERE, one with ORDER BY, one with both). Submit the notebook.

---

### Lecture 2 (2 hours): Data Types, Schemas, and Your First Table Design

**Goal:** Students understand that *how you structure data matters*, and they can design a simple table from a business description.

**Hour 1 — Data Types & Schema Design**

I'd start with a flawed example. Show a "spreadsheet" where someone stored dates as text ("Jan 15", "1/15/25", "January 15, 2025" — three formats in one column), prices as text with dollar signs ("$29.99"), and quantities sometimes as text ("twelve"). Ask the class: what goes wrong when you try to sort by date? Sum the prices? Count inventory?

This motivates *data types*. I'd cover the essential ones, keeping it to what business students need:

| Type | When You Use It | Example |
|------|----------------|---------|
| INTEGER | Whole numbers — IDs, counts, quantities | `emp_id INTEGER` |
| DECIMAL(p,s) | Money, precise numbers | `price DECIMAL(10,2)` |
| VARCHAR | Text — names, descriptions, categories | `name VARCHAR` |
| DATE | Calendar dates | `hire_date DATE` |
| BOOLEAN | Yes/no flags | `is_active BOOLEAN` |

Then I'd introduce constraints — `PRIMARY KEY` (every row needs a unique ID), `NOT NULL` (this field can never be blank), and briefly mention `FOREIGN KEY` (we'll dig deep into this in Week 2). The framing: constraints are *rules you build into the structure* so bad data can't sneak in. It's like data quality enforcement that runs automatically.

I'd do a live design exercise with the class. Business scenario: "You're building a database for a small online bookstore. What tables do you need? What columns?" We'd work through it together on the board:

- What information do we need about each book? (title, author, price, genre, publication_year, stock_quantity)
- What's the primary key? (book_id — and why not title? Because two books could have the same title)
- What data type for each column? (price is DECIMAL, not VARCHAR — why?)

Then they'd build it in Jupyter:

```sql
CREATE TABLE books (
    book_id    INTEGER PRIMARY KEY,
    title      VARCHAR NOT NULL,
    author     VARCHAR NOT NULL,
    genre      VARCHAR,
    price      DECIMAL(8,2) NOT NULL,
    pub_year   INTEGER,
    in_stock   INTEGER DEFAULT 0
)
```

**Hour 2 — Hands-On: Build, Populate, Query**

Students insert 10–15 books into their table and write queries:

- "Show all books by a specific author"
- "Which books cost more than $20?"
- "List books published after 2020, sorted by price"
- "How many books are in each genre?" (their first GROUP BY — I'd introduce it gently here)

I'd emphasize the *pattern* they're learning: CREATE → INSERT → SELECT. Every database interaction follows this rhythm: define the structure, put data in, ask questions.

I'd close with a comparison: "Look at what you just did. You designed a data model, enforced rules on it, loaded data, and asked four different business questions — all in about 20 lines of SQL. In Excel, you'd have no schema enforcement, no query language, and the 'genre count' question would require a pivot table or COUNTIF formula."

**Homework 2:** Design a table for a business of your choice (restaurant menu, gym members, product inventory — anything). Create it in a notebook with at least 10 rows and write 5 queries that answer realistic business questions. Include comments explaining what each query does.

---

## Teaching Principles I'd Follow

**1. Business first, syntax second.** Every SQL concept is introduced with a business question that motivates it. "Your manager asks..." comes before "the syntax is..."

**2. Live coding, not slides.** I'd spend maybe 10% of class time on slides/board and 90% in Jupyter. Students learn SQL by writing SQL, not by reading about it. I type, they type along, then they experiment on their own.

**3. Errors are learning.** When a query fails, I'd resist the urge to immediately fix it. "Look at the error message. What is it telling us? WHERE can't use AVG — why not?" Debugging is a skill.

**4. Pair work for practice.** During hands-on portions, students work in pairs. One types, one navigates. Switch halfway. Business professionals rarely work alone, and explaining SQL to a peer solidifies understanding.

**5. Spiral, don't stack.** Each lecture revisits previous concepts in a new context. Lecture 5 uses GROUP BY, but also requires WHERE and ORDER BY from Week 1. Homework 6 requires everything from all 6 lectures. Knowledge compounds.

**6. Keep the schema small.** Resist the urge to build 10-table databases. 2–3 tables with 10–20 rows each is enough to teach any concept. Students get lost in big schemas. Clarity beats complexity.

**7. Name things well.** Column names like `emp_id`, `customer_name`, `order_date` are self-documenting. Never use `col1`, `x`, `temp`. Business students especially need readable schemas because they think in business terms, not abstractions.

**8. Show the output.** Every query must be run immediately after writing it. The feedback loop of "write SQL → see result → understand" is the core learning mechanism. Pre-computed outputs in notebooks let students see expected results even if their setup has issues.

---

*Prepared for Dr. Mahmoud Parsian — OMIS 105, Fall 2026*

---

## Deliverables

| Lecture | In Class | Homework |
|---------|----------|----------|
| 1 | Software setup + My_Very_First_DuckDB_Notebook | Add rows, write 3 queries |
| 2 | Design a table from scratch (bookstore example) | Design your own table, 5 queries |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
