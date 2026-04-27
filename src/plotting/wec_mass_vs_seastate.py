import pandas as pd
import matplotlib.pyplot as plt

# Load your original cluster centers
clusters = pd.read_csv("data/seastate_clusters_10/clusterclusters.csv")

# Load this new dataset
cols = [
    "seastate_id","width","thickness","wec_mass","hinge2joint",
    "piston_area","accum_volume","accum_P0","capacity","LCOW"
]
params = pd.read_csv("data/sensitivity_results.csv", names=cols)

params["LCOW"] = (
    params["LCOW"]
    .astype(str)
    .str.strip("[]")   # remove brackets
    .astype(float)     # convert to number
)

# If rows correspond directly, just combine them:
df = pd.concat([clusters, params], axis=1)

# Plot with color = fitness (you can change this)
plt.figure()
sc = plt.scatter(
    df["center_Tp"],
    df["center_Hs"],
    c=df["wec_mass"],          # <-- color dimension
    s=100
)

plt.colorbar(sc, label="var")

plt.xlabel("Tp (s)")
plt.ylabel("Hs (m)")
plt.grid(True)

plt.show()