# Week 6 — Joins II: `INNER`, `LEFT`, and `RIGHT JOIN` in Practice

📦 **[Download Week 6 as a ZIP](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week06-sql-joins-2.zip)** — this week's lectures and review, in one file. No git needed.

Week 5 introduced joins. This week is all practice. Joins are the most
important skill in SQL, so we give them a second week.

## The Data: Valley Fitness 🏋️

A small gym with four tables. The data has **gaps on purpose**, so
`INNER`, `LEFT`, and `RIGHT JOIN` each give a different answer.

| Table | Rows | The gaps |
|---|---|---|
| `members` | 10 | Ava Martinez and Ben Taylor never booked a class |
| `bookings` | 16 | Booking 1015 belongs to member 12, who does not exist |
| `classes` | 8 | Aqua Fitness was never booked; Senior Stretch has no trainer |
| `trainers` | 6 | Maria Lopez and Noah Kim teach no class; `manager_id` points to another trainer |

`members INNER JOIN bookings` gives 15 rows, `LEFT JOIN` gives 17,
`RIGHT JOIN` gives 16, and `FULL OUTER JOIN` gives 18.

## Session 1 — LEFT, RIGHT, and Finding What Is Missing

- [`slides_1.md`](slides_1.md) — slide deck
- [`demo1.py`](demo1.py) — Marimo notebook: the three join types side
  by side, an interactive **join switcher**, the anti-join pattern
  (`LEFT JOIN ... WHERE ... IS NULL`), `COALESCE`, the `ON` vs.
  `WHERE` trap, and a real "ambiguous column" error

## Session 2 — Joins at Work

- [`slides_2.md`](slides_2.md) — slide deck
- [`demo2.py`](demo2.py) — Marimo notebook: counting with `LEFT JOIN`
  (`COUNT(*)` vs. `COUNT(column)`), joining 3 and 4 tables, why one
  `INNER JOIN` in a chain can drop rows, self-joins with an org chart
  **drawn from the query result**, and `FULL OUTER JOIN`

## Lab and Quiz

- [`lab06_student.md`](lab06_student.md) — **the week's lab**: 10
  questions, 30 points, with the expected row count for each one
- [`lab06_student_marimo.py`](lab06_student_marimo.py) — the same lab as a Marimo
  notebook: the data is loaded for you; replace each placeholder query
- [`lab06_instructor_marimo.py`](lab06_instructor_marimo.py) — the notebook with answers,
  real results, and a short explanation for each question
- [`quiz.md`](quiz.md) — 10 multiple-choice questions

## Files in This Folder

| File | What It Is |
|------|-----------|
| `slides_1.md`, `slides_2.md` | Marp slide decks — one per session |
| `demo1.py`, `demo2.py` | Live-demo Marimo notebooks — one per session |
| `lab06_student.md` | The lab, with blanks to fill in |
| `lab06_student_marimo.py`, `lab06_instructor_marimo.py` | The lab as Marimo notebooks — without and with answers |
| `quiz.md` | Short quiz |
| `data/` | `members.csv`, `bookings.csv`, `classes.csv`, `trainers.csv` |
| `images/` | Join diagrams (copied from Week 5's `joins_are_visualized/`) |

Run the notebooks from inside this folder:

```bash
cd weekly_lectures/week06-sql-joins-2
marimo edit demo1.py
```

## More Practice from Week 5

Want more? These Week 5 folders use other datasets for the same skills:

- [`joins_with_emps_depts/`](../week05-sql-joins/joins_with_emps_depts/) — every join type on 4 departments and 6 employees
- [`join_in_action_with_emps_depts/`](../week05-sql-joins/join_in_action_with_emps_depts/) — 20 questions, including the `ON` vs. `WHERE` trap
- [`joins_with_users_roles_cities/`](../week05-sql-joins/joins_with_users_roles_cities/) — 40 practice queries on three tables
- [`joins_with_authors_books_orders/`](../week05-sql-joins/joins_with_authors_books_orders/) and [`joins_with_students_and_courses/`](../week05-sql-joins/joins_with_students_and_courses/) — larger databases
- [`../../tutorials/SELF_JOIN/`](../../tutorials/SELF_JOIN/) — a full self-join lesson

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
