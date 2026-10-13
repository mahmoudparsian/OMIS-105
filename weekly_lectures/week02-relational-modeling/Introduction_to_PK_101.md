# Learning Primary Keys with DuckDB: A Beginner's Guide

Welcome to the world of databases! If you're just getting started, think of a **Primary Key (PK)** as the ultimate **VIP ID badge** for your data. 

Imagine you run an animal shelter. You might have two different dogs named "Max". If someone says, *"Feed Max,"* how do you know *which* Max they mean? 

That is why databases use a **Primary Key**. It is a column (or set of columns) where **every single value is completely unique and can never be empty (`NULL`)**.

---

## Step 1: Creating a Table with a Primary Key in DuckDB

Let's create a very simple table for our shelter using DuckDB. We will make `pet_id` our Primary Key.

```sql
CREATE TABLE pets (
    pet_id INTEGER PRIMARY KEY,
    name VARCHAR,
    species VARCHAR
);
```

* **`pet_id INTEGER PRIMARY KEY`**: 
	* This tells DuckDB: *This number identifies each pet.* 
	* Make sure no two pets share the same `pet_id`, and every pet must have one."

---

## Step 2: Adding a Few Sample Rows

Now, let's insert three adorable animals into our DuckDB table:

```sql
INSERT INTO pets (pet_id, name, species)
VALUES 
    (1, 'Luna', 'Cat'),
    (2, 'Max', 'Dog'),
    (3, 'Charlie', 'Bird');
```

If we look inside our DuckDB table now (`SELECT * FROM pets;`), it looks like this:

| pet_id | name | species |
| :--- | :--- | :--- |
| **1** | Luna | Cat |
| **2** | Max | Dog |
| **3** | Charlie | Bird |

---

## Step 3: Why is the Primary Key so powerful? (The Rules)

Because `pet_id` is a Primary Key, DuckDB strictly enforces two ironclad rules:

1. **No Duplicates (Uniqueness):** You cannot have two rows with the same `pet_id`.

2. **No Blanks (Not Null):** You cannot leave the `pet_id` empty.

### What happens if you break the rule?
Suppose a new dog named "Bella" arrives, and you accidentally try to give her `pet_id = 1` (which already belongs to Luna):

```sql
INSERT INTO pets VALUES (1, 'Bella', 'Dog');
```

**DuckDB will immediately put its foot down and throw an error like this:**

> **Constraint Error:** <br>
> Duplicate key "pet_id: 1" violates primary key constraint.

DuckDB protects your data from getting mixed up or overwritten by refusing to let you make that mistake!

---
## DuckDB DEMO Session 

