import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb
    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Weeks 7 & 8 Review

    ## Window Functions · Query Performance · Transactions · ACID

    **Dataset: CloudMetrics SaaS** — A software-as-a-service company
    that sells analytics tools to businesses. 10 customers across
    8 industries, 3 subscription plans, 25 payment records, and
    15 support tickets.

    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Setting Up the Database

    We create five tables that model a SaaS business:

    - **plans** — three subscription tiers (Starter, Professional, Enterprise)
    - **customers** — 10 companies, each on one plan
    - **payments** — 25 monthly payment records (completed, failed, or refunded)
    - **support_tickets** — 15 support requests with priority and category
    - **accounts** — account balances for transaction exercises (Week 8)
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Create the plans table (3 subscription tiers)
        CREATE OR REPLACE TABLE plans AS
        SELECT * FROM (VALUES
            (1, 'Starter',       29.99),
            (2, 'Professional',  79.99),
            (3, 'Enterprise',   149.99)
        ) AS t(plan_id, plan_name, monthly_price);
        """
    )
    return


@app.cell
def _(mo, plans):
    _df = mo.sql(
        f"""
        SELECT * FROM plans ORDER BY plan_id;
        """
    )
    return


@app.cell
def _(mo, plans):
    _df = mo.sql(
        f"""
        -- Create the customers table (10 companies)
        CREATE OR REPLACE TABLE customers AS
        SELECT * FROM (VALUES
            (1,  'Acme Corp',           'Manufacturing', '2025-01-15'::DATE, 2),
            (2,  'Bright Ideas',        'Marketing',     '2025-02-01'::DATE, 1),
            (3,  'ClearView Analytics', 'Finance',       '2025-01-10'::DATE, 3),
            (4,  'DataFlow Inc',        'Technology',    '2025-03-01'::DATE, 2),
            (5,  'EcoGreen Solutions',  'Energy',        '2025-02-15'::DATE, 1),
            (6,  'Falcon Logistics',    'Logistics',     '2025-01-20'::DATE, 3),
            (7,  'GrowthLab',           'Marketing',     '2025-03-10'::DATE, 2),
            (8,  'Harbor Health',       'Healthcare',    '2025-02-01'::DATE, 3),
            (9,  'Innovate AI',         'Technology',    '2025-04-01'::DATE, 1),
            (10, 'JetStream Media',     'Media',         '2025-03-15'::DATE, 2)
        ) AS t(customer_id, company_name, industry, signup_date, plan_id);
        """
    )
    return


@app.cell
def _(customers, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM customers ORDER BY customer_id;
        """
    )
    return


@app.cell
def _(customers, mo):
    _df = mo.sql(
        f"""
        -- Create the payments table (25 records)
        CREATE OR REPLACE TABLE payments AS
        SELECT * FROM (VALUES
            (101, 1, '2025-02-01'::DATE, 79.99,  'completed'),
            (102, 1, '2025-03-01'::DATE, 79.99,  'completed'),
            (103, 1, '2025-04-01'::DATE, 79.99,  'completed'),
            (104, 2, '2025-03-01'::DATE, 29.99,  'completed'),
            (105, 2, '2025-04-01'::DATE, 29.99,  'completed'),
            (106, 3, '2025-02-01'::DATE, 149.99, 'completed'),
            (107, 3, '2025-03-01'::DATE, 149.99, 'completed'),
            (108, 3, '2025-04-01'::DATE, 149.99, 'completed'),
            (109, 3, '2025-05-01'::DATE, 149.99, 'completed'),
            (110, 4, '2025-04-01'::DATE, 79.99,  'completed'),
            (111, 4, '2025-05-01'::DATE, 79.99,  'failed'),
            (112, 5, '2025-03-01'::DATE, 29.99,  'completed'),
            (113, 5, '2025-04-01'::DATE, 29.99,  'completed'),
            (114, 5, '2025-05-01'::DATE, 29.99,  'refunded'),
            (115, 6, '2025-02-01'::DATE, 149.99, 'completed'),
            (116, 6, '2025-03-01'::DATE, 149.99, 'completed'),
            (117, 6, '2025-04-01'::DATE, 149.99, 'completed'),
            (118, 6, '2025-05-01'::DATE, 149.99, 'completed'),
            (119, 7, '2025-04-01'::DATE, 79.99,  'completed'),
            (120, 7, '2025-05-01'::DATE, 79.99,  'completed'),
            (121, 8, '2025-03-01'::DATE, 149.99, 'completed'),
            (122, 8, '2025-04-01'::DATE, 149.99, 'completed'),
            (123, 8, '2025-05-01'::DATE, 149.99, 'completed'),
            (124, 9, '2025-05-01'::DATE, 29.99,  'completed'),
            (125, 10,'2025-04-01'::DATE, 79.99,  'completed')
        ) AS t(payment_id, customer_id, payment_date, amount, status);
        """
    )
    return


