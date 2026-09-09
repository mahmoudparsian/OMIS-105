# Sample Lab

A preview of what an in-class lab looks like in 
this course — a self-contained Marimo notebook, 
not tied to any specific week.


| File | Description |
|------|-------------|
| [`sample_lab_student.py`](./sample_lab_student.py) | The lab students receive — setup is done for you; each question has an empty `con.execute(...)` cell to fill in |
| [`sample_lab_student_solution.py`](./sample_lab_student_solution.py) | A worked solution, provided for reference |
| `data/products.csv` | The dataset the lab queries |
| `data/expensive_products.csv` | A small reference file used by one of the questions |
| [`solution_output.html`](https://mahmoudparsian.github.io/OMIS-105/sample_lab/solution_output.html) | A static snapshot of the solution notebook, with every query's output already run — see [Viewing the solution output](#viewing-the-solution-output) below |


## What it covers

**Sample Lab: Getting Started with DuckDB and SQL Basics** — 16 questions
across 5 parts: exploration, filtering and sorting, aggregation,
computed columns, and a bonus challenge. Concepts: `SELECT`, `WHERE`,
`ORDER BY`, `LIMIT`, `LIKE`, `DISTINCT`, `COUNT`/`SUM`/`AVG`/`MIN`/`MAX`,
and `CASE` expressions.

## Running it

To open the notebook in the interactive Marimo editor (what students
actually use):

```bash
cd sample_lab
marimo edit sample_lab_student.py
```

To just check that the notebook runs cleanly, 
top to bottom, without opening a browser (a Marimo 
notebook is a regular Python file, so plain
`python3` executes every cell in order):


```bash
cd sample_lab
MPLBACKEND=Agg python3 sample_lab_student.py
```

`MPLBACKEND=Agg` tells Matplotlib to render to memory 
instead of trying to open a GUI window — harmless here 
since this lab doesn't plot anything, but it's the repo-wide 
convention (see the root [`README.md`](../README.md), 
§19 "Verifying a Notebook"), so it's used consistently. 
Run it **twice**: the second run is what catches a missing
`CREATE OR REPLACE TABLE`.

## Checking your answers against the solution

`sample_lab_student_solution.py` is a separate notebook — a 
finished copy of the lab with every query already filled in. 
Run it the same two ways:

```bash
cd sample_lab
marimo edit sample_lab_student_solution.py               # browse it interactively
MPLBACKEND=Agg python3 sample_lab_student_solution.py    # just confirm it runs clean
```

Use it to check your own answers after you attempt 
each question yourself — not as a shortcut to skip the 
lab. Copying it in as your submission defeats the point 
of the exercise.

## Viewing the solution output

`solution_output.html` is a static, already-run snapshot of
`sample_lab_student_solution.py` — every question's code **and** its
result table, frozen into one HTML file
(via `marimo export html sample_lab_student_solution.py -o solution_output.html`).
It's for a quick look at expected results without installing anything
or running DuckDB yourself.

**[View the rendered output](https://mahmoudparsian.github.io/OMIS-105/sample_lab/solution_output.html)**
— opens right in your browser, nothing to install. (It needs an
internet connection: the page loads its Marimo viewer assets from a
CDN rather than bundling them.)

If you edit the solution notebook, regenerate this file so it stays in
sync:

```bash
cd sample_lab
MPLBACKEND=Agg marimo export html sample_lab_student_solution.py -o solution_output.html -f
```

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
