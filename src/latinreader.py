import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import openmdao.api as om
from src.runner import RunWDDS
import numpy as np

cr = om.CaseReader("run_latin_out/508cases.sql")
cases = cr.list_cases('driver',recurse=True)
dvs = ["width","thickness","wec_mass","hinge2joint","piston_area","accum_volume","accum_P0","capacity"]
var_values = {case:{var:cr.get_case(case).outputs[var] for var in dvs } for case in cases }
obj_values = {case:cr.get_case(case).outputs["LCOW"] for case in cases }


# Filter cases where LCOW is not 1000 or NaN
cases = {case: value for case, value in obj_values.items() if value != np.nan}
valid_cases = {case: value for case, value in obj_values.items() if value < np.inf}
print(f"there are {len(valid_cases)} valid cases out of {len(cases)} total cases")

# Use the filtered cases to create a new var_values dictionary
filtered_var_values = {case: var_values[case] for case in valid_cases}
filtered_obj_values = valid_cases  # Since valid_cases already contains LCOW values

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Convert filtered data to a DataFrame
df = pd.DataFrame.from_dict(filtered_var_values, orient="index")
df["LCOW"] = pd.Series(filtered_obj_values)
df = df.applymap(lambda x: x.item() if isinstance(x, np.ndarray) and x.size == 1 else (np.nan if isinstance(x, np.ndarray) else x))

# Compute correlations
corr_matrix = df.corr()["LCOW"].drop("LCOW")  # Drop self-correlation

# Plot correlation bar chart
plt.figure(figsize=(8, 5))
sns.barplot(x=corr_matrix.index, y=corr_matrix.values, palette="coolwarm")
plt.xlabel("Design Variables")
plt.ylabel("Correlation with LCOW")
plt.title("LCOW Sensitivity to Design Variables")
plt.xticks(rotation=45)
plt.show()

# Find the case with the minimum LCOW
min_lcow_case = min(filtered_obj_values, key=filtered_obj_values.get)
min_lcow_value = filtered_obj_values[min_lcow_case]

# Find the case with the maximum LCOW
max_lcow_case = max(obj_values, key=obj_values.get)
max_lcow_value = obj_values[max_lcow_case]

print(f"Case with minimum LCOW: {min_lcow_case}")
print(f"Minimum LCOW value: {min_lcow_value}")
print(f"Design Variables:{filtered_var_values[min_lcow_case]}")
print(f"Case with maximum LCOW: {max_lcow_case}")
print(f"Maximum LCOW value: {max_lcow_value}")
print(f"Design Variables:{var_values[max_lcow_case]}")
#for var in dvs:  # Loop through design variables
#    sns.scatterplot(x=df[var], y=df["LCOW"])
#    plt.xlabel(var)
#    plt.ylabel("LCOW")
#    plt.title(f"Impact of {var} on LCOW")
#    plt.show()
from sklearn.ensemble import RandomForestRegressor

# Drop NaNs
df_clean = df.dropna()

# Train a simple random forest model
X = df_clean.drop(columns=["LCOW"])
y = df_clean["LCOW"]
model = RandomForestRegressor()
model.fit(X, y)

# Get feature importances
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)

print(importances)

importances.plot(kind='bar', figsize=(10,6))
plt.xlabel("Design Variables")
plt.ylabel("Importance")
plt.title("Feature Importance from Random Forest")
plt.xticks(rotation=45)
plt.show()


from sklearn.feature_selection import mutual_info_regression

# Drop NaNs
df_clean = df.dropna()

# Compute mutual information
mi = mutual_info_regression(df_clean.drop(columns=["LCOW"]), df_clean["LCOW"])
mi_series = pd.Series(mi, index=df_clean.drop(columns=["LCOW"]).columns).sort_values(ascending=False)

print(mi_series)

import shap

explainer = shap.Explainer(model, X)  # Use trained Random Forest model
shap_values = explainer(X)

shap.summary_plot(shap_values, X)
#shap.interaction_plot(shap_values, X)
