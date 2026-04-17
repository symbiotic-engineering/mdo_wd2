import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# DATA
# -----------------------------
df = pd.DataFrame({
    "Variable": ["w", "t", "m", "l1", "Ap", "Vacc", "P0", "Qpmax"],
    "Nominal": [18, 1.8, 127e3, 1.9, 0.26, 6, 3.00, 3100],
    "SDO 1":   [4.0, 2.51, 71e3, 1.38, 0.855, 0.29, 5.92, 6753],
    "SDO 2":   [4.0, 2.51, 71e3, 3.83, 0.404, 2.41, 5.91, 1000],
    "MDO":     [4.07, 0.83, 219e3, 2.68, 0.746, 2.45, 5.73, 6612],
}).set_index("Variable")

# -----------------------------
# BASELINE (Nominal)
# -----------------------------
nominal = df["Nominal"]

# -----------------------------
# FRACTIONAL DEVIATION
# (same idea as your parallel coords)
# -----------------------------
df_dev = (df - nominal) / nominal

# -----------------------------
# VISUAL SCALING (KEY STEP)
# makes plot readable WITHOUT destroying meaning
# -----------------------------
scale = 2.5  # tune this (2–4 is typical)

df_plot = 0.5 + scale * df_dev

# optional safety clamp for radar geometry
df_plot = df_plot.clip(0, 1)

# -----------------------------
# LCOW (same as before)
# -----------------------------
lcow = {
    "Nominal": 3.97,
    "SDO 1": 2.39,
    "SDO 2": 2.17,
    "MDO": 1.21,
}

lcow = pd.Series(lcow)

lcow_norm = (lcow.max() - lcow) / (lcow.max() - lcow.min())

# -----------------------------
# RADAR SETUP
# -----------------------------
labels = ["w", "t", "m", "l1", "Ap", "Vacc", "P0", "Qpmax"]
num_vars = len(labels)

angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# -----------------------------
# LINE STYLE CONTROL (edit freely)
# -----------------------------
colors = {
    "Nominal": "gray",
    "SDO 1": "tab:blue",
    "SDO 2": "tab:orange",
    "MDO": "tab:green",
}

linestyles = {
    "Nominal": "--",
    "SDO 1": "-",
    "SDO 2": "-",
    "MDO": "-",
}

# LCOW → line emphasis
def lw_map(x):
    return 1 + 3 * x

# -----------------------------
# PLOT
# -----------------------------
for col in df_plot.columns:
    values = df_plot[col].tolist()
    values += values[:1]

    lw = lw_map(lcow_norm[col])

    ax.plot(
        angles,
        values,
        label=col,
        color=colors.get(col, "black"),
        linestyle=linestyles.get(col, "-"),
        linewidth=2,
        alpha=0.9
    )

    ax.fill(angles, values, alpha=0.05 + 0.15 * lcow_norm[col])

# -----------------------------
# FORMATTING
# -----------------------------
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

ax.set_ylim(0, 1)

ax.axhline(0.5, color="black", linestyle=":", linewidth=1, alpha=0.5)

ax.set_title("Design Deviations from Nominal (Radar View)")

ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1))

plt.tight_layout()
plt.show()