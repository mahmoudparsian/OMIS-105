# Week 9 — Ranking Functions: `ROW_NUMBER`, `RANK`, `DENSE_RANK`

📦 **[Download Week 9 as a ZIP](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week09-ranking-functions.zip)** — this week's lectures and review, in one file. No git needed.

A **ranking function** gives every row a number — 1st, 2nd, 3rd, … —
**without** grouping the rows away. It answers questions like "Who are
the top 2 reps in each team?" or "Which items have the second-highest
price?"

The three functions differ only in how they treat **ties**:

| Function | Sales 95, 95, 88 | Ties |
|---|---|---|
| `ROW_NUMBER()` | 1, 2, 3 | different numbers (add a tie-breaker) |
| `RANK()` | 1, 1, 3 | same rank, then a **gap** |
| `DENSE_RANK()` | 1, 1, 2 | same rank, **no gap** |

⚠️ **`ORDER BY … LIMIT n` is not a ranking tool.** `LIMIT` counts
**rows**, not values: it silently cuts tied rows, `OFFSET 1` skips a row
(not a value), and it cannot restart for each group. Both sessions show
puzzles that `LIMIT` gets wrong.

## Session 1 — `ROW_NUMBER` and `RANK`

- [`ranking_slides_1.md`](ranking_slides_1.md) — slide deck
- [`ranking_demo_1.py`](ranking_demo_1.py) — Marimo notebook on 12 sales reps
  (`data/sales_reps.csv`; ties at 95, 88 and 60): `ROW_NUMBER`, `RANK`,
  `PARTITION BY`, top N per group, and three `LIMIT` puzzles (top 4 reps,
  top rep per team, lowest sales)

## Session 2 — `DENSE_RANK` and Ranking Results

- [`ranking_slides_2.md`](ranking_slides_2.md) — slide deck
- [`ranking_demo_2.py`](ranking_demo_2.py) — Marimo notebook on a small café
  chain (`data/cafe_*.csv`): all three functions side by side, ranking
  `GROUP BY` results with a CTE, best seller per category, "second-highest"
  questions, and why `LIMIT 1 OFFSET 1` gets them wrong

## Lab and Quiz

- [`ranking_slides_3.md`](ranking_slides_3.md) — **the week's lab**: 11
  questions (Q1 is a warm-up), 30 points, on an online store (`customers`,
  `orders`, `products`, …). Q6 asks you to try `LIMIT` and explain what it
  got wrong
- [`ranking_demo_3.py`](ranking_demo_3.py) — the same lab as a Marimo
  notebook: the data is loaded for you; replace each placeholder query
- [`ranking_demo_4.py`](ranking_demo_4.py) — the lab notebook **with
  answers** and real results. Try `ranking_demo_3.py` first!
- [`quiz.md`](quiz.md) — 18 multiple-choice questions

## Files in This Folder

| File | What It Is |
|------|-----------|
| `ranking_slides_1.md`, `ranking_slides_2.md` | Slide decks — Session 1 and Session 2 |
| `ranking_slides_3.md` | The lab, with blanks to fill in |
| `ranking_demo_1.py`, `ranking_demo_2.py` | Live-demo Marimo notebooks — Session 1 and Session 2 |
| `ranking_demo_3.py` | The lab as a Marimo notebook, with blanks |
| `ranking_demo_4.py` | The lab as a Marimo notebook, **with answers** |
| `quiz.md` | Short quiz |
| `data/` | `sales_reps.csv` (Session 1), `cafe_shops.csv`, `cafe_items.csv`, `cafe_orders.csv` (Session 2), and the store CSVs for the lab |

Run the notebooks from inside this folder:

```bash
cd weekly_lectures/week09-ranking-functions
marimo edit ranking_demo_1.py
```

## Before You Start

You should be comfortable with `GROUP BY` (Week 4), subqueries in `FROM`
and CTEs (`WITH`, Week 7), and `ORDER BY … LIMIT` (Week 1). This week
shows where `LIMIT` stops being enough.

The review notebook for this week is in
[`../../weekly_reviews/week09-ranking-functions/`](../../weekly_reviews/week09-ranking-functions/).

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
