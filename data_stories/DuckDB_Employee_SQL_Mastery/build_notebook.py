import json

def md_cell(source):
    return {"cell_type": "markdown", "metadata": {}, "source": [source]}

def code_cell(source):
    return {"cell_type": "code", "metadata": {}, "source": [source], "outputs": [], "execution_count": None}

cells = []

# ═══════════════════════════════════════════════════════════════════════════════
# TITLE & SETUP
# ═══════════════════════════════════════════════════════════════════════════════

cells.append(md_cell("""# 🗄️ DuckDB Employee Database — SQL Mastery Notebook
---
**Topics covered:** `GROUP BY`, `JOIN` (Inner, Left, Right), `Ranking Functions`, `Subqueries with WITH (CTEs)`

**Levels:**
- 🟢 **Basic** (Cells 1–10): Simple aggregations and single joins
- 🟡 **Intermediate** (Cells 11–30): Multi-table joins, CTEs, window functions
- 🔴 **Intermediate+** (Cells 31–40): Complex CTEs, correlated subqueries, advanced analytics

---"""))

cells.append(code_cell("""# ── Setup: Import libraries and helper functions ──────────────────────────────
import duckdb
import pandas as pd
import sys, os

# Import our clean display/plot helpers
from notebook_helpers import (
    display_result, plot_bar, plot_hbar, plot_pie,
    plot_line, plot_grouped_bar, plot_heatmap, plot_scatter
)

# Connect to DuckDB (in-memory)
con = duckdb.connect()

print("✅ DuckDB connected. Ready to query!")"""))

cells.append(code_cell("""# ── Load CSV data into DuckDB tables ──────────────────────────────────────────
DATA_DIR = "/Users/max/mp/data_analytics/SQL-Project-Employee-Database/mp_emps_project/data/"

# Create tables and load data
con.execute(\"\"\"
CREATE TABLE department (
    dept_id   VARCHAR NOT NULL PRIMARY KEY,
    dept_name VARCHAR NOT NULL
);

CREATE TABLE titles (
    title_id VARCHAR NOT NULL PRIMARY KEY,
    title    VARCHAR NOT NULL UNIQUE
);

CREATE TABLE employee (
    emp_id       INT     NOT NULL PRIMARY KEY,
    emp_title_id VARCHAR NOT NULL REFERENCES titles(title_id),
    birth_date   DATE    NOT NULL,
    first_name   VARCHAR NOT NULL,
    last_name    VARCHAR NOT NULL,
    gender       VARCHAR NOT NULL,
    hire_date    DATE    NOT NULL
);

CREATE TABLE department_employee (
    emp_id  INT     NOT NULL REFERENCES employee(emp_id),
    dept_id VARCHAR NOT NULL REFERENCES department(dept_id),
    PRIMARY KEY (emp_id, dept_id)
);

CREATE TABLE department_manager (
    dept_id VARCHAR NOT NULL REFERENCES department(dept_id),
    emp_id  INT     NOT NULL REFERENCES employee(emp_id),
    PRIMARY KEY (dept_id, emp_id)
);

CREATE TABLE salaries (
    emp_id INT NOT NULL PRIMARY KEY REFERENCES employee(emp_id),
    salary INT NOT NULL
);
\"\"\")

# Load CSVs
con.execute(f"COPY department   FROM '{DATA_DIR}departments.csv'  (HEADER TRUE);")
con.execute(f"COPY titles       FROM '{DATA_DIR}titles.csv'       (HEADER TRUE);")
con.execute(f"COPY employee     FROM '{DATA_DIR}employees.csv'    (HEADER TRUE, DATEFORMAT '%m/%d/%Y');")
con.execute(f"COPY department_employee FROM '{DATA_DIR}dept_emp.csv' (HEADER TRUE);")
con.execute(f"COPY department_manager  FROM '{DATA_DIR}dept_manager.csv' (HEADER TRUE);")
con.execute(f"COPY salaries     FROM '{DATA_DIR}salaries.csv'     (HEADER TRUE);")

print("✅ All 6 tables loaded successfully!")
print(f"   • employees:  {con.execute('SELECT COUNT(*) FROM employee').fetchone()[0]:,} rows")
print(f"   • salaries:   {con.execute('SELECT COUNT(*) FROM salaries').fetchone()[0]:,} rows")
print(f"   • dept_emp:   {con.execute('SELECT COUNT(*) FROM department_employee').fetchone()[0]:,} rows")
print(f"   • departments:{con.execute('SELECT COUNT(*) FROM department').fetchone()[0]:,} rows")"""))

# ═══════════════════════════════════════════════════════════════════════════════
# 🟢 BASIC (Cells 1–10)
# ═══════════════════════════════════════════════════════════════════════════════

cells.append(md_cell("""---
## 🟢 BASIC — Simple Aggregations & Single Joins (Cells 1–10)
---"""))

# Cell 1
cells.append(md_cell("""### Cell 1: List All Departments
**Concept:** Simple `SELECT` — explore the `department` table."""))
cells.append(code_cell("""sql = \"\"\"
SELECT  dept_id,
        dept_name
FROM    department
ORDER BY dept_id;
\"\"\"

df = con.execute(sql).df()
display_result(df, "All Departments")"""))

# Cell 2
cells.append(md_cell("""### Cell 2: Count Employees per Department
**Concept:** `GROUP BY` with `COUNT` + `INNER JOIN`."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_name,
         COUNT(*) AS employee_count
FROM     department_employee de
         INNER JOIN department d ON de.dept_id = d.dept_id
GROUP BY d.dept_name
ORDER BY employee_count DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Employee Count per Department")
plot_bar(df, "dept_name", "employee_count",
         title="Number of Employees per Department",
         xlabel="Department", ylabel="Count", rotate_x=30)"""))

