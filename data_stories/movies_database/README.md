# 🎬 Movies Database

**OMIS-105 · Week 3 — SQL Basics** *(notebook 1)*
**→ Week 5 — Joins** *(notebook 2)*

**The largest and richest schema in `data_stories/`: 18 tables, 4,803 movies,
104,842 people, 129,581 crew credits.** A real film database, close to what a
studio or a streaming service would actually run.

If you want one dataset that carries students from their first `SELECT` all the way
to multi-table joins, this is it.

---

## Run it

```bash
marimo edit notebook_01_basics.py         # Week 3 — start here
marimo edit notebook_02_intermediate.py   # Week 5
```

| File | Role |
|---|---|
| `notebook_01_basics.py` | **Notebook 1** — 15 queries, simple → intermediate |
| `notebook_02_intermediate.py` | **Notebook 2** — 20 queries, intermediate → advanced |
| `plot_util.py` | Chart functions, kept out of the notebooks |
| `movies_db.duckdb` | The database |
| `movies_db_copy.duckdb` | Identical copy — safe to experiment on |
| `duckdb_sql/` | The 12 build scripts, numbered in dependency order |
| `mysql_sql/` | The same schema in MySQL dialect |
| `scripts/`, `create_duckdb.sh` | Build tooling |
| `blog/` | Source material, including a schema diagram (`blog/movies_db_schema.webp`) |
| `CLAUDE.md`, `what_to_do.txt` | Build notes (provenance) |

---

## The schema

Eighteen tables. The core is `movie` and `person`, connected by junction tables:

| Table | Rows | What it holds |
|---|---|---|
| `movie` | 4,803 | One row per film |
| `person` | 104,842 | Actors, directors, crew — everyone |
| `movie_cast` | 106,257 | **Who acted in what**, and as which character |
| `movie_crew` | 129,581 | **Who worked on what**, and in which job |
| `movie_keywords` | 36,162 | Film ↔ keyword |
| `movie_company` | 13,677 | Film ↔ production company |
| `movie_genres` | 12,160 | Film ↔ genre |
| `movie_languages` | 11,740 | Film ↔ language |
| `production_country` | 6,436 | Film ↔ country |
| `keyword` | 9,794 | Keyword lookup |
| `production_company` | 5,047 | Company lookup |
| `country`, `language` | 88 each | Lookups |
| `genre` | 20 | Lookup |
| `department` | 12 | Crew departments |
| `gender`, `language_role` | 3, 2 | Small lookups |

**Six of those are junction tables.** A film has many genres and a genre has many
films; a person appears in many films and a film has many people. None of that fits
in a column — which is the Week 2 lesson, at full scale.

---

## Which notebook belongs to which week

| Notebook | Section | Content | Week |
|---|---|---|---|
| 1 | A | Five simple queries | **3** |
| 1 | B | Five simple+ queries | **3** |
| 1 | C | Five intermediate — joins & aggregations | **4–5** |
| 2 | A | Five simple+ queries | 3–4 |
| 2 | B | Five intermediate — joins & aggregations | **5** |
| 2 | C | Ten intermediate+ — Top-N, **window functions, CTEs** | *beyond the core* |

Notebook 2 §C uses window functions and CTEs, which the 10-week core does not teach.
Fine as demonstration; not assignable as assessed work.

---

## Why this dataset works well

**Students can check the answers.** If a query says the highest-grossing film is
*Avatar*, that is verifiable without trusting the database — which is exactly the
property that makes a teaching dataset good.

**The joins are motivated.** "Which actors appeared in the most films?" genuinely
requires `person` → `movie_cast` → `movie`. Students are not joining tables because
the exercise said to; they are joining them because the question cannot be answered
otherwise.

**`duckdb_sql/` is numbered for a reason.** The twelve build scripts run
`duckdb_sql/01_reference_data.sql` through `duckdb_sql/12_production_country.sql` — lookups first, then
core entities, then junction tables. That ordering *is* the dependency graph: a
foreign key cannot point at a table that does not exist yet. Worth showing when you
teach foreign keys.

---

## Teaching notes

- **Experiment on `movies_db_copy.duckdb`, not `movies_db.duckdb`.** That is what the
  copy is for.
- The schema diagram in `blog/movies_db_schema.webp` is worth projecting before the
  first query. Eighteen tables is intimidating as a list and comprehensible as a
  picture.
- Comparing `duckdb_sql/` with `mysql_sql/` is a quick, concrete look at SQL dialect
  differences — the same schema, two dialects, sitting side by side.
- At 100,000+ row junction tables this is also a reasonable place to revisit
  `INDEXES_AND_PERFORMANCE/` (Week 7) on data students already understand.
