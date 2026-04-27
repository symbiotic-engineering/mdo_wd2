import sys
import os
import pandas as pd
import plotly.graph_objects as go
parent_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
sys.path.append(parent_folder)

# -----------------------------
# DESIGN SPACE BOUNDS
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
})

# LCOW (performance metric)
df["LCOW"] = [3.97, 2.39, 2.17, 1.21]

# -----------------------------
# VARIABLES
# -----------------------------
variables = ["w", "t", "m", "l1", "Ap", "Vacc", "P0", "Qpmax"]

# -----------------------------
# DESIGN ENCODING (IMPORTANT)
# -----------------------------
design_order = ["Nominal", "SDO 1", "SDO 2", "MDO"]

design_code = {d: i for i, d in enumerate(design_order)}
df["code"] = df["Design"].map(design_code)

colorscale = [
    [0.00, "gray"],
    [0.33, "blue"],
    [0.66, "purple"], 
    [1.00, "crimson"] 
]

# -----------------------------
# DIMENSIONS (FULL DESIGN SPACE)
# -----------------------------
dimensions = [
    dict(
        label=v,
        values=df[v],
        range=BOUNDS[v]
    )
    for v in variables
]

dimensions.append(
    dict(
        label="LCOW",
        values=df["LCOW"]
    )
)

# -----------------------------
# PARALLEL COORDINATES
# -----------------------------
fig = go.Figure(
    go.Parcoords(
        line=dict(
            color=df["code"],
            colorscale=colorscale,
            cmin=0,
            cmax=len(design_order) - 1,
            showscale=False
        ),
        dimensions=dimensions,

        labelfont=dict(size=16, color="black"),
        tickfont=dict(size=16, color="black"),
        rangefont=dict(size=16, color="black"),

    )
)

fig.show()