"""Regenerate docs/screenshots/*.png from a running Streamlit app.

    ./run_app.sh                                          # in one terminal
    uv run --with playwright python docs/screenshots/_capture.py

Optional first argument is the output directory (default: this script's own
directory). Second is the base URL (default: http://localhost:8501).

Two traps this script exists to avoid:

1. `chrome --headless --screenshot` captures the loading skeleton. Streamlit
   holds a websocket open, so --virtual-time-budget never advances and the shot
   fires before any content arrives. Hence Playwright, waiting on real text.

2. `full_page=True` DOES NOT WORK on Streamlit. The page body does not scroll --
   `document.body.scrollHeight` is 0 -- because the content lives inside
   `[data-testid="stMain"]`, which is its own scroll container. Playwright has
   nothing to expand, so it captures exactly one viewport and silently truncates
   every long page. The fix is to measure that container and grow the viewport
   to fit before shooting. Re-measure after the resize: reflow changes the
   height, and on a wide page a chart can get taller as it gets wider.
"""

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

PAGES = ["Dashboard", "Sailor registration", "Boat registration",
         "Reservation system", "View a day", "View a date range",
         "Boat availability", "Constraint playground", "Ask in English",
         "SQL console"]

WIDTH = 1600
MIN_HEIGHT = 900
MAX_HEIGHT = 6000      # a safety stop; nothing here is legitimately taller
SETTLE_MS = 3000       # let charts draw before measuring

out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
base_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8501"
out_dir.mkdir(parents=True, exist_ok=True)


def content_height(pg) -> int:
    """Tallest of the two scroll containers, in CSS pixels."""
    return pg.evaluate("""() => {
        const h = sel => {
            const e = document.querySelector(sel);
            return e ? Math.max(e.scrollHeight, e.clientHeight) : 0;
        };
        return Math.ceil(Math.max(h('[data-testid="stMain"]'),
                                  h('[data-testid="stSidebar"]')));
    }""")


def fit_viewport(pg) -> int:
    """Grow the viewport until the content stops growing with it."""
    height = MIN_HEIGHT
    for _ in range(4):
        wanted = min(max(content_height(pg) + 40, MIN_HEIGHT), MAX_HEIGHT)
        if abs(wanted - height) <= 8:
            break
        height = wanted
        pg.set_viewport_size({"width": WIDTH, "height": height})
        pg.wait_for_timeout(900)      # reflow, then re-measure
    return height


errors = []
with sync_playwright() as p:
    # channel="chrome" borrows the installed browser instead of downloading one.
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": WIDTH, "height": MIN_HEIGHT},
                    device_scale_factor=2)
    pg.on("console", lambda m: errors.append(m.text[:160]) if m.type == "error" else None)
    pg.goto(base_url, wait_until="networkidle")
    pg.wait_for_selector("text=Marina at a glance", timeout=60000)

    for name in PAGES:
        # Streamlit renders radio options as <label> inside a [role=radiogroup];
        # they carry no accessible name, so get_by_role("radio", name=...) misses.
        pg.set_viewport_size({"width": WIDTH, "height": MIN_HEIGHT})
        pg.locator('[role="radiogroup"] label').filter(
            has_text=re.compile(rf"^{re.escape(name)}$")).click()
        pg.wait_for_timeout(SETTLE_MS)
        height = fit_viewport(pg)
        out = out_dir / f"{name.lower().replace(' ', '_')}.png"
        pg.screenshot(path=out, full_page=True)
        print(f"  {name:24s} {WIDTH}x{height:<5d} -> {out.name}")
    b.close()

print(f"\n  console errors during the sweep: {len(errors)}")
for e in errors[:5]:
    print(f"    {e}")
