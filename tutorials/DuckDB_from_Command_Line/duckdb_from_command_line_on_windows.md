---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: 'Segoe UI', Arial, sans-serif;
    background-color: #fff;
    color: #333;
  }
  section.lead {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #fff;
    text-align: center;
  }
  section.lead h1 {
    font-size: 2.4em;
    color: #ffd700;
  }
  section.lead h2 {
    color: #ccc;
    font-weight: 300;
  }
  h1 {
    color: #0f3460;
    border-bottom: 3px solid #ffd700;
    padding-bottom: 8px;
  }
  code {
    background: #f0f4f8;
    color: #0f3460;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.9em;
  }
  pre {
    background: #1a1a2e;
    border-radius: 8px;
    padding: 10px 16px;
    margin: 6px 0;
    color-scheme: dark;
  }
  pre code {
    background: transparent;
    color: #f0f4f8;
    padding: 0;
    font-size: 0.72em;
    line-height: 1.3;
  }
  table {
    font-size: 0.85em;
  }
  th {
    background: #0f3460;
    color: #fff;
  }
  strong {
    color: #0f3460;
  }
  blockquote {
    border-left: 4px solid #ffd700;
    background: #f9f9f0;
    padding: 12px 20px;
    font-style: italic;
  }
  section.closing {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #fff;
    text-align: center;
  }
  section.closing h1 {
    color: #ffd700;
    border: none;
  }
  section.lead strong,
  section.closing strong {
    color: #ffd700;
  }
  section.dense p {
    margin: 0.3em 0;
  }
  section.dense pre {
    margin: 4px 0;
    padding: 8px 14px;
  }
---

<!-- _class: lead -->

# DuckDB from the Command Line

## A Second Way to Talk to Your Database — Windows

---

# Table of Contents

1. Why Learn the Command Line?
2. Two Different "DuckDBs"
3. What You'll Need
4. Installing the DuckDB CLI on Windows
5. Verifying the Install
6. Starting DuckDB
7. The DuckDB Prompt
8. Dot-Commands — Your Toolbox
9. Changing How Results Look
10. Querying a CSV — No Loading Step
11. One-Off Queries and Script Files
12. Leaving DuckDB
13. Common Mistakes
14. Troubleshooting
15. More "What If...?" Scenarios
16. Cheat Sheet
17. Practice Exercise

---

# Why Learn the Command Line?

So far, you've used DuckDB **inside Marimo notebooks**. That's great
for building and sharing analysis.

The **command line** is different — it's a fast, no-frills way to:

- Quickly check a table without opening a notebook
- Run a `.sql` file as part of a script or pipeline
- Peek inside a `.csv` file in seconds
- Practice SQL the way many working analysts actually do

👉 Notebooks and the command line are **two tools for the same job**.
Knowing both makes you more flexible.

---

# Two Different "DuckDBs"

You already have the **DuckDB Python package** installed
(`pip install duckdb`). That's what powers `import duckdb` in Marimo.

Today we install a **second, separate thing**: the **DuckDB CLI** —
a standalone program called `duckdb.exe` that you run directly in a
terminal, with no Python involved at all.

| | Python package | DuckDB CLI |
|---|---|---|
| How you use it | `import duckdb` in a script/notebook | Type `duckdb` in a terminal |
| Needs Python? | Yes | No |
| Best for | Notebooks, analysis with pandas | Quick checks, scripts, learning SQL |

---

# What You'll Need

- A terminal — either works, but they behave a little differently:
  - **Command Prompt** (press `Win`, type `cmd`, press Enter)
  - **PowerShell** (press `Win`, type `powershell`, press Enter)
- Time to install the DuckDB CLI (allow extra time for package-manager setup)
- The sample file `data/students.csv` in this same tutorial folder
- **Windows 10 or 11**
- The [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)
  required by DuckDB; install the matching architecture if missing

That's it — no server, no account, no configuration file.

---

# Installing the DuckDB CLI — Option A: `winget` (recommended)

`winget` is Microsoft's package manager, delivered through **App
Installer** on supported Windows versions. It may be missing on some
devices. Check whether it is available:

```powershell
winget --version
```

**If that prints a version number**, install DuckDB with one command
(works the same in Command Prompt or PowerShell):

```powershell
winget install DuckDB.cli
```

Watch for a line ending in `Successfully installed`. If `winget` asks
you to accept a source agreement the first time you ever use it, type
`Y` and press Enter.

