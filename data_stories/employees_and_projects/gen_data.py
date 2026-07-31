#!/usr/bin/env python3
"""Generate expanded dataset with 100 employees for data2/ folder."""

import csv, random, os

random.seed(42)

# ── 100 real first/last names with gender ──
PEOPLE = [
    # Original 20 (keep exactly as-is including SSNs, salaries, etc.)
    ("John","B","Smith","M"), ("Franklin","T","Wong","M"),
    ("Alicia","J","Zelaya","F"), ("Jennifer","S","Wallace","F"),
    ("Ramesh","K","Narayan","M"), ("Joyce","A","English","F"),
    ("Ahmad","V","Jabbar","M"), ("James","E","Borg","M"),
    ("Maria","L","Garcia","F"), ("Robert","D","Chen","M"),
    ("Susan","M","Park","F"), ("David","R","Kim","M"),
    ("Lisa","A","Patel","F"), ("Carlos","F","Martinez","M"),
    ("Nora","K","Williams","F"), ("Kevin","J","Brown","M"),
    ("Priya","S","Sharma","F"), ("Tom","W","Jackson","M"),
    ("Elena","R","Petrova","F"), ("Marcus","T","Lee","M"),
    # New 80 employees
    ("Angela","M","Davis","F"), ("Brian","P","Thompson","M"),
    ("Carmen","L","Rodriguez","F"), ("Daniel","K","Murphy","M"),
    ("Emily","A","Taylor","F"), ("Frank","J","Anderson","M"),
    ("Gloria","N","Hernandez","F"), ("Henry","D","Wilson","M"),
    ("Irene","C","Thomas","F"), ("Jason","R","Moore","M"),
    ("Karen","E","Martin","F"), ("Lawrence","G","White","M"),
    ("Monica","S","Harris","F"), ("Nathan","H","Clark","M"),
    ("Olivia","T","Lewis","F"), ("Patrick","B","Robinson","M"),
    ("Quinn","A","Walker","F"), ("Raymond","F","Hall","M"),
    ("Sandra","M","Allen","F"), ("Timothy","L","Young","M"),
    ("Uma","K","Reddy","F"), ("Victor","J","King","M"),
    ("Wendy","R","Wright","F"), ("Xavier","D","Lopez","M"),
    ("Yolanda","C","Hill","F"), ("Zachary","N","Scott","M"),
    ("Amara","P","Okafor","F"), ("Benjamin","E","Green","M"),
    ("Chloe","A","Adams","F"), ("Derek","S","Baker","M"),
    ("Eva","M","Gonzalez","F"), ("George","T","Nelson","M"),
    ("Hannah","L","Carter","F"), ("Isaac","R","Mitchell","M"),
    ("Julia","K","Perez","F"), ("Kyle","D","Roberts","M"),
    ("Lena","C","Turner","F"), ("Michael","J","Phillips","M"),
    ("Nina","B","Campbell","F"), ("Oscar","A","Parker","M"),
    ("Paula","G","Evans","F"), ("Quentin","H","Edwards","M"),
    ("Rosa","F","Collins","F"), ("Samuel","N","Stewart","M"),
    ("Tanya","E","Sanchez","F"), ("Ulysses","S","Morris","M"),
    ("Valerie","M","Rogers","F"), ("William","T","Reed","M"),
    ("Xena","L","Cook","F"), ("Yusuf","R","Morgan","M"),
    ("Zara","K","Bell","F"), ("Adrian","D","Howard","M"),
    ("Bianca","C","Ward","F"), ("Charles","N","Cox","M"),
    ("Diana","P","Diaz","F"), ("Edward","E","Richardson","M"),
    ("Fatima","A","Wood","F"), ("Gregory","S","Watson","M"),
    ("Helen","M","Brooks","F"), ("Ivan","T","Kelly","M"),
    ("Janet","L","Sanders","F"), ("Keith","R","Price","M"),
    ("Laura","K","Bennett","F"), ("Martin","D","Gray","M"),
    ("Natasha","C","Barnes","F"), ("Oliver","J","Ross","M"),
    ("Pamela","B","Henderson","F"), ("Ricardo","A","Coleman","M"),
    ("Sophia","G","Jenkins","F"), ("Thomas","H","Perry","M"),
    ("Ursula","F","Powell","F"), ("Vincent","N","Long","M"),
    ("Whitney","E","Patterson","F"), ("Yuri","S","Hughes","M"),
    ("Amelia","M","Flores","F"), ("Brandon","T","Washington","M"),
    ("Cecilia","L","Butler","F"), ("Douglas","R","Simmons","M"),
    ("Esther","K","Foster","F"), ("Felix","D","Gonzales","M"),
    ("Grace","C","Bryant","F"), ("Hugo","N","Alexander","M"),
    ("Ingrid","P","Russell","F"), ("Jerome","E","Griffin","M"),
]

