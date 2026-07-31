import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import duckdb
    import os
    return duckdb, mo, os


@app.cell
def __(mo):
    mo.md(
        r"""
        # 🎬 Notebook 1 — Build `netflix.duckdb`

        This notebook does three things:
        1. Reads `netflix_titles.csv` into DuckDB and persists it as `netflix.duckdb`
        2. Verifies every column name is **SQL-style snake_case** (lowercase, underscores)
        3. Runs a handful of **basic sanity-check queries** so we know the data loaded correctly

        > **Data source:** Kaggle — Netflix Movies and TV Shows
        > **Rows:** 8 809 titles  |  **Columns:** 12
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## Step 1 — Connect to (or create) `netflix.duckdb`")
    return


@app.cell
def __(duckdb, os):
    # Resolve path relative to this notebook's location
    _nb_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "."
    DB_PATH  = os.path.join(_nb_dir, "netflix.duckdb")
    CSV_PATH = os.path.join(_nb_dir, "netflix_titles.csv")

    # Open (or create) a persistent DuckDB database file
    con = duckdb.connect(DB_PATH)
    print(f"Connected to: {DB_PATH}")
    print(f"CSV source  : {CSV_PATH}")
    return CSV_PATH, DB_PATH, con


@app.cell
def __(mo):
    mo.md(
        """
        ## Step 2 — Load CSV and rename columns to snake_case

        The raw CSV from Kaggle already uses lowercase snake_case headers
        (`show_id`, `type`, `title`, …), so no renaming is required.
        We still run the canonical snake_case transform — turn any space,
        hyphen, or camelCase into underscored lowercase — so the notebook
        handles any future CSV that arrives with messy headers.

        **Transform rules:**
        - `"daysPassed"` → `"days_passed"`
        - `"days passed"` → `"days_passed"`
        - `"Listed-In"`  → `"listed_in"`
        """
    )
    return


@app.cell
def __(CSV_PATH, con):
    import re

    def to_snake(name: str) -> str:
        """Convert any column name to SQL-safe snake_case."""
        # Insert underscore before uppercase letters (camelCase → snake_case)
        s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
        # Replace spaces, hyphens, dots with underscores
        s = re.sub(r"[\s\-\.]+", "_", s)
        return s.lower().strip("_")

    # Read raw CSV headers
    raw = con.execute(f"SELECT * FROM read_csv_auto('{CSV_PATH}') LIMIT 0").description
    raw_cols = [d[0] for d in raw]
    snake_cols = [to_snake(c) for c in raw_cols]

    print("Column mapping (raw → snake_case):")
    for r, s in zip(raw_cols, snake_cols):
        arrow = "✓  (no change)" if r == s else f"→  {s}"
        print(f"  {r:20s}  {arrow}")

    return raw, raw_cols, re, snake_cols, to_snake


@app.cell
def __(CSV_PATH, con, snake_cols):
    # Build a SELECT with aliased columns so the table always has clean names
    _aliases = ", ".join(
        f'"{raw}" AS {snake}'
        for raw, snake in zip(
            [d[0] for d in con.execute(
                f"SELECT * FROM read_csv_auto('{CSV_PATH}') LIMIT 0"
            ).description],
            snake_cols,
        )
    )

    # Drop & recreate for idempotency (re-running this cell always gives a fresh table)
    con.execute("DROP TABLE IF EXISTS netflix_titles")
    con.execute(
        f"""
        CREATE TABLE netflix_titles AS
        SELECT {_aliases}
        FROM read_csv_auto('{CSV_PATH}', header = true, nullstr = '')
        """
    )

    _count = con.execute("SELECT COUNT(*) FROM netflix_titles").fetchone()[0]
    print(f"✅  Table 'netflix_titles' created with {_count:,} rows.")
    return


@app.cell
def __(mo):
    mo.md("## Step 3 — Verify schema")
    return


@app.cell
def __(con, mo):
    _schema = con.execute(
        """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'netflix_titles'
        ORDER BY ordinal_position
        """
    ).df()

    mo.ui.table(_schema, label="netflix_titles — column schema")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## Step 4 — Basic queries

        Five quick queries to confirm the data loaded correctly.
        Each query answers a simple question about the dataset.
        """
    )
    return


# ─────────────────────────────────────────────
# BASIC QUERY 1 — First 10 rows
# ─────────────────────────────────────────────
@app.cell
def __(mo):
    mo.md(
        """
        ### Query 1 — First 10 rows (`LIMIT 10`)

        **What:** A plain `SELECT *` with a row limit — the most basic
        possible query. Use this as a quick eyeball check to confirm columns,
        sample values, and data types look right.

        ```sql
        SELECT *
        FROM   netflix_titles
        LIMIT  10;
        ```
        """
    )
    return


