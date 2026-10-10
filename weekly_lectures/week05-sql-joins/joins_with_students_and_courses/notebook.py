import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from plot_helpers import (
        plot_bar,
        plot_grades,
        plot_hbar,
        plot_line,
        plot_stacked_bar,
    )

    return plot_bar, plot_grades, plot_hbar, plot_line, plot_stacked_bar


@app.cell
def _(mo):
    import duckdb

    # Open the database built by ./create_duckdb_database.sh.
    # read_only=True: queries can read the tables, but nothing in
    # this notebook can change them.
    db_path = mo.notebook_dir() / "students_courses_grades.duckdb"
    if not db_path.exists():
        raise FileNotFoundError(
            f"{db_path} not found. Build it first:  ./create_duckdb_database.sh"
        )
    con = duckdb.connect(database=str(db_path), read_only=True)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Students / Courses / Grades: Learning SQL Joins

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### About This Database

    A small university keeps 3 tables to track student grades:

    | Table | Rows | Columns | Links to |
    |-------|-----:|---------|----------|
    | `students` | 500   | student_id, first_name, last_name, major, gender, country | — |
    | `courses`  | 50    | course_id, course_name, course_level, num_of_credits | — |
    | `grades`   | 8,000 | grade_id, student_id, course_id, year, grade | `grades.student_id` → `students.student_id`, `grades.course_id` → `courses.course_id` |

    `grades` sits **in the middle**. Each row says: *this student*
    took *this course* in *this year* and earned *this grade*.
    One student takes many courses. One course has many students.

    ```
    students ──< grades >── courses
    ```

    On purpose, the data has gaps, the way real data usually does:

    - **5 students have never taken a course** (no rows in `grades`).
    - **3 courses have never been taken:** ENGR204, MATH204, FIN204.

    These gaps are why `INNER JOIN`, `LEFT JOIN`, and `RIGHT JOIN`
    give *different* answers here. **Watch the row counts.**

    ### The Plan

    | Part | Queries | Focus |
    |------|---------|-------|
    | 1. Meet the data | V1–V3 | Look at each table |
    | 2. Aggregation | A1–A3 | COUNT, COUNT(DISTINCT), GROUP BY |
    | 3. INNER JOIN `A ⋈ B` | J1–J4 | Only rows that match on both sides |
    | 4. LEFT JOIN `A ⟕ B` | J5–J7 | Keep every row from the left table |
    | 5. RIGHT JOIN `A ⟖ B` | J8–J10 | Keep every row from the right table |

    Six queries are followed by a chart. The plotting code lives in
    `plot_helpers.py`, so you can focus on the SQL.

    ### Read-Only

    The notebook opens `students_courses_grades.duckdb` in
    **read-only** mode. You can run any `SELECT` you like. You cannot
    break the data by accident. If the file is missing, build it first
    with `./create_duckdb_database.sh`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Setup — Confirm the Database Opened

    You should see 500 students, 50 courses, and 8,000 grades.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT 'students' AS table_name, COUNT(*) AS row_count FROM students
        UNION ALL SELECT 'courses', COUNT(*) FROM courses
        UNION ALL SELECT 'grades',  COUNT(*) FROM grades
        ORDER BY table_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Proof that it is read-only

    This cell tries to add a new course. DuckDB refuses, because the
    connection is read-only.
    """)
    return


@app.cell
def _(con, mo):
    try:
        con.execute("INSERT INTO courses VALUES ('TEST999', 'Test', 'graduate', 1)")
        read_only_result = mo.md("The INSERT worked — the database is **not** read-only.")
    except Exception as err:
        read_only_result = mo.md(f"**Refused, as expected:** `{err}`")
    read_only_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 1 — Meet the Data

    Before you join tables, look at each one by itself. Know what a
    row means, and know the key that links it to the other tables.

    ## V1 — The `students` table

    One row per student. `student_id` is the **primary key**: no two
    students share it. `major`, `gender`, and `country` are `ENUM`
    columns — they only accept values from a fixed list.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM students
        ORDER BY student_id
        LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## V2 — The `courses` table

    One row per course. `course_id` is text, like `'CSCI103'`. The
    letters name the department, and the number gives the level:
    `1xx` courses are undergraduate, `2xx` courses are graduate.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM courses
        ORDER BY course_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## V3 — The `grades` table

    One row per student per course. `student_id` and `course_id` are
    **foreign keys**: each value must exist in `students` or
    `courses`. By themselves, these rows are hard to read — there are
    no names. Joins will fix that.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM grades
        ORDER BY grade_id
        LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 2 — Aggregation

    Aggregate functions turn many rows into one number. `GROUP BY`
    gives you one number **per group**.

    ## A1 — Students per country

    Most students come from the USA, India, and China.
    """)
    return


