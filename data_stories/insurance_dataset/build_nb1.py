import json, textwrap

def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.strip().split("\n")}

def code(source):
    lines = textwrap.dedent(source).strip().split("\n")
    # add newlines for proper ipynb format
    lines = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "code", "metadata": {}, "source": lines, "outputs": [], "execution_count": None}

cells = []

# ── Title ──
cells.append(md("""# Notebook 1 — Build the Insurance DuckDB Database
---
**Goal:** Read `insurance.csv`, identify and remove duplicate rows, and persist a clean table into `insurance_db.duckdb`.

**Columns:** `age`, `gender`, `bmi`, `children`, `smoker`, `region`, `charges`
"""))

# ── Cell 1: Imports ──
cells.append(md("""## Step 1 — Import Libraries
We import **DuckDB** for our SQL database, **Pandas** for display, and our custom **util_plot** module for visualizations."""))

cells.append(code("""
import duckdb
import pandas as pd
from util_plot import *

print("Libraries loaded successfully!")
"""))

# ── Cell 2: Load CSV & preview ──
cells.append(md("""## Step 2 — Load the CSV and Preview the Data
We create an **in-memory** DuckDB connection first, load the CSV, and take a quick look at the shape and first rows."""))

cells.append(code("""
con = duckdb.connect()  # in-memory for now

# Load CSV into a temporary table
con.execute(\"\"\"
    CREATE TABLE raw_insurance AS
    SELECT * FROM read_csv_auto('insurance.csv')
\"\"\")

total_rows = con.execute("SELECT COUNT(*) FROM raw_insurance").fetchone()[0]
print(f"Total rows loaded: {total_rows:,}")

df_preview = con.execute("SELECT * FROM raw_insurance LIMIT 10").df()
df_preview
"""))

# ── Cell 3: Schema ──
cells.append(md("""## Step 3 — Inspect the Table Schema
Let's confirm the column names and data types DuckDB inferred from the CSV."""))

cells.append(code("""
con.execute("DESCRIBE raw_insurance").df()
"""))

# ── Cell 4: Find duplicates ──
cells.append(md("""## Step 4 — Identify All Duplicate Rows
We group by **every column** and keep groups that appear more than once. This shows us the exact rows that are duplicated and how many copies exist."""))

cells.append(code("""
df_dupes = con.execute(\"\"\"
    SELECT age, gender, bmi, children, smoker, region, charges,
           COUNT(*) AS duplicate_count
    FROM   raw_insurance
    GROUP  BY age, gender, bmi, children, smoker, region, charges
    HAVING COUNT(*) > 1
    ORDER  BY duplicate_count DESC, charges DESC
\"\"\").df()

print(f"Number of distinct rows that have duplicates: {len(df_dupes)}")
print(f"Total extra (duplicate) rows: {df_dupes['duplicate_count'].sum() - len(df_dupes)}")
print()
highlight_duplicates(df_dupes)
"""))

# ── Cell 5: Visualize duplicates ──
cells.append(md("""## Step 5 — Visualize the Duplicate Distribution
A bar chart showing how many rows have 2 copies, 3 copies, etc."""))

cells.append(code("""
dup_dist = df_dupes.groupby("duplicate_count").size().reset_index(name="num_rows")
dup_dist["duplicate_count"] = dup_dist["duplicate_count"].astype(str) + "x"

plot_bar(dup_dist, x="duplicate_count", y="num_rows",
         title="Distribution of Duplicate Counts",
         xlabel="Number of Copies", ylabel="Number of Distinct Rows",
         color="#e74c3c")
"""))

# ── Cell 6: Delete duplicates ──
cells.append(md("""## Step 6 — Remove Duplicate Rows
We use DuckDB's **window function** with `ROW_NUMBER()` to keep only the first occurrence of each row. The clean data goes into a new table called `insurance`."""))

