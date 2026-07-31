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
    # Notebook 1 — Build the Insurance DuckDB Database---**Goal:** Read `insurance.csv`, identify and remove duplicate rows, and persist a clean table into `insurance_db.duckdb`.**Columns:** `age`, `gender`, `bmi`, `children`, `smoker`, `region`, `charges`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1 — Import LibrariesWe import **DuckDB** for our SQL database, **Pandas** for display, and our custom **util_plot** module for visualizations.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    from util_plot import (PALETTE, FIG_SMALL, FIG_MEDIUM, FIG_WIDE, FIG_TALL, plot_bar, plot_grouped_bar, plot_line, plot_scatter, plot_histogram, plot_boxplot, plot_pie, plot_heatmap, plot_stacked_bar, plot_lollipop, plot_multi_line, highlight_duplicates)
    print("Libraries loaded successfully!")
    return (duckdb, highlight_duplicates, plot_bar)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2 — Load the CSV and Preview the DataWe create an **in-memory** DuckDB connection first, load the CSV, and take a quick look at the shape and first rows.
    """)
    return


@app.cell
def _(duckdb):
    con = duckdb.connect()  # in-memory for now

    # Load CSV into a temporary table
    con.execute("""
        CREATE TABLE raw_insurance AS
        SELECT *
        FROM read_csv_auto('insurance.csv');
    """)

    total_rows = con.execute("""
        SELECT COUNT(*)
        FROM raw_insurance;
    """).fetchone()[0]
    print(f"Total rows loaded: {total_rows:,}")

    df_preview = con.execute("""
        SELECT *
        FROM raw_insurance
        LIMIT 10;
    """).df()
    df_preview
    return (con, total_rows)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3 — Inspect the Table SchemaLet's confirm the column names and data types DuckDB inferred from the CSV.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        DESCRIBE raw_insurance;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4 — Identify All Duplicate RowsWe group by **every column** and keep groups that appear more than once. This shows us the exact rows that are duplicated and how many copies exist.
    """)
    return


@app.cell
def _(con, highlight_duplicates):
    df_dupes = con.execute("""
        SELECT
            age,
            gender,
            bmi,
            children,
            smoker,
            region,
            charges,
            COUNT(*) AS duplicate_count
        FROM raw_insurance
        GROUP BY age, gender, bmi, children, smoker, region, charges
        HAVING COUNT(*) > 1
        ORDER BY duplicate_count DESC, charges DESC;
    """).df()

    print(f"Number of distinct rows that have duplicates: {len(df_dupes)}")
    print(f"Total extra (duplicate) rows: {df_dupes['duplicate_count'].sum() - len(df_dupes)}")
    print()
    highlight_duplicates(df_dupes)
    return (df_dupes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5 — Visualize the Duplicate DistributionA bar chart showing how many rows have 2 copies, 3 copies, etc.
    """)
    return


@app.cell
def _(df_dupes, plot_bar):
    dup_dist = df_dupes.groupby("duplicate_count").size().reset_index(name="num_rows")
    dup_dist["duplicate_count"] = dup_dist["duplicate_count"].astype(str) + "x"

    plot_bar(dup_dist, x="duplicate_count", y="num_rows",
             title="Distribution of Duplicate Counts",
             xlabel="Number of Copies", ylabel="Number of Distinct Rows",
             color="#e74c3c")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6 — Remove Duplicate RowsWe use DuckDB's **window function** with `ROW_NUMBER()` to keep only the first occurrence of each row. The clean data goes into a new table called `insurance`.
    """)
    return


