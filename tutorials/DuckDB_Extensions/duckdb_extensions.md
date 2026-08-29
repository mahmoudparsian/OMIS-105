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

# DuckDB Extensions

## Giving Your Database New Superpowers

---

# Table of Contents

1. What Is an Extension?
2. Built-In vs. Add-On Features
3. Checking What You Have
4. INSTALL and LOAD — The Manual Way
5. Autoloading — The Easy Way
6. `httpfs` — Read Files Straight from the Web
7. `json` — Nested Data, Already Included
8. `excel` — Talk Directly to Spreadsheets
9. A Peek at the Wider Ecosystem
10. Staying Safe
11. Cheat Sheet + Practice Exercise

---

# What Is an Extension?

DuckDB's **core** is small and fast on purpose. Not every feature
anyone might want is built in from day one.

Instead, extra features live in **extensions** — optional add-ons
you turn on only when you need them.

👉 Same idea as installing an app on your phone: the operating
system stays lean, and you add only what you actually use.

Today: reading files from the internet, working with JSON, and
reading/writing Excel spreadsheets — all through extensions.

---

# Built-In vs. Add-On Features

Some things work immediately, with **zero setup**:

```sql
D SELECT * FROM read_csv('data/students.csv');   -- always works
D SELECT * FROM read_json('data/students.json'); -- always works
```

Others need to be **added** before DuckDB can use them:

```sql
D SELECT * FROM 'https://duckdb.org/data/prices.parquet';
-- needs the httpfs extension
```

`csv`, `parquet`, and `json` ship **bundled** with DuckDB. `httpfs`
and `excel` do not — DuckDB fetches them the first time you need
them.

---

# Checking What You Have

`duckdb_extensions()` is a table function — query it like any table:

```sql
D SELECT extension_name, loaded, installed
  FROM duckdb_extensions()
  WHERE extension_name IN ('json','parquet','httpfs','excel','spatial');
```

```text
┌────────────────┬─────────┬───────────┐
│ extension_name │ loaded  │ installed │
├────────────────┼─────────┼───────────┤
│ excel          │ false   │ false     │
│ httpfs         │ false   │ false     │
│ json           │ true    │ true      │
│ parquet        │ true    │ true      │
│ spatial        │ false   │ false     │
└────────────────┴─────────┴───────────┘
```

`installed` = downloaded to your machine. `loaded` = active in
**this session**.

---

# INSTALL and LOAD — The Manual Way

Two separate steps, two separate jobs:

```sql
D INSTALL httpfs;   -- download it (once — saved to your machine)
D LOAD httpfs;      -- turn it on (every new duckdb session)
```

- `INSTALL` needs internet the **first** time only.
- `LOAD` is cheap and instant, but only lasts for your **current**
  session — run it again next time you open `duckdb`.

👉 Recall `~/.duckdbrc` from the command-line tutorial? That's
exactly where you'd put `LOAD` commands you want to run every time.

---

# Autoloading — The Easy Way

Modern DuckDB (yours included) usually does this **for you**:

```sql
D SELECT * FROM 'https://duckdb.org/data/prices.parquet' LIMIT 3;
```

The first time this runs, DuckDB notices it needs `httpfs`,
silently installs it, loads it, and answers your query — no
`INSTALL`/`LOAD` typed by you at all.

⚠️ Autoloading still needs internet **the first time** a given
extension is used on a machine. After that, it's cached locally.

---

<!-- _class: dense -->

# `httpfs` — Read Files Straight from the Web

⚠️ **This slide needs Wi-Fi to run live.**

```sql
D SELECT * FROM 'https://duckdb.org/data/prices.parquet' LIMIT 5;
```

```text
┌─────────┬─────────────────────┬───────┐
│ ticker  │        when         │ price │
├─────────┼─────────────────────┼───────┤
│ APPL    │ 2001-01-01 00:00:00 │     1 │
│ APPL    │ 2001-01-01 00:01:00 │     2 │
│ APPL    │ 2001-01-01 00:02:00 │     3 │
│ MSFT    │ 2001-01-01 00:00:00 │     1 │
│ MSFT    │ 2001-01-01 00:01:00 │     2 │
└─────────┴─────────────────────┴───────┘
```

No download step. The file lives on DuckDB's own server; the
`https://` URL **is** the table.

---

# `httpfs` — Same SQL You Already Know

`GROUP BY` doesn't care whether the file is local or remote:

```sql
D SELECT ticker, COUNT(*) AS n, MAX(price) AS max_price
  FROM 'https://duckdb.org/data/prices.parquet'
  GROUP BY ticker
  ORDER BY ticker;
```