@app.cell
def _(mo, payments):
    _df = mo.sql(
        f"""
        SELECT * FROM payments ORDER BY payment_id;
        """
    )
    return


@app.cell
def _(customers, mo):
    _df = mo.sql(
        f"""
        -- Create the support_tickets table (15 tickets)
        CREATE OR REPLACE TABLE support_tickets AS
        SELECT * FROM (VALUES
            (501, 1,  '2025-02-10'::DATE, '2025-02-11'::DATE, 'low',      'billing'),
            (502, 2,  '2025-03-05'::DATE, '2025-03-05'::DATE, 'medium',   'login'),
            (503, 3,  '2025-02-20'::DATE, '2025-02-22'::DATE, 'high',     'data'),
            (504, 3,  '2025-04-15'::DATE, NULL,                'high',     'performance'),
            (505, 4,  '2025-04-10'::DATE, '2025-04-10'::DATE, 'low',      'feature'),
            (506, 5,  '2025-03-20'::DATE, '2025-03-21'::DATE, 'medium',   'billing'),
            (507, 6,  '2025-02-05'::DATE, '2025-02-06'::DATE, 'low',      'login'),
            (508, 6,  '2025-05-01'::DATE, '2025-05-03'::DATE, 'high',     'data'),
            (509, 7,  '2025-04-20'::DATE, '2025-04-21'::DATE, 'medium',   'feature'),
            (510, 8,  '2025-03-15'::DATE, '2025-03-16'::DATE, 'high',     'performance'),
            (511, 8,  '2025-04-25'::DATE, NULL,                'critical', 'data'),
            (512, 9,  '2025-05-05'::DATE, '2025-05-05'::DATE, 'low',      'login'),
            (513, 10, '2025-04-05'::DATE, '2025-04-07'::DATE, 'medium',   'billing'),
            (514, 1,  '2025-04-12'::DATE, '2025-04-13'::DATE, 'medium',   'feature'),
            (515, 5,  '2025-05-10'::DATE, '2025-05-11'::DATE, 'high',     'login')
        ) AS t(ticket_id, customer_id, created_date, resolved_date, priority, category);
        """
    )
    return


@app.cell
def _(mo, support_tickets):
    _df = mo.sql(
        f"""
        SELECT * FROM support_tickets ORDER BY ticket_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Part 1: Window Functions (Week 7)

    A **window function** computes a value for each row using a
    "window" of related rows — without collapsing the result into
    one row per group (like GROUP BY does).

    Every window function needs an `OVER(...)` clause:
    - `ORDER BY` — how to sort the window
    - `PARTITION BY` — how to divide rows into groups
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.1 ROW_NUMBER() — Number All Customers by Signup Date

    `ROW_NUMBER()` assigns a unique sequential number to each row.
    """)
    return


@app.cell
def _(customers, mo):
    _df = mo.sql(
        f"""
        -- Number customers by signup date (earliest = 1)
        SELECT customer_id,
               company_name,
               signup_date,
               ROW_NUMBER() OVER (ORDER BY signup_date) AS signup_rank
        FROM   customers
        ORDER BY signup_rank;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.2 ROW_NUMBER() with PARTITION BY

    Number payments within each customer (payment 1, 2, 3... per customer).
    """)
    return


