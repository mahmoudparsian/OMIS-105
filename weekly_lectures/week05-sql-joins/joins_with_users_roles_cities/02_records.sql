-- ============================================================
-- 02_records.sql -- Sample data
--
-- Tables:   roles (7 rows), cities (8 rows), users (36 rows)
-- Database: DuckDB
--
-- The data has gaps ON PURPOSE, so that LEFT JOIN ... IS NULL
-- has real rows to find:
--   * roles never assigned to a user:  tester (4), QA (5)
--   * cities with no users:            Cupertino (5), Detroit (6)
--   * users with no role  (role_id NULL):  ids 30, 31, 32, 35, 36
--   * users with no city  (city_id NULL):  ids 33, 34, 35, 36
--   * users with no role AND no city:      ids 35, 36
--   * every user name is unique
-- ============================================================

-- ---------------------
-- Populate Table: roles
-- ---------------------
INSERT INTO roles(id, role, description) VALUES
(1, 'admin',     'Manages users, roles, and system settings'),
(2, 'user',      'Uses everyday features of the tool'),
(3, 'superuser', 'Has extra rights beyond a regular user'),
(4, 'tester',    'Tests new features before release'),
(5, 'QA',        'Checks quality and reports defects'),
(6, 'developer', 'Builds and maintains the software'),
(7, 'analyst',   'Analyzes data and builds reports');

-- ----------------------
-- Populate Table: cities
-- ----------------------
-- population = 2020 U.S. Census count
INSERT INTO cities(id, city, population) VALUES
(1, 'New York',      8804190),
(2, 'Philadelphia',  1603797),
(3, 'San Francisco',  873965),
(4, 'Sunnyvale',      155805),
(5, 'Cupertino',       60381),
(6, 'Detroit',        639111),
(7, 'San Jose',      1013240),
(8, 'Santa Clara',    127647);

-- ---------------------
-- Populate Table: users
-- ---------------------
INSERT INTO users(id, name, role_id, city_id) VALUES
-- users with a role and a city
(1,  'Alex',    1, 1),
(2,  'John',    1, 3),
(3,  'Alexis',  2, 2),
(4,  'Max',     2, 3),
(5,  'Barb',    3, 3),
(6,  'Jane',    2, 2),
(7,  'Maria',   2, 3),
(8,  'Ben',     3, 3),
(9,  'Julia',   3, 4),
(10, 'Jo',      1, 1),
(11, 'Jack',    1, 2),
(12, 'Coco',    1, 3),
(13, 'Dave',    1, 1),
(14, 'Roger',   1, 2),
(15, 'Rafa',    1, 3),
(16, 'Stan',    1, 3),
(17, 'Mo',      1, 4),
(18, 'Priya',   6, 7),
(19, 'Carlos',  6, 8),
(20, 'Mei',     7, 7),
(21, 'Omar',    7, 8),
(22, 'Sofia',   6, 3),
(23, 'Liam',    7, 1),
(24, 'Aisha',   2, 7),
(25, 'Noah',    6, 8),
(26, 'Elena',   7, 2),
(27, 'Kenji',   3, 8),
(28, 'James',   2, 4),
(29, 'Fatima',  6, 7),
-- users with a city but NO role
(30, 'Diego',   NULL, 3),
(31, 'Hana',    NULL, 7),
(32, 'Victor',  NULL, 1),
-- users with a role but NO city
(33, 'Grace',   2,    NULL),
(34, 'Ravi',    6,    NULL),
-- users with NO role and NO city
(35, 'Zoe',     NULL, NULL),
(36, 'Tom',     NULL, NULL);
