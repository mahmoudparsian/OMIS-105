# SQL Subqueries and `WITH` (CTEs) in DuckDB

A **subquery** is a query inside another query. A **CTE** (Common Table
Expression, written with `WITH`) is a subquery that you give a name and
write first. This folder teaches both, step by step, with small tables
you create yourself — no data files are needed.

**Course fit:** Week 7 — Subqueries. The CTE and ranking lessons also
support Week 9 (window functions and CTEs).

## Files — read them in this order

| # | File | What it is | Tables used |
|---|---|---|---|
| 1 | [`subqueries_01_basics.md`](subqueries_01_basics.md) | A short first look: the "solve for X" idea, then three levels — one value, a list, a table in `FROM`. Includes common errors. | `employees` (5 rows) |
| 2 | [`subqueries_02_single_table.md`](subqueries_02_single_table.md) | Scalar, `IN`, derived-table, and correlated subqueries on one table, then the same ideas rewritten with `WITH`. | `employees` (7 rows) |
| 3 | [`subqueries_03_two_tables.md`](subqueries_03_two_tables.md) | Two related tables: `INNER JOIN`, `IN`, `EXISTS`, scalar subqueries, and CTEs that join. | `departments`, `employees` |
| 4 | [`subqueries_notebook_01.py`](subqueries_notebook_01.py) | A Marimo notebook with the very basics: one value (`=`, `>`, `MAX`), a subquery in `SELECT`, a list (`IN`, `NOT IN`), a table in `FROM`, the most common error, an interactive demo, and 3 exercises. | `employees` (8 rows) |
| 5 | [`subqueries_notebook_03.py`](subqueries_notebook_03.py) | A Marimo notebook on **correlated subqueries** and **`EXISTS` / `NOT EXISTS`**, including the alias pitfall, the `NOT IN` + `NULL` trap, two interactive demos, and 3 exercises. | `departments`, `employees` (9 rows) |
| 6 | [`subqueries_notebook_04.py`](subqueries_notebook_04.py) | A Marimo notebook on **CTEs with `WITH`**, step by step: subquery → CTE, anatomy, chained CTEs, CTE + `JOIN`, using a CTE twice, debugging a pipeline one step at a time (interactive), real error messages, and 3 exercises. | `departments`, `employees` (8 rows) |
| 7 | [`subqueries_notebook_02.py`](subqueries_notebook_02.py) | A Marimo notebook: 9 lessons + a finale on `WITH` — from one CTE to multi-step pipelines and ranking (`ROW_NUMBER`, `RANK`, `DENSE_RANK`). | `employees` (20 rows) |
| 8 | [`subqueries_04_tutorial.md`](subqueries_04_tutorial.md) | The complete reference: every subquery type, `ANY`/`ALL`, recursive CTEs, joins vs. subqueries, common mistakes, and 15 exercises with solutions. | `sales`, then `sales` + `products` |

Files 1–3 are quick reads (15–30 minutes each). Notebooks 01, 03, and
04 take about 45 minutes each, and notebook 02 about one hour. File 8 is
long — use it as a reference and for practice.

**Short on time?** Do the four notebooks in the order of the table:
`01` (basics) → `03` (correlated subqueries, `EXISTS`) → `04` (CTEs,
step by step) → `02` (more CTE patterns and ranking). Each notebook
creates its own tables, so none of them needs another file.

Each Markdown file creates its own tables at the top, so you can run
its SQL in any DuckDB tool (the DuckDB CLI, qStudio, or a Marimo
notebook). Run the setup block first, then the examples in order.

## How to run the notebooks

You need the course software (see `software_installation/`):

```bash
pip install duckdb marimo pandas
```

Open a terminal in this folder and run:

```bash
marimo edit subqueries_notebook_01.py
marimo edit subqueries_notebook_02.py
marimo edit subqueries_notebook_03.py
marimo edit subqueries_notebook_04.py
```

Each command opens a notebook in your browser. Both notebooks create
their own tables, so no data files are needed.

### Notebook 01 — the very basics

**Dataset (`employees`, 8 rows):** `emp_id`, `name`, `dept` (Sales,
Engineering, Marketing, HR), `salary`.

| Part | Queries | Key idea |
|---|---|---|
| 1 | Q1 | Look at the data |
| 2 | Q2 – Q4 | A question in two steps; replace a typed number with a subquery; read it from the inside out |
| 3 | Q5 | One value: who earns the most (`MAX`) |
| 4 | Q6 | A subquery as a column in `SELECT` |
| 5 | Q7 | A subquery that returns text: same department as Farid |
| 6 | Q8 – Q10 | A list: `IN` and `NOT IN` (and the `NULL` warning) |
| 7 | Q11 – Q13 | A table in `FROM` (derived table); why `MAX(AVG(...))` fails |
| 8 | — | The most common error: `=` with a subquery that returns a list |
| 9 | — | Interactive: pick a department, see the inner and outer results change |
| 10 | E1 – E3 | Exercises with hidden solutions |

