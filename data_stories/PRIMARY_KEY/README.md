# 🔑 Primary Keys

**OMIS-105 · Week 2 — Relational Modeling**

Why does every table need a primary key? This notebook answers it the honest way:
it builds a table **without** one, lets bad data in, and then builds the same table
**with** one and watches the database refuse.

---

## Run it

```bash
marimo edit primary_key_marimo.py    # interactive
marimo run  primary_key_marimo.py    # read-only
```

| File | Role |
|---|---|
| `primary_key_marimo.py` | The notebook |
| `plot_util.py` | Chart helpers, kept out of the notebook |
| `data/employees.csv` | 10 employees |

---

## What it covers

| § | Section | Point |
|---|---|---|
| 0 | Setup | Connect, load the CSV |
| 1 | **The problem with no primary key** | Build `employees_no_pk`, load it, then insert a duplicate — **it works**, and now the table is corrupt |
| 2 | **Enforcing the primary key** | Build `employees` with `PRIMARY KEY`, try the same duplicate — rejected |
| 3 | CRUD operations | Insert, update, delete against a keyed table |
| 4 | Analytics queries | What a trustworthy table lets you compute |

---

## The idea

A **primary key** is a promise: *this column identifies exactly one row, and always
will.* The database enforces the promise on every single write, forever.

```
WITHOUT a primary key              WITH a primary key
────────────────────               ──────────────────
emp_id 101  Alice                  emp_id 101  Alice
emp_id 101  Alice   ← allowed!     emp_id 101  Alice   ← REJECTED
emp_id 101  Bob     ← allowed!
                                   "Which row is employee 101?"
"Which row is employee 101?"        has exactly one answer, always
   ...three answers. Or none.
```

Once duplicates get in, three things break at once:

- **Every count is wrong.** `COUNT(*)` includes the copies.
- **Every join multiplies rows.** One duplicate on one side doubles the output.
- **You cannot tell which copy is real.** Nothing marks one as the original.

**The damage is not the duplicate row itself — it is that you can no longer trust any
answer the table gives you.**

---

## Teaching notes

- **Run §1 before saying what a primary key is.** Let the duplicate insert succeed.
  Ask the class what `SELECT COUNT(*) FROM employees_no_pk WHERE emp_id = 101` should
  return, and what it now returns. The need for the constraint should be felt first.
- The `staging` table in the notebook is worth a mention: real pipelines often load
  into an unkeyed staging table on purpose, check it, and only then move clean rows
  into the keyed one. "No primary key" is sometimes a deliberate, temporary choice.
- Natural follow-on: `FK_JOINS/` (Week 5), which adds the *foreign* key — a promise
  that points at this one.

---

<details>
<summary>Original build prompt (provenance)</summary>

This folder's README previously held the prompt used to generate the notebook. It is
preserved in git history. The notebook itself is the authoritative artifact.

</details>
