import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_folder)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.params import BOUNDS

colors = {
    "Nominal": "tab:gray",
    "SDO 1": "tab:blue",
    "SDO 2": "tab:purple",
    "MDO": "tab:green",
    #"Initial": "tab:red",
}

linestyles = {
    "Nominal": "-",
    "SDO 1": "-",
    "SDO 2": "-",
    "MDO": "-",
}


# Design variable data (NO LCOW)

data = {
    "Variable": ["width", "thickness", "wec_mass", "hinge2joint", "piston_area", "accum_volume", "accum_P0", "capacity"],
    "Nominal": [18, 1.8, 127e3, 1.9, 0.26, 6, 3.00, 3100],
    "SDO 1":   [4.0, 2.51, 71e3, 1.38, 0.855, 0.29, 5.92, 6753],
    "SDO 2":   [4.0, 2.51, 71e3, 3.83, 0.404, 2.41, 5.91, 1000],
    "MDO":     [4.07, 0.83, 219e3, 2.68, 0.746, 2.45, 5.73, 6612],
    #"Initial": [11.3, 1.99, 396e3, 3.25, 0.859, 4.57, 5.95, 4882],
}

df = pd.DataFrame(data).set_index("Variable")

# Normalize using bounds
df_norm = df.copy()

for var in df.index:
    lb, ub = BOUNDS[var]
    df_norm.loc[var] = (df.loc[var] - lb) / (ub - lb)

# Flip variables where LOWER is better
#lower_better = ["t", "m"]  # maybe also w depending on interpretation

#for var in lower_better:
#    df_norm.loc[var] = 1 - df_norm.loc[var]

# Radar setup
labels = [
    r"$w$",
    r"$t$",
    r"$m$",
    r"$\ell_1$",
    r"$A_p$",
    r"$V_{acc}$",
    r"$P_0$",
    r"$Q_{p,\max}$"
]
num_vars = len(labels)

angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

# Orientation
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

lcow = {
    "Nominal": 3.97,
    "SDO 1": 2.39,
    "SDO 2": 2.17,
    "Initial": 1.68,
    "MDO": 1.21,
}

# Normalize LCOW (inverted so better = bigger)
vals = np.array(list(lcow.values()))
lcow_norm = (vals.max() - vals) / (vals.max() - vals.min())

lcow_scaled = dict(zip(lcow.keys(), lcow_norm))

def lw_map(x, lw_min=1.0, lw_max=4.0):
    return lw_min + x * (lw_max - lw_min)

# Plot each design
for col in df_norm.columns:
    values = df_norm[col].tolist()
    values += values[:1]
    lw = lw_map(lcow_scaled[col])
    
    ax.plot(
        angles,
        values,
        linewidth=lw,
        label=col,
        linestyle=linestyles.get(col, "-"),
        color=colors.get(col, "black")
    )

    ax.fill(
        angles,
        values,
        color=colors.get(col, "black"),
        alpha=0.05 + 0.15 * lcow_scaled[col]
    )

# Labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

ax.set_ylim(0, 1)

# Legend outside
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1))

plt.tight_layout()
plt.show()