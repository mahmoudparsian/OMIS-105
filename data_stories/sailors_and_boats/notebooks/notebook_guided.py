"""OMIS 105 -- Sailors & Boats: a guided SQL notebook (Marimo).

Run it with:
    uv run marimo edit notebooks/notebook_guided.py

Parts 1-4 are the 16 queries the assignment grades: 3 simple, 5 intermediate,
5 intermediate with a plot, 3 advanced. Part 5 adds an extra query with a pie
chart, Part 6 is a lesson on column aliases, and Part 7 works through the
twelve classic Sailors/Boats exercises (Q19-Q28, plus cross-references to Q4
and Q14, which already answer two of them).

Every plot is drawn by a function in src/plots.py -- this notebook contains no
plotting code, only SQL.
"""

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium", app_title="Sailors & Boats -- SQL Notebook")


@app.cell
def _():
    import sys
    import marimo as mo
    import pandas as pd
    from pathlib import Path

    NOTEBOOK_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = NOTEBOOK_DIR.parent
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

    import plots
    import sailors_db as sdb

    # Read-only: the notebook explores, the Streamlit app writes.
    con = sdb.connect(read_only=True)

    def run(sql: str):
        """Execute a SELECT and return a DataFrame.

        Goes through sailors_db.q so DATE columns print as YYYY-MM-DD rather
        than as pandas timestamps with a spurious 00:00:00 -- the notebook and
        the app render dates identically.
        """
        return sdb.q(con, sql)

    return mo, pd, plots, run


@app.cell
def _(mo):
    mo.md(r"""
    # Sailors & Boats -- SQL Notebook

    Three tables, one relationship:

    | table | grain -- "one row is..." | key |
    |---|---|---|
    | `sailors` | one person | `sid` |
    | `boats` | one hull | `bid` |
    | `reserves` | one boat, on one day | **`(bid, day)`**, plus `UNIQUE (sid, day)` |

    The interesting choice is the last one. The tutorial PDF keys `reserves`
    on `(sid, bid, day)`, which would let two sailors take the same boat on
    the same day -- forbidden by R2 and R3. So the key is the *slot* the
    reservation occupies -- a boat on a date -- and `sid` records who holds
    it.

    `UNIQUE (sid, day)` is the mirror rule (R10): a sailor sails one boat a
    day. It has to be declared separately, because the primary key constrains
    the *boat* side of the relationship and never looks at how many boats
    one sailor has taken. Between them, a single day is a one-to-one
    matching: every boat that is out has exactly one sailor, and every
    sailor who is out has exactly one boat. Several queries below lean on
    that.

    **Where the rules are written down.** Every database requirement --
    labelled R1-R10, P1-P3, D1-D2 -- is defined in one place: the
    `REQUIREMENTS` block at the top of `database/sql/01_schema.sql`, next to the
    constraint enforcing it. This notebook cites those labels rather than
    restating the rules. `DESIGN.md` has the long-form reasoning.

    **Data:**

    * the 10 sailors,
    * 4 boats and
    * 10 reservations from the tutorial,
    * plus sailor 99 'Dan' (unrated), 3 more sailors who never reserve anything, and
    * 5 boats nobody has ever booked.

    One tutorial reservation had to move: Figure 1 has sailor 22 holding
    boats 101 *and* 102 on 1998-10-10, so boat 102 sits on 1998-10-09 here.
    Moving it rather than dropping it keeps all 10 rows and every count the
    PDF's worked answers depend on.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why not `PRIMARY KEY (sid, bid, day)`?

    This is the question the schema above always gets, so it is worth
    answering before the queries start: *the PDF's key names all three
    columns, and ours names two -- surely three columns constrain more?*

    They constrain **less**. A `PRIMARY KEY` or `UNIQUE` forbids exactly one
    thing: two rows agreeing on **every** column in the list. Rows differing
    in even one column are legal -- so each column you add is one more way
    for rows to differ, and differing is what makes them legal.

    > **The wider the key, the weaker the constraint.**

    `(sid, bid, day)` is the widest key in this discussion, so it is the
    weakest one. All it forbids is the *identical triple*: the same sailor
    booking the same boat on the same day twice. That is a duplicate-row
    rule, not a rule about boats.

    **What it lets through.** One day, 1998-10-10, four inserts in order,
    under the PDF's `PRIMARY KEY (sid, bid, day)`:

    | # | sid | sailor | bid | boat | accepted? |
    |---|---|---|---|---|---|
    | 1 | 22 | Dustin | 101 | Interlake (blue) | accepted -- the baseline booking |
    | 2 | 22 | Dustin | 102 | Interlake (red) | **accepted** -- differs from #1 in `bid` |
    | 3 | 29 | Brutus | 101 | Interlake (blue) | **accepted** -- differs from #1 in `sid` |
    | 4 | 22 | Dustin | 101 | Interlake (blue) | rejected -- identical to #1 |

    Three rows survive, and they describe a marina where **Dustin is out in
    two boats at once** (rows 1-2, which R10 forbids) and **boat 101 is out
    with both Dustin and Brutus the same morning** (rows 1 and 3, which R2,
    R3 and R4 forbid). The only insert the key stopped was the exact
    duplicate -- the one case nobody needed protecting from.

    **Two rules, so two constraints.** Read each key as the sentence it
    asserts about a single day:

    | constraint | reads as | forbids | but permits |
    |---|---|---|---|
    | `PRIMARY KEY (bid, day)` | a boat has **one** sailor | boat 101 to Dustin *and* Brutus | Dustin in 101 *and* 102 |
    | `UNIQUE (sid, day)` | a sailor has **one** boat | Dustin in 101 *and* 102 | boat 101 to Dustin *and* Brutus |
    | `PRIMARY KEY (sid, bid, day)` | a (sailor, boat, day) appears **once** | Dustin in 101 twice | *both of the above* |

    The first two are mirror images: each one permits precisely what the
    other forbids. That is what "neither implies the other" means in
    practice, and why both are declared. The third forbids neither.

    Two consequences you will meet further down. **Q12's fleet calendar**
    is readable only because of these two constraints -- one sailor per
    cell comes from the primary key, no name repeated down a column comes
    from the `UNIQUE`. And **Q6** has to look for two *sailors* sharing a
    day rather than one sailor's two boats, because `UNIQUE (sid, day)`
    makes the second question structurally unanswerable: no data could
    satisfy it.

    Finally, the sharpest argument of all is the tutorial's own data.
    Figure 1 gives Dustin both boat 101 and boat 102 on 1998-10-10 -- row 2
    of the table above -- which is why one reservation had to move to
    1998-10-09. The PDF's key is the reason the PDF's data breaks the rule.

    `DESIGN.md` §3 has the long-form argument, including R9 (whether
    `UNIQUE (sid, bid, day)` is worth declaring on top of what we have --
    it is not, since each of our two constraints already implies it).
    """)
    return


