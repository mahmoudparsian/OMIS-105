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
    # 🎓 Week 8, Lab 1: First Normal Form (1NF) & Database Design (INSTRUCTOR SOLUTION)
    **Course**: Database Systems / Data Management
    **Tool**: DuckDB (In-Memory) & Marimo Notebooks

    ---

    ## 📌 Lab Objectives
    In this lab, students learn and apply the core principles of **First Normal Form (1NF)**:
    1. **Atomic Values**: Eliminating multi-value cells (e.g., CSV strings, comma-separated lists).
    2. **No Repeating Columns**: Eliminating numbered columns (e.g., `phone_1`, `phone_2`).
    3. **Primary Keys**: Ensuring every row is uniquely identifiable.
    4. **SQL Transformation**: Using DuckDB functions (`STRING_SPLIT`, `UNNEST`, `UNPIVOT`, and string parsing) to normalize messy datasets.
    """)
    return


@app.cell
def _(duckdb):
    # Initialize DuckDB in-memory database
    con = duckdb.connect(database=":memory:")

    # Dataset 1: Unnormalized Student Enrollments
    con.execute("""
        CREATE TABLE raw_student_enrollments (
            student_id INT,
            student_name VARCHAR,
            department VARCHAR,
            courses VARCHAR
        );
    """)
    con.execute("""
        INSERT INTO raw_student_enrollments VALUES
            (101, 'Alice Smith', 'Computer Science', 'CS101, CS102, MATH201'),
            (102, 'Bob Jones', 'Data Science', 'DS101, CS101'),
            (103, 'Charlie Brown', 'Computer Science', 'CS102'),
            (104, 'Diana Prince', 'Mathematics', 'MATH201, MATH202, STAT101');
    """)

    # Dataset 2: Unnormalized Customer Contacts
    con.execute("""
        CREATE TABLE raw_customer_contacts (
            customer_id INT,
            customer_name VARCHAR,
            phone_1 VARCHAR,
            phone_2 VARCHAR,
            phone_3 VARCHAR
        );
    """)
    con.execute("""
        INSERT INTO raw_customer_contacts VALUES
            (201, 'Acme Corp', '555-0100', '555-0101', NULL),
            (202, 'Beta LLC', '555-0200', NULL, NULL),
            (203, 'Gamma Inc', '555-0300', '555-0301', '555-0302');
    """)

    # Dataset 3: Unnormalized Employee Departments
    con.execute("""
        CREATE TABLE raw_employee_departments (
            emp_id INT,
            emp_info VARCHAR
        );
    """)
    con.execute("""
        INSERT INTO raw_employee_departments VALUES
            (301, 'Edward Miller (Engineering)'),
            (302, 'Fiona Gallagher (Marketing)'),
            (303, 'George Clark (Finance)');
    """)
    return (con,)


@app.cell
def _(con, mo):
    df_students = con.execute("SELECT * FROM raw_student_enrollments").df()
    df_contacts = con.execute("SELECT * FROM raw_customer_contacts").df()
    df_employees = con.execute("SELECT * FROM raw_employee_departments").df()

    mo.md(
        f"""
        ## 📊 Initial Unnormalized Datasets

        #### Dataset 1: `raw_student_enrollments`
        {mo.ui.table(df_students)}

        #### Dataset 2: `raw_customer_contacts`
        {mo.ui.table(df_contacts)}

        #### Dataset 3: `raw_employee_departments`
        {mo.ui.table(df_employees)}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## ✏️ Questions & Instructor Solutions
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Question 1 (Conceptual)
    Why does the `courses` column in `raw_student_enrollments` violate First Normal Form (1NF)?
    """)
    return


@app.cell
def _(mo):
    q1_solution = """
    **Instructor Solution:**
    The `courses` column violates 1NF because its values are non-atomic (multi-valued). 
    It stores multiple comma-separated values (e.g., 'CS101, CS102, MATH201') inside a single column cell, preventing standard index usage, atomic filtering, and direct aggregate operations.
    """
    mo.md(q1_solution)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Question 2 (SQL Query: `STRING_SPLIT` & `UNNEST`)
    Write a DuckDB SQL query using `STRING_SPLIT()` and `UNNEST()` to transform `raw_student_enrollments` so that each course enrollment occupies its own individual row.

    ---
    💡 **How to use `STRING_SPLIT` and `UNNEST` in DuckDB:**
    - **`STRING_SPLIT(string_column, 'delimiter')`**: Converts a single string with separated items into a DuckDB List array.
      *Example*: `STRING_SPLIT('CS101, CS102', ', ')` ➔ `['CS101', 'CS102']`
    - **`UNNEST(list_column)`**: Expands each element of a List into its own individual row.
    - **`TRIM(string)`**: Strips leading and trailing whitespace from the resulting items.

    *Syntax Template*:
    ```sql
    SELECT
        id_col,
        TRIM(UNNEST(STRING_SPLIT(comma_separated_col, ','))) AS item_name
    FROM table_name;
    ```
    """)
    return


