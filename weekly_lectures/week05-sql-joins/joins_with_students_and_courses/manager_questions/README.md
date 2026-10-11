# Questions from Managers — Students / Courses / Grades

**Optional.** Do the joins notebook in the parent folder first.

At work, nobody hands you a precise SQL exercise. A manager sends a
short, often vague message and expects an **answer**, not a table.
This folder has 8 such requests — from the Dean, the Registrar, the
CFO, and others — on the same students / courses / grades database.

For each request you:

1. **Define it** — decide exactly what you will measure.
2. **Query it** — write the SQL.
3. **Answer it** — write 2–3 sentences you could send back.

There is often more than one correct definition. What matters is
that you choose one, say it clearly, and that your numbers match it.

## File Structure

```
manager_questions/
├── README.md                        # this file
├── manager_questions.py             # the 8 requests, with a template in each SQL cell
└── manager_questions_answers.py     # model definitions, queries, 5 charts, answers to send
```

Both notebooks use the clean database and `plot_helpers.py` from the
parent folder. Nothing here changes the data.

## Usage

```bash
cd joins_with_students_and_courses
./create_duckdb_database.sh                  # if you have not built it yet
cd manager_questions
marimo edit manager_questions.py             # the requests
marimo edit manager_questions_answers.py     # the answers — open after you try
```

## The 8 Requests

| # | From | Request | What it practices |
|---|------|---------|-------------------|
| M1 | Dean | Has grading gotten easier? | "no change" is a real answer; honest chart axes |
| M2 | Registrar | Which courses could we cancel? | `LEFT JOIN` keeps courses with 0 students; 2025 vs. all years |
| M3 | Math Chair | Is Math the hardest? Why? | going one level deeper (department → course) |
| M4 | Admissions | Where do our strongest students come from? | small differences and small groups are not signals |
| M5 | CFO | Tuition per department, and vs. last year | stating assumptions; answering two questions in order |
| M6 | Dean of Students | List the struggling students | the definition sets the list size (1 to 95 students) |
| M7 | Provost | Who teaches other departments' students? | mapping majors to departments with `CASE` |
| M8 | President | 5–6 numbers for the board | leading with the number that changed most |

The answers use only Week 1–5 SQL, except one query in M6 that uses a
subquery (Week 9) to compare definitions; the notebook says so.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
