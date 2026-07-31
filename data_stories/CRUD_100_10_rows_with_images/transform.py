#!/usr/bin/env python3
"""
Transform CRUD notebook: add image_url (avatar) column to schema,
CSV, and every notebook cell.
"""
import json, os, re, shutil

SRC = "../CRUD_100_10_rows"
DST = "."

# ── Avatar URLs for each employee ──────────────────────────────────
AVATARS = {
    "Alex":    "https://ui-avatars.com/api/?name=Alex&size=40&background=4C72B0&color=fff&bold=true",
    "Jeff":    "https://ui-avatars.com/api/?name=Jeff&size=40&background=55A868&color=fff&bold=true",
    "Rafa":    "https://ui-avatars.com/api/?name=Rafa&size=40&background=C44E52&color=fff&bold=true",
    "Susan":   "https://ui-avatars.com/api/?name=Susan&size=40&background=8172B2&color=fff&bold=true",
    "Jen":     "https://ui-avatars.com/api/?name=Jen&size=40&background=E58606&color=fff&bold=true",
    "Barb":    "https://ui-avatars.com/api/?name=Barb&size=40&background=937860&color=fff&bold=true",
    "Dara":    "https://ui-avatars.com/api/?name=Dara&size=40&background=DA8BC3&color=fff&bold=true",
    "Venus":   "https://ui-avatars.com/api/?name=Venus&size=40&background=CCB974&color=fff&bold=true",
    "Margie":  "https://ui-avatars.com/api/?name=Margie&size=40&background=64B5CD&color=fff&bold=true",
    "Betty":   "https://ui-avatars.com/api/?name=Betty&size=40&background=4878CF&color=fff&bold=true",
    # Extra employees created during CRUD C operations
    "Carlos":  "https://ui-avatars.com/api/?name=Carlos&size=40&background=2ecc71&color=fff&bold=true",
    "Diana":   "https://ui-avatars.com/api/?name=Diana&size=40&background=e74c3c&color=fff&bold=true",
    "Ethan":   "https://ui-avatars.com/api/?name=Ethan&size=40&background=3498db&color=fff&bold=true",
    "Fiona":   "https://ui-avatars.com/api/?name=Fiona&size=40&background=9b59b6&color=fff&bold=true",
    "George":  "https://ui-avatars.com/api/?name=George&size=40&background=1abc9c&color=fff&bold=true",
}

BASE_URL = "https://ui-avatars.com/api/?name={name}&size=40&background=random&bold=true"

def avatar_url(name):
    return AVATARS.get(name, BASE_URL.format(name=name))

# ── 1. Create CSV ──────────────────────────────────────────────────
os.makedirs(os.path.join(DST, "data"), exist_ok=True)

csv_lines = [
    "emp_id,emp_name,department,salary,gender,image_url",
    f"100,Alex,SALES,120000,MALE,{avatar_url('Alex')}",
    f"200,Jeff,SALES,140000,MALE,{avatar_url('Jeff')}",
    f"300,Rafa,BUSINESS,150000,MALE,{avatar_url('Rafa')}",
    f"400,Susan,SALES,150000,FMALE,{avatar_url('Susan')}",
    f"500,Jen,BUSINESS,160000,FEMALE,{avatar_url('Jen')}",
    f"600,Barb,BUSINESS,180000,FEMALE,{avatar_url('Barb')}",
    f"700,Dara,AI,190000,MALE,{avatar_url('Dara')}",
    f"800,Venus,AI,200000,FEMALE,{avatar_url('Venus')}",
    f"900,Margie,SALES,140000,FEMALE,{avatar_url('Margie')}",
    f"910,Betty,SALES,170000,FEMALE,{avatar_url('Betty')}",
]
with open(os.path.join(DST, "data", "employees.csv"), "w") as f:
    f.write("\n".join(csv_lines) + "\n")
print("✅ CSV created with image_url column")

# ── 2. Transform notebook ─────────────────────────────────────────
with open(os.path.join(SRC, "CRUD_Employees_DuckDB.ipynb")) as f:
    nb = json.load(f)

def transform_source(src_text):
    """Apply all transformations to a cell's source text."""
    s = src_text

    # ── A. Schema: add image_url column after gender ──
    # Pattern: "gender     VARCHAR\n)"
    s = re.sub(
        r"(gender\s+VARCHAR)\s*\n(\s*\))",
        r"\1,\n    image_url  VARCHAR\n\2",
        s
    )
    # Short form: "gender VARCHAR\n)"
    s = re.sub(
        r"(gender VARCHAR)\s*\n(\s*\))",
        r"\1,\n    image_url  VARCHAR\n\2",
        s
    )

    # ── B. INSERT column lists: add image_url ──
    s = s.replace(
        "(emp_id, emp_name, department, salary, gender)",
        "(emp_id, emp_name, department, salary, gender, image_url)"
    )

    # ── C. INSERT VALUES for the original 10 employees ──
    # Each row: (id, 'Name', 'DEPT', salary, 'GENDER')
    # → (id, 'Name', 'DEPT', salary, 'GENDER', 'url')
    insert_pattern = re.compile(
        r"\((\d+),\s*'(\w+)',\s*'(\w+)',\s*(\d+),\s*'(\w+)'\)"
    )
    def replace_insert(m):
        eid, name, dept, sal, gen = m.groups()
        url = avatar_url(name)
        return f"({eid}, '{name}', '{dept}', {sal}, '{gen}', '{url}')"

    s = insert_pattern.sub(replace_insert, s)

    # ── D. INSERT-SELECT for Fiona (C-3): add image_url ──
    if "950" in s and "'Fiona'" in s and "salary + 5000" in s:
        s = s.replace(
            "    'FEMALE'      AS gender",
            "    'FEMALE'      AS gender,\n    'https://ui-avatars.com/api/?name=Fiona&size=40&background=9b59b6&color=fff&bold=true' AS image_url"
        )

    # ── E. INSERT NULL for George (C-4): add image_url ──
    if "960" in s and "'George'" in s:
        s = s.replace(
            "VALUES (960, 'George', 'SALES', NULL, 'MALE')",
            f"VALUES (960, 'George', 'SALES', NULL, 'MALE', '{avatar_url('George')}')"
        )

    return s


