#!/usr/bin/env python3
"""Generate images/er_diagram.png — the "How the Tables Connect" diagram.

Replaces the old box-drawing ASCII-art code fence (illegible in print, and
prone to splitting across a page break). Re-run this after editing the
layout below; then re-run make_pdf.sh / make_pdf_html.sh to pick it up.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path

INK = "#1a1a1a"        # box border / text
MUTED = "#57606a"       # row-count subtitle
ACCENT = "#0969da"      # arrows + cardinality labels
FACE = "#f6f8fa"        # box fill

fig, ax = plt.subplots(figsize=(9.5, 3.3), dpi=300)
ax.set_xlim(0, 9.5)
ax.set_ylim(0, 3.3)
ax.axis("off")

BOX_W, BOX_H = 1.7, 0.9


def box(cx, cy, title, subtitle):
    ax.add_patch(FancyBboxPatch(
        (cx - BOX_W / 2, cy - BOX_H / 2), BOX_W, BOX_H,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=1.3, edgecolor=INK, facecolor=FACE, zorder=2,
    ))
    ax.text(cx, cy + 0.14, title, ha="center", va="center",
             fontsize=12.5, fontweight="bold", color=INK,
             family="monospace", zorder=3)
    ax.text(cx, cy - 0.20, subtitle, ha="center", va="center",
             fontsize=9.5, color=MUTED, zorder=3)


def arrow(x0, x1, y, label):
    ax.add_patch(FancyArrowPatch(
        (x0, y), (x1, y), arrowstyle="-|>", mutation_scale=14,
        linewidth=1.4, color=ACCENT, zorder=1,
    ))
    ax.text((x0 + x1) / 2, y + 0.20, label, ha="center", va="center",
             fontsize=10, fontweight="bold", color=ACCENT)


top_y = 2.45
gap = 0.55
xs = [1.1, 3.55, 6.15, 8.6]  # customers, orders, order_items, products

box(xs[0], top_y, "customers", "(8 rows)")
box(xs[1], top_y, "orders", "(10 rows)")
box(xs[2], top_y, "order_items", "(15 rows)")
box(xs[3], top_y, "products", "(6 rows)")

arrow(xs[0] + BOX_W / 2 + 0.05, xs[1] - BOX_W / 2 - 0.05, top_y, "1 : N")
arrow(xs[1] + BOX_W / 2 + 0.05, xs[2] - BOX_W / 2 - 0.05, top_y, "1 : N")
arrow(xs[3] - BOX_W / 2 - 0.05, xs[2] + BOX_W / 2 + 0.05, top_y, "N : 1")

# employees, with a self-join loop for manager_id -> employee_id
emp_x, emp_y = 1.1, 0.65
box(emp_x, emp_y, "employees", "(7 rows)")

loop = FancyArrowPatch(
    posA=(emp_x + BOX_W / 2, emp_y + 0.22),
    posB=(emp_x + BOX_W / 2, emp_y - 0.22),
    connectionstyle="arc3,rad=-1.5",
    arrowstyle="-|>", mutation_scale=14, linewidth=1.4, color=ACCENT,
)
ax.add_patch(loop)
ax.text(emp_x + BOX_W / 2 + 1.05, emp_y, "manager_id references employee_id\n(self-join — an employee's manager\nis also a row in this table)",
         ha="left", va="center", fontsize=9.5, color=INK)

fig.tight_layout(pad=0.3)
fig.savefig("images/er_diagram.png", transparent=False, facecolor="white")
print("wrote images/er_diagram.png")
