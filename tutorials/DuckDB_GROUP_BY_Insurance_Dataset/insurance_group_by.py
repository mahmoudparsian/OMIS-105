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
    # 🦆 Mastering SQL `GROUP BY` with DuckDB
    ### Insurance Dataset — 1,800 Rows of Real-World Data

    ---

    > **Learning Goal:** Understand how `GROUP BY` collapses many rows into summary groups — and how to combine it with aggregate functions like `COUNT`, `AVG`, `SUM`, `MIN`, and `MAX`.

    **Files needed in the same folder:**
    ```
    📄 insurance_groupby_v3.ipynb   ← this notebook
    📄 insurance_plots.py           ← all plotting functions (don't edit)
    📄 insurance.csv                ← the dataset
    ```

    **Dataset columns:**
    | Column | Type | Description |
    |---|---|---|
    | `age` | integer | Age of the insured |
    | `gender` | string | `male` / `female` |
    | `bmi` | float | Body Mass Index |
    | `num_children` | integer | Number of dependents |
    | `smoker` | string | `yes` / `no` |
    | `region` | string | US region (`northeast`, `northwest`, `southeast`, `southwest`) |
    | `charges` | float | Insurance charges billed ($) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ⚙️ Setup — Install, Import & Load Data
    Run this cell once before anything else.
    """)
    return


@app.cell
def _():

    import duckdb
    import pandas as pd
    import warnings
    warnings.filterwarnings('ignore')

    # ── Import everything from our plotting module ────────────────────────────────
    from plots_util import (
        setup_style, styled_table,
        plot_histogram, plot_bar_2col, plot_single_bar, plot_pie_bar,
        plot_avg_median, plot_hbar, plot_grouped_bar, plot_line_fill,
        plot_hbar_threshold, plot_bmi_bar, plot_top5, plot_age_range,
        plot_error_bar, plot_rollup_stacked, plot_rank_hbar, plot_bubble,
        PALETTE
    )

    setup_style()   # apply dark theme

    # ── Connect DuckDB & load CSV ─────────────────────────────────────────────────
    con = duckdb.connect()
    con.execute("""
        CREATE TABLE insurance AS
        SELECT *
        FROM read_csv_auto('insurance.csv', types={'smoker': 'VARCHAR'});
    """)
    total = con.execute("""
        SELECT COUNT(*)
        FROM insurance;
    """).fetchone()[0]
    print(f'✅  Loaded {total:,} rows into DuckDB table  →  insurance')
    con.execute("""
        DESCRIBE insurance;
    """).df()
    return (PALETTE, con, plot_age_range, plot_avg_median, plot_bar_2col, plot_bmi_bar, plot_bubble, plot_error_bar, plot_grouped_bar, plot_hbar, plot_hbar_threshold, plot_histogram, plot_line_fill, plot_pie_bar, plot_rank_hbar, plot_rollup_stacked, plot_single_bar, plot_top5, styled_table)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 1 — Basic Statistics (No GROUP BY yet)
    **What are we doing?**  
    Before we group anything, let's see the overall summary statistics for the whole dataset — min, max, average, count, and standard deviation.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            COUNT(*) AS total_rows,
            ROUND(AVG(age), 1) AS avg_age,
            ROUND(AVG(bmi), 2) AS avg_bmi,
            ROUND(AVG(charges), 2) AS avg_charges,
            ROUND(MIN(charges), 2) AS min_charges,
            ROUND(MAX(charges), 2) AS max_charges,
            ROUND(STDDEV(charges), 2) AS stddev_charges
        FROM insurance;
    """
    df_1 = con.execute(_sql).df()
    styled_table(df_1)
    return (df_1,)


