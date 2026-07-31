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
    # 🎓 Database 101 — Introduction to SQL with DuckDB
    ---

    **Course:** OMIS 105 — Database Management
    **Environment:** DuckDB (in-memory, no server setup required)
    **Original MySQL concepts adapted for DuckDB**

    ---

    ### Topics Covered

    | # | Topic | Cells |
    |---|-------|-------|
    | 1 | Creating tables & inserting data | 1–3 |
    | 2 | Basic SELECT queries | 4–8 |
    | 3 | Filtering with WHERE, IN | 9–13 |
    | 4 | Sorting & LIMIT | 14–17 |
    | 5 | Aggregate functions (COUNT, AVG, MIN, MAX) | 18–22 |
    | 6 | GROUP BY | 23–26 |
    | 7 | Data modification (INSERT, UPDATE, DELETE) | 27–30 |

    ---

    ### Key Differences: MySQL vs. DuckDB

    | Feature | MySQL | DuckDB |
    |---------|-------|--------|
    | Server | Requires running server | In-memory, no server |
    | Connection | `mysql -u root -p` | `duckdb.connect()` in Python |
    | Database | `CREATE DATABASE; USE db;` | Not needed (in-memory) |
    | Syntax | Standard SQL | Standard SQL (same!) |

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ⚙️ Setup — Environment & Helpers
    ---
    """)
    return


@app.cell
def _():
    # ── Setup: Import libraries and helper functions ──────────────────────────────
    import pandas as pd

    # Import our clean display/plot helpers (keeps this notebook uncluttered)
    from helpers import display_result, plot_bar, plot_hbar, plot_pie, plot_line

    print("Setup complete — using mo.sql() for all queries!")
    return display_result, plot_bar, plot_hbar, plot_pie


@app.cell
def _():
    import duckdb
    con = duckdb.connect(database=":memory:")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📋 Section 1: Creating Tables & Inserting Data (Cells 1–3)

    **Key Concepts from Slides:**
    - `CREATE OR REPLACE TABLE` defines the structure (columns and types)
    - **Constraints:** `PRIMARY KEY` (unique ID), `NOT NULL` (required)
    - **Data Types:** `INT` (numbers), `VARCHAR(n)` (text), `DATE` (dates)
    - `INSERT INTO` adds rows of data

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 1: Create the `students` Table
    **What we're doing:** Define a table with 5 columns — id, name, age, grade, and country.
    Each student has a unique `id` (PRIMARY KEY) and a required `name` (NOT NULL).
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE students (
            id      INT PRIMARY KEY,
            name    VARCHAR(50) NOT NULL,
            age     INT,
            grade   VARCHAR(5),
            country VARCHAR(30)
        )
        """
    )
    print("✅ Table 'students' created successfully!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 2: Insert Sample Data
    **What we're doing:** Insert 10 students into our table using `INSERT INTO ... VALUES`.
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        INSERT INTO students VALUES
            (1,  'Alice',   20, 'A', 'USA'),
            (2,  'Bob',     22, 'B', 'CANADA'),
            (3,  'Charlie', 21, 'A', 'USA'),
            (4,  'Diana',   23, 'C', 'GERMANY'),
            (5,  'Ethan',   20, 'B', 'MEXICO'),
            (6,  'Fiona',   22, 'A', 'USA'),
            (7,  'George',  24, 'B', 'ITALY'),
            (8,  'Hannah',  21, 'C', 'USA'),
            (9,  'Ivan',    23, 'A', 'CANADA'),
            (10, 'Julia',   22, 'B', 'GERMANY')
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 3: Verify Table Structure
    **What we're doing:** Use `DESCRIBE` to inspect the table schema — column names, types, and constraints.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        DESCRIBE students
        """
    )
    display_result(_df, 'Table Schema: students')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🔍 Section 2: Basic SELECT Queries (Cells 4–8)

    **Key Concepts from Slides:**
    - `SELECT *` retrieves all columns
    - `SELECT col1, col2` retrieves specific columns
    - `SELECT DISTINCT` removes duplicate values

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 4: Show All Records
    **What we're doing:** Retrieve every row and every column from the `students` table using `SELECT *`.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   students
        """
    )
    display_result(_df, 'All Students')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 5: Select Specific Columns
    **What we're doing:** Retrieve only `name` and `age` — we don't always need every column.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT name,
               age
        FROM   students
        """
    )
    display_result(_df, 'Student Names and Ages')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 6: Find Distinct Countries
    **What we're doing:** Use `SELECT DISTINCT` to see unique country values (no duplicates).
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT DISTINCT country
        FROM   students
        ORDER BY country
        """
    )
    display_result(_df, 'Distinct Countries')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 7: Count Total Students
    **What we're doing:** Use `COUNT(*)` to count how many rows are in the table.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS total_students
        FROM   students
        """
    )
    display_result(_df, 'Total Number of Students')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 8: Select with Calculated Column
    **What we're doing:** Create a new column on-the-fly — calculate birth year from age.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT name,
               age,
               2026 - age AS birth_year
        FROM   students
        ORDER BY name
        """
    )
    display_result(_df, 'Students with Calculated Birth Year')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🎯 Section 3: Filtering with WHERE (Cells 9–13)

    **Key Concepts from Slides:**
    - `WHERE` filters rows based on conditions
    - Comparison operators: `=`, `>`, `<`, `>=`, `<=`, `!=`
    - `IN (...)` checks membership in a list
    - `AND`, `OR` combine conditions

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 9: Filter by Country
    **What we're doing:** Find all students from the USA using `WHERE country = 'USA'`.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   students
        WHERE  country = 'USA'
        """
    )
    display_result(_df, 'Students from USA')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 10: Filter by Age (Greater Than)
    **What we're doing:** Find students older than 22 using the `>` operator.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   students
        WHERE  age > 22
        """
    )
    display_result(_df, 'Students Older Than 22')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 11: Filter by Grade
    **What we're doing:** Find all students who earned grade 'A'.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   students
        WHERE  grade = 'A'
        """
    )
    display_result(_df, 'Students with Grade A')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 12: Filter Using IN
    **What we're doing:** Find students who are 20 or 21 years old using `IN (20, 21)` — cleaner than `OR`.
    """)
    return


