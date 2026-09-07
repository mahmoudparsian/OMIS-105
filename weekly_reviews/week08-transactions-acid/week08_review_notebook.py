import marimo

__generated_with = "0.23.10"
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
    mo.md(r"""
    # OMIS 105 — Week 8 Review: Transactions, ACID & Constraints

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    A bank transfer is two `UPDATE` statements. If the second one fails
    after the first succeeded, money disappears. Transactions make a group
    of statements all-or-nothing.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | Group statements | `BEGIN TRANSACTION`, `COMMIT` |
    | Undo a mistake | `ROLLBACK` |
    | Enforce business rules | `CHECK`, `NOT NULL`, `PRIMARY KEY` |
    | Track what happened | Audit-log tables |

    ### How to Use

    Run the cells from top to bottom. Every database cell takes `con`, the
    DuckDB connection created in the setup cell. Read the markdown between
    queries — it explains the *why*, not just the *how*.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Setup — Build the CloudMetrics Database

    **CloudMetrics** is a software-as-a-service company selling analytics tools to
    businesses. All the data is created inline below — there is no CSV to load, so
    this notebook runs anywhere.

    | Table | Rows | What It Holds |
    |-------|------|---------------|
    | `plans` | 3 | Subscription tiers and monthly prices |
    | `customers` | 10 | Companies, their industry, and their plan |
    | `payments` | 25 | Monthly payments — completed, failed, refunded |
    | `support_tickets` | 15 | Support requests by priority and category |
    """)
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM plans ORDER BY plan_id;
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM customers ORDER BY customer_id;
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM payments ORDER BY payment_id;
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM support_tickets ORDER BY ticket_id;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Transactions & ACID

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
    ### 1.1 Create the Accounts Table

    Each customer has an account balance. We'll use this table
    for transaction exercises.
    """)
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        SELECT * FROM accounts ORDER BY account_id;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.2 BEGIN / COMMIT — A Successful Transfer

    Transfer $500 from Acme Corp (1001) to DataFlow Inc (1004).
    Both UPDATEs succeed → COMMIT makes it permanent.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Step 1: Start the transaction
        BEGIN TRANSACTION;
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Step 2: Debit $500 from Acme Corp
        UPDATE accounts SET balance = balance - 500
        WHERE  account_id = 1001;
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Step 3: Credit $500 to DataFlow Inc
        UPDATE accounts SET balance = balance + 500
        WHERE  account_id = 1004;
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Step 4: Commit — make it permanent
        COMMIT;
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Verify: Acme should be 4500, DataFlow should be 4000
        SELECT account_id, customer_id, balance
        FROM   accounts
        WHERE  account_id IN (1001, 1004)
        ORDER BY account_id;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.3 BEGIN / ROLLBACK — Undoing a Mistake

    Suppose we accidentally debit Bright Ideas (1002) by $2000.
    That would overdraw the account! ROLLBACK undoes everything.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Check current balance before the transaction
        SELECT account_id, balance
        FROM   accounts
        WHERE  account_id = 1002;
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Start a transaction, make the accidental debit
        BEGIN TRANSACTION;
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Oops! $2000 debit on a $1200 account
        UPDATE accounts SET balance = balance - 2000
        WHERE  account_id = 1002;
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- We realize the mistake — ROLLBACK!
        ROLLBACK;
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Verify: balance should still be 1200 (unchanged)
        SELECT account_id, balance
        FROM   accounts
        WHERE  account_id = 1002;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.4 CHECK Constraint — The Database Enforces Rules

    A `CHECK` constraint lets the database reject invalid data
    automatically. No application code needed.
    """)
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        -- This works: positive balance
        INSERT INTO safe_accounts VALUES (1, 'Alice', 500.00);
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Verify
        SELECT * FROM safe_accounts;
        """
    ).fetchdf()
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
    ### 1.5 NOT NULL Constraint

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
    ### 1.6 PRIMARY KEY Violation

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
    ### 1.7 Audit Logging — Tracking Every Transaction

    Financial systems must record every operation. An audit log
    answers: *who did what, when, and how much?*
    """)
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        -- Log a transfer that happened earlier
        INSERT INTO audit_log VALUES
            (1, 1001, 'debit',  500.00, '2025-05-01 10:00:00'),
            (2, 1004, 'credit', 500.00, '2025-05-01 10:00:00');
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- View the audit log
        SELECT * FROM audit_log ORDER BY log_id;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.8 Putting It All Together — Full Transfer Workflow

    A complete transfer with debit, credit, and audit logging,
    wrapped in a transaction.
    """)
    return


@app.cell
def _(con):
    con.execute(
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
def _(con):
    con.execute(
        f"""
        -- Verify balances: Falcon should be 11000, GrowthLab should be 3500
        SELECT account_id, customer_id, balance
        FROM   accounts
        WHERE  account_id IN (1006, 1007)
        ORDER BY account_id;
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Verify audit log has all 4 entries
        SELECT * FROM audit_log ORDER BY log_id;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 8 Summary

    **Transactions**
    - `BEGIN TRANSACTION` opens a unit of work
    - `COMMIT` makes every change in it permanent
    - `ROLLBACK` undoes every change in it
    - Nothing in between is visible to anyone else until you commit

    **ACID**
    - **A**tomicity — all statements succeed, or none do
    - **C**onsistency — the database never lands in an invalid state
    - **I**solation — concurrent transactions do not see each other's partial work
    - **D**urability — once committed, the data survives a crash

    **Constraints**
    - `CHECK` enforces a business rule (`balance >= 0`)
    - `NOT NULL` makes a field required
    - `PRIMARY KEY` prevents duplicate identifiers
    - The database rejects bad data itself — no application code required

    ### Looking Ahead

    Week 9 puts everything together: CTEs, subqueries, and the full window
    function toolkit on a single analytical question.
    """)
    return


if __name__ == "__main__":
    app.run()
