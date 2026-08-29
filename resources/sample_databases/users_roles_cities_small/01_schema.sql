-- Table Definitions

-- Tables: { `users`, `roles`, `cities` } 

-- Database: DuckDB



-- sql
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
