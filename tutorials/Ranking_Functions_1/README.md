# DuckDB Ranking Functions Flagship Tutorial

Files:

- `duckdb_ranking_functions_flagship.ipynb` — full 20-cell teaching notebook
- `data/employees_1000.csv` — 1,000-row employee dataset
- `helpers/rendering.py` — styled `show()` helper for high-quality rendered tables
- `helpers/plots.py` — plotting helpers so plotting code stays out of the notebook

## Requirements

Install packages:

```bash
pip install duckdb pandas matplotlib faker nbformat
```

Then open the notebook:

```bash
jupyter notebook duckdb_ranking_functions_flagship.ipynb
```

## Dataset design

Department counts:

- SALES: 100
- BUSINESS: 50
- AI: 150
- MARKETING: 50
- SOFTWARE: 400
- HARDWARE: 250

Country counts:

- USA: 600
- CANADA: 200
- GERMANY: 100
- CHINA: 50
- INDIA: 50

PhD salaries range from 200,000 to 280,000.
