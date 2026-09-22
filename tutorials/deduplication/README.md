# Identify Duplicates and Deduplication

Source problem: https://medium.com/@rakeshmakhijani77_66351/sql-interview-quickie-8-faang-identify-duplicates-and-deduplication-c950b3647302

This repo works through the two original interview questions, then extends
them into a small teaching set of related deduplication problems — each
with a working, DuckDB-verified SQL solution.

## 1. What Is Deduplication?

**Deduplication ("dedup")** is the process of finding rows in a table
that represent the same real-world thing and collapsing them down to a
single row, according to some rule for which copy to keep (or how to
combine them). It comes up constantly in practice: an `INSERT` that got
retried after a network timeout, an upstream system that emits the same
event twice, a form a user double-submitted, or — as in this exercise —
an application bug that let the same email sign up more than once.

Before writing a single dedup query, the question to answer is: **what
makes two rows "duplicates" of each other?** That's rarely "every single
column matches" — usually it's "some subset of columns matches, and we
don't care that the rest differ." This repo works with both flavors.

### 1.1 Dedup by a set of columns

Most real dedup problems are keyed on one column, or a small set of
columns, that's supposed to be unique — even though the table has other
columns that are allowed (even expected) to differ between the
"duplicate" rows. That's exactly Problems #1–#5 in this repo: two rows
with the same `email` count as duplicates *even though* their `status`
and `created_on` differ, and the actual problem is choosing which of
those differing rows to keep.

`ROW_NUMBER() OVER (PARTITION BY <key column(s)> ORDER BY <tiebreak>)` is
the standard SQL tool for this: it groups rows by the key, ranks each
group according to the tiebreak rule, and `rn = 1` (or `rn > 1`) marks the
row to keep (or discard) within each group. The key isn't limited to one
column, either — Problem #6 dedupes on the *pair* `(email, status)`, a
composite key, which changes which rows count as duplicates of one
another. See §7 and §8 for the full set of "dedup by column(s)" examples.

### 1.2 Dedup by the entire row

The other common case is an **exact-duplicate** row, where every single
column is identical — typically caused by a retried `INSERT`, a
double-submitted form, or a batch job re-run over data it already loaded.
There's no "different column values, pick a winner" decision to make
here: any one of the identical copies is as good as any other, so the
"tiebreak" is just "keep one, arbitrarily."

`users.user_id` is a primary key, so by construction no two rows in this
repo's `users` table can ever be full-row duplicates (`user_id` alone
already makes every row unique). To make whole-row dedup concrete, this
example uses its own tiny illustrative table with no surrogate key —
closer to what a raw event log or an un-deduped CSV import might look
like:

```sql
CREATE TABLE raw_events (
    email      VARCHAR,
    status     VARCHAR,
    created_on TIMESTAMP
);

INSERT INTO raw_events VALUES
('a@example.com', 'verified',     '2026-01-01 00:00:00'),
('a@example.com', 'verified',     '2026-01-01 00:00:00'),  -- exact duplicate row
('b@example.com', 'not-verified', '2026-01-01 00:00:00');

-- Option A: build a deduped copy with SELECT DISTINCT
CREATE TABLE raw_events_deduped AS
SELECT DISTINCT * FROM raw_events;

-- Option B: delete in place, keeping one arbitrary survivor per distinct row
-- (works even without a rowid/PK to break ties on, using GROUP BY on every column)
DELETE FROM raw_events
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM raw_events
    GROUP BY email, status, created_on
);
```

**Result** (verified against DuckDB): both options collapse the table
from 3 rows to 2 — the two identical `a@example.com` rows become one,
`b@example.com` is untouched since it had no duplicate:

| email          | status       | created_on          |
|----------------|--------------|----------------------|
| a@example.com  | verified     | 2026-01-01 00:00:00 |
| b@example.com  | not-verified | 2026-01-01 00:00:00 |

If you ran the same "delete unless it's the row with the smallest
identifier" query against the real `users` table — grouping by every
column *except* `user_id` (`GROUP BY email, status, created_on`) — it
would delete nothing, because no two rows in the sample data happen to
share identical `email`, `status`, *and* `created_on` values at once.
That's the key difference from §1.1: whole-row dedup can't lose
information by picking a winner, since the rows really are identical;
column-subset dedup always involves a policy decision about which
differing values to keep — which is what Problems #1–#8 below are all
about.