@app.cell
def _(con, mo):
    df_countries = mo.sql(
        f"""
        SELECT country,
               COUNT(*) AS num_students
        FROM students
        GROUP BY country
        ORDER BY num_students DESC;
        """,
        engine=con
    )
    return (df_countries,)


@app.cell
def _(df_countries, plot_hbar):
    plot_hbar(df_countries, labels="country", values="num_students",
              title="Students per country", xlabel="number of students")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A2 — How many of each letter grade?

    `grade` is an `ENUM` with the order `'A', 'B', 'C', 'D', 'F'`, so
    `ORDER BY grade` sorts from best to worst — not alphabetically.
    """)
    return


@app.cell
def _(con, mo):
    df_grade_counts = mo.sql(
        f"""
        SELECT grade,
               COUNT(*) AS num_grades
        FROM grades
        GROUP BY grade
        ORDER BY grade;
        """,
        engine=con
    )
    return (df_grade_counts,)


@app.cell
def _(df_grade_counts, plot_grades):
    plot_grades(df_grade_counts, grades="grade", counts="num_grades",
                title="Letter grades, all years")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A3 — Activity per year

    `COUNT(*)` counts rows. `COUNT(DISTINCT column)` counts
    **different values**. One student has many grades in a year, so
    the number of students is much smaller than the number of grades.
    """)
    return


@app.cell
def _(con, mo):
    df_years = mo.sql(
        f"""
        SELECT year,
               COUNT(*)                   AS num_grades,
               COUNT(DISTINCT student_id) AS num_students,
               COUNT(DISTINCT course_id)  AS num_courses
        FROM grades
        GROUP BY year
        ORDER BY year;
        """,
        engine=con
    )
    return (df_years,)


