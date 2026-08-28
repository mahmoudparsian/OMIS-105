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
    # Creating DuckDB Tables from CSV Files

    This notebook demonstrates multiple approaches to creating DuckDB tables from small CSV files (3–4 columns). We cover:

    1. **Setup** – Installing DuckDB and creating sample CSV files
    2. **Basic table creation** – `read_csv_auto` and `CREATE TABLE AS`
    3. **Explicit schema definition** – Defining column types before loading
    4. **CSV read options** – Delimiters, headers, null values, date formats
    5. **In-memory vs. persistent databases**
    6. **Querying and verifying tables**
    7. **Loading multiple CSVs into one table**
    8. **Using the Python `duckdb` relational API**
    9. **Error handling and best practices**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Setup
    """)
    return


@app.cell
def _():
    # Install DuckDB (run once)
    return


@app.cell
def _():
    import duckdb
    import os

    print(f"DuckDB version: {duckdb.__version__}")
    return (duckdb, os)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Create sample CSV files

    We'll create several small CSV files to demonstrate different scenarios.
    """)
    return


@app.cell
def _():
    # --- Sample 1: employees.csv (4 columns) ---
    csv_employees = """employee_id,name,department,salary
    101,Alice Johnson,Engineering,95000.00
    102,Bob Smith,Marketing,72000.50
    103,Carol White,Engineering,98000.00
    104,David Brown,Sales,68000.75
    105,Eva Martinez,Marketing,74000.00
    106,Frank Lee,Engineering,102000.00
    107,Grace Kim,Sales,71000.25
    108,Henry Chen,Engineering,97000.00
    """

    with open("employees.csv", "w") as _f:
        _f.write(csv_employees.strip())

    print("Created: employees.csv")
    print(csv_employees.strip())
    return


@app.cell
def _():
    # --- Sample 2: sales.csv (3 columns) ---
    csv_sales = """date,product,revenue
    2024-01-15,Widget A,1200.50
    2024-01-16,Widget B,890.00
    2024-01-17,Widget A,1350.75
    2024-01-18,Widget C,2100.00
    2024-01-19,Widget B,760.25
    2024-01-20,Widget A,1500.00
    """

    with open("sales.csv", "w") as _f:
        _f.write(csv_sales.strip())

    print("Created: sales.csv")
    print(csv_sales.strip())
    return (csv_sales,)


@app.cell
def _():
    # --- Sample 3: sensors.csv (4 columns, with NULL values) ---
    csv_sensors = """timestamp,sensor_id,temperature,humidity
    2024-03-01 08:00:00,S001,22.5,45.2
    2024-03-01 08:05:00,S002,23.1,
    2024-03-01 08:10:00,S001,,46.8
    2024-03-01 08:15:00,S003,21.9,44.0
    2024-03-01 08:20:00,S002,22.8,47.1
    2024-03-01 08:25:00,S001,23.4,45.9
    """

    with open("sensors.csv", "w") as _f:
        _f.write(csv_sensors.strip())

    print("Created: sensors.csv")
    print(csv_sensors.strip())
    return


@app.cell
def _():
    # --- Sample 4: products_pipe.csv (3 columns, pipe-delimited, no header) ---
    csv_products = """P001|Laptop|999.99
    P002|Keyboard|49.99
    P003|Mouse|29.99
    P004|Monitor|349.99
    P005|Headphones|79.99
    """

    with open("products_pipe.csv", "w") as _f:
        _f.write(csv_products.strip())

    print("Created: products_pipe.csv")
    print(csv_products.strip())
    return