@app.cell
def _(mo, run):
    overview = run(
        """
        SELECT 'sailors'  AS table_name, count(*) AS n_rows FROM sailors
        UNION ALL SELECT 'boats',    count(*) FROM boats
        UNION ALL SELECT 'reserves', count(*) FROM reserves
        """
    )
    mo.ui.table(overview, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Part 1 -- Three simple queries
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q1. The whole crew

    The plainest query there is: pick columns, name a table, order the
    result. `ORDER BY` is what makes the output stable -- without it SQL is
    free to hand rows back in any order.
    """)
    return


@app.cell
def _(mo, run):
    q1 = run(
        """
        SELECT sid, sname, rating, age
        FROM sailors
        ORDER BY sid
        """
    )
    mo.ui.table(q1, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q2. The red boats

    A `WHERE` filter on one column. Because `boats.color` carries a `CHECK`
    constraint restricting it to a fixed vocabulary, `= 'red'` cannot miss a
    row that somebody typed as `'Red'` -- the schema made this query safe.
    """)
    return


@app.cell
def _(mo, run):
    q2 = run(
        """
        SELECT bid, bname, color
        FROM boats
        WHERE color = 'red'
        ORDER BY bid
        """
    )
    mo.ui.table(q2, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q3. Distinct sailor names

    `DISTINCT` collapses duplicates. There are two different sailors called
    Horatio (`sid` 64 and 74), so this list is shorter than the crew list --
    which is exactly why `sname` is not the key.
    """)
    return


@app.cell
def _(mo, run):
    q3 = run(
        """
        SELECT DISTINCT sname
        FROM sailors
        ORDER BY sname
        """
    )
    mo.ui.table(q3, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Part 2 -- Five intermediate queries
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q4. Who has sailed a red boat? (three-table join)

    The classic path across the schema: `sailors -> reserves -> boats`.
    `reserves` is the bridge; you cannot get from a sailor to a boat without
    walking through it.

    Note the duplicate rows this *would* produce if a sailor took red boats
    twice -- `DISTINCT` keeps the answer a set of people, not a set of trips.
    """)
    return


@app.cell
def _(mo, run):
    q4 = run(
        """
        SELECT DISTINCT s.sid, s.sname, s.age
        FROM sailors  s
        JOIN reserves r ON r.sid = s.sid
        JOIN boats    b ON b.bid = r.bid
        WHERE b.color = 'red'
        ORDER BY s.age
        """
    )
    mo.ui.table(q4, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q5. Sailors who reserved boat 103 -- three ways to say it

    `IN`, `EXISTS` and a plain join all answer this. They are logically
    equivalent here; the difference is style, and how they behave when the
    subquery returns duplicates or NULLs.

    `EXISTS` is *correlated* -- its inner query mentions `s.sid` from the
    outer query, so it re-runs conceptually once per candidate sailor.
    """)
    return


@app.cell
def _(mo, run):
    q5 = run(
        """
        WITH by_in AS (
            SELECT s.sid, s.sname, 'IN'     AS style
            FROM sailors s
            WHERE s.sid IN (SELECT r.sid FROM reserves r WHERE r.bid = 103)
        ),
        by_exists AS (
            SELECT s.sid, s.sname, 'EXISTS' AS style
            FROM sailors s
            WHERE EXISTS (SELECT 1 FROM reserves r
                          WHERE r.bid = 103 AND r.sid = s.sid)
        ),
        by_join AS (
            SELECT DISTINCT s.sid, s.sname, 'JOIN'   AS style
            FROM sailors s JOIN reserves r ON r.sid = s.sid
            WHERE r.bid = 103
        )
        SELECT * FROM by_in
        UNION ALL SELECT * FROM by_exists
        UNION ALL SELECT * FROM by_join
        ORDER BY sid, style
        """
    )
    mo.ui.table(q5, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q6. Which sailors were out together? (self-join)

    A table joined to itself: `reserves` plays the part of two different
    tables, one for each sailor in a pair. The join condition
    `b.day = a.day` puts them on the water on the same date.

    `r1.sid < r2.sid` is doing two jobs at once. Without any condition on
    `sid`, every row would match itself (Dustin out with Dustin). With
    `r1.sid <> r2.sid` we would get each pair *twice*, once in each order
    -- (64, 74) and (74, 64). The `<` keeps one row per pair and does it
    without a `DISTINCT`. Try swapping it for `<>` and count the rows.

    The single pair this finds is a good one: sailors 64 and 74 are the
    two *different* Horatios, out on 1998-09-08 in the Interlake and the
    Clipper. The output columns say "Horatio" twice, which is a reminder
    that the join ran on `sid` -- names are not keys.

    Note what this query can no longer be. Under R10 a sailor
    holds one boat a day, so the self-join that asks "who had two boats
    at once" is guaranteed to return nothing -- the schema answers it
    before the query runs. The interesting question moved to the other
    side of the relationship: not one sailor with many boats, but many
    sailors sharing a day.
    """)
    return


