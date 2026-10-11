-- ============================================================
-- db_messy.sql -- Builds the "raw import" tables for data_quality.py
--
-- SPOILER: this file lists every planted problem.
--          Try data_quality.py first.
--
-- Run by create_messy_database.sh, AFTER ../db_schema.sql and
-- ../db_records.sql. It copies the clean tables into raw_students,
-- raw_courses, and raw_grades, then plants problems in the copies.
--
-- The raw_ tables pretend to be an export from an old system:
-- every text column is plain VARCHAR, and there are no PRIMARY KEY,
-- FOREIGN KEY, NOT NULL, or ENUM rules. So bad data gets in.
--
-- Finally the clean tables and ENUM types are dropped, so only
-- the raw_ tables remain.
--
-- Result:
--     raw_students:   504 rows  (500 + 4 duplicates)
--     raw_courses:     50 rows
--     raw_grades:   8,013 rows  (8,000 + 13 extra)
-- ============================================================

CREATE TABLE raw_students AS
SELECT student_id,
       first_name,
       last_name,
       CAST(major   AS VARCHAR) AS major,
       CAST(gender  AS VARCHAR) AS gender,
       CAST(country AS VARCHAR) AS country
FROM students;

CREATE TABLE raw_courses AS
SELECT course_id,
       course_name,
       CAST(course_level AS VARCHAR) AS course_level,
       num_of_credits
FROM courses;

CREATE TABLE raw_grades AS
SELECT grade_id,
       student_id,
       course_id,
       year,
       CAST(grade AS VARCHAR) AS grade
FROM grades;

-- ------------------------------------------------------------
-- raw_students
-- ------------------------------------------------------------

-- [DQ2, DQ3] 3 exact duplicate rows: the same student imported twice
INSERT INTO raw_students
SELECT * FROM raw_students WHERE student_id IN (12, 205, 333);

-- [DQ2] 1 conflicting duplicate: same student_id, different major
INSERT INTO raw_students
SELECT student_id, first_name, last_name, 'FINANCE', gender, country
FROM raw_students WHERE student_id = 88;

-- [DQ4, DQ5] 6 non-standard country spellings
UPDATE raw_students SET country = 'usa'           WHERE student_id = 3;
UPDATE raw_students SET country = 'United States' WHERE student_id = 6;
UPDATE raw_students SET country = 'U.S.A.'        WHERE student_id = 18;
UPDATE raw_students SET country = ' INDIA'        WHERE student_id = 1;   -- leading space
UPDATE raw_students SET country = 'india'         WHERE student_id = 4;
UPDATE raw_students SET country = 'China '        WHERE student_id = 22;  -- trailing space

-- [DQ6] 3 missing names: 2 NULL, 1 empty string
UPDATE raw_students SET last_name  = NULL WHERE student_id IN (20, 21);
UPDATE raw_students SET first_name = ''   WHERE student_id = 30;

-- [DQ7] 4 invalid gender codes
UPDATE raw_students SET gender = 'M'      WHERE student_id = 31;
UPDATE raw_students SET gender = 'F'      WHERE student_id = 32;
UPDATE raw_students SET gender = 'Female' WHERE student_id = 33;
UPDATE raw_students SET gender = 'male'   WHERE student_id = 19;

-- ------------------------------------------------------------
-- raw_courses
-- ------------------------------------------------------------

-- [DQ8] 1 course with 0 credits, 2 invalid course levels
UPDATE raw_courses SET num_of_credits = 0     WHERE course_id = 'BUS106';
UPDATE raw_courses SET course_level = 'Graduate' WHERE course_id = 'CSCI201';
UPDATE raw_courses SET course_level = 'grad'     WHERE course_id = 'FIN202';

-- ------------------------------------------------------------
-- raw_grades
-- ------------------------------------------------------------

-- [DQ9] 4 grades for students who do not exist
INSERT INTO raw_grades VALUES
   (8001, 9001, 'BUS101',  2024, 'B'),
   (8002, 9001, 'CSCI101', 2024, 'A'),
   (8003, 9002, 'MATH101', 2025, 'C'),
   (8004, 9002, 'FIN101',  2025, 'B');

-- [DQ10] 5 grades for courses that do not exist:
--        2 for a made-up course, 3 with a lowercase course_id
INSERT INTO raw_grades VALUES
   (8005, 60, 'CSCI999', 2025, 'A'),
   (8006, 61, 'CSCI999', 2025, 'B');
UPDATE raw_grades SET course_id = lower(course_id) WHERE grade_id IN (401, 402, 403);

-- [DQ11] 4 years outside 2021-2025: 3 in the future, 1 typo
UPDATE raw_grades SET year = 2027 WHERE grade_id IN (101, 102, 103);
UPDATE raw_grades SET year = 1925 WHERE grade_id = 104;

-- [DQ12] 5 invalid letter grades + 2 missing (NULL) grades
UPDATE raw_grades SET grade = 'A+' WHERE grade_id IN (201, 202);
UPDATE raw_grades SET grade = 'E'  WHERE grade_id = 203;
UPDATE raw_grades SET grade = 'b'  WHERE grade_id IN (204, 205);
UPDATE raw_grades SET grade = NULL WHERE grade_id IN (301, 302);

-- [DQ13] 5 duplicate enrollments: the same grade loaded twice,
--        under a new grade_id
INSERT INTO raw_grades
SELECT grade_id + 7506, student_id, course_id, year, grade   -- 501..505 -> 8007..8011
FROM raw_grades WHERE grade_id BETWEEN 501 AND 505;

-- [DQ14] 2 reused grade_ids: a new, different grade under an old id
INSERT INTO raw_grades VALUES
   (600, 83,  'BUS101', 2022, 'B'),
   (700, 127, 'BUS102', 2022, 'A');

-- ------------------------------------------------------------
-- Keep only the raw_ tables
-- ------------------------------------------------------------
DROP TABLE grades;
DROP TABLE students;
DROP TABLE courses;
DROP TYPE level_type;
DROP TYPE major_type;
DROP TYPE country_type;
DROP TYPE grade_type;
DROP TYPE gender_type;
