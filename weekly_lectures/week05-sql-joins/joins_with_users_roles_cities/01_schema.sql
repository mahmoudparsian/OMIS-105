-- ============================================================
-- 01_schema.sql -- Table definitions
--
-- Tables:   roles, cities, users
-- Database: DuckDB
--
-- Create order matters: roles and cities come first, because
-- users has FOREIGN KEYs that point to them.
-- ============================================================

-- ---------------
-- Table: roles --
-- ---------------
CREATE TABLE roles (
    id          INTEGER PRIMARY KEY,
    role        VARCHAR NOT NULL,
    description VARCHAR NOT NULL    -- what this role is allowed to do
);

-- ----------------
-- Table: cities --
-- ----------------
CREATE TABLE cities (
    id         INTEGER PRIMARY KEY,
    city       VARCHAR NOT NULL,
    population INTEGER NOT NULL     -- 2020 U.S. Census count
);

-- ----------------
-- Table: users  --
-- ----------------
-- role_id and city_id are allowed to be NULL on purpose:
-- NULL means "not assigned yet". A FOREIGN KEY accepts NULL,
-- but any non-NULL value must exist in roles.id / cities.id.
CREATE TABLE users (
    id      INTEGER PRIMARY KEY,
    name    VARCHAR NOT NULL,
    role_id INTEGER,
    city_id INTEGER,

    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (city_id) REFERENCES cities(id)
);
