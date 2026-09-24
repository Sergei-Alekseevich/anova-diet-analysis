"""
Step 1: Exploratory, descriptive, and visual analysis.
"""

import pandas as pd

from src.config import FIGURE_DIR, SAVE_FIGURES
from src.plots import save_boxplot, save_histograms, save_mean_barplot


def print_section(title: str) -> None:
    print(f"\n{'=' * 70}\n  {title}\n{'=' * 70}")


def print_subsection(title: str) -> None:
    print(f"\n--- {title} " + "-" * max(1, 60 - len(title)))


def descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-group descriptive statistics."""
    desc = (
        df.groupby("group")["value"]
        .agg(
            n="count",
            mean="mean",
            median="median",
            std="std",
            var="var",
            min="min",
            max="max",
            q1=lambda x: x.quantile(0.25),
            q3=lambda x: x.quantile(0.75),
        )
        .round(3)
    )
    desc["range"] = (desc["max"] - desc["min"]).round(3)
    desc["cv_%"] = (desc["std"] / desc["mean"] * 100).round(2)
    return desc


def exploratory_analysis(df: pd.DataFrame, var_name: str, var_unit: str) -> pd.DataFrame:
    """Run Step 1: descriptive stats + save figures. Returns desc table."""
    print_section("STEP 1. EXPLORATORY / DESCRIPTIVE / VISUAL ANALYSIS")

    print_subsection("1.1. Structure")
    print(f"Total observations: {len(df)}")
    print(f"Number of groups:   {df['group'].nunique()}")
    print(f"Groups:             {list(df['group'].unique())}")
    print("\nGroup sizes:")
    print(df["group"].value_counts().to_string())

    print_subsection("1.2. Descriptive stats per group")
    desc = descriptive_stats(df)
    print(desc.to_string())

    print_subsection("1.3. Overall stats")
    print(df["value"].describe().round(3).to_string())

    if SAVE_FIGURES:
        print_subsection("1.4. Figures")
        ylabel = f"{var_name}, {var_unit}".strip(", ")
        save_boxplot(df, var_name, ylabel, FIGURE_DIR)
        save_histograms(df, var_name, ylabel, FIGURE_DIR)
        save_mean_barplot(df, var_name, ylabel, FIGURE_DIR)

    return desc