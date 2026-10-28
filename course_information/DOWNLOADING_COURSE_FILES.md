# Downloading Course Files

## 📦 One ZIP File per Week — No Git Needed

You do **not** need git to get the course files. Each week of the
course is ready as **one ZIP file**. Click a link, unzip the file,
and you have everything for that week.

## ⬇️ Download Links

| Week | Topic | Download |
|------|-------|----------|
| 1 | Database Foundations | [`week01-database-foundations.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week01-database-foundations.zip) |
| 2 | Relational Modeling | [`week02-relational-modeling.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week02-relational-modeling.zip) |
| 3 | SQL Basics | [`week03-sql-basics.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week03-sql-basics.zip) |
| 4 | SQL Aggregation | [`week04-sql-aggregation.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week04-sql-aggregation.zip) |
| 5 | SQL Joins | [`week05-sql-joins.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week05-sql-joins.zip) |
| 6 | Joins II | [`week06-sql-joins-2.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week06-sql-joins-2.zip) |
| 7 | Subqueries | [`week07-subqueries.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week07-subqueries.zip) |
| 8 | Database Design | [`week08-database-design.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week08-database-design.zip) |
| 9 | Query Performance | [`week09-query-performance.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week09-query-performance.zip) |
| 10 | Transactions & ACID | [`week10-transactions-acid.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/week10-transactions-acid.zip) |
| Bonus | Project Integration (optional) | [`bonus-week11-project-integration.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/bonus-week11-project-integration.zip) |
| Bonus | Review & Modern Data (optional) | [`bonus-week12-review-modern-data.zip`](https://github.com/mahmoudparsian/OMIS-105/releases/download/weekly-zips/bonus-week12-review-modern-data.zip) |

**Changed on October 27, 2026:** we added Joins II (Week 6) and
Subqueries (Week 7). Database Design, Query Performance, and
Transactions moved to Weeks 8–10. Project Integration and Modern Data
are now optional bonus weeks. If you saved an old link for Weeks 6–10,
please use the links above instead.

## 🗂️ What Is Inside a ZIP File

Each ZIP file holds one folder with two folders inside it.
For example, `week03-sql-basics.zip` gives you:

```
week03-sql-basics/
├── lectures/   ← slides, demo notebooks, labs, quizzes, and data
└── review/     ← the review notebook, review notes, and data
```

`lectures/` is the week's folder from
[`weekly_lectures/`](../weekly_lectures). `review/` is the matching
folder from [`weekly_reviews/`](../weekly_reviews).

Each folder has its own `data/` folder. Nothing depends on another
week, so every week works on its own.

## 🍎 On a MacBook

1. Click the link for your week. The file goes to your **Downloads**
   folder.
2. Double-click the ZIP file. macOS creates a folder with the same
   name, for example `week03-sql-basics`.
3. Open **Terminal** and go into the folder you need:

   ```bash
   cd Downloads/week03-sql-basics/lectures
   ```

4. Open a notebook with Marimo:

   ```bash
   marimo edit
   ```

   Marimo opens in your browser and lists the notebooks in that
   folder. Click one to open it.

## 🪟 On Windows

1. Click the link for your week. The file goes to your **Downloads**
   folder.
2. Right-click the ZIP file and choose **Extract All…**, then click
   **Extract**.

   > ⚠️ Do **not** just double-click the ZIP and open the notebooks
   > from there. Windows only shows a preview, and the notebooks
   > cannot find their `data/` folder. Always **Extract All** first.

3. Windows puts the files in a folder named after the ZIP file, so
   you will see the week name **twice** in the path. This is normal:

   ```
   Downloads\week03-sql-basics\week03-sql-basics\lectures
   ```

4. Open **Command Prompt** and go into the folder you need:

   ```bat
   cd Downloads\week03-sql-basics\week03-sql-basics\lectures
   ```

5. Open a notebook with Marimo:

   ```bat
   marimo edit
   ```

   Marimo opens in your browser and lists the notebooks in that
   folder. Click one to open it.

If `marimo` is "not recognized" on either computer, see the
installation guide in
[`software_installation/`](../software_installation).

## 🔄 Getting Updates

The ZIP files are **rebuilt automatically** every time the course
files change. The link always gives you the newest version.

If you downloaded a week earlier, download it again to get any
updates. Before you do, save a copy of any notebook you changed, so
the new download does not replace your work.

You can see when the files were last updated on the
[Releases page](https://github.com/mahmoudparsian/OMIS-105/releases/tag/weekly-zips).
Look for the line that starts with **"Last updated"**.

## ❓ Common Questions

**What are "Source code (zip)" and "Source code (tar.gz)" on the
Releases page?**
GitHub adds these two files to every release automatically. They hold
the **whole** course repository, not a single week. Please ignore them
and download a `weekNN-….zip` file instead.

**Can I download a whole topic folder, like `tutorials/` or
`data_stories/`?**
Not as a ZIP file yet. These ZIP files cover the ten week folders only.
To get everything, use the green **Code** button on the
[repository page](https://github.com/mahmoudparsian/OMIS-105) and choose
**Download ZIP**.

**I already know git. Do I need these ZIP files?**
No. You can keep using `git clone` and `git pull`. The ZIP files hold
the same files.

**A link says "Not Found." What should I do?**
Check that you copied the whole link. If it still fails, tell me in
class or during office hours (see
[`QUESTIONS_and_OFFICE_HOURS.md`](./QUESTIONS_and_OFFICE_HOURS.md)).

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
