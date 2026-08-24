-- Table  Populations

-- Tables: { `users`, `roles`, `cities` } 

-- Database: DuckDB


-- sql
-- ---------------------
-- Populate Table: roles
-- ---------------------
INSERT INTO roles(id, role) VALUES
(1, 'admin'),
(2, 'user'),
(3, 'superuser'),
(4, 'tester'),
(5, 'QA');

-- ----------------------
-- Populate Table: cities
-- ----------------------
INSERT INTO cities(id, city) VALUES
(1, 'New York'),
(2, 'Philadelphia'),
(3, 'San Francisco'),
(4, 'Sunnyvale'),
(5, 'Cupertino'),
(6, 'Detroit');

-- ---------------------
-- Populate Table: users
-- ---------------------
INSERT INTO users(id, name, role_id, city_id) VALUES
(1, 'Alex', 1, 1),
(2, 'John', 1, 3),
(3, 'Alexis', 2, 2),
(4, 'Max', 2, 3),
(5, 'Barb', 3, 3),
(6, 'Jane', 2, 2),
(7, 'Max', 2, 3),
(8, 'Barb', 3, 3),
(9, 'Jane', 3, 4),
(10, 'Jo', 1, 1),
(11, 'Jack', 1, 2),
(12, 'Coco', 1, 3),
(13, 'Dave', 1, 1),
(14, 'Roger', 1, 2),
(15, 'Rafa', 1, 3),
(16, 'Stan', 1, 3),
(17, 'Mo', 1, 4);
