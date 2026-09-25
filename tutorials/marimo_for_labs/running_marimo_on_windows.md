# OMIS 105 <br> Running Marimo Notebooks & Connecting to DuckDB (Windows)

**Course:** OMIS 105 — Introduction to Database Management Systems
**Quarter:** Fall 2026
**Author:** Dr. Mahmoud Parsian

---

This page has two parts:

1. How to open and run a Marimo notebook file (`.py`), step by step.
2. How to connect that notebook to a DuckDB database — and how to
   write the file path correctly. This is where most Windows students
   get stuck, so read Part 2 carefully, even if Part 1 feels easy.

---

## Part 1 — Opening a Marimo Notebook

### Step 0 — Set up a LABS folder (one time only)

If you followed the [Git tutorial](../git/README.md), you already
cloned the course repo to your Desktop as `OMIS-105`. That folder is
**read-only** — you `git pull` it every week, and editing files inside
it causes conflicts. So labs live in a **separate** folder, right next
to it, that only you touch.

Open **Command Prompt** (press `Win`, type `cmd`, press Enter) and run:

```
mkdir "%USERPROFILE%\Desktop\OMIS-105-LABS"
copy "%USERPROFILE%\Desktop\OMIS-105\tutorials\marimo_for_labs\week_01_lab_02_sample.py" "%USERPROFILE%\Desktop\OMIS-105-LABS\"
```

`%USERPROFILE%` is a Windows shortcut that always means "my user
folder" — you never have to type your own username for it to work.

That copies this guide's sample notebook, **`week_01_lab_02_sample.py`**,
into your new working folder. From now on, every lab you copy from
`OMIS-105` goes into `OMIS-105-LABS` first — edit and run it there, not
inside the clone.

> **Downloaded the ZIP instead of using Git?** Your source folder is
> named `OMIS-105-main` and is probably in **Downloads**, not Desktop.
> Adjust the `copy` command's first path to match.

### Step 1 — Open Command Prompt in your LABS folder

**Easiest way — the address-bar trick:**

1. Open **File Explorer** and navigate to your `OMIS-105-LABS` folder.
2. Click once in the **address bar** at the top (the strip showing the
   folder path).
3. Type `cmd` and press Enter.

A Command Prompt opens **already pointed at that folder** — no typing
a path at all.

**Or manually:** open Command Prompt (`Win` → type `cmd` → Enter), then:

```
cd %USERPROFILE%\Desktop\OMIS-105-LABS
```

### Step 2 — Confirm you're in the right place

```
cd
dir
```

Plain `cd` (no arguments) prints the folder you're standing in. `dir`
lists the files in it — you should see `week_01_lab_02_sample.py` in that
list. If you don't, you're in the wrong folder — that is the #1 reason
the next step fails.

> **Folder or file name has spaces?** Wrap it in quotes:
> `cd "C:\Users\maria\Desktop\OMIS-105 LABS"`

### Step 3 — Run the notebook

```
marimo edit week_01_lab_02_sample.py
```

For any other lab, swap in that file's name — spelled **exactly** the
way `dir` showed it.

This should automatically open a new tab in your web browser with the
notebook running. Leave the Command Prompt window open — closing it
shuts the notebook down.

### If nothing opens in the browser

Look at the Command Prompt window — Marimo prints a line like:

```
http://localhost:2718/?access_token=...
```

Copy that **entire** line and paste it into your browser's address bar
by hand.

### Stopping the notebook

Click back on the Command Prompt window and press `Ctrl + C`. Closing
the browser tab alone does **not** stop it — the notebook keeps
running until you do this (or close the window).

### Common errors

| Error | What it means | Fix |
|---|---|---|
| `'marimo' is not recognized as an internal or external command` | Marimo isn't on your PATH | Try `python -m marimo edit week_01_lab_02_sample.py` instead |
| `The system cannot find the file specified` | You're in the wrong folder, or mistyped the file name | Run `dir` and check the spelling, then `cd` to the right folder |
| Browser tab says "unable to connect" | The notebook process stopped | Go back to Command Prompt and check for an error message; re-run Step 3 |

---

## Part 2 — Connecting to DuckDB

Inside your notebook, you connect to a database with one line of
Python:

```python
import duckdb
con = duckdb.connect(database=":memory:")
```

There are **two kinds** of connection. Picking the right one matters —
this is the difference between your tables disappearing when you close
the notebook, or staying there next time you open it.

### Option A — In-memory (temporary)

```python
con = duckdb.connect(database=":memory:")
```

`:memory:` is not a file — it tells DuckDB "don't save anything to
disk." Every table you create exists only while the notebook is
running. Close the notebook (or press `Ctrl+C`), and everything is
gone. Next time you open the notebook, you start empty again.

