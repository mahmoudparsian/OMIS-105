import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Sales Data Exploration with DuckDB

    **Course:** OMIS 105 &nbsp;|&nbsp; **Author:** Professor Mahmoud Parsian

    ---

    ## Introduction

    This notebook analyses a sales database for a paper company.
    We explore orders for different paper types (standard, gloss, poster)
    placed by companies such as Walmart, Apple, Microsoft, and others.

    **Goals:**
    - Identify best-selling products and biggest customers
    - Analyse sales growth rate year-over-year
    - Examine regional performance and sales rep effectiveness
    - Understand web-event channel distribution

    **Tech stack:** Python · DuckDB (in-process SQL engine) · Pandas · Matplotlib
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Entity Relationship Diagram

    The database has five tables: **accounts**, **orders**, **region**, **sales_reps**, and **web_events**.

    ![ERD](ERD.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 &nbsp; Environment Setup

    Install required packages (only needed once) and import libraries.
    """)
    return


@app.cell
def _():
    # ── install packages (run once) ──
    # !pip install duckdb pandas matplotlib
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import warnings
    warnings.filterwarnings('ignore')

    # Helper module  – keeps the notebook clean
    from display_utils import show, plot_bar, plot_line, plot_pie, plot_hbar, plot_grouped_bar, plot_stacked_bar

    # Create an in-memory DuckDB connection
    con = duckdb.connect()
    print('DuckDB version:', duckdb.__version__)
    return (con, pd, plot_bar, plot_grouped_bar, plot_hbar, plot_line, plot_pie, plot_stacked_bar, show)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 &nbsp; Load Data from CSV Files

    We read each CSV into a DuckDB table. The CSV files live in the `data/` folder.
    """)
    return


@app.cell
def _(con):
    # ── Create tables from CSV files ──

    con.execute("""
        CREATE TABLE region AS
        SELECT *
        FROM read_csv_auto('data/region.csv');
    """)

    con.execute("""
        CREATE TABLE sales_reps AS
        SELECT *
        FROM read_csv_auto('data/sales_reps.csv');
    """)

    con.execute("""
        CREATE TABLE accounts AS
        SELECT *
        FROM read_csv_auto('data/accounts.csv');
    """)

    con.execute("""
        CREATE TABLE orders AS
        SELECT *
        FROM read_csv_auto('data/orders.csv');
    """)

    con.execute("""
        CREATE TABLE web_events AS
        SELECT *
        FROM read_csv_auto('data/web_events.csv');
    """)

    print('All 5 tables loaded successfully.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.1 &nbsp; Quick Preview of Each Table
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM region
        LIMIT 5;
    """).df()
    show(_df, title='region')
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM sales_reps
        LIMIT 5;
    """).df()
    show(_df, title='sales_reps')
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM accounts
        LIMIT 5;
    """).df()
    show(_df, title='accounts')
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM orders
        LIMIT 5;
    """).df()
    show(_df, title='orders')
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT *
        FROM web_events
        LIMIT 5;
    """).df()
    show(_df, title='web_events')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2 &nbsp; Row Counts per Table
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            'region' AS table_name,
            COUNT(*) AS row_count
        FROM region
        UNION ALL
        SELECT
            'sales_reps',
            COUNT(*)
        FROM sales_reps
        UNION ALL
        SELECT
            'accounts',
            COUNT(*)
        FROM accounts
        UNION ALL
        SELECT
            'orders',
            COUNT(*)
        FROM orders
        UNION ALL
        SELECT
            'web_events',
            COUNT(*)
        FROM web_events;
    """).df()
    show(_df, title='Row Counts')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3 &nbsp; Sales Analysis
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1 &nbsp; Total Sales per Year

    How much did we sell each year (in USD)?
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT EXTRACT(YEAR
        FROM occurred_at) AS year, SUM(total_amt_usd) AS total_usd
        FROM orders
        GROUP BY year
        ORDER BY year;
    """).df()

    show(_df, title='Total Sales per Year')
    plot_bar(_df, 'year', 'total_usd',
             title='Total Sales per Year (USD)',
             xlabel='Year', ylabel='Total Sales (USD)',
             currency=True, fmt='${:,.0f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2 &nbsp; Why 2013 and 2017 Have Low Totals

    Both years appear low because only one month of data exists for each.
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT EXTRACT(YEAR
        FROM occurred_at) AS year, EXTRACT(MONTH
        FROM occurred_at) AS month, SUM(total_amt_usd) AS total_usd
        FROM orders
        WHERE EXTRACT(YEAR
        FROM occurred_at) IN (2013, 2017)
        GROUP BY year, month
        ORDER BY year;
    """).df()

    show(_df, title='Monthly Breakdown for 2013 & 2017')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.3 &nbsp; Daily Detail for 2017

    Only two days are recorded in 2017 — January 1st and 2nd.
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT EXTRACT(YEAR
        FROM occurred_at) AS year, EXTRACT(MONTH
        FROM occurred_at) AS month, EXTRACT(DAY
        FROM occurred_at) AS day, SUM(total_amt_usd) AS total_usd
        FROM orders
        WHERE EXTRACT(YEAR
        FROM occurred_at) = 2017
        GROUP BY year, month, day
        ORDER BY total_usd;
    """).df()

    show(_df, title='2017 Daily Breakdown')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.4 &nbsp; January 1st Sales — Year-over-Year Comparison

    Comparing the same date each year shows a steady upward trend.
    """)
    return


