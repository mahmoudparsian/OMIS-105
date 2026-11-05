# Getting Started with the DuckDB CLI: <br> A Beginner's Guide

* DuckDB is a fast, in-process analytical database system. 
* Its Command Line Interface (CLI) allows you to query data files directly, run SQL, and manage databases—all from your terminal.

---
## 0. Data Used Here

```sh
% ls -1 data/
orders.json
sales.csv
students.csv
transactions.csv
users.json
```

## 1. Launching DuckDB

To start an **in-memory** session (data disappears when you exit):

```bash
duckdb
```

To create or open a **persistent database** file (data saves to disk):

```bash
duckdb my_data.duckdb
```

---

## 2. Essential Dot Commands (`.help`, `.mode`, `.schema`, etc.)

1. Dot commands are built-in CLI directives that don't end with a semicolon. 
2. They control CLI output, formats, and environment settings.

### `.help` — Get Help
Displays available dot commands.
```text
D .help
```

### `.mode` — Change Output Format
By default, DuckDB uses `duckbox` format. You can switch to markdown, CSV, JSON, or table formatting for easier viewing or exporting.

```sql
-- Change display mode to markdown
.mode markdown

-- Change back to the standard visual box
.mode duckbox
```

### `.show` — View Current Settings
Shows the active configuration settings of your CLI session (e.g., active database, output mode).
```sql
.show
```

### `.tables` & `.schema` — Inspect Database Objects
Lists tables and views in the current database, or displays the SQL used to create them.

```sql
-- List all tables
.tables

-- View schema/structure of a specific table
.schema sales_data
```

### `.exit` or `.quit` — Exit DuckDB
Leaves the DuckDB interactive shell.
```text
D .exit
```

---

## 3. Querying Files Directly (CSV, Parquet, JSON)

One of DuckDB’s greatest features is running SQL directly on flat files without importing them first.

### Querying a CSV File
```sql
SELECT 
    transaction_id, user_id, amount, category
FROM 'data/transactions.csv' 
WHERE amount > 100.00 
LIMIT 5;
```

### Querying a Parquet File
Parquet files are columnar and highly efficient 
for analytical queries:

```sql
SELECT 
    region, 
    COUNT(*) AS total_orders, 
    ROUND(AVG(sales), 2) AS avg_sales 
FROM 'orders.parquet' 
GROUP BY region;
```

### Querying JSON Files
DuckDB automatically parses structured or auto-detected JSON:

```sql
SELECT 
    user.id, 
    user.email 
FROM 'users.json' 
LIMIT 10;
```

---

## 4. Realistic Workflow Example

Here is a realistic scenario: loading raw CSV data, creating a clean table, running analytical aggregations, and exporting the results to Parquet.

### Step 1: Create a Table from CSV

```sql
CREATE TABLE sales AS 
SELECT * FROM 'https://raw.githubusercontent.com/duckdb/duckdb/main/data/csv/lineitem.csv';
```

### Step 2: Perform Data Analysis

```sql
SELECT 
    l_returnflag, 
    l_linestatus, 
    SUM(l_quantity) AS sum_qty, 
    SUM(l_extendedprice) AS sum_base_price, 
    ROUND(AVG(l_discount), 2) AS avg_disc 
FROM sales 
GROUP BY 
    l_returnflag, 
    l_linestatus 
ORDER BY 
    l_returnflag, 
    l_linestatus;
```

### Step 3: Export Results to CSV or Parquet

```sql
-- Export directly to a new Parquet file
COPY (
    SELECT l_orderkey, l_extendedprice 
    FROM sales 
    WHERE l_discount > 0.05
) TO 'discounted_sales.parquet' (FORMAT PARQUET);
```

---

## 5. Useful Non-Interactive CLI Commands

You can run DuckDB commands directly from your 
terminal shell without entering interactive mode.

### Execute SQL String Directly

```bash
duckdb -c "SELECT name, type FROM 'plugins.csv' WHERE active = true;"
```

### Execute SQL Script from File

```bash
duckdb my_data.duckdb < script.sql
```

### Convert CSV to Parquet via One-Liner

```bash
duckdb -c "COPY (SELECT * FROM 'input.csv') TO 'output.parquet' (FORMAT PARQUET);"
```

---

## Quick Reference Summary

| Task | Command / Syntax |
| :--- | :--- |
| Start In-Memory Session | `duckdb` |
| Start/Open File Session | `duckdb filename.db` |
| Display Tables | `.tables` |
| View Schema | `.schema table_name` |
| Change View Format | `.mode markdown` / `.mode duckbox` / `.mode csv` |
| Query Data File | `SELECT * FROM 'file.csv'` |
| Exit Shell | `.exit` or `.quit` |