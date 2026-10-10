-- ============================================================
-- db_records.sql -- Sample data for db_schema.sql
--
-- Tables:   authors (6 rows), books (20 rows), orders (80 rows)
-- Database: DuckDB
--
-- The data has gaps ON PURPOSE, so that LEFT JOIN ... IS NULL
-- has real rows to find:
--   * authors with no books:   5 (Priya Sharma), 6 (Omar Haddad)
--   * books never ordered:     B06, B12, B17, B20
--   * authors do not have an equal number of books:
--       author 1 -> 8 books, author 2 -> 6,
--       author 3 -> 4,       author 4 -> 2
-- ============================================================

-- create 6 authors, only 4 of them have published books
INSERT INTO authors(author_id, name, email, age, country) VALUES
(1, 'Maria Lopez',   'maria.lopez@example.com',   45, 'Spain'),
(2, 'James Carter',  'james.carter@example.com',  52, 'USA'),
(3, 'Aiko Tanaka',   'aiko.tanaka@example.com',   38, 'Japan'),
(4, 'Lars Nilsson',  'lars.nilsson@example.com',  61, 'Sweden'),
(5, 'Priya Sharma',  'priya.sharma@example.com',  29, 'India'),
(6, 'Omar Haddad',   'omar.haddad@example.com',   47, 'Egypt');

-- create 20 books (authors do not have equal number of publications)
-- books should be in 3 categories: SPORT, BUSINESS, COMPUTERS
INSERT INTO books(book_id, author_id, title, category, publication_year) VALUES
-- author 1: Maria Lopez (8 books)
('B01', 1, 'Data Science for Managers',      'COMPUTERS', 2019),
('B02', 1, 'SQL Made Simple',                'COMPUTERS', 2020),
('B03', 1, 'Databases in Practice',          'COMPUTERS', 2022),
('B04', 1, 'The Startup Playbook',           'BUSINESS',  2018),
('B05', 1, 'Leading Small Teams',            'BUSINESS',  2021),
('B06', 1, 'Running Your First Marathon',    'SPORT',     2017),
('B07', 1, 'Python for Business Analytics',  'COMPUTERS', 2023),
('B08', 1, 'Soccer Tactics Explained',       'SPORT',     2016),
-- author 2: James Carter (6 books)
('B09', 2, 'Marketing in the Digital Age',   'BUSINESS',  2019),
('B10', 2, 'Basketball Fundamentals',        'SPORT',     2015),
('B11', 2, 'Negotiation Basics',             'BUSINESS',  2020),
('B12', 2, 'Cloud Computing 101',            'COMPUTERS', 2021),
('B13', 2, 'Finance for Non-Finance People', 'BUSINESS',  2022),
('B14', 2, 'The Art of Tennis',              'SPORT',     2018),
-- author 3: Aiko Tanaka (4 books)
('B15', 3, 'Machine Learning Foundations',   'COMPUTERS', 2021),
('B16', 3, 'Swimming for Fitness',           'SPORT',     2019),
('B17', 3, 'Supply Chain Essentials',        'BUSINESS',  2023),
('B18', 3, 'Web Development Basics',         'COMPUTERS', 2024),
-- author 4: Lars Nilsson (2 books)
('B19', 4, 'Cycling Through the Alps',       'SPORT',     2020),
('B20', 4, 'Investing for Beginners',        'BUSINESS',  2024);

