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

    # Open the database built by ./create_duckdb_database.sh, read-only.
    db_path = mo.notebook_dir() / "students_courses_grades.duckdb"
    if not db_path.exists():
        raise FileNotFoundError(
            f"{db_path} not found. Build it first:  ./create_duckdb_database.sh"
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
    # OMIS 105 — SQL Interview Practice

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Database:** `students_courses_grades.duckdb` (read-only)

    ---

    Data analyst interviews almost always include a live SQL test.
    The questions look like the ones below: a manager asks a business
    question in plain English, and you write the query.

    ### How to practice

    1. **Set a timer for 60 minutes.** That is about 5 minutes per
       question. Real interviews are timed.
    2. **Say your plan out loud** before you type: "I need students
       and grades, so I join on `student_id`, then group by…"
       Interviewers grade your thinking, not only your answer.
    3. **Check the row count.** Under each question, a box tells you
       whether your row count and column names are right. Green
       means the *shape* is right — still look at the values.
    4. **If a question is unclear, ask.** In this notebook, write down
       how you decided. Some questions are unclear on purpose.

    ### The tables

    ```
    students (student_id, first_name, last_name, major, gender, country)
    grades   (grade_id, student_id, course_id, year, grade)
    courses  (course_id, course_name, course_level, num_of_credits)
    ```

    - `grades.student_id` → `students.student_id`
    - `grades.course_id` → `courses.course_id`
    - `grade` is `'A'`, `'B'`, `'C'`, `'D'`, or `'F'`. Grade points:
      A = 4, B = 3, C = 2, D = 1, F = 0. An `F` earns no credits.
    - Department = the letters at the front of `course_id`:
      `rtrim(course_id, '0123456789')` turns `'MATH105'` into `'MATH'`.

    ### Rules

    - Use the column names given in each question, in that order
      (use `AS` to rename).
    - When a question asks for a top 10, break ties by `student_id`.
    - Replace the `SELECT 'not answered yet' AS todo;` line with
      your query.

    | Level | Questions | Skills |
    |-------|-----------|--------|
    | Warm-up | Q1–Q4 | `GROUP BY`, `HAVING`, anti-join, join + `LIMIT` |
    | Core | Q5–Q9 | outer joins, conditional counts, 3-table joins |
    | Hard | Q10–Q12 | weighted averages, "zero rows" answers, unclear questions |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Warm-up

    ## Q1 — Students per major

    > *"How many students do we have in each major? Biggest major
    > first."*

    **Columns:** `major`, `num_students`
    """)
    return


@app.cell
def _(con, mo):
    q1 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q1,)


@app.cell(hide_code=True)
def _(check, q1):
    check(q1, rows=5, columns=["major", "num_students"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q2 — Possible duplicate records

    > *"The registrar thinks some students were entered twice. Find
    > every first name + last name pair that belongs to more than one
    > student. Most common pair first."*

    **Columns:** `first_name`, `last_name`, `num_students`
    """)
    return


@app.cell
def _(con, mo):
    q2 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q2,)


@app.cell(hide_code=True)
def _(check, q2):
    check(q2, rows=104, columns=["first_name", "last_name", "num_students"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q3 — Courses nobody has taken

    > *"We want to cancel courses with zero enrollment. Which courses
    > have never had a single student?"*

    **Columns:** `course_id`, `course_name`
    """)
    return


@app.cell
def _(con, mo):
    q3 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q3,)


@app.cell(hide_code=True)
def _(check, q3):
    check(q3, rows=3, columns=["course_id", "course_name"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q4 — The 10 busiest students

    > *"Who are the 10 students who have taken the most courses? Show
    > their names."*

    **Columns:** `student_id`, `first_name`, `last_name`, `courses_taken`
    """)
    return


@app.cell
def _(con, mo):
    q4 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q4,)