@app.cell
def _(con, total_rows):
    con.execute("""
        CREATE TABLE insurance AS
        SELECT
            age,
            gender,
            bmi,
            children,
            smoker,
            region,
            charges
        FROM (
        SELECT
            *,
            ROW_NUMBER() OVER ( PARTITION BY age, gender, bmi, children, smoker, region, charges ) AS rn
        FROM raw_insurance )
        WHERE rn = 1;
    """)

    clean_rows = con.execute("""
        SELECT COUNT(*)
        FROM insurance;
    """).fetchone()[0]
    removed = total_rows - clean_rows
    print(f"Original rows:  {total_rows:,}")
    print(f"Clean rows:     {clean_rows:,}")
    print(f"Rows removed:   {removed:,}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 7 — Verify: No Duplicate Rows RemainWe run the same duplicate-detection query on the clean `insurance` table. The result should be **empty**.
    """)
    return


@app.cell
def _(con):
    df_verify = con.execute("""
        SELECT
            age,
            gender,
            bmi,
            children,
            smoker,
            region,
            charges,
            COUNT(*) AS cnt
        FROM insurance
        GROUP BY age, gender, bmi, children, smoker, region, charges
        HAVING COUNT(*) > 1;
    """).df()

    if len(df_verify) == 0:
        print("VERIFIED: The 'insurance' table has ZERO duplicate rows.")
    else:
        print(f"WARNING: {len(df_verify)} duplicated groups still found!")
        display(df_verify)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 8 — Persist to `insurance_db.duckdb`We now write the clean `insurance` table into a **persistent** DuckDB database file on disk.
    """)
    return


@app.cell
def _(con, duckdb):
    import os

    db_path = "insurance_db.duckdb"

    # Remove old DB if it exists so we start fresh
    if os.path.exists(db_path):
        os.remove(db_path)

    disk_con = duckdb.connect(db_path)

    # Copy clean table from in-memory to disk via pandas
    df_clean = con.execute("""
        SELECT *
        FROM insurance;
    """).df()
    disk_con.execute("""
        CREATE TABLE insurance AS
        SELECT *
        FROM df_clean;
    """)

    row_count = disk_con.execute("""
        SELECT COUNT(*)
        FROM insurance;
    """).fetchone()[0]
    print(f"Persisted {row_count:,} rows into '{db_path}'")
    print(f"File size: {os.path.getsize(db_path):,} bytes")

    disk_con.close()
    con.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 9 — Final Verification: Reopen the DatabaseOpen the persisted file from scratch and confirm everything is intact.
    """)
    return


@app.cell
def _(duckdb):
    verify_con = duckdb.connect("insurance_db.duckdb", read_only=True)

    # Check table exists
    tables = verify_con.execute("SHOW TABLES").df()
    print("Tables in database:")
    print(tables)
    print()

    # Row count
    n = verify_con.execute("""
        SELECT COUNT(*)
        FROM insurance;
    """).fetchone()[0]
    print(f"Row count: {n:,}")
    print()

    # Quick sample
    print("Sample rows:")
    verify_con.execute("""
        SELECT *
        FROM insurance
        LIMIT 5;
    """).df()
    return (verify_con,)


@app.cell
def _(verify_con):
    # Final duplicate check on the persisted database
    dup_check = verify_con.execute("""
        SELECT COUNT(*) AS dup_groups
        FROM (
        SELECT
            age,
            gender,
            bmi,
            children,
            smoker,
            region,
            charges
        FROM insurance
        GROUP BY age, gender, bmi, children, smoker, region, charges
        HAVING COUNT(*) > 1 );
    """).fetchone()[0]

    print(f"Duplicate groups found: {dup_check}")
    if dup_check == 0:
        print("FINAL VERIFICATION PASSED: insurance_db.duckdb is clean and ready!")

    verify_con.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---## Summary| Step | Result ||------|--------|| CSV loaded | 1,773 rows (excluding header) || Duplicates identified | Displayed above || Duplicates removed | Using `ROW_NUMBER()` window function || Clean table persisted | `insurance_db.duckdb` → table `insurance` || Final verification | Zero duplicates confirmed |The database is now ready for **Notebook 2** (SQL Queries Tutorial).
    """)
    return


if __name__ == "__main__":
    app.run()
