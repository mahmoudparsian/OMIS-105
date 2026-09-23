# OMIS 105 <br> Installation Troubleshooting (Mac)

**Course:** OMIS 105 — Introduction to Database Management Systems  
**Quarter:** Fall 2026  
**Author:** Dr. Mahmoud Parsian

---

## What This Document Is

This document collects fixes for the problems Mac students actually
hit on the first day of class, beyond what's already covered in
[`step_1_install_python_macbook.md`](step_1_install_python_macbook.md)
and [`step_4_install_qstudio_macbook.md`](step_4_install_qstudio_macbook.md). Start
there first — come here when something still isn't working.

If your problem isn't listed here, take a screenshot of the error and
bring it to office hours (see the end of this document).

---

## 1. qStudio Won't Open Because It Can't Find Java

**Symptom:** qStudio fails to launch, or shows an error message
mentioning "Java" or "JRE" (Java Runtime Environment) when you double-click it.

qStudio needs Java to run. The Mac download from timestored.com is
labeled "with Java," but some students still saw this error — the
bundled Java didn't work on their Mac. The fix is to install your own
copy of Java. **Java 21 works fine for this course.**

### Step 1 — Install Homebrew

Homebrew is a package manager for Mac — a tool that installs other
software from the Terminal. You will use it to install Java.

