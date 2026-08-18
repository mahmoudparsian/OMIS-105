"""Data-access layer for the Sailors & Boats database.

Shared by the Marimo notebook and the Streamlit application so that both talk
to the database through exactly one set of rules.

Design note: every write goes through a function here, and every function lets
the *database* be the judge -- the CHECK / PRIMARY KEY / FOREIGN KEY
constraints in database/sql/01_schema.sql are what actually reject bad data. The
pre-flight checks in this module exist only to turn a raw
``duckdb.ConstraintException`` into a sentence a student can read.
"""

from __future__ import annotations

import datetime as dt
import os
import textwrap
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import duckdb
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Which database file everything talks to. Override it with the SAILORS_DB
# environment variable -- that is how run_app.sh and run_notebook.sh point the
# app and the notebook at a database given on the command line, and how you
# keep a scratch copy for experimenting without touching the seeded one.
DEFAULT_DB_PATH = PROJECT_ROOT / "sailors_and_boats.duckdb"
DB_PATH = Path(os.environ.get("SAILORS_DB") or DEFAULT_DB_PATH).expanduser()

VALID_COLORS = ["red", "green", "blue", "white", "black", "yellow"]


class BusinessRuleError(Exception):
    """A write was rejected. The message explains which rule stopped it."""


# ---------------------------------------------------------------------------
# Connections
# ---------------------------------------------------------------------------

def connect(db_path: Path | str = DB_PATH, read_only: bool = False) -> duckdb.DuckDBPyConnection:
    """Open a connection to the database file.

    DuckDB allows many reader processes *or* one writer process, and within a
    single process every connection to a file must share the same settings.
    So: the notebook connects with `read_only=True` and only reads; the
    Streamlit app holds one writable connection and does everything through it.
    Running both against the same file at the same time will fail on the lock --
    close the notebook before starting the app, or point one of them at a copy.
    """
    db_path = Path(db_path)
    if not db_path.exists():
        raise FileNotFoundError(
            f"{db_path} does not exist. Build it first:\n"
            f"    uv run python src/build_database.py"
        )
    return duckdb.connect(str(db_path), read_only=read_only)


@contextmanager
def writer(db_path: Path | str = DB_PATH,
           con: duckdb.DuckDBPyConnection | None = None
           ) -> Iterator[duckdb.DuckDBPyConnection]:
    """A transaction: committed on success, rolled back on error.

    Pass `con` to reuse a connection the caller already owns (the Streamlit app
    holds exactly one). DuckDB refuses to open the same file twice in one
    process with different settings -- a read-only handle and a writable handle
    cannot coexist -- so a long-lived caller must own its single connection and
    hand it in here rather than letting this function open a second one.

    With `con=None` a short-lived writable connection is opened and closed.
    """
    owned = con is None
    con = connect(db_path, read_only=False) if owned else con
    try:
        con.execute("BEGIN")
        yield con
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise
    finally:
        if owned:
            con.close()


def as_literal(value) -> str:
    """Render one bound parameter the way it would be typed in SQL."""
    if value is None:
        return "NULL"
    if isinstance(value, (dt.date, dt.datetime)):
        return f"DATE '{value:%Y-%m-%d}'"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, str):
        return "'" + value.replace("'", "''") + "'"
    return str(value)


def format_sql(sql: str, params: list | None = None) -> str:
    """The statement with its bound values filled in -- for DISPLAY only.

    The app executes the parameterised form; substituting values into executed
    SQL is how injection bugs happen. But `VALUES (?, ?, ?, ?)` teaches a
    student nothing, and this is a teaching app, so the panels show the
    statement as a person would have typed it.
    """
    out = sql
    for value in params or []:
        out = out.replace("?", as_literal(value), 1)
    # The statements are written inside indented triple-quoted strings, so the
    # first line arrives flush and the rest carry the Python indentation.
    # Strip the blank first line, then remove the common leading whitespace.
    return textwrap.dedent(out.strip("\n")).strip()


class SqlLog(list):
    """Collects the statements a write helper actually executed.

    Pass one into a write function and it records `(sql, params)` for every
    statement it ran, in order. The UI shows exactly these -- never a
    hand-written copy, which would drift from reality the first time somebody
    edits one and forgets the other.
    """

    def record(self, sql: str, params: list | None = None) -> None:
        self.append((sql, list(params or [])))

    def rendered(self) -> str:
        return ";\n\n".join(format_sql(sql, params) for sql, params in self) + ";"


def q(con: duckdb.DuckDBPyConnection, sql: str, params: list | None = None,
      log: "SqlLog | None" = None) -> pd.DataFrame:
    """Run a SELECT and hand back a DataFrame.

    Pass `log` to have the statement recorded for the app's "Show SQL" panels.

    A DuckDB DATE arrives in pandas as datetime64, which renders as
    "1998-10-10 00:00:00" -- a time component on a column whose entire design
    point (R5) is that it has none.

    This schema has no TIMESTAMP column anywhere: `reserves.day` is the only
    temporal column and it is a DATE, so any datetime64 column pandas hands
    back came from a DATE and is converted straight back to one. Every caller
    -- app, notebook, tests -- therefore prints YYYY-MM-DD without having to
    remember to.
    """
    if log is not None:
        log.record(sql, params)
    df = con.execute(sql, params or []).df()
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.date
    return df


# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------

def all_sailors(con, log=None) -> pd.DataFrame:
    return q(con, "SELECT sid, sname, rating, age FROM sailors ORDER BY sid", log=log)


def all_boats(con, log=None) -> pd.DataFrame:
    return q(con, "SELECT bid, bname, color FROM boats ORDER BY bid", log=log)


def all_reservations(con, log=None) -> pd.DataFrame:
    return q(
        con,
        """
        SELECT r.day, r.bid, b.bname, b.color, r.sid, s.sname, s.rating
        FROM reserves r
        JOIN boats   b ON b.bid = r.bid
        JOIN sailors s ON s.sid = r.sid
        ORDER BY r.day, r.bid
        """,
        log=log,
    )


def reservations_on(con, day: dt.date, log=None) -> pd.DataFrame:
    """View the register for a single day."""
    return q(
        con,
        """
        SELECT r.day, r.bid, b.bname, b.color, r.sid, s.sname, s.rating
        FROM reserves r
        JOIN boats   b ON b.bid = r.bid
        JOIN sailors s ON s.sid = r.sid
        WHERE r.day = ?
        ORDER BY r.bid
        """,
        [day], log,
    )


def reservations_between(con, start: dt.date, end: dt.date, log=None) -> pd.DataFrame:
    """View the register across a date range (both ends inclusive)."""
    if start > end:
        start, end = end, start
    return q(
        con,
        """
        SELECT r.day, r.bid, b.bname, b.color, r.sid, s.sname, s.rating
        FROM reserves r
        JOIN boats   b ON b.bid = r.bid
        JOIN sailors s ON s.sid = r.sid
        WHERE r.day BETWEEN ? AND ?
        ORDER BY r.day, r.bid
        """,
        [start, end], log,
    )


def available_boats_on(con, day: dt.date, log=None) -> pd.DataFrame:
    """Boats with no reservation on `day` -- the free slots for that date.

    This is the direct consequence of PRIMARY KEY (bid, day): a boat is either
    in `reserves` for that day or it is available, never both.
    """
    return q(
        con,
        """
        SELECT b.bid, b.bname, b.color
        FROM boats b
        WHERE NOT EXISTS (
            SELECT 1 FROM reserves r WHERE r.bid = b.bid AND r.day = ?
        )
        ORDER BY b.bid
        """,
        [day], log,
    )


def free_sailors_on(con, day: dt.date, log=None) -> pd.DataFrame:
    """Sailors with no reservation on `day` -- who is still able to book.

    The exact mirror of available_boats_on, down to the NOT EXISTS: that one
    comes from PRIMARY KEY (bid, day), this one from UNIQUE (sid, day). Both
    constraints turn "already booked" into a clean either/or, so availability
    on each side is a single negation.
    """
    return q(
        con,
        """
        SELECT s.sid, s.sname, s.rating, s.age
        FROM sailors s
        WHERE NOT EXISTS (
            SELECT 1 FROM reserves r WHERE r.sid = s.sid AND r.day = ?
        )
        ORDER BY s.sid
        """,
        [day], log,
    )


def who_holds(con, bid: int, day: dt.date) -> pd.DataFrame:
    """The (at most one) sailor holding boat `bid` on `day`."""
    return q(
        con,
        """
        SELECT r.sid, s.sname, r.bid, r.day
        FROM reserves r JOIN sailors s ON s.sid = r.sid
        WHERE r.bid = ? AND r.day = ?
        """,
        [bid, day],
    )


def next_sid(con) -> int:
    return int(con.execute("SELECT nextval('seq_sid')").fetchone()[0])


def next_bid(con) -> int:
    return int(con.execute("SELECT nextval('seq_bid')").fetchone()[0])


# ---------------------------------------------------------------------------
# Writes
# ---------------------------------------------------------------------------

def register_sailor(sname: str, rating: int | None, age: float | None,
                    sid: int | None = None, db_path: Path | str = DB_PATH,
                    con: duckdb.DuckDBPyConnection | None = None,
                    log: "SqlLog | None" = None) -> int:
    """Register a new sailor. Returns the sid actually used.

    `sid=None` draws the next value from seq_sid (starts at 1000).
    """
    sname = (sname or "").strip()
    if not sname:
        raise BusinessRuleError("A sailor needs a name.")
    if rating is not None and not (1 <= rating <= 10):
        raise BusinessRuleError(f"Rating must be between 1 and 10 (got {rating}).")
    if age is not None and not (0 <= age <= 120):
        raise BusinessRuleError(f"Age must be between 0 and 120 (got {age}).")

    with writer(db_path, con) as w:
        con = w
        if sid is None:
            sid = next_sid(con)
            if log is not None:
                log.record("SELECT nextval('seq_sid')")
        elif con.execute("SELECT 1 FROM sailors WHERE sid = ?", [sid]).fetchone():
            raise BusinessRuleError(
                f"Sailor id {sid} is already taken -- sailor ids are unique (R6)."
            )
        stmt = "INSERT INTO sailors (sid, sname, rating, age) VALUES (?, ?, ?, ?)"
        con.execute(stmt, [sid, sname, rating, age])
        if log is not None:
            log.record(stmt, [sid, sname, rating, age])
    return int(sid)


