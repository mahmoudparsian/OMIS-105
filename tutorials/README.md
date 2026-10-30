# Tutorials

* Standalone SQL and DuckDB tutorials for OMIS 105.
* Each folder is self-contained: a Marimo notebook or Markdown walkthrough, its README,
and any data it needs.
* The **Best-Fit Week** column maps each tutorial to the
[10-week syllabus](../outline-10-weeks/Outline_OMIS_105_10_weeks.md) topic
it reinforces best. Many tutorials are useful outside that week too —
use the column as a starting point, not a hard rule.
* **When a tutorial needs Mac- and Windows-specific steps** (install
commands, PATH setup, path/quoting differences), it's split into two
fully self-contained files — `..._on_macbook.md` / `..._on_windows.md`,
with no "see the other OS's version" cross-references — plus a folder
`README.md` that acts as a picker. See
[`marimo_for_labs/`](marimo_for_labs/) and
[`DuckDB_from_Command_Line/`](DuckDB_from_Command_Line/) for examples.

## Directory Structure

| Folder | What It Covers | Best-Fit Week(s) |
|---|---|---|
| [`git/`](git/) | Git and GitHub for students: what they are, installing Git on macOS/Windows, cloning this repository, and keeping it up to date | Before Week 1 — setup |
| [`DuckDB_101/`](DuckDB_101/) | Intro slides + notebook: what DuckDB is and why it's used in this course | Week 1 — Database Foundations |
| [`DuckDB_from_Command_Line/`](DuckDB_from_Command_Line/) | Installing and using the DuckDB CLI shell — dot-commands, `.mode`, reading CSVs, script files; separate Mac and Windows decks ([Mac PDF](DuckDB_from_Command_Line/duckdb_from_command_line_on_macbook.pdf), [Windows PDF](DuckDB_from_Command_Line/duckdb_from_command_line_on_windows.pdf)) | Week 1 — Database Foundations |
| [`Create_DuckDB_Database_from_SQL_Files/`](Create_DuckDB_Database_from_SQL_Files/) | Building a saved `.duckdb` database file from a schema file and a records file with `.read`; practice SQL files included; separate Mac and Windows guides | Week 1 — Database Foundations (useful again in Week 5, where the joins databases are built this way) |
| [`DuckDB_Querying_CSV_Files/`](DuckDB_Querying_CSV_Files/) | Reading and querying CSV files directly with DuckDB | Week 1 — Database Foundations |
| [`DuckDB_SQL_Introduction/`](DuckDB_SQL_Introduction/) | First SQL queries against a weather CSV dataset | Week 1 — Database Foundations |
| [`SQL_Tutorial_Documents/`](SQL_Tutorial_Documents/) | Reference PDFs: intro to RDBMS and intro to SQL | Week 1 — background reading |
| [`marimo_introduction/`](marimo_introduction/) | Getting started with Marimo notebooks and `mo.sql()`; `101` = first SQL notebook, `102` = joins, `103` = subqueries/CTEs | Week 1 (`101`) → Week 5 (`102`, joins) → Week 9 (`103`, CTEs) |
| [`marimo_for_labs/`](marimo_for_labs/) | Bulletproof, OS-specific walkthrough: opening a Marimo notebook from the terminal, and DuckDB in-memory vs. persistent connections — including how to write a Windows path correctly (forward vs. backward slashes) | Week 1 — setup, referenced all quarter |
| [`SQL_Tutorial_Notebooks/`](SQL_Tutorial_Notebooks/) | Quick-tour → fundamentals → comprehensive SQL notebook series | Week 1 (`01` quick tour) → Week 3 (`02` fundamentals) → Weeks 7–9 (`03` comprehensive: joins, CTEs, window functions) |
| [`marimo_widgets/`](marimo_widgets/) | Interactive Marimo UI widgets (dropdown, radio, slider) for building queries, incl. a `WHERE`-clause builder | Week 1 / Week 3 — SQL basics, filtering |
| [`CASE_Expression/`](CASE_Expression/) | SQL's `CASE` expression from zero: basic → basic+ → intermediate (conditional counts/sums, `JOIN`, segments, `UPDATE`); a Markdown tutorial with real results plus a matching Marimo notebook | Week 3 — SQL Basics (Part 3 is good review for Weeks 4–9) |
| [`GROUP_BY/`](GROUP_BY/) | `GROUP BY` from a 30-second reference to a 35-lesson capstone | Week 2 — Relational Modeling |
| [`WHERE_vs_HAVING/`](WHERE_vs_HAVING/) | `WHERE` vs. `HAVING` — filtering rows vs. filtering groups | Week 2 — Relational Modeling |
| [`GROUP_BY_and_JOIN_on_Insurance/`](GROUP_BY_and_JOIN_on_Insurance/) | `GROUP BY` aggregation on a real insurance dataset, then `INNER JOIN` + `GROUP BY` with a `regions` table, with charts | Week 2 — Relational Modeling (also good aggregation practice for Week 4; Part 2 joins fit Week 5) |
| [`Table_Relationships_1_M_MM/`](Table_Relationships_1_M_MM/) | One-to-one, one-to-many, and many-to-many relationships explained with examples | Week 2 — Relational Modeling (revisit for Week 6 — Database Design) |
| [`DuckDB_Extensions/`](DuckDB_Extensions/) | `INSTALL`/`LOAD`/autoloading, plus hands-on `httpfs`, `json`, and `excel` extensions ([slides PDF](DuckDB_Extensions/duckdb_extensions.pdf)) | Week 4 — SQL Aggregation (reading external/CSV/Excel sources) |
| [`Join_Operations_by_Examples/`](Join_Operations_by_Examples/) | `INNER`/`LEFT`/`RIGHT`/`FULL` joins across employees, departments, countries | Week 5 — SQL Joins |
| [`Join_Operations_in_Action/`](Join_Operations_in_Action/) | `INNER`/`LEFT`/`RIGHT`/`FULL` joins across 2 tables: `t1` and `t2` | Week 5 — SQL Joins |
| [`SELF_JOIN/`](SELF_JOIN/) | Self joins — one table, two aliases: employee → manager, `LEFT JOIN` + `COALESCE`, pairs with the `<` trick, direct-report counts, grand-managers, today vs. yesterday; a quick-start notebook (`01`) and a full lesson with exercises (`02`) | Week 5 — SQL Joins (the today-vs-yesterday part previews `LAG()` in Week 9) |
| [`LIMIT_vs_RANK/`](LIMIT_vs_RANK/) | Why `RANK()` beats `LIMIT` for top-N-per-group queries, incl. ties | Week 7 — Query Performance |
| [`Ranking_Functions/`](Ranking_Functions/) | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, and `NTILE` window functions | Week 7 — Query Performance (advanced notebook's `NTILE`/`LAG`/`LEAD` also fits Week 9) |
| [`deduplication/`](deduplication/) | Deleting duplicate rows with `ROW_NUMBER() OVER (PARTITION BY ...)`, plus extensions: composite keys, normalized-value dedup, upsert prevention, merge-before-delete, and whole-row dedup | Week 7 — Query Performance (window functions; upsert variant also touches Week 8 constraints) |
| [`Transactions/`](Transactions/) | `BEGIN`/`COMMIT`/`ROLLBACK` and ACID properties in action | Week 8 — Transactions & ACID |
| [`DuckDB_Sub_Queries/`](DuckDB_Sub_Queries/) | Subqueries — scalar, correlated, `IN`/`EXISTS`/`ANY`/`ALL`, derived tables, plus CTEs (`WITH`); 4 guides from basic to complete reference, and four notebooks (basics; correlated subqueries and `EXISTS`; CTEs step by step; more CTEs and ranking) | Week 7 — Subqueries (CTE and ranking notebook also supports Week 9) |
| [`sales_1000_rows/`](sales_1000_rows/) | Three-level SQL progression (basic → intermediate → advanced) on a sales dataset | Weeks 1–8 — see the folder's own week-by-week breakdown |
| [`Introduction_to_RDBMS_with_DuckDB/`](Introduction_to_RDBMS_with_DuckDB/) | 13-part, ~2.5-hour self-paced course covering the whole syllabus in one sequence: relational model & keys, `CREATE TABLE`/`INSERT`, `SELECT`/`WHERE`/`ORDER BY`, joins, aggregation, subqueries/CTEs, constraints & ACID, normalization, views & transactions, DuckDB superpowers, a capstone, and a bonus window-functions deep dive | Weeks 1–9 — comprehensive; see the folder's own README for notebook-by-notebook mapping |

## How to Use

1. Pick a folder that matches what you're learning that week — use the
   **Best-Fit Week** column above as a guide.
2. Open the `.py` file in Marimo (`marimo edit <file>.py`), or read the
   `.md` file directly.
3. Check the folder's own `README.md` (where present) for suggested
   reading order and file-by-file details.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
