"""OMIS 105 -- Sailors & Boats, Level 2: ten intermediate queries (Marimo).

Run it with:
    ./run_notebook_level_02.sh

Ten queries that put the three tables together: joins, GROUP BY, HAVING,
scalar subqueries, EXISTS, FILTER and UNION ALL.

Every plot is drawn by a function in src/plots_level_02.py -- this notebook
contains no plotting code, only SQL.
"""

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium", app_title="Sailors & Boats -- Level 2")


@app.cell
def _():
    import sys
    from pathlib import Path

    import marimo as mo

    NOTEBOOK_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = NOTEBOOK_DIR.parent
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

    import plots_level_02 as plots
    import sailors_db as sdb

    con = sdb.connect(read_only=True)

    def run(sql: str):
        return sdb.q(con, sql)

    return mo, plots, run


@app.cell
def _(mo):
    mo.md(r"""
    # Level 2 -- ten intermediate queries

    Level 1 read one table at a time. Everything here needs two or three of
    them at once, which brings the two questions that make SQL feel different
    from a spreadsheet:

    * **which rows survive a join** -- an inner join silently deletes anything
      unmatched, and this database is built so that matters: ten sailors have
      never reserved a boat and five boats have never been reserved;
    * **what a row means after `GROUP BY`** -- once rows are collapsed into
      groups, a column is only askable if it is the thing you grouped by or an
      aggregate over the group.

    `reserves` is the table that connects the other two. One row means *this
    boat, on this day, held by this sailor* -- and the schema's two keys (R2,
    R3, R10, defined in `database/sql/01_schema.sql`) mean a day is a one-to-one
    matching: a boat has at most one sailor, a sailor at most one boat.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Q1. Who has ever reserved a boat -- and who never has *(chart)*

    Two ways to ask this. The direct one is a join:

    ```sql
    SELECT DISTINCT s.sid, s.sname
    FROM sailors s JOIN reserves r ON r.sid = s.sid
    ```

    `DISTINCT` is doing real work there -- Dustin has four reservations, so the
    join produces four Dustin rows and only the `DISTINCT` turns them back into
    one sailor. Any time a join multiplies rows, ask whether the question was
    about sailors or about reservations.

    The query below asks it with `EXISTS` instead, which stops at the first
    matching reservation rather than building all four and throwing three away
    -- and, because it answers *yes or no* per sailor, it can label the sailors
    who have never booked anything in the same pass. Ten of the fourteen.
    """)
    return


@app.cell
def _(plots, run):
    q1 = run(
        """
        SELECT CASE WHEN EXISTS (SELECT 1 FROM reserves r WHERE r.sid = s.sid)
                    THEN 'has reserved a boat'
                    ELSE 'never reserved a boat' END AS status,
               count(*) AS n_sailors,
               string_agg(s.sname, ', ' ORDER BY s.sid) AS who
        FROM sailors s
        GROUP BY status
        ORDER BY n_sailors DESC
        """
    )
    plots.plot_who_sails(q1)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q2. Sailors who have reserved a red boat

    The three-table join, and the shape most questions in this course take:
    start at `sailors`, step through `reserves` to reach `boats`, then filter
    on the far table.

    Each `ON` clause names the column pair that links two tables -- `r.sid =
    s.sid`, then `b.bid = r.bid`. Leave one out and the database joins every
    row to every row (a cross join): 14 x 10 x 9 = 1,260 rows of nonsense, no
    error message.

    `DISTINCT` again, and for the same reason as Q1: Dustin holds two different
    red boats, and the question asked for sailors.
    """)
    return


@app.cell
def _(mo, run):
    q2 = run(
        """
        SELECT DISTINCT s.sid, s.sname, s.rating
        FROM sailors s
        JOIN reserves r ON r.sid = s.sid
        JOIN boats    b ON b.bid = r.bid
        WHERE b.color = 'red'
        ORDER BY s.sid
        """
    )
    mo.ui.table(q2, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q3. Sailors who have reserved at least two boats *(chart)*

    `WHERE` filters rows before grouping; **`HAVING` filters groups after**.
    "At least two boats" is a fact about a sailor's whole set of reservations,
    so it cannot be tested until the group exists -- which is why it belongs in
    `HAVING` and could not be written in `WHERE`.

    `count(DISTINCT r.bid)` rather than `count(*)`: the question is about
    different boats, and a sailor who took the same hull out twice has not
    reserved two boats. In this data the two counts agree for everybody, which
    is exactly when the distinction is easiest to get wrong and hardest to
    notice.
    """)
    return