@app.cell
def _(csv_sales, os):
    # --- Sample 5: additional sales files for multi-file loading ---
    csv_sales_feb = """date,product,revenue
    2024-02-01,Widget A,1100.00
    2024-02-02,Widget C,2200.50
    2024-02-03,Widget B,950.00
    """

    csv_sales_mar = """date,product,revenue
    2024-03-01,Widget B,880.00
    2024-03-02,Widget A,1450.25
    2024-03-03,Widget C,2050.00
    """

    os.makedirs("monthly_sales", exist_ok=True)
    with open("monthly_sales/sales_jan.csv", "w") as _f:
        _f.write(csv_sales.strip())
    with open("monthly_sales/sales_feb.csv", "w") as _f:
        _f.write(csv_sales_feb.strip())
    with open("monthly_sales/sales_mar.csv", "w") as _f:
        _f.write(csv_sales_mar.strip())

    print("Created: monthly_sales/sales_jan.csv, sales_feb.csv, sales_mar.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. Basic Table Creation with `read_csv_auto`

    DuckDB's `read_csv_auto` automatically detects column types, delimiters, and headers.
    """)
    return


@app.cell
def _(duckdb):
    # Connect to an in-memory database
    con = duckdb.connect()

    # Method 1: CREATE TABLE AS SELECT from read_csv_auto
    con.execute("""
        CREATE TABLE employees AS
        SELECT *
        FROM read_csv_auto('employees.csv');
    """)

    # Verify the table
    print("=== employees table ===")
    print(con.execute("""
        SELECT *
        FROM employees;
    """).fetchdf())
    print("\n=== Schema ===")
    print(con.execute("""
        DESCRIBE employees;
    """).fetchdf())
    return (con,)


@app.cell
def _(con):
    # Method 2: CREATE TABLE directly from a CSV file path
    # (DuckDB 0.9+ supports this shorthand)
    con.execute("""
        CREATE TABLE sales AS
        SELECT *
        FROM 'sales.csv';
    """)

    print("=== sales table ===")
    print(con.execute("""
        SELECT *
        FROM sales;
    """).fetchdf())
    print("\n=== Schema ===")
    print(con.execute("""
        DESCRIBE sales;
    """).fetchdf())
    return


@app.cell
def _(con):
    # Method 3: Query the CSV directly without creating a table
    # (useful for one-off exploration)
    _result = con.execute("""
        SELECT *
        FROM read_csv_auto('sensors.csv')
        WHERE temperature IS NOT NULL;
    """).fetchdf()

    print("=== Direct CSV query (sensors with non-null temperature) ===")
    print(_result)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. Explicit Schema Definition

    When you want full control over column types, define the schema first, then insert data.
    """)
    return


@app.cell
def _(con):
    # Approach A: Define schema then INSERT from CSV
    con.execute("""
        CREATE TABLE sensors (
            TIMESTAMP   TIMESTAMP,
            sensor_id   VARCHAR(10),
            temperature DOUBLE,
            humidity    DOUBLE
        );
    """)

    con.execute("""
        INSERT INTO sensors
        SELECT *
        FROM read_csv_auto('sensors.csv');
    """)

    print("=== sensors table (explicit schema) ===")
    print(con.execute("""
        SELECT *
        FROM sensors;
    """).fetchdf())
    print("\n=== Schema ===")
    print(con.execute("""
        DESCRIBE sensors;
    """).fetchdf())
    return


