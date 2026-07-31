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
    # Movies Database - Notebook 2: Intermediate -> Intermediate+

    This notebook builds on the basics and works up to **window functions**,
    **Common Table Expressions** (`WITH`), **ranking**, and **Top-N-per-group**
    queries - the tools you reach for in real analytical SQL.

    **This notebook covers:** 5 simple+ queries, 5 intermediate queries
    (joins & aggregations), and 10 intermediate+ queries (Top-N, ranking
    functions such as `ROW_NUMBER`/`RANK`/`LAG`, cumulative windows, and
    subqueries using `WITH`).

    > Build the database first with `./create_duckdb.sh`, then run this notebook with
    > `marimo edit notebook_02_intermediate.py` (or `marimo run ...`).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## A. Five simple+ queries
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 1. The 10 most popular movies

    **What we are doing.** A straight Top-N on the `popularity` score (TMDB's engagement metric), rounded for readability.

    **Concept:** `ORDER BY ... DESC`, `LIMIT`, `ROUND`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    p1_top_popularity = mo.sql(
        f"""
        SELECT title,
           ROUND(popularity, 1) AS popularity
        FROM movie
        ORDER BY popularity DESC
        LIMIT 10;
        """,
        engine=conn
    )
    return (p1_top_popularity,)


@app.cell
def _(p1_top_popularity, plot_util):
    plot_util.barh(p1_top_popularity, cat='title', val='popularity', title='10 most popular movies', xlabel='Popularity score')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 2. Movies released per decade

    **What we are doing.** We turn a year into a decade with a little arithmetic: `floor(year/10)*10`. Grouping on that computed value buckets every film into its decade.

    **Concept:** computed grouping key, `FLOOR`, `CAST`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    p2_per_decade = mo.sql(
        f"""
        SELECT CAST(FLOOR(year(release_date) / 10.0) * 10 AS INTEGER) AS decade,
           COUNT(*) AS n
        FROM movie
        WHERE release_date IS NOT NULL
        GROUP BY decade
        ORDER BY decade;
        """,
        engine=conn
    )
    return (p2_per_decade,)


@app.cell
def _(p2_per_decade, plot_util):
    plot_util.bar(p2_per_decade, cat='decade', val='n', title='Movies released per decade', ylabel='Number of movies')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 3. The 10 most profitable movies

    **What we are doing.** Profit is a derived column: `revenue - budget`. We only consider movies where both figures are known (> 0) and sort by the computed profit.

    **Concept:** arithmetic in `SELECT`, ordering by a derived value.
    """)
    return


@app.cell
def _(conn, mo, movie):
    p3_most_profitable = mo.sql(
        f"""
        SELECT title,
           budget,
           revenue,
           (revenue - budget) AS profit
        FROM movie
        WHERE budget > 0 AND revenue > 0
        ORDER BY profit DESC
        LIMIT 10;
        """,
        engine=conn
    )
    return (p3_most_profitable,)


@app.cell
def _(p3_most_profitable, plot_util):
    plot_util.barh(p3_most_profitable, cat='title', val='profit', title='10 most profitable movies', xlabel='Profit = revenue - budget (US$)')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 4. Average rating by year (busy years only)

    **What we are doing.** Group by year and average the ratings, but use `HAVING COUNT(*) >= 20` to keep only years with a meaningful sample. `HAVING` filters groups after aggregation, the way `WHERE` filters rows before it.

    **Concept:** `GROUP BY` + `AVG` + `HAVING`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    p4_avg_rating_by_year = mo.sql(
        f"""
        SELECT year(release_date) AS yr,
           ROUND(AVG(vote_average), 2) AS avg_rating,
           COUNT(*) AS n
        FROM movie
        WHERE release_date IS NOT NULL
        GROUP BY yr
        HAVING COUNT(*) >= 20
        ORDER BY yr;
        """,
        engine=conn
    )
    return (p4_avg_rating_by_year,)


@app.cell
def _(p4_avg_rating_by_year, plot_util):
    plot_util.line(p4_avg_rating_by_year, x='yr', y='avg_rating', title='Average movie rating by year (>= 20 movies/yr)', xlabel='Year', ylabel='Average rating')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 5. Distribution of ratings

    **What we are doing.** We bucket each movie into an integer rating (`ROUND(vote_average, 0)`) and count how many fall in each bucket - a histogram expressed purely in SQL. A vote floor keeps barely-rated films out.

    **Concept:** binning with `ROUND`, `GROUP BY` on the bin.
    """)
    return


