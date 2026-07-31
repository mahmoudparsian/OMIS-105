#!/usr/bin/env python3
"""
gen_notebooks.py
----------------
Generate the two Marimo notebooks from scripts/query_specs.py.

Produces (in the project root):
    notebook_01_basics.py
    notebook_02_intermediate.py

Design choices that make the notebooks robust:
  * One setup cell imports marimo / duckdb / plot_util and opens a READ-ONLY
    connection to movies_db.duckdb (resolved relative to the notebook).
  * Every query is a PURE SQL cell: `result = mo.sql(f\"\"\"...\"\"\", engine=conn)`.
    Passing `engine=conn` makes each SQL cell depend on the connection cell, so
    marimo's reactive runtime always runs them in the right order.
  * Markdown explanation cells are flush-left so Markdown renders correctly.
  * Plot cells call plot_util (kept out of the notebook) and return the Figure,
    which marimo renders inline.
"""
import os
import textwrap

import query_specs

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

HEADER = '''import marimo

__generated_with = "0.16.0"
app = marimo.App(width="medium")


'''

FOOTER = '''
@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
'''


def setup_cell():
    body = '''@app.cell
def _():
    import marimo as mo
    import duckdb
    import plot_util
    from pathlib import Path

    try:
        _here = Path(__file__).resolve().parent
    except NameError:
        _here = Path.cwd()

    _candidates = [
        Path.cwd() / "movies_db.duckdb",
        _here / "movies_db.duckdb",
        _here.parent / "movies_db.duckdb",
    ]
    _db = next((str(p) for p in _candidates if p.exists()), "movies_db.duckdb")
    conn = duckdb.connect(_db, read_only=True)
    return conn, mo, plot_util


'''
    return body


def md_cell(markdown_text):
    # content is placed flush-left so Markdown (not indented code) is rendered
    return (
        "@app.cell\n"
        "def _(mo):\n"
        "    mo.md(\n"
        '        r"""\n'
        f"{markdown_text}\n"
        '"""\n'
        "    )\n"
        "    return\n\n\n"
    )


def sql_cell(var, sql):
    return (
        "@app.cell\n"
        "def _(conn, mo):\n"
        f"    {var} = mo.sql(\n"
        '        f"""\n'
        f"{sql}\n"
        '"""\n'
        "        ,\n"
        "        engine=conn,\n"
        "    )\n"
        f"    return ({var},)\n\n\n"
    )


def plot_cell(var, plot):
    # build kwargs string
    parts = []
    for k, v in plot.items():
        if k == "kind":
            continue
        parts.append(f"{k}={v!r}")
    kwargs = ", ".join(parts)
    fn = plot["kind"]
    return (
        "@app.cell\n"
        f"def _(plot_util, {var}):\n"
        f"    plot_util.{fn}({var}, {kwargs})\n"
        "    return\n\n\n"
    )


def build(specs, title_md, out_name):
    chunks = [HEADER, setup_cell(), md_cell(title_md)]
    current_section = None
    for spec in specs:
        if spec.get("section") and spec["section"] != current_section:
            current_section = spec["section"]
            chunks.append(md_cell(f"---\n\n## {current_section}"))
        # explanation
        heading = f"### {spec['title']}"
        chunks.append(md_cell(f"{heading}\n\n{spec['md']}"))
        # pure SQL
        chunks.append(sql_cell(spec["id"], spec["sql"]))
        # optional plot
        if spec.get("plot"):
            chunks.append(plot_cell(spec["id"], spec["plot"]))
    chunks.append(FOOTER)
    out_path = os.path.join(ROOT, out_name)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("".join(chunks))
    print(f"wrote {out_path}  ({len(specs)} queries)")


TITLE_1 = textwrap.dedent("""\
# Movies Database - Notebook 1: SQL Basics

A guided tour of the **movies** DuckDB database using *pure SQL* cells in
Marimo.  Each query below has four parts: a plain-English explanation of
**what** we are doing and **why**, the **SQL** itself, the **result table**,
and - where it helps - a **chart**.

The database has 17 tables.  The central table is `movie` (4,803 films); the
people, genres, keywords, companies, languages and countries each live in
their own table and are linked to movies through small *bridge* tables
(`movie_cast`, `movie_genres`, ...).

**This notebook covers:** 5 simple queries, 5 simple+ queries, and 5
intermediate queries (joins & aggregations).

> Build the database first with `./create_db.sh`, then run this notebook with
> `marimo edit notebook_01_basics.py` (or `marimo run ...`).""")

TITLE_2 = textwrap.dedent("""\
# Movies Database - Notebook 2: Intermediate -> Intermediate+

This notebook builds on the basics and works up to **window functions**,
**Common Table Expressions** (`WITH`), **ranking**, and **Top-N-per-group**
queries - the tools you reach for in real analytical SQL.

**This notebook covers:** 5 simple+ queries, 5 intermediate queries
(joins & aggregations), and 10 intermediate+ queries (Top-N, ranking
functions such as `ROW_NUMBER`/`RANK`/`LAG`, cumulative windows, and
subqueries using `WITH`).

> Build the database first with `./create_db.sh`, then run this notebook with
> `marimo edit notebook_02_intermediate.py` (or `marimo run ...`).""")


def main():
    build(query_specs.NB1, TITLE_1, "notebook_01_basics.py")
    build(query_specs.NB2, TITLE_2, "notebook_02_intermediate.py")


if __name__ == "__main__":
    main()
