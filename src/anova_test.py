"""
Step 3-5: One-way ANOVA (standard or Welch) + Tukey HSD post-hoc.
"""

import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from src.config import ALPHA
from src.descriptive import print_section, print_subsection


def run_anova(df: pd.DataFrame, use_welch: bool = False) -> dict:
    """Run standard or Welch one-way ANOVA."""
    print_section("STEP 3-4. ONE-WAY ANOVA")

    groups = list(df["group"].unique())
    k = len(groups)

    print_subsection("Hypotheses")
    print(f"H0: {' = '.join(f'mu_{g}' for g in groups)} - all means equal")
    print("H1: at least one group mean differs")
    print(f"alpha = {ALPHA}")

    print_subsection("Results")

    if not use_welch:
        model = ols("value ~ C(group)", data=df).fit()
        table = sm.stats.anova_lm(model, typ=2)
        print(table.to_string())
        F = table.loc["C(group)", "F"]
        p = table.loc["C(group)", "PR(>F)"]
        df1 = int(table.loc["C(group)", "df"])
        df2 = int(table.loc["Residual", "df"])
        F_cr = stats.f.ppf(1 - ALPHA, df1, df2)
        print(f"\nF-statistic       = {F:.4f}")
        print(f"p-value           = {p:.4e}")
        print(f"F-critical        = {F_cr:.4f}  (df = {df1}, {df2}, alpha = {ALPHA})")
        print(f"df between groups = {df1}  (= k - 1 = {k} - 1)")
        print(f"df within groups  = {df2}  (= N - k)")
        significant = p < ALPHA
        print(f"\nConclusion: p {'<' if significant else '>='} {ALPHA} -> "
              f"H0 {'REJECTED' if significant else 'not rejected'}")
        return {"F": F, "p": p, "df1": df1, "df2": df2,
                "F_crit": F_cr, "significant": significant, "table": table}

    # Welch ANOVA (used when Levene's test shows unequal variances)
    try:
        import pingouin as pg
        welch = pg.welch_anova(data=df, dv="value", between="group")
        print(welch.to_string())
        # pingouin 0.6.x uses 'p_unc'; older versions use 'p-unc'
        p_col = "p_unc" if "p_unc" in welch.columns else "p-unc"
        p = float(welch[p_col].iloc[0])
        F = float(welch["F"].iloc[0])
        significant = p < ALPHA
        print(f"\nConclusion: p {'<' if significant else '>='} {ALPHA} -> "
              f"H0 {'REJECTED' if significant else 'not rejected'}")
        return {"F": F, "p": p, "significant": significant, "welch": welch}
    except ImportError:
        print("pingouin not installed - falling back to standard ANOVA")
        return run_anova(df, use_welch=False)


def posthoc_tukey(df: pd.DataFrame) -> list:
    """Run Tukey HSD post-hoc; return list of pairwise results."""
    print_section("STEP 5. POST-HOC (Tukey HSD)")

    tukey = pairwise_tukeyhsd(endog=df["value"], groups=df["group"], alpha=ALPHA)
    print(tukey.summary().as_text())

    print_subsection("All pairwise comparisons")
    results = []
    for row in tukey.summary().data[1:]:
        g1, g2, diff, p_adj, lo, hi, reject = row
        status = "SIGNIFICANT" if reject else "not significant"
        print(f"  {g1} vs {g2}: delta = {diff:+.3f}, p = {p_adj:.4e}, "
              f"95% CI [{lo:.3f}, {hi:.3f}] - {status}")
        results.append({
            "pair": f"{g1} - {g2}",
            "meandiff": diff,
            "p_adj": p_adj,
            "ci_lower": lo,
            "ci_upper": hi,
            "significant": reject,
        })
    return results