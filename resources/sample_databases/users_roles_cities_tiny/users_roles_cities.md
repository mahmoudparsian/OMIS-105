# Tiny Database of Users, Roles, and Cities 

	For this tiny database, we create 3 
	tables using DuckDB, populate them, 
	and view the content of tbales.

# 1. Table Definitions

This is a tiny DuckDB database with 3 tables: 

* `users`
* `roles`
* `cities` 


---

```sql
-- ---------------
-- Table: roles --
-- ---------------
CREATE TABLE roles (
    id INTEGER PRIMARY KEY,
    role VARCHAR NOT NULL
);

-- ----------------
-- Table: cities --
-- ----------------
CREATE TABLE cities (
    id INTEGER PRIMARY KEY,
    city VARCHAR NOT NULL
);

-- ----------------
-- Table: users  --
-- ----------------
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    role_id INTEGER,
    city_id INTEGER,
    
    -- Defining the Foreign Key constraints
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (city_id) REFERENCES cities(id)
);
```

---

# 2. Table Populations

```sql
-- ---------------------
-- Populate Table: roles
-- ---------------------
INSERT INTO roles(id, role) VALUES
(1, 'admin'),
(2, 'user');

-- ----------------------
-- Populate Table: cities
-- ----------------------
INSERT INTO cities(id, city) VALUES
(1, 'New York'),
(2, 'Philadelphia'),
(3, 'San Francisco');

-- ---------------------
-- Populate Table: users
-- ---------------------
INSERT INTO users(id, name, role_id, city_id) VALUES
(1, 'Alex', 1, 1),
(2, 'John', 1, 3),
(3, 'Alexis', 2, 2);
```

---

# 3. View Tables

```sql
duckdb ▸ select * from roles;
┌───────┬─────────┐
│  id   │  role   │
│ int32 │ varchar │
├───────┼─────────┤
│     1 │ admin   │
│     2 │ user    │
└───────┴─────────┘

duckdb ▸ select * from cities;
┌───────┬───────────────┐
│  id   │     city      │
│ int32 │    varchar    │
├───────┼───────────────┤
│     1 │ New York      │
│     2 │ Philadelphia  │
│     3 │ San Francisco │
└───────┴───────────────┘

duckdb ▸ select * from users;
┌───────┬─────────┬─────────┬─────────┐
│  id   │  name   │ role_id │ city_id │
│ int32 │ varchar │  int32  │  int32  │
├───────┼─────────┼─────────┼─────────┤
│     1 │ Alex    │       1 │       1 │
│     2 │ John    │       1 │       3 │
│     3 │ Alexis  │       2 │       2 │
└───────┴─────────┴─────────┴─────────┘
```
