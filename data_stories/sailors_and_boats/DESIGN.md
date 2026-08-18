# Database design — Sailors & Boats

OMIS 105 · DuckDB · schema in [`database/sql/01_schema.sql`](database/sql/01_schema.sql)

> **Where the rules live.** Every database requirement is *defined* in one
> place: the `REQUIREMENTS` block at the top of
> [`database/sql/01_schema.sql`](database/sql/01_schema.sql), which lists R1–R10, P1–P3 and
> D1–D2 next to the constraint enforcing each. 
> 
> **This document does not
> redefine them** — it explains the reasoning and cites the labels. 
> 
> The SQL
> quoted below is illustrative; the schema file is authoritative.

---

## 1. The three tables

Three tables, two of them entities and one of them a relationship:

```
  sailors ──────< reserves >────── boats
   (who)         (who has          (what)
                what, when)
```

| table | one row is… | key | rows |
|---|---|---|---|
| `sailors` | one person | `sid` | 14 |
| `boats` | one hull | `bid` | 9 |
| `reserves` | **one boat, on one day** | **`(bid, day)`** | 10 |

The phrase in bold — the *grain* of `reserves` — is the whole design. Everything
below follows from it.

---

### `sailors`

```sql
CREATE TABLE sailors (
    sid     INTEGER      NOT NULL,
    sname   VARCHAR(32)  NOT NULL,
    rating  INTEGER,
    age     REAL,
    CONSTRAINT pk_sailors        PRIMARY KEY (sid),
    CONSTRAINT ck_sailors_rating CHECK (rating IS NULL OR rating BETWEEN 1 AND 10),
    CONSTRAINT ck_sailors_age    CHECK (age    IS NULL OR age    BETWEEN 0 AND 120),
    CONSTRAINT ck_sailors_sname  CHECK (length(trim(sname)) > 0)
);
```

| column | type | why |
|---|---|---|
| `sid` | `INTEGER` PK | **R6**. Identity lives here, not in the name. |
| `sname` | `VARCHAR(32)` NOT NULL | A name, not an identifier. The seed data has **two different sailors both called Horatio** (`sid` 64 and 74) — the standard demonstration that names are not keys. |
| `rating` | `INTEGER`, **nullable** | 1–10 skill level. Left nullable on purpose: the tutorial inserts sailor 99 'Dan' with a `NULL` rating, which is what makes `COUNT(*)` = 14 while `COUNT(rating)` = 13. |
| `age` | `REAL` | The textbook ages are fractional — 55.5, 25.5, 63.5. An `INTEGER` would silently destroy them. |

**Why `CHECK` on `rating` and `age`.** A rating of 40 or an age of −3 is not a
typo the application should catch politely; it is a value that must never exist
in the table, no matter which program does the inserting. Constraints that
protect the *meaning* of a column belong in the schema.

---

### `boats`

```sql
CREATE TABLE boats (
    bid     INTEGER      NOT NULL,
    bname   VARCHAR(32)  NOT NULL,
    color   VARCHAR(16)  NOT NULL,
    CONSTRAINT pk_boats       PRIMARY KEY (bid),
    CONSTRAINT ck_boats_bname CHECK (length(trim(bname)) > 0),
    CONSTRAINT ck_boats_color CHECK (color IN ('red','green','blue','white','black','yellow'))
);
```

| column | type | why |
|---|---|---|
| `bid` | `INTEGER` PK | **R7**. |
| `bname` | `VARCHAR(32)` NOT NULL | The model. Boats 101 and 102 are **both** `'Interlake'` — two hulls of one model are two boats. Same lesson as Horatio. |
| `color` | `VARCHAR(16)` NOT NULL + `CHECK` | The textbook treats colour as free text. Constraining it to a fixed vocabulary means `WHERE color = 'red'` can never miss a boat because someone typed `'Red'` or `' red '`. |

That `CHECK` on colour is a small decision with a large payoff: it turns "find
the red boats" from a query you have to *trust* into a query that is
*correct by construction*.

---

### `reserves` — the interesting one

```sql
CREATE TABLE reserves (
    sid     INTEGER  NOT NULL,
    bid     INTEGER  NOT NULL,
    day     DATE     NOT NULL,
    CONSTRAINT pk_reserves         PRIMARY KEY (bid, day),
    CONSTRAINT uq_reserves_sid_day UNIQUE (sid, day),
    CONSTRAINT fk_reserves_sid     FOREIGN KEY (sid) REFERENCES sailors(sid),
    CONSTRAINT fk_reserves_bid     FOREIGN KEY (bid) REFERENCES boats(bid)
);
```

