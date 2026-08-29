# Tutorials

* Standalone SQL and DuckDB tutorials for OMIS 105. 
* Each folder is self-contained: a Marimo notebook or Markdown walkthrough, its README,
and any data it needs.

## Directory Structure

| Folder | What It Covers |
|---|---|
| [`DuckDB_101/`](DuckDB_101/) | Intro slides + notebook: what DuckDB is and why it's used in this course |
| [`DuckDB_from_command_line/`](DuckDB_from_command_line/) | Installing and using the DuckDB CLI shell — dot-commands, `.mode`, reading CSVs, script files |
| [`DuckDB_GROUP_BY_Insurance_Dataset/`](DuckDB_GROUP_BY_Insurance_Dataset/) | `GROUP BY` aggregation on a real insurance dataset, with charts |
| [`DuckDB_Querying_CSV_Files/`](DuckDB_Querying_CSV_Files/) | Reading and querying CSV files directly with DuckDB |
| [`DuckDB_SQL_Introduction/`](DuckDB_SQL_Introduction/) | First SQL queries against a weather CSV dataset |
| [`DuckDB_Sub_Queries_Tutorial/`](DuckDB_Sub_Queries_Tutorial/) | Subqueries — scalar, correlated, and `IN`/`EXISTS` patterns |
| [`GROUP_BY/`](GROUP_BY/) | `GROUP BY` from a 30-second reference to a 35-lesson capstone |
| [`Join_Operations/`](Join_Operations/) | `INNER`/`LEFT`/`RIGHT`/`FULL` joins across employees, departments, countries |
| [`LIMIT_vs_RANK/`](LIMIT_vs_RANK/) | Why `RANK()` beats `LIMIT` for top-N-per-group queries, incl. ties |
| [`marimo_introduction/`](marimo_introduction/) | Getting started with Marimo notebooks and `mo.sql()` |
| [`marimo_widgets/`](marimo_widgets/) | Interactive Marimo UI widgets (dropdown, radio, slider) for building queries |
| [`Ranking_Functions/`](Ranking_Functions/) | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, and `NTILE` window functions |
| [`sales_1000_rows/`](sales_1000_rows/) | Three-level SQL progression (basic → intermediate → advanced) on a sales dataset |
| [`SQL_Tutorial_Documents/`](SQL_Tutorial_Documents/) | Reference PDFs: intro to RDBMS and intro to SQL |
| [`SQL_Tutorial_Notebooks/`](SQL_Tutorial_Notebooks/) | Quick-tour → fundamentals → comprehensive SQL notebook series |
| [`Table_Relationships_1_M_MM/`](Table_Relationships_1_M_MM/) | One-to-many and many-to-many relationships explained with examples |
| [`Transactions/`](Transactions/) | `BEGIN`/`COMMIT`/`ROLLBACK` and ACID properties in action |
| [`WHERE_vs_HAVING/`](WHERE_vs_HAVING/) | `WHERE` vs. `HAVING` — filtering rows vs. filtering groups |

## How to Use

1. Pick a folder that matches what you're learning that week.
2. Open the `.py` file in Marimo (`marimo edit <file>.py`), or read the
   `.md` file directly.
3. Check the folder's own `README.md` (where present) for suggested
   reading order and file-by-file details.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
