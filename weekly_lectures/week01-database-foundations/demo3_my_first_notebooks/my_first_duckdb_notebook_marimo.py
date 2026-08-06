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
    # 🦆 My Very First DuckDB + Jupyter Notebook

    ### This notebook is intentionally simple.

    ### We will learn:

    1. How to connect to DuckDB

    2. How to create a table

    3. How to insert rows

    4. How to run basic SQL queries

    ### This notebook is designed to be:
    - beginner friendly
    - minimal
    - runnable many times from beginning to end
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Step 1 — Import DuckDB

    ### DuckDB lets us run SQL directly inside Jupyter Notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 1.1 Make Sure that DuckDB is installed...
    """)
    return


@app.cell
def _():
    # 1.1 DuckDB is installed automatically via the PEP 723
    # dependencies listed at the top of this file.
    # The connection cell below imports duckdb and creates the connection.
    print("Step 1.1: DuckDB is ready (installed via PEP 723 metadata).")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 1.2 Create a Connection to DuckDB
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect(database=":memory:")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Step 2 — Create Table and Insert 10 Rows

    `CREATE OR REPLACE TABLE` makes the notebook re-runnable —
    if the table already exists, it is replaced automatically.
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE students AS
        SELECT * FROM (VALUES
            (100, 'Alex',   'Business', 20, 3.5),
            (200, 'Jeff',   'Business', 21, 3.7),
            (300, 'Rafa',   'AI',       22, 3.9),
            (400, 'Susan',  'Finance',  20, 3.6),
            (500, 'Jen',    'Finance',  21, 3.8),
            (600, 'Barb',   'AI',       23, 3.4),
            (700, 'Dara',   'Business', 22, 3.2),
            (800, 'Venus',  'AI',       21, 4.0),
            (900, 'Margie', 'Finance',  20, 3.3),
            (910, 'Betty',  'Business', 22, 3.9)
        ) AS t(student_id, student_name, major, age, gpa)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 2.1 Describe Table
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        DESCRIBE students
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Step 5 — Read All Rows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5.1 Read ALL Rows
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT
                *
            FROM students
            ORDER BY student_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5.2 Read ALL Rows Ordered by `student_id` (1 -> 100)
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT
                *
            FROM students
            ORDER BY student_id
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 5.3 Get/Read all rows from `students` table (100 -> 1)
    """)
    return


@app.cell
def _(mo, students):
    rows = mo.sql(
        f"""
        SELECT *
        FROM students
        ORDER BY student_id DESC
        """
    )
    return (rows,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 5.4 Iterate retrieved rows one-by-one
    """)
    return


@app.cell
def _(rows):
    # iterate retrieved rows one-by-one

    print("type(rows)=", type(rows))
    #
    print("----\n")
    for index, row in rows.iterrows():
        print("index=", index)
        print("type(row)=", type(row))
        print(row)
        print("----\n")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Step 6 — Show student names only (ordered)
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT
                student_name
            FROM students
            ORDER BY student_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Step 7 — Show Business students
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT
                *
            FROM students
            WHERE major = 'Business'
            ORDER BY student_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Step 7.1  — Show Business students (use a variable)
    """)
    return


@app.cell
def _(mo, students):
    major_name = "Business"
    _df = mo.sql(
        f"""
        SELECT *
        FROM students
        WHERE major = '{major_name}'
        ORDER BY student_name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Step 8 — Show students older than 21
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT
                *
            FROM students
            WHERE age > 21
            ORDER BY age
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Step 9 — Show top 3 GPAs
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT
                student_name,
                gpa
            FROM students
            ORDER BY gpa DESC
            LIMIT 3
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Step 10 — Count students per major
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT
                major,
                COUNT(*) AS student_count
            FROM students
            GROUP BY major
            ORDER BY student_count DESC
        """
    )
    return


@app.cell
def _(mo, students):
    df = mo.sql(
        f"""
        SELECT
            major,
            COUNT(*) AS student_count
        FROM students
        GROUP BY major
        ORDER BY student_count DESC
        """
    )
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Plot:  Count students per Major
    """)
    return


@app.cell
def _(df):
    # Count students per Major
    df.plot(kind='bar', x='major', y='student_count', title='Count students per Major')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Plot: Count students per Major (pie chart)
    """)
    return


@app.cell
def _(df):
    df.set_index("major").plot(
        kind="pie",
        y="student_count",
        autopct="%1.1f%%",
        figsize=(6, 6),
        legend=False,
        ylabel="",
        title="Students per Major"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 11. Add 2 more new rows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 11.1 Add one more row using a List of values
    """)
    return


@app.cell
def _(mo, students):
    # Add one more row
    _df = mo.sql(
        f"""
        INSERT INTO students VALUES (970, 'Carlos', 'Business', 37, 3.8)
        """
    )
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT * FROM students WHERE student_id = 970
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 11.2 Add one more row using a Dictionary of values
    """)
    return


@app.cell
def _(mo, students):
    # Add one more row
    _df = mo.sql(
        f"""
        INSERT INTO students VALUES (980, 'Sasha', 'Business', 22, 3.3)
        """
    )
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        SELECT * FROM students WHERE student_id = 980
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 12. DELETE a Record

    <div style="background-color:#FFF3CD;
                padding:12px;
                border-radius:8px;">

    # Important Note

    Always use `WHERE` with `DELETE` statements.

    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Delete a student with student_id = 300
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


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        DELETE 
            FROM students
            WHERE student_id = 300
        """
    )
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
    mo.md(r"""
    ---
    # 13. Save Table To Disk/File
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        COPY students TO 'students.csv'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Summary

    ### In this notebook, we learned how to:
    1. connect to DuckDB
    2. create a table
    3. insert rows
    4. run basic SQL queries

    ### We used:
    - `CREATE`
    - `SELECT`
    - `WHERE`
    - `ORDER BY`
    - `LIMIT`
    - `GROUP BY`
    """)
    return


if __name__ == "__main__":
    app.run()
