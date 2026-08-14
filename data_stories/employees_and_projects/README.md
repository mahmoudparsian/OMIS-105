# 🏗️ Employees & Projects — the Classic COMPANY Schema

**OMIS-105 · Week 2 — Relational Modeling** *(schema)*
**→ revisit in Week 5** *(the join queries)*

The six-table COMPANY database that appears in most database textbooks, loaded into
DuckDB. If students go on to another database course, **this is the schema they will
meet again** — which is a good reason to use it here.

Ships in **two sizes**. Pick one.

---

## Run it

```bash
marimo edit employees_and_projects_20_marimo.py     # 20 employees  ← start here
marimo edit employees_and_projects_100_marimo.py    # 100 employees
```

| File | Role |
|---|---|
| `employees_and_projects_20_marimo.py` | Notebook, reads `data/` |
| `employees_and_projects_100_marimo.py` | Notebook, reads `data2/` |
| `display_utils.py` | Table display and the avatar gallery |
| `gen_data.py` | Data generator |
| `build_notebook_*.py` | Generator scripts (produce `.ipynb`) — not the notebooks |
| `data/` | The 20-employee dataset |
| `data2/` | The 100-employee dataset |

**Use the 20-employee version for teaching.** Every result fits on screen, so students
can verify a join by counting rows by hand. Switch to 100 when you want a query whose
answer is not obvious by inspection.

| Table | 20-emp | 100-emp | Meaning |
|---|---|---|---|
| `department` | 5 | 5 | One row per department |
| `employee` | 20 | 100 | One row per person |
| `dept_locations` | 10 | 10 | **A department can have several locations** |
| `project` | 12 | 12 | One row per project |
| `works_on` | 40 | 256 | **Which employee works on which project, and for how many hours** |
| `dependent` | 16 | 83 | An employee's dependents |

---

## The schema

```
   dept_locations              department                 project
  ┌───────────────┐        ┌────────────────┐        ┌──────────────────┐
  │ dnumber   FK  │───────►│ dnumber    PK  │◄───FK──│ dnum          FK │
  │ dlocation     │        │ dname          │        │ pnumber       PK │
  │  composite PK │        │ mgr_ssn    FK  │        │ pname, plocation │
  └───────────────┘        └───────┬────────┘        └────────┬─────────┘
                                   │                          │
                                   │ FK                       │
                          ┌────────▼────────┐                 │
                          │   employee      │                 │
                          │ ssn         PK  │                 │
                          │ dno         FK  │                 │
                          │ super_ssn   FK  │◄── self-reference:
                          │ fname, lname,   │    an employee's supervisor
                          │ salary, …       │    is another employee
                          └────┬───────┬────┘                 │
                               │       │                      │
                    ┌──────────▼──┐  ┌─▼──────────────────────▼──┐
                    │ dependent   │  │ works_on                  │
                    │ essn    FK  │  │ essn, pno   composite PK  │
                    │ name        │  │ hours                     │
                    └─────────────┘  └───────────────────────────┘
```

---

## Three things this schema teaches that smaller ones cannot

**1 · A junction table that carries its own data.**

- `works_on` links employees to projects — and also stores `hours`.
- Ask where `hours` belongs. Not on the employee (they work different hours on
  different projects). Not on the project (different people work different hours on
  it).
- **It belongs to the relationship itself**, which is why the junction table is a real
  table and not just plumbing.

**2 · A foreign key that points at its own table.**

- `employee.super_ssn` points at `employee.ssn` — an employee's supervisor is another
  employee.
- One table, a foreign key onto itself.
- This is what makes *"list every employee with their manager's name"* a **self-join**,
  which students meet in Week 5.

**3 · A repeated value stored properly.**

- A department can be in several locations.
- **The wrong answer:** a `locations` column holding `"Houston, Stafford"`. You cannot
  filter it, count it, or join on it.
- **The right answer:** `dept_locations` as its own table, with a composite key.
- This is exactly what normalization exists to prevent, and Week 6 revisits it.

---

## Which section belongs to which week

| Notebook part | Teaches | Week |
|---|---|---|
| Load Data, Verify, Table Schemas | Six tables, keys, row counts | **2** |
| Query 1–2 (all employees, gallery) | `SELECT` | **3** |
| Query 3–4 (avg salary by dept, projects per dept) | `GROUP BY` | **4** |
| Query 5+ (top employees by hours) | JOINs across `employee` + `works_on` | **5** |

---

## Teaching notes

- **Start from `dept_locations` when explaining normalization.** It is small (10 rows),
  obviously repetitive, and students immediately see why it is not a column.
- The self-reference on `super_ssn` reliably confuses people the first time. Drawing
  it as an arrow leaving `employee` and coming back into `employee` helps more than
  any sentence.
- Because this schema is a textbook standard, exercises written for it elsewhere will
  work unchanged — useful if you want extra practice problems without authoring them.
