import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 06: Joins II
    ## Lab 1 — INNER, LEFT & RIGHT JOIN, Finding What Is Missing · Instructor

    Work with the **Valley Fitness** gym database (members, bookings, classes, trainers). It is the same data as this week's demos. Run the setup cells first, then each question. Answers are filled in.

    The data has gaps on purpose:

    - Ava Martinez and Ben Taylor never booked a class
    - Booking 1015 belongs to member 12, who does not exist
    - Aqua Fitness was never booked; Senior Stretch has no trainer
    - Maria Lopez and Noah Kim teach no class

    See `week06_lab_01_design_notes.md`: every "find the missing" question was checked to return real rows.
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    members = mo.sql(
        f"""
        CREATE OR REPLACE TABLE members AS
        SELECT * FROM (
          VALUES
            (1, 'Olivia Brown', 'Santa Clara', DATE '2025-01-15'),
            (2, 'Liam Garcia', 'San Jose', DATE '2025-02-03'),
            (3, 'Sophia Nguyen', 'Santa Clara', DATE '2025-03-21'),
            (4, 'Ethan Patel', 'Sunnyvale', DATE '2025-04-10'),
            (5, 'Mia Johnson', 'San Jose', DATE '2025-05-05'),
            (6, 'Lucas Rossi', 'Cupertino', DATE '2025-06-18'),
            (7, 'Ava Martinez', 'Santa Clara', DATE '2025-07-01'),
            (8, 'Ben Taylor', 'Sunnyvale', DATE '2025-08-12'),
            (9, 'Chloe Davis', 'San Jose', DATE '2026-01-09'),
            (10, 'Ryan Lee', 'Cupertino', DATE '2026-02-14')
        ) AS t(member_id, member_name, city, join_date);
        """
    )
    return


@app.cell
def _(mo):
    bookings = mo.sql(
        f"""
        CREATE OR REPLACE TABLE bookings AS
        SELECT * FROM (
          VALUES
            (1001, 1, 101, DATE '2026-09-01'),
            (1002, 1, 102, DATE '2026-09-03'),
            (1003, 2, 103, DATE '2026-09-02'),
            (1004, 3, 101, DATE '2026-09-02'),
            (1005, 3, 104, DATE '2026-09-05'),
            (1006, 4, 102, DATE '2026-09-04'),
            (1007, 5, 105, DATE '2026-09-06'),
            (1008, 5, 103, DATE '2026-09-08'),
            (1009, 6, 106, DATE '2026-09-07'),
            (1010, 9, 101, DATE '2026-09-09'),
            (1011, 9, 107, DATE '2026-09-10'),
            (1012, 10, 102, DATE '2026-09-11'),
            (1013, 1, 103, DATE '2026-09-12'),
            (1014, 2, 105, DATE '2026-09-12'),
            (1015, 12, 104, DATE '2026-09-13'),
            (1016, 4, 101, DATE '2026-09-15')
        ) AS t(booking_id, member_id, class_id, booking_date);
        """
    )
    return


@app.cell
def _(mo):
    classes = mo.sql(
        f"""
        CREATE OR REPLACE TABLE classes AS
        SELECT * FROM (
          VALUES
            (101, 'Morning Yoga', 3, 15),
            (102, 'Spin Cycle', 2, 20),
            (103, 'HIIT Bootcamp', 4, 25),
            (104, 'Pilates Core', 5, 18),
            (105, 'Strength Basics', 2, 22),
            (106, 'Boxing Fit', 4, 25),
            (107, 'Senior Stretch', NULL, 12),
            (108, 'Aqua Fitness', 5, 16)
        ) AS t(class_id, class_name, trainer_id, price);
        """
    )
    return


@app.cell
def _(mo):
    trainers = mo.sql(
        f"""
        CREATE OR REPLACE TABLE trainers AS
        SELECT * FROM (
          VALUES
            (1, 'Maria Lopez', NULL),
            (2, 'James Chen', 1),
            (3, 'Aisha Khan', 1),
            (4, 'Diego Santos', 2),
            (5, 'Emma Wilson', 2),
            (6, 'Noah Kim', 3)
        ) AS t(trainer_id, trainer_name, manager_id);
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q1. Every class, with its bookings (`LEFT JOIN`)

    Show `class_name` and `booking_id` for **every** class, including a class with no bookings.

    🔮 **Predict:** 17 rows = 16 bookings + 1 row for Aqua Fitness (with `NULL`).
    """)
    return


