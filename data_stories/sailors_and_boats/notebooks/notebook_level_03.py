"""OMIS 105 -- Sailors & Boats, Level 3: ten intermediate+ queries (Marimo).

Run it with:
    ./run_notebook_level_03.sh

Ten queries about combinations and absences: INTERSECT, EXCEPT, NOT EXISTS,
CASE, date arithmetic, ranking windows and the CROSS JOIN that sets up
relational division in Level 4.

Every plot is drawn by a function in src/plots_level_03.py -- this notebook
contains no plotting code, only SQL.
"""

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium", app_title="Sailors & Boats -- Level 3")


@app.cell
def _():
    import sys
    from pathlib import Path

    import marimo as mo

    NOTEBOOK_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = NOTEBOOK_DIR.parent
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

    import plots_level_03 as plots
    import sailors_db as sdb

    con = sdb.connect(read_only=True)

    def run(sql: str):
        return sdb.q(con, sql)

    return mo, plots, run


@app.cell
def _(mo):
    mo.md(r"""
    # Level 3 -- ten intermediate+ queries

    Level 2 asked what is in the data. This level asks harder shapes of
    question:

    * **combinations** -- red *and* green, red *but not* green. A single `WHERE`
      cannot express either, because both are conditions on a sailor's whole
      set of reservations rather than on any one row.
    * **absences** -- boats nobody took, sailors who never sailed. The rows that
      answer these questions are the rows that are *not* there, so the query
      has to be written from the other side.
    * **rank and position** -- top three, bottom three, busiest day. Easy to
      write with `LIMIT`, easy to get wrong when values tie.

    A note on the charts: the top-three and bottom-three queries deliberately
    return the **whole crew** with a flag, rather than three rows. The
    interesting fact at the bottom of this data is a ten-way tie, and `LIMIT 3`
    is precisely the tool that hides it.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Q1. Sailors who have reserved a red boat **and** a green one

    "And" over two conditions on *different rows* is not `AND`. No single
    reservation is both red and green, so `WHERE b.color = 'red' AND b.color =
    'green'` returns nothing -- correctly, and unhelpfully.

    The question is about two sets: sailors seen with a red boat, and sailors
    seen with a green one. `INTERSECT` keeps the sids in both.

    Two other forms say the same thing:

    ```sql
    -- two EXISTS, one per colour
    WHERE EXISTS (SELECT 1 FROM reserves r JOIN boats b ON b.bid = r.bid
                  WHERE r.sid = s.sid AND b.color = 'red')
      AND EXISTS (… AND b.color = 'green')

    -- keep only the two colours, then require both to be present
    WHERE b.color IN ('red', 'green')
    GROUP BY r.sid
    HAVING count(DISTINCT b.color) = 2
    ```

    All three return Dustin and Lubber. Pick by readability: `INTERSECT` when
    the question really is set arithmetic, `EXISTS` when the conditions differ
    in kind rather than in value.
    """)
    return


@app.cell
def _(mo, run):
    q1 = run(
        """
        WITH red_sailors AS (
            SELECT r.sid FROM reserves r JOIN boats b ON b.bid = r.bid
            WHERE b.color = 'red'
        ),
        green_sailors AS (
            SELECT r.sid FROM reserves r JOIN boats b ON b.bid = r.bid
            WHERE b.color = 'green'
        )
        SELECT s.sid, s.sname
        FROM sailors s
        WHERE s.sid IN (SELECT sid FROM red_sailors
                        INTERSECT
                        SELECT sid FROM green_sailors)
        ORDER BY s.sid
        """
    )
    mo.ui.table(q1, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q2. Sailors who reserved a red boat **but no** green one

    The same two sets, subtracted instead of intersected. `EXCEPT` keeps every
    sid on the left that does not appear on the right -- and, like `UNION`, it
    removes duplicates on the way, which is why the result is a clean list of
    sailor ids without a `DISTINCT`.

    Horatio (64) is the answer: he took the red Interlake and the blue one, and
    never a green boat. Dustin and Lubber are removed by the right-hand side.

    Set operators compare **rows, not columns**, so both sides must select the
    same columns in the same order. That is why this query returns bare sids;
    to get names back, wrap it and join `sailors` on the outside -- pulling
    `s.sname` into the `EXCEPT` itself would change what "the same row" means.
    """)
    return


@app.cell
def _(mo, run):
    q2 = run(
        """
        SELECT s.sid, s.sname
        FROM sailors s
        WHERE s.sid IN (
            SELECT r.sid FROM reserves r JOIN boats b ON b.bid = r.bid
            WHERE b.color = 'red'
            EXCEPT
            SELECT r.sid FROM reserves r JOIN boats b ON b.bid = r.bid
            WHERE b.color = 'green'
        )
        ORDER BY s.sid
        """
    )
    mo.ui.table(q2, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q3. The three busiest sailors *(chart)*

    The short answer is `ORDER BY count(*) DESC LIMIT 3`, and for this data it
    is right: Dustin 4, Lubber 3, Horatio (64) 2.

    The query below uses `RANK() OVER (ORDER BY …)` instead and keeps everyone,
    flagging the top three. Two reasons, and both matter more as data grows:

    * a window function **numbers the rows without deleting any**, so the
      answer and its context arrive together -- you can see that fourth place
      is one reservation behind third;
    * `RANK` handles ties the way a scoreboard does. `LIMIT 3` cannot: if three
      sailors tied for third it would return one of them, picked by nothing at
      all.

    `LEFT JOIN` keeps the ten sailors with no reservations in the picture, at
    zero. They are not the answer, but they are the reason the answer is only
    four reservations wide.
    """)
    return


