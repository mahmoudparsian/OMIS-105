# OMIS 105 <br> How to Install Python (Windows)

**Course:** OMIS 105 — Introduction to Database Management Systems  
**Quarter:** Fall 2026  
**Author:** Dr. Mahmoud Parsian  

---

## What You Need

| Item | Requirement |
|------|-------------|
| Python version | **3.10 or higher** (we recommend 3.12+) |
| Operating system | Windows 10 or Windows 11 |
| Internet connection | Required for download and package installation |
| Disk space | ~200 MB |

After Python is installed, you will run a setup script (`step_2_setup_software.py`) that automatically installs everything else (DuckDB, Pandas, Marimo). You will also install qStudio separately (see `step_4_install_qstudio.md`).

---

## Step 1 — Check if Python is Already Installed

Open **Command Prompt** (press `Win` key, type `cmd`, press Enter) and type:

```
python --version
```

If you see `Python 3.10.x` or higher (e.g., `Python 3.12.4`), **you're done — skip to "Verify Your Installation" below.**

If you see an error, or the Microsoft Store opens, or you see a version below 3.10, continue to Step 2.

## Step 2 — Download Python

1. Open your web browser and go to: **https://www.python.org/downloads/**
2. Click the big yellow button that says **"Download Python 3.x.x"**
3. An `.exe` file will download to your Downloads folder

## Step 3 — Run the Installer

1. Open the downloaded `.exe` file
2. **CRITICAL — On the very first screen, check BOTH boxes at the bottom:**
   - ✅ **"Use admin privileges when installing py.exe"**
   - ✅ **"Add python.exe to PATH"**
3. Click **"Install Now"** (the top option)
4. Wait for the installation to complete
5. If you see "Setup was successful," click **Close**

> **Why is "Add to PATH" so important?**  
> Without it, Windows won't know where to find Python when you type `python` in Command Prompt. This is the #1 cause of installation problems.

## Step 4 — Verify

**Close Command Prompt completely**, then reopen it and type:

```
python --version
```

You should see something like `Python 3.12.4`.

Also verify pip:

```
pip --version
```

You should see something like `pip 24.0 from ...`.

---

## Verify Your Installation

Open a fresh Command Prompt and run these three commands one at a time:

```
python --version
pip --version
python -c "print('Hello, OMIS 105!')"
```

If all three commands work and you see `Hello, OMIS 105!` at the end, Python is installed correctly.

---

## Next Step

Once Python is working, run the course setup script:

```
python step_2_setup_software.py
```

This script will automatically install DuckDB, Pandas, and Marimo, then verify everything works.

---

## Troubleshooting

### "python" is not recognized

Python was installed without "Add to PATH." The easiest fix:

1. Uninstall Python (Settings → Apps → Python → Uninstall)
2. Re-download from python.org
3. This time, **check "Add python.exe to PATH"** on the first screen
4. Install again
5. Close and reopen Command Prompt

### The Microsoft Store opens when I type "python"

Windows sometimes redirects the `python` command to the Microsoft Store. Fix:

1. Open **Settings → Apps → Advanced app settings → App execution aliases**
2. Turn **OFF** both "App Installer: python.exe" and "App Installer: python3.exe"
3. Close and reopen Command Prompt
4. Now install Python from python.org as described above

### "pip" is not recognized

If Python works but pip doesn't:

```
python -m ensurepip --upgrade
```

After that, use `python -m pip install` instead of `pip install`:

```
python -m pip install duckdb
```

### Permission denied errors

Run Command Prompt **as Administrator**:

1. Press the `Win` key
2. Type `cmd`
3. Right-click **Command Prompt** and select **"Run as administrator"**
4. Try the install command again

### My antivirus is blocking the installation

Some antivirus software may flag Python or pip downloads. Temporarily disable your antivirus during installation, then re-enable it afterward. Windows Defender generally does not cause issues.

### I installed packages but Python can't find them

This usually means you have multiple Python installations. Check which Python you're using:

```
where python
```

Make sure the path points to the Python you installed from python.org (typically `C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe`).

### Everything is installed but Marimo won't launch

If `marimo edit step_3_verification.py` gives an error after running `step_2_setup_software.py`:

```
python -m marimo edit step_3_verification.py
```

Using `python -m` ensures you're launching Marimo from the correct Python installation.

### "python" works but shows Python 2.x

You may have an old Python 2 installation. Try:

```
python3 --version
```

or

```
py -3 --version
```

If either shows Python 3.10+, use that command instead. You can also uninstall the old Python 2 from Settings → Apps.

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Check Python version | `python --version` |
| Check pip version | `pip --version` |
| Run setup script | `python step_2_setup_software.py` |
| Launch Marimo | `marimo edit step_3_verification.py` |
| Install a package | `pip install <name>` |

---

## Getting Help

If you've tried the troubleshooting steps above and are still stuck:

1. Take a **screenshot** of the error message
2. Note your **Windows version** (Settings → System → About)
3. Bring both to **office hours** or post on the course discussion board

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
