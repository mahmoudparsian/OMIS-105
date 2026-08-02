# OMIS 105 Welcome Notebook

## Purpose

Day-one onboarding notebook for **OMIS 105 — Introduction to Database Management Systems**, Fall 2026. 

This is the first thing students open. 

It introduces Marimo, the concept of a database, and their very first SQL queries — all in one self-guided, interactive notebook.

* **Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
* **Tech stack:** Python · DuckDB · Marimo
* **Audience:** Junior/Senior business students with zero prior exposure to notebooks, SQL, or databases.

## Files in This Folder

| File | Purpose |
|------|---------|
| `SQL_101_DuckDB_Notebook_1.py` | Interactive Marimo notebook — the day-one student experience |
| `SQL_101_DuckDB_Notebook_2.py` | Interactive Marimo notebook — the day-one student experience |
| `Outline_OMIS_105_10_weeks.md` | Outline of the course for 10 weeks |

## Notebook Structure

The welcome notebook has a deliberate progression:

1. **What is a notebook?** — Cells, text vs SQL, how to run (Cmd/Ctrl+Enter)
2. **What is a database?** — Tables = spreadsheets with rows and columns
3. **First table: `students`** — CREATE TABLE + INSERT with 6 rows (names, majors, favorite foods)
4. **Asking questions with SQL** — Three queries, each introduced by a plain-English business question:
   - "Who are the Marketing majors?" → SELECT ... WHERE
   - "Who likes Pizza?" → SELECT ... WHERE (different column)
   - "How many students in each major?" → GROUP BY + COUNT
5. **Try It Yourself** — Editable SQL cell with guided suggestions
6. **Why Marimo is reactive** — Explains automatic cell updates
7. **Course roadmap** — 10-week overview table

## Marimo Conventions (Pure SQL Cells)

- All SQL cells use the pure SQL pattern: `_df = mo.sql(f"""...""")` with bare `return`
- `duckdb.connect(database=':memory:')` is created but NOT returned (Marimo auto-discovers the connection for SQL cells)
- Markdown cells use `mo.md("""...""")` with `hide_code=True`
- No Python comments (`#`) inside SQL cells — use SQL comments (`--`) instead, so Marimo renders them as native SQL cells with connection dropdown
- `CREATE OR REPLACE TABLE` for re-runnability in Marimo's reactive model

## Design Decisions

- **Favorite foods, not business data.** The `students` table uses relatable, low-stakes data (Pizza, Sushi, Tacos) so students focus on learning the tool, not understanding a business scenario. Business datasets start in Week 1.
- **Only 6 rows.** Small enough to see everything at a glance. Students can verify query results by eye.
- **Three queries only.** Enough to show the pattern (SELECT + FROM + WHERE, then GROUP BY) without overwhelming. The goal is confidence, not coverage.
- **"Try It Yourself" cell.** Hands-on editing in the first session builds comfort with the tool. Specific suggestions lower the barrier ("change Pizza to Sushi").
- **No plots.** Charts come in Week 3. Day one is about reading tables and writing SQL.

## Teaching Notes

- **In-class usage:** Open this notebook live. Walk through the first few cells together (5 min), then give students 10 minutes to edit the "Try It Yourself" cell on their own laptops.
- **Reactivity demo:** After students edit the sandbox cell, scroll back up to show that other cells didn't break. Explain: "Marimo keeps everything consistent. You can't get stale results."
- **Common student question:** "Where is the data stored?" Answer: In memory only. When you close the notebook, the data disappears. This is by design for learning — we'll talk about persistent databases later.

## Related Materials

| Folder | Content |
|--------|---------|
| `OMIS-105/weekly_reviews/` | Weeks 1–3 and 4–6 notebooks (Jupyter + Marimo), CSV datasets, plot helpers, teaching plans |
| `OMIS-105/software_installation/` | Python install guides (Mac/Windows), setup script, verification notebook |
| `OMIS-105/data_stories/` | Standalone Python+DuckDB CRUD demos |