for cell in nb['cells']:
    src = "".join(cell['source'])
    new_src = transform_source(src)

    if new_src != src:
        # Split back into lines preserving the original line structure
        lines = new_src.split("\n")
        cell['source'] = [l + "\n" for l in lines[:-1]] + [lines[-1]]

    # Also update markdown cells that mention the schema
    if cell['cell_type'] == 'markdown':
        md = "".join(cell['source'])
        if "(emp_id, emp_name, department, salary, gender)" in md:
            md = md.replace(
                "(emp_id, emp_name, department, salary, gender)",
                "(emp_id, emp_name, department, salary, gender, image_url)"
            )
        # Update schema table in markdown
        if "| Column | Type | Description |" in md:
            md = md.replace(
                "| gender | VARCHAR |",
                "| gender | VARCHAR |"
            )
            # Add image_url row to schema table if not present
            if "image_url" not in md:
                md = md.replace(
                    "| gender     | VARCHAR",
                    "| gender     | VARCHAR"
                )
                # Find the last table row and add after it
                if "| gender" in md and "image_url" not in md:
                    md = re.sub(
                        r"(\| gender\s+\| VARCHAR\s+\|[^\n]*\n)",
                        r"\1| image_url  | VARCHAR | Avatar image URL |\n",
                        md
                    )
        if md != "".join(cell['source']):
            lines = md.split("\n")
            cell['source'] = [l + "\n" for l in lines[:-1]] + [lines[-1]]

# Write transformed notebook
with open(os.path.join(DST, "CRUD_Employees_DuckDB.ipynb"), "w") as f:
    json.dump(nb, f, indent=1)
print("✅ Notebook transformed with image_url column in all cells")

# ── 3. Copy and update crud_helpers.py ─────────────────────────────
with open(os.path.join(SRC, "crud_helpers.py")) as f:
    helpers = f.read()

# Add image rendering to show_table
old_show = '''def show_table(df: pd.DataFrame, title: str = "Result Set",
               max_rows: int = 50) -> None:
    if df is None or df.empty:
        display(HTML(f"<p><i>No rows returned for: <b>{title}</b></i></p>"))
        return
    df_show = df.head(max_rows).copy()
    df_show.insert(0, "#", range(1, len(df_show) + 1))'''

new_show = '''def show_table(df: pd.DataFrame, title: str = "Result Set",
               max_rows: int = 50) -> None:
    if df is None or df.empty:
        display(HTML(f"<p><i>No rows returned for: <b>{title}</b></i></p>"))
        return
    df_show = df.head(max_rows).copy()
    # Render image_url as <img> tag if the column exists
    if 'image_url' in df_show.columns:
        df_show['image_url'] = df_show['image_url'].apply(
            lambda u: f'<img src="{u}" width="32" height="32" '
                      f'style="border-radius:50%">'
            if pd.notna(u) and u else ''
        )
    df_show.insert(0, "#", range(1, len(df_show) + 1))'''

helpers = helpers.replace(old_show, new_show)

# Update the styled display to render HTML in image_url column
old_display = "    display(styled)"
new_display = '''    # If image_url column has <img> tags, render as HTML
    if 'image_url' in df_show.columns:
        html_str = styled.to_html()
        # Unescape the <img> tags so they render properly
        html_str = html_str.replace('&lt;img ', '<img ')
        html_str = html_str.replace('&gt;', '>')
        html_str = html_str.replace('&quot;', '"')
        html_str = html_str.replace('&#x27;', "'")
        display(HTML(html_str))
    else:
        display(styled)'''

helpers = helpers.replace(old_display, new_display)

with open(os.path.join(DST, "crud_helpers.py"), "w") as f:
    f.write(helpers)
print("✅ crud_helpers.py updated with image rendering support")

# ── 4. Update README ──────────────────────────────────────────────
with open(os.path.join(SRC, "README.md")) as f:
    readme = f.read()

readme = readme.replace(
    "(emp_id, emp_name, department, salary, gender)",
    "(emp_id, emp_name, department, salary, gender, image_url)"
)

# Update each employee line to include avatar URL
for name, url in AVATARS.items():
    # Match lines like: (100, 'Alex', 'SALES', 120000, 'MALE')
    pattern = rf"\((\d+), '{name}', '(\w+)', (\d+), '(\w+)'\)"
    replacement = rf"(\1, '{name}', '\2', \3, '\4', '{url}')"
    readme = re.sub(pattern, replacement, readme)

readme = readme.replace("CRUD_100_10_rows", "CRUD_100_10_rows_with_images")

with open(os.path.join(DST, "README.md"), "w") as f:
    f.write(readme)
print("✅ README.md updated")

print("\n✅ ALL FILES CREATED in CRUD_100_10_rows_with_images/")
