"""OMIS 105 -- Sailors & Boats, Level 1: ten basic queries (Marimo).

Run it with:
    ./run_notebook_level_01.sh

Ten queries using one table at a time: SELECT, WHERE, ORDER BY, LIMIT, DISTINCT
and a first GROUP BY. Levels 2-4 add joins, subqueries and window functions.

Every plot is drawn by a function in src/plots_level_01.py -- this notebook
contains no plotting code, only SQL.
"""

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium", app_title="Sailors & Boats -- Level 1")


@app.cell
def _():
    import sys
    from pathlib import Path

    import marimo as mo

    NOTEBOOK_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = NOTEBOOK_DIR.parent
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

    import plots_level_01 as plots
    import sailors_db as sdb

    # Read-only: notebooks explore, the Streamlit app writes.
    con = sdb.connect(read_only=True)

    def run(sql: str):
        """Execute a SELECT and return a DataFrame.

        Goes through sailors_db.q so DATE columns print as YYYY-MM-DD rather
        than as pandas timestamps with a spurious 00:00:00.
        """
        return sdb.q(con, sql)

    return mo, plots, run


@app.cell
def _(mo):
    mo.md(r"""
    # Level 1 -- ten basic queries

    Everything here touches **one table at a time**. That is the whole
    difficulty setting: no joins, no subqueries in the FROM clause, nothing
    that needs two ideas at once. What each query does have is a reason for
    every clause, and that is what to read for.

    | table | one row is... | key |
    |---|---|---|
    | `sailors` | one person | `sid` |
    | `boats` | one hull | `bid` |
    | `reserves` | one boat, on one day | `(bid, day)`, plus `UNIQUE (sid, day)` |

    **The data.** Fourteen sailors, nine boats, ten reservations, all in the
    autumn of 1998. Ten of the fourteen sailors have never reserved anything
    and five of the nine boats have never left the dock -- those rows are in
    the database on purpose, and from Level 2 onwards they are what makes
    outer joins worth learning.

    The rules the database enforces (R1-R10, P1-P3, D1-D2) are defined in one
    place, the `REQUIREMENTS` block at the top of `database/sql/01_schema.sql`. These
    notebooks cite the labels and never restate them.

    **The four levels**

    | notebook | what it adds |
    |---|---|
    | **Level 1** (this one) | one table at a time |
    | Level 2 | joins, `GROUP BY`, `HAVING`, subqueries |
    | Level 3 | set operations, anti-joins, `CASE`, ranking |
    | Level 4 | relational division, window functions, `PIVOT`, recursion |
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Q1. Sailors under the age of 40

    A `WHERE` clause is a filter on rows, and it runs before anything else you
    can see. `ORDER BY` then decides the order they come back in -- without it
    a database is free to hand rows over in whatever order it found them, and
    that order can change between runs.

    `age < 40` is a strict comparison: a sailor of exactly 40 is not under 40,
    and Horatio (74) is exactly that, so he is missing from the answer. Nearly
    every off-by-one in SQL is a `<` that should have been `<=`.
    """)
    return


@app.cell
def _(mo, run):
    q1 = run(
        """
        SELECT sid, sname, rating, age
        FROM sailors
        WHERE age < 40
        ORDER BY age, sid
        """
    )
    mo.ui.table(q1, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q2. Sailors with a rating above 7

    The same shape as Q1, on a column that is allowed to be **NULL**. Dan (99)
    has no rating at all, and he does not appear here -- not because his rating
    is low, but because `NULL > 7` is not false, it is *unknown*, and `WHERE`
    keeps only rows where the condition came out true.

    That is worth sitting with: `WHERE rating > 7` and `WHERE rating <= 7`
    between them do **not** cover the whole crew. Dan falls out of both. To ask
    about him you need `WHERE rating IS NULL`, which is a different kind of
    test -- `= NULL` never matches anything, not even another NULL.
    """)
    return


@app.cell
def _(mo, run):
    q2 = run(
        """
        SELECT sid, sname, rating, age
        FROM sailors
        WHERE rating > 7
        ORDER BY rating DESC, sname
        """
    )
    mo.ui.table(q2, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q3. The red boats

    String comparison is exact: `'red'` matches `'red'` and not `'Red'`. That
    is not a rule you have to remember here, because the schema will not let a
    boat be stored as `'Red'` in the first place -- the colour column carries a
    `CHECK` constraint (see D2 in the requirements block), and the app offers
    the same six colours from `sailors_db.VALID_COLORS`.

    Constraints do that quietly: they stop a whole class of query bug by
    making the bad value impossible to store.
    """)
    return


