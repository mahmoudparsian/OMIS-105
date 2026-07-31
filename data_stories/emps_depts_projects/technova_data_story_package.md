
# Employee-Department-Project Analytics – Data Story, Schema, Sample Data, and Queries

## Data Story (Business Requirement)

TechNova is a global technology consultancy that employs specialists from over ten countries. Each **employee** belongs to exactly one **department** (such as Engineering, Marketing, or HR), which determines their career development path and reporting structure. Departments manage budgets, track headcounts, and often need insights into staffing distribution across geographies. Management wants to know which departments are growing fastest, how average salaries differ by country, and which teams are most effective at retaining talent.

Employees also work on multiple **projects** throughout the year, reflecting the dynamic, cross-functional nature of consulting. Projects can be local or global, and often involve collaboration across departments. Leadership needs to understand which employees are working on the most projects, how project workloads are distributed by department, and which projects are contributing most to billable hours. By analyzing the links between employees, departments, and projects, TechNova can better allocate resources, plan future hiring, and identify rising stars within the workforce.

---

## MySQL Schema
```sql

CREATE DATABASE IF NOT EXISTS technova;
USE technova;

CREATE TABLE departments (
  dept_id INT PRIMARY KEY,
  dept_name VARCHAR(50) NOT NULL
);

CREATE TABLE employees (
  emp_id INT PRIMARY KEY,
  first_name VARCHAR(40) NOT NULL,
  last_name  VARCHAR(40) NOT NULL,
  country    VARCHAR(40) NOT NULL,
  dept_id    INT NOT NULL,
  salary     INT NOT NULL,
  hire_date  DATE NOT NULL,
  FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE projects (
  proj_id INT PRIMARY KEY,
  proj_name VARCHAR(100) NOT NULL,
  start_date DATE NOT NULL,
  end_date   DATE
);

CREATE TABLE employee_projects (
  emp_id  INT NOT NULL,
  proj_id INT NOT NULL,
  role    VARCHAR(50),
  PRIMARY KEY (emp_id, proj_id),
  FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
  FOREIGN KEY (proj_id) REFERENCES projects(proj_id)
);

```

## Sample Data (INSERTS)
```sql
INSERT INTO departments(dept_id, dept_name) VALUES
(1,'Engineering'),
(2,'Marketing'),
(3,'HR'),
(4,'Finance'),
(5,'Sales');
```
```sql
INSERT INTO employees(emp_id,first_name,last_name,country,dept_id,salary,hire_date) VALUES
(1,'Bob','Jones','CANADA',4,94937,'2016-03-17'),
(2,'Bob','Davis','FRANCE',3,66802,'2016-10-15'),
(3,'Eve','Miller','FRANCE',2,81466,'2015-01-07'),
(4,'Oscar','Johnson','UK',1,60864,'2018-07-16'),
(5,'Paul','Johnson','USA',1,147443,'2016-08-05'),
(6,'Eve','Smith','MEXICO',4,135157,'2020-05-07'),
(7,'Ivy','Garcia','USA',3,105018,'2020-11-06'),
(8,'Quinn','Brown','FRANCE',1,112197,'2022-03-31'),
(9,'Rita','Davis','JAPAN',5,147617,'2019-09-15'),
(10,'Mona','Rodriguez','USA',2,70827,'2020-06-17'),
(11,'Ivy','Williams','FRANCE',3,132640,'2019-05-22'),
(12,'Carol','Garcia','UK',5,104054,'2015-03-08'),
(13,'Grace','Martinez','CANADA',3,61681,'2018-12-12'),
(14,'Hank','Davis','USA',3,124851,'2022-01-24'),
(15,'Hank','Rodriguez','JAPAN',2,80153,'2021-01-06'),
(16,'Paul','Davis','JAPAN',1,61330,'2016-07-05'),
(17,'Paul','Brown','USA',3,106143,'2022-09-06'),
(18,'Ivy','Davis','UK',1,74237,'2021-12-04'),
(19,'Carol','Rodriguez','FRANCE',1,70866,'2019-11-10'),
(20,'Alice','Rodriguez','UK',1,131641,'2022-10-14');
```
```sql
INSERT INTO projects(proj_id,proj_name,start_date,end_date) VALUES
(1,'AI Platform','2022-10-13','2023-08-15'),
(2,'Cloud Migration','2021-01-30','2021-10-22'),
(3,'Data Warehouse','2021-09-26','2023-05-08'),
(4,'Mobile App','2022-04-29','2022-08-23'),
(5,'E-commerce Site','2023-02-08','2024-03-01'),
(6,'Cybersecurity Audit','2021-12-09','2022-10-17'),
(7,'ERP Implementation','2021-12-23','2022-04-14'),
(8,'Marketing Analytics','2022-10-17','2023-12-16');
```
```sql
INSERT INTO employee_projects(emp_id,proj_id,role) VALUES
(6,7,'Developer'),
(5,6,'Architect'),
(3,1,'Architect'),
(13,5,'Manager'),
(10,7,'Developer'),
(4,3,'Architect'),
(13,7,'Developer'),
(5,8,'Tester'),
(12,8,'Analyst'),
(6,6,'Architect'),
(17,3,'Analyst'),
(17,2,'Architect'),
(12,4,'Architect'),
(11,2,'Analyst'),
(17,4,'Developer'),
(11,5,'Tester'),
(2,2,'Manager'),
(7,5,'Architect'),
(8,2,'Architect'),
(18,3,'Architect'),
(13,1,'Analyst'),
(19,8,'Analyst'),
(13,4,'Architect'),
(5,1,'Architect'),
(20,8,'Analyst'),
(19,2,'Developer'),
(14,6,'Analyst'),
(7,8,'Analyst'),
(7,3,'Tester'),
(2,7,'Tester'),
(17,5,'Manager'),
(18,7,'Analyst'),
(3,5,'Developer'),
(9,6,'Developer');
```