@app.cell
def _(plots, run):
    q3 = run(
        """
        SELECT s.sid, s.sname,
               count(r.bid)                             AS n_reservations,
               count(DISTINCT r.bid)                    AS n_boats,
               rank() OVER (ORDER BY count(r.bid) DESC) AS rank_from_top,
               rank() OVER (ORDER BY count(r.bid) DESC) <= 3 AS in_top_3
        FROM sailors s
        LEFT JOIN reserves r ON r.sid = s.sid
        GROUP BY s.sid, s.sname
        ORDER BY n_reservations DESC, s.sid
        """
    )
    plots.plot_top_sailors(q3)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q4. The three least active sailors *(chart)*

    The mirror of Q3, and the one where `LIMIT 3` breaks outright. **Ten
    sailors have zero reservations.** Asking for "the bottom three" by
    `ORDER BY count ASC LIMIT 3` returns three of those ten, chosen by whatever
    order the database happened to produce -- a different three is just as
    correct, and the output gives no sign that seven others tied.

    `DENSE_RANK() OVER (ORDER BY n_reservations)` answers the question the way
    it was meant: rank 1 is everyone at zero, rank 2 is Horatio (74) at one,
    rank 3 is Horatio (64) at two. Twelve sailors hold the bottom three
    *ranks*, and that is the honest answer.

    `DENSE_RANK` rather than `RANK` because ranks here are being used as
    labels, and `RANK` would jump from 1 straight to 11 after a ten-way tie.
    Level 4 puts all three ranking functions side by side.
    """)
    return


@app.cell
def _(plots, run):
    q4 = run(
        """
        WITH counted AS (
            SELECT s.sid, s.sname, count(r.bid) AS n_reservations
            FROM sailors s
            LEFT JOIN reserves r ON r.sid = s.sid
            GROUP BY s.sid, s.sname
        )
        SELECT sid, sname, n_reservations,
               dense_rank() OVER (ORDER BY n_reservations)      AS rank_from_bottom,
               dense_rank() OVER (ORDER BY n_reservations) <= 3 AS in_bottom_3
        FROM counted
        ORDER BY n_reservations, sid
        """
    )
    plots.plot_bottom_sailors(q4)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q5. What colour does each sailor sail? *(chart)*

    Grouping by two things at once. One row per (sailor, colour) pair, so a
    sailor with two colours gets two rows -- and the chart stacks them back
    into one bar per sailor.

    **Group by `s.sid`, not by `s.sname`.** Both Horatios would otherwise
    collapse into a single sailor holding three reservations across three
    colours, and nothing in the output would look wrong. This is the concrete
    cost of the fact Level 2's Q7 established: names are not keys.

    The label `sname || ' (' || sid || ')'` is in the `SELECT` for the reader,
    and `sid` is in the `GROUP BY` for the database. Grouping on the id and
    displaying the name is the general pattern.
    """)
    return


