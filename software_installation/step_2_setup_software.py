#!/usr/bin/env python3
"""
OMIS 105 — Software Setup & Verification Script
=================================================
Course : OMIS 105 — Introduction to Database Management Systems
Quarter: Fall 2026
Author : Dr. Mahmoud Parsian

PURPOSE
-------
Run this script FIRST, before anything else.
It will:
  1. Check that your Python version is 3.10 or higher
  2. Install the required packages (duckdb, pandas, marimo)
  3. Verify each package works correctly
  4. Run a small DuckDB query to prove everything is working
  5. Show you how to launch Marimo

HOW TO RUN
----------
  Mac:     Open Terminal, then type:     python3 step_2_setup_software.py
  Windows: Open Command Prompt, then:    python step_2_setup_software.py

  If "python" doesn't work on Windows, try "python3" or "py".
"""

import sys
import subprocess

# ════════════════════════════════════════════════════════════════
#  STEP 1: Check Python version
# ════════════════════════════════════════════════════════════════

def check_python():
    v = sys.version.split()[0]
    major, minor = sys.version_info.major, sys.version_info.minor
    if major < 3 or (major == 3 and minor < 10):
        print(f"  [X] FAIL  Python {v} — Need 3.10 or higher")
        print()
        print("  HOW TO FIX:")
        print("    1. Go to https://www.python.org/downloads/")
        print("    2. Download Python 3.12 or later")
        print("    3. Install it (Windows: CHECK 'Add Python to PATH')")
        print("    4. Close this window, reopen, and run this script again")
        print()
        sys.exit(1)
    else:
        print(f"  [+] PASS  Python {v}")
        return True


# ════════════════════════════════════════════════════════════════
#  STEP 2: Install packages
# ════════════════════════════════════════════════════════════════

def install_packages():
    packages = ["duckdb", "pandas", "marimo"]
    print()
    print("  Installing required packages...")
    print(f"  (This may take a minute the first time)")
    print()

    for pkg in packages:
        print(f"  Installing {pkg}...", end=" ", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", pkg],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("done")
        else:
            print("PROBLEM")
            print(f"    Error: {result.stderr.strip()[:200]}")
            print(f"    Try running manually:  pip install {pkg}")
            print()


# ════════════════════════════════════════════════════════════════
#  STEP 3: Verify each package
# ════════════════════════════════════════════════════════════════

def verify_packages():
    print()
    results = []

    # DuckDB
    try:
        import duckdb
        r = duckdb.query("SELECT 42 AS answer").fetchone()
        assert r[0] == 42
        results.append(("DuckDB", duckdb.__version__, True))
    except ImportError:
        results.append(("DuckDB", "not found", False))
    except Exception as e:
        results.append(("DuckDB", str(e), False))

    # Pandas
    try:
        import pandas as pd
        results.append(("Pandas", pd.__version__, True))
    except ImportError:
        results.append(("Pandas", "not found", False))

    # Marimo
    try:
        import marimo
        results.append(("Marimo", marimo.__version__, True))
    except ImportError:
        results.append(("Marimo", "not found", False))

    return results


# ════════════════════════════════════════════════════════════════
#  BONUS CHECK: run a live DuckDB query (shown as part of Step 3's
#  success output, not its own numbered step — "Step 4" is qStudio,
#  covered separately in step_4_install_qstudio.md)
# ════════════════════════════════════════════════════════════════

def test_duckdb_query():
    print()
    print("-" * 52)
    print("  Test: Running a DuckDB query")
    print("-" * 52)
    print()

    import duckdb

    con = duckdb.connect(database=':memory:')

    con.execute("""
        CREATE OR REPLACE TABLE test_students (
            student_id INTEGER,
            name       VARCHAR,
            major      VARCHAR,
            gpa        DECIMAL(3,2)
        )
    """)

    con.execute("""
        INSERT INTO test_students VALUES
            (1, 'Alice', 'Computer Science', 3.80),
            (2, 'Bob',   'Business',         3.20),
            (3, 'Carol', 'Mathematics',      3.95)
    """)

    df = con.execute("""
        SELECT * FROM test_students ORDER BY student_id
    """).fetchdf()

    print(df.to_string(index=False))
    print()
    print(f"  [+] PASS  DuckDB created a table, inserted 3 rows,")
    print(f"            and queried them successfully!")

    con.close()
    return True


# ════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════

def main():
    width = 52

    print()
    print("=" * width)
    print("  OMIS 105 — Software Setup & Verification")
    print("=" * width)
    print()

    # Step 1: Python
    print("-" * width)
    print("  Step 1: Checking Python version")
    print("-" * width)
    check_python()

    # Step 2: Install
    print()
    print("-" * width)
    print("  Step 2: Installing required packages")
    print("-" * width)
    install_packages()

    # Step 3: Verify
    print("-" * width)
    print("  Step 3: Verifying installations")
    print("-" * width)
    results = verify_packages()

    all_ok = True
    for name, version, passed in results:
        if passed:
            print(f"  [+] PASS  {name} {version}")
        else:
            print(f"  [X] FAIL  {name} — {version}")
            all_ok = False

    # Bonus: live test query, shown as part of Step 3's success output
    if all_ok:
        test_duckdb_query()

    # Final report
    print()
    print("=" * width)
    if all_ok:
        print("  ALL CHECKS PASSED!")
        print("  You are ready for OMIS 105.")
        print("=" * width)
        print()
        print("  NEXT STEP — Launch Marimo:")
        print()
        print("    1. Open your terminal / Command Prompt")
        print("    2. Type:  marimo edit step_3_verification.py")
        print("    3. Press Enter")
        print()
        print("  Marimo will open in your web browser as an interactive notebook.")
        print()
        print("  ALSO — Install qStudio (Step 4):")
        print()
        print("    qStudio is a free SQL editor for writing and testing queries.")
        print("    See step_4_install_qstudio.md for download and setup instructions.")
    else:
        print("  SOME CHECKS FAILED")
        print("  See the errors above and follow the fix instructions.")
        print("  Then run this script again.")
        print("=" * width)

    print()


if __name__ == "__main__":
    main()
