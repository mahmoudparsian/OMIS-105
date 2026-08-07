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
    # OMIS 105 — Weeks 9 & 10 Review

    ## CTEs · Subqueries · Advanced Window Functions · Modern DuckDB

    **Dataset: CloudMetrics SaaS (Extended)** — The same SaaS company
    from Weeks 7–8, now with user activity events (including JSON
    metadata) and quarterly KPI targets.

    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Setting Up the Database

    We create five tables:

    - **plans** — three subscription tiers
    - **customers** — 10 companies
    - **payments** — 25 monthly payment records
    - **events** — 25 user activity events with JSON metadata
    - **kpi_targets** — 6 quarterly performance targets
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
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
def _(mo, plans):
    _df = mo.sql(
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
def _(customers, mo):
    _df = mo.sql(
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
def _(customers, mo):
    _df = mo.sql(
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
def _(events, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM events ORDER BY event_id;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
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
def _(kpi_targets, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM kpi_targets ORDER BY metric, quarter;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Part 1: CTEs & Subqueries (Week 9)

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
def _(customers, mo, payments):
    _df = mo.sql(
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
    )
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
def _(customers, mo, payments, plans):
    _df = mo.sql(
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
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.3 Subquery in WHERE — Above-Average Customers

    Find customers whose total payments exceed the overall average.
    """)
    return


@app.cell
def _(customers, mo, payments):
    _df = mo.sql(
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
    )
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
def _(customers, mo, payments):
    _df = mo.sql(
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
    )
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
def _(customers, mo, payments):
    _df = mo.sql(
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
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.6 EXISTS — Customers with Failed Payments

    `EXISTS` checks whether a subquery returns any rows.
    """)
    return


@app.cell
def _(customers, mo, payments):
    _df = mo.sql(
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
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.7 IN Subquery — Customers on Enterprise Plan

    `IN` checks if a value belongs to a set returned by a subquery.
    """)
    return


@app.cell
def _(customers, events, mo):
    _df = mo.sql(
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
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Part 2: Advanced Window Functions (Week 9)

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
def _(customers, mo, payments):
    _df = mo.sql(
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
    )
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
def _(customers, mo, payments):
    _df = mo.sql(
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
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.3 Running Total — Cumulative Revenue Over Time

    `SUM() OVER (ORDER BY date)` computes a running total.
    """)
    return


@app.cell
def _(mo, payments):
    _df = mo.sql(
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
    )
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
def _(mo, payments):
    _df = mo.sql(
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
    )
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
def _(customers, mo, payments):
    _df = mo.sql(
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
    )
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
def _(customers, mo, payments):
    _df = mo.sql(
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
    )
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
def _(customers, mo, payments):
    _df = mo.sql(
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
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 2.8 CTE + Window Function — Percentage of Total Revenue

    Combine a CTE (for total) with a window function (for per-row %).
    """)
    return


@app.cell
def _(customers, mo, payments):
    _df = mo.sql(
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
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Part 3: Modern DuckDB Features (Week 10)

    DuckDB can query JSON, pivot tables, collect values into lists,
    and more — features that go beyond standard SQL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.1 json_extract_string — Pull Fields from JSON

    The `metadata` column stores JSON. We can extract specific
    fields using `json_extract_string(column, '$.field')`.
    """)
    return


@app.cell
def _(events, mo):
    _df = mo.sql(
        f"""
        -- Extract page and referral from JSON metadata
        SELECT event_id,
               event_type,
               json_extract_string(metadata, '$.page')     AS page,
               json_extract_string(metadata, '$.referral') AS referral
        FROM   events
        ORDER BY event_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.2 json_extract + CAST — Extract Numeric Values

    The `amount` field inside JSON is text. We cast it to a number
    for calculations.
    """)
    return


@app.cell
def _(customers, events, mo):
    _df = mo.sql(
        f"""
        -- Extract purchase amounts from JSON
        SELECT c.company_name,
               e.event_date,
               CAST(json_extract(e.metadata, '$.amount') AS DECIMAL(10,2))
                   AS purchase_amount
        FROM   events e
        JOIN   customers c ON e.customer_id = c.customer_id
        WHERE  e.event_type = 'purchase'
        ORDER BY e.event_date;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.3 Referral Analysis — Which Source Drives Purchases?

    Combine JSON extraction with GROUP BY to analyze referral
    sources.
    """)
    return


@app.cell
def _(events, mo):
    _df = mo.sql(
        f"""
        -- Count events by referral source
        SELECT json_extract_string(metadata, '$.referral') AS referral,
               event_type,
               COUNT(*) AS event_count
        FROM   events
        GROUP BY referral, event_type
        ORDER BY referral, event_count DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.4 PIVOT — Reshape Event Counts into Columns

    `PIVOT` rotates rows into columns — like a pivot table in Excel.
    Each event_type becomes its own column.
    """)
    return


@app.cell
def _(customers, events, mo):
    _df = mo.sql(
        f"""
        -- Pivot: one row per customer, one column per event type
        PIVOT (
            SELECT c.company_name, e.event_type
            FROM   events e
            JOIN   customers c ON e.customer_id = c.customer_id
        )
        ON event_type
        USING COUNT(*)
        ORDER BY company_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.5 LIST() — Collect Values into an Array

    `LIST()` is an aggregate that collects all values into an
    array instead of counting or summing.
    """)
    return


@app.cell
def _(customers, events, mo):
    _df = mo.sql(
        f"""
        -- Collect all event types per customer into a list
        SELECT c.company_name,
               LIST(DISTINCT e.event_type ORDER BY e.event_type) AS event_types,
               COUNT(*) AS total_events
        FROM   events e
        JOIN   customers c ON e.customer_id = c.customer_id
        GROUP BY c.company_name
        ORDER BY total_events DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.6 UNNEST — Expand a List Back into Rows

    `UNNEST` is the opposite of `LIST` — it turns an array
    into individual rows.
    """)
    return


@app.cell
def _(customers, events, mo):
    _df = mo.sql(
        f"""
        -- First collect, then unnest to demonstrate the round-trip
        WITH customer_events AS (
            SELECT c.company_name,
                   LIST(DISTINCT e.event_type ORDER BY e.event_type) AS event_types
            FROM   events e
            JOIN   customers c ON e.customer_id = c.customer_id
            GROUP BY c.company_name
        )
        SELECT company_name,
               UNNEST(event_types) AS event_type
        FROM   customer_events
        ORDER BY company_name, event_type;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.7 STRFTIME — Day of Week Analysis

    `STRFTIME(date, '%A')` extracts the day name. Which days
    are most active?
    """)
    return


@app.cell
def _(events, mo):
    _df = mo.sql(
        f"""
        -- Event count by day of week
        SELECT STRFTIME(event_date, '%A') AS day_of_week,
               COUNT(*) AS event_count
        FROM   events
        GROUP BY day_of_week
        ORDER BY event_count DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.8 CROSS JOIN — Compare Actuals vs KPI Targets

    A `CROSS JOIN` pairs every row from one table with every row
    from another. Here we compare actual metrics to targets.
    """)
    return


@app.cell
def _(events, kpi_targets, mo, payments):
    _df = mo.sql(
        f"""
        -- Calculate actual revenue per quarter
        WITH actual_revenue AS (
            SELECT CASE
                       WHEN payment_date BETWEEN '2025-01-01' AND '2025-03-31'
                       THEN 'Q1-2025'
                       ELSE 'Q2-2025'
                   END AS quarter,
                   ROUND(SUM(amount), 2) AS actual_value
            FROM   payments
            WHERE  status = 'completed'
            GROUP BY quarter
        )
        -- Compare actuals to targets
        SELECT t.quarter,
               t.metric,
               t.target_value,
               a.actual_value,
               ROUND(a.actual_value - t.target_value, 2) AS gap
        FROM   kpi_targets t
        JOIN   actual_revenue a ON t.quarter = a.quarter
        WHERE  t.metric = 'revenue'
        ORDER BY t.quarter;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.9 Grand Finale — CTE + Window + JSON + HAVING

    One query that combines everything: a CTE for JSON extraction,
    a window function for ranking, and HAVING for filtering.
    """)
    return


@app.cell
def _(customers, events, mo):
    _df = mo.sql(
        f"""
        -- Find the top referral source per customer (by event count),
        -- but only for customers with 3+ events
        WITH customer_referrals AS (
            SELECT c.company_name,
                   json_extract_string(e.metadata, '$.referral') AS referral,
                   COUNT(*) AS ref_count
            FROM   events e
            JOIN   customers c ON e.customer_id = c.customer_id
            GROUP BY c.company_name, referral
        ),
        ranked AS (
            SELECT company_name,
                   referral,
                   ref_count,
                   ROW_NUMBER() OVER (
                       PARTITION BY company_name
                       ORDER BY ref_count DESC
                   ) AS rn,
                   SUM(ref_count) OVER (
                       PARTITION BY company_name
                   ) AS total_events
            FROM   customer_referrals
        )
        SELECT company_name,
               referral     AS top_referral,
               ref_count,
               total_events
        FROM   ranked
        WHERE  rn = 1
          AND  total_events >= 3
        ORDER BY total_events DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Summary

    **Week 9 — CTEs & Subqueries:**
    - `WITH ... AS` defines a named temporary result set (CTE)
    - Chained CTEs build on each other (separated by commas)
    - Subqueries can appear in WHERE, FROM, or SELECT
    - Correlated subqueries reference the outer query
    - `EXISTS` checks if a subquery returns any rows
    - `IN` checks membership in a set

    **Week 9 — Advanced Window Functions:**
    - `LAG()` / `LEAD()` — access previous / next row
    - `SUM() OVER (ORDER BY ...)` — running total
    - `ROWS BETWEEN n PRECEDING AND CURRENT ROW` — moving average
    - `DENSE_RANK()` — no gaps after ties
    - `NTILE(n)` — divide into n buckets
    - `FIRST_VALUE()` — first value in the window

    **Week 10 — Modern DuckDB:**
    - `json_extract_string()` — pull text from JSON
    - `json_extract() + CAST` — pull numbers from JSON
    - `PIVOT` — rows to columns (like Excel pivot tables)
    - `LIST()` — collect values into an array
    - `UNNEST` — expand an array into rows
    - `STRFTIME()` — format dates (day of week, month name)
    - `CROSS JOIN` — pair every row with every row (actuals vs targets)

    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
