import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import os
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="altair")
    return duckdb, mo, os


@app.cell
def _(duckdb, os):
    _nb_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "."
    DB_PATH = os.path.join(_nb_dir, "netflix.duckdb")
    con = duckdb.connect(DB_PATH)
    print(f"Connected to: {DB_PATH}")
    return (con,)


@app.cell
def _(mo):
    mo.md(r"""
    # 🎬 Notebook 2 — Netflix Data Analysis

    **Pre-requisite:** Run `01_build_netflix_db.py` first to create `netflix.duckdb`.

    This notebook:
    1. Adds **derived columns** (year_added, month_added, duration_min, season_count, first_country, age_group)
    2. Runs **20 SQL queries** across four difficulty tiers
    3. Displays results as interactive tables and plots (via Marimo's built-in `mo.ui` and `altair`/`matplotlib`)

    ---
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Section 1 — Add Derived Columns

    Raw CSV columns give us a solid base, but many analyses require
    pre-computed values.  We create a **view** (not a new table) so
    the derivations stay in sync with the base table automatically.

    | New column | Source | Logic |
    |---|---|---|
    | `year_added` | `date_added` | `EXTRACT(YEAR FROM …)` |
    | `month_added` | `date_added` | `EXTRACT(MONTH FROM …)` |
    | `month_name` | `date_added` | `MONTHNAME(…)` |
    | `duration_min` | `duration` | Minutes for Movies (NULL for TV Shows) |
    | `season_count` | `duration` | Season number for TV Shows (NULL for Movies) |
    | `first_country` | `country` | First country in comma-separated list |
    | `age_group` | `rating` | Human-readable audience group |
    """)
    return


@app.cell
def _(con):
    con.execute("DROP VIEW IF EXISTS netflix")
    con.execute(
        """
        CREATE VIEW netflix AS
        SELECT
            *,

            -- Date-derived columns
            -- date_added is "Month DD, YYYY" (e.g. "September 25, 2021") — use STRPTIME
            TRY_STRPTIME(TRIM(date_added), '%B %d, %Y')::DATE          AS date_added_parsed,
            EXTRACT(YEAR  FROM TRY_STRPTIME(TRIM(date_added), '%B %d, %Y')) AS year_added,
            EXTRACT(MONTH FROM TRY_STRPTIME(TRIM(date_added), '%B %d, %Y')) AS month_added,
            STRFTIME(TRY_STRPTIME(TRIM(date_added), '%B %d, %Y'), '%B') AS month_name,

            -- Duration: minutes for Movies, NULL for TV Shows
            CASE
                WHEN type = 'Movie'
                 AND duration LIKE '%min%'
                THEN CAST(REGEXP_REPLACE(duration, '[^0-9]', '', 'g') AS INTEGER)
                ELSE NULL
            END AS duration_min,

            -- Season count for TV Shows, NULL for Movies
            CASE
                WHEN type = 'TV Show'
                 AND duration LIKE '%Season%'
                THEN CAST(REGEXP_REPLACE(duration, '[^0-9]', '', 'g') AS INTEGER)
                ELSE NULL
            END AS season_count,

            -- First country listed (multi-country entries use commas)
            TRIM(SPLIT_PART(country, ',', 1))  AS first_country,

            -- Audience age group
            CASE rating
                WHEN 'TV-Y'    THEN 'Kids'
                WHEN 'TV-Y7'   THEN 'Older Kids'
                WHEN 'TV-Y7-FV'THEN 'Older Kids'
                WHEN 'TV-G'    THEN 'Kids'
                WHEN 'G'       THEN 'Kids'
                WHEN 'TV-PG'   THEN 'Older Kids'
                WHEN 'PG'      THEN 'Older Kids'
                WHEN 'PG-13'   THEN 'Teens'
                WHEN 'TV-14'   THEN 'Teens'
                WHEN 'TV-MA'   THEN 'Adults'
                WHEN 'R'       THEN 'Adults'
                WHEN 'NC-17'   THEN 'Adults'
                ELSE 'Unknown'
            END AS age_group

        FROM netflix_titles
        """
    )
    print("✅  View 'netflix' created with derived columns.")
    return


