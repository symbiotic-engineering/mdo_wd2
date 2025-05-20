import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import openmdao.api as om
from src.runner import RunWDDS
import numpy as np
import src.plotting.importance_plot as imp

cr = om.CaseReader("data/LHSampling_results/508cases.sql")
cases = cr.list_cases('driver',recurse=True)
dvs = ["width","thickness","wec_mass","hinge2joint","piston_area","accum_volume","accum_P0","capacity"]
var_values = {case:{var:cr.get_case(case).outputs[var] for var in dvs } for case in cases }
obj_values = {case:cr.get_case(case).outputs["LCOW"] for case in cases }


# Filter cases 
cases = {case: value for case, value in obj_values.items() if value != np.nan}
valid_cases = {case: value for case, value in obj_values.items() if value < 10}
print(f"there are {len(valid_cases)} valid cases out of {len(cases)} total cases")

# Use the filtered cases to create a new var_values dictionary
filtered_var_values = {case: var_values[case] for case in valid_cases}
filtered_obj_values = valid_cases  # Since valid_cases already contains LCOW values

import pandas as pd
import matplotlib.pyplot as plt


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

# Convert filtered data to a DataFrame
df = pd.DataFrame.from_dict(filtered_var_values, orient="index")
df["LCOW"] = pd.Series(filtered_obj_values)
df = df.applymap(lambda x: x.item() if isinstance(x, np.ndarray) and x.size == 1 else (np.nan if isinstance(x, np.ndarray) else x))

imp.randomtrees(df)