**The tutorial PDF is wrong for our requirements.** It declares:

```sql
CONSTRAINT PK_reserves PRIMARY KEY (sid, bid, day)   -- from the PDF
```

Under that key, both of these rows are accepted:

| sid | bid | day |
|---|---|---|
| 22 | 101 | 1998-10-10 |
| 29 | 101 | 1998-10-10 |

They differ in `sid`, so the triple `(sid, bid, day)` is unique — and boat 101
has just been handed to two sailors on the same morning. R2, R3 and R4
all say that must be impossible.

**The fix is to key on the slot, not on the row.** A boat is a physical object.
On a given day it is out with at most one sailor. So the thing that identifies a
reservation is *which boat, on which day* — and `sid` is an attribute of that
slot recording **who holds it**:

```sql
PRIMARY KEY (bid, day)
```

Read it as a sentence: *for each boat and each day there is at most one row, and
that row names the sailor who has it.*

| column | type | why |
|---|---|---|
| `bid` | part of PK, FK → `boats` | Which boat is out. |
| `day` | part of PK and of `UNIQUE (sid, day)`, `DATE` | Which day it is out. |
| `sid` | `NOT NULL`, FK → `sailors`, `UNIQUE (sid, day)` | Who has it. Not part of the key, but not unconstrained either. |

**And one more constraint on top.** The key settles the boat side of the
relationship; R10 settles the sailor side, and needs its own
declaration:

```sql
UNIQUE (sid, day)
```

Read as a sentence: *for each sailor and each day there is at most one row, and
that row names the boat they took.* Section 2 works through why this does not
follow from the primary key, and section 3 through why it nonetheless leaves
`(sid, bid, day)` redundant.

**Why `DATE` and not the PDF's `datetime`.** R5 fixes the format at
`YYYY-MM-DD`, and DuckDB's `DATE` both parses and prints exactly that, so
`'1998-10-10'` round-trips unchanged and `'1998-13-45'` is rejected by the type
system before any constraint runs. A `datetime` would carry a time component,
and then `1998-10-10 00:00` and `1998-10-10 09:30` would look like two different
days to the primary key — quietly reopening the double-booking hole we just
closed.

**Why the foreign keys.** A reservation naming a sailor or a boat that does not
exist is not data, it is a bug. The FKs make it unrepresentable.

---

## 2. Requirement-by-requirement

> **The requirements themselves are not restated here.** Every database
> requirement — R1–R10, the population requirements P1–P3, and the derived
> rules D1–D2 — is defined in exactly one place, the `REQUIREMENTS` block at
> the top of [`database/sql/01_schema.sql`](database/sql/01_schema.sql), together with the
> constraint that enforces each one. Read that block first; this document
> explains the reasoning behind it and refers to the rules by label.
>
> If a rule and this document ever disagree, the schema file is right.

The headline is that **R2, R3, R4, R8 and R9 are all delivered by one
constraint**, `PRIMARY KEY (bid, day)`. That is the sign the grain was chosen
correctly: when the key matches what a row actually *means*, the rules stop
being a checklist and become a consequence.

R10 is the exception that proves it, and it is worth dwelling on. It is the
only rule the primary key does **not** deliver, because it is the only rule
that constrains the *sailor* side of the relationship. `(bid, day)`
answers "how many sailors may hold this boat today?" — one. It has nothing to
say about "how many boats may this sailor hold today?", and so it permits:

```
(22, 101, '1998-10-10')     -- Dustin takes the blue Interlake
(22, 102, '1998-10-10')     -- ...and the red one, the same day
```

Two different `(bid, day)` slots, so the key is satisfied. `UNIQUE (sid, day)`
is the mirror constraint, and it is genuinely a second one — neither implies
the other:

| | `PRIMARY KEY (bid, day)` alone | with `UNIQUE (sid, day)` |
|---|---|---|
| two sailors, one boat, one day | rejected ✓ | rejected ✓ |
| one sailor, two boats, one day | **accepted** ✗ | rejected ✓ |
| one sailor, one boat, two days | accepted ✓ | accepted ✓ |
| two sailors, two boats, one day | accepted ✓ | accepted ✓ |

Together they make any single day a **one-to-one matching** between the sailors
who are out and the boats that are out: each boat has at most one sailor, each
sailor has at most one boat. That is a stronger and more useful statement than
either constraint alone, and it is why `count(*)` over one day counts sailors
and boats simultaneously.