@app.cell
def _(con, mo):
    _df = con.execute("SELECT * FROM netflix LIMIT 5").df()
    mo.ui.table(_df, label="netflix view — first 5 rows (with derived columns)")
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Section 2 — Simple Queries

    These five queries each ask a single, direct question about the dataset
    using basic `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, and `LIMIT`.
    No subqueries, no joins — just the fundamentals.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q1 · Movies vs. TV Shows — how many of each?

    **Concept:** `GROUP BY` + `COUNT(*)`
    **Why it matters:** The very first thing to know about any catalogue
    is its content split.  Netflix is predominantly Movies (~70 %).

    ```sql
    SELECT   type,
             COUNT(*)                              AS total,
             ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
    FROM     netflix
    GROUP BY type
    ORDER BY total DESC;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   type,
                 COUNT(*)                                              AS total,
                 ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1)  AS pct
        FROM     netflix
        GROUP BY type
        ORDER BY total DESC
        """
    ).df()
    mo.ui.table(_df, label="Q1 · Movies vs TV Shows")
    return


@app.cell
def _(con, mo):
    import plots_02 as _p
    _w = _p.chart_q1(con, mo)
    _w
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q2 · Top 10 countries producing Netflix content

    **Concept:** `GROUP BY`, `COUNT`, `ORDER BY … DESC`, `LIMIT`
    **Why it matters:** Shows geographic concentration.
    The United States dominates, followed by India.

    ```sql
    SELECT   first_country,
             COUNT(*) AS titles
    FROM     netflix
    WHERE    first_country IS NOT NULL
      AND    first_country <> ''
    GROUP BY first_country
    ORDER BY titles DESC
    LIMIT    10;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   first_country,
                 COUNT(*) AS titles
        FROM     netflix
        WHERE    first_country IS NOT NULL
          AND    first_country <> ''
        GROUP BY first_country
        ORDER BY titles DESC
        LIMIT    10
        """
    ).df()
    mo.ui.table(_df, label="Q2 · Top 10 producing countries")
    return


@app.cell
def _(con, mo):
    import plots_02 as _p
    _w = _p.chart_q2(con, mo)
    _w
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q3 · Content added per year

    **Concept:** `GROUP BY` on a derived column (`year_added`)
    **Why it matters:** Tracks Netflix's content growth trajectory.
    Huge ramp-up from 2016 to 2019, then a slight COVID dip.

    ```sql
    SELECT   year_added,
             COUNT(*) AS titles_added
    FROM     netflix
    WHERE    year_added IS NOT NULL
    GROUP BY year_added
    ORDER BY year_added;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   year_added,
                 COUNT(*) AS titles_added
        FROM     netflix
        WHERE    year_added IS NOT NULL
        GROUP BY year_added
        ORDER BY year_added
        """
    ).df()
    mo.ui.table(_df, label="Q3 · Titles added per year")
    return


@app.cell
def _(con, mo):
    import plots_02 as _p
    _w = _p.chart_q3(con, mo)
    _w
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q4 · Titles released before the year 2000

    **Concept:** `WHERE` filter on a numeric column
    **Why it matters:** Identifies "classic" titles in the catalogue —
    movies and shows produced before streaming existed.

    ```sql
    SELECT   title, type, release_year, first_country
    FROM     netflix
    WHERE    release_year < 2000
    ORDER BY release_year
    LIMIT    20;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   title, type, release_year, first_country
        FROM     netflix
        WHERE    release_year < 2000
        ORDER BY release_year
        LIMIT    20
        """
    ).df()
    mo.ui.table(_df, label="Q4 · Titles released before 2000")
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q5 · Distribution by maturity rating

    **Concept:** `GROUP BY`, `COUNT`, `ORDER BY`
    **Why it matters:** Shows how family-friendly (or adult-oriented)
    the Netflix library is. TV-MA (adult) is by far the most common rating.

    ```sql
    SELECT   rating,
             age_group,
             COUNT(*) AS titles
    FROM     netflix
    WHERE    rating IS NOT NULL
    GROUP BY rating, age_group
    ORDER BY titles DESC;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   rating,
                 age_group,
                 COUNT(*) AS titles
        FROM     netflix
        WHERE    rating IS NOT NULL
        GROUP BY rating, age_group
        ORDER BY titles DESC
        """
    ).df()
    mo.ui.table(_df, label="Q5 · Titles by rating")
    return


