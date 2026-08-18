# Concept index — what is taught where

Three tables, one relationship, **71 queries**. This is the map from an idea to
the cell that teaches it, and to the trap that makes it worth teaching.

**How to read a reference.** `G Q14` is the guided notebook,
[`notebooks/notebook_guided.py`](notebooks/notebook_guided.py),
query 14. `L3 Q9` is [`notebooks/notebook_level_03.py`](notebooks/notebook_level_03.py),
query 9.

| code | notebook | queries |
|---|---|---|
| **G** | `notebook_guided.py` — the guided tour | Q1–Q17, Q18 (alias lesson), Q19–Q28 |
| **L1** | `notebook_level_01.py` — one table at a time | Q1–Q10 |
| **L2** | `notebook_level_02.py` — the three tables together | Q1–Q10 |
| **L3** | `notebook_level_03.py` — combinations and absences | Q1–Q10 |
| **L4** | `notebook_level_04.py` — division, windows, reshaping | Q1–Q12 |

**This file points; it does not explain.** The explanation lives in the notebook
cell, next to the SQL it is about, and a database *requirement* lives only in
the `REQUIREMENTS` block of
[`database/sql/01_schema.sql`](database/sql/01_schema.sql). What is written here
is a location and a one-line reason — so this index cannot drift into being a
second, staler copy of the course.

---

## Contents

