# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A 12-part, ~2-hour, self-paced course ("Introduction to RDBMS with
DuckDB") taught entirely through interactive [marimo](https://marimo.io)
notebooks backed by [DuckDB](https://duckdb.org). It is not an
application — there is no build step, server, or deploy target. The
"product" is the set of `.py` notebook files themselves, meant to be
opened with `marimo edit` and worked through by a learner. See
`README.md` for the full syllabus and learner-facing instructions.

## Commands

Build the shared, persistent course database — required once before
running any notebook or the headless smoke test, and after any change
to `ecommerce_data.py`'s DDL or data-generation functions:

```bash
./create_database.sh
```

Verify it built correctly (fast, no marimo involved):

```bash
python3 -c "import duckdb; con = duckdb.connect('ecommerce_database.duckdb', read_only=True); print(con.sql('SHOW TABLES'))"
```

Open a notebook for interactive editing (what a learner does):

```bash
marimo edit 01_setup_and_marimo_basics.py
```

Structural/style lint a notebook (or all of them) — exclude
`ecommerce_data.py`, which is a plain module, not a notebook:

```bash
marimo check --ignore-scripts 0*.py 1*.py       # check all 12
marimo check --fix 05_joins.py                  # auto-fix style, then re-check
```

**Headless execution smoke test** — this is the primary way to catch
real bugs (a bad JOIN, a typo'd column, a query that raises at
runtime). `marimo check` only catches structural/style issues; it does
not execute cells. Every cell actually runs in dependency order, and
any exception surfaces immediately:

```bash
python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('nb', '<file>.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
outputs, defs = mod.app.run()
print('OK, cells ran:', len(outputs))
"
```

Run this after creating or editing **any** notebook, for every notebook
touched. Treat a passing run as required, not optional — it's what
confirms every demo query and every exercise's accordion solution
actually executes against the live data, not just "reads correctly."

There is no separate test suite, linter config, or CI — these two
commands (`marimo check` + the headless smoke test) are the full
verification loop used to build this course, for every file.

## Architecture

**`ecommerce_data.py`** is the single source of truth for the shared
sample database — a plain Python module (not a marimo notebook) with no
`app.cell` decorators. It defines:
- Five DataFrame-generating functions (`customers_df`, `employees_df`,
  `products_df`, `orders_df`, `order_items_df`), each seeded (`SEED =
  42` and small offsets) so output is identical on every call.
- `DDL`, the raw `CREATE TABLE` SQL for all five tables, with real
  constraints (`PRIMARY KEY`, composite PK on `order_items`, `FOREIGN
  KEY`, `NOT NULL`, `UNIQUE`, `CHECK`) — this is what notebook 02/03
  inspect and explain.
- `create_schema(con)` and `load_data(con)` — the low-level building
  blocks, given an open connection.
- `build_database(path=DB_PATH, overwrite=True)` — creates the
  persistent on-disk database file. Called only by `create_database.sh`,
  never by a notebook directly.

There is deliberately **no wrapper function** for connecting — notebooks
open the shared database with the plain DuckDB API,
`duckdb.connect("ecommerce_database.duckdb", read_only=True)`, the same
call notebook 01 already teaches, just pointed at a file. Don't
reintroduce a `connect()`-style helper (an `ecommerce_data.connect()`
and a `fresh_connection()` were both tried and removed) — having a
same-named wrapper alongside `duckdb.connect(...)` confused the "what
does connect even mean here" story for learners, and every notebook now
uses `duckdb.connect(...)` directly, including the ones that write.

**`create_database.sh`** is the build script: it calls
`ecommerce_data.build_database()` to (re)create
`ecommerce_database.duckdb` at the repo root. It is a **generated build
artifact, gitignored, not committed** — run the script once per clone
(or whenever `ecommerce_data.py`'s schema/data changes) before opening
any notebook. Every notebook from 02 onward connects to this one shared
file directly:
- Most open it **read-only**: `duckdb.connect("ecommerce_database.duckdb",
  read_only=True)`.
- **08** opens it read-write (`duckdb.connect("ecommerce_database.duckdb")`)
  but every `INSERT` it runs is a deliberately invalid constraint
  violation — none of them ever actually commit, so the shared file is
  never really mutated.
- **10** opens it read-write too, and *does* commit real rows and a real
  view as part of its transaction demos — but it has a cleanup cell right
  after connecting (removes leftovers from a *previous* run) and another
  right before its recap (removes what *this* run just created), so the
  shared file is back to its original state by the time the notebook
  finishes executing, regardless of how many times it's opened.
- (03's own `:memory:` demos are throwaway, unrelated connections used
  only to illustrate `CREATE TABLE`/`INSERT` by hand.)

When adding a new notebook or exercise that needs to write, follow 10's
pattern (cleanup cell before *and* after) rather than reaching for an
isolated in-memory connection — keeping every notebook on the same
`duckdb.connect("ecommerce_database.duckdb")` call is a deliberate,
learner-facing simplicity decision (see memory), not an oversight.

**`employees.manager_id` is a self-referencing
foreign key** (used later for self-join and hierarchy teaching);
because of that, `load_data()` inserts employee rows one at a time in
`employee_id` order (a single bulk `INSERT ... SELECT` fails DuckDB's FK
check on self-referencing rows — see the comment at that call site
before "simplifying" it back to a bulk insert).

**The 12 numbered notebooks** (`01_...py` through `12_...py`) are the
actual course content, meant to be read/run in order. Each is a real
marimo app file (`import marimo; app = marimo.App(...)`, a sequence of
`@app.cell` functions, `if __name__ == "__main__": app.run()`) and
follows the same internal shape:

1. A `hide_code=True` markdown cell with the title, notebook number,
   time estimate, and learning objectives.
2. A setup cell: `con = duckdb.connect("ecommerce_database.duckdb",
   read_only=True)` — omit `read_only=True` for the two notebooks (08,
   10) that write; see Architecture above.
3. Alternating explanation (markdown) cells and live-query (`con.sql(...)`)
   cells that build up the notebook's concept, each with prose
   afterward explaining *why*, not just *what*.
4. Numbered exercises: an `mo.ui.text_area` for the learner's SQL,
   followed by a cell that runs `con.sql(q.value).df()` inside a
   try/except (SQL errors render as a `mo.callout(..., kind="danger")`
   rather than crashing the notebook), followed by a `mo.accordion`
   containing the worked solution — collapsed by default so learners
   attempt the exercise before checking.
5. A closing `hide_code=True` recap cell that names what was covered and
   links to the next notebook by filename.

When adding a new notebook or exercise, match this shape exactly —
it's what makes the course consistent and self-teaching. Interactive
elements throughout favor `mo.ui.slider`/`mo.ui.dropdown`/
`mo.ui.radio` feeding directly into parameterized `con.execute(sql,
[params]).fetchdf()` calls (not f-string interpolation) wherever a
value comes from a UI element — this is a deliberate, called-out
teaching point (notebook 02 flags the injection risk; notebook 04 fixes
it) and should stay consistent in any new interactive cell.

`mo.sql(query, engine=con)` (marimo's native SQL-cell form) is used
sparingly and intentionally — notebooks 01 and 11 spotlight it
explicitly as an alternative to `con.sql(...).df()`; most other cells
use the plain DuckDB API on purpose, since it's what transfers to
non-marimo Python code.

Any file the course writes out for demonstration purposes (notebook 11)
must go to a temp directory (`tempfile.mkdtemp()`), never into this
folder — re-running a notebook should never leave stray artifacts next
to the course files.