# Cell 3
cells.append(md_cell("""### Cell 3: Average Salary by Department
**Concept:** `GROUP BY` + `AVG` + `INNER JOIN` across three tables."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_name,
         ROUND(AVG(s.salary), 2) AS avg_salary
FROM     department_employee de
         INNER JOIN department d ON de.dept_id = d.dept_id
         INNER JOIN salaries s   ON de.emp_id  = s.emp_id
GROUP BY d.dept_name
ORDER BY avg_salary DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Average Salary by Department")
plot_hbar(df, "dept_name", "avg_salary",
          title="Average Salary by Department",
          xlabel="Average Salary ($)", ylabel="Department")"""))

# Cell 4
cells.append(md_cell("""### Cell 4: Employee Count by Gender
**Concept:** `GROUP BY` on a single column."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   gender,
         COUNT(*) AS total
FROM     employee
GROUP BY gender
ORDER BY total DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Employee Count by Gender")
plot_pie(df, "gender", "total", title="Employee Distribution by Gender")"""))

# Cell 5
cells.append(md_cell("""### Cell 5: Employee Count by Job Title
**Concept:** `GROUP BY` + `INNER JOIN` with `titles` table."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   t.title,
         COUNT(*) AS emp_count
FROM     employee e
         INNER JOIN titles t ON e.emp_title_id = t.title_id
GROUP BY t.title
ORDER BY emp_count DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Employee Count by Title")
plot_bar(df, "title", "emp_count",
         title="Employees per Job Title",
         xlabel="Title", ylabel="Count", rotate_x=25)"""))

# Cell 6
cells.append(md_cell("""### Cell 6: Highest Salary in Each Department
**Concept:** `GROUP BY` + `MAX` + multi-table `JOIN`."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_name,
         MAX(s.salary) AS max_salary
FROM     department_employee de
         INNER JOIN department d ON de.dept_id = d.dept_id
         INNER JOIN salaries s   ON de.emp_id  = s.emp_id
GROUP BY d.dept_name
ORDER BY max_salary DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Highest Salary per Department")
plot_bar(df, "dept_name", "max_salary",
         title="Maximum Salary by Department",
         xlabel="Department", ylabel="Max Salary ($)", rotate_x=30)"""))

# Cell 7
cells.append(md_cell("""### Cell 7: Employees Hired per Year
**Concept:** `GROUP BY` with `EXTRACT(YEAR ...)` — date functions."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   EXTRACT(YEAR FROM hire_date) AS hire_year,
         COUNT(*) AS hires
FROM     employee
GROUP BY hire_year
ORDER BY hire_year;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Hires per Year")
plot_line(df, "hire_year", "hires",
          title="Employees Hired per Year",
          xlabel="Year", ylabel="Number of Hires")"""))

# Cell 8
cells.append(md_cell("""### Cell 8: Departments with More Than 30,000 Employees
**Concept:** `GROUP BY` + `HAVING` — filtering aggregated results."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_name,
         COUNT(*) AS emp_count
FROM     department_employee de
         INNER JOIN department d ON de.dept_id = d.dept_id
GROUP BY d.dept_name
HAVING   COUNT(*) > 30000
ORDER BY emp_count DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Large Departments (>30K employees)")
plot_bar(df, "dept_name", "emp_count",
         title="Departments with >30,000 Employees",
         xlabel="Department", ylabel="Employee Count", rotate_x=25)"""))

# Cell 9
cells.append(md_cell("""### Cell 9: Average Salary by Gender
**Concept:** `GROUP BY` + `JOIN` — comparing salary across groups."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   e.gender,
         ROUND(AVG(s.salary), 2) AS avg_salary,
         MIN(s.salary) AS min_salary,
         MAX(s.salary) AS max_salary
FROM     employee e
         INNER JOIN salaries s ON e.emp_id = s.emp_id
GROUP BY e.gender;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Salary Statistics by Gender")
plot_grouped_bar(df, "gender", ["avg_salary", "min_salary", "max_salary"],
                 title="Salary Stats by Gender (Avg / Min / Max)",
                 ylabel="Salary ($)")"""))

# Cell 10
cells.append(md_cell("""### Cell 10: Total Salary Budget per Department
**Concept:** `GROUP BY` + `SUM` — aggregate spending."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_name,
         SUM(s.salary) AS total_budget,
         COUNT(*) AS emp_count
FROM     department_employee de
         INNER JOIN department d ON de.dept_id = d.dept_id
         INNER JOIN salaries s   ON de.emp_id  = s.emp_id
GROUP BY d.dept_name
ORDER BY total_budget DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Total Salary Budget per Department")
plot_hbar(df, "dept_name", "total_budget",
          title="Total Salary Budget by Department",
          xlabel="Total Budget ($)", ylabel="Department")"""))

# ═══════════════════════════════════════════════════════════════════════════════
# 🟡 INTERMEDIATE (Cells 11–30)
# ═══════════════════════════════════════════════════════════════════════════════

cells.append(md_cell("""---
## 🟡 INTERMEDIATE — Multi-Table Joins, CTEs, Window Functions (Cells 11–30)
---"""))

# Cell 11
cells.append(md_cell("""### Cell 11: Full Employee Profile (3-Table INNER JOIN)
**Concept:** Joining `employee`, `salaries`, and `titles` together."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   e.emp_id,
         e.first_name || ' ' || e.last_name AS full_name,
         t.title,
         s.salary,
         e.hire_date
FROM     employee e
         INNER JOIN titles t   ON e.emp_title_id = t.title_id
         INNER JOIN salaries s ON e.emp_id = s.emp_id
ORDER BY s.salary DESC
LIMIT 15;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Top 15 Highest-Paid Employees (Full Profile)")"""))

