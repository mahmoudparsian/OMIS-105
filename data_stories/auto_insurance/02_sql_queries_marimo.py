import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook 2: SQL Queries on the Auto Insurance Database

    **Objective:** Learn SQL through progressively harder queries <br>
    on the `insurance` table in our DuckDB database.

    * We move from simple SELECT statements through aggregations, <br>
    joins, window functions, CTEs, and analytical segmentation.

    **Prerequisites:** Run `01_data_cleaning_and_db_creation.ipynb` first to create `auto_insurance_db.duckdb`.

    **Difficulty Levels:**
    - **3.1 Simple** — SELECT, WHERE, ORDER BY, LIMIT
    - **3.2 Simple+** — GROUP BY, aggregate functions (COUNT, AVG, SUM)
    - **3.3 Intermediate** — CASE, multi-column GROUP BY, HAVING, nested filters
    - **3.4 Intermediate+** — Top-N, window/ranking functions, CTEs (WITH)
    - **3.5 Key SQL Concepts** — Derived columns, segmentation, percentiles

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    from util_plot import plot_bar, plot_grouped_bar, plot_histogram
    from util_plot import plot_boxplot, plot_pie, plot_scatter, plot_heatmap
    from util_plot import plot_line, plot_countplot, plot_top_n_bar

    COLORS = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#E58606",
              "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]

    # Connect to our database
    con = duckdb.connect('auto_insurance_db.duckdb')

    # Helper: run SQL and return a DataFrame
    def sql(query):
        return con.execute(query).df()

    # Quick sanity check
    result = sql("SELECT COUNT(*) AS total_rows FROM insurance")
    print(f"Connected! The insurance table has {result['total_rows'][0]:,} rows.")
    return (
        COLORS,
        con,
        plot_bar,
        plot_grouped_bar,
        plot_heatmap,
        plot_line,
        plot_pie,
        plot_scatter,
        plot_top_n_bar,
        plt,
        sns,
        sql,
    )


@app.cell
def _(sql):
    # Preview the table
    sql("SELECT * FROM insurance LIMIT 5")
    return


@app.cell
def _(sql):
    # Column overview
    sql("DESCRIBE insurance")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3.0 Add Derived Columns

    **What are we doing?** Before querying, we add a few useful derived columns that will make later analysis richer. We use DuckDB's `ALTER TABLE` with computed expressions. Since we opened the database read-only above, we reconnect briefly in write mode to add these columns.

    Derived columns:
    - **`claim_to_premium_ratio`**: `total_claim_amount / monthly_premium_auto` — how much claims cost relative to the premium paid. A higher ratio means the customer costs the insurer more.
    - **`income_group`**: Categorizes income into Low / Medium / High / Very High brackets.
    - **`clv_group`**: Categorizes customer lifetime value into quartile-based tiers.
    """)
    return


@app.cell
def _(con, sql):
    # --- claim_to_premium_ratio ---
    try:
        con.execute("ALTER TABLE insurance ADD COLUMN claim_to_premium_ratio DOUBLE")
    except:
        pass  # column already exists

    con.execute("""
        UPDATE insurance 
        SET claim_to_premium_ratio = ROUND(total_claim_amount / NULLIF(monthly_premium_auto, 0), 4)
    """)

    # --- income_group ---
    try:
        con.execute("ALTER TABLE insurance ADD COLUMN income_group VARCHAR")
    except:
        pass

    con.execute("""
        UPDATE insurance 
        SET income_group = CASE
            WHEN income = 0 THEN 'No Income'
            WHEN income < 30000 THEN 'Low'
            WHEN income < 60000 THEN 'Medium'
            WHEN income < 90000 THEN 'High'
            ELSE 'Very High'
        END
    """)

    # --- clv_group (based on quartiles) ---
    try:
        con.execute("ALTER TABLE insurance ADD COLUMN clv_group VARCHAR")
    except:
        pass

    con.execute("""
        UPDATE insurance
        SET clv_group = CASE
            WHEN customer_lifetime_value < 3500 THEN 'Low CLV'
            WHEN customer_lifetime_value < 5500 THEN 'Medium CLV'
            WHEN customer_lifetime_value < 8500 THEN 'High CLV'
            ELSE 'Very High CLV'
        END
    """)


    print("Derived columns added: claim_to_premium_ratio, income_group, clv_group")
    sql("SELECT customer, income, income_group, customer_lifetime_value, clv_group, claim_to_premium_ratio FROM insurance LIMIT 5")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3.1 Simple Queries

    **SQL concepts:** `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, comparison operators, `DISTINCT`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 1: Top 10 Customers by Lifetime Value

    **What are we doing?** We retrieve the 10 most valuable customers — those with the highest `customer_lifetime_value`. This is a straightforward `ORDER BY ... DESC LIMIT` pattern, one of the most common things you'll do in SQL.
    """)
    return


