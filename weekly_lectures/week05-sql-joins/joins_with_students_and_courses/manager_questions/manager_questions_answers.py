import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    import sys

    # plot_helpers.py lives in the parent folder, next to notebook.py.
    sys.path.insert(0, str(mo.notebook_dir().parent))
    from plot_helpers import plot_bar, plot_hbar, plot_line, plot_stacked_bar

    return plot_bar, plot_hbar, plot_line, plot_stacked_bar


@app.cell
def _(mo):
    import duckdb

    # Open the clean database in the parent folder, read-only.
    # Build it first with ../create_duckdb_database.sh
    db_path = mo.notebook_dir().parent / "students_courses_grades.duckdb"
    if not db_path.exists():
        raise FileNotFoundError(
            f"{db_path} not found. Build it first:  ../create_duckdb_database.sh"
        )
    con = duckdb.connect(database=str(db_path), read_only=True)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Questions from Managers: Answers

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian

    ---

    Try `manager_questions.py` first. Then come here.

    For each request you get:

    - **One good definition** — not the only one.
    - **The query,** and a chart where it helps the manager.
    - **The answer to send,** written the way you would really send
      it: answer first, then the key numbers, then one honest limit.
    - **Other reasonable definitions,** and how they change the
      result.

    Notice how often the most useful answer is *not* the one the
    manager expected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## M1 — The Dean: "Has grading gotten easier?"

    **Definition:** for each year, the average grade points (GPA), the
    percent of A's, and the percent of F's. If grading got easier, GPA
    and the A's should go up, and the F's should go down.
    """)
    return


@app.cell
def _(con, mo):
    df_m1 = mo.sql(
        f"""
        SELECT year,
               COUNT(*) AS num_grades,
               ROUND(AVG(CASE grade
                            WHEN 'A' THEN 4
                            WHEN 'B' THEN 3
                            WHEN 'C' THEN 2
                            WHEN 'D' THEN 1
                            WHEN 'F' THEN 0
                         END), 2) AS avg_gpa,
               ROUND(100.0 * SUM(CASE WHEN grade = 'A' THEN 1 ELSE 0 END)
                     / COUNT(*), 1) AS pct_a,
               ROUND(100.0 * SUM(CASE WHEN grade = 'F' THEN 1 ELSE 0 END)
                     / COUNT(*), 1) AS pct_f
        FROM grades
        GROUP BY year
        ORDER BY year;
        """,
        engine=con
    )
    return (df_m1,)


@app.cell
def _(df_m1, plot_line):
    plot_line(df_m1, x="year", y="avg_gpa",
              title="Average GPA per year (4.0 scale)", ylabel="average GPA")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **The answer to send:**

    > No. The average GPA has stayed between 2.81 and 2.86 every year
    > from 2021 to 2025, and the share of A's has stayed between 30%
    > and 33%. There is no upward trend. One limit: 2021 has only 411
    > grades (the other years have 1,000+), so 2021 alone is less
    > reliable.

    **Why this is a good answer:** "nothing changed" is a real
    answer. Many people feel they must "find something". A clear "no",
    with the evidence, is often the most valuable answer you can give.

    **Notice the chart:** the y-axis starts at 0. If it started at
    2.80, the tiny changes would look like big jumps — and the chart
    would tell the opposite story.

    **Other reasonable definitions:** compare only 2022–2025 (the
    years with enough grades), or compare within each course, in case
    students simply moved to easier courses.

    ---
    ## M2 — The Registrar: "Which courses should we think about cancelling?"

    **Definition:** courses with the fewest students in the most
    recent year (2025). We also show all 5 years, so a course with one
    bad year is not cancelled by mistake. A `LEFT JOIN` keeps courses
    with **no** students.
    """)
    return


@app.cell
def _(con, mo):
    df_m2 = mo.sql(
        f"""
        SELECT c.course_id,
               c.course_name,
               c.course_level,
               SUM(CASE WHEN g.year = 2025 THEN 1 ELSE 0 END) AS students_2025,
               COUNT(g.grade_id) AS students_all_years
        FROM courses c
        LEFT JOIN grades g ON c.course_id = g.course_id
        GROUP BY c.course_id, c.course_name, c.course_level
        ORDER BY students_2025, c.course_id
        LIMIT 10;
        """,
        engine=con
    )
    return (df_m2,)


