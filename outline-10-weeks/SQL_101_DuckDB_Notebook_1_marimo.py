import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Welcome to Marimo and DuckDB!

    * **Course:** OMIS 105 — Introduction to Database Management Systems
    * **Instructor:** Dr. Mahmoud Parsian
    * **Tool:** Marimo — an interactive notebook for SQL and Python
    * **DuckDB** a powerful database

    ---

    ## What Is a Notebook?

    A **notebook** is a document made of **cells**. <br>
    Each cell can contain:

    - **Text** (like what you're reading right now) — for explanations
    - **SQL** — to ask questions of a database
    - **Python** — to run code, make charts, etc.

    You read the text cells, then **run** the SQL/code cells to see results.
    Think of it like a lab workbook where the experiments run themselves.

    ## How to Use This Notebook

    1. **Read** the text cells (like this one)
    2. **Look at** the SQL cells below each explanation — they show both the query and the result
    3. **Try editing** a SQL cell and pressing **Cmd+Enter** (Mac) or **Ctrl+Enter** (Windows) to re-run it
    4. Notice how **downstream cells update automatically** — that's Marimo's superpower!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Your First Database

    * A **database** is an organized collection of data stored in **tables**.
    * A **table** looks like a spreadsheet — it has **rows** (records) and **columns** (fields).

    Let's create a tiny table of students and their favorite foods.
    The cell below is a **SQL cell** — it contains a command that creates a table.

    ![](https://media.geeksforgeeks.org/wp-content/uploads/20260124113248518106/rdbms_4.webp)



    Your First Database

    * A database is an organized collection of data stored in tables.

    * A table looks like a spreadsheet — it has rows (records) and columns (fields).

    * Let's create a tiny table of students and their favorite foods.


    ![](https://www.pragimtech.com/blog/contribute/article_images/2220211210231003/what-is-a-relational-database.jpg)
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    # Create a Connection to DuckDB
    """)
    return


@app.cell
def _():
    # Python Cell

    import duckdb
    con = duckdb.connect(database=":memory:")
    print("DuckDB version: ", duckdb.__version__)
    print("DuckDB Connection Object: ", con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Create a database table called "students"
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- SQL Cell
        CREATE OR REPLACE TABLE students (
            student_id   INTEGER,
            name         VARCHAR,
            major        VARCHAR,
            favorite_food VARCHAR
        );
        """
    )
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        -- SQL cell
        -- Describe the structure of students table
        DESC students;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    We just told the database: *"Create a table called `students` with four columns."*

    But the table is empty!

    ---

    # Let's add some data:
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        -- SQL cell
        INSERT INTO students (student_id, name, major, favorite_food) 
        VALUES
            (1, 'Alice',   'Marketing',  'Pizza'),
            (2, 'Bob',     'Finance',    'Sushi'),
            (3, 'Carol',   'Accounting', 'Tacos'),
            (4, 'David',   'Marketing',  'Pasta'),
            (5, 'Eva',     'Finance',    'Pizza'),
            (6, 'Frank',   'Accounting', 'Sushi'),
            (7, 'Rafa',    'Sports',     'Pizza');
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Now let's **look** at our data. The SQL command `SELECT * FROM students`
    means *"show me everything in the students table."*
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM students
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Asking Questions with SQL

    SQL stands for **Structured Query Language**. It's how you ask a database
    to answer business questions. You don't need to be a programmer — SQL reads
    almost like English.

    ---

    **Question 1:** *"Who are the Marketing majors?"*
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT name, 
               major
        FROM   students
        WHERE  major = 'Marketing'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Read that SQL out loud: *"Select the name and major from students where the major is Marketing."*
    It's almost plain English!

    ---

    **Question 2:** *"Who likes Pizza?"*
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT name, 
               favorite_food
        FROM   students
        WHERE  favorite_food = 'Pizza'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    **Question 3:** *"How many students are in each major?"*

    The `GROUP BY` command groups rows together, and `COUNT(*)` counts them:
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT major,
               COUNT(*) AS num_students
        FROM   students
        GROUP BY major
        ORDER BY num_students DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Try It Yourself!

    Here's the fun part. **Edit the SQL cell below** and press **Cmd+Enter** (Mac) or **Ctrl+Enter** (Windows) to run it.

    Some ideas to try:

    - Change `'Pizza'` to `'Sushi'` and see who likes Sushi
    - Change `favorite_food` to `major` to group by major instead
    - Change `COUNT(*)` to see what happens if you remove it
    - Add your own name! Try: `INSERT INTO students VALUES (7, 'YourName', 'OMIS', 'Ramen')`
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        -- Edit this query! Try different foods, different columns, or add yourself.
        SELECT name, 
               favorite_food
        FROM   students
        WHERE  favorite_food = 'Pizza'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## What Makes Marimo Special?

    Marimo is **reactive** — when you change one cell,   <br>
    every cell that depends on it updates automatically. <br>
    You never have to worry about running cells in the   <br>
    right order or getting stale results.

    This is different from regular scripts where you run      <br>
    everything top-to-bottom and hope nothing is out of date. <br>
    In Marimo, the notebook always shows you the truth.

    ---
    ## What You'll Learn This Quarter

    | Week | Topic | What You'll Be Able to Do |
    |------|-------|---------------------------|
    | 1 | Database Foundations | Understand what databases are and why businesses need them |
    | 2 | Relational Modeling | Design tables that avoid data problems |
    | 3 | SQL Basics | Write SELECT, WHERE, ORDER BY, GROUP BY |
    | 4 | SQL Aggregation | Compute totals, averages, rankings |
    | 5 | SQL Joins | Combine data from multiple tables |
    | 6 | Database Design | Normalize data, define constraints |
    | 7 | Query Performance | Make queries run fast with indexes |
    | 8 | Transactions | Keep data safe and consistent |
    | 9 | Project Integration | Build a complete database project |
    | 10 | Review & Modern Data | Wrap up and look ahead |

    Every class will use Marimo notebooks like this one. You'll write SQL,
    see results instantly, and build up your skills week by week.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Practice, be Hand-on, and Learn!
    """)
    return


if __name__ == "__main__":
    app.run()