@app.cell
def _(sql):
    q1 = sql("""
        SELECT customer, 
               state, 
               ROUND(customer_lifetime_value, 2) AS clv,
               income,
               coverage
        FROM insurance
        ORDER BY customer_lifetime_value DESC
        LIMIT 10
    """)
    q1
    return (q1,)


@app.cell
def _(plot_top_n_bar, q1):
    plot_top_n_bar(q1, 'clv', 'customer', 'Top 10 Customers by Lifetime Value', n=10, xlabel='Customer Lifetime Value ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 2: All Customers in Oregon with Premium > $100

    **What are we doing?** We filter rows using multiple `WHERE` conditions combined with `AND`. This selects customers who live in Oregon **and** pay more than $100/month in premiums.
    """)
    return


@app.cell
def _(sql):
    q2 = sql("""
        SELECT customer, 
               state, 
               monthly_premium_auto,
               total_claim_amount,
               vehicle_class
        FROM insurance
        WHERE state = 'Oregon'
          AND monthly_premium_auto > 100
        ORDER BY monthly_premium_auto DESC
        LIMIT 15
    """)
    print(f"Found {len(q2)} rows (showing first 15)")
    q2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 3: Distinct Vehicle Classes

    **What are we doing?** `SELECT DISTINCT` returns unique values only. This is useful for understanding the categories in a column before writing more complex queries.
    """)
    return


@app.cell
def _(sql):
    q3 = sql("""
        SELECT DISTINCT vehicle_class
        FROM insurance
        ORDER BY vehicle_class
    """)
    q3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 4: Customers with Zero Income Who Responded to an Offer

    **What are we doing?** We combine equality checks on different columns. Inspired by the Kaggle notebook's observation that employment status and income are strong clustering features — here we look at unemployed (zero-income) customers who still responded "Yes" to a marketing offer.
    """)
    return


@app.cell
def _(sql):
    q4 = sql("""
        SELECT customer, state, employmentstatus, income, 
               coverage, renew_offer_type, sales_channel
        FROM insurance
        WHERE income = 0
          AND response = 'Yes'
        ORDER BY customer_lifetime_value DESC
        LIMIT 10
    """)
    print(f"Zero-income customers who responded 'Yes': showing top 10 by CLV")
    q4
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 5: Customers with High Claim-to-Premium Ratio

    **What are we doing?** We use our derived column `claim_to_premium_ratio` to find customers whose claims are disproportionately high relative to the premium they pay. A ratio above 8 means the claim was more than 8x the monthly premium.
    """)
    return


@app.cell
def _(sql):
    q5 = sql("""
        SELECT customer, 
               monthly_premium_auto, 
               ROUND(total_claim_amount, 2) AS total_claim,
               claim_to_premium_ratio,
               vehicle_class,
               coverage
        FROM insurance
        WHERE claim_to_premium_ratio > 8
        ORDER BY claim_to_premium_ratio DESC
        LIMIT 10
    """)
    q5
    return (q5,)


