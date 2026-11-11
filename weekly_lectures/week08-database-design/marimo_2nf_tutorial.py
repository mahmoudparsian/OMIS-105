import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import duckdb
    import pandas as pd
    return duckdb, mo, pd


@app.cell
def __(mo):
    mo.md(
        r"""
        # 🔑 Database Design & Second Normal Form (2NF) with DuckDB

        Welcome to the interactive guide on **Second Normal Form (2NF)**!

        ---

        ### 🎯 Core Concepts Covered
        1. **Prerequisite for 2NF**: The table must already be in **1NF**.
        2. **Composite Keys & Partial Dependency**: What happens when non-key attributes depend on only *part* of a multi-column primary key.
        3. **Drawbacks of Partial Dependencies**: Redundant data, update anomalies, and insert/delete issues.
        4. **Decomposition**: Splitting 1NF tables into multiple 2NF tables using DuckDB SQL (`CREATE TABLE AS SELECT DISTINCT ...`).
        """
    )
    return


@app.cell
def __(duckdb):
    # Initialize an in-memory DuckDB database
    con = duckdb.connect(database=":memory:")

    # Create 1NF table with a Composite Primary Key (student_id, course_id)
    # This table has a partial dependency: instructor_name depends ONLY on course_id!
    con.execute("""
        CREATE TABLE student_courses_1nf (
            student_id INT,
            course_id VARCHAR,
            student_name VARCHAR,
            course_name VARCHAR,
            instructor_name VARCHAR,
            grade VARCHAR,
            PRIMARY KEY (student_id, course_id)
        );
    """)

    con.execute("""
        INSERT INTO student_courses_1nf VALUES
            (101, 'CS101', 'Alice', 'Intro to SQL', 'Prof. Miller', 'A'),
            (101, 'CS102', 'Alice', 'Data Structures', 'Prof. Davis', 'B'),
            (102, 'CS101', 'Bob', 'Intro to SQL', 'Prof. Miller', 'A'),
            (103, 'CS102', 'Charlie', 'Data Structures', 'Prof. Davis', 'A'),
            (103, 'CS103', 'Charlie', 'Database Systems', 'Prof. Miller', 'C');
    """)

    # Decomposed 2NF Tables
    con.execute("""
        CREATE TABLE students_2nf AS 
        SELECT DISTINCT student_id, student_name FROM student_courses_1nf;
    """)

    con.execute("""
        CREATE TABLE courses_2nf AS 
        SELECT DISTINCT course_id, course_name, instructor_name FROM student_courses_1nf;
    """)

    con.execute("""
        CREATE TABLE enrollments_2nf AS 
        SELECT student_id, course_id, grade FROM student_courses_1nf;
    """)
    return con,


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 🚨 The Problem: Table in 1NF, but Violating 2NF

        Look at the table below. The primary key is **Composite**: `(student_id, course_id)`.

        ### What is a Partial Dependency?
        * `student_name` depends **only** on `student_id` (not `course_id`).
        * `course_name` and `instructor_name` depend **only** on `course_id` (not `student_id`).
        * `grade` depends on **BOTH** `student_id` and `course_id` (this attribute is fully dependent on the whole key!).

        ### Why is this BAD?
        * **Redundancy**: `Intro to SQL` and `Prof. Miller` are repeated every time a student registers for CS101.
        * **Update Anomaly**: If Prof. Miller changes classrooms, you must update multiple rows across the database.
        * **Insertion Anomaly**: You cannot add a new course until at least one student enrolls in it!
        """
    )
    return


@app.cell
def __(con, mo):
    df_1nf = con.execute("SELECT * FROM student_courses_1nf").df()
    mo.md(f"### ❌ Table in 1NF (Violates 2NF due to Partial Dependencies)\n{mo.ui.table(df_1nf)}")
    return df_1nf,


@app.cell
def __(mo):
    mo.md(
        r"""
        ## ✅ The 2NF Fix: Table Decomposition

        To satisfy **2NF**, we remove partial dependencies by breaking the single unnormalized table into **3 separate tables**:

        1. **`Students`**: Maps `student_id` ➔ `student_name`
        2. **`Courses`**: Maps `course_id` ➔ `course_name`, `instructor_name`
        3. **`Enrollments`**: Linking table with `(student_id, course_id)` ➔ `grade`
        """
    )
    return


@app.cell
def __(con, mo):
    df_students = con.execute("SELECT * FROM students_2nf").df()
    df_courses = con.execute("SELECT * FROM courses_2nf").df()
    df_enrollments = con.execute("SELECT * FROM enrollments_2nf").df()

    mo.md(
        f"""
        ### ✅ Decomposed 2NF Tables

        #### 1. Students Table (`student_id` is Primary Key)
        {mo.ui.table(df_students)}

        #### 2. Courses Table (`course_id` is Primary Key)
        {mo.ui.table(df_courses)}

        #### 3. Enrollments Table (`(student_id, course_id)` is Composite Primary Key)
        {mo.ui.table(df_enrollments)}
        """
    )
    return df_courses, df_enrollments, df_students


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 🛠️ DuckDB Magic: Rejoining 2NF Tables with `JOIN`

        Normalizing tables into 2NF prevents duplication, but what if you need the full combined report back?
        You can easily perform an inner join using DuckDB SQL:
        """
    )
    return


@app.cell
def __(con, mo):
    join_query = """
    SELECT 
        e.student_id,
        s.student_name,
        e.course_id,
        c.course_name,
        c.instructor_name,
        e.grade
    FROM enrollments_2nf e
    JOIN students_2nf s ON e.student_id = s.student_id
    JOIN courses_2nf c ON e.course_id = c.course_id;
    """

    reconstructed_df = con.execute(join_query).df()

    mo.md(
        f"""
        ### 🔄 Reconstructed View using SQL JOIN
        ```sql
        {join_query.strip()}
        ```
        {mo.ui.table(reconstructed_df)}
        """
    )
    return join_query, reconstructed_df


@app.cell
def __(mo):
    student_selector = mo.ui.dropdown(
        options=['Alice', 'Bob', 'Charlie'],
        value='Alice',
        label='Select Student to Query:'
    )
    student_selector
    return student_selector,


@app.cell
def __(con, mo, student_selector):
    filtered_df = con.execute("""
        SELECT 
            s.student_name,
            c.course_name,
            c.instructor_name,
            e.grade
        FROM enrollments_2nf e
        JOIN students_2nf s ON e.student_id = s.student_id
        JOIN courses_2nf c ON e.course_id = c.course_id
        WHERE s.student_name = ?
    """, [student_selector.value]).df()

    mo.md(
        f"""
        ### 🔍 Interactive Query on Normalized Schema
        Showing course schedule and grades for **{student_selector.value}**:

        {mo.ui.table(filtered_df)}
        """
    )
    return filtered_df,


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## 💡 Summary Checklist for 2NF

        | Condition | Requirement |
        | :--- | :--- |
        | **1NF Compliance** | Table must already satisfy all 1NF rules (atomic values, primary key, no repeating columns). |
        | **Composite Primary Key** | 2NF is only an issue if the primary key consists of two or more columns. |
        | **No Partial Dependencies** | Every non-key column must depend on the **entire** composite key, not just part of it. |
        | **Decomposition** | Move partially dependent columns into their own dedicated table. |
        """
    )
    return


if __name__ == "__main__":
    app.run()
