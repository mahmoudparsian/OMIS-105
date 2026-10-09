# AUTO-INCREMENT Columns in DuckDB

* An **auto-increment** column is a column that the
  database fills in **for you**, with the next
  number in a series: 1, 2, 3, ...

* It is most often used for a **primary key**
  (`customer_id`, `order_id`, ...). You never have
  to invent a new ID yourself.

* **DuckDB has no `AUTO_INCREMENT` keyword.**
  Instead, you build the same behavior from two
  pieces: a **`SEQUENCE`** (a number counter) and a
  **`DEFAULT nextval(...)`** on the column.

*All DuckDB examples were tested with DuckDB v1.5.5.*

---

## 1. Why Use an Auto-Increment Key?

| Without auto-increment | With auto-increment |
| :--- | :--- |
| You must choose a new ID for every row. | The database chooses the ID. |
| Two people may pick the same ID. | Every new ID is different. |
| `INSERT` must list the ID. | `INSERT` can leave the ID out. |

An auto-increment ID is a **surrogate key**: a
number with no business meaning. Its only job is
to identify one row.

---

## 2. Auto-Increment in Other Databases

Every database system offers this feature, but the
**syntax is different** in each one:

| Database | How to declare it |
| :--- | :--- |
| MySQL | `id INT AUTO_INCREMENT PRIMARY KEY` |
| PostgreSQL | `id SERIAL PRIMARY KEY` or `id INT GENERATED ALWAYS AS IDENTITY` |
| SQLite | `id INTEGER PRIMARY KEY AUTOINCREMENT` |
| SQL Server | `id INT IDENTITY(1,1) PRIMARY KEY` |
| **DuckDB** | `CREATE SEQUENCE ...` + `id INTEGER PRIMARY KEY DEFAULT nextval('...')` |

None of the first four forms work in DuckDB:

```sql
CREATE TABLE t (id INTEGER PRIMARY KEY AUTOINCREMENT);
-- Parser Error: syntax error at or near "AUTOINCREMENT"

CREATE TABLE t (id SERIAL PRIMARY KEY);
-- Catalog Error: Type with name SERIAL does not exist!

CREATE TABLE t (id INTEGER GENERATED ALWAYS AS IDENTITY);
-- Not implemented Error: Constraint not implemented!
```

---

## 3. Example: AUTO_INCREMENT in MySQL

In MySQL, the `AUTO_INCREMENT` attribute generates
a unique, sequential number whenever a new row is
added. By default, it starts at `1` and goes up by
`1` for each new row.

```sql
mysql> CREATE TABLE users (
    ->     id INT AUTO_INCREMENT PRIMARY KEY,
    ->     username VARCHAR(50) NOT NULL,
    ->     email VARCHAR(100) NOT NULL
    -> );
Query OK, 0 rows affected (0.006 sec)

mysql> DESC users;
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| id       | int          | NO   | PRI | NULL    | auto_increment |
| username | varchar(50)  | NO   |     | NULL    |                |
| email    | varchar(100) | NO   |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
3 rows in set (0.006 sec)

mysql> INSERT INTO users (username, email)
    -> VALUES
    -> ('alice_dev', 'alice@example.com'),
    -> ('bob_codes', 'bob@example.com'),
    -> ('charlie_ux', 'charlie@example.com');
Query OK, 3 rows affected (0.004 sec)

mysql> SELECT * FROM users;
+----+------------+---------------------+
| id | username   | email               |
+----+------------+---------------------+
|  1 | alice_dev  | alice@example.com   |
|  2 | bob_codes  | bob@example.com     |
|  3 | charlie_ux | charlie@example.com |
+----+------------+---------------------+
3 rows in set (0.001 sec)
```

Notice: the `INSERT` never mentions `id`.
MySQL fills it in.

---

## 4. Auto-Increment in DuckDB: Three Steps

```sql
-- Step 1. Create a sequence (a counter that starts at 1)
CREATE SEQUENCE user_id_seq START 1;

-- Step 2. Use the sequence as the column's DEFAULT value
CREATE TABLE users (
    user_id  BIGINT PRIMARY KEY DEFAULT nextval('user_id_seq'),
    username VARCHAR NOT NULL,
    email    VARCHAR
);

-- Step 3. Insert rows WITHOUT the user_id column
INSERT INTO users (username, email)
VALUES
    ('alex',  'alex@example.com'),
    ('janet', 'janet@example.com'),
    ('mo',    'mo@example.com');

SELECT * FROM users;
```