@app.cell
def _(plot_bar, q5):
    plot_bar(q5, 'customer', 'claim_to_premium_ratio', 
             'Top 10 Customers by Claim-to-Premium Ratio', 
             ylabel='Claim / Premium Ratio')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3.2 Simple+ Queries

    **SQL concepts:** `GROUP BY`, `COUNT`, `AVG`, `SUM`, `MIN`, `MAX`, `ROUND`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 6: Number of Customers per State

    **What are we doing?** `GROUP BY` groups rows with the same value together; `COUNT(*)` counts how many rows are in each group. This tells us the geographic distribution of our customers.
    """)
    return


@app.cell
def _(sql):
    q6 = sql("""
        SELECT state, 
               COUNT(*) AS customer_count
        FROM insurance
        GROUP BY state
        ORDER BY customer_count DESC
    """)
    q6
    return (q6,)


@app.cell
def _(plot_bar, q6):
    plot_bar(q6, 'state', 'customer_count', 
             'Number of Customers per State', ylabel='Customer Count')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 7: Average Monthly Premium by Vehicle Class

    **What are we doing?** We use `AVG()` inside a `GROUP BY` to calculate the average monthly premium for each vehicle class. `ROUND()` formats the result to 2 decimal places.
    """)
    return


@app.cell
def _(sql):
    q7 = sql("""
        SELECT vehicle_class, 
               ROUND(AVG(monthly_premium_auto), 2) AS avg_premium,
               COUNT(*) AS num_customers
        FROM insurance
        GROUP BY vehicle_class
        ORDER BY avg_premium DESC
    """)
    q7
    return (q7,)


@app.cell
def _(plot_bar, q7):
    plot_bar(q7, 'vehicle_class', 'avg_premium',
             'Average Monthly Premium by Vehicle Class', ylabel='Avg Monthly Premium ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 8: Total Claim Amount by Coverage Type

    **What are we doing?** `SUM()` adds up all values in a group. Here we see how total claims break down across Basic, Extended, and Premium coverage plans.
    """)
    return


@app.cell
def _(sql):
    q8 = sql("""
        SELECT coverage, 
               COUNT(*) AS num_customers,
               ROUND(SUM(total_claim_amount), 2) AS total_claims,
               ROUND(AVG(total_claim_amount), 2) AS avg_claim
        FROM insurance
        GROUP BY coverage
        ORDER BY total_claims DESC
    """)
    q8
    return (q8,)


@app.cell
def _(plot_pie, q8):
    plot_pie(q8, 'coverage', 'total_claims', 'Total Claim Amount by Coverage Type')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 9: Average Customer Lifetime Value by Education Level

    **What are we doing?** We group by education level and compute average CLV. This reveals whether education correlates with customer value.
    """)
    return


@app.cell
def _(sql):
    q9 = sql("""
        SELECT education,
               COUNT(*) AS num_customers,
               ROUND(AVG(customer_lifetime_value), 2) AS avg_clv,
               ROUND(AVG(income), 2) AS avg_income
        FROM insurance
        GROUP BY education
        ORDER BY avg_clv DESC
    """)
    q9
    return (q9,)


