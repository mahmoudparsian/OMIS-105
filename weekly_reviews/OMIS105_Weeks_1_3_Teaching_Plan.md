# OMIS 105 — Teaching Plan: Weeks 1–3 (6 Lectures)

**Course:** OMIS 105 — Introduction to Database Management Systems  
**Audience:** Senior undergraduate business students (SCU Leavey School of Business)  
**Quarter:** Fall 2026  
**Substitute Instructor:** Claude (standing in for Dr. Mahmoud Parsian)  
**Tech Stack:** Python + DuckDB + Jupyter Notebook  

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

## Week 2: Relational Thinking — Connecting Tables

### Lecture 3 (2 hours): Why One Table Isn't Enough

**Goal:** Students understand *why* we split data into multiple tables and what problems that solves.

**Hour 1 — The Problem of Redundancy**

I'd start with a deliberately bad design. Show a single flat table for a company's orders:

| order_id | customer_name | customer_email | customer_city | product | price | order_date |
|----------|--------------|----------------|---------------|---------|-------|-----------|
| 1 | Alice | alice@email.com | San Jose | Laptop | 999 | 2025-01-15 |
| 2 | Alice | alice@email.com | San Jose | Mouse | 29 | 2025-01-16 |
| 3 | Alice | alice@email.com | San Jose | Keyboard | 79 | 2025-02-01 |
| 4 | Bob | bob@email.com | Santa Clara | Laptop | 999 | 2025-02-10 |

Then ask: "What's wrong with this?" Let them discover the problems:

- **Redundancy:** Alice's name, email, and city are repeated 3 times. If she moves, you have to update 3 rows. Miss one? Now your data is inconsistent.
- **Update anomalies:** Change Alice's email in row 1 but forget rows 2 and 3 — which email is correct?
- **Deletion anomaly:** If Bob returns his laptop and we delete row 4, we lose all knowledge that Bob exists.
- **Insertion anomaly:** We can't add a new customer until they place an order.

I'd name these formally — "These are called *anomalies*, and they're the #1 reason we split data into multiple related tables." This is the motivation for the relational model.

Then I'd show the fix — three tables:

**customers:** customer_id, name, email, city  
**products:** product_id, name, price  
**orders:** order_id, customer_id, product_id, order_date

And introduce the *foreign key*: `customer_id` in the orders table *refers to* `customer_id` in the customers table. It's a link. A relationship. This is why it's called a *relational* database.

I'd use a visual — draw the three tables on the board with arrows showing the foreign key relationships. This is an Entity-Relationship (ER) picture, and I'd keep it informal: "boxes are tables, arrows are relationships."

**Hour 2 — Build It in DuckDB**

Live-code the three-table design together:

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name        VARCHAR NOT NULL,
    email       VARCHAR,
    city        VARCHAR
);

CREATE TABLE products (
    product_id  INTEGER PRIMARY KEY,
    name        VARCHAR NOT NULL,
    price       DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    product_id  INTEGER REFERENCES products(product_id),
    order_date  DATE NOT NULL
);
```

Insert 5 customers, 6 products, 10–12 orders. Then show that we can query each table independently (`SELECT * FROM customers`), but the real power is *combining* them — which leads directly into Lecture 4.

I'd end with a teaser: "Right now, the orders table shows customer_id 1 bought product_id 3. But who is customer 1? What is product 3? Next class, you'll learn JOIN — the SQL command that reconnects these tables to answer real questions."

**Homework 3:** Take your single-table design from Homework 2 and *normalize* it — split it into 2 or 3 related tables with foreign keys. Create the tables in a notebook, insert data, and show `SELECT *` from each table. Write a paragraph explaining why you split the data the way you did.

---

### Lecture 4 (2 hours): JOINs — Reconnecting the Pieces

**Goal:** Students can write INNER JOIN and LEFT JOIN queries to combine tables and answer multi-table business questions.

**Hour 1 — INNER JOIN**

I'd pick up exactly where Lecture 3 ended: "We have customers, products, and orders in separate tables. Now a manager asks: *Show me every order with the customer name and product name.* How?"

Introduce JOIN as the answer — it's how SQL reconnects related tables:

```sql
SELECT o.order_id,
       c.name AS customer,
       p.name AS product,
       p.price,
       o.order_date