@app.cell
def _(con, plot_line, show):
    _df = con.execute("""
        SELECT EXTRACT(YEAR
        FROM occurred_at) AS year, SUM(total_amt_usd) AS total_usd
        FROM orders
        WHERE EXTRACT(MONTH
        FROM occurred_at) = 1
        AND EXTRACT(DAY
        FROM occurred_at) = 1
        GROUP BY year
        ORDER BY year;
    """).df()

    show(_df, title='January 1st Sales by Year')
    plot_line(_df, 'year', 'total_usd',
              title='January 1st Sales — Year-over-Year',
              xlabel='Year', ylabel='Total Sales (USD)',
              currency=True, fmt='${:,.0f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.5 &nbsp; Year-over-Year Sales Growth (Jan 1st)

    Using the `LAG` window function to compute absolute and percentage growth.
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        WITH jan1 AS (
        SELECT EXTRACT(YEAR
        FROM occurred_at) AS year, SUM(total_amt_usd) AS total_usd
        FROM orders
        WHERE EXTRACT(MONTH
        FROM occurred_at) = 1
        AND EXTRACT(DAY
        FROM occurred_at) = 1
        GROUP BY year
        ORDER BY year )
        SELECT
            year,
            total_usd,
            total_usd - LAG(total_usd) OVER (
        ORDER BY year) AS growth_usd, ROUND((total_usd - LAG(total_usd) OVER (
        ORDER BY year)) / LAG(total_usd) OVER (
        ORDER BY year) * 100, 2) AS growth_pct
        FROM jan1;
    """).df()

    show(_df, title='Year-over-Year Growth (Jan 1st)')
    # Plot growth percentage (skip first year which is NULL)
    plot_bar(_df.dropna(), 'year', 'growth_pct',
             title='Year-over-Year Growth Rate (%)',
             xlabel='Year', ylabel='Growth (%)',
             color='#55A868', fmt='{:.1f}%')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.6 &nbsp; Average Paper Quantity per Account (Top 10)

    Which companies order the most paper on average?
    """)
    return


