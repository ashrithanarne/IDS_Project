# Humanitarian Media Coverage Analysis

## Project Overview
This project investigates how global humanitarian crises are covered in the media.
Using publicly available datasets, we analyze the volume, distribution, and framing
of news coverage across multiple crises, outlets, and time periods. The aim is to
assess whether media attention aligns with measurable humanitarian indicators such
as number of people affected, funds required, and crisis duration, and to explore
the structural and narrative factors influencing coverage patterns.

## Data Sources
- **Crises data:** Overview of humanitarian crises including start date, funds required,
  people affected, and coverage metrics.
- **Monthly coverage:** Time-series data showing the number of articles published per
  crisis per month.
- **Outlet coverage:** Number of articles published per media outlet for each crisis.
- **Framing data:** Classification of articles based on narrative frame (e.g.,
  humanitarian, economic, geopolitical). Available for Gaza and Ukraine only.
- **Sentiment data:** Sentiment of media mentions per entity within crisis coverage.
  Available for Gaza and Ukraine only.
- **Victim/Causor data:** Mentions of victims or causative actors in each article.
  Available for Gaza and Ukraine only.

## Project Structure
IDS_Project/
├── data/
│   ├── raw/                        # Original CSV datasets
│   └── processed/
│       └── monthly_model_data.csv  # Cleaned monthly-level modeling dataset
├── notebooks/
│   └── milestone_2/
│       ├── data_wrangling.ipynb          # Feature engineering and master table
│       ├── data_modeling.ipynb           # Model training and evaluation
│       ├── data_visualization_static.ipynb  # Interactive dashboard
│       └── milestone1_analysis.ipynb     # EDA and database creation
├── diary/                          # Weekly reflection entries
├── docs/                           # Supporting documents
├── sql/
│   └── schema.sql                  # Relational database schema
├── humanitarian.db                 # SQLite database
├── README.md
└── requirements.txt

## Milestone 1 — Exploratory Analysis
- **Total Media Coverage:** Bar plot ranking crises by total article count. Gaza has the
  highest coverage, followed by Ukraine, Syria, and Afghanistan. Chad has the lowest.
- **Monthly Coverage Trends:** Line plot of articles per crisis over time. Syria and Yemen
  have long-running attention; Gaza shows high recent spikes.
- **Coverage by Outlet:** Al Jazeera leads total coverage, followed by Reuters and NYT,
  with a steady decline across remaining outlets.
- **Sentiment per Entity:** Hamas is predominantly negatively portrayed; Zelensky
  predominantly positive.
- **Framing Distribution:** Humanitarian framing dominates across all articles; legal
  framing is least common.
- **Crisis Summary Table:** Overview of all crises with metrics including raw coverage,
  coverage per day, coverage per funding, and coverage per people affected.

## Milestone 2 — Data Wrangling, Modeling, and Visualization

### Data Wrangling
The master modeling dataset was built at the monthly level (734 rows, one per crisis
per month) rather than the crisis level, enabling proper train/test evaluation.

Feature engineering included:
- `months_since_start` — months elapsed since each crisis began
- `is_onset` — flag for the first 3 months of a crisis (coverage spike period)
- `log_coverage` — log-transformed monthly article count (modeling target)
- `top3_outlet_ratio` — share of coverage from the top 3 outlets per crisis
- `post_onset_ratio` — ratio of post-onset to onset coverage (decay measure)
- Framing ratios for economic, geopolitical, and humanitarian frames (Gaza and
  Ukraine only; filled with 0 for other crises)

### Data Modeling
Four regression models were compared using an 80/20 temporal train/test split:

| Model | R2 | RMSE | MAE |
|---|---|---|---|
| Linear Regression | 0.653 | 0.760 | 0.615 |
| Ridge Regression | 0.656 | 0.757 | 0.612 |
| Decision Tree | 0.674 | 0.737 | 0.602 |
| Random Forest | 0.472 | 0.937 | 0.769 |

Decision Tree achieved the highest test R2. Random Forest underperformed relative
to expectations, likely because the dataset relationships are largely linear and
framing features are sparse across most crises.

Key finding: `crisis_days` and `fund_required` are the strongest predictors of
monthly coverage. Crisis severity in terms of people affected shows little predictive
power, confirming that humanitarian scale does not drive media attention.

### Data Visualization
An interactive static dashboard built with ipywidgets covers:
- Crisis coverage landscape across four normalized metrics
- Coverage vs severity scatter plots
- Monthly timeline with smoothing toggle
- Outlet analysis (global ranking, per-crisis heatmap, concentration)
- Narrative framing distribution and per-crisis breakdown
- Entity sentiment analysis (Gaza and Ukraine only)
- Model results including comparison, feature importance, actual vs predicted,
  and residual analysis
- Composite summary panel

## How to Reproduce

### Milestone 1
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run `notebooks/milestone_2/milestone1_analysis.ipynb` to recreate the database
   and exploratory visualizations

### Milestone 2
1. Run `notebooks/milestone_2/data_wrangling.ipynb` to produce
   `data/processed/monthly_model_data.csv`
2. Run `notebooks/milestone_2/data_modeling.ipynb` to train and evaluate models
3. Run `notebooks/milestone_2/data_visualization_static.ipynb` to launch the dashboard

## Notes
- Framing, sentiment, and victim/causor data are only available for Gaza and Ukraine.
  All analyses involving these features are scoped to those two crises.
- All numerical indicators are normalized from the source datasets.
- The modeling target is log-transformed monthly coverage to reduce skew from high-
  coverage crises such as Gaza and Ukraine.