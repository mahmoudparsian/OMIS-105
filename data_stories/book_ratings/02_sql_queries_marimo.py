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
    # Notebook 2 — Teaching SQL with DuckDB (`books_db.duckdb`)

    **Course:** OMIS 105 · Data Stories · *Book Ratings*

    This notebook teaches SQL through a guided tour of queries that get progressively
    harder, all run against the clean database built in Notebook 1.

    **Tables**

    | table | grain | key columns |
    |-------|-------|-------------|
    | `books` | one row per book | `id` (1–10000), `book_id`, `title`, `authors`, `average_rating`, `ratings_count`, `ratings_1`…`ratings_5`, `original_publication_year`, `language_code` |
    | `ratings` | one row per (book, user) rating | `book_id`, `user_id`, `rating` (1–5) |

    **Important join key:** `ratings.book_id = books.id`.
    (`ratings.book_id` runs 1–10000, matching `books.id` — *not* the large Goodreads `books.book_id`.)

    **Roadmap**

    - **3.0** Add useful derived columns.
    - **3.1** 5 simple queries — `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`.
    - **3.2** 5 simple+ queries — `GROUP BY`, aggregates, expressions.
    - **3.3** 5 intermediate queries — `JOIN`, `HAVING`, scalar subqueries.
    - **3.4** 1 query — books **not rated by anyone** (`LEFT JOIN` anti-join).
    - **3.5** 5 intermediate+ queries — Top-N, window/ranking functions, `WITH` (CTEs).

    Every step follows the same pattern: **explain → formatted SQL → result table → plot** (plots live in `util_plot.py`).
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
    import util_plot as up

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 140)

    con = duckdb.connect("books_db.duckdb")
    print("Connected. Tables:", [t[0] for t in con.execute("SHOW TABLES").fetchall()])
    return con, up


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.0 — Add derived columns

    Some questions are easier to ask if we precompute a few helper columns on `books`.
    We add:

    - **`num_star_ratings`** — total number of individual star ratings, `ratings_1 + … + ratings_5`.
    - **`pct_favorable`** — share of 4- and 5-star ratings (a "how well-loved" measure).
    - **`rating_spread`** — `ratings_5 − ratings_1`, a rough sign of polarization.
    - **`publication_decade`** — the decade of `original_publication_year`.

    We rebuild `books` with these columns appended (safe to re-run).
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE OR REPLACE TABLE books AS
        SELECT
            *,
            (ratings_1 + ratings_2 + ratings_3 + ratings_4 + ratings_5)            AS num_star_ratings,
            ROUND( (ratings_4 + ratings_5) * 1.0
                   / NULLIF(ratings_1 + ratings_2 + ratings_3 + ratings_4 + ratings_5, 0), 3) AS pct_favorable,
            (ratings_5 - ratings_1)                                                AS rating_spread,
            CAST(FLOOR(original_publication_year / 10) * 10 AS INTEGER)            AS publication_decade
        FROM books
    """)
    con.execute("SELECT id, title, num_star_ratings, pct_favorable, rating_spread, publication_decade FROM books LIMIT 5").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.1 — Five simple queries

    Foundational single-table queries: choosing columns, filtering rows, sorting, limiting.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1.1 — Preview the catalog
    Select a few readable columns for the first 10 books. `SELECT` chooses columns; `LIMIT` caps rows.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT id, title, authors, average_rating\nFROM books\nORDER BY id\nLIMIT 10\n'
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1.2 — How many books are in the catalog?
    `COUNT(*)` counts rows. This is the cleaned total from Notebook 1.
    """)
    return


@app.cell
def _(con):
    con.execute("SELECT COUNT(*) AS n_books FROM books").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1.3 — Recent books (published after 2010)
    `WHERE` filters rows; we sort newest first.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT title, authors, original_publication_year, average_rating\nFROM books\nWHERE original_publication_year > 2010\nORDER BY original_publication_year DESC, average_rating DESC\nLIMIT 15\n'
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1.4 — What languages appear?
    `DISTINCT` removes repeats; we list the language codes present.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT DISTINCT language_code
        FROM books
        WHERE language_code IS NOT NULL
        ORDER BY language_code
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1.5 — Highest-rated books
    Order by `average_rating` and keep the top 10. We require a reasonable number of
    ratings so a single 5-star book doesn't dominate.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT title, authors, average_rating, ratings_count\nFROM books\nWHERE ratings_count >= 10000\nORDER BY average_rating DESC\nLIMIT 10\n'
    df = con.execute(_sql).df()
    df
    return (df,)


