# Humanitarian Media Coverage Analysis

## **Project Overview**
This project investigates how global humanitarian crises are covered in the media. Using publicly available datasets, we analyze the volume, distribution, and framing of news coverage across multiple crises, outlets, and time periods. The aim is to assess whether media attention aligns with measurable humanitarian indicators such as number of people affected, funds required, and crisis duration, and to explore the structural and narrative factors influencing coverage patterns.

## **Data Sources**
- **Crises data:** Overview of humanitarian crises including start date, funds required, people affected, and coverage metrics.  
- **Monthly coverage:** Time-series data showing the number of articles published per crisis per month.  
- **Outlet coverage:** Number of articles published per media outlet for each crisis.  
- **Framing data:** Classification of articles based on narrative frame (e.g., humanitarian, economic, geopolitical).  
- **Sentiment data:** Sentiment of media mentions per entity within crisis coverage.  
- **Victim/Causor data:** Mentions of victims or causative actors in each article.

## **Project Structure**
- **`schema.sql`** – Defines the relational database structure, including tables for crises, monthly coverage, outlet coverage, framing, sentiment, and victim/causor.  
- **`milestone1.ipynb`** – Notebook containing data loading, database creation, and exploratory data analysis.  
- **`data/raw/`** – Folder containing all input CSV datasets.  
- **`humanitarian.db`** – SQLite database created from the raw datasets.  

## **Exploratory Analysis**
- **Total Media Coverage:** Bar plot ranking crises by total article count. Gaza has the highest coverage, followed by Ukraine, Syria, and Afghanistan. Chad has the lowest coverage.  
- **Monthly Coverage Trends:** Line plot of articles per crisis over time. Syria and Yemen have long-running attention; Gaza shows high recent spikes.  
- **Coverage by Outlet:** Horizontal bar plot of total articles per media outlet. **Al Jazeera** leads significantly, followed by Reuters, then NYT, with a steady decline thereafter.  
- **Sentiment per Entity:** Analysis of positive, neutral, and negative mentions per entity across crises. Hamas is predominantly negative; Zelensky predominantly positive.  
- **Framing Distribution:** Bar plots showing the number of articles per narrative frame. Humanitarian framing dominates; legal framing has the least coverage.  
- **Crisis Summary Table:** Overview of all crises with metrics including raw coverage, coverage per day, coverage per funding, and coverage per people affected.

## **Reflection and Next Steps**
- Data exploration highlighted uneven media attention across crises and outlets, with coverage not fully explained by crisis severity metrics.  
- Structured database design improved reproducibility and analytical flexibility.  
- **Next steps** include correlation and regression analyses to identify predictors of media coverage, integration of framing and sentiment into modeling, and investigation of outlet-specific reporting patterns.

## **How to Use**
1. Clone the repository.  
2. Ensure Python dependencies are installed: `pandas`, `numpy`, `sqlite3`, `matplotlib`, `seaborn`.  
3. Run `milestone1.ipynb` to reproduce data loading, database creation, and exploratory visualizations.  
4. Extend analysis in future sprints for hypothesis testing and predictive modeling.

## **Notes**
- All numerical indicators (funds required, people affected) are normalized/scaled from the source datasets; original transformation methods are not provided.  
- Observations are based on pre-processed datasets; missing values and anomalies are minimal due to source standardization.  
- The project focuses on descriptive patterns and exploratory insights; causal inferences require further analysis in subsequent sprints.