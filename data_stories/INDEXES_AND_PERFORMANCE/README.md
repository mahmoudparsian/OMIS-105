# ⚡ Indexes & Query Performance

**OMIS-105 · Week 7 — Query Performance**

A hands-on DuckDB notebook that follows the Week 7 lab exactly — create a table,
query it, create an index, query it again — and then answers the question the lab
leaves open: **why didn't it get much faster?**

---

## Why this story exists

The Week 7 teaching notes flag a recurring problem:

> *Common issue: Students expect visible speed difference on small data.*

This notebook confronts that directly. It reproduces the disappointing result on
purpose, then scales the same experiment up to 2,000,000 rows and shows that even
there the index only buys about **1.6×** — nothing like the hundred-fold difference
textbooks describe.

The explanation is the real content: **DuckDB is a columnar database**, and it is
already very good at the thing an index is supposed to rescue you from.

---

## Run it

```bash
marimo edit indexes_and_performance_marimo.py    # interactive
marimo run  indexes_and_performance_marimo.py    # read-only, for students
python      indexes_and_performance_marimo.py    # smoke test
```

A few practical notes:

- **No data files and no setup.** Every table is generated with `range()`.
- **The database is in-memory,** so nothing is written to disk and you can re-run the
  notebook as often as you like.
- **It takes about 20 seconds**, most of that building the 2,000,000-row table.

| File | Role |
|---|---|
| `indexes_and_performance_marimo.py` | The notebook — 10 sections |
| `perf_plot_util.py` | `display_table`, `time_query`, and the three charts |

---

## What it covers

| § | Section | Point |
|---|---|---|
| 1 | Build a small table | The lab's starting point, 1,000 rows |
| 2 | Time it without an index | How to measure honestly: warm-up run, median not mean |
| 3 | `CREATE INDEX`, measure again | **1.02× — no gain.** The expected disappointment |
| 4 | Scale to 2,000,000 rows | The same experiment at four sizes, charted |
| 5 | Why the gain is small | Columnar storage, zone maps, vectorised scans |
| 6 | `EXPLAIN` / `EXPLAIN ANALYZE` | Reading the plan instead of guessing |
| 7 | What *does* help | Projection pushdown; filtering an ordered column |
| 8 | When an index *is* worth it | Selective text lookup — the 4× case |
| 9 | The costs nobody mentions | Disk, slower writes, maintenance |
| 10 | Summary + 5 exercises | Including the lab's own challenge question |

---

## Measured results

These are the numbers the notebook produces on a typical laptop. Yours will differ
in absolute terms; the **shape** is what matters.

| Rows | No index | With index | Speedup |
|---|---|---|---|
| 1,000 | 0.073 ms | 0.072 ms | **1.02×** |
| 10,000 | 0.076 ms | 0.070 ms | 1.09× |
| 100,000 | 0.103 ms | 0.069 ms | 1.49× |
| 500,000 | 0.175 ms | 0.102 ms | 1.72× |
| 2,000,000 | 0.322 ms | 0.197 ms | 1.64× |

And the cases that beat it:

| Change | Speedup |
|---|---|
| Index on a **text** column, 1M rows | **4.1×** |
| `SELECT` 2 columns instead of `SELECT *` | **2.1×** |
| Filter an **ordered** column (zone maps) | **1.5×** |

> **Two of the three biggest wins involve no index at all.** That is the lesson.

---

## The three reasons an index does less here

1. **Column pruning** — DuckDB stores each column separately, so filtering on
   `price` reads only `price`. A row-store must walk over every other column too.
2. **Zone maps** — DuckDB records the min and max of each block of rows and skips
   blocks that cannot contain your value. That is most of an index's benefit, for
   free, with no `CREATE INDEX`.
3. **Vectorised execution** — comparisons run in batches of ~2,048 values across
   multiple cores. A "full scan" is nothing like reading rows one at a time.

---

## A note on `EXPLAIN`

The notebook shows DuckDB reporting `SEQ_SCAN` **even when a usable index exists**.
That is not a bug, and not a mistake in the notebook:

- DuckDB uses an index scan **only** when it estimates the result is a tiny slice of
  the table.
- The rest of the time it decides its own scan is faster — and it is usually right.
- So **the optimiser is allowed to ignore the index you created.**

The takeaway for students: you cannot tell whether an index is being used by looking
at your SQL. You have to check the plan, and then measure.

---

## Teaching suggestions

- **Run sections 1–3 live, and let the disappointment land** before explaining it.
  The moment students see `1.02×` is the moment they are ready to hear why.
- **Ask before revealing section 5**: "the index exists, the filter matches one row,
  so why is it not faster?" Most guesses will be about the index being wrong. The
  real answer is that the scan was never slow.
- **Exercise 5 is the lab's own challenge question** — explain the result without
  using the words "index" or "scan". It is a good exit ticket.
- If your class also uses PostgreSQL or MySQL, running the same experiment there
  makes an excellent contrast: the identical query, the identical index, a wildly
  different result.