@app.cell
def _(bookings, classes, mo):
    q1 = mo.sql(
        f"""
        -- Predict: 17 rows
        SELECT c.class_name, b.booking_id
        FROM classes c
        LEFT JOIN bookings b ON c.class_id = b.class_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. Bookings for classes that cost $20 or more (`INNER JOIN`)

    Show `booking_id`, `class_name`, and `price` for bookings of classes with a price of **20 or more**.

    Expected: 9 rows.
    """)
    return


@app.cell
def _(bookings, classes, mo):
    q2 = mo.sql(
        f"""
        SELECT b.booking_id, c.class_name, c.price
        FROM bookings b
        INNER JOIN classes c ON b.class_id = c.class_id
        WHERE c.price >= 20;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. Q1 again — with `RIGHT JOIN`

    Rewrite Q1 so it starts `FROM bookings b` and uses `RIGHT JOIN classes c`. You must get the same rows as Q1.

    ✍️ **Explain it (sample answer):** "Both keep every row of `classes`. `LEFT` keeps the table on the left of the word JOIN, `RIGHT` keeps the table on the right — here that is `classes` both times, so the result is the same 17 rows."
    """)
    return


@app.cell
def _(bookings, classes, mo):
    q3 = mo.sql(
        f"""
        SELECT c.class_name, b.booking_id
        FROM bookings b
        RIGHT JOIN classes c ON c.class_id = b.class_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. Members in Sunnyvale or Cupertino who never booked

    Show `member_name` and `city` of members who live in **Sunnyvale or Cupertino** and have **no** bookings.

    Expected: 1 row — Ben Taylor. The city filter is on the **left** table, so it belongs in `WHERE`. (Ava has no bookings too, but she lives in Santa Clara.)
    """)
    return


@app.cell
def _(bookings, members, mo):
    q4 = mo.sql(
        f"""
        SELECT m.member_name, m.city
        FROM members m
        LEFT JOIN bookings b ON m.member_id = b.member_id
        WHERE b.booking_id IS NULL
          AND m.city IN ('Sunnyvale', 'Cupertino');
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Classes with no trainer

    Use `LEFT JOIN trainers` and `IS NULL` to find classes that have **no trainer**. Show `class_name`.

    Expected: 1 row — Senior Stretch.
    """)
    return


@app.cell
def _(classes, mo, trainers):
    q5 = mo.sql(
        f"""
        SELECT c.class_name
        FROM classes c
        LEFT JOIN trainers t ON c.trainer_id = t.trainer_id
        WHERE t.trainer_id IS NULL;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. Every member and their booking dates (`COALESCE`)

    Show every member's `member_name` and each `booking_date`. Members with no bookings should show the text `'no bookings yet'`. *Hint:* `CAST(b.booking_date AS VARCHAR)` turns a date into text.

    Expected: 17 rows. Ava and Ben show `no bookings yet`.
    """)
    return


@app.cell
def _(bookings, members, mo):
    q6 = mo.sql(
        f"""
        SELECT m.member_name,
               COALESCE(CAST(b.booking_date AS VARCHAR), 'no bookings yet') AS booking_date
        FROM members m
        LEFT JOIN bookings b 
            ON m.member_id = b.member_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. Every class, with Olivia's bookings only

    Show `class_name` and `booking_id` for **every** class (all 8), but only fill in the bookings made by member **1** (Olivia Brown). Classes she did not book show `NULL`.

    Expected: 8 rows — Olivia's three bookings (1001, 1002, 1013) and five `NULL`s. The `b.member_id = 1` filter must go in `ON`; in `WHERE` it would return only 3 rows.
    """)
    return


