"""
insurance_plots.py
==================
Plotting functions for the GROUP BY DuckDB tutorial notebook.
All functions accept a pandas DataFrame and keyword arguments,
and produce a matplotlib figure using the shared dark theme.

Usage in notebook:
    from insurance_plots import setup_style, styled_table, *
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Palette (module-level so every function can use it) ───────────────────────
PALETTE = ['#6c8ebf','#f4a261','#2a9d8f','#e76f51',
           '#a8dadc','#457b9d','#e9c46a','#264653']


def setup_style():
    """Apply the dark theme. Call once at the top of the notebook."""
    plt.rcParams.update({
        'figure.facecolor': '#0f1117',
        'axes.facecolor':   '#1a1d2e',
        'axes.edgecolor':   '#3a3f5c',
        'axes.labelcolor':  '#e0e0f0',
        'xtick.color':      '#b0b8d8',
        'ytick.color':      '#b0b8d8',
        'text.color':       '#e0e0f0',
        'grid.color':       '#2a2d40',
        'grid.linestyle':   '--',
        'grid.alpha':       0.5,
        'font.family':      'DejaVu Sans',
        'axes.titlesize':   13,
        'axes.labelsize':   11,
    })
    print('✅  Dark theme applied.')


def styled_table(df):
    """Render a DataFrame as a styled HTML table."""
    fmt = {c: '{:,.2f}' for c in df.select_dtypes('float').columns}
    fmt.update({c: '{:,}' for c in df.select_dtypes('int').columns})
    return (
        df.style
          .format(fmt)
          .set_table_styles([
              {'selector': 'thead th',
               'props': [('background-color','#1e2235'),('color','#a8d8ea'),
                         ('font-weight','bold'),('border-bottom','2px solid #6c8ebf'),
                         ('text-align','center'),('padding','8px 14px')]},
              {'selector': 'tbody td',
               'props': [('background-color','#161929'),('color','#e0e0f0'),
                         ('border-bottom','1px solid #2a2d40'),('padding','6px 14px')]},
              {'selector': 'tbody tr:hover td',
               'props': [('background-color','#252840')]},
              {'selector': 'table',
               'props': [('border-collapse','collapse'),('border-radius','8px'),
                         ('overflow','hidden'),('font-size','13px')]},
          ])
          .hide(axis='index')
    )


# ─────────────────────────────────────────────────────────────────────────────
# PLOT FUNCTIONS — one per lesson cell
# ─────────────────────────────────────────────────────────────────────────────

def plot_histogram(series, title='Distribution of Insurance Charges'):
    """Cell 1 — histogram with mean line."""
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.hist(series, bins=50, color=PALETTE[0], edgecolor='#0f1117', linewidth=0.4)
    ax.axvline(series.mean(), color='#f4a261', linestyle='--', linewidth=1.8,
               label=f'Mean  ${series.mean():,.0f}')
    ax.set_title(title, color='#a8d8ea')
    ax.set_xlabel('Charges ($)')
    ax.set_ylabel('Number of Policies')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend()
    ax.grid(True, axis='y')
    plt.tight_layout()
    plt.show()


def plot_bar_2col(df, x, y1, y2, label1, label2, title):
    """Cell 2 — two side-by-side bar charts sharing the same category axis."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    colors = [PALETTE[0], PALETTE[1]]
    ax1.bar(df[x], df[y1], color=colors, edgecolor='#0f1117', linewidth=0.5)
    ax1.set_title(label1)
    ax1.set_ylabel('Count')
    for bar, val in zip(ax1.patches, df[y1]):
        ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+8,
                 f'{val:,}', ha='center', fontsize=11, color='#e0e0f0')
    ax2.bar(df[x], df[y2], color=colors, edgecolor='#0f1117', linewidth=0.5)
    ax2.set_title(label2)
    ax2.set_ylabel('Avg Charge ($)')
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    for bar, val in zip(ax2.patches, df[y2]):
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+50,
                 f'${val:,.0f}', ha='center', fontsize=10, color='#e0e0f0')
    for ax in [ax1, ax2]:
        ax.grid(True, axis='y')
    plt.suptitle(title, fontsize=14, color='#a8d8ea')
    plt.tight_layout()
    plt.show()


