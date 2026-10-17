"""Helpers for notebook.py — a chart and an HTML "matchmaker" view.

They live here so the notebook can focus on the SQL.
Every function accepts pandas or polars columns (anything with
.to_list(), or a plain list).
"""

import matplotlib.pyplot as plt

# One fixed color per idea, used everywhere
GREY = "#9AA5B1"      # "before the join": numbers only
BLUE = "#2E86DE"      # "after the join": real names
TEXT = "#2D3436"
MUTED = "#636E72"


def _list(values):
    return values.to_list() if hasattr(values, "to_list") else list(values)


def _style(ax, title):
    ax.set_title(title, fontsize=13, fontweight="bold", color=TEXT, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)


def _bars(ax, labels, values, color):
    top = max(values)
    ax.bar(range(len(labels)), values, color=color, width=0.6)
    for i, v in enumerate(values):
        ax.text(i, v + top * 0.03, f"${v:,.2f}", ha="center",
                fontsize=10, color=TEXT, fontweight="bold")
    ax.set_xticks(range(len(labels)), labels)
    ax.set_ylim(0, top * 1.2)
    ax.set_ylabel("Total spent ($)", fontsize=11, color=TEXT)


def plot_before_after(ids, id_totals, names, name_totals):
    """Two bar charts side by side: totals by customer_id (orders table
    alone) and the same totals by customer name (after the join)."""
    ids = [str(i) for i in _list(ids)]
    names = _list(names)
    id_totals = [float(v) for v in _list(id_totals)]
    name_totals = [float(v) for v in _list(name_totals)]

    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    _bars(left, ids, id_totals, GREY)
    _style(left, "BEFORE: orders table alone\n(who are these numbers?)")
    left.set_xlabel("customer_id", fontsize=11, color=MUTED)

    _bars(right, names, name_totals, BLUE)
    _style(right, "AFTER: orders INNER JOIN customers\n(real people!)")
    right.set_xlabel("customer name", fontsize=11, color=MUTED)

    fig.tight_layout()
    return fig


# -- The matchmaker: one order compared with every customer ----------
_CELL = "padding:6px 12px;border-bottom:1px solid rgba(128,128,128,.25);"
_HEAD = _CELL + "font-weight:700;text-align:left;"
_MATCH = "background:rgba(46,204,113,.28);font-weight:700;"
_PICKED = "background:rgba(241,196,15,.35);font-weight:700;"


def _table(headers, rows, row_styles):
    head = "".join(f"<th style='{_HEAD}'>{h}</th>" for h in headers)
    body = ""
    for row, style in zip(rows, row_styles):
        cells = "".join(f"<td style='{_CELL}'>{v}</td>" for v in row)
        body += f"<tr style='{style}'>{cells}</tr>"
    return (f"<table style='border-collapse:collapse;font-size:15px;'>"
            f"<tr>{head}</tr>{body}</table>")


def matchmaker_html(order, customers):
    """order: dict with order_id, customer_id, item, price.
    customers: dict of lists with customer_id, name, city.
    Returns HTML: the order, every comparison, and the glued row."""
    key = order["customer_id"]
    cust_ids = _list(customers["customer_id"])
    names = _list(customers["name"])
    cities = _list(customers["city"])

    step1 = _table(
        ["order_id", "customer_id", "item", "price"],
        [[order["order_id"], f"<b>{key}</b>", order["item"],
          f"${order['price']:.2f}"]],
        [_PICKED],
    )

    rows, styles, match = [], [], None
    for cid, name, city in zip(cust_ids, names, cities):
        same = cid == key
        verdict = "✅ match — keep it!" if same else "❌ no match"
        rows.append([cid, name, city, f"{key} = {cid} ?", verdict])
        styles.append(_MATCH if same else "opacity:.55;")
        if same:
            match = (cid, name, city)
    step2 = _table(
        ["customer_id", "name", "city", "test", "result"], rows, styles)

    step3 = _table(
        ["order_id", "item", "price", "customer_id", "name", "city"],
        [[order["order_id"], order["item"], f"${order['price']:.2f}",
          match[0], match[1], match[2]]],
        [_MATCH],
    )

    return f"""
    <div style="display:flex;flex-direction:column;gap:14px;">
      <div><b>Step 1 — Take one row from <code>orders</code>.</b>
           Its <code>customer_id</code> is <b>{key}</b>.<br>{step1}</div>
      <div><b>Step 2 — Compare it with every row in <code>customers</code>.</b>
           Is <code>o.customer_id = c.customer_id</code>?<br>{step2}</div>
      <div><b>Step 3 — Glue the matching rows side by side.</b> 🪄<br>
           {step3}</div>
    </div>
    """
