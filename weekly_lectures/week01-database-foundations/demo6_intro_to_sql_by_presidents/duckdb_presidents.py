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
    # Introducing DuckDB 🦆 — A Tour Through U.S. Presidents

    ### This notebook is a hands-on introduction to DuckDB.

    ### Dataset

    | file            | Description             |
    |-----------------|-------------------------|
    |`presidents.csv` |the 47 U.S. presidencies |
    |`parties.csv`    | political parties       |

    ### How this notebook is organised

    | Section | What it covers |
    |---|---|
    | **1 – Setup** | Install & import DuckDB, apply a plotting theme |
    | **2 – Build the database** | Load the two CSVs, add derived columns, save `presidents_db.duckdb` |
    | **3 – Inspect the tables** | Sanity-check what we loaded |
    | **4.1 – Simple queries** | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `COUNT` |
    | **4.2 – Simple+ queries** | `BETWEEN`, `LIKE`, `IN`, `CASE`, computed columns |
    | **4.3 – Intermediate** | `JOIN`, `GROUP BY`, `HAVING`, aggregations |
    | **4.4 – Intermediate+** | Top-N, `RANK()`/`LAG()` window functions, `WITH` (CTEs) |
    | **4.5 – Key DuckDB/SQL concepts** | Querying DataFrames directly, the relational API |

    ### The convention we follow for every query

    Each query below is presented in four consistent steps:

    1. **What are we doing?** — a plain-English explanation of the question.
    2. **The SQL** — a cleanly formatted query run with `con.execute()`.
    3. **The result** — displayed as a tidy pandas DataFrame.
    4. **A plot** — whenever a chart tells the story better than a table.

    > **Plotting is fully decoupled.** <br>
    > * Every chart is drawn by a function in `util_plot.py`.  <br>
    > * The notebook only ever *queries* and then hands the resulting <br>
    > DataFrame to a plot helper — so the SQL stays front-and-centre.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1 · Setup

    ### What are we doing?
    First we make sure the libraries we need are available and import them.

    * **`duckdb`** — the database engine. It runs entirely inside this Python
      process; there is no server to start and no configuration to manage.
    * **`pandas`** — DuckDB hands query results back to us as pandas DataFrames via
      the `.df()` method, which Jupyter renders as a clean table.
    * **`util_plot`** — our own module (sitting next to this notebook) that holds
      *all* the plotting code.

    The `%matplotlib inline` magic tells Jupyter to render charts directly under the
    cell that produces them.
    """)
    return


@app.cell
def _():
    # Install dependencies (safe to re-run; skip if already installed)
    # packages added via marimo's package management: duckdb pandas matplotlib seaborn !pip install duckdb pandas matplotlib seaborn --quiet
    return


@app.cell
def _():
    import pandas as pd

    import util_plot as up          # <-- all plotting lives here

    # '%matplotlib inline' command supported automatically in marimo
    import matplotlib.pyplot as plt

    up.set_theme()                  # <-- apply our shared chart styling once

    # Make wide result tables readable
    pd.set_option("display.max_rows", 60)
    pd.set_option("display.width", 120)

    print("pandas version :", pd.__version__)
    return plt, up


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2 · Build the DuckDB database

    ### What are we doing?

    ```
    1. We create a DuckDB database  called `presidents_db.duckdb`
       and load our two CSV files into it as tables.

    2. DuckDB can read a CSV directly with `read_csv_auto()`,
       which sniffs column types automatically.

       We wrap that in `CREATE OR REPLACE TABLE ... AS SELECT ...` so the
       data is stored inside the database file (not re-read from
       disk every query).

    3. We delete any existing copy first so the notebook is
       **idempotent** — running it from top to bottom always
       produces the same fresh database.
    ```
    """)
    return


@app.cell
def _():
    import duckdb
    DATA_DIR = './data'
    print("DuckDB version:", duckdb.__version__)
    return (DATA_DIR, duckdb)


