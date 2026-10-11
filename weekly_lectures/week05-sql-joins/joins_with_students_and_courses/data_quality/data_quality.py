import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    import duckdb

    # Open the database built by ./create_messy_database.sh, read-only.
    db_path = mo.notebook_dir() / "students_courses_grades_messy.duckdb"
    if not db_path.exists():
        raise FileNotFoundError(
            f"{db_path} not found. Build it first:  ./create_messy_database.sh"
        )
    con = duckdb.connect(database=str(db_path), read_only=True)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    def check(df, rows, columns):
        """Compare a result with the expected row count and column names."""
        got_cols = [c.lower() for c in df.columns]
        if got_cols == ["todo"]:
            return mo.callout(mo.md("Not answered yet."), kind="neutral")
        problems = []
        if len(df) != rows:
            problems.append(f"expected **{rows}** rows, got **{len(df)}**")
        if got_cols != [c.lower() for c in columns]:
            problems.append(
                f"expected columns `{', '.join(columns)}`, "
                f"got `{', '.join(df.columns)}`"
            )
        if problems:
            return mo.callout(mo.md("Not yet: " + "; ".join(problems) + "."),
                              kind="warn")
        return mo.callout(
            mo.md(f"Row count and columns match ({rows} rows). "
                  "Now check the values make sense."),
            kind="success")

    return (check,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Data-Quality Round

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Database:** `students_courses_grades_messy.duckdb` (read-only)

    ---

    ### The situation

    The university is moving to a new system. The old system exported
    its data into three **raw** tables. The dean wants a report next
    week. Your manager says:

    > *"Before we build any report, check the data. Find every problem,
    > and tell me how many rows each one affects."*

    This is a real, everyday job for data analysts and data
    engineers. Bad data in means wrong numbers out.

    ### The raw tables

    ```
    raw_students (student_id, first_name, last_name, major, gender, country)
    raw_courses  (course_id, course_name, course_level, num_of_credits)
    raw_grades   (grade_id, student_id, course_id, year, grade)
    ```

    The old system had **no rules**: no `PRIMARY KEY`, no
    `FOREIGN KEY`, no `NOT NULL`, and every text column accepts any
    text. So anything could get in.

    ### What the data *should* look like

    | Column | Valid values |
    |--------|--------------|
    | `student_id`, `grade_id` | unique — one row each |
    | `first_name`, `last_name` | not missing, not empty |
    | `country` | `'USA'`, `'CANADA'`, `'CHINA'`, `'INDIA'`, `'GERMANY'`, `'MEXICO'`, `'ITALY'` |
    | `gender` | `'MALE'`, `'FEMALE'`, `'NA'` |
    | `major` | `'BUSINESS'`, `'ENGINEERING'`, `'MATH'`, `'COMPUTER-SCIENCE'`, `'FINANCE'` |
    | `course_level` | `'undergraduate'`, `'graduate'` |
    | `num_of_credits` | more than 0 |
    | `year` | 2021 to 2025 |
    | `grade` | `'A'`, `'B'`, `'C'`, `'D'`, `'F'` — not missing |
    | `raw_grades.student_id` | must exist in `raw_students` |
    | `raw_grades.course_id` | must exist in `raw_courses` |
    | a student + a course | at most one grade |

    ### How to work

    Each task asks for one check. Write a query that returns **the
    bad rows** (or a summary, when the task says so). The box under
    each task checks your row count and column names. Replace the
    `SELECT 'not answered yet' AS todo;` line with your query.

    **Watch out for `NULL`.** A test like `grade NOT IN (...)` is
    *not true* for a `NULL` grade, so `NULL` rows quietly slip
    through. Several tasks are built around this.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ### Why this matters: the dean's report, run on raw data

    Here is "students per country", written the normal way. Look at
    the country names and the number of rows. Would you send this to
    the dean?
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT country,
               COUNT(*) AS num_students
        FROM raw_students
        GROUP BY country
        ORDER BY num_students DESC, country;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part A — Profile the Data

    ## DQ1 — Rows vs. unique ids

    > *"For each raw table, how many rows does it have, and how many
    > **different** ids? (`student_id`, `course_id`, `grade_id`.)"*

    If the two numbers differ, some id appears more than once.

    **Columns:** `table_name`, `num_rows`, `num_distinct_ids`
    """)
    return


@app.cell
def _(con, mo):
    dq1 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq1,)


@app.cell(hide_code=True)
def _(check, dq1):
    check(dq1, rows=3, columns=["table_name", "num_rows", "num_distinct_ids"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part B — Students

    ## DQ2 — Duplicate student ids

    > *"Which `student_id` values appear more than once, and how many
    > times?"*

    **Columns:** `student_id`, `num_rows`
    """)
    return


@app.cell
def _(con, mo):
    dq2 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq2,)


@app.cell(hide_code=True)
def _(check, dq2):
    check(dq2, rows=4, columns=["student_id", "num_rows"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ3 — Exact copies

    > *"Some duplicates are the same row loaded twice. Others are two
    > **different** versions of a student. Which duplicated students
    > are exact copies?"*

    *Hint:* group by **every** column.

    **Columns:** `student_id`, `num_copies`

    When you are done, compare with DQ2: which student is a duplicate
    but **not** an exact copy? What is different about its two rows?
    """)
    return


@app.cell
def _(con, mo):
    dq3 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq3,)


@app.cell(hide_code=True)
def _(check, dq3):
    check(dq3, rows=3, columns=["student_id", "num_copies"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ4 — Country spellings

    > *"Show every `country` value that is not one of the 7 official
    > values, with how many rows use it."*

    *Hint:* some bad values contain spaces you cannot see. Show the
    value inside brackets so the spaces become visible:
    `'[' || country || ']' AS country`.

    **Columns:** `country`, `num_rows`
    """)
    return


@app.cell
def _(con, mo):
    dq4 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq4,)