# Cell 12
cells.append(md_cell("""### Cell 12: LEFT JOIN — All Departments with Manager Info
**Concept:** `LEFT JOIN` ensures all departments appear, even those without a manager in our data."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_id,
         d.dept_name,
         e.first_name || ' ' || e.last_name AS manager_name,
         s.salary AS manager_salary
FROM     department d
         LEFT JOIN department_manager dm ON d.dept_id = dm.dept_id
         LEFT JOIN employee e            ON dm.emp_id = e.emp_id
         LEFT JOIN salaries s            ON e.emp_id  = s.emp_id
ORDER BY d.dept_id;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Departments with Their Managers (LEFT JOIN)")"""))

# Cell 13
cells.append(md_cell("""### Cell 13: CTE — Department Statistics
**Concept:** `WITH` (Common Table Expression) for readable multi-step queries."""))
cells.append(code_cell("""sql = \"\"\"
WITH dept_stats AS (
    SELECT   d.dept_name,
             COUNT(*)            AS emp_count,
             ROUND(AVG(s.salary), 2) AS avg_salary,
             MIN(s.salary)       AS min_salary,
             MAX(s.salary)       AS max_salary
    FROM     department_employee de
             INNER JOIN department d ON de.dept_id = d.dept_id
             INNER JOIN salaries s   ON de.emp_id  = s.emp_id
    GROUP BY d.dept_name
)
SELECT   *
FROM     dept_stats
ORDER BY avg_salary DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Department Statistics (via CTE)")
plot_grouped_bar(df, "dept_name", ["min_salary", "avg_salary", "max_salary"],
                 title="Salary Range by Department (Min / Avg / Max)",
                 xlabel="Department", ylabel="Salary ($)")"""))

# Cell 14
cells.append(md_cell("""### Cell 14: RANK — Employees Ranked by Salary Within Department
**Concept:** `RANK() OVER (PARTITION BY ... ORDER BY ...)` window function."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_name,
         e.first_name || ' ' || e.last_name AS full_name,
         s.salary,
         RANK() OVER (PARTITION BY d.dept_name ORDER BY s.salary DESC) AS salary_rank
FROM     department_employee de
         INNER JOIN department d ON de.dept_id = d.dept_id
         INNER JOIN employee e   ON de.emp_id  = e.emp_id
         INNER JOIN salaries s   ON de.emp_id  = s.emp_id
QUALIFY  salary_rank <= 3
ORDER BY d.dept_name, salary_rank;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Top 3 Earners per Department (RANK)")"""))

# Cell 15
cells.append(md_cell("""### Cell 15: DENSE_RANK — Top Salary Tiers per Department
**Concept:** `DENSE_RANK` — no gaps in ranking when ties exist."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_name,
         s.salary,
         DENSE_RANK() OVER (PARTITION BY d.dept_name ORDER BY s.salary DESC) AS dense_rnk
FROM     department_employee de
         INNER JOIN department d ON de.dept_id = d.dept_id
         INNER JOIN salaries s   ON de.emp_id  = s.emp_id
QUALIFY  dense_rnk <= 5
ORDER BY d.dept_name, dense_rnk;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Top 5 Distinct Salary Tiers per Department (DENSE_RANK)")"""))

# Cell 16
cells.append(md_cell("""### Cell 16: CTE — Employees Earning Above Department Average
**Concept:** `WITH` to compute department average, then filter employees above it."""))
cells.append(code_cell("""sql = \"\"\"
WITH dept_avg AS (
    SELECT   de.dept_id,
             d.dept_name,
             ROUND(AVG(s.salary), 2) AS avg_salary
    FROM     department_employee de
             INNER JOIN department d ON de.dept_id = d.dept_id
             INNER JOIN salaries s   ON de.emp_id  = s.emp_id
    GROUP BY de.dept_id, d.dept_name
)
SELECT   da.dept_name,
         e.first_name || ' ' || e.last_name AS full_name,
         s.salary,
         da.avg_salary,
         s.salary - da.avg_salary AS above_avg_by
FROM     department_employee de
         INNER JOIN employee e ON de.emp_id = e.emp_id
         INNER JOIN salaries s ON de.emp_id = s.emp_id
         INNER JOIN dept_avg da ON de.dept_id = da.dept_id
WHERE    s.salary > da.avg_salary
ORDER BY above_avg_by DESC
LIMIT 15;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Employees Earning Above Their Department Average (Top 15)")"""))

# Cell 17
cells.append(md_cell("""### Cell 17: RIGHT JOIN — All Titles with Employee Counts
**Concept:** `RIGHT JOIN` to ensure all titles appear even if no employees have them."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   t.title_id,
         t.title,
         COUNT(e.emp_id) AS emp_count
FROM     employee e
         RIGHT JOIN titles t ON e.emp_title_id = t.title_id
GROUP BY t.title_id, t.title
ORDER BY emp_count DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "All Titles with Employee Count (RIGHT JOIN)")
plot_bar(df, "title", "emp_count",
         title="Employee Count by Title (RIGHT JOIN ensures all titles shown)",
         xlabel="Title", ylabel="Count", rotate_x=25)"""))

# Cell 18
cells.append(md_cell("""### Cell 18: INNER JOIN — Identify Department Managers with Salary
**Concept:** Multi-table `INNER JOIN` to get manager details."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_name,
         e.first_name || ' ' || e.last_name AS manager_name,
         t.title,
         s.salary
FROM     department_manager dm
         INNER JOIN department d ON dm.dept_id = d.dept_id
         INNER JOIN employee e   ON dm.emp_id  = e.emp_id
         INNER JOIN titles t     ON e.emp_title_id = t.title_id
         INNER JOIN salaries s   ON e.emp_id  = s.emp_id
ORDER BY s.salary DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "All Department Managers with Salary")
plot_hbar(df, "manager_name", "salary",
          title="Department Manager Salaries",
          xlabel="Salary ($)", ylabel="Manager")"""))