@app.cell
def _(con):
    # Approach B: Use read_csv with explicit column definitions
    con.execute("""
        CREATE TABLE employees_typed AS
        SELECT *
        FROM read_csv( 'employees.csv', columns = { 'employee_id': 'INTEGER', 'name': 'VARCHAR', 'department': 'VARCHAR', 'salary': 'DECIMAL(10,2)' } );
    """)

    print("=== employees_typed table ===")
    print(con.execute("""
        DESCRIBE employees_typed;
    """).fetchdf())
    print()
    print(con.execute("""
        SELECT *
        FROM employees_typed;
    """).fetchdf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. CSV Read Options

    DuckDB provides many parameters to handle non-standard CSV files.
    """)
    return


@app.cell
def _(con):
    # Handle pipe-delimited file with no header row
    con.execute("""
        CREATE TABLE products AS
        SELECT *
        FROM read_csv( 'products_pipe.csv', delim = '|', header = false, columns = { 'product_id': 'VARCHAR', 'product_name': 'VARCHAR', 'price': 'DECIMAL(8,2)' } );
    """)

    print("=== products table (pipe-delimited, no header) ===")
    print(con.execute("""
        SELECT *
        FROM products;
    """).fetchdf())
    print("\n=== Schema ===")
    print(con.execute("""
        DESCRIBE products;
    """).fetchdf())
    return


@app.cell
def _(con):
    # Demonstrate additional read_csv options
    # (Using employees.csv but showing available parameters)

    _result = con.execute("""
        SELECT *
        FROM read_csv(
            'employees.csv',
            delim = ',',          -- column delimiter
            header = true,        -- first row is header
            quote = '"',          -- quote character
            escape = '"',         -- escape character inside quotes
            nullstr = '',         -- string that represents NULL
            skip = 0,             -- rows to skip at beginning
            auto_detect = true,   -- auto-detect types
            sample_size = -1      -- sample all rows for type detection
        );
    """).fetchdf()

    print("=== read_csv with explicit options ===")
    print(_result)
    print("\n--- Common read_csv parameters ---")
    print("""
      delim        : Column separator (default: auto-detected)
      header       : true/false — first row is header?
      columns      : Dict of column_name: type
      quote        : Quote character (default '"')
      escape       : Escape char within quotes (default '"')
      nullstr      : String representing NULL values
      skip         : Number of rows to skip at start
      dateformat   : Custom date format (e.g., '%d/%m/%Y')
      timestampformat : Custom timestamp format
      sample_size  : Rows to sample for type detection (-1 = all)
      all_varchar  : true = read all columns as VARCHAR
      auto_detect  : true/false — auto-detect types?
      filename     : true = adds a 'filename' column
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. In-Memory vs. Persistent Databases

    DuckDB can operate entirely in memory or persist data to disk.
    """)
    return


@app.cell
def _(duckdb):
    # --- In-memory database (default) ---
    # Data is lost when connection closes
    mem_con = duckdb.connect()  # or duckdb.connect(':memory:')
    mem_con.execute("""
        CREATE TABLE temp_data AS
        SELECT *
        FROM 'sales.csv';
    """)
    print("In-memory table created successfully")
    print(mem_con.execute("""
        SELECT COUNT(*) AS row_count
        FROM temp_data;
    """).fetchdf())
    mem_con.close()
    # Table is gone after close!
    return


@app.cell
def _(duckdb, os):
    # --- Persistent database (saved to disk) ---
    db_path = "my_database.duckdb"

    # Remove if exists (for clean demo)
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create persistent database and load CSV
    _disk_con = duckdb.connect(db_path)

    _disk_con.execute("""
        CREATE TABLE employees AS
        SELECT *
        FROM read_csv_auto('employees.csv');
    """)

    _disk_con.execute("""
        CREATE TABLE sales AS
        SELECT *
        FROM read_csv_auto('sales.csv');
    """)

    print("Tables in persistent database:")
    print(_disk_con.execute("SHOW TABLES").fetchdf())
    _disk_con.close()

    print(f"\nDatabase file size: {os.path.getsize(db_path)} bytes")
    print(f"Database saved to: {db_path}")
    return (db_path,)


@app.cell
def _(db_path, duckdb):
    # Reopen the persistent database — data is still there!
    _disk_con = duckdb.connect(db_path)

    print("=== Reopened persistent database ===")
    print("Tables:", _disk_con.execute("SHOW TABLES").fetchdf().to_dict())
    print("\nEmployees:")
    print(_disk_con.execute("""
        SELECT *
        FROM employees
        LIMIT 3;
    """).fetchdf())
    _disk_con.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6. Querying and Verifying Tables

    Once tables are loaded, you can run full SQL against them.
    """)
    return


