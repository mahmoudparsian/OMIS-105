# Create a DuckDB Database from SQL Files — Windows

This guide shows you how to build a **database file** called
`my_database.duckdb` from two SQL files:

| File | What it contains | Run it |
|---|---|---|
| `db_schema.sql` | `CREATE TABLE` statements — the structure | **First** |
| `db_records.sql` | `INSERT` statements — the rows | **Second** |

A database file is **persistent**: your tables stay saved after you close
DuckDB. You can open the same file again tomorrow, or from a Marimo
notebook.

This folder includes a small practice `db_schema.sql` and `db_records.sql`
(2 tables: `departments` and `employees`). Use them the first time.
Later, the same steps work with any pair of SQL files.

Examples use **DuckDB 1.5.5**. A newer version is fine.

---

## Contents

1. [Before you start](#1-before-you-start)
2. [Open PowerShell in the right folder](#2-open-powershell-in-the-right-folder)
3. [Method A: run the files inside DuckDB](#3-method-a-run-the-files-inside-duckdb)
4. [Method B: one command from PowerShell](#4-method-b-one-command-from-powershell)
5. [Check your database](#5-check-your-database)
6. [Start over (rebuild from scratch)](#6-start-over-rebuild-from-scratch)
7. [Use the database later](#7-use-the-database-later)
8. [Troubleshooting](#8-troubleshooting)
9. [Quick reference](#9-quick-reference)

---

## 1. Before you start

This guide uses **PowerShell**, the standard command window on Windows 10
and 11. To open it: press the **Windows** key, type `PowerShell`, and press
Enter. (Windows Terminal also works: it opens PowerShell by default.)

**Two prompts, two kinds of commands.** You will type in two places:

| Where you are | The prompt looks like | Examples |
|---|---|---|
| PowerShell (the shell) | `PS C:\Users\yourname>` | `cd`, `dir`, `duckdb` |
| DuckDB | `D` | `.read`, `SHOW TABLES;`, `.quit` |

Do **not** type the prompt itself (`PS C:\...>` or `D`). Copy only the
command.

**Check that DuckDB is installed.** In PowerShell, run:

```powershell
duckdb --version
```

You should see a version number, such as `v1.5.5`. If you see
`duckdb : The term 'duckdb' is not recognized ...`, install DuckDB first:

```powershell
winget install --id DuckDB.cli --exact
```

Then **close PowerShell and open a new window**, so it can find the new
program. (Full install help is in the tutorial *DuckDB from the Command
Line — Windows*, in the `tutorials/DuckDB_from_Command_Line/` folder.)

---

## 2. Open PowerShell in the right folder

DuckDB looks for `db_schema.sql` and `db_records.sql` in your **current
folder**. So first, move PowerShell into the folder that holds them.

**Easiest way:**

1. In File Explorer, find the folder that holds the two `.sql` files.
2. Hold **Shift**, right-click the folder, and choose **Copy as path**.
   (On Windows 11 you can also right-click and choose **Copy as path**
   directly.)
3. In PowerShell, type `cd` and a space, press `Ctrl + V` to paste, then
   press Enter. The copied path already includes the quotes.

```powershell
cd "C:\Users\yourname\Downloads\Create_DuckDB_Database_from_SQL_Files"
```

Keep the quotes. They are required when the path has spaces, and they do
no harm when it does not.

**Confirm** that both files are here:

```powershell
dir *.sql
```

You should see `db_records.sql` and `db_schema.sql` in the list. If you
see `Cannot find path` or an empty result, you are in the wrong folder.
Repeat the `cd` step.

**Watch out for hidden file extensions.** File Explorer hides extensions
by default, so a file that *looks* like `db_schema.sql` may really be
`db_schema.sql.txt`. The `dir` command always shows the real name. To see
extensions in File Explorer, choose **View → Show → File name extensions**
(Windows 11) or tick **File name extensions** on the **View** tab
(Windows 10).

**Avoid OneDrive folders if you can.** If your path contains `OneDrive`,
syncing can lock the database file while you work. A local folder such as
`C:\Users\yourname\OMIS105` is safer.

---

## 3. Method A: run the files inside DuckDB

Use this method when you are learning. You see each step happen.

### Step 1 — Open (and create) the database file

```powershell
duckdb my_database.duckdb
```

If `my_database.duckdb` does not exist yet, DuckDB creates it. The prompt
changes to `D`. You are now inside DuckDB.

Tip: always use a simple file name like `my_database.duckdb` here, with no
folder path, after you `cd` into the folder. That avoids backslash and
quoting problems.

### Step 2 — Run the two SQL files, in order

Type these at the `D` prompt, one at a time:

```sql
.read db_schema.sql
.read db_records.sql
```

The order matters. `db_records.sql` inserts rows into tables that
`db_schema.sql` creates.

If nothing prints, that is good news: **no message means success.**
If a file has an error, DuckDB prints it and stops reading that file.
See [Troubleshooting](#8-troubleshooting).

Notes on `.read`:

- Commands that start with a dot (`.read`, `.tables`, `.quit`) are DuckDB
  **dot commands**. They do **not** end with a semicolon.
- SQL statements (`SELECT`, `SHOW TABLES`) **do** end with a semicolon.

### Step 3 — Check the result

```sql
SHOW TABLES;
```

Expected output:

```text
┌─────────────┐
│    name     │
│   varchar   │
├─────────────┤
│ departments │
│ employees   │
└─────────────┘
```

For a full check, see [Section 5](#5-check-your-database).

### Step 4 — Leave DuckDB

```sql
.quit
```

(`.exit` also works.) Your tables are saved in `my_database.duckdb`.
You are back at the PowerShell prompt.

---

## 4. Method B: one command from PowerShell

Use this method when you already know the files are correct. It builds the
database in one line, without entering DuckDB:

```powershell
duckdb my_database.duckdb -c ".read db_schema.sql" -c ".read db_records.sql"
```

How it works:

- `-c` means "run this command." After the last `-c`, DuckDB exits.
- The two `-c` commands run **in order**, left to right.
- If the first one fails, DuckDB **stops** and does not run the second.
  This protects you from a half-built database.
- No output means success.

**Do not use `<` in PowerShell.** Some tutorials show this:

```text
duckdb my_database.duckdb < db_schema.sql
```

PowerShell does not support `<` for input. It stops with this error:

```text
The '<' operator is reserved for future use.
```

The `-c ".read ..."` command above is the correct way on Windows. It also
works the same in the older **Command Prompt** (`cmd`) window.

---

## 5. Check your database

Open the database again:

```powershell
duckdb my_database.duckdb
```

Then run these checks at the `D` prompt:

```sql
SHOW TABLES;

SELECT 'departments' AS table_name, COUNT(*) AS row_count FROM departments
UNION ALL
SELECT 'employees', COUNT(*) FROM employees;

SELECT * FROM employees LIMIT 3;
```

With the practice files, you should see **3** departments and **6**
employees:

```text
┌─────────────┬───────────┐
│ table_name  │ row_count │
│   varchar   │   int64   │
├─────────────┼───────────┤
│ departments │         3 │
│ employees   │         6 │
└─────────────┴───────────┘
```

### A complete example session

Here is the whole process in one place, with the practice files: delete
any old copy, create the database, load both files, and check the result.
The first two lines are typed in PowerShell; the rest is typed at the `D`
prompt. The two highlighted lines load your SQL files into the database.

<pre>
PS C:\OMIS105&gt; Remove-Item my_database.duckdb, my_database.duckdb.wal -ErrorAction SilentlyContinue
PS C:\OMIS105&gt; duckdb my_database.duckdb
DuckDB v1.5.5 (Variegata)
Enter ".help" for usage hints.
<mark><b>D .read db_schema.sql</b></mark>
<mark><b>D .read db_records.sql</b></mark>
D SHOW TABLES;
┌─────────────┐
│    name     │
│   varchar   │
├─────────────┤
│ departments │
│ employees   │
└─────────────┘
D .schema
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name VARCHAR NOT NULL UNIQUE, "location" VARCHAR NOT NULL);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, "name" VARCHAR NOT NULL, salary INTEGER NOT NULL, dept_id INTEGER, CHECK((salary &gt; 0)), FOREIGN KEY (dept_id) REFERENCES departments(dept_id));
D SELECT * FROM departments;
┌─────────┬─────────────┬─────────────┐
│ dept_id │  dept_name  │  location   │
│  int32  │   varchar   │   varchar   │
├─────────┼─────────────┼─────────────┤
│      10 │ Sales       │ San Jose    │
│      20 │ Engineering │ Santa Clara │
│      30 │ Marketing   │ Palo Alto   │
└─────────┴─────────────┴─────────────┘
D SELECT * FROM employees;
┌────────┬─────────┬────────┬─────────┐
│ emp_id │  name   │ salary │ dept_id │
│ int32  │ varchar │ int32  │  int32  │
├────────┼─────────┼────────┼─────────┤
│      1 │ Alice   │  95000 │      20 │
│      2 │ Bob     │  72000 │      10 │
│      3 │ Chen    │  88000 │      20 │
│      4 │ Diana   │  67000 │      30 │
│      5 │ Omar    │  70000 │      10 │
│      6 │ Priya   │  99000 │    NULL │
└────────┴─────────┴────────┴─────────┘
D .quit
</pre>

What to notice:

- The first line deletes any old `my_database.duckdb`, so you start clean.
  Without it, `.read db_schema.sql` fails with "already exists" if you
  built the database earlier. (Close DuckDB and any Marimo notebook that
  uses the file before you delete it.)
- The two `.read` lines print nothing. No message means success.
- `.schema` (a dot command, no semicolon) prints the `CREATE TABLE`
  statement for every table. DuckDB stores them in its own style, so they
  look a little different from `db_schema.sql`. For example, `INT` becomes
  `INTEGER`. They mean the same thing.
- Priya's `dept_id` is `NULL`. She is not in any department yet. The
  foreign key allows this, because `dept_id` is not marked `NOT NULL`.
- Your version number may be newer. Some setups also print extra lines,
  such as `Run Time (s): ...`. That is normal.

Useful extra checks:

- `DESCRIBE employees;` — lists each column and its data type.
- `.tables` — a short list of the tables (a dot command, no semicolon).

When you finish, type `.quit`.

---

## 6. Start over (rebuild from scratch)

`db_schema.sql` uses `CREATE TABLE`. If you run it a second time on the same
database, you get:

```text
Catalog Error: Table with name "departments" already exists!
```

And if you run `db_records.sql` twice, you get duplicate-key errors.

This is normal. The clean fix is to **delete the database file and build
it again**. First make sure DuckDB is closed (`.quit`), and close any
Marimo notebook that uses this file. Then, in PowerShell:

```powershell
Remove-Item my_database.duckdb, my_database.duckdb.wal -ErrorAction SilentlyContinue
duckdb my_database.duckdb -c ".read db_schema.sql" -c ".read db_records.sql"
```

- `Remove-Item` deletes files **permanently** (they do not go to the
  Recycle Bin). Double-check the file name before you press Enter.
- `-ErrorAction SilentlyContinue` means "no error if a file is already
  gone."
- The `.wal` file is a temporary helper file. It may or may not exist.
- If you see `because it is being used by another process`, DuckDB or a
  notebook still has the file open. Close it, then try again.

Rebuild from scratch any time you **edit** `db_schema.sql` or
`db_records.sql`.

---

## 7. Use the database later

**From PowerShell:**

```powershell
cd "C:\path\to\your\folder"
duckdb my_database.duckdb
```

Your tables are still there. Type `.quit` when you finish.

**From a Marimo notebook or Python** (in the same folder as the file):

```python
import duckdb

con = duckdb.connect("my_database.duckdb", read_only=True)
con.execute("SELECT * FROM employees").fetchdf()
```

`read_only=True` lets you query safely, and it lets other programs read the
same file at the same time.

Python on Windows also accepts forward slashes in a full path, for example
`duckdb.connect("C:/Users/yourname/OMIS105/my_database.duckdb")`. Forward
slashes avoid backslash problems in Python strings.

**Important:** if you run `duckdb my_database.duckdb` **without** the file
name — just `duckdb` — you get a temporary **in-memory** database.
Everything in it disappears when you quit.

---

## 8. Troubleshooting

| What you see | What it means | What to do |
|---|---|---|
| `The term 'duckdb' is not recognized ...` | DuckDB is not installed, or PowerShell cannot find it | Run `winget install --id DuckDB.cli --exact`, then open a **new** PowerShell window |
| `Error: cannot open "db_schema.sql"` | DuckDB cannot find the file in the current folder | `.quit`, then `cd` to the right folder and check with `dir *.sql`. Also check for a hidden `.txt` extension |
| `Catalog Error: Table with name "..." already exists!` | You ran `db_schema.sql` twice | Rebuild from scratch ([Section 6](#6-start-over-rebuild-from-scratch)) |
| `Constraint Error: Duplicate key ... violates primary key constraint` | You ran `db_records.sql` twice, or the file has a repeated key | Rebuild from scratch. If it happens on a clean build, fix the repeated value in the file |
| `Catalog Error: Table with name ... does not exist!` | You ran `db_records.sql` before `db_schema.sql` | Rebuild from scratch, running the schema file **first** |
| `IO Error: Could not set lock on file ...` or `being used by another process` | Another program has the database open (another PowerShell window, a Marimo notebook, or OneDrive syncing) | Close the other program, or `.quit` in the other window, then try again. Move the folder out of OneDrive if it keeps happening |
| `The '<' operator is reserved for future use.` | You used `<` redirection, which PowerShell does not support | Use `-c ".read db_schema.sql"` instead ([Section 4](#4-method-b-one-command-from-powershell)) |
| `Parser Error: syntax error at or near ...` | A typo in the SQL file, or a missing `;` | Open the file in a text editor, fix the line named in the error, then rebuild |
| You press Enter and nothing happens; the prompt changed | DuckDB is waiting for the end of a SQL statement | Type `;` and press Enter |
| `SHOW TABLES;` shows nothing | You opened a different file, or no file (in-memory) | `.quit`, check you are in the right folder, and open `duckdb my_database.duckdb` |

**Editing SQL files on Windows:** use a plain-text editor such as VS Code
or Notepad. Do not use Word or WordPad. In Notepad, when you choose
**Save As**, set **Save as type** to **All files (\*.\*)** and type the full
name, such as `db_schema.sql`, or Notepad may add `.txt` to the end.

---

## 9. Quick reference

```powershell
# 1. Go to the folder with your SQL files
cd "C:\path\to\your\folder"
dir *.sql

# 2. Build the database (one line)
duckdb my_database.duckdb -c ".read db_schema.sql" -c ".read db_records.sql"

# 3. Open it and look around
duckdb my_database.duckdb
```

```sql
SHOW TABLES;
SELECT COUNT(*) FROM employees;
.quit
```

```powershell
# Rebuild from scratch (close DuckDB and Marimo first)
Remove-Item my_database.duckdb, my_database.duckdb.wal -ErrorAction SilentlyContinue
duckdb my_database.duckdb -c ".read db_schema.sql" -c ".read db_records.sql"
```

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