@app.cell
def _(mo, run):
    q6 = run(
        """
        SELECT r1.day,
               s1.sname AS sailor_a, b1.bname AS boat_a,
               s2.sname AS sailor_b, b2.bname AS boat_b
        FROM reserves r1
        JOIN reserves r2 ON r2.day = r1.day
                        AND r1.sid < r2.sid
        JOIN sailors  s1 ON s1.sid = r1.sid
        JOIN sailors  s2 ON s2.sid = r2.sid
        JOIN boats    b1 ON b1.bid = r1.bid
        JOIN boats    b2 ON b2.bid = r2.bid
        ORDER BY r1.day
        """
    )
    mo.ui.table(q6, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q7. Average age per rating, for ratings with more than one sailor

    `GROUP BY` makes the groups, `HAVING` filters the *groups* (after
    aggregation), `WHERE` would have filtered the *rows* (before it). That
    is the whole distinction, and it is the one students most often trip on.

    Sailor 99 'Dan' has a NULL rating and forms his own group -- `AVG`
    discards NULL values, but `GROUP BY` treats NULL as a group of its own.
    """)
    return


@app.cell
def _(mo, run):
    q7 = run(
        """
        SELECT s.rating,
               round(avg(s.age), 2) AS avg_age,
               count(*)             AS n_sailors
        FROM sailors s
        GROUP BY s.rating
        HAVING count(*) > 1
        ORDER BY s.rating
        """
    )
    mo.ui.table(q7, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q8. Everyone, including the sailors who never sail (LEFT OUTER JOIN)

    An inner join answers "who *did*". Only an outer join can answer "who
    did **not**" -- the sailors with no matching `reserves` row survive with
    NULLs, and `count(r.bid)` counts them as 0 because `COUNT(column)`
    skips NULL while `COUNT(*)` would have counted the row anyway.

    Popeye, Olive, Wendy and Dan appear here with 0. They are invisible to
    every query in Part 2 that used a plain join.
    """)
    return


@app.cell
def _(mo, run):
    q8 = run(
        """
        SELECT s.sid, s.sname, s.rating,
               count(r.bid) AS n_reservations,
               min(r.day)   AS first_day,
               max(r.day)   AS last_day
        FROM sailors s
        LEFT JOIN reserves r ON r.sid = s.sid
        GROUP BY s.sid, s.sname, s.rating
        ORDER BY n_reservations DESC, s.sid
        """
    )
    mo.ui.table(q8, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Part 3 -- Five intermediate queries, with plots

    Each cell below runs one query and hands the result to a function in
    `src/plots.py`. No chart code appears in this notebook.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q9. How often is each boat booked?

    `LEFT JOIN` again, from `boats` this time, so the five never-reserved
    boats stay in the answer at zero. Sorting by the count turns the query
    into a ranking.
    """)
    return


@app.cell
def _(plots, run):
    q9 = run(
        """
        SELECT b.bid, b.bname, b.color,
               count(r.day) AS n_reservations
        FROM boats b
        LEFT JOIN reserves r ON r.bid = b.bid
        GROUP BY b.bid, b.bname, b.color
        ORDER BY n_reservations DESC, b.bid
        """
    )
    plots.plot_reservations_per_boat(q9)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q10. Average age at each rating level

    The same grouping as Q7 without the `HAVING`, so every rating level is
    present. `WHERE rating IS NOT NULL` drops Dan's group -- "unrated" is
    not a point on a 1-10 scale and does not belong on this axis.
    """)
    return


