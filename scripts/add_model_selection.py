import json
from pathlib import Path

NB_PATH = Path("/Users/simonedinato/Documents/Classes/Applied Econometrics/Project/scripts/regression_models.ipynb")

def format_source(text):
    lines = text.split('\n')
    return [line + '\n' for line in lines[:-1]] + [lines[-1]]

def update_notebook():
    with open(NB_PATH, 'r') as f:
        nb = json.load(f)
    
    # Find the "Evaluation of Model 4" cell
    for cell in nb['cells']:
        if "### Evaluation of Model 4" in "".join(cell['source']):
            print("Found Evaluation of Model 4 cell.")
            cell['source'] = format_source("""### Evaluation of Model 4
Model 4, our Parsimonious Gravity Model, focuses on the structural determinants of student flows.
- **Goodness of Fit**: The $R^2$ is around 0.41. This is lower than Model 2 (0.52), but this is expected as we dropped the tuition and earnings variables.
- **Coefficients**:
    - **Destination GDP**: Positive and significant (+0.74). Economic opportunity is a major pull factor.
    - **Distance**: Surprisingly **positive** (+0.10). In standard gravity models, distance is negative. However, with Origin Fixed Effects, this might capture that students from certain regions prefer further destinations (e.g., Asian students going to US/UK vs nearby).
    - **Cultural Ties**: Common Language and Colonial ties are strongly positive.

### Conclusion: Which Model is "Best"?
- **Model 2 (Origin FE)** has the highest explanatory power ($R^2 \\approx 0.52$). However, the positive coefficient on Tuition suggests **endogeneity** (tuition proxies for quality). It is the best model for *prediction* but potentially biased for *causal inference* regarding costs.
- **Model 4 (Parsimonious)** has a lower $R^2$ ($0.41$) but avoids the biased cost variables. It provides cleaner estimates for the structural gravity forces (GDP, Culture).

**Recommendation**: We prefer **Model 4** as the structural baseline because it avoids the misleading "positive tuition" effect, even though it explains less total variance.""")
            
    with open(NB_PATH, 'w') as f:
        json.dump(nb, f, indent=1)
    print("Notebook updated.")

if __name__ == "__main__":
    update_notebook()
