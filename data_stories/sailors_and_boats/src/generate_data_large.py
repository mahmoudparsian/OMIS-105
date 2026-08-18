#!/usr/bin/env python3
"""Generate the second dataset -- a marina three years wide -- as SQL.

    uv run python src/generate_data_large.py          # rewrite database/sql_large/02_data.sql
    uv run python src/generate_data_large.py --check  # regenerate and diff, write nothing

This writes `database/sql_large/02_data.sql`, which `create_database_large.sh` loads on top of the
*unchanged* `database/sql/01_schema.sql`. The tutorial data in `database/sql/02_data.sql` is never
touched: the two datasets share a schema and nothing else.

WHY A GENERATOR AND NOT 2,000 HAND-WRITTEN ROWS. The dataset has to satisfy a
specification exactly -- 10 sailors rated 10, 20 sailors over 70, 5 who never
book, 4 boats never booked, 2,000 reservations, summer-heavy -- while obeying
two constraints that make naive random data illegal:

    PRIMARY KEY (bid, day)   one boat, one day, one sailor
    UNIQUE      (sid, day)   one sailor, one day, one boat

Those are why reservations are built a *day at a time*: for each day the
generator draws k distinct boats and k distinct sailors and pairs them off, so
both constraints hold by construction rather than by retrying until DuckDB stops
complaining.

The seed is fixed, so the same file comes out every run -- rerunning this script
is a no-op unless the specification below changes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import random
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = PROJECT_ROOT / "database" / "sql_large" / "02_data.sql"

SEED = 20260817

# --- the specification, in one place ----------------------------------------
N_SAILORS = 235
N_SAILORS_NEVER_BOOK = 5
N_RATING_10 = 10          # exactly this many sailors are rated 10
N_OVER_70 = 20            # exactly this many sailors are older than 70
N_UNRATED = 8             # rating IS NULL -- keeps the NULL lessons alive

N_BOATS = 44
N_BOATS_NEVER_BOOKED = 4
# Red and white dominate; the six colours are the ones ck_boats_color allows.
COLOUR_MIX = {"red": 13, "white": 11, "blue": 7, "green": 6, "yellow": 4, "black": 3}

N_RESERVATIONS = 5000
SEASON_START = dt.date(2024, 1, 1)
SEASON_END = dt.date(2026, 8, 17)      # "so far" -- no future-dated bookings

# Relative weight of a booking landing in each month. Summer dominates; the
# marina barely runs in midwinter.
MONTH_WEIGHT = {1: 0.15, 2: 0.20, 3: 0.45, 4: 0.90, 5: 1.70, 6: 3.20,
                7: 4.00, 8: 3.80, 9: 1.90, 10: 0.85, 11: 0.35, 12: 0.20}

# Days the marina books NOTHING at all, per calendar year. At 5,000 bookings
# over ~960 days the weighted draw would otherwise touch nearly every date, and
# "which days did nobody sail?" is a question worth being able to ask -- it is
# the calendar-spine lesson, and the answer has to be non-empty for the question
# to teach anything. Chosen against the month weights, so most land in winter
# and a handful fall in the season.
IDLE_DAYS_PER_YEAR = 45

# Regatta days: a few dates each summer when the fleet nearly empties. Without
# them the busiest day is only a little above the average and "find the busiest
# day" has no interesting answer. Each takes at least PEAK_SHARE of the boats
# that can be booked at all.
PEAK_DAYS_PER_YEAR = 6
PEAK_MONTHS = (6, 7, 8)
PEAK_SHARE = 0.75

# ids stay below 1000: seq_sid and seq_bid start there, so the app's
# registration forms can add rows to this database without colliding.
FIRST_SID = 1
FIRST_BID = 101

FIRST_NAMES = [
    "Ada", "Alan", "Amara", "Anders", "Anita", "Arjun", "Astrid", "Beatriz",
    "Bram", "Camila", "Cathy", "Cesar", "Chidi", "Clara", "Dagny", "Dario",
    "Deepa", "Dmitri", "Eero", "Elena", "Elias", "Esme", "Farid", "Fiona",
    "Gabriel", "Greta", "Hana", "Hugo", "Ida", "Imani", "Ines", "Isaac",
    "Jonas", "Julia", "Kaito", "Karin", "Kwame", "Lars", "Leila", "Linus",
    "Lucia", "Magnus", "Maren", "Mateo", "Mei", "Nadia", "Niels", "Nora",
    "Omar", "Oona", "Otto", "Pablo", "Petra", "Priya", "Quinn", "Rafael",
    "Rania", "Rosa", "Rune", "Sanne", "Sergei", "Sofia", "Soren", "Tariq",
    "Tessa", "Theo", "Tomas", "Ulla", "Vera", "Viktor", "Wei", "Yara",
    "Yusuf", "Zara", "Zoltan",
]
LAST_NAMES = [
    "Aalto", "Abara", "Almeida", "Bergman", "Bianchi", "Bouchard", "Cabral",
    "Chandra", "Costa", "Dahl", "Delgado", "Eriksen", "Fabre", "Ferreira",
    "Gallo", "Grimaldi", "Haas", "Halvorsen", "Ibarra", "Ivanov", "Jansen",
    "Kaur", "Keller", "Kimura", "Kovac", "Laurent", "Lindqvist", "Mensah",
    "Moreau", "Nakamura", "Novak", "Okafor", "Olsen", "Ortega", "Pereira",
    "Petrov", "Rasmussen", "Reyes", "Rossi", "Sandoval", "Schneider", "Silva",
    "Sorensen", "Tanaka", "Vargas", "Virtanen", "Walsh", "Weber", "Yilmaz",
    "Zhang",
]
BOAT_NAMES = [
    "Albatross", "Anemone", "Aurora", "Bluefin", "Boreas", "Cormorant",
    "Corsair", "Dolphin", "Eider", "Fulmar", "Gannet", "Halcyon", "Harrier",
    "Heron", "Kestrel", "Kingfisher", "Kittiwake", "Lodestar", "Mistral",
    "Nautilus", "Nimbus", "Northwind", "Osprey", "Pelican", "Peregrine",
    "Petrel", "Puffin", "Quicksilver", "Regatta", "Sandpiper", "Scoter",
    "Seafarer", "Shearwater", "Skua", "Solstice", "Spindrift", "Squall",
    "Sunfish", "Tern", "Trade Wind", "Vagabond", "Wayfarer", "Windward",
    "Zephyr",
]


def _days(start: dt.date, end: dt.date) -> list[dt.date]:
    return [start + dt.timedelta(days=i) for i in range((end - start).days + 1)]


def make_sailors(rng: random.Random) -> list[tuple[int, str, int | None, float]]:
    """235 sailors hitting every count in the specification exactly.

    Ratings and ages are assigned to *positions* first and shuffled afterwards,
    which is what makes "exactly 10 rated 10" and "exactly 20 over 70" true by
    construction. Drawing each sailor independently and hoping the totals land
    on 10 and 20 would need a retry loop and would still be luck.
    """
    names: list[str] = []
    seen: set[str] = set()
    while len(names) < N_SAILORS - 3:
        name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
        if name not in seen and len(name) <= 32:
            seen.add(name)
            names.append(name)
    # Three deliberate duplicate names. The tutorial database has two Horatios
    # so that `count(DISTINCT sname)` differs from `count(*)`; keep that lesson
    # available here, at a scale where it is easy to miss.
    names += rng.sample(names, 3)
    rng.shuffle(names)

    ratings: list[int | None] = (
        [10] * N_RATING_10
        + [None] * N_UNRATED
        + [rng.randint(1, 9) for _ in range(N_SAILORS - N_RATING_10 - N_UNRATED)]
    )
    rng.shuffle(ratings)

    ages = [round(rng.uniform(70.5, 88.0) * 2) / 2 for _ in range(N_OVER_70)]
    ages += [round(rng.uniform(18.0, 69.5) * 2) / 2
             for _ in range(N_SAILORS - N_OVER_70)]
    rng.shuffle(ages)

    return [(FIRST_SID + i, names[i], ratings[i], ages[i])
            for i in range(N_SAILORS)]


def make_boats(rng: random.Random) -> list[tuple[int, str, str]]:
    """44 boats, red and white dominant, colours from the CHECK constraint."""
    assert sum(COLOUR_MIX.values()) == N_BOATS, "COLOUR_MIX must total N_BOATS"
    colours = [c for c, n in COLOUR_MIX.items() for _ in range(n)]
    rng.shuffle(colours)
    names = list(BOAT_NAMES)
    assert len(names) >= N_BOATS, "need one hull name per boat"
    return [(FIRST_BID + i, names[i], colours[i]) for i in range(N_BOATS)]


def daily_counts(days: list[dt.date], capacity: int, rng: random.Random) -> list[int]:
    """How many boats go out on each day, summing to exactly N_RESERVATIONS.

    Three shapes are imposed here, in this order, because each constrains the
    next:

    1. **Idle days** -- IDLE_DAYS_PER_YEAR dates a year book nothing. Drawn
       against the month weights (winter is likeliest) so the marina reads as
       closed rather than randomly skipped, but a few land mid-season.
    2. **Peak days** -- PEAK_DAYS_PER_YEAR summer dates where most of the fleet
       goes out at once. These are assigned their counts up front so they cannot
       be diluted by the general draw.
    3. **Everything else** -- the remaining bookings handed out one at a time to
       a day drawn with its month's weight, dropping a day from the pool when it
       reaches `capacity`, since the fleet cannot send out more hulls than it
       owns.

    An earlier version apportioned by rounding each day's share down and giving
    the remainder to the largest fractions: every winter day rounded to zero and
    the leftovers all landed in July, which produced three years with no booking
    at all between November and February. Idle days are now chosen on purpose
    rather than falling out of arithmetic.
    """
    by_year: dict[int, list[int]] = defaultdict(list)
    for i, day in enumerate(days):
        by_year[day.year].append(i)

    counts = [0] * len(days)
    idle: set[int] = set()
    peak: dict[int, int] = {}

    for _year, idxs in sorted(by_year.items()):
        # Quiet dates: an inverse month weight makes February far likelier than
        # July, without making July impossible.
        pool = list(idxs)
        weights = {i: 1.0 / MONTH_WEIGHT[days[i].month] for i in pool}
        for _ in range(min(IDLE_DAYS_PER_YEAR, len(pool) // 3)):
            pick = rng.choices(pool, weights=[weights[i] for i in pool])[0]
            pool.remove(pick)
            idle.add(pick)

        # Regatta days: summer only, and never one of the quiet dates.
        summer = [i for i in idxs
                  if days[i].month in PEAK_MONTHS and i not in idle]
        for pick in rng.sample(summer, min(PEAK_DAYS_PER_YEAR, len(summer))):
            peak[pick] = rng.randint(int(capacity * PEAK_SHARE), capacity)

    remaining = N_RESERVATIONS - sum(peak.values())
    if remaining < 0:                                # pragma: no cover
        raise RuntimeError("peak days alone exceed N_RESERVATIONS")
    for i, n in peak.items():
        counts[i] = n

    weights = [MONTH_WEIGHT[d.month] * rng.uniform(0.55, 1.45) for d in days]
    available = [i for i in range(len(days)) if i not in idle and i not in peak]
    for _ in range(remaining):
        if not available:                            # pragma: no cover
            raise RuntimeError("every bookable day is at capacity")
        i = rng.choices(available, weights=[weights[j] for j in available])[0]
        counts[i] += 1
        if counts[i] == capacity:
            available.remove(i)

    return counts


def make_reserves(sailors, boats, rng: random.Random):
    """2,000 reservations that satisfy PRIMARY KEY (bid, day) and UNIQUE (sid, day).

    Built one day at a time: pick k distinct boats and k distinct sailors for
    that day and zip them. Within a day no boat and no sailor repeats, so
    neither constraint can be violated; across days there is nothing to check.

    Two of the specification's counts are about *absence* -- 5 sailors and 4
    boats that never appear -- so those are held out of the pools entirely. The
    remaining sailors are weighted so the marina has regulars and occasionals,
    then every one of them is guaranteed at least one booking by the repair pass
    at the end: "5 never book" has to mean exactly five.
    """
    never_book = {s[0] for s in rng.sample(sailors, N_SAILORS_NEVER_BOOK)}
    never_booked = {b[0] for b in rng.sample(boats, N_BOATS_NEVER_BOOKED)}
    active_sids = [s[0] for s in sailors if s[0] not in never_book]
    active_bids = [b[0] for b in boats if b[0] not in never_booked]

    days = _days(SEASON_START, SEASON_END)
    counts = daily_counts(days, capacity=len(active_bids), rng=rng)

    # A long tail: some sailors book often, most book a handful of times. The
    # spread is deliberately modest -- a Pareto tail here gave one sailor 132 of
    # the 2,000 bookings, which is not a marina, it is a boat owner.
    sailor_weight = {sid: rng.lognormvariate(0.0, 0.62) for sid in active_sids}
    boat_weight = {bid: rng.uniform(0.6, 1.6) for bid in active_bids}

    rows: list[tuple[int, int, dt.date]] = []
    per_sailor: dict[int, list[int]] = defaultdict(list)   # sid -> row indexes
    for day, k in zip(days, counts):
        if k == 0:
            continue
        chosen_boats = _weighted_sample(active_bids, boat_weight, k, rng)
        chosen_sailors = _weighted_sample(active_sids, sailor_weight, k, rng)
        for bid, sid in zip(chosen_boats, chosen_sailors):
            per_sailor[sid].append(len(rows))
            rows.append((sid, bid, day))

    _guarantee_everyone_books(rows, per_sailor, active_sids, rng)
    _guarantee_every_boat_books(rows, active_bids, rng)

    assert len(rows) == N_RESERVATIONS
    rows.sort(key=lambda r: (r[2], r[1]))
    return rows, never_book, never_booked


def _weighted_sample(population, weights, k, rng):
    """k *distinct* items, drawn with weights. Distinctness is the whole point."""
    pool = list(population)
    picks = []
    for _ in range(k):
        total = sum(weights[x] for x in pool)
        r = rng.uniform(0, total)
        acc = 0.0
        for x in pool:
            acc += weights[x]
            if acc >= r:
                picks.append(x)
                pool.remove(x)
                break
    return picks


def _guarantee_everyone_books(rows, per_sailor, active_sids, rng) -> None:
    """Give every active sailor at least one booking, without adding rows.

    A weighted draw leaves some sailors at zero, which would make more than five
    sailors "never book" and quietly break the specification. So each empty
    sailor takes over a row from a sailor who has several -- checking first that
    they are not already out that day, which would violate UNIQUE (sid, day).
    """
    day_of_sailor = defaultdict(set)      # sid -> days they already hold
    for sid, _bid, day in rows:
        day_of_sailor[sid].add(day)

    empty = [sid for sid in active_sids if not per_sailor[sid]]
    for sid in empty:
        donors = sorted((s for s in per_sailor if len(per_sailor[s]) > 1),
                        key=lambda s: -len(per_sailor[s]))
        for donor in donors:
            for idx in list(per_sailor[donor]):
                day = rows[idx][2]
                if day in day_of_sailor[sid]:
                    continue
                rows[idx] = (sid, rows[idx][1], day)
                per_sailor[donor].remove(idx)
                per_sailor[sid].append(idx)
                day_of_sailor[sid].add(day)
                day_of_sailor[donor].discard(day)
                break
            if per_sailor[sid]:
                break
        else:                                        # pragma: no cover
            raise RuntimeError(f"could not give sailor {sid} a booking")


def _guarantee_every_boat_books(rows, active_bids, rng) -> None:
    """The same repair for boats: every boat outside the never-booked four sails.

    With 2,000 rows over 40 boats this is almost always already true; almost is
    not a specification.
    """
    used = {bid for _sid, bid, _day in rows}
    missing = [bid for bid in active_bids if bid not in used]
    for bid in missing:                              # pragma: no cover
        busiest = max(used, key=lambda b: sum(1 for r in rows if r[1] == b))
        for i, (sid, b, day) in enumerate(rows):
            if b != busiest:
                continue
            if any(r[1] == bid and r[2] == day for r in rows):
                continue
            rows[i] = (sid, bid, day)
            used.add(bid)
            break


def render(sailors, boats, reserves, never_book, never_booked) -> str:
    """The .sql file: a header explaining where it came from, then the rows."""
    summers = sum(1 for _s, _b, d in reserves if d.month in (6, 7, 8))
    by_year = defaultdict(int)
    per_day = defaultdict(int)
    for _s, _b, d in reserves:
        by_year[d.year] += 1
        per_day[d] += 1
    idle_by_year = defaultdict(int)
    day = SEASON_START
    while day <= SEASON_END:
        if day not in per_day:
            idle_by_year[day.year] += 1
        day += dt.timedelta(days=1)
    busiest = sorted(per_day.items(), key=lambda kv: (-kv[1], kv[0]))[:3]

    lines = [
        "-- " + "=" * 74,
        "--  OMIS 105 -- Sailors & Boats",
        "--  File   : database/sql_large/02_data.sql",
        "--  Purpose: Populate the SECOND database -- a marina three years wide.",
        "--",
        "--  GENERATED FILE. Do not hand-edit: change the specification at the",
        "--  top of src/generate_data_large.py and re-run it.",
        "--",
        "--      uv run python src/generate_data_large.py",
        "--      ./create_database_large.sh --force",
        "--",
        "--  This file is deliberately NOT in database/sql/. Everything in that directory",
        "--  is loaded into the tutorial database by ./create_database.sh, which",
        "--  globs database/sql/*.sql -- dropping this file there would silently add 2,000",
        "--  rows to the database the notebooks and tests describe.",
        "--",
        "--  The SCHEMA is shared and unmodified: create_database_large.sh runs",
        "--  database/sql/01_schema.sql and then this file. Every rule R1-R10, D1-D2 is",
        "--  therefore enforced here too -- ./create_database_large.sh --verify",
        "--  proves it against these rows.",
        "--",
        "--  WHAT IS IN HERE",
        f"--    {len(sailors):>5} sailors      {len(never_book)} of whom never reserve a boat",
        f"--    {N_RATING_10:>5} rated 10     {N_OVER_70} older than 70, {N_UNRATED} unrated (NULL)",
        f"--    {len(boats):>5} boats        {len(never_booked)} of which are never reserved",
        f"--    {len(reserves):>5} reservations {SEASON_START} .. {SEASON_END}",
        "--",
        "--  Reservations by year: "
        + ", ".join(f"{y} {n}" for y, n in sorted(by_year.items())),
        f"--  June-August holds {summers} of the {len(reserves)} bookings "
        f"({100 * summers / len(reserves):.0f}%) -- the season is the summer.",
        "--  Days with no booking at all: "
        + ", ".join(f"{y} {n}" for y, n in sorted(idle_by_year.items()))
        + "  (the marina is shut, mostly in winter)",
        "--  Busiest days: "
        + ", ".join(f"{d} with {n} boats out" for d, n in busiest)
        + f" -- against a median day of {sorted(per_day.values())[len(per_day)//2]}.",
        "--",
        "--  Ids stay below 1000 because seq_sid and seq_bid start there: the",
        "--  Streamlit app can register new sailors and boats in this database",
        "--  without colliding with these rows.",
        "-- " + "=" * 74,
        "",
        "-- ---------------------------------------------------------------------------",
        f"-- SAILORS -- {len(sailors)} rows",
        "-- ---------------------------------------------------------------------------",
        "INSERT INTO sailors (sid, sname, rating, age) VALUES",
    ]
    body = []
    for sid, sname, rating, age in sailors:
        r = "NULL" if rating is None else str(rating)
        name = f"'{sname}',"            # quote first, then pad: the columns line
        body.append(f"    ({sid:>3}, {name:<24} {r:>4}, {age:>5.1f})")   # up in the file
    lines.append(",\n".join(body) + ";")

    lines += [
        "",
        "-- ---------------------------------------------------------------------------",
        f"-- BOATS -- {len(boats)} rows",
        "-- ---------------------------------------------------------------------------",
        "INSERT INTO boats (bid, bname, color) VALUES",
    ]
    lines.append(",\n".join(
        f"    ({bid}, {(chr(39) + bname + chr(39) + ','):<16} '{colour}')"
        for bid, bname, colour in boats) + ";")

    lines += [
        "",
        "-- ---------------------------------------------------------------------------",
        f"-- RESERVES -- {len(reserves)} rows, ordered by day then boat",
        "--",
        "--   Every (bid, day) pair below is distinct, and so is every (sid, day)",
        "--   pair: one boat has one sailor that day, one sailor has one boat.",
        "-- ---------------------------------------------------------------------------",
        "INSERT INTO reserves (sid, bid, day) VALUES",
    ]
    lines.append(",\n".join(
        f"    ({sid:>3}, {bid}, DATE '{day}')" for sid, bid, day in reserves) + ";")
    lines.append("")
    return "\n".join(lines)


def generate() -> str:
    rng = random.Random(SEED)
    sailors = make_sailors(rng)
    boats = make_boats(rng)
    reserves, never_book, never_booked = make_reserves(sailors, boats, rng)

    # Fail here rather than in DuckDB: a violated assumption is a bug in this
    # script, and the error should name it.
    assert len({(b, d) for _s, b, d in reserves}) == len(reserves), "duplicate (bid, day)"
    assert len({(s, d) for s, _b, d in reserves}) == len(reserves), "duplicate (sid, day)"
    assert sum(1 for s in sailors if s[2] == 10) == N_RATING_10
    assert sum(1 for s in sailors if s[2] is None) == N_UNRATED
    assert sum(1 for s in sailors if s[3] > 70) == N_OVER_70
    booked = {s for s, _b, _d in reserves}
    assert len(sailors) - len(booked) == N_SAILORS_NEVER_BOOK
    sailed = {b for _s, b, _d in reserves}
    assert len(boats) - len(sailed) == N_BOATS_NEVER_BOOKED

    # The two shapes that are easy to lose in a refactor, and invisible in a
    # row count: every year must have days nobody sailed, and the busiest day
    # must genuinely stand out rather than being one above average.
    booked_days = {d for _s, _b, d in reserves}
    for year in {d.year for d in booked_days}:
        in_year = sum(1 for d in _days(SEASON_START, SEASON_END) if d.year == year)
        booked_in_year = sum(1 for d in booked_days if d.year == year)
        assert in_year - booked_in_year >= IDLE_DAYS_PER_YEAR, (
            f"{year} has only {in_year - booked_in_year} idle days")
    per_day = defaultdict(int)
    for _s, _b, d in reserves:
        per_day[d] += 1
    busiest = max(per_day.values())
    median_day = sorted(per_day.values())[len(per_day) // 2]
    assert busiest >= 3 * median_day, (
        f"busiest day ({busiest}) barely beats the median ({median_day})")

    return render(sailors, boats, reserves, never_book, never_booked)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="regenerate and compare with the file on disk; "
                             "write nothing, exit 1 if they differ")
    args = parser.parse_args()

    sql = generate()
    if args.check:
        current = OUT_PATH.read_text() if OUT_PATH.exists() else ""
        if current == sql:
            print(f"{OUT_PATH.relative_to(PROJECT_ROOT)} is up to date")
            return 0
        print(f"{OUT_PATH.relative_to(PROJECT_ROOT)} DIFFERS from a fresh "
              f"generation -- re-run without --check", file=sys.stderr)
        return 1

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(sql)
    print(f"wrote {OUT_PATH.relative_to(PROJECT_ROOT)}  ({len(sql.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