@app.cell
def _(conn, mo, movie):
    p5_rating_distribution = mo.sql(
        f"""
        SELECT CAST(ROUND(vote_average, 0) AS INTEGER) AS rating_bucket,
           COUNT(*) AS n
        FROM movie
        WHERE vote_count >= 50
        GROUP BY rating_bucket
        ORDER BY rating_bucket;
        """,
        engine=conn
    )
    return (p5_rating_distribution,)


@app.cell
def _(p5_rating_distribution, plot_util):
    plot_util.bar(p5_rating_distribution, cat='rating_bucket', val='n', title='Distribution of movie ratings (>= 50 votes)', xlabel='Rating bucket', ylabel='Number of movies')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## B. Five intermediate queries (joins & aggregations)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 6. The 15 most prolific directors

    **What we are doing.** Crew roles live in `movie_crew` with a `job` column. We filter to `job = 'Director'`, join to `person`, and count distinct movies per director.

    **Concept:** filtered JOIN, `COUNT(DISTINCT ...)`.
    """)
    return


@app.cell
def _(conn, mo, movie_crew, person):
    p6_top_directors = mo.sql(
        f"""
        SELECT p.person_name AS director,
           COUNT(DISTINCT mc.movie_id) AS movies
        FROM movie_crew mc
        JOIN person p ON p.person_id = mc.person_id
        WHERE mc.job = 'Director'
        GROUP BY p.person_name
        ORDER BY movies DESC
        LIMIT 15;
        """,
        engine=conn
    )
    return (p6_top_directors,)


@app.cell
def _(p6_top_directors, plot_util):
    plot_util.barh(p6_top_directors, cat='director', val='movies', title='15 most prolific directors', xlabel='Number of movies directed')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 7. The 15 busiest production companies

    **What we are doing.** Join the `movie_company` bridge to `production_company` and count movies per studio.

    **Concept:** JOIN + `GROUP BY` + `COUNT` + `LIMIT`.
    """)
    return


@app.cell
def _(conn, mo, movie_company, production_company):
    p7_top_companies = mo.sql(
        f"""
        SELECT pco.company_name,
           COUNT(*) AS movies
        FROM movie_company mc
        JOIN production_company pco ON pco.company_id = mc.company_id
        GROUP BY pco.company_name
        ORDER BY movies DESC
        LIMIT 15;
        """,
        engine=conn
    )
    return (p7_top_companies,)


@app.cell
def _(p7_top_companies, plot_util):
    plot_util.barh(p7_top_companies, cat='company_name', val='movies', title='15 busiest production companies', xlabel='Number of movies')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 8. Which genres are rated highest?

    **What we are doing.** Average the rating within each genre (joined through the bridge table), keeping genres with a healthy sample via `HAVING`.

    **Concept:** JOIN + `GROUP BY` + `AVG` + `HAVING`.
    """)
    return


@app.cell
def _(conn, genre, mo, movie, movie_genres):
    p8_genre_rating = mo.sql(
        f"""
        SELECT g.genre_name,
           ROUND(AVG(m.vote_average), 2) AS avg_rating,
           COUNT(*) AS n
        FROM movie m
        JOIN movie_genres mg ON mg.movie_id = m.movie_id
        JOIN genre g         ON g.genre_id  = mg.genre_id
        GROUP BY g.genre_name
        HAVING COUNT(*) >= 30
        ORDER BY avg_rating DESC;
        """,
        engine=conn
    )
    return (p8_genre_rating,)


@app.cell
def _(p8_genre_rating, plot_util):
    plot_util.bar(p8_genre_rating, cat='genre_name', val='avg_rating', title='Average rating by genre', ylabel='Average rating', rotate=45)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 9. The 15 most common plot keywords

    **What we are doing.** Join `movie_keywords` to `keyword` and count the most frequently tagged themes across all movies.

    **Concept:** JOIN + `GROUP BY` + `COUNT` + `LIMIT`.
    """)
    return


