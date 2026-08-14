# 🔗 Foreign Keys & JOINs

**OMIS-105 · Week 5 — SQL Joins** *(PK/FK sections also serve Week 2)*

**The purpose-built joins story.** Two small tables, deliberately shaped so that every
kind of join returns something different — including the rows that get left out.

If you teach one joins story, teach this one.

---

## Run it

```bash
marimo edit fk_joins_marimo.py    # interactive
marimo run  fk_joins_marimo.py    # read-only
```

| File | Role |
|---|---|
| `fk_joins_marimo.py` | The notebook |
| `fk_joins_plot_util.py` | Display and chart helpers |
| `PK_FK_Concepts.md` / `.pdf` | Companion reading on keys |
| `build_notebook.py` | Generator script — not the notebook |
| `data/employees.csv` | **8 employees** |
| `data/departments.csv` | **4 departments** |

---

## The schema — and why it is built this way

```
 departments                       employees
┌─────────────────────────┐       ┌──────────────────────────────┐
│ dept_id   PK  INTEGER   │◄──FK──│ emp_id    PK  INTEGER        │
│ dept_name     VARCHAR   │       │ dept_id   FK  INTEGER (NULL) │
│ dept_location VARCHAR   │       │ gender        VARCHAR        │
│ budget        INTEGER   │       │ salary        INTEGER        │
└─────────────────────────┘       └──────────────────────────────┘
```

Three design choices make the joins teachable:

1. **`employees.dept_id` is nullable** — some employees have no department yet.
   Those are the rows a `LEFT JOIN` keeps and an `INNER JOIN` drops.
2. **One department has no employees** (`LEGAL`). That is the row a `RIGHT JOIN`
   keeps and an `INNER JOIN` drops.
3. **The foreign key is enforced** — you cannot insert an employee into a department
   that does not exist.

Because of 1 and 2, the three joins return **three different row counts**. On a
tidier dataset they would all return the same thing and the lesson would evaporate.

---

## What it covers

| § | Section |
|---|---|
| 0 | Setup |
| 1–4 | Primary keys, foreign keys, referential integrity — including failed inserts |
| 5 | Exploring the data before joining |
| 6 | **INNER JOIN** — only rows matching on both sides |
| 7 | **LEFT JOIN** — every employee, department or not |
| 8 | **RIGHT JOIN** — every department, employees or not |

---

## The one picture to remember

```
INNER JOIN     employees WITH a department          ← drops both edge cases
LEFT JOIN      ALL employees, dept may be NULL      ← finds unassigned people
RIGHT JOIN     ALL departments, emp may be NULL     ← finds empty departments
```

The useful reframing: **a `LEFT JOIN` is how you find things that are missing.**
"Which employees have no department?" and "which departments have nobody?" are the
questions joins answer that a single table cannot.

---

## Teaching notes

- **Run all three joins and compare row counts before explaining any of them.** The
  numbers differ, and "why?" is a better entry point than a definition.
- Section 4's failed `INSERT` is worth dwelling on — the database refusing to create
  an employee in a nonexistent department is referential integrity made visible.
- Related: `PRIMARY_KEY/` (Week 2) is the prerequisite; `JOIN_101_EMPS_DEPTS_*/` cover
  the same ground with more rows.
