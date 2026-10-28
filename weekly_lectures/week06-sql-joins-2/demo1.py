import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from pathlib import Path

    import duckdb

    DATA_DIR = Path(__file__).parent / "data"
    con = duckdb.connect(database=":memory:")
    for _t in ["members", "bookings", "classes", "trainers"]:
        con.execute(
            f"CREATE OR REPLACE TABLE {_t} AS "
            f"SELECT * FROM read_csv('{DATA_DIR}/{_t}.csv')"
        )
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 6 — Joins II, Session 1: LEFT, RIGHT, and Finding What Is Missing

    **OMIS 105 — Introduction to Database Management Systems**

    This notebook follows `slides_1.md`. Run the cells from top to bottom.
    Every database cell takes `con`, the DuckDB connection made in the setup
    cell. The setup cell loads four CSV files from `data/`.

    | Table | Rows | One row is… |
    |---|---|---|
    | `members` | 10 | a gym member |
    | `bookings` | 16 | one member booking one class |
    | `classes` | 8 | a class (yoga, spin, …) |
    | `trainers` | 6 | a trainer |

    **The data has gaps on purpose:**

    - Ava Martinez and Ben Taylor **never booked** a class
    - Booking 1015 belongs to member 12, who **does not exist**
    - Aqua Fitness was **never booked**
    - Senior Stretch has **no trainer** yet
    - Maria Lopez and Noah Kim **teach no class**

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Look at the Data First

    Always look at your tables before you join them. Find the gaps by eye:
    which `member_id` values in `bookings` are **not** in `members`?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM members
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM bookings
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. `INNER JOIN` — Only Matches

    Ava and Ben have no bookings, and booking 1015 has no member. Count the
    rows: are they here?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, b.booking_id, b.class_id
        FROM members AS m
        INNER JOIN bookings AS b
            ON m.member_id = b.member_id
        ORDER BY b.booking_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **15 rows.** Ava, Ben, and booking 1015 are all **gone**.

    ---
    ## 3. `LEFT JOIN` — Every Member

    The left table is `members` (after `FROM`). Every member is kept. Scroll
    to member 7 and 8: their booking columns are `NULL`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, b.booking_id, b.class_id
        FROM members AS m
        LEFT JOIN bookings AS b
            ON m.member_id = b.member_id
        ORDER BY m.member_id, b.booking_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **17 rows** = 15 matches + Ava + Ben.

    ---
    ## 4. `RIGHT JOIN` — Every Booking

    The right table is `bookings` (after `JOIN`). Booking 1015 is kept, with
    a `NULL` member name.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, b.booking_id, b.class_id
        FROM members AS m
        RIGHT JOIN bookings AS b
            ON m.member_id = b.member_id
        ORDER BY b.booking_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **16 rows** = 15 matches + booking 1015.

    ### `RIGHT JOIN` = `LEFT JOIN` with the tables swapped

    Same 16 rows. Most analysts only write `LEFT JOIN`: start from the table
    you want to keep.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, b.booking_id, b.class_id
        FROM bookings AS b
        LEFT JOIN members AS m
            ON m.member_id = b.member_id
        ORDER BY b.booking_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. Try It: The Join Switcher 🔀

    Pick a join type. The SQL, the row count, and the result update.
    Watch which rows appear and disappear.
    """)
    return


@app.cell
def _(mo):
    join_type = mo.ui.dropdown(
        options=["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"],
        value="INNER JOIN",
        label="Join type:",
    )
    join_type
    return (join_type,)


@app.cell
def _(con, join_type, mo):
    _sql = f"""SELECT m.member_id, m.member_name, b.booking_id, b.member_id AS b_member_id
    FROM members AS m
    {join_type.value} bookings AS b
        ON m.member_id = b.member_id
    ORDER BY b.booking_id, m.member_id"""
    _df = con.execute(_sql).fetchdf()
    _why = {
        "INNER JOIN": "15 matches only. Ava, Ben, and booking 1015 are dropped.",
        "LEFT JOIN": "15 matches + Ava + Ben (every member).",
        "RIGHT JOIN": "15 matches + booking 1015 (every booking).",
        "FULL OUTER JOIN": "15 matches + Ava + Ben + booking 1015 (everything).",
    }[join_type.value]
    mo.vstack([
        mo.md(f"```sql\n{_sql}\n```"),
        mo.md(f"### {len(_df)} rows — {_why}"),
        _df,
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6. Finding What Is Missing (Anti-Join)

    Recipe:

    1. Start `FROM` the table you want to check
    2. `LEFT JOIN` the table where a partner *should* be
    3. Keep rows with **no** partner: `WHERE right_key IS NULL`

    ### Members who never booked a class
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_id, m.member_name, m.city
        FROM members AS m
        LEFT JOIN bookings AS b
            ON m.member_id = b.member_id
        WHERE b.booking_id IS NULL
        ORDER BY m.member_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bookings with an unknown member (a data quality check)
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT b.booking_id, b.member_id, b.class_id
        FROM bookings AS b
        LEFT JOIN members AS m
            ON m.member_id = b.member_id
        WHERE m.member_id IS NULL
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Classes nobody booked
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.class_id, c.class_name
        FROM classes AS c
        LEFT JOIN bookings AS b
            ON c.class_id = b.class_id
        WHERE b.booking_id IS NULL
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7. `COALESCE` — A Friendly Value Instead of `NULL`

    `COALESCE(a, b)` returns `a`, or `b` when `a` is `NULL`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.class_name,
               COALESCE(t.trainer_name, '(not assigned)') AS trainer
        FROM classes AS c
        LEFT JOIN trainers AS t
            ON c.trainer_id = t.trainer_id
        ORDER BY c.class_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8. The `ON` vs. `WHERE` Trap ⚠️

    **Question:** "Show **every** member, with their bookings made on or
    after September 10."

    ### Wrong: the filter is in `WHERE`
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, b.booking_id, b.booking_date
        FROM members AS m
        LEFT JOIN bookings AS b
            ON m.member_id = b.member_id
        WHERE b.booking_date >= DATE '2026-09-10'
        ORDER BY m.member_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Only **5 rows**. The `WHERE` runs **after** the join. For members with no
    late booking, `booking_date` is `NULL` or too early, so `WHERE` removes
    them. The `LEFT JOIN` quietly became an `INNER JOIN`.

    ### Right: the filter is in `ON`
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, b.booking_id, b.booking_date
        FROM members AS m
        LEFT JOIN bookings AS b
            ON m.member_id = b.member_id
           AND b.booking_date >= DATE '2026-09-10'
        ORDER BY m.member_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **10 rows** — every member is kept.

    | You want to filter… | Put the condition in… |
    |---|---|
    | the **left** table (the one you keep) | `WHERE` |
    | the **right** table (the optional one) | `ON ... AND ...` |
    | to find rows with **no** match | `WHERE right_key IS NULL` |

    ---
    ## 9. A Real Error: Ambiguous Column Name

    Both tables have a `member_id` column. If you do not say **which one**,
    DuckDB stops with an error. This cell runs the broken query and shows
    the real message.
    """)
    return


@app.cell(hide_code=True)
def _(mo, con):
    _bad = """SELECT member_id, member_name, booking_id
    FROM members AS m
    INNER JOIN bookings AS b
        ON m.member_id = b.member_id"""
    try:
        con.execute(_bad).fetchdf()
        _msg = "No error?!"
    except Exception as _e:
        _msg = str(_e)
    mo.md(f"""
    ```sql
    {_bad}
    ```

    **DuckDB says:**

    ```
    {_msg}
    ```

    **Fix:** write `m.member_id` (or `b.member_id`).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    - `INNER JOIN` → matches only (15 rows)
    - `LEFT JOIN` → all left rows (17 rows)
    - `RIGHT JOIN` → all right rows (16 rows)
    - `A RIGHT JOIN B` = `B LEFT JOIN A`
    - Anti-join: `LEFT JOIN ... WHERE right_key IS NULL`
    - `COALESCE` turns `NULL` into a friendly value
    - Filter the optional (right) table in `ON`, not in `WHERE`

    **Next:** `demo2.py` — counting with joins, 3+ tables, and self-joins.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