@app.cell
def _(plots, run):
    q10 = run(
        """
        SELECT s.rating,
               round(avg(s.age), 2) AS avg_age,
               count(*)             AS n_sailors
        FROM sailors s
        WHERE s.rating IS NOT NULL
        GROUP BY s.rating
        ORDER BY s.rating
        """
    )
    plots.plot_avg_age_by_rating(q10)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q11. Booking volume, month by month

    `date_trunc('month', day)` snaps every date down to the first of its
    month, giving a column you can group on. This is the standard way to
    roll a date column up to a coarser grain -- swap in `'week'` or
    `'year'` and nothing else changes.
    """)
    return


@app.cell
def _(plots, run):
    q11 = run(
        """
        SELECT date_trunc('month', r.day)::DATE AS month_start,
               count(*)                          AS n_reservations
        FROM reserves r
        GROUP BY month_start
        ORDER BY month_start
        """
    )
    plots.plot_reservations_by_month(q11)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q12. The fleet calendar

    Every reservation, laid out as boat x day. This is a picture of both
    of the schema's rules at once. Each **cell** holds at most one sailor,
    because `PRIMARY KEY (bid, day)` makes a second one impossible to
    insert. And no sailor's name appears twice in any **column**, because
    `UNIQUE (sid, day)` forbids it -- a column is one day, and a repeated
    name in it would be a sailor with two boats.

    So read the grid twice: down a column for "who was out that day", and
    along a row for "when was that boat out". Neither direction can ever
    contain a duplicate.
    """)
    return


@app.cell
def _(plots, run):
    q12 = run(
        """
        SELECT r.day,
               r.bid,
               r.bid || ' ' || b.bname AS boat_label,
               r.sid,
               s.sname
        FROM reserves r
        JOIN boats   b ON b.bid = r.bid
        JOIN sailors s ON s.sid = r.sid
        ORDER BY r.day, r.bid
        """
    )
    plots.plot_fleet_calendar(q12)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q13. Does experience predict activity?

    One row per rated sailor, with age, rating and booking count together --
    a scalar subquery in the `SELECT` list is a compact alternative to a
    `LEFT JOIN ... GROUP BY` when you need exactly one number per row.
    """)
    return


@app.cell
def _(plots, run):
    q13 = run(
        """
        SELECT s.sid, s.sname, s.rating, s.age,
               (SELECT count(*) FROM reserves r WHERE r.sid = s.sid) AS n_reservations
        FROM sailors s
        WHERE s.rating IS NOT NULL
        ORDER BY s.sid
        """
    )
    plots.plot_age_vs_rating(q13)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Part 4 -- Three advanced queries
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q14. Relational division -- "has reserved *every* red boat"

    "For all" has no SQL keyword, so it is written as a double negative:
    *there is no red boat that this sailor has not reserved*. The `EXCEPT`
    form below reads almost literally as that sentence -- subtract the
    sailor's boats from all red boats; if nothing is left over, they had
    them all.

    Asking for *every* boat in the fleet returns nobody, because five boats
    have never been reserved at all. Narrowing to red boats gives a real
    answer -- and shows why division is so sensitive to what the divisor is.
    """)
    return


@app.cell
def _(mo, run):
    q14 = run(
        """
        WITH red_boats AS (
            SELECT bid FROM boats WHERE color = 'red'
        ),
        -- Formulation A: set difference must come out empty.
        division_except AS (
            SELECT s.sid, s.sname
            FROM sailors s
            WHERE NOT EXISTS (
                SELECT rb.bid FROM red_boats rb
                EXCEPT
                SELECT r.bid FROM reserves r WHERE r.sid = s.sid
            )
        ),
        -- Formulation B: counting. Cheaper, and usually what an optimiser likes.
        division_count AS (
            SELECT s.sid, s.sname
            FROM sailors s
            JOIN reserves r ON r.sid = s.sid
            JOIN red_boats rb ON rb.bid = r.bid
            GROUP BY s.sid, s.sname
            HAVING count(DISTINCT r.bid) = (SELECT count(*) FROM red_boats)
        )
        SELECT a.sid, a.sname,
               (b.sid IS NOT NULL) AS agrees_with_counting_form
        FROM division_except a
        FULL OUTER JOIN division_count b USING (sid, sname)
        ORDER BY a.sid
        """
    )
    mo.ui.table(q14, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q15. Window functions -- each sailor's season, in order

    `LAG(...) OVER (PARTITION BY sid ORDER BY day)` looks at the previous
    row *within the same sailor* without collapsing the result the way
    `GROUP BY` would. That is the whole point of a window function: you keep
    every row and gain the context around it.

    `days_since_previous` is NULL on a sailor's first booking -- there is no
    previous row to subtract.
    """)
    return


@app.cell
def _(mo, run):
    q15 = run(
        """
        SELECT s.sname,
               r.sid,
               r.day,
               r.bid,
               b.bname,
               row_number() OVER w                       AS trip_no,
               lag(r.day)   OVER w                       AS previous_day,
               r.day - lag(r.day) OVER w                 AS days_since_previous,
               count(*)     OVER (PARTITION BY r.sid)    AS trips_this_season,
               first_value(b.bname) OVER w               AS first_boat_of_season
        FROM reserves r
        JOIN sailors s ON s.sid = r.sid
        JOIN boats   b ON b.bid = r.bid
        WINDOW w AS (PARTITION BY r.sid ORDER BY r.day, r.bid)
        ORDER BY r.sid, r.day, r.bid
        """
    )
    mo.ui.table(q15, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q16. Fleet utilisation over a calendar spine

    The database only stores days on which *something* happened. To measure
    utilisation you also need the quiet days, and they exist nowhere in the
    data -- so you manufacture them with `generate_series` and left-join the
    facts onto that spine.

    This "calendar spine" pattern is the standard fix for gaps in any time
    series, and it is the only way `pct_of_fleet_out` can be honest: without
    it, every day in the result would be a day with at least one booking.
    """)
    return


