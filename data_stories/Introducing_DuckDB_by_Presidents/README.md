# 🦆 Introducing DuckDB — by U.S. Presidents

**OMIS-105 · Week 1 — Database Foundations** *(tool tour; parts reach well beyond Week 1)*

A guided tour of **DuckDB as a tool**, using a small, genuinely interesting dataset:
every U.S. president, their party, and their term dates. Eleven sections take you
from installation to running SQL directly against pandas DataFrames.

---

## Run it

```bash
marimo edit duckdb_intro_marimo.py    # interactive
marimo run  duckdb_intro_marimo.py    # read-only
```

| File | Role |
|---|---|
| `duckdb_intro_marimo.py` | The notebook — 11 sections |
| `plots.py` | Five chart functions, kept out of the notebook |
| `data/presidents.csv` | 1 row per president: sequence, name, term dates, party_id |
| `data/parties.csv` | Lookup table: party_id → party_name |
| `presidents.duckdb` | Built by the notebook |
| `presidential_terms_by_century.md` | Worked analysis write-up |
| `longest_serving_president_by_party.md` | Worked analysis write-up |

---

## What it covers

| § | Topic |
|---|---|
| 0 | What DuckDB is, and why it is not like MySQL |
| 1–2 | Installation and a sanity check |
| 3 | Open a connection, load both CSVs into tables |
| 4 | SQL queries against the data |
| 5 | The **relational Python API** — the same query without writing SQL |
| 6 | Concurrency — what DuckDB does and does not allow |
| 7 | **Custom Python UDFs** — calling your own Python from inside SQL |
| 8 | pandas and Polars integration |
| 9 | Visualisations (via `plots.py`) |
| 10 | Querying a DataFrame directly, with no table at all |

---

## The data

Two tables, linked by `party_id`:

- `presidents.party_id` points at `parties.party_id`.
- That link is a **foreign key** — the thing Week 2 covers formally.
- Here it appears quietly, without the terminology, which is a gentle first exposure.

```
parties                        presidents
┌──────────────────┐          ┌────────────────────────────┐
│ party_id         │◄─────────│ party_id                   │
│ party_name       │          │ sequence, last_name,       │
└──────────────────┘          │ first_name, term_start,    │
                              │ term_end                   │
                              └────────────────────────────┘
```

---

## A note on scope

**This story is broader than Week 1 SQL.** How to split it:

- **§0–4 — use these in Week 1.** Installing DuckDB, connecting, loading CSVs, and a
  first look at SQL. This is the "what is this tool" tour.
- **§5–10 — save these for later.** They cover the Python API, user-defined
  functions, concurrency, and pandas/Polars integration. All useful, none of it part
  of the SQL syllabus.
- Good uses for §5–10: students who ask what else DuckDB can do, or a revisit in
  Week 10 alongside the modern-data discussion.

---

## Teaching notes

- The presidents dataset works well because **students can check the answers**. If a
  query claims Franklin D. Roosevelt served longest, that is verifiable without
  trusting the database.
- §6 (concurrency) pairs naturally with the Week 8 transactions story — it explains
  why DuckDB allows one writer, which is the constraint `TRANSACTIONS_AND_ACID/`
  works within.
- The two `.md` write-ups are good models for how you want student analysis
  submitted: a question, the SQL, the result, and a sentence saying what it means.