@app.cell
def _(df, up):
    _fig = up.barh(df, x='average_rating', y='title', title='Top 10 highest-rated books (≥ 10k ratings)', xlabel='average rating', value_fmt='{:.2f}')
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.2 — Five simple+ queries

    Now we aggregate with `GROUP BY` and summary functions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.1 — Number of books per language
    `GROUP BY` collapses rows into one per language; `COUNT(*)` sizes each group.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT language_code, COUNT(*) AS n_books\nFROM books\nWHERE language_code IS NOT NULL\nGROUP BY language_code\nORDER BY n_books DESC\nLIMIT 12\n'
    df_1 = con.execute(_sql).df()
    df_1
    return (df_1,)


@app.cell
def _(df_1, up):
    _fig = up.bar(df_1, x='language_code', y='n_books', title='Books per language (top 12)', ylabel='# books', rotate=45)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.2 — Rating summary statistics
    A single row of `MIN`, `MAX`, `AVG`, and standard deviation over `average_rating`.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            ROUND(MIN(average_rating), 2)   AS min_rating,
            ROUND(AVG(average_rating), 3)   AS avg_rating,
            ROUND(MAX(average_rating), 2)   AS max_rating,
            ROUND(STDDEV(average_rating), 3) AS sd_rating
        FROM books
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.3 — Most prolific authors
    `GROUP BY authors` then count titles. (The `authors` field can list co-authors; we treat
    each distinct string as one entry.)
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT authors, COUNT(*) AS n_books, ROUND(AVG(average_rating), 2) AS avg_rating\nFROM books\nGROUP BY authors\nORDER BY n_books DESC\nLIMIT 10\n'
    df_2 = con.execute(_sql).df()
    df_2
    return (df_2,)


@app.cell
def _(df_2, up):
    _fig = up.barh(df_2, x='n_books', y='authors', title='Most prolific authors (by # books)', xlabel='# books')
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.4 — Books published per decade
    Uses the derived `publication_decade`. Filtered to plausible decades.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT publication_decade, COUNT(*) AS n_books\nFROM books\nWHERE publication_decade BETWEEN 1900 AND 2020\nGROUP BY publication_decade\nORDER BY publication_decade\n'
    df_3 = con.execute(_sql).df()
    df_3
    return (df_3,)


@app.cell
def _(df_3, up):
    _fig = up.bar(df_3, x='publication_decade', y='n_books', title='Books published per decade', xlabel='decade', ylabel='# books', rotate=45)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.5 — Average rating by decade
    Combines a `GROUP BY` with an `AVG`, showing how average ratings drift over time.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT publication_decade,\n       COUNT(*)                       AS n_books,\n       ROUND(AVG(average_rating), 3)  AS avg_rating\nFROM books\nWHERE publication_decade BETWEEN 1900 AND 2020\nGROUP BY publication_decade\nHAVING COUNT(*) >= 20\nORDER BY publication_decade\n'
    df_4 = con.execute(_sql).df()
    df_4
    return (df_4,)


@app.cell
def _(df_4, up):
    _fig = up.line(df_4, x='publication_decade', y='avg_rating', title='Average rating by publication decade', xlabel='decade', ylabel='avg rating')
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.3 — Five intermediate queries

    These bring in the **`ratings`** table via `JOIN`, plus `HAVING` and scalar subqueries.
    Remember the join: `ratings.book_id = books.id`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.3.1 — Most-rated books (by number of ratings received)
    We count rows in `ratings` per book, then join to `books` for titles.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT b.title, b.authors, COUNT(*) AS ratings_received\nFROM ratings r\nJOIN books b ON r.book_id = b.id\nGROUP BY b.title, b.authors\nORDER BY ratings_received DESC\nLIMIT 10\n'
    df_5 = con.execute(_sql).df()
    df_5
    return (df_5,)


