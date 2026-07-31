---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: 'Segoe UI', Arial, sans-serif;
    background-color: #fff;
    color: #333;
  }
  section.lead {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #fff;
    text-align: center;
  }
  section.lead h1 {
    font-size: 2.4em;
    color: #ffd700;
  }
  section.lead h2 {
    color: #ccc;
    font-weight: 300;
  }
  h1 {
    color: #0f3460;
    border-bottom: 3px solid #ffd700;
    padding-bottom: 8px;
  }
  code {
    background: #f0f4f8;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.9em;
  }
  pre {
    background: #1a1a2e;
    border-radius: 8px;
    padding: 16px;
  }
  table {
    font-size: 0.85em;
  }
  th {
    background: #0f3460;
    color: #fff;
  }
  strong {
    color: #0f3460;
  }
  blockquote {
    border-left: 4px solid #ffd700;
    background: #f9f9f0;
    padding: 12px 20px;
    font-style: italic;
  }
  section.closing {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #fff;
    text-align: center;
  }
  section.closing h1 {
    color: #ffd700;
    border: none;
  }
---

<!-- _class: lead -->

# What Is DuckDB and Why Should I Use It?

## A Modern Analytical Database That Fits in Your Pocket

---

# What Is DuckDB?

DuckDB is a **fast, in-process analytical database** written in C++.

It runs **inside your application** — no server, no setup, no configuration.

> Think of it as "SQLite for analytics."

**Key idea:** You embed DuckDB in your Python script, R session, or application the same way you'd import any library.

```python
import duckdb
con = duckdb.connect()          # That's it. You have a database.
con.sql("SELECT 42 AS answer").show()
```

Created by Mark Raasveldt and Hannes Mühleisen at CWI Amsterdam.
First released in 2019; production-stable since 2024.

---

# The Problem DuckDB Solves

Traditional analytics workflows have **friction at every step**:

| Step | Traditional Way | Pain Point |
|------|----------------|------------|
| Get data | Export CSV from database | Slow, extra step |
| Load data | Write ETL scripts | Boilerplate code |
| Analyze | Pandas / R / SQL Server | Memory limits, speed |
| Share results | Set up a database server | Ops overhead |

**DuckDB eliminates the middle steps.**

You point it at your CSV, Parquet, or JSON file and run SQL directly — no loading, no ETL, no server.

```python
duckdb.sql("SELECT * FROM read_csv('sales_2024.csv') WHERE revenue > 10000").show()
```

---

# Core Architecture: Why It's Fast

DuckDB uses a **columnar-vectorized execution engine** — the same design behind enterprise data warehouses, but embedded.

**Columnar storage:** Data is organized by column, not by row. Analytical queries that scan one or two columns out of fifty skip everything else.

**Vectorized execution:** Instead of processing one row at a time, DuckDB processes batches of thousands of values in tight CPU loops, exploiting modern hardware caches.

**Parallel processing:** Queries automatically use all your CPU cores. A 4-core laptop runs queries 4× faster with zero configuration.

**Zero-copy integration:** When you query a Pandas DataFrame, DuckDB reads it in place — no copying the data.

The result: queries that take minutes in Pandas often finish in seconds in DuckDB.

---

# When Should You Use DuckDB?

**DuckDB shines when you need to:**

- Analyze CSV, Parquet, or JSON files without setting up a database
- Run SQL queries against Pandas/Polars DataFrames
- Process datasets that are too large for Pandas but don't need a cluster
- Build data pipelines that run on a single machine
- Prototype analytical queries before deploying to a warehouse
- Embed a database inside a desktop or mobile application

**DuckDB is probably not the right choice for:**

- High-concurrency web applications (many users writing at once)
- Real-time transactional workloads (use PostgreSQL or SQLite)
- Petabyte-scale data (use Spark, BigQuery, or Snowflake)

---

# DuckDB vs. the Alternatives

| Feature | DuckDB | SQLite | PostgreSQL | Pandas |
|---------|--------|--------|------------|--------|
| Setup needed | None | None | Server install | None |
| Best for | Analytics | Transactions | Both | Small data |
| Handles 10 GB+ | Yes | Slowly | Yes | Crashes |
| SQL support | Full | Full | Full | No |
| Columnar engine | Yes | No | No | N/A |
| Parallel queries | Yes | No | Yes | Limited |
| Read CSV/Parquet | Built-in | No | Extensions | Yes |
| In-process | Yes | Yes | No | Yes |

**DuckDB fills the gap** between "quick scripting" tools like Pandas and "heavy infrastructure" databases like PostgreSQL.

---

# Superpower: Query Anything with SQL

DuckDB reads multiple formats **directly in SQL** — no import step.

```sql
-- CSV files
SELECT * FROM read_csv('customers.csv');

-- Parquet files (columnar, compressed)
SELECT * FROM read_parquet('events/*.parquet');

-- JSON files
SELECT * FROM read_json('api_response.json');

-- Pandas DataFrames (just use the variable name!)
SELECT * FROM my_dataframe WHERE status = 'active';

-- Even remote files over HTTP
SELECT * FROM read_parquet('https://example.com/data.parquet');
```

You can also **join across formats** in a single query — a CSV with a Parquet file with a DataFrame. No other tool makes this so effortless.

---

# Real-World Example: Log Analysis

Imagine you have 2 GB of web server logs in CSV format.

```python
import duckdb

# One line to answer: "Which pages got the most 500 errors yesterday?"
duckdb.sql("""
    SELECT
        url,
        COUNT(*)            AS error_count,
        COUNT(DISTINCT ip)  AS unique_users
    FROM read_csv('access_log_*.csv')
    WHERE status_code = 500
      AND timestamp >= CURRENT_DATE - INTERVAL 1 DAY
    GROUP BY url
    ORDER BY error_count DESC
    LIMIT 10
""").show()
```

This runs in seconds on a laptop. In Pandas, you'd first need to load the entire dataset into memory, parse dates, filter, group — and probably run out of RAM.

---

# Getting Started in 60 Seconds

**Install:**
```bash
pip install duckdb
```

**In-memory (ephemeral):**
```python
import duckdb
con = duckdb.connect()            # data lives in RAM, gone when script ends
```

**Persistent (saved to disk):**
```python
con = duckdb.connect('my_data.db')  # data survives across sessions
```

**Quick one-liner (no connection needed):**
```python
duckdb.sql("SELECT * FROM read_csv('data.csv') LIMIT 5").show()
```

**Works everywhere:** Python, R, Java, Node.js, Rust, Go, C/C++, WASM (in-browser), and a standalone CLI.

---

<!-- _class: closing -->

# Start Using DuckDB Today

Replace your next `pd.read_csv()` + filtering + groupby
with a single `duckdb.sql(...)` call — and feel the difference.

**Resources**

duckdb.org — Official docs and guides
github.com/duckdb/duckdb — Source code
duckdb.org/docs/guides — Tutorials and recipes

**Install now:**
`pip install duckdb`