@app.cell
def _(df_years, plot_line):
    plot_line(df_years, x="year", y="num_grades",
              title="Grades recorded per year", ylabel="number of grades")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 3 — INNER JOIN `A ⋈ B`

    An `INNER JOIN` keeps a row **only when it matches on both
    sides**. A student with no grades disappears. A course nobody took
    disappears.

    ```sql
    FROM grades g
    INNER JOIN students s ON g.student_id = s.student_id
    ```

    `g` and `s` are **aliases** — short names for the tables. The `ON`
    clause says which columns must be equal.

    ## J1 — Every grade with the student's name

    `grades ⋈ students`: 8,000 rows — every grade has a valid student,
    because the foreign key guarantees it. We show the first 10.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT g.grade_id,
               s.first_name,
               s.last_name,
               g.course_id,
               g.year,
               g.grade
        FROM grades g
        INNER JOIN students s ON g.student_id = s.student_id
        ORDER BY g.grade_id
        LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J2 — The 10 most popular courses

    `grades ⋈ courses`, then `GROUP BY`. The join brings in the course
    name, so the result is easy to read.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT c.course_id,
               c.course_name,
               c.course_level,
               COUNT(*) AS num_students
        FROM grades g
        INNER JOIN courses c ON g.course_id = c.course_id
        GROUP BY c.course_id, c.course_name, c.course_level
        ORDER BY num_students DESC, c.course_id
        LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J3 — Three tables: one student's transcript

    `students ⋈ grades ⋈ courses`. Chain two joins: first match the
    student to their grades, then match each grade to its course.
    Here is the transcript for student 1.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT s.first_name,
               s.last_name,
               g.year,
               c.course_id,
               c.course_name,
               c.num_of_credits,
               g.grade
        FROM students s
        INNER JOIN grades  g ON s.student_id = g.student_id
        INNER JOIN courses c ON g.course_id  = c.course_id
        WHERE s.student_id = 1
        ORDER BY g.year, c.course_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J4 — Average GPA by department

    A `CASE` expression turns each letter grade into grade points
    (A = 4, B = 3, C = 2, D = 1, F = 0). Then `AVG` gives the GPA.

    The department is the letters at the front of `course_id`.
    `rtrim(c.course_id, '0123456789')` removes the digits at the end:
    `'MATH105'` becomes `'MATH'`.

    Which department gives the hardest grades?
    """)
    return


@app.cell
def _(con, mo):
    df_dept_gpa = mo.sql(
        f"""
        SELECT rtrim(c.course_id, '0123456789') AS department,
               COUNT(*) AS num_grades,
               ROUND(AVG(CASE g.grade
                            WHEN 'A' THEN 4
                            WHEN 'B' THEN 3
                            WHEN 'C' THEN 2
                            WHEN 'D' THEN 1
                            WHEN 'F' THEN 0
                         END), 2) AS avg_gpa
        FROM grades g
        INNER JOIN courses c ON g.course_id = c.course_id
        GROUP BY department
        ORDER BY avg_gpa DESC;
        """,
        engine=con
    )
    return (df_dept_gpa,)


@app.cell
def _(df_dept_gpa, plot_hbar):
    plot_hbar(df_dept_gpa, labels="department", values="avg_gpa",
              title="Average GPA by department (4.0 scale)",
              xlabel="average GPA", decimals=2, xmax=4.0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 4 — LEFT JOIN `A ⟕ B`

    A `LEFT JOIN` keeps **every row from the left table** (the one
    after `FROM`). When a row has no match on the right, the right
    side's columns are filled with `NULL`.

    ## J5 — Courses taken per student, fewest first

    `students ⟕ grades`. The 5 students with no grades are kept, with
    a count of 0.

    Note: `COUNT(g.grade_id)` counts only non-NULL values, so it gives
    0 for those students. `COUNT(*)` would count the NULL-filled row
    and give a wrong 1.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT s.student_id,
               s.first_name,
               s.last_name,
               s.major,
               COUNT(g.grade_id) AS courses_taken
        FROM students s
        LEFT JOIN grades g ON s.student_id = g.student_id
        GROUP BY s.student_id, s.first_name, s.last_name, s.major
        ORDER BY courses_taken, s.student_id
        LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J6 — Students who have never taken a course

    This is the **anti-join** pattern: `LEFT JOIN`, then keep only
    the rows where the right side is `NULL`. It answers the question
    "what is in A but **not** in B?"
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT s.student_id,
               s.first_name,
               s.last_name,
               s.major,
               s.country
        FROM students s
        LEFT JOIN grades g ON s.student_id = g.student_id
        WHERE g.grade_id IS NULL
        ORDER BY s.student_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J7 — Enrollment in every graduate course

    `courses ⟕ grades`, for the 20 graduate courses. The 3 courses
    nobody took stay in the result with 0 students. In the chart they
    are dashed **"none"** bars.

    The `WHERE` filter is on the **left** table (`c.course_level`), so
    it does not remove the unmatched rows.
    """)
    return


@app.cell
def _(con, mo):
    df_grad_enroll = mo.sql(
        f"""
        SELECT c.course_id,
               c.course_name,
               COUNT(g.grade_id) AS num_students
        FROM courses c
        LEFT JOIN grades g ON c.course_id = g.course_id
        WHERE c.course_level = 'graduate'
        GROUP BY c.course_id, c.course_name
        ORDER BY c.course_id;
        """,
        engine=con
    )
    return (df_grad_enroll,)


