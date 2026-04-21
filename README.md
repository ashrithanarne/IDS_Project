# Does the World Notice? Analyzing Media Coverage of Global Humanitarian Crises

**Live Site:** https://ashrithanarne.github.io/IDS_Project/
**Report:** https://ashrithanarne.github.io/IDS_Project/IDS_final_report.pdf

---

## Project Overview

This project investigates whether international media coverage of humanitarian crises aligns
with their measurable severity. Using a dataset of 78,667 news articles spanning ten crises
from 2009 to 2025, we apply exploratory analysis, feature engineering, and regression modeling
to identify what predicts monthly media attention.

**Key Finding:** Coverage is driven more by the timing of crises and geopolitical salience
than by humanitarian scale. Gaza received 83 times more articles per person affected than
Sudan, despite Sudan having nine times more people in need. Regression modeling confirms
that crisis duration and funding requirements are stronger predictors of coverage than the
number of people affected.

**Authors:** Ashritha Narne & Nikhitha Nagabhyru
**Course:** CAP5771 — Introduction to Data Science, University of Florida
**Semester:** Spring 2026

---

## Data Source

Data is sourced from the *Humanitarian Crisis Coverage Report* published by the Media and
Journalism Research Center (Dragomir, 2025), which collected and processed 78,667 news
articles from English-language outlets across the US, UK, Canada, Australia, Ireland, and
three internationally prominent non-Western outlets (Al Jazeera, RT, IRNA).

> Dragomir, M. (2025). Humanitarian Crisis Coverage Report. Media and Journalism Research
> Center. https://doi.org/10.13140/RG.2.2.13831.87203

---

## Repository Structure

## Repository Structure

```
IDS_Project/
├── data/
│   ├── raw/                                   # Original CSV datasets from MJRC
│   │   ├── chart1_overall_coverage_bar.csv
│   │   ├── chart3_monthly_coverage.csv
│   │   ├── chart4_crisis_coverage_per_outlet_chart.csv
│   │   ├── framing_per_article.csv
│   │   ├── sentiment_per_article.csv
│   │   └── victim_causor_per_article.csv
│   └── processed/
│       └── monthly_model_data.csv             # 734-row monthly modeling dataset
├── docs/
│   ├── index.html                             # GitHub Pages landing page
│   └── IDS_final_report.pdf                  # Final project report
├── notebooks/
│   ├── milestone_1/
│   │   └── exploratory_analysis.ipynb         # EDA and database creation
│   └── milestone_2/
│       ├── data_wrangling.ipynb               # Feature engineering and master table
│       ├── data_modeling.ipynb                # Model training and evaluation
│       ├── data_visualization_static.ipynb    # Interactive ipywidgets dashboard
│       ├── dashboard_summary.png              # Dashboard export image
│       └── humanitarian.db                    # SQLite relational database
├── diary/                                     # Weekly reflection entries
├── docs_archive/                              # Database schema diagram and reference
│   ├── database_schema
│   └── humanitarian_db_schema.png
├── sql/
│   └── schema.sql                            # Relational database schema
├── .gitignore
├── data_dictionary.pdf
├── database_file_access_instructions.md
├── README.md
└── requirements.txt
```

---

## How to Reproduce

### Milestone 1 — Database and Exploratory Analysis
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run `notebooks/exploratory_analysis.ipynb` to recreate the SQLite database
   and all exploratory visualizations

### Milestone 2 — Wrangling, Modeling, and Dashboard
1. Run `notebooks/milestone_2/data_wrangling.ipynb` to produce
   `data/processed/monthly_model_data.csv`
2. Run `notebooks/milestone_2/data_modeling.ipynb` to train and evaluate
   the four regression models
3. Run `notebooks/milestone_2/data_visualization_static.ipynb` to launch
   the interactive dashboard

### Final Report
The final report PDF is available at the live site link above, or directly in
`docs/IDS_final_report.pdf`.

---

## Model Results Summary

| Model | Test R² | RMSE | MAE |
|---|---|---|---|
| Linear Regression | 0.653 | 0.760 | 0.615 |
| Ridge Regression | 0.656 | 0.757 | 0.612 |
| Decision Tree (depth 4) | 0.674 | 0.737 | 0.602 |
| Random Forest (200 trees) | 0.472 | 0.937 | 0.769 |

Target variable: log-transformed monthly article count across 734 monthly observations.

---

## Key Features Engineered

| Feature | Description |
|---|---|
| `months_since_start` | Months elapsed since each crisis began |
| `is_onset` | Binary flag for first 3 months of a crisis |
| `log_coverage` | Log-transformed monthly article count (target) |
| `top3_outlet_ratio` | Share of coverage from the top 3 outlets |
| `post_onset_ratio` | Ratio of post-onset to onset coverage |
| `framing_ratio_*` | Framing composition (Gaza and Ukraine only) |

---

## Data Limitations

- Framing, sentiment, and victim/causor data are only available for Gaza and Ukraine.
  All analyses involving these features are scoped to those two crises.
- The dataset is weighted toward English-language Anglophone media from the Global North.
- All numerical indicators are sourced from and normalized by the MJRC study.
- The modeling target is log-transformed to reduce skew from high-coverage crises.

---

## Dependencies

pandas
numpy
matplotlib
seaborn
scikit-learn
ipywidgets
sqlite3

Install with: `pip install -r requirements.txt`