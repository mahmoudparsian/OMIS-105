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
    # Notebook 2 — SQL Queries Tutorial with Insurance Data
    ---
    **Database:** `insurance_db.duckdb` (built in Notebook 1)

    **Table:** `insurance` — columns: `age`, `gender`, `bmi`, `children`, `smoker`, `region`, `charges`

    We will explore SQL from simple `SELECT` statements all the way to window functions and CTEs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup — Connect & Add Derived Columns
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    from util_plot import (PALETTE, FIG_SMALL, FIG_MEDIUM, FIG_WIDE, FIG_TALL, plot_bar, plot_grouped_bar, plot_line, plot_scatter, plot_histogram, plot_boxplot, plot_pie, plot_heatmap, plot_stacked_bar, plot_lollipop, plot_multi_line, highlight_duplicates)
    con = duckdb.connect("insurance_db.duckdb")
    print("Connected to insurance_db.duckdb")
    con.execute("""
        SELECT COUNT(*) AS total_rows
        FROM insurance;
    """).df()
    return (con, plot_bar, plot_grouped_bar, plot_line, plot_lollipop, plot_pie)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.0 — Add Derived Columns

    We enrich the table with useful calculated columns:

    | Column | Definition |
    |--------|-----------|
    | `age_group` | 18-29, 30-39, 40-49, 50-64 |
    | `bmi_category` | Underweight / Normal / Overweight / Obese (WHO) |
    | `charge_level` | Low / Medium / High / Very High (quartile-based) |
    | `cost_per_child` | `charges / children` (NULL if no children) |
    """)
    return


@app.cell
def _(con):
    # Drop derived columns if they already exist (idempotent)
    for col in ['age_group', 'bmi_category', 'charge_level', 'cost_per_child']:
        try:
            con.execute(f"ALTER TABLE insurance DROP COLUMN {col}")
        except:
            pass

    con.execute("""
        ALTER TABLE insurance ADD COLUMN age_group VARCHAR;
    """)
    con.execute("""
        UPDATE insurance
        SET age_group = CASE WHEN age BETWEEN 18
        AND 29 THEN '18-29' WHEN age BETWEEN 30
        AND 39 THEN '30-39' WHEN age BETWEEN 40
        AND 49 THEN '40-49' ELSE '50-64' END;
    """)

    con.execute("""
        ALTER TABLE insurance ADD COLUMN bmi_category VARCHAR;
    """)
    con.execute("""
        UPDATE insurance
        SET bmi_category = CASE WHEN bmi < 18.5 THEN 'Underweight' WHEN bmi < 25.0 THEN 'Normal' WHEN bmi < 30.0 THEN 'Overweight' ELSE 'Obese' END;
    """)

    con.execute("""
        ALTER TABLE insurance ADD COLUMN charge_level VARCHAR;
    """)
    con.execute("""
        UPDATE insurance
        SET charge_level = CASE WHEN charges < 4740 THEN 'Low' WHEN charges < 9382 THEN 'Medium' WHEN charges < 16640 THEN 'High' ELSE 'Very High' END;
    """)

    con.execute("""
        ALTER TABLE insurance ADD COLUMN cost_per_child DOUBLE;
    """)
    con.execute("""
        UPDATE insurance
        SET cost_per_child = CASE WHEN children > 0 THEN ROUND(charges / children, 2) ELSE NULL END;
    """)

    print("Derived columns added!")
    con.execute("""
        SELECT *
        FROM insurance
        LIMIT 5;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 3.1 — Simple Queries
    These queries use basic `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, and `COUNT`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q1: How many rows are in the table?
    **Concept:** `COUNT(*)` — counts all rows in a table.
    """)
    return


@app.cell
def _(con):
    q1 = con.execute("""
        SELECT COUNT(*) AS total_rows
        FROM insurance;
    """).df()
    q1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q2: Show the 10 most expensive insurance charges
    **Concept:** `ORDER BY ... DESC` with `LIMIT` to get the top rows.
    """)
    return


@app.cell
def _(con):
    q2 = con.execute("""
        SELECT
            age,
            gender,
            smoker,
            region,
            charges
        FROM insurance
        ORDER BY charges DESC
        LIMIT 10;
    """).df()
    q2
    return (q2,)


@app.cell
def _(plot_bar, q2):
    plot_bar(q2, x="age", y="charges",
             title="Top 10 Most Expensive Insurance Charges",
             xlabel="Age", ylabel="Charges ($)",
             currency=True, color="#e74c3c")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q3: How many smokers vs. non-smokers?
    **Concept:** `GROUP BY` with `COUNT` for frequency counts.
    """)
    return


@app.cell
def _(con):
    q3 = con.execute("""
        SELECT
            smoker,
            COUNT(*) AS count
        FROM insurance
        GROUP BY smoker;
    """).df()
    q3
    return (q3,)


@app.cell
def _(plot_pie, q3):
    plot_pie(q3, labels_col="smoker", values_col="count",
             title="Smokers vs Non-Smokers")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q4: What are the distinct regions?
    **Concept:** `DISTINCT` — returns unique values in a column.
    """)
    return


@app.cell
def _(con):
    q4 = con.execute("""
        SELECT DISTINCT region
        FROM insurance
        ORDER BY region;
    """).df()
    q4
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q5: Find all records where charges exceed $40,000
    **Concept:** `WHERE` clause with a numeric comparison filter.
    """)
    return


@app.cell
def _(con):
    q5 = con.execute("""
        SELECT
            age,
            gender,
            bmi,
            smoker,
            region,
            charges
        FROM insurance
        WHERE charges > 50000
        ORDER BY charges DESC;
    """).df()
    print(f"Records with charges > $50,000: {len(q5)}")
    q5
    return (q5,)


@app.cell
def _(plot_bar, q5):
    plot_bar(q5, x="age", y="charges",
             title="Patients with Charges > $50,000",
             xlabel="Age", ylabel="Charges ($)",
             currency=True, color="#8e44ad")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 3.2 — Simple+ Queries
    These add `GROUP BY` with aggregation functions, `HAVING`, `BETWEEN`, `ROUND`, and multiple conditions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q6: Average charges by region
    **Concept:** `AVG()` aggregate with `GROUP BY` and `ROUND()` for formatting.
    """)
    return


@app.cell
def _(con):
    q6 = con.execute("""
        SELECT
            region,
            ROUND(AVG(charges), 2) AS avg_charges,
            COUNT(*) AS num_people
        FROM insurance
        GROUP BY region
        ORDER BY avg_charges DESC;
    """).df()
    q6
    return (q6,)


@app.cell
def _(plot_bar, q6):
    plot_bar(q6, x="region", y="avg_charges",
             title="Average Insurance Charges by Region",
             xlabel="Region", ylabel="Avg Charges ($)",
             currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q7: Average BMI by gender and smoker status
    **Concept:** Multiple columns in `GROUP BY` — cross-tabulation.
    """)
    return


@app.cell
def _(con):
    q7 = con.execute("""
        SELECT
            gender,
            smoker,
            ROUND(AVG(bmi), 2) AS avg_bmi,
            COUNT(*) AS count
        FROM insurance
        GROUP BY gender, smoker
        ORDER BY gender, smoker;
    """).df()
    q7
    return (q7,)


@app.cell
def _(plot_grouped_bar, q7):
    plot_grouped_bar(q7, x="gender", group_col="smoker", y="avg_bmi",
                     title="Average BMI by Gender and Smoker Status",
                     xlabel="Gender", ylabel="Avg BMI")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q8: Regions with average charges above $13,000
    **Concept:** `HAVING` — filters **after** aggregation (unlike `WHERE` which filters before).
    """)
    return


@app.cell
def _(con):
    q8 = con.execute("""
        SELECT
            region,
            ROUND(AVG(charges), 2) AS avg_charges
        FROM insurance
        GROUP BY region
        HAVING AVG(charges) > 13000
        ORDER BY avg_charges DESC;
    """).df()
    q8
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q9: Number of people in each age group
    **Concept:** Using a derived column (`age_group`) with `GROUP BY` and `COUNT`.
    """)
    return


@app.cell
def _(con):
    q9 = con.execute("""
        SELECT
            age_group,
            COUNT(*) AS count
        FROM insurance
        GROUP BY age_group
        ORDER BY age_group;
    """).df()
    q9
    return (q9,)


@app.cell
def _(plot_bar, q9):
    plot_bar(q9, x="age_group", y="count",
             title="Number of People by Age Group",
             xlabel="Age Group", ylabel="Count",
             color="#27ae60")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q10: Min, Max, and Average charges for smokers aged 30-50
    **Concept:** Combining `WHERE` with `BETWEEN` and multiple aggregate functions.
    """)
    return


@app.cell
def _(con):
    q10 = con.execute("""
        SELECT
            ROUND(MIN(charges), 2) AS min_charges,
            ROUND(AVG(charges), 2) AS avg_charges,
            ROUND(MAX(charges), 2) AS max_charges,
            COUNT(*) AS num_people
        FROM insurance
        WHERE smoker = 'yes'
        AND age BETWEEN 30
        AND 50;
    """).df()
    q10
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 3.3 — Intermediate Queries
    These introduce `CASE`, nested aggregation, `LIKE`, `IN`, and joining aggregates back to detail rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q11: Charges distribution by BMI category
    **Concept:** `CASE WHEN` (here via derived column) with multiple aggregates to profile a distribution.
    """)
    return


@app.cell
def _(con):
    q11 = con.execute("""
        SELECT
            bmi_category,
            COUNT(*) AS count,
            ROUND(AVG(charges), 2) AS avg_charges,
            ROUND(MIN(charges), 2) AS min_charges,
            ROUND(MAX(charges), 2) AS max_charges
        FROM insurance
        GROUP BY bmi_category
        ORDER BY avg_charges DESC;
    """).df()
    q11
    return (q11,)


@app.cell
def _(plot_bar, q11):
    plot_bar(q11, x="bmi_category", y="avg_charges",
             title="Average Charges by BMI Category",
             xlabel="BMI Category", ylabel="Avg Charges ($)",
             currency=True, color="#e67e22")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q12: Percentage of smokers by region
    **Concept:** Conditional aggregation with `SUM(CASE ...)` inside `GROUP BY` to compute percentages.
    """)
    return


@app.cell
def _(con):
    q12 = con.execute("""
        SELECT
            region,
            COUNT(*) AS total,
            SUM(CASE WHEN smoker = 'yes' THEN 1 ELSE 0 END) AS smokers,
            ROUND(100.0 * SUM(CASE WHEN smoker = 'yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS smoker_pct
        FROM insurance
        GROUP BY region
        ORDER BY smoker_pct DESC;
    """).df()
    q12
    return (q12,)


@app.cell
def _(plot_bar, q12):
    plot_bar(q12, x="region", y="smoker_pct",
             title="Percentage of Smokers by Region",
             xlabel="Region", ylabel="Smoker %",
             color="#c0392b", fmt="{:.1f}%")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q13: Average charges by age group AND smoker status
    **Concept:** Two-dimensional `GROUP BY` — the foundation of pivot-table thinking in SQL.
    """)
    return


@app.cell
def _(con):
    q13 = con.execute("""
        SELECT
            age_group,
            smoker,
            ROUND(AVG(charges), 2) AS avg_charges
        FROM insurance
        GROUP BY age_group, smoker
        ORDER BY age_group, smoker;
    """).df()
    q13
    return (q13,)


@app.cell
def _(plot_grouped_bar, q13):
    plot_grouped_bar(q13, x="age_group", group_col="smoker", y="avg_charges",
                     title="Average Charges: Age Group x Smoker Status",
                     xlabel="Age Group", ylabel="Avg Charges ($)",
                     currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q14: People who pay more than the average charge
    **Concept:** **Scalar subquery** — using a `SELECT` inside `WHERE` to compare each row against a global aggregate.
    """)
    return


@app.cell
def _(con):
    q14 = con.execute("""
        SELECT
            age,
            gender,
            smoker,
            region,
            charges
        FROM insurance
        WHERE charges > (
        SELECT AVG(charges)
        FROM insurance)
        ORDER BY charges DESC
        LIMIT 15;
    """).df()
    print(f"People above average: shown top 15")
    q14
    return


@app.cell
def _(con, plot_bar):
    # Show how above-average patients distribute across regions
    q14_summary = con.execute("""
        SELECT
            region,
            COUNT(*) AS above_avg_count
        FROM insurance
        WHERE charges > (
        SELECT AVG(charges)
        FROM insurance)
        GROUP BY region
        ORDER BY above_avg_count DESC;
    """).df()

    plot_bar(q14_summary, x="region", y="above_avg_count",
             title="Above-Average Charges: Count by Region",
             xlabel="Region", ylabel="Count",
             color="#2980b9")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q15: Charges spread — standard deviation by region and smoker status
    **Concept:** `STDDEV()` aggregate — measures how spread out the charges are within each group.
    """)
    return


@app.cell
def _(con):
    q15 = con.execute("""
        SELECT
            region,
            smoker,
            COUNT(*) AS n,
            ROUND(AVG(charges), 2) AS mean,
            ROUND(STDDEV(charges), 2) AS std_dev
        FROM insurance
        GROUP BY region, smoker
        ORDER BY std_dev DESC;
    """).df()
    q15
    return (q15,)


@app.cell
def _(plot_grouped_bar, q15):
    plot_grouped_bar(q15, x="region", group_col="smoker", y="std_dev",
                     title="Standard Deviation of Charges by Region & Smoker",
                     xlabel="Region", ylabel="Std Dev ($)",
                     currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 3.4 — Intermediate+ Queries
    **Advanced concepts:** Top-N per group, `RANK()` / `DENSE_RANK()` / `ROW_NUMBER()` window functions, and Common Table Expressions (`WITH`).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q16: Top 3 most expensive patients per region (Window Function)
    **Concept:** `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` assigns a row number within each partition. Wrapping it in a CTE (`WITH`) lets us filter by that number.
    """)
    return


@app.cell
def _(con):
    q16 = con.execute("""
        WITH ranked AS (
        SELECT
            age,
            gender,
            smoker,
            region,
            charges,
            ROW_NUMBER() OVER ( PARTITION BY region
        ORDER BY charges DESC ) AS rn
        FROM insurance )
        SELECT
            region,
            age,
            gender,
            smoker,
            ROUND(charges, 2) AS charges,
            rn AS rank
        FROM ranked
        WHERE rn <= 3
        ORDER BY region, rn;
    """).df()
    q16
    return (q16,)


@app.cell
def _(plot_grouped_bar, q16):
    plot_grouped_bar(q16, x="region", group_col="rank", y="charges",
                     title="Top 3 Most Expensive Patients per Region",
                     xlabel="Region", ylabel="Charges ($)",
                     currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q17: Rank regions by total charges using DENSE_RANK
    **Concept:** `DENSE_RANK()` — like `RANK()` but without gaps. Here we rank regions by their total charges in a CTE, then display.
    """)
    return


@app.cell
def _(con):
    q17 = con.execute("""
        WITH region_totals AS (
        SELECT
            region,
            ROUND(SUM(charges), 2) AS total_charges,
            COUNT(*) AS num_people
        FROM insurance
        GROUP BY region )
        SELECT
            region,
            total_charges,
            num_people,
            DENSE_RANK() OVER (
        ORDER BY total_charges DESC) AS rank
        FROM region_totals
        ORDER BY RANK;
    """).df()
    q17
    return (q17,)


@app.cell
def _(plot_lollipop, q17):
    plot_lollipop(q17, x="region", y="total_charges",
                  title="Regions Ranked by Total Insurance Charges",
                  xlabel="Total Charges ($)", ylabel="Region",
                  currency=True, color="#16a085")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q18: Each person's charges vs. their region's average (CTE + Window)
    **Concept:** CTE computes the region average; we then join it back to compute the difference. Shows how each person compares to their regional peers.
    """)
    return


@app.cell
def _(con):
    q18 = con.execute("""
        WITH region_avg AS (
        SELECT
            region,
            ROUND(AVG(charges), 2) AS avg_charges
        FROM insurance
        GROUP BY region )
        SELECT
            i.age,
            i.gender,
            i.smoker,
            i.region,
            ROUND(i.charges, 2) AS charges,
            ra.avg_charges AS region_avg,
            ROUND(i.charges - ra.avg_charges, 2) AS diff_from_avg
        FROM insurance i
        JOIN region_avg ra ON i.region = ra.region
        ORDER BY diff_from_avg DESC
        LIMIT 15;
    """).df()
    q18
    return (q18,)


@app.cell
def _(plot_bar, q18):
    plot_bar(q18, x="age", y="diff_from_avg",
             title="Top 15: Charges Above Their Region's Average",
             xlabel="Patient Age", ylabel="Difference ($)",
             currency=True, color="#d35400")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q19: Running total of charges by age (Cumulative Sum)
    **Concept:** `SUM() OVER (ORDER BY ...)` — a running (cumulative) aggregate. Shows how total charges accumulate as age increases.
    """)
    return


@app.cell
def _(con):
    q19 = con.execute("""
        WITH age_totals AS (
        SELECT
            age,
            ROUND(SUM(charges), 2) AS age_charges
        FROM insurance
        GROUP BY age )
        SELECT
            age,
            age_charges,
            ROUND(SUM(age_charges) OVER (
        ORDER BY age), 2) AS running_total
        FROM age_totals
        ORDER BY age;
    """).df()
    q19.head(15)
    return (q19,)


@app.cell
def _(plot_line, q19):
    plot_line(q19, x="age", y="running_total",
              title="Cumulative Insurance Charges by Age",
              xlabel="Age", ylabel="Running Total ($)",
              currency=True, marker=None)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q20: Percentile ranking of each person's charges within their age group
    **Concept:** `PERCENT_RANK()` — gives each row a value 0–1 indicating what percentage of its group has lower values. Combined with `NTILE(4)` for quartile assignment.
    """)
    return


@app.cell
def _(con):
    q20 = con.execute("""
        WITH pctiles AS (
        SELECT
            age,
            gender,
            smoker,
            age_group,
            ROUND(charges, 2) AS charges,
            ROUND(PERCENT_RANK() OVER ( PARTITION BY age_group
        ORDER BY charges ), 3) AS pct_rank, NTILE(4) OVER ( PARTITION BY age_group
        ORDER BY charges ) AS quartile
        FROM insurance )
        SELECT *
        FROM pctiles
        ORDER BY age_group, pct_rank DESC
        LIMIT 20;
    """).df()
    q20
    return


@app.cell
def _(con, plot_grouped_bar):
    # Show charge level distribution across age groups
    q20_viz = con.execute("""
        SELECT
            age_group,
            charge_level,
            COUNT(*) AS count
        FROM insurance
        GROUP BY age_group, charge_level
        ORDER BY age_group, charge_level;
    """).df()

    plot_grouped_bar(q20_viz, x="age_group", group_col="charge_level", y="count",
                     title="Charge Level Distribution by Age Group",
                     xlabel="Age Group", ylabel="Count")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 3.5 — Key SQL Concepts Summary

    This section consolidates the SQL concepts demonstrated throughout this notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Concept 1: SELECT, WHERE, ORDER BY, LIMIT
    The most basic SQL pattern — retrieve rows, filter them, sort them, and take the first N.

    ```sql
    SELECT   column1, column2
    FROM     table_name
    WHERE    condition
    ORDER BY column1 DESC
    LIMIT    10
    ```
    **Used in:** Q1, Q2, Q4, Q5
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Concept 2: GROUP BY + Aggregate Functions
    Collapse many rows into summary rows using `COUNT`, `AVG`, `SUM`, `MIN`, `MAX`, `STDDEV`.

    ```sql
    SELECT   group_col, COUNT(*) AS n, AVG(value_col) AS avg_val
    FROM     table_name
    GROUP BY group_col
    HAVING   COUNT(*) > 10    -- filter AFTER aggregation
    ```
    **Used in:** Q3, Q6, Q7, Q8, Q9, Q10, Q12, Q15

    **Key distinction:** `WHERE` filters rows *before* grouping; `HAVING` filters groups *after* aggregation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Concept 3: CASE WHEN (Conditional Logic)
    SQL's if/else — used to create categories, flag conditions, or do conditional aggregation.

    ```sql
    SELECT CASE
        WHEN age < 30  THEN 'Young'
        WHEN age < 50  THEN 'Middle'
        ELSE 'Senior'
    END AS age_category
    ```
    **Used in:** Q12 (conditional aggregation), derived columns (age_group, bmi_category, charge_level)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Concept 4: Subqueries
    A query inside another query. Can appear in `WHERE`, `FROM`, or `SELECT`.

    ```sql
    -- Scalar subquery in WHERE
    SELECT * FROM insurance
    WHERE charges > (SELECT AVG(charges) FROM insurance)
    ```
    **Used in:** Q14
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Concept 5: Common Table Expressions (WITH / CTE)
    Named temporary result sets that make complex queries readable and composable.

    ```sql
    WITH summary AS (
        SELECT region, AVG(charges) AS avg_charges
        FROM   insurance
        GROUP BY region
    )
    SELECT i.*, s.avg_charges
    FROM   insurance i
    JOIN   summary s ON i.region = s.region
    ```
    **Used in:** Q16, Q17, Q18, Q19, Q20

    **Why use CTEs?** They replace deeply nested subqueries with named, readable steps — like assigning intermediate variables.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Concept 6: Window Functions
    Perform calculations across related rows **without collapsing** them (unlike `GROUP BY`).

    | Function | Purpose |
    |----------|---------|
    | `ROW_NUMBER()` | Unique sequential number per partition |
    | `RANK()` | Rank with gaps on ties |
    | `DENSE_RANK()` | Rank without gaps on ties |
    | `PERCENT_RANK()` | Relative rank as 0–1 fraction |
    | `NTILE(n)` | Divide partition into n equal buckets |
    | `SUM() OVER (ORDER BY ...)` | Running (cumulative) total |

    ```sql
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY region ORDER BY charges DESC) AS rn
    FROM insurance
    ```
    **Used in:** Q16, Q17, Q19, Q20
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Concept 7: JOINs
    Combine rows from two tables (or a table with a CTE) based on a matching condition.

    ```sql
    SELECT i.*, ra.avg_charges
    FROM   insurance i
    JOIN   region_avg ra ON i.region = ra.region
    ```
    **Used in:** Q18

    In this notebook we used a self-join pattern (joining the table to an aggregate of itself via a CTE).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Congratulations!
    You've worked through **20 SQL queries** covering:
    - Basic selection, filtering, sorting
    - Aggregation and grouping
    - Conditional logic and subqueries
    - CTEs and window functions
    - Ranking, percentiles, and cumulative sums

    These concepts form the foundation of SQL proficiency for data analysis.
    """)
    return


if __name__ == "__main__":
    app.run()
