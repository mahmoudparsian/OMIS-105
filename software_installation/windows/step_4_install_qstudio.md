# OMIS 105 <br> How to Install qStudio (Windows)

**Course:** OMIS 105 — Introduction to Database Management Systems  
**Quarter:** Fall 2026  
**Author:** Dr. Mahmoud Parsian  

---

## What Is qStudio?

qStudio is a free SQL editor that lets you write and run SQL queries against databases, including DuckDB. Think of it as a dedicated workbench for SQL — separate from the Marimo notebooks we use in class.

You will use qStudio to practice writing SQL queries on your own and to explore databases visually (browse tables, see column types, preview data).

| Item | Requirement |
|------|-------------|
| Software | qStudio (free, open-source) |
| Java | **Required** — qStudio will not run without it (Java 21 recommended) |
| Operating system | Windows 10 or Windows 11 |
| Internet connection | Required for download |
| Disk space | ~500 MB, plus ~200 MB for Java |

---

## Step 0 — Install Java (Required by qStudio)

qStudio is written in Java, and it will not open without a working
Java installed. **Install this before you try to open qStudio** —
skipping this step is the #1 reason qStudio fails to launch.

1. Open **Command Prompt** (press `Win`, type `cmd`, press Enter)
2. Install Java 21:

   ```
   winget install EclipseAdoptium.Temurin.21.JDK
   ```

3. Press **Y** if asked to accept a license agreement
4. Close Command Prompt completely, reopen it, and verify:

   ```
   java -version
   ```

   You should see something mentioning `21`.

> **`winget` not recognized?** See
> [`installation_trouble_shooting.md`](installation_trouble_shooting.md#1-qstudio-wont-open-because-it-cant-find-java)
> for a manual install option and the full walkthrough.

---

## Step 1 — Download qStudio

1. Open your web browser and go to: **https://www.timestored.com/qstudio/download/**
2. Click **"Download Installer for Windows"** — this downloads an `.exe` file
3. The file will download to your Downloads folder

---

## Step 2 — Install qStudio

1. Open the downloaded `.exe` installer
2. If you see **"Windows protected your PC"**, click **"More info"**, then **"Run anyway"** — this is normal for installers from smaller vendors, not a sign of a broken download
3. Click **Next** through the setup screens
4. Click **Install**
5. When the installation finishes, click **Finish**
6. qStudio should now appear in your Start menu

---

## Step 3 — Create a DuckDB Database

The DuckDB driver is **built into qStudio** — there is nothing extra to download.

Unlike Marimo, where we use an in-memory database that disappears when you close it, qStudio works with a DuckDB **file**. That is a good thing here: the tables you create stay put, so you can come back to them later.

1. Launch qStudio
2. Go to **File → New DuckDB Database**
3. Choose where to save it and give it a name, for example `omis105.duckdb`
4. Click **Save**

The new database appears in the panel on the left, and qStudio connects to it automatically.

### Quick Test

Type this in the query editor and press **Ctrl+E**:

```sql
SELECT 'Hello, OMIS 105!' AS greeting, 42 AS answer;
```

If you see a result table with "Hello, OMIS 105!" — qStudio is working.

Now try one that actually stores something:

```sql
CREATE OR REPLACE TABLE test_students (
    student_id INTEGER,
    name       VARCHAR,
    gpa        DECIMAL(3,2)
);

INSERT INTO test_students VALUES
    (1, 'Alice', 3.80),
    (2, 'Bob',   3.20);

SELECT * FROM test_students;
```

Select all three statements and press **Ctrl+E**. You should see Alice and Bob. Expand the connection in the left panel and you will see `test_students` listed there.

### Running Queries

**Use this one — it always works:**

| Shortcut | What it runs |
|----------|-------------|
| **Ctrl+E** | The highlighted text. If nothing is highlighted, the **whole editor** |

So: highlight the statement you want, press **Ctrl+E**. Highlight nothing, and the whole file runs.

You have a second option — **Ctrl+Q** runs just the one statement your cursor is sitting in, without highlighting anything.

---

## Step 4 — Opening an Existing Database File (Optional)

To open a `.duckdb` file you already have — one you made earlier, or one handed out in class:

1. Go to **File → Open Database (sqlite/duckdb/h2)**
2. Pick the `.duckdb` file
3. Click **Open**

If you installed with the installer, you can also just double-click a `.duckdb` file and it opens in qStudio.

qStudio also ships with a built-in example: **File → Open DuckDB Example .sql**.

---

## Troubleshooting

### qStudio won't open, or complains it can't find Java

This means Java isn't installed yet, or isn't the version qStudio
expects. Go back to **Step 0** above and install Java 21. If you've
already done that and it's still not working, see
[`installation_trouble_shooting.md`](installation_trouble_shooting.md#1-qstudio-wont-open-because-it-cant-find-java)
for less common causes (multiple Javas installed, broken PATH, etc.).

### "Windows protected your PC" when opening the installer

This is Windows SmartScreen, not a broken download — it appears
because the installer isn't from one of the handful of vendors Windows
recognizes by default. Click **"More info"**, then **"Run anyway"**.

### I don't see "New DuckDB Database" in the File menu

You may have an older version of qStudio. Go to
**https://www.timestored.com/qstudio/download/** and download the latest
version (5.08 or newer).

### My tables disappeared

Check which database is selected in the left panel. If you created a
second database, or opened a different `.duckdb` file, you are looking
at an empty one. Your tables are still in the file you made in Step 3.

### Tables I made in qStudio don't show up in Marimo (or the reverse)

That is expected, and worth understanding — it trips people up all
quarter.

Marimo uses an **in-memory** database that is created fresh every time
you run the notebook and vanishes when you close it. qStudio uses the
**file** you created in Step 3, which persists. They are two separate
databases and neither can see the other's tables.

### Nothing happens when I press Ctrl+E

Make sure a database is selected in the left panel first — qStudio needs
to know where to send the query. Also check that your cursor is in the
query editor, not in the results panel.

---

## Quick Reference Card

| Task | How |
|------|-----|
| Install Java | `winget install EclipseAdoptium.Temurin.21.JDK` |
| Check Java version | `java -version` |
| Open qStudio | Start menu |
| Create a DuckDB database | File → New DuckDB Database |
| Open an existing `.duckdb` file | File → Open Database (sqlite/duckdb/h2), or double-click the file |
| Run the highlighted text (main one) | Ctrl+E |
| Run the statement at the cursor | Ctrl+Q |
| Browse tables | Expand the database in the left panel |

---

## Getting Help

If you've tried the troubleshooting steps above and are still stuck:

1. Take a **screenshot** of the error message
2. Note your **Windows version** and **qStudio version** (Help → About)
3. Bring both to **office hours** or post on the course discussion board

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
