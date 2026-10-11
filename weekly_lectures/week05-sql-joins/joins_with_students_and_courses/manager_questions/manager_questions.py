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
    # OMIS 105 — Questions from Managers

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Database:** `../students_courses_grades.duckdb` (read-only)

    ---

    At work, nobody hands you a precise SQL exercise. A manager sends
    you a short message, often vague, and expects an **answer** — not
    a table.

    In this notebook, 8 people at the university each send you one
    request. For each request, you do 3 things:

    1. **Define it.** Decide exactly what you will measure. "Struggling
       students" or "low enrollment" can mean many things. Choose one
       meaning and write it down.
    2. **Query it.** Write the SQL.
    3. **Answer it.** Write 2–3 sentences you could send back.

    Write your definition and your answer as `--` comments at the top
    of each SQL cell. There is a template in every cell.

    ### What a good answer looks like

    | | Weak answer | Strong answer |
    |---|-------------|---------------|
    | **Starts with** | "Here is the table." | The answer: "No — grades have not changed." |
    | **Gives** | 10 numbers | 1 or 2 numbers that matter |
    | **Says** | nothing about limits | one honest limit ("2021 has few grades") |
    | **Ends with** | nothing | what to do next, if anything |

    There is often **more than one correct definition**. What matters
    is that you choose one, say it clearly, and that your numbers
    match it.

    ### The tables

    ```
    students (student_id, first_name, last_name, major, gender, country)
    grades   (grade_id, student_id, course_id, year, grade)
    courses  (course_id, course_name, course_level, num_of_credits)
    ```

    Useful pieces from earlier notebooks:

    - **Grade points:** `CASE grade WHEN 'A' THEN 4 WHEN 'B' THEN 3
      WHEN 'C' THEN 2 WHEN 'D' THEN 1 WHEN 'F' THEN 0 END`
    - **Department:** `rtrim(course_id, '0123456789')` turns
      `'MATH105'` into `'MATH'`.
    - **Count rows that pass a test:** `SUM(CASE WHEN … THEN 1 ELSE 0 END)`
    - **Keep rows with no match:** `LEFT JOIN`, and put extra
      conditions in `ON`.
    - Grades cover the years **2021–2025**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## M1 — The Dean

    > *"People keep telling me grading has gotten easier. Is that
    > true?"*

    **Before you write SQL, think:**

    - "Easier" how? A higher average GPA? More A's? Fewer F's?
    - Over what time? You have 2021–2025.
    - Does every year have enough grades to compare fairly?

    **Sanity check:** if you count grades per year, the counts add up
    to 8,000.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- My definition:
        --
        -- My answer to the Dean (2-3 sentences):
        --
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## M2 — The Registrar

    > *"We need to save money. Which courses should we think about
    > cancelling?"*

    **Before you write SQL, think:**

    - What makes a course a candidate? Few students? None at all?
    - Few students **when**? Over all 5 years, or last year (2025)?
    - Will your query show a course that had **zero** students? Which
      join keeps it?
    - Is "few students" enough reason to cancel? What else would you
      want to know?

    **Sanity check:** the list of all courses has 50 rows.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- My definition:
        --
        -- My answer to the Registrar (2-3 sentences):
        --
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## M3 — The Chair of the Math Department

    > *"Students say Math is the hardest department. Is that fair? If
    > it is true, I want to know why."*

    **Before you write SQL, think:**

    - How do you measure "hard"? Average GPA? Percent of F's?
    - Compare Math with what — each other department?
    - If Math is lower, is it **every** Math course, or just a few?
      (That is the "why".)

    *Hint:* you may need two queries — one per department, then one
    per Math course. Use two cells if you like.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- My definition:
        --
        -- My answer to the Chair (2-3 sentences):
        --
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## M4 — The Director of Admissions

    > *"I want to recruit more students like our best ones. Which
    > countries do our strongest students come from?"*

    **Before you write SQL, think:**

    - What is a "strong" student? A high GPA?
    - Some countries have 20 students, some have 170. Is a small
      group's average as reliable as a big group's?
    - How big must a difference be before it matters for a decision?
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- My definition:
        --
        -- My answer to the Director (2-3 sentences):
        --
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## M5 — The Chief Financial Officer

    > *"Tuition is $1,200 per credit. How much tuition did each
    > department bring in last year? And how does last year compare
    > with the year before?"*

    **Before you write SQL, think:**

    - "Last year" is 2025 in this data. The year before is 2024.
    - Tuition = credits × $1,200. Where do the credits come from?
    - Does a student who fails a course still pay for it? (Assume
      yes, and say so.)

    *Hint:* two questions, so two results: tuition per department in
    2025, and total tuition per year.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- My definition:
        --
        -- My answer to the CFO (2-3 sentences):
        --
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## M6 — The Dean of Students

    > *"I want to reach out to students who are struggling. Send me a
    > list."*

    **Before you write SQL, think:**

    - What does "struggling" mean? A low GPA? Several F's? How low?
      How many?
    - **Now** or ever? A student who failed two courses in 2021 and
      has done well since may not need help today.
    - How long should the list be? Can the Dean's office really
      contact 100 students? 5?
    - What should each row show so the Dean's office can act on it?

    Try two or three definitions and look at how the list size
    changes. Then pick one and explain why.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- My definition:
        --
        -- My answer to the Dean of Students (2-3 sentences):
        --
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## M7 — The Provost

    > *"How much do students take courses outside their own major? I
    > need to know which departments teach other departments'
    > students."*

    **Before you write SQL, think:**

    - A student's `major` is a word like `'COMPUTER-SCIENCE'`. A
      course's department is a code like `'CSCI'`. How do you compare
      them?
    - Count per student, or per grade (one course taken)?

    *Hint:* a `CASE` can turn a major into its department code:
    `CASE s.major WHEN 'BUSINESS' THEN 'BUS' WHEN 'ENGINEERING' THEN
    'ENGR' WHEN 'MATH' THEN 'MATH' WHEN 'COMPUTER-SCIENCE' THEN 'CSCI'
    WHEN 'FINANCE' THEN 'FIN' END`
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- My definition:
        --
        -- My answer to the Provost (2-3 sentences):
        --
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## M8 — The President, for the Board of Trustees

    > *"I have 2 minutes at the board meeting. Give me the 5 or 6
    > numbers that best describe last year, and how each one changed
    > from the year before."*

    **Before you write SQL, think:**

    - Which numbers would a board care about? Students? Courses?
      Grades? Credits? GPA? Fail rate?
    - "Students" — all 500 in the table, or only those who took a
      course that year?
    - One query can return all the numbers: one row per year,
      `WHERE year IN (2024, 2025)`.

    When you look at your result, one number changed much more than
    the others. Your answer should start with it.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        -- My definition:
        --
        -- My answer to the President (2-3 sentences):
        --
        SELECT 'not answered yet' AS todo;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ### When you are done

    Open `manager_questions_answers.py`. For each request it shows one
    good definition, the query, a chart where it helps, the answer it
    would send — and **other reasonable definitions**, with how they
    change the result. If your definition differs, that is fine. Check
    that your numbers match *your* definition, and that your answer
    says which one you used.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
