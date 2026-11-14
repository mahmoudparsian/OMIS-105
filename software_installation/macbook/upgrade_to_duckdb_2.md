# Upgrade to DuckDB 2.0 (Mac)

**DuckDB 2.0 or newer is required for OMIS 105** (since November 13, 2026).
Most of the class already has it. This page is for you if your DuckDB is still
**1.5.x**. It takes about 5 minutes.

DuckDB 1.5 is no longer supported in this course. If you see the error
`Trying to read a database file with version number 999`, that is an old copy of
DuckDB trying to open a newer file (see Step 5).

> 💡 **Shortcut:** running `step_2_setup_software.py` again now upgrades DuckDB to 2.0 for you
> (it installs `duckdb>=2.0`). The steps below do the same by hand.

---

## Step 1 — Check your version

Open **Terminal** and type:

```
python3 -c "import duckdb; print(duckdb.__version__)"
```

* `2.0.0` or newer: you are done. You do not need this page.
* `1.5.5` (or another `1.x`): continue with Step 2.

If you also installed the **DuckDB command line tool** (optional, see
[`README.md`](README.md#duckdb-cli-optional)), check it too:

```
duckdb --version
```

---

## Step 2 — Close Marimo

If Marimo is running, go to its Terminal window and press **Control + C**
(answer `y` if it asks). Close any Marimo tabs in your browser.

---

## Step 3 — Upgrade the Python package

```
python3 -m pip install --upgrade "duckdb>=2.0"
```

If you see `error: externally-managed-environment`, your Python protects
itself from changes (normal for Homebrew Python). Run this instead:

```
python3 -m pip install --upgrade --break-system-packages "duckdb>=2.0"
```

---

## Step 4 — Upgrade the command line tool (only if you installed it)

```
brew upgrade duckdb
```

If you did not install the DuckDB command line tool, skip this step.

---

## Step 5 — Check again

```
python3 -c "import duckdb; print(duckdb.__version__)"
duckdb --version
```

Both should now show **2.0.0** (or newer). **They must match.** Your computer
can have several copies of DuckDB (the Python package, the command line tool,
and the one inside qStudio), and a database file (`.duckdb`) made by DuckDB 2.0
**cannot** be opened by an older copy. That is what the "version number 999"
error means.

If qStudio cannot open a `.duckdb` file after your upgrade, you need
**qStudio 5.09 or newer** (check **Help → About**). On a Mac, download the `.dmg`
from [GitHub](https://github.com/timestored/qstudio/releases/latest) — **not**
timestored.com, whose Mac download is still the old 5.01. Details:
[Step 4 guide](step_4_install_qstudio.md#step-1--download-qstudio).

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
  python3 -m pip install seaborn altair jinja2 tabulate pyarrow polars
  ```

  (Add `--break-system-packages` after `install` if you see the
  `externally-managed-environment` error.)

## Still stuck?

See [`installation_trouble_shooting.md`](installation_trouble_shooting.md),
or take a screenshot of the error and bring it to office hours.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
