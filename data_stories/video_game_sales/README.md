# 🎮 Video Game Sales

**OMIS-105 · Week 4 — SQL Aggregation**

Sixteen thousand games with sales broken out by region. A natural fit for Week 4
because almost every interesting question here is a `GROUP BY`: by platform, by
genre, by publisher, by year.

---

## Run it

```bash
marimo edit 01_build_database_marimo.py    # build sales_db.duckdb — run first
marimo edit 02_sql_queries_marimo.py       # the analysis
```

| File | Role |
|---|---|
| `01_build_database_marimo.py` | Loads the CSVs and builds the database |
| `02_sql_queries_marimo.py` | The query notebook |
| `util_plot.py` | Chart functions |
| `video_game_sales.csv` | **16,598 games** |
| `video-games-developers.csv` | 686 developers |
| `sales_db.duckdb` | Built by notebook 1 |
| `video_game_sales_profile.html` | An automated data profile — open it in a browser |
| `metadata.txt`, `CLAUDE.md`, `what-to-do.txt` | Notes (provenance) |

**Run notebook 1 first.**

---

## The data

One row per game, with sales split by region:

```
rank, name, platform, year, genre, publisher,
na_sales, eu_sales, jp_sales, other_sales, global_sales
```

Those four regional columns are what make the dataset worth using:

- **The same game sells very differently in different places.**
- That is a real finding students can **discover** with one `GROUP BY`, rather than
  being told it.

---

## What it covers

| § | Section | Techniques |
|---|---|---|
| 3.0 | Add derived columns | Computed values |
| 3.1 | Five **simple** queries — best-sellers, dataset overview, games from 1985 | `SELECT`, `ORDER BY`, `WHERE` |
| 3.2+ | Aggregation | `GROUP BY` platform / genre / publisher, `HAVING` |

---

## Questions worth asking of it

- Which genre sells best **in Japan** but not in North America? (The answer is
  genuinely surprising, and it is one `GROUP BY` away.)
- Which publisher has the most games, and is that the same as the publisher with the
  most *sales*? (Volume and success are different measures — a recurring theme.)
- Plot games per year. There is a rise and a fall, and the fall says more about when
  the dataset was collected than about the games industry.

---

## A caution about the data

Two things to tell students before they draw conclusions:

- **The data stops in the mid-2010s** and undercounts digital-only sales. It is a
  snapshot of the retail era, not a picture of the industry today.
- **So every claim should say "in this dataset"**, not "in the world". That habit is
  worth enforcing from the first week.

There is also a ready-made data profile:

- `video_game_sales_profile.html` lists column types, missing values and
  distributions for the raw CSV.
- **Open it in a browser before writing any SQL.** Looking at what you have before
  querying it is a good model of how to approach unfamiliar data.
