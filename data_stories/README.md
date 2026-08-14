# Data Stories

**OMIS-105 · Database Management Systems · Santa Clara University**

A **data story** is a self-contained DuckDB + Marimo notebook set built around one
dataset or one concept. Each can be dropped into a lecture, assigned as practice, or
used as a worked example. There are **35** of them here.

They complement `weekly_lectures/` rather than replace it: a week folder teaches the
technique, a data story shows that technique doing real work.

---

## Which story belongs to which week

The course runs **10 weeks**. Every story below is mapped to the week whose material
it exercises.

| Data story | Week |
|---|---|
| `My_Very_First_DuckDB_Notebook/` | **1** |
| `Introducing_DuckDB_by_Presidents/` | **1** |
| `duckdb_magic_notebooks/` | **1** |
| `Python_and_DuckDB/` | **1** |
| `PRIMARY_KEY/` | **2** |
| `DuckDB_Employee_SQL_Mastery/` | **2** |
| `cats_and_breeds/` | **2** |
| `cats_and_breeds_and_images/` | **2** |
| `employees_and_projects/` | **2** |
| `emps_depts_projects/` | **2** |
| `emps_single_table/` | **3** |
| `CRUD_100_emps/` | **3** |
| `CRUD_101_emps/` | **3** |
| `CRUD_102_emps/` | **3** |
| `CRUD_100_10_rows/` | **3** |
| `CRUD_100_10_rows_with_dql/` | **3** |
| `CRUD_100_10_rows_with_images/` | **3** |
| `movies_database/` — notebook 1 (SQL Basics) | **3** |
| `book_ratings/` | **4** |
| `video_game_sales/` | **4** |
| `employees_getting_bonuses/` | **4** |
| `netflix_titles/` | **4** |
| `Top_500_Movies/` | **4** |
| `super_stores_sales/` | **4** |
| `JOIN_101_EMPS_DEPTS_5_departments/` | **5** |
| `JOIN_101_EMPS_DEPTS_10_departments/` | **5** |
| `FK_JOINS/` | **5** (PK/FK intro → 2) |
| `movies_database/` — notebooks 2–3 | **5** |
| `sales-data-exploration/` | **5** |
| `fresh_cart_story/` | **6** (→ 9) |
| `INDEXES_AND_PERFORMANCE/` | **7** |
| `TRANSACTIONS_AND_ACID/` | **8** |
| `auto_insurance/` | **9** |
| `insurance_dataset/` | **9** |
| `CRUD_100_10_rows_with_images_openai/` | **10** |
| `music_dataset_1950_to_2019/` | — *(raw CSV only — no notebooks)* |

---

## What each week covers

Taken from `weekly_lectures/` and its `lab.md` files, so the mapping can be checked
rather than taken on trust:

| Week | Folder | Topic | What a story needs to fit |
|---|---|---|---|
| **1** | `week01-database-foundations` | What a database is; first DuckDB contact | Runs from zero; no schema knowledge assumed |
| **2** | `week02-relational-modeling` | Tables, keys, PK/FK, ER thinking | `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY` |
| **3** | `week03-sql-basics` | `SELECT`, `WHERE`, `ORDER BY` | Single table, row-level filtering |
| **4** | `week04-sql-aggregation` | `COUNT`, `SUM`, `GROUP BY`, `HAVING` | Aggregation is the point of the queries |
| **5** | `week05-sql-joins` | `INNER JOIN`, `LEFT JOIN` | Two or more related tables |
| **6** | `week06-database-design` | Normalization, splitting tables | A schema worth critiquing or normalizing |
| **7** | `week07-query-performance` | Indexing, `EXPLAIN` | Query plans, index effects |
| **8** | `week08-transactions-acid` | Transactions, ACID | `BEGIN` / `COMMIT` / `ROLLBACK` |
| **9** | `week09-project-integration` | End-to-end build | Full pipeline: load → model → query → report |
| **10** | `week10-review-modern-data` | Synthesis, modern data trends | Beyond core SQL — AI, external services, new formats |

---

## Why each story lands where it does

Technique counts come from scanning every `mo.sql()` / `execute()` cell in each
folder, not from titles.