@app.cell
def _(con, mo):
    import plots_02 as _p
    _w = _p.chart_q5(con, mo)
    _w
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Section 3 — Simple+ Queries

    One level up: multi-column filters, string functions, `CASE` expressions,
    `HAVING`, and window-function basics (`SUM … OVER ()`).
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q6 · Longest movies on Netflix

    **Concept:** `WHERE type = 'Movie'`, `ORDER BY duration_min DESC`
    **Why it matters:** Demonstrates filtering on a derived numeric column.
    Epic films (> 3 hours) are rare on streaming.

    ```sql
    SELECT   title, first_country, release_year,
             duration_min AS runtime_minutes
    FROM     netflix
    WHERE    type = 'Movie'
      AND    duration_min IS NOT NULL
    ORDER BY duration_min DESC
    LIMIT    15;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   title, first_country, release_year,
                 duration_min AS runtime_minutes
        FROM     netflix
        WHERE    type = 'Movie'
          AND    duration_min IS NOT NULL
        ORDER BY duration_min DESC
        LIMIT    15
        """
    ).df()
    mo.ui.table(_df, label="Q6 · Longest movies")
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q7 · TV Shows with the most seasons

    **Concept:** `WHERE type = 'TV Show'`, `ORDER BY season_count DESC`
    **Why it matters:** Long-running shows signal Netflix's investment
    in sustained story-telling.

    ```sql
    SELECT   title, first_country, release_year,
             season_count AS seasons
    FROM     netflix
    WHERE    type = 'TV Show'
      AND    season_count IS NOT NULL
    ORDER BY season_count DESC
    LIMIT    15;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   title, first_country, release_year,
                 season_count AS seasons
        FROM     netflix
        WHERE    type = 'TV Show'
          AND    season_count IS NOT NULL
        ORDER BY season_count DESC
        LIMIT    15
        """
    ).df()
    mo.ui.table(_df, label="Q7 · TV Shows with most seasons")
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q8 · Content added each month of the year

    **Concept:** `GROUP BY month_added`, labelling with `month_name`
    **Why it matters:** Netflix has a seasonal release cadence.
    January is historically a big content-drop month.

    ```sql
    SELECT   CAST(month_added AS INTEGER)  AS month_num,
             month_name,
             COUNT(*)                      AS titles
    FROM     netflix
    WHERE    month_added IS NOT NULL
    GROUP BY month_num, month_name
    ORDER BY month_num;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   CAST(month_added AS INTEGER)  AS month_num,
                 month_name,
                 COUNT(*)                      AS titles
        FROM     netflix
        WHERE    month_added IS NOT NULL
        GROUP BY month_num, month_name
        ORDER BY month_num
        """
    ).df()
    mo.ui.table(_df, label="Q8 · Titles added by month")
    return


