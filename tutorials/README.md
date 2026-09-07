# Tutorials

* Standalone SQL and DuckDB tutorials for OMIS 105.
* Each folder is self-contained: a Marimo notebook or Markdown walkthrough, its README,
and any data it needs.
* The **Best-Fit Week** column maps each tutorial to the
[10-week syllabus](../outline-10-weeks/Outline_OMIS_105_10_weeks.md) topic
it reinforces best. Many tutorials are useful outside that week too —
use the column as a starting point, not a hard rule.

## Directory Structure

| Folder | What It Covers | Best-Fit Week(s) |
|---|---|---|
| [`DuckDB_101/`](DuckDB_101/) | Intro slides + notebook: what DuckDB is and why it's used in this course | Week 1 — Database Foundations |
| [`DuckDB_from_Command_Line/`](DuckDB_from_Command_Line/) | Installing and using the DuckDB CLI shell — dot-commands, `.mode`, reading CSVs, script files ([slides PDF](DuckDB_from_command_line/duckdb_from_command_line.pdf)) | Week 1 — Database Foundations |
| [`DuckDB_Querying_CSV_Files/`](DuckDB_Querying_CSV_Files/) | Reading and querying CSV files directly with DuckDB | Week 1 — Database Foundations |
| [`DuckDB_SQL_Introduction/`](DuckDB_SQL_Introduction/) | First SQL queries against a weather CSV dataset | Week 1 — Database Foundations |
| [`SQL_Tutorial_Documents/`](SQL_Tutorial_Documents/) | Reference PDFs: intro to RDBMS and intro to SQL | Week 1 — background reading |
| [`marimo_introduction/`](marimo_introduction/) | Getting started with Marimo notebooks and `mo.sql()`; `101` = first SQL notebook, `102` = joins, `103` = subqueries/CTEs | Week 1 (`101`) → Week 5 (`102`, joins) → Week 9 (`103`, CTEs) |
| [`SQL_Tutorial_Notebooks/`](SQL_Tutorial_Notebooks/) | Quick-tour → fundamentals → comprehensive SQL notebook series | Week 1 (`01` quick tour) → Week 3 (`02` fundamentals) → Weeks 7–9 (`03` comprehensive: joins, CTEs, window functions) |
| [`marimo_widgets/`](marimo_widgets/) | Interactive Marimo UI widgets (dropdown, radio, slider) for building queries, incl. a `WHERE`-clause builder | Week 1 / Week 3 — SQL basics, filtering |
| [`GROUP_BY/`](GROUP_BY/) | `GROUP BY` from a 30-second reference to a 35-lesson capstone | Week 2 — Relational Modeling |
| [`WHERE_vs_HAVING/`](WHERE_vs_HAVING/) | `WHERE` vs. `HAVING` — filtering rows vs. filtering groups | Week 2 — Relational Modeling |
| [`DuckDB_GROUP_BY_Insurance_Dataset/`](DuckDB_GROUP_BY_Insurance_Dataset/) | `GROUP BY` aggregation on a real insurance dataset, with charts | Week 2 — Relational Modeling (also good aggregation practice for Week 4) |
| [`Table_Relationships_1_M_MM/`](Table_Relationships_1_M_MM/) | One-to-one, one-to-many, and many-to-many relationships explained with examples | Week 2 — Relational Modeling (revisit for Week 6 — Database Design) |
| [`DuckDB_Extensions/`](DuckDB_Extensions/) | `INSTALL`/`LOAD`/autoloading, plus hands-on `httpfs`, `json`, and `excel` extensions ([slides PDF](DuckDB_Extensions/duckdb_extensions.pdf)) | Week 4 — SQL Aggregation (reading external/CSV/Excel sources) |
| [`Join_Operations/`](Join_Operations/) | `INNER`/`LEFT`/`RIGHT`/`FULL` joins across employees, departments, countries | Week 5 — SQL Joins |
| [`LIMIT_vs_RANK/`](LIMIT_vs_RANK/) | Why `RANK()` beats `LIMIT` for top-N-per-group queries, incl. ties | Week 7 — Query Performance |
| [`Ranking_Functions/`](Ranking_Functions/) | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, and `NTILE` window functions | Week 7 — Query Performance (advanced notebook's `NTILE`/`LAG`/`LEAD` also fits Week 9) |
| [`Transactions/`](Transactions/) | `BEGIN`/`COMMIT`/`ROLLBACK` and ACID properties in action | Week 8 — Transactions & ACID |
| [`DuckDB_Sub_Queries_Tutorial/`](DuckDB_Sub_Queries_Tutorial/) | Subqueries — scalar, correlated, and `IN`/`EXISTS` patterns, plus CTEs (`WITH`) | Week 9 — Project Integration (CTEs also reinforce Week 7) |
| [`sales_1000_rows/`](sales_1000_rows/) | Three-level SQL progression (basic → intermediate → advanced) on a sales dataset | Weeks 1–8 — see the folder's own week-by-week breakdown |

## How to Use

1. Pick a folder that matches what you're learning that week — use the
   **Best-Fit Week** column above as a guide.
2. Open the `.py` file in Marimo (`marimo edit <file>.py`), or read the
   `.md` file directly.
3. Check the folder's own `README.md` (where present) for suggested
   reading order and file-by-file details.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
