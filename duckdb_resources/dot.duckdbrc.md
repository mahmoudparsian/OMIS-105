# DuckDB Configuration File — ~/.duckdbrc

## What is ~/.duckdbrc?

`~/.duckdbrc` is a startup configuration file for the DuckDB command-line interface (CLI).

DuckDB automatically executes commands in this file whenever you start:

```bash
duckdb
```

This is useful for:

- teaching SQL
- formatting query output
- enabling timers
- loading extensions
- improving the student experience

---

# File Location

## Mac / Linux

```bash
~/.duckdbrc
```

## Windows

```text
C:\Users\yourname\.duckdbrc
```

---

# Minimal Example

```sql
.timer on
.mode table
.nullvalue NULL
.maxrows 50
```

Meaning:

| Command | Description |
|---|---|
| `.timer on` | show query execution time |
| `.mode table` | pretty table output |
| `.nullvalue NULL` | display NULL clearly |
| `.maxrows 50` | limit very large outputs |

---

# Recommended Configuration for SQL Courses

```sql
.timer on
.mode table
.headers on
.nullvalue NULL

.maxrows 1000000
.maxwidth 1000

.echo off
```

Benefits:

- clean output
- readable tables
- column headers enabled
- avoids row truncation
- allows wider tables
- better classroom demonstrations

---

# Showing All Rows and Columns

DuckDB may trim output when:

- tables have many columns
- rows are very wide
- result sets are large

These settings help avoid truncation:

```sql
.maxrows 1000000
.maxwidth 1000
```

This effectively disables most row trimming and allows wider output.

---

# Output Modes

DuckDB supports multiple output styles.

## Table Mode (Recommended)

```sql
.mode table
```

## CSV Mode

```sql
.mode csv
```

## Markdown Mode

```sql
.mode markdown
```

For teaching SQL:

```sql
.mode table
```

is usually the best option.

For very wide tables:

```sql
.mode markdown
```

or

```sql
.mode csv
```

often displays results more cleanly.

---

# Writing Large Results to a File

Example:

```sql
.output sales_output.txt

SELECT * FROM sales;

.output stdout
```

This writes the full query output to a file.

Useful for:

- debugging
- grading
- exporting large results

---

# Loading Extensions Automatically

DuckDB extensions can be loaded automatically.

Example:

```sql
INSTALL httpfs;
LOAD httpfs;
```

Useful for:

- Parquet files
- HTTP/S3 access
- remote datasets

---

# Automatically Open a Database

Example:

```sql
.open course.duckdb
```

Then running:

```bash
duckdb
```

automatically opens:

```text
course.duckdb
```

---

# Creating the File

## Mac / Linux

```bash
nano ~/.duckdbrc
```

Paste the configuration and save the file.

---

# Example Teaching Workflow

Start DuckDB:

```bash
duckdb
```

Then automatically:

- pretty tables appear
- timers are enabled
- headers are displayed
- most row/column truncation is avoided

This provides a much cleaner classroom experience.

---

# Helpful Tip

Instead of:

```sql
SELECT * FROM sales;
```

Sometimes use:

```sql
DESCRIBE sales;
```

This avoids overwhelming displays when tables contain many columns.

---

# Important Note

`~/.duckdbrc` supports:

- DuckDB CLI commands
- SQL statements

Example:

```sql
.mode table

CREATE SCHEMA IF NOT EXISTS bronze;
```

However, for teaching purposes, keeping the file simple is usually best.
