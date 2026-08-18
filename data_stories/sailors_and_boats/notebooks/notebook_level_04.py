"""OMIS 105 -- Sailors & Boats, Level 4: twelve advanced queries (Marimo).

Run it with:
    ./run_notebook_level_04.sh

Twelve queries at the top of the course: relational division three ways,
window functions (running totals, LAG, the three ranking functions, QUALIFY),
PIVOT, and two ways to manufacture the days the database never stored -- a
recursive CTE and a generated range.

Every plot is drawn by a function in src/plots_level_04.py -- this notebook
contains no plotting code, only SQL.
"""

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium", app_title="Sailors & Boats -- Level 4")


@app.cell
def _():
    import sys
    from pathlib import Path

    import marimo as mo

    NOTEBOOK_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = NOTEBOOK_DIR.parent
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

    import plots_level_04 as plots
    import sailors_db as sdb

    con = sdb.connect(read_only=True)

    def run(sql: str):
        return sdb.q(con, sql)

    return mo, plots, run


@app.cell
def _(mo):
    mo.md(r"""
    # Level 4 -- twelve advanced queries

    Three ideas, and everything here is one of them.

    **Relational division** (Q1-Q3) answers *"has this sailor got them all?"*
    SQL has no "for all" keyword, so the question is always written as a double
    negative: *there is no boat that this sailor is missing*. Q10 of Level 3
    built the raw material -- every sailor-boat pair that never happened.

    **Window functions** (Q4-Q7, Q10, Q12) add context to a row without
    collapsing it. `GROUP BY` answers "what is true of this group" and destroys
    the rows; a window answers "where does this row sit in its group" and keeps
    them. That is the whole distinction, and it is worth being able to state.
    Q12 pushes it one step further: three windows in one query, each with a
    different frame.

    **Manufactured rows** (Q8, Q9, Q11) deal with data that is not in the
    database: the months that make a readable grid, and the quiet days between
    bookings. `PIVOT` reshapes what exists; a recursive CTE (Q9) and a generated
    range (Q11) produce what never did.

    Two answers in this level are **empty or trivial**, and both are correct.
    Nobody has reserved all nine boats, and every sailor who has ever sailed
    has sailed "in every year" -- because there is exactly one year. Reading a
    degenerate answer correctly is a skill; assuming the query is broken is the
    mistake.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Q1. Has anybody reserved *every* boat? *(chart)*

    The counting form of division: count each sailor's distinct boats and
    compare against the size of the fleet. It is usually the fastest form, and
    it is the one to reach for when you also want to know *how close* everyone
    got.

    **The answer is nobody**, and the reason is in the data rather than in the
    query: five of the nine boats have never been reserved by anyone (P2), so
    no sailor can possibly hold all nine. Dustin leads with four.

    Written as `HAVING count(DISTINCT r.bid) = (SELECT count(*) FROM boats)`
    this query returns zero rows -- a correct answer that teaches nothing and
    looks identical to a broken query. So the `HAVING` is dropped, every sailor
    is kept, and the comparison becomes a column. The chart draws the fleet
    size as a target line, and the gap between the tallest bar and that line is
    the empty answer, made visible.

    `LEFT JOIN` keeps the ten never-booking sailors at zero;
    `count(DISTINCT r.bid)` counts values rather than rows, so their single
    NULL-filled row scores 0 rather than 1.
    """)
    return