Every one of these is demonstrated — not asserted — by
`uv run python src/build_database.py --verify`, which tries each forbidden
insert in turn and prints the database's own rejection.

---

## 3. R9: is `UNIQUE (sid, bid, day)` redundant?

R9 asks whether `(sid, bid, day)` should be declared unique, or whether that is
redundant. (For the wording of the rule, see the `REQUIREMENTS` block in
[`database/sql/01_schema.sql`](database/sql/01_schema.sql); the short answer also lives there, as
note **[C]**. This section is the long-form argument behind it.)

**It is redundant.** It is not wrong, and it is not harmful to *think* about —
it is simply implied by a constraint we already have, so declaring it forbids
nothing new.

### The argument

A uniqueness constraint on a set of columns `K` says: no two rows agree on all
of `K`. Now take any superset `K ⊇ K'` where `K'` is already unique. If two rows
agreed on every column of `K`, they would in particular agree on every column of
`K'` — which `K'`'s uniqueness has already ruled out. So **any superset of a
unique column set is automatically unique.**

Here `K' = (bid, day)` is the primary key, and `K = (sid, bid, day) ⊇ K'`.
Therefore `(sid, bid, day)` is *already* unique. Adding the constraint changes
the set of accepted databases by exactly nothing, while costing a second index
and its maintenance on every insert, update and delete.

R10 makes the point twice over. `(sid, day)` is *also* a subset of
`(sid, bid, day)`, so the triple is now implied independently by each of our two
constraints — either one alone is enough to rule it out. A constraint that two
separate constraints already guarantee is not a close call.

Note the contrast, because it is the whole lesson of this section: `(sid, day)`
and `(bid, day)` are each a *subset* of the triple, so each one **implies** it
and it stays redundant. But neither is a subset of the *other*, which is why
both of them must be declared. Redundancy is about the subset relation, not
about how similar two constraints look.

### Redundant is not the same as sufficient

The most common question this section gets is the reverse of R9: *if the triple
is implied anyway, why not simply declare `PRIMARY KEY (sid, bid, day)` — the
PDF's key — and drop the other two? Wouldn't one key covering all three columns
be the strongest of the lot?*

It would be the **weakest**, and it enforces neither half of the requirement.

**The rule that makes this counter-intuitive.** A `UNIQUE` or `PRIMARY KEY` on a
column list forbids exactly one thing: two rows agreeing on **every** column in
the list. Rows that differ in even one of them are legal. So each column you add
to a key gives rows one more way to differ, and differing is what makes them
legal:

> **The wider the key, the weaker the constraint.**

`(sid, bid, day)` is the widest of the three keys under discussion, so it is the
weakest. What it forbids is the *identical triple* — the same sailor booking the
same boat on the same day twice, which is a duplicate-row rule rather than a
business rule. Nobody was trying to do that anyway.

**Worked example — one day, four inserts, three surviving rows.** Take
1998-10-10, and try to insert these in order under
`PRIMARY KEY (sid, bid, day)`:

| # | sid | sailor | bid | boat | day | accepted? |
|---|---|---|---|---|---|---|
| 1 | 22 | Dustin | 101 | Interlake (blue) | 1998-10-10 | accepted — the baseline booking |
| 2 | 22 | Dustin | 102 | Interlake (red) | 1998-10-10 | **accepted** ✗ — differs from #1 in `bid` |
| 3 | 29 | Brutus | 101 | Interlake (blue) | 1998-10-10 | **accepted** ✗ — differs from #1 in `sid` |
| 4 | 22 | Dustin | 101 | Interlake (blue) | 1998-10-10 | rejected — identical to #1 |

The table that results is a database in which **Dustin is out in two boats at
once** (rows 1 and 2, which R10 forbids) and **boat 101 has been handed to both
Dustin and Brutus on the same morning** (rows 1 and 3, which R2, R3 and R4
forbid). The only insert the key stopped was row 4, the exact duplicate — the
one case nobody needed protection from.

Run it yourself; it takes no database and touches nothing. The fourth `INSERT`
is *meant* to raise — the `duckdb` CLI reports it and carries on, so the closing
`SELECT` shows what got through:

```sql
CREATE TABLE reserves_pdf (
    sid INTEGER NOT NULL,
    bid INTEGER NOT NULL,
    day DATE    NOT NULL,
    PRIMARY KEY (sid, bid, day)          -- the tutorial PDF's key
);
INSERT INTO reserves_pdf VALUES (22, 101, DATE '1998-10-10');   -- ok
INSERT INTO reserves_pdf VALUES (22, 102, DATE '1998-10-10');   -- ok: Dustin in two boats
INSERT INTO reserves_pdf VALUES (29, 101, DATE '1998-10-10');   -- ok: boat 101 to two sailors
INSERT INTO reserves_pdf VALUES (22, 101, DATE '1998-10-10');   -- ConstraintException
SELECT * FROM reserves_pdf;                                     -- three rows, both rules broken
```

```
┌───────┬───────┬────────────┐
│  sid  │  bid  │    day     │
├───────┼───────┼────────────┤
│    22 │   101 │ 1998-10-10 │   -- Dustin has the blue Interlake…
│    22 │   102 │ 1998-10-10 │   -- …and the red one, same day     (R10 broken)
│    29 │   101 │ 1998-10-10 │   -- Brutus has the blue one too    (R2/R3/R4 broken)
└───────┴───────┴────────────┘
```

Piping a file in — `duckdb < scratch.sql` — works too: the CLI reports the
constraint error and moves on to the `SELECT`. Driving it from Python does
**not**, because a single `duckdb.sql(...)` call raises on the fourth statement
and never reaches the fifth; run the statements one at a time there.

**One rule, one constraint.** The requirement is two independent English
sentences, so it needs two constraints. Read each key as the sentence it
asserts:

| constraint | reads as | the example it forbids | the example it permits |
|---|---|---|---|
| `PRIMARY KEY (bid, day)` | a boat on a day has **one** sailor | boat 101 to Dustin (22) *and* Brutus (29) on 1998-10-10 | Dustin in boats 101 and 102 on 1998-10-10 |
| `UNIQUE (sid, day)` | a sailor on a day has **one** boat | Dustin in boats 101 and 102 on 1998-10-10 | boat 101 to Dustin *and* Brutus on 1998-10-10 |
| `PRIMARY KEY (sid, bid, day)` | a (sailor, boat, day) triple appears **once** | Dustin in boat 101 twice on 1998-10-10 | *both* of the above |

Each of the first two permits precisely what the other forbids, which is another
way of saying neither implies the other — the boat-side key says nothing about
how many boats one sailor holds, and the sailor-side key says nothing about how
many sailors one boat serves. Drop either and the matching hole reopens; that is
why `UNIQUE (sid, day)` is called the *mirror* constraint rather than a tidier
spelling of the primary key.

**A useful sanity check on the whole design.** The tutorial's own Figure 1 data
*cannot load* under our schema: it gives Dustin both boat 101 and boat 102 on
1998-10-10 — row 2 of the worked example above. Section 5 explains how that one
reservation was moved to 1998-10-09 rather than dropped. Turned around, this is
the sharpest argument in the section: **the PDF's key is the reason the PDF's
data violates the requirement.** Re-key to `(sid, bid, day)` and the offending
row loads exactly as printed.

### It goes only one way

The implication does **not** run backwards, and that is precisely why the PDF's
schema fails our requirements:

| | `UNIQUE (sid, bid, day)` | `PRIMARY KEY (bid, day)` | + `UNIQUE (sid, day)` |
|---|---|---|---|
| Dustin books 101 twice on 1998-10-10 | rejected | rejected | rejected |
| Dustin *and* Brutus both book 101 on 1998-10-10 | **accepted** ✗ | rejected ✓ | rejected ✓ |
| Dustin books 101 and 102 on 1998-10-10 | **accepted** ✗ | **accepted** ✗ | rejected ✓ |
| Dustin books 101 on the 10th and the 11th | accepted ✓ | accepted ✓ | accepted ✓ |

`(bid, day)` is *strictly stronger* than the triple. It catches everything the
triple catches, plus the case the triple misses — which happens to be the case
the assignment was actually worried about. Adding `UNIQUE (sid, day)` closes the
remaining row, the one no single constraint in the first two columns can reach.

### So R8 comes free

R8 is the first row of that table. Two such reservations would be two rows with
the same `bid` and the same `day`, and the primary key rejects the second one
without ever looking at `sid`.

### The verdict

Declaring `UNIQUE (sid, bid, day)` would be defensible only as documentation —
and a comment does that job for free, which is exactly what
[`database/sql/01_schema.sql`](database/sql/01_schema.sql) does:

```sql
--     CONSTRAINT uq_reserves_sid_bid_day UNIQUE (sid, bid, day)   -- redundant
```

### The one thing to double-check

