# OMIS 105 — Software Installation Guide

**Course:** OMIS 105 — Introduction to Database Management Systems  
**Quarter:** Fall 2026  

---

## Overview

Before the first class ends, every student must have the following installed and working:

1. **Python** (3.10+)
2. **DuckDB** (SQL database engine)
3. **Marimo Notebook** (interactive notebook environment)
4. **Pandas** (data manipulation library)
5. **qStudio** (SQL editor)

Detailed step-by-step guides are in the `software_installation/` folder. This document gives you the quick-start version.

---

## Quick Start (5 Minutes)

### Step 1 — Install Python

Download from [python.org/downloads](https://www.python.org/downloads/) and install version 3.10 or higher.

**Windows users:** On the installer's first screen, check **"Add python.exe to PATH"** — this is critical.

Verify it works:

| OS | Command |
|----|---------|
| Mac | `python3 --version` |
| Windows | `python --version` |

You should see `Python 3.10.x` or higher.

### Step 2 — Install Python Packages

| OS | Command |
|----|---------|
| Mac | `pip3 install duckdb "marimo[sql]" pandas` |
| Windows | `pip install duckdb "marimo[sql]" pandas` |

### Step 3 — Verify DuckDB

| OS | Command |
|----|---------|
| Mac | `python3 -c "import duckdb; print(duckdb.__version__)"` |
| Windows | `python -c "import duckdb; print(duckdb.__version__)"` |

If this prints a version number, DuckDB is installed correctly.

### Step 4 — Launch Marimo

```
marimo edit
```

Marimo opens in your browser. Create a new notebook and run this in a cell:

```python
import duckdb
con = duckdb.connect()
con.execute("SELECT 42 AS answer").df()
```

If you see a table with `42`, everything works.

### Step 5 — Install qStudio

Download from [timestored.com/qstudio/download](https://www.timestored.com/qstudio/download) and follow the installer for your OS. qStudio is a desktop application — no pip install needed.

---

## Automated Setup (Recommended)

For a guided experience with error checking, use the setup scripts in the `software_installation/` folder:

```
Step 1:  Install Python                          (see step_1_install_python_macbook.md
                                                   or step_1_install_python_windows.md)
Step 2:  python3 step_2_setup_software.py        (installs + verifies DuckDB, Marimo, Pandas)
Step 3:  marimo edit step_3_verification.py       (final check in Marimo)
Step 4:  Install qStudio                          (see step_4_install_qstudio.md)
```

---

## First-Day Success Checklist

By the end of the first class, every student should be able to do both of these:

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

The DuckDB command-line interface is optional but useful for quick SQL testing outside of Python.

### Mac

```
brew install duckdb
```

Or: [DuckDB CLI for Mac](https://duckdb.org/install/?platform=macos&environment=cli)

### Windows

```
winget install DuckDB.DuckDB
```

Or: [DuckDB CLI for Windows](https://duckdb.org/install/?platform=windows&environment=cli)

**Verify:**

```
duckdb --version
```

---

## Getting Help

If you run into problems:

1. Check the troubleshooting sections in the `software_installation/` guides
2. Take a **screenshot** of the error message
3. Note your **operating system** and **Python version**
4. Bring these to **office hours** or post on the course discussion board
