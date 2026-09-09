# OMIS 105 — Software Installation & Verification

**Course:** OMIS 105 — Introduction to Database Management Systems  
**Quarter:** Fall 2026  
**Author:** Dr. Mahmoud Parsian  

---

## Overview

This folder contains everything you need to set up your computer for OMIS 105. Follow **Step 0 → Step 1 → Step 2 → Step 3 → Step 4 below, in order** — don't skip ahead or run any install command until its step tells you to. By the end, you will have **Python**, **DuckDB**, **Marimo**, **Pandas**, and **qStudio** installed and verified.

**Set aside about an hour**, and do this **before the first class**. If you get stuck at any step, stop there and bring it to office hours — don't skip a step and hope the next one works.

## What You'll End Up With

| Software | What It Is | Minimum Version | Installed In | Verified In |
|----------|-----------|-----------------|---------------|-------------|
| [Python](https://www.python.org) | Programming language — the foundation everything else runs on | 3.10+ (3.12+ recommended) | Step 1 | Steps 1, 2, 3 |
| [DuckDB](https://duckdb.org) | In-process SQL database engine — no server to install or configure | 1.0+ | Step 2 | Steps 2, 3 |
| [Marimo](https://marimo.io) | Interactive notebook environment (replaces Jupyter for this course) | any recent | Step 2 | Steps 2, 3 |
| [Pandas](https://pandas.pydata.org) | Data manipulation library — DuckDB query results come back as Pandas tables | any recent | Step 2 | Steps 2, 3 |
| [qStudio](https://www.timestored.com/qstudio/download) | Free SQL editor for writing and exploring queries visually | any recent | Step 4 | Step 4 |

This table is just a reference — **the actual install commands are in the steps below, not here.**

---

## Step 0 — Get the Course Files

Steps 2 and 3 run files that live in this folder, so you need a copy on your own computer first.

1. Go to **https://github.com/mahmoudparsian/OMIS-105**
2. Click the green **`< > Code`** button near the top right
3. Click **Download ZIP**. It is a large file — give it a minute to finish
4. Find **`OMIS-105-main.zip`** in your **Downloads** folder and double-click it to unzip
5. You now have a folder called **`OMIS-105-main`**. Inside it, open the folder named **`software_installation`** — that is where Steps 2 and 3 live

### Now open a terminal *in that folder*

This trick matters: Steps 2 and 3 only work if your terminal is pointed at the `software_installation` folder. You do **not** need to type any folder names.

**Mac**

1. Press `Cmd + Space`, type `Terminal`, press Enter
2. Type `cd` followed by **one space** — do not press Enter yet:

   ```
   cd 
   ```

3. Drag the **`software_installation`** folder from Finder and drop it onto the Terminal window. The full path appears by itself
4. Now press Enter

**Windows**

1. Open the **`software_installation`** folder in File Explorer
2. Click once on the **address bar** at the top (the strip showing the folder path)
3. Type `cmd` and press Enter

A Command Prompt opens already pointed at the right folder.

### Check that it worked

Type this and press Enter:

| OS | Command |
|----|---------|
| Mac | `ls` |
| Windows | `dir` |

You should see `step_2_setup_software.py` in the list. If you do, you are in the right place. If you don't, repeat the drag step above.

---

## Step 1 — Install and Verify Python

* Python is the only piece of software you download and install manually from a website.
* Steps 2 and 3 are handled by scripts; Step 4 (qStudio) is the only other manual install.

| Operating system | What to do |
|------------------|------------|
|**Mac users:**    |Follow [`step_1_install_python_macbook.md`](step_1_install_python_macbook.md) |
|**Windows users:**| Follow [`step_1_install_python_windows.md`](step_1_install_python_windows.md) |

Each guide ends with a "Verify Your Installation" 
section — run those commands before moving on. 
Do not continue to Step 2 until Python is confirmed working.

## Step 2 — Install and Verify DuckDB, Marimo, and Pandas

One script does all of it: installs the three packages, 
then verifies each one, then runs a real DuckDB query 
to prove it all works together.

Use the terminal window you opened in **Step 0** — the one already pointed at the `software_installation` folder. Type this and press Enter:

| OS | Command |
|----|---------|
| Mac | `python3 step_2_setup_software.py` |
| Windows | `python step_2_setup_software.py` |

> **If you see `can't open file ... No such file or directory`,** your terminal is not in the right folder. Go back to Step 0 and redo the drag (Mac) or address-bar (Windows) trick.

Watch for **`[+] PASS`** next to DuckDB, Pandas, and Marimo, and **"ALL CHECKS PASSED"** at the end. If you see any `[X] FAIL`, follow the fix instructions the script prints and run it again — don't move on until every check passes.

## Step 3 — Verify Everything Together in Marimo

Step 2 verifies the packages individually; this step opens a real Marimo notebook to confirm Python, DuckDB, and Marimo all work together the way you'll use them in class.

In the same terminal window, type:

```
marimo edit step_3_verification.py
```

Marimo opens in your web browser. The notebook runs a few checks and then executes a real SQL query. If you can see the query results, **your Python + DuckDB + Marimo setup is complete.**

When you are finished looking at it, go back to the terminal and press `Ctrl + C` to stop Marimo.

> **If you see `marimo: command not found`,** Marimo installed correctly but your computer doesn't know where to find it. Use this instead — it always works:
>
> | OS | Command |
> |----|---------|
> | Mac | `python3 -m marimo edit step_3_verification.py` |
> | Windows | `python -m marimo edit step_3_verification.py` |

## Step 4 — Install and Verify qStudio

qStudio is a free SQL editor you download separately (it's a desktop application, not a `pip` package). Follow [`step_4_install_qstudio.md`](step_4_install_qstudio.md) — it walks through installing qStudio, connecting it to DuckDB, and running a quick test query to confirm it works.

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `step_1_install_python_macbook.md` | Python installation guide for **Mac** |
| `step_1_install_python_windows.md` | Python installation guide for **Windows** |
| `step_2_setup_software.py` | Script that installs and verifies DuckDB, Marimo, and Pandas |
| `step_3_verification.py` | Marimo notebook that verifies everything works together |
| `step_4_install_qstudio.md` | qStudio installation, connection, and verification guide (Mac and Windows) |

---

## Quick Summary

Mac:

```
Step 0:  Download ZIP from GitHub, unzip, open Terminal in software_installation/
Step 1:  Install Python                          (follow the Mac guide, then verify)
Step 2:  python3 step_2_setup_software.py        (installs + verifies DuckDB, Pandas, Marimo)
Step 3:  marimo edit step_3_verification.py      (final check — everything together, in Marimo)
Step 4:  Install qStudio                         (download from timestored.com, then verify)
```

Windows:

```
Step 0:  Download ZIP from GitHub, unzip, open Command Prompt in software_installation\
Step 1:  Install Python                          (follow the Windows guide, then verify)
Step 2:  python step_2_setup_software.py         (installs + verifies DuckDB, Pandas, Marimo)
Step 3:  marimo edit step_3_verification.py      (final check — everything together, in Marimo)
Step 4:  Install qStudio                         (download from timestored.com, then verify)
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
