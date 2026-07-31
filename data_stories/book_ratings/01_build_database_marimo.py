import marimo

__generated_with = "0.23.8"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook 1 — Build the DuckDB Database (`books_db.duckdb`)

    **Course:** OMIS 105 · Data Stories · *Book Ratings*

    This notebook performs the **ETL** (Extract, Transform, Load) step:

    1. **2.0** Read `books.csv` and `ratings.csv`; normalize column names to lowercase, underscore-separated (no spaces).
    2. **2.1** Identify and **display** all duplicate rows.
    3. **2.2 / 2.3** Delete the duplicate rows so the database contains none.
    4. **2.4** Verify that no duplicate rows remain.

    The result is a clean database, `books_db.duckdb`, with two tables: `books` and `ratings`.

    > Plotting code is kept out of this notebook — it lives in `util_plot.py`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    We use **DuckDB** (a fast, file-based analytical SQL engine) as our database, and
    pandas only to display query results as tidy tables.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import util_plot as up

    pd.set_option("display.max_columns", None)
    print("DuckDB version:", duckdb.__version__)
    return duckdb, pd, up


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.0 — Read the CSVs and create the database

    We connect to (and create) the database file `books_db.duckdb`, then load each CSV
    with DuckDB's `read_csv`.

    **A note on messy data in `books.csv`.** The file contains a handful of *malformed*
    rows that carry an extra comma-separated field (24 fields instead of the expected 23).
    We load with `ignore_errors=true` so DuckDB skips these corrupt rows automatically,
    and we report how many were skipped. `ratings.csv` is well-formed.
    """)
    return


@app.cell
def _(duckdb):
    con = duckdb.connect("books_db.duckdb")

    # --- books: tolerant load 
    # (skips malformed rows with the wrong field count) ---

    con.execute("""
        CREATE OR REPLACE TABLE books AS
        SELECT * FROM read_csv('books.csv', header=true, ignore_errors=true)
    """)

    # --- ratings: clean, strongly-typed load ---
    con.execute("""
        CREATE OR REPLACE TABLE ratings AS
        SELECT * FROM read_csv('ratings.csv', header=true)
    """)

    n_books = con.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    n_ratings = con.execute("SELECT COUNT(*) FROM ratings").fetchone()[0]
    print(f"Loaded books   rows: {n_books:,}")
    print(f"Loaded ratings rows: {n_ratings:,}")
    return con, n_books, n_ratings


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How many rows were skipped as malformed?

    We compare the number of data lines physically present in `books.csv` against the
    number of rows DuckDB actually loaded.
    """)
    return


@app.cell
def _(n_books):
    with open("books.csv") as f:
        file_data_lines = sum(1 for _ in f) - 1   # minus the header line

    skipped = file_data_lines - n_books
    print(f"Data lines in books.csv : {file_data_lines:,}")
    print(f"Rows loaded into 'books': {n_books:,}")
    print(f"Malformed rows skipped  : {skipped:,}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.0 (cont.) — Normalize column names

    Requirement: column names must be **lowercase**, words separated by **underscores**,
    and contain **no spaces**. We apply a small, reusable normalizer to every column of
    both tables. (Most columns already follow this convention; the normalizer guarantees
    it and is safe to re-run.)
    """)
    return


@app.cell
def _(con):
    def normalize_columns(con, table):
        """Rename every column of `table` to lowercase, underscore-separated, no spaces."""
        cols = con.execute(f"PRAGMA table_info('{table}')").df()["name"].tolist()
        for c in cols:
            new = "_".join(c.strip().lower().split())   
            # collapses spaces -> single _
            while "__" in new:
                new = new.replace("__", "_")
            if new != c:
                con.execute(f'ALTER TABLE {table} RENAME COLUMN "{c}" TO "{new}"')
        return con.execute(f"PRAGMA table_info('{table}')").df()["name"].tolist()

    print("books columns :", normalize_columns(con, "books"))
    print("ratings columns:", normalize_columns(con, "ratings"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.1 — Identify and display duplicate rows

    A **duplicate row** is a row whose values are identical across **all** columns to
    another row. In DuckDB, `GROUP BY ALL ... HAVING COUNT(*) > 1` finds them.

    ### Duplicates in `books`
    """)
    return


@app.cell
def _(con):
    book_dups = con.execute("""
        SELECT id, 
               book_id, 
               title, 
               authors, 
               COUNT(*) AS n_copies
        FROM books
        GROUP BY ALL
        HAVING COUNT(*) > 1
        ORDER BY id
    """).df()

    print(f"Distinct rows that are duplicated in 'books': {len(book_dups)}")
    print(f"Extra (removable) copies: {int(book_dups['n_copies'].sum() - len(book_dups))}")
    book_dups
    return (book_dups,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Duplicates in `ratings`

    `ratings` has many duplicated `(book_id, user_id, rating)` rows. We display a sample
    and summarize the totals.
    """)
    return


@app.cell
def _(con):
    rating_dups = con.execute("""
        SELECT book_id, 
               user_id, 
               rating, 
               COUNT(*) AS n_copies
        FROM ratings
        GROUP BY ALL
        HAVING COUNT(*) > 1
        ORDER BY n_copies DESC, book_id
    """).df()

    extra_copies = int(rating_dups["n_copies"].sum() - len(rating_dups))
    print(f"Distinct rows that are duplicated in 'ratings': {len(rating_dups):,}")
    print(f"Extra (removable) copies: {extra_copies:,}")
    rating_dups.head(10)
    return (extra_copies,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Visualize the duplication

    A quick view of how many extra duplicate copies each table carries.
    """)
    return


@app.cell
def _(book_dups, extra_copies, pd, up):
    summary = pd.DataFrame({
        "table": ["books", "ratings"],
        "extra_duplicate_copies": [
            int(book_dups["n_copies"].sum() - len(book_dups)),
            extra_copies,
        ],
    })
    fig = up.bar(summary, x="table", y="extra_duplicate_copies",
                 title="Extra duplicate copies before cleaning",
                 ylabel="# extra copies", value_labels=True)
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.2 / 2.3 — Delete the duplicate rows

    We rebuild each table from its **`DISTINCT`** rows. This keeps exactly one copy of
    every unique row and drops all redundant duplicates, so the saved database has none.
    """)
    return


@app.function
def dedup_table(con, table_name):
    # 1. Create a new table with only unique rows
    con.execute(f"CREATE OR REPLACE TABLE {table_name}_deduped AS SELECT DISTINCT * FROM {table_name};")

    # 2. Drop the original table
    con.execute(f"DROP TABLE {table_name};")


    # 3. Rename the deduplicated table to the original name
    con.execute(f"ALTER TABLE {table_name}_deduped RENAME TO {table_name};")


@app.cell
def _(con, n_books, n_ratings):
    # dedup books
    dedup_table(con, "books")   

    # dedup ratings
    dedup_table(con, "ratings")


    n_books2   = con.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    n_ratings2 = con.execute("SELECT COUNT(*) FROM ratings").fetchone()[0]
    print(f"books  : {n_books:,} -> {n_books2:,}  (removed {n_books - n_books2:,})")
    print(f"ratings: {n_ratings:,} -> {n_ratings2:,}  (removed {n_ratings - n_ratings2:,})")

    # Flush changes to the .duckdb file so other connections (e.g. the CLI) see them
    con.execute("CHECKPOINT")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.4 — Verify that no duplicate rows remain

    We re-run the duplicate check on both cleaned tables. Both must return **0** rows.
    """)
    return


@app.cell
def _(con):
    books_left = con.execute("""
        SELECT COUNT(*) FROM (
            SELECT * FROM books GROUP BY ALL HAVING COUNT(*) > 1
        )""").fetchone()[0]

    ratings_left = con.execute("""
        SELECT COUNT(*) FROM (
            SELECT * FROM ratings GROUP BY ALL HAVING COUNT(*) > 1
        )""").fetchone()[0]

    print(f"Duplicate rows remaining in books  : {books_left}")
    print(f"Duplicate rows remaining in ratings: {ratings_left}")
    assert books_left == 0 and ratings_left == 0, "Duplicates still present!"
    print("\n[OK] Verified: the database contains no duplicate rows.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    `books_db.duckdb` now holds two clean tables:

    | table   | description                                  |
    |---------|----------------------------------------------|
    | `books` | one row per book (deduplicated, normalized)  |
    | `ratings` | one row per (book, user) rating (deduplicated) |

    Changes are persisted automatically by DuckDB. We close the connection below.

    **Next:** Notebook 2 teaches SQL queries against this database.
    """)
    return


@app.cell
def _(con):
    con.close()
    print("Connection closed. books_db.duckdb is ready.")
    return


if __name__ == "__main__":
    app.run()