```sql
% duckdb
DuckDB v1.5.5 (Variegata)

duckdb ▸ CREATE TABLE pets (
             pet_id INTEGER PRIMARY KEY,
             name VARCHAR,
             species VARCHAR
         );

duckdb ▸ DESC pets;
┌──────────────────────────┐
│           pets           │
│                          │
│ pet_id  integer not null │
│ name    varchar          │
│ species varchar          │
└──────────────────────────┘

duckdb ▸ .schema
CREATE TABLE pets(
   pet_id INTEGER PRIMARY KEY, 
   "name" VARCHAR, 
   species VARCHAR
);


duckdb ▸ INSERT INTO pets VALUES
             (1, 'Luna', 'Cat'),
             (2, 'Max', 'Dog'),
             (3, 'Charlie', 'Bird');

duckdb ▸ SELECT * FROM pets;
┌────────┬─────────┬─────────┐
│ pet_id │  name   │ species │
│ int32  │ varchar │ varchar │
├────────┼─────────┼─────────┤
│      1 │ Luna    │ Cat     │
│      2 │ Max     │ Dog     │
│      3 │ Charlie │ Bird    │
└────────┴─────────┴─────────┘


duckdb ▸ INSERT INTO pets (pet_id, name, species)
         VALUES (4, 'Max', 'Cat');

duckdb ▸ SELECT * FROM pets;
┌────────┬─────────┬─────────┐
│ pet_id │  name   │ species │
│ int32  │ varchar │ varchar │
├────────┼─────────┼─────────┤
│      1 │ Luna    │ Cat     │
│      2 │ Max     │ Dog     │
│      3 │ Charlie │ Bird    │
│      4 │ Max     │ Cat     │
└────────┴─────────┴─────────┘

duckdb ▸ INSERT INTO pets (pet_id, name, species)
         VALUES (5, 'Max', 'Cat');

duckdb ▸ SELECT * FROM pets;
┌────────┬─────────┬─────────┐
│ pet_id │  name   │ species │
│ int32  │ varchar │ varchar │
├────────┼─────────┼─────────┤
│      1 │ Luna    │ Cat     │
│      2 │ Max     │ Dog     │
│      3 │ Charlie │ Bird    │
│      4 │ Max     │ Cat     │
│      5 │ Max     │ Cat     │
└────────┴─────────┴─────────┘

duckdb ▸ INSERT INTO pets (pet_id, name, species)
         VALUES (5, 'Pishi', 'Cat');
Constraint Error:
Duplicate key "pet_id: 5" violates primary key constraint.

duckdb ▸ SELECT * FROM pets;
┌────────┬─────────┬─────────┐
│ pet_id │  name   │ species │
│ int32  │ varchar │ varchar │
├────────┼─────────┼─────────┤
│      1 │ Luna    │ Cat     │
│      2 │ Max     │ Dog     │
│      3 │ Charlie │ Bird    │
│      4 │ Max     │ Cat     │
│      5 │ Max     │ Cat     │
└────────┴─────────┴─────────┘

duckdb ▸ SELECT * FROM pets WHERE pet_id = 4;
┌────────┬─────────┬─────────┐
│ pet_id │  name   │ species │
│ int32  │ varchar │ varchar │
├────────┼─────────┼─────────┤
│      4 │ Max     │ Cat     │
└────────┴─────────┴─────────┘

duckdb ▸ SELECT * FROM pets WHERE pet_id = 5;
┌────────┬─────────┬─────────┐
│ pet_id │  name   │ species │
│ int32  │ varchar │ varchar │
├────────┼─────────┼─────────┤
│      5 │ Max     │ Cat     │
└────────┴─────────┴─────────┘

duckdb ▸ SELECT * FROM pets;
┌────────┬─────────┬─────────┐
│ pet_id │  name   │ species │
│ int32  │ varchar │ varchar │
├────────┼─────────┼─────────┤
│      1 │ Luna    │ Cat     │
│      2 │ Max     │ Dog     │
│      3 │ Charlie │ Bird    │
│      4 │ Max     │ Cat     │
│      5 │ Max     │ Cat     │
└────────┴─────────┴─────────┘

duckdb ▸ DELETE FROM pets WHERE pet_id = 3;

duckdb ▸ SELECT * FROM pets;
┌────────┬─────────┬─────────┐
│ pet_id │  name   │ species │
│ int32  │ varchar │ varchar │
├────────┼─────────┼─────────┤
│      1 │ Luna    │ Cat     │
│      2 │ Max     │ Dog     │
│      4 │ Max     │ Cat     │
│      5 │ Max     │ Cat     │
└────────┴─────────┴─────────┘

duckdb ▸ UPDATE pets
         SET name = 'PishiNaz'
         WHERE pet_id = 1;

duckdb ▸ SELECT * FROM pets;
┌────────┬──────────┬─────────┐
│ pet_id │   name   │ species │
│ int32  │ varchar  │ varchar │
├────────┼──────────┼─────────┤
│      1 │ PishiNaz │ Cat     │
│      2 │ Max      │ Dog     │
│      4 │ Max      │ Cat     │
│      5 │ Max      │ Cat     │
└────────┴──────────┴─────────┘

```

## Summary Checklist
* **Primary Key:** A unique identifier for every row in a table.
* **Analogy:** Like a Social Security Number, a Passport Number, or a Student ID. 
* **DuckDB Behavior:** Automatically checks for duplicates and missing values to keep your data clean and trustworthy.