@app.cell
def _(df_m2, plot_bar):
    plot_bar(df_m2, labels="course_id", values="students_2025",
             title="The 10 courses with the fewest students in 2025",
             ylabel="students in 2025")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **The answer to send:**

    > Three graduate courses have never had a single student in five
    > years: ENGR204 (Robotics), FIN204 (Fintech and Digital Payments),
    > and MATH204 (Optimization Theory). They are the clear candidates.
    > The next-lowest courses still had 22–29 students in 2025, and
    > most of them are basic undergraduate courses such as Statics and
    > Principles of Management. Before cutting any of those, we should
    > check whether a major requires them.

    **Why this is a good answer:** it separates a **clear** decision
    (zero students in 5 years) from a **risky** one (a basic course
    with 22 students). Data does not know which courses a major
    requires — say so.

    **Other reasonable definitions:** use all 5 years instead of 2025.
    The list changes: then MATH202 (137 students) is the lowest course
    with students, while ENGR102 — lowest in 2025 — is not in the
    bottom 3. Sort by `students_all_years` to see it.

    ---
    ## M3 — The Math Chair: "Is Math really the hardest? If so, why?"

    **Definition:** "hard" = a low average GPA and a high percent of
    F's. First compare departments, then look inside Math.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT rtrim(c.course_id, '0123456789') AS department,
               COUNT(*) AS num_grades,
               ROUND(AVG(CASE g.grade
                            WHEN 'A' THEN 4
                            WHEN 'B' THEN 3
                            WHEN 'C' THEN 2
                            WHEN 'D' THEN 1
                            WHEN 'F' THEN 0
                         END), 2) AS avg_gpa,
               ROUND(100.0 * SUM(CASE WHEN g.grade = 'F' THEN 1 ELSE 0 END)
                     / COUNT(*), 1) AS pct_f
        FROM grades g
        INNER JOIN courses c ON g.course_id = c.course_id
        GROUP BY department
        ORDER BY avg_gpa;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Math is last. Now the "why" — every Math course:
    """)
    return


@app.cell
def _(con, mo):
    df_m3 = mo.sql(
        f"""
        SELECT c.course_id || ' ' || c.course_name AS course,
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
        WHERE c.course_id LIKE 'MATH%'
        GROUP BY c.course_id, c.course_name
        ORDER BY avg_gpa;
        """,
        engine=con
    )
    return (df_m3,)


@app.cell
def _(df_m3, plot_hbar):
    plot_hbar(df_m3, labels="course", values="avg_gpa",
              title="Average GPA in each Math course", xlabel="average GPA",
              decimals=2, xmax=4.0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Two courses are far below the rest. One more query proves the
    point: group the grades into 3 buckets with a `CASE`.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT CASE
                   WHEN g.course_id IN ('MATH105', 'MATH203')
                        THEN '1. Math: the 2 hardest courses'
                   WHEN g.course_id LIKE 'MATH%'
                        THEN '2. Math: the other 7 courses'
                   ELSE '3. All other departments'
               END AS bucket,
               COUNT(*) AS num_grades,
               ROUND(AVG(CASE g.grade
                            WHEN 'A' THEN 4
                            WHEN 'B' THEN 3
                            WHEN 'C' THEN 2
                            WHEN 'D' THEN 1
                            WHEN 'F' THEN 0
                         END), 2) AS avg_gpa
        FROM grades g
        GROUP BY bucket
        ORDER BY bucket;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **The answer to send:**

    > Yes, on average: Math has the lowest GPA of the five departments
    > (2.68, against 2.77–2.93). But the cause is two courses, not the
    > department. Stochastic Processes (2.16) and Discrete Mathematics
    > (2.17) are far below every other Math course. Without them, Math
    > averages 2.82 — close to the 2.86 of all other departments. I
    > suggest looking at those two courses.

    **Why this is a good answer:** it turns a vague reputation ("Math
    is hard") into something the Chair can act on (two specific
    courses). Going one level deeper — department → course — is the
    most common way to find the "why".

    **Other reasonable definitions:** use the percent of F's (Math is
    second, behind Engineering), or compare only undergraduate
    courses.

    ---
    ## M4 — Admissions: "Which countries do our strongest students come from?"

    **Definition:** the average grade points of all grades earned by
    students from each country, with the number of students, so we can
    see how much to trust each average.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT s.country,
               COUNT(DISTINCT s.student_id) AS num_students,
               COUNT(*) AS num_grades,
               ROUND(AVG(CASE g.grade
                            WHEN 'A' THEN 4
                            WHEN 'B' THEN 3
                            WHEN 'C' THEN 2
                            WHEN 'D' THEN 1
                            WHEN 'F' THEN 0
                         END), 2) AS avg_gpa
        FROM students s
        INNER JOIN grades g ON s.student_id = g.student_id
        GROUP BY s.country
        ORDER BY avg_gpa DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **The answer to send:**

    > No country stands out. The average GPA ranges only from 2.77
    > (China) to 2.86 (Canada and Italy) — less than a tenth of a grade
    > point. Canada and Italy also have only 20–30 students each, so a
    > few students can move their average. I would not change
    > recruiting based on these numbers. If you want stronger students,
    > we could look at other data, such as high-school grades or test
    > scores, which this database does not have.

    **Why this is a good answer:** a sorted list *always* has a top
    row. That does not mean the top row is meaningfully better. Saying
    "the differences are too small to act on" protects the Director
    from a bad decision.

    **Other reasonable definitions:** average each *student's* GPA
    first, then average the students (so a student with 25 courses
    does not count more than a student with 8). Or count the share of
    students with a GPA above 3.3. Both need a query inside a query
    (a *subquery*, Week 9). On this data, the per-student average
    gives the same picture (2.78 to 2.85). The "above 3.3" count looks
    different — the USA is highest at 7.5% — but only 23 students in
    the whole university are above 3.3, so each country has 0 to 13 of
    them. That is too few to compare countries fairly.

    ---
    ## M5 — The CFO: "Tuition per department last year, and vs. the year before"

    **Definition:** tuition = credits × $1,200, for every course
    taken — including failed courses, since students pay for those
    too. "Last year" = 2025.
    """)
    return


