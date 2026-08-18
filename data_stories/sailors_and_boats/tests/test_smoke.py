"""End-to-end smoke tests.

    uv run python tests/test_smoke.py

Three things get checked:
  1. every schema constraint rejects what it is supposed to reject;
  2. every write helper in src/sailors_db.py behaves, against a throwaway copy
     of the database, so the real one is never touched;
  3. every Streamlit page renders without raising.

No pytest needed -- this is a plain script so students can run it as-is.
"""

from __future__ import annotations

import datetime as dt
import os
import shutil
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import build_database  # noqa: E402
import sailors_db as sdb  # noqa: E402

PASSED = 0
FAILED = 0


def check(label: str, condition: bool) -> None:
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  ok    {label}")
    else:
        FAILED += 1
        print(f"  FAIL  {label}")


def expect_rejected(label: str, fn) -> None:
    """`fn` must raise -- it is trying to do something the rules forbid."""
    try:
        fn()
    except Exception as exc:
        check(f"{label}  [{type(exc).__name__}]", True)
        return
    check(f"{label}  -- WAS ALLOWED", False)


# ---------------------------------------------------------------------------

def ensure_database() -> None:
    """Build the database if it is missing, but never clobber an existing one.

    Without this the whole suite runs against an empty file and reports
    nonsense. An existing database is left alone -- it may hold rows somebody
    added through the Streamlit app.
    """
    if sdb.DB_PATH.exists():
        return
    print(f"\n[0] {sdb.DB_PATH.name} not found -- building it first")
    build_database.build()


def test_constraints() -> None:
    print("\n[1] Schema constraints")
    ok = build_database.verify()
    check("build_database.verify() passed", ok)


def test_write_helpers() -> None:
    print("\n[2] Write helpers (against a temporary copy)")
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "test.duckdb"
        shutil.copy(sdb.DB_PATH, db)

        # -- registration -----------------------------------------------------
        sid = sdb.register_sailor("Ahab", rating=9, age=52.0, db_path=db)
        check(f"register_sailor auto-assigned sid {sid} (>= 1000)", sid >= 1000)

        bid = sdb.register_boat("Pequod", "black", db_path=db)
        check(f"register_boat auto-assigned bid {bid} (>= 1000)", bid >= 1000)

        unrated = sdb.register_sailor("Ishmael", rating=None, age=28.0, db_path=db)
        con = sdb.connect(db)
        rating = con.execute("SELECT rating FROM sailors WHERE sid = ?", [unrated]).fetchone()[0]
        check("a sailor may be registered unrated (rating IS NULL)", rating is None)
        con.close()

        expect_rejected("duplicate sid is refused",
                        lambda: sdb.register_sailor("Clone", 5, 30.0, sid=22, db_path=db))
        expect_rejected("duplicate bid is refused",
                        lambda: sdb.register_boat("Clone", "red", bid=101, db_path=db))
        expect_rejected("a blank sailor name is refused",
                        lambda: sdb.register_sailor("   ", 5, 30.0, db_path=db))
        expect_rejected("rating 11 is refused",
                        lambda: sdb.register_sailor("Too Good", 11, 30.0, db_path=db))
        expect_rejected("an unlisted colour is refused",
                        lambda: sdb.register_boat("Weird", "chartreuse", db_path=db))

        # -- reservations -----------------------------------------------------
        day = dt.date(1999, 7, 4)
        sdb.make_reservation(sid, bid, day, db_path=db)
        con = sdb.connect(db)
        check("the reservation landed", len(sdb.who_holds(con, bid, day)) == 1)
        con.close()

        expect_rejected("a second sailor cannot take that boat that day",
                        lambda: sdb.make_reservation(22, bid, day, db_path=db))
        expect_rejected("the same sailor cannot re-book that boat that day",
                        lambda: sdb.make_reservation(sid, bid, day, db_path=db))
        expect_rejected("a reservation for an unknown sailor is refused",
                        lambda: sdb.make_reservation(999_999, bid, day, db_path=db))
        expect_rejected("a reservation for an unknown boat is refused",
                        lambda: sdb.make_reservation(sid, 999_999, day, db_path=db))
        # R10. Boat 105 is never reserved, so the primary key has no
        # objection -- only UNIQUE (sid, day) can reject this one.
        expect_rejected("a sailor cannot take a second boat the same day",
                        lambda: sdb.make_reservation(sid, 105, day, db_path=db))

        # legal variations on the same theme
        sdb.make_reservation(22, bid, day + dt.timedelta(days=1), db_path=db)
        check("the same boat on the next day is fine", True)
        sdb.make_reservation(31, 105, day, db_path=db)
        check("a free sailor taking a free boat that day is fine", True)

        # -- cancel -----------------------------------------------------------
        removed = sdb.cancel_reservation(bid, day, db_path=db)
        check("cancel released exactly one slot", removed == 1)
        check("cancelling an empty slot removes nothing",
              sdb.cancel_reservation(bid, day, db_path=db) == 0)
        sdb.make_reservation(22, bid, day, db_path=db)
        check("the freed slot can be taken by somebody else", True)

        # -- reads ------------------------------------------------------------
        con = sdb.connect(db)
        check("reservations_on returns rows for a booked day",
              len(sdb.reservations_on(con, day)) >= 1)
        # Compare against the database, not a hardcoded seed count. These
        # assertions used to read `== 10`, which failed the moment somebody
        # registered a sailor through the app -- the suite cried wolf on a
        # database that was doing exactly what it is for.
        in_window = con.execute(
            "SELECT count(*) FROM reserves WHERE day BETWEEN ? AND ?",
            [dt.date(1998, 9, 1), dt.date(1998, 12, 31)]).fetchone()[0]
        check(f"reservations_between spans a range ({in_window} rows)",
              len(sdb.reservations_between(con, dt.date(1998, 9, 1),
                                           dt.date(1998, 12, 31))) == in_window)
        check("reservations_between tolerates a reversed range",
              len(sdb.reservations_between(con, dt.date(1998, 12, 31),
                                           dt.date(1998, 9, 1))) == in_window)
        n_boats = len(sdb.all_boats(con))
        free = len(sdb.available_boats_on(con, day))
        taken = len(sdb.reservations_on(con, day))
        check(f"free ({free}) + taken ({taken}) == fleet ({n_boats})", free + taken == n_boats)
        # The R10 mirror of the identity above. `taken` serves as the
        # count of busy sailors too: one row per boat out IS one row per sailor
        # out, which is exactly what the two constraints together guarantee.
        n_sailors = len(sdb.all_sailors(con))
        idle = len(sdb.free_sailors_on(con, day))
        check(f"idle ({idle}) + out ({taken}) == crew ({n_sailors})",
              idle + taken == n_sailors)
        con.close()