---

# Query Library (60)
## Basic Queries (20)

**1. List all employees**

```sql
SELECT * FROM employees;
```

**2. List all departments**

```sql
SELECT * FROM departments;
```

**3. List all projects**

```sql
SELECT * FROM projects;
```

**4. Show employee names and salaries**

```sql
SELECT first_name,last_name,salary FROM employees;
```

**5. Show employees from India**

```sql
SELECT * FROM employees WHERE country='INDIA';
```

**6. Find employees earning over 100000**

```sql
SELECT * FROM employees WHERE salary>100000;
```

**7. Show top 5 highest salaries**

```sql
SELECT * FROM employees ORDER BY salary DESC LIMIT 5;
```

**8. Show employees hired after 2020**

```sql
SELECT * FROM employees WHERE hire_date>'2020-01-01';
```

**9. Show distinct countries**

```sql
SELECT DISTINCT country FROM employees;
```

**10. Count total employees**

```sql
SELECT COUNT(*) FROM employees;
```

**11. Average salary overall**

```sql
SELECT AVG(salary) FROM employees;
```

**12. Minimum and maximum salary**

```sql
SELECT MIN(salary),MAX(salary) FROM employees;
```

**13. List project names starting with 'C'**

```sql
SELECT * FROM projects WHERE proj_name LIKE 'C%';
```

**14. Find department by id=3**

```sql
SELECT * FROM departments WHERE dept_id=3;
```

**15. List employees ordered by country**

```sql
SELECT * FROM employees ORDER BY country;
```

**16. Find employees with last name = 'Smith'**

```sql
SELECT * FROM employees WHERE last_name='Smith';
```

**17. Count employees from USA**

```sql
SELECT COUNT(*) FROM employees WHERE country='USA';
```

**18. List first 10 projects**

```sql
SELECT * FROM projects LIMIT 10;
```

**19. Show employees not from USA**

```sql
SELECT * FROM employees WHERE country<>'USA';
```

**20. List employees sorted by hire_date**

```sql
SELECT * FROM employees ORDER BY hire_date;
```

## Basic-to-Intermediate Queries (20)

**1. Join employees with departments**

```sql
SELECT e.first_name,e.last_name,d.dept_name FROM employees e JOIN departments d ON e.dept_id=d.dept_id;
```

**2. Count employees per department**

```sql
SELECT d.dept_name,COUNT(*) FROM employees e JOIN departments d ON e.dept_id=d.dept_id GROUP BY d.dept_name;
```

**3. Average salary per department**

```sql
SELECT d.dept_name,AVG(e.salary) FROM employees e JOIN departments d ON e.dept_id=d.dept_id GROUP BY d.dept_name;
```

**4. Find departments with avg salary > 100k**

```sql
SELECT d.dept_name FROM employees e JOIN departments d ON e.dept_id=d.dept_id GROUP BY d.dept_name HAVING AVG(e.salary)>100000;
```

**5. Employees and their projects**

```sql
SELECT e.first_name,e.last_name,p.proj_name FROM employees e JOIN employee_projects ep ON e.emp_id=ep.emp_id JOIN projects p ON ep.proj_id=p.proj_id;
```

**6. Projects with number of employees**

