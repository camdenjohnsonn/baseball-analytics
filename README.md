# Baseball Analytics & Player Performance Prediction

A full end-to-end data science project using the Lahman Baseball Database to predict player performance and Hall of Fame induction probability.

## Project Overview

This project demonstrates an industry-level analytics pipeline including SQL database design, Python data cleaning, exploratory data analysis, and machine learning modeling.

**Two models were built:**
- **OPS Prediction** — predicts a player's offensive performance next season using Ridge Regression (RMSE: 0.079, R²: 0.432)
- **Hall of Fame Prediction** — predicts HOF induction probability using Logistic Regression (AUC-ROC: 0.896, Recall: 0.87)

## Key Findings

- Current season OPS is the strongest predictor of next season performance
- Walk rate (BB) is one of the most consistent and repeatable offensive skills
- Career longevity is the strongest predictor of Hall of Fame induction
- Linear models outperformed ensemble methods (Random Forest, XGBoost) on aggregated baseball statistics
- Salary shows only weak correlation with OPS, supporting the Moneyball hypothesis

## Project Structure
```
baseball_analytics/
├── sql/
│   ├── 01_ingest.py          # Loads CSVs into SQLite database
│   ├── 02_exploration.sql    # Analytical views with CTEs and window functions
│   └── 03_runner.py          # Executes SQL views and loads DataFrames
├── notebooks/
│   ├── cleaning.ipynb     # Data cleaning and feature engineering
│   ├── eda_visualization.ipynb  # Exploratory data analysis
│   ├── ops_modeling.ipynb       # OPS prediction models
│   └── hof_modeling.ipynb       # Hall of Fame prediction models
├── reports/
│   └── baseball_report.py    # PDF report generation
├── outputs/
│   ├── figures/              # Saved visualizations
│   └── baseball_report.pdf   # Final PDF report
└── README.md
```

## Tech Stack

| Tool | Purpose |
|---|---|
| SQLite | Database storage and querying |
| Python | Data cleaning, modeling, reporting |
| pandas / numpy | Data manipulation |
| matplotlib / seaborn | Visualization |
| scikit-learn | ML pipeline and evaluation |
| XGBoost | Gradient boosting models |
| SHAP | Model explainability |
| reportlab | PDF report generation |

## Data Source

[Lahman Baseball Database](https://www.seanlahman.com/baseball-archive/statistics/) — comprehensive MLB statistics from 1871 to 2025, maintained by Sean Lahman and the Chadwick Baseball Bureau.

## Report

📄 [View the full PDF report](outputs/baseball_report.pdf)

## Author

Camden Johnson