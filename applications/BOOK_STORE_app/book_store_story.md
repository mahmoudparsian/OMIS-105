# OMIS-105: Introduction to DBMS
## The University Bookstore — Data Story

---

### Why This Story?

Every student has bought a textbook. That shared experience makes the University Bookstore
a perfect domain for learning relational databases. The entities are immediately familiar —
students, courses, books, purchases — yet the relationships between them are rich enough
to motivate every major concept in an introductory DBMS course.

---

### Setting the Scene

Santa Clara University's bookstore processes thousands of transactions each semester.
Students shop by course, looking up which books are required or optional. The bookstore
manager needs to know which titles move fast, which departments spend the most, and
whether students are actually buying the required reading.

Behind all of this is a relational database. Five tables. Dozens of interesting questions.

---

### The Cast of Entities

**Students** are the buyers. Each student has a major, an academic year, and a GPA.
We care about their buying behavior: do CS students buy more books than Business students?
Do seniors spend more per purchase than freshmen?

**Courses** are the demand drivers. A course in the Engineering department requires
different books than one in the Humanities. Courses carry credit values and are tied
to a semester — so we can track purchasing trends over time.

**Books** are the inventory. Each book has a price, a category (textbook, novel,
reference, etc.), and an ISBN — a natural key that uniquely identifies a title in
the real world, independent of our internal `book_id`.

**Purchases** are the transactions. Every time a student buys a book, a row lands here.
It records not just what was bought, but when, for which course, and the total amount
paid — capturing the price at the time of sale, not just what the book costs today.

**Course-Books** is the bridge. A course can require many books; a book can be
required by many courses. This many-to-many relationship is resolved by a junction
table that also tells us whether a book is *required* or merely *recommended*.

---

### The Questions This Story Can Answer

**Level 1 — Exploration (SELECT, WHERE, ORDER BY)**
- What books does the bookstore carry in the "Computer Science" category?
- Which students are in their sophomore year?
- What are the five most expensive textbooks?

**Level 2 — Relationships (JOIN, GROUP BY, HAVING)**
- Which books did Engineering students buy most this semester?
- What is the total revenue per department?
- Which courses have the highest required-book spending burden per student?
- Are students buying required books at a higher rate than optional ones?

**Level 3 — Analytics (Window Functions, Subqueries, Indexes)**
- What is the running total of bookstore revenue by date?
- Which students spent more than the overall average? More than their major's average?
- How does each book's price compare to the average price within its category?
- How does query performance change when we add an index on `purchases.student_id`?

---

### Why a Relational Database?

A spreadsheet could hold this data — but only badly. Imagine storing the instructor's
name inside every purchase row. Change the instructor, update hundreds of rows.
Misspell a department name once, and your GROUP BY silently splits it in two.

Normalization solves this. Each fact lives in exactly one place:
- A student's major is in `students`, not repeated in `purchases`.
- A book's price is in `books`, and `purchases` records the `total_amount` at time of sale.
- A course's department is in `courses`, referenced by foreign key everywhere else.

This is the core promise of an RDBMS: **one fact, one place, enforced by the engine.**
DuckDB lets us experience that promise directly, running analytical SQL in milliseconds
on a dataset that fits in a single file — no server, no configuration, just SQL.

---

### The Three-Level Application

| Level | Theme | New Concepts |
|-------|-------|--------------|
| 1 | Explore & Query | Tables, rows, SELECT, WHERE, ORDER BY, LIMIT |
| 2 | Relationships & Joins | Foreign keys, JOIN types, GROUP BY, HAVING |
| 3 | Analytics & Power | Window functions, subqueries, indexes, "what-if" |

Each level uses the same five tables and the same dataset. Students build intuition
progressively, and by Level 3 the data feels familiar — which makes the advanced
concepts land harder and stick longer.

---

*OMIS-105 · Santa Clara University · Leavey School of Business*