@app.cell
def _(conn, keyword, mo, movie_keywords):
    p9_top_keywords = mo.sql(
        f"""
        SELECT k.keyword_name,
           COUNT(*) AS n
        FROM movie_keywords mk
        JOIN keyword k ON k.keyword_id = mk.keyword_id
        GROUP BY k.keyword_name
        ORDER BY n DESC
        LIMIT 15;
        """,
        engine=conn
    )
    return (p9_top_keywords,)


@app.cell
def _(p9_top_keywords, plot_util):
    plot_util.barh(p9_top_keywords, cat='keyword_name', val='n', title='15 most common plot keywords', xlabel='Number of movies')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 10. Average revenue by genre

    **What we are doing.** Among movies with known revenue, average the box office within each genre to see which genres earn most per film.

    **Concept:** JOIN + `GROUP BY` + `AVG` with a `WHERE` pre-filter.
    """)
    return


@app.cell
def _(conn, genre, mo, movie, movie_genres):
    p10_genre_revenue = mo.sql(
        f"""
        SELECT g.genre_name,
           ROUND(AVG(m.revenue), 0) AS avg_revenue
        FROM movie m
        JOIN movie_genres mg ON mg.movie_id = m.movie_id
        JOIN genre g         ON g.genre_id  = mg.genre_id
        WHERE m.revenue > 0
        GROUP BY g.genre_name
        ORDER BY avg_revenue DESC;
        """,
        engine=conn
    )
    return (p10_genre_revenue,)


@app.cell
def _(p10_genre_revenue, plot_util):
    plot_util.bar(p10_genre_revenue, cat='genre_name', val='avg_revenue', title='Average revenue by genre', ylabel='Average revenue (US$)', rotate=45)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## C. Ten intermediate+ queries (Top-N, window functions, CTEs)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 11. The highest-grossing movie of each decade

    **What we are doing.** A Common Table Expression (`WITH`) computes a `ROW_NUMBER()` that restarts (`PARTITION BY decade`) and ranks movies by revenue within each decade. Keeping `rn = 1` gives the single biggest hit per decade.

    **Concept:** CTE, window function `ROW_NUMBER() OVER (PARTITION BY ...)`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    p11_top_per_decade = mo.sql(
        f"""
        WITH ranked AS (
        SELECT title,
               revenue,
               CAST(FLOOR(year(release_date) / 10.0) * 10 AS INTEGER) AS decade,
               ROW_NUMBER() OVER (
                   PARTITION BY CAST(FLOOR(year(release_date) / 10.0) * 10 AS INTEGER)
                   ORDER BY revenue DESC
               ) AS rn
        FROM movie
        WHERE release_date IS NOT NULL AND revenue > 0
        )
        SELECT decade, title, revenue
        FROM ranked
        WHERE rn = 1
        ORDER BY decade;
        """,
        engine=conn
    )
    return (p11_top_per_decade,)


@app.cell
def _(p11_top_per_decade, plot_util):
    plot_util.barh(p11_top_per_decade, cat='title', val='revenue', title='Highest-grossing movie of each decade', xlabel='Revenue (US$)')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 12. The top 3 best-rated movies in every genre

    **What we are doing.** Same Top-N-per-group pattern, but we keep `rn <= 3`. `ROW_NUMBER()` partitions by genre and orders by rating (breaking ties on vote count).

    **Concept:** CTE + `ROW_NUMBER()` for Top-N within each group.
    """)
    return


