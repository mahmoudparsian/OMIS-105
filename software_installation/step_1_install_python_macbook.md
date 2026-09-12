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
| Disk space | ~600 MB (Python itself, plus the packages Step 2 installs) |

After Python is installed, you will run a setup script (`step_2_setup_software.py`) that automatically installs everything else (DuckDB, Pandas, Marimo, Matplotlib). You will also install qStudio separately (see `step_4_install_qstudio.md`).

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

Once Python is working, go back to [`README.md`](README.md) and continue with **Step 2**. You will run the course setup script:

```
python3 step_2_setup_software.py
```

This script will automatically install DuckDB, Pandas, Marimo, and Matplotlib, then verify everything works.

> Your Terminal must be pointed at the `software_installation` folder for this to work. **Step 0** in the README shows the drag-and-drop trick that does it.

---

## Troubleshooting

### "python3" gives "command not found"

This means Python 3 is not installed or not in your PATH. Go back to Step 2 and download it from python.org.

### Should I type `python` or `python3`?

Always type **`python3`** and **`pip3`** on a Mac.

On most Macs, plain `python` does not exist at all, so the command simply
fails. On a Mac where it does exist, it may point at a different Python
than the one you just installed. Typing `python3` and `pip3` removes the
guesswork:

```
python3 --version
pip3 install duckdb
```

### "pip3" is not recognized

Try this instead:

```
python3 -m pip --version
```

If that works, use `python3 -m pip install` instead of `pip3 install` for all commands.

### "error: externally-managed-environment"

You may see this when installing packages. It means your `python3` came
from Homebrew rather than from python.org. It is not a broken computer —
that Python simply protects itself from changes.

**`step_2_setup_software.py` already handles this for you** — it notices
the message and installs anyway. If you hit it while typing a `pip3`
command by hand, add the flag the script uses:

```
pip3 install --break-system-packages duckdb
```

### Permission denied errors

If you see "Permission denied" when installing packages:

```
pip3 install --user duckdb pandas marimo matplotlib
```

The `--user` flag installs packages in your home folder, avoiding permission issues.

> If this gives you `externally-managed-environment` instead, `--user`
> will not help — that is the different problem described just above.
> Use `--break-system-packages` for those commands.

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
