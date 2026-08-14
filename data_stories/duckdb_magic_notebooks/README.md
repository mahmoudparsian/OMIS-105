# ✨ DuckDB + JupySQL — Magic Notebooks

**OMIS-105 · Week 1 — Database Foundations**

Two short, deliberately near-identical notebooks that demonstrate **one idea**: the
difference between a database that lives in memory and one that lives in a file.

Same table, same rows, same queries. The only difference is where the data goes —
and whether it is still there tomorrow.

---

## Run it

```bash
marimo edit duckdb_magic_memory_marimo.py       # in-memory
marimo edit duckdb_magic_persistent_marimo.py   # writes a file
```

| File | Database | Survives a restart? |
|---|---|---|
| `duckdb_magic_memory_marimo.py` | `:memory:` | ❌ No |
| `duckdb_magic_persistent_marimo.py` | a `.duckdb` file | ✅ Yes |

**Run them in that order.** The contrast is the lesson, and it only lands if the
in-memory one comes first.

---

## What they cover

Both notebooks do the same four things:

| § | Step | SQL |
|---|---|---|
| 1 | Create an `employees` table | `CREATE TABLE` |
| 2 | Insert 7 rows | `INSERT INTO` |
| 3 | Read all rows | `SELECT *` |
| 4 | Summarise by group | `GROUP BY` |

The persistent notebook adds a fifth step: **verify the database file exists on
disk** — proof that something was actually written.

---

## What "magic" means here

These notebooks use **JupySQL**, which lets you write SQL in a cell directly:

```sql
%%sql
SELECT department, COUNT(*) FROM employees GROUP BY department;
```

instead of wrapping every query in Python:

```python
con.execute("SELECT department, COUNT(*) FROM employees GROUP BY department").df()
```

The `%%sql` prefix is called a **cell magic**. It is a convenience, not a different
database — the SQL is identical either way.

---

## Teaching notes

- **Ask the question before running the second notebook:** "we just created a table
  with seven employees — where is it?" Most students assume a file appeared somewhere.
  The in-memory notebook proves it did not.
- This is the cheapest possible introduction to **durability**, which Week 8 makes
  formal. `TRANSACTIONS_AND_ACID/` picks up exactly this thread: in-memory versus on
  disk, committed versus uncommitted.
- If your students will use Jupyter rather than Marimo, the `%%sql` syntax here is
  the one they will meet most often in tutorials online — worth five minutes.