@app.cell
def _(conn, genre, mo, movie, movie_genres):
    p12_top3_per_genre = mo.sql(
        f"""
        WITH ranked AS (
        SELECT g.genre_name,
               m.title,
               m.vote_average,
               ROW_NUMBER() OVER (
                   PARTITION BY g.genre_name
                   ORDER BY m.vote_average DESC, m.vote_count DESC
               ) AS rn
        FROM movie m
        JOIN movie_genres mg ON mg.movie_id = m.movie_id
        JOIN genre g         ON g.genre_id  = mg.genre_id
        WHERE m.vote_count >= 200
        )
        SELECT genre_name,
           title,
           ROUND(vote_average, 1) AS rating
        FROM ranked
        WHERE rn <= 3
        ORDER BY genre_name, rating DESC;
        """,
        engine=conn
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 13. The #1 box-office movie of each year (2000-2016)

    **What we are doing.** `RANK()` orders movies by revenue inside each release year. We keep the rank-1 film per year for a recent window. `RANK` (versus `ROW_NUMBER`) would tie movies with identical revenue.

    **Concept:** CTE + `RANK() OVER (PARTITION BY year ORDER BY revenue)`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    p13_rank_in_year = mo.sql(
        f"""
        WITH r AS (
        SELECT year(release_date) AS yr,
               title,
               revenue,
               RANK() OVER (
                   PARTITION BY year(release_date)
                   ORDER BY revenue DESC
               ) AS rnk
        FROM movie
        WHERE release_date IS NOT NULL AND revenue > 0
        )
        SELECT yr, title, revenue
        FROM r
        WHERE rnk = 1 AND yr BETWEEN 2000 AND 2016
        ORDER BY yr;
        """,
        engine=conn
    )
    return (p13_rank_in_year,)


@app.cell
def _(p13_rank_in_year, plot_util):
    plot_util.barh(p13_rank_in_year, cat='title', val='revenue', title='#1 box-office movie per year (2000-2016)', xlabel='Revenue (US$)')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 14. Movies more popular than average

    **What we are doing.** A scalar subquery computes the overall average popularity, and the outer query keeps movies above it. The subquery runs once and its single value is compared against every row.

    **Concept:** scalar subquery in the `WHERE` clause.
    """)
    return


@app.cell
def _(conn, mo, movie):
    p14_above_avg_pop = mo.sql(
        f"""
        SELECT title,
           ROUND(popularity, 1) AS popularity
        FROM movie
        WHERE popularity > (SELECT AVG(popularity) FROM movie)
        ORDER BY popularity DESC
        LIMIT 15;
        """,
        engine=conn
    )
    return (p14_above_avg_pop,)


@app.cell
def _(p14_above_avg_pop, plot_util):
    plot_util.barh(p14_above_avg_pop, cat='title', val='popularity', title='Most popular of the above-average movies', xlabel='Popularity score')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 15. The 2nd through 5th highest-grossing movies

    **What we are doing.** `LIMIT 4 OFFSET 1` skips the single biggest hit and returns the next four - the classic way to fetch "the runners up."

    **Concept:** `LIMIT ... OFFSET` paging.
    """)
    return


@app.cell
def _(conn, mo, movie):
    p15_second_to_fifth = mo.sql(
        f"""
        SELECT title, revenue
        FROM movie
        WHERE revenue > 0
        ORDER BY revenue DESC
        LIMIT 4 OFFSET 1;
        """,
        engine=conn
    )
    return (p15_second_to_fifth,)


@app.cell
def _(p15_second_to_fifth, plot_util):
    plot_util.barh(p15_second_to_fifth, cat='title', val='revenue', title='2nd-5th highest-grossing movies', xlabel='Revenue (US$)')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 16. Cumulative movies released over time

    **What we are doing.** A CTE counts movies per year; then a running total `SUM(n) OVER (ORDER BY yr)` accumulates them into a cumulative curve - the total catalogue size as of each year.

    **Concept:** CTE + cumulative window `SUM() OVER (ORDER BY ...)`.
    """)
    return


@app.cell
def _(conn, mo, movie):
    p16_cumulative = mo.sql(
        f"""
        WITH per_year AS (
        SELECT year(release_date) AS yr,
               COUNT(*) AS n
        FROM movie
        WHERE release_date IS NOT NULL
        GROUP BY yr
        )
        SELECT yr,
           n,
           SUM(n) OVER (ORDER BY yr) AS cumulative
        FROM per_year
        ORDER BY yr;
        """,
        engine=conn
    )
    return (p16_cumulative,)


@app.cell
def _(p16_cumulative, plot_util):
    plot_util.line(p16_cumulative, x='yr', y='cumulative', title='Cumulative number of movies over time', xlabel='Year', ylabel='Movies released (cumulative)')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 17. Each genre's share of all genre tags

    **What we are doing.** First a CTE counts movies per genre. Then an empty-window total `SUM(n) OVER ()` gives the grand total, letting us compute each genre's percentage share without a self-join.

    **Concept:** CTE + whole-table window `SUM() OVER ()` for a ratio.
    """)
    return


