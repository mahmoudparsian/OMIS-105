# 🏢 Employee SQL Mastery — a Real Six-Table Schema

**OMIS-105 · Week 2 — Relational Modeling**

A proper corporate HR database: **six tables, six primary keys, six foreign keys**,
and enough rows that the design has to be right. This is the story to use when you
want students to see what a real schema looks like rather than a two-table example.

---

## Run it

```bash
marimo edit DuckDB_Employee_SQL_Mastery.py    # interactive
```

| File | Role |
|---|---|
| `DuckDB_Employee_SQL_Mastery.py` | The notebook |
| `schema.sql` | **The DDL** — all six tables with their constraints |
| `notebook_helpers.py` | Display helpers |
| `build_notebook.py` | Generator script (produces `.ipynb`) — not the notebook itself |
| `data/*.csv` | Six CSV files |

---

## The schema

```
        titles                    employees                    departments
   ┌──────────────┐          ┌────────────────────┐        ┌──────────────┐
   │ title_id  PK │◄────FK───│ emp_id          PK │   ┌───►│ dept_id   PK │
   │ title        │          │ emp_title_id    FK │   │    │ dept_name    │
   └──────────────┘          │ birth_date         │   │    └──────┬───────┘
                             │ first_name         │   │           │
                             │ last_name          │   │           │
                             │ gender             │   │           │
                             │ hire_date          │   │           │
                             └─────┬──────────────┘   │           │
                                   │                  │           │
              ┌────────────────────┼──────────────────┼───────────┤
              │                    │                  │           │
        ┌─────▼──────┐   ┌─────────▼─────────┐  ┌─────▼───────────▼──────┐
        │ salaries   │   │ dept_employee     │  │ dept_manager           │
        │ emp_id  FK │   │ emp_id, dept_id   │  │ dept_id, emp_id   PK   │
        │ salary     │   │      composite PK │  │      composite PK      │
        └────────────┘   └───────────────────┘  └────────────────────────┘
```

| Table | Rows | What it holds |
|---|---|---|
| `departments` | 12 | One row per department |
| `titles` | 9 | Job titles |
| `employees` | 300,023 | One row per person |
| `salaries` | 300,023 | Pay per employee |
| `dept_employee` | 331,602 | **Which employees are in which departments** |
| `dept_manager` | 23 | Which employee manages which department |

---

## Why this schema is worth studying

**It has two junction tables.** `dept_employee` and `dept_manager` both exist because
the relationships they represent are many-to-many: an employee can move between
departments over time, and a department can have had several managers. Neither fact
fits in a column on `employees`.

**They use composite primary keys.** `PRIMARY KEY (dept_id, emp_id)` — the identity
of the row is the *pair*, not either half. This is the cleanest example of a
composite key in the whole `data_stories/` folder.

**The order of creation matters.**

- `schema.sql` opens with a comment telling you to create the tables in order.
- The reason: **a foreign key cannot point at a table that does not exist yet.**
- So `departments` and `titles` must exist before `employees` can reference them.
- A rule about *your workflow* falls straight out of a rule in the *schema*.

---

## Scale warning

- At **300,000+ employees** and **331,000+ department assignments**, this is by far
  the largest schema in `data_stories/`.
- **Good for:** showing that design decisions matter once data gets big.
- **Bad for:** a student's first `SELECT` — results are too large to read.
- **Start elsewhere:** `PRIMARY_KEY/` (10 rows) or `cats_and_breeds/` (80 cats), then
  come here.

---

## Teaching notes

- **Open `schema.sql` before the notebook.** Six `CREATE TABLE` statements read
  top-to-bottom are a better introduction to relational design than any diagram, and
  the `CONSTRAINT pk_… PRIMARY KEY (…)` syntax names each constraint explicitly.
- Ask why `dept_employee` exists at all. The wrong answer — "put a `dept_id` column on
  `employees`" — is worth exploring, because it is exactly what students will try, and
  it breaks the moment somebody transfers.
- Composite keys reappear in the Week 5 join stories. This is where they are declared.
