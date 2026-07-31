CREATE TABLE students (id INT, name VARCHAR);
CREATE TABLE courses (id INT, title VARCHAR);
CREATE TABLE enrollments (student_id INT, course_id INT);

-- JOIN
SELECT s.name, c.title
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id;