@app.cell
def _(mo, display_result, plot_bar, students):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   students
        WHERE  age IN (20, 21)
        """
    )
    display_result(_df, 'Students Age 20 or 21')
    plot_bar(_df, 'name', 'age', title='Students Aged 20–21', xlabel='Student', ylabel='Age')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 13: Combining Conditions (AND / OR)
    **What we're doing:** Find students from USA who are older than 20 — combining two filters with `AND`.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   students
        WHERE  country = 'USA'
          AND  age > 20
        """
    )
    display_result(_df, 'USA Students Older Than 20')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ↕️ Section 4: Sorting & LIMIT (Cells 14–17)

    **Key Concepts from Slides:**
    - `ORDER BY col ASC` — sort ascending (default)
    - `ORDER BY col DESC` — sort descending
    - `LIMIT n` — return only the first n rows

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 14: Sort by Age (Ascending)
    **What we're doing:** Display students sorted from youngest to oldest.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   students
        ORDER BY age ASC
        """
    )
    display_result(_df, 'Students Sorted by Age (Youngest First)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 15: Sort by Name (Descending)
    **What we're doing:** Display students in reverse alphabetical order by name.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   students
        ORDER BY name DESC
        """
    )
    display_result(_df, 'Students Sorted by Name (Z → A)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 16: Show First 5 Students (LIMIT)
    **What we're doing:** Use `LIMIT 5` to see only the first 5 rows — useful for previewing large tables.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   students
        LIMIT 5
        """
    )
    display_result(_df, 'First 5 Students (LIMIT)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 17: Find the Youngest and Oldest Student
    **What we're doing:** Combine `ORDER BY` with `LIMIT 1` to find extreme values.
    """)
    return


@app.cell
def _(mo, display_result, students):
    df_young = mo.sql(
        f"""
        SELECT *
        FROM   students
        ORDER BY age ASC
        LIMIT 1
        """
    )
    display_result(df_young, "Youngest Student")
    return

