# 📈 Sales Data Exploration — a Five-Table CRM

**OMIS-105 · Week 5 — SQL Joins**

A B2B sales database: **five related tables, 6,912 orders, 9,073 web events**. Where
`FK_JOINS/` teaches joins on eight rows, this one makes you use them on data big
enough that the join is doing real work.

Ships with an **ERD diagram** — the only story here that does.

---

## Run it

```bash
marimo edit sales_data_exploration_marimo.py
```

| File | Role |
|---|---|
| `sales_data_exploration_marimo.py` | The notebook |
| `display_utils.py` | Display helpers |
| `ERD.png` | **Entity-relationship diagram — open this first** |
| `sql_schema.sql` | Full schema plus data as `INSERT` statements |
| `sales-data-exploration.sql` | The query set |
| `sales-analysis.md` | Written analysis |
| `data/*.csv` | Five CSV files |

---

## The schema

```
   region                sales_reps              accounts             orders
┌────────────┐        ┌──────────────┐       ┌──────────────┐    ┌───────────────┐
│ id      PK │◄──FK───│ region_id FK │◄──FK──│ sales_rep_id │◄FK─│ account_id FK │
│ name       │        │ id        PK │       │ id        PK │    │ id         PK │
└────────────┘        │ name         │       │ name, website│    │ occurred_at   │
                      └──────────────┘       └──────┬───────┘    │ standard_qty  │
                                                    │            │ gloss_qty …   │
                                                    │ FK         └───────────────┘
                                             ┌──────▼────────┐
                                             │ web_events    │
                                             │ account_id FK │
                                             │ occurred_at   │
                                             │ channel       │
                                             └───────────────┘
```

| Table | Rows | Meaning |
|---|---|---|
| `region` | 4 | Sales regions |
| `sales_reps` | 50 | Reps, each in one region |
| `accounts` | 351 | Customer accounts, each owned by one rep |
| `orders` | 6,912 | Orders placed by accounts |
| `web_events` | 9,073 | Site visits by accounts, with channel |

---

## Why it is a good joins story

**1 · The chain is four tables deep.**

- *"What is total revenue by region?"* needs `orders → accounts → sales_reps → region`.
- There is **no shortcut** — two intermediate tables sit between the number and the
  grouping.
- That is exactly how a real CRM is shaped.

**2 · Two fact tables share one dimension.**

- Both `orders` and `web_events` hang off `accounts`.
- So you can ask: **does web activity predict orders?**
- Answering it means joining an account's events to that account's orders — a genuinely
  interesting question, not an invented exercise.

**3 · The row counts are lopsided.**

- 4 regions at one end, 9,073 web events at the other.
- Joining from the small side and from the large side produce very
  different-looking results from the same data.

---

## Teaching notes

- **Project `ERD.png` before writing any SQL.** Five tables is where students stop
  being able to hold the schema in their heads, and a diagram fixes that instantly.
  It is also a good moment to say that professionals draw these before they build.
- Good progression: one join (orders → accounts), then two (→ sales_reps), then three
  (→ region). Ask for the revenue-by-region number after each step and let them see
  it only becomes answerable at the end.
- `sql_schema.sql` starts with `BEGIN TRANSACTION;` — a natural forward reference to
  Week 8, and a chance to mention that bulk loads are wrapped in transactions so a
  failure halfway through leaves nothing behind.
