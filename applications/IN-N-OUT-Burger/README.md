# 🍔 In-N-Out POS + Analytics — DuckDB & Streamlit

A teaching application for **OMIS-105: Introduction to DBMS** (Santa Clara
University). It looks and behaves like a real point-of-sale system: students
build an order, place it, and watch a real transaction get written into a
fully **normalized** relational database. A live dashboard, a SQL playground,
and lookup/search screens then query that same database — so students see, end
to end, how one data model powers both an operational system and analytics,
and how SQL is used to build a real application.

The logo and food art are original SVGs (not the trademarked In-N-Out logo).

## What's inside — every file in this folder

**Application code**

| File | Purpose |
|------|---------|
| `app.py` | The entire Streamlit application — all 8 pages/tabs, styling, and the DB helpers. Start here. |
| `build_duckdb.py` | Builds `innout.duckdb` from scratch: applies `schema.sql`, loads the menu reference data, generates 6,000 demo orders, and voids ~1.5% of them. Uses `RANDOM_SEED = 105` for reproducibility. |
| `_verify.py` | Offline sanity check for the seeder (no DuckDB needed): referential integrity, unique transaction IDs, money arithmetic, per-store counts. Not part of the running app. |

**Data model & content**

| File | Purpose |
|------|---------|
| `schema.sql` | The fully normalized schema — 10 tables with PK / FK / CHECK constraints and sequences. The source of truth for the data model. |
| `menu.md` | The In-N-Out menu the app is built from (items, prices, sizes, secret-menu customizations). |
| `er_diagram.dot` | Graphviz DOT source for the entity-relationship diagram shown on the Schema page. Edit this to change the diagram. |
| `nl2sql_system_prompt.md` | The system prompt for the optional “Ask Claude” natural-language→SQL helper. Edit to tune its behavior. |

**Documentation**

| File | Purpose |
|------|---------|
| `README.md` | This file — overview, how to run, and the tour of all screens. |
| `database_schema_design.md` | Long-form explanation of the schema: every table, keys, relationships, normalization, and the soft-delete design. |
| `CLAUDE.md` | Guidance for AI assistants (and humans) working in the repo — architecture notes, conventions, gotchas, and the roadmap. |

**Configuration**

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies (`streamlit`, `duckdb`, `pandas`, `altair`, plus optional `anthropic` / `python-dotenv`). |
| `.streamlit/config.toml` | Pins the app to a light theme so text is always dark-on-light and readable. |
| `.gitignore` | Keeps secrets (`.env`) and the generated database out of version control. |
| `.env.example` | Template for the optional Ask-Claude keys — copy to `.env` and fill in your Anthropic API key. |
| `.env` | Your local secrets (`ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`). Loaded automatically; **not** committed. Optional. (A personal variant like `.env.mp` may also exist locally — keep any file containing a real key out of git.) |

**Convenience scripts**

| File | Purpose |
|------|---------|
| `build_duckdb.sh` | One-liner wrapper: deletes the old DB and runs `python3 build_duckdb.py`. |
| `run_app.sh` | One-liner wrapper: runs `streamlit run app.py`. |

**Brand art (`assets/`)**

| File | Purpose |
|------|---------|
| `assets/logo.svg` | Original burger wordmark logo shown in the sidebar (not the trademarked In-N-Out logo). |
| `assets/logo_icon.svg` | Square icon version of the logo (used when the sidebar is collapsed). |
| `assets/hero.svg` | The banner illustration at the top of the Point of Sale screen. |

**Generated (not committed)**

| File | Purpose |
|------|---------|
| `innout.duckdb` | The DuckDB database file created by `build_duckdb.py`. Rebuildable at any time; a `.wal` write-ahead-log file may sit next to it. |

## Run it