@app.cell
def _(mo, display_result, students):
    df_old = mo.sql(
        f"""
        SELECT *
        FROM   students
        ORDER BY age DESC
        LIMIT 1
        """
    )
    display_result(df_old, "Oldest Student")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 Section 5: Aggregate Functions (Cells 18–22)

    **Key Concepts from Slides:**
    - `COUNT(*)` — count rows
    - `AVG(col)` — average value
    - `SUM(col)` — total sum
    - `MIN(col)` — smallest value
    - `MAX(col)` — largest value

    These functions **collapse many rows into one summary value**.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 18: Average Age of All Students
    **What we're doing:** Use `AVG(age)` to compute the mean age across all students.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT ROUND(AVG(age), 2) AS average_age
        FROM   students
        """
    )
    display_result(_df, 'Average Student Age')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 19: MIN and MAX Age
    **What we're doing:** Find the youngest and oldest age in a single query.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT MIN(age) AS youngest_age,
               MAX(age) AS oldest_age,
               MAX(age) - MIN(age) AS age_range
        FROM   students
        """
    )
    display_result(_df, 'Age Range Statistics')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 20: All Aggregates at Once
    **What we're doing:** Combine multiple aggregate functions in one query for a complete summary.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS total_students,
               MIN(age) AS min_age,
               MAX(age) AS max_age,
               ROUND(AVG(age), 2) AS avg_age,
               SUM(age) AS sum_of_ages
        FROM   students
        """
    )
    display_result(_df, 'Complete Age Statistics')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 21: Count Students per Grade
    **What we're doing:** Use `COUNT(*)` with `GROUP BY grade` to see how many students earned each grade.
    """)
    return


@app.cell
def _(mo, display_result, plot_bar, students):
    _df = mo.sql(
        f"""
        SELECT   grade,
                 COUNT(*) AS student_count
        FROM     students
        GROUP BY grade
        ORDER BY grade
        """
    )
    display_result(_df, 'Students per Grade')
    plot_bar(_df, 'grade', 'student_count', title='Number of Students per Grade', xlabel='Grade', ylabel='Count')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 22: Count Students per Country
    **What we're doing:** Use `GROUP BY country` to see the distribution of students across countries.
    """)
    return


@app.cell
def _(mo, display_result, plot_pie, students):
    _df = mo.sql(
        f"""
        SELECT   country,
                 COUNT(*) AS student_count
        FROM     students
        GROUP BY country
        ORDER BY student_count DESC
        """
    )
    display_result(_df, 'Students per Country')
    plot_pie(_df, 'country', 'student_count', title='Student Distribution by Country')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📈 Section 6: GROUP BY — Grouping & Summarizing (Cells 23–26)

    **Key Concepts from Slides:**
    - `GROUP BY` splits data into groups, then applies aggregate functions to each group
    - Every non-aggregated column in `SELECT` must appear in `GROUP BY`
    - Often combined with `COUNT`, `AVG`, `SUM`, etc.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 23: Average Age per Country
    **What we're doing:** Group students by country and calculate each country's average age.
    """)
    return


@app.cell
def _(mo, display_result, plot_bar, students):
    _df = mo.sql(
        f"""
        SELECT   country,
                 COUNT(*)           AS num_students,
                 ROUND(AVG(age), 1) AS avg_age
        FROM     students
        GROUP BY country
        ORDER BY avg_age DESC
        """
    )
    display_result(_df, 'Average Age by Country')
    plot_bar(_df, 'country', 'avg_age', title='Average Student Age by Country', xlabel='Country', ylabel='Average Age')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 24: Grade Distribution per Country
    **What we're doing:** Cross-tabulate countries and grades — how many A's, B's, C's per country?
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT   country,
                 grade,
                 COUNT(*) AS student_count
        FROM     students
        GROUP BY country, grade
        ORDER BY country, grade
        """
    )
    display_result(_df, 'Grade Distribution by Country')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 25: Countries with More Than 1 Student
    **What we're doing:** Use `HAVING` to filter *groups* (not rows) — only show countries with 2+ students.
    """)
    return


@app.cell
def _(mo, display_result, plot_hbar, students):
    _df = mo.sql(
        f"""
        SELECT   country,
                 COUNT(*) AS student_count
        FROM     students
        GROUP BY country
        HAVING   COUNT(*) > 1
        ORDER BY student_count DESC
        """
    )
    display_result(_df, 'Countries with More Than 1 Student (HAVING)')
    plot_hbar(_df, 'country', 'student_count', title='Countries with Multiple Students', xlabel='Student Count', ylabel='Country')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 26: Age Statistics per Grade
    **What we're doing:** For each grade, compute min, max, and average age — combining `GROUP BY` with multiple aggregates.
    """)
    return


@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT   grade,
                 COUNT(*)           AS num_students,
                 MIN(age)           AS youngest,
                 MAX(age)           AS oldest,
                 ROUND(AVG(age), 1) AS avg_age
        FROM     students
        GROUP BY grade
        ORDER BY grade
        """
    )
    display_result(_df, 'Age Statistics per Grade')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ✏️ Section 7: Data Modification — INSERT, UPDATE, DELETE (Cells 27–30)

    **Key Concepts from Slides:**
    - `INSERT INTO` adds new rows
    - `UPDATE ... SET ... WHERE` modifies existing rows
    - `DELETE FROM ... WHERE` removes rows
    - ⚠️ Always use `WHERE` with UPDATE and DELETE — without it, ALL rows are affected!

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 27: INSERT — Add a New Student
    **What we're doing:** Add student Kate (id=11) to the table.
    """)
    return


@app.cell
def _(mo, students):
    _df = mo.sql(
        f"""
        INSERT INTO students
        VALUES (11, 'Kate', 21, 'B', 'USA')
        """
    )
    return

@app.cell
def _(mo, display_result, students):
    _df = mo.sql(
        f"""
        SELECT * FROM students WHERE id = 11
        """
    )
    display_result(_df, 'Newly Inserted Student')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 28: UPDATE — Change Bob's Grade to A
    **What we're doing:** Modify an existing record — change Bob's grade from 'B' to 'A'.
    """)
    return


