# 🚗 Auto Insurance Customers

**OMIS-105 · Week 9 — Project Integration**

Nine thousand insurance customers across **24 columns** — lifetime value, coverage,
claims, channel, vehicle class and more. The larger and messier of the two insurance
stories, and the one that needs a genuine **data-cleaning pass** before any question
can be asked.

---

## Run it

```bash
marimo edit 01_data_cleaning_and_db_creation_marimo.py   # clean + build — run first
marimo edit 02_sql_queries_marimo.py                     # the analysis
```

| File | Role |
|---|---|
| `01_data_cleaning_and_db_creation_marimo.py` | **Cleaning and database creation** |
| `02_sql_queries_marimo.py` | The analysis notebook |
| `util_plot.py` | Chart functions |
| `auto_insurance.csv` | **9,134 customers, 24 columns** |
| `auto_insurance_db.duckdb` | Built by notebook 1 |
| `CLAUDE.md`, `what-to-do.txt` | Build notes (provenance) |

**Run notebook 1 first.**

---

## Why notebook 1 exists

The raw CSV has column names like `Customer Lifetime Value`, `Effective To Date`,
`EmploymentStatus` and `Location Code` — spaces, inconsistent casing, and dates stored
as text.

None of that can be queried comfortably:

- `SELECT Customer Lifetime Value` is a **syntax error** — the spaces break it.
- You would need `SELECT "Customer Lifetime Value"`, with quotes, **every single
  time**.
- Dates stored as text cannot be sorted chronologically or grouped by year.

So notebook 1 fixes the names and the types **before** any analysis happens.

**That separation is the lesson.** Cleaning is its own step, it happens once, and
everything downstream depends on it being right. It is the same discipline as
`netflix_titles/`, at larger scale.

---

## What it covers

| § | Section |
|---|---|
| 3.0 | Add derived columns — e.g. claim-to-premium ratio |
| 3.1 | **Simple queries** — top customers by lifetime value, customers in Oregon, distinct vehicle classes |
| 3.2+ | Aggregation and ranking across coverage, channel and region |

Sample questions from the notebook:

- Top 10 customers by lifetime value
- Customers in Oregon with premium > $10
- Customers with **zero income who responded to a campaign**
- Customers with a high claim-to-premium ratio

Those last two are real business questions — the kind an analyst is actually asked,
rather than an exercise invented to use a keyword.

---

## Scope

The notebook uses **CTEs, window functions and 8 ranking calls**, which the 10-week
core does not teach (see the outline's optional Advanced SQL appendix).

Use §1 (cleaning) and §3.1 (simple queries) freely. Treat the ranking sections as
demonstration unless you have taught the techniques.

---

## The pair of insurance stories

| Story | Rows | Columns | Use it for |
|---|---|---|---|
| `insurance_dataset/` | 1,773 | 7 | Clean data, clear signal, gentle ramp |
| **`auto_insurance/`** ← this one | 9,134 | 24 | Messy data, real cleaning, business questions |

Assign `insurance_dataset/` first.