@app.cell
def _(con, mo):
    import plots_02 as _p
    _w = _p.chart_q8(con, mo)
    _w
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q9 · Countries with more than 100 Movies AND more than 10 TV Shows

    **Concept:** `HAVING` clause with multiple conditions, conditional aggregation
    **Why it matters:** Identifies markets where Netflix has deep investment
    in **both** content formats — not just one.

    ```sql
    SELECT   first_country,
             COUNT(CASE WHEN type = 'Movie'   THEN 1 END) AS movies,
             COUNT(CASE WHEN type = 'TV Show' THEN 1 END) AS tv_shows
    FROM     netflix
    WHERE    first_country IS NOT NULL AND first_country <> ''
    GROUP BY first_country
    HAVING   COUNT(CASE WHEN type = 'Movie'   THEN 1 END) > 100
       AND   COUNT(CASE WHEN type = 'TV Show' THEN 1 END) > 10
    ORDER BY movies DESC;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   first_country,
                 COUNT(CASE WHEN type = 'Movie'   THEN 1 END) AS movies,
                 COUNT(CASE WHEN type = 'TV Show' THEN 1 END) AS tv_shows
        FROM     netflix
        WHERE    first_country IS NOT NULL AND first_country <> ''
        GROUP BY first_country
        HAVING   COUNT(CASE WHEN type = 'Movie'   THEN 1 END) > 100
           AND   COUNT(CASE WHEN type = 'TV Show' THEN 1 END) > 10
        ORDER BY movies DESC
        """
    ).df()
    mo.ui.table(_df, label="Q9 · Multi-format country markets")
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q10 · Average movie runtime by country (top 15 countries)

    **Concept:** `AVG()`, `ROUND()`, filtered `GROUP BY`
    **Why it matters:** Cultural differences in film length are real —
    Indian Bollywood films are famously long, for example.

    ```sql
    SELECT   first_country,
             COUNT(*)               AS movies,
             ROUND(AVG(duration_min), 1) AS avg_runtime_min
    FROM     netflix
    WHERE    type = 'Movie'
      AND    duration_min IS NOT NULL
      AND    first_country IS NOT NULL AND first_country <> ''
    GROUP BY first_country
    HAVING   COUNT(*) >= 20
    ORDER BY avg_runtime_min DESC
    LIMIT    15;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   first_country,
                 COUNT(*)                    AS movies,
                 ROUND(AVG(duration_min), 1) AS avg_runtime_min
        FROM     netflix
        WHERE    type = 'Movie'
          AND    duration_min IS NOT NULL
          AND    first_country IS NOT NULL AND first_country <> ''
        GROUP BY first_country
        HAVING   COUNT(*) >= 20
        ORDER BY avg_runtime_min DESC
        LIMIT    15
        """
    ).df()
    mo.ui.table(_df, label="Q10 · Avg movie runtime by country")
    return


@app.cell
def _(con, mo):
    import plots_02 as _p
    _w = _p.chart_q10(con, mo)
    _w
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Section 4 — Intermediate Queries

    Aggregations with `CASE WHEN`, string splitting to handle
    multi-valued fields, genre analysis, time-gap calculations,
    and cross-type comparisons using pivot-style logic.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q11 · Top 20 most frequent genres (exploded from `listed_in`)

    **Concept:** `UNNEST(STRING_SPLIT())` to explode multi-value field
    **Why it matters:** `listed_in` can contain multiple genres separated
    by commas.  To count genres accurately we must split and explode each
    row before aggregating.

    ```sql
    SELECT   TRIM(genre)  AS genre,
             COUNT(*)     AS appearances
    FROM (
        SELECT UNNEST(STRING_SPLIT(listed_in, ',')) AS genre
        FROM   netflix
        WHERE  listed_in IS NOT NULL
    ) sub
    GROUP BY genre
    ORDER BY appearances DESC
    LIMIT    20;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   TRIM(genre)  AS genre,
                 COUNT(*)     AS appearances
        FROM (
            SELECT UNNEST(STRING_SPLIT(listed_in, ',')) AS genre
            FROM   netflix
            WHERE  listed_in IS NOT NULL
        ) sub
        GROUP BY genre
        ORDER BY appearances DESC
        LIMIT    20
        """
    ).df()
    mo.ui.table(_df, label="Q11 · Top 20 genres")
    return


