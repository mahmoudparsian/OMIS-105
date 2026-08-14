# 🐍 Python + DuckDB — CRUD from a Program

**OMIS-105 · Week 1 — Database Foundations**

Two plain Python scripts showing how an application talks to a database. Every one
of the four CRUD operations — **C**reate, **R**ead, **U**pdate, **D**elete — is
demonstrated with the SQL printed before it runs and the table shown before and
after.

---

## Run it

> ⚠️ **These are scripts, not notebooks.** Unlike most stories here, they are
> standalone `.py` programs you run from the terminal — no Marimo, no cells, nothing
> to click.

```bash
python3 python_duckdb_crud_in_memory.py     # nothing written to disk
python3 python_duckdb_crud_persistent.py    # creates sales_demo.duckdb
```

That is deliberate:

- It is the shape **real application code** takes.
- A program opens a connection, does its work, and closes it.
- Nobody is sitting there running cells one at a time.

| File | Database | Survives after the program exits? |
|---|---|---|
| `python_duckdb_crud_in_memory.py` | `:memory:` | ❌ No |
| `python_duckdb_crud_persistent.py` | `sales_demo.duckdb` | ✅ Yes |
| `python_duckdb_crud_persistent.py.README.md` | — | Original build spec (provenance) |

**Run the in-memory one first.** The pair only teaches its lesson in that order.

---

## What they cover

Both scripts walk the same eight steps against a `sales` table:

| Step | Operation | SQL |
|---|---|---|
| 1 | Create the table | `CREATE TABLE` with `PRIMARY KEY`, `NOT NULL` |
| 2 | Insert 4 records **one at a time** | `INSERT INTO … VALUES` |
| 3 | Insert 4 records **in bulk** | `executemany` — one call, many rows |
| 4–5 | Update a column, then another | `UPDATE … SET … WHERE` |
| 6–7 | Delete two records by `sale_id` | `DELETE FROM … WHERE` |
| 8 | Read the final state | `SELECT *` |

Every step prints the SQL, then the table before and after — so you can see exactly
what each statement changed.

---

## The table

```sql
sales (
    sale_id    INTEGER PRIMARY KEY,
    customer   VARCHAR NOT NULL,
    product    VARCHAR NOT NULL,
    price      DECIMAL(10,2) NOT NULL,
    sale_date  DATE
)
```

---

## Two details worth noticing

**One-at-a-time versus bulk (steps 2 and 3).**

- Both insert four rows, and both end with the same data.
- Step 2 makes **four separate calls**; step 3 makes **one**.
- On four rows the difference is invisible.
- On four million it is the difference between seconds and hours.
- **Same result, very different cost.**

**`WHERE` on `UPDATE` and `DELETE` is not optional.**

- Steps 4–7 all filter by `sale_id`, so each one changes exactly one row.
- Leave the `WHERE` off and the statement applies to **every row in the table**.
- **No error is raised.** It simply does what you asked.
- This is the most expensive beginner mistake in SQL — better made here, on eight
  rows, than on eight million.

---

## Teaching notes

- Run the in-memory script twice in a row: identical output both times, because it
  starts empty every run. Then run the persistent one twice and watch it behave
  differently the second time. That contrast is the whole point of the pair.
- Ask what would happen if step 6's `DELETE` had no `WHERE`. Then let someone try it
  on the in-memory version, where the damage lasts about a second.
- These scripts pair well with `duckdb_magic_notebooks/`, which makes the same
  memory-versus-file point from the notebook side.