@app.cell
def _(con, mo):
    q2_query = """
    SELECT 
        student_id,
        student_name,
        department,
        TRIM(UNNEST(STRING_SPLIT(courses, ','))) AS course_id
    FROM raw_student_enrollments;
    """

    df_q2 = con.execute(q2_query).df()
    mo.md(f"""**Instructor Solution Query:**
    ```sql
    {q2_query.strip()}
    ```
    {mo.ui.table(df_q2)}""")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Question 3 (DDL Schema Design)
    Write a SQL `CREATE TABLE` statement to define a 1NF compliant table named `student_courses_1nf`.
    Define appropriate column data types and specify a **Composite Primary Key**.
    """)
    return


@app.cell
def _(con, mo):
    q3_ddl = """
    CREATE TABLE IF NOT EXISTS student_courses_1nf (
        student_id INT,
        course_id VARCHAR,
        PRIMARY KEY (student_id, course_id)
    );
    """
    con.execute(q3_ddl)
    mo.md(f"""**Instructor Solution DDL:**
    ```sql
    {q3_ddl.strip()}
    ```""")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Question 4 (Conceptual)
    Why does the schema of `raw_customer_contacts` (`phone_1`, `phone_2`, `phone_3`) violate 1NF, even though each cell contains a single phone number?
    """)
    return


@app.cell
def _(mo):
    q4_solution = """
    **Instructor Solution:**
    It violates 1NF because it introduces repeating groups/columns across the horizontal row structure. 
    This creates an arbitrary limit on phone numbers per customer, forces schema modifications (`ALTER TABLE`) if a 4th number is needed, and causes sparse tables filled with `NULL` values.
    """
    mo.md(q4_solution)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Question 5 (SQL `UNPIVOT`)
    Use DuckDB's `UNPIVOT` clause to transform `raw_customer_contacts` into a 1NF table structure where all phone numbers are stored in a single `phone_number` column, excluding `NULL` values.

    ---
    💡 **How to use `UNPIVOT` in DuckDB:**
    - **`UNPIVOT`**: Transposes wide repeating columns across a row into tall individual rows. DuckDB automatically excludes `NULL` values during unpivoting!
    - **`ON col_1, col_2, ...`**: Specifies the list of repeating columns to collapse.
    - **`INTO NAME label_col VALUE data_col`**: Sets the name for the category label column and the value data column.

    *Syntax Template*:
    ```sql
    UNPIVOT table_name
    ON column_1, column_2, column_3
    INTO
        NAME column_label_name
        VALUE column_value_name;
    ```
    """)
    return


@app.cell
def _(con, mo):
    q5_query = """
    UNPIVOT raw_customer_contacts
    ON phone_1, phone_2, phone_3
    INTO
        NAME phone_type
        VALUE phone_number;
    """

    df_q5 = con.execute(q5_query).df()
    mo.md(f"""**Instructor Solution Query:**
    ```sql
    {q5_query.strip()}
    ```
    {mo.ui.table(df_q5)}""")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Question 6 (SQL String Parsing)
    In `raw_employee_departments`, the `emp_info` column contains both employee name and department in one string (e.g., `'Edward Miller (Engineering)'`).
    Write a DuckDB SQL query using string parsing functions to separate `emp_name` and `department` into distinct columns.

    ---
    💡 **How to perform String Parsing in DuckDB:**
    - **`SPLIT_PART(string, delimiter, part_number)`**: Splits a string by a delimiter and extracts the specific 1-indexed part.
      *Example*: `SPLIT_PART('Edward Miller (Engineering)', '(', 1)` ➔ `'Edward Miller '`
    - **`REPLACE(string, 'from', 'to')`**: Replaces occurrences of a substring.
      *Example*: `REPLACE('Engineering)', ')', '')` ➔ `'Engineering'`
    - **`TRIM(string)`**: Removes surrounding spaces.

    *Syntax Template*:
    ```sql
    SELECT
        emp_id,
        TRIM(SPLIT_PART(emp_info, '(', 1)) AS emp_name,
        REPLACE(SPLIT_PART(emp_info, '(', 2), ')', '') AS department
    FROM table_name;
    ```
    """)
    return


@app.cell
def _(con, mo):
    q8_query = """
    SELECT 
        emp_id,
        TRIM(SPLIT_PART(emp_info, '(', 1)) AS emp_name,
        REPLACE(SPLIT_PART(emp_info, '(', 2), ')', '') AS department
    FROM raw_employee_departments;
    """

    df_q6 = con.execute(q8_query).df()
    mo.md(f"""**Instructor Solution Query:**
    ```sql
    {q8_query.strip()}
    ```
    {mo.ui.table(df_q6)}""")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Question 7 (Primary Key Identification)
    In a normalized student course enrollment table with columns `(student_id, student_name, course_id, grade)`, which column or combination of columns forms the **Primary Key**? Explain why.
    """)
    return


@app.cell
def _(mo):
    q7_solution = """
    **Instructor Solution:**
    The composite primary key is **`(student_id, course_id)`**.

    *Explanation*: `student_id` alone is not unique because a student can enroll in multiple courses. `course_id` alone is not unique because multiple students can take the same course. The combination of `(student_id, course_id)` uniquely identifies each student's enrollment record in a course.
    """
    mo.md(q7_solution)
    return


if __name__ == "__main__":
    app.run()
