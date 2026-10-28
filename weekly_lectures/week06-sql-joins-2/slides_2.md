---
title: OMIS 105 - Week 6 (Joins II — Joins at Work)
author: Dr. Mahmoud Parsian
marp: true
theme: default
paginate: true
class: lead
style: |
  section {
    justify-content: flex-start;
  }
  table {
    font-size: 0.7em;
  }

---

# OMIS 105: Week 6
## Joins II — Session 2 <br> Joins at Work

---

# Agenda

- Counting with `LEFT JOIN` + `GROUP BY` — including **zero**
- Joining 3 and 4 tables
- One `INNER JOIN` in a chain can drop rows
- Self-joins: a table joined to itself
- A quick look at `FULL OUTER JOIN`
- Which join do I need? A cheat sheet

---

# Recap from Session 1

- `INNER JOIN` → matches only
- `LEFT JOIN` → every left row; no partner = `NULL`
- `A RIGHT JOIN B` = `B LEFT JOIN A`
- Anti-join: `LEFT JOIN ... WHERE right_key IS NULL`
- Filter the optional (right) table in `ON`, not in `WHERE`

Same data today: **Valley Fitness** — `members`, `bookings`,
`classes`, `trainers`.

---

# Question: How Many Bookings per Member?

The manager wants **every** member — even those with zero bookings.

So we need a `LEFT JOIN` and a `GROUP BY`.

But **what** do we count? Let's try `COUNT(*)` first…

---

# Attempt 1: `COUNT(*)` ❌

```sql
SELECT m.member_name, COUNT(*) AS bookings
FROM members AS m
LEFT JOIN bookings AS b
    ON m.member_id = b.member_id
GROUP BY m.member_name
ORDER BY bookings, m.member_name;
```

| member_name | bookings |
|---|---|
| Ava Martinez | 1 |
| Ben Taylor | 1 |
| Lucas Rossi | 1 |
| Ryan Lee | 1 |
| … | … |

😱 Ava and Ben have **1** booking? They never booked anything!

---

# Why Is `COUNT(*)` Wrong Here?

After the `LEFT JOIN`, Ava still has **one row**:

| member_name | booking_id |
|---|---|
| Ava Martinez | NULL |

- `COUNT(*)` counts **rows** → 1 ❌
- `COUNT(b.booking_id)` counts **non-`NULL` values** → 0 ✅

👉 After a `LEFT JOIN`, count a column from the **right** table —
usually its key.

---

# Attempt 2: `COUNT(b.booking_id)` ✅

```sql
SELECT m.member_name, COUNT(b.booking_id) AS bookings
FROM members AS m
LEFT JOIN bookings AS b
    ON m.member_id = b.member_id
GROUP BY m.member_name
ORDER BY bookings, m.member_name;
```

| member_name | bookings |
|---|---|
| Ava Martinez | 0 |
| Ben Taylor | 0 |
| Lucas Rossi | 1 |
| Ryan Lee | 1 |
| … | … |

---

# Revenue per Class — Including Zero

```sql
SELECT c.class_name,
       c.price,
       COUNT(b.booking_id)           AS bookings,
       COUNT(b.booking_id) * c.price AS revenue
FROM classes AS c
LEFT JOIN bookings AS b
    ON c.class_id = b.class_id
GROUP BY c.class_name, c.price
ORDER BY revenue DESC, c.class_name;
```

---

# Revenue per Class — Result

| class_name | price | bookings | revenue |
|---|---|---|---|
| HIIT Bootcamp | 25 | 3 | 75 |
| Morning Yoga | 15 | 4 | 60 |
| Spin Cycle | 20 | 3 | 60 |
| Strength Basics | 22 | 2 | 44 |
| Pilates Core | 18 | 2 | 36 |
| Boxing Fit | 25 | 1 | 25 |
| Senior Stretch | 12 | 1 | 12 |
| Aqua Fitness | 16 | 0 | 0 |

💡 Aqua Fitness: 0 bookings, $0. An `INNER JOIN` would have hidden it.

---

# Joining 3 Tables

A JOIN can follow **more than one link**. Add one `JOIN` per table:

```
members ──< bookings >── classes
```

```sql
SELECT m.member_name, c.class_name, b.booking_date
FROM members AS m
INNER JOIN bookings AS b
    ON m.member_id = b.member_id
INNER JOIN classes AS c
    ON b.class_id = c.class_id
ORDER BY b.booking_date, m.member_name;
```

---

# Joining 3 Tables — Result (15 rows)