@app.cell
def _(con, plot_hbar, show):
    _df = con.execute("""
        SELECT
            ac.name AS account_name,
            ROUND(AVG(o.standard_qty), 1) AS avg_standard,
            ROUND(AVG(o.gloss_qty), 1) AS avg_gloss,
            ROUND(AVG(o.poster_qty), 1) AS avg_poster,
            ROUND(AVG(o.total), 1) AS avg_total
        FROM accounts ac
        JOIN orders o ON ac.id = o.account_id
        GROUP BY ac.name
        ORDER BY avg_total DESC
        LIMIT 10;
    """).df()

    show(_df, title='Top 10 Accounts by Avg. Total Qty')
    plot_hbar(_df, 'account_name', 'avg_total',
              title='Top 10 Accounts — Avg. Quantity per Order',
              xlabel='Average Quantity')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.7 &nbsp; Average Spend per Order by Account (Top 10)

    Which companies spend the most per order?
    """)
    return


@app.cell
def _(con, plot_hbar, show):
    _df = con.execute("""
        SELECT
            ac.name AS account_name,
            ROUND(AVG(o.standard_amt_usd), 2) AS avg_standard_usd,
            ROUND(AVG(o.gloss_amt_usd), 2) AS avg_gloss_usd,
            ROUND(AVG(o.poster_amt_usd), 2) AS avg_poster_usd,
            ROUND(AVG(o.total_amt_usd), 2) AS avg_total_usd
        FROM accounts ac
        JOIN orders o ON ac.id = o.account_id
        GROUP BY ac.name
        ORDER BY avg_total_usd DESC
        LIMIT 10;
    """).df()

    show(_df, title='Top 10 Accounts by Avg. Spend per Order')
    plot_hbar(_df, 'account_name', 'avg_total_usd',
              title='Top 10 Accounts — Avg. Spend per Order (USD)',
              xlabel='Average Spend (USD)',
              currency=True, fmt='${:,.0f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.8 &nbsp; Total Paper Sold by Type

    Standard paper is the best seller by a wide margin.
    """)
    return


@app.cell
def _(con, pd, plot_pie, show):
    _df = con.execute("""
        SELECT
            SUM(standard_qty) AS standard,
            SUM(gloss_qty) AS gloss,
            SUM(poster_qty) AS poster
        FROM orders;
    """).df()

    show(_df, title='Total Quantity Sold by Paper Type')

    # Reshape for pie chart
    _pie_df = pd.DataFrame({
        'paper_type': ['Standard', 'Gloss', 'Poster'],
        'quantity': [_df['standard'].iloc[0], _df['gloss'].iloc[0], _df['poster'].iloc[0]]
    })
    plot_pie(_pie_df, 'paper_type', 'quantity',
             title='Paper Sales Distribution (by Quantity)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.9 &nbsp; Revenue by Paper Type
    """)
    return


@app.cell
def _(con, pd, plot_pie, show):
    _df = con.execute("""
        SELECT
            SUM(standard_amt_usd) AS standard_usd,
            SUM(gloss_amt_usd) AS gloss_usd,
            SUM(poster_amt_usd) AS poster_usd
        FROM orders;
    """).df()

    show(_df, title='Total Revenue by Paper Type (USD)')

    _pie_df = pd.DataFrame({
        'paper_type': ['Standard', 'Gloss', 'Poster'],
        'revenue': [_df['standard_usd'].iloc[0], _df['gloss_usd'].iloc[0], _df['poster_usd'].iloc[0]]
    })
    plot_pie(_pie_df, 'paper_type', 'revenue',
             title='Revenue Distribution by Paper Type (USD)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.10 &nbsp; Unit Price Analysis

    For orders with > 100 standard papers and > 50 poster papers,
    what is the unit price each company pays?
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            r.name AS region,
            ac.name AS account_name,
            ROUND(o.total_amt_usd / (o.total + 0.01), 2) AS unit_price
        FROM region r
        JOIN sales_reps sr ON r.id = sr.region_id
        JOIN accounts ac ON sr.id = ac.sales_rep_id
        JOIN orders o ON ac.id = o.account_id
        WHERE o.standard_qty > 100
        AND o.poster_qty > 50
        ORDER BY unit_price DESC;
    """).df()

    show(_df, title='Unit Price (std > 100 & poster > 50)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.11 &nbsp; Walmart — Best Month for Gloss Paper

    In which month did Walmart spend the most on gloss paper?
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            ac.name AS account_name,
            EXTRACT(YEAR
        FROM o.occurred_at) AS year, EXTRACT(MONTH
        FROM o.occurred_at) AS month, SUM(o.gloss_amt_usd) AS gloss_total_usd
        FROM accounts ac
        JOIN orders o ON ac.id = o.account_id
        WHERE ac.name = 'Walmart'
        GROUP BY ac.name, year, month
        ORDER BY gloss_total_usd DESC
        LIMIT 1;
    """).df()

    show(_df, title='Walmart — Peak Gloss Spending Month')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.12 &nbsp; Midwest Sales Reps and Their Accounts
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            r.name AS region,
            sr.name AS rep_name,
            ac.name AS account_name
        FROM region r
        JOIN sales_reps sr ON r.id = sr.region_id
        JOIN accounts ac ON sr.id = ac.sales_rep_id
        WHERE r.name = 'Midwest'
        ORDER BY ac.name;
    """).df()

    show(_df, title='Midwest — Reps & Accounts')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.13 &nbsp; Web Event Channels per Sales Rep (Top 20)
    """)
    return


@app.cell
def _(con, show):
    _df = con.execute("""
        SELECT
            sr.name AS sales_rep,
            we.channel AS channel,
            COUNT(we.channel) AS occurrences
        FROM web_events we
        JOIN accounts ac ON we.account_id = ac.id
        JOIN sales_reps sr ON ac.sales_rep_id = sr.id
        GROUP BY sr.name, we.channel
        ORDER BY occurrences DESC
        LIMIT 20;
    """).df()

    show(_df, title='Top 20 — Channel Usage by Sales Rep')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 &nbsp; Additional Insights
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.1 &nbsp; Monthly Revenue Trend (2014-2016)

    Full-year data only — excludes partial years 2013 and 2017.
    """)
    return


