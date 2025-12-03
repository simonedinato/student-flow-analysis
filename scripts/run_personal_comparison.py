from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from IPython.display import display

BASE_DIR = Path("/Users/simonedinato/Documents/Classes/Applied Econometrics/Project")
DATA_DIR = BASE_DIR / "Datasets"

fact_path = DATA_DIR / "07_fact_tables" / "od_fact_table.csv"

fact = pd.read_csv(fact_path)

# Prepare data for Regression Models
reg_data = fact.copy()

# Dependent Variable
reg_data["log_students"] = np.log1p(reg_data["students_enrolled"])

# Independent Variables
reg_data["log_earnings_diff"] = np.log(reg_data["earnings_dest"]) - np.log(reg_data["earnings_orig"])
reg_data["log_tuition_diff"] = np.log1p(reg_data["cost_tuition_dest"]) - np.log1p(reg_data["cost_tuition_orig"])
reg_data["log_living_diff"] = np.log1p(reg_data["cost_living_dest"]) - np.log1p(reg_data["cost_living_orig"])
reg_data["log_dist"] = np.log(reg_data["dist"])
reg_data["log_gdp_dest"] = np.log(reg_data["gdp_pc_dest"])

# Restricted Model Variables
reg_data["total_cost_dest"] = reg_data["cost_tuition_dest"] + reg_data["cost_living_dest"]
reg_data["total_cost_orig"] = reg_data["cost_tuition_orig"] + reg_data["cost_living_orig"]
reg_data["roi_dest"] = reg_data["earnings_dest"] / reg_data["total_cost_dest"]
reg_data["roi_orig"] = reg_data["earnings_orig"] / reg_data["total_cost_orig"]
reg_data["log_roi_diff"] = np.log(reg_data["roi_dest"]) - np.log(reg_data["roi_orig"])

regression_cols = [
    "log_students",
    "log_earnings_diff",
    "log_tuition_diff",
    "log_living_diff",
    "log_dist",
    "comlang_off",
    "colony",
    "log_gdp_dest",
    "log_roi_diff"
]

# Drop NaNs and Infinite values
reg_data = reg_data.replace([np.inf, -np.inf], np.nan)
reg_data = reg_data.dropna(subset=regression_cols)
print(f"Regression rows: {len(reg_data)}")

model1 = smf.ols(
    "log_students ~ log_tuition_diff + log_earnings_diff + log_living_diff + log_dist + comlang_off + colony + log_gdp_dest",
    data=reg_data
).fit(cov_type='HC1')
print(model1.summary())

model2 = smf.ols(
    "log_students ~ log_tuition_diff + log_earnings_diff + log_living_diff + log_dist + comlang_off + colony + C(origin_country_code)",
    data=reg_data
).fit(cov_type='HC1')
print(model2.summary())

model3 = smf.ols(
    "log_students ~ log_roi_diff + log_dist + comlang_off + colony + C(origin_country_code)",
    data=reg_data
).fit(cov_type='HC1')
print(model3.summary())

model4 = smf.ols(
    "log_students ~ log_gdp_dest + log_dist + comlang_off + colony + C(origin_country_code)",
    data=reg_data
).fit(cov_type='HC1')
print(model4.summary())

# User Profile Data (Italy - Data Science)
user_origin = "ITA"
user_tuition = 2800
user_earnings = 29000
user_living = 12000
user_total_cost = user_tuition + user_living
user_roi = user_earnings / user_total_cost

# Select Top Destinations
destinations = ["USA", "GBR", "DEU", "FRA", "CAN"]

# Get base data for these pairs from existing dataset
# We filter for ITA origin and the selected destinations to get their specific destination values (GDP, Dist, etc.)
personal_data = reg_data[
    (reg_data["origin_country_code"] == user_origin) &
    (reg_data["destination_country_code"].isin(destinations))
].copy()

# Overwrite Origin Variables with User Specific Data
# Note: The dataset uses log1p for costs and log for earnings/distance

# Recalculate Diffs for Models 1 & 2
personal_data["log_tuition_diff"] = np.log1p(personal_data["cost_tuition_dest"]) - np.log1p(user_tuition)
personal_data["log_earnings_diff"] = np.log(personal_data["earnings_dest"]) - np.log(user_earnings)
personal_data["log_living_diff"] = np.log1p(personal_data["cost_living_dest"]) - np.log1p(user_living)

# Recalculate ROI Diff for Model 3
# ROI Dest is already in the dataset, we just need to update the diff with new Origin ROI
personal_data["log_roi_diff"] = np.log(personal_data["roi_dest"]) - np.log(user_roi)

# Model 4 (Parsimonious) uses only GDP, Dist, Culture - these remain unchanged as they are structural.

# Run Predictions
personal_data["pred_m1"] = model1.predict(personal_data)
personal_data["pred_m2"] = model2.predict(personal_data)
personal_data["pred_m3"] = model3.predict(personal_data)
personal_data["pred_m4"] = model4.predict(personal_data)

# Convert log predictions back to student counts (exp - 1)
cols_to_show = ["destination_country_code", "pred_m1", "pred_m2", "pred_m3", "pred_m4"]
results = personal_data[cols_to_show].copy()

for col in ["pred_m1", "pred_m2", "pred_m3", "pred_m4"]:
    results[col + "_count"] = np.expm1(results[col]).astype(int)

print(results[["destination_country_code", "pred_m1_count", "pred_m2_count", "pred_m3_count", "pred_m4_count"]])