@app.cell
def _(plot_bar, q9):
    plot_bar(q9, 'education', 'avg_clv',
             'Average Customer Lifetime Value by Education', ylabel='Avg CLV ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 10: Response Rate by Sales Channel

    **What are we doing?** We calculate what fraction of customers responded "Yes" in each sales channel by counting total customers and those who responded positively. This is a business-critical metric — which channel converts best?
    """)
    return


@app.cell
def _(sql):
    q10 = sql("""
        SELECT sales_channel,
               COUNT(*) AS total,
               SUM(CASE WHEN response = 'Yes' THEN 1 ELSE 0 END) AS responded_yes,
               ROUND(100.0 * SUM(CASE WHEN response = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS response_rate_pct
        FROM insurance
        GROUP BY sales_channel
        ORDER BY response_rate_pct DESC
    """)
    q10
    return (q10,)


@app.cell
def _(plot_bar, q10):
    plot_bar(q10, 'sales_channel', 'response_rate_pct',
             'Response Rate by Sales Channel', ylabel='Response Rate (%)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3.3 Intermediate Queries

    **SQL concepts:** `CASE WHEN`, multi-column `GROUP BY`, `HAVING`, subqueries, `IN`, `BETWEEN`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 11: Income Group Distribution

    **What are we doing?** We use `CASE WHEN` to create categories on the fly (inline version of the derived column we already stored). We then count how many customers fall into each income bracket and compute their average CLV. Inspired by the Kaggle notebook's finding that income is the strongest clustering feature.
    """)
    return


@app.cell
def _(sql):
    q11 = sql("""
        SELECT income_group,
               COUNT(*) AS num_customers,
               ROUND(AVG(customer_lifetime_value), 2) AS avg_clv,
               ROUND(AVG(monthly_premium_auto), 2) AS avg_premium,
               ROUND(AVG(total_claim_amount), 2) AS avg_claim
        FROM insurance
        GROUP BY income_group
        ORDER BY avg_clv DESC
    """)
    q11
    return (q11,)


@app.cell
def _(plot_bar, q11):
    plot_bar(q11, 'income_group', 'num_customers',
             'Customer Count by Income Group', ylabel='Number of Customers')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 12: Average CLV by State and Gender (Multi-Column GROUP BY)

    **What are we doing?** We group by **two** columns simultaneously — state and gender. This produces a row for every (state, gender) combination, letting us compare CLV across both dimensions at once.
    """)
    return


@app.cell
def _(sql):
    q12 = sql("""
        SELECT state, 
               gender,
               COUNT(*) AS num_customers,
               ROUND(AVG(customer_lifetime_value), 2) AS avg_clv
        FROM insurance
        GROUP BY state, gender
        ORDER BY state, gender
    """)
    q12
    return (q12,)


@app.cell
def _(plot_grouped_bar, q12):
    plot_grouped_bar(q12, 'state', 'avg_clv', 'gender',
                     'Average CLV by State and Gender', ylabel='Avg CLV ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 13: Vehicle Classes with Average Claim > $400 (HAVING)

    **What are we doing?** `HAVING` filters groups *after* aggregation (unlike `WHERE`, which filters rows *before* aggregation). Here we find vehicle classes where the average claim exceeds $400.
    """)
    return


@app.cell
def _(sql):
    q13 = sql("""
        SELECT vehicle_class,
               COUNT(*) AS num_customers,
               ROUND(AVG(total_claim_amount), 2) AS avg_claim,
               ROUND(MAX(total_claim_amount), 2) AS max_claim
        FROM insurance
        GROUP BY vehicle_class
        HAVING AVG(total_claim_amount) > 400
        ORDER BY avg_claim DESC
    """)
    q13
    return (q13,)


@app.cell
def _(plot_bar, q13):
    plot_bar(q13, 'vehicle_class', 'avg_claim',
             'Vehicle Classes with Avg Claim > $400', ylabel='Avg Claim Amount ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 14: Employment Status vs. Response Rate

    **What are we doing?** The Kaggle notebook identified employment status as a strong clustering feature. Here we examine whether employment status relates to marketing response rates — a practical business question.
    """)
    return


@app.cell
def _(sql):
    q14 = sql("""
        SELECT employmentstatus,
               COUNT(*) AS total_customers,
               SUM(CASE WHEN response = 'Yes' THEN 1 ELSE 0 END) AS responded_yes,
               ROUND(100.0 * SUM(CASE WHEN response = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS response_rate_pct,
               ROUND(AVG(customer_lifetime_value), 2) AS avg_clv,
               ROUND(AVG(income), 2) AS avg_income
        FROM insurance
        GROUP BY employmentstatus
        ORDER BY response_rate_pct DESC
    """)
    q14
    return (q14,)


@app.cell
def _(plot_bar, q14):
    plot_bar(q14, 'employmentstatus', 'response_rate_pct',
             'Response Rate by Employment Status', ylabel='Response Rate (%)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 15: Policy Type and Coverage Crosstab

    **What are we doing?** We build a crosstab (pivot) using `CASE WHEN` inside aggregates. This shows how customers distribute across policy types and coverage levels — a technique for building summary tables in SQL.
    """)
    return


@app.cell
def _(sql):
    q15 = sql("""
        SELECT policy_type,
               SUM(CASE WHEN coverage = 'Basic' THEN 1 ELSE 0 END) AS basic,
               SUM(CASE WHEN coverage = 'Extended' THEN 1 ELSE 0 END) AS extended,
               SUM(CASE WHEN coverage = 'Premium' THEN 1 ELSE 0 END) AS premium,
               COUNT(*) AS total
        FROM insurance
        GROUP BY policy_type
        ORDER BY total DESC
    """)
    q15
    return (q15,)


@app.cell
def _(COLORS, plt, q15):
    # Stacked bar chart for the crosstab
    q15_plot = q15.set_index('policy_type')[['basic', 'extended', 'premium']]
    ax = q15_plot.plot(kind='bar', stacked=True, figsize=(10, 6), color=COLORS[:3])
    ax.set_title('Policy Type by Coverage Level', fontweight='bold', fontsize=14)
    ax.set_xlabel('Policy Type')
    ax.set_ylabel('Customer Count')
    ax.legend(title='Coverage')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3.4 Intermediate+ Queries

    **SQL concepts:** Top-N per group, `ROW_NUMBER()`, `RANK()`, `NTILE()`, CTEs (`WITH`), subqueries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 16: Top 3 Customers per State by CLV (Window Function + CTE)

    **What are we doing?** This is the classic "Top-N per group" pattern. We use a CTE (`WITH ranked AS ...`) and `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` to rank customers within each state, then filter to keep only the top 3.
    """)
    return


@app.cell
def _(sql):
    q16 = sql("""
        WITH ranked AS (
            SELECT customer,
                   state,
                   ROUND(customer_lifetime_value, 2) AS clv,
                   ROW_NUMBER() OVER (PARTITION BY state ORDER BY customer_lifetime_value DESC) AS rank
            FROM insurance
        )
        SELECT customer, state, clv, rank
        FROM ranked
        WHERE rank <= 3
        ORDER BY state, rank
    """)
    q16
    return (q16,)


@app.cell
def _(plot_grouped_bar, q16):
    plot_grouped_bar(q16, 'state', 'clv', 'rank',
                     'Top 3 Customers per State by CLV', ylabel='Customer Lifetime Value ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 17: Percentile Ranking of Customers by Total Claims (NTILE)

    **What are we doing?** `NTILE(4)` divides all customers into 4 equal-sized buckets (quartiles) by total claim amount. We then summarize each quartile. This mirrors the segmentation approach from the Kaggle notebook but done purely in SQL.
    """)
    return


@app.cell
def _(sql):
    q17 = sql("""
        WITH quartiles AS (
            SELECT *,
                   NTILE(4) OVER (ORDER BY total_claim_amount) AS claim_quartile
            FROM insurance
        )
        SELECT claim_quartile,
               COUNT(*) AS num_customers,
               ROUND(MIN(total_claim_amount), 2) AS min_claim,
               ROUND(MAX(total_claim_amount), 2) AS max_claim,
               ROUND(AVG(total_claim_amount), 2) AS avg_claim,
               ROUND(AVG(monthly_premium_auto), 2) AS avg_premium,
               ROUND(AVG(customer_lifetime_value), 2) AS avg_clv
        FROM quartiles
        GROUP BY claim_quartile
        ORDER BY claim_quartile
    """)
    q17
    return (q17,)


@app.cell
def _(plot_bar, q17):
    q17['claim_quartile'] = q17['claim_quartile'].astype(str)
    plot_bar(q17, 'claim_quartile', 'avg_claim',
             'Average Claim by Quartile', xlabel='Claim Quartile', ylabel='Avg Claim ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 18: Running Total of Claims by State (Cumulative Window)

    **What are we doing?** We compute a running (cumulative) sum of total claims across customers within each state, ordered by CLV. This demonstrates `SUM() OVER (PARTITION BY ... ORDER BY ...)` — one of the most powerful window function patterns.
    """)
    return


@app.cell
def _(sql):
    q18 = sql("""
        WITH running AS (
            SELECT customer,
                   state,
                   ROUND(total_claim_amount, 2) AS claim,
                   ROUND(SUM(total_claim_amount) OVER (
                       PARTITION BY state 
                       ORDER BY customer_lifetime_value DESC
                       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                   ), 2) AS running_total
            FROM insurance
        )
        SELECT *
        FROM running
        WHERE state = 'California'
        LIMIT 15
    """)
    q18
    return (q18,)


@app.cell
def _(plot_line, q18):
    plot_line(q18.reset_index(), 'index', 'running_total',
              'Running Total of Claims (California, by CLV rank)',
              xlabel='Customer Rank (by CLV)', ylabel='Cumulative Claims ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 19: States Where Average CLV Exceeds the Overall Average (Subquery with WITH)

    **What are we doing?** We use a CTE to compute the overall average CLV first, then compare each state's average against it. This is a clean alternative to a correlated subquery.
    """)
    return


@app.cell
def _(sql):
    q19 = sql("""
        WITH overall AS (
            SELECT AVG(customer_lifetime_value) AS overall_avg_clv
            FROM insurance
        ),
        state_avg AS (
            SELECT state,
                   ROUND(AVG(customer_lifetime_value), 2) AS avg_clv,
                   COUNT(*) AS num_customers
            FROM insurance
            GROUP BY state
        )
        SELECT s.state,
               s.avg_clv,
               ROUND(o.overall_avg_clv, 2) AS overall_avg,
               ROUND(s.avg_clv - o.overall_avg_clv, 2) AS difference,
               s.num_customers
        FROM state_avg s
        CROSS JOIN overall o
        WHERE s.avg_clv > o.overall_avg_clv
        ORDER BY difference DESC
    """)
    q19
    return (q19,)


@app.cell
def _(COLORS, plot_bar, q19):
    plot_bar(q19, 'state', 'difference',
             'States Above Overall Average CLV (difference)', 
             ylabel='CLV Above Average ($)', color=COLORS[2])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 20: Ranking Policies by Claim Amount within Each Vehicle Class (RANK)

    **What are we doing?** `RANK()` assigns a rank within each partition. Unlike `ROW_NUMBER()`, `RANK()` gives the same rank to ties. We rank policies within each vehicle class by average claim amount.
    """)
    return


@app.cell
def _(sql):
    q20 = sql("""
        WITH policy_stats AS (
            SELECT vehicle_class,
                   policy,
                   COUNT(*) AS num_customers,
                   ROUND(AVG(total_claim_amount), 2) AS avg_claim
            FROM insurance
            GROUP BY vehicle_class, policy
        )
        SELECT vehicle_class,
               policy,
               num_customers,
               avg_claim,
               RANK() OVER (PARTITION BY vehicle_class ORDER BY avg_claim DESC) AS claim_rank
        FROM policy_stats
        ORDER BY vehicle_class, claim_rank
    """)
    q20
    return (q20,)


@app.cell
def _(plot_grouped_bar, q20):
    plot_grouped_bar(q20, 'vehicle_class', 'avg_claim', 'policy',
                     'Average Claim by Policy within Vehicle Class', ylabel='Avg Claim ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3.5 Key SQL Concepts — Analytical Segmentation

    **SQL concepts demonstrated in this notebook:**

    | Concept | Query Examples |
    |---------|---------------|
    | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT` | Q1–Q5 |
    | `DISTINCT` | Q3 |
    | `GROUP BY` + aggregate functions | Q6–Q10 |
    | `CASE WHEN` (conditional logic) | Q10, Q11, Q14, Q15 |
    | Multi-column `GROUP BY` | Q12, Q15 |
    | `HAVING` (filter after aggregation) | Q13 |
    | CTEs (`WITH`) | Q16–Q20 |
    | `ROW_NUMBER()` (window function) | Q16 |
    | `NTILE()` (quartile bucketing) | Q17 |
    | Cumulative `SUM() OVER()` | Q18 |
    | Subqueries + `CROSS JOIN` | Q19 |
    | `RANK()` (ranking with ties) | Q20 |
    | Derived columns | Q5, Q11 (claim_to_premium_ratio, income_group, clv_group) |

    The following queries show more advanced segmentation, tying together these concepts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bonus Query A: Customer Segmentation by CLV and Income (Inspired by Kaggle K-Means)

    **What are we doing?** The Kaggle notebook used K-Means clustering to segment customers by income and CLV. Here we achieve a similar segmentation entirely in SQL using `CASE WHEN` on our derived columns, then analyze each segment's behavior.
    """)
    return


@app.cell
def _(sql):
    qA = sql("""
        SELECT income_group,
               clv_group,
               COUNT(*) AS num_customers,
               ROUND(AVG(monthly_premium_auto), 2) AS avg_premium,
               ROUND(AVG(total_claim_amount), 2) AS avg_claim,
               ROUND(100.0 * SUM(CASE WHEN response = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS response_rate_pct
        FROM insurance
        GROUP BY income_group, clv_group
        ORDER BY income_group, clv_group
    """)
    qA
    return (qA,)


@app.cell
def _(plot_heatmap, qA):
    # Heatmap: response rate across income group and CLV group
    pivot = qA.pivot_table(index='income_group', columns='clv_group', values='response_rate_pct')
    # Reorder for logical display
    income_order = ['No Income', 'Low', 'Medium', 'High', 'Very High']
    clv_order = ['Low CLV', 'Medium CLV', 'High CLV', 'Very High CLV']
    pivot = pivot.reindex(index=[x for x in income_order if x in pivot.index],
                          columns=[x for x in clv_order if x in pivot.columns])
    plot_heatmap(pivot, 'Response Rate (%) by Income Group and CLV Group', fmt='.1f', cmap='YlGnBu')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bonus Query B: Percentile Distribution of Customer Lifetime Value

    **What are we doing?** We compute the 10th, 25th, 50th (median), 75th, and 90th percentiles of CLV using DuckDB's `PERCENTILE_CONT` function — the SQL equivalent of computing quantiles in Python.
    """)
    return


@app.cell
def _(sql):
    qB = sql("""
        SELECT 
            ROUND(PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY customer_lifetime_value), 2) AS p10,
            ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY customer_lifetime_value), 2) AS p25,
            ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY customer_lifetime_value), 2) AS p50_median,
            ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY customer_lifetime_value), 2) AS p75,
            ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY customer_lifetime_value), 2) AS p90,
            ROUND(AVG(customer_lifetime_value), 2) AS mean
        FROM insurance
    """)
    qB
    return (qB,)


@app.cell
def _(COLORS, plt, qB, sns, sql):
    # Histogram of CLV with percentile markers
    clv_data = sql('SELECT customer_lifetime_value FROM insurance')
    fig, ax_1 = plt.subplots(figsize=(10, 6))
    sns.histplot(data=clv_data, x='customer_lifetime_value', bins=50, kde=True, ax=ax_1, color=COLORS[0])
    percentiles = {'P10': qB['p10'][0], 'P25': qB['p25'][0], 'Median': qB['p50_median'][0], 'P75': qB['p75'][0], 'P90': qB['p90'][0]}
    # Mark percentiles
    line_colors = [COLORS[1], COLORS[2], COLORS[3], COLORS[4], COLORS[5]]
    for (label, val), c in zip(percentiles.items(), line_colors):
        ax_1.axvline(val, color=c, linestyle='--', linewidth=2, label=f'{label}: ${val:,.0f}')
    ax_1.set_title('Distribution of Customer Lifetime Value with Percentile Markers', fontweight='bold')
    ax_1.set_xlabel('Customer Lifetime Value ($)')
    ax_1.set_ylabel('Frequency')
    ax_1.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bonus Query C: Premium vs. Claims Scatter by Vehicle Class

    **What are we doing?** We pull premium and claim data for a scatter plot colored by vehicle class. This visualization reveals whether higher premiums actually correlate with higher claims.
    """)
    return


@app.cell
def _(plot_scatter, sql):
    qC = sql("""
        SELECT monthly_premium_auto,
               total_claim_amount,
               vehicle_class,
               customer_lifetime_value
        FROM insurance
    """)
    plot_scatter(qC, 'monthly_premium_auto', 'total_claim_amount',
                 'Monthly Premium vs. Total Claim Amount',
                 hue='vehicle_class',
                 xlabel='Monthly Premium ($)', ylabel='Total Claim Amount ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cleanup
    """)
    return


@app.cell
def _():
    # con.close()
    print("Connection closed. Notebook complete!")
    return


if __name__ == "__main__":
    app.run()
