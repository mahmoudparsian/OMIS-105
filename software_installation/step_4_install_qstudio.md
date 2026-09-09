# OMIS 105 <br> How to Install qStudio

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
| Operating system | macOS, Windows, or Linux |
| Internet connection | Required for download |
| Disk space | ~100 MB |

---

## Step 1 — Download qStudio

1. Open your web browser and go to: **https://www.timestored.com/qstudio/download/**
2. Click the download button for your operating system:
   - **Mac:** "Download .App Mac with Java" (downloads a `.zip` file)
   - **Windows:** "Download Installer for Windows" (downloads an `.exe` file)
3. The file will download to your Downloads folder

---

## Step 2 — Install qStudio

### Mac

1. Find **`qstudio-mac.zip`** in your Downloads folder and double-click it — macOS unzips it automatically into an app called **QStudio**
2. Drag **QStudio** into the **Applications** folder
3. Open **Applications** and double-click **QStudio**
4. If macOS says the app is from an "unidentified developer":
   - Go to **System Settings → Privacy & Security**
   - Scroll down and click **"Open Anyway"** next to the qStudio message
   - Click **Open** in the confirmation dialog

### Windows

1. Open the downloaded `.exe` installer
2. Click **Next** through the setup screens
3. Click **Install**
4. When the installation finishes, click **Finish**
5. qStudio should now appear in your Start menu

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

Type this in the query editor and press **Ctrl+E** (Windows) or **Cmd+E** (Mac):

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

Select all three statements and press **Ctrl+E** / **Cmd+E**. You should see Alice and Bob. Expand the connection in the left panel and you will see `test_students` listed there.

### Running Queries

**Use this one — it always works:**

| OS | Shortcut | What it runs |
|----|----------|-------------|
| Windows | **Ctrl+E** | The highlighted text. If nothing is highlighted, the **whole editor** |
| Mac | **Cmd+E** | Same |

So: highlight the statement you want, press it. Highlight nothing, and the whole file runs.

Windows users have a second option — **Ctrl+Q** runs just the one statement your cursor is sitting in, without highlighting anything.

> **Mac users: do not try Cmd+Q for this.** On macOS, `Cmd+Q` quits the
> application. Stick with **Cmd+E** and highlight what you want to run.

In general, qStudio's own documentation writes shortcuts with `Ctrl`, and on a Mac you use `Cmd` instead — with `Cmd+Q` as the exception above.

---

## Step 4 — Opening an Existing Database File (Optional)

To open a `.duckdb` file you already have — one you made earlier, or one handed out in class:

1. Go to **File → Open Database (sqlite/duckdb/h2)**
2. Pick the `.duckdb` file
3. Click **Open**

On Windows, if you installed with the installer, you can also just double-click a `.duckdb` file and it opens in qStudio.

qStudio also ships with a built-in example: **File → Open DuckDB Example .sql**.

---

## Troubleshooting

### qStudio won't open on Mac ("unidentified developer")

This is a macOS security feature. Go to **System Settings → Privacy & Security**, find the message about qStudio, and click **"Open Anyway"**.

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
| Open qStudio | Applications (Mac) or Start menu (Windows) |
| Create a DuckDB database | File → New DuckDB Database |
| Open an existing `.duckdb` file | File → Open Database (sqlite/duckdb/h2) |
| Run the highlighted text (main one) | Ctrl+E (Win) / Cmd+E (Mac) |
| Run the statement at the cursor | Ctrl+Q — **Windows only** (Cmd+Q quits on Mac) |
| Browse tables | Expand the database in the left panel |

---

## Getting Help

If you've tried the troubleshooting steps above and are still stuck:

1. Take a **screenshot** of the error message
2. Note your **operating system** and **qStudio version** (Help → About)
3. Bring both to **office hours** or post on the course discussion board

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