@app.cell
def _(plots, run):
    q1 = run(
        """
        SELECT s.sid, s.sname,
               count(DISTINCT r.bid)                                AS boats_reserved,
               (SELECT count(*) FROM boats)                         AS fleet_size,
               count(DISTINCT r.bid) = (SELECT count(*) FROM boats) AS has_them_all
        FROM sailors s
        LEFT JOIN reserves r ON r.sid = s.sid
        GROUP BY s.sid, s.sname
        ORDER BY boats_reserved DESC, s.sid
        """
    )
    plots.plot_division_progress(q1)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q2. Sailors who have reserved every **red** boat

    The same division with a smaller divisor -- and now there is an answer,
    because both red boats have actually been booked. Dustin and Lubber each
    hold 102 and 104.

    This is the classical formulation, and it is worth reading from the inside
    out:

    ```
    NOT EXISTS (              -- there is no ...
      red boat b               -- ... red boat ...
      such that NOT EXISTS (   -- ... that is missing from ...
        a reservation of b by this sailor))   -- ... this sailor's reservations
    ```

    Two negatives, one for "for all" and one for "does not have", which is
    exactly how "has them all" is expressed in a language that only knows how
    to test existence.

    Note what happens to the ten sailors with no reservations: the inner
    `NOT EXISTS` is true for every red boat, so the outer one is false and they
    are excluded -- correctly. The edge case to remember is that if there were
    **no red boats at all**, the outer `NOT EXISTS` would be true for
    *everybody*: with nothing to be missing, every sailor vacuously has them
    all. Division over an empty divisor returns the whole crew, and that is
    logic, not a bug.
    """)
    return


@app.cell
def _(mo, run):
    q2 = run(
        """
        SELECT s.sid, s.sname
        FROM sailors s
        WHERE NOT EXISTS (
            SELECT 1
            FROM boats b
            WHERE b.color = 'red'
              AND NOT EXISTS (
                  SELECT 1 FROM reserves r
                  WHERE r.sid = s.sid AND r.bid = b.bid
              )
        )
        ORDER BY s.sid
        """
    )
    mo.ui.table(q2, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q3. Sailors who have sailed in **every** year

    Division again, over a divisor computed from the data itself: the set of
    years that appear in `reserves`.

    **Every sailor who has ever sailed qualifies, because there is exactly one
    year in this database.** "Sailed in all years" and "sailed at all" are the
    same question when the data covers one season, and the query is right --
    the divisor is simply as small as a divisor can be while still being
    non-empty.

    The columns are kept in the output for that reason: `years_in_data` says 1,
    so the reader can see immediately why `years_sailed = years_in_data` is
    such a low bar. A result that looks impressive because of the shape of the
    data, rather than because of what anybody did, is worth labelling as such.

    The pattern generalises without change. Add a 1999 season and this query
    starts distinguishing sailors who came back from sailors who did not --
    which is the point of writing division rather than `count(*) = 1`.
    """)
    return


@app.cell
def _(mo, run):
    q3 = run(
        """
        WITH years AS (
            SELECT DISTINCT extract(year FROM day) AS yr FROM reserves
        )
        SELECT s.sid, s.sname,
               count(DISTINCT extract(year FROM r.day)) AS years_sailed,
               (SELECT count(*) FROM years)             AS years_in_data
        FROM sailors s
        JOIN reserves r ON r.sid = s.sid
        GROUP BY s.sid, s.sname
        HAVING count(DISTINCT extract(year FROM r.day)) = (SELECT count(*) FROM years)
        ORDER BY s.sid
        """
    )
    mo.ui.table(q3, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q4. The season accumulating *(chart)*

    `sum(count(*)) OVER (ORDER BY r.day)` -- an aggregate inside a window
    function, which reads like a typo the first time.

    It is not. The two run in order: `GROUP BY r.day` collapses the
    reservations into one row per day, and `count(*)` is that day's total. The
    window then runs **over those grouped rows**, summing every count from the
    first day up to the current one. A running total is by definition an
    aggregate of aggregates.

    `OVER (ORDER BY r.day)` with no frame clause means "everything up to and
    including this row" -- the default frame is what makes it cumulative.
    `OVER ()` with no `ORDER BY`, used in the last column, means "the whole
    result", which is how a percentage-of-total gets its denominator without a
    second query.

    The chart steps rather than slopes: the total holds flat between bookings,
    and a straight line between two points would claim reservations on days
    that had none.
    """)
    return


@app.cell
def _(plots, run):
    q4 = run(
        """
        SELECT r.day,
               count(*)                                       AS n_reservations,
               sum(count(*)) OVER (ORDER BY r.day)::BIGINT    AS running_total,
               round(100.0 * sum(count(*)) OVER (ORDER BY r.day)
                     / sum(count(*)) OVER (), 1)              AS pct_of_season
        FROM reserves r
        GROUP BY r.day
        ORDER BY r.day
        """
    )
    plots.plot_running_total(q4)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q5. `ROW_NUMBER` vs `RANK` vs `DENSE_RANK` *(chart)*

    Three functions, one window, and they only ever disagree inside a tie:

    | function | on a tie | after a tie of 10 |
    |---|---|---|
    | `ROW_NUMBER()` | breaks it arbitrarily -- 5, 6, 7 … | next value 15 |
    | `RANK()` | shares the position -- 5, 5, 5 … | jumps to 15 |
    | `DENSE_RANK()` | shares the position -- 5, 5, 5 … | continues at 6 |

    For the four sailors who have actually sailed, all three agree. Then ten
    sailors tie at zero reservations: `ROW_NUMBER` fans them out from 5 to 14 in
    an order nothing in the query specifies, while `RANK` and `DENSE_RANK` hold
    flat at 5.

    That fanning-out is the danger. `ROW_NUMBER` always produces distinct
    numbers, so `WHERE rn <= 3` always returns exactly three rows -- and looks
    authoritative whether or not the boundary between third and fourth means
    anything. It is the right tool when you need exactly one row per group
    (Q10), and the wrong one for "the top three".

    `WINDOW w AS (...)` names the window once so all three functions share it.
    Repeating the `OVER (...)` clause three times would work identically and
    drift the first time somebody edits one of them.
    """)
    return