---

# Installing the DuckDB CLI — Option B: Manual Download

No `winget`, or it's blocked by school-managed device policy? Get the
binary directly:

1. Go to **duckdb.org/install** and choose **Windows** + **CLI**
2. Download the `.zip` (`duckdb_cli-windows-amd64.zip` for almost
   everyone — Windows on Arm is rare and out of scope for this course)
3. Right-click the downloaded `.zip` in **Downloads** and choose
   **Extract All...** — you get a single file named `duckdb.exe`
4. Move `duckdb.exe` somewhere permanent, e.g. create the folder
   `C:\duckdb\` and move it there
5. Add that folder to your **PATH** (next slide) so Windows can find
   `duckdb` from any folder

---

# Adding `duckdb.exe` to Your PATH

Only needed for the manual-download route — `winget` does this step
for you automatically.

1. Press `Win`, type **`environment variables`**, open **"Edit the
   system environment variables"**
2. Click the **"Environment Variables..."** button
3. Under **"User variables"**, select **`Path`**, click **"Edit..."**
4. Click **"New"**, type `C:\duckdb`, click **OK** on all three open
   windows
5. **Close every open Command Prompt / PowerShell window** — the PATH
   change only applies to *new* terminal windows

---

# "Windows protected your PC" — SmartScreen Warning

If Windows shows **“Windows protected your PC”**, SmartScreen may not
recognize the download's reputation. This is not proof that a file is
unsigned or malicious.

Verify that you downloaded it from **duckdb.org/install**. If permitted
by your device policy, use **“More info” → “Run anyway”** for the trusted
file. If that option is unavailable, contact IT.

`winget` is convenient, but it does not guarantee exemption from
SmartScreen or other managed-device security controls.

---

# Verifying the Install

**Open a brand-new** Command Prompt or PowerShell window (PATH
changes are not automatically loaded into existing shells), then run:

```
duckdb --version
```

The examples below use **DuckDB 1.5.5**. Your installed version may
differ; the installation commands are not pinned to 1.5.5.

Example output:

```text
v1.5.5 (Variegata) d8cdaa33fd
```

Confirm **where** it's running from:

```
where.exe duckdb
```

(`where.exe` works in both shells. PowerShell also provides
`Get-Command duckdb`; bare `where` means something different.)

---

# Starting DuckDB — In-Memory

Just type `duckdb` with nothing after it:

```
duckdb
```

```text
v1.5.5 (Variegata) d8cdaa33fd
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
D
```

The `D` is your **prompt** — DuckDB is waiting for a command.
**Do not type or paste the `D` shown in examples.**

⚠️ "In-memory" means: when you close this window, **everything you
created is gone**. Good for quick experiments.

---

# Starting DuckDB — Persistent File

To **save** your work to disk, give `duckdb` a filename:

```
duckdb my_class.db
```

- If `my_class.db` doesn't exist yet, DuckDB **creates** it.
- If it already exists, DuckDB **reopens** it — your tables are
  still there.

👉 This is exactly like the difference between
`duckdb.connect(':memory:')` and `duckdb.connect('my_class.db')`
in your Marimo notebooks.

An absolute Windows path also works. Forward slashes are a convenient
convention; Windows backslashes also work. Quote paths with spaces:

```
duckdb C:/Users/maria/Desktop/OMIS-105-LABS/my_class.db
```

(`maria` is a stand-in for your own username — on your PC it reads
`C:/Users/<your username>/...`.)

---

# The DuckDB Prompt

Once you see the `D` prompt, you can type SQL directly:

```sql
D SELECT 6 * 7 AS answer;
┌────────┐
│ answer │
│ int32  │
├────────┤
│     42 │
└────────┘
```

Press **Enter** after the `;` to run the statement.

---

# Don't Forget the Semicolon

If you forget the `;`, DuckDB just waits for more input:

```text
D SELECT 6 * 7 AS answer
   ...>