# Cell 19
cells.append(md_cell("""### Cell 19: PERCENT_RANK — Salary Percentile per Department
**Concept:** `PERCENT_RANK()` — position of each salary as a percentage within the partition."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_name,
         e.first_name || ' ' || e.last_name AS full_name,
         s.salary,
         ROUND(PERCENT_RANK() OVER (
             PARTITION BY d.dept_name ORDER BY s.salary
         ), 4) AS pct_rank
FROM     department_employee de
         INNER JOIN department d ON de.dept_id = d.dept_id
         INNER JOIN employee e   ON de.emp_id  = e.emp_id
         INNER JOIN salaries s   ON de.emp_id  = s.emp_id
WHERE    d.dept_name = 'Development'
ORDER BY pct_rank DESC
LIMIT 15;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Salary Percentile Ranking in Development Dept")"""))

# Cell 20
cells.append(md_cell("""### Cell 20: CTE — Compare Department Headcount vs. Salary Budget
**Concept:** `WITH` for a clean two-metric comparison."""))
cells.append(code_cell("""sql = \"\"\"
WITH dept_metrics AS (
    SELECT   d.dept_name,
             COUNT(DISTINCT de.emp_id) AS headcount,
             SUM(s.salary) AS total_salary,
             ROUND(AVG(s.salary), 0) AS avg_salary
    FROM     department_employee de
             INNER JOIN department d ON de.dept_id = d.dept_id
             INNER JOIN salaries s   ON de.emp_id  = s.emp_id
    GROUP BY d.dept_name
)
SELECT   dept_name,
         headcount,
         total_salary,
         avg_salary,
         ROUND(total_salary * 100.0 / SUM(total_salary) OVER (), 2) AS pct_of_total_budget
FROM     dept_metrics
ORDER BY total_salary DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Department Headcount vs. Salary Budget")
plot_pie(df, "dept_name", "total_salary",
         title="Share of Total Salary Budget by Department")"""))

# Cell 21
cells.append(md_cell("""### Cell 21: ROW_NUMBER — Paginated Employee List
**Concept:** `ROW_NUMBER()` for sequential numbering — useful for pagination."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   ROW_NUMBER() OVER (ORDER BY e.hire_date) AS row_num,
         e.emp_id,
         e.first_name || ' ' || e.last_name AS full_name,
         e.hire_date,
         t.title
FROM     employee e
         INNER JOIN titles t ON e.emp_title_id = t.title_id
ORDER BY e.hire_date
LIMIT 15;
\"\"\"

df = con.execute(sql).df()
display_result(df, "First 15 Employees Hired (ROW_NUMBER for Pagination)")"""))

# Cell 22
cells.append(md_cell("""### Cell 22: NTILE — Divide Employees into Salary Quartiles
**Concept:** `NTILE(4)` — evenly distributes rows into N buckets."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   NTILE(4) OVER (ORDER BY s.salary) AS quartile,
         COUNT(*) AS emp_count,
         MIN(s.salary) AS min_salary,
         MAX(s.salary) AS max_salary,
         ROUND(AVG(s.salary), 0) AS avg_salary
FROM     salaries s
GROUP BY quartile
ORDER BY quartile;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Salary Quartiles (NTILE)")
plot_grouped_bar(df, "quartile", ["min_salary", "avg_salary", "max_salary"],
                 title="Salary Range by Quartile",
                 xlabel="Quartile", ylabel="Salary ($)")"""))

# Cell 23
cells.append(md_cell("""### Cell 23: CTE + HAVING — Departments Above Overall Average Salary
**Concept:** `WITH` to calculate overall avg, then filter departments exceeding it."""))
cells.append(code_cell("""sql = \"\"\"
WITH overall AS (
    SELECT ROUND(AVG(salary), 2) AS company_avg
    FROM   salaries
),
dept_avgs AS (
    SELECT   d.dept_name,
             ROUND(AVG(s.salary), 2) AS dept_avg
    FROM     department_employee de
             INNER JOIN department d ON de.dept_id = d.dept_id
             INNER JOIN salaries s   ON de.emp_id  = s.emp_id
    GROUP BY d.dept_name
)
SELECT   da.dept_name,
         da.dept_avg,
         o.company_avg,
         ROUND(da.dept_avg - o.company_avg, 2) AS diff_from_avg
FROM     dept_avgs da
         CROSS JOIN overall o
WHERE    da.dept_avg > o.company_avg
ORDER BY diff_from_avg DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Departments with Above-Average Salary")
plot_bar(df, "dept_name", "diff_from_avg",
         title="How Much Each Department Exceeds Company Average Salary",
         xlabel="Department", ylabel="$ Above Company Avg", rotate_x=25)"""))

# Cell 24
cells.append(md_cell("""### Cell 24: Cumulative Salary Distribution (Running Total)
**Concept:** `SUM() OVER (ORDER BY ...)` — cumulative window function."""))
cells.append(code_cell("""sql = \"\"\"
WITH salary_bands AS (
    SELECT   CASE
                WHEN salary < 40000 THEN '< 40K'
                WHEN salary < 50000 THEN '40K-50K'
                WHEN salary < 60000 THEN '50K-60K'
                WHEN salary < 70000 THEN '60K-70K'
                WHEN salary < 80000 THEN '70K-80K'
                WHEN salary < 90000 THEN '80K-90K'
                ELSE '90K+'
             END AS band,
             CASE
                WHEN salary < 40000 THEN 1
                WHEN salary < 50000 THEN 2
                WHEN salary < 60000 THEN 3
                WHEN salary < 70000 THEN 4
                WHEN salary < 80000 THEN 5
                WHEN salary < 90000 THEN 6
                ELSE 7
             END AS band_order
    FROM     salaries
)
SELECT   band,
         COUNT(*) AS emp_count,
         SUM(COUNT(*)) OVER (ORDER BY band_order) AS cumulative_count,
         ROUND(SUM(COUNT(*)) OVER (ORDER BY band_order) * 100.0
               / SUM(COUNT(*)) OVER (), 2) AS cumulative_pct
FROM     salary_bands
GROUP BY band, band_order
ORDER BY band_order;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Salary Distribution with Cumulative Totals")
plot_bar(df, "band", "emp_count",
         title="Salary Band Distribution",
         xlabel="Salary Band", ylabel="Employee Count")"""))