@app.cell
def _(con, plot_histogram):
    charges = con.execute("""
        SELECT charges
        FROM insurance;
    """).df()['charges']
    plot_histogram(charges, title='Distribution of Insurance Charges')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 2 — GROUP BY One Column: Count by Gender
    **What are we doing?**  
    How many policies does each gender hold? We `GROUP BY gender` and count the rows in each group.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            gender,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge
        FROM insurance
        GROUP BY gender
        ORDER BY num_policies DESC;
    """
    df_2 = con.execute(_sql).df()
    styled_table(df_2)
    return (df_2,)


@app.cell
def _(df_2, plot_bar_2col):
    plot_bar_2col(df_2, x='gender', y1='num_policies', y2='avg_charge',
                  label1='Policy Count by Gender',
                  label2='Avg Charge by Gender',
                  title='Gender Analysis')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 3 — GROUP BY One Column: Avg Charges by Smoker Status
    **What are we doing?**  
    Does smoking significantly raise insurance costs? We `GROUP BY smoker` and compare average charges between the two groups.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            smoker,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge,
            ROUND(MIN(charges), 2) AS min_charge,
            ROUND(MAX(charges), 2) AS max_charge
        FROM insurance
        GROUP BY smoker
        ORDER BY avg_charge DESC;
    """
    df_3 = con.execute(_sql).df()
    styled_table(df_3)
    return (df_3,)


@app.cell
def _(df_3, plot_single_bar):
    plot_single_bar(df_3, x='smoker', y='avg_charge',
                    title='Avg Charges by Smoking Status')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 4 — GROUP BY One Column: Policies by Region
    **What are we doing?**  
    How is the customer base distributed across the four US regions? We `GROUP BY region` and count policies and sum charges.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            region,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge,
            ROUND(SUM(charges), 2) AS total_charges
        FROM insurance
        GROUP BY region
        ORDER BY total_charges DESC;
    """
    df_4 = con.execute(_sql).df()
    styled_table(df_4)
    return (df_4,)


@app.cell
def _(df_4, plot_pie_bar):
    plot_pie_bar(df_4, x='region', count_col='num_policies',
                 charge_col='total_charges', title='Regional Distribution')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 5 — GROUP BY One Column: Charges by Number of Children
    **What are we doing?**  
    Does having more dependents increase your premium? We `GROUP BY num_children` and compare average vs median charges.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            num_children,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge,
            ROUND(MEDIAN(charges), 2) AS median_charge
        FROM insurance
        GROUP BY num_children
        ORDER BY num_children;
    """
    df_5 = con.execute(_sql).df()
    styled_table(df_5)
    return (df_5,)


@app.cell
def _(df_5, plot_avg_median):
    plot_avg_median(df_5, x='num_children', avg_col='avg_charge',
                    median_col='median_charge',
                    title='Avg vs Median Charges by Number of Children')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 6 — GROUP BY with CASE: Age Buckets
    **What are we doing?**  
    We bucket continuous `age` values into life-stage groups using `CASE`, then `GROUP BY` that derived column to see how charges scale with age.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            CASE WHEN age < 25 THEN '18-24  Young Adult' WHEN age < 35 THEN '25-34  Early Career' WHEN age < 45 THEN '35-44  Mid Career' WHEN age < 55 THEN '45-54  Late Career' ELSE '55+    Pre-Retirement' END AS age_group,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge,
            ROUND(SUM(charges), 0) AS total_charges
        FROM insurance
        GROUP BY age_group
        ORDER BY MIN(age);
    """
    df_6 = con.execute(_sql).df()
    styled_table(df_6)
    return (df_6,)


@app.cell
def _(df_6, plot_hbar):
    plot_hbar(df_6, x='age_group', y='avg_charge',
              title='Average Charges by Age Group')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 7 — GROUP BY Two Columns: Region x Gender
    **What are we doing?**  
    We combine two dimensions — `region` AND `gender` — to see if gender differences in charges vary by geography.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            region,
            gender,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge
        FROM insurance
        GROUP BY region, gender
        ORDER BY region, gender;
    """
    df_7 = con.execute(_sql).df()
    styled_table(df_7)
    return (df_7,)