@app.cell
def _(con, plot_line, show):
    _df = con.execute("""
        SELECT EXTRACT(YEAR
        FROM occurred_at) AS year, EXTRACT(MONTH
        FROM occurred_at) AS month, SUM(total_amt_usd) AS total_usd
        FROM orders
        WHERE EXTRACT(YEAR
        FROM occurred_at) BETWEEN 2014
        AND 2016
        GROUP BY year, month
        ORDER BY year, month;
    """).df()

    show(_df, title='Monthly Revenue 2014-2016')

    # Create a label like '2014-01'
    _df['period'] = _df['year'].astype(int).astype(str) + '-' + _df['month'].astype(int).astype(str).str.zfill(2)
    plot_line(_df, 'period', 'total_usd',
              title='Monthly Revenue Trend (2014–2016)',
              xlabel='Month', ylabel='Revenue (USD)',
              currency=True, annotate=False,
              figsize=(14, 5))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2 &nbsp; Total Revenue by Region
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT
            r.name AS region,
            SUM(o.total_amt_usd) AS total_usd,
            COUNT(o.id) AS order_count
        FROM region r
        JOIN sales_reps sr ON r.id = sr.region_id
        JOIN accounts ac ON sr.id = ac.sales_rep_id
        JOIN orders o ON ac.id = o.account_id
        GROUP BY r.name
        ORDER BY total_usd DESC;
    """).df()

    show(_df, title='Revenue by Region')
    plot_bar(_df, 'region', 'total_usd',
             title='Total Revenue by Region (USD)',
             xlabel='Region', ylabel='Revenue (USD)',
             currency=True, fmt='${:,.0f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.3 &nbsp; Top 10 Customers by Total Lifetime Spend
    """)
    return


@app.cell
def _(con, plot_hbar, show):
    _df = con.execute("""
        SELECT
            ac.name AS account_name,
            SUM(o.total_amt_usd) AS total_spend,
            COUNT(o.id) AS order_count
        FROM accounts ac
        JOIN orders o ON ac.id = o.account_id
        GROUP BY ac.name
        ORDER BY total_spend DESC
        LIMIT 10;
    """).df()

    show(_df, title='Top 10 Customers — Lifetime Spend')
    plot_hbar(_df, 'account_name', 'total_spend',
              title='Top 10 Customers — Total Spend (USD)',
              xlabel='Total Spend (USD)',
              currency=True, fmt='${:,.0f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.4 &nbsp; Bottom 10 Customers by Total Lifetime Spend
    """)
    return


@app.cell
def _(con, plot_hbar, show):
    _df = con.execute("""
        SELECT
            ac.name AS account_name,
            SUM(o.total_amt_usd) AS total_spend,
            COUNT(o.id) AS order_count
        FROM accounts ac
        JOIN orders o ON ac.id = o.account_id
        GROUP BY ac.name
        ORDER BY total_spend ASC
        LIMIT 10;
    """).df()

    show(_df, title='Bottom 10 Customers — Lifetime Spend')
    plot_hbar(_df, 'account_name', 'total_spend',
              title='Bottom 10 Customers — Total Spend (USD)',
              xlabel='Total Spend (USD)',
              currency=True, fmt='${:,.0f}',
              color='#C44E52')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.5 &nbsp; Top 10 Sales Reps by Revenue Generated
    """)
    return


