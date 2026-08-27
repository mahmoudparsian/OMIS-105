# Marimo Notebooks and Tutorials

## 1. Getting Started with Marimo

* [Getting Started with the Marimo Notebook (pdf format)](./getting_started_with_the_marimo_notebook.pdf)

## 2. Notebooks in This Folder: SQL/DuckDB

| Notebook | Start Here If... | What It Covers |
|----------|-------------------|-----------------|
| DuckDB/SQL Notebook <br> `marimo_101_duckdb_sql.py` | You've never used Marimo before | Cells, reactivity, UI elements, then DuckDB/SQL (`CREATE TABLE`, `INSERT`, `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`, and an interactive dropdown filter) on a small campus-bookstore dataset |
| DuckDB/SQL Notebook <br> `marimo_102_joins.py` | You've finished 101 | Multi-table data (`customers`, `products`, `orders` — 5–8 rows each) and `JOIN`: `INNER JOIN` vs. `LEFT JOIN`, table aliases, join + `GROUP BY`, and an interactive customer picker |
| DuckDB/SQL Notebook <br> `marimo_103_subqueries_ctes.py` | You've finished 102 | Subqueries in `WHERE`, `FROM`, and with `IN`/`NOT IN`; CTEs (`WITH ... AS`) and chaining multiple CTEs; an interactive threshold slider |
| Marimo Notebook <br> `marimo_introduction.py` | You want Marimo's own official tour | Editor mechanics: reactivity, UI elements, running notebooks as apps, keyboard shortcuts — no SQL |

## 3. How to run any notebook above

Open a terminal in this folder and run

`marimo edit <notebook_file.py>` 

For example, the following command

`marimo edit marimo_101_duckdb_sql.py`

opens the notebook in your browser, ready to edit and run.

## 4. External Docs and Tutorials

[1. marimo: A Reactive, Reproducible Notebook](https://realpython.com/marimo-notebook/)

[2. marimo is an open-source reactive Python notebook](https://docs.marimo.io)

[3. marimo Notebooks for DuckDB](https://www.duckdb.org/docs/lts/guides/python/marimo)

[4. marimo Key concepts](https://docs.marimo.io/getting_started/key_concepts/)