def test_sql_guard() -> None:
    """The read-only guard for generated SQL: allow reads, refuse everything else."""
    print("\n[3] Text-to-SQL safety guard")
    import text_to_sql as t2s

    con = sdb.connect()   # same settings as the rest of the suite
    try:
        allowed = [
            "SELECT * FROM sailors",
            "WITH t AS (SELECT 1 AS x) SELECT * FROM t",
            "SELECT unnest(generate_series(DATE '1998-09-01', DATE '1998-09-03', INTERVAL 1 DAY))",
        ]
        refused = [
            "DELETE FROM reserves",
            "UPDATE sailors SET age = 1",
            "DROP TABLE boats",
            "INSERT INTO boats VALUES (900, 'X', 'red')",
            "SELECT 1; DROP TABLE boats",
            "COPY (SELECT 1) TO '/tmp/pwned.csv'",
            "ATTACH '/tmp/evil.db'",
            "PRAGMA database_list",
            "SELECT * FROM read_csv('/etc/passwd')",
            "SELECT * FROM read_parquet('/tmp/x.pq')",
            "SELECT * FROM glob('/**')",
            "/* sneaky */ DELETE FROM boats",
            "",
        ]
        for sql in allowed:
            try:
                t2s.validate_select(sql, con)
                check(f"allows  {sql[:44]}", True)
            except t2s.SqlSafetyError as exc:
                check(f"allows  {sql[:44]}  -- {str(exc)[:50]}", False)
        for sql in refused:
            try:
                t2s.validate_select(sql, con)
                check(f"refuses {sql[:44]!r}  -- WAS ALLOWED", False)
            except t2s.SqlSafetyError:
                check(f"refuses {sql[:44]!r}", True)
    finally:
        con.close()