@app.cell
def _(con, plot_hbar, show):
    _df = con.execute("""
        SELECT
            sr.name AS sales_rep,
            r.name AS region,
            SUM(o.total_amt_usd) AS total_revenue,
            COUNT(DISTINCT ac.id) AS num_accounts
        FROM sales_reps sr
        JOIN region r ON sr.region_id = r.id
        JOIN accounts ac ON ac.sales_rep_id = sr.id
        JOIN orders o ON o.account_id = ac.id
        GROUP BY sr.name, r.name
        ORDER BY total_revenue DESC
        LIMIT 10;
    """).df()

    show(_df, title='Top 10 Sales Reps — Revenue')
    plot_hbar(_df, 'sales_rep', 'total_revenue',
              title='Top 10 Sales Reps by Revenue (USD)',
              xlabel='Total Revenue (USD)',
              currency=True, fmt='${:,.0f}',
              color='#8172B3')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.6 &nbsp; Web Event Channel Distribution

    Which marketing channels drive the most web events?
    """)
    return


@app.cell
def _(con, plot_pie, show):
    _df = con.execute("""
        SELECT
            channel,
            COUNT(*) AS event_count
        FROM web_events
        GROUP BY channel
        ORDER BY event_count DESC;
    """).df()

    show(_df, title='Web Events by Channel')
    plot_pie(_df, 'channel', 'event_count',
             title='Web Event Channel Distribution')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.7 &nbsp; Revenue by Paper Type per Year (Stacked)

    How does the revenue mix evolve over time?
    """)
    return


@app.cell
def _(con, plot_stacked_bar, show):
    _df = con.execute("""
        SELECT EXTRACT(YEAR
        FROM occurred_at) AS year, SUM(standard_amt_usd) AS standard, SUM(gloss_amt_usd) AS gloss, SUM(poster_amt_usd) AS poster
        FROM orders
        GROUP BY year
        ORDER BY year;
    """).df()

    show(_df, title='Revenue by Paper Type per Year')
    plot_stacked_bar(_df, 'year', ['standard', 'gloss', 'poster'],
                     title='Revenue by Paper Type per Year (USD)',
                     xlabel='Year', ylabel='Revenue (USD)',
                     labels=['Standard', 'Gloss', 'Poster'],
                     currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.8 &nbsp; Number of Accounts per Region
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT
            r.name AS region,
            COUNT(ac.id) AS num_accounts
        FROM region r
        JOIN sales_reps sr ON r.id = sr.region_id
        JOIN accounts ac ON sr.id = ac.sales_rep_id
        GROUP BY r.name
        ORDER BY num_accounts DESC;
    """).df()

    show(_df, title='Accounts per Region')
    plot_bar(_df, 'region', 'num_accounts',
             title='Number of Accounts per Region',
             xlabel='Region', ylabel='# Accounts',
             color='#DD8452')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.9 &nbsp; Average Order Value by Region
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT
            r.name AS region,
            ROUND(AVG(o.total_amt_usd), 2) AS avg_order_value
        FROM region r
        JOIN sales_reps sr ON r.id = sr.region_id
        JOIN accounts ac ON sr.id = ac.sales_rep_id
        JOIN orders o ON ac.id = o.account_id
        GROUP BY r.name
        ORDER BY avg_order_value DESC;
    """).df()

    show(_df, title='Avg. Order Value by Region')
    plot_bar(_df, 'region', 'avg_order_value',
             title='Average Order Value by Region (USD)',
             xlabel='Region', ylabel='Avg. Order Value (USD)',
             currency=True, fmt='${:,.0f}',
             color='#55A868')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.10 &nbsp; Quarterly Revenue Trend (2014-2016)
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        SELECT EXTRACT(YEAR
        FROM occurred_at) AS year, EXTRACT(QUARTER
        FROM occurred_at) AS quarter, SUM(total_amt_usd) AS total_usd
        FROM orders
        WHERE EXTRACT(YEAR
        FROM occurred_at) BETWEEN 2014
        AND 2016
        GROUP BY year, quarter
        ORDER BY year, quarter;
    """).df()

    show(_df, title='Quarterly Revenue 2014-2016')

    _df['period'] = _df['year'].astype(int).astype(str) + '-Q' + _df['quarter'].astype(int).astype(str)
    plot_bar(_df, 'period', 'total_usd',
             title='Quarterly Revenue Trend (2014–2016)',
             xlabel='Quarter', ylabel='Revenue (USD)',
             currency=True, fmt='${:,.0f}',
             rotate_x=45, figsize=(12, 5))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.11 &nbsp; Top Customer in Each Region
    """)
    return


