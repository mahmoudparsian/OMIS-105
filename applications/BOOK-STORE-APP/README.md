# University Bookstore — DuckDB + Streamlit

A four-app teaching series that builds up from single-table queries to a
full read-write analytics platform, all on the same 5-table bookstore
schema (`students`, `courses`, `books`, `purchases`, `course_books`).

**The progression:**

| App | Level | Teaches | Mode |
|---|---|---|---|
| [`app_level1.py`](app_level1.md) | 1 — Explore & Query | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `BETWEEN` | Read-only |
| [`app_level2.py`](app_level2.md) | 2 — Relationships & Joins | `JOIN`, `GROUP BY`, `HAVING`, aggregate functions | Read-only |
| [`app_level3.py`](app_level3.md) | 3 — Analytics & Power | Window functions, subqueries, indexes, `INSERT` | Read + write |
| [`app_bookstore.py`](app_bookstore.md) | Everything at once | A full bookstore intelligence platform: KPI dashboard, LEFT JOIN anti-joins, window-function leaderboards, a chart-building SQL playground | Read + write |

Each level has its own `.md` write-up (linked above) explaining what the
app does and why, written for students.

**Setup:**

```bash
pip install duckdb streamlit pandas matplotlib
python seed.py                # creates bookstore.duckdb
streamlit run app_level1.py   # or app_level2.py / app_level3.py / app_bookstore.py
```

> Reset the database anytime with `python seed.py` — it wipes and rebuilds from scratch.

**More about this project:**

| File | Description |
|---|---|
| [`book_store_story.md`](book_store_story.md) | The data story — why a university bookstore, and the pedagogical reasoning behind it |
| [`schema.md`](schema.md) | Full table DDL, relationships, and design notes |
| `schema.jpg`, `bookstore_schema_erd.svg` | ERD diagrams of the 5-table schema |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