@app.cell
def _(duckdb):
    _con = duckdb.connect()
    _con.execute("""
        CREATE TABLE employees AS
        SELECT *
        FROM 'employees.csv';
    """)
    _con.execute("""
        CREATE TABLE sales AS
        SELECT *
        FROM 'sales.csv';
    """)
    _con.execute("""
        CREATE TABLE sensors AS
        SELECT *
        FROM read_csv_auto('sensors.csv');
    """)

    # Check table metadata
    print("=== All Tables ===")
    print(con.execute("SHOW TABLES").fetchdf())

    print("\n=== Table Info (employees) ===")
    print(_con.execute("""
        DESCRIBE employees;
    """).fetchdf())

    print("\n=== Row Counts ===")
    for table in ['employees', 'sales', 'sensors']:
        count = _con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")
    return (_con,)


@app.cell
def _(con):
    # Aggregation queries
    print("=== Average Salary by Department ===")
    print(con.execute("""
        SELECT
            department,
            COUNT(*) AS headcount,
            ROUND(AVG(salary), 2) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
    """).fetchdf())

    print("\n=== Daily Revenue Summary ===")
    print(con.execute("""
        SELECT
            product,
            COUNT(*) AS num_sales,
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(AVG(revenue), 2) AS avg_revenue
        FROM sales
        GROUP BY product
        ORDER BY total_revenue DESC;
    """).fetchdf())
    return


@app.cell
def _(con):
    # Handling NULLs in sensor data
    print("=== Sensor NULL Analysis ===")
    print(con.execute("""
        SELECT
            sensor_id,
            COUNT(*) AS total_readings,
            COUNT(temperature) AS temp_readings,
            COUNT(humidity) AS humidity_readings,
            ROUND(AVG(temperature), 1) AS avg_temp,
            ROUND(AVG(humidity), 1) AS avg_humidity
        FROM sensors
        GROUP BY sensor_id
        ORDER BY sensor_id;
    """).fetchdf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7. Loading Multiple CSVs into One Table

    DuckDB supports glob patterns to load multiple files at once.
    """)
    return


@app.cell
def _(con):
    # Load all CSV files from a directory using glob pattern
    con.execute("""
        CREATE TABLE all_sales AS
        SELECT *
        FROM read_csv_auto('monthly_sales/sales_*.csv');
    """)

    print("=== Combined sales from all months ===")
    print(con.execute("""
        SELECT COUNT(*) AS total_rows
        FROM all_sales;
    """).fetchdf())
    print()
    print(con.execute("""
        SELECT *
        FROM all_sales
        ORDER BY DATE;
    """).fetchdf())
    return


@app.cell
def _(con):
    # Include the source filename as a column
    con.execute("""
        DROP TABLE IF EXISTS all_sales_with_source;
    """)
    con.execute("""
        CREATE TABLE all_sales_with_source AS
        SELECT *
        FROM read_csv_auto( 'monthly_sales/sales_*.csv', filename = true );
    """)

    print("=== Sales with source filename ===")
    print(con.execute("""
        SELECT
            DATE,
            product,
            revenue,
            filename
        FROM all_sales_with_source
        ORDER BY DATE;
    """).fetchdf())
    return


@app.cell
def _(con):
    # Load a list of specific files
    con.execute("""
        DROP TABLE IF EXISTS selected_sales;
    """)
    con.execute("""
        CREATE TABLE selected_sales AS
        SELECT *
        FROM read_csv_auto([ 'monthly_sales/sales_jan.csv', 'monthly_sales/sales_mar.csv' ]);
    """)

    print("=== Jan + Mar sales only ===")
    print(con.execute("""
        SELECT *
        FROM selected_sales
        ORDER BY DATE;
    """).fetchdf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8. Using the Python Relational API

    DuckDB's Python API supports a pandas-like relational interface.
    """)
    return