## 2. Scenario & Sample Data

Table `users (user_id PK, email, status, created_on)`. `email` is supposed
to be unique but the table has duplicate emails. `user_id` is an integer
primary key.

```sql
CREATE TABLE users
(
    user_id int PRIMARY KEY,
    email varchar(100),
    status varchar(50),
    created_on datetime
);

INSERT INTO users (user_id, email, status, created_on)
VALUES
(1,  'john@yahoo.com',   'not-verified', '2026-01-01 02:00:00'),
(2,  'john@yahoo.com',   'verified',     '2026-01-02 03:00:00'),
(3,  'john@yahoo.com',   'verified',     '2026-01-02 04:00:00'),
(4,  'john@yahoo.com',   'not-verified', '2026-01-02 05:00:00'),
(5,  'rakesh@yahoo.com', 'not-verified', '2026-01-01 02:00:00'),
(6,  'rakesh@yahoo.com', 'verified',     '2026-01-01 03:00:00'),
(7,  'rakesh@yahoo.com', 'verified',     '2026-01-01 04:00:00'),
(8,  'rakesh@yahoo.com', 'not-verified', '2026-01-01 07:00:00'),
(9,  'rakesh@yahoo.com', 'not-verified', '2026-01-02 08:00:00'),
(10, 'steve@gmail.com',  'not-verified', '2026-01-01 01:00:00');
```

## 3. Problems

- **Problem #1** — Write a DELETE query to remove duplicate emails while
  keeping the **oldest** entry (smallest `created_on`) for each email.
- **Problem #2** — Write a DELETE query to remove duplicate emails while
  keeping the **most recently verified** entry for each email.
- **Problem #3** — Write a DELETE query to remove duplicate emails while
  keeping the **most recent entry overall** (largest `created_on`,
  regardless of `status`) for each email. The mirror image of Problem #1.
- **Problem #4** — Write a DELETE query to remove duplicate emails while
  keeping the entry with the **highest-priority status** for each email,
  using a status hierarchy (e.g. `verified` > `pending` > `not-verified` >
  `banned`) instead of a plain verified/not-verified check, breaking ties
  with the most recent `created_on`. A generalization of Problem #2.
- **Problem #5** — Instead of cleaning up duplicates after the fact,
  **prevent** them from being written in the first place: add a `UNIQUE`
  constraint on `email` and use `INSERT ... ON CONFLICT` (upsert) logic so
  a duplicate `email` is rejected or merged into the existing row at
  insert time, rather than requiring a periodic `DELETE`.
- **Problem #6** — Dedupe on a **composite key** instead of `email` alone:
  treat `(email, status)` as the uniqueness key, so an email is allowed one
  `verified` row *and* one `not-verified` row, but not two rows with the
  same email **and** the same status.
- **Problem #7** — Dedupe on a **normalized value** of `email` rather than
  its raw text, so near-duplicate spellings (`John@Yahoo.com` vs.
  `john@yahoo.com `, or Gmail's `jane+promo@gmail.com` /
  `ja.ne@gmail.com` dot/plus-addressing) are recognized as the same email
  and collapsed together.
- **Problem #8** — **Merge, don't just delete**: before removing the
  duplicate rows, roll their information into the surviving row (e.g. keep
  the earliest `created_on` as the "signup date" but upgrade `status` to
  `verified` if *any* duplicate for that email was ever verified), so no
  information is silently lost by picking one row and discarding the rest.
- **Problem #9** — Dedupe by the **entire row**: instead of a key column
  like `email`, treat *every* column as the uniqueness key, so only
  byte-for-byte identical rows count as duplicates. The `ROW_NUMBER()` +
  `WITH` + `DELETE` version of the whole-row dedup introduced in §1.2.

## 4. Repository Files

| File                                       | Purpose                                                           |
|---------------------------------------------|--------------------------------------------------------------------|
| `db_setup.py`                               | Creates the DuckDB `users` table and seeds it with the sample data (Step 1). |
| `problem1_keep_oldest.py`                   | Solves Problem #1 (Step 2).                                       |
| `problem2_keep_most_recently_verified.py`   | Solves Problem #2 (Step 3).                                       |
| `run_problem1.sh`                           | Wrapper: builds the DuckDB `users` table, then runs Problem #1.   |
| `run_problem2.sh`                           | Wrapper: builds the DuckDB `users` table, then runs Problem #2.   |