@app.cell
def _(plots, run):
    q3 = run(
        """
        SELECT s.sid, s.sname,
               count(DISTINCT r.bid) AS n_boats,
               count(*)              AS n_reservations
        FROM sailors s
        JOIN reserves r ON r.sid = s.sid
        GROUP BY s.sid, s.sname
        HAVING count(DISTINCT r.bid) >= 2
        ORDER BY n_boats DESC, s.sid
        """
    )
    plots.plot_boats_per_sailor(q3)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q4. Sailors whose name begins and ends with B, and is at least 3 letters

    Three conditions, one per phrase in the question. `LIKE 'b%'` anchors the
    start, `LIKE '%b'` anchors the end, and `length(sname) >= 3` keeps a
    hypothetical sailor called "Bb" out -- with two letters, one B would be
    doing both jobs.

    The `lower(...)` is what makes this work at all. Bob is stored with a
    capital B, so `LIKE 'b%'` alone matches nothing and `LIKE 'B%'` misses a
    lower-case entry. Folding both sides to one case is the habit worth
    keeping; a bare `LIKE` on user-entered text is a bug waiting for the first
    person who types their name differently.
    """)
    return


@app.cell
def _(mo, run):
    q4 = run(
        """
        SELECT sid, sname, age
        FROM sailors
        WHERE lower(sname) LIKE 'b%'
          AND lower(sname) LIKE '%b'
          AND length(sname) >= 3
        ORDER BY age
        """
    )
    mo.ui.table(q4, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q5. Who is rated highest? *(chart)*

    The tie trap from Level 1's Q5, now with data that actually ties: **Rusty
    and Zorba both hold a 10**. `ORDER BY rating DESC LIMIT 1` would name one
    of them and quietly discard the other.

    So the maximum is computed once, in a scalar subquery, and every rating is
    compared against it. The query returns the whole distribution with the top
    one flagged, which answers the question *and* shows the shape it came from
    -- and the flagged bar being two sailors tall is the tie, drawn.

    `WHERE rating IS NOT NULL` drops Dan. "Unrated" is not a point on a 1-10
    scale, and leaving him in would add a bar the axis cannot honestly place.
    """)
    return


@app.cell
def _(plots, run):
    q5 = run(
        """
        WITH top AS (SELECT max(rating) AS top_rating FROM sailors)
        SELECT s.rating,
               count(*) AS n_sailors,
               string_agg(s.sname, ', ' ORDER BY s.sid) AS who,
               s.rating = (SELECT top_rating FROM top) AS is_top_rating
        FROM sailors s
        WHERE s.rating IS NOT NULL
        GROUP BY s.rating
        ORDER BY s.rating
        """
    )
    plots.plot_rating_distribution(q5)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q6. The youngest and the oldest sailor, in one answer

    Two questions whose answers have the same shape, stacked with `UNION ALL`.
    The rule is that both sides must have the same number of columns, in the
    same order, with compatible types -- the column *names* come from the first
    branch, which is why the second one does not need to repeat them.

    The literal `'youngest'` / `'oldest'` column is the important part: without
    it the result is two rows with no way to tell which is which. Adding a tag
    column to label the branch is the standard trick, and Level 4 reuses it to
    run the same division against two different divisors.

    `UNION ALL` keeps duplicates; plain `UNION` would sort and de-duplicate the
    combined result, doing work this query does not need.
    """)
    return


@app.cell
def _(mo, run):
    q6 = run(
        """
        SELECT 'youngest' AS which, sid, sname, age
        FROM sailors
        WHERE age = (SELECT min(age) FROM sailors)

        UNION ALL

        SELECT 'oldest', sid, sname, age
        FROM sailors
        WHERE age = (SELECT max(age) FROM sailors)

        ORDER BY age
        """
    )
    mo.ui.table(q6, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q7. How many *different* sailor names are there?

    Fourteen sailors, thirteen names: **sid 64 and sid 74 are both called
    Horatio**. They are different people, and the database says so -- the key
    is `sid`, and nothing anywhere requires `sname` to be unique.

    `count(DISTINCT sname)` is the answer to the question as asked. Put beside
    `count(*)` and `count(sname)` it also shows the two different reasons those
    three numbers can disagree: NULLs make `count(column)` smaller than
    `count(*)`, and repeats make `count(DISTINCT column)` smaller again.

    The practical warning: any query that groups people by name merges the two
    Horatios into one sailor with three reservations. Group by `sid`, and carry
    `sname` along for the reader.
    """)
    return


