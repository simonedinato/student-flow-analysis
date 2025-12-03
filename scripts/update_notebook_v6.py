import nbformat

nb_path = "scripts/regression_models.ipynb"
nb = nbformat.read(nb_path, as_version=4)

# We need to find the cell that saves the CSV and update the path
# It's the same cell "personal_est_code" we updated before.

new_code = """# User Profile Data (Italy - Data Science)
user_origin = "ITA"
user_tuition = 2800
user_earnings = 29000
user_living = 12000
user_total_cost = user_tuition + user_living
user_roi = user_earnings / user_total_cost

# Select Top Destinations (Expanded List)
# Added: ESP, NLD, DNK, NOR, SWE, CHE, CHN, JPN, KOR, ARE, ITA
destinations = [
    "USA", "GBR", "DEU", "FRA", "CAN", 
    "ESP", "NLD", "DNK", "NOR", "SWE", "CHE", 
    "CHN", "JPN", "KOR", "ARE", "ITA"
]

# --- FETCH DATA FROM RAW FACT TABLE ---
# We use 'fact' instead of 'reg_data' because 'reg_data' dropped rows with missing values
# We filter for ITA origin and the selected destinations
personal_data = fact[
    (fact["origin_country_code"] == user_origin) &
    (fact["destination_country_code"].isin(destinations))
].copy()

# Filter for the latest year available for each destination
if "year" in personal_data.columns:
    personal_data = personal_data.sort_values("year", ascending=False).drop_duplicates(subset=["destination_country_code"])

# Ensure all structural variables are present (fill from reg_data logic if needed)
# The raw 'fact' table has 'gdp_pc_dest', 'dist', 'comlang_off', 'colony'
# We need to create the log variables

# --- INJECT MISSING DATA (WEB SCRAPED) ---
# Dictionary of missing data
# Format: Country Code: {col: value}
missing_data_map = {
    "CHN": {
        "cost_tuition_dest": 6500,   # ~Avg for Master's
        "earnings_dest": 53000,      # ~Entry Level Data Scientist
        "cost_living_dest": 12000    # ~Major city student living
    },
    "KOR": {
        "cost_tuition_dest": 13000,  # ~Avg Private Uni
        "earnings_dest": 67000,      # ~Entry Level
        "cost_living_dest": 9000     # ~Student avg
    },
    "ARE": {
        "cost_tuition_dest": 25000,  # ~Avg International Uni
        "cost_living_dest": 18000    # ~Mid-range student living
        # Earnings already in dataset (~73k)
    },
    "ITA": {
        "dist": 0.0001,              # Hardcoded small distance for internal flow
        "cost_tuition_dest": user_tuition,
        "earnings_dest": user_earnings,
        "cost_living_dest": user_living
    }
}

# Apply the manual data
for country, data in missing_data_map.items():
    mask = personal_data["destination_country_code"] == country
    if mask.any():
        for col, val in data.items():
            personal_data.loc[mask, col] = val
    else:
        print(f"Warning: {country} not found in raw fact rows.")

# -----------------------------------------

# Now calculate the regression variables
# Dependent Variable (placeholder, not needed for prediction but good for consistency)
personal_data["log_students"] = np.log1p(personal_data["students_enrolled"])

# Independent Variables
personal_data["log_earnings_diff"] = np.log(personal_data["earnings_dest"]) - np.log(user_earnings)
personal_data["log_tuition_diff"] = np.log1p(personal_data["cost_tuition_dest"]) - np.log1p(user_tuition)
personal_data["log_living_diff"] = np.log1p(personal_data["cost_living_dest"]) - np.log1p(user_living)
personal_data["log_dist"] = np.log(personal_data["dist"])
personal_data["log_gdp_dest"] = np.log(personal_data["gdp_pc_dest"])

# Restricted Model Variables
personal_data["total_cost_dest"] = personal_data["cost_tuition_dest"] + personal_data["cost_living_dest"]
personal_data["roi_dest"] = personal_data["earnings_dest"] / personal_data["total_cost_dest"]
personal_data["log_roi_diff"] = np.log(personal_data["roi_dest"]) - np.log(user_roi)

# Drop any rows that STILL have NaNs in the required columns (e.g. if we missed some data)
# But we want to keep as many as possible.
# Model 4 only needs GDP, Dist, Culture.
# Model 2 needs Tuition, Earnings.

# Run Predictions
# We handle NaNs by filling with 0 or dropping, but let's try to predict where possible.
# If a row has NaN for a model's features, predict() will return NaN.

personal_data["pred_m1"] = model1.predict(personal_data)
personal_data["pred_m2"] = model2.predict(personal_data)
personal_data["pred_m3"] = model3.predict(personal_data)
personal_data["pred_m4"] = model4.predict(personal_data)

# Convert log predictions back to student counts (exp - 1)
results = personal_data[["destination_country_code"]].copy()

for col in ["pred_m1", "pred_m2", "pred_m3", "pred_m4"]:
    # Calculate raw counts
    results[col + "_count"] = np.expm1(personal_data[col])
    
    # Calculate Probabilities (Weights)
    # The probability of choosing destination j is Count_j / Sum(Counts)
    # We ignore NaNs in the sum
    total_flow = results[col + "_count"].sum()
    results[col + "_prob"] = results[col + "_count"] / total_flow

# Save Results to CSV for Visualization
# FIX: Use ../Datasets because notebook runs in scripts/
results.to_csv("../Datasets/personalized_predictions.csv", index=False)
print("Results saved to ../Datasets/personalized_predictions.csv")

# Display Results as Probabilities
print("Estimated Probability of Choosing Each Destination (Weights):")
cols_prob = ["destination_country_code", "pred_m1_prob", "pred_m2_prob", "pred_m3_prob", "pred_m4_prob"]
display(results[cols_prob].set_index("destination_country_code").style.format({
    "pred_m1_prob": "{:.1%}",
    "pred_m2_prob": "{:.1%}",
    "pred_m3_prob": "{:.1%}",
    "pred_m4_prob": "{:.1%}"
}).background_gradient(cmap="Blues", axis=0))"""

for cell in nb.cells:
    if cell.get("id") == "personal_est_code":
        cell.source = new_code

nbformat.write(nb, nb_path)
print("Notebook updated successfully.")