Each problem script resets and reseeds the table before running so it can
be run independently, in any order, with reproducible output. Problems
#3–#9 are SQL-only teaching extensions (see §8) with no dedicated Python
script — run #3–#8 directly against `users.db`; #9 uses its own
`raw_events` table (see §8.7).

## 5. Requirements

```bash
pip install duckdb pandas
```

## 6. Usage

### One-shot wrapper scripts (recommended)

Each wrapper builds the DuckDB database and runs the matching dedup script
in one step:

```bash
./run_problem1.sh   # build DB + dedupe (keep oldest row per email)
./run_problem2.sh   # build DB + dedupe (keep most recently verified row per email)
```

### Or run the pieces individually

```bash
# Step 1: build the DuckDB database file (users.db) and inspect the seed data
python3 db_setup.py

# Step 2: Problem #1 — dedupe keeping the oldest row per email
python3 problem1_keep_oldest.py

# Step 3: Problem #2 — dedupe keeping the most recently verified row per email
python3 problem2_keep_most_recently_verified.py
```

## 7. Solutions — Problems #1 and #2

Both solutions delete rows in a single set-based `DELETE` statement — no
self-joins and no row-by-row loops in Python — by ranking each email's rows
with the `ROW_NUMBER()` window function and deleting everything except rank 1.
This is the standard efficient pattern for this class of problem: one sort
per `email` partition (`O(n log n)`), executed entirely inside DuckDB.

### 7.1 Problem #1 — keep the oldest row per email

```sql
DELETE FROM users
WHERE user_id NOT IN (
    SELECT user_id
    FROM (
        SELECT
            user_id,
            ROW_NUMBER() OVER (
                PARTITION BY email
                ORDER BY created_on ASC, user_id ASC
            ) AS rn
        FROM users
    ) ranked
    WHERE rn = 1
);
```

`user_id ASC` is a tiebreaker only (for rows with an identical `created_on`
within the same email) and doesn't change the result on this sample data.

**Result:**

| user_id | email             | status       | created_on          |
|---------|-------------------|--------------|----------------------|
| 1       | john@yahoo.com    | not-verified | 2026-01-01 02:00:00 |
| 5       | rakesh@yahoo.com  | not-verified | 2026-01-01 02:00:00 |
| 10      | steve@gmail.com   | not-verified | 2026-01-01 01:00:00 |

#### 7.1.1 Problem #1 alternative — `WITH` CTE form

The query above uses `NOT IN (subquery)` because it reads naturally as
"keep rank 1, delete the rest." The same logic can be expressed with a
`WITH` common table expression (CTE) instead of a nested subquery — some
people find this more readable, and it's the form you'll often see in
interview answers. DuckDB supports referencing a CTE directly inside a
`DELETE`'s `WHERE` clause, so the ranking logic only needs to be written
once, and here `rn > 1` marks the duplicates to remove directly (instead
of picking survivors via `rn = 1` and inverting with `NOT IN`):

```sql
WITH ranked AS (
    SELECT
        user_id,
        ROW_NUMBER() OVER (
            PARTITION BY email
            ORDER BY created_on ASC, user_id ASC
        ) AS rn
    FROM users
)
DELETE FROM users
WHERE user_id IN (SELECT user_id FROM ranked WHERE rn > 1);
```

Produces an identical result to §7.1 — the query plan DuckDB generates is
effectively the same either way; this is purely a style choice.

### 7.2 Problem #2 — keep the most recently verified row per email

```sql
DELETE FROM users
WHERE user_id NOT IN (
    SELECT user_id
    FROM (
        SELECT
            user_id,
            ROW_NUMBER() OVER (
                PARTITION BY email
                ORDER BY (status = 'verified') DESC, created_on DESC, user_id ASC
            ) AS rn
        FROM users
    ) ranked
    WHERE rn = 1
);
```

`(status = 'verified') DESC` sorts `verified` rows ahead of `not-verified`
rows within each email, and `created_on DESC` then picks the most recent one.
If an email has no `verified` rows at all (e.g. `steve@gmail.com`), the
ranking falls back to that email's most recent row, so every email still
ends up with exactly one row.