@app.cell
def _(mo, run):
    q16 = run(
        """
        WITH calendar AS (
            SELECT unnest(generate_series(DATE '1998-09-01',
                                          DATE '1998-11-30',
                                          INTERVAL 1 DAY))::DATE AS day
        ),
        fleet AS (SELECT count(*) AS n_boats FROM boats),
        daily AS (
            SELECT c.day,
                   count(r.bid)                  AS boats_out,
                   count(DISTINCT r.sid)         AS sailors_out,
                   string_agg(DISTINCT s.sname, ', ' ORDER BY s.sname) AS who
            FROM calendar c
            LEFT JOIN reserves r ON r.day = c.day
            LEFT JOIN sailors  s ON s.sid = r.sid
            GROUP BY c.day
        )
        SELECT d.day,
               strftime(d.day, '%a')                                   AS weekday,
               d.boats_out,
               d.sailors_out,
               round(100.0 * d.boats_out / f.n_boats, 1)               AS pct_of_fleet_out,
               d.who,
               rank() OVER (ORDER BY d.boats_out DESC)                 AS busyness_rank
        FROM daily d CROSS JOIN fleet f
        WHERE d.boats_out > 0          -- flip to `>= 0` to see the 80 quiet days too
        ORDER BY d.day
        """
    )
    mo.ui.table(q16, selection=None)
    return


@app.cell
def _(mo, run):
    q16_summary = run(
        """
        WITH calendar AS (
            SELECT unnest(generate_series(DATE '1998-09-01',
                                          DATE '1998-11-30',
                                          INTERVAL 1 DAY))::DATE AS day
        ),
        daily AS (
            SELECT c.day, count(r.bid) AS boats_out
            FROM calendar c LEFT JOIN reserves r ON r.day = c.day
            GROUP BY c.day
        )
        SELECT count(*)                                        AS days_in_season,
               count(*) FILTER (WHERE boats_out > 0)           AS days_with_activity,
               count(*) FILTER (WHERE boats_out = 0)           AS idle_days,
               max(boats_out)                                  AS busiest_day_boats,
               round(avg(boats_out), 3)                        AS avg_boats_out_per_day,
               round(100.0 * sum(boats_out)
                     / (count(*) * (SELECT count(*) FROM boats)), 2) AS season_utilisation_pct
        FROM daily
        """
    )
    mo.vstack([mo.md("### Season summary"),
               mo.ui.table(q16_summary, selection=None)])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Part 5 -- Extra: the fleet mix

    The four tiers above are the 16 queries the assignment asks for. This last
    one is an extra, kept separate so the counts stay easy to audit.

    ## Q17. What share of bookings goes to each boat colour?

    Two things worth noticing in the SQL. First, the denominator: a window
    function (`sum(...) OVER ()`) computes the grand total alongside each
    group, so the percentage needs no second pass over the table and no
    subquery. Second, this is an *inner* join on purpose -- a colour nobody has
    ever booked contributes nothing to a share of bookings, so unlike most
    questions in this notebook the absent rows genuinely should be dropped.

    A pie is the right chart here and almost nowhere else: the slices are parts
    of one whole. Every reservation is on exactly one boat, which has exactly
    one colour, so the counts add up to every booking ever made. Compare
    magnitudes across many categories and a bar chart wins -- Q9 is that chart.
    """)
    return


@app.cell
def _(plots, run):
    q17 = run(
        """
        SELECT b.color,
               count(*)                                        AS n_reservations,
               100.0 * count(*) / sum(count(*)) OVER ()        AS pct
        FROM reserves r
        JOIN boats b ON b.bid = r.bid
        GROUP BY b.color
        ORDER BY n_reservations DESC, b.color
        """
    )
    plots.plot_bookings_by_colour(q17)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Part 6 -- Lesson: naming a column, and then referring to it

    This one came out of a real mistake. A query aliased a column and then
    sorted by that alias **qualified with the table name**:

    ```sql
    SELECT or2.prev_day AS from_day     -- 'from_day' is invented here
    FROM   ordered_reserves or2
    ORDER BY or2.from_day               -- ...and asked for as a column of or2
    ```

    ```
    Binder Error: Values list "or2" does not have a column named "from_day"
    ```

    ## The rule

    An alias in the `SELECT` list names a column **of the result**. It does not
    add a column to any table in the `FROM` clause. So:

    * **`ORDER BY from_day`** -- fine. You are naming a column of the result.
    * **`ORDER BY or2.from_day`** -- always wrong. Writing `or2.` means "the
      column `from_day` belonging to `or2`", and `or2` has `prev_day`. The
      qualification is the entire bug; drop it and the same query runs.

    The moment you write a table prefix you have stopped talking about the
    result and started talking about the table. Two ways to fix it: use the
    alias bare, or repeat the real column (`ORDER BY or2.prev_day`).

    ## Where can an alias be used?

    Run the next cell. It tries the same alias in every clause and reports what
    DuckDB does -- worth running rather than memorising, because **DuckDB is
    more permissive here than most databases.**

    In textbook SQL the clauses are evaluated `FROM -> WHERE -> GROUP BY ->
    HAVING -> SELECT -> ORDER BY`, so only `ORDER BY` -- which runs after
    `SELECT` -- can see an alias, and `WHERE` cannot. DuckDB relaxes that and
    resolves an unqualified alias in every clause. Postgres and SQL Server do
    not: `WHERE r > 5` against `SELECT rating AS r` is an error there. So code
    that relies on the leniency is not portable, while `or2.from_day` is
    invalid *everywhere* -- including DuckDB.
    """)
    return