| member_name | class_name | booking_date |
|---|---|---|
| Olivia Brown | Morning Yoga | 2026-09-01 |
| Liam Garcia | HIIT Bootcamp | 2026-09-02 |
| Sophia Nguyen | Morning Yoga | 2026-09-02 |
| Olivia Brown | Spin Cycle | 2026-09-03 |
| Ethan Patel | Spin Cycle | 2026-09-04 |
| Sophia Nguyen | Pilates Core | 2026-09-05 |
| Mia Johnson | Strength Basics | 2026-09-06 |
| Lucas Rossi | Boxing Fit | 2026-09-07 |
| … | … | … |

👉 Each `JOIN ... ON` adds one table. Read it top to bottom:
members → their bookings → the class of each booking.

---

# Joining 4 Tables — All `INNER`

Now add the trainer of each class:

```sql
SELECT m.member_name, c.class_name, t.trainer_name
FROM members AS m
INNER JOIN bookings AS b ON m.member_id = b.member_id
INNER JOIN classes  AS c ON b.class_id  = c.class_id
INNER JOIN trainers AS t ON c.trainer_id = t.trainer_id
ORDER BY m.member_name, c.class_name;
```

**14 rows.** But we had 15 bookings with a known member…
**which row went missing?**

---

# The Missing Row

Chloe booked **Senior Stretch** (booking 1011).
Senior Stretch has **no trainer** (`trainer_id` is `NULL`).

The last `INNER JOIN trainers` found no partner → the row was
**dropped**.

👉 One `INNER JOIN` anywhere in a chain can quietly drop rows.

---

# The Fix: `LEFT JOIN` the Optional Table

```sql
SELECT m.member_name, c.class_name,
       COALESCE(t.trainer_name, '(not assigned)') AS trainer
FROM members AS m
INNER JOIN bookings AS b ON m.member_id = b.member_id
INNER JOIN classes  AS c ON b.class_id  = c.class_id
LEFT  JOIN trainers AS t ON c.trainer_id = t.trainer_id
ORDER BY m.member_name, c.class_name;
```

| member_name | class_name | trainer |
|---|---|---|
| *13 other rows* | … | … |
| Chloe Davis | Morning Yoga | Aisha Khan |
| Chloe Davis | Senior Stretch | (not assigned) |

**15 rows** — Chloe's Senior Stretch booking is back.

---

# Rule for Chains of JOINs

- Use `INNER JOIN` when a partner **must** exist
- Use `LEFT JOIN` when a partner is **optional**
- Once a row can have `NULL`s, keep using `LEFT JOIN` for the tables
  that come after it

---

# Trainer Workload — 3 Tables + `GROUP BY`

```sql
SELECT t.trainer_name,
       COUNT(DISTINCT c.class_id) AS classes,
       COUNT(b.booking_id)        AS bookings
FROM trainers AS t
LEFT JOIN classes  AS c ON t.trainer_id = c.trainer_id
LEFT JOIN bookings AS b ON c.class_id   = b.class_id
GROUP BY t.trainer_name
ORDER BY bookings DESC, t.trainer_name;
```

---

# Trainer Workload — Result

| trainer_name | classes | bookings |
|---|---|---|
| James Chen | 2 | 5 |
| Aisha Khan | 1 | 4 |
| Diego Santos | 2 | 4 |
| Emma Wilson | 2 | 2 |
| Maria Lopez | 0 | 0 |
| Noah Kim | 0 | 0 |

- `COUNT(DISTINCT c.class_id)`: after joining bookings, a class
  appears once **per booking** — `DISTINCT` counts it once
- Maria and Noah teach no class → 0 and 0, thanks to `LEFT JOIN`

---

# Self-Join: A Table Joined to Itself

`trainers` has a `manager_id` column. It points to **another trainer**.

| trainer_id | trainer_name | manager_id |
|---|---|---|
| 1 | Maria Lopez | NULL |
| 2 | James Chen | 1 |
| 3 | Aisha Khan | 1 |
| 4 | Diego Santos | 2 |
| 5 | Emma Wilson | 2 |
| 6 | Noah Kim | 3 |

To show a trainer **and** their manager's name, use the table
**twice**, with two different aliases: `e` (employee) and `m` (manager).

---

# Self-Join with `INNER JOIN`

```sql
SELECT e.trainer_name AS trainer,
       m.trainer_name AS manager
FROM trainers AS e
INNER JOIN trainers AS m
    ON e.manager_id = m.trainer_id
ORDER BY e.trainer_id;
```

| trainer | manager |
|---|---|
| James Chen | Maria Lopez |
| Aisha Khan | Maria Lopez |
| Diego Santos | James Chen |
| Emma Wilson | James Chen |
| Noah Kim | Aisha Khan |

