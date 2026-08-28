# DuckDB CSV Files Tutorial

A hands-on Marimo notebook that teaches every common way to get a CSV
file into a DuckDB table — from a one-line auto-detect to explicit
schemas, multi-file loading, and error handling.

## Files

| File | What it is |
|---|---|
| `duckdb_csv_tables.py` | The Marimo notebook (all code below). Creates its own sample CSV files when you run it — no data files to download. |

## Requirements

```bash
pip install duckdb marimo pandas
```

## How to Run

Open a terminal in this folder and run:

```bash
marimo edit duckdb_csv_tables.py
```

This opens the notebook in your browser. Run the cells top to bottom —
each one builds on the last.

## What's Inside

| # | Section | What It Covers |
|---|---------|-----------------|
| 1 | Setup | Creates 5 sample CSV files: `employees.csv`, `sales.csv`, `sensors.csv` (with missing values), `products_pipe.csv` (pipe-delimited, no header), and a `monthly_sales/` folder with 3 files |
| 2 | Basic Table Creation | `read_csv_auto`, the `'file.csv'` shorthand, and querying a CSV directly without creating a table |
| 3 | Explicit Schema Definition | `CREATE TABLE` with typed columns + `INSERT`, and `read_csv(..., columns={...})` |
| 4 | CSV Read Options | Pipe delimiters, no header row, `nullstr`, `quote`, `escape`, and a full list of `read_csv` parameters |
| 5 | In-Memory vs. Persistent Databases | Ephemeral (`:memory:`) connections vs. saving to a `.duckdb` file and reopening it later |
| 6 | Querying and Verifying Tables | `DESCRIBE`, `SHOW TABLES`, aggregations, `GROUP BY`, and counting `NULL`s |
| 7 | Loading Multiple CSVs into One Table | Glob patterns (`sales_*.csv`), explicit file lists, and the `filename = true` trick to track source files |
| 8 | Python Relational API | `duckdb.read_csv()` with chained `.filter()` / `.project()` / `.aggregate()`, plus round-tripping with pandas DataFrames |
| 9 | Error Handling and Best Practices | `CREATE OR REPLACE`, a `safe_load_csv()` helper function, `COPY` for bulk loads, `sniff_csv()` to preview a file before loading, and `CREATE VIEW` for live CSV access |

The last cell cleans up all the sample files the notebook created.

## Quick Reference

| Method | Use Case | Example |
|--------|----------|---------|
| `read_csv_auto('file.csv')` | Auto-detect everything | `SELECT * FROM read_csv_auto('data.csv')` |
| `'file.csv'` (string literal) | Quick shorthand | `SELECT * FROM 'data.csv'` |
| `read_csv(...)` with `columns` | Explicit type control | `read_csv('f.csv', columns={...})` |
| `COPY ... FROM` | Bulk loading (fastest) | `COPY t FROM 'f.csv' (HEADER true)` |
| Glob patterns | Multiple files at once | `read_csv_auto('dir/*.csv')` |
| `CREATE VIEW` | Dynamic/live CSV access | `CREATE VIEW v AS SELECT * FROM 'f.csv'` |

## Key Tips

- Use `CREATE OR REPLACE TABLE` so re-running a cell never errors with "table already exists."
- Use `sniff_csv('file.csv')` to preview what DuckDB detects before loading.
- Use `filename = true` when loading multiple files, so you can trace each row back to its source.
- For data that should survive after the notebook closes, connect to a `.duckdb` file instead of `:memory:`.
- Run `DESCRIBE table_name` any time you want to double-check a schema.
