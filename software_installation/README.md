# OMIS 105 — Software Installation & Verification

**Course:** OMIS 105 — Introduction to Database Management Systems  
**Quarter:** Fall 2026  
**Author:** Dr. Mahmoud Parsian  

---

## Overview

This folder contains everything you need to set up your computer for OMIS 105. By the end of these steps, you will have **Python**, **DuckDB**, **Marimo**, **Pandas**, and **qStudio** installed and verified.

## Required Software

| Software | What It Is | Minimum Version |
|----------|-----------|-----------------|
| Python   | Programming language | 3.10+ |
| DuckDB   | In-process SQL database engine | any recent |
| Marimo   | Interactive notebook environment | any recent |
| Pandas   | Data manipulation library | any recent |
| qStudio  | Free SQL editor for writing and testing queries | any recent |

### 1. Python

[https://www.python.org](https://www.python.org)

Python is a programming language that lets you work quickly and integrate systems more effectively. We use Python as the foundation for running notebooks, loading data, and executing SQL.

Install version **3.10 or higher** (we recommend 3.12+).

### 2. DuckDB

[https://duckdb.org](https://duckdb.org)

DuckDB is an open-source, in-process SQL database engine designed for fast analytical query workloads. It runs entirely inside your Python process — no server to install or configure.

**Install the latest version (1.0+).**

```
pip install duckdb
```

### 3. Marimo Notebook

[https://marimo.io](https://marimo.io)

Marimo is an interactive notebook environment for Python. It replaces Jupyter for this course and provides a reactive, reproducible workflow with built-in SQL support.

Install the latest version.

```
pip install marimo
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

### 4. Pandas

[https://pandas.pydata.org](https://pandas.pydata.org)

Pandas is a data manipulation library for Python. DuckDB query results are returned as Pandas DataFrames, which Marimo renders as clean tables.

Install the latest version.

```
pip install pandas
```

### 5. qStudio

[https://www.timestored.com/qstudio/download](https://www.timestored.com/qstudio/download)

qStudio is a free, open-source SQL editor for writing and testing queries. You will use it alongside Marimo to practice SQL and explore databases visually.

Install the latest version. Download from the link above (qStudio is a desktop application, not a pip package).

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `step_1_install_python_macbook.md` | Python installation guide for **Mac** |
| `step_1_install_python_windows.md` | Python installation guide for **Windows** |
| `step_2_setup_software.py` | Script that installs DuckDB, Marimo, and Pandas |
| `step_3_verification.py` | Marimo notebook that verifies everything works |
| `step_4_install_qstudio.md` | qStudio installation guide (Mac and Windows) |

---

## Four Steps to Get Ready

### Step 1 — Install Python

Python is the first software you download and install manually from a website. Steps 2 and 3 are handled by scripts — you only go back to manual installs for qStudio in Step 4.

- **Mac users:** Follow `step_1_install_python_macbook.md`
- **Windows users:** Follow `step_1_install_python_windows.md`

### Step 2 — Run the Setup Script

Open your terminal (Mac) or Command Prompt (Windows) and run:

| OS | Command |
|----|---------|
| Mac | `python3 step_2_setup_software.py` |
| Windows | `python step_2_setup_software.py` |

This script will check your Python version, install the required packages (DuckDB, Pandas, Marimo), verify each one, and print a PASS/FAIL report. When you see **"ALL CHECKS PASSED"**, move to Step 3.

### Step 3 — Open the Verification Notebook

Launch the verification notebook in Marimo:

| OS | Command |
|----|---------|
| Mac | `marimo edit step_3_verification.py` |
| Windows | `marimo edit step_3_verification.py` |

Marimo will open in your web browser. The notebook runs a few checks and then executes a real SQL query. If you can see the query results, **your Python + DuckDB + Marimo setup is complete!**

### Step 4 — Install qStudio

qStudio is a free SQL editor that you download separately. Follow `step_4_install_qstudio.md` for installation instructions on both Mac and Windows.

---

## Quick Summary

```
Step 1:  Install Python                          (follow the guide for your OS)
Step 2:  python3 step_2_setup_software.py        (installs + verifies packages)
Step 3:  marimo edit step_3_verification.py      (final check in Marimo)
Step 4:  Install qStudio                         (download from timestored.com)
```

---

## First-Day Success Checklist

By the end of the first class, every student should be able to do
both of these:

**1. Terminal check:**

| OS | Command |
|----|---------|
| Mac | `python3 -c "import duckdb; print(duckdb.__version__)"` |
| Windows | `python -c "import duckdb; print(duckdb.__version__)"` |

**2. Marimo check** — run this in a Marimo cell:

```python
import duckdb
con = duckdb.connect()
con.execute("SELECT 42 AS answer").df()
```

If both work, your environment is fully ready for OMIS 105.

---

## DuckDB CLI (Optional)

The DuckDB command-line interface is optional but useful for quick
SQL testing outside of Python.

### Mac

```
brew install duckdb
```

Or: [DuckDB CLI for Mac](https://duckdb.org/install/?platform=macos&environment=cli)

### Windows

```
winget install DuckDB.cli
```

Or: [DuckDB CLI for Windows](https://duckdb.org/install/?platform=windows&environment=cli)

**Verify:**

```
duckdb --version
```

---

## Getting Help

If you run into problems:

1. Check the **Troubleshooting** section in the relevant guide
2. Take a **screenshot** of the error message
3. Note your **operating system** and **Python version**
4. Bring these to **office hours** (see
   [`course_information/QUESTIONS_and_OFFICE_HOURS.md`](../course_information/QUESTIONS_and_OFFICE_HOURS.md))
   or post on the course discussion board

Remember: you must also bring a fully charged laptop to every class
session (see
[`course_information/LAPTOP.md`](../course_information/LAPTOP.md)).

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