@app.cell
def _(mo, display_result, students):
    # Show Bob's record BEFORE update
    _df = mo.sql(
        f"""
        SELECT * FROM students WHERE name = 'Bob'
        """
    )
    display_result(_df, 'BEFORE Update')
    return

@app.cell
def _(mo, students):
    # Perform the UPDATE
    _df = mo.sql(
        f"""
        UPDATE students
        SET    grade = 'A'
        WHERE  name = 'Bob'
        """
    )
    return

@app.cell
def _(mo, display_result, students):
    # Show Bob's record AFTER update
    _df = mo.sql(
        f"""
        SELECT * FROM students WHERE name = 'Bob'
        """
    )
    display_result(_df, 'AFTER Update (grade changed to A)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 29: DELETE — Remove Student with id=10
    **What we're doing:** Delete Julia (id=10) from the table. Always verify with `WHERE`!
    """)
    return


@app.cell
def _(mo, display_result, students):
    # Show who we're about to delete
    _df = mo.sql(
        f"""
        SELECT * FROM students WHERE id = 10
        """
    )
    display_result(_df, 'Record to be DELETED')
    return

@app.cell
def _(mo, students):
    # Perform the DELETE
    _df = mo.sql(
        f"""
        DELETE FROM students
        WHERE  id = 10
        """
    )
    return

@app.cell
def _(mo, display_result, students):
    # Verify deletion
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS students_remaining
        FROM   students
        """
    )
    display_result(_df, 'Students Remaining After DELETE')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 30: Verify Final State of Table
    **What we're doing:** Show the complete table after all modifications (INSERT, UPDATE, DELETE).
    """)
    return


@app.cell
def _(mo, display_result, plot_bar, students):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   students
        ORDER BY id
        """
    )
    display_result(_df, 'Final State of Students Table (after modifications)')
    plot_bar(_df, 'name', 'age', title='All Students — Final Dataset', xlabel='Student', ylabel='Age', rotate_x=30)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🎓 Summary — SQL Commands Learned

    | Command | Purpose | Example |
    |---------|---------|---------|
    | `CREATE OR REPLACE TABLE` | Define table structure | `CREATE OR REPLACE TABLE students (id INT PRIMARY KEY, ...)` |
    | `INSERT INTO` | Add new rows | `INSERT INTO students VALUES (1, 'Alice', ...)` |
    | `SELECT` | Retrieve data | `SELECT * FROM students` |
    | `SELECT DISTINCT` | Unique values only | `SELECT DISTINCT country FROM students` |
    | `WHERE` | Filter rows | `WHERE age > 20` |
    | `IN` | Match a list | `WHERE age IN (20, 21)` |
    | `ORDER BY` | Sort results | `ORDER BY age DESC` |
    | `LIMIT` | Restrict row count | `LIMIT 5` |
    | `COUNT, AVG, MIN, MAX` | Aggregate functions | `SELECT AVG(age) FROM students` |
    | `GROUP BY` | Group + aggregate | `GROUP BY country` |
    | `HAVING` | Filter groups | `HAVING COUNT(*) > 1` |
    | `UPDATE` | Modify existing rows | `UPDATE students SET grade='A' WHERE ...` |
    | `DELETE` | Remove rows | `DELETE FROM students WHERE id=10` |

    ---

    ### ✅ What's Next?

    In the **next notebook**, we'll cover:
    - **JOINs** (INNER, LEFT, RIGHT) — combining multiple tables
    - **Subqueries** with `WITH` (CTEs)
    - **Window / Ranking functions** (RANK, ROW_NUMBER, NTILE)

    ---
    *Notebook by Professor M. Parsian — Santa Clara University*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    *Great work! You've completed the notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
