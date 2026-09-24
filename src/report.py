"""
Step 6: Interpretation + saving results to CSV.
"""

import os
import pandas as pd

from src.config import ALPHA, OUTPUT_DIR, SAVE_CSV
from src.descriptive import print_section


def interpret(df: pd.DataFrame, anova_res: dict, posthoc_res: list,
              var_name: str, var_unit: str) -> None:
    """Print a plain-language interpretation of the results."""
    print_section("STEP 6. INTERPRETATION")

    means = df.groupby("group")["value"].mean().round(3)
    best, worst = means.idxmax(), means.idxmin()

    print("Group means:")
    for g, m in means.items():
        print(f"  {g}: {m:.3f} {var_unit}".strip())

    print(f"\nHighest: {best} ({means[best]:.3f} {var_unit})".strip())
    print(f"Lowest:  {worst} ({means[worst]:.3f} {var_unit})".strip())
    print(f"Range:   {means[best] - means[worst]:.3f} {var_unit}".strip())

    print("\nStatistical conclusion:")
    if anova_res.get("significant"):
        print(f"  p = {anova_res['p']:.4e} < {ALPHA} -> H0 REJECTED")
        print("  Differences between groups are statistically significant.")
    else:
        print(f"  p = {anova_res['p']:.4f} >= {ALPHA} -> H0 not rejected")
        print("  No statistically significant differences.")

    if posthoc_res:
        sig = [r for r in posthoc_res if r["significant"]]
        print(f"\nTukey: significant pairs - {len(sig)} of {len(posthoc_res)}")
        for r in sig:
            print(f"  - {r['pair']}: delta = {r['meandiff']:+.3f}, "
                  f"p = {r['p_adj']:.4e}")


def save_results(desc: pd.DataFrame, anova_res: dict,
                 posthoc_res: list) -> None:
    """Save result tables as UTF-8-BOM CSVs (Excel-friendly)."""
    if not SAVE_CSV:
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    desc.to_csv(f"{OUTPUT_DIR}/descriptive_stats.csv", encoding="utf-8-sig")
    if "table" in anova_res:
        anova_res["table"].to_csv(f"{OUTPUT_DIR}/anova_table.csv",
                                  encoding="utf-8-sig")
    if posthoc_res:
        pd.DataFrame(posthoc_res).to_csv(f"{OUTPUT_DIR}/posthoc_tukey.csv",
                                         index=False, encoding="utf-8-sig")
    print(f"\nSaved: {OUTPUT_DIR}/")