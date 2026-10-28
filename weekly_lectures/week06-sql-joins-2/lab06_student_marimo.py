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
    # Lab 6: Joins II — `INNER`, `LEFT`, and `RIGHT JOIN` in Practice

    ## OMIS 105 — Database Management Systems
    **Week 6 | Estimated time: 75–90 minutes | 10 questions × 3 points = 30 points**

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
        -- Your query here
        SELECT 'Q1: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2. Every class.** Same as Q1, but keep **every class**, even one with no trainer. Order by `class_name`. Which class shows `NULL`, and why?

    *Expected: 8 rows.*

    *(Write your answer here.)*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        -- Your query here
        SELECT 'Q2: replace this query' AS todo
        """
    ).fetchdf()
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
        -- Your query here
        SELECT 'Q3: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4. Same answer, with `LEFT JOIN`.** Rewrite Q3 so it uses `LEFT JOIN` instead of `RIGHT JOIN`. Your result must be exactly the same as Q3. In one sentence: what did you change?

    *Expected: 9 rows.*

    *(Write your answer here.)*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        -- Your query here
        SELECT 'Q4: replace this query' AS todo
        """
    ).fetchdf()
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
        -- Your query here
        SELECT 'Q5: replace this query' AS todo
        """
    ).fetchdf()
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
        -- Your query here
        SELECT 'Q6: replace this query' AS todo
        """
    ).fetchdf()
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

    *(Write your answer here.)*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        -- Your query here
        SELECT 'Q7: replace this query' AS todo
        """
    ).fetchdf()
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
        -- Your query here
        SELECT 'Q8: replace this query' AS todo
        """
    ).fetchdf()
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
        -- Your query here
        SELECT 'Q9: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10. The `ON` vs. `WHERE` trap.** For **every** class, count its bookings made **on or after** `2026-09-10`, as `late_bookings`. Classes with no late booking must show **0**. Order by `late_bookings` (highest first), then `class_name`. *Hint:* where does the date filter go?

    *Expected: 8 rows.*

    *(Write your answer here.)*
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        -- Your query here
        SELECT 'Q10: replace this query' AS todo
        """
    ).fetchdf()
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
