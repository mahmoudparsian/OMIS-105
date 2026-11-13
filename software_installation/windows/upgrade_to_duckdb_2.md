# Upgrade to DuckDB 2.0 (Windows)

**DuckDB 2.0 is the recommended version for OMIS 105** (since November 10, 2026).
Most of the class already has it. This page is for you if your DuckDB is still
**1.5.x**. It takes about 5 minutes.

DuckDB 1.5.5 still works for every class notebook, so this upgrade is
recommended, not required. But if you see the error
`Trying to read a database file with version number 999`, you **must** upgrade
(see Step 5).

> ⚠️ **Running `step_2_setup_software.py` again does not upgrade DuckDB.** It
> only installs packages that are missing. Use the commands below.

---

## Step 1 — Check your version

Open **Command Prompt** and type:

```
python -c "import duckdb; print(duckdb.__version__)"
```

(If `python` doesn't work, try `py` instead, in this command and in the ones
below.)

* `2.0.0` or newer: you are done. You do not need this page.
* `1.5.5` (or another `1.x`): continue with Step 2.

If you also installed the **DuckDB command line tool** (optional, see
[`README.md`](README.md#duckdb-cli-optional)), check it too:

```
duckdb --version
```

---

## Step 2 — Close Marimo

If Marimo is running, go to its Command Prompt window and press
**Ctrl + C** (answer `y` if it asks). Close any Marimo tabs in your browser.

This step matters on Windows: while Marimo is running, Windows will not let
pip replace DuckDB's files, and the upgrade fails with an "Access is denied"
error.

---

## Step 3 — Upgrade the Python package

```
python -m pip install --upgrade duckdb
```

---

## Step 4 — The command line tool (only if you installed it)

**`winget` cannot do this step:** its `DuckDB.cli` package stops at **1.5.6**
and does not offer 2.0 yet. You have two choices.

**Easiest — remove the command line tool.** Class notebooks, labs, and exams
do not need it (Marimo uses the Python package from Step 3):

```
winget uninstall --id DuckDB.cli --exact
```

**Or install the 2.0 command line tool by hand:**

1. In **Settings > System > About**, look at **System type**: x64
   (Intel/AMD) or Arm.
2. Remove the old copy: `winget uninstall --id DuckDB.cli --exact`
3. At [duckdb.org/install](https://duckdb.org/install/), choose **Windows /
   CLI** and download **duckdb-cli-windows-amd64.tar.gz** (x64) or
   **duckdb-cli-windows-arm64.tar.gz** (Arm) to your **Downloads** folder.
4. In Command Prompt, unpack it (Arm: change `amd64` to `arm64`):

   ```
   mkdir "%USERPROFILE%\duckdb-cli"
   tar -xzf "%USERPROFILE%\Downloads\duckdb-cli-windows-amd64.tar.gz" -C "%USERPROFILE%\duckdb-cli"
   ```

   You should now have `duckdb-cli\duckdb.exe`. If the files landed in an
   extra folder, move **duckdb.exe** up into `duckdb-cli`.
5. Add that folder to your PATH: Start menu → search **Edit environment
   variables for your account** → under **User variables**, edit **Path** →
   **New** → paste the full path of your `duckdb-cli` folder (copy it from
   File Explorer; no `duckdb.exe`, no quote marks). Keep the existing entries.
6. **Close Command Prompt and open a new one.**

---

## Step 5 — Check again

```
python -c "import duckdb; print(duckdb.__version__)"
duckdb --version
```

Both should now show **2.0.0** (or newer). (If you removed the command line
tool in Step 4, `duckdb --version` says it is not recognized; that is fine.)
**They must match.** Your computer
can have several copies of DuckDB (the Python package, the command line tool,
and the one inside qStudio), and a database file (`.duckdb`) made by DuckDB 2.0
**cannot** be opened by an older copy. That is what the "version number 999"
error means.

If qStudio cannot open a `.duckdb` file after your upgrade, you need
**qStudio 5.09 or newer** (check **Help → About**); install it from its
[download page](https://www.timestored.com/qstudio/download).

---

## Step 6 — Start Marimo again

```
marimo edit
```

Open any class notebook. It now uses DuckDB 2.0.

---

## Good to know

* **Your files are safe.** DuckDB 2.0 opens `.duckdb` files that were made
  with 1.5. You do not need to rebuild anything.
* **The SQL is the same.** Labs and exams do not change.
* **Optional data stories** in `data_stories/` use a few extra packages. Class
  notebooks do not need them. To run the data stories, install them once:

  ```
  python -m pip install seaborn altair jinja2 tabulate pyarrow polars
  ```

## Still stuck?

See [`installation_trouble_shooting.md`](installation_trouble_shooting.md),
or take a screenshot of the error and bring it to office hours.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
