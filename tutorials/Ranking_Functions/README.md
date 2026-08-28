# DuckDB Ranking Functions Tutorial

Three Marimo notebooks that teach SQL ranking functions —
`ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` — plus, in the advanced
notebook, `NTILE()`, `LAG()`, `LEAD()`, `PERCENT_RANK()`, and
`WITH`-based CTEs. All three run against DuckDB with a 1,000-row
employees dataset, and every SQL result renders as a styled,
high-quality table (no raw DataFrame dumps).

Pick the notebook that matches how you want to teach or learn:

| Notebook | Level | Style | Dataset |
|---|---|---|---|
| `ranking_functions_01_basics_standalone.py` | Basics (20 lessons) | Self-contained in one file — its own inline `show()` helper, no `helpers/` needed | `data/employees_1000.csv` |
| `ranking_functions_02_basics_modular.py` | Basics (20 lessons) | Same curriculum as above, refactored so rendering and plotting code live in `helpers/` — the notebook itself stays focused on SQL | `data/employees_1000.csv` |
| `ranking_functions_03_advanced.py` | Advanced (20 lessons) | Self-contained; adds subquery/CTE warm-up and window functions beyond basic ranking | `data/employees.csv` |

Suggested order: work through `01` first, then `02` to see the same
lessons organized with reusable helper modules, then `03` for the
advanced material.

## Files

- `ranking_functions_01_basics_standalone.py` — 20-cell notebook covering `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, and `PARTITION BY`/`WITH` patterns, in a single self-contained file (its own inline `show()` helper, no charts)
- `ranking_functions_02_basics_modular.py` — the same 20-lesson basics curriculum, refactored to import `helpers/rendering.py` for table display and `helpers/plots.py` for charts
- `ranking_functions_03_advanced.py` — 20-cell notebook that starts with subqueries and CTEs, then covers all three basic ranking functions plus `NTILE()`, `LAG()`, `LEAD()`, `PERCENT_RANK()`, running totals, and a composite leaderboard
- `data_generator.py` — Faker-based script that generated `data/employees_1000.csv`
- `data/employees_1000.csv` — 1,000-row employee dataset used by the two basics notebooks
- `data/employees.csv` — 1,000-row employee dataset used by the advanced notebook (same schema, independently generated)
- `helpers/rendering.py` — styled `show()` helper (dark navy headers, alternating rows, hover highlight, row counts) used by `ranking_functions_02_basics_modular.py`
- `helpers/plots.py` — matplotlib helper functions (salary by degree, top departments, rank curve, top-N per department) used by `ranking_functions_02_basics_modular.py`

## Dataset schema

```
emp_id,      -- 1, 2, 3, ...
emp_name,    -- full name
dept_id,     -- SALES, BUSINESS, AI, MARKETING, SOFTWARE, HARDWARE
country,     -- USA, CANADA, GERMANY, CHINA, INDIA
gender,      -- MALE, FEMALE
salary,      -- integer, 80,000–280,000
degree,      -- BA, BS, MS, MSIS, PHD
performance, -- yearly performance score, 1–10
hire_date    -- date of hire, spans 3 years
```

Department counts: SALES 100 · BUSINESS 50 · AI 150 · MARKETING 50 ·
SOFTWARE 400 · HARDWARE 250

Country counts: USA 600 · CANADA 200 · GERMANY 100 · CHINA 50 · INDIA 50

PhD salaries range from $200,000 to $280,000, so ranking examples have
realistic spread and ties.

## Requirements

```bash
pip install marimo duckdb pandas matplotlib faker
```

## How to run

```bash
marimo edit ranking_functions_01_basics_standalone.py
# or
marimo edit ranking_functions_02_basics_modular.py
# or
marimo edit ranking_functions_03_advanced.py
```

Run from inside the `Ranking_Functions/` folder so the relative
`data/...csv` paths resolve correctly.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
