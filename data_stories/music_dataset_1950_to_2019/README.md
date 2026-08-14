# 🎵 Music Dataset, 1950–2019

**OMIS-105 · Not yet a data story — raw data only**

⚠️ **This folder has no notebook.** It contains a dataset and reference material, but
nothing to run. It is a *candidate* for a data story rather than a finished one.

---

## What is here

| File | Role |
|---|---|
| `tcc_ceds_music.csv` | **28,372 songs**, 1950–2019 |
| `tcc_ceds_music.csv.zip` | Compressed copy of the same file |
| `metadata.md` | Column documentation |
| `kaggle_notebooks/` | Reference notebooks from Kaggle (not course material) |

---

## What it would take to finish it

The dataset is large and clean enough to be useful. To bring it in line with the other
stories it needs:

1. **A build notebook** — load the CSV, normalise column names, create the database
2. **An analysis notebook** — tiered queries, following the pattern in
   `netflix_titles/` or `video_game_sales/`
3. **A plot helper module** — charts kept out of the notebook
4. **A week assignment** — on the shape of the data, it would suit **Week 4**
   (aggregation by decade, genre and artist)

`netflix_titles/` is the closest template: single wide table, a date column that needs
parsing, and questions that are mostly `GROUP BY`.

---

## Why it fits the course well if completed

- **Songs by decade and genre** is a natural aggregation exercise.
- Like the movie and Netflix datasets, **students can sanity-check the results**
  against music they already know.
- At **28,372 rows** it is too big to scroll through, so answers have to come from
  `GROUP BY`.

---

## Before using it

- `kaggle_notebooks/` holds **third-party** notebooks.
- They were downloaded for reference, **not vetted for teaching**.
- Check their licensing and quality before putting any of it in front of students.