def register_boat(bname: str, color: str, bid: int | None = None,
                  db_path: Path | str = DB_PATH,
                  con: duckdb.DuckDBPyConnection | None = None,
                  log: "SqlLog | None" = None) -> int:
    """Register a new boat. Returns the bid actually used."""
    bname = (bname or "").strip()
    color = (color or "").strip().lower()
    if not bname:
        raise BusinessRuleError("A boat needs a name.")
    if color not in VALID_COLORS:
        raise BusinessRuleError(
            f"'{color}' is not an allowed colour. Pick one of: {', '.join(VALID_COLORS)}."
        )

    with writer(db_path, con) as w:
        con = w
        if bid is None:
            bid = next_bid(con)
            if log is not None:
                log.record("SELECT nextval('seq_bid')")
        elif con.execute("SELECT 1 FROM boats WHERE bid = ?", [bid]).fetchone():
            raise BusinessRuleError(
                f"Boat id {bid} is already taken -- boat ids are unique (R7)."
            )
        stmt = "INSERT INTO boats (bid, bname, color) VALUES (?, ?, ?)"
        con.execute(stmt, [bid, bname, color])
        if log is not None:
            log.record(stmt, [bid, bname, color])
    return int(bid)


def make_reservation(sid: int, bid: int, day: dt.date, db_path: Path | str = DB_PATH,
                     con: duckdb.DuckDBPyConnection | None = None,
                     log: "SqlLog | None" = None) -> None:
    """Reserve boat `bid` for sailor `sid` on `day`.

    Fails, with an explanation, if the boat is already out that day
    (R2, R3, R4, R8 -- PRIMARY KEY (bid, day)) or if the sailor is already out
    that day (R10 -- UNIQUE (sid, day)). Both checks exist only to produce a
    readable sentence; the schema is what actually rejects the row. Rule labels
    are defined in the REQUIREMENTS block of database/sql/01_schema.sql.
    """
    if isinstance(day, dt.datetime):
        day = day.date()

    with writer(db_path, con) as w:
        con = w
        if not con.execute("SELECT 1 FROM sailors WHERE sid = ?", [sid]).fetchone():
            raise BusinessRuleError(f"No sailor with id {sid}. Register the sailor first.")
        if not con.execute("SELECT 1 FROM boats WHERE bid = ?", [bid]).fetchone():
            raise BusinessRuleError(f"No boat with id {bid}. Register the boat first.")

        holder = con.execute(
            """
            SELECT r.sid, s.sname FROM reserves r
            JOIN sailors s ON s.sid = r.sid
            WHERE r.bid = ? AND r.day = ?
            """,
            [bid, day],
        ).fetchone()
        if holder:
            if holder[0] == sid:
                raise BusinessRuleError(
                    f"Sailor {sid} already has boat {bid} on {day}. "
                    f"A sailor cannot book the same boat twice for one date (R8)."
                )
            raise BusinessRuleError(
                f"Boat {bid} is already reserved on {day} by {holder[1]} (sailor {holder[0]}). "
                f"One boat, one day, one sailor (R2-R4)."
            )

        # R10, the mirror image of the check above: the boat is free,
        # but the sailor may already be out on something else that day.
        busy = con.execute(
            """
            SELECT r.bid, b.bname FROM reserves r
            JOIN boats b ON b.bid = r.bid
            WHERE r.sid = ? AND r.day = ?
            """,
            [sid, day],
        ).fetchone()
        if busy:
            raise BusinessRuleError(
                f"Sailor {sid} already has boat {busy[0]} ({busy[1]}) on {day}. "
                f"A sailor can only sail one boat a day (R10). "
                f"Cancel that reservation first, or pick another date."
            )

        stmt = "INSERT INTO reserves (sid, bid, day) VALUES (?, ?, ?)"
        con.execute(stmt, [sid, bid, day])
        if log is not None:
            log.record(stmt, [sid, bid, day])


def cancel_reservation(bid: int, day: dt.date, db_path: Path | str = DB_PATH,
                       con: duckdb.DuckDBPyConnection | None = None,
                       log: "SqlLog | None" = None) -> int:
    """Release the (bid, day) slot. Returns the number of rows removed (0 or 1)."""
    if isinstance(day, dt.datetime):
        day = day.date()
    with writer(db_path, con) as w:
        before = w.execute("SELECT count(*) FROM reserves WHERE bid = ? AND day = ?",
                           [bid, day]).fetchone()[0]
        stmt = "DELETE FROM reserves WHERE bid = ? AND day = ?"
        w.execute(stmt, [bid, day])
        if log is not None:
            log.record(stmt, [bid, day])
    return int(before)
