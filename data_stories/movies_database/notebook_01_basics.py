import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import plot_util
    from pathlib import Path

    try:
        _here = Path(__file__).resolve().parent
    except NameError:
        _here = Path.cwd()

    _candidates = [
        Path.cwd() / "movies_db.duckdb",
        _here / "movies_db.duckdb",
        _here.parent / "movies_db.duckdb",
    ]
    _db = next((str(p) for p in _candidates if p.exists()), "movies_db.duckdb")
    conn = duckdb.connect(_db, read_only=True)
    return conn, mo, plot_util


@app.cell
def _(mo):
    mo.md(r"""
    # Movies Database - Notebook 1: SQL Basics

    A guided tour of the **movies** DuckDB database using *pure SQL* cells in
    Marimo.  Each query below has four parts: a plain-English explanation of
    **what** we are doing and **why**, the **SQL** itself, the **result table**,
    and - where it helps - a **chart**.

    The database has 17 tables.  The central table is `movie` (4,803 films); the
    people, genres, keywords, companies, languages and countries each live in
    their own table and are linked to movies through small *bridge* tables
    (`movie_cast`, `movie_genres`, ...).

    **This notebook covers:** 5 simple queries, 5 simple+ queries, and 5
    intermediate queries (joins & aggregations).

    > Build the database first with `./create_duckdb.sh`, then run this notebook with
    > `marimo edit notebook_01_basics.py` (or `marimo run ...`).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## A. Five simple queries
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 1. How many movies are in the database?

    **What we are doing.** The simplest possible question: a single-row count of the whole `movie` table. `COUNT(*)` counts every row, and we give the result a readable alias with `AS total_movies`.

    **Concept:** `SELECT`, `COUNT(*)`, column aliasing.
    """)
    return


@app.cell
def _(conn, mo, movie):
    q1_total_movies = mo.sql(
        f"""
        SELECT COUNT(*) AS total_movies
        FROM movie;
        """,
        engine=conn
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 2. The 10 highest-grossing movies

    **What we are doing.** We sort the table by `revenue` from highest to lowest and keep only the first ten rows. `WHERE revenue > 0` drops the many rows whose revenue is unknown (stored as 0).

    **Concept:** `WHERE`, `ORDER BY ... DESC`, `LIMIT`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    q2_top_revenue = mo.sql(
        f"""
        SELECT title, revenue
        FROM movie
        WHERE revenue > 0
        ORDER BY revenue DESC
        LIMIT 10;
        """,
        engine=conn
    )
    return (q2_top_revenue,)


@app.cell
def _(plot_util, q2_top_revenue):
    plot_util.barh(q2_top_revenue, cat='title', val='revenue', title='Top 10 highest-grossing movies', xlabel='Worldwide revenue (US$)')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 3. The 10 best-rated movies (with enough votes)

    **What we are doing.** We rank movies by `vote_average`, but only among films with at least 1,000 votes so that obscure titles with a single perfect score do not dominate. `ROUND(vote_average, 1)` tidies the rating to one decimal place.

    **Concept:** filtering on a threshold, `ROUND`, multi-key `ORDER BY`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    q3_top_rated = mo.sql(
        f"""
        SELECT title,
           ROUND(vote_average, 1) AS rating,
           vote_count
        FROM movie
        WHERE vote_count >= 1000
        ORDER BY vote_average DESC, vote_count DESC
        LIMIT 10;
        """,
        engine=conn
    )
    return (q3_top_rated,)


@app.cell
def _(plot_util, q3_top_rated):
    plot_util.barh(q3_top_rated, cat='title', val='rating', title='Top 10 best-rated movies (>= 1000 votes)', xlabel='Average rating (0-10)')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 4. How many movies per release status?

    **What we are doing.** Our first aggregation. `GROUP BY movie_status` collapses the table into one row per distinct status (Released, Rumored, Post Production, ...) and `COUNT(*)` tells us how many movies fall in each bucket.

    **Concept:** `GROUP BY` with `COUNT(*)`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    q4_status_counts = mo.sql(
        f"""
        SELECT movie_status,
           COUNT(*) AS n
        FROM movie
        GROUP BY movie_status
        ORDER BY n DESC;
        """,
        engine=conn
    )
    return (q4_status_counts,)


@app.cell
def _(plot_util, q4_status_counts):
    plot_util.bar(q4_status_counts, cat='movie_status', val='n', title='Movies by release status', ylabel='Number of movies')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 5. The 10 longest movies by runtime

    **What we are doing.** A straight sort on `runtime` (minutes), keeping the ten longest. `WHERE runtime > 0` removes rows with a missing runtime.

    **Concept:** `ORDER BY ... DESC` on a numeric column, `LIMIT`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    q5_longest = mo.sql(
        f"""
        SELECT title, runtime
        FROM movie
        WHERE runtime > 0
        ORDER BY runtime DESC
        LIMIT 10;
        """,
        engine=conn
    )
    return (q5_longest,)


@app.cell
def _(plot_util, q5_longest):
    plot_util.barh(q5_longest, cat='title', val='runtime', title='Top 10 longest movies', xlabel='Runtime (minutes)')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## B. Five simple+ queries
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 6. Every movie with "dark" in the title

    **What we are doing.** Pattern matching with `LIKE`. We lower-case the title first so the search is case-insensitive, and `'%dark%'` matches the word anywhere in the title (the `%` are wildcards).

    **Concept:** `LOWER`, `LIKE`, wildcards.
    """)
    return


@app.cell
def _(conn, mo, movie):
    q6_dark_titles = mo.sql(
        f"""
        SELECT title,
           ROUND(vote_average, 1) AS rating
        FROM movie
        WHERE LOWER(title) LIKE '%dark%'
        ORDER BY vote_average DESC;
        """,
        engine=conn
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 7. Best-rated movies released in Q1 2005

    **What we are doing.** We restrict to a date window with `BETWEEN` (January-March 2005) and order by rating. DuckDB compares the `DATE` column directly against the date literals.

    **Concept:** `BETWEEN` on dates, date literals.
    """)
    return