@app.cell
def _(con, mo):
    import plots_02 as _p
    _w = _p.chart_q11(con, mo)
    _w
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q12 · Directors with the most titles (Movies and TV Shows separately)

    **Concept:** Conditional aggregation (`COUNT CASE WHEN`) as a
    column-pivot; `HAVING` to filter out NULL directors.

    **Why it matters:** Identifies prolific Netflix-associated directors.
    Many directors show up repeatedly in stand-up comedy specials.

    ```sql
    SELECT   director,
             COUNT(*)                                  AS total,
             COUNT(CASE WHEN type='Movie'   THEN 1 END) AS movies,
             COUNT(CASE WHEN type='TV Show' THEN 1 END) AS tv_shows
    FROM     netflix
    WHERE    director IS NOT NULL AND director <> ''
    GROUP BY director
    ORDER BY total DESC
    LIMIT    20;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   director,
                 COUNT(*)                                    AS total,
                 COUNT(CASE WHEN type='Movie'   THEN 1 END) AS movies,
                 COUNT(CASE WHEN type='TV Show' THEN 1 END) AS tv_shows
        FROM     netflix
        WHERE    director IS NOT NULL AND director <> ''
        GROUP BY director
        ORDER BY total DESC
        LIMIT    20
        """
    ).df()
    mo.ui.table(_df, label="Q12 · Most prolific directors")
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q13 · Gap between release year and year added to Netflix

    **Concept:** Arithmetic on two integer columns; `AVG`, `MIN`, `MAX`
    grouped by type.

    **Why it matters:** How quickly does Netflix acquire content after
    it's produced?  A small gap = Netflix originals or same-year deals.
    A large gap = back-catalogue acquisitions.

    ```sql
    SELECT   type,
             ROUND(AVG(year_added - release_year), 1) AS avg_gap_years,
             MIN(year_added - release_year)           AS min_gap,
             MAX(year_added - release_year)           AS max_gap
    FROM     netflix
    WHERE    year_added IS NOT NULL
      AND    release_year IS NOT NULL
      AND    year_added >= release_year
    GROUP BY type;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   type,
                 ROUND(AVG(year_added - release_year), 1) AS avg_gap_years,
                 MIN(year_added - release_year)           AS min_gap,
                 MAX(year_added - release_year)           AS max_gap
        FROM     netflix
        WHERE    year_added IS NOT NULL
          AND    release_year IS NOT NULL
          AND    year_added >= release_year
        GROUP BY type
        """
    ).df()
    mo.ui.table(_df, label="Q13 · Gap: release year vs added year")
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q14 · Movies vs TV Shows added each year (crosstab)

    **Concept:** Conditional aggregation as a pivot / crosstab.
    One row per year, separate columns for each content type.

    **Why it matters:** Shows how the Movies/TV balance shifted
    as Netflix's strategy evolved (TV originals grew after 2016).

    ```sql
    SELECT   year_added,
             COUNT(CASE WHEN type = 'Movie'   THEN 1 END) AS movies,
             COUNT(CASE WHEN type = 'TV Show' THEN 1 END) AS tv_shows,
             COUNT(*)                                      AS total
    FROM     netflix
    WHERE    year_added IS NOT NULL
    GROUP BY year_added
    ORDER BY year_added;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   year_added,
                 COUNT(CASE WHEN type = 'Movie'   THEN 1 END) AS movies,
                 COUNT(CASE WHEN type = 'TV Show' THEN 1 END) AS tv_shows,
                 COUNT(*)                                      AS total
        FROM     netflix
        WHERE    year_added IS NOT NULL
        GROUP BY year_added
        ORDER BY year_added
        """
    ).df()
    mo.ui.table(_df, label="Q14 · Movies vs TV Shows by year")
    return


