# 🐈 Cats, Breeds & Tricks

**OMIS-105 · Week 2 — Relational Modeling** *(schema)*
**→ revisit in Weeks 3 and 5** *(the notebook's later sections)*

A cat show database in four tables. Small enough to hold in your head, but it
contains a **genuine many-to-many relationship** — which is the one modelling idea
that cannot be taught with two tables.

**Use it more than once.** The schema is Week 2 material, but the notebook keeps
going: Section 1 is Week 3 (`SELECT`), Section 2 is Week 5 (JOINs), and Sections 3–5
go past the syllabus into CTEs and window functions. Stop where your week stops.

---

## Run it

```bash
marimo edit cats_and_breeds_duckdb_marimo.py    # interactive
marimo run  cats_and_breeds_duckdb_marimo.py    # read-only
```

| File | Role |
|---|---|
| `cats_and_breeds_duckdb_marimo.py` | The notebook |
| `display_utils.py` | Table display helpers |
| `plot_utils.py` | Chart functions |
| `cats_package.md` | The dataset write-up |
| `cats_cte_ranking_queries.md` | Extra queries using CTEs and ranking — **beyond the Week 2 syllabus** |
| `build_notebook.py` | Generator script — not the notebook itself |
| `data/*.csv` | Four CSV files |

---

## The schema

```
   breeds                    cats                     cat_tricks              tricks
┌──────────────┐      ┌──────────────────┐      ┌──────────────────┐    ┌─────────────┐
│ breed_id  PK │◄─FK──│ cat_id        PK │◄─FK──│ cat_id        FK │    │ trick_id PK │
│ breed_name   │      │ breed_id      FK │      │ trick_id      FK │───►│ trick_name  │
│ …            │      │ name, age, …     │      │  composite PK    │    │ difficulty  │
└──────────────┘      └──────────────────┘      └──────────────────┘    └─────────────┘
      1 ─── many              many ─────────── many
```

| Table | Rows | Meaning |
|---|---|---|
| `breeds` | 15 | One row per breed |
| `cats` | 80 | One row per cat |
| `tricks` | 15 | One row per trick |
| `cat_tricks` | 374 | **Which cat can do which trick** |

---

## The one idea to take away

There are two different kinds of relationship here, and they are modelled
differently.

**A cat has one breed.** That is *one-to-many* — many cats, one breed each — so it
fits in a single column: `cats.breed_id`.

**A cat knows many tricks, and a trick is known by many cats.** That is
*many-to-many*, and it does **not** fit in a column. You cannot put a list in
`cats.tricks` — the moment you try, you cannot query it, count it, or join on it.

The answer is a fourth table whose entire job is to hold the pairs:

```
cat_tricks
  cat_id   trick_id
     7        3        ← cat 7 can do trick 3
     7        9        ← cat 7 can also do trick 9
    12        3        ← cat 12 can also do trick 3
```

That table is called a **junction table** (or bridge, or link table). Its primary key
is the pair `(cat_id, trick_id)` — which also encodes a rule: *a cat can know a given
trick only once.*

**374 rows across 80 cats and 15 tricks.** Neither table could have held that.

---

## Which section belongs to which week

The notebook is a full ladder, not a single lesson. Assign the part you need:

| Notebook section | Teaches | Week |
|---|---|---|
| Database Schema, Create Tables | PK, FK, junction table | **2** |
| Section 1 — Basic SELECT | `SELECT`, `WHERE`, `ORDER BY` | **3** |
| Section 2 — JOIN Queries | `INNER`/`LEFT JOIN` across all four tables | **5** |
| Section 3 — CTEs | `WITH … AS` | *beyond the core* |
| Section 4 — Window & Ranking | `ROW_NUMBER`, `RANK` | *beyond the core* |
| Section 5 — Advanced Analytics | mixed | *beyond the core* |

Sections 3–5, and the whole of `cats_cte_ranking_queries.md`, use techniques the
10-week core does not teach (see the outline's optional Advanced SQL appendix). They
are fine as enrichment or demonstration — just not as assessed work.

---

## Teaching notes

- **Ask the modelling question before showing the answer.** "Cat number 7 can do five
  tricks. Where do we put that?" Let students propose a `tricks` column. Then ask them
  to write the query for *"which cats can do trick 3?"* against their design.
- Once `cat_tricks` exists, `COUNT(*)` per cat and per trick both become one-line
  queries. That is the payoff, and it is worth showing immediately.
- `cats_and_breeds_and_images/` is the same schema with cat avatar images added — use
  one or the other, not both.
- The junction table here is the same shape as `dept_employee` in
  `DuckDB_Employee_SQL_Mastery/` and `employee_projects` in `emps_depts_projects/`.
  Pointing that out helps students recognise the pattern rather than memorise a case.