@app.cell
def _(conn, mo, movie):
    q7_q1_2005 = mo.sql(
        f"""
        SELECT title,
           release_date,
           ROUND(vote_average, 1) AS rating
        FROM movie
        WHERE release_date BETWEEN DATE '2005-01-01' AND DATE '2005-03-31'
        ORDER BY vote_average DESC
        LIMIT 15;
        """,
        engine=conn
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 8. How many movies were released each year?

    **What we are doing.** We extract the calendar year from `release_date` with the `year()` function, group by it, and count. This is a classic time-series shape, perfect for a line chart.

    **Concept:** date-part extraction (`year`), `GROUP BY` a computed column, `IS NOT NULL`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    q8_per_year = mo.sql(
        f"""
        SELECT year(release_date) AS yr,
           COUNT(*) AS n
        FROM movie
        WHERE release_date IS NOT NULL
        GROUP BY yr
        ORDER BY yr;
        """,
        engine=conn
    )
    return (q8_per_year,)


@app.cell
def _(plot_util, q8_per_year):
    plot_util.line(q8_per_year, x='yr', y='n', title='Movies released per year', xlabel='Year', ylabel='Number of movies')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 9. Budget & revenue summary statistics

    **What we are doing.** Several aggregate functions in one query to profile the money columns: how many movies have a known budget, and their average/maximum budget, revenue and runtime. `ROUND(..., 0)` keeps the big dollar figures readable.

    **Concept:** multiple aggregates (`COUNT`, `AVG`, `MAX`) in a single `SELECT`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    q9_money_summary = mo.sql(
        f"""
        SELECT COUNT(*)                  AS movies_with_budget,
           ROUND(AVG(budget), 0)     AS avg_budget,
           MAX(budget)               AS max_budget,
           ROUND(AVG(revenue), 0)    AS avg_revenue,
           MAX(revenue)              AS max_revenue,
           ROUND(AVG(runtime), 1)    AS avg_runtime
        FROM movie
        WHERE budget > 0;
        """,
        engine=conn
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 10. Movies that are both great and widely voted

    **What we are doing.** Two conditions joined with `AND`: a high rating (>= 8.0) and broad audience engagement (>= 5,000 votes). This finds the crowd-certified classics.

    **Concept:** compound `WHERE` with `AND`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    q10_great_and_popular = mo.sql(
        f"""
        SELECT title,
           ROUND(vote_average, 1) AS rating,
           vote_count
        FROM movie
        WHERE vote_average >= 8.0
          AND vote_count  >= 5000
        ORDER BY vote_count DESC;
        """,
        engine=conn
    )
    return (q10_great_and_popular,)


@app.cell
def _(plot_util, q10_great_and_popular):
    plot_util.barh(q10_great_and_popular, cat='title', val='vote_count', title='Great + widely-voted movies', xlabel='Number of votes')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## C. Five intermediate queries (joins & aggregations)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 11. Top 10 Action movies by rating

    **What we are doing.** Our first JOIN. Genres live in a separate `genre` table linked to movies through the `movie_genres` bridge table. We chain two joins to filter to Action films, then rank by rating (with a vote threshold).

    **Concept:** many-to-many JOIN through a bridge table.
    """)
    return


@app.cell
def _(conn, genre, mo, movie, movie_genres):
    q11_action_top = mo.sql(
        f"""
        SELECT m.title,
           ROUND(m.vote_average, 1) AS rating
        FROM movie m
        JOIN movie_genres mg ON mg.movie_id = m.movie_id
        JOIN genre g         ON g.genre_id  = mg.genre_id
        WHERE g.genre_name = 'Action'
          AND m.vote_count >= 500
        ORDER BY m.vote_average DESC
        LIMIT 10;
        """,
        engine=conn
    )
    return (q11_action_top,)


@app.cell
def _(plot_util, q11_action_top):
    plot_util.barh(q11_action_top, cat='title', val='rating', title='Top 10 Action movies by rating', xlabel='Average rating (0-10)')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 12. How many movies in each genre?

    **What we are doing.** Join the bridge table to `genre`, group by genre name, and count. Because one movie can have several genres the totals add up to more than the number of movies.

    **Concept:** JOIN + `GROUP BY` + `COUNT`.
    """)
    return


@app.cell
def _(conn, genre, mo, movie_genres):
    q12_genre_counts = mo.sql(
        f"""
        SELECT g.genre_name,
           COUNT(*) AS n
        FROM movie_genres mg
        JOIN genre g ON g.genre_id = mg.genre_id
        GROUP BY g.genre_name
        ORDER BY n DESC;
        """,
        engine=conn
    )
    return (q12_genre_counts,)


@app.cell
def _(plot_util, q12_genre_counts):
    plot_util.bar(q12_genre_counts, cat='genre_name', val='n', title='Number of movies per genre', ylabel='Number of movies', rotate=45)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 13. The 15 most prolific actors

    **What we are doing.** Count how many cast credits each person has by joining `movie_cast` to `person`, grouping by the actor's name.

    **Concept:** JOIN + `GROUP BY` + `COUNT`, `LIMIT` for a Top-N list.
    """)
    return


@app.cell
def _(conn, mo, movie_cast, person):
    q13_busy_actors = mo.sql(
        f"""
        SELECT p.person_name AS actor,
           COUNT(*)      AS movie_count
        FROM movie_cast mc
        JOIN person p ON p.person_id = mc.person_id
        GROUP BY p.person_name
        ORDER BY movie_count DESC
        LIMIT 15;
        """,
        engine=conn
    )
    return (q13_busy_actors,)


@app.cell
def _(plot_util, q13_busy_actors):
    plot_util.barh(q13_busy_actors, cat='actor', val='movie_count', title='15 most prolific actors', xlabel='Number of cast credits')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 14. The cast of "Forrest Gump"

    **What we are doing.** A three-way JOIN movie -> movie_cast -> person to list who played whom, ordered by billing position (`cast_order`).

    **Concept:** multi-table JOIN, ordering by a sort key.
    """)
    return