@app.cell
def _(df_5, up):
    _fig = up.barh(df_5, x='ratings_received', y='title', title='Most-rated books (count of ratings in the ratings table)', xlabel='# ratings received')
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.3.2 — Stored vs. observed average rating
    `books.average_rating` is precomputed; here we compute the average of the actual
    `rating` values in `ratings` and compare. A `JOIN` + `GROUP BY` per book.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT b.title,\n       b.average_rating                 AS stored_avg,\n       ROUND(AVG(r.rating), 2)          AS observed_avg,\n       COUNT(*)                         AS n_ratings\nFROM ratings r\nJOIN books b ON r.book_id = b.id\nGROUP BY b.title, b.average_rating\nORDER BY n_ratings DESC\nLIMIT 10\n'
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.3.3 — Authors whose books beat the overall average
    A **scalar subquery** computes the global mean rating; `HAVING` keeps authors above it.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT authors,\n       COUNT(*)                       AS n_books,\n       ROUND(AVG(average_rating), 3)  AS avg_rating\nFROM books\nGROUP BY authors\nHAVING AVG(average_rating) > (SELECT AVG(average_rating) FROM books)\n   AND COUNT(*) >= 5\nORDER BY avg_rating DESC\nLIMIT 10\n'
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.3.4 — Average rating given by the busiest users
    Which users rate the most books, and how generously? Aggregates on `ratings` alone.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT user_id,\n       COUNT(*)                 AS books_rated,\n       ROUND(AVG(rating), 2)    AS avg_rating_given\nFROM ratings\nGROUP BY user_id\nORDER BY books_rated DESC\nLIMIT 10\n'
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.3.5 — Distribution of star ratings
    Across all 980k ratings, how many of each star value were given? `GROUP BY rating`.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT rating, COUNT(*) AS n\nFROM ratings\nGROUP BY rating\nORDER BY rating\n'
    df_6 = con.execute(_sql).df()
    df_6
    return (df_6,)


@app.cell
def _(df_6, up):
    _fig = up.bar(df_6, x='rating', y='n', title='How many ratings of each star value?', xlabel='star rating', ylabel='# ratings', value_labels=False)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.4 — Books **not rated by anyone**

    A classic **anti-join**: `LEFT JOIN` `books` to `ratings` and keep books whose match is
    `NULL` (no ratings exist). Because every clean book (id 1–10000) has ratings, the only
    rows returned are the **7 salvaged "dirty" rows** (ids 19986–19992) left over from the
    malformed input — a nice demonstration that anti-joins also surface data-quality issues.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT b.id, b.book_id, b.title, b.authors\nFROM books b\nLEFT JOIN ratings r ON r.book_id = b.id\nWHERE r.book_id IS NULL\nORDER BY b.id\n'
    df_7 = con.execute(_sql).df()
    print(f'Books with zero ratings: {len(df_7)}')
    df_7
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.5 — Five intermediate+ queries

    Top-N, **window / ranking functions**, and **`WITH` (CTEs)** — the workhorses of analytical SQL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.5.1 — Top 3 books per language (window `ROW_NUMBER`)
    We rank books within each `language_code` by `average_rating` using a window function,
    then keep the top 3 per group with `QUALIFY`.
    """)
    return


@app.cell
def _(con):
    _sql = '\nSELECT language_code, title, average_rating, ratings_count\nFROM books\nWHERE language_code IS NOT NULL AND ratings_count >= 5000\nQUALIFY ROW_NUMBER() OVER (\n            PARTITION BY language_code\n            ORDER BY average_rating DESC\n        ) <= 3\nORDER BY language_code, average_rating DESC\n'
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.5.2 — Rank authors by total ratings received (`WITH` + `RANK`)
    A CTE aggregates ratings per author; an outer `RANK()` orders them.
    """)
    return


