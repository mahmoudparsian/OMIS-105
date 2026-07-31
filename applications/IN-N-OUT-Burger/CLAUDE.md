# CLAUDE.md

Guidance for AI assistants (and humans) working in this repository.

## What this project is

A teaching application for **OMIS-105: Introduction to DBMS** (Santa Clara
University). It mimics an In-N-Out point-of-sale system to show that
**DuckDB + Streamlit** is a powerful, approachable combo for learning database
concepts. Students place real orders, watch transactions get written to a
fully **normalized** database, and explore that data through a dashboard and a
SQL playground.

The audience is intro DBMS students. Favor clarity over cleverness: readable
SQL, explicit relationships, and visible "Show SQL" panels are core to the
pedagogy.

## Files

| File | Role |
|---|---|
| `schema.sql` | The normalized schema (10 tables, sequences, PK/FK/CHECK). Source of truth for the data model. |
| `build_duckdb.py` | Creates `innout.duckdb`: applies `schema.sql`, loads the menu, generates historical orders. |
| `app.py` | The Streamlit app: POS, Dashboard, SQL Playground, Schema inspector, Stores. |
| `menu.md` | The source menu the app is built from. |
| `nl2sql_system_prompt.md` | System prompt for the Ask-Claude NL→SQL helper (edit to tune behavior). |
| `er_diagram.dot` | Graphviz DOT for the Schema-page ER diagram (edit to change the diagram). |
| `database_schema_design.md` | Long-form explanation of the schema (tables, keys, relationships, normalization). |
| `_verify.py` | Offline integrity/aggregation check for the seeder. Not part of the running app. |
| `requirements.txt` | Python deps (`streamlit>=1.40`, `duckdb>=1.1`, `pandas>=2.0`, `altair>=5.0`). |
| `.streamlit/config.toml` | Pins the app to a light theme so text stays readable. |
| `README.md` | End-user run instructions. |

## How to run

```bash
pip install -r requirements.txt
python build_duckdb.py        # (re)creates innout.duckdb — destructive, rebuilds from scratch
streamlit run app.py
```

`build_duckdb.py` deletes and rebuilds `innout.duckdb` every run, using
`RANDOM_SEED = 105` for reproducibility. Stores added through the app's UI live
only in the database file and are wiped on the next rebuild.

## Architecture notes

- **One cached DuckDB connection** (`get_con`, `@st.cache_resource`) is shared
  across reruns and used for both reads and writes. DuckDB is single-writer; do
  not open a second read-write connection to the same file in the app.
- **Reference data is cached** via `ref()` (`@st.cache_data`). After any write
  to a reference table (e.g. adding a store), call `ref.clear()` so the UI
  picks up the change, then `st.rerun()`.
- **Writes are transactional.** `place_order()` wraps its inserts in
  `BEGIN … COMMIT` with a `ROLLBACK` on error. Keep that pattern for any new
  multi-table write.
- **Surrogate keys** come from DuckDB sequences (`nextval('seq_order_id')`).
  The human-readable `transaction_id` is generated in Python as
  `INO-<store>-<YYYYMMDD>-<daily seq>`.
- **Per-store volume** is configured in `build_duckdb.py` via `STORE_ORDER_COUNTS`
  (`{1:1500, 2:2000, 3:2500}` → 6,000 orders total). `DAYS_OF_HISTORY = 365`
  spreads them across a year so monthly/cumulative charts have ~12–13 buckets.
- **Constraint demos never mutate data.** The Schema page's "Try to break it"
  panel uses `try_violation()`, which wraps the attempted INSERT in
  `BEGIN … ROLLBACK` and returns the DB's error message. Any new "show the DB
  rejecting bad data" feature must follow this always-rollback pattern.

## Conventions & gotchas

- **DuckDB reserved words.** `column`, `type`, `name`, `default` are reserved.
  When selecting from `pragma_table_info()` etc., prefer `SELECT *` and rename
  in pandas rather than aliasing to a reserved word.
- **Date/time:** use `date_part('hour', ts)` rather than the string-literal
  `extract('hour' FROM ts)` form.