```
┌─────────┬──────────┬───────────────────┐
│ user_id │ username │       email       │
│  int64  │ varchar  │      varchar      │
├─────────┼──────────┼───────────────────┤
│       1 │ alex     │ alex@example.com  │
│       2 │ janet    │ janet@example.com │
│       3 │ mo       │ mo@example.com    │
└─────────┴──────────┴───────────────────┘
```

`DESCRIBE users;` shows the rule on the column:

```
│ user_id  bigint  not null default nextval('user_id_seq') │
```

---

## 5. How a Sequence Works

A **sequence** is a separate database object (not
part of any table). It remembers the last number it
gave out.

| Function | What it does |
| :--- | :--- |
| `nextval('seq')` | Moves the counter forward and returns the new number |
| `currval('seq')` | Returns the last number given out (does not move the counter) |

`DEFAULT nextval('user_id_seq')` means: *"If the
`INSERT` does not give a `user_id`, call
`nextval()` and use that number."*

```sql
SELECT currval('user_id_seq') AS last_value_used;   -- 3
```

**Tip:** `RETURNING` shows the ID that was just
created:

```sql
INSERT INTO users (username, email)
VALUES ('ted', 'ted@example.com')
RETURNING user_id;                                   -- 4
```

---

## 6. Choosing the Start Value and Step Size

A sequence does not have to start at 1:

```sql
CREATE SEQUENCE tester_id_seq START 1000;

CREATE TABLE test_users (
    user_id  BIGINT PRIMARY KEY DEFAULT nextval('tester_id_seq'),
    username VARCHAR NOT NULL
);

INSERT INTO test_users (username)
VALUES ('alex'), ('bob'), ('jane'), ('ted');

SELECT * FROM test_users;
```

```
┌─────────┬──────────┐
│ user_id │ username │
│  int64  │ varchar  │
├─────────┼──────────┤
│    1000 │ alex     │
│    1001 │ bob      │
│    1002 │ jane     │
│    1003 │ ted      │
└─────────┴──────────┘
```

It can also count by a different step:

```sql
CREATE SEQUENCE ticket_seq START 100 INCREMENT BY 10;
SELECT nextval('ticket_seq') AS a, nextval('ticket_seq') AS b;
-- a = 100, b = 110
```

---

## 7. Rule 1: You Can Still Supply Your Own ID

`DEFAULT` is used **only when the column is left
out** of the `INSERT`. If you give a value, DuckDB
uses your value and **does not touch the
sequence**.

```sql
-- user_id is given explicitly: the sequence is NOT used
INSERT INTO users (user_id, username, email)
VALUES (6, 'austin', 'austin@example.com');

SELECT * FROM users;
```

```
┌─────────┬──────────┬────────────────────┐
│ user_id │ username │       email        │
│  int64  │ varchar  │      varchar       │
├─────────┼──────────┼────────────────────┤
│       1 │ alex     │ alex@example.com   │
│       2 │ janet    │ janet@example.com  │
│       3 │ mo       │ mo@example.com     │
│       4 │ ted      │ ted@example.com    │
│       6 │ austin   │ austin@example.com │
└─────────┴──────────┴────────────────────┘
```

The sequence still remembers `4`. It does **not**
know that `6` is now taken.

---

## 8. Rule 2 (Warning): Mixing Your Own IDs Can Cause Errors

Continue the example. Insert three rows **without**
an ID:

```sql
INSERT INTO users (username, email) VALUES ('max', 'max@example.com');
-- OK: the sequence gives 5

INSERT INTO users (username, email) VALUES ('max', 'max@example.com');
-- The sequence gives 6, but 6 is already used by 'austin':
-- Constraint Error: Duplicate key "user_id: 6" violates primary key constraint.

INSERT INTO users (username, email) VALUES ('max', 'max@example.com');
-- OK: the sequence gives 7
```

```
┌─────────┬──────────┬────────────────────┐
│ user_id │ username │       email        │
├─────────┼──────────┼────────────────────┤
│       1 │ alex     │ alex@example.com   │
│       2 │ janet    │ janet@example.com  │
│       3 │ mo       │ mo@example.com     │
│       4 │ ted      │ ted@example.com    │
│       6 │ austin   │ austin@example.com │
│       5 │ max      │ max@example.com    │
│       7 │ max      │ max@example.com    │
└─────────┴──────────┴────────────────────┘
```

