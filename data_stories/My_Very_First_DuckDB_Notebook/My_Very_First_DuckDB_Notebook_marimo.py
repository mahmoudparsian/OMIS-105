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
    # My Very First DuckDB Notebook
    **Course:** OMIS 105 — Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Topic:** Getting started with SQL using DuckDB

    ---

    ### What You Will Learn
    - How to **connect** to an in-memory DuckDB database
    - How to **create a table** with a simple schema
    - How to **insert rows** into the table
    - How to **query** data with `SELECT`
    - How to **filter** rows with `WHERE`
    - How to **sort** results with `ORDER BY`
    - How to **count** and **aggregate** with `COUNT`, `AVG`, `SUM`

    ### Key Concepts

    1. We use an **in-memory** database (`':memory:'`).

    2. This means the database lives only while the notebook kernel is running.

    3. You can **re-run this notebook from top to bottom** as many times as you want — it will always produce the same results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 1 — Import DuckDB and Connect
    """)
    return


@app.cell
def _():
    #------------------------------------------
    # 1.1 Bullet-proof install and import block
    #------------------------------------------
    import sys
    import subprocess
    import duckdb

    return (duckdb,)


@app.cell
def _(duckdb):
    #------------------------------------------
    # 1.2 Connect to a DuckDB database
    #------------------------------------------
    # Connect to an in-memory database (no file on disk)
    con = duckdb.connect(database=':memory:')
    print("Connected to DuckDB (in-memory)")
    print(f"DuckDB version: {duckdb.__version__}")
    print("con=", con)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 2 — Create the `students` Table

    Our table has 4 columns:

    | Column     | Type    | Description            |
    |------------|---------|------------------------|
    | student_id | INTEGER | Unique ID (primary key)|
    | name       | VARCHAR | Student's first name   |
    | major      | VARCHAR | Area of study          |
    | gpa        | DECIMAL | Grade point average    |
    """)
    return


@app.cell
def _(con):
    # In DuckDB, the CREATE OR REPLACE TABLE students 
    # command is shorthand for dropping an existing 
    # table named "students" and creating a new one 
    # with the same name

    con.execute("""
        CREATE
        OR REPLACE TABLE students ( student_id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, major VARCHAR NOT NULL, gpa DECIMAL(3, 2) NOT NULL );
    """)
    print("Table 'students' created successfully.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 3 — Insert 10 Rows
    """)
    return


@app.cell
def _(con):
    con.execute("""
        INSERT INTO students
        VALUES
            (1, 'Alice', 'Computer Science', 3.80),
            (2, 'Bob', 'Mathematics', 3.20),
            (3, 'Carol', 'Computer Science', 3.95),
            (4, 'David', 'Business', 2.90),
            (5, 'Eva', 'Mathematics', 3.60),
            (6, 'Frank', 'Business', 3.10),
            (7, 'Grace', 'Computer Science', 3.70),
            (8, 'Henry', 'Business', 3.45),
            (9, 'Ivy', 'Mathematics', 3.85),
            (10, 'Jack', 'Computer Science', 2.75);
    """)
    print("10 rows inserted successfully.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 4 — View All Rows

    The simplest SQL query: `SELECT * FROM students`
    The `*` means "give me all columns."
    """)
    return


@app.cell
def _(con):
    # select/view ALL rows:

    con.execute("""
        SELECT *
        FROM students
        ORDER BY student_id;
    """).fetchdf()
    return


@app.cell
def _(con):
    # select/view ALL rows:

    con.sql("""
        SELECT *
        FROM students
        ORDER BY student_id;
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 5 — Filter with `WHERE`

    Find all Computer Science students:
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            student_id,
            name,
            gpa
        FROM students
        WHERE major = 'Computer Science'
        ORDER BY gpa DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Find students with GPA above 3.5:
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            name,
            major,
            gpa
        FROM students
        WHERE gpa > 3.5
        ORDER BY gpa DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 6 — Sort with `ORDER BY`

    List all students sorted by GPA (lowest first):
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            name,
            major,
            gpa
        FROM students
        ORDER BY gpa ASC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 7 — Count Rows

    How many students are in each major?
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            major,
            COUNT(*) AS num_students
        FROM students
        GROUP BY major
        ORDER BY num_students DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 8 — Aggregate: `AVG` and `SUM`

    What is the **average GPA** per major?
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            major,
            ROUND(AVG(gpa), 2) AS avg_gpa,
            ROUND(MIN(gpa), 2) AS min_gpa,
            ROUND(MAX(gpa), 2) AS max_gpa
        FROM students
        GROUP BY major
        ORDER BY avg_gpa DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 9 — Top N with `LIMIT`

    Show only the **top 3** students by GPA:
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT
            name,
            major,
            gpa
        FROM students
        ORDER BY gpa DESC
        LIMIT 3;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 10 — Close the Connection

    Always close the connection when you're done:
    """)
    return


@app.cell
def _(con):
    con.close()
    print("Connection closed. Done!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    In this notebook you learned **9 fundamental SQL concepts**:

    | #  | Concept       | SQL Keyword   | What It Does                     |
    |----|---------------|---------------|----------------------------------|
    | 1  | Connect       | `duckdb.connect()` | Open a database connection  |
    | 2  | Create Table  | `CREATE TABLE`| Define columns and data types    |
    | 3  | Insert Data   | `INSERT INTO` | Add rows to a table              |
    | 4  | Select All    | `SELECT *`    | Retrieve all columns             |
    | 5  | Filter        | `WHERE`       | Keep only matching rows          |
    | 6  | Sort          | `ORDER BY`    | Arrange rows in order            |
    | 7  | Count         | `COUNT(*)`    | Count rows per group             |
    | 8  | Aggregate     | `AVG, MIN, MAX` | Compute summary statistics    |
    | 9  | Top N         | `LIMIT`       | Return only the first N rows     |

    ### Key Takeaway

    > You can **re-run this notebook** from top to bottom
    > (`Kernel → Restart & Run All`) as many times as you want.
    > Because we use an **in-memory** database, each run
    > starts fresh — no leftover data, no conflicts.
    """)
    return


if __name__ == "__main__":
    app.run()
