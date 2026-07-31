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
    # Notebook 2 — Teaching SQL with `sales_db.duckdb`

    **Course:** OMIS 105 · Data Stories · Video Game Sales

    This notebook uses the clean database built in Notebook 1 to teach SQL through a
    graded series of **20 queries**, from simple `SELECT`s up to window functions and
    CTEs. The queries progress in four tiers of five:

    | Tier | Section | Focus |
    | --- | --- | --- |
    | Simple    | 3.1 | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT` |
    | Simple+   | 3.2 | `GROUP BY`, aggregates (`SUM`, `AVG`, `COUNT`), aliases |
    | Intermediate  | 3.3 | `HAVING`, `CASE`, multi-column grouping, `NULL` handling |
    | Intermediate+ | 3.4 | Top-N per group, ranking windows, `WITH` (CTEs), subqueries |

    **Every query cell follows the same rhythm:** a plain-English explanation → the
    formatted SQL → the result table → a chart (rendered through `util_plot`, so no
    plotting code clutters the query). Several queries are adapted from the reference
    Kaggle notebook in this folder, re-expressed in SQL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup — connect to the database

    We open the existing `sales_db.duckdb`. The helper `run()` executes a SQL string,
    returns the result as a pandas DataFrame (so it displays as a clean table), and is
    what every query cell below calls.
    """)
    return


@app.cell
def _(_sql):
    from pathlib import Path

    import duckdb
    import pandas as pd

    import util_plot as up   # all matplotlib lives here

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 140)

    DB_PATH = Path.cwd() / 'sales_db.duckdb'
    con = duckdb.connect(str(DB_PATH))

    def run(_sql: str) -> pd.DataFrame:
        """Execute SQL and return the result as a DataFrame."""
        return con.sql(_sql).df()

    print('Connected. Rows in sales:', run("""
        SELECT COUNT(*) AS n
        FROM sales;
    """).iloc[0, 0])
    run("""
        DESCRIBE sales;
    """)
    return (con, run, up)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.0 — Add derived columns

    **What we are doing:** before querying, we add two *derived* columns that several
    queries reuse, so the logic lives in one place:

    - **`decade`** — the release decade, computed as `(year // 10) * 10` (floor
      division). `2006 → 2000`. Handy for grouping trends over time.
    - **`region_sum`** — the sum of the four regional sales columns. Useful as a data
      sanity check against `global_sales`.

    We use `ADD COLUMN IF NOT EXISTS` so this cell is **safe to re-run**.
    """)
    return


@app.cell
def _(con, run):
    con.execute("""
        ALTER TABLE sales ADD COLUMN IF NOT EXISTS decade INTEGER;
    """)
    con.execute("""
        ALTER TABLE sales ADD COLUMN IF NOT EXISTS region_sum DOUBLE;
    """)

    con.execute("""
        UPDATE sales
        SET decade = (year // 10) * 10;
    """)
    con.execute("""
        UPDATE sales
        SET region_sum = ROUND(na_sales + eu_sales + jp_sales + other_sales, 2);
    """)

    run("""
        SELECT
            name,
            year,
            decade,
            na_sales,
            eu_sales,
            jp_sales,
            other_sales,
            region_sum,
            global_sales
        FROM sales
        ORDER BY global_sales DESC
        LIMIT 5;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.1 — Five simple queries

    *Concepts: `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q1 · The ten best-selling games of all time

    **What we are doing:** sorting every game by worldwide sales and keeping the top
    ten. This is the bread-and-butter `ORDER BY ... DESC` + `LIMIT` pattern.
    """)
    return


@app.cell
def _(run, up):
    _sql = '''
    SELECT rank, name, platform, year, global_sales
    FROM sales
    ORDER BY global_sales DESC
    LIMIT 10
    '''
    _res = run(_sql)
    up.bar(_res, x='name', y='global_sales', horizontal=True,
           title='Top 10 best-selling games (millions of copies)',
           xlabel='Global sales (M)', ylabel='')
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q2 · The dataset at a glance

    **What we are doing:** one row of headline numbers. `COUNT(*)` counts rows;
    `COUNT(DISTINCT col)` counts unique values. A quick orientation before we dig in.
    """)
    return


@app.cell
def _(run):
    _sql = """
        SELECT
            COUNT(*) AS total_games,
            COUNT(DISTINCT platform) AS platforms,
            COUNT(DISTINCT genre) AS genres,
            COUNT(DISTINCT publisher) AS publishers,
            ROUND(SUM(global_sales), 1) AS total_global_sales_m
        FROM sales;
    """
    _res = run(_sql)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q3 · Every game released in 1985

    **What we are doing:** filtering rows with `WHERE year = 1985` — the year the
    NES launched in North America. Shows how a single predicate narrows the table.
    """)
    return


@app.cell
def _(run, up):
    _sql = '''
    SELECT name, platform, genre, global_sales
    FROM sales
    WHERE year = 1985
    ORDER BY global_sales DESC
    '''
    _res = run(_sql)
    up.bar(_res, x='name', y='global_sales',
           title='Games released in 1985, by global sales',
           xlabel='', ylabel='Global sales (M)', rotate=40)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q4 · What genres exist?

    **What we are doing:** `SELECT DISTINCT` returns the unique genre values. A simple
    way to learn the vocabulary of a categorical column.
    """)
    return


@app.cell
def _(run):
    _sql = '''
    SELECT DISTINCT genre
    FROM sales
    ORDER BY genre
    '''
    _res = run(_sql)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q5 · Mega-hits: games that sold over 20 million

    **What we are doing:** filtering on a numeric measure (`global_sales > 20`). Only a
    handful of titles clear this bar.
    """)
    return


@app.cell
def _(run, up):
    _sql = '''
    SELECT name, platform, year, global_sales
    FROM sales
    WHERE global_sales > 20
    ORDER BY global_sales DESC
    '''
    _res = run(_sql)
    up.bar(_res, x='name', y='global_sales', horizontal=True,
           title='Games that sold more than 20M copies',
           xlabel='Global sales (M)', ylabel='')
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.2 — Five simple+ queries

    *Concepts: `GROUP BY` with `SUM` / `AVG` / `COUNT`, column aliases, `ROUND`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q6 · Total sales by genre

    **What we are doing:** collapsing thousands of rows into one row per genre and
    summing their sales. This is the core `GROUP BY` + aggregate idea.
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        SELECT
            genre,
            ROUND(SUM(global_sales), 2) AS total_sales
        FROM sales
        GROUP BY genre
        ORDER BY total_sales DESC;
    """
    _res = run(_sql)
    up.bar(_res, x='genre', y='total_sales',
           title='Total global sales by genre',
           xlabel='', ylabel='Global sales (M)', rotate=40)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q7 · How many games per platform? (top 15)

    **What we are doing:** counting rows within each platform group. The DS, PS2 and
    Wii dominate the catalog.
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        SELECT
            platform,
            COUNT(*) AS games
        FROM sales
        GROUP BY platform
        ORDER BY games DESC
        LIMIT 15;
    """
    _res = run(_sql)
    up.bar(_res, x='platform', y='games',
           title='Number of games per platform (top 15)',
           xlabel='', ylabel='Games', rotate=0)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q8 · Which genres sell best *per game*?

    **What we are doing:** `AVG` instead of `SUM` answers a different question — not the
    biggest category, but the highest average sales per title. Platform and Shooter
    games punch above their weight here.
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        SELECT
            genre,
            COUNT(*) AS games,
            ROUND(AVG(global_sales), 3) AS avg_sales
        FROM sales
        GROUP BY genre
        ORDER BY avg_sales DESC;
    """
    _res = run(_sql)
    up.bar(_res, x='genre', y='avg_sales',
           title='Average global sales per game, by genre',
           xlabel='', ylabel='Avg sales per game (M)', rotate=40)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q9 · Releases and sales per decade

    **What we are doing:** grouping by our derived `decade` column. Shows the rise of
    the industry through the 2000s. We drop `NULL` decades (missing years).
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        SELECT
            decade,
            COUNT(*) AS games,
            ROUND(SUM(global_sales),1) AS total_sales
        FROM sales
        WHERE decade IS NOT NULL
        GROUP BY decade
        ORDER BY decade;
    """
    _res = run(_sql)
    up.bar(_res, x='decade', y='games',
           title='Number of game releases per decade',
           xlabel='Decade', ylabel='Games', rotate=0)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q10 · The global market split by region

    **What we are doing:** summing each regional column, then stacking the four results
    into one column with `UNION ALL` so we can pie-chart them. North America is the
    largest single market in this dataset.
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        SELECT
            'North America' AS region,
            ROUND(SUM(na_sales), 1) AS sales
        FROM sales
        UNION ALL
        SELECT
            'Europe',
            ROUND(SUM(eu_sales), 1)
        FROM sales
        UNION ALL
        SELECT
            'Japan',
            ROUND(SUM(jp_sales), 1)
        FROM sales
        UNION ALL
        SELECT
            'Other',
            ROUND(SUM(other_sales), 1)
        FROM sales
        ORDER BY sales DESC;
    """
    _res = run(_sql)
    up.pie(_res, labels='region', values='sales',
           title='Share of global sales by region')
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.3 — Five intermediate queries

    *Concepts: `HAVING`, `CASE`, multi-column grouping, `NULL` handling.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q11 · Prolific publishers (more than 100 games)

    **What we are doing:** `WHERE` filters *rows before* grouping; `HAVING` filters
    *groups after* aggregating. Here `HAVING COUNT(*) > 100` keeps only publishers with
    a large catalog, and we report each one's total and average sales.
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        SELECT
            publisher,
            COUNT(*) AS games,
            ROUND(SUM(global_sales), 1) AS total_sales,
            ROUND(AVG(global_sales), 3) AS avg_sales
        FROM sales
        WHERE publisher IS NOT NULL
        GROUP BY publisher
        HAVING COUNT(*) > 100
        ORDER BY total_sales DESC;
    """
    _res = run(_sql)
    up.bar(_res.head(15), x='publisher', y='total_sales',
           title='Total sales of high-volume publishers (>100 games)',
           xlabel='', ylabel='Global sales (M)', rotate=60)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q12 · Regional taste: sales by genre across regions

    **What we are doing:** aggregating four measures at once, grouped by genre. The
    grouped bars reveal regional preferences — e.g. Role-Playing games are
    proportionally far bigger in Japan. (Adapted from the Kaggle notebook's regional
    breakdown.)
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        SELECT
            genre,
            ROUND(SUM(na_sales), 1) AS na_sales,
            ROUND(SUM(eu_sales), 1) AS eu_sales,
            ROUND(SUM(jp_sales), 1) AS jp_sales,
            ROUND(SUM(other_sales), 1) AS other_sales
        FROM sales
        GROUP BY genre
        ORDER BY (SUM(na_sales) + SUM(eu_sales) + SUM(jp_sales) + SUM(other_sales)) DESC;
    """
    _res = run(_sql)
    up.grouped_bar(_res, x='genre',
                   y_cols=['na_sales', 'eu_sales', 'jp_sales', 'other_sales'],
                   title='Regional sales by genre',
                   xlabel='', ylabel='Sales (M)', rotate=40)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q13 · Classifying games into sales tiers with CASE

    **What we are doing:** `CASE` builds a new categorical column on the fly. We bucket
    every game into Blockbuster / Hit / Niche, then count the buckets. It shows how
    top-heavy the market is: a tiny number of blockbusters, a long tail of niche titles.
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        SELECT
            CASE WHEN global_sales >= 10 THEN 'Blockbuster (>=10M)' WHEN global_sales >= 1 THEN 'Hit (1-10M)' ELSE 'Niche (<1M)' END AS sales_tier,
            COUNT(*) AS games,
            ROUND(SUM(global_sales), 1) AS total_sales
        FROM sales
        GROUP BY sales_tier
        ORDER BY MIN(global_sales) DESC;
    """
    _res = run(_sql)
    up.bar(_res, x='sales_tier', y='games',
           title='How many games fall in each sales tier?',
           xlabel='', ylabel='Games', rotate=20)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q14 · A missing-data audit (NULL handling)

    **What we are doing:** teaching the difference between `COUNT(*)` (all rows) and
    `COUNT(col)` (non-NULL values), plus counting NULLs explicitly with `CASE`. This
    quantifies the gaps we already know about: missing years and publishers.
    """)
    return


@app.cell
def _(run):
    _sql = """
        SELECT
            COUNT(*) AS total_rows,
            COUNT(year) AS rows_with_year,
            SUM(CASE WHEN year IS NULL THEN 1 ELSE 0 END) AS missing_year,
            SUM(CASE WHEN publisher IS NULL THEN 1 ELSE 0 END) AS missing_publisher
        FROM sales;
    """
    _res = run(_sql)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q15 · Best average-selling platforms (with a volume floor)

    **What we are doing:** combining `AVG` with a `HAVING` floor so tiny platforms with
    one lucky hit don't dominate. We require at least 50 games per platform.
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        SELECT
            platform,
            COUNT(*) AS games,
            ROUND(AVG(global_sales), 3) AS avg_sales
        FROM sales
        GROUP BY platform
        HAVING COUNT(*) >= 50
        ORDER BY avg_sales DESC
        LIMIT 15;
    """
    _res = run(_sql)
    up.bar(_res, x='platform', y='avg_sales',
           title='Average sales per game by platform (>=50 games)',
           xlabel='', ylabel='Avg sales per game (M)', rotate=0)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.4 — Five intermediate+ queries

    *Concepts: Top-N per group, ranking window functions (`RANK`, `ROW_NUMBER`),
    running totals (`SUM() OVER`), `LAG`, common table expressions (`WITH`), and
    subqueries.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q16 · Top 5 publishers by total sales — using a CTE (`WITH`)

    **What we are doing:** a **common table expression** names an intermediate result
    (`publisher_totals`) so the final query reads cleanly. CTEs are the readable way to
    build multi-step queries. (Compare with Q11, which used `HAVING`.)
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        WITH publisher_totals AS (
        SELECT
            publisher,
            ROUND(SUM(global_sales), 1) AS total_sales
        FROM sales
        WHERE publisher IS NOT NULL
        GROUP BY publisher )
        SELECT *
        FROM publisher_totals
        ORDER BY total_sales DESC
        LIMIT 5;
    """
    _res = run(_sql)
    up.bar(_res, x='publisher', y='total_sales',
           title='Top 5 publishers by total global sales',
           xlabel='', ylabel='Global sales (M)', rotate=20)
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q17 · The #1 best-seller in every genre (ranking window)

    **What we are doing:** `RANK() OVER (PARTITION BY genre ORDER BY global_sales DESC)`
    numbers games *within* each genre. DuckDB's `QUALIFY` then keeps only rank 1 — the
    champion of each genre — in a single, elegant statement.
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        SELECT
            genre,
            name,
            platform,
            global_sales,
            RANK() OVER (PARTITION BY genre
        ORDER BY global_sales DESC) AS genre_rank
        FROM sales QUALIFY genre_rank = 1
        ORDER BY global_sales DESC;
    """
    _res = run(_sql)
    up.bar(_res, x='name', y='global_sales', horizontal=True,
           title='Best-selling game in each genre',
           xlabel='Global sales (M)', ylabel='')
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q18 · How concentrated is the market? (running total)

    **What we are doing:** a **running total** window (`SUM() OVER (ORDER BY ...)`)
    accumulates sales from the biggest game downward, and a scalar subquery turns it
    into a percentage of *all* sales. The curve shows that the top 100 titles already
    account for a large slice of the entire market.
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        WITH ranked AS (
        SELECT
            name,
            global_sales,
            ROW_NUMBER() OVER (
        ORDER BY global_sales DESC) AS game_no, SUM(global_sales) OVER (
        ORDER BY global_sales DESC ROWS UNBOUNDED PRECEDING) AS cumulative_sales
        FROM sales )
        SELECT
            game_no,
            name,
            global_sales,
            ROUND(cumulative_sales, 1) AS cumulative_sales,
            ROUND(100 * cumulative_sales / (
        SELECT SUM(global_sales)
        FROM sales), 2) AS pct_of_all_sales
        FROM ranked
        WHERE game_no <= 100
        ORDER BY game_no;
    """
    _res = run(_sql)
    up.area(_res, x='game_no', y='pct_of_all_sales',
            title='Cumulative share of all sales held by the top 100 games',
            xlabel='Game rank (by sales)', ylabel='% of all global sales')
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q19 · The flagship title of each platform (Top-N per group)

    **What we are doing:** the classic *greatest-per-group* problem. A subquery in the
    `FROM` clause numbers games within each platform with `ROW_NUMBER()`; the outer
    query keeps `rn = 1`. This pattern generalizes to "top N per group" by changing the
    filter to `rn <= N`.
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        SELECT
            platform,
            name,
            year,
            global_sales
        FROM (
        SELECT
            platform,
            name,
            year,
            global_sales,
            ROW_NUMBER() OVER (PARTITION BY platform
        ORDER BY global_sales DESC) AS rn
        FROM sales ) ranked
        WHERE rn = 1
        ORDER BY global_sales DESC
        LIMIT 15;
    """
    _res = run(_sql)
    up.bar(_res, x='name', y='global_sales', horizontal=True,
           title='Best-selling game on each platform (top 15 platforms)',
           xlabel='Global sales (M)', ylabel='')
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q20 · Year-over-year growth with LAG

    **What we are doing:** a CTE aggregates sales per year, then `LAG()` reaches back to
    the previous year's value so we can compute absolute and percentage change. We cap
    at 2016 because later years are sparsely scraped and would distort the trend.
    """)
    return


@app.cell
def _(run, up):
    _sql = """
        WITH yearly AS (
        SELECT
            year,
            ROUND(SUM(global_sales), 1) AS total_sales
        FROM sales
        WHERE year IS NOT NULL
        AND year <= 2016
        GROUP BY year )
        SELECT
            year,
            total_sales,
            LAG(total_sales) OVER (
        ORDER BY year) AS prev_year_sales, ROUND(total_sales - LAG(total_sales) OVER (
        ORDER BY year), 1) AS yoy_change, ROUND(100.0 * (total_sales - LAG(total_sales) OVER (
        ORDER BY year)) / LAG(total_sales) OVER (
        ORDER BY year), 1) AS yoy_pct
        FROM yearly
        ORDER BY year;
    """
    _res = run(_sql)
    up.line(_res, x='year', y='total_sales',
            title='Total global sales per year (1980-2016)',
            xlabel='Year', ylabel='Global sales (M)')
    _res
    return (_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.5 — Key SQL concepts, recapped

    Each query above was chosen to introduce one more idea. Here is the map of
    concepts the notebook covers, in the order they appeared:

    | Query | SQL concept introduced |
    | --- | --- |
    | Q1  | `ORDER BY ... DESC`, `LIMIT` |
    | Q2  | `COUNT(*)`, `COUNT(DISTINCT ...)`, `SUM` |
    | Q3  | `WHERE` on a value |
    | Q4  | `SELECT DISTINCT` |
    | Q5  | `WHERE` on a numeric measure |
    | Q6  | `GROUP BY` + `SUM`, aliases |
    | Q7  | `GROUP BY` + `COUNT` |
    | Q8  | `AVG` (per-group average) |
    | Q9  | grouping on a derived column (`decade`) |
    | Q10 | `UNION ALL` to reshape for a chart |
    | Q11 | `HAVING` vs `WHERE` |
    | Q12 | multiple aggregates, regional grouping |
    | Q13 | `CASE` (conditional buckets) |
    | Q14 | `NULL` handling: `COUNT(col)` vs `COUNT(*)` |
    | Q15 | `AVG` with a `HAVING` volume floor |
    | Q16 | CTE with `WITH` |
    | Q17 | `RANK() OVER (PARTITION BY ...)` + `QUALIFY` |
    | Q18 | running total `SUM() OVER (... ROWS UNBOUNDED PRECEDING)` + scalar subquery |
    | Q19 | Top-N per group via `ROW_NUMBER()` in a subquery |
    | Q20 | `LAG()` for period-over-period change |

    **The progression in one sentence:** start by *reading and filtering* rows (3.1),
    learn to *summarize* them in groups (3.2), then *filter and reshape* those groups
    (3.3), and finally *rank and compare across* groups with window functions and CTEs
    (3.4).
    """)
    return


@app.cell
def _(con):
    con.close()
    print('Done. Connection closed.')
    return


if __name__ == "__main__":
    app.run()