@app.cell
def _(PALETTE, df_7, plot_grouped_bar):
    plot_grouped_bar(df_7, index_col='region', col_col='gender',
                     val_col='avg_charge',
                     title='Avg Charges - Region x Gender',
                     colors=[PALETTE[1], PALETTE[0]])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 8 — GROUP BY Two Columns: Smoker x Gender
    **What are we doing?**  
    Is the smoking penalty the same for men and women? We `GROUP BY smoker, gender` to reveal the interaction.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            smoker,
            gender,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge,
            ROUND(SUM(charges), 0) AS total_charges
        FROM insurance
        GROUP BY smoker, gender
        ORDER BY smoker DESC, gender;
    """
    df_8 = con.execute(_sql).df()
    styled_table(df_8)
    return (df_8,)


@app.cell
def _(PALETTE, df_8, plot_grouped_bar):
    plot_grouped_bar(df_8, index_col='smoker', col_col='gender',
                     val_col='avg_charge',
                     title='Smoking x Gender - Who Pays Most?',
                     colors=[PALETTE[1], PALETTE[0]], xlabel='Smoker')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 9 — GROUP BY Two Columns: Region x Smoker
    **What are we doing?**  
    Do some regions have more smokers, and does that drive up regional costs? We `GROUP BY region, smoker`.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            region,
            smoker,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge
        FROM insurance
        GROUP BY region, smoker
        ORDER BY region, smoker DESC;
    """
    df_9 = con.execute(_sql).df()
    styled_table(df_9)
    return (df_9,)