**Use this for:** in-class labs, practice, anything you re-run from
scratch each time (most of this course's labs use this).

### Option B — Persistent (a real file on disk)

```python
con = duckdb.connect(database="week_01_lab_02_sample.duckdb")
```

This creates a **file** on your disk named `week_01_lab_02_sample.duckdb`. Every
table you create is saved into that file. Close the notebook, come
back tomorrow, run `duckdb.connect(database="week_01_lab_02_sample.duckdb")` again —
your tables are still there.

**Use this for:** a semester project, or anything you want to build up
over multiple sessions.

### Example: A Persistent DuckDB Database URL (Windows)

**Step 1 — Copy the path the way Windows shows it** (File Explorer,
"Copy as path"). It uses **backslashes**:

```
C:\Users\maria\Desktop\OMIS-105-LABS\week_01_lab_02_sample.duckdb
```

**Step 2 — Replace every `\` with `/` before typing it into Python:**

```python
con = duckdb.connect(database="C:/Users/maria/Desktop/OMIS-105-LABS/week_01_lab_02_sample.duckdb")
```

Both strings point to the exact same file — Windows itself doesn't
care which slash you use. Python does: inside a quoted string, `\` is
an escape character, so a pasted backslash path can silently corrupt
itself (full explanation below, in **"The backslash problem"**). The
forward-slash version from Step 2 is the one to actually use in your
code.

Reading the URL left to right:

| Part | Meaning |
|---|---|
| `C:` | Your main drive |
| `/Users/maria` | Your user folder — replace `maria` with your own username |
| `/Desktop/OMIS-105-LABS` | The folder holding your lab files (Step 0) |
| `/week_01_lab_02_sample.duckdb` | The actual database file name |

---

### What is a database "path"?

The text you put inside the quotes — `"week_01_lab_02_sample.duckdb"` — is a
**path**. A path is just an address that tells DuckDB exactly where a
file lives on your computer, the same way a street address tells a
delivery driver exactly which house to go to.

There are two kinds:

| Type | Starts from | Example |
|---|---|---|
| **Relative path** | Wherever you launched `marimo edit` from | `week_01_lab_02_sample.duckdb` or `data/week_01_lab_02_sample.duckdb` |
| **Absolute path** | The very top of a drive (`C:\`) | `C:\Users\maria\Desktop\OMIS-105-LABS\week_01_lab_02_sample.duckdb` |

A **relative path** is short, but it only works if you launch the
notebook from the folder you expect — the folder you `cd`-ed into in
Part 1. If you `cd` somewhere else and run the same notebook,
`week_01_lab_02_sample.duckdb` might get created in a completely different — and
wrong — folder, or DuckDB might say it can't find the existing one.

An **absolute path** always points to the same file no matter where
you launched the notebook from. It's longer to type, but it's the
"bulletproof" option — recommended if you're at all unsure.

Throughout this guide, `maria` is a **stand-in example username** — on
your own laptop every `C:\Users\maria\...` path will actually read
`C:\Users\<your username>\...`. You don't need to know or type it
yourself for `%USERPROFILE%` or the steps below — they fill it in for
you automatically.

### How to get your exact absolute path on Windows

1. Open **File Explorer** and navigate to the folder that has (or will
   have) your database file.
2. Right-click the folder (in Windows 11, you may need "Show more
   options" first) and choose **"Copy as path"**.
3. Paste it somewhere you can edit it, e.g. Notepad. It will look like:

   ```
   "C:\Users\maria\Desktop\OMIS-105-LABS"
   ```

   Windows adds quotation marks — delete them.
4. Add your file name at the end. **Before you use it in Python, read
   the next section** — a raw pasted Windows path will break your code.

---

### The backslash problem — read this before you type a Windows path into Python

File Explorer shows paths with **backslashes**: `\`. That's just how
Windows displays them. But inside a Python string, the backslash is a
special character — it doesn't mean "backslash," it means "the next
character is special." For example `\n` means "start a new line" and
`\t` means "tab."

This causes a real, silent bug. Say your path is:

```
C:\Users\maria\newdata\week_01_lab_02_sample.duckdb
```

If you paste that directly into Python:

```python
# BROKEN — do not copy this
con = duckdb.connect(database="C:\Users\maria\newdata\week_01_lab_02_sample.duckdb")
```

Python sees `\n` inside `\newdata` and turns it into a newline
character. Your path is now silently corrupted — and depending on the
rest of the path, Python may even stop with an error like:
`(unicode error) 'unicodeescape' codec can't decode bytes`. Either way,
DuckDB cannot find your file, and the reason is invisible just from
looking at the text.

**You have three ways to fix this. Use #1 in this course — it's the
simplest and it always works:**

**1. Replace every `\` with `/` (recommended).**
DuckDB and Python both accept forward slashes on Windows just fine,
even though Windows itself displays backslashes:

```python
con = duckdb.connect(database="C:/Users/maria/newdata/week_01_lab_02_sample.duckdb")
```

**2. Put an `r` in front of the string** (a "raw string" — tells Python
to ignore the special meaning of `\`):

```python
con = duckdb.connect(database=r"C:\Users\maria\newdata\week_01_lab_02_sample.duckdb")
```

**3. Double every backslash:**

```python
con = duckdb.connect(database="C:\\Users\\maria\\newdata\\week_01_lab_02_sample.duckdb")
```

All three work. This course standardizes on **#1 (forward slashes)**
because it looks the same as the Mac version of this guide, and it's
the easiest one to type correctly by hand.

---

### Full example — persistent database with an absolute path

```python
import duckdb

con = duckdb.connect(database="C:/Users/maria/Desktop/OMIS-105-LABS/week_01_lab_02_sample.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE students (
        student_id INTEGER,
        name       VARCHAR,
        gpa        DECIMAL(3,2)
    )
""")

con.execute("INSERT INTO students VALUES (1, 'Alice', 3.80), (2, 'Bob', 3.20)")

con.execute("SELECT * FROM students").fetchdf()
```

Run this notebook once, close it, and reopen it later — `students`
is still there. Change the path to `":memory:"` and run it twice in a
row — `students` is empty the second time, because nothing was saved.

---

## Troubleshooting

### My path "looks right" but DuckDB can't find the file

You almost certainly have a raw backslash path pasted straight from
File Explorer. Go back to **"The backslash problem"** above and switch
every `\` to `/`.

### `IsADirectoryError` or "unable to open database"

The **folder** in your path doesn't exist yet. DuckDB will create the
`.duckdb` *file* for you automatically, but it will not create missing
*folders*. Double-check every folder in your path exists in File
Explorer, or use a plain file name like `"week_01_lab_02_sample.duckdb"` instead.

### My tables are empty every time I open the notebook

You're almost certainly using `:memory:`. Switch to a file path (Option
B above) if you want your tables to persist.

### "Conflicting lock is held" error

DuckDB only allows **one program at a time** to have a persistent
database file open for writing. This happens if you have the same
`.duckdb` file open in qStudio and Marimo at the same time — close one
of them.

### My relative path worked yesterday but not today

You probably launched `marimo edit` from a different folder this time.
Run plain `cd` in Command Prompt before running `marimo edit` and
confirm you're in the same folder as before — or switch to an absolute
path, which doesn't have this problem.

### OneDrive is messing with my path

If your Desktop or Documents folder is backed up by OneDrive (common on
school-managed laptops), your real path may include `OneDrive` in it,
e.g. `C:/Users/maria/OneDrive/Desktop/OMIS-105-LABS/week_01_lab_02_sample.duckdb`.
Always copy the path with "Copy as path" (see above) rather than typing
it from memory, so you get the real folder name.

OneDrive can also **lock** your `.duckdb` file while syncing it, which
shows up as a confusing "permission denied" or "file in use" error
even though your path is correct. If that keeps happening, move your
`OMIS-105-LABS` folder to a non-synced location such as `C:\OMIS105-LABS\`
and work from there — see
[`installation_trouble_shooting.md`](../../software_installation/windows/installation_trouble_shooting.md#files-behave-strangely-wont-save-or-give-permission-errors-inside-a-onedrive-folder)
for the full explanation.

---

## Quick Reference Card

| Task | Command / Path |
|---|---|
| Go to your notebook's folder | `cd %USERPROFILE%\Desktop\OMIS-105-LABS` |
| Confirm you're in the right folder | plain `cd` then `dir` |
| Open a notebook | `marimo edit week_01_lab_02_sample.py` |
| Stop a notebook | `Ctrl + C` in Command Prompt |
| In-memory connection (temporary) | `duckdb.connect(database=":memory:")` |
| Persistent connection (saved to disk) | `duckdb.connect(database="week_01_lab_02_sample.duckdb")` |
| Get an absolute path | File Explorer → right-click folder → "Copy as path" |
| Windows path as shown by File Explorer | Backslashes: `C:\Users\maria\Desktop\OMIS-105-LABS\week_01_lab_02_sample.duckdb` |
| **Windows path to actually type into Python** | Forward slashes: `C:/Users/maria/Desktop/OMIS-105-LABS/week_01_lab_02_sample.duckdb` |

---

## Getting Help

If you've tried the troubleshooting steps above and are still stuck:

1. Take a **screenshot** of the error message and the Command Prompt window.
2. Note the **exact command** you typed.
3. Bring both to **office hours** or post on the course discussion board.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
