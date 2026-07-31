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
    # Notebook 1: Data Cleaning & DuckDB Database Creation

    **Objective:** Read the `auto_insurance.csv` file, clean the data (normalize column names, identify and remove duplicates), and store the cleaned data in a DuckDB database (`auto_insurance_db.duckdb`) with a single table called `insurance`.

    **Tools:** Python, Pandas, DuckDB

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup: Import Libraries
    """)
    return


@app.cell
def _():
    import pandas as pd
    import duckdb
    import os

    print(f"Pandas version: {pd.__version__}")
    print(f"DuckDB version: {duckdb.__version__}")
    return duckdb, os, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Read the CSV File

    **What are we doing?** We load the raw `auto_insurance.csv` file into a Pandas DataFrame to inspect its structure — column names, data types, row count, and a preview of the first few rows.
    """)
    return


@app.cell
def _(pd):
    # Read the CSV file
    df = pd.read_csv('auto_insurance.csv')
    print(f'Shape: {df.shape[0]} rows x {df.shape[1]} columns')
    print(f'\nOriginal column names:')
    for _i, _col in enumerate(df.columns, 1):
        print(f'  {_i:2d}. {_col}')
    return (df,)


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _(df):
    df.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2.0: Convert Column Names to Lowercase with Underscores

    **What are we doing?** Column names like `Customer Lifetime Value` and `Monthly Premium Auto` contain spaces, which makes them awkward to use in SQL queries. We convert all column names to lowercase and replace spaces with underscores (snake_case convention). For example:
    - `Customer Lifetime Value` → `customer_lifetime_value`
    - `Monthly Premium Auto` → `monthly_premium_auto`

    This makes the columns easy to reference in SQL without needing quotes.
    """)
    return


@app.cell
def _(df):
    # Convert column names: lowercase + replace spaces with underscores
    df.columns = [_col.lower().replace(' ', '_') for _col in df.columns]
    print('New column names (snake_case):')
    for _i, _col in enumerate(df.columns, 1):
        print(f'  {_i:2d}. {_col}')
    return


@app.cell
def _(df):
    df.head(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2.1: Identify All Duplicate Rows

    **What are we doing?** Before building our database, we need to check data quality. Duplicate rows can skew analysis and waste storage. We identify all rows that are exact duplicates (keeping all occurrences marked so we can see the full picture).
    """)
    return


@app.cell
def _(df):
    # Find all duplicate rows (mark ALL occurrences, not just subsequent ones)
    duplicate_mask = df.duplicated(keep=False)
    duplicates_df = df[duplicate_mask].sort_values(by=df.columns.tolist())

    num_duplicate_rows = df.duplicated(keep='first').sum()
    num_groups = duplicates_df.shape[0]

    print(f"Total rows in dataset: {df.shape[0]}")
    print(f"Number of duplicate rows (to be removed): {num_duplicate_rows}")
    print(f"Total rows involved in duplication (all occurrences): {num_groups}")
    print(f"\n--- Showing duplicate rows (all occurrences) ---")
    return (duplicates_df,)


@app.cell
def _(display, duplicates_df):
    # Display the duplicate rows
    if duplicates_df.shape[0] > 0:
        display(duplicates_df)
    else:
        print("No duplicate rows found!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2.2: Delete the Duplicate Rows

    **What are we doing?** We remove duplicate rows, keeping only the first occurrence of each duplicated set. This ensures every row in our cleaned dataset is unique.
    """)
    return


@app.cell
def _(df):
    # Remove duplicates, keeping the first occurrence
    df_clean = df.drop_duplicates(keep='first').reset_index(drop=True)

    print(f"Rows before cleaning: {df.shape[0]}")
    print(f"Rows after cleaning:  {df_clean.shape[0]}")
    print(f"Rows removed:         {df.shape[0] - df_clean.shape[0]}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2.3: Create the DuckDB Database

    **What are we doing?** We create a persistent DuckDB database file (`auto_insurance_db.duckdb`) and load our cleaned DataFrame into a single table called `insurance`. DuckDB is an in-process analytical database — fast for SQL queries on local data, perfect for teaching SQL in a notebook environment.
    """)
    return


@app.cell
def _(duckdb, os):
    # Remove existing database file if present (fresh start)
    db_path = 'auto_insurance_db.duckdb'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

    # Create DuckDB database and load cleaned data
    con = duckdb.connect(db_path)
    con.execute("CREATE TABLE insurance AS SELECT * FROM df_clean")

    # Verify table creation
    result = con.execute("SELECT COUNT(*) AS row_count FROM insurance").fetchone()
    print(f"\nDatabase created: {db_path}")
    print(f"Table 'insurance' created with {result[0]} rows")
    return con, db_path


@app.cell
def _(con):
    # Show the table schema
    print("Table schema:")
    con.execute("DESCRIBE insurance").df()
    return


@app.cell
def _(con):
    # Preview data from the database
    con.execute("SELECT * FROM insurance LIMIT 5").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2.4: Verify No Duplicate Rows in the Database

    **What are we doing?** As a final quality check, we query the database directly to confirm there are zero duplicate rows. We use a SQL GROUP BY on all columns and check for any group with a count > 1.
    """)
    return


@app.cell
def _(con, display):
    # Verification: Check for duplicates using SQL
    # Get all column names from the table
    columns = con.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'insurance'").fetchall()
    col_list = ', '.join([_col[0] for _col in columns])
    verification_query = f'\nSELECT {col_list}, COUNT(*) as duplicate_count\nFROM insurance\nGROUP BY {col_list}\nHAVING COUNT(*) > 1\n'
    duplicates_in_db = con.execute(verification_query).df()
    if duplicates_in_db.shape[0] == 0:
        print('✓ VERIFICATION PASSED: No duplicate rows found in the database!')
    else:
        print(f'✗ WARNING: {duplicates_in_db.shape[0]} duplicate groups found!')
        display(duplicates_in_db)
    return


@app.cell
def _(con):
    # Additional verification: compare row counts
    total_rows = con.execute("SELECT COUNT(*) FROM insurance").fetchone()[0]
    distinct_rows = con.execute(f"SELECT COUNT(*) FROM (SELECT DISTINCT * FROM insurance)").fetchone()[0]

    print(f"Total rows in 'insurance' table:    {total_rows}")
    print(f"Distinct rows in 'insurance' table: {distinct_rows}")
    print(f"Difference (duplicates):            {total_rows - distinct_rows}")

    assert total_rows == distinct_rows, "ERROR: Duplicates still exist!"
    print("\n✓ All rows are unique. Database is clean and ready for analysis.")
    return


@app.cell
def _(con, db_path, os):
    # Close the connection
    con.close()
    print(f"\nDatabase file size: {os.path.getsize(db_path) / 1024:.1f} KB")
    print("Done! The database 'auto_insurance_db.duckdb' is ready for Notebook 2.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    | Step | Action | Result |
    |------|--------|--------|
    | 2.0 | Normalized column names to snake_case | 24 columns renamed |
    | 2.1 | Identified duplicate rows | Found and displayed all duplicates |
    | 2.2 | Removed duplicate rows | Kept first occurrence only |
    | 2.3 | Created DuckDB database | `auto_insurance_db.duckdb` with table `insurance` |
    | 2.4 | Verified no duplicates | Confirmed 0 duplicates in database |
    """)
    return


if __name__ == "__main__":
    app.run()
