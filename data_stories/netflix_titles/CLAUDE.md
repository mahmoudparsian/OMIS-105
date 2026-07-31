# Netflix Titles — DuckDB + Marimo Project

## Project Overview

Exploratory data analysis of the Netflix Movies & TV Shows dataset using
**DuckDB** as the query engine and **Marimo** as the reactive notebook framework.

- Dataset: `netflix_titles.csv` (8 809 rows, 12 columns)
- Source: [Kaggle — Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

---

## Directory Layout

```
netflix_titles/
├── netflix_titles.csv          # Raw data (source of truth)
├── netflix.duckdb              # Persistent DuckDB file (created by notebook 1)
│
├── 01_build_netflix_db.py      # Notebook 1 — build DB, verify schema, basic queries
├── 02_netflix_analysis.py      # Notebook 2 — derived columns + 20 SQL queries
├── util_plot.py                # Fallback matplotlib plotting (used when altair absent)
│
├── kaggle_notebooks/           # Reference Kaggle notebooks (pandas/plotly baseline)
│   ├── netflix-data-visualization.ipynb
│   ├── netflix-shows-and-movies-exploratory-analysis.ipynb
│   └── netflix-visualizations-recommendation-eda.ipynb
│
└── CLAUDE.md                   # This file
```

---

## How to Run

### Prerequisites

```bash
pip install marimo duckdb altair
# altair is optional; util_plot.py (matplotlib) is the fallback
```

### Step 1 — Build the database

```bash
marimo run 01_build_netflix_db.py
# or open interactively:
marimo edit 01_build_netflix_db.py
```

This creates `netflix.duckdb` in the same directory.

### Step 2 — Run the analysis

```bash
marimo run 02_netflix_analysis.py
# or:
marimo edit 02_netflix_analysis.py
```

---

## Notebook 1 — `01_build_netflix_db.py`

**Purpose:** One-time setup. Load CSV → DuckDB → verify.

| Cell | What it does |
|---|---|
| Connect | Opens / creates `netflix.duckdb` |
| snake_case check | Converts any column name to `lowercase_with_underscores` |
| CREATE TABLE | Loads `netflix_titles.csv` into DuckDB with clean column names |
| Schema verify | Shows column names + data types via `information_schema` |
| Q1 LIMIT 10 | Eyeball check — first 10 rows |
| Q2 COUNT(*) | Total row count (expected: 8 809) |
| Q3 type counts | Movies vs TV Shows |
| Q4 NULL counts | Data quality: which columns have missing values |
| Q5 ratings | All distinct maturity ratings |

### Column Schema (snake_case — already clean in this dataset)

| Column | DuckDB type | Notes |
|---|---|---|
| `show_id` | VARCHAR | Primary key (s1, s2, …) |
| `type` | VARCHAR | "Movie" or "TV Show" |
| `title` | VARCHAR | Title of the content |
| `director` | VARCHAR | NULL for ~30 % of rows |
| `cast` | VARCHAR | Comma-separated; NULL for ~10 % |
| `country` | VARCHAR | Comma-separated; NULL for ~5 % |
| `date_added` | VARCHAR | Raw string; parsed in view |
| `release_year` | BIGINT | Year content was produced |
| `rating` | VARCHAR | Maturity rating (TV-MA, PG-13, …) |
| `duration` | VARCHAR | "90 min" or "2 Seasons" |
| `listed_in` | VARCHAR | Comma-separated genres |
| `description` | VARCHAR | Plot summary |

---

## Notebook 2 — `02_netflix_analysis.py`

**Purpose:** Deep analysis via a DuckDB view with derived columns + 20 SQL queries.

### Derived Columns (added via `CREATE VIEW netflix AS …`)

| Column | Logic |
|---|---|
| `date_added_parsed` | `TRY_CAST(TRIM(date_added) AS DATE)` |
| `year_added` | `EXTRACT(YEAR FROM date_added_parsed)` |
| `month_added` | `EXTRACT(MONTH FROM date_added_parsed)` |
| `month_name` | `STRFTIME(date_added_parsed, '%B')` |
| `duration_min` | Minutes extracted from `duration` for Movies |
| `season_count` | Season number extracted from `duration` for TV Shows |
| `first_country` | `SPLIT_PART(country, ',', 1)` — first country listed |
| `age_group` | Mapping of `rating` → Kids / Older Kids / Teens / Adults |

### Query Inventory

#### Simple (Q1–Q5)
| # | Question | Key SQL |
|---|---|---|
| Q1 | Movies vs TV Shows split | `GROUP BY type`, window `SUM … OVER ()` for % |
| Q2 | Top 10 producing countries | `GROUP BY`, `ORDER BY`, `LIMIT` |
| Q3 | Content added per year | `GROUP BY year_added` |
| Q4 | Titles released before 2000 | `WHERE release_year < 2000` |
| Q5 | Distribution by maturity rating | `GROUP BY rating, age_group` |

#### Simple+ (Q6–Q10)
| # | Question | Key SQL |
|---|---|---|
| Q6 | Longest movies | `WHERE type='Movie' ORDER BY duration_min DESC` |
| Q7 | TV Shows with most seasons | `ORDER BY season_count DESC` |
| Q8 | Content added by month | `GROUP BY month_added`, ordering by month number |
| Q9 | Countries with >100 movies AND >10 TV Shows | `HAVING` with two conditions |
| Q10 | Avg movie runtime by country | `AVG(duration_min)` + `HAVING COUNT(*) >= 20` |

#### Intermediate (Q11–Q15)
| # | Question | Key SQL |
|---|---|---|
| Q11 | Top 20 genres | `UNNEST(STRING_SPLIT(listed_in, ','))` |
| Q12 | Prolific directors: movies vs TV breakdown | Conditional `COUNT(CASE WHEN …)` |
| Q13 | Gap: release year → added to Netflix | `AVG(year_added - release_year)` |
| Q14 | Movies vs TV Shows per year (crosstab) | Pivot via conditional aggregation |
| Q15 | Most frequent cast members | `UNNEST(STRING_SPLIT(cast, ','))` |

#### Intermediate+ (Q16–Q20)
| # | Question | Key SQL |
|---|---|---|
| Q16 | Top 3 genres per content type | `WITH` + `RANK() OVER (PARTITION BY type …)` |
| Q17 | Running total of titles over time | `SUM() OVER (ORDER BY year_added)` |
| Q18 | Country rank + quartile tier | `ROW_NUMBER()`, `NTILE(4)`, `CASE NTILE …` |
| Q19 | Year-over-year growth rate | `LAG()` + arithmetic + `NULLIF` |
| Q20 | Top 3 directors per top-10 country | Multi-CTE + `DENSE_RANK() OVER (PARTITION BY …)` + `JOIN` |

---

## SQL Concepts Covered

- `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT`, `HAVING`
- `COUNT`, `AVG`, `MIN`, `MAX`, `SUM`, `ROUND`
- `CASE WHEN … END` (inline conditional)
- Conditional aggregation: `COUNT(CASE WHEN … THEN 1 END)`
- String functions: `SPLIT_PART`, `STRING_SPLIT`, `UNNEST`, `TRIM`, `REGEXP_REPLACE`, `STRFTIME`
- Type casting: `TRY_CAST`, `CAST`, `EXTRACT`
- `WITH` (Common Table Expressions / CTEs)
- Window functions: `RANK()`, `DENSE_RANK()`, `ROW_NUMBER()`, `SUM() OVER`, `LAG()`, `NTILE()`
- `PARTITION BY` for per-group computations
- `JOIN … USING` to combine CTEs
- `NULLIF` for safe division

---

## Plotting Strategy

Each query cell attempts to render a chart using **Altair** (`mo.ui.altair_chart`).
If Altair is not installed, the cell catches the `ImportError` and calls the
equivalent function from `util_plot.py` (matplotlib).

| `util_plot` function | Chart type | Used by |
|---|---|---|
| `plot_bar_simple` | Vertical bar | Q1, Q8, Q19 |
| `plot_bar_h` | Horizontal bar | Q2, Q10, Q11 |
| `plot_line` | Line + fill | Q3 |
| `plot_line_dual` | Two-series line | Q14 |
| `plot_area` | Filled area | Q17 |
| `plot_pie` | Donut pie | Q5 |

---

## Design Decisions

- **View not table** for derived columns — the base `netflix_titles` table stays
  unmodified; re-running notebook 1 never breaks notebook 2.
- **`TRY_CAST`** instead of `CAST` for date parsing — gracefully handles the
  handful of malformed date strings without crashing the view.
- **`NULLIF` for division** — prevents divide-by-zero in Q19's growth-rate formula.
- **`UNNEST(STRING_SPLIT(…))`** to explode multi-value columns (`cast`, `listed_in`)
  at query time — no denormalised tables needed.
- **Altair-first, matplotlib-fallback** plotting keeps the notebooks portable:
  they work in any environment whether or not Altair is installed.
