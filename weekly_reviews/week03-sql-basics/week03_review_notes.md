# OMIS 105 — Week 3 Review Notes: Aggregation, Grouping & Subqueries

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week03_review_notebook.py`. Open the notebook
and teach from it; use these notes for timing, discussion prompts, and the
homework assignment.

---

## My Teaching Philosophy for This Course

These students are business seniors, not CS majors. They will manage people who build databases, write requirements that become schemas, and make decisions based on queried data. Every concept must be grounded in a business scenario they recognize. No abstract theory without a concrete "here's why you'd care about this at work" moment.

I would teach SQL as a *language of questions* — you have business questions, SQL is how you ask a database to answer them. DuckDB running inside Jupyter means zero infrastructure friction: no servers, no configuration files, no passwords, no cloud consoles. Students open a notebook and they're immediately writing SQL against data.

The three weeks build as follows: Week 1 creates confidence ("I can do this"), Week 2 creates competence ("I understand how data is structured"), Week 3 creates capability ("I can answer real business questions with SQL").

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
| 5 | GROUP BY / HAVING on the normalized orders database | 8 aggregation queries |
| 6 | Subqueries + comprehensive review | Mini-project: 3-table database + 10 queries |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