@app.cell(hide_code=True)
def _(check, dq4):
    check(dq4, rows=6, columns=["country", "num_rows"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ5 — Fix the dean's report

    > *"Now redo 'students per country' correctly: clean up the
    > country names, and count each student only once. Biggest
    > country first."*

    *Hints:* `trim()` removes spaces at both ends. `upper()` makes
    text uppercase. A `CASE` can map `'UNITED STATES'` and
    `'U.S.A.'` to `'USA'`. To check your numbers: the clean database
    has **174** students from the USA and **110** from China.

    **Columns:** `country`, `num_students`
    """)
    return


@app.cell
def _(con, mo):
    dq5 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq5,)


@app.cell(hide_code=True)
def _(check, dq5):
    check(dq5, rows=7, columns=["country", "num_students"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ6 — Missing names

    > *"Which students are missing a first name or a last name?"*

    Think about what "missing" can look like in a text column.

    **Columns:** `student_id`, `first_name`, `last_name`
    """)
    return


@app.cell
def _(con, mo):
    dq6 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq6,)


@app.cell(hide_code=True)
def _(check, dq6):
    check(dq6, rows=3, columns=["student_id", "first_name", "last_name"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ7 — Invalid gender codes

    > *"Which students have a `gender` that is not `'MALE'`,
    > `'FEMALE'`, or `'NA'`?"*

    **Columns:** `student_id`, `gender`
    """)
    return


@app.cell
def _(con, mo):
    dq7 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq7,)


@app.cell(hide_code=True)
def _(check, dq7):
    check(dq7, rows=4, columns=["student_id", "gender"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part C — Courses

    ## DQ8 — Invalid courses

    > *"Which courses have an invalid `course_level`, or a number of
    > credits that is not more than 0?"*

    **Columns:** `course_id`, `course_level`, `num_of_credits`
    """)
    return


@app.cell
def _(con, mo):
    dq8 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq8,)


@app.cell(hide_code=True)
def _(check, dq8):
    check(dq8, rows=3, columns=["course_id", "course_level", "num_of_credits"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part D — Grades

    ## DQ9 — Grades for unknown students

    > *"Which grades belong to a `student_id` that is not in
    > `raw_students`?"*

    *Hint:* you already know this pattern from the joins notebook.

    **Columns:** `grade_id`, `student_id`, `course_id`
    """)
    return


@app.cell
def _(con, mo):
    dq9 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq9,)


@app.cell(hide_code=True)
def _(check, dq9):
    check(dq9, rows=4, columns=["grade_id", "student_id", "course_id"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ10 — Grades for unknown courses

    > *"Which grades belong to a `course_id` that is not in
    > `raw_courses`?"*

    When you are done, look closely at the `course_id` values you
    found. Are they all really unknown courses?

    **Columns:** `grade_id`, `student_id`, `course_id`
    """)
    return


@app.cell
def _(con, mo):
    dq10 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq10,)


@app.cell(hide_code=True)
def _(check, dq10):
    check(dq10, rows=5, columns=["grade_id", "student_id", "course_id"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ11 — Impossible years

    > *"Which grades have a `year` outside 2021–2025?"*

    **Columns:** `grade_id`, `student_id`, `year`
    """)
    return


@app.cell
def _(con, mo):
    dq11 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq11,)


@app.cell(hide_code=True)
def _(check, dq11):
    check(dq11, rows=4, columns=["grade_id", "student_id", "year"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ12 — Invalid or missing grades

    > *"Which rows have a `grade` that is not `'A'`–`'F'`, or no grade
    > at all?"*

    Read the `NULL` warning at the top again before you start.

    **Columns:** `grade_id`, `grade`
    """)
    return


@app.cell
def _(con, mo):
    dq12 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq12,)


@app.cell(hide_code=True)
def _(check, dq12):
    check(dq12, rows=7, columns=["grade_id", "grade"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ13 — The same course, loaded twice

    > *"Which student + course pairs have more than one grade row?"*

    **Columns:** `student_id`, `course_id`, `num_rows`
    """)
    return


@app.cell
def _(con, mo):
    dq13 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq13,)


@app.cell(hide_code=True)
def _(check, dq13):
    check(dq13, rows=5, columns=["student_id", "course_id", "num_rows"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ14 — Reused grade ids

    > *"Which `grade_id` values appear more than once?"*

    You may have seen a hint of this in DQ1.

    **Columns:** `grade_id`, `num_rows`
    """)
    return


@app.cell
def _(con, mo):
    dq14 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (dq14,)


@app.cell(hide_code=True)
def _(check, dq14):
    check(dq14, rows=2, columns=["grade_id", "num_rows"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ### When you are done

    1. Write a short note to your manager: one line per problem, with
       the number of rows it affects.
    2. Open `../db_schema.sql` (in the parent folder). For each problem, ask: **would the clean
       database's rules (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`,
       `ENUM`) have stopped it?** Some would not.
    3. Then open `data_quality_answers.py` and compare.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
