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
    "Qpmax": [3100, 6753, 1000, 6612],
}).set_index("Design")

# -----------------------------
# BASELINE (Nominal design)
# -----------------------------
baseline = df.loc["Nominal"]

# -----------------------------
# LCOW
# -----------------------------
lcow = pd.Series({
    "Nominal": 3.97,
    "SDO 1": 2.39,
    "SDO 2": 2.17,
    "MDO": 1.21,
})

# -----------------------------
# NORMALIZE ABOUT BASELINE
# -----------------------------
df_dev = df.copy()

for col in df.columns:
    df_dev[col] = (df[col] - baseline[col]) / baseline[col]

# -----------------------------
# ADD LCOW (normalized separately)
# -----------------------------
lcow_norm = (lcow - lcow["Nominal"]) / (lcow["Nominal"])
df_dev["LCOW"] = lcow_norm

# -----------------------------
# ORDER AXES
# -----------------------------
variables = ["w", "t", "m", "l1", "Ap", "Vacc", "Qpmax", "LCOW"]
df_dev = df_dev[variables]

# -----------------------------
# PLOTTING SETUP
# -----------------------------
df_plot = df_dev.reset_index()
x = np.arange(len(variables))

colors = {
    "Nominal": "red",
    "SDO 1": "gray",
    "SDO 2": "gray",
    "MDO": "tab:green",
}

linestyles = {
    "Nominal": "--",
    "SDO 1": "--",
    "SDO 2": ":",
    "MDO": "-",
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
        alpha=0.9
    )

# -----------------------------
# FORMATTING
# -----------------------------
ax.set_xticks(x)
ax.set_xticklabels(variables, rotation=45)

#ax.axhline(0, color="black", linewidth=1, linestyle=":", alpha=0.6)

ax.set_ylabel("Fractional Change from Nominal")
#ax.set_title("Parallel Coordinates (Normalized about Nominal)")

ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.show()