import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", app_title="Top 500 Movies — DuckDB + SQL")


@app.cell
def _(mo):
    mo.md(r"""
    # 🎬 Top 500 Movies — a DuckDB + SQL Data Story

    This Marimo notebook loads `top_500_movies_ranked.csv` into a persistent
    **DuckDB** database (`top_500_movies.duckdb`), reshapes it with a handful
    of **derived columns**, and then tells a story about the data through
    **20 progressively harder SQL queries**.

    **How the notebook is organised** — every analytical step is three cells:

    1. **A short briefing** (markdown) — *what* we are asking and *why*, plus the
       SQL concept it teaches.
    2. **A pure-SQL cell** — the query itself, formatted for readability. Marimo
       runs it against DuckDB and renders the result table automatically.
    3. **A chart** — drawn by helper functions in `util_plot.py` so the notebook
       stays focused on SQL, not on matplotlib boilerplate.

    The queries are grouped into four tiers — *Simple*, *Simple+*,
    *Intermediate*, and *Intermediate+* — ending with an **interactive explorer**
    that shows off reactive, notebook-native SQL.

    > **Naming convention:** every column uses **lower_snake_case**
    > (`custom_score`, `imdb_votes`, `primary_genre`, …) — the classic SQL style.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import duckdb
    import pandas as pd
    import util_plot as up

    return duckdb, mo, up


@app.cell
def _(duckdb, mo):
    # Resolve paths relative to the notebook so it runs from anywhere.
    import pathlib

    try:
        _base = mo.notebook_dir()
    except Exception:
        _base = None
    if _base is None:
        _base = pathlib.Path(".").resolve()

    CSV_PATH = str(_base / "top_500_movies_ranked.csv")
    DB_PATH = str(_base / "top_500_movies.duckdb")

    # Persistent on-disk DuckDB database.
    conn = duckdb.connect(DB_PATH)

    # ----------------------------------------------------------------------- #
    #  One SQL statement does the whole ETL:
    #    * renames every CSV column to lower_snake_case
    #    * adds derived columns (decade, era, primary_genre, award counts, ...)
    #  Written as three CTEs so each stage is easy to read.
    # ----------------------------------------------------------------------- #
    BUILD_SQL = rf"""
    CREATE OR REPLACE TABLE movies AS
    WITH raw AS (
        SELECT *
        FROM read_csv_auto('{CSV_PATH}', header = true, sample_size = -1)
    ),
    renamed AS (
        SELECT
            "Rank"             AS rank,
            "Title"            AS title,
            "Year"             AS year,
            "Genre"            AS genre,
            "Director"         AS director,
            "Cast"             AS "cast",
            "Language"         AS language,
            "Plot"             AS plot,
            "Awards"           AS awards,
            "Production"       AS production,
            "Flickmetrix_Score" AS flickmetrix_score,
            "IMDb_10"          AS imdb_10,
            "IMDb_100"         AS imdb_100,
            "IMDb_Votes"       AS imdb_votes,
            "Metacritic"       AS metacritic,
            "Critic_Rating_RT" AS critic_rating_rt,
            "Critic_Reviews"   AS critic_reviews,
            "Audience_Rating"  AS audience_rating,
            "Audience_Reviews" AS audience_reviews,
            "Letterboxd"       AS letterboxd,
            "Letterboxd_Votes" AS letterboxd_votes,
            "Google_Score"     AS google_score,
            "Streaming_On"     AS streaming_on,
            "RT_URL"           AS rt_url,
            "imdbID"           AS imdb_id,
            "Custom_Score"     AS custom_score
        FROM raw
    ),
    derived AS (
        SELECT
            *,
            (year / 10) * 10                                       AS decade,
            CASE
                WHEN year < 1970 THEN 'Classic (pre-1970)'
                WHEN year < 2000 THEN 'Modern (1970-1999)'
                ELSE 'Contemporary (2000+)'
            END                                                    AS era,
            trim(split_part(genre, ',', 1))                        AS primary_genre,
            (length(genre) - length(replace(genre, ',', '')) + 1)  AS num_genres,
            (language = 'en')                                      AS is_english,
            CASE
                WHEN "cast" IS NULL OR "cast" = '' THEN 0
                ELSE length("cast") - length(replace("cast", ',', '')) + 1
            END                                                    AS num_cast_members,
            CASE
                WHEN streaming_on IS NULL OR streaming_on = '' THEN 0
                ELSE length(streaming_on) - length(replace(streaming_on, ',', '')) + 1
            END                                                    AS num_streaming_platforms,
            COALESCE(TRY_CAST(regexp_extract(awards, 'Won (\d+) Oscar', 1)            AS INTEGER), 0) AS oscar_wins,
            COALESCE(TRY_CAST(regexp_extract(awards, 'Nominated for (\d+) Oscar', 1)  AS INTEGER), 0) AS oscar_nominations,
            COALESCE(TRY_CAST(regexp_extract(awards, '(\d+) wins?', 1)                AS INTEGER), 0) AS other_wins,
            COALESCE(TRY_CAST(regexp_extract(awards, '(\d+) nominations?', 1)         AS INTEGER), 0) AS other_nominations
        FROM renamed
    )
    SELECT
        *,
        (oscar_wins + other_wins)               AS total_wins,
        (oscar_nominations + other_nominations) AS total_nominations
    FROM derived;
    """

    conn.execute(BUILD_SQL)
    _n = conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
    _c = conn.execute("SELECT COUNT(*) FROM pragma_table_info('movies')").fetchone()[0]

    mo.md(
        f"""
        ✅ **Database ready** — `top_500_movies.duckdb`

        Loaded **{_n} movies** into table `movies` with **{_c} columns**
        ({26} renamed from the CSV + {_c - 26} derived).
        """
    )
    return (conn,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 🧱 Schema & derived columns

    Below is the full table schema. Beyond the 26 renamed source columns we
    engineered several **derived columns** to make the questions ahead easier:

    | Derived column | How it is built | Used for |
    |---|---|---|
    | `decade` | `(year / 10) * 10` | grouping films by era |
    | `era` | `CASE` on `year` | Classic / Modern / Contemporary labels |
    | `primary_genre` | first item of the `genre` list | one genre per film |
    | `num_genres` | comma count in `genre` + 1 | genre breadth |
    | `is_english` | `language = 'en'` | English vs. world cinema |
    | `num_cast_members` | comma count in `cast` + 1 | cast size |
    | `num_streaming_platforms` | comma count in `streaming_on` + 1 | availability |
    | `oscar_wins` / `oscar_nominations` | regex over `awards` | Academy recognition |
    | `other_wins` / `other_nominations` | regex over `awards` | festival/other recognition |
    | `total_wins` / `total_nominations` | Oscar + other | overall acclaim |
    """)
    return


