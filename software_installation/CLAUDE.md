# CLAUDE.md — software_installation

## Purpose

This folder contains the student-facing software setup guide for
OMIS 105 — Introduction to Database Management Systems (Fall 2026).
Students follow these steps **before the first class** to install and
verify the five required tools.

## Audience

Senior business students at Santa Clara University with **zero prior
exposure** to programming, SQL, or command-line tools. Every instruction
must be explicit, jargon-free, and assume nothing beyond basic computer
literacy (opening a browser, downloading a file, finding the Downloads
folder).

## Five Required Tools

| Tool | Installed in | Verified in |
|------|-------------|-------------|
| Python (>= 3.10) | Step 1 (platform-specific guides) | Step 2 + Step 3 |
| DuckDB | Step 2 (pip install) | Step 2 + Step 3 |
| Pandas | Step 2 (pip install) | Step 2 + Step 3 |
| Marimo | Step 2 (pip install) | Step 3 (the notebook itself) |
| qStudio | Step 4 (manual download) | Step 4 (quick test query) |

## File Inventory

| File | Format | Role |
|------|--------|------|
| `README.md` | Markdown | Landing page — what each tool is and why it's required, plus the 4-step install/verification walkthrough |
| `step_1_install_python_macbook.md` | Markdown | Mac Python installation guide |
| `step_1_install_python_windows.md` | Markdown | Windows Python installation guide |
| `step_2_setup_software.py` | Python script | Automated installer — checks Python version, pip-installs duckdb/pandas/marimo, verifies each, runs a test query |
| `step_3_verification.py` | Marimo notebook | Interactive verification — if students can open and see it, everything works |
| `step_4_install_qstudio.md` | Markdown | qStudio download, install, and connect-to-DuckDB guide |

`REQUIRED_SOFTWARE.md` (formerly in `course_information/`) and
`SOFTWARE_INSTALLATION.md` (formerly in `course_information/`) were
both retired — all of their content now lives in `README.md`, so
this folder has a single landing page instead of three overlapping
documents. Any new "what/why" content for a tool belongs in the
`README.md` **Required Software** section; any new "how-to" content
belongs in the **Four Steps to Get Ready** section or a new
`step_N_*` file.

## Conventions

### SQL pattern — `con.execute()`, not `mo.sql()`

All SQL in this folder (and across the entire course) uses:

```python
import duckdb
con = duckdb.connect()
con.execute("CREATE OR REPLACE TABLE ...")
_df = con.execute("SELECT ...").df()
```

Do **not** use `mo.sql()`. The `con.execute()` pattern is consistent
with every teaching notebook (SQL_101, SQL_102, SQL_103, weekly lectures,
labs). Students should see one pattern from day one.

### Table creation — `CREATE OR REPLACE TABLE`

Always use `CREATE OR REPLACE TABLE` so cells are re-runnable without
errors.

### Marimo notebooks

- Use `@app.cell(hide_code=True)` on all markdown/header cells so
  students see clean output without Python code.
- No PEP 723 inline script metadata (`# /// script` blocks). Packages
  are installed system-wide via Step 2; the sandbox prompt requires
  network access and confuses beginners.
- Cell output must be the **last top-level expression**. Never place
  output inside `if/else` branches — assign to variables inside branches,
  then `mo.vstack([...])` unconditionally at the end.
- Use underscore-prefixed variables (`_df`, `_sql`) for cell-private
  data that should not enter Marimo's reactive graph.

### Platform coverage

Every guide must cover **both macOS and Windows**. Use separate sections
or separate files (as Step 1 does). Linux users are not the primary
audience but a brief note ("install Python via your package manager")
is welcome where appropriate.

### Tone and style

- Short sentences, simple vocabulary.
- Numbered steps for procedures (1, 2, 3...).
- `[+] PASS` / `[X] FAIL` format for verification output.
- Every guide includes a **Troubleshooting** section addressing the
  most common issues (PATH not set, macOS "unidentified developer",
  wrong Python version, etc.).
- End every document with the course footer line:
  `*OMIS 105 — Introduction to Database Management Systems — Fall 2026*`

### What NOT to change

- The 4-step ordering (Python first, then packages, then Marimo
  verification, then qStudio) is deliberate — each step depends on
  the previous one.
- `step_2_setup_software.py` is a plain Python script, **not** a
  Marimo notebook. It must run with just `python3 step_2_setup_software.py`
  before Marimo is installed.