@app.cell
def _(conn, genre, mo, movie_genres):
    p17_genre_share = mo.sql(
        f"""
        WITH g AS (
        SELECT ge.genre_name,
               COUNT(*) AS n
        FROM movie_genres mg
        JOIN genre ge ON ge.genre_id = mg.genre_id
        GROUP BY ge.genre_name
        )
        SELECT genre_name,
           n,
           ROUND(100.0 * n / SUM(n) OVER (), 1) AS pct_of_tags
        FROM g
        ORDER BY n DESC;
        """,
        engine=conn
    )
    return (p17_genre_share,)


@app.cell
def _(p17_genre_share, plot_util):
    plot_util.bar(p17_genre_share, cat='genre_name', val='pct_of_tags', title="Each genre's share of all genre tags (%)", ylabel='Share of tags (%)', rotate=45)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 18. The 15 actors with the most combined box office

    **What we are doing.** A CTE sums the revenue of every movie an actor appears in (cast joined to movie), then we take the Top 15 by total box office. Note this double-counts ensemble films, which is typical for star-power rankings.

    **Concept:** CTE + multi-table JOIN + `SUM` aggregation + Top-N.
    """)
    return


@app.cell
def _(conn, mo, movie, movie_cast, person):
    p18_actor_boxoffice = mo.sql(
        f"""
        WITH actor_rev AS (
        SELECT p.person_name AS actor,
               SUM(m.revenue) AS total_revenue,
               COUNT(*)       AS movies
        FROM movie_cast mc
        JOIN person p ON p.person_id = mc.person_id
        JOIN movie m  ON m.movie_id  = mc.movie_id
        WHERE m.revenue > 0
        GROUP BY p.person_name
        )
        SELECT actor, total_revenue, movies
        FROM actor_rev
        ORDER BY total_revenue DESC
        LIMIT 15;
        """,
        engine=conn
    )
    return (p18_actor_boxoffice,)


@app.cell
def _(p18_actor_boxoffice, plot_util):
    plot_util.barh(p18_actor_boxoffice, cat='actor', val='total_revenue', title='15 actors with the most combined box office', xlabel='Total box office (US$)')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 19. The 3 most prolific actors of each gender

    **What we are doing.** Two stacked CTEs: the first counts credits per (gender, actor); the second applies `RANK() OVER (PARTITION BY gender ORDER BY movies DESC)`. We keep the top 3 of each gender.

    **Concept:** chained CTEs + `RANK()` partitioned Top-N.
    """)
    return


@app.cell
def _(conn, gender, mo, movie_cast, person):
    p19_top_actor_per_gender = mo.sql(
        f"""
        WITH counts AS (
        SELECT gd.gender   AS gender,
               p.person_name AS actor,
               COUNT(*)    AS movies
        FROM movie_cast mc
        JOIN person p  ON p.person_id = mc.person_id
        JOIN gender gd ON gd.gender_id = mc.gender_id
        GROUP BY gd.gender, p.person_name
        ),
        ranked AS (
        SELECT gender, actor, movies,
               RANK() OVER (PARTITION BY gender ORDER BY movies DESC) AS rnk
        FROM counts
        )
        SELECT gender, actor, movies
        FROM ranked
        WHERE rnk <= 3
        ORDER BY gender, movies DESC;
        """,
        engine=conn
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 20. Year-over-year change in movies released

    **What we are doing.** A CTE counts movies per year; then `LAG(n)` looks at the previous year's count so we can compute the year-over-year delta. `LAG` is the window function for "the value in the row before."

    **Concept:** CTE + `LAG() OVER (ORDER BY ...)` for period-over-period change.
    """)
    return


@app.cell
def _(conn, mo, movie):
    p20_yoy_change = mo.sql(
        f"""
        WITH per_year AS (
        SELECT year(release_date) AS yr,
               COUNT(*) AS n
        FROM movie
        WHERE release_date IS NOT NULL
        GROUP BY yr
        )
        SELECT yr,
           n,
           n - LAG(n) OVER (ORDER BY yr) AS yoy_change
        FROM per_year
        WHERE yr BETWEEN 1990 AND 2016
        ORDER BY yr;
        """,
        engine=conn
    )
    return (p20_yoy_change,)


@app.cell
def _(p20_yoy_change, plot_util):
    plot_util.line(p20_yoy_change, x='yr', y='yoy_change', title='Year-over-year change in movies released', xlabel='Year', ylabel='Change vs. previous year')
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
