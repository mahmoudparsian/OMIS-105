# 🏆 Top 500 Movies

**OMIS-105 · Week 4 — SQL Aggregation**

A ranked list of the best films ever made — assembled by **scraping it**, filtering
it, and then querying it. The smallest dataset in the Week 4 group (452 films), and
the only one that shows where the data came from.

---

## Run it

```bash
marimo edit top_500_movies.py    # the analysis
```

| File | Role |
|---|---|
| `top_500_movies.py` | The analysis notebook |
| `web_scraping_top_500_movies.py` | **The scraper that produced the CSV** |
| `util_plot.py` | Chart functions |
| `top_500_movies_ranked.csv` | **452 films** after filtering |
| `top_500_movies.duckdb` | The database |
| `CLAUDE.md`, `what_to_do.txt` | Build notes (provenance) |

---

## What it covers

| # | Question |
|---|---|
| 1 | The ten best films overall |
| 2 | Highest IMDb ratings |
| 3 | Crowd-pleasers — audience favourites |
| 4 | The most-voted films |
| 5 | The best of the recent era |
| 6 | How many films per decade? |

Questions 1–5 are ranking and filtering; question 6 is the `GROUP BY` that makes this
a Week 4 story.

---

## Why "500" is 452

The scraper collected 500 films; the CSV holds 452. The 48 missing ones were removed
by a **filtering step with explicit rules**:

- A minimum vote threshold
- A whitelist of films that are never removed
- A check on how many volume columns fall below a cutoff

That gap is the most interesting thing in this folder:

- It is a decision analysts make constantly and **almost never write down**.
- The question is always the same: *which rows do we drop, and can we defend it?*
- Here the rules are **visible in `web_scraping_top_500_movies.py`**, not hidden in
  someone's head.

**Worth asking the class:** if a film was excluded for having too few votes, is the
resulting "top 500" still a top 500? Of what, exactly?

---

## Where the data came from

Unlike every other story here, this one includes its own acquisition step. Students
can read the scraper and see that data does not arrive as a tidy CSV — somebody
fetched pages, parsed them, made judgement calls, and wrote the file.

If your course touches on data sourcing at all, this is the cheapest way to make the
point concrete.

---

## Teaching notes

- 452 rows is small enough to skim, which makes it a good place to sanity-check a
  `GROUP BY` result against the raw data.
- The decade question (#6) is a nice integer-arithmetic exercise: `(year / 10) * 10`
  with **integer** division. In DuckDB use `//`, since `/` returns a decimal and would
  produce `199.7` instead of `1990`.
- Pairs well with `movies_database/` — this one is small and opinionated, that one is
  large and comprehensive.
