"""
util_plot.py - Plotting utilities for the Auto Insurance data story.

All visualization code is centralized here to keep notebooks clean and focused
on SQL logic and explanations. Uses matplotlib + seaborn for polished static plots.

Usage in notebooks:
    from util_plot import *
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# -- Global style setup --
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'figure.dpi': 100,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
})

COLORS = sns.color_palette("muted", 10)


def plot_bar(df, x, y, title, xlabel=None, ylabel=None, horizontal=False, top_n=None, color=None):
    """Bar chart from a DataFrame. Optionally limit to top N rows."""
    if top_n:
        df = df.head(top_n)

    fig, ax = plt.subplots(figsize=(10, max(5, len(df) * 0.4)) if horizontal else (10, 6))

    if horizontal:
        ax.barh(df[x].astype(str), df[y], color=color or COLORS[0])
        ax.set_xlabel(ylabel or y)
        ax.set_ylabel(xlabel or x)
        ax.invert_yaxis()
    else:
        ax.bar(df[x].astype(str), df[y], color=color or COLORS[0])
        ax.set_xlabel(xlabel or x)
        ax.set_ylabel(ylabel or y)
        plt.xticks(rotation=45, ha='right')

    ax.set_title(title, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_grouped_bar(df, x, y, hue, title, xlabel=None, ylabel=None):
    """Grouped bar chart using seaborn."""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=df, x=x, y=y, hue=hue, ax=ax)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title=hue, bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def plot_histogram(df, column, title, bins=30, xlabel=None, ylabel="Frequency", kde=True):
    """Histogram with optional KDE overlay."""
    fig, ax = plt.subplots()
    sns.histplot(data=df, x=column, bins=bins, kde=kde, ax=ax, color=COLORS[0])
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel or column)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    plt.show()


def plot_boxplot(df, x, y, title, xlabel=None, ylabel=None):
    """Box plot for comparing distributions across categories."""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x=x, y=y, ax=ax, palette="muted")
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def plot_pie(df, labels_col, values_col, title, top_n=8):
    """Pie chart from a DataFrame. Groups small slices into 'Other'."""
    data = df[[labels_col, values_col]].copy()
    if len(data) > top_n:
        top = data.head(top_n)
        other_val = data.iloc[top_n:][values_col].sum()
        other_row = pd.DataFrame({labels_col: ['Other'], values_col: [other_val]})
        data = pd.concat([top, other_row], ignore_index=True)

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        data[values_col], labels=data[labels_col],
        autopct='%1.1f%%', startangle=90, colors=sns.color_palette("muted", len(data))
    )
    ax.set_title(title, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_scatter(df, x, y, title, hue=None, xlabel=None, ylabel=None):
    """Scatter plot with optional color grouping."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x=x, y=y, hue=hue, ax=ax, alpha=0.6)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    if hue:
        plt.legend(title=hue, bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def plot_heatmap(df, title, fmt=".2f", cmap="YlOrRd", annot=True):
    """Heatmap from a pivot table or correlation matrix."""
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(df, annot=annot, fmt=fmt, cmap=cmap, ax=ax, linewidths=0.5)
    ax.set_title(title, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_line(df, x, y, title, xlabel=None, ylabel=None, hue=None):
    """Line chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    if hue:
        sns.lineplot(data=df, x=x, y=y, hue=hue, ax=ax, marker='o')
        plt.legend(title=hue, bbox_to_anchor=(1.02, 1), loc='upper left')
    else:
        ax.plot(df[x], df[y], marker='o', color=COLORS[0])
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.tight_layout()
    plt.show()


def plot_countplot(df, column, title, xlabel=None, ylabel="Count", order=None, horizontal=False):
    """Count plot for categorical data."""
    fig, ax = plt.subplots(figsize=(10, 6))
    if horizontal:
        sns.countplot(data=df, y=column, order=order, ax=ax, palette="muted")
    else:
        sns.countplot(data=df, x=column, order=order, ax=ax, palette="muted")
        plt.xticks(rotation=45, ha='right')
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel or ("Count" if horizontal else column))
    ax.set_ylabel(ylabel if not horizontal else column)
    plt.tight_layout()
    plt.show()


def plot_top_n_bar(df, value_col, label_col, title, n=10, xlabel=None):
    """Horizontal bar chart for Top-N rankings."""
    top = df.head(n)
    fig, ax = plt.subplots(figsize=(10, max(4, n * 0.5)))
    bars = ax.barh(range(n), top[value_col], color=COLORS[0])
    ax.set_yticks(range(n))
    ax.set_yticklabels(top[label_col].astype(str))
    ax.invert_yaxis()
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel or value_col)

    # Add value labels on bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width * 1.01, bar.get_y() + bar.get_height()/2,
                f'{width:,.0f}', va='center', fontsize=9)

    plt.tight_layout()
    plt.show()