```sql
SELECT p.proj_name,COUNT(*) FROM employee_projects ep JOIN projects p ON ep.proj_id=p.proj_id GROUP BY p.proj_name;
```

**7. Employees working on 'AI Platform'**

```sql
SELECT e.first_name,e.last_name FROM employees e JOIN employee_projects ep ON e.emp_id=ep.emp_id JOIN projects p ON ep.proj_id=p.proj_id WHERE p.proj_name='AI Platform';
```

**8. Departments with project counts**

```sql
SELECT d.dept_name,COUNT(DISTINCT ep.proj_id) FROM employees e JOIN departments d ON e.dept_id=d.dept_id JOIN employee_projects ep ON e.emp_id=ep.emp_id GROUP BY d.dept_name;
```

**9. Top 3 projects by employees assigned**

```sql
SELECT p.proj_name,COUNT(*) c FROM employee_projects ep JOIN projects p ON ep.proj_id=p.proj_id GROUP BY p.proj_name ORDER BY c DESC LIMIT 3;
```

**10. Employees with multiple projects**

```sql
SELECT e.emp_id,e.first_name,COUNT(ep.proj_id) FROM employees e JOIN employee_projects ep ON e.emp_id=ep.emp_id GROUP BY e.emp_id,e.first_name HAVING COUNT(ep.proj_id)>1;
```

**11. Employees and roles on projects**

```sql
SELECT e.first_name,p.proj_name,ep.role FROM employees e JOIN employee_projects ep ON e.emp_id=ep.emp_id JOIN projects p ON ep.proj_id=p.proj_id;
```

**12. Projects without employees**

```sql
SELECT p.* FROM projects p LEFT JOIN employee_projects ep ON p.proj_id=ep.proj_id WHERE ep.emp_id IS NULL;
```

**13. Employees without projects**

```sql
SELECT e.* FROM employees e LEFT JOIN employee_projects ep ON e.emp_id=ep.emp_id WHERE ep.proj_id IS NULL;
```

**14. Departments and avg salary sorted desc**

```sql
SELECT d.dept_name,AVG(e.salary) FROM employees e JOIN departments d ON e.dept_id=d.dept_id GROUP BY d.dept_name ORDER BY AVG(e.salary) DESC;
```

**15. Projects started after 2022**

```sql
SELECT * FROM projects WHERE start_date>'2022-01-01';
```

**16. Projects ending in 2024**

```sql
SELECT * FROM projects WHERE end_date<'2024-12-31';
```

**17. Number of projects per employee**

```sql
SELECT e.first_name,COUNT(ep.proj_id) FROM employees e JOIN employee_projects ep ON e.emp_id=ep.emp_id GROUP BY e.first_name;
```

**18. Highest paid employee in each department**

solution-1:

```sql
SELECT d.dept_name,e.first_name,e.salary FROM employees e JOIN departments d ON e.dept_id=d.dept_id WHERE e.salary=(SELECT MAX(salary) FROM employees WHERE dept_id=d.dept_id);
```

solution-2:

```sql
WITH dept_max AS (
    SELECT dept_id, MAX(salary) AS max_salary
    FROM employees
    GROUP BY dept_id
)
SELECT d.dept_name,
       e.first_name,
       e.salary
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
JOIN dept_max dm ON e.dept_id = dm.dept_id
                AND e.salary = dm.max_salary;
```

🔎 Explanation:

	1.	The dept_max CTE computes the maximum salary per department.
	
	2.	Then we join employees and departments with this CTE.
	
	3.	The condition e.salary = dm.max_salary ensures we only return 
	    employees who earn the max salary in their department.


**19. Average project duration**

```sql
SELECT AVG(DATEDIFF(end_date,start_date)) FROM projects;
```

**20. Employees and their departments with country**

```sql
SELECT e.first_name,e.country,d.dept_name FROM employees e JOIN departments d ON e.dept_id=d.dept_id;
```

## Intermediate Queries (20)

**1. CTE: rank employees by salary**

```sql
WITH ranked AS (
  SELECT e.*,RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) rnk FROM employees e)
SELECT * FROM ranked WHERE rnk=1;
```

**2. CTE: top 2 projects per department**

```sql
WITH dept_proj AS (
  SELECT d.dept_name,p.proj_name,COUNT(*) c FROM employees e JOIN departments d ON e.dept_id=d.dept_id JOIN employee_projects ep ON e.emp_id=ep.emp_id JOIN projects p ON ep.proj_id=p.proj_id GROUP BY d.dept_name,p.proj_name)
, ranked AS (
  SELECT *,ROW_NUMBER() OVER(PARTITION BY dept_name ORDER BY c DESC) rn FROM dept_proj)
SELECT * FROM ranked WHERE rn<=2;
```

