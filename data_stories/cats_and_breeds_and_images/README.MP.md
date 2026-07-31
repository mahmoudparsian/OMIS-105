I want to poke a fun to this project: we have 80 cats, what if we add a cat image to every record of cat? your opinion/input?

Fun idea! Here are a few approaches to think about:

**Option A: URL-based cat avatars (easiest, no storage needed)**
Add an `image_url` column to `cats.csv` using a service like `robohash.org` with `set=4` (which generates unique kitten avatars deterministically from any text). For example, `https://robohash.org/Luna?set=4` always produces the same cute cat avatar for "Luna." No API key, no storage, works in HTML table displays inside the notebook.

**Option B: Breed-specific photos via The Cat API**
Use `thecatapi.com` to get real breed-specific cat photos. More realistic, but depends on an external API and would need a (free) API key. Images could vanish if the service changes.

**Option C: Local AI-generated images**
Generate 80 small images (one per cat) using an image generation service and store them in an `images/` folder. Most self-contained but heaviest in file size.

**My recommendation: Option A.** It's lightweight, deterministic (same URL always gives the same image), works offline in the notebook via HTML rendering, and it's genuinely fun — each cat gets its own unique cartoon avatar based on its name. We'd add one column to the CSV and one new query in the notebook that renders a "cat gallery" with images in an HTML table.

Want me to go ahead with Option A? Or would you prefer real cat photos (Option B), or a different approach altogether?

let's go with your recommendation: Option A. But do not override the created files, you can create everything under a new folder: /Users/max/mp/OMIS_105/data_stories/cats_and_breeds_and_images/    So this is kind of a new project

Now the cats CSV with the new `image_url` column:Now let me create the display utilities with image support:Now let me build the new notebook with image-enhanced queries:Let me verify the complete project structure:Everything is in place. Let me also write a quick README for this new project:Done! Here's the new project at [cats_and_breeds_and_images](computer:///Users/max/mp/OMIS_105/data_stories/cats_and_breeds_and_images):

**What's new compared to the original project:**

- **`image_url` column** in `cats.csv` — each cat gets a unique kitten avatar from `robohash.org/CatName_catID?set=4&size=150x150`
- **`show_gallery()`** function in `display_utils.py` — renders cats as visual card grids with circular avatar images, names, and details
- **`show_table_with_images()`** — renders standard tables but with inline circular thumbnail images
- **3 gallery-specific queries** (Q1: full gallery, Q3: breed-filtered gallery, Q34: premium collection with trick counts)
- **Image-enhanced result tables** throughout (Q2, Q9, Q10, Q13, Q15, Q17, Q19, Q21, Q24) — wherever it makes visual sense, results include cat avatars

To run it: `pip install duckdb pandas matplotlib` then open the notebook. You'll need internet for the avatars to load (they come from robohash.org in real time).