@app.cell
def _(duckdb):
    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.1 · Load `parties` and add nothing — it is already tidy
    The parties table is just a lookup of `party_id → party_name`, so we load it as-is.
    """)
    return


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE parties AS
                SELECT *
                FROM read_csv_auto('{DATA_DIR}/parties.csv')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM parties ORDER BY party_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2 · Load `presidents` in **two steps**

    > **Task step 3 — "add new derived columns if necessary."**

    We do this in two clear steps so the pattern is easy to follow:

    **Step 1 — create the table *as-is* from the CSV.** `read_csv_auto()` sniffs the
    column types for us; because the dates are in ISO `YYYY-MM-DD` form, DuckDB loads
    `term_start` and `term_end` as real `DATE` columns automatically.

    **Step 2 — add the derived columns.** We `ALTER TABLE ... ADD COLUMN` for each new
    field, then a single `UPDATE` fills them in. Computing them from the already-typed
    `DATE` columns keeps the SQL clean (no repeated casts):

    | Derived column | How it is computed | Why it is useful |
    |---|---|---|
    | `full_name` | `first_name \|\| ' ' \|\| last_name` | a ready-to-display label |
    | `term_days` | `term_end - term_start` | DuckDB subtracts two `DATE`s into an **integer number of days** — our core "length of service" measure |
    | `term_years` | `term_days / 365.25` | the same length, in human-friendly years |
    | `term_start_year` / `term_end_year` | `YEAR(...)` | makes century/era filtering trivial |
    | `century` | a `CASE` expression | groups presidencies into 18th–21st century |
    """)
    return


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE presidents AS
                SELECT *
                FROM read_csv_auto('{DATA_DIR}/presidents.csv')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM presidents ORDER BY sequence LIMIT 5
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Step 2 — add and populate the derived columns:**
    """)
    return


@app.cell
def _(con):
    # Step 2a — add the derived columns
    con.execute(
        f"""
        ALTER TABLE presidents ADD COLUMN full_name        VARCHAR;
        ALTER TABLE presidents ADD COLUMN term_days        INTEGER;
        ALTER TABLE presidents ADD COLUMN term_years       DOUBLE;
        ALTER TABLE presidents ADD COLUMN term_start_year  INTEGER;
        ALTER TABLE presidents ADD COLUMN term_end_year    INTEGER;
        ALTER TABLE presidents ADD COLUMN century          VARCHAR
        """
    )
    return

@app.cell
def _(con):
    # Step 2b — populate the derived columns
    con.execute(
        f"""
        UPDATE presidents SET
            full_name       = first_name || ' ' || last_name,
            term_days       = (term_end - term_start),
            term_years      = ROUND((term_end - term_start) / 365.25, 2),
            term_start_year = YEAR(term_start),
            term_end_year   = YEAR(term_end),
            century         = CASE
                                  WHEN YEAR(term_start) < 1800 THEN '18th century'
                                  WHEN YEAR(term_start) < 1900 THEN '19th century'
                                  WHEN YEAR(term_start) < 2000 THEN '20th century'
                                  ELSE '21st century'
                              END
        """
    )
    return

@app.cell
def _(con):
    # Verify: count loaded rows
    con.execute(
        f"""
        SELECT COUNT(*) AS rows_loaded FROM presidents
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3 · Inspect the tables

    ### What are we doing?
    A quick look at the full `presidents` table — including our new derived columns —
    to confirm everything loaded and computed correctly.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
                FROM presidents
                ORDER BY sequence
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 4 · SQL Queries

    ## 4.1 · Five **simple** queries
    The fundamentals: choosing columns, filtering rows, ordering, limiting, counting.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.1.1 — Select specific columns, ordered
    **What are we doing?** The most basic query: pick a few columns and sort the
    rows. We list every president by their order of service (`sequence`).
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT sequence,
                       first_name,
                       last_name
                FROM presidents
                ORDER BY sequence
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.1.2 — Count the rows
    **What are we doing?**

    ```
    `COUNT(*)` is the simplest aggregate —
    it tells us how many presidencies are in
    the data (47, including Grover Cleveland's
    two non-consecutive terms and Donald Trump's
    two non-consecutive terms).
    ```
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT COUNT(*) AS total_presidencies
                FROM presidents
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.1.3 — Filter with `WHERE`
    **What are we doing?**

    ```
    Show only the earliest presidents —
    those who took office before the year 1800 —
    using a `WHERE` filter on a derived column.
    ```
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT sequence,
                       full_name,
                       term_start
                FROM presidents
                WHERE term_start_year < 1800
                ORDER BY sequence
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.1.4 — Order by length of service, `LIMIT` the result
    **What are we doing?**

    ```
    Sort presidents by how long they served
    (our derived `term_days`) and keep just
    the top 10. This previews the Top-N idea
    we develop fully in §4.4.
    ```
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT full_name,
                       term_days,
                       term_years
                FROM presidents
                ORDER BY term_days DESC
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.1.5 — The party lookup table
    **What are we doing?** A plain `SELECT *` on the small `parties` reference table,
    which we will join against repeatedly from §4.3 onward.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT party_id,
                       party_name
                FROM parties
                ORDER BY party_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4.2 · Five **simple+** queries
    A step up: range filters, pattern matching, set membership, conditional labels,
    and computed output columns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2.1 — `BETWEEN` for a range
    **What are we doing?** Select every president who first took office during the
    **19th century** (1800–1899 inclusive) using a `BETWEEN` range filter.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT sequence,
                       full_name,
                       term_start_year
                FROM presidents
                WHERE term_start_year BETWEEN 1800 AND 1899
                ORDER BY sequence
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2.2 — `LIKE` for pattern matching
    **What are we doing?** Find presidents whose **last name starts with "J"** using
    the `LIKE` operator with a `%` wildcard.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT full_name,
                       last_name
                FROM presidents
                WHERE last_name LIKE 'J%'
                ORDER BY last_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2.3 — `IN` for set membership
    **What are we doing?**

    ```
    Select presidents belonging to either
    the Democratic (`party_id = 40`) or
    Republican (`party_id = 60`) parties using `IN (...)`,
    which is shorthand for several `OR` conditions.
    ```
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT full_name,
                       party_id
                FROM presidents
                WHERE party_id IN (40, 60)
                ORDER BY sequence
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2.4 — `CASE` for conditional labels
    **What are we doing?** Although we already stored `century` as a derived column,
    here we show the `CASE` expression *in the query itself* to classify each
    president's term length into a readable bucket — a very common SQL pattern.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT full_name,
                       term_years,
                       CASE
                           WHEN term_days < 365         THEN 'Less than a year'
                           WHEN term_days < 365 * 4     THEN 'Partial / single short term'
                           WHEN term_days <= 365 * 4 + 5 THEN 'About one full term'
                           ELSE 'More than one term'
                       END AS service_bucket
                FROM presidents
                ORDER BY term_days
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2.5 — A computed output column
    **What are we doing?**

    ```
    Build a brand-new column *in the SELECT list* —
    the percentage of a full 4-year (1461-day) term
    that each president actually served — and sort
    by it.

    This shows that SELECT can contain arithmetic,
    not just columns.
    ```
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT full_name,
                       term_days,
                       ROUND(100.0 * term_days / 1461, 1) AS pct_of_full_term
                FROM presidents
                ORDER BY pct_of_full_term DESC
                LIMIT 12
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4.3 · Five **intermediate** queries — joins & aggregations
    Now we combine the two tables with `JOIN` and summarise with `GROUP BY`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.3.1 — `JOIN` presidents to their party names
    **What are we doing?** The `presidents` table stores only a `party_id`. To show
    the human-readable party *name* we join to the `parties` lookup table on the
    shared `party_id` key.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT p.sequence,
                       p.full_name,
                       pt.party_name
                FROM presidents p
                JOIN parties pt
                  ON p.party_id = pt.party_id
                ORDER BY p.sequence
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.3.2 — `GROUP BY`: how many presidents per party?
    **What are we doing?** Count the number of presidents each party has produced by
    joining, then `GROUP BY` the party name. This is the classic
    *join-then-aggregate* pattern.
    """)
    return


@app.cell
def _(con):
    party_counts = con.execute(
        f"""
        SELECT pt.party_name,
               COUNT(*) AS president_count
        FROM presidents p
        JOIN parties pt
          ON p.party_id = pt.party_id
        GROUP BY pt.party_name
        ORDER BY president_count DESC
        """
    ).fetchdf()
    return (party_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The result, as a chart:**
    """)
    return