@app.cell
def _(mo, pd, run):
    alias_cases = [
        ("SELECT defines the alias",   "SELECT s.rating AS r FROM sailors s"),
        ("WHERE r > 5",                "SELECT s.rating AS r FROM sailors s WHERE r > 5"),
        ("GROUP BY r",                 "SELECT s.rating AS r, count(*) AS n "
                                       "FROM sailors s GROUP BY r"),
        ("HAVING n > 1",               "SELECT s.rating AS r, count(*) AS n "
                                       "FROM sailors s GROUP BY s.rating HAVING n > 1"),
        ("ORDER BY r",                 "SELECT s.rating AS r FROM sailors s ORDER BY r"),
        ("ORDER BY s.r  (qualified)",  "SELECT s.rating AS r FROM sailors s ORDER BY s.r"),
        ("ORDER BY s.rating (column)", "SELECT s.rating AS r FROM sailors s ORDER BY s.rating"),
    ]

    alias_results = []
    for where_used, stmt in alias_cases:
        try:
            run(stmt)
            verdict, detail = "works", ""
        except Exception as exc:                      # noqa: BLE001 - the error IS the lesson
            verdict = "ERROR"
            detail = str(exc).strip().splitlines()[0]
        alias_results.append({"alias used in": where_used,
                              "DuckDB": verdict, "message": detail})

    q18 = pd.DataFrame(alias_results)
    mo.ui.table(q18, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    One row fails, and it is the qualified one. Read the message literally --
    *"Table `s` does not have a column named `r`"* -- and it is telling you
    exactly the truth: `r` is a name on the output, and you asked the table for
    it.

    **The habit to build:** qualify real columns (`s.rating`), never aliases
    (`r`, not `s.r`). If you find yourself writing a table prefix in front of a
    name you invented one line earlier, that is the bug.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Part 7 -- The classic exercise set

    The twelve questions that come up in every version of this schema. Two of
    them are already answered in full earlier in this notebook, so they are
    cross-referenced rather than repeated:

    | # | question | where |
    |---|---|---|
    | 1 | reserved **all** boats | Q19 |
    | 2 | reserved **all red** boats | **Q14** (relational division, two formulations) |
    | 3 | reserved at least **two** boats | Q20 |
    | 4 | names who reserved **a red** boat | **Q4** (three-table join) |
    | 5 | names who reserved **at least one** boat | Q21 |
    | 6 | ages of sailors whose name begins **and** ends with B, >= 3 chars | Q22 |
    | 7 | reserved a red **and** a green boat | Q23 |
    | 8 | sids who reserved red **but not** green | Q24 |
    | 9 | sailors with the **highest rating** | Q25 |
    | 10 | name of the **oldest** sailor | Q26 |
    | 11 | count of **different** sailor names | Q27 |
    | 12 | sailors old enough to vote (> 18) **per rating level** | Q28 |

    Several of these have a trap in them, and the traps are the reason they
    are classics. Each one is called out where it bites.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q19. Sailors who have reserved *all* boats

    Relational division again, but over the **whole fleet** rather than the
    red boats of Q14. Read the `NOT EXISTS (… EXCEPT …)` as: *there is no boat
    that this sailor is missing.*

    **Nobody qualifies over the whole fleet, and that is the correct answer.**
    Five boats (105-109) have never been reserved by anybody, so no sailor can
    hold all nine. Division answers "empty" far more often than students
    expect, and the useful instinct is to ask *which* element is missing
    rather than to assume the query is broken.

    So the query runs the same division twice, against two different divisors,
    and the second one -- the tutorial's original four boats -- finds Dustin.
    Same shape, smaller divisor, completely different answer.

    Note the `LEFT JOIN` at the end. Without it the "all 9 boats" row would
    not appear at all, and an empty answer would look identical to a question
    nobody asked. Making "zero" visible is the point.
    """)
    return


@app.cell
def _(mo, run):
    q19 = run(
        """
        WITH divisors AS (
            -- two different "all": the whole fleet, and the tutorial's four
            SELECT 'all 9 boats'        AS divisor, bid FROM boats
            UNION ALL
            SELECT 'boats 101-104 only' AS divisor, bid FROM boats WHERE bid <= 104
        ),
        labels AS (SELECT DISTINCT divisor FROM divisors),
        qualifying AS (
            SELECT l.divisor, s.sid, s.sname
            FROM labels l
            CROSS JOIN sailors s
            WHERE NOT EXISTS (          -- no boat in this divisor is missing
                SELECT d.bid FROM divisors d WHERE d.divisor = l.divisor
                EXCEPT
                SELECT r.bid FROM reserves r WHERE r.sid = s.sid
            )
        )
        -- LEFT JOIN so the divisor with NO qualifying sailor still shows a row
        SELECT l.divisor,
               count(q.sid) AS n_sailors,
               coalesce(string_agg(q.sname, ', ' ORDER BY q.sid), '(none)') AS who
        FROM labels l
        LEFT JOIN qualifying q ON q.divisor = l.divisor
        GROUP BY l.divisor
        ORDER BY l.divisor
        """
    )
    mo.ui.table(q19, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q20. Sailors who have reserved at least two boats

    `HAVING` filters groups, so "at least two" is a condition on the count.

    **The trap is `count(DISTINCT r.bid)` versus `count(*)`.** They differ the
    moment a sailor books the same boat on two different days -- which is
    legal, and which Lubber and Dustin both do. `count(*)` would answer "at
    least two *bookings*"; the question asks for two *boats*.

    Group by `s.sid`, never by `s.sname`: the two Horatios would otherwise be
    merged into one group of three bookings and wrongly qualify.
    """)
    return


