# Self Join — When a Table Joins Itself

```
   What is a Self Join?

   A self join joins a table to ITSELF. You list the
   same table twice, give each copy its own alias
   (for example e = employee, m = manager), and write
   an ON rule that connects the two roles. There is
   no SELF JOIN keyword: you use INNER JOIN or
   LEFT JOIN, exactly as before.
```

* Two beginner-friendly Marimo notebooks on the self join, in DuckDB.
* They assume you already know a basic `INNER JOIN` and `LEFT JOIN`
between **two** tables.
* All examples use tiny tables built in memory, so you can check
every result by eye.

## Files

| File | What it is | Time |
|------|------------|------|
| [`self_join_notebook_01.py`](self_join_notebook_01.py) | **Quick start.** 5 queries on a 10-row `employees` table: employee → manager, `LEFT JOIN` to keep the boss, earns more than the manager, coworker pairs, direct-report counts | ~20 min |
| [`self_join_notebook_02.py`](self_join_notebook_02.py) | **Full lesson.** 15 queries in 13 parts on a 12-row company, plus a second table (`daily_sales`). Adds an org chart drawn from a self join, a step-by-step matching tracer, `COALESCE`, three-way pair counts (why `<`), the `COUNT(*)` trap, grand-managers (three copies of one table), today vs. yesterday, a pick-a-manager widget, real error messages, a cheat sheet, and 6 exercises with solutions | ~60 min |

Start with `01` for a short first look, or go straight to `02`.
Both use the same idea and the same alias names (`e` = employee,
`m` = manager), so they work well together.

## What You Will Learn (Notebook 02)

| Part | Queries | Topic |
|------|---------|-------|
| 1 | Q1–Q2 | Meet the data — the table and its org chart |
| 2 | — | One table, two roles: why a self join needs two aliases |
| 3 | Q3 | Your first self join: employee next to manager |
| 4 | — | How the matching works — pick an employee and trace it |
| 5 | Q4–Q5 | Keep the boss with `LEFT JOIN`; replace `NULL` with `COALESCE` |
| 6 | Q6–Q7 | Compare a row to its partner: paid more / hired earlier than the manager |
| 7 | Q8–Q10 | Pairs from one table, and the `a.id < b.id` trick |
| 8 | Q11–Q12 | Count direct reports; the `COUNT(*)` trap; team payroll with `HAVING` |
| 9 | Q13 | Two steps up: the grand-manager (three copies of one table) |
| 10 | Q14–Q15 | Not only org charts: today vs. yesterday on `daily_sales` |
| 11 | — | Explore: pick a manager, see the team |
| 12 | — | Common mistakes — two real errors and two silent bugs |
| 13 | — | Cheat sheet (3 patterns) and 6 exercises with solutions |

## The Sample Data (Notebook 02)

```
employees   (employee_id, name, title, department, manager_id, salary, hire_date)   -- 12 rows
daily_sales (sale_date, revenue)                                                    -- 7 rows

employees.manager_id → employees.employee_id   (the table points to itself)
```

* Alice is the CEO, so her `manager_id` is `NULL`, on purpose.
* The company has four levels: CEO → VPs → managers → staff.

## Best-Fit Week

**Week 5 — SQL Joins.** Notebook 02 also reviews `GROUP BY` /
`HAVING` (Week 2) and `COALESCE` / `IS NULL` (Week 5). Its
today-vs-yesterday part is a good warm-up for `LAG()` in Week 9.

## How to Run

```bash
cd tutorials/SELF_JOIN
marimo edit self_join_notebook_02.py
```

Requirements: `duckdb`, `pandas`, and `marimo`
(see `software_installation/` if you have not installed them yet).

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
