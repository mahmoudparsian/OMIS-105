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
    # Introduction to DuckDB with Python

    **DuckDB** is a fast, in-process analytical database.  
    Think of it as *SQLite for analytics* — no server needed, just `pip install duckdb` and go.

    ---

    ## What you'll learn in this notebook

    1. Installing and importing DuckDB
    2. Creating an in-memory database and a connection
    3. Creating tables and inserting data
    4. Running queries (SELECT, WHERE, ORDER BY, GROUP BY)
    5. Using aggregate functions
    6. Working with Python variables inside SQL
    7. Reading query results as Pandas DataFrames
    8. Querying CSV files directly (no loading step!)
    9. Cleaning up
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Installation

    Run this cell once to install DuckDB (skip if already installed).
    """)
    return


@app.cell
def _():
    # Install DuckDB (only needed once)

    ### OR -------------------------
    ### !pip3 install duckdb --quiet
    ### ----------------------------
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. Import and connect

    DuckDB can run entirely **in memory** — no files, no server.  
    Just create a connection and you're ready.
    """)
    return


@app.cell
def _():
    import duckdb

    # Create an in-memory database connection
    con = duckdb.connect()

    print(f"DuckDB version: {duckdb.__version__}")
    print("Connected to an in-memory database!")
    return (con, duckdb)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. Create a table and insert data

    Let's create a simple `students` table and add some rows.
    """)
    return


@app.cell
def _(con):
    # Create a table
    con.execute("""
        CREATE TABLE students (
            id    INTEGER,
            name  VARCHAR,
            age   INTEGER,
            grade DOUBLE
        );
    """)

    # Insert rows one at a time
    con.execute("""
        INSERT INTO students
        VALUES (1, 'Alice', 20, 3.8);
    """)
    con.execute("""
        INSERT INTO students
        VALUES (2, 'Bob', 22, 3.5);
    """)
    con.execute("""
        INSERT INTO students
        VALUES (3, 'Charlie', 21, 3.9);
    """)

    # Insert multiple rows at once
    con.execute("""
        INSERT INTO students
        VALUES
            (4, 'Diana', 23, 3.2),
            (5, 'Eve', 20, 3.7),
            (6, 'Frank', 22, 3.6);
    """)

    print("Table 'students' created with 6 rows.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. Basic queries

    ### 4a. SELECT all rows

    Use `.fetchall()` to get results as a list of tuples.
    """)
    return


@app.cell
def _(con):
    # Fetch all rows
    _results = con.execute("""
        SELECT *
        FROM students;
    """).fetchall()

    for _row in _results:
        print(_row)
    return


@app.cell
def _(con):
    # Fetch all rows
    _results = con.execute("""
        SELECT *
        FROM students;
    """).fetchall()
    _results
    return


@app.cell
def _(con):
    # Fetch all rows
    con.execute("""
        SELECT *
        FROM students;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4b. SELECT specific columns
    """)
    return


@app.cell
def _(con):
    # Select only name and grade
    _results = con.execute("""
        SELECT
            name,
            grade
        FROM students;
    """).fetchall()

    for _row in _results:
        print(f"{_row[0]:>10s}  →  GPA {_row[1]}")
    return


@app.cell
def _(con):
    # Select only name and grade
    con.execute("""
        SELECT
            name,
            grade
        FROM students;
    """).df()
    return


@app.cell
def _(con):
    # Select only name and grade
    con.execute("""
    SELECT name, grade 
    FROM students
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4c. WHERE — filtering rows
    """)
    return


@app.cell
def _(con):
    # Students with GPA above 3.6
    _results = con.execute("""
        SELECT
            name,
            grade
        FROM students
        WHERE grade > 3.6;
    """).fetchall()

    print("Students with GPA > 3.6:")
    for _row in _results:
        print(f"  {_row[0]} — {_row[1]}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4d. ORDER BY — sorting results
    """)
    return


@app.cell
def _(con):
    # Sort students by grade, highest first
    _results = con.execute("""
        SELECT
            name,
            grade
        FROM students
        ORDER BY grade DESC;
    """).fetchall()

    print("Students ranked by GPA (highest first):")
    for rank, row in enumerate(_results, 1):
        print(f"  {rank}. {row[0]} — {row[1]}")
    return


@app.cell
def _(con):
    # Sort students by grade, highest first
    con.execute("""
        SELECT
            name,
            grade
        FROM students
        ORDER BY grade DESC;
    """).df()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. Aggregate functions

    DuckDB supports all the standard SQL aggregates: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
    """)
    return


@app.cell
def _(con):
    # Basic aggregates
    result = con.execute("""
        SELECT
            COUNT(*) AS total_students,
            AVG(grade) AS avg_gpa,
            MIN(grade) AS min_gpa,
            MAX(grade) AS max_gpa,
            AVG(age) AS avg_age
        FROM students;
    """).fetchone()

    print(f"Total students : {result[0]}")
    print(f"Average GPA    : {result[1]:.2f}")
    print(f"GPA range      : {result[2]} – {result[3]}")
    print(f"Average age    : {result[4]:.1f}")
    return


@app.cell
def _(con):
    # Basic aggregates
    con.execute("""
        SELECT
            COUNT(*) AS total_students,
            AVG(grade) AS avg_gpa,
            MIN(grade) AS min_gpa,
            MAX(grade) AS max_gpa,
            AVG(age) AS avg_age
        FROM students;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### GROUP BY — aggregates per group
    """)
    return


