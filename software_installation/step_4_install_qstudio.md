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

1. Find the downloaded `.zip` file in your Downloads folder and double-click it — macOS unzips it automatically into a **qStudio** app
2. Drag the **qStudio** app into the **Applications** folder
3. Open **Applications** and double-click **qStudio**
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

## Step 3 — Connect qStudio to DuckDB

qStudio can connect to many database types. For this course, we use DuckDB in-memory databases.

1. Launch qStudio
2. Go to **Server → Add Server** (or click the **+** icon in the connections panel)
3. In the **Server Type** dropdown, select **DuckDB**
4. Leave the connection settings as defaults (in-memory)
5. Click **Add** or **OK**

You should see the connection appear in the left panel. You can now type SQL in the editor and press **Ctrl+E** (Windows) or **Cmd+E** (Mac) to run it — this runs the highlighted text, or the whole editor if nothing is selected.

### Quick Test

Type this in the query editor and run it:

```sql
SELECT 'Hello, OMIS 105!' AS greeting, 42 AS answer;
```

If you see a result table with "Hello, OMIS 105!" — qStudio is working.

---

## Step 4 — Connecting to a DuckDB File (Optional)

In class we mostly use in-memory databases, but if you want to open a `.duckdb` file:

1. Go to **Server → Add Server**
2. Select **DuckDB** as the server type
3. In the **Database** field, enter the full path to your `.duckdb` file
4. Click **Add**

---

## Troubleshooting

### qStudio won't open on Mac ("unidentified developer")

This is a macOS security feature. Go to **System Settings → Privacy & Security**, find the message about qStudio, and click **"Open Anyway"**.

### qStudio won't connect to DuckDB

Make sure you selected **DuckDB** (not PostgreSQL, MySQL, etc.) as the server type. If qStudio's bundled DuckDB version is outdated, you can point it to your installed DuckDB — but for this course, the default settings should work.

### Queries run in qStudio but not in Marimo (or vice versa)

qStudio and Marimo use **separate** DuckDB connections. Tables you create in one are not visible in the other. This is expected — each tool has its own in-memory database.

### I don't see DuckDB in the Server Type dropdown

You may have an older version of qStudio. Go to **https://www.timestored.com/qstudio/download/** and download the latest version.

---

## Quick Reference Card

| Task | How |
|------|-----|
| Open qStudio | Applications (Mac) or Start menu (Windows) |
| Add a DuckDB connection | Server → Add Server → DuckDB |
| Run a query | Type SQL, then Ctrl+E (Win) or Cmd+E (Mac) |
| Browse tables | Expand the connection in the left panel |

---

## Getting Help

If you've tried the troubleshooting steps above and are still stuck:

1. Take a **screenshot** of the error message
2. Note your **operating system** and **qStudio version** (Help → About)
3. Bring both to **office hours** or post on the course discussion board

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