`(bid, day)` is the right key **because a reservation covers a whole day**. If
the marina ever moved to morning and afternoon slots, the grain would change to
*one boat, one day, one time-slot*, and the key would become
`(bid, day, slot)` — still not `(sid, bid, day)`. The key tracks the grain; it
never tracks the row's attributes.

---

## 4. What the schema deliberately still allows

Constraints should forbid what is impossible, not what is merely unusual. These
are all legal, and all of them appear in the data:

* **Two sailors, two boats, same day.** Both Horatios (64 and 74) are on the
  water on 1998-09-08, in the Interlake and the Clipper. A day holds as many
  reservations as there are hulls; what it cannot hold is two of them naming
  the same boat, or two of them naming the same sailor. Query Q6 in the
  notebook finds exactly this.
* **One boat, many days.** Boat 103 is out on 1998-09-08, 1998-10-08 and
  1998-11-06 under three different sailors.
* **Two sailors with the same name.** Horatio 64 and Horatio 74.
* **Two boats with the same name.** Interlake 101 and Interlake 102.
* **A sailor with no rating.** Dan (99), `rating IS NULL`.
* **A sailor who never sails, and a boat nobody books.** Deliberately seeded —
  see below.

---

## 5. The data

### From the tutorial PDF (`sailors_and_boats_SQL_Tutorial.pdf`)

* **10 sailors** from Figure 1, plus sailor 99 'Dan' (unrated) from the
  NULL / OUTER JOIN section on p. 7.
* **4 boats** from Figure 1: Interlake (101, blue), Interlake (102, red),
  Clipper (103, green), Marine (104, red).
* **10 reservations** from Figure 1, dates normalised to `YYYY-MM-DD`
  (`1998-10-8` → `1998-10-08`). Every `(bid, day)` pair in that data is already
  distinct, so the tutorial's own rows satisfy the stricter key unchanged —
  with one exception, below.

**The one row that had to move.** Figure 1 gives Dustin (22) *both* boat 101 and
boat 102 on 1998-10-10 — precisely the pattern R10 forbids, and the
worked example in section 2. The tutorial's own data will not load under our
schema, which is worth saying out loud to students rather than hiding: a new
business rule can invalidate existing data, and someone has to decide what
happens to it.

The reservation of boat 102 was moved back one day, to **1998-10-09**, rather
than deleted. That choice preserves everything the PDF's answers depend on —
all 10 rows, every (sailor, boat) pairing, every sailor's reservation count, and
the October grouping — so only queries that group on that exact date differ, and
only for that one row. Deleting it would have changed Dustin's count from 4 to 3
and quietly broken several worked answers.

### Added for the assignment

* **5 boats nobody has ever reserved** — 105 Sunfish, 106 Catalina, 107 Laser,
  108 Optimist, 109 Windseeker.
* **3 sailors who have never reserved anything** — 96 Popeye, 97 Olive,
  98 Wendy — joining Dan (99), who also never books.

These rows are the point of the outer-join and `NOT EXISTS` material: they are
invisible to every inner join in the notebook and appear only when a query is
written to look for absence.

**No reservations were added, and of the tutorial's ten only the one date above
was changed.** That is deliberate: every worked answer in the PDF still
reproduces here exactly, and the counts are untouched even by that edit. The
new sailors were even given ratings (4, 5, 6) that no tutorial sailor holds, so
each forms a group of one and the PDF's `GROUP BY … HAVING COUNT(*) > 1` answer
(3 → 44.5, 7 → 40, 8 → 40.5, 10 → 25.5) comes back character for character.

---

## 6. Two design notes on DuckDB

**Constraints must be declared inside `CREATE TABLE`.** DuckDB does not support
`ALTER TABLE … ADD CONSTRAINT`, so there is no bolting a key on afterwards. The
schema file declares everything up front and drops tables child-first to respect
the foreign keys.

**One writer at a time.** DuckDB allows many reader processes *or* one writer
process, and within a single process every connection to a file must share the
same settings. So the notebook connects read-only and the Streamlit app holds a
single writable connection — and the two cannot be open on the same file
simultaneously. Close one before starting the other.

---

## 7. Verifying the design

```
uv run python src/build_database.py --verify
```

Ten forbidden inserts, each one attempted for real inside a transaction that is
rolled back, each one rejected by the database with its own error message. The
same attempts are available interactively on the **Constraint playground** page
of the Streamlit app — press a button, watch the schema refuse.

The full suite, which also exercises the write helpers and renders every
Streamlit page:

```
uv run python tests/test_smoke.py
```
