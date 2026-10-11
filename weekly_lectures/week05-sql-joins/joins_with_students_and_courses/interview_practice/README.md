# SQL Interview Practice — Students / Courses / Grades

**Optional.** Do the joins notebook in the parent folder first.

## File Structure

```
interview_practice/
├── README.md                       # this file
├── interview_practice.py           # 12 timed SQL interview questions, with automatic checks
└── interview_practice_answers.py   # solutions, what each question tests, common wrong answers
```

## About

Data analyst interviews almost always include a live SQL test.
`interview_practice.py` has 12 interview-style questions on this
database, written the way a manager would ask them. Set a timer for
60 minutes.

```bash
cd joins_with_students_and_courses
./create_duckdb_database.sh                 # if you have not built it yet
cd interview_practice
marimo edit interview_practice.py           # the questions
marimo edit interview_practice_answers.py   # the answers — open after you try
```

Both notebooks use the clean database in the parent folder. Nothing
here changes the data.

Under each question, a box checks your **row count and column
names**: green means the shape of your result is right. The
questions get harder:

| Level | Questions | Skills |
|-------|-----------|--------|
| Warm-up | Q1–Q4 | `GROUP BY`, `HAVING`, anti-join, join + `LIMIT`, ties |
| Core | Q5–Q9 | filter in `ON` vs. `WHERE`, conditional counts, `COUNT(DISTINCT)`, 3-table joins |
| Hard | Q10–Q12 | weighted averages, a correct answer with 0 rows, an unclear question |

The answers notebook explains what each question is really testing,
and runs the most common wrong answer next to the right one, so you
can see how the results differ.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
