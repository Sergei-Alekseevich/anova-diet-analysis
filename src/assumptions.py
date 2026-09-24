"""
Step 2: Assumption checks (Shapiro-Wilk, Levene).
"""

import pandas as pd
from scipy import stats

from src.config import ALPHA
from src.descriptive import print_section, print_subsection


def check_assumptions(df: pd.DataFrame) -> dict:
    """Run Shapiro-Wilk and Levene tests; return results dict."""
    print_section("STEP 2. ASSUMPTION CHECKS")
    results = {}

    print_subsection("2.1. Normality (Shapiro-Wilk)")
    print(f"{'Group':<20}{'n':>5}{'W':>10}{'p-value':>12}  Verdict")
    for g in df["group"].unique():
        s = df.loc[df["group"] == g, "value"]
        if len(s) < 3:
            print(f"{g:<20}{len(s):>5}{'-':>10}{'-':>12}  too few")
            results[f"shapiro_{g}"] = {"normal": None}
            continue
        W, p = stats.shapiro(s)
        verdict = "normal OK" if p > ALPHA else "NOT normal"
        print(f"{g:<20}{len(s):>5}{W:>10.4f}{p:>12.4f}  {verdict}")
        results[f"shapiro_{g}"] = {"W": W, "p": p, "normal": p > ALPHA}

    print_subsection("2.2. Equal variances (Levene)")
    groups = [g["value"].values for _, g in df.groupby("group")]
    lev_stat, lev_p = stats.levene(*groups, center="median")
    print(f"Levene statistic = {lev_stat:.4f}")
    print(f"p-value          = {lev_p:.4f}")
    print("-> Variances equal" if lev_p > ALPHA else "-> Variances NOT equal")
    results["levene"] = {"stat": lev_stat, "p": lev_p, "equal_var": lev_p > ALPHA}

    print_subsection("2.3. Overall")
    normals = [v["normal"] for k, v in results.items() if k.startswith("shapiro")]
    normal_all = all(n for n in normals if n is not None)
    if normal_all and results["levene"]["equal_var"]:
        print("All conditions met -> standard one-way ANOVA")
    elif normal_all and not results["levene"]["equal_var"]:
        print("Normal, unequal variances -> Welch ANOVA will be used")
    else:
        print("Normality violated -> prefer Kruskal-Wallis (non-parametric)")

    return results