@app.cell
def _(plots, run):
    q5 = run(
        """
        SELECT s.sid,
               s.sname || ' (' || s.sid || ')' AS sailor,
               b.color,
               count(*) AS n_reservations
        FROM reserves r
        JOIN sailors s ON s.sid = r.sid
        JOIN boats   b ON b.bid = r.bid
        GROUP BY s.sid, sailor, b.color
        ORDER BY s.sid, b.color
        """
    )
    plots.plot_colour_mix(q5)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q6. Each boat's season, first outing to last *(chart)*

    `min(day)` and `max(day)` are the two ends of a boat's season, and
    subtracting one date from another gives a plain number of days -- date
    arithmetic, not string handling. That is what having a real `DATE` type
    buys.

    Read `span_days` carefully, because it is a good example of a number that
    invites a wrong conclusion. The red Interlake (102) spans 63 days and the
    blue one (101) spans 35, but both figures describe *gaps*, not activity:
    102 was out three times and 101 twice. A boat taken out once would have a
    span of zero and could still be the most-used hull in a one-day season.

    The chart draws the span as a bar and the outing count in the tooltip, so
    the two facts stay separate.
    """)
    return


@app.cell
def _(plots, run):
    q6 = run(
        """
        SELECT b.bid,
               b.bid || ' ' || b.bname AS boat,
               b.color,
               count(r.day)            AS n_reservations,
               min(r.day)              AS first_out,
               max(r.day)              AS last_out,
               max(r.day) - min(r.day) AS span_days
        FROM boats b
        JOIN reserves r ON r.bid = b.bid
        GROUP BY b.bid, boat, b.color
        ORDER BY first_out, b.bid
        """
    )
    plots.plot_boat_seasons(q6)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q7. Which day was busiest? *(chart)*

    Group by `day` and count. The subquery `(SELECT count(*) FROM boats)` turns
    that count into a share of the fleet -- a scalar subquery again, computed
    once and reused on every row.

    **1998-09-08 is the only day this marina ever had two boats out**, and it
    is two *different* Horatios: 64 in the red Interlake, 74 in the Clipper.
    Every other day has exactly one reservation.

    That single-boat pattern is data, not a rule. The schema (R2, R3, R10)
    forbids two sailors on one boat, and one sailor on two boats -- it has
    nothing to say about how many distinct boats may be out at once, and nine
    would be perfectly legal.

    Note the two orders: the query sorts by `boats_out DESC` because the
    question is "which day was busiest", and the chart puts the days back in
    date order, because a time axis sorted by value is no longer a time axis.
    """)
    return


@app.cell
def _(plots, run):
    q7 = run(
        """
        SELECT r.day,
               count(*) AS boats_out,
               round(100.0 * count(*) / (SELECT count(*) FROM boats), 1) AS pct_of_fleet,
               string_agg(s.sname || ' / ' || b.bname, ', ' ORDER BY r.bid) AS who
        FROM reserves r
        JOIN sailors s ON s.sid = r.sid
        JOIN boats   b ON b.bid = r.bid
        GROUP BY r.day
        ORDER BY boats_out DESC, r.day
        """
    )
    plots.plot_busiest_days(q7)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q8. The crew in age bands *(chart)*

    `CASE` builds a column that does not exist in the table -- it turns a
    continuous age into a handful of labelled buckets. The branches are tested
    **in order** and the first true one wins, which is why each test only needs
    an upper bound: by the time `age < 40` is reached, everything under 25 has
    already been claimed.

    Two details that decide whether the result is readable:

    * the bands are ordered by `min(age)`, not by the label. Sorted as text,
      `'25 to 39'` comes before `'under 25'`, and the chart tells a story in
      the wrong order.
    * `avg(rating)` skips Dan's NULL, so the band containing him averages four
      ratings across five sailors. That is usually what you want, and it is
      always worth knowing.
    """)
    return


@app.cell
def _(plots, run):
    q8 = run(
        """
        SELECT CASE WHEN age < 25 THEN 'under 25'
                    WHEN age < 40 THEN '25 to 39'
                    WHEN age < 55 THEN '40 to 54'
                    ELSE               '55 and over' END AS age_band,
               count(*)           AS n_sailors,
               round(avg(rating), 2) AS avg_rating,
               round(avg(age), 1)    AS avg_age,
               min(age)              AS band_floor
        FROM sailors
        GROUP BY age_band
        ORDER BY band_floor
        """
    )
    plots.plot_age_bands(q8)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q9. Sailors who have **never** reserved a red boat -- and the `NOT IN` trap

    "Never" is written as `NOT EXISTS`: *there is no reservation of a red boat
    belonging to this sailor*. The subquery is **correlated** -- it mentions
    `s.sid` from the outer query, so it is a different question for each
    sailor, and it can stop at the first match it finds.

    Eleven sailors qualify, including Horatio (74), who has sailed but only
    ever in a green boat.

    The two extra columns are a demonstration, not part of the answer:

    * `sid NOT IN (SELECT sid FROM reserves)` works, because `reserves.sid` can
      never be NULL -- a foreign key with `NOT NULL` behind it (D1).
    * `sid NOT IN (SELECT sid FROM reserves UNION ALL SELECT NULL)` returns
      **NULL for every sailor who is not in the list**, and `WHERE` treats NULL
      as "no". One NULL in the subquery silently empties the result.

    Why: `x NOT IN (a, b, NULL)` means `x <> a AND x <> b AND x <> NULL`, and
    that last comparison is unknown. Unknown ANDed with true is unknown, so the
    row is dropped. `NOT EXISTS` has no such failure mode, which is the reason
    to reach for it by default.
    """)
    return