```bash
pip install -r requirements.txt
python build_duckdb.py      # one-time: builds innout.duckdb with demo data
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501). If you skip
`python build_duckdb.py`, the app offers a **Build database** button on first
launch. Re-running the builder rebuilds from scratch with a fixed seed
(`RANDOM_SEED = 105`), so demos are reproducible.

### Optional: the “Ask Claude” SQL helper

The SQL Playground can turn plain-English questions into DuckDB SQL. It's
optional — the rest of the app works without it. To enable, install the extra
deps (already in `requirements.txt`) and add a `.env` next to `app.py`:

```
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-4-6
```

Keep `.env` out of version control (it's already in `.gitignore`). Generated
SQL still passes through the read-only guard before it can run.

## The screens

1. **🧾 Point of Sale** — Build an order from combos or à-la-carte items, pick
   drink sizes, add “Not So Secret Menu” customizations (Animal Style, Protein
   Style, extra patties…). Placing it writes atomically across three tables and
   mints a human-readable `transaction_id` (e.g. `INO-01-20260618-00042`); the
   page prints a receipt and shows the *actual* committed `INSERT`s.
2. **🔎 Order Lookup & Refund** — Find an order by `transaction_id` and reprint
   its receipt (parameterized queries + joins). **Void / refund** an order as a
   **soft delete** (`UPDATE is_voided = TRUE`), reversible via Un-void, with a
   soft-vs-hard-delete explanation.
3. **📋 Browse Orders** — Search and filter (store, order type, payment,
   date range, `transaction_id` contains) with `LIMIT/OFFSET` pagination, built
   on a dynamic, fully parameterized `WHERE`.
4. **📊 Dashboard** — KPIs and charts (revenue over time, orders by hour, top
   items, revenue by category/store, order-type & payment mix, a weekday×hour
   heatmap, cumulative revenue via a window function, best-seller per store via
   `QUALIFY`, monthly revenue by store). Revenue excludes voided orders. Every
   chart has a **🔍 Show SQL** expander.
5. **🧪 SQL Playground** — A read-only query box with worked examples, an
   optional **Ask Claude** box, and results shown as a table (CSV download) or a
   configurable chart.
6. **🗂️ Schema** — An ER diagram, a per-table inspector (metadata, constraints,
   sample rows), and a **“Try to break it”** panel that shows the database
   rejecting FK / PK / CHECK / UNIQUE violations.
7. **🏪 Stores** — List stores with order counts/revenue and open a new store
   (a single `INSERT` that immediately becomes a register on the POS screen).
8. **🔄 Transactions** — A step-by-step **COMMIT vs ROLLBACK** atomicity demo (a
   two-till cash transfer) that runs in an isolated in-memory database.

## The data model (why it's a good teaching example)

```
menu_categories ──< menu_items ──< item_prices >── sizes
                         │  │
                         │  └──< combos
                         │
stores ──< orders ──< order_items >── sizes
                          │   ├──< order_item_modifiers >── modifiers
                          │   └── (item_id  OR  combo_id)
```

Key concepts it demonstrates: surrogate vs. business keys (`order_id` vs.
`transaction_id`); one-to-many relationships; the many-to-many **bridge**
pattern (`item_prices`, `order_item_modifiers`); a `CHECK` constraint (a line
is an item *or* a combo); **soft delete** (`is_voided`) vs. hard delete;
parameterized queries and pagination; transactions and atomicity; and how the
same normalized tables serve both transactions (POS) and analytics (dashboard).
See `database_schema_design.md` for the full write-up.

## Notes

- Default sales tax is 9.25% (Santa Clara County); change `TAX_RATE` in
  `build_duckdb.py` / `app.py` if needed.
- Per-store order volume is set in `build_duckdb.py` (`STORE_ORDER_COUNTS`,
  currently 1,500 / 2,000 / 2,500) and spread over `DAYS_OF_HISTORY = 365`.
  The seeder voids ~1.5% of orders so the soft-delete behavior is visible.
- Combo lines intentionally carry a `combo_id` and no `item_id`; “Revenue by
  category” excludes them — a nice prompt for a modeling-trade-offs discussion.
- Stores added through the app and orders you place live only in
  `innout.duckdb`; re-running `build_duckdb.py` resets everything.

## Possible future work

Ideas for future iterations, roughly ordered by classroom value. (The detailed,
living backlog lives in `CLAUDE.md`.)

**Teaching-focused**

- **`EXPLAIN` & indexing** — let the Playground show query plans, add an index
  on e.g. `orders(order_ts)`, and show the plan/timing change (intro to
  optimization).
- **Normalized-vs-flat toggle** — show the same order as joined normalized rows
  vs. one wide denormalized row, to motivate *why* we normalize.
- **SQL Views** — define a view (e.g. `v_order_lines`) and query it, introducing
  views as reusable, named queries.
- **Guided SQL exercises / mini-autograder** — prompts like "find each store's
  busiest hour" where a student's query result is checked against the expected
  answer.

**App / data model**

- **`employees`** table tied to `orders` (who rang it up) → a "sales by cashier"
  report.
- **`customers` / loyalty** table — another clean many-to-many.
- **`inventory`** table that decrements on sale (derived state / triggers).
- **discounts / promotions** applied at the line or order level.
- **"Generate N demo orders for this store"** button so a newly opened store can
  be populated instantly.

**Analytics / usability**

- **Dashboard filters** (date range + store) that flow into every query.
- **Download to CSV/Excel** from dashboard tables (the Playground already has
  it).
- **Growth / period-over-period** comparisons (e.g. month-over-month %).

**Polish / tech debt**

- Migrate the deprecated `use_container_width` to `width="stretch"`.
- Extend `_verify.py` as new tables/relationships are added.
- Consider splitting `app.py` into per-page modules if it keeps growing.

## Verifying changes (for contributors)

```bash
python _verify.py                              # integrity + aggregation checks
python -m py_compile app.py build_duckdb.py    # syntax check
```

`.streamlit/config.toml` pins a light theme so text stays readable. Requires
`streamlit>=1.40`, `duckdb>=1.1`, `pandas>=2.0`, `altair>=5.0` (plus
`anthropic` / `python-dotenv` for the optional Ask-Claude box).