def plot_single_bar(df, x, y, title,
                    color_yes=PALETTE[3], color_no=PALETTE[2]):
    """Cell 3 — single bar chart, smoker yes/no coloured differently."""
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = [color_yes if v == 'yes' else color_no for v in df[x]]
    bars = ax.bar(df[x], df[y], color=colors, edgecolor='#0f1117', width=0.5)
    yes_row = df[df[x] == 'yes']
    no_row  = df[df[x] == 'no']
    if not yes_row.empty and not no_row.empty:
        ratio = yes_row[y].values[0] / no_row[y].values[0]
        ax.set_title(f'Smokers Pay {ratio:.1f}× More — {title}', color='#a8d8ea')
    else:
        ax.set_title(title, color='#a8d8ea')
    for bar, val in zip(bars, df[y]):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+200,
                f'${val:,.0f}', ha='center', fontsize=12,
                color='#e0e0f0', fontweight='bold')
    ax.set_ylabel('Avg Annual Charge ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.grid(True, axis='y')
    plt.tight_layout()
    plt.show()


def plot_pie_bar(df, x, count_col, charge_col, title):
    """Cell 4 — bar chart + pie chart side by side."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.bar(df[x], df[count_col], color=PALETTE[:len(df)], edgecolor='#0f1117')
    ax1.set_title('Policy Count by Region')
    ax1.set_ylabel('Count')
    ax1.grid(True, axis='y')
    wedges, texts, autotexts = ax2.pie(
        df[charge_col], labels=df[x], autopct='%1.1f%%',
        colors=PALETTE[:len(df)], startangle=140, pctdistance=0.75,
        wedgeprops={'edgecolor': '#0f1117', 'linewidth': 1.5})
    for t in autotexts:
        t.set_color('#0f1117')
        t.set_fontweight('bold')
    ax2.set_title('Share of Total Charges')
    plt.suptitle(title, fontsize=14, color='#a8d8ea')
    plt.tight_layout()
    plt.show()


def plot_avg_median(df, x, avg_col, median_col, title):
    """Cell 5 — overlapping bars showing avg vs median."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df[x].astype(str), df[avg_col],    color=PALETTE[0], label='Avg Charge',    alpha=0.85)
    ax.bar(df[x].astype(str), df[median_col], color=PALETTE[2], label='Median Charge', alpha=0.85, width=0.4)
    ax.set_title(title, color='#a8d8ea')
    ax.set_xlabel('Number of Children')
    ax.set_ylabel('Charge ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend()
    ax.grid(True, axis='y')
    plt.tight_layout()
    plt.show()


def plot_hbar(df, x, y, title, xlabel='Avg Charge ($)'):
    """Cell 6 — horizontal bar chart."""
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.barh(df[x], df[y], color=PALETTE[:len(df)], edgecolor='#0f1117')
    for bar, val in zip(bars, df[y]):
        ax.text(val + 150, bar.get_y()+bar.get_height()/2,
                f'${val:,.0f}', va='center', fontsize=10, color='#e0e0f0')
    ax.set_title(title, color='#a8d8ea')
    ax.set_xlabel(xlabel)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.grid(True, axis='x')
    plt.tight_layout()
    plt.show()


def plot_grouped_bar(df, index_col, col_col, val_col, title,
                     colors=None, xlabel=None, stacked=False):
    """Cells 7,8,9,13,16 — grouped (or stacked) bar from a pivot."""
    pivot = df.pivot(index=index_col, columns=col_col, values=val_col)
    clrs  = colors or PALETTE[:len(pivot.columns)]
    fig, ax = plt.subplots(figsize=(10, 4))
    pivot.plot(kind='bar', ax=ax, color=clrs, edgecolor='#0f1117',
               width=0.6, stacked=stacked)
    ax.set_title(title, color='#a8d8ea')
    ax.set_xlabel(xlabel or index_col)
    ax.set_ylabel('Avg Charge ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend(title=col_col)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15)
    ax.grid(True, axis='y')
    plt.tight_layout()
    plt.show()


def plot_line_fill(df, index_col, col_col, val_col, title,
                   col_low='no', col_high='yes'):
    """Cell 10 — line chart with fill between two series."""
    pivot = df.pivot(index=index_col, columns=col_col, values=val_col)
    fig, ax = plt.subplots(figsize=(10, 4))
    pivot.plot(kind='line', ax=ax, marker='o', markersize=8,
               color=['#2a9d8f', '#e76f51'], linewidth=2.5)
    ax.fill_between(range(len(pivot)),
                    pivot[col_low], pivot[col_high],
                    alpha=0.12, color='#e76f51')
    ax.set_xticks(range(len(pivot)))
    ax.set_xticklabels(pivot.index)
    ax.set_title(title, color='#a8d8ea')
    ax.set_ylabel('Avg Charge ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend(title=col_col)
    ax.grid(True)
    plt.tight_layout()
    plt.show()


def plot_hbar_threshold(df, x, y, threshold, title):
    """Cell 11 — horizontal bar with a vertical threshold line."""
    fig, ax = plt.subplots(figsize=(8, 4))
    labels = df[x[0]] + ' / ' + df[x[1]]
    ax.barh(labels, df[y], color=PALETTE[3], edgecolor='#0f1117')
    ax.axvline(threshold, color='#e9c46a', linestyle='--',
               linewidth=1.5, label=f'${threshold:,} threshold')
    ax.set_title(title, color='#a8d8ea')
    ax.set_xlabel('Avg Charge ($)')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend()
    ax.grid(True, axis='x')
    plt.tight_layout()
    plt.show()


def plot_bmi_bar(df, index_col, col_col, val_col, short_labels, title):
    """Cell 12 — side-by-side bars for BMI categories."""
    pivot = df.pivot(index=index_col, columns=col_col, values=val_col)
    fig, ax = plt.subplots(figsize=(10, 4))
    x = range(len(pivot))
    w = 0.35
    ax.bar([i-w/2 for i in x], pivot['no'],  width=w,
           color='#2a9d8f', label='Non-Smoker', edgecolor='#0f1117')
    ax.bar([i+w/2 for i in x], pivot['yes'], width=w,
           color='#e76f51', label='Smoker',     edgecolor='#0f1117')
    ax.set_xticks(list(x))
    ax.set_xticklabels(short_labels)
    ax.set_title(title, color='#a8d8ea')
    ax.set_ylabel('Avg Charge ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend()
    ax.grid(True, axis='y')
    plt.tight_layout()
    plt.show()


def plot_top5(df, x_cols, y, title):
    """Cell 14 — bar chart for top-N groups, label = joined x_cols."""
    fig, ax = plt.subplots(figsize=(10, 4))
    labels = df[x_cols[0]] + '\n' + df[x_cols[1]] + ' / ' + df[x_cols[2]]
    bars = ax.bar(labels, df[y], color=PALETTE[:len(df)], edgecolor='#0f1117')
    for bar, val in zip(bars, df[y]):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+150,
                f'${val:,.0f}', ha='center', fontsize=9, color='#e0e0f0')
    ax.set_title(title, color='#a8d8ea')
    ax.set_ylabel('Avg Charge ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.grid(True, axis='y')
    plt.tight_layout()
    plt.show()


def plot_age_range(df, region_col, min_col, max_col, avg_col, title):
    """Cell 15 — horizontal range lines showing min/max age per region."""
    fig, ax = plt.subplots(figsize=(8, 4))
    for i, row in df.iterrows():
        ax.plot([row[min_col], row[max_col]],
                [row[region_col], row[region_col]],
                color=PALETTE[i % len(PALETTE)], linewidth=6,
                solid_capstyle='round', alpha=0.8)
        ax.scatter(row[avg_col], row[region_col], color='white', s=60, zorder=5)
    ax.set_title(title + '  (dot = average)', color='#a8d8ea')
    ax.set_xlabel('Age')
    ax.grid(True, axis='x')
    plt.tight_layout()
    plt.show()


def plot_error_bar(df, x, bar_col, avg_col, err_col, title):
    """Cell 17 — bar chart with error bars showing stddev."""
    fig, ax = plt.subplots(figsize=(9, 4))
    xpos = range(len(df))
    ax.bar(xpos, df[bar_col], color=PALETTE[:len(df)], edgecolor='#0f1117', alpha=0.85)
    ax.errorbar(xpos, df[avg_col], yerr=df[err_col],
                fmt='o', color='white', capsize=6, linewidth=2, label='Avg ± StdDev')
    ax.set_xticks(list(xpos))
    ax.set_xticklabels(df[x])
    ax.set_title(title, color='#a8d8ea')
    ax.set_ylabel('Charges ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend()
    ax.grid(True, axis='y')
    plt.tight_layout()
    plt.show()


def plot_rollup_stacked(df, region_col, smoker_col, val_col, title):
    """Cell 18 — stacked bar chart from ROLLUP result (excludes total rows)."""
    sub   = df[~df[region_col].str.startswith('──')].copy()
    pivot = sub.pivot(index=region_col, columns=smoker_col, values=val_col).fillna(0)
    pivot = pivot[[c for c in pivot.columns if not str(c).startswith('──')]]
    fig, ax = plt.subplots(figsize=(10, 4))
    pivot.plot(kind='bar', stacked=True, ax=ax,
               color=['#2a9d8f', '#e76f51'], edgecolor='#0f1117')
    ax.set_title(title, color='#a8d8ea')
    ax.set_xlabel('Region')
    ax.set_ylabel('Total Charges ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e6:.1f}M'))
    ax.legend(title='Smoker')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15)
    ax.grid(True, axis='y')
    plt.tight_layout()
    plt.show()


def plot_rank_hbar(df, region_col, smoker_col, val_col, rank_col, title):
    """Cell 19 — side-by-side horizontal bars, one panel per smoker group."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=False)
    for ax, smoker, color in zip(axes, ['yes', 'no'], ['#e76f51', '#2a9d8f']):
        sub  = df[df[smoker_col] == smoker].sort_values(val_col, ascending=True)
        bars = ax.barh(sub[region_col], sub[val_col], color=color, edgecolor='#0f1117')
        for bar, rank in zip(bars, sub[rank_col]):
            ax.text(bar.get_width()-500, bar.get_y()+bar.get_height()/2,
                    f'#{int(rank)}', va='center', color='white',
                    fontweight='bold', fontsize=11)
        ax.set_title(f'Smoker = {smoker}  — Region Ranking', color='#a8d8ea')
        ax.set_xlabel('Avg Charge ($)')
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
        ax.grid(True, axis='x')
    plt.suptitle(title, fontsize=13, color='#a8d8ea')
    plt.tight_layout()
    plt.show()


def plot_bubble(df, x_col, y_col, size_col, color_col,
                label_cols, rank_col, title):
    """Cell 20 — bubble scatter, size = policy count, colour = revenue."""
    fig, ax = plt.subplots(figsize=(12, 5))
    labels = df[label_cols[0]] + '\n' + df[label_cols[1]] + '/' + df[label_cols[2]]
    sc = ax.scatter(range(len(df)), df[y_col],
                    c=df[color_col], cmap='plasma',
                    s=df[size_col]*4, alpha=0.85,
                    edgecolors='white', linewidth=0.6)
    plt.colorbar(sc, ax=ax, label='Total Charges ($)',
                 format=mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    for i, row in df.iterrows():
        ax.text(i, row[y_col]+250, f"#{int(row[rank_col])}",
                ha='center', fontsize=8, color='#e0e0f0')
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_title(title, color='#a8d8ea', fontsize=13)
    ax.set_ylabel('Avg Charge ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.grid(True, axis='y')
    plt.tight_layout()
    plt.show()
