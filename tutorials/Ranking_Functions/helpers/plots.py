
import matplotlib.pyplot as plt
import pandas as pd


def plot_salary_by_degree(con):
    df = con.execute("""
        WITH degree_stats AS (
            SELECT degree, ROUND(AVG(salary), 0) AS avg_salary
            FROM employees
            GROUP BY degree
        )
        SELECT * FROM degree_stats
        ORDER BY avg_salary DESC;
    """).df()
    plt.figure(figsize=(8, 4.5))
    plt.bar(df['degree'], df['avg_salary'])
    plt.title('Average Salary by Degree')
    plt.xlabel('Degree')
    plt.ylabel('Average Salary')
    plt.tight_layout()
    plt.show()


def plot_top_departments(con):
    df = con.execute("""
        WITH dept_stats AS (
            SELECT dept_id, ROUND(AVG(salary), 0) AS avg_salary
            FROM employees
            GROUP BY dept_id
        )
        SELECT * FROM dept_stats
        ORDER BY avg_salary DESC;
    """).df()
    plt.figure(figsize=(9, 4.5))
    plt.bar(df['dept_id'], df['avg_salary'])
    plt.title('Average Salary by Department')
    plt.xlabel('Department')
    plt.ylabel('Average Salary')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.show()


def plot_rank_curve(con):
    df = con.execute("""
        WITH ranked AS (
            SELECT salary,
                   ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num
            FROM employees
        )
        SELECT row_num, salary
        FROM ranked
        WHERE row_num <= 100
        ORDER BY row_num;
    """).df()
    plt.figure(figsize=(8.5, 4.5))
    plt.plot(df['row_num'], df['salary'], marker='o', linewidth=1)
    plt.title('Salary Curve for Top 100 Employees')
    plt.xlabel('ROW_NUMBER by Salary Descending')
    plt.ylabel('Salary')
    plt.tight_layout()
    plt.show()


def plot_top_n_per_dept(con, n=3):
    df = con.execute(f"""
        WITH ranked AS (
            SELECT dept_id, emp_name, salary,
                   ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
            FROM employees
        )
        SELECT dept_id, rn, salary
        FROM ranked
        WHERE rn <= {int(n)}
        ORDER BY dept_id, rn;
    """).df()
    labels = df['dept_id'] + ' #' + df['rn'].astype(str)
    plt.figure(figsize=(10, 4.8))
    plt.bar(labels, df['salary'])
    plt.title(f'Top {n} Salaries per Department')
    plt.xlabel('Department Rank')
    plt.ylabel('Salary')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
