# Lab 6: Joins II — `INNER`, `LEFT`, and `RIGHT JOIN` in Practice

## OMIS 105 — Database Management Systems
**Week 6 | Estimated time: 75–90 minutes | 10 questions × 3 points = 30 points**

---

## Setup

Open a new Marimo notebook **inside the `week06-sql-joins-2` folder**
(so the `data/` path works), and run this cell first:

```python
import duckdb
con = duckdb.connect(database=":memory:")
for t in ["members", "bookings", "classes", "trainers"]:
    con.execute(f"CREATE OR REPLACE TABLE {t} AS SELECT * FROM read_csv('data/{t}.csv')")
```

Then write each answer in its own cell:

```python
con.execute("""
    SELECT ...
""").fetchdf()
```

**The tables** (the same Valley Fitness data as the demos):

| Table | Columns |
|---|---|
| `members` | `member_id`, `member_name`, `city`, `join_date` |
| `bookings` | `booking_id`, `member_id`, `class_id`, `booking_date` |
| `classes` | `class_id`, `class_name`, `trainer_id`, `price` |
| `trainers` | `trainer_id`, `trainer_name`, `manager_id` |

**Rules for every query:**

- Give every table an alias (`m`, `b`, `c`, `t`) and use it on
  every column: `c.class_name`, not `class_name`
- List the columns you need — no `SELECT *`
- Use the `ORDER BY` given in the question, so your rows match the
  expected row count and order
- The **expected row count** is given for each question. If your
  count is different, look again at your join type.

---

## Part 1: The Three Join Types (12 points)

**Q1. Classes with their trainer.** Show `class_name` and `trainer_name` for classes that **have** a trainer. Use `INNER JOIN`. Order by `class_name`.

*Expected: 7 rows.*

```sql
-- your query here

```

---

**Q2. Every class.** Same as Q1, but keep **every class**, even one with no trainer. Order by `class_name`. Which class shows `NULL`, and why?

*Expected: 8 rows.*

```sql
-- your query here

```

---

**Q3. Every trainer, with `RIGHT JOIN`.** Write `FROM classes AS c RIGHT JOIN trainers AS t`. Show `trainer_name` and `class_name`, and keep **every trainer**. Order by `trainer_name`, then `class_name`.

*Expected: 9 rows.*

```sql
-- your query here

```

---

**Q4. Same answer, with `LEFT JOIN`.** Rewrite Q3 so it uses `LEFT JOIN` instead of `RIGHT JOIN`. Your result must be exactly the same as Q3. In one sentence: what did you change?

*Expected: 9 rows.*

```sql
-- your query here

```

---

## Part 2: Finding What Is Missing (6 points)

**Q5. Trainers who teach no class.** Show `trainer_id` and `trainer_name`. Use `LEFT JOIN` and `IS NULL`. Order by `trainer_id`.

*Expected: 2 rows.*

```sql
-- your query here

```

---

**Q6. Members who never booked.** Show `member_name` and `city` for members with **no** bookings. Order by `member_name`. Marketing will send them a free-class coupon.

*Expected: 2 rows.*

```sql
-- your query here

```

---

## Part 3: Joins at Work (12 points)

**Q7. Classes per trainer, including zero.** For **every** trainer, show `trainer_name` and the number of classes they teach as `classes`. Trainers with no class must show **0**. Order by `classes` (highest first), then `trainer_name`. *Hint:* `COUNT(*)` gives the wrong answer here. Why?

*Expected: 6 rows.*

```sql
-- your query here

```

---

**Q8. Who booked Morning Yoga?** Join **three** tables (`members`, `bookings`, `classes`). Show `member_name` and `booking_date` for every booking of `'Morning Yoga'`. Order by `booking_date`.

*Expected: 4 rows.*

```sql
-- your query here

```

---

**Q9. Trainer and manager (self-join).** Show every trainer as `trainer` and their manager's name as `manager`. The trainer with no manager must show `'(no manager)'`. Use the `trainers` table twice. Order by `trainer`.

*Expected: 6 rows.*

```sql
-- your query here

```

---

**Q10. The `ON` vs. `WHERE` trap.** For **every** class, count its bookings made **on or after** `2026-09-10`, as `late_bookings`. Classes with no late booking must show **0**. Order by `late_bookings` (highest first), then `class_name`. *Hint:* where does the date filter go?

*Expected: 8 rows.*

```sql
-- your query here

```

---


---

## Grading

- 3 points per question: 2 for a correct result, 1 for a clean query
  (aliases on every column, the right join type, the given `ORDER BY`)
- For Q2, Q4, Q7, and Q10, the short written answer is part of the
  "clean query" point


---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