Only **5 rows**. Maria has no manager, so she was dropped.

---

# Self-Join with `LEFT JOIN` ✅

```sql
SELECT e.trainer_name AS trainer,
       COALESCE(m.trainer_name, '(head trainer)') AS manager
FROM trainers AS e
LEFT JOIN trainers AS m
    ON e.manager_id = m.trainer_id
ORDER BY e.trainer_id;
```

| trainer | manager |
|---|---|
| Maria Lopez | (head trainer) |
| James Chen | Maria Lopez |
| Aisha Khan | Maria Lopez |
| Diego Santos | James Chen |
| Emma Wilson | James Chen |
| Noah Kim | Aisha Khan |

---

# The Self-Join Draws the Org Chart

Each row of the self-join is one line in this chart:

```
Maria Lopez (head trainer)
├── James Chen
│   ├── Diego Santos
│   └── Emma Wilson
└── Aisha Khan
    └── Noah Kim
```

👉 The demo notebook draws this chart **from the query result**.

---

# How Many Direct Reports?

Self-join + `GROUP BY`. Start from the **manager** side:

```sql
SELECT m.trainer_name AS manager,
       COUNT(e.trainer_id) AS direct_reports
FROM trainers AS m
LEFT JOIN trainers AS e
    ON e.manager_id = m.trainer_id
GROUP BY m.trainer_name
ORDER BY direct_reports DESC, manager;
```

---

# Direct Reports — Result

| manager | direct_reports |
|---|---|
| James Chen | 2 |
| Maria Lopez | 2 |
| Aisha Khan | 1 |
| Diego Santos | 0 |
| Emma Wilson | 0 |
| Noah Kim | 0 |

👉 Same counting rule as before: `COUNT(e.trainer_id)`, not
`COUNT(*)`, so trainers with no reports show **0**.

---

# A Quick Look: `FULL OUTER JOIN`

`FULL OUTER JOIN` keeps **every row from both sides**.

- `members FULL OUTER JOIN bookings` → 18 rows
  (15 matches + Ava + Ben + booking 1015)

Show **only** the gaps, from both sides at once:

```sql
SELECT m.member_name, b.booking_id
FROM members AS m
FULL OUTER JOIN bookings AS b
    ON m.member_id = b.member_id
WHERE m.member_id IS NULL
   OR b.booking_id IS NULL
ORDER BY b.booking_id, m.member_name;
```

| member_name | booking_id |
|---|---|
| NULL | 1015 |
| Ava Martinez | NULL |
| Ben Taylor | NULL |

---

# Business Report: Activity by City

```sql
SELECT m.city,
       COUNT(DISTINCT m.member_id) AS members,
       COUNT(b.booking_id)         AS bookings
FROM members AS m
LEFT JOIN bookings AS b
    ON m.member_id = b.member_id
GROUP BY m.city
ORDER BY bookings DESC, m.city;
```

| city | members | bookings |
|---|---|---|
| San Jose | 3 | 6 |
| Santa Clara | 3 | 5 |
| Cupertino | 2 | 2 |
| Sunnyvale | 2 | 2 |

`COUNT(DISTINCT m.member_id)`: a member with 3 bookings appears in
3 rows, but is **one** member.

---

# Which Join Do I Need? 🗺️

| Business question | Join |
|---|---|
| "Show orders **with** their customer names" | `INNER JOIN` |
| "Show **all** customers, with orders if any" | `LEFT JOIN` |
| "Which customers **never** ordered?" | `LEFT JOIN ... WHERE right_key IS NULL` |
| "Count orders per customer, **including 0**" | `LEFT JOIN` + `COUNT(right_key)` |
| "Show each employee **and their manager**" | self-join (`LEFT JOIN` the same table) |
| "Show **every** gap on **both** sides" | `FULL OUTER JOIN` |

---

# Summary

- After a `LEFT JOIN`, count the right table's key, not `*`
- Add one `JOIN ... ON` per table; read the chain top to bottom
- One `INNER JOIN` in a chain can drop rows — use `LEFT JOIN` for
  optional partners
- A self-join uses the **same table twice** with two aliases
- `FULL OUTER JOIN` keeps both sides' gaps

---

# What's Next?

**Week 7: Subqueries — a query inside a query**

- "Which members booked **more than the average**?"
- `IN`, `NOT IN`, `EXISTS`
- Many "find what is missing" questions can be answered
  **with a join or with a subquery** — you will learn both

---

# Questions?

Thank you!

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
