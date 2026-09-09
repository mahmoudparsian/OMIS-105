---
title: OMIS 105 — Tech Stack & Welcome Notebooks
author: Dr. Mahmoud Parsian
marp: true
theme: default
paginate: true
class: lead
style: |
  section {
    justify-content: flex-start;
  }
---

# OMIS 105
## Welcome Notebooks & Tech Stack

Quarter: Fall 2026
Instructor: Dr. Mahmoud Parsian (mparsian@scu.edu)

---

# Tech Stack

- **Language:** Python · SQL
- **Database:** DuckDB (in-memory)
- **Notebooks:** Marimo (reactive)
- **Audience:** Senior business students
- Zero prior exposure to notebooks, SQL, or databases

---

# Purpose

Day-one onboarding notebooks for
**OMIS 105 — Introduction to Database Management Systems**

These are among the first things students open.

- Introduces Marimo
- Introduces the concept of a database
- Walks through the very first SQL queries

👉 Two self-guided, interactive notebooks

---

# Where to Find the Notebooks

`weekly_lectures/week01-database-foundations/sql_notebooks/`:

| File | Purpose |
|------|---------|
| `SQL_Notebook_01_marimo.py` | Day-one student notebook — first table, first queries |
| `SQL_Notebook_02_marimo.py` | Day-one student notebook — broader SQL 101 tour, with charts |

---

# Notebook 1: Structure (1/2)

1. **What is a notebook?** — Cells, text vs SQL, Cmd/Ctrl+Enter
2. **What is a database?** — Tables = spreadsheets with rows/columns
3. **First table: `students`** — CREATE TABLE + INSERT, 7 rows
4. **Asking questions with SQL** — three business questions:
   - "Who are the Marketing majors?" → WHERE
   - "Who likes Pizza?" → WHERE (different column)
   - "How many students in each major?" → GROUP BY + COUNT

---

# Notebook 1: Structure (2/2)

5. **Try It Yourself** — editable SQL cell, guided suggestions
6. **Why Marimo is reactive** — automatic cell updates explained
7. **Course roadmap** — 10-week overview table

---

# Notebook 2: SQL 101 Tour

A broader, denser walkthrough — better for a second sitting or self-paced
review than a first-day walkthrough:

- Creating tables & inserting data
- Basic SELECT, filtering with WHERE/IN
- Sorting & LIMIT, aggregate functions, GROUP BY
- Data modification: INSERT, UPDATE, DELETE
- Charts via `plot_util.py` (`display_result`, `plot_bar`, `plot_hbar`,
  `plot_pie`, `plot_line`)

---

# Marimo Conventions (`con.execute()`)

- The connection is created with `duckdb.connect(database=':memory:')`,
  and that cell **returns** `(con,)`
- Query cells: `con.execute("""...""").fetchdf()` displays the result
- Every cell touching the database takes `con` as a parameter (`def _(con):`)
  — that's what wires it into Marimo's reactivity
- Markdown cells use `mo.md("""...""")` with `hide_code=True`
- Use `--` SQL comments inside SQL string literals, not Python `#`
- `CREATE OR REPLACE TABLE` for re-runnability

---

# Notebook 1: Design Decisions (1/2)

- **Favorite foods, not business data.**
  Low-stakes data (Pizza, Sushi, Tacos) keeps focus on the tool,
  not the business scenario. Business data starts right after,
  in the Week 1 demos.
- **Only a handful of rows.** Small enough to see everything at a glance.
- **Three queries only.** Enough to show the pattern —
  SELECT + FROM + WHERE, then GROUP BY.

---

# Notebook 1: Design Decisions (2/2)

- **"Try It Yourself" cell.**
  Hands-on editing builds comfort with the tool.
  Specific suggestions lower the barrier.
- **No plots.** Notebook 2 is where charts appear.
  Day one is about reading tables and writing SQL.

---

# Teaching Notes

- **In-class usage:** Open Notebook 1 live. Walk through the first
  few cells together (5 min), then give students 10 minutes
  to edit "Try It Yourself" on their own laptops.
- **Reactivity demo:** After editing, scroll back up to show
  other cells didn't break. "Marimo keeps everything consistent."
- **Common question:** "Where is the data stored?"
  → In memory only. Data disappears when the notebook closes.
- **Notebook 2** is denser — better suited to a second sitting
  or self-paced review than the first-day walkthrough.

---

# Related Materials

| Folder | Content |
|--------|---------|
| `weekly_lectures/week01-database-foundations/` | The welcome notebooks above, plus demo1–demo6 |
| `weekly_reviews/` | One self-contained review notebook per week (`week01`–`week10`) |
| `software_installation/` | Install guides, setup script, verification |
| `tutorials/` | Standalone SQL, DuckDB, and Git walkthroughs |
| `data_stories/` | Standalone Python + DuckDB demo notebooks |

---

# Let's Get Started 🚀

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
