"""
Command-line pipeline: ties all steps together.
"""

import sys

from src.io_utils import ask_groups, ask_variable_label, ask_yes_no
from src.data_loader import validate_data, build_dataframe
from src.descriptive import exploratory_analysis, print_section
from src.assumptions import check_assumptions
from src.anova_test import run_anova, posthoc_tukey
from src.report import interpret, save_results


def run_pipeline() -> None:
    """Run one full analysis iteration."""
    print("\n" + "=" * 70)
    print("  INTERACTIVE ONE-WAY ANOVA CALCULATOR")
    print("=" * 70)

    data = ask_groups()
    var_name, var_unit = ask_variable_label()

    try:
        validate_data(data)
    except (TypeError, ValueError) as e:
        print(f"Data error: {e}")
        sys.exit(1)

    df = build_dataframe(data)
    print(f"\nLoaded groups: {df['group'].nunique()}")
    print(f"Total observations: {len(df)}")
    print(f"Groups: {list(df['group'].unique())}")

    desc = exploratory_analysis(df, var_name, var_unit)
    assumptions = check_assumptions(df)

    use_welch = not assumptions["levene"]["equal_var"]
    anova_res = run_anova(df, use_welch=use_welch)

    posthoc_res = []
    if anova_res.get("significant"):
        posthoc_res = posthoc_tukey(df)
    else:
        print_section("STEP 5. POST-HOC")
        print("No significant differences - post-hoc skipped.")

    interpret(df, anova_res, posthoc_res, var_name, var_unit)
    save_results(desc, anova_res, posthoc_res)

    print("\n" + "=" * 70)
    print("  ANALYSIS COMPLETE")
    print("=" * 70 + "\n")


def main() -> None:
    """Entry point with optional repeat."""
    run_pipeline()
    if ask_yes_no("\nRun another analysis?", default=False):
        main()