**3. Window: salary z-score per department**

```sql
SELECT emp_id,dept_id,(salary-AVG(salary) OVER(PARTITION BY dept_id))/NULLIF(STDDEV_POP(salary) OVER(PARTITION BY dept_id),0) z FROM employees;
```

**4. Total salary per project**

```sql
SELECT p.proj_name,SUM(e.salary) FROM employees e JOIN employee_projects ep ON e.emp_id=ep.emp_id JOIN projects p ON ep.proj_id=p.proj_id GROUP BY p.proj_name;
```

**5. Departments with employees in more than 3 countries**

```sql
SELECT d.dept_name,COUNT(DISTINCT e.country) c FROM employees e JOIN departments d ON e.dept_id=d.dept_id GROUP BY d.dept_name HAVING c>3;
```

**6. Employees with most projects**

```sql
SELECT e.emp_id,e.first_name,COUNT(ep.proj_id) c FROM employees e JOIN employee_projects ep ON e.emp_id=ep.emp_id GROUP BY e.emp_id,e.first_name ORDER BY c DESC LIMIT 5;
```

**7. Project participation by country**

```sql
SELECT e.country,p.proj_name,COUNT(*) FROM employees e JOIN employee_projects ep ON e.emp_id=ep.emp_id JOIN projects p ON ep.proj_id=p.proj_id GROUP BY e.country,p.proj_name;
```

**8. Longest running project**

```sql
SELECT proj_name,DATEDIFF(end_date,start_date) dur FROM projects ORDER BY dur DESC LIMIT 1;
```

**9. Employees in multiple departments (should be none)**

```sql
SELECT emp_id,COUNT(DISTINCT dept_id) FROM employees GROUP BY emp_id HAVING COUNT(DISTINCT dept_id)>1;
```

**10. Department with highest avg tenure**

```sql
SELECT d.dept_name,AVG(DATEDIFF(CURDATE(),hire_date)/365) tenure FROM employees e JOIN departments d ON e.dept_id=d.dept_id GROUP BY d.dept_name ORDER BY tenure DESC LIMIT 1;
```

**11. Projects with at least 5 employees**

```sql
SELECT p.proj_name,COUNT(*) c FROM projects p JOIN employee_projects ep ON p.proj_id=ep.proj_id GROUP BY p.proj_name HAVING c>=5;
```

**12. Countries with most projects assigned**

```sql
SELECT e.country,COUNT(DISTINCT ep.proj_id) c FROM employees e JOIN employee_projects ep ON e.emp_id=ep.emp_id GROUP BY e.country ORDER BY c DESC;
```

**13. Employees who are Managers**

```sql
SELECT e.first_name,e.last_name,p.proj_name FROM employees e JOIN employee_projects ep ON e.emp_id=ep.emp_id JOIN projects p ON ep.proj_id=p.proj_id WHERE ep.role='Manager';
```

**14. Average salary per country**

```sql
SELECT country,AVG(salary) FROM employees GROUP BY country;
```

**15. Project with most departments involved**

```sql
SELECT p.proj_name,COUNT(DISTINCT e.dept_id) c FROM projects p JOIN employee_projects ep ON p.proj_id=ep.proj_id JOIN employees e ON e.emp_id=ep.emp_id GROUP BY p.proj_name ORDER BY c DESC LIMIT 1;
```

**16. Employees without projects using NOT EXISTS**

```sql
SELECT * FROM employees e WHERE NOT EXISTS (SELECT 1 FROM employee_projects ep WHERE ep.emp_id=e.emp_id);
```

**17. Department-country employee matrix**

```sql
SELECT d.dept_name,e.country,COUNT(*) FROM employees e JOIN departments d ON e.dept_id=d.dept_id GROUP BY d.dept_name,e.country;
```

**18. Employee with highest salary overall**

```sql
SELECT * FROM employees ORDER BY salary DESC LIMIT 1;
```

**19. Average employees per project**

```sql
SELECT AVG(c) FROM (SELECT COUNT(*) c FROM employee_projects GROUP BY proj_id) t;
```

**20. Departments and their highest paid employee using window**

```sql
WITH ranked AS (
  SELECT e.first_name,d.dept_name,salary,ROW_NUMBER() OVER(PARTITION BY d.dept_name ORDER BY salary DESC) rn FROM employees e JOIN departments d ON e.dept_id=d.dept_id)
SELECT * FROM ranked WHERE rn=1;
```