@app.cell
def _(con):
    # Average GPA by age group
    _results = con.execute("""
        SELECT
            age,
            COUNT(*) AS num_students,
            ROUND(AVG(grade), 2) AS avg_gpa
        FROM students
        GROUP BY age
        ORDER BY age;
    """).fetchall()

    print(f"{'Age':>5}  {'Count':>5}  {'Avg GPA':>8}")
    print("-" * 22)
    for _row in _results:
        print(f"{_row[0]:>5}  {_row[1]:>5}  {_row[2]:>8}")
    return


@app.cell
def _(con):
    # Average GPA by age group

    con.execute("""
        SELECT
            age,
            COUNT(*) AS num_students,
            ROUND(AVG(grade), 2) AS avg_gpa
        FROM students
        GROUP BY age
        ORDER BY age;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6. Using Python variables in SQL queries

    You can pass Python values into queries using **`$1, $2, ...`** placeholders.
    """)
    return


@app.cell
def _(con):
    # Python variables
    min_gpa = 3.5
    max_age = 22

    # Use $1, $2 as placeholders
    _results = con.execute("""
        SELECT
            name,
            age,
            grade
        FROM students
        WHERE grade >= $1
        AND age <= $2;
    """, [min_gpa, max_age]).fetchall()

    print(f"Students with GPA >= {min_gpa} and age <= {max_age}:")
    for _row in _results:
        print(f"  {_row[0]} (age {_row[1]}, GPA {_row[2]})")
    return


@app.cell
def _(con):
    # Python variables
    _min_gpa = 3.5
    _max_age = 22

    # Use $1, $2 as placeholders
    con.execute("""
        SELECT
            name,
            age,
            grade
        FROM students
        WHERE grade >= $1
        AND age <= $2;
    """, [_min_gpa, _max_age]).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7. Getting results as a Pandas DataFrame

    DuckDB integrates beautifully with Pandas — just call `.df()` on any result.
    """)
    return


@app.cell
def _(con):
    # Convert query result directly to a Pandas DataFrame
    df = con.execute("""
        SELECT *
        FROM students
        ORDER BY grade DESC;
    """).df()

    df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Querying a Pandas DataFrame with SQL!

    One of DuckDB's superpowers: you can query **any Python DataFrame** directly with SQL — no import step needed.
    """)
    return


@app.cell
def _(con):
    import pandas as pd

    # Create a DataFrame in Python
    products = pd.DataFrame({
        'product':  ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard'],
        'price':    [999.99,   699.99,  449.99,   329.99,    79.99],
        'in_stock': [True,     True,    False,    True,      True]
    })

    # Query it directly with SQL — no loading needed!
    _result = con.execute("""
        SELECT
            product,
            price
        FROM products
        WHERE in_stock = true
        ORDER BY price DESC;
    """).df()

    print("In-stock products (most expensive first):")
    _result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8. Query CSV files directly

    DuckDB can read CSV (and Parquet, JSON, Excel) files **directly in SQL** — no loading code needed.

    Let's create a small CSV file and query it.
    """)
    return


@app.cell
def _():
    # First, create a sample CSV file
    csv_data = """city,country,population
    Tokyo,Japan,13960000
    Delhi,India,11030000
    Shanghai,China,24870000
    Sao Paulo,Brazil,12330000
    Mexico City,Mexico,9210000
    Cairo,Egypt,9540000
    Mumbai,India,12440000
    Beijing,China,21540000
    Osaka,Japan,2750000
    New York,USA,8340000"""

    with open('cities.csv', 'w') as f:
        f.write(csv_data)

    print("Created cities.csv")
    return


@app.cell
def _(con):
    # Query the CSV file directly — no import step!
    con.execute("""
        SELECT *
        FROM read_csv('cities.csv')
        ORDER BY population DESC;
    """).df()
    return


@app.cell
def _(con):
    # Aggregate query on the CSV
    con.execute("""
        SELECT
            country,
            COUNT(*) AS num_cities,
            SUM(population) AS total_pop,
            ROUND(AVG(population)) AS avg_pop
        FROM read_csv('cities.csv')
        GROUP BY country
        ORDER BY total_pop DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 9. Bonus: Using the `duckdb.sql()` shorthand

    For quick one-off queries, DuckDB offers a convenient top-level `duckdb.sql()` function  
    that uses a shared default connection — no need to create one yourself.
    """)
    return


@app.cell
def _(duckdb):
    # Quick query using the top-level function
    duckdb.sql("SELECT 42 AS answer, 'Hello DuckDB!' AS message").show()
    return


@app.cell
def _(duckdb):
    # You can also use it with the CSV
    duckdb.sql("""
        SELECT
            city,
            population
        FROM read_csv('cities.csv')
        WHERE population > 10000000
        ORDER BY population DESC;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 10. Clean up

    Close the connection when you're done. For in-memory databases, all data is released.
    """)
    return


@app.cell
def _(con):
    # Clean up
    con.close()

    import os
    if os.path.exists('cities.csv'):
        os.remove('cities.csv')

    print("Connection closed. Temporary files removed. Done!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Quick Reference

    | What you want to do | How to do it |
    |---|---|
    | Connect (in-memory) | `con = duckdb.connect()` |
    | Connect (file-based) | `con = duckdb.connect('my.db')` |
    | Run SQL | `con.execute("SELECT ...")` |
    | Get tuples | `.fetchall()` or `.fetchone()` |
    | Get DataFrame | `.df()` |
    | Print results | `.show()` |
    | Query a CSV | `SELECT * FROM read_csv('file.csv')` |
    | Query a Parquet | `SELECT * FROM read_parquet('file.parquet')` |
    | Query a DataFrame | `SELECT * FROM my_dataframe` |
    | Use Python variables | `con.execute("... WHERE x > $1", [val])` |
    | Quick one-liner | `duckdb.sql("SELECT ...").show()` |
    """)
    return


if __name__ == "__main__":
    app.run()
