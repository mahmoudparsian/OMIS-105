import json

def md(*lines):
    return {"cell_type": "markdown", "id": None, "metadata": {}, "source": list(lines)}

def code(*lines):
    return {"cell_type": "code", "execution_count": None, "id": None, "metadata": {}, "outputs": [], "source": list(lines)}

import uuid
cells_raw = [

md(
"# 🔗 Foreign Keys & JOINs in Relational Databases\n",
"### A Hands-On Tutorial with DuckDB\n",
"\n",
"---\n",
"\n",
"## What You Will Learn\n",
"\n",
"| Topic | Description |\n",
"|---|---|\n",
"| **Primary Key (PK)** | Quick recap — uniquely identifies every row |\n",
"| **Foreign Key (FK)** | Links rows in one table to rows in another |\n",
"| **Referential Integrity** | Why the database enforces FK rules |\n",
"| **INNER JOIN** | Returns only rows that match in **both** tables |\n",
"| **LEFT JOIN** | Returns **all** rows from the left table, matched or not |\n",
"| **RIGHT JOIN** | Returns **all** rows from the right table, matched or not |\n",
"\n",
"---\n",
"\n",
"## The Schema We Will Use\n",
"\n",
"```\n",
" departments                       employees\n",
"┌─────────────────────────┐       ┌──────────────────────────────┐\n",
"│ dept_id   PK  INTEGER   │◄──FK──│ emp_id    PK  INTEGER        │\n",
"│ dept_name     VARCHAR   │       │ dept_id   FK  INTEGER (NULL) │\n",
"│ dept_location VARCHAR   │       │ gender        VARCHAR        │\n",
"│ budget        INTEGER   │       │ salary        INTEGER        │\n",
"└─────────────────────────┘       └──────────────────────────────┘\n",
"```\n",
"\n",
"**Key design decisions:**\n",
"- `employees.dept_id` is a **Foreign Key** pointing to `departments.dept_id`.\n",
"- `employees.dept_id` is **nullable** — some employees have not yet been assigned to a department.\n",
"- One department (`LEGAL`) has **no employees** — intentional, so RIGHT JOIN has something to show.\n",
"- The FK constraint means you **cannot** insert an employee with a `dept_id` that does not exist in `departments`.",
),

md(
"---\n",
"## 0 · Setup\n",
"\n",
"Install dependencies (safe to re-run), import libraries, and connect to DuckDB.",
),

code("! pip install duckdb pandas matplotlib ipython notebook --quiet"),

code(
"import duckdb\n",
"import pandas as pd\n",
"import sys, os\n",
"\n",
"sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))\n",
"from fk_joins_plot_util import (\n",
"    display_table,\n",
"    plot_join_counts,\n",
"    plot_salary_by_dept,\n",
"    plot_budget_vs_headcount,\n",
"    plot_null_dept_pie,\n",
")\n",
"\n",
"DEPT_CSV = 'data/departments.csv'\n",
"EMP_CSV  = 'data/employees.csv'\n",
"\n",
"# In-memory DuckDB — fresh each run, so notebook is fully idempotent\n",
"con = duckdb.connect(database=':memory:')\n",
"print('✅  DuckDB connected  |  version:', duckdb.__version__)",
),

md(
"---\n",
"## 1 · Quick Recap — Primary Key (PK)\n",
"\n",
"A **Primary Key** uniquely identifies every row in a table.\n",
"\n",
"Rules:\n",
"- Every value must be **unique** — no two rows share the same PK.\n",
"- PK columns can **never be NULL**.\n",
"- A table can have only **one** primary key (though it may span multiple columns).\n",
"\n",
"In our schema:\n",
"- `departments.dept_id` is the PK of the departments table.\n",
"- `employees.emp_id` is the PK of the employees table.",
),

md(
"---\n",
"## 2 · Foreign Key (FK) — The Link Between Tables\n",
"\n",
"A **Foreign Key** is a column in one table that **references the Primary Key of another table**.\n",
"\n",
"```\n",
"  departments.dept_id  ←──── employees.dept_id\n",
"       (PK)                       (FK)\n",
"```\n",
"\n",
"### What the FK constraint guarantees\n",
"\n",
"| Scenario | Without FK | With FK enforced |\n",
"|---|---|---|\n",
"| Insert employee with `dept_id = 99` (non-existent) | Silently accepted ❌ | Error raised ✅ |\n",
"| Delete a dept that still has employees | Silently accepted ❌ | Error raised ✅ |\n",
"\n",
"### NULL is allowed\n",
"\n",
"A FK column *may* be `NULL` — it simply means the row has no parent yet.  \n",
"In our data, employees 401 and 402 have `dept_id = NULL`, meaning they have not been assigned to any department.",
),

md(
"---\n",
"## 3 · Create Tables and Load Data\n",
"\n",
"We always create the **parent table first** (`departments`), then the **child table** (`employees`).  \n",
"The FK cannot reference a table that does not yet exist.",
),

code(
"# ── Parent table first ───────────────────────────────────────────────────────\n",
"con.execute('DROP TABLE IF EXISTS employees')    # child must be dropped first\n",
"con.execute('DROP TABLE IF EXISTS departments')\n",
"\n",
"sql = \"\"\"\n",
"CREATE TABLE departments (\n",
"    dept_id       INTEGER  PRIMARY KEY,\n",
"    dept_name     VARCHAR  NOT NULL,\n",
"    dept_location VARCHAR  NOT NULL,\n",
"    budget        INTEGER  NOT NULL\n",
")\n",
"\"\"\"\n",
"con.execute(sql)\n",
"con.execute('INSERT INTO departments SELECT * FROM read_csv_auto(?)', [DEPT_CSV])\n",
"\n",
"df = con.execute('SELECT * FROM departments ORDER BY dept_id').df()\n",
"display_table(df, 'departments — 4 rows (LEGAL has no employees yet)')",
),

code(
"# ── Child table second — FK references departments ───────────────────────────\n",
"sql = \"\"\"\n",
"CREATE TABLE employees (\n",
"    emp_id   INTEGER  PRIMARY KEY,\n",
"    dept_id  INTEGER  REFERENCES departments(dept_id),  -- FK\n",
"    gender   VARCHAR  NOT NULL,\n",
"    salary   INTEGER  NOT NULL\n",
")\n",
"\"\"\"\n",
"con.execute(sql)\n",
"con.execute('INSERT INTO employees SELECT * FROM read_csv_auto(?)', [EMP_CSV])\n",
"\n",
"df = con.execute('SELECT * FROM employees ORDER BY emp_id').df()\n",
"display_table(df, 'employees — 8 rows (401 and 402 have NULL dept_id)')",
),

md(
"---\n",
"## 4 · FK Enforcement in Action\n",
"\n",
"Let's try to break referential integrity and watch DuckDB stop us.",
),

code(
"# ── Attempt 1: insert an employee pointing to a dept that does NOT exist ──────\n",
"print('Inserting emp_id=999 with dept_id=99 (dept 99 does not exist)...')\n",
"try:\n",
"    con.execute('INSERT INTO employees VALUES (999, 99, \\'MALE\\', 50000)')\n",
"    print('ERROR: DuckDB accepted an invalid FK — not good!')\n",
"except Exception as e:\n",
"    print(f'✅  DuckDB rejected it:\\n    {e}')",
),

code(
"# ── Attempt 2: delete a department that still has employees ───────────────────\n",
"print('Deleting dept_id=10 (SALES) which has employees 101 and 102...')\n",
"try:\n",
"    con.execute('DELETE FROM departments WHERE dept_id = 10')\n",
"    print('ERROR: DuckDB allowed orphaned employees — not good!')\n",
"except Exception as e:\n",
"    print(f'✅  DuckDB rejected it:\\n    {e}')",
),

code(
"# ── Attempt 3: NULL dept_id IS allowed (employee not yet assigned) ────────────\n",
"con.execute('DELETE FROM employees WHERE emp_id = 501')\n",
"print('Inserting emp_id=501 with dept_id=NULL (unassigned employee)...')\n",
"try:\n",
"    con.execute('INSERT INTO employees VALUES (501, NULL, \\'FEMALE\\', 72000)')\n",
"    df = con.execute('SELECT * FROM employees WHERE emp_id = 501').df()\n",
"    display_table(df, 'NULL dept_id accepted — employee exists but is unassigned')\n",
"    con.execute('DELETE FROM employees WHERE emp_id = 501')  # clean up\n",
"except Exception as e:\n",
"    print(f'Unexpected error: {e}')",
),

md(
"---\n",
"## 5 · Exploring the Data Before Joining\n",
"\n",
"Before writing any JOIN, understand the shape of your data:  \n",
"how many employees have a department, and how many do not?",
),

code(
"sql = \"\"\"\n",
"SELECT\n",
"    COUNT(*)                      AS total_employees,\n",
"    COUNT(dept_id)                AS with_dept,\n",
"    COUNT(*) - COUNT(dept_id)     AS without_dept\n",
"  FROM employees\n",
"\"\"\"\n",
"print('SQL:\\n', sql)\n",
"df = con.execute(sql).df()\n",
"display_table(df, 'Employee dept assignment summary')\n",
"\n",
"row = df.iloc[0]\n",
"plot_null_dept_pie(int(row['with_dept']), int(row['without_dept']))",
),

md(
"---\n",
"## 6 · JOINs — Combining Two Tables\n",
"\n",
"A **JOIN** lets you combine columns from two (or more) tables based on a matching condition.\n",
"\n",
"The general syntax is:\n",
"\n",
"```sql\n",
"SELECT ...\n",
"  FROM  left_table\n",
"  <JOIN TYPE>  right_table  ON  left_table.key = right_table.key\n",
"```\n",
"\n",
"In our case the join condition is always:\n",
"\n",
"```sql\n",
"ON employees.dept_id = departments.dept_id\n",
"```\n",
"\n",
"### The three JOIN types we will cover\n",
"\n",
"| JOIN type | What it returns |\n",
"|---|---|\n",
"| `INNER JOIN` | Only rows where `dept_id` matches in **both** tables |\n",
"| `LEFT JOIN`  | **All** employees — matched get dept info, unmatched get NULL |\n",
"| `RIGHT JOIN` | **All** departments — matched get employee info, empty depts show up too |\n",
"\n",
"Think of it visually:\n",
"\n",
"```\n",
" employees          departments\n",
"┌────────┐         ┌────────────┐\n",
"│  101   │◄───────►│     10     │  INNER: both sides match\n",
"│  102   │◄───────►│     10     │\n",
"│  201   │◄───────►│     20     │\n",
"│  202   │◄───────►│     20     │\n",
"│  301   │◄───────►│     30     │\n",
"│  302   │◄───────►│     30     │\n",
"│  401   │  NULL   │            │  LEFT only: employee has no dept\n",
"│  402   │  NULL   │            │  LEFT only: employee has no dept\n",
"│        │         │     40     │  RIGHT only: LEGAL has no employees\n",
"└────────┘         └────────────┘\n",
"```",
),

md(
"---\n",
"### 6.1  INNER JOIN\n",
"\n",
"**Returns only the rows where the join condition is satisfied on both sides.**\n",
"\n",
"- Employees with `dept_id = NULL` are **excluded** (no match).\n",
"- Department 40 (`LEGAL`) is **excluded** (no employees point to it).\n",
"- Result: only the 6 employees who are assigned to an existing department.\n",
"\n",
"> Use INNER JOIN when you only care about rows that have a complete match on both sides.",
),

code(
"sql = \"\"\"\n",
"SELECT e.emp_id,\n",
"       d.dept_name,\n",
"       d.dept_location,\n",
"       e.gender,\n",
"       e.salary\n",
"  FROM employees   AS e\n",
" INNER JOIN departments AS d\n",
"    ON e.dept_id = d.dept_id\n",
" ORDER BY e.emp_id\n",
"\"\"\"\n",
"print('SQL:\\n', sql)\n",
"df_inner = con.execute(sql).df()\n",
"display_table(df_inner,\n",
"    f'INNER JOIN — {len(df_inner)} rows '\n",
"    '(employees 401/402 excluded; LEGAL excluded)')\n",
"\n",
"plot_salary_by_dept(\n",
"    df_inner.groupby('dept_name', as_index=False)['salary'].mean().rename(\n",
"        columns={'salary': 'avg_salary'}),\n",
"    title='INNER JOIN — Average Salary per Department'\n",
")",
),

md(
"---\n",
"### 6.2  LEFT JOIN\n",
"\n",
"**Returns every row from the LEFT table (`employees`), plus matching columns from the RIGHT table (`departments`) where available.**\n",
"\n",
"- Employees **with** a valid `dept_id` → dept columns filled in.\n",
"- Employees **without** a `dept_id` (NULL) → still appear, but dept columns are `NULL`.\n",
"- Department 40 (`LEGAL`) → still excluded because no employees reference it.\n",
"\n",
"> Use a LEFT JOIN when you need all records from the left table, regardless of whether a match exists.  \n",
"> Classic question: *Show all employees and their department if they have one.*",
),

code(
"sql = \"\"\"\n",
"SELECT e.emp_id,\n",
"       e.dept_id            AS emp_dept_id,\n",
"       d.dept_name,\n",
"       d.dept_location,\n",
"       e.gender,\n",
"       e.salary\n",
"  FROM employees   AS e\n",
"  LEFT JOIN departments AS d\n",
"    ON e.dept_id = d.dept_id\n",
" ORDER BY e.emp_id\n",
"\"\"\"\n",
"print('SQL:\\n', sql)\n",
"df_left = con.execute(sql).df()\n",
"display_table(df_left,\n",
"    f'LEFT JOIN — {len(df_left)} rows '\n",
"    '(all 8 employees; 401/402 show NULL for dept columns)')",
),

code(
"# ── Use LEFT JOIN + WHERE IS NULL to find unassigned employees ────────────────\n",
"sql = \"\"\"\n",
"SELECT e.emp_id,\n",
"       e.gender,\n",
"       e.salary,\n",
"       d.dept_name\n",
"  FROM employees   AS e\n",
"  LEFT JOIN departments AS d\n",
"    ON e.dept_id = d.dept_id\n",
" WHERE d.dept_id IS NULL\n",
" ORDER BY e.emp_id\n",
"\"\"\"\n",
"print('SQL:\\n', sql)\n",
"df_unassigned = con.execute(sql).df()\n",
"display_table(df_unassigned,\n",
"    'LEFT JOIN + WHERE IS NULL — employees with no department assigned')",
),

md(
"---\n",
"### 6.3  RIGHT JOIN\n",
"\n",
"**Returns every row from the RIGHT table (`departments`), plus matching columns from the LEFT table (`employees`) where available.**\n",
"\n",
"- Departments **with** employees → those employees appear.\n",
"- Department 40 (`LEGAL`) → still appears, but employee columns are `NULL`.\n",
"- Employees 401/402 (no dept) → excluded because they match no department.\n",
"\n",
"> Use a RIGHT JOIN when you need all records from the right table.  \n",
"> Classic question: *Show all departments — even the ones with no staff.*\n",
"\n",
"> **Tip:** A RIGHT JOIN is equivalent to swapping table order and writing a LEFT JOIN.  \n",
"> Most developers prefer LEFT JOINs for readability, but RIGHT JOIN is useful when reordering the FROM clause is awkward.",
),

code(
"sql = \"\"\"\n",
"SELECT d.dept_id,\n",
"       d.dept_name,\n",
"       d.dept_location,\n",
"       d.budget,\n",
"       e.emp_id,\n",
"       e.gender,\n",
"       e.salary\n",
"  FROM employees   AS e\n",
" RIGHT JOIN departments AS d\n",
"    ON e.dept_id = d.dept_id\n",
" ORDER BY d.dept_id, e.emp_id\n",
"\"\"\"\n",
"print('SQL:\\n', sql)\n",
"df_right = con.execute(sql).df()\n",
"display_table(df_right,\n",
"    f'RIGHT JOIN — {len(df_right)} rows '\n",
"    '(LEGAL dept_id=40 appears with NULL employee columns)')",
),

code(
"# ── RIGHT JOIN + WHERE IS NULL to find departments with NO employees ──────────\n",
"sql = \"\"\"\n",
"SELECT d.dept_id,\n",
"       d.dept_name,\n",
"       d.dept_location,\n",
"       d.budget\n",
"  FROM employees   AS e\n",
" RIGHT JOIN departments AS d\n",
"    ON e.dept_id = d.dept_id\n",
" WHERE e.emp_id IS NULL\n",
" ORDER BY d.dept_id\n",
"\"\"\"\n",
"print('SQL:\\n', sql)\n",
"df_empty_depts = con.execute(sql).df()\n",
"display_table(df_empty_depts,\n",
"    'RIGHT JOIN + WHERE IS NULL — departments with no employees')",
),

md(
"---\n",
"## 7 · Comparing the Three JOINs Side-by-Side\n",
"\n",
"The same two tables, three different lenses:",
),

code(
"labels = ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN']\n",
"counts = [len(df_inner), len(df_left), len(df_right)]\n",
"\n",
"for label, count in zip(labels, counts):\n",
"    print(f'  {label:<12}  →  {count} rows')\n",
"\n",
"plot_join_counts(labels, counts)",
),

md(
"---\n",
"## 8 · Analytics Across Tables\n",
"\n",
"JOINs become powerful when combined with aggregations.  \n",
"Here we combine data from both tables to answer real business questions.",
),

code(
"# ── Headcount, avg salary, and budget per department ─────────────────────────\n",
"sql = \"\"\"\n",
"SELECT d.dept_name,\n",
"       d.dept_location,\n",
"       d.budget,\n",
"       COUNT(e.emp_id)         AS headcount,\n",
"       ROUND(AVG(e.salary), 0) AS avg_salary\n",
"  FROM departments AS d\n",
"  LEFT JOIN employees AS e\n",
"    ON d.dept_id = e.dept_id\n",
" GROUP BY d.dept_name, d.dept_location, d.budget\n",
" ORDER BY headcount DESC\n",
"\"\"\"\n",
"print('SQL:\\n', sql)\n",
"df_stats = con.execute(sql).df()\n",
"display_table(df_stats, 'Dept stats — headcount, avg salary, budget (LEGAL shows 0 headcount)')\n",
"\n",
"df_with_emp = df_stats[df_stats['headcount'] > 0].copy()\n",
"plot_salary_by_dept(df_with_emp, title='Average Salary by Department (assigned employees only)')",
),

code(
"# ── Budget vs headcount scatter (all depts including empty LEGAL) ─────────────\n",
"plot_budget_vs_headcount(\n",
"    df_stats,\n",
"    title='Department Budget vs Headcount'\n",
")",
),

code(
"# ── Budget per assigned employee (resource efficiency) ───────────────────────\n",
"sql = \"\"\"\n",
"SELECT d.dept_name,\n",
"       d.budget,\n",
"       COUNT(e.emp_id)                                    AS headcount,\n",
"       ROUND(d.budget * 1.0 / NULLIF(COUNT(e.emp_id),0)) AS budget_per_employee\n",
"  FROM departments AS d\n",
"  LEFT JOIN employees AS e\n",
"    ON d.dept_id = e.dept_id\n",
" GROUP BY d.dept_name, d.budget\n",
" ORDER BY budget_per_employee DESC NULLS LAST\n",
"\"\"\"\n",
"print('SQL:\\n', sql)\n",
"df_eff = con.execute(sql).df()\n",
"display_table(df_eff,\n",
"    'Budget per employee by department '\n",
"    '(LEGAL shows NULL — divide by zero avoided with NULLIF)')",
),

md(
"---\n",
"## 9 · Summary\n",
"\n",
"| Concept | Key Takeaway |\n",
"|---|---|\n",
"| **Primary Key** | Uniquely identifies every row; never NULL |\n",
"| **Foreign Key** | Links child rows to parent rows; enforces referential integrity |\n",
"| **FK + NULL** | A NULL FK is allowed — it means not yet assigned |\n",
"| **INNER JOIN** | Only matched rows on both sides — strictest, smallest result |\n",
"| **LEFT JOIN** | All rows from the left table — unmatched right columns become NULL |\n",
"| **RIGHT JOIN** | All rows from the right table — unmatched left columns become NULL |\n",
"| **IS NULL trick** | Combine with LEFT/RIGHT JOIN to find *unmatched* rows specifically |\n",
"\n",
"### When to use which JOIN?\n",
"\n",
"- **INNER JOIN** — Give me only records that exist in both tables.\n",
"- **LEFT JOIN** — Give me everything from the left table; fill in right-side data where it exists.\n",
"- **RIGHT JOIN** — Give me everything from the right table; fill in left-side data where it exists.\n",
"\n",
"> **Good habit:** Always think about NULLs *before* writing a JOIN.  \n",
"> Ask yourself: are there rows on either side that have no match? What should happen to them?",
),

]

# Assign unique IDs
for i, cell in enumerate(cells_raw):
    cell["id"] = str(uuid.uuid4())[:8]

nb = {
    "cells": cells_raw,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

out = '/sessions/great-bold-newton/mnt/FK_JOINS/fk_joins.ipynb'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

# Verify
with open(out, encoding='utf-8') as f:
    nb2 = json.load(f)

import ast
errors = []
for i, cell in enumerate(nb2['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        if src.startswith('!'):
            continue
        try:
            ast.parse(src)
        except SyntaxError as e:
            errors.append(f"Cell {i}: {e}")

total = len(nb2['cells'])
code_c = sum(1 for c in nb2['cells'] if c['cell_type'] == 'code')
md_c   = sum(1 for c in nb2['cells'] if c['cell_type'] == 'markdown')

if errors:
    for e in errors: print("SYNTAX ERROR:", e)
else:
    print(f"✅  JSON valid, all code cells parse OK")
    print(f"   Total cells: {total}  ({code_c} code, {md_c} markdown)")