@app.cell
def _(customers, mo, payments):
    _df = mo.sql(
        f"""
        -- Number each customer's payments in chronological order
        SELECT c.company_name,
               p.payment_date,
               p.amount,
               p.status,
               ROW_NUMBER() OVER (
                   PARTITION BY p.customer_id
                   ORDER BY p.payment_date
               ) AS payment_num
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        ORDER BY c.company_name, payment_num;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.3 RANK() — Rank Customers by Total Revenue

    `RANK()` is like `ROW_NUMBER()`, but ties get the same rank
    and the next rank is skipped.
    """)
    return


@app.cell
def _(customers, mo, payments):
    _df = mo.sql(
        f"""
        -- Rank customers by total completed payments
        SELECT c.company_name,
               SUM(p.amount) AS total_paid,
               RANK() OVER (ORDER BY SUM(p.amount) DESC) AS revenue_rank
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        WHERE  p.status = 'completed'
        GROUP BY c.company_name
        ORDER BY revenue_rank;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.4 ROW_NUMBER vs RANK — Side by Side

    Notice: when two customers have the same total, RANK gives
    them the same number. ROW_NUMBER always gives unique numbers.
    """)
    return


@app.cell
def _(customers, mo, payments):
    _df = mo.sql(
        f"""
        -- Compare ROW_NUMBER and RANK
        SELECT c.company_name,
               COUNT(*)    AS num_payments,
               ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS row_num,
               RANK()       OVER (ORDER BY COUNT(*) DESC) AS rank_num
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        WHERE  p.status = 'completed'
        GROUP BY c.company_name
        ORDER BY row_num;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.5 AVG() OVER PARTITION BY — Compare Each Payment to Plan Average

    For each payment, show the average payment for that plan
    right next to it. No GROUP BY needed.
    """)
    return


@app.cell
def _(customers, mo, payments, plans):
    _df = mo.sql(
        f"""
        -- Each payment vs its plan's average
        SELECT c.company_name,
               pl.plan_name,
               p.amount,
               ROUND(AVG(p.amount) OVER (PARTITION BY c.plan_id), 2)
                   AS plan_avg,
               ROUND(p.amount - AVG(p.amount) OVER (PARTITION BY c.plan_id), 2)
                   AS diff_from_avg
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        JOIN   plans pl     ON c.plan_id    = pl.plan_id
        WHERE  p.status = 'completed'
        ORDER BY pl.plan_name, c.company_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.6 Top-2 Paying Customers Per Plan

    Use `ROW_NUMBER()` inside a subquery to find the top-2
    customers by total revenue within each plan.
    """)
    return


@app.cell
def _(customers, mo, payments, plans):
    _df = mo.sql(
        f"""
        -- Top 2 customers per plan by total revenue
        SELECT plan_name, company_name, total_paid, rn
        FROM (
            SELECT pl.plan_name,
                   c.company_name,
                   SUM(p.amount) AS total_paid,
                   ROW_NUMBER() OVER (
                       PARTITION BY c.plan_id
                       ORDER BY SUM(p.amount) DESC
                   ) AS rn
            FROM   payments p
            JOIN   customers c ON p.customer_id = c.customer_id
            JOIN   plans pl     ON c.plan_id    = pl.plan_id
            WHERE  p.status = 'completed'
            GROUP BY pl.plan_name, c.company_name, c.plan_id
        ) ranked
        WHERE rn <= 2
        ORDER BY plan_name, rn;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.7 Window Function on Support Tickets

    Rank tickets within each priority level by how long they
    took to resolve (fastest first). Unresolved tickets go last.
    """)
    return


@app.cell
def _(mo, support_tickets):
    _df = mo.sql(
        f"""
        -- Rank resolved tickets by resolution time within priority
        SELECT ticket_id,
               priority,
               created_date,
               resolved_date,
               resolved_date - created_date AS days_to_resolve,
               ROW_NUMBER() OVER (
                   PARTITION BY priority
                   ORDER BY COALESCE(resolved_date - created_date, 9999)
               ) AS speed_rank
        FROM   support_tickets
        ORDER BY priority, speed_rank;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Part 2: Query Performance (Week 7)

    Databases are fast because they **plan** before executing.
    Understanding query plans helps you write better SQL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.1 Selective Columns — Avoid SELECT *

    Always request only the columns you need.
    """)
    return