| Story | Notebooks | Dominant SQL | Week |
|---|---|---|---|
| `My_Very_First_DuckDB_Notebook` | 1 | 10 queries, `INSERT`, one `GROUP BY` | 1 |
| `Introducing_DuckDB_by_Presidents` | 2 | `CREATE`, `WHERE` ×7, gentle joins | 1 |
| `duckdb_magic_notebooks` | 2 | JupySQL / in-memory tooling | 1 |
| `Python_and_DuckDB` | 2 | Python↔DuckDB lifecycle, `UPDATE`/`DELETE` | 1 |
| `PRIMARY_KEY` | 2 | `PRIMARY KEY`, `INSERT` ×5, `DELETE` ×4 | 2 |
| `DuckDB_Employee_SQL_Mastery` | 3 | `CREATE TABLE` ×6, **PK ×6, FK ×6** | 2 |
| `cats_and_breeds` (+`_and_images`) | 4 / 3 | `CREATE TABLE` ×4 — two related entities | 2 |
| `employees_and_projects` | 6 | Schema definition across 100 employees | 2 |
| `emps_depts_projects` | 2 | Three-entity model | 2 |
| `emps_single_table` | 3 | Full CRUD, `WHERE` ×11, one table | 3 |
| `CRUD_100_emps` / `_101` / `_102` | 2 / 2 / 1 | `INSERT`/`DELETE`/`WHERE` ×7–12 | 3 |
| `CRUD_100_10_rows` (+ `_dql`, `_images`) | 2–3 | CRUD on 10 rows; readable by eye | 3 |
| `movies_database` nb1 | 3 total | Titled "SQL Basics"; `WHERE` ×29 | 3 |
| `book_ratings` | 3 | `GROUP BY` ×4, **`HAVING` ×4** | 4 |
| `video_game_sales` | 4 | `GROUP BY`, `HAVING` | 4 |
| `employees_getting_bonuses` | 1 | `GROUP BY` ×5, `HAVING`, "SQL Fundamentals" | 4 |
| `netflix_titles` | 4 | **`GROUP BY` ×30**, `WHERE` ×35 | 4 |
| `Top_500_Movies` | 3 | `GROUP BY` ×14, `HAVING` ×4 | 4 |
| `super_stores_sales` | 3 | **`GROUP BY` ×74** — the aggregation workhorse | 4 |
| `JOIN_101_EMPS_DEPTS_5_/10_departments` | 2 / 4 | **`JOIN` ×6/×5, `LEFT JOIN` ×2** | 5 |
| `FK_JOINS` | 3 | README states the goal: "teach PK, FK, and JOINS" — inner/left/right | 5 |
| `movies_database` nb2–3 | 3 total | **`JOIN` ×21** | 5 |
| `sales-data-exploration` | 2 | **`JOIN` ×26**, `GROUP BY` ×22 | 5 |
| `fresh_cart_story` | 2 | Normalized schema: PK ×3, FK ×2, `JOIN` ×43, `GROUP BY` ×42 | 6 → 9 |
| `INDEXES_AND_PERFORMANCE` | 1 | `CREATE INDEX`, `EXPLAIN`, `EXPLAIN ANALYZE`, timed comparisons | 7 |
| `TRANSACTIONS_AND_ACID` | 1 | `BEGIN`/`COMMIT`/`ROLLBACK`, `CHECK`, PK, two connections | 8 |
| `auto_insurance` | 3 | Build → clean → analyse; CTE ×5, window ×4, rank ×8 | 9 |
| `insurance_dataset` | 5 | Five-notebook pipeline; `GROUP BY` ×17, CTE ×5 | 9 |
| `CRUD_100_10_rows_with_images_openai` | 2 | CRUD **plus an OpenAI call** — beyond core SQL | 10 |

### The reasoning in one line each

- **Week 1** — the four "meet DuckDB" stories. `My_Very_First_DuckDB_Notebook` assumes
  nothing at all; the other three introduce the tooling (JupySQL magics, the Python
  API, an in-memory database).
- **Week 2** — everything whose real subject is *schema*: `PRIMARY_KEY`,
  `DuckDB_Employee_SQL_Mastery` (6 PKs and 6 FKs across its DDL), and the
  `cats_and_breeds` / `employees_and_projects` modelling sets.
- **Week 3** — the CRUD family. All single-table, all `WHERE`-driven, most of them 10
  to 100 rows so a student can check a result by eye.
- **Week 4** — the aggregation set. `super_stores_sales` has 74 `GROUP BY` clauses; it
  is the natural workhorse for this week.