@app.cell
def _(mo, run):
    q3 = run(
        """
        SELECT bid, bname, color
        FROM boats
        WHERE color = 'red'
        ORDER BY bid
        """
    )
    mo.ui.table(q3, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q4. The red *and* the green boats

    Read the question carefully: it asks for boats that are red **or** green,
    because no boat is both. English "and" over a set of categories almost
    always means SQL `OR` -- `color = 'red' AND color = 'green'` is a condition
    no row can satisfy, and it returns nothing rather than an error.

    `IN ('red', 'green')` is the same test as two `OR`s, in half the space, and
    it stays readable when the list grows to five colours.
    """)
    return


@app.cell
def _(mo, run):
    q4 = run(
        """
        SELECT bid, bname, color
        FROM boats
        WHERE color IN ('red', 'green')
        ORDER BY color, bid
        """
    )
    mo.ui.table(q4, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q5. The youngest sailor

    Sort by age and keep the first row. `LIMIT 1` is the everyday way to ask
    for an extreme, and it works here -- Zorba at 16 is the only sailor that
    young.

    But notice what `LIMIT 1` actually promises: *one row*, not *the answer*.
    If two sailors tied for youngest it would still return one of them, chosen
    arbitrarily, and nothing in the output would hint that a second one
    existed. That trap is real in this data at the other end of the rating
    scale, where Rusty and Zorba both hold a 10 -- Q6 shows the form that
    survives a tie.
    """)
    return


@app.cell
def _(mo, run):
    q5 = run(
        """
        SELECT sid, sname, rating, age
        FROM sailors
        ORDER BY age
        LIMIT 1
        """
    )
    mo.ui.table(q5, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q6. The oldest sailor -- all of them

    `WHERE age = (SELECT max(age) FROM sailors)` asks a different question from
    `ORDER BY age DESC LIMIT 1`: it computes the maximum first, then returns
    **every** sailor holding it. One row today (Bob, 63.5), but two the moment
    somebody ties, and no edit to the query.

    The bracketed part is a *scalar subquery* -- a query used where a single
    value is expected. It runs once, produces one number, and the outer `WHERE`
    compares against it.

    Prefer this form whenever "the largest" is a question about the data rather
    than a request for one example.
    """)
    return


@app.cell
def _(mo, run):
    q6 = run(
        """
        SELECT sid, sname, rating, age
        FROM sailors
        WHERE age = (SELECT max(age) FROM sailors)
        ORDER BY sid
        """
    )
    mo.ui.table(q6, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q7. How many boats of each colour? *(chart)*

    The first `GROUP BY`. It collapses the nine boat rows into one row per
    colour, and every column in the `SELECT` then has to be either the thing
    you grouped by or an aggregate over the group -- there is no sensible
    single `bid` for the two blue boats, so asking for one is an error.

    `count(*)` counts rows in the group. `string_agg` is the aggregate that
    keeps the detail: instead of collapsing the names, it pastes them into one
    string, which is how a grouped answer can still show its working.
    """)
    return