@app.cell
def _(conn, mo):
    schema = mo.sql(
        f"""
        SELECT
            column_name  AS column,
            data_type    AS type
        FROM information_schema.columns
        WHERE table_name = 'movies'
        ORDER BY ordinal_position
        """,
        engine=conn
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    # 🟢 Tier 1 — Simple queries
    Single-table reads: `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`. The foundation
    of every SQL question — pick columns, filter rows, sort, and cap the result.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 1. The ten best films overall
    **What & why:** The dataset ships with a blended `custom_score` (0–100) that
    fuses critic and audience signals. The simplest possible question — *which
    movies are rated highest?* — is just a sort on that column capped at ten.
    **Concept:** `ORDER BY ... DESC` + `LIMIT`.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q1 = mo.sql(
        f"""
        SELECT rank, title, year, custom_score
        FROM movies
        ORDER BY custom_score DESC
        LIMIT 10
        """,
        engine=conn
    )
    return (q1,)


@app.cell
def _(q1, up):
    up.barh_top(
        q1, label="title", value="custom_score",
        title="Top 10 movies by Custom Score", xlabel="Custom Score (0–100)",
        value_fmt="{:.2f}",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 2. Highest IMDb ratings
    **What & why:** A different lens on "best" — pure IMDb user score
    (`imdb_10`, the familiar 0–10 scale). When two films tie, we break the tie
    with the number of votes so well-established classics rank ahead.
    **Concept:** multi-key `ORDER BY` (primary + tie-breaker).
    """)
    return


@app.cell
def _(conn, mo, movies):
    q2 = mo.sql(
        f"""
        SELECT rank, title, year, imdb_10, imdb_votes
        FROM movies
        ORDER BY imdb_10 DESC, imdb_votes DESC
        LIMIT 10
        """,
        engine=conn
    )
    return (q2,)


@app.cell
def _(q2, up):
    up.barh_top(
        q2, label="title", value="imdb_10",
        title="Top 10 movies by IMDb rating", xlabel="IMDb rating (0–10)",
        value_fmt="{:.1f}", color="#55A868",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 3. Crowd-pleasers (audience favourites)
    **What & why:** Critics and crowds don't always agree. Here we rank by
    Rotten Tomatoes `audience_rating`, filtering out films that have no audience
    score recorded so the ranking is meaningful.
    **Concept:** `WHERE ... IS NOT NULL` to exclude missing data before sorting.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q3 = mo.sql(
        f"""
        SELECT rank, title, year, audience_rating
        FROM movies
        WHERE audience_rating IS NOT NULL
        ORDER BY audience_rating DESC
        LIMIT 10
        """,
        engine=conn
    )
    return (q3,)


@app.cell
def _(q3, up):
    up.barh_top(
        q3, label="title", value="audience_rating",
        title="Top 10 audience-rated movies", xlabel="Audience rating (%)",
        value_fmt="{:.0f}", color="#DD8452",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 4. The most-voted films on IMDb
    **What & why:** Ratings show *how* loved a film is; vote counts show *how
    many* people weighed in — a proxy for cultural reach. These are the
    blockbusters everyone has seen.
    **Concept:** sorting on a large integer measure; reading values at scale.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q4 = mo.sql(
        f"""
        SELECT rank, title, year, imdb_votes
        FROM movies
        ORDER BY imdb_votes DESC
        LIMIT 12
        """,
        engine=conn
    )
    return (q4,)


@app.cell
def _(q4, up):
    up.barh_top(
        q4, label="title", value="imdb_votes",
        title="Most-voted films on IMDb", xlabel="IMDb votes",
        value_fmt="{:,.0f}", color="#8172B3",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 5. The best of the recent era
    **What & why:** Is great cinema still being made? We restrict to films from
    **2018 onward** and take the ten best by `custom_score`.
    **Concept:** combining a `WHERE` range filter with `ORDER BY` + `LIMIT`.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q5 = mo.sql(
        f"""
        SELECT rank, title, year, custom_score
        FROM movies
        WHERE year >= 2018
        ORDER BY custom_score DESC
        LIMIT 10
        """,
        engine=conn
    )
    return (q5,)


@app.cell
def _(q5, up):
    up.barh_top(
        q5, label="title", value="custom_score",
        title="Best films since 2018", xlabel="Custom Score (0–100)",
        value_fmt="{:.2f}", color="#C44E52",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    # 🔵 Tier 2 — Simple+ queries
    Now we **summarise** rather than list: `GROUP BY` with aggregate functions
    (`COUNT`, `AVG`), `CASE` expressions, and derived columns.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 6. How many films per decade?
    **What & why:** The list leans heavily toward recent decades. Counting films
    per `decade` reveals that recency bias at a glance.
    **Concept:** `GROUP BY` a derived column + `COUNT(*)`.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q6 = mo.sql(
        f"""
        SELECT decade, COUNT(*) AS movie_count
        FROM movies
        GROUP BY decade
        ORDER BY decade
        """,
        engine=conn
    )
    return (q6,)


@app.cell
def _(q6, up):
    up.bar(
        q6, x="decade", y="movie_count",
        title="Films per decade", xlabel="Decade", ylabel="Number of films",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 7. Which languages dominate the list?
    **What & why:** Counting films per `language` shows how English-language
    cinema compares with world cinema in this ranking.
    **Concept:** `GROUP BY` + `COUNT`, then `ORDER BY` the aggregate and `LIMIT`.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q7 = mo.sql(
        f"""
        SELECT language, COUNT(*) AS movie_count
        FROM movies
        GROUP BY language
        ORDER BY movie_count DESC
        LIMIT 10
        """,
        engine=conn
    )
    return (q7,)


@app.cell
def _(q7, up):
    up.bar(
        q7, x="language", y="movie_count",
        title="Films per language (top 10)", xlabel="Language code",
        ylabel="Number of films", color="#64B5CD",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 8. The most common primary genres
    **What & why:** Each film lists several genres; our derived `primary_genre`
    keeps only the first. Counting it tells us what kind of film dominates the
    canon (spoiler: Drama).
    **Concept:** aggregating over an engineered column.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q8 = mo.sql(
        f"""
        SELECT primary_genre, COUNT(*) AS movie_count
        FROM movies
        GROUP BY primary_genre
        ORDER BY movie_count DESC
        LIMIT 10
        """,
        engine=conn
    )
    return (q8,)


@app.cell
def _(q8, up):
    up.bar(
        q8, x="primary_genre", y="movie_count",
        title="Most common primary genres", xlabel="Primary genre",
        ylabel="Number of films", rotate=35, color="#937860",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 9. English vs. world cinema — does score differ?
    **What & why:** Using the boolean `is_english`, we split the list in two and
    compare both **how many** films each side has and their **average score**.
    **Concept:** `CASE` to relabel a boolean, plus `COUNT` and `AVG` together.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q9 = mo.sql(
        f"""
        SELECT
            CASE WHEN is_english THEN 'English' ELSE 'Non-English' END AS language_group,
            COUNT(*)                       AS films,
            ROUND(AVG(custom_score), 2)    AS avg_score,
            ROUND(AVG(imdb_10), 2)         AS avg_imdb
        FROM movies
        GROUP BY is_english
        ORDER BY films DESC
        """,
        engine=conn
    )
    return (q9,)


@app.cell
def _(q9, up):
    up.bar(
        q9, x="language_group", y="avg_score",
        title="Average Custom Score: English vs. world cinema",
        xlabel="", ylabel="Average Custom Score", value_fmt="{:.2f}",
        color="#4C72B0",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 10. Have IMDb ratings drifted over time?
    **What & why:** Averaging `imdb_10` within each decade shows whether older or
    newer films enjoy higher user scores — a gentle look at nostalgia vs. recency.
    **Concept:** `AVG` per group, viewed as a trend over an ordered dimension.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q10 = mo.sql(
        f"""
        SELECT decade, ROUND(AVG(imdb_10), 2) AS avg_imdb, COUNT(*) AS films
        FROM movies
        GROUP BY decade
        ORDER BY decade
        """,
        engine=conn
    )
    return (q10,)


@app.cell
def _(q10, up):
    up.line(
        q10, x="decade", ys="avg_imdb",
        title="Average IMDb rating by decade", xlabel="Decade",
        ylabel="Average IMDb rating",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    # 🟣 Tier 3 — Intermediate queries
    Joins and richer aggregation: exploding list columns with `UNNEST`, joining
    CTEs together, and filtering groups with `HAVING`.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 11. Genre popularity — counting *every* genre tag
    **What & why:** A film tagged "Drama, Crime" should count toward both. We
    `UNNEST` the comma-split genre list into one row per tag (a cross join), then
    aggregate — counting films and averaging their score per genre.
    **Concept:** `string_split` + `UNNEST` (a lateral/cross join) then `GROUP BY`.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q11 = mo.sql(
        f"""
        WITH exploded AS (
            SELECT
                m.rank,
                m.custom_score,
                trim(tag) AS genre_tag
            FROM movies AS m,
                 UNNEST(string_split(m.genre, ',')) AS t(tag)
        )
        SELECT
            genre_tag,
            COUNT(*)                     AS films,
            ROUND(AVG(custom_score), 2)  AS avg_score
        FROM exploded
        GROUP BY genre_tag
        ORDER BY films DESC
        LIMIT 12
        """,
        engine=conn
    )
    return (q11,)


@app.cell
def _(q11, up):
    up.bar(
        q11, x="genre_tag", y="films",
        title="Films per genre tag (every genre counted)",
        xlabel="Genre", ylabel="Number of films", rotate=40, color="#8172B3",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 12. Director leaderboard
    **What & why:** Which directors place the most films *and* keep quality high?
    We aggregate by `director`, keep only those with **3+ films** via `HAVING`,
    and rank by average score.
    **Concept:** `GROUP BY` + `HAVING` (filtering on an aggregate).
    """)
    return


@app.cell
def _(conn, mo, movies):
    q12 = mo.sql(
        f"""
        SELECT
            director,
            COUNT(*)                     AS films,
            ROUND(AVG(custom_score), 2)  AS avg_score
        FROM movies
        GROUP BY director
        HAVING COUNT(*) >= 3
        ORDER BY avg_score DESC, films DESC
        LIMIT 15
        """,
        engine=conn
    )
    return (q12,)


@app.cell
def _(q12, up):
    up.barh_top(
        q12, label="director", value="avg_score",
        title="Top directors (3+ films) by average score",
        xlabel="Average Custom Score", value_fmt="{:.1f}", color="#55A868",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 13. Critics vs. audiences, decade by decade
    **What & why:** Do professional critics and ordinary viewers move together
    over time? We build two per-decade averages — one for `metacritic`, one for
    `audience_rating` — and **`JOIN`** them on `decade` to compare side by side.
    **Concept:** joining two aggregated CTEs on a shared key.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q13 = mo.sql(
        f"""
        WITH critics AS (
            SELECT decade, ROUND(AVG(metacritic), 1) AS avg_metacritic
            FROM movies
            WHERE metacritic IS NOT NULL
            GROUP BY decade
        ),
        audience AS (
            SELECT decade, ROUND(AVG(audience_rating), 1) AS avg_audience
            FROM movies
            WHERE audience_rating IS NOT NULL
            GROUP BY decade
        )
        SELECT c.decade, c.avg_metacritic, a.avg_audience
        FROM critics AS c
        JOIN audience AS a ON c.decade = a.decade
        ORDER BY c.decade
        """,
        engine=conn
    )
    return (q13,)


@app.cell
def _(q13, up):
    up.line(
        q13, x="decade", ys=["avg_metacritic", "avg_audience"],
        labels=["Critics (Metacritic)", "Audience (RT)"],
        title="Critics vs. audiences by decade", xlabel="Decade",
        ylabel="Average rating (0–100)",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 14. Which languages punch above their weight?
    **What & why:** For every language with **at least 3 films**, we compute the
    average IMDb and Custom scores. Small but mighty national cinemas often top
    the table.
    **Concept:** `GROUP BY` + `HAVING` + multiple aggregates side by side.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q14 = mo.sql(
        f"""
        SELECT
            language,
            COUNT(*)                     AS films,
            ROUND(AVG(imdb_10), 2)       AS avg_imdb,
            ROUND(AVG(custom_score), 2)  AS avg_custom
        FROM movies
        GROUP BY language
        HAVING COUNT(*) >= 3
        ORDER BY avg_custom DESC
        """,
        engine=conn
    )
    return (q14,)


@app.cell
def _(q14, up):
    up.barh_top(
        q14, label="language", value="avg_custom",
        title="Average Custom Score by language (3+ films)",
        xlabel="Average Custom Score", value_fmt="{:.1f}", color="#DA8BC3",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 15. Which genres rack up the most awards?
    **What & why:** Using the award counts we parsed from the `awards` text, we
    compare average **wins** and **nominations** per `primary_genre` (genres with
    5+ films). Prestige drama vs. crowd-pleasing comedy shows up clearly.
    **Concept:** aggregating engineered numeric columns across groups.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q15 = mo.sql(
        f"""
        SELECT
            primary_genre,
            COUNT(*)                         AS films,
            ROUND(AVG(total_wins), 1)        AS avg_wins,
            ROUND(AVG(total_nominations), 1) AS avg_nominations
        FROM movies
        GROUP BY primary_genre
        HAVING COUNT(*) >= 5
        ORDER BY avg_wins DESC
        """,
        engine=conn
    )
    return (q15,)


@app.cell
def _(q15, up):
    up.grouped_bar(
        q15, x="primary_genre", ys=["avg_wins", "avg_nominations"],
        labels=["Avg wins", "Avg nominations"],
        title="Average awards by primary genre (5+ films)",
        xlabel="Primary genre", ylabel="Average count",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    # 🔴 Tier 4 — Intermediate+ queries
    The good stuff: **window functions** (`ROW_NUMBER`, `RANK`, `NTILE`),
    **Top-N-per-group**, and **`WITH` subqueries** that compare each row against
    a computed benchmark.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 16. The top 3 films of every decade
    **What & why:** A classic **Top-N-per-group** problem. `ROW_NUMBER()` numbers
    films *within* each decade by descending score; we then keep only ranks 1–3.
    **Concept:** `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` + outer filter.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q16 = mo.sql(
        f"""
        WITH ranked AS (
            SELECT
                decade,
                title,
                custom_score,
                ROW_NUMBER() OVER (
                    PARTITION BY decade
                    ORDER BY custom_score DESC
                ) AS rnk
            FROM movies
        )
        SELECT decade, rnk, title, custom_score
        FROM ranked
        WHERE rnk <= 3
        ORDER BY decade, rnk
        """,
        engine=conn
    )
    return (q16,)


@app.cell
def _(q16, up):
    # Reshape long -> wide (decade x rank) purely for the grouped-bar chart.
    _df = q16.to_pandas() if hasattr(q16, "to_pandas") else q16.copy()
    _wide = _df.pivot(index="decade", columns="rnk", values="custom_score").reset_index()
    _wide.columns = ["decade"] + [f"top{int(c)}" for c in _wide.columns[1:]]
    up.grouped_bar(
        _wide, x="decade", ys=["top1", "top2", "top3"],
        labels=["#1", "#2", "#3"],
        title="Top 3 Custom Scores in each decade",
        xlabel="Decade", ylabel="Custom Score",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 17. Ranking directors with `RANK()`
    **What & why:** We reuse the "3+ films" director pool from a `WITH` clause,
    then apply `RANK()` to assign a competition rank by average score (ties share
    a rank). This separates *computing* the metric from *ranking* it.
    **Concept:** a `WITH` subquery feeding a `RANK()` window function.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q17 = mo.sql(
        f"""
        WITH director_stats AS (
            SELECT
                director,
                COUNT(*)                     AS films,
                ROUND(AVG(custom_score), 2)  AS avg_score
            FROM movies
            GROUP BY director
            HAVING COUNT(*) >= 3
        )
        SELECT
            RANK() OVER (ORDER BY avg_score DESC) AS score_rank,
            director,
            films,
            avg_score
        FROM director_stats
        ORDER BY score_rank
        LIMIT 12
        """,
        engine=conn
    )
    return (q17,)


@app.cell
def _(q17, up):
    up.barh_top(
        q17, label="director", value="avg_score",
        title="Director ranking by average score (RANK)",
        xlabel="Average Custom Score", value_fmt="{:.1f}", color="#CCB974",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 18. The single best film in each genre
    **What & why:** Another partitioned ranking — this time we keep only the
    **#1 film per `primary_genre`**, giving a "genre champions" board.
    **Concept:** `ROW_NUMBER()` partitioned by genre, keeping `rn = 1`.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q18 = mo.sql(
        f"""
        WITH ranked AS (
            SELECT
                primary_genre,
                title,
                year,
                custom_score,
                ROW_NUMBER() OVER (
                    PARTITION BY primary_genre
                    ORDER BY custom_score DESC
                ) AS rn
            FROM movies
        )
        SELECT primary_genre, title, year, custom_score
        FROM ranked
        WHERE rn = 1
        ORDER BY custom_score DESC
        """,
        engine=conn
    )
    return (q18,)


@app.cell
def _(q18, up):
    up.barh_top(
        q18, label="primary_genre", value="custom_score",
        title="Best film in each primary genre",
        xlabel="Custom Score", value_fmt="{:.1f}", color="#C44E52",
        max_label_len=18,
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 19. Films that beat their decade's average
    **What & why:** A row-vs-benchmark comparison. We compute each `decade`'s
    average score in a `WITH` clause, `JOIN` it back to every film, and surface
    the films that exceed their own decade's average by the widest margin.
    **Concept:** subquery benchmark + `JOIN` + derived comparison column.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q19 = mo.sql(
        f"""
        WITH decade_avg AS (
            SELECT decade, AVG(custom_score) AS decade_mean
            FROM movies
            GROUP BY decade
        )
        SELECT
            m.title,
            m.year,
            m.custom_score,
            ROUND(d.decade_mean, 2)                  AS decade_avg,
            ROUND(m.custom_score - d.decade_mean, 2) AS above_by
        FROM movies AS m
        JOIN decade_avg AS d ON m.decade = d.decade
        WHERE m.custom_score > d.decade_mean
        ORDER BY above_by DESC
        LIMIT 12
        """,
        engine=conn
    )
    return (q19,)


@app.cell
def _(q19, up):
    up.barh_top(
        q19, label="title", value="above_by",
        title="Films most above their decade's average",
        xlabel="Points above decade average", value_fmt="{:.1f}", color="#4C72B0",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 20. Splitting the canon into quartiles with `NTILE`
    **What & why:** `NTILE(4)` slices the films into four equal-sized score bands
    (top 25%, next 25%, …). We then describe each quartile — its size and score
    range — to see how tightly packed the very best films are.
    **Concept:** the `NTILE` window function for bucketing/percentile bands.
    """)
    return


@app.cell
def _(conn, mo, movies):
    q20 = mo.sql(
        f"""
        WITH quartiles AS (
            SELECT
                title,
                custom_score,
                NTILE(4) OVER (ORDER BY custom_score DESC) AS quartile
            FROM movies
        )
        SELECT
            quartile,
            COUNT(*)                     AS films,
            ROUND(MIN(custom_score), 2)  AS min_score,
            ROUND(MAX(custom_score), 2)  AS max_score,
            ROUND(AVG(custom_score), 2)  AS avg_score
        FROM quartiles
        GROUP BY quartile
        ORDER BY quartile
        """,
        engine=conn
    )
    return (q20,)


@app.cell
def _(q20, up):
    up.bar(
        q20, x="quartile", y="avg_score",
        title="Average score by Custom-Score quartile",
        xlabel="Quartile (1 = top 25%)", ylabel="Average Custom Score",
        value_fmt="{:.1f}", color="#937860",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    # ✨ Interactive explorer — reactive SQL
    This is the concept that's *proper to notebooks*: SQL parameterised by UI.
    Pick a **decade** and a **minimum score**, and the query below re-runs
    automatically — Marimo tracks the dependency between the widgets and the SQL
    cell and keeps everything in sync.
    """)
    return


@app.cell
def _(conn, mo):
    decades = [r[0] for r in conn.execute(
        "SELECT DISTINCT decade FROM movies ORDER BY decade"
    ).fetchall()]

    decade_dd = mo.ui.dropdown(
        options={str(d): d for d in decades},
        value=str(decades[-2]),
        label="Decade",
    )
    min_score = mo.ui.slider(
        start=77, stop=94, step=1, value=85, label="Minimum Custom Score",
    )
    mo.hstack([decade_dd, min_score], justify="start", gap=2)
    return decade_dd, min_score


@app.cell
def _(conn, decade_dd, min_score, mo, movies):
    explorer = mo.sql(
        f"""
        SELECT rank, title, year, primary_genre, custom_score, imdb_10
        FROM movies
        WHERE decade = {decade_dd.value}
          AND custom_score >= {min_score.value}
        ORDER BY custom_score DESC
        """,
        engine=conn
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 🎓 Key SQL concepts covered

    | Tier | Concepts |
    |---|---|
    | **Simple** | `SELECT`, `WHERE`, `IS NOT NULL`, multi-key `ORDER BY`, `LIMIT` |
    | **Simple+** | `GROUP BY`, `COUNT` / `AVG`, `CASE`, derived columns |
    | **Intermediate** | `string_split` + `UNNEST`, `JOIN` of CTEs, `HAVING` |
    | **Intermediate+** | `ROW_NUMBER`, `RANK`, `NTILE`, Top-N-per-group, `WITH` benchmarks |
    | **Notebook-native** | reactive SQL driven by `mo.ui` widgets |

    The full pipeline — CSV → renamed & enriched DuckDB table → 20 queries →
    charts — lives in `top_500_movies.duckdb`, ready for your own questions.
    Open a fresh SQL cell and try one!
    """)
    return


if __name__ == "__main__":
    app.run()
