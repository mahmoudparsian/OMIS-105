# Create a DuckDB Database from SQL Files — macOS

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
2. [Open Terminal in the right folder](#2-open-terminal-in-the-right-folder)
3. [Method A: run the files inside DuckDB](#3-method-a-run-the-files-inside-duckdb)
4. [Method B: one command from Terminal](#4-method-b-one-command-from-terminal)
5. [Check your database](#5-check-your-database)
6. [Start over (rebuild from scratch)](#6-start-over-rebuild-from-scratch)
7. [Use the database later](#7-use-the-database-later)
8. [Troubleshooting](#8-troubleshooting)
9. [Quick reference](#9-quick-reference)

---

## 1. Before you start

**Two prompts, two kinds of commands.** You will type in two places:

| Where you are | The prompt looks like | Examples |
|---|---|---|
| Terminal (the shell) | `%` or `$` | `cd`, `ls`, `duckdb` |
| DuckDB | `D` | `.read`, `SHOW TABLES;`, `.quit` |

Do **not** type the prompt itself (`%`, `$`, or `D`). Copy only the command.

**Check that DuckDB is installed.** Open **Terminal** (press `Cmd + Space`,
type `Terminal`, press Return) and run:

```bash
duckdb --version
```

You should see a version number, such as `v1.5.5`. If you see
`zsh: command not found: duckdb`, install DuckDB first:

```bash
brew install duckdb
```

(Full install help is in the tutorial *DuckDB from the Command Line —
macOS*, in the `tutorials/DuckDB_from_Command_Line/` folder.)

---

## 2. Open Terminal in the right folder

DuckDB looks for `db_schema.sql` and `db_records.sql` in your **current
folder**. So first, move Terminal into the folder that holds them.

**Easiest way:** type `cd` and a space, then **drag the folder** from Finder
into the Terminal window. macOS types the full path for you. Press Return.

```bash
cd /Users/yourname/Downloads/Create_DuckDB_Database_from_SQL_Files
```

If the path has spaces, keep it inside quotes:

```bash
cd "/Users/yourname/Documents/OMIS 105/Create_DuckDB_Database_from_SQL_Files"
```

**Confirm** that both files are here:

```bash
ls *.sql
```

Expected output:

```text
db_records.sql	db_schema.sql
```

If you see `zsh: no matches found: *.sql`, you are in the wrong folder. Repeat the `cd`
step.

---

## 3. Method A: run the files inside DuckDB

Use this method when you are learning. You see each step happen.

### Step 1 — Open (and create) the database file

```bash
duckdb my_database.duckdb
```

If `my_database.duckdb` does not exist yet, DuckDB creates it. The prompt
changes to `D`. You are now inside DuckDB.

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

(`.exit` and `Ctrl + D` also work.) Your tables are saved in
`my_database.duckdb`. You are back at the Terminal prompt.

---

## 4. Method B: one command from Terminal

Use this method when you already know the files are correct. It builds the
database in one line, without entering DuckDB:

```bash
duckdb my_database.duckdb -c ".read db_schema.sql" -c ".read db_records.sql"
```

How it works:

- `-c` means "run this command." After the last `-c`, DuckDB exits.
- The two `-c` commands run **in order**, left to right.
- If the first one fails, DuckDB **stops** and does not run the second.
  This protects you from a half-built database.
- No output means success.

**Older style (also works on Mac):** you may see input redirection with `<`
in other tutorials:

```bash
duckdb -bail my_database.duckdb < db_schema.sql
duckdb -bail my_database.duckdb < db_records.sql
```

Always add `-bail` with `<`. Without it, DuckDB **skips a failed statement
and keeps going**. You could end up with some rows missing and no clear
warning. The `-c ".read ..."` command above does not have this problem, so
prefer it.

---

## 5. Check your database

Open the database again:

```bash
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
The first two lines are typed in Terminal; the rest is typed at the `D`
prompt. The two highlighted lines load your SQL files into the database.

<pre>
% rm -f my_database.duckdb my_database.duckdb.wal
% duckdb my_database.duckdb
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
Marimo notebook that uses this file. Then, in Terminal:

```bash
rm -f my_database.duckdb my_database.duckdb.wal
duckdb my_database.duckdb -c ".read db_schema.sql" -c ".read db_records.sql"
```

- `rm` deletes files **permanently** (they do not go to the Trash).
  Double-check the file name before you press Return.
- `-f` means "no error if the file is already gone."
- The `.wal` file is a temporary helper file. It may or may not exist.

Rebuild from scratch any time you **edit** `db_schema.sql` or
`db_records.sql`.

---

## 7. Use the database later

**From Terminal:**

```bash
cd /path/to/your/folder
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

**Important:** if you run `duckdb my_database.duckdb` **without** the file
name — just `duckdb` — you get a temporary **in-memory** database.
Everything in it disappears when you quit.

---

## 8. Troubleshooting

| What you see | What it means | What to do |
|---|---|---|
| `zsh: command not found: duckdb` | DuckDB is not installed, or Terminal cannot find it | Run `brew install duckdb`, then open a **new** Terminal window |
| `Error: cannot open "db_schema.sql"` | DuckDB cannot find the file in the current folder | `.quit`, then `cd` to the right folder and check with `ls *.sql` |
| `Catalog Error: Table with name "..." already exists!` | You ran `db_schema.sql` twice | Rebuild from scratch ([Section 6](#6-start-over-rebuild-from-scratch)) |
| `Constraint Error: Duplicate key ... violates primary key constraint` | You ran `db_records.sql` twice, or the file has a repeated key | Rebuild from scratch. If it happens on a clean build, fix the repeated value in the file |
| `Catalog Error: Table with name ... does not exist!` | You ran `db_records.sql` before `db_schema.sql` | Rebuild from scratch, running the schema file **first** |
| `IO Error: Could not set lock on file ... Conflicting lock is held` | Another program has the database open (another Terminal, or a Marimo notebook) | Close the other program, or `.quit` in the other Terminal, then try again |
| `Parser Error: syntax error at or near ...` | A typo in the SQL file, or a missing `;` | Open the file in a text editor, fix the line named in the error, then rebuild |
| You press Return and nothing happens; the prompt changed | DuckDB is waiting for the end of a SQL statement | Type `;` and press Return |
| `SHOW TABLES;` shows nothing | You opened a different file, or no file (in-memory) | `.quit`, check you are in the right folder, and open `duckdb my_database.duckdb` |

**Editing SQL files on a Mac:** use a plain-text editor such as VS Code.
If you use TextEdit, choose **Format → Make Plain Text** first, or the file
will be saved as rich text and DuckDB cannot read it.

---

## 9. Quick reference

```bash
# 1. Go to the folder with your SQL files
cd /path/to/your/folder
ls *.sql

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

```bash
# Rebuild from scratch (close DuckDB and Marimo first)
rm -f my_database.duckdb my_database.duckdb.wal
duckdb my_database.duckdb -c ".read db_schema.sql" -c ".read db_records.sql"
```

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
