# Mastering DuckDB Self Joins: <br> A Beginner's Guide

A **self join** is a regular join where a table is joined **with itself**.

It sounds strange at first. But it is very useful when the rows of
one table are related to each other. Examples: an org chart
(employee → manager), pairs of coworkers, or today's sales vs.
yesterday's sales.

There is no `SELF JOIN` keyword. You use `INNER JOIN` or `LEFT JOIN`,
exactly as before.

---

## 1. The Key Idea

Treat the one table as if it were **two separate tables**.

You do this by giving the table **two different aliases** (nicknames).
Each alias plays a **role**:

* `e` for the employee
* `m` for the manager

```
   +----------------------------------------------------+
   |                  employees                         |
   +----------------------------------------------------+
            /                                     \
           /                                       \
          ▼                                         ▼
+-----------------+     INNER JOIN      +----------------+
| employees AS e  |     LEFT JOIN       | employees AS m |
| (The Employee)  | <-----------------> |  (The Manager) |
+-----------------+                     +----------------+
```

---

## 2. Sample Table

Our example is a small `employees` table. Each employee has a
`manager_id`. It holds the `emp_id` of their manager, who is **another
row in the same table**.

### Setup Script (DuckDB)

```sql
-- Create the employees table
CREATE OR REPLACE TABLE employees (
    emp_id     INTEGER,
    name       VARCHAR,
    title      VARCHAR,
    salary     INTEGER,
    manager_id INTEGER
);

-- Insert 5 employees
INSERT INTO employees VALUES
    (1, 'Alice',   'CEO',            150000, NULL), -- Alice has no manager (top boss)
    (2, 'Bob',     'Engineering VP', 120000, 1),    -- Bob reports to Alice (1)
    (3, 'Charlie', 'Senior Dev',      95000, 2),    -- Charlie reports to Bob (2)
    (4, 'David',   'Junior Dev',      65000, 2),    -- David reports to Bob (2)
    (5, 'Eve',     'QA Lead',         70000, 1);    -- Eve reports to Alice (1)
```

### The `employees` Table

| emp_id | name    | title          | salary | manager_id |
|-------:|---------|----------------|-------:|-----------:|
| 1      | Alice   | CEO            | 150000 | NULL       |
| 2      | Bob     | Engineering VP | 120000 | 1          |
| 3      | Charlie | Senior Dev     |  95000 | 2          |
| 4      | David   | Junior Dev     |  65000 | 2          |
| 5      | Eve     | QA Lead        |  70000 | 1          |

---

## 3. Three Basic Self Joins

### Basic Example 1: Each Employee and Their Manager (`INNER JOIN`)

**Goal:** Show each employee next to the name of their manager.

```sql
SELECT
    e.name AS employee_name,
    e.title AS employee_title,
    m.name AS manager_name
FROM employees AS e
INNER JOIN employees AS m
    ON e.manager_id = m.emp_id
ORDER BY e.emp_id;
```

**Result (4 rows):**

| employee_name | employee_title | manager_name |
|---------------|----------------|--------------|
| Bob           | Engineering VP | Alice        |
| Charlie       | Senior Dev     | Bob          |
| David         | Junior Dev     | Bob          |
| Eve           | QA Lead        | Alice        |

How it matches:

* Bob's `manager_id` is 1. The row with `emp_id = 1` is Alice.
* Charlie's and David's `manager_id` is 2. The row with `emp_id = 2` is Bob.
* Eve's `manager_id` is 1, so her manager is Alice.

> **Note:** Alice is missing. Her `manager_id` is `NULL`, and `NULL`
> never matches anything. `INNER JOIN` drops rows with no match.

---

### Basic Example 2: Keep Everyone, Even the Top Boss (`LEFT JOIN`)

**Goal:** List **all** employees. If someone has no manager, show a
friendly label instead of `NULL`.