@app.cell
def _(con, mo):
    import plots_02 as _p
    _w = _p.chart_q14(con, mo)
    _w
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q15 · Most common cast members across all titles

    **Concept:** `UNNEST(STRING_SPLIT())` on the `cast` column (multi-value),
    `GROUP BY`, `ORDER BY`, `LIMIT`.

    **Why it matters:** Which actors appear most frequently across Netflix's
    catalogue?  Reveals Netflix's preferred talent relationships.

    ```sql
    SELECT   TRIM(actor) AS actor,
             COUNT(*)    AS appearances
    FROM (
        SELECT UNNEST(STRING_SPLIT("cast", ',')) AS actor
        FROM   netflix
        WHERE  "cast" IS NOT NULL AND "cast" <> ''
    ) sub
    WHERE TRIM(actor) <> ''
    GROUP BY actor
    ORDER BY appearances DESC
    LIMIT    20;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        SELECT   TRIM(actor) AS actor,
                 COUNT(*)    AS appearances
        FROM (
            SELECT UNNEST(STRING_SPLIT("cast", ',')) AS actor
            FROM   netflix
            WHERE  "cast" IS NOT NULL AND "cast" <> ''
        ) sub
        WHERE TRIM(actor) <> ''
        GROUP BY actor
        ORDER BY appearances DESC
        LIMIT    20
        """
    ).df()
    mo.ui.table(_df, label="Q15 · Most frequent cast members")
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Section 5 — Intermediate+ Queries

    Top-N per group, window ranking functions (`RANK`, `ROW_NUMBER`,
    `NTILE`), running totals, and `WITH` (CTE) subqueries.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q16 · Top 3 genres per content type (Top-N per group with CTE + RANK)

    **Concept:** `WITH` CTE → `RANK() OVER (PARTITION BY … ORDER BY …)` → outer `WHERE rank <= 3`

    **Why it matters:** Illustrates the canonical Top-N-per-group pattern.
    The most important SQL window-function use case you will encounter.

    ```sql
    WITH genre_counts AS (
        SELECT   type,
                 TRIM(genre) AS genre,
                 COUNT(*)    AS appearances
        FROM (
            SELECT type,
                   UNNEST(STRING_SPLIT(listed_in, ',')) AS genre
            FROM   netflix
            WHERE  listed_in IS NOT NULL
        ) exploded
        GROUP BY type, genre
    ),
    ranked AS (
        SELECT *,
               RANK() OVER (PARTITION BY type ORDER BY appearances DESC) AS rnk
        FROM   genre_counts
    )
    SELECT type, genre, appearances, rnk
    FROM   ranked
    WHERE  rnk <= 3
    ORDER BY type, rnk;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        WITH genre_counts AS (
            SELECT   type,
                     TRIM(genre) AS genre,
                     COUNT(*)    AS appearances
            FROM (
                SELECT type,
                       UNNEST(STRING_SPLIT(listed_in, ',')) AS genre
                FROM   netflix
                WHERE  listed_in IS NOT NULL
            ) exploded
            GROUP BY type, genre
        ),
        ranked AS (
            SELECT *,
                   RANK() OVER (PARTITION BY type ORDER BY appearances DESC) AS rnk
            FROM   genre_counts
        )
        SELECT type, genre, appearances, rnk
        FROM   ranked
        WHERE  rnk <= 3
        ORDER BY type, rnk
        """
    ).df()
    mo.ui.table(_df, label="Q16 · Top 3 genres per content type")
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q17 · Running total of titles added over time

    **Concept:** `SUM() OVER (ORDER BY year_added)` — a cumulative window function

    **Why it matters:** Shows total catalogue size as it grew year by year.
    The cumulative sum makes the growth story more dramatic than a per-year bar chart.

    ```sql
    WITH yearly AS (
        SELECT   year_added,
                 COUNT(*) AS titles_added
        FROM     netflix
        WHERE    year_added IS NOT NULL
        GROUP BY year_added
    )
    SELECT year_added,
           titles_added,
           SUM(titles_added) OVER (ORDER BY year_added) AS cumulative_total
    FROM   yearly
    ORDER BY year_added;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        WITH yearly AS (
            SELECT   year_added,
                     COUNT(*) AS titles_added
            FROM     netflix
            WHERE    year_added IS NOT NULL
            GROUP BY year_added
        )
        SELECT year_added,
               titles_added,
               SUM(titles_added) OVER (ORDER BY year_added) AS cumulative_total
        FROM   yearly
        ORDER BY year_added
        """
    ).df()
    mo.ui.table(_df, label="Q17 · Running total of Netflix titles")
    return