@app.cell
def _(con, plot_bar, show):
    _df = con.execute("""
        WITH ranked AS (
        SELECT
            r.name AS region,
            ac.name AS account_name,
            SUM(o.total_amt_usd) AS total_spend,
            ROW_NUMBER() OVER ( PARTITION BY r.name
        ORDER BY SUM(o.total_amt_usd) DESC ) AS rn
        FROM region r
        JOIN sales_reps sr ON r.id = sr.region_id
        JOIN accounts ac ON sr.id = ac.sales_rep_id
        JOIN orders o ON ac.id = o.account_id
        GROUP BY r.name, ac.name )
        SELECT
            region,
            account_name,
            total_spend
        FROM ranked
        WHERE rn = 1
        ORDER BY total_spend DESC;
    """).df()

    show(_df, title='Top Customer per Region')
    plot_bar(_df, 'region', 'total_spend',
             title='Top Customer Spend per Region (USD)',
             xlabel='Region', ylabel='Total Spend (USD)',
             currency=True, fmt='${:,.0f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.12 &nbsp; Web Events Over Time by Channel
    """)
    return


@app.cell
def _(con, plot_grouped_bar, show):
    _df = con.execute("""
        SELECT EXTRACT(YEAR
        FROM occurred_at) AS year, EXTRACT(MONTH
        FROM occurred_at) AS month, channel, COUNT(*) AS events
        FROM web_events
        WHERE EXTRACT(YEAR
        FROM occurred_at) BETWEEN 2014
        AND 2016
        GROUP BY year, month, channel
        ORDER BY year, month;
    """).df()

    # Pivot for grouped bar by year
    yearly = con.execute("""
        SELECT EXTRACT(YEAR
        FROM occurred_at) AS year, channel, COUNT(*) AS events
        FROM web_events
        WHERE EXTRACT(YEAR
        FROM occurred_at) BETWEEN 2014
        AND 2016
        GROUP BY year, channel
        ORDER BY year;
    """).df()

    pivot = yearly.pivot_table(index='year', columns='channel', values='events', fill_value=0).reset_index()
    channels = [c for c in pivot.columns if c != 'year']
    show(pivot, title='Web Events by Year and Channel')
    plot_grouped_bar(pivot, 'year', channels,
                     title='Web Events by Year and Channel',
                     xlabel='Year', ylabel='Event Count',
                     labels=channels)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 &nbsp; Conclusions

    1. **Sales are growing** — year-on-year there has been a steady increase, with a surge of over 150% from 2016 to 2017 (comparing Jan 1st figures).
    2. **2017 is on pace for record sales** — even with only two days of data, the Jan 1st total already exceeds prior years.
    3. **Standard paper dominates** — it accounts for the largest share of both quantity sold and revenue.
    4. **Pacific Life is the biggest spender** per order, while **State Farm** leads in volume.
    5. **Northeast region** drives the most revenue, followed by Southeast.
    6. **Direct channel** is the most common web-event type, but organic and social also play significant roles.
    7. **Unit prices vary** from ~\$5.12 (State Farm) to ~\$8.09 (IBM) for large orders — useful for pricing transparency and competitive analysis.
    """)
    return


if __name__ == "__main__":
    app.run()