**Result:**

| user_id | email             | status       | created_on          |
|---------|-------------------|--------------|----------------------|
| 3       | john@yahoo.com    | verified     | 2026-01-02 04:00:00 |
| 7       | rakesh@yahoo.com  | verified     | 2026-01-01 04:00:00 |
| 10      | steve@gmail.com   | not-verified | 2026-01-01 01:00:00 |

#### 7.2.1 Problem #2 alternative — `WITH` CTE form

Same subquery-vs-CTE trade-off as §7.1.1, applied to Problem #2's ranking:

```sql
WITH ranked AS (
    SELECT
        user_id,
        ROW_NUMBER() OVER (
            PARTITION BY email
            ORDER BY (status = 'verified') DESC, created_on DESC, user_id ASC
        ) AS rn
    FROM users
)
DELETE FROM users
WHERE user_id IN (SELECT user_id FROM ranked WHERE rn > 1);
```

Produces an identical result to §7.2.

## 8. Extra Scenarios (Problems #3–#9)

Seven more dedup variants worth practicing in class, all built on the same
`ROW_NUMBER()` + `WITH` pattern from §7.1.1/§7.2.1 — what changes each time
is either the `PARTITION BY` key, the `ORDER BY` tiebreak, or (for #5 and
#8) the statement type itself. None of these have a dedicated Python
script; they are SQL-only and were each run and verified against DuckDB
before being written up here. Run them directly against `users.db` (e.g.
`duckdb users.db` at the command line, or `duckdb.sql(...)` in Python) —
except Problem #9, which (like §1.2) uses its own `raw_events` table
since `users.db`'s `user_id` primary key rules out whole-row duplicates
by construction.

### 8.1 Problem #3 — keep the most recent row overall

This is Problem #1 with the sort direction flipped: newest `created_on`
wins instead of oldest, and `status` is ignored entirely.

```sql
WITH ranked AS (
    SELECT
        user_id,
        ROW_NUMBER() OVER (
            PARTITION BY email
            ORDER BY created_on DESC, user_id ASC
        ) AS rn
    FROM users
)
DELETE FROM users
WHERE user_id IN (SELECT user_id FROM ranked WHERE rn > 1);
```

**Result:**

| user_id | email             | status       | created_on          |
|---------|-------------------|--------------|----------------------|
| 4       | john@yahoo.com    | not-verified | 2026-01-02 05:00:00 |
| 9       | rakesh@yahoo.com  | not-verified | 2026-01-02 08:00:00 |
| 10      | steve@gmail.com   | not-verified | 2026-01-01 01:00:00 |

### 8.2 Problem #4 — keep the highest-priority status

Problem #2 hard-codes a two-way `(status = 'verified') DESC` check. This
version replaces that with a `CASE` expression that ranks an arbitrary
number of status values, so it keeps working if `pending` or `banned`
statuses are introduced later — only the `CASE` needs updating, not the
overall query shape.

```sql
WITH ranked AS (
    SELECT
        user_id,
        ROW_NUMBER() OVER (
            PARTITION BY email
            ORDER BY
                CASE status
                    WHEN 'verified'     THEN 1
                    WHEN 'pending'      THEN 2
                    WHEN 'not-verified' THEN 3
                    WHEN 'banned'       THEN 4
                    ELSE 5
                END ASC,
                created_on DESC,
                user_id ASC
        ) AS rn
    FROM users
)
DELETE FROM users
WHERE user_id IN (SELECT user_id FROM ranked WHERE rn > 1);
```

**Result** (on this sample data, this matches Problem #2's result exactly,
since `verified` and `not-verified` are the only two statuses present —
the query only diverges from Problem #2 once a `pending` or `banned` row
shows up):

| user_id | email             | status       | created_on          |
|---------|-------------------|--------------|----------------------|
| 3       | john@yahoo.com    | verified     | 2026-01-02 04:00:00 |
| 7       | rakesh@yahoo.com  | verified     | 2026-01-01 04:00:00 |
| 10      | steve@gmail.com   | not-verified | 2026-01-01 01:00:00 |

### 8.3 Problem #5 — prevent duplicates at insert time (`INSERT ... ON CONFLICT`)

Problems #1–#4 are all *cleanup* queries: they assume the table already
has duplicate emails and `DELETE` down to one row per email. Problem #5 is
a different kind of fix — a *prevention* pattern that stops duplicate
emails from ever being inserted, so there's no periodic cleanup job to run
at all.

This requires a `UNIQUE` constraint on `email` (the schema in this repo
doesn't have one, since the assignment's whole premise is that duplicates
already got in). With that constraint in place, DuckDB's
`INSERT ... ON CONFLICT` clause can either silently reject a duplicate or
upsert it into the existing row:

```sql
CREATE TABLE users (
    user_id    INTEGER PRIMARY KEY,
    email      VARCHAR(100) UNIQUE,
    status     VARCHAR(50),
    created_on TIMESTAMP
);
```

**Option A — reject duplicates (`DO NOTHING`):** first write for an email
wins, every later insert for the same email is silently dropped.

```sql
INSERT INTO users (user_id, email, status, created_on)
VALUES (2, 'john@yahoo.com', 'verified', '2026-01-02 03:00:00')
ON CONFLICT (email) DO NOTHING;
```

**Option B — upsert, keep the most authoritative row (`DO UPDATE`):** if a
new row for an email is newer than what's stored, merge its `status` and
`created_on` into the existing row instead of rejecting it. This mirrors
the "keep most recent" logic from Problems #2–#4, but applied incrementally
at insert time instead of as a batch `DELETE`:

```sql
INSERT INTO users (user_id, email, status, created_on)
VALUES (2, 'john@yahoo.com', 'verified', '2026-01-02 03:00:00')
ON CONFLICT (email) DO UPDATE SET
    status     = EXCLUDED.status,
    created_on = EXCLUDED.created_on
WHERE EXCLUDED.created_on > users.created_on;
```

`EXCLUDED` refers to the row that was about to be inserted; the `WHERE`
clause makes this a conditional upsert so an older/stale insert can't
overwrite newer data. Verified against DuckDB: inserting
`(1, 'john@yahoo.com', 'not-verified', '2026-01-01 02:00:00')` followed by
`(2, 'john@yahoo.com', 'verified', '2026-01-02 03:00:00')` with the query
above leaves a single row — `user_id 1`, `status 'verified'`,
`created_on 2026-01-02 03:00:00` — i.e. the original `user_id` is kept,
but its `status`/`created_on` are updated from the newer insert.

**Trade-off vs. Problems #1–#4:** Problem #5 only stops *new* duplicates;
it does nothing about emails that are already duplicated. In practice
these two approaches are complementary — run a one-time `DELETE` (using
the Problem #1–#4 patterns) to clean up existing duplicates, then add the
`UNIQUE` constraint and switch inserts to `ON CONFLICT` so the table can't
drift back into having duplicates again.

### 8.4 Problem #6 — dedupe on a composite key (`email`, `status`)

Every earlier problem treats `email` alone as the uniqueness key, so each
email ends up with exactly one surviving row. Problem #6 changes the
*grain* of deduplication: the key is the pair `(email, status)`, so an
email is allowed to keep one `verified` row **and** one `not-verified`
row — it only collapses rows that share **both** the same email and the
same status. This is the pattern to reach for when two rows aren't true
duplicates unless several columns match, not just one.

The only change from the Problem #1/#3 query is the `PARTITION BY` clause:

```sql
WITH ranked AS (
    SELECT
        user_id,
        ROW_NUMBER() OVER (
            PARTITION BY email, status
            ORDER BY created_on DESC, user_id ASC
        ) AS rn
    FROM users
)
DELETE FROM users
WHERE user_id IN (SELECT user_id FROM ranked WHERE rn > 1);
```

**Result** (note `john@yahoo.com` and `rakesh@yahoo.com` each keep *two*
rows — their most recent `verified` row and their most recent
`not-verified` row — while `steve@gmail.com`, which only ever had one
status, still collapses to one row):

| user_id | email             | status       | created_on          |
|---------|-------------------|--------------|----------------------|
| 4       | john@yahoo.com    | not-verified | 2026-01-02 05:00:00 |
| 3       | john@yahoo.com    | verified     | 2026-01-02 04:00:00 |
| 9       | rakesh@yahoo.com  | not-verified | 2026-01-02 08:00:00 |
| 7       | rakesh@yahoo.com  | verified     | 2026-01-01 04:00:00 |
| 10      | steve@gmail.com   | not-verified | 2026-01-01 01:00:00 |

### 8.5 Problem #7 — dedupe on a normalized value of `email`

Real-world duplicate emails are often not byte-identical: capitalization
(`John@Yahoo.com` vs. `john@yahoo.com`), stray whitespace, or Gmail's
dot-insensitive / `+tag` addressing (`jane+promo@gmail.com`,
`ja.ne@gmail.com`, and `jane@gmail.com` all deliver to the same inbox) all
count as "the same email" to a human, but `ROW_NUMBER() PARTITION BY
email` alone would treat them as different groups and miss the duplicate
entirely. The fix is to partition by a **normalized key** computed from
`email`, not by `email` itself.

The sample `users` table doesn't contain any near-duplicate spellings, so
this example uses its own small illustrative table (`users_raw`) to make
the technique concrete — the same `normalized`/`keyed` CTE approach can be
layered onto the real `users` table's `email` column if messy data shows
up there too:

```sql
CREATE TABLE users_raw (
    user_id    INTEGER,
    email      VARCHAR,
    status     VARCHAR,
    created_on TIMESTAMP
);

INSERT INTO users_raw VALUES
(101, 'John@Yahoo.com',       'not-verified', '2026-01-01 02:00:00'),
(102, ' john@yahoo.com ',     'verified',     '2026-01-02 03:00:00'),
(103, 'jane+promo@gmail.com', 'not-verified', '2026-01-01 05:00:00'),
(104, 'jane@gmail.com',       'verified',     '2026-01-02 06:00:00'),
(105, 'ja.ne@gmail.com',      'not-verified', '2026-01-03 07:00:00');

WITH normalized AS (
    SELECT
        user_id, email, status, created_on,
        -- lowercase + trim everyone; for gmail.com addresses, also
        -- strip dots from the local part (Gmail ignores them)
        CASE
            WHEN LOWER(TRIM(email)) LIKE '%@gmail.com'
                THEN REPLACE(SPLIT_PART(LOWER(TRIM(email)), '@', 1), '.', '')
                     || '@gmail.com'
            ELSE LOWER(TRIM(email))
        END AS email_key
    FROM users_raw
),
keyed AS (
    -- strip a Gmail "+tag" suffix from the local part
    SELECT
        user_id, email, status, created_on,
        REGEXP_REPLACE(email_key, '\+[^@]*@', '@') AS email_key
    FROM normalized
),
ranked AS (
    SELECT
        user_id,
        ROW_NUMBER() OVER (
            PARTITION BY email_key
            ORDER BY created_on DESC, user_id ASC
        ) AS rn
    FROM keyed
)
DELETE FROM users_raw
WHERE user_id IN (SELECT user_id FROM ranked WHERE rn > 1);
```

**Result** (verified against DuckDB — all three Yahoo spellings collapse
to the newest, and all three Gmail dot/plus variants collapse to the
newest):

| user_id | email            | status       | created_on          |
|---------|------------------|--------------|----------------------|
| 102     | ` john@yahoo.com ` | verified     | 2026-01-02 03:00:00 |
| 105     | ja.ne@gmail.com  | not-verified | 2026-01-03 07:00:00 |

The surviving `email` value is still whatever raw text happened to be in
the winning row (e.g. the un-trimmed `' john@yahoo.com '`) — normalizing
for *comparison* doesn't automatically clean up the *stored* value. A
real fix would also `UPDATE email = email_key` on the survivor, or better,
normalize `email` before it's ever inserted (see Problem #5).

### 8.6 Problem #8 — merge duplicates into the survivor instead of discarding them

Every prior `DELETE`-based problem picks one row per email by some
ordering rule and throws the rest away — which means whatever information
lived only on a "losing" row is gone for good. Problem #1 keeps the
earliest signup but permanently forgets that the email was later
verified; Problem #2 keeps the verified row but loses the true original
`created_on`. Problem #8 asks: what if we want *both* — the earliest
`created_on` **and** the fact that the email was eventually verified?

The answer is a two-step **merge**, not a straight delete: first `UPDATE`
the row we're going to keep (the oldest one, same tiebreak as Problem #1)
so its `status` reflects the best status seen anywhere in its duplicate
group, *then* `DELETE` everything else. Because the ranking subquery only
looks at `email`/`created_on`/`user_id` — none of which the `UPDATE`
touches — it's safe to recompute the same "oldest row" ranking in both
statements.

```sql
-- Step 1: upgrade the survivor's status if any duplicate for that email
-- was ever verified, without touching created_on (the "signup date").
UPDATE users
SET status = 'verified'
WHERE status != 'verified'
  AND user_id IN (
      SELECT user_id
      FROM (
          SELECT
              user_id, email,
              ROW_NUMBER() OVER (
                  PARTITION BY email
                  ORDER BY created_on ASC, user_id ASC
              ) AS rn
          FROM users
      ) ranked
      WHERE rn = 1
  )
  AND email IN (SELECT email FROM users WHERE status = 'verified');

-- Step 2: now delete every non-survivor row, same as Problem #1.
DELETE FROM users
WHERE user_id NOT IN (
    SELECT user_id
    FROM (
        SELECT
            user_id, email,
            ROW_NUMBER() OVER (
                PARTITION BY email
                ORDER BY created_on ASC, user_id ASC
            ) AS rn
        FROM users
    ) ranked
    WHERE rn = 1
);
```

**Result** (verified against DuckDB): compare this to Problem #1's result
above — same surviving `user_id`s and the same (earliest) `created_on`
values, but `john@yahoo.com` and `rakesh@yahoo.com` now show `verified`
instead of `not-verified`, since both had a verified duplicate that would
otherwise have been silently discarded. `steve@gmail.com` is unchanged,
since it was never verified:

| user_id | email             | status       | created_on          |
|---------|-------------------|--------------|----------------------|
| 1       | john@yahoo.com    | verified     | 2026-01-01 02:00:00 |
| 5       | rakesh@yahoo.com  | verified     | 2026-01-01 02:00:00 |
| 10      | steve@gmail.com   | not-verified | 2026-01-01 01:00:00 |

This is the pattern to teach alongside straight `DELETE` dedup: whenever
"pick a winner" would throw away information you actually still need,
merge first, delete second.

### 8.7 Problem #9 — dedupe by the entire row (exact-duplicate rows)

§1.2 introduced whole-row dedup conceptually, with two quick options
(`SELECT DISTINCT` and a `GROUP BY`-every-column `DELETE`). This section
gives it the same `ROW_NUMBER()` + `WITH` + `DELETE` shape as Problems
#1–#8, so it's clear it's the *same tool*, just pointed at a different
`PARTITION BY` key: partition by **every column** instead of a single key
column like `email`. Two rows only rank against each other here if they
agree on all of them.

Since this table has no `user_id`-style primary key to break ties on (the
whole point is that duplicate rows are indistinguishable), the query uses
DuckDB's built-in `rowid` instead — the same tiebreaker §1.2's Option B
used:

```sql
WITH ranked AS (
    SELECT
        rowid,
        ROW_NUMBER() OVER (
            PARTITION BY email, status, created_on
            ORDER BY rowid ASC
        ) AS rn
    FROM raw_events
)
DELETE FROM raw_events
WHERE rowid IN (SELECT rowid FROM ranked WHERE rn > 1);
```

**Result** (verified against DuckDB, same `raw_events` seed data as §1.2):
identical to both §1.2 options — the two identical `a@example.com` rows
collapse to one, `b@example.com` is untouched:

| email          | status       | created_on          |
|----------------|--------------|----------------------|
| a@example.com  | verified     | 2026-01-01 00:00:00 |
| b@example.com  | not-verified | 2026-01-01 00:00:00 |

The `ROW_NUMBER()` form costs more than `SELECT DISTINCT` for this simple
case — it's overkill for pure whole-row dedup — but it's worth knowing
because real "whole-row" dedup is often "whole-row-except-a-timestamp":
swap the `PARTITION BY` list to the columns that must match and keep
`ORDER BY created_on DESC` (or similar) as the tiebreak, and this becomes
"keep the newest copy of each exact duplicate," which `SELECT DISTINCT`
can't express at all.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
