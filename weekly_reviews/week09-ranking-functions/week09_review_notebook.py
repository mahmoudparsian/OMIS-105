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
    # OMIS 105 — Week 9 Review: Ranking Functions

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    Window functions rank and compare rows **without collapsing them**.
    This week: `ROW_NUMBER`, `RANK`, and `DENSE_RANK` — and how each one
    treats ties.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | Number and rank rows | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `PARTITION BY` |
    | Compare to a group | `AVG(...) OVER (PARTITION BY ...)` |
    | Filter on a rank | rank in a CTE, `WHERE` outside |

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
    ## Part 1: Window Functions

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
def _(con):
    con.execute(
        f"""
        -- Number customers by signup date (earliest = 1)
        SELECT customer_id,
               company_name,
               signup_date,
               ROW_NUMBER() OVER (ORDER BY signup_date) AS signup_rank
        FROM   customers
        ORDER BY signup_rank;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.2 ROW_NUMBER() with PARTITION BY

    Number payments within each customer (payment 1, 2, 3... per customer).
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.4 ROW_NUMBER vs RANK vs DENSE_RANK — Side by Side

    Several customers tie on the number of payments. Watch the three columns:

    - `ROW_NUMBER` always gives unique numbers — `company_name` breaks the ties
    - `RANK` gives ties the same number, then **skips** (1, 1, 3, 3, 5, …)
    - `DENSE_RANK` gives ties the same number, **no gaps** (1, 1, 2, 2, 3, …)
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Compare ROW_NUMBER, RANK, and DENSE_RANK
        SELECT c.company_name,
               COUNT(*)    AS num_payments,
               ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC, c.company_name) AS row_num,
               RANK()       OVER (ORDER BY COUNT(*) DESC) AS rank_num,
               DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS dense_num
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        WHERE  p.status = 'completed'
        GROUP BY c.company_name
        ORDER BY row_num;
        """
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
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
def _(con):
    con.execute(
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
    ).fetchdf()
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.8 "Second-Highest" — DENSE_RANK in a CTE

    Which customers have the **second-highest** number of completed payments?
    `WHERE` cannot see a window function, so compute the rank in a CTE first,
    then filter outside it.

    With `DENSE_RANK`, rank 2 is the second-highest **value** (3 payments):
    Harbor Health and Acme Corp. With `RANK`, no customer has rank 2 — the two
    customers tied at the top take ranks 1 and 1, and the next rank is 3.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Customers with the second-highest number of completed payments
        WITH ranked AS (
            SELECT c.company_name,
                   COUNT(*) AS num_payments,
                   DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS dense_num
            FROM   payments p
            JOIN   customers c ON p.customer_id = c.customer_id
            WHERE  p.status = 'completed'
            GROUP BY c.company_name
        )
        SELECT company_name, num_payments
        FROM   ranked
        WHERE  dense_num = 2
        ORDER BY company_name;
        """
    ).fetchdf()
    return



@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.9 Why `ORDER BY ... LIMIT` Cannot Rank

    `LIMIT n` counts **rows**; a ranking function compares **values**.
    ClearView Analytics and Falcon Logistics are tied at the top with 4
    completed payments each.

    **"Who has the most payments?"** `LIMIT 1` returns only ClearView Analytics
    (the tie-breaker `company_name` picked it). Falcon Logistics is cut with
    no warning.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        WITH counts AS (
            SELECT c.company_name, COUNT(*) AS num_payments
            FROM   payments p
            JOIN   customers c ON p.customer_id = c.customer_id
            WHERE  p.status = 'completed'
            GROUP BY c.company_name
        )
        SELECT company_name, num_payments
        FROM   counts
        ORDER BY num_payments DESC, company_name
        LIMIT 1;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **"Who has the second-highest number of payments?"** `LIMIT 1 OFFSET 1`
    skips one **row**, not one **value**: it returns Falcon Logistics with 4,
    which is still the highest value. The right answer (section 1.8) is Acme
    Corp and Harbor Health with 3.

    Also: `LIMIT` cannot restart per group, so "top 2 per plan" (section 1.6)
    needs `PARTITION BY`. Use `LIMIT` only to make a long result shorter.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        WITH counts AS (
            SELECT c.company_name, COUNT(*) AS num_payments
            FROM   payments p
            JOIN   customers c ON p.customer_id = c.customer_id
            WHERE  p.status = 'completed'
            GROUP BY c.company_name
        )
        SELECT company_name, num_payments
        FROM   counts
        ORDER BY num_payments DESC, company_name
        LIMIT 1 OFFSET 1;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 9 Summary

    **Window functions**
    - `ROW_NUMBER()` assigns unique sequential numbers — no ties
    - `RANK()` gives ties the same rank, then skips numbers
    - `DENSE_RANK()` gives ties the same rank, with no gaps
    - `PARTITION BY` restarts the calculation for each group
    - `AVG() OVER (PARTITION BY ...)` compares each row to its group

    **Filtering on a rank**
    - `WHERE` runs before window functions, so it cannot see a rank
    - Compute the rank in a CTE (or subquery), then filter outside it
    - "Second-highest value" → `DENSE_RANK() ... = 2`
    - `ORDER BY ... LIMIT n` / `OFFSET` count **rows**: they cut tied rows and cannot work per group — never use them to rank

    ### Looking Ahead

    A correct query is worthless if it leaves the data half-updated. Week 10 covers
    transactions: making a group of changes all-or-nothing.
    """)
    return


if __name__ == "__main__":
    app.run()
