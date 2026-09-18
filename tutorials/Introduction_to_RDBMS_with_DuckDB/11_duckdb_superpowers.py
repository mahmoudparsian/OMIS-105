import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="11 - DuckDB Superpowers")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 11 · DuckDB Superpowers

    Notebook **11 of 12** · estimated time: **10 minutes**.

    Everything so far — tables, keys, joins, constraints,
    transactions — is standard RDBMS material that transfers
    directly to Postgres, MySQL, SQL Server, and friends. This
    notebook is about what makes **DuckDB** specifically worth
    knowing: it treats files and DataFrames as first-class,
    queryable tables, with no import step.

    Objectives:

    - Query a CSV or Parquet file directly with SQL — no `CREATE
      TABLE`, no loading
    - Query a pandas DataFrame that's just sitting in your notebook
    - Read a query plan with `EXPLAIN`
    - Export a result straight to a file
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect("ecommerce_database.duckdb", read_only=True)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Querying a file directly

    In most databases, getting data in requires a loading step —
    exactly what `ecommerce_data.load_data()` did back in notebook
    03. DuckDB can skip that entirely and run SQL **straight against
    a file on disk**. First, let's export `customers` to a real CSV
    file, to have something to point at:
    """)
    return


@app.cell
def _(con):
    import os
    import tempfile

    export_dir = tempfile.mkdtemp(prefix="duckdb_course_")
    csv_path = os.path.join(export_dir, "customers_export.csv")
    con.sql("SELECT * FROM customers").df().to_csv(csv_path, index=False)
    f"Wrote {csv_path}"
    return csv_path, export_dir


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    (This writes to a temporary directory outside the course folder,
    purely so re-running this notebook doesn't leave export files
    scattered around — in a real project you'd write wherever makes
    sense for your workflow.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now query that file directly — `read_csv_auto` infers the column names and types from the file itself:
    """)
    return


@app.cell
def _(con, csv_path):
    con.sql(f"SELECT * FROM read_csv_auto('{csv_path}') WHERE state = 'CA' LIMIT 5")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    No `CREATE TABLE`, no `INSERT`, no schema declaration — DuckDB
    scanned the file, inferred `customer_id` is an integer,
    `signup_date` is a date, and so on, and let you run ordinary SQL
    against it immediately. The same works for **Parquet** files
    (`read_parquet(...)`, a compressed columnar format very common
    in data engineering) and even **JSON** (`read_json_auto(...)`).
    This is what makes DuckDB popular for ad-hoc analysis: point it
    at whatever files you already have and start writing SQL.

    ## Querying a pandas DataFrame — with no loading step either

    This might be the single most useful DuckDB trick for a Python
    user: if a pandas DataFrame is sitting in your local variables,
    you can reference its **variable name directly in a SQL query**,
    as if it were a table:
    """)
    return


@app.cell
def _(con):
    import pandas as pd

    quick_lookup = pd.DataFrame(
        {"category": ["Electronics", "Office", "Stationery"], "target_margin": [0.35, 0.45, 0.55]}
    )
    con.sql("SELECT * FROM quick_lookup WHERE target_margin > 0.4")
    return (quick_lookup,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `quick_lookup` was never registered, never `CREATE TABLE`'d —
    DuckDB detected it by name in the surrounding Python scope. You
    can even `JOIN` a DataFrame against a real table in the same
    query, mixing "data I just computed in Python" with "data that
    lives in the database" in one statement:
    """)
    return


@app.cell
def _(con):
    con.sql(
        """
        SELECT p.product_name, p.category, p.unit_price, q.target_margin
        FROM products p
        JOIN quick_lookup q ON p.category = q.category
        ORDER BY p.category, p.product_name
        LIMIT 6
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading a query plan with `EXPLAIN`

    Prefix any query with `EXPLAIN` and DuckDB shows you *how* it
    intends to run it, instead of running it:
    """)
    return


@app.cell
def _(con, mo):
    plan_text = con.sql("EXPLAIN SELECT * FROM customers WHERE state = 'CA'").fetchone()[1]
    mo.md(f"```\n{plan_text}\n```")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read it bottom-to-top: `SEQ_SCAN` (a full sequential scan of
    `customers`) happens first, with the `state='CA'` filter applied
    during the scan, then `PROJECTION` picks the columns to return.
    For a table this small it barely matters, but on a large table,
    this is how you'd discover whether a query is scanning
    everything versus using an index efficiently — the starting
    point for any real performance investigation.

    ## Exporting results

    Just as DuckDB reads files without ceremony, it writes them the
    same way. A few common targets:

    ```python
    con.sql("SELECT * FROM customers").df()                    # pandas DataFrame
    con.sql("SELECT * FROM customers").pl()                    # polars DataFrame
    con.sql("SELECT * FROM customers").write_parquet("out.parquet")
    con.sql("COPY customers TO 'out.csv' (HEADER, DELIMITER ',')")  # pure SQL export
    ```

    ## `mo.sql` revisited

    Notebook 01 introduced `mo.sql(query, engine=con)` as marimo's
    native SQL-cell flavor. It gets everything above for free too —
    DataFrame and file scanning work identically, because under the
    hood it's still DuckDB:
    """)
    return


@app.cell
def _(con, mo, quick_lookup):
    mo.sql("SELECT * FROM quick_lookup", engine=con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the interactive `marimo edit` UI, a cell like that gets SQL
    syntax highlighting and autocomplete against every table (and
    DataFrame!) currently in scope — worth switching to for any
    query you're actively iterating on.

    ## Exercise

    The cell below writes `products` out to a Parquet file at
    `products_path`. Without loading it into a table, write a query
    against `read_parquet(products_path)` that returns the 3 most
    expensive `in_stock` products.
    """)
    return


@app.cell
def _(con, export_dir):
    import os as _os

    products_path = _os.path.join(export_dir, "products_export.parquet")
    con.sql("SELECT * FROM products").df().to_parquet(products_path, index=False)
    f"Wrote {products_path}"
    return (products_path,)


@app.cell
def _(mo):
    ex1 = mo.ui.text_area(
        placeholder="SELECT ... FROM read_parquet('...') ...",
        label="11.1",
        full_width=True,
        rows=4,
    )
    ex1
    return (ex1,)


@app.cell
def _(con, ex1, mo):
    def _run(q):
        if not q.strip():
            return mo.md("_Write a query above._")
        try:
            return con.sql(q).df()
        except Exception as e:
            return mo.callout(mo.md(f"**SQL error:** {e}"), kind="danger")

    _run(ex1.value)
    return


@app.cell(hide_code=True)
def _(mo, products_path):
    mo.accordion(
        {
            "💡 Solution": mo.md(
                f"```sql\n"
                f"SELECT product_name, unit_price\n"
                f"FROM read_parquet('{products_path}')\n"
                f"WHERE in_stock = TRUE\n"
                f"ORDER BY unit_price DESC\n"
                f"LIMIT 3\n"
                f"```"
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - DuckDB can query CSV/Parquet/JSON files directly
      (`read_csv_auto`, `read_parquet`, `read_json_auto`) — no load
      step.
    - It can also query pandas (or polars) DataFrames by variable
      name, and join them against real tables in the same query.
    - `EXPLAIN` shows the query plan DuckDB will actually run.
    - `mo.sql(...)` gets all of this for free — same engine,
      friendlier editing experience.

    ➡️ **Next:** `12_capstone_project.py` — the last notebook: a
    multi-step set of real business questions that pull together
    everything from all eleven notebooks before it.
    """)
    return


if __name__ == "__main__":
    app.run()
