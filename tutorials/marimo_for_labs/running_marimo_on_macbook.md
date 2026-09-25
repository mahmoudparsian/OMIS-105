# OMIS 105 <br> Running Marimo Notebooks & Connecting to DuckDB (Mac)

**Course:** OMIS 105 — Introduction to Database Management Systems
**Quarter:** Fall 2026
**Author:** Dr. Mahmoud Parsian

---

This page has two parts:

1. How to open and run a Marimo notebook file (`.py`), step by step.
2. How to connect that notebook to a DuckDB database — and how to
   write the file path correctly, which is where most students get
   stuck.

---

## Part 1 — Opening a Marimo Notebook

### Step 0 — Set up a LABS folder (one time only)

If you followed the [Git tutorial](../git/README.md), you already
cloned the course repo to `~/Desktop/OMIS-105`. That folder is
**read-only** — you `git pull` it every week, and editing files inside
it causes conflicts. So labs live in a **separate** folder, right next
to it, that only you touch:

```
mkdir -p ~/Desktop/OMIS-105-LABS
cp ~/Desktop/OMIS-105/tutorials/marimo_for_labs/week_01_lab_02_sample.py ~/Desktop/OMIS-105-LABS/
```

That copies this guide's sample notebook, **`week_01_lab_02_sample.py`**,
into your new working folder. From now on, every lab you copy from
`OMIS-105` goes into `OMIS-105-LABS` first — edit and run it there, not
inside the clone.

### Step 1 — Open Terminal

Press `Cmd + Space`, type `Terminal`, press Enter.

### Step 2 — Go to your LABS folder

You must be **in the same folder as the `.py` file** before you run
Marimo. Use `cd` ("change directory") to get there:

```
cd ~/Desktop/OMIS-105-LABS
```

`~` is a shortcut for your home folder. Throughout this guide,
`/Users/maria` is a **stand-in example** — on your own Mac it will be
`/Users/<your username>`. You never have to type it yourself here,
since `~` fills it in automatically.

Check you're in the right place, and that the file is actually there:

```
pwd
ls
```

`pwd` prints the folder you're standing in. `ls` lists the files in
it — you should see `week_01_lab_02_sample.py` in that list. If you don't,
you're in the wrong folder — that is the #1 reason the next step fails.

> **Folder or file name has spaces?** Wrap it in quotes:
> `cd "~/Desktop/OMIS-105 LABS"`

### Step 3 — Run the notebook

```
marimo edit week_01_lab_02_sample.py
```

For any other lab, swap in that file's name — spelled **exactly** the
way `ls` showed it, including capital letters.

This should automatically open a new tab in your web browser with the
notebook running. Leave the Terminal window open — closing it shuts
the notebook down.

### If nothing opens in the browser

Look at the Terminal — Marimo prints a line like:

```
http://localhost:2718/?access_token=...
```

Copy that **entire** line and paste it into your browser's address bar
by hand.

### Stopping the notebook

Click back on the Terminal window and press `Ctrl + C`. Closing the
browser tab alone does **not** stop it — the notebook keeps running
until you do this (or quit Terminal).

### Common errors

| Error | What it means | Fix |
|---|---|---|
| `zsh: command not found: marimo` | Marimo isn't on your PATH | Try `python3 -m marimo edit week_01_lab_02_sample.py` instead |
| `No such file or directory` | You're in the wrong folder, or mistyped the file name | Run `ls` and check the spelling, then `cd` to the right folder |
| Browser tab says "unable to connect" | The notebook process stopped | Go back to Terminal and check for an error message; re-run Step 3 |

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

### Example: A Persistent DuckDB Database URL (Mac)

**Step 1 — Copy the path the way Finder shows it** (hold **Option**,
right-click the folder, "Copy as Pathname" — see below). On a Mac it
already uses **forward slashes**:

```
/Users/maria/Desktop/OMIS-105-LABS
```

**Step 2 — Add your file name and use it directly in Python:**

```python
con = duckdb.connect(database="/Users/maria/Desktop/OMIS-105-LABS/week_01_lab_02_sample.duckdb")
```

No conversion needed — unlike Windows, a Mac path already types
correctly as-is (see the Windows version of this guide if you're
curious why that's not true there).

Reading this URL left to right:

| Part | Meaning |
|---|---|
| `/Users/maria` | Your home folder — replace `maria` with your own username |
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
| **Absolute path** | The very top of your disk | `/Users/maria/Desktop/OMIS-105-LABS/week_01_lab_02_sample.duckdb` |

A **relative path** is short, but it only works if you launch the
notebook from the folder you expect — which is the folder you `cd`-ed
into in Part 1. If you `cd` somewhere else and run the same notebook,
`week_01_lab_02_sample.duckdb` might get created in a completely different — and
wrong — folder, or DuckDB might say it can't find the existing one.

An **absolute path** always points to the same file no matter where
you launched the notebook from. It's longer to type, but it's the
"bulletproof" option — recommended if you're at all unsure.

### How to get your exact absolute path on a Mac

1. Open **Finder** and navigate to the folder that has (or will have)
   your database file.
2. Right-click the folder, hold down the **Option (⌥)** key — the menu
   item changes to **"Copy '\<foldername\>' as Pathname"**. Click it.
3. Paste it into your code. It looks like:

   ```
   /Users/maria/Desktop/OMIS-105-LABS
   ```

4. Add your file name at the end:

   ```python
   con = duckdb.connect(database="/Users/maria/Desktop/OMIS-105-LABS/week_01_lab_02_sample.duckdb")
   ```

You can also get this by typing `pwd` in Terminal while standing in
that folder (see Part 1, Step 2).

### Mac paths always use forward slashes — good news

On a Mac, paths always use the forward slash `/`, and Python strings
never treat `/` as anything special. So Mac paths just work, exactly
as typed. (This is *not* true on Windows — see the Windows version of
this guide if you're helping a classmate who's on one.)

---

### Full example — persistent database with an absolute path

```python
import duckdb

con = duckdb.connect(database="/Users/maria/Desktop/OMIS-105-LABS/week_01_lab_02_sample.duckdb")

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

### `IsADirectoryError` or "unable to open database"

The **folder** in your path doesn't exist yet. DuckDB will create the
`.duckdb` *file* for you automatically, but it will not create missing
*folders*. Double-check every folder name in your path exists in
Finder, or remove the folders you haven't created and use a plain file
name like `"week_01_lab_02_sample.duckdb"` instead.

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
Run `pwd` in Terminal before running `marimo edit` and confirm you're
in the same folder as before — or switch to an absolute path, which
doesn't have this problem.

---

## Quick Reference Card

| Task | Command / Path |
|---|---|
| Go to your notebook's folder | `cd ~/Desktop/OMIS-105-LABS` |
| Confirm you're in the right folder | `pwd` then `ls` |
| Open a notebook | `marimo edit week_01_lab_02_sample.py` |
| Stop a notebook | `Ctrl + C` in Terminal |
| In-memory connection (temporary) | `duckdb.connect(database=":memory:")` |
| Persistent connection (saved to disk) | `duckdb.connect(database="week_01_lab_02_sample.duckdb")` |
| Get an absolute path | Finder → right-click folder → hold **Option** → "Copy as Pathname" |
| Mac path style | Forward slashes only: `/Users/maria/Desktop/OMIS-105-LABS/week_01_lab_02_sample.duckdb` |

---

## Getting Help

If you've tried the troubleshooting steps above and are still stuck:

1. Take a **screenshot** of the error message and the Terminal window.
2. Note the **exact command** you typed.
3. Bring both to **office hours** or post on the course discussion board.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
