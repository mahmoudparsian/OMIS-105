# Design Notes — Week 06, Lab 1

## Dataset check (the lesson from week 4 Lab 3 and week 5 Lab 4)

Every "find the missing" question was run against the data before
writing it. None returns 0 rows by accident:

| Question | Result |
|---|---|
| Q4 — Sunnyvale/Cupertino members with no bookings | 1 row (Ben Taylor) |
| Q5 — classes with no trainer | 1 row (Senior Stretch) |
| Q10 — booking with an unknown member | 1 row (1015 → Pilates Core) |
| Q11 — members who never booked (after the fix) | 2 rows (Ava, Ben) |
| Q12 — classes no Santa Clara member booked | 4 rows |

The data is the same as the public `week06-sql-joins-2/data/` CSVs,
written inline as `VALUES` so the notebook needs no files.

## The four moves

| Move | Where | Why |
|---|---|---|
| Predict | Q1 | 16 bookings + 1 unbooked class = 17. Rehearses "which rows does a LEFT JOIN add?" |
| Explain it | Q3 | `A RIGHT JOIN B` = `B LEFT JOIN A` in the student's own words |
| Debug it | Q11 | `INNER JOIN` + `WHERE ... IS NULL`: silently 0 rows. A different silent bug from week 5's `= NULL` |
| Bonus | Q12 | Two LEFT JOINs + a filter in `ON` + `HAVING COUNT(...) = 0` |

Q7 (filter on the right table goes in `ON`) and Q8 (filter on the left
table stays in `WHERE`) are a deliberate pair: same idea, opposite answers.

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