@app.cell
def _(plots, run):
    q7 = run(
        """
        SELECT color,
               count(*) AS n_boats,
               string_agg(bname, ', ' ORDER BY bid) AS boats
        FROM boats
        GROUP BY color
        ORDER BY n_boats DESC, color
        """
    )
    plots.plot_boats_per_colour(q7)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q8. Counting, and the hole in the count

    Five aggregates over the whole table -- no `GROUP BY`, so the entire table
    is one group and the answer is one row.

    The pair to compare is `count(*)` and `count(rating)`. **`count(*)` counts
    rows; `count(rating)` counts non-NULL values in that column**, so the
    difference between them is exactly the number of unrated sailors. One:
    Dan.

    Every other aggregate here behaves the same way -- `avg(age)` divides by
    the number of ages it actually saw, not by the number of sailors. When a
    column can be NULL, an average is quietly an average *of the rows that had
    a value*, and it is worth saying so out loud when you report it.
    """)
    return


@app.cell
def _(mo, run):
    q8 = run(
        """
        SELECT count(*)                AS n_sailors,
               count(rating)           AS n_rated,
               count(*) - count(rating) AS n_unrated,
               min(age)                AS youngest,
               max(age)                AS oldest,
               round(avg(age), 2)      AS avg_age
        FROM sailors
        """
    )
    mo.ui.table(q8, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q9. The whole crew, oldest first *(chart)*

    No filter at all: every sailor, arranged. Sorting is not a cosmetic step --
    it is how a list of fourteen rows becomes an answer to "who is old and who
    is young", and the chart is the same `ORDER BY` drawn instead of printed.

    Watch where Dan lands. He has no rating, and `ORDER BY age DESC` says
    nothing about ratings, so he sorts purely on age. Had we sorted by `rating`
    instead, his NULL would go to one end of the list -- DuckDB puts NULLs last
    on an ascending sort -- and `NULLS FIRST` / `NULLS LAST` is how you say
    which end you meant.
    """)
    return


@app.cell
def _(plots, run):
    q9 = run(
        """
        SELECT sid, sname, age, rating
        FROM sailors
        ORDER BY age DESC, sid
        """
    )
    plots.plot_crew_by_age(q9)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q10. Everything that happened in the 1998 season *(chart)*

    `BETWEEN` is an inclusive range: `day BETWEEN '1998-09-01' AND '1998-11-30'`
    keeps both end dates. It is shorthand for `day >= ... AND day <= ...`, and
    the inclusiveness is the part people forget when a report double-counts the
    boundary day.

    Dates are a real type here, not strings -- `DATE '1998-09-01'` compares as a
    date, sorts as a date, and can be subtracted from another date to give a
    number of days. Level 3 leans on that.

    This is also the last query in the level that touches only one table. Every
    row below names a `bid` and a `sid` and nothing more; turning those numbers
    into a boat name and a sailor name is a **join**, which is where Level 2
    starts.
    """)
    return


@app.cell
def _(plots, run):
    q10 = run(
        """
        SELECT day, bid, sid
        FROM reserves
        WHERE day BETWEEN DATE '1998-09-01' AND DATE '1998-11-30'
        ORDER BY day, bid
        """
    )
    plots.plot_season_strip(q10)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ### What Level 1 covered

    | | query | the idea |
    |---|---|---|
    | Q1 | sailors under 40 | `WHERE`, and strict vs inclusive comparison |
    | Q2 | rating above 7 | NULL is *unknown*, not false |
    | Q3 | red boats | exact string match, guarded by a `CHECK` |
    | Q4 | red and green boats | English "and" over categories is SQL `OR` |
    | Q5 | the youngest sailor | `LIMIT 1` returns a row, not an answer |
    | Q6 | the oldest sailor(s) | scalar subquery, tie-safe |
    | Q7 | boats per colour | first `GROUP BY`, with `string_agg` |
    | Q8 | counting | `count(*)` vs `count(column)` |
    | Q9 | the crew by age | `ORDER BY` as the answer; NULL ordering |
    | Q10 | the 1998 season | `BETWEEN` is inclusive; dates are a type |

    **Next:** `notebook_level_02.py` joins the three tables together.
    """)
    return


if __name__ == "__main__":
    app.run()
