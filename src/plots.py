"""
Visualizations: boxplot, histograms, mean ± SE barplot.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _setup_style() -> None:
    sns.set_theme(style="whitegrid", palette="Set2")
    plt.rcParams["font.size"] = 11


def save_boxplot(df: pd.DataFrame, var_name: str, ylabel: str, out_dir: str) -> None:
    """Save boxplot with individual data points."""
    _setup_style()
    os.makedirs(out_dir, exist_ok=True)
    n = df["group"].nunique()

    fig, ax = plt.subplots(figsize=(max(8, n * 1.5), 5))
    sns.boxplot(data=df, x="group", y="value", ax=ax)
    sns.stripplot(data=df, x="group", y="value", color="black",
                  size=3, alpha=0.5, ax=ax)
    ax.set_title(f"{var_name} by group (boxplot)")
    ax.set_xlabel("Group")
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(f"{out_dir}/boxplot.png", dpi=150)
    plt.close(fig)
    print(f"  saved: {out_dir}/boxplot.png")


def save_histograms(df: pd.DataFrame, var_name: str, ylabel: str, out_dir: str) -> None:
    """Save a grid of per-group histograms with KDE."""
    _setup_style()
    os.makedirs(out_dir, exist_ok=True)
    groups = sorted(df["group"].unique())
    cols = min(len(groups), 4)
    rows = (len(groups) + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows),
                             squeeze=False)
    for i, g in enumerate(groups):
        r, c = divmod(i, cols)
        ax = axes[r][c]
        sns.histplot(df.loc[df["group"] == g, "value"], kde=True, ax=ax,
                     bins=min(10, max(3, (df["group"] == g).sum())))
        ax.set_title(g)
        ax.set_xlabel(ylabel)
    for j in range(len(groups), rows * cols):
        r, c = divmod(j, cols)
        axes[r][c].axis("off")
    fig.suptitle(f"Distribution of {var_name.lower()}", y=1.02)
    fig.tight_layout()
    fig.savefig(f"{out_dir}/histograms.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved: {out_dir}/histograms.png")


def save_mean_barplot(df: pd.DataFrame, var_name: str, ylabel: str, out_dir: str) -> None:
    """Save barplot of means with standard error bars."""
    _setup_style()
    os.makedirs(out_dir, exist_ok=True)
    n = df["group"].nunique()

    fig, ax = plt.subplots(figsize=(max(8, n * 1.5), 5))
    sns.barplot(data=df, x="group", y="value", errorbar="se",
                capsize=0.15, ax=ax)
    ax.set_title(f"Mean {var_name.lower()} (M ± SE)")
    ax.set_xlabel("Group")
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(f"{out_dir}/mean_barplot.png", dpi=150)
    plt.close(fig)
    print(f"  saved: {out_dir}/mean_barplot.png")