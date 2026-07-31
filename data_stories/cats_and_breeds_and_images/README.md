# Cats, Breeds & Tricks — with Cat Avatar Images

**Course:** OMIS 105 — Data Analytics with SQL

## Overview

A complete DuckDB-based Jupyter Notebook exploring a Cat Show database
with 80 cats, 15 breeds, 15 tricks, and unique avatar images for every cat.

## How to Run

```bash
pip install duckdb pandas matplotlib
jupyter notebook cats_and_breeds_duckdb.ipynb
```

## Project Structure

```
cats_and_breeds_and_images/
├── cats_and_breeds_duckdb.ipynb   # Main notebook (34 queries, 6 sections)
├── display_utils.py               # Table display + image gallery functions
├── plot_utils.py                  # All plotting functions
├── data/
│   ├── breeds.csv                 # 15 breeds
│   ├── cats.csv                   # 80 cats (includes image_url column)
│   ├── tricks.csv                 # 15 tricks
│   └── cat_tricks.csv             # 374 cat-trick relationships
└── README.md
```

## Image Feature

Each cat has a unique avatar via RoboHash (set=4, kitten avatars).
URLs are deterministic — same name always gives the same image.
The notebook displays cats in visual card galleries and tables with
inline thumbnail images.

## Requirements

- Python 3.8+
- duckdb
- pandas
- matplotlib
- Internet connection (for loading cat avatar images from robohash.org)
