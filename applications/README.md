# Sample Applications

Streamlit + DuckDB apps that turn each week's SQL topic into something
students can click through, not just read. Every app is self-contained —
its own folder, its own `README.md`, and (where needed) its own
`requirements.txt`.

| App | SQL Focus | Schema | Run |
|---|---|---|---|
| [`AGGREGATION-APP/`](AGGREGATION-APP/) | `COUNT`, `SUM`, `AVG`, `MIN`/`MAX`, `GROUP BY`, `HAVING`, `STRING_AGG`/`LIST` | one table (`employees`) or three tables (`customers`, `products`, `orders`) | `streamlit run app_aggregation_single.py` |
| [`BOOK-STORE-APP/`](BOOK-STORE-APP/) | Progressive series: `SELECT`/`WHERE`/`ORDER BY` → `JOIN`/`GROUP BY` → window functions/subqueries/`INSERT` → full analytics platform | 5 tables (`students`, `courses`, `books`, `purchases`, `course_books`) | `python seed.py && streamlit run app_level1.py` |
| [`CRUD-APP/`](CRUD-APP/) | `INSERT`, `SELECT`, `UPDATE`, `DELETE` | one table (`customers`) | `streamlit run app_v1_basic.py` |
| [`IN-N-OUT-Burger/`](IN-N-OUT-Burger/) | End-to-end POS: normalized schema, transactions, dashboard analytics, natural-language-to-SQL | 10 tables (fully normalized) | `streamlit run app.py` (after `python build_duckdb.py`) |
| [`JOINS-APP/`](JOINS-APP/) | `INNER`, `LEFT`, `RIGHT`, `FULL OUTER` JOIN, Cartesian products | two tables (`employees`, `projects`) | `streamlit run app_joins.py` |
| [`RANKING-APP/`](RANKING-APP/) | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `PARTITION BY` | one table (`player_scores`) | `streamlit run app_ranking.py` |

Each app's own `README.md` has the full tab-by-tab tour and setup
details.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
