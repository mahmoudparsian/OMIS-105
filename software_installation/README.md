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
| DuckDB   | In-process SQL database engine | 0.9+ |
| Marimo   | Interactive notebook environment | any recent |
| Pandas   | Data manipulation library | any recent |
| qStudio  | Free SQL editor for writing and testing queries | any recent |

## Files in This Folder

| Step | File | Purpose |
|------|------|---------|
| 1 | `step_1_install_python_macbook.md` | Python installation guide for **Mac** |
| 1 | `step_1_install_python_windows.md` | Python installation guide for **Windows** |
| 2 | `step_2_setup_software.py` | Script that installs DuckDB, Marimo, and Pandas |
| 3 | `step_3_verification.py` | Marimo notebook that verifies everything works |
| 4 | `step_4_install_qstudio.md` | qStudio installation guide (Mac and Windows) |

---

## Four Steps to Get Ready

### Step 1 — Install Python

Python is the only software you install manually from a website. Everything else in Steps 2–3 is handled by scripts.

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
Step 3:  marimo edit step_3_verification.py       (final check in Marimo)
Step 4:  Install qStudio                          (download from timestored.com)
```

## Getting Help

If you run into problems:

1. Check the **Troubleshooting** section in the relevant guide
2. Take a **screenshot** of the error message
3. Note your **operating system** and **Python version**
4. Bring these to **office hours** or post on the course discussion board

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