@app.cell
def _(party_counts, plt, up):
    fig = up.plot_presidents_per_party(party_counts)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.3.3 — Aggregate with `AVG`: average term length by party
    **What are we doing?** For each party, compute the average term length (in days)
    and how many presidents that average is based on. We pass the result straight to
    a plot helper that converts days to years.
    """)
    return


@app.cell
def _(con):
    avg_term = con.execute(
        f"""
        SELECT pt.party_name,
               AVG(p.term_days)  AS avg_days,
               COUNT(*)          AS president_count
        FROM presidents p
        JOIN parties pt
          ON p.party_id = pt.party_id
        GROUP BY pt.party_name
        ORDER BY avg_days DESC
        """
    ).fetchdf()
    return (avg_term,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The result, as a chart:**
    """)
    return


@app.cell
def _(avg_term, plt, up):
    fig_1 = up.plot_avg_term_by_party(avg_term)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.3.4 — `HAVING`: filter *after* aggregating
    **What are we doing?**

    ### `WHERE` filters individual rows.
    ### `HAVING` filters **groups** after aggregation.

    Here we keep only the parties that have produced
    more than three presidents.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT pt.party_name,
                       COUNT(*) AS president_count
                FROM presidents p
                JOIN parties pt
                  ON p.party_id = pt.party_id
                GROUP BY pt.party_name
                HAVING president_count > 3
                ORDER BY president_count DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.3.5 — Multiple aggregates grouped by century
    **What are we doing?** Group presidencies by century and compute several
    summary statistics at once — a count plus the average, shortest, and longest
    term lengths. This is the kind of one-row-per-group summary that analytics
    databases like DuckDB excel at.
    """)
    return


@app.cell
def _(con):
    by_century = con.execute(
        f"""
        SELECT century,
               COUNT(*)                         AS presidents,
               CAST(AVG(term_days) AS INTEGER)  AS avg_days_in_office,
               MIN(term_days)                   AS shortest_term_days,
               MAX(term_days)                   AS longest_term_days
        FROM presidents
        GROUP BY century
        ORDER BY century
        """
    ).fetchdf()
    return (by_century,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The result, as a chart:**
    """)
    return


