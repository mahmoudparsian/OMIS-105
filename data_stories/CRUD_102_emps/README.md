# CRUD 101 Employees — DuckDB + Jupyter

This teaching package contains:

- `CRUD_101_Employees_DuckDB.ipynb` — main notebook
- `data/employees.csv` — source CSV data
- `helpers/crud_display.py` — display and plotting helper functions
- `requirements.txt` — Python packages

Recommended folder on your Mac:

```bash
/Users/max/mp/OMIS_105/data_stories/CRUD_101_emps/
```

To use:

```bash
cd /Users/max/mp/OMIS_105/data_stories/CRUD_101_emps/
python -m pip install -r requirements.txt
jupyter notebook CRUD_101_Employees_DuckDB.ipynb
```

The notebook is designed to be rerun from top to bottom. It recreates the DuckDB tables safely.