```sql
SELECT
    e.name AS employee_name,
    e.title AS employee_title,
    COALESCE(m.name, 'No Manager (Top Boss)') AS manager_name
FROM employees AS e
LEFT JOIN employees AS m
    ON e.manager_id = m.emp_id
ORDER BY e.emp_id;
```

**Result (5 rows):**

| employee_name | employee_title | manager_name          |
|---------------|----------------|-----------------------|
| Alice         | CEO            | No Manager (Top Boss) |
| Bob           | Engineering VP | Alice                 |
| Charlie       | Senior Dev     | Bob                   |
| David         | Junior Dev     | Bob                   |
| Eve           | QA Lead        | Alice                 |

> **Why it works:** `LEFT JOIN` keeps every row of `e`. For Alice, no
> manager matches, so `m.name` is `NULL`. `COALESCE(a, b)` returns `b`
> when `a` is `NULL`.

---

### Basic Example 3: Coworkers With the Same Manager

**Goal:** Find pairs of employees who report to the same manager.

```sql
SELECT
    e1.name AS employee_1,
    e2.name AS employee_2,
    m.name  AS shared_manager
FROM employees AS e1
INNER JOIN employees AS e2
    ON e1.manager_id = e2.manager_id
   AND e1.emp_id < e2.emp_id   -- no self-pairs, each pair only once
INNER JOIN employees AS m
    ON e1.manager_id = m.emp_id
ORDER BY shared_manager;
```

**Result (2 rows):**

| employee_1 | employee_2 | shared_manager |
|------------|------------|----------------|
| Bob        | Eve        | Alice          |
| Charlie    | David      | Bob            |

* Bob and Eve both report to Alice (`manager_id = 1`).
* Charlie and David both report to Bob (`manager_id = 2`).

> **Why `e1.emp_id < e2.emp_id`?**
> Without it, Charlie is paired with himself (Charlie–Charlie). You
> also get every pair twice: Charlie–David **and** David–Charlie.
> The `<` rule keeps each pair exactly once.

---

## 4. Two Intermediate Self Joins

### Intermediate Example 1: The Manager's Manager (Grand-Manager)

**Goal:** Show each employee, their direct manager, **and** their
manager's manager. To do this, use the same table **three times**.

```sql
SELECT
    e.name  AS employee,
    m.name  AS direct_manager,
    gm.name AS grand_manager
FROM employees AS e
INNER JOIN employees AS m
    ON e.manager_id = m.emp_id
INNER JOIN employees AS gm
    ON m.manager_id = gm.emp_id
ORDER BY e.emp_id;
```

**Result (2 rows):**

| employee | direct_manager | grand_manager |
|----------|----------------|---------------|
| Charlie  | Bob            | Alice         |
| David    | Bob            | Alice         |

* Charlie reports to Bob (2), and Bob reports to Alice (1).
* David reports to Bob (2), and Bob reports to Alice (1).

> **Note:** Alice, Bob, and Eve are missing. Alice has no manager.
> Bob and Eve report to Alice, and Alice has no manager, so they have
> no grand-manager. Each `INNER JOIN` drops rows with no match.

---

### Intermediate Example 2: Employees Who Earn More Than Their Manager

**Goal:** Compare two rows: find employees whose salary is higher
than their manager's salary.

Nobody in our table does this yet. So first, add one new employee:

```sql
-- Frank earns more than his manager, Bob
INSERT INTO employees VALUES
    (6, 'Frank', 'AI Specialist', 135000, 2);
```

> **Heads up:** the table now has 6 rows. If you re-run the earlier
> examples, Frank appears in them too. Re-run the setup script to
> go back to 5 rows.

```sql
SELECT
    e.name   AS employee_name,
    e.salary AS employee_salary,
    m.name   AS manager_name,
    m.salary AS manager_salary,
    e.salary - m.salary AS salary_difference
FROM employees AS e
INNER JOIN employees AS m
    ON e.manager_id = m.emp_id
WHERE e.salary > m.salary
ORDER BY e.emp_id;
```

**Result (1 row):**

