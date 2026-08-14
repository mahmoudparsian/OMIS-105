# 🏥 Health Insurance Charges

**OMIS-105 · Week 9 — Project Integration** *(the query tiers also serve Weeks 3–4)*

A small, clean, seven-column dataset about what drives medical insurance costs. The
**gentlest of the two insurance stories** — start here before `auto_insurance/`.

---

## Run it

```bash
marimo edit 01_build_database_marimo.py           # build insurance_db.duckdb — run first
marimo edit 02_sql_queries_tutorial_marimo.py     # the tutorial
```

| File | Role |
|---|---|
| `01_build_database_marimo.py` | Reads the CSV, builds the database |
| `02_sql_queries_tutorial_marimo.py` | The query tutorial |
| `util_plot.py` | Chart functions |
| `insurance.csv` | **1,773 policyholders** |
| `insurance_db.duckdb` | Built by notebook 1 |
| `build_nb1.py`, `build_nb2.py` | Generator scripts — not the notebooks |
| `CLAUDE.md`, `what-to-do.txt` | Build notes (provenance) |

**Run notebook 1 first.**

---

## The data

Seven columns, no missing values, no cleaning required:

```
age, gender, bmi, children, smoker, region, charges
```

That simplicity is the point. Nothing here distracts from the SQL, and every column
is something a student already understands without a domain briefing.

---

## What it covers

The tutorial is numbered question by question, from trivial to analytical:

| Q | Question | Technique |
|---|---|---|
| 1 | How many rows? | `COUNT(*)` |
| 2 | Ten most expensive charges | `ORDER BY`, `LIMIT` |
| 3 | Smokers vs non-smokers | `GROUP BY` |
| 4 | Distinct regions | `DISTINCT` |
| 5 | Charges over $40,000 | `WHERE` |
| 6 | Average charges by region | `GROUP BY` + `AVG` |
| … | Progressively harder | `HAVING`, CTEs |

---

## The finding students will remember

**Smoking dominates everything.** Group charges by `smoker` and the gap is enormous —
far larger than the gap by age, region or number of children.

Why that makes it a good teaching dataset:

- **The strongest signal is the one students expect.** When the result matches
  intuition, they trust that their SQL is correct.
- **Then you can ask something harder:** *does BMI matter more for smokers than for
  non-smokers?*
- That second question needs a **two-column `GROUP BY`**, and its answer is not
  obvious in advance.

---

## The pair of insurance stories

| Story | Rows | Columns | Use it for |
|---|---|---|---|
| **`insurance_dataset/`** ← this one | 1,773 | 7 | Clean data, clear signal, gentle ramp |
| `auto_insurance/` | 9,134 | 24 | Messy data needing a real cleaning pass |

Start here. Move to `auto_insurance/` when students are ready for data that fights
back.
