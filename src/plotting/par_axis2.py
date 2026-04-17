import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# DATA
# -----------------------------
df = pd.DataFrame({
    "Design": ["Nominal", "SDO 1", "SDO 2", "MDO"],
    "w": [18, 4.0, 4.0, 4.07],
    "t": [1.8, 2.51, 2.51, 0.83],
    "m": [127e3, 71e3, 71e3, 219e3],
    "l1": [1.9, 1.38, 3.83, 2.68],
    "Ap": [0.26, 0.855, 0.404, 0.746],
    "Vacc": [6, 0.29, 2.41, 2.45],
    "P0": [3.00, 5.92, 5.91, 5.73],
    "Qpmax": [3100, 6753, 1000, 6612],
}).set_index("Design")

# -----------------------------
# BOUNDS
# -----------------------------
BOUNDS = {
    'w': (4., 24.),
    't': (0.8, 3.),
    'm': (50e3, 500e3),
    'l1': (0.1, 4.),
    'Ap': (1e-1, 1),
    'Vacc': (1e-2, 6),
    'P0': (3.00, 6.0),
    'Qpmax': (1000, 10000),
}

# -----------------------------
# NORMALIZE (0–1)
# -----------------------------
df_norm = df.copy()

for col in df.columns:
    lb, ub = BOUNDS[col]
    df_norm[col] = (df[col] - lb) / (ub - lb)

# -----------------------------
# OPTIONAL: LCOW (separate metric, normalized)
# -----------------------------
lcow = pd.Series({
    "Nominal": 3.97,
    "SDO 1": 2.39,
    "SDO 2": 2.17,
    "MDO": 1.21,
})

df_norm["LCOW"] = (lcow-lcow.min()) / (lcow.max() - lcow.min())

# -----------------------------
# ORDER
# -----------------------------
variables = ["w", "t", "m", "l1", "Ap", "Vacc", "P0", "Qpmax", "LCOW"]
df_norm = df_norm[variables]

# -----------------------------
# PLOT SETUP
# -----------------------------
df_plot = df_norm.reset_index()

x = np.arange(len(variables))

colors = {
    "Nominal": "tab:gray",
    "SDO 1": "tab:blue",
    "SDO 2": "tab:purple",
    "MDO": "tab:green",
}

linestyles = {
    "Nominal": "-",
    "SDO 1": "-",
    "SDO 2": "-",
    "MDO": "-",
}

alphas = {
    "Nominal": 0.3,
    "SDO 1": 0.5,
    "SDO 2": 0.5,
    "MDO": 1.0,
}

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 5))

for design in df_plot["Design"]:
    y = df_plot[df_plot["Design"] == design][variables].values.flatten()

    ax.plot(
        x,
        y,
        label=design,
        color=colors.get(design, "black"),
        linestyle=linestyles.get(design, "-"),
        linewidth=2,
        alpha=alphas.get(design, 1.0)
    )

# -----------------------------
# FORMATTING
# -----------------------------
ax.set_xticks(x)
ax.set_xticklabels(variables, rotation=45)

ax.set_ylim(0, 1)

ax.set_ylabel("Normalized Value (0 = lower bound, 1 = upper bound)")
ax.set_title("Parallel Coordinates Plot (Design Variable Bounds Normalization)")

ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.show()