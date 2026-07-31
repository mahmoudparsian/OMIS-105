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
    # Notebook 1 — Building the `sales_db.duckdb` Database

    **Course:** OMIS 105 · Data Stories · Video Game Sales

    ## What this notebook does

    We start from a raw CSV scraped from vgchartz.com (`video_game_sales.csv`) and
    turn it into a clean, query-ready DuckDB database (`sales_db.duckdb`) containing
    a single table called **`sales`** with **no duplicate rows**.

    The steps follow the assignment exactly:

    1. **2.0** — Normalize column names to lowercase `snake_case` (no spaces).
    2. **2.1** — Identify and *display* all duplicate rows.
    3. **2.2** — Delete the duplicate rows.
    4. **2.3** — Store the result as a single `sales` table in `sales_db.duckdb`.
    5. **2.4** — Verify, in SQL, that the database has no duplicates.

    Each cell explains *what* we are doing and *why* before showing the code and result.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 0 — Setup and imports

    We use three tools:

    - **pandas** to read the CSV and do the row-level cleaning,
    - **duckdb** to create and query the on-disk database, and
    - **util_plot** (our own helper module) so that *plotting code stays out of the
      notebook* — every chart is one tidy function call. This keeps each cell focused
      on a single idea.
    """)
    return


@app.cell
def _():
    import os
    from pathlib import Path

    import duckdb
    import pandas as pd

    import util_plot as up   # local helper: all matplotlib code lives here

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 140)

    # Resolve paths relative to this notebook so it runs anywhere.
    BASE_DIR = Path.cwd()
    CSV_PATH = BASE_DIR / 'video_game_sales.csv'
    DB_PATH  = BASE_DIR / 'sales_db.duckdb'

    print('DuckDB version :', duckdb.__version__)
    print('CSV file       :', CSV_PATH.name, '->', 'found' if CSV_PATH.exists() else 'MISSING')
    return (CSV_PATH, DB_PATH, duckdb, os, pd, up)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1 — Load the raw CSV

    We read the file straight into a pandas DataFrame and take a first look at its
    shape and a few rows. The raw file has one header row and ~16,600 game records.
    Each row is a single game *release on a specific platform* — so the same game can
    appear more than once (e.g. on PS3 and on X360).
    """)
    return


@app.cell
def _(CSV_PATH, pd):
    raw = pd.read_csv(CSV_PATH)

    print(f'Rows: {raw.shape[0]:,}   Columns: {raw.shape[1]}')
    print('Original column names:', list(raw.columns))
    raw.head()
    return (raw,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2.0 — Normalize column names to `snake_case`

    **What we are doing:** converting every column name to lowercase words separated
    by underscores, with no spaces. This is the standard for SQL and Python because
    it lets us write `na_sales` instead of quoting `"NA_Sales"` in every query.

    Our small `to_snake()` helper handles all three cases that can appear in messy
    headers: spaces/hyphens become underscores, `CamelCase` boundaries get an
    underscore inserted, and everything is lowercased. So `NA_Sales` becomes
    `na_sales` and a hypothetical `Global Sales` would become `global_sales`.
    """)
    return


@app.cell
def _(pd, raw):
    import re

    def to_snake(name: str) -> str:
        """Convert any column header to lowercase snake_case."""
        name = name.strip()
        name = re.sub(r'[ \-]+', '_', name)              # spaces / hyphens -> _
        name = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name)  # camelCase -> camel_Case
        name = re.sub(r'_+', '_', name)                   # collapse repeats
        return name.lower()

    before = list(raw.columns)
    raw.columns = [to_snake(c) for c in raw.columns]
    after = list(raw.columns)

    pd.DataFrame({'original': before, 'snake_case': after})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2.1 — Identify all duplicate rows

    **What we are doing:** finding rows that are genuine duplicates.

    There is one subtlety worth teaching here. The first column, `rank`, is just a
    running sales ranking — a *surrogate id* that is unique on every row. So if we
    ask pandas for rows that are identical across **all** columns, we get **zero**,
    because `rank` always differs.

    A *true* duplicate is a row that repeats the same game data — identical in every
    column **except** the `rank` id. So we look for duplicates on every column other
    than `rank`. The cell below shows both checks, then displays the offending rows.
    """)
    return


