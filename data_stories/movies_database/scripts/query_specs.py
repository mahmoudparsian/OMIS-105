# -*- coding: utf-8 -*-
"""
query_specs.py
--------------
Single source of truth for every query used in the two Marimo notebooks.

Each spec is a dict:
    id     : short unique slug (also used as the SQL-result variable name)
    title  : human title
    md     : a detailed explanation (rendered as a marimo markdown cell)
    sql    : a PURE DuckDB SQL statement (string, no f-string interpolation)
    plot   : None, or a dict describing how plot_util should chart the result
             { "kind": "barh|bar|line", "cat"/"x": col, "val"/"y": col,
               "title": str, "xlabel": str, "ylabel": str }

The same specs feed:
  * scripts/gen_notebooks.py   -> builds the .py marimo notebooks
  * scripts/test_queries.py    -> executes every SQL against the real data
                                  (via SQLite with year()/floor() shims) to
                                  prove the logic is correct.
"""

# ---------------------------------------------------------------------------
# NOTEBOOK 1  --  Basics
# ---------------------------------------------------------------------------

NB1 = [
    # ===================== 5 SIMPLE =====================
    dict(
        id="q1_total_movies",
        section="A. Five simple queries",
        title="1. How many movies are in the database?",
        md=(
            "**What we are doing.** The simplest possible question: a single-row "
            "count of the whole `movie` table. `COUNT(*)` counts every row, and "
            "we give the result a readable alias with `AS total_movies`.\n\n"
            "**Concept:** `SELECT`, `COUNT(*)`, column aliasing."
        ),
        sql="SELECT COUNT(*) AS total_movies\nFROM movie;",
        plot=None,
    ),
    dict(
        id="q2_top_revenue",
        section="A. Five simple queries",
        title="2. The 10 highest-grossing movies",
        md=(
            "**What we are doing.** We sort the table by `revenue` from highest to "
            "lowest and keep only the first ten rows. `WHERE revenue > 0` drops the "
            "many rows whose revenue is unknown (stored as 0).\n\n"
            "**Concept:** `WHERE`, `ORDER BY ... DESC`, `LIMIT`."
        ),
        sql=(
            "SELECT title, revenue\n"
            "FROM movie\n"
            "WHERE revenue > 0\n"
            "ORDER BY revenue DESC\n"
            "LIMIT 10;"
        ),
        plot=dict(kind="barh", cat="title", val="revenue",
                  title="Top 10 highest-grossing movies",
                  xlabel="Worldwide revenue (US$)"),
    ),
    dict(
        id="q3_top_rated",
        section="A. Five simple queries",
        title="3. The 10 best-rated movies (with enough votes)",
        md=(
            "**What we are doing.** We rank movies by `vote_average`, but only among "
            "films with at least 1,000 votes so that obscure titles with a single "
            "perfect score do not dominate. `ROUND(vote_average, 1)` tidies the "
            "rating to one decimal place.\n\n"
            "**Concept:** filtering on a threshold, `ROUND`, multi-key `ORDER BY`."
        ),
        sql=(
            "SELECT title,\n"
            "       ROUND(vote_average, 1) AS rating,\n"
            "       vote_count\n"
            "FROM movie\n"
            "WHERE vote_count >= 1000\n"
            "ORDER BY vote_average DESC, vote_count DESC\n"
            "LIMIT 10;"
        ),
        plot=dict(kind="barh", cat="title", val="rating",
                  title="Top 10 best-rated movies (>= 1000 votes)",
                  xlabel="Average rating (0-10)"),
    ),
    dict(
        id="q4_status_counts",
        section="A. Five simple queries",
        title="4. How many movies per release status?",
        md=(
            "**What we are doing.** Our first aggregation. `GROUP BY movie_status` "
            "collapses the table into one row per distinct status (Released, "
            "Rumored, Post Production, ...) and `COUNT(*)` tells us how many movies "
            "fall in each bucket.\n\n"
            "**Concept:** `GROUP BY` with `COUNT(*)`."
        ),
        sql=(
            "SELECT movie_status,\n"
            "       COUNT(*) AS n\n"
            "FROM movie\n"
            "GROUP BY movie_status\n"
            "ORDER BY n DESC;"
        ),
        plot=dict(kind="bar", cat="movie_status", val="n",
                  title="Movies by release status",
                  ylabel="Number of movies"),
    ),
    dict(
        id="q5_longest",
        section="A. Five simple queries",
        title="5. The 10 longest movies by runtime",
        md=(
            "**What we are doing.** A straight sort on `runtime` (minutes), keeping "
            "the ten longest. `WHERE runtime > 0` removes rows with a missing "
            "runtime.\n\n"
            "**Concept:** `ORDER BY ... DESC` on a numeric column, `LIMIT`."
        ),
        sql=(
            "SELECT title, runtime\n"
            "FROM movie\n"
            "WHERE runtime > 0\n"
            "ORDER BY runtime DESC\n"
            "LIMIT 10;"
        ),
        plot=dict(kind="barh", cat="title", val="runtime",
                  title="Top 10 longest movies",
                  xlabel="Runtime (minutes)"),
    ),

    # ===================== 5 SIMPLE+ =====================
    dict(
        id="q6_dark_titles",
        section="B. Five simple+ queries",
        title="6. Every movie with \"dark\" in the title",
        md=(
            "**What we are doing.** Pattern matching with `LIKE`. We lower-case the "
            "title first so the search is case-insensitive, and `'%dark%'` matches "
            "the word anywhere in the title (the `%` are wildcards).\n\n"
            "**Concept:** `LOWER`, `LIKE`, wildcards."
        ),
        sql=(
            "SELECT title,\n"
            "       ROUND(vote_average, 1) AS rating\n"
            "FROM movie\n"
            "WHERE LOWER(title) LIKE '%dark%'\n"
            "ORDER BY vote_average DESC;"
        ),
        plot=None,
    ),
    dict(
        id="q7_q1_2005",
        section="B. Five simple+ queries",
        title="7. Best-rated movies released in Q1 2005",
        md=(
            "**What we are doing.** We restrict to a date window with `BETWEEN` "
            "(January-March 2005) and order by rating. DuckDB compares the `DATE` "
            "column directly against the date literals.\n\n"
            "**Concept:** `BETWEEN` on dates, date literals."
        ),
        sql=(
            "SELECT title,\n"
            "       release_date,\n"
            "       ROUND(vote_average, 1) AS rating\n"
            "FROM movie\n"
            "WHERE release_date BETWEEN DATE '2005-01-01' AND DATE '2005-03-31'\n"
            "ORDER BY vote_average DESC\n"
            "LIMIT 15;"
        ),
        plot=None,
    ),
    dict(
        id="q8_per_year",
        section="B. Five simple+ queries",
        title="8. How many movies were released each year?",
        md=(
            "**What we are doing.** We extract the calendar year from `release_date` "
            "with the `year()` function, group by it, and count. This is a classic "
            "time-series shape, perfect for a line chart.\n\n"
            "**Concept:** date-part extraction (`year`), `GROUP BY` a computed "
            "column, `IS NOT NULL`."
        ),
        sql=(
            "SELECT year(release_date) AS yr,\n"
            "       COUNT(*) AS n\n"
            "FROM movie\n"
            "WHERE release_date IS NOT NULL\n"
            "GROUP BY yr\n"
            "ORDER BY yr;"
        ),
        plot=dict(kind="line", x="yr", y="n",
                  title="Movies released per year",
                  xlabel="Year", ylabel="Number of movies"),
    ),
    dict(
        id="q9_money_summary",
        section="B. Five simple+ queries",
        title="9. Budget & revenue summary statistics",
        md=(
            "**What we are doing.** Several aggregate functions in one query to "
            "profile the money columns: how many movies have a known budget, and "
            "their average/maximum budget, revenue and runtime. `ROUND(..., 0)` "
            "keeps the big dollar figures readable.\n\n"
            "**Concept:** multiple aggregates (`COUNT`, `AVG`, `MAX`) in a single "
            "`SELECT`."
        ),
        sql=(
            "SELECT COUNT(*)                  AS movies_with_budget,\n"
            "       ROUND(AVG(budget), 0)     AS avg_budget,\n"
            "       MAX(budget)               AS max_budget,\n"
            "       ROUND(AVG(revenue), 0)    AS avg_revenue,\n"
            "       MAX(revenue)              AS max_revenue,\n"
            "       ROUND(AVG(runtime), 1)    AS avg_runtime\n"
            "FROM movie\n"
            "WHERE budget > 0;"
        ),
        plot=None,
    ),
    dict(
        id="q10_great_and_popular",
        section="B. Five simple+ queries",
        title="10. Movies that are both great and widely voted",
        md=(
            "**What we are doing.** Two conditions joined with `AND`: a high rating "
            "(>= 8.0) and broad audience engagement (>= 5,000 votes). This finds "
            "the crowd-certified classics.\n\n"
            "**Concept:** compound `WHERE` with `AND`."
        ),
        sql=(
            "SELECT title,\n"
            "       ROUND(vote_average, 1) AS rating,\n"
            "       vote_count\n"
            "FROM movie\n"
            "WHERE vote_average >= 8.0\n"
            "  AND vote_count  >= 5000\n"
            "ORDER BY vote_count DESC;"
        ),
        plot=dict(kind="barh", cat="title", val="vote_count",
                  title="Great + widely-voted movies",
                  xlabel="Number of votes"),
    ),

    # ===================== 5 INTERMEDIATE =====================
    dict(
        id="q11_action_top",
        section="C. Five intermediate queries (joins & aggregations)",
        title="11. Top 10 Action movies by rating",
        md=(
            "**What we are doing.** Our first JOIN. Genres live in a separate "
            "`genre` table linked to movies through the `movie_genres` bridge "
            "table. We chain two joins to filter to Action films, then rank by "
            "rating (with a vote threshold).\n\n"
            "**Concept:** many-to-many JOIN through a bridge table."
        ),
        sql=(
            "SELECT m.title,\n"
            "       ROUND(m.vote_average, 1) AS rating\n"
            "FROM movie m\n"
            "JOIN movie_genres mg ON mg.movie_id = m.movie_id\n"
            "JOIN genre g         ON g.genre_id  = mg.genre_id\n"
            "WHERE g.genre_name = 'Action'\n"
            "  AND m.vote_count >= 500\n"
            "ORDER BY m.vote_average DESC\n"
            "LIMIT 10;"
        ),
        plot=dict(kind="barh", cat="title", val="rating",
                  title="Top 10 Action movies by rating",
                  xlabel="Average rating (0-10)"),
    ),
    dict(
        id="q12_genre_counts",
        section="C. Five intermediate queries (joins & aggregations)",
        title="12. How many movies in each genre?",
        md=(
            "**What we are doing.** Join the bridge table to `genre`, group by "
            "genre name, and count. Because one movie can have several genres the "
            "totals add up to more than the number of movies.\n\n"
            "**Concept:** JOIN + `GROUP BY` + `COUNT`."
        ),
        sql=(
            "SELECT g.genre_name,\n"
            "       COUNT(*) AS n\n"
            "FROM movie_genres mg\n"
            "JOIN genre g ON g.genre_id = mg.genre_id\n"
            "GROUP BY g.genre_name\n"
            "ORDER BY n DESC;"
        ),
        plot=dict(kind="bar", cat="genre_name", val="n",
                  title="Number of movies per genre",
                  ylabel="Number of movies", rotate=45),
    ),
    dict(
        id="q13_busy_actors",
        section="C. Five intermediate queries (joins & aggregations)",
        title="13. The 15 most prolific actors",
        md=(
            "**What we are doing.** Count how many cast credits each person has by "
            "joining `movie_cast` to `person`, grouping by the actor's name.\n\n"
            "**Concept:** JOIN + `GROUP BY` + `COUNT`, `LIMIT` for a Top-N list."
        ),
        sql=(
            "SELECT p.person_name AS actor,\n"
            "       COUNT(*)      AS movie_count\n"
            "FROM movie_cast mc\n"
            "JOIN person p ON p.person_id = mc.person_id\n"
            "GROUP BY p.person_name\n"
            "ORDER BY movie_count DESC\n"
            "LIMIT 15;"
        ),
        plot=dict(kind="barh", cat="actor", val="movie_count",
                  title="15 most prolific actors",
                  xlabel="Number of cast credits"),
    ),
    dict(
        id="q14_forrest_cast",
        section="C. Five intermediate queries (joins & aggregations)",
        title="14. The cast of \"Forrest Gump\"",
        md=(
            "**What we are doing.** A three-way JOIN movie -> movie_cast -> person "
            "to list who played whom, ordered by billing position "
            "(`cast_order`).\n\n"
            "**Concept:** multi-table JOIN, ordering by a sort key."
        ),
        sql=(
            "SELECT mc.cast_order,\n"
            "       mc.character_name,\n"
            "       p.person_name AS actor\n"
            "FROM movie m\n"
            "JOIN movie_cast mc ON mc.movie_id  = m.movie_id\n"
            "JOIN person p      ON p.person_id  = mc.person_id\n"
            "WHERE m.title = 'Forrest Gump'\n"
            "ORDER BY mc.cast_order\n"
            "LIMIT 20;"
        ),
        plot=None,
    ),
    dict(
        id="q15_country_counts",
        section="C. Five intermediate queries (joins & aggregations)",
        title="15. Top 15 production countries",
        md=(
            "**What we are doing.** Join the `production_country` bridge table to "
            "`country` and count movies per country to see where films are made.\n\n"
            "**Concept:** JOIN + `GROUP BY` + `COUNT` + `LIMIT`."
        ),
        sql=(
            "SELECT c.country_name,\n"
            "       COUNT(*) AS n\n"
            "FROM production_country pc\n"
            "JOIN country c ON c.country_id = pc.country_id\n"
            "GROUP BY c.country_name\n"
            "ORDER BY n DESC\n"
            "LIMIT 15;"
        ),
        plot=dict(kind="barh", cat="country_name", val="n",
                  title="Top 15 production countries",
                  xlabel="Number of movies"),
    ),
]