@app.cell
def _(con):
    _sql = '\nWITH author_totals AS (\n    SELECT b.authors,\n           COUNT(*) AS total_ratings\n    FROM ratings r\n    JOIN books b ON r.book_id = b.id\n    GROUP BY b.authors\n)\nSELECT RANK() OVER (ORDER BY total_ratings DESC) AS rnk,\n       authors,\n       total_ratings\nFROM author_totals\nORDER BY rnk\nLIMIT 10\n'
    df_8 = con.execute(_sql).df()
    df_8
    return (df_8,)


@app.cell
def _(df_8, up):
    _fig = up.barh(df_8, x='total_ratings', y='authors', title='Authors ranked by total ratings received', xlabel='# ratings')
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.5.3 — Each book's rank within its decade (`DENSE_RANK`)
    Within every `publication_decade`, rank books by `average_rating`; show the top 2 per decade.
    """)
    return


@app.cell
def _(con):
    _sql = '\nWITH ranked AS (\n    SELECT publication_decade, title, average_rating,\n           DENSE_RANK() OVER (\n               PARTITION BY publication_decade\n               ORDER BY average_rating DESC\n           ) AS rnk_in_decade\n    FROM books\n    WHERE publication_decade BETWEEN 1950 AND 2020\n      AND ratings_count >= 5000\n)\nSELECT publication_decade, rnk_in_decade, title, average_rating\nFROM ranked\nWHERE rnk_in_decade <= 2\nORDER BY publication_decade, rnk_in_decade\n'
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.5.4 — Popularity quartiles (`NTILE`)
    `NTILE(4)` splits books into four equal buckets by `ratings_count`. We then summarize
    each quartile — showing how lopsided book popularity is.
    """)
    return


@app.cell
def _(con):
    _sql = '\nWITH bucketed AS (\n    SELECT title, ratings_count,\n           NTILE(4) OVER (ORDER BY ratings_count) AS popularity_quartile\n    FROM books\n)\nSELECT popularity_quartile,\n       COUNT(*)                         AS n_books,\n       MIN(ratings_count)               AS min_ratings,\n       MAX(ratings_count)               AS max_ratings,\n       CAST(AVG(ratings_count) AS BIGINT) AS avg_ratings\nFROM bucketed\nGROUP BY popularity_quartile\nORDER BY popularity_quartile\n'
    df_9 = con.execute(_sql).df()
    df_9
    return (df_9,)


@app.cell
def _(df_9, up):
    _fig = up.bar(df_9, x='popularity_quartile', y='avg_ratings', title='Average ratings_count by popularity quartile (NTILE)', xlabel='quartile (1 = least popular)', ylabel='avg ratings_count')
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.5.5 — Top-N with a share-of-total (`WITH` + window total)
    For the 10 most-rated books, also show each one's **percentage of all ratings** using a
    window `SUM() OVER ()` as the denominator.
    """)
    return


@app.cell
def _(con):
    _sql = '\nWITH per_book AS (\n    SELECT b.title,\n           COUNT(*) AS ratings_received\n    FROM ratings r\n    JOIN books b ON r.book_id = b.id\n    GROUP BY b.title\n)\nSELECT title,\n       ratings_received,\n       ROUND(100.0 * ratings_received / SUM(ratings_received) OVER (), 2) AS pct_of_all_ratings\nFROM per_book\nORDER BY ratings_received DESC\nLIMIT 10\n'
    con.execute(_sql).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Wrap-up

    We progressed from single-table `SELECT`s to multi-table `JOIN`s, aggregates, anti-joins,
    and window/CTE analytics — the core toolkit of analytical SQL.

    **Concepts demonstrated:** `SELECT` / `WHERE` / `ORDER BY` / `LIMIT` · `DISTINCT` ·
    `GROUP BY` / `HAVING` · aggregate functions (`COUNT`, `AVG`, `MIN`, `MAX`, `STDDEV`) ·
    derived columns · scalar subqueries · `JOIN` and `LEFT JOIN` anti-joins ·
    window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, `SUM() OVER`) ·
    `QUALIFY` · common table expressions (`WITH`).
    """)
    return


@app.cell
def _(con):
    con.close()
    print("Done. Connection closed.")
    return


if __name__ == "__main__":
    app.run()