# Cell 25
cells.append(md_cell("""### Cell 25: LEFT JOIN — Find Departments Without Managers
**Concept:** `LEFT JOIN` + `WHERE ... IS NULL` pattern to find missing relationships."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_id,
         d.dept_name,
         dm.emp_id AS manager_emp_id
FROM     department d
         LEFT JOIN department_manager dm ON d.dept_id = dm.dept_id
WHERE    dm.emp_id IS NULL
ORDER BY d.dept_id;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Departments Without Any Manager")"""))

# Cell 26
cells.append(md_cell("""### Cell 26: Multi-CTE — Department Stats then Rank Them
**Concept:** Chaining multiple CTEs — first compute stats, then rank."""))
cells.append(code_cell("""sql = \"\"\"
WITH dept_stats AS (
    SELECT   d.dept_name,
             COUNT(*) AS emp_count,
             ROUND(AVG(s.salary), 0) AS avg_salary,
             SUM(s.salary) AS total_budget
    FROM     department_employee de
             INNER JOIN department d ON de.dept_id = d.dept_id
             INNER JOIN salaries s   ON de.emp_id  = s.emp_id
    GROUP BY d.dept_name
),
ranked AS (
    SELECT   *,
             RANK() OVER (ORDER BY avg_salary DESC) AS salary_rank,
             RANK() OVER (ORDER BY emp_count DESC)  AS size_rank
    FROM     dept_stats
)
SELECT   dept_name,
         emp_count,
         avg_salary,
         total_budget,
         salary_rank,
         size_rank
FROM     ranked
ORDER BY salary_rank;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Departments Ranked by Average Salary and Size")"""))

# Cell 27
cells.append(md_cell("""### Cell 27: LAG / LEAD — Compare Salary with Neighbors
**Concept:** `LAG()` and `LEAD()` — access previous/next row's value."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   e.first_name || ' ' || e.last_name AS full_name,
         s.salary,
         LAG(s.salary)  OVER (ORDER BY s.salary DESC) AS higher_salary,
         LEAD(s.salary) OVER (ORDER BY s.salary DESC) AS lower_salary,
         s.salary - LEAD(s.salary) OVER (ORDER BY s.salary DESC) AS gap_to_next
FROM     employee e
         INNER JOIN salaries s ON e.emp_id = s.emp_id
ORDER BY s.salary DESC
LIMIT 15;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Top 15 Salaries with LAG/LEAD Comparison")"""))

# Cell 28
cells.append(md_cell("""### Cell 28: CTE — Hire Cohort Analysis by Year
**Concept:** `WITH` to group employees by hire year and analyze salary patterns."""))
cells.append(code_cell("""sql = \"\"\"
WITH cohorts AS (
    SELECT   EXTRACT(YEAR FROM e.hire_date) AS hire_year,
             COUNT(*)                       AS cohort_size,
             ROUND(AVG(s.salary), 0)        AS avg_salary,
             MIN(s.salary)                  AS min_salary,
             MAX(s.salary)                  AS max_salary
    FROM     employee e
             INNER JOIN salaries s ON e.emp_id = s.emp_id
    GROUP BY hire_year
)
SELECT   *
FROM     cohorts
ORDER BY hire_year;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Hire Cohort Analysis")
plot_line(df, "hire_year", "avg_salary",
          title="Average Salary by Hire Cohort Year",
          xlabel="Hire Year", ylabel="Average Salary ($)")"""))

# Cell 29
cells.append(md_cell("""### Cell 29: 4-Table INNER JOIN — Complete Employee Detail
**Concept:** Joining `employee` + `titles` + `department_employee` + `department` + `salaries`."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   e.emp_id,
         e.first_name || ' ' || e.last_name AS full_name,
         t.title,
         d.dept_name,
         s.salary,
         e.hire_date
FROM     employee e
         INNER JOIN titles t              ON e.emp_title_id = t.title_id
         INNER JOIN department_employee de ON e.emp_id = de.emp_id
         INNER JOIN department d           ON de.dept_id = d.dept_id
         INNER JOIN salaries s             ON e.emp_id = s.emp_id
ORDER BY s.salary DESC
LIMIT 20;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Complete Employee Profile — Top 20 by Salary")"""))

# Cell 30
cells.append(md_cell("""### Cell 30: Rank Departments by Total Salary Budget
**Concept:** `RANK()` applied to aggregated results via CTE."""))
cells.append(code_cell("""sql = \"\"\"
WITH budget AS (
    SELECT   d.dept_name,
             SUM(s.salary) AS total_budget,
             COUNT(*) AS headcount
    FROM     department_employee de
             INNER JOIN department d ON de.dept_id = d.dept_id
             INNER JOIN salaries s   ON de.emp_id  = s.emp_id
    GROUP BY d.dept_name
)
SELECT   dept_name,
         total_budget,
         headcount,
         RANK() OVER (ORDER BY total_budget DESC) AS budget_rank,
         ROUND(total_budget * 1.0 / headcount, 0) AS cost_per_employee
FROM     budget
ORDER BY budget_rank;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Departments Ranked by Total Budget")
plot_bar(df, "dept_name", "cost_per_employee",
         title="Cost per Employee by Department",
         xlabel="Department", ylabel="Avg Cost ($)", rotate_x=30)"""))

# ═══════════════════════════════════════════════════════════════════════════════
# 🔴 INTERMEDIATE+ (Cells 31–40)
# ═══════════════════════════════════════════════════════════════════════════════

cells.append(md_cell("""---
## 🔴 INTERMEDIATE+ — Complex CTEs, Correlated Subqueries, Advanced Analytics (Cells 31–40)
---"""))