**Lesson:** for an auto-increment column, let the
sequence choose **every** ID. If you insert
`user_id = 1000` by hand, the error waits silently
until the sequence reaches `1000`.

(Also notice: rows are **not** stored in ID order.
Use `ORDER BY user_id` when order matters.)

---

## 9. Rule 3: IDs Are Unique, Not Gap-Free

A sequence **never goes backward** and **never
reuses** a number. Gaps appear when:

* an `INSERT` **fails** — the number was already taken from the sequence;
* a row is **deleted** — its number is not given out again.

```sql
CREATE SEQUENCE item_id_seq START 1;
CREATE TABLE items (
    item_id BIGINT PRIMARY KEY DEFAULT nextval('item_id_seq'),
    name    VARCHAR NOT NULL
);

INSERT INTO items (name) VALUES ('pen'), ('book');  -- 1, 2
INSERT INTO items (name) VALUES (NULL);             -- uses 3, then FAILS (NOT NULL)
INSERT INTO items (name) VALUES ('lamp');           -- 4
DELETE FROM items WHERE item_id = 4;                -- 4 is gone for good
INSERT INTO items (name) VALUES ('desk');           -- 5

SELECT * FROM items;
```

```
┌─────────┬─────────┐
│ item_id │  name   │
├─────────┼─────────┤
│       1 │ pen     │
│       2 │ book    │
│       5 │ desk    │
└─────────┴─────────┘
```

**Lesson:** never use the largest ID to count rows.
Use `SELECT COUNT(*) FROM items;` instead.

---

## 10. Rule 4: Use One Sequence per Table

A sequence is not tied to a table. If two tables
share one sequence, they **share one counter**:

```sql
CREATE SEQUENCE shared_seq START 1;
CREATE TABLE customers (id BIGINT PRIMARY KEY DEFAULT nextval('shared_seq'), name VARCHAR);
CREATE TABLE vendors   (id BIGINT PRIMARY KEY DEFAULT nextval('shared_seq'), name VARCHAR);

INSERT INTO customers (name) VALUES ('Alice'), ('Bob');   -- 1, 2
INSERT INTO vendors   (name) VALUES ('Acme'), ('Globex'); -- 3, 4
INSERT INTO customers (name) VALUES ('Carol');            -- 5
```

```
customers: 1 Alice, 2 Bob, 5 Carol
vendors:   3 Acme,  4 Globex
```

This is legal, but confusing. Give each table its
own sequence, named after the column:
`customer_id_seq`, `vendor_id_seq`, ...

---

## 11. Re-Running Your Script

A sequence is a named object, just like a table.
Creating it twice is an error:

```sql
CREATE SEQUENCE item_id_seq START 1;
-- Catalog Error: Sequence with name "item_id_seq" already exists!
```

A sequence also cannot be dropped while a table
still uses it:

```sql
DROP SEQUENCE item_id_seq;
-- Dependency Error: Cannot drop entry "item_id_seq"
-- because there are entries that depend on it.
```

To make a script safe to run again, **drop the
table first, then the sequence**, and then create
both again:

```sql
DROP TABLE IF EXISTS items;
DROP SEQUENCE IF EXISTS item_id_seq;

CREATE SEQUENCE item_id_seq START 1;
CREATE TABLE items (
    item_id BIGINT PRIMARY KEY DEFAULT nextval('item_id_seq'),
    name    VARCHAR NOT NULL
);
```

---

## 12. Summary

* DuckDB has **no** `AUTO_INCREMENT`, `AUTOINCREMENT`,
  `SERIAL`, or `IDENTITY` keyword.
* Auto-increment in DuckDB = **`CREATE SEQUENCE`** +
  **`DEFAULT nextval('seq_name')`**.
* Leave the ID column **out** of your `INSERT`;
  the sequence fills it in.
* If you insert your own IDs, the sequence does not
  know — later inserts may fail with a duplicate
  key error.
* IDs are **unique** but may have **gaps**.
* Use **one sequence per table**.
* To re-run a script: drop the table, then the
  sequence, then create both again.

---

## 13. References

1. [CREATE SEQUENCE Statement — DuckDB documentation](https://duckdb.org/docs/stable/sql/statements/create_sequence)
2. [Using AUTO_INCREMENT — MySQL Reference Manual](https://dev.mysql.com/doc/refman/9.7/en/example-auto-increment.html)

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
