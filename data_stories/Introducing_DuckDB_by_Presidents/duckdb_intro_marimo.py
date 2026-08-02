import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Introducing DuckDB 🦆

    A hands-on notebook covering the [Real Python DuckDB tutorial](https://realpython.com/python-duckdb/).

    **What we'll cover:**
    1. Installation & quick test
    2. Load CSVs → build the database
    3. Querying with SQL
    4. Querying with the Relational Python API
    5. Advanced queries (window functions, aggregations, CTEs)
    6. Concurrency — reads vs writes
    7. Custom Python UDFs
    8. Integration with pandas / Polars
    9. Visualisations (via `plots.py`)

    > **Data files required** (in the same directory as this notebook):

    1. `data/presidents.csv`

    2. `data/parties.csv`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 0. What is DuckDB

    ```
    1. DuckDB is a free
    2. DuckDB is open-source
    3. DuckDB is an embedded relational database management system
    4. DuckDB is designed specifically for Online Analytical Processing (OLAP) workloads.
    ```

    - **DuckDB is an in-process analytical database** <br> that runs directly inside your Python program, Jupyter notebook, or application—no server installation required.

    - **DuckDB speaks standard SQL**, <br> making it easy to query CSV, Parquet, Excel, and database tables using familiar SQL statements.

    - **DuckDB is extremely fast for analytics**, <br> allowing you to analyze millions of rows on a laptop without needing a large database server.

    - **DuckDB is simple to use and free**, <br> making it ideal for learning SQL, data analysis, data science, and database management.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1 · Installation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 · Quick sanity check
    """)
    return


@app.cell
def _():
    import duckdb
    print("duckdb version=", duckdb.__version__)
    return (duckdb,)


@app.cell
def _(duckdb):
    duckdb.sql("SELECT 'hello duck' AS waterfowl, 'whistle' AS call")
    return


@app.cell
def _(duckdb):
    duckdb.sql("""
        SELECT *
        FROM (
        VALUES
            ('Alex', 10),
            ('Jane', 20),
            ('Barb', 30) ) t(name,
            value);
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 · Open connection & load CSV data

    We open one persistent connection `con` for the whole notebook and load both CSV files into tables.
    """)
    return


@app.cell
def _():
    # 3.1 

    import os

    # Delete database if it already exists
    DB_PATH = "presidents.duckdb"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    return (DB_PATH,)


@app.cell
def _(DB_PATH, duckdb):
    # 3.2 Create a DuckDB Connection object

    con = duckdb.connect(DB_PATH)
    print("con=", con)
    return (con,)


@app.cell
def _():
    # 3.3 Examine INPUT: presidents.csv
    return


@app.cell
def _(con):
    # 3.4 Create presidents table: 

    con.execute("""
        CREATE TABLE presidents AS
        SELECT
            sequence,
            last_name,
            first_name,
            CAST(term_start AS DATE) AS term_start,
            CAST(term_end AS DATE) AS term_end,
            party_id
        FROM read_csv_auto('data/presidents.csv');
    """)

    con.execute("""
        SELECT COUNT(*) AS presidents_loaded
        FROM presidents;
    """).df()
    return


@app.cell
def _(con):
    # 3.4 View all of the presidents
    con.execute("""
        SELECT *
        FROM presidents;
    """).df()
    return


@app.cell
def _(con):
    # 3.5 Create parties table: 
    con.execute("""
        CREATE TABLE parties AS
        SELECT *
        FROM read_csv_auto('data/parties.csv');
    """)

    con.execute("""
        SELECT *
        FROM parties;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 · SQL Queries

    ### 4.1  Basic SELECT with WHERE
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            sequence,
            first_name,
            last_name
        FROM presidents
        WHERE sequence <= 5
        ORDER BY sequence;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2  JOIN — presidents and their party names
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            p.first_name,
            p.last_name,
            pt.party_name
        FROM presidents p
        JOIN parties pt ON p.party_id = pt.party_id
        WHERE pt.party_name = 'Whig'
        ORDER BY p.last_name DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.3  Aggregate — count of presidents per party
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            pt.party_name,
            COUNT(*) AS president_count
        FROM presidents p
        JOIN parties pt ON p.party_id = pt.party_id
        GROUP BY pt.party_name
        ORDER BY president_count DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.4  Date arithmetic — days in office
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            first_name || ' ' || last_name AS president,
            (term_end - term_start) AS days_in_office
        FROM presidents
        ORDER BY days_in_office DESC
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.5  Window function — running total of days in office
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            sequence,
            last_name,
            (term_end - term_start) AS days_in_office,
            SUM(term_end - term_start) OVER (
        ORDER BY sequence) AS cumulative_days
        FROM presidents
        ORDER BY sequence
        LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.6  CTE — longest-serving president per party
    """)
    return


@app.cell
def _(con):
    con.execute("""
        WITH terms AS (
        SELECT
            p.sequence,
            p.first_name || ' ' || p.last_name AS president,
            pt.party_name,
            (p.term_end - p.term_start) AS days_in_office
        FROM presidents p
        JOIN parties pt ON p.party_id = pt.party_id ), ranked AS (
        SELECT
            *,
            RANK() OVER (PARTITION BY party_name
        ORDER BY days_in_office DESC) AS rnk
        FROM terms )
        SELECT
            party_name,
            president,
            days_in_office
        FROM ranked
        WHERE rnk = 1
        ORDER BY days_in_office DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## EXPLAIN: Longest Serving President

    ### ** EXPLAIN** : [Longest Serving President by Party](longest_serving_president_by_party.md)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.7  Century breakdown
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            CASE WHEN YEAR(term_start) < 1800 THEN '18th century' WHEN YEAR(term_start) < 1900 THEN '19th century' WHEN YEAR(term_start) < 2000 THEN '20th century' ELSE '21st century' END AS century,
            COUNT(*) AS presidents,
            AVG(term_end - term_start)::INTEGER AS avg_days_in_office,
            MIN(term_end - term_start) AS shortest_term,
            MAX(term_end - term_start) AS longest_term
        FROM presidents
        GROUP BY 1
        ORDER BY 1;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Century breakdown EXPLANATION

    ### ** EXPLAIN** : [presidential_terms_by_century.md](presidential_terms_by_century.md)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5 · Relational Python API

    DuckDB's `DuckDBPyRelation` supports method-chaining as an alternative to raw SQL.
    """)
    return


@app.cell
def _(con, mo):
    _presidents_rel = con.table("presidents").set_alias("presidents")
    _parties_rel    = con.table("parties").set_alias("parties")

    _df = (
        _presidents_rel
        .join(_parties_rel, "presidents.party_id = parties.party_id")
        .select("first_name", "last_name", "party_name")
        .filter("party_name = 'Whig'")
        .order("last_name DESC")
    ).df()
    mo.ui.table(_df)
    return


@app.cell
def _(con):
    # Top 5 longest-serving
    con.execute("""
        SELECT
            first_name || ' ' || last_name AS president,
            (term_end - term_start) AS days_in_office
        FROM presidents
        ORDER BY days_in_office DESC
        LIMIT 5;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6 · Concurrency

    ### 6.1  Concurrent reads — always succeed
    """)
    return


@app.cell
def _(DB_PATH, duckdb):
    from concurrent.futures import ThreadPoolExecutor

    def read_data(thread_id):
        print(f"Thread {thread_id} starting its read.")
        # Each thread needs its own connection
        _thread_con = duckdb.connect(DB_PATH)
        _thread_con.execute("""
            SELECT
                first_name,
                last_name
            FROM presidents
            WHERE sequence = 1;
        """).df().to_string(index=False)
        _thread_con.close()
        print(f"Thread {thread_id} done. ✅")

    with ThreadPoolExecutor(max_workers=3) as _ex:
        _ex.map(read_data, range(3))
    return (ThreadPoolExecutor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.2  Concurrent writes — only one wins

    DuckDB lets the first writer commit and rolls back the others.
    """)
    return