| employee_name | employee_salary | manager_name | manager_salary | salary_difference |
|---------------|----------------:|--------------|---------------:|------------------:|
| Frank         | 135000          | Bob          | 120000         | 15000             |

> **Remember:** `ON` decides **which rows belong together**
> (employee + manager). `WHERE` decides **which of those pairs to keep**
> (only the ones where the employee earns more).

---

## 5. Cheat Sheet

| Task | Join pattern | Tip |
|------|--------------|-----|
| **Find the parent row** | `e.manager_id = m.emp_id` | Name aliases after their roles (`e` = employee, `m` = manager). |
| **Find peers / coworkers** | `e1.manager_id = e2.manager_id` | Add `e1.emp_id < e2.emp_id` to avoid self-pairs and duplicate pairs. |
| **Climb the hierarchy** | Chain the joins: `e → m → gm` | Use `LEFT JOIN` to keep rows with missing levels. |
| **Compare two rows** | Join the rows, then `WHERE e.salary > m.salary` | Works for salaries, prices, dates, and more. |

**Always prefix every column** with its alias (`e.name`, `m.name`).
In a self join, every column exists in both copies, so a bare `name`
causes an "ambiguous column" error.

---

## 6. A Complete Second Example: Customer Referrals

Self joins are not only for org charts. Any table where one row
**points to another row** of the same table works the same way.

**The story:** an online store gives a reward when a customer invites
a friend. The store keeps every customer in **one table**,
`customers`. The `referred_by` column holds the `cust_id` of the
customer who invited them. If someone found the store on their own,
`referred_by` is `NULL`.

### Setup Script (DuckDB)

```sql
-- Create the customers table
CREATE OR REPLACE TABLE customers (
    cust_id     INTEGER,
    name        VARCHAR,
    city        VARCHAR,
    join_date   DATE,
    total_spent INTEGER,
    referred_by INTEGER
);

-- Insert 8 customers
INSERT INTO customers VALUES
    (1, 'Maria', 'San Jose',    DATE '2024-01-15', 1200, NULL), -- found the store on her own
    (2, 'Kevin', 'Santa Clara', DATE '2024-02-03',  450, 1),    -- invited by Maria (1)
    (3, 'Priya', 'San Jose',    DATE '2024-02-20', 1800, 1),    -- invited by Maria (1)
    (4, 'Tom',   'Oakland',     DATE '2024-03-11',  300, 2),    -- invited by Kevin (2)
    (5, 'Lina',  'Santa Clara', DATE '2024-03-29',  950, 2),    -- invited by Kevin (2)
    (6, 'Omar',  'San Jose',    DATE '2024-04-05',  700, 3),    -- invited by Priya (3)
    (7, 'Sofia', 'Oakland',     DATE '2024-05-17',  150, NULL), -- found the store on her own
    (8, 'Ben',   'Santa Clara', DATE '2024-06-02',  600, 5);    -- invited by Lina (5)
```

### The `customers` Table

| cust_id | name  | city        | join_date  | total_spent | referred_by |
|--------:|-------|-------------|------------|------------:|------------:|
| 1       | Maria | San Jose    | 2024-01-15 | 1200        | NULL        |
| 2       | Kevin | Santa Clara | 2024-02-03 |  450        | 1           |
| 3       | Priya | San Jose    | 2024-02-20 | 1800        | 1           |
| 4       | Tom   | Oakland     | 2024-03-11 |  300        | 2           |
| 5       | Lina  | Santa Clara | 2024-03-29 |  950        | 2           |
| 6       | Omar  | San Jose    | 2024-04-05 |  700        | 3           |
| 7       | Sofia | Oakland     | 2024-05-17 |  150        | NULL        |
| 8       | Ben   | Santa Clara | 2024-06-02 |  600        | 5           |

### The Two Roles

| Alias | Role | Read it as |
|-------|------|------------|
| `c` | the **customer** | "the person we are talking about" |
| `r` | the **referrer** | "the person who invited `c`" |

