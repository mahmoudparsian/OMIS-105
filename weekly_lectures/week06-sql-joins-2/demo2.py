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


@app.cell
def _():
    import matplotlib.pyplot as plt

    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 6 — Joins II, Session 2: Joins at Work

    **OMIS 105 — Introduction to Database Management Systems**

    This notebook follows `slides_2.md`. Same Valley Fitness data as
    `demo1.py`: `members`, `bookings`, `classes`, `trainers`.

    | Part | You will learn |
    |---|---|
    | 1 | Counting with `LEFT JOIN` + `GROUP BY` — including zero |
    | 2 | Joining 3 and 4 tables |
    | 3 | Self-joins: a table joined to itself |
    | 4 | A quick look at `FULL OUTER JOIN` |

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Counting with `LEFT JOIN` — Including Zero

    **Question:** How many bookings does each member have — including members
    with none?

    ### Attempt 1: `COUNT(*)` ❌
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, COUNT(*) AS bookings
        FROM members AS m
        LEFT JOIN bookings AS b
            ON m.member_id = b.member_id
        GROUP BY m.member_name
        ORDER BY bookings, m.member_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ava and Ben show **1**. But they never booked! After the `LEFT JOIN`,
    each of them still has **one row** (with `NULL` booking columns), and
    `COUNT(*)` counts rows.

    ### Attempt 2: `COUNT(b.booking_id)` ✅

    `COUNT(column)` skips `NULL` values.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, COUNT(b.booking_id) AS bookings
        FROM members AS m
        LEFT JOIN bookings AS b
            ON m.member_id = b.member_id
        GROUP BY m.member_name
        ORDER BY bookings, m.member_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Revenue per class, including classes nobody booked
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.class_name,
               c.price,
               COUNT(b.booking_id)           AS bookings,
               COUNT(b.booking_id) * c.price AS revenue
        FROM classes AS c
        LEFT JOIN bookings AS b
            ON c.class_id = b.class_id
        GROUP BY c.class_name, c.price
        ORDER BY revenue DESC, c.class_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(con, plt):
    _df = con.execute("""
        SELECT c.class_name, COUNT(b.booking_id) * c.price AS revenue
        FROM classes AS c
        LEFT JOIN bookings AS b ON c.class_id = b.class_id
        GROUP BY c.class_name, c.price
        ORDER BY revenue
    """).fetchdf()
    _fig, _ax = plt.subplots(figsize=(7, 3.5))
    _colors = ["#d62728" if v == 0 else "#1f77b4" for v in _df["revenue"]]
    _ax.barh(_df["class_name"], _df["revenue"], color=_colors)
    _ax.set_xlabel("Revenue ($)")
    _ax.set_title("Revenue per class (red = never booked)")
    plt.tight_layout()
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Aqua Fitness shows **$0**. With an `INNER JOIN`, it would not be in the
    chart at all — and nobody would ask why it earns nothing.

    ---
    ## 2. Joining 3 and 4 Tables

    Add one `JOIN ... ON` per table. Read it top to bottom:
    members → their bookings → the class of each booking.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, c.class_name, b.booking_date
        FROM members AS m
        INNER JOIN bookings AS b
            ON m.member_id = b.member_id
        INNER JOIN classes AS c
            ON b.class_id = c.class_id
        ORDER BY b.booking_date, m.member_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Add the trainer — all `INNER JOIN`
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, c.class_name, t.trainer_name
        FROM members AS m
        INNER JOIN bookings AS b ON m.member_id = b.member_id
        INNER JOIN classes  AS c ON b.class_id  = c.class_id
        INNER JOIN trainers AS t ON c.trainer_id = t.trainer_id
        ORDER BY m.member_name, c.class_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **14 rows** — one booking is missing! Chloe booked **Senior Stretch**,
    which has no trainer. The last `INNER JOIN` found no partner and
    dropped the row.

    ### Fix: `LEFT JOIN` the optional table
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, c.class_name,
               COALESCE(t.trainer_name, '(not assigned)') AS trainer
        FROM members AS m
        INNER JOIN bookings AS b ON m.member_id = b.member_id
        INNER JOIN classes  AS c ON b.class_id  = c.class_id
        LEFT  JOIN trainers AS t ON c.trainer_id = t.trainer_id
        ORDER BY m.member_name, c.class_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **15 rows.** Rule: use `INNER JOIN` when a partner **must** exist, and
    `LEFT JOIN` when it is **optional**.

    ### Trainer workload (3 tables + `GROUP BY`)

    `COUNT(DISTINCT c.class_id)`: after joining bookings, a class appears
    once per booking. `DISTINCT` counts each class once.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT t.trainer_name,
               COUNT(DISTINCT c.class_id) AS classes,
               COUNT(b.booking_id)        AS bookings
        FROM trainers AS t
        LEFT JOIN classes  AS c ON t.trainer_id = c.trainer_id
        LEFT JOIN bookings AS b ON c.class_id   = b.class_id
        GROUP BY t.trainer_name
        ORDER BY bookings DESC, t.trainer_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. Self-Join: A Table Joined to Itself

    `trainers.manager_id` points to **another trainer**. Use the table twice
    with two aliases: `e` (the employee) and `m` (the manager).
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *
        FROM trainers
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `INNER JOIN` — the head trainer disappears
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.trainer_name AS trainer,
               m.trainer_name AS manager
        FROM trainers AS e
        INNER JOIN trainers AS m
            ON e.manager_id = m.trainer_id
        ORDER BY e.trainer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `LEFT JOIN` — everyone is kept ✅
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT e.trainer_name AS trainer,
               COALESCE(m.trainer_name, '(head trainer)') AS manager
        FROM trainers AS e
        LEFT JOIN trainers AS m
            ON e.manager_id = m.trainer_id
        ORDER BY e.trainer_id
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The org chart, drawn from the self-join

    The chart below is **not a picture someone drew**. A Python cell runs the
    self-join above and turns each *manager → trainer* row into an arrow.
    """)
    return


@app.cell(hide_code=True)
def _(mo, con):
    _rows = con.execute("""
        SELECT m.trainer_name AS manager, e.trainer_name AS trainer
        FROM trainers AS e
        INNER JOIN trainers AS m
            ON e.manager_id = m.trainer_id
    """).fetchall()
    _ids = {}
    def _node(name):
        return _ids.setdefault(name, f"t{len(_ids)}")
    _lines = ["graph TD"]
    for _mgr, _emp in _rows:
        _lines.append(f'    {_node(_mgr)}["{_mgr}"] --> {_node(_emp)}["{_emp}"]')
    mo.mermaid("\n".join(_lines))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How many direct reports does each trainer have?
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.trainer_name AS manager,
               COUNT(e.trainer_id) AS direct_reports
        FROM trainers AS m
        LEFT JOIN trainers AS e
            ON e.manager_id = m.trainer_id
        GROUP BY m.trainer_name
        ORDER BY direct_reports DESC, manager
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Same counting rule as Part 1: `COUNT(e.trainer_id)`, not `COUNT(*)`.

    ---
    ## 4. A Quick Look: `FULL OUTER JOIN`

    `FULL OUTER JOIN` keeps every row from **both** sides — 18 rows here
    (15 matches + Ava + Ben + booking 1015). This query shows **only the gaps**:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.member_name, b.booking_id
        FROM members AS m
        FULL OUTER JOIN bookings AS b
            ON m.member_id = b.member_id
        WHERE m.member_id IS NULL
           OR b.booking_id IS NULL
        ORDER BY b.booking_id, m.member_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. Business Report: Activity by City

    `COUNT(DISTINCT m.member_id)`: a member with 3 bookings appears in 3
    rows, but is one member.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT m.city,
               COUNT(DISTINCT m.member_id) AS members,
               COUNT(b.booking_id)         AS bookings
        FROM members AS m
        LEFT JOIN bookings AS b
            ON m.member_id = b.member_id
        GROUP BY m.city
        ORDER BY bookings DESC, m.city
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Which Join Do I Need?

    | Business question | Join |
    |---|---|
    | "Show orders **with** their customer names" | `INNER JOIN` |
    | "Show **all** customers, with orders if any" | `LEFT JOIN` |
    | "Which customers **never** ordered?" | `LEFT JOIN ... WHERE right_key IS NULL` |
    | "Count orders per customer, **including 0**" | `LEFT JOIN` + `COUNT(right_key)` |
    | "Show each employee **and their manager**" | self-join |
    | "Show **every** gap on **both** sides" | `FULL OUTER JOIN` |

    **Next week:** Subqueries — a query inside a query.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
