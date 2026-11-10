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
    # 🧪 Week 8, Lab 1: First Normal Form (1NF) & Database Design
    **Course**: Database Systems / Data Management
    **Tool**: DuckDB (In-Memory) & Marimo Notebooks

    ---

    ## 📌 Lab Objectives
    In this lab, you will learn and apply the core principles of **First Normal Form (1NF)**:
    1. **Atomic Values**: Eliminating multi-value cells (e.g., CSV strings, comma-separated lists).
    2. **No Repeating Columns**: Eliminating numbered columns (e.g., `phone_1`, `phone_2`).
    3. **Primary Keys**: Ensuring every row is uniquely identifiable.
    4. **SQL Transformation**: Using DuckDB functions (`STRING_SPLIT`, `UNNEST`, `UNPIVOT`, and string parsing) to normalize messy datasets.

    ---

    ## 📖 Quick Reference: 1NF Rules
    * **Rule 1**: Every column cell must contain a single, indivisible (atomic) value.
    * **Rule 2**: No repeating columns/groups for similar data.
    * **Rule 3**: Each record must be uniquely identifiable via a Primary Key (single column or composite).
    """)
    return


@app.cell
def _(duckdb):
    # Initialize DuckDB in-memory database
    con = duckdb.connect(database=":memory:")

    # Dataset 1: Unnormalized Student Enrollments (Violates 1NF - Non-atomic multi-values)
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

    # Dataset 2: Unnormalized Customer Contacts (Violates 1NF - Repeating Columns)
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

    # Dataset 3: Unnormalized Employee Departments (Violates 1NF - Combined String Attributes)
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
    ## ✏️ Student Exercises (7 Essential Questions)

    Complete the SQL queries or answers in each placeholder below.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Question 1 (Conceptual)
    Why does the `courses` column in `raw_student_enrollments` violate First Normal Form (1NF)? Explain in 1-2 sentences.
    """)
    return


@app.cell
def _(mo):
    # TODO: Write your answer below
    q1_answer = """
    YOUR ANSWER HERE
    """
    mo.md(f"""**Your Answer:**
    {q1_answer}""")
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
    # TODO: Replace the placeholder query with your DuckDB SQL code
    q2_query = """
    -- WRITE YOUR SQL QUERY HERE
    SELECT * FROM raw_student_enrollments;
    """

    df_q2 = con.execute(q2_query).df()
    mo.md(f"""```sql
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
def _(mo):
    # TODO: Execute your CREATE TABLE statement here
    q3_ddl = """
    -- WRITE YOUR CREATE TABLE STATEMENT HERE
    CREATE TABLE IF NOT EXISTS student_courses_1nf (
        -- define columns and primary key
        student_id INT
    );
    """
    # con.execute(q3_ddl)
    mo.md(f"""```sql
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
    q4_answer = """
    YOUR ANSWER HERE
    """
    mo.md(f"""**Your Answer:**
    {q4_answer}""")
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
    # TODO: Write your UNPIVOT query
    q5_query = """
    -- WRITE YOUR UNPIVOT QUERY HERE
    SELECT * FROM raw_customer_contacts;
    """

    df_q5 = con.execute(q5_query).df()
    mo.md(f"""```sql
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
    # TODO: Write string parsing query
    q6_query = """
    -- WRITE YOUR QUERY TO PARSE emp_info HERE
    SELECT emp_id, emp_info FROM raw_employee_departments;
    """

    df_q6 = con.execute(q6_query).df()
    mo.md(f"""```sql
    {q6_query.strip()}
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
    q7_answer = """
    YOUR ANSWER HERE
    """
    mo.md(f"""**Your Answer:**
    {q7_answer}""")
    return


if __name__ == "__main__":
    app.run()