@app.cell
def _(mo, run):
    q7 = run(
        """
        SELECT count(*)                            AS n_rows,
               count(sname)                        AS n_non_null_names,
               count(DISTINCT sname)               AS n_different_names,
               count(*) - count(DISTINCT sname)    AS n_names_shared
        FROM sailors
        """
    )
    mo.ui.table(q7, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q8. Sailors old enough to vote, per rating level *(chart)*

    Two counts over the same group: how many sailors hold this rating, and how
    many of them are over 18. `count(*) FILTER (WHERE age > 18)` does the
    second without a second pass and without a second query -- the `FILTER`
    clause applies to that aggregate alone.

    The alternative you will see in older code is
    `sum(CASE WHEN age > 18 THEN 1 ELSE 0 END)`, which does the same thing more
    noisily. Both are worth recognising; `FILTER` is worth writing.

    One sailor is excluded by the filter: Zorba, aged 16 -- and he is rated 10,
    so the rating level with the most experience is also the only one with a
    minor in it.
    """)
    return


@app.cell
def _(plots, run):
    q8 = run(
        """
        SELECT rating,
               count(*)                          AS n_sailors,
               count(*) FILTER (WHERE age > 18)  AS n_can_vote,
               count(*) FILTER (WHERE age <= 18) AS n_too_young
        FROM sailors
        WHERE rating IS NOT NULL
        GROUP BY rating
        ORDER BY rating
        """
    )
    plots.plot_voting_by_rating(q8)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q9. How many boats were used each year?

    `extract(year FROM day)` pulls a grouping key out of a date -- the standard
    way to roll a time column up to a coarser grain. Swap `year` for `month` or
    `week` and nothing else in the query changes.

    **And then the answer is one row, because every reservation in this
    database happened in 1998.** That is not a bug and it is not worth
    "fixing" with invented data: it is what a per-period query looks like when
    the data covers one period, and reading it correctly is the skill.

    Two things follow. First, a chart of a single bar is a number with
    decoration, so this query is a table. Second, be careful what you conclude
    from it -- "4 boats used in 1998" is a fact about the season; it is not a
    trend, and there is no second year to compare it with. Level 4 asks the
    same data which sailors sailed *in every year*, and gets an answer that
    looks impressive for the same uninteresting reason.
    """)
    return


@app.cell
def _(mo, run):
    q9 = run(
        """
        SELECT extract(year FROM r.day) AS yr,
               count(DISTINCT r.bid)    AS n_boats_used,
               count(DISTINCT r.sid)    AS n_sailors,
               count(*)                 AS n_reservations,
               min(r.day)               AS first_day,
               max(r.day)               AS last_day
        FROM reserves r
        GROUP BY yr
        ORDER BY yr
        """
    )
    mo.ui.table(q9, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q10. Every boat, including the ones nobody has ever booked *(chart)*

    The join that keeps its left-hand rows. `LEFT JOIN reserves` gives boats
    105-109 a row each with nothing attached, and `count(r.day)` counts
    **non-NULL values**, so those boats score 0 rather than 1 -- the mistake
    `count(*)` would make, because there is still one row there to count.

    Three ways to ask "which boats have never been reserved", all correct here:

    | form | how it reads |
    |---|---|
    | `LEFT JOIN … GROUP BY … HAVING count(r.day) = 0` | keep everything, then count |
    | `WHERE NOT EXISTS (SELECT 1 FROM reserves r WHERE r.bid = b.bid)` | no matching reservation exists |
    | `WHERE b.bid NOT IN (SELECT bid FROM reserves)` | not in the list of booked bids |

    The third is the one to be careful with: if the subquery can return a NULL,
    `NOT IN` returns no rows at all, and gives no hint why. Level 3 has the
    worked demonstration.

    The `LEFT JOIN` form is used below because it answers a wider question --
    every boat with its count -- and the never-booked ones are the rows at
    zero.
    """)
    return


@app.cell
def _(plots, run):
    q10 = run(
        """
        SELECT b.bid, b.bname, b.color,
               count(r.day)      AS n_reservations,
               count(r.day) = 0  AS never_reserved
        FROM boats b
        LEFT JOIN reserves r ON r.bid = b.bid
        GROUP BY b.bid, b.bname, b.color
        ORDER BY n_reservations DESC, b.bid
        """
    )
    plots.plot_bookings_per_boat(q10)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ### What Level 2 covered

    | | query | the idea |
    |---|---|---|
    | Q1 | who sails at all | `EXISTS` vs `JOIN … DISTINCT` |
    | Q2 | reserved a red boat | the three-table join |
    | Q3 | at least two boats | `HAVING`, and `count(DISTINCT …)` |
    | Q4 | names from B to B | `LIKE` anchors, case folding |
    | Q5 | the highest rating | scalar subquery beats `LIMIT 1` on ties |
    | Q6 | youngest and oldest | `UNION ALL` with a tag column |
    | Q7 | different names | three counts, two reasons to differ |
    | Q8 | voters per rating | `FILTER` on an aggregate |
    | Q9 | boats per year | a one-row grouping, read honestly |
    | Q10 | boats never booked | `LEFT JOIN`, and `count(column)` at zero |

    **Next:** `notebook_level_03.py` -- set operations, anti-joins and ranking.
    """)
    return


if __name__ == "__main__":
    app.run()
