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
    return con, duckdb


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Data-Quality Round: Answers

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian

    ---

    Try `data_quality.py` first. Then come here.

    For each task you get a solution, what it teaches, and — where it
    helps — the **tempting wrong query**, run for real, so you can see
    how many bad rows it misses.

    At the end, two summaries:

    1. **A data-quality report** — one query that counts every
       problem. This is what you would send your manager.
    2. **Would the rules have stopped it?** We load `../db_schema.sql`
       into an empty database, try to insert one bad row of each kind,
       and see which ones the database rejects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part A — Profile the Data

    ## DQ1 — Rows vs. unique ids
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT 'raw_students' AS table_name,
               COUNT(*) AS num_rows,
               COUNT(DISTINCT student_id) AS num_distinct_ids
        FROM raw_students
        UNION ALL
        SELECT 'raw_courses', COUNT(*), COUNT(DISTINCT course_id)
        FROM raw_courses
        UNION ALL
        SELECT 'raw_grades', COUNT(*), COUNT(DISTINCT grade_id)
        FROM raw_grades;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** **profile before you query.** In 10 seconds
    you learn that `raw_students` has 4 extra rows (504 rows, 500 ids)
    and `raw_grades` has 2 extra (8,013 rows, 8,011 ids). An id is
    supposed to name exactly one row, so both tables have a problem
    before you have looked at a single value.

    ---
    # Part B — Students

    ## DQ2 — Duplicate student ids (4 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT student_id,
               COUNT(*) AS num_rows
        FROM raw_students
        GROUP BY student_id
        HAVING COUNT(*) > 1
        ORDER BY student_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** the standard duplicate check —
    `GROUP BY` the key, `HAVING COUNT(*) > 1`. You will write this
    query hundreds of times in your career.

    ## DQ3 — Exact copies (3 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT student_id,
               COUNT(*) AS num_copies
        FROM raw_students
        GROUP BY student_id, first_name, last_name, major, gender, country
        HAVING COUNT(*) > 1
        ORDER BY student_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** two kinds of duplicates need two different
    fixes.

    - **Exact copies** (12, 205, 333): safe to remove — keep one row.
    - **Conflicting versions** (88): in DQ2 but not here. Look at its
      two rows below: one says `BUSINESS`, the other `FINANCE`. SQL
      cannot tell you which one is true. **Someone has to ask the
      registrar.** A good analyst flags this instead of guessing.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM raw_students
        WHERE student_id = 88;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Why duplicates hurt every join:** each grade of a duplicated
    student now matches **two** student rows. `raw_grades` has 8,013
    rows, but joining it to `raw_students` gives more:
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT (SELECT COUNT(*) FROM raw_grades) AS grade_rows,
               COUNT(*) AS rows_after_join
        FROM raw_grades g
        INNER JOIN raw_students s ON g.student_id = s.student_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    8,080 rows. Every total built on that join — credits, GPA, revenue
    in a business setting — is quietly too big. This is called a
    **fan-out**, and it is one of the most common causes of wrong
    numbers in real reports.

    ## DQ4 — Country spellings (6 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT '[' || country || ']' AS country,
               COUNT(*) AS num_rows
        FROM raw_students
        WHERE country NOT IN ('USA', 'CANADA', 'CHINA', 'INDIA',
                              'GERMANY', 'MEXICO', 'ITALY')
        GROUP BY country
        ORDER BY country;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** check values against an **allowed list**.
    The brackets show the problems you cannot see: `[ INDIA]` and
    `[China ]` have extra spaces. Without the brackets, `' INDIA'`
    looks exactly like `'INDIA'` in a result table — but `GROUP BY`
    treats them as different countries.

    ## DQ5 — Fix the dean's report (7 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT CASE upper(trim(country))
                   WHEN 'UNITED STATES' THEN 'USA'
                   WHEN 'U.S.A.'        THEN 'USA'
                   ELSE upper(trim(country))
               END AS country,
               COUNT(DISTINCT student_id) AS num_students
        FROM raw_students
        GROUP BY 1
        ORDER BY num_students DESC, country;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** cleaning in two steps.

    1. **Standardize:** `trim()` removes the spaces, `upper()` fixes
       the case, and `CASE` maps the other spellings to `'USA'`.
    2. **De-duplicate:** `COUNT(DISTINCT student_id)` counts each
       student once.

    `GROUP BY 1` means "group by the first column in the `SELECT`" —
    here, the cleaned country. It saves repeating the long `CASE`.

    **The tempting wrong query** fixes the names but forgets step 2.
    USA and CHINA come out 2 too high each:
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- WRONG: COUNT(*) counts the duplicate rows too
        SELECT CASE upper(trim(country))
                   WHEN 'UNITED STATES' THEN 'USA'
                   WHEN 'U.S.A.'        THEN 'USA'
                   ELSE upper(trim(country))
               END AS country,
               COUNT(*) AS num_students
        FROM raw_students
        GROUP BY 1
        ORDER BY num_students DESC, country;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ6 — Missing names (3 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT student_id,
               first_name,
               last_name
        FROM raw_students
        WHERE first_name IS NULL OR trim(first_name) = ''
           OR last_name  IS NULL OR trim(last_name)  = ''
        ORDER BY student_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** "missing" has two forms in a text column:

    - `NULL` — no value at all (students 20 and 21).
    - `''` — an **empty string**: a value, but with nothing in it
      (student 30). It is **not** `NULL`, so `IS NULL` does not find
      it. `trim()` also catches a value that is only spaces.

    **The tempting wrong query** only checks `IS NULL`, and finds 2:
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- WRONG: misses the empty string
        SELECT student_id,
               first_name,
               last_name
        FROM raw_students
        WHERE first_name IS NULL
           OR last_name  IS NULL
        ORDER BY student_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ7 — Invalid gender codes (4 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT student_id,
               gender
        FROM raw_students
        WHERE gender NOT IN ('MALE', 'FEMALE', 'NA')
           OR gender IS NULL
        ORDER BY student_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** codes drift when people type them by hand:
    `M`, `F`, `Female`, `male`. Text comparison is **case-sensitive**,
    so `'male'` is not `'MALE'`. The `OR gender IS NULL` part finds
    nothing here, but always include it — see DQ12 for why.

    ---
    # Part C — Courses

    ## DQ8 — Invalid courses (3 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT course_id,
               course_level,
               num_of_credits
        FROM raw_courses
        WHERE course_level NOT IN ('undergraduate', 'graduate')
           OR course_level IS NULL
           OR num_of_credits IS NULL
           OR num_of_credits <= 0
        ORDER BY course_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** check numbers against a **valid range**, not
    only text against a list. A course with 0 credits would make
    every credit-weighted GPA (interview question Q10) quietly wrong
    for the students who took it.

    ---
    # Part D — Grades

    ## DQ9 — Grades for unknown students (4 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT g.grade_id,
               g.student_id,
               g.course_id
        FROM raw_grades g
        LEFT JOIN raw_students s ON g.student_id = s.student_id
        WHERE s.student_id IS NULL
        ORDER BY g.grade_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** the anti-join is also a data-quality tool.
    Rows like these are called **orphans**: children (grades) whose
    parent (a student) does not exist. An `INNER JOIN` would silently
    drop them from every report — 4 grades would just disappear.

    ## DQ10 — Grades for unknown courses (5 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT g.grade_id,
               g.student_id,
               g.course_id
        FROM raw_grades g
        LEFT JOIN raw_courses c ON g.course_id = c.course_id
        WHERE c.course_id IS NULL
        ORDER BY g.grade_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** look at your orphans before you delete them.
    These 5 rows are two different problems:

    - `fin106`, `math104`, `engr101` are **real courses**, typed in
      lowercase. They can be fixed with `upper()`.
    - `CSCI999` is a course that really does not exist. These 2 rows
      need a human decision.

    After fixing the case, only the 2 real orphans remain:
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- After the fix: join on upper(course_id)
        SELECT g.grade_id,
               g.student_id,
               g.course_id
        FROM raw_grades g
        LEFT JOIN raw_courses c ON upper(g.course_id) = c.course_id
        WHERE c.course_id IS NULL
        ORDER BY g.grade_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ11 — Impossible years (4 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT grade_id,
               student_id,
               year
        FROM raw_grades
        WHERE year NOT BETWEEN 2021 AND 2025
           OR year IS NULL
        ORDER BY grade_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** two typical kinds of bad dates. **2027** is
    in the future — impossible for a grade that was already given.
    **1925** looks like a typing mistake (2025 → 1925). A quick
    `MIN(year)` and `MAX(year)` per table finds both in seconds; make
    it a habit.

    ## DQ12 — Invalid or missing grades (7 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT grade_id,
               grade
        FROM raw_grades
        WHERE grade NOT IN ('A', 'B', 'C', 'D', 'F')
           OR grade IS NULL
        ORDER BY grade_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** the most important `NULL` rule in SQL.

    For a `NULL` grade, `grade NOT IN ('A', …)` is not `TRUE` and not
    `FALSE` — it is **unknown**. `WHERE` keeps only rows where the
    test is `TRUE`, so `NULL` rows are silently skipped. You must ask
    for them with `IS NULL`.

    **The tempting wrong query** finds 5 of the 7 problems:
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- WRONG: NOT IN skips the NULL grades
        SELECT grade_id,
               grade
        FROM raw_grades
        WHERE grade NOT IN ('A', 'B', 'C', 'D', 'F')
        ORDER BY grade_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## DQ13 — The same course, loaded twice (5 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT student_id,
               course_id,
               COUNT(*) AS num_rows
        FROM raw_grades
        GROUP BY student_id, course_id
        HAVING COUNT(*) > 1
        ORDER BY student_id, course_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** a duplicate does not always have the same id.
    These rows have **different** `grade_id` values, so the id check
    in DQ1 cannot see them. You find them by grouping on what the row
    *means* — one student, one course — not on its id.

    Compare with interview question Q11: on the clean data, this exact
    query returns 0 rows.

    ## DQ14 — Reused grade ids (2 rows)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT grade_id,
               COUNT(*) AS num_rows
        FROM raw_grades
        GROUP BY grade_id
        HAVING COUNT(*) > 1
        ORDER BY grade_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **What it teaches:** the opposite of DQ13 — the **same id** on
    two **different** rows. DQ1 hinted at this: 8,013 rows but only
    8,011 ids. Any query that looks up "grade 600" now gets two
    answers.

    ---
    # Summary 1 — The Data-Quality Report

    One query, one row per problem. This is what you send your
    manager. Each count matches the task above.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT 'DQ2'  AS check_id, 'duplicate student ids' AS problem,
               COUNT(*) AS rows_affected
        FROM (SELECT student_id FROM raw_students
              GROUP BY student_id HAVING COUNT(*) > 1)
        UNION ALL
        SELECT 'DQ4', 'non-standard country', COUNT(*)
        FROM raw_students
        WHERE country NOT IN ('USA', 'CANADA', 'CHINA', 'INDIA',
                              'GERMANY', 'MEXICO', 'ITALY')
        UNION ALL
        SELECT 'DQ6', 'missing name', COUNT(*)
        FROM raw_students
        WHERE first_name IS NULL OR trim(first_name) = ''
           OR last_name  IS NULL OR trim(last_name)  = ''
        UNION ALL
        SELECT 'DQ7', 'invalid gender', COUNT(*)
        FROM raw_students
        WHERE gender NOT IN ('MALE', 'FEMALE', 'NA') OR gender IS NULL
        UNION ALL
        SELECT 'DQ8', 'invalid course', COUNT(*)
        FROM raw_courses
        WHERE course_level NOT IN ('undergraduate', 'graduate')
           OR course_level IS NULL
           OR num_of_credits IS NULL OR num_of_credits <= 0
        UNION ALL
        SELECT 'DQ9', 'grade for unknown student', COUNT(*)
        FROM raw_grades g
        LEFT JOIN raw_students s ON g.student_id = s.student_id
        WHERE s.student_id IS NULL
        UNION ALL
        SELECT 'DQ10', 'grade for unknown course', COUNT(*)
        FROM raw_grades g
        LEFT JOIN raw_courses c ON g.course_id = c.course_id
        WHERE c.course_id IS NULL
        UNION ALL
        SELECT 'DQ11', 'year outside 2021-2025', COUNT(*)
        FROM raw_grades
        WHERE year NOT BETWEEN 2021 AND 2025 OR year IS NULL
        UNION ALL
        SELECT 'DQ12', 'invalid or missing grade', COUNT(*)
        FROM raw_grades
        WHERE grade NOT IN ('A', 'B', 'C', 'D', 'F') OR grade IS NULL
        UNION ALL
        SELECT 'DQ13', 'same student + course twice', COUNT(*)
        FROM (SELECT student_id, course_id FROM raw_grades
              GROUP BY student_id, course_id HAVING COUNT(*) > 1)
        UNION ALL
        SELECT 'DQ14', 'reused grade id', COUNT(*)
        FROM (SELECT grade_id FROM raw_grades
              GROUP BY grade_id HAVING COUNT(*) > 1);
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The `FROM (SELECT …)` parts are **subqueries**: a query inside a
    query. Each one first finds the duplicated keys, and the outer
    `COUNT(*)` counts them. You will learn subqueries properly in
    Week 9.

    ---
    # Summary 2 — Would the Rules Have Stopped It?

    The clean database is built from `../db_schema.sql`, which has
    `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, and `ENUM` rules. The
    cell below loads that schema into a new, empty, in-memory
    database, adds one valid student, course, and grade, and then
    tries to insert **one bad row of each kind**. It records whether
    DuckDB accepted or rejected it.
    """)
    return


@app.cell
def _(duckdb, mo):
    import pandas as pd

    test_db = duckdb.connect(database=":memory:")
    test_db.execute((mo.notebook_dir().parent / "db_schema.sql").read_text())
    test_db.execute("INSERT INTO courses  VALUES ('BUS101', 'Intro', 'undergraduate', 3)")
    test_db.execute("INSERT INTO courses  VALUES ('BUS102', 'Writing', 'undergraduate', 3)")
    test_db.execute("INSERT INTO students VALUES (1, 'Ann', 'Lee', 'BUSINESS', 'FEMALE', 'USA')")
    test_db.execute("INSERT INTO grades   VALUES (1, 1, 'BUS101', 2024, 'A')")

    attempts = [
        ("DQ2",  "duplicate student_id",
         "INSERT INTO students VALUES (1, 'Ann', 'Lee', 'BUSINESS', 'FEMALE', 'USA')"),
        ("DQ4",  "country 'usa'",
         "INSERT INTO students VALUES (2, 'Bo', 'Kim', 'MATH', 'MALE', 'usa')"),
        ("DQ6",  "last_name NULL",
         "INSERT INTO students VALUES (3, 'Cy', NULL, 'MATH', 'MALE', 'USA')"),
        ("DQ6",  "first_name '' (empty)",
         "INSERT INTO students VALUES (4, '', 'Diaz', 'MATH', 'MALE', 'USA')"),
        ("DQ7",  "gender 'M'",
         "INSERT INTO students VALUES (5, 'Ed', 'Fox', 'MATH', 'M', 'USA')"),
        ("DQ8",  "course_level 'Graduate'",
         "INSERT INTO courses VALUES ('BUS201', 'Strategy', 'Graduate', 3)"),
        ("DQ8",  "num_of_credits 0",
         "INSERT INTO courses VALUES ('BUS106', 'Law', 'undergraduate', 0)"),
        ("DQ9",  "grade for student 9001",
         "INSERT INTO grades VALUES (2, 9001, 'BUS101', 2024, 'B')"),
        ("DQ10", "grade for course 'bus101'",
         "INSERT INTO grades VALUES (3, 1, 'bus101', 2024, 'B')"),
        ("DQ11", "year 2027",
         "INSERT INTO grades VALUES (4, 1, 'BUS102', 2027, 'B')"),
        ("DQ12", "grade 'A+'",
         "INSERT INTO grades VALUES (5, 1, 'BUS101', 2024, 'A+')"),
        ("DQ12", "grade NULL",
         "INSERT INTO grades VALUES (6, 1, 'BUS101', 2024, NULL)"),
        ("DQ13", "same student + course twice",
         "INSERT INTO grades VALUES (7, 1, 'BUS101', 2024, 'A')"),
        ("DQ14", "reused grade_id",
         "INSERT INTO grades VALUES (1, 1, 'BUS102', 2024, 'C')"),
    ]

    results = []
    for check_id, bad_row, sql in attempts:
        try:
            test_db.execute(sql)
            results.append((check_id, bad_row, "ACCEPTED — the rules missed it", ""))
        except duckdb.Error as err:
            results.append((check_id, bad_row, "rejected",
                            str(err).splitlines()[0][:70]))
    test_db.close()

    pd.DataFrame(results, columns=["check_id", "bad_row", "result", "error"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **10 of 14 bad rows are rejected.** The rules in `db_schema.sql`
    do a lot of work: the `PRIMARY KEY`s stop reused ids, the
    `FOREIGN KEY`s stop orphans, `NOT NULL` stops missing values, and
    the `ENUM` types stop misspelled countries, genders, levels, and
    grades.

    The `ENUM` errors look strange: *"Could not convert string 'usa'
    to UINT8"*. DuckDB stores an `ENUM` as a small number, one per
    allowed value. The message just means **"'usa' is not in the
    list."**

    **But 4 get through,** because no rule covers them:

    | Problem | Missing rule (you will learn `CHECK` and `UNIQUE` in Weeks 6–8) |
    |---------|-------------------|
    | empty first name `''` | `CHECK (trim(first_name) <> '')` |
    | 0 credits | `CHECK (num_of_credits > 0)` |
    | year 2027 | `CHECK (year BETWEEN 2000 AND 2100)`, or a check against today's date when rows are loaded |
    | same student + course twice | `UNIQUE (student_id, course_id)` |

    ### The lesson

    1. **Rules in the database are the first line of defense.** They
       stop bad data *before* it gets in, every time, for free.
    2. **Rules never cover everything.** So analysts still write
       checks like the ones in this round — and run them every time
       new data arrives.
    3. **Count, then report.** A manager can act on "11 kinds of
       problems, with the rows for each". They cannot act on "the
       data looks weird".

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
