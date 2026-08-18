"""OMIS 105 -- Sailors & Boats: the marina front desk.

Run it with:
    uv run streamlit run app/streamlit_app.py

Every write goes through src/sailors_db.py, and every rule is enforced by the
DuckDB schema underneath it. The app never decides whether a booking is legal;
it asks the database and reports the answer.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import plots  # noqa: E402
import sailors_db as sdb  # noqa: E402
import text_to_sql as t2s  # noqa: E402

st.set_page_config(page_title="Sailors & Boats -- Marina Desk", page_icon="⛵",
                   layout="wide")

SEASON_DEFAULT = dt.date(1998, 10, 10)   # a day with bookings, so views open non-empty


# ---------------------------------------------------------------------------
# Data access
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def get_con():
    """The app's single DuckDB connection, reused across reruns.

    It is writable, and reads go through it too. Within one process DuckDB
    refuses to open the same file twice with different settings, so a
    read-only handle plus a writable handle is not an option -- one
    connection does both jobs.
    """
    return sdb.connect(read_only=False)


def bump():
    """Force a rerun after a write so every panel reflects the new state."""
    st.rerun()


def flash(kind: str, msg: str, sql: str | None = None) -> None:
    """Queue a message (and optionally the SQL that ran) for after the rerun.

    A successful write triggers st.rerun(), which wipes the page before the
    user could read anything -- so both the confirmation and the statement have
    to survive in session_state and be rendered on the next pass.
    """
    st.session_state["_flash"] = (kind, msg, sql)


def show_flash() -> None:
    if "_flash" not in st.session_state:
        return
    kind, msg, sql = st.session_state.pop("_flash")
    getattr(st, kind)(msg)
    if sql:
        sql_panel(sql, label="Show the SQL that just ran")


def sql_enabled() -> bool:
    """Whether the teaching panels are switched on (sidebar toggle)."""
    return st.session_state.get("show_sql", True)


def sql_panel(sql, params=None, label: str = "Show SQL", note: str | None = None) -> None:
    """Collapsed panel showing the statement that produced what is above it.

    Collapsed by default and hidden entirely by the sidebar toggle, so the app
    stays usable as an app; expanded, it is the lesson. `sql` may be a string
    or an SqlLog holding several statements.

    Everything shown here is the SQL that actually executed -- the pages pass
    the same variable they handed to the database, and the write helpers record
    their own statements. Nothing is retyped for display, so the panel cannot
    drift away from the truth.
    """
    if not sql_enabled():
        return
    text = sql.rendered() if isinstance(sql, sdb.SqlLog) else sdb.format_sql(sql, params)
    if not text.strip():
        return
    with st.expander(label, expanded=False):
        if note:
            st.caption(note)
        st.code(text, language="sql")


def sailor_options(con, only_sids: list[int] | None = None) -> dict[str, int]:
    df = sdb.all_sailors(con)
    if only_sids is not None:
        df = df[df["sid"].isin(only_sids)]
    return {f"{r.sid} -- {r.sname}"
            + (f" (rating {int(r.rating)})" if pd.notna(r.rating) else " (unrated)"): int(r.sid)
            for r in df.itertuples()}


def boat_options(con, only_bids: list[int] | None = None) -> dict[str, int]:
    df = sdb.all_boats(con)
    if only_bids is not None:
        df = df[df["bid"].isin(only_bids)]
    return {f"{r.bid} -- {r.bname} ({r.color})": int(r.bid) for r in df.itertuples()}


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def page_dashboard(con) -> None:
    st.header("Marina at a glance")

    kpi_sql = """
        SELECT (SELECT count(*) FROM sailors)                       AS sailors,
               (SELECT count(*) FROM boats)                         AS boats,
               (SELECT count(*) FROM reserves)                      AS reservations,
               (SELECT count(*) FROM sailors s
                 WHERE NOT EXISTS (SELECT 1 FROM reserves r WHERE r.sid = s.sid)) AS idle_sailors,
               (SELECT count(*) FROM boats b
                 WHERE NOT EXISTS (SELECT 1 FROM reserves r WHERE r.bid = b.bid)) AS unbooked_boats
    """
    kpi = con.execute(kpi_sql).fetchone()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Sailors", kpi[0])
    c2.metric("Boats", kpi[1])
    c3.metric("Reservations", kpi[2])
    c4.metric("Sailors who never booked", kpi[3])
    c5.metric("Boats never booked", kpi[4])
    sql_panel(kpi_sql, label="Show SQL — the five numbers above",
              note="Five scalar subqueries in one SELECT, so the whole strip of "
                   "metrics costs a single round trip to the database.")

    # One item per row, full width. This is a teaching dashboard, not an
    # operations dashboard: side-by-side charts save screen space but halve the
    # size of every chart and push each SQL panel away from the thing it
    # explains. Stacked, each query sits directly under its own result.
    st.divider()

    per_boat_sql = """
        SELECT b.bid, b.bname, b.color, count(r.day) AS n_reservations
        FROM boats b
        LEFT JOIN reserves r ON r.bid = b.bid
        GROUP BY b.bid, b.bname, b.color
        ORDER BY n_reservations DESC, b.bid
    """
    per_boat = sdb.q(con, per_boat_sql)
    st.altair_chart(plots.plot_reservations_per_boat(per_boat), width="stretch")
    sql_panel(per_boat_sql, label="Show SQL — reservations per boat",
              note="LEFT JOIN, so boats with no reservations stay in the result at "
                   "zero. count(r.day) counts matches; count(*) would count the "
                   "unmatched rows too and report 1 for every idle boat.")

    st.divider()

    by_month_sql = """
        SELECT date_trunc('month', day)::DATE AS month_start,
               count(*)                       AS n_reservations
        FROM reserves
        GROUP BY 1
        ORDER BY 1
    """
    by_month = sdb.q(con, by_month_sql)
    if by_month.empty:
        st.info("Bookings by month — no reservations yet.")
    else:
        st.altair_chart(plots.plot_reservations_by_month(by_month), width="stretch")
    sql_panel(by_month_sql, label="Show SQL — bookings by month",
              note="date_trunc snaps every date down to the first of its month, "
                   "giving a column to group on. Swap 'month' for 'week' and "
                   "nothing else changes.")

    st.divider()

    cal_sql = """
        SELECT r.day, r.bid, r.bid || ' ' || b.bname AS boat_label, r.sid, s.sname
        FROM reserves r
        JOIN boats   b ON b.bid = r.bid
        JOIN sailors s ON s.sid = r.sid
        ORDER BY r.day, r.bid
    """
    cal = sdb.q(con, cal_sql)
    if cal.empty:
        st.info("Fleet calendar — nothing booked yet.")
    else:
        st.altair_chart(plots.plot_fleet_calendar(cal), width="stretch")
        st.caption("Each cell holds at most one sailor (PRIMARY KEY (bid, day)), "
                   "and no name repeats within a column (UNIQUE (sid, day)).")
    sql_panel(cal_sql, label="Show SQL — the fleet calendar",
              note="The full three-table path: sailors -> reserves -> boats. "
                   "reserves is the bridge; there is no way from a sailor to a "
                   "boat that does not go through it.")


def page_register_sailor(con) -> None:
    st.header("Sailor registration")
    st.caption("R6: every sailor is unique. `sid` is the primary key; "
               "names are not, which is why two sailors can both be called Horatio.")

    with st.form("sailor_form", clear_on_submit=True):
        c1, c2 = st.columns([2, 1])
        sname = c1.text_input("Name *", placeholder="e.g. Ahab")
        auto_id = c2.checkbox("Auto-assign sid", value=True,
                              help="Auto ids come from seq_sid and start at 1000.")
        manual_sid = c2.number_input("sid", min_value=1, max_value=999_999, value=1000,
                                     step=1, disabled=auto_id)

        c3, c4 = st.columns(2)
        unrated = c3.checkbox("Unrated (rating IS NULL)", value=False,
                              help="Like sailor 99 'Dan' in the tutorial.")
        rating = c3.slider("Rating", 1, 10, 5, disabled=unrated)
        age = c4.number_input("Age", min_value=0.0, max_value=120.0, value=30.0, step=0.5,
                              help="REAL, so half-years like 55.5 are exact.")

        if st.form_submit_button("Register sailor", type="primary"):
            try:
                log = sdb.SqlLog()
                new_sid = sdb.register_sailor(
                    con=con,
                    log=log,
                    sname=sname,
                    rating=None if unrated else int(rating),
                    age=float(age),
                    sid=None if auto_id else int(manual_sid),
                )
                flash("success", f"Registered **{sname.strip()}** as sailor **{new_sid}**.",
                      sql=log.rendered())
                bump()
            except sdb.BusinessRuleError as exc:
                st.error(str(exc))
            except Exception as exc:  # a constraint the pre-flight checks missed
                st.error(f"The database rejected this sailor: {exc}")

    st.subheader("Current crew")
    crew_sql = """
        SELECT s.sid, s.sname, s.rating, s.age,
               count(r.bid) AS reservations
        FROM sailors s
        LEFT JOIN reserves r ON r.sid = s.sid
        GROUP BY s.sid, s.sname, s.rating, s.age
        ORDER BY s.sid
    """
    st.dataframe(sdb.q(con, crew_sql), hide_index=True)
    sql_panel(crew_sql, label="Show SQL — the crew list")


def page_register_boat(con) -> None:
    st.header("Boat registration")
    st.caption("R7: every boat is unique. `bid` is the primary key -- "
               "boats 101 and 102 are both 'Interlake' and are still two different hulls.")

    with st.form("boat_form", clear_on_submit=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        bname = c1.text_input("Boat name *", placeholder="e.g. Pequod")
        color = c2.selectbox("Colour *", sdb.VALID_COLORS)
        auto_id = c3.checkbox("Auto-assign bid", value=True,
                              help="Auto ids come from seq_bid and start at 1000.")
        manual_bid = c3.number_input("bid", min_value=1, max_value=999_999, value=1000,
                                     step=1, disabled=auto_id)

        if st.form_submit_button("Register boat", type="primary"):
            try:
                log = sdb.SqlLog()
                new_bid = sdb.register_boat(
                    con=con,
                    log=log,
                    bname=bname, color=color,
                    bid=None if auto_id else int(manual_bid),
                )
                flash("success", f"Registered **{bname.strip()}** as boat **{new_bid}**.",
                      sql=log.rendered())
                bump()
            except sdb.BusinessRuleError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"The database rejected this boat: {exc}")

    st.subheader("Current fleet")
    fleet_sql = """
        SELECT b.bid, b.bname, b.color,
               count(r.day) AS reservations,
               min(r.day)   AS first_booked,
               max(r.day)   AS last_booked
        FROM boats b
        LEFT JOIN reserves r ON r.bid = b.bid
        GROUP BY b.bid, b.bname, b.color
        ORDER BY b.bid
    """
    st.dataframe(sdb.q(con, fleet_sql), hide_index=True)
    sql_panel(fleet_sql, label="Show SQL — the fleet list")


def page_reservations(con) -> None:
    st.header("Reservation system")
    st.caption("R2, R3, R4 and R8 from `PRIMARY KEY (bid, day)` -- one boat, "
               "one day, one sailor. R10 from `UNIQUE (sid, day)` -- and one "
               "sailor, one day, one boat.")

    book_tab, cancel_tab = st.tabs(["Make a reservation", "Cancel a reservation"])

    with book_tab:
        day = st.date_input("Date", value=SEASON_DEFAULT, key="book_day",
                            format="YYYY-MM-DD",
                            help="Stored as DATE, printed as YYYY-MM-DD (R5).")

        free_log, taken_log, idle_log = sdb.SqlLog(), sdb.SqlLog(), sdb.SqlLog()
        free = sdb.available_boats_on(con, day, log=free_log)
        taken = sdb.reservations_on(con, day, log=taken_log)
        idle = sdb.free_sailors_on(con, day, log=idle_log)

        c1, c2, c3 = st.columns(3)
        c1.metric(f"Boats free on {day}", len(free))
        c2.metric("Boats already out", len(taken))
        c3.metric("Sailors still free", len(idle))

        if free.empty:
            st.warning(f"Every boat is already reserved on {day}. "
                       "Pick another date, or cancel a booking first.")
        elif idle.empty:
            st.warning(f"Every sailor is already out on {day}. Boats are free, "
                       "but R10 gives each sailor one boat a day.")
        else:
            sailors = sailor_options(con, only_sids=idle["sid"].tolist())
            boats = boat_options(con, only_bids=free["bid"].tolist())

            with st.form("reserve_form"):
                cc1, cc2 = st.columns(2)
                sailor_label = cc1.selectbox(
                    "Sailor (only sailors free that day are listed)", list(sailors))
                boat_label = cc2.selectbox("Boat (only boats free that day are listed)",
                                           list(boats))
                if st.form_submit_button("Reserve", type="primary"):
                    try:
                        log = sdb.SqlLog()
                        sdb.make_reservation(sailors[sailor_label], boats[boat_label],
                                             day, con=con, log=log)
                        flash("success",
                              f"Reserved **{boat_label}** for **{sailor_label}** on **{day}**.",
                              sql=log.rendered())
                        bump()
                    except sdb.BusinessRuleError as exc:
                        st.error(str(exc))
                    except Exception as exc:
                        st.error(f"The database rejected this reservation: {exc}")

        st.subheader(f"Already out on {day}")
        if taken.empty:
            st.info("Nothing booked on this date -- the whole fleet is available.")
        else:
            st.dataframe(taken, hide_index=True)
        sql_panel(taken_log, label="Show SQL — what is already out")

        with st.expander("Boats free on this date"):
            st.dataframe(free, hide_index=True)
        sql_panel(free_log, label="Show SQL — which boats are free",
                  note="NOT EXISTS is the whole availability rule. Because "
                       "(bid, day) is the primary key, a boat is either in "
                       "reserves for that day or it is free -- never both.")

        with st.expander("Sailors free on this date"):
            st.dataframe(idle, hide_index=True)
        sql_panel(idle_log, label="Show SQL — which sailors are free",
                  note="The same query with sid in place of bid. That symmetry "
                       "is the point: UNIQUE (sid, day) constrains sailors "
                       "exactly the way the primary key constrains boats, so "
                       "'who is free' is one NOT EXISTS on either side.")

    with cancel_tab:
        st.caption("A reservation is identified by the slot it occupies: (bid, day).")
        current = sdb.all_reservations(con)
        if current.empty:
            st.info("There is nothing to cancel.")
        else:
            labels = {
                f"{r.day}  --  boat {r.bid} {r.bname} ({r.color})  --  {r.sname} ({r.sid})":
                    (int(r.bid), r.day)
                for r in current.itertuples()
            }
            choice = st.selectbox("Reservation", list(labels), key="cancel_choice")
            if st.button("Cancel this reservation", type="secondary"):
                bid, day_val = labels[choice]
                day_val = pd.Timestamp(day_val).date()
                log = sdb.SqlLog()
                removed = sdb.cancel_reservation(bid, day_val, con=con, log=log)
                if removed:
                    flash("success", f"Released boat **{bid}** on **{day_val}**.",
                          sql=log.rendered())
                else:
                    flash("warning", "That reservation was already gone.", sql=log.rendered())
                bump()

            st.dataframe(current, hide_index=True)


def page_day_view(con) -> None:
    st.header("Register for a day")
    day = st.date_input("Date", value=SEASON_DEFAULT, key="view_day", format="YYYY-MM-DD")

    rows_log, free_log = sdb.SqlLog(), sdb.SqlLog()
    rows = sdb.reservations_on(con, day, log=rows_log)
    free = sdb.available_boats_on(con, day, log=free_log)
    total_boats = len(sdb.all_boats(con))

    c1, c2, c3 = st.columns(3)
    c1.metric("Boats out", len(rows))
    c2.metric("Boats free", len(free))
    c3.metric("Fleet utilisation", f"{(100 * len(rows) / total_boats) if total_boats else 0:.0f}%")

    st.subheader(f"Out on {day}")
    if rows.empty:
        st.info(f"No reservations on {day}.")
    else:
        st.dataframe(rows, hide_index=True)

    sql_panel(rows_log, label="Show SQL — who is out")

    st.subheader(f"Free on {day}")
    st.dataframe(free, hide_index=True)
    sql_panel(free_log, label="Show SQL — what is free")

    st.caption("Note that the two tables are complements: a boat is either out "
               "or free that day, never both, and never out twice.")


def page_range_view(con) -> None:
    st.header("Register for a date range")

    bounds = con.execute("SELECT min(day), max(day) FROM reserves").fetchone()
    lo = bounds[0] or dt.date(1998, 9, 1)
    hi = bounds[1] or dt.date(1998, 11, 30)

    c1, c2 = st.columns(2)
    start = c1.date_input("From", value=lo, key="range_start", format="YYYY-MM-DD")
    end = c2.date_input("To", value=hi, key="range_end", format="YYYY-MM-DD")
    if start > end:
        st.warning("The start date is after the end date -- showing the range reversed.")
        start, end = end, start

    rows_log = sdb.SqlLog()
    rows = sdb.reservations_between(con, start, end, log=rows_log)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Reservations", len(rows))
    m2.metric("Distinct boats", rows["bid"].nunique() if not rows.empty else 0)
    m3.metric("Distinct sailors", rows["sid"].nunique() if not rows.empty else 0)
    m4.metric("Days in range", (end - start).days + 1)

    if rows.empty:
        st.info("No reservations in this range.")
        return

    st.dataframe(rows, hide_index=True)
    sql_panel(rows_log, label="Show SQL — bookings in this range")

    st.subheader("Day by day, including the quiet days")
    daily_sql = """
        WITH calendar AS (
            SELECT unnest(generate_series(?::DATE, ?::DATE, INTERVAL 1 DAY))::DATE AS day
        )
        SELECT c.day,
               strftime(c.day, '%a')                                        AS weekday,
               count(r.bid)                                                 AS boats_out,
               count(DISTINCT r.sid)                                        AS sailors_out,
               round(100.0 * count(r.bid) / (SELECT count(*) FROM boats), 1) AS pct_fleet_out,
               string_agg(DISTINCT s.sname, ', ' ORDER BY s.sname)          AS who
        FROM calendar c
        LEFT JOIN reserves r ON r.day = c.day
        LEFT JOIN sailors  s ON s.sid = r.sid
        GROUP BY c.day
        ORDER BY c.day
    """
    daily = sdb.q(con, daily_sql, [start, end])
    st.dataframe(daily, hide_index=True)
    sql_panel(daily_sql, [start, end], label="Show SQL — the day-by-day calendar",
              note="generate_series manufactures every date in the window, then "
                   "LEFT JOIN attaches the bookings. The database stores no row "
                   "for a quiet day, so without the spine those rows cannot exist.")
    st.caption("The zero rows only exist because the query builds a calendar spine "
               "with `generate_series` -- the database stores no row for a quiet day.")

    st.download_button(
        "Download this range as CSV",
        data=rows.to_csv(index=False).encode(),
        file_name=f"reservations_{start}_{end}.csv",
        mime="text/csv",
    )


def page_availability(con) -> None:
    st.header("Find a free boat")
    st.caption("Pick a boat and a window; the app lists every date in that window "
               "on which the boat is not already out.")

    boats = boat_options(con)
    c1, c2, c3 = st.columns(3)
    boat_label = c1.selectbox("Boat", list(boats))
    start = c2.date_input("From", value=dt.date(1998, 9, 1), key="avail_from", format="YYYY-MM-DD")
    end = c3.date_input("To", value=dt.date(1998, 11, 30), key="avail_to", format="YYYY-MM-DD")
    if start > end:
        start, end = end, start

    bid = boats[boat_label]
    avail_sql = """
        WITH calendar AS (
            SELECT unnest(generate_series(?::DATE, ?::DATE, INTERVAL 1 DAY))::DATE AS day
        )
        SELECT c.day,
               strftime(c.day, '%a')                    AS weekday,
               (r.bid IS NULL)                          AS is_free,
               s.sname                                  AS held_by
        FROM calendar c
        LEFT JOIN reserves r ON r.day = c.day AND r.bid = ?
        LEFT JOIN sailors  s ON s.sid = r.sid
        ORDER BY c.day
    """
    df = sdb.q(con, avail_sql, [start, end, bid])

    free_days = int(df["is_free"].sum())
    c1, c2 = st.columns(2)
    c1.metric("Free days", free_days)
    c2.metric("Booked days", len(df) - free_days)

    only_free = st.toggle("Show free days only", value=True)
    st.dataframe(df[df["is_free"]] if only_free else df, hide_index=True)
    st.caption("'Free' here means the *boat* is free. R10 is the other "
               "half: a sailor already out on one of these days still cannot take "
               "it. The reservation page filters both sides.")
    sql_panel(avail_sql, [start, end, bid],
              label="Show SQL — this boat's calendar",
              note="The join condition carries the boat id, so the LEFT JOIN keeps "
                   "every date and only attaches a row where THIS boat is booked. "
                   "Putting `r.bid = ?` in a WHERE clause instead would drop the "
                   "free days -- the exact rows the question is about.")


def page_playground(con) -> None:
    st.header("Constraint playground")
    st.markdown(
        "Try to break the rules. Each button runs a statement the schema should "
        "refuse; the database's own error message comes back verbatim. "
        "Nothing here is committed -- every attempt runs inside a transaction "
        "that is rolled back."
    )

    existing = con.execute(
        "SELECT sid, bid, day FROM reserves ORDER BY day LIMIT 1"
    ).fetchone()
    if existing is None:
        st.info("Add a reservation first, then come back and try to duplicate it.")
        return
    sid0, bid0, day0 = int(existing[0]), int(existing[1]), existing[2]

    other_sailor = con.execute(
        "SELECT sid FROM sailors WHERE sid <> ? ORDER BY sid LIMIT 1", [sid0]
    ).fetchone()[0]

    # A boat with nothing booked on day0. R10 is only convincing with
    # one: if the boat were already taken the primary key would reject the row
    # first, and the student would learn nothing about UNIQUE (sid, day).
    free_boat = con.execute(
        """
        SELECT bid FROM boats b
        WHERE NOT EXISTS (SELECT 1 FROM reserves r WHERE r.bid = b.bid AND r.day = ?)
        ORDER BY bid LIMIT 1
        """,
        [day0],
    ).fetchone()

    attempts = [
        ("R3 -- let a second sailor take the same boat that day",
         "INSERT INTO reserves (sid, bid, day) VALUES (?, ?, ?)",
         [int(other_sailor), bid0, day0]),
        ("R4/R8 -- book the same boat twice for the same date",
         "INSERT INTO reserves (sid, bid, day) VALUES (?, ?, ?)",
         [sid0, bid0, day0]),
        ("R6 -- reuse an existing sailor id",
         "INSERT INTO sailors (sid, sname, rating, age) VALUES (?, 'Impostor', 5, 30.0)",
         [sid0]),
        ("R7 -- reuse an existing boat id",
         "INSERT INTO boats (bid, bname, color) VALUES (?, 'Clone', 'red')",
         [bid0]),
        ("D1 -- reserve for a sailor who does not exist",
         "INSERT INTO reserves (sid, bid, day) VALUES (999999, ?, DATE '1999-01-01')",
         [bid0]),
        ("D2 -- a rating of 11",
         "INSERT INTO sailors (sid, sname, rating, age) VALUES (999999, 'Overachiever', 11, 30.0)",
         []),
        ("D2 -- a boat the colour of chartreuse",
         "INSERT INTO boats (bid, bname, color) VALUES (999999, 'Chartreuse Dream', 'chartreuse')",
         []),
    ]

    if free_boat is not None:
        # Slot it next to the other reserves rules rather than at the end.
        attempts.insert(2, (
            "R10 -- give that sailor a second (free!) boat the same day",
            "INSERT INTO reserves (sid, bid, day) VALUES (?, ?, ?)",
            [sid0, int(free_boat[0]), day0],
        ))

    # Display form comes from sailors_db.format_sql -- one implementation,
    # shared with every other Show SQL panel in the app.

    for i, (label, sql, params) in enumerate(attempts):
        with st.container(border=True):
            st.markdown(f"**{label}**")
            st.code(sdb.format_sql(sql, params), language="sql")
            if st.button("Try it", key=f"attempt_{i}"):
                try:
                    with sdb.writer(con=con) as w:
                        w.execute(sql, params)
                        raise RuntimeError("_rollback_")   # never commit the playground
                except RuntimeError as exc:
                    if "_rollback_" in str(exc):
                        st.error("The database ACCEPTED this row. A constraint is missing!")
                    else:
                        st.exception(exc)
                except Exception as exc:
                    st.success("Rejected, as it should be.")
                    st.code(str(exc).strip().splitlines()[0], language="text")


def _run_readonly(con, sql: str) -> None:
    """Validate, then run, then render. Every query path goes through here."""
    try:
        t2s.validate_select(sql, con)
    except t2s.SqlSafetyError as exc:
        st.error(str(exc))
        return
    try:
        out = sdb.q(con, sql)
    except Exception as exc:
        st.error(str(exc))
        return
    st.success(f"{len(out)} row(s).")
    if out.empty:
        st.caption("The query is valid and returned nothing — often the right answer, "
                   "but check the literals: colours are lower-case, and dates fall "
                   "between 1998-09-05 and 1998-11-12.")
    else:
        st.dataframe(out, hide_index=True)
        st.download_button("Download as CSV", out.to_csv(index=False).encode(),
                           file_name="query_result.csv", mime="text/csv")


def page_ask(con) -> None:
    """Ask a question in English; Claude writes the SQL; you run it."""
    st.header("Ask in English")
    st.caption("Claude writes DuckDB SQL against this exact schema. You see the query "
               "before it runs, and you can edit it.")

    if not t2s.credentials_available():
        st.warning("No Anthropic credential found — this page needs one to generate SQL.")
        st.markdown(
            "Set one and restart the app:\n\n"
            "```bash\n"
            "export ANTHROPIC_API_KEY=sk-ant-...\n"
            "./run_app.sh\n"
            "```\n"
            "The **SQL console** page works without a credential."
        )
        with st.expander("What gets sent to the API"):
            st.caption("Your question, plus the schema brief below. No table rows are "
                       "sent beyond the five sample rows per table shown here.")
            st.code(t2s.build_system_prompt(t2s.harvest(con)), language="markdown")
        return

    examples = [
        "Which sailors have never reserved a boat?",
        "Who had the most reservations in October 1998?",
        "Which red boats were free on 1998-10-10?",
        "Which sailors were not out on 1998-10-10?",
        "For each sailor, how many days passed between their bookings?",
        "Which boats were reserved by more than one different sailor?",
    ]
    picked = st.selectbox("Try an example, or write your own below", ["(write my own)"] + examples)
    default_q = "" if picked == "(write my own)" else picked

    question = st.text_area("Your question", value=default_q, height=80,
                            placeholder="e.g. Which sailors never reserved a red boat?")

    c1, c2 = st.columns([1, 3])
    # Deliberately NOT disabled when the box looks empty. Streamlit commits a
    # text_area on blur, so a user who types and clicks straight through has
    # their first click consumed by the blur while the button is still
    # disabled -- it takes two clicks to submit. Validating on click instead
    # costs nothing and removes that trap.
    go = c1.button("Generate SQL", type="primary")
    effort = c2.select_slider(
        "Effort", options=["low", "medium", "high"], value="medium",
        help="How hard Claude thinks before answering. Medium suits schema-grounded "
             "SQL; raise it for questions needing several joins or window functions.",
    )

    if go and not question.strip():
        st.warning("Type a question first, or pick one of the examples above.")
    elif go:
        with st.spinner("Asking Claude…"):
            try:
                meta = t2s.harvest(con)
                generated = t2s.generate_sql(question, meta, effort=effort)
                st.session_state["_t2s"] = generated
                st.session_state["_t2s_question"] = question
                # A keyed widget reads st.session_state[key] in preference to
                # its `value=` argument on every rerun after the first. So the
                # SQL box must be updated HERE, explicitly. Relying on `value=`
                # left the previous question's SQL on screen underneath the new
                # explanation -- the reader sees the right answer and runs the
                # wrong query, which is the worst shape a bug can take.
                st.session_state["t2s_sql"] = generated.get("sql", "")
            except Exception as exc:
                st.session_state.pop("_t2s", None)
                st.error(f"Could not generate SQL: {exc}")

    result = st.session_state.get("_t2s")
    if not result:
        return

    st.divider()
    st.caption(f"Question: *{st.session_state.get('_t2s_question', '')}*")

    conf = result.get("confidence", "medium")
    badge = {"high": "🟢 high", "medium": "🟡 medium", "low": "🔴 low"}.get(conf, conf)
    st.markdown(f"**Claude's confidence: {badge}**")
    st.write(result.get("explanation", ""))

    for note in result.get("assumptions") or []:
        st.info(f"Assumption: {note}")

    # Editable: the generated SQL is a draft, not a verdict.
    # No `value=` here on purpose -- the keyed widget is driven by
    # st.session_state["t2s_sql"], which the generation step above sets. The
    # setdefault covers a result restored without a matching box value.
    st.session_state.setdefault("t2s_sql", result.get("sql", ""))
    sql = st.text_area("Generated SQL — edit before running if you want",
                       height=190, key="t2s_sql")

    # Bind-check before the user commits to running it. EXPLAIN resolves every
    # table, column and alias without executing, so an invalid query is caught
    # here rather than as a raw database error after a click.
    bind_error = t2s.dry_run(sql, con) if sql.strip() else None

    c_run, c_fix = st.columns([1, 2])
    run_clicked = c_run.button("Run this query", type="primary",
                               disabled=bool(bind_error))

    if bind_error:
        st.error(f"This query will not run: {bind_error}")
        if c_fix.button("Ask Claude to fix it", type="secondary"):
            with st.spinner("Sending the error back to Claude…"):
                try:
                    fixed = t2s.repair_sql(
                        st.session_state.get("_t2s_question", ""), sql,
                        bind_error, t2s.harvest(con), effort=effort)
                    st.session_state["_t2s"] = fixed
                    st.session_state["t2s_sql"] = fixed.get("sql", "")
                    st.session_state["_t2s_repaired"] = True
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not repair it: {exc}")
        st.caption("You can also edit the SQL above by hand — the check re-runs "
                   "as soon as you leave the box.")

    if run_clicked:
        _run_readonly(con, sql)

    if st.session_state.pop("_t2s_repaired", False):
        st.success("Claude revised the query — the corrected SQL is above.")

    usage = result.get("_usage", {})
    if usage:
        cached = usage.get("cache_read_input_tokens", 0)
        written = usage.get("cache_creation_input_tokens", 0)
        note = (f" · {cached:,} read from cache" if cached
                else f" · {written:,} written to cache" if written else "")
        st.caption(
            f"{usage.get('model', '')} · {usage.get('input_tokens', 0):,} in / "
            f"{usage.get('output_tokens', 0):,} out{note}. The schema brief is "
            "identical every time, so it is cached after the first question."
        )


def page_sql(con) -> None:
    st.header("SQL console")
    st.caption("Read-only. Write your own query against sailors, boats and reserves.")

    presets = {
        "Sailors who never reserved anything":
            "SELECT s.*\nFROM sailors s\nWHERE NOT EXISTS (\n"
            "    SELECT 1 FROM reserves r WHERE r.sid = s.sid\n)\nORDER BY s.sid",
        "Boats nobody has ever booked":
            "SELECT b.*\nFROM boats b\nWHERE NOT EXISTS (\n"
            "    SELECT 1 FROM reserves r WHERE r.bid = b.bid\n)\nORDER BY b.bid",
        "Sailors who reserved every red boat (relational division)":
            "SELECT s.sid, s.sname\nFROM sailors s\nWHERE NOT EXISTS (\n"
            "    SELECT b.bid FROM boats b WHERE b.color = 'red'\n"
            "    EXCEPT\n"
            "    SELECT r.bid FROM reserves r WHERE r.sid = s.sid\n)\nORDER BY s.sid",
        "Everyone, with their booking count (LEFT OUTER JOIN)":
            "SELECT s.sid, s.sname, count(r.bid) AS n_reservations\n"
            "FROM sailors s LEFT JOIN reserves r ON r.sid = s.sid\n"
            "GROUP BY s.sid, s.sname\nORDER BY n_reservations DESC, s.sid",
        "Proof that (bid, day) is unique":
            "SELECT bid, day, count(*) AS rows_in_slot\n"
            "FROM reserves\nGROUP BY bid, day\nHAVING count(*) > 1",
        "Proof that (sid, day) is unique -- R10":
            "SELECT sid, day, count(*) AS boats_that_day\n"
            "FROM reserves\nGROUP BY sid, day\nHAVING count(*) > 1",
    }
    preset = st.selectbox("Start from", ["(blank)"] + list(presets))
    default = presets.get(preset, "SELECT * FROM reserves ORDER BY day, bid")

    sql = st.text_area("Query", value=default, height=200, key=f"sql_{preset}")
    if st.button("Run", type="primary"):
        _run_readonly(con, sql)

    with st.expander("Schema reminder"):
        st.code(
            "sailors(sid PK, sname NOT NULL, rating 1..10 or NULL, age REAL)\n"
            "boats  (bid PK, bname NOT NULL, color IN (red, green, blue, white, black, yellow))\n"
            "reserves(sid FK->sailors, bid FK->boats, day DATE,\n"
            "         PRIMARY KEY (bid, day),   -- one boat, one day, one sailor\n"
            "         UNIQUE (sid, day))        -- one sailor, one day, one boat",
            language="text",
        )


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------

PAGES = {
    "Dashboard": page_dashboard,
    "Sailor registration": page_register_sailor,
    "Boat registration": page_register_boat,
    "Reservation system": page_reservations,
    "View a day": page_day_view,
    "View a date range": page_range_view,
    "Boat availability": page_availability,
    "Constraint playground": page_playground,
    "Ask in English": page_ask,
    "SQL console": page_sql,
}


def main() -> None:
    st.sidebar.title("⛵ Marina desk")
    st.sidebar.caption("OMIS 105 -- Sailors & Boats")

    try:
        con = get_con()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()
    except Exception as exc:
        st.error(f"Could not open the database: {exc}\n\n"
                 "If a Marimo notebook has it open, close that first.")
        st.stop()

    choice = st.sidebar.radio("Go to", list(PAGES), label_visibility="collapsed")

    st.sidebar.divider()
    st.sidebar.toggle(
        "Show SQL panels", value=True, key="show_sql",
        help="Reveal the exact statement behind every table, chart and write. "
             "Turn it off for a clean interface.",
    )
    st.sidebar.markdown(
        "**The rules to remember**\n\n"
        "`reserves` is keyed on **(bid, day)**: a boat is a physical object, so "
        "on any given day it is out with at most one sailor. **UNIQUE (sid, day)** "
        "is the mirror rule -- a sailor takes at most one boat a day. Together "
        "they make each day a one-to-one match of sailors to boats."
    )
    st.sidebar.caption(f"Database: `{sdb.DB_PATH.name}`")

    show_flash()
    PAGES[choice](con)


if __name__ == "__main__":
    main()