FROM   orders o
JOIN   customers c ON o.customer_id = c.customer_id
JOIN   products p  ON o.product_id  = p.product_id
ORDER BY o.order_date
```

I'd break this down slowly:

- `FROM orders o` — start with the orders table, give it a short alias `o`
- `JOIN customers c ON o.customer_id = c.customer_id` — for each order, find the matching customer
- `JOIN products p ON o.product_id = p.product_id` — for each order, find the matching product
- The ON clause is the *matching rule* — it tells SQL which rows to connect

Then run it and show: "Now instead of customer_id 1, you see 'Alice'. Instead of product_id 3, you see 'Keyboard'. The JOIN filled in the names."

I'd do several business questions as live examples:

- "How much did each customer spend in total?" (JOIN + GROUP BY + SUM)
- "Which products have never been ordered?" (this naturally introduces LEFT JOIN)
- "Show all orders from San Jose customers" (JOIN + WHERE)

**Hour 2 — LEFT JOIN & Practice**

The "products never ordered" question is the perfect transition. INNER JOIN only returns rows that match in both tables. If a product has zero orders, it disappears. LEFT JOIN keeps *everything* from the left table, filling in NULLs where there's no match:

```sql
SELECT p.name, COUNT(o.order_id) AS times_ordered
FROM   products p
LEFT JOIN orders o ON p.product_id = o.product_id
GROUP BY p.name
ORDER BY times_ordered
```

Products with zero orders show `0` instead of vanishing. I'd emphasize this is one of the most common real-world needs: "Show me *all* customers, even those who haven't bought anything yet."

Then I'd give them practice time with progressively harder queries. I'd have 8–10 business questions prepared and let them work in pairs:

1. List all orders with customer and product details
2. Find the total revenue per customer
3. Which customer placed the most orders?
4. Which products were ordered more than once?
5. Show all customers who have NOT placed any orders (LEFT JOIN + WHERE IS NULL)
6. What is the average order value per city?

**Homework 4:** Using the multi-table design from Homework 3, write 6 JOIN queries that answer business questions. At least 2 must use LEFT JOIN. Each query must have a comment above it stating the business question in plain English.

---

## Week 3: SQL Power — Aggregation, Grouping, and Subqueries

### Lecture 5 (2 hours): GROUP BY, HAVING, and Aggregate Functions

**Goal:** Students can summarize data by categories and filter those summaries — the core of business reporting.

**Hour 1 — GROUP BY & Aggregate Functions**

I'd start with a new dataset for this week — an employees table with 20 rows across multiple departments, with salary, gender, hire_date, and city. Richer data means richer questions.

Motivation: "Your VP of Sales asks: *What's the average salary in each department?* You can't answer this with WHERE — WHERE filters individual rows. You need to *group* rows by department and *aggregate* within each group."

Build up the concept step by step:

```sql
-- Step 1: Just the raw data
SELECT department, salary FROM employees

-- Step 2: Group by department
SELECT department, AVG(salary) AS avg_salary
FROM   employees
GROUP BY department

-- Step 3: Add more aggregates
SELECT department,
       COUNT(*)        AS num_employees,
       ROUND(AVG(salary), 0) AS avg_salary,
       MIN(salary)     AS min_salary,
       MAX(salary)     AS max_salary
FROM   employees
GROUP BY department
ORDER BY avg_salary DESC
```

I'd run each step so they can see the transformation: raw rows → grouped summaries. The key insight: "GROUP BY collapses many rows into one row per group. The aggregate functions (COUNT, AVG, MIN, MAX, SUM) tell SQL *how* to collapse them."

Then layer on GROUP BY with multiple columns:

```sql
SELECT department, gender, 
       COUNT(*) AS count,
       ROUND(AVG(salary), 0) AS avg_salary
