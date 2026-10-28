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
    # OMIS 105 — Week 9 Review: CTEs, Subqueries & Advanced Window Functions

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    This is the integration week. Every analytical question here needs more
    than one step: name an intermediate result with a CTE, or nest a query
    inside another, then rank and compare across rows.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | Name intermediate results | `WITH ... AS`, chained CTEs |
    | Nest a query | Subqueries in `WHERE`, in `FROM`, correlated subqueries |
    | Test for existence | `EXISTS`, `IN` |
    | Look forward and back | `LAG`, `LEAD` |
    | Accumulate and smooth | Running totals, moving averages |
    | Rank and bucket | `DENSE_RANK`, `NTILE`, `FIRST_VALUE` |

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
    ## Setup — Build the CloudMetrics Database (Extended)

    The same **CloudMetrics** SaaS company from Weeks 7–8, plus two new tables:
    user activity `events` (with JSON metadata) and quarterly `kpi_targets`.
    All the data is created inline — there is no CSV to load.

    | Table | Rows | What It Holds |
    |-------|------|---------------|
    | `plans` | 3 | Subscription tiers and monthly prices |
    | `customers` | 10 | Companies, their industry, and their plan |
    | `payments` | 25 | Monthly payments — completed, failed, refunded |
    | `events` | 25 | User activity, with a JSON `metadata` column |
    | `kpi_targets` | 6 | Quarterly revenue and signup targets |
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Subscription plans
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
        -- 10 customer companies
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
        -- 25 payment records
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
        -- 25 user activity events with JSON metadata
        CREATE OR REPLACE TABLE events AS
        SELECT * FROM (VALUES
            (1,  1,  '2025-02-05'::DATE, 'page_view',  '{{"page": "dashboard", "referral": "google"}}'),
            (2,  1,  '2025-02-10'::DATE, 'purchase',   '{{"page": "checkout", "amount": 79.99, "referral": "direct"}}'),
            (3,  1,  '2025-03-15'::DATE, 'page_view',  '{{"page": "reports", "referral": "email"}}'),
            (4,  2,  '2025-03-01'::DATE, 'signup',     '{{"page": "register", "referral": "google"}}'),
            (5,  2,  '2025-03-10'::DATE, 'page_view',  '{{"page": "dashboard", "referral": "direct"}}'),
            (6,  3,  '2025-02-01'::DATE, 'page_view',  '{{"page": "analytics", "referral": "google"}}'),
            (7,  3,  '2025-02-15'::DATE, 'purchase',   '{{"page": "checkout", "amount": 149.99, "referral": "email"}}'),
            (8,  3,  '2025-03-20'::DATE, 'export',     '{{"page": "reports", "format": "csv", "referral": "direct"}}'),
            (9,  3,  '2025-04-10'::DATE, 'page_view',  '{{"page": "dashboard", "referral": "direct"}}'),
            (10, 3,  '2025-05-05'::DATE, 'upgrade',    '{{"page": "billing", "from_plan": "Pro", "to_plan": "Enterprise", "referral": "email"}}'),
            (11, 4,  '2025-03-15'::DATE, 'signup',     '{{"page": "register", "referral": "linkedin"}}'),
            (12, 4,  '2025-04-01'::DATE, 'page_view',  '{{"page": "dashboard", "referral": "direct"}}'),
            (13, 5,  '2025-03-01'::DATE, 'signup',     '{{"page": "register", "referral": "google"}}'),
            (14, 5,  '2025-03-20'::DATE, 'page_view',  '{{"page": "pricing", "referral": "google"}}'),
            (15, 6,  '2025-02-01'::DATE, 'page_view',  '{{"page": "analytics", "referral": "email"}}'),
            (16, 6,  '2025-02-20'::DATE, 'purchase',   '{{"page": "checkout", "amount": 149.99, "referral": "direct"}}'),
            (17, 6,  '2025-03-15'::DATE, 'export',     '{{"page": "reports", "format": "pdf", "referral": "direct"}}'),
            (18, 6,  '2025-04-10'::DATE, 'page_view',  '{{"page": "dashboard", "referral": "email"}}'),
            (19, 7,  '2025-04-01'::DATE, 'signup',     '{{"page": "register", "referral": "linkedin"}}'),
            (20, 7,  '2025-04-15'::DATE, 'page_view',  '{{"page": "dashboard", "referral": "direct"}}'),
            (21, 8,  '2025-03-01'::DATE, 'page_view',  '{{"page": "analytics", "referral": "google"}}'),
            (22, 8,  '2025-04-05'::DATE, 'purchase',   '{{"page": "checkout", "amount": 149.99, "referral": "google"}}'),
            (23, 9,  '2025-04-15'::DATE, 'signup',     '{{"page": "register", "referral": "google"}}'),
            (24, 10, '2025-04-01'::DATE, 'page_view',  '{{"page": "pricing", "referral": "linkedin"}}'),
            (25, 10, '2025-04-20'::DATE, 'purchase',   '{{"page": "checkout", "amount": 79.99, "referral": "linkedin"}}')
        ) AS t(event_id, customer_id, event_date, event_type, metadata);
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM events ORDER BY event_id;
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Quarterly KPI targets
        CREATE OR REPLACE TABLE kpi_targets AS
        SELECT * FROM (VALUES
            ('revenue',     'Q1-2025', 800.00),
            ('revenue',     'Q2-2025', 1200.00),
            ('new_signups', 'Q1-2025', 3),
            ('new_signups', 'Q2-2025', 5),
            ('events',      'Q1-2025', 15),
            ('events',      'Q2-2025', 20)
        ) AS t(metric, quarter, target_value);
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM kpi_targets ORDER BY metric, quarter;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Part 1: CTEs & Subqueries

    A **CTE** (Common Table Expression) is a named temporary result
    set defined with `WITH`. A **subquery** is a query nested inside
    another query.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.1 Basic CTE — Revenue Per Customer

    Calculate total revenue per customer, then filter to those
    who paid more than $200.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        WITH customer_revenue AS (
            SELECT c.customer_id,
                   c.company_name,
                   SUM(p.amount) AS total_paid
            FROM   payments p
            JOIN   customers c ON p.customer_id = c.customer_id
            WHERE  p.status = 'completed'
            GROUP BY c.customer_id, c.company_name
        )
        SELECT company_name, total_paid
        FROM   customer_revenue
        WHERE  total_paid > 200
        ORDER BY total_paid DESC;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.2 Chained CTEs — Plan-Level Summary

    First CTE: revenue per customer. Second CTE: aggregate by plan.
    Final query: compare plans.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        WITH customer_revenue AS (
            SELECT c.customer_id,
                   c.company_name,
                   c.plan_id,
                   SUM(p.amount) AS total_paid
            FROM   payments p
            JOIN   customers c ON p.customer_id = c.customer_id
            WHERE  p.status = 'completed'
            GROUP BY c.customer_id, c.company_name, c.plan_id
        ),
        plan_summary AS (
            SELECT pl.plan_name,
                   COUNT(*)                          AS num_customers,
                   ROUND(SUM(cr.total_paid), 2)      AS plan_revenue,
                   ROUND(AVG(cr.total_paid), 2)      AS avg_per_customer
            FROM   customer_revenue cr
            JOIN   plans pl ON cr.plan_id = pl.plan_id
            GROUP BY pl.plan_name
        )
        SELECT * FROM plan_summary
        ORDER BY plan_revenue DESC;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.3 Subquery in WHERE — Above-Average Customers

    Find customers whose total payments exceed the overall average.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Subquery calculates the average; outer query filters
        SELECT c.company_name,
               SUM(p.amount) AS total_paid
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        WHERE  p.status = 'completed'
        GROUP BY c.company_name
        HAVING SUM(p.amount) > (
            SELECT AVG(customer_total)
            FROM (
                SELECT SUM(amount) AS customer_total
                FROM   payments
                WHERE  status = 'completed'
                GROUP BY customer_id
            )
        )
        ORDER BY total_paid DESC;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.4 Subquery in FROM — Derived Table

    Use a subquery as a virtual table to join aggregated data
    back to detail rows.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Join each payment with the customer's total
        SELECT c.company_name,
               p.payment_date,
               p.amount,
               totals.total_paid,
               ROUND(p.amount / totals.total_paid * 100, 1) AS pct_of_total
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        JOIN   (
            SELECT customer_id, SUM(amount) AS total_paid
            FROM   payments
            WHERE  status = 'completed'
            GROUP BY customer_id
        ) totals ON p.customer_id = totals.customer_id
        WHERE  p.status = 'completed'
        ORDER BY c.company_name, p.payment_date;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.5 Correlated Subquery — Most Recent Payment

    For each customer, find the date and amount of their most
    recent completed payment. The subquery references the outer
    query's customer_id.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Correlated subquery: runs once per customer
        SELECT c.company_name,
               p.payment_date AS latest_date,
               p.amount
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        WHERE  p.status = 'completed'
          AND  p.payment_date = (
               SELECT MAX(p2.payment_date)
               FROM   payments p2
               WHERE  p2.customer_id = p.customer_id
                 AND  p2.status = 'completed'
          )
        ORDER BY c.company_name;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.6 EXISTS — Customers with Failed Payments

    `EXISTS` checks whether a subquery returns any rows.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Find customers who have at least one failed payment
        SELECT c.customer_id, c.company_name
        FROM   customers c
        WHERE  EXISTS (
            SELECT 1 FROM payments p
            WHERE  p.customer_id = c.customer_id
              AND  p.status = 'failed'
        );
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.7 IN Subquery — Customers on Enterprise Plan

    `IN` checks if a value belongs to a set returned by a subquery.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Find events from Enterprise-plan customers
        SELECT e.event_id,
               c.company_name,
               e.event_type,
               e.event_date
        FROM   events e
        JOIN   customers c ON e.customer_id = c.customer_id
        WHERE  c.customer_id IN (
            SELECT customer_id FROM customers WHERE plan_id = 3
        )
        ORDER BY e.event_date;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Part 2: Advanced Window Functions

    Building on the ROW_NUMBER and RANK from Week 7, we now
    explore LAG, LEAD, running totals, moving averages, and more.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.1 LAG() — Previous Payment Comparison

    `LAG(column, 1)` returns the value from the previous row.
    Useful for month-over-month analysis.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Each payment next to the customer's previous payment
        SELECT c.company_name,
               p.payment_date,
               p.amount,
               LAG(p.amount, 1) OVER (
                   PARTITION BY p.customer_id
                   ORDER BY p.payment_date
               ) AS prev_amount,
               p.amount - LAG(p.amount, 1) OVER (
                   PARTITION BY p.customer_id
                   ORDER BY p.payment_date
               ) AS change
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        WHERE  p.status = 'completed'
        ORDER BY c.company_name, p.payment_date;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.2 LEAD() — Next Payment Preview

    `LEAD(column, 1)` returns the value from the next row.
    The last row in each partition gets NULL.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Each payment with a preview of the next one
        SELECT c.company_name,
               p.payment_date,
               p.amount         AS current_amount,
               LEAD(p.amount, 1) OVER (
                   PARTITION BY p.customer_id
                   ORDER BY p.payment_date
               )                AS next_amount,
               LEAD(p.payment_date, 1) OVER (
                   PARTITION BY p.customer_id
                   ORDER BY p.payment_date
               )                AS next_date
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        WHERE  p.status = 'completed'
        ORDER BY c.company_name, p.payment_date;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.3 Running Total — Cumulative Revenue Over Time

    `SUM() OVER (ORDER BY date)` computes a running total.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Cumulative revenue over time (all customers combined)
        SELECT payment_date,
               amount,
               SUM(amount) OVER (ORDER BY payment_date, payment_id)
                   AS cumulative_revenue
        FROM   payments
        WHERE  status = 'completed'
        ORDER BY payment_date, payment_id;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.4 Moving Average — Smoothing Fluctuations

    `AVG() OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`
    computes the average of the current row and the 2 before it.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- 3-payment moving average of payment amounts
        SELECT payment_id,
               payment_date,
               amount,
               ROUND(
                   AVG(amount) OVER (
                       ORDER BY payment_date, payment_id
                       ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                   ), 2
               ) AS moving_avg_3
        FROM   payments
        WHERE  status = 'completed'
        ORDER BY payment_date, payment_id;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.5 DENSE_RANK — No Gaps in Ranking

    `DENSE_RANK` is like `RANK` but never skips numbers after ties.

    | Rank | DENSE_RANK |
    |------|------------|
    | 1    | 1          |
    | 2    | 2          |
    | 2    | 2          |
    | 4 ← skip | 3 ← no skip |
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Compare RANK and DENSE_RANK
        SELECT c.company_name,
               COUNT(*) AS num_payments,
               RANK()       OVER (ORDER BY COUNT(*) DESC) AS rank_num,
               DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS dense_rank_num
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        WHERE  p.status = 'completed'
        GROUP BY c.company_name
        ORDER BY rank_num;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.6 NTILE(4) — Quartile Buckets

    `NTILE(4)` divides customers into 4 roughly equal groups.
    Quartile 1 = top 25%, Quartile 4 = bottom 25%.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Divide customers into revenue quartiles
        SELECT company_name,
               total_paid,
               NTILE(4) OVER (ORDER BY total_paid DESC) AS quartile
        FROM (
            SELECT c.company_name,
                   SUM(p.amount) AS total_paid
            FROM   payments p
            JOIN   customers c ON p.customer_id = c.customer_id
            WHERE  p.status = 'completed'
            GROUP BY c.company_name
        )
        ORDER BY quartile, total_paid DESC;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.7 FIRST_VALUE — Compare to First Payment

    `FIRST_VALUE(column)` returns the first value in the window.
    Here: each customer's first payment date.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Each payment with the customer's first payment date
        SELECT c.company_name,
               p.payment_date,
               p.amount,
               FIRST_VALUE(p.payment_date) OVER (
                   PARTITION BY p.customer_id
                   ORDER BY p.payment_date
               ) AS first_payment_date
        FROM   payments p
        JOIN   customers c ON p.customer_id = c.customer_id
        WHERE  p.status = 'completed'
        ORDER BY c.company_name, p.payment_date;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.8 CTE + Window Function — Percentage of Total Revenue

    Combine a CTE (for total) with a window function (for per-row %).
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Each customer's share of total revenue
        WITH customer_totals AS (
            SELECT c.company_name,
                   SUM(p.amount) AS total_paid
            FROM   payments p
            JOIN   customers c ON p.customer_id = c.customer_id
            WHERE  p.status = 'completed'
            GROUP BY c.company_name
        )
        SELECT company_name,
               total_paid,
               ROUND(
                   total_paid * 100.0 / SUM(total_paid) OVER (), 1
               ) AS pct_of_total
        FROM   customer_totals
        ORDER BY total_paid DESC;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 9 Summary

    **CTEs and subqueries**
    - `WITH name AS (...)` names a temporary result set
    - Chained CTEs build on each other, separated by commas
    - A subquery can sit in `WHERE`, in `FROM` (a derived table), or in `SELECT`
    - A **correlated** subquery references the outer query and runs once per row
    - `EXISTS` asks "are there any rows?"; `IN` asks "is this value in that set?"

    **Advanced window functions**
    - `LAG()` / `LEAD()` reach into the previous / next row
    - `SUM() OVER (ORDER BY ...)` gives a running total
    - `ROWS BETWEEN n PRECEDING AND CURRENT ROW` gives a moving average
    - `DENSE_RANK()` ranks ties together with no gaps afterwards
    - `NTILE(n)` splits rows into n equal buckets (quartiles, deciles)
    - `FIRST_VALUE()` returns the first row's value across the whole window

    ### Looking Ahead

    Week 10 closes the course with the features that make DuckDB more than
    standard SQL: JSON, `PIVOT`, and lists.
    """)
    return


if __name__ == "__main__":
    app.run()