@app.cell
def _(by_century, plt, up):
    fig_2 = up.plot_presidents_per_century(by_century)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4.4 · Five **intermediate+** queries — Top-N, window functions & CTEs
    The most powerful patterns: ranking within groups, running totals, comparing a
    row to its neighbours, and structuring queries with `WITH` (Common Table
    Expressions).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.4.1 — Top-N: the longest-serving presidents
    **What are we doing?** A **Top-N** query: sort by term length descending and keep
    the top 8. We also join in the party so the chart can colour each bar.
    """)
    return


@app.cell
def _(con):
    top_longest = con.execute(
        f"""
        SELECT p.full_name      AS president,
               p.term_days      AS days_in_office,
               pt.party_name
        FROM presidents p
        JOIN parties pt
          ON p.party_id = pt.party_id
        ORDER BY days_in_office DESC
        LIMIT 8
        """
    ).fetchdf()
    return (top_longest,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The result, as a chart:**
    """)
    return


@app.cell
def _(plt, top_longest, up):
    fig_3 = up.plot_top_n_longest(top_longest)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.4.2 — `RANK()` window function inside a CTE
    **What are we doing?** Find the **longest-serving president *within each party***.
    We use a `WITH` clause (a CTE) to first build a tidy `terms` table, then a
    `RANK() OVER (PARTITION BY party ORDER BY days DESC)` window function to rank
    presidents inside their own party, and finally keep only the rank-1 row per
    party.

    A **window function** computes a value across a set of rows *related to the
    current row* without collapsing them the way `GROUP BY` does.
    """)
    return


@app.cell
def _(ranked, terms, con):
    con.execute(
        f"""
        WITH terms AS (
                    SELECT p.full_name      AS president,
                           pt.party_name,
                           p.term_days       AS days_in_office
                    FROM presidents p
                    JOIN parties pt
                      ON p.party_id = pt.party_id
                ),
                ranked AS (
                    SELECT *,
                           RANK() OVER (
                               PARTITION BY party_name
                               ORDER BY days_in_office DESC
                           ) AS rnk
                    FROM terms
                )
                SELECT party_name,
                       president,
                       days_in_office
                FROM ranked
                WHERE rnk = 1
                ORDER BY days_in_office DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.4.3 — Running total with `SUM() OVER (...)`
    **What are we doing?** Compute a **cumulative running total** of days served as we
    walk through the presidents in order. The window
    `SUM(term_days) OVER (ORDER BY sequence)` adds up every term from the first
    president through the current one.
    """)
    return


@app.cell
def _(con):
    cumulative = con.execute(
        f"""
        SELECT sequence,
               last_name,
               term_days                                   AS days_in_office,
               SUM(term_days) OVER (ORDER BY sequence)      AS cumulative_days
        FROM presidents
        ORDER BY sequence
        """
    ).fetchdf()
    return (cumulative,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The result, as a chart:**
    """)
    return