@app.cell
def _(mo, payments):
    _df = mo.sql(
        f"""
        -- Bad: SELECT * (fetches everything)
        -- SELECT * FROM payments;

        -- Good: select only what you need
        SELECT payment_id, customer_id, amount
        FROM   payments
        WHERE  status = 'completed'
        ORDER BY amount DESC
        LIMIT 5;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.2 EXPLAIN — See the Query Plan

    `EXPLAIN` shows the steps DuckDB takes to answer your query.
    """)
    return


@app.cell
def _(customers, mo, payments):
    _df = mo.sql(
        f"""
        -- See the execution plan for a JOIN query
        EXPLAIN
        SELECT c.company_name, SUM(p.amount) AS total
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        WHERE  p.status = 'completed'
        GROUP BY c.company_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.3 CREATE INDEX — Speed Up Lookups

    An index is like the index at the back of a textbook:
    it lets DuckDB jump straight to matching rows.
    """)
    return


@app.cell
def _(mo, payments):
    _df = mo.sql(
        f"""
        -- Create an index on payment_date
        CREATE INDEX IF NOT EXISTS idx_payment_date
        ON payments(payment_date);
        """
    )
    return


@app.cell
def _(mo, payments):
    _df = mo.sql(
        f"""
        -- Now queries filtering by payment_date can use the index
        EXPLAIN
        SELECT * FROM payments
        WHERE  payment_date >= '2025-04-01';
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.4 Sargable vs Non-Sargable Predicates

    **Sargable** (Search ARGument ABLE): the database can use an
    index. Wrapping a column in a function makes it non-sargable.

    | Sargable (fast) | Non-sargable (slow) |
    |-----------------|---------------------|
    | `WHERE payment_date >= '2025-03-01'` | `WHERE MONTH(payment_date) = 3` |
    | `WHERE amount BETWEEN 50 AND 100` | `WHERE ROUND(amount) = 80` |
    """)
    return


@app.cell
def _(mo, payments):
    _df = mo.sql(
        f"""
        -- Sargable: DuckDB can use the index on payment_date
        SELECT payment_id, payment_date, amount
        FROM   payments
        WHERE  payment_date BETWEEN '2025-03-01' AND '2025-03-31'
        ORDER BY payment_date;
        """
    )
    return


@app.cell
def _(mo, payments):
    _df = mo.sql(
        f"""
        -- Non-sargable: same result, but the function call
        -- prevents index usage
        SELECT payment_id, payment_date, amount
        FROM   payments
        WHERE  MONTH(payment_date) = 3
        ORDER BY payment_date;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.5 CTE (Common Table Expression) — Named Subqueries

    A CTE is a temporary named result set defined with `WITH`.
    It makes complex queries much easier to read.
    """)
    return


@app.cell
def _(customers, mo, payments, plans):
    _df = mo.sql(
        f"""
        -- CTE: calculate revenue per customer, then filter
        WITH customer_revenue AS (
            SELECT c.customer_id,
                   c.company_name,
                   pl.plan_name,
                   SUM(p.amount) AS total_paid
            FROM   payments p
            JOIN   customers c ON p.customer_id = c.customer_id
            JOIN   plans pl     ON c.plan_id    = pl.plan_id
            WHERE  p.status = 'completed'
            GROUP BY c.customer_id, c.company_name, pl.plan_name
        )
        SELECT company_name, plan_name, total_paid
        FROM   customer_revenue
        WHERE  total_paid > 200
        ORDER BY total_paid DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.6 Chained CTEs

    You can define multiple CTEs separated by commas.
    Each CTE can reference the ones defined before it.
    """)
    return


