# 🔁 CRUD with Four Examples per Operation

**OMIS-105 · Week 3 — SQL Basics**

The same ten-employee CRUD story as `CRUD_100_10_rows/`, but with **four worked
examples of each operation** instead of one or two. Choose it when students need
repetition rather than novelty.

---

## A note on this folder's history

This story used to be called `CRUD_100_10_rows_with_dql`, after the **`%%dql` cell
magic** from the `magic-duckdb` extension. That is no longer how it works:

- The notebook was converted from Jupyter to **Marimo**.
- `%%dql` is an **IPython cell magic** — Marimo cannot run it.
- Every query now uses Marimo's native SQL cells instead.

The folder, the notebook and the text were cleaned up in 2026: the `%%dql`
explanations, an unused `magic_duckdb` dependency, and an empty "load the magic" cell
were all removed. Nothing about how the notebook behaves changed.

---

## Run it

```bash
marimo edit CRUD_100_10_rows_drill_marimo.py    # interactive
marimo run  CRUD_100_10_rows_drill_marimo.py    # read-only
```

| File | Role |
|---|---|
| `CRUD_100_10_rows_drill_marimo.py` | The notebook |
| `display_utils.py` | Display and chart helpers |
| `data/employees.csv` | 10 employees |

---

## What it covers

| § | Section | Operations |
|---|---|---|
| 0 | Environment setup | Install packages, connect |
| 2A | **CREATE** | 4 `INSERT` examples |
| 2B | **READ** | 4 `SELECT` examples |
| 2C | **UPDATE** | 4 `UPDATE` examples |
| 2D | **DELETE** | 4 `DELETE` examples |

**Sixteen worked examples in total** — more drill per concept than any other CRUD
story here. That is now its real distinguishing feature.

---

## Why it exists as a separate story

Before the Marimo conversion, this variant showed an **alternative way of writing
SQL** — the `%%dql` magic, instead of wrapping each query in Python. That was its
reason to be separate.

That reason is gone: **the SQL here now looks the same as in every other story.**

What remains is the repetition. Sixteen worked examples across the four operations is
more practice per concept than any sibling, so use it when students need the drill —
not to show them a different notebook style.

---

## Choosing among the CRUD stories

They all teach the same four operations. The differences:

| Story | Rows | What makes it different |
|---|---|---|
| `CRUD_100_10_rows/` | 10 | The plainest version. **Start here.** |
| **`CRUD_100_10_rows_drill/`** ← this one | 10 | **4 examples per operation** — most repetition |
| `CRUD_100_10_rows_with_images/` | 10 | Adds employee photos to result tables |
| `CRUD_100_10_rows_flagship/` | 10 | Photos, backup table, persistence, re-runnability |
| `CRUD_9_emps_intro/` | 9 | Longest conceptual intro — "what is DuckDB", "what is CRUD" |
| `CRUD_10_emps_staging/` | 10 | Staging-table variant |
| `CRUD_10_emps_persistent/` | 10 | Persistent database and backup table |
| `emps_single_table/` | 1,100 | Real-size table; adds a "did the changes stick?" check |

> **Note:** five of these folders were renamed in 2026 to say what they actually
> contain. They were previously `CRUD_100_emps`, `CRUD_101_emps`, `CRUD_102_emps`,
> `CRUD_100_10_rows_with_images_openai` and `CRUD_100_10_rows_with_dql` — names whose
> numbers were not row counts, that promised an AI integration which does not exist,
> or that named a feature the notebook no longer uses.

**Assign one.** They are variations on a theme, and doing several is repetition
without new material.
