# OMIS 105 <br> How to Install Python (Mac)

**Course:** OMIS 105 — Introduction to Database Management Systems  
**Quarter:** Fall 2026  
**Author:** Dr. Mahmoud Parsian  

---

## What You Need

| Item | Requirement |
|------|-------------|
| Python version | **3.10 or higher** (we recommend 3.12+) |
| Operating system | macOS |
| Internet connection | Required for download and package installation |
| Disk space | ~200 MB |

After Python is installed, you will run a setup script (`step_2_setup_software.py`) that automatically installs everything else (DuckDB, Pandas, Marimo). You will also install qStudio separately (see `step_4_install_qstudio.md`).

---

## Step 1 — Check if Python is Already Installed

Open **Terminal** (press `Cmd + Space`, type `Terminal`, press Enter) and type:

```
python3 --version
```

If you see `Python 3.10.x` or higher (e.g., `Python 3.12.4`), **you're done — skip to "Verify Your Installation" below.**

If you see `Python 2.x.x`, or `command not found`, or anything below 3.10, continue to Step 2.

## Step 2 — Download Python

1. Open your web browser and go to: **https://www.python.org/downloads/**
2. Click the big yellow button that says **"Download Python 3.x.x"** (the latest version)
3. A `.pkg` file will download to your Downloads folder

## Step 3 — Run the Installer

1. Open the downloaded `.pkg` file
2. Click **Continue** through each screen
3. Click **Install** when prompted
4. Enter your Mac password if asked
5. When you see "The installation was successful," click **Close**

## Step 4 — Verify

**Close Terminal completely** (`Cmd + Q`), then reopen it and type:

```
python3 --version
```

You should see something like `Python 3.12.4`. If so, Python is installed.

Also verify pip (Python's package manager):

```
pip3 --version
```

You should see something like `pip 24.0 from ...`. If so, you're all set.

---

## Verify Your Installation

Open a fresh Terminal and run these three commands one at a time:

```
python3 --version
pip3 --version
python3 -c "print('Hello, OMIS 105!')"
```

If all three commands work and you see `Hello, OMIS 105!` at the end, Python is installed correctly.

---

## Next Step

Once Python is working, run the course setup script:

```
python3 step_2_setup_software.py
```

This script will automatically install DuckDB, Pandas, and Marimo, then verify everything works.

---

## Troubleshooting

### "python3" gives "command not found"

This means Python 3 is not installed or not in your PATH. Go back to Step 2 and download it from python.org.

### I have Python 2 and Python 3 both installed

That's fine. macOS sometimes ships with Python 2 pre-installed. Always use `python3` and `pip3` to make sure you're using the right version:

```
python3 --version
pip3 install duckdb
```

Never use plain `python` or `pip` on a Mac — those may point to the old Python 2.

### "pip3" is not recognized

Try this instead:

```
python3 -m pip --version
```

If that works, use `python3 -m pip install` instead of `pip3 install` for all commands.

### Permission denied errors

If you see "Permission denied" when installing packages:

```
pip3 install --user duckdb pandas marimo
```

The `--user` flag installs packages in your home folder, avoiding permission issues.

### "No module named pip"

Run:

```
python3 -m ensurepip --upgrade
```

### Everything is installed but Marimo won't launch

If `marimo edit step_3_verification.py` gives an error after running `step_2_setup_software.py`:

```
python3 -m marimo edit step_3_verification.py
```

Using `python3 -m` ensures you're launching Marimo from the correct Python installation.

### I installed packages but Python can't find them

This usually means you have multiple Python installations (e.g., one from Homebrew, one from python.org). Check which Python you're using:

```
which python3
```

Make sure the path points to the Python you installed from python.org.

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Check Python version | `python3 --version` |
| Check pip version | `pip3 --version` |
| Run setup script | `python3 step_2_setup_software.py` |
| Launch Marimo | `marimo edit step_3_verification.py` |
| Install a package | `pip3 install <name>` |

---

## Getting Help

If you've tried the troubleshooting steps above and are still stuck:

1. Take a **screenshot** of the error message
2. Note your **macOS version** (Apple menu → About This Mac)
3. Bring both to **office hours** or post on the course discussion board

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
