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
    # My Second DuckDB Notebook

    ### Building on the basics from Notebook 1

    ### In this notebook we will learn:

    1. **DISTINCT** — removing duplicates
    2. **WHERE** with multiple conditions (AND, OR, IN, BETWEEN, LIKE)
    3. **ORDER BY** with multiple columns
    4. **Aggregate functions** — COUNT, SUM, AVG, MIN, MAX
    5. **GROUP BY** — summarizing data by category
    6. **HAVING** — filtering groups
    7. **Aliases** — renaming columns with AS
    8. **NULL handling** — IS NULL, IS NOT NULL, COALESCE

    ### Dataset: a small bookstore inventory (12 rows)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 1 — Connect to DuckDB
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 2 — Create the `books` Table
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE books (
            book_id     INTEGER,
            title       VARCHAR,
            author      VARCHAR,
            genre       VARCHAR,
            price       DOUBLE,
            pages       INTEGER,
            rating      DOUBLE,
            year        INTEGER,
            in_stock    BOOLEAN
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO books VALUES
            (1,  'The Great Gatsby',       'F. Scott Fitzgerald', 'Fiction',     12.99, 180,  4.2, 1925, true),
            (2,  'To Kill a Mockingbird',  'Harper Lee',          'Fiction',     14.99, 281,  4.5, 1960, true),
            (3,  'A Brief History of Time','Stephen Hawking',     'Science',     18.50, 256,  4.6, 1988, true),
            (4,  '1984',                   'George Orwell',       'Fiction',     11.99, 328,  4.7, 1949, false),
            (5,  'The Art of War',         'Sun Tzu',             'History',      9.99,  68,  4.3, NULL, true),
            (6,  'Dune',                   'Frank Herbert',       'Sci-Fi',      15.99, 412,  4.5, 1965, true),
            (7,  'Sapiens',                'Yuval Noah Harari',   'History',     19.99, 443,  4.4, 2011, true),
            (8,  'The Hobbit',             'J.R.R. Tolkien',      'Fiction',     13.49, 310,  4.7, 1937, true),
            (9,  'Cosmos',                 'Carl Sagan',          'Science',     16.99, 365,  4.6, 1980, false),
            (10, 'Fahrenheit 451',         'Ray Bradbury',        'Sci-Fi',      10.99, 194,  4.4, 1953, true),
            (11, 'Educated',               'Tara Westover',       'Memoir',      16.49, 334,  4.7, 2018, true),
            (12, 'Thinking, Fast and Slow','Daniel Kahneman',     'Science',     17.99, 499,  4.1, 2011, false)
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * 
            FROM books 
            ORDER BY book_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 3 — SELECT DISTINCT

    `DISTINCT` removes duplicate values. How many different genres do we have?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT DISTINCT genre
            FROM books
            ORDER BY genre
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT COUNT(DISTINCT genre) AS num_genres
            FROM books
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 4 — Filtering with WHERE

    ### 4.1 Simple comparison
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT title, author, price
            FROM books
            WHERE price < 15.00
            ORDER BY price
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2 AND / OR — combining conditions
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT title, author, price, in_stock
            FROM books
            WHERE genre = 'Fiction'
              AND in_stock = true
            ORDER BY title
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT title, genre, price
            FROM books
            WHERE genre = 'Fiction'
               OR genre = 'Sci-Fi'
            ORDER BY genre, title
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.3 IN — matching a list

    `IN` is a cleaner way to check multiple values (instead of many `OR`s).
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT title, genre, price
            FROM books
            WHERE genre IN ('Fiction', 'Sci-Fi')
            ORDER BY genre, title
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.4 BETWEEN — range filtering
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT title, price
            FROM books
            WHERE price BETWEEN 12.00 AND 17.00
            ORDER BY price
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.5 LIKE — pattern matching

    - `%` matches any sequence of characters
    - `_` matches exactly one character
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT title, author
            FROM books
            WHERE title LIKE 'The%'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 5 — NULL Handling

    Notice that 'The Art of War' has `NULL` for its year. NULL means **unknown** — it's not zero, not empty, it's missing.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT title, author, year
            FROM books
            WHERE year IS NULL
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT title, author, year
            FROM books
            WHERE year IS NULL
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT title, year
            FROM books
            WHERE year IS NOT NULL
            ORDER BY year
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT title,
                   year,
                   COALESCE(year, 0) AS year_or_zero
            FROM books
            ORDER BY book_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 6 — ORDER BY with Multiple Columns

    You can sort by more than one column. The first column is the primary sort; ties are broken by the second.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT title, genre, price
            FROM books
            ORDER BY genre ASC, price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 7 — Aggregate Functions

    These collapse many rows into a single summary value.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                COUNT(*)              AS total_books,
                ROUND(AVG(price), 2)  AS avg_price,
                MIN(price)            AS cheapest,
                MAX(price)            AS most_expensive,
                ROUND(SUM(price), 2)  AS total_value,
                ROUND(AVG(rating), 2) AS avg_rating
            FROM books
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## COUNT() Function: count rows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## COUNT vs COUNT(column):
    #### `COUNT(*)` counts all rows,
    #### `COUNT(year)` counts only non-NULL values
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                COUNT(*)    AS total_rows,
                COUNT(year) AS rows_with_year
            FROM books
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 8 — GROUP BY

    `GROUP BY` splits data into groups, then applies an aggregate to each group.

    **Rule:** Every column in SELECT must be either (a) in the GROUP BY, or (b) inside an aggregate function.
    """)
    return


@app.cell
def _(con):
    # How many books per genre?
    df_genre = con.execute(
        f"""
        SELECT
            genre,
            COUNT(*) AS num_books
        FROM books
        GROUP BY genre
        ORDER BY num_books DESC
        """
    ).fetchdf()
    return (df_genre,)


@app.cell
def _(df_genre):
    # Plot: books per genre
    df_genre.plot(kind='bar', x='genre', y='num_books',
        title='Number of Books per Genre',
        xlabel='Genre', ylabel='Count',
        legend=False, rot=0)
    return


@app.cell
def _(con):
    # Average price and rating per genre
    df_stats = con.execute(
        f"""
        SELECT
            genre,
            COUNT(*)              AS num_books,
            ROUND(AVG(price), 2)  AS avg_price,
            ROUND(AVG(rating), 2) AS avg_rating,
            ROUND(SUM(price), 2)  AS total_value
        FROM books
        GROUP BY genre
        ORDER BY avg_price DESC
        """
    ).fetchdf()
    return (df_stats,)


@app.cell
def _(df_stats):
    # Plot: average price by genre
    df_stats.plot(kind='barh', x='genre', y='avg_price',
        title='Average Book Price by Genre',
        xlabel='Average Price ($)', ylabel='Genre',
        legend=False, color='coral')
    return


@app.cell
def _(con):
    # Books in stock vs out of stock
    df_stock = con.execute(
        f"""
        SELECT
            in_stock,
            COUNT(*)             AS num_books,
            ROUND(AVG(price), 2) AS avg_price
        FROM books
        GROUP BY in_stock
        ORDER BY in_stock DESC
        """
    ).fetchdf()
    return (df_stock,)


@app.cell
def _(df_stock):
    # Plot: in stock vs out of stock
    labels = ['In Stock' if v else 'Out of Stock' for v in df_stock['in_stock']]
    df_stock.plot(kind='pie', y='num_books', labels=labels,
        autopct='%1.0f%%', figsize=(5, 5),
        title='Book Availability', legend=False, ylabel='')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 9 — HAVING: Filtering Groups

    `WHERE` filters **rows** (before grouping).
    `HAVING` filters **groups** (after grouping).

    You cannot use `WHERE` with aggregate results — use `HAVING` instead.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                genre,
                COUNT(*)              AS num_books,
                ROUND(AVG(price), 2)  AS avg_price
            FROM books
            GROUP BY genre
            HAVING COUNT(*) > 1
            ORDER BY num_books DESC
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                genre,
                ROUND(AVG(price), 2) AS avg_price
            FROM books
            GROUP BY genre
            HAVING AVG(price) > 15.00
            ORDER BY avg_price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 10 — Aliases with AS

    `AS` renames a column in the output. You have already been using it! Here we make it explicit.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                title                          AS book_title,
                price                          AS retail_price,
                ROUND(price * 0.90, 2)         AS sale_price_10pct_off,
                pages                          AS total_pages,
                ROUND(price / pages * 100, 2)  AS cents_per_page
            FROM books
            ORDER BY cents_per_page DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 11 — Putting It All Together

    A single query that combines WHERE, GROUP BY, HAVING, ORDER BY, and aliases.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT
                genre                 AS category,
                COUNT(*)              AS books_available,
                ROUND(AVG(price), 2)  AS avg_price,
                ROUND(AVG(rating), 2) AS avg_rating
            FROM books
            WHERE in_stock = true
            GROUP BY genre
            HAVING COUNT(*) >= 2
            ORDER BY avg_rating DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Summary

    ### SQL Concepts Practiced

    | Concept | What It Does | Example |
    |---------|-------------|---------|
    | `DISTINCT` | Removes duplicates | `SELECT DISTINCT genre` |
    | `WHERE` | Filters rows | `WHERE price < 15` |
    | `AND / OR` | Combines conditions | `WHERE genre = 'Fiction' AND in_stock = true` |
    | `IN` | Matches a list | `WHERE genre IN ('Fiction', 'Sci-Fi')` |
    | `BETWEEN` | Range filter | `WHERE price BETWEEN 12 AND 17` |
    | `LIKE` | Pattern matching | `WHERE title LIKE 'The%'` |
    | `IS NULL` | Checks for missing data | `WHERE year IS NULL` |
    | `COALESCE` | Replaces NULL with default | `COALESCE(year, 0)` |
    | `ORDER BY` | Sorts results | `ORDER BY genre, price DESC` |
    | `COUNT, AVG, ...` | Aggregate functions | `AVG(price)` |
    | `GROUP BY` | Groups + aggregates | `GROUP BY genre` |
    | `HAVING` | Filters groups | `HAVING COUNT(*) > 1` |
    | `AS` | Column alias | `AVG(price) AS avg_price` |

    ### What's Next?

    In the **next notebook**, we'll cover:
    - **JOINs** — combining multiple tables
    - **Subqueries** and **CTEs** (WITH clauses)

    ---
    *Notebook by Professor M. Parsian — Santa Clara University*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    *Great work! You've completed the notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
