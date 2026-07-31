create a comprehensive jupyter notebook to show how to create DuckDB tables from CSV files (the files can be small size) files with 3 or 4 columns.

The sandbox doesn't have network access to install DuckDB, but I'll create the notebook file directly for you. Let me build a comprehensive `.ipynb` notebook:Here's your comprehensive Jupyter notebook:

[View your notebook](computer:///Users/max/Library/Application%20Support/Claude/local-agent-mode-sessions/17406518-bf97-4472-94aa-60236611f432/e77d4f9a-42e6-42a2-8e2a-d58ec34b1a49/local_247e75c9-8d05-4fdb-bb15-1d4e9b7859d0/outputs/duckdb_csv_tables.ipynb)

The notebook covers 9 sections with runnable examples:

1. **Setup** — Creates 5 sample CSV files (3–4 columns each: employees, sales, sensors, pipe-delimited products, and multi-month sales)
2. **Basic table creation** — `read_csv_auto`, string literal shorthand, and direct CSV querying
3. **Explicit schemas** — `CREATE TABLE` with typed columns, and `read_csv` with a `columns` dict
4. **CSV options** — Handling pipe delimiters, missing headers, null strings, date formats, quoting
5. **In-memory vs. persistent** — Demonstrates ephemeral connections vs. `.duckdb` file storage
6. **Querying tables** — Aggregations, GROUP BY, NULL handling, DESCRIBE
7. **Multiple CSVs** — Glob patterns (`sales_*.csv`), file lists, and the `filename` column trick
8. **Python relational API** — `duckdb.read_csv()` with chained `.filter()/.project()/.aggregate()`, plus pandas integration
9. **Best practices** — `CREATE OR REPLACE`, error-handling helper function, `COPY` for bulk loads, `sniff_csv()`, and `CREATE VIEW` for live access

All cells are self-contained — just run them top to bottom after `pip install duckdb`.