# ---------------------------------------------------------------------------
# NOTEBOOK 2  --  Intermediate -> Intermediate+
# ---------------------------------------------------------------------------

NB2 = [
    # ===================== 5 SIMPLE+ =====================
    dict(
        id="p1_top_popularity",
        section="A. Five simple+ queries",
        title="1. The 10 most popular movies",
        md=(
            "**What we are doing.** A straight Top-N on the `popularity` score "
            "(TMDB's engagement metric), rounded for readability.\n\n"
            "**Concept:** `ORDER BY ... DESC`, `LIMIT`, `ROUND`."
        ),
        sql=(
            "SELECT title,\n"
            "       ROUND(popularity, 1) AS popularity\n"
            "FROM movie\n"
            "ORDER BY popularity DESC\n"
            "LIMIT 10;"
        ),
        plot=dict(kind="barh", cat="title", val="popularity",
                  title="10 most popular movies",
                  xlabel="Popularity score"),
    ),
    dict(
        id="p2_per_decade",
        section="A. Five simple+ queries",
        title="2. Movies released per decade",
        md=(
            "**What we are doing.** We turn a year into a decade with a little "
            "arithmetic: `floor(year/10)*10`. Grouping on that computed value "
            "buckets every film into its decade.\n\n"
            "**Concept:** computed grouping key, `FLOOR`, `CAST`."
        ),
        sql=(
            "SELECT CAST(FLOOR(year(release_date) / 10.0) * 10 AS INTEGER) AS decade,\n"
            "       COUNT(*) AS n\n"
            "FROM movie\n"
            "WHERE release_date IS NOT NULL\n"
            "GROUP BY decade\n"
            "ORDER BY decade;"
        ),
        plot=dict(kind="bar", cat="decade", val="n",
                  title="Movies released per decade",
                  ylabel="Number of movies"),
    ),
    dict(
        id="p3_most_profitable",
        section="A. Five simple+ queries",
        title="3. The 10 most profitable movies",
        md=(
            "**What we are doing.** Profit is a derived column: `revenue - budget`. "
            "We only consider movies where both figures are known (> 0) and sort by "
            "the computed profit.\n\n"
            "**Concept:** arithmetic in `SELECT`, ordering by a derived value."
        ),
        sql=(
            "SELECT title,\n"
            "       budget,\n"
            "       revenue,\n"
            "       (revenue - budget) AS profit\n"
            "FROM movie\n"
            "WHERE budget > 0 AND revenue > 0\n"
            "ORDER BY profit DESC\n"
            "LIMIT 10;"
        ),
        plot=dict(kind="barh", cat="title", val="profit",
                  title="10 most profitable movies",
                  xlabel="Profit = revenue - budget (US$)"),
    ),
    dict(
        id="p4_avg_rating_by_year",
        section="A. Five simple+ queries",
        title="4. Average rating by year (busy years only)",
        md=(
            "**What we are doing.** Group by year and average the ratings, but use "
            "`HAVING COUNT(*) >= 20` to keep only years with a meaningful sample. "
            "`HAVING` filters groups after aggregation, the way `WHERE` filters "
            "rows before it.\n\n"
            "**Concept:** `GROUP BY` + `AVG` + `HAVING`."
        ),
        sql=(
            "SELECT year(release_date) AS yr,\n"
            "       ROUND(AVG(vote_average), 2) AS avg_rating,\n"
            "       COUNT(*) AS n\n"
            "FROM movie\n"
            "WHERE release_date IS NOT NULL\n"
            "GROUP BY yr\n"
            "HAVING COUNT(*) >= 20\n"
            "ORDER BY yr;"
        ),
        plot=dict(kind="line", x="yr", y="avg_rating",
                  title="Average movie rating by year (>= 20 movies/yr)",
                  xlabel="Year", ylabel="Average rating"),
    ),
    dict(
        id="p5_rating_distribution",
        section="A. Five simple+ queries",
        title="5. Distribution of ratings",
        md=(
            "**What we are doing.** We bucket each movie into an integer rating "
            "(`ROUND(vote_average, 0)`) and count how many fall in each bucket - a "
            "histogram expressed purely in SQL. A vote floor keeps barely-rated "
            "films out.\n\n"
            "**Concept:** binning with `ROUND`, `GROUP BY` on the bin."
        ),
        sql=(
            "SELECT CAST(ROUND(vote_average, 0) AS INTEGER) AS rating_bucket,\n"
            "       COUNT(*) AS n\n"
            "FROM movie\n"
            "WHERE vote_count >= 50\n"
            "GROUP BY rating_bucket\n"
            "ORDER BY rating_bucket;"
        ),
        plot=dict(kind="bar", cat="rating_bucket", val="n",
                  title="Distribution of movie ratings (>= 50 votes)",
                  xlabel="Rating bucket", ylabel="Number of movies"),
    ),

    # ===================== 5 INTERMEDIATE =====================
    dict(
        id="p6_top_directors",
        section="B. Five intermediate queries (joins & aggregations)",
        title="6. The 15 most prolific directors",
        md=(
            "**What we are doing.** Crew roles live in `movie_crew` with a `job` "
            "column. We filter to `job = 'Director'`, join to `person`, and count "
            "distinct movies per director.\n\n"
            "**Concept:** filtered JOIN, `COUNT(DISTINCT ...)`."
        ),
        sql=(
            "SELECT p.person_name AS director,\n"
            "       COUNT(DISTINCT mc.movie_id) AS movies\n"
            "FROM movie_crew mc\n"
            "JOIN person p ON p.person_id = mc.person_id\n"
            "WHERE mc.job = 'Director'\n"
            "GROUP BY p.person_name\n"
            "ORDER BY movies DESC\n"
            "LIMIT 15;"
        ),
        plot=dict(kind="barh", cat="director", val="movies",
                  title="15 most prolific directors",
                  xlabel="Number of movies directed"),
    ),
    dict(
        id="p7_top_companies",
        section="B. Five intermediate queries (joins & aggregations)",
        title="7. The 15 busiest production companies",
        md=(
            "**What we are doing.** Join the `movie_company` bridge to "
            "`production_company` and count movies per studio.\n\n"
            "**Concept:** JOIN + `GROUP BY` + `COUNT` + `LIMIT`."
        ),
        sql=(
            "SELECT pco.company_name,\n"
            "       COUNT(*) AS movies\n"
            "FROM movie_company mc\n"
            "JOIN production_company pco ON pco.company_id = mc.company_id\n"
            "GROUP BY pco.company_name\n"
            "ORDER BY movies DESC\n"
            "LIMIT 15;"
        ),
        plot=dict(kind="barh", cat="company_name", val="movies",
                  title="15 busiest production companies",
                  xlabel="Number of movies"),
    ),
    dict(
        id="p8_genre_rating",
        section="B. Five intermediate queries (joins & aggregations)",
        title="8. Which genres are rated highest?",
        md=(
            "**What we are doing.** Average the rating within each genre (joined "
            "through the bridge table), keeping genres with a healthy sample via "
            "`HAVING`.\n\n"
            "**Concept:** JOIN + `GROUP BY` + `AVG` + `HAVING`."
        ),
        sql=(
            "SELECT g.genre_name,\n"
            "       ROUND(AVG(m.vote_average), 2) AS avg_rating,\n"
            "       COUNT(*) AS n\n"
            "FROM movie m\n"
            "JOIN movie_genres mg ON mg.movie_id = m.movie_id\n"
            "JOIN genre g         ON g.genre_id  = mg.genre_id\n"
            "GROUP BY g.genre_name\n"
            "HAVING COUNT(*) >= 30\n"
            "ORDER BY avg_rating DESC;"
        ),
        plot=dict(kind="bar", cat="genre_name", val="avg_rating",
                  title="Average rating by genre",
                  ylabel="Average rating", rotate=45),
    ),
    dict(
        id="p9_top_keywords",
        section="B. Five intermediate queries (joins & aggregations)",
        title="9. The 15 most common plot keywords",
        md=(
            "**What we are doing.** Join `movie_keywords` to `keyword` and count "
            "the most frequently tagged themes across all movies.\n\n"
            "**Concept:** JOIN + `GROUP BY` + `COUNT` + `LIMIT`."
        ),
        sql=(
            "SELECT k.keyword_name,\n"
            "       COUNT(*) AS n\n"
            "FROM movie_keywords mk\n"
            "JOIN keyword k ON k.keyword_id = mk.keyword_id\n"
            "GROUP BY k.keyword_name\n"
            "ORDER BY n DESC\n"
            "LIMIT 15;"
        ),
        plot=dict(kind="barh", cat="keyword_name", val="n",
                  title="15 most common plot keywords",
                  xlabel="Number of movies"),
    ),
    dict(
        id="p10_genre_revenue",
        section="B. Five intermediate queries (joins & aggregations)",
        title="10. Average revenue by genre",
        md=(
            "**What we are doing.** Among movies with known revenue, average the "
            "box office within each genre to see which genres earn most per film.\n\n"
            "**Concept:** JOIN + `GROUP BY` + `AVG` with a `WHERE` pre-filter."
        ),
        sql=(
            "SELECT g.genre_name,\n"
            "       ROUND(AVG(m.revenue), 0) AS avg_revenue\n"
            "FROM movie m\n"
            "JOIN movie_genres mg ON mg.movie_id = m.movie_id\n"
            "JOIN genre g         ON g.genre_id  = mg.genre_id\n"
            "WHERE m.revenue > 0\n"
            "GROUP BY g.genre_name\n"
            "ORDER BY avg_revenue DESC;"
        ),
        plot=dict(kind="bar", cat="genre_name", val="avg_revenue",
                  title="Average revenue by genre",
                  ylabel="Average revenue (US$)", rotate=45),
    ),

    # ===================== 10 INTERMEDIATE+ =====================
    dict(
        id="p11_top_per_decade",
        section="C. Ten intermediate+ queries (Top-N, window functions, CTEs)",
        title="11. The highest-grossing movie of each decade",
        md=(
            "**What we are doing.** A Common Table Expression (`WITH`) computes a "
            "`ROW_NUMBER()` that restarts (`PARTITION BY decade`) and ranks movies "
            "by revenue within each decade. Keeping `rn = 1` gives the single "
            "biggest hit per decade.\n\n"
            "**Concept:** CTE, window function `ROW_NUMBER() OVER (PARTITION BY ...)`."
        ),
        sql=(
            "WITH ranked AS (\n"
            "    SELECT title,\n"
            "           revenue,\n"
            "           CAST(FLOOR(year(release_date) / 10.0) * 10 AS INTEGER) AS decade,\n"
            "           ROW_NUMBER() OVER (\n"
            "               PARTITION BY CAST(FLOOR(year(release_date) / 10.0) * 10 AS INTEGER)\n"
            "               ORDER BY revenue DESC\n"
            "           ) AS rn\n"
            "    FROM movie\n"
            "    WHERE release_date IS NOT NULL AND revenue > 0\n"
            ")\n"
            "SELECT decade, title, revenue\n"
            "FROM ranked\n"
            "WHERE rn = 1\n"
            "ORDER BY decade;"
        ),
        plot=dict(kind="barh", cat="title", val="revenue",
                  title="Highest-grossing movie of each decade",
                  xlabel="Revenue (US$)"),
    ),
    dict(
        id="p12_top3_per_genre",
        section="C. Ten intermediate+ queries (Top-N, window functions, CTEs)",
        title="12. The top 3 best-rated movies in every genre",
        md=(
            "**What we are doing.** Same Top-N-per-group pattern, but we keep "
            "`rn <= 3`. `ROW_NUMBER()` partitions by genre and orders by rating "
            "(breaking ties on vote count).\n\n"
            "**Concept:** CTE + `ROW_NUMBER()` for Top-N within each group."
        ),
        sql=(
            "WITH ranked AS (\n"
            "    SELECT g.genre_name,\n"
            "           m.title,\n"
            "           m.vote_average,\n"
            "           ROW_NUMBER() OVER (\n"
            "               PARTITION BY g.genre_name\n"
            "               ORDER BY m.vote_average DESC, m.vote_count DESC\n"
            "           ) AS rn\n"
            "    FROM movie m\n"
            "    JOIN movie_genres mg ON mg.movie_id = m.movie_id\n"
            "    JOIN genre g         ON g.genre_id  = mg.genre_id\n"
            "    WHERE m.vote_count >= 200\n"
            ")\n"
            "SELECT genre_name,\n"
            "       title,\n"
            "       ROUND(vote_average, 1) AS rating\n"
            "FROM ranked\n"
            "WHERE rn <= 3\n"
            "ORDER BY genre_name, rating DESC;"
        ),
        plot=None,
    ),
    dict(
        id="p13_rank_in_year",
        section="C. Ten intermediate+ queries (Top-N, window functions, CTEs)",
        title="13. The #1 box-office movie of each year (2000-2016)",
        md=(
            "**What we are doing.** `RANK()` orders movies by revenue inside each "
            "release year. We keep the rank-1 film per year for a recent window. "
            "`RANK` (versus `ROW_NUMBER`) would tie movies with identical revenue.\n\n"
            "**Concept:** CTE + `RANK() OVER (PARTITION BY year ORDER BY revenue)`."
        ),
        sql=(
            "WITH r AS (\n"
            "    SELECT year(release_date) AS yr,\n"
            "           title,\n"
            "           revenue,\n"
            "           RANK() OVER (\n"
            "               PARTITION BY year(release_date)\n"
            "               ORDER BY revenue DESC\n"
            "           ) AS rnk\n"
            "    FROM movie\n"
            "    WHERE release_date IS NOT NULL AND revenue > 0\n"
            ")\n"
            "SELECT yr, title, revenue\n"
            "FROM r\n"
            "WHERE rnk = 1 AND yr BETWEEN 2000 AND 2016\n"
            "ORDER BY yr;"
        ),
        plot=dict(kind="barh", cat="title", val="revenue",
                  title="#1 box-office movie per year (2000-2016)",
                  xlabel="Revenue (US$)"),
    ),
    dict(
        id="p14_above_avg_pop",
        section="C. Ten intermediate+ queries (Top-N, window functions, CTEs)",
        title="14. Movies more popular than average",
        md=(
            "**What we are doing.** A scalar subquery computes the overall average "
            "popularity, and the outer query keeps movies above it. The subquery "
            "runs once and its single value is compared against every row.\n\n"
            "**Concept:** scalar subquery in the `WHERE` clause."
        ),
        sql=(
            "SELECT title,\n"
            "       ROUND(popularity, 1) AS popularity\n"
            "FROM movie\n"
            "WHERE popularity > (SELECT AVG(popularity) FROM movie)\n"
            "ORDER BY popularity DESC\n"
            "LIMIT 15;"
        ),
        plot=dict(kind="barh", cat="title", val="popularity",
                  title="Most popular of the above-average movies",
                  xlabel="Popularity score"),
    ),
    dict(
        id="p15_second_to_fifth",
        section="C. Ten intermediate+ queries (Top-N, window functions, CTEs)",
        title="15. The 2nd through 5th highest-grossing movies",
        md=(
            "**What we are doing.** `LIMIT 4 OFFSET 1` skips the single biggest hit "
            "and returns the next four - the classic way to fetch \"the runners "
            "up.\"\n\n"
            "**Concept:** `LIMIT ... OFFSET` paging."
        ),
        sql=(
            "SELECT title, revenue\n"
            "FROM movie\n"
            "WHERE revenue > 0\n"
            "ORDER BY revenue DESC\n"
            "LIMIT 4 OFFSET 1;"
        ),
        plot=dict(kind="barh", cat="title", val="revenue",
                  title="2nd-5th highest-grossing movies",
                  xlabel="Revenue (US$)"),
    ),
    dict(
        id="p16_cumulative",
        section="C. Ten intermediate+ queries (Top-N, window functions, CTEs)",
        title="16. Cumulative movies released over time",
        md=(
            "**What we are doing.** A CTE counts movies per year; then a running "
            "total `SUM(n) OVER (ORDER BY yr)` accumulates them into a cumulative "
            "curve - the total catalogue size as of each year.\n\n"
            "**Concept:** CTE + cumulative window `SUM() OVER (ORDER BY ...)`."
        ),
        sql=(
            "WITH per_year AS (\n"
            "    SELECT year(release_date) AS yr,\n"
            "           COUNT(*) AS n\n"
            "    FROM movie\n"
            "    WHERE release_date IS NOT NULL\n"
            "    GROUP BY yr\n"
            ")\n"
            "SELECT yr,\n"
            "       n,\n"
            "       SUM(n) OVER (ORDER BY yr) AS cumulative\n"
            "FROM per_year\n"
            "ORDER BY yr;"
        ),
        plot=dict(kind="line", x="yr", y="cumulative",
                  title="Cumulative number of movies over time",
                  xlabel="Year", ylabel="Movies released (cumulative)"),
    ),
    dict(
        id="p17_genre_share",
        section="C. Ten intermediate+ queries (Top-N, window functions, CTEs)",
        title="17. Each genre's share of all genre tags",
        md=(
            "**What we are doing.** First a CTE counts movies per genre. Then an "
            "empty-window total `SUM(n) OVER ()` gives the grand total, letting us "
            "compute each genre's percentage share without a self-join.\n\n"
            "**Concept:** CTE + whole-table window `SUM() OVER ()` for a ratio."
        ),
        sql=(
            "WITH g AS (\n"
            "    SELECT ge.genre_name,\n"
            "           COUNT(*) AS n\n"
            "    FROM movie_genres mg\n"
            "    JOIN genre ge ON ge.genre_id = mg.genre_id\n"
            "    GROUP BY ge.genre_name\n"
            ")\n"
            "SELECT genre_name,\n"
            "       n,\n"
            "       ROUND(100.0 * n / SUM(n) OVER (), 1) AS pct_of_tags\n"
            "FROM g\n"
            "ORDER BY n DESC;"
        ),
        plot=dict(kind="bar", cat="genre_name", val="pct_of_tags",
                  title="Each genre's share of all genre tags (%)",
                  ylabel="Share of tags (%)", rotate=45),
    ),
    dict(
        id="p18_actor_boxoffice",
        section="C. Ten intermediate+ queries (Top-N, window functions, CTEs)",
        title="18. The 15 actors with the most combined box office",
        md=(
            "**What we are doing.** A CTE sums the revenue of every movie an actor "
            "appears in (cast joined to movie), then we take the Top 15 by total "
            "box office. Note this double-counts ensemble films, which is typical "
            "for star-power rankings.\n\n"
            "**Concept:** CTE + multi-table JOIN + `SUM` aggregation + Top-N."
        ),
        sql=(
            "WITH actor_rev AS (\n"
            "    SELECT p.person_name AS actor,\n"
            "           SUM(m.revenue) AS total_revenue,\n"
            "           COUNT(*)       AS movies\n"
            "    FROM movie_cast mc\n"
            "    JOIN person p ON p.person_id = mc.person_id\n"
            "    JOIN movie m  ON m.movie_id  = mc.movie_id\n"
            "    WHERE m.revenue > 0\n"
            "    GROUP BY p.person_name\n"
            ")\n"
            "SELECT actor, total_revenue, movies\n"
            "FROM actor_rev\n"
            "ORDER BY total_revenue DESC\n"
            "LIMIT 15;"
        ),
        plot=dict(kind="barh", cat="actor", val="total_revenue",
                  title="15 actors with the most combined box office",
                  xlabel="Total box office (US$)"),
    ),
    dict(
        id="p19_top_actor_per_gender",
        section="C. Ten intermediate+ queries (Top-N, window functions, CTEs)",
        title="19. The 3 most prolific actors of each gender",
        md=(
            "**What we are doing.** Two stacked CTEs: the first counts credits per "
            "(gender, actor); the second applies `RANK() OVER (PARTITION BY "
            "gender ORDER BY movies DESC)`. We keep the top 3 of each gender.\n\n"
            "**Concept:** chained CTEs + `RANK()` partitioned Top-N."
        ),
        sql=(
            "WITH counts AS (\n"
            "    SELECT gd.gender   AS gender,\n"
            "           p.person_name AS actor,\n"
            "           COUNT(*)    AS movies\n"
            "    FROM movie_cast mc\n"
            "    JOIN person p  ON p.person_id = mc.person_id\n"
            "    JOIN gender gd ON gd.gender_id = mc.gender_id\n"
            "    GROUP BY gd.gender, p.person_name\n"
            "),\n"
            "ranked AS (\n"
            "    SELECT gender, actor, movies,\n"
            "           RANK() OVER (PARTITION BY gender ORDER BY movies DESC) AS rnk\n"
            "    FROM counts\n"
            ")\n"
            "SELECT gender, actor, movies\n"
            "FROM ranked\n"
            "WHERE rnk <= 3\n"
            "ORDER BY gender, movies DESC;"
        ),
        plot=None,
    ),
    dict(
        id="p20_yoy_change",
        section="C. Ten intermediate+ queries (Top-N, window functions, CTEs)",
        title="20. Year-over-year change in movies released",
        md=(
            "**What we are doing.** A CTE counts movies per year; then `LAG(n)` "
            "looks at the previous year's count so we can compute the year-over-year "
            "delta. `LAG` is the window function for \"the value in the row "
            "before.\"\n\n"
            "**Concept:** CTE + `LAG() OVER (ORDER BY ...)` for period-over-period "
            "change."
        ),
        sql=(
            "WITH per_year AS (\n"
            "    SELECT year(release_date) AS yr,\n"
            "           COUNT(*) AS n\n"
            "    FROM movie\n"
            "    WHERE release_date IS NOT NULL\n"
            "    GROUP BY yr\n"
            ")\n"
            "SELECT yr,\n"
            "       n,\n"
            "       n - LAG(n) OVER (ORDER BY yr) AS yoy_change\n"
            "FROM per_year\n"
            "WHERE yr BETWEEN 1990 AND 2016\n"
            "ORDER BY yr;"
        ),
        plot=dict(kind="line", x="yr", y="yoy_change",
                  title="Year-over-year change in movies released",
                  xlabel="Year", ylabel="Change vs. previous year"),
    ),
]