The `ON` rule connects them. Read it out loud: *"the customer's
`referred_by` equals the referrer's `cust_id`."*

```sql
ON c.referred_by = r.cust_id
```

---

### Referral Example 1: Who Invited Whom? (`INNER JOIN`)

**Goal:** Show each customer next to the person who invited them.

```sql
SELECT
    c.name AS customer,
    r.name AS referred_by
FROM customers AS c
INNER JOIN customers AS r
    ON c.referred_by = r.cust_id
ORDER BY c.cust_id;
```

**Result (6 rows):**

| customer | referred_by |
|----------|-------------|
| Kevin    | Maria       |
| Priya    | Maria       |
| Tom      | Kevin       |
| Lina     | Kevin       |
| Omar     | Priya       |
| Ben      | Lina        |

> **Note:** Maria and Sofia are missing. Their `referred_by` is
> `NULL`, so `INNER JOIN` finds no match and drops them.

---

### Referral Example 2: Every Customer, With a Label (`LEFT JOIN`)

**Goal:** List **all 8** customers. If nobody invited them, say
*"Signed up on their own"*.

```sql
SELECT
    c.name AS customer,
    c.join_date,
    COALESCE(r.name, 'Signed up on their own') AS referred_by
FROM customers AS c
LEFT JOIN customers AS r
    ON c.referred_by = r.cust_id
ORDER BY c.cust_id;
```

**Result (8 rows):**

| customer | join_date  | referred_by            |
|----------|------------|------------------------|
| Maria    | 2024-01-15 | Signed up on their own |
| Kevin    | 2024-02-03 | Maria                  |
| Priya    | 2024-02-20 | Maria                  |
| Tom      | 2024-03-11 | Kevin                  |
| Lina     | 2024-03-29 | Kevin                  |
| Omar     | 2024-04-05 | Priya                  |
| Sofia    | 2024-05-17 | Signed up on their own |
| Ben      | 2024-06-02 | Lina                   |

---

### Referral Example 3: Who Invited the Most Friends? (`LEFT JOIN` + `GROUP BY`)

**Goal:** For every customer, count how many friends they invited,
and how much those friends spent. Now the referrer `r` is on the
**left**, so we start from every customer and look for the friends
they invited.

```sql
SELECT
    r.name AS customer,
    COUNT(c.cust_id)                AS referrals,
    COALESCE(SUM(c.total_spent), 0) AS spent_by_referrals
FROM customers AS r
LEFT JOIN customers AS c
    ON c.referred_by = r.cust_id
GROUP BY r.cust_id, r.name
ORDER BY referrals DESC, r.cust_id;
```

**Result (8 rows):**

| customer | referrals | spent_by_referrals |
|----------|----------:|-------------------:|
| Maria    | 2         | 2250               |
| Kevin    | 2         | 1250               |
| Priya    | 1         |  700               |
| Lina     | 1         |  600               |
| Tom      | 0         |    0               |
| Omar     | 0         |    0               |
| Sofia    | 0         |    0               |
| Ben      | 0         |    0               |

* Maria invited Kevin and Priya: 450 + 1800 = 2250.
* Kevin invited Tom and Lina: 300 + 950 = 1250.

> **Why `COUNT(c.cust_id)` and not `COUNT(*)`?** Tom invited nobody,
> but `LEFT JOIN` still gives him one row, full of `NULL`s.
> `COUNT(*)` counts that row and says **1**. `COUNT(c.cust_id)` skips
> `NULL`s and correctly says **0**. For the same reason, `SUM` returns
> `NULL` for Tom, and `COALESCE` turns it into 0.

---

### Referral Example 4: Friends Who Spent More Than the Person Who Invited Them

**Goal:** Find customers who spent more than their referrer. These are
the "best" invitations.

```sql
SELECT
    c.name        AS customer,
    c.total_spent AS customer_spent,
    r.name        AS referred_by,
    r.total_spent AS referrer_spent,
    c.total_spent - r.total_spent AS difference
FROM customers AS c
INNER JOIN customers AS r
    ON c.referred_by = r.cust_id
WHERE c.total_spent > r.total_spent
ORDER BY difference DESC;
```

