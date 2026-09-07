# OMIS 105 — Week 2 Review Notes: Relational Design & JOINs

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week02_review_notebook.py`. Open the notebook
and teach from it; use these notes for timing, discussion prompts, and the
homework assignment.

---

## My Teaching Philosophy for This Course

These students are business seniors, not CS majors. They will manage people who build databases, write requirements that become schemas, and make decisions based on queried data. Every concept must be grounded in a business scenario they recognize. No abstract theory without a concrete "here's why you'd care about this at work" moment.

I would teach SQL as a *language of questions* — you have business questions, SQL is how you ask a database to answer them. DuckDB running inside Jupyter means zero infrastructure friction: no servers, no configuration files, no passwords, no cloud consoles. Students open a notebook and they're immediately writing SQL against data.

The three weeks build as follows: Week 1 creates confidence ("I can do this"), Week 2 creates competence ("I understand how data is structured"), Week 3 creates capability ("I can answer real business questions with SQL").

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
| 3 | Multi-table orders database (customers, products, sales) | Normalize your Week 1 design into multiple tables |
| 4 | JOINs on the orders database | 6 JOIN queries on your multi-table design |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
