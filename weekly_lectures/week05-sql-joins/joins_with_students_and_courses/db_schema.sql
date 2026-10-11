-- ------------------------------------------------------------------
-- A small university holds the following
-- tables to track the grades for students.
--
-- Each student may take any number of courses.
--
-- Students ('undergraduate', 'graduate')
-- are from the following countries:
-- ('USA', 'CANADA', 'CHINA', 'INDIA', 'GERMANY', 'MEXICO', 'ITALY');
--
-- Most of the students are from USA, CHINA, and INDIA
--
-- ------------------------------------------------------------------

CREATE TYPE level_type AS ENUM 
   ('undergraduate', 'graduate');
   
CREATE TYPE major_type AS ENUM 
   ('BUSINESS', 'ENGINEERING', 'MATH', 'COMPUTER-SCIENCE', 'FINANCE');

CREATE TYPE country_type AS ENUM 
   ('USA', 'CANADA', 'CHINA', 'INDIA', 'GERMANY', 'MEXICO', 'ITALY');

CREATE TYPE grade_type AS ENUM 
   ('A', 'B', 'C', 'D', 'F');

CREATE TYPE gender_type AS ENUM 
   ('MALE', 'FEMALE', 'NA');
   
-- courses
CREATE TABLE courses (
   course_id VARCHAR PRIMARY KEY,
   course_name VARCHAR NOT NULL,
   course_level level_type NOT NULL,
   num_of_credits INT NOT NULL
);

-- students
CREATE TABLE students (
   student_id INT PRIMARY KEY,
   first_name VARCHAR NOT NULL,
   last_name VARCHAR NOT NULL,
   major major_type NOT NULL,
   gender gender_type NOT NULL,
   country  country_type NOT NULL
);

-- grades
CREATE TABLE grades (
   grade_id INT PRIMARY KEY,
   student_id INT NOT NULL,     -- REFERENCES students(student_id)
   course_id VARCHAR NOT NULL,  -- REFERENCES courses(course_id)
   year INT NOT NULL, -- 'YYYY'
   grade grade_type NOT NULL,
   
   -- every grades.student_id must exist in students
   FOREIGN KEY (student_id) REFERENCES students(student_id),
   
   -- every grades.course_id must exist in courses
   FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