@app.cell
def _(plots, run):
    q5 = run(
        """
        SELECT s.sid, s.sname,
               count(r.bid)        AS n_reservations,
               row_number() OVER w AS as_row_number,
               rank()       OVER w AS as_rank,
               dense_rank() OVER w AS as_dense_rank
        FROM sailors s
        LEFT JOIN reserves r ON r.sid = s.sid
        GROUP BY s.sid, s.sname
        WINDOW w AS (ORDER BY count(r.bid) DESC)
        ORDER BY n_reservations DESC, s.sid
        """
    )
    plots.plot_rank_functions(q5)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q6. How long does each boat sit idle? *(chart)*

    `LAG(r.day) OVER (PARTITION BY r.bid ORDER BY r.day)` reaches back to the
    previous row **within the same boat**. Subtract it from the current day and
    you have the turnaround: how long that hull sat at the dock.

    `PARTITION BY` is what keeps boats from bleeding into each other -- without
    it, `LAG` would hand boat 102 the last outing of boat 101 and produce a gap
    that spans two different hulls. Read it as "restart the window here".

    Every boat's first outing has a NULL gap, because there is no earlier row
    to subtract. That is the correct answer, not missing data, and the chart
    drops those rows rather than drawing them as zero -- "no previous outing"
    and "went out again the next day" are different facts and must not look
    alike.

    The gaps here are all around a month, which says something the reservation
    counts do not: this is a marina used a few times a season, not a fleet in
    daily rotation.
    """)
    return


@app.cell
def _(plots, run):
    q6 = run(
        """
        SELECT b.bid || ' ' || b.bname AS boat,
               r.day,
               lag(r.day) OVER w            AS previous_outing,
               r.day - lag(r.day) OVER w    AS idle_days
        FROM reserves r
        JOIN boats b ON b.bid = r.bid
        WINDOW w AS (PARTITION BY r.bid ORDER BY r.day)
        ORDER BY r.bid, r.day
        """
    )
    plots.plot_boat_idle(q6)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q7. Each sailor's share of the season *(chart)*

    `sum(count(*)) OVER ()` -- the same construction as Q4 with the `ORDER BY`
    removed. An empty `OVER ()` means the window is the entire result set, so
    the denominator is every reservation in the season, computed in the same
    pass as the numerator.

    Without it this needs two queries and a join, or a repeated subquery in
    every row. With it the percentages are guaranteed to sum to 100, because
    they were divided by a total the database computed rather than one somebody
    typed.

    Four sailors, 4/3/2/1 reservations, 40/30/20/10 percent. The pie is
    defensible for the usual reason: every reservation belongs to exactly one
    sailor, so the slices really are parts of one whole.
    """)
    return