# Cell 31
cells.append(md_cell("""### Cell 31: Salary Band Distribution by Department (CASE + CTE + Pivot)
**Concept:** Complex `CASE` expression with `GROUP BY` across departments — creating a pivot view."""))
cells.append(code_cell("""sql = \"\"\"
WITH salary_bands AS (
    SELECT   d.dept_name,
             CASE
                WHEN s.salary < 45000 THEN 'Low (<45K)'
                WHEN s.salary < 65000 THEN 'Mid (45K-65K)'
                ELSE 'High (65K+)'
             END AS band
    FROM     department_employee de
             INNER JOIN department d ON de.dept_id = d.dept_id
             INNER JOIN salaries s   ON de.emp_id  = s.emp_id
)
SELECT   dept_name,
         COUNT(*) FILTER (WHERE band = 'Low (<45K)')    AS low_count,
         COUNT(*) FILTER (WHERE band = 'Mid (45K-65K)') AS mid_count,
         COUNT(*) FILTER (WHERE band = 'High (65K+)')   AS high_count,
         COUNT(*) AS total
FROM     salary_bands
GROUP BY dept_name
ORDER BY dept_name;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Salary Band Distribution by Department")
plot_grouped_bar(df, "dept_name", ["low_count", "mid_count", "high_count"],
                 title="Salary Band Distribution Across Departments",
                 xlabel="Department", ylabel="Employee Count")"""))

# Cell 32
cells.append(md_cell("""### Cell 32: Multi-CTE Chain — Top Earners Then Cross-Department Comparison
**Concept:** Three chained CTEs building on each other for layered analysis."""))
cells.append(code_cell("""sql = \"\"\"
WITH dept_top AS (
    -- Step 1: Find the top earner in each department
    SELECT   d.dept_name,
             e.first_name || ' ' || e.last_name AS top_earner,
             s.salary AS top_salary,
             ROW_NUMBER() OVER (PARTITION BY d.dept_name ORDER BY s.salary DESC) AS rn
    FROM     department_employee de
             INNER JOIN department d ON de.dept_id = d.dept_id
             INNER JOIN employee e   ON de.emp_id  = e.emp_id
             INNER JOIN salaries s   ON de.emp_id  = s.emp_id
),
top_one AS (
    -- Step 2: Keep only rank=1 per department
    SELECT dept_name, top_earner, top_salary
    FROM   dept_top
    WHERE  rn = 1
),
comparison AS (
    -- Step 3: Compare to company-wide max
    SELECT   *,
             MAX(top_salary) OVER () AS company_max,
             ROUND(top_salary * 100.0 / MAX(top_salary) OVER (), 1) AS pct_of_max
    FROM     top_one
)
SELECT   dept_name,
         top_earner,
         top_salary,
         company_max,
         pct_of_max
FROM     comparison
ORDER BY top_salary DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Top Earner per Department vs. Company Max")
plot_hbar(df, "dept_name", "pct_of_max",
          title="Top Earner's Salary as % of Company Maximum",
          xlabel="% of Company Max Salary", ylabel="Department")"""))

# Cell 33
cells.append(md_cell("""### Cell 33: Correlated Subquery — Employees Above Department Median
**Concept:** Subquery referencing the outer query (correlated) to compare each employee to their department median."""))
cells.append(code_cell("""sql = \"\"\"
WITH dept_medians AS (
    SELECT   de.dept_id,
             d.dept_name,
             PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY s.salary) AS median_salary
    FROM     department_employee de
             INNER JOIN department d ON de.dept_id = d.dept_id
             INNER JOIN salaries s   ON de.emp_id  = s.emp_id
    GROUP BY de.dept_id, d.dept_name
)
SELECT   dm.dept_name,
         e.first_name || ' ' || e.last_name AS full_name,
         s.salary,
         ROUND(dm.median_salary, 0) AS dept_median,
         s.salary - ROUND(dm.median_salary, 0) AS above_median_by
FROM     department_employee de
         INNER JOIN employee e      ON de.emp_id = e.emp_id
         INNER JOIN salaries s      ON e.emp_id = s.emp_id
         INNER JOIN dept_medians dm ON de.dept_id = dm.dept_id
WHERE    s.salary > dm.median_salary * 1.5
ORDER BY above_median_by DESC
LIMIT 15;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Employees Earning >150% of Their Department Median")"""))

# Cell 34
cells.append(md_cell("""### Cell 34: Window Functions Combined — Running Stats per Department
**Concept:** Multiple window functions (`AVG`, `COUNT`, `RANK`) with `PARTITION BY` + `ORDER BY`."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_name,
         e.first_name || ' ' || e.last_name AS full_name,
         s.salary,
         ROUND(AVG(s.salary) OVER (PARTITION BY d.dept_name), 0) AS dept_avg,
         COUNT(*) OVER (PARTITION BY d.dept_name) AS dept_size,
         RANK() OVER (PARTITION BY d.dept_name ORDER BY s.salary DESC) AS dept_rank,
         ROUND(s.salary - AVG(s.salary) OVER (PARTITION BY d.dept_name), 0) AS vs_dept_avg
FROM     department_employee de
         INNER JOIN department d ON de.dept_id = d.dept_id
         INNER JOIN employee e   ON de.emp_id  = e.emp_id
         INNER JOIN salaries s   ON de.emp_id  = s.emp_id
WHERE    d.dept_name IN ('Finance', 'Sales', 'Development')
QUALIFY  dept_rank <= 5
ORDER BY d.dept_name, dept_rank;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Top 5 per Department with Running Stats (3 Depts)")"""))

