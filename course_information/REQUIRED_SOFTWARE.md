# OMIS 105 — Required Software

**Course:** OMIS 105 — Introduction to Database Management Systems  
**Quarter:** Fall 2026  

---

## 1. Python

[https://www.python.org](https://www.python.org)

Python is a programming language that lets you work quickly and integrate systems more effectively. We use Python as the foundation for running notebooks, loading data, and executing SQL.

Install version **3.10 or higher** (we recommend 3.12+).

---

## 2. DuckDB

[https://duckdb.org](https://duckdb.org)

DuckDB is an open-source, in-process SQL database engine designed for fast analytical query workloads. It runs entirely inside your Python process — no server to install or configure.

Install the latest version (1.0+).

**Install via pip:**

```
pip install duckdb
```

---

## 3. Marimo Notebook

[https://marimo.io](https://marimo.io)

Marimo is an interactive notebook environment for Python. It replaces Jupyter for this course and provides a reactive, reproducible workflow with built-in SQL support.

Install the latest version.

**Install via pip:**

```
pip install "marimo[sql]"
```

**To launch a notebook:**

```
marimo edit <notebook>.py
```

**To verify a notebook runs correctly:**

```
python3 <notebook>.py
```

---

## 4. Pandas

[https://pandas.pydata.org](https://pandas.pydata.org)

Pandas is a data manipulation library for Python. DuckDB query results are returned as Pandas DataFrames, which Marimo renders as clean tables.

Install the latest version.

**Install via pip:**

```
pip install pandas
```

---

## 5. qStudio

[https://www.timestored.com/qstudio/download](https://www.timestored.com/qstudio/download)

qStudio is a free, open-source SQL editor for writing and testing queries. You will use it alongside Marimo to practice SQL and explore databases visually.

Install the latest version. Download from the link above (qStudio is a desktop application, not a pip package).

---

## Quick Install Summary

**Step 1** — Install Python from [python.org](https://www.python.org/downloads/)

**Step 2** — Install Python packages:

```
pip install duckdb "marimo[sql]" pandas
```

**Step 3** — Download and install qStudio from [timestored.com](https://www.timestored.com/qstudio/download)

For a step-by-step walkthrough of these same installs, see
[`SOFTWARE_INSTALLATION.md`](./SOFTWARE_INSTALLATION.md). For the
guided setup scripts, see the top-level `software_installation/`
folder in the repository (not this file).

Remember: you must also bring a fully charged laptop to every class
session (see [`LAPTOP.md`](./LAPTOP.md)).

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