@app.cell
def _(plots, run):
    q7 = run(
        """
        SELECT s.sname || ' (' || s.sid || ')' AS sailor,
               count(*)                        AS n_reservations,
               round(100.0 * count(*) / sum(count(*)) OVER (), 1) AS pct_of_season
        FROM reserves r
        JOIN sailors s ON s.sid = r.sid
        GROUP BY sailor
        ORDER BY n_reservations DESC, sailor
        """
    )
    plots.plot_season_share(q7)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q8. A boat-by-month grid, with `PIVOT` *(chart)*

    `GROUP BY` puts categories down the page; `PIVOT` puts them across it. The
    months become **columns**, which is the shape a person reads a calendar in.

    ```sql
    PIVOT (…rows…) ON month USING count(*) GROUP BY boat
    ```

    Three parts: the rows to reshape, the column whose *values* become column
    names, and the aggregate that fills each cell. DuckDB reads the distinct
    months out of the data to decide the columns -- which is convenient, and
    the reason a pivoted query has a shape that depends on its contents. Add a
    1999 booking and this result grows a column; a program consuming it has to
    cope with that, which is why pivoting is usually the last step before a
    human looks.

    The chart melts the grid straight back to one row per cell, because that is
    what a renderer wants. Wide for people, long for machines -- worth seeing
    both shapes of the same ten reservations side by side.
    """)
    return


@app.cell
def _(plots, run):
    q8 = run(
        """
        PIVOT (
            SELECT b.bid || ' ' || b.bname   AS boat,
                   strftime(r.day, '%Y-%m')  AS month
            FROM reserves r
            JOIN boats b ON b.bid = r.bid
        )
        ON month
        USING count(*)
        GROUP BY boat
        ORDER BY boat
        """
    )
    plots.plot_month_heatmap(q8)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q9. The quiet days -- a recursive calendar *(chart)*

    Every query so far could only see days that appear in `reserves`. There are
    nine of them. The season is sixty-nine days long, and the sixty days when
    nothing happened exist in the calendar but in no table -- so utilisation
    cannot be measured from the data alone. It has to be measured against a
    spine of every date, and the spine has to be manufactured.

    `WITH RECURSIVE` does that in two parts: a starting row (the first booking)
    and a rule that produces the next row from the previous one (`day + 1`),
    stopping at the last booking. The database applies the rule until it
    returns nothing.

    The `LEFT JOIN` onto that spine is what makes zero-days real rows, and
    `count(r.bid)` -- counting a column, not `*` -- is what makes them count 0.
    This is the same pattern as Level 2's never-reserved boats, applied to time
    instead of to hulls.

    DuckDB also has `generate_series`, which produces the same spine in one
    line. The recursive form is here because it is the general tool: series of
    dates are the easy case, and the same shape walks a hierarchy or follows a
    chain of references.
    """)
    return


