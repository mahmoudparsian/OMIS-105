# OMIS 105 <br> Installation Troubleshooting (Windows)

**Course:** OMIS 105 — Introduction to Database Management Systems  
**Quarter:** Fall 2026  
**Author:** Dr. Mahmoud Parsian

---

## What This Document Is

This document collects fixes for the problems Windows students
actually hit on the first day of class, beyond what's already covered
in
[`step_1_install_python_windows.md`](step_1_install_python_windows.md)
and [`step_4_install_qstudio_windows.md`](step_4_install_qstudio_windows.md). Start
there first — come here when something still isn't working.

If your problem isn't listed here, take a screenshot of the error and
bring it to office hours (see the end of this document).

---

## 1. qStudio Won't Open Because It Can't Find Java

**Symptom:** qStudio fails to launch, or shows an error message
mentioning "Java" or "JRE" (Java Runtime Environment) when you try to
run it.

qStudio needs Java to run. If your Windows computer doesn't already
have a working Java installed, qStudio can't start. **Java 21 works
fine for this course.**

### Option A — Install with `winget` (recommended, simplest)

Most Windows 10/11 computers already have `winget` (the Windows
Package Manager) built in.

1. Open **Command Prompt** (press `Win`, type `cmd`, press Enter)
2. Type:

   ```
   winget install EclipseAdoptium.Temurin.21.JDK
   ```

3. Press **Y** if asked to accept a license agreement
4. Wait for it to finish — `winget` adds Java to your PATH
   automatically

**Close Command Prompt completely, reopen it**, and verify:

```
java -version
```

You should see something mentioning `21` (e.g., `openjdk version "21..."`).

> **"winget" is not recognized?** Your Windows may be older or missing
> the **App Installer** package. Open the **Microsoft Store**, search
> for **"App Installer"**, and install/update it. Then try the
> `winget` command again. If that still doesn't work, use Option B.

### Option B — Manual install from Adoptium

1. Go to **https://adoptium.net**
2. Choose **Version: 21 (LTS)**, **Operating System: Windows**,
   **Architecture: x64** (or arm64 if you have a Windows-on-ARM
   laptop), **Package Type: JDK**
