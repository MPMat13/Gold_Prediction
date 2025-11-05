# 🪙 Gold Price Prediction — Machine Learning for Non-Stationary Time Series

## Overview  
This project explores machine-learning methods for predicting gold prices using engineered lag and rolling features.  
The main objective was to understand how **validation strategy** affects model reliability when dealing with **non-stationary financial data**.

## Key Features  
- 📊 **Data Source:** Yahoo Finance, retrieved via a custom `DataScrapper` class  
- 🧩 **Feature Engineering:** Lagged prices, rolling means, and smoothed trend indicators  
- 🧠 **Models Used:** Linear Regression, Ridge, Lasso, Decision Tree, Random Forest, Gradient Boosting, XGBoost  
- 🧪 **Validation Approaches:**  
  - **Time-series split:** realistic chronological testing that revealed weak forward generalization  
  - **Random split:** exploratory setup showing strong in-sample fit but potential overfitting  

## Insights  
- Highlights the critical difference between random and time-aware validation in financial forecasting.  
- Demonstrates that models may appear strong under random splits while failing to generalize over time.  
- Emphasizes the importance of stationarity, validation discipline, and feature interpretability.  
- Encourages a practical, experiment-driven mindset when applying ML to volatile markets.  

## Next Steps  
- Extend experiments with models designed for temporal data (e.g., RNNs, Transformers).  
- Integrate macroeconomic indicators or volatility metrics to enrich the feature space.  
- Apply rolling retraining and backtesting for more realistic performance evaluation.  

---

**Author:** [Your Name]  
**Focus:** Data Science / Machine Learning / Time-Series Analysis  
**Goal:** Exploring predictive modeling challenges in non-stationary financial data
