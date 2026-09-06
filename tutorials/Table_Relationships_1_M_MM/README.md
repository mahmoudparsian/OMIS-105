# Table Relationships: 1:1, 1:N, N:M

A hands-on Marimo notebook that teaches the three relational table
relationship types using small, self-contained DuckDB tables and inline
SVG diagrams.

**[`relational_db_relationships_tutorial.py`](relational_db_relationships_tutorial.py)** covers:

1. **One-to-One (1:1)** — `persons` ↔ `passports`, with a `UNIQUE` foreign
   key enforcing the relationship. Includes a proof cell that attempts
   (and fails) to insert a duplicate.
2. **One-to-Many (1:N)** — `departments` → `employees`, with aggregation
   queries showing per-department summaries.
3. **Many-to-Many (N:M)** — `students` ↔ `courses` via an `enrollments`
   junction table, including a weighted-GPA calculation using the
   junction table's extra attributes.
4. **Visual diagrams** — inline SVG rendered via `IPython.display.SVG`
   for all three relationship types.
5. **Bonus queries** — anti-joins, self-joins across the N:M tables, and
   schema inspection.
6. **Summary** — a comparison table and key design principles.

Run it with:

```bash
pip install marimo duckdb
marimo edit relational_db_relationships_tutorial.py
```

Everything runs in-memory — no external files needed.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