@app.cell
def _(plots, run):
    q9 = run(
        """
        WITH RECURSIVE bounds AS (
            SELECT min(day) AS first_day, max(day) AS last_day FROM reserves
        ),
        season(day) AS (
            SELECT first_day FROM bounds            -- the starting row
            UNION ALL
            SELECT day + 1 FROM season, bounds      -- ... and the rule
            WHERE day < bounds.last_day
        )
        SELECT se.day,
               count(r.bid) AS boats_out,
               round(100.0 * count(r.bid) / (SELECT count(*) FROM boats), 1)
                   AS pct_of_fleet
        FROM season se
        LEFT JOIN reserves r ON r.day = se.day
        GROUP BY se.day
        ORDER BY se.day
        """
    )
    plots.plot_utilisation(q9)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q10. Each sailor's first outing of the season

    "One row per group, chosen by a rule" -- the top-N-per-group problem, and
    the reason `ROW_NUMBER` exists.

    `QUALIFY` is the piece that makes it readable. A window function cannot go
    in `WHERE`, because `WHERE` runs before the window is computed; the
    standard workaround is to compute the row number in a subquery and filter
    it on the outside. `QUALIFY` filters on a window function directly, in the
    same way `HAVING` filters on an aggregate -- one clause instead of a
    wrapper.

    The `ORDER BY r.day, r.bid` inside the window is deliberate. `ROW_NUMBER`
    always returns exactly one row per sailor, so if two reservations tied on
    the day it would pick one silently; adding `r.bid` makes the choice
    deterministic. In this database no sailor *can* have two reservations on
    one day -- `UNIQUE (sid, day)`, R10 -- so the tiebreaker never fires here.
    Write it anyway: the query outlives the schema that guaranteed it.

    Horatio (64) opened the season on 5 September; Lubber did not start until
    November.
    """)
    return


@app.cell
def _(mo, run):
    q10 = run(
        """
        SELECT s.sname, r.sid, r.day, b.bid, b.bname, b.color
        FROM reserves r
        JOIN sailors s ON s.sid = r.sid
        JOIN boats   b ON b.bid = r.bid
        QUALIFY row_number() OVER (PARTITION BY r.sid ORDER BY r.day, r.bid) = 1
        ORDER BY r.day
        """
    )
    mo.ui.table(q10, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q11. How many days a year did nobody sail? *(chart)*

    A question about **days that are not in the table**, so the days have to be
    manufactured first — the same calendar-spine idea as Q9, with two changes
    worth studying.

    **The spine in one line.** Q9 built it with `WITH RECURSIVE`; this is
    `range(...)` unnested into rows, which is what you would actually write for
    a series of dates. The recursive form is still the general tool — it walks
    hierarchies and follows chains, where `range` only counts — but for a
    calendar it is three lines of ceremony for one line of work.

    **The join must be against *distinct* days.** This is the trap:

    ```sql
    LEFT JOIN reserves r ON r.day = s.day        -- WRONG for this question
    ```

    1998-09-08 has two reservations, so that join emits the day twice and the
    spine of 69 days comes back as 70 rows with 10 "booked days". The counts are
    of *reservations*, not of days, and nothing about the result looks broken.
    Joining `SELECT DISTINCT day FROM reserves` keeps one row per day, which is
    what "days where nobody sailed" is asking about.

    **Idle relative to what?** The bar is the *observed* season —
    `min(day)` to `max(day)` — not the calendar year. Over the tutorial's 69
    observed days, 9 had a booking and **60 did not: 87% idle**. Measured
    against the whole of 1998 instead it would be 356 idle days, which is true
    and useless: nobody claims the marina was shut in March, only that the data
    says nothing about it. Choosing the window is part of answering the
    question, and it belongs in the output so a reader can see which one you
    chose.

    Against `sailors_and_boats_2.duckdb` this returns three real years —
    roughly 100 idle days each, mostly winter.
    """)
    return