@app.cell
def _(DB_PATH, ThreadPoolExecutor, con, duckdb):
    def update_data(thread_id):
        new_name = f"George ({thread_id})"
        try:
            _thread_con = duckdb.connect(DB_PATH)
            print(f"Thread {thread_id} starting its update.")
            _thread_con.execute(f"""
                UPDATE presidents
                SET first_name = '{new_name}'
                WHERE sequence = 1
            """)
            _thread_con.close()
            print(f"Thread {thread_id} ending its update. ✅")
        except Exception as e:
            print(f"Thread {thread_id} failed ❌: {type(e).__name__}: {e}")

    with ThreadPoolExecutor(max_workers=3) as _ex:
        _ex.map(update_data, range(3))

    # Restore and verify
    con.execute("""
        UPDATE presidents
        SET first_name = 'George'
        WHERE sequence = 1;
    """)
    con.execute("""
        SELECT
            first_name,
            last_name
        FROM presidents
        WHERE sequence = 1;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7 · Custom Python UDFs

    Register Python functions so they can be called inside SQL.
    """)
    return


@app.cell
def _(con):
    def short_name(first_name: str, last_name: str) -> str:
        """Return 'F. LastName' format."""
        return f"{first_name[0]}. {last_name}"

    con.create_function("short_name", short_name)

    con.execute("""
        SELECT
            short_name(first_name, last_name) AS name,
            (term_end - term_start) AS days_in_office
        FROM presidents
        ORDER BY days_in_office DESC
        LIMIT 8;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8 · pandas & Polars integration
    """)
    return


