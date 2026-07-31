Relational database table relationships define how data in one table links to another, primarily using foreign keys to maintain data integrity. The three main types are One-to-One (1:1), One-to-Many (1:N), and Many-to-Many (N:M). These structures reduce data redundancy and organize information efficiently, as detailed in this guide to Database Relationship Types from Medium.

Key Relationship TypesOne-to-One (1:1): Each record in Table A is linked to only one record in Table B. Used for security or to split large tables (e.g., Employee and EmployeePersonalDetails).One-to-Many (1:N or 1:M): A single record in Table A can be linked to multiple records in Table B, but records in Table B relate to only one record in Table A. This is the most common type (e.g., Customer to Orders).Many-to-Many (N:M): Multiple records in Table A relate to multiple records in Table B, requiring a "junction table" (or bridging table) to connect them (e.g., Students and Courses).Self-Referencing (Recursive): A table references its own primary key, such as an Employee table with a "ManagerID" column referencing the EmployeeID.

Implementation ComponentsPrimary Key: Uniquely identifies a record in a table.Foreign Key: A column in a table that references the Primary Key in another table, creating the link.Junction Table: Essential for Many-to-Many relationships to store the pairs of foreign keys from both tables.

Understanding Database Relationship Types: A Comprehensive Guide
https://medium.com/@enesalbayrak12345/understanding-database-relationship-types-a-comprehensive-guide-c5a1840039d5


Database table relationships
https://www.metabase.com/learn/grow-your-data-skills/data-fundamentals/table-relationships

Relational database table relationships define how data in one table links to another, primarily using foreign keys to maintain data integrity. The three main types are One-to-One (1:1), One-to-Many (1:N), and Many-to-Many (N:M).  Create a comprehensive  hands-on tutorial using jupyter notebook, python, duckdb, and Markdown. Use simple tables in duckdb to explain the relationships. Be as precise as possible. For tables, you may have small set of records to show POC in action. If possible, include simple images to show the relationships of tables.


Let me first check that DuckDB is available, then build the notebook.DuckDB isn't pre-installed in the sandbox, but that's fine — I'll create the notebook for you to run on your own machine (where `pip install duckdb` will work). Let me build a comprehensive tutorial now.Now let me build the full notebook. This will be a substantial file with markdown explanations, SVG relationship diagrams, and DuckDB code cells.Let me verify the notebook is valid JSON and well-formed:[View your tutorial notebook](computer:///Users/max/Library/Application%20Support/Claude/local-agent-mode-sessions/17406518-bf97-4472-94aa-60236611f432/e77d4f9a-42e6-42a2-8e2a-d58ec34b1a49/local_ba723757-b0c6-4a80-b1b5-3a8d2ec0abfa/outputs/relational_db_relationships_tutorial.ipynb)

The notebook contains 40 cells (15 markdown + 25 code) organized into seven sections:

1. **Setup** — creates an in-memory DuckDB connection and a helper `run()` function
2. **One-to-One (1:1)** — `persons` ↔ `passports` with a `UNIQUE` foreign key constraint; includes a proof cell that attempts (and fails) to insert a duplicate
3. **One-to-Many (1:N)** — `departments` → `employees` with no UNIQUE on the FK; aggregation queries show department summaries
4. **Many-to-Many (N:M)** — `students` ↔ `courses` via an `enrollments` junction table; includes a weighted GPA calculation using the junction table's extra attributes
5. **Visual diagrams** — inline SVG diagrams rendered via `IPython.display.SVG` for all three relationship types
6. **Bonus queries** — anti-joins, self-joins across the N:M, and schema inspection
7. **Summary** — comparison table and key design principles

To run it, just open it in Jupyter and make sure `duckdb` is installed (`pip install duckdb`). Everything runs in-memory with no external dependencies.