@app.cell
def _(plots, run):
    q11 = run(
        """
        WITH bounds AS (
            SELECT min(day) AS first_day, max(day) AS last_day FROM reserves
        ),
        spine AS (          -- every date in the observed season, one per row
            SELECT unnest(range((SELECT first_day FROM bounds),
                                (SELECT last_day  FROM bounds) + INTERVAL 1 DAY,
                                INTERVAL 1 DAY))::DATE AS day
        ),
        booked AS (         -- one row per DAY, not per reservation
            SELECT DISTINCT day FROM reserves
        )
        SELECT extract(year FROM s.day)::INTEGER AS yr,
               count(*)                          AS days_observed,
               count(b.day)                      AS days_with_a_booking,
               count(*) - count(b.day)           AS idle_days,
               round(100.0 * (count(*) - count(b.day)) / count(*), 1) AS pct_idle
        FROM spine s
        LEFT JOIN booked b ON b.day = s.day
        GROUP BY yr
        ORDER BY yr
        """
    )
    plots.plot_idle_days(q11)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q12. Which year saw the most sailing? *(chart)*

    Ranking a `GROUP BY`, which brings up something this notebook has not said
    yet: **a window's `ORDER BY` has nothing to do with the result's `ORDER BY`,
    and the two here are deliberately different.**

    * `rank() OVER (ORDER BY count(*) DESC)` — ranks the years by *volume*.
    * `lag(count(*)) OVER (ORDER BY yr)` — looks back one year in *chronology*,
      so the change column compares each year with the one before it, not with
      the year above it in the table.
    * `sum(count(*)) OVER ()` — the whole-result denominator from Q7 again.

    Three windows, three different frames, one pass over the data.

    **The error you will hit writing this.** The natural way to spell the second
    one is:

    ```sql
    lag(count(*)) OVER (ORDER BY extract(year FROM day))   -- Binder Error
    ```

    and DuckDB refuses: *column "day" must appear in the GROUP BY clause*. After
    grouping, `day` no longer exists as a row-level column — the only things a
    window can see are the grouping expressions and the aggregates. Ordering by
    the alias `yr` works because that *is* the grouping expression. (Part 6 of
    the guided notebook is the sibling lesson: where you may and may not use a
    name you invented one line earlier.)

    `change_on_previous_year` is NULL for the earliest year, because `LAG` has
    no previous row — the same NULL as Q6's first outing, for the same reason.

    **A caution the query cannot express.** Ranking years by total bookings
    compares windows of different length. On the second database 2026 ranks
    last with 1,357 bookings, but 2026 stops on 17 August — it is two-thirds of
    a year losing to two whole ones. `n_sailors` and `n_boats` are in the output
    as a sanity check; a fair comparison would divide by observed days, which is
    exactly what Q11 counted.

    On the tutorial data there is one season, so the ranking is a formality:
    one row, rank 1, 100%.
    """)
    return


@app.cell
def _(plots, run):
    q12 = run(
        """
        SELECT extract(year FROM day)::INTEGER AS yr,
               count(*)            AS n_reservations,
               count(DISTINCT sid) AS n_sailors,
               count(DISTINCT bid) AS n_boats,
               rank() OVER (ORDER BY count(*) DESC)               AS rank_by_volume,
               round(100.0 * count(*) / sum(count(*)) OVER (), 1) AS pct_of_all_time,
               -- ORDER BY yr, not by volume: this looks back one YEAR
               count(*) - lag(count(*)) OVER (ORDER BY yr) AS change_on_previous_year
        FROM reserves
        GROUP BY yr
        ORDER BY rank_by_volume, yr
        """
    )
    plots.plot_year_ranking(q12)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ### What Level 4 covered

    | | query | the idea |
    |---|---|---|
    | Q1 | every boat? | division by counting; an empty answer, drawn |
    | Q2 | every red boat | division as a double `NOT EXISTS` |
    | Q3 | every year? | division over a divisor of size one |
    | Q4 | running total | an aggregate inside a window; the default frame |
    | Q5 | three rank functions | they differ only inside a tie |
    | Q6 | idle days per boat | `LAG` with `PARTITION BY`; the NULL first row |
    | Q7 | share of the season | `OVER ()` as a whole-result denominator |
    | Q8 | boats by month | `PIVOT`, and why wide tables are for people |
    | Q9 | quiet days | `WITH RECURSIVE` manufactures rows that never existed |
    | Q10 | first outing per sailor | `QUALIFY` + `ROW_NUMBER` for top-N-per-group |
    | Q11 | idle days per year | a spine from `range()`, and why the join needs `DISTINCT` |
    | Q12 | years ranked | three windows, three frames; ordering by a grouping alias |

    That is the four levels. `notebooks/sailors_and_boats_notebook.py` is the
    original guided notebook, which works the same schema from a different
    angle -- the assignment's sixteen graded queries, the twelve classic
    exercises, and the argument for why `reserves` is keyed the way it is.
    """)
    return


if __name__ == "__main__":
    app.run()
