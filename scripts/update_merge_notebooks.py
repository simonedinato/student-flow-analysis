import json
from pathlib import Path

BASE_DIR = Path("/Users/simonedinato/Documents/Classes/Applied Econometrics/Project/scripts")

def format_source(text):
    lines = text.split('\n')
    return [line + '\n' for line in lines[:-1]] + [lines[-1]]

def update_notebook(path, updates):
    with open(path, 'r') as f:
        nb = json.load(f)
    
    for idx, content in updates.items():
        if idx < len(nb['cells']):
            if nb['cells'][idx]['cell_type'] == 'markdown':
                nb['cells'][idx]['source'] = format_source(content)
                print(f"Updated cell {idx} in {path.name}")
            else:
                print(f"Warning: Cell {idx} in {path.name} is not markdown, skipping.")
        else:
            # Append if index is out of range (for new cells)
            new_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": format_source(content)
            }
            nb['cells'].append(new_cell)
            print(f"Appended new cell to {path.name}")

    with open(path, 'w') as f:
        json.dump(nb, f, indent=1)

# 1. merge_01_mobility.ipynb
nb1_updates = {
    0: """# Step 1: Mobility Data Construction

## Objective
Construct the base panel dataset of international student flows (Origin-Destination-Year).

## Data Sources
1.  **OECD Mobility Data**: Detailed bilateral student flows (Enrolled, Graduated, New Entrants).
2.  **UNESCO Inbound/Outbound**: Aggregate totals used to estimate bilateral flows where direct OECD data is missing.

## Methodology: Gravity Weighting
Many country pairs have missing bilateral flow data. To maximize coverage, we use a **Gravity Weighting** approach:
1.  Calculate the **share of total outbound students** from Origin $i$ that go to Destination $j$ (based on available data or regional averages).
2.  Multiply this share by the **total outbound students** from Origin $i$ (UNESCO) to estimate the bilateral flow $Students_{ij}$.
3.  Where direct OECD data exists (`flow_source = 'reported'`), we prioritize it over estimates (`flow_source = 'estimated'`).

## Validation
We verify that the calculated weights sum to 1 for each origin-year, ensuring no students are "lost" or double-counted."""
}

# 2. merge_02_earnings_03_costs.ipynb
nb2_updates = {
    0: """# Step 2 & 3: Earnings and Costs Data

## Objective
Enrich the panel with economic determinants: Earnings (Benefits) and Costs (Tuition + Living).

## Data Sources
1.  **ILO / World Bank**: Median earnings by country.
2.  **Education Costs Database**: Tuition fees for international students.
3.  **Numbeo / World Bank**: Cost of living indices.

## Methodology
- **Currency Conversion**: All values are converted to **USD (PPP)** to ensure comparability across countries.
- **Inflation Adjustment**: Values are adjusted to constant base-year dollars.
- **Gap Calculation**: We calculate the *difference* between Destination and Origin:
    - `log_earnings_diff` = $\ln(Earnings_{dest}) - \ln(Earnings_{orig})$
    - `log_tuition_diff` = $\ln(Tuition_{dest}) - \ln(Tuition_{orig})$
    - `log_living_diff` = $\ln(Living_{dest}) - \ln(Living_{orig})$""",
    2: """## 2.1 Earnings Data
We load median income data and fill gaps using GDP per capita (PPP) where direct income data is missing.""",
    6: """## 2.2 Costs Data
We load tuition and living cost data. Note that tuition is specific to *international* students, which is often higher than domestic tuition."""
}

# 3. merge_04_employability.ipynb
nb3_updates = {
    0: """# Step 4: Employability and Quality Proxies

## Objective
Add proxies for the "Quality" and "Opportunity" of the destination, which are key pull factors.

## Data Sources
1.  **Youth Transition (TRANS)**: Employment rates for recent graduates (aged 25-29).
2.  **University Rankings**: (Optional) Presence of top-ranked universities.

## Methodology
- **Employment Rate**: We use the employment rate of tertiary graduates as a proxy for the *probability* of finding a job after graduation.
- **Imputation**: Missing years are imputed using nearest-neighbor interpolation (±1 or ±2 years) to maximize coverage.""",
}

# 4. merge_06_macro.ipynb
nb4_updates = {
    0: """# Step 6: Macro and Gravity Variables

## Objective
Finalize the dataset by adding standard Gravity Model variables and Macroeconomic controls.

## Data Sources
1.  **CEPII Gravity Database**:
    - **Distance**: Geodesic distance between population centers ($dist_{ij}$).
    - **Common Language**: Official or major languages spoken in both countries ($comlang\_off$).
    - **Colonial Ties**: Historical colonial relationships ($colony$).
2.  **World Bank WDI**: GDP per capita (PPP) for both Origin and Destination.

## Methodology
- **Gravity Variables**: These are time-invariant structural determinants of migration.
- **GDP per Capita**: Used as a robust proxy for general economic development and quality of life.
- **Final Merge**: All components (Mobility, Earnings, Costs, Employability, Gravity) are merged into the final `od_fact_table.csv` used for regression analysis.""",
}

# Execute Updates
print("Updating merge_01_mobility.ipynb...")
update_notebook(BASE_DIR / "merge_01_mobility.ipynb", nb1_updates)

print("Updating merge_02_earnings_03_costs.ipynb...")
update_notebook(BASE_DIR / "merge_02_earnings_03_costs.ipynb", nb2_updates)

print("Updating merge_04_employability.ipynb...")
update_notebook(BASE_DIR / "merge_04_employability.ipynb", nb3_updates)

print("Updating merge_06_macro.ipynb...")
update_notebook(BASE_DIR / "merge_06_macro.ipynb", nb4_updates)

print("All notebooks updated successfully.")