@app.cell
def _(df_9, plot_grouped_bar):
    plot_grouped_bar(df_9, index_col='region', col_col='smoker',
                     val_col='avg_charge',
                     title='Avg Charges - Region x Smoker Status',
                     colors=['#2a9d8f', '#e76f51'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 10 — GROUP BY Two Columns: Age Group x Smoker
    **What are we doing?**  
    Does the cost of smoking compound as you age? We combine the `age_group` bucket with `smoker` status.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            CASE WHEN age < 25 THEN '18-24' WHEN age < 35 THEN '25-34' WHEN age < 45 THEN '35-44' WHEN age < 55 THEN '45-54' ELSE '55+' END AS age_group,
            smoker,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge
        FROM insurance
        GROUP BY age_group, smoker
        ORDER BY MIN(age), smoker DESC;
    """
    df_10 = con.execute(_sql).df()
    styled_table(df_10)
    return (df_10,)


@app.cell
def _(df_10, plot_line_fill):
    plot_line_fill(df_10, index_col='age_group', col_col='smoker',
                   val_col='avg_charge',
                   title='How Smoking Costs Grow with Age',
                   col_low='no', col_high='yes')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 11 — GROUP BY + HAVING: Filter Groups After Aggregating
    **What are we doing?**  
    `HAVING` is `WHERE` *for groups* — it filters after aggregation. Here we keep only region-gender groups whose average charge exceeds $14,000.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            region,
            gender,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge
        FROM insurance
        GROUP BY region, gender
        HAVING AVG(charges) > 14000
        ORDER BY avg_charge DESC;
    """
    df_11 = con.execute(_sql).df()
    styled_table(df_11)
    return (df_11,)


@app.cell
def _(df_11, plot_hbar_threshold):
    plot_hbar_threshold(df_11, x=['region', 'gender'], y='avg_charge',
                        threshold=14000,
                        title='Groups with Avg Charge > $14,000  (HAVING clause)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 12 — GROUP BY Two Columns: BMI Tier x Smoker
    **What are we doing?**  
    We bucket BMI into WHO categories with `CASE`, then cross it with `smoker` — a classic risk-factor interaction query.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            CASE WHEN bmi < 18.5 THEN '1 Underweight  (<18.5)' WHEN bmi < 25.0 THEN '2 Normal        (18.5-24.9)' WHEN bmi < 30.0 THEN '3 Overweight    (25-29.9)' ELSE '4 Obese         (30+)' END AS bmi_category,
            smoker,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge
        FROM insurance
        GROUP BY bmi_category, smoker
        ORDER BY bmi_category, smoker DESC;
    """
    df_12 = con.execute(_sql).df()
    styled_table(df_12)
    return (df_12,)


@app.cell
def _(df_12, plot_bmi_bar):
    plot_bmi_bar(df_12, index_col='bmi_category', col_col='smoker',
                 val_col='avg_charge',
                 short_labels=['Underweight', 'Normal', 'Overweight', 'Obese'],
                 title='BMI Category x Smoking - Avg Charges')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 13 — GROUP BY Two Columns: Children x Smoker
    **What are we doing?**  
    Do smokers with many kids pay dramatically more? We `GROUP BY num_children, smoker` to reveal the compounded risk.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            num_children,
            smoker,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge
        FROM insurance
        GROUP BY num_children, smoker
        ORDER BY num_children, smoker DESC;
    """
    df_13 = con.execute(_sql).df()
    styled_table(df_13)
    return (df_13,)


@app.cell
def _(df_13, plot_grouped_bar):
    plot_grouped_bar(df_13, index_col='num_children', col_col='smoker',
                     val_col='avg_charge',
                     title='Avg Charges - Children x Smoker Status',
                     colors=['#2a9d8f', '#e76f51'], xlabel='Number of Children')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 14 — GROUP BY + ORDER BY + LIMIT: Top 5 Most Expensive Groups
    **What are we doing?**  
    Which 5 specific region-smoker-gender combinations have the highest average charges? We use `ORDER BY` and `LIMIT` after `GROUP BY` to get the top-N.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            region,
            smoker,
            gender,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge
        FROM insurance
        GROUP BY region, smoker, gender
        ORDER BY avg_charge DESC
        LIMIT 5;
    """
    df_14 = con.execute(_sql).df()
    styled_table(df_14)
    return (df_14,)


@app.cell
def _(df_14, plot_top5):
    plot_top5(df_14, x_cols=['region', 'smoker', 'gender'],
              y='avg_charge',
              title='Top 5 Most Expensive Region-Smoker-Gender Groups')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 15 — GROUP BY + COUNT DISTINCT: Unique Ages per Region
    **What are we doing?**  
    `COUNT(DISTINCT col)` counts *unique* values within each group. Here we measure how many distinct ages appear in each region.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            region,
            COUNT(*) AS num_policies,
            COUNT(DISTINCT age) AS distinct_ages,
            MIN(age) AS youngest,
            MAX(age) AS oldest,
            ROUND(AVG(age), 1) AS avg_age
        FROM insurance
        GROUP BY region
        ORDER BY distinct_ages DESC;
    """
    df_15 = con.execute(_sql).df()
    styled_table(df_15)
    return (df_15,)


@app.cell
def _(df_15, plot_age_range):
    plot_age_range(df_15, region_col='region', min_col='youngest',
                   max_col='oldest', avg_col='avg_age',
                   title='Age Range per Region')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 16 — GROUP BY Two Columns: Region x Number of Children
    **What are we doing?**  
    Are large families concentrated in specific regions? We `GROUP BY region, num_children` to count policies per family-size bracket per region.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            region,
            num_children,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge
        FROM insurance
        GROUP BY region, num_children
        ORDER BY region, num_children;
    """
    df_16 = con.execute(_sql).df()
    styled_table(df_16)
    return (df_16,)


@app.cell
def _(PALETTE, df_16, plot_grouped_bar):
    plot_grouped_bar(df_16, index_col='num_children', col_col='region',
                     val_col='num_policies',
                     title='Policy Count - Children x Region',
                     colors=PALETTE[:4], xlabel='Number of Children')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 17 — Multiple Aggregates: Full Region Summary
    **What are we doing?**  
    One `GROUP BY` can compute many aggregate functions at once. Here we build a complete financial snapshot per region: count, sum, mean, median, stddev, min, max.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            region,
            COUNT(*) AS policies,
            ROUND(SUM(charges), 0) AS total_revenue,
            ROUND(AVG(charges), 2) AS avg_charge,
            ROUND(MEDIAN(charges), 2) AS median_charge,
            ROUND(STDDEV(charges), 2) AS stddev_charge,
            ROUND(MIN(charges), 2) AS min_charge,
            ROUND(MAX(charges), 2) AS max_charge
        FROM insurance
        GROUP BY region
        ORDER BY total_revenue DESC;
    """
    df_17 = con.execute(_sql).df()
    styled_table(df_17)
    return (df_17,)


@app.cell
def _(df_17, plot_error_bar):
    plot_error_bar(df_17, x='region', bar_col='total_revenue',
                   avg_col='avg_charge', err_col='stddev_charge',
                   title='Total Revenue + Avg+-StdDev by Region')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 18 — GROUP BY ROLLUP: Subtotals & Grand Total
    **What are we doing?**  
    `GROUP BY ROLLUP(a, b)` automatically adds a subtotal row for each group of `a`, plus a grand-total row — multi-level summaries in a single query.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        SELECT
            COALESCE(region, '-- ALL REGIONS --') AS region,
            COALESCE(CAST(smoker AS VARCHAR), '-- ALL --') AS smoker,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge,
            ROUND(SUM(charges), 0) AS total_charges
        FROM insurance
        GROUP BY ROLLUP(region, smoker)
        ORDER BY region, smoker;
    """
    df_18 = con.execute(_sql).df()
    styled_table(df_18)
    return (df_18,)


@app.cell
def _(df_18, plot_rollup_stacked):
    plot_rollup_stacked(df_18, region_col='region', smoker_col='smoker',
                        val_col='total_charges',
                        title='ROLLUP - Stacked Total Charges by Region')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 19 — GROUP BY + Window Function: Rank within Groups
    **What are we doing?**  
    We combine `GROUP BY` (in a CTE) with `RANK() OVER (PARTITION BY ...)` to rank each region by average charge *within* each smoker cohort.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        WITH base AS (
        SELECT
            region,
            smoker,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge
        FROM insurance
        GROUP BY region, smoker )
        SELECT
            region,
            smoker,
            num_policies,
            avg_charge,
            RANK() OVER ( PARTITION BY smoker
        ORDER BY avg_charge DESC ) AS rank_within_smoker_group
        FROM base
        ORDER BY smoker DESC, rank_within_smoker_group;
    """
    df_19 = con.execute(_sql).df()
    styled_table(df_19)
    return (df_19,)


@app.cell
def _(df_19, plot_rank_hbar):
    plot_rank_hbar(df_19, region_col='region', smoker_col='smoker',
                   val_col='avg_charge', rank_col='rank_within_smoker_group',
                   title='RANK() OVER - Region Rank within Smoker Group')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Cell 20 — The Grand Finale: Everything Together
    **What are we doing?**  
    Our final query combines three `GROUP BY` dimensions, six aggregate functions, a `HAVING` filter, and a window `RANK()` — all in one clean SQL statement.
    """)
    return


@app.cell
def _(con, styled_table):
    _sql = """
        WITH grouped AS (
        SELECT
            region,
            smoker,
            gender,
            COUNT(*) AS num_policies,
            ROUND(AVG(charges), 2) AS avg_charge,
            ROUND(MEDIAN(charges),2) AS median_charge,
            ROUND(MIN(charges), 2) AS min_charge,
            ROUND(MAX(charges), 2) AS max_charge,
            ROUND(SUM(charges), 0) AS total_charges,
            ROUND(STDDEV(charges),2) AS stddev_charge
        FROM insurance
        GROUP BY region, smoker, gender
        HAVING COUNT(*) >= 15 )
        SELECT
            *,
            RANK() OVER (
        ORDER BY avg_charge DESC) AS overall_rank
        FROM grouped
        ORDER BY overall_rank;
    """
    df_20 = con.execute(_sql).df()
    styled_table(df_20)
    return (df_20,)


@app.cell
def _(df_20, plot_bubble):
    plot_bubble(df_20, x_col='overall_rank', y_col='avg_charge',
                size_col='num_policies', color_col='total_charges',
                label_cols=['region', 'smoker', 'gender'],
                rank_col='overall_rank',
                title='Grand Summary - All Groups Ranked\n(bubble size = policy count | color = total revenue)')

    print('\n Congratulations!  You have now mastered SQL GROUP BY!')
    print('   Key takeaways:')
    print('   * GROUP BY collapses many rows into one row per unique group value')
    print('   * Every SELECT column must be in GROUP BY or inside an aggregate function')
    print('   * HAVING filters AFTER aggregation  (WHERE filters BEFORE)')
    print('   * ROLLUP adds automatic subtotal / grand-total rows')
    print('   * Window functions (RANK, ROW_NUMBER) operate ON TOP of group results')
    return


if __name__ == "__main__":
    app.run()
