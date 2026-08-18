#!/usr/bin/env python3
"""Build (or rebuild) the Sailors & Boats DuckDB database from the SQL files.

    uv run python src/build_database.py            # build ./sailors_and_boats.duckdb
    uv run python src/build_database.py --verify   # build, then prove the
                                                   # constraints actually bite

    # a different dataset on the same schema (see create_database_large.sh)
    uv run python src/build_database.py --sql database/sql/01_schema.sql database/sql_large/02_data.sql

The database file is recreated from scratch every run, so this script is the
single source of truth: edit database/sql/01_schema.sql or database/sql/02_data.sql and re-run.

With no --sql argument it runs every database/sql/*.sql in filename order, which is the
tutorial database. --sql names the scripts explicitly instead, which is how the
second dataset reuses database/sql/01_schema.sql -- one schema, two sets of rows -- while
staying out of the glob that builds the first.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = PROJECT_ROOT / "database" / "sql"

# One definition of "which database" for the whole project -- honours the
# SAILORS_DB environment variable. See sailors_db.DB_PATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sailors_db import DB_PATH  # noqa: E402


def sql_scripts() -> list[Path]:
    """Every database/sql/*.sql file, in filename order.

    The numeric prefixes (01_, 02_, …) are the execution order, so adding
    database/sql/03_extra_boats.sql is enough to have it run — there is no list of
    filenames here to forget to update. Sorting is by name, which is why the
    prefixes are zero-padded.
    """
    scripts = sorted(SQL_DIR.glob("*.sql"))
    if not scripts:
        raise FileNotFoundError(f"No .sql files found in {SQL_DIR}")
    return scripts


def build(db_path: Path = DB_PATH, scripts: list[Path] | None = None) -> Path:
    """Drop any existing database file and rebuild it from SQL.

    `scripts` defaults to every database/sql/*.sql -- the tutorial database. Pass a list
    to build a different dataset on the same schema, as create_database_large.sh
    does with [database/sql/01_schema.sql, database/sql_large/02_data.sql].
    """
    if db_path.exists():
        db_path.unlink()
    # DuckDB writes a WAL alongside the database; clear it too.
    wal = db_path.with_suffix(db_path.suffix + ".wal")
    if wal.exists():
        wal.unlink()

    con = duckdb.connect(str(db_path))
    try:
        for script in (scripts if scripts is not None else sql_scripts()):
            con.execute(Path(script).read_text())
            print(f"  ran {Path(script).name}")
        report_row_counts(con)
    finally:
        con.close()
    return db_path


def report_row_counts(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    """Print one line per table: how many rows it ended up holding.

    The tables are read out of the database rather than listed here, in creation
    order (`table_oid`), which is the order they appear in 01_schema.sql. Adding
    a fourth table to the schema therefore adds a line here on its own -- the
    same reasoning as `sql_scripts()` globbing instead of naming filenames.

    Returned as well as printed, so a caller can assert on the numbers.
    """
    tables = [r[0] for r in con.execute(
        "SELECT table_name FROM duckdb_tables() ORDER BY table_oid").fetchall()]
    counts = {t: con.execute('SELECT count(*) FROM "' + t + '"').fetchone()[0]
              for t in tables}
    if not counts:
        print("  no tables -- did the schema script run?")
        return counts

    width = max(len(t) for t in counts)
    print("  rows per table:")
    for table, n in counts.items():
        print(f"    {table:<{width}}  {n:>9,}")
    print(f"    {'total':<{width}}  {sum(counts.values()):>9,}")
    return counts


# The only errors that count as "a rule did its job". Anything else -- a missing
# table, a typo in the test's own SQL -- means the check never exercised the rule,
# and reporting that as a pass would be worse than useless.
_ENFORCEMENT_ERRORS = (duckdb.ConstraintException, duckdb.ConversionException)


def _expect_failure(con: duckdb.DuckDBPyConnection, label: str, sql: str) -> bool:
    """Run `sql` inside a rolled-back transaction; the constraint must reject it."""
    try:
        con.execute("BEGIN")
        con.execute(sql)
        con.execute("ROLLBACK")
        print(f"  FAIL  {label} -- the database ACCEPTED a row it should reject")
        return False
    except _ENFORCEMENT_ERRORS as exc:
        con.execute("ROLLBACK")
        first_line = str(exc).strip().splitlines()[0]
        print(f"  ok    {label}")
        print(f"          rejected with: {first_line[:110]}")
        return True
    except duckdb.Error as exc:
        # Rejected, but for the wrong reason -- the rule was never reached.
        con.execute("ROLLBACK")
        first_line = str(exc).strip().splitlines()[0]
        print(f"  FAIL  {label} -- failed before reaching the constraint")
        print(f"          {type(exc).__name__}: {first_line[:100]}")
        return False


@dataclass(frozen=True)
class Fixtures:
    """The rows `verify()` builds its forbidden statements out of.

    Every case needs the same six things: a real reservation (sid, bid, day), a
    sailor who is free that day, a boat that is free that day, and a later day
    on which both that sailor and that boat are free. Given those, each rule can
    be broken with one INSERT.
    """
    sid: int          # a sailor who holds a reservation on `day`
    bid: int          # the boat that sailor holds
    day: str          # the day of that reservation, as YYYY-MM-DD
    other_sid: int    # a sailor with nothing booked on `day`
    free_bid: int     # a boat with nothing booked on `day`
    next_day: str     # a later day on which both `sid` and `bid` are free
    absent_sid: int   # a sid that is not in sailors
    absent_bid: int   # a bid that is not in boats
    spare_id: int     # an id free in BOTH tables, for the CHECK-constraint rows


# The tutorial database's fixtures, hardcoded on purpose. The two "must SUCCEED"
# statements they produce are the accepted rows in the worked-example tables of
# schema notes [A] and [B], and CLAUDE.md requires those to stay identical to
# what the documentation shows. Deriving them from the data would pick a
# different, equally valid reservation and silently break that tie -- so when
# this is the tutorial data, the documented example wins.
_TUTORIAL = Fixtures(sid=22, bid=101, day="1998-10-10", other_sid=29,
                     free_bid=105, next_day="1998-10-11",
                     absent_sid=999, absent_bid=999, spare_id=500)


def _fixtures(con: duckdb.DuckDBPyConnection) -> Fixtures:
    """Pick the rows to attack, from whatever database this is.

    The tutorial database is recognised by the reservation the documentation
    quotes; anything else -- the 2024-2026 dataset, or a database somebody has
    been adding to through the app -- gets fixtures derived from its own rows,
    so the same eleven rules can be tested against it.
    """
    is_tutorial = con.execute(
        """
        SELECT count(*) FROM reserves
        WHERE sid = 22 AND bid = 101 AND day = DATE '1998-10-10'
        """
    ).fetchone()[0] == 1
    if is_tutorial:
        return _TUTORIAL

    # A real reservation to collide with: the most recent one, tie broken by
    # bid so the choice is deterministic.
    row = con.execute(
        "SELECT sid, bid, day FROM reserves ORDER BY day DESC, bid LIMIT 1"
    ).fetchone()
    if row is None:
        raise RuntimeError("cannot verify an empty database: reserves has no rows")
    sid, bid, day = int(row[0]), int(row[1]), row[2]

    # A sailor and a boat that are free that day. Both exist by construction in
    # this project's datasets (sailors who never book, boats never booked), but
    # ask the database rather than assume it.
    other_sid = con.execute(
        """
        SELECT s.sid FROM sailors s
        WHERE NOT EXISTS (SELECT 1 FROM reserves r
                          WHERE r.sid = s.sid AND r.day = ?)
        ORDER BY s.sid LIMIT 1
        """, [day]).fetchone()
    free_bid = con.execute(
        """
        SELECT b.bid FROM boats b
        WHERE NOT EXISTS (SELECT 1 FROM reserves r
                          WHERE r.bid = b.bid AND r.day = ?)
        ORDER BY b.bid LIMIT 1
        """, [day]).fetchone()
    if other_sid is None or free_bid is None:
        raise RuntimeError(
            f"every sailor or every boat is already booked on {day}; "
            "verify() needs one of each free to test R10 and note [B]")

    # A later day on which BOTH the sailor and the boat are free -- that is the
    # note [A] case, "same sailor keeps the same boat the next day".
    next_day = con.execute(
        """
        WITH days AS (SELECT unnest(range(? + INTERVAL 1 DAY,
                                          ? + INTERVAL 61 DAY,
                                          INTERVAL 1 DAY))::DATE AS day)
        SELECT d.day FROM days d
        WHERE NOT EXISTS (SELECT 1 FROM reserves r
                          WHERE r.day = d.day AND (r.sid = ? OR r.bid = ?))
        ORDER BY d.day LIMIT 1
        """, [day, day, sid, bid]).fetchone()
    if next_day is None:
        raise RuntimeError(
            f"sailor {sid} or boat {bid} is booked on every day for two months "
            f"after {day}; verify() has nowhere to put the note [A] row")

    max_sid = con.execute("SELECT max(sid) FROM sailors").fetchone()[0] or 0
    max_bid = con.execute("SELECT max(bid) FROM boats").fetchone()[0] or 0
    spare = int(max(max_sid, max_bid)) + 1

    return Fixtures(
        sid=sid, bid=bid, day=day.isoformat(),
        other_sid=int(other_sid[0]), free_bid=int(free_bid[0]),
        next_day=next_day[0].isoformat(),
        absent_sid=int(max_sid) + 1000, absent_bid=int(max_bid) + 1000,
        spare_id=spare,
    )


def verify(db_path: Path = DB_PATH) -> bool:
    """Try to violate every assignment rule. Each attempt must be rejected.

    Labels below (R2, R10, D1, ...) are the requirement labels defined in the
    REQUIREMENTS block at the top of database/sql/01_schema.sql -- the one place any
    database requirement is written down. Nothing here restates a rule; it
    cites one and then tries to break it.

    The statements are built from `_fixtures()`, so the same eleven rules can be
    run against any database on this schema. Against the tutorial data the
    fixtures are the documented ones and the output is unchanged.
    """
    con = duckdb.connect(str(db_path))
    ok = True
    try:
        f = _fixtures(con)
        print("\nConstraint verification -- every statement below must FAIL:")

        ok &= _expect_failure(
            con,
            "R6: duplicate sailor id",
            f"INSERT INTO sailors VALUES ({f.sid}, 'Impostor', 5, 30.0)",
        )
        ok &= _expect_failure(
            con,
            "R7: duplicate boat id",
            f"INSERT INTO boats VALUES ({f.bid}, 'Clone', 'red')",
        )
        ok &= _expect_failure(
            con,
            f"R2/R3: a second sailor takes boat {f.bid} on {f.day}",
            f"INSERT INTO reserves VALUES ({f.other_sid}, {f.bid}, DATE '{f.day}')",
        )
        ok &= _expect_failure(
            con,
            f"R4: boat {f.bid} booked twice for {f.day}",
            f"INSERT INTO reserves VALUES ({f.sid}, {f.bid}, DATE '{f.day}')",
        )
        ok &= _expect_failure(
            con,
            f"R8: sailor {f.sid} re-books boat {f.bid} on the same date",
            f"INSERT INTO reserves VALUES ({f.sid}, {f.bid}, DATE '{f.day}')",
        )
        # R10 needs a FREE boat to be convincing: `free_bid` has nothing booked
        # that day, so the primary key has no objection here and only
        # UNIQUE (sid, day) can reject it. The sailor is already out on `bid`.
        ok &= _expect_failure(
            con,
            f"R10: sailor {f.sid} takes a second (free) boat on {f.day}",
            f"INSERT INTO reserves VALUES ({f.sid}, {f.free_bid}, DATE '{f.day}')",
        )
        ok &= _expect_failure(
            con,
            "D1: reservation for a sailor who does not exist",
            f"INSERT INTO reserves VALUES ({f.absent_sid}, {f.free_bid}, DATE '{f.next_day}')",
        )
        ok &= _expect_failure(
            con,
            "D1: reservation for a boat that does not exist",
            f"INSERT INTO reserves VALUES ({f.sid}, {f.absent_bid}, DATE '{f.next_day}')",
        )
        ok &= _expect_failure(
            con,
            "R5: an impossible calendar date",
            f"INSERT INTO reserves VALUES ({f.sid}, {f.free_bid}, DATE '1998-13-45')",
        )
        ok &= _expect_failure(
            con,
            "D2: rating outside 1..10",
            f"INSERT INTO sailors VALUES ({f.spare_id}, 'Overachiever', 11, 30.0)",
        )
        ok &= _expect_failure(
            con,
            "D2: unknown boat colour",
            f"INSERT INTO boats VALUES ({f.spare_id}, 'Chartreuse Dream', 'chartreuse')",
        )

        # And the mirror image: legal rows must be ACCEPTED. These are the two
        # "accepted" rows in the worked-example tables of notes [A] and [B] in
        # database/sql/01_schema.sql -- kept identical so the documentation describes
        # statements that genuinely run.
        print("\nSanity check -- these must SUCCEED:")
        con.execute("BEGIN")
        con.execute(f"INSERT INTO reserves VALUES ({f.sid}, {f.bid}, DATE '{f.next_day}')")
        con.execute(f"INSERT INTO reserves VALUES ({f.other_sid}, {f.free_bid}, DATE '{f.day}')")
        con.execute("ROLLBACK")
        print("  ok    [A] same sailor keeps the same boat the next day")
        print("  ok    [B] a free sailor takes a boat nobody has booked")
    finally:
        con.close()

    print("\nAll constraint checks passed." if ok else "\nSOME CHECKS FAILED.")
    return bool(ok)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="run the constraint tests after building")
    parser.add_argument("--sql", nargs="+", metavar="FILE", type=Path,
                        help="the SQL scripts to run, in order "
                             "(default: every database/sql/*.sql)")
    args = parser.parse_args()

    missing = [f for f in (args.sql or []) if not f.is_file()]
    if missing:
        print(f"error: no such SQL file: {', '.join(str(m) for m in missing)}",
              file=sys.stderr)
        return 2

    print(f"Building {DB_PATH}")
    build(scripts=args.sql)
    if args.verify:
        return 0 if verify() else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