3. Download the `.msi` installer and open it
4. Click through the setup screens. On the **"Custom Setup"** screen,
   make sure these are all set to install (not "Entire feature will
   be unavailable"):
   - **Add to PATH**
   - **Set JAVA_HOME variable**
5. Click **Install**, then **Finish**

**Close Command Prompt completely, reopen it**, and verify:

```
java -version
```

> **`java -version` shows the wrong version, or an old one?** You
> likely have more than one Java installed. List every copy on your
> PATH:
>
> ```
> where java
> ```
>
> Windows uses the **first** path in that list. If the wrong one is
> first, either uninstall the older Java (Settings → Apps), or move
> the Temurin 21 folder above the others in your PATH — see Section 2
> below for how to edit PATH order.

### After Installing Java

Close qStudio completely if it's open, then launch it again from the
Start menu. It should open normally now.

---

## 2. Putting Java, Python, Marimo, and DuckDB on Your PATH

**What is PATH?** PATH is a list of folders Windows searches through
when you type a command name. If a program's folder isn't in that
list, Command Prompt says `'x' is not recognized as an internal or
external command` — even though the program is installed and sitting
right there on your disk.

You mostly won't need to do this by hand — the installers in this
course add themselves to PATH automatically **if you check the right
box during install**. But here's what to do if one of them didn't,
and where each tool normally lives:

| Tool | Added to PATH by | Typical folder |
|------|-------------------|-----------------|
| Python (`python`, `pip`) | checking **"Add python.exe to PATH"** during install (Step 1 of the main setup) | `C:\Users\YourName\AppData\Local\Programs\Python\Python312\` |
| Java (`java`) | checking **"Add to PATH"** during the Temurin install, or automatically via `winget` | `C:\Program Files\Eclipse Adoptium\jdk-21...\bin` |
| Marimo (`marimo`) | `pip install marimo` (Step 2 of the main setup) | `...\Python312\Scripts\` |
| DuckDB (Python package) | `pip install duckdb` | not a command — it's a Python import, no PATH needed |

**If a command still says "not recognized" after installing it,** add
its folder to PATH by hand:

1. Press `Win`, type **"environment variables"**, and open **"Edit
   environment variables for your account"**
2. Under the top box ("User variables"), click **Path**, then **Edit**
3. Click **New** and paste in the folder that's missing (for example,
   `C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts\`)
4. Click **OK** on all three windows
5. **Close Command Prompt completely and reopen it** — PATH changes
   only take effect in new windows

**To check where a command is currently coming from:**

```
where python
where java
```

Each should print a file path. If it prints nothing, that tool is not
on your PATH yet.

---

## 3. Getting `step_2_setup_software.py` and `step_3_verification.py` Onto Your Windows Laptop

These two files live inside the course's GitHub repository, in the
`software_installation` folder. **Step 0** in
[`README.md`](README.md) covers this in full — here's the short
version:

1. Go to **https://github.com/mahmoudparsian/OMIS-105**
2. Click the green **`< > Code`** button, then **Download ZIP**
3. Find the ZIP in your **Downloads** folder, right-click it, and
   choose **Extract All...**
4. Open the extracted folder, then open **`software_installation`** —
   both files are inside

> **Extract the ZIP somewhere outside OneDrive if you can** (for
> example, `C:\OMIS105\` instead of your OneDrive Desktop or
> Documents). See the OneDrive note under "Other Common Problems"
> below — it explains why this avoids a common Windows-specific
> problem.

If you only need to re-download these two files specifically (for
example, you deleted them by accident but still have the rest):

1. Go to **https://github.com/mahmoudparsian/OMIS-105/tree/main/software_installation**
2. Click on `step_2_setup_software.py`
3. Click the **Download raw file** button (a download-arrow icon
   near the top right of the file view)
4. Repeat for `step_3_verification.py`
5. Move both downloaded files into your `software_installation` folder

> **Already comfortable with Git?** `git clone` or `git pull` also
> works, and makes future weeks easier. See
> [`tutorials/git/README.md`](../tutorials/git/README.md). If that's
> unfamiliar, ignore it — the ZIP is simpler for now.

---

## Other Common Problems

### Files behave strangely, won't save, or give permission errors inside a OneDrive folder

If your Desktop or Documents folder is synced with OneDrive (common on
school-managed laptops), OneDrive can lock files while it's syncing
them, which shows up as confusing "permission denied" or "file in
use" errors while Python or pip is working. If you keep hitting
unexplained errors, move the `software_installation` folder to a
non-synced location, such as `C:\OMIS105\`, and work from there.

### "python" is not recognized, or the Microsoft Store opens instead

These are Python PATH issues, not Java issues — see the full fix in
[`step_1_install_python_windows.md`](step_1_install_python_windows.md#troubleshooting).

### `winget` command not found

Open the **Microsoft Store**, search for **"App Installer"**, and
install or update it — this is what provides `winget`. Restart
Command Prompt afterward. If that still fails, use **Option B (manual
install)** in Section 1 above.

### "Windows protected your PC" (SmartScreen) when opening an installer

This appears on the Python, Java/Temurin, or qStudio installer because
it isn't from one of the handful of vendors Windows recognizes by
default — it doesn't mean the file is unsafe. Click **"More info"**,
then click **"Run anyway"**.

### My antivirus / school-managed laptop is blocking an installer

Some school-managed Windows laptops restrict running `.exe` or `.msi`
installers, or flag them for review. If an installer silently does
nothing, or is blocked with a message from your antivirus or IT
department, you may need administrator rights you don't have on a
managed machine. Bring this to office hours — Dr. Parsian can help you
find an alternative (e.g., a portable install, or IT help).

### Downloaded a new Python and package installs suddenly fail to build

If you installed the very newest Python version (released within the
last few weeks), some packages this course needs may not have a
ready-made install for it yet, and `pip` tries to compile it from
scratch — which fails without extra developer tools. Simplest fix:
uninstall it and install **Python 3.12** instead (still meets the
3.10+ requirement, and everything has ready-made installs for it). See
[`step_1_install_python_windows.md`](step_1_install_python_windows.md).

### `marimo edit` doesn't open a browser tab by itself

This can happen if your default browser is unusual or the app is
sandboxed. Look at the Command Prompt output — Marimo prints a line
like `http://localhost:2718/?access_token=...`. Copy that whole
address and paste it into any browser's address bar by hand.

### The folder looks empty, or I can't find `software_installation` inside it

Make sure you used **Extract All** (right-click the `.zip` →
**Extract All...**) rather than just double-clicking to peek inside —
double-clicking opens a "compressed folder" preview that *looks* like
a real folder but isn't, and running scripts from inside it fails in
confusing ways. The real, extracted folder is named
**`OMIS-105-main`**.

### A path is "too long" error while installing or unzipping

Older Windows versions can fail on file paths longer than 260
characters. Extract the ZIP closer to your drive root (for example,
`C:\OMIS105\` instead of several folders deep inside Downloads) to
keep the full path short.

### Everything from Step 1/Step 2 troubleshooting

Package install errors (permission denied, `pip` not found, Marimo not
launching, multiple Python installs) are covered in
[`step_1_install_python_windows.md`](step_1_install_python_windows.md#troubleshooting)
— check there first if your problem is about Python packages rather
than Java or qStudio.

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Install Java 21 (winget) | `winget install EclipseAdoptium.Temurin.21.JDK` |
| Check Java version | `java -version` |
| Check where a command lives / list every copy on PATH | `where python` / `where java` |
| Open environment variables editor | `Win` key → search "environment variables" |

---

## Getting Help

If you've tried the steps above and are still stuck:

1. Take a **screenshot** of the error message
2. Note your **Windows version** (Settings → System → About)
3. Bring both to **office hours** (see
   [`course_information/QUESTIONS_and_OFFICE_HOURS.md`](../course_information/QUESTIONS_and_OFFICE_HOURS.md))
   or post on the course discussion board

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