# Original 20 SSNs and data
ORIG_SSN = [
    123456789, 333445555, 999887777, 987654321, 666884444,
    453453453, 987987987, 888665555, 111223333, 222334444,
    444556666, 555667777, 777889999, 888990000, 111334455,
    222445566, 333556677, 444667788, 555778899, 666889900
]

ORIG_BIRTH = [
    "1965-01-09","1965-12-08","1968-01-19","1941-06-20","1962-09-15",
    "1972-07-31","1969-03-29","1937-11-10","1975-06-15","1980-03-22",
    "1971-11-30","1983-08-14","1978-04-02","1985-12-20","1979-08-25",
    "1988-02-17","1990-11-03","1982-05-19","1986-09-07","1974-01-28"
]

ORIG_ADDR = [
    "731 Fondren, Houston TX","638 Voss, Houston TX",
    "3321 Castle, Spring TX","291 Berry, Bellaire TX",
    "975 Fire Oak, Humble TX","5631 Rice, Houston TX",
    "980 Dallas, Houston TX","450 Stone, Houston TX",
    "1200 Main, Sugar Land TX","450 Westheimer, Houston TX",
    "789 Kirby, Houston TX","321 Montrose, Houston TX",
    "567 Richmond, Houston TX","234 Shepherd, Houston TX",
    "890 Bissonnet, Houston TX","145 Gessner, Houston TX",
    "678 Hillcroft, Houston TX","432 Bellaire Blvd, Houston TX",
    "567 Westpark, Houston TX","321 Wilcrest, Houston TX"
]

ORIG_SAL = [
    30000,40000,25000,43000,38000,25000,25000,55000,
    35000,42000,37000,29000,46000,32000,41000,28000,
    34000,31000,39000,48000
]

ORIG_SUPER = [
    333445555,888665555,987654321,888665555,333445555,
    333445555,987654321,None,333445555,987654321,
    333445555,987654321,888665555,333445555,222334444,
    777889999,222334444,777889999,333445555,888665555
]

ORIG_DNO = [5,5,4,4,5,5,4,1,5,4,5,4,1,5,6,7,6,7,5,1]

# Departments: 1=HQ, 4=Admin, 5=Research, 6=Engineering, 7=Marketing
DEPT_IDS = [1, 4, 5, 6, 7]
# Supervisors per dept (manager SSN)
DEPT_MGR = {1: 888665555, 4: 987654321, 5: 333445555, 6: 222334444, 7: 777889999}

STREETS = [
    "Oak","Maple","Cedar","Pine","Elm","Birch","Walnut","Cherry",
    "Willow","Ash","Magnolia","Cypress","Pecan","Laurel","Spruce",
    "Hickory","Poplar","Sycamore","Juniper","Redwood","Dogwood",
    "Chestnut","Hawthorn","Holly","Beech","Alder","Hemlock","Linden"
]
CITIES = ["Houston TX","Bellaire TX","Sugar Land TX","Spring TX",
          "Humble TX","Stafford TX","Katy TX","Pearland TX"]

