# Week 4 — SQL Aggregation

Lecture materials for Week 4 of **OMIS 105**. This week is about
summarizing data: aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`,
`MAX`), `GROUP BY`, `HAVING`, and a first look at joins.

## Start Here: Learning `GROUP BY`

**[`group_by_with_emps_depts/`](group_by_with_emps_depts/)** — the
main `GROUP BY` tutorial. It uses a small company: 5 departments and
13 employees, small enough to check every answer by eye. Keep it as
your reference for grouping. It includes:

- [`notebook.py`](group_by_with_emps_depts/notebook.py) — a Marimo
  notebook with 18 SQL queries and 11 charts. It opens
  `emps_depts_db.duckdb` read-only and goes from statistics for the
  whole table to 8 `GROUP BY` queries (basic → advanced: `WHERE`,
  `HAVING`, two columns, a pivot table), then 4 joins, and ends with
  "which departments have no employees?". `GROUP_CONCAT` shows the
  rows inside each group, so you can see how each aggregate works.

Start with that folder's [README](group_by_with_emps_depts/README.md).

## Files in This Folder

| File | What It Is |
|------|-----------|
| `slides_1.md` | Marp slide deck, session 1 — aggregation, `GROUP BY`, `HAVING` |
| `slides_2.md` | Marp slide deck, session 2 — joins and multi-table queries |
| `demo1.py` | Live-demo Marimo notebook, session 1 — aggregation and `GROUP BY` |
| `demo2.py` | Live-demo Marimo notebook, session 2 — joins and multi-table queries |
| `lab04_student.md` | The week's lab (joins and multi-table queries), with blanks to fill in |
| `lab04_student_marimo.py` | The lab as a Marimo notebook |
| `lab04_instructor_marimo.py` | The lab notebook, with answers |
| `quiz.md` | Short quiz questions for the week |
| `data/` | CSV files the demos and lab read |
| `lab.md`, `notes.md`, `solution.sql` | Brief scratch notes and sample SQL |

Run the demo notebooks from inside this folder, so the `data/` paths
work:

```bash
cd weekly_lectures/week04-sql-aggregation
marimo edit demo1.py
```

## Next Week

Week 5 goes deeper into joins. Its first demo,
[`joins_with_emps_depts/`](../week05-sql-joins/joins_with_emps_depts/),
uses the same kind of employees/departments data.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