@app.cell
def _(bookings, classes, mo):
    q7 = mo.sql(
        f"""
        SELECT c.class_name, b.booking_id
        FROM classes c
        LEFT JOIN bookings b
            ON c.class_id = b.class_id
           AND b.member_id = 1;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. New members (joined in 2026) and their bookings

    Show `member_name`, `join_date`, and `booking_id` for members who joined on or after `2026-01-01`. Keep them even if they have no bookings.

    Expected: 3 rows (Chloe twice, Ryan once). The date filter is on the **left** table, so `WHERE` is correct here.
    """)
    return


@app.cell
def _(bookings, members, mo):
    q8 = mo.sql(
        f"""
        SELECT m.member_name, m.join_date, b.booking_id
        FROM members m
        LEFT JOIN bookings b ON m.member_id = b.member_id
        WHERE m.join_date >= DATE '2026-01-01';
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. All bookings for James Chen's classes (3 tables)

    Show `booking_id`, `class_name`, and `trainer_name` for every booking of a class taught by **James Chen**.

    Expected: 5 rows (Spin Cycle ×3, Strength Basics ×2).
    """)
    return


@app.cell
def _(bookings, classes, mo, trainers):
    q9 = mo.sql(
        f"""
        SELECT b.booking_id, c.class_name, t.trainer_name
        FROM bookings b
        INNER JOIN classes  c ON b.class_id   = c.class_id
        INNER JOIN trainers t ON c.trainer_id = t.trainer_id
        WHERE t.trainer_name = 'James Chen';
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. Which class did the unknown member book?

    Find bookings whose member does **not** exist in `members`. Show `booking_id`, `member_id`, and the `class_name` they booked.

    Expected: 1 row — booking 1015, member 12, Pilates Core.
    """)
    return


@app.cell
def _(bookings, classes, members, mo):
    q10 = mo.sql(
        f"""
        SELECT b.booking_id, b.member_id, c.class_name
        FROM bookings b
        LEFT JOIN members m ON b.member_id = m.member_id
        INNER JOIN classes c ON b.class_id = c.class_id
        WHERE m.member_id IS NULL;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. 🐞 Debug it



    Broken query:

    ```sql
    SELECT m.member_name
    FROM members m
    INNER JOIN bookings b ON m.member_id = b.member_id
    WHERE b.booking_id IS NULL;
    ```

    **The bug:** `INNER JOIN` keeps only members **with** a matching booking, so `b.booking_id` is never `NULL` after it. The `IS NULL` test can never be true → always 0 rows, no error.

    **The fix:** `LEFT JOIN`. The anti-join needs the unmatched rows, and only `LEFT JOIN` keeps them.

    Expected after the fix: 2 rows (Ava, Ben).
    """)
    return


@app.cell
def _(bookings, members, mo):
    q11 = mo.sql(
        f"""
        SELECT m.member_name
        FROM members m
        LEFT JOIN bookings b ON m.member_id = b.member_id
        WHERE b.booking_id IS NULL;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional — only if you finish early)

    Which classes were **never** booked by a member from **Santa Clara**? Show `class_name`, in alphabetical order. *Hint:* you need two `LEFT JOIN`s, a condition in `ON`, and `HAVING`.

    Expected: Aqua Fitness, Boxing Fit, Senior Stretch, Strength Basics. (Santa Clara members 1, 3, 7 booked only Morning Yoga, Spin Cycle, HIIT Bootcamp, Pilates Core.)
    """)
    return


@app.cell
def _(bookings, classes, members, mo):
    q12 = mo.sql(
        f"""
        SELECT c.class_name
        FROM classes c
        LEFT JOIN bookings b ON c.class_id = b.class_id
        LEFT JOIN members  m ON b.member_id = m.member_id
                            AND m.city = 'Santa Clara'
        GROUP BY c.class_name
        HAVING COUNT(m.member_id) = 0
        ORDER BY c.class_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## ✅ Exit Ticket — before you submit

    (Instructor copy — read a few out loud, anonymously, next class.)
    """)
    return


@app.cell
def _():
    exit_ticket = """
    1. One thing that clicked for you today:


    2. One thing about JOINs/NULLs that is still fuzzy or confusing:


    """
    return


if __name__ == "__main__":
    app.run()