-- Create 80 orders
-- 4 of the books have never been bought by anyone: B06, B12, B17, B20
INSERT INTO orders(order_id, book_id, sale_price, order_date) VALUES
( 1, 'B13', 47, DATE '2025-01-05'),
( 2, 'B18', 34, DATE '2025-01-08'),
( 3, 'B01', 23, DATE '2025-01-17'),
( 4, 'B07', 43, DATE '2025-01-19'),
( 5, 'B02', 35, DATE '2025-01-23'),
( 6, 'B11', 31, DATE '2025-01-26'),
( 7, 'B10', 27, DATE '2025-02-03'),
( 8, 'B13', 49, DATE '2025-02-12'),
( 9, 'B13', 44, DATE '2025-02-13'),
(10, 'B07', 45, DATE '2025-02-14'),
(11, 'B04', 25, DATE '2025-02-15'),
(12, 'B01', 26, DATE '2025-02-16'),
(13, 'B01', 23, DATE '2025-02-24'),
(14, 'B11', 33, DATE '2025-02-25'),
(15, 'B09', 38, DATE '2025-02-27'),
(16, 'B09', 35, DATE '2025-03-02'),
(17, 'B01', 28, DATE '2025-03-03'),
(18, 'B03', 42, DATE '2025-03-15'),
(19, 'B19', 24, DATE '2025-03-26'),
(20, 'B15', 40, DATE '2025-03-27'),
(21, 'B05', 30, DATE '2025-04-06'),
(22, 'B14', 24, DATE '2025-04-08'),
(23, 'B02', 33, DATE '2025-04-18'),
(24, 'B03', 39, DATE '2025-04-19'),
(25, 'B09', 33, DATE '2025-04-20'),
(26, 'B01', 28, DATE '2025-04-22'),
(27, 'B09', 33, DATE '2025-04-29'),
(28, 'B01', 26, DATE '2025-05-01'),
(29, 'B15', 40, DATE '2025-05-01'),
(30, 'B02', 32, DATE '2025-05-04'),
(31, 'B07', 43, DATE '2025-05-06'),
(32, 'B04', 20, DATE '2025-05-06'),
(33, 'B13', 44, DATE '2025-05-15'),
(34, 'B16', 29, DATE '2025-05-18'),
(35, 'B13', 46, DATE '2025-05-19'),
(36, 'B07', 45, DATE '2025-05-23'),
(37, 'B11', 31, DATE '2025-05-24'),
(38, 'B07', 45, DATE '2025-05-27'),
(39, 'B05', 25, DATE '2025-06-04'),
(40, 'B07', 42, DATE '2025-06-10'),
(41, 'B03', 42, DATE '2025-06-14'),
(42, 'B10', 24, DATE '2025-06-17'),
(43, 'B03', 39, DATE '2025-06-23'),
(44, 'B01', 23, DATE '2025-06-24'),
(45, 'B13', 46, DATE '2025-06-28'),
(46, 'B15', 35, DATE '2025-06-28'),
(47, 'B01', 26, DATE '2025-06-28'),
(48, 'B03', 39, DATE '2025-07-05'),
(49, 'B05', 27, DATE '2025-07-06'),
(50, 'B03', 37, DATE '2025-07-06'),
(51, 'B13', 49, DATE '2025-07-18'),
(52, 'B02', 30, DATE '2025-07-31'),
(53, 'B09', 38, DATE '2025-08-12'),
(54, 'B02', 30, DATE '2025-08-14'),
(55, 'B08', 22, DATE '2025-08-15'),
(56, 'B11', 33, DATE '2025-08-30'),
(57, 'B05', 27, DATE '2025-09-07'),
(58, 'B05', 27, DATE '2025-09-09'),
(59, 'B10', 24, DATE '2025-09-23'),
(60, 'B03', 37, DATE '2025-09-28'),
(61, 'B18', 36, DATE '2025-10-01'),
(62, 'B04', 20, DATE '2025-10-15'),
(63, 'B11', 33, DATE '2025-10-23'),
(64, 'B15', 38, DATE '2025-11-04'),
(65, 'B15', 38, DATE '2025-11-13'),
(66, 'B10', 25, DATE '2025-11-15'),
(67, 'B02', 32, DATE '2025-11-26'),
(68, 'B03', 42, DATE '2025-11-27'),
(69, 'B03', 42, DATE '2025-11-28'),
(70, 'B19', 26, DATE '2025-11-30'),
(71, 'B03', 40, DATE '2025-12-03'),
(72, 'B07', 45, DATE '2025-12-05'),
(73, 'B08', 22, DATE '2025-12-06'),
(74, 'B15', 38, DATE '2025-12-13'),
(75, 'B07', 42, DATE '2025-12-16'),
(76, 'B01', 28, DATE '2025-12-17'),
(77, 'B02', 30, DATE '2025-12-17'),
(78, 'B16', 26, DATE '2025-12-21'),
(79, 'B09', 33, DATE '2025-12-21'),
(80, 'B16', 28, DATE '2025-12-25');