@app.cell
def __(con, mo):
    _df = con.execute(
        """
        SELECT *
        FROM   netflix_titles
        LIMIT  10
        """
    ).df()
    mo.ui.table(_df, label="First 10 rows")
    return


# ─────────────────────────────────────────────
# BASIC QUERY 2 — Row count
# ─────────────────────────────────────────────
@app.cell
def __(mo):
    mo.md(
        """
        ### Query 2 — Total row count (`COUNT(*)`)

        **What:** Counts every row in the table.
        Expected: **8 809** (the full Kaggle dataset).

        ```sql
        SELECT COUNT(*) AS total_titles
        FROM   netflix_titles;
        ```
        """
    )
    return


@app.cell
def __(con, mo):
    _df = con.execute(
        """
        SELECT COUNT(*) AS total_titles
        FROM   netflix_titles
        """
    ).df()
    mo.ui.table(_df, label="Total row count")
    return


# ─────────────────────────────────────────────
# BASIC QUERY 3 — Distinct content types
# ─────────────────────────────────────────────
@app.cell
def __(mo):
    mo.md(
        """
        ### Query 3 — Distinct content types

        **What:** Lists every unique value in the `type` column.
        Netflix has exactly two types: **Movie** and **TV Show**.

        ```sql
        SELECT   type,
                 COUNT(*) AS count
        FROM     netflix_titles
        GROUP BY type
        ORDER BY count DESC;
        ```
        """
    )
    return


@app.cell
def __(con, mo):
    _df = con.execute(
        """
        SELECT   type,
                 COUNT(*) AS count
        FROM     netflix_titles
        GROUP BY type
        ORDER BY count DESC
        """
    ).df()
    mo.ui.table(_df, label="Content types")
    return


# ─────────────────────────────────────────────
# BASIC QUERY 4 — NULL counts per column
# ─────────────────────────────────────────────
@app.cell
def __(mo):
    mo.md(
        """
        ### Query 4 — NULL counts per column

        **What:** Data quality check — how many NULLs exist in each column?
        High-NULL columns (`director`, `cast`, `country`) need special
        handling in later analysis.

        ```sql
        SELECT
            COUNT(*) - COUNT(show_id)    AS show_id_nulls,
            COUNT(*) - COUNT(type)       AS type_nulls,
            COUNT(*) - COUNT(title)      AS title_nulls,
            COUNT(*) - COUNT(director)   AS director_nulls,
            COUNT(*) - COUNT("cast")     AS cast_nulls,
            COUNT(*) - COUNT(country)    AS country_nulls,
            COUNT(*) - COUNT(date_added) AS date_added_nulls,
            COUNT(*) - COUNT(rating)     AS rating_nulls,
            COUNT(*) - COUNT(duration)   AS duration_nulls
        FROM netflix_titles;
        ```
        """
    )
    return


@app.cell
def __(con, mo):
    _df = con.execute(
        """
        SELECT
            COUNT(*) - COUNT(show_id)    AS show_id_nulls,
            COUNT(*) - COUNT(type)       AS type_nulls,
            COUNT(*) - COUNT(title)      AS title_nulls,
            COUNT(*) - COUNT(director)   AS director_nulls,
            COUNT(*) - COUNT("cast")     AS cast_nulls,
            COUNT(*) - COUNT(country)    AS country_nulls,
            COUNT(*) - COUNT(date_added) AS date_added_nulls,
            COUNT(*) - COUNT(rating)     AS rating_nulls,
            COUNT(*) - COUNT(duration)   AS duration_nulls
        FROM netflix_titles
        """
    ).df()
    mo.ui.table(_df, label="NULL counts per column")
    return


# ─────────────────────────────────────────────
# BASIC QUERY 5 — Distinct ratings
# ─────────────────────────────────────────────
@app.cell
def __(mo):
    mo.md(
        """
        ### Query 5 — Distinct content ratings

        **What:** Shows every unique maturity rating (TV-MA, PG-13, R, …)
        and how many titles carry each rating.  Useful for understanding
        the age-group distribution of the library.

        ```sql
        SELECT   rating,
                 COUNT(*) AS count
        FROM     netflix_titles
        WHERE    rating IS NOT NULL
        GROUP BY rating
        ORDER BY count DESC;
        ```
        """
    )
    return


@app.cell
def __(con, mo):
    _df = con.execute(
        """
        SELECT   rating,
                 COUNT(*) AS count
        FROM     netflix_titles
        WHERE    rating IS NOT NULL
        GROUP BY rating
        ORDER BY count DESC
        """
    ).df()
    mo.ui.table(_df, label="Ratings distribution")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ---
        ## ✅ Database ready

        `netflix.duckdb` now contains the `netflix_titles` table with
        clean snake_case columns.
        Open **`02_netflix_analysis.py`** to run the full suite of queries.
        """
    )
    return


if __name__ == "__main__":
    app.run()