cells.append(code("""
con.execute(\"\"\"
    CREATE TABLE insurance AS
    SELECT age, gender, bmi, children, smoker, region, charges
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY age, gender, bmi, children, smoker, region, charges
               ) AS rn
        FROM raw_insurance
    )
    WHERE rn = 1
\"\"\")

clean_rows = con.execute("SELECT COUNT(*) FROM insurance").fetchone()[0]
removed = total_rows - clean_rows
print(f"Original rows:  {total_rows:,}")
print(f"Clean rows:     {clean_rows:,}")
print(f"Rows removed:   {removed:,}")
"""))

# ── Cell 7: Verify no duplicates ──
cells.append(md("""## Step 7 — Verify: No Duplicate Rows Remain
We run the same duplicate-detection query on the clean `insurance` table. The result should be **empty**."""))

cells.append(code("""
df_verify = con.execute(\"\"\"
    SELECT age, gender, bmi, children, smoker, region, charges,
           COUNT(*) AS cnt
    FROM   insurance
    GROUP  BY age, gender, bmi, children, smoker, region, charges
    HAVING COUNT(*) > 1
\"\"\").df()

if len(df_verify) == 0:
    print("VERIFIED: The 'insurance' table has ZERO duplicate rows.")
else:
    print(f"WARNING: {len(df_verify)} duplicated groups still found!")
    display(df_verify)
"""))

# ── Cell 8: Persist to disk ──
cells.append(md("""## Step 8 — Persist to `insurance_db.duckdb`
We now write the clean `insurance` table into a **persistent** DuckDB database file on disk."""))

cells.append(code("""
import os

db_path = "insurance_db.duckdb"

# Remove old DB if it exists so we start fresh
if os.path.exists(db_path):
    os.remove(db_path)

disk_con = duckdb.connect(db_path)

# Copy clean table from in-memory to disk
disk_con.execute(\"\"\"
    CREATE TABLE insurance AS
    SELECT * FROM con.insurance
\"\"\")

row_count = disk_con.execute("SELECT COUNT(*) FROM insurance").fetchone()[0]
print(f"Persisted {row_count:,} rows into '{db_path}'")
print(f"File size: {os.path.getsize(db_path):,} bytes")

disk_con.close()
con.close()
"""))

# ── Cell 9: Final verification ──
cells.append(md("""## Step 9 — Final Verification: Reopen the Database
Open the persisted file from scratch and confirm everything is intact."""))

cells.append(code("""
verify_con = duckdb.connect("insurance_db.duckdb", read_only=True)

# Check table exists
tables = verify_con.execute("SHOW TABLES").df()
print("Tables in database:")
print(tables)
print()

# Row count
n = verify_con.execute("SELECT COUNT(*) FROM insurance").fetchone()[0]
print(f"Row count: {n:,}")
print()

# Quick sample
print("Sample rows:")
verify_con.execute("SELECT * FROM insurance LIMIT 5").df()
"""))

cells.append(code("""
# Final duplicate check on the persisted database
dup_check = verify_con.execute(\"\"\"
    SELECT COUNT(*) AS dup_groups
    FROM (
        SELECT age, gender, bmi, children, smoker, region, charges
        FROM insurance
        GROUP BY age, gender, bmi, children, smoker, region, charges
        HAVING COUNT(*) > 1
    )
\"\"\").fetchone()[0]

print(f"Duplicate groups found: {dup_check}")
if dup_check == 0:
    print("FINAL VERIFICATION PASSED: insurance_db.duckdb is clean and ready!")

verify_con.close()
"""))

cells.append(md("""---
## Summary
| Step | Result |
|------|--------|
| CSV loaded | 1,773 rows (excluding header) |
| Duplicates identified | Displayed above |
| Duplicates removed | Using `ROW_NUMBER()` window function |
| Clean table persisted | `insurance_db.duckdb` → table `insurance` |
| Final verification | Zero duplicates confirmed |

The database is now ready for **Notebook 2** (SQL Queries Tutorial).
"""))

# Build notebook
nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "cells": cells
}

with open("/sessions/awesome-elegant-lovelace/mnt/insurance_dataset/01_build_database.ipynb", "w") as f:
    json.dump(nb, f, indent=1)

print("Notebook 1 created: 01_build_database.ipynb")
