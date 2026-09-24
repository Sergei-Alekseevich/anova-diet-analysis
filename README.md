# anova-diet-analysis
One-way ANOVA tool with automatic assumption checks, Welch correction, Tukey HSD post-hoc, and visualizations. Interactive CLI, no code editing required.
# One-Way ANOVA Calculator

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: PEP8](https://img.shields.io/badge/code%20style-PEP8-brightgreen)](https://peps.python.org/pep-0008/)

A universal one-way ANOVA tool with automatic assumption checks,
Welch correction, Tukey HSD post-hoc, and publication-ready visualizations.

Built for educational and research use — suitable for any study with
**one categorical factor** and **one quantitative outcome**.

---

## ✨ Features

- 📊 **Descriptive statistics** per group (mean, median, std, CV, min, max, quartiles)
- 🔍 **Assumption checks** — Shapiro-Wilk (normality) + Levene (equal variances)
- 🧪 **Automatic method selection**
  - Standard one-way ANOVA
  - Welch ANOVA (used when variances are unequal)
- 🎯 **Tukey HSD post-hoc** — all pairwise comparisons with adjusted p-values
- 📈 **Visualizations** — boxplot, per-group histograms, mean ± SE bar plot
- 💾 **CSV export** — all tables saved to `results/` (Excel-friendly UTF-8-BOM)
- 🖥️ **Interactive CLI** — enter data on the fly, no code editing required
- 🔢 **Any number of groups** — works with 2, 3, 5, 10, ... groups
- 📏 **Any units** — kg, mmHg, points, mg/dL, ...

---

## 📋 When to use this tool

This calculator is appropriate when **all** of the following are true:

| Requirement | ✅ |
|---|---|
| **ONE categorical factor** | e.g. diet, drug, breed, treatment, fertilizer |
| **2 or more independent groups** | each subject belongs to exactly one group |
| **ONE quantitative outcome** | kg, mmHg, %, points, mg/dL, ... |
| **n ≥ 5 per group** | better n ≥ 15 for reliable results |
| **Data approximately normal** | checked automatically via Shapiro-Wilk |
| **Equal variances** (or Welch) | checked automatically via Levene's test |

### Typical use cases

| Field | Factor | Outcome |
|---|---|---|
| 🐄 Animal science | breed, feeding type | milk yield, weight gain |
| 💊 Medicine | drug, dose | blood pressure, weight loss |
| 🌾 Agriculture | fertilizer, variety | crop yield |
| 🧪 Biology | temperature, medium | growth rate |
| 🏭 Industry | supplier, batch | product strength |
| 📚 Education | teaching method | test scores |

---

## 🚫 When NOT to use this tool

This calculator is **not suitable** for the following designs — use other methods instead:

| Design | Use instead |
|---|---|
| ❌ **Repeated measures** (same subjects over time) | Repeated Measures ANOVA |
| ❌ **Two or more factors** (e.g. drug × sex) | Two-Way ANOVA |
| ❌ **Ordinal / categorical outcome** | Kruskal-Wallis, chi-square |
| ❌ **Very small samples** (n < 5 per group) | Non-parametric tests |
| ❌ **Strong outliers / severe non-normality** | Kruskal-Wallis |
| ❌ **Covariates to adjust for** (age, baseline) | ANCOVA |

> ⚠️ The script **warns** you if normality or homogeneity of variance
> is violated, so you can interpret results with caution.

---

## 🔬 Analysis pipeline

The tool follows a 6-step statistical pipeline:

1. **Exploratory analysis** — structure, descriptive stats, visualizations
2. **Assumption checks** — Shapiro-Wilk (normality), Levene (equal variances)
3. **ANOVA** — standard or Welch (auto-selected based on Levene's result)
4. **F-statistic and p-value** — with degrees of freedom and F-critical value
5. **Tukey HSD post-hoc** — if the ANOVA is significant
6. **Interpretation** — plain-language conclusions in terms of the study

---

## 🚀 Quick start

```bash
git clone https://github.com/Sergei-Alekseevich/anova-diet-analysis.git
cd anova-diet-analysis
pip install -r requirements.txt

python main.py
```

Follow the interactive prompts to enter:

- the number of groups
- group names
- values for each group
- variable name and unit (optional)

---

## 🧪 Example — 3 diets (student project)

**Input:** three groups of 50 patients each, measured weight loss (kg) after 8 weeks on different diets.

**Console output (abridged):**

```text
======================================================================
  INTERACTIVE ONE-WAY ANOVA CALCULATOR
======================================================================

Loaded groups: 3
Total observations: 150
Groups: ['Diet A', 'Diet B', 'Diet C']

--- 1.2. Descriptive stats per group ----------------------------
         n  mean  median   std   var   min   max    q1    q3  range  cv_%
group
Diet A  50  3.348   3.350  0.228  0.052  2.9   3.8  3.20  3.50  0.900  6.81
Diet B  50  5.448   5.450  0.228  0.052  5.0   5.9  5.30  5.60  0.900  4.19
Diet C  50  2.144   2.100  0.147  0.022  1.9   2.4  2.00  2.30  0.500  6.86

--- 2.1. Normality (Shapiro-Wilk) -------------------------------
Group                   n         W     p-value  Verdict
Diet A                 50    0.9642      0.1332  normal OK
Diet B                 50    0.9642      0.1332  normal OK
Diet C                 50    0.9325      0.0069  NOT normal

--- 2.2. Equal variances (Levene) ------------------------------
Levene statistic = 6.3120
p-value          = 0.0023
-> Variances NOT equal

--- STEP 3-4. ONE-WAY ANOVA (Welch) ---------------------------
  Source  ddof1  ddof2        F  p_unc   np2
0  group      2 93.307 3699.678  0.000 0.978

Conclusion: p < 0.05 -> H0 REJECTED

--- STEP 5. POST-HOC (Tukey HSD) ------------------------------
Diet A vs Diet B: delta = +2.100, p = 0.0000e+00 - SIGNIFICANT
Diet A vs Diet C: delta = -1.204, p = 0.0000e+00 - SIGNIFICANT
Diet B vs Diet C: delta = -3.304, p = 0.0000e+00 - SIGNIFICANT
```

**Conclusion:** Diet B produces the highest average weight loss (**5.45 kg**),
Diet C — the lowest (**2.14 kg**). All differences are statistically
significant (p < 0.001).

---

## 📊 Output

After running, the project produces:

```text
figures/
├── boxplot.png           # distribution by group
├── histograms.png        # per-group histograms with KDE
└── mean_barplot.png      # means ± standard error

results/
├── descriptive_stats.csv # per-group summary table
├── anova_table.csv       # full ANOVA table
└── posthoc_tukey.csv     # pairwise post-hoc comparisons
```

---

## 🏗️ Project structure

```text
anova-diet-analysis/
├── main.py                # entry point
├── requirements.txt
├── README.md
├── data/                  # optional CSV inputs
├── src/
│   ├── __init__.py
│   ├── config.py          # global constants
│   ├── io_utils.py        # interactive input + parsing
│   ├── data_loader.py     # validation + DataFrame construction
│   ├── descriptive.py     # Step 1: EDA
│   ├── assumptions.py     # Step 2: Shapiro-Wilk + Levene
│   ├── anova_test.py      # Step 3-5: ANOVA + Tukey HSD
│   ├── plots.py           # all visualizations
│   ├── report.py          # Step 6: interpretation + CSV export
│   └── cli.py             # pipeline orchestration
├── notebooks/             # Jupyter notebooks
├── figures/               # generated PNG plots (gitignored)
└── results/               # generated CSV tables (gitignored)
```

---

## 🛠️ Technologies

- **Python 3.10+**
- **pandas, numpy** — data manipulation
- **scipy** — statistical tests (Shapiro-Wilk, Levene, F-distribution)
- **statsmodels** — ANOVA and Tukey HSD
- **pingouin** — Welch ANOVA
- **matplotlib, seaborn** — visualization

---

## 📜 License

Released under the **MIT License** — free to use for education and research.

---

## 👤 Author

**Sergei Alekseevich**

- GitHub: [@Sergei-Alekseevich](https://github.com/Sergei-Alekseevich)

---

## 🎓 About this project

This tool was developed as a **student project in biostatistics**, as part of coursework on
statistical methods in animal science and biology.

The goal of the project was to:

- practice **one-way ANOVA** on real and synthetic biological data;
- understand the **conditions of applicability** of parametric tests;
- implement **automatic method selection** (standard vs Welch ANOVA)
  based on assumption checks;
- apply **post-hoc comparisons** (Tukey HSD) to identify which groups differ;
- produce **publication-style visualizations** and exportable result tables.

The tool is used for educational purposes and can be adapted
for any study with a single categorical factor and a quantitative outcome.
