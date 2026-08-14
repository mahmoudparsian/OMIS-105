# 🌐 TechNova — Employees, Departments & Projects

**OMIS-105 · Week 2 — Relational Modeling** *(schema)*
**→ revisit in Week 5** *(the join queries)*

A four-table consultancy database with a business story attached. Where
`employees_and_projects/` gives you the textbook schema, this one gives you the
**questions a manager would actually ask** — and a schema built to answer them.

---

## Run it

```bash
marimo edit technova_duckdb_analytics_marimo.py    # interactive
marimo run  technova_duckdb_analytics_marimo.py    # read-only
```

| File | Role |
|---|---|
| `technova_duckdb_analytics_marimo.py` | The notebook — 6 sections |
| `display_utils.py` | Table display helpers |
| `technova_data_story_package.md` | **The business story, schema and query set** |
| `data/*.csv` | Four CSV files |

---

## The business story

> TechNova is a global technology consultancy employing specialists from over ten
> countries. Each employee belongs to exactly one department. Employees work on
> multiple projects through the year, often across departments. Leadership wants to
> know which departments are growing fastest, how salaries differ by country, and
> which employees carry the heaviest project load.

Everything in the schema exists to answer one of those questions. That is the point
of the story: **the data model follows from what the business needs to know.**

---

## The schema

```
   departments                employees              employee_projects        projects
 ┌───────────────┐      ┌──────────────────┐      ┌──────────────────┐   ┌──────────────┐
 │ dept_id   PK  │◄─FK──│ emp_id        PK │◄─FK──│ emp_id        FK │   │ project_id PK│
 │ dept_name     │      │ dept_id       FK │      │ project_id    FK │──►│ project_name │
 │ …             │      │ name, country,   │      │  composite PK    │   │ …            │
 └───────────────┘      │ salary, …        │      └──────────────────┘   └──────────────┘
                        └──────────────────┘
       1 ─── many              many ─────────── many
```

| Table | Rows | Meaning |
|---|---|---|
| `departments` | 8 | One row per department |
| `employees` | 50 | One row per person; belongs to exactly one department |
| `projects` | 12 | One row per project |
| `employee_projects` | 72 | **Which employee works on which project** |

Two relationships, modelled two different ways:

- **An employee belongs to one department** → one-to-many → a column, `employees.dept_id`
- **An employee works on many projects, a project has many employees** → many-to-many
  → a junction table, `employee_projects`

---

## Which section belongs to which week

| Notebook section | Teaches | Week |
|---|---|---|
| 1–3 · Setup, Load, Verify | Four tables, keys, row counts | **2** |
| 4 · Basic Queries | `SELECT`, `WHERE`, `ORDER BY` | **3** |
| 5 · Join Queries | `INNER`/`LEFT JOIN` across the junction table | **5** |
| 6 · Intermediate & Advanced | Mixed; parts go past the core syllabus | **5 →** |

---

## How it compares to the other two "employees" stories

| Story | Tables | Rows | Best for |
|---|---|---|---|
| `emps_depts_projects/` (this one) | 4 | 50 employees | A **business narrative** driving the schema |
| `employees_and_projects/` | 6 | 20 or 100 | The **textbook** COMPANY schema, self-joins |
| `DuckDB_Employee_SQL_Mastery/` | 6 | 300,023 | **Scale**, composite keys, two junction tables |

They overlap heavily. Pick one per term rather than assigning several.

---

## Teaching notes

- **Read the business story aloud before showing the schema.** Then ask the class to
  sketch the tables. Most will get `departments` and `employees` right and stall on
  projects — which is exactly the moment to introduce the junction table.
- Good exercise: pick one sentence from the story ("how salaries differ by country")
  and have students trace which tables and columns are needed to answer it.
- `technova_data_story_package.md` includes a MySQL version of the schema. Comparing
  it with what DuckDB accepts is a quick, concrete look at SQL dialect differences.