FROM   employees
GROUP BY department, gender
ORDER BY department, gender
```

"Now you're cross-tabulating — average salary by department AND gender. This is the kind of analysis that drives HR decisions."

**Hour 2 — HAVING & Combined Queries**

Introduce the problem: "Show me only departments where the average salary exceeds $150,000." Students will instinctively try WHERE:

```sql
-- This FAILS:
SELECT department, AVG(salary) AS avg_salary
FROM   employees
WHERE  AVG(salary) > 150000   -- ERROR!
GROUP BY department
```

Explain *why* it fails: WHERE runs *before* grouping — it filters individual rows. HAVING runs *after* grouping — it filters groups. This is a critical conceptual distinction.

```sql
-- This WORKS:
SELECT department, AVG(salary) AS avg_salary
FROM   employees
GROUP BY department
HAVING AVG(salary) > 150000
ORDER BY avg_salary DESC
```

I'd draw the SQL execution order on the board:

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

"This is the order SQL actually processes your query. Understanding this order explains *why* WHERE can't see AVG(salary) but HAVING can."

Then combine everything — queries that use WHERE, GROUP BY, HAVING, and ORDER BY together:

```sql
-- For employees hired after 2023, show departments 
-- with more than 3 employees, sorted by headcount
SELECT   department, COUNT(*) AS headcount
FROM     employees
WHERE    hire_date >= '2023-01-01'
GROUP BY department
HAVING   COUNT(*) > 3
ORDER BY headcount DESC
```

Walk through each clause's role: WHERE filters the rows first, GROUP BY groups what's left, HAVING filters the groups, ORDER BY sorts the final result.

**Homework 5:** Using the 20-employee dataset from class, write 8 queries: 4 using GROUP BY with different aggregate functions, 2 using HAVING, and 2 that combine WHERE + GROUP BY + HAVING. Each query must be preceded by a comment stating the business question.

---

### Lecture 6 (2 hours): Subqueries, Review & Looking Ahead

**Goal:** Students can use subqueries to answer complex questions, and consolidate everything from Weeks 1–3.

**Hour 1 — Subqueries**

Motivation: "Who earns more than the company average?" You can't do this in one simple query because you need to compute the average first, then compare each employee to it. This is where subqueries come in — a query inside a query:

```sql
SELECT name, department, salary
FROM   employees
WHERE  salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC
```

"The inner query computes the average. The outer query uses that number to filter. SQL runs the inner query first, gets a number, then plugs it into the outer query."

Then show subqueries in different positions:

**In WHERE (most common):**
```sql
-- Employees in the department with the highest average salary
SELECT name, department, salary
FROM   employees
WHERE  department = (
    SELECT   department
    FROM     employees
    GROUP BY department
    ORDER BY AVG(salary) DESC
    LIMIT    1
)
```

**In FROM (derived table):**
```sql
-- Compare each department's avg salary to the company avg
SELECT dept_stats.department,
       dept_stats.avg_salary,
       (SELECT ROUND(AVG(salary),0) FROM employees) AS company_avg
FROM (
    SELECT   department, ROUND(AVG(salary),0) AS avg_salary
    FROM     employees
    GROUP BY department
) AS dept_stats
ORDER BY dept_stats.avg_salary DESC
```

I'd emphasize: "Subqueries let you answer *two-step questions*. Whenever a business question sounds like 'compared to...' or 'among those that...' or 'the ones where X is the highest,' you're probably looking at a subquery."

**Hour 2 — Comprehensive Review & Wrap-Up**

I'd run a live "business analyst challenge" — present 6–8 business questions of increasing difficulty and have students write the SQL in their notebooks. Work in pairs, we discuss each answer together.

Example progression:

1. "List all employees sorted by salary descending" (basic SELECT + ORDER BY)
2. "Show only AI department employees earning above $180K" (WHERE with AND)
3. "How many employees are in each department?" (GROUP BY + COUNT)
4. "Which departments have an average salary above $160K?" (GROUP BY + HAVING)
5. "Show each employee alongside their department's average salary" (subquery in SELECT)
6. "Which employees earn above their own department's average?" (correlated subquery or JOIN to derived table)
7. "For each department, show the employee with the highest salary" (subquery + JOIN)
8. "Rank all employees by salary within their department" (preview of window functions — Week 4 material)

For question 8, I'd show the answer but say: "This uses something called a *window function*. We're not covering it today, but this is where the course goes next. You now have the foundation to understand it."

**Closing: What You've Learned in 3 Weeks**

I'd close by mapping what they've learned back to business reality:

| Week | What You Learned | Business Equivalent |
|------|-----------------|-------------------|
| 1 | CREATE, INSERT, SELECT, WHERE, ORDER BY | Defining and querying a single dataset |
| 2 | Multi-table design, PRIMARY KEY, FOREIGN KEY, JOIN | Modeling real business relationships without redundancy |
| 3 | GROUP BY, HAVING, Subqueries | Business reporting, summaries, comparative analysis |

"Three weeks ago, you'd never written SQL. Now you can design a multi-table database, load it with data, and answer complex business questions by combining JOINs, aggregation, and subqueries. That's a real, marketable skill."

**Homework 6 (Mini-Project):** Design a 3-table database for a business scenario of your choice. Create it in a Jupyter notebook, populate it with realistic data (at least 10 rows per table), and write 10 queries that answer real business questions. The queries must include: at least 2 JOINs, at least 2 GROUP BY with aggregates, at least 1 HAVING, and at least 1 subquery. Write each business question in plain English as a comment above the SQL.

---

## Summary of Deliverables per Lecture

| Lecture | Notebook Used in Class | Homework |
|---------|----------------------|----------|
| 1 | Software setup + My_Very_First_DuckDB_Notebook | Add rows, write 3 queries |
| 2 | Design a table from scratch (bookstore example) | Design your own table, 5 queries |
| 3 | Multi-table orders database (customers, products, orders) | Normalize your HW2 design into multiple tables |
| 4 | JOINs on the orders database | 6 JOIN queries on your multi-table design |
| 5 | GROUP BY/HAVING on 20-employee dataset | 8 aggregation queries |
| 6 | Comprehensive review + subqueries | Mini-project: 3-table database + 10 queries |

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
