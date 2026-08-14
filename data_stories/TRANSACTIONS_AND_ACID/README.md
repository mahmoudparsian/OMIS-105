# 🏦 Transactions & ACID

**OMIS-105 · Week 8 — Transactions & ACID**

A hands-on DuckDB notebook built on the Week 8 lab's bank-transfer scenario. It
demonstrates each of the four ACID properties with code you can run, and answers
the lab's challenge question directly.

---

## Why this story exists

The Week 8 teaching notes flag the problem this notebook is designed around:

> *Common issue: Students memorize ACID but don't understand it.*

So nothing here is defined and moved past. Each letter gets a demonstration where
the database **visibly refuses to do the wrong thing**, and you watch it happen
before you read the label.

It also answers the lab's challenge — *"What happens if COMMIT is not executed?"* —
by closing the database and reopening it, so students see the uncommitted change
genuinely gone rather than being told it would be.

---

## Run it

```bash
marimo edit transactions_and_acid_marimo.py    # interactive
marimo run  transactions_and_acid_marimo.py    # read-only, for students
python      transactions_and_acid_marimo.py    # smoke test
```

Runs in about two seconds. No data files needed.

| File | Role |
|---|---|
| `transactions_and_acid_marimo.py` | The notebook — 10 sections |
| `acid_plot_util.py` | `display_table`, `show_balances`, and the three charts |
| `bank.duckdb` | Created on each run — **gitignored** |

**Why a real file and not `:memory:`** — Section 8 has to close the connection,
reopen the database, and show what survived. That is impossible in memory. The file
is deleted at the top of every run, so the notebook stays idempotent.

---

## What it covers

| § | Section | Point |
|---|---|---|
| 1 | The `accounts` table | Bank schema with `PRIMARY KEY`, `NOT NULL`, `CHECK (balance >= 0)` |
| 2 | The **unsafe** transfer | Stop between the two `UPDATE`s — the total reads **700, not 800** |
| 3 | `BEGIN` … `COMMIT` | The same transfer, made indivisible |
| 4 | `ROLLBACK` | The undo button |
| 5 | **A** — Atomicity | A valid update is discarded because its partner failed |
| 6 | **C** — Consistency | Three attempts to break the rules, all refused |
| 7 | **I** — Isolation | Two connections; the reader never sees uncommitted work |
| 8 | **D** — Durability | Close, reopen — **the lab's challenge question, answered** |
| 9–10 | Summary + 5 exercises | Including a shop stock/order scenario |

---

## The demonstrations, and what each proves

**Atomicity (§5)** — inside one transaction, take \$100 from Alice (succeeds), then
take \$99,999 from Bob (violates the `CHECK`). After `ROLLBACK`, Alice's \$100 is
back. The successful statement was thrown away because its partner failed.

Two behaviours students should see here:

- Once a statement fails, DuckDB puts the transaction in an **aborted** state —
  even a `SELECT` is refused until you `ROLLBACK`.
- Issuing `COMMIT` on an aborted transaction **returns without error but writes
  nothing**. "COMMIT succeeded" is not the same as "my data was saved". This
  surprises people and is worth pausing on.

**Consistency (§6)** — three invalid writes, all rejected by the table's own
constraints:

| Attempt | Result |
|---|---|
| Overdraw Alice by \$10,000 | REJECTED — `ConstraintException` |
| Insert a duplicate `account_id` | REJECTED — `ConstraintException` |
| Insert an account with no owner | REJECTED — `ConstraintException` |

No application code did any checking. The rules live in the schema, so they apply
to every program that ever touches this database.

**Isolation (§7)** — two connections via `con.cursor()`:

```
Writer, inside its own transaction : 250.00
Reader, a different connection     : 500.00   ← no dirty read
Reader, after the COMMIT           : 250.00   ← now visible
```

**Durability (§8)** — commit a \$50 transfer, then start a second change and close
the database without committing it. On reopening: the \$50 survived, the
uncommitted change is gone.

> **No `COMMIT`, no promise. No promise, no data.**

---

## Teaching suggestions

- **Run §2 before saying the word "transaction".** The chart shows the total as
  `700` in red at the crash window. Ask what the bank's auditor would say. The need
  for the tool should be felt before the tool is named.
- **§5 works well as a prediction exercise.** Before running it, ask the class to
  vote: after the second statement fails, is Alice \$100 poorer or not? The vote is
  usually split, which makes the answer land.
- **§8 is the exit ticket.** It is the lab's challenge question, so students can
  answer it from something they watched rather than something they memorised.
- If your class has seen the `FK_JOINS` story, note the continuity: constraints
  there prevented *invalid references*; constraints here prevent *invalid states*.
  Same mechanism, different job.

---

## A caveat worth mentioning in class

DuckDB is an **embedded, single-writer** database. It gives you real transactions
and real isolation, and everything in this notebook is genuine — but it is not a
multi-user server like PostgreSQL. Phenomena that need several concurrent writers —
deadlocks, lock waits, isolation levels beyond snapshot — cannot be demonstrated
here. If your course discusses those, flag them as concepts students will meet on a
client-server database rather than something this notebook can show.