@app.cell
def _(customers, mo, payments, plans):
    _df = mo.sql(
        f"""
        -- Chained CTEs: revenue per plan, then compare to target
        WITH plan_revenue AS (
            SELECT c.plan_id,
                   pl.plan_name,
                   SUM(p.amount) AS total_revenue,
                   COUNT(DISTINCT c.customer_id) AS num_customers
            FROM   payments p
            JOIN   customers c ON p.customer_id = c.customer_id
            JOIN   plans pl     ON c.plan_id    = pl.plan_id
            WHERE  p.status = 'completed'
            GROUP BY c.plan_id, pl.plan_name
        ),
        plan_summary AS (
            SELECT plan_name,
                   total_revenue,
                   num_customers,
                   ROUND(total_revenue / num_customers, 2) AS avg_per_customer
            FROM plan_revenue
        )
        SELECT * FROM plan_summary
        ORDER BY total_revenue DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Part 3: Transactions & ACID (Week 8)

    A **transaction** is a group of SQL statements that must either
    ALL succeed or ALL fail. This is critical for financial operations.

    **ACID properties:**
    - **A**tomicity — All or nothing
    - **C**onsistency — Database stays valid
    - **I**solation — Transactions don't interfere
    - **D**urability — Committed data survives crashes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.1 Create the Accounts Table

    Each customer has an account balance. We'll use this table
    for transaction exercises.
    """)
    return