# Cell 35
cells.append(md_cell("""### Cell 35: Hire Year Cohort Retention — Year-Over-Year Comparison
**Concept:** CTE with window function `LAG` to analyze year-over-year hiring trends."""))
cells.append(code_cell("""sql = \"\"\"
WITH yearly_hires AS (
    SELECT   EXTRACT(YEAR FROM hire_date) AS hire_year,
             COUNT(*)                     AS hires,
             COUNT(*) FILTER (WHERE gender = 'M') AS male_hires,
             COUNT(*) FILTER (WHERE gender = 'F') AS female_hires
    FROM     employee
    GROUP BY hire_year
),
with_change AS (
    SELECT   *,
             LAG(hires) OVER (ORDER BY hire_year) AS prev_year_hires,
             hires - LAG(hires) OVER (ORDER BY hire_year) AS yoy_change,
             ROUND((hires - LAG(hires) OVER (ORDER BY hire_year)) * 100.0
                   / NULLIF(LAG(hires) OVER (ORDER BY hire_year), 0), 1) AS yoy_pct_change
    FROM     yearly_hires
)
SELECT   *
FROM     with_change
ORDER BY hire_year;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Year-Over-Year Hiring Analysis")
plot_grouped_bar(df, "hire_year", ["male_hires", "female_hires"],
                 title="Male vs. Female Hires by Year",
                 xlabel="Year", ylabel="Hires")"""))

# Cell 36
cells.append(md_cell("""### Cell 36: Complex JOIN + GROUP BY + HAVING + RANK
**Concept:** Combining aggregation, filtering, and ranking in one query."""))
cells.append(code_cell("""sql = \"\"\"
WITH dept_title_stats AS (
    SELECT   d.dept_name,
             t.title,
             COUNT(*)             AS emp_count,
             ROUND(AVG(s.salary), 0) AS avg_salary
    FROM     department_employee de
             INNER JOIN department d ON de.dept_id = d.dept_id
             INNER JOIN employee e   ON de.emp_id  = e.emp_id
             INNER JOIN titles t     ON e.emp_title_id = t.title_id
             INNER JOIN salaries s   ON e.emp_id  = s.emp_id
    GROUP BY d.dept_name, t.title
    HAVING   COUNT(*) > 1000
)
SELECT   dept_name,
         title,
         emp_count,
         avg_salary,
         RANK() OVER (PARTITION BY dept_name ORDER BY avg_salary DESC) AS title_salary_rank
FROM     dept_title_stats
ORDER BY dept_name, title_salary_rank;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Titles Ranked by Salary Within Each Department (>1000 employees)")"""))

# Cell 37
cells.append(md_cell("""### Cell 37: Pivot-Style — Gender Salary Comparison per Department
**Concept:** `CASE` inside aggregation to pivot data — comparing genders side-by-side."""))
cells.append(code_cell("""sql = \"\"\"
SELECT   d.dept_name,
         ROUND(AVG(CASE WHEN e.gender = 'M' THEN s.salary END), 0) AS avg_male_salary,
         ROUND(AVG(CASE WHEN e.gender = 'F' THEN s.salary END), 0) AS avg_female_salary,
         ROUND(AVG(CASE WHEN e.gender = 'M' THEN s.salary END) -
               AVG(CASE WHEN e.gender = 'F' THEN s.salary END), 0) AS gender_gap,
         COUNT(CASE WHEN e.gender = 'M' THEN 1 END) AS male_count,
         COUNT(CASE WHEN e.gender = 'F' THEN 1 END) AS female_count
FROM     department_employee de
         INNER JOIN department d ON de.dept_id = d.dept_id
         INNER JOIN employee e   ON de.emp_id  = e.emp_id
         INNER JOIN salaries s   ON de.emp_id  = s.emp_id
GROUP BY d.dept_name
ORDER BY gender_gap DESC;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Gender Salary Comparison by Department")
plot_grouped_bar(df, "dept_name", ["avg_male_salary", "avg_female_salary"],
                 title="Average Salary: Male vs. Female by Department",
                 xlabel="Department", ylabel="Average Salary ($)")"""))

# Cell 38
cells.append(md_cell("""### Cell 38: Multi-CTE with Window Functions — Salary Growth by Seniority
**Concept:** Chained CTEs computing seniority buckets, then applying window functions for comparison."""))
cells.append(code_cell("""sql = \"\"\"
WITH seniority AS (
    SELECT   e.emp_id,
             s.salary,
             d.dept_name,
             EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) AS years_employed,
             CASE
                WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) < 30 THEN 'Junior (<30 yrs)'
                WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) < 35 THEN 'Mid (30-35 yrs)'
                ELSE 'Senior (35+ yrs)'
             END AS seniority_band
    FROM     employee e
             INNER JOIN salaries s             ON e.emp_id = s.emp_id
             INNER JOIN department_employee de ON e.emp_id = de.emp_id
             INNER JOIN department d           ON de.dept_id = d.dept_id
),
band_stats AS (
    SELECT   seniority_band,
             dept_name,
             COUNT(*)             AS emp_count,
             ROUND(AVG(salary), 0) AS avg_salary,
             ROUND(STDDEV(salary), 0) AS salary_stddev
    FROM     seniority
    GROUP BY seniority_band, dept_name
)
SELECT   dept_name,
         seniority_band,
         emp_count,
         avg_salary,
         salary_stddev,
         RANK() OVER (PARTITION BY seniority_band ORDER BY avg_salary DESC) AS rank_in_band
FROM     band_stats
WHERE    emp_count > 500
ORDER BY seniority_band, rank_in_band;
\"\"\"

df = con.execute(sql).df()
display_result(df, "Salary by Seniority Band Across Departments")"""))

