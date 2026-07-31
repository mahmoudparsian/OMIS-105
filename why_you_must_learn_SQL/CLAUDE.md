# CLAUDE.md — why_you_must_learn_SQL

## Purpose

This folder contains **"Can AI Write Your SQL? Yes. Should You Trust
It? Let's Find Out."** — the flagship Week 1 document for OMIS 105
(Introduction to Database Management Systems, Fall 2026, Dr. Mahmoud
Parsian, Santa Clara University).

The document uses a realistic 5-table retail database (BrightCart) to
show students 7 examples where AI-generated SQL is wrong, 4 examples
where it is right, and a practical guide for prompting AI better once
they understand SQL.

## Audience

Senior business students with **zero prior exposure** to SQL. The
document is read before students write any code — it motivates why
they need to learn SQL rather than relying on AI/LLM tools.

## File Inventory

| File | Role |
|------|------|
| `why_you_must_learn_SQL.md` | The source document (Markdown) |
| `why_you_must_learn_SQL.html` | HTML export (from MacDown) |
| `why_you_must_learn_SQL.pdf` | PDF export (from Chrome Print → Save as PDF) |
| `why_you_must_learn_SQL.md.v1` | Version 1 archive |
| `why_you_must_learn_SQL.md.v2` | Version 2 archive |
| `why_you_must_learn_SQL.md.v3` | Version 3 archive |
| `CLAUDE.md` | This file — conventions and context |

## Document Structure (18 Sections)

**Part I — When AI Gets It Wrong** (sections 1–11)

- Sections 1–4: Setup (the question, the company, schema + ER diagram,
  DDL + data)
- Sections 5–11: Seven failure examples (JOIN, price column, status
  filter, NULL, aggregation grain, ranking function, LIMIT vs window)

**Part II — When AI Gets It Right** (sections 12–15)

- Four success examples where AI produces correct SQL but students must
  verify it (top customers, revenue by category, department salaries,
  product catalog with subquery)

**Closing** (sections 16–18)

- Section 16: Verdict table (all 7 errors summarized)
- Section 17: Summary of Lessons (Part I and Part II tables)
- Section 18: How to Prompt AI Better (6 practical rules)

## The BrightCart Retail Schema

Five tables with intentional data traps:

| Table | Rows | Key Trap |
|-------|------|----------|
| `customers` | 8 | 2 customers have zero orders (tests LEFT JOIN) |
| `products` | 6 | Mouse and Desk Mat have price changes — `unit_price` ≠ historical `sale_price` |
| `orders` | 10 | Mixed statuses: 7 Delivered, 1 Cancelled, 1 Returned, 1 Pending |
| `order_items` | 15 | `sale_price` is the historical price; 2 products tied at 1 unit sold |
| `employees` | 7 | 2 employees have NULL department (tests NULL handling) |

**Critical numbers for verification:**

| Metric | Correct Value |
|--------|--------------|
| Total delivered revenue | $559.82 |
| Total revenue (all statuses) | $799.78 |
| Average order value (delivered) | $79.97 |
| Customer count (all) | 8 |
| Delivered order count | 7 |
| Non-Sales employees (including NULL dept) | 5 |

If any edit to the data or queries changes these numbers, every example
in the document must be re-verified.

## Conventions

### TOC with HTML anchors

Use explicit `<a id="section-N"></a>` tags before each heading. Do not
rely on auto-generated anchors — MacDown and other renderers handle
special characters (em dashes, colons) inconsistently.

### Foreign keys in DDL

The `CREATE TABLE` statements include `REFERENCES` clauses that document
foreign key relationships and match the ER diagram in section 3. Keep
these in sync.

### SQL engine

All SQL is DuckDB. The document instructs students to run queries in
**qStudio** connected to DuckDB.

### PDF export workflow

Export `.md` → `.html` first (MacDown or any renderer), then open the
`.html` in Chrome → Print → Save as PDF. This preserves internal TOC
links. MacDown's direct PDF export drops HTML anchor links.

### Course footer

End the document with:
`*OMIS 105 — Introduction to Database Management Systems — Fall 2026*`

### Tone

Short sentences, simple vocabulary. Direct and encouraging, never
condescending. The document is a persuasive argument, not a textbook —
it should feel like a conversation with the instructor.

## What NOT to Change

- **BrightCart data values.** The INSERT data is carefully designed so
  that each example produces specific wrong-vs-right answer pairs. Do
  not add, remove, or change rows without re-verifying all 11 examples
  and the closing verification totals ($559.82, $799.78, $79.97, etc.).
- **Section numbering.** The document uses 18 numbered sections with
  `<a id="section-N">` anchors and a TOC. If you add or remove a
  section, renumber everything and verify all anchors match.
- **The `REFERENCES` clauses** in the CREATE TABLE statements. They
  document foreign key relationships and match the ER diagram.
- **The weak-vs-strong prompt examples** in section 18. They
  deliberately reference Examples 2 and 3 to tie the closing advice
  back to the failure cases.

## Related Files (Sibling Folders)

| Folder | Relationship |
|--------|-------------|
| `../week01_with_qStudio/` | Two companion qStudio practice docs (intro + intermediate) using a `students` table — these are the hands-on exercises that pair with this motivational document |
| `../OMIS_105_github/software_installation/` | Has its own CLAUDE.md — covers the 4-step install flow and 5 required tools |
| `../OMIS_105_github/` | Course GitHub repository — weekly lectures, labs, Marimo notebooks |

## Course-Wide Conventions (for reference)

- **SQL pattern:** `con.execute()`, not `mo.sql()` — applies to all
  Marimo notebooks across the course
- **Table creation:** Always `CREATE OR REPLACE TABLE` for re-runnability
- **Week 1 pedagogy:** qStudio first (pure SQL, no Python), then Marimo
  notebooks starting Week 2
- **Database engine:** DuckDB only — no PostgreSQL, MySQL, or SQLite