@app.cell
def _(con):
    # ── pandas ────────────────────────────────────────────────────────────────────
    df_pd = con.execute("""
        SELECT
            p.sequence,
            p.last_name,
            p.first_name,
            pt.party_name,
            YEAR(p.term_start) AS term_start_year,
            (p.term_end - p.term_start) AS days_in_office
        FROM presidents p
        JOIN parties pt ON p.party_id = pt.party_id;
    """).df()

    print(type(df_pd))
    df_pd.head()
    return


@app.cell
def _(con):
    # ── Polars ────────────────────────────────────────────────────────────────────
    df_pl = con.execute("""
        SELECT
            p.sequence,
            p.last_name,
            p.first_name,
            pt.party_name,
            YEAR(p.term_start) AS term_start_year,
            (p.term_end - p.term_start) AS days_in_office
        FROM presidents p
        JOIN parties pt ON p.party_id = pt.party_id;
    """).pl()

    print(type(df_pl))
    df_pl.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9 · Visualisations

    All plotting logic lives in **`plots.py`** — this notebook only handles queries.
    """)
    return


@app.cell
def _(con):
    import matplotlib.pyplot as plt
    import plots

    # Full joined dataset used by all plots
    df_full = con.execute("""
        SELECT
            p.sequence,
            p.last_name,
            p.first_name,
            pt.party_name,
            YEAR(p.term_start) AS term_start_year,
            (p.term_end - p.term_start) AS days_in_office
        FROM presidents p
        JOIN parties pt ON p.party_id = pt.party_id;
    """).df()

    print(f"Loaded {len(df_full)} rows")
    df_full.head()
    return df_full, plots, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9.1  Presidents per party
    """)
    return


@app.cell
def _(con, plots, plt):
    party_counts = con.execute("""
        SELECT
            pt.party_name,
            COUNT(*) AS president_count
        FROM presidents p
        JOIN parties pt ON p.party_id = pt.party_id
        GROUP BY pt.party_name;
    """).df()

    _fig = plots.plot_presidents_per_party(party_counts)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9.2  Distribution of term lengths
    """)
    return


@app.cell
def _(df_full, plots, plt):
    _fig = plots.plot_days_in_office_distribution(df_full)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9.3  Presidential timeline
    """)
    return


@app.cell
def _(df_full, plots, plt):
    _fig = plots.plot_term_timeline(df_full)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9.4  Average term length by party
    """)
    return


@app.cell
def _(con, plots, plt):
    avg_term = con.execute("""
        SELECT
            pt.party_name,
            AVG(p.term_end - p.term_start) AS avg_days,
            COUNT(*) AS president_count
        FROM presidents p
        JOIN parties pt ON p.party_id = pt.party_id
        GROUP BY pt.party_name;
    """).df()

    _fig = plots.plot_avg_term_by_party(avg_term)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9.5  Sequence vs days in office
    """)
    return


@app.cell
def _(df_full, plots, plt):
    _fig = plots.plot_sequence_vs_days(df_full)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10 · Query DataFrames directly with DuckDB

    DuckDB can query in-memory DataFrames by referencing their Python variable names in SQL.
    """)
    return


@app.cell
def _(df_full, duckdb):
    # Query the pandas DataFrame we already have — no round-trip to the DB file
    duckdb.execute("""
        SELECT
            party_name,
            ROUND(AVG(days_in_office), 0) AS avg_days,
            MAX(days_in_office) AS max_days
        FROM df_full
        GROUP BY party_name
        ORDER BY avg_days DESC;
    """).df()
    return


@app.cell
def _(con):
    # NumPy interop via fetchnumpy()
    arr = con.execute("""
        SELECT
            sequence,
            days_in_office
        FROM df_full
        ORDER BY sequence;
    """).fetchnumpy()

    print("Keys  :", list(arr.keys()))
    print("First 5:", arr["sequence"][:5])
    return


@app.cell
def _(con):
    # Close the connection when done
    con.close()
    print("Connection closed.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Summary

    | Feature | What we used |
    |---|---|
    | Persistent connection | `con = duckdb.connect('presidents.duckdb')` |
    | Load CSV | `read_csv_auto()` inside `CREATE TABLE AS` |
    | Execute & fetch | `con.execute(sql).df()` |
    | SQL queries | `SELECT`, `JOIN`, `WHERE`, `GROUP BY`, CTE, window functions |
    | Relational API | `.join()`, `.select()`, `.filter()`, `.order()` → `.df()` |
    | Custom UDFs | `con.create_function()` |
    | Concurrency | `ThreadPoolExecutor` — reads OK, writes conflict |
    | pandas export | `.df()` |
    | Polars export | `.pl()` |
    | NumPy export | `.fetchnumpy()` |
    | Plotting | `plots.py` via `matplotlib` |
    """)
    return


if __name__ == "__main__":
    app.run()
