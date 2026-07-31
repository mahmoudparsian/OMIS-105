for my OMIS-105: introduction to DBMS, I was thinking to create a simple streamlit app to show the power and usage of RDBMS by DuckDB. We can develop a series of applications: level 1, level 2, level 3 : do you have any idea on this. Do not create any code, just talk to me about a data story, design of some tables, and then application. what do you think?

Great idea — DuckDB + Streamlit is a perfect combo for teaching because DuckDB runs entirely in-process (no server setup), so students see pure SQL power without infrastructure friction.

Here's a concept I'd suggest:

---

## The Data Story: A University Bookstore

A familiar, relatable domain for students. It covers the classic RDBMS concepts — entities, relationships, aggregations, joins — without feeling contrived.

**Core entities:**
- `students` — student_id, name, major, year
- `books` — book_id, title, author, isbn, price, category
- `courses` — course_id, name, department, credits
- `purchases` — purchase_id, student_id, book_id, course_id, purchase_date, quantity
- `course_books` — which books are required/optional for which course

This schema is simple enough to understand in 10 minutes but rich enough to ask interesting questions.

---

## The Three Levels

**Level 1 — Explore & Query**
The app is a data explorer. Students browse tables, run pre-written SELECT queries, filter by major or department, and see results instantly. The lesson: *what is a table, what is a row, what does SELECT/WHERE/ORDER BY do?* The UI has dropdowns that build queries behind the scenes — students see the SQL that ran.

**Level 2 — Relationships & Joins**
Now students answer questions that span tables: *"Which books did Computer Science students buy most?"* or *"What's the total revenue per department?"* The app visualizes JOIN results as charts. The lesson: *why normalization matters, what a foreign key does, why we don't just put everything in one table.* Side-by-side views showing a flat denormalized version vs. the normalized version make the tradeoff tangible.

**Level 3 — Aggregation, Analytics & "What If"**
Students become the bookstore manager. They can add a new book, simulate a price change, see how it affects revenue projections, run window functions (e.g., running total of purchases by month), and explore indexes by timing the same query on an indexed vs. unindexed table. The lesson: *RDBMS isn't just storage — it's a computation engine.*

---

## Why This Works Pedagogically

The same dataset runs through all three levels, so students build intuition progressively rather than context-switching. By Level 3, they feel ownership of the data — they've been querying it for weeks.

---

Want to dig deeper into any of these levels, refine the schema, or talk about how to structure the Streamlit UI layout?


before you build level 1, can you present a solid schema, which you proposed



Here's a walkthrough of the design decisions:

**Three table types, color-coded:**
- **Purple — core entities** (`students`, `courses`, `books`): pure "nouns" with no foreign keys. These are the independent tables everything else references.
- **Green — fact table** (`purchases`): the transactional center of the schema. Three foreign keys make it the hub — every interesting question in Levels 2 and 3 flows through here.
- **Orange — junction table** (`course_books`): resolves the many-to-many between courses and books (a course has many required books; a book can be required by many courses). Its PK is composite: `(course_id, book_id)`.

**A few intentional choices worth noting:**

`total_amount` in `purchases` is technically derivable from `price × quantity`, but storing it is a realistic design tradeoff — prices change over time, and you want to capture what the student *actually paid*, not today's price. Good discussion point for class.

`isbn` on `books` carries a `UNIQUE` constraint — not the PK, but a natural key. Teaches students the difference between surrogate keys and natural keys.

`course_books.required` (BOOLEAN) means you can ask: *"did a student buy a required book or an optional one?"* — a richer question than just what they bought.

Ready to proceed to building Level 1?

should we populate these tables, and then add more records by the app???

Great design question — and the answer matters pedagogically. Here are the two real options:

**Option A: Pre-seed a static dataset, app adds on top**
You ship a DuckDB file (or a `seed.sql` script) with ~50–100 rows per table already loaded. The app then lets students INSERT new records. This is the most realistic pattern — it mirrors production systems where data exists before the app UI arrives. Students also have something to query immediately at Level 1 without having to populate anything first.

