# 🍔 In-N-Out POS + Analytics — DuckDB & Streamlit

A teaching application for **OMIS-105: Introduction to DBMS** (Santa Clara
University). It looks and behaves like a real point-of-sale system: students
build an order, place it, and watch a real transaction get written into a
fully **normalized** relational database. A live dashboard then queries that
same database — so students see, end to end, how an operational system and an
analytics system share one data model.

## What's inside

| File | Purpose |
|------|---------|
| `schema.sql` | The fully normalized schema (10 tables, PK/FK relationships). |
| `build_db.py` | Creates `innout.duckdb`, loads the menu, generates ~1,500 demo orders. |
| `app.py` | The Streamlit app: POS, dashboard, SQL playground, schema browser. |
| `menu.md` | The source menu the app is built from. |
| `_verify.py` | Offline integrity/aggregation check for the seeder (optional). |

## Run it

```bash
pip install -r requirements.txt
python build_db.py          # one-time: builds innout.duckdb with demo data
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).
If you skip `python build_db.py`, the app offers a **Build database** button on
first launch.

## The four screens

1. **🧾 Point of Sale** — Pick combos or à-la-carte items, choose drink sizes,
   add "Not So Secret Menu" customizations (Animal Style, Protein Style, extra
   patties…), and place the order. Each order is written atomically across
   three tables and gets a human-readable `transaction_id`
   (e.g. `INO-01-20260618-00042`).
2. **📊 Dashboard** — KPIs and charts (revenue by day, orders by hour, top
   items, revenue by category/store, popular modifiers, recent transactions),
   each with a **🔍 Show SQL** expander revealing the exact query.
3. **🧪 SQL Playground** — A read-only query box with worked examples
   (window functions, `QUALIFY`, anti-joins, `GROUP BY ALL`) so students can
   experiment against live data.
4. **🗂️ Schema** — Row counts, table inspector, and the relationship map.

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

Key concepts it demonstrates: surrogate vs. business keys
(`order_id` vs. `transaction_id`), one-to-many relationships, the
many-to-many **bridge** pattern (`item_prices`, `order_item_modifiers`),
a `CHECK` constraint (a line is an item *or* a combo), and how the same
normalized tables serve both transactions (POS) and analytics (dashboard).

## Notes

- Default sales tax is 9.25% (Santa Clara County); change `TAX_RATE` in
  `build_db.py` / `app.py` if needed.
- Re-running `python build_db.py` rebuilds the database from scratch with the
  same seed (`RANDOM_SEED = 105`), so demos are reproducible.
- Combo lines intentionally carry a `combo_id` and no `item_id`; the
  "Revenue by category" chart excludes them, which is a nice prompt for a
  classroom discussion about modeling trade-offs.
