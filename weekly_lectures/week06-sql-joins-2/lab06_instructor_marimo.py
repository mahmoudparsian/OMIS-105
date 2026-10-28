import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 6: Joins II — `INNER`, `LEFT`, and `RIGHT JOIN` in Practice — INSTRUCTOR SOLUTIONS

    ## OMIS 105 — Database Management Systems
    **Week 6 | Answer Key | 10 questions × 3 points = 30 points**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Run the next two cells first. They connect to DuckDB and load `members`, `bookings`, `classes`, `trainers`
    from this folder's `data/` directory — the same data as the demos.

    **Rules for every query:** give every table an alias and use it on every
    column; list the columns you need (no `SELECT *`); use the `ORDER BY` given
    in the question. The **expected row count** is given for each question —
    if yours is different, look again at your query.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import duckdb

    DATA_DIR = Path(__file__).parent / "data"
    con = duckdb.connect(database=":memory:")
    return DATA_DIR, con


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"CREATE OR REPLACE TABLE members AS SELECT * FROM read_csv('{DATA_DIR}/members.csv')"
    )
    con.execute(
        f"CREATE OR REPLACE TABLE bookings AS SELECT * FROM read_csv('{DATA_DIR}/bookings.csv')"
    )
    con.execute(
        f"CREATE OR REPLACE TABLE classes AS SELECT * FROM read_csv('{DATA_DIR}/classes.csv')"
    )
    con.execute(
        f"CREATE OR REPLACE TABLE trainers AS SELECT * FROM read_csv('{DATA_DIR}/trainers.csv')"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: The Three Join Types (12 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1. Classes with their trainer.** Show `class_name` and `trainer_name` for classes that **have** a trainer. Use `INNER JOIN`. Order by `class_name`.

    *Expected: 7 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT c.class_name, t.trainer_name
        FROM classes AS c
        INNER JOIN trainers AS t
            ON c.trainer_id = t.trainer_id
        ORDER BY c.class_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | class_name | trainer_name |
    |---|---|
    | Aqua Fitness | Emma Wilson |
    | Boxing Fit | Diego Santos |
    | HIIT Bootcamp | Diego Santos |
    | Morning Yoga | Aisha Khan |
    | Pilates Core | Emma Wilson |
    | Spin Cycle | James Chen |
    | Strength Basics | James Chen |

    **Why:** Senior Stretch has `trainer_id = NULL`, so `INNER JOIN` drops it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2. Every class.** Same as Q1, but keep **every class**, even one with no trainer. Order by `class_name`. Which class shows `NULL`, and why?

    *Expected: 8 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT c.class_name, t.trainer_name
        FROM classes AS c
        LEFT JOIN trainers AS t
            ON c.trainer_id = t.trainer_id
        ORDER BY c.class_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | class_name | trainer_name |
    |---|---|
    | Aqua Fitness | Emma Wilson |
    | Boxing Fit | Diego Santos |
    | HIIT Bootcamp | Diego Santos |
    | Morning Yoga | Aisha Khan |
    | Pilates Core | Emma Wilson |
    | Senior Stretch | NULL |
    | Spin Cycle | James Chen |
    | Strength Basics | James Chen |

    **Why:** Senior Stretch is kept with `trainer_name = NULL`: it has no trainer yet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3. Every trainer, with `RIGHT JOIN`.** Write `FROM classes AS c RIGHT JOIN trainers AS t`. Show `trainer_name` and `class_name`, and keep **every trainer**. Order by `trainer_name`, then `class_name`.

    *Expected: 9 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT t.trainer_name, c.class_name
        FROM classes AS c
        RIGHT JOIN trainers AS t
            ON c.trainer_id = t.trainer_id
        ORDER BY t.trainer_name, c.class_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | trainer_name | class_name |
    |---|---|
    | Aisha Khan | Morning Yoga |
    | Diego Santos | Boxing Fit |
    | Diego Santos | HIIT Bootcamp |
    | Emma Wilson | Aqua Fitness |
    | Emma Wilson | Pilates Core |
    | James Chen | Spin Cycle |
    | James Chen | Strength Basics |
    | Maria Lopez | NULL |
    | Noah Kim | NULL |

    **Why:** Maria Lopez and Noah Kim teach no class, so `class_name` is `NULL`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4. Same answer, with `LEFT JOIN`.** Rewrite Q3 so it uses `LEFT JOIN` instead of `RIGHT JOIN`. Your result must be exactly the same as Q3. In one sentence: what did you change?

    *Expected: 9 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT t.trainer_name, c.class_name
        FROM trainers AS t
        LEFT JOIN classes AS c
            ON c.trainer_id = t.trainer_id
        ORDER BY t.trainer_name, c.class_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | trainer_name | class_name |
    |---|---|
    | Aisha Khan | Morning Yoga |
    | Diego Santos | Boxing Fit |
    | Diego Santos | HIIT Bootcamp |
    | Emma Wilson | Aqua Fitness |
    | Emma Wilson | Pilates Core |
    | James Chen | Spin Cycle |
    | James Chen | Strength Basics |
    | Maria Lopez | NULL |
    | Noah Kim | NULL |

    **Why:** Swap the two tables: `trainers LEFT JOIN classes`. `A RIGHT JOIN B` = `B LEFT JOIN A`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Finding What Is Missing (6 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5. Trainers who teach no class.** Show `trainer_id` and `trainer_name`. Use `LEFT JOIN` and `IS NULL`. Order by `trainer_id`.

    *Expected: 2 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT t.trainer_id, t.trainer_name
        FROM trainers AS t
        LEFT JOIN classes AS c
            ON t.trainer_id = c.trainer_id
        WHERE c.class_id IS NULL
        ORDER BY t.trainer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | trainer_id | trainer_name |
    |---|---|
    | 1 | Maria Lopez |
    | 6 | Noah Kim |

    **Why:** Test the key of the right table (`c.class_id`), which is never `NULL` in a real row.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6. Members who never booked.** Show `member_name` and `city` for members with **no** bookings. Order by `member_name`. Marketing will send them a free-class coupon.

    *Expected: 2 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT m.member_name, m.city
        FROM members AS m
        LEFT JOIN bookings AS b
            ON m.member_id = b.member_id
        WHERE b.booking_id IS NULL
        ORDER BY m.member_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | member_name | city |
    |---|---|
    | Ava Martinez | Santa Clara |
    | Ben Taylor | Sunnyvale |

    **Why:** Common mistake: `INNER JOIN` here returns 0 rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Joins at Work (12 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7. Classes per trainer, including zero.** For **every** trainer, show `trainer_name` and the number of classes they teach as `classes`. Trainers with no class must show **0**. Order by `classes` (highest first), then `trainer_name`. *Hint:* `COUNT(*)` gives the wrong answer here. Why?

    *Expected: 6 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT t.trainer_name, COUNT(c.class_id) AS classes
        FROM trainers AS t
        LEFT JOIN classes AS c
            ON t.trainer_id = c.trainer_id
        GROUP BY t.trainer_name
        ORDER BY classes DESC, t.trainer_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | trainer_name | classes |
    |---|---|
    | Diego Santos | 2 |
    | Emma Wilson | 2 |
    | James Chen | 2 |
    | Aisha Khan | 1 |
    | Maria Lopez | 0 |
    | Noah Kim | 0 |

    **Why:** `COUNT(*)` gives 1 to Maria and Noah: after the `LEFT JOIN` each still has one row. `COUNT(c.class_id)` skips `NULL`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8. Who booked Morning Yoga?** Join **three** tables (`members`, `bookings`, `classes`). Show `member_name` and `booking_date` for every booking of `'Morning Yoga'`. Order by `booking_date`.

    *Expected: 4 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT m.member_name, b.booking_date
        FROM members AS m
        INNER JOIN bookings AS b
            ON m.member_id = b.member_id
        INNER JOIN classes AS c
            ON b.class_id = c.class_id
        WHERE c.class_name = 'Morning Yoga'
        ORDER BY b.booking_date
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | member_name | booking_date |
    |---|---|
    | Olivia Brown | 2026-09-01 |
    | Sophia Nguyen | 2026-09-02 |
    | Chloe Davis | 2026-09-09 |
    | Ethan Patel | 2026-09-15 |

    **Why:** Two `INNER JOIN`s are right here: we only want real bookings of a real class.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9. Trainer and manager (self-join).** Show every trainer as `trainer` and their manager's name as `manager`. The trainer with no manager must show `'(no manager)'`. Use the `trainers` table twice. Order by `trainer`.

    *Expected: 6 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT e.trainer_name AS trainer,
               COALESCE(m.trainer_name, '(no manager)') AS manager
        FROM trainers AS e
        LEFT JOIN trainers AS m
            ON e.manager_id = m.trainer_id
        ORDER BY e.trainer_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | trainer | manager |
    |---|---|
    | Aisha Khan | Maria Lopez |
    | Diego Santos | James Chen |
    | Emma Wilson | James Chen |
    | James Chen | Maria Lopez |
    | Maria Lopez | (no manager) |
    | Noah Kim | Aisha Khan |

    **Why:** With `INNER JOIN`, Maria Lopez (the head trainer) would be missing: 5 rows instead of 6.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10. The `ON` vs. `WHERE` trap.** For **every** class, count its bookings made **on or after** `2026-09-10`, as `late_bookings`. Classes with no late booking must show **0**. Order by `late_bookings` (highest first), then `class_name`. *Hint:* where does the date filter go?

    *Expected: 8 rows.*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        SELECT c.class_name, COUNT(b.booking_id) AS late_bookings
        FROM classes AS c
        LEFT JOIN bookings AS b
            ON c.class_id = b.class_id
           AND b.booking_date >= DATE '2026-09-10'
        GROUP BY c.class_name
        ORDER BY late_bookings DESC, c.class_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Expected result:**

    | class_name | late_bookings |
    |---|---|
    | HIIT Bootcamp | 1 |
    | Morning Yoga | 1 |
    | Pilates Core | 1 |
    | Senior Stretch | 1 |
    | Spin Cycle | 1 |
    | Strength Basics | 1 |
    | Aqua Fitness | 0 |
    | Boxing Fit | 0 |

    **Why:** If the date filter is in `WHERE`, Aqua Fitness and Boxing Fit disappear (6 rows instead of 8). The filter is on the optional (right) table, so it belongs in `ON`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Grading

    - 3 points per question: 2 for a correct result, 1 for a clean query
      (and, where asked, the short written answer)
    - **Total: 30 points**

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