- **Week 5** — the two `JOIN_101` folders are purpose-built for it, and `FK_JOINS`
  states in its own README that it exists to teach inner, left and right joins.
- **Week 6** — `fresh_cart_story` is the only story with a properly normalized
  multi-table schema to critique.
- **Week 7** — `INDEXES_AND_PERFORMANCE` follows the lab exactly (build, query,
  index, query again), then explains why the speedup is small: DuckDB is columnar.
- **Week 8** — `TRANSACTIONS_AND_ACID` demonstrates all four properties on the
  lab's bank-transfer scenario, and answers its challenge question by closing and
  reopening the database.
- **Week 9** — the two insurance stories are full pipelines (3 and 5 notebooks: load,
  clean, model, analyse), which is what project week needs.
- **Week 10** — `CRUD_100_10_rows_with_images_openai` is the only story that reaches
  outside SQL to an external AI service.

---

## Gaps and caveats

These are worth knowing before you plan the quarter.

**1. Weeks 7 and 8 were uncovered — now filled.** A scan of every `.py` and `.md`
file for `BEGIN TRANSACTION`, `ROLLBACK`, `CREATE INDEX`, `EXPLAIN ANALYZE` and
`ACID` originally returned **zero matches**: query performance and transactions were
taught in `weekly_lectures/` with no supporting story. `INDEXES_AND_PERFORMANCE/`
and `TRANSACTIONS_AND_ACID/` were written to close that gap. Both are new, so they
have had less classroom exposure than the older stories.

**2. Several stories exceed the course's SQL ceiling.** The syllabus tops out at joins
in Week 5, but `super_stores_sales` (22 window functions, 14 CTEs), `auto_insurance`
(8 ranking calls), `netflix_titles` (10 windows) and `fresh_cart_story` (18 each) all
use CTEs and window functions that are never taught. They work as demos or stretch
material — but they cannot be assigned as assessment without teaching those first.

**3. The outline deck disagrees with the lecture folders.**
`outline-10-weeks/Outline_OMIS_105_10_weeks.md` labels Week 3 "Functions & GROUP BY"
and Week 4 "JOINs", while `weekly_lectures/` and its labs have Week 3 = SQL basics,
Week 4 = aggregation, Week 5 = joins. The deck is also internally inconsistent — its
Week 4 is titled both "SQL Core (Part 2)" and "JOINs", and Week 5 both "JOINs" and
"Advanced Techniques". **This mapping follows the lecture folders and lab files**,
since those are the delivered material. Worth reconciling.

**4. Near-duplicate stories.** `CRUD_100_10_rows` has four variants (`_with_dql`,
`_with_images`, `_with_images_openai`), `CRUD_100/101/102_emps` are three takes on the
same idea, `JOIN_101_EMPS_DEPTS` exists in 5- and 10-department versions, and
`cats_and_breeds` has an `_and_images` twin. Pick one per week rather than assigning
several.

**5. Two stories are incomplete.** `music_dataset_1950_to_2019/` holds a CSV and no
notebooks. `CRUD_102_emps/` and `CRUD_100_10_rows_with_images_openai/` returned no
parsable SQL cells in the scan — worth opening before relying on them.

**6. Stray files at the top level.** `flights.csv` and `test_marimo.py` sit directly in
`data_stories/` rather than in a story folder.

**7. Most stories have no README.** 13 of 35 folders lack one. The per-folder READMEs
that do exist are often the original build prompt rather than student-facing
orientation. The two newest stories (`INDEXES_AND_PERFORMANCE/`,
`TRANSACTIONS_AND_ACID/`) have full ones, including teaching suggestions.

**8. DuckDB limits what Week 7 and 8 can show.** Being columnar, DuckDB gets far less
from an index than a row-store would — the Week 7 story measures ~1.6x on 2M rows
where PostgreSQL might show 100x, and treats *why* as the lesson. Being embedded and
single-writer, it also cannot demonstrate deadlocks, lock waits, or isolation levels
beyond snapshot. Both stories say so explicitly rather than overclaiming.

---

## Inside a data story

The common shape:

| File | Role |
|---|---|
| `*_marimo.py` / `notebook*.py` | The runnable notebook(s) |
| `*_helpers.py` / `plot_*.py` | Plotting and helper code, kept out of the notebook |
| `*.duckdb` | Built database — regenerate rather than commit |
| `*.csv` | Source data |
| `README.md` | Per-story orientation (where present) |