- **Streamlit HTML:** the markdown sanitizer passes inline tags (`<span>`) but
  may strip block tags (`<div>`). Use native markdown (`**bold**`, `st.caption`)
  for text; reserve raw HTML for small inline styling like the price tag.
- **Charts/text color:** the app forces a light background, so always ensure
  text has an explicit dark color (handled in the global CSS + `config.toml`).
- **"Show SQL" everywhere.** When you add a chart, table, or write action, also
  surface the underlying SQL via the `show_sql()` helper (or an expander with
  `st.code(..., language="sql")`). This is a product requirement, not optional.
- **Keep it normalized.** New menu concepts should reuse the existing tables
  (items + modifiers + sizes) rather than adding denormalized columns. For
  example, "Animal Style Fries" = `French Fries` item + `Animal Style` modifier.
- **DuckDB enforces constraints.** PK, UNIQUE, CHECK, and FOREIGN KEY are all
  enforced on INSERT (needs DuckDB ≥1.1), which is what makes the constraint
  demo work. Don't assume FK enforcement is off the way it is in some engines.
- **Charts use Altair** (bundled with Streamlit) for the weekday×hour heatmap.
  Native `st.bar_chart`/`st.line_chart`/`st.area_chart` cover the rest.
- **Ask-Claude (NL→SQL)** lives in the Playground. `app.py` loads `.env`
  (`_load_dotenv()`) into named config constants near the top: `ANTHROPIC_API_KEY`,
  `ANTHROPIC_MODEL` (defaults to `claude-sonnet-4-6` if blank), and
  `NL2SQL_SYSTEM_PROMPT` (the system prompt is decoupled from
  `ask_claude_for_sql()` and can be overridden via `ANTHROPIC_SYSTEM_PROMPT`).
  `schema_context()` builds the schema string sent with each question. It's
  optional: if `anthropic` isn't installed or no key is set, the box is
  disabled with a hint. Generated SQL still goes through the read-only guard.
  Keep `.env` out of git (see `.gitignore`).
  - The fallback `.env` parser (used when `python-dotenv` isn't installed)
    strips quotes **and** inline `# comments`, so `MODEL=foo  # note` reads as
    `foo`. Prefer editing these constants over hard-coding values inline.
- **Playground editor state.** The SQL box is a single `st.session_state`
  source of truth keyed `pg_sql`; the examples dropdown and Ask-Claude both
  write to it *before* the `text_area` is instantiated (never after, or
  Streamlit errors). It's styled via a `.stTextArea textarea` rule in the
  global CSS block (monospace coding font, taller height).
- **Post-commit "actual SQL".** `place_order()` returns
  `(transaction_id, executed_sql)`; the POS page shows those literal INSERTs
  (real values, wrapped in `BEGIN … COMMIT`) full-width below the columns,
  next to the parameterized template. `sql_lit()` renders Python values as SQL
  literals for display only — never use it to actually execute.

## Verifying changes

There is no DuckDB-free way to run the full app headless, but the data model
and seeder can be checked offline:

```bash
python _verify.py     # referential integrity, unique txn ids, totals, per-store counts
python -m py_compile app.py build_duckdb.py    # syntax check
```

After schema or seeder changes, run `_verify.py` and confirm "ALL CHECKS
PASSED", then `python build_duckdb.py` and click through the app.

## App pages (in `app.py`)

1. **🧾 Point of Sale** — opens with a "Why a database?" framing callout;
   card-grid menu; combos, à-la-carte, simplified Sides, fountain sizes and
   burger customizations via popovers; writes real orders, prints a receipt,
   and shows the actual committed INSERTs (real values) alongside the template.
2. **📊 Dashboard** — KPIs and charts, each with a Show SQL expander.
3. **🧪 SQL Playground** — read-only query box (SELECT/WITH/EXPLAIN/…) with
   worked examples, plus an **Ask Claude** box that turns a plain-English
   question into DuckDB SQL (optional; needs `anthropic` + an API key).
   Results show in a **Table** tab (with CSV download) and a **Chart** tab
   (Bar / Horizontal bar / Line / Area / Pie / Scatter, configurable X/Y/color,
   Altair). The result is cached in `st.session_state.pg_result` so changing
   chart options doesn't re-run the query; the chart pickers
   (`pg_ctype/pg_x/pg_y/pg_color`) are reset on each new run. Pie slices are
   labeled with a short **% share** (computed into a `__share` column) while
   full category names live in the legend — this avoids clipping long labels
   like store names; hover shows name + value + share.
4. **🗂️ Schema** — ER diagram (Graphviz) + per-table inspector (metadata,
   constraints, sample rows) + the "Try to break it" constraint demo.
5. **🏪 Stores** — list stores with counts/revenue; add a store (one INSERT).
6. **🔄 Transactions** — step-by-step COMMIT-vs-ROLLBACK atomicity demo (a
   two-till cash transfer). Runs in a **separate in-memory DuckDB**
   (`get_demo_con`, table `demo_tills`) — fully isolated from `innout.duckdb`,
   so it cannot affect real data. `run_txn_demo()` resets to baseline each run,
   snapshots balances after each statement, and never leaves an open
   transaction.

The sidebar shows total orders and an orders-per-store breakdown (with SQL).

The Dashboard (page 2) includes two KPI rows, revenue by day, orders by hour,
top items, revenue by category/store, customizations, order-type & payment mix,
order-type mix by store, a weekday×hour Altair heatmap, cumulative revenue
(window function), best-seller-per-store (`QUALIFY`), and monthly revenue by
store. Every chart has a "Show SQL" expander.

## Future directions / roadmap

A prioritized backlog for future sessions. Items are roughly ordered by
classroom value. Keep the pedagogy principles above (readable SQL, visible
"Show SQL", stay normalized) when implementing any of these.

### Done

- [x] **Constraint demo** — "Try to break it" panel on the Schema page (FK / PK
  / CHECK / UNIQUE), via `try_violation()` with always-rollback.
- [x] **ER diagram** — Graphviz diagram + "how to read it" on the Schema page.
- [x] **"Why a database?" callout** — framing expander on the POS page.
- [x] **Transaction / ROLLBACK demo** — dedicated 🔄 Transactions page; a
  two-till cash transfer shown step by step (COMMIT vs ROLLBACK), in an
  isolated in-memory DuckDB.

### Teaching-focused (highest value)

- [ ] **EXPLAIN & indexing** — let the Playground show query plans
  (`EXPLAIN`/`EXPLAIN ANALYZE`), add an index on e.g. `orders(order_ts)`, and
  show the plan/timing change. Gentle intro to optimization.
- [ ] **Normalized-vs-flat toggle** — show the same order as joined normalized
  rows vs one wide denormalized row, to motivate *why* we normalize.
- [ ] **SQL VIEWs** — define a view (e.g. `v_order_lines`) and query it, to
  introduce views as reusable, named queries.
- [ ] **Guided SQL exercises / mini autograder** — prompts ("find each store's
  busiest hour") where a student's query result is compared to the expected
  result set. Big engagement win.

### App / data model

- [ ] **Order lookup & receipt reprint** by `transaction_id`.
- [ ] **Void / refund** an order — discuss `DELETE`, cascades, and soft-deletes
  (`is_voided` flag vs hard delete).
- [ ] **employees** table tied to `orders` (who rang it up); adds a join and a
  "sales by cashier" report.
- [ ] **customers / loyalty** table — another clean many-to-many
  (`customer_orders` or a `customer_id` FK on `orders`).
- [ ] **inventory** table + decrement on sale, to show triggers/derived state.
- [ ] **discounts / promotions** applied at the line or order level.
- [ ] **"Generate N demo orders for this store"** button on the Stores page so a
  newly opened store can be populated instantly for a demo.

### Analytics / usability

- [ ] **Dashboard filters** — date-range + store pickers that flow into every
  query.
- [ ] **Download to CSV/Excel** from Playground results and dashboard tables.
- [ ] **Growth / period-over-period** comparisons (e.g. month-over-month %).

### Polish / tech debt

- [ ] **Migrate `use_container_width`** → `width="stretch"` / `"content"`
  (deprecated by Streamlit after 2025-12-31). Currently emits warnings only.
- [ ] **Extend `_verify.py`** as new tables/relationships are added.
- [ ] Consider splitting `app.py` into per-page modules if it keeps growing.