**Option B: App generates everything from scratch on first run**
The app uses Python (Faker library) to procedurally generate realistic data on startup. Clean, repeatable, no external file dependency. But it's a bigger setup step for Level 1, and the data feels synthetic.

**My recommendation: hybrid.**

Seed the database with a fixed, curated dataset — maybe 10 students, 8 courses, 20 books, 15 course_book mappings, ~60 purchases. Make it feel like a real semester. Then in the app:

- **Level 1** — read-only, students just query the seeded data
- **Level 2** — still read-only, but richer joins reveal the seeded relationships
- **Level 3** — students can INSERT new students, new purchases, simulate price changes; the app shows how the aggregate queries update in real time

This way the seed data tells a consistent story (e.g., CS students buy the most, Fall semester outsells Spring), and the Level 3 inserts let students *break* or *extend* that story — which is a memorable learning moment.

**For the seed itself**, I'd suggest a Python script (`seed.py`) that creates the DuckDB file and loads all tables from hardcoded data. That way it's version-controllable, readable, and reproducible — no binary `.duckdb` file to manage in the repo.

Want me to build `seed.py` next?


Please update CLAUDE.md and other .md if require

Let me check what the current CLAUDE.md says about Level 1 and Level 2 before editing.Good. Now I have the exact lines to update. Level 1 is 444 lines now, Level 2 is 611 lines. Let me also check what the Table Explorer description says in CLAUDE.md and app_level1.md.Now I have everything I need. Three targeted edits to CLAUDE.md and two to the level docs:Now update `app_level1.md` — the Table Explorer controls section:Now update `app_level2.md` — the Join Explorer controls section:All three files updated. Here's a summary of every change:

**CLAUDE.md**
- Level 1 line count: 428 → 444
- Level 1 Table Explorer note: mentions 0 = no LIMIT, max = table cardinality
- Level 2 line count: 593 → 611
- Level 2 Join Explorer note: mentions 0 = no LIMIT, max = actual join result count, updates on join type change

**app_level1.md**
- Table Explorer controls section rewritten: explains the 0 = no LIMIT behaviour, shows the SQL with and without the LIMIT clause

**app_level2.md**
- Added a "Row limit" subsection under Join Explorer explaining the 0 behaviour and the fact that the max updates dynamically when switching INNER ↔ LEFT


These 3 apps will be used for teaching purposes in my OMIS-105 class, thank you very much!!!

That means a lot — thank you for the kind words! It was a genuinely enjoyable project to build.

Your students are going to have a great experience. The progression from "just looking at one table" all the way to window functions, live INSERTs, and timing index performance on a real database — all in a familiar bookstore domain they can relate to — is a really effective way to teach DBMS concepts.

A few things worth knowing as you use it in class:

- **Reset anytime** — `python seed.py` wipes and rebuilds the database cleanly, which is handy between class sessions after students have been inserting records in Level 3.
- **CLAUDE.md** is up to date, so if you want to extend or modify anything in a future session, just point me to that file and I'll have full context immediately.
- If you ever want a **Level 4** — maybe stored procedures, views, transactions, or a multi-user scenario — the foundation is all there.

Good luck with OMIS-105, Dr. Parsian! 🎓


one more question: If I add more rows in seed.py,  
will this  require any changes in apps?

No changes needed in any of the three apps. Here's why each one handles it automatically:

**Level 1** — the Table Explorer slider max is computed from `SELECT COUNT(*) FROM {table}` at runtime, so it always reflects the actual cardinality. All query templates are dynamic too — they pull distinct values (majors, categories, date ranges) from live queries, not hardcoded lists.

**Level 2** — the Join Explorer slider max runs a live `COUNT(*)` of the join result, so it scales with the data. All aggregation templates use `GROUP BY` against whatever rows exist.

**Level 3** — window functions, subqueries, and the INSERT forms all work against the live database. The `next_id()` helper computes `MAX(id) + 1` dynamically, so new rows won't conflict even if you add hundreds of seed records.

The only thing worth keeping consistent is the **domain values** — if you add new majors, departments, or book categories in `seed.py`, they'll automatically appear in all the dropdowns and `GROUP BY` results without any code change.

So just edit `seed.py`, run `python seed.py`, and all three apps adapt immediately.