# Cell 39
cells.append(md_cell("""### Cell 39: Department Comparison Dashboard Query
**Concept:** Single comprehensive CTE combining all key metrics per department."""))
cells.append(code_cell("""sql = \"\"\"
WITH metrics AS (
    SELECT   d.dept_name,
             COUNT(DISTINCT de.emp_id) AS headcount,
             SUM(s.salary)             AS total_budget,
             ROUND(AVG(s.salary), 0)   AS avg_salary,
             ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY s.salary), 0) AS median_salary,
             MAX(s.salary)             AS max_salary,
             MIN(s.salary)             AS min_salary,
             MAX(s.salary) - MIN(s.salary) AS salary_range,
             COUNT(DISTINCT dm.emp_id) AS num_managers
    FROM     department d
             INNER JOIN department_employee de ON d.dept_id = de.dept_id
             INNER JOIN salaries s             ON de.emp_id = s.emp_id
             LEFT JOIN department_manager dm   ON d.dept_id = dm.dept_id
    GROUP BY d.dept_name
)
SELECT   dept_name,
         headcount,
         avg_salary,
         median_salary,
         max_salary,
         salary_range,
         total_budget,
         num_managers,
         RANK() OVER (ORDER BY avg_salary DESC) AS salary_rank,
         RANK() OVER (ORDER BY headcount DESC)  AS size_rank
FROM     metrics
ORDER BY salary_rank;
\"\"\"

df = con.execute(sql).df()
display_result(df, "📊 Department Dashboard — All Key Metrics")
plot_scatter(df, "headcount", "avg_salary",
             title="Department Size vs. Average Salary",
             xlabel="Headcount", ylabel="Average Salary ($)")"""))

# Cell 40
cells.append(md_cell("""### Cell 40: Grand Finale — Combining All Concepts
**Concept:** Multi-CTE + Window Functions + JOINs + CASE + GROUP BY + HAVING — a comprehensive analytical query."""))
cells.append(code_cell("""sql = \"\"\"
WITH employee_full AS (
    -- CTE 1: Build complete employee profile
    SELECT   e.emp_id,
             e.first_name || ' ' || e.last_name AS full_name,
             e.gender,
             e.hire_date,
             t.title,
             d.dept_name,
             s.salary,
             EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) AS tenure_years
    FROM     employee e
             INNER JOIN titles t              ON e.emp_title_id = t.title_id
             INNER JOIN department_employee de ON e.emp_id = de.emp_id
             INNER JOIN department d           ON de.dept_id = d.dept_id
             INNER JOIN salaries s             ON e.emp_id = s.emp_id
),
dept_analysis AS (
    -- CTE 2: Department-level aggregations
    SELECT   dept_name,
             COUNT(*) AS dept_size,
             ROUND(AVG(salary), 0) AS dept_avg_salary,
             ROUND(AVG(tenure_years), 1) AS avg_tenure
    FROM     employee_full
    GROUP BY dept_name
),
ranked_employees AS (
    -- CTE 3: Rank employees with full context
    SELECT   ef.*,
             da.dept_size,
             da.dept_avg_salary,
             da.avg_tenure AS dept_avg_tenure,
             RANK() OVER (PARTITION BY ef.dept_name ORDER BY ef.salary DESC) AS salary_rank_in_dept,
             NTILE(10) OVER (ORDER BY ef.salary) AS salary_decile,
             CASE
                WHEN ef.salary > da.dept_avg_salary * 1.2 THEN 'Above (+20%)'
                WHEN ef.salary < da.dept_avg_salary * 0.8 THEN 'Below (-20%)'
                ELSE 'Average Range'
             END AS salary_category
    FROM     employee_full ef
             INNER JOIN dept_analysis da ON ef.dept_name = da.dept_name
)
SELECT   dept_name,
         salary_category,
         COUNT(*) AS emp_count,
         ROUND(AVG(salary), 0) AS avg_salary,
         ROUND(AVG(tenure_years), 1) AS avg_tenure,
         MIN(salary) AS min_salary,
         MAX(salary) AS max_salary
FROM     ranked_employees
GROUP BY dept_name, salary_category
HAVING   COUNT(*) > 100
ORDER BY dept_name, salary_category;
\"\"\"

df = con.execute(sql).df()
display_result(df, "🏆 Grand Finale: Salary Category Analysis by Department")
plot_grouped_bar(df.head(15), "dept_name", ["min_salary", "avg_salary", "max_salary"],
                 title="Salary Range by Category (First 15 Groups)",
                 xlabel="Department", ylabel="Salary ($)")"""))

# Final cell
cells.append(md_cell("""---
## 🎓 Summary

In this notebook we practiced:

| Concept | Cells |
|---------|-------|
| `GROUP BY` + aggregates (`COUNT`, `AVG`, `SUM`, `MIN`, `MAX`) | 2–10, 13, 20, 23, 24 |
| `INNER JOIN` (2, 3, 4+ tables) | 2, 3, 5, 6, 11, 18, 29 |
| `LEFT JOIN` (preserving all rows) | 12, 25, 39 |
| `RIGHT JOIN` | 17 |
| `WITH` / CTEs (single & chained) | 13, 16, 20, 23, 26, 28, 31–40 |
| `RANK()`, `DENSE_RANK()`, `ROW_NUMBER()` | 14, 15, 21, 26, 30 |
| `NTILE`, `PERCENT_RANK` | 19, 22, 40 |
| `LAG` / `LEAD` | 27, 35 |
| `CASE` (pivot-style) | 24, 31, 37, 38, 40 |
| Cumulative / Running aggregates | 24, 34 |
| `HAVING` | 8, 36, 40 |
| Correlated subqueries / Median | 33 |

---
*Notebook by Professor M. Parsian — Santa Clara University*
"""))

cells.append(code_cell("""# Close the connection
con.close()
print("✅ DuckDB connection closed. Great work!")"""))

# ═══════════════════════════════════════════════════════════════════════════════
# Build the notebook JSON
# ═══════════════════════════════════════════════════════════════════════════════

notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0"
        }
    },
    "cells": cells
}

output_path = "/sessions/great-hopeful-dirac/mnt/outputs/DuckDB_Employee_SQL_Mastery.ipynb"
with open(output_path, "w") as f:
    json.dump(notebook, f, indent=1)

print(f"✅ Notebook created: {output_path}")
print(f"   Total cells: {len(cells)}")
