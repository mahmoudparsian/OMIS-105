# Week 6 Quiz — Joins II

All questions use the Valley Fitness data: 10 `members`, 16 `bookings`.
Two members (Ava, Ben) have no bookings. One booking (1015) belongs to a
member who does not exist.

---

**1.** How many rows does `members INNER JOIN bookings` return?

- a) 10
- b) 15 ✅
- c) 16
- d) 17

**2.** How many rows does `members LEFT JOIN bookings` return?

- a) 15
- b) 16
- c) 17 ✅ — 15 matches + Ava + Ben
- d) 18

**3.** `A RIGHT JOIN B` returns the same rows as:

- a) `A LEFT JOIN B`
- b) `B LEFT JOIN A` ✅
- c) `A INNER JOIN B`
- d) `B INNER JOIN A`

**4.** To find members who **never** booked a class, you write
`members LEFT JOIN bookings ...` and then:

- a) `WHERE b.booking_id = NULL`
- b) `WHERE b.booking_id IS NULL` ✅
- c) `WHERE m.member_id IS NULL`
- d) `HAVING COUNT(*) = 0`

**5.** After `members LEFT JOIN bookings ... GROUP BY m.member_name`,
what does `COUNT(*)` show for Ava (who has no bookings)?

- a) 0
- b) 1 ✅ — her one row with `NULL`s is still a row
- c) `NULL`
- d) An error

**6.** Which expression correctly gives **0** for Ava in question 5?

- a) `COUNT(*)`
- b) `COUNT(m.member_id)`
- c) `COUNT(b.booking_id)` ✅
- d) `SUM(*)`

**7.** `COALESCE(t.trainer_name, '(not assigned)')` returns:

- a) Always `'(not assigned)'`
- b) `t.trainer_name`, or `'(not assigned)'` when it is `NULL` ✅
- c) `NULL` when `t.trainer_name` is `NULL`
- d) The number of non-`NULL` trainer names

**8.** You write `members LEFT JOIN bookings ... WHERE b.booking_date >=
'2026-09-10'`. What happens to members with **no** bookings?

- a) They are kept with `NULL`s
- b) They are removed — the `WHERE` turns the `LEFT JOIN` into an
  `INNER JOIN` ✅
- c) DuckDB gives an error
- d) Their `booking_date` becomes `'2026-09-10'`

**9.** In a chain `members JOIN bookings JOIN classes JOIN trainers`,
one class has no trainer. To **keep** its bookings, the last join should be:

- a) `INNER JOIN trainers`
- b) `LEFT JOIN trainers` ✅
- c) `CROSS JOIN trainers`
- d) It does not matter

**10.** A **self-join** is:

- a) A join with no `ON` clause
- b) A table joined to itself, using two different aliases ✅
- c) A join that only works on one column
- d) Another name for `FULL OUTER JOIN`

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
