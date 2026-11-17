import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

n = 1000

degrees = ["BA", "BS", "MS", "MSIS", "PHD"]

degree_salary_ranges = {
    "BA":   (80000, 130000),
    "BS":   (90000, 150000),
    "MS":   (120000, 200000),
    "MSIS": (130000, 220000),
    "PHD":  (200000, 280000)  # ✅ FIXED
}

def generate_salary(degree):
    low, high = degree_salary_ranges[degree]
    return random.randrange(low, high + 1, 1000)

data = []

for i in range(1, n + 1):
    degree = random.choice(degrees)
    
    data.append({
        "emp_id": i,
        "emp_name": fake.name(),
        "dept_id": random.choice(["SALES","BUSINESS","AI","MARKETING","SOFTWARE","HARDWARE"]),
        "country": random.choice(["USA","CANADA","GERMANY","CHINA","INDIA"]),
        "gender": random.choice(["MALE","FEMALE"]),
        "degree": degree,
        "salary": generate_salary(degree),
        "performance": random.randint(1,10),
        "hire_date": fake.date_between(start_date="-3y", end_date="today")
    })

df = pd.DataFrame(data)
df.to_csv("employees_1000.csv", index=False)