- [1. Filtering rows](#1-filtering-rows)
- [2. NULL](#2-null)
- [3. Ordering, and what counts as an answer](#3-ordering-and-what-counts-as-an-answer)
- [4. Aggregation and grouping](#4-aggregation-and-grouping)
- [5. Joins](#5-joins)
- [6. Subqueries](#6-subqueries)
- [7. Set operations](#7-set-operations)
- [8. Relational division — "for all"](#8-relational-division--for-all)
- [9. Window functions](#9-window-functions)
- [10. Dates, and calendars that do not exist](#10-dates-and-calendars-that-do-not-exist)
- [11. Reshaping results](#11-reshaping-results)
- [12. The schema as a teaching instrument](#12-the-schema-as-a-teaching-instrument)
- [13. Lessons that come from the data's shape](#13-lessons-that-come-from-the-datas-shape)
- [14. Reading a result honestly](#14-reading-a-result-honestly)
- [Teaching paths](#teaching-paths)

---

## 1. Filtering rows

| concept | where | the trap |
|---|---|---|
| `WHERE` as a row filter | L1 Q1, G Q2 | it runs before anything you can see, including aliases |
| strict vs inclusive comparison | L1 Q1 | `age < 40` drops the sailor who is exactly 40 |
| equality on text | L1 Q3, G Q2 | `'red'` ≠ `'Red'`; here a `CHECK` makes the wrong case unstorable |
| `IN` as a list of equalities | L1 Q4 | English "red **and** green" is SQL `OR`; `AND` returns nothing, silently |
| `BETWEEN` | L1 Q10 | inclusive at both ends — the classic double-counted boundary day |
| `LIKE` with anchors | L2 Q4, G Q22 | `'b%'` and `'%b'` need case folding, or Bob matches nothing |
| a length guard on a pattern | L2 Q4, G Q22 | "begins and ends with B" would otherwise accept a two-letter name |

## 2. NULL

| concept | where | the trap |
|---|---|---|
| NULL is *unknown*, not false | L1 Q2 | `WHERE rating > 7` and `WHERE rating <= 7` together do **not** cover the crew |
| `IS NULL` vs `= NULL` | L1 Q2 | `= NULL` matches nothing, not even another NULL |
| `count(*)` vs `count(column)` | L1 Q8, L2 Q7, G Q3 | the difference between them *is* the number of NULLs |
| aggregates skip NULL | L1 Q8, L3 Q8, G Q10 | an average is silently an average *of the rows that had a value* |
| NULL in a `NOT IN` subquery | **L3 Q9**, L2 Q10 | one NULL empties the whole result, with no error and no hint |
| NULL from a window with no previous row | L4 Q6, L4 Q12, G Q15 | "no previous outing" and "zero days" must not look alike |
| excluding NULL from an axis | L2 Q5, G Q10 | "unrated" is not a point on a 1–10 scale |

## 3. Ordering, and what counts as an answer

| concept | where | the trap |
|---|---|---|
| `ORDER BY` makes output stable | L1 Q1, G Q1 | without it the database may return rows in any order, and the order can change between runs |
| `ORDER BY` as the answer itself | L1 Q9 | the same rows, arranged, *are* the finding |
| `LIMIT 1` for an extreme | L1 Q5 | it promises **one row**, not *the* answer — a tie is invisible |
| the tie-safe form | L1 Q6, L2 Q5, G Q25, G Q26 | `WHERE x = (SELECT max(x) …)` returns everybody who ties |
| ranking instead of truncating | L3 Q3, L3 Q4 | `LIMIT 3` over a ten-way tie returns three rows chosen by nothing |
| NULL placement in a sort | L1 Q9 | `NULLS FIRST` / `NULLS LAST` is how you say which end you meant |
| the result's order ≠ a window's order | **L4 Q12**, L3 Q7 | one query can rank by volume while looking back by year |

## 4. Aggregation and grouping

| concept | where | the trap |
|---|---|---|
| first `GROUP BY` | L1 Q7 | every selected column must be grouped or aggregated — there is no "the" bid for two blue boats |
| the whole table as one group | L1 Q8 | no `GROUP BY` at all still returns exactly one row |
| `HAVING` vs `WHERE` | L2 Q3, G Q7, G Q20 | a fact about a *group* cannot be tested before the group exists |
| `count(DISTINCT …)` | L2 Q3, L2 Q7, G Q20, G Q27 | "two boats" is about distinct hulls, not row count |
| conditional aggregation with `FILTER` | L2 Q8, G Q28 | the readable form of `sum(CASE WHEN … THEN 1 ELSE 0 END)` |
| `string_agg` to keep the detail | L1 Q7, L3 Q7, G Q19 | how a grouped answer can still show its working |
| grouping on an id, displaying a name | **L3 Q5** | grouping by name merges the two Horatios into one sailor, and nothing looks wrong |
| grouping by a derived value | L3 Q8, L2 Q9, L4 Q11 | `CASE` bands and `extract(year …)` are columns that do not exist in the table |
| ordering groups by value, not label | L3 Q8 | `'25 to 39'` sorts before `'under 25'` as text |

## 5. Joins

| concept | where | the trap |
|---|---|---|
| the three-table join | L2 Q2, G Q4 | start at `sailors`, step through `reserves`, filter on `boats` |
| a missing `ON` clause | L2 Q2 | 14 × 10 × 9 = 1,260 rows of nonsense, and no error message |
| joins multiply rows | L2 Q1, L2 Q2, G Q4 | four reservations make four Dustins; `DISTINCT` is doing real work |
| `LEFT JOIN` keeps the unmatched | **L2 Q10**, L1 Q9→L2, G Q8, G Q9 | an inner join deletes ten sailors and five boats without saying so |
| the same question from both sides | G Q8 vs **G Q21** | one keeps everybody and shows the gaps; the other keeps only those who appear |
| `count(column)` after a `LEFT JOIN` | L2 Q10, L4 Q1, G Q8 | `count(*)` scores a never-booked boat 1, because the row is still there |
| joining to a **distinct** subquery | **L4 Q11** | joining `reserves` directly counts *reservations*, not days — 69 days becomes 70 rows |
| self-join | G Q6 | two rows of the same table, aliased apart; here it must compare sailors, not one sailor's boats |
| `CROSS JOIN` to build the complete set | **L3 Q10** | every pair that *could* exist, so the missing ones can be subtracted |

## 6. Subqueries

| concept | where | the trap |
|---|---|---|
| scalar subquery | L1 Q6, L3 Q7, L4 Q1 | runs once, yields one value, compares against it |
| subquery in a `WHERE … IN` | L3 Q1, L3 Q2 | the set-membership form |
| correlated subquery | L3 Q9, L4 Q2, L2 Q1 | mentions the outer row, so it is a different question per row |
| `EXISTS` vs `JOIN … DISTINCT` | **L2 Q1**, G Q5, G Q21 | `EXISTS` answers yes/no and stops early; the join builds rows to throw away |
| a subquery in the `SELECT` list | **G Q13** | one number per row without a `LEFT JOIN … GROUP BY` |
| `NOT EXISTS` for "never" | L3 Q9, L2 Q10, L4 Q2 | the safe way to ask an absence question |
| `NOT IN` and NULL | **L3 Q9** | correct only while the subquery cannot produce NULL |
| three spellings of one question | **G Q5** | `IN`, `EXISTS` and a join, side by side, same answer |

## 7. Set operations

| concept | where | the trap |
|---|---|---|
| `UNION ALL` to stack answers | L2 Q6, G Q19 | same column count, same order, compatible types; names come from the first branch |
| a tag column to label the branch | **L2 Q6**, G Q19 | without it, two rows with no way to tell which is which |
| `UNION` vs `UNION ALL` | L2 Q6 | plain `UNION` sorts and de-duplicates — work you usually do not need |
| `INTERSECT` for "both" | **L3 Q1**, G Q23 | "red and green" is not `AND`; no single row is both colours |
| `EXCEPT` for "but not" | **L3 Q2**, G Q24 | it also de-duplicates, so no `DISTINCT` is needed |
| set operators compare whole rows | L3 Q2 | pull a name into the `EXCEPT` and you change what "the same row" means |

## 8. Relational division — "for all"

| concept | where | the trap |
|---|---|---|
| the double `NOT EXISTS` | **L4 Q2**, G Q14 | "has them all" = *there is no X that is missing* |
| the `EXCEPT` formulation | G Q14, G Q19 | subtract what they have from what exists; empty means they had it all |
| the counting formulation | **L4 Q1**, G Q14 | `count(DISTINCT …) = (SELECT count(*) …)`, usually the fastest |
| the divisor decides the answer | L4 Q1 vs L4 Q2, G Q19 | "every boat" is nobody; "every red boat" is two sailors |
| an empty divisor | L4 Q2 | with nothing to be missing, *everyone* qualifies — logic, not a bug |
| division over a computed divisor | **L4 Q3** | the set of years is read out of the data itself |
| division seen from the other side | **L3 Q10** | count what each sailor is *missing*; zero missing = has them all |

## 9. Window functions

| concept | where | the trap |
|---|---|---|
| a window keeps the rows a `GROUP BY` would destroy | L4 intro, G Q15 | "what is true of this group" vs "where does this row sit in it" |
| `OVER ()` — the whole result | **L4 Q7**, G Q17 | the denominator for a percentage, computed in the same pass |
| `OVER (ORDER BY …)` — a running frame | **L4 Q4** | the default frame is what makes a total cumulative |
| an aggregate *inside* a window | **L4 Q4**, L4 Q12 | `sum(count(*)) OVER (…)` reads like a typo and is not |
| `PARTITION BY` | L4 Q6, G Q15 | without it, one boat's gap spans two different hulls |
| `LAG` | L4 Q6, L4 Q12, G Q15 | the first row of each partition has no previous row, so NULL |
| `ROW_NUMBER` vs `RANK` vs `DENSE_RANK` | **L4 Q5** | identical until a tie; `ROW_NUMBER` always returns "exactly N rows" and looks authoritative |
| ranking a `GROUP BY` | **L4 Q12**, L3 Q3, L3 Q4 | after grouping, a window can only see grouping expressions and aggregates |
| `QUALIFY` | **L4 Q10** | `WHERE` runs before the window exists; `QUALIFY` is to windows what `HAVING` is to aggregates |
| top-N-per-group | L4 Q10 | `ROW_NUMBER() = 1` per partition, with a deterministic tiebreaker |

## 10. Dates, and calendars that do not exist

| concept | where | the trap |
|---|---|---|
| `DATE` as a real type | L1 Q10 | compares, sorts and subtracts as a date, not a string |
| date arithmetic | **L3 Q6**, L4 Q6 | `max(day) - min(day)` is a number of days |
| rolling up to a coarser grain | L2 Q9, L4 Q8, G Q11 | `extract(year …)`, `date_trunc('month', …)`, `strftime(…)` |
| a span is not activity | **L3 Q6** | 63 days between first and last outing can mean three trips |
| the calendar spine, recursively | **L4 Q9**, G Q16 | days with no bookings exist in the calendar and in no table |
| the calendar spine, from a range | **L4 Q11** | `range(…)` unnested — the one-liner; the recursive form is the general tool |
| choosing the window | **L4 Q11** | "idle days" measured against the season (60) or the calendar year (356) are different claims |
| year-over-year change | L4 Q12 | `LAG` ordered by year, while the ranking orders by volume |

## 11. Reshaping results

| concept | where | the trap |
|---|---|---|
| `PIVOT` | **L4 Q8** | categories become *columns*, so the result's shape depends on its contents |
| wide for people, long for machines | L4 Q8 | the chart melts the grid straight back |
| a column alias, and where it may be used | **G Q18** | you may qualify a real column, never a name you invented one line earlier |
| ordering by a grouping alias | L4 Q12 | inside a window over a grouped query, the alias is how you name the group key |

## 12. The schema as a teaching instrument

| concept | where | the trap |
|---|---|---|
| why `reserves` is keyed `(bid, day)` | G front matter, [`DESIGN.md`](DESIGN.md) §3, [README §6](README.md#6-the-one-decision-that-matters) | a **wider** key is a **weaker** constraint |
| the mirror constraint `UNIQUE (sid, day)` | G front matter, G Q12 | the primary key says nothing about how many boats one sailor holds |
| a day is a one-to-one matching | G Q12, L2 intro | one sailor per cell, no name twice in a column |
| a `CHECK` prevents a class of query bug | L1 Q3 | the wrong case cannot be stored, so it cannot be missed by a filter |
| a constraint can make a query pointless | G Q6 | `UNIQUE (sid, day)` makes "one sailor's two boats on a day" structurally empty |
| constraints shape the *data generator* too | [`DATASET_LARGE.md` §I](DATASET_LARGE.md#i-step-4--the-reservations) | rows are built a day at a time so both keys hold by construction |
| watching the rules reject rows | `./create_database.sh --verify` | eleven forbidden inserts, each printing the database's own refusal |

## 13. Lessons that come from the data's shape

Seed rows chosen so that a lesson exists. Change these and the prose stops
matching the output. The full list of which rows are load-bearing is in
`CLAUDE.md`, a local working file that the repository does not carry.

| the data | where it teaches | what it teaches |
|---|---|---|
| 10 sailors who never book, 5 boats never booked | L2 Q1, L2 Q10, L3 Q4, L4 Q1, G Q8, G Q9 | absence is what makes outer joins and anti-joins visible |
| two sailors named Horatio | **L2 Q7**, L3 Q5, G Q27 | names are not keys; `count(DISTINCT sname)` ≠ `count(*)` |
| Rusty and Zorba both rated 10 | **L2 Q5**, G Q25 | why `ORDER BY … LIMIT 1` is the wrong tool |
| ten sailors tied at zero | **L3 Q4**, L4 Q5 | ties break `LIMIT`, and reveal what each ranking function does |
| Dan, unrated | L1 Q8, L2 Q7, G Q3 | the whole NULL section rests on one row |
| Bob — the only B…B name | L2 Q4, G Q22 | and it only matches once you fold the case |
| every reservation in 1998 | L2 Q9, L4 Q3, L4 Q11, L4 Q12 | a degenerate answer is still an answer, and must be read as one |
| one reservation moved off 1998-10-10 | [README §7](README.md#7-the-database), [`DESIGN.md`](DESIGN.md) §5 | a new rule can invalidate existing data, and somebody must decide what happens to it |
| 235 sailors, 44 boats, 5,000 bookings, 3 years | [`DATASET_LARGE.md`](DATASET_LARGE.md) | the same queries at a scale where you cannot check by eye |

## 14. Reading a result honestly

The judgement half of the course — worth as much as the syntax.

| idea | where | in one line |
|---|---|---|
| an empty answer is an answer | **L4 Q1**, G Q19 | nobody has all nine boats, and the chart draws the gap so "empty" is visible |
| a degenerate answer is an answer | **L2 Q9**, L4 Q3, L4 Q12 | one year in the data makes "sailed every year" trivially true |
| a query can be structurally unanswerable | **G Q6** | if a constraint guarantees zero rows, the question is wrong, not the data |
| comparing unequal windows | **L4 Q12** | 2026 ranks last on 7½ months against two full years |
| a number that invites the wrong conclusion | **L3 Q6** | `span_days` looks like activity and is not |
| one row is not a chart | **L2 Q9** | a single bar is a number with decoration |
| the same rows, two orders | L3 Q7, L4 Q12 | the query answers "which is busiest", the chart restores time order |

---

## Teaching paths

Ready-made selections, if you want a subset rather than a level.

| goal | queries |
|---|---|
| **One-hour intro** | L1 Q1, Q4, Q5, Q6, Q7, Q8 |
| **Why NULL is hard** | L1 Q2, L1 Q8, L3 Q9, L2 Q7 |
| **Joins, properly** | L2 Q1, L2 Q2, L2 Q10, G Q8, L4 Q11 |
| **`GROUP BY` and `HAVING`** | L1 Q7, L2 Q3, L2 Q8, L3 Q8 |
| **Sets and absence** | L3 Q1, L3 Q2, L3 Q9, L3 Q10 |
| **"For all" / division** | L3 Q10 → L4 Q1 → L4 Q2 → L4 Q3, then G Q14 |
| **Window functions** | L4 Q4, L4 Q5, L4 Q6, L4 Q7, L4 Q10, L4 Q12 |
| **Dates and missing days** | L1 Q10, L3 Q6, L4 Q9, L4 Q11 |
| **Ties and duplicates** | L1 Q5 → L1 Q6, L2 Q5, L2 Q7, L3 Q4, L4 Q5 |
| **Judgement, not syntax** | [§14](#14-reading-a-result-honestly) — every row |
| **The schema decision** | [`DESIGN.md`](DESIGN.md) §3, G front matter, G Q12, then `./create_database.sh --verify` |
| **Scale** | any level notebook against `sailors_and_boats_large.duckdb` ([`DATASET_LARGE.md`](DATASET_LARGE.md)) |