@app.cell
def _(customers, mo):
    _df = mo.sql(
        f"""
        -- Create accounts with starting balances
        CREATE OR REPLACE TABLE accounts AS
        SELECT * FROM (VALUES
            (1001, 1,  5000.00),
            (1002, 2,  1200.00),
            (1003, 3,  15000.00),
            (1004, 4,  3500.00),
            (1005, 5,  800.00),
            (1006, 6,  12000.00),
            (1007, 7,  2500.00),
            (1008, 8,  9000.00),
            (1009, 9,  600.00),
            (1010, 10, 4000.00)
        ) AS t(account_id, customer_id, balance);
        """
    )
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM accounts ORDER BY account_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.2 BEGIN / COMMIT — A Successful Transfer

    Transfer $500 from Acme Corp (1001) to DataFlow Inc (1004).
    Both UPDATEs succeed → COMMIT makes it permanent.
    """)
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        -- Step 1: Start the transaction
        BEGIN TRANSACTION;
        """
    )
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        -- Step 2: Debit $500 from Acme Corp
        UPDATE accounts SET balance = balance - 500
        WHERE  account_id = 1001;
        """
    )
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        -- Step 3: Credit $500 to DataFlow Inc
        UPDATE accounts SET balance = balance + 500
        WHERE  account_id = 1004;
        """
    )
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        -- Step 4: Commit — make it permanent
        COMMIT;
        """
    )
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        -- Verify: Acme should be 4500, DataFlow should be 4000
        SELECT account_id, customer_id, balance
        FROM   accounts
        WHERE  account_id IN (1001, 1004)
        ORDER BY account_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.3 BEGIN / ROLLBACK — Undoing a Mistake

    Suppose we accidentally debit Bright Ideas (1002) by $2000.
    That would overdraw the account! ROLLBACK undoes everything.
    """)
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        -- Check current balance before the transaction
        SELECT account_id, balance
        FROM   accounts
        WHERE  account_id = 1002;
        """
    )
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        -- Start a transaction, make the accidental debit
        BEGIN TRANSACTION;
        """
    )
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        -- Oops! $2000 debit on a $1200 account
        UPDATE accounts SET balance = balance - 2000
        WHERE  account_id = 1002;
        """
    )
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        -- We realize the mistake — ROLLBACK!
        ROLLBACK;
        """
    )
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        -- Verify: balance should still be 1200 (unchanged)
        SELECT account_id, balance
        FROM   accounts
        WHERE  account_id = 1002;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.4 CHECK Constraint — The Database Enforces Rules

    A `CHECK` constraint lets the database reject invalid data
    automatically. No application code needed.
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Create a table with a CHECK constraint: no negative balances
        CREATE OR REPLACE TABLE safe_accounts (
            account_id  INTEGER PRIMARY KEY,
            owner_name  VARCHAR NOT NULL,
            balance     DECIMAL(10,2) CHECK (balance >= 0)
        );
        """
    )
    return


@app.cell
def _(mo, safe_accounts):
    _df = mo.sql(
        f"""
        -- This works: positive balance
        INSERT INTO safe_accounts VALUES (1, 'Alice', 500.00);
        """
    )
    return


@app.cell
def _(mo, safe_accounts):
    _df = mo.sql(
        f"""
        -- Verify
        SELECT * FROM safe_accounts;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Try inserting a negative balance — the CHECK constraint will
    reject it.** In a live session, uncomment the cell below to see
    the error.

    ```sql
    -- This FAILS: CHECK constraint violation
    INSERT INTO safe_accounts VALUES (2, 'Bob', -100.00);
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.5 NOT NULL Constraint

    `NOT NULL` ensures a column always has a value.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Try inserting without an owner_name — the NOT NULL constraint
    will reject it.**

    ```sql
    -- This FAILS: NOT NULL violation
    INSERT INTO safe_accounts VALUES (3, NULL, 200.00);
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.6 PRIMARY KEY Violation

    A PRIMARY KEY must be unique. Inserting a duplicate is rejected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Try inserting a duplicate account_id — the PRIMARY KEY
    constraint will reject it.**

    ```sql
    -- This FAILS: duplicate primary key
    INSERT INTO safe_accounts VALUES (1, 'Charlie', 300.00);
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.7 Audit Logging — Tracking Every Transaction

    Financial systems must record every operation. An audit log
    answers: *who did what, when, and how much?*
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Create an audit log table
        CREATE OR REPLACE TABLE audit_log (
            log_id      INTEGER PRIMARY KEY,
            account_id  INTEGER NOT NULL,
            action      VARCHAR NOT NULL,
            amount      DECIMAL(10,2),
            log_time    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    return


@app.cell
def _(audit_log, mo):
    _df = mo.sql(
        f"""
        -- Log a transfer that happened earlier
        INSERT INTO audit_log VALUES
            (1, 1001, 'debit',  500.00, '2025-05-01 10:00:00'),
            (2, 1004, 'credit', 500.00, '2025-05-01 10:00:00');
        """
    )
    return


@app.cell
def _(audit_log, mo):
    _df = mo.sql(
        f"""
        -- View the audit log
        SELECT * FROM audit_log ORDER BY log_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.8 Putting It All Together — Full Transfer Workflow

    A complete transfer with debit, credit, and audit logging,
    wrapped in a transaction.
    """)
    return


@app.cell
def _(accounts, audit_log, mo):
    _df = mo.sql(
        f"""
        -- Full workflow: Transfer $1000 from Falcon (1006) to GrowthLab (1007)
        BEGIN TRANSACTION;

        UPDATE accounts SET balance = balance - 1000
        WHERE  account_id = 1006;

        UPDATE accounts SET balance = balance + 1000
        WHERE  account_id = 1007;

        INSERT INTO audit_log VALUES
            (3, 1006, 'debit',  1000.00, CURRENT_TIMESTAMP),
            (4, 1007, 'credit', 1000.00, CURRENT_TIMESTAMP);

        COMMIT;
        """
    )
    return


@app.cell
def _(accounts, mo):
    _df = mo.sql(
        f"""
        -- Verify balances: Falcon should be 11000, GrowthLab should be 3500
        SELECT account_id, customer_id, balance
        FROM   accounts
        WHERE  account_id IN (1006, 1007)
        ORDER BY account_id;
        """
    )
    return


@app.cell
def _(audit_log, mo):
    _df = mo.sql(
        f"""
        -- Verify audit log has all 4 entries
        SELECT * FROM audit_log ORDER BY log_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Summary

    **Week 7 — Window Functions & Performance:**
    - `ROW_NUMBER()` assigns unique sequential numbers
    - `RANK()` handles ties (same rank, skip next)
    - `PARTITION BY` divides rows into groups
    - `AVG() OVER (PARTITION BY ...)` compares each row to its group
    - `EXPLAIN` shows the query plan
    - `CREATE INDEX` speeds up lookups
    - Sargable predicates allow index usage
    - CTEs make complex queries readable

    **Week 8 — Transactions & ACID:**
    - `BEGIN` / `COMMIT` makes changes permanent
    - `BEGIN` / `ROLLBACK` undoes all changes
    - `CHECK` constraints enforce business rules
    - `NOT NULL` ensures required fields
    - `PRIMARY KEY` prevents duplicates
    - Audit logs track every operation

    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
