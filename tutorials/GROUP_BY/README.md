# GROUP BY Tutorials

Reference notes and hands-on Marimo notebooks that teach SQL's
`GROUP BY` clause with DuckDB — from a 30-second reference to a
comprehensive, 35-lesson capstone. Every SQL example follows the same
pattern: a natural-language question, the DuckDB SQL that answers it,
and a rendered result table.

Suggested order: `100` → `101` → `102` → `103`.

## Files

- **`GROUP_BY_Tutorial_100_basics.md`** — a one-page reference: a raw
  DuckDB CLI session showing what `GROUP BY` does (collapsing rows
  into one summary row per group), the `MIN`/`MAX`/`AVG`/`LISTAGG`
  aggregates, and `RANK() OVER (PARTITION BY ...)` for a top-N-per-group
  query. Read this first for the 30-second idea. Not a notebook — just
  markdown.

- **`GROUP_BY_Tutorial_101.md`** and **`GROUP_BY_Tutorial_101.py`** —
  the same beginner lesson in two formats: the `.md` is a written
  DuckDB-CLI walkthrough, the `.py` is the equivalent interactive
  Marimo notebook (with matplotlib bar charts added). Both use a small
  `scores(player, score)` table for Alex and Jane — including `NULL`
  scores — to teach `AVG`/`MIN`/`MAX`/`SUM`, `COUNT(*)` vs
  `COUNT(column)`, combining multiple aggregates, `HAVING`,
  `STRING_AGG`/`LIST`, multi-column `GROUP BY`, `WHERE` + `GROUP BY` +
  `HAVING` together, `ORDER BY` on an aggregate, and ranking scores per
  player.

- **`GROUP_BY_Tutorial_102.py`** — a 30-lesson Marimo notebook using a
  12-row `employees` table (department, job title, region, gender,
  salary). Goes from basic aggregation through `COUNT(DISTINCT ...)`,
  DuckDB's `GROUP BY ALL` shortcut, an introduction to `ROLLUP` and
  `GROUPING SETS`, a preview of `GROUP BY` vs. window functions, and a
  practice challenge with worked solutions.

- **`GROUP_BY_Tutorial_103.py`** — the comprehensive 35-lesson capstone
  notebook (plus a cheat-sheet appendix), using `employees` (20 rows)
  joined with `departments` (5 rows). Covers everything above, plus
  `GROUP BY` with `JOIN`, `CASE`, date parts, `COALESCE`, `HAVING` +
  `ORDER BY` + `LIMIT` (top-N), subqueries, CTEs, `ROLLUP`, `CUBE`,
  `GROUPING SETS`, and `GROUP BY` combined with window functions —
  ending with a full department analytics report and a `WHERE` vs
  `HAVING` decision guide.

## Requirements

```bash
pip install marimo duckdb pandas matplotlib
```

`matplotlib` is only needed for `GROUP_BY_Tutorial_101.py`, which adds
bar charts to a few lessons.

## How to run

```bash
marimo edit GROUP_BY_Tutorial_101.py
# or
marimo edit GROUP_BY_Tutorial_102.py
# or
marimo edit GROUP_BY_Tutorial_103.py
```

The two `.md` files (`100_basics` and `101`) are meant to be read
directly — they are DuckDB CLI transcripts, not notebooks.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
