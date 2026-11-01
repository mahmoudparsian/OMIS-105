# Self Join — When a Table Joins Itself

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/mahmoudparsian/OMIS-105/blob/main/tutorials/SELF_JOIN/self_join_notebook_02_company.py/wasm) &nbsp; ← click to open the full lesson (Notebook 02) in your web browser. Nothing to install.

You need to learn the SQL self-join because it allows you to query relationships that exist within a single table.

```
   What is a Self Join?

   A self join joins a table to  ITSELF.  You 
   list the SAME table twice,  give each copy 
   its  own alias (for  example e = employee, 
   m = manager),  and  write an ON rule  that 
   connects the two roles. 
   
   There  is no SELF JOIN  keyword:  you  use 
   INNER JOIN or LEFT JOIN, exactly as before.
```

```sql
   -- SELF-JOIN EXAMPLE: 
   -- find manager's name for employees

   employees(emp_id, emp_name, mgr_id)

   SELECT e.emp_name AS employee_name, 
          m.emp_name AS manager_name
   FROM employees AS e 
   JOIN employees AS m 
      ON e.mgr_id = m.emp_id;
```

* A short reading guide and three beginner-friendly Marimo notebooks
on the self join, in DuckDB.
* They assume you already know a basic `INNER JOIN` and `LEFT JOIN`
between **two** tables.
* All examples use tiny tables built in memory, so you can check
every result by eye.

## Files

| File | What it is | Time |
|------|------------|------|
| [`self_joins_guide.md`](self_joins_guide.md) | **Read first.** A short guide you can read on GitHub: 5 self joins on a 5-row `employees` table (employee → manager, `LEFT JOIN` + `COALESCE`, coworker pairs, grand-managers, earns more than the manager), a cheat sheet, and a complete second example: 6 self joins on an 8-row `customers` referral table | ~25 min |
| [`self_join_notebook_01_quickstart.py`](self_join_notebook_01_quickstart.py)<br>[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/mahmoudparsian/OMIS-105/blob/main/tutorials/SELF_JOIN/self_join_notebook_01_quickstart.py/wasm) | **Quick start.** 5 queries on a 10-row `employees` table: employee → manager, `LEFT JOIN` to keep the boss, earns more than the manager, coworker pairs, direct-report counts | ~20 min |
| [`self_join_notebook_02_company.py`](self_join_notebook_02_company.py)<br>[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/mahmoudparsian/OMIS-105/blob/main/tutorials/SELF_JOIN/self_join_notebook_02_company.py/wasm) | **Full lesson.** 15 queries in 13 parts on a 12-row company, plus a second table (`daily_sales`). Adds an org chart drawn from a self join, a step-by-step matching tracer, `COALESCE`, three-way pair counts (why `<`), the `COUNT(*)` trap, grand-managers (three copies of one table), today vs. yesterday, a pick-a-manager widget, real error messages, a cheat sheet, and 6 exercises with solutions | ~60 min |
| [`self_join_notebook_03_referrals.py`](self_join_notebook_03_referrals.py)<br>[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/mahmoudparsian/OMIS-105/blob/main/tutorials/SELF_JOIN/self_join_notebook_03_referrals.py/wasm) | **New table, same patterns.** The guide's customer-referral example as a live notebook: 9 queries on an 8-row `customers` table (`referred_by` → `cust_id`). A referral tree drawn from a self join, `LEFT JOIN` + `COALESCE`, referral counts and the `COUNT(*)` trap, friends who spent more than their referrer, same-city pairs (why `<`), the referral chain (three copies of one table), a pick-a-referrer widget, and 4 exercises with solutions | ~40 min |

Read the guide first, then start with `01` for a short first look,
or go straight to `02`. Notebooks 01 and 02 use the same idea and the
same alias names (`e` = employee, `m` = manager), so they work well
together. Then try `03`: the same patterns on a different table
(`c` = customer, `r` = referrer).

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
-- 12 rows
employees   (emp_id, name, title, department, manager_id, salary, hire_date)   

-- 7 rows
daily_sales (sale_date, revenue)                                                    

employees.manager_id → employees.emp_id   (the table points to itself)
```

* Alice is the CEO, so her `manager_id` is `NULL`, on purpose.
* The company has four levels: CEO → VPs → managers → staff.

## Best-Fit Week

**Week 6 — SQL Joins II** (self joins are a Week 6 topic). It builds
on the joins from Week 5. Notebook 02 also reviews `GROUP BY` /
`HAVING` (Week 2) and `COALESCE` / `IS NULL` (Week 5). Its
today-vs-yesterday part is a good warm-up for `LAG()` in bonus Week 11.

## How to Run

**No install needed:** open any notebook in your web browser with molab:

* [**Open `self_join_notebook_01_quickstart.py` in molab**](https://molab.marimo.io/github/mahmoudparsian/OMIS-105/blob/main/tutorials/SELF_JOIN/self_join_notebook_01_quickstart.py/wasm)
* [**Open `self_join_notebook_02_company.py` in molab**](https://molab.marimo.io/github/mahmoudparsian/OMIS-105/blob/main/tutorials/SELF_JOIN/self_join_notebook_02_company.py/wasm)
* [**Open `self_join_notebook_03_referrals.py` in molab**](https://molab.marimo.io/github/mahmoudparsian/OMIS-105/blob/main/tutorials/SELF_JOIN/self_join_notebook_03_referrals.py/wasm)

Or run one on your own computer:

```bash
cd tutorials/SELF_JOIN
marimo edit self_join_notebook_02_company.py
```

Requirements: `duckdb`, `pandas`, and `marimo`
(see `software_installation/` if you have not installed them yet).

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
