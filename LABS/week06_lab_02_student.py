import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 06: Joins II
    ## Lab 2 — Joins at Work: Counting, Chains & Self-Joins · Student

    Work with the **Valley Fitness** gym database (members, bookings, classes, trainers). It is the same data as this week's demos. Run the setup cells first, then write your SQL in each question cell (replace `-- YOUR SQL HERE`).

    The data has gaps on purpose:

    - Ava Martinez and Ben Taylor never booked a class
    - Booking 1015 belongs to member 12, who does not exist
    - Aqua Fitness was never booked; Senior Stretch has no trainer
    - Maria Lopez and Noah Kim teach no class

    Today: a prediction, two explain-its, a bug to fix, and an optional bonus.
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

    🔮 **Predict first:** how many rows? And what number will Aqua Fitness (never booked) show if you count correctly?
    """)
    return


@app.cell
def _(mo):
    q1 = mo.sql(
        """
        -- Predict: ___ rows
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. How many different classes did each member try?

    For every member, show `member_name` and the number of **different** classes they booked as `different_classes`. Members with no bookings show 0. Order by `different_classes` (highest first), then `member_name`.
    """)
    return


@app.cell
def _(mo):
    q2 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. Total spent per member (3 tables)

    For every member, show `member_name` and the total price of all classes they booked as `total_spent`. Members with no bookings must show **0**, not `NULL`. Order by `total_spent` (highest first), then `member_name`.

    ✍️ **Explain it:** without `COALESCE`, Ava's total is `NULL`, but in Q1 Aqua Fitness's count was `0`. Why do `SUM` and `COUNT` disagree?
    """)
    return


@app.cell
def _(mo):
    q3 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. How many different members did each trainer teach? (4 tables)

    For **every** trainer, show `trainer_name` and the number of different members who booked one of their classes, as `members_taught`. Trainers with no classes show 0. Order by `members_taught` (highest first), then `trainer_name`.
    """)
    return


@app.cell
def _(mo):
    q4 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Who reports to James Chen? (self-join)

    Use the `trainers` table twice to show the `trainer_name` of every trainer whose manager is **James Chen**.
    """)
    return


@app.cell
def _(mo):
    q5 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. Co-workers with the same manager (self-join)

    Show every **pair** of trainers who have the **same manager**, as `trainer_1` and `trainer_2`. Each pair should appear **once** (not A–B and B–A), and no trainer should be paired with themselves.
    """)
    return


@app.cell
def _(mo):
    q6 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. Each class, its trainer, and the trainer's manager

    For **every** class, show `class_name`, the trainer's name as `trainer`, and the trainer's manager as `trainers_manager`. Show `'(none)'` where there is no one. *Hint:* join `trainers` twice.
    """)
    return


@app.cell
def _(mo):
    q7 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. All the gaps between classes and trainers (`FULL OUTER JOIN`)

    With **one** query, show the classes with no trainer **and** the trainers with no class. Show `class_name` and `trainer_name`.
    """)
    return


@app.cell
def _(mo):
    q8 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Revenue per trainer

    For **every** trainer, show `trainer_name` and the money their classes earned as `revenue` (one class price per booking). Trainers with no bookings show 0. Order by `revenue` (highest first), then `trainer_name`.

    ✍️ **Explain it:** a classmate used `COALESCE(SUM(c.price), 0)` and got **52** for Emma Wilson. Check her classes and bookings by hand. What is the right number, and where did the extra money come from?
    """)
    return


@app.cell
def _(mo):
    q9 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. Report: bookings per city and class

    Show `city`, `class_name`, and the number of bookings as `bookings`, for every city/class pair that has at least one booking. Order by `city`, then `bookings` (highest first), then `class_name`.
    """)
    return


@app.cell
def _(mo):
    q10 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. 🐞 Debug it



    This query should show how many bookings each member has, **including zero**:

    ```sql
    SELECT m.member_name, COUNT(*) AS bookings
    FROM members m
    LEFT JOIN bookings b ON m.member_id = b.member_id
    GROUP BY m.member_name
    ORDER BY bookings, m.member_name;
    ```

    It runs with no error — but Ava and Ben show **1** booking each, and they never booked anything. Fix it.
    """)
    return


@app.cell
def _(mo):
    q11 = mo.sql(
        """
        -- YOUR SQL HERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional — only if you finish early)

    Which members booked classes from **at least 2 different trainers**? Show `member_name` and the number of trainers as `trainers`. Order by `trainers` (highest first), then `member_name`.
    """)
    return


@app.cell
def _(mo):
    q12 = mo.sql(
        """
        -- YOUR SQL HERE (bonus)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## ✅ Exit Ticket — before you submit
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