@app.cell
def _(cumulative, plt, up):
    fig_4 = up.plot_cumulative_days(cumulative)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.4.4 — Compare each row to its group average (`AVG() OVER PARTITION`)
    **What are we doing?** A window function does **not** have to collapse rows. Here
    `AVG(term_days) OVER (PARTITION BY party_name)` attaches each party's average to
    *every* president of that party, so we can compute how far above or below their
    party's norm each president served. We show the biggest over-performers via a
    subquery (`WITH`).
    """)
    return


@app.cell
def _(joined, con):
    con.execute(
        f"""
        WITH joined AS (
                    SELECT p.full_name,
                           pt.party_name,
                           p.term_days
                    FROM presidents p
                    JOIN parties pt
                      ON p.party_id = pt.party_id
                )
                SELECT full_name,
                       party_name,
                       term_days,
                       CAST(AVG(term_days) OVER (PARTITION BY party_name) AS INTEGER)
                                                            AS party_avg_days,
                       term_days
                         - CAST(AVG(term_days) OVER (PARTITION BY party_name) AS INTEGER)
                                                            AS days_vs_party_avg
                FROM joined
                ORDER BY days_vs_party_avg DESC
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.4.5 — `LAG()`: compare a president to the one before
    **What are we doing?** The `LAG()` window function looks at the **previous row**.
    We use it to compare each president's term length with that of their immediate
    predecessor, computing the change between them. (`NULL`/`NaN` for Washington,
    who had no predecessor.)
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT sequence,
                       full_name,
                       term_days,
                       LAG(term_days) OVER (ORDER BY sequence)               AS prev_term_days,
                       term_days - LAG(term_days) OVER (ORDER BY sequence)   AS change_vs_prev
                FROM presidents
                ORDER BY sequence
                LIMIT 12
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4.5 · Key DuckDB / notebook concepts
    DuckDB shines *inside* a notebook because it blurs the line between SQL and
    Python. These three idioms are worth knowing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.5.1 — Query a pandas DataFrame *directly* with SQL
    **What are we doing?** DuckDB can run SQL against an **in-memory pandas
    DataFrame** by referencing its Python variable name — no need to load it into the
    database first. Below we pull a joined data set into `df_full`, then query that
    DataFrame as if it were a table.
    """)
    return


@app.cell
def _(con):
    # Build a joined DataFrame for plotting and the DataFrame-query demo
    df_full = con.execute(
        f"""
        SELECT p.sequence,
               p.last_name,
               p.full_name,
               p.term_start,
               p.term_end,
               p.term_days,
               p.term_start_year,
               p.century,
               pt.party_name
        FROM presidents p
        JOIN parties pt
          ON p.party_id = pt.party_id
        """
    ).fetchdf()
    return (df_full,)

@app.cell
def _(duckdb, df_full):
    # DuckDB can query a pandas DataFrame directly — note 'FROM df_full'
    duckdb.sql("""
        SELECT party_name,
               ROUND(AVG(term_days), 0) AS avg_days,
               MAX(term_days)           AS max_days
        FROM df_full
        GROUP BY party_name
        ORDER BY avg_days DESC
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.5.2 — The relational (method-chaining) API
    **What are we doing?** Besides raw SQL strings, DuckDB offers a fluent
    **relational API** — `.filter()`, `.select()`, `.order()`, `.limit()` — that some
    people find more natural to compose programmatically. Here is the Top-5
    longest-serving query written without any SQL string.
    """)
    return


@app.cell
def _(con):
    # The relational (method-chaining) API — an alternative to SQL strings
    (
        con.sql("SELECT * FROM presidents")
           .order("term_days DESC")
           .limit(5)
           .select("full_name, term_days, term_years")
    ).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.5.3 — Two big-picture visualisations
    **What are we doing?** Finally, two charts that summarise the whole data set:
    the **distribution** of term lengths, and a full **timeline** of every
    presidency coloured by party. Both are drawn by `util_plot.py` from the
    `df_full` DataFrame we built above.
    """)
    return