@app.cell
def _(con, mo):
    df_m5 = mo.sql(
        f"""
        SELECT rtrim(c.course_id, '0123456789') AS department,
               SUM(c.num_of_credits) AS credits,
               SUM(c.num_of_credits) * 1200 AS tuition_usd
        FROM grades g
        INNER JOIN courses c ON g.course_id = c.course_id
        WHERE g.year = 2025
        GROUP BY department
        ORDER BY tuition_usd DESC;
        """,
        engine=con
    )
    return (df_m5,)


@app.cell
def _(df_m5, plot_hbar):
    plot_hbar(df_m5, labels="department", values="tuition_usd",
              title="Tuition by department, 2025",
              xlabel="tuition (US dollars)", money=True)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT g.year,
               SUM(c.num_of_credits) * 1200 AS tuition_usd
        FROM grades g
        INNER JOIN courses c ON g.course_id = c.course_id
        WHERE g.year IN (2024, 2025)
        GROUP BY g.year
        ORDER BY g.year;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **The answer to send:**

    > Tuition in 2025 was $9.74 million. Computer Science brought in
    > the most ($2.40M) and Math the least ($1.73M). That is 8.5% less
    > than 2024 ($10.65M). This assumes $1,200 per credit for every
    > course taken, including failed courses. M8 shows the reason for
    > the drop: fewer students were active in 2025.

    **Why this is a good answer:** the CFO asked two questions, and it
    answers both, in the order asked. It states the assumption (failed
    courses are paid), so the CFO can correct it if it is wrong.

    **Other reasonable definitions:** count only passed courses, or
    split each department's tuition by its own majors vs. other majors
    (see M7).

    ---
    ## M6 — The Dean of Students: "Send me a list of struggling students"

    **Choosing the definition is the real work here.** Before picking
    one, look at how many students each reasonable definition gives.
    This query uses a *subquery* (Week 9): the inner query computes
    each student's numbers, and the outer query counts the students
    who meet each definition.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT SUM(CASE WHEN gpa < 2.0 AND num_courses >= 5
                        THEN 1 ELSE 0 END) AS gpa_under_2_0,
               SUM(CASE WHEN gpa < 2.3 THEN 1 ELSE 0 END) AS gpa_under_2_3,
               SUM(CASE WHEN gpa < 2.5 THEN 1 ELSE 0 END) AS gpa_under_2_5,
               SUM(CASE WHEN f_ever >= 3 THEN 1 ELSE 0 END) AS three_f_ever,
               SUM(CASE WHEN f_ever >= 2 THEN 1 ELSE 0 END) AS two_f_ever,
               SUM(CASE WHEN f_2025 >= 2 THEN 1 ELSE 0 END) AS two_f_in_2025
        FROM (
            SELECT student_id,
                   COUNT(*) AS num_courses,
                   AVG(CASE grade
                          WHEN 'A' THEN 4
                          WHEN 'B' THEN 3
                          WHEN 'C' THEN 2
                          WHEN 'D' THEN 1
                          WHEN 'F' THEN 0
                       END) AS gpa,
                   SUM(CASE WHEN grade = 'F' THEN 1 ELSE 0 END) AS f_ever,
                   SUM(CASE WHEN grade = 'F' AND year = 2025
                            THEN 1 ELSE 0 END) AS f_2025
            FROM grades
            GROUP BY student_id
        );
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    From 1 student to 95, depending only on the definition.

    **Chosen definition:** students who failed **2 or more courses in
    2025**. It is recent (these students may need help *now*), and it
    gives a list the Dean's office can really contact one by one. Each
    row shows what an advisor needs before the first call.
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
               COUNT(*) AS courses_2025,
               SUM(CASE WHEN g.grade = 'F' THEN 1 ELSE 0 END) AS f_2025,
               ROUND(AVG(CASE g.grade
                            WHEN 'A' THEN 4
                            WHEN 'B' THEN 3
                            WHEN 'C' THEN 2
                            WHEN 'D' THEN 1
                            WHEN 'F' THEN 0
                         END), 2) AS gpa_2025
        FROM students s
        INNER JOIN grades g ON s.student_id = g.student_id
        WHERE g.year = 2025
        GROUP BY s.student_id, s.first_name, s.last_name, s.major
        HAVING SUM(CASE WHEN g.grade = 'F' THEN 1 ELSE 0 END) >= 2
        ORDER BY f_2025 DESC, gpa_2025, s.student_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **The answer to send:**

    > Here are the 21 students who failed two or more courses in 2025,
    > with their major and 2025 GPA, most at risk first. I used 2025
    > failures because they show who may need help now. Other
    > definitions give very different lists — from 1 student (GPA
    > under 2.0) to 95 (two F's at any time) — so tell me if you want
    > a wider or narrower list.

    **Why this is a good answer:** it shows the Dean that the list
    size is a **choice**, and offers to change it. Never hide your
    definition — someone will act on this list.

    ---
    ## M7 — The Provost: "Which departments teach other departments' students?"

    **Definition:** compare each grade's course department with the
    student's major. A `CASE` turns the major into a department code.
    Counted per grade (one course taken), from the department's side.
    """)
    return


@app.cell
def _(con, mo):
    df_m7 = mo.sql(
        f"""
        SELECT rtrim(c.course_id, '0123456789') AS department,
               COUNT(*) AS enrollments,
               SUM(CASE WHEN rtrim(c.course_id, '0123456789')
                             = CASE s.major
                                   WHEN 'BUSINESS'         THEN 'BUS'
                                   WHEN 'ENGINEERING'      THEN 'ENGR'
                                   WHEN 'MATH'             THEN 'MATH'
                                   WHEN 'COMPUTER-SCIENCE' THEN 'CSCI'
                                   WHEN 'FINANCE'          THEN 'FIN'
                               END
                        THEN 1 ELSE 0 END) AS own_majors,
               SUM(CASE WHEN rtrim(c.course_id, '0123456789')
                             <> CASE s.major
                                   WHEN 'BUSINESS'         THEN 'BUS'
                                   WHEN 'ENGINEERING'      THEN 'ENGR'
                                   WHEN 'MATH'             THEN 'MATH'
                                   WHEN 'COMPUTER-SCIENCE' THEN 'CSCI'
                                   WHEN 'FINANCE'          THEN 'FIN'
                               END
                        THEN 1 ELSE 0 END) AS other_majors
        FROM grades g
        INNER JOIN students s ON g.student_id = s.student_id
        INNER JOIN courses  c ON g.course_id  = c.course_id
        GROUP BY department
        ORDER BY other_majors * 1.0 / enrollments DESC;
        """,
        engine=con
    )
    return (df_m7,)


@app.cell
def _(df_m7, plot_stacked_bar):
    plot_stacked_bar(df_m7, labels="department",
                     parts=["other_majors", "own_majors"],
                     part_names=["students from other majors",
                                 "students in the department's own major"],
                     title="Who takes each department's courses? (all years)",
                     ylabel="enrollments")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **The answer to send:**

    > Every department teaches many students from other majors. Math
    > depends on them the most: 69% of its enrollments are non-Math
    > students. Even in Computer Science, the lowest, it is 48%. Across
    > the university, only 44% of the courses students take are in
    > their own major. Budgets based only on each department's number
    > of majors would badly under-fund Math and Engineering.

    **Why this is a good answer:** the Provost asked "how much?"; the
    answer gives a number, and then says what it *means* for the
    Provost's real job — the budget.

    **Other reasonable definitions:** look from the student's side
    (what percent of each major's courses are outside it — 41% to 47%
    stay inside), or count only undergraduate courses.

    ---
    ## M8 — The President: "5 or 6 numbers for the board"

    **Definition:** for 2024 and 2025: students active that year (took
    at least one course), courses that had students, grades given,
    credits, courses per active student, average GPA, and the fail
    rate.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT g.year,
               COUNT(DISTINCT g.student_id) AS active_students,
               COUNT(DISTINCT g.course_id)  AS courses_with_students,
               COUNT(*) AS grades_given,
               SUM(c.num_of_credits) AS credits,
               ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT g.student_id), 2)
                   AS courses_per_student,
               ROUND(AVG(CASE g.grade
                            WHEN 'A' THEN 4
                            WHEN 'B' THEN 3
                            WHEN 'C' THEN 2
                            WHEN 'D' THEN 1
                            WHEN 'F' THEN 0
                         END), 2) AS avg_gpa,
               ROUND(100.0 * SUM(CASE WHEN g.grade = 'F' THEN 1 ELSE 0 END)
                     / COUNT(*), 1) AS pct_f
        FROM grades g
        INNER JOIN courses c ON g.course_id = c.course_id
        WHERE g.year IN (2024, 2025)
        GROUP BY g.year
        ORDER BY g.year;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **The answer to send:**

    > The biggest change in 2025: active students fell 26%, from 477
    > to 355. Grades given fell only 7% (2,424 → 2,256), because the
    > students who stayed took more courses — 6.4 each, up from 5.1.
    > Academic quality did not change: the average GPA was 2.83
    > (2.84 in 2024) and 4.9% of grades were F's both years. We should
    > find out why 122 fewer students were active: graduation, or
    > students leaving?

    **Why this is a good answer:** out of 7 numbers, it leads with the
    one that changed the most, explains it with a second number, and
    ends with the question the board will ask anyway. Numbers that did
    *not* change are reported in one sentence, as good news.

    **Watch out:** `courses_per_student` uses `* 1.0` so the division
    keeps its decimals in any database.

    ---
    ## What These 8 Requests Practiced

    | Habit | Where |
    |-------|-------|
    | Turn a vague word into a precise measure | all, especially M6 ("struggling") |
    | "No change" is a real answer | M1, M4 |
    | Go one level deeper to find the "why" | M3 (department → course) |
    | Keep the zeros with a `LEFT JOIN` | M2 |
    | State your assumptions | M5 (failed courses are paid) |
    | Show how the definition changes the result | M2, M6 |
    | Lead with the number that matters most | M7, M8 |

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
