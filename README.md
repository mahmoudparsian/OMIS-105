# OMIS 105 <br> Introduction to Database Management Systems

[![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)](https://duckdb.org)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Marimo](https://img.shields.io/badge/Marimo-2D2D2D?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI0YyOEQxQSIgZD0iTTEyIDJDNi40NzcgMiAyIDYuNDc3IDIgMTJzNC40NzcgMTAgMTAgMTAgMTAtNC40NzcgMTAtMTBTMTcuNTIzIDIgMTIgMnoiLz48L3N2Zz4=&logoColor=white)](https://marimo.io)
[![qStudio](https://img.shields.io/badge/qStudio-4A90D9?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHRleHQgeD0iNCIgeT0iMTgiIGZvbnQtc2l6ZT0iMTgiIGZvbnQtd2VpZ2h0PSJib2xkIiBmaWxsPSJ3aGl0ZSI+UTwvdGV4dD48L3N2Zz4=&logoColor=white)](https://www.timestored.com/qstudio/)

**Instructor:** [Dr. Mahmoud Parsian](https://www.scu.edu/business/isa/faculty/parsian/)

# 1. 🏛️ Course Description

In this course, you will learn the fundamentals of modern relational
data management. Topics include SQL, schema design, data modeling,
querying data with SQL, database applications, and transactions.
Through lectures, hands-on labs, and assignments, you will discover
how real-world database systems work, the principles behind them,
and how they shape the way organizations store, retrieve, and
analyze information every day.

* [This course](https://www.scu.edu/business/isa/academics/courses/) covers the core issues in databases and database management systems (DBMS).
* Students will acquire technical and managerial skills in planning, analysis, design, implementation, and maintenance of databases.
* Hands-on training in relational database design, normalization, SQL, and database implementation is provided.
* Use of DBMS software is required. The course emphasizes the practical issues of managing a database environment.

---

# 2. 🧑‍🎓 Target Students

* This course is designed for undergraduate students in the [Department of Information Systems and Analytics](https://www.scu.edu/business/isa/academics/courses/), Santa Clara University.

---

# 3. Course Prerequisite

* OMIS 30: Introduction to Programming

---

# 4. [Can AI-LLM Write Your SQL?](./why_you_must_learn_SQL/why_you_must_learn_SQL.md)

---

# 5. 🗄️ Folders

| File Name                    | Description     |
|------------------------------|-----------------|
|[`README.md`](./README.md)    | The file you are reading/viewing |
|[`course_information`](./course_information) | Course information (labs, grading, policies, and more) |
|[`course_information/INSTRUCTOR.md`](./course_information/INSTRUCTOR.md) | Mahmoud Parsian, Instructor |
|[`course_information/QUESTIONS_and_OFFICE_HOURS.md`](./course_information/QUESTIONS_and_OFFICE_HOURS.md) | How to Ask Questions; Office Hours |
|[`course_information/REQUIRED_BOOK.md`](./course_information/REQUIRED_BOOK.md)| Required Book (none — all materials in this repo) |
|[`course_information/REQUIRED_SOFTWARE.md`](./course_information/REQUIRED_SOFTWARE.md) | Required Software |
|[`course_information/SOFTWARE_INSTALLATION.md`](./course_information/SOFTWARE_INSTALLATION.md)| Guide to Software Installation |
|[`course_information/LAPTOP.md`](./course_information/LAPTOP.md) | Bring a Fully Charged Laptop to Every Class |
|[`course_information/LAB-IN-CLASS-POLICY.md`](./course_information/LAB-IN-CLASS-POLICY.md) | Lab-in-Class Policies |
|[`course_information/CLASS_ATTENDANCE.md`](./course_information/CLASS_ATTENDANCE.md) | Class Attendance is Mandatory |
|[`course_information/ASSIGNMENTS_and_GRADING.md`](./course_information/ASSIGNMENTS_and_GRADING.md) | Assignments, Labs, and Exams |
|[`course_information/ACADEMIC_CONDUCT.md`](./course_information/ACADEMIC_CONDUCT.md)| Academic Conduct |
|[`outline-10-weeks`](./outline-10-weeks) | Outline/TOC for 10 Weeks |
|[`weekly_lectures`](./weekly_lectures) | Weekly Lectures and Notebooks: 10 weeks |
|[`weekly_reviews`](./weekly_reviews) | Cumulative review notebooks & lecture notes: Weeks 1–3, 4–6, 7–8, 9–10 |
|[`books`](./books) | DuckDB and Database Books |
|[`data_stories`](./data_stories) | Data Stories: 35 self-contained Marimo notebooks for deep learning — see [`data_stories/README.md`](./data_stories/README.md) for **which story maps to which week** |
|[`duckdb_resources`](./duckdb_resources)| DuckDB Resources and Examples |
|[`tutorials`](./tutorials) | Database Tutorials and Notebooks |
|[`applications`](./applications) | Sample Streamlit apps built with DuckDB (e.g. the In-N-Out POS + analytics teaching app) |
|[`data`](./data) | Sample data files (CSV and Parquet) |
|[`software_installation`](./software_installation) | Steps to make sure Python, DuckDB, and Marimo are installed properly |

---

# 6. What is a Database?

A database is an organized collection of digital data or
information, stored electronically in a system. It lets users
store, access, update, and manage information quickly.

## How It Works

* Managed by a Database Management System (DBMS) — software that controls access and security.
* Uses query languages like SQL (Structured Query Language) to find and change data.
* Handles multiple users at the same time without losing data.

## Common Types

* **Relational Databases**: Store data in tables with rows and columns. Examples: DuckDB, PostgreSQL, MySQL.
* **NoSQL Databases**: Store flexible or unstructured data, like emails and videos.
* **Cloud Databases**: Built and accessed through virtual cloud platforms. Examples: Snowflake, Amazon RDS, Google Cloud SQL.

---

# 7. Example of a Database

Common database examples include relational systems like DuckDB,
MySQL, and PostgreSQL, and document systems like MongoDB. These
digital storage tools organize information into rows, columns, or
files so computer programs can find and change data fast.

## Relational Databases (SQL)

* **DuckDB**: An in-process, high-performance analytical SQL database. It runs inside your application (no separate server needed) and uses columnar storage with vectorized query execution to make large-scale data analysis fast.
* **MySQL**: Free software used for websites and online stores.
* **PostgreSQL**: A strong, reliable system used in banks and finance apps.
* **Microsoft SQL Server**: A tool that works well with Windows programs.

## Non-Relational Databases (NoSQL)

* **MongoDB**: Saves data in flexible, text-like files instead of strict tables.
* **Redis**: Stores quick key-value pairs for fast memory lookups.
* **Apache Cassandra**: Handles very large amounts of data spread across many servers.

---

# 8. What is a Database Management System?

* A Database Management System (DBMS) is the core software used to **create**, **store**, **manage**, and **retrieve** data in a database.
* It acts as a bridge between a central database and the users or applications that interact with it, keeping data consistent, secure, and easily accessible.

![](https://databasetown.com/wp-content/uploads/2023/03/What-is-DBMS-Components-of-DBMS-Copy-min.jpg)

---

# 9. What is a Relational Database Management System?

* An RDBMS (Relational Database Management System) is software used to store, manage, and retrieve structured data as **tables of rows and columns**.

![](https://media.geeksforgeeks.org/wp-content/uploads/20260124115821542989/rdbms-2.webp)

* Data is organized into **tables of rows and columns**, and these tables are linked using keys to ensure data integrity and let applications query connected information efficiently.

  | `product_id` | `customer_id` | `purchase_date` | `cost` |
  |:------------:|:-------------:|:---------------:|-------:|
  | P0123789     | C00100745     | 2026-02-23      | 123.45 |
  | P0123700     | C00100745     | 2026-02-26      | 45.00  |

* In an RDBMS, "**relational**" means that data is organized into **tables of rows and columns**, and these tables can be logically linked, or related, to one another using shared data values.

---

# 10. Classic Architecture of DBMS

![](./images/dbms.webp)

---

# 11. Key Concepts of "Relational" Data

* **Tables** (Relations): Data is stored in two-dimensional grids.
* **Row**: Each row represents a single record (for example, a specific customer). Each column represents a specific attribute (for example, an email address).
* **Primary Keys**: A unique identifier for every row in a table (like a Customer ID or Product ID), so that no two records are exactly identical.
* **Foreign Keys**: A column in one table that points to the Primary Key of another table. This creates the "relationship" by linking related records across tables.
* **Normalization**: The process of organizing data into multiple related tables to reduce duplication and prevent data errors.

---

# 12. A Table in RDBMS

![](./images/table.webp)

---

# 13. Set of Tables in RDBMS

![](./images/rdbms.webp)

---

![](./images/sql-nosql.webp)

---

# 14. 🦆 DuckDB as RDBMS

* DuckDB is an analytical, in-process SQL database management system.
* DuckDB is lightweight and high-performance, designed for local and embedded data processing.
* **Embedded, serverless architecture**: DuckDB runs directly inside your application process (like Python) — no separate server to install or configure. This makes it portable and easy to set up.
* **Fast analytical processing**: Built with a columnar query execution engine, DuckDB is optimized for complex SQL queries, aggregations, and instantly querying large files (like Parquet and CSV) directly from your local disk or cloud storage.

---

# 15. 📊 Integration of Data Sources

![](./images/duckdb_echo_system.webp)

---

# 16. 🔧 DuckDB Ecosystem

![](./images/duckdb_ecosystem_svg.svg)

---

# 17. 📗 References

[1. SQL Introduction - DuckDB Documentation](https://duckdb.org/docs/current/sql/introduction)

[2. What is a Relational Database - Google](https://cloud.google.com/learn/what-is-a-relational-database)

[3. What is a Relational Database - IBM](https://www.ibm.com/think/topics/relational-databases)

[4. What is a Relational Database - Microsoft](https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-is-a-relational-database)

[5. Introduction to SQL - GitHub](https://github.com/bobbyiliev/introduction-to-sql)

[6. SQL Tutorial - w3schools](https://www.w3schools.com/sql/)

[7. SQL Tutorial - geeksforgeeks](https://www.geeksforgeeks.org/sql/sql-tutorial/)
