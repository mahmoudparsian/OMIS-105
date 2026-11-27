# CLAUDE.md — weekly_reviews/ (gitignored; never `git add`)
One self-contained folder per week, same names as `weekly_lectures/` (the ZIP build pairs them by path; bonus = `bonus/weekNN-*`).
- **Each week folder runs on its own:** own `:memory:` connection, builds every table it queries, own copy of its CSVs,
  `DATA_DIR = Path(__file__).parent / "data"`. New review: copy the nearest week folder.
- Weeks 6–7 setup cells are copied verbatim from `week05_review_notebook.py`: change week 05's setup → re-check the numbers in 6–7.
- Keep the "📦 Download Week N as a ZIP" line under each README's H1.
- Small data (10–30 rows) with edge cases on purpose (NULL `dept_id`, empty department, self-referencing `manager_id`).
Human-facing guide: `weekly_reviews/README.md`. History: `OMIS-105/instructor/archive/claude_notes_2026-11-26/weekly_reviews/CLAUDE.md`