# Generate new SSNs for employees 21-100
new_ssns = []
ssn_base = 100000001
for i in range(80):
    new_ssns.append(ssn_base + i * 11111)

# Build employee rows
employees = []
for i in range(100):
    fn, mi, ln, g = PEOPLE[i]
    if i < 20:
        ssn = ORIG_SSN[i]
        bd = ORIG_BIRTH[i]
        addr = ORIG_ADDR[i]
        sal = ORIG_SAL[i]
        sup = ORIG_SUPER[i]
        dno = ORIG_DNO[i]
    else:
        ssn = new_ssns[i - 20]
        yr = random.randint(1958, 1998)
        mo = random.randint(1, 12)
        dy = random.randint(1, 28)
        bd = f"{yr}-{mo:02d}-{dy:02d}"
        num = random.randint(100, 9999)
        street = random.choice(STREETS)
        city = random.choice(CITIES)
        addr = f"{num} {street}, {city}"
        sal = random.randint(24, 58) * 1000
        dno = random.choice(DEPT_IDS)
        sup = DEPT_MGR[dno]
    img = f"https://api.dicebear.com/7.x/personas/svg?seed={fn}{ln}"
    employees.append([fn, mi, ln, ssn, bd, addr, g, sal,
                      sup if sup else "", dno, img])

# Write employee.csv
with open("data2/employee.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["first_name","middle_init","last_name","ssn","birth_date",
                "address","gender","salary","super_ssn","dno","image_url"])
    for row in employees:
        w.writerow(row)

# ── works_on.csv ──
# Original 40 records + new records for employees 21-100
PROJECT_IDS = [1,2,3,10,20,30,40,50,60,70,80,90]

orig_wo = [
    (123456789,1,32.5),(123456789,2,7.5),(666884444,3,40.0),
    (453453453,1,20.0),(453453453,2,20.0),(333445555,2,10.0),
    (333445555,3,10.0),(333445555,10,10.0),(333445555,20,10.0),
    (999887777,30,30.0),(999887777,10,10.0),(987987987,10,35.0),
    (987987987,30,5.0),(987654321,30,20.0),(987654321,20,15.0),
    (888665555,20,16.0),(111223333,1,15.0),(111223333,60,25.0),
    (222334444,40,30.0),(222334444,50,10.0),(444556666,2,20.0),
    (444556666,60,20.0),(555667777,10,25.0),(555667777,40,15.0),
    (777889999,70,35.0),(777889999,20,5.0),(888990000,3,20.0),
    (888990000,50,20.0),(111334455,40,25.0),(111334455,90,15.0),
    (222445566,70,20.0),(222445566,80,20.0),(333556677,50,15.0),
    (333556677,90,25.0),(444667788,70,10.0),(444667788,80,30.0),
    (555778899,1,10.0),(555778899,60,30.0),(666889900,20,10.0),
    (666889900,90,5.0),
]

wo_records = list(orig_wo)
for i in range(20, 100):
    ssn = employees[i][3]
    num_proj = random.randint(1, 4)
    projs = random.sample(PROJECT_IDS, num_proj)
    for pid in projs:
        hrs = round(random.uniform(10.0, 40.0), 1)
        wo_records.append((ssn, pid, hrs))

with open("data2/works_on.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ssn","project_id","hours"])
    for row in wo_records:
        w.writerow(row)