```

Type the `;` on the next line and press Enter to finish it.

⚠️ This is the #1 "why isn't anything happening?" moment for
beginners. When the prompt changes to `...>`, DuckDB is still
listening — it just needs your semicolon.

---

# Dot-Commands — Your Toolbox

Commands that start with a **dot (`.`)** are not SQL — they're
DuckDB CLI shortcuts. No semicolon needed.

```text
.help       show all dot-commands
.tables     list tables in the current database
.schema     show CREATE TABLE statements
.mode       change how results are displayed
.headers    show/hide column names
.timer      show how long each query took
.quit       exit the CLI
```

👉 Think of dot-commands as **settings for your session**, and SQL
as **questions for your data**.

---

# .tables and .schema

Create a table, add some rows, then inspect it:

```sql
D CREATE TABLE students (
    id INTEGER, 
    name VARCHAR, 
    gpa DOUBLE);
    
D INSERT INTO students VALUES
    (1, 'Alice', 3.8), (2, 'Bob', 3.5), 
    (3, 'Charlie', 3.9), (4, 'Diana', 3.2), 
    (5, 'Ethan', 2.9), (6, 'Fiona', 3.7),
    (7, 'George', 3.1), (8, 'Hana', 3.95);
D .tables
students
D .schema students
CREATE TABLE students(id INTEGER, name VARCHAR, gpa DOUBLE);
```

`.tables` answers *"what tables exist?"*
`.schema` answers *"what do they look like?"*

👉 The next few slides keep querying this same `students` table —
it stays alive for the rest of your session.

---

# .mode — Changing How Results Look

The default look (`duckbox`, shown so far) is nice to read, but not
easy to paste elsewhere. Switch styles with `.mode`:

```text
D .mode csv
D SELECT * FROM students LIMIT 2;
id,name,gpa
1,Alice,3.8
2,Bob,3.5
```

Other useful modes: `.mode markdown` (great for pasting into a
README), `.mode json`, `.mode line`. Switch back anytime with
`.mode duckbox`.

---

# .headers and .timer

```text
D .headers off
D SELECT name FROM students LIMIT 1;
Alice
```

```text
D .mode box
D .headers on
D .timer on
D SELECT COUNT(*) FROM students;
┌──────────────┐
│ count_star() │
├──────────────┤
│            8 │
└──────────────┘
Run Time (s): real 0.001 user 0.000539 sys 0.000315
```

`.timer on` is handy once your tables get big and you want to know
if a query is fast or slow.

---

<!-- _class: dense -->

# Querying a CSV — No Loading Step

This is DuckDB's superpower, and it works the same on the command
line as it does in a notebook. No `CREATE TABLE`, no import wizard —
the file **is** the table.

If you see `D`, exit with `.quit` first. Change to this tutorial's
folder in your shell (adjust the example to your actual repo location).

**Command Prompt:**
```bat
cd /d "%USERPROFILE%\Desktop\OMIS-105\tutorials\DuckDB_from_Command_Line"
cd
dir data
```

**PowerShell:**
```powershell
cd "$env:USERPROFILE\Desktop\OMIS-105\tutorials\DuckDB_from_Command_Line"
Get-Location
dir data
```

Run `duckdb` again, then `.mode box` and `.headers on` at `D`.

---

# Querying a CSV — Running the Query

```sql
D SELECT major, ROUND(AVG(gpa), 2) AS avg_gpa
  FROM read_csv('data/students.csv')
  GROUP BY major
  ORDER BY avg_gpa DESC, major;
