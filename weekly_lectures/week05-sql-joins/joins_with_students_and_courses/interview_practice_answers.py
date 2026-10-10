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
    mo.md("""
    # OMIS 105 — SQL Interview Practice: Answers

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian

    ---

    Try `interview_practice.py` first, with a timer. Then come here.

    For each question you get:

    - **A solution.** It is not the only correct one. If your query
      gives the same rows, it is right too.
    - **What the interviewer is checking.** Each question tests one
      or two skills on purpose.
    - **A common mistake,** often run as real SQL, so you can see how
      the wrong answer differs. Most wrong answers do not cause an
      error. They just give a different row count.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Warm-up

    ## Q1 — Students per major (5 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT major,
               COUNT(*) AS num_students
        FROM students
        GROUP BY major
        ORDER BY num_students DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:** basic `GROUP BY`, and that
    you sort by the count, not by the major's name. This is a 1-minute
    question. Answer it fast and move on.

    ---
    ## Q2 — Possible duplicate records (104 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT first_name,
               last_name,
               COUNT(*) AS num_students
        FROM students
        GROUP BY first_name, last_name
        HAVING COUNT(*) > 1
        ORDER BY num_students DESC, last_name, first_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:** `HAVING` filters **groups**;
    `WHERE` filters **rows**. You cannot write `WHERE COUNT(*) > 1`.

    **The follow-up question you should raise yourself:** the same
    name does **not** mean the same person. Two students can both be
    named Olivia Jones. To find real duplicates, you would also compare
    `major`, `country`, and other details. Saying this out loud shows
    you think about data quality — interviewers like that.

    ---
    ## Q3 — Courses nobody has taken (3 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT c.course_id,
               c.course_name
        FROM courses c
        LEFT JOIN grades g ON c.course_id = g.course_id
        WHERE g.grade_id IS NULL
        ORDER BY c.course_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:** the **anti-join** —
    `LEFT JOIN`, then keep the rows where the right side is `NULL`.
    This is one of the most common SQL interview questions. Real
    versions: "customers who never ordered", "products never sold",
    "employees with no manager".

    **Common mistake:** using `INNER JOIN`. It removes exactly the rows
    you are looking for, so you get 0 rows.

    ---
    ## Q4 — The 10 busiest students (10 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT s.student_id,
               s.first_name,
               s.last_name,
               COUNT(*) AS courses_taken
        FROM students s
        INNER JOIN grades g ON s.student_id = g.student_id
        GROUP BY s.student_id, s.first_name, s.last_name
        ORDER BY courses_taken DESC, s.student_id
        LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:** join, group, sort, limit —
    in one query.

    **Two details that matter:**

    - **Group by `student_id`, not by the name.** Q2 showed that many
      students share a name. `GROUP BY first_name, last_name` would
      add their courses together, as if they were one person.
    - **Ties.** Several students took 25 courses. Without a tie-break
      (`, s.student_id`), the 10th row can change from run to run.
      Mention ties before the interviewer does.

    ---
    # Core

    ## Q5 — F grades in every course (50 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT c.course_id,
               c.course_name,
               COUNT(g.grade_id) AS num_f
        FROM courses c
        LEFT JOIN grades g
               ON c.course_id = g.course_id
              AND g.grade = 'F'
        GROUP BY c.course_id, c.course_name
        ORDER BY num_f DESC, c.course_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:** where you put the filter in
    an outer join. This question catches many people with work
    experience.

    The `g.grade = 'F'` test is in the **`ON`** clause, so it decides
    *which grades match*. A course with no F's still has its row, with
    `NULL`s, and `COUNT(g.grade_id)` turns that into 0.

    **Common mistake:** put the test in `WHERE`. `WHERE` runs *after*
    the join and throws away every row where `g.grade` is not `'F'` —
    including the `NULL` rows the `LEFT JOIN` kept. The `LEFT JOIN`
    quietly becomes an `INNER JOIN`. Watch the row count:
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- WRONG: the filter in WHERE drops courses with no F's
        SELECT c.course_id,
               c.course_name,
               COUNT(g.grade_id) AS num_f
        FROM courses c
        LEFT JOIN grades g ON c.course_id = g.course_id
        WHERE g.grade = 'F'
        GROUP BY c.course_id, c.course_name
        ORDER BY num_f DESC, c.course_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    47 rows, not 50. The 3 courses nobody took are gone, with no
    error message. The first rows look identical, which is why this
    bug is easy to miss. **Always check the row count.**

    ---
    ## Q6 — Departments with a high fail rate (2 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT rtrim(c.course_id, '0123456789') AS department,
               COUNT(*) AS num_grades,
               SUM(CASE WHEN g.grade = 'F' THEN 1 ELSE 0 END) AS num_f,
               ROUND(100.0 * SUM(CASE WHEN g.grade = 'F' THEN 1 ELSE 0 END)
                     / COUNT(*), 1) AS pct_f
        FROM grades g
        INNER JOIN courses c ON g.course_id = c.course_id
        GROUP BY department
        HAVING 100.0 * SUM(CASE WHEN g.grade = 'F' THEN 1 ELSE 0 END)
               / COUNT(*) > 5
        ORDER BY pct_f DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:** a **conditional count**.
    `SUM(CASE WHEN … THEN 1 ELSE 0 END)` counts only the rows that
    pass the test. You will use this pattern all the time at work.

    **Two details:**

    - **`100.0`, not `100`.** In many databases (PostgreSQL, SQL
      Server) an integer divided by an integer drops the decimals:
      `85 / 1427` is `0`. Writing `100.0` makes it a decimal division.
      DuckDB happens to be safe here, but write it the portable way.
    - **`HAVING` repeats the formula.** DuckDB lets you write
      `HAVING pct_f > 5`, but most databases do not allow a column
      alias in `HAVING`. Repeating it works everywhere.

    ---
    ## Q7 — One-year students (2 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT s.student_id,
               s.first_name,
               s.last_name,
               MIN(g.year) AS year,
               COUNT(*) AS courses_taken
        FROM students s
        INNER JOIN grades g ON s.student_id = g.student_id
        GROUP BY s.student_id, s.first_name, s.last_name
        HAVING COUNT(DISTINCT g.year) = 1
        ORDER BY s.student_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:** `COUNT(DISTINCT …)` inside
    `HAVING`. "All of their courses in one year" means "only one
    *different* year".

    **The trick for `year`:** you cannot `SELECT g.year` without
    grouping by it. But when a group has only one year, `MIN(g.year)`
    (or `MAX`) **is** that year. Explain this if you use it.

    **Common mistake:** `GROUP BY s.student_id, g.year` and then
    `HAVING COUNT(*) …`. That makes one group per student *per year*,
    so every group has exactly one year, and the question cannot be
    answered.

    ---
    ## Q8 — Students with at least one F, by country (7 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT s.country,
               COUNT(DISTINCT s.student_id) AS num_students,
               COUNT(DISTINCT CASE WHEN g.grade = 'F'
                                   THEN s.student_id END) AS students_with_f,
               ROUND(100.0 * COUNT(DISTINCT CASE WHEN g.grade = 'F'
                                                 THEN s.student_id END)
                     / COUNT(DISTINCT s.student_id), 1) AS pct_with_f
        FROM students s
        LEFT JOIN grades g ON s.student_id = g.student_id
        GROUP BY s.country
        ORDER BY num_students DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:**

    - **`COUNT(DISTINCT …)`.** After the join there is one row per
      *grade*, not per student. `COUNT(*)` would count grades.
    - **`COUNT(DISTINCT CASE WHEN … THEN s.student_id END)`.** The
      `CASE` has no `ELSE`, so it gives `NULL` for non-F rows, and
      `COUNT` skips `NULL`s. This counts each student with an F once,
      even if they have 3 F's.
    - **`LEFT JOIN`, because the question says "count all students".**
      An `INNER JOIN` drops the 5 students with no courses:
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- WRONG for this question: INNER JOIN drops students with no grades
        SELECT s.country,
               COUNT(DISTINCT s.student_id) AS num_students
        FROM students s
        INNER JOIN grades g ON s.student_id = g.student_id
        GROUP BY s.country
        ORDER BY num_students DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The totals are 495 instead of 500. Each country's count is a
    little smaller. That is very hard to notice by eye.

    **A good thing to say out loud:** Italy has the highest rate
    (65%), but Italy has only 20 students. With a small group, a few
    students change the percent a lot. Do not draw a big conclusion
    from it.

    ---
    ## Q9 — Most credits earned (10 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT s.student_id,
               s.first_name,
               s.last_name,
               SUM(CASE WHEN g.grade <> 'F' THEN c.num_of_credits
                        ELSE 0 END) AS credits_earned
        FROM students s
        INNER JOIN grades  g ON s.student_id = g.student_id
        INNER JOIN courses c ON g.course_id  = c.course_id
        GROUP BY s.student_id, s.first_name, s.last_name
        ORDER BY credits_earned DESC, s.student_id
        LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:** a 3-table join, and a
    business rule inside `SUM`.

    **Common mistakes:**

    - `COUNT(*)` instead of `SUM(num_of_credits)` — that counts
      *courses*, not *credits*.
    - Forgetting the F rule. Then you rank students by credits
      *attempted*, which is a different list:
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- WRONG: counts credits for failed courses too
        SELECT s.student_id,
               s.first_name,
               s.last_name,
               SUM(c.num_of_credits) AS credits_earned
        FROM students s
        INNER JOIN grades  g ON s.student_id = g.student_id
        INNER JOIN courses c ON g.course_id  = c.course_id
        GROUP BY s.student_id, s.first_name, s.last_name
        ORDER BY credits_earned DESC, s.student_id
        LIMIT 10;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Same shape — 10 rows, same columns — but different students and
    bigger numbers. The row-count check cannot catch this one. Only
    reading the question carefully can.

    ---
    # Hard

    ## Q10 — GPA by major, done right (5 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT s.major,
               ROUND(AVG(CASE g.grade
                            WHEN 'A' THEN 4
                            WHEN 'B' THEN 3
                            WHEN 'C' THEN 2
                            WHEN 'D' THEN 1
                            WHEN 'F' THEN 0
                         END), 3) AS simple_gpa,
               ROUND(SUM(CASE g.grade
                            WHEN 'A' THEN 4
                            WHEN 'B' THEN 3
                            WHEN 'C' THEN 2
                            WHEN 'D' THEN 1
                            WHEN 'F' THEN 0
                         END * c.num_of_credits)
                     / SUM(c.num_of_credits), 3) AS weighted_gpa
        FROM students s
        INNER JOIN grades  g ON s.student_id = g.student_id
        INNER JOIN courses c ON g.course_id  = c.course_id
        GROUP BY s.major
        ORDER BY weighted_gpa DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:** that you know `AVG` is not
    always the right average.

    A **weighted average** is
    `SUM(value × weight) / SUM(weight)`. Here the value is the grade
    points and the weight is the course's credits. This is how
    universities really compute GPA. The same idea is everywhere at
    work: average price weighted by quantity sold, average rating
    weighted by number of reviews.

    **Does the ranking change?** Yes. With the simple average,
    BUSINESS is first (2.849). With the weighted GPA, ENGINEERING is
    first (2.841). The numbers are close, but a report that says "who
    is first" would be wrong with the simple average.

    ---
    ## Q11 — Repeated courses (0 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT student_id,
               course_id,
               COUNT(*) AS times_taken
        FROM grades
        GROUP BY student_id, course_id
        HAVING COUNT(*) > 1;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:** whether you trust a correct
    answer that is **empty**.

    Zero rows is the right answer here: no student has taken the
    same course twice. Many people panic and start changing a correct
    query. Instead, say what it means: *"There are no repeated
    enrollments in this data."*

    **How to be sure an empty result is real:** test the logic on a
    case where you know the answer. For example, change `> 1` to
    `>= 1`. You should then get one row per enrollment — 8,000 rows.

    **A strong follow-up:** "If repeats should never happen, the
    database can enforce it with a `UNIQUE (student_id, course_id)`
    constraint." That connects the query to database design (Week 6).

    ---
    ## Q12 — Students who never earned an A (1 row)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Decision: "students" means students who took at least one
        -- course. A student with no courses never had a chance to
        -- earn an A, so they do not belong in this list.
        SELECT s.student_id,
               s.first_name,
               s.last_name,
               COUNT(*) AS courses_taken
        FROM students s
        INNER JOIN grades g ON s.student_id = g.student_id
        GROUP BY s.student_id, s.first_name, s.last_name
        HAVING SUM(CASE WHEN g.grade = 'A' THEN 1 ELSE 0 END) = 0
        ORDER BY s.student_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What the interviewer is checking:** whether you **ask a
    question** before you write SQL. "Students who never earned an A"
    can mean two different lists:

    1. Students who took courses but got no A — **1 student.**
    2. That, plus every student who took no courses at all — **6.**

    The best answer in an interview is: *"Do you mean students who
    took at least one course? Five students have no grades at all —
    should they be included?"* Then write the query for the answer
    you get.

    Many people write the anti-join from Q3 here, without thinking
    about it. It silently gives meaning 2:
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- Meaning 2: includes the 5 students who took no courses
        SELECT s.student_id,
               s.first_name,
               s.last_name
        FROM students s
        LEFT JOIN grades g
               ON s.student_id = g.student_id
              AND g.grade = 'A'
        WHERE g.grade_id IS NULL
        ORDER BY s.student_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    6 rows: Emily Davis (224), plus the 5 students with no courses.
    Neither query is "wrong" SQL. The question was unclear. **Asking
    is the skill being tested.**

    ---
    # What These 12 Questions Practiced

    | Skill | Questions | You will use it for… |
    |-------|-----------|------------------------|
    | `GROUP BY` + `HAVING` | Q1, Q2, Q6, Q7, Q11 | any "per category" report |
    | Anti-join (`LEFT JOIN … IS NULL`) | Q3, Q12 | "who never…" questions |
    | Filter in `ON` vs. `WHERE` | Q5, Q12 | keeping zero rows in outer joins |
    | Conditional count `SUM(CASE …)` | Q6, Q9, Q12 | rates, percentages, KPIs |
    | `COUNT(DISTINCT …)` | Q7, Q8 | counting people, not rows |
    | Weighted average | Q10 | GPA, average price, average rating |
    | Ties, empty results, unclear questions | Q4, Q11, Q12 | every interview |

    ### Interview habits

    1. **Repeat the question** in your own words before you type.
    2. **Know the grain:** after a join, what does one row mean? One
       grade? One student?
    3. **Check the row count** against what you expect.
    4. **Say your assumptions** out loud — ties, NULLs, who counts.
    5. **Read the first rows** of your result. Do the numbers make
       sense?

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