@app.cell
def _(raw):
    key_cols = [c for c in raw.columns if c != 'rank']  # every column except the id

    fully_identical = raw.duplicated(keep=False).sum()
    true_dupes      = raw.duplicated(subset=key_cols, keep=False)

    print(f'Rows identical across ALL columns (incl. rank): {fully_identical}')
    print(f'Rows that duplicate another (ignoring rank)   : {true_dupes.sum()}')
    print()
    print('The duplicate row(s):')
    raw[true_dupes].sort_values(key_cols)
    return (key_cols,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Reading the result.** The pair of `Wii de Asobu: Metroid Prime` rows are
    > identical in every field except `rank` — a real duplicate. (Note: a game like
    > *Madden NFL 13* may appear twice on the same platform/year, but with *different*
    > sales numbers — that is **not** a duplicate, just two records, so we correctly
    > leave it alone.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2.2 — Delete the duplicate rows

    **What we are doing:** keeping the *first* occurrence of each duplicated game and
    dropping the rest. We dedupe on `key_cols` (everything except `rank`) so the
    surrogate id never hides a real duplicate. We print the row count before and after
    so the change is auditable.
    """)
    return


@app.cell
def _(key_cols, raw):
    n_before = len(raw)
    clean = raw.drop_duplicates(subset=key_cols, keep='first').reset_index(drop=True)
    n_after = len(clean)

    print(f'Rows before : {n_before:,}')
    print(f'Rows after  : {n_after:,}')
    print(f'Removed      : {n_before - n_after}')
    print(f'Duplicates remaining: {clean.duplicated(subset=key_cols).sum()}')
    return (clean,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2.3 — Build `sales_db.duckdb` with a single `sales` table

    **What we are doing:** writing the cleaned DataFrame into an on-disk DuckDB
    database as one table named `sales`.

    While creating the table we make one small type improvement: `year` arrived as a
    float (because pandas stores missing years as `NaN`). We cast it to a nullable
    `INTEGER` so years read as `2006`, not `2006.0`, and missing years become `NULL`.

    ### "Do we need another table for the sales columns?"

    **Short answer: no.** The four regional columns — `na_sales`, `eu_sales`,
    `jp_sales`, `other_sales` (plus `global_sales`) — are all *measurements of the
    same row*: one game on one platform. They are attributes at the same grain, not a
    separate entity, so they belong in the same table. Splitting them out would force
    a join on every query for no benefit — that is over-normalization for a teaching
    dataset. We therefore keep a **single wide `sales` table**, exactly as the
    assignment specifies. (In Notebook 2 we can build a *view* that reshapes the four
    regions into long form when a particular chart needs it — without changing the
    base table.)
    """)
    return


@app.cell
def _(DB_PATH, clean, duckdb, os):
    # Start fresh so the notebook is re-runnable.
    if DB_PATH.exists():
        os.remove(DB_PATH)

    con = duckdb.connect(str(DB_PATH))
    con.register('clean_df', clean)   # expose the DataFrame to SQL

    con.execute("""
        CREATE
        OR REPLACE TABLE sales AS
        SELECT
            CAST(RANK AS INTEGER) AS rank,
            name,
            platform,
            TRY_CAST(year AS INTEGER) AS year,
            /* 2006.0 -> 2006, NaN -> NULL */ genre,
            publisher,
            na_sales,
            eu_sales,
            jp_sales,
            other_sales,
            global_sales
        FROM clean_df;
    """)

    con.unregister('clean_df')

    row_count = con.sql("""
        SELECT COUNT(*) AS n
        FROM sales;
    """).fetchone()[0]
    print(f'Table "sales" created with {row_count:,} rows.')
    con.sql("""
        DESCRIBE sales;
    """).df()
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2.4 — Verify (in SQL) that the database has no duplicates

    **What we are doing:** trusting but verifying — this time *inside DuckDB*. We
    group by every column except `rank` and keep only groups that appear more than
    once. DuckDB's `GROUP BY ALL` groups by all selected non-aggregated columns, and
    it treats `NULL` years as equal to one another (which is what we want, since the
    Metroid Prime duplicate had a missing year). An empty result means **zero
    duplicates** — the database is clean.
    """)
    return


@app.cell
def _(con):
    dupe_check = con.sql("""
        SELECT
            name,
            platform,
            year,
            genre,
            publisher,
            na_sales,
            eu_sales,
            jp_sales,
            other_sales,
            global_sales,
            COUNT(*) AS copies
        FROM sales
        GROUP BY ALL
        HAVING COUNT(*) > 1
        ORDER BY copies DESC;
    """).df()

    print(f'Duplicate groups found in the database: {len(dupe_check)}')
    if len(dupe_check) == 0:
        print('PASS - sales_db.duckdb contains no duplicate rows.')
    dupe_check
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3 — A quick sanity-check chart

    To confirm the table looks sensible, we run one small SQL query and plot it with
    our decoupled helper. This is also a preview of the Notebook 1 → Notebook 2
    pattern: **query in SQL, plot via `util_plot`.** Here: how many games were
    released per year.
    """)
    return


@app.cell
def _(con, up):
    games_per_year = con.sql("""
        SELECT
            year,
            COUNT(*) AS games
        FROM sales
        WHERE year IS NOT NULL
        GROUP BY year
        ORDER BY year;
    """).df()

    up.line(games_per_year, x='year', y='games',
            title='Number of game releases per year',
            xlabel='Year', ylabel='Games released')
    games_per_year.tail()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    We have:

    - normalized all column names to `snake_case` (Step 2.0),
    - identified the one true duplicate row and displayed it (Step 2.1),
    - removed it, going from 16,598 to 16,597 rows (Step 2.2),
    - written a single clean `sales` table into `sales_db.duckdb` (Step 2.3), and
    - verified in SQL that no duplicates remain (Step 2.4).

    The database is now ready for **Notebook 2**, where we use `sales_db.duckdb` to
    teach SQL through a graded series of queries.
    """)
    return


@app.cell
def _(con):
    con.close()
    print('Connection closed. sales_db.duckdb is ready.')
    return


if __name__ == "__main__":
    app.run()