@app.cell
def _(duckdb):
    # Read CSV into a DuckDB relation (lazy evaluation)
    rel = duckdb.read_csv('employees.csv')

    print("=== DuckDB Relation ===")
    print(f"Type: {type(rel)}")
    print(f"Columns: {rel.columns}")
    print(f"Types: {rel.types}")
    print()

    # Chain operations (filter, project, aggregate)
    _result = (
        rel
        .filter("department = 'Engineering'")
        .project("name, salary")
        .order("salary DESC")
    )

    print("=== Engineering employees sorted by salary ===")
    print(_result.fetchdf())
    return


@app.cell
def _(duckdb):
    # Convert relation to a persistent table
    con2 = duckdb.connect()

    # Read and register as a table
    sales_rel = con2.read_csv('sales.csv')
    con2.execute("""
        CREATE TABLE sales_data AS
        SELECT *
        FROM sales_rel;
    """)

    # Use aggregate on the relation
    agg = (
        con2.read_csv('sales.csv')
        .aggregate("product, SUM(revenue) as total_rev, COUNT(*) as cnt")
        .order("total_rev DESC")
    )

    print("=== Aggregation via Relational API ===")
    print(agg.fetchdf())
    return


@app.cell
def _(duckdb):
    # Integration with pandas DataFrames
    import pandas as pd

    # CSV -> DuckDB -> pandas DataFrame
    df = duckdb.query("""
        SELECT
            department,
            COUNT(*) AS headcount,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM 'employees.csv'
        GROUP BY department;
    """).to_df()

    print("=== Result as pandas DataFrame ===")
    print(type(df))
    print(df)

    # pandas DataFrame -> DuckDB table
    con3 = duckdb.connect()
    df_products = pd.DataFrame({
        'id': ['P001', 'P002', 'P003'],
        'name': ['Laptop', 'Keyboard', 'Mouse'],
        'price': [999.99, 49.99, 29.99]
    })

    con3.execute("""
        CREATE TABLE products_from_df AS
        SELECT *
        FROM df_products;
    """)
    print("\n=== Table created from pandas DataFrame ===")
    print(con3.execute("""
        SELECT *
        FROM products_from_df;
    """).fetchdf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 9. Error Handling and Best Practices
    """)
    return


@app.cell
def _(duckdb):
    # Best Practice 1: Use OR REPLACE / IF NOT EXISTS
    con4 = duckdb.connect()

    # Safe re-creation (won't error if table exists)
    con4.execute("""
        CREATE
        OR REPLACE TABLE employees AS
        SELECT *
        FROM read_csv_auto('employees.csv');
    """)

    # Only create if it doesn't exist
    con4.execute("""
        CREATE TABLE IF NOT EXISTS employees AS
        SELECT *
        FROM read_csv_auto('employees.csv');
    """)

    print("Tables created safely (no duplicate errors)")
    print(con4.execute("SHOW TABLES").fetchdf())
    return


@app.cell
def _(duckdb, os):
    # Best Practice 2: Error handling for missing/malformed files
    import traceback

    def safe_load_csv(connection, table_name, csv_path, **kwargs):
        """
        Safely load a CSV file into a DuckDB table with error handling.
        
        Parameters:
            connection: DuckDB connection
            table_name: Name for the target table
            csv_path: Path to the CSV file
            **kwargs: Additional read_csv parameters
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(csv_path):
                print(f"ERROR: File not found: {csv_path}")
                return False
            
            # Check file is not empty
            if os.path.getsize(csv_path) == 0:
                print(f"ERROR: File is empty: {csv_path}")
                return False
            
            # Build options string
            options = ", ".join(f"{k} = {repr(v)}" for k, v in kwargs.items())
            options_str = f", {options}" if options else ""
            
            # Load the CSV
            connection.execute(f"""
                CREATE OR REPLACE TABLE {table_name} AS
                SELECT * FROM read_csv_auto('{csv_path}'{options_str})
            """)
            
            row_count = connection.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]
            
            print(f"SUCCESS: Loaded {row_count} rows into '{table_name}' from '{csv_path}'")
            return True
            
        except duckdb.Error as e:
            print(f"DuckDB ERROR loading '{csv_path}': {e}")
            return False
        except Exception as e:
            print(f"UNEXPECTED ERROR: {e}")
            traceback.print_exc()
            return False


    # Test the helper function
    con5 = duckdb.connect()

    print("--- Test 1: Valid file ---")
    safe_load_csv(con5, "emp", "employees.csv")

    print("\n--- Test 2: Missing file ---")
    safe_load_csv(con5, "bad", "nonexistent.csv")

    print("\n--- Test 3: Pipe-delimited with options ---")
    safe_load_csv(con5, "prod", "products_pipe.csv")
    return