# ── dependent.csv ──
ORIG_DEP = [
    (333445555,"Alice","F","1986-04-04","Daughter"),
    (333445555,"Theodore","M","1983-10-25","Son"),
    (333445555,"Joy","F","1958-05-03","Spouse"),
    (987654321,"Abner","M","1942-02-28","Spouse"),
    (123456789,"Michael","M","1988-01-04","Son"),
    (123456789,"Alice","F","1988-12-30","Daughter"),
    (123456789,"Elizabeth","F","1967-05-05","Spouse"),
    (111223333,"Sofia","F","2005-07-12","Daughter"),
    (111223333,"Pedro","M","1974-01-20","Spouse"),
    (222334444,"Emily","F","2010-03-18","Daughter"),
    (444556666,"James","M","2008-11-05","Son"),
    (777889999,"Raj","M","1975-09-30","Spouse"),
    (111334455,"Oliver","M","2012-06-15","Son"),
    (555778899,"Anna","F","2015-03-22","Daughter"),
    (555778899,"Dmitri","M","1984-07-10","Spouse"),
    (666889900,"Jasmine","F","2000-09-18","Daughter"),
]

SPOUSE_NAMES_F = ["Sarah","Linda","Patricia","Barbara","Margaret","Nancy",
                  "Betty","Dorothy","Helen","Sandra","Donna","Carol",
                  "Ruth","Sharon","Michelle","Laura","Kimberly","Deborah",
                  "Jessica","Stephanie","Rebecca","Cynthia","Katherine",
                  "Christine","Janet","Catherine","Diane","Tammy","Pamela"]
SPOUSE_NAMES_M = ["Robert","William","Richard","Joseph","Thomas","Charles",
                  "Christopher","Daniel","Matthew","Anthony","Mark","Donald",
                  "Steven","Paul","Andrew","Joshua","Kenneth","George",
                  "Edward","Brian","Ronald","Timothy","Jason","Jeffrey",
                  "Ryan","Gary","Nicholas","Eric","Stephen","Larry"]
CHILD_NAMES_F = ["Emma","Sophia","Isabella","Mia","Charlotte","Amelia",
                 "Harper","Evelyn","Abigail","Ella","Avery","Scarlett",
                 "Grace","Victoria","Riley","Aria","Lily","Zoey","Chloe"]
CHILD_NAMES_M = ["Liam","Noah","Oliver","Elijah","Lucas","Mason",
                 "Logan","Alexander","Ethan","Jacob","Aiden","Jack",
                 "Owen","Sebastian","Caleb","Ryan","Nathan","Leo","Max"]

dep_records = list(ORIG_DEP)
used_names = {}  # per ssn to avoid dup names

for i in range(20, 100):
    ssn = employees[i][3]
    gender = employees[i][6]
    if random.random() < 0.45:  # ~45% have dependents
        used = set()
        # Spouse
        if random.random() < 0.7:
            if gender == "M":
                sname = random.choice(SPOUSE_NAMES_F)
                sg = "F"
            else:
                sname = random.choice(SPOUSE_NAMES_M)
                sg = "M"
            yr = random.randint(1960, 1996)
            bd = f"{yr}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            dep_records.append((ssn, sname, sg, bd, "Spouse"))
            used.add(sname)
        # Children (0-3)
        num_kids = random.randint(0, 3)
        for _ in range(num_kids):
            if random.random() < 0.5:
                cname = random.choice(CHILD_NAMES_F)
                cg = "F"
            else:
                cname = random.choice(CHILD_NAMES_M)
                cg = "M"
            if cname in used:
                continue
            used.add(cname)
            yr = random.randint(2000, 2020)
            bd = f"{yr}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            rel = "Daughter" if cg == "F" else "Son"
            dep_records.append((ssn, cname, cg, bd, rel))

with open("data2/dependent.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ssn","dependent_name","gender","birth_date","relationship"])
    for row in dep_records:
        w.writerow(row)

# ── Copy unchanged tables ──
import shutil
for fname in ["department.csv", "dept_locations.csv", "project.csv"]:
    shutil.copy2(f"data/{fname}", f"data2/{fname}")

# Print summary
print(f"employee.csv     : {len(employees)} rows")
print(f"works_on.csv     : {len(wo_records)} rows")
print(f"dependent.csv    : {len(dep_records)} rows")
print(f"department.csv   : copied (5 depts)")
print(f"project.csv      : copied (12 projects)")
print(f"dept_locations.csv: copied (10 locations)")