**Result (2 rows):**

| customer | customer_spent | referred_by | referrer_spent | difference |
|----------|---------------:|-------------|---------------:|-----------:|
| Priya    | 1800           | Maria       | 1200           | 600        |
| Lina     |  950           | Kevin       |  450           | 500        |

---

### Referral Example 5: Customers Who Live in the Same City (Pairs)

**Goal:** Pair up every two customers who live in the same city. Both
aliases play the **same role** here, so we call them `a` and `b`.

```sql
SELECT
    a.name AS customer_1,
    b.name AS customer_2,
    a.city
FROM customers AS a
INNER JOIN customers AS b
    ON a.city = b.city
   AND a.cust_id < b.cust_id   -- no self-pairs, each pair only once
ORDER BY a.city, a.cust_id, b.cust_id;
```

**Result (7 rows):**

| customer_1 | customer_2 | city        |
|------------|------------|-------------|
| Tom        | Sofia      | Oakland     |
| Maria      | Priya      | San Jose    |
| Maria      | Omar       | San Jose    |
| Priya      | Omar       | San Jose    |
| Kevin      | Lina       | Santa Clara |
| Kevin      | Ben        | Santa Clara |
| Lina       | Ben        | Santa Clara |

* San Jose and Santa Clara have 3 customers each, so 3 pairs each.
* Oakland has 2 customers, so 1 pair. 3 + 3 + 1 = 7.

> **Notice:** this join does not use `referred_by` at all. A self join
> can match rows on **any** columns they share.

---

### Referral Example 6: The Referral Chain (Three Copies of One Table)

**Goal:** Show each customer, the person who invited them, **and** the
person who invited *that* person. Each join climbs **one step** up
the chain.

```sql
SELECT
    c.name  AS customer,
    r.name  AS referred_by,
    rr.name AS referrers_referrer
FROM customers AS c
INNER JOIN customers AS r
    ON c.referred_by = r.cust_id
INNER JOIN customers AS rr
    ON r.referred_by = rr.cust_id
ORDER BY c.cust_id;
```

**Result (4 rows):**

| customer | referred_by | referrers_referrer |
|----------|-------------|--------------------|
| Tom      | Kevin       | Maria              |
| Lina     | Kevin       | Maria              |
| Omar     | Priya       | Maria              |
| Ben      | Lina        | Kevin              |

* Ben was invited by Lina, and Lina was invited by Kevin.
* Kevin and Priya are missing: they were invited by Maria, and
  nobody invited Maria. Maria and Sofia are missing too: nobody
  invited them.

> **Try it yourself:** change both `INNER JOIN`s to `LEFT JOIN`. You
> should get all 8 customers, with `NULL` where a step is missing.

---

### Same Patterns, New Table

| Pattern | Employees (Sections 3–4) | Customers (Section 6) |
|---------|--------------------------|-----------------------|
| Row → its parent | `e.manager_id = m.emp_id` | `c.referred_by = r.cust_id` |
| Keep rows with no parent | `LEFT JOIN` + `COALESCE` | `LEFT JOIN` + `COALESCE` |
| Compare a row to its parent | `e.salary > m.salary` | `c.total_spent > r.total_spent` |
| Pairs of peers | same `manager_id` + `<` | same `city` + `<` |
| Two steps up | `e → m → gm` | `c → r → rr` |

---

## 7. Next Steps

Practice with the three notebooks in this folder:

* [`self_join_notebook_01_quickstart.py`](self_join_notebook_01_quickstart.py) — quick start, 5 queries
* [`self_join_notebook_02_company.py`](self_join_notebook_02_company.py) — the full lesson, with an org chart, common mistakes, and 6 exercises
* [`self_join_notebook_03_referrals.py`](self_join_notebook_03_referrals.py) — the referral example from Section 6, as live queries, with a referral tree and 4 exercises

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
