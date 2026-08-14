# 🍿 Netflix Titles

**OMIS-105 · Week 4 — SQL Aggregation**

Every title in Netflix's catalogue — 8,809 movies and TV shows with country, cast,
rating, date added and duration. A dataset students already have opinions about,
which makes the questions land.

---

## Run it

```bash
marimo edit 01_build_netflix_db.py    # build netflix.duckdb — run first
marimo edit 02_netflix_analysis.py    # the analysis
```

| File | Role |
|---|---|
| `01_build_netflix_db.py` | Loads the CSV, renames columns to `snake_case`, builds the database |
| `02_netflix_analysis.py` | The analysis notebook |
| `plots_02.py`, `util_plot.py` | Chart functions |
| `netflix_titles.csv` | **8,809 titles** |
| `netflix.duckdb` | Built by notebook 1 |
| `kaggle_notebooks/` | Reference notebooks from Kaggle |
| `CLAUDE.md`, `what_to_do.txt` | Build notes (provenance) |

**Run notebook 1 first.**

---

## What it covers

| § | Section | Techniques |
|---|---|---|
| 1 | Add derived columns | Parsing `date_added`, splitting duration |
| 2 | **Simple queries** — movies vs TV, top countries, titles per year, pre-2000 titles | `GROUP BY`, `COUNT`, `ORDER BY` |
| 3+ | Deeper aggregation | `HAVING`, multi-column grouping |

---

## Why the cleaning step matters

Notebook 1 does something worth pausing on: it **renames every column to
`snake_case`** and parses `date_added` from text into a real date.

Before that step, `date_added` is a string like `"September 9, 2019"`. To the database
that is just text that happens to look like a date, so:

- You **cannot sort it chronologically** — it sorts alphabetically, putting April
  before January.
- You **cannot extract the year**.
- You **cannot group by month**.

**A column's type determines what questions you can ask of it.** That is the whole
lesson, and it shows up again in Week 4 the moment someone tries to group by year.

---

## Good questions for this dataset

- Movies or TV shows — which does Netflix have more of, and has that changed?
- Which countries produce the most titles? (`country` needs care — some titles list
  several, which is a multi-valued column and a Week 6 normalization discussion.)
- Titles added per year: the shape tells you when Netflix's catalogue grew fastest.
- Ratings distribution — is this catalogue aimed at adults or families?

---

## Two cautions

**`country` holds multiple values in one field**, comma-separated.

- Grouping by it naively treats `"United States, Canada"` as a country of its own.
- So the counts will be wrong, and wrong in a way that looks plausible.
- The correct fix is a **junction table** — exactly what Week 6 covers.

**`netflix.duckdb.wal` may be present.** That is DuckDB's write-ahead log. If the
database behaves oddly, close every connection and delete both `.duckdb` and `.wal`,
then re-run notebook 1.
