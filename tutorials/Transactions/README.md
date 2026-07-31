# Database Transactions

	1. This is for introductory database class. 
	It  is assumed  that  students  have  no 
	knowledge of database transactions (`commit`, 
	`rollback`, ...). 

	2. Create a md/marp document (using mysql database) 
	to teach  database transactions concepts from A 
	to Z: concepts: examples + real demo with MySQL. 

	3. This is a self contained independent document.

## MySQL supports database transactions

## DuckDB supports database transactions



Here's what's inside:

---

**Structure (6 Parts):**

| Part | Topic | Slides |
|---|---|---|
| 1 | The Problem — why transactions exist | Bank disaster, partial update animation |
| 2 | Core Concepts — ACID explained | One slide per property with concrete examples |
| 3 | MySQL Commands | `START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, autocommit |
| 4 | Real Demos | Bank transfer, e-commerce checkout, payroll with savepoints |
| 5 | Isolation Levels | Dirty reads, non-repeatable reads, the 4 levels comparison table |
| 6 | Best Practices | 4 common mistakes, diagnostics, cheat sheet, exercises |

---

# References

[1. MySQL Transactions from MySQL Tutorial](https://www.mysqltutorial.org/mysql-stored-procedure/mysql-transactions/)

[2. The Complete Guide to Database Transactions](https://medium.com/@alxkm/the-complete-guide-to-database-transactions-how-commit-and-rollback-really-work-in-mysql-and-36d1ce81b9eb)

[3. MySQL Transaction](https://www.geeksforgeeks.org/mysql/mysql-transaction/)