@app.cell(hide_code=True)
def _(check, q4):
    check(q4, rows=10,
          columns=["student_id", "first_name", "last_name", "courses_taken"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Core

    ## Q5 — F grades in every course

    > *"For **every** course, how many F grades has it given? Courses
    > with no F grades must still be in the list, with 0. Most F's
    > first."*

    **Columns:** `course_id`, `course_name`, `num_f`
    """)
    return


@app.cell
def _(con, mo):
    q5 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q5,)


@app.cell(hide_code=True)
def _(check, q5):
    check(q5, rows=50, columns=["course_id", "course_name", "num_f"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q6 — Departments with a high fail rate

    > *"Which departments have an F rate above 5%? Show the number of
    > grades, the number of F's, and the F percent rounded to 1
    > decimal. Highest rate first."*

    **Columns:** `department`, `num_grades`, `num_f`, `pct_f`
    """)
    return


@app.cell
def _(con, mo):
    q6 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q6,)


@app.cell(hide_code=True)
def _(check, q6):
    check(q6, rows=2, columns=["department", "num_grades", "num_f", "pct_f"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q7 — One-year students

    > *"Which students took **all** of their courses in a single year?
    > Show which year, and how many courses they took."*

    **Columns:** `student_id`, `first_name`, `last_name`, `year`,
    `courses_taken`
    """)
    return


@app.cell
def _(con, mo):
    q7 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q7,)


@app.cell(hide_code=True)
def _(check, q7):
    check(q7, rows=2, columns=["student_id", "first_name", "last_name",
                               "year", "courses_taken"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q8 — Students with at least one F, by country

    > *"For each country: how many students do we have, how many of
    > them have at least one F, and what percent is that (1 decimal)?
    > Count **all** students, even ones who have not taken a course
    > yet. Biggest country first."*

    **Columns:** `country`, `num_students`, `students_with_f`, `pct_with_f`
    """)
    return


@app.cell
def _(con, mo):
    q8 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q8,)


@app.cell(hide_code=True)
def _(check, q8):
    check(q8, rows=7, columns=["country", "num_students",
                               "students_with_f", "pct_with_f"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q9 — Most credits earned

    > *"Which 10 students have **earned** the most credits? A course
    > earns its `num_of_credits` when the grade is A–D. An F earns
    > nothing."*

    **Columns:** `student_id`, `first_name`, `last_name`, `credits_earned`
    """)
    return


@app.cell
def _(con, mo):
    q9 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q9,)


@app.cell(hide_code=True)
def _(check, q9):
    check(q9, rows=10,
          columns=["student_id", "first_name", "last_name", "credits_earned"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Hard

    ## Q10 — GPA by major, done right

    > *"Show each major's GPA two ways: a simple average of grade
    > points, and a GPA **weighted by credits** (a 5-credit course
    > counts 5 times as much as a 1-credit course). Round both to 3
    > decimals. Sort by the weighted GPA, highest first. Does the
    > ranking change?"*

    **Columns:** `major`, `simple_gpa`, `weighted_gpa`
    """)
    return


@app.cell
def _(con, mo):
    q10 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q10,)


@app.cell(hide_code=True)
def _(check, q10):
    check(q10, rows=5, columns=["major", "simple_gpa", "weighted_gpa"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q11 — Repeated courses

    > *"Find every student who has more than one grade for the
    > **same** course. Show how many times they took it."*

    **Columns:** `student_id`, `course_id`, `times_taken`

    When you have your answer, write one sentence: what does your
    result tell the manager?
    """)
    return


@app.cell
def _(con, mo):
    q11 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q11,)


@app.cell(hide_code=True)
def _(check, q11):
    check(q11, rows=0, columns=["student_id", "course_id", "times_taken"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Q12 — Students who never earned an A

    > *"List the students who never earned an A."*

    **Columns:** `student_id`, `first_name`, `last_name`, `courses_taken`

    This question is short on purpose. Before you write SQL, ask
    yourself: **which students does the manager mean?** Write your
    decision as a `--` comment at the top of your query.
    """)
    return


@app.cell
def _(con, mo):
    q12 = mo.sql(
        f"""
        -- Write your query here
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return (q12,)


@app.cell(hide_code=True)
def _(check, q12):
    check(q12, rows=1,
          columns=["student_id", "first_name", "last_name", "courses_taken"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ### When you are done

    Open `interview_practice_answers.py` and compare. For each
    question, it explains what the interviewer is really checking,
    and it runs the most common wrong answer so you can see how its
    result differs.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