### Notebook 03 — correlated subqueries and `EXISTS`

**Dataset:** `departments` (5 rows — Legal has no employees) and
`employees` (9 rows — Ivan, a new hire, has a `NULL` department).

| Part | Queries | Key idea |
|---|---|---|
| 1–2 | Q1 – Q4 | The data; why "above *my department's* average" needs a new idea |
| 3 | Q5 | First correlated subquery: `WHERE x.dept_id = e.dept_id`, read as a loop |
| 4 | Q6 | X-ray: the correlated subquery as a column, one result per row |
| 5 | — | Interactive: pick an employee, see the inner query for that row |
| 6 | Q7 | Top earner in each department (`MAX`) |
| 7 | Q8 | Pitfall: no aliases → no error, but a wrong answer |
| 8 | Q9 – Q11 | `EXISTS`; why it never duplicates rows, unlike `JOIN` |
| 9 | Q12 | `NOT EXISTS` — the anti-join (departments with no employees) |
| 10 | Q13 – Q15 | The `NOT IN` + `NULL` trap: zero rows, and two fixes |
| 11 | — | Interactive: salary slider, `EXISTS` vs. `NOT EXISTS` side by side |
| 12 | E1 – E3 | Exercises with hidden solutions |

### Notebook 04 — CTEs with `WITH`, step by step

**Dataset:** `departments` (5 rows — Legal has no employees) and the
same 8 `employees` as notebook 01.

| Part | Queries | Key idea |
|---|---|---|
| 1 | Q1 – Q2 | Look at the data |
| 2 | Q3 – Q4 | Cut a derived table out, move it to the top, give it a name |
| 3 | — | Anatomy of `WITH`: one `WITH`, commas between CTEs, none before the main `SELECT` |
| 4 | Q5 | A one-row CTE + `CROSS JOIN` (company average) |
| 5 | Q6 | Two independent CTEs |
| 6 | Q7 – Q8 | A CTE that reads an earlier CTE, vs. the same query nested without `WITH` |
| 7 | Q9 – Q10 | CTE + `LEFT JOIN` (keeps Legal); the CTE version of notebook 03's correlated query |
| 8 | Q11 | Using the same CTE twice |
| 9 | Q12 | Interactive: inspect each step of a 3-CTE pipeline with `SELECT * FROM <step>` |
| 10 | — | Five real error messages (scope, order, double `WITH`, missing/extra comma); when to use a CTE |
| 11 | E1 – E3 | Exercises with hidden solutions |

### Notebook 02 — more CTE patterns and ranking

Every query result is shown as a styled HTML table by a small `show()`
helper defined in the first code cell.

**Dataset (`employees`, 20 rows):**

| Column | Description |
|---|---|
| `emp_id` | Unique employee ID |
| `name` | Employee name |
| `department` | Department they belong to |
| `job_title` | Their role |
| `salary` | Annual salary (USD) |
| `years_exp` | Years of experience |
| `hire_year` | Year they were hired |
| `rating` | Annual performance rating (1–5) |

**Lessons:**

| Lesson | Pattern | Key idea |
|------|---------|----------|
| 1 | Why `WITH`? | The same question as a subquery and as a named CTE |
| 2 | Basic `WITH` | Filter rows inside a CTE, then filter again in the main query |
| 3 | Aggregate in a CTE | Put `GROUP BY` in the CTE; the outer query just formats and sorts |
| 4 | Two CTEs | List CTEs with a comma, then use both in the main query |
| 5 | Join a CTE to the base table | Compute a summary, then `JOIN` it back to the detail rows |
| 6 | Three CTEs | A pipeline: max salary → top earners → elite filter |
| 7 | Derive + aggregate | Create a salary band with `CASE` in a CTE, then `GROUP BY` it |
| 8 | Ranking functions | `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()` side by side — they differ only on ties |
| 9 | Filter by rank | Rank inside a CTE, then `WHERE rank = 1` outside |
| 🏁 | Grand Finale | Three CTEs, salary bands, department ranking, and a company-average filter |

## Key takeaways

- **Know the shape of the inner result** before you write the outer
  query. One value → use `=`, `>`, `<`. A list → use `IN` or
  `EXISTS`. A table → put it in `FROM` (or in a CTE).
- A **correlated** subquery uses a column from the outer query, so its
  answer changes for each outer row (for example, "the average of
  *this* employee's department").
- **`NOT IN` has a `NULL` trap:** if the list contains a `NULL`, you
  get no rows. `NOT EXISTS` does not have this problem.
- **`WITH name AS (...)`** gives a step a name. A CTE can use any CTE
  defined before it, so you can build a query as a pipeline of steps.
- Window functions (`RANK()` and friends) cannot go in `WHERE`.
  Compute them in a CTE, then filter on the result.

**Next steps:** `tutorials/Ranking_Functions/` and
`tutorials/LIMIT_vs_RANK/` go deeper into ranking; the Week 7 lecture
folder (`weekly_lectures/week07-subqueries/`) has slides, demos, and a
lab on the same topics.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
