# Building the large database, A to Z

How `sailors_and_boats_large.duckdb` — 235 sailors, 44 boats, 5,000 reservations
across 2024–2026 — is produced, from the specification to the verified database.

This is the long-form companion to [§7.1 of `README.md`](README.md#71-the-second-dataset--a-marina-three-years-wide),
which is the short version. Nothing here restates a database *requirement*:
R1–R10, P1–P3 and D1–D2 are defined once, in the `REQUIREMENTS` block at the top
of [`database/sql/01_schema.sql`](database/sql/01_schema.sql), and cited by label everywhere else,
including here.

---

## Contents

- [The one-minute version](#the-one-minute-version)
- [A. Why a second dataset](#a-why-a-second-dataset)
- [B. The two databases, side by side](#b-the-two-databases-side-by-side)
- [C. The rule that shapes everything: `database/sql/` is a glob](#c-the-rule-that-shapes-everything-databasesql-is-a-glob)
- [D. The pipeline](#d-the-pipeline)
- [E. The specification](#e-the-specification)
- [F. Step 1 — the sailors](#f-step-1--the-sailors)
- [G. Step 2 — the boats](#g-step-2--the-boats)
- [H. Step 3 — the shape of the calendar](#h-step-3--the-shape-of-the-calendar)
- [I. Step 4 — the reservations](#i-step-4--the-reservations)
- [J. Step 5 — the repair passes](#j-step-5--the-repair-passes)
- [K. Step 6 — the assertions](#k-step-6--the-assertions)
- [L. Step 7 — rendering the SQL file](#l-step-7--rendering-the-sql-file)
- [M. Step 8 — building the database](#m-step-8--building-the-database)
- [N. Step 9 — proving the rules still bite](#n-step-9--proving-the-rules-still-bite)
- [O. Step 10 — the test suite](#o-step-10--the-test-suite)
- [P. Using it](#p-using-it)
- [Q. Changing the data — recipes](#q-changing-the-data--recipes)
- [R. Determinism, and why the seed matters](#r-determinism-and-why-the-seed-matters)
- [S. How it fails, and what it says](#s-how-it-fails-and-what-it-says)
- [T. What the current dataset actually contains](#t-what-the-current-dataset-actually-contains)
- [U. Two bugs that shaped the generator](#u-two-bugs-that-shaped-the-generator)
- [V. Gotchas](#v-gotchas)
- [W. Where everything is defined](#w-where-everything-is-defined)

---

## The one-minute version

```bash
# build it (first time)
./create_database_large.sh --verify

# change the data: edit the constants at the top of src/generate_data_large.py, then
./create_database_large.sh --regenerate --force --verify

# check it
./run_tests.sh                    # group [11] is this dataset
```

Three files are involved, and each has exactly one job:

| file | job |
|---|---|
| `src/generate_data_large.py` | holds the specification; writes the SQL |
| `database/sql_large/02_data.sql` | the generated rows — 5,333 lines of `INSERT` |
| `create_database_large.sh` | runs `database/sql/01_schema.sql` + that file into a new database |

---

## A. Why a second dataset

The tutorial data is deliberately tiny: fourteen sailors you can hold in your
head, ten reservations, and worked answers that match a printed textbook. That
is exactly right for learning what a join *is*, and exactly wrong for seeing
what one *does*:

- a `GROUP BY` over 14 rows shows groups of one or two — you cannot see a
  distribution in it;
- "the busiest day" is a day with two boats out;
- window functions, ranking and `PIVOT` all work, but on data so small that the
  answer is obvious before the query runs;
- and a query that is accidentally quadratic is indistinguishable from one that
  is not.

The second dataset keeps every rule and changes only the scale, so the same
queries can be run twice: once where you can check the answer by eye, and once
where you have to trust the SQL.

## B. The two databases, side by side

|  | tutorial | second dataset |
|---|---|---|
| built by | `./create_database.sh` | `./create_database_large.sh` |
| file | `sailors_and_boats.duckdb` | `sailors_and_boats_large.duckdb` |
| schema | `database/sql/01_schema.sql` | **the same file** |
| rows from | `database/sql/02_data.sql` | `database/sql_large/02_data.sql` |
| sailors | 14 | 235 |
| boats | 9 | 44 |
| reservations | 10 | 5,000 |
| period | Sept–Nov 1998 | 2024-01-03 → 2026-08-17 |
| origin | transcribed from the PDF | generated |
| described by | the notebooks' prose, the PDF's worked answers | this document |

**`database/sql/02_data.sql` is never edited.** It is what the notebooks' prose, the
tutorial's worked answers and most of the test suite describe. The second
dataset exists precisely so that the first one does not have to change.

## C. The rule that shapes everything: `database/sql/` is a glob

`create_database.sh` does not list filenames. It runs **every** `database/sql/*.sql` in
filename order — that is a feature (`database/sql/03_extra.sql` needs no code change),
and it is a trap for a second dataset:

```python
# src/build_database.py
def sql_scripts() -> list[Path]:
    scripts = sorted(SQL_DIR.glob("*.sql"))
```

A file called `database/sql/03_big_data.sql` would therefore be loaded into the
**tutorial** database too — silently adding 5,000 rows to the database whose
every count is quoted in notebook prose, and breaking every seed-dependent
lesson at once.

So the second dataset lives in **`database/sql_large/`**, outside the glob, and
`create_database_large.sh` names its two scripts explicitly:

```bash
uv run python src/build_database.py --sql database/sql/01_schema.sql database/sql_large/02_data.sql
```

`--sql` exists for exactly this. With no `--sql`, `build_database.py` still
globs `database/sql/*.sql` and builds the tutorial database as it always did.

## D. The pipeline

```
   src/generate_data_large.py          ← the specification lives here (constants)
        │  seeded RNG, 0.2s
        ▼
   database/sql_large/02_data.sql               ← 5,333 lines: 235 + 44 + 5,000 INSERTs
        │
        │   create_database_large.sh
        │        runs, in order:
        │            database/sql/01_schema.sql   (shared, unmodified)
        │            database/sql_large/02_data.sql
        ▼
   sailors_and_boats_large.duckdb      ← 2.6 MB build artifact, git-ignored
        │
        ├── --verify   → 11 forbidden inserts, each rejected by the schema
        └── run_tests.sh → group [11]: 20 checks against the specification
```

Every arrow is reproducible: the same seed produces the same SQL file, and the
same SQL file produces the same database.

## E. The specification

All of it is constants at the top of `src/generate_data_large.py`. Nothing is
hidden further down; the functions read these and nothing else.

| constant | value | meaning |
|---|---|---|
| `SEED` | `20260817` | fixes the RNG; change it for a different marina with the same statistics |
| `N_SAILORS` | 235 | rows in `sailors` |
| `N_SAILORS_NEVER_BOOK` | 5 | sailors with no reservation, ever |
| `N_RATING_10` | 10 | sailors rated exactly 10 |
| `N_OVER_70` | 20 | sailors with `age > 70` |
| `N_UNRATED` | 8 | sailors with `rating IS NULL` |
| `N_BOATS` | 44 | rows in `boats` |
| `N_BOATS_NEVER_BOOKED` | 4 | boats no one has ever reserved |
| `COLOUR_MIX` | red 13, white 11, blue 7, green 6, yellow 4, black 3 | must total `N_BOATS`; only the six colours `ck_boats_color` allows |
| `N_RESERVATIONS` | 5000 | rows in `reserves` |
| `SEASON_START` / `SEASON_END` | 2024-01-01 / 2026-08-17 | the window; the end is "today", so nothing is future-dated |
| `MONTH_WEIGHT` | Jan 0.15 … Jul 4.00 … Dec 0.20 | relative likelihood of a booking landing in each month |
| `IDLE_DAYS_PER_YEAR` | 45 | dates each year that are forced to book **nothing** |
| `PEAK_DAYS_PER_YEAR` | 6 | regatta days each summer |
| `PEAK_MONTHS` | (6, 7, 8) | which months a regatta day may fall in |
| `PEAK_SHARE` | 0.75 | a regatta day books at least this fraction of the bookable fleet |
| `FIRST_SID` / `FIRST_BID` | 1 / 101 | id ranges — see the note below |

**Ids stay below 1000 on purpose.** `database/sql/01_schema.sql` creates
`seq_sid`/`seq_bid` starting at 1000, and the Streamlit app's registration forms
draw from them. Sailors 1–235 and boats 101–144 therefore leave the app free to
add rows to this database without ever colliding.

## F. Step 1 — the sailors

`make_sailors()` produces 235 rows in which every count in the specification is
exact — not approximately right.

**Names.** Built from a first-name × last-name product (75 × 50), rejecting
duplicates and anything over `VARCHAR(32)`. Then three names are deliberately
*re-used*, so 235 sailors carry 232 distinct names. That mirrors the tutorial's
two Horatios: `sname` is not a key, `count(DISTINCT sname)` differs from
`count(*)`, and grouping people by name silently merges two of them. The lesson
survives the change of scale.

**Ratings and ages are dealt, not drawn.** This is the important part:

```python
ratings = [10] * N_RATING_10 + [None] * N_UNRATED + [random 1..9 for the rest]
random.shuffle(ratings)
```

Building the list first and shuffling it guarantees "exactly 10 rated 10" and
"exactly 8 unrated". Drawing each sailor's rating independently and hoping the
total lands on 10 would need a retry loop, and would still be luck. Ages work
the same way: 20 values in 70.5–88.0, 215 in 18.0–69.5, shuffled together. Ages
are half-integers (`.0`/`.5`) because the tutorial's are, and the column is
`REAL`.

## G. Step 2 — the boats

`make_boats()` is the simple one. `COLOUR_MIX` is expanded into a list of 44
colours, shuffled, and zipped with 44 hull names (seabirds and weather, mostly).
The assertion `sum(COLOUR_MIX.values()) == N_BOATS` is what stops a mix that
does not add up from becoming a confusing failure 200 lines later.

Red (13) and white (11) dominate, as specified. Every colour is one of the six
`ck_boats_color` permits — the constraint would reject anything else at build
time, which is the schema doing the generator's quality control.

## H. Step 3 — the shape of the calendar

`daily_counts()` decides how many boats go out on each of the 960 days. Three
shapes are imposed **in this order**, because each constrains the next.

**1. Idle days — `IDLE_DAYS_PER_YEAR` dates a year book nothing at all.**
Drawn against the *inverse* month weight, so February is far likelier to be shut
than July, without July being impossible. These days are removed from the pool
entirely.

Why force them? At 5,000 bookings over 960 days, a purely weighted draw touches
nearly every date, and "which days did nobody sail?" comes back empty. That
question is the whole point of the calendar-spine pattern in Level 4 of the
notebooks — a query that manufactures the missing days and left-joins the facts
onto them. The answer has to be non-empty for the lesson to land.

**2. Peak days — `PEAK_DAYS_PER_YEAR` summer dates where the fleet nearly
empties.** Each is assigned a count of `PEAK_SHARE × capacity` to `capacity`
*up front*, so the general draw cannot dilute them. Without this the busiest day
is only slightly above average and "find the busiest day" has a boring answer.
With it, the answer is a regatta: 40 boats out against a median day of 5.

**3. Everything else** — the remaining bookings, handed out one at a time to a
day drawn with its month's weight:

```python
for _ in range(remaining):
    i = rng.choices(available, weights=[weights[j] for j in available])[0]
    counts[i] += 1
    if counts[i] == capacity:
        available.remove(i)          # the fleet has no more hulls that day
```

`capacity` is the number of *bookable* boats — 44 minus the 4 that never sail =
40. A day can never exceed it, because `PRIMARY KEY (bid, day)` makes a 41st
boat impossible to name.

## I. Step 4 — the reservations

`make_reserves()` turns those daily counts into rows. The whole design follows
from two constraints in `database/sql/01_schema.sql`:

```sql
PRIMARY KEY (bid, day)     -- one boat, one day, one sailor
UNIQUE      (sid, day)     -- one sailor, one day, one boat
```

So reservations are built **a day at a time**: for a day needing `k` bookings,
draw `k` *distinct* boats and `k` *distinct* sailors, and zip them together.

```python
chosen_boats   = _weighted_sample(active_bids, boat_weight, k, rng)
chosen_sailors = _weighted_sample(active_sids, sailor_weight, k, rng)
for bid, sid in zip(chosen_boats, chosen_sailors):
    rows.append((sid, bid, day))
```

Within a day no boat and no sailor repeats, so **both constraints hold by
construction** — there is no retry loop, and DuckDB is never asked to reject
anything. Across days there is nothing to check: the keys only constrain a
single date.

Two pools are held out before any of this happens, because the specification is
partly about *absence*:

- `N_SAILORS_NEVER_BOOK` sailors are excluded from `active_sids`;
- `N_BOATS_NEVER_BOOKED` boats are excluded from `active_bids`.

Sailor weights come from `rng.lognormvariate(0, 0.62)` — a modest long tail, so
the marina has regulars and occasionals (currently: median 18 bookings, max
118) without one person owning the season.

## J. Step 5 — the repair passes

A weighted draw leaves *some* active sailors with nothing, which would make more
than five sailors "never book" and quietly break the specification. Two passes
fix that without adding rows:

**`_guarantee_everyone_books()`** — each empty sailor takes over a row from a
sailor who holds several, checking first that they are not already out that day
(which `UNIQUE (sid, day)` would forbid). The row count never changes; only who
holds it.

**`_guarantee_every_boat_books()`** — the same for boats. With 5,000 rows over
40 boats this is almost always already true, but *almost* is not a
specification.

## K. Step 6 — the assertions

Before a single line is written, `generate()` checks its own work. These fail in
Python, naming the problem, rather than failing in DuckDB as a constraint error
that says only "duplicate key":

```python
assert len({(b, d) for _s, b, d in reserves}) == len(reserves)   # PK holds
assert len({(s, d) for s, _b, d in reserves}) == len(reserves)   # UNIQUE holds
assert sum(1 for s in sailors if s[2] == 10)   == N_RATING_10
assert sum(1 for s in sailors if s[2] is None) == N_UNRATED
assert sum(1 for s in sailors if s[3] > 70)    == N_OVER_70
assert len(sailors) - len(booked) == N_SAILORS_NEVER_BOOK
assert len(boats)   - len(sailed) == N_BOATS_NEVER_BOOKED
```

plus the two shape assertions that are easy to lose in a refactor and invisible
in a row count:

- every year has at least `IDLE_DAYS_PER_YEAR` days with no booking;
- the busiest day is at least **3×** the median day.

## L. Step 7 — rendering the SQL file

`render()` writes plain, readable `INSERT` statements — no `COPY`, no binary
format — because the file is meant to be opened and read:

```sql
INSERT INTO sailors (sid, sname, rating, age) VALUES
    (  1, 'Esme Novak',               9,  41.5),
    (  2, 'Deepa Petrov',             9,  47.0),
```

Columns are padded so they line up. The file opens with a header block that
records what it contains — counts, reservations per year, the summer share, idle
days per year, the busiest days — so the numbers travel with the data:

```
--  WHAT IS IN HERE
--      235 sailors      5 of whom never reserve a boat
--       10 rated 10     20 older than 70, 8 unrated (NULL)
--       44 boats        4 of which are never reserved
--     5000 reservations 2024-01-01 .. 2026-08-17
--
--  Reservations by year: 2024 1734, 2025 1909, 2026 1357
--  June-August holds 3489 of the 5000 bookings (70%) -- the season is the summer.
--  Days with no booking at all: 2024 103, 2025 105, 2026 61  (the marina is shut, mostly in winter)
--  Busiest days: 2025-06-20 with 40 boats out, ... -- against a median day of 5.
```

The header also says, in the file itself, that it is generated and must not be
hand-edited.

## M. Step 8 — building the database

```bash
./create_database_large.sh [database-path] [--verify] [--force] [--regenerate]
```

| flag | what it does |
|---|---|
| *(none)* | build `sailors_and_boats_large.duckdb` from the schema + the generated data |
| `--verify` | after building, attempt 11 forbidden inserts and print each rejection |
| `--force` | replace an existing database (refused without it — see below) |
| `--regenerate` | re-run `src/generate_data_large.py` first, then build |
| *first argument* | a database path, as with every other script in the project |

What it does, in order: loads `.env`, checks `uv` is installed, warns if the app
or a notebook is holding a database open, **refuses to overwrite an existing
file without `--force`** (printing what that file currently holds), then:

```bash
export SAILORS_DB="$DB"
uv run python src/build_database.py --sql database/sql/01_schema.sql database/sql_large/02_data.sql
```

The refusal matters because the app writes real rows: a database is a build
artifact right up until somebody registers a sailor in it.

## N. Step 9 — proving the rules still bite

The second dataset is on the same schema, so the same eleven rules must hold —
and `--verify` proves it against *these* rows rather than assuming:

```
Constraint verification -- every statement below must FAIL:
  ok    R2/R3: a second sailor takes boat 106 on 2026-08-17
          rejected with: Constraint Error: Duplicate key "bid: 106, day: 2026-08-17" …
  ok    R10: sailor 9 takes a second (free) boat on 2026-08-17
          rejected with: Constraint Error: Duplicate key "sid: 9, day: 2026-08-17" …
```

This works because `verify()` no longer hardcodes the tutorial's ids. `_fixtures()`
picks, out of whatever database it was handed:

- a real reservation `(sid, bid, day)` — the most recent one, ties broken by
  `bid`, so the choice is deterministic;
- a sailor with nothing booked that day, and a boat with nothing booked that day
  (the never-booking sailors and never-booked boats guarantee both exist);
- a later day on which that sailor *and* that boat are both free;
- ids that are absent from each table, for the foreign-key cases.

**One deliberate exception.** When the database *is* the tutorial one — detected
by the reservation `(22, 101, 1998-10-10)` — `_fixtures()` returns hardcoded
constants instead. The two "must SUCCEED" statements it builds are the accepted
rows in the worked-example tables of schema notes [A] and [B], and those are
required to stay byte-identical to what the documentation shows. Deriving them
would pick a different, equally valid reservation and silently break that tie.

## O. Step 10 — the test suite

`./run_tests.sh` group **[11]** covers this dataset — 20 checks:

```
[11] Second dataset (database/sql_large/02_data.sql)
  ok    database/sql_large/02_data.sql matches a fresh generation
  ok    235 sailors (got 235)
  ok    5 sailors never reserve a boat (got 5)
  ok    10 sailors rated 10 (got 10)
  ok    20 sailors older than 70 (got 20)
  ok    8 sailors unrated (got 8)
  ok    44 boats (got 44)
  ok    4 boats never reserved (got 4)
  ok    5000 reservations (got 5000)
  ok    3 years covered (got 3)
  ok    every (bid, day) is unique (got 5000)
  ok    every (sid, day) is unique (got 5000)
  ok    every year has days with no booking at all (2024: 101, 2025: 105, 2026: 61)
  ok    some days dominate: busiest 40 boats out vs a median day of 5
  ok    the busiest day nearly empties the fleet (40 boats)
  ok    summer dominates: 69.8% of bookings are June-August
  ok    every month of the year appears (12/12)
  ok    no future-dated bookings (latest 2026-08-17)
  ok    red and white are the two commonest colours
  ok    no tutorial rows leaked into the second dataset
```

Two of these deserve a note:

- **"matches a fresh generation"** regenerates the file in memory and compares
  it byte for byte. That is what makes the committed SQL trustworthy: a hand
  edit, or a specification change without a regeneration, fails here. It needs
  no database, so it runs even if you never build the second one.
- The rest **skip** with a message if `sailors_and_boats_large.duckdb` does not
  exist. The second database is optional; nothing else in the project depends on
  it.

## P. Using it

Every script takes a database path as its first argument, so the app and all
five notebooks run against this dataset unmodified:

```bash
./run_app.sh              sailors_and_boats_large.duckdb
./run_notebook_level_04.sh sailors_and_boats_large.duckdb
./run_tests.sh            sailors_and_boats_large.duckdb   # see the note below
```

Under the hood every one of them just exports `SAILORS_DB`, which
`sailors_db.DB_PATH` reads — the single place in the project where "which
database" is decided.

**Two Level 4 cells were written with this database in mind.** They are honest
but degenerate against the tutorial's single season, and become the questions
they were meant to be here:

| cell | tutorial database | this database |
|---|---|---|
| **Q11** — days per year nobody sailed | one season: 69 observed days, 9 booked, 60 idle | three years, ~100 idle days each, mostly winter |
| **Q12** — years ranked by bookings | one row, rank 1, 100% | 2025 (1,909) ahead of 2024 (1,734), 2026 still in progress at 1,357 |

Q12's `change_on_previous_year` is worth a look here: it uses `LAG` ordered by
*year* while `RANK` orders by *volume* — two different frames in one query,
which the single-season database cannot demonstrate at all.

Two things to expect:

- **The notebooks' prose describes the tutorial data.** "Fourteen sailors", "ten
  sailors tie at zero", "the only day with two boats out" — those sentences are
  facts about `database/sql/02_data.sql`. The *queries* are all correct here; the
  surrounding text is not about this database.
- **`./run_tests.sh <this database>` will fail**, and should. Most of the suite
  asserts tutorial-specific behaviour. Run it with no argument.

## Q. Changing the data — recipes

Every one of these is a constant, a regeneration, and a rebuild:

```bash
# edit src/generate_data_large.py, then:
./create_database_large.sh --regenerate --force --verify
```

| you want | change | watch out for |
|---|---|---|
| more/fewer reservations | `N_RESERVATIONS` | the ceiling is `bookable days × 40`; the generator raises rather than looping forever |
| a longer history | `SEASON_START` / `SEASON_END` | `SEASON_END` in the future gives forward-dated bookings, and the "no future bookings" test will fail |
| more empty days | `IDLE_DAYS_PER_YEAR` | capped internally at a third of the year |
| bigger regattas | `PEAK_SHARE` → 0.9, or `PEAK_DAYS_PER_YEAR` | peak totals must not exceed `N_RESERVATIONS` |
| a different season | `MONTH_WEIGHT` | the "summer dominates" test asserts June–August > 50% |
| a different fleet | `N_BOATS` + `COLOUR_MIX` | they must total; add hull names to `BOAT_NAMES` |
| a different colour balance | `COLOUR_MIX` | the "red and white are commonest" test |
| more sailors | `N_SAILORS` | 75 × 50 name combinations is the current ceiling |
| a different random marina | `SEED` | every number changes; the *proportions* do not |

If you change a proportion the tests assert (summer share, colour dominance),
update `tests/test_smoke.py` group [11] in the same commit — those checks exist
to catch accidental drift, so they should move deliberately.

## R. Determinism, and why the seed matters

`SEED = 20260817` is fixed, so:

- the same file comes out of every run — regenerating is a no-op unless the
  specification changed;
- `database/sql_large/02_data.sql` can be committed and diffed like source, and a change in
  it is a real change, not RNG noise;
- the test suite can compare the committed file against a fresh generation;
- the numbers quoted in this document stay true.

```bash
uv run python src/generate_data_large.py --check   # regenerate and compare, write nothing
```

Change the seed and you get a different marina with the same statistics: still
235 sailors, still exactly 10 rated 10, still ~70% summer.

## S. How it fails, and what it says

The generator refuses rather than producing quietly wrong data:

| message | cause |
|---|---|
| `COLOUR_MIX must total N_BOATS` | the colour counts do not add up |
| `need one hull name per boat` | `N_BOATS` exceeds `BOAT_NAMES` |
| `peak days alone exceed N_RESERVATIONS` | `PEAK_DAYS_PER_YEAR × PEAK_SHARE × capacity` is too big |
| `every bookable day is at capacity` | `N_RESERVATIONS` exceeds what the fleet and calendar can hold |
| `could not give sailor N a booking` | the repair pass could not find a donor row |
| `YEAR has only N idle days` | a change made the calendar denser than `IDLE_DAYS_PER_YEAR` |
| `busiest day (N) barely beats the median (M)` | peak days were diluted or removed |

And from the build script:

| message | cause |
|---|---|
| `a database already exists at …` | build without `--force`; it prints what the file holds first |
| `database/sql_large/02_data.sql is missing` | never generated — run with `--regenerate` |
| `error: no such SQL file: …` | a `--sql` path that does not exist |

## T. What the current dataset actually contains

Measured from the built database, not from intent:

| | |
|---|---|
| sailors | 235 — sid 1…235, 232 distinct names (3 shared by two sailors) |
| ratings | 10 sailors rated 10; 8 unrated (`NULL`); the rest spread over 1–9 |
| ages | 18.0 … 87.5, of which 20 are over 70 |
| boats | 44 — bid 101…144 — red 13, white 11, blue 7, green 6, yellow 4, black 3 |
| never book | 5 sailors; 4 boats never booked |
| reservations | 5,000 — 2024: 1,734 · 2025: 1,909 · 2026: 1,357 (to 17 August) |
| calendar | 960 days in the window, 691 with at least one booking |
| idle days | 2024: 103 · 2025: 105 · 2026: 61 — counted from 1 January. The suite reports 101 for 2024 because its calendar spine starts at the first booking, 3 January |
| busiest days | 2025-06-20 and 2026-07-01 with **40 boats out**; median day is **5** |
| summer | 3,489 of 5,000 bookings (**70%**) fall in June–August |
| per sailor | min 2, median 18, max 118 |
| per boat | min 80, max 169 |
| file sizes | `database/sql_large/02_data.sql` 5,333 lines / 186 KB; database 2.6 MB |
| generation time | ~0.2 s |

## U. Two bugs that shaped the generator

Both produced data that looked fine in a row count, and both are worth not
reintroducing:

**Three years without a single winter booking.** The first version apportioned
each day's share by rounding down and gave the remainder to the largest
fractional parts. Every winter day rounded to zero, and every leftover landed in
July — so the dataset had *no rows at all* between November and February, and
its first booking was 1 March rather than January. A marina that closes for
winter is plausible; one that has never taken a February booking in three years
is an arithmetic artefact. Bookings are now drawn one at a time, and idle days
are chosen deliberately instead of falling out of rounding.

**One sailor with 132 of the 2,000 bookings.** Sailor weights came from
`paretovariate(1.6)`, whose tail is heavy enough that a single sailor took 6.6%
of the marina's entire season. Now `lognormvariate(0, 0.62)`: still a long tail,
still regulars and occasionals, no boat-owner.

The lesson both times: **a row count proves nothing about shape.** That is why
the generator asserts its own distributions and why group [11] checks idle days,
month coverage and peak dominance rather than just `count(*)`.

## V. Gotchas

- **One writer.** DuckDB allows many readers *or* one writer. The app holds a
  writer, so a notebook cannot open the same file at the same time, and
  `./run_tests.sh` fails while the app is running. Point one of them at a copy.
- **Don't hand-edit `database/sql_large/02_data.sql`.** The suite regenerates and compares it;
  your edit will be reported as a failure and lost at the next `--regenerate`.
- **Don't move it into `database/sql/`.** See [C](#c-the-rule-that-shapes-everything-databasesql-is-a-glob).
- **`sailors_and_boats_large.duckdb` is git-ignored** by `*.duckdb*`, along with its
  WAL. The generated *SQL* is the artifact worth committing.
- **The app can write to this database too.** Registrations draw from
  `seq_sid`/`seq_bid` starting at 1000, which is why the generated ids stop at
  235 and 144.
- **Rebuilding discards app-written rows** — that is what `--force` is asking
  you to confirm.

## W. Where everything is defined

| what | where | note |
|---|---|---|
| database requirements R1–R10, P1–P3, D1–D2 | `database/sql/01_schema.sql`, `REQUIREMENTS` block | the only definition; everything else cites labels |
| the schema itself | `database/sql/01_schema.sql` | shared by both databases, unmodified |
| tutorial rows | `database/sql/02_data.sql` | never edited |
| this dataset's specification | `src/generate_data_large.py`, top of file | executable, so it cannot drift from the data |
| this dataset's rows | `database/sql_large/02_data.sql` | generated |
| how it is built | `create_database_large.sh` | and `build_database.py --sql` |
| what it must satisfy | `tests/test_smoke.py`, group [11] | 20 checks |
| the short version of this document | `README.md` §7.1 | entry point |
| why `reserves` is keyed `(bid, day)` | `DESIGN.md` §3 | the design argument, in full |
| instructions for Claude Code | `CLAUDE.md` | invariants and traps |