@app.cell
def _(duckdb):
    # Best Practice 3: Use COPY for bulk loading (faster for large files)
    con6 = duckdb.connect()

    # First create the table with schema
    con6.execute("""
        CREATE TABLE employees_copy (
            employee_id INTEGER,
            name        VARCHAR,
            department  VARCHAR,
            salary      DOUBLE
        );
    """)

    # Use COPY command (often faster for large files)
    con6.execute("""
        COPY employees_copy
        FROM 'employees.csv' (HEADER true);
    """)

    print("=== Loaded via COPY command ===")
    print(con6.execute("""
        SELECT *
        FROM employees_copy;
    """).fetchdf())
    return


@app.cell
def _(duckdb):
    # Best Practice 4: Inspect CSV before loading
    con7 = duckdb.connect()

    # Sniff the CSV to see what DuckDB detects
    print("=== CSV Sniff Results ===")
    sniff = con7.execute("""
        SELECT *
        FROM sniff_csv('employees.csv');
    """).fetchdf()
    print(sniff.to_string())
    return


@app.cell
def _(duckdb):
    # Best Practice 5: Using VIEWS instead of tables for dynamic CSV access
    con8 = duckdb.connect()

    # A VIEW reads the CSV fresh each time it's queried
    # (useful if the CSV file is updated externally)
    con8.execute("""
        CREATE VIEW live_sales AS
        SELECT *
        FROM read_csv_auto('sales.csv');
    """)

    print("=== View (reads CSV on each query) ===")
    print(con8.execute("""
        SELECT *
        FROM live_sales;
    """).fetchdf())
    print("\nNote: If you update sales.csv, the view reflects changes immediately.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary & Quick Reference

    | Method | Use Case | Example |
    |--------|----------|--------|
    | `read_csv_auto('file.csv')` | Auto-detect everything | `SELECT * FROM read_csv_auto('data.csv')` |
    | `'file.csv'` (string literal) | Quick shorthand (DuckDB 0.9+) | `SELECT * FROM 'data.csv'` |
    | `read_csv(...)` with columns | Explicit type control | `read_csv('f.csv', columns={...})` |
    | `COPY ... FROM` | Bulk loading (fastest) | `COPY t FROM 'f.csv' (HEADER true)` |
    | Glob patterns | Multiple files | `read_csv_auto('dir/*.csv')` |
    | `CREATE VIEW` | Dynamic/live CSV access | `CREATE VIEW v AS SELECT * FROM 'f.csv'` |

    ### Key Tips

    - Use `CREATE OR REPLACE TABLE` to avoid "table already exists" errors
    - Use `sniff_csv()` to preview what DuckDB detects before loading
    - Use `filename = true` when loading multiple files to track the source
    - For persistent storage, connect to a `.duckdb` file instead of memory
    - Use `DESCRIBE table_name` to verify the schema after loading
    - The relational API (`duckdb.read_csv()`) supports chained operations
    """)
    return


@app.cell
def _(os):
    # Cleanup: remove sample files created in this notebook
    import shutil

    files_to_remove = [
        'employees.csv', 'sales.csv', 'sensors.csv',
        'products_pipe.csv', 'my_database.duckdb'
    ]

    for _f in files_to_remove:
        if os.path.exists(_f):
            os.remove(_f)

    if os.path.exists('monthly_sales'):
        shutil.rmtree('monthly_sales')

    print("Cleanup complete!")
    return


if __name__ == "__main__":
    app.run()
