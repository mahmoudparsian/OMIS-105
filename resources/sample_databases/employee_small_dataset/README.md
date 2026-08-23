# Employee Sample Database

A small "employee" HR database (departments, employees, titles,
salaries, managers), provided in two equivalent forms:

```
employee_small_dataset/
├── mysql/    # original MySQL version (reference — see mysql/README.md)
└── duckdb/   # DuckDB version for OMIS 105 (self-contained — see duckdb/README.md)
```

## Which one do I want?

- **OMIS 105 students / labs:** use `duckdb/`. It needs no server —
  just the DuckDB CLI and Python. Run `./create_duckdb.sh` to build
  the database, then open `employee_notebook.py` in Marimo to practice queries.
- **MySQL reference:** `mysql/` holds the original dataset and install
  script this course's DuckDB version was ported from.

`duckdb/` does not depend on `mysql/` at all — it has its own copy of
the data under `duckdb/data/` and builds itself from there.

## Schema (both versions)

| Table | What it holds |
|-------|----------------|
| `department` | department code + name |
| `employee` | name, birth date, gender, hire date |
| `dept_emp` | employee ↔ department history |
| `dept_manager` | employee ↔ department manager history |
| `title` | job titles held over time |
| `salary` | salary history |

The DuckDB version adds a few extra rows on top of the base data (3
employees with no department, 3 departments with no employees) so
`LEFT JOIN ... IS NULL` queries have something to find — see
`duckdb/README.md` for details.

## Build Requirements (`duckdb/`)

This is the original spec `duckdb/` was built to satisfy:

1. Create a DuckDB version of the `mysql/` database, under `duckdb/`.
2. Under `duckdb/`:
   - `create_duckdb.sh` creates a database equivalent to the MySQL one.
   - 3 employees are added who are not assigned to any department.
   - 3 departments are added where no one works.
   - A new Marimo notebook has 4 simple queries, 5 intermediate
     queries, and 5 intermediate+ queries, with plotting where
     possible (pie chart, ...) — plotting code lives outside the
     notebook.
   - `mysql/` is a reference only; `duckdb/` does not depend on it.

All of the above is implemented and verified — see `duckdb/README.md`.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
