"""
acid_plot_util.py — display + plotting helpers for the Week 8 transactions notebook.

All presentation code lives here so the notebook stays SQL + explanation.

Exports
-------
    display_table(df, caption)          pretty-print a result set
    show_balances(con, caption)         the accounts table, formatted
    plot_transfer_states(states)        balances at each step of a transfer
    plot_isolation(reader, writer)      what two connections see at the same moment
    plot_acid_summary(results)          which ACID property each demo proved
"""

import matplotlib.pyplot as plt

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

ALICE = "#2a78d6"   # blue
BOB = "#eb6834"     # orange
GOOD = "#1baf7a"    # aqua
BAD = "#c73e1d"     # deep red, for the failure states

plt.rcParams.update({
    "figure.figsize": (9, 5),
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK_SECONDARY,
    "axes.titlecolor": INK,
    "axes.titlesize": 13,
    "axes.titleweight": "600",
    "axes.titlelocation": "left",
    "axes.titlepad": 14,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": GRIDLINE,
    "grid.linewidth": 0.8,
    "text.color": INK,
    "xtick.color": INK_MUTED,
    "ytick.color": INK_MUTED,
    "legend.frameon": False,
})


# ── Display ──────────────────────────────────────────────────────────────────

def display_table(df, caption=""):
    if caption:
        print(f"\n{caption}")
        print("-" * max(len(caption), 40))
    print(df.to_string(index=False))
    print()
    return df


def show_balances(con, caption="Account balances"):
    df = con.execute("""
        SELECT account_id, owner, balance
        FROM accounts
        ORDER BY account_id
    """).df()
    return display_table(df, caption)


# ── Charts ───────────────────────────────────────────────────────────────────

def _style(ax, title, xlabel=None, ylabel=None):
    ax.set_title(title, color=INK)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, labelpad=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, labelpad=10)
    ax.grid(axis="y")
    ax.grid(axis="x", visible=False)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    return ax


def _label(ax, bars, values, fmt="{:,.0f}"):
    span = max(values) if values else 1
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + span * 0.02,
                fmt.format(v), ha="center", va="bottom",
                fontsize=9, color=INK_SECONDARY)


def plot_transfer_states(states):
    """
    Grouped bars showing both balances at each stage of a transfer.

    `states` is a list of (label, alice_balance, bob_balance). The total is
    annotated above each pair, because the whole point of a transfer is that the
    total must never change.
    """
    labels = [s[0] for s in states]
    alice = [float(s[1]) for s in states]
    bob = [float(s[2]) for s in states]
    x = range(len(states))
    w = 0.38

    fig, ax = plt.subplots(figsize=(10, 5.5))
    b1 = ax.bar([i - w / 2 - 0.01 for i in x], alice, width=w,
                color=ALICE, label="Alice")
    b2 = ax.bar([i + w / 2 + 0.01 for i in x], bob, width=w,
                color=BOB, label="Bob")

    _style(ax, "Both balances at each step — the total must never change",
           ylabel="Balance")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, max(alice + bob) * 1.28)
    _label(ax, b1, alice)
    _label(ax, b2, bob)

    top = max(alice + bob) * 1.18
    for i, (a, b) in enumerate(zip(alice, bob)):
        ax.text(i, top, f"total {a + b:,.0f}", ha="center", fontsize=9,
                color=GOOD if abs((a + b) - (alice[0] + bob[0])) < 0.01 else BAD,
                fontweight="600")

    ax.legend(loc="upper left")
    fig.tight_layout()
    return fig


def plot_isolation(writer_sees, reader_sees, committed):
    """Three bars: what the writer sees mid-transaction, what everyone else sees."""
    labels = ["Writer\n(inside its transaction)",
              "Reader\n(another connection)",
              "Reader\n(after COMMIT)"]
    values = [float(writer_sees), float(reader_sees), float(committed)]
    colors = [ALICE, GOOD, ALICE]

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, width=0.6, color=colors)
    _style(ax, "Isolation: uncommitted changes are invisible to everyone else",
           ylabel="Alice's balance")
    ax.set_ylim(0, max(values) * 1.2)
    _label(ax, bars, values)
    fig.tight_layout()
    return fig


def plot_acid_summary(results):
    """
    Horizontal bar marking each ACID property as demonstrated.

    `results` is a list of (letter, property_name, demonstrated_bool).
    """
    labels = [f"{letter} — {name}" for letter, name, _ in results][::-1]
    ok = [1 if d else 0 for _, _, d in results][::-1]
    colors = [GOOD if v else BAD for v in ok]

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.barh(labels, [1] * len(labels), height=0.6, color=colors)

    _style(ax, "All four ACID properties, demonstrated rather than defined")
    ax.grid(axis="x", visible=False)
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    for side in ("bottom",):
        ax.spines[side].set_visible(False)
    for i, (_, _, d) in enumerate(results[::-1]):
        ax.text(0.02, i, "demonstrated" if d else "not shown",
                va="center", ha="left", fontsize=10,
                color="white", fontweight="600")

    fig.tight_layout()
    return fig