@app.cell
def _(df_grad_enroll, plot_bar):
    plot_bar(df_grad_enroll, labels="course_id", values="num_students",
             title="Students per graduate course (LEFT JOIN keeps all 20)",
             ylabel="number of students")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 5 — RIGHT JOIN `A ⟖ B`

    A `RIGHT JOIN` keeps **every row from the right table** (the one
    after `RIGHT JOIN`). It is the mirror of `LEFT JOIN`:

    ```
    A LEFT JOIN B   gives the same rows as   B RIGHT JOIN A
    ```

    ## J8 — Courses that no student has taken

    `grades ⟖ courses`, then keep the rows where the `grades` side is
    `NULL`. Same anti-join as J6, written from the other direction.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT c.course_id,
               c.course_name,
               c.course_level,
               c.num_of_credits
        FROM grades g
        RIGHT JOIN courses c ON g.course_id = c.course_id
        WHERE g.grade_id IS NULL
        ORDER BY c.course_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J9 — Courses offered vs. courses taken, per department

    `grades ⟖ courses` keeps all 50 courses.

    - `COUNT(DISTINCT c.course_id)` counts every course offered.
    - `COUNT(DISTINCT g.course_id)` skips the NULLs, so it counts
      only courses that someone took.

    The difference is the number of courses nobody took.
    """)
    return


@app.cell
def _(con, mo):
    df_dept_courses = mo.sql(
        f"""
        SELECT rtrim(c.course_id, '0123456789') AS department,
               COUNT(DISTINCT c.course_id) AS offered,
               COUNT(DISTINCT g.course_id) AS taken,
               COUNT(DISTINCT c.course_id)
                 - COUNT(DISTINCT g.course_id) AS never_taken
        FROM grades g
        RIGHT JOIN courses c ON g.course_id = c.course_id
        GROUP BY department
        ORDER BY department;
        """,
        engine=con
    )
    return (df_dept_courses,)


@app.cell
def _(df_dept_courses, plot_stacked_bar):
    plot_stacked_bar(df_dept_courses, labels="department",
                     parts=["taken", "never_taken"],
                     part_names=["taken by at least 1 student", "never taken"],
                     title="Courses offered per department",
                     ylabel="number of courses")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J10 — The hardest courses (and the empty ones)

    `grades ⟖ courses`, one row per course, sorted by GPA from low to
    high. `NULLS FIRST` puts the 3 courses with no grades at the top.

    **Watch out:** the `CASE` has no `ELSE`. For a course nobody took,
    `g.grade` is `NULL`, so `CASE` returns `NULL` and `AVG` returns
    `NULL` — "no data". If we wrote `ELSE 0`, those courses would get
    a fake GPA of 0.00 and look like the hardest courses of all.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT c.course_id,
               c.course_name,
               COUNT(g.grade_id) AS num_students,
               ROUND(AVG(CASE g.grade
                            WHEN 'A' THEN 4
                            WHEN 'B' THEN 3
                            WHEN 'C' THEN 2
                            WHEN 'D' THEN 1
                            WHEN 'F' THEN 0
                         END), 2) AS avg_gpa
        FROM grades g
        RIGHT JOIN courses c ON g.course_id = c.course_id
        GROUP BY c.course_id, c.course_name
        ORDER BY avg_gpa NULLS FIRST, c.course_id
        LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Summary — Row Counts by Join Type

    The same two tables, joined three ways. The extra rows in each
    outer join are exactly the gaps: 5 students with no grades, and
    3 courses nobody took.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT 'students INNER JOIN grades' AS join_query,
               COUNT(*) AS num_rows
        FROM students s INNER JOIN grades g ON s.student_id = g.student_id
        UNION ALL
        SELECT 'students LEFT JOIN grades', COUNT(*)
        FROM students s LEFT JOIN grades g ON s.student_id = g.student_id
        UNION ALL
        SELECT 'grades RIGHT JOIN students', COUNT(*)
        FROM grades g RIGHT JOIN students s ON g.student_id = s.student_id
        UNION ALL
        SELECT 'courses INNER JOIN grades', COUNT(*)
        FROM courses c INNER JOIN grades g ON c.course_id = g.course_id
        UNION ALL
        SELECT 'courses LEFT JOIN grades', COUNT(*)
        FROM courses c LEFT JOIN grades g ON c.course_id = g.course_id
        UNION ALL
        SELECT 'grades RIGHT JOIN courses', COUNT(*)
        FROM grades g RIGHT JOIN courses c ON g.course_id = c.course_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Cheat Sheet

    | You want… | Write |
    |-----------|-------|
    | only rows that match on both sides | `A INNER JOIN B ON …` |
    | every row of A, matched or not | `A LEFT JOIN B ON …` |
    | every row of B, matched or not | `A RIGHT JOIN B ON …` (= `B LEFT JOIN A`) |
    | rows of A with **no** match in B | `A LEFT JOIN B ON … WHERE B.key IS NULL` |
    | count matches, 0 when none | `COUNT(B.key)`, not `COUNT(*)` |

    ### Try It Yourself

    1. List every student from `'CANADA'` with the number of courses
       they took. (INNER or LEFT?)
    2. Find the average GPA per **country**. Which country is highest?
    3. For each course, count how many students earned an `'F'`.
       Make sure courses with no F still appear with 0.
       (Hint: put the `'F'` test in the `ON` clause, not in `WHERE`.)
    4. Rewrite J6 as a `RIGHT JOIN`. Check that you still get 5 rows.
    5. Which students took at least one graduate course in 2025?
       Show each student only once.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