@app.cell
def _(con, mo):
    import plots_02 as _p
    _w = _p.chart_q17(con, mo)
    _w
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q18 · Rank countries by content volume, show percentile tier

    **Concept:** `NTILE(4)` window function to bucket rows into quartiles,
    combined with `ROW_NUMBER()` for absolute rank.

    **Why it matters:** `NTILE` is an elegant way to label rows as Top 25 %,
    Next 25 %, etc. — very useful in business reporting.

    ```sql
    WITH country_totals AS (
        SELECT   first_country,
                 COUNT(*) AS titles
        FROM     netflix
        WHERE    first_country IS NOT NULL AND first_country <> ''
        GROUP BY first_country
    )
    SELECT first_country,
           titles,
           ROW_NUMBER() OVER (ORDER BY titles DESC)           AS country_rank,
           NTILE(4)     OVER (ORDER BY titles DESC)           AS quartile,
           CASE NTILE(4) OVER (ORDER BY titles DESC)
               WHEN 1 THEN 'Top 25%'
               WHEN 2 THEN 'Upper-Mid'
               WHEN 3 THEN 'Lower-Mid'
               ELSE        'Bottom 25%'
           END                                                AS tier
    FROM   country_totals
    ORDER BY titles DESC
    LIMIT  30;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        WITH country_totals AS (
            SELECT   first_country,
                     COUNT(*) AS titles
            FROM     netflix
            WHERE    first_country IS NOT NULL AND first_country <> ''
            GROUP BY first_country
        )
        SELECT first_country,
               titles,
               ROW_NUMBER() OVER (ORDER BY titles DESC)           AS country_rank,
               NTILE(4)     OVER (ORDER BY titles DESC)           AS quartile,
               CASE NTILE(4) OVER (ORDER BY titles DESC)
                   WHEN 1 THEN 'Top 25%'
                   WHEN 2 THEN 'Upper-Mid'
                   WHEN 3 THEN 'Lower-Mid'
                   ELSE        'Bottom 25%'
               END                                                AS tier
        FROM   country_totals
        ORDER BY titles DESC
        LIMIT  30
        """
    ).df()
    mo.ui.table(_df, label="Q18 · Country rank with quartile tier")
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q19 · Year-over-year growth rate in content additions

    **Concept:** `LAG()` window function to access the previous row's value,
    then arithmetic to compute percentage change.

    **Why it matters:** `LAG` is the standard SQL way to compute period-over-period
    growth without a self-join. The result shows Netflix's content investment
    ramp-up and plateau.

    ```sql
    WITH yearly AS (
        SELECT   year_added,
                 COUNT(*) AS titles
        FROM     netflix
        WHERE    year_added IS NOT NULL
        GROUP BY year_added
    ),
    with_lag AS (
        SELECT year_added,
               titles,
               LAG(titles) OVER (ORDER BY year_added) AS prev_year_titles
        FROM yearly
    )
    SELECT year_added,
           titles,
           prev_year_titles,
           ROUND(
               (titles - prev_year_titles) * 100.0
               / NULLIF(prev_year_titles, 0),
           1) AS yoy_growth_pct
    FROM   with_lag
    ORDER BY year_added;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        WITH yearly AS (
            SELECT   year_added,
                     COUNT(*) AS titles
            FROM     netflix
            WHERE    year_added IS NOT NULL
            GROUP BY year_added
        ),
        with_lag AS (
            SELECT year_added,
                   titles,
                   LAG(titles) OVER (ORDER BY year_added) AS prev_year_titles
            FROM yearly
        )
        SELECT year_added,
               titles,
               prev_year_titles,
               ROUND(
                   (titles - prev_year_titles) * 100.0
                   / NULLIF(prev_year_titles, 0),
               1) AS yoy_growth_pct
        FROM   with_lag
        ORDER BY year_added
        """
    ).df()
    mo.ui.table(_df, label="Q19 · Year-over-year content growth")
    return


@app.cell
def _(con, mo):
    import plots_02 as _p
    _w = _p.chart_q19(con, mo)
    _w
    return


@app.cell
def _(mo):
    mo.md("""
    ### Q20 · Most productive director-country pairs, ranked within each country

    **Concept:** Multi-level CTE → `DENSE_RANK() OVER (PARTITION BY country ORDER BY titles DESC)`
    Shows the top director for each of the top 10 producing countries.

    **Why it matters:** Combines partitioned ranking with a CTE pipeline.
    This is the "Top-N per group" pattern applied to a two-dimensional breakdown —
    arguably the most common real-world window function use case.

    ```sql
    WITH dir_country AS (
        SELECT   first_country,
                 director,
                 COUNT(*) AS titles
        FROM     netflix
        WHERE    director    IS NOT NULL AND director    <> ''
          AND    first_country IS NOT NULL AND first_country <> ''
        GROUP BY first_country, director
    ),
    top_countries AS (
        SELECT first_country
        FROM   netflix
        WHERE  first_country IS NOT NULL AND first_country <> ''
        GROUP BY first_country
        ORDER BY COUNT(*) DESC
        LIMIT  10
    ),
    ranked AS (
        SELECT dc.first_country,
               dc.director,
               dc.titles,
               DENSE_RANK() OVER (
                   PARTITION BY dc.first_country
                   ORDER BY dc.titles DESC
               ) AS country_rank
        FROM   dir_country dc
        JOIN   top_countries tc USING (first_country)
    )
    SELECT first_country, director, titles, country_rank
    FROM   ranked
    WHERE  country_rank <= 3
    ORDER BY first_country, country_rank;
    ```
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute(
        """
        WITH dir_country AS (
            SELECT   first_country,
                     director,
                     COUNT(*) AS titles
            FROM     netflix
            WHERE    director     IS NOT NULL AND director     <> ''
              AND    first_country IS NOT NULL AND first_country <> ''
            GROUP BY first_country, director
        ),
        top_countries AS (
            SELECT first_country
            FROM   netflix
            WHERE  first_country IS NOT NULL AND first_country <> ''
            GROUP BY first_country
            ORDER BY COUNT(*) DESC
            LIMIT  10
        ),
        ranked AS (
            SELECT dc.first_country,
                   dc.director,
                   dc.titles,
                   DENSE_RANK() OVER (
                       PARTITION BY dc.first_country
                       ORDER BY dc.titles DESC
                   ) AS country_rank
            FROM   dir_country dc
            JOIN   top_countries tc USING (first_country)
        )
        SELECT first_country, director, titles, country_rank
        FROM   ranked
        WHERE  country_rank <= 3
        ORDER BY first_country, country_rank
        """
    ).df()
    mo.ui.table(_df, label="Q20 · Top 3 directors per top-10 country")
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Section 6 — SQL Concepts Reference

    | Concept | Query(ies) | Description |
    |---|---|---|
    | `SELECT / FROM / LIMIT` | Q1, Q4 | Basic retrieval |
    | `WHERE` filter | Q2, Q4, Q6 | Row-level filtering |
    | `GROUP BY` + `COUNT` | Q1–Q5 | Aggregation |
    | `ORDER BY … DESC` | Q2, Q6 | Sorting |
    | `HAVING` | Q9, Q10 | Post-aggregation filtering |
    | `CASE WHEN` in `SELECT` | Q5, Q9, Q14, Q18 | Conditional expressions |
    | `ROUND`, `AVG`, `MIN`, `MAX` | Q10, Q13 | Numeric aggregates |
    | `UNNEST(STRING_SPLIT())` | Q11, Q15, Q16 | Exploding multi-value strings |
    | `WITH` CTE | Q16–Q20 | Readable multi-step queries |
    | `RANK() / DENSE_RANK() OVER (PARTITION BY …)` | Q16, Q20 | Top-N per group |
    | `SUM() OVER (ORDER BY …)` | Q17 | Cumulative / running total |
    | `NTILE(n) OVER (…)` | Q18 | Percentile bucketing |
    | `LAG() OVER (ORDER BY …)` | Q19 | Period-over-period comparison |
    | `ROW_NUMBER() OVER (…)` | Q18 | Absolute sequential rank |
    | `JOIN … USING` | Q20 | Joining two CTEs |
    | `NULLIF` | Q19 | Safe division (avoid divide-by-zero) |
    | `TRY_CAST`, `EXTRACT` | View | Type casting + date arithmetic |
    | `REGEXP_REPLACE` | View | String → integer extraction |

    ---
    **End of Notebook 2.**  All queries run against `netflix.duckdb`.
    """)
    return


if __name__ == "__main__":
    app.run()