@app.cell
def _(mo, run):
    q20 = run(
        """
        SELECT s.sid, s.sname,
               count(DISTINCT r.bid) AS n_boats,
               count(*)              AS n_bookings
        FROM sailors  s
        JOIN reserves r ON r.sid = s.sid
        GROUP BY s.sid, s.sname
        HAVING count(DISTINCT r.bid) >= 2
        ORDER BY n_boats DESC, s.sid
        """
    )
    mo.ui.table(q20, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q21. Sailors who have reserved at least one boat

    The mirror of Q8's outer join: `EXISTS` keeps the sailors who *do* appear
    in `reserves`, where Q8 keeps everybody and shows the gaps.

    Note what `DISTINCT sname` costs here. Both Horatios have booked -- 64 has
    two boats, 74 has one -- but they share a name, so asking for *names*
    returns three rows where asking for sailors returns four. The `sid` column
    is included to make that visible; drop it and the duplicate disappears
    silently.
    """)
    return


@app.cell
def _(mo, run):
    q21 = run(
        """
        SELECT s.sid, s.sname
        FROM sailors s
        WHERE EXISTS (SELECT 1 FROM reserves r WHERE r.sid = s.sid)
        ORDER BY s.sname, s.sid
        """
    )
    mo.ui.table(q21, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q22. Ages of sailors whose name begins and ends with B (>= 3 characters)

    Three conditions, `AND`-ed: `LIKE 'B%'`, `LIKE '%B'`, and
    `length(sname) >= 3`. The length test is what stops the single character
    `'B'` from satisfying both patterns at once.

    **The trap is case.** Read literally, "begins and ends with B" is
    case-sensitive, and in this data it matches **nothing** -- `'Bob'` ends in
    a lower-case `b`. Both readings are below so the difference is visible.
    Real answer to give: state the assumption. `lower(sname) LIKE '%b'` finds
    Bob, age 63.5.
    """)
    return


@app.cell
def _(mo, run):
    q22 = run(
        """
        SELECT 'case-sensitive (literal reading)' AS reading, sname, age
        FROM sailors
        WHERE sname LIKE 'B%' AND sname LIKE '%B' AND length(sname) >= 3
        UNION ALL
        SELECT 'case-insensitive',                            sname, age
        FROM sailors
        WHERE lower(sname) LIKE 'b%' AND lower(sname) LIKE '%b'
          AND length(sname) >= 3
        ORDER BY reading, sname
        """
    )
    mo.ui.table(q22, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q23. Sailors who have reserved a red *and* a green boat

    **The trap is writing `WHERE b.color = 'red' AND b.color = 'green'`**,
    which asks one row to be two colours and returns nothing. "Red and green"
    is a condition on the *sailor*, not on a row, so it needs two independent
    lookups -- two `EXISTS` clauses, or `INTERSECT`, or a `GROUP BY` with
    `HAVING count(DISTINCT color) = 2`.

    Both spellings are shown; they agree on Dustin and Lubber. Contrast with
    Q4, where "a red boat" is a single-row condition and one `WHERE` suffices.
    """)
    return


@app.cell
def _(mo, run):
    q23 = run(
        """
        WITH by_exists AS (
            SELECT s.sid, s.sname, 'EXISTS x2' AS style
            FROM sailors s
            WHERE EXISTS (SELECT 1 FROM reserves r JOIN boats b ON b.bid = r.bid
                          WHERE r.sid = s.sid AND b.color = 'red')
              AND EXISTS (SELECT 1 FROM reserves r JOIN boats b ON b.bid = r.bid
                          WHERE r.sid = s.sid AND b.color = 'green')
        ),
        by_having AS (
            SELECT s.sid, s.sname, 'GROUP BY/HAVING' AS style
            FROM sailors  s
            JOIN reserves r ON r.sid = s.sid
            JOIN boats    b ON b.bid = r.bid
            WHERE b.color IN ('red', 'green')
            GROUP BY s.sid, s.sname
            HAVING count(DISTINCT b.color) = 2
        )
        SELECT * FROM by_exists
        UNION ALL SELECT * FROM by_having
        ORDER BY sid, style
        """
    )
    mo.ui.table(q23, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q24. Sids of sailors who reserved red boats but *not* green ones

    `EXCEPT` is set difference, and it is the cleanest way to say "but not".
    The left side collects everyone who took a red boat, the right side
    everyone who took a green one, and the subtraction leaves Horatio (64).

    Two things `EXCEPT` does for free: it de-duplicates (no `DISTINCT`
    needed), and it compares whole rows, so both sides must project the same
    columns in the same order. The `NOT IN` spelling below agrees -- but note
    it would break if the inner query could return `NULL`, because
    `x NOT IN (1, NULL)` is never true. Here `sid` is `NOT NULL`, so it is
    safe; that is a property of the schema, not of the query.
    """)
    return