1. Open **Terminal** (press `Cmd + Space`, type `Terminal`, press Enter)
2. Paste this command and press Enter:

   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. You may be asked for your Mac password. Type it (nothing will show
   on screen as you type — that's normal) and press Enter
4. If a popup asks to install the "Command Line Developer Tools,"
   click **Install** and wait for it to finish before continuing
5. Wait for the install to finish — it can take a few minutes

> **What does that command actually do?** It downloads Homebrew's
> official install script from GitHub and runs it. This is the
> standard, documented way to install Homebrew (see
> [brew.sh](https://brew.sh)) — you are not running a random script
> from a stranger.

### Step 2 — Add Homebrew to Your PATH

Right after Homebrew finishes installing, it prints a message that
looks like **"Next steps"** with 1–2 commands under it. **Run those
commands** — this step is what makes the `brew` command actually work.
If you already closed that message, here's what it says, depending on
your Mac:

**Apple Silicon Mac (M1 / M2 / M3 / M4 — most Macs sold since late 2020):**

```
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Intel Mac (older):**

```
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/usr/local/bin/brew shellenv)"
```

> **Not sure which kind of Mac you have?** Click the Apple menu →
> **About This Mac**. If it says "Chip: Apple M1/M2/M3/M4," use the
> Apple Silicon commands. If it says "Processor: Intel," use the Intel
> commands.

**Close Terminal completely** (`Cmd + Q`), reopen it, and type:

```
brew --version
```

If you see a version number (e.g., `Homebrew 4.x.x`), Homebrew is
installed and on your PATH.

### Step 3 — Install Java 21

```
brew update
brew install --cask temurin@21
```

This installs **Eclipse Temurin**, a free, standard build of Java.
Version 21 is what this course has confirmed works with qStudio.

### Step 4 — Verify Java

```
java -version
```

You should see something mentioning `21` (e.g., `openjdk version "21..."`).

> **`java -version` shows the wrong version, or an old one you didn't
> install?** You likely have more than one Java on your Mac (for
> example, one bundled inside another app). List every Java your Mac
> knows about:
>
> ```
> /usr/libexec/java_home -V
> ```
>
> This prints each installed version and its path. Find the line for
> `21`, then point your shell at it:
>
> ```
> echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 21)' >> ~/.zprofile
> ```
>
> Close Terminal completely, reopen it, and check `java -version` again.

### Step 5 — Open qStudio Again

Go back to **Applications** and double-click **QStudio**. It should
open normally now. If it still doesn't, quit qStudio completely and
try again — it sometimes needs a full restart to notice the new Java.

---

## 2. Putting Homebrew, Java, Python, Marimo, and DuckDB on Your PATH

**What is PATH?** PATH is a list of folders your Mac's Terminal
searches through when you type a command name. If a program's folder
isn't in that list, Terminal says `command not found` — even though
the program is installed and sitting right there on your disk.

You mostly won't need to do this by hand — the installers in this
course add themselves to PATH automatically. But here's what to do if
one of them doesn't, and where each tool normally lives:

| Tool | Normally added to PATH by | Typical folder |
|------|---------------------------|-----------------|
| Homebrew (`brew`) | Step 2 above | `/opt/homebrew/bin` (Apple Silicon) or `/usr/local/bin` (Intel) |
| Java (`java`) | Homebrew, automatically, once `brew` itself is on PATH | inside `/opt/homebrew/opt/temurin@21` or similar |
| Python (`python3`, `pip3`) | the python.org installer | `/usr/local/bin` or `/Library/Frameworks/Python.framework/...` |
| Marimo (`marimo`) | `pip3 install marimo` (Step 2 of the main setup) | wherever `pip3` installs command-line scripts for your Python |
| DuckDB (Python package) | `pip3 install duckdb` | not a command — it's a Python import, no PATH needed |

**If a command still says "not found" after installing it:**

1. Find out where it actually is:

   ```
   python3 -m site --user-base
   ```

   This prints a folder. The missing command is usually inside a
   `bin` subfolder there.

2. Add that `bin` folder to your PATH by appending an `export` line to
   your shell's startup file. Most Macs today use `zsh`, so edit
   `~/.zprofile`:

   ```
   echo 'export PATH="$HOME/Library/Python/3.12/bin:$PATH"' >> ~/.zprofile
   ```

   (Replace `3.12` with your actual Python version from
   `python3 --version`.)

3. Close Terminal completely (`Cmd + Q`), reopen it, and try the
   command again.

**To check where a command is currently coming from:**

```
which python3
which brew
which java
```

Each should print a file path. If it prints nothing, that tool is not
on your PATH yet.

---

## 3. Getting `step_2_setup_software.py` and `step_3_verification.py` Onto Your Mac

These two files live inside the course's GitHub repository, in the
`software_installation` folder. **Step 0** in
[`README.md`](README.md) covers this in full — here's the short
version:

1. Go to **https://github.com/mahmoudparsian/OMIS-105**
2. Click the green **`< > Code`** button, then **Download ZIP**
3. Find the ZIP in your **Downloads** folder and double-click it to unzip
4. Open the unzipped folder, then open **`software_installation`** —
   both files are inside

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

### A popup interrupted the Homebrew install asking about "Command Line Developer Tools"

This is normal and expected the first time you install Homebrew on a
Mac. Click **Install**, wait for the small installer to finish (a few
minutes), then re-run the Homebrew command from Step 1 above if it
didn't continue on its own.

### "zsh: command not found: brew" right after installing Homebrew

You installed Homebrew but skipped the PATH step. Go back to **Step 2**
above and run the two commands Homebrew printed for you.

### "xcrun: error: invalid active developer path" when running `brew` or `pip3`

This means the Xcode Command Line Tools are missing or broke, often
after a macOS update. Fix it by reinstalling them:

```
xcode-select --install
```

Click **Install** in the popup that appears and wait for it to finish.
If that command says the tools are "already installed" but the error
keeps happening, reset and reinstall:

```
sudo xcode-select --reset
xcode-select --install
```

### Homebrew (or a PATH change) fails with a permissions error, and this is a school-managed laptop

If your Mac is managed by SCU IT (an MDM profile, or you don't know
your own admin password), Homebrew and some PATH changes need admin
rights you may not have. This isn't something you can fix from the
Terminal — bring it to office hours so Dr. Parsian can help you find a
workaround or get an IT exception.

### Downloaded a new Python and package installs suddenly fail to build

If you installed the very newest Python version (released within the
last few weeks), some packages this course needs may not have a
ready-made install for it yet, and `pip` tries to compile it from
scratch — which fails without extra developer tools. Simplest fix:
uninstall it and install **Python 3.12** instead (still meets the
3.10+ requirement, and everything has ready-made installs for it). See
[`step_1_install_python_macbook.md`](step_1_install_python_macbook.md).

### `marimo edit` doesn't open a browser tab by itself

This can happen if your default browser is unusual or the app is
sandboxed. Look at the Terminal output — Marimo prints a line like
`http://localhost:2718/?access_token=...`. Copy that whole address and
paste it into any browser's address bar by hand.

### The unzipped folder looks empty, or I can't find `software_installation` inside it

Make sure you fully unzipped the file rather than just previewing it —
double-clicking a `.zip` on a Mac should extract it automatically into
a real folder sitting next to the `.zip`. If you see a folder with a
zipper icon, it isn't extracted yet; double-click it again. The real
folder is named **`OMIS-105-main`**.

### macOS says qStudio (or another app) is from an "unidentified developer"

This is Gatekeeper, a macOS security feature — not a broken download.

1. Go to **System Settings → Privacy & Security**
2. Scroll down to the message about the blocked app
3. Click **"Open Anyway"**
4. Click **Open** in the confirmation dialog

### `curl` or `pip3 install` fails with an SSL / certificate error

This usually happens on school or coffee-shop Wi-Fi that intercepts
secure connections (common on eduroam-style networks with a captive
portal or security software). Try:

- Switching to a different network (phone hotspot works well to test)
- If you're on a VPN, temporarily turning it off
- Retrying — some campus networks are just briefly unreliable

### My terminal doesn't show the `software_installation` folder when I run `ls`

Your Terminal isn't pointed at the right folder. Redo the drag-and-drop
trick in **Step 0** of [`README.md`](README.md) — type `cd ` (with a
trailing space), drag the `software_installation` folder from Finder
onto the Terminal window, then press Enter.

### I have more than one Python installed and things behave inconsistently

Check which one you're actually using:

```
which python3
```

If it doesn't point at the Python you installed in Step 1 (usually
under `/Library/Frameworks/Python.framework/` or `/usr/local/bin/`),
see the "I installed packages but Python can't find them" section in
[`step_1_install_python_macbook.md`](step_1_install_python_macbook.md#troubleshooting).

### Everything from Step 1/Step 2 troubleshooting

Package install errors (`externally-managed-environment`, permission
denied, `pip3` not found, Marimo not launching) are covered in
[`step_1_install_python_macbook.md`](step_1_install_python_macbook.md#troubleshooting)
— check there first if your problem is about Python packages rather
than Java or qStudio.

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Install Homebrew | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Add Homebrew to PATH (Apple Silicon) | `eval "$(/opt/homebrew/bin/brew shellenv)"` |
| Add Homebrew to PATH (Intel) | `eval "$(/usr/local/bin/brew shellenv)"` |
| Install Java 21 | `brew install --cask temurin@21` |
| Check Java version | `java -version` |
| List every Java installed | `/usr/libexec/java_home -V` |
| Check Homebrew is on PATH | `brew --version` |
| Check where a command lives | `which <command>` |
| Fix broken Xcode Command Line Tools | `xcode-select --install` |

---

## Getting Help

If you've tried the steps above and are still stuck:

1. Take a **screenshot** of the error message
2. Note your **macOS version** (Apple menu → About This Mac) and
   whether your Mac is **Apple Silicon or Intel**
3. Bring both to **office hours** (see
   [`course_information/QUESTIONS_and_OFFICE_HOURS.md`](../course_information/QUESTIONS_and_OFFICE_HOURS.md))
   or post on the course discussion board

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