```

```text
┌──────────────────────┬─────────┐
│         major        │ avg_gpa │
├──────────────────────┼─────────┤
│ Information Systems  │    3.83 │
│ Accounting           │    3.50 │
│ Finance              │    3.35 │
│ Marketing            │    3.35 │
└──────────────────────┴─────────┘
```

`'data/students.csv'` uses a **forward slash** and is a **relative
path** — it only resolves correctly if your terminal is standing in
this tutorial's folder (see the previous slide). DuckDB accepts
forward slashes on Windows even though File Explorer shows backslashes.

---

# One-Off Queries with `-c`

Sometimes you don't want to open the interactive prompt at all —
you just want **one quick answer**. Run it straight from your
terminal (not from inside `duckdb`) using `-c`.

**Command Prompt:**

```
duckdb -c "SELECT COUNT(*) FROM read_csv('data/students.csv')"
```

**PowerShell** (same syntax works too):

```powershell
duckdb -c "SELECT COUNT(*) FROM read_csv('data/students.csv')"
```

```text
┌──────────────┐
│ count_star() │
├──────────────┤
│            8 │
└──────────────┘
```

---

# Quoting on Windows — Command Prompt vs. PowerShell

Both shells accept the pattern above (**double quotes around the
whole SQL statement, single quotes inside for string literals** like
`'data/students.csv'` or `WHERE major = 'Finance'`), but they diverge
if you go further:

- **Command Prompt** has no concept of single-quoted strings at all —
  `'...'` is passed through literally, so keep using it *only* inside
  the double-quoted SQL, never as the outer quote.
- **PowerShell** treats single quotes (`'...'`) as **literal strings**
  (no variable expansion) and double quotes as **interpolating**
  strings (a `$name` inside would be substituted). This rarely bites
  you with `-c "SELECT ..."`, but if a query ever needs a literal `$`,
  use a `.sql` file to avoid shell quoting complexity.

---

# Running a Script File

**1. Create the file.** Open any plain-text editor (VS Code,
Notepad — not Word), type the SQL below, and save it as
`report.sql` in this same folder (choose **All files** in Notepad
and check that the name is not `report.sql.txt`):

```sql
SELECT major, COUNT(*) AS n
FROM read_csv('data/students.csv')
GROUP BY major;
```

**2. Run it.** Back in your terminal (not inside the `duckdb`
prompt):

```
duckdb -c ".read report.sql"
```

👉 `report.sql` is just text — DuckDB reads it and runs each
statement in order. Save once, rerun anytime: that's **repeatable**
SQL.

---

# Leaving DuckDB

Any of these will exit the interactive prompt:

```text
D .quit
```

```text
D .exit
```

Use `.quit` or `.exit` for a consistent exit across Windows terminals;
keyboard end-of-input behavior can depend on the CLI input mode.

⚠️ If you used an **in-memory** session, everything you built
disappears the moment you exit. Use a file
(`duckdb my_class.db`) if you want it to survive.

---

# Common Mistakes

- **Forgetting the `;`** → prompt hangs at `...>`. Type `;` + Enter.
- **Typing a dot-command with a `;`** → dot-commands don't need one
  (`.tables;` will error).
- **Leaving a file path unquoted in SQL** → use a SQL string:
  `read_csv('C:/Users/maria/data.csv')`. Forward slashes are a useful
  convention. Ordinary DuckDB SQL strings also preserve backslashes;
  they do not have Python's backslash-escape behavior.

---

# Common Mistakes (continued)

- **Using an in-memory session, then closing the window** →
  your table is gone. Use a `.db` file if you need it saved.
- **Running `duckdb` from the wrong folder** →
  `read_csv('data/students.csv')` only works if your terminal is in
  this tutorial's folder. Check with `cd` in Command Prompt or
  `Get-Location` in PowerShell.
- **Installed with `winget`, but `'duckdb' is not recognized`**
  (Command Prompt) **or `The term 'duckdb' is not recognized as the
  name of a cmdlet...`** (PowerShell) → same cause either way: you're
  still in the terminal window that was open *before* the install
  finished. Open a brand-new window.

---

# Troubleshooting

### `'duckdb' is not recognized as an internal or external command`

Seeing this in **PowerShell** instead? Same problem, different
wording: `The term 'duckdb' is not recognized as the name of a
cmdlet, function, script file, or operable program.` The fix below
is identical for both shells.

1. Open a **brand-new** Command Prompt or PowerShell window — PATH
   changes are not automatically loaded into existing shells.
2. If you installed manually, confirm the folder you added really
   contains `duckdb.exe`: `dir C:\duckdb`.
3. Re-check the PATH entry: `Win` → "environment variables" →
   "Edit the system environment variables" → "Environment
   Variables..." → confirm `C:\duckdb` is listed under the `Path`
   variable for your user.
4. As a sanity check, run `duckdb.exe` using its **full path** once:
   `C:\duckdb\duckdb.exe --version`. If that works, the PATH step
   above is the only thing left to fix.

---

# Troubleshooting (continued)

### SmartScreen keeps blocking `duckdb.exe`

See the SmartScreen slide earlier. If your managed device blocks the
file or does not offer **“Run anyway”**, ask IT for help. Installing
through `winget` does not override device security policy.

### My CSV query says "No files found that match the pattern"

Check the file exists and the path is correct. Show your current folder
with `cd` in Command Prompt or `Get-Location` in PowerShell. Use a
quoted absolute SQL path if needed: `read_csv('C:/path/data.csv')`.

---

# Troubleshooting (continued)

### OneDrive is messing with my path or file

If your Desktop or Documents folder is backed up by OneDrive (common
on school-managed laptops), your real path may include `OneDrive` in
it, e.g. `C:/Users/maria/OneDrive/Desktop/...`. Use File Explorer's
**"Copy as path"** on the actual folder rather than typing a path from
memory. OneDrive can also **lock** a `.db` file while syncing it,
which shows up as a confusing "unable to open database" error even
though the path is correct — if that keeps happening, work from a
non-synced folder such as `C:\OMIS105-LABS\` instead.

### `winget` itself isn't found, or refuses to run

`winget` ships with the **App Installer** package from the Microsoft
Store. On an older or locked-down Windows 10 install it may be
missing — update **App Installer** from the Microsoft Store, or use
Option B (manual download) instead.

---

# More "What If...?" Scenarios

- **Results table shows garbled characters like `Γöî` instead of
  clean lines?** → legacy Command Prompt's default codepage (437)
  doesn't support the Unicode box-drawing characters DuckDB draws by
  default. Don't reach for `chcp 65001` — it's been reported to make
  DuckDB CLI queries hang instead of fixing the display. Use
  `.mode table` instead: it prints a plain `+---+` table that doesn't
  depend on the codepage at all.

---

- **Display problems persist?** → try a normal (non-Administrator)
  terminal and `.mode table`. Record your DuckDB version and terminal
  version when seeking help; behavior can vary between releases.
- **Opening a `.db` file says `IO Error: Could not set lock on
  file...`?** → another terminal window — or a session you forgot to
  `.quit` — already has that file open; the message even names the
  PID holding it. Close that window, or run `.quit` there, then retry.

---

- **A manually downloaded `duckdb.exe` disappears?** → endpoint
  protection may have quarantined it. Check the security notification
  and ask IT if needed. A `winget` install does not normally place the
  executable in Downloads; use `where.exe duckdb` to locate it.
- **Folder name has spaces, like `C:\Users\maria\OMIS 105 Labs`?** →
  only the **shell** cares — quote it:
  `cd "C:\Users\maria\OMIS 105 Labs"`. A path written as a SQL string,
  like `'data/students.csv'`, needs no extra escaping.

---

- **"Edit the system environment variables" greyed out or blocked by
  school policy?** → you don't need admin rights for your **own**
  PATH — these steps already edit the **User variables** `Path`, not
  the System one. If even that's locked down, skip PATH for now: run
  `set PATH=%PATH%;C:\duckdb` (Command Prompt) or
  `$env:PATH += ";C:\duckdb"` (PowerShell) once per session, or just
  type `C:\duckdb\duckdb.exe` in full each time.

👉 None of these are common — but now you'll recognize them instantly
instead of guessing.

---

<!-- _class: dense -->

# Cheat Sheet

| Command | What it does |
|---|---|
| `winget install DuckDB.cli` | install the DuckDB CLI (recommended) |
| `duckdb --version` | confirm the install worked |
| `where.exe duckdb` | show which copy of `duckdb` will run |
| `duckdb` | start in-memory session |
| `duckdb file.db` | start/reopen a persistent database |
| `duckdb -c "SQL"` | run one query from your terminal, then exit |
| `duckdb -c ".read file.sql"` | run a whole script file |
| `.tables` | list tables |
| `.schema [table]` | show table structure |
| `.mode duckbox \| csv \| markdown \| json` | change output style |
| `.headers on \| off` | show/hide column names |
| `.timer on \| off` | show query run time |
| `.quit` / `.exit` | leave DuckDB |

---

# Practice Exercise

In your terminal, `cd` into this tutorial's folder, then:

1. Confirm the install: `duckdb --version` and `where.exe duckdb`
2. Start DuckDB: `duckdb`
3. Run: `SELECT * FROM read_csv('data/students.csv');`
4. Find the average GPA **per major**, highest first
5. Switch to `.mode markdown` and rerun your query
6. Save your query in a file called `my_query.sql`, then exit DuckDB
   with `.quit`
7. In Command Prompt or PowerShell, run
   `duckdb -c ".read my_query.sql"`

👉 If you can do all seven steps, you can use DuckDB from the command
line on Windows with confidence.

---

<!-- _class: closing -->

# You're Ready

Notebooks for building analysis.
The command line for quick answers and repeatable scripts.

**Resources**

https://duckdb.org/docs/stable/clients/cli/overview — Official CLI documentation
duckdb.org/install — Install DuckDB for Windows (winget or manual)

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
