import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import pandas as pd

    return duckdb, mo


@app.cell
def _(mo):
    mo.md(r"""
    # 🗄️ Database Design & First Normal Form (1NF) with DuckDB

    Welcome! This interactive notebook will teach you the fundamental principles of relational database design and **First Normal Form (1NF)**.

    ---

    ### 🎯 Core Concepts Covered
    1. **What is Database Normalization?** Why do we structure data?
    2. **Rules of First Normal Form (1NF)**:
       - Atomic values (no list/multi-value attributes per cell).
       - Unique record identification (Primary Keys).
       - Order independence for rows and columns.
    3. **DuckDB SQL Transformations**: How to take messy non-1NF data and clean it up using SQL functions like `UNNEST()` and `STRING_SPLIT()`.
    """)
    return


@app.cell
def _(duckdb):
    # Initialize an in-memory DuckDB database
    con = duckdb.connect(database=":memory:")

    # Create unnormalized table (violates 1NF)
    con.execute("""
        CREATE TABLE student_courses_non_1nf (
            student_id INT,
            student_name VARCHAR,
            enrolled_courses VARCHAR
        );
    """)

    con.execute("""
        INSERT INTO student_courses_non_1nf VALUES
            (101, 'Alice Smith', 'SQL Basics, Data Analysis, Python'),
            (102, 'Bob Jones', 'Web Dev, SQL Basics'),
            (103, 'Charlie Brown', 'Python');
    """)

    # Create normalized table (1NF Compliant)
    con.execute("""
        CREATE TABLE student_courses_1nf (
            student_id INT,
            course_name VARCHAR,
            PRIMARY KEY (student_id, course_name)
        );
    """)

    con.execute("""
        INSERT INTO student_courses_1nf VALUES
            (101, 'SQL Basics'),
            (101, 'Data Analysis'),
            (101, 'Python'),
            (102, 'Web Dev'),
            (102, 'SQL Basics'),
            (103, 'Python');
    """)
    return (con,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 🚨 Example 1: Non-Atomic Values (The Multi-Value Problem)

    Look at the table below. The `enrolled_courses` column contains multiple course names stored inside a single cell separated by commas.

    ### Why is this BAD?
    * How do you query for students taking `'SQL Basics'`? A standard `=` won't work; you would have to use fragile string searches like `LIKE '%SQL Basics%'`.
    * You cannot easily `COUNT()` how many students are enrolled in each individual course.
    * Adding or dropping a course requires complex string manipulation rather than simple `INSERT` or `DELETE` statements.
    """)
    return


@app.cell
def _(con, mo):
    df_non_1nf = con.execute("SELECT * FROM student_courses_non_1nf").df()
    mo.md(f"### ❌ Table Before 1NF (Unnormalized)\n{mo.ui.table(df_non_1nf)}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## ✅ Applying 1NF: Atomic Values & Primary Keys

    To satisfy **1NF**, every cell in a table must contain **a single, indivisible (atomic) value**.
    Instead of stacking courses into one cell, each course enrollment gets its own dedicated row.

    * Each row represents **one student enrolled in one course**.
    * The combination of `(student_id, course_name)` serves as the **Composite Primary Key**.
    """)
    return


@app.cell
def _(con, mo):
    df_1nf = con.execute("SELECT * FROM student_courses_1nf").df()
    mo.md(f"### ✅ Table in 1NF (Normalized)\n{mo.ui.table(df_1nf)}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 🛠️ DuckDB Magic: Normalizing Non-1NF Data with SQL

    If you inherit a database with comma-separated values, DuckDB makes it trivial to convert it into **1NF** using `STRING_SPLIT()` and `UNNEST()`.

    Try running the SQL query transformation below interactively!
    """)
    return


@app.cell
def _(con, mo):
    transform_query = """
    SELECT 
        student_id,
        student_name,
        TRIM(UNNEST(STRING_SPLIT(enrolled_courses, ','))) AS course_name
    FROM student_courses_non_1nf;
    """

    transformed_df = con.execute(transform_query).df()

    mo.md(
        f"""
        ### 🔄 Live SQL Transformation Result
        ```sql
        {transform_query.strip()}
        ```
        {mo.ui.table(transformed_df)}
        """
    )
    return


@app.cell
def _(mo):
    selected_course = mo.ui.dropdown(
        options=['SQL Basics', 'Python', 'Data Analysis', 'Web Dev'],
        value='SQL Basics',
        label='Select a Course to Filter:'
    )
    selected_course
    return (selected_course,)


@app.cell
def _(con, mo, selected_course):
    filtered_df = con.execute(
        "SELECT * FROM student_courses_1nf WHERE course_name = ?",
        [selected_course.value]
    ).df()

    mo.md(
        f"""
        ### 🔍 Demonstrating Query Simplicity in 1NF
        Because the data is in **1NF**, filtering for students in a specific course is a straightforward, indexable SQL query:

        ```sql
        SELECT * FROM student_courses_1nf WHERE course_name = '{selected_course.value}';
        ```
        {mo.ui.table(filtered_df)}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## 📋 Summary: Checklist for First Normal Form (1NF)

    | Rule | Description |
    | :--- | :--- |
    | **Atomic Values** | Each cell contains exactly one scalar value (no lists, arrays, or CSV strings). |
    | **No Repeating Groups** | Do not create columns like `course_1`, `course_2`, `course_3`. |
    | **Primary Key Identified** | Every table must have a primary key (single column or composite) that uniquely identifies each row. |
    | **Order Independence** | The order of rows and columns does not affect data meaning or retrieval. |
    """)
    return


if __name__ == "__main__":
    app.run()