@app.cell
def _(mo, run):
    q24 = run(
        """
        WITH by_except AS (
            SELECT r.sid FROM reserves r JOIN boats b ON b.bid = r.bid
            WHERE b.color = 'red'
            EXCEPT
            SELECT r.sid FROM reserves r JOIN boats b ON b.bid = r.bid
            WHERE b.color = 'green'
        )
        SELECT e.sid, s.sname,
               (e.sid IN (
                   SELECT r.sid FROM reserves r JOIN boats b ON b.bid = r.bid
                   WHERE b.color = 'red'
                     AND r.sid NOT IN (
                         SELECT r2.sid FROM reserves r2 JOIN boats b2 ON b2.bid = r2.bid
                         WHERE b2.color = 'green')
               )) AS agrees_with_not_in
        FROM by_except e
        JOIN sailors s ON s.sid = e.sid
        ORDER BY e.sid
        """
    )
    mo.ui.table(q24, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q25. The sailors with the highest rating

    **The trap is `ORDER BY rating DESC LIMIT 1`**, which silently picks one
    winner when there is a tie. Two sailors share rating 10 -- Rusty and Zorba
    -- so the honest query compares against a scalar subquery and returns
    both.

    `max(rating)` ignores `NULL`s, so Dan (unrated) neither wins nor breaks
    the comparison; `rating = NULL` would never be true anyway.
    """)
    return


@app.cell
def _(mo, run):
    q25 = run(
        """
        SELECT sid, sname, rating, age
        FROM sailors
        WHERE rating = (SELECT max(rating) FROM sailors)
        ORDER BY sid
        """
    )
    mo.ui.table(q25, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q26. The name of the oldest sailor

    Same shape as Q25, on `age`. Here there is no tie, so `ORDER BY age DESC
    LIMIT 1` would happen to give the right answer today -- and would quietly
    start lying the day two sailors share the maximum. Prefer the subquery
    form when the question says "the oldest", because that phrasing does not
    promise there is only one.
    """)
    return


@app.cell
def _(mo, run):
    q26 = run(
        """
        SELECT sname, age, rating
        FROM sailors
        WHERE age = (SELECT max(age) FROM sailors)
        """
    )
    mo.ui.table(q26, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q27. How many *different* sailor names are there?

    Three counts that a student expects to be equal, and are not:

    * `count(*)` counts rows -- 14 sailors.
    * `count(sname)` counts non-`NULL` values -- also 14, since names are
      `NOT NULL`. Run the same trio on `rating` and it drops to 13, because
      Dan is unrated.
    * `count(DISTINCT sname)` counts values -- **13**, because two different
      sailors are both called Horatio.

    That gap of one is the whole reason `sid` is the key and `sname` is not.
    """)
    return


@app.cell
def _(mo, run):
    q27 = run(
        """
        SELECT count(*)                 AS rows_in_table,
               count(sname)             AS non_null_names,
               count(DISTINCT sname)    AS different_names,
               count(rating)            AS non_null_ratings,
               count(DISTINCT rating)   AS different_ratings
        FROM sailors
        """
    )
    mo.ui.table(q27, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Q28. Sailors old enough to vote (age > 18), per rating level

    `WHERE` before `GROUP BY`: the filter removes rows, then the groups are
    formed from what survives. Writing the age test in `HAVING` instead would
    be wrong here -- `HAVING` runs after grouping, on aggregates.

    Two details worth watching in the output:

    * **Zorba (rating 10, age 16) disappears**, so rating 10 counts 1 rather
      than 2. That is the filter doing its job.
    * **`NULL` forms its own group.** Dan is 48 and unrated, so he is a voter
      with no rating level. `GROUP BY` treats all `NULL`s as one group even
      though `NULL = NULL` is not true -- grouping uses "not distinct from",
      not `=`. Decide deliberately whether that row belongs in the answer.
    """)
    return


@app.cell
def _(mo, run):
    q28 = run(
        """
        SELECT rating,
               count(*)          AS n_voters,
               round(avg(age), 1) AS avg_age
        FROM sailors
        WHERE age > 18
        GROUP BY rating
        ORDER BY rating NULLS LAST
        """
    )
    mo.ui.table(q28, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Where to go next

    * `DESIGN.md` -- why `reserves` is keyed on `(bid, day)` and why
      `UNIQUE (sid, bid, day)` would add nothing.
    * `uv run python src/build_database.py --verify` -- watch the database
      reject each forbidden row in turn.
    * `uv run streamlit run app/streamlit_app.py` -- the same rules, behind
      registration and booking forms.
    """)
    return


if __name__ == "__main__":
    app.run()
