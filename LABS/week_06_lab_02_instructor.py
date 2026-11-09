import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 06: Joins II
    ## Lab 2 — Joins at Work: Counting, Chains & Self-Joins · Instructor

    Work with the **Valley Fitness** gym database (members, bookings, classes, trainers). It is the same data as this week's demos. Run the setup cells first, then each question. Answers are filled in.

    The data has gaps on purpose:

    - Ava Martinez and Ben Taylor never booked a class
    - Booking 1015 belongs to member 12, who does not exist
    - Aqua Fitness was never booked; Senior Stretch has no trainer
    - Maria Lopez and Noah Kim teach no class

    See `week06_lab_02_design_notes.md` for Q4 and Q9 (the two numbers students will argue about).
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
    return (members,)


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
    return (bookings,)


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
    return (classes,)


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
    return (trainers,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q1. Bookings per class — including zero

    For **every** class, show `class_name` and its number of bookings as `bookings`. Order by `bookings` (highest first), then `class_name`.

    🔮 **Predict:** 8 rows; Aqua Fitness shows **0** with `COUNT(b.booking_id)` (`COUNT(*)` would show 1).
    """)
    return


@app.cell
def _(bookings, classes, mo):
    q1 = mo.sql(
        f"""
        -- Predict: 8 rows
        SELECT c.class_name, COUNT(b.booking_id) AS bookings
        FROM classes c
        LEFT JOIN bookings b ON c.class_id = b.class_id
        GROUP BY c.class_name
        ORDER BY bookings DESC, c.class_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. How many different classes did each member try?

    For every member, show `member_name` and the number of **different** classes they booked as `different_classes`. Members with no bookings show 0. Order by `different_classes` (highest first), then `member_name`.

    Expected: 10 rows. Olivia 3; Ava and Ben 0. Needs `COUNT(DISTINCT b.class_id)`.
    """)
    return


@app.cell
def _(bookings, members, mo):
    q2 = mo.sql(
        f"""
        SELECT m.member_name, COUNT(DISTINCT b.class_id) AS different_classes
        FROM members m
        LEFT JOIN bookings b ON m.member_id = b.member_id
        GROUP BY m.member_name
        ORDER BY different_classes DESC, m.member_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. Total spent per member (3 tables)

    For every member, show `member_name` and the total price of all classes they booked as `total_spent`. Members with no bookings must show **0**, not `NULL`. Order by `total_spent` (highest first), then `member_name`.

    ✍️ **Explain it (sample answer):** "`COUNT` counts rows — no matching rows means 0. `SUM` adds values — with no values there is nothing to add, so SQL returns `NULL`. `COALESCE(..., 0)` turns that `NULL` into 0."

    Expected: 10 rows; Olivia 60, Ava and Ben 0.
    """)
    return


@app.cell
def _(bookings, classes, members, mo):
    q3 = mo.sql(
        f"""
        SELECT m.member_name, COALESCE(SUM(c.price), 0) AS total_spent
        FROM members m
        LEFT JOIN bookings b ON m.member_id = b.member_id
        LEFT JOIN classes  c ON b.class_id  = c.class_id
        GROUP BY m.member_name
        ORDER BY total_spent DESC, m.member_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. How many different members did each trainer teach? (4 tables)

    For **every** trainer, show `trainer_name` and the number of different members who booked one of their classes, as `members_taught`. Trainers with no classes show 0. Order by `members_taught` (highest first), then `trainer_name`.

    Expected: 6 rows — James 5, Aisha 4, Diego 4, **Emma 1**, Maria 0, Noah 0.

    **Talking point:** Emma's Pilates Core has two bookings, but one is from member 12, who does not exist. `COUNT(DISTINCT m.member_id)` gives 1; `COUNT(DISTINCT b.member_id)` gives 2. Both are defensible — ask students which one a manager wants.
    """)
    return


@app.cell
def _(bookings, classes, members, mo, trainers):
    q4 = mo.sql(
        f"""
        SELECT t.trainer_name, COUNT(DISTINCT m.member_id) AS members_taught
        FROM trainers t
        LEFT JOIN classes  c ON t.trainer_id = c.trainer_id
        LEFT JOIN bookings b ON c.class_id   = b.class_id
        LEFT JOIN members  m ON b.member_id  = m.member_id
        GROUP BY t.trainer_name
        ORDER BY members_taught DESC, t.trainer_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Who reports to James Chen? (self-join)

    Use the `trainers` table twice to show the `trainer_name` of every trainer whose manager is **James Chen**.

    Expected: 2 rows — Diego Santos, Emma Wilson.
    """)
    return


@app.cell
def _(mo, trainers):
    q5 = mo.sql(
        f"""
        SELECT e.trainer_name
        FROM trainers e
        INNER JOIN trainers m ON e.manager_id = m.trainer_id
        WHERE m.trainer_name = 'James Chen';
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. Co-workers with the same manager (self-join)

    Show every **pair** of trainers who have the **same manager**, as `trainer_1` and `trainer_2`. Each pair should appear **once** (not A–B and B–A), and no trainer should be paired with themselves.

    Expected: 2 rows — (James Chen, Aisha Khan), (Diego Santos, Emma Wilson). The trick is `t1.trainer_id < t2.trainer_id` in `ON`.
    """)
    return


@app.cell
def _(mo, trainers):
    q6 = mo.sql(
        f"""
        SELECT t1.trainer_name AS trainer_1, t2.trainer_name AS trainer_2
        FROM trainers t1
        INNER JOIN trainers t2
            ON t1.manager_id = t2.manager_id
           AND t1.trainer_id < t2.trainer_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. Each class, its trainer, and the trainer's manager

    For **every** class, show `class_name`, the trainer's name as `trainer`, and the trainer's manager as `trainers_manager`. Show `'(none)'` where there is no one. *Hint:* join `trainers` twice.

    Expected: 8 rows. Senior Stretch shows `(none)` twice.
    """)
    return


@app.cell
def _(classes, mo, trainers):
    q7 = mo.sql(
        f"""
        SELECT c.class_name,
               COALESCE(t.trainer_name, '(none)') AS trainer,
               COALESCE(m.trainer_name, '(none)') AS trainers_manager
        FROM classes c
        LEFT JOIN trainers t ON c.trainer_id = t.trainer_id
        LEFT JOIN trainers m ON t.manager_id = m.trainer_id
        ORDER BY c.class_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. All the gaps between classes and trainers (`FULL OUTER JOIN`)

    With **one** query, show the classes with no trainer **and** the trainers with no class. Show `class_name` and `trainer_name`.

    Expected: 3 rows — Senior Stretch (no trainer), Maria Lopez and Noah Kim (no class).
    """)
    return


@app.cell
def _(classes, mo, trainers):
    q8 = mo.sql(
        f"""
        SELECT c.class_name, t.trainer_name
        FROM classes c
        FULL OUTER JOIN trainers t ON c.trainer_id = t.trainer_id
        WHERE c.class_id IS NULL
           OR t.trainer_id IS NULL;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Revenue per trainer

    For **every** trainer, show `trainer_name` and the money their classes earned as `revenue` (one class price per booking). Trainers with no bookings show 0. Order by `revenue` (highest first), then `trainer_name`.

    ✍️ **Explain it (sample answer):** "Emma teaches Pilates Core (2 bookings × 18 = 36) and Aqua Fitness (0 bookings). After the `LEFT JOIN`, Aqua Fitness still has one row with its price (16) and a `NULL` booking, so `SUM(c.price)` adds 16 for a class nobody booked: 36 + 16 = 52. Only add the price when a booking exists."

    The classmate's query:

    ```sql
    SELECT t.trainer_name, COALESCE(SUM(c.price), 0) AS revenue
    FROM trainers t
    LEFT JOIN classes  c ON t.trainer_id = c.trainer_id
    LEFT JOIN bookings b ON c.class_id   = b.class_id
    GROUP BY t.trainer_name
    ORDER BY revenue DESC, t.trainer_name;
    ```

    Expected: James 104, Diego 100, Aisha 60, Emma **36**, Maria 0, Noah 0.
    """)
    return


@app.cell
def _(bookings, classes, mo, trainers):
    q9 = mo.sql(
        f"""
        SELECT t.trainer_name,
               SUM(CASE WHEN b.booking_id IS NOT NULL THEN c.price ELSE 0 END) AS revenue
        FROM trainers t
        LEFT JOIN classes  c ON t.trainer_id = c.trainer_id
        LEFT JOIN bookings b ON c.class_id   = b.class_id
        GROUP BY t.trainer_name
        ORDER BY revenue DESC, t.trainer_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. Report: bookings per city and class

    Show `city`, `class_name`, and the number of bookings as `bookings`, for every city/class pair that has at least one booking. Order by `city`, then `bookings` (highest first), then `class_name`.

    Expected: 12 rows. Booking 1015 (unknown member) is not counted — it has no city.
    """)
    return


@app.cell
def _(bookings, classes, members, mo):
    q10 = mo.sql(
        f"""
        SELECT m.city, c.class_name, COUNT(*) AS bookings
        FROM members m
        INNER JOIN bookings b ON m.member_id = b.member_id
        INNER JOIN classes  c ON b.class_id  = c.class_id
        GROUP BY m.city, c.class_name
        ORDER BY m.city, bookings DESC, c.class_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. 🐞 Debug it



    Broken query:

    ```sql
    SELECT m.member_name, COUNT(*) AS bookings
    FROM members m
    LEFT JOIN bookings b ON m.member_id = b.member_id
    GROUP BY m.member_name
    ORDER BY bookings, m.member_name;
    ```

    **The bug:** after the `LEFT JOIN`, Ava still has **one row** (with `NULL` booking columns). `COUNT(*)` counts rows → 1.

    **The fix:** `COUNT(b.booking_id)` counts non-`NULL` values → 0.

    **Talking point:** this is the same idea as Q1 — tie them together out loud.
    """)
    return


@app.cell
def _(bookings, members, mo):
    q11 = mo.sql(
        f"""
        SELECT m.member_name, COUNT(b.booking_id) AS bookings
        FROM members m
        LEFT JOIN bookings b ON m.member_id = b.member_id
        GROUP BY m.member_name
        ORDER BY bookings, m.member_name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional — only if you finish early)

    Which members booked classes from **at least 2 different trainers**? Show `member_name` and the number of trainers as `trainers`. Order by `trainers` (highest first), then `member_name`.

    Expected: 5 rows — Olivia 3; Ethan, Liam, Mia, Sophia 2. (Chloe has 2 classes, but Senior Stretch has no trainer, and `COUNT(DISTINCT ...)` skips `NULL`.)
    """)
    return


@app.cell
def _(bookings, classes, members, mo, trainers):
    q12 = mo.sql(
        f"""
        SELECT m.member_name, COUNT(DISTINCT c.trainer_id) AS trainers
        FROM members m
        INNER JOIN bookings b ON m.member_id = b.member_id
        INNER JOIN classes  c ON b.class_id  = c.class_id
        GROUP BY m.member_name
        HAVING COUNT(DISTINCT c.trainer_id) >= 2
        ORDER BY trainers DESC, m.member_name;
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


    2. One thing about counting with joins or self-joins that is still fuzzy or confusing:


    """
    return (exit_ticket,)


if __name__ == "__main__":
    app.run()
