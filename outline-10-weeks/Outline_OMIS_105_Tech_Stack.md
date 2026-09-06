---
title: OMIS 105 - Tech Stack & Welcome Notebook
author: Instructor
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
## Welcome Notebook & Tech Stack

Quarter: Fall 2026
Instructor: Dr. Mahmoud Parsian (mparsian@scu.edu)

---

# Tech Stack

- **Language:** Python · SQL
- **Database:** DuckDB (in-memory)
- **Notebooks:** Marimo (reactive)
- **Audience:** Junior/Senior business students
- Zero prior exposure to notebooks, SQL, or databases

---

# Purpose

Day-one onboarding notebook for
**OMIS 105 — Introduction to Database Management Systems**

This is the first thing students open.

- Introduces Marimo
- Introduces the concept of a database
- Walks through the very first SQL queries

👉 One self-guided, interactive notebook

---

# Files in This Folder

| File | Purpose |
|------|---------|
| `SQL_101_DuckDB_Notebook_1.py` | Day-one student notebook |
| `SQL_101_DuckDB_Notebook_2.py` | Day-one student notebook |
| `Outline_OMIS_105_10_weeks.md` | 10-week course outline |

---

# Notebook Structure (1/2)

1. **What is a notebook?** — Cells, text vs SQL, Cmd/Ctrl+Enter
2. **What is a database?** — Tables = spreadsheets with rows/columns
3. **First table: `students`** — CREATE TABLE + INSERT, 6 rows
4. **Asking questions with SQL** — three business questions:
   - "Who are the Marketing majors?" → WHERE
   - "Who likes Pizza?" → WHERE (different column)
   - "How many students in each major?" → GROUP BY + COUNT

---

# Notebook Structure (2/2)

5. **Try It Yourself** — editable SQL cell, guided suggestions
6. **Why Marimo is reactive** — automatic cell updates explained
7. **Course roadmap** — 10-week overview table

---

# Marimo Conventions (Pure SQL Cells)

- SQL cells use `_df = mo.sql(f"""...""")` with a bare `return`
- `duckdb.connect(database=':memory:')` created, NOT returned
  (Marimo auto-discovers the connection)
- Markdown cells use `mo.md("""...""")` with `hide_code=True`
- Use `--` SQL comments, not Python `#`, inside SQL cells
- `CREATE OR REPLACE TABLE` for re-runnability

---

# Design Decisions (1/2)

- **Favorite foods, not business data.**
  Low-stakes data (Pizza, Sushi, Tacos) keeps focus on the tool,
  not the business scenario. Business data starts in Week 1.
- **Only 6 rows.** Small enough to see everything at a glance.
- **Three queries only.** Enough to show the pattern —
  SELECT + FROM + WHERE, then GROUP BY.

---

# Design Decisions (2/2)

- **"Try It Yourself" cell.**
  Hands-on editing builds comfort with the tool.
  Specific suggestions lower the barrier.
- **No plots.** Charts come in Week 3.
  Day one is about reading tables and writing SQL.

---

# Teaching Notes

- **In-class usage:** Open live. Walk through the first
  few cells together (5 min), then give students 10 minutes
  to edit "Try It Yourself" on their own laptops.
- **Reactivity demo:** After editing, scroll back up to show
  other cells didn't break. "Marimo keeps everything consistent."
- **Common question:** "Where is the data stored?"
  → In memory only. Data disappears when the notebook closes.

---

# Related Materials

| Folder | Content |
|--------|---------|
| `weekly_reviews/` | Weeks 1–3, 4–6 notebooks, CSVs, plot helpers |
| `software_installation/` | Install guides, setup script, verification |
| `data_stories/` | Standalone Python + DuckDB CRUD demos |

---

# Let's Get Started 🚀

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