@app.cell
def _(df_full, plt, up):
    fig_5 = up.plot_term_length_distribution(df_full)
    plt.show()
    return


@app.cell
def _(df_full, plt, up):
    fig_6 = up.plot_term_timeline(df_full)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And the term-length-across-history scatter, to spot long-run trends:
    """)
    return


@app.cell
def _(df_full, plt, up):
    fig_7 = up.plot_term_vs_sequence(df_full)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 · Close the connection

    ### What are we doing?
    DuckDB flushes everything to `presidents_db.duckdb` as we go, but it is good
    practice to close the connection explicitly when we are done. The database file
    remains on disk and can be reopened any time with
    `duckdb.connect('presidents_db.duckdb')`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    *Great work! You've completed the notebook.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary — what we covered

    | Concept | Where | Example |
    |---|---|---|
    | Persistent DB + load CSV | §2 | `read_csv_auto()` inside `CREATE OR REPLACE TABLE AS` |
    | Derived columns | §2.2 | `term_days`, `term_years`, `century`, `full_name` |
    | `SELECT` / `WHERE` / `ORDER BY` / `LIMIT` / `COUNT` | §4.1 | the fundamentals |
    | `BETWEEN` / `LIKE` / `IN` / `CASE` / computed cols | §4.2 | richer filtering |
    | `JOIN` / `GROUP BY` / `HAVING` / aggregates | §4.3 | combine + summarise |
    | Top-N, `RANK()`, `SUM() OVER`, `AVG() OVER`, `LAG()`, CTEs | §4.4 | window functions & `WITH` |
    | Query a DataFrame, relational API | §4.5 | DuckDB ↔ Python |
    | Decoupled plotting | everywhere | every chart drawn by `util_plot.py` |

    🦆 **You now have a reusable `presidents_db.duckdb` and a full tour of analytical SQL.**
    """)
    return


if __name__ == "__main__":
    app.run()