@app.cell
def _(conn, mo, movie, movie_cast, person):
    q14_forrest_cast = mo.sql(
        f"""
        SELECT mc.cast_order,
           mc.character_name,
           p.person_name AS actor
        FROM movie m
        JOIN movie_cast mc ON mc.movie_id  = m.movie_id
        JOIN person p      ON p.person_id  = mc.person_id
        WHERE m.title = 'Forrest Gump'
        ORDER BY mc.cast_order
        LIMIT 20;
        """,
        engine=conn
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 15. Top 15 production countries

    **What we are doing.** Join the `production_country` bridge table to `country` and count movies per country to see where films are made.

    **Concept:** JOIN + `GROUP BY` + `COUNT` + `LIMIT`.
    """)
    return


@app.cell
def _(conn, country, mo, production_country):
    q15_country_counts = mo.sql(
        f"""
        SELECT c.country_name,
           COUNT(*) AS n
        FROM production_country pc
        JOIN country c ON c.country_id = pc.country_id
        GROUP BY c.country_name
        ORDER BY n DESC
        LIMIT 15;
        """,
        engine=conn
    )
    return (q15_country_counts,)


@app.cell
def _(plot_util, q15_country_counts):
    plot_util.barh(q15_country_counts, cat='country_name', val='n', title='Top 15 production countries', xlabel='Number of movies')
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