```text
┌─────────┬───────┬───────────┐
│ ticker  │   n   │ max_price │
├─────────┼───────┼───────────┤
│ APPL    │     3 │         3 │
│ GOOG    │     3 │         3 │
│ MSFT    │     3 │         3 │
└─────────┴───────┴───────────┘
```

👉 The extension only changes **where DuckDB can look**. Every SQL
skill you already have still applies.

---

# `json` — Nested Data, Already Included

`json` ships bundled — no `INSTALL`, no `LOAD`, ever. Query
`data/students.json` (a plain JSON array of student records)
directly, same as any CSV:

```sql
D SELECT name, gpa
  FROM read_json('data/students.json')
  WHERE gpa > 3.6
  ORDER BY gpa DESC;
```

```text
┌─────────┬──────┐
│  name   │ gpa  │
├─────────┼──────┤
│ Hana    │ 3.95 │
│ Charlie │ 3.9  │
│ Alice   │ 3.8  │
│ Fiona   │ 3.7  │
└─────────┴──────┘
```

---

# `excel` — Talk Directly to Spreadsheets

Business students live in `.xlsx` files. DuckDB can read **and**
write them with the `excel` extension:

```sql
D INSTALL excel;
D LOAD excel;
D CREATE TABLE students AS SELECT * FROM read_csv('data/students.csv');
D COPY students TO 'data/students.xlsx' WITH (FORMAT xlsx, HEADER true);
```

That's it — `data/students.xlsx` now exists, ready to open in Excel
or Google Sheets.

---

# `excel` — Reading It Back

```sql
D SELECT * FROM read_xlsx('data/students.xlsx') LIMIT 3;
```

```text
┌────────┬─────────┬────────────┬────────┐
│   id   │  name   │   major    │  gpa   │
├────────┼─────────┼────────────┼────────┤
│    1.0 │ Alice   │ Marketing  │    3.8 │
│    2.0 │ Bob     │ Finance    │    3.5 │
│    3.0 │ Charlie │ Accounting │    3.9 │
└────────┴─────────┴────────────┴────────┘
```

⚠️ Notice `id` came back as `1.0`, not `1`. Excel has no separate
"integer" type — every number is a decimal. Small surprise, good to
know before you rely on it.

---

# A Peek at the Wider Ecosystem

DuckDB ships more **core extensions** beyond today's three:

| Extension | What it adds |
|---|---|
| `spatial` | Maps, coordinates, `ST_Distance`, `ST_Point` |
| `fts` | Full-text search over text columns |
| `icu` | International date/time and collation support |
| `autocomplete` | The Tab-completion you've been using in the CLI — also an extension! |

Beyond that, **community extensions** (`community-extensions.duckdb.org`)
are built by outside developers — more specialized, less
officially vetted.

---

# Staying Safe

`INSTALL` downloads and runs **code** — treat it like installing
software, not like opening a data file.

- Only install extensions from `duckdb.org` or a source you trust.
- On a locked-down or offline machine, autoloading can be turned off:

```sql
D SET autoload_known_extensions = false;
D SET autoinstall_known_extensions = false;
```

- Both default to `true` — DuckDB is helpful by default, but you
  can always take manual control.

---

<!-- _class: dense -->

# Cheat Sheet

| Command | What it does |
|---|---|
| `SELECT * FROM duckdb_extensions();` | list installed/loaded extensions |
| `INSTALL name;` | download an extension (once) |
| `LOAD name;` | turn an extension on (per session) |
| `read_csv/json/parquet(...)` | bundled — always available |
| `'https://...file.parquet'` | needs `httpfs` (often autoloaded) |
| `read_xlsx(...)` / `COPY ... (FORMAT xlsx)` | needs `excel` |
| `SET autoload_known_extensions=false;` | disable autoloading |

---

# Practice Exercise (1/2)

In your terminal, `cd` into this tutorial's folder, then start
`duckdb`:

1. Run `SELECT * FROM duckdb_extensions() WHERE extension_name = 'json';`
   — is it `loaded`?
2. Query `data/students.json` for students majoring in
   **`'Finance'`**
3. `INSTALL` and `LOAD` the `excel` extension

---

# Practice Exercise (2/2)

4. Write `data/students.csv` out to a new file, `my_students.xlsx`
5. Read `my_students.xlsx` back with `read_xlsx(...)` and confirm
   the row count matches the original CSV
6. If you have Wi-Fi: query
   `'https://duckdb.org/data/holdings.parquet'` and find which
   `ticker` has the single largest `shares` value

---

<!-- _class: closing -->

# Extensions = DuckDB, Customized

Small core. Add exactly the features you need, when you need them.

**Resources**

duckdb.org/docs/extensions/overview — Official extensions guide
community-extensions.duckdb.org — Community-built extensions

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