@app.cell
def _(mo, run):
    q9 = run(
        """
        SELECT s.sid, s.sname,
               s.sid NOT IN (SELECT r.sid FROM reserves r) AS not_in_reserves,
               s.sid NOT IN (SELECT r.sid FROM reserves r
                             UNION ALL SELECT NULL)        AS not_in_with_a_null
        FROM sailors s
        WHERE NOT EXISTS (
            SELECT 1
            FROM reserves r
            JOIN boats b ON b.bid = r.bid
            WHERE r.sid = s.sid AND b.color = 'red'
        )
        ORDER BY s.sid
        """
    )
    mo.ui.table(q9, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q10. Which boats has each sailor *not* taken out?

    `CROSS JOIN` pairs every sailor with every boat: 14 x 9 = 126 combinations,
    all the reservations that *could* exist. `NOT EXISTS` then removes the ones
    that do, leaving the gaps.

    Manufacturing the complete set and subtracting what happened is the general
    way to ask a question about missing rows, and it is worth recognising
    because Level 4 is built on it. Read the last column: **nobody has a gap
    count of zero**, and a sailor with no gaps would be a sailor who has
    reserved every boat -- which is exactly the division question, computed
    from the other end.

    The ten sailors at 9 are the ones who have never booked anything; Dustin's
    5 are the five boats nobody has ever booked at all.
    """)
    return


@app.cell
def _(mo, run):
    q10 = run(
        """
        SELECT s.sid, s.sname,
               count(*) AS n_boats_missing,
               string_agg(b.bid::VARCHAR, ', ' ORDER BY b.bid) AS missing_bids
        FROM sailors s
        CROSS JOIN boats b
        WHERE NOT EXISTS (
            SELECT 1 FROM reserves r
            WHERE r.sid = s.sid AND r.bid = b.bid
        )
        GROUP BY s.sid, s.sname
        ORDER BY n_boats_missing, s.sid
        """
    )
    mo.ui.table(q10, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ### What Level 3 covered

    | | query | the idea |
    |---|---|---|
    | Q1 | red *and* green | `INTERSECT`; "and" across rows is not `AND` |
    | Q2 | red but not green | `EXCEPT`; set operators compare whole rows |
    | Q3 | top three sailors | `RANK()` keeps the context `LIMIT` deletes |
    | Q4 | bottom three | ties break `LIMIT`; `DENSE_RANK` survives them |
    | Q5 | colour mix per sailor | grouping on the id, displaying the name |
    | Q6 | each boat's season | date subtraction, and a misleading measure |
    | Q7 | the busiest day | scalar subquery as a denominator |
    | Q8 | age bands | `CASE`, ordered by value not by label |
    | Q9 | never a red boat | correlated `NOT EXISTS`, and the `NOT IN` NULL trap |
    | Q10 | boats not taken | `CROSS JOIN` + `NOT EXISTS` -- division, upside down |

    **Next:** `notebook_level_04.py` -- division, window functions, `PIVOT` and
    a recursive calendar.
    """)
    return


if __name__ == "__main__":
    app.run()
