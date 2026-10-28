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
    # OMIS 105 — Week 10 Review: Modern DuckDB — JSON, PIVOT & Lists

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    Real business data is rarely a tidy grid. It arrives as JSON, it needs
    reshaping for a report, and it has to be compared against targets. This
    week covers the DuckDB features that handle all three.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | Query JSON | `json_extract_string`, `json_extract` + `CAST` |
    | Reshape for reporting | `PIVOT` — rows into columns |
    | Work with arrays | `LIST`, `UNNEST` |
    | Format dates | `STRFTIME` |
    | Compare to targets | `CROSS JOIN` actuals against KPIs |

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
    ## Modern DuckDB Features

    DuckDB can query JSON, pivot tables, collect values into lists,
    and more — features that go beyond standard SQL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.1 json_extract_string — Pull Fields from JSON

    The `metadata` column stores JSON. We can extract specific
    fields using `json_extract_string(column, '$.field')`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Extract page and referral from JSON metadata
        SELECT event_id,
               event_type,
               json_extract_string(metadata, '$.page')     AS page,
               json_extract_string(metadata, '$.referral') AS referral
        FROM   events
        ORDER BY event_id;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.2 json_extract + CAST — Extract Numeric Values

    The `amount` field inside JSON is text. We cast it to a number
    for calculations.
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.3 Referral Analysis — Which Source Drives Purchases?

    Combine JSON extraction with GROUP BY to analyze referral
    sources.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Count events by referral source
        SELECT json_extract_string(metadata, '$.referral') AS referral,
               event_type,
               COUNT(*) AS event_count
        FROM   events
        GROUP BY referral, event_type
        ORDER BY referral, event_count DESC;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.4 PIVOT — Reshape Event Counts into Columns

    `PIVOT` rotates rows into columns — like a pivot table in Excel.
    Each event_type becomes its own column.
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.5 LIST() — Collect Values into an Array

    `LIST()` is an aggregate that collects all values into an
    array instead of counting or summing.
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.6 UNNEST — Expand a List Back into Rows

    `UNNEST` is the opposite of `LIST` — it turns an array
    into individual rows.
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.7 STRFTIME — Day of Week Analysis

    `STRFTIME(date, '%A')` extracts the day name. Which days
    are most active?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Event count by day of week
        SELECT STRFTIME(event_date, '%A') AS day_of_week,
               COUNT(*) AS event_count
        FROM   events
        GROUP BY day_of_week
        ORDER BY event_count DESC;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.8 CROSS JOIN — Compare Actuals vs KPI Targets

    A `CROSS JOIN` pairs every row from one table with every row
    from another. Here we compare actual metrics to targets.
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 1.9 Grand Finale — CTE + Window + JSON + HAVING

    One query that combines everything: a CTE for JSON extraction,
    a window function for ranking, and HAVING for filtering.
    """)
    return


@app.cell
def _(con):
    con.execute(
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
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 10 Summary

    | Feature | What It Does |
    |---------|-------------|
    | `json_extract_string(col, '$.field')` | Pull a text field out of JSON |
    | `CAST(json_extract(col, '$.field') AS DECIMAL)` | Pull a number out of JSON |
    | `PIVOT` | Turn rows into columns, like an Excel pivot table |
    | `LIST(col)` | Collect many values into a single array |
    | `UNNEST(list)` | Expand an array back into rows |
    | `STRFTIME(date, '%A')` | Format a date (day name, month name, `YYYY-MM`) |
    | `CROSS JOIN` | Pair every row with every row — actuals against targets |

    ### The Whole Course, in One Table

    | Weeks | What You Learned |
    |-------|-----------------|
    | 1–3 | Query one table, design several, summarize them |
    | 4–6 | Analyze without collapsing rows, join every way, design formally |
    | 7–8 | Make queries fast, make changes safe |
    | 9–10 | Compose multi-step analysis, and handle real-world data shapes |

    You can now take a business question, decide which tables answer it, write the
    query, check that it is correct, and make it fast. That is the job.
    """)
    return


if __name__ == "__main__":
    app.run()
