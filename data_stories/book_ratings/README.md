# 📚 Book Ratings

**OMIS-105 · Week 4 — SQL Aggregation**

Ten thousand books and **nearly a million ratings**. Big enough that every question
has to be answered with `GROUP BY` rather than by looking, which is exactly what
Week 4 is about.

---

## Run it

```bash
marimo edit 01_build_database_marimo.py    # build books_db.duckdb — run first
marimo edit 02_sql_queries_marimo.py       # the analysis
```

| File | Role |
|---|---|
| `01_build_database_marimo.py` | Reads the CSVs, normalises column names, builds the database |
| `02_sql_queries_marimo.py` | The query notebook |
| `util_plot.py` | Chart functions, kept out of the notebooks |
| `books.csv` | **10,014 books** |
| `ratings.csv` | **981,756 ratings** |
| `books_db.duckdb` | Built by notebook 1 |
| `CLAUDE.md`, `what-to-do.txt` | Build notes (provenance) |

**Run notebook 1 first.** Notebook 2 expects the database to exist.

---

## The data

| Table | Rows | Meaning |
|---|---|---|
| `books` | 10,014 | One row per book — title, author, year, average rating |
| `ratings` | 981,756 | One row per rating — which user rated which book, and how |

Two tables linked by book id, so a rating can be joined back to the title it belongs
to. That join is what makes the aggregation questions interesting.

---

## What it covers

Notebook 2 is tiered:

| § | Section | Techniques |
|---|---|---|
| 3.0 | Add derived columns | `ALTER`/computed values |
| 3.1 | Five **simple** queries | `SELECT`, `WHERE`, `ORDER BY`, `COUNT` |
| 3.2+ | Aggregation and grouping | `GROUP BY`, `HAVING`, `AVG` |

---

## The lesson hiding in the data

With a million ratings, **"the highest-rated book" is a trap.** A book with one
five-star rating outranks a beloved classic with fifty thousand ratings averaging
4.4 — unless you require a minimum:

```sql
GROUP BY title
HAVING COUNT(*) >= 100        -- ← the line that makes the answer meaningful
ORDER BY AVG(rating) DESC
```

Two lessons in that one line:

- **`HAVING` is the difference between a number and an answer.** Without it, the query
  runs fine and tells you nothing useful.
- **`HAVING` exists because `WHERE` cannot do this job.** You cannot write
  `WHERE COUNT(*) >= 100` — at `WHERE` time the rows have not been grouped yet, so the
  count does not exist.

---

## Teaching notes

- **Run the top-rated query without `HAVING` first.** The result will be a list of
  obscure books nobody has heard of. Then add the threshold and watch the list turn
  into recognisable titles. That before/after is the whole of Week 4 in one example.
- Ask students to justify their threshold. There is no correct number, and defending
  a choice is a more useful skill than being handed one.
- If you also teach **ISBA-2402**, its `books_users_ratings` data story (different
  repo, different book dataset) has the same minimum-votes trap. Worth knowing if you
  run both courses.
