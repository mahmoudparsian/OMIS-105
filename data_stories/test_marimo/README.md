# ✅ Marimo + DuckDB — Smoke Test

**OMIS-105 · Setup check** *(not a data story)*

The smallest possible notebook that proves your setup works. Four SQL cells: create a
table, insert two rows, read them back, filter them.

**Run this first**, before any of the data stories. If it works, your environment is
ready. If it does not, the problem is your install — not the story you were about to
open.

---

## Run it

```bash
marimo edit test_marimo.py    # interactive
python  test_marimo.py        # quickest check — just confirms it runs
```

| File | Role |
|---|---|
| `test_marimo.py` | The notebook — 5 cells |

The database is **in-memory** (`:memory:`), so:

- Nothing is written to disk
- No file to clean up afterwards
- You can run it as many times as you like, and it always starts empty

---

## What it does

| Cell | SQL | Checks that… |
|---|---|---|
| 1 | — | `marimo` imports |
| 2 | — | `duckdb` imports and a connection opens |
| 3 | `CREATE OR REPLACE TABLE emps(name VARCHAR, age INT)` | You can create a table |
| 4 | `INSERT INTO emps VALUES ('alex', 20), ('jane', 30)` | You can write rows |
| 5 | `SELECT * FROM emps` | You can read them back |
| 6 | `SELECT * FROM emps WHERE name = 'alex'` | `WHERE` filtering works |

Expected result from the last cell: **one row — `alex`, `20`.**

---

## If it fails

| Symptom | Likely fix |
|---|---|
| `ModuleNotFoundError: marimo` | `pip install marimo` |
| `ModuleNotFoundError: duckdb` | `pip install duckdb` |
| `marimo: command not found` | Marimo installed, but not on your `PATH` — try `python -m marimo edit test_marimo.py` |
| Cells show results but nothing renders | Check you opened it with `marimo edit`, not a plain text editor |

Once this notebook runs, everything in `data_stories/` should run too.

---

## Note

This is a **setup check, not a lesson**. It is not mapped to any week, and there is
nothing here to teach — it exists so that a failing install is diagnosed in ten
seconds rather than in the middle of a class.
