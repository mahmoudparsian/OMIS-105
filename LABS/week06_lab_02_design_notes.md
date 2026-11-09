# Design Notes — Week 06, Lab 2

## Two numbers students will argue about

**Q4, Emma Wilson = 1 or 2?** Her Pilates Core has two bookings: member 3
and member 12 (who does not exist). `COUNT(DISTINCT m.member_id)` → 1,
`COUNT(DISTINCT b.member_id)` → 2. The key accepts 1 (real members);
accept 2 with a sensible sentence. Good discussion: "what does the
manager actually want to know?"

**Q9, Emma Wilson = 36 or 52?** `COALESCE(SUM(c.price), 0)` gives 52:
the `LEFT JOIN` keeps Aqua Fitness (never booked) as one row with its
price, so 16 is added for a class nobody booked. Correct: add the price
only when a booking exists (`CASE WHEN b.booking_id IS NOT NULL ...`) → 36.
This is the explain-it for Q9; it uses `CASE` from Week 3.

## Dataset check

| Question | Result |
|---|---|
| Q1 — Aqua Fitness bookings | 0 (not 1) |
| Q6 — co-worker pairs | 2 pairs |
| Q8 — FULL OUTER JOIN gaps | 3 rows (one class side, two trainer side) |
| Q12 — members with 2+ trainers | 5 rows (Chloe excluded: Senior Stretch has no trainer) |

## The four moves

| Move | Where |
|---|---|
| Predict | Q1 (8 rows; Aqua shows 0) |
| Explain it | Q3 (`SUM` → `NULL` vs. `COUNT` → 0) and Q9 (leaked price) |
| Debug it | Q11 — `COUNT(*)` after `LEFT JOIN` gives Ava and Ben 1 |
| Bonus | Q12 — `HAVING COUNT(DISTINCT c.trainer_id) >= 2` |

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