def test_metadata() -> None:
    """The schema brief must be introspected, complete, and cacheable."""
    print("\n[4] Text-to-SQL schema brief")
    import text_to_sql as t2s

    con = sdb.connect()   # same settings as the rest of the suite
    try:
        meta = t2s.harvest(con)
        live = con.execute("SELECT count(*) FROM sailors").fetchone()[0]
        check(f"row counts harvested (live count {live})",
              meta.row_counts["sailors"] == live)
        # Seed fidelity is only assertable when nothing has been added through
        # the app (app-created ids start at 1000).
        untouched = con.execute(
            "SELECT count(*) FROM sailors WHERE sid >= 1000").fetchone()[0] == 0
        if untouched:
            check("seeded database still holds the 14 tutorial sailors", live == 14)
        else:
            print("  --    seed-count check skipped: this database has app-created rows")
        check("colour enumeration is exact and lower-case",
              meta.enumerations["boats.color"] == sorted(sdb.VALID_COLORS))
        # Against the database, not against the seed count: booking one more
        # day through the app used to fail this line, which is the same trap
        # the row counts above were rewritten to avoid.
        distinct_days = con.execute(
            "SELECT count(DISTINCT day) FROM reserves").fetchone()[0]
        check(f"date range harvested ({distinct_days} distinct days)",
              meta.ranges["reserves.day"]["distinct_days"] == distinct_days)
        check("sample rows present", len(meta.samples["reserves"]) == 5)

        brief = t2s.build_system_prompt(meta)
        # The DDL is DuckDB's own reconstruction, so it is machine-normalised:
        # `PRIMARY KEY(bid, "day")`, no space, `day` quoted as a reserved word.
        # The prose section states the same key in the form a reader expects.
        for needle in ('PRIMARY KEY(bid, "day")',   # from the introspected DDL
                       'UNIQUE(sid, "day")',        # R10, same source
                       "`(bid, day)`",              # from the prose grain section
                       "boat on any given day",     # req 10 in prose
                       "Horatio", "generate_series",
                       "'red'", "NOT EXISTS", "sailors.sid"):
            check(f"brief mentions {needle!r}", needle in brief)
        # Opus 5 caches prefixes of 512+ tokens; below that the breakpoint is a no-op.
        check(f"brief is cacheable (~{len(brief)//4} tokens > 512)", len(brief) // 4 > 512)
    finally:
        con.close()


def test_charts_serialise() -> None:
    """Every chart must survive JSON serialisation with real query data.

    `chart.to_dict()` alone is not enough: it succeeds on a frame holding
    `datetime.date` values, and the failure only appears when Vega serialises
    the embedded data to JSON. That is why a date-handling change once broke
    two notebook charts while the app still looked fine -- Streamlit's chart
    path tolerates `date`, marimo's does not.
    """
    print("\n[5] Charts serialise with real data")
    import json
    import plots

    con = sdb.connect()
    try:
        cases = [
            ("reservations per boat", plots.plot_reservations_per_boat, """
                SELECT b.bid, b.bname, b.color, count(r.day) AS n_reservations
                FROM boats b LEFT JOIN reserves r ON r.bid = b.bid
                GROUP BY 1, 2, 3"""),
            ("avg age by rating", plots.plot_avg_age_by_rating, """
                SELECT rating, round(avg(age), 2) AS avg_age, count(*) AS n_sailors
                FROM sailors WHERE rating IS NOT NULL GROUP BY 1"""),
            ("reservations by month", plots.plot_reservations_by_month, """
                SELECT date_trunc('month', day)::DATE AS month_start,
                       count(*) AS n_reservations
                FROM reserves GROUP BY 1 ORDER BY 1"""),
            ("fleet calendar", plots.plot_fleet_calendar, """
                SELECT r.day, r.bid, r.bid || ' ' || b.bname AS boat_label,
                       r.sid, s.sname
                FROM reserves r JOIN boats b ON b.bid = r.bid
                JOIN sailors s ON s.sid = r.sid"""),
            ("bookings by colour (pie)", plots.plot_bookings_by_colour, """
                SELECT b.color, count(*) AS n_reservations,
                       100.0 * count(*) / sum(count(*)) OVER () AS pct
                FROM reserves r JOIN boats b ON b.bid = r.bid
                GROUP BY b.color ORDER BY n_reservations DESC, b.color"""),
            ("age vs rating", plots.plot_age_vs_rating, """
                SELECT sid, sname, rating, age,
                       (SELECT count(*) FROM reserves r WHERE r.sid = s.sid)
                           AS n_reservations
                FROM sailors s WHERE rating IS NOT NULL"""),
        ]
        for label, fn, query in cases:
            df = sdb.q(con, query)
            try:
                spec = fn(df).to_dict()
                json.dumps(spec)          # the step that actually caught the bug
                check(f"{label} serialises to JSON", True)
            except Exception as exc:
                check(f"{label} serialises to JSON -- {type(exc).__name__}: "
                      f"{str(exc)[:60]}", False)
    finally:
        con.close()


# Every chart in the four level notebooks, with the query that feeds it. The
# SQL is a compact version of the notebook's own -- what is being guarded is the
# *shape* of the frame each plotting function is handed (column names, and the
# date columns Vega cannot serialise), not the prose around it.
LEVEL_CHART_CASES = [
    ("L1 boats per colour", "plots_level_01", "plot_boats_per_colour", """
        SELECT color, count(*) AS n_boats, string_agg(bname, ', ') AS boats
        FROM boats GROUP BY color"""),
    ("L1 crew by age", "plots_level_01", "plot_crew_by_age", """
        SELECT sid, sname, age, rating FROM sailors ORDER BY age DESC"""),
    ("L1 season strip", "plots_level_01", "plot_season_strip", """
        SELECT day, bid, sid FROM reserves
        WHERE day BETWEEN DATE '1998-09-01' AND DATE '1998-11-30'"""),

    ("L2 who sails", "plots_level_02", "plot_who_sails", """
        SELECT CASE WHEN EXISTS (SELECT 1 FROM reserves r WHERE r.sid = s.sid)
                    THEN 'has reserved a boat' ELSE 'never reserved a boat' END AS status,
               count(*) AS n_sailors, string_agg(s.sname, ', ') AS who
        FROM sailors s GROUP BY status"""),
    ("L2 boats per sailor", "plots_level_02", "plot_boats_per_sailor", """
        SELECT s.sid, s.sname, count(DISTINCT r.bid) AS n_boats,
               count(*) AS n_reservations
        FROM sailors s JOIN reserves r ON r.sid = s.sid
        GROUP BY s.sid, s.sname HAVING count(DISTINCT r.bid) >= 2"""),
    ("L2 rating distribution", "plots_level_02", "plot_rating_distribution", """
        SELECT rating, count(*) AS n_sailors, string_agg(sname, ', ') AS who,
               rating = (SELECT max(rating) FROM sailors) AS is_top_rating
        FROM sailors WHERE rating IS NOT NULL GROUP BY rating"""),
    ("L2 voting by rating", "plots_level_02", "plot_voting_by_rating", """
        SELECT rating, count(*) AS n_sailors,
               count(*) FILTER (WHERE age > 18)  AS n_can_vote,
               count(*) FILTER (WHERE age <= 18) AS n_too_young
        FROM sailors WHERE rating IS NOT NULL GROUP BY rating"""),
    ("L2 bookings per boat", "plots_level_02", "plot_bookings_per_boat", """
        SELECT b.bid, b.bname, b.color, count(r.day) AS n_reservations,
               count(r.day) = 0 AS never_reserved
        FROM boats b LEFT JOIN reserves r ON r.bid = b.bid
        GROUP BY b.bid, b.bname, b.color"""),

    ("L3 top sailors", "plots_level_03", "plot_top_sailors", """
        SELECT s.sid, s.sname, count(r.bid) AS n_reservations,
               count(DISTINCT r.bid) AS n_boats,
               rank() OVER (ORDER BY count(r.bid) DESC) AS rank_from_top,
               rank() OVER (ORDER BY count(r.bid) DESC) <= 3 AS in_top_3
        FROM sailors s LEFT JOIN reserves r ON r.sid = s.sid
        GROUP BY s.sid, s.sname"""),
    ("L3 bottom sailors", "plots_level_03", "plot_bottom_sailors", """
        WITH counted AS (
            SELECT s.sid, s.sname, count(r.bid) AS n_reservations
            FROM sailors s LEFT JOIN reserves r ON r.sid = s.sid
            GROUP BY s.sid, s.sname)
        SELECT sid, sname, n_reservations,
               dense_rank() OVER (ORDER BY n_reservations)      AS rank_from_bottom,
               dense_rank() OVER (ORDER BY n_reservations) <= 3 AS in_bottom_3
        FROM counted"""),
    ("L3 colour mix", "plots_level_03", "plot_colour_mix", """
        SELECT s.sid, s.sname || ' (' || s.sid || ')' AS sailor, b.color,
               count(*) AS n_reservations
        FROM reserves r JOIN sailors s ON s.sid = r.sid JOIN boats b ON b.bid = r.bid
        GROUP BY s.sid, sailor, b.color"""),
    ("L3 boat seasons", "plots_level_03", "plot_boat_seasons", """
        SELECT b.bid, b.bid || ' ' || b.bname AS boat, b.color,
               count(r.day) AS n_reservations, min(r.day) AS first_out,
               max(r.day) AS last_out, max(r.day) - min(r.day) AS span_days
        FROM boats b JOIN reserves r ON r.bid = b.bid GROUP BY b.bid, boat, b.color"""),
    ("L3 busiest days", "plots_level_03", "plot_busiest_days", """
        SELECT r.day, count(*) AS boats_out,
               round(100.0 * count(*) / (SELECT count(*) FROM boats), 1) AS pct_of_fleet,
               string_agg(s.sname || ' / ' || b.bname, ', ') AS who
        FROM reserves r JOIN sailors s ON s.sid = r.sid JOIN boats b ON b.bid = r.bid
        GROUP BY r.day"""),
    ("L3 age bands", "plots_level_03", "plot_age_bands", """
        SELECT CASE WHEN age < 25 THEN 'under 25' WHEN age < 40 THEN '25 to 39'
                    WHEN age < 55 THEN '40 to 54' ELSE '55 and over' END AS age_band,
               count(*) AS n_sailors, round(avg(rating), 2) AS avg_rating,
               round(avg(age), 1) AS avg_age, min(age) AS band_floor
        FROM sailors GROUP BY age_band"""),

    ("L4 division progress", "plots_level_04", "plot_division_progress", """
        SELECT s.sid, s.sname, count(DISTINCT r.bid) AS boats_reserved,
               (SELECT count(*) FROM boats) AS fleet_size,
               count(DISTINCT r.bid) = (SELECT count(*) FROM boats) AS has_them_all
        FROM sailors s LEFT JOIN reserves r ON r.sid = s.sid GROUP BY s.sid, s.sname"""),
    ("L4 running total", "plots_level_04", "plot_running_total", """
        SELECT r.day, count(*) AS n_reservations,
               sum(count(*)) OVER (ORDER BY r.day)::BIGINT AS running_total,
               round(100.0 * sum(count(*)) OVER (ORDER BY r.day)
                     / sum(count(*)) OVER (), 1) AS pct_of_season
        FROM reserves r GROUP BY r.day"""),
    ("L4 rank functions", "plots_level_04", "plot_rank_functions", """
        SELECT s.sid, s.sname, count(r.bid) AS n_reservations,
               row_number() OVER w AS as_row_number, rank() OVER w AS as_rank,
               dense_rank() OVER w AS as_dense_rank
        FROM sailors s LEFT JOIN reserves r ON r.sid = s.sid
        GROUP BY s.sid, s.sname WINDOW w AS (ORDER BY count(r.bid) DESC)"""),
    ("L4 boat idle", "plots_level_04", "plot_boat_idle", """
        SELECT b.bid || ' ' || b.bname AS boat, r.day,
               lag(r.day) OVER w AS previous_outing,
               r.day - lag(r.day) OVER w AS idle_days
        FROM reserves r JOIN boats b ON b.bid = r.bid
        WINDOW w AS (PARTITION BY r.bid ORDER BY r.day)"""),
    ("L4 season share", "plots_level_04", "plot_season_share", """
        SELECT s.sname || ' (' || s.sid || ')' AS sailor, count(*) AS n_reservations,
               round(100.0 * count(*) / sum(count(*)) OVER (), 1) AS pct_of_season
        FROM reserves r JOIN sailors s ON s.sid = r.sid GROUP BY sailor"""),
    ("L4 month heatmap", "plots_level_04", "plot_month_heatmap", """
        PIVOT (SELECT b.bid || ' ' || b.bname AS boat,
                      strftime(r.day, '%Y-%m') AS month
               FROM reserves r JOIN boats b ON b.bid = r.bid)
        ON month USING count(*) GROUP BY boat"""),
    ("L4 idle days", "plots_level_04", "plot_idle_days", """
        WITH bounds AS (SELECT min(day) AS first_day, max(day) AS last_day FROM reserves),
        spine AS (SELECT unnest(range((SELECT first_day FROM bounds),
                                      (SELECT last_day FROM bounds) + INTERVAL 1 DAY,
                                      INTERVAL 1 DAY))::DATE AS day),
        booked AS (SELECT DISTINCT day FROM reserves)
        SELECT extract(year FROM s.day)::INTEGER AS yr, count(*) AS days_observed,
               count(b.day) AS days_with_a_booking,
               count(*) - count(b.day) AS idle_days,
               round(100.0 * (count(*) - count(b.day)) / count(*), 1) AS pct_idle
        FROM spine s LEFT JOIN booked b ON b.day = s.day
        GROUP BY yr ORDER BY yr"""),
    ("L4 year ranking", "plots_level_04", "plot_year_ranking", """
        SELECT extract(year FROM day)::INTEGER AS yr, count(*) AS n_reservations,
               count(DISTINCT sid) AS n_sailors, count(DISTINCT bid) AS n_boats,
               rank() OVER (ORDER BY count(*) DESC) AS rank_by_volume,
               round(100.0 * count(*) / sum(count(*)) OVER (), 1) AS pct_of_all_time,
               count(*) - lag(count(*)) OVER (ORDER BY yr) AS change_on_previous_year
        FROM reserves GROUP BY yr ORDER BY rank_by_volume, yr"""),
    ("L4 utilisation", "plots_level_04", "plot_utilisation", """
        WITH RECURSIVE bounds AS (
            SELECT min(day) AS first_day, max(day) AS last_day FROM reserves),
        season(day) AS (
            SELECT first_day FROM bounds
            UNION ALL
            SELECT day + 1 FROM season, bounds WHERE day < bounds.last_day)
        SELECT se.day, count(r.bid) AS boats_out,
               round(100.0 * count(r.bid) / (SELECT count(*) FROM boats), 1) AS pct_of_fleet
        FROM season se LEFT JOIN reserves r ON r.day = se.day GROUP BY se.day"""),
]


def test_level_charts_serialise() -> None:
    """The same JSON guard as [5], for the four level notebooks' charts.

    `to_dict()` is not the test -- `json.dumps` of the result is. Two of these
    charts came in as lollipops whose stem encoding serialised perfectly and
    then failed to *render*, which is why the plotting modules also get looked
    at in a browser after a change.
    """
    print("\n[6] Level-notebook charts serialise with real data")
    import importlib
    import json

    con = sdb.connect()
    try:
        for label, module, fn_name, query in LEVEL_CHART_CASES:
            fn = getattr(importlib.import_module(module), fn_name)
            try:
                json.dumps(fn(sdb.q(con, query)).to_dict())
                check(f"{label} serialises to JSON", True)
            except Exception as exc:
                check(f"{label} serialises to JSON -- {type(exc).__name__}: "
                      f"{str(exc)[:60]}", False)
    finally:
        con.close()


# How many queries each level notebook holds. Levels 1-3 are ten; Level 4 has
# twelve, the last two added for the year-shaped questions (idle days per year,
# and years ranked) that only come alive on the 2024-2026 database.
LEVEL_QUERY_COUNTS = {"01": 10, "02": 10, "03": 10, "04": 12}


def test_level_notebooks() -> None:
    """Each level notebook must execute end to end, and hold exactly 10 queries.

    Run in a *subprocess*, not here: the notebooks open the database read-only
    and this process already holds a writable connection, which DuckDB refuses
    to allow at the same time inside one process.

    The count check is the auditable part of the assignment. The expected size
    of each level lives in LEVEL_QUERY_COUNTS below, and the numbering must be
    contiguous from q1 -- so a query added without a number, renumbered by hand,
    or duplicated fails here rather than being noticed months later.
    """
    print("\n[7] Level notebooks execute (each in its own process)")
    import re
    import subprocess

    for level, expected in LEVEL_QUERY_COUNTS.items():
        name = f"notebook_level_{level}"
        source = (PROJECT_ROOT / "notebooks" / f"{name}.py").read_text()
        found = {int(m) for m in re.findall(r"^    q(\d+) = run\(", source, re.M)}
        check(f"{name}: {expected} queries, q1-q{expected}",
              found == set(range(1, expected + 1)))

        result = subprocess.run(
            [sys.executable, "-c",
             "import sys; sys.argv = ['x']; sys.path.insert(0, 'notebooks');"
             f"import {name} as nb; o, d = nb.app.run(); print(len(o), 'cells')"],
            cwd=PROJECT_ROOT, capture_output=True, text=True,
            env={**os.environ, "SAILORS_DB": str(sdb.DB_PATH)},
        )
        if result.returncode == 0:
            check(f"{name}: runs headlessly ({result.stdout.strip()})", True)
        else:
            check(f"{name}: runs headlessly", False)
            print(f"          {result.stderr.strip().splitlines()[-1][:100]}")


def test_ask_page_refreshes_sql() -> None:
    """A second question must replace the SQL box, not leave the first one there.

    Reported from real use: after asking one question and then another, the
    explanation and confidence updated but the SQL box still held the FIRST
    query -- so the reader saw the right answer and ran the wrong SQL.

    Cause: a Streamlit widget with an explicit `key` reads
    st.session_state[key] in preference to its `value=` argument on every
    rerun after the first, so `value=` silently stopped having any effect.
    The page now assigns st.session_state["t2s_sql"] at generation time.
    """
    print("\n[8] Ask page refreshes its SQL box")
    from streamlit.testing.v1 import AppTest

    q1 = ("SELECT s.sid FROM sailors s WHERE NOT EXISTS "
          "(SELECT 1 FROM reserves r WHERE r.sid = s.sid)")
    q2 = ("SELECT s.sname FROM boats b JOIN reserves r ON r.bid = b.bid "
          "JOIN sailors s ON s.sid = r.sid WHERE b.bname = 'All Sunshine'")
    usage = {"input_tokens": 20, "output_tokens": 90, "cache_read_input_tokens": 0,
             "cache_creation_input_tokens": 0, "model": "test"}

    def reply(sql):
        return {"sql": sql, "explanation": "stub", "assumptions": [],
                "confidence": "high", "_usage": usage}

    at = AppTest.from_file(str(PROJECT_ROOT / "app" / "streamlit_app.py"),
                           default_timeout=60)
    at.run()
    import text_to_sql
    text_to_sql.credentials_available = lambda: True
    at.sidebar.radio[0].set_value("Ask in English").run()

    text_to_sql.generate_sql = lambda q, m, **k: reply(q1)
    at.text_area[0].set_value("first question").run()
    next(b for b in at.button if "Generate SQL" in b.label).click().run()
    check("first question populates the SQL box", "NOT EXISTS" in at.text_area[1].value)

    text_to_sql.generate_sql = lambda q, m, **k: reply(q2)
    at.text_area[0].set_value("second question").run()
    next(b for b in at.button if "Generate SQL" in b.label).click().run()
    box = at.text_area[1].value
    check("second question REPLACES the SQL box", "All Sunshine" in box)
    check("no stale SQL left behind", "NOT EXISTS" not in box)

    at.text_area[1].set_value("SELECT 1 AS edited").run()
    check("a manual edit still survives a rerun",
          at.text_area[1].value == "SELECT 1 AS edited")


def test_sql_panels() -> None:
    """The Show SQL panels must display the statements that actually executed.

    The teaching value collapses if the panel is a hand-written copy that has
    drifted from the code, so the write helpers record their own statements and
    the UI renders those. This checks the recording, and the rendering of
    values (a `?` on screen teaches nothing).
    """
    print("\n[9] Show SQL panels")
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "panels.duckdb"
        shutil.copy(sdb.DB_PATH, db)

        log = sdb.SqlLog()
        sid = sdb.register_sailor("Panel Tester", 6, 41.0, db_path=db, log=log)
        text = log.rendered()
        check("register_sailor records the sequence call", "nextval('seq_sid')" in text)
        check("register_sailor records the INSERT", "INSERT INTO sailors" in text)
        check("values are substituted, not '?'", "?" not in text and "Panel Tester" in text)
        check("the recorded id matches the row written", str(sid) in text)

        log = sdb.SqlLog()
        bid = sdb.register_boat("Panel Boat", "green", db_path=db, log=log)
        check("register_boat records its INSERT",
              "INSERT INTO boats" in log.rendered() and "'green'" in log.rendered())

        log = sdb.SqlLog()
        sdb.make_reservation(sid, bid, dt.date(1999, 5, 1), db_path=db, log=log)
        text = log.rendered()
        check("make_reservation records its INSERT", "INSERT INTO reserves" in text)
        check("a date renders as a DATE literal", "DATE '1999-05-01'" in text)

        log = sdb.SqlLog()
        sdb.cancel_reservation(bid, dt.date(1999, 5, 1), db_path=db, log=log)
        check("cancel_reservation records its DELETE", "DELETE FROM reserves" in log.rendered())

        # Reads funnel through q(), so logging there covers every view page.
        con = sdb.connect(db)
        log = sdb.SqlLog()
        sdb.reservations_on(con, dt.date(1998, 10, 10), log=log)
        check("read helpers record their query", "FROM reserves r" in log.rendered())
        check("read params are substituted", "DATE '1998-10-10'" in log.rendered())
        con.close()

        # Rendering details that make the panel readable.
        check("NULL renders as NULL",
              "NULL" in sdb.format_sql("SELECT ?", [None]))
        check("quotes inside a string are escaped",
              "'O''Brien'" in sdb.format_sql("SELECT ?", ["O'Brien"]))
        # Reported from real use: the model wrote `ORDER BY or2.from_day`,
        # qualifying a SELECT output alias, and DuckDB rejected it. dry_run has
        # to catch that class of thing before the user clicks Run.
        con = sdb.connect(db)
        import text_to_sql as t2s_mod
        bad = ("WITH t AS (SELECT sid, day FROM reserves) "
               "SELECT t.sid, t.day AS from_day FROM t ORDER BY t.from_day")
        err = t2s_mod.dry_run(bad, con)
        check("dry_run catches a qualified output alias", err is not None and "Binder" in err)
        check("dry_run passes a valid query",
              t2s_mod.dry_run("SELECT sid FROM sailors", con) is None)
        check("dry_run does not execute (EXPLAIN only)",
              t2s_mod.dry_run("SELECT 1/0 AS boom", con) is None)
        con.close()

        check("indentation is stripped for display",
              sdb.format_sql("\n    SELECT 1\n    FROM t\n").startswith("SELECT 1"))


def test_streamlit_pages() -> None:
    print("\n[10] Streamlit pages render")
    from streamlit.testing.v1 import AppTest

    app_path = str(PROJECT_ROOT / "app" / "streamlit_app.py")
    pages = [
        "Dashboard", "Sailor registration", "Boat registration",
        "Reservation system", "View a day", "View a date range",
        "Boat availability", "Constraint playground", "Ask in English",
        "SQL console",
    ]
    for page in pages:
        at = AppTest.from_file(app_path, default_timeout=60).run()
        at.sidebar.radio[0].set_value(page).run()
        if at.exception:
            check(f"{page} rendered", False)
            print(f"          {at.exception[0].message}")
        else:
            check(f"{page} rendered", True)


def test_second_dataset() -> None:
    """The 2024-2026 dataset: generated deterministically, and to specification.

    The generator check comes first and needs no database: `generate()` must
    reproduce database/sql_large/02_data.sql byte for byte, which is what makes the committed
    file trustworthy — if someone edits the SQL by hand, or changes the
    specification without regenerating, this fails.

    The rest only runs when the second database has been built, because it is
    optional: `./create_database_large.sh`.
    """
    print("\n[11] Second dataset (database/sql_large/02_data.sql)")
    import generate_data_large as gen

    on_disk = gen.OUT_PATH.read_text() if gen.OUT_PATH.exists() else ""
    check("database/sql_large/02_data.sql matches a fresh generation", on_disk == gen.generate())

    db2 = PROJECT_ROOT / "sailors_and_boats_large.duckdb"
    if not db2.exists():
        print("  --    database checks skipped: build it with ./create_database_large.sh")
        return

    con = sdb.connect(db2, read_only=True)
    try:
        def scalar(sql: str):
            return con.execute(sql).fetchone()[0]

        # Each row: what the specification says, and the query that proves it.
        for label, sql, want in [
            (f"{gen.N_SAILORS} sailors", "SELECT count(*) FROM sailors", gen.N_SAILORS),
            (f"{gen.N_SAILORS_NEVER_BOOK} sailors never reserve a boat",
             """SELECT count(*) FROM sailors s WHERE NOT EXISTS
                (SELECT 1 FROM reserves r WHERE r.sid = s.sid)""",
             gen.N_SAILORS_NEVER_BOOK),
            (f"{gen.N_RATING_10} sailors rated 10",
             "SELECT count(*) FROM sailors WHERE rating = 10", gen.N_RATING_10),
            (f"{gen.N_OVER_70} sailors older than 70",
             "SELECT count(*) FROM sailors WHERE age > 70", gen.N_OVER_70),
            (f"{gen.N_UNRATED} sailors unrated",
             "SELECT count(*) FROM sailors WHERE rating IS NULL", gen.N_UNRATED),
            (f"{gen.N_BOATS} boats", "SELECT count(*) FROM boats", gen.N_BOATS),
            (f"{gen.N_BOATS_NEVER_BOOKED} boats never reserved",
             """SELECT count(*) FROM boats b WHERE NOT EXISTS
                (SELECT 1 FROM reserves r WHERE r.bid = b.bid)""",
             gen.N_BOATS_NEVER_BOOKED),
            (f"{gen.N_RESERVATIONS} reservations", "SELECT count(*) FROM reserves",
             gen.N_RESERVATIONS),
            ("3 years covered",
             "SELECT count(DISTINCT extract(year FROM day)) FROM reserves", 3),
            # The two constraints, counted rather than trusted: if either pair
            # repeated, the row count and the distinct count would disagree.
            ("every (bid, day) is unique",
             "SELECT count(DISTINCT (bid, day)) FROM reserves", gen.N_RESERVATIONS),
            ("every (sid, day) is unique",
             "SELECT count(DISTINCT (sid, day)) FROM reserves", gen.N_RESERVATIONS),
        ]:
            got = scalar(sql)
            check(f"{label} (got {got})", got == want)

        # Days nobody sailed -- the point of the calendar-spine lesson, and a
        # property the generator has to force: at 5,000 bookings a weighted
        # draw alone would touch nearly every date.
        idle = con.execute("""
            WITH spine AS (SELECT unnest(range((SELECT min(day) FROM reserves),
                                               (SELECT max(day) FROM reserves)
                                                   + INTERVAL 1 DAY,
                                               INTERVAL 1 DAY))::DATE AS day)
            SELECT extract(year FROM s.day) AS yr, count(*) AS idle_days
            FROM spine s
            WHERE NOT EXISTS (SELECT 1 FROM reserves r WHERE r.day = s.day)
            GROUP BY yr ORDER BY yr""").fetchall()
        check(f"every year has days with no booking at all "
              f"({', '.join(f'{int(y)}: {n}' for y, n in idle)})",
              len(idle) == 3 and all(n >= gen.IDLE_DAYS_PER_YEAR for _y, n in idle))

        # ...and the opposite shape: regatta days where the fleet nearly empties.
        busiest, median_day = con.execute("""
            WITH per_day AS (SELECT day, count(*) AS c FROM reserves GROUP BY day)
            SELECT max(c), median(c) FROM per_day""").fetchone()
        check(f"some days dominate: busiest {busiest} boats out vs a median "
              f"day of {median_day:.0f}", busiest >= 3 * median_day)
        check(f"the busiest day nearly empties the fleet ({busiest} boats)",
              busiest >= gen.PEAK_SHARE * (gen.N_BOATS - gen.N_BOATS_NEVER_BOOKED))

        summer = scalar("""SELECT round(100.0 * count(*) FILTER
                           (WHERE extract(month FROM day) IN (6, 7, 8))
                           / count(*), 1) FROM reserves""")
        check(f"summer dominates: {summer}% of bookings are June-August",
              summer > 50)
        months = scalar("SELECT count(DISTINCT extract(month FROM day)) FROM reserves")
        # A generator bug once emptied November-February entirely; every month
        # having at least one booking is the cheapest guard against its return.
        check(f"every month of the year appears ({months}/12)", months == 12)
        latest = scalar("SELECT max(day) FROM reserves")
        check(f"no future-dated bookings (latest {latest})",
              latest <= dt.date.today())
        check("red and white are the two commonest colours",
              [r[0] for r in con.execute(
                  """SELECT color FROM boats GROUP BY color
                     ORDER BY count(*) DESC, color LIMIT 2""").fetchall()]
              == ["red", "white"])
        # The tutorial database must be untouched by any of this.
        tutorial = scalar("SELECT count(*) FROM reserves WHERE day < DATE '2000-01-01'")
        check("no tutorial rows leaked into the second dataset", tutorial == 0)
    finally:
        con.close()


def test_concept_index() -> None:
    """Every `G Q14` / `L3 Q9` reference in CONCEPTS.md must point at a real query.

    The index is a map from an idea to the cell that teaches it, so its value is
    entirely in the references being right. They are the thing most likely to
    rot: renumber a query, drop one, and the index still *reads* fine.

    This parses the notebooks for the queries they actually define and checks
    every citation against them.
    """
    print("\n[12] Concept index references resolve")
    import re

    index = PROJECT_ROOT / "CONCEPTS.md"
    if not index.exists():
        check("CONCEPTS.md exists", False)
        return

    notebooks = {
        "G": "notebook_guided",
        "L1": "notebook_level_01",
        "L2": "notebook_level_02",
        "L3": "notebook_level_03",
        "L4": "notebook_level_04",
    }
    defined: dict[str, set[int]] = {}
    for code, module in notebooks.items():
        source = (PROJECT_ROOT / "notebooks" / f"{module}.py").read_text()
        # `q7 = run(...)`, and the guided notebook's q18, which is built from a
        # DataFrame rather than a query but is still a numbered lesson.
        defined[code] = {int(m) for m in re.findall(r"^    q(\d+) = ", source, re.M)}
        check(f"{code}: {len(defined[code])} queries found in {module}.py",
              len(defined[code]) > 0)

    text = index.read_text()
    refs = re.findall(r"\b(G|L[1-4]) Q(\d+)\b", text)
    check(f"the index cites {len(refs)} queries", len(refs) > 50)

    broken = sorted({f"{c} Q{n}" for c, n in refs if int(n) not in defined[c]})
    check(f"every citation resolves{'' if not broken else ' -- broken: ' + ', '.join(broken)}",
          not broken)

    # Every notebook should be represented; an index that quietly stops covering
    # a level is worse than no index.
    for code in notebooks:
        cited = {int(n) for c, n in refs if c == code}
        missing = sorted(defined[code] - cited)
        check(f"{code}: every query is cited at least once"
              f"{'' if not missing else ' -- missing: ' + str(missing)}",
              not missing)


def main() -> int:
    print("Sailors & Boats -- smoke tests")
    ensure_database()
    test_constraints()
    test_write_helpers()
    test_sql_guard()
    test_metadata()
    test_charts_serialise()
    test_level_charts_serialise()
    test_level_notebooks()
    test_ask_page_refreshes_sql()
    test_sql_panels()
    test_streamlit_pages()
    test_second_dataset()
    test_concept_index()

    print(f"\n{PASSED} passed, {FAILED} failed